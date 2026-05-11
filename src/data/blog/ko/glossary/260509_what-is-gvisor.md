---
title: gVisor이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 16:51:26.458171+09:00
slug: what-is-gvisor
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: gVisor는 독자적인 사용자 공간 커널을 통해 시스템 콜을 제어함으로써 호스트와 컨테이너 간의 강력한 보안 격리를 제공하는
  오픈 소스 샌드박스 런타임입니다. GKE 등에서 신뢰할 수 없는 외부 워크로드를 안전하게 실행하고 호스트 시스템 침입을 방지하기 위한 핵심적인
  보안 솔루션으로 활용됩니다.
references: []
modDatetime: 2026-05-09 17:01:26.458171+09:00
---### 사전적 정의 (Dictionary Definition)
gVisor는 구글(Google)에서 개발한 오픈 소스 기반의 컨테이너 런타임 샌드박스입니다. 이 기술은 애플리케이션과 호스트 운영체제 커널 사이에서 시스템 콜(System Call)을 가로채고 처리하는 독자적인 사용자 공간 커널(User-space kernel)을 제공합니다. 기존 리눅스 컨테이너가 호스트 커널을 공유함으로써 발생할 수 있는 보안 취약점을 보완하며, 강력한 보안 격리 환경을 구축하는 데 목적이 있습니다.

### 실무 사용 예시 (Practical Use Case)
GKE(Google Kubernetes Engine) Agent Sandbox 환경에서 신뢰할 수 없는 외부 코드를 실행해야 하는 AI 에이전트 워크로드를 보호하기 위해 활용됩니다. 보안성이 낮은 제3자 응용 프로그램을 실행할 때 시스템 콜을 제어하여 호스트 시스템으로의 침입을 방지하는 격리 계층으로 사용되나, 이 과정에서 발생하는 시스템 콜 오버헤드로 인해 고성능 추론 작업 시 지연 시간이 발생할 수 있습니다.

### 관련 단어 (Related Words)
* 컨테이너 런타임(Container Runtime)
* 샌드박스(Sandbox)
* 시스템 콜(System Call)
