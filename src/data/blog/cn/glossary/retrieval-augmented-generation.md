---
title: "RAG (Retrieval-Augmented Generation)"
author: "editornom"
pubDatetime: 2026-04-16T17:10:54+09:00
slug: "retrieval-augmented-generation"
featured: false
draft: false
tags: ["glossary", "LLM", "GenerativeAI", "AI"]
ogImage: "../../../../../source/glossary/RAG_(Retrieval-Augmented_Generation)/3f23135c-0.png"
description: "本文介绍 RAG（检索增强生成）技术，这是一种通过从外部知识源检索信息并将其整合到生成过程中，以提高大语言模型准确性和可靠性的技术。"
---

![展示 RAG 工作流程的概念图：用户查询触发外部知识库检索，为大语言模型 (LLM) 的响应提供上下文。](../../../../../source/glossary/RAG_(Retrieval-Augmented_Generation)/3f23135c-0.png)

### 1. RAG 核心信息摘要

| 项目 | 内容 |
| :--- | :--- |
| **英文全称** | Retrieval-Augmented Generation |
| **缩写** | RAG |
| **主要相关技术** | LLM, Vector Database, Embedding, Semantic Search, Prompt Engineering |
| **最初提议** | Patrick Lewis et al. (2020) |

### 2. RAG 的概念与定义
检索增强生成 (RAG) 是一种在大型语言模型 (LLM) 生成回答之前，先从外部可靠的数据源中检索相关信息，并将这些内容包含在提示词 (Prompt) 中的技术。其核心在于不单纯依赖模型在预训练阶段学到的知识，而是让模型在回答前实时“查阅”所需信息。通过这种方式，可以克服模型训练数据的局限性，准确传达最新信息或特定领域的专业知识，并能有效抑制 AI 常见的副作用——幻觉 (Hallucination) 现象。

### 3. 技术引入背景
LLM 仅能记住截至预训练 (Pre-training) 完成时的数据。因此，它无法获知训练之后发生的事件，或者企业内部机密数据等未公开信息。当模型被问及不知道的信息时，如果仅依赖内部参数信息，往往会给出看似合理但与事实不符的回答，这就是“幻觉”问题。为了解决这一问题，如果每次都对模型进行微调 (Fine-tuning)，在成本和时间上都会造成巨大负担。RAG 采用了一种另辟蹊径的方法，即从外部存储中查找准确数据并将其作为“参考资料”提供给模型，从而解决这些局限。

### 4. 工作原理及主要特点
*   **检索与信息增强：** 当用户的提问被输入时，系统将其转换为向量，并在向量数据库 (Vector Database) 中查找语义相似的文档片段。接着，将找到的相关信息与用户的原始提问整合在一起，传递给 LLM。
*   **基于证据的回答生成：** LLM 会优先参考提示词中提供的外部文档，而非仅凭自身原有的知识来生成回答。这不仅提高了回答的准确性，还能明确标示出回答所引用的信息来源 (Source)，有利于增强可信度。
*   **知识更新的灵活性：** 无需对模型本身进行重新训练。只需更新外部数据库中的最新信息，模型就能立即给出反映最新情况的回答，从而大幅节省运营资源。

### 5. RAG 与微调 (Fine-tuning) 的区别
*   **RAG：** 保持模型结构不变，通过从外部获取数据来寻找答案，类似于“开卷考试”。优点是信息更新快，且能提供依据。
*   **微调 (Fine-tuning)：** 通过特定数据集直接修改模型参数的“学习”方式。它适用于学习特定的语气、格式或复杂的模式，但每当需要更新知识时都要承担重新训练的成本，且难以完全控制幻觉问题。

