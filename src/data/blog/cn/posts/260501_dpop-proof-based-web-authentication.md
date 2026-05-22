---
title: "从持有者模型到基于证明的安全：DPoP 如何重新定义 Web 认证的信任模型"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-01 16:47:12.606269+09:00
slug: dpop-proof-based-web-authentication
featured: false
draft: false
ogImage: "../../../../../source/posts/DPoP_(RFC_9449)/29edb26c-0.webp"
description: "了解 RFC 9449 DPoP 技术的概念与工作原理，该技术旨在弥补传统 Bearer 令牌的安全漏洞，并介绍了在应用层证明令牌所有权的方法。通过加密签名保护系统免受令牌窃取威胁，并提出实现更强健的 OAuth 2.0 安全架构的方案。"
references:
- https://auth0.com/blog/protect-your-access-tokens-with-dpop/
- https://www.authgear.com/post/demonstrating-proof-of-possession-dpop
- https://github.com/istio/istio/issues/59439
modDatetime: 2026-05-01 16:57:12.606269+09:00
---

作为 OAuth 2.0 协议的标准，Bearer 令牌方式是现代 Web 安全架构中应用最广泛的机制。然而，这种方式将令牌持有者视为合法授权者，具有结构性脆弱性：一旦令牌被窃取，系统资源就会在没有任何额外验证程序的情况下暴露。如果令牌通过网络截获或日志文件泄露，攻击者可以立即伪装成合法用户。为了填补这一安全空白，RFC 9449 标准化的 DPoP (Demonstrating Proof-of-Possession) 技术应运而生。

DPoP 采用在应用层直接证明令牌所有权的方式。它不仅要求出示令牌这一“入场券”，还强制要求在每次请求时提交证明自己是该入场券合法获取者的加密签名。该机制基于客户端生成的非对称密钥对，从数学上证明客户端在请求和使用令牌时确实持有私钥。

![DPoP (RFC 9449) - 客户端生成密钥并在认证服务器注册，仅持有该密钥的用户可使用安全令牌的技术架构图。](../../../../../source/posts/DPoP_(RFC_9449)/29edb26c-0.webp)

## 在应用层实现强大的所有权绑定

过去，曾尝试通过 mTLS (Mutual TLS) 等硬件及传输层绑定技术来增强安全性。然而，由于复杂的证书管理体系以及在浏览器环境中的实现限制，mTLS 在通用 Web 应用程序中的应用门槛较高。相比之下，DPoP 将这一过程提升到应用层，从而确保其能够在 Web 浏览器或移动应用环境中灵活运行。

从工作原理来看，客户端首先生成自己的公钥和私钥对。随后，在向认证服务器请求令牌时，会发送一个由其私钥签名的短寿命 JWT，即“DPoP Proof”。认证服务器从该证明中提取公钥，并在颁发的 Access Token 和 Refresh Token 中将该密钥的指纹 (Thumbprint) 作为 `cnf` (Confirmation) 声明插入。通过这一过程，令牌与特定的密钥对在密码学上实现了绑定。

该机制的核心在于每次请求生成的证明中包含的 `htu` (目标 URI)、`htm` (HTTP 方法) 和 `jti` (唯一标识符) 值。这些信息可以防止为特定请求生成的证明被重复用于其他 API 调用。即使攻击者同时获取了特定时刻的令牌和证明，也无法利用它们调用其他路径的 API，或在一段时间后重新使用。

## 实务视角的性能影响与实现考量

在考虑引入 DPoP 时，首要评估的因素是额外的运算成本。虽然前端和后端都增加了非对称密钥签名和验证逻辑，但现代设备的硬件性能足以在毫秒 (ms) 级别处理这些运算。网络开销也仅相当于增加了一行 HTTP 标头，而服务器端的 JTI 缓存成本由于其短生命周期的特性，对基础设施造成的负担并不大。

但在实现阶段，需要进行一些精细化处理。必须构建排除查询字符串的准确 `htu` 路径，并且为了防止因客户端与服务器之间的系统时钟不一致而导致 `iat` (签发时间) 验证错误，需要精密的同步策略。特别是在 SPA (Single Page Application) 环境中，如何安全地在浏览器内保存私钥，仍然是设计上的核心挑战。

- <b>安全模型</b>：如果说传统的 Bearer 方式是基于简单的持有者模型，那么 DPoP 则旨在建立基于签发者证明的强健模型。
- <b>窃取应对</b>：即使令牌泄露，如果没有私钥也无法重新使用，从而防止连锁安全侵害。
- <b>实现复杂度</b>：由于需要实现密钥管理和签名逻辑，复杂度处于中等水平。
- <b>主要目标</b>：适用于对信任水平要求较高的金融、医疗保健和企业级安全环境。

![DPoP (RFC 9449) - 普通令牌 (Bearer) 与增强型 DPoP 令牌在安全认证要素及防重放技术方面的对比图表。](../../../../../source/posts/DPoP_(RFC_9449)/b04236db-1.webp)

## 向云原生生态系统与基础设施扩展

从最近开源服务网格项目 Istio 的技术讨论中，可以感受到市场对 DPoP 的极高关注。运营大规模微服务架构的组织不再倾向于在每个服务中实现复杂的验证逻辑，而是积极要求在 Sidecar (Envoy) 层面执行 DPoP 验证。这是一种通过将安全功能卸载 (Offloading) 到基础设施层来提高开发效率的策略。

同样值得注意的是，全球 IDP (Identity Provider) 供应商正在将 DPoP 支持作为标准规范。特别是对于寿命较长的 Refresh Token，一次窃取可能导致持续的权限滥用，因此通过 DPoP 进行绑定已不再是可选项，而是安全设计的必选项。

虽然 DPoP 有效地抑制了通过令牌窃取进行的非法重用，但在 XSS (Cross-Site Scripting) 等客户端控制权被完全掌控的情况下，它仍有局限性。因为如果私钥本身泄露，安全体系可能会发生连锁崩溃。因此，安全的重心正在从“令牌保护”转向“密钥存储保护”。开发者应利用浏览器的 Web Crypto API 制定不可导出 (Non-extractable) 的密钥管理策略。比技术规范更重要的，是基于实际运营环境中密钥存储隔离水平能达到何种程度的实务判断。

## 🔗 相关阅读

- [Attention 重塑的技术版图与 Transformer 的光与影](/ko/posts/attention-transformers-tech-landscape)
- [MCP：穿透 AI 集成复杂性的标准协议蓝图](/ko/posts/mcp-ai-integration-standard-protocol)