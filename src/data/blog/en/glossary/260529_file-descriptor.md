---
title: "File Descriptor"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 15:43:58.422341+09:00
slug: "file-descriptor"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Explore the definition and characteristics of file descriptors, the non-negative integers used to access I/O resources like files and sockets in Unix-like operating systems. Learn how they enable efficient system resource management through practical use cases such as I/O multiplexing."
references: []
modDatetime: 2026-05-29 15:53:58.422341+09:00
---

# What is a File Descriptor?

### Dictionary Definition
In Unix and Unix-like operating systems, a file descriptor is an abstract non-negative integer used by a process to access various input/output resources, such as files, sockets, and pipes. It is allocated by the Kernel when a process opens a resource and serves as an index pointing to a specific resource within that process's file descriptor table.

### Practical Use Case
In network server architecture, when a client connection is established, the operating system creates a file descriptor for that specific socket. During the I/O multiplexing process designed to solve the C10K problem, functions such as select() or poll() receive multiple file descriptors as arguments to monitor whether data has been received. By selecting and processing only the file descriptors where actual data has arrived, the system can manage its resources with high efficiency.

### Related Words
- Socket
- I/O Multiplexing
- Kernel