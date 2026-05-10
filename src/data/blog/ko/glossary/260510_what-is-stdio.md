---
title: STDIO이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-10 17:03:53.759572+09:00
slug: what-is-stdio
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: STDIO(표준 입출력)의 개념과 MCP 환경에서의 실무 활용 사례를 통해 프로세스 간 통신(IPC)의 핵심 원리를 살펴봅니다.
  시스템의 표준 스트림을 활용해 별도의 네트워크 포트 없이도 안전하고 효율적인 데이터 교환을 구현하는 방법을 설명합니다.
references: []
modDatetime: 2026-05-10 17:13:53.759572+09:00
---

### STDIO이란?

#### 사전적 정의 (Dictionary Definition)
STDIO(Standard Input/Output)는 컴퓨터 운영체제에서 프로그램과 외부 환경 간의 데이터 교환을 처리하기 위해 기본적으로 연결되는 입출력 통로인 표준 스트림을 의미합니다. 일반적으로 표준 입력(stdin), 표준 출력(stdout), 표준 에러(stderr)의 세 가지 채널로 구성되며, 프로그램이 구체적인 하드웨어나 네트워크 설정에 구애받지 않고 데이터를 읽고 쓸 수 있도록 돕는 추상화된 인터페이스 역할을 수행합니다.

#### 실무 사용 예시 (Practical Use Case)
Model Context Protocol(MCP) 규격에서 로컬 환경에 설치된 클라이언트와 서버 프로세스가 통신할 때, 별도의 네트워크 포트를 개방하는 대신 시스템의 STDIO를 주요 전송 통로로 사용합니다. 이는 프로세스 간 직접적인 입출력을 통해 데이터 전송의 지연시간을 줄이고, 네트워크 계층을 통한 외부 접근 가능성을 원천 차단하여 로컬 환경에서의 보안성을 강화하는 데 활용됩니다.

#### 관련 단어 (Related Words)
- **IPC (Inter-Process Communication)**: 운영체제 내 프로세스들이 서로 데이터를 주고받는 메커니즘을 의미하며, STDIO는 그 중 가장 기본적인 통신 수단 중 하나입니다.
- **JSON-RPC**: STDIO 스트림을 통해 구조화된 명령과 응답을 주고받기 위해 사용되는 경량 원격 프로시저 호출 프로토콜입니다.
- **Standard Stream (표준 스트림)**: 시스템 터미널이나 입출력 장치와 프로그램 사이를 연결하는 데이터 흐름의 표준 모델을 통칭합니다.