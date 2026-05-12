---
title: "What is SRE?"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-12 11:28:39.488100+09:00
slug: "what-is-sre"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Site Reliability Engineering (SRE) is a practice that applies software engineering principles to system operations to maximize service stability and availability. Explore the core concepts of quantitative management and automation using SLOs and Error Budgets for efficient IT infrastructure operations."
references: []
modDatetime: 2026-05-12 11:38:39.488100+09:00
---

# What is SRE?

## Dictionary Definition
Site Reliability Engineering (SRE) is a system operation methodology created by Google that applies software engineering principles to IT infrastructure and operations problems. It leverages automation and monitoring to ensure system reliability, availability, and efficiency. SRE is characterized by minimizing manual 'toil' (repetitive, manual tasks) and quantitatively managing system stability based on Service Level Objectives (SLOs).

## Practical Use Case
When implementing security technologies such as eBPF, SREs measure the load that security logic places on system availability and establish monitoring frameworks. If a drop in system call processing speed is detected after a security program deployment—risking the depletion of a pre-defined Error Budget—the SRE team may decide to halt the deployment or prioritize performance optimization to ensure system availability.

## Related Terms
* <b>DevOps</b>: A cultural philosophy that emphasizes collaboration between software development and operations. SRE is often viewed as a specific implementation model of DevOps through engineering techniques.
* <b>SLO (Service Level Objective)</b>: Specific target values for performance and availability that a service provider aims to achieve.
* <b>Error Budget</b>: The total amount of allowable system downtime or performance degradation while still meeting the SLO. It serves as a benchmark for deciding whether to release new features or focus on stability.