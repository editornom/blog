---
title: "什么是 JSON-RPC 2.0？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-25 09:10:00+09:00
slug: json-rpc-2-0-standard-overview
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "JSON-RPC 2.0 是一种基于 JSON 的轻量级远程过程调用 (RPC) 协议，支持无状态的高效数据交换和批处理。本文介绍了 JSON-RPC 2.0 的定义及其实践案例，该协议目前被广泛应用于 Anthropic 的 MCP 等 AI 模型与数据间的实时交互。"
references: []
modDatetime: 2026-04-28 15:14:18.960187+09:00
---

# 什么是 JSON-RPC 2.0？

### 词典定义 (Dictionary Definition)
JSON-RPC 2.0 是一种基于 JSON (JavaScript Object Notation) 数据格式的轻量级远程过程调用 (Remote Procedure Call, RPC) 协议。作为一种专为客户端与服务器间数据交换设计的无状态 (Stateless) 通信规范，它支持请求 (Request)、响应 (Response)、通知 (Notification) 以及批处理 (Batch) 操作。由于其结构独立于传输层，因此可以灵活应用于 HTTP、WebSockets、TCP 等多种网络环境。

### 实际应用案例 (Practical Use Case)
Anthropic 推出的 MCP (Model Context Protocol) 采用了 JSON-RPC 2.0 作为标准通信协议，旨在统一 AI 模型与外部数据源之间碎片化的接口。客户端通过发送 JSON 格式的消息请求服务器执行特定工具 (Tools) 或查询资源 (Resources)，服务器则返回标准化的 JSON 数据响应，从而实现了 AI Agent 与企业级数据库之间的实时交互。

### 相关词汇 (Related Words)
- RPC (Remote Procedure Call)
- JSON (JavaScript Object Notation)
- MCP (Model Context Protocol)