### 6. 实务应用案例与相关术语
*   **业务应用：** 企业可以将庞大的内部技术文档或产品手册构建到向量数据库中，进而运行基于此数据库的客户支持 AI 聊天机器人。它可以针对客户的问题实时提供基于手册的准确回答，并附带相关页面的链接。
*   **相关主要术语：**
    1.  **向量数据库 (Vector Database)：** 专门用于存储和检索向量数据的存储库，旨在通过数值计算文本的语义相似性。
    2.  **임베딩 (Embedding)：** 将文本等非结构化数据转换为计算机可以理解和运算的高维向量的核心过程。
    3.  **환각 (Hallucination)：** 指 AI 模型自信地输出与事实不符的信息，并将其视为事实的错误现象。

## ✅ 常见问题 (FAQ)

<details>
  <summary>什么是 RAG？</summary>
  <div class="faq-content">

RAG（检索增强生成）是一种技术，它让大语言模型 (LLM) 在生成回答之前，先从外部可靠的数据源中检索相关信息，并参考这些内容来回答。其核心是让模型不再仅仅依赖已学习的知识，而是实时“查阅”所需信息后做出回答。

  </div>
</details>

<details>
  <summary>RAG 的缩写和中文名称是什么？</summary>
  <div class="faq-content">

英文缩写为 RAG，全称是“Retrieval-Augmented Generation”。中文通常直译为“检索增强生成”。

  </div>
</details>

<details>
  <summary>RAG 技术出现的背景是什么？</summary>
  <div class="faq-content">

因为 LLM 无法获知训练完成后的信息或非公开数据，容易产生“幻觉 (Hallucination)”现象，即给出与事实不符的回答。为了解决这个问题，研究者开发了从外部查找并传递准确数据的方法，而不是每次都重新训练模型。

  </div>
</details>

<details>
  <summary>构建 RAG 系统需要哪些主要技术？</summary>
  <div class="faq-content">

核心技术包括作为回答基础的 LLM，以及用于存储和检索数据的向量数据库 (Vector Database)、将文本数值化的嵌入 (Embedding) 技术，以及基于语义的搜索技术等。

  </div>
</details>

<details>
  <summary>使用 RAG 有哪些优点？</summary>
  <div class="faq-content">

它克服了模型训练数据的局限性，能够准确传达最新信息和专业知识，有效抑制 AI 常见的幻觉现象。此外，由于可以明确提供回答的出处，能为用户提供更高的可信度。

  </div>
</details>

<details>
  <summary>RAG 和微调 (Fine-tuning) 的关键区别是什么？</summary>
  <div class="faq-content">

RAG 像是参考外部资料寻找答案的“开卷考试”，而微调则是通过直接修改模型参数来获取知识的“学习”方式。RAG 的信息更新快且成本低，而微调更擅长掌握特定的语气或格式。

  </div>
</details>

<details>
  <summary>RAG 是如何减少 AI 的“幻觉”现象的？</summary>
  <div class="faq-content">

因为它在提示词中包含了与问题相关的真实文档片段，并指示模型“基于此内容进行回答”，从而防止模型随意捏造答案。通过引导模型生成基于证据的回答，最大限度地减少了事实性错误。

  </div>
</details>

<details>
  <summary>在 RAG 工作流程中，“向量数据库”起什么作用？</summary>
  <div class="faq-content">

它充当存储库的角色。将用户的问题转换为向量后，向量数据库能从海量数据中快速找到语义最相似的文档片段，从而为 LLM 提供最符合提问意图的参考资料。

  </div>
</details>

<details>
  <summary>当有新信息产生时，RAG 系统如何应对？</summary>
  <div class="faq-content">

无需重新训练模型，只需将包含最新信息的文档更新到外部数据库中即可。这使得系统能够实时补充知识，在大幅节省运营资源的同时，始终保持最新状态。

  </div>
</details>

<details>
  <summary>如果企业在实务中引入 RAG，可以用于哪些用途？</summary>
  <div class="faq-content">

可以运行基于企业内部庞大技术文档或产品手册的客户支持 AI 聊天机器人。它能针对客户提问实时提供基于手册的准确回答，并给出依据页面的链接，从而提高工作效率。

  </div>
</details>