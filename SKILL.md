---
name: lecture-html
description: 乘势 AI 商业实战课·讲师团内部专用 — 生成中式黑金风格(深黑底 + 古金装饰)的 HTML 全屏讲课 slide。当讲师要做新一节课的讲课 HTML / 把讲稿做成幻灯片 / 制作章节封面页时触发。产出是自包含单文件 HTML(背景 + logo 已内嵌),可发学员、可发布、可全屏开讲。底部品牌条统一是「乘势金 logo + 乘势 AI 商业实战课」,所有产出共享同一套视觉。
---

# lecture-html · 乘势讲师团专用讲课 HTML

> **这不是开源通用 skill** —— 这是「乘势 AI 商业实战课」讲师团的内部工具。所有产出默认带乘势品牌(金 logo + 「乘势 AI 商业实战课」 + 「虽有智慧 · 不如乘势」收尾)。**不要**生成"通用模板",不要让用户填"你的品牌"—— 默认就是乘势。

把「一份讲稿要点」变成「一份能演示、能分享、能发布的 HTML 幻灯片」。

> **标准范本**:`C:/Users/Z/Desktop/乘势AI商业实战课_物料包/3-第一节课/*_讲课版.html` 这 8 份课件就是基准,所有规则都从这里提炼。最新基准:`2.5_用上海外大模型_讲课版.html`。**写之前打开它对照**。

## 何时使用这个 skill

触发场景(讲师常说的话):

- "帮我把这节课做成讲课 HTML"
- "把这份讲稿做成幻灯片"
- "X.X 这一节做个课件"
- "帮我做章节封面 / 开课导言"
- "把这份讲稿改成乘势风格"

## 视觉规则(锁定数值 · 不要改)

色板:

| 变量 | 值 | 用途 |
|:---|:---|:---|
| `--bg-0` | `#060410` | 底色(近黑 · 偏紫蓝) |
| `--paper` | `#ebe5d5` | 主文字(米白) |
| `--cream` | `#d6cdb3` | 辅助文字 |
| `--gold-d` | `#8a6a32` | 古金 · 深 |
| `--gold` | `#c8a35c` | 古金 · 标准 |
| `--gold-l` | `#e8d4a0` | 古金 · 浅 |
| `--gold-3` | `#f3d678` | 高亮金(用于 `.em` / 加重) |
| `--red` | `#d84a3a` | 红色强调(用于 `.red` / 警告) |
| `--muted` | `#8a8070` | 弱化文字 |

字体(Google Fonts CDN 加载):

- **Serif**(标题/正文):`Noto Serif SC` 思源宋体
- **Sans**(辅助/UI):`Noto Sans SC`
- **Num**(数字/英文):`Cinzel`

核心字号(`clamp(min, viewport, max)` · 全部锁死,**不要改**):

| 元素 | clamp 值 | 用途 |
|:---|:---|:---|
| `.cover-title` | `(2.4rem, 5.6vw, 4.8rem)` | 封面大标题 |
| `.cover-eyebrow` | `(0.95rem, 1.4vw, 1.2rem)` | 封面眉头(章节号) |
| `.cover-motto` | `(1.2rem, 2.2vw, 1.7rem)` | 封面下方一句话 |
| `h1.title` | `(2.4rem, 5.5vw, 5rem)` | 正文章节标题 |
| `h2.subtitle` | `(1.4rem, 2.6vw, 2.4rem)` | 副标题 |
| `.quote-big` | `(2rem, 4.5vw, 4rem)` | 金句大 |
| `.quote-mid` | `(1.5rem, 3vw, 2.8rem)` | 金句中 |
| `.list-big` | `(1.3rem, 2.3vw, 1.9rem)` | 列表 |
| `.bignum` | `(5rem, 16vw, 14rem)` | 大数字 |

> 例外:**整门课总开篇**(第 0.0 节)可以把 cover-title 调到 `clamp(3rem, 8vw, 7rem)`,更震撼。其他章节保持 4.8rem。

背景:`images/bg-stage.jpg`(横屏)+ `images/bg-tile.jpg`(竖屏自动平铺),`body::before` 全屏铺。

切换动画:`.slide.active>*` 用 fadeUp,子元素 nth-child(1..6) 错开 0.12s,营造逐条出现的呼吸感(已经写在 template 里,**不要删**)。

## 资源文件

| 文件 | 用途 |
|:---|:---|
| `template.html` | 空白可填模板 — 完整覆盖乘势在用的所有 slide 类型 |
| `examples/design-formula.html` | 早期设计公式范例(参考用) |
| `images/bg-stage.jpg` | 横屏背景(乘势 v2 版本) |
| `images/bg-tile.jpg` | 平铺背景(乘势 v2 版本) |
| `images/bg-cover.jpg` | 封面背景(留白克制版) |
| `images/logo.png` | 圆徽 logo(乘势 logo-only,可换) |
| `scripts/generate_images.py` | 用 gpt-image-2 跑自己的背景/logo |
| `scripts/pack.py` / `inline.py` | 分发 — 打 zip 或内嵌成单文件(详见 README) |

