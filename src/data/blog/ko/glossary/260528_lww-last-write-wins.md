---
title: LWW(Last-Write-Wins)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-28 15:44:09.776756+09:00
slug: lww-last-write-wins
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: LWW(Last-Write-Wins)는 분산 시스템에서 타임스탬프를 기준으로 최신 데이터를 채택하여 충돌을 해결하는 결정론적
  알고리즘입니다. NoSQL 데이터베이스에서 결과적 일관성을 달성하기 위한 핵심 전략으로 활용되며, 단순하고 빠른 데이터 처리가 가능하다는 장점이
  있습니다.
references: []
modDatetime: 2026-05-28 15:54:09.776756+09:00
---

# LWW(Last-Write-Wins)이란?

### 사전적 정의 (Dictionary Definition)
LWW(Last-Write-Wins)는 분산 컴퓨팅 및 분산 데이터베이스 시스템에서 발생하는 데이터 충돌을 해결하기 위한 결정론적 알고리즘입니다. 여러 노드에서 동일한 데이터에 대해 서로 다른 쓰기 요청이 발생할 경우, 각 요청에 부여된 타임스탬프(Timestamp)를 비교하여 가장 최근에 발생한 기록만을 최종 데이터로 채택하고 나머지 이전 기록들은 폐기하는 방식입니다. 구현이 단순하여 시스템 부하가 적고 빠른 처리가 가능하지만, 분산된 노드 간의 시계 동기화(Clock Synchronization) 오차나 동시 다발적인 요청 상황에서 유효한 데이터가 손실될 수 있는 '데이터 유실(Data Loss)' 위험을 수반합니다.

### 실무 사용 예시 (Practical Use Case)
Apache Cassandra, Amazon DynamoDB, Couchbase 등 가용성과 분절 용인(AP)을 중시하는 NoSQL 데이터베이스에서 결과적 일관성(Eventual Consistency)을 달성하기 위한 기본 전략으로 활용됩니다. 예를 들어, 서로 다른 지역의 서버 노드에서 동일한 사용자의 주소 정보가 거의 동시에 변경되었을 때, 시스템은 더 큰 타임스탬프 값을 가진 노드의 정보를 최종 주소로 갱신하여 모든 노드에 전파합니다.

### 관련 단어 (Related Words)
- CAP 정리 (CAP Theorem)
- 결과적 일관성 (Eventual Consistency)
- 충돌 해소 (Conflict Resolution)