---
title: "Cloudflare的PQC宣言与“半截盾牌”：仅靠防御“收获后解密”(HNDL)还远远不够"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-27 11:48:05.566836+09:00
slug: "cloudflare-pqc-hndl-defense"
featured: false
draft: false
ogImage: "../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp"
description: "通过Cloudflare的PQC部署现状，分析基于ML-KEM的未来解密攻击防御策略及实时威胁应对的技术局限。了解为何为了实现真正的量子抗性安全，基础设施转型必须扩展至源站服务器。"
references:
- https://blog.cloudflare.com/post-quantum-warp/
- https://blogs.cisco.com/developer/how-post-quantum-cryptography-affects-security-and-encryption-algorithms
- https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/
modDatetime: 2026-05-27 11:58:05.566836+09:00
faqs:
- q: "什么是量子抗性密码 (PQC)？"
  a: "这是一种旨在即使面对量子计算机的强大计算能力也无法被破解的下一代加密算法体系。为了应对现有的 RSA 或 ECC 加密体系在量子计算环境下失效，NIST 等机构正在推进该技术的标准化。"
- q: "“先收获，后解密 (HNDL)”攻击为什么危险？"
  a: "因为攻击者即便现在无法解密，也会预先收集并存储加密流量，待未来开发出性能卓越的量子计算机时，再对过去的这些数据进行解密。这对国家机密或需要长期保存的数据具有致命威胁。"
- q: "Cloudflare 采用的 ML-KEM 技术有哪些主要特点？"
  a: "这是一种利用格密码学的密钥封装方式。它专注于安全地生成和交换加密数据所需的私钥，使其免受量子计算机攻击。目前已被选定为 NIST FIPS 203 标准。"
- q: "为什么目前的 PQC 支持方式中缺少“数字签名”？"
  a: "因为数字签名标准 ML-DSA 的标准化及基础设施应用速度慢于密钥协商方式。因此，在证明服务器合法性的阶段，仍在使用古典密码，这在应对实时威胁方面存在局限性。"
- q: "文中提到的“最后一公里”安全风险是指什么？"
  a: "这意味着虽然用户与 Cloudflare 边缘服务器之间受 PQC 保护，但从边缘服务器到实际存储数据的源站服务器之间的区间如果仍使用古典密码，安全链条就会断裂。该区间将成为量子威胁的盲区。"
- q: "引入 PQC 时需要考虑哪些技术性能问题？"
  a: "与古典密码相比，PQC 算法的加密密钥和签名数据量要大得多。这可能会导致网络数据包分片或握手延迟增加，因此必须预先审查网络设备的性能和带宽。"
- q: "Cloudflare 的 PQC 策略与安卓 17 的安全方案有什么区别？"
  a: "Cloudflare 侧重于网络层的隧道安全，而安卓 17 则从基于硬件的验证启动阶段就开始整合 ML-DSA 签名。安卓的目标更根本，即构建设备自身的量子抗性信任链。"
- q: "企业安全管理员在使用 Cloudflare One 时应注意什么？"
  a: "除了启用 PQC 选项外，还必须实施严格的策略覆盖，以防御强制降低安全等级的降级攻击。此外，内部源站服务器的库也应根据标准进行更新。"
- q: "“使用 Cloudflare 支持的量子抗性密码会让公司服务器变慢吗？”"
  a: "由于 PQC 的密钥数据较大，在连接初始阶段可能会出现微小延迟。但这主要影响连接建立时间，而非实际数据传输速度，在现代硬件环境下，用户通常难以察觉。"
- q: "“现在还没有量子计算机，现在就更换 PQC 基础设施是否浪费预算？”"
  a: "由于存在“先收获，后解密 (HNDL)”攻击，现在传输的数据在未来也可能面临威胁。NIST 建议在 2035 年前完成全面转型，从预防安全事故的成本角度来看，分阶段的基础设施转型被视为必要的投资。"
---

