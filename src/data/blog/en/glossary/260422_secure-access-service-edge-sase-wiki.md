---
title: "Understanding SASE (Secure Access Service Edge): Definition and Architecture"
author: "editornom"
pubDatetime: 2026-04-22T09:00:55+09:00
slug: "what-is-sase-architecture-and-key-components"
featured: false
draft: false
ogImage: "../../../../../source/glossary/SASE_(Secure_Access_Service_Edge)/8c8212bf-0.webp"
description: "Learn about the concept of SASE, its core elements, and the differences between SASE and SSE as it integrates networking and security into a Cloud-native environment."
faqs:
- q: What is SASE (Secure Access Service Edge)?
  a: SASE is an architecture that integrates network functions (SD-WAN) and security services (SSE) into a single Cloud-native platform. It applies consistent security policies at the Edge based on 'identity,' regardless of user location or device.
- q: What is the background behind the emergence of SASE?
  a: As Cloud adoption and remote work expanded, traditional centralized perimeter security models began to cause bottlenecks. SASE emerged to reduce latency and improve efficiency by processing traffic near the user instead of backhauling it to headquarters.
- q: What are the main components of SASE?
  a: The core components are SD-WAN for network optimization and SSE for security. Specifically, it includes Zero Trust Network Access (ZTNA), Cloud Access Security Broker (CASB), Secure Web Gateway (SWG), and Firewall-as-a-Service (FWaaS).
- q: What does 'Edge' mean in the context of SASE?
  a: It refers to globally distributed Points of Presence (PoPs) rather than distant data centers. By performing security inspections and network optimization at locations physically closest to the user, data transmission speeds are maximized.
- q: What is the core operating principle of SASE?
  a: Instead of trusting a user's IP address, SASE verifies the 'context'—such as identity, device health, and connection location—for every access request. It works by inspecting traffic and controlling permissions in real-time through an integrated platform.
- q: What is the critical difference between SASE and SSE?
  a: SASE is a comprehensive framework that includes both networking (SD-WAN) and security functions. In contrast, SSE (Security Service Edge) is a subset of SASE that refers only to the security service stack, excluding network optimization features.
- q: What operational benefits do companies gain from adopting SASE?
  a: SASE significantly reduces management complexity by consolidating fragmented security solutions into a single platform. It also leverages Cloud scalability to respond flexibly to traffic spikes while providing unified security visibility.
- q: What role does Zero Trust (ZTNA) play within SASE?
  a: Based on the principle of 'Never Trust, Always Verify,' ZTNA authenticates every access request individually without distinguishing between internal and external boundaries. It prevents the spread of damage during security incidents by granting only the minimum necessary permissions for specific apps.
- q: How is SASE utilized in a remote work environment?
  a: When remote workers connect to the corporate network, they undergo real-time security inspections through the nearest Edge node without needing additional hardware. This process ensures secure connections by checking for malware and immediately controlling Cloud app permissions.
- q: What should companies consider when evaluating SASE adoption?
  a: First, assess the stability of the current network infrastructure. Strategic decisions are needed on whether to adopt SSE in stages if a network is already in place, or to transition to a full SASE model that includes SD-WAN.
---

![SASE (Secure Access Service Edge) - A network structure securely connecting central cloud systems and various devices](../../../../../source/glossary/SASE_(Secure_Access_Service_Edge)/8c8212bf-0.webp)

### 1. Wiki Summary Table

| Item | Content |
| :--- | :--- |
| English Name | Secure Access Service Edge |
| Abbreviation | SASE (pronounced 'sassy') |
| Related Technologies | SD-WAN, ZTNA, CASB, SWG, FWaaS |

### 2. Core Concepts of SASE
SASE is an architecture that consolidates corporate network functions (SD-WAN) and security services (SSE) into a single Cloud-native platform rather than keeping them as separate solutions. It applies consistent security policies based on 'identity,' regardless of where the user is or what device they are using. By processing traffic at the point closest to the user—without the need to reroute it through a central data center—it ensures both speed and efficiency.

### 3. Why the Security Paradigm Shifted
In the past, corporate networks relied on a "Castle-and-Moat" perimeter security model that surrounded the data center like a fortress. However, as work environments shifted toward Cloud and hybrid models, the limitations of this approach became clear. Forcing all external traffic to reroute to a headquarter server for security checks creates bottlenecks and degrades the user experience. SASE emerged to solve latency issues by moving the focus of security from the central server to the "Edge," closer to the user.

### 4. Key Components and Operating Principles
- <b>Integrated Service Availability</b>: SASE integrates the path optimization of SD-WAN with complex security functions like SWG, CASB, and ZTNA into a single platform. This drastically reduces the complexity of operational management.
- <b>Identity-Based Zero Trust</b>: Instead of trusting a user's IP address, SASE verifies the context—identity, device security status, and location—every time. It implements the Zero Trust principle of "Never Trust, Always Verify" at a practical, operational level.
- <b>Global Edge Points of Presence</b>: Security services are delivered through Points of Presence (PoPs) distributed worldwide. This prevents performance degradation caused by physical distance and allows for flexible scaling to handle traffic surges by utilizing Cloud-native scalability.

### 5. Differences Between SASE and SSE
While these two terms are often used interchangeably, there is a clear distinction. SASE refers to the entire framework encompassing both networking (SD-WAN) and security functions. On the other hand, SSE (Security Service Edge) is a subset of SASE that refers only to the security service stack (SWG, CASB, ZTNA, etc.), excluding the network optimization components. Companies that already have a stable network infrastructure often start by adopting SSE.

### 6. Practical Application and Key Terms
- <b>Real-World Application</b>: When a remote employee connects to the internal network, they pass through the nearest SASE Edge node for real-time inspection without requiring separate hardware devices. During this process, the system checks for malware infections and immediately manages access permissions for Cloud applications to maintain a secure connection.
- <b>Key Terminology</b>: 
  - <b>SD-WAN (Software-Defined Wide Area Network)</b>: A technology that virtualizes and manages wide-area networks through software.
  - <b>ZTNA (Zero Trust Network Access)</b>: A security approach that individually authenticates every access request without assuming trust based on network boundaries.
  - <b>CASB (Cloud Access Security Broker)</b>: A solution that mediates security policies and provides visibility between an organization and Cloud service providers.