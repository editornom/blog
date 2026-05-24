---
title: "RTT (往返时延)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-24 15:26:59.405265+09:00
slug: "rtt-round-trip-time"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "RTT（Round Trip Time，往返时延）是衡量数据包收发过程的核心指标，也是决定分布式系统共识算法性能和网络可用性的关键因素。"
references: []
modDatetime: 2026-05-24 15:36:59.405265+09:00
---

# 什么是 RTT？

- 词典定义 (Dictionary Definition): RTT（Round Trip Time，往返时延）是指发送端发送的数据包到达接收端，并由接收端返回确认消息到发送端所经历的总时间。它是衡量网络延迟程度最基础的指标。

- 实际应用案例 (Practical Use Case): 在分布式共识协议（如 Raft 或 Paxos）环境中，节点间的数据同步及法定人数（Quorum）达成共识的速度直接取决于节点间的 RTT。如果因网络环境的物理距离或负载导致 RTT 变长，会导致集群状态更新延迟，进而成为系统整体可用性下降的原因。

- 相关词汇 (Related Words): 延迟 (Latency), 法定人数 (Quorum), Ping