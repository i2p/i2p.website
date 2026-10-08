---
title: "Tunnel 라우팅"
description: "I2P tunnel 용어, 구성 및 운영 개요"
slug: "tunnel-routing"
lastUpdated: "2026-03"
accurateFor: "0.9.68"
---

## 개요

이 페이지는 I2P tunnel 용어와 작동 방식에 대한 개요를 제공하며, 더 자세한 기술 페이지, 세부사항 및 사양에 대한 링크를 포함합니다.

[소개](/docs/overview/intro/)에서 간략히 설명했듯이, I2P는 가상 "tunnel"을 구축합니다 - 이는 일련의 router를 통한 임시적이고 단방향적인 경로입니다. 이러한 tunnel은 인바운드 tunnel(해당 tunnel에 전달된 모든 것이 tunnel 생성자에게 향하는)이나 아웃바운드 tunnel(tunnel 생성자가 메시지를 자신으로부터 밀어내는) 중 하나로 분류됩니다. Alice가 Bob에게 메시지를 보내고 싶을 때, 그녀는 (일반적으로) 기존의 아웃바운드 tunnel 중 하나를 통해 메시지를 보내며, 해당 tunnel의 엔드포인트가 Bob의 현재 인바운드 tunnel 중 하나의 게이트웨이 router로 전달하도록 지시하고, 이는 차례로 Bob에게 전달합니다.

![Alice가 자신의 outbound tunnel을 통해 Bob의 inbound tunnel을 거쳐 Bob에게 연결하는 모습](/images/tunnelSending.svg)

```
A: Outbound Gateway (Alice)
B: Outbound Participant
C: Outbound Endpoint
D: Inbound Gateway
E: Inbound Participant
F: Inbound Endpoint (Bob)
```
---

## 터널 용어집

- **Tunnel gateway** - tunnel의 첫 번째 router입니다. inbound tunnel의 경우, 이는 [network database](/docs/overview/network-database/)에 게시된 LeaseSet에 언급된 router입니다. outbound tunnel의 경우, gateway는 발신 router입니다. (예: 위의 A와 D 모두)

- **Tunnel endpoint** - tunnel의 마지막 router입니다. (예: 위의 C와 F 모두)

- **터널 참여자** - gateway나 endpoint를 제외한 터널 내의 모든 router들 (예: 위의 B와 E 모두)

- **n-Hop tunnel** - 특정한 수의 라우터 간 점프를 가진 터널, 예를 들어:
  - **0-hop tunnel** - 게이트웨이가 동시에 엔드포인트인 터널
  - **1-hop tunnel** - 게이트웨이가 엔드포인트와 직접 통신하는 터널
  - **2-(또는 그 이상)-hop tunnel** - 최소 하나의 중간 터널 참여자가 있는 터널. (위 다이어그램은 두 개의 2-hop tunnel을 포함합니다 - Alice로부터의 아웃바운드 하나, Bob으로의 인바운드 하나)

