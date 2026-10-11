# 学术作业管线对接设计

> 本文是 `skills-academic/ppt-master`（学术专用分支）与上游写作管线（Pepper）的对接设计。
> 目标读者：维护这条管线的人。
>
> **本文不含任何具体课题内容。** 存在性数据来自 **4 个真实生产会话备份**的普查；
> 目录名与规则引文取自上游代码（`worker/plugins/pepper-orchestrator/src/`）。

---

## 0. 一页结论

**问题**：作业管线已经产出中间件，但 PPT 技能默认只吃「最终论文」，导致：

1. 答辩稿缺防守层 —— 讲清了「是什么」，讲不了「为什么」；
2. 更严重：**会编造或误述事实**（对照实测首版 5 处缺陷，其中 3 处为实质性错误）。

**架构**：**声明式来源清单 + 运行时解析器**。

> 技能侧持有一份**来源清单**（描述"可能有什么、各自什么含义、能满足什么需求"），
> 运行时**探测实际产物**并与之比对，产出一份**已解析的供给简报**，技能再按需消费。

这样把判断从散落的 `if exists` 逻辑变成**数据**：管线加了新产物，改清单而不是改技能。

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

## 1. 实测结论（内容层面）

同一份作业素材，首版只喂最终论文，二版接入中间件；两版页数与版式结构相同。

### 1.1 首版的缺陷（按类型归类）

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

## 2. 上游事实（4 份样本调研 + 代码）

> ⚠️ **关于 §2 中的数据**：存在性比例、命名统计、`M/R` 比值均来自 **4 份测试样本**。
> 它们的作业内容**高度局限**，足以**确立问题的形状**（产物条件存在、素材名不可预测、
> 声明与目录可能不一致、契约冗余），**但不足以量化**这些现象的真实分布。
>
> **因此**：文中凡引用这些比例处，均作**指示性**而非**已确立**解读；
> **实现与验收不得依赖具体数值**，只依赖由此推出的**判定规则**。
> 真实分布应由**生产运行日志**逐步积累（§3.2.4 的 `unknown_policy`）。

### 2.1 命名稳定性 —— **决定清单必须两层匹配**

| 组 | 不同文件名 | 单名最高命中 | 匹配方式 |
|---|---|---|---|
| `refine-logs/*.md` | **8** | 4 个 **4/4** | ✅ **按精确文件名** |
| `contracts/*.json` | 3 | 2/4 | （不读） |
| `necessary_materials/tables/*` | **49** | 每个 **1/4** | ❌ 按目录 + 扩展名枚举 |
| `necessary_materials/figures/*` | **28** | 每个 **1/4**（前缀 100% = `fig`） | ❌ 同上 |
| `output/results/*` | **24** | 最高 2/4 | ❌ 同上 |

> **结论**：`refine-logs/` 名字稳定可精确匹配；**素材目录的名字完全不可预测**，
> 只能按目录 + 扩展名枚举。**按文件名写全清单必然失效。**

### 2.2 `refine-logs/` 实测命中率

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

### 2.3 `contracts/` —— 决定不读

`module-tools.ts` 的注释：`/** Materialize the module's contract JSON (audit/fallback view). */`
与 *"files are a materialized view for audit/delivery, **never the contract**"*。

**实测**：命中 2/4；出现不规则（有 `LITERATURE_REVIEW.md` 却无 `litReview.json`）；
内容在 `VERIFICATION_REPORT.md` / `DECISION_LOG.md` / `EXPERIMENT_PLAN.md` 中有语义等价物。

### 2.4 素材目录：**4/4，但不要枚举 —— 要用正文的声明**

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

### 2.4.1 关键实测：`METHOD_UNDERSTANDING` / `EXPERIMENT_PLAN` 能否砍掉？

**假设**：论文正文既然完整，这两份的「为什么」是否已被覆盖、可以省略？

**测法**：抽出带理由标记的句子（R），再测其中**正文中术语几乎不出现**的（M）。
`M/R` 即「真正的边际贡献」占比。

