---
title: "Thundering Herdとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 11:39:40.174633+09:00
slug: "thundering-herd"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Thundering Herd（サンダリングハード）とは、複数のプロセスが同時に起動して単一のリソースを競い合うことで発生する分散システムの性能低下現象を指します。本記事では、キャッシュスタンピードやミューテックスの競合などの原因と、システムの安定性を維持するための主要な戦略を解説します。"
references: []
modDatetime: 2026-05-29 11:49:40.174633+09:00
---

# Thundering Herd（サンダリングハード）とは？

### 辞書的定義 (Dictionary Definition)
「サンダリングハード（Thundering Herd）」問題とは、コンピュータサイエンスおよび分散システムにおいて、特定のイベントが発生した際に、待機していた多数のプロセスやスレッドが一斉に起動し、同一のリソースを処理しようとすることで発生するパフォーマンス低下現象を指します。すべてのリクエストがリソースを獲得するために競い合いますが、実際には極めて少数、あるいは単一のプロセスのみが成功し、残りは再び待機状態に戻ります。この過程で発生する過度なコンテキストスイッチ（Context Switching）とCPUリソースの浪費が、システム全体の可用性を低下させるのが特徴です。

### 実務における使用例 (Practical Use Case)
1. **キャッシュスタンピード (Cache Stampede)**: トラフィックの多い特定のデータのキャッシュが期限切れになった瞬間、多数のクライアントが同時にオリジンデータベース（Origin DB）にアクセスしてレスポンスを要求することで、データベースサーバーが麻痺する状況で主に発生します。
2. **ヘッジドリクエスト (Hedged Requests) の副作用**: システム遅延が発生した際、複数の複製されたリクエストを同時に送信する手法を不注意に使用すると、遅延が発生している特定のバックエンドノードにトラフィックが爆発的に増加し、システムが回復不能な状態に陥る「自爆型DoS」現象がこれに該当します。
3. **ミューテックス (Mutex) の競合**: 共有リソースのロックが解除された際、それを待機していたすべてのスレッドが一斉に起動してリソースを占有しようとする、カーネルレベルのスケジューリング負荷の状況で見られます。

### 関連用語 (Related Words)
- Request Coalescing（リクエスト結合）
- Cache Stampede（キャッシュスタンピード）
- Exponential Backoff（指数的バックオフ）