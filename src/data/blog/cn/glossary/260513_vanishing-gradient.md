---
title: "什么是梯度消失？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 20:18:00.657625+09:00
slug: "vanishing-gradient"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "深入探讨梯度消失（Vanishing Gradient Problem）的定义与产生原因，并介绍 LSTM、Transformer 等解决该问题的实战深度学习技术。"
references: []
modDatetime: 2026-05-13 20:28:00.657625+09:00
---

# 什么是梯度消失？

### 词典定义 (Dictionary Definition)
梯度消失（Vanishing Gradient Problem）是指在人工神经网络的训练过程中，执行反向传播（Backpropagation）算法时，从输出层向输入层传导的梯度（Gradient）随着经过的层数增多而逐渐变小，最终趋近于零的现象。这会导致神经网络层数越深，权重更新就越缓慢甚至停滞，是造成模型无法有效学习数据中长期依赖（Long-term Dependency）关系的主要原因。

### 实务应用案例 (Practical Use Case)
该问题常出现在使用循环神经网络（RNN）结构处理长序列数据时。一个典型的例子是，随着句子长度的增加，位于句子开头的单词信息无法有效传递到末尾，导致信息遗忘。为了解决这一问题，业界开发了 LSTM（Long Short-Term Memory）或 GRU（Gated Recurrent Unit）等特殊架构。而近年来，Transformer 架构通过 Attention 机制直接计算序列中任意两个位置之间的关系，从而在根本上规避了这一问题。

### 相关词汇 (Related Words)
* 反向传播 (Backpropagation)
* 循环神经网络 (RNN)
* 长期依赖 (Long-term Dependency)