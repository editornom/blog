---
title: "kprobeとは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-05 14:33:23.133915+09:00
slug: linux-kernel-kprobe-tracing-guide
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "kprobeは、Linuxカーネルの特定地点に動的なブレークポイントを設定し、システムの再起動なしにリアルタイムで動作を追跡・情報収集する軽量なメカニズムです。eBPFと結合してシステムコール監視、パフォーマンス分析、セキュリティ監査など、多様なカーネルレベルの観測作業において中心的な役割を果たします。"
references: []
modDatetime: 2026-05-05 14:43:23.133915+09:00
---

# kprobeとは？

### 辞書的定義 (Dictionary Definition)
kprobe（Kernel Probe）は、Linuxカーネルの特定の命令や関数が実行される地点に動的なブレークポイント（Breakpoint）を設定し、カーネルの動作を追跡して関連情報を収集できるようにする軽量なメカニズムです。ソースコードの修正やカーネルの再コンパイル、再起動を必要とせず、実行中のシステムのカーネル内部にプロブを設置することで、該当地点が呼び出された際に事前定義されたハンドラ関数が実行されるよう制御します。

### 실무 사용 예시 (Practical Use Case)
eBPF（extended Berkeley Packet Filter）と組み合わせることで、「ゼロ・インストルメンテーション」環境でのシステムコール（System Call）監視に広く利用されています。例えば、特定のプロセスがネットワークソケットを作成したり、ファイルシステムの特定領域に書き込み作業を行ったりする際、その作業を処理するカーネル関数にkprobeをアタッチし、引数や戻り値をリアルタイムで記録することで、セキュリティ監査の実施やパフォーマンスのボトルネックの特定に役立てられます。

### 関連用語 (Related Words)
* **eBPF (Extended Berkeley Packet Filter):** カーネルソースの修正なしにカーネルレベルでプログラムを実行可能にする技術であり、kprobeを主要な追跡手段として活用します。
* **uprobe (User Probe):** カーネル空間ではなく、ユーザ空間（User Space）アプリケーションの関数を追跡するためのメカニズムです。
* **Tracepoint:** カーネルソースコードに事前に定義された静的な追跡地点であり、kprobeよりもオーバーヘッドが少なく安定していますが、柔軟性は低くなります。
* **System Call:** ユーザ空間のプロセスがカーネルに対して特定のサービスを要求するためのインターフェースであり、kprobeの主な追跡対象となります。