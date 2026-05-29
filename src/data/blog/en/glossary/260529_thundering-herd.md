---
title: "What is Thundering Herd?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 11:39:40.174633+09:00
slug: "thundering-herd"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Thundering Herd refers to a performance degradation in distributed systems where multiple processes simultaneously wake up to compete for a single resource, causing excessive CPU waste and context switching."
references: []
modDatetime: 2026-05-29 11:49:40.174633+09:00
---

# What is Thundering Herd?

### Dictionary Definition
The "Thundering Herd" problem is a phenomenon in computer science and distributed systems where a specific event triggers a large number of waiting processes or threads to wake up simultaneously to compete for a single resource. Although all requests vie for access, typically only one or very few processes succeed while the rest are forced back into a waiting state. The defining characteristic of this issue is the excessive context switching and CPU resource waste generated during this process, which significantly degrades overall system availability.

### Practical Use Cases
1. **Cache Stampede**: This occurs most commonly when the cache for a high-traffic data item expires. Numerous clients simultaneously attempt to fetch the data from the Origin DB, leading to a surge in requests that can paralyze the database server.
2. **Hedged Requests Side Effects**: This refers to a "self-inflicted DoS" scenario that can occur when hedged requests—a technique used to reduce latency by sending duplicate requests—are implemented without proper safeguards. If a specific backend node experiences latency, the resulting traffic spike can push the system into an irrecoverable state.
3. **Mutex Contention**: This occurs at the kernel level when multiple threads waiting for a shared resource lock are all awakened simultaneously once the lock is released, creating a scheduling bottleneck as they all attempt to claim the resource at once.

### Related Terms
- Request Coalescing
- Cache Stampede
- Exponential Backoff