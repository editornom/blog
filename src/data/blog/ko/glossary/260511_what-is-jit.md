---
title: JIT이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 15:30:57.403279+09:00
slug: what-is-jit
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: JIT(Just-In-Time) 컴파일은 실행 시점에 바이트코드를 기계어로 번역하여 런타임 성능을 최적화하는 기술로, AOT와
  인터프리터 방식의 장점을 결합한 것이 특징입니다. eBPF 기술 등에서 하드웨어 네이티브 명령어로 즉시 변환되어 시스템 호출 비용을 절감하고 네이티브
  수준의 처리 속도를 구현합니다.
references: []
modDatetime: 2026-05-11 15:40:57.403279+09:00
---

# JIT이란?\n\n- 사전적 정의 (Dictionary Definition): JIT(Just-In-Time) 컴파일은 프로그램이 실행되는 시점에 바이트코드를 대상 시스템의 기계어로 실시간 번역하는 기술입니다. 소스 코드를 사전에 전부 기계어로 변환하는 AOT(Ahead-Of-Time) 방식의 실행 효율성과 인터프리터 방식의 유연성을 결합하여 런타임 성능을 최적화합니다.\n\n- 실무 사용 예시 (Practical Use Case): eBPF(Extended Berkeley Packet Filter) 기술에서 JIT 컴파일러는 커널 내 가상 머신에서 구동되는 바이트코드를 하드웨어 네이티브 명령어로 즉시 변환합니다. 이를 통해 시스템 호출(System Call) 시 발생하는 유저 공간과 커널 공간 사이의 컨텍스트 스위칭 비용을 혁신적으로 절감하며 네이티브 코드에 근접한 실행 속도를 제공합니다.\n\n- 관련 단어 (Related Words): AOT(Ahead-Of-Time), 바이트코드(Bytecode), eBPF Verifier