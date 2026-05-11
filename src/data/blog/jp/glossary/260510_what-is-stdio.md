---
title: "STDIOとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-10 17:03:53.759572+09:00
slug: "what-is-stdio"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "STDIO（標準入出力）の概念と、MCP環境における実務での活用事例を通じて、プロセス間通信（IPC）の核心的な原理を解説します。システムの標準ストリームを活用し、別途ネットワークポートを開放することなく、安全で効率的なデータ交換を実現する方法について説明します。"
references: []
modDatetime: 2026-05-10 17:13:53.759572+09:00
---### STDIOとは？

#### 辞書的定義 (Dictionary Definition)
STDIO（Standard Input/Output）は、コンピュータのオペレーティングシステムにおいて、プログラムと外部環境の間でデータをやり取りするためにデフォルトで用意されている入出力経路である「標準ストリーム」を指します。一般的に、標準入力（stdin）、標準出力（stdout）、標準エラー出力（stderr）の3つのチャネルで構成されます。プログラムが特定のハードウェアやネットワーク設定に依存することなくデータを読み書きできるように支援する、抽象化されたインターフェースの役割を果たします。

#### 実務での活用事例 (Practical Use Case)
Model Context Protocol（MCP）の規格において、ローカル環境にインストールされたクライアントとサーバープロセスが通信する際、別途ネットワークポートを開放する代わりに、システムのSTDIOを主要な転送経路として利用します。これは、プロセス間の直接的な入出力を通じてデータ転送の遅延（レイテンシ）を最小限に抑え、ネットワークレイヤーを介した外部からのアクセスを物理的に遮断することで、ローカル環境におけるセキュリティを強化するために活用されています。

#### 関連用語 (Related Words)
- **IPC (Inter-Process Communication)**: オペレーティングシステム内で複数のプロセスが互いにデータをやり取りするメカニズムを指し、STDIOはその中で最も基本的な通信手段の一つです。
- **JSON-RPC**: STDIOストリームを通じて構造化されたコマンドやレスポンスをやり取りするために使用される、軽量な遠隔手続き呼出しプロトコルです。
- **Standard Stream (標準ストリーム)**: システムのターミナルや入出力デバイスとプログラムの間を接続する、データフローの標準モデルの総称です。
