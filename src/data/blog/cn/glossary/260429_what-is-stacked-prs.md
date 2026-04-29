---
title: "什么是 Stacked PRs？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-29 17:12:18.110264+09:00
slug: understanding-stacked-prs-workflow
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Stacked PRs 是一种将大型功能拆分为逻辑清晰的小单元并进行分层管理的日常工作流策略，旨在最大化评审效率和开发生产力。本文介绍了无需等待下游 PR 批准即可连续工作的 Stacked PRs 的定义、实战应用方法及高效管理技巧。"
references: []
modDatetime: 2026-04-29 17:22:18.110264+09:00
---

### 词典定义 (Dictionary Definition)
Stacked PRs 是一种工作流策略，它将大型功能拆分为逻辑上完整的微小单元，并将多个 Pull Request（PR）层层堆叠。与其使用一个庞大的功能分支，不如将每项更改拆分为独立的分支，并按顺序建立依赖关系。通过这种方式，开发者无需等待下游 PR 被批准或合并，即可继续进行上层开发，而评审人员则可以通过审查上下文清晰的小型代码块来最大化评审效率。

### 实战使用示例 (Practical Use Case)
在开发大型新功能时，可以将其划分为数据库架构修改、业务逻辑实现、API 端点开发、UI 层作业等 4 个逻辑单元。每个阶段都会创建一个单独的 PR，其中 “API 端点” PR 是在 “业务逻辑” 分支之上创建的。评审人员独立审查每个 PR 并提供快速反馈，而开发者在下游阶段进行评审期间可以不间断地进行 UI 工作。但是，如果下游 PR 被 Squash Merge，上层分支的父提交哈希值会发生变化，因此需要通过 Rebase 重新构建历史。

### 相关术语 (Related Words)
- **Rebase（变基）**: 一种 Git 命令，通过重新设置分支的基准提交来整理提交历史，是维持 Stacked PRs 一致性的核心工具。
- **Squash Merge（压缩合并）**: 一种将多个提交合并为一个提交进行合并的方式，在 Stacked PRs 结构中，有时会成为导致与上层分支连接断开的技术债原因。
- **Feature Branch（功能分支）**: 在一个分支中管理整个功能的传统方式，是与 Stacked PRs 相对的概念。