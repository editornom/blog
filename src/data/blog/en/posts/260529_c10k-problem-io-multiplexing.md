---
title: "The C10K Problem: The Birth of Modern Network Architecture and the Evolution of I/O Multiplexing"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 15:43:15.852478+09:00
slug: "c10k-problem-io-multiplexing"
featured: false
draft: false
ogImage: "../../../../../source/posts/C10K_Problem/c22c229f-0.webp"
description: "We analyze the root cause of the C10K problem—linear resource waste during I/O monitoring and the limitations of the traditional select/poll models. This article covers structural bottlenecks that prevented full utilization of hardware and the resulting need for high-performance server architectures."
references:
- https://medium.com/@m-ibrahim.research/demystifying-select-poll-kernel-internals-and-the-c10k-challenge-6f3f5b5cd632
- https://en.wiktionary.org/wiki/C10k_problem
- https://fr.wikipedia.org/wiki/C10k_problem
modDatetime: 2026-05-29 15:53:15.852478+09:00
faqs:
- q: "What exactly does the C10K problem mean?"
  a: "It is a challenge posed by engineer Dan Kegel in 1999, referring to the inability of a single server to efficiently handle 10,000 concurrent client connections. The primary cause was structural bottlenecks in the operating system and software design rather than hardware limits."
- q: "Why couldn't servers in 1999 handle 10,000 connections?"
  a: "They primarily used a model that created one process or thread per connection. As users increased, context-switching overhead spiked, and the stack memory allocated to each thread quickly exhausted physical RAM, causing the server to freeze."
- q: "Why is I/O Multiplexing technology important?"
  a: "It allows a single process to monitor thousands of connections simultaneously and only handle active ones where data has actually arrived. This prevents unnecessary resource waste and enables efficient management of large-scale concurrent connections with minimal resources."
- q: "What is the biggest drawback of the traditional select() model?"
  a: "The number of sockets it can monitor is usually limited to 1,024, and it uses an O(n) approach that performs an exhaustive search of the entire socket list every time it is called. Additionally, there is inefficiency in having to re-specify the monitoring targets to the kernel repeatedly."
- q: "How did poll() improve upon the limitations of select()?"
  a: "poll introduced an array structure, solving the critical 1,024-connection limit of select. Sockets could be registered almost indefinitely as long as memory allowed, but it still maintained the linear scanning method to check the status of all sockets."
- q: "Why are epoll and kqueue significantly faster than traditional methods?"
  a: "They use an event-driven approach where the kernel places only the sockets that have changed state into an event queue. This results in O(1) complexity, where performance is affected only by the number of actual events occurring, regardless of the total number of connections."
- q: "How does data copying between kernel and user space affect performance?"
  a: "select and poll must copy large amounts of socket information to the kernel and back every time they are called. With tens of thousands of connections, this data copying overhead puts a heavy load on the memory bus, slowing down the entire system's response speed."
- q: "What is the technical background behind Nginx's popularity over Apache?"
  a: "Apache used a model that allocated a process per request, limiting its ability to solve the C10K problem. Nginx adopted an event-driven architecture like epoll, allowing it to handle tens of thousands of concurrent connections with just a few processes and low memory usage."
- q: "Why is Nginx considered faster than Apache when concurrent users increase?"
  a: "Nginx uses an event-driven model that processes only the connections sending signals rather than checking every single one. Even with 10,000 users, it focuses resources only on active connections, using much less memory and achieving higher processing speeds."
- q: "Nowadays, people talk about 10 million connections instead of 10,000. What should developers study?"
  a: "To prepare for the C10M era, look into technologies that bypass or directly control the kernel's network stack. Understanding zero-copy techniques that reduce data copying overhead and the principles of high-performance asynchronous frameworks will be greatly beneficial in modern distributed system design."
---

<div class="bluf"><strong>[BLUF]</strong><p>The root cause of the C10K problem is <strong>linear resource waste (O(n) overhead)</strong> during the I/O monitoring process. Despite having sufficient hardware performance, traditional select() and poll() models were hindered because they performed exhaustive searches on all connections and triggered excessive data copying between the kernel and user space.</p></div>

Think back to the technical landscape of 1999. It was a strange time when the pace of hardware development seemed to overwhelm software's processing capabilities. The "C10K problem," raised by engineer Dan Kegel, was more than just a numerical goal for a single server to handle 10,000 connections; it was a landmark event that shifted the paradigm of modern high-performance system design.

In an era where 500MHz CPUs were becoming common, servers were screaming to a halt even though, theoretically, they could have allocated tens of thousands of calculation cycles to a single client. This signaled an era of "structural mismatch," where software architecture failed to fully unleash the potential of the hardware.

## The C10K Problem: The Disconnect Between Hardware and Software Amidst Internet Growth

### The 1999 Warning: Why a 500MHz CPU Couldn't Handle 10,000 Users

