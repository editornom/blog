---
title: "The First Step to Quantum Security: The Connection Gap in Cloudflare PQC"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-02 11:07:45.171268+09:00
slug: cloudflare-pqc-connection-gap
featured: false
draft: false
ogImage: "../../../../../source/posts/PQC_(Post-Quantum_Cryptography)/e863a673-0.webp"
description: "To counter quantum computing threats, Cloudflare has implemented Post-Quantum Cryptography (PQC) in WARP and Cloudflare One. We explore technical strategies to protect data from 'Harvest Now, Decrypt Later' attacks and meet NIST security standards."
references:
- https://blog.cloudflare.com/post-quantum-warp/
- https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/
- https://www.keyfactor.com/education-center/what-is-post-quantum-cryptography-and-why-does-it-matter/
modDatetime: 2026-05-02 11:17:45.171268+09:00
faqs:
- q: "What is Post-Quantum Cryptography (PQC) and why is it necessary?"
  a: "It is a next-generation encryption technology designed to be secure against the powerful computing capabilities of quantum computers. It is being introduced to ensure long-term data security as traditional RSA and ECC methods become vulnerable."
- q: "What exactly is a 'Harvest Now, Decrypt Later' attack?"
  a: "It is a strategy where attackers collect encrypted data now, even if they cannot decrypt it yet, to decrypt it later using high-performance quantum computers. This is particularly critical for government secrets and financial data."
- q: "What is the core algorithm of the PQC technology introduced by Cloudflare?"
  a: "The core is the ML-KEM algorithm, which uses lattice-based mathematical models. It is currently a standard recommended by NIST and is designed based on mathematical problems far more complex than traditional methods."
- q: "Do I need special settings to use PQC on the WARP client?"
  a: "It is automatically applied if you are using WARP for Windows (version 2025.5.893.0 or higher) or the latest iOS version. You can enjoy the latest security technology immediately without additional hardware or costs."
- q: "What does Hybrid Encryption Mode mean?"
  a: "It is a method of dual-protecting data by simultaneously using the new Post-Quantum Cryptography (ML-KEM) and existing classical cryptography (X25519). It serves as a safety net against potential flaws in the new algorithm."
- q: "What are the limitations of Cloudflare's PQC implementation?"
  a: "The protection is limited to the segment between the client and the Cloudflare network. If the segment from Cloudflare to the final destination (origin server) uses classical encryption, security vulnerabilities still exist."
- q: "Does applying PQC slow down network speeds?"
  a: "According to internal benchmarks, the PQC environment using the QUIC-based MASQUE protocol showed more efficient computation speeds than existing TLS 1.2. The focus is on efficient implementation rather than performance degradation."
- q: "How does the downgrade policy affect security?"
  a: "Allowing a transition to classical encryption if a PQC connection fails increases availability, but it requires caution as it can provide a path for 'downgrade attacks' where attackers forcibly lower the security level."
- q: "'Can I stop worrying about quantum computer hacking entirely just by installing the latest WARP?'"
  a: "It is a partial success. While the entrance from the user to Cloudflare is strengthened, perfect defense requires the entire path to the destination server to support PQC, necessitating general infrastructure improvements."
- q: "'Will server costs increase significantly if I apply quantum encryption to Cloudflare One at work?'"
  a: "Cloudflare provides the PQC environment at no extra charge, so there is no direct increase in Cloud costs. However, operational effort may be required for engineers to redesign infrastructure to match security levels across the entire segment."
---

Concerns that quantum computing could neutralize existing encryption systems are emerging as a realistic security threat. As the National Institute of Standards and Technology (NIST) has specified 2030 as the phase-out period for RSA and Elliptic Curve Cryptography (ECC), the industry's response is accelerating. Cloudflare's recent introduction of Post-Quantum Cryptography (PQC) technology to its WARP client is evaluated as a proactive measure reflecting this trend. However, looking into the technical implementation details, this is more of a transitional response during a period of major shift rather than the establishment of complete security.

**Proactive Response to 'Harvest Now, Decrypt Later' Scenarios**

The most alarming aspect for the security industry today is the "Harvest Now, Decrypt Later" (HNDL) strategy. This involves an attacker capturing and storing encrypted data now, with the intent of decrypting it en masse once sufficiently powerful quantum computers are developed in the future. Data requiring long-term security longevity, such as financial records or government secrets, is already within the potential risk group for exposure.

According to Cloudflare data, over 45% of general traffic currently entering its network is already protected by post-quantum encryption. This speed is ahead of NIST's recommended timeline and is significant in that it provides a PQC environment to users without additional hardware implementation or cost burdens. In particular, applying this technology to both the consumer WARP (1.1.1.1) and the enterprise Cloudflare One agent is a decision that accurately targets the importance of endpoint security.

