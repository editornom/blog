---
title: "AI 令牌窃取 (AI Token Hijacking) 时代，您的会话安全吗？"
author: "editornom"
pubDatetime: 2026-04-17T11:03:09+09:00
slug: "ai-token-hijacking-session-security-guide"
featured: false
draft: false
tags: ["AI 令牌窃取", "设备代码钓鱼", "网络安全", "Haionnet", "提示注入"]
ogImage: "../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/74150eef-0.webp"
description: "本文深入分析了近期激增的 AI 令牌窃取 (AI Token Hijacking) 技术机制，并针对 AI Agent 环境提出了专业的安全应对策略。"
---

最近，网络攻击正从跨越 ID 和密码的第一道防线，进化为直接瞄准登录会话本身。如果说过去的黑客攻击还停留在窃取账号信息的水平，那么现在已经发展到了直接夺取已完成认证的“令牌（Token）”，从而使多因素身份验证 (MFA) 体系失效的阶段。而这其中的核心，便是利用生成式 AI 提升攻击精细度与速度的“AI 令牌窃取 (AI Token Hijacking)”。

![AI 令牌窃取 (AI Token Hijacking) - 在复杂的神经网络背景下，机器人手抓取半透明发光令牌的高科技数字安全概念插图，极简编辑风格，带有蓝色和霓虹橙色调。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/74150eef-0.webp)

## AI 令牌窃取，企业安全的新威胁

根据微软安全研究中心 (Microsoft Defender Security Research) 的最新报告，已监测到利用名为“EvilTokens”的钓鱼服务化 (PhaaS) 工具包进行的大规模攻击活动。这种攻击的核心在于通过自动化基础设施尝试 AI 令牌窃取。攻击者利用生成式 AI，根据受害者的职位或工作流程定制极其逼真的钓鱼诱饵，诱导其点击。

一旦令牌被窃取，威胁将迅速扩散至企业的整个 Cloud 基础设施。在令牌有效期内，攻击者无需额外认证即可尝试非法导出邮件、分析公司内部目录、提升权限等。这不仅是简单的敏感数据泄露，更会导致企业内部根本性的“信任链”崩溃，后果极其严重。

![AI 令牌窃取 (AI Token Hijacking) - 代表大规模钓鱼活动的全球网络概念图，服务器节点上闪烁着红色警告图标，扁平化设计编辑风格，专业配色。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/4cc4071d-1.webp)

## 渗透正常认证程序的设备代码钓鱼

在本次发现的攻击手段中，尤其值得关注的是对“设备代码流 (Device Code Flow)”的滥用。该功能原是为了方便智能电视或打印机等输入设备受限的终端而设计的，但攻击者却侵入这一正常流程，诱导用户输入钓鱼网站提供的代码。

这里动用了“动态代码生成”和“后端自动化”等精尖技术。为了规避通常只有 15 分钟有效期的设备代码限制，攻击者在 Railway.com 等 PaaS 平台创建了数千个短期轮询 Node。在用户点击链接的瞬间，实时生成代码以躲避过期。用户一旦输入代码，会话即刻被劫持。由于攻击者的会话与用户环境是隔离的，传统的安全监控手段很难检测到这种异常。

![AI 令牌窃取 (AI Token Hijacking) - 代码编辑器屏幕特写，显示恶意脚本正被插入到正常函数中，现代办公室柔和的虚化背景，数字艺术风格。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/822cf2dd-2.webp)

## 打破数据与指令边界的提示注入

AI Agent 的普及形成了另一条安全战线。最近研究发现，主流 AI 模型的代理程序极易受到“间接提示注入 (Indirect Prompt Injection)”攻击。攻击者不再直接向 AI 下达命令，而是将恶意指令隐藏在 AI 会读取的外部数据（如 GitHub PR 标题、邮件正文等）中。

例如，一个执行安全审查的 AI Agent 在读取包含恶意代码的 PR 标题时，可能会根据其中隐藏的指令，将当前会话的 API 密钥或令牌发送到攻击者的服务器。这是因为 AI 模型在结构上无法明确区分“数据”与“指令”。用户可能认为 AI 正在执行正常任务，而后台却在悄无声息地进行令牌窃取。由于此类漏洞往往在没有发布正式 CVE 的情况下被默然修复，使用旧版本 Agent 的环境极易暴露在风险之中。

