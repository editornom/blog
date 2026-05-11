---
title: "What is SFT (Supervised Fine-Tuning)?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 20:50:22.686784+09:00
slug: "what-is-sft"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Supervised Fine-Tuning (SFT) is a core process that aligns pre-trained language models with user intent and enhances specific task performance using high-quality instruction-response datasets. Learn more about the definition and practical use cases of SFT for implementing chatbot services and building domain-specific models."
references: []
modDatetime: 2026-05-11 21:00:22.686784+09:00
---

# What is SFT (Supervised Fine-Tuning)?

### Dictionary Definition
Supervised Fine-Tuning (SFT) is the process of adjusting the weights of a pre-trained Large Language Model (LLM) using high-quality, human-authored 'instruction-response' datasets to enable the model to understand user instructions and generate appropriate responses. This is considered the first critical step in 'Alignment,' moving the model beyond simple statistical next-token prediction and allowing it to master specific task execution and conversational formats according to human intent.

### Practical Use Case
SFT is primarily used before deploying a Large Language Model as a chatbot service. By training the model on tens of thousands of exemplary dialogue samples, developers ensure that the model provides clear and consistent answers. It is also an indispensable step when building domain-specific models, as it allows the AI to learn the specialized terminology and question-and-answer patterns required in professional fields such as medicine or law.

### Related Words
* RLHF (Reinforcement Learning from Human Feedback)
* Instruction Tuning
* Pre-training