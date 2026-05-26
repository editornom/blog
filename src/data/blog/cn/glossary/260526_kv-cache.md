---
title: "什么是 KV Cache？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-26 18:52:40.627031+09:00
slug: "kv-cache"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "KV Cache 是一种在 LLM 推理过程中将先前标记的运算结果存储在 VRAM 中并重复使用的技术，旨在提高生成速度并优化内存效率。它通过减少 Transformer 架构中的重复计算来缩短推理延迟。"
references: []
modDatetime: 2026-05-26 19:02:40.627031+09:00
---

# 什么是 KV Cache？

## 词典定义 (Dictionary Definition)
KV Cache (键值缓存) 是在自回归 (Autoregressive) 大语言模型 (LLM) 推理过程中，为提高运算效率而引入的一种内存优化技术。在 Transformer 架构的自注意力 (Self-Attention) 计算时，它将已经生成的标记 (Token) 所对应的键 (Key) 和值 (Value) 张量存储在 VRAM (显存) 中以便重复使用，而不是每次都重新计算。通过这种机制，可以减少生成新标记时产生的不必要重复运算，从而显著缩短推理延迟 (Latency)。

## 实际应用案例 (Practical Use Case)
该技术被广泛应用于 NVIDIA 驱动的各类推理框架以及 Google 的 Gemma 4 和 DeepSeek-V3 等最新 LLM 架构中，以加速推理过程。特别是通过设计让主模型和轻量级草稿模型共享 KV Cache，可以最大化模型间的数据传输效率，在抑制额外内存消耗的同时，提高整体标记生成速度。

## 相关词汇 (Related Words)
*   投机性解码 (Speculative Decoding)
*   注意力机制 (Attention Mechanism)
*   推理优化 (Inference Optimization)
*   VRAM (Video Random Access Memory)