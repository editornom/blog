---
title: Bare 리포지토리 (Bare Repository)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-15 15:22:39.054299+09:00
slug: bare-repository
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Bare 리포지토리는 워킹 디렉터리가 없는 Git 저장소로, 주로 협업을 위한 중앙 원격 저장소 및 데이터 백업 용도로 사용됩니다.
  Git 메타데이터만으로 구성되어 데이터의 무결성을 유지하며 효율적인 소스 코드 관리를 지원합니다.
references: []
modDatetime: 2026-05-15 15:32:39.054299+09:00
---

# Bare 리포지토리이란?

### 사전적 정의 (Dictionary Definition)
Bare 리포지토리(Bare Repository)는 소스 코드의 실제 수정 및 편집이 이루어지는 워킹 디렉터리(Working Directory)가 없는 Git 저장소 형식을 의미합니다. 일반적인 Git 저장소가 소스 파일과 함께 버전 관리 메타데이터가 담긴 .git 디렉터리를 포함하는 것과 달리, Bare 리포지토리는 .git 디렉터리의 내용물만으로 구성됩니다. 작업 공간인 워킹 트리가 존재하지 않으므로 저장소 내에서 직접 파일을 수정하거나 커밋하는 작업이 불가능하며, 주로 협업을 위한 중앙 서버나 데이터의 안전한 공유 및 백업을 위한 용도로 사용됩니다.

### 실무 사용 예시 (Practical Use Case)
Bare 리포지토리는 주로 GitHub, GitLab 또는 기업 내부 서버에서 중앙 원격 저장소를 구축할 때 사용됩니다. 개발자들은 로컬 리포지토리에서 작업을 마친 후 push 명령어를 통해 변경 사항을 이 Bare 리포지토리로 전송합니다. 최근 Git 2.54 업데이트에서는 인덱스 과정을 거치지 않고도 Bare 리포지토리 내에서 직접 객체 데이터를 조작할 수 있는 기능이 포함되어, 워킹 트리가 없는 환경에서도 정교한 히스토리 수정과 데이터 관리가 가능해졌습니다.

### 관련 단어 (Related Words)
1. 워킹 트리 (Working Tree): 개발자가 실제로 파일을 수정하고 프로젝트 작업을 수행하는 영역입니다.
2. 리모트 리포지토리 (Remote Repository): 네트워크상에 위치한 원격 저장소로, 대개 Bare 리포지토리 형식으로 운영됩니다.
3. 데이터 정합성 (Data Integrity): 데이터의 무결성과 추적 가능성을 의미하며, Bare 리포지토리는 중앙 관리를 통해 이 정합성을 유지하는 핵심 역할을 합니다.