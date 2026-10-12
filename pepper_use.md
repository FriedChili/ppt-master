# 对接 Pepper 工作区

本文说明**如何把一份 Pepper 上游工作区喂给 `skills-academic/deck`**：
为什么需要这一步、工作区长什么样、解析器怎么做、命令怎么跑、哪些设计被放弃了。

> **本文不含任何具体课题内容。** 存在性数据来自 **4 个真实生产会话备份**的普查；
> 目录名与规则引文取自上游代码（`worker/plugins/pepper-orchestrator/src/`）。
>
> 分支层面的其余改造（确认页文案、Stage 2 入口二选一、色彩方案重构、模板 spec 英文化等）
> 与 Pepper 无关，见 [`skills-academic/deck/FORK.md`](skills-academic/deck/FORK.md)。

---

## 0. 一页结论

**问题**：作业管线已经产出中间件，但 PPT 技能默认只吃「最终论文」，导致：

1. 答辩稿缺防守层 —— 讲清了「是什么」，讲不了「为什么」；
2. 更严重：**会编造或误述事实**（对照实测首版 5 处缺陷，其中 3 处为实质性错误）。

**架构**：**声明式来源清单 + 运行时解析器**。

> 技能侧持有一份**来源清单**（描述"什么对 PPT 有贡献、各自什么含义、能满足什么需求"），
> 运行时**探测实际产物**并与之比对，产出一份**已解析的供给简报**，技能再按需消费。

判断从散落的 `if exists` 逻辑变成**数据**：管线加了新产物，改清单而不是改技能。

```bash
SK=skills-academic/deck
python3 $SK/scripts/resolve_sources.py <workspace> --stage <flat_dir>   # 探测 + 铺成扁平目录
python3 $SK/scripts/project_manager.py init <project_name>              # 建项目
python3 $SK/scripts/project_manager.py import-sources <project> <flat_dir> --copy   # 摄入
```

**四条经实测确立的前提**：

> **前提一：不读 `contracts/`。** 它是模块间通信的传输层（代码注释：*"never the contract"*），
> 内容在散文与 `.tex` 中有可用对应物，且只有 2/4 会话存在。
>
> **前提二：稳定载体是 `refine-logs/` 的散文与 `necessary_materials/` 的素材**（均 4/4）。
>
> **前提三：页面名册必须是解析结果的函数**（四份样本形态差异极大）。
>
> **前提四：不存在写作模块**（`pepper_write` 已删除）→ **没有 `structure_plan.json`**。

---

## 1. 为什么需要它：只喂论文会错在哪

同一份作业素材，首版只喂最终论文，二版接入中间件；两版页数与版式结构相同。

### 1.1 首版的五类缺陷

| 缺陷类型 | 表现 | 为什么「只喂论文」必然发生 |
|---|---|---|
| **编造** | 把「研究缺口」写成了论文里并不存在的说法 | 正文写的是「我做了什么」，缺口只在综述与定位段 |
| **误述** | 把「在本维度下不可解释的检验」写成「检验未通过」 | 该判断只在验收记录里 |
| **重复计算** | 把与基准**完全等价**的设定当成独立证据 | 等价性由验收记录点破 |
| **标签冲突** | 同一标签在两页指代**不同分组** | 分组口径差异记在方法说明里 |
| **细节失真** | 数据缺失年份范围写错 | 正确口径只在与文档不符的核对记录里 |

**共同特征：五处全都不在论文正文的显眼位置。** 不是能力问题，是信息不在那里。

### 1.2 二版的升级

补上**对标**、**「为什么」**、**自我边界**、**验证层**，并修正上述三类错误。
**中间件首先改善的是「正确性」，其次才是「深度」。**

### 1.3 图注的正确来源

首版曾**自己编造图注**。实测对照：

| 情形 | 图注在哪 |
|---|---|
| 有 `visualization.json` 的样本 | 契约里是**完整版**；`.tex` 的 `\caption{}` 是**短版**；论文正文补充单位与来源 |
| **没有**该契约的样本 | orchestrator **直接在 `main.tex` 里写出完整图注** |

