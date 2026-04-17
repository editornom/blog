---
title: "AI Token Hijacking 时代：您的会话安全吗？"
author: "Antigravity"
pubDatetime: 2026-04-17T11:03:09+09:00
slug: "ai-token-hijacking-session-security-guide"
featured: false
draft: false
tags: ["AI 令牌劫持", "设备代码钓鱼", "网络安全", "Haionnet", "提示词注入"]
ogImage: "../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/74150eef-0.webp"
description: "分析近期激增的 AI Token Hijacking（AI 令牌劫持）技术机制，并提出在基于代理的 AI 环境下的安全应对策略。"
---

如今的网络攻击已进化到绕过 ID 和密码，直接瞄准登录会话本身。以往的黑客行为仅停留在获取账号信息的层面，而现在则演变为直接窃取已通过认证的“Token（令牌）”，甚至让多因素身份验证（MFA）体系失效。核心正是利用生成式 AI 提高攻击精度和速度的 “AI Token Hijacking（AI 令牌劫持）”。

![AI Token Hijacking - 在复杂的神经背景下，机器人手抓取半透明发光令牌的高科技数字安全概念插图，极简编辑风格，蓝色和霓虹橙色点缀。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/74150eef-0.webp)

## AI Token Hijacking，企业安全的新威胁

根据微软安全实验室（Microsoft Defender Security Research）的最新报告，已监测到利用名为 “EvilTokens” 的网络钓鱼即服务（PhaaS）工具包发起的大规模活动。此类攻击的核心在于通过自动化基础设施尝试 AI Token Hijacking。攻击者利用生成式 AI，根据受害者的职位或工作流程定制钓鱼诱饵，诱导用户点击。

这些被窃取的令牌成为了威胁向企业整个 Cloud 基础设施扩散的跳板。在令牌有效期内，攻击者无需额外认证即可尝试非法导出邮件、分析内部目录、提升权限等。这已不仅是简单的数据泄露，更会导致企业内部根本的“信任链”崩溃。

![AI Token Hijacking - 全球网络概念图，显示大规模钓鱼活动，服务器节点闪烁红色警报图标，扁平化编辑设计风格，专业色调。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/4cc4071d-1.webp)

## 渗透正常认证程序的设备代码钓鱼

在本次发现的攻击手法中，特别值得关注的是对“设备代码认证流（Device Code Flow）”的滥用。该功能初衷是为智能电视或打印机等输入受限的设备提供便利，但攻击者却潜入这一正常流程，诱导用户在钓鱼网站输入代码。

这涉及到“动态代码生成”和“后端自动化”等精尖技术。为了绕过通常只有 15 分钟时效的设备代码，攻击者在 Railway.com 等 PaaS 平台上创建数千个短期轮询 Node。在用户点击链接的瞬间实时生成代码，从而避开过期时间。一旦用户输入代码，会话立即被劫持，且攻击者的会话与用户的环境是分离的，传统安全监控很难发现。

![AI Token Hijacking - 代码编辑器画面的特写，显示恶意脚本被插入正常函数中，现代办公室柔和的焦外成像背景，数字艺术风格。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/822cf2dd-2.webp)

## 模糊数据与命令界限的提示词注入

AI 代理的普及形成了另一条安全战线。近期研究发现，主要 AI 模型的代理极易受到“间接提示词注入（Indirect Prompt Injection）”攻击。攻击者并非直接向 AI 下达命令，而是将恶意指令隐藏在 AI 会读取的外部数据（如 GitHub PR 标题、邮件正文等）中。

例如，一个执行安全审查的 AI 代理在读取包含恶意代码的 PR 标题时，可能会根据隐藏指令将当前会话的 API 密钥或令牌发送到攻击者服务器。这是因为 AI 模型在结构上无法明确区分“数据”与“指令”。用户以为 AI 在执行任务，而背后却在悄悄进行令牌劫持。由于此类漏洞往往在没有正式发布 CVE 的情况下被暗中修复，使用旧版本代理的环境极易暴露在风险中。

![AI Token Hijacking - 集成电路图案的安全保险箱门，象征数据保护与零信任架构，3D 渲染，简洁建筑风格。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/24e52313-3.webp)

