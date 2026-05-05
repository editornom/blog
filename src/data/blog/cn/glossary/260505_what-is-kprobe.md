---
title: "什么是 kprobe？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-05 14:33:23.133915+09:00
slug: linux-kernel-kprobe-guide
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "kprobe 是一种轻量级机制，通过在 Linux 内核的特定位置动态设置断点，无需重启系统即可实时跟踪其行为并收集信息。它与 eBPF 结合，在系统调用监控、性能分析和安全审计等内核级观测任务中发挥着核心作用。"
references: []
modDatetime: 2026-05-05 14:43:23.133915+09:00
---

# 什么是 kprobe？

### 词典定义 (Dictionary Definition)
kprobe (Kernel Probe) 是一种轻量级机制，允许在 Linux 内核执行特定指令或函数的位置动态设置断点 (Breakpoint)，从而跟踪内核的行为并收集相关信息。它无需修改源代码，也不需要重新编译内核或重启系统，通过在运行中的系统内核内部安装探针，当执行到指定位置时，预定义的处理函数 (Handler) 就会被触发执行。

### 实际应用案例 (Practical Use Case)
kprobe 常与 eBPF (extended Berkeley Packet Filter) 结合使用，在“无侵入 (Zero-instrumentation)”环境下监控系统调用 (System Call)。例如，当特定进程创建网络套接字或向文件系统的特定区域执行写入操作时，可以将 kprobe 附加到处理这些操作的内核函数上。通过实时记录参数值和返回值，开发人员或系统管理员可以进行安全审计，或精准识别性能瓶颈所在。

### 相关词汇 (Related Words)
* **eBPF (Extended Berkeley Packet Filter):** 一种允许在不修改内核源码的情况下在内核级运行程序的技术，它将 kprobe 作为主要的跟踪手段之一。
* **uprobe (User Probe):** 一种用于跟踪用户空间 (User Space) 应用程序函数而非内核空间函数的机制。
* **Tracepoint:** 预先定义在内核源代码中的静态跟踪点。与 kprobe 相比，它的开销更小且更稳定，但灵活性较低（无法像 kprobe 那样动态设置）。
* **System Call:** 用户空间进程向内核请求特定服务的接口，是 kprobe 最主要的跟踪对象。