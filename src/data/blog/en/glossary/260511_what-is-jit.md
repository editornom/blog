---
title: "What is JIT?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 15:30:57.403279+09:00
slug: "what-is-jit"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "JIT (Just-In-Time) compilation optimizes runtime performance by translating bytecode into machine code at execution time, combining the advantages of AOT and interpreters. In technologies like eBPF, it delivers native-level speeds by converting code into hardware instructions to minimize system call overhead."
references: []
modDatetime: 2026-05-11 15:40:57.403279+09:00
---

# What is JIT?

- **Dictionary Definition**: JIT (Just-In-Time) compilation is a technology that translates bytecode into the target system's machine code in real-time at the moment of program execution. It optimizes runtime performance by combining the execution efficiency of AOT (Ahead-Of-Time) compilation—which translates source code into machine code beforehand—with the flexibility of the interpreter method.

- **Practical Use Case**: In eBPF (Extended Berkeley Packet Filter) technology, a JIT compiler immediately converts bytecode running within the kernel's virtual machine into hardware-native instructions. This drastically reduces the context-switching overhead between user space and kernel space during system calls, delivering execution speeds that approach native performance.

- **Related Words**: AOT (Ahead-Of-Time), Bytecode, eBPF Verifier