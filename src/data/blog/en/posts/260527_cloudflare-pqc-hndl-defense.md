---
title: "Cloudflare's PQC Declaration and the 'Half-Shield': Why HNDL Defense Alone Isn't Enough"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-27 11:48:05.566836+09:00
slug: "cloudflare-pqc-hndl-defense"
featured: false
draft: false
ogImage: "../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp"
description: "We analyze Cloudflare's PQC implementation, focusing on ML-KEM-based strategies against future decryption attacks and the technical limitations in real-time threat response. Discover why infrastructure must extend to origin servers for true quantum-resistant security."
references:
- https://blog.cloudflare.com/post-quantum-warp/
- https://blogs.cisco.com/developer/how-post-quantum-cryptography-affects-security-and-encryption-algorithms
- https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/
modDatetime: 2026-05-27 11:58:05.566836+09:00
faqs:
- q: "What is Post-Quantum Cryptography (PQC)?"
  a: "It refers to a next-generation cryptographic system designed to be secure against the powerful computing capabilities of quantum computers. It involves algorithms currently being standardized by NIST to prepare for the eventual obsolescence of RSA and ECC in a quantum computing environment."
- q: "Why is the 'Harvest-Now-Decrypt-Later (HNDL)' attack dangerous?"
  a: "It is an attack where an adversary collects and stores encrypted traffic today, even if they cannot decrypt it immediately, with the intent to decrypt it later once a sufficiently powerful quantum computer is developed. This is critical for national secrets or long-term archived data."
- q: "What are the key features of the ML-KEM technology adopted by Cloudflare?"
  a: "ML-KEM is a Key Encapsulation Mechanism based on lattice cryptography. It focuses on securely generating and exchanging secret keys needed for data encryption in a way that is resistant to quantum attacks. It is currently selected as the NIST FIPS 203 standard."
- q: "Why are 'Digital Signatures' missing from the current PQC support?"
  a: "The digital signature standard, ML-DSA, has lagged behind key agreement methods in terms of standardization and infrastructure readiness. As a result, classical cryptography is still used to prove server identity, which limits defenses against real-time threats."
- q: "What does the 'Last Mile' security risk mentioned in the text mean?"
  a: "It refers to a phenomenon where the security chain is broken because the segment from the Cloudflare edge server to the origin server where the actual data resides still uses classical encryption, even if the connection between the user and the edge server is protected by PQC."
- q: "What performance issues should be considered when implementing PQC?"
  a: "PQC algorithms have significantly larger cryptographic keys and signature data compared to classical cryptography. This can lead to network packet fragmentation or increased handshake latency, making a prior review of network equipment performance and bandwidth essential."
- q: "What is the difference between Cloudflare's PQC strategy and Android 17's security approach?"
  a: "While Cloudflare focuses on tunneling security at the network layer, Android 17 integrates ML-DSA signatures from the hardware-based Verified Boot stage. Android aims for a more fundamental goal of building the device's entire Chain of Trust on a quantum-resistant foundation."
- q: "What should enterprise security managers keep in mind when using Cloudflare One?"
  a: "Beyond simply enabling the PQC option, they must apply strict policy overrides to prevent 'downgrade attacks' that force security levels lower. Additionally, the libraries of internal origin servers must be updated to comply with current standards."
- q: "Will using the quantum-resistant cryptography supported by Cloudflare slow down my company's server speed?"
  a: "PQC can cause slight delays during the initial connection phase due to larger key sizes. However, it affects connection establishment time rather than actual data transfer speed, and in modern hardware environments, this delay is often imperceptible to users."
- q: "Is it a waste of budget to switch to PQC infrastructure when quantum computers don't even exist yet?"
  a: "Due to Harvest-Now-Decrypt-Later (HNDL) attacks, data transmitted today could be threatened in the future. NIST recommends a full transition by 2035, and a gradual infrastructure shift is considered an essential investment in terms of the cost of preventing future security breaches."
