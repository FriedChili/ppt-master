# FORK.md — 科研/学术专用分支

本目录 `skills-academic/ppt-master/` 是从 `skills/ppt-master/`（ppt-master 6.7.0）派生的
**科研学术-only** 分支。上游：`git@github.com:hugohe3/ppt-master.git`

**原始 skill 未被修改。** 基线已提交在 git 里（见下），本分支作为对照树独立存在。

---

## 1. 怎么用

两种方式二选一。

**A. 直接替换（推荐，先备份）**

```powershell
cd E:\ppt-master-6.7.0
Rename-Item skills\ppt-master ppt-master.upstream      # 保留原版
Rename-Item skills-academic\ppt-master ppt-master
# 还原：Rename-Item skills\ppt-master ppt-master.academic; Rename-Item skills\ppt-master.upstream ppt-master
```

**B. 只作为独立 skill 目录**，让 DSH 指向 `skills-academic/ppt-master/`。

---

## 2. 回滚

```powershell
cd E:\ppt-master-6.7.0
git checkout 90e4370 -- skills/ppt-master     # 恢复原版 skill 的全部 13016 个文件
git clean -fd skills/ppt-master               # 清掉多余文件（谨慎：先加 -n 预览）
```

- 基线提交：`90e4370 baseline: ppt-master 6.7.0 as extracted (pristine, before academic slimming)`
- `skills/ppt-master` 在本分支的所有提交里始终未被触碰。
- 另有 `_pristine/skills/` 一份纯拷贝作为第二重保险（可删）。

---

## 3. 删除清单

| 目标 | 数量/体积 | 理由 |
|---|---|---|
| `templates/brands/` | 21 个企业身份（accenture/alibaba/aws/bain/bcg/deloitte/google/huawei/ibm/jpmorgan/mckinsey/microsoft/nvidia/pwc/tencent/xiaomi/中国电建/中国电信/中汽研/zcare…） | 纯企业身份，是 Stage-1 面板上最主要的场景噪音 |
| `templates/decks/` 中的企业标识 | — | **目录保留**，仅需去标识化（见 §5） |
| `templates/sounds/` | 191 文件 / 12 MB | 音效，静态学术 deck 不需要 |
| `templates/icons/simple-icons/` | 3,675 个企业 logo | 商标图形，非科研语言 |
| `references/image-palettes/` | 15 文件 | 仓库文档自己标注 "legacy compatibility material only" |
| `references/modes/showcase.md` | 1 | 发布/品牌揭示专用论证骨架 |
| `references/animations.md`、`workflows/stages/customize-animations.md` | 2 | 动画，只留静态 |
| `workflows/stages/generate-audio.md` | 1 | 配音 |
| `references/video-design.md` | 1 | 视频化交付 |
| `workflows/create-template/create-brand.md` | 1 | 品牌工作区创建；无 brand 目录后无对象 |
| `templates/charts/` 营销类 | 5：funnel / gauge / bullet / progress_bar / word_cloud | 销售漏斗、仪表盘、进度条、词云 |
| `templates/styles/` 商务方法 | 7：consulting-decision / mbb-consulting / investor-pitch / creative-pitch / product-launch / solution-proposal / operating-review | 非科研沟通方法 |

**明确保留**：`templates/decks/`（改中性名）、`references/visual-styles/`、`references/image-renderings/`、
`templates/layouts/`（含 `presentation_core` 结构化 Master/Layout 能力）、科研图表全家
（line/column/grouped_bar/stacked/scatter/bubble/histogram/box_plot/pareto/heatmap/dual_axis_line/dumbbell/butterfly/radar）、
`workflows/stages/topic-research.md`（学术选题检索）。

---

## 4. 已完成的改动

**索引 / 注册表（工具会解析，已复验）**
- `templates/styles/styles_index.json`：14 → 7
- `templates/charts/charts_index.json`：`charts` 33 → 28，`meta.total` 同步
- `scripts/register_template.py`：移除 `brand` kind 与 `brands_index.json`；CLI 现为 `--kind {style,layout,deck}`
- `scripts/confirm_ui/server.py`：移除 `'brand'` 目录映射
- `scripts/prompt_audit_manifest.json`：部分清理（见 §5 遗留）