| 样本 | 文件 | R | **M** | **M/R** | 流程噪音 P |
|---|---|---|---|---|---|
| S1 数据驱动 | `EXPERIMENT_PLAN.md` | 27 | **24** | **89%** | 34 |
| S2 习题 | `METHOD_UNDERSTANDING.md` | 6 | 1 | 17% | 0 |
| S2 习题 | `EXPERIMENT_PLAN.md` | 2 | 1 | 50% | 1 |
| S3 毕业论文 | `METHOD_UNDERSTANDING.md` | 20 | **12** | **60%** | 26 |
| S3 毕业论文 | `EXPERIMENT_PLAN.md` | 30 | **25** | **83%** | 35 |
| S4 硕士报告 | `METHOD_UNDERSTANDING.md` | 4 | 0 | 0% | 0 |
| S4 硕士报告 | `EXPERIMENT_PLAN.md` | 2 | 0 | 0% | 0 |

**结论：不可砍。** 两份"重"样本中 83–89% 的理由在正文中缺席，抽样内容均为答辩要害
（识别策略的维度约束、组内变异过小必须写入局限、稳健性预期、理论基准）。

**同时发现一个可优化点**：这两份含 **26–35 句流程元数据**（"执行入口 `codes/run`"、
"本文件是…参考"、"模块：Experiment Agent"），这些**不是理由**。
但换算后仅约 500 tokens/文件，**不值得为它引入抽取步骤**（抽取会带来漏检风险）。

> **成本对照**：这两份合计约 19 KB ≈ 7K tokens，换来 60–89% 的独有理由 —— **划算**。
> 真正的浪费在 `codes/`（1617 KB）、`contracts/`（47–78 KB）、`ORCHESTRATOR_COMPACT.md`（23 KB），
> 而这些**已全部排除**。

### 2.5 `assignment_profile.json`（4/4）`{deliverableType, topic, targetLength, formatRequirements[], citationStyle, language, attachments[{name, role}], constraints[], source}`

**`deliverableType` 是自由文本，不是枚举** —— 四份样本四种自然语言写法。
因此场景映射需要一次**分类**，不能字符串精确匹配。
`constraints[]` 同为自由文本，但信息密度高（语言、结构、数据真实性、篇幅要求）。

### 2.6 目录约定与模块条件性

`PATH_ACCESS_RULES`：交付物 **ONLY** in `output/`；结果数据 **ONLY** in `output/results/` 或
`necessary_materials/`；图表与参考文献 **ONLY** in `necessary_materials/`；源码 **ONLY** in `codes/`；
每模块日志 **ONLY** in `refine-logs/`；`assignment_profile.json` **ONLY** 在工作区根。
`logs/` 永不读写；`archive/` 永不写入。

模块条件：`litReview` *"USE ONLY when the assignment requires academic literature"*；
`experiment` *"**YOUR judgment, not an obligation**"*、*"**NEVER for essays/case studies**"*；
`visualization` *"USE ONLY when experiment actually ran"*；**写作无模块**。

> §2.1–2.4 的命中率差异正是这些条件性的直接后果。

### 2.7 三类典型作业的实测形态

| 类型 | 会有 |
|---|---|
| 数据驱动型 | `refine-logs` 全套 + 图表 + `output/results/` |
| 习题/代码型 | `refine-logs` 全套 + 图表 + `codes/`；**无 `output/results/`** |
| 写作型 | `refine-logs` 全套 + 图表 |

> **即使最"轻"的样本，`refine-logs` 四件套与图表目录依然齐备。**

---

## 3. P0：来源清单与解析器

### 3.1 架构

```
技能侧持有                 运行时                        技能消费
─────────────            ─────────────                 ─────────────
source-manifest.json  →  探测工作区 + 与清单比对  →  source-resolution.json
（声明式：可能有什么、      （两层匹配、stem 去重、        （需求 → 供给 +
  什么含义、满足什么需求）    排除规则、降级判定）            缺什么、降级了什么）
```

**清单是数据，不是逻辑**：管线新增产物时改清单，不改技能。

### 3.2 清单是**贡献者白名单**，不是存在性清单

> **设计反转（关键）**：清单**不描述"可能有什么"**，只描述**"什么对 PPT 有贡献"**。
> 不在清单里的一律不读 —— **默认拒绝，而非默认枚举**。

理由：`codes/` 有 39 个文件 1617 KB、`__pycache__` 一堆、编译垃圾 30+ KB。
这些**永远不会出现在 PPT 里**，告诉技能"它们存在"是纯浪费。

#### 3.2.1 贡献者（清单的全部条目）

