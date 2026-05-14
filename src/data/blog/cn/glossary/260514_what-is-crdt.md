---
title: "什么是 CRDT？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-14 15:13:45.869153+09:00
slug: "what-is-crdt"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "CRDT (Conflict-free Replicated Data Type，无冲突复制数据类型) 是一种特殊的分布式数据结构，能够在无需额外共识过程的情况下防止数据冲突并保证最终一致性。它是实时协作工具或离线优先应用中维护数据完整性和高可用性的核心技术。"
references: []
modDatetime: 2026-05-14 15:23:45.869153+09:00
---

# 什么是 CRDT？

### 词典定义 (Dictionary Definition)
CRDT (Conflict-free Replicated Data Type，无冲突复制数据类型) 是专为分布式计算环境设计的一种特殊数据结构，旨在让分布在多个节点上的数据副本在无需集中式共识过程的情况下保持一致。即使各个节点独立进行更新，根据数学规则（如交换律、结合律、幂等性等），在合并时也能无冲突地收敛到相同状态。它是 Raft 或 Paxos 等强共识算法的替代方案，用于解决网络延迟或可用性下降问题，并实现最终一致性 (Eventual Consistency)。

### 实际应用案例 (Practical Use Case)
CRDT 主要用于多人同时编辑文档的实时协作工具（如 Figma、Google Docs），或者即使在网络连接不稳定的环境下也需保证数据输入的离线优先 (Offline-first) 应用程序的数据同步。此外，它也被用作 Riak、Redis 等分布式数据库系统中维持节点间数据一致性的机制。

### 相关术语 (Related Words)
- 最终一致性 (Eventual Consistency)
- 分布式共识 (Distributed Consensus)
- 高可用性 (High Availability)