**路由 / 文档**
- `workflows/routing.md`：删 5 行（create-brand、video-design、animations、customize-animations、generate-audio 的触发行）；4 处替换（输出契约去掉 "narrated PPTX/MP4"、Create Template 描述去掉 brand、Quick 工作区种类 Brand/Style/Layout/Deck → Style/Layout/Deck、发现列表去掉 `brands_index.json`）
- `workflows/index.md`：删 3 行（create-brand、customize-animations、generate-audio）
- `workflows/create-template.md`：子工作区分发去掉 create-brand
- `templates/README.md`：删 `brands/` 行；分发列表去掉 Create Brand
- 恢复 `workflows/create-template/create-deck.md`（deck 能力保留，否则 routing §5 会悬空）

**验证**
- `attribution_guard.py` exit 0
- 全树 Python 语法检查 0 错、JSON 解析 0 错
- `register_template.py` / `icon_sync.py` / `confirm_ui.server` 均可导入运行

---

## 5. 第二轮：交互选项面收敛（已完成）

**UI 选项宇宙**（`scripts/confirm_ui/static/catalogs.json`，这是用户在确认页真正看到的清单）

| 目录 | 之前 | 现在 |
|---|---|---|
| `modes` | pyramid / narrative / instructional / **showcase** / briefing | pyramid / narrative / instructional / briefing |
| `canvas` | ppt169 / ppt43 / **wechat** / **xiaohongshu** / **moments** / **story** / **banner** / a4 | **ppt169 / ppt43 / a4** |
| `visual_styles` | 5 组 18 个 | 未动（按你的要求保留，作为模板库丰富度） |
| `icons` / `image_usage` / `image_ai_path` / `generation_mode` / `design_spec_depth` / `delivery_purpose` | — | 未动（本身与场景无关） |

`app.js` 已确认**不引用**任何被删 id。

**社媒版式工作区**：删除 `templates/layouts/{moments_square, story_vertical, xiaohongshu_post}/`（30 个原型文件），
`layouts_index.json` 7 → 4（`editorial_bleed` / `presentation_core` / `presentation_core_43` / `report_core`）。

**文档同步**：`references/canvas-formats.md` −10 行；`scripts/docs/project.md` −4 行；
`scripts/project_management/cli.py` 移除 `xhs -> xiaohongshu` 别名提示。

**动画/音频/视频暴露面**：删除开发文档 `scripts/docs/{pptx-animations, pptx-transitions, narration, video-motion-plan}.md`；
`scripts/README.md` −4 行；`svg-pipeline.md` −4 行；`generate-pptx.md` −4 行；
`quick-generate.md` −2 行；`edit-native-pptx.md` −2 行；`apply-template-workspace.md` −1 行；
`modes/_index.md` 移除 showcase 行；`templates/README.md` 移除 Sound Library 小节。

**链接完整性**：全树 954 条链接从 **39 条悬空 → 1 条**（仅剩 `spec_lock.schema.json` 里一条正则误报）。
修复过程中有 4 处被机械切分切出残句，已逐句还原为完整文本。

---

## 6. 第三轮：decks 去标识化与重命名（已完成）

| 旧 | 新 |
|---|---|
| 目录 `templates/decks/中国电信/` | `templates/decks/signal_red/` |
| 目录 `templates/decks/中汽研/` | `templates/decks/engineering_blue/` |
| `china_telecom_brand_master` / `China Telecom Brand` | `signal_red_brand_master` / `Signal Red Brand` |
| `china_telecom_content_master` / `China Telecom Content` | `signal_red_content_master` / `Signal Red Content` |
| `catarc_dark_master` / `CATARC Dark` | `engineering_blue_dark_master` / `Engineering Blue Dark` |
| `catarc_light_master` / `CATARC Light` | `engineering_blue_light_master` / `Engineering Blue Light` |
| 元素 id 前缀 `brand-master-` | `deck-master-` |

