---
title: "ECIES 목적지를 위한 스트리밍 MTU"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Closed"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## 노트
네트워크 배포 및 테스트 진행 중.
약간의 수정이 있을 수 있음.


## 개요


### 요약

ECIES는 기존 세션(ES) 메시지 오버헤드를 약 90바이트 줄입니다.
따라서 우리는 ECIES 연결을 위해 MTU를 약 90바이트 증가시킬 수 있습니다.
See the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/)를 참조하세요.

MTU를 증가시키지 않는다면, 많은 경우에 오버헤드 절감이 실제로 '절감되지' 않으며,
메시지들이 어차피 두 개의 전체 터널 메시지로 패딩될 것입니다.

이 제안은 사양 변경을 요구하지 않습니다.
추천 값과 구현 세부 사항의 토론 및 합의 구축을 위해 제안으로 게시되었습니다.


### 목표

- 협상된 MTU 증가
- 1KB 터널 메시지의 사용 극대화
- 스트리밍 프로토콜 변경 없음


## 설계

기존의 MAX_PACKET_SIZE_INCLUDED 옵션과 MTU 협상을 사용합니다.
스트리밍은 전송 및 수신된 MTU의 최소값을 계속해서 사용합니다.
기본값은 어떤 키가 사용되든 상관없이 모든 연결에 대해 1730으로 유지됩니다.

구현체는 모든 SYN 패킷에 양방향으로 MAX_PACKET_SIZE_INCLUDED 옵션을 포함시키는 것이 권장됩니다,
하지만 이는 요구 사항은 아닙니다.

목적지가 ECIES 전용인 경우, 더 높은 값을 사용합니다(앨리스나 밥이든).
목적지가 듀얼 키인 경우, 동작이 다를 수 있습니다:

듀얼 키 클라이언트가 라우터 외부에 있는 경우(외부 애플리케이션),
원격에서 사용되는 키를 "알지" 못할 수 있으며, 앨리스가 SYN에서 더 높은 값을 요청할 수 있으며, SYN의 최대 데이터는 1730으로 유지됩니다.

듀얼 키 클라이언트가 라우터 내부에 있는 경우, 어떤 키가 사용되는지에 대한 정보가 클라이언트에 알려질 수도 있고, 알려지지 않을 수도 있습니다.
리스셋이 아직 가져오지 않았을 수도 있으며, 내부 API 인터페이스가 클라이언트에 쉽게 그 정보를 제공하지 않을 수 있습니다.
정보가 가능한 경우, 앨리스는 더 높은 값을 사용할 수 있습니다;
그렇지 않은 경우, 앨리스는 협상될 때까지 표준 값인 1730을 사용해야 합니다.

듀얼 키 클라이언트가 밥으로서, 요청 거부 없이 더 높은 값을 응답할 수 있습니다;
그러나 스트리밍에서 상향 협상의 규정이 없으므로, MTU는 1730으로 유지됩니다.


the [Streaming API documentation](/docs/api/streaming/)에 명시된 것처럼,
앨리스에서 밥으로 보낸 SYN 패킷의 데이터는 밥의 MTU를 초과할 수 있습니다.
이것은 스트리밍 프로토콜의 약점입니다.
따라서, 듀얼 키 클라이언트는 전송된 SYN 패킷의 데이터를 1730 바이트로 제한하면서 더 높은 MTU 옵션을 전송해야 합니다.
밥으로부터 더 높은 MTU를 받으면, 앨리스는 보낸 최대 페이로드를 증가시킬 수 있습니다.


### 분석