**结论**：图注来源 = **`tables/*.tex` 的 `\caption{}` + 论文正文对应段落**，与契约无关。
对 PPT 而言短版图注即足够，单位与口径从正文取。

---

## 2. 上游工作区长什么样

### 2.1 目录约定（取自上游 `PATH_ACCESS_RULES`）

```
<workspace>/
├── assignment_profile.json          # 作业元信息（ONLY 在工作区根）
├── output/                          # 交付物 ONLY 在这里
│   ├── main.tex                     # ★ 硬门
│   ├── main.pdf
│   └── results/*.csv
├── necessary_materials/             # 图表与参考文献 ONLY 在这里
│   ├── figures/                     # 图件（png / pdf / svg 混存）
│   ├── tables/                      # 表格（tex / csv / md 混存）
│   └── references.bib
├── refine-logs/                     # 每模块日志 ONLY 在这里
│   ├── DECISION_LOG.md
│   ├── VERIFICATION_REPORT.md
│   ├── LITERATURE_REVIEW.md
│   ├── METHOD_UNDERSTANDING.md
│   └── EXPERIMENT_PLAN.md
├── codes/                           # 源码 ONLY 在这里
├── dois/  library/  contracts/      # 文献原文 / 传输层
└── logs/  archive/                  # logs 永不读写；archive 永不写入
```

**目录名不是硬约束**：清单里的路径可按需改。硬约束只有两条：
`output/main.tex` 必须存在，且清单里写的路径必须与工作区实际一致。

### 2.2 命名稳定性 —— 决定清单必须两层匹配

| 组 | 不同文件名 | 单名最高命中 | 匹配方式 |
|---|---|---|---|
| `refine-logs/*.md` | **8** | 4 个 **4/4** | ✅ **按精确文件名** |
| `contracts/*.json` | 3 | 2/4 | （不读） |
| `necessary_materials/tables/*` | **49** | 每个 **1/4** | ❌ 按目录 + 扩展名枚举 |
| `necessary_materials/figures/*` | **28** | 每个 **1/4**（前缀 100% = `fig`） | ❌ 同上 |
| `output/results/*` | **24** | 最高 2/4 | ❌ 同上 |

> **结论**：`refine-logs/` 名字稳定可精确匹配；**素材目录的名字完全不可预测**。
> **按文件名写全清单必然失效。**

### 2.3 `refine-logs/` 实测命中率

| 文件 | 命中 | 平均 | 最大 | 角色 |
|---|---|---|---|---|
| `DECISION_LOG.md` | **4/4** | 7.9 KB | 10.5 KB | 决策与残留记录 —— 答辩的「为什么」主源 |
| `EXPERIMENT_PLAN.md` | **4/4** | 9.6 KB | 15.4 KB | 先于代码写定的设计书 |
| `LITERATURE_REVIEW.md` | **4/4** | 7.8 KB | 14.3 KB | 定位、缺口、对标 |
| `VERIFICATION_REPORT.md` | **4/4** | 10.7 KB | 17.7 KB | 自检/独立验收 —— 追问清单主源 |
| `ORCHESTRATOR_COMPACT.md` | 3/4 | **23.0 KB** | **25.6 KB** | ⛔ **必须排除** |
| `METHOD_UNDERSTANDING.md` | 3/4 | 9.5 KB | 18.3 KB | 理论/方法参考 |
| `experiment_run_report.md` | 2/4 | 5.9 KB | 8.5 KB | 运行报告 |
| `VIZ_DATA_NOTES.md` | 2/4 | 15.1 KB | 24.8 KB | 列级数据说明 |

> `ORCHESTRATOR_COMPACT.md` 平均 23 KB，在某份样本里占 `refine-logs` 总量的 **43%**。
> 读它是纯浪费。

### 2.4 `contracts/` —— 决定不读

`module-tools.ts` 的注释：*"files are a materialized view for audit/delivery, **never the contract**"*。