---

<div class="bluf"><strong>[BLUF]</strong>
Cloudflare's current PQC support focuses on preventing future decryption attacks (HNDL) through 'Key Agreement (<a href="/en/glossary/ml-kem" class="glossary-tooltip" data-definition="A next-generation key encapsulation method designed to securely exchange secret keys even against attacks from quantum computers, utilizing lattice-based cryptography.">ML-KEM</a>)'. However, due to the lack of standardization in 'Digital Signatures (ML-DSA)', it remains limited in defending against real-time Man-in-the-Middle (MITM) attacks. For true end-to-end security, PQC upgrades are essential for the 'Origin Server' segment beyond the WARP tunnel, necessitating an infrastructure transition that goes beyond simple client updates.</div>

Warnings of 'Q-Day,' the day quantum computers will dismantle modern encryption systems, are no longer relegated to the realm of science fiction. While global security giant Cloudflare’s full-scale introduction of <a href="/en/glossary/post-quantum-cryptography" class="glossary-tooltip" data-definition="A next-generation cryptographic algorithm system that cannot be decrypted even by the computational power of quantum computers.">Post-Quantum Cryptography</a> to its WARP clients is an encouraging sign, a look at the technical underpinnings reveals that we are still holding a 'half-shield.' In this analysis, we will take a cold, hard look at the actual value of Cloudflare's PQC declaration and the critical gaps hidden behind it from the perspective of a security architect.

## 1. Why Current PQC Support Is Biased Toward 'HNDL' Attacks

### The Gap Between ML-KEM Adoption and the Absence of ML-DSA

The first technology Cloudflare adopted, ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism), is a technique for safely generating and sharing secret keys used to encrypt data. This is a highly effective means of defending against <a href="/en/glossary/harvest-now-decrypt-later" class="glossary-tooltip" data-definition="An attack where current encrypted traffic is collected and stored so it can be decrypted in the future once powerful quantum computers are developed.">Harvest-now-decrypt-later</a> attacks, where adversaries collect current encrypted traffic to decrypt it in the future. However, 'Digital Signatures,' the other pillar of encrypted communication, still rely on classical RSA or Elliptic Curve Cryptography (ECC), leaving the server authentication stage exposed to quantum threats.

### Current PQC Tunneling Structures Still Exposed to Active Attacks (MITM)

A PQC tunnel without digital signatures is like replacing a vault lock with a state-of-the-art model while the owner's ID remains an easily forged piece of paper. In a Man-in-the-Middle (MITM) environment where an attacker intervenes in real-time to present a fake certificate, a security tunnel built only with ML-KEM is likely to be neutralized. Until NIST's FIPS 204 standard, ML-DSA, is fully integrated across the infrastructure, current PQC remains a limited defense system that only prevents passive eavesdropping.

![Post-Quantum Cryptography - A digital safe with a glass texture, featuring a glowing circuit at the center symbolizing encryption technology, and fine cracks at the edges indicating missing digital signatures.](../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp)

## 2. The Massive Gap in End-to-End Quantum Security: Origin Server Limitations

### The 'Last Mile' Security Risk WARP Clients Can't Solve

Even if a user is securely connected to a Cloudflare Edge server via WARP, the segment from the edge server to the origin server where the actual data is stored remains a problem. If classical cryptographic systems are still used in this segment, the entire security chain will eventually break at its weakest link. This absence of 'last mile' security in the architecture is a key reason why companies should not mistake Cloudflare's PQC support for the immediate safety of their entire infrastructure.

### Technical Barriers to Automatic SSL/TLS Upgrades and Standardization Issues

Cloudflare is attempting to upgrade connections to origin servers through its Automatic SSL/TLS feature, but it faces massive walls of hardware compatibility and performance degradation. Because ML-KEM keys are significantly larger than those of classical cryptography, they can cause network packet fragmentation and handshake latency. Highlighting PQC as a marketing rhetorical device without resolving this technical debt makes it difficult to avoid criticism that it is more about brand imaging than substantive security enhancement.

