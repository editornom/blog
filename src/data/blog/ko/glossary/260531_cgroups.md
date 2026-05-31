---
title: cgroups
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-31 15:48:37.300383+09:00
slug: cgroups
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: cgroups(control groups)는 프로세스 그룹의 CPU, 메모리 등 시스템 자원 사용을 제한하고 격리하는 리눅스
  커널 기능입니다. 도커와 쿠버네티스 환경에서 자원 고갈을 방지하고 시스템 안정성을 확보하는 cgroups의 정의와 실무 활용 사례를 알아봅니다.
references: []
modDatetime: 2026-05-31 15:58:37.300383+09:00
---

# cgroups이란?

### 사전적 정의 (Dictionary Definition)
cgroups(control groups)는 프로세스 그룹의 시스템 자원(CPU, 메모리, 네트워크 대역폭, 디스크 I/O 등) 사용을 제한, 격리 및 모니터링하기 위해 제공되는 리눅스 커널의 기능입니다. 시스템 관리자가 특정 프로세스 집합의 자원 소모량을 제어함으로써 시스템의 안정성을 확보하는 데 목적이 있습니다.

### 실무 사용 예시 (Practical Use Case)
쿠버네티스(Kubernetes)나 도커(Docker) 환경에서 특정 컨테이너에 메모리 제한(Limit)을 설정하여, 메모리 누수가 발생한 컨테이너가 전체 노드(Node)의 자원을 고갈시키지 않도록 방지하는 'Out Of Memory(OOM) 킬러' 관리 기법 등에 활용됩니다.

### 관련 단어 (Related Words)
* 네임스페이스(Namespaces): 프로세스별로 시스템 리소스를 격리하여 서로의 가시성을 제한하는 기술입니다.
* 컨테이너 가상화(Container Virtualization): 호스트 운영체제의 커널을 공유하며 애플리케이션을 격리된 환경에서 실행하는 기술입니다.
* 리눅스 커널(Linux Kernel): 하드웨어 자원을 관리하고 프로세스 제어권을 가지는 리눅스 운영체제의 핵심부입니다.