---
title: "What is Positional Encoding?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-25 21:16:19.412845+09:00
slug: "positional-encoding"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "This article explains the concept of Positional Encoding, a technique used to inject sequence order information into input data within the Transformer architecture, along with its practical applications."
references: []
modDatetime: 2026-05-25 21:26:19.412845+09:00
---

### Dictionary Definition
Positional Encoding is a technique used to inject information regarding the order or position of input data into neural network models that process data in parallel, such as the Transformer architecture. Unlike Recurrent Neural Networks (RNNs), Transformers process all words in a sentence simultaneously, which means they inherently lack the structural capacity to perceive the sequence of words. To resolve this, unique vector values representing positional information are added to each word's embedding vector. This allows the model to recognize the relative or absolute position of data within a sequence. It typically utilizes values derived from periodic functions, such as Sine and Cosine functions.

### Practical Use Case
It is widely used in the text generation process of Large Language Models (LLMs) to accurately grasp the contextual meaning of sentences. For example, the sentences 'Alice likes Bob' and 'Bob likes Alice' contain the exact same words, but the meaning changes entirely as the subject and object are determined by word order. Positional Encoding quantifies this word order information and transmits it to the model, ensuring that the same word is processed in different contexts depending on its specific position in the sequence.

### Related Words
- Transformer Architecture
- Self-Attention
- Word Embedding