**实测**：命中 2/4；出现不规则（有 `LITERATURE_REVIEW.md` 却无 `litReview.json`）；
内容在 `VERIFICATION_REPORT.md` / `DECISION_LOG.md` / `EXPERIMENT_PLAN.md` 中有语义等价物。

### 2.5 素材目录：4/4，但**不要枚举 —— 要用正文的声明**

| 目录 | 命中 | 实测形态 |
|---|---|---|
| `necessary_materials/figures/` | **4/4** | 4–8 文件，555–1118 KB；**PNG 与 PDF 可能双份并存** |
| `necessary_materials/tables/` | **4/4** | 6–22 文件；**可能 `.csv`+`.md`+`.tex` 三格式并存** |
| `output/results/` | 3/4 | 7–12 CSV + `experiment_summary.json` |
| `output/main.tex` · `main.pdf` | **4/4** | 交付物本体 |
| `assignment_profile.json` | **4/4** | 工作区根 |

#### ⭐ 关键实测：正文声明的图表 vs 目录实际

`main.tex` 用 `\input{...tables/...}` 与 `\includegraphics{...}` **显式声明了它用了哪些图表**。

| 样本 | 正文声明表 | 目录实际表 | **死产物** | 声明图 | 目录实际图 | 死产物 |
|---|---|---|---|---|---|---|
| S1 | 6 | 6 | **0** | 4 | 4 | 0 |
| **S2** | **0** | **14** | **14** ⚠️ | 8 | 8 | 0 |
| S3 | 6 | 6 | **0** | 4 | 4 | 0 |
| S4 | 11 | 11 | **0** | 8 | 8 | 0 |

**结论：图表的解析依据是正文声明，不是目录枚举。**

- 三份样本声明数与目录数**完全一致** → 声明可靠
- **S2 的 14 个 `.tex` 全是死产物** —— 该作业的表**内联**在正文里，`.tex` 只是中间片段。
  按目录枚举会白读 14 个文件
- 声明顺序即**论文的叙述顺序**，可直接用作页序
- 每个 `\input` 附近的 `\caption{}` 就是该图表的图注

> **⚠️ 同 stem 多扩展名仍须分组去重**：天真枚举会把 4 张图数成 8 张。
> **扩展名偏好**：图 `png > pdf > svg`；表格优先取 `.tex`（含 caption），
> **需要原生表格数值时才按需取同 stem 的 `.csv`**。

### 2.6 关键实测：`METHOD_UNDERSTANDING` / `EXPERIMENT_PLAN` 能否砍掉？

**假设**：论文正文既然完整，这两份的「为什么」是否已被覆盖、可以省略？

**测法**：抽出带理由标记的句子（R），再测其中**正文中术语几乎不出现**的（M）。
`M/R` 即「真正的边际贡献」占比。

| 样本 | 文件 | R | **M** | **M/R** |
|---|---|---|---|---|
| S1 数据驱动 | `EXPERIMENT_PLAN.md` | 27 | **24** | **89%** |
| S2 习题 | `METHOD_UNDERSTANDING.md` | 6 | 1 | 17% |
| S3 毕业论文 | `METHOD_UNDERSTANDING.md` | 20 | **12** | **60%** |
| S3 毕业论文 | `EXPERIMENT_PLAN.md` | 30 | **25** | **83%** |
| S4 硕士报告 | 两份 | 4 / 2 | 0 | 0% |

**结论：不可砍。** 两份"重"样本中 83–89% 的理由在正文中缺席，抽样内容均为答辩要害
（识别策略的维度约束、组内变异过小必须写入局限、稳健性预期、理论基准）。

> **成本对照**：这两份合计约 19 KB ≈ 7K tokens，换来 60–89% 的独有理由 —— **划算**。
> 真正的浪费在 `codes/`（1617 KB）、`contracts/`（47–78 KB）、`ORCHESTRATOR_COMPACT.md`（23 KB），
> 而这些**已全部排除**。