**企业图形处理**（两张 deck 共 12 个 `<image>`，全部清除）：

| 原图形 | 处理 |
|---|---|
| 通栏 footer ribbon（中国电信 ×3 处，master 层） | 换成同几何的中性实色带，保留页脚结构 |
| 封面/结束页大标识（中汽研 ×2，592×238） | 换成同中心的居中强调线 |
| 页眉 logo（中国电信 ×2 / 中汽研 ×2，master 与 layout 层） | 直接删除（页眉横线仍在） |
| slogan 图形（×3）、城市线稿（×3） | 直接删除 |
| `top_emblem.png` | 未被任何 SVG 引用，直接删除 |

6 + 2 个图片资产全部删除，`images/` 空目录一并移除；两份 `design_spec.md` 的 `summary` / `keywords` /
§I 应用语境表 / §IV 签名元素 / §V 页表里的企业业务话术与 Logo 描述全部改写为中性学术措辞；
§VI Assets 小节删除。`decks_index.json` 重写为 `signal_red` / `engineering_blue` 两条中性摘要。

**连带修复**：`scripts/tests/test_apply_template.py`（7 处夹具引用）与 `scripts/svg_quality/cli.py`（1 处）
改为新名；全树企业身份串残留归零。

**注册表验证**：`register_template.py --rebuild-all --dry-run` exit 0，索引正确列出 2 条。

---

## 7. 尚未完成（TODO）

1. ~~**decks 去标识化**~~ —— 已在 §6 完成
2. **`simple-icons` 的散文引用**：`templates/icons/README.md`、`THIRD_PARTY_NOTICES.md`、
   `scripts/icon_sync.py`（`_SYNC_LIBRARIES`）、`scripts/svg_finalize/embed_icons.py`、`references/executor-base.md`、
   `spec_lock_reference.md`、`strategist.md`、`plan-core.md`、`design_spec_reference.md`、`quick-generate.md`
   （功能影响：`icon_sync.py` 会把已删库当可用库；不崩溃，但应清理）
3. **画布注册表仍在代码里支持被删的 5 个格式**：`scripts/config.py`、`scripts/project_utils.py`、
   `scripts/svg_position_calculator.py`、`scripts/project_management/project_specs.py`、
   `scripts/generate_examples_index.py`。这是**有意的**：它们是跨切面注册表，从代码里摘除风险高且不影响暴露面；
   `--format xiaohongshu` 仍可用，但 UI 不再提供。
4. **`templates/styles/README.md`** 是否枚举了已删的 7 个方法
5. `scripts/docs/confirm_ui.md`（catalog 文件清单）、`scripts/docs/template-tools.md`（index 清单）
6. `prompt_audit_manifest.json` 残留字符串（`create-brand`×2、`create-deck`×2、`video-design`×5、
   `templates/brands`×4、`generate-audio`×4、`customize-animations`×3、`templates/sounds`×2、`animations.md`×1）
   —— 只服务 `prompt_audit.py` 开发期校验，不影响生成；建议按瘦身后的树重新生成而非逐条修补
7. `register_template.py` 帮助文本仍写 "brand / style / layout / deck"；`_BRAND_REQUIRED_SECTIONS` 成死代码
8. **端到端验收**：用本分支完整跑一次生成（默认路线 + 导出），确认无回退

---

## 6. 设计边界（有意保留）

- **`brand-only` / `flat` 等结构术语保留**。它们是 `pptx_structure.mode` 的结构概念
  （无模板身份 → 扁平结构），被 `pptx-structure-interface.md`、`semantic-svg.md`、`executor-base.md` 广泛引用。
  删除会波及结构契约本身，且它们不出现在用户的交互选项里。
- **转换器代码保留**：`pptx_animations.py`、`pptx_transitions.py`、`animation_config.py` 等仍留在
  `scripts/svg_to_pptx/`。删掉会直接破坏导出链。本轮只移除**暴露面**（文档、路由、阶段、CLI 选项），
  导出默认输出静态 deck。
- **`templates/layouts/` 全保留**：这是原生 PPTX 的 Master/Layout/占位符能力，不是商务场景。
