---
title: "什么是 SRv6 (IPv6 分段路由)？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 17:07:47.039006+09:00
slug: "srv6-ipv6-segment-routing-technology"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "SRv6 (IPv6 分段路由) 是一种基于 IPv6 的分段路由技术，在大规模基础设施运营中提供卓越的扩展性和灵活的流量控制功能。它是能够像 OpenAI 的 MCR 架构一样，实现大规模 GPU 集群低延迟通信和高效网络运营的下一代协议。"
references: []
modDatetime: 2026-05-07 17:17:47.039006+09:00
---

# 什么是 SRv6 (IPv6 分段路由)？

### 词典定义 (Dictionary Definition)
SRv6 (IPv6 Segment Routing) 是基于 IPv6 数据平面并应用了分段路由 (Segment Routing) 技术的新一代网络协议。发送端节点显式指定数据包必须经过的路径及要执行的操作，并将这些信息封装在 IPv6 报头的分段路由扩展报头 (SRH) 中进行传输。由于中间节点无需维护复杂的网络状态信息，SRv6 在大规模基础设施运营中展现出卓越的扩展性和灵活的流量控制能力。

### 实际应用案例 (Practical Use Case)
OpenAI 的 MCR (Multipath Reliable Connection) 架构是引入 SRv6 以最大化大规模 GPU 集群通信效率的代表性案例。通过将传统的复杂多层结构简化为两层 (2-Tier)，该架构实现了数万个 GPU 的低延迟连接并有效降低了功耗。然而，由于发送方掌握路径选择权，这种特性可能会绕过传统的集中式网络安全策略，因此在设计基础设施时，必须进行严谨的安全审查。

### 相关术语 (Related Words)
- IPv6：SRv6 技术运行的基础，是下一代互联网协议地址体系。
- Segment Routing (SR)：一种将网络路径定义为一系列分段列表，从而实现基于源路由 (Source Routing) 的技术。
- MCR (Multipath Reliable Connection)：为了提升 AI 模型的训练与推理性能，应用了基于 SRv6 的网络优化协议。