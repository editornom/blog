---
title: "OAuth 토큰이 열어준 SaaS 공급망 공격의 새로운 이면"
author: "editornom"
pubDatetime: 2026-04-22T09:08:13+09:00
slug: "oauth-supply-chain-security-risks-lessons"
featured: false
draft: false
ogImage: "../../../../../source/posts/OAuth_Supply_Chain_Security/f4692288-0.webp"
description: "신뢰받는 타사 통합 앱의 OAuth 토큰을 탈취해 수백 개 기업의 데이터를 노출시킨 Salesloft와 Gainsight 사례를 통해 현대 SaaS 공급망 보안의 허점과 대응책을 분석합니다."
faqs:
- q: OAuth란 무엇이며 왜 사용하나요?
  a: 비밀번호를 공유하지 않고 제3자 앱에 특정 데이터 접근 권한을 부여하는 프로토콜입니다. 'Google로 로그인'처럼 앱 간 데이터를 안전하고
    편리하게 연동하기 위해 사용하지만, 탈취 시 대리 권한을 남용당할 위험이 있습니다.
- q: OAuth 기반 공급망 공격의 특징은 무엇인가요?
  a: 보안이 강력한 본 시스템을 직접 공격하는 대신, 상대적으로 취약한 연결 앱을 먼저 장악하는 방식입니다. 탈취한 권한을 이용해 신뢰 관계를
    악용하므로, 보안망을 우회하여 내부 데이터에 깊숙이 침투할 수 있습니다.
- q: Salesloft와 Gainsight 사고의 핵심 원인은 무엇인가요?
  a: 공격자들이 서드파티 앱인 Drift를 해킹하여 사용자들의 OAuth '리프레시 토큰'을 대량 탈취한 것이 원인입니다. 이를 통해 Salesforce
    등 연결된 시스템에 MFA 인증 없이도 장기간 지속적으로 접근할 수 있었습니다.
- q: 리프레시 토큰(Refresh Token)이 왜 보안에 더 위험한가요?
  a: 일반 액세스 토큰과 달리 유효 기간이 매우 길기 때문입니다. 사용자가 명시적으로 권한을 철회하기 전까지 유효하므로, 공격자가 한 번 손에
    넣으면 다중 요소 인증(MFA)을 우회하여 지속적으로 데이터를 빼낼 수 있는 통로가 됩니다.
- q: 과도한 '권한 범위(Scope)' 설정은 어떤 문제를 일으키나요?
  a: 앱이 기능 수행에 필요한 것보다 넓은 권한을 가질 때 발생합니다. 예를 들어 단순 챗봇이 CRM 전체 읽기 권한을 가지면, 토큰 탈취 시
    공격자가 연동된 모든 시스템의 데이터를 추출할 수 있어 '폭발 반경'이 기업 전체로 확산됩니다.
- q: 왜 기존 보안 모니터링으로는 이러한 공격을 탐지하기 어렵나요?
  a: 공격자의 데이터 요청이 '이미 승인된 신뢰 앱'의 이름으로 수행되기 때문입니다. 로그상으로는 정상적인 서비스 동기화 작업처럼 보여, 일반적인
    API 사용 패턴과 악성 활동을 구분해내기가 매우 까다롭습니다.
- q: 에이전틱 AI(Agentic AI) 도입이 OAuth 보안 위협을 어떻게 키우나요?
  a: AI 에이전트는 자율적 판단을 위해 기존 앱보다 훨씬 광범위한 권한을 부여받는 경우가 많습니다. AI의 토큰이 탈취되면 단순 유출을 넘어
    메일 발송, 결제 승인, 인프라 설정 변경 등 자율적인 파괴 공작이 가능해집니다.
- q: OAuth 공급망 공격을 막기 위한 '제로 트러스트' 관점의 핵심은 무엇인가요?
  a: 제3자 앱에 대한 신뢰를 당연시하지 않고, 내부 계정과 동일한 수준으로 엄격하게 관리하는 것입니다. '한 번 설정하면 끝'이라는 인식을 버리고,
    모든 연동 권한을 지속적으로 검증하고 거버넌스 아래 두어야 합니다.
- q: 기업이 당장 실천할 수 있는 기술적 대응책은 무엇인가요?
  a: 먼저 SSPM 솔루션 등으로 조직 내 OAuth 연동 현황을 전수 조사해야 합니다. 이후 '최소 권한 원칙'에 따라 불필요하거나 과도한 권한을
    가진 앱을 차단하고, 방치된 리프레시 토큰을 주기적으로 정리해야 합니다.
