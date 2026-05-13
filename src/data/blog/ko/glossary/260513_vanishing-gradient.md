---
title: 기울기 소실이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-13 20:18:00.657625+09:00
slug: vanishing-gradient
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 기울기 소실(Vanishing Gradient Problem)의 정의와 발생 원인을 살펴보고, 이를 해결하기 위한 LSTM과
  트랜스포머 등 실무적인 딥러닝 기법들을 소개합니다.
references: []
modDatetime: 2026-05-13 20:28:00.657625+09:00
---

# 기울기 소실이란?

### 사전적 정의 (Dictionary Definition)
기울기 소실(Vanishing Gradient Problem)은 인공 신경망의 학습 과정에서 역전파(Backpropagation) 알고리즘을 수행할 때, 출력층에서 입력층 방향으로 전달되는 기울기(Gradient)가 층을 거듭할수록 점차 작아져 결국 사라지는 현상을 의미합니다. 이는 신경망의 층이 깊어질수록 가중치 업데이트가 제대로 이루어지지 않게 만들어, 모델이 데이터의 장기적인 의존 관계를 학습하지 못하게 하는 주요 원인이 됩니다. 

### 실무 사용 예시 (Practical Use Case)
순환 신경망(RNN) 구조를 사용하여 긴 시퀀스 데이터를 처리할 때 발생합니다. 문장의 길이가 길어질수록 앞부분에 위치한 단어의 정보가 뒷부분까지 전달되지 못하고 잊혀지는 현상이 대표적입니다. 이를 해결하기 위해 LSTM(Long Short-Term Memory)이나 GRU(Gated Recurrent Unit) 같은 특수한 구조가 고안되었으며, 최근에는 트랜스포머(Transformer)의 어텐션 메커니즘을 통해 모든 데이터 간의 관계를 직접 계산함으로써 이 문제를 원천적으로 우회합니다.

### 관련 단어 (Related Words)
* 역전파 (Backpropagation)
* 순환 신경망 (RNN)
* 장기 의존성 (Long-term Dependency)