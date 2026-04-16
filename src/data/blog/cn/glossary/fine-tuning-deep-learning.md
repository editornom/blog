---
title: "微调 (Fine-tuning)"
author: "Antigravity"
pubDatetime: 2026-04-16T17:43:55+09:00
slug: "fine-tuning-deep-learning"
featured: false
draft: false
tags: ["glossary", "deep-learning", "transfer-learning", "AI"]
ogImage: "../../../../../source/glossary/fine-tuning/ef69ec01-0.png"
description: "介绍微调（Fine-tuning）的定义和原理。微调是一种深度学习技术，通过对预训练模型进行针对特定任务或领域的追加训练，从而优化模型性能。"
---

![展示预训练层和特定任务更新的神经网络微调过程示意图](../../../../../source/glossary/fine-tuning/ef69ec01-0.png)

| 项目 | 内容 |
| :--- | :--- |
| **英文名称** | Fine-tuning |
| **中文名称** | 微调 |
| **缩写** | - |
| **相关技术** | 迁移学习 (Transfer Learning), 深度学习, LLM, PEFT, LoRA |

### 针对特定任务优化模型的过程
微调是以已经在海量数据上完成学习的基础模型（Pre-trained Model）的权重作为起点，使用具有特定目的的数据集进行追加训练的技术。它是迁移学习（Transfer Learning）的一种，核心在于将具备通用知识的模型优化为适用于特定任务（Downstream Task）或专业垂直领域的专用模型。

### 高效的模型训练与专业性提升
从零开始训练（Training from scratch）大语言模型（LLM）或大规模神经网络需要天文数字般的计算资源和时间。微调可以显著减轻这种成本负担。由于模型已经掌握了通用的特征识别能力，因此只需少量的训练数据和资源，即可满足医疗咨询或法律文档摘要等需要高度专业性的业务需求。

### 微调的核心机制
*   **权重更新策略**：可以根据具体情况选择重新训练模型所有参数的“全参数微调（Full Fine-tuning）”，或是仅训练特定层而固定其他层的“冻结（Freezing）”技术。近期，旨在最大化效率的参数高效微调（PEFT）技术正成为主流。
*   **LoRA 等高效技术应用**：在保持模型结构不变的同时，仅插入少量额外参数（Adapter），或利用低秩矩阵调整权重的 LoRA（Low-Rank Adaptation）方式也被广泛应用。这种方式能大幅节省显存和计算成本。
*   **领域适应与性能提升**：通过学习在通用数据集中难以接触到的行业术语或特有模式，提高模型在特定任务中的回答准确度和语境理解能力。

### 与预训练 (Pre-training) 的区别
如果说预训练是利用大规模无标签数据构建模型基础智能和表达能力的阶段，那么微调则可以理解为利用带标签的特定数据对已构建的模型进行精雕细琢的优化阶段。这好比是在已经完成基础工程建设的大楼中，根据特定用途进行内部装修。

### 实际应用案例与主要概念
*   **实务应用案例**：如果将企业内部的技术文档和手册对通用 GPT 模型进行微调，就可以创建一个专门针对该企业产品提供专业咨询的客户支持聊天机器人。
*   **相关术语**：
    *   **PEFT (Parameter-Efficient Fine-tuning)**：指仅修改极少数参数来高效改进模型的技术。
    *   **RLHF (Reinforcement Learning from Human Feedback)**：指引入人类反馈，使模型的回答与用户的意图及价值观保持一致（Alignment）的技术。
    *   **Catastrophic Forgetting (灾难性遗忘)**：指在学习新数据时，模型遗忘之前学到的通用知识的现象。这是在微调过程中必须关注的风险点。

## ✅ 常见问题 (FAQ)

<details>
  <summary>什么是微调 (Fine-tuning)？</summary>
  <div class="faq-content">

微调是一种深度学习技术，它以已经在海量数据上训练过的基础模型为基础，使用针对特定目的的数据集进行追加训练以实现优化。它是迁移学习的一种，旨在将具备通用知识的模型调整为适用于医疗、法律等专业领域或特定任务的模型。

  </div>
</details>

<details>
  <summary>微调为什么重要？</summary>
  <div class="faq-content">

因为它能显著减少从零开始训练大型模型所需的海量时间和成本。通过复用已训练模型的智能，仅需较少的数据和计算资源即可实现高性能的专业化模型。

  </div>
</details>

<details>
  <summary>预训练 (Pre-training) 和微调有什么区别？</summary>
  <div class="faq-content">

预训练是利用大规模数据构建基础智能和表达能力的阶段，而微调则是针对特定任务对其进行精细打磨的优化阶段。可以将其比喻为在完成主体建设的房屋内根据用途进行装修的过程。

  </div>
</details>

<details>
  <summary>PEFT (Parameter-Efficient Fine-tuning) 是什么技术？</summary>
  <div class="faq-content">

这是一种“参数高效微调”技术，它通过仅修改最少量的参数而非整个模型来高效提升性能。这可以在保持模型整体性能的同时，大幅节省计算成本和显存占用。

  </div>
</details>

<details>
  <summary>通过微调可以获得什么样的预期效果？</summary>
  <div class="faq-content">

通过学习通用数据集中罕见的行业术语或特有模式，可以提高模型在特定任务中的回答准确率。最终能够获得符合业务需求语境的理解能力和专业性。

  </div>
</details>

<details>
  <summary>微调过程中有哪些权重更新策略？</summary>
  <div class="faq-content">

主要有重新训练模型全部参数的“全参数微调”方式，以及仅训练特定层而固定其他层的“冻结（Freezing）”技术。目前为了追求极致效率，应用 LoRA 等适配器（Adapter）的方法非常流行。

  </div>
</details>

<details>
  <summary>LoRA (Low-Rank Adaptation) 方式的优点是什么？</summary>
  <div class="faq-content">

它是在保持模型结构不变的前提下，利用低秩矩阵仅学习少量额外参数的方式。与全量微调相比，它在显存和计算成本极低的情况下，能够获得类似的性能提升。

  </div>
</details>

<details>
  <summary>微调时需要注意的“灾难性遗忘 (Catastrophic Forgetting)”是什么？</summary>
  <div class="faq-content">

是指在学习新的特定数据过程中，模型忘掉了之前学到的通用知识的现象。如果模型过度优化于某一特定领域，其通用能力可能会下降，因此需要引起注意。

  </div>
</details>

<details>
  <summary>RLHF (Reinforcement Learning from Human Feedback) 与微调是什么关系？</summary>
  <div class="faq-content">

这是一种通过引入人类反馈，使模型的回答符合用户意图和伦理标准的对齐（Alignment）技术。它常作为微调的一个环节，引导模型给出更有用且更安全的回答。

  </div>
</details>

<details>
  <summary>在实际业务中引入微调时需要考虑的核心要素是什么？</summary>
  <div class="faq-content">

最重要的是获取适合解决目标问题的高质量带标签数据。此外，还需要根据项目的预算和时间限制，决定是进行全参数微调，还是使用 PEFT 等高效技术。

  </div>
</details>