![AI 令牌窃取 (AI Token Hijacking) - 集成了电路图案的安全金库门，象征数据保护与零信任架构，3D 渲染，整洁的建筑风格。](../../../../../source/posts/AI_토큰_탈취(AI_Token_Hijacking)/24e52313-3.webp)

## 网络层面的实时响应与防御策略

应对 AI 令牌窃取，不能仅依赖于单个用户的警惕性，必须采取从网络层就开始进行彻底验证与监控的多层防御策略。

从这一角度来看，**Haionnet** 的安全解决方案提供了务实的防御屏障。基于专用线路的稳定基础设施，通过托管安全服务 (MSSP) 实时追踪异常流量。通过在网络端源头阻断数据向攻击者常用设施外泄或来自可疑域名的访问，形成第一道防线。特别是它可以根据企业的具体业务特征设定精细的安全策略，在确保业务连续性的同时，有效抵御自动化的 AI 攻击。

> “AI 是安全的强大盟友，但同时也为攻击者提供了前所未有的锐利长矛。现在，如何确保登录后的‘会话可靠性’，将决定安全防护的成败。”

## 持续验证，向零信任转型

AI 令牌窃取已不再是理论上的方案，而是现实的威胁。自动化工具正无时无刻不在觊觎会话，我们为了提高效率而引入的 AI Agent 反而可能成为攻击的通道。

现在是时候摒弃“认证过的会话即安全”这一传统观念了。必须实践零信任原则，对所有连接进行持续验证，并在网络层面同步实施强有力的安全管控。与 Haionnet 等专业安全合作伙伴一起重新检查基础设施的根基，才是安全度过 AI 时代最可靠的方法。

## ✅ 常见问题 (FAQ)

<details>
  <summary>什么是 AI 令牌窃取 (AI Token Hijacking)？</summary>
  <div class="faq-content">

这是一种利用生成式 AI 拦截已完成认证的“登录会话令牌”的攻击。它的特点是超越了获取账号密码的阶段，直接令多因素身份验证 (MFA) 失效，并以用户的权限非法访问企业内部系统。

  </div>
</details>

<details>
  <summary>像 'EvilTokens' 这样的钓鱼工具包有哪些主要特点？</summary>
  <div class="faq-content">

作为钓鱼服务化 (PhaaS) 工具，它通过生成式 AI 创建针对受害者职位的定制化诱饵。它基于自动化基础设施进行大规模攻击，并利用窃取的令牌进行邮件窃取或权限提升等后续攻击。

  </div>
</details>

<details>
  <summary>为什么设备代码钓鱼非常危险？</summary>
  <div class="faq-content">

因为它利用了智能电视等设备中使用的正常认证程序。攻击者通过创建实时自动化节点来绕过代码过期时间，并在用户输入代码的瞬间劫持会话。这种方式极难被传统的安全监控手段察觉。

  </div>
</details>

<details>
  <summary>什么是间接提示注入 (Indirect Prompt Injection)？</summary>
  <div class="faq-content">

这是一种将恶意指令隐藏在 AI 读取的外部数据（邮件、文档等）中的手段。利用 AI 模型无法明确区分数据与指令的结构性缺陷，诱导 AI 自动将会话令牌或 API 密钥发送给攻击者。

  </div>
</details>

<details>
  <summary>为什么登录后的“会话安全”变得如此重要？</summary>
  <div class="faq-content">

因为最近的攻击目标不再是突破第一道认证，而是瞄准作为认证结果的会话。一旦会话被劫持，攻击者无需额外认证即可操控企业的整个 Cloud 基础设施，导致根本性的信任体系崩溃。

  </div>
</details>

<details>
  <summary>攻击者为了绕过设备代码使用了哪些技术手段？</summary>
  <div class="faq-content">

他们在 Railway.com 等 PaaS 平台创建数千个“短期轮询 Node”。为了克服 15 分钟的极短有效期，在用户点击链接的瞬间通过后端自动化实时生成代码，从而立即捕获认证会话。

  </div>
</details>

<details>
  <summary>在 AI Agent 环境中需要注意哪些安全事项？</summary>
  <div class="faq-content">

