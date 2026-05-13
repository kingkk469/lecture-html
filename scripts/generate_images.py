"""生成讲课 HTML 用的图片素材(背景 + logo)

需要通过环境变量传入:
  OPENAI_API_KEY    — 你的 API key
  OPENAI_API_BASE   — (可选) API 端点,默认 https://api.openai.com
                      用中转 API 时改成对应域名,例如 https://api.xxx.com
  OPENAI_MODEL      — (可选) 模型名,默认 gpt-image-1
                      不同中转服务的模型名可能不同(gpt-image-2 / dall-e-3 等)
"""
import os, sys, json, base64, time
import urllib.request, urllib.error

API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com")
API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
MODEL = os.environ.get("OPENAI_MODEL", "gpt-image-1")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

if not API_KEY:
    print("ERROR: 请先设置 OPENAI_API_KEY 环境变量")
    print('  Windows PowerShell: $env:OPENAI_API_KEY = "sk-..."')
    print('  macOS/Linux:        export OPENAI_API_KEY="sk-..."')
    sys.exit(1)

os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# 修改 TASKS 列表 → 生成你自己的背景/logo
# 已有同名文件会跳过,删掉旧文件即可重新生成
# ============================================================
TASKS = [
    {
        "name": "bg-stage.jpg",
        "size": "1536x1024",   # 横屏 3:2
        "quality": "high",
        "output_format": "jpeg",
        "background": "opaque",
        "prompt": (
            "Horizontal 3:2 landscape presentation slide background, "
            "near-pure-black obsidian base (#020208 to #060810), profoundly dark and luxurious, "
            "chinese traditional decorative meets digital tech aesthetic, "
            "refined antique gold line-art Chinese auspicious cloud patterns at the LEFT vertical edge, "
            "delicate antique gold water wave patterns at the BOTTOM LEFT corner, "
            "fine antique gold printed-circuit-board traces with tiny hexagonal nodes on the LEFT side, "
            "a graceful sweeping arc of muted golden light ribbon from the UPPER RIGHT corner with shimmering particle trail, "
            "faint constellation-style golden dot-and-line connections in the RIGHT side and lower right, "
            "sparse refined floating gold particle dust throughout, "
            "a small vermilion red square seal stamp accent in the LOWER LEFT corner, "
            "CENTER 60 percent kept VERY DEEP DARK clean and empty for white text overlay, "
            "absolutely NO Chinese characters, NO calligraphy, NO main subject, NO text, "
            "all decorations only at the edges, high-end luxury obsidian-black-gold poster, "
            "4K ultra detailed, horizontal landscape"
        )
    },
    {
        "name": "bg-tile.jpg",
        "size": "1024x1024",
        "quality": "high",
        "output_format": "jpeg",
        "background": "opaque",
        "prompt": (
            "Seamless tileable Chinese luxury wallpaper texture, perfectly repeating without visible seams, "
            "near-pure-black obsidian base (#020208 to #060810), "
            "sparse refined antique gold line-art Chinese auspicious cloud and water wave patterns evenly distributed, "
            "fine antique gold printed-circuit-board traces with tiny hexagonal nodes sparsely interwoven, "
            "sparse delicate gold particle dust and tiny star-like glints throughout, "
            "extremely subtle, low contrast, dark atmospheric, uniform distribution without focal point, "
            "MUST tile seamlessly when repeated horizontally and vertically, "
            "absolutely NO Chinese characters, NO text, NO bright spots, NO dominant elements, "
            "high-end obsidian-black-gold luxury wallpaper, 4K"
        )
    },
    {
        "name": "bg-cover.jpg",
        "size": "1536x1024",
        "quality": "high",
        "output_format": "jpeg",
        "background": "opaque",
        "prompt": (
            "Horizontal 3:2 landscape COURSE COVER background, ultra minimalist and high-end, "
            "near-pure-black obsidian base (#020208 to #060810), profoundly dark, "
            "extremely restrained Chinese decorative elements only at edges (at least 75 percent canvas is pure dark empty space), "
            "subtle antique gold cloud patterns at FAR LEFT edge fading away, fine circuit traces on left, "
            "delicate water waves at BOTTOM LEFT corner, "
            "a single muted golden arc at UPPER RIGHT corner, "
            "sparse constellation dots at FAR RIGHT, small vermilion red seal in lower left, "
            "absolutely NO TEXT, NO CALLIGRAPHY, NO subject, museum-gallery quality, "
            "4K, horizontal landscape"
        )
    },
    {
        "name": "logo.jpg",
        "size": "1024x1024",
        "quality": "high",
        "output_format": "jpeg",
        "background": "opaque",
        "prompt": (
            "Square 1:1 logo on solid pure pitch black background, "
            "TOP CENTER OCCUPYING UPPER 70 PERCENT: elegant circular medallion - thin antique gold (#d4a955) ring with slight weathering, "
            "inside the ring against pure black: two Chinese characters '乘 势' (CHANGE TO YOUR OWN CHARACTERS) "
            "in BOLD POWERFUL SEMI-CURSIVE CALLIGRAPHY (xingshu/行书 style with strong masculine brush strokes), "
            "antique gold color with hot-stamped foil texture, both clearly readable, "
            "several tiny golden constellation dot-and-line accents along the outer ring like a star map, "
            "BELOW THE MEDALLION: small horizontal line of text 'YOUR COURSE NAME' in thin golden Chinese serif font, "
            "slight weathering on ring edges, solid pure pitch black background, "
            "chinese classical imperial aesthetic meets modern brand mark, premium gallery quality, "
            "4K ultra detailed, perfect square 1:1"
        )
    },
]

def call_api(task):
    url = f"{API_BASE}/v1/images/generations"
    body = {"model": MODEL, "prompt": task["prompt"], "n": 1, "size": task["size"], "quality": task["quality"]}
    if task.get("output_format"): body["output_format"] = task["output_format"]
    if task.get("background"): body["background"] = task["background"]
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        return json.loads(resp.read())

for task in TASKS:
    out_path = os.path.join(OUT_DIR, task["name"])
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
        print(f"\n=== {task['name']} SKIP (already exists, {os.path.getsize(out_path)//1024} KB) ===")
        continue

    print(f"\n=== {task['name']} ({task['size']} {task['quality']}) ===")
    t0 = time.time()
    data = None
    for attempt in range(3):
        try:
            data = call_api(task)
            break
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"  attempt {attempt+1} HTTP {e.code}: {err_body[:300]}")
            if attempt < 2: time.sleep(5)
        except Exception as e:
            print(f"  attempt {attempt+1} ERROR: {type(e).__name__}: {e}")
            if attempt < 2: time.sleep(5)
    if data is None:
        print(f"  FAIL after 3 retries")
        continue

    item = data.get("data", [{}])[0]
    if "b64_json" in item and item["b64_json"]:
        img_bytes = base64.b64decode(item["b64_json"])
    elif "url" in item and item["url"]:
        with urllib.request.urlopen(item["url"], timeout=60) as r:
            img_bytes = r.read()
    else:
        print(f"  ERROR: unrecognized response, keys={list(item.keys())}")
        continue

    with open(out_path, "wb") as f:
        f.write(img_bytes)
    kb = os.path.getsize(out_path) // 1024
    print(f"  OK -> {out_path} ({kb} KB, {time.time() - t0:.1f}s)")

print("\nDone.")
