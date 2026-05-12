---
title: '사용자 동의 없는 4GB 다운로드: 구글 크롬이 몰래 설치한 Gemini Nano와 온디바이스 AI의 역설'
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-12 11:15:00+09:00
slug: chrome-silent-gemini-nano-download-controversy
featured: false
draft: false
ogImage: "../../../../../source/posts/chrome_silent_gemini_nano/og-image.webp"
description: 구글 크롬 브라우저가 사용자 동의 없이 4GB 분량의 Gemini Nano 온디바이스 AI 모델을 무단 설치해 논란이 일고 있습니다. 디스크 및 대역폭 남용 문제와 온디바이스 AI 시대의 프라이버시, 해결 방법을 입체적으로 분석합니다.
references:
- https://www.bleepingcomputer.com/news/google/google-chrome-is-silently-downloading-gemini-nano-ai-model-on-desktops/
- https://www.androidauthority.com/chrome-gemini-nano-download-3465812/
modDatetime: 2026-05-12 11:15:00+09:00
faqs:
- q: 크롬이 왜 사용자 동의 없이 Gemini Nano를 다운로드했나요?
  a: 구글은 크롬 내에서 제공되는 온디바이스 AI 기능(Help me write, 탭 정리, AI 방문 기록 검색 등)을 클라우드 서버 전송 없이 로컬에서 빠르고 안전하게 처리하기 위해 사용자 하드웨어가 조건에 맞을 경우 백그라운드에서 자동으로 모델을 다운로드하도록 설계했습니다.
- q: 내 컴퓨터에 이 모델이 설치되어 있는지 어떻게 확인하나요?
  a: 크롬 주소창에 `chrome://components`를 입력한 뒤 'Optimization Guide On Device Model' 항목을 찾거나, 크롬 데이터 폴더 내의 `OptGuideOnDeviceModel` 디렉토리 하위의 약 4GB 크기 `weights.bin` 파일 존재 여부를 통해 확인할 수 있습니다.
- q: 4GB AI 모델이 차지하는 용량을 지우려면 단순히 파일만 삭제하면 되나요?
  a: 단순 파일 삭제로는 해결되지 않습니다. 크롬 내 온디바이스 AI 관련 설정이나 Flag가 켜져 있다면 브라우저가 다시 모델을 자동으로 다운로드하기 때문입니다. 반드시 Flag를 비활성화한 뒤 폴더를 삭제해야 합니다.
- q: 이 무단 다운로드가 왜 큰 논란이 되고 있나요?
  a: 저용량 SSD(128GB/256GB)를 사용하는 노트북 사용자에게 4GB는 큰 부담이며, 종량제 요금제나 모바일 핫스팟 등 제한된 네트워크를 사용하는 환경에서 알림 없이 기가바이트 단위의 대역폭을 소모한 점, 그리고 사용자 제어권(Transparency)을 무시한 강제 AI 탑재라는 측면에서 거센 비판을 받고 있습니다.
- q: 온디바이스 AI 기능을 끄고 모델을 완전히 삭제하는 구체적인 방법은 무엇인가요?
  a: "chrome://flags 주소로 이동하여 Enables optimization guide on device와 같은 온디바이스 AI 관련 플래그를 모두 'Disabled'로 변경하고 재시작한 뒤, 사용자 크롬 데이터 폴더 내의 OptGuideOnDeviceModel 디렉토리를 수동으로 완전히 삭제하시면 됩니다."
---

<div class="bluf"><strong>[BLUF]</strong><p>구글 크롬이 사용자의 명시적 동의 없이 백그라운드에서 4GB 용량의 온디바이스 AI 모델 'Gemini Nano'를 강제 설치하며 투명성 논란이 촉발되었습니다. 프라이버시 강화라는 명분 뒤에 숨겨진 자원 독점과 네트워크 무단 소모 문제를 분석하고, 이를 완전히 비활성화 및 삭제하는 실전 가이드를 제공합니다.</p></div>

 인공지능이 클라우드를 넘어 우리의 개인 기기 안으로 들어오는 '온디바이스 AI(On-device AI)'의 흐름은 이제 거스를 수 없는 거대한 물결이 되었어요. 하지만 아무리 뛰어난 기술이라도 사용자의 안방을 예고 없이 무단으로 차지한다면 그것은 혁신이 아닌 침해로 다가오기 마련입니다.

최근 구글 크롬(Google Chrome) 브라우저가 전 세계 수억 명의 사용자 컴퓨터에 수 기가바이트에 달하는 인공지능 모델을 조용히 다운로드해 설치한 사실이 밝혀지며 거센 논란의 중심에 섰습니다.

 ![chrome gemini nano silent - 어둡고 미래 지향적인 분위기 속에서 구글 크롬 로고가 새겨진 투명한 유리 구체 내부로 4GB 분량의 빛나는 마이크로 칩과 복잡한 신경망 데이터가 몰래 흘러 들어가는 극적인 장면입니다.](../../../../../source/posts/chrome_silent_gemini_nano/og-image.webp)

