---
title: SRv6(IPv6 Segment Routing)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 17:07:47.039006+09:00
slug: what-is-srv6-segment-routing
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: SRv6(IPv6 Segment Routing)은 IPv6 기반의 세그먼트 라우팅 기술로 대규모 인프라 운영 시 우수한 확장성과
  유연한 트래픽 제어 기능을 제공합니다. 오픈AI의 MCR 아키텍처와 같이 대규모 GPU 클러스터의 저지연 통신과 효율적인 네트워크 운영을 가능하게
  하는 차세대 프로토콜입니다.
references: []
modDatetime: 2026-05-07 17:17:47.039006+09:00
---

# SRv6(IPv6 Segment Routing)이란?\n\n### 사전적 정의 (Dictionary Definition)\nSRv6(IPv6 Segment Routing)은 IPv6 데이터 평면을 기반으로 세그먼트 라우팅(Segment Routing) 기법을 적용한 차세대 네트워크 프로토콜입니다. 송신측 노드가 패킷이 거쳐야 할 경로와 수행할 동작을 명시적으로 지정하며, 이를 IPv6 헤더의 세그먼트 라우팅 확장 헤더(SRH)에 담아 전송합니다. 복합적인 네트워크 상태 정보를 중간 노드에서 유지할 필요가 없어 대규모 인프라 운영 시 우수한 확장성과 유연한 트래픽 제어 기능을 제공합니다.\n\n### 실무 사용 예시 (Practical Use Case)\n오픈AI의 MCR(Multipath Reliable Connection) 아키텍처는 SRv6를 도입하여 대규모 GPU 클러스터의 통신 효율을 극대화하는 사례로 활용됩니다. 기존의 복잡한 계층 구조를 2계층(2-Tier)으로 축소하여 수만 개의 GPU를 저지연으로 연결하고 전력 소비를 절감합니다. 다만, 송신자가 경로 선택권을 가지는 특성상 기존의 중앙 집중식 네트워크 보안 정책을 우회할 가능성이 존재하므로 인프라 설계 시 보안 검토가 필수적입니다.\n\n### 관련 단어 (Related Words)\n- IPv6: SRv6 기술이 동작하는 기반이 되는 차세대 인터넷 프로토콜 주소 체계입니다.\n- Segment Routing (SR): 네트워크 경로를 여러 세그먼트의 목록으로 정의하여 소스 기반 라우팅을 구현하는 기술입니다.\n- MCR (Multipath Reliable Connection): AI 모델 학습 및 추론 성능을 높이기 위해 SRv6 기반의 네트워크 최적화를 적용한 프로토콜입니다.