---
title: "什么是 TTFB？"
author: editornom
author_role: "资深技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-17 11:32:39.256277+09:00
slug: "what-is-ttfb"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "了解 Web 性能优化的核心指标 TTFB (Time to First Byte) 的定义与重要性，并介绍如何解决 Service Worker 延迟以及通过导航预加载（Navigation Preload）提升服务器响应速度的方法。"
references: []
modDatetime: 2026-05-17 11:42:39.256277+09:00
---

# 什么是 TTFB？

### 定义 (Dictionary Definition)
TTFB（Time to First Byte，首字节时间）是衡量 Web 浏览器向服务器发送 HTTP 请求后，收到响应数据的第一个字节所需时间的性能指标。该数值综合反映了网络延迟（Latency）、服务器的请求处理时间以及浏览器与服务器之间连接建立的效率。在 Web 性能优化中，它是识别服务器响应速度和网络瓶颈的核心衡量标准。

### 实际应用场景 (Practical Use Case)
在使用 Service Worker 的 Web 架构中，TTFB 是评估服务初始加载性能的重要基准。在浏览器唤醒处于休眠状态的 Service Worker 的过程中产生的“Service Worker 延迟（Service Worker Latency）”，会导致 TTFB 增加几十到几百毫秒（ms）。为了优化这一环节，工程师们会采用“导航预加载（Navigation Preload）”技术，在 Service Worker 启动的同时发起网络请求，从而缩短 TTFB 并提升整体用户体验。

### 相关术语 (Related Words)
- **Service Worker 延迟 (Service Worker Latency)**：指 Service Worker 启动和运行时的初始延迟，是导致 TTFB 增加的主要原因之一。
- **导航预加载 (Navigation Preload)**：一种用于绕过 Service Worker 启动延迟并优化 TTFB 的浏览器 API。
- **服务器响应时间 (Server Response Time)**：服务器处理请求并生成响应所需的时间，是 TTFB 的核心组成部分。