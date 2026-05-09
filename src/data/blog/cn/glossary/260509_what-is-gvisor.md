---
title: "什么是 gVisor？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 16:51:26.458171+09:00
slug: "what-is-gvisor"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "gVisor 是一款开源沙箱运行时，通过独立的用户空间内核控制系统调用，在宿主机与容器之间提供强大的安全隔离。它被广泛应用于 GKE 等环境，用于安全地运行不可信的外部工作负载，并防止对宿主机系统的入侵。"
references: []
modDatetime: 2026-05-09 17:01:26.458171+09:00
---

### 词典定义 (Dictionary Definition)
gVisor 是由 Google 开发的一款基于开源的容器运行时沙箱。该技术通过在应用程序与宿主机操作系统内核之间提供一个独立的用户空间内核 (User-space kernel)，来拦截并处理系统调用 (System Call)。其目的在于弥补传统 Linux 容器因共享宿主机内核而可能产生的安全漏洞，从而构建一个强隔离的安全环境。

### 实际应用场景 (Practical Use Case)
在 GKE (Google Kubernetes Engine) Agent Sandbox 环境中，它被用于保护需要运行不可信外部代码的 AI 智能体工作负载。在运行安全性较低的第三方应用程序时，gVisor 作为隔离层通过控制系统调用来防止攻击者入侵宿主机系统。然而，由于该过程中产生的系统调用开销 (Overhead)，在进行高性能推理任务时可能会产生一定的延迟。

### 相关词汇 (Related Words)
* 容器运行时 (Container Runtime)
* 沙箱 (Sandbox)
* 系统调用 (System Call)