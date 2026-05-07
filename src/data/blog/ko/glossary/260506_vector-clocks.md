---
title: Vector Clocks
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-06 14:49:27.272957+09:00
slug: vector-clocks
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 분산 시스템에서 이벤트 간 인과 관계를 추적하고 데이터 충돌을 감지하는 벡터 클락(Vector Clocks)의 정의와 실무
  활용 사례를 소개합니다. Amazon DynamoDB와 같은 NoSQL 데이터베이스에서 데이터 일관성을 유지하기 위해 사용하는 핵심 알고리즘을
  확인해 보세요.
references: []
modDatetime: 2026-05-06 14:59:27.272957+09:00
---

# Vector Clocks이란?

### 사전적 정의 (Dictionary Definition)
분산 컴퓨팅 환경에서 이벤트 간의 인과 관계(Causality)를 추적하고 논리적인 선후 관계를 결정하기 위해 사용하는 알고리즘입니다. 각 노드가 시스템 내 모든 노드의 논리적 시간 정보를 벡터(배열) 형태로 유지하며, 데이터 업데이트나 메시지 교환 시 이 벡터 값을 갱신하고 공유합니다. 이를 통해 특정 이벤트가 다른 이벤트보다 먼저 발생했는지, 혹은 두 이벤트가 인과 관계없이 동시에(Concurrent) 발생했는지를 판별할 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
Amazon DynamoDB나 Riak과 같은 분산 키-값 저장소(NoSQL)에서 데이터의 일관성을 유지하고 쓰기 충돌을 감지하는 데 사용됩니다. 예를 들어, 네트워크 파티션으로 인해 서로 다른 노드에서 동일한 데이터에 대한 수정이 동시에 일어날 경우, 각 노드는 자신의 벡터 클락을 업데이트합니다. 이후 시스템이 복구되어 데이터를 병합할 때 벡터 클락의 상태를 비교하여 버전 간의 선후 관계를 확인하거나, 충돌이 발생했음을 사용자에게 알려 수동으로 병합하도록 유도합니다.

### 관련 단어 (Related Words)
- 논리적 시계 (Logical Clocks)
- 램포트 시계 (Lamport Clocks)
- 최종 일관성 (Eventual Consistency)