![PQC (Post-Quantum Cryptography) - A structural diagram showing a secure connection between a remote worker's laptop and a corporate server via PQC and MASQUE technologies.](../../../../../source/posts/PQC_%28Post-Quantum_Cryptography%29/e863a673-0.webp)

**Technical Combination of MASQUE Protocol and ML-KEM**

The core of this PQC implementation is MASQUE (Multiplexed Application Substrate over QUIC Encryption) tunneling technology based on the <a href="/en/glossary/what-is-quic" class="glossary-tooltip" data-definition="A transport protocol designed based on UDP to reduce internet communication latency and enhance security, improving the speed and efficiency of modern web connections.">QUIC</a> protocol. It utilizes the ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism) algorithm, which uses lattice-based mathematical models. Notably, the current PQC application works in a 'Hybrid Mode' combined with the existing classical encryption, X25519. This strategy runs existing encryption systems in parallel as a safety net against potential defects that may arise in the new algorithm.

Internal benchmark results showed that the performance of applying ML-KEM-768 in a hybrid mode within a TLS 1.3 environment recorded more efficient computation speeds than encryption based on the older TLS 1.2. These encryption sequences are immediately operational in the latest client environments of WARP Desktop for Windows (version 2025.5.893.0 or higher) and iOS (version 1.11 or higher).

| Category | Classical Public Key Cryptography | Post-Quantum Cryptography (PQC) |
| :--- | :--- | :--- |
| Main Algorithms | RSA, ECC (ECDH, ECDSA) | ML-KEM (Kyber), ML-DSA (Dilithium) |
| Mathematical Basis | Factoring, Discrete Logarithm Problems | Lattice-based Mathematics |
| Quantum Threat Response | Can be neutralized by Shor's Algorithm | Resistant to currently known quantum algorithms |
| Primary Use | Key Exchange, Digital Signatures | Key Encapsulation (KEM), Digital Signatures |
| Performance Impact | Relatively low computational load | Load increases due to larger key and signature sizes |

**The Origin Server Gap and Segment Security Limitations**

Despite building these defenses, structural limitations still exist. The PQC protection segment provided by Cloudflare is limited to the area between the client and the Cloudflare network. For true end-to-end encryption, the final destination—the origin server—must also support post-quantum cryptography. However, the majority of corporate and public web servers still remain within legacy systems.

Even if the WARP client transmits data through a post-quantum tunnel, if it is converted back to classical encryption for the final segment from the Cloudflare edge server to the origin server, security uncertainty increases once again. The entrance to the tunnel is a solid fortress, but the exit is left in a vulnerable state. Furthermore, ML-DSA, a core component of the authentication system, is still in the process of standardization, making a technical gap inevitable until a complete trust system is secured.

![A realistic 3D infographic showing a secure tunnel with a transparent section revealing the internal data flow, one end glowing with advanced blue light (PQC) and the other end fading into dim orange (Legacy), emphasizing the security gap.](../../../../../source/posts/PQC_%28Post-Quantum_Cryptography%29/e863a673-0.webp)

**Downgrade Inducement and Operational Challenges**

The 'Allow Downgrade' policy, designed to ensure compatibility, is also a point that needs review from a security perspective. Cloudflare has set a phase 1 transition period until the summer of 2026, allowing connections to downgrade to classical encryption if PQC negotiation fails. While this is a desperate measure for service availability, it can become a path for downgrade attacks where an attacker intentionally interferes with the communication environment to force a lower security level.

Options to enforce PQC-only mode via MDM (Mobile Device Management) exist, but this is an alternative limited to enterprise environments with professional management capabilities. For general users or small organizations, such settings are likely to act as an operational burden. The reason Google integrated ML-DSA-based digital signatures into Android 17 and set a goal for full transition by 2029 is the judgment that it is difficult to fundamentally block quantum threats through the fragmented responses of individual companies alone.

Introducing PQC is a complex task that goes beyond simply replacing encryption algorithms; it requires redesigning the entire corporate infrastructure. Rather than being satisfied with strengthening security at the tunnel entrance, efforts must be made to uniformly raise the security level across the entire segment, including the origin server. Ultimately, true post-quantum security will be achieved only when all network nodes share the same security standards and the security blind spots left for backward compatibility are completely eliminated.

## 🔗 Recommended Reads
- [The Technological Landscape Reshaped by Attention and the Pros and Cons of Transformers](/en/posts/attention-transformers-tech-landscape)
- [MCP: The Blueprint for a Standard Protocol Navigating the Complexity of AI Integration](/en/posts/mcp-ai-integration-standard-protocol)