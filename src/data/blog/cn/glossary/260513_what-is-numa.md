---
title: "NUMA (Non-Uniform Memory Access) 是什么？"
author: editornom
author_role: 高级技术编辑
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 11:36:42.093125+09:00
slug: "what-is-numa"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "NUMA (Non-Uniform Memory Access) 是一种多处理器系统架构，其内存访问速度取决于处理器与内存的相对位置。本文将介绍 NUMA 的定义，并分析在 MPI 应用等实际环境中可能出现的内存性能下降问题。"
references: []
modDatetime: 2026-05-13 11:46:42.093125+09:00
---

# NUMA (Non-Uniform Memory Access) 是什么？

## 词典定义
NUMA (Non-Uniform Memory Access，非一致性内存访问) 是一种多处理器系统架构。在这种架构中，每个处理器（或处理器组）都拥有专用的本地内存。访问本地内存时速度很快，但访问其他处理器的本地内存（远程内存）时，访问速度相对较慢。这种情况通常发生在物理内存被分割并分配给多个插槽（Socket）时，其核心特征是内存访问速度的不均匀性。

## 实际应用案例
在 NASA 的高性能计算 (HECC) 环境中运行基于 MPI (Message Passing Interface) 的应用程序时，NUMA 架构常因页面缓存（Page Cache）独占问题，导致内存饥饿现象及性能下降。例如，当某个特定进程独占了本地插槽的内存时，其他进程不得不访问数据传输速度明显较慢的远程插槽内存，从而导致整体计算效率大幅降低。

## 相关术语
- 页面缓存 (Page Cache)
- MPI (Message Passing Interface)
- Direct I/O