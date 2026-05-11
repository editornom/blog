---
title: "AF_ALGとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 11:30:06.736176+09:00
slug: "what-is-af-alg"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "AF_ALGは、ユーザー空間アプリケーションが標準のソケットAPIを介して暗号アルゴリズムやハードウェアアクセラレーションにアクセスできるようにするLinuxカーネルインターフェースです。技術的実装、splice()システムコールによる実用例、CVE-2026-31431などの脆弱性との関連性について解説します。"
references: []
modDatetime: 2026-05-08 11:40:06.736176+09:00
---## AF_ALGとは？

### 辞書的定義 (Dictionary Definition)
AF_ALGは、Linuxカーネル（Linux Kernel）が提供する暗号化サブシステムにアクセスするためのユーザー空間（User-space）インターフェースです。「Address Family - Algorithm」の略称であり、ユーザー空間のアプリケーションが標準のソケットAPI（Socket API）を通じて、カーネル内部に実装された暗号化アルゴリズム（AES、SHA、HMACなど）を直接呼び出して利用できるように設計された経路です。ハードウェアアクセラレータなどのカーネルレベルのリソースを活用し、効率的な暗号化演算の実行を支援します。

### 実務での使用例 (Practical Use Case)
- **カーネル暗号化エンジンの呼び出し**: ユーザー空間のプログラムがカーネルの暗号化モジュールを使用してデータを処理する場合、ソケットを作成し、bind()およびaccept()を介して特定のアルゴリズムに接続して使用します。
- **システムコールとの相互作用**: splice()システムコールと組み合わせてデータコピープロセスを最適化したり、暗号化データを処理したりするために活用されます。最近では、このプロセスにおける設計上の欠陥を悪用したCVE-2026-31431（Copy Fail）脆弱性の事例のように、AF_ALGとsplice()の相互作用を通じた権限昇格攻撃の研究対象として分析されています。

### 関連用語 (Related Words)
- CVE-2026-31431 (Copy Fail)
- splice() システムコール
- Linuxカーネル暗号化API (Crypto API)
- ページキャッシュ汚染 (Page Cache Corruption)
