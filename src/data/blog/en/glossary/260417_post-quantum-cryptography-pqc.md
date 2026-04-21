---
title: Post-Quantum Cryptography (PQC)
author: editornom
pubDatetime: 2026-04-17 08:35:27+09:00
slug: post-quantum-cryptography-pqc
featured: false
draft: false
tags:
- glossary
- Cybersecurity
- QuantumComputing
- Cryptography
description: An overview of Post-Quantum Cryptography (PQC), a next-generation encryption
  framework designed to remain secure against the advanced computational power of
  quantum computers.
faqs:
- q: What is Post-Quantum Cryptography (PQC)?
  a: PQC refers to new cryptographic algorithms designed to keep data secure even
    against attacks from future quantum computers with massive processing power. Unlike
    current public-key encryption, it ensures security by leveraging complex mathematical
    problems such as lattices or codes.
- q: Why should we pay attention to Post-Quantum Cryptography right now?
  a: Because the RSA and ECC encryption systems currently in use are at risk of being
    decrypted almost instantly by Shor’s algorithm on a quantum computer. For national
    secrets or data requiring long-term storage, security levels must be raised now
    to prepare for future threats.
- q: What does the term 'Q-Day' mean?
  a: Q-Day refers to the moment when quantum computing technology advances to the
    point where it can completely neutralize the standard cryptographic systems we
    use today. Security experts aim to complete the transition to secure PQC before
    this day arrives.
- q: What are the main technical characteristics of PQC?
  a: PQC is characterized by its use of sophisticated mathematical structures—like
    lattice-based, multivariate, and hash-based systems—that are difficult for quantum
    computers to solve. Since it is a purely algorithmic software approach, it is
    highly compatible with existing internet infrastructure.
- q: What is a 'Harvest Now, Decrypt Later' attack?
  a: This is an attack method where encrypted data is collected today with the intent
    to decrypt it in the future when high-performance quantum computers become available.
    To defend against this, PQC should be applied proactively, considering the duration
    for which the data remains sensitive.
- q: What is the difference between QKD and PQC?
  a: PQC is a mathematical algorithm that runs as software on existing networks, while
    QKD requires dedicated fiber-optic cables and special hardware to utilize the
    physical properties of quantum mechanics. PQC is focused on data encryption, whereas
    QKD is mainly focused on secure key distribution and eavesdropping detection.
- q: What strategy is used when introducing PQC to existing systems?
  a: A 'Hybrid Migration Strategy' is primarily used, where classical cryptography
    (RSA, ECC) and new PQC algorithms are used together. This is a practical way to
    ensure defense against quantum attacks while the long-term stability of PQC algorithms
    is being fully verified.
- q: What are the currently standardized international PQC algorithms?
  a: Led by the U.S. National Institute of Standards and Technology (NIST), algorithms
    such as ML-KEM (formerly Kyber) and ML-DSA (formerly Dilithium) have been selected
    as standards. These lattice-based algorithms are becoming the new standard for
    security solutions worldwide.
- q: What is the significance of Apple's 'PQ3' adoption in the security industry?
  a: By applying the PQ3 protocol to iMessage in 2024, Apple became a leader among
    global tech giants in deploying PQC for large-scale services. This case serves
    as a symbolic proof that robust, quantum-level end-to-end encryption is possible
    even in everyday mobile messaging.
- q: How does Grover's Algorithm affect the PQC environment?
  a: Grover's Algorithm has the property of halving the security strength of symmetric-key
    encryption. To counter this in a PQC environment, security is maintained by using
    longer key lengths than before, such as AES-256.
---

![Post-quantum cryptography securing data against quantum attacks.](../../../../../source/glossary/PQC/7c7a31fa-0.png)

| Category | Content |
| :--- | :--- |
| **English Name** | Post-Quantum Cryptography |
| **Abbreviation** | PQC |
| **Related Technologies** | Lattice-based Cryptography, Shor's Algorithm, NIST PQC Standards, ML-KEM, ML-DSA |

## The Core of Post-Quantum Cryptography
Post-Quantum Cryptography (PQC) refers to new cryptographic algorithms designed to protect data from attacks by quantum computers capable of ultra-high-speed processing. As the mathematical problems that current public-key infrastructure (PKI) relies on face potential obsolescence due to quantum algorithms like Shor's algorithm, PQC ensures security by utilizing more complex mathematical structures, such as lattices or codes.

## Quantum Threats and the Background of Adoption
The RSA and ECC-based public-key encryption systems we use today are grounded in the difficulty of integer factorization or discrete logarithms. However, once sufficiently powerful quantum computers become commercially available, Shor's algorithm will be able to solve these problems in a very short amount of time.

A particularly concerning threat to the security industry is the "Harvest Now, Decrypt Later" (HNDL) attack model. In this scenario, an adversary collects encrypted sensitive data today, even if they cannot decrypt it immediately, with the intention of decrypting it in the future once quantum computers are available. This is why a preemptive transition to PQC is being discussed now to protect national secrets and long-term corporate data.

## Technical Features and Implementation
*   **Utilization of New Mathematical Problems**: PQC employs complex mathematical structures—such as lattice-based, multivariate, hash-based, and code-based systems—that have been proven difficult for even quantum computers to solve efficiently.
*   **High Compatibility with Existing Infrastructure**: Unlike Quantum Key Distribution (QKD), which requires specialized physical hardware, PQC is a software-based approach purely rooted in algorithms. It offers excellent versatility as it can be implemented on current digital communication networks and devices through simple algorithm updates.
*   **Hybrid Migration Strategy**: Until the stability of new algorithms is fully verified, a hybrid approach that uses both classical cryptography (RSA, ECC) and PQC in tandem is commonly adopted. This is a realistic strategy to prepare for quantum attacks while safeguarding against any unforeseen vulnerabilities in the new algorithms.

## Difference from Quantum Key Distribution (QKD)
*   **Post-Quantum Cryptography (PQC)**: Focuses on creating **mathematical algorithms** that are resistant to quantum computing. It operates as software within existing internet environments, primarily to maintain data confidentiality.
*   **Quantum Key Distribution (QKD)**: Utilizes the **physical properties** of quantum mechanics (such as the no-cloning theorem and state changes upon observation). It requires dedicated fiber-optic cables and expensive quantum hardware, and is mainly used to detect eavesdropping during key exchange.

## Real-world Applications and Related Concepts
*   **Apple’s PQ3 Adoption**: In 2024, Apple implemented a PQC protocol called 'PQ3' in iMessage. This is considered a landmark case where a global Big Tech company deployed PQC at scale, raising the bar for end-to-end encryption (E2EE) security.
*   **Key Terminology**:
    *   **Q-Day (Y2Q)**: The point in time when quantum computers will be powerful enough to completely break current cryptographic systems.
    *   **NIST PQC Standards**: Standard algorithms selected by the National Institute of Standards and Technology (NIST), including ML-KEM (formerly Kyber) and ML-DSA (formerly Dilithium).
    *   **Grover's Algorithm**: A quantum algorithm that effectively halves the security strength of symmetric-key cryptography. To counter this, PQC environments maintain security by increasing symmetric key lengths, such as using AES-256.
