---
title: "Bloated and Imperfect Fortresses: The Mathematical Gambles and Structural Cracks of Public Key Encryption"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-30 15:12:46.260104+09:00
slug: "public-key-encryption-flaws"
featured: false
draft: false
ogImage: "../../../../../source/posts/공개키_암호화/05880d68-0.webp"
description: "Public key encryption revolutionized digital trust by solving the key distribution problem, yet it carries structural limitations such as computational inefficiency and mathematical challenges. We analyze the essence of public key encryption and hybrid security systems, which face inevitable change in the quantum computing era."
references:
- https://people.cs.rutgers.edu/pxk/classes/419/notes/integrity-1.html
- https://nordpass.com/blog/public-key-encryption/
- https://www.keyfactor.com/blog/best-practices-for-public-key-vs-private-key-management/
modDatetime: 2026-05-30 15:22:46.260104+09:00
faqs:
- q: "What is public key encryption?"
  a: "It is a method of encrypting and decrypting data using two different keys: a public key and a private key. It became the standard for modern digital security by overcoming the physical limitations of symmetric encryption, which required sharing secret keys in advance."
- q: "What is the biggest advantage of public key encryption?"
  a: "The most significant achievement is solving the key distribution problem. By allowing anyone to have the public key for encryption while the owner keeps the private key for decryption, it enables secure communication even in open environments like the Internet."
- q: "Why is this method referred to as a mathematical gamble?"
  a: "Because public key systems rely on the hypothesis that integer factorization or discrete logarithm problems are difficult to solve with current computing resources. In other words, security is not perfectly proven; it implies the uncertainty that an efficient solution simply hasn't been discovered yet."
- q: "What is the difference between RSA and ECC?"
  a: "RSA utilizes the difficulty of factoring large integers, while ECC uses the discrete logarithm problem on elliptic curves. ECC is considered more advanced in terms of computational efficiency because it can provide the same security strength with much smaller bit sizes than RSA."
- q: "Why is public key encryption said to have low computational efficiency?"
  a: "It is because it performs complex mathematical modular exponentiation or point addition operations. Compared to symmetric key methods that perform simple bit substitutions, it consumes hundreds to thousands of times more CPU resources and has significantly slower data processing speeds."
- q: "Why is padding essential in public key encryption?"
  a: "If only the pure algorithm is used, the same plaintext will always result in the same ciphertext, allowing attackers to guess the content. Padding techniques like OAEP mix random data with the plaintext to hide patterns in the ciphertext, thereby enhancing security."
- q: "What kind of structure does a hybrid cryptosystem refer to?"
  a: "It is a method that combines the security of public key encryption with the efficiency of symmetric key encryption. It is a practical yet anomalous structure where the heavy public key is used only to safely deliver a symmetric key, while the actual encrypted transmission of large volumes of data is handled by the fast symmetric key."
- q: "What threat does quantum computing pose to public key encryption?"
  a: "Quantum computers equipped with Shor's algorithm can solve integer factorization and discrete logarithm problems almost instantaneously. This fundamentally neutralizes existing RSA and ECC systems, making the transition to Post-Quantum Cryptography (PQC) urgent."
- q: "Does using public key encryption increase server load and costs?"
  a: "Yes, that's correct. Public key operations like RSA consume a significant amount of CPU resources. To optimize server costs and speed, a hybrid method is used where public keys are used briefly only for the initial key exchange, rather than for processing all data."
- q: "Is it true that Elliptic Curve Cryptography is better than RSA these days?"
  a: "Yes, it is true. ECC uses much shorter keys than RSA while offering stronger security. Since the keys are smaller, the amount of data transmitted is reduced and computations are relatively faster, which is why most modern smartphone apps and web browser security prefer ECC."
---

