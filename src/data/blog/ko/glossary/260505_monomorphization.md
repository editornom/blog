---
title: 단형화(Monomorphization)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-05 11:19:45.062991+09:00
slug: monomorphization
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 단형화(Monomorphization)는 제네릭 코드를 구체적인 타입별 기계어 코드로 변환하여 런타임 오버헤드를 제거하고 실행
  성능을 극대화하는 컴파일 프로세스입니다. 정적 디스패치를 통해 프로그램의 효율성을 높이는 핵심 메커니즘과 그에 따른 장단점을 설명합니다.
references: []
modDatetime: 2026-05-05 11:29:45.062991+09:00
---

# 단형화(Monomorphization)이란?

### 사전적 정의 (Dictionary Definition)
단형화(Monomorphization)는 프로그래밍 언어의 컴파일러가 제네릭(Generic) 코드를 실제 사용 시 지정된 구체적인 타입별로 각각 별도의 기계어 코드로 변환하는 프로세스를 의미합니다. 이 기법은 정적 디스패치(Static Dispatch)를 구현하는 핵심 메커니즘으로, 런타임에 타입 정보를 확인하거나 분기하는 오버헤드를 제거하여 실행 성능을 극대화합니다. 반면, 다양한 타입에 대해 동일한 제네릭 함수가 중복 생성되므로 컴파일 시간이 길어지고 최종 바이너리의 크기가 비대해지는 원인이 되기도 합니다.

### 실무 사용 예시 (Practical Use Case)
Rust 언어에서 제네릭 함수를 정의한 뒤 이를 정수형(i32)과 문자열(String) 타입으로 각각 호출할 경우, 컴파일러는 각 타입의 메모리 레이아웃과 특성에 최적화된 두 개의 독립적인 함수 구현체를 기계어로 생성합니다. 이를 통해 각 타입에 최적화된 인라인(Inline) 처리가 가능해지며 실행 속도가 향상됩니다.

### 관련 단어 (Related Words)
* 제네릭(Generics)
* 정적 디스패치(Static Dispatch)
* 다형성(Polymorphism)