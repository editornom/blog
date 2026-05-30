---
title: "FLOPs (Floating Point Operations per Second)"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-30 19:36:48.490759+09:00
slug: "flops-floating-point-operations"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "FLOPs（Floating Point Operations per Second）の定義と、AIモデルの学習および推論における演算リソースを定量化する重要指標としての役割を解説します。モデルパラメータとデータ規模に基づく演算量の計算から、効率的なAI開発のための実例まで詳しく紹介します。"
references: []
modDatetime: 2026-05-30 19:46:48.490759+09:00
---

# FLOPsとは？

### 事典的定義 (Dictionary Definition)
FLOPs（Floating Point Operations per Second）は、1秒間に実行可能な浮動小数点演算の回数を測定する単位です。コンピュータの演算性能を表す代表的な尺度であり、AI（人工知能）の分野では、大規模言語モデル（LLM）などの学習（Training）や推論（Inference）の過程で必要とされる総演算量（Total Floating Point Operations）を指す指標としても広く用いられています。これはモデルのパラメータ数や学習データの量と密接に関連しており、AIの性能向上のために投入されるコンピュートリソース（Compute）の規模を定量化する重要な変数です。

### 実務での活用例 (Practical Use Case)
1. AIモデルの開発時、学習全体に必要な総FLOPsを算出することで、必要なGPUリソースの規模やクラウドコンピューティングコストを事前に予測します。
2. 同等の性能を維持しながら、より少ないFLOPsで動作する軽量化アルゴリズムを開発し、デバイス上での推論（On-device AI）の効率を高めます。
3. NVIDIA H100のようなAIアクセラレータの性能を比較する際、テラフロップス（TFLOPS）やペタフロップス（PFLOPS）単位の演算処理能力を基準にします。

### 関連用語 (Related Words)
* **スケーリング則 (Scaling Laws)**: コンピュートリソース、データサイズ、パラメータ数が増加するにつれて、モデルの性能が予測可能な形で向上するという法則です。
* **チンチラの法則 (Chinchilla Law)**: 与えられた演算量（FLOPs）の予算内で最適な性能を引き出すための、モデルパラメータ数とデータ量の適切な比率を定義した法則です。
* **コンピュートリソース (Compute)**: AIモデルの演算を処理するために投入されるハードウェアの処理能力、およびその総量を指します。