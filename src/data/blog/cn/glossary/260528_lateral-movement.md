---
title: "横向移动 (Lateral Movement)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-28 11:37:00.759886+09:00
slug: "lateral-movement"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "横向移动 (Lateral Movement) 是攻击者进入内部网络后，通过扩展权限并触达高价值资产的关键攻击阶段。本文将介绍横向移动的定义、实际应用案例，以及旨在防止此类攻击的基于零信任的微隔离策略。"
references: []
modDatetime: 2026-05-28 11:47:00.759886+09:00
---

# 什么是横向移动 (Lateral Movement)？

### 词典定义 (Dictionary Definition)
在网络安全领域，横向移动 (Lateral Movement) 是指攻击者在初步侵入组织的内部网络后，通过在系统内部进行探测，逐步扩大对其他服务器、工作站或数据的访问权限的一系列过程。攻击者在成功渗透并建立初始立足点 (Foothold) 后，其最终目标是获取管理员权限或窃取凭据，从而触达网络中的高价值资产 (Crown Jewels)。

### 实际应用案例 (Practical Use Case)
典型的案例是攻击者通过钓鱼邮件感染普通员工的 PC，随后利用该终端上存储的身份凭据，移动到内部文件服务器或数据库管理服务器，从而窃取企业的敏感信息。传统的边界防护安全模型（如 VPN 等）由于对内部访问者采取隐式信任，因此在应对此类横向移动时非常脆弱。为了防止这种情况，业界建议采用验证所有连接的零信任架构以及微隔离 (Micro-segmentation) 策略。

### 相关词汇 (Related Words)
- 零信任 (Zero Trust)
- 微隔离 (Micro-segmentation)
- 最小权限原则 (Principle of Least Privilege)