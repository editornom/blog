---
title: 분산 트레이싱
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-22 11:44:59.981016+09:00
slug: distributed-tracing
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 분산 트레이싱은 MSA 및 서버리스 환경에서 요청의 전체 경로를 추적하여 시스템의 관찰 가능성을 확보하는 모니터링 기법입니다.
  서비스 간 호출 관계와 처리 시간을 시각화해 성능 병목 현상이나 오류 발생 지점을 신속하게 파악하고 해결할 수 있습니다.
references: []
modDatetime: 2026-05-22 11:54:59.981016+09:00
---

# 분산 트레이싱이란?

### 사전적 정의 (Dictionary Definition)
분산 트레이싱(Distributed Tracing)은 마이크로서비스 아키텍처(MSA)나 서버리스 환경과 같이 분산된 시스템 구조에서 하나의 요청이 거치는 모든 경로를 추적하고 기록하는 모니터링 기법입니다. 각 서비스 간의 호출 관계와 처리 시간을 시각화하여 시스템 전체의 관찰 가능성(Observability)을 확보하고, 성능 병목 현상이나 오류가 발생한 지점을 정확히 파악하는 데 사용됩니다.

### 실무 사용 예시 (Practical Use Case)
복잡하게 연결된 서버리스 마이크로서비스 환경에서 특정 API의 응답 속도가 평소보다 느려졌을 때, 분산 트레이싱 도구를 활용하여 어느 단계의 함수(Function)나 데이터베이스 호출에서 지연이 발생하는지 실시간으로 확인하고 조치합니다.

### 관련 단어 (Related Words)
* 관찰 가능성 (Observability)
* 마이크로서비스 아키텍처 (MSA)
* 벤더 락인 (Vendor Lock-in)