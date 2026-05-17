---
title: "什么是 GRPO？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-17 19:09:52.295471+09:00
slug: "what-is-grpo"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "GRPO（Group Relative Policy Optimization）是一种强化学习技术，它无需独立的奖励模型，通过比较组内响应的相对表现来优化模型的推理能力。该技术解决了传统 RLHF 的成本问题，在数学和编码等需要逻辑验证的大语言模型训练中非常有效。"
references: []
modDatetime: 2026-05-17 19:19:52.295471+09:00
---

# 什么是 GRPO？

### 词典定义
GRPO（Group Relative Policy Optimization）是一种在人工智能强化学习过程中，无需构建独立奖励模型（Reward Model），而是通过比较生成的响应组内的相对表现来优化模型策略的技术。该方法的提出是为了解决传统 RLHF（基于人类反馈的强化学习）方式中存在的高昂计算成本和奖励黑客（Reward Hacking）问题。这种方式不以单个响应的绝对分数为指标，而是以相对于组内平均水平的表现作为参考，从而引导模型学习更加逻辑化且可验证的推理过程。

### 实际应用案例
GRPO 主要用于训练需要验证正确答案和逻辑路径的推理型大语言模型（LLM），例如数学解题、编程代码生成等场景。其运作方式是让模型针对同一个问题生成多个候选答案，然后在组内为最准确、最有效的答案赋予更高的权重，以此来不断进化模型的推理能力。

### 相关术语
- RLHF (Reinforcement Learning from Human Feedback)
- DPO (Direct Preference Optimization)
- 奖励黑客 (Reward Hacking)
- 推理模型 (Reasoning Model)