---
title: "What is KV Cache?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-26 18:52:40.627031+09:00
slug: "kv-cache"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "KV Cache is a technology that optimizes memory efficiency and accelerates generation speed by storing and reusing computation results of previous tokens in VRAM during LLM inference."
references: []
modDatetime: 2026-05-26 19:02:40.627031+09:00
---

# What is KV Cache?

## Dictionary Definition
KV Cache (Key-Value Cache) is a memory optimization technique introduced to improve computational efficiency during the inference process of autoregressive Large Language Models (LLMs). Within the self-attention mechanism of the Transformer architecture, it refers to the process of storing the Key and Value tensors calculated for previously generated tokens in VRAM (Video RAM) and reusing them, rather than recalculating them for every new token. This significantly reduces inference latency by eliminating redundant repetitive computations during the generation of subsequent tokens.

## Practical Use Case
KV Cache is utilized to accelerate inference in modern LLM architectures, such as Google's Gemma and DeepSeek-V3. In particular, it is used to maximize data transfer efficiency between models and suppress additional memory consumption by allowing a main model and a lightweight draft model to share the KV Cache, thereby increasing the overall token generation speed.

## Related Words
*   Speculative Decoding
*   Attention Mechanism
*   Inference Optimization
*   VRAM (Video Random Access Memory)