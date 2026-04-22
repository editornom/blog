---
title: "隐形后门：OAuth 令牌引发的 SaaS 供应链陷阱"
author: editornom
pubDatetime: 2026-04-22 09:08:13+09:00
slug: saas-supply-chain-oauth-token-security
featured: false
draft: false
ogImage: "../../../../../source/posts/OAuth_Supply_Chain_Security/img1.webp"
description: "通过 Salesloft 和 Gainsight 因信任的第三方集成应用 OAuth 令牌被盗导致数百家企业数据泄露的案例，分析现代 SaaS 供应链安全漏洞及应对策略。"
faqs:
- q: 什么是 OAuth，为什么要使用它？
  a: 这是一种无需共享密码即可授予第三方应用特定数据访问权限的协议。正如'使用 Google 登录'一样，它被广泛用于实现应用间安全便捷的数据联动，但一旦被窃取，则面临代理权限被滥用的风险。
- q: 基于 OAuth 的供应链攻击有何特点？
  a: 攻击者并非直接攻击防御严密的骨干系统，而是先攻破相对脆弱的关联应用。利用获取的权限恶意利用信任关系，从而绕过安全网深度渗透到内部数据中。
- q: Salesloft 和 Gainsight 事故的核心原因是什么？
  a: 原因是攻击者黑进了第三方应用 Drift，大量窃取了用户的 OAuth '刷新令牌(Refresh Token)'。通过这些令牌，攻击者无需 MFA 认证即可长期持续访问 Salesforce 等关联系统。
- q: 为什么刷新令牌(Refresh Token)在安全上更危险？
  a: 与普通访问令牌不同，刷新令牌的有效期通常非常长。在用户明确撤销权限之前它一直有效，因此攻击者一旦得手，就成了绕过多因素身份验证(MFA)并持续窃取数据的通道。
- q: 过度的'权限范围(Scope)'设置会引发什么问题？
  a: 当应用拥有的权限超过其执行功能所需时，就会发生此问题。例如，如果一个简单的聊天机器人拥有 CRM 的完整读取权限，一旦令牌被盗，攻击者就能提取所有联动系统的数据，导致'爆炸半径'扩大到整个企业。
- q: 为什么传统安全监控难以发现此类攻击？
  a: 因为攻击者的数据请求是以'已获授权的信任应用'的名义进行的。在日志中，这看起来就像是正常的服务同步工作，因此极难将恶意活动与常规 API 使用模式区分开来。
- q: 引入代理型 AI (Agentic AI) 如何增加 OAuth 安全威胁？
  a: AI 代理为了进行自主判断，通常被赋予比传统应用更广泛的权限。如果 AI 的令牌被盗，攻击者不仅能窃取数据，还能利用其自主权进行发送邮件、批准付款、更改基础设施配置等破坏性活动。
- q: 从'零信任'角度出发，防止 OAuth 供应链攻击的核心是什么？
  a: 不再想当然地信任第三方应用，而是将其提升到与内部账号同等严苛的管理水平。必须摒弃'一次设置，终身免检'的观念，对所有联动权限进行持续验证并纳入治理体系。
- q: 企业目前可以采取哪些技术应对措施？
  a: 首先应使用 SSPM 解决方案等对组织内的 OAuth 联动现状进行全面调查。随后根据'最小权限原则'封锁不必要或权限过大的应用，并定期清理闲置的刷新令牌。
- q: 为了监测异常迹象，需要建立什么样的监控体系？
  a: 不能仅查看是否登录，还必须分析应用的 API 调用模式。一旦监测到特定应用获取的数据量超过平时等异常模式，必须建立能立即自动作废相关令牌的响应系统。
references:
- https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html
- https://www.obsidiansecurity.com/blog/a-guide-to-saas-supply-chain-solutions
- https://cloudsecurityalliance.org/blog/2025/09/25/the-salesloft-drift-oauth-supply-chain-attack-cross-industry-lessons-in-third-party-access-visibility
- https://www.zscaler.com/blogs/product-insights/gainsight-supply-chain-attack-what-it-means-saas-security
- https://appomni.com/learn/saas-security-fundamentals/oauth-token-security-risks/
- https://unit42.paloaltonetworks.com/third-party-supply-chain-token-management/
- https://www.obsidiansecurity.com/blog/what-are-oauth-tokens-vulnerabilities
- https://www.valencesecurity.com/resources/blogs/salesforce-oauth-token-breach-what-every-security-team-must-know
- https://redcanary.com/blog/threat-detection/google-workspace-oauth-attack/
- https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
author_role: Senior Tech Editor
modDatetime: '2026-04-22T13:22:20.777134+09:00'
---

现代企业的安全边界早已不再局限于机房的防火墙。如今的入侵事件并非发生在系统外部，而是发生在我们信任并允许的“连接”缝隙中。2025 年震动 Salesloft 和 Gainsight 的供应链安全事故，正是证明这种致命信任被背叛的典型案例。

