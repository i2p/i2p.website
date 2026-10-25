---
title: "ElGamal/AES + SessionTag 암호화"
description: "ElGamal, AES, SHA-256, 그리고 일회성 세션 태그를 결합한 레거시 종단 간 암호화"
slug: "elgamal-aes"
aliases:
  - "/ko/how_elgamalaes"
  - "/ko/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## 개요

ElGamal/AES+SessionTags가 종단 간 암호화에 사용됩니다.

신뢰할 수 없고 순서가 보장되지 않는 메시지 기반 시스템인 I2P는 비대칭 및 대칭 암호화 알고리즘의 간단한 조합을 사용하여 garlic 메시지에 데이터 기밀성과 무결성을 제공합니다. 전체적으로 이 조합은 ElGamal/AES+SessionTags라고 불리지만, 이는 2048bit ElGamal, AES256, SHA256, 그리고 32바이트 nonce의 사용을 설명하기에는 지나치게 장황한 방식입니다.

router가 다른 router에게 garlic 메시지를 처음 암호화하려고 할 때, AES256 세션 키의 키잉 자료를 ElGamal로 암호화하고 암호화된 ElGamal 블록 뒤에 AES256/CBC 암호화된 페이로드를 덧붙입니다. 암호화된 페이로드 외에도, AES 암호화 섹션에는 페이로드 길이, 암호화되지 않은 페이로드의 SHA256 해시, 그리고 다수의 "session tags" - 랜덤 32바이트 nonce들이 포함됩니다. 다음번에 송신자가 다른 router에게 garlic 메시지를 암호화하려고 할 때, 새로운 세션 키를 ElGamal로 암호화하는 대신 이전에 전달된 session tags 중 하나를 선택하고 해당 session tag와 함께 사용된 세션 키를 사용하여 이전과 같이 페이로드를 AES 암호화하되, session tag 자체를 앞에 붙입니다. router가 garlic 암호화된 메시지를 받으면, 처음 32바이트가 사용 가능한 session tag와 일치하는지 확인합니다. 일치하면 단순히 메시지를 AES 복호화하지만, 일치하지 않으면 첫 번째 블록을 ElGamal 복호화합니다.

각 세션 태그는 내부 적대자가 서로 다른 메시지를 동일한 router 간의 통신으로 불필요하게 연관짓는 것을 방지하기 위해 한 번만 사용될 수 있습니다. ElGamal/AES+SessionTag 암호화된 메시지의 발신자는 언제 얼마나 많은 태그를 전달할지 선택하여, 수신자에게 일련의 메시지들을 처리할 수 있을 만큼 충분한 태그를 미리 제공합니다. Garlic 메시지는 작은 추가 메시지를 clove로 묶어서("delivery status message") 성공적인 태그 전달을 감지할 수 있습니다 - garlic 메시지가 의도된 수신자에게 도착하여 성공적으로 복호화되면, 이 작은 delivery status 메시지가 노출된 clove 중 하나가 되며, 수신자가 해당 clove를 원래 발신자에게 다시 전송하도록 하는 지시사항을 포함합니다(물론 inbound tunnel을 통해서). 원래 발신자가 이 delivery status 메시지를 받으면, garlic 메시지에 묶인 세션 태그들이 성공적으로 전달되었음을 알 수 있습니다.

Session tags 자체는 짧은 수명을 가지며, 사용되지 않으면 폐기됩니다. 또한 각 키에 대해 저장되는 양이 제한되어 있으며, 키 자체의 수도 제한됩니다 - 너무 많이 도착하면 새 메시지나 오래된 메시지가 삭제될 수 있습니다. 발신자는 session tags를 사용하는 메시지가 제대로 전달되고 있는지 추적하며, 충분한 통신이 없으면 이전에 제대로 전달된 것으로 가정했던 것들을 삭제하고 완전한 비용이 많이 드는 ElGamal 암호화로 되돌아갈 수 있습니다. 세션은 모든 tags가 소진되거나 만료될 때까지 계속 존재합니다.

세션은 단방향입니다. 태그는 Alice에서 Bob으로 전달되고, Alice는 이후 Bob에게 보내는 메시지에서 태그를 하나씩 사용합니다.

세션은 Destination 간, router 간, 또는 router와 Destination 간에 설정될 수 있습니다. 각 router와 Destination은 Session Key와 Session Tag를 추적하기 위해 자체적인 Session Key Manager를 유지합니다. 별도의 Session Key Manager는 적대자가 여러 Destination을 서로 또는 router에 연결하여 추적하는 것을 방지합니다.

## 메시지 수신

수신된 각 메시지는 다음 두 가지 조건 중 하나를 가집니다:

1. 기존 세션의 일부이며 Session Tag와 AES 암호화 블록을 포함합니다
2. 새 세션용이며 ElGamal과 AES 암호화 블록을 모두 포함합니다

router가 메시지를 수신하면, 먼저 기존 세션에서 온 것으로 가정하고 Session Tag를 찾아서 AES를 사용하여 다음 데이터를 복호화를 시도합니다. 이것이 실패하면, 새로운 세션을 위한 것으로 가정하고 ElGamal을 사용하여 복호화를 시도합니다.

## 새 세션 메시지 사양 {#new}

새로운 세션 ElGamal 메시지는 두 부분으로 구성됩니다: 암호화된 ElGamal 블록과 암호화된 AES 블록입니다.

암호화된 메시지에는 다음이 포함됩니다:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### ElGamal 블록

암호화된 ElGamal 블록은 항상 514바이트 길이입니다.