### 2.7 `assignment_profile.json`（4/4）

```jsonc
{ "deliverableType", "topic", "targetLength", "formatRequirements[]",
  "citationStyle", "language", "attachments[{name, role}]", "constraints[]", "source" }
```

**`deliverableType` 是自由文本，不是枚举** —— 四份样本四种自然语言写法。
`constraints[]` 同为自由文本，但信息密度高（语言、结构、数据真实性、篇幅要求）。

### 2.8 三类典型作业的实测形态

| 类型 | 会有 |
|---|---|
| 数据驱动型 | `refine-logs` 全套 + 图表 + `output/results/` |
| 习题/代码型 | `refine-logs` 全套 + 图表 + `codes/`；**无 `output/results/`** |
| 写作型 | `refine-logs` 全套 + 图表 |

> **即使最"轻"的样本，`refine-logs` 四件套与图表目录依然齐备。**

### 2.9 模块条件性

`litReview` *"USE ONLY when the assignment requires academic literature"*；
`experiment` *"**YOUR judgment, not an obligation**"*、*"**NEVER for essays/case studies**"*；
`visualization` *"USE ONLY when experiment actually ran"*；**写作无模块**。

> §2.2–2.5 的命中率差异正是这些条件性的直接后果。

---

## 3. 为对接做的适配

| # | 适配点 | 说明 |
|---|---|---|
| 1 | **新增解析器** | `scripts/resolve_sources.py` + `scripts/source_manifest.json`。声明式清单，确定性执行，**不调用模型** |
| 2 | **技能侧零改动** | 解析器产出**扁平目录**，正好是 `import-sources` 本来就接受的形态。不改 `source_to_md.py`、不改 `import-sources`、不改任何 ingest 路径 |
| 3 | **绕开 pandoc 依赖** | 图件优先取位图本体（png），表格同时带上 `.tex`（结构与题注）与 `.csv`（原生数值）——**两者都不触发 LaTeX 转换** |
| 4 | **只读声明，不猜命名** | 图件与表格的名字不可预测，因此**从论文自己的 `\input{}` / `\includegraphics{}` 声明反查**，而不是枚举目录 |
| 5 | **管线产出即事实源** | 论文正文（PDF→markdown）承担全部数值；图注取自浮动环境；`refine-logs/` 的五份文档提供契约字段的措辞依据 |

### 3.1 被放弃的设计（**重要**）

早期设计（v5–v7）含三条**技能侧改动**，最终**全部未实施**，因为扁平暂存方案让它们变得不必要：

| 原计划 | 现状 |
|---|---|
| 改 `workflows/generate-pptx.md` Step 1，加"若给了上游工作区先跑 resolver" | ✗ **未做** —— 解析器是独立命令，由调用方显式执行 |
| 改 `references/strategist.md`，加"理由层"规则（方法页/局限页/追问页的来源） | ✗ **未做** —— 理由层已由 `refine-logs/` 的文档本身进入 `sources/`，技能照常摄入 |
| 改 `references/plan-core.md`，名册按 `resolution.json` 生成 | ✗ **未做** —— 页面名册仍由 Strategist 按常规流程推导 |

同样被放弃的还有：

| 原设计 | 实际实现 | 原因 |
|---|---|---|
| `resolution.json` 带 `scenario` / `level`（T0–T3） / `degraded` / `resolved` | 简化为 `primary` / `read`（按 need 分组）/ `assets` / `unavailable` / `missing_assets` / `unknown` | 等级与降级链在实现中未产生真实分支；`needs ↔ conditional` 的反向索引已覆盖同一诉求 |
| CLI `--project <project_path>`（解析器直接物化进项目） | CLI `--stage <flat_dir>`（只铺扁平目录） | 让解析器与技能解耦：解析器只备料，摄入由 `import-sources` 负责 |
| `resolution.log` 作为读取日志 | 并入 `resolution.json` 的 `audit.resolver_read` | 少一个文件 |
| `scenario` 分类（`deliverableType` → 六类场景） | 不做分类 | Stage 1 的契约字段由 AI 写推荐值、用户确认，不需要分类器 |
| 页面名册按 `resolution` 生成 | 不做 | 同上 |
| `scripts/docs/source-resolution.md` 过程说明 | 未单独成文 | 本文承担该职责 |

