---
title: Confused Deputy
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 18:48:35.245929+09:00
slug: confused-deputy
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Confused Deputy는 권한을 가진 대리인이 낮은 권한의 요청을 검증 없이 수행하여 발생하는 보안 취약점으로, 권한
  오남용과 데이터 유출의 주요 원인이 됩니다. AI 에이전트 환경에서 발생할 수 있는 간접 프롬프트 인젝션 등 관련 위험성과 보안 대책에 대해 설명합니다.
references: []
modDatetime: 2026-05-29 18:58:35.245929+09:00
---

# Confused Deputy이란?\n\n### 사전적 정의 (Dictionary Definition)\n권한을 가진 대리인(Deputy)이 자신에게 부여된 특권을 적절한 검증 없이 사용하여, 권한이 낮은 개체의 요청을 대신 수행함으로써 발생하는 보안 취약점입니다. 시스템이 요청자의 권한이 아닌 대리인 자신의 권한을 기준으로 작업을 승인할 때 발생하며, 이는 권한 오남용 및 데이터 유출의 주요 원인이 됩니다.\n\n### 실무 사용 예시 (Practical Use Case)\nModel Context Protocol(MCP) 기반의 AI 에이전트가 사용자의 명령에 따라 이메일을 전송하거나 파일을 수정할 때, 해당 명령이 보안 정책에 위배되는지 확인하지 않고 에이전트의 시스템 권한으로 즉시 실행하는 경우가 이에 해당합니다.\n\n### 관련 단어 (Related Words)\n권한 상승(Privilege Escalation), 간접 프롬프트 인젝션(Indirect Prompt Injection), 접근 제어(Access Control)