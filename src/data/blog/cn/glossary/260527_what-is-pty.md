---
title: "什么是 PTY？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-27 18:48:41.240525+09:00
slug: "what-is-pty"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "深入探讨 PTY（伪终端）的概念与主从结构，介绍 SSH 和终端模拟器等实际应用案例。了解 PTY 如何在无需物理设备的情况下，通过软件处理交互式输入输出的核心原理。"
references: []
modDatetime: 2026-05-27 18:58:41.240525+09:00
---

PTY（Pseudo Terminal，伪终端）是指在没有物理硬件终端设备的情况下，通过软件模拟终端功能的虚拟设备对。它由主（Master）和从（Slave）两个文件接口组成，主进程发送的数据会作为从进程的输入，而从进程的输出则传回主进程。通过这种结构，操作系统可以像连接了实际物理终端一样与进程通信，并处理交互式输入输出。

### 实际应用案例 (Practical Use Case)
1. **远程连接环境**：通过 SSH (Secure Shell) 连接服务器时，服务器会为每个用户会话分配一个 PTY，提供可供用户实时输入命令并查看结果的 Shell 环境。
2. **终端模拟器**：xterm、iTerm2、VS Code 内置终端等现代基于 GUI 的终端软件，在内部分别利用 PTY 与操作系统内核进行通信。
3. **AI 智能体自动化**：当 AI 智能体在沙盒内部直接执行代码或更改系统设置时，通过 PTY 模拟交互式界面，处理实时错误响应及复杂的命令执行。

### 相关术语 (Related Words)
- **TTY (Teletype)**：计算机早期使用的物理电传打字机或系统中终端设备的统称。
- **SSH (Secure Shell)**：用于登录网络中其他计算机或执行远程命令的安全协议，连接会话时会分配 PTY。
- **Shell**：将用户命令传递给操作系统内核的命令行解释器，通常通过 PTY 与用户进行交互。