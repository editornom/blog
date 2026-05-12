---
title: "什么是 AF_ALG？"
author: editornom
author_role: "高级技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 11:30:06.736176+09:00
slug: "what-is-af-alg"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "AF_ALG 是一个 Linux 内核接口，允许用户空间应用程序通过标准 Socket API 访问加密算法和硬件加速。本概览涵盖了其技术实现、使用 splice() 等系统调用的实际用法，以及其与 CVE-2026-31431 等安全漏洞的相关性。"
references: []
modDatetime: 2026-05-08 11:40:06.736176+09:00
---## 什么是 AF_ALG？

### 定义 (Definition)
AF_ALG 是 Linux 内核提供的一个用于访问加密子系统的用户空间 (User-space) 接口。它是“Address Family - Algorithm”的缩写，是专为用户空间应用程序设计的通道，使其能够通过标准 Socket API 调用内核中实现的加密算法（如 AES、SHA、HMAC 等）。它支持利用硬件加速器等内核级资源，从而实现高效的加密运算。

### 实际应用案例 (Practical Use Case)
- <b>调用内核加密引擎</b>：当用户空间程序需要使用内核加密模块处理数据时，会创建一个套接字 (socket)，并通过 bind() 和 accept() 函数连接到特定的算法进行操作。
- <b>与系统调用的交互</b>：它常与 splice() 系统调用结合使用，以优化数据复制过程或处理加密数据。最近，针对该过程中设计缺陷的 CVE-2026-31431 (Copy Fail) 漏洞案例，使得 AF_ALG 与 splice() 的交互成为了研究通过此类手段进行权限提升攻击的重点对象。

### 相关术语 (Related Words)
- CVE-2026-31431 (Copy Fail)
- splice() 系统调用
- Linux 内核加密 API (Crypto API)
- 页缓存污染 (Page Cache Corruption)
