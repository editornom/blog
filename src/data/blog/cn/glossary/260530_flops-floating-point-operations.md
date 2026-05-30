---
title: "FLOPs (每秒浮点运算次数)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-30 19:36:48.490759+09:00
slug: "flops-floating-point-operations"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "探讨 FLOPs (每秒浮点运算次数) 的定义及其在 AI 模型训练与推理过程中作为衡量计算资源的核心指标所发挥的作用。本文将详细介绍基于模型参数和数据规模的运算量计算方法，以及旨在实现高效 AI 开发的实际应用案例。"
references: []
modDatetime: 2026-05-30 19:46:48.490759+09:00
---

# 什么是 FLOPs？

### 词典定义 (Dictionary Definition)
FLOPs (Floating Point Operations per Second) 是衡量每秒可执行浮点运算次数的单位。它是计算机运算性能的代表性衡量标准。在人工智能领域，它也常被用作表示在训练 (Training) 或推理 (Inference) 大语言模型 (LLM) 等过程中所需的总运算量 (Total Floating Point Operations) 的指标。该指标与模型的参数量、训练数据量密切相关，是量化为提升 AI 性能而投入的计算资源规模的核心变量。

### 实际应用案例 (Practical Use Case)
1. 在开发 AI 模型时，通过计算整个训练所需的总 FLOPs，可以提前预测所需的 GPU 资源规模和 Cloud 计算成本。
2. 通过开发性能相同但消耗更少 FLOPs 的轻量化算法，可以提高端侧 AI (On-device AI) 的推理效率。
3. 在比较 NVIDIA H100 等 AI 加速器的性能时，通常以每秒万亿次浮点运算 (TFLOPS) 或每秒千万亿次浮点运算 (PFLOPS) 为单位的运算处理能力作为基准。

### 相关术语 (Related Words)
* **缩放法则 (Scaling Laws)**：该法则指出，随着计算资源 (Compute)、数据规模和参数量的增加，模型性能会以可预测的方式得到提升。
* **香奇拉法则 (Chinchilla Law)**：该法则定义了在给定的运算量 (FLOPs) 预算内，为实现最佳性能而所需的模型参数量与数据量之间的最优比例。
* **计算资源 (Compute)**：指为了处理 AI 模型的运算而投入的硬件处理能力及其总量。