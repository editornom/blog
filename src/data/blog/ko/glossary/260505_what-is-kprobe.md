---
title: kprobe이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-05 14:33:23.133915+09:00
slug: what-is-kprobe
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: kprobe은 리눅스 커널의 특정 지점에 동적으로 중단점을 설정하여 시스템 재부팅 없이 실시간으로 동작을 추적하고 정보를 수집하는
  경량 메커니즘입니다. eBPF와 결합하여 시스템 콜 모니터링, 성능 분석 및 보안 감사 등 다양한 커널 레벨 관찰 작업에 핵심적으로 활용됩니다.
references: []
modDatetime: 2026-05-05 14:43:23.133915+09:00
---

# kprobe이란?

### 사전적 정의 (Dictionary Definition)
kprobe(Kernel Probe)는 리눅스 커널의 특정 명령어나 함수가 실행되는 지점에 동적으로 중단점(Breakpoint)을 설정하여 커널의 동작을 추적하고 관련 정보를 수집할 수 있게 해주는 경량 메커니즘입니다. 소스 코드를 수정하거나 커널을 재컴파일하여 다시 부팅할 필요 없이, 실행 중인 시스템의 커널 내부에 프로브를 설치하여 해당 지점이 호출될 때 미리 정의된 핸들러 함수가 실행되도록 제어합니다.

### 실무 사용 예시 (Practical Use Case)
eBPF(extended Berkeley Packet Filter)와 결합하여 '제로 인스트루멘테이션' 환경에서 시스템 콜(System Call)을 모니터링하는 데 널리 사용됩니다. 예를 들어, 특정 프로세스가 네트워크 소켓을 생성하거나 파일 시스템의 특정 영역에 쓰기 작업을 수행할 때, 해당 작업을 처리하는 커널 함수에 kprobe를 부착하여 인자 값과 반환 값을 실시간으로 기록함으로써 보안 감사를 수행하거나 성능 병목 지점을 식별합니다.

### 관련 단어 (Related Words)
* <b>eBPF (Extended Berkeley Packet Filter):</b> 커널 소스 수정 없이 커널 레벨에서 프로그램을 실행할 수 있게 하는 기술로, kprobe를 주요 추적 수단으로 활용합니다.
* <b>uprobe (User Probe):</b> 커널 공간이 아닌 사용자 공간(User Space) 애플리케이션의 함수를 추적하기 위한 메커니즘입니다.
* <b>Tracepoint:</b> 커널 소스 코드에 미리 정의된 정적 추적 지점으로, kprobe보다 오버헤드가 적고 안정적이지만 유연성은 낮습니다.
* <b>System Call:</b> 사용자 공간의 프로세스가 커널에 특정 서비스를 요청하는 인터페이스로, kprobe의 주요 추적 대상입니다.