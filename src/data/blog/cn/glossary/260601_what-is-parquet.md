---
title: "什么是 Parquet？"
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-06-01 12:26:58.572384+09:00
slug: "what-is-parquet"
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: "Apache Parquet 是一种专为大规模数据分析优化的开源列式（Columnar）数据存储格式。本文介绍 Parquet 的特点，它通过高数据压缩率和高效的查询性能，最大限度地提高数据仓库及数据湖环境下的 I/O 效率。"
references: []
modDatetime: 2026-06-01 12:36:58.572384+09:00
---

# 什么是 Parquet？

### 定义 (Definition)
由 Apache 软件基金会开发的开源列式（Columnar）数据存储格式。它采用按列而非按行存储数据的方式，旨在优化数据仓库和数据湖等大规模数据分析环境中的查询性能。Parquet 提供仅选择性读取所需列的投影（Projection）功能和极高的数据压缩率，能够最大限度地节省存储空间并提高输入/输出（I/O）效率。

### 实际应用场景 (Practical Use Case)
在数据处理流水线中，Parquet 主要用于替代低效的 CSV 格式，以显著降低数据传输和存储成本。特别是在使用 DuckDB、Apache Spark 和 Presto 等分析引擎读取大规模数据集时，利用 Parquet 高效的编码方式可以减少网络带宽消耗，并大幅提升查询执行速度，是目前业界广泛采用的标准存储格式。

### 相关词汇 (Related Words)
- 列式存储 (Columnar Storage)
- 数据湖 (Data Lake)
- Apache Arrow