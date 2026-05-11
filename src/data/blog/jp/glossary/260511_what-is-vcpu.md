---
title: "vCPUとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 11:36:06.856378+09:00
slug: "what-is-vcpu"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "vCPU（仮想中央演算処理装置）の定義、物理CPUリソースを仮想マシンに割り当てる仕組み、およびクラウド環境での実務活用事例について解説します。ハイパーバイザーを通じて演算能力を効率的に管理し、インスタンスのパフォーマンスを最適化する重要指標を確認しましょう。"
references: []
modDatetime: 2026-05-11 11:46:06.856378+09:00
---

# vCPUとは？

## 辞書的定義 (Dictionary Definition)
vCPU（Virtual Central Processing Unit）とは、仮想化されたコンピューティング環境において仮想マシン（VM）に割り当てられる論理的な演算単位を指します。物理プロセッサ（pCPU）のリソースをハイパーバイザー（Hypervisor）を通じて抽象化して提供し、一般的にはハードウェアの物理コア、またはハイパースレッディング（Hyper-threading）技術が適用された論理スレッドに対応します。

## 実務での活用事例 (Practical Use Case)
クラウドサービス利用時、インスタンスの性能を決定する重要な指標として活用されます。例えば、MySQLデータベースをクラウド環境（AWS RDSなど）に構築する際、ワークロードの複雑さと処理量に合わせてvCPU数を選択することで、演算能力を拡張または制限します。

## 関連用語 (Related Words)
ハイパーバイザー（Hypervisor）、物理CPU（Physical CPU）、インスタンス（Instance）