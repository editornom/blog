---
title: "什么是 CVSS？"
author: editornom
author_role: "高级技术编辑"
author_url: https://editornom.com/about
pubDatetime: 2026-05-06 11:25:09.238064+09:00
slug: cvss-vulnerability-severity-rating-standard
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "CVSS（通用漏洞评分系统）是一种用于评估安全漏洞严重程度的标准化框架，评分范围从 0.0 到 10.0。了解如何利用该系统客观分析风险并制定高效的安全修复策略。"
references: []
modDatetime: 2026-05-06 11:35:09.238064+09:00
---

# 什么是 CVSS？

### 定义 (Definition)
通用漏洞评分系统 (Common Vulnerability Scoring System, CVSS) 是一个旨在评估信息安全漏洞严重程度的标准化开放框架。它通过量化漏洞的技术特征，赋予 0.0 到 10.0 之间的分值。通过该系统，企业和组织可以客观地比较已发现安全缺陷的风险等级，并定量地决定安全补丁及应对措施的优先级。

### 实际应用案例 (Practical Use Case)
安全运维团队在应对 CVE-2026-31431 (Copy Fail) 漏洞时，会参考 CVSS 3.1 的基础评分 (Base Score) 7.8 (High)。在意识到该分数属于高风险级别后，即使攻击向量 (AV) 为本地 (L)，团队也会结合其具备容器逃逸能力的这一技术细节，将其作为优先修复 Cloud 基础设施内 Linux 内核补丁的判断依据。

### 相关术语 (Related Words)
* <b>CVE (Common Vulnerabilities and Exposures)</b>: 为安全漏洞分配的唯一标准标识符列表。
* <b>CWE (Common Weakness Enumeration)</b>: 根据类型对导致软件漏洞的根本弱点进行分类的体系。
* <b>NVD (National Vulnerability Database)</b>: 美国政府提供的国家级漏洞数据库，提供 CVSS 评分计算及漏洞分析信息。