At the time, servers adhered to a method of creating and allocating a new process or thread every time a user connected. However, as the number of users grew, a reversal occurred where hardware resources were consumed by "management" itself rather than actual computation. The memory and CPU cycles required to maintain 10,000 connections far exceeded the physical thresholds the servers could handle.

This bottleneck wasn't something that could be solved simply by increasing CPU speed. Rather, the overhead generated by the operating system kernel scheduling and managing numerous processes was the main culprit. Ultimately, the C10K problem served as a loud alarm, demanding a fundamental review of software design rather than just hardware limits.

### Limitations of Memory and Context Switching in the Thread-per-connection Model

The structure of creating one thread per connection had the advantage of being intuitive to implement, but it revealed fatal weaknesses in scalability. The independent stack memory allocated each time a thread was created quickly exhausted the system's physical RAM. Servers running low on memory would begin virtual memory swapping, falling into a swamp of rapidly degrading performance.

An even bigger issue was Context Switching. The latency involved in the CPU saving and restoring states to switch between multiple threads increased exponentially in proportion to the number of connections. In essence, more energy was spent on "administrative procedures"—moving between threads—than on processing actual business logic.

![C10K Problem - A visual representation of data moving efficiently through a glowing glass prism.](../../../../../source/posts/C10K_Problem/c22c229f-0.webp)

## The Collapse of Traditional I/O Models: Why Servers Froze Despite Sufficient Hardware

While hardware architecture raced toward multi-core processors and high-speed buses, traditional I/O methods remained stuck in 1980s philosophy. Even with thousands of network sockets open, only a fraction were "active connections" actually sending or receiving data. Most connections were idle, yet the system wasted precious resources trying to manage them all equally.

To prevent this inefficient resource consumption, <a href="/en/glossary/io-multiplexing" class="glossary-tooltip" data-definition="A technology that allows a single process to monitor multiple I/O channels simultaneously and process only the channels that are ready.">I/O Multiplexing</a> emerged as an alternative. This approach was designed so that a single process could monitor numerous connections at once and react only when actual data arrived. However, the early technologies, select() and poll(), were not perfect solutions either.

## Structural Flaw Analysis of select() and poll(): When Monitoring Overwhelms Processing

### select(): The 1024 Wall and Inefficient Bitmask Reconstruction

Used since the early days of UNIX systems, select() managed the state of sockets to be monitored in the form of a Bitmask. However, this method had a fatal limit where the maximum number of connections was usually restricted to 1,024 by a constant called FD_SETSIZE. Even if you wanted to handle more connections, performance scaling was impossible due to this wall set at the OS level.

Furthermore, there was the hassle of having to re-specify the monitoring targets every time the function was called. The kernel had to perform an exhaustive search of the bitmask from beginning to end to check which sockets had changed. Even if only one out of 1,000 connected clients sent data, the kernel still had to scan all 1,000 bits, making it a highly inefficient structure.

### poll(): Infinite <a href="/en/glossary/file-descriptor" class="glossary-tooltip" data-definition="A unique identifier assigned by the operating system to access system resources like files or sockets, used to identify and manage each I/O channel.">File Descriptors</a>, but Still the Heavy O(n) Exhaustive Search

poll() was introduced with an array structure to solve the limitation on the number of connections found in select(). Now, sockets could be registered almost infinitely as long as memory allowed, but the fundamental problem of computational complexity remained. As the number of sockets increased, the time spent traversing the entire list to check their status increased proportionally, trapping the system in the O(n) cycle.

On a server with thousands of idle connections, poll() wasted time scanning the entire array at every moment. Even "quiet connections" that were not sending any data were included in the monitoring target, eating away at CPU cycles. Consequently, it was impossible to prevent the overall system response speed from slowing down non-linearly as the number of connections grew.

### Data Copying Between Kernel and User Space: The Mechanism Where Idle Connections Become Toxic

Another hidden obstacle in the I/O Multiplexing model was the constant data copying between the kernel and user space. Every time select() or poll() was called, information about all sockets to be monitored had to be passed to the kernel, and the results had to be copied back to user space. As the number of connected clients grew, this data copying process itself placed an enormous load on the memory bus.

When managing 10,000 sockets, the copying overhead of several hundred kilobytes occurring with each call was significant. This copying didn't stop even when no actual data processing was taking place. As idle connections increased, a strange situation arose where the server's energy was concentrated solely on the wasteful activity of "exchanging notifications."

### Performance and Structural Comparison by Technical Model

| Feature | select() | poll() | epoll() / kqueue() |
|:---:|:---:|:---:|:---:|
| Time Complexity | O(n) (Exhaustive Scan) | O(n) (Exhaustive Scan) | O(1) (Events only) |
| Max Connections | 1024 (Hard limit) | No limit (Memory dependent) | No limit (System resource dependent) |
| Data Copying | Copies all sockets every call | Copies all sockets every call | Only sends info on state changes |
| Performance Impact | Sharp drop as connections increase | Sharp drop as connections increase | Performance maintained regardless of count |

