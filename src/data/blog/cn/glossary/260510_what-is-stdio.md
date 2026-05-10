---
title: "什么是 STDIO？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-10 17:03:53.759572+09:00
slug: "what-is-stdio"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "本文探讨了 STDIO（标准输入输出）的概念，并结合 MCP 环境下的实际应用案例，深入分析了进程间通信（IPC）的核心原理。介绍了如何利用系统的标准流实现安全高效的数据交换，而无需额外的网络端口。"
references: []
modDatetime: 2026-05-10 17:13:53.759572+09:00
---

### 什么是 STDIO？

#### 词典定义 (Dictionary Definition)
STDIO（Standard Input/Output，标准输入输出）是指计算机操作系统中，为了处理程序与外部环境之间的数据交换而默认连接的输入输出通道，即标准流（Standard Streams）。它通常由标准输入 (stdin)、标准输出 (stdout) 和标准错误 (stderr) 三个通道组成。作为一个抽象接口，STDIO 允许程序在无需关心具体硬件或网络配置的情况下进行数据读写。

#### 实际应用案例 (Practical Use Case)
在 Model Context Protocol (MCP) 规范中，当部署在本地环境的客户端与服务器进程进行通信时，通常会使用系统的 STDIO 作为主要传输通道，而不是开放专门的网络端口。这种方式利用进程间的直接输入输出，不仅降低了数据传输的延迟，还从根本上阻断了通过网络层进行外部访问的可能性，从而显著增强了本地环境的安全性。

#### 相关术语 (Related Words)
- **IPC (Inter-Process Communication)**：指操作系统内进程之间交换数据的机制，而 STDIO 是其中最基础的通信手段之一。
- **JSON-RPC**：一种轻量级的远程过程调用协议，常用于通过 STDIO 流传输结构化的指令和响应。
- **Standard Stream (标准流)**：连接系统终端、输入输出设备与程序之间数据流的标准模型的总称。