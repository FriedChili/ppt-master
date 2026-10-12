# ppt-master（科研学术分支）

把论文、图表、实验材料和过程文档，变成**原生可编辑的 PowerPoint**。

这是 ppt-master 的**科研/学术专用分支**：已移除企业品牌、商务沟通方法、音效、
动画/配音/视频交付等非科研场景面。当前交付物是**静态**幻灯片。
改动清单与回滚方式见 [`skills-academic/ppt-master/FORK.md`](skills-academic/ppt-master/FORK.md)。

**本文档面向使用者。** 与上游写作管线对接、解析器原理与命令，见 [`pepper_use.md`](pepper_use.md)。

---

## 它做什么

给一份材料（论文 PDF / LaTeX / Markdown / 图片 / 直接文字），产出一个 `.pptx`，
其中每个文本框、形状、图表都是 PowerPoint **原生对象**，可以直接改，不是截图贴图。

```bash
SK=skills-academic/ppt-master

python3 $SK/scripts/project_manager.py init my_deck
python3 $SK/scripts/project_manager.py import-sources projects/my_deck_20261011 ./paper.pdf
```

之后由 AI 按 [`SKILL.md`](skills-academic/ppt-master/SKILL.md) 走生成流程，
产出在 `exports/<name>_<时间戳>.pptx`。

---

## 目录结构

```
skills-academic/ppt-master/     ← 本分支的技能本体（唯一需要读的）
├── SKILL.md                    ← 全局纪律与路线入口；改任何东西前先读
├── workflows/                  ← 路线权威：generate-pptx / create-template / edit-native-pptx
├── references/                 ← 角色核心与按需加载的技术模块
├── scripts/                    ← 可执行工具，其中 docs/ 是面向工具的说明
├── templates/                  ← 模板与图标库
└── FORK.md                     ← 本分支改了什么、怎么回滚

docs/                           ← 面向使用者的文档
projects/                       ← 用户项目工作区
```

> **仓库根另有 `skills/ppt-master/`，那是上游原始副本，不是本分支。**
> 不要在那边改东西。

---

## 快速开始

**前置**：Python 3.10+；可选 `pandoc`（转 `.tex`，缺失不影响主流程，见 [`pepper_use.md`](pepper_use.md) §8.1）。

```bash
pip install -r skills-academic/ppt-master/requirements.txt
```

### 三条路线

| 路线 | 用在什么时候 | 权威文档 |
|---|---|---|
| **Generate PPTX** | 从材料做一份新稿 | [generate-pptx.md](skills-academic/ppt-master/workflows/generate-pptx.md) |
| **Create Template** | 从 PPTX / SVG / 图片 / 文档做 `style`、`layout`、`deck` 模板 | [create-template.md](skills-academic/ppt-master/workflows/create-template.md) |
| **Edit Native PPTX** | 改一份已有的原生 PPTX | [edit-native-pptx.md](skills-academic/ppt-master/workflows/edit-native-pptx.md) |

Generate 有两个互斥运行时：默认的 **Strategist → Image_Generator → Executor**（含确认环节），
以及**无独立策略与确认**的 Quick。

### 典型流程（默认运行时）

```
Step 1–3  摄取材料 → 解析图片 → 准备模板候选
Stage 1   确认沟通契约 + 从零设计 / 套用模板
Stage 2   最终方案打磨 + 各节细节
Step 4    design_spec.md + spec_lock.md
Step 5    图片（仅当需要 AI 生成图时）
Step 6    逐页 SVG → 质检 → 后处理 → 讲者备注
Step 7    导出 PPTX
```

### 命令速查

```bash
SK=skills-academic/ppt-master

python3 $SK/scripts/project_manager.py init <project_name>
python3 $SK/scripts/project_manager.py import-sources <project_path> <sources...>
python3 $SK/scripts/project_manager.py validate <project_path>
python3 $SK/scripts/confirm_ui/server.py <project_path> --daemon
python3 $SK/scripts/svg_quality_checker.py <project_path> --canonical-authoring --stage final --json
python3 $SK/scripts/finalize_svg.py <project_path>
python3 $SK/scripts/svg_to_pptx.py <project_path>
```

其余命令（模板物化与预览、切片、创作视图刷新等）由拥有它的路线或阶段列出，
并见 [`scripts/docs/svg-pipeline.md`](skills-academic/ppt-master/scripts/docs/svg-pipeline.md)。

---

## 文档

| 文档 | 内容 |
|---|---|
| [`pepper_use.md`](pepper_use.md) | 对接上游写作工作区、解析器原理与用法 |
| [`FORK.md`](skills-academic/ppt-master/FORK.md) | 本分支的改动清单与回滚 |
| [`SKILL.md`](skills-academic/ppt-master/SKILL.md) | 全局执行纪律与路线选择 |
| [`docs/getting-started.md`](docs/getting-started.md) | 做出第一份稿 |
| [`docs/templates-guide.md`](docs/templates-guide.md) | 模板怎么用 |
| [`docs/faq.md`](docs/faq.md) | 常见问题 |
| [`docs/windows-installation.md`](docs/windows-installation.md) | Windows 安装 |

---

## 许可与第三方署名

MIT，见 [`LICENSE`](LICENSE)。

图标库、字体等第三方资源的署名要求在各资源目录内的说明文件中。
**这些署名是许可要求，不得移除。**
