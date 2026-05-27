---
title: 'Cloudflare의 PQC 선언과 ''반쪽짜리 방패'': 수확 후 해독(HNDL) 방어만으론 부족하다'
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-27 11:48:05.566836+09:00
slug: cloudflare-pqc-hndl-defense
featured: false
draft: false
ogImage: "../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp"
description: Cloudflare의 PQC 도입 현황을 통해 ML-KEM 기반의 미래 해독 공격 방어 전략과 실시간 위협 대응을 위한 기술적
  한계를 분석합니다. 진정한 양자 내성 보안을 위해 오리진 서버까지 확장되어야 할 인프라 전환의 필요성을 확인해 보세요.
references:
- https://blog.cloudflare.com/post-quantum-warp/
- https://blogs.cisco.com/developer/how-post-quantum-cryptography-affects-security-and-encryption-algorithms
- https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/
modDatetime: 2026-05-27 11:58:05.566836+09:00
faqs:
- q: 양자 내성 암호(PQC)란 무엇인가요?
  a: 양자 컴퓨터의 강력한 연산 능력으로도 해독할 수 없도록 설계된 차세대 암호화 알고리즘 체계입니다. 기존의 RSA나 ECC 암호 체계가 양자
    컴퓨팅 환경에서 무력화될 것에 대비하여 NIST 등이 표준화하고 있는 기술입니다.
