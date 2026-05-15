---
title: "Kubernetes 1.36：华丽功能背后的'配置过载'与迁移风险深度分析"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-15 11:36:22.330278+09:00
slug: "kubernetes-1-36-configuration-overload-migration-risks"
featured: false
draft: false
ogImage: "../../../../../source/posts/Kubernetes_1.36/81baafaf-0.webp"
description: "Kubernetes v1.36 在为高性能工作负载引入重大创新的同时，也因移除 gitRepo 等遗留功能而带来了迁移风险。了解如何应对 'Haru' 版本的操作复杂性和架构变化，以确保基础设施的稳定性。"
references:
- https://kubernetes.io/blog/2026/04/22/kubernetes-v1-36-release/
- https://kubernetes.io/blog/2026/03/30/kubernetes-v1-36-sneak-peek/
- https://kubernetes.io/releases/1.36/
modDatetime: 2026-05-15 11:46:22.330278+09:00
faqs:
- q: "Kubernetes v1.36 'Haru' 版本核心主题是什么？"
  a: "核心是为高性能 AI/ML 工作负载提供创新资源管理功能，同时移除危险的遗留功能以加强安全性，并考验运营效率。"
- q: "此版本中强调的 DRA (Dynamic Resource Allocation) 是什么功能？"
  a: "这是一种高级资源分配框架，它摆脱了以往对 GPU 等特殊硬件资源的静态分配方式，支持更灵活、更精细的管理。"
- q: "引入工作负载感知调度 (WAS) 的效果是什么？"
  a: "通过将多个 Pod 作为一个逻辑单元进行原子级调度，可以解决分布式环境中的部分部署问题，并最大化高性能计算资源的效率。"
- q: "在安全方面，Kubelet 细粒度授权 (Fine-grained Authz) 的意义是什么？"
  a: "通过对以往授予 Kubelet 的广泛权限进行精细控制，可以实现最小权限原则，更安全地保护集群免受内部威胁。"
- q: "为什么在此次更新中 '配置过载' 被指出是一个主要问题？"
  a: "因为许多新功能处于 Alpha/Beta 阶段，需要手动控制的特性门控增加，且随着配置的精细化，运维人员需要管理的变量急剧增加，导致人为错误风险上升。"
- q: "针对 gitRepo 卷驱动程序删除的具体技术应对方案是什么？"
  a: "由于该驱动程序已被永久删除，现有的部署流水线将会中断。为解决此问题，必须立即重新设计架构，配置 init 容器或使用 git-sync 等 Sidecar 模式。"
- q: "externalIPs 停止支持对旧系统运营有什么影响？"
  a: "为了修复 CVE-2020-8554 安全漏洞，其使用受到严格限制。使用该功能的现有基础设施应尽快转向基于 Gateway API 的最新网络标准，以保证业务连续性。"
- q: "将 Alpha 阶段的功能引入实际生产环境时最需要注意什么？"
  a: "Alpha 功能很可能不保持 API 兼容性，且排错难度极高。盲目引入会降低系统可观测性，因此必须并行开展充分的验证和配置简化策略。"
- q: "如果更新到 Kubernetes 1.36，以前使用的 gitRepo 配置会完全无法运行吗？"
  a: "是的，从 v1.36 开始，gitRepo 驱动程序已被完全移除，现有配置将无法工作。为防止业务中断，务必在升级前将部署方式更改为 Sidecar 模式或其他工具。"
- q: "很多人说 1.36 版本运维起来非常复杂，实务人员最先应该关注什么？"
  a: "比起华丽的新技术，防止因功能删除导致的业务故障更为优先。特别是要先检查是否使用了 gitRepo 和 externalIPs，并将增加的配置值简化到可管理的水平，这一点至关重要。"
---

<div class="bluf"><strong>[BLUF]</strong><p>Kubernetes v1.36 为高性能工作负载带来了创新，但由于强制移除 gitRepo 和停止支持 externalIPs，给现有的遗留系统带来了破坏性的迁移风险。运维人员应优先考虑解决由 Alpha/Beta API 引起的“配置过载”问题，而非单纯的功能引入。</p></div>

Kubernetes 的新版本 v1.36 “Haru” 给了我们一个双刃剑般的课题。随着云原生生态系统的成熟，系统变得越来越精细，但与此同时，运维人员必须承担的复杂度重量也在呈几何级数增长。现在是时候冷静地审视这次更新究竟在实际基础设施架构中制造了哪些裂痕，而不仅仅是罗列新功能。

## 1. “飞翔的” Haru，背后的复杂阴影

### 1.1. 新功能的承诺：高性能工作负载与精细控制

v1.36 展现了容纳人工智能 (AI) 和机器学习 (ML) 工作负载的强大意愿。<a href="/cn/glossary/dra-dynamic-resource-allocation" class="glossary-tooltip" data-definition="Kubernetes 用于灵活分配 GPU 等特殊硬件的新型资源分配框架">DRA (Dynamic Resource Allocation)</a> 的高度完善，为摆脱过去静态资源分配方式、灵活管理硬件加速器奠定了基础。这对于需要高性能计算的企业来说无疑是福音，但为了实现它而需要的复杂 API 结构则构成了另一道屏障。

引入将 Pod 组作为一个逻辑单元处理的 <a href="/cn/glossary/was-workload-aware-scheduling" class="glossary-tooltip" data-definition="将 Pod 组识别为一个逻辑单元并进行原子级调度的高性能工作负载优化功能">WAS (Workload Aware Scheduling)</a> 同样具有创新性。它从源头上解决了分布式环境中出现的部分调度问题，能够最大化整体资源效率。然而，这种“原子级调度”显著提高了调度器配置的难度，导致运维人员需要关注的变量大幅增加。

