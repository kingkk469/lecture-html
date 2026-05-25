"""
内嵌脚本 — 把 HTML 引用的本地图片全部转成 base64 data URI,产出一个完全自包含的单文件 HTML。

适合微信/邮件直接发给别人 — 对方双击就能看到完整效果,不需要带 images/ 文件夹。

用法:
    python scripts/inline.py <html-file> [output.html]

例:
    python scripts/inline.py my-lecture.html
    # → 产出 my-lecture.inline.html

注:
- 远程 URL (http/https) 和已经内嵌的 data: URI 会被跳过。
- 文件会变大(base64 比原图大约 33%),但所有图都打包进 1 个文件了。
"""

import base64
import mimetypes
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


IMG_PATTERN = re.compile(
    r"""((?:url\(\s*['"]?|src\s*=\s*['"]))([^'")]+\.(?:jpg|jpeg|png|gif|webp|svg))(['"]?)""",
    re.IGNORECASE,
)

# 当 HTML 在用户工作目录、而图在 skill 自带目录时,从这里兜底找图
SKILL_FALLBACK_DIR = Path(__file__).resolve().parent.parent  # scripts/.. = skill 根目录


def resolve_image(rel_url: str, html_dir: Path) -> Path | None:
    """先找 HTML 旁边,找不到再去 skill 目录兜底。"""
    primary = (html_dir / rel_url).resolve()
    if primary.is_file():
        return primary
    fallback = (SKILL_FALLBACK_DIR / rel_url).resolve()
    if fallback.is_file():
        return fallback
    return None


def to_data_uri(img_path: Path) -> str:
    mime, _ = mimetypes.guess_type(img_path.name)
    if mime is None:
        mime = "application/octet-stream"
    data = base64.b64encode(img_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    html_path = Path(sys.argv[1]).resolve()
    if not html_path.is_file():
        print(f"找不到文件:{html_path}")
        return 1

    base_dir = html_path.parent
    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2]).resolve()
    else:
        out_path = html_path.with_name(html_path.stem + ".inline.html")

    text = html_path.read_text(encoding="utf-8")
    converted, missing, skipped = [], [], 0

    def replace(match: re.Match) -> str:
        nonlocal skipped
        prefix, url, suffix = match.group(1), match.group(2), match.group(3)
        if url.startswith(("http://", "https://", "data:")):
            skipped += 1
            return match.group(0)
        src = resolve_image(url, base_dir)
        if src is None:
            missing.append(url)
            return match.group(0)
        data_uri = to_data_uri(src)
        converted.append((url, src.stat().st_size, src))
        return f"{prefix}{data_uri}{suffix}"

    new_text = IMG_PATTERN.sub(replace, text)
    out_path.write_text(new_text, encoding="utf-8")

    in_size = html_path.stat().st_size
    out_size = out_path.stat().st_size
    print(f"已生成自包含文件:{out_path}")
    print(f"  · 内嵌图片: {len(converted)} 张")
    for url, sz, src in converted:
        source_tag = "(skill 兜底)" if SKILL_FALLBACK_DIR in src.parents else ""
        print(f"      [OK] {url}  ({sz / 1024:.1f} KB) {source_tag}")
    if skipped:
        print(f"  · 跳过远程/已内嵌: {skipped} 处")
    if missing:
        print(f"  · 缺失(保留原引用,打开依然 404):")
        for m in missing:
            print(f"      - {m}")
    print(f"  · 文件大小: {in_size / 1024:.1f} KB → {out_size / 1024:.1f} KB")
    print(f"\n发给对方:这一个文件就够了,对方双击直接打开。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
