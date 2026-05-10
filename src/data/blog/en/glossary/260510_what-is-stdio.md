---
title: "What is STDIO?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-10 17:03:53.759572+09:00
slug: "what-is-stdio"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Explore the core principles of Inter-Process Communication (IPC) through the concept of STDIO (Standard Input/Output) and practical use cases in MCP environments. Learn how to implement secure and efficient data exchange using standard system streams without the need for separate network ports."
references: []
modDatetime: 2026-05-10 17:13:53.759572+09:00
---

### What is STDIO?

#### Dictionary Definition
STDIO (Standard Input/Output) refers to the standard streams that serve as the default input and output channels for data exchange between a program and its external environment in a computer operating system. It generally consists of three channels—Standard Input (stdin), Standard Output (stdout), and Standard Error (stderr)—acting as an abstracted interface that allows programs to read and write data regardless of specific hardware or network configurations.

#### Practical Use Case
In the Model Context Protocol (MCP) specification, when client and server processes installed in a local environment communicate, they use the system's STDIO as the primary transport channel instead of opening separate network ports. This approach is utilized to reduce data transmission latency through direct input/output between processes and to enhance security in local environments by fundamentally blocking potential external access through the network layer.

#### Related Words
- **IPC (Inter-Process Communication)**: Refers to the mechanisms within an operating system that allow processes to exchange data; STDIO is one of the most fundamental communication methods among them.
- **JSON-RPC**: A lightweight remote procedure call protocol used to exchange structured commands and responses via STDIO streams.
- **Standard Stream**: A collective term for the standard model of data flow connecting a program to a system terminal or input/output devices.