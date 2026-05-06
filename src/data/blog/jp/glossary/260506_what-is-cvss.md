---
title: "CVSSとは？共通脆弱性評価システムの定義と活用方法"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-06 11:25:09.238064+09:00
slug: what-is-cvss-vulnerability-scoring-system
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "CVSS（共通脆弱性評価システム）は、セキュリティ脆弱性の深刻度を0.0から10.0のスコアで評価し、対応の優先順位を決定するための標準化されたフレームワークです。リスクレベルを客観的に分析し、効率的なパッチ管理戦略を立案する方法を解説します。"
references: []
modDatetime: 2026-05-06 11:35:09.238064+09:00
---

# CVSSとは？

### 辞書的な定義 (Definition)
共通脆弱性評価システム（Common Vulnerability Scoring System、CVSS）は、情報セキュリティにおける脆弱性の深刻度を評価するために設計された、標準化されたオープンなフレームワークです。脆弱性が持つ技術的な特性を数値化し、0.0から10.0までのスコアを付与します。これにより、組織は発見されたセキュリティ上の欠陥のリスクレベルを客観的に比較し、セキュリティパッチの適用や対応の優先順位を定量的に判断することが可能になります。

### 実務での活用事例 (Practical Use Case)
セキュリティ運用チームは、CVE-2026-31431（Copy Fail）脆弱性に対応する際、CVSS 3.1のベーススコア（Base Score）である7.8（High）を参考にします。このスコアが高リスク群に属することを認識し、攻撃元区分（AV）がローカル（L）であるにもかかわらず、コンテナ脱出が可能であるという技術的な詳細を組み合わせることで、Cloudインフラ内のLinuxカーネルパッチ適用を最優先課題として選定する判断根拠として活用します。

### 関連用語 (Related Words)
* CVE (Common Vulnerabilities and Exposures): セキュリティ脆弱性に付与される、固有の標準識別子リストです。
* CWE (Common Weakness Enumeration): ソフトウェア脆弱性を引き起こす根本的な弱点をタイプ別に分類した体系です。
* NVD (National Vulnerability Database): CVSSスコアの算出や脆弱性分析情報を提供する、米国政府の国家脆弱性データベースです。