---
title: "什么是知识蒸馏 (Knowledge Distillation)？"
author: editornom
author_role: "高级技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 15:09:19.640732+09:00
slug: "what-is-knowledge-distillation"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "知识蒸馏 (Knowledge Distillation) 是一种机器学习技术，通过将大型精密模型的知识迁移到轻量级模型中，在最大限度减少性能损失的同时，减小模型体积并优化推理速度。它是通过将高性能教师模型的推理逻辑进行高效资产化，从而以低成本实现精密 AI 服务的核心模型轻量化技术。"
references: []
modDatetime: 2026-05-07 15:19:19.640732+09:00
---

# 什么是知识蒸馏 (Knowledge Distillation)？

### 词典定义 (Dictionary Definition)
知识蒸馏 (Knowledge Distillation) 是一种机器学习技术，旨在将大型且精密的人工智能模型（Teacher Model，教师模型）所拥有的知识迁移到相对较小且高效的模型（Student Model，学生模型）中。其核心是通过利用复杂教师模型的输出值——软目标 (Soft Targets) 作为训练数据，引导学生模型模仿教师模型的推理逻辑，从而在尽量减少性能损失的前提下，缩小模型规模并提升推理速度。

### 实际应用案例 (Practical Use Case)
在 Andrej Karpathy 的 “LLM Wiki” 架构中，该技术被用于将高成本推理模型生成的精密结果提炼并积累为 Markdown 格式的结构化知识。通过这种方式，将单次高成本推理获得的知识转化为资产，使得后续处理类似请求时，可以由低成本的轻量级模型提供即时响应，从而实现系统优化。

### 相关术语 (Related Words)
- 教师模型 (Teacher Model)
- 学生模型 (Student Model)
- 模型轻量化/模型压缩 (Model Compression)