## Slide 类型(13 种 · 乘势真实在用)

| 类型 | 何时用 | CSS class |
|:---|:---|:---|
| **封面 cover** | 开场 / 结尾 / 章节封面 | `.slide-cover` + `.cover-title` |
| **章节标题 title** | 章节定位 | `h1.title` + `h2.subtitle` |
| **金句 quote** | 一句话戳到点 | `.quote-big` / `.quote-mid` |
| **大数字 bignum** | 让数据说话 | `.bignum`(用得不多) |
| **列表 list** | 3-5 个并列要点 | `.list-big` |
| **详情卡 spec** | 三段式 key-val 说明(问题/怎么办/怎么记) | `.spec-card + .spec-row` |
| **对比卡 cmp** | A vs B(推荐/不推荐 · 值得/没必要) | `.cmp-grid + .cmp-card.good/.bad` |
| **流程链 fly-row** | 三关 / 三步 一字排开 | `.fly-row + .node + .arr` |
| **人设/方案卡 adv-hero** | 介绍一个角色/方案/路径 | `.adv-hero` |
| **风险提示 warn** | 必须提醒的坑 | `.warn-box` |
| **步骤卡 step** | 一步详细教学 | `.step-card` |
| **比喻卡 meta** | 把抽象概念类比成日常物 | `.meta-card` |
| **路径表 pick-table** | 多方案多维度对照 | `.pick-table` |

所有类型在 `template.html` 里都有占位 slide,改字即可。

## 怎么用(给 Claude 的步骤)

### 步骤 1:了解用户的讲课内容

问清楚:
- **课程名 + 章节号**(用于封面眉头 `第 X 章 · 第 Y 节`)
- **本节要解决的核心问题**(用一句话回答)
- **每页的论点**(一页一个)
- **听众是谁**(影响金句语气和案例深度)

### 步骤 2:为每个论点选 slide 类型

参考上面 13 种类型表。**节奏建议**(乘势真实节奏):

```
封面 → 章节定位 → 引入痛点(quote-big) →
[内容主体:list / cmp-grid / spec-card / adv-hero / fly-row 交替] →
风险提示(warn-box,如有) → 金句收束(quote-big) → 尾页
```

一节课大约 **15-22 页**,**不要少于 10 页**(乘势 1.2 是 22 页,2.5 是 22 页)。

### 步骤 3:复制 template.html,挨个填 slide

把 skill 目录的 `template.html` 复制到用户工作目录下,命名为 `<章节号>_<主题>_讲课版.html`(乘势命名规则,如 `2.5_用上海外大模型_讲课版.html`)。

#### 步骤 3.5:底部品牌条 — 不要改

模板末尾的 `opening-brand` div 已经预设好:

```html
<div class="opening-brand">
  <img src="images/logo.png" alt="乘势 logo">
  <span class="brand-text">乘势 AI 商业实战课</span>
</div>
```

**不要改**。logo 和文字都是乘势品牌锁定的。**也不要删** —— 所有乘势课件底部都必须有这一条,这是品牌一致性。

唯一例外:如果讲师明确说"这不是乘势的课"(罕见 · 八成是误用),才提示他换 logo 和 brand-text。

### 步骤 4:自动内嵌图片,产出自包含单文件(强制 · 默认交付方式)

填完字后,立刻跑:

```bash
python <skill 目录>/scripts/inline.py <topic>.html
```

会产出 `<topic>.inline.html` — 把 skill 自带的背景图 + logo 全部以 base64 内嵌进去,**用户双击就能看到完整效果,不需要 images/ 文件夹**。

然后把 `<topic>.inline.html` 重命名成最终交付名,把中间的 `<topic>.html` 删掉(或留作"源文件")。

### 步骤 5:浏览器打开 → F 全屏 → 开讲

### 步骤 6(可选):如果需要自定义背景/logo

调用 `scripts/generate_images.py`,详见 README。

---

## 乘势内容编写规则(核心 · 写文案时严格遵守)

### 1. 全角空格做字间距(封面/章节标题)

封面眉头和封面大标题用**全角空格**(`U+3000`)拉开字距,让标题有"庙堂感":

```
✓ 第 二 章 · 第 五 节
✓ 大 模 型 的 能 力 边 界
✗ 第二章·第五节
✗ 大模型的能力边界
```

正文 `h1.title` **不用**全角空格,正常写。

### 2. 中点 · 用于停顿和分隔

中文标点用 `·`(中文中点 U+00B7)做"停顿"和"分隔",**不要用顿号/逗号**:

```
✓ 卡点 · 原理 · 两条路径
✓ 知道有 · 还得真的用得上
✓ 第 二 章 · 第 五 节 · 完
```

### 3. 加重三色规则

`.em`(金色 `--gold-3`) > `.red`(红色) > 普通文字(米白)

- **`.em` 用于关键词加重**:80% 的加重用这个,标记"这句话的核心"
- **`.red` 仅用于警告/反例/痛点**:不要滥用,一页最多 2-3 处
- 加重比例:**一句话最多 2 个加重,一页所有加重总数 ≤ 5**

