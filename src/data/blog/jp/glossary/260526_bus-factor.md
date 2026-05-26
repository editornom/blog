---
title: "バス係数（Bus Factor）とは？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-26 15:35:45.158948+09:00
slug: "bus-factor"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "バス係数（Bus Factor）の定義と、プロジェクト内の知識集中によるリスク管理策を紹介します。特定の個人への依存度を下げ、チームの回復力を高めるための知識共有およびドキュメント化戦略を確認しましょう。"
references: []
modDatetime: 2026-05-26 15:45:45.158948+09:00
---

# バス係数（Bus Factor）とは？

### 辞書的定義 (Dictionary Definition)
バス係数（Bus Factor）は、特定のプロジェクトや組織において、知識や能力が少数のメンバーにどれだけ集中しているかを示す指標です。これは「プロジェクトの運営が中断されないためには、最低何人のチームメンバーが突然離脱（例：バスに跳ねられる）しなければならないか」を問う概念的な数値です。指数が低いほど（例：1）、特定の個人への依存度が高くリスクが大きいことを意味し、指数が高いほど知識共有が円滑に行われており、チームの回復力（レジリエンス）が高いことを示します。

### 実務での活用事例 (Practical Use Case)
Rustのように学習曲線が急峻な技術を導入する場合、その言語に精通した極少数の開発者だけがコードを理解し、管理できる状況に陥りやすくなります。この場合、バス係数は1に収束し、該当する開発者の不在時にプロジェクト全体が停止するリスクが高まります。そのため、テクニカルリーダーはコードレビューやドキュメント化、継続的な教育を通じて知識のサイロ化（情報の断絶）を防ぎ、バス係数を高めることで経営リスクを管理する必要があります。

### 関連用語 (Related Words)
- トラック係数 (Truck Factor)
- 知識のサイロ化 (Knowledge Silo)
- 人的リソースリスク (Human Resource Risk)