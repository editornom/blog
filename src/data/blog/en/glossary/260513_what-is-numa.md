---
title: "What is NUMA (Non-Uniform Memory Access)?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 11:36:42.093125+09:00
slug: "what-is-numa"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "NUMA (Non-Uniform Memory Access) is a multiprocessor system architecture where memory access speed varies based on the processor's location. This post defines NUMA and analyzes performance issues that can arise in environments such as MPI applications."
references: []
modDatetime: 2026-05-13 11:46:42.093125+09:00
---

# What is NUMA (Non-Uniform Memory Access)?

## Definition
NUMA (Non-Uniform Memory Access) is a multiprocessor system architecture where each processor (or processor group) is assigned its own dedicated local memory. While a processor can access its local memory at high speeds, accessing the local memory of another processor (remote memory) results in relatively higher latency and slower speeds. This occurs when physical memory is partitioned and allocated across multiple sockets, characterizing the non-uniformity of memory access performance.

## Practical Use Cases
In high-performance computing (HECC) environments such as those used by NASA, NUMA architecture can lead to memory starvation and performance degradation when running MPI (Message Passing Interface) based applications, particularly when combined with page cache monopoly issues. If a specific process monopolizes the memory of its local socket, other processes are forced to access remote socket memory with significantly slower data transfer rates, which can drastically reduce overall computational efficiency.

## Related Terms
- Page Cache
- MPI (Message Passing Interface)
- Direct I/O