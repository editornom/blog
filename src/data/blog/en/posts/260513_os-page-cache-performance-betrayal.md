---
title: "The Betrayal of OS Page Cache: From Efficient Automation to a Performance Monopoly Boomerang"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 11:35:54.585211+09:00
slug: "os-page-cache-performance-betrayal"
featured: false
draft: false
ogImage: "../../../../../source/posts/Page-Cache/05581c16-0.webp"
description: "An in-depth analysis of resource monopoly and system instability caused by automated OS page cache in high-performance computing and container environments. Explores the shift toward Direct I/O and manual memory control architectures using NASA and PostgreSQL 18 as case studies."
references:
- https://www.nas.nasa.gov/hecc/support/kb/checking-and-managing-page-cache-usage_505.html
- https://medium.com/@amanpatel.workid/os-page-cache-what-it-is-and-what-it-is-not-51178d52913b
- https://developer.adobe.com/commerce/frontend-core/guide/caching
modDatetime: 2026-05-13 11:45:54.585211+09:00
faqs:
- q: "What is OS page cache and what is its role?"
  a: "It is an area where the Linux kernel temporarily stores file data in surplus physical memory to enhance I/O performance. It is an automated optimization technology that reduces disk access by keeping recently read data in memory."
- q: "Why did page cache become a problem in NASA's case?"
  a: "A specific process performing massive I/O monopolized the node's available memory as page cache. This caused memory starvation, leaving other processes on the same node without enough memory, which degraded overall system performance."
- q: "What is the relationship between OOMKill in Kubernetes container environments and page cache?"
  a: "The kernel considers page cache as 'used' memory. If cache data exceeds the memory limit set for a container, the system may trigger an OOMKill to forcibly terminate the process, even if the application's actual heap memory usage is low."
- q: "How does cache monopoly affect performance in a NUMA architecture?"
  a: "If cache occupies one side of physically separated memory nodes, other processes are forced to access memory on remote sockets, which is significantly slower. This asymmetric resource occupancy causes data transfer delays and drastically reduces computational efficiency."
- q: "What is the core of the Direct I/O technology introduced in PostgreSQL 18?"
  a: "It is a method where the application communicates directly with the disk, bypassing the operating system's automated page cache layer. The goal is to ensure performance determinism by allowing the database engine to control I/O directly instead of relying on opaque kernel cache policies."
- q: "Specifically, what role does the NASA-introduced pcachem tool play?"
  a: "It is a tool that forcibly sets a ceiling on the page cache automatically allocated by the OS. It ensures system stability and prevents resource monopoly by imposing physical limits so that a specific process cannot cannibalize all available memory."
- q: "Which system calls can developers use to resolve memory management debt?"
  a: "Developers can use posix_fadvise to explicitly inform the kernel that a specific cache is no longer needed after an I/O operation. Additionally, mbind.x can be used to physically bind a process to specific CPU cores and memory nodes to minimize interference."
- q: "What are the key Linux kernel parameters that affect page cache policy?"
  a: "vm.dirty_background_ratio determines when to start background asynchronous writes, and vm.dirty_ratio determines when to block process writes and commit data to disk. These parameters dictate the system-wide cache accumulation and stability."
- q: "My app memory seems fine, but OOM errors keep occurring in Kubernetes. Is this related to page cache?"
  a: "Yes, that is correct. Beyond the memory used by the application, page cache generated during file read/write operations counts toward the container's memory limit. Reaching this limit triggers an OOMKill, a common occurrence in environments with heavy logging or file handling."
- q: "Is it always better to disable OS caching and manage it manually for database performance?"
  a: "In environments where high-performance transactions are critical, direct control methods like Direct I/O are advantageous for performance predictability. However, since this increases implementation complexity and management overhead, the choice should depend on the system scale and I/O characteristics."
---

**[BLUF]** While the operating system's automated page cache is efficient, it can cause resource monopoly and unpredictable OOMKills in high-performance computing (HPC) and container environments. To address this, organizations like NASA and technologies like PostgreSQL 18 are shifting toward manual control architectures, such as `pcachem` and Direct I/O, to ensure system stability.

The operating system design principle that "unused RAM is wasted RAM" has been a golden rule of system optimization for decades. However, as we enter the era of high-performance parallel computing and cloud-native environments with isolated resources, this well-intentioned automation is turning into unexpected "operational debt." It is time to look closely at the internal paradox of how the [Page Cache](/en/glossary/page-cache), managed by the Linux kernel to accelerate file I/O, creates bottlenecks in modern systems.

![Page-Cache - A computer core system overloaded and surrounded by a massive amount of data fragments.](../../../../../source/posts/Page-Cache/05581c16-0.webp)

## 1. Bottlenecks Caused by System Goodwill: NASA's MPI Memory Starvation

### 1.1 The Tragedy of the Commons: How Rank 0 I/O Paralyzes an Entire Node

A case observed in NASA's High-End Computing Capability (HECC) environment serves as a perfect example of how automated optimization can become toxic. When an MPI (Message Passing Interface) based application runs, the "Rank 0" process responsible for data I/O performs large-scale operations. To assist this, the kernel begins allocating all available physical memory as page cache. The problem is that this process indiscriminately encroaches upon the memory areas intended for other Rank processes on the same node, leading to a "memory starvation" phenomenon that paralyzes the entire system.