<div class="bluf"><strong>[BLUF]</strong><p>Public key encryption is a brilliant compromise that solved the symmetric key distribution problem, but it is fundamentally an unstable architecture reliant on unproven mathematical challenges and abysmal computational efficiency. Defined as a 'bloated fortress' that cannot stand without padding and hybrid structures, it is a historical legacy whose replacement by the post-public key era is inevitable due to the emergence of quantum computing.</p></div>

Behind every digital trust that sustains modern society lies a precarious hypothesis known as 'mathematical difficulty.' From the banking systems we use daily to private messenger conversations, the public key encryption technology responsible for all this security is, in fact, the result of a 'massive compromise' with a structure as heavy and inefficient as its status is prestigious.

## 1. The Origin of Trust: A 'Great Compromise' Solving Symmetric Key Distribution

### - Limitations of Shared Secrets and the Era of Asymmetry Opened by Diffie-Hellman

In the past, cryptographic systems relied on symmetric key methods where both parties had to share a secret key in advance for communication to work. However, in the vast and open environment of the Internet, safely sharing a secret key with unspecified individuals worldwide was physically near-impossible. To break through these limitations, the concept of a <a href="/en/glossary/trapdoor-function" class="glossary-tooltip" data-definition="A function that is easy to compute in one direction but impossible to compute in the opposite direction without specific information.">trapdoor function</a> was revolutionary. The logic of asymmetry—where anyone can lock the information, but only the owner with the key can open it—opened a new era of security.

However, this innovation was not free. Instead of requiring prior trust between communicating parties, we began to pay a massive cost in computational inefficiency. This was a historical choice by humanity to sacrifice speed for security and choose complexity over flexibility.

### - Unproven Mathematical Complexity: The 'Gamble' of Factorization and Discrete Logarithms

Did you know that the cryptographic systems we trust implicitly, such as RSA or ECC, are actually based on 'unsolved homework'? These systems rely on the empirical statistic that the difficulty of integer factorization or the complexity of discrete logarithm problems will not change in the future. In other words, they are not mathematically proven to be perfectly secure in a rigorous sense; rather, they are like a massive gamble built on the hypothesis that they will be difficult to solve with current computing resources.

![Public Key Encryption - A giant lock made of glass and crystal reflecting glowing mathematical formulas in a dark virtual space.](../../../../../source/posts/공개키_암호화/05880d68-0.webp)

## 2. The Paradox of Efficiency: Why Wrap 64-bit Data in 2048-bit Armor?

### - Fatal Flaws of RSA: Computational Load and Inefficient Ciphertext Expansion

In the actual data transmission process, public key encryption shows abysmal efficiency. <a href="/en/glossary/modular-exponentiation" class="glossary-tooltip" data-definition="An operation that finds the remainder of a power divided by a specific number, serving as the core mathematical basis for RSA encryption.">Modular exponentiation</a>, the core of RSA encryption, is a primary culprit that consumes hundreds to thousands of times more CPU resources compared to symmetric keys (AES) that perform simple bit substitution. The inefficiency of having to generate a massive 2048-bit ciphertext block just to protect a few bytes of information is no different from deploying a giant armored vehicle just to move a single needle.

### - The Rise of ECC (Elliptic Curve): Proving RSA's Bloat and Persistent Computational Limits

To address the bloat of RSA, Elliptic Curve Cryptography (ECC) emerged, drastically reducing key sizes. However, ECC also involves complex mathematical procedures called point addition, which still has clear structural limitations for encrypting large volumes of data in real-time. Ultimately, we do not gain 'efficiency' through public keys; we only seek the 'delivery of trust.'

| Encryption Method | Core Mathematical Principle | Key Size for Security Strength (bits) | Computational Speed (Relative to AES-128) |
| :--- | :--- | :--- | :--- |
| RSA-3072 | Integer Factorization Problem | 3,072 bits | Approx. 1,000x slower or more |
| ECC-256 | Elliptic Curve Discrete Logarithm | 256 bits | Approx. 100x slower or more |
| AES-128 | Substitution and Permutation Operations | 128 bits | Baseline (Very Fast) |

