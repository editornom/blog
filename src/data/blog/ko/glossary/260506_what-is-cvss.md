---
title: CVSS이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-06 11:25:09.238064+09:00
slug: what-is-cvss
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: CVSS(공통 취약점 점수 시스템)는 보안 취약점의 심각도를 0.0에서 10.0 사이의 점수로 평가하여 대응 우선순위를 결정하는
  표준화된 프레임워크입니다. 이 시스템을 통해 보안 결함의 위험 수준을 객관적으로 분석하고 효율적인 보안 패치 전략을 수립하는 방법을 확인해 보세요.
references: []
modDatetime: 2026-05-06 11:35:09.238064+09:00
---

# CVSS이란?

### 사전적 정의 (Dictionary Definition)
공통 취약점 점수 시스템(Common Vulnerability Scoring System, CVSS)은 정보 보안 취약점의 심각도를 평가하기 위해 설계된 표준화된 개방형 프레임워크입니다. 취약점이 지닌 기술적 특성을 수치화하여 0.0에서 10.0 사이의 점수를 부여하며, 이를 통해 조직은 발견된 보안 결함의 위험 수준을 객관적으로 비교하고 보안 패치 및 대응의 우선순위를 정량적으로 결정할 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
보안 운영팀은 CVE-2026-31431(Copy Fail) 취약점에 대응할 때 CVSS 3.1 Base Score인 7.8(High) 점수를 참고합니다. 해당 점수가 고위험군에 속함을 인지하고, 공격 벡터(AV)가 로컬(L)임에도 불구하고 컨테이너 탈출이 가능하다는 기술적 상세 내용을 결합하여 클라우드 인프라 내 리눅스 커널 패치를 최우선 과제로 선정하는 판단 근거로 활용합니다.

### 관련 단어 (Related Words)
* CVE (Common Vulnerabilities and Exposures): 보안 취약점에 부여되는 고유한 표준 식별자 목록입니다.
* CWE (Common Weakness Enumeration): 소프트웨어 취약점을 유발하는 근본적인 약점을 유형별로 분류한 체계입니다.
* NVD (National Vulnerability Database): CVSS 점수 산출 및 취약점 분석 정보를 제공하는 미국 정부의 국가 취약점 데이터베이스입니다.