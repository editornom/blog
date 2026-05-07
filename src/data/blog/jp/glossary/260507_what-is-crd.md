---
title: "CRD（Custom Resource Definition）とは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 11:29:40.487351+09:00
slug: what-is-kubernetes-crd
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "CRD（Custom Resource Definition）は、Kubernetes APIを拡張して標準リソース以外に独自のオブジェクトタイプを定義・管理できるようにする標準メカニズムです。オペレーターパターンやGateway APIのように、特定の要件に最適化されたリソースの作成や運用の自動化に不可欠です。"
references: []
modDatetime: 2026-05-07 11:39:40.487351+09:00
---

# CRD（Custom Resource Definition）とは？

### 辞書的定義 (Dictionary Definition)
カスタムリソース定義（Custom Resource Definition, CRD）は、Kubernetes APIを拡張するための標準メカニズムであり、ユーザーが標準で提供されているリソース（Pod、Serviceなど）のほかに、独自のオブジェクトタイプを定義してクラスターに追加できるようにする機能です。これにより、開発者や運用担当者は特定のアプリケーションの要件に合わせたカスタムリソースを作成し、Kubernetes APIサーバーを通じてこれらを標準リソースと同様に管理することができます。

### 実務での使用例 (Practical Use Case)
Kubernetes Gateway APIは、従来のIngressの限界を克服するために、GatewayClass、Gateway、HTTPRouteといったリソースをCRD形式で定義してデプロイします。また、データベース管理や自動バックアップのような複雑な運用ロジックを処理するオペレーター（Operator）パターンにおいて、アプリケーションの状態を定義・制御するためのデータ規格として不可欠に使用されています。

### 関連用語 (Related Words)
- Custom Resource (CR)
- Operator Pattern
- Kubernetes API Server
- Gateway API