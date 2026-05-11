---
title: OpenTelemetry이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 14:19:31.002554+09:00
slug: what-is-opentelemetry
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: OpenTelemetry(오픈텔레메트리)는 CNCF의 오픈 소스 관측성 프레임워크로, 벤더 종속성 없이 트레이스, 메트릭,
  로그 데이터를 표준화된 방식으로 수집 및 전송합니다. 복잡한 MSA 환경에서 시스템 가시성을 확보하고 성능을 분석하기 위한 필수적인 도구와 기술을
  제공합니다.
references: []
modDatetime: 2026-05-08 14:29:31.002554+09:00
---# OpenTelemetry이란?

### 사전적 정의 (Dictionary Definition)
오픈텔레메트리(OpenTelemetry, OTel)는 클라우드 네이티브 컴퓨팅 재단(CNCF)에서 주도하는 오픈 소스 관측성(Observability) 프레임워크입니다. 소프트웨어의 성능 및 상태를 분석하기 위해 필요한 트레이스(Traces), 메트릭(Metrics), 로그(Logs) 등의 텔레메트리 데이터를 생성, 수집, 처리, 전송하기 위한 표준화된 API, SDK 및 도구 모음을 제공합니다. 특정 벤더에 종속되지 않는 데이터 표준을 수립하여 분산 시스템 환경에서의 통합적인 가시성 확보를 목적으로 합니다.

### 실무 사용 예시 (Practical Use Case)
마이크로서비스 아키텍처(MSA) 환경에서 서비스 간 호출 경로를 추적하는 분산 트레이싱 구현에 주로 활용됩니다. 개발자는 OpenTelemetry SDK를 애플리케이션에 통합하여 사용자 요청이 여러 서버를 거치는 과정에서 발생하는 지연 시간과 오류를 파악할 수 있습니다. 특히 eBPF와 같은 커널 수준의 데이터 수집 기술과 상호보완적으로 결합될 경우, 인프라의 하드웨어 지표와 애플리케이션의 비즈니스 로직 문맥을 결합한 통합 분석이 가능해집니다.

### 관련 단어 (Related Words)
* 관측성(Observability)
* 분산 트레이싱(Distributed Tracing)
* CNCF(Cloud Native Computing Foundation)
