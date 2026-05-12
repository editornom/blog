---
title: SRE이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-12 11:28:39.488100+09:00
slug: what-is-sre
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: SRE(사이트 신뢰성 공학)는 소프트웨어 공학 방법론을 시스템 운영에 적용하여 서비스의 안정성과 가용성을 극대화하는 실무 체계입니다.
  SLO와 에러 예산을 활용한 정량적 관리와 자동화의 핵심 개념을 통해 효율적인 IT 인프라 운영 전략을 살펴봅니다.
references: []
modDatetime: 2026-05-12 11:38:39.488100+09:00
---

# SRE이란?

## 사전적 정의 (Dictionary Definition)
SRE(Site Reliability Engineering, 사이트 신뢰성 공학)는 구글(Google)에서 창안한 시스템 운영 방식으로, 소프트웨어 공학적 방법론을 IT 인프라 및 운영 문제에 적용하는 실무 체계를 의미합니다. 시스템의 신뢰성, 가용성, 효율성을 보장하기 위해 자동화와 모니터링을 적극적으로 활용하며, 수동 작업인 토일(Toil)을 최소화하고 서비스 수준 목표(SLO)를 기반으로 시스템 안정성을 정량적으로 관리하는 것이 특징입니다.

## 실무 사용 예시 (Practical Use Case)
eBPF와 같은 보안 기술을 도입하는 과정에서 SRE는 보안 로직이 시스템 가용성에 미치는 부하를 측정하고 모니터링 체계를 구축합니다. 만약 보안 프로그램 배포 후 시스템 호출 처리 속도가 저하되어 미리 설정된 에러 예산(Error Budget)을 초과할 위험이 감지되면, SRE는 가용성 확보를 위해 배포를 중단하거나 성능 최적화 작업을 우선적으로 수행하도록 결정합니다.

## 관련 단어 (Related Words)
* <b>DevOps</b>: 소프트웨어 개발과 운영의 협업을 강조하는 문화적 철학으로, SRE는 이를 구체적인 공학적 기법으로 구현한 모델로 평가받습니다.
* <b>SLO (Service Level Objective)</b>: 서비스 제공자가 준수하고자 하는 성능 및 가용성에 대한 구체적인 목표치입니다.
* <b>Error Budget (에러 예산)</b>: SLO를 달성하기 위해 허용 가능한 시스템 불능 시간의 총량을 의미하며, 새로운 기능의 배포 여부를 결정하는 기준이 됩니다.