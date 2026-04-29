---
title: Stacked PRs이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-29 17:12:18.110264+09:00
slug: what-is-stacked-prs
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Stacked PRs는 대규모 기능을 논리적인 작은 단위로 세분화하여 계층적으로 관리함으로써 리뷰 효율과 개발 생산성을 극대화하는
  워크플로우 전략입니다. 하위 PR의 승인을 기다리지 않고 연속적인 작업이 가능한 Stacked PRs의 정의와 실무 적용 방법, 효율적인 관리
  팁을 소개합니다.
references: []
modDatetime: 2026-04-29 17:22:18.110264+09:00
---

### 사전적 정의 (Dictionary Definition)
Stacked PRs는 대규모 기능을 논리적으로 완결된 작은 단위로 세분화하여 여러 개의 풀 리퀘스트(Pull Request)를 계층적으로 쌓아 올리는 워크플로우 전략입니다. 하나의 거대한 기능 브랜치를 사용하는 대신, 각 변경 사항을 독립적인 브랜치로 분리하고 이를 순차적인 의존 관계로 연결합니다. 이 방식을 통해 개발자는 하위 PR이 승인되거나 병합되기를 기다리지 않고 상위 레이어의 작업을 지속할 수 있으며, 리뷰어는 작고 명확한 맥락의 코드를 검토함으로써 리뷰 효율을 극대화할 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
대규모 신규 기능을 개발할 때 이를 데이터베이스 스키마 수정, 비즈니스 로직 구현, API 엔드포인트 개발, UI 레이어 작업 등 4개의 논리적 단위로 나눕니다. 각 단계는 별도의 PR로 생성되며, 'API 엔드포인트' PR은 '비즈니스 로직' 브랜치 위에서 생성됩니다. 리뷰어는 각각의 PR을 독립적으로 검토하여 빠른 피드백을 전달하며, 개발자는 하위 단계의 리뷰가 진행되는 동안 UI 작업을 중단 없이 이어갑니다. 다만, 하위 PR이 스쿼시 머지(Squash Merge)될 경우 상위 브랜치들의 부모 커밋 해시가 변경되므로 리베이스(Rebase)를 통한 이력 재구성이 필요합니다.

### 관련 단어 (Related Words)
- **리베이스(Rebase)**: 브랜치의 베이스를 다른 커밋으로 재설정하여 커밋 이력을 정렬하는 Git 명령어이며, Stacked PRs의 정합성을 유지하는 핵심 도구입니다.
- **스쿼시 머지(Squash Merge)**: 여러 커밋을 하나의 커밋으로 합쳐서 병합하는 방식으로, Stacked PRs 구조에서는 상위 브랜치와의 연결을 끊어뜨리는 기술적 부채의 원인이 되기도 합니다.
- **피처 브랜치(Feature Branch)**: 하나의 전체 기능을 하나의 브랜치에서 관리하는 전통적인 방식으로, Stacked PRs와 대비되는 개념입니다.