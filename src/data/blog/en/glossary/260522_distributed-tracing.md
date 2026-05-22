---
title: "Distributed Tracing"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-22 11:44:59.981016+09:00
slug: "distributed-tracing"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Distributed tracing is a monitoring technique used to gain observability by tracking the entire path of a request in MSA and serverless environments, allowing for the visualization of service relationships and bottleneck identification."
references: []
modDatetime: 2026-05-22 11:54:59.981016+09:00
---

# What is Distributed Tracing?

### Dictionary Definition
Distributed tracing is a monitoring technique used to track and record the entire path a single request takes through distributed system architectures, such as Microservices Architecture (MSA) or serverless environments. By visualizing the call relationships and processing times between individual services, it ensures system-wide observability and is used to accurately pinpoint exactly where performance bottlenecks or errors occur.

### Practical Use Case
In a complex, interconnected serverless microservices environment, if the response speed of a specific API becomes slower than usual, distributed tracing tools are utilized to check in real-time which function stage or database call is causing the latency, enabling immediate troubleshooting and action.

### Related Terms
* Observability
* Microservices Architecture (MSA)
* Vendor Lock-in