| id | 路径 | 匹配 | 角色 | 权威 | 满足的需求 |
|---|---|---|---|---|---|
| `profile` | `assignment_profile.json` | exact | meta | **T0** | 场景 · 语言 · 硬约束 |
| `paper` | `output/main.tex` | exact | primary | **T0** | 主张 · 结构 · 论证 · 图注 · **图表声明** · 页序 |
| `decision-log` | `refine-logs/DECISION_LOG.md` | exact | rationale | T1 | 「为什么」· `communication_intent` |
| `verification` | `refine-logs/VERIFICATION_REPORT.md` | exact | rationale | T1 | 追问清单 · `audience_outcome` · 可靠性页 |
| `lit-review` | `refine-logs/LITERATURE_REVIEW.md` | exact | rationale | T1 | 缺口 · 对标 |
| `method-understanding` | `refine-logs/METHOD_UNDERSTANDING.md` | exact | rationale | T1 | 机制页 · 方法理由 |
| `experiment-plan` | `refine-logs/EXPERIMENT_PLAN.md` | exact | rationale | T1 | 设计理由 |
| `figures` | **正文 `\includegraphics{}` 声明的那些** | declared | visual | T2 | 图页 |
| `tables` | **正文 `\input{}` 声明的那些** | declared | data | T2 | 表页 · 图注 |

**仅此九条。** 其中八条是精确路径，一条是正文声明解析。

#### 3.2.2 明确排除（**不进清单，也不探测**）

| 产物 | 实测体量 | 为什么无贡献 |
|---|---|---|
| `codes/**` | S1 **1617 KB** / 39 文件 | 代码不进 PPT |
| `**/__pycache__/**` · `*.pyc` | 多个 | 字节码 |
| `output/*.log` · `.aux` · `.bbl` | 30+ KB | 编译垃圾 |
| `dois/**` · `library/**` | — | 文献原文 PDF |
| `contracts/**` | 47–78 KB | 传输层（§2.3） |
| `refine-logs/ORCHESTRATOR_COMPACT.md` | 平均 **23 KB** | 管线内部编排 |
| `refine-logs/VIZ_DATA_NOTES.md` | 平均 15 KB | 列级 dtype/nan 统计 |
| `refine-logs/experiment_run_report.md` | 平均 5.9 KB | 运行日志 |
| **未被正文声明的 tables** | S2 有 **14 个** | 死产物（§2.4） |

> **修正**：早期版本把 `VIZ_DATA_NOTES.md` 等标为 🟡「按需」。
> **这是错的 —— 它们没有"需"。** 应直接排除，而不是留一个永远不会触发的分支。

#### 3.2.3 按需读取（不进清单，只在特定需求下查）

| 需求 | 路径 |
|---|---|
| 需要某张表的**原始数值**做原生表格 | 同 stem 的 `necessary_materials/tables/*.csv` |
| 需要某张图的**原始数据** | `output/results/*.csv`（按图表名匹配） |
| 核对某个数值的**代码出处** | `codes/`（只读该行，不读文件） |

这三条是**查找路径**，不是"告诉技能有什么"。技能只在需要时按名取。

#### 3.2.4 清单外策略

```jsonc
"unknown_policy": "ignore-and-log"
```

**为什么仍需记录**：清单一定不完整 —— 本次 4 份样本里就出现了起草时未预见的
`VIZ_DATA_NOTES.md`、`experiment_run_report.md`、`ORCHESTRATOR_COMPACT.md`。
记录清单外文件，供事后**判断它们该进白名单还是黑名单**，但不影响本次运行。

**默认行为是「不读」**，所以漏判的代价是少一个来源，不是多烧 context。

### 3.3 解析器输出（**这是交给技能的东西**）

**关键：输出不是文件列表，是「需求 → 供给」的解析结果。**
因为技能问的是语义问题（"已知会被追问什么"），不是"有没有某个文件"。

