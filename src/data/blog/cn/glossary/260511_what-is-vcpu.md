---
title: "什么是 vCPU？"
author: editornom
author_role: "高级技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 11:36:06.856378+09:00
slug: "what-is-vcpu"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "本文介绍了 vCPU（虚拟中央处理器）的定义、将物理 CPU 资源分配给虚拟机的原理，以及在云计算环境中的实际应用案例。了解如何通过 Hypervisor 有效管理计算能力并优化实例性能的关键指标。"
references: []
modDatetime: 2026-05-11 11:46:06.856378+09:00
---

# 什么是 vCPU？

## 词典定义 (Dictionary Definition)
vCPU（虚拟中央处理器，Virtual Central Processing Unit）是指在虚拟化计算环境中分配给虚拟机（VM）的逻辑计算单位。它通过 Hypervisor 将物理处理器（pCPU）的资源进行抽象化后提供，通常对应于硬件的物理核心或应用了超线程（Hyper-threading）技术的逻辑线程。

## 实际应用案例 (Practical Use Case)
在利用 Cloud 服务时，vCPU 是决定实例性能的核心指标。例如，在云环境（如 AWS RDS 等）中部署 MySQL 数据库时，需要根据工作负载的复杂度和处理量来选择 vCPU 的数量，以此来扩展或限制计算能力。

## 相关词汇 (Related Words)
Hypervisor、物理 CPU（Physical CPU）、实例（Instance）