## 1. 쥐도 새도 모르게 들어온 4GB: 사건의 전말

### 1.1 'Optimization Guide'라는 이름의 검은 손
어느 날 갑자기 하드디스크의 용량이 4GB 가까이 증발했다면 무엇을 가장 먼저 의심하시겠어요? 많은 사용자가 대용량 캐시 파일이나 시스템 업데이트를 의심했지만, 범인은 바로 매일 사용하는 크롬 브라우저였습니다.

구글은 크롬 브라우저 내부에 포함된 온디바이스 AI 기능들을 구동하기 위해, 사용자의 로컬 환경에 <a href="/ko/glossary/gemini-nano" class="glossary-tooltip" data-definition="구글이 개발한 온디바이스 최적화 경량 언어 모델로, 클라우드 연결 없이 기기 로컬에서 텍스트 요약, 스마트 답장, 교정 등의 AI 연산을 빠르고 안전하게 처리하는 모델">Gemini Nano</a> 모델을 자동으로 다운로드하기 시작했습니다. 

크롬의 컴포넌트 페이지(`chrome://components`)에 조용히 등장한 <b>'Optimization Guide On Device Model'</b>이 바로 그 실체였으며, 이 파일은 사용자의 로컬 크롬 데이터 디렉토리 아래 약 4GB 크기의 `weights.bin` 파일로 저장되었습니다.

### 1.2 "동의한 적 없는데..." 사용자들이 분노하는 이유
온디바이스 AI는 강력한 성능과 데이터 프라이버시 보호라는 확실한 이점을 제공해요. 그러나 구글의 배포 방식은 심각한 '투명성(Transparency) 결여'라는 치명적인 오점을 남겼습니다.

* <b>네트워크 대역폭 무단 점유</b>: 종량제 요금제(Metered Connection), 모바일 핫스팟, 혹은 네트워크 속도가 제한된 개발 도상국의 사용자들에게 예고 없는 4GB 백그라운드 다운로드는 요금 폭탄과 급격한 네트워크 병목을 야기했습니다.
* <b>디스크 공간 독점</b>: 128GB나 256GB SSD를 탑재한 맥북(Macbook)이나 보급형 노트북 환경에서 4GB는 시스템 전체 안정성을 좌우할 수 있는 결코 무시할 수 없는 귀중한 저장 용량입니다.
* <b>통제권 상실</b>: 브라우저가 스스로 하드웨어 사양(특히 GPU 메모리와 성능)을 스캔한 뒤, 사양이 적합하다고 판단되면 사용자에게 "AI 기능을 사용하겠습니까?"라는 팝업 창 하나 띄우지 않고 일방적으로 거대한 모델을 밀어 넣은 점이 파이어폭스(Firefox)나 사파리(Safari)로의 이탈을 가속화하고 있습니다.

---

## 2. 온디바이스 AI의 역설: 프라이버시 강화인가, 자원 침해인가?

> "클라우드로 내 개인 데이터를 보내지 않아 안전하다는 온디바이스 AI의 매력은, 정작 내 로컬 자원을 허락 없이 강탈하는 침해 행위로 인해 그 가치를 상실했다."

### 2.1 로컬 연산의 명분과 현실의 트레이드오프
구글은 이 모델이 크롬의 스마트 작성 도구('Help me write'), 탭 정리('Tab organizer'), 그리고 AI 기반 방문 기록 검색('History search with AI')을 로컬에서 구현하기 위해 필수적이라고 설명합니다. 데이터를 구글 서버로 전송하지 않고 로컬 기기 내에서 처리하므로 완벽한 개인정보 보호가 가능하다는 명분이지요.

하지만 이는 명백한 트레이드오프를 동반합니다. 클라우드 API를 쓰면 서버 비용은 기업이 부담하지만, 온디바이스 AI는 연산에 필요한 하드웨어 자원(GPU, RAM) 소모와 모델 파일 저장의 의무를 고스란히 <b>사용자의 개인 지갑</b>과 <b>기기 수명</b>으로 전가하기 때문입니다.

 ![on device ai private - 인터넷 네트워크 연결선이 완전히 끊겨 완전히 오프라인 상태인 노트북 내부에서 다크 골드 톤으로 반짝이며 스스로 추론 연산을 수행하는 세련된 인공지능 CPU 프로세서 칩셋입니다.](../../../../../source/posts/chrome_silent_gemini_nano/on-device-ai.webp)

### 2.2 메인 성능 데이터 비교 분석
크롬의 Gemini Nano 자동 탑재가 시스템 자원에 미치는 영향력과 리스크 요소를 비교해 보면 다음과 같습니다.

