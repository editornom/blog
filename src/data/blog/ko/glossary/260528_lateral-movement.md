---
title: 횡적 이동(Lateral Movement)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-28 11:37:00.759886+09:00
slug: lateral-movement
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 횡적 이동(Lateral Movement)은 공격자가 내부 네트워크 진입 후 권한을 확장하며 고가치 자산에 도달하는 핵심 공격
  단계입니다. 본 포스팅에서는 횡적 이동의 정의와 실무 사례, 그리고 이를 방지하기 위한 제로 트러스트 기반의 마이크로 세그멘테이션 전략을 소개합니다.
references: []
modDatetime: 2026-05-28 11:47:00.759886+09:00
---

# 횡적 이동(Lateral Movement)이란?\n\n### 사전적 정의 (Dictionary Definition)\n사이버 보안에서 횡적 이동(Lateral Movement)이란 공격자가 조직의 내부 네트워크에 최초로 진입한 후, 시스템 내부를 탐색하며 다른 서버, 워크스테이션 또는 데이터로 접근 권한을 확장해 나가는 일련의 과정을 의미합니다. 공격자는 침투 성공 후 최초 거점(Foothold)에서 관리자 권한을 확보하거나 자격 증명을 탈취하여 네트워크 내의 고가치 자산(Crown Jewels)에 도달하는 것을 최종 목표로 합니다.\n\n### 실무 사용 예시 (Practical Use Case)\n공격자가 피싱 메일을 통해 일반 직원의 PC를 감염시킨 뒤, 해당 단말기에 저장된 자격 증명을 이용하여 내부 파일 서버나 데이터베이스 관리 서버로 이동하며 기업의 민감 정보를 유출하는 사례가 대표적입니다. 기존의 경계 기반 보안 모델(VPN 등)은 내부 접속자를 암시적으로 신뢰하기 때문에 이러한 횡적 이동에 취약하며, 이를 방지하기 위해 모든 연결을 검증하는 제로 트러스트 기반의 마이크로 세그멘테이션 도입이 권장됩니다.\n\n### 관련 단어 (Related Words)\n- 제로 트러스트(Zero Trust)\n- 마이크로 세그멘테이션(Micro-segmentation)\n- 최소 권한 원칙(Principle of Least Privilege)