## 网络层的实时应对与防御策略

应对 AI Token Hijacking 不能仅依赖个人警觉。必须建立从网络层开始进行彻底验证与监控的多层防御策略。

从这个角度来看，**Haionnet** 的安全解决方案提供了实用的防护屏障。依托基于专线的稳定基础设施，通过托管安全服务（MSSP）实时追踪异常流量。通过在网络端切断向攻击者常用基础设施的数据外泄或来自可疑域名的访问，形成第一道防线。特别是它可以根据企业的基础设施特性设定精细策略，在确保业务连续性的同时，对抗自动化 AI 攻击。

> “AI 是安全的强力盟友，但同时也成为了攻击者手中前所未有的利刃。如今，如何保证登录后的‘会话可靠性’将决定安全防御的成败。”

## 持续验证，向零信任转型

AI Token Hijacking 已不再是理论上的剧本，而是现实的威胁。自动化工具正无时无刻不在窥视着会话，而我们为了提高效率引入的 AI 代理，反而可能成为攻击的通道。

现在是时候摒弃“认证过的会话即安全”这一观念了。必须实践零信任原则，不断验证所有连接，并结合网络层面的强力安全控制。与 Haionnet 等专业安全合作伙伴一起重新检查基础设施，是安全度过 AI 时代最可靠的方法。

## ✅ 常见问题 (FAQ)

<details>
  <summary>什么是 AI Token Hijacking（AI 令牌劫持）？</summary>
  <div class="faq-content">

这是一种利用生成式 AI 窃取已完成认证的“登录会话令牌”的攻击。它超越了获取账号密码的阶段，旨在使多因素身份验证（MFA）失效，并以用户的权限非法访问企业内部系统。

  </div>
</details>

<details>
  <summary>类似 “EvilTokens” 的钓鱼工具包有哪些主要特征？</summary>
  <div class="faq-content">

这是一种网络钓鱼即服务（PhaaS）工具，通过生成式 AI 生成针对受害者职位定制的钓鱼诱饵。它基于自动化基础设施进行大规模攻击，并利用窃取的令牌进行邮件劫持或权限提升等后续攻击。

  </div>
</details>

<details>
  <summary>为什么设备代码钓鱼很危险？</summary>
  <div class="faq-content">

因为它利用了智能电视等设备使用的正常认证程序。攻击者创建实时自动化节点来绕过代码过期时间，在用户输入代码的瞬间劫持会话。传统安全监控极难检测到这种行为。

  </div>
</details>

<details>
  <summary>什么是间接提示词注入（Indirect Prompt Injection）？</summary>
  <div class="faq-content">

这是一种将恶意指令隐藏在 AI 读取的外部数据（邮件、文档等）中的手法。利用 AI 模型无法明确区分数据与指令的结构性缺陷，诱导 AI 自动将会话令牌或 API 密钥发送给攻击者。

  </div>
</details>

<details>
  <summary>为什么登录后的“会话安全”变得如此重要？</summary>
  <div class="faq-content">

因为近期的攻击目标不再是突破第一道认证，而是瞄准认证结果——会话。一旦会话被劫持，攻击者无需额外认证即可掌控企业的整个 Cloud 基础设施，面临信任体系崩溃的巨大风险。

  </div>
</details>

<details>
  <summary>攻击者绕过设备代码的技术方法是什么？</summary>
  <div class="faq-content">

他们在 Railway.com 等 PaaS 平台上创建数千个“短期轮询 Node”。为了克服 15 分钟的极短有效期，在用户点击链接的瞬间通过后端自动化实时生成代码，从而立即钓取认证会话。

  </div>
</details>

<details>
  <summary>在 AI 代理环境下需要注意哪些安全事项？</summary>
  <div class="faq-content">

AI 代理的漏洞往往在没有正式 CVE 的情况下被暗中修复。因此，应注意避免使用旧版本代理，并始终警惕 AI 处理的外部数据可能会转化为恶意指令。

  </div>
</details>

<details>
  <summary>Haionnet 的解决方案如何应对此类威胁？</summary>
  <div class="faq-content">