```html
✓ ChatGPT、Claude、Gemini · <span class="em">在国内默认打不开</span> —— 这是第一道坎
✓ "我知道有 <span class="em">ChatGPT</span>,可是 —— <span class="red">我根本打不开它</span>"
```

### 4. 引入页 = 痛点引语

第三页通常是「引入痛点」,固定句式 — **学员的原话+情绪**,放进 `quote-big`:

```html
<div class="label">很多人 · <span style="color:var(--gold-3)">卡在这一步</span></div>
<div class="quote-big" style="line-height:1.5">
  "我知道有 <span class="em">XXX</span><br>
  可是 ——<br>
  <span class="red">我就是用不起来</span>"
</div>
<div class="caption">这一节 · 就把这层窗户纸<span style="color:var(--gold-3);font-weight:700">捅破</span></div>
```

### 5. 章节眉头格式

正文章节标题页的眉头固定格式:

```html
<div class="eyebrow"><span class="num">2.5</span>第二章 · 第五节</div>
```

- num 用阿拉伯数字 + 小数点(`2.5`),Cinzel 字体显示
- 文字部分用中文「第 N 章 · 第 N 节」

封面眉头格式不同(用全角中文数字):

```html
<div class="cover-eyebrow">第 二 章 · 第 五 节</div>
```

### 6. 收尾固定句:「虽有智慧 · 不如乘势」(强制 · 锁定)

每节最后一页的 `cover-motto` **必须**用这句(出自《孟子·公孙丑上》)—— 这是乘势的品牌锚定,**不要换成本节金句、不要改字、不要去掉**:

```html
<section class="slide slide-cover">
  <div class="cover-eyebrow">第 二 章 · 第 五 节 · 完</div>
  <h1 class="cover-title">本节主题 · <span class="gold">不再遥远</span></h1>
  <div class="cover-motto" style="margin-top:5vh">虽有智慧 · 不如乘势</div>
</section>
```

### 7. 收尾标题格式:「主题 · 不再 X」

尾页的 `cover-title` 用对仗结构,如:

- `海外模型 · 不再遥远`
- `大模型 · 不再玄`
- `AI · 不再让你卡住`

骨架是「主语 · 不再 + 一个动词/形容词」。

### 8. 不用 emoji,用几何字符

- ✗ 🔴 ⚠️ 💡 ✅ ❌
- ✓ ① ② ③ ★ ◆ ◇ ⚠ →

`⚠` 唯一允许的"半 emoji"字符(在 `.warn-box .wb-tag` 里用)。

### 9. 标题不超过 2 行

`cover-title` 最多 2 行,超过就分两个 slide。乘势所有标题都遵守这条。

### 10. 一页一核心

每页只讲一件事。判断方法:**这页删了,我下一页接得上吗?接不上就拆**。

### 11. 副标用 `<br><span style="font-size:0.5em">` 嵌在标题里

需要副标时不要单独开 `h2`,而是嵌在标题里:

```html
<h1 class="cover-title">
  如何 · <span class="gold">用上海外大模型</span>
  <br>
  <span style="font-size:0.5em;color:var(--cream);font-weight:500;letter-spacing:0.08em">卡点 · 原理 · 两条路径</span>
</h1>
```

### 12. 文件命名

`<章节号>_<主题>_讲课版.html`,如:

- `0.0_开课导言_讲课版.html`(开篇用 0.0)
- `1.1_一句话讲清大模型_讲课版.html`
- `2.5_用上海外大模型_讲课版.html`

主题用 5-8 个汉字概括,**不要用空格**,**保留下划线作分隔**。

### 13. title 标签格式

```html
<title>2.5 如何用上海外大模型 · 卡点 · 原理 · 两条路径 | 乘势 AI 商业实战课</title>
```

格式:`<章节号> <主题> · <三个副标关键词> | <课程名>`。

---

## 反例(常犯的错)

- ✗ 用 PowerPoint 风格的"一页 10 条要点 + 5 张配图"(乘势是"一页一句"风格)
- ✗ 用 emoji 做图标(除了 `⚠`)
- ✗ 封面标题不用全角空格(失去"庙堂感")
- ✗ 加重满天飞 — 一页 10 处 `.em`(加重失去意义)
- ✗ 尾页用普通"谢谢观看"(必须用「虽有智慧 · 不如乘势」)
- ✗ 改底部 brand-text 或 logo(锁定的,不要动)
- ✗ 写"你的课程名 · 你的品牌"这种通用占位(这是乘势内部工具,默认就是乘势)
- ✗ 标题超过 2 行(拆页)
- ✗ 一页塞 3 个论点(应该拆 3 页)
- ✗ 修改 CSS 变量数值或字号 clamp 值(锁定的,不要动)

## 进一步

完整范例见:`C:/Users/Z/Desktop/乘势AI商业实战课_物料包/3-第一节课/2.5_用上海外大模型_讲课版.html`(最新基准 · 22 页 · 涵盖所有 13 种 slide 类型)。