![An abstract visualization of a data bridge made of translucent glass blocks, where the first half is glowing with quantum energy and the second half is crumbling into wireframe, symbolizing the broken security chain between edge and origin servers, soft blue and orange studio lighting](../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp)

## 3. Comparative Analysis with Android 17's Hardware-Based PQC Strategy

### Building an OS-Level Chain of Trust vs. Network Layer Security

Unlike Cloudflare, a cloud service, Google's Android 17 takes a more fundamental approach. By integrating ML-DSA into the hardware-level Android Verified Boot (AVB) stage, it demonstrates a strategy for securing quantum resistance from the moment of boot. This provides a much stronger 'Root of Trust' than merely layering security at the network level, creating a decisive difference in guaranteeing the integrity of the entire operating system.

### A Practical Response Guide for Enterprise Client (Cloudflare One) Users

Enterprise security managers currently using Cloudflare One should not be satisfied with simply toggling a PQC setting. They must enforce a 'PQC Only' mode through MDM (Mobile Device Management) policies and apply strict policy overrides to prevent attackers from attempting downgrade attacks. Furthermore, a true quantum-resistant architecture can only be completed by updating internal origin server libraries to meet the latest NIST standards.

| Security Entity | Algorithm Applied | Primary Security Layer | NIST Compliance & Authority |
| :--- | :--- | :--- | :--- |
| Cloudflare | ML-KEM (Key Agreement) | Network/Tunneling (MASQUE) | FIPS 203 (ML-KEM-768 Hybrid) |
| Android 17 | ML-DSA (Digital Signature) | Hardware/Kernel (AVB) | FIPS 204 (Chain of Trust) |
| Cisco (SKIP) | PSK-DHE / ML-KEM | VPN/IPSec Infrastructure | Leading global standardization based on IOS-XE |
| Google Play | ML-DSA (Hybrid Signature) | App Distribution Layer | App integrity verification and anti-tampering |

> "PQC tunneling blocks the static threat of 'Harvest-now-decrypt-later,' but the current structure, lacking digital signatures, remains a classical shield against the active threat of Man-in-the-Middle (MITM) attacks."

> "While Android 17 strengthens fundamental security by building a hardware-based Chain of Trust, cloud edge security still faces the technical debt of a standardization gap with origin servers."

## Conclusion: True Security Sovereignty Toward Q-Day—Infrastructure Innovation Beyond Marketing Terms Is Key

Quantum security is not a simple checkbox option; it signifies a paradigm shift for the entire infrastructure. Cloudflare's moves are certainly in the right direction, but the absence of digital signatures and the isolation of origin servers remain challenges for us to solve. Only when we clearly recognize the vulnerabilities hidden behind the brilliance of the technology and implement gradual infrastructure upgrades will we be able to safely welcome the coming quantum era.

* NIST and Industry Quantum Security Response Status:
  - **Over 45%**: The percentage of human-generated traffic sent to Cloudflare that already has post-quantum encryption applied.
  - **2030**: The point at which the use of classical cryptographic algorithms (RSA, ECC) of 112 bits or less will be officially deprecated according to NIST guidelines.
  - **2035**: The final deadline by which the use of classical cryptographic algorithms is strictly disallowed, and all federal security systems must fully transition to PQC.
  - **5-15 Years**: The timeframe experts predict for the emergence of Cryptographically Relevant Quantum Computers (CRQC) and the collapse of modern cryptographic systems.

## 🔗 Recommended Reading
- [The Rust Paradox: How Innovative Safety Leads to Management Bottlenecks and Productivity Crises](/en/posts/rust-paradox-safety-productivity)
- [Warp's Open Source Declaration: Developer Freedom or AI Dependency in the Agent-First Era?](/en/posts/warp-open-source-agent-first-era)