## 3. Inherent Vulnerabilities and Life Support: Padding and the Shadow of Symmetric Keys

### - The Reality of Raw Encryption: Vulnerable to Chosen-Plaintext Attacks

As a pure mathematical algorithm, public key encryption is actually much more vulnerable than one might think. Because it always outputs the same ciphertext for the same plaintext, it is highly susceptible to 'guessing' where an attacker inputs predictable plaintexts. To defend against this, we add auxiliary devices called padding techniques, such as OAEP. This is a prime example of how original encryption technology cannot protect itself and must rely on external support systems.

### - Hybrid Cryptosystems: A 'Dull Armored Vehicle' Carrying a 'Racing Car' Called Symmetric Keys

> Public key encryption is not an independent, perfect security solution; it is merely a heavy and dull armored vehicle designed to safely transport the racing car that is the symmetric key.

Modern security systems have an anomalous symbiotic structure where the public key safely delivers the symmetric key, and the symmetric key handles the fast processing of actual data. We want to use the high-speed 'racing car,' but we are forced to charter a heavy 'armored vehicle' to pass through the dangerous road of key delivery. This double structure can be seen as a kind of 'necessary evil' maintenance cost that the modern IT ecosystem pays to maintain security.

![Public Key Encryption - A sleek neon car safely protected inside a massive transparent sphere.](../../../../../source/posts/공개키_암호화/9aa20cd6-1.webp)

## 4. The End of the Crumbling Fortress: Quantum Computing and the Dawn of Post-Public Key

### - <a href="/en/glossary/shors-algorithm" class="glossary-tooltip" data-definition="An algorithm that can solve integer factorization and discrete logarithm problems very quickly using a quantum computer, potentially neutralizing existing public key cryptosystems like RSA or ECC.">Shor's Algorithm</a>: Aiming for the Heart of Asymmetric Encryption

The mathematical barriers that have guarded the fortress for decades are now shaking before the massive wave of quantum computing. The emergence of Shor's algorithm points directly at the heart of public key systems: integer factorization and discrete logarithm problems. If a quantum computer with sufficient performance appears, the RSA and ECC systems we currently use are essentially living on borrowed time and could be neutralized instantly.

### - Monumental Value and Limitations of Public Key Encryption at the End of a Great Era

The numerical limitations of public key encryption are clear:
1. **Computational Efficiency**: RSA-2048 modular exponentiation consumes approximately 1,000 to 10,000 times more CPU cycles than software-implemented AES-128 without hardware acceleration.
2. **Data Expansion**: In RSA encryption, even sending 1 byte of data generates a ciphertext block of at least 256 bytes (2048 bits), causing bandwidth waste.
3. **Quantum Threat**: When Shor's algorithm is applied, current RSA and ECC systems possess structural vulnerabilities that allow them to be decrypted in polynomial time by a quantum computer with sufficient qubits.

# Conclusion: A Historical Legacy of Modern Security Built on Imperfect Mathematics

The foundation of the digital trust we enjoy is like a massive gambling house built on mathematical conjectures that things are 'hard to solve,' which could collapse at any time. Even if public key encryption is an inefficient and unstable architecture, it cannot be denied that it is the most sophisticated historical legacy humanity has created to overcome the fundamental limitations of the communication environment. Now, we stand at a point where we must look beyond this bloated fortress and prepare for a new horizon of security suitable for the quantum era.

## 🔗 Recommended Reading
- [SilverTorch: Meta's 23x Performance Leap or the Start of New 'Technical Debt'?](/en/posts/silvertorch-meta-23x-performance-technical-debt)
- [Model Context Protocol (MCP): The 'USB-C' of AI Integration or a 'Pandora's Box' of Security?](/en/posts/mcp-model-context-protocol-usb-c-pandoras-box)