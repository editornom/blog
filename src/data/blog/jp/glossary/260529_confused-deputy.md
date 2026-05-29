---
title: "Confused Deputy"
author: editornom
author_role: シニアテックエディター
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 18:48:35.245929+09:00
slug: "confused-deputy"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Confused Deputyは、権限を持つ代理人が低い権限の要求を検証なしに実行することで発生するセキュリティ脆弱性で、権限の濫用やデータ流出の主な原因となります。AIエージェント環境で発生し得る間接プロンプトインジェクションなどの関連リスクとセキュリティ対策について説明します。"
references: []
modDatetime: 2026-05-29 18:58:35.245929+09:00
---

# Confused Deputyとは？

### 辞書的な定義 (Dictionary Definition)
権限を持つ代理人（Deputy）が、自身に付与された特権を適切な検証なしに使用し、権限の低いエンティティの要求を代行することで発生するセキュリティ脆弱性です。システムが要求者の権限ではなく、代理人自身の権限を基準にタスクを承認してしまうことで発生し、これは権限の濫用やデータ流出の主な原因となります。

### 実務での使用例 (Practical Use Case)
Model Context Protocol (MCP) ベースのAIエージェントが、ユーザーの指示に従ってメールを送信したりファイルを修正したりする際、その指示がセキュリティポリシーに抵触するかどうかを確認せず、エージェント自身のシステム権限で即座に実行してしまうケースがこれに該当します。

### 関連用語 (Related Words)
権限昇格 (Privilege Escalation)、間接プロンプトインジェクション (Indirect Prompt Injection)、アクセス制御 (Access Control)