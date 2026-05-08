---
title: AF_ALG이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 11:30:06.736176+09:00
slug: what-is-af-alg
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: AF_ALG is a Linux kernel interface that allows user-space applications
  to access cryptographic algorithms and hardware acceleration through the standard
  socket API. This overview covers its technical implementation, practical usage with
  system calls like splice(), and its relevance to security vulnerabilities such as
  CVE-2026-31431.
references: []
modDatetime: 2026-05-08 11:40:06.736176+09:00
---

## AF_ALG이란?

### 사전적 정의 (Dictionary Definition)
AF_ALG는 리눅스 커널(Linux Kernel)에서 제공하는 암호화 서브시스템에 접근하기 위한 사용자 공간(User-space) 인터페이스입니다. 'Address Family - Algorithm'의 약칭이며, 사용자 공간의 애플리케이션이 표준 소켓 API(Socket API)를 통해 커널 내부에 구현된 암호화 알고리즘(AES, SHA, HMAC 등)을 직접 호출하고 활용할 수 있도록 설계된 통로입니다. 하드웨어 가속기 등 커널 수준의 자원을 활용하여 효율적인 암호화 연산을 수행할 수 있게 지원합니다.

### 실무 사용 예시 (Practical Use Case)
- **커널 암호화 엔진 호출**: 사용자 공간 프로그램이 커널의 암호화 모듈을 사용하여 데이터를 처리할 때 소켓을 생성하고 bind() 및 accept()를 통해 특정 알고리즘에 연결하여 사용합니다.
- **시스템 콜과의 상호작용**: splice() 시스템 콜과 결합하여 데이터 복사 과정을 최적화하거나 암호화된 데이터를 처리하는 데 활용됩니다. 최근에는 이 과정에서의 설계 결함을 악용한 CVE-2026-31431(Copy Fail) 취약점 사례처럼, AF_ALG와 splice()의 상호작용을 통한 권한 상승 공격의 연구 대상으로 분석되기도 합니다.

### 관련 단어 (Related Words)
- CVE-2026-31431 (Copy Fail)
- splice() 시스템 콜
- 리눅스 커널 암호화 API (Crypto API)
- 페이지 캐시 오염 (Page Cache Corruption)