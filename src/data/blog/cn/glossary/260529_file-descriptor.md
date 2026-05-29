---
title: "文件描述符"
author: editornom
author_role: "资深技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 15:43:58.422341+09:00
slug: "file-descriptor"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "了解在类 Unix 操作系统中用于访问文件、套接字等 I/O 资源的非负整数——文件描述符的定义与特征。通过 I/O 多路复用等实际应用案例，详细阐述高效管理系统资源的原理。"
references: []
modDatetime: 2026-05-29 15:53:58.422341+09:00
---

# 什么是文件描述符？

### 词典定义 (Dictionary Definition)
在 Unix 及类 Unix 操作系统中，文件描述符（File Descriptor）是进程用于访问文件、套接字、管道等各种输入/输出资源的抽象非负整数（Non-negative Integer）。当进程打开资源时，由内核进行分配，并作为该进程文件描述符表内指向特定资源的索引。

### 实际应用案例 (Practical Use Case)
在网络服务器架构中，当发生客户端连接时，操作系统会为该套接字创建一个文件描述符。在解决 C10K 问题的 I/O 多路复用过程中，select() 或 poll() 等函数接收多个文件描述符作为参数，监控其是否收到数据，并仅筛选出实际有数据到达的文件描述符进行处理，从而实现对系统资源的高效管理。

### 相关词汇 (Related Words)
- 套接字 (Socket)
- I/O 多路复用 (I/O Multiplexing)
- 内核 (Kernel)