---
title: "gVisorとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 16:51:26.458171+09:00
slug: "what-is-gvisor"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "gVisorは、独自のユーザ空間カーネルを通じてシステムコールを制御することで、ホストとコンテナ間の強力なセキュリティ分離を提供するオープンソースのサンドボックスランタイムです。"
references: []
modDatetime: 2026-05-09 17:01:26.458171+09:00
---### 辞書的定義 (Dictionary Definition)
gVisorは、Google（グーグル）によって開発されたオープンソースベースのコンテナランタイムサンドボックスです。この技術は、アプリケーションとホストオペレーティングシステムのカーネルとの間でシステムコール（System Call）をインターセプトして処理する、独自のユーザ空間カーネル（User-space kernel）を提供します。従来のLinuxコンテナがホストカーネルを共有することで発生しうるセキュリティ上の脆弱性を補完し、強力なセキュリティ分離環境を構築することを目的としています。

### 実務での活用事例 (Practical Use Case)
GKE (Google Kubernetes Engine) Agent Sandbox環境において、信頼できない外部コードを実行する必要がある AI エージェントのワークロードを保護するために活用されています。セキュリティレベルの低いサードパーティ製アプリケーションを実行する際にシステムコールを制御し、ホストシステムへの侵入を防ぐ分離レイヤーとして使用されますが、この過程で発生するシステムコールのオーバーヘッドにより、高性能な推論作業時に遅延（レイテンシ）が生じることがあります。

### 関連用語 (Related Words)
* コンテナランタイム (Container Runtime)
* サンドボックス (Sandbox)
* システムコール (System Call)
