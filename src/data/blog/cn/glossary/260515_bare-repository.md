---
title: "Bare 仓库 (Bare Repository)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-15 15:22:39.054299+09:00
slug: "bare-repository"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Bare 仓库是一种没有工作目录的 Git 仓库，主要用于协作的中央远程仓库及数据备份。它仅由 Git 元数据组成，旨在维护数据完整性并支持高效的源代码管理。"
references: []
modDatetime: 2026-05-15 15:32:39.054299+09:00
---

# 什么是 Bare 仓库？

### 词典定义 (Dictionary Definition)
Bare 仓库（Bare Repository）是指一种没有工作目录（Working Directory）的 Git 仓库格式，而源代码的实际修改和编辑通常是在工作目录中进行的。一般的 Git 仓库包含源代码文件以及存储版本控制元数据的 .git 目录，与此不同，Bare 仓库仅由 .git 目录中的内容组成。由于不存在作为工作空间的工作树（Working Tree），因此无法在仓库内直接修改文件或进行提交（Commit）。它主要用于协作的中央服务器，或者用于安全地共享和备份数据。

### 实际使用案例 (Practical Use Case)
Bare 仓库主要用于在 GitHub、GitLab 或企业内部服务器上构建中央远程仓库。开发人员在本地仓库完成工作后，通过 push 命令将更改发送到该 Bare 仓库。在最近的 Git 2.54 更新中，包含了无需经过索引（Index）过程即可直接在 Bare 仓库内操作对象数据的功能，这使得在没有工作树的环境下也能进行精细的历史修改和数据管理。

### 相关术语 (Related Words)
1. 工作树 (Working Tree)：开发人员实际修改文件并执行项目工作的区域。
2. 远程仓库 (Remote Repository)：位于网络上的仓库，通常以 Bare 仓库的形式运行。
3. 数据完整性 (Data Integrity)：指数据的准确性和可追溯性。Bare 仓库通过中央管理，在维护这种完整性方面发挥着核心作用。