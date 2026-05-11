---
title: SFT (지도 미세조정)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-11 20:50:22.686784+09:00
slug: what-is-sft
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 지도 미세조정(SFT)은 고품질의 지시문-답변 데이터셋을 활용해 사전 학습된 언어 모델을 사용자 의도에 맞게 정렬하고 특정
  작업 수행 능력을 고도화하는 핵심 과정입니다. 챗봇 서비스 구현 및 도메인 특화 모델 구축을 위한 SFT의 정의와 실무 활용 사례를 자세히 확인해
  보세요.
references: []
modDatetime: 2026-05-11 21:00:22.686784+09:00
---

# SFT (지도 미세조정)이란?

### 사전적 정의 (Dictionary Definition)
지도 미세조정(Supervised Fine-Tuning, SFT)은 사전 학습된 거대 언어 모델(LLM)이 사용자의 지시사항을 이해하고 적절한 응답을 생성할 수 있도록, 사람이 작성한 '지시문-답변' 쌍의 고품질 데이터셋을 활용하여 모델의 가중치를 조정하는 과정입니다. 이는 모델이 단순히 다음 단어를 통계적으로 예측하는 단계를 넘어, 특정 작업 수행 능력이나 대화 형식을 학습하게 함으로써 모델을 인간의 의도에 정렬(Alignment)시키는 첫 번째 핵심 단계로 평가받습니다.

### 실무 사용 예시 (Practical Use Case)
대규모 언어 모델을 챗봇 서비스로 배포하기 전, 수만 건의 모범 대화 데이터를 학습시켜 모델이 질문에 대해 명확하고 일관된 형식으로 답변하도록 고도화하는 과정에서 사용됩니다. 또한 특정 전문 분야(의료, 법률 등)의 질의응답 형식을 익히게 하여 도메인 특화 모델을 제작할 때도 필수적으로 활용됩니다.

### 관련 단어 (Related Words)
* RLHF (인간 피드백 기반 강화학습)
* 인스트럭션 튜닝 (Instruction Tuning)
* 사전 학습 (Pre-training)