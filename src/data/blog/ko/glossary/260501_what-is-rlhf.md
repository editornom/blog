---
title: RLHF이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-01 00:24:21.461709+09:00
slug: what-is-rlhf
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: RLHF(인간 피드백 기반 강화학습)는 인공지능의 답변을 인간의 가치와 의도에 부합하도록 최적화하는 모델 정렬(Alignment)
  핵심 기술입니다. 보상 모델과 PPO 알고리즘을 활용해 대규모 언어 모델(LLM)의 품질과 신뢰성을 높이는 RLHF의 정의와 작동 원리를 상세히
  소개합니다.
references: []
modDatetime: 2026-05-01 00:34:21.461709+09:00
---

## RLHF이란?

## 사전적 정의 (Dictionary Definition)

RLHF(Reinforcement Learning from Human Feedback)는 인공지능 모델의 출력물을 인간의 가치관, 의도, 선호도에 부합하도록 정렬(Alignment)하기 위해 인간의 피드백을 강화학습의 보상 신호로 사용하는 기술적 방법론입니다. 대규모 언어 모델(LLM)이 단순히 학습 데이터의 확률적 분포를 따르는 것을 넘어, 인간이 주관적으로 판단하는 답변의 품질과 사회적 규범을 학습하도록 설계되었습니다.

## 실무 사용 예시 (Practical Use Case)

언어 모델이 생성한 여러 개의 답변 후보군에 대해 인간 검수자가 선호도 순위를 매깁니다. 이 데이터를 바탕으로 특정 답변이 인간에게 줄 만족도를 수치화하는 보상 모델(Reward Model)을 훈련시키며, 최종적으로 PPO(Proximal Policy Optimization) 알고리즘을 통해 모델이 보상 점수를 극대화하는 방향으로 답변을 생성하도록 최적화합니다. 이 과정에서 초기 모델과의 차이를 제한하는 KL 발산(KL Divergence) 기법을 적용하여 모델의 언어적 일관성을 유지합니다.

## 관련 단어 (Related Words)

- SFT (Supervised Fine-tuning)
- PPO (Proximal Policy Optimization)
- 보상 모델 (Reward Model)
- 리워드 해킹 (Reward Hacking)