```jsonc
{
  "schema": "ppt-master.source-resolution.v1",
  "workspace": "<abs path>",

  "scenario": {
    "value": "thesis",                        // 分类结果
    "from": "assignment_profile.json#deliverableType",
    "level": "T0", "confidence": "classified"
  },
  "language": { "value": "zh", "from": "assignment_profile.json#language", "level": "T0" },

  "resolved": {
    "communication_intent": { "from": ["decision-log"],        "level": "T1", "available": true },
    "audience_outcome":     { "from": ["verification-report"], "level": "T1", "available": true },
    "positioning":          { "from": ["literature-review", "main-tex"], "level": "T1", "available": true },
    "figure_images":        { "from": ["figures"],  "level": "T2", "available": true, "count": 4 },
    "figure_captions":      { "from": ["tables"],   "level": "T2", "available": true, "count": 6 },
    "data_tables":          { "from": ["tables", "output-results"], "level": "T2",
                              "available": true, "count": 6, "format": "csv" }
  },

  "unavailable": ["experiment_defects"],     // 需求无供给 → 名册相应页不出现
  "degraded":    ["method_rationale"],       // 有供给但等级低于首选 → 页面须标注
  "unknown_files": ["refine-logs/xxx.md"]    // 清单外，供反哺清单
}
```

技能据此**按需取用**：`available` 的走首选来源，`degraded` 的标注来源等级，
`unavailable` 的对应页面从名册中移除。

### 3.4 降级链（解析器内部的判定表）

| 需求 | 首选 | 命中 | 次选 | 再降级 |
|---|---|---|---|---|
| 场景 | `assignment_profile.deliverableType` → 分类 | 4/4 | 问用户 | — |
| 内容语言 | `assignment_profile.language` | 4/4 | `main.tex` 判定 | 问用户 |
| 硬约束 | `assignment_profile.constraints[]` | 4/4 | 空 | — |
| **`core_message`** | `main.tex` 定位段 | 4/4 | 论文结论 + **标记降级** | — |
| **`audience_outcome`** | `VERIFICATION_REPORT.md` 未决项 | 4/4 | `DECISION_LOG.md` 取舍段 | 场景模板通用条目 |
| **`communication_intent`** | `DECISION_LOG.md` 纪律/取舍段 | 4/4 | `EXPERIMENT_PLAN.md` | 场景模板通用意图 |
| 定位与缺口 | `LITERATURE_REVIEW.md` | 4/4 | `main.tex` 综述段 | — |
| 理论机制 | `METHOD_UNDERSTANDING.md` | 3/4 | `LITERATURE_REVIEW.md` | `main.tex` 机制段 |
| 方法页「为什么」 | `EXPERIMENT_PLAN.md` + `DECISION_LOG.md` | 4/4 | **只讲「是什么」，不编造理由** | — |
| 验证页 | `VERIFICATION_REPORT.md` | 4/4 | **名册中不出现验证页** | — |
| 图页 | 正文 `\includegraphics{}` 声明（4/4） | **名册中不出现图页**；不生成占位图 | — |
| 图注 | 声明处的 `\caption{}` + `main.tex` 对应段 | **不编造**：该页无图注 | — |
| 表页 | 正文 `\input{}` 声明（4/4） | `tables/*.tex` → `main.tex` 内联表格 | — |
| 表格原始数值 | 同 stem 的 `tables/*.csv`（按需） | 从 `.tex` 解析 | — |

**三条硬规则**：

1. **降级 ≠ 编造**：宁可少一页，不可补一个猜测。
2. **降级必须可见**：进入 `degraded`，页面上标注来源等级。
3. **缺产物不阻断**：只有 T0 缺失才阻断。

### 3.5 冲突规则

> 定量值：T0 → T1 → T2 → T3（按 `authority`）。
> 散文理由：`refine-logs/` 为准。
> 同级冲突或跨级冲突时**标注冲突**，不得静默择一。

### 3.6 前置门

```
output/main.tex 缺失                     → 阻断（T0 缺失）
VERIFICATION_REPORT.md 结论行含阻断性判断 → 回报管线「先修」
```

> 不读契约后，`defects[].severity` 这一**结构化**门不再可用，
> 改从验收报告的结论行解析。**该门因此从「硬门」降级为「启发式提示」**，不得据此误阻断。

---

## 4. P1：页面名册按解析结果生成

```
必有页：封面 · 定位/主张 · 结构/机制 · 结论 · 结束        （T0，4/4）

条件页：
  literature-review 可用          → 研究缺口页 · 对标页
  method-understanding 可用       → 理论机制页
  experiment-plan 可用            → 样本页 · 变量页 · 方法页
  data_tables 可用                → 数据表页
  figure_images 可用              → 图表页（每图一页或并列）
  verification-report 可用        → 可靠性页 · 预期追问页
```