> **判断修正史见附录。**

---

## 4. 解析器原理

### 4.1 它回答两个技能自己回答不了的问题

1. **哪些上游产物值得读？** —— 其余都是噪音（代码、契约、构建日志、管线内部笔记）。
2. **图件和表格到底是什么？** —— 它们的名字不可预测。

### 4.2 清单是**贡献者白名单**，不是存在性清单

> **设计反转（关键）**：清单**不描述"可能有什么"**，只描述**"什么对 PPT 有贡献"**。
> 不在清单里的一律不读 —— **默认拒绝，而非默认枚举**。

理由：`codes/` 有 39 个文件 1617 KB、`__pycache__` 一堆、编译垃圾 30+ KB。
这些**永远不会出现在 PPT 里**，告诉技能"它们存在"是纯浪费。

**全部条目**（`fixed` + `conditional` + `assets`）：

| id | 路径 | 匹配 | 角色 |
|---|---|---|---|
| `assignment_profile.json` | 工作区根 | exact | meta |
| `output/main.tex` | exact | exact | 主张 · 结构 · 论证 · 图注 · **图表声明** · 页序 |
| `output/main.pdf` | exact | exact | 主交付物（正文与数值的事实源） |
| `decision-log` | `refine-logs/DECISION_LOG.md` | exact | 「为什么」· `communication_intent` |
| `verification` | `refine-logs/VERIFICATION_REPORT.md` | exact | 追问清单 · `audience_outcome` · 可靠性 |
| `lit-review` | `refine-logs/LITERATURE_REVIEW.md` | exact | 缺口 · 对标 · 定位 |
| `method-understanding` | `refine-logs/METHOD_UNDERSTANDING.md` | exact | 机制页 · 方法理由 |
| `experiment-plan` | `refine-logs/EXPERIMENT_PLAN.md` | exact | 设计理由 |
| `figures` | **正文 `\includegraphics{}` 声明的那些** | declared | 图页 |
| `tables` | **正文 `\input{}` 声明的那些** | declared | 表页 · 图注 |

**明确排除**（不进清单，也不探测）：

| 产物 | 实测体量 | 为什么无贡献 |
|---|---|---|
| `codes/**` | S1 **1617 KB** / 39 文件 | 代码不进 PPT |
| `**/__pycache__/**` · `*.pyc` | 多个 | 字节码 |
| `output/*.log` · `.aux` · `.bbl` · `.out` | 30+ KB | 编译垃圾 |
| `dois/**` · `library/**` | — | 文献原文 PDF |
| `contracts/**` | 47–78 KB | 传输层（§2.4） |
| `logs/**` · `archive/**` | — | 上游规定永不读写 |
| `refine-logs/ORCHESTRATOR_COMPACT.md` | 平均 **23 KB** | 管线内部编排 |
| `refine-logs/VIZ_DATA_NOTES.md` | 平均 15 KB | 列级 dtype/nan 统计 |
| `refine-logs/experiment_run_report.md` | 平均 5.9 KB | 运行日志 |
| **未被正文声明的 tables** | S2 有 **14 个** | 死产物（§2.5） |

> **修正**：早期版本把 `VIZ_DATA_NOTES.md` 等标为「按需」。
> **这是错的 —— 它们没有"需"。** 应直接排除，而不是留一个永远不会触发的分支。

### 4.3 图件与表格：从声明反查，按主名去重

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
  LaTeX 外壳（`$`、`\_`、`\textbf{}`）只做**无损**剥离，任何需要判断语义的都不动 ——
  那属于技能侧。

### 4.4 契约字段：`needs` ↔ `conditional` 反向索引

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

