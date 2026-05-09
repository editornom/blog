---
title: "Rowhammer"
author: "editornom"
author_role: "Senior Tech Editor"
author_url: "https://editornom.com/about"
pubDatetime: 2026-05-09 11:23:04.486265+09:00
slug: "rowhammer"
featured: false
draft: false
ogImage: "../../../../assets/images/placeholder.png"
description: "Rowhammer 是一种硬件安全漏洞，通过高速重复激活 DRAM 的特定行来诱发相邻行的比特翻转，从而导致系统权限夺取和数据篡改等严重安全威胁。本文深入分析了针对最新 DDR5 和 GPU 的攻击案例，以及从 TRR 到 PRAC 等实务性应对技术和防御策略。"
references: []
modDatetime: 2026-05-09 11:33:04.486265+09:00
---

# 什么是 Rowhammer？

### 词典定义 (Dictionary Definition)
Rowhammer 是一种硬件安全漏洞，通过高速重复激活 DRAM (Dynamic Random Access Memory) 的特定内存行 (Row) 来诱发相邻行的电荷干扰，从而导致存储的数据发生比特翻转 (Bit-flip)。这是利用了微细加工后的半导体器件之间的物理干扰现象，可被用于绕过软件访问权限，篡改内存数据或夺取系统权限。

### 实际使用案例 (Practical Use Case)
1. **DDR5 漏洞攻击**：已证实存在 Phoenix 攻击，该攻击能够绕过制造商应用的 TRR (Target Row Refresh) 技术的采样逻辑，在最新的内存模块中也能成功诱发比特翻转。
2. **GPU 安全入侵**：利用 GDDR6 内存的架构特性执行 GPUBreach 攻击，用于在高性能计算环境中夺取 Root 权限。
3. **实际应对策略**：通过缩短刷新周期 (tREFI)，在电荷流失发生前为内存单元重新充电；或引入 PRAC (Per-Row Activation Counting) 技术，在 DRAM 内部直接计数行激活次数，从而在源头上阻断攻击。

### 相关术语 (Related Words)
1. **比特翻转 (Bit-flip)**：由于物理干扰导致内存中的逻辑数据值从 0 翻转为 1 或从 1 翻转为 0 的现象。
2. **TRR (Target Row Refresh)**：一种基于硬件的防御技术，当检测到特定行被过度激活时，主动刷新相邻行以保护数据。
3. **PRAC (Per-Row Activation Counting)**：实时统计 DRAM 各行激活次数，防止达到 Rowhammer 攻击阈值的下一代安全标准技术。