- q: '''수확 후 해독(HNDL)'' 공격은 왜 위험한가요?'
  a: 공격자가 당장 해독할 수 없더라도 암호화된 트래픽을 미리 수집해 저장해 두었다가, 향후 성능이 우수한 양자 컴퓨터가 개발되었을 때 과거의
    데이터를 해독하는 공격 방식이기 때문입니다. 국가 기밀이나 장기 보존 데이터에 치명적입니다.
- q: Cloudflare가 도입한 ML-KEM 기술의 주요 특징은 무엇인가요?
  a: 격자 기반 암호학을 활용한 키 캡슐화 방식입니다. 데이터를 암호화하는 데 필요한 비밀 키를 양자 컴퓨터 공격으로부터 안전하게 생성하고 교환하는
    데 집중하며, 현재 NIST FIPS 203 표준으로 선정되어 있습니다.
- q: 현재 PQC 지원 방식에서 '디지털 서명'이 빠진 이유는 무엇인가요?
  a: 디지털 서명 표준인 ML-DSA는 키 합의 방식보다 표준화 및 인프라 적용 속도가 늦기 때문입니다. 이로 인해 서버의 정당성을 증명하는 단계에서는
    여전히 고전 암호를 사용하며, 실시간 위협 대응에 한계를 보입니다.
- q: 본문에서 언급한 '라스트 마일' 보안 위험이란 무엇을 의미하나요?
  a: 사용자와 Cloudflare 에지 서버 사이는 PQC로 보호되더라도, 에지 서버에서 실제 데이터가 있는 오리진 서버까지의 구간이 고전 암호를
    사용할 경우 보안 체인이 끊어지는 현상을 의미합니다. 이 구간이 양자 위협의 사각지대가 됩니다.
- q: PQC 도입 시 기술적으로 고려해야 할 성능 이슈는 무엇인가요?
  a: PQC 알고리즘은 고전 암호에 비해 암호 키와 서명 데이터의 크기가 월등히 큽니다. 이는 네트워크 패킷의 단편화나 핸드쉐이크 지연 시간을
    초래할 수 있어, 네트워크 장비의 성능과 대역폭에 대한 사전 검토가 필수적입니다.
- q: Cloudflare의 PQC 전략과 안드로이드 17의 보안 접근 방식은 어떤 차이가 있나요?
  a: Cloudflare는 네트워크 계층의 터널링 보안에 집중하는 반면, 안드로이드 17은 하드웨어 기반의 검증된 부팅 단계부터 ML-DSA 서명을
    통합합니다. 안드로이드는 기기 자체의 신뢰 체인을 양자 내성으로 구축하는 데 더 근본적인 목표를 둡니다.
- q: 기업 보안 관리자가 Cloudflare One을 사용할 때 유의해야 할 점은 무엇인가요?
  a: 단순히 PQC 옵션을 활성화하는 것뿐만 아니라, 보안 수준을 강제로 낮추는 다운그레이드 공격을 방어하기 위해 엄격한 정책 오버라이드를 적용해야
    합니다. 또한 내부 오리진 서버의 라이브러리도 표준에 맞춰 업데이트해야 합니다.
- q: '"Cloudflare에서 지원하는 양자 내성 암호를 쓰면 우리 회사 서버 속도가 많이 느려지나요?"'
  a: PQC는 암호 키 데이터가 커서 연결 초기 단계에서 약간의 지연이 발생할 수 있습니다. 하지만 실제 데이터 전송 속도보다는 연결 수립 시간에
    영향을 주며, 최신 하드웨어 환경에서는 사용자가 체감하기 어려운 수준인 경우가 많습니다.
- q: '"지금 당장 양자 컴퓨터가 있는 것도 아닌데 PQC로 인프라를 바꾸는 게 예산 낭비는 아닐까요?"'
  a: 수확 후 해독(HNDL) 공격 때문에 지금 전송되는 데이터도 미래에 위협받을 수 있습니다. NIST에서도 2035년까지 완전 전환을 권고하고
    있으며, 보안 사고 예방 비용 측면에서 단계적인 인프라 전환은 필수적인 투자로 평가받습니다.
---

<div class="bluf"><strong>[BLUF]</strong>
Cloudflare의 현재 PQC 지원은 '키 합의(<a href="/ko/glossary/ml-kem" class="glossary-tooltip" data-definition="격자 기반 암호학을 활용하여 양자 컴퓨터의 공격에도 안전하게 비밀 키를 교환할 수 있도록 설계된 차세대 키 캡슐화 방식입니다.">ML-KEM</a>)'를 통해 미래의 해독 공격(HNDL)을 막는 데 집중하고 있으나, '디지털 서명(ML-DSA)' 표준화 미비로 인해 실시간 중간자 공격(MITM) 방어에는 한계가 있습니다. 진정한 종단 간 보안을 위해서는 WARP 터널 이후의 '오리진 서버' 구간에 대한 PQC 업그레이드가 필수적이며, 이는 단순한 클라이언트 업데이트 이상의 인프라 전환을 요구합니다.</div>

양자 컴퓨터가 현대 암호화 체계를 무너뜨릴 것이라는 'Q-Day'의 경고는 더 이상 공상 과학의 영역에 머물지 않습니다. 글로벌 보안 거인 Cloudflare가 WARP 클라이언트에 <a href="/ko/glossary/post-quantum-cryptography" class="glossary-tooltip" data-definition="양자 컴퓨터의 계산 능력으로도 해독할 수 없는 차세대 암호화 알고리즘 체계">Post-Quantum Cryptography</a>를 전격 도입한 것은 고무적인 신호이지만, 기술적 이면을 들여다보면 우리는 아직 '반쪽짜리 방패'를 들고 있을 뿐이라는 사실을 깨닫게 됩니다. 이번 분석에서는 Cloudflare의 PQC 선언이 가진 실제적인 가치와 그 뒤에 숨겨진 치명적인 공백을 보안 아키텍트의 시각에서 냉철하게 짚어보겠습니다.

## 1. 현재의 PQC 지원이 'HNDL' 공격에만 치중된 이유

### 키 합의(ML-KEM) 도입과 디지털 서명(ML-DSA) 부재의 간극

Cloudflare가 가장 먼저 도입한 ML-KEM(Module-Lattice-Based Key-Encapsulation Mechanism)은 데이터를 암호화하기 위한 비밀 키를 안전하게 생성하고 공유하는 기술입니다. 이는 현재의 암호화된 트래픽을 미리 수집한 뒤 미래에 해독하려는 <a href="/ko/glossary/harvest-now-decrypt-later" class="glossary-tooltip" data-definition="현재의 암호화된 트래픽을 수집해두었다가 미래에 강력한 양자 컴퓨터가 개발되면 해독하려는 공격">Harvest-now-decrypt-later</a> 공격을 방어하는 데 매우 효과적인 수단입니다. 하지만 암호화 통신의 또 다른 축인 '디지털 서명' 분야는 여전히 고전적인 RSA나 타원 곡선 암호(ECC)에 의존하고 있어, 서버의 정당성을 증명하는 단계에서는 여전히 양자 위협에 노출되어 있습니다.

### 능동적 공격(MITM)에 여전히 노출된 현재의 PQC 터널링 구조

디지털 서명이 빠진 PQC 터널은 마치 금고의 자물쇠는 최첨단으로 바꿨지만, 정작 금고 주인의 신분증은 위조하기 쉬운 종이 조각인 상태와 같습니다. 공격자가 실시간으로 개입하여 가짜 인증서를 내미는 중간자 공격(MITM) 환경에서는 ML-KEM만으로 구축된 보안 터널이 무력해질 가능성이 큽니다. NIST의 FIPS 204 표준인 ML-DSA가 인프라 전반에 완전히 녹아들기 전까지는, 지금의 PQC는 수동적 감청을 막는 제한적인 방어 체계에 머무를 수밖에 없습니다.

![Post-Quantum Cryptography - 암호화 기술을 상징하는 빛나는 회로가 중심에 있고, 가장자리에는 디지털 서명 누락을 나타내는 미세한 균열이 있는 유리 질감의 디지털 금고입니다.](../../../../../source/posts/Post-Quantum_Cryptography/26fc91f8-0.webp)

## 2. 종단 간(End-to-End) 양자 보안의 거대한 공백: 오리진 서버의 한계

### WARP 클라이언트가 해결하지 못하는 '라스트 마일' 보안 위험

사용자가 WARP를 통해 Cloudflare 에지(Edge) 서버까지 안전하게 연결되었다 하더라도, 에지 서버에서 실제 데이터가 저장된 오리진 서버까지의 구간이 문제입니다. 이 구간에서 여전히 고전 암호 체계가 사용된다면 전체 보안 체인은 결국 가장 약한 고리에서 끊어지게 됩니다. 보안 아키텍처에서 말하는 이 '라스트 마일'의 부재는 기업들이 Cloudflare의 PQC 지원을 곧바로 전체 인프라의 안전으로 오해해서는 안 되는 핵심적인 이유입니다.

### 자동 SSL/TLS 업그레이드의 기술적 장벽과 표준화 이슈

Cloudflare는 Automatic SSL/TLS 기능을 통해 오리진 서버와의 연결을 업그레이드하려 노력 중이지만, 하드웨어 호환성과 성능 저하라는 거대한 벽에 부딪혀 있습니다. ML-KEM은 고전 암호에 비해 키 사이즈가 월등히 크기 때문에 네트워크 패킷의 단편화나 핸드쉐이크 지연 시간을 초래할 수 있습니다. 이러한 기술적 부채를 해결하지 못한 채 마케팅적 수사로만 PQC를 강조하는 것은 실질적인 보안 강화보다는 브랜드 이미지 제고에 가깝다는 비판을 피하기 어렵습니다.

[이미지: An abstract visualization of a data bridge made of translucent glass blocks, where the first half is glowing with quantum energy and the second half is crumbling into wireframe, symbolizing the broken security chain between edge and origin servers, soft blue and orange studio lighting]

## 3. 안드로이드 17의 하드웨어 기반 PQC 전략과의 비교 분석

### OS 레벨의 신뢰 체인(Chain of Trust) 구축과 네트워크 계층 보안의 차이

클라우드 서비스인 Cloudflare와 달리, 구글의 안드로이드 17은 보다 근본적인 접근 방식을 택하고 있습니다. 하드웨어 레벨의 안드로이드 검증 부팅(AVB) 단계에 ML-DSA를 통합함으로써 부팅 시점부터 양자 저항성을 확보하는 전략을 보여줍니다. 이는 네트워크 계층에서만 보안을 덧씌우는 방식보다 훨씬 강력한 '신뢰의 뿌리'를 제공하며, 운영체제 전반의 무결성을 보장하는 데 결정적인 차이를 만듭니다.

### 기업용 클라이언트(Cloudflare One) 사용자들을 위한 실질적 대응 가이드

현재 Cloudflare One을 사용하는 기업 보안 관리자들은 단순히 버튼 하나로 PQC 설정을 켜는 것에 만족해서는 안 됩니다. MDM(Mobile Device Management) 정책을 통해 'PQC Only' 모드를 강제하고, 공격자가 보안 수준을 강제로 낮추는 다운그레이드 공격을 시도할 수 없도록 엄격한 정책 오버라이드를 적용해야 합니다. 또한, 내부 오리진 서버의 라이브러리를 최신 NIST 표준에 맞게 업데이트하는 작업을 병행해야만 진정한 양자 내성 아키텍처를 완성할 수 있습니다.

| 보안 주체 | 적용 알고리즘 | 주요 보안 계층 | NIST 표준 준수 및 권위 |
| :--- | :--- | :--- | :--- |
| Cloudflare | ML-KEM (키 합의) | 네트워크/터널링 (MASQUE) | FIPS 203 (ML-KEM-768 하이브리드) |
| Android 17 | ML-DSA (디지털 서명) | 하드웨어/커널 (AVB) | FIPS 204 (Chain of Trust) |
| Cisco (SKIP) | PSK-DHE / ML-KEM | VPN/IPSec 인프라 | IOS-XE 기반 글로벌 표준화 선점 |
| Google Play | ML-DSA (하이브리드 서명) | 애플리케이션 유통 계층 | 앱 무결성 검증 및 위변조 방지 |

> "PQC 터널링은 '수확 후 해독'이라는 정적인 위협은 차단하지만, 디지털 서명이 빠진 현재의 구조는 중간자 공격(MITM)이라는 능동적 위협 앞에서는 여전히 고전적인 방패일 뿐이다."

> "안드로이드 17이 하드웨어 기반의 신뢰 체인을 구축하며 근본적 보안을 강화하는 반면, 클라우드 에지 보안은 여전히 오리진 서버와의 표준화 격차라는 기술적 부채에 직면해 있다."

## 결론: Q-Day를 향한 진정한 보안 자립, 마케팅 용어 너머의 인프라 혁신이 핵심이다

양자 보안은 단순한 체크박스 옵션이 아니라 인프라 전체의 패러다임 전환을 의미합니다. Cloudflare의 행보는 분명 올바른 방향을 향하고 있지만, 디지털 서명의 부재와 오리진 서버의 고립은 우리가 해결해야 할 숙제로 남아 있습니다. 기술의 화려함 뒤에 숨겨진 취약점을 명확히 인지하고, 단계적인 인프라 고도화를 실천할 때 비로소 우리는 다가올 양자 시대를 안전하게 맞이할 수 있을 것입니다.

* NIST 및 업계 양자 보안 대응 현황:
  - **45% 이상**: Cloudflare로 전송되는 인간 생성 트래픽 중 이미 포스트 양자 암호화가 적용된 비율.
  - **2030년**: NIST 가이드라인에 따라 112비트 이하 고전 암호(RSA, ECC) 알고리즘 사용이 공식 중단(Deprecated)되는 시점.
  - **2035년**: 고전 암호 알고리즘 사용이 전면 금지(Disallowed)되며, 모든 연방 보안 시스템은 PQC로 완전 전환되어야 하는 최종 기한.
  - **5-15년**: 전문가들이 예상하는 암호학적으로 유효한 양자 컴퓨터(CRQC) 등장 및 현대 암호 체계 붕괴 시점.

## 🔗 함께 읽으면 좋은 글
- [러스트(Rust)의 역설: 혁신적 안전성이 초래한 경영의 병목과 생산성 위기](/ko/posts/rust-paradox-safety-productivity)
- [Warp의 오픈소스 선언: 에이전트 우선 시대, 개발자의 자유인가 AI의 종속인가?](/ko/posts/warp-open-source-agent-first-era)