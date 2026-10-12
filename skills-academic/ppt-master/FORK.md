# FORK.md — 科研/学术专用分支

本目录 `skills-academic/ppt-master/` 是从 `skills/ppt-master/`（ppt-master 6.7.0）派生的

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
| `workflows/create-template/create-style.md` | 1 | 品牌工作区创建；无 brand 目录后无对象 |
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
- `workflows/routing.md`：删 5 行（create-style、video-design、animations、customize-animations、generate-audio 的触发行）；4 处替换（输出契约去掉 "narrated PPTX/MP4"、Create Template 描述去掉 brand、Quick 工作区种类 Brand/Style/Layout/Deck → Style/Layout/Deck、发现列表去掉 `brands_index.json`）
- `workflows/index.md`：删 3 行（create-style、customize-animations、generate-audio）
- `workflows/create-template.md`：子工作区分发去掉 create-style
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

### 7.2 测试套件 — 全 55 个模块，逐模块带超时

**方法**：`scripts/tests/` 下 55 个模块逐个在独立子进程里跑，每个 180s 超时
（整轮 `unittest discover` 会被挂住的模块拖死，且输出缓冲到结束，看不到进度）。
**每个模块必须继承完整环境变量** —— `config.py` 依赖 `Path.home()`，环境裁剪会让 33 个模块在导入期假失败。

**结果对照（同一 runner、同一环境，仅换 skill 根）**

| 模块 | 原树 | 学术树 | 判定 |
|---|---|---|---|
| 其余 49 个 | OK | OK | — |
| `test_image_backend_tencent` | FAIL | **OK** | 学术树更好 |
| `test_template_flow_batch1` | TIMEOUT | **OK** | 学术树更好 |
| `test_dogfood_leaves_fixes` | TIMEOUT | **OK** | 学术树更好（见 §7.2.1） |
| `test_edit_native_batch_a` | FAIL | FAIL | 预存在（缺 ffmpeg） |
| `test_source_to_md_content_loss_docx` | FAIL | FAIL | 预存在（缺 python-docx） |
| `test_template_flow_batch4` | FAIL | FAIL | 机器级符号链接权限 |
| `test_web_to_md_security` | FAIL | FAIL | 网络/TLS |

**学术树 51 OK / 4 FAIL / 0 TIMEOUT；原树 48 OK / 5 FAIL / 2 TIMEOUT。
没有任何一个模块相对原树发生回归，3 个从失败/超时转为通过。**

- `test_edit_native_batch_a`（4 个 narration 用例）：`Recorded narration requires readable audio
  durations. Install ffprobe/ffmpeg` —— 机器未装 ffmpeg
- `test_source_to_md_content_loss_docx`：`ModuleNotFoundError: No module named 'docx'`
- `test_template_flow_batch4`：创建符号链接需 `SeCreateSymbolicLinkPrivilege`（开发者模式未开），
  非受限复跑结果一致
- `test_web_to_md_security`：公网连接/TLS 校验，沙箱无网络
- `test_dogfood_leaves_fixes`：原树同样 180s 超时

**本轮修掉的真实回归（全量运行才暴露出来）**：`test_template_flow_batch1` 5 个 error 与
`test_template_flow_batch3` 1 个 failure —— 两个文件用 `templates/brands/zcare-rescue` 与合成
`brand` 工作区做夹具，而 brand kind 已从工具移除。已改为存活的 kind（`style` / `layout` /
捆绑的 `styles/technical-deepdive`），并保持每个用例原本的断言语义：
N5 不相交根、N5 多 kind 根不可部分选择、N6 外部资产漂移、N8 无关已装 spec 不能完成交接、
N8 已装资产漂移使交接失效。修复后 batch1 22 tests OK、batch3 15 tests OK。

#### 7.2.1 `test_dogfood_leaves_fixes` 超时的根因（三方交互，非本分支缺陷）

该模块在原树与学术树上**同样**卡满 180s。逐层定位：

1. 卡点是 `ImportSourcesProjectTreeTests.test_research_web_sources_dir_is_not_a_project`
   的 `tempfile.TemporaryDirectory(dir=PROJECTS_ROOT)` 这一行（插桩计时确认：进到该行前 0.36s，
   之后不再前进）。
2. `PROJECTS_ROOT` = `E:\ppt-master-6.7.0\projects`（`config.py:42` `REPO_ROOT = PROJECT_ROOT.parent.parent`；
   两棵树都恰好在仓库下两层，故解析到同一路径 —— 这正是原树也卡住的原因）。
3. 该目录**已存在**，而沙箱只允许在根目录与会话内新建的目录里写入 →
   `os.mkdir(PROJECTS_ROOT / ...)` 抛 `PermissionError [WinError 5]`。
4. CPython `tempfile._mkdtemp` 在 Windows 上把 `PermissionError` 当作"候选名被占用"处理，
   判据是 `os.access(dir, os.W_OK)` —— 而 Windows 的 `os.access` **只检查只读属性、不检查 ACL**，
   于是恒为 True，循环继续。
5. 本机 Python 构建的 `tempfile.TMP_MAX` 是 **2147483647**，不是常见的 10000。

⇒ 每次 mkdir 立即被拒 → 重试约 21 亿次 → 永远跑不完。

**实验证明**：把 `TMP_MAX` 压到 5 / 50 / 200，同一调用在 0.00 / 0.01 / 0.03 秒内以
`FileExistsError: No usable temporary directory name found` 返回。在可写 `projects/` 的正常环境里，
第一次 mkdir 就成功，测试瞬时通过。

**修法**：先用一次真实 `mkdir` 探测 `projects/` 是否可写，不可写则 `skipTest` 并给出原因
（可写时行为与原来完全一致）。修复后该模块 **1.8s 跑完，51 tests OK (skipped=1)**。

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

## 8. 第四轮：词表、图标库与命名（已完成）

**表格词表**：`tables_index.json` 移除 `feature_matrix`（产品能力对比网格）→ 5 个；
`table-vocabulary.md` 投影同步删除该行。保留 `comparison_matrix` / `hierarchical_table` /
`metric_table` / `rating_matrix`（准则×方案的序数评分，科研评价可用）/ `record_table`。

**图标库 `simple-icons` 彻底移除**（不只是删目录）：

| 位置 | 处理 |
|---|---|
| `scripts/icon_sync.py` | `_SYNC_LIBRARIES` 不再并集 `simple-icons`；docstring 与错误提示同步 |
| `scripts/svg_finalize/embed_icons.py` | 移除尺寸映射项与 docstring 说明 |
| `templates/icons/README.md` | 删除库表行、示例、检索示例、Brand-logo exception 段；计数 `12,027 / 五库` → `8,352 / 四库` |
| `templates/icons/THIRD_PARTY_NOTICES.md` | 删除 Simple Icons 许可与商标声明整节（库已不存在，保留声明是错的） |

**命名去企业化**：`references/image-renderings/corporate-photo.md` → `professional-photo.md`，
9 个文件同步（`image-generator.md`、`image-renderings/_index.md` 与同级文件、
`visual-styles/` 配对渲染列、`ai-image-comparison` 清单、Confirm UI）。
`app.js` 的四语言标签改为 `专业摄影 / 專業攝影 / Professional photo / プロフェッショナル写真`，
目录描述 `product shots` → `field, reportage, and subject photography`。

**残留 `brand` kind 引用清零**：`routing.md` §4、`edit-native-pptx.md`、
`scripts/docs/{template-tools,confirm_ui}.md`、`register_template.py`（docstring + 帮助文本）、
`references/template-designer.md`、`templates/styles/README.md` 优先级表。

**本轮修复的一个自伤**：删除 `icon_sync.py` 里 simple-icons 提示串时拆坏了 `print()` 调用
（留下孤立参数），已修复并全树复验。

---

## 9. 最终状态

| 项目 | 结果 |
|---|---|
| 文件数 | 13,016 → 9,281 |
| 全树链接 | 881 条，0 悬空（1 条正则误报） |
| Python 语法 / JSON 解析 | 0 错 / 0 错 |
| `attribution_guard.py` | exit 0 |
| `prompt_audit.py` | **exit 0**（1 条 advisory 警告） |
| 测试（相关定向组） | 69/75 通过；6 个 error 已证实为机器级符号链接权限 |
| 导出链端到端 | postflight passed，18 页，1 master / 11 layouts / 40 占位符 |
| 企业身份串残留 | 0 |
| 非科研 `brand` kind 引用残留 | 0（§11 修正了本轮此前误报的 0） |
| 交互选项 | 模式 4 / 画布 3 / 版式 4 / 图标库 4 |

### 有意保留的边界（见 §10）

1. **画布注册表已在代码层裁剪为 3 个格式**（`config.py` `CANVAS_FORMATS`、`project_utils.py`、
   `svg_position_calculator.py`、`project_specs.py`、`generate_examples_index.py`）。
   > **更正**：本文件早期版本在这里写的是"跨切面注册表，从代码里摘除风险高且不影响暴露面：UI 不再提供"。
   > 这个判断**是错的**。`confirm_ui/server.py::_build_catalogs` 的注释写明 *"canvas synced live from
   > config"* —— 画布选项以 `config.CANVAS_FORMATS` 为唯一真源，`catalogs.json` 只补文案。
   > 因此只改 `catalogs.json` 时，UI 实际仍提供全部 8 个格式（含 WeChat / 小红书 / 朋友圈 / 竖屏 / 横幅）。
   > 现已从所有并列注册表移除这 5 个格式；实测 `/api/catalogs` 返回 3 个，全套测试无新增失败。
   > **教训**：改一个"选项"前，先确认 UI 的真源在数据文件还是在代码注册表。
2. **仓库根 `docs/` 未裁剪** —— 其中 `audio narration` 等页面属非科研场景，但它不在 skill 内。
3. **`prompt_audit` 的 3 组跨文件重复段落**（advisory，不影响 exit code）。
4. **`register_template.py` 的 `_BRAND_REQUIRED_SECTIONS` 成死代码**；无害，未删以免波及校验路径。

## 10. 设计边界（有意保留）

---

## 9. 设计边界（有意保留）

- **`brand-only` / `flat` 等结构术语保留**。它们是 `pptx_structure.mode` 的结构概念
  （无模板身份 → 扁平结构），被 `pptx-structure-interface.md`、`semantic-svg.md`、`executor-base.md` 广泛引用。
  删除会波及结构契约本身，且它们不出现在用户的交互选项里。
- **转换器代码保留**：`pptx_animations.py`、`pptx_transitions.py`、`animation_config.py` 等仍留在
  `scripts/svg_to_pptx/`。删掉会直接破坏导出链。本轮只移除**暴露面**（文档、路由、阶段、CLI 选项），
  导出默认输出静态 deck。
- **`templates/layouts/` 全保留**：这是原生 PPTX 的 Master/Layout/占位符能力，不是商务场景。

---

## 11. 第五轮：`brand` kind 的文档残留清理（已完成）

**起因**：本轮此前在 §8 声明「残留 `brand` kind 引用清零」，但那个结论是**误报**。
当时的扫描只匹配 `--kind brand` 这类**代码字面量**，漏掉了散文形态 ——
`Create Brand`、`brand-only`、`Brand/Style`、`Brand overrides Deck identity`。
实际残留分布在 **20+ 个文件、约 50 处**；其中 `workflows/create-template.md` 一处就占约 20 处
（含一整行 Create Brand 子工作区分发行、`Kind: brand | style | layout | deck`、
`Primary Color ← Brand/Deck only` 等），足以让模型去找一个**已删除的子工作流**。

**判据**：区分三种 `brand`，只清第一种。

| 类别 | 处置 |
|---|---|
| **已删的工作区种类**（`kind: brand`、`templates/brands/`、`brand_id`、`brand-only`、`Create Brand`） | 清除 |
| **`category: brand` 发现分类枚举**（`engineering_blue` / `signal_red` 仍在使用） | **保留** |
| **一般语义**（`brand-neutral`、`user / brand`、`brand manuals`、`brand marks` / `simple-icons`） | **保留** |

**清理范围（24 个文件）**

- `workflows/create-template.md`：删 Create Brand 分发行与身份字段行；kind 枚举收为 `style | layout | deck`；
  `--kind brand|style|deck|layout` → `--kind style|deck|layout`；其余约 15 处散文改为只剩 Style。
- `references/strategist-template.md`：优先级规则
  `all four may coexist. Brand overrides Deck identity. Layout overrides Deck structure; Deck keeps application context and identity not overridden by Brand;`
  → `all three may coexist. Layout overrides Deck structure; Deck keeps application context and identity;`；
  另 3 处 `Brand/Deck` → `Deck`。
- 扁平页分类 `brand-only` 的清零：`references/executor-base.md`、`references/executor-structured.md`、
  `references/pptx-structure-interface.md`、`references/semantic-svg.md`、
  `references/shared-standards-core.md`、`references/strategist.md`、`scripts/docs/svg-pipeline.md`。
- 其余：`SKILL.md`、`workflows/routing.md`、`workflows/generate-pptx.md`、
  `workflows/profiles/image-to-pptx.md`、`workflows/profiles/quick-generate.md`、
  `workflows/stages/apply-template-workspace.md`（示例路径 `templates/brands/mckinsey/` → `templates/layouts/report_core/`）、
  `workflows/create-template/create-deck.md`、`templates/README.md`、`templates/layouts/README.md`、
  `scripts/apply_template.py`、`scripts/mirror_template_materialize.py`、`scripts/register_template.py`、
  `scripts/svg_quality/checker.py`、`scripts/svg_quality/cli.py`、
  `scripts/svg_to_pptx/pptx_package/cli.py`、`scripts/docs/template-tools.md`。

**指纹刷新**：上述编辑使 `prompt_audit_manifest.json` 的 `schema_grammars` accepted 指纹失配 6 处
（`page_layouts` / `page_pptx_layouts` / `page_visualizations` / `pptx_layouts` / `pptx_masters`
的 projection，以及 `image_ai_path` 的 owner）。已用审计自身的 `_schema_owner_fingerprint` 与
`_schema_projection` 重算并更新 —— 这是**人工复核过编辑之后的正常重录**，不是绕过检查。
其中 `image_ai_path` 的 owner 失配源于**更早一轮**改 `scripts/docs/confirm_ui.md` 时漏刷，一并补上。

**有意保留**

- `register_template.py` 与 `checker.py` 内部对 `brand` 工作区的**校验实现**（`_BRAND_*` 常量、
  `validate_brand_workspace`、`'brand': validate_brand_workspace` 映射）。这是**不可达死代码** ——
  没有 brand 目录可指，且 `--kind` 的 choices 由分派表生成，CLI 实际输出为 `--kind {style,layout,deck}`。
  删它要动 kind 分派表，风险大于收益。
- `references/visual-review.md` 的 `brand_review.json` 与 "Brand-token" 措辞。功能正常
  （指 `spec_lock.md` 里锁定的设计 token），文件名是在用产物名，改名会牵动编排侧的聚合逻辑。
- `prompt_audit_manifest.json` 里的 Brand `load_sets` —— **本轮已清理，见下**。

**治理层：Brand `load_sets` 的清理（本轮完成）**

该 manifest 是 `audit_only: true` / `runtime_consumed: false`（上下文预算测量记录，不参与运行时）；
`coverage` 只有 `exempt` 列表、无「必须被覆盖」断言；6 个名字在 manifest 之外**零引用**。
因此删除不影响运行，也不影响审计。

| load_set | 处置 | 理由 |
|---|---|---|
| `route.create-template.brand` | 删除 | 兄弟 `route.create-template.{style,layout,deck}` 均在，只此一条无对应能力 |
| `stage.generate.template.brand` | 删除 | 单 Brand 工作区应用，已不可能 |
| `stage.generate.template.brand-two` | 删除 | 双 Brand 冲突路径，已不可能 |
| `route.generate.brand-flat-no-image` | 删除 | 建在已删的 stage 上；Style 路径由 `stage.generate.template.style` 覆盖 |
| `stage.generate.template.fusion-brand-style-layout-deck` | **改名** → `stage.generate.template.fusion-style-layout-deck` | 三类最大融合**仍然可能**，是上下文上界，必须保留；只去掉 Brand 并改描述 |
| `route.generate.quick-generate.template-fusion` | 更新描述与 `include` | 指向改名后的 stage |

`load_sets` 95 → 91；终检 **0 个含 brand、0 个悬空 `include`**，`prompt_audit` 仍 exit 0。

**验收**

