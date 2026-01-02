---
title: "SSU2 트랜스포트"
date: 2022-10-11
author: "zzz"
description: "SSU2 트랜스포트"
categories: ["development"]
---

## 개요

I2P는 2005년부터 검열 저항성이 있는 UDP 전송 프로토콜 "SSU"를 사용해 왔습니다. 지난 17년 동안 SSU가 차단되었다는 보고는 거의, 혹은 전혀 없었습니다. 그러나 보안, 차단 저항성, 성능에 대한 오늘날의 기준으로 보면, 우리는 더 개선할 수 있습니다. 훨씬 더요.

이러한 이유로, [i2pd project](https://i2pd.xyz/)와 함께 우리는 최고 수준의 보안 및 차단 저항성(blocking resistance) 표준에 맞춰 설계된 현대적인 UDP 프로토콜인 "SSU2"를 개발하고 구현했습니다. 이 프로토콜은 SSU를 대체할 것입니다.

우리는 업계 표준 암호화를 UDP 프로토콜인 WireGuard와 QUIC의 최고의 기능, 그리고 우리의 TCP 프로토콜 "NTCP2"의 검열 저항 기능과 결합했습니다. SSU2는 지금까지 설계된 전송 프로토콜 가운데 가장 안전한 것들 중 하나일 수 있습니다.

Java I2P 및 i2pd 팀은 SSU2 transport(전송 프로토콜)를 마무리하고 있으며, 다음 릴리스에서 모든 routers에서 이를 활성화할 것입니다. 이는 2003년으로 거슬러 올라가는 원래의 Java I2P 구현에서 비롯된 모든 암호화를 업그레이드하려는 10년에 걸친 우리의 계획을 완성합니다. SSU2는 SSU를 대체할 것이며, SSU는 우리가 ElGamal 암호화를 사용하는 유일하게 남은 사용처입니다.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

SSU2로의 전환이 완료되면, 우리의 인증되고 암호화된 모든 프로토콜을 표준 [Noise Protocol](https://noiseprotocol.org/) 핸드셰이크로 이전하게 됩니다:

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

모든 I2P Noise 프로토콜은 다음의 표준 암호 알고리즘을 사용합니다:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## 목표

오직 번역만 제공하고, 그 외에는 아무것도 포함하지 마십시오:

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## 설계

I2P는 공격자로부터 트래픽을 보호하기 위해 여러 계층의 암호화를 사용합니다. 가장 하위 계층은 두 routers 간의 포인트-투-포인트 링크에 사용되는 전송 프로토콜 계층입니다. 현재 두 가지 전송 프로토콜이 있습니다: 2018년에 도입된 현대적인 TCP 프로토콜인 NTCP2와, 2005년에 개발된 UDP 프로토콜인 SSU입니다.

SSU2는 이전 I2P 전송 프로토콜과 마찬가지로, 데이터용 범용 파이프가 아니다. 그 주된 역할은 한 router에서 다음 router로 I2P의 저수준 I2NP 메시지를 안전하게 전달하는 것이다. 이러한 점대점(point-to-point) 연결 각각은 I2P tunnel에서 하나의 홉을 이룬다. 상위 계층 I2P 프로토콜은 이러한 점대점 연결 위에서 동작하여 I2P의 destinations 간에 garlic 메시지를 종단 간으로 전달한다.

UDP 전송을 설계하는 일은 TCP 기반 프로토콜에는 존재하지 않는 고유하고 복잡한 과제를 제시한다. UDP 프로토콜은 주소 스푸핑으로 인해 발생하는 보안 문제를 처리해야 하며, 자체 혼잡 제어를 구현해야 한다. 또한 모든 메시지는 네트워크 경로의 최대 전송 단위(MTU)에 맞도록 단편화되어야 하며, 수신자가 이를 재조립해야 한다.

우리는 먼저 NTCP2, SSU, 그리고 스트리밍 프로토콜에 관한 기존 경험에 크게 의존했습니다. 그 다음, 최근에 개발된 두 가지 UDP 프로토콜을 면밀히 검토하고 거기에서 많은 부분을 차용했습니다:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

국가 수준의 방화벽과 같은 적대적 경로 상(on-path) 공격자에 의한 프로토콜 분류 및 차단은 해당 프로토콜들의 위협 모델에 명시적으로 포함되어 있지 않습니다. 그러나 I2P의 위협 모델에서는 매우 중요한 요소입니다. 우리의 사명은 전 세계의 위험에 처한 사용자들에게 익명성과 검열 저항성을 갖춘 통신 시스템을 제공하는 것이기 때문입니다. 따라서 우리의 설계 작업 상당 부분은 NTCP2와 SSU에서 얻은 교훈을 QUIC과 WireGuard가 제공하는 기능과 보안에 결합하는 것이었습니다.

## 성능

I2P 네트워크는 다양한 router(라우터)가 복합적으로 섞여 있는 구조입니다. 고성능 데이터센터 컴퓨터부터 Raspberry Pi와 Android 폰에 이르기까지 다양한 하드웨어에서 전 세계적으로 실행되는 두 가지 주요 구현체가 있습니다. router는 TCP와 UDP 전송 프로토콜을 모두 사용합니다. SSU2 개선 사항은 상당하지만, 로컬 환경이나 종단 간 전송 속도에서 사용자에게 눈에 띄게 나타나리라고는 예상하지 않습니다.

SSU2와 SSU를 비교했을 때 예상되는 개선 사항의 주요 내용은 다음과 같습니다:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## 전환 계획

I2P는 네트워크 안정성을 보장하고 구형 router가 계속 유용하고 안전하게 기능할 수 있도록 하위 호환성을 유지하려고 노력합니다. 그러나 호환성은 코드 복잡성과 유지보수 요구사항을 증가시키므로 한계가 있습니다.

Java I2P와 i2pd 프로젝트는 둘 다 2022년 11월 말에 출시될 다음 릴리스(2.0.0 및 2.44.0)에서 기본적으로 SSU2를 활성화할 예정이다. 그러나 SSU 비활성화에 대한 계획은 서로 다르다. i2pd는 SSU2가 그들의 SSU 구현에 비해 대폭 향상되었기 때문에 SSU를 즉시 비활성화할 것이다. Java I2P는 점진적인 전환을 지원하고 구형 router(라우터)들이 업그레이드할 시간을 주기 위해 2023년 중반에 SSU를 비활성화할 계획이다.

## 요약


I2P의 창립자들은 암호 알고리즘과 프로토콜에 대해 여러 가지 선택을 해야 했습니다. 그 선택들 가운데 일부는 다른 것들보다 더 나았지만, 20년이 지난 지금 대부분은 노후화의 기미를 보이고 있습니다. 물론 우리는 이런 일이 올 것을 알고 있었고, 지난 10년 동안 암호학적 업그레이드를 계획하고 구현해 왔습니다.

SSU2는 우리의 긴 업그레이드 경로에서 개발해야 했던 마지막이자 가장 복잡한 프로토콜이었습니다. UDP는 전제와 위협 모델이 매우 까다롭습니다. 우리는 먼저 Noise 프로토콜의 다른 세 가지 변형을 설계하고 배포했으며, 그 과정을 통해 보안 및 프로토콜 설계상의 문제에 대한 경험을 쌓고 더 깊이 이해하게 되었습니다.

SSU2는 2022년 11월 말로 예정된 i2pd 및 Java I2P 릴리스에서 활성화될 예정입니다. 업데이트가 원활히 진행되면, 누구도 어떤 변화도 전혀 알아차리지 못할 것입니다. 성능상의 이점은 상당하지만, 대부분의 사용자에게는 아마 측정할 수 없을 것입니다.

항상 그렇듯이, 새 릴리스가 제공되면 업데이트할 것을 권장합니다. 보안을 유지하고 네트워크에 도움을 주는 가장 좋은 방법은 최신 릴리스를 실행하는 것입니다.