<div class="bluf"><strong>[BLUF]</strong>
Cloudflare 目前的 PQC 支持侧重于通过“密钥协商（<a href="/cn/glossary/ml-kem" class="glossary-tooltip" data-definition="一种利用基于格的密码学设计的下一代密钥封装方式，旨在确保即使面对量子计算机的攻击也能安全地交换私钥。">ML-KEM</a>）”来防御未来的解密攻击 (HNDL)，但由于“数字签名 (ML-DSA)”标准化的滞后，在防御实时中间人攻击 (MITM) 方面仍有局限。为了实现真正的端到端安全，必须对 WARP 隧道之后的“源站服务器”区间进行 PQC 升级，这需要进行超越简单客户端更新的基础设施转型。</div>

量子计算机将摧毁现代加密体系的“Q-Day”预警已不再停留于科幻领域。全球安全巨头 Cloudflare 在 WARP 客户端中全面引入 <a href="/cn/glossary/post-quantum-cryptography" class="glossary-tooltip" data-definition="一种即使利用量子计算机的计算能力也无法破解的下一代加密算法体系">Post-Quantum Cryptography</a> 是一个令人振奋的信号，但深入审视其技术细节，我们会发现自己仍只是拿着一面“半截盾牌”。在本分析中，我们将从安全架构师的角度，冷静地探讨 Cloudflare 的 PQC 宣言所具有的实际价值及其背后隐藏的致命空白。

## 1. 为什么目前的 PQC 支持仅侧重于“HNDL”攻击

### 密钥协商 (ML-KEM) 的引入与数字签名 (ML-DSA) 缺失之间的差距

Cloudflare 率先引入的 ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism) 是一种用于安全生成和共享加密数据所需私钥的技术。它是防御 <a href="/cn/glossary/harvest-now-decrypt-later" class="glossary-tooltip" data-definition="一种攻击方式，即先收集现在的加密流量并存储，待未来开发出强大的量子计算机后再进行解密。">Harvest-now-decrypt-later</a>（先收获，后解密）攻击的极佳手段。然而，加密通信的另一支柱——“数字签名”领域仍依赖于传统的 RSA 或椭圆曲线密码 (ECC)，这意味着在证明服务器合法性的阶段，依然暴露在量子威胁之下。

### 依然暴露在主动攻击 (MITM) 下的现有 PQC 隧道结构

缺少数字签名的 PQC 隧道，就好比虽然把保险箱的锁换成了最先进的，但保险箱主人的身份证件却依然是容易伪造的纸片。在攻击者实时介入并出示假证书的中间人攻击 (MITM) 环境下，仅靠 ML-KEM 构建的安全隧道极易失效。在 NIST 的 FIPS 204 标准（即 ML-DSA）完全融合进整个基础设施之前，目前的 PQC 只能作为一种防御被动监听的有限防御体系。

![Post-Quantum Cryptography - 这是一个具有玻璃质感的数字保险箱，中心是象征加密技术的发光电路，边缘有微小的裂缝，代表数字签名的缺失。](../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp)

## 2. 端到端 (End-to-End) 量子安全的巨大空白：源站服务器的局限性

### WARP 客户端无法解决的“最后一公里”安全风险

即便用户通过 WARP 安全地连接到了 Cloudflare 边缘 (Edge) 服务器，从边缘服务器到存储实际数据的源站服务器之间的区间仍然是个问题。如果该区间依然使用古典密码体系，整个安全链条最终会在最薄弱的环节断裂。安全架构中所谓的这“最后一公里”的缺失，是企业不应将 Cloudflare 的 PQC 支持误认为整个基础设施已经安全的内核原因。

### 自动 SSL/TLS 升级的技术壁垒与标准化问题

尽管 Cloudflare 正努力通过 Automatic SSL/TLS 功能升级与源站服务器的连接，但却面临着硬件兼容性和性能下降的巨大障碍。由于 ML-KEM 的密钥尺寸远大于古典密码，可能会导致网络数据包分片或握手延迟。在未能解决这些技术债务的情况下，仅通过营销辞令强调 PQC，与其说是实质性的安全强化，倒不如说更接近于提升品牌形象。