通过基于专线的基础设施和托管安全服务（MSSP），在网络层构建第一道防线。实时追踪异常流量，从源头切断向可疑域名的数据外泄，确保业务连续性。

  </div>
</details>

<details>
  <summary>与传统安全方式相比，多层防御策略有何不同？</summary>
  <div class="faq-content">

它不单依赖于用户的警觉，而是在网络端设定强有力的策略。结合实时流量分析与针对基础设施特性的精细验证程序，分层拦截自动化 AI 攻击向内部扩散。

  </div>
</details>

<details>
  <summary>企业应实践的“零信任”安全核心是什么？</summary>
  <div class="faq-content">

核心是摒弃“认证过的会话即安全”的盲目信任。不断验证所有连接和会话，并与 Haionnet 等专业合作伙伴一起重新审视基础设施，在网络层面实施强力控制。

  </div>
</details>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是 AI Token Hijacking（AI 令牌劫持）？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "这是一种利用生成式 AI 窃取已完成认证的“登录会话令牌”的攻击。它超越了获取账号密码的阶段，旨在使多因素身份验证（MFA）失效，并以用户的权限非法访问企业内部系统。"
      }
    },
    {
      "@type": "Question",
      "name": "类似 “EvilTokens” 的钓鱼工具包有哪些主要特征？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "这是一种网络钓鱼即服务（PhaaS）工具，通过生成式 AI 生成针对受害者职位定制的钓鱼诱饵。它基于自动化基础设施进行大规模攻击，并利用窃取的令牌进行邮件劫持或权限提升等后续攻击。"
      }
    },
    {
      "@type": "Question",
      "name": "为什么设备代码钓鱼很危险？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "因为它利用了智能电视等设备使用的正常认证程序。攻击者创建实时自动化节点来绕过代码过期时间，在用户输入代码的瞬间劫持会话。传统安全监控极难检测到这种行为。"
      }
    },
    {
      "@type": "Question",
      "name": "什么是间接提示词注入（Indirect Prompt Injection）？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "这是一种将恶意指令隐藏在 AI 读取的外部数据（邮件、文档等）中的手法。利用 AI 模型无法明确区分数据与指令的结构性缺陷，诱导 AI 自动将会话令牌或 API 密钥发送给攻击者。"
      }
    },
    {
      "@type": "Question",
      "name": "为什么登录后的‘会话安全’变得如此重要？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "因为近期的攻击目标不再是突破第一道认证，而是瞄准认证结果——会话。一旦会话被劫持，攻击者无需额外认证即可掌控企业的整个 Cloud 基础设施，面临信任体系崩溃的巨大风险。"
      }
    },
    {
      "@type": "Question",
      "name": "攻击者绕过设备代码的技术方法是什么？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "他们在 Railway.com 等 PaaS 平台上创建数千个‘短期轮询 Node’。为了克服 15 分钟的极短有效期，在用户点击链接的瞬间通过后端自动化实时生成代码，从而立即钓取认证会话。"
      }
    },
    {
      "@type": "Question",
      "name": "在 AI 代理环境下需要注意哪些安全事项？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "AI 代理的漏洞往往在没有正式 CVE 的情况下被暗中修复。因此，应注意避免使用旧版本代理，并始终警惕 AI 处理的外部数据可能会转化为恶意指令。"
      }
    },
    {
      "@type": "Question",
      "name": "Haionnet 的解决方案如何应对此类威胁？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "通过基于专线的基础设施和托管安全服务（MSSP），在网络层构建第一道防线。实时追踪异常流量，从源头切断向可疑域名的数据外泄，确保业务连续性。"
      }
    },
    {
      "@type": "Question",
      "name": "与传统安全方式相比，多层防御策略有何不同？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "它不单依赖于用户的警觉，而是在网络端设定强有力的策略。结合实时流量分析与针对基础设施特性的精细验证程序，分层拦截自动化 AI 攻击向内部扩散。"
      }
    },
    {
      "@type": "Question",
      "name": "企业应实践的‘零信任’安全核心是什么？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "核心是摒弃‘认证过的会话即安全’的盲目信任。不断验证所有连接和会话，并与 Haionnet 等专业合作伙伴一起重新审视基础设施，在网络层面实施强力控制。"
      }
    }
  ]
}
</script>