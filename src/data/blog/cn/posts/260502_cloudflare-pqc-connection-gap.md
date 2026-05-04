---
title: "量子安全的第一步：Cloudflare PQC 面临的连接空白"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-02 11:07:45.171268+09:00
slug: cloudflare-pqc-connection-gap
featured: false
draft: false
ogImage: "../../../../../source/posts/PQC_(Post-Quantum_Cryptography)/e863a673-0.webp"
description: "针对量子计算带来的安全威胁，Cloudflare 在 WARP 和 Cloudflare One 中引入了后量子加密 (PQC)，构建了先发制人的保护体系。本文介绍了旨在防御‘先收集后解密’攻击、并提前践行 NIST 安全建议的技术应对方案。"
references:
- https://blog.cloudflare.com/post-quantum-warp/
- https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/
- https://www.keyfactor.com/education-center/what-is-post-quantum-cryptography-and-why-does-it-matter/
modDatetime: 2026-05-02 11:17:45.171268+09:00
faqs:
- q: "什么是后量子加密 (PQC)，为什么需要它？"
  a: "这是一种即使是量子计算机强大的运算能力也难以破解的下一代加密技术。它的引入是为了应对现有 RSA 或 ECC 方式可能被攻破的威胁，确保数据的长期安全性。"
- q: "‘先收集后解密’攻击具体是什么威胁？"
  a: "这是一种攻击方式：攻击者先收集并存储目前无法破解的加密数据，待未来高性能量子计算机问世后，再对其进行大规模解密。这对政府机密或金融数据尤为致命。"
- q: "Cloudflare 引入的 PQC 技术核心算法是什么？"
  a: "核心是使用基于格（Lattice-based）数学模型的 ML-KEM 算法。这是目前 NIST 推荐的标准技术，基于比现有方式复杂得多的数学难题设计而成。"
- q: "在 WARP 客户端使用 PQC 需要单独设置吗？"
  a: "如果您使用的是 Windows 版 WARP（版本 2025.5.893.0 或更高）或最新版本的 iOS 版，该功能将自动启用。无需引入额外硬件或支付额外费用即可享受最新安全技术。"
- q: "混合加密模式意味着什么？"
  a: "这是一种同时使用新的后量子加密 (ML-KEM) 和传统的古典加密 (X25519) 来对数据进行双重保护的方式。它可以作为一种安全机制，应对新算法可能存在的潜在缺陷。"
- q: "Cloudflare 应用 PQC 的区间有什么局限性？"
  a: "目前仅保护客户端与 Cloudflare 网络之间的区间。如果从 Cloudflare 到最终目的地源站服务器的区间仍使用古典加密，则依然存在安全薄弱点。"
- q: "应用 PQC 会导致网络速度变慢吗？"
  a: "根据内部基准测试，使用基于 QUIC 的 MASQUE 协议的 PQC 环境表现出了比传统 TLS 1.2 更高效的运算速度。目前的重点在于高效实现，而非担忧性能下降。"
- q: "降级允许政策对安全有什么影响？"
  a: "在 PQC 连接失败时切换回古典加密可以提高可用性，但也可能成为攻击者强制降低安全等级的‘降级攻击’的通道，因此需要注意。"
- q: "‘只要安装了最新的 WARP，就完全不用担心量子计算机黑客攻击了吗？’"
  a: "这只能算成功了一半。虽然用户和 Cloudflare 之间的通道入口变得坚固了，但只有当数据到达服务器的全路径都支持 PQC 时，才能实现完美防御，因此需要同步改进整体基础设施。"
- q: "‘在公司使用的 Cloudflare One 中应用量子加密会导致服务器成本大幅增加吗？’"
  a: "Cloudflare 提供 PQC 环境无需额外付费，因此不会导致云成本直接上升。不过，工程师可能需要投入运营精力来重新设计基础设施，以确保全路径的安全等级一致。"
---

量子计算可能使现有加密体系失效的担忧正演变为现实的安全威胁。随着美国国家标准与技术研究院 (NIST) 将 RSA 和椭圆曲线加密 (ECC) 的阶段性停用时间定在 2030 年，业界的应对速度也在加快。最近，Cloudflare 在其 WARP 客户端中引入后量子加密 (PQC) 技术，被视为顺应这一趋势的先发制人举措。然而，深入观察其技术实现细节可以发现，这与其说是构建了完美的安全性，不如说是通过大转型期时的一种过渡性应对。

## 针对“先收集后解密”场景的预防性防御

目前安全界最警惕的是“先收集，后解密”（Harvest Now, Decrypt Later）策略。攻击者预先获取加密数据并存储，等到未来性能强大的量子计算机出现时再进行大规模解密。像金融记录或政府机密这样需要长期保密的数据，已经处于潜在的泄露风险之中。