### 1.2 Performance Plunge Due to Socket-Level Memory Partitioning and Remote Access

This issue is particularly fatal in NUMA (Non-Uniform Memory Access) architectures, such as NASA's Electra Broadwell nodes. With 128GB of RAM per node physically partitioned into 64GB per socket, if Rank 0 monopolizes the cache on one socket, other processes are forced to access memory on the remote socket, where data transfer speeds are significantly slower. This asymmetric resource occupancy ultimately leads to a sharp decline in computational efficiency for the entire simulation and causes unpredictable performance degradation.

![Page-Cache - A high-performance computer server where a specific resource is monopolized, glowing brightly while blocking the flow of data.](../../../../../source/posts/Page-Cache/4df40d2d-1.webp)

## 2. The Cloud-Native Paradox: K8s OOMKill and PostgreSQL's Declaration of "De-Kernelization"

### 2.1 "Free RAM is Not Free": Why Page Cache is a Time Bomb in Container Environments

A common mystery for operators in Kubernetes (K8s) environments is the occurrence of OOMKills even when the application's actual heap memory usage is low. The Linux kernel loads file I/O data into the page cache and treats it as "used memory." When this cache data exceeds the memory limit set in the `cgroup`, the system forcibly terminates the process. The moment the accumulation of "dirty pages"—which the kernel delays for asynchronous writes—reaches the limit, the cache intended for efficiency transforms into a time bomb that destroys system stability.

### 2.2 PostgreSQL 18 and Direct I/O: Why Databases are Refusing the OS Cache's "Favor"

A prime example of a revolt against these opaque kernel cache policies is the evolution of PostgreSQL 18. Database engines that traditionally relied on the operating system's caching capabilities are now bypassing the kernel by opting for [Direct I/O](/en/glossary/direct-io). Instead of the "sweetness" of system automation, this "de-kernelization" strategy—where the application controls I/O directly to ensure performance determinism—is becoming a core trend in modern high-performance system design.

![Page-Cache - A crystal representing the page cache expanding and putting pressure on a container.](../../../../../source/posts/Page-Cache/847624dc-2.webp)

## 3. Response Strategies: The Era of Sophisticated Manual Control Beyond Automation

### 3.1 From pcachem to posix_fadvise: Memory Management Debt Shifted to Developers

As autonomous system management hits its limits, NASA adopted a manual control approach by introducing a tool called `pcachem` to forcibly set a ceiling on the page cache. Similarly, modern senior developers are now required to have the design capability to use system calls like `posix_fadvise(POSIX_FADV_DONTNEED)` to explicitly clear the cache immediately after specific I/O operations. This suggests that the responsibility for fine-tuned performance tuning, which automation cannot solve, has fallen back onto human developers.

### 3.2 Securing Performance Predictability via Process Binding with mbind.x

Beyond simply being allocated memory, strategies that use sophisticated tools like `mbind.x` to bind processes to specific CPU cores and memory nodes are now highly recommended. By explicitly allocating resources from the physical layer up, minimizing interference between adjacent processes and ensuring extreme predictability has become a survival strategy in high-performance computing.

| Category | OS Auto Page Cache (Standard) | NASA pcachem Control | PostgreSQL 18 Direct I/O |
| :--- | :--- | :--- | :--- |
| I/O Management Entity | Kernel | User-defined tool (pcachem) | DB Engine (Userspace) |
| Memory Availability | High uncertainty (Monopoly risk) | Ceiling set (Limit secured) | Bypasses kernel cache (Predictable) |
| Primary Environment | General Desktop/Server | NASA MPI Simulations | High-performance Transaction DB |
| Key Trade-offs | Ease of use vs Resource contention | Manual overhead vs Node protection | Complex architecture vs I/O determinism |

## Conclusion: A Future for HPC Where System Autonomy Cannot Be Trusted

> "In modern operating systems, 'surplus RAM' is no longer a spare asset, but an operational debt that can paralyze the entire system through resource monopoly."
> "The versatility provided by automated kernel optimization is replaced by the cost of 'uncertainty' in ultra-high-performance environments."

We are living in an era where we can no longer blindly trust the automated favors of the system. NASA's MPI optimization cases and the architectural changes in PostgreSQL serve as warnings that general-purpose automation can actually become toxic in specialized, high-performance environments. Here are the technical facts we must remember:

*   **NASA Electra Hardware Specs**: Each Broadwell node has 128GB of RAM, physically split into 64GB per socket, which causes NUMA issues.
*   **Page Cache Identification**: Can be checked via the `Cached` entry in `/proc/meminfo`; in the NASA case, cache monopoly of over 60GB was observed on a single node.
*   **Linux Kernel Parameter Standards**: `vm.dirty_background_ratio` (start of async writes) and `vm.dirty_ratio` (blocking process writes) determine system-wide cache policy.
*   **Technical Authority Indicators**: Following the "Bypass Kernel" trend, PostgreSQL 18 introduced an asynchronous I/O subsystem to resolve the performance debt caused by the OS abstraction layer.

Developers and engineers must now look beyond the system's automated abstraction layers. Sophisticated manual control and resource isolation strategies will be the only keys to overcoming the paradox of automation and building truly high-performance systems.
