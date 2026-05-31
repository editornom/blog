---
title: "cgroups"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-31 15:48:37.300383+09:00
slug: "cgroups"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "cgroups（control groups）是 Linux 内核的一项功能，用于限制和隔离进程组的 CPU、内存等系统资源的使用。本文将探讨 cgroups 的定义及其实践案例，了解其在 Docker 和 Kubernetes 环境中如何防止资源耗尽并确保系统稳定性。"
references: []
modDatetime: 2026-05-31 15:58:37.300383+09:00
---

# 什么是 cgroups？

### 词典定义 (Dictionary Definition)
cgroups（control groups）是 Linux 内核提供的一种功能，用于限制、隔离和监视进程组对系统资源（如 CPU、内存、网络带宽、磁盘 I/O 等）的使用。其目的是让系统管理员能够控制特定进程集合的资源消耗，从而确保系统的稳定性。

### 实际应用案例 (Practical Use Case)
在 Kubernetes 或 Docker 环境中，通过为特定容器设置内存限制（Limit），可以防止发生内存泄漏的容器耗尽整个节点（Node）的资源。这通常被用于“Out Of Memory (OOM) Killer”管理机制等实务场景中。

### 相关术语 (Related Words)
* **命名空间 (Namespaces)**：一种按进程隔离系统资源并限制其相互可见性的技术。
* **容器虚拟化 (Container Virtualization)**：一种共享宿主机操作系统内核并在隔离环境中运行应用程序的技术。
* **Linux 内核 (Linux Kernel)**：Linux 操作系统的核心部分，负责管理硬件资源并拥有进程控制权。