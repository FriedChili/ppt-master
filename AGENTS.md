# AGENTS.md

**本仓库是 deck 的科研/学术专用分支（academic fork）。**
企业品牌、商务沟通方法、音效、动画/配音/视频交付等非科研场景面已移除；
当前交付物是**静态**幻灯片。改动清单与回滚方式见
[`skills-academic/ppt-master/FORK.md`](skills-academic/ppt-master/FORK.md)。

## 入口

**做任何 PPT 生成任务或改仓库之前，必须先读
[`skills-academic/ppt-master/SKILL.md`](skills-academic/ppt-master/SKILL.md)。**
它拥有全局执行纪律，并指向路线选择器；选定路线后，由该路线的运行时权威
拥有自己的步骤、闸门与命令。

**分支自己的完整入口说明**（路线清单、执行要求、约定、命令速查、核心目录）
在 [`skills-academic/AGENTS.md`](skills-academic/AGENTS.md)，与本文件同级同源。

## 两个必须知道的事

**一、改哪里。** 只改 `skills-academic/ppt-master/` —— 它是本分支的唯一副本。
上游原版已从工作区移除，需要时用标签取回：`git checkout pristine-6.7.0 -- skills/ppt-master`。

**二、路径锚点。** 从本文件所在位置解析出仓库根的绝对路径，并保留
`skills-academic/ppt-master` 的绝对根之后再执行第一条命令。本文件里的路径是
仓库相对记法，只用于表达位置；实际调用一律走那两个绝对根，并保留初始化返回的
绝对项目路径。不要 `cd skills-academic/ppt-master`，也不要 `cd projects/...`。

解析机器可读的 stdout 时保持 stderr 分离，不要把 `2>&1` 放在 JSON 或 XML
解析器上游。每个命令对一组具体参数只调用一次；不要把它编码进标量 shell 字符串、
不要用 shell 循环批处理、命令已提供紧凑视图时不要再加下游解析器。

## 用户文档

面向使用者的入口是 [`README.md`](README.md)（中文见 [`README_CN.md`](README_CN.md)），
用户文档目录是 [`docs/`](docs/)。与上游写作管线对接、解析器原理与用法见
[`pepper_use.md`](pepper_use.md)。

## 兼容边界

- 本仓库是工作流/技能包，不是应用或服务脚手架。
- 除非用户明确要求，不要假设通用项目约定（`.worktrees/`、CI、强制分支流程）。
- 唯一的测试位置是 `skills-academic/ppt-master/scripts/tests/`。
- 与通用编码技能冲突时，以本仓库内的
  [`SKILL.md`](skills-academic/ppt-master/SKILL.md) 为准。
