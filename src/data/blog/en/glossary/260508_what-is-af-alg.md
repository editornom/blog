---
title: "What is AF_ALG?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 11:30:06.736176+09:00
slug: "what-is-af-alg"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "AF_ALG is a Linux kernel interface that allows user-space applications to access cryptographic algorithms and hardware acceleration through the standard socket API. This overview covers its technical implementation, practical usage with system calls like splice(), and its relevance to security vulnerabilities such as CVE-2026-31431."
references: []
modDatetime: 2026-05-08 11:40:06.736176+09:00
---## What is AF_ALG?

### Technical Definition
AF_ALG is a user-space interface provided by the Linux kernel to access its internal cryptographic subsystem. Standing for 'Address Family - Algorithm,' it is a communication channel designed to allow user-space applications to directly invoke and utilize cryptographic algorithms (such as AES, SHA, HMAC, etc.) implemented within the kernel via the standard Socket API. This interface enables efficient cryptographic operations by leveraging kernel-level resources, including hardware accelerators.

### Practical Use Cases
- <b>Invoking Kernel Cryptographic Engines</b>: When a user-space program needs to process data using the kernel's cryptographic modules, it creates a socket and connects to a specific algorithm through the bind() and accept() functions.
- <b>Interaction with System Calls</b>: AF_ALG is often used in conjunction with the splice() system call to optimize data transfer by minimizing copying overhead or to process encrypted data efficiently. Recently, it has been a focal point for security research regarding privilege escalation attacks—such as the CVE-2026-31431 (Copy Fail) vulnerability—which exploit design flaws in how AF_ALG and splice() interact.

### Related Terms
- CVE-2026-31431 (Copy Fail)
- splice() System Call
- Linux Kernel Crypto API
- Page Cache Corruption