- **Tunnel ID** - tunnel의 각 홉마다 다르고, router의 모든 tunnel 중에서 고유한 [4바이트 정수](/docs/specs/common-structures/#type_TunnelId)입니다. tunnel 생성자가 무작위로 선택합니다.

---

## Tunnel 구축 정보

세 가지 역할(gateway, participant, endpoint)을 수행하는 router들은 각자의 작업을 수행하기 위해 초기 [Tunnel Build Message](/docs/specs/tunnel-creation/)에서 서로 다른 데이터를 받습니다:

**tunnel 게이트웨이가 받는 것:**

- **tunnel encryption key** - 다음 홉으로 메시지와 명령을 암호화하기 위한 [AES 개인키](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - 다음 홉으로 IV를 이중 암호화하기 위한 [AES 개인키](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel 구축 요청에 대한 응답을 암호화하기 위한 [AES 공개키](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel 구축 요청에 대한 응답을 암호화하기 위한 IV
- **tunnel id** - 4바이트 정수 (인바운드 게이트웨이만 해당)
- **next hop** - 경로에서 다음 router가 무엇인지 (0홉 tunnel이고 게이트웨이가 엔드포인트이기도 한 경우 제외)
- **next tunnel id** - 다음 홉의 tunnel ID

**모든 중간 tunnel 참여자가 받는 것:**

- **tunnel encryption key** - 다음 홉으로 메시지와 지시사항을 암호화하는 데 사용하는 [AES 개인 키](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - 다음 홉으로 IV를 이중 암호화하는 데 사용하는 [AES 개인 키](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel 구축 요청에 대한 응답을 암호화하는 데 사용하는 [AES 공개 키](/docs/specs/common-structures/#type_SessionKey)
- **reply IV** - tunnel 구축 요청에 대한 응답을 암호화하는 데 사용하는 IV
- **tunnel id** - 4바이트 정수
- **next hop** - 경로에서 다음 router
- **next tunnel id** - 다음 홉의 tunnel ID

**tunnel 엔드포인트가 받는 것:**

- **tunnel encryption key** - 엔드포인트(자기 자신)에게 메시지와 지시사항을 암호화하기 위한 [AES 개인 키](/docs/specs/common-structures/#type_SessionKey)
- **tunnel IV key** - 엔드포인트(자기 자신)에게 IV를 이중 암호화하기 위한 [AES 개인 키](/docs/specs/common-structures/#type_SessionKey)
- **reply key** - tunnel 빌드 요청에 대한 응답을 암호화하기 위한 [AES 공개 키](/docs/specs/common-structures/#type_SessionKey) (아웃바운드 엔드포인트만 해당)
- **reply IV** - tunnel 빌드 요청에 대한 응답을 암호화하기 위한 IV (아웃바운드 엔드포인트만 해당)
- **tunnel id** - 4바이트 정수 (아웃바운드 엔드포인트만 해당)
- **reply router** - 응답을 전송할 tunnel의 인바운드 게이트웨이 (아웃바운드 엔드포인트만 해당)
- **reply tunnel id** - reply router의 tunnel ID (아웃바운드 엔드포인트만 해당)

자세한 내용은 [터널 생성 사양서](/docs/specs/tunnel-creation/)에서 확인할 수 있습니다.

---

## Tunnel 풀링

특정 목적을 위한 여러 tunnel은 [tunnel 사양](/docs/specs/tunnel-implementation/#tunnel.pooling)에 설명된 대로 "tunnel pool"로 그룹화될 수 있습니다. 이는 중복성과 추가 대역폭을 제공합니다. router 자체에서 사용하는 pool을 "exploratory tunnel"이라고 하고, 애플리케이션에서 사용하는 pool을 "client tunnel"이라고 합니다.

---

## 터널 길이

위에서 언급했듯이, 각 클라이언트는 자신의 router가 최소한 특정 수의 홉을 포함하는 tunnel을 제공하도록 요청합니다. 아웃바운드 및 인바운드 tunnel에 포함할 router의 수를 결정하는 것은 I2P가 제공하는 지연시간, 처리량, 신뢰성, 익명성에 중요한 영향을 미칩니다. 메시지가 거쳐야 하는 피어가 많을수록 도착하는 데 시간이 더 오래 걸리고, 해당 router 중 하나가 조기에 실패할 가능성이 높아집니다. tunnel의 router가 적을수록 공격자가 트래픽 분석 공격을 수행하여 누군가의 익명성을 뚫기가 더 쉬워집니다. tunnel 길이는 클라이언트가 [I2CP 옵션](/docs/specs/i2cp/#options)을 통해 지정합니다. tunnel의 최대 홉 수는 7개입니다.

### 0-홉 터널

tunnel에 원격 router가 없는 경우, 사용자는 매우 기본적인 그럴듯한 부인 가능성을 가집니다 (메시지를 보낸 피어가 단순히 tunnel의 일부로 전달하는 것이 아니라는 것을 아무도 확실히 알 수 없기 때문입니다). 하지만 통계 분석 공격을 시도하여 특정 목적지를 대상으로 하는 메시지가 항상 단일 게이트웨이를 통해 전송된다는 것을 알아차리는 것은 상당히 쉬울 것입니다. 아웃바운드 0-hop tunnel에 대한 통계 분석은 더 복잡하지만 유사한 정보를 보여줄 수 있습니다 (비록 실행하기가 약간 더 어려울 것이지만).

### 1-hop tunnel

tunnel에 원격 router가 하나만 있는 경우, 사용자는 내부 적대자를 상대하지 않는 한([위협 모델](/docs/overview/threat-model/)에서 설명한 대로) 그럴듯한 부인 가능성과 기본적인 익명성을 모두 확보할 수 있습니다. 하지만 적대자가 충분한 수의 router를 운영하여 tunnel의 단일 원격 router가 종종 그러한 손상된 router 중 하나가 되는 경우, 위에서 언급한 통계적 트래픽 분석 공격을 수행할 수 있게 됩니다.

### 2-hop tunnel

tunnel에 두 개 이상의 원격 router가 있는 경우, 많은 원격 router들이 공격을 수행하기 위해 손상되어야 하므로 트래픽 분석 공격을 실행하는 비용이 증가합니다.

### 3-hop (또는 그 이상) tunnel

일부 공격에 대한 취약성을 줄이기 위해 최고 수준의 보호를 위해 3개 이상의 홉(hop)을 사용하는 것이 권장됩니다. [최근 연구](https://blog.torproject.org/one-cell-enough-break-tors-anonymity/)에서는 3개를 초과하는 홉이 추가적인 보호를 제공하지 않는다고 결론짓고 있습니다.

### Tunnel 기본 길이

router는 기본적으로 탐색 tunnel에 대해 2-hop tunnel을 사용합니다. 클라이언트 tunnel 기본값은 [I2CP 옵션](/docs/specs/i2cp/#options)을 사용하여 애플리케이션에서 설정됩니다. 대부분의 애플리케이션은 기본값으로 2 또는 3 hop을 사용합니다.

---

## Tunnel 테스트

모든 tunnel은 생성자에 의해 주기적으로 테스트됩니다. 이는 outbound tunnel을 통해 DeliveryStatusMessage를 보내고 다른 inbound tunnel로 향하게 하여 두 tunnel을 동시에 테스트하는 방식입니다. 만약 연속된 테스트에서 여러 번 실패하면, 해당 tunnel은 더 이상 작동하지 않는 것으로 표시됩니다. 만약 이것이 클라이언트의 inbound tunnel에 사용되었다면, 새로운 leaseSet이 생성됩니다. Tunnel 테스트 실패는 [peer profile의 용량 등급](/docs/overview/peer-selection/#capacity)에도 반영됩니다.

---

터널 생성은 [garlic routing](/docs/overview/garlic-routing/)에 의해 처리되며, router에게 Tunnel Build Message를 보내 터널 참여를 요청합니다(위의 모든 적절한 정보와 함께 인증서를 제공하며, 현재는 'null' 인증서이지만 필요시 hashcash 또는 기타 유료가 아닌 인증서를 지원할 예정입니다). 해당 router는 메시지를 터널의 다음 홉으로 전달합니다. 자세한 내용은 [터널 생성 사양](/docs/specs/tunnel-creation/)에 있습니다.

## Tunnel 생성

---

다중 계층 암호화는 터널 메시지의 [garlic encryption](/docs/overview/garlic-routing/)에 의해 처리됩니다. 자세한 내용은 [터널 사양](/docs/specs/tunnel-implementation/)에 있습니다. 각 홉의 IV는 해당 문서에서 설명된 대로 별도의 키로 암호화됩니다.

## 터널 암호화

---

---

## 향후 작업

- 다른 터널 테스트 기법들이 사용될 수 있습니다. 예를 들어 여러 테스트를 clove로 garlic wrapping하거나, 개별 터널 참가자들을 따로 테스트하는 등의 방법이 있습니다.

- 3-hop 탐색 tunnel 기본값으로 이동.

- 향후 먼 미래 릴리스에서는 풀링, 믹싱 및 chaff 생성 설정을 지정하는 옵션이 구현될 수 있습니다.

- 먼 미래의 릴리스에서는 tunnel의 수명 동안 허용되는 메시지의 수량과 크기에 대한 제한이 구현될 수 있습니다 (예: 분당 300개 이하의 메시지 또는 1MB).

---

## 참고 자료

- [Tunnel 사양](/docs/specs/tunnel-implementation/)
- [Tunnel 생성 사양](/docs/specs/tunnel-creation/)
- [단방향 tunnel](/docs/legacy/unidirectional/)
- [Tunnel 메시지 사양](/docs/specs/tunnel-message/)
- [Garlic routing](/docs/overview/garlic-routing/)
- [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/)
- [I2CP 옵션](/docs/specs/i2cp/#options)