the [ECIES specification](/docs/specs/ecies/#overhead)에 설명된 대로, 기존 세션 메시지에 대한 ElGamal 오버헤드는
151바이트이며, Ratchet 오버헤드는 69바이트입니다.
따라서, 우리는 ratchet 연결에 대해 MTU를 (151 - 69) = 82바이트 증가시킬 수 있으며,
1730에서 1812로 변경됩니다.


## 사양

the [Streaming API documentation](/docs/api/streaming/)의 MTU 선택 및 협상 섹션에 다음 변경 사항 및 명확성을 추가하십시오.
the [Streaming specification](/docs/specs/streaming/)에 대한 변경 사항은 없습니다.


옵션 i2p.streaming.maxMessageSize의 기본 값은 어떤 키가 사용되든 상관없이 모든 연결에 대해 1730으로 유지됩니다.
클라이언트는 전송 및 수신된 MTU의 최소값을 사용해야 합니다.

네 가지 관련 MTU 상수 및 변수가 있습니다:

- DEFAULT_MTU: 모든 연결에 대해 1730, 변경 없음
- i2cp.streaming.maxMessageSize: 기본 1730 또는 1812, 구성에 의해 변경 가능
- ALICE_SYN_MAX_DATA: 앨리스가 SYN 패킷에 포함할 수 있는 최대 데이터
- negotiated_mtu: 앨리스와 밥의 MTU 중 최소값, 밥에서 앨리스로 SYN ACK에서 사용할 최대 데이터 크기 및 양방향으로 전송되는 모든 후속 패킷에 사용


다섯 가지 경우를 고려하십시오:


### 1) 앨리스 ElGamal 전용
모든 패킷에 1730 MTU.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 기본값: 1730
- 앨리스는 SYN에서 MAX_PACKET_SIZE_INCLUDED를 보낼 수 있음, != 1730이 아닌 경우 요구되지 않음


### 2) 앨리스 ECIES 전용
모든 패킷에 1812 MTU.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize 기본값: 1812
- 앨리스는 SYN에서 MAX_PACKET_SIZE_INCLUDED를 반드시 보내야 함


### 3) 앨리스 듀얼 키이며 밥이 ElGamal인 경우 알고 있음
모든 패킷에 1730 MTU.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 기본값: 1812
- 앨리스는 SYN에서 MAX_PACKET_SIZE_INCLUDED를 보낼 수 있음, != 1730이 아닌 경우 요구되지 않음


### 4) 앨리스 듀얼 키이며 밥이 ECIES인 경우 알고 있음
모든 패킷에 1812 MTU.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize 기본값: 1812
- 앨리스는 SYN에서 MAX_PACKET_SIZE_INCLUDED를 반드시 보내야 함


### 5) 앨리스 듀얼 키이며 밥의 키가 알려져 있지 않음
SYN 패킷의 데이터는 1730으로 제한하면서 SYN 패킷에 1812를 MAX_PACKET_SIZE_INCLUDED로 보냄.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize 기본값: 1812
- 앨리스는 SYN에서 MAX_PACKET_SIZE_INCLUDED를 반드시 보내야 함


### 모든 경우에 대해

앨리스와 밥은
negotiated_mtu를 계산하며, 이는 앨리스와 밥의 MTU 중 최소값으로, 밥에서 앨리스로 SYN ACK 및 양방향으로 전송되는 모든 후속 패킷에서 최대 데이터 크기로 사용됩니다.


## 정당성

현재 값이 1730인 이유는 the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220)을 참조하세요.
ECIES 오버헤드가 ElGamal보다 82바이트 적은 이유는 the [ECIES specification](/docs/specs/ecies/#overhead)를 참조하세요.


## 구현 노트

스트리밍이 최적의 크기의 메시지를 생성 중이라면, ECIES-Ratchet 레이어가 그 이상의 패딩을 추가하지 않도록 하는 것이 매우 중요합니다.

두 개의 터널 메시지에 맞도록 최적화된 갈릭 메시지의 사이즈는,
16 바이트 갈릭 메시지 I2NP 헤더, 4 바이트 갈릭 메시지 길이,
8 바이트 ES 태그, 16 바이트 MAC을 포함하여 1956 바이트입니다.

ECIES에서 추천되는 패딩 알고리즘은 다음과 같습니다:

- 갈릭 메시지의 총 길이가 1954-1956 바이트인 경우,
  패딩 블록을 추가하지 않음 (공간 없음)
- 갈릭 메시지의 총 길이가 1938-1953 바이트인 경우,
  정확히 1956 바이트가 되도록 패딩 블록을 추가.
- 그렇지 않으면, 일반적인 방식대로 패딩, 예를 들어 0-15 바이트의 랜덤 양으로.

유사한 전략은 최적의 한 터널 메시지 크기(964 바이트) 및 세 개의 터널 메시지 크기(2952 바이트)에서도 사용될 수 있지만, 이러한 크기는 실제로 드문 경우일 것입니다.


## 문제점

1812 값은 예비 값입니다. 확인 및 조정 가능성이 있습니다.


## 마이그레이션

역호환성 문제 없음.
이것은 기존 옵션이며 MTU 협상은 이미 사양의 일부입니다.

이전 ECIES 목적지는 1730을 지원할 것입니다.
더 높은 값을 수신한 모든 클라이언트는 1730으로 응답할 것이며, 원격 끝은 보통 하향 협상할 것입니다.


