---
title: "그림이 포함된 기본 I2P tunnel 튜토리얼"
date: 2019-06-02
author: "idk"
description: "기본 i2ptunnel 설정"
categories: ["tutorial"]
---

Java I2P router는 사용자의 첫 eepSite를 제공하기 위해 정적 웹 서버인 jetty가 미리 구성되어 있지만, 많은 사용자는 웹 서버에서 더 정교한 기능을 필요로 하며 다른 서버로 eepSite를 만들기를 선호합니다. 물론 이것은 가능하며, 한 번만 해보면 실제로 매우 쉽습니다.

설정 자체는 쉽지만, 실행하기 전에 고려해야 할 몇 가지 사항이 있습니다. 서버/배포판 유형을 보고하는 기본 오류 페이지나 식별에 사용될 수 있는 헤더 등, 웹 서버에서 신원을 식별할 수 있는 특성은 제거하는 것이 좋습니다. 잘못 구성된 애플리케이션이 초래하는 익명성 위협에 대한 더 자세한 정보는 다음을 참고하세요: [Riseup 여기](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix 여기](https://www.whonix.org/wiki/Onion_Services), [일부 OPSEC(운영 보안) 실패 사례를 다룬 이 블로그 글](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [그리고 I2P applications 페이지 여기](https://geti2p.net/docs/applications/supported). 이러한 정보의 상당수는 Tor Onion Services를 기준으로 설명되어 있지만, 동일한 절차와 원칙은 I2P를 통해 애플리케이션을 호스팅할 때도 그대로 적용됩니다.

### 1단계: Tunnel 마법사 열기

127.0.0.1:7657의 I2P 웹 인터페이스로 이동하여 [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr)를 여십시오(로컬호스트로 연결됩니다). 시작하려면 "Tunnel Wizard"라고 표시된 버튼을 클릭하십시오.

### 2단계: 서버 Tunnel 선택

tunnel 마법사는 매우 간단합니다. 우리는 http *서버*를 설정하는 것이므로, 우리가 해야 할 일은 *서버* tunnel을 선택하는 것뿐입니다.

### 3단계: HTTP Tunnel 선택

HTTP tunnel(터널)은 HTTP 서비스를 호스팅하도록 최적화된 tunnel 유형입니다. 그 목적에 특별히 맞춘 필터링 및 요청 속도 제한 기능이 기본으로 활성화되어 있습니다. 표준 tunnel도 사용할 수 있지만, 표준 tunnel을 선택하면 이러한 보안 기능을 직접 처리해야 합니다. HTTP Tunnel 구성에 대한 더 심층적인 설명은 다음 튜토리얼에서 확인할 수 있습니다.

### 4단계: 이름과 설명을 지정하세요

본인이 tunnel(터널)을 무엇에 사용하는지 기억하고 구분하기 쉽도록, 적절한 별칭과 설명을 지정하세요. 나중에 다시 돌아와 추가로 관리해야 할 때, hidden services manager에서 해당 tunnel을 식별하는 기준이 됩니다.

### 5단계: 호스트와 포트 구성

이 단계에서는 웹 서버가 수신 대기 중인 TCP 포트를 가리키도록 설정합니다. 대부분의 웹 서버는 포트 80 또는 포트 8080에서 수신 대기하므로, 예제에서는 이를 사용합니다. 웹 서비스를 격리하기 위해 다른 포트나 가상 머신 또는 컨테이너를 사용하는 경우, 호스트, 포트, 또는 둘 다를 조정해야 할 수 있습니다.

### 6단계: 자동으로 시작할지 결정하기

이 단계에 대해 더 자세히 설명할 방법을 떠올릴 수 없습니다.

### 7단계: 설정을 검토하세요

마지막으로, 선택한 설정을 확인하세요. 괜찮다고 판단되면 저장하세요. tunnel을 자동으로 시작하도록 선택하지 않았다면, 숨은 서비스 관리자에서 서비스를 제공하려는 경우 수동으로 시작하세요.

### 부록: HTTP 서버 사용자 지정 옵션

I2P는 HTTP 서버 tunnel을 다양한 맞춤형 방식으로 구성할 수 있는 상세한 패널을 제공합니다. 저는 그것들을 모두 차례대로 살펴보며 이 튜토리얼을 마무리하겠습니다. 언젠가.