| 检查 | 结果 |
|---|---|
| `prompt_audit.py` | **exit 0**（仅剩改动前即存在的 DUPLICATE_EXACT_CANDIDATES 警告） |
| `attribution_guard.py` | exit 0 |
| `hyperlink_contract.py` | exit 0 |
| Confirm UI `TEMPLATE_KINDS` | `style` / `layout` / `deck` |
| `register_template.py --help` | `--kind {style,layout,deck}` |
| 测试套件（56 模块） | 51 OK；5 FAIL 全部为机器级（符号链接特权 / 缺 ffmpeg / 临时目录权限 / 缺 python-docx / 无网络） |
| 终检残留 | 4 处，全部为上述不可达死代码 |
| Brand load_sets | 0（4 删 1 改名 1 更新；91 条，0 悬空 include） |

---

## 12. 第六轮：Confirm UI 汉化与模板库中文标签（已完成）

**起因**：学生看 Stage 1 / Stage 2 时大量选项是英文或内部术语，读不懂。

### 12.1 补上 §11 漏掉的一类文件

§11 的扫描只覆盖 `.md` / `.py` / `.json`，**漏了 `.js`**，因此 `confirm_ui/static/app.js`
四语言字典里的 Brand 残留未被发现：

```
template_use_desc: "选择一个或多个 Brand、Style、Layout、Deck 或指定工作区。"
```

四种语言的 `template_use_desc` 全部含 Brand，本轮一并清除。
`index.html` / `style.css` 里的 `.brand-block` / `.brand-mark` 是**应用 logo 的 CSS 类名**，
不面向用户，保留。

### 12.2 界面文本汉化（38 项）

只改学生看不懂的；已经清楚的条目（目标受众 / 色彩方案 / 字体方案 / 图标使用 …）不动。

| 类别 | 示例 |
|---|---|
| **英文种类名** | `Style` / `Layout` / `Deck` → **风格模板 / 版式模板 / 成套模板** |
| **过期数量词** | "**四种**模板均可组合" → "三类可任意组合"（Brand 移除后只剩三种） |
| **内部角色名** | "由 **Strategist** 推导视觉系统" → "由 **AI** 自己推导配色、字体和版面" |
| **文件格式术语** | "阅读模板的全部 **SVG**" → "读完你选的模板" |
| **结构术语** | "各**根**的模板类型不得重叠" → "每个目录自带类型，同一类型不能重复选" |
| **抽象节标题** | 主动执行 → **自动生成项**；图片生产 → **生成配图设置** |

替换一律在**目标语言的字典块内**进行 —— 裸值替换（如 `"Style"`）会误伤 `en` 字典与代码本身。

### 12.3 模板库中文标签（贯通四层）

下拉里显示的是原始 id（`academic-research` / `report_core` / `engineering_blue` …），
因为候选对象的 `label` 就是 id，且索引里没有中文字段。UI 的
`localized(candidate, "label")` 本来就支持 `label_zh`，缺的是上游数据。

链路：`design_spec.md` frontmatter → `register_template.py` 索引 → `server.py` 候选 → UI（零改动）

| 层 | 改动 |
|---|---|
| 13 个 `design_spec.md` | frontmatter 增 `label_zh` 与 `summary_zh` |
| `register_template.py` | `_STYLE_ALLOWED_FRONTMATTER_FIELDS` 增两个字段；新增 `_localized_fields()` 做类型校验；style / layout / deck 三处 `entry` 透传 |
| `confirm_ui/server.py` | `_build_template_library()` 的候选对象透传两个字段 |
| `confirm_ui/static/app.js` | **零改动** |

`register_template.py --rebuild-all` 重建三个索引后，7 个风格、4 个版式、2 个成套模板
全部有中文名与中文摘要。

