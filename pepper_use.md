# 对接 Pepper 工作区

本文说明**如何把一份 Pepper 上游工作区喂给 ppt-master**，解析器做什么、为什么这么做，
以及每一步该怎么跑。设计论证与实测证据在 [`PIPELINE-INTEGRATION.md`](PIPELINE-INTEGRATION.md)；
UI 与分支层面的改造清单在 [`skills-academic/ppt-master/FORK.md`](skills-academic/ppt-master/FORK.md)。

---

## 0. 一句话

Pepper 工作区里有论文、图件、表格和一堆管线内部产物。
**解析器把"对做 PPT 有贡献的那部分"挑出来，铺成一个扁平目录，交给技能原生的摄入通道。**
技能侧一行代码都不用改。

```bash
python3 skills-academic/ppt-master/scripts/resolve_sources.py <workspace> --stage <flat_dir>
python3 skills-academic/ppt-master/scripts/project_manager.py init <project_name>
python3 skills-academic/ppt-master/scripts/project_manager.py import-sources <project> <flat_dir> --copy
```

---

## 1. 本次为对接 Pepper 做的适配

| # | 适配点 | 说明 |
|---|---|---|
| 1 | **新增解析器** | `scripts/resolve_sources.py` + `scripts/source_manifest.json`。声明式清单，确定性执行，**不调用模型** |
| 2 | **技能侧零改动** | 解析器产出**扁平目录**，正好是 `import-sources` 本来就接受的形态。不改 `source_to_md.py`、不改 `import-sources`、不改任何 ingest 路径 |
| 3 | **绕开 pandoc 依赖** | 图件优先取位图本体（png），表格同时带上 `.tex`（结构与题注）与 `.csv`（原生数值）——**两者都不触发 LaTeX 转换**。若环境没有 pandoc，管线照样跑通 |
| 4 | **只读声明，不猜命名** | 图件与表格的名字不可预测，因此**从论文自己的 `\input{}` / `\includegraphics{}` 声明反查**，而不是枚举目录 |
| 5 | **管线产出即事实源** | 论文正文（PDF→markdown）承担全部数值；图注取自浮动环境；`refine-logs/` 的五份文档提供契约字段的措辞依据 |

> 分支层面还做了别的改造（确认页文案、Stage 2 入口二选一、色彩方案重构、模板 spec 英文化等），
> 那些与 Pepper 无关，见 `FORK.md`。

---

## 2. Pepper 工作区长什么样

解析器认的是这套约定（本仓库 `projects/` 就是一份真实样本）：

```
<workspace>/
├── assignment_profile.json          # 作业元信息（可选）
├── output/
│   ├── main.tex                     # ★ 硬门：没有它就不产稿
│   ├── main.pdf                     # ★ 主交付物，正文与数值的事实源
│   └── results/*.csv                # 实验数值（备份源）
├── necessary_materials/
│   ├── figures/                     # 图件（png / pdf / svg 混存）
│   ├── tables/                      # 表格（tex / csv / md 混存）
│   └── references.bib
├── refine-logs/                     # 过程文档，五份对 PPT 有贡献
│   ├── DECISION_LOG.md
│   ├── VERIFICATION_REPORT.md
│   ├── LITERATURE_REVIEW.md
│   ├── METHOD_UNDERSTANDING.md
│   └── EXPERIMENT_PLAN.md
├── codes/                           # ✗ 不读（实验代码，与做 PPT 无关）
└── dois/ library/ contracts/ logs/ archive/   # ✗ 不读
```

**目录名不是硬约束**：清单里的路径可按需改。硬约束只有两条：
`output/main.tex` 必须存在，且清单里写的路径必须与工作区实际一致。

---

## 3. 解析器原理

### 3.1 它回答两个技能自己回答不了的问题

1. **哪些上游产物值得读？** —— 其余都是噪音（代码、契约、构建日志、管线内部笔记）。
2. **图件和表格到底是什么？** —— 它们的名字不可预测。

### 3.2 图件与表格：从声明反查，按主名去重

```
output/main.tex
    \input{tables/tab_main_p95}        →  表格 stem: tab_main_p95
    \includegraphics{figures/fig_cost} →  图件 stem: fig_cost

配对的浮动环境
    \begin{figure} ... \includegraphics{...} \caption{...} \end{figure}
                                        →  该 stem 的图注
```

