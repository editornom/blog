---
title: 임의 코드 실행(ACE)이란?
author: editornom
author_role: Senior Tech Editor
author_url: https://editornom.com/about
pubDatetime: 2026-05-07 17:28:53.718744+09:00
slug: what-is-arbitrary-code-execution
featured: false
draft: false
ogImage: ../../../../assets/images/placeholder.png
description: 임의 코드 실행(ACE)은 시스템 취약점을 악용해 공격자가 의도한 비인가 코드를 실행하는 치명적인 보안 결함입니다. ACE의
  정의와 위험성, 그리고 MCP 환경에서의 구체적인 발생 사례를 통해 시스템 제어권을 위협하는 보안 경로를 상세히 알아봅니다.
references: []
modDatetime: 2026-05-07 17:38:53.718744+09:00
---

# 임의 코드 실행(ACE)이란?

### 사전적 정의 (Dictionary Definition)
임의 코드 실행(Arbitrary Code Execution, ACE)은 공격자가 시스템이나 애플리케이션의 취약점을 악용하여 대상 컴퓨터 또는 프로세스상에서 자신이 의도한 임의의 명령어와 소프트웨어를 실행할 수 있는 보안 결함입니다. 공격자는 이 취약점을 통해 시스템의 제어권을 획득하거나 데이터를 변조, 탈취할 수 있으며, 이는 시스템 보안 경계를 완전히 무너뜨리는 고위험군 위협으로 분류됩니다.

### 실무 사용 예시 (Practical Use Case)
Model Context Protocol(MCP) 환경에서 호스트가 서버의 기능을 탐색하는 'Capability Discovery' 단계 중에 발생할 수 있습니다. 신뢰할 수 없는 서버가 악성 코드가 포함된 도구(Tools) 스키마를 호스트에 제공하고, LLM이 이를 정상적인 도구로 오인하여 실행하도록 유도되는 경우, 해당 시스템 내부에서 공격자가 의도한 비인가 코드가 실행되는 ACE 경로가 형성됩니다.

### 관련 단어 (Related Words)
- RCE (Remote Code Execution)
- 권한 상승 (Privilege Escalation)
- 취약점 공격 (Exploit)