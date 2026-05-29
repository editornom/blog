---
title: 파일 디스크립터
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-29 15:43:58.422341+09:00
slug: file-descriptor
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 유닉스 계열 운영 체제에서 파일이나 소켓 등 입출력 자원에 접근하기 위해 사용하는 비음수 정수인 파일 디스크립터의 정의와 특징을
  알아봅니다. I/O 멀티플렉싱과 같은 실무 활용 사례를 통해 시스템 자원을 효율적으로 관리하는 원리를 상세히 설명합니다.
references: []
modDatetime: 2026-05-29 15:53:58.422341+09:00
---

# 파일 디스크립터이란?

### 사전적 정의 (Dictionary Definition)
유닉스 및 유닉스 계열 운영 체제에서 프로세스가 파일, 소켓, 파이프 등 다양한 입출력 자원에 접근하기 위해 사용하는 추상적인 비음수 정수(Non-negative Integer)입니다. 프로세스가 자원을 열 때 커널에 의해 할당되며, 해당 프로세스의 파일 디스크립터 테이블 내에서 특정 자원을 가리키는 인덱스 역할을 수행합니다.

### 실무 사용 예시 (Practical Use Case)
네트워크 서버 아키텍처에서 클라이언트 접속이 발생하면 운영 체제는 해당 소켓에 대한 파일 디스크립터를 생성합니다. C10K 문제 해결을 위한 I/O 멀티플렉싱 과정에서 select()나 poll()과 같은 함수는 다수의 파일 디스크립터를 인자로 전달받아 데이터 수신 여부를 감시하며, 실제 데이터가 도착한 파일 디스크립터만을 선별하여 처리함으로써 시스템 자원을 효율적으로 관리합니다.

### 관련 단어 (Related Words)
- 소켓(Socket)
- I/O 멀티플렉싱(I/O Multiplexing)
- 커널(Kernel)