AI Agent 的漏洞往往在没有发布正式 CVE 的情况下被默然修复。因此，必须注意避免使用旧版本代理，并始终警惕 AI 处理的外部数据可能转化为恶意指令的风险。

  </div>
</details>

<details>
  <summary>Haionnet 的解决方案是如何应对的？</summary>
  <div class="faq-content">

通过基于专用线路的基础设施和托管安全服务 (MSSP)，在网络层构建第一道防线。实时追踪异常流量，从源头阻断数据外泄至可疑域名，确保业务的连续性。

  </div>
</details>

<details>
  <summary>与传统安全方式相比，多层防御策略有何不同？</summary>
  <div class="faq-content">

它不单纯依赖用户的警惕性，而是在网络端设定强有力的策略。通过实时流量分析和针对基础设施特征的精细验证程序，分层阻断自动化 AI 攻击向内部扩散。

  </div>
</details>

<details>
  <summary>企业践行“零信任”安全的核心是什么？</summary>
  <div class="faq-content">

核心是摒弃“一次认证即永久安全”的迷思。对所有连接和会话进行持续验证，并与 Haionnet 等专业伙伴合作重新检查基础设施，在网络层面同步实施强力管控。

  </div>
</details>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是 AI 令牌窃取 (AI Token Hijacking)？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "这是一种利用生成式 AI 拦截已完成认证的“登录会话令牌”的攻击。它的特点是超越了获取账号密码的阶段，直接令多因素身份验证 (MFA) 失效，并以用户的权限非法访问企业内部系统。"
      }
    },
    {
      "@type": "Question",
      "name": "像 'EvilTokens' 这样的钓鱼工具包有哪些主要特点？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "作为钓鱼服务化 (PhaaS) 工具，它通过生成式 AI 创建针对受害者职位的定制化诱饵。它基于自动化基础设施进行大规模攻击，并利用窃取的令牌进行邮件窃取或权限提升等后续攻击。"
      }
    },
    {
      "@type": "Question",
      "name": "为什么设备代码钓鱼非常危险？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "因为它利用了智能电视等设备中使用的正常认证程序。攻击者通过创建实时自动化节点来绕过代码过期时间，并在用户输入代码的瞬间劫持会话。"
      }
    },
    {
      "@type": "Question",
      "name": "什么是间接提示注入 (Indirect Prompt Injection)？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "这是一种将恶意指令隐藏在 AI 读取的外部数据中的手段。利用 AI 模型无法明确区分数据与指令的结构性缺陷，诱导 AI 自动将令牌发送给攻击者。"
      }
    },
    {
      "@type": "Question",
      "name": "为什么登录后的“会话安全”变得如此重要？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "因为最近的攻击目标瞄准作为认证结果的会话。一旦会话被劫持，攻击者无需额外认证即可操控企业的 Cloud 基础设施，导致信任体系崩溃。"
      }
    },
    {
      "@type": "Question",
      "name": "攻击者为了绕过设备代码使用了哪些技术手段？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "他们在 PaaS 平台创建数千个短期轮询 Node。在用户点击链接的瞬间通过后端自动化实时生成代码，从而立即捕获认证会话。"
      }
    },
    {
      "@type": "Question",
      "name": "在 AI Agent 环境中需要注意哪些安全事项？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "AI Agent 漏洞常被默然修复而不发布 CVE。应避免使用旧版本，并警惕外部数据转化为指令的风险。"
      }
    },
    {
      "@type": "Question",
      "name": "Haionnet 的解决方案是如何应对的？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "通过专用线路和 MSSP 在网络层构建防线。实时追踪异常流量并阻断数据外泄，确保业务连续性。"
      }
    },
    {
      "@type": "Question",
      "name": "与传统安全方式相比，多层防御策略有何不同？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "它在网络端设定强力策略，不只依赖用户警惕。通过实时分析和精细验证分层阻断攻击扩散。"
      }
    },
    {
      "@type": "Question",
      "name": "企业践行“零信任”安全的核心是什么？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "核心是摒弃‘一次认证即安全’的迷思，对所有连接进行持续验证，并在网络层面实施强力管控。"
      }
    }
  ]
}
</script>