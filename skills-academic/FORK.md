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

## 5. 尚未完成（TODO）

1. **`simple-icons` 的散文引用**：`templates/icons/README.md`、`THIRD_PARTY_NOTICES.md`、
   `scripts/icon_sync.py`（`_SYNC_LIBRARIES` 仍含 `simple-icons`）、`scripts/svg_finalize/embed_icons.py`（尺寸映射）、
   `references/executor-base.md`、`spec_lock_reference.md`、`strategist.md`、`plan-core.md`、
   `design_spec_reference.md`、`quick-generate.md`
2. **动画/音频/视频的散文引用**：`routing.md §6`、`generate-pptx.md`（Step 7 的 `-a` / `--no-animations` 与 §I 行）、
   `SKILL.md`、`executor-base.md §1`（motion endpoints）、`executor-notes.md`、`design_spec_reference.md §I`、
   `spec_lock_reference.md`、`visual-styles/_index.md`、`confirm-surface.md`、`workflows/index.md` 的 `video-design` 行
3. **decks 去标识化**：`中国电信` / `中汽研` → 中性名；剥离 `logo.png`、`header_brand.png`、`slogan_red.png`、
   `top_emblem.png`、`大型 logo.png`、`右上角 logo.png` 等企业资产；改写 `design_spec.md` 与 `decks_index.json`
4. **`templates/styles/README.md`** 是否枚举了已删的 7 个方法
5. `scripts/docs/confirm_ui.md`（catalog 文件清单）、`scripts/docs/template-tools.md`（index 清单）
6. `prompt_audit_manifest.json` 残留字符串（`create-brand`×2、`create-deck`×2、`video-design`×5、
   `templates/brands`×4、`generate-audio`×4、`customize-animations`×3、`templates/sounds`×2、`animations.md`×1）
   —— 该文件只服务 `prompt_audit.py` 开发期校验，不影响生成；建议按瘦身后的树重新生成而非逐条修补
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
