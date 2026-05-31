---
title: "cgroups"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-31 15:48:37.300383+09:00
slug: "cgroups"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "cgroups(control groups)は、プロセスグループのCPU、メモリなどのシステムリソースの使用を制限および隔離するLinuxカーネルの機能です。DockerやKubernetes環境でリソースの枯渇を防ぎ、システムの安定性を確保するcgroupsの定義と実務での活用事例について解説します。"
references: []
modDatetime: 2026-05-31 15:58:37.300383+09:00
---

# cgroupsとは？

### 辞書的定義 (Dictionary Definition)
cgroups（control groups）は、プロセスグループのシステムリソース（CPU、メモリ、ネットワーク帯域幅、ディスクI/Oなど）の使用を制限、隔離、および監視するために提供されるLinuxカーネルの機能です。システム管理者が特定のプロセス集合のリソース消費量を制御することで、システムの安定性を確保することを目的としています。

### 実務での活用事例 (Practical Use Case)
KubernetesやDocker環境において、特定のコンテナにメモリ制限（Limit）を設定することで、メモリリークが発生したコンテナがノード（Node）全体のリソースを枯渇させないように防ぐ「Out Of Memory (OOM) キラー」の管理手法などに活用されています。

### 関連用語 (Related Words)
* 名前空間（Namespaces）: プロセスごとにシステムリソースを隔離し、相互の可視性を制限する技術です。
* コンテナ仮想化（Container Virtualization）: ホストOSのカーネルを共有しながら、アプリケーションを隔離された環境で実行する技術です。
* Linuxカーネル（Linux Kernel）: ハードウェアリソースを管理し、プロセスの制御権を持つLinuxオペレーティングシステムの核心部です。