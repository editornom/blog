---
title: NUMA (Non-Uniform Memory Access)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 11:36:42.093125+09:00
slug: what-is-numa
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: NUMA(Non-Uniform Memory Access)는 멀티프로세서 시스템에서 프로세서 위치에 따라 메모리 접근 속도가
  달라지는 아키텍처를 의미합니다. 본 포스팅에서는 NUMA의 정의와 함께 MPI 애플리케이션 등 실무 환경에서 발생할 수 있는 메모리 성능 저하
  이슈를 분석합니다.
references: []
modDatetime: 2026-05-13 11:46:42.093125+09:00
---

# NUMA (Non-Uniform Memory Access)이란?

## 사전적 정의
NUMA(Non-Uniform Memory Access)는 멀티프로세서 시스템 아키텍처 중 하나로, 각 프로세서(또는 프로세서 그룹)가 전용 로컬 메모리를 가지며, 이 로컬 메모리에 접근할 때는 빠르게 접근하지만 다른 프로세서의 로컬 메모리(원격 메모리)에 접근할 때는 상대적으로 느린 접근 속도를 보이는 방식입니다. 이는 물리적 메모리가 여러 소켓에 분할되어 할당될 때 발생하며, 메모리 접근 속도의 비균일성을 특징으로 합니다.

## 실무 사용 예시
NASA의 고성능 컴퓨팅(HECC) 환경에서 MPI(Message Passing Interface) 기반 애플리케이션이 실행될 때, NUMA 아키텍처는 페이지 캐시 독점 문제와 결합하여 메모리 기아 현상 및 성능 저하를 야기합니다. 특정 프로세스가 로컬 소켓의 메모리를 독점할 경우, 다른 프로세스들은 데이터 전송 속도가 현저히 느린 원격 소켓의 메모리에 접근해야 하므로 전체 계산 효율이 급격히 감소하는 사례가 있습니다.

## 관련 단어
- 페이지 캐시 (Page Cache)
- MPI (Message Passing Interface)
- Direct I/O