![数据桥的抽象可视化，由半透明玻璃块组成，前半部分闪烁着量子能量，后半部分崩塌成线框，象征边缘服务器与源站服务器之间断裂的安全链，柔和的蓝色和橙色演播室灯光](../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp)

## 3. 与安卓 17 基于硬件的 PQC 策略对比分析

### OS 级别的信任链 (Chain of Trust) 构建与网络层安全的差异

与作为 Cloud Cloud 服务的 Cloudflare 不同，谷歌的安卓 17 采取了更为根本的方法。通过在硬件级别的安卓验证启动 (AVB) 阶段整合 ML-DSA，展现了从启动时刻起就确保量子抗性的策略。这比仅在网络层覆盖安全的做法提供了更强大的“信任根”，在保障整个操作系统完整性方面产生了决定性的差异。

### 针对企业客户端 (Cloudflare One) 用户的实际应对指南

目前使用 Cloudflare One 的企业安全管理员不应仅仅满足于通过点击一个按钮开启 PQC 设置。应当通过 MDM (Mobile Device Management) 策略强制开启“仅限 PQC (PQC Only)”模式，并实施严格的策略覆盖，防止攻击者尝试强制降低安全等级的降级攻击。此外，还必须同步进行将内部源站服务器的库更新至最新 NIST 标准的工作，才能完成真正的量子抗性架构。

| 安全主体 | 应用算法 | 主要安全层 | NIST 标准合规性及权威 |
| :--- | :--- | :--- | :--- |
| Cloudflare | ML-KEM (密钥协商) | 网络/隧道 (MASQUE) | FIPS 203 (ML-KEM-768 混合模式) |
| Android 17 | ML-DSA (数字签名) | 硬件/内核 (AVB) | FIPS 204 (信任链) |
| Cisco (SKIP) | PSK-DHE / ML-KEM | VPN/IPSec 基础设施 | 基于 IOS-XE 的全球标准化先锋 |
| Google Play | ML-DSA (混合签名) | 应用分发层 | 应用完整性验证及防篡改 |

> "PQC 隧道虽然拦截了‘先收获，后解密’这种静态威胁，但缺少数字签名的现有结构在中间人攻击 (MITM) 这种主动威胁面前，依然只是一面古典的盾牌。"

> "在安卓 17 通过构建基于硬件的信任链来强化根本安全的同时，Cloud Cloud 边缘安全依然面临着与源站服务器标准化差距的技术债务。"

## 结论：迈向 Q-Day 的真正安全自立，基础设施创新是超越营销术语的核心

量子安全并非一个简单的复选框选项，而是意味着整个基础设施的范式转移。Cloudflare 的举措无疑指向了正确的方向，但数字签名的缺失和源站服务器的孤立仍是我们必须解决的课题。只有清晰认识到技术华丽外表下隐藏的脆弱性，并付诸实践分阶段的基础设施升级，我们才能安全地迎接即将到来的量子时代。

* NIST 及行业量子安全应对现状：
  - **超过 45%**：传输至 Cloudflare 的人类生成流量中，已经应用后量子加密的比例。
  - **2030 年**：根据 NIST 指南，正式停止使用 (Deprecated) 112 位及以下古典密码 (RSA, ECC) 算法的时间点。
  - **2035 年**：全面禁止使用 (Disallowed) 古典密码算法，所有联邦安全系统必须完全转向 PQC 的最后期限。
  - **5-15 年**：专家预测的加密有效量子计算机 (CRQC) 出现及现代加密体系崩溃的时间点。

## 🔗 相关阅读
- [Rust 的悖论：创新安全性引发的管理瓶颈与生产力危机](/cn/posts/rust-paradox-safety-productivity)
- [Warp 的开源宣言：Agent 优先时代，开发者的自由还是 AI 的从属？](/cn/posts/warp-open-source-agent-first-era)