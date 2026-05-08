---
title: "什么是 OpenTelemetry？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 14:19:31.002554+09:00
slug: "what-is-opentelemetry"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "OpenTelemetry 是由 CNCF 托管的开源可观测性框架，它以标准化的方式收集和传输链路追踪、指标及日志数据，且不受特定厂商限制。它为在复杂的微服务架构 (MSA) 环境中确保系统可见性及分析性能提供了不可或缺的工具和技术。"
references: []
modDatetime: 2026-05-08 14:29:31.002554+09:00
---

# 什么是 OpenTelemetry？

### 定义 (Definition)
OpenTelemetry (OTel) 是由云原生计算基金会 (CNCF) 主导的一个开源可观测性 (Observability) 框架。它提供了一套标准化的 API、SDK 和工具集，用于生成、收集、处理及传输链路追踪 (Traces)、指标 (Metrics) 和日志 (Logs) 等遥测数据，以分析软件的性能和状态。其目的是通过建立不依赖于特定厂商的数据标准，在分布式系统环境中实现统一的可观测性。

### 实际应用场景 (Practical Use Case)
在微服务架构 (MSA) 环境中，OpenTelemetry 主要用于实现分布式链路追踪，以跟踪服务间的调用路径。开发人员通过将 OpenTelemetry SDK 集成到应用程序中，可以掌握用户请求在经过多个服务器过程中产生的延迟和错误。特别是当它与 eBPF 等内核级数据收集技术互补结合时，可以实现将基础设施硬件指标与应用程序业务逻辑上下文相结合的综合分析。

### 相关术语 (Related Words)
* 可观测性 (Observability)
* 分布式链路追踪 (Distributed Tracing)
* CNCF (Cloud Native Computing Foundation)