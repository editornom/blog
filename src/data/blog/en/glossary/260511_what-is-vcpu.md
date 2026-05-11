---
title: "What is vCPU?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 11:36:06.856378+09:00
slug: "what-is-vcpu"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Discover the definition of vCPU (Virtual Central Processing Unit), how physical CPU resources are allocated to virtual machines, and practical use cases in cloud environments. Learn how hypervisors efficiently manage processing power to optimize instance performance."
references: []
modDatetime: 2026-05-11 11:46:06.856378+09:00
---

# What is vCPU?

## Definition
A vCPU (Virtual Central Processing Unit) represents a logical unit of computing power assigned to a virtual machine (VM) in a virtualized environment. It is created by abstracting physical processor (pCPU) resources through a Hypervisor. Generally, a vCPU corresponds to a physical core or a logical thread of the underlying hardware, especially when Hyper-threading technology is utilized.

## Practical Use Case
In Cloud computing, vCPUs serve as a primary metric for determining the performance of an Instance. For example, when deploying a MySQL database on a Cloud platform (such as AWS RDS), you can scale or limit computational capacity by selecting the appropriate number of vCPUs to match the complexity and throughput of your workload.

## Related Terms
Hypervisor, Physical CPU (pCPU), Instance