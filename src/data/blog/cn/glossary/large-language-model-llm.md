---
title: "大语言模型 (Large Language Model)"
author: "editornom"
pubDatetime: 2026-04-16T15:09:54+09:00
slug: "large-language-model-llm"
featured: false
draft: false
tags: ["glossary", "Artificial-Intelligence", "Deep-Learning", "NLP"]
ogImage: "../../../../../source/glossary/Large_Language_Model/54353314-0.png"
description: "本文介绍大语言模型 (LLM) 的定义及其核心技术。LLM 是一种通过学习海量文本数据，实现自然语言生成、翻译及推理的人工智能模型。"
---

![处理海量文本数据流并生成类人语言输出的神经网络结构概念可视化](../../../../../source/glossary/Large_Language_Model/54353314-0.png)

### 1. 主要信息摘要

| 项目 | 内容 |
| :--- | :--- |
| **英文名** | Large Language Model |
| **缩写** | LLM |
| **相关技术** | Transformer, Deep Learning, Tokenization, RLHF, RAG |

### 2. 大语言模型 (LLM) 的定义
大语言模型 (LLM) 是旨在通过学习海量文本数据来理解和生成人类语言的人工智能模型。它基于数亿甚至更多数量级的参数构建，主要利用 Transformer 架构来把握上下文语境。除了简单的文本生成，它还能胜任摘要、翻译以及复杂的逻辑推理等各种高级语言处理任务。

### 3. 技术背景
LLM 的出现源于对传统 RNN（循环神经网络）或 LSTM 模型结构局限性的突破。在以往的模型中，随着句子变长，往往会出现由于无法保留前期信息而导致的“长期依赖”问题，以及串行计算导致的训练速度缓慢等顽疾。2017 年 Google 发布的基于 Attention 机制的 Transformer 架构实现了数据的并行处理，大幅提升了训练效率。得益于计算资源的增长和大规模互联网数据的结合，如今的 LLM 时代正式开启。

### 4. 核心原理与主要特征
*   **Transformer 架构：** 通过 Self-Attention 机制同时计算句子中所有单词之间的关系。其核心优势在于能够精确捕捉物理位置较远的单词之间的语境联系。
*   **预训练与微调：** 首先通过非结构化数据进行预训练 (Pre-training)，学习语言的通用结构。随后，通过指令微调 (Instruction Tuning) 针对特定任务进行优化，或通过反映人类反馈的强化学习 (RLHF) 过程来提升回答的适切性。
*   **扩展法则与涌现能力：** 模型的性能随着参数量、数据规模和计算能力的增加而呈指数级提升。特别是当规模超过特定阈值时，模型会展现出以往小规模模型所不具备的高阶推理能力，业界称之为“涌现能力 (Emergent abilities)”。

### 5. LLM 与 SLM 的区别
如果说 LLM 是精通所有领域的全能型选手，那么 **SLM (Small Language Model, 小语言模型)** 则更像是专注于特定目的的专家。虽然 LLM 展现出压倒性的性能，但其构建和运营需要耗费巨大的成本和计算资源。相比之下，SLM 通过优化参数数量，旨在特定领域（如医疗、法律、金融等）发挥高效性能。由于其轻量化和运行速度快的特点，SLM 成为对安全性要求较高的私有网络环境或端侧 AI (On-device AI) 实现的更佳选择。

### 6. 实际应用与主要术语
*   **实战应用案例：** 代表性应用是利用企业内部知识库构建聊天机器人。当用户提问时，通过 **RAG (检索增强生成)** 技术先检索公司内部文档，然后再给出回答。这种方式可以有效减少 LLM 将错误信息当作事实陈述的“幻觉 (Hallucination)”现象，提高回答的可信度。
*   **相关术语整理：**
    1.  **Tokenization：** 将文本拆分为模型可处理的最小单位“Token”的预处理过程。
    2.  **Prompt Engineering：** 为了从模型中获得理想结果，对输入值（问题）进行精细设计和优化的技术。
    3.  **Multimodality：** 不仅是文本，还具备同时理解和生成图像、声音、视频等不同形式数据的能力。

