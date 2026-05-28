---
title: "LWW (Last-Write-Wins)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-28 15:44:09.776756+09:00
slug: "lww-last-write-wins"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "LWW (Last-Write-Wins) 是一种分布式系统中的确定性算法，通过根据时间戳选择最新数据来解决冲突。它是 NoSQL 数据库实现最终一致性的核心策略，具有简单、高效处理数据的优点。"
references: []
modDatetime: 2026-05-28 15:54:09.776756+09:00
---

# 什么是 LWW (Last-Write-Wins)？

### 词典定义 (Dictionary Definition)
LWW (Last-Write-Wins) 是一种用于解决分布式计算及分布式数据库系统中数据冲突的确定性算法。当多个节点对同一数据发出不同的写入请求时，系统会比较每个请求附带的时间戳 (Timestamp)，仅保留最近的一次记录作为最终数据，并丢弃其余之前的记录。该算法实现简单，系统负载低且处理速度快，但也存在由于分布式节点间的时钟同步 (Clock Synchronization) 误差或并发请求导致有效数据被覆盖的“数据丢失 (Data Loss)”风险。

### 实务应用案例 (Practical Use Case)
LWW 被广泛用作 Apache Cassandra、Amazon DynamoDB、Couchbase 等重视可用性和分区容错性 (AP) 的 NoSQL 数据库实现最终一致性 (Eventual Consistency) 的基本策略。例如，当不同地区的服务器节点几乎同时修改同一用户的地址信息时，系统会根据时间戳大小，将数值较大的节点信息更新为最终地址，并将其同步到所有节点。

### 相关术语 (Related Words)
- CAP 定理 (CAP Theorem)
- 最终一致性 (Eventual Consistency)
- 冲突解决 (Conflict Resolution)