**大纲推导顺序**（没有 `structure_plan.json`）：

1. `output/main.tex` 的**章节结构**（论文自身的论证骨架）
2. `LITERATURE_REVIEW.md`（定位与缺口）
3. `output/results/` 与 `tables/` 的组织（数据页）
4. `VERIFICATION_REPORT.md` 与 `DECISION_LOG.md`（局限与追问页）
5. `assignment_profile.targetLength` 与场景（页数预算）

**答辩稿 ≠ 论文**：论文要**证明**，答辩要**接住追问**。名册不应照搬论文章节。

---

## 5. P2：Stage 1 字段重构

### 5.1 逐字段来源（均不依赖 `contracts/`）

| 字段 | 来源 | 命中 |
|---|---|---|
| `primary_language` | `assignment_profile.language` | 4/4 |
| `audience` · `delivery_context` · `artifact_afterlife` | `deliverableType` **分类** + `constraints[]` | 4/4 |
| `content_divergence` | 固定 `strict` | — |
| `core_message` | `main.tex` 定位段 | 4/4 |
| `audience_outcome` | `VERIFICATION_REPORT.md` 未决项 | 4/4 |
| `communication_intent` | `DECISION_LOG.md` 纪律/取舍段 | 4/4 |
| `canvas` / 模板 | 场景 | 4/4 |

### 5.2 场景需要一次分类

`deliverableType` 是自由文本。约定分类函数：

```
输入：deliverableType + constraints[] + formatRequirements[]
输出：场景 ∈ { course_paper, competition_paper, thesis, proposal, midterm, group_meeting }
```

**上游若愿意配合**，最小改动是在 `AssignmentProfile` 上加可选枚举 `scenario?`。

场景 → 字段默认值示例（构造）：

| 场景 | `audience` | `delivery_context` | `artifact_afterlife` |
|---|---|---|---|
| 课内论文 | 任课教师与同班同学 | 课堂展示，有讲者 | 计入课程成绩，课后提交 |
| 比赛论文 | 竞赛评委（多为校外） | 现场答辩，含限时陈述与提问 | 参赛材料归档，可复用于后续赛程 |
| 毕业论文 | 答辩委员会：导师与评审专家 | 现场答辩，含提问；次要为会后独立阅读 | 答辩留档与评审复核 |
| 开题 | 导师与开题评审组 | 以提问与修改意见为主 | 开题记录，指导后续研究 |
| 中期 | 导师与中期检查小组 | 汇报进展与问题，侧重风险 | 过程记录 |
| 组会 | 导师与研究组成员 | 短时汇报，侧重方法与进展 | 一般无正式留档 |

### 5.3 交互改造原则

**保持字段为文本，变成「可点击填入」而非「下拉替换」。**

1. 下游规范**明确禁止**把沟通意图做成分类器：
   > `plan-core.md`：*"Communication intent is open-ended … are prompts, **never a classifier**."*
   > `confirm-surface.md`：*"The intent paths … are help text, **never a `primary_job` field**."*
2. 标签装不下**优先级与顺序**，而那是逐页大纲排序的依据
3. 真实痛点是「好默认值以散文呈现，学生要判断和改写」

| 字段 | 形态 |
|---|---|
| `delivery_context` · `artifact_afterlife` | **真选择** + 可选补充框 |
| `content_divergence` | **三档**，默认严格贴源 |
| `audience` | 选择 + 必填限定语 |
| `communication_intent` · `audience_outcome` | 文本 + 2–4 个「填入句」chip |
| `core_message` | **文本，标注来源，单独确认** |

### 5.4 复用现有交互

Stage 2 已有「3 个候选 + 推荐标记 + 自定义出口 + 恢复原方案 + 已调整标记」。
**Stage 1 直接移植**，切换场景时批量重写默认值，但**保留用户已手改的字段**。

---

## 6. 风险与对策

