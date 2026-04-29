---
title: TTP(Tactics, Techniques, and Procedures) 정의 및 사이버 보안 활용 가이드
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-28 09:10:00+09:00
slug: ttp-cybersecurity-guide
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: TTP(전술, 기법, 절차)는 사이버 공격자의 전략적 행동 패턴을 분석하여 단순 지표 이상의 위협 흐름을 파악하고 선제적 방어
  체계를 구축하는 데 필수적인 개념입니다. 공격자의 목적과 실행 방식을 체계화한 TTP의 정의부터 실무 활용 사례 및 MITRE ATT&CK 등
  관련 지식까지 상세히 알아보세요.
references: []
modDatetime: 2026-04-29 17:09:43.972005+09:00
---

# TTP이란?

## 사전적 정의 (Dictionary Definition)
TTP는 전술(Tactics), 기법(Techniques), 절차(Procedures)의 약어로, 사이버 보안 분야에서 공격자나 특정 위협 그룹이 공격을 수행할 때 나타내는 고유한 행동 양식과 전략적 패턴을 체계화한 개념입니다. 단순히 IP 주소나 파일 해시값 같은 단편적인 침해 지표(IoC)를 식별하는 것을 넘어, 공격자가 목표를 달성하기 위해 사용하는 논리적 흐름과 실행 구조를 분석하는 데 초점을 맞춥니다. '전술'은 공격의 상위 목적을, '기법'은 해당 목적을 달성하기 위한 구체적인 방법론을, '절차'는 기법을 실행에 옮기는 세부적인 단계별 과정을 의미합니다.

## 실무 사용 예시 (Practical Use Case)
보안 운영 센터(SOC) 및 위협 분석가들은 침해 사고 분석 시 공격자의 TTP를 식별하여 대응 전략을 수립합니다. 예를 들어, 에이전틱 사이버 보안 시스템은 로그 데이터를 정밀 분석하여 공격자의 TTP를 자율적으로 식별하며, 이를 기반으로 인프라 전반에 걸친 선제적 격리 조치를 수행합니다. 이는 단순히 위협 징후를 요약하는 수준을 넘어 공격자의 다음 행동을 예측하고 방어 체계를 최적화하는 데 활용됩니다.

## 관련 단어 (Related Words)
* IoC (Indicators of Compromise): 공격의 증거가 되는 IP, 도메인, 파일 해시 등 기술적 지표입니다.
* MITRE ATT&CK: 공격자의 전술 및 기법을 표준화하여 분류한 글로벌 지식 베이스 프레임워크입니다.
* Cyber Kill Chain: 사이버 공격이 발생하여 목표를 달성하기까지의 단계를 모델링한 개념입니다.