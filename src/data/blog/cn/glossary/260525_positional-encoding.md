---
title: "什么是位置编码 (Positional Encoding)？"
author: editornom
author_role: "高级技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-25 21:16:19.412845+09:00
slug: "positional-encoding"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "本文介绍了在 Transformer 架构中注入输入数据顺序信息的位置编码 (Positional Encoding) 的概念及实际应用案例。涵盖了通过在词嵌入中加入位置信息，帮助模型准确识别序列内上下文的核心原理。"
references: []
modDatetime: 2026-05-25 21:26:19.412845+09:00
---

### 词典定义 (Dictionary Definition)
位置编码 (Positional Encoding) 是一种在 Transformer 架构等并行处理数据的神经网络模型中，为了注入输入数据的顺序或位置信息而使用的技术。与循环神经网络 (RNN) 不同，Transformer 同时处理句子中的所有单词，因此在结构上无法直接掌握单词的排列顺序。为了解决这一问题，通过在每个单词的嵌入向量 (Word Embedding) 中加上包含位置信息的独特向量值，帮助模型识别序列中数据的相对或绝对位置。通常利用基于正弦 (Sine) 和余弦 (Cosine) 函数的周期性函数值来生成这些位置向量。

### 实际应用案例 (Practical Use Case)
该技术被广泛应用于大语言模型 (AI/LLM) 的文本生成过程中，以准确把握句子的含义。例如，“张三喜欢李四”和“李四喜欢张三”这两句话虽然组成单词完全相同，但根据单词顺序的不同，主语和宾语也会随之改变，从而导致含义完全不同。位置编码将这些词序信息数值化并传递给模型，确保即使是相同的单词，也能根据其在句子中位置的不同，被作为不同的上下文进行处理。

### 相关词汇 (Related Words)
- Transformer Architecture
- Self-Attention
- Word Embedding