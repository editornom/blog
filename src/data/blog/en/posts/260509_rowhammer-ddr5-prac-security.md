---
title: "Evolving Rowhammer: The Critical Limit of Hardware Security Where Even DDR5 and PRAC Are Breached"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 11:22:18.616670+09:00
slug: "rowhammer-ddr5-prac-security"
featured: false
draft: false
ogImage: "../../../../../source/posts/Rowhammer/647f00a3-0.webp"
description: "Optimism regarding hardware security has hit a wall as DDR5's Rowhammer defenses are neutralized by the Phoenix attack. Practical response strategies, such as shortening the refresh interval (tREFI), are now urgent."
references:
- https://www.microsoft.com/en-us/research/video/six-years-of-rowhammer-breakthroughs-and-future-directions/
- https://www.securityweek.com/gpubreach-root-shell-access-achieved-via-gpu-rowhammer-attack/
- https://comsec.ethz.ch/phoenix
modDatetime: 2026-05-09 11:32:18.616670+09:00
faqs:
- q: "What exactly is the Rowhammer security threat?"
  a: "Rowhammer is a hardware security vulnerability where electromagnetic interference, caused by repeatedly activating a specific row in a memory chip, physically alters the data in adjacent cells."
- q: "What are the primary defense mechanisms introduced in DDR5 memory?"
  a: "Manufacturers integrated Target Row Refresh (TRR) technology directly into the memory to detect excessive activation of specific rows and protect surrounding data."
- q: "What are the characteristics of the recently discovered Phoenix attack?"
  a: "The Phoenix attack precisely exploits flaws in the sampling-based defense logic used by DDR5's TRR, neutralizing existing protections and inducing bit-flips."
- q: "Why is the GPUBreach attack dangerous?"
  a: "It targets GDDR6 memory in GPUs rather than the system's main memory, potentially allowing attackers to gain root-level access to the system."
- q: "What is the PRAC technology proposed by Microsoft?"
  a: "PRAC stands for Per-Row Activation Counting. It is a technology that prevents Rowhammer attacks by directly counting the activation frequency of every row within the DRAM."
- q: "What security benefits come from shortening the refresh interval (tREFI) in DDR5?"
  a: "Shortening the refresh interval by more than threefold reduces the time window for an attacker to cause a bit-flip, thereby strengthening data integrity and system stability."
- q: "Is sacrificing performance for hardware security a viable practical response?"
  a: "While it results in a performance loss of approximately 8.4%, it is currently the most reliable and immediate countermeasure against fatal threats like Phoenix or GPUBreach."
- q: "Why is the standardization and field application of PRAC technology being delayed?"
  a: "Delays are caused by friction in the JEDEC standardization process and differing implementation methods among manufacturers, making it difficult to ensure interoperability between different hardware."
- q: "How much will server performance decrease if the memory refresh interval is reduced?"
  a: "If the memory refresh interval is set to be about three times shorter than usual for security reasons, overall system performance may drop by approximately 8.4%."
- q: "Is DDR5 memory truly safe from Rowhammer attacks?"
  a: "While it was previously believed to be safe, the emergence of the Phoenix attack and GPUBreach techniques means that DDR5 and GPU memory can no longer be considered secure."
---<div class="bluf"><strong>[BLUF]</strong><p>Optimism that DDR5 would be safe from <a href="/en/glossary/rowhammer" class="glossary-tooltip" data-definition="A hardware security vulnerability where electromagnetic interference, caused by repeatedly activating a specific row in a memory chip, physically alters data in adjacent cells.">Rowhammer</a> is no longer valid. The Phoenix attack and GPUBreach have neutralized hardware-level defense mechanisms, and alternatives like PRAC are failing to fully block real-world threats due to a lack of standardization. Immediate practical responses, such as shortening the refresh interval (tREFI), are urgent even if they come at the cost of performance.</p></div>