### 4.5 输出：扁平目录 + `resolution.json`

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
| `read` | 按 need 分组的来源文件（§4.4） |
| `assets.figures` / `assets.tables` | 每条的 `file` / `ext` / `stem` / `caption` / `alt`，以及 `count`、`mode` |
| `unavailable` | 清单声明要、但工作区里缺失的 need |
| `missing_assets` | 论文声明引用了、但 `necessary_materials/` 里找不到的图或表 |
| `dead` | 素材目录里有、但论文从未声明的文件（多半是废弃件） |
| `unknown` | `unknown-scan` 区域里清单外的 md/json —— **只登记不读取**，供事后 review 清单缺口 |
| `audit.resolver_read` | 除主交付物外，解析器实际读过的文件 |
| `staged` | 实际复制进扁平目录的文件名 |

**路径都是裸文件名** —— 正是技能 `import-sources` 之后在 `sources/` 里看到的样子。

### 4.6 清单外策略

```jsonc
"unknown-scan": { "roots": ["", "refine-logs"], "patterns": ["*.md", "*.json"] }
```

**为什么仍需记录**：清单一定不完整 —— 4 份样本里就出现了起草时未预见的
`VIZ_DATA_NOTES.md`、`experiment_run_report.md`、`ORCHESTRATOR_COMPACT.md`。
记录清单外文件，供事后**判断它们该进白名单还是黑名单**，但不影响本次运行。

**默认行为是「不读」**，所以漏判的代价是少一个来源，不是多烧 context。

### 4.7 前置门

```
output/main.tex 缺失  →  阻断，报「上游未产出 output/main.tex —— 管线未完成，不应产稿」
```

**宁可不做，也不要拿半成品产稿。**

> 早期设计还有第二道门：从 `VERIFICATION_REPORT.md` 的结论行解析阻断性判断。
> 该门**未实施** —— 不读契约后它失去了结构化依据，按设计已降级为"启发式提示，不得据此误阻断"，
> 而启发式提示无法机械判定，因此留给人看。

---

## 5. 怎么用

### 5.1 先探一遍（不落盘）

```bash
python3 $SK/scripts/resolve_sources.py <workspace> --json
```

看三件事：

- `unavailable` 是否为空 —— 不为空说明工作区缺料
- `missing_assets` 是否为空 —— 不为空说明论文引用的图/表没找到
- `unknown` 里有什么 —— 值得的话补进清单

### 5.2 落盘并建项目

```bash
# 铺成扁平目录
python3 $SK/scripts/resolve_sources.py <workspace> --stage <flat_dir>

# 建项目（不带 --format，画布在确认页决定）
python3 $SK/scripts/project_manager.py init <project_name>

# 摄入（--copy：保留扁平目录，便于复跑）
python3 $SK/scripts/project_manager.py import-sources <project> <flat_dir> --copy

# 体检
python3 $SK/scripts/project_manager.py validate <project>
```

`validate` 此时会报两条 warn（缺 `design_spec.md`、`svg_output/` 为空）—— **正常**，
那是 Step 4 与 Step 6 才产出的东西。

### 5.3 然后照常走 Default Generate

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

完整命令与闸门由 [`skills-academic/deck/workflows/generate-pptx.md`](skills-academic/deck/workflows/generate-pptx.md) 拥有，本文不重复。

### 5.4 一条实测过的完整链路

