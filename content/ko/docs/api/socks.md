---
title: "SOCKS 프록시"
description: "I2P의 SOCKS tunnel 안전하게 사용하기"
slug: "socks"
aliases:
  - "/ko/socks"
  - "/ko/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS와 SOCKS 프록시 {#overview}

SOCKS 프록시는 릴리스 0.7.1부터 작동합니다. SOCKS 4/4a/5가 지원됩니다. i2ptunnel에서 SOCKS 클라이언트 tunnel을 생성하여 SOCKS를 활성화하세요. 공유 클라이언트와 비공유 클라이언트 모두 지원됩니다. SOCKS outproxy가 없으므로 사용이 제한적입니다.

[FAQ](/docs/overview/faq#socks)에서 설명하는 바와 같이:

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
그리고 2005년 이메일에서 인용하면:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
I2P 위에 임의의 클라이언트를 그냥 연결하고 보안과 익명성에 대한 행동과 노출된 프로토콜을 감사하지 않고도 잘 작동할 것이라고 기대하는 것은 순진한 생각입니다. 익명성을 위해 특별히 설계된 경우가 아닌 이상 거의 *모든* 애플리케이션과 프로토콜이 익명성을 침해하며, 심지어 익명성을 위해 설계된 경우에도 대부분이 그렇습니다. 이것이 현실입니다. 최종 사용자들은 익명성과 보안을 위해 설계된 시스템으로 더 잘 서비스받을 수 있습니다. 기존 시스템을 익명 환경에서 작동하도록 수정하는 것은 쉬운 일이 아니며, 기존 I2P API를 단순히 사용하는 것보다 몇 배나 더 많은 작업이 필요합니다.

SOCKS proxy는 표준 주소록 이름을 지원하지만 Base64 대상은 지원하지 않습니다. Base32 해시는 릴리스 0.7부터 작동해야 합니다. 이는 나가는 연결만 지원합니다. 즉, I2PTunnel 클라이언트입니다. UDP 지원은 스텁이 구현되어 있지만 아직 작동하지 않습니다. 포트 번호별 아웃프록시 선택은 스텁이 구현되어 있습니다.

## 참고 항목 {#see-also}

- 회의 81 (2004년 3월 16일)과 회의 82 (2004년 3월 23일)의 회의록.
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## 만약 무언가가 작동하게 된다면 {#working}

알려주시기 바랍니다. 그리고 SOCKS 프록시의 위험성에 대해 충분한 경고를 제공해 주시기 바랍니다.
