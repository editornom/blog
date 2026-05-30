---
title: FLOPs (Floating Point Operations per Second)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-30 19:36:48.490759+09:00
slug: flops-floating-point-operations
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: FLOPs(Floating Point Operations per Second)의 정의와 인공지능 모델 학습 및 추론 과정에서
  연산 자원을 정량화하는 핵심 지표로서의 역할을 살펴봅니다. 모델 파라미터와 데이터 규모에 따른 연산량 계산부터 효율적인 AI 개발을 위한 실무
  활용 사례까지 상세히 확인하세요.
references: []
modDatetime: 2026-05-30 19:46:48.490759+09:00
---

# FLOPs이란?

### 사전적 정의 (Dictionary Definition)
FLOPs(Floating Point Operations per Second)는 초당 수행 가능한 부동 소수점 연산의 횟수를 측정하는 단위입니다. 컴퓨터의 연산 성능을 나타내는 대표적인 척도이며, 인공지능 분야에서는 거대 언어 모델(LLM) 등을 학습(Training)하거나 추론(Inference)하는 과정에서 요구되는 총 연산량(Total Floating Point Operations)을 의미하는 지표로도 널리 사용됩니다. 이는 모델의 파라미터 수, 학습 데이터의 양과 밀접하게 연계되며, 인공지능 성능 향상을 위해 투입되는 컴퓨팅 자원의 규모를 정량화하는 핵심 변수입니다.

### 실무 사용 예시 (Practical Use Case)
1. 인공지능 모델 개발 시 전체 학습에 필요한 총 FLOPs를 계산하여, 필요한 GPU 자원의 규모와 클라우드 컴퓨팅 비용을 사전에 예측합니다.
2. 동일한 성능을 발휘하면서도 더 적은 FLOPs를 소모하는 경량화 알고리즘을 개발하여 기기 내 추론(On-device AI)의 효율성을 높입니다.
3. 엔비디아(NVIDIA) H100과 같은 AI 가속기의 성능을 비교할 때 테라플롭스(TFLOPS) 또는 페타플롭스(PFLOPS) 단위의 연산 처리 능력을 기준으로 삼습니다.

### 관련 단어 (Related Words)
* 스케일링 법칙 (Scaling Laws): 컴퓨팅 자원(Compute), 데이터 크기, 파라미터 양이 증가함에 따라 모델 성능이 예측 가능하게 향상된다는 법칙입니다.
* 친칠라 법칙 (Chinchilla Law): 주어진 연산량(FLOPs) 예산 내에서 최적의 성능을 내기 위한 모델 파라미터 수와 데이터 양의 적정 비율을 정의한 법칙입니다.
* 컴퓨팅 자원 (Compute): 인공지능 모델의 연산을 처리하기 위해 투입되는 하드웨어의 처리 능력 및 그 총량을 의미합니다.