```bash
SK=skills-academic/deck

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

## 6. 清单怎么改

`scripts/source_manifest.json` 是**贡献者白名单**。不在清单里、也不匹配 `exclude` 的文件一律不读。

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

## 7. 验收标准与测试

### 7.1 验收判据

| # | 判据 | 检查方式 |
|---|---|---|
| **A1** | **能发现首版的五类缺陷** | 同一素材重跑，检查是否还犯 §1.1 的五类错 |
| **A2** | **无实验时也能跑** | 用写作型/习题型样本跑一次（无 `output/results/`） |
| **A3** | **无新增编造** | 页面每个数字都能在 T0–T3 中找到 |
| **A4** | **图注来自素材** | 逐条核对 = `\caption{}` 或 `main.tex` 对应段 |
| **A5** | **降级可见** | `unavailable` 项有对应提示 |
| **A6** | **不重复计数** | 4 张图不得解析成 8 张（stem 去重生效） |
| **A7** | **不读无贡献产物** | `audit.resolver_read` 中不得出现：`codes/` · `contracts/` · `__pycache__` · `ORCHESTRATOR_COMPACT.md` · `VIZ_DATA_NOTES.md` · `experiment_run_report.md` · 编译垃圾 |
| **A8** | **不读死产物** | 用 S2 型样本（表内联）跑一次：**不得读取任何未被正文声明的 `.tex`** |

**A2 与 A6 是硬指标。** A7/A8 可机械检查（扫 `audit.resolver_read` 与 `dead`），
是"不浪费上下文"这一诉求的直接验收。

### 7.2 测规则，不测样本

> **为什么不冻结样本输出**：4 份测试样本的作业内容高度局限，
> 冻结它们等于把**不具代表性的样本固化成设计约束** —— 清单该扩展时快照反而成为阻力。
> 样本的作用是**发现问题的形状**，不是**验证解法**。

| 层 | 手段 | 验什么 |
|---|---|---|
| **单元** | `scripts/tests/test_source_resolution.py`，**构造的目录树**，每个 fixture 只考一条规则 | 精确匹配 · 声明解析 · stem 去重 · 扩展名偏好 · 题注提取 · `stage-alt` · 排除规则 · `unavailable` / `missing_assets` / `unknown` 判定 · 硬门 |
| **性质** | 不变量断言，不比对快照 | ① 不读 `codes/` ② 图数 == 正文声明数 ③ 无同 stem 重复项 ④ 同一输入两次运行结果一致 |
| **冒烟** | 真实工作区仅作**输入**，跑通即可 | 不崩溃、输出结构合法、`unavailable` / `missing_assets` 字段存在 |
| **生产** | 真实运行积累 `unknown` | 清单**哪里不完整** —— 前瞻性机制，不是回归机制 |

**单元 fixture 是构造的**，因此可以覆盖样本没覆盖的形态 ——
无图作业、纯文献作业、多语言、短论文、上游半途中止。**这些是样本给不了的。**

```bash
python3 -m unittest discover -s skills-academic/deck/scripts/tests \
  -t skills-academic/deck/scripts/tests -p 'test_source_resolution.py'