- **按 stem 去重**：同一张图存在 `.png` 与 `.pdf` 两份时只算一条。
- **按 `ext-preference` 取首选扩展名**：图件默认 `png > pdf > svg`。
  备选扩展名**默认不暂存** —— PDF 会被摄入工具转成 markdown，产生一堆垃圾文件。
- **表格例外**：`stage-alt: true`，同时暂存 `.tex` 与 `.csv`。
  tex 供结构与题注，csv 供原生表格数值，**两者都不触发 pandoc**。
- **图注来源**：优先取浮动环境里的 `\caption{}`；表格若没有，就从 `.tex` 体内提取。
  LaTeX 外壳（`$`、`\_`、`\textbf{}`）只做**无损**剥离，任何需要判断语义的都不动。

### 3.3 契约字段：`needs` ↔ `conditional` 反向索引

```json
"needs":      ["positioning", "mechanism", "design_rationale",
               "communication_intent", "audience_outcome", "reliability"],
"conditional": [
  { "id": "decision-log", "path": "refine-logs/DECISION_LOG.md",
    "provides": ["communication_intent", "design_rationale", "audience_outcome"] },
  ...
]
```

产出 `read` 段是**按需要分组**的文件列表：

```
read.design_rationale → ["DECISION_LOG.md", "EXPERIMENT_PLAN.md"]
read.mechanism        → ["LITERATURE_REVIEW.md", "METHOD_UNDERSTANDING.md"]
```

**某个 need 一个来源都没有 → 进 `unavailable`**，提示这份工作区缺料。

### 3.4 输出：扁平目录 + `resolution.json`

```
<flat_dir>/
├── main.pdf  main.tex  main.md         # 主交付物（main.md 由摄入工具从 PDF 转出）
├── fig_*.png × 7                        # 图件本体
├── tab_*.tex / tab_*.csv × 9            # 表格：结构 + 数值
├── DECISION_LOG.md  VERIFICATION_REPORT.md  ... × 5
└── resolution.json                      # 索引
```

`resolution.json` 的键：

| 键 | 含义 |
|---|---|
| `primary` | 恒定路径：`main_tex` / `main_pdf` / `assignment_profile` |
| `read` | 按 need 分组的来源文件（上表 3.3） |
| `assets.figures` / `assets.tables` | 每条的 `file` / `ext` / `stem` / `caption` / `alt`，以及 `count`、`mode` |
| `unavailable` | 清单声明要、但工作区里缺失的 need |
| `missing_assets` | 论文声明引用了、但 `necessary_materials/` 里找不到的图或表 |
| `dead` | 素材目录里有、但论文从未声明的文件（多半是废弃件） |
| `unknown` | `unknown-scan` 区域里清单外的 md/json —— **只登记不读取**，供事后 review 清单缺口 |
| `audit.resolver_read` | 除主交付物外，解析器实际读过的文件 |

**路径都是裸文件名** —— 正是技能 `import-sources` 之后在 `sources/` 里看到的样子。

### 3.5 硬门与排除

- **硬门**：`output/main.tex` 不存在 → 直接退出并报
  `上游未产出 output/main.tex —— 管线未完成，不应产稿`。
  **宁可不做，也不要拿半成品产稿。**
- **排除**：`codes/**`、`__pycache__`、编译日志（`.log/.aux/.bbl/.out`）、
  `contracts/`、`library/`、`archive/`、以及几份管线内部笔记。
- **`unknown-scan`**：只在根目录与 `refine-logs/` 找清单外的 `*.md` / `*.json`，
  **找到只登记，不读取** —— 用来发现"清单漏了什么"。

---

## 4. 怎么用

### 4.1 先探一遍（不落盘）

```bash
python3 skills-academic/ppt-master/scripts/resolve_sources.py <workspace> --json
```

看三件事：

- `unavailable` 是否为空 —— 不为空说明工作区缺料
- `missing_assets` 是否为空 —— 不为空说明论文引用的图/表没找到
- `unknown` 里有什么 —— 值得的话补进清单

### 4.2 落盘并建项目

```bash
# 铺成扁平目录
python3 skills-academic/ppt-master/scripts/resolve_sources.py <workspace> --stage <flat_dir>

# 建项目（不带 --format，画布在确认页决定）
python3 skills-academic/ppt-master/scripts/project_manager.py init <project_name>

# 摄入（--copy：保留扁平目录，便于复跑）
python3 skills-academic/ppt-master/scripts/project_manager.py import-sources <project> <flat_dir> --copy

# 体检
python3 skills-academic/ppt-master/scripts/project_manager.py validate <project>
```

