---
title: "分布式追踪"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-22 11:44:59.981016+09:00
slug: "distributed-tracing"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "分布式追踪是一种在 MSA 和无服务器环境中通过跟踪请求的完整路径来确保系统可观测性的监控技术。它能够将服务间的调用关系和处理时间可视化，从而快速定位并解决性能瓶颈或错误发生点。"
references: []
modDatetime: 2026-05-22 11:54:59.981016+09:00
---

# 分布式追踪是什么？

### 定义 (Dictionary Definition)
分布式追踪 (Distributed Tracing) 是一种在微服务架构 (MSA) 或无服务器 (Serverless) 环境等分布式系统结构中，跟踪并记录单个请求所经过的所有路径的监控技术。通过将各服务间的调用关系和处理时间可视化，以确保整个系统的可观测性 (Observability)，并用于准确识别性能瓶颈或错误发生的具体位置。

### 实际应用案例 (Practical Use Case)
在错综复杂的无服务器微服务环境中，当特定 API 的响应速度比平时变慢时，可以利用分布式追踪工具实时查看是在哪个阶段的函数 (Function) 或数据库调用中产生了延迟，并据此采取针对性措施。

### 相关术语 (Related Words)
* 可观测性 (Observability)
* 微服务架构 (MSA)
* 厂商锁定 (Vendor Lock-in)