## ✅ 常见问题解答 (FAQ)

<details>
  <summary>什么是大语言模型 (LLM)？</summary>
  <div class="faq-content">

LLM 是一种旨在通过学习海量文本数据来理解和生成人类语言的人工智能模型。它基于数亿个以上的参数，其特点是除了简单的文案撰写外，还能执行摘要、翻译以及复杂的逻辑推理。

  </div>
</details>

<details>
  <summary>作为 LLM 核心的 Transformer 架构起什么作用？</summary>
  <div class="faq-content">

Transformer 是一种通过 Self-Attention 机制同时计算句子内所有单词之间关系的技术。通过这种方式，即使句子变长，模型也不会遗忘前面的信息，从而精确把握上下文，并通过数据并行处理大幅提升训练速度。

  </div>
</details>

<details>
  <summary>LLM 中所说的“涌现能力 (Emergent abilities)”是什么意思？</summary>
  <div class="faq-content">

它是指当模型的参数数量和数据规模超过特定阈值时，突然出现以前的小型模型中不曾见到的高阶推理能力的现象。这是根据扩展法则 (Scaling Law)，随着计算资源和数据的增加，模型能力飞跃式提升过程中产生的现象。

  </div>
</details>

<details>
  <summary>LLM 训练过程中的“预训练”和“微调”有什么区别？</summary>
  <div class="faq-content">

预训练是初始阶段，通过大规模非结构化数据学习语言的通用结构和知识。微调则是优化阶段，通过针对特定任务调整模型或通过反映人类反馈的强化学习 (RLHF) 来提高回答的适切性和准确度。

  </div>
</details>

<details>
  <summary>什么是分词 (Tokenization)，它为什么重要？</summary>
  <div class="faq-content">

分词是将文本拆分为模型可以处理的最小单位“Token”的预处理过程。由于人工智能并不是直接理解文本，而是通过这些分词后的数字进行运算，因此高效的分词直接影响模型的性能和成本。

  </div>
</details>

<details>
  <summary>LLM 和小语言模型 (SLM) 的主要区别是什么？</summary>
  <div class="faq-content">

LLM 是消耗巨大资源的通用模型，而 SLM 是通过优化参数数量、专注于特定目的（医疗、法律等）的模型。由于 SLM 轻量且快速，在安全性要求高的私有网络环境或在设备本身运行的端侧 AI 实现中更具优势。

  </div>
</details>

<details>
  <summary>如何解决 LLM 引入时产生的“幻觉 (Hallucination)”现象？</summary>
  <div class="faq-content">

幻觉是指模型将错误信息当作事实陈述的现象。为了解决这一问题，主要采用 RAG (检索增强生成) 技术。通过让模型先参考与问题相关的可靠外部文档后再生成回答，可以显著提高信息的准确度。

  </div>
</details>

<details>
  <summary>实战中经常提到的 RAG (检索增强生成) 具体是什么？</summary>
  <div class="faq-content">

RAG 是一种不完全依赖模型自身知识，而是实时从企业知识库或外部数据库中检索相关信息并将其作为回答依据的技术。通过这种方式可以提高回答的可信度，并实时反映最新信息。

  </div>
</details>

<details>
  <summary>为什么提示词工程 (Prompt Engineering) 很重要？</summary>
  <div class="faq-content">

因为根据提问（输入值）的形式，LLM 输出结果的质量会有很大差异。通过精细设计和优化提问方式，让模型准确理解上下文，可以更高效地获得所需形式的高质量回答。

</details>

<details>
  <summary>多模态 (Multimodality) 对 LLM 的未来有什么影响？</summary>
  <div class="faq-content">

多模态是超越文本，同时理解和生成图像、声音、视频等多种形式数据的能力。通过多模态，LLM 可以结合视觉信息或听觉语境，实现更接近人类的综合思考和交互。

  </div>
</details>