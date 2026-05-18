---
title: "什么是策略即代码 (Policy as Code)？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-18 11:43:48.881608+09:00
slug: "policy-as-code"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "策略即代码 (PaC) 是一种通过将安全和合规性策略代码化，实现自动化治理和系统一致性的方法论。通过云基础设施安全和数据治理等实际应用案例，了解 PaC 的核心概念及提高运营效率的方法。"
references: []
modDatetime: 2026-05-18 11:53:48.881608+09:00
---

# 什么是策略即代码 (Policy as Code)？

### 词典定义 (Dictionary Definition)
策略即代码 (Policy as Code, PaC) 是一种将组织的安全、治理和合规性策略编写为基于文本的代码，并以自动化方式进行管理和应用的方法论。它将策略像软件代码一样在版本控制系统 (VCS) 中进行管理，通过系统化的验证和强制执行来确保一致性并最大限度地降低运营风险，而无需人工干预。

### 实际应用案例 (Practical Use Case)
- **数据治理合规性**：在数据网格 (Data Mesh) 架构中，在发布阶段自动验证各业务团队发布的数据产品是否符合中央定义的个人信息保护及质量标准。
- **云基础设施安全**：在基础设施即代码 (IaC) 环境中，应用安全策略以阻止在特定区域 (Region) 以外创建资源，或自动防止创建暴露于公共互联网的存储桶 (Bucket)。
- **持续合规 (Continuous Compliance)**：在 CI/CD 流水线中，如果检测到存在安全漏洞的容器镜像，则通过基于策略的审批程序自动中断部署流程。

### 相关词汇 (Related Words)
- 联邦治理 (Federated Governance)
- 基础设施即代码 (Infrastructure as Code, IaC)
- 合规自动化 (Compliance Automation)