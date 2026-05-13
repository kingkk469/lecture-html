# lecture-html · 讲课 HTML 设计公式

> 把「讲稿要点」变成「能演示、能分享、能发布的 HTML 幻灯片」。
> 设计风格:中式古典 × 科技未来 · 深黑底 + 古金装饰 · 适合中文 AI / 商业 / 创业课程。

## 这是什么

一个 **Claude Code Skill**(也能直接当做 HTML 模板用),帮你 10 分钟做出有质感的讲课幻灯片。

**特点:**

- 🎯 一页一个核心要点 · 大字号 · 后排能看清
- 🌑 近黑底 + 古金装饰 · 投影不刺眼
- 📱 响应式 · 电脑/平板/手机都能演示
- 📦 单文件 HTML · 可发链接 / 上传 GitHub Pages / 发文件给学员
- ⌨️ 键盘控制 · `← →` 翻页 / `F` 全屏 / `Home` 回首页
- 🎨 8 种 slide 类型覆盖 95% 场景

## 快速开始

### 方式一:作为 Claude Code Skill 使用(推荐)

把这个 repo clone 到 `~/.claude/skills/` 下:

```bash
cd ~/.claude/skills
git clone https://github.com/<your-username>/lecture-html.git
```

然后在 Claude Code 里,直接说:

> "帮我做一份关于 XXX 的讲课 HTML"

Claude 会自动识别并使用这套设计公式。

### 方式二:直接复制模板用

不用 Claude 也行 — 这是个普通 HTML 模板。

1. 下载这个 repo 的 zip 或 git clone
2. 复制 `template.html` 到你的项目
3. 复制 `images/` 文件夹(背景 + logo 素材)
4. 编辑 `template.html`,改字改内容
5. 浏览器打开 → 按 `F` 全屏 → 开讲

## 文件结构

```
lecture-html/
├── SKILL.md                    # Claude Code 识别用(写明何时触发)
├── README.md                   # 你正在看的文件
├── template.html               # 空白模板 · 复制改字即可
├── examples/
│   └── design-formula.html     # 完整范例 · 这套公式的演示页(本身就用了这套公式做)
├── images/
│   ├── bg-stage.jpg            # 横屏背景
│   ├── bg-tile.jpg             # 手机平铺背景
│   ├── bg-cover.jpg            # 封面背景(克制留白)
│   └── logo.png                # 圆徽 logo(透明 PNG)
├── scripts/
│   └── generate_images.py      # 一键跑你自己的背景/logo
└── LICENSE                     # MIT
```

## 8 种 Slide 类型

| 类型 | 何时用 | 关键 class |
|:---|:---|:---|
| **封面 cover** | 开场 / 结尾 | `.slide-cover` |
| **章节标题 title** | 分章节 | `h1.title` |
| **大数字 bignum** | 让数据说话 | `.bignum` |
| **时间轴 timeline** | 变化前后 | `.timeline` |
| **对比 vs** | A vs B | `.vs` |
| **列表 list** | 3-5 个要点 | `.list-big` |
| **卡片 card** | 2-3 栏对比 | `.three-col` |
| **金句 quote** | 一句话戳点 | `.quote-big` |

每种类型在 `template.html` 里都有现成示例,复制改字即可。

## 设计原则

1. **一页一个核心** — 不堆信息,比 PPT 信息密度低 30%
2. **大字号高对比** — 标题至少 `clamp(2.4rem, 5.5vw, 5rem)`
3. **克制装饰** — 所有装饰只在角落,中心大段留黑
4. **不用 emoji** — 用几何字符代替(★ ① ② ③ ◆)
5. **全局品牌条** — 底部居中 logo + 课程名,所有 slide 共享

## 视觉系统

### 配色

```css
--bg-0:    #020208   /* 近黑底 */
--gold:    #c8a35c   /* 古金 */
--gold-3:  #f3d678   /* 亮金强调 */
--red:     #d84a3a   /* 红色强调 */
--paper:   #ebe5d5   /* 米白文字 */
```

### 字体

- **Serif** (标题正文): Noto Serif SC 思源宋体
- **Sans** (辅助): Noto Sans SC 思源黑体
- **Num** (数字英文): Cinzel

字体通过 Google Fonts CDN 加载,无需本地安装。

### 间距

- `.slide { padding: 6vh 8vw; }`
- 标题 `margin-bottom: 2vh`
- 行高 `1.6 ~ 2.0`

## 自己生成背景图 / Logo

如果默认素材不符合你的主题:

```bash
# 1. 设置 OpenAI API key (or 中转 API)
export OPENAI_API_KEY="sk-..."

# 2. 编辑 scripts/generate_images.py 里的 TASKS,改 prompt

# 3. 跑脚本生成
python scripts/generate_images.py
```

**生成 prompt 公式:**

```
[尺寸]   Square 1:1 / Horizontal 3:2 / Vertical 2:3
[基底]   near-black obsidian #020208 / pure black background
[主体]   what you want as focal point (or "no center subject")
[装饰]   chinese cloud / circuit / arc / constellation / seal at edges
[留白]   center 60% kept dark and empty for text overlay
[禁止]   NO text, NO people, NO faces, NO logos
[质感]   premium luxurious, museum-quality, 4K ultra detailed
```

## 翻页控制

| 按键 | 动作 |
|:---|:---|
| `→` / `空格` / `Enter` / `PageDown` | 下一页 |
| `←` / `Backspace` / `PageUp` | 上一页 |
| `Home` / `End` | 第一页 / 最后一页 |
| `F` | 全屏 / 退出全屏 |
| 屏幕右侧点击 | 下一页 |
| 屏幕左侧 1/4 点击 | 上一页 |
| 触摸屏左右滑动 | 翻页 |

## 浏览器兼容

- ✓ Chrome / Edge / Firefox / Safari(桌面 + 移动)
- ✓ 离线可用(只依赖 Google Fonts CDN 外字体)
- ✓ 投影 / 直播 / 录屏

## 部署到 GitHub Pages

```bash
# 1. fork 这个 repo
# 2. settings → Pages → main branch → /
# 3. 改 template.html 内容
# 4. push,等几分钟,访问 https://<username>.github.io/lecture-html/template.html
```

## License

MIT — 自由使用、改造、商用。**如果做得好,@ 一下原作者就行 😊**

## 致谢

- 设计原型来自《乘势 AI 商业实战课》— 数字生命 KING
- 背景图 / Logo 用 gpt-image-2 生成
- 字体来自 Google Fonts (Noto Serif SC + Cinzel)

---

> 改了发我看 — issues / discussions / @ 都可以。
