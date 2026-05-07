---
title: CRD이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 11:29:40.487351+09:00
slug: what-is-crd
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: CRD(Custom Resource Definition)는 쿠버네티스 API를 확장하여 기본 리소스 외에 사용자 고유의 객체
  유형을 정의하고 관리할 수 있게 해주는 표준 메커니즘입니다. 오퍼레이터 패턴이나 Gateway API와 같이 특정 애플리케이션 요구사항에 최적화된
  리소스를 생성하고 운영을 자동화하는 데 필수적으로 사용됩니다.
references: []
modDatetime: 2026-05-07 11:39:40.487351+09:00
---

# CRD이란?

### 사전적 정의 (Dictionary Definition)
사용자 정의 리소스 정의(Custom Resource Definition, CRD)는 쿠버네티스 API를 확장하기 위한 표준 메커니즘으로, 사용자가 기본으로 제공되는 리소스(Pod, Service 등) 외에 고유한 객체 유형을 정의하고 클러스터에 추가할 수 있도록 지원하는 기능입니다. 이를 통해 개발자나 운영자는 특정 애플리케이션의 요구사항에 맞는 커스텀 리소스를 생성하고, 쿠버네티스 API 서버를 통해 이를 표준 리소스와 동일하게 관리할 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
쿠버네티스 Gateway API는 기존 Ingress의 한계를 극복하기 위해 GatewayClass, Gateway, HTTPRoute와 같은 리소스를 CRD 형태로 정의하여 배포합니다. 또한 데이터베이스 관리나 자동화된 백업과 같이 복잡한 운영 로직을 처리하는 오퍼레이터(Operator) 패턴에서 애플리케이션의 상태를 정의하고 제어하기 위한 데이터 규격으로 필수적으로 사용됩니다.

### 관련 단어 (Related Words)
- Custom Resource (CR)
- Operator Pattern
- Kubernetes API Server
- Gateway API