---
title: "AI DoS (人工智能拒绝服务攻击)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-04 17:44:25.150003+09:00
slug: understanding-ai-denial-of-service-attacks
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "AI DoS 是一种利用 AI 模型设计漏洞耗尽系统资源并中断服务的攻击方式。通过了解 Prompt Injection 导致的资源枯竭及 API 配额耗尽等典型案例，掌握 AI DoS 的定义与安全威胁。"
references: []
modDatetime: 2026-05-04 17:54:25.150003+09:00
---

# 什么是 AI DoS？

### 定义 (Dictionary Definition)
AI DoS（AI Denial of Service，人工智能拒绝服务攻击）是指攻击者利用人工智能模型或其底层基础设施的设计缺陷，恶意消耗系统资源并最终导致服务不可用的攻击手段。此类攻击通常利用了 LLM（大语言模型）无法有效区分输入数据与操作指令的“指令与数据分离失败（Command/Data separation failure）”缺陷。攻击者可以通过植入特定字符序列或构建复杂的 Prompt，诱导模型陷入无限循环或触发极其昂贵的推理计算，从而瞬间耗尽用户的 API 配额（Quota），使用户无法正常使用服务。

### 实际案例 (Practical Use Case)
近期有安全报告指出，在 AI 编程助手 Claude Code 环境中，如果模型读取到包含特定元数据（如 OpenClaw 相关字符串）的源代码，可能会将其误判为系统级指令，从而触发 Prompt Injection。在这种情况下，无论用户的原始意图是什么，AI 模型都会开始反复执行异常运算，在极短时间内耗尽 Claude Pro 订阅计划的所有配额并强制终止当前会话，形成典型的 AI DoS 攻击场景。

### 相关术语 (Related Words)
- Prompt Injection (提示词注入)
- 资源耗尽攻击 (Resource Exhaustion)
- 架构缺陷 (Architectural Flaw)