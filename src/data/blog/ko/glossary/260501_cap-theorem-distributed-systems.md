---
title: 'CAP 정리: 분산 시스템 설계의 핵심 원칙과 전략적 선택'
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-01 18:13:42.707068+09:00
slug: cap-theorem-distributed-systems
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: CAP 정리는 분산 시스템에서 일관성, 가용성, 분할 내성을 동시에 만족할 수 없다는 원칙으로, 비즈니스 목적에 따른 CP
  및 AP 모델 선택 기준을 제시합니다. 각 속성의 정의와 실무 활용 사례를 통해 분산 컴퓨팅 환경에서의 효율적인 시스템 설계 전략을 확인해 보세요.
references: []
modDatetime: 2026-05-01 18:23:42.707068+09:00
---

# CAP 정리이란?

## 사전적 정의 (Dictionary Definition)

CAP 정리는 분산 컴퓨팅 시스템에서 일관성(Consistency), 가용성(Availability), 분할 내성(Partition Tolerance)이라는 세 가지 속성을 동시에 모두 만족시키는 것이 이론적으로 불가능하다는 원칙입니다. 2000년 에릭 브루어(Eric Brewer)에 의해 제안되었으며, 네트워크 장애가 발생할 수 있는 분산 환경에서는 분할 내성(P)을 기본적으로 확보해야 하므로 설계자가 일관성(CP)과 가용성(AP) 중 하나를 비즈니스 목적에 따라 선택해야 함을 규정합니다.

## 실무 사용 예시 (Practical Use Case)

- **CP (Consistency + Partition Tolerance) 모델**: 데이터의 정확성과 무결성이 최우선인 금융 거래, 자산 관리, 재고 시스템 등에서 활용됩니다. 네트워크 분할 발생 시 데이터 불일치를 막기 위해 시스템은 응답을 거절하거나 지연시키며 일관성을 유지합니다. Google Spanner, MongoDB, ZooKeeper 등이 이에 해당합니다.
- **AP (Availability + Partition Tolerance) 모델**: 서비스의 중단 없는 응답과 사용자 경험이 중요한 소셜 미디어, 콘텐츠 스트리밍, 장바구니 시스템 등에서 활용됩니다. 네트워크 장애 시 일부 데이터가 최신 상태가 아니더라도 가용한 노드에서 즉시 응답을 제공하여 서비스의 연속성을 보장합니다. Apache Cassandra, Amazon DynamoDB 등이 대표적입니다.

## 관련 단어 (Related Words)

- 일관성 (Consistency)
- 가용성 (Availability)
- 분할 내성 (Partition Tolerance)
- PACELC 정리