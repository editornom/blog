---
title: Thundering Herd이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 11:39:40.174633+09:00
slug: thundering-herd
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Thundering Herd refers to a performance degradation in distributed systems
  where multiple processes simultaneously wake up to compete for a single resource,
  causing excessive CPU waste and context switching. This post explores common causes
  like cache stampede and mutex contention, along with key strategies to maintain
  system stability.
references: []
modDatetime: 2026-05-29 11:49:40.174633+09:00
---

# Thundering Herd이란?

### 사전적 정의 (Dictionary Definition)
'천둥 치는 소 떼(Thundering Herd)' 문제란 컴퓨터 과학 및 분산 시스템에서 특정 이벤트가 발생했을 때 대기 중이던 수많은 프로세스나 스레드가 한꺼번에 깨어나 동일한 자원을 처리하려고 시도하면서 발생하는 성능 저하 현상을 의미합니다. 모든 요청이 자원을 획득하기 위해 경쟁하지만 실제로는 극소수 혹은 단 하나의 프로세스만 성공하고 나머지는 다시 대기 상태로 돌아가게 되는데, 이 과정에서 발생하는 과도한 컨텍스트 스위칭(Context Switching)과 CPU 자원 낭비가 시스템 전체의 가용성을 떨어뜨리는 것이 특징입니다.

### 실무 사용 예시 (Practical Use Case)
1. 캐시 폭풍(Cache Stampede): 높은 트래픽을 받는 특정 데이터의 캐시가 만료되는 순간, 수많은 클라이언트가 동시에 원본 데이터베이스(Origin DB)에 접근하여 응답을 요청함으로써 데이터베이스 서버가 마비되는 상황에서 주로 발생합니다.
2. 수동적 헤징(Hedged Requests) 부작용: 시스템 지연이 발생할 때 여러 개의 복제된 요청을 동시에 보내는 기법을 부주의하게 사용할 경우, 지연이 발생한 특정 백엔드 노드에 트래픽이 폭증하여 시스템이 회복 불가능한 상태에 빠지는 '자폭형 DoS' 현상이 이에 해당합니다.
3. 뮤텍스(Mutex) 경합: 공유 자원의 잠금이 해제될 때 이를 대기하던 모든 스레드가 동시에 깨어나 자원을 점유하려 시도하는 커널 수준의 스케줄링 부하 상황에서 나타납니다.

### 관련 단어 (Related Words)
- Request Coalescing (요청 병합)
- Cache Stampede (캐시 폭풍)
- Exponential Backoff (지수적 백오프)