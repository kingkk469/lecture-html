"""
打包脚本 — 把 HTML + 它引用的 images/ 文件夹一起打成 zip,方便发给别人。

用法:
    python scripts/pack.py <html-file> [output.zip]

例:
    python scripts/pack.py my-lecture.html
    # → 产出 my-lecture.zip,里面有 my-lecture.html + images/(只含被引用的图)
"""

import os
import re
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


IMG_PATTERN = re.compile(
    r"""(?:url\(\s*['"]?|src\s*=\s*['"])([^'")]+\.(?:jpg|jpeg|png|gif|webp|svg))""",
    re.IGNORECASE,
)


def find_referenced_images(html_path: Path) -> list[str]:
    text = html_path.read_text(encoding="utf-8")
    paths = IMG_PATTERN.findall(text)
    seen, result = set(), []
    for p in paths:
        if p.startswith(("http://", "https://", "data:")):
            continue
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    html_path = Path(sys.argv[1]).resolve()
    if not html_path.is_file():
        print(f"找不到文件:{html_path}")
        return 1

    base_dir = html_path.parent
    out_zip = Path(sys.argv[2]).resolve() if len(sys.argv) >= 3 else html_path.with_suffix(".zip")

    images = find_referenced_images(html_path)
    if not images:
        print("提示:HTML 里没找到本地图片引用,只打包 HTML 本身。")

    missing = []
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(html_path, arcname=html_path.name)
        for rel in images:
            src = (base_dir / rel).resolve()
            if not src.is_file():
                missing.append(rel)
                continue
            zf.write(src, arcname=rel)

    print(f"已打包:{out_zip}")
    print(f"  · HTML: {html_path.name}")
    print(f"  · 图片: {len(images) - len(missing)}/{len(images)} 张")
    if missing:
        print("  · 缺失(对方解压后这些图依然会 404):")
        for m in missing:
            print(f"      - {m}")
    print(f"\n发给对方:让对方解压后双击 {html_path.name} 即可。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
