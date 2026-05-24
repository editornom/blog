---
title: RTT (Round Trip Time)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-24 15:26:59.405265+09:00
slug: rtt-round-trip-time
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: RTT(Round Trip Time, 왕복 시간)는 데이터 패킷의 송수신 과정을 측정하는 핵심 지표로, 분산 시스템의 합의
  알고리즘 성능과 네트워크 가용성을 결정짓는 중요한 요소입니다.
references: []
modDatetime: 2026-05-24 15:36:59.405265+09:00
---

# RTT이란?

- 사전적 정의 (Dictionary Definition): RTT(Round Trip Time, 왕복 시간)는 송신측에서 보낸 데이터 패킷이 수신측에 도달하고, 그에 대한 응답 메시지가 다시 송신측으로 돌아오기까지 걸리는 총 시간을 의미합니다. 이는 네트워크의 지연 정도를 파악하는 가장 기본적인 지표입니다.

- 실무 사용 예시 (Practical Use Case): 분산 합의 프로토콜인 Raft나 Paxos 환경에서 노드 간의 데이터 동기화 및 정족수(Quorum) 합의 속도는 노드 간 RTT에 직접적으로 의존합니다. 네트워크 환경의 물리적 거리나 부하로 인해 RTT가 길어지면, 클러스터의 상태 업데이트가 늦어지고 시스템 전체의 가용성이 저하되는 원인이 됩니다.

- 관련 단어 (Related Words): 레이턴시 (Latency), 정족수 (Quorum), 핑 (Ping)