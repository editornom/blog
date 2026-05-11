---
title: "什么是JIT？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 15:30:57.403279+09:00
slug: "what-is-jit"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "JIT（即时）编译是一种在程序运行时将字节码翻译成机器码以优化运行时性能的技术，它结合了AOT和解释器方法的优点。在eBPF等技术中，它能将字节码即时转换为硬件原生指令，从而显著降低系统调用成本，并实现接近原生代码的处理速度。"
references: []
modDatetime: 2026-05-11 15:40:57.403279+09:00
---

# 什么是JIT？

- 词典定义 (Dictionary Definition)：JIT（Just-In-Time，即时）编译是一种在程序运行时，将字节码实时翻译成目标系统机器码的技术。它结合了AOT（Ahead-Of-Time，预先）编译方式的执行效率和解释器方式的灵活性，从而优化运行时性能。

- 实际应用案例 (Practical Use Case)：在eBPF（Extended Berkeley Packet Filter）技术中，JIT编译器能够将运行在内核内虚拟机中的字节码即时转换为硬件原生指令。这显著降低了系统调用（System Call）时用户空间和内核空间之间上下文切换的开销，并提供了接近原生代码的执行速度。

- 相关词汇 (Related Words)：AOT（Ahead-Of-Time），字节码（Bytecode），eBPF Verifier