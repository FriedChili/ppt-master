---
deck_id: signal_red
kind: deck
category: brand
summary: 克制的红灰 16:9 通用 deck 骨架：封面、目录、章节、开放内容、结束语；浅色内容 Master 配深色封面/章节/结束 Master，适合报告、评审与答辩。
label_zh: 信号红
summary_zh: 白底配红黑两色：红色顶栏底栏加左侧红竖条，清爽又有力度。适合报告、评审、答辩，以及需要一点警示感的内容。
keywords: [signal-red, report, review, defense, general-purpose]
primary_color: "#C00000"
canvas_format: ppt169
canvas_width: 1280
canvas_height: 720
canvas_viewbox: "0 0 1280 720"
source_canvas_width: 1280
source_canvas_height: 720
source_viewbox: "0 0 1280 720"
replication_mode: fidelity
native_structure_mode: structured
page_count: 5
---

# signal_red — Design Specification

## I. Template Overview

| Application context | Definition |
| --- | --- |
| Recurring presentation family | 研究报告、方法说明、结果评审与阶段性汇报 |
| Intended audiences and outcomes | 面向评审者、导师、同行与项目干系人；帮助受众理解背景与结论、形成判断，并明确下一步 |
| Delivery and reading assumptions | 以现场讲解为主，同时需要会后独立阅读与复核；页面应保留关键结论与必要证据，不依赖口头说明才能辨认主题 |
| Representative narrative/page roles | 当前原型覆盖封面、目录、章节、开放内容和结束语；具体选页、重复、顺序与内容处理由当前项目的 Strategist 根据材料决定 |

- 视觉基调为白底、红色结构条与银灰内容承载区，强调权威、清晰和克制。
- 结构上分为两个可复用 Master 家族：Signal Red Brand 服务封面、章节与收尾，Signal Red Content 服务目录与正文；它们按视觉体系分工，不是按单个 Layout 拆分出的重复 Master。

## II. Color Scheme

| Role | Color | Application |
| --- | --- | --- |
| Telecom red | #C00000 | 页眉胶囊、编号、分隔线和关键强调 |
| Silver gray | #D9D9D9 | 页眉结构带 |
| Panel gray | #F8FAFC | 内容承载区与品牌卡片 |
| Graphite | #111827 | 标题和关键文字 |
| Muted gray | #6B7280 | 辅助说明与页脚 |
| White | #FFFFFF | Master 背景与反白文字 |

## III. Typography

| Role | Font stack | Application |
| --- | --- | --- |
| Chinese title and body | `"Microsoft YaHei", "PingFang SC", Arial, sans-serif` | 标题、正文、目录项与中文品牌说明 |
| Latin label and folio | `Arial, "Microsoft YaHei", sans-serif` | 英文标识、日期与页码 |

字体栈仅使用常见系统字体；Windows 优先微软雅黑，macOS 可回退苹方，不依赖额外字体安装。

## IV. Signature Design Elements

- 内容页和目录页使用“红色胶囊 + 银灰长带”的页眉结构，右侧保留横向品牌图形。
- 封面、章节页和结束页复用红色口号、城市线稿与底部红色飘带，但控制在独立品牌卡片中。
- Signal Red Brand Master 统一承载白底、顶部红线、底部品牌飘带与英文标识；Signal Red Content Master 统一承载红灰页眉、横向品牌标识和页脚分隔线。
- 内容承载区采用浅灰圆角面板；实际内容由边界完整的 `object` slot（PowerPoint 内容占位区域）承载，不显示提示性虚线。
- 标题与通用内容保持左对齐；只在品牌图形内部使用居中构图。

## V. Page Roster

| File | Master | Layout key | PowerPoint picker name | Visual character | Reusable slots |
| --- | --- | --- | --- | --- | --- |
| `01_cover.svg` | Signal Red Brand | cover | Cover | 左侧标题簇、右侧品牌卡片、底部飘带 | 标题、副标题、单位、日期 |
| `02_toc.svg` | Signal Red Content | agenda | Agenda | 左侧品牌说明卡、右侧四行编号目录 | 页面标题、四个目录项、页码 |
| `03_chapter.svg` | Signal Red Brand | section | Section Header | 左侧章节信息、右侧品牌卡片、底部飘带 | 章节号、章节标题、章节副标题 |
| `04_content.svg` | Signal Red Content | content | Title and Content | 红灰页眉与大面积浅灰开放内容区 | 栏目标、页面标题、内容对象、来源、页码 |
| `05_ending.svg` | Signal Red Brand | closing | Closing | 左侧结束语、右侧品牌卡片、底部飘带 | 结束标题、副标题、联系信息、页码 |

