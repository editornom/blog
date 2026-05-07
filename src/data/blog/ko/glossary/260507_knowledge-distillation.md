---
title: 지식 증류(Distillation)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 15:09:19.640732+09:00
slug: knowledge-distillation
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 지식 증류(Knowledge Distillation)는 거대 모델의 지식을 경량 모델로 전이하여 성능 손실을 최소화하면서 모델
  크기를 줄이고 추론 속도를 최적화하는 기계 학습 기법입니다. 고성능 교사 모델의 추론 논리를 효율적으로 자산화함으로써 저비용으로도 정교한 AI
  서비스를 구현할 수 있는 모델 경량화의 핵심 기술입니다.
references: []
modDatetime: 2026-05-07 15:19:19.640732+09:00
---

# 지식 증류(Distillation)이란?

### 사전적 정의 (Dictionary Definition)
지식 증류(Knowledge Distillation)는 거대하고 정교한 인공지능 모델(Teacher Model)이 보유한 지식을 상대적으로 작고 효율적인 모델(Student Model)로 전이하는 기계 학습 기법입니다. 이는 복잡한 교사 모델의 출력값인 소프트 타겟(Soft Targets)을 학습 데이터로 활용하여, 학생 모델이 교사 모델의 추론 논리를 모사하게 함으로써 성능 손실을 최소화하면서도 모델의 크기를 줄이고 추론 속도를 향상시키는 것을 목적으로 합니다.

### 실무 사용 예시 (Practical Use Case)
안드레 카파시의 'LLM Wiki' 아키텍처에서 고비용 추론 모델이 생성한 정교한 결과물을 마크다운 형태의 구조화된 지식으로 정제 및 축적하는 과정에 활용됩니다. 이를 통해 한 번의 고비용 추론으로 얻은 지식을 자산화하여, 이후 유사한 요청에 대해 저비용의 경량 모델이 즉각적인 답변을 제공하도록 최적화하는 데 기여합니다.

### 관련 단어 (Related Words)
- 교사 모델(Teacher Model)
- 학생 모델(Student Model)
- 모델 경량화(Model Compression)