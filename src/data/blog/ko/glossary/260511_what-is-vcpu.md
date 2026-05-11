---
title: vCPU이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 11:36:06.856378+09:00
slug: what-is-vcpu
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: vCPU(가상 중앙 처리 장치)의 정의와 물리적 CPU 자원을 가상 머신에 할당하는 원리 및 클라우드 환경에서의 실무 활용
  사례를 설명합니다. 하이퍼바이저를 통해 연산 능력을 효율적으로 관리하고 인스턴스 성능을 최적화하는 핵심 지표를 확인해 보세요.
references: []
modDatetime: 2026-05-11 11:46:06.856378+09:00
---

# vCPU이란?

## 사전적 정의 (Dictionary Definition)
vCPU(Virtual Central Processing Unit)는 가상화된 컴퓨팅 환경에서 가상 머신(VM)에 할당되는 논리적인 연산 단위를 의미합니다. 물리적 프로세서(pCPU)의 자원을 하이퍼바이저(Hypervisor)를 통해 추상화하여 제공하며, 일반적으로 하드웨어의 물리 코어 또는 하이퍼스레딩(Hyper-threading) 기술이 적용된 논리 스레드와 대응됩니다.

## 실무 사용 예시 (Practical Use Case)
클라우드 서비스 이용 시 인스턴스의 성능을 결정하는 핵심 지표로 활용됩니다. 예를 들어, MySQL 데이터베이스를 클라우드 환경(AWS RDS 등)에 구축할 때 워크로드의 복잡도와 처리량에 맞춰 vCPU 개수를 선택하여 연산 능력을 확장하거나 제한합니다.

## 관련 단어 (Related Words)
하이퍼바이저(Hypervisor), 물리적 CPU(Physical CPU), 인스턴스(Instance)