| 风险 | 对策 |
|---|---|
| **`core_message` 单点故障** | 即便全自动也**露出该字段单独确认** |
| **清单腐化** | `unknown_policy: ignore-and-log`；每次运行反哺 |
| **天真枚举导致重复** | `group_by: stem` + `ext_preference`（§2.4） |
| **误读 `contracts/`** | ⛔ 列入 `exclude` |
| **误读 `ORCHESTRATOR_COMPACT.md`** | ⛔ 列入 `exclude` |
| **条件产物缺失被当成「没有内容」** | §3.4 降级链；降级必须可见 |
| **`deliverableType` 自由文本** | §5.2 分类约定；或上游补可选枚举 |
| **前置门失去结构化依据** | §3.6：降级为启发式，不得误阻断 |
| `strict` 限制表达 | 留出口：允许显式改 `balanced`，默认 `strict` |

---

## 7. 验收标准

| # | 判据 | 检查方式 |
|---|---|---|
| **A1** | **能发现首版的五类缺陷** | 同一素材重跑，检查是否还犯 §1.1 的五类错 |
| **A2** | **无实验时也能跑** | 用写作型/习题型样本跑一次（无 `output/results/`） |
| **A3** | **无新增编造** | 页面每个数字都能在 T0–T3 中找到 |
| **A4** | **图注来自素材** | 逐条核对 = `\caption{}` 或 `main.tex` 对应段 |
| **A5** | **降级可见** | `degraded` 项在页面上标注来源等级 |
| **A6** | **不重复计数** | 4 张图不得解析成 8 张（stem 去重生效） |
| **A7** | **不读无贡献产物** | 读取日志中不得出现：`codes/` · `contracts/` · `__pycache__` · `ORCHESTRATOR_COMPACT.md` · `VIZ_DATA_NOTES.md` · `experiment_run_report.md` · 编译垃圾 |
| **A8** | **不读死产物** | 用 S2 型样本（表内联）跑一次：**不得读取任何未被正文声明的 `.tex`** |

**A2 与 A6 是硬指标。** A2 检验条件性前提；**A6 检验一个容易静默出错的解析细节**。
**A7/A8 可机械检查**（扫描读取日志），是"不浪费上下文"这一诉求的直接验收。

---

## 8. 实施顺序

### 8.0 新增什么（**不动上游一行代码**）

| 文件 | 作用 |
|---|---|
| `scripts/source_manifest.json` | 九条贡献者白名单（声明式数据，§3.2.1） |
| `scripts/resolve_sources.py` | 探测器 + 解析器（§3.3 的输出） |
| `scripts/docs/source-resolution.md` | 过程说明（按 `docs/rules/prompt-layers.md`，过程归 `scripts/docs/`） |

**CLI**：

```bash
# 探测 + 物化 + 出简报（一条命令）
python3 scripts/resolve_sources.py <upstream_workspace> --project <project_path>

# 只探测（调试 / 测试）
python3 scripts/resolve_sources.py <upstream_workspace> --json
```

**产出**：

```
<project>/sources/
├── resolution.json   ← 语义简报（需求 → 供给 + unavailable/degraded）
├── upstream/         ← 物化的九条贡献者（保持相对路径，自包含）
└── resolution.log    ← 读取日志（A7/A8 的机械验收依据）
```

### 8.1 三处接入点（改现有文件）

| 文件 | 改动 |
|---|---|
| `workflows/generate-pptx.md` Step 1 | 加一步：若给了上游工作区，先跑 resolver |
| `references/strategist.md` | 加**理由层**规则：方法页/局限页/追问页的来源（§2.4.1 的证据） |
| `references/plan-core.md` | 名册按 `resolution.json` 生成（§4） |

### 8.2 阶段

```
第一步（P0）  §3 清单 + 解析器（声明式白名单 / 正文声明解析 / stem 去重 / 降级链）
              → 纯增量，零上游改动
              → 四份样本各跑一次，逐条验 A1–A8
              → 四份 resolution.json 存为**金样本基线**

第二步（P1）  §8.1 三处接入

第三步（P2）  §5 Stage 1 字段默认值由 resolution 供给

第四步（P3）  §5.3 确认页交互（场景分类 + chip + 三档发散度）

第五步（P4）  Stage 1 自动确认开关（默认开）
```

### 8.3 三条工程纪律

1. **skill-driven，不是 pipeline-driven** —— 技能自己探测工作区，上游零改动。
   工作区路径由显式参数给出，不做隐式搜索。
2. **测规则，不测样本** —— 见 §8.5。
3. **`resolution.log` 是验收依据** —— A7/A8 靠扫这个日志，不靠人判断。

### 8.4 怎么验证解析器（**不用样本快照**）

