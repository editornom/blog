---
title: "PKI (公开键基础设施) 定义与核心摘要"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-30 08:55:37.007710+09:00
slug: pki-fundamentals-digital-security-guide
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "PKI (公开键基础设施) 是通过数字证书和非对称加密技术保障数据机密性与完整性的核心安全体系。本文详细介绍了作为 HTTPS 安全通信及电子签名基础的 PKI 定义与实务案例。"
references: []
modDatetime: 2026-04-30 09:05:37.007710+09:00
---

# 什么是 PKI？

## 词典定义 (Dictionary Definition)
PKI (Public Key Infrastructure，公开键基础设施) 是为了数字证书的生成、管理、分发、使用、存储及撤销而所需的硬件、软件、人员、政策及流程的集合体。它基于非对称加密技术，利用公钥和私钥对在网络上保障数据的机密性、完整性以及身份确认，是一套完整的安全标准体系。

## 实际应用案例 (Practical Use Cases)
- **HTTPS 安全通信**：在以浏览器地址栏锁形图标为代表的 SSL/TLS 通信中，用于证明服务器的可信度并对传输数据进行加密。
- **电子签名**：用于确保电子文档的完整性并验证签署者身份，从而赋予电子文件法律效力。
- **企业安全**：作为企业内部电子邮件加密、远程 VPN 接入时的用户身份验证以及内部系统访问控制的技术基石。

## 相关术语 (Related Terms)
- **非对称加密 (Asymmetric Encryption)**：一种使用一对互补的密钥（公钥和私钥）分别进行加密和解密的加密方式。
- **证书颁发机构 (CA, Certificate Authority)**：负责颁发和管理数字证书，并对密钥所有权进行认证的可信第三方机构。
- **RSA/ECC**：在 PKI 环境中用于生成数字证书和加密数据的两种最主流的加密算法。