根据 Cloudflare 的数据，目前进入其网络的普通流量中，已有超过 45% 受到后量子加密的保护。这一进度领先于 NIST 建议的时间表，其意义在于无需用户承担额外的硬件成本或费用即可提供 PQC 环境。特别是将该技术同时应用于消费者版 WARP (1.1.1.1) 和企业版 Cloudflare One 代理，精准瞄准了端点安全的重要性。

![PQC (Post-Quantum Cryptography) - 远程办公者的笔记本电脑与公司服务器通过安全技术（PQC、MASQUE）安全连接的架构图。](../../../../../source/posts/PQC_%28Post-Quantum_Cryptography%29/e863a673-0.webp)

## MASQUE 协议与 ML-KEM 的技术结合

此次 PQC 实现的核心是基于 <a href="/ko/glossary/what-is-quic" class="glossary-tooltip" data-definition="一种基于 UDP 的传输协议，旨在减少互联网通信延迟并强化安全性，提升了现代 Web 连接的速度和效率。">QUIC</a> 协议的 MASQUE (Multiplexed Application Substrate over QUIC Encryption) 隧道技术。其中使用了基于格数学模型的 ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism) 算法。值得注意的是，目前的 PQC 应用方式是与传统的古典加密 X25519 结合的“混合模式”。这是一种策略，旨在通过并行运行现有加密体系作为安全保障，以应对新算法可能存在的潜在缺陷。

内部基准测试结果显示，在 TLS 1.3 环境下应用混合模式 ML-KEM-768 时的性能，甚至比基于 TLS 1.2 的加密具有更高效的运算速度。这种加密序列可立即在 Windows 版 WARP 桌面端（版本 2025.5.893.0 或更高）及 iOS（版本 1.11 或更高）的最新客户端环境中运行。

| 类别 | 传统公钥加密 (Classical) | 后量子加密 (PQC) |
| :--- | :--- | :--- |
| 主要算法 | RSA, ECC (ECDH, ECDSA) | ML-KEM (Kyber), ML-DSA (Dilithium) |
| 数学基础 | 整数分解, 离散对数问题 | 基于格 (Lattice-based) 的数学 |
| 量子威胁应对 | 可被 Shor 算法破解 | 对目前已知的量子算法具有抗性 |
| 主要用途 | 密钥交换, 数字签名 | 密钥封装 (KEM), 数字签名 |
| 性能影响 | 运算负载相对较小 | 密钥和签名尺寸增加导致负载产生 |

## 源站服务器的空白与区间安全的局限性

然而，尽管构建了这些防线，结构性的局限性依然存在。Cloudflare 提供的 PQC 保护区间仅限于客户端与 Cloudflare 网络之间。要实现真正意义上的端到端 (End-to-End) 加密，最终目的地的源站服务器也必须支持后量子加密，但绝大多数企业和公共 Web 服务器仍停留在传统体系中。

即使 WARP 客户端通过后量子隧道发送数据，如果数据在通过 Cloudflare 边缘服务器前往源站服务器的最后一段区间被转换为古典加密，安全上的不确定性将再次增加。这相当于隧道的入口是坚固的堡垒，而出口却处于脆弱状态。此外，认证体系的核心 ML-DSA 仍处于标准化过程中，在建立完全的信任体系之前，技术空白不可避免。

[图像：一个真实的 3D 信息图，展示了一个带有透明部分的加密隧道，揭示了内部数据流。一端散发着先进的蓝光 (PQC)，另一端逐渐褪色为暗橙色 (Legacy)，强调了安全缺口。]

## 降级诱导与运营挑战

为了保证兼容性而制定的“允许降级”政策也是安全角度需要审视的地方。Cloudflare 将 2026 年夏天之前设为第一阶段转型期，允许在 PQC 协商失败时将连接降级为古典加密。虽然这是为了保障服务可用性的权宜之计，但也可能成为攻击者故意干扰通信环境、强制降低安全等级的“降级攻击”通道。

虽然存在通过 MDM（移动设备管理）强制开启 PQC 专用模式的选项，但这仅限于具备专业管理能力的后勤环境。对于普通用户或小型组织来说，这种设置本身就可能成为运营负担。谷歌在 Android 17 中集成基于 ML-DSA 的数字签名，并设定 2029 年完成全面转换的目标，也是因为意识到仅靠个别企业的零散应对难以从根本上阻断量子威胁。

引入 PQC 不仅仅是更换加密算法，更是一项需要重新设计整个企业基础设施的复合型任务。与其满足于强化隧道入口的安全，不如同步努力提升包括源站服务器在内的全路径安全水平。最终，真正的后量子安全只有在所有网络节点共享相同的安全标准，并彻底消除因向后兼容而留下的安全死角时，才能最终实现。

## 🔗 相关阅读

- [Attention 重塑的技术版图与 Transformer 的光影](/ko/posts/attention-transformers-tech-landscape)
- [MCP：贯穿 AI 集成复杂性的标准协议蓝图](/ko/posts/mcp-ai-integration-standard-protocol)