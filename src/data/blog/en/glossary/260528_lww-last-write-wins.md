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
description: "LWW (Last-Write-Wins) is a deterministic algorithm that resolves conflicts in distributed systems by selecting the most recent data based on timestamps. It is a core strategy for achieving eventual consistency in NoSQL databases, enabling simple and high-speed data processing."
references: []
modDatetime: 2026-05-28 15:54:09.776756+09:00
---

# What is LWW (Last-Write-Wins)?

### Dictionary Definition
LWW (Last-Write-Wins) is a deterministic algorithm used to resolve data conflicts that occur in distributed computing and distributed database systems. When multiple write requests for the same piece of data occur across different nodes, the system compares the timestamp assigned to each request. It adopts only the most recent record as the final state and discards the previous ones. While its simple implementation results in low system overhead and high processing speeds, it carries the risk of "Data Loss," where valid data may be overwritten due to clock synchronization errors between distributed nodes or during concurrent request spikes.

### Practical Use Case
LWW is utilized as a default strategy for achieving Eventual Consistency in NoSQL databases that prioritize availability and partition tolerance (AP), such as Apache Cassandra, Amazon DynamoDB, and Couchbase. For example, if a user's address information is modified almost simultaneously on server nodes in different geographical regions, the system updates the final address using the information from the node with the higher timestamp value and propagates this change to all other nodes.

### Related Words
- CAP Theorem
- Eventual Consistency
- Conflict Resolution