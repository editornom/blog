---
title: 'JSON-RPC 2.0: 원격 프로시저 호출의 표준 규격'
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-04-25 09:10:00+09:00
slug: json-rpc-2-0-standard-specification
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: JSON-RPC 2.0은 JSON 기반의 경량 원격 프로시저 호출(RPC) 프로토콜로, 상태 비저장 방식의 효율적인 데이터
  교환과 배치 처리를 지원합니다. 앤스로픽의 MCP 등 AI 모델과 데이터 간의 실시간 상호작용을 위한 표준 규약으로 활용되는 JSON-RPC 2.0의
  정의와 실무 사례를 소개합니다.
references: []
modDatetime: 2026-04-28 15:14:18.960187+09:00
---

# JSON-RPC 2.0이란?

### 사전적 정의 (Dictionary Definition)
JSON-RPC 2.0은 JSON(JavaScript Object Notation) 데이터를 기반으로 하는 경량 원격 프로시저 호출(Remote Procedure Call, RPC) 프로토콜입니다. 클라이언트와 서버 간의 데이터 교환을 위해 설계된 상태 비저장(Stateless) 통신 규약으로, 요청(Request), 응답(Response), 알림(Notification) 및 배치(Batch) 처리를 지원합니다. 전송 계층과 독립적인 구조를 지니고 있어 HTTP, 웹소켓(WebSockets), TCP 등 다양한 네트워크 환경에서 활용 가능합니다.

### 실무 사용 예시 (Practical Use Case)
앤스로픽(Anthropic)이 공개한 MCP(Model Context Protocol)는 AI 모델과 외부 데이터 소스 간의 파편화된 인터페이스를 통합하기 위해 JSON-RPC 2.0을 표준 통신 프로토콜로 사용합니다. 클라이언트는 JSON 형식의 메시지를 통해 서버에 특정 도구(Tools)의 실행이나 리소스(Resources) 조회를 요청하며, 서버는 규격화된 JSON 데이터로 응답함으로써 AI 에이전트와 기업용 데이터베이스 간의 실시간 상호작용을 구현합니다.

### 관련 단어 (Related Words)
- RPC (Remote Procedure Call)
- JSON (JavaScript Object Notation)
- MCP (Model Context Protocol)