<table style="width:100%; border-collapse: collapse;"><thead><tr style="background-color: #f2f2f2;"><th>리소스 지표</th><th>클라우드 AI 기반 기능</th><th>온디바이스 Gemini Nano 탑재</th></tr></thead><tbody><tr><td>디스크 용량 소모</td><td><strong>0 MB (영향 없음)</strong></td><td>약 3.8GB ~ 4.2GB (`weights.bin` 파일)</td></tr><tr><td>초기 다운로드 대역폭</td><td>없음 (API 호출만 수행)</td><td>최소 1.5GB ~ 2GB 이상의 압축 파일 무단 다운로드</td></tr><tr><td>추론 연산 시 RAM 점유</td><td>미미함 (HTTP 응답 대기 수준)</td><td>구동 시 최소 1GB ~ 2GB 이상의 가용 시스템 메모리 독점</td></tr><tr><td>배터리 및 CPU/GPU 발열</td><td>지극히 낮음</td><td>온디바이스 연산 집중 시 순간 전력 소비 급증 및 발열 발생</td></tr><tr><td>데이터 프라이버시 등급</td><td>보통 (데이터가 외부 서버로 전송됨)</td><td><strong>매우 우수 (로컬 샌드박스 내부에서만 순수 처리)</strong></td></tr></tbody></table>

---

## 3. 원치 않는 4GB 완전 비활성화 및 삭제 가이드 (How-to)

구글은 이 컴포넌트의 수동 삭제를 까다롭게 만들어 두었어요. 단순히 설치된 폴더로 찾아가 `weights.bin` 파일을 지우면, 브라우저가 다시 켜지는 순간 "AI 기능이 활성화 상태"로 인지되어 백그라운드에서 동일한 4GB 데이터를 다시 다운로드하기 시작합니다.

따라서 모델을 완전히 지우고 자동 다운로드를 영구적으로 차단하려면 반드시 <b>'기능 비활성화(Flags Off) -> 수동 삭제'</b>의 2단계 구조를 거쳐야 합니다.

### Step 1: 크롬 실험실(Flags)에서 온디바이스 기능 비활성화하기
1. 크롬 주소창에 `chrome://flags`를 입력하고 접속합니다.
2. 상단 검색창에 `on-device` 혹은 `optimization`을 검색합니다.
3. 다음 플래그들을 찾아 값을 모두 <b>[Disabled]</b>로 강제 변경해 줍니다:
   * `Enables optimization guide on device` (온디바이스 최적화 가이드 비활성화)
   * `Prompt API for Gemini Nano` (Gemini Nano 호출 API 차단)
4. 우측 하단의 <b>[Relaunch]</b> 버튼을 눌러 크롬 브라우저를 완전히 재시작합니다.

### Step 2: 4GB 용량의 로컬 폴더 완전히 삭제하기
플래그를 비활성화하여 크롬의 자동 다운로드 로직을 정지시켰다면, 이제 안심하고 기기에 남아 있는 4GB 좀비 파일을 삭제하여 용량을 확보할 수 있습니다. 운영체제별 크롬 데이터 경로로 이동하여 `OptGuideOnDeviceModel` 폴더 전체를 휴지통에 버려 주세요.

* <b>Windows OS 사용자 경로</b>:
  `%LOCALAPPDATA%\Google\Chrome\User Data\OptGuideOnDeviceModel`
* <b>macOS 사용자 경로</b>:
  `~/Library/Application Support/Google/Chrome/OptGuideOnDeviceModel`

*삭제 완료 후 크롬 주소창에 `chrome://on-device-internals`를 입력해 접속했을 때, 모델 로드 상태가 완전히 정지되어 있거나 비어 있다면 완벽히 성공한 것입니다.*

---

## 4. 결론: 투명성이 담보되지 않는 혁신은 독배에 불과하다

 구글의 이번 '조용한 4GB 배포' 사건은 향후 온디바이스 AI를 도입하고자 하는 모든 글로벌 테크 기업들에게 뼈아픈 교훈을 남겼습니다. 로컬에서 AI를 돌리는 것의 효용과 프라이버시가 아무리 뛰어나더라도, <b>"내 저장 장치와 내 인터넷 데이터는 온전히 나의 통제 하에 있어야 한다"</b>는 사용자 기본 주권을 무시하는 기술은 환영받을 수 없기 때문입니다.

진정한 기술 대기업이라면 혁신적인 기능을 선보이기에 앞서, "더 스마트한 사용을 위해 4GB 모델 설치가 필요합니다. 동의하십니까?"라는 극히 상식적인 질문을 먼저 던지는 정직함과 투명성(Accountability)을 갖추어야 할 것입니다. 

---

## 🔗 함께 읽으면 좋은 글
- [GPT-5.5 vs Claude Opus 4.7: 72%의 토큰 절감이 숨긴 '유지보수 부채'의 경고](/ko/posts/gpt-5-5-vs-claude-opus-4-7-maintenance-debt)
- [AgentOps, 자율 경영의 서막인가 아니면 통제 불능의 '블랙박스'인가?](/ko/posts/agentops-autonomy-or-black-box)
