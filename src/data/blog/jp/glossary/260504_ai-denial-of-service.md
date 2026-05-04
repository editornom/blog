---
title: "AI DoS (AI Denial of Service)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-04 17:44:25.150003+09:00
slug: ai-dos-security-threats-explained
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "AI DoS（AIサービス拒否攻撃）は、AIモデルの設計上の脆弱性を悪用してシステムリソースを枯渇させ、サービス提供を中断させる攻撃手法です。プロンプトインジェクションによるリソース消費やAPIクォータの枯渇など、AI DoSの定義と主要事例を通じてセキュリティの脅威を確認しましょう。"
references: []
modDatetime: 2026-05-04 17:54:25.150003+09:00
---

# AI DoSとは？

### 辞書的定義 (Dictionary Definition)
AI DoS（AI Denial of Service、人工知能サービス拒否）は、人工知能モデルや関連インフラの設計上の脆弱性を悪用して、システムリソースを枯渇させたり、サービス提供を中断させたりする攻撃手法です。これは、LLM（大規模言語モデル）が入力データと命令語を明確に区別できない「入力データと命令語の分離の失敗（Command/Data separation failure）」という現象を利用する場合が多いです。攻撃者は特定の文字列や複雑なプロンプトを通じてモデルを無限ループに陥らせたり、過度な推論コストを発生させてユーザーのAPIクォータ（Quota）を即座に使い果たさせることで、正常なサービスの利用を妨害します。

### 実務での使用例 (Practical Use Case)
最近、AIコーディングアシスタントである「Claude Code」環境において、特定のメタデータ（例：OpenClaw関連の文字列）が含まれるソースコードを読み込む際、これをシステム命令と誤認してプロンプトインジェクションが発生する事例が報告されました。この過程で、ユーザーの意図とは関係なくAIモデルが異常な演算を繰り返し、Claude Proプランの割り当て量を瞬時に100%消費してセッションを終了させるAI DoS状態を誘発することが確認されました。

### 関連用語 (Related Words)
- プロンプトインジェクション (Prompt Injection)
- リソース枯渇攻撃 (Resource Exhaustion)
- アーキテクチャ上の欠陥 (Architectural Flaw)