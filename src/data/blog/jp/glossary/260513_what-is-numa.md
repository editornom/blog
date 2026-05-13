---
title: "NUMA (Non-Uniform Memory Access)とは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 11:36:42.093125+09:00
slug: "what-is-numa"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "NUMA（Non-Uniform Memory Access）は、マルチプロセッサシステムにおいてプロセッサの位置によってメモリへのアクセス速度が異なるアーキテクチャを指します。本記事では、NUMAの定義とともに、MPIアプリケーションなどの実務環境で発生し得るメモリ性能の低下問題について解説します。"
references: []
modDatetime: 2026-05-13 11:46:42.093125+09:00
---

# NUMA (Non-Uniform Memory Access)とは？

## 辞書的定義
NUMA（Non-Uniform Memory Access）は、マルチプロセッサシステムのアーキテクチャの一つであり、各プロセッサ（またはプロセッサグループ）が専用のローカルメモリを持ち、このローカルメモリにアクセスする際は高速ですが、他のプロセッサのローカルメモリ（リモートメモリ）にアクセスする際は相対的に低速になる方式です。これは、物理メモリが複数のソケットに分割して割り当てられる際に発生し、メモリへのアクセス速度が不均一（Non-Uniform）であることを特徴としています。

## 実務での使用例
NASAのハイパフォーマンス・コンピューティング（HECC）環境において、MPI（Message Passing Interface）ベースのアプリケーションが実行される際、NUMAアーキテクチャはページキャッシュの独占問題と相まって、メモリ枯渇（Memory Starvation）現象およびパフォーマンスの低下を引き起こすことがあります。特定のプロセスがローカルソケットのメモリを独占した場合、他のプロセスはデータ転送速度が著しく遅いリモートソケットのメモリにアクセスしなければならず、結果として計算効率全体が急激に低下するケースがあります。

## 関連用語
- ページキャッシュ (Page Cache)
- MPI (Message Passing Interface)
- Direct I/O