## 以信任为名的万能钥匙：OAuth

“使用 Google 登录”或“CRM 联动”已成为现代业务的必备语言。OAuth (Open Authorization) 协议允许在不直接共享密码的情况下授予特定数据的访问权限，这极大地提高了协作效率，但同时也产生了一个脱离管理员控制的“代理权限”盲区。

2025 年 8 月发生的 Salesloft-Drift 安全事故精准地利用了这一结构性漏洞。攻击者并未正面硬闯防御严密的 Salesforce，而是将防御体系相对松懈的第三方应用 Drift 作为迂回路径。他们通过大量窃取用户授予 Drift 的 OAuth “刷新令牌 (Refresh Token)”，成功瓦解了巨大的数据堡垒。

![OAuth 供应链安全 - 数字网络中的信任崩塌，闪耀的钥匙化作阴影。](../../../../../source/posts/OAuth_Supply_Chain_Security/img1.webp)

## 永恒的权限与无法控制的爆炸半径

此次事故暴露的技术盲点在于令牌的有效期和权限范围。通常使用的访问令牌有效期较短，但刷新令牌往往在用户明确撤销权限之前长期有效。攻击者通过获取这些令牌，轻而易举地绕过了多因素身份验证 (MFA)，获得了可以长期驻留在目标企业内部数据的通行证。

如果再加上“权限范围蔓延 (Scope Creep)”，问题将变得一发不可收拾。许多第三方应用以运行顺畅为由，要求超出其职能所需的广泛权限。当一个简单的聊天机器人服务拥有“读取/写入全部 CRM 数据”的权限时，一旦该应用被攻破，随即就会导致整个企业的数据大逃亡。这就是所谓的“爆炸半径 (Blast Radius)”扩散至整个企业。

> “对第三方的信任不再理所应当。它们必须像内部特权账号一样，受到严格的持续验证和治理管理。”

## 隐藏在正常流量背后的入侵者

在 Salesloft 和 Gainsight 案例中，安全团队感到最棘手的是难以立即感知入侵事实。这是因为攻击者的数据请求是以“已获授权、可信应用”的名义执行的。在安全日志中，这看起来就像 Drift 应用在照常同步数据，属于正常操作，极难辨别其背后的操纵者。

特别是，攻击者使用了诸如 `Salesforce-Multi-Org-Fetcher/1.0` 之类的特定 User-Agent 字符串，以自动化的方式提取多个组织的数据。虽然这是一种与普通使用模式截然不同的、以 API 为中心的攻击形式，但由于它躲在已经建立的信任关系幕后，因此落入了监测盲区。

![OAuth 供应链安全 - 复杂的齿轮系统中，一个金色小齿轮的损坏导致整体结构扭曲。](../../../../../source/posts/OAuth_Supply_Chain_Security/img2.webp)

## 代理型 AI：更广泛、更自主的威胁涌现

预计这种基于 OAuth 的供应链攻击未来将变得更加精细。特别是随着能够自主判断和行动的“代理型 AI (Agentic AI)”集成到企业系统中，风险因素必然会随之增加。AI 代理被授予的 OAuth 令牌可能比现有的简单应用联动具有更广泛、更强大的权限。

如果 AI 代理使用的令牌被窃取，攻击者将不仅仅停留在窃取数据的层面，还可能借用 AI 的权限发送邮件、批准付款，甚至更改基础设施配置，开展自主破坏活动。现在，我们必须开始思考从“应用对应用 (App-to-App)”转向“AI 对应用”的安全体系。

## 用零信任重新设计 SaaS 治理

必须彻底摒弃将 SaaS 联动视为“一次设置，终身免检”的传统管理方式。企业应实际考虑的应对方向如下：

- **OAuth 可视化全量调查**：当务之急是掌握组织内用户向哪些应用授予了哪些权限。应利用 SSPM (SaaS Security Posture Management) 解决方案等识别并系统地管理那些被闲置的联动应用。
- **落实最小权限原则 (Least Privilege)**：严格审核第三方应用要求的权限是否与其服务目的相符。对于过度的权限要求，需要建立坚决予以限制的治理机制。
- **基于令牌的行为分析**：超越简单的登录确认，实时监控特定应用是否在获取超过平时的异常数据。必须建立自动化应对体系，在检测到异常模式时立即废除相关令牌。

![OAuth 供应链安全 - 穿透数字迷雾、照亮巨大网络架构的未来派灯塔光芒。](../../../../../source/posts/OAuth_Supply_Chain_Security/img3.webp)

SaaS 生态系统的紧密连接虽然提高了业务生产力，但同时也成为了最脆弱的攻击路径。如果外部合作伙伴发生安全事故会导致我们的系统也毫无防备地暴露，那么这种连接就绝非安全。

将第三方集成环境提升到与内部员工账号同等严苛的管理水平，是当今安全领导者必须具备的新标准。请务必重新检查，您组织中的那些“代理权限”目前正在何处以及如何被使用。