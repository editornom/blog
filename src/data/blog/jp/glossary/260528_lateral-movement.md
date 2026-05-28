---
title: "ラテラルムーブメント（Lateral Movement）"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-28 11:37:00.759886+09:00
slug: "lateral-movement"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "ラテラルムーブメント（Lateral Movement）は、攻撃者が内部ネットワークに侵入した後、権限を拡張しながら高価値の資産へと到達する主要な攻撃フェーズです。本記事では、その定義と実例、防止策としてのマイクロセグメンテーション戦略を解説します。"
references: []
modDatetime: 2026-05-28 11:47:00.759886+09:00
---

# ラテラルムーブメント（Lateral Movement）とは？

### 辞書的定義 (Dictionary Definition)
サイバーセキュリティにおけるラテラルムーブメント（Lateral Movement、横展開）とは、攻撃者が組織の内部ネットワークへの初期侵入に成功した後、システム内部を探索しながら他のサーバー、ワークステーション、またはデータへのアクセス権限を拡張していく一連のプロセスを指します。攻撃者は侵入後の最初の足がかり（Foothold）から特権アカウントの奪取や認証情報の窃取を行い、ネットワーク内の「重要資産（Crown Jewels）」に到達することを最終的な目標とします。

### 実務での使用例 (Practical Use Case)
攻撃者がフィッシングメールを通じて一般社員のPCをマルウェアに感染させ、その端末に保存されていた認証情報を利用して内部のファイルサーバーやデータベース管理サーバーへと移動し、企業の機密情報を外部へ流出させるケースが代表例です。従来の境界型セキュリティモデル（VPNなど）は内部の接続者を暗黙的に信頼するため、このようなラテラルムーブメントに対して脆弱です。これを防ぐためには、すべての接続を常に検証するゼロトラスト（Zero Trust）ベースのマイクロセグメンテーション（Micro-segmentation）の導入が推奨されます。

### 関連用語 (Related Words)
- ゼロトラスト（Zero Trust）
- マイクロセグメンテーション（Micro-segmentation）
- 最小権限の原則（Principle of Least Privilege）