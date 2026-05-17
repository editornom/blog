---
title: GRPO이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-17 19:09:52.295471+09:00
slug: what-is-grpo
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: GRPO(Group Relative Policy Optimization)는 별도의 보상 모델 없이 그룹 내 응답의 상대적 성과를
  비교하여 모델의 추론 능력을 최적화하는 강화 학습 기법입니다. 기존 RLHF의 비용 문제를 해결하며 수학 및 코딩 등 논리적 검증이 필요한 대규모
  언어 모델 학습에 효과적입니다.
references: []
modDatetime: 2026-05-17 19:19:52.295471+09:00
---

# GRPO이란?

### 사전적 정의
GRPO(Group Relative Policy Optimization)는 인공지능 강화 학습 과정에서 별도의 보상 모델(Reward Model)을 구축하는 대신, 생성된 응답 그룹 내의 상대적 성과를 비교하여 모델의 정책을 최적화하는 기법입니다. 기존의 RLHF(인간 피드백 기반 강화 학습) 방식에서 발생하는 높은 연산 비용과 보상 해킹(Reward Hacking) 문제를 해결하기 위해 고안되었습니다. 이 방식은 개별 응답의 절대적 점수가 아닌 그룹 내 평균 대비 성능을 지표로 삼아, 모델이 더 논리적이고 검증 가능한 추론 과정을 학습하도록 유도합니다.

### 실무 사용 예시
수학 문제 풀이, 프로그래밍 코드 생성 등 정답과 논리적 경로의 검증이 필요한 추론 전용 대규모 언어 모델(LLM) 학습에 주로 사용됩니다. 모델이 동일한 질문에 대해 여러 개의 답변 후보를 생성하게 한 뒤, 그룹 내에서 가장 정확하고 효율적인 답변에 더 높은 가중치를 부여하는 방식으로 추론 능력을 고도화합니다.

### 관련 단어
- RLHF (Reinforcement Learning from Human Feedback)
- DPO (Direct Preference Optimization)
- 보상 해킹 (Reward Hacking)
- 추론 모델 (Reasoning Model)