**命名**：风格用「学术研究 / 规程手册 / 事故复盘 / 叙事演讲 / 科学解释 / 技术深潜 / 工作坊教学」；
版式用「满版编辑 / 演示核心 / 演示核心 4:3 / 报告核心」；成套模板用「工程蓝 / 信号红」。
中文摘要按各 spec 的英文 summary 重写，不新增原文没有的能力描述。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check app.js` | 语法 OK |
| 四语言字典结构 | 各 182 键，**缺 0 / 多 0** |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |
| 模板相关测试（64 项） | 63 OK；1 error 为机器级符号链接特权 |
| 测试套件（56 模块） | 52 OK；4 FAIL 全部机器级（ffmpeg / python-docx / 符号链接 / 无网络） |
| `/api/recommendations` 的 13 个候选 | 全部带 `label_zh` + `summary_zh` |

---

## 13. 第七轮：模板预览图（已完成）

**起因**：用户反馈 Stage 1 的版式模板与成套模板「看都看不懂」—— 光有名字
（满版编辑 / 报告核心 / 工程蓝 / 信号红）无法判断长什么样。

### 13.1 生成预览素材

用 `template_preview_pptx.py` 把工作区导出为 review PPTX，再用捆绑的 LibreOffice Kit
渲染成 PNG，最后拼版（Pillow）。13 个模板里 **只有 4 个版式与 2 个成套模板有原型页面**；
7 个风格模板的 spec 明确写着 no SVG roster（只提供方法与设计默认值），**没有可渲染的页面**，
因此不给预览图，下拉里靠名称与摘要说明。

产物落在 `scripts/confirm_ui/static/template_previews/`，一模板一张拼版图：

| 文件 | 页 |
|---|---|
| `deck_engineering_blue.png` / `deck_signal_red.png` | 封面、章节、内容 |
| `layout_report_core.png` | 封面、标题内容、图表、流程 |
| `layout_presentation_core.png` / `layout_presentation_core_43.png` | 标题、内容、两栏、KPI |
| `layout_editorial_bleed.png` | 满版、满版加蒙版、分栏、三联 |

再生成流程写在同目录的 `README.md`；生成脚本固化为 `scripts/build_template_previews.py`。
渲染需要 LibreOffice Kit，因此 PNG 入库，**Confirm UI 运行时不依赖渲染器**。

### 13.2 接入 UI

| 文件 | 改动 |
|---|---|
| `confirm_ui/static/app.js` | 新增 `templatePreviewUrl()`；`renderTemplateSelectField()` 在下拉下方加预览图，随选中项更新，无图则隐藏，`onerror` 兜底 |
| `confirm_ui/static/style.css` | `.template-preview` / `.template-preview-img` |
| `scripts/prompt_audit_manifest.json` | 新增 README 无法归入任何 load set，按既有惯例加入 `coverage.exempt` 并写明理由 |

**验收**

| 检查 | 结果 |
|---|---|
| 6 张预览图经 HTTP 可取 | 全部 200 |
| `node --check app.js` | 语法 OK |
| `prompt_audit` | exit 0（Coverage: 142 in load sets / 34 exempt / **0 uncovered**） |
| `attribution_guard` / `hyperlink_contract` | exit 0 |
| confirm_ui 测试 | 6 OK |
| 测试套件（56 模块） | 52 OK；4 FAIL 全部机器级 |

---

## 14. 第八轮：模板浮窗提示与简介的可读性（已完成）

**起因**：用户看 Stage 1 模板下拉的悬停提示，得到的是
「16:9 纯结构版式，10 个版面：图片出血到画布边缘，文字压在图上并加蒙版。 ·
`E:\...\skills\ppt-master\templates\layouts\editorial_bleed`」——
一半是印刷术语（「出血」），一半是本地绝对路径。

### 14.1 浮窗不再带路径

`templateOptionTitle()` 原本把 `workspace_root` 拼进悬停提示。该函数**只**服务于模板库
下拉（L1293 一处调用）；「指定目录」那一栏走 `template-selected-path-value` 单独渲染
完整路径。因此提示里再带一次路径纯属噪音，还会泄露本地目录结构。已改为只返回简介。

### 14.2 简介改为描述观感与场合

原先 6 条简介是按 spec 规格表写的（页数、版面数、结构术语），现在改成说「长什么样、
什么时候用它」：

| 模板 | 新简介（节选） |
|---|---|
| 报告核心 | 像一份正式报告：页眉、页脚和页码固定在版面上，标题下一条细线，内容区干净不加框。 |
| 演示核心 | 最通用的一套，20 种页面可选……内容装在浅灰圆角卡片里。拿不准选它就对了。 |
| 演示核心 4:3 | 和「演示核心」同一套设计，但画布是 4:3 的方屏比例。 |
| 满版编辑 | 图片铺满整页、四周不留白边，文字压在图上并加深色蒙版以保证看得清。 |
| 工程蓝 | 深蓝底、白字的稳重风格：封面和章节页是整片深蓝，内容页白底。 |
| 信号红 | 白底配红黑两色：红色顶栏底栏加左侧红竖条，清爽又有力度。 |

「出血」等印刷术语全部去掉；页数与版面数不再进用户可见文案。
7 个风格模板的简介本来就描述方法本身，未改。

**验收**

| 检查 | 结果 |
|---|---|
| 服务端候选的 `summary_zh` | 6 条全部为新文案 |
| 服务端 `app.js` 的 `templateOptionTitle()` | 函数体内**不含** `workspace_root` |
| `node --check app.js` | 语法 OK |
| 三个索引重建 | layout 4 / deck 2，`[OK]` |

**流程教训**：上一轮把 `app.js` / `style.css` 的改动写进了 `_audit-staging`，
随后 `robocopy /MIR` 从 fork 覆盖过去，改动被自己抹掉。**约定：改 fork，再同步。**
本轮及之后所有改动均在 `skills-academic/` 下完成后再同步；同步后已复核 fork 与 staging
逐字节一致（0 差异）。

---

## 15. 第九轮：「指定目录」的文案澄清（已完成）

**起因**：用户问 Stage 1「指定目录」是干什么的 —— 原文案
「可以使用本次运行中另外指定的模板目录」没说清**谁会指定**，也没说清它与上方模板库的关系。

**它实际是什么**（`workflows/routing.md` §7 与 `generate-pptx.md` Step 3）：

> Candidates follow routing.md §7: **registered roots from the four indexes** plus
> **every exact root supplied for this run**.
> | Explicit current workspace root exposing at least one `templates/` Design Spec |
> Preserve it as a Stage-1 candidate and initialize template mode |

即：**本次运行中明确给出的模板工作区根**，按绝对路径给出，不来自模板库索引。
常规运行下为空数组。另有一条硬规则：**绝不把模板名解析成本地路径** ——
只报名字（如「用学术研究」）只能从上方模板库索引里选。

| 键 | 原文案 | 新文案 |
|---|---|---|
| `template_source_explicit` | 指定目录 | **本次指定的模板** |
| `template_none_explicit` | 本次运行没有指定模板目录 | **本次没有另外指定模板 —— 用上面的模板库就行** |
| `template_explicit_hint` | 可以使用本次运行中另外指定的模板目录。…… | **这里是本次明确给出的模板文件夹（不在上面的模板库里）。每个文件夹自带类型，同一类型不能重复选；选中后下方会显示它的完整路径，方便你核对。** |

zh / zh-TW / en 三种语言共 8 处；ja 未改（语言菜单只有中文与 English 两项）。

**顺带发现一处死条目**：`sec_template_explicit`（四语言均有）**没有被任何渲染调用**——
该栏的标题实际取自 `template_source_explicit`（`app.js` L1335）。未删除，仅记录。

**验收**

| 检查 | 结果 |
|---|---|
| 服务端 `app.js` 的三个键 | 全部为新文案 |
| `node --check app.js` | 语法 OK |
| 替换计数 | zh 3 / zh-TW 3 / en 2，未命中 0 |

---

## 16. 第十轮：「设计基础」的信息架构修正（已完成）

**起因**：用户指出「从零设计」的说明写着「由 AI 根据这份材料自己推导**配色、字体和版面**」，
读者自然会把下面并排的三个下拉理解成**分别对应这三件事**；但实际是
**风格模板 / 版式模板 / 成套模板**——三种模板包，而且「成套」包含前两者，是**层级关系而非并列**。

**实际语义**（据各 spec 的 frontmatter 与 `strategist-template.md` 的优先级规则）：

| 模板类型 | 提供什么 |
|---|---|
| 风格模板 | 沟通方法与视觉方向：配色、字体、装饰、构图节奏；**不含页面结构** |
| 版式模板 | 母版、版面、占位符等页面结构；**不含配色与字体身份** |
| 成套模板 | 身份 + 结构 + 应用场景，**一次给全** |

三者不是三个维度，而是「整包」与「拆成两半」。用户若按「配色/字体/版面」去对应，必然选错。

**改法**（三处，互不冲突）：

1. **不再制造错误并列**：`template_free_desc` 改为「不套用现成模板，整套视觉与版面由 AI
   根据这份材料现做。」——不再枚举三样东西。
2. **每栏自己解释自己**：新增 `template_kind_gives_style` / `_layout` / `_deck` 三个 i18n 键，
   在下拉标签下方渲染一行小字（`renderTemplateSelectField()` + `.template-select-gives`）：
   「只给配色和字体，不给页面结构」/「只给页面结构，不给配色」/「配色和版面一次给全，最省事」。
   兜底用 `t(key) !== key` 判断——`t()` 找不到键时返回键名本身，因此未知类型不会渲染出原始键。
3. **顶部提示只留组合规则**：`template_library_hint` 改为「每类最多挑一个，可以只挑一类，
   也可以组合。同时套用时，版面以版式模板为准，配色和字体沿用成套模板。」

`template_kind_*` 三个短标签**保持原样**——它们同时用于「本次指定的模板」一栏的 kind 展示
（`explicitRootOptions()`），加长会在那里显得累赘。

**验收**

| 检查 | 结果 |
|---|---|
| i18n 替换/新增 | 16 项，**未命中 0**（zh / zh-TW / en） |
| 服务端 `app.js` 的 6 个键 | 全部为新文案 |
| 渲染层 `.template-select-gives` | 已接入 |
| `style.css` `.template-select-gives` | 已加 |
| `node --check app.js` | 语法 OK |

---

## 17. 第十一轮：Stage 2 信息架构审查（已完成）

**起因**：§16 修掉 Stage 1「设计基础」的假并列之后，同一类问题在 Stage 2（15 个节）尚未审过。
本轮先枚举渲染顺序与每节的「标题 / 说明 / 实际字段 / 条件」，再逐条判读。

**Stage 2 实际顺序**（`app.js` 渲染入口）：模板应用方式 → 成套方案 → 内容展开方式 → 视觉方向
→ 阅读模式 → 页数 →（色彩方案 · 图标使用 · 字体方案，包在 `.style-group` 里）→ 图片使用
→ 生成配图设置 → 自动生成项 → 生成模式 → 先审核设计规范 → 设计规范详细程度。

发现六处，其中三处用户可见：

| # | 问题 | 处置 |
|---|---|---|
| **F4** | **节名与选项不符**：「叙事方向」的四个选项是金字塔（结论先行）/ 叙事 / 教学 / 简报——这是**内容组织方式**，「金字塔」尤其不是叙事；且节名与选项「叙事」撞词 | `sec_narrative` → **内容展开方式** / `How the content unfolds` |
| **F5** | **说明与字段标签用词不一致**：`image_production_hint` 写「图片来源和**渲染方向**已在上方选择」，而上方那一栏的字段标签是「**生成图风格**」 | 说明改为「图片来源和**生成图风格**已在上方选好……」，en 同步 |
| **F6** | 同一件事两个词：标题「成套设计方向」vs 提示里的「成套方案」 | 标题统一为 **成套方案** / `Coherent design options` |
| **F1** | `section()` 的**首参是死参数**——显示编号取自 `_secCounter`，`num` 完全未使用；18 个调用点白传，其中 8 个传字母（"T"/"B"/"D"/"P"/"M"/"A"/"R"）伪装成有意义 | 删除该参数与 18 处实参 |
| **F3** | 「阅读模式」的节标题**借用目录字段名** `delivery_purpose`（其余节都走 `sec_*`）；目录里该字段的语义是"传递目的"，与"阅读模式"并不等同 | 新增 `sec_reading_mode`（三语言），调用点改用 |
| **F2** | `sub_mode`（叙事模式）四语言都有，**从未被任何渲染调用** | 删除 |

**一个被否掉的怀疑**：`sec_visual` 与 `sec_color` 都传 5、`sec_reading_mode` 与 `sec_design_spec_depth`
都传 "D"，看似重号——但 `section()` 根本不用首参，编号由计数器给出，**不存在重号**。
真正的问题是那个参数本身（F1）。

**有意保留**：`delivery_purpose` 作为 **state / JSON 兼容键**仍在使用（`app.js` L4171 注释：
"Keep the legacy delivery_purpose key for JSON compatibility"），只有它的 i18n 节标题成了死键。
未删除，仅记录。

**验收**

| 检查 | 结果 |
|---|---|
| 修正项 | 18 项，**未命中 0** |
| `node --check app.js` | 语法 OK |
| 服务端 `app.js` | 内容展开方式 / 成套方案 / `sec_reading_mode` / 生成图风格 全部就位；`section(` 死参数 0 残留；`sub_mode` 0 残留 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |
| confirm_ui 测试 | 6 OK |

---

## 18. 第十二轮：三类模板「给什么」的更正（已完成）

**这是一次错误更正，记下原因。**

§16 给三个模板下拉各加了一行小字说明「这类给什么」。其中风格模板写成
**「只给配色和字体，不给页面结构」** —— 与它自己的模板简介（「论文式汇报方法：……**」）**对不上。
用户当场指出。**该句是凭印象写的，没有查规范。**

### 18.1 权威依据

`workflows/create-template.md` 的子工作区表：

| Child | Select when | Exclusive responsibility |
|---|---|---|
| Create Style | Reuse a **communication method and visual direction** without identity truth or prototypes | **Method**, page-role vocabulary, evidence expression, visual defaults, image/icon direction, advisory review focus; **no roster** |
| Create Layout | Reuse a **brand-neutral structural skeleton** without a recurring application | Canvas, page grammar, semantic text roles, **Master/Layout/slot contract, SVG roster**; no identity or application contract |
| Create Deck | Reuse a **branded structural system or a recurring application** | Descriptive application context, **integrated identity/structure**, SVG roster |

三个 spec 的实际章节（决定性证据）：

| kind | 章节 |
|---|---|
| style | I 概览 · **II 沟通方法** · III 页面角色词汇 · IV 证据与数据表达 · **V 视觉系统默认值** · VI 图片图标方向 · VII 评审关注点 |
| layout | IV 标志性设计元素 · **V 页面名册** |
| deck | I 概览 · **II 配色方案** · **III 字体** · IV 标志性元素 · **V 页面名册** |

### 18.2 更正结果

| kind | 错 | 对 |
|---|---|---|
| style | 只给配色和字体，不给页面结构 | **管「怎么讲」——汇报方法与视觉基调；页面结构要另配** |
| layout | 只给页面结构，不给配色 | **管「长什么样」——母版与版面；配色字体要另配** |
| deck | 配色和版面一次给全，最省事 | **页面结构、配色字体、适用场景，一次给全** |

**deck 那条也连改两次**：第一版写「『怎么讲』和『长什么样』一次给全」，但 deck 的 spec
**没有 Communication Method 章节**，`create-template.md` 也只说 "integrated identity/structure"。
成套给的是**身份 + 结构 + 应用语境**，**不含沟通方法**。

**教训**：给用户看的解释必须来自规范或 spec 的**实际内容**，不能来自"这类东西大概是干什么的"的
直觉。§16 那三条小字的意图（就地解答"这类给什么"）是对的，错在**内容不是查出来的**。

---

## 19. 第十三轮：「设计基础」这一节到底决定什么（已完成）

**起因**：用户追问——节说明写「决定这份演示的**外观和结构**从哪来」，而风格模板的小字写
「管『**怎么讲**』——汇报方法与视觉基调」，模板浮窗又写「**论文式汇报方法**」。
**汇报方法与外观结构是两件独立的事，为什么混在一起？**

### 19.1 事实（规范原文）


eferences/strategist-template.md：

> **Style owns Direction / method only**: its visual values are candidate defaults that
> yield to resolved Deck identity, and its **preferred Mode / Visual Style seed the single
> final locks**.

风格 spec 的 ## II. Communication Method 含 Preferred Mode / Mode References /
Mode Behavior（一整段论证顺序的说明）——**风格模板确实同时装着方法与视觉两样**。

**但两者在这一节都不被最终决定。** 该节只决定「设计从哪来」；模板自带的做法作为
**默认值**预填到下面几节（内容展开方式 / 视觉方向 / 色彩方案 / 字体方案），在那里可以逐项改。
规范也把这层写清楚了：它们是 **candidate defaults**，只 **seed** 最终锁定值。

### 19.2 问题所在

不是事实错，而是**两句的框架不一致**：节说明用「外观与结构」的框架，小字用「方法与视觉」的
框架，读起来像这一节同时敲定两件独立的事。

### 19.3 改法

| 键 | 现在 |
|---|---|
| 	emplate_choice_hint | **这一节只决定「设计从哪来」：让 AI 现做，还是套用现成模板。套用模板后，模板自带的做法会作为默认值预填到下面几节，你在那里仍然可以逐项修改。** |
| 	emplate_kind_gives_style | 给「怎么讲」和视觉基调的**默认值**；页面结构要另配 |
| 	emplate_kind_gives_layout | 给页面结构的**默认值**（母版与版面）；配色字体要另配 |
| 	emplate_kind_gives_deck | 页面结构、配色字体、适用场景，一次给全 |

三条小字全部点明「默认值」，与节说明的「仍然可以逐项修改」呼应。

**验收**：更正 12 项未命中 0；
ode --check OK；prompt_audit exit 0。

---

## 20. 第十四轮：模板简介改为「视觉优先」（已完成）

**起因**：用户指出——**PPT 模板的核心目的是选视觉效果**，但三类模板里用户无法把每个选项
与"最终会长成什么样"挂钩，这是展示失败。7 个风格模板的简介尤其严重，只讲方法：

> 学术研究 — 论文式汇报方法：从问题、方法到结果，逐步立起一个经得起质疑的结论……

读完**不知道这会长成什么样**。

### 20.1 数据来源

全部改写依据各 spec 的 ## V. Visual System Defaults 与 ## VI. Image & Icon Direction，
不凭印象。7 个风格的视觉特征其实非常具体：

| 模板 | 底子 | 装饰 | 颜色用法 |
|---|---|---|---|
| academic-research | swiss-minimal | 几乎为零，只有发丝线 | 只编码一个声明过的变量 |
| duty-manual | 暗场网格 | 网格/引线/刻度**本身是信息** | 一个冷色结构 + 两个强调色分工固定 |
| incident-postmortem | swiss-minimal | 几乎为零 | 只留给**严重度与状态** |
| narrative-keynote | editorial | 几乎没有，靠尺度与留白 | 随叙事弧线**由暗转亮** |
| science-explainer | paper-cut | 层=概念、箭头=方向、大小=量级 | 固定代表某物质/某阶段 |
| technical-deepdive | blueprint | 线宽/虚线/箭头**都承载含义** | 编码层次或路径类型 |
| workshop-teaching | sketch-notes | 圈画、箭头、页边标注 | 区分「新的/变了的/对的/错的」 |

### 20.2 写法

统一为「**先讲长什么样，再讲适合什么**」：

> 学术研究 → **极简学术风：大留白、只有发丝分隔线、几乎没有装饰；颜色只用来标记分组或条件，
> 全篇同一实体同一色。** 适合论文答辩、会议报告。

共改写 8 条（7 风格 + 演示核心），另外 5 条（满版编辑 / 演示核心 4:3 / 报告核心 / 工程蓝 /
信号红）原本就以视觉开头的，保持不动。

英文 summary 是 spec 自身的原始描述，未改；本轮只改用户可见的 summary_zh。

**验收**：13 条经 /api/recommendations 全部返回新文案；prompt_audit exit 0；
fork 与 staging 0 差异。

---

## 21. 第十五轮：三个层级统一到「视觉」框架（已完成）

**起因**：§20 把 13 个模板的简介改成视觉优先之后，用户指出**上下不一致**：

| 层 | 改前 | 框架 |
|---|---|---|
| 栏目标签 | 风格模板 / 版式模板 / 成套模板 | **功能词** |
| 栏目小字 | 管「怎么讲」/ 管「长什么样」/ 一次给全 | **半功能半视觉** |
| 模板简介 | 极简学术风：大留白…… | **视觉**（§20 已改） |

三套框架并存，读起来互相打架。用户的要求是：**让简介的解释直接对应用户看到的最终视觉**，
所以三层必须同框。

### 21.1 统一后

| 层 | 改后 |
|---|---|
| 节标题 | 设计基础 → **整体视觉** |
| 节说明 | 这一节决定整套视觉从哪来……套用后，模板的配色、字体和页面版式会成为下面几节的**默认值**……你随时都能改。 |
| 栏 1 | **视觉基调** — 配色、字体、装饰密度；页面版式要另配 |
| 栏 2 | **页面版式** — 母版与版面，决定内容怎么摆；配色字体要另配 |
| 栏 3 | **整套视觉** — 视觉基调与页面版式一次给全 |
| 组合规则 | 同时套用时，**页面版式以版式那一栏为准，配色和字体沿用整套那一栏**。 |

**「方法」不再进三个小字** —— 那里只讲视觉。它会预填 Stage 2 的「内容展开方式」这件事，
只在共同的节说明里提一次。

**用词统一**：Stage 2 的「成套方案」→「**整套方案**」，与「整套视觉」同词根。

### 21.2 本轮修掉的一个自伤

英文 `template_choice_hint` 里写了 `pre-fills "how the content unfolds"` —— **直双引号截断了
JS 字符串**，`node --check` 报 `SyntaxError: Unexpected identifier 'how'`。

更糟的是：**第一次检查时我读到的"语法 OK"是假的** —— `$LASTEXITCODE` 取到的是
PowerShell 管道里 `Select-Object` 的结果，不是 node 的退出码。单独取退出码后才看到真实失败。

修法：串内改用单引号。**教训：检查退出码时不要把它接在管道后面。**

（同一个坑本轮踩了三次：用 PowerShell here-string 调 Python 时，`\"` 会被吞掉或转义出错。
正确做法是**把脚本写成文件再执行**，不要内联带引号的 Python。）

**验收**

| 检查 | 结果 |
|---|---|
| 统一项 | 31 项，未命中 0 |
| `node --check`（真实退出码） | **0** |
| en 串含裸双引号 | False |
| 服务端返回的十项文案 | 全部就位 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |
| fork vs staging | 0 差异 |

---

## 22. 第十六轮：去掉「要另配」类措辞（已完成）

**起因**：用户指出三个小字里的「页面版式要另配」「配色字体要另配」**没意义**。

**为什么没意义**：那是从**系统视角**写的"你还要做什么"，而用户想知道的是"我能得到什么"；
而且与前半句**冗余** —— 说清了给什么，缺什么自然就懂了。更糟的是它把选择框成
"不完整、还得再折腾"，而实际上只挑一类也能直接用。

### 22.1 改后（三栏形式统一为「列举给什么」）

| 栏 | 小字 |
|---|---|
| 视觉基调 | 配色、字体、装饰密度 |
| 页面版式 | 母版与版面，决定内容怎么摆 |
| 整套视觉 | 配色、字体、装饰密度 + 母版与版面 |

**顺带修掉一处繁中残留**：proactive_speaker_notes_desc 的 zh-TW 仍是旧文案
（「無需另行要求，**Agent** 也會生成……」），既含「另行」也含内部角色名 Agent —— 简中在
§12 已改，繁中漏了。已对齐为「預設開啟：不用另外交代，AI 也會為每一頁寫好講稿備註。」

**验收**：改 9 + 1 项未命中 0；
ode --check（真实退出码）0；prompt_audit exit 0；
需另 / 另配 残留均为 0。

---

## 23. 第十七轮：从选项列表移除「演示核心 4:3」（已完成）

**要求**：只让该选项从下拉里消失，**用户不感知即可，相关引用一律不动**。

**最小改动**：只删 `templates/layouts/layouts_index.json` 里的 `presentation_core_43` 条目。
UI 的模板下拉由该索引驱动（`confirm_ui/server.py` 的 `_build_template_library` 读它），
因此删条目即可隐藏。**工作区、预览图、`build_template_previews.py` 的计划行、预览 README
的清单行全部保留** —— 仓库里不留悬空引用，日后要恢复只需把条目加回索引。

| | 改前 | 改后 |
|---|---|---|
| 索引里的版式 | editorial_bleed, presentation_core, **presentation_core_43**, report_core | editorial_bleed, presentation_core, report_core |
| 下拉实际显示 | 4 个 | **3 个**（满版编辑 / 演示核心 / 报告核心） |

### 23.1 连带发现：画布与版式之间没有兼容性校验

删掉唯一的 4:3 版式后，现余 3 个版式**全部是 `ppt169`**，而 `ppt43` **仍是可选的画布格式**
（`config.CANVAS_FORMATS` 保留 ppt169 / ppt43 / a4）。查证结果：

| 查证项 | 事实 |
|---|---|
| `canvas_format` 在 `confirm_ui/server.py` 的用途 | **仅**用于把画布列表从 `config.CANVAS_FORMATS` 同步进目录，**不做模板↔画布校验** |
| layout 候选携带的字段 | `id / key / kind / label / label_zh / source / summary / summary_zh / workspace_root` —— **不含 `canvas_format`** |
| 现余 3 个版式的画布 | 全部 `ppt169` |

即：**选「画布格式 = 4:3」再选任一版式，当前没有任何东西会拦住或提示**；
候选数据里连 `canvas_format` 都没有，UI 想提示也拿不到。

移除前，选 4:3 有一个显然匹配的版式；移除后**没有了**。是否一并处理 `ppt43` 画布，
留给用户决定 —— 本轮不动。

---

## 24. 第十八轮：重设计第 3、4 节 + 删除 ppt43 画布（已完成）

### 24.1 删除 ppt43（用户确认方案 A）

`ppt43` 从 11 个文件里移除：

| 文件 | 处置 |
|---|---|
| `scripts/config.py` | 删两处字典条目（CANVAS_FORMATS 与安全区表） |
| `scripts/project_utils.py` | 删字典条目 |
| `scripts/svg_position_calculator.py` | 删字典行；docstring 的格式举例改为 `ppt169, a4` |
| `scripts/generate_examples_index.py` | `format_order` 去掉 ppt43 |
| `scripts/svg_quality/cli.py` | 用法串改为 `<ppt169\|a4\|...>` |
| `scripts/confirm_ui/static/app.js` | `isPptCanvas()` 只认 ppt169 |
| `scripts/confirm_ui/static/catalogs.json` | 删条目 |
| `scripts/docs/project.md` | 格式清单去掉 ppt43 |
| `references/canvas-formats.md` | 删表格行；字号带表三行的 `ppt169 / ppt43` 改为 `ppt169` |
| `references/image-layout-spec.md` | 删 4:3 那句（改写为只提 A4 竖版） |
| `workflows/profiles/beautify-pptx.md` | 画布清单去掉 ppt43 |

字典条目一律**括号匹配**删除，不用行号。改完 11 个文件语法自检全过。
唯一残留是已从索引隐藏的 `templates/layouts/presentation_core_43/`（§23 按要求保留）。

### 24.2 画布说明是死数据（根因）

`enumField()` 每个选项卡片的文案是：

```js
var label = optionLabel(o);          // localized(o, "label")
var desc = optionDesc(o);            // localized(o, "desc")
if (desc) label += (isCjkUi() ? "：" : " — ") + desc;
```

**但只有 `canvas` 条目用的是 `use_zh` / `use_en`**，其他目录（`modes`、`delivery_purpose`）
都用 `desc_*`。`app.js` 里**从未引用任何 `use_*` 字段** —— 所以画布的说明一直是死数据，
用户只看到「PPT 16:9」「A4 1:41」两个光秃秃的标签。这正是"不知道是什么含义"的根因。

改为 `desc_*` 后说明立即显示，并重写文案：

| id | 旧 | 新 |
|---|---|---|
| ppt169 | PPT 16:9 ／ 现代投影 / 在线演示 | **16:9 横屏** ／ 最常用 —— 投影、屏幕演示、线上会议 |
| a4 | A4 1:41 ／ 打印 / 文档导出 | **A4 竖版** ／ 像一张纸 —— 适合打印出来当讲义或文档 |

### 24.3 合并第 3、4 节

**理由**：两者是**因果关系**，不是两件事。版式/成套模板的 SVG 原型按固定画布硬画
（`register_template.py` 会校验每张 SVG 的画布**精确等于**声明的 `canvas_format`），
所以选了模板，画布就已经定了。原设计却先问画布、后问模板，模板还可能把刚才的选择作废，
且没有任何提示（画布与模板之间**不存在兼容性校验**）。

合并为一节 —— **「这份演示长什么样」**：

```
从零设计  →  显示「画布格式」，由用户决定
套用模板  →  显示模板选择面板 + 一行事实：画布：16:9 横屏（由所选的版式或成套模板决定）
```

- `renderCanvas()` → `renderCanvasField()`（去掉 section 外壳，改为这一节里的字段）
- 新增 `selectedTemplateCanvas()`（**版式优先于成套**，与 "Layout overrides Deck structure" 一致）、
  `canvasDisplayLabel()`、`renderTemplateCanvasFact()`、`refreshTemplateCanvasFact()`
- `updateTemplateSelectionControls()` 联动画布字段与事实行的显隐
- 后端：`server.py` 候选新增 `canvas_format`（取自索引元数据；风格没有该字段，正确）

### 24.4 本轮踩的两个坑

1. **编辑之间有顺序依赖导致漏改**：第二步的锚点在前一步已被替换，`renderCanvasField` 里
   残留 `host.appendChild(sec)` —— `sec` 已改名为 `field`，**这是运行时 ReferenceError，
   `node --check` 抓不到**（它只查语法）。同时四个辅助函数没插进去，却已被调用。
2. 因此补了一个**静态自检脚本**：检查改动函数体内的 `t("key")` 是否都在各语言字典里、
   用到的 CSS 类是否存在、有没有残留旧符号、旧 `renderCanvas(` 是否清零。

**验收**

| 检查 | 结果 |
|---|---|
| 11 个 Python/JS/JSON 语法 | 全 exit 0 |
| 静态自检（i18n / CSS / 旧符号） | zh 缺失无 · en 缺失无 · CSS 缺失无 · 残留无 · 旧调用 0 |
| 服务端候选 `canvas_format` | layout/deck 均为 `ppt169`，style 为 `None` |
| 服务端画布目录 | 2 项，均带中文说明 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 25. 第十九轮：改为「画布独立 + 模板按画布过滤」（已完成）

**§24.3 的设计是错的，本轮推翻重做。**

### 25.1 错在哪

§24.3 把画布藏进了模板节：从零设计时才出现，套模板时降级为一行事实。用户指出这是**反的**：

> 应该保留画布比例选项，然后根据用户选择去过滤下面的选项列表。
> 如果选 4:3，下面三个下拉里的内容就只留 4:3 的；选 16:9 就只有 16:9 的。

**正确的模型**：

```
画布 = 你要什么形状（独立的一步，先问）
模板 = 这个形状下有哪些样子（按画布过滤后列出）
```

这样**不可能选出不匹配的组合** —— 而 §24.3 只是把画布变成一个事后被告知的结果。
更根本的是：版式/成套模板的原型按固定画布硬画（`register_template.py` 校验每张 SVG 的
画布必须精确等于声明的 `canvas_format`），**是画布约束模板，不是模板决定画布**。
§24.3 把因果装反了。

### 25.2 现在的实现

| 节 | 内容 |
|---|---|
| **3 画布比例** | 独立一节，在模板之前。说明：「页面是横的还是竖的。它会决定下面能选哪些模板。」 |
| **4 整体视觉** | 从零设计 / 套用模板；三个下拉的内容**按画布过滤** |

- `renderCanvas()` 恢复为独立一节（`sec_canvas` 改名「画布比例」）
- 新增 `templateCandidatesFor(kind)`：**版式与成套**按 `canvas_format` 精确匹配过滤；
  **风格不含页面原型、与页面形状无关，始终可选**
- 新增 `pruneTemplateSelections()`：换画布后，原先选中的模板若已不在列表里就清空选择
  （否则提交会带着无效选择）
- 面板加一行说明列表为什么只有这些：**「页面版式」和「整套视觉」只列出适配「16:9 横屏」的；
  「视觉基调」与页面形状无关，任何画布都能用。** 三个标签名走 `{layout}` / `{deck}` /
  `{style}` / `{canvas}` 占位符替换，不写死在文案里
- 某个 kind 过滤后为空时，下拉下方提示「没有适配这个画布的模板」
- 删掉 §24.3 引入的 `renderCanvasField` / `selectedTemplateCanvas` /
  `renderTemplateCanvasFact` / `refreshTemplateCanvasFact` 与三个 `template_canvas_fact_*` 键

### 25.3 顺带修掉一个自己造的 bug

上一轮用 `addkey` 插新键时，**把已存在的 `sec_template_choice` / `template_choice_hint`
也当成新键插了一份** —— 字典里出现重复键。JS 对象字面量**后者生效**，所以界面显示的
并不是想要的那个值。本轮写了一个去重脚本检查四个语言块，重复键与死键均已清零。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| 静态自检 | 函数齐全 · zh/en 无缺失键 · 无残留旧符号 |
| 四个语言块重复键 | 全为「无」 |
| `template_canvas_fact_*` 死键 | 0 |
| 服务端文案 | 画布比例 / 3 条说明全部就位 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 26. 第二十轮：恢复 ppt43 画布与「演示核心 4:3」（已完成）

**§23、§24.1 的删除被撤销。**

用户看到画布里没有 4:3 后询问，确认要**两样都恢复**。回顾：§23 只把 `presentation_core_43`
从索引里摘掉（工作区按要求保留）；§24.1 按用户选的方案 A 把 `ppt43` 画布从 11 个文件删除。
本轮全部恢复。

### 26.1 恢复内容

原始内容取自 pristine 的 `skills/ppt-master/`，按 fork 的缩进与字段风格改写
（fork 此前把画布集收窄为 ppt169 / ppt43 / a4，因此**不是**照抄 pristine 的完整列表）。

| 文件 | 恢复内容 |
|---|---|
| `scripts/config.py` | `CANVAS_FORMATS` 与 `LAYOUT_MARGINS` 两条目；docstring 补 ppt43 |
| `scripts/project_utils.py` | 字典条目 |
| `scripts/svg_position_calculator.py` | 字典行；docstring 补 ppt43 |
| `scripts/generate_examples_index.py` | `format_order` 加回 ppt43 |
| `scripts/svg_quality/cli.py` | 用法串补 ppt43 |
| `scripts/confirm_ui/static/app.js` | `isPptCanvas()` 认回 ppt43 |
| `scripts/confirm_ui/static/catalogs.json` | 加回条目（**用新的 `desc_*` 写法**，文案与另两个画布同一风格） |
| `scripts/docs/project.md` | 格式清单补 ppt43 |
| `references/canvas-formats.md` | 画布表行 + 字号带表三行 |
| `references/image-layout-spec.md` | 恢复 4:3 那句 |
| `workflows/profiles/beautify-pptx.md` | 画布清单补 ppt43 |

**版式索引不手写条目**，改用 `register_template.py --rebuild-all --kind layout` 重建 ——
从 spec 重新推导，避免手写出错。结果 4 个版式，`presentation_core_43` 的
`canvas_format` 正确读回 `ppt43`。

预览图 `layout_presentation_core_43.png` 从未删除（§23 只动索引），无需重做。

### 26.2 过滤后的实际可用量

| 画布 | 视觉基调 | 页面版式 | 整套视觉 |
|---|---|---|---|
| 16:9 横屏 | 7 | 3 | 2 |
| **4:3 方屏** | 7 | **1** | 0 |
| A4 竖版 | 7 | 0 | 0 |

「视觉基调」不受画布约束（无页面原型），三个画布下都是 7 个。
4:3 与 A4 下「整套视觉」为空是**事实**（两个成套模板都是 16:9），界面上会提示
「没有适配这个画布的模板」。

**验收**

| 检查 | 结果 |
|---|---|
| 7 个 Python/JS/JSON 语法 | 全 exit 0 |
| 版式索引重建 | 4 个，`presentation_core_43` canvas=`ppt43` |
| 画布目录 | 3 项，均带中文说明 |
| 过滤统计 | 与上表一致 |
| 预览图 | 6 张俱在 |

---

## 27. 第二十一轮：六类快捷方案（已完成）

### 27.1 起因与取舍

用户指出三个模板槽位"各自负责的视觉效果太混乱、逻辑不清晰"，并给出两个方案：

1. **列举** —— 把所有搭配做成完全排列
2. **重构** —— 把每类彻底解耦成独立维度（配色 / 排版 / 装饰密度）

**两个都不成立，理由如下**（记录以免重走）：

- **列举**：7 风格 × 4 版式 × 2 成套 = 56 个完整组合，加子集共 **119** 条；每加一个模板条目乘性增长。更要紧的是**枚举会摧毁可组合性** —— 13 个模板能拼出上百种组合正是因为它们是积木。
- **重构**：三个 kind 是**上游定义的包**（`create-template.md` 的 Style/Layout/Deck 各有 spec 契约与 `register_template.py` 校验）。而且**数据本身不正交**：具体配色数值与字体**只有成套模板给**，论证方法**只有风格模板给**。要拆成正交轴等于重写整个模板系统。

用户随后追问：**"用户都看不懂这些选项 都不知道如何组合 可组合性还有意义吗"** —— 这一问是对的。
可组合性的价值以"用户能组合"为前提；对一个看不懂三栏的人，它是零。
**因此不再拿可组合性当保留复杂入口的理由。**

### 27.2 落地方案

**「整体视觉」的默认入口改为一张预设列表** —— 每条预设是一个用户认识的**结果名**，
而不是三个需要自己组合的**零件名**。三栏收进「自定义组合」，默认不展开。

| 预设 | 组合（怎么讲 / 页面版式 / 配色与字体） |
|---|---|
| **论文答辩** | 学术研究 + 报告核心 + 工程蓝 |
| **组会速览** | 技术深潜 + 演示核心 + 工程蓝 |
| **课堂讲解** | 科学解释 + 演示核心 + 信号红 |
| **动手培训** | 工作坊教学 + 演示核心 + 信号红 |
| **事故复盘** | 事故复盘 + 报告核心 + 信号红 |
| **老投影仪** | 学术研究 + 演示核心 4:3 +（无成套） |

**接口未动**：预设只是指向现有 13 个模板的指针，落在 `catalogs.json` 的
`template_presets`，不需要改后端、schema 或工作区契约。

**实现要点**

| 位置 | 内容 |
|---|---|
| `catalogs.json` | 新增 `template_presets`（四语言 label / desc + style / layout / deck 三个 id） |
| `app.js` | `presetList` / `presetSelectionKeys` / `presetAvailable` / `activePresetId` / `presetById` / `chooseTemplatePreset` / `chooseCustomCombination` / `renderTemplatePresetChoice` / `renderPresetAppliedSummary` / `refreshPresetAppliedSummary` |
| `app.js` | `renderTemplateSelection` 改为「预设列表 + 自定义组合 + 从零设计」 |
| `app.js` | `updateTemplateSelectionControls` 增加预设选中态；**三个下拉只在自定义组合下展开** |
| CSS | `.template-preset-applied` / `.tpa-label` / `.tpa-value` |

**选中态是推导出来的**，不是存下来的：`activePresetId()` 比较当前选择是否**恰好等于**
某条预设。因此从预设微调后会自动落到「自定义组合」，不需要额外状态。

**预设选中时显示一行摘要**「已套用：学术研究 · 报告核心 · 工程蓝」——
用户看到一个结果名之后仍需知道它由什么组成，否则改不动。

### 27.3 本轮抓到的一个真问题

初版「老投影仪」引用了 `engineering_blue`（**16:9**）。而预设的可用性要求
**引用的模板全部适配当前画布**，所以在 4:3 下这条预设**整条消失**。

**根因**：4:3 下没有任何成套模板可用（两个成套都是 16:9）。
**修法**：这条预设**不带成套** —— 4:3 没有可配的成套，描述也相应改为「卡片式版面」。

**由此得出一条约束**：**预设引用的模板必须共享同一画布。**已验证 6 条全部满足。

### 27.4 各画布下的实际结果

| 画布 | 出现的预设 | 怎么讲 / 页面版式 / 配色与字体 |
|---|---|---|
| 16:9 横屏 | 论文答辩 / 组会速览 / 课堂讲解 / 动手培训 / 事故复盘 | 7 / 3 / 2 |
| 4:3 方屏 | 老投影仪 | 7 / 1 / 0 |
| A4 竖版 | （无） | 7 / 0 / 0 |

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0（中途一次失败：英文串里的直双引号截断字符串，已修） |
| 6 条预设引用完整性 | **0 缺失** |
| 6 条预设画布一致性 | **0 不一致** |
| 各画布可用预设 | 与上表一致 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 28. 第二十二轮：预设移入「套用模板」选项卡，三个下拉移除（已完成）

**要求**（用户）：保留之前两个大选项卡（分别对应模板与 AI 设计），把 6 条预设放进模板那个
选项卡里，**直接取代原来的三个下拉搭配**。

### 28.1 最终结构

```
4  整体视觉
   先决定样子从哪来：套一套现成的方案，还是让 AI 根据这份材料现做。

   ○ 从零设计
     不套用现成模板，整套视觉与版面由 AI 根据这份材料现做。
   ● 套用模板
     从模板库里挑一套现成的方案，样子已经配好
        ↓ 展开
        ○ 论文答辩  [版式样张]  报告式版面 + 深蓝配色。结论先行，局限单独成页
        ○ 组会速览  [版式样张]  卡片式版面 + 深蓝配色。一页一事，便于快速读完
        ○ 课堂讲解  [版式样张]  卡片式版面 + 红色配色。概念拆解，分步推进
        ○ 动手培训  [版式样张]  卡片式版面 + 红色配色。示范与练习交替
        ○ 事故复盘  [版式样张]  报告式版面 + 红色配色。时间线还原，对事不对人
        ○ 老投影仪  [版式样张]  4:3 方屏 + 卡片式版面。教室和会议室的旧设备专用
        指定模板
        本次没有另外指定模板
```

### 28.2 移除与新增

**移除**：`renderTemplateSelectField` / `templateOptionTitle` / `templatePreviewUrl` /
`chooseTemplateForSlot` / `chooseCustomCombination`，以及「自定义组合」入口和
「已套用：……」摘要行。删后逐一验证 **0 处残留引用**。

**新增**：`presetPreviewUrl()` —— 预设卡片带一张样张。
**预览图取该预设所用版式的样张**：页面结构由版式决定，样张看的就是结构；配色由成套模板定，
已在描述里写明（如「深蓝配色」）。这是**近似而非精确** —— 样张用的是版式自带的配色。

### 28.3 顺带清理

用**可靠判据**找死 i18n 键：*键只在字典区出现、代码区一次都不出现*。
（先前用「是否被 `t()` 调用」判断不可靠 —— `section("sec_canvas")` 是把键当字符串传递，
不走 `t()`。）动态拼接前缀 `template_kind_` / `role_` / `font_` / `size_role_` 已排除。

删掉 **12 个死键**（zh / zh-TW / en 各 12，ja 7）：
本轮产生的 7 个（`template_custom_title` / `template_custom_desc` /
`template_applied_prefix` / `template_library_hint` / `template_select_none` /
`template_slot_empty_canvas` / `template_canvas_filter_note`），
以及旧模板 UI 遗留的 5 个（`sec_template_library` / `sec_template_explicit` /
`template_source_library` / `template_source_path` / `template_none_registered`）。

**仍剩 4 个**（`sample_heading_cjk` / `sample_body_cjk` / `no_icons` /
`preview_section_title`）—— 属于其他域，可能是有意留给预览功能的，未动，仅记录。

CSS 同步清理：删掉 `.template-select-gives` / `.template-select-empty` /
`.template-canvas-filter` / `.template-preset-applied` / `.tpa-label` / `.tpa-value` /
`.template-select-grid`；`.template-select-field` 与 `.template-select-label` **保留** ——
「指定模板」那一栏仍在使用。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| 被删函数的残留引用 | 全部 **0** |
| 结构确认 | 两个大选项卡在 · 自定义组合已移除 · 三个下拉已移除 · 预设列表与样张在 · 指定模板在 |
| 死键 | 12 删 / 4 留（已记录） |
| 各画布可用预设 | 16:9 五条 · 4:3 一条 · A4 无（提示用自由设计） |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 29. 第二十三轮：修两个自己造成的 bug（已完成）

### 29.1 Bug A —— 点「从零设计」后「套用模板」仍高亮

§28 改写 `updateTemplateSelectionControls()` 时，我用一个缩写版替换了原来的 `useChoice` 分支，
**把 `classList.toggle("selected", ...)` 与 `aria-pressed` 一起删掉了**：

```js
if (useChoice) {
    useChoice.setAttribute("aria-expanded", templatesSelected ? "true" : "false");
    // ← selected 的切换没了，所以卡片永远保持高亮
}
```

而 `renderTemplateModeChoice()` 只在**渲染时**决定初始 `selected`，
后续状态完全由 `updateTemplateSelectionControls()` 负责 —— 于是高亮再也不会消失。

**修法**：恢复 `classList.toggle("selected", templatesSelected)` 与 `aria-pressed`。

### 29.2 Bug B —— 预设卡片只有图片，没有文字

`renderTemplatePresetChoice()` 里 `copy` 节点被构造、标题与描述都挂进去了，
**但 `choice.appendChild(copy)` 这一行不存在** —— §28 重写该函数加缩略图时丢掉的。

于是卡片里只有 `radio + thumb`，文字**存在于内存却从未进入 DOM**。
`node --check` 查不出这类错误，表现是"东西莫名不见了"。

**修法**：补回 `choice.appendChild(copy)`。

**并加了一条启发式自检**（已并入 `check-i18n-keys-v2.py` 的同类检查）：
函数内 `var X = el(...)` 构造出的节点，必须在同一函数里被
`appendChild` / `insertBefore` / `append` / `prepend` 引到某处，或被 `return`。
扫描全文件后确认**没有第二处**同类问题。

### 29.3 顺带：不可用的预设改为灰显

用户反馈「只有 5 个选项」—— 因为「老投影仪」需要 4:3 画布，被过滤掉了，
而**消失**让用户不知道它存在。

改为**灰显 + 说明缺什么**：
- 新增 `presetRequiredCanvas()`，从**未过滤**的库里查该预设所需画布
  （过滤后就查不到了，这是必须用未过滤库的原因）
- 新增 i18n 键 `template_preset_needs_canvas`（四语言），显示「需要「4:3 方屏」画布」
- 灰显卡片 `disabled` 且不绑定点击
- CSS `.template-preset-choice.unavailable` / `.template-choice-need`

**残留的已知限制**：「组会速览」「课堂讲解」「动手培训」都基于 `presentation_core`，
所以三张样张相同。文字补回后由描述区分（「深蓝配色」vs「红色配色」），
但样张仍是版式自带的配色，**与预设实际配色不完全一致** —— 这是 §28 已声明的近似。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| 孤儿节点全文件扫描 | **无** |
| 服务端代码确认 | `choice.appendChild(copy)` 在 · 灰显分支在 · 需要画布提示在 · 渲染全部预设 |
| 静态自检 | 函数齐全 · zh/en 无缺失键 · CSS 无缺失类 |
| `prompt_audit` | exit 0 |

---

## 30. 第二十四轮：预设卡片去掉预览图（已完成）

**用户判定**：样张**不能正确展示**六条预设 —— 「要么不给预览图，要么重新生成符合描述的预览图」。

**判定成立。** §28/§29 用的是**该预设所用版式的样张**，而版式样张用的是**版式自带的配色**，
预设的实际配色却来自成套模板。「论文答辩」实际是工程蓝的深蓝，样张却是中性色 ——
**图与描述不符，就是误导**。更糟的是三条共用 `presentation_core` 的预设样张完全相同。

### 30.1 为什么没有选"重新生成"

查了 `template_preview_pptx.py`：它只能导出**一个工作区自带的 SVG 原型**，
而预设是**组合**（版式的结构 + 成套的配色），不存在这样的工作区。准确预览只有两条路：

| 路 | 代价 |
|---|---|
| 机械地把版式原型按成套配色重新上色 | **结果无法验证** —— 很可能比现状更误导 |
| 每个预设真跑一遍生成（Strategist + Executor） | **每次是一次完整 LLM 生成**；ESG 那次约 ¥19.90，6 次约 ¥120，只为做预览图 |

**两条都不划算**，因此采用用户给的第一个选项。

### 30.2 改动

- `renderTemplatePresetChoice()` 去掉缩略图分支
- 删 `presetPreviewUrl()`
- 删 CSS `.template-preset-thumb` / `.template-preset-img` / `.template-preset-thumb[hidden]`

**保留**：`scripts/confirm_ui/static/template_previews/*.png`（6 张）与
`build_template_previews.py`、同目录 README。**它们已不被 UI 引用**，但保留的理由是：
README 记录了完整的再生成流程，日后若要做真预览可直接复用这套管线。**这是一处已知的
"有文档、无引用"资产**，记录在此以免日后被误认为遗漏。

### 30.3 现在的预设卡片

**纯文字**：标题 + 描述（+ 画布不匹配时的灰显说明）。

```
○ 论文答辩    报告式版面 + 深蓝配色。结论先行，局限单独成页
○ 组会速览    卡片式版面 + 深蓝配色。一页一事，便于快速读完
○ 课堂讲解    卡片式版面 + 红色配色。概念拆解，分步推进
○ 动手培训    卡片式版面 + 红色配色。示范与练习交替
○ 事故复盘    报告式版面 + 红色配色。时间线还原，对事不对人
○ 老投影仪    4:3 方屏 + 卡片式版面。教室和会议室的旧设备专用
```

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| `presetPreviewUrl` / `template-preset-thumb` / `template-preset-img` 残留 | 全部 **0** |
| 服务端代码确认 | 卡片内无 `img` · `appendChild(copy)` 在 · 灰显分支在 |
| 静态自检 | zh/en 无缺失键 · CSS 无缺失类 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 31. 第二十五轮：预设列表改为紧凑从属样式（已完成）

**用户反馈**：预设用与两个大选项卡相同尺寸的整宽卡片，**读起来像第三个并列选项**，
而它是挂在「套用模板」下面的。

**改法**（纯 CSS，不动结构）：

| 项 | 改前 | 改后 |
|---|---|---|
| 列表缩进 | 无 | `margin-left: 44px` —— 对齐到「套用模板」的文字 |
| 从属标识 | 无 | `border-left: 2px solid var(--line)` 一条竖线 |
| 行距 | `gap: 8px` | `gap: 1px` |
| 卡片内边距 | `11px 13px` | `6px 10px` |
| 卡片边框 | 常驻 `1px solid var(--line)` | 平时透明，悬停/选中才出现 |
| 标题与描述 | 两行（纵向 flex） | **同一行**（`flex-direction: row` + `wrap`） |
| 单选项圆点 | 17px | 14px |
| 面板顶部 | `border-top` + `padding-top: 14px` | **去掉** —— 它会强化"独立区块"的观感 |

六条预设的纵向占用因此大幅压缩，且视觉上明确从属于「套用模板」。

**顺带修一处文案**：`template_none_explicit`（「指定模板」空态）原写
「本次没有另外指定模板 —— **用上面的模板库就行**」，但三个下拉与"模板库"入口
已在 §28 移除。改为「从上面挑一条方案即可」（四语言）。

**验收**：服务端 CSS 四项规则确认就位（列表缩进/竖线、卡片紧凑、标题行内、面板无横线）。

---

## 32. 第二十六轮：「从零设计」改名「AI 生成」（已完成）

**改动 12 项 + 1 处连带**：

| 键 | 改后 |
|---|---|
| `template_free_title` | **AI 生成**（zh / zh-TW / ja）· `AI-generated`（en） |
| `template_free_desc` | 不套用现成模板，**每一页由 AI 根据这份材料现画**。（原句"由 AI 现做"与标题重复） |
| `template_preset_none` | 这个画布暂时没有配套方案，用**「AI 生成」**即可 ← 引用了旧名，必须连带改 |
| `template_selection_required` | 请先选**「AI 生成」**或「套用模板」；选了「套用模板」后**至少挑一条方案**。（顺带把"至少挑一个模板"改为"一条方案" —— 现在挑的是预设） |

**全仓复查**：`app.js` 内「从零设计 / 從零設計」残留 **0**。
`FORK.md` 内 7 处为历史记录，保留。

### 32.1 本轮第四次踩同一个坑

英文串里写 `Choose "AI-generated" or "Use a template" first; ...` ——
**值内的直双引号截断了 JS 字符串**，`node --check` 报 `SyntaxError: Unexpected identifier 'AI'`。

**这个坑本轮已是第四次**（§21、§27 各一次，§29 附近一次）。`node --check` **每次都抓到了**，
说明工序有效；问题在于我写串时手快。

**对策（本次落实）**：加了一道常驻扫描 —— 逐语言块检查
`key: "value",` 形式的值里是否含**未转义**的双引号。本次扫描四个语言块 **0 可疑行**。
英文串此后一律不用直双引号，改用无引号表述。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| 未转义双引号扫描 | 四语言块 **0 行** |
| 「从零设计」残留（app.js） | **0** |
| 服务端文案 | 四个键全部为新文案 |
| `prompt_audit` | exit 0 |

---

## 33. 第二十七轮：修悬停覆盖选中态（已完成）

**用户反馈**：预设已选中（蓝底），鼠标悬停上去**蓝底消失，只剩边框高亮**。

### 33.1 成因：优先级相同时后写的赢

```css
.template-preset-choice:hover  { background: var(--card); }          /* 0,2,0 */
.template-mode-choice.selected { background: var(--accent-soft); }   /* 0,2,0 */
```

两者选择器优先级**相同**（都是两个类），而 `:hover` 规则在文件中更靠后 ——
**悬停时白色底盖掉了选中的蓝底**。

两张大卡片的 `:hover` 只改边框、不改底色，所以没有这个问题；
**是我 §31 给预设加 `background` 时引入的**。

### 33.2 修法

```css
.template-preset-choice:not(.selected):hover { … }   /* 悬停样式排除已选中项 */
.template-preset-choice.selected:hover        { border-color: var(--accent); }
```

### 33.3 顺带全表排查

扫描全表 `:hover` 规则里设了 `background` 的，共 4 条：

| 选择器 | 是否有选中态 |
|---|---|
| `.lang-select-btn:hover` | 无（只有基础态与 hover） |
| `.direction-reset-button:hover` | 无（只有基础态、hover、focus-visible） |
| `#btn-confirm:hover` | 无（ID 选择器，优先级最高） |
| `.template-preset-choice:hover` | **有 → 本次修掉** |

**结论：只有预设这一处有该问题。**

**规律（记下来）**：给一个带 `.selected` 状态的组件加悬停背景时，
必须写成 `:not(.selected):hover`，否则同优先级下后写的 hover 会盖掉选中态。

**验收**：服务端 CSS 确认两条新规则就位；`prompt_audit` exit 0。

---

## 34. 第二十八轮：预设描述去掉「版面 + 配色」前缀（已完成）

**要求**：去掉每条预设描述里 `xxx版面 + xx配色` 的前半段，只留后半段。

| 预设 | 改前 | 改后 |
|---|---|---|
| 论文答辩 | ~~报告式版面 + 深蓝配色。~~结论先行，局限单独成页 | 结论先行，局限单独成页 |
| 组会速览 | ~~卡片式版面 + 深蓝配色。~~一页一事，便于快速读完 | 一页一事，便于快速读完 |
| 课堂讲解 | ~~卡片式版面 + 红色配色。~~概念拆解，分步推进 | 概念拆解，分步推进 |
| 动手培训 | ~~卡片式版面 + 红色配色。~~示范与练习交替 | 示范与练习交替 |
| 事故复盘 | ~~报告式版面 + 红色配色。~~时间线还原，对事不对人 | 时间线还原，对事不对人 |
| 老投影仪 | ~~4:3 方屏 + 卡片式版面。~~教室和会议室的旧设备专用 | 教室和会议室的旧设备专用 |

四语言同步改（zh / zh-TW / en / ja）。**直接写新值而非按标点切割** —— 避免中英标点差异切错。

### 34.1 由此产生的空缺（需决策）

图片已在 §30 移除，**「版面 + 配色」是预设卡片上最后一条视觉信息**。
去掉后，六条预设**只剩使用场景描述，没有任何视觉描述**。
使用者因此无法从卡片判断"这套长什么样"。

**这不是本轮引入的错误，而是一个待补的空缺。** 可选补法（尚未实施）：

1. 在标题旁挂两个小标签：`报告式版面` / `深蓝配色` —— 信息保留，但不占描述正文
2. 恢复按预设真渲染的样张（代价见 §30）
3. 维持现状，视觉信息交由 Stage 2 的「视觉方向」「色彩方案」呈现

**验收**：`/api/catalogs` 返回六条新描述；`catalogs.json` JSON 合法；`prompt_audit` exit 0。
（残留检查命中的 `layout,` 一处属 `visual_styles` 目录中 `swiss-minimal` 自身的描述，与预设无关。）

---

## 35. 第二十九轮：查证「版面 + 配色」是否有机械保证，并恢复描述（已完成）

**用户的判据（正确的判据）**：

> 你要验证也不是靠那几次的结果，而是去看代码啊，看看代码是如何保证生效的。
> 如果真有保证，那就可以留。

**§34 去掉的描述在本轮恢复。** 以下是从代码查到的强制点，不依赖运行结果。

### 35.1 结构（「xxx 版面」）—— 硬保证

| 环节 | 谁做 | 强制方式 |
|---|---|---|
| 版式原型 SVG 装入项目 | `apply_template.py`（机械） | ESG 项目里实存 `01_cover.svg … 13_closing.svg` 共 13 张 |
| 每页必须映射到一个原型 | `project_management/project_specs.py` | `if structure.get("mode") == "structured"` 时，`page_layouts` / `page_pptx_layouts` 的键集合必须**完全等于** `page_rhythm` 的键集；缺失或多余都是 **schema 错误** |
| 原型的 Master/Layout 与 lock 一致 | `svg_to_pptx/pptx_package/template_structure.py` | `Return mismatches between parsed SVG layouts and the project lock` —— **反向比对器** |
| 只选风格时不得有版面映射 | 同上 | `spec_lock.md template_reuse_scope: style must omit page_layouts` |
| 取值受限 | 同上 | `template_reuse_scope must be one of: …`；`page_layouts key must be P<NN>`；`Layout prototype source must be …` |

### 35.2 配色（「xx 配色」）—— 强保证，含一处 LLM 环节

`svg_quality/checker.py` L6714-6731：

```python
lock = self._get_spec_lock(svg_path)
allowed_colors = set()
for v in lock.get('colors', {}).values():
    allowed_colors.add(color)
...
if val not in allowed_colors:                                    # 用了 lock 之外的颜色 → 报错
elif val in prototype_colors and val not in locked_colors:        # 原型色不在 lock 里 → 报错
```

**页面颜色必须落在 `spec_lock` 的 `colors` 里 —— 这是机械强制，配色无法漂移。**

链路：`成套 spec（机械装入）→ Strategist 抄调色板进 lock → checker 强制页面只用 lock 内的颜色`。
**唯一非机械的环节是「Strategist 抄对来源」**；它读的是被机械装进项目的
`design_spec.deck.<id>.md`（含 Color Scheme 章），并被要求原样重复。

### 35.3 结论与处置

| 宣称 | 保证强度 |
|---|---|
| 「xxx 版面」 | **硬保证** |
| 「xx 配色」 | **强保证**（调色板不可漂移；一处 LLM 抄写环节） |

**因此恢复 §34 去掉的前半段**（六条预设，四语言）。`catalogs.json` JSON 合法，
`/api/catalogs` 返回恢复后的文案，`prompt_audit` exit 0。

**方法教训（记下来）**：验证"某特征会不会生效"，**要看代码里的强制点**，
不能只看几次运行结果 —— 运行结果只能说明"这次碰巧对"，说明不了"有保证"。

---

## 36. 第三十轮：第一阶段「沟通契约」四个字段的解释改写（已完成）

### 36.1 用户提出一个关键疑问

> 期望的受众变化/成功条件 —— 上一个字段问了目的是什么，那很显然成功条件不应该就是
> 达成目的吗？我不明白为什么这里又问一遍。

**查了规范，两者确实不是重复提问。** `references/plan-core.md` 分开定义：

| 字段 | 规范原文 |
|---|---|
| `communication_intent` | **What must the presentation accomplish?** It may combine several purposes and state priority or sequence. |
| `audience_outcome` | **What observable change means the communication succeeded** — what will the audience know, understand, believe, decide, or do? |

**官方示例（`confirm-surface.md`）把差别说得很清楚**：

```
communication_intent: 先汇报进展并暴露交付风险，再推动管理层决定下一阶段投入   ← 你要做什么
audience_outcome:     管理层能比较三个选项、接受风险判断，并选定一条获得预算的路径 ← 他们到什么状态才算成功
```

**即：前者是"你的动作"，后者是"可观察的成功标准"。** 目的是"推动决定"，但"什么叫推动了"
（点头 / 能比较三个选项 / 当场批预算）导向的内容完全不同 —— 所以必须单独问。

规范另有两条佐证其独立用途：
- `strategist.md`：把完整契约留在 §I，只把 `audience` 与 **`objective`（一句执行句，保留 intent 与 audience_outcome 两者）** 投影给下游
- `modes/_index.md`：读 `communication_intent`、`audience_outcome`、`core_message` 等**一起**判断论证模式

**结论：字段该留，但旧标签「期望的受众变化 / 成功条件」太抽象，没把这层关系说出来。** 本轮改写。

### 36.2 改动（四语言各 8 项）

| 键 | 改前 | 改后 |
|---|---|---|
| `sec_communication`（节标题） | 这份演示要完成什么 | **这次演讲** |
| `sec_audience` | 目标受众 | **听众是谁？** |
| `placeholder_audience` | 这份演示文稿面向谁？ | 例如：本院系答辩委员会，其中两位不是本方向 |
| `communication_intent` | 这份演示文稿需要完成什么？ | **这次演讲的目的是什么？** |
| `communication_intent_hint` | 「告知、解释、说服…」一串名词 | **逐条扩成完整短句**（9 条，见下） |
| `audience_outcome` | 期望的受众变化 / 成功条件 | **怎么算讲成功了？** |
| `placeholder_audience_outcome` | 结束后，受众应该知道… | ……**这是检验上面那个目的有没有达到的标准** |
| `core_message` | 核心信息 / 决策请求 / 行动 | **想传达的核心主旨是什么？** |

目的清单（原为一串名词，现每条给出"做什么"）：

```
告知 —— 让大家知道某件事
解释 —— 让人弄懂一个机制或原因
说服 —— 让人接受一个判断
决策 —— 推动一个具体决定
对齐 —— 让各方对同一套事实或口径达成一致
教学 —— 教会一项方法或操作
汇报与问责 —— 交代进展并说明责任
动员 —— 让人愿意投入行动
留档与交接 —— 留下可查阅、可接手的记录
```

### 36.3 顺带

提示文本原来挤在一行（9 条读不动）。`labeledTextarea` 的提示由 `.toggle-desc` 渲染，
是纯文本、不保留换行。新增 `.subfield-hint-block { white-space: pre-line }` 并让该提示使用它
（`pre-line` 只保留换行、仍折叠空格，对既有单行提示无影响）。

**验收**：四语言各改 8 项且未命中 0；`node --check` exit 0；静态自检通过；
服务端文案确认；`prompt_audit` exit 0。

---

## 37. 第三十一轮：目的一栏压缩为一行 + 占位示例改学术场景（已完成）

### 37.1 目的一栏：9 条清单压成一行

§36 把「告知、解释、说服…」扩成了 9 行完整短句，用户反馈**太长、堆在一起**，要求
**挑两个常用的、一行举例完**。

| | 内容 |
|---|---|
| §36 | 可组合多个，也可说明主次或先后。常见的有：\n 告知 ——…（9 行） |
| **现在** | **可组合多个。例如：汇报研究结果并说明责任，或说服评委接受一个判断。** |

四语言同步。提示里不再有换行转义（复查 0 处）。

### 37.2 占位示例：企业管理场景 → 学术场景

原占位示例是企业管理语境，与本分支的科研定位不符（同 §8–§12 的品牌清理理由）：

| 键 | 改前 | 改后 |
|---|---|---|
| `placeholder_communication_intent` | 例如：先汇报进展并暴露风险，再推动**管理层**决定下一阶段**投入**。 | 例如：先讲清研究设计与结果，再回应评委可能提出的质疑。 |
| `placeholder_delivery_context` | 例如：主要为有主讲的 20 分钟**管理层现场评审**；次要为会后独立阅读的**审批材料**。 | 例如：主要为 15 分钟答辩现场讲解；次要为评委会后翻阅的书面材料。 |
| `placeholder_artifact_afterlife` | 例如：**审批**、评审、**审计**、留档、交接或复用 | 例如：评审、留档、交接或复用 |

**zh 字典复查**：管理层 / 预算 / 审批 / 季度审计 / 公司 / 客户 / 股东 / 交付风险 —— **全部为 0**。

（§36 新增的 `.subfield-hint-block { white-space: pre-line }` 保留：它使所有提示对换行安全，
且当前已无提示使用换行，属于通用能力而非专用代码。）

**验收**：四语言各改 8 项；`node --check` exit 0；静态自检通过；三项守卫全部 exit 0。

---

## 38. 第三十二轮：多行输入框统一为一行高（已完成）

**要求**：所有输入框默认高度一致，都是**一行那么高**。

### 38.1 现状

高度由调用点传的 `rows` 决定，高低不一：

| 字段 | rows |
|---|---|
| `communication_intent` | 3 |
| `audience_outcome` / `core_message` / `delivery_context` / `artifact_afterlife` / `sub_divergence` | 2 |

### 38.2 改法

| 位置 | 改动 |
|---|---|
| `textareaField()` | `input.rows = rows \|\| 2` → **`input.rows = 1`**；删掉 `rows` 形参 |
| `labeledTextarea()` | 删掉 `rows` 形参并停止透传 |
| 6 个调用点 | 删掉尾参 |
| 新增 `autoGrowTextarea()` | 输入时把 `height` 设为 `scrollHeight`；挂载后再量一次，兼顾回填的多行初值 |
| CSS | `textarea.text-input` 加 `overflow-y: auto` |

**为什么加自动增高**：一行高的框里打字只看得到一行，需要手动拖拽才能看全。
自动增高让"默认一行"真正可用，同时保留 `resize: vertical` 供手动调整。

`box-sizing: border-box` 是全局设置，因此 `height = scrollHeight` 的量法正确
（scrollHeight 含 padding，border-box 下正好对应元素高度）。

**验收**

| 检查 | 结果 |
|---|---|
| `node --check` | exit 0 |
| `rows \|\| 2` / 旧签名 / 旧透传 残留 | 全部 **0** |
| 6 个调用点 | 均仍存在且已去掉尾参 |
| 服务端确认 | `input.rows = 1` 在 · `autoGrowTextarea` 在 · 签名已改 · CSS 已改 |
| `prompt_audit` / `attribution_guard` / `hyperlink_contract` | 全部 exit 0 |

---

## 39. 第三十三轮：「传递场景」简化（已完成）

### 39.1 先查清它实际起什么作用

| 环节 | 保障方式 |
|---|---|
| Stage 1 存储 | 代码：`server.py` 的 `_CONTRACT_VALUE_KEYS` |
| 写进 `design_spec.md §I` | 事实确认：ESG 产物里有「交付情境」一行（**中文名**，按英文键名搜不到） |
| 被 Strategist 读来推导阅读模式 | 仅由 `plan-core.md` 的文字规定 —— **`strategist.md` 里不含 `delivery_context`**，**无代码校验** |
| 推导出的 `consumption_mode` | 进 `spec_lock`（`spec_lock.schema.json` 里有该键） |
| 改变页面与备注 | `executor-base.md` Step 2 与 `executor-notes.md` §3 的对照表 |

**对产物的具体影响**（写死在 Executor 的对照表里）：

| 模式 | 页面承载 | 备注承载 |
|---|---|---|
| `text` | 完整句子、明确标注、表格 —— 页面自己能读 | 解读与衔接 |
| `balanced` | 主张 + 证据 | 补充解读与过渡 |
| `presentation` | 一个主张 + 一个大视觉，文字精简 | 讲者刻意省略的推理与上下文 |

即：**它决定页面是"自己读得懂"还是"靠你讲"，以及备注该写什么。**

### 39.2 改动（四语言各 3 项）

| 键 | 改前 | 改后 |
|---|---|---|
| `delivery_context` | 传递场景（明确主要模式） | **这场演讲怎么进行？** |
| `delivery_context_hint` | 区分演讲者主导、读者主导、混合、**录制/自动播放**；混合场景要说明哪一种主导，以及还要兼顾什么次要用途。 | **你现场讲，还是听众自己读？会后还要留给他们翻阅吗？** |
| `placeholder_delivery_context` | 例如：主要为 15 分钟答辩现场讲解；次要为评委会后翻阅的书面材料。 | 例如：15 分钟现场答辩，会后材料留给评委复核。 |

**「录制/自动播放」去掉**：本分支已移除音频/动画/视频交付，该情形无对应能力，留着会误导。
四语言复查残留 **0**。

**验收**：`node --check` exit 0；四语言录制类残留全为 0；服务端文案确认；`prompt_audit` exit 0。

---

## 40. 第三十四轮：第 2 节后两个字段补说明（已完成）

第 2 节共三个字段，`delivery_context` 已在 §39 加说明；本轮补齐后两个，
格式与它一致 —— **先问，再说这影响什么**。

### 40.1 依据（规范原文）

| 字段 | 定义 | 对产物的影响 |
|---|---|---|
| `artifact_afterlife` | What must the file support afterward — review, approval, archive, hand-off, reuse, or nothing? | 是推导阅读模式的**三个输入之一**（`plan-core.md` §2） |
| `content_divergence` | how closely the deck follows the source versus how freely it reshapes it —— 从 *stay close* 到 *balanced* 到 *free* | 决定版面如何重组材料；**硬规则：不管多自由，事实必须来自源材料**，发散不等于引入外部事实 |

### 40.2 改动（四语言）

| 键 | 改前 | 改后 |
|---|---|---|
| `artifact_afterlife` | 演示后的成果用途 | **会后还要派什么用场？** |
| `artifact_afterlife_hint` | （无） | **要给人复核、留档或接手的话，页面就得自己能读懂。** |
| `sub_divergence` | 材料发散度（多大程度重塑，还是贴近源材料） | **材料发散度**（括号内容移交说明句） |
| `sub_divergence_hint` | （无） | **贴着你给的材料讲，还是允许重新组织？不管多自由，事实都必须来自材料。** |

两个 `labeledTextarea` 调用点的 hint 参数由 `null` 接上新键。

**验收**：四语言各改 8 项 + 新增 8 键，未命中 0；`node --check` exit 0；
静态自检通过；服务端文案确认；`prompt_audit` exit 0。

---

## 41. 运维备注：Confirm UI 何时需要重启（本轮查证）

**起因**：用户反映每次改动都弹出 python 控制台窗口。根因是**我每轮都重启服务器**，
而实际上多数改动并不需要。

### 41.1 代码依据

| 资源 | 读取时机 | 依据 |
|---|---|---|
| `/static/app.js`、`/static/style.css` | **每次请求读盘** | Flask 静态文件服务 |
| `/api/catalogs` | **每次请求读盘** | `server.py` L2441 `resp = jsonify(_build_catalogs())`，而 L2233 在该函数内 `_CATALOGS_PATH.read_text()` |
| `server.py` 本身 | 启动时载入 | —— |

**结论：只有改动 `server.py` 才需要重启；文案、样式、`catalogs.json`、模板索引一律免重启，
浏览器刷新即可。**（模板索引由 `_build_template_library` 读取，同属每次请求路径。）

### 41.2 弹窗的技术根因（供后续决定是否修）

`server_common.popen_detached()`（L174）用
`CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` 派生后台子进程，**本意就是无控制台**。
但实测子进程仍有可见窗口，原因是：

```
pid=48400  启动器   E:\...\.venv\Scripts\python.exe  （无窗口）
pid=9108   子进程   C:\Users\...\Python310\python.exe  （有窗口）
```

**venv 的 `python.exe` 会把自身重新执行为系统 Python**，因此启动器内的 `sys.executable`
指向系统解释器，子进程随之带上控制台。**这是产品行为，不只是本地调试现象** ——
任何用户执行 `server.py --daemon` 都会看到这个窗口。

**未修**：`DETACHED_PROCESS` 与 `CREATE_NO_WINDOW` 在 MSDN 上互斥
（后者在前者存在时被忽略），改起来需要重新验证后台存活语义，本轮不做，仅记录。

---

## 42. 运维备注（续 §41）：Confirm UI 改为无窗口启动（已解决）

**用户反馈的实际后果**：§41 提到的那个控制台窗口**就是服务器进程本体**，
用户顺手关掉它，服务就没了 —— 本轮实际发生了一次（日志停在正常 200 响应之后，
无错误、无 shutdown 记录，属外部终止）。**所以这不止是"烦"，还是个稳定性隐患。**

### 42.1 为什么直接加 flag 不管用

| 尝试 | 结果 |
|---|---|
| `server.py --daemon`（官方路径） | 有窗口。子进程用 `sys.executable` 启动，而 **venv 的 `python.exe` 是存根，会拉起源码目录里的系统 Python** —— 控制台在那一步产生 |
| 直接跑 + `Popen(creationflags=CREATE_NO_WINDOW\|DETACHED_PROCESS)` | 仍有窗口。存根拉起的系统 Python 不受这两个 flag 约束（MSDN：`CREATE_NO_WINDOW` 在 `DETACHED_PROCESS` 存在时被忽略） |
| `Start-Process -WindowStyle Hidden` | 仍有窗口 |

### 42.2 有效解法

用 **`pythonw.exe`**（Windows 上无控制台的解释器）启动，**并把 stdout/stderr 重定向到文件**。

后者是必需的：`pythonw` 下 `sys.stdout` / `sys.stderr` 为 `None`，
而 `server.py` 启动时会调用 `configure_utf8_stdio()` 去 reconfigure 它们 —— 会直接崩，
表现为"启动了但服务不在"。重定向后它们是真实文件对象，问题消失。

固化为 `run/serve-confirm-ui.py`：先探活并关掉已有实例，再以 pythonw 启动，最后轮询就绪。

**验证**：启动后 `Get-Process python,pythonw | Where MainWindowTitle -ne ''` **返回空**，
`/api/health` **HTTP 200**。

**注意**：这是**本地调试用的启动方式**，没有改动仓库内的 `server_common.popen_detached()`。
上游那条 `--daemon` 路径仍会弹窗 —— 若要为最终用户解决，需另行动 `server_common`，
并重新验证后台存活与 Job Object 语义。

---

## 43. 第三十五轮：「材料发散度」改标签与说明句（已完成）

**用户给定的原文，照此落地：**

```
材料怎么用？
照材料顺序讲，还是按论证需要允许重排、合并或拆分？
```

原标签「材料发散度」是统计术语，用户看到不知道在问什么；原说明句里的「重新组织」
也含糊。改动如下（四语言）：

| 键 | 改前 | 改后 |
|---|---|---|
| `sub_divergence` | 材料发散度 | **材料怎么用？** |
| `sub_divergence_hint` | 贴着你给的材料讲，还是允许重新组织？不管多自由，事实都必须来自材料。 | **照材料顺序讲，还是按论证需要允许重排、合并或拆分？** |

英文 `allow rearranging, merging, and splitting`、日文「並べ替え・統合・分割を許す」
对应「允许」。标签改成问句后与本节其余三个一致（这场演讲怎么进行？／会后还要派什么用场？）。

**一处提示，已确认按用户原样保留**：说明句不含规范里的硬规则
（`plan-core.md`：*facts stay sourced however free the user asks*）。
用户明确要求「就按我说的」，故不添加。该规则由下游 AI 执行，不依赖用户填写。

**验收**：`node --check` exit 0；服务端直接取到新文案；**未重启**（`app.js` 为静态文件，
按请求读盘 —— 见 §41）。

---

## 44. 第三十六轮：Stage 2 去掉「模板应用方式」一节（已完成）

**用户判定**：这一段是 AI 生成的内部术语，**用户根本读不懂，不该展示**。

实际生成的内容（取自 ESG 产物）：

> 沿用已安装的 report_core 版式系统：封面与结束页走在 engineering_blue 的深蓝反白 **Master** 上，
> 章节页走 **divider**，正文页走浅色 **content Master**，保留发丝分隔线、页码槽位与页边距。
> 按每页的信息模型选择 **Layout** —— ……用 **table_summary 的原生表格槽位**，……
> 与 **swiss-minimal 的栅格偏好**。所有页面内容按本篇论文材料重写……

**全是内部词汇**（Master / Layout / divider / 槽位 / 栅格偏好），既读不懂也改不动，只是增加困惑。

### 44.1 隐藏前的安全性验证

关键在 `app.js` 载入推荐时的两行：

```js
var templateApplication = templateApplicationRecommendation();
if (templateApplication != null) {
    STATE.template_application = templateApplication;   // ← 值来自推荐
} else {
    delete STATE.template_application;
}
```

**该字段由推荐自动填入并提交，输入框只负责"编辑"它。** 因此去掉显示后：
**字段照常填充、照常提交，下游流水线完全不受影响** —— 只是用户不再能看/改它。
（`templateApplicationRecommendation()` 与上述填充逻辑**均保留**，仅删渲染。）

### 44.2 改动

| 项 | 内容 |
|---|---|
| Stage 2 渲染序列 | 去掉 `renderTemplateApplication(host)` |
| 函数 | 删 `renderTemplateApplication()` |
| i18n | 删四语言各 3 个死键：`sec_template_application` / `template_application_hint` / `placeholder_template_application` |

Stage 2 由 15 节变为 **14 节**。

**验收**：`node --check` exit 0；服务端确认渲染函数与调用均已消失、填充逻辑仍在、
推荐里仍有该字段、stage 仍为 stage2；三个死键四语言残留 **0**。

---

## 45. 第三十七轮：修「只点卡片却被判为已调整」+ 加载时无卡片选中（已完成）

### 45.1 现象与疑问

用户点了一下「数据管线审计」卡片、没改任何东西，卡片却显示「已调整」并冒出「恢复原方案」按钮。
用户问：**这个按钮的意义是什么？**

**按钮本身的意义**是"撤销你在下面各节做的改动，还原成该方向的原样"，
**本来就只应在真的改动过时出现** —— 所以它出现本身就是 bug。

### 45.2 成因：基线取在重绘之前

`applyDesignDirection()` 原来的顺序：

```js
…设置 STATE…
ACTIVE_DIRECTION_ID = directionId;
ACTIVE_DIRECTION_BASELINE = directionStateSignature(candidate);   // ← 先取基线
if (shouldRender !== false) renderAll();                          // ← 再重绘
```

`renderAll()` 过程中会补写派生字段（字体 `css`、字号默认值一类，
如 `renderTypography` 内的 `updateRoleCss`、`syncUnpinnedTypographySizes`）。
**于是重绘后的实际状态与"重绘前取的基线"不同**，
`activeDirectionAdjusted()` 判定为已调整 → 卡片显示「已调整」+ 显示「恢复原方案」。

**修法**：基线改到 `renderAll()` 之后取，并补一次 `refreshDesignDirectionState()`。

### 45.3 顺带发现：加载时没有任何卡片显示为选中

`var ACTIVE_DIRECTION_ID = "";`，而它**只**在 `applyDesignDirection` 里被赋值。
所以首次打开页面时 `ACTIVE_DIRECTION_ID` 为空 → **所有卡片都不高亮**，
尽管推荐的那套其实已经生效 —— 用户不知道当前走的是哪条路线。

**修法**：`renderDesignDirections` 首次渲染时，若 `ACTIVE_DIRECTION_ID` 为空，
就用 `selectedDesignDirectionIndex()` 把已生效的那条标为选中，并同步基线。

### 45.4 本轮同时完成的文案改动

| 项 | 改前 | 改后 |
|---|---|---|
| 节标题 | 整套方案 | **设计路线** |
| 说明句 | …或在**下方**微调各项。调整后可用"恢复原方案"还原整套预设。 | …点别的卡片就整套换过去；**要逐项改，请往下滚到后面各节**。 |

「下方」原本指页面下面那十几节，用户读成了"卡片下方会出现可调项"，点卡片后自然觉得没反应。

**验收**：`node --check` exit 0；服务端确认两处修复与文案均在。
**未能验证**：我无法真点击，需用户刷新后确认。

---

## 46. 第三十八轮：不再展示「整体形象」预览（已完成）

**用户判定**：价值不大，不对用户展示。

**改法（只去掉展示，不动代码）**：删掉 Stage 2 渲染序列里的那一行调用。

```js
// 改前
if (previewHost) renderStylePreview(previewHost);
if (previewHost) renderImageStrategyPreview(previewHost);

// 改后
// 「整体形象」预览已按用户要求不再展示（函数保留，随时可恢复）。
// 顶栏仍渲染配图风格预览。
if (previewHost) renderImageStrategyPreview(previewHost);
```

**保留未删**（用户明确"只是去掉 UI 里的展示而已"）：

| 保留项 | 状态 |
|---|---|
| `renderStylePreview()`（87 行）与其辅助 `stylePreviewContentMarkup()` | 仍在，未被调用 |
| `refreshStylePreview` 变量与 14 处调用 | 仍在；因该变量从未被赋值，始终是空函数，无副作用 |
| 相关 CSS（`.style-preview*` / `.sp-*` / `.spl-*`） | 仍在，未被使用 |
| 顶栏的「配图风格预览」 | **不受影响，照常渲染** |

**说明**：本轮特意不做死代码清理 —— 用户要求的是最小改动，且该预览随时可能恢复。
这属于**已知的有意保留**，不是遗漏。

**验收**：`node --check` exit 0；`renderStylePreview(previewHost)` 调用已消失、
函数本体仍在、`renderImageStrategyPreview(previewHost)` 仍在。

---

## 47. 第三十九轮：「自定义色值覆盖」改为真正的取色器（已完成）

**用户判定**：色块只是个展示用的方块，旁边是 HEX 文本框 —— **想改颜色必须先知道 HEX**，
等于逼用户去别处查色值。"看似提供了选择，实际上没人知道咋改。"

### 47.1 改动

| 项 | 改前 | 改后 |
|---|---|---|
| 色块 | `<div class="hex-swatch">` 纯展示 | **`<input type="color">`** —— 点击弹系统色盘 |
| HEX 文本框 | 唯一入口 | 保留，供精确输入与粘贴 |
| 同步 | 单向（文本框 → 状态） | **双向**：色盘选值回填文本框；手输 HEX 同步色盘 |

两个入口写同一份状态，收敛在一个局部函数里：

```js
function applyOverride(value, fromPicker) {
    …STATE.color.palette[role] = value;
    var n = normHex(value);
    if (n) sw.value = n;                    // 色盘跟随手输值
    if (fromPicker) inp.value = n || value; // 只有色盘来的才回填文本框，避免打字时光标跳动
    …同步到已选卡片上的色块…
}
sw.addEventListener("input", function () { applyOverride(sw.value, true); });
inp.addEventListener("input", function () { applyOverride(inp.value, false); });
```

`applyHexInputs()` 也改为用新helper `syncColorPicker()` 回填取色器
（切换配色卡片时两者都要跟上）。取色器只接受合法 `#rrggbb`，空值时保持不变以免原生控件报错。

新增 i18n 键 `pick_color`（四语言），作为取色器的 title / aria-label。

### 47.2 顺带清理

改造后 `paintSwatch()` 已无调用方（只剩定义），`hex-swatch-empty` 随之失效。
**两者均已删除**（函数 + CSS 规则），残留 0。

**验收**：`node --check` exit 0；静态自检通过；服务端确认
`sw.type = "color"` / `syncColorPicker` / `pick_color` / 三条 CSS 规则全部就位。
**未能验证**：色盘的实际弹出需用户在浏览器确认。

---

## 48. §47 引入的 ReferenceError：pal is not defined（已修）

**现象**：页面报「无法加载推荐文件，需在启动前写入。 pal is not defined」，
Stage 2 整页白屏。

**成因**：§47 给取色器做初始化时写了 `syncColorPicker(sw, pal[role])`，
但 `pal` 是**候选配色卡片那个 forEach 回调里的局部变量**（`var pal = normPalette(c);`），
取色器那一行在回调之外，作用域里根本没有它。

**修法**：改用当前状态里的调色板。

```js
// 改前
syncColorPicker(sw, pal[role]);
// 改后
syncColorPicker(sw, (STATE.color && STATE.color.palette &&
    STATE.color.palette[role]) || "");
```

### 48.1 为什么没被拦住

`node --check` **只验语法** —— 引用一个不存在的变量语法完全合法，
只有真正执行到那一行才抛 ReferenceError，而页面只在浏览器里跑。

**这是同一类问题的第二次**（第一次是 §24 的 `sec is not defined`）。

### 48.2 尝试写自动检查，未成功，已放弃

写了一个作用域分析器 `run/check-undefined-identifiers.py`：
剥注释与字符串 → 按花括号配对建函数作用域树 → 检查每个标识符是否在
自身/祖先/顶层/已知全局里。

**结果：481 个作用域里报出 114 处可疑，全是误报**（`preset`、`pair`、`item`
等回调参数被误判）。用 `presetSelectionKeys` 单独复现时正则与参数提取都正确，
问题在作用域树的构建环节。

**已删除该脚本** —— 一个满是误报的检查器比没有检查器更糟，会训练人忽略它。
此类问题目前只能靠**在浏览器里真跑一遍**发现。

**验收**：`node --check` exit 0；服务端确认旧写法消失、新写法就位。用户需刷新确认页面恢复。

---

## 49. 第四十轮：把「整体形象」预览搬进「色彩方案」（已完成）

**用户指出的后果**：§46 从顶栏移除该预览后，「自定义色值覆盖」变成盲改 ——
用户看到「主色 / 强调 / 次强调 / 次级背景」这些角色名，
**却看不到它们对应 PPT 的哪一部分**。"那这个调整依旧是无效的。"

**根因**：那个预览本来就是干这个的（标题用主色、竖条用强调、正文用正文色、
底条用次级背景），它此前**只挂在顶栏**，离改色的位置太远，所以显得没意义。
**问题不在组件，在位置。**

### 49.1 改动

在 `renderColor` 里就地调用一次 `renderStylePreview(sec)` —— 预览出现在改色行的正下方。

```js
override.appendChild(row);
sec.appendChild(override);
// 色值就地预览：这些角色色分别对应页面的哪一部分，必须看得见，
// 否则改色等于盲改。同一个组件原先只挂在顶栏，离改色的位置太远，因此搬到这里。
renderStylePreview(sec);
// 顶栏那版是 position:sticky 的，内嵌进本节后要去掉，否则会粘在滚动容器顶部。
var inlinePreview = sec.querySelector(".style-preview");
if (inlinePreview) {
    inlinePreview.classList.add("style-preview-inline");
    inlinePreview.style.top = "";
}
host.appendChild(sec);
```

新增 CSS `.style-preview-inline`：`position: static / z-index: auto / background: none /
padding: 0 / margin: 14px 0 0`。

**无需额外接线**：`renderStylePreview` 内部本来就把自己注册成 `refreshStylePreview`
（`refreshStylePreview = paint;`），而改色值的 `applyOverride` 末尾会调它 ——
所以**改色时预览实时重绘**。全文件共 11 处该调用，均有效。

**复用而非重写**：`renderStylePreview` 及其 `stylePreviewContentMarkup`、
`stylePreviewRows`、`paint` 闭包全部沿用原实现，一行未改。

**验收**：`node --check` exit 0；静态自检通过；确认 `renderStylePreview(sec)` 在
`renderColor` 内、`refreshStylePreview = paint` 仍在、11 处调用仍在。

---

## 50. 第四十一轮：内嵌预览缩小（已完成）

承 §49。用户要求：**把预览缩小，并放进「色彩方案」里，免得每调一次就滚回顶部。**

放置位置 §49 已完成（`renderColor` 内就地调用，位于「自定义色值覆盖」正下方）。
本轮做的是**收紧体积**。

### 50.1 关键约束：字号缩不动

`renderStylePreview` 的 `paint()` 把字号**内联**写在元素上：

```js
title.style.fontSize = Math.round(bodyPx * 1.7) + "px";
bodyWrap.style.fontSize = bodyPx + "px";
```

内联样式优先于 CSS，**所以字号无法用 CSS 缩小**（`bodyPx` 自身已钳制在 12–34px）。

**但占空间的不是字号**，而是布局尺寸 —— 顶栏版靠 `min-height: 260px` 撑出展示感，
另外 `padding` 与 `gap` 也偏大。这些都能收紧：

```css
.style-preview-inline .style-preview-card { min-height: 0; padding: 10px 12px; gap: 8px; }
.style-preview-inline .style-preview-label { margin-bottom: 3px; }
.style-preview-inline .sp-body { margin-top: 4px; }
.style-preview-inline .sp-content { gap: 5px; }
.style-preview-inline .sp-content-row { padding: 5px 8px; }
.style-preview-inline .sp-chip { padding: 5px 9px; }
```

（顶栏版样式一字未动 —— 全部规则都以 `.style-preview-inline` 限定，只作用于内嵌的那份。）

**验收**：静态自检通过；服务端确认 4 条 CSS 规则就位。
若仍偏大，可进一步精简示例行（`.sp-content` 那组图标行），需用户确认后再做。

---

## 51. §50 的 CSS 顺序错误：内嵌规则整块失效（已修）

**现象**（用户截图）：预览纹丝不动 —— 仍是 260px 高的白色大卡、
标签行仍是顶栏那种深色底、英文样例横向溢出到容器外。

**成因**：上一轮把 `.style-preview-inline` 整块插在了 **L153**，
而 `.style-preview` 的基础规则在 **L1084**。
两者优先级相同（都是单个类），**后出现的胜出** —— 于是内嵌规则全被覆盖，形同不存在。

**这是我自己引入的错误**：加规则时只想着"插在 .style-preview-card 前面"，
没有确认基础规则在文件中的位置。

### 51.1 修法

1. **整块搬到文件末尾**，并写明"必须放在基础规则之后"的原因，避免后人重蹈。
   位置：基础规则 L1084，内嵌规则 L1288+。
2. **同时解决横向溢出** —— 该组件原为顶栏宽横条设计，塞进节内窄列必然溢出。
   仅对**内嵌版**做两项裁剪：
   - 隐藏三行图标示例（`.sp-content`）：与「图标使用」一节重复，且是最大的空间占用者
   - 隐藏英文样例（`.sp-title-english` / `.sp-body-english`）：窄列里只会溢出，
     中文样例已足够判断字体与颜色
   - 文本容器补 `min-width: 0` + 正确的 `overflow` / `ellipsis` 裁剪

**顶栏版样式一字未动**（全部规则以 `.style-preview-inline` 限定）。

**验收**：确认 `.style-preview-inline` 全部 11 处位于基础规则之后。

---

## 52. 第四十二轮：「色彩方案」重构 —— 只留六个角色色 + 就地预览（已完成）

**用户要求**：去掉「深蓝证据 / 对照双色 / 自定义配色」这几张预设卡片，
**只留下面的 6 个角色色选择**（背景 / 次级背景 / 主色 / 强调 / 次强调 / 正文文字），
**下面实时展示整体形象的对应变化**。
同时指出：上一轮调整后预览**变成了横幅**。

### 52.1 先修横幅（我的错）

`.style-preview-card` 基础规则是 `display:flex; align-items:center` 的**横排**。
上一轮为缩小体积隐藏了中间的内容列，于是变成"标题在左、色块被甩到最右"，
整条被撑成横幅。

**修法**：内嵌版改竖排。

```css
.style-preview-inline .style-preview-card {
    flex-direction: column;
    align-items: flex-start;
    …
}
```

### 52.2 删掉的东西

`renderColor` 由 **153 行缩到 60 行**。移除：

| 移除 | 说明 |
|---|---|
| `color-grid` 与候选卡片循环 | 三张预设配色卡 |
| `customCard`（自定义配色）与 `customInput`（配色文字说明） | 用户明确要求去掉 |
| `selectCard()` / `selectCustomColor()` | 卡片选择逻辑 |
| `cardSwatchRefs` / `selectedIdx` / `applyHexInputs()` | 随卡片一并失效 |
| `applyOverride` 里"把改动映到已选卡片色块"那段 | 卡片已不存在 |

**保留**：六个角色色的取色器 + HEX 输入、`syncColorPicker`、就地预览（含内嵌变体类）。

### 52.3 提交不受影响（已核对）

`designSystemValid()` 只要求二者之一：

```js
var completePalette = PALETTE_ROLES.every(role => !!normHex(palette[role]));
var customPalette   = color.name === "custom" && String(color.custom || "").trim();
```

去掉预设后，**六个色值仍由设计路线**（`design_directions` 的 `candidate.color`）
带进来，`palette` 始终齐全，故校验照常通过。
`color.name` 亦由设计路线赋值，不再依赖卡片。

**保留未动**：`colorRecommendationCandidates()`（载入推荐时仍用，L4287）
与 `custom_color_required` 校验分支（安全网）。

### 52.4 顺带清理

`custom_color`（自定义配色）与 `custom_color_placeholder` 因 UI 移除而成为死键，
**四语言各 2 个已删**，残留 0。

**验收**：`node --check` exit 0；静态自检通过；服务端确认预设网格与自定义配色选择已消失、
取色器与就地预览仍在、竖排修复就位。
**未决**：`hex_override` 的文案仍是「自定义色值覆盖：」—— 现在它是唯一入口，
"覆盖"二字已不贴切，待用户定夺是否改名。

---

## 53. 第四十三轮：预览标签、嵌入化、连续缩小（已完成）

### 53.1 标签

`style_preview_label` 四语言由「整体形象（配色 + 字体 + 图标）」改为 **「效果预览」**
（zh-TW 效果預覽 / en Preview / ja プレビュー）。
后半句 `style_preview_body`（「· 仅大致形象，非实际版式」）保留 —— 它是免责说明，仍然准确。
该键只被 `renderStylePreview` 一处使用，改动无外溢。

### 53.2 去掉浮窗感

浮窗感来自基础规则的 `box-shadow: var(--shadow)`。内嵌版改为 `box-shadow: none` + 细边框。

**注意**：不能覆盖 `background` —— 那正是 `paint()` 要展示的用户所选背景色。

### 53.3 连续缩小（三轮迭代）

| 版本 | 做法 | 预览卡高度 |
|---|---|---|
| v7 | 强制 `aspect-ratio: 16/9` | ~365px |
| v9 | 去掉 16:9，盒子按内容收紧 | ~300px |
| v10 | `INLINE_PREVIEW_SCALE = 0.66` | ~270px |
| v11 | `INLINE_PREVIEW_SCALE = 0.55` + 示例行/色块 9.5px | **~235px** |

**途中两次误判，均靠截图发现**：

1. **`zoom: 0.62` 无效** —— 只缩了内容，盒子仍是满宽，反而留出大片空白。
2. **正文下方一大块空白** —— 先误判为 grid 的 `align-content`，改后截图**字节数完全相同**，
   说明没生效；真正原因是 `.sp-textcol { flex: 1 }`：横排时用于占宽，
   改竖排后变成吸收所有剩余高度。
3. **`.sp-textcol { flex: none }`** 修掉空白。

### 53.4 为什么这次允许缩字号

此前两次拒绝缩字号，理由是"会谎报用户选定的字号"。
但该预览的标签本身声明 **「仅大致形象，非实际版式」** —— 它的定位是近似效果，
不是版式复刻。据此，等比缩小语义一致，等同幻灯片缩略图。

**且不缩就缩不动**：字号是这块高度的主要来源。
实现为 `paint()` 内的统一系数 `INLINE_PREVIEW_SCALE`（当前 0.55），
CSS 侧的示例行与色块同步降到 9.5px 以保持比例。

### 53.5 方法改进（本轮最重要的产出）

**从此每次改 UI 都用 headless Edge 截图自查**，不再靠读代码推断：

```powershell
msedge --headless=new --window-size=1200,5600 --screenshot=out.png http://127.0.0.1:5055/
```

本轮前三个错误（CSS 顺序、横幅、HEX 空值）都是因为没有实际渲染而漏掉的；
引入截图后，`zoom` 无效与 grid 误判都是**立刻**发现的。

### 53.6 顺带根治缓存

`/static/*` 原先回 `Cache-Control: no-cache`（需重新校验），
现由 `server.py` 新增的 `_no_store_static` 钩子改为 **`no-store`** —— 普通刷新即生效。

**注意**：该钩子必须在 `app = Flask(...)` **所在的函数内**、按 4 空格缩进插入。
第一次插到模块级，导致 `NameError: name 'app' is not defined` 并截断了该函数剩余语句。

**验收**：`node --check` exit 0；静态自检通过；截图确认标签、嵌入效果与尺寸。

### 53.7 收窄宽度（用户追加）

字号缩小后，卡片仍占满整节宽度，显得空旷（约 940×235，比例 4:1）。
加 `max-width: 440px` 后宽度收窄、高度不变（高度由字号决定），
比例自然落到约 **1.87:1 —— 接近 ppt169 的 16:9**，观感即一张幻灯片缩略图。

无需其它改动：`.style-preview` 外层是块级元素，卡片左对齐即可。

---

## 54. 第四十四轮：AI 自拟文字里的目录 id（已查清，用户决定暂不处理）

### 54.1 现象

「内容展开方式」「视觉方向」的 AI 自拟卡片里出现内部 id：

> 以 **pyramid** 为主导：第 2 页直接给出结论与限定…
> 由 **swiss-minimal** 负责精确栅格和大留白…

这些文字直接展示给用户，用户读不懂；且它可编辑，行话让人无从下手。

### 54.2 根因：规范示例与规范规则自相矛盾

规范**要求**这些文字面向用户 —— `scripts/docs/confirm_ui.md` L432：

> **Candidate display text is written once, in the confirmed UI language**

规范**另有字段**承载目录来源 —— `confirm_ui.md` L476-478 与
`templates/spec_lock_reference.md` L95-96：

```markdown
- mode_references: pyramid, narrative, instructional     ← id 该在这里
- mode_behavior: Open conclusion-first with pyramid, …   ← 这里又写了一遍
```

**但两处示例都把 id 写进了句子**：

| 文件 | 行 | 内容 |
|---|---|---|
| `references/confirm-surface.md` | L74 / L76 | `recommendations.stage2.json` 的示例（**AI 照此写界面文字**） |
| `templates/spec_lock_reference.md` | L96 | `spec_lock` 示例（内部文件，影响较小） |

**AI 是照抄示例，不是自己发挥。**

### 54.3 建议改法（本轮未执行）

1. `confirm-surface.md` L74/L76：把 id 换成目录项的 UI 语言名称
   （pyramid → 「结论先行」、swiss-minimal → 「瑞士极简」）。
2. `confirm_ui.md` L432 补一句：界面文字不得内嵌目录 id，它们属于 `*_references` 字段。

**未执行的理由**：属于提示词改动（`references/`），会影响后续生成，用户明确表示暂不处理。

### 54.4 一个未解的耦合（若日后要改，必须先解决）

`confirm_ui.md` L473-480 规定：`mode_references` 等**仅当该 behavior 确实使用了具名目录来源时**才投影。
若把 id 从 behavior 文字里去掉，这条触发条件可能落空，导致 Executor 拿不到来源。
**改示例前需先确认 Strategist 能否按 UI 语言名称（如「结论先行」）匹配目录项**，否则会断链。

### 54.5 相关：本轮已完成的标签改动

`catalogs.json` 中 `id=pyramid` 的显示标签已改为
「结论先行 / 結論先行 / Conclusion first / 結論から先に」（**id 未动** ——
`spec_lock.schema.json` 的 `field_enums.mode` 枚举了它，`findCatalogOption()` 也按 id 匹配）。

---

## 55. 第四十五轮：Stage 2 界面文字全面通俗化（已完成）

**用户要求**：以"第一次使用、什么都不懂的大学生"视角通读 Stage 2 的标题与说明，
把看不懂的、有疑惑的全部重写（排除 AI 生成的内容）。

### 55.1 第一轮：标题与主干说明（app.js，四语言 60 处）

| 键 | 改前 | 改后 | 问题 |
|---|---|---|---|
| `design_directions_hint` | 这份 **deck** 走哪条路线… | 这份**演示文稿**走哪条路线… | deck 是英文行话 |
| `scheme_component_options` | **项目专属自定义方案** · 选中卡片后可编辑 | **AI 为这份材料写的做法** · 选中卡片后可编辑 | 词序别扭 |
| `sec_reading_mode` | **阅读模式** | **内容详略** | 像 Kindle 设置；实际问的是页面放多少字 |
| `hex_override` | 自定义色值**覆盖**： | **六个部分各自的颜色**： | 已无"被覆盖"的对象 |
| `font_body_size` | 正文**基准**字号 | **正文字号** | 基准是行话 |
| `image_strategy_reference_hint` | 只展示**渲染风格** | 只用来**定画法** | 渲染是行话 |
| `sec_refine` | 先审核**设计规范** | **先看一遍大纲** | 内部产物名 |
| `sec_design_spec_depth` | **设计规范**详细程度 | **大纲写多细** | 同上 |
| `sec_mode` | **生成模式** | **生成方式** | 太泛 |
| `refine_on_desc` / `refine_off_desc` | 生成**设计规范**后暂停…生成**执行锁**… | 先出一份逐页大纲让你过目… | 内部术语 |
| `mode_split_desc` | 写完**设计规范**后停止 | 先出大纲，你确认之后再生页面 | 内部术语 |

### 55.2 第二轮：剩余行话（app.js，四语言 48 处）

清掉 11 个残留：`font_body_size_hint`（正文基准）、`body_size_hint_purpose`
（引用了已改名的旧节名「阅读模式」）、`size_override`（逐角色）、
`image_strategy_rendering`（渲染风格）、`image_strategy_ai_custom_desc`、
`body_size_hint_canvas` / `body_size_hint_oor` / `sec_canvas` /
`template_preset_none` / `template_preset_needs_canvas`（画布 → 比例）、
`delivery_purpose`（阅读模式 → 内容详略）、`custom_color_required`（描述的是已移除的字段）。

### 55.3 catalogs.json

| 项目 | 改动 |
|---|---|
| `image_usage` 五项 | **原本一个描述都没有**；补齐四语言描述，「占位符」→「先放占位方块」，其余改为「让 AI 画图 / 从网上找 / 用我自己给的图 / 完全不用图」 |
| `image_ai_path` 四项 | **原本全是实现细节**（接口后端 / 宿主原生工具 / `image_gen.py` / `IMAGE_BACKEND` / Codex）；改为「自动（两条路都试）/ 只用绘图接口 / 只用这个工具自带的画图能力 / 我自己画好再放进来」，描述里不再出现任何实现名词 |
| `delivery_purpose` | 「文字型 · **近读**」（生造词）→「偏文字 · 能独立读懂」等 |
| `modes` 的结论先行 | 去掉「**相互独立且完全穷尽**」（MECE 行话） |

### 55.4 过程中发现并修掉的三个真问题

1. **日语缺 5 个键** —— `canvas_section_hint`、`sec_reading_mode`、
   `template_kind_gives_{style,layout,deck}`。界面会**直接显示键名**。
   其中前两个仍在使用（已补），后三个是 §18 改版留下的**死键**（四语言删除，ja 本就没有）。

2. **自检只比对 zh 与 en** —— 这正是日语缺键长期未被发现的原因。
   已改为四语言全查，并增加"多出键"检测。

3. **自检的括号计数会被字符串内的花括号污染** —— 占位符 `~{lo}-{hi}px`、「{canvas}」
   会被当成真括号，导致块边界偏移、报出并不存在的"多出键"。
   另有一处：语言块自身的开头行 `en: {` 被当成一个键，
   使 en / ja 各多报一个与自己同名的键。两个都已修。

### 55.5 又一次踩到直引号陷阱

`design_spec_depth_locked` 的值里用了直引号 `"`，把 JS 字符串截断 —— **本项目第 5 次**。
已改用中文引号「」。同时新增扫描：逐行检查「键: 值」形态的值里是否含未转义直引号。

### 55.6 验收

- `node --check` exit 0
- 自检：四语言各 **178** 键，**缺 0 多 0**；zh 残留行话扫描 **0 处**
- 截图确认：卡片组标题、各节标题与说明、图片使用五项描述、生成/大纲各节均按新文案渲染

**未处理（用户已表态）**：AI 自拟文字里的 `pyramid` / `instructional` 等目录 id —— 见 §54。

---

## 56. 第四十六轮：Stage 2 入口加「交给 AI / 我自己调」必选（已完成）

**用户提议**：进入 Stage 2 时先让用户在「自定义」与「交给 AI」之间二选一；
交给 AI 即全盘接受直接确认。**并明确要求：没有默认，两个按钮，必须选一个。**

### 56.1 设计

```
1  这一步怎么走？   先选一个。选完才能确认，之后也可以随时改。
   ( ) 交给 AI     直接用 AI 推荐的方案，不再逐项调整
   ( ) 我自己调     展开下面各项，逐个看过再改

   选「交给 AI」时追加一行摘要：
   将按：设计路线 数据管线审计 ｜ 页数 14-16 ｜ 内容详略 图文均衡 · 报告 ｜ …
```

| 状态 | 界面 |
|---|---|
| 未选 | **不渲染任何一节**，确认被拦住并提示 |
| 交给 AI | 仍不渲染各节，改显示一行摘要 |
| 我自己调 | 展开全部 14 节，与原行为一致 |

**摘要的意义**：这是全盘接受，用户至少要看见自己接受了什么。

### 56.2 实现

- `STAGE2_MODE` 模块变量，初值 `""`（无默认）；`renderStage2ModeChoice()` 渲染二选一
- 复用 Stage 1 的 `renderTemplateModeChoice()`；为其增加可选参数 `currentMode`
  （省略时沿用 `TEMPLATE_MODE`，Stage 1 行为不变），避免重复一套样式
- `renderForStage` 的 Stage 2 分支：先渲染选择区，**只有 `manual` 才渲染 14 节**
- `confirm()` 开头拦截：`STAGE === 2 && !STAGE2_MODE` → 提示 `stage2_mode_required`
  并滚动到选择区（沿用 §45 的做法：底部提示看不见时要把问题区域滚进视野）
- 新增 8 个 i18n 键 × 4 语言（184 键）

### 56.3 验证时发现并修掉的三个问题

摘要首次渲染出：

```
将按：设计路线 数据管线审计 · 页数 14-16 · 内容详略 图文均衡 · 报告 ·
     色彩方案 深蓝证据 · 图标使用 线性描边图标 · sec_typography 微软雅黑 + Arial
```

1. **`sec_typography` 这个键不存在**（正确的键是 **`sec_type`**）→ 摘要里直接显示键名。
2. **分隔符与标签撞车**：分隔用「 · 」，而选项标签自带「 · 」（如「图文均衡 · 报告」）
   → 改为全角竖线「 ｜ 」。
3. **深底深字**：摘要框用了 `var(--shell-2)`，而 `--shell-2` 是 **`#12121f`**
   —— 那是**页面外壳**的深色底，不是卡片底色；文字色又用了**根本不存在的 `var(--text)`**。
   改用 `var(--accent-soft)`（#eaf4ff）+ `var(--ink)`（#1d2430）。

**教训**：写 CSS 变量前先看 `:root` 里到底有没有这个变量。
本轮 `--shell-2` / `--text` 两个都是想当然用的。

### 56.4 未点击状态如何验证

我无法真点击，因此三次验证分别用「临时改 `STAGE2_MODE` 初值 → 截图 → 还原」的方式完成。
过程中踩到一个自造陷阱：批量替换时**第一次改成 `"manual"` 后锚点就再也匹配不到了**，
导致第二张截图仍是 manual 状态（两张 PNG 字节数完全相同才暴露）。
正确做法是每轮替换前先从备份还原。

另：**在 Python 里用 `subprocess` 起 Edge 截图不可行** ——
沙箱下给子进程建管道会被拒（EPERM，DEVNULL 亦然）。改用 PowerShell 调用即可。

---

## 57. 第四十七轮：合并「图片使用」与「生成配图设置」两节（已完成）

**用户指出**：第 10 节「图片使用」的那几个选项本身就是图片来源，
第 11 节「生成配图设置」却又显示「已选图片来源」回显 —— 两节重复。

### 57.1 核对结果：用户是对的

| 节 | 实际渲染 |
|---|---|
| 10 图片使用 | 5 个来源 chip + 图片补充要求 + **生成图风格**（仅需 AI 图时显示） |
| 11 生成配图设置 | **一行来源回显（纯重复）** + 生成方式（仅需 AI 图时显示） |

**所以第 11 节实际只贡献一个控件**：`image_ai_path`（生成方式）。

### 57.2 合并方式

把「生成方式」并进第 10 节的 `strategySub` —— 它本就在
`needsGeneratedImagesForUsage()` 时显隐，与新控件的适用条件**完全一致**：

```js
var aiPathField = el("div", "subfield");
aiPathField.appendChild(el("div", "subfield-label", t("image_ai_path")));
enumField(aiPathField, CAT.image_ai_path, recOrFirst("image_ai_path", CAT.image_ai_path),
    function () { return STATE.image_ai_path; },
    function (value) { STATE.image_ai_path = value; });
strategySub.appendChild(aiPathField);
```

**删除**：第 11 节整节、来源回显、`renderImageProduction()`（27 行）、
`refreshImageProduction` 变量与全部调用、3 个 i18n 键（四语言）、
`.locked-summary-chip` 两条 CSS（已无引用）。

**Stage 2 各节由 15 节变为 14 节**（含新增的走法二选一）。

### 57.3 验证边界（如实记录）

- ✅ 第 11 节消失、编号自动接续 —— 截图确认
- ✅ `node --check` exit 0；四语言各 182 键、缺 0 多 0
- ✅ 合并后 `strategySub.style.display` 的判定条件**一字未改**，
  且新控件原本就在同一条件下渲染 —— 行为由构造保证
- ❌ **未能视觉确认「选『让 AI 画图』后该控件出现」**：
  试了两次改样例数据（先写成裸数组，后写成 `{"value": ["ai"]}`）都没能让页面进入该状态，
  说明推荐文件里该字段的实际路径与我的猜测不符。**未继续深挖。**

**换句话说**：该路径的**条件判断复用未动**，但「AI 图被选中时它确实显示」这一点
目前只有代码推断，没有截图证据。请用户在界面上选一次「让 AI 画图」确认。

### 57.4 顺带确认的一件事

`/api/recommendations` **在服务器启动时读入内存**，改文件后需重启才生效
（与 `/api/catalogs` 每次请求读盘不同 —— 见 §41）。本轮两次失败均与此无关，但值得记录。
