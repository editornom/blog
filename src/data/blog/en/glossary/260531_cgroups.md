---
title: "cgroups"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-31 15:48:37.300383+09:00
slug: "cgroups"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "cgroups (control groups) is a Linux kernel feature that limits and isolates system resource usage such as CPU and memory for groups of processes. This guide explores the definition and practical applications of cgroups in Docker and Kubernetes environments to prevent resource exhaustion and ensure system stability."
references: []
modDatetime: 2026-05-31 15:58:37.300383+09:00
---

# What is cgroups?

### Dictionary Definition
cgroups (control groups) is a Linux kernel feature that allows for the limitation, isolation, and monitoring of system resource usage—such as CPU, memory, network bandwidth, and disk I/O—for specific groups of processes. Its primary objective is to ensure system stability by enabling administrators to control the resource consumption of particular process sets.

### Practical Use Case
In Kubernetes or Docker environments, cgroups are used to set memory limits on specific containers. This prevents a container with a memory leak from exhausting the resources of the entire host node, serving as a critical mechanism for 'Out Of Memory (OOM) Killer' management and overall cluster reliability.

### Related Words
* **Namespaces**: A technology that isolates system resources per process to limit their visibility of one another.
* **Container Virtualization**: A technology that runs applications in isolated environments while sharing the host operating system's kernel.
* **Linux Kernel**: The core part of the Linux operating system that manages hardware resources and holds process control authority.