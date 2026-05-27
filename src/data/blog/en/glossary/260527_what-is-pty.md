---
title: "What is PTY?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-27 18:48:41.240525+09:00
slug: "what-is-pty"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Explore the concept of PTY (Pseudo Terminal) and its master-slave architecture, along with practical use cases such as SSH and terminal emulators. Learn how PTY enables software-based interactive I/O without physical hardware."
references: []
modDatetime: 2026-05-27 18:58:41.240525+09:00
---

PTY (Pseudo Terminal) refers to a pair of virtual devices that emulate terminal functionality via software, without requiring physical hardware terminal devices. It consists of two file interfaces: a Master and a Slave. In this architecture, data sent from the master process is delivered as input to the slave process, and output from the slave is returned to the master. This allows the operating system to communicate with processes as if they were connected to an actual physical terminal, facilitating interactive input and output.

### Practical Use Case
1. **Remote Connection Environments**: When connecting to a server via SSH (Secure Shell), the server allocates a PTY for each user session. This provides a shell environment where users can input commands and receive results in real-time.
2. **Terminal Emulators**: Modern GUI-based terminal software such as xterm, iTerm2, and the built-in terminal in VS Code utilize PTYs internally to communicate with the operating system kernel.
3. **AI Agent Automation**: When an AI agent executes code within a sandbox or modifies system configurations, it uses a PTY to mimic an interactive interface. This allows the agent to handle real-time error responses and execute complex, multi-step commands.

### Related Words
- **TTY (Teletype)**: A collective term for the physical teleprinters used in the early days of computing or the terminal devices of a system.
- **SSH (Secure Shell)**: A secure protocol for logging into remote computers or executing commands over a network; it allocates a PTY when a session is established.
- **Shell**: A command-line interpreter that relays user commands to the operating system kernel, typically interacting with the user through a PTY.