---
title: "什么是 SSL/TLS？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-10 14:54:36.932330+09:00
slug: "what-is-ssl-tls"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "SSL/TLS 是为网络通信安全而设计的加密协议，是通过 HTTPS 安全保护 Web 浏览器与服务器之间数据的核心技术。它利用非对称和对称加密方式保证数据的机密性和完整性，防止敏感信息泄露。"
references: []
modDatetime: 2026-05-10 15:04:36.932330+09:00
---# 什么是 SSL/TLS？

### 词典定义 (Dictionary Definition)
SSL（安全套接层，Secure Sockets Layer）及其后续版本 TLS（传输层安全，Transport Layer Security）是为在计算机网络上提供通信安全而设计的加密协议。该协议利用非对称加密技术对通信双方的身份进行验证，并安全地交换加密数据所需的会话密钥。随后，在实际数据传输过程中，使用效率较高的对称加密方式来确保数据的机密性和完整性。为了解决早期 SSL 协议中发现的安全漏洞，IETF（互联网工程任务组）对 TLS 进行了标准化，现代所有的安全通信基本上都是基于 TLS 实现的。

### 实际应用案例 (Practical Use Case)
它被广泛用作 HTTPS 协议的基础技术，以确保 Web 浏览器与 Web 服务器之间的安全通信。当用户访问网站时，浏览器地址栏中显示的挂锁图标表示该连接受 SSL/TLS 保护，从而防止登录信息或信用卡号等敏感信息泄露到外部或被伪造。此外，它还被用于电子邮件发送（SMTP）与接收（IMAP、POP3）、虚拟专用网络（VPN）连接等必须确保网络安全的环境中的数据隧道化。

### 相关术语 (Related Words)
- PKI (公钥基础设施)
- HTTPS (超文本传输安全协议)
- 非对称加密 (Asymmetric Encryption)