- q: 이상 징후 탐지를 위해 어떤 모니터링 체계가 필요한가요?
  a: 단순히 접속 여부만 보는 것이 아니라, 앱의 API 호출 패턴을 분석해야 합니다. 특정 앱이 평소보다 과도한 데이터를 가져가는 등의 이상
    패턴이 감지되면, 해당 토큰을 즉시 자동 무효화하는 대응 시스템 구축이 필수적입니다.
references:
- https://www.trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html
- https://www.obsidiansecurity.com/blog/a-guide-to-saas-supply-chain-solutions
- https://cloudsecurityalliance.org/blog/2025/09/25/the-salesloft-drift-oauth-supply-chain-attack-cross-industry-lessons-in-third-party-access-visibility
- https://www.zscaler.com/blogs/product-insights/gainsight-supply-chain-attack-what-it-means-saas-security
- https://appomni.com/learn/saas-security-fundamentals/oauth-token-security-risks/
- https://unit42.paloaltonetworks.com/third-party-supply-chain-token-management/
- https://www.obsidiansecurity.com/blog/what-are-oauth-tokens-vulnerabilities
- https://www.valencesecurity.com/resources/blogs/salesforce-oauth-token-breach-what-every-security-team-must-know
- https://redcanary.com/blog/threat-detection/google-workspace-oauth-attack/
- https://vercel.com/kb/bulletin/vercel-april-2026-security-incident
---

최근 IT 보안의 최전선은 서버 자체의 취약점을 넘어, 시스템 간의 신뢰 관계를 파고드는 양상으로 변하고 있습니다. 특히 2025년 발생한 Salesloft와 Gainsight의 공급망 보안 사고는 우리가 편의를 위해 도입한 OAuth 통합이 어떻게 치명적인 공격 통로가 될 수 있는지 여실히 보여주었습니다.

## 신뢰를 파고드는 취약점, OAuth

협업 효율을 위해 'Google로 로그인'이나 'Salesforce 연동' 버튼을 누르는 것은 이제 일상입니다. 이는 비밀번호를 직접 공유하지 않고도 특정 데이터에 접근할 수 있는 권한을 부여하는 OAuth(Open Authorization) 프로토콜 덕분이죠. 하지만 이 편리한 '대리 권한'이 관리자의 감시망을 벗어나면서 보안의 사각지대가 발생합니다.

2025년 8월의 Salesloft-Drift 보안 사고는 이 구조적 허점을 노린 대표적인 사례입니다. 공격자들은 Salesforce를 직접 타격하는 대신, 상대적으로 보안이 취약한 서드파티 앱 Drift를 먼저 장악했습니다. 이후 사용자들이 Drift에 부여했던 OAuth '리프레시 토큰(Refresh Token)'을 대량으로 탈취하는 방식을 취했습니다.

![OAuth Supply Chain Security - 디지털 네트워크에서 신뢰가 무너지며 빛나던 열쇠들이 어두운 그림자로 변하는 모습.](../../../../../source/posts/OAuth_Supply_Chain_Security/f4692288-0.webp)

## 리프레시 토큰의 영속성과 권한 남용의 위험성

이번 사고에서 주목해야 할 첫 번째 기술적 핵심은 토큰의 수명입니다. 일반적으로 쓰이는 액세스 토큰은 유효 기간이 짧지만, 리프레시 토큰은 사용자가 명시적으로 권한을 철회하기 전까지 장기간 유효한 경우가 많습니다. 공격자들은 이 토큰을 손에 넣음으로써 다중 요소 인증(MFA)을 우회하고, 타깃 기업의 내부 데이터에 지속적으로 접근할 수 있는 통로를 확보했습니다.

두 번째 문제는 '권한 범위(Scope)'의 과도한 설정입니다. 많은 서드파티 앱들이 원활한 구동을 명목으로 필요 이상의 넓은 권한을 요구하곤 해요. 단순한 챗봇 서비스가 'CRM 데이터 전체 읽기/쓰기' 권한을 가지는 식이죠. 공격자들은 탈취한 토큰으로 Salesforce뿐만 아니라 연결된 Google Workspace, Slack까지 넘나들며 데이터를 추출했습니다. 이른바 '폭발 반경(Blast Radius)'이 기업 전체로 확산된 것입니다.

> "제3자에 대한 신뢰는 더 이상 당연한 것이 아닙니다. 내부의 특권 계정만큼이나 엄격하게 지속적으로 검증되고 거버넌스 아래 관리되어야 합니다."

## 기존 보안 모니터링의 한계

