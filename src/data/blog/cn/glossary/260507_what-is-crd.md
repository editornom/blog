---
title: "什么是 CRD？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 11:29:40.487351+09:00
slug: understanding-kubernetes-crd-mechanism
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "CRD (Custom Resource Definition) 是扩展 Kubernetes API 的标准机制，允许用户在基础资源之外定义和管理自定义对象类型。它是实现 Operator 模式、Gateway API 以及针对特定应用需求优化资源并实现运营自动化的核心工具。"
references: []
modDatetime: 2026-05-07 11:39:40.487351+09:00
---

# 什么是 CRD？

### 词典定义 (Dictionary Definition)
自定义资源定义（Custom Resource Definition，简称 CRD）是扩展 Kubernetes API 的一种标准机制。它允许用户在 Pod、Service 等原生资源的基础上，定义并向集群中添加自定义的对象类型。通过 CRD，开发人员或运维人员可以根据特定应用的需求创建自定义资源，并像管理标准资源一样，通过 Kubernetes API Server 对其进行统一管理。

### 实际应用场景 (Practical Use Case)
Kubernetes Gateway API 为了克服传统 Ingress 的局限性，以 CRD 的形式定义并部署了 GatewayClass、Gateway 和 HTTPRoute 等资源。此外，在处理数据库管理或自动备份等复杂运维逻辑的 Operator 模式中，CRD 被作为定义和控制应用状态的标准数据规范而广泛使用，是实现运维自动化的基础。

### 相关词汇 (Related Words)
- Custom Resource (CR)
- Operator Pattern
- Kubernetes API Server
- Gateway API