## The Paradigm Shift: From 'Status Monitoring' to 'Event Notification'

### The Evolution of I/O Multiplexing: The Background of epoll and kqueue

To break through these limitations, epoll (Linux) and kqueue (BSD) were introduced. They completely shattered the fixed idea of "performing an exhaustive search on all sockets every time." Instead, they adopted a method of pre-registering a list of sockets of interest within the kernel and passing only the sockets where state changes occurred to the user via a separate "event queue."

Now, a process no longer has to ask which of the tens of thousands of connections are ready. Instead, the system switched to an event-driven approach where the kernel informs the process, "Here are the ready sockets, take them." This provided remarkable efficiency, approximating O(1), where performance is proportional only to the number of actual active events, regardless of the total number of connections.

> "The C10K problem was not a hardware bottleneck, but a software design bottleneck caused by the failure to efficiently manage thousands of idle connections."

> "The shift from a status-polling method to an event-driven method, which notifies when an event occurs, is the core of modern high-performance servers."

### The Victory of Event-driven Architecture: Power Shift from Apache to Nginx

This technical advancement completely reshaped the web server market. Apache, the traditional leader, struggled to solve the C10K problem due to the limitations of its process-per-request model. In contrast, Nginx actively utilized event-driven models like epoll to easily handle tens of thousands of concurrent connections with just a few processes.

The emergence of Nginx was not merely the birth of new server software. It represented a victory for a fundamental philosophy regarding how servers should handle large-scale connections. This became a decisive catalyst for the emergence of asynchronous runtimes like Node.js and the establishment of the "Single-thread Event-loop" model as a standard in modern web development.

![C10K Problem - A futuristic network server schematic representing data flow through glowing spheres and lines.](../../../../../source/posts/C10K_Problem/b25477fe-1.webp)

## Beyond C10K to C10M: The Legacy Left for Modern Distributed Systems

### Kafkorama and WebSockets: New Scaling Strategies for the Real-time Data Era

Today, we are discussing the C10M era, which refers to 10 million connections rather than 10,000. This is because we must manage massive amounts of stateful connections through WebSockets in real-time streaming, online gaming, and large-scale chat services. Now, we have gone beyond efficient <a href="/en/glossary/file-descriptor" class="glossary-tooltip" data-definition="An integer-based identifier used in Unix-like operating systems to access files or sockets.">File Descriptor</a> management to using technologies that bypass the kernel's network stack altogether.

Distributed messaging platforms like the Kafka ecosystem and high-performance communication frameworks have deeply internalized the lessons learned from solving the C10K problem. Techniques like "Zero-copy," which react immediately only when data is generated and minimize unnecessary copying, can all be seen as great legacies originating from the concerns of 1999.

### The Evolutionary Link from Vertical to Horizontal Scaling

The solution to the C10K problem didn't stop at optimizing the performance of a single server. As one server became capable of handling tens of thousands of users, we were able to build larger systems with fewer nodes. This became a solid foundation for making horizontal scaling more efficient in cloud-native environments.

Modern architects now worry less about the threshold of a single server and more about how to organically connect numerous high-performance nodes. However, beneath all those designs, the fundamental question of "how to efficiently multiplex a single resource" still lives on.

### Empirical Indicators Related to C10K and High-Concurrency Systems

* **1999:** The C10K problem (10,000 Concurrent Connections) was formally raised by Dan Kegel.
* **Data Copying Overhead:** When managing 10,000 connections, memory traffic from copying the pollfd structure is approximately 120KB per call.
* **Nginx Performance:** Adopting an event-driven architecture reduced memory usage by more than 10 times compared to Apache.
* **C10M Milestone:** The Kafkorama benchmark achieved less than 3ms of latency for 1 million (1M) WebSocket clients on a single node.
* **Hardware-Software Performance Gap:** Servers based on 500MHz CPUs were theoretically capable of processing 50,000 cycles per client but failed due to software bottlenecks.

## Conclusion: Is the C10K Problem Still Relevant?

The C10K problem faced by previous generations of developers has been elegantly solved at the OS and runtime levels and remains part of our infrastructure today. However, technical advancement always brings new challenges. We now stand at a point where we must consider another form of the "aesthetics of connection" in edge computing and serverless architecture environments.

The spirit of the 1999 engineers who struggled while scanning bitmasks remains valid within today's microservices architecture. Efficient resource management and event-driven thinking are the unchanging essence of system optimization. I hope you take a moment to look back at your code today and see if your server's precious resources are being wasted somewhere.

## 🔗 Recommended Reading
- [SilverTorch: Meta's 23x Performance Leap or the Start of New 'Technical Debt'?](/en/posts/silvertorch-meta-23x-performance-technical-debt)
- [The Paradox of Zero Trust Implementation: Is Your Security Network a Fortress or a Shackle?](/en/posts/zero-trust-implementation-paradox)