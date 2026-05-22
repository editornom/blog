---
title: SVN이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-22 15:38:55.434356+09:00
slug: what-is-svn
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: SVN(Subversion)은 중앙 서버에서 소스 코드의 변경 이력을 통합 관리하는 대표적인 중앙 집중식 버전 관리 시스템(CVCS)입니다.
  Git과의 차이점부터 보안이 중요한 기업 환경에서의 실무 활용 사례까지 SVN의 핵심 개념을 상세히 설명합니다.
references: []
modDatetime: 2026-05-22 15:48:55.434356+09:00
---

# SVN이란?

### 사전적 정의 (Dictionary Definition)
SVN(Subversion)은 소프트웨어 개발 과정에서 소스 코드의 변경 사항을 추적하고 관리하는 중앙 집중식 버전 관리 시스템(Centralized Version Control System, CVCS)입니다. 아파치 소프트웨어 재단에서 오픈 소스로 개발 및 유지보수하며, 모든 프로젝트 데이터와 변경 이력이 중앙 서버에 저장되는 구조를 가집니다. 사용자는 중앙 저장소에서 최신 코드를 내려받아(Checkout) 수정하고, 변경된 내용을 다시 서버에 반영(Commit)함으로써 협업을 진행합니다. 분산 버전 관리 시스템(DVCS)인 Git과 달리, 작업 시 중앙 서버와의 연결이 필수적이며 로컬 환경에는 전체 히스토리가 아닌 현재 작업 중인 스냅샷 위주로 관리되는 것이 특징입니다.

### 실무 사용 예시 (Practical Use Case)
코드 보안 및 통제가 엄격한 기업 환경에서 소스 코드를 단일 지점에 집중하여 관리하고자 할 때 활용됩니다. 특히 대규모 바이너리 파일이 포함된 프로젝트나 전체 소스 코드 히스토리를 개별 개발자의 로컬 환경에 모두 복제할 필요가 없는 구조에서 서버 저장 공간을 효율적으로 사용하기 위해 도입됩니다.

### 관련 단어 (Related Words)
- **CVCS (Centralized Version Control System)**: 모든 소스 코드와 이력을 중앙의 한 서버에서 통합 관리하는 방식입니다.
- **Git**: SVN의 중앙 집중 방식과 대조되는 개념인 분산 버전 관리 시스템(DVCS)으로, 현재 업계 표준으로 널리 사용됩니다.
- **Repository (저장소)**: 소스 코드의 현재 상태와 모든 변경 이력이 저장되는 물리적 공간을 의미합니다.