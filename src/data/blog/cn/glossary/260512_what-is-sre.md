---
title: "什么是 SRE？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-12 11:28:39.488100+09:00
slug: "what-is-sre"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "SRE（站点可靠性工程）是将软件工程方法论应用于系统运维，以最大限度地提高服务稳定性和可用性的实践体系。本文将通过 SLO 和错误预算的定量管理及自动化核心概念，探讨高效的 IT 基础设施运营策略。"
references: []
modDatetime: 2026-05-12 11:38:39.488100+09:00
---

# 什么是 SRE？

## 词典定义 (Dictionary Definition)
SRE（Site Reliability Engineering，站点可靠性工程）是由 Google 创立的一种系统运维方式，是指将软件工程方法论应用于 IT 基础设施及运维问题的实践体系。其特点是积极利用自动化和监控来保证系统的可靠性、可用性和效率，最大限度地减少重复性手动工作（Toil，琐事），并基于服务水平目标（SLO）对系统稳定性进行定量管理。

## 实际应用案例 (Practical Use Case)
在引入 eBPF 等安全技术的过程中，SRE 会衡量安全逻辑对系统可用性造成的负载并建立监控体系。如果在安全程序发布后检测到系统调用处理速度下降，并存在超出预设错误预算（Error Budget）的风险，SRE 将决定停止发布或优先进行性能优化工作，以确保系统的可用性。

## 相关术语 (Related Words)
* <b>DevOps</b>：一种强调软件开发与运维协作的文化哲学，而 SRE 被视为通过具体工程技术实现该哲学的实践模型。
* <b>SLO (Service Level Objective)</b>：服务提供者承诺遵守的关于性能和可用性的具体目标值。
* <b>Error Budget（错误预算）</b>：指在达成 SLO 的前提下，允许系统不可用的总时长，它是衡量是否可以发布新功能的关键基准。