# Ran 30 tests ... OK
```

---

## 8. 已知限制与风险

### 8.1 限制

| 限制 | 现状 |
|---|---|
| **pandoc 不是依赖，但环境里也没有** | `.tex` 不会被转成 markdown。**不影响结果**：PDF→markdown 已带全部数值（含表格行），且 `.tex`/`.csv` 原件都在 `sources/` 里可直接读 |
| **只认 LaTeX 声明** | 图件与表格必须由 `main.tex` 的 `\input{}` / `\includegraphics{}` 声明。手写进 `necessary_materials/` 却未被论文引用的素材不会进暂存区（会出现在 `dead` 里） |
| **`assignment_profile.json` 可选** | 缺失不报错。它的字段供技能参考，不是硬门 |
| **清单路径与工作区强耦合** | 上游改目录名就得同步改清单。目前靠 `--json` 的 `unknown` / `missing_assets` 兜底发现 |
| **`deliverableType` 自由文本** | 四份样本四种写法。**当前不做分类** —— Stage 1 的契约字段由 AI 写推荐值、用户确认 |
| **确认页端口** | 别用 5060/5061 —— 那是 SIP 端口，Chromium 系浏览器一律拒连（`ERR_UNSAFE_PORT`）。5070 可用 |

### 8.2 风险与对策

| 风险 | 对策 |
|---|---|
| **`core_message` 单点故障** | 即便全自动也**露出该字段单独确认**（Stage 1 必填） |
| **清单腐化** | `unknown-scan` 记录但不读取；每次运行按 `unknown` 反哺 |
| **天真枚举导致重复** | `group-by: stem` + `ext-preference`（§4.3） |
| **误读 `contracts/`** | ⛔ 列入 `exclude` |
| **误读 `ORCHESTRATOR_COMPACT.md`** | ⛔ 列入 `exclude` |
| **条件产物缺失被当成「没有内容」** | 进 `unavailable`，在确认与写作时可见；缺产物不阻断 |
| **上游半途中止** | 硬门：缺 `output/main.tex` 直接退出 |

### 8.3 上游侧可选改动（未实施）

1. `AssignmentProfile` 增加可选枚举 `scenario?`
2. 论文自我定位句作为可选字符串字段输出

---

## 附录 A：证据出处

| 结论 | 来自 |
|---|---|
| **命名稳定性数据**（§2.2） | **4 份样本普查** |
| **素材同 stem 多扩展名**（§2.5） | 同上 |
| **契约不读**（§2.4） | 代码注释 *"never the contract"* + 命中 2/4 + 对应物核验 |
| **图注来源**（§1.3） | 契约 caption 与 `\caption{}` 并排对照 + 无契约样本的 `main.tex` 图注 |
| 目录归属规则（§2.1） | `module-tools.ts` · `PATH_ACCESS_RULES` |
| 模块条件性 · 无写作模块（§2.9） | `orchestrator-persona.ts` · `pepper-plugin.ts` |
| 五类内容缺陷（§1.1） | 对照实测 |

> ⚠️ **关于 §2 的数据**：存在性比例、命名统计、`M/R` 比值均来自 **4 份测试样本**。
> 它们的作业内容**高度局限**，足以**确立问题的形状**（产物条件存在、素材名不可预测、
> 声明与目录可能不一致、契约冗余），**但不足以量化**这些现象的真实分布。
> 因此凡引用这些比例处，均作**指示性**而非**已确立**解读；
> **实现与验收不得依赖具体数值**，只依赖由此推出的**判定规则**。

## 附录 B：判断修正史

| 版本 | 判断 | 修正依据 |
|---|---|---|
| v1 | 新建 `roles.json` + `defense-brief.json` | — |
| v2 | 取消新文件；字段已在 `contracts/*.json` | 读上游代码 |
| v3 | 产物条件存在；无写作模块 | 用户提醒 + 读 persona |
| v4 | 不读 `contracts/`；散文与素材是基线 | 4 份样本普查 |
| v5 | 声明式清单 + 运行时解析器；两层匹配；stem 去重 | 命名稳定性实测 |
| **v6** | **清单改为「贡献者白名单」；图表按正文声明解析；明确排除无贡献产物** | **用户指出"存在 ≠ 有贡献"** |
| **v7** | **取消样本快照；改为「测规则不测样本」；§2 数据降级为指示性** | **用户指出样本作业内容局限，仅供调研参考** |
| **v8** | **落定为扁平暂存 + 技能侧零改动；放弃三条技能侧接入、`level`/`degraded` 分级与场景分类** | **实现中发现分级未产生真实分支，且扁平目录已满足摄入需求** |

> **v7 的教训**：样本帮我**发现了问题的形状**（条件存在、命名不稳、声明≠目录、契约冗余），
> **但不能验证解法**。把样本输出冻结成基线，等于把不具代表性的样本固化成设计约束。
> **发现用样本，验证用构造的 fixture，校准用生产日志。**
>
> **v8 的教训**：设计文档里的"三层接入 + 分级解析"最终没有产生真实分支。
> **能用一个更简单的形态满足同一诉求时，先做简单的那一个** ——
> 扁平暂存让技能侧一行都不用改，这比任何分级机制都更可靠。

---

## 附：本文不含的内容

样本的选题、数据、文献与路径均**未写入本文**；`deliverableType` 仅以「四份样本写法各异」的方式提及。
目录名、字段名与规则引文均取自上游代码，属于管线设计的一部分。
