---
title: Parquet이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-06-01 12:26:58.572384+09:00
slug: what-is-parquet
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 아파치 Parquet은 대규모 데이터 분석에 최적화된 오픈 소스 열 지향(Columnar) 데이터 저장 포맷입니다. 높은 데이터
  압축률과 효율적인 쿼리 성능을 통해 데이터 웨어하우스 및 데이터 레이크 환경에서의 I/O 효율성을 극대화하는 Parquet의 특징을 소개합니다.
references: []
modDatetime: 2026-06-01 12:36:58.572384+09:00
---

# Parquet이란?

### 사전적 정의 (Dictionary Definition)
아파치 소프트웨어 재단에서 개발한 오픈 소스 열 지향(Columnar) 데이터 저장 포맷입니다. 데이터를 행(Row) 단위가 아닌 열(Column) 단위로 저장하여 데이터 웨어하우스나 데이터 레이크와 같은 대규모 데이터 분석 환경에서 쿼리 성능을 최적화하도록 설계되었습니다. 필요한 열만 선택적으로 읽어 들이는 프로젝션(Projection) 기능과 높은 데이터 압축률을 제공하여 저장 공간 절약 및 입출력(I/O) 효율성을 극대화합니다.

### 실무 사용 예시 (Practical Use Case)
데이터 처리 파이프라인에서 비효율적인 CSV 포맷을 대체하여 데이터 전송 및 저장 비용을 절감하는 데 주로 사용됩니다. 특히 DuckDB, Apache Spark, Presto와 같은 분석 엔진에서 대용량 데이터셋을 읽어올 때 Parquet의 효율적인 인코딩 방식을 활용하여 네트워크 대역폭 소비를 줄이고 쿼리 실행 속도를 비약적으로 향상시키는 표준 포맷으로 널리 활용됩니다.

### 관련 단어 (Related Words)
- 열 지향 저장소(Columnar Storage)
- 데이터 레이크(Data Lake)
- 아파치 아로(Apache Arrow)