---
title: "什么是惊群效应 (Thundering Herd)？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 11:39:40.174633+09:00
slug: "thundering-herd"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "惊群效应（Thundering Herd）是指在分布式系统中，当多个进程同时被唤醒以争夺单个资源时，导致严重的 CPU 浪费和上下文切换，从而引发性能下降。本文将深入探讨其成因与应对策略。"
references: []
modDatetime: 2026-05-29 11:49:40.174633+09:00
---

# 什么是惊群效应 (Thundering Herd)？

### 词典定义 (Dictionary Definition)
“惊群效应”（Thundering Herd）是计算机科学和分布式系统中的一种现象。当某个特定事件发生时，大量处于等待状态的进程或线程会同时被唤醒，并尝试处理同一个资源，从而导致系统性能大幅下降。虽然所有请求都在竞争该资源，但实际上只有极少数（通常只有一个）进程能够成功获取，其余进程则被迫重新回到等待状态。在这一过程中产生的过度上下文切换（Context Switching）和 CPU 资源浪费会显著降低整个系统的可用性。

### 实务使用案例 (Practical Use Case)
1. **缓存击穿 (Cache Stampede)**：在高并发流量下，当某个热点数据的缓存过期的瞬间，大量客户端同时访问后端源数据库（Origin DB）请求数据，导致数据库服务器因负载过重而瘫痪。
2. **被动对冲请求 (Hedged Requests) 的副作用**：在系统出现延迟时，如果为了降低延迟而盲目采用同时向多个副本发送重复请求的技术，可能会导致本就处理缓慢的后端节点流量激增，使系统陷入不可恢复的“自杀式 DoS”状态。
3. **互斥锁 (Mutex) 争用**：当共享资源的锁被释放时，所有等待该锁的线程会同时被唤醒并尝试占有资源，这会在内核层面引发剧烈的调度负荷。

### 相关术语 (Related Words)
- **Request Coalescing (请求合并)**
- **Cache Stampede (缓存击穿/雪崩)**
- **Exponential Backoff (指数退避)**