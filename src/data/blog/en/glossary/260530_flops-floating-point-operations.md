---
title: "FLOPs (Floating Point Operations per Second)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-30 19:36:48.490759+09:00
slug: "flops-floating-point-operations"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Explore the definition of FLOPs and its role as a key metric for quantifying computational resources in AI training and inference, covering calculation methods and practical use cases."
references: []
modDatetime: 2026-05-30 19:46:48.490759+09:00
---

# What is FLOPs?

### Dictionary Definition
FLOPs (Floating Point Operations per Second) is a unit used to measure the number of floating-point operations a computer can perform in one second. It is a primary benchmark for representing computational performance. In the field of Artificial Intelligence (AI), it is also widely used as a metric to represent the total amount of computation (Total Floating Point Operations) required during the training or inference of Large Language Models (LLMs). This is closely linked to the number of model parameters and the volume of training data, serving as a core variable for quantifying the scale of computing resources invested in enhancing AI performance.

### Practical Use Cases
1. When developing AI models, the total FLOPs required for full training are calculated to predict the necessary GPU resources and cloud computing costs in advance.
2. Lightweight algorithms that consume fewer FLOPs while maintaining the same performance are developed to increase the efficiency of On-device AI.
3. When comparing the performance of AI accelerators like the NVIDIA H100, the processing capacity is measured in units of Teraflops (TFLOPS) or Petaflops (PFLOPS).

### Related Terms
* **Scaling Laws**: A principle stating that model performance improves predictably as computing resources (Compute), data size, and the number of parameters increase.
* **Chinchilla Law**: A rule that defines the optimal ratio between the number of model parameters and the amount of data to achieve peak performance within a given compute (FLOPs) budget.
* **Compute**: Refers to the processing power of the hardware and the total amount of resources invested to process the operations of an AI model.