> **为什么不冻结样本输出**：4 份测试样本的作业内容高度局限，
> 冻结它们等于把**不具代表性的样本固化成设计约束** —— 清单该扩展时快照反而成为阻力。
> 样本的作用是**发现问题的形状**，不是**验证解法**。

**正确做法：测规则。** 分层如下：

| 层 | 手段 | 验什么 |
|---|---|---|
| **单元** | `scripts/tests/` 下**构造的目录树**，每个 fixture 只考一条规则 | 精确匹配 · 声明解析 · stem 去重 · 排除规则 · 降级判定 · 清单外策略 |
| **性质** | 不变量断言，不比对快照 | ① 日志中不出现 `codes/`「不读无贡献产物」<br>② 图数 == 正文声明数「不重复计数」<br>③ 无同 stem 重复项<br>④ 同一输入两次运行结果一致「可复现」 |
| **冒烟** | 4 份样本仅作**输入**，跑通即可 | 不崩溃、输出结构合法、`unavailable`/`degraded` 字段存在 |
| **生产** | 真实运行积累 `resolution.log` 的 `unknown_files` | 清单**哪里不完整** —— 这是前瞻性机制，不是回归机制 |

**关键**：单元 fixture 是**构造**的，因此可以覆盖样本没覆盖的形态 ——
无图作业、纯文献作业、多语言、短论文、上游半途中止。**这些是样本给不了的。**

真实分布的积累路径是 §3.2.4 的 `unknown_policy`：记录但不读取，事后据此判断该进白名单还是黑名单。

### 8.5 待定的三件事

| # | 问题 | 倾向 |
|---|---|---|
| 1 | 上游工作区路径怎么传？ | 独立命令 `--project` + 可选 `--workspace`；不隐式搜索 |
| 2 | 物化还是引用？ | **物化** —— 项目自包含、可复现，且图件本就要嵌入 |
| 3 | 场景分类放哪？ | 技能侧分类 + 上游可选 `scenario?` 覆盖（§5.2） |

**上游侧建议改动（可选）**：
1. `AssignmentProfile` 增加可选枚举 `scenario?`
2. 论文自我定位句作为可选字符串字段输出

---

## 附录 A：证据出处

| 结论 | 来自 |
|---|---|
| **命名稳定性数据**（§2.1） | **4 份样本普查** |
| **素材同 stem 多扩展名**（§2.4） | 同上 |
| **契约不读**（§2.3） | 代码注释 *"never the contract"* + 命中 2/4 + 对应物核验 |
| **图注来源**（§1.3） | 契约 caption 与 `\caption{}` 并排对照 + 无契约样本的 `main.tex` 图注 |
| 目录归属规则 | `module-tools.ts` · `PATH_ACCESS_RULES` |
| 模块条件性 · 无写作模块 | `orchestrator-persona.ts` · `pepper-plugin.ts` |
| 五类内容缺陷 | 对照实测 |

## 附录 B：判断修正史

| 版本 | 判断 | 修正依据 |
|---|---|---|
| v1 | 新建 `roles.json` + `defense-brief.json` | — |
| v2 | 取消新文件；字段已在 `contracts/*.json` | 读上游代码 |
| v3 | 产物条件存在；无写作模块 | 用户提醒 + 读 persona |
| v4 | 不读 `contracts/`；散文与素材是基线 | 4 份样本普查 |
| v5 | 声明式清单 + 运行时解析器；两层匹配；stem 去重 | 命名稳定性实测 |
| **v6** | **清单改为「贡献者白名单」；图表按正文声明解析；明确排除 9 类无贡献产物** | **用户指出"存在 ≠ 有贡献"** |
| **v7** | **取消样本快照；改为「测规则不测样本」；§2 数据降级为指示性** | **用户指出样本作业内容局限，仅供调研参考** |

> **v7 的教训**：样本帮我**发现了问题的形状**（条件存在、命名不稳、声明≠目录、契约冗余），
> **但不能验证解法**。把样本输出冻结成基线，等于把不具代表性的样本固化成设计约束。
> **发现用样本，验证用构造的 fixture，校准用生产日志。**

---

## 附：本文不含的内容

样本的选题、数据、文献与路径均**未写入本文**；`deliverableType` 仅以「四份样本写法各异」的方式提及。
目录名、字段名与规则引文均取自上游代码，属于管线设计的一部分。
