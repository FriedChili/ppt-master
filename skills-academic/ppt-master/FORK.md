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
| 非科研 `brand` kind 引用残留 | 0 |
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
