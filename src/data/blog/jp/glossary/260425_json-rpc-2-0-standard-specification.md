---
title: "JSON-RPC 2.0とは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-25 09:10:00+09:00
slug: json-rpc-2-0-specification-and-use-cases
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "JSON-RPC 2.0は、JSONベースの軽量な遠隔手続き呼び出し(RPC)プロトコルであり、ステートレスなデータ交換やバッチ処理をサポートします。AIモデルとデータ間の標準的な通信プロトコルとしての定義と実例を紹介します。"
references: []
modDatetime: 2026-04-28 15:14:18.960187+09:00
---

# JSON-RPC 2.0とは？

### 辞書的定義 (Dictionary Definition)
JSON-RPC 2.0は、JSON (JavaScript Object Notation) データをベースとした軽量な遠隔手続き呼び出し (Remote Procedure Call, RPC) プロトコルです。クライアントとサーバー間のデータ交換のために設計されたステートレス (Stateless) 通信規約であり、リクエスト (Request)、レスポンス (Response)、通知 (Notification)、およびバッチ (Batch) 処理をサポートします。トランスポート層に依存しない構造を持っており、HTTP、WebSockets、TCPなど、さまざまなネットワーク環境で活用可能です。

### 実務での活用事例 (Practical Use Case)
Anthropicが公開した MCP (Model Context Protocol) は、AIモデルと外部データソース間の断片化されたインターフェースを統合するために、JSON-RPC 2.0を標準通信プロトコルとして採用しています。クライアントはJSON形式のメッセージを通じてサーバーに特定のツール (Tools) の実行やリソース (Resources) の照会をリクエストし、サーバーは規格化されたJSONデータで応答することで、AIエージェントと企業用データベース間のリアルタイムな相互作用を実現します。

### 関連用語 (Related Words)
- RPC (Remote Procedure Call)
- JSON (JavaScript Object Notation)
- MCP (Model Context Protocol)