---
title: "混淆代理 (Confused Deputy)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 18:48:35.245929+09:00
slug: "confused-deputy"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "混淆代理（Confused Deputy）是指拥有权限的代理人在未对低权限请求进行验证的情况下执行操作，从而导致的安全性漏洞。它是权限滥用和数据泄露的主要原因。本文将解释 AI Agent 环境中可能出现的间接提示词注入等相关风险及安全对策。"
references: []
modDatetime: 2026-05-29 18:58:35.245929+09:00
---

# 什么是混淆代理 (Confused Deputy)？

### 词典定义 (Dictionary Definition)
混淆代理是指拥有权限的代理人（Deputy）在没有进行适当验证的情况下，利用其被授予的特权执行权限较低实体的请求，从而引发的安全性漏洞。当系统基于代理人自身的权限而非原始请求者的权限来批准操作时，就会发生这种情况。这是导致权限滥用和数据泄露的主要原因。

### 实务应用案例 (Practical Use Case)
例如，基于 Model Context Protocol (MCP) 的 AI Agent 根据用户的指令发送电子邮件或修改文件时，如果未确认该指令是否违反安全策略，而是直接以 Agent 拥有的系统权限执行，即属于此类情况。

### 相关术语 (Related Words)
权限提升 (Privilege Escalation)、间接提示词注入 (Indirect Prompt Injection)、访问控制 (Access Control)