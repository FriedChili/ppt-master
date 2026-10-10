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

## 7. 验收证据

### 7.1 `prompt_audit` — **exit 0**

`prompt_audit.py` 的路径约定是 `<root>/skills/ppt-master/...`，所以需要造一个安装后布局的根。
用 `_audit-staging/`（**真实拷贝，不能用 junction** —— junction 会被 `resolve()` 穿透，破坏相对路径计算）。

```powershell
python skills/ppt-master/scripts/prompt_audit.py --root <staging> --skip-near-duplicates
# exit 0，仅剩 1 条 advisory 警告 DUPLICATE_EXACT_CANDIDATES（3 组跨文件重复段落）
```

为达成全绿做的**真实修复**（不是屏蔽检查）：
- `modes/_index.md` 计数 5 → 4，移除 showcase 对比行
- `templates/charts/chart-vocabulary.md` 移除已删的 5 个营销图表（投影与注册表漂移）
- 清单内 `file_budgets` / `registries` / `authority_edges` / `coverage` / `duplicates`
  中指向不存在文件的条目，按实树存在性清除
- `load_sets` 中匹配 0 文件的选择器（**任意嵌套深度**）清除；`select` **仅在超出可用数时下调**
  （`select` 是"选择数量"，上限为可用文件数，不是"必须等于总数"）

> **`tiktoken` 依赖缺口（上游问题，与本分支无关）**：`prompt_audit.py` 需要 `tiktoken>=0.7.0`，
> 但它**不在** `requirements.txt` 里。未修改的原树跑同一条命令报**完全相同**的错误。
> 已 `pip install 'tiktoken>=0.7.0'`。

### 7.2 测试套件

`scripts/tests/` 共 55 个测试文件。与本分支改动直接相关的定向组：

```powershell
python -m unittest tests.test_apply_template tests.test_template_flow_batch1 `
  tests.test_template_flow_batch4 tests.test_dogfood_template_route_fixes `
  tests.test_dogfood_template_material_fixes tests.test_spec_lock_forbidden `
  tests.test_embed_icons tests.test_svg_quality_checker
# 75 tests：3 个 failure 已修复，剩 6 个 error
```

**已修复的 3 个 failure**（我的改动造成的夹具失效）：`test_apply_template.py` 原本用
`templates/brands/<name>` 作夹具 —— brand kind 已从工具移除，故删除该能力专测；
被删的 `styles/consulting-decision` 换成保留的 `technical-deepdive`；
deck 不再附带图片，去掉 `images/logo.png` 断言；目的冲突与 dry-run 两测改用 `DECK_ROOT`。

**剩余 6 个 error 是机器级权限问题，非本分支缺陷**：这些测试要创建符号链接做"越界逃逸"安全校验，
而当前 Windows 账户没有 `SeCreateSymbolicLinkPrivilege`（开发者模式未开），报 `WinError 1314`。
**已在非受限（danger-full-access）下复跑同一组，6 个 error 完全一致** —— 证实既非沙箱、也非本分支所致。
开启 Windows 开发者模式后即可通过。

### 7.3 导出链端到端（安装后布局）

在 `_audit-staging`（`skills/ppt-master` + `projects/` 的真实安装布局）下，用已有的 18 页
Default 项目跑完整 checker + exporter 链：

```
svg_quality_checker.py --canonical-authoring --stage final   exit=0
finalize_svg.py                                              exit=0
svg_to_pptx.py --native-charts-and-tables                    exit=0

[POSTFLIGHT] status=passed quality_gate=passed slides=18 warning_categories=0
Explicit Layout structure: 1 master(s), 11 layout(s), 40 placeholder definition(s)
Native objects: charts 0 | tables 3 | formulas 2 ; Presets: chevron x3
```

**与原树导出的结构计数完全一致**（18 页 / 1 master / 11 layouts / 40 占位符 / tables 3 / formulas 2），
说明裁剪未触及生成路径。

### 7.4 静态一致性

- 全树链接：**881 条，0 悬空**（余 1 条为 `spec_lock.schema.json` 内的正则，误报）
- Python 语法 0 错、JSON 解析 0 错
- `attribution_guard.py` exit 0
- 企业身份串（中国电信 / 中汽研 / China Telecom / CATARC）全树残留 **0**
- `register_template.py --rebuild-all --dry-run` exit 0，索引正确列出 2 条 deck

---

## 8. 尚未完成（TODO）

1. **`simple-icons` 的散文引用**：`templates/icons/README.md`、`THIRD_PARTY_NOTICES.md`、
   `scripts/icon_sync.py`（`_SYNC_LIBRARIES`）、`scripts/svg_finalize/embed_icons.py`、`references/executor-base.md`、
   `spec_lock_reference.md`、`strategist.md`、`plan-core.md`、`design_spec_reference.md`、`quick-generate.md`
   （功能影响：`icon_sync.py` 会把已删库当可用库；不崩溃，但应清理）
2. **画布注册表仍在代码里支持被删的 5 个格式**：`scripts/config.py`、`scripts/project_utils.py`、
   `scripts/svg_position_calculator.py`、`scripts/project_management/project_specs.py`、
   `scripts/generate_examples_index.py`。这是**有意的**：跨切面注册表，从代码里摘除风险高且不影响暴露面；
   `--format xiaohongshu` 仍可用，但 UI 不再提供。
3. **`templates/styles/README.md`** 是否枚举了已删的 7 个方法
4. `scripts/docs/confirm_ui.md`（catalog 文件清单）、`scripts/docs/template-tools.md`（index 清单）
5. `register_template.py` 帮助文本仍写 "brand / style / layout / deck"；`_BRAND_REQUIRED_SECTIONS` 成死代码
6. **`docs/`（仓库根）未裁剪** —— 其中 `audio narration` 等页面属于非科研场景，但它不在 skill 内，
   属仓库级文档，需要时单独处理
7. `prompt_audit` 剩余的 3 组跨文件重复段落（advisory，不影响 exit code）

---

## 9. 设计边界（有意保留）

- **`brand-only` / `flat` 等结构术语保留**。它们是 `pptx_structure.mode` 的结构概念
  （无模板身份 → 扁平结构），被 `pptx-structure-interface.md`、`semantic-svg.md`、`executor-base.md` 广泛引用。
  删除会波及结构契约本身，且它们不出现在用户的交互选项里。
- **转换器代码保留**：`pptx_animations.py`、`pptx_transitions.py`、`animation_config.py` 等仍留在
  `scripts/svg_to_pptx/`。删掉会直接破坏导出链。本轮只移除**暴露面**（文档、路由、阶段、CLI 选项），
  导出默认输出静态 deck。
- **`templates/layouts/` 全保留**：这是原生 PPTX 的 Master/Layout/占位符能力，不是商务场景。
