---
title: 할루시네이션(Hallucination)
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 15:15:26.547836+09:00
slug: hallucination
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 거대언어모델(LLM)의 할루시네이션(Hallucination) 현상에 대한 정의와 발생 원인, 그리고 실무적인 사례를 상세히
  설명합니다. 확률적 토큰 예측의 한계와 이를 보완하기 위한 RAG 기술 등 생성형 AI의 핵심 개념을 확인해 보세요.
references: []
modDatetime: 2026-05-07 15:25:26.547836+09:00
---

# 할루시네이션(Hallucination)이란?

### 사전적 정의 (Dictionary Definition)
할루시네이션(Hallucination)은 거대언어모델(LLM)이 문법적으로 유창하고 자연스러운 문장을 생성하면서도, 실제 사실과 부합하지 않거나 논리적으로 근거가 없는 허위 정보를 제공하는 현상을 말합니다. 이는 트랜스포머 아키텍처의 핵심인 '확률적 다음 토큰 예측(Stochastic Next-Token Prediction)' 과정에서 비롯되는 구조적 한계입니다. 모델은 텍스트의 의미적 진실을 검증하는 것이 아니라, 학습 데이터 내의 통계적 패턴에 따라 확률적으로 가장 가능성 높은 단어 조합을 생성하기 때문에 발생합니다.

### 실무 사용 예시 (Practical Use Case)
특정 인물에 대한 약력을 질문했을 때 AI가 실존하지 않는 수상 경력이나 학력을 상세히 서술하는 경우, 또는 법률 검토 시 존재하지 않는 조항이나 판례를 근거로 제시하는 행위가 실무적인 할루시네이션의 사례에 해당합니다.

### 관련 단어 (Related Words)
* 확률적 앵무새 (Stochastic Parrot): LLM이 의미 이해 없이 기계적인 통계 학습을 통해 언어를 생성하는 특성을 비유하는 용어입니다.
* 검색 증강 생성 (RAG): 외부의 신뢰할 수 있는 정보를 실시간으로 참조하여 답변의 정확도를 높이고 환각 현상을 억제하는 기술적 대안입니다.
* 트랜스포머 아키텍처 (Transformer Architecture): 어텐션 메커니즘을 기반으로 문맥을 파악하지만, 확률 기반 연산 체계로 인해 할루시네이션의 태생적 원인을 내포하고 있는 모델 구조입니다.