---
title: "Rowhammer"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 11:23:04.486265+09:00
slug: "rowhammer"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "RowhammerはDRAMの特定の行を繰り返しアクティブ化することで隣接する行のビット反転を誘発するハードウェアの脆弱性であり、システム権限の奪取やデータ改ざんなどの深刻なセキュリティ脅威をもたらします。最新のDDR5やGPUを標的とした攻撃事例から、TRR、PRACなどの実務的な対応技術まで解説します。"
references: []
modDatetime: 2026-05-09 11:33:04.486265+09:00
---

# Rowhammerとは？

### 辞書的な定義 (Dictionary Definition)
DRAM(Dynamic Random Access Memory)の特定のメモリ行(Row)を高速で繰り返しアクティブ化することで、隣接する行の電荷干渉を誘発し、それによって保存されたデータのビットが反転(Bit-flip)するハードウェアのセキュリティ脆弱性です。これは微細化された半導体素子間の物理的な干渉現象を悪用したもので、ソフトウェア的なアクセス権限をバイパスしてメモリデータを改ざんしたり、システム権限を奪取したりするために悪用される可能性があります。

### 実務での活用事例 (Practical Use Case)
1. **DDR5脆弱性攻撃**: 製造元が適用したTRR(Target Row Refresh)技術のサンプリングロジックを回避する「Phoenix」攻撃を通じて、最新のメモリモジュールでもビットフリップを発生させる事例が確認されています。
2. **GPUセキュリティ侵害**: GDDR6メモリのアーキテクチャ的特性を利用した「GPUBreach」攻撃を実行し、高性能コンピューティング環境においてルート権限を奪取する手法に活用されます。
3. **実務的な対応戦略**: リフレッシュ周期(tREFI)を短縮して電荷漏洩が発生する前にメモリセルを再充電するか、DRAM内部で行のアクティブ化回数を直接カウントするPRAC(Per-Row Activation Counting)技術を導入して攻撃を遮断します。

### 関連用語 (Related Words)
1. **ビットフリップ (Bit-flip)**: 物理的な干渉により、メモリ内の論理データ値が0から1、または1から0へと反転する現象です。
2. **TRR (Target Row Refresh)**: 特定の行の過度なアクティブ化が検出された際に、隣接する行を先制的にリフレッシュするハードウェアベースの防御技術です。
3. **PRAC (Per-Row Activation Counting)**: DRAMの各行がアクティブ化される回数をリアルタイムでカウントし、Rowhammer攻撃のしきい値への到達を防止する次世代のセキュリティ標準手法です。