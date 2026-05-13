---
title: Stop-the-world이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 15:17:57.877292+09:00
slug: stop-the-world
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Stop-the-world (STW) temporarily suspends all application threads for
  garbage collection, ensuring safe memory reclamation. This critical process impacts
  system performance and is key to optimizing applications in languages like Java
  and Go.
references: []
modDatetime: 2026-05-13 15:27:57.877292+09:00
---

# Stop-the-world이란?\n\n## 사전적 정의 (Dictionary Definition)\nStop-the-world(STW)는 가비지 컬렉션(Garbage Collection)을 수행하기 위해 애플리케이션의 모든 스레드 실행을 일시적으로 중단하는 상태를 의미합니다. 가비지 컬렉터가 메모리 내의 객체 참조 관계를 정확히 파악하고 더 이상 사용되지 않는 메모리를 안전하게 회수하기 위해서는 데이터의 정적 상태가 보장되어야 하므로, 가비지 컬렉션 전담 스레드를 제외한 모든 작업 스레드를 멈추는 작업 방식에서 유래했습니다.\n\n## 실무 사용 예시 (Practical Use Case)\n자바(Java)나 고(Go)와 같이 가비지 컬렉터를 사용하는 언어로 개발된 시스템에서 응답 속도가 불규칙하게 느려지는 현상이 발생할 경우, 가비지 컬렉션 로그를 통해 Stop-the-world 발생 빈도와 지속 시간을 측정합니다. 이를 기반으로 힙(Heap) 메모리 크기를 최적화하거나 저지연(Low-latency) 가비지 컬렉션 알고리즘을 적용하여 시스템의 가용성을 높입니다.\n\n## 관련 단어 (Related Words)\n- 가비지 컬렉션(Garbage Collection)\n- 지연 시간(Latency)\n- 메모리 안전성(Memory Safety)