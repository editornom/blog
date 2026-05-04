---
title: AI DoS (AI Denial of Service)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-04 17:44:25.150003+09:00
slug: ai-denial-of-service
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: AI DoS(인공지능 서비스 거부)는 AI 모델의 설계적 취약점을 악용해 시스템 자원을 고갈시키고 서비스 제공을 중단시키는
  공격 방식입니다. 프롬프트 인젝션을 통한 자원 소진 및 API 할당량 고갈 등 AI DoS의 정의와 주요 사례를 통해 보안 위협을 확인하세요.
references: []
modDatetime: 2026-05-04 17:54:25.150003+09:00
---

# AI DoS이란?

### 사전적 정의 (Dictionary Definition)
AI DoS(AI Denial of Service, 인공지능 서비스 거부)는 인공지능 모델이나 관련 인프라의 설계적 취약점을 악용하여 시스템 자원을 고갈시키거나 서비스 제공을 중단시키는 공격 방식입니다. 이는 LLM(대규모 언어 모델)이 입력 데이터와 명령어를 명확히 구분하지 못하는 '입력 데이터와 명령어 분리 실패(Command/Data separation failure)' 현상을 이용하는 경우가 많습니다. 공격자는 특정 문자열이나 복잡한 프롬프트를 통해 모델이 무한 루프에 빠지게 하거나, 과도한 추론 비용을 발생시켜 사용자의 API 쿼터(Quota)를 즉각적으로 소진시킴으로써 정상적인 서비스 이용을 방해합니다.

### 실무 사용 예시 (Practical Use Case)
최근 AI 코딩 어시스턴트인 '클로드 코드(Claude Code)' 환경에서 특정 메타데이터(예: OpenClaw 관련 문자열)가 포함된 소스 코드를 읽어 들일 때, 이를 시스템 명령어로 오인하여 프롬프트 인젝션이 발생하는 사례가 보고되었습니다. 이 과정에서 사용자의 의도와 상관없이 AI 모델이 비정상적인 연산을 반복하며 클로드 프로 요금제의 할당량을 순식간에 100% 소진시키고 세션을 종료시키는 AI DoS 상태를 유발하는 것으로 확인되었습니다.

### 관련 단어 (Related Words)
- 프롬프트 인젝션(Prompt Injection)
- 자원 고갈 공격(Resource Exhaustion)
- 아키텍처 결함(Architectural Flaw)