## 1. Memory Scaling and the Return of Rowhammer

 For some time, the hardware security industry believed that the arrival of DDR5 would signal the end of the Rowhammer threat. This expectation was fueled by the Target Row Refresh (TRR) technology integrated into memory modules, which was supposed to form an impenetrable fortress of defense.

 However, a series of recent studies have vividly demonstrated how dangerously optimistic that belief was. We are now at a point where we must move beyond blind trust in the "inherent safety of hardware" and confront increasingly sophisticated attack vectors.

![Rowhammer - A close-up of a semiconductor wafer with neon lights glowing at the point where a data error has occurred.](../../../../../source/posts/Rowhammer/647f00a3-0.webp)

### Core Analysis from a Technical Perspective

 One of the core threats that shook the security ecosystem in 2025 was the emergence of the Phoenix attack. This technique induces bit-flips by precisely exploiting loopholes in the sampling-based defense logic adopted by current TRR implementations.

 In particular, comprehensive testing conducted on 15 types of SK Hynix DDR5 modules revealed that every single model was vulnerable to the Phoenix attack. This symbolically demonstrates how easily "security mitigations" hidden by manufacturers as black boxes can collapse.

> "A manufacturer's closed defense strategy only increases security opacity and can never be a fundamental solution. We must now move the hardware security model from the realm of 'trust' to the realm of 'verification.'"

## 2. Collapse of DDR5 TRR Hardware Defense

 The scope of these attacks is not limited to main system memory. "GPUBreach," published by researchers at the University of Toronto, proved that GDDR6 memory in GPUs is also not immune to Rowhammer attacks.

 Contamination of GPU memory goes beyond simple data tampering; it provides a fatal path for seizing root privileges of a system. This poses an unprecedented threat to Cloud service providers operating High-Performance Computing (HPC) and AI infrastructure.

![Rowhammer - An abstract representation of information disparity, with light pouring through broken crystal shards against a dark background.](../../../../../source/posts/Rowhammer/3db7938d-1.webp)

## 3. Practical Defensive Strategy and Effectiveness of PRAC

 To address these security blind spots, Microsoft proposed an ambitious technology called PRAC (Per-Row Activation Counting). Based on Project STEMA (Panopticon) technology, this method seeks to block attacks proactively by directly counting the activation frequency of each row within the DRAM.

 However, PRAC is also facing limitations in field application due to friction in the standardization process. The vacuum in JEDEC standards and differences in implementation among manufacturers are providing attackers with yet another pretext for bypass routes.

| Attack Technique | Key Features and Target | Security Blind Spot |
| :--- | :--- | :--- |
| **Phoenix** | Bypasses all tested SK Hynix DDR5 models | Exploits blind spots in TRR sampling logic |
| **GPUBreach** | Gains root access via NVIDIA GDDR6 | Lack of defense in GPU memory architecture |
| **PRAC** | In-DRAM counting technology proposed by MS | Lack of interoperability due to incomplete standardization |

## 4. Future Silicon-Level Memory Security Architecture

 We must fundamentally change our perspective on hardware security. The latest vulnerabilities, epitomized by the CVE-2025-6202 identifier, warn that software patches alone can no longer provide a complete solution.

 From a practical standpoint, the most reliable countermeasure is to shorten the memory refresh interval (tREFI) to more than three times its original frequency, despite the performance trade-off. While this will result in a performance loss of approximately 8.4%, it is an unavoidable choice to ensure data integrity and system stability.

![Rowhammer - An abstract representation of cyber security resilience, with golden data streams pushing through a digital security mesh.](../../../../../source/posts/Rowhammer/26e3b4b2-2.webp)

 Furthermore, CTOs and security architects must establish a hardware verification system based on "Zero Trust." Rather than relying on manufacturer marketing, processes are needed to constantly check for vulnerabilities in their own hardware through independent security audits.

 Close cooperation with the global security ecosystem, such as the responsible disclosure process of the Swiss National Cyber Security Centre (NCSC), is also essential. Only by resolving information asymmetry and sharing threat intelligence in real-time can we transcend the critical limits of hardware security.

 Hardware security is not a static wall; it is a dynamic battlefield where attackers and defenders constantly engage in a game of wits. Taking the limitations shown by DDR5 and PRAC as a lesson, we must design a more robust and transparent security ecosystem.