암호화되지 않은 ElGamal 데이터는 222바이트 길이로 다음을 포함합니다:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
32바이트 [Session Key](/docs/specs/common-structures#type_SessionKey)는 세션의 식별자입니다. 32바이트 Pre-IV는 뒤따르는 AES 블록의 IV를 생성하는 데 사용됩니다. IV는 Pre-IV의 SHA-256 해시의 첫 16바이트입니다.

222바이트 페이로드는 [ElGamal을 사용하여](/docs/specs/cryptography#elgamal) 암호화되며, 암호화된 블록의 길이는 514바이트입니다.

### AES 블록 {#aes}

AES 블록의 암호화되지 않은 데이터에는 다음이 포함됩니다:

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### 정의

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
최소 길이: 48바이트

그런 다음 데이터는 ElGamal 섹션의 세션 키와 IV(pre-IV에서 계산됨)를 사용하여 [AES 암호화](/docs/specs/cryptography)됩니다. 암호화된 AES 블록 길이는 가변적이지만 항상 16바이트의 배수입니다.

#### 참고사항

- 실제 최대 페이로드 길이와 최대 블록 길이는 64 KB 미만입니다. [I2NP Overview](/docs/protocol/i2np)를 참조하세요.
- New Session Key는 현재 사용되지 않으며 절대 존재하지 않습니다.

## 기존 세션 메시지 명세 {#existing}

성공적으로 전달된 session tag들은 사용되거나 폐기될 때까지 짧은 기간(현재 15분) 동안 기억됩니다. tag는 AES 암호화 블록만을 포함하고 ElGamal 블록이 앞에 오지 않는 Existing Session Message에 하나씩 포장하여 사용됩니다.

기존 세션 메시지는 다음과 같습니다:

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### 정의

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
session tag는 또한 pre-IV 역할을 합니다. IV는 sessionTag의 SHA-256 해시의 처음 16바이트입니다.

기존 세션에서 메시지를 디코딩하려면, router가 Session Tag를 조회하여 연결된 Session Key를 찾습니다. Session Tag가 발견되면, 연결된 Session Key를 사용하여 AES 블록이 복호화됩니다. 태그가 발견되지 않으면, 메시지는 [New Session Message](#new)로 간주됩니다.

## 세션 태그 구성 옵션 {#config}

릴리즈 0.9.2부터 클라이언트는 현재 세션에 대해 전송할 기본 Session Tag 수와 낮은 태그 임계값을 구성할 수 있습니다. 짧은 스트리밍 연결이나 데이터그램의 경우, 이러한 옵션을 사용하여 대역폭을 크게 줄일 수 있습니다. 자세한 내용은 [I2CP 옵션 명세](/docs/protocol/i2cp#options)를 참조하세요. 세션 설정은 메시지별로도 재정의할 수 있습니다. 자세한 내용은 [I2CP Send Message Expires 명세](/docs/specs/i2cp#msg_SendMessageExpires)를 참조하세요.

## 향후 작업 {#future}

**참고:** ElGamal/AES+SessionTags는 ECIES-X25519-AEAD-Ratchet (제안 144)로 대체되고 있습니다. 아래에서 언급된 문제점과 아이디어들은 새로운 프로토콜의 설계에 반영되었습니다. 다음 항목들은 ElGamal/AES+SessionTags에서는 해결되지 않을 것입니다.

Session Key Manager의 알고리즘을 조정할 수 있는 많은 영역이 있습니다. 일부는 스트리밍 라이브러리 동작과 상호 작용하거나 전반적인 성능에 상당한 영향을 미칠 수 있습니다.

- 전달되는 태그의 수는 메시지 크기에 따라 달라질 수 있으며, tunnel 메시지 계층에서 최종적으로 1KB로 패딩되는 것을 고려해야 합니다.

- 클라이언트는 필요한 태그 수에 대한 권고사항으로 세션 수명 추정치를 router에 전송할 수 있습니다.

- 너무 적은 수의 태그가 전달되면 router가 비용이 많이 드는 ElGamal 암호화로 되돌아가게 됩니다.

- router는 Session Tag의 전달을 가정하거나, 사용하기 전에 확인응답을 기다릴 수 있습니다;
  각 전략마다 장단점이 있습니다.

- 매우 짧은 메시지의 경우, 세션을 설정하는 대신 ElGamal 블록의 pre-IV와 패딩 필드의 거의 전체 222바이트를 전체 메시지에 사용할 수 있습니다.

- 패딩 전략을 평가하세요; 현재 최소 128바이트로 패딩하고 있습니다.
  패딩하는 것보다 작은 메시지에 몇 개의 태그를 추가하는 것이 더 좋을 것입니다.

- Session Tag 시스템이 양방향이라면 더 효율적일 수 있습니다.
  '순방향' 경로에서 전달된 태그를 '역방향' 경로에서 사용할 수 있어
  초기 응답에서 ElGamal을 피할 수 있기 때문입니다.
  router는 현재 자신에게 tunnel 테스트 메시지를 보낼 때
  이런 방식의 트릭을 사용합니다.

- Session Tags에서 
  [동기화된 PRNG](/docs/overview/performance#future#prng)로 변경.

- 이러한 아이디어들 중 일부는 새로운 I2NP 메시지 유형이 필요하거나,
  [Delivery Instructions](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions)에서
  플래그를 설정하거나, Session Key 필드의 처음 몇 바이트에 매직 넘버를 설정하고
  랜덤 Session Key가 매직 넘버와 일치할 작은 위험을 감수해야 할 수 있습니다.
