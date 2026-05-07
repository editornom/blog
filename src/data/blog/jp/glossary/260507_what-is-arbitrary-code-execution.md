---
title: "任意コード実行（ACE）とは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 17:28:53.718744+09:00
slug: understanding-arbitrary-code-execution-security
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "任意コード実行（ACE）は、システムの脆弱性を悪用して攻撃者が意図した非認可コードを実行する致命的なセキュリティ上の欠陥です。ACEの定義と危険性、そしてMCP環境における具体的な発生事例を通じて、システム制御権を脅かすセキュリティ経路を詳細に解説します。"
references: []
modDatetime: 2026-05-07 17:38:53.718744+09:00
---

# 任意コード実行（ACE）とは？

### 辞書的定義 (Dictionary Definition)
任意コード実行（Arbitrary Code Execution, ACE）は、攻撃者がシステムやアプリケーションの脆弱性を悪用し、対象のコンピュータまたはプロセス上で自身が意図した任意のコマンドやソフトウェアを実行できるセキュリティ上の欠陥です。攻撃者はこの脆弱性を介してシステムの制御権を奪取したり、データの改ざんや窃取を行ったりすることが可能であり、システムのセキュリティ境界を完全に崩壊させる高リスクな脅威として分類されます。

### 実務での活用例 (Practical Use Case)
Model Context Protocol (MCP) 環境において、ホストがサーバーの機能を探索する「Capability Discovery（機能探索）」フェーズで発生する可能性があります。信頼できないサーバーが、悪意のあるコードを含むツール（Tools）スキーマをホストに提供し、LLM がこれを正当なツールであると誤認して実行するように誘導された場合、該当システム内部で攻撃者が意図した非認可コードが実行される ACE 経路が形成されます。

### 関連用語 (Related Words)
- RCE (Remote Code Execution)
- 権限昇格 (Privilege Escalation)
- エクスプロイト (Exploit)