`validate` 此时会报两条 warn（缺 `design_spec.md`、`svg_output/` 为空）—— **正常**，
那是 Step 4 与 Step 6 才产出的东西。

### 4.3 然后照常走 Default Generate

解析器只管**备料**。备好之后就是标准流程：

```
Step 3  模板候选（技能内部准备）
Stage 1 确认沟通契约 + 从零设计/套用模板   ← 写 recommendations.stage1.json 后起确认页
Stage 2 最终方案打磨 + 各节                 ← 写 recommendations.stage2.json
Step 4  design_spec.md + spec_lock.md
Step 5  图片（image_usage 含 ai 时才需要）
Step 6  逐页 SVG → 质检 → finalize_svg.py → 讲者备注
Step 7  svg_to_pptx.py 导出
```

完整命令与闸门由 [`skills-academic/ppt-master/workflows/generate-pptx.md`](skills-academic/ppt-master/workflows/generate-pptx.md) 拥有，本文不重复。

### 4.4 一条实测过的完整链路

```bash
SK=skills-academic/ppt-master

# ① 解析
python3 $SK/scripts/resolve_sources.py <workspace> --stage <flat_dir>

# ② 建项目 + 摄入
python3 $SK/scripts/project_manager.py init cc_inventory_defense
python3 $SK/scripts/project_manager.py import-sources <project> <flat_dir> --copy

# ③ Stage 1 确认页
python3 $SK/scripts/confirm_ui/server.py <project> --port 5070 --timeout 0 --daemon
#    → 用户在页面上确认；随后写 recommendations.stage2.json

# ④ 生成与导出
python3 $SK/scripts/svg_quality_checker.py <project> --canonical-authoring --stage final --json
python3 $SK/scripts/finalize_svg.py <project>
python3 $SK/scripts/svg_to_pptx.py <project>
```

---

## 5. 清单怎么改

`scripts/source_manifest.json` 是**贡献者白名单**，不是存在性清单 ——
不在清单里、也不匹配 `exclude` 的文件一律不读。

| 段 | 用途 | 改它的时机 |
|---|---|---|
| `fixed` | 恒定路径，技能自己会读 | 上游换了主交付物路径 |
| `conditional` | 过程文档 → 契约字段的映射 | 上游多了/少了一份过程文档 |
| `needs` | 技能需要哪些字段来源 | 确认页字段变了 |
| `assets` | 素材目录、扩展名偏好、是否暂存备选 | 上游素材目录改名，或新增一类素材 |
| `unknown-scan` | 找清单外文件的区域 | 想扩大"漏检"的覆盖范围 |
| `exclude` | 显式排除 | 出现新的内部产物噪音 |

**加了新目录后，先跑 `--json` 看 `unknown` 与 `missing_assets` 的变化，再决定要不要改清单。**

---

## 6. 测试

```bash
python3 -m unittest discover -s skills-academic/ppt-master/scripts/tests -t skills-academic/ppt-master/scripts/tests -p 'test_source_resolution.py'
```

`test_source_resolution.py` 共 30 个用例，覆盖声明解析、stem 去重、
扩展名偏好、题注提取、`stage-alt` 行为、`unavailable` / `missing_assets` / `unknown` 判定、
以及硬门（缺 `main.tex` 时必须报错退出）。

---

## 7. 已知限制

| 限制 | 现状 |
|---|---|
| **pandoc 不是依赖，但也没有** | 环境里没装 pandoc，`.tex` 不会被转成 markdown。**不影响结果**：PDF→markdown 已带全部数值（含表格行），且 `.tex`/`.csv` 原件都在 `sources/` 里可直接读 |
| **只认 LaTeX 声明** | 图件与表格必须由 `main.tex` 的 `\input{}` / `\includegraphics{}` 声明。手写进 `necessary_materials/` 却未被论文引用的素材不会进暂存区（会出现在 `dead` 里） |
| **`assignment_profile.json` 可选** | 缺失不报错。它的字段供技能参考，不是硬门 |
| **清单路径与工作区强耦合** | 上游改目录名就得同步改清单。目前靠 `--json` 的 `unknown` / `missing_assets` 兜底发现 |
| **确认页端口** | 别用 5060/5061 —— 那是 SIP 端口，Chromium 系浏览器一律拒连（`ERR_UNSAFE_PORT`）。5070 可用 |
