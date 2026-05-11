---
title: "Rowhammer"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 11:23:04.486265+09:00
slug: "rowhammer"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Rowhammer is a hardware vulnerability where repeatedly activating specific DRAM rows induces bit-flips in adjacent rows, leading to severe security threats such as privilege escalation and data tampering. This article analyzes key threats and defense strategies, covering attacks on DDR5 and GPUs as well as practical mitigation technologies like TRR and PRAC."
references: []
modDatetime: 2026-05-09 11:33:04.486265+09:00
---# What is Rowhammer?

### Dictionary Definition
Rowhammer is a hardware security vulnerability where a specific memory row in DRAM (Dynamic Random Access Memory) is repeatedly activated at high speeds to induce charge interference in adjacent rows, causing stored logical data bits to invert (Bit-flip). This exploits physical interference between semiconductor components resulting from miniaturization processes. It can be used to bypass software-level access controls, manipulate memory data, or seize system privileges.

### Practical Use Case
1. **DDR5 Vulnerability Attacks**: Cases like the 'Phoenix' attack have been identified, which bypass the sampling logic of TRR (Target Row Refresh) technology implemented by manufacturers to trigger bit-flips even in the latest memory modules.
2. **GPU Security Breaches**: The 'GPUBreach' attack exploits the architectural characteristics of GDDR6 memory to perform privilege escalation, potentially gaining root access in high-performance computing environments.
3. **Practical Mitigation Strategies**: Defense strategies include shortening the refresh interval (tREFI) to recharge memory cells before charge leakage occurs, or adopting PRAC (Per-Row Activation Counting) technology, which prevents attacks by directly counting row activation frequencies within the DRAM.

### Related Words
1. **Bit-flip**: A phenomenon where logical data values in memory are inverted from 0 to 1 or 1 to 0 due to physical interference.
2. **TRR (Target Row Refresh)**: A hardware-based defense technology that preemptively refreshes adjacent rows when excessive activation of a specific row is detected.
3. **PRAC (Per-Row Activation Counting)**: A next-generation security standard technique that monitors the activation count of each DRAM row in real-time to prevent reaching the Rowhammer threshold.
