---
title: "什么是 SBOM？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-27 15:10:00+09:00
slug: what-is-sbom-definition-and-security-role
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "SBOM (软件物料清单) 是详细记录软件组件及其依赖关系的清单，旨在确保供应链透明度并快速响应安全漏洞。它在现代软件开发中起着系统化管理安全风险的关键作用。"
references: []
modDatetime: 2026-04-29 17:02:58.183611+09:00
---

# 什么是 SBOM？

### 定义
SBOM (Software Bill of Materials，软件物料清单) 是详细记录构成软件产品的所有开源包、库、模块及其相互依赖关系的明细表。它是将制造业中的物料清单 (BOM) 概念应用于软件开发领域，旨在复杂的现代软件供应链中确保组件透明度，并为系统化管理安全漏洞提供标准化的列表。

### 实战应用案例
当某个特定开源库（如 Log4j）发现严重安全漏洞时，安全运营团队可以通过检索预先构建的 SBOM 数据库，立即识别公司内部哪些系统和应用程序包含该库。这大大缩短了全面排查所需的时间，并能迅速确定补丁修复等应对措施的优先级。

### 相关术语
* **软件供应链安全 (SSCS)：** 指从软件设计、开发、发布到运营的全过程，对安全威胁进行管理和控制的体系。
* **SCA (Software Composition Analysis)：** 软件成分分析，是一种用于分析应用程序中所含开源组件的安全漏洞和许可证风险的技术。
* **SLSA (Supply-chain Levels for Software Artifacts)：** 由 Google 提出的安全框架，旨在确保软件产出物的完整性。