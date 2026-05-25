---
title: Positional Encoding이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-25 21:16:19.412845+09:00
slug: positional-encoding
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 트랜스포머 아키텍처에서 입력 데이터의 순서 정보를 주입하는 Positional Encoding의 개념과 실무 활용 사례를 설명합니다.
  단어 임베딩에 위치 정보를 더해 모델이 시퀀스 내 맥락을 정확하게 인식하도록 돕는 핵심 원리를 다룹니다.
references: []
modDatetime: 2026-05-25 21:26:19.412845+09:00
---

### 사전적 정의 (Dictionary Definition)
Positional Encoding은 트랜스포머(Transformer) 아키텍처와 같이 데이터를 병렬로 처리하는 신경망 모델에서 입력 데이터의 순서나 위치 정보를 주입하기 위해 사용하는 기술입니다. 순환 신경망(RNN)과 달리 트랜스포머는 문장의 단어들을 동시에 처리하므로 단어의 배치 순서를 파악할 수 없는 구조적 특성을 가집니다. 이를 해결하기 위해 각 단어의 임베딩 벡터에 위치 정보를 담은 고유한 벡터값을 더함으로써, 모델이 시퀀스 내에서 데이터의 상대적 또는 절대적 위치를 인식할 수 있도록 돕습니다. 주로 사인(Sine) 및 코사인(Cosine) 함수를 이용한 주기적 함수 기반의 값을 활용합니다.

### 실무 사용 예시 (Practical Use Case)
대규모 언어 모델(LLM)의 텍스트 생성 과정에서 문장의 의미를 정확히 파악하기 위해 활용됩니다. 예를 들어 "철수가 영희를 좋아한다"와 "영희가 철수를 좋아한다"라는 문장은 구성 단어가 동일하지만 단어의 순서에 따라 주어와 목적어가 달라져 의미가 완전히 변합니다. Positional Encoding은 이러한 어순 정보를 수치화하여 모델에 전달함으로써, 동일한 단어라도 위치에 따라 서로 다른 맥락으로 처리될 수 있도록 보장합니다.

### 관련 단어 (Related Words)
- Transformer Architecture
- Self-Attention
- Word Embedding