Salesloft와 Gainsight 사례에서 보안 팀이 가장 당혹스러웠던 지점은 침해 사실을 즉각 감지하기 어려웠다는 점입니다. 공격자의 데이터 요청이 '이미 승인된, 신뢰할 수 있는 앱'의 이름으로 수행되었기 때문입니다. 보안 로그상으로는 Drift 앱이 평소처럼 데이터를 동기화하는 것으로 보였을 뿐, 그 배후에 공격자가 있다는 사실을 구분해내기란 쉽지 않았습니다.

특히 공격자들은 `Salesforce-Multi-Org-Fetcher/1.0`과 같은 특정 사용자 에이전트 스트링을 사용해 여러 조직의 데이터를 자동화된 방식으로 추출했습니다. 이는 일반적인 사용 패턴과는 확연히 다른 API 중심의 공격 형태였지만, 이미 형성된 신뢰 관계라는 장벽 뒤에 숨어 있었기에 탐지의 사각지대에 놓여 있었던 것입니다.

![OAuth Supply Chain Security - 작은 황금색 기어 하나의 파손으로 인해 전체 수정 구조가 일그러지는 복잡한 기어 시스템의 모습.](../../../../../source/posts/OAuth_Supply_Chain_Security/6dc3d615-1.webp)

## 에이전틱 AI 도입과 보안 위협의 확장

이러한 OAuth 기반의 공급망 공격은 앞으로 더 정교해질 것으로 보입니다. 특히 자율적으로 판단하고 행동하는 '에이전틱 AI(Agentic AI)'가 기업 시스템에 통합되면서 위험 요소는 늘어날 수밖에 없습니다. AI 에이전트가 부여받은 OAuth 토큰은 기존의 단순 앱 연동보다 훨씬 더 광범위하고 강력한 권한을 가질 가능성이 높기 때문입니다.

만약 AI 에이전트가 사용하는 토큰이 탈취된다면, 공격자는 단순히 데이터를 훔치는 수준을 넘어 AI의 권한을 빌려 이메일을 발송하거나 결제를 승인하고, 인프라 설정까지 변경하는 등 자율적인 파괴 공작을 펼칠 수 있습니다. 이제 '앱 대 앱(App-to-App)'을 넘어 'AI 대 앱' 보안 체계를 고민해야 하는 시점입니다.

## 제로 트러스트 관점의 실질적인 대응책

SaaS 연동을 '한 번 설정하면 끝'이라고 생각하는 기존의 관리 방식에서 벗어나야 합니다. 기업 차원에서 고려해야 할 구체적인 대응 방향은 다음과 같습니다.

- **OAuth 가시성 전수 조사**: 조직 내 사용자가 어떤 앱에 어떤 권한을 부여했는지 파악해야 합니다. SSPM(SaaS Security Posture Management) 솔루션 등을 도입해 방치된 연동 앱들을 식별하고 관리하는 것이 우선입니다.
- **최소 권한 원칙(Least Privilege) 적용**: 서드파티 앱이 요구하는 권한이 서비스 목적에 부합하는지 엄격히 심사해야 합니다. 과도한 권한 요구에는 단호히 제한을 두는 거버넌스 구축이 필요합니다.
- **토큰 기반 행동 분석**: 접속 여부만 확인하는 것이 아니라, 특정 앱이 평소보다 과도한 데이터를 가져가는지 등 이상 징후를 모니터링해야 합니다. 이상 패턴 감지 시 해당 토큰을 즉시 무효화하는 자동화된 대응 체계가 뒷받침되어야 합니다.

![OAuth Supply Chain Security - 거대한 네트워크망을 비추며 디지털 안개를 가르는 미래형 등대 불빛.](../../../../../source/posts/OAuth_Supply_Chain_Security/f7a515df-2.webp)

## 연결성의 대가와 보안의 기준점

SaaS 생태계의 긴밀한 연결은 비즈니스 생산성을 높여주지만, 동시에 가장 취약한 공격 루트가 되기도 합니다. Salesloft와 Gainsight 사고는 우리가 누리는 편의 뒤에 어떤 위험이 도사리고 있는지 보여주는 사례입니다.

결국 보안의 핵심은 지속적인 검증입니다. 외부 파트너사가 보안 사고를 당했을 때 우리 시스템까지 무방비로 노출되는 구조라면, 그것은 결코 안전하다고 할 수 없습니다. 제3자 통합 환경을 내부 임직원 계정과 동일한 수준으로 엄격하게 관리하는 것, 그것이 현재의 보안 리더들이 갖춰야 할 새로운 기준입니다. 지금 우리 조직의 '대리 권한'들이 어디서 어떻게 쓰이고 있는지 다시 한번 점검해 보시길 바랍니다.