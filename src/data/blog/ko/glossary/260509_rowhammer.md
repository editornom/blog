---
title: Rowhammer
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-09 11:23:04.486265+09:00
slug: rowhammer
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: Rowhammer는 DRAM의 특정 행을 반복 활성화하여 인접 행의 비트 플립을 유도하는 하드웨어 취약점으로, 시스템 권한
  탈취 및 데이터 변조 등의 심각한 보안 위협을 초래합니다. 최신 DDR5와 GPU를 겨냥한 공격 사례부터 TRR, PRAC 등 실무적인 대응 기술까지
  핵심적인 보안 위협과 방어 전략을 상세히 분석합니다.
references: []
modDatetime: 2026-05-09 11:33:04.486265+09:00
---# Rowhammer이란?

### 사전적 정의 (Dictionary Definition)
DRAM(Dynamic Random Access Memory)의 특정 메모리 행(Row)을 고속으로 반복 활성화하여 인접한 행의 전하 간섭을 유도하고, 이로 인해 저장된 데이터의 비트가 반전(Bit-flip)되는 하드웨어 보안 취약점입니다. 이는 미세 공정화된 반도체 소자 간의 물리적 간섭 현상을 악용한 것으로, 소프트웨어적 접근 권한을 우회하여 메모리 데이터를 변조하거나 시스템 권한을 탈취하는 데 악용될 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
1. DDR5 취약점 공격: 제조사가 적용한 TRR(Target Row Refresh) 기술의 샘플링 로직을 우회하는 Phoenix 공격을 통해 최신 메모리 모듈에서도 비트 플립을 발생시키는 사례가 확인되었습니다.
2. GPU 보안 침해: GDDR6 메모리의 아키텍처적 특성을 이용한 GPUBreach 공격을 수행하여 고성능 컴퓨팅 환경에서 루트 권한을 탈취하는 데 활용됩니다.
3. 실무적 대응 전략: 리프레시 주기(tREFI)를 단축하여 전하 유출이 발생하기 전에 메모리 셀을 재충전하거나, DRAM 내부에서 행 활성화 횟수를 직접 계수하는 PRAC(Per-Row Activation Counting) 기술을 도입하여 공격을 차단합니다.

### 관련 단어 (Related Words)
1. 비트 플립 (Bit-flip): 물리적 간섭으로 인해 메모리 내의 논리 데이터 값이 0에서 1 또는 1에서 0으로 반전되는 현상입니다.
2. TRR (Target Row Refresh): 특정 행의 과도한 활성화가 감지될 때 인접 행을 선제적으로 리프레시하는 하드웨어 기반 방어 기술입니다.
3. PRAC (Per-Row Activation Counting): DRAM의 각 행이 활성화되는 횟수를 실시간으로 카운팅하여 Rowhammer 공격 임계점 도달을 방지하는 차세대 보안 표준 기법입니다.
