---
title: "JSON-RPC 2.0: The Standard Specification for Remote Procedure Calls"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-25 09:10:00+09:00
slug: understanding-json-rpc-2-0-protocol-standard
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "JSON-RPC 2.0 is a lightweight JSON-based Remote Procedure Call (RPC) protocol supporting stateless data exchange and batch processing. This post introduces the definition and practical applications of JSON-RPC 2.0, a standard for real-time interaction between AI models and data, such as Anthropic's MCP."
references: []
modDatetime: 2026-04-28 15:14:18.960187+09:00
---

# What is JSON-RPC 2.0?

### Dictionary Definition
JSON-RPC 2.0 is a lightweight Remote Procedure Call (RPC) protocol encoded in JSON (JavaScript Object Notation). It is a stateless communication protocol designed for data exchange between a client and a server, supporting requests, responses, notifications, and batch processing. Because it is transport-independent, the protocol can be utilized across various network environments, including HTTP, WebSockets, and TCP.

### Practical Use Case
The Model Context Protocol (MCP), introduced by Anthropic, utilizes JSON-RPC 2.0 as its standard communication protocol to unify fragmented interfaces between AI models and external data sources. Clients request the execution of specific tools or query resources from the server using JSON-formatted messages. The server then responds with standardized JSON data, enabling seamless real-time interaction between AI agents and enterprise databases.

### Related Words
- RPC (Remote Procedure Call)
- JSON (JavaScript Object Notation)
- MCP (Model Context Protocol)