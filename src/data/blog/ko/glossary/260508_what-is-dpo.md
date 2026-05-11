---
title: DPO(직접 선호 최적화)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-08 19:10:24.269176+09:00
slug: what-is-dpo
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: DPO(직접 선호 최적화)는 보상 모델 없이 인간의 선호 데이터를 직접 학습하여 거대 언어 모델(LLM)을 효율적으로 정렬하는
  혁신적인 알고리즘입니다. 기존 RLHF의 복잡성을 해결하고 학습 안정성과 모델 성능을 동시에 확보하는 DPO의 개념과 실무 활용 사례를 확인해
  보세요.
references: []
modDatetime: 2026-05-08 19:20:24.269176+09:00
---# DPO(직접 선호 최적화)이란?

### 사전적 정의 (Dictionary Definition)
DPO(Direct Preference Optimization)는 거대 언어 모델(LLM)이 인간의 선호도에 부합하도록 정렬하는 인공지능 학습 알고리즘입니다. 기존의 RLHF 방식이 별도의 보상 모델을 학습시키고 PPO와 같은 강화학습 과정을 거쳐야 했던 복잡성을 해결하기 위해 제안되었습니다. DPO는 선호도 데이터를 기반으로 모델의 정책을 직접 최적화하여 보상 모델 없이도 인간의 가치를 효과적으로 반영할 수 있게 합니다. 이를 통해 학습 과정의 안정성을 확보하고 연산 자원을 절감하면서도 RLHF와 동등하거나 그 이상의 성능을 낼 수 있습니다.

### 실무 사용 예시 (Practical Use Case)
복잡한 강화학습 하이퍼파라미터 튜닝이 어려운 환경에서 모델의 안전성을 높이고 답변 품질을 정교하게 제어하기 위해 활용됩니다. 인간이 작성한 선호 데이터 쌍을 활용하여 모델이 선호되는 답변을 생성할 확률은 높이고 선호되지 않는 답변의 확률은 낮추는 방식으로 모델의 응답 품질을 개선하는 데 적용됩니다.

### 관련 단어 (Related Words)
- RLHF(인간 피드백 기반 강화학습)
- PPO(근사 정책 최적화)
- AI Alignment(인공지능 정렬)
