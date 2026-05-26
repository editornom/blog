---
title: KV 캐시이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-26 18:52:40.627031+09:00
slug: kv-cache
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: KV 캐시는 LLM 추론 시 이전 토큰의 연산 결과를 VRAM에 저장 및 재사용하여 생성 속도를 높이고 메모리 효율을 최적화하는
  기술입니다. 트랜스포머 아키텍처에서 불필요한 반복 연산을 줄여 지연 시간을 단축하는 KV 캐시의 원리와 활용 사례를 소개합니다.
references: []
modDatetime: 2026-05-26 19:02:40.627031+09:00
---

# KV 캐시이란?

## 사전적 정의 (Dictionary Definition)
KV 캐시(Key-Value Cache)는 자기회귀(Autoregressive) 방식의 거대 언어 모델(LLM) 추론 과정에서 연산 효율을 높이기 위해 도입된 메모리 최적화 기술입니다. 트랜스포머(Transformer) 아키텍처의 셀프 어텐션(Self-Attention) 계산 시, 이미 생성된 토큰들에 대해 계산된 키(Key)와 값(Value) 텐서를 매번 다시 계산하지 않고 VRAM(비디오 램)에 저장하여 재사용하는 메커니즘을 의미합니다. 이를 통해 새로운 토큰을 생성할 때 발생하는 불필요한 반복 연산을 줄여 추론 지연 시간(Latency)을 유의미하게 단축할 수 있습니다.

## 실무 사용 예시 (Practical Use Case)
구글의 Gemma 4 및 DeepSeek-V3와 같은 최신 LLM 아키텍처에서 추론 가속화를 위해 활용됩니다. 특히 메인 모델과 가벼운 드래프트 모델이 KV 캐시를 서로 공유하도록 설계함으로써, 모델 간 데이터 전송 효율을 극대화하고 추가적인 메모리 소모를 억제하면서 전체적인 토큰 생성 속도를 높이는 데 사용됩니다.

## 관련 단어 (Related Words)
*   투기적 디코딩(Speculative Decoding)
*   어텐션 메커니즘(Attention Mechanism)
*   추론 최적화(Inference Optimization)
*   VRAM(Video Random Access Memory)