### 1.2. 现实挑战：Alpha/Beta API 带来的运营阴影

大多数创新功能仍处于 Alpha 或 Beta 阶段，这对一线运维人员来说是巨大的负担。不成熟的 API 可能随时忽略向下兼容性并发生变更，这直接关系到生产环境的不稳定性。为了使用功能而必须激活的大量 <a href="/cn/glossary/what-is-feature-gate" class="glossary-tooltip" data-definition="用于在 Kubernetes 集群中单独控制特定功能是否激活的配置机制。">特性门控</a> (Feature Gates) 诱发了所谓的“配置过载”，这是提高人为错误发生可能性的核心因素。

![Kubernetes 1.36 - 青绿色与紫色光芒交织的玻璃板之间，点与线精巧连接的抽象数字景观。](../../../../../source/posts/Kubernetes_1.36/81baafaf-0.webp)

## 2. 主要更新分析：玫瑰色的功能与隐藏的复杂度

通过下表一目了然地确认此次发布的内核。明确认知各项功能的状态及其带来的风险，是成功迁移的第一步。

| 分类 | 功能名 | 状态 | 主要影响及风险 |
| :--- | :--- | :--- | :--- |
| **安全** | Kubelet Fine-grained Authz | Stable | 可实现权限最小化，但 RBAC 配置复杂度增加 |
| **调度** | Workload Aware Scheduling (WAS) | Alpha | 可实现高性能 Pod 组原子级部署，诱发配置过载 |
| **存储** | gitRepo Volume Driver | Removed | 导致现有工作负载中断，必须立即迁移 |
| **网络** | Service.spec.externalIPs | Deprecated | 消除 CVE-2020-8554 安全风险，计划于 v1.43 完全删除 |

### 2.1. Stable 功能：在获得稳定性的同时迎来新的管理点

Kubelet Fine-grained Authorization 进入 Stable 阶段是安全方面的重大进展。通过对以往授予 Kubelet 的广泛权限进行精细控制，可以保护集群免受内部威胁。然而，精细的控制意味着需要管理的 RBAC 策略会增多，这加剧了运维大规模集群组织的配置管理疲劳感。

### 2.2. Beta 功能：实用但仍有许多课题的功能

Beta 阶段的功能虽然功能完整度较高，但往往运营指南尚未明确建立。特别是网络和存储接口的扩展，要求与云服务提供商 (CSP) 紧密集成。这可能会加深厂商锁定风险，对于推进多云战略的企业来说，这也是强制其进行额外架构审查的环节。

### 2.3. Alpha 功能：窥见未来，却是“配置过载”的顶点

Alpha 阶段提供的功能实际上是“双刃剑”。虽然具有率先引入最新技术以获取竞争力的优点，但应用于生产环境的风险过大。像 WAS 这样的功能尤其会让调度逻辑变得复杂，使排错难度呈指数级上升。专家警告说，盲目引入此类 Alpha 功能可能会降低整个系统的可观测性。

> "v1.36 预示着‘配置过载’时代的到来，在赋予运维人员更精细控制力的同时，也赋予了沉重的管理责任。"

## 3. 阻碍实务的“破坏性迁移”风险

### 3.1. Service.spec.externalIPs Deprecation：清理安全债务的开始

长期被忽视的 `externalIPs` 安全漏洞终于进入了正式监管阶段。这个被称为 CVE-2020-8554 的漏洞是攻击者可以拦截流量的致命漏洞。从 v1.36 开始，该功能的使用将受到严格限制，并计划在未来的 v1.43 中完全移除。由于许多遗留基础设施仍在使用这种方式，向 Gateway API 的转型已成为迫在眉睫的生存问题。

### 3.2. gitRepo Volume Driver 强制删除：清理遗留与即时应对

更严重的问题是 `gitRepo` 卷驱动程序的永久删除。虽然这是为了消除利用节点的 root 权限执行恶意代码的潜在风险而采取的措施，但一直利用该功能的旧部署流水线正面临立即中断的危机。现在，运维团队必须配置 init 容器或使用 `git-sync` 等 Sidecar 模式彻底重新设计架构。这超出了单纯的版本升级，是威胁业务运营连续性的破坏性变化。

![Kubernetes 1.36 - 半透明的晶体碎片被精密分解并重新组装，象征着新的开始与变化。](../../../../../source/posts/Kubernetes_1.36/fe8ff0c5-1.webp)

## 4. 结论：Kubernetes v1.36，明智升级的检查点

Kubernetes v1.36 “Haru” 在向我们展示技术进步的同时，也提出了考验运营成熟度的问题。与其沉溺于华丽的新技术，不如先衡量我们承担的安全债务和遗留系统的重量。此次发布的数字化成果如下：

* 发布周期：2026 年 1 月 12 日至 4 月 22 日，历时 15 周
* 贡献规模：106 家企业参与，491 名个人贡献者完成了 70 项强化事项
* 功能分布：18 项功能转为 Stable，25 项功能进入 Beta/Alpha
* 市场特异点：报告了以金融和电商为中心的 externalIPs 使用案例，Gateway API 的引入正在加速

> "为解决安全债务而永久删除 gitRepo，不是选择，而是为了生存的强制性转折点。"

归根结底，成功运营 v1.36 的核心在于“简化”。抵御新功能提供的诱惑，将集群的复杂度保持在可控范围内，同时迅速清除构成安全威胁的遗留系统，这正是当代 Kubernetes 架构师被赋予的真正能力。

## 🔗 推荐阅读
- [RLHF 的明与暗：AI 对齐革命与阿谀奉承式智能的本质局限性分析](/cn/posts/rlhf-ai-alignment-limitations-sycophancy)
- [分布式共识的悖论：数学上的完美带来的过度工程陷阱](/cn/posts/distributed-consensus-overengineering-paradox)