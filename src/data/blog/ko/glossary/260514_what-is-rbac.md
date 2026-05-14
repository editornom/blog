---
title: RBAC이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-14 17:32:53.429057+09:00
slug: what-is-rbac
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: RBAC(역할 기반 접근 제어)의 정의와 보안 관리의 효율성을 높이는 실무 활용 사례를 살펴봅니다. 특히 AI 에이전트 거버넌스와
  시스템 리스크 통제를 위한 핵심 보안 모델로서의 RBAC 개념을 상세히 설명합니다.
references: []
modDatetime: 2026-05-14 17:42:53.429057+09:00
---

# RBAC이란?

## 사전적 정의 (Dictionary Definition)
Role-Based Access Control (RBAC)은 사용자 개인의 ID가 아닌 조직 내에서 맡고 있는 '역할(Role)'을 기준으로 시스템 리소스에 대한 접근 권한을 관리하는 방식입니다. 각 역할에 필요한 최소한의 권한 집합을 미리 정의하고 사용자를 해당 역할에 할당함으로써, 보안 관리의 복잡성을 줄이고 권한 남용을 방지하는 보안 모델입니다.

## 실무 사용 예시 (Practical Use Case)
에이전틱 AI 기반의 레거시 현대화 아키텍처에서 AI 에이전트에게 '데이터 조회자' 역할을 부여하여 읽기 전용 API만 호출할 수 있도록 제한함으로써, 자율형 에이전트가 의도치 않게 시스템 설정을 변경하거나 데이터를 삭제하는 리스크를 통제하는 거버넌스 수단으로 활용됩니다.

## 관련 단어 (Related Words)
- ABAC (Attribute-Based Access Control)
- ACL (Access Control List)
- IAM (Identity and Access Management)