---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "닫힘"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## 참고

네트워크 배포 및 테스트가 진행 중입니다. 사소한 수정이 있을 수 있습니다. 공식 사양은 [SPEC](/docs/specs/ecies/)을 참조하십시오.

다음 기능들은 0.9.46 버전 기준으로 구현되지 않았습니다:

- MessageNumbers, Options, 및 Termination 블록
- 프로토콜 계층 응답
- Zero static key
- 멀티캐스트

## 개요

이것은 I2P 시작 이래 첫 번째 새로운 end-to-end 암호화 유형에 대한 제안으로, ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/)를 대체하기 위한 것입니다.

다음과 같은 이전 작업에 의존합니다:

- 공통 구조 명세 [Common Structures](/docs/specs/common-structures/)
- LS2를 포함한 [I2NP](/docs/specs/i2np/) 명세
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) 새로운 비대칭 암호화 개요
- 저수준 암호화 개요 [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [제안서 111](/proposals/111-ntcp-2/)
- 123 새로운 netDB 항목
- 142 새로운 암호화 템플릿
- [Noise](https://noiseprotocol.org/noise.html) 프로토콜
- [Signal](https://signal.org/docs/) double ratchet 알고리즘

목표는 종단 간, destination-to-destination 통신을 위한 새로운 암호화를 지원하는 것입니다.

설계는 Signal의 이중 래칫을 통합한 Noise 핸드셰이크 및 데이터 단계를 사용할 것입니다.

이 제안서에서 Signal과 Noise에 대한 모든 언급은 배경 정보 목적으로만 제공됩니다. 이 제안서를 이해하거나 구현하는 데 Signal과 Noise 프로토콜에 대한 지식은 필요하지 않습니다.

### Current ElGamal Uses

검토를 위해, ElGamal 256바이트 공개 키는 다음 데이터 구조에서 찾을 수 있습니다. 공통 구조 사양을 참조하세요.

- Router Identity에서
  이것은 라우터의 암호화 키입니다.

- Destination에서
  destination의 공개 키는 버전 0.6에서 비활성화된 이전 i2cp-to-i2cp 암호화에 사용되었으며,
  현재는 더 이상 사용되지 않는 LeaseSet 암호화를 위한 IV를 제외하고는 사용되지 않습니다.
  대신 LeaseSet의 공개 키가 사용됩니다.

- LeaseSet에서
  이것은 목적지의 암호화 키입니다.

- LS2에서
  이것은 목적지의 암호화 키입니다.

### EncTypes in Key Certs

복습해보면, signature type 지원을 추가할 때 암호화 유형에 대한 지원도 추가했습니다. 암호화 유형 필드는 Destination과 RouterIdentity 모두에서 항상 0입니다. 이를 변경할지 여부는 미정입니다. 공통 구조 사양 [Common Structures](/docs/specs/common-structures/)를 참조하십시오.

### 현재 ElGamal 사용

복습으로, 우리는 다음을 위해 ElGamal을 사용합니다:

1) Tunnel Build 메시지 (키는 RouterIdentity에 있음)    대체는 이 제안서에서 다루지 않습니다.    제안서 152 [Proposal 152](/proposals/152-ecies-tunnels)를 참조하세요.

2) netdb 및 기타 I2NP 메시지의 router 간 암호화 (키는 RouterIdentity에 있음)    이 제안에 따라 달라짐.    1)에 대한 제안 또는 RI 옵션에 키를 넣는 것도 필요함.

3) 클라이언트 종단 간 ElGamal+AES/SessionTag (키는 LeaseSet에 있으며, Destination 키는 사용되지 않음)    대체는 이 제안서에서 다루어집니다.

4) NTCP1 및 SSU용 임시 DH    교체는 이 제안서에서 다루지 않습니다.    NTCP2에 대해서는 제안서 111을 참조하십시오.    SSU2에 대한 현재 제안서는 없습니다.

### Key Cert의 EncTypes

- 하위 호환성 제공
- LS2(제안서 123) 필요 및 기반으로 구축
- NTCP2(제안서 111)에 추가된 새로운 암호화 또는 원시 기능 활용
- 지원을 위한 새로운 암호화 또는 원시 기능 불필요
- 암호화와 서명의 분리 유지; 모든 현재 및 향후 버전 지원
- destination을 위한 새로운 암호화 활성화
- router를 위한 새로운 암호화 활성화, 단 garlic 메시지만 해당 - 터널 구축은 별도 제안서가 필요
- 32바이트 이진 destination 해시에 의존하는 기능(예: bittorrent) 손상 방지
- ephemeral-static DH를 사용한 0-RTT 메시지 전달 유지
- 이 프로토콜 계층에서 메시지 버퍼링/큐잉 요구하지 않음;
  응답 대기 없이 양방향 무제한 메시지 전달 지원 지속
- 1 RTT 후 ephemeral-ephemeral DH로 업그레이드
- 순서 이탈 메시지 처리 유지
- 256비트 보안 유지
- 전방향 보안 추가
- 인증(AEAD) 추가
- ElGamal보다 훨씬 CPU 효율적
- DH 효율성을 위해 Java jbigi에 의존하지 않음
- DH 연산 최소화
- ElGamal보다 훨씬 대역폭 효율적(514바이트 ElGamal 블록)
- 원하는 경우 동일 터널에서 신규 및 기존 암호화 지원
- 수신자가 동일 터널을 통해 들어오는 신규 및 기존 암호화를 효율적으로 구별 가능
- 타인은 신규, 기존 또는 향후 암호화를 구별할 수 없음
- 신규 대 기존 세션 길이 분류 제거(패딩 지원)
- 새로운 I2NP 메시지 불필요
- AES 페이로드의 SHA-256 체크섬을 AEAD로 교체
- 송신 및 수신 세션 바인딩 지원으로
  프로토콜 내에서 승인이 발생할 수 있도록 하며, 대역 외 방식만이 아니도록 함.
  이를 통해 응답이 즉시 전방향 보안을 가질 수 있음.
- CPU 오버헤드로 인해 현재 수행하지 않는 특정 메시지(RouterInfo 저장소)의
  종단 간 암호화 활성화.
- I2NP Garlic Message 또는
  Garlic Message Delivery Instructions 형식을 변경하지 않음.
- Garlic Clove Set 및 Clove 형식에서 사용되지 않거나 중복된 필드 제거.

다음을 포함한 세션 태그의 여러 문제점들을 해결합니다:

- 첫 번째 응답까지 AES 사용 불가
- 태그 전달이 가정될 경우 불안정성 및 정체
- 대역폭 비효율성, 특히 첫 번째 전달 시
- 태그 저장을 위한 막대한 공간 비효율성
- 태그 전달을 위한 막대한 대역폭 오버헤드
- 매우 복잡하고 구현이 어려움
- 다양한 사용 사례에 대한 튜닝이 어려움
  (스트리밍 vs. 데이터그램, 서버 vs. 클라이언트, 높은 vs. 낮은 대역폭)
- 태그 전달로 인한 메모리 고갈 취약점

### 비대칭 암호화 사용법

- LS2 형식 변경 (제안 123 완료)
- 새로운 DHT 순환 알고리즘 또는 공유 랜덤 생성
- 터널 구축을 위한 새로운 암호화.
  제안 152 [Proposal 152](/proposals/152-ecies-tunnels) 참조.
- 터널 레이어 암호화를 위한 새로운 암호화.
  제안 153 [Proposal 153](/proposals/153-chacha20-layer-encryption) 참조.
- I2NP DLM / DSM / DSRM 메시지의 암호화, 전송, 수신 방법.
  변경 없음.
- LS1-to-LS2 또는 ElGamal/AES-to-this-proposal 통신은 지원되지 않음.
  이 제안은 양방향 프로토콜임.
  목적지는 동일한 터널을 사용하여 두 개의 leaseSet을 게시하거나
  LS2에 두 가지 암호화 유형을 모두 포함시켜 하위 호환성을 처리할 수 있음.
- 위협 모델 변경
- 구현 세부사항은 여기서 논의되지 않으며 각 프로젝트에 맡김.
- (낙관적) 멀티캐스트 지원을 위한 확장 또는 훅 추가

### 목표

ElGamal/AES+SessionTag는 약 15년간 우리의 유일한 종단간 프로토콜이었으며, 본질적으로 프로토콜에 대한 수정 없이 사용되어 왔습니다. 이제 더 빠른 암호화 원시 함수들이 존재합니다. 우리는 프로토콜의 보안을 강화해야 합니다. 또한 프로토콜의 메모리 및 대역폭 오버헤드를 최소화하기 위한 휴리스틱 전략과 임시방편을 개발했지만, 이러한 전략들은 취약하고 조정하기 어려우며, 프로토콜을 더욱 손상되기 쉽게 만들어 세션이 끊어지는 원인이 됩니다.

거의 같은 기간 동안, ElGamal/AES+SessionTag 명세와 관련 문서들은 세션 태그를 전달하는 것이 얼마나 대역폭 비용이 많이 드는지 설명해왔으며, 세션 태그 전달을 "동기화된 PRNG"로 대체할 것을 제안해왔습니다. 동기화된 PRNG는 공통 시드에서 파생되어 양쪽 끝에서 동일한 태그를 결정론적으로 생성합니다. 동기화된 PRNG는 "래칫(ratchet)"이라고도 할 수 있습니다. 이 제안서는 (마침내) 해당 래칫 메커니즘을 명세하고 태그 전달을 제거합니다.

ratchet(동기화된 PRNG)을 사용하여 세션 태그를 생성함으로써, New Session 메시지와 필요시 후속 메시지에서 세션 태그를 전송하는 오버헤드를 제거합니다. 일반적인 32개 태그 세트의 경우, 이는 1KB입니다. 또한 송신 측에서 세션 태그 저장을 제거하여 저장 요구사항을 절반으로 줄입니다.

Key Compromise Impersonation (KCI) 공격을 방지하기 위해서는 Noise IK 패턴과 유사한 완전한 양방향 handshake가 필요합니다. [NOISE](https://noiseprotocol.org/noise.html)의 Noise "Payload Security Properties" 표를 참조하세요. KCI에 대한 자세한 정보는 다음 논문을 참조하세요: https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### 비목표 / 범위 외

위협 모델은 NTCP2 (제안서 111)와는 다소 다릅니다. MitM 노드들은 OBEP와 IBGW이며, floodfill들과 공모하여 현재 또는 과거의 전역 netDb에 대한 완전한 가시성을 가지고 있다고 가정됩니다.

목표는 이러한 MitM들이 트래픽을 새로운 메시지와 기존 세션 메시지로 분류하거나, 새로운 암호화 방식과 기존 암호화 방식으로 분류하는 것을 방지하는 것입니다.

## Detailed Proposal

이 제안서는 ElGamal/AES+SessionTags를 대체할 새로운 종단 간 프로토콜을 정의합니다. 이 설계는 Signal의 이중 래칫(double ratchet)을 통합한 Noise 핸드셰이크와 데이터 단계를 사용할 것입니다.

### 정당화

재설계해야 할 프로토콜의 다섯 가지 부분이 있습니다:

- 1) 새로운 세션 컨테이너 형식과 기존 세션 컨테이너 형식이
  새로운 형식으로 교체됩니다.
- 2) ElGamal (256바이트 공개 키, 128바이트 개인 키)이
  ECIES-X25519 (32바이트 공개 키 및 개인 키)로 교체됩니다
- 3) AES가
  AEAD_ChaCha20_Poly1305 (아래에서 ChaChaPoly로 축약)로 교체됩니다
- 4) SessionTags가 ratchets로 교체되는데,
  이는 본질적으로 암호화된 동기화 PRNG입니다.
- 5) ElGamal/AES+SessionTags 사양에 정의된 AES 페이로드가
  NTCP2와 유사한 블록 형식으로 교체됩니다.

다섯 가지 변경사항 각각에 대해 아래에 별도 섹션이 있습니다.

### 위협 모델

기존 I2P router 구현에서는 현재 I2P 프로토콜에서 요구되지 않는 다음 표준 암호화 기본 요소들에 대한 구현이 필요합니다:

- ECIES (하지만 이는 본질적으로 X25519입니다)
- Elligator2

[NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/))를 아직 구현하지 않은 기존 I2P router 구현체들도 다음에 대한 구현이 필요합니다:

- X25519 키 생성 및 DH
- AEAD_ChaCha20_Poly1305 (아래에서 ChaChaPoly로 줄여서 표기)
- HKDF

### Crypto Type

암호화 타입(LS2에서 사용됨)은 4입니다. 이는 리틀 엔디안 32바이트 X25519 공개 키와 여기에 명시된 end-to-end 프로토콜을 나타냅니다.

Crypto type 0은 ElGamal입니다. Crypto type 1-3은 ECIES-ECDH-AES-SessionTag를 위해 예약되어 있으며, proposal 145 [Proposal 145](/proposals/145-ecies)를 참조하세요.

### 암호화 설계 요약

이 제안서는 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)를 기반으로 한 요구사항을 제공합니다. Noise는 [SSU](/docs/legacy/ssu/) 프로토콜의 기반이 되는 Station-To-Station 프로토콜 [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol)와 유사한 특성을 가지고 있습니다. Noise 용어로는 Alice가 개시자(initiator)이고, Bob이 응답자(responder)입니다.

이 제안은 Noise protocol Noise_IK_25519_ChaChaPoly_SHA256을 기반으로 합니다. (초기 키 유도 함수의 실제 식별자는 I2P 확장을 나타내기 위해 "Noise_IKelg2_25519_ChaChaPoly_SHA256"입니다 - 아래 KDF 1 섹션 참조) 이 Noise protocol은 다음 프리미티브를 사용합니다:

- Interactive Handshake Pattern: IK
  Alice가 즉시 자신의 정적 키를 Bob에게 전송함 (I)
  Alice는 이미 Bob의 정적 키를 알고 있음 (K)

- One-Way Handshake Pattern: N
  Alice는 자신의 정적 키를 Bob에게 전송하지 않습니다 (N)

- DH Function: X25519
  [RFC-7748](https://tools.ietf.org/html/rfc7748)에서 명시된 32바이트 키 길이를 가진 X25519 DH.

- Cipher Function: ChaChaPoly
  [RFC-7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8에 명시된 AEAD_CHACHA20_POLY1305.
  12바이트 nonce, 처음 4바이트는 0으로 설정.
  [NTCP2](/docs/specs/ntcp2/)와 동일.

- Hash Function: SHA256
  I2P에서 이미 광범위하게 사용되고 있는 표준 32바이트 해시.

### I2P를 위한 새로운 암호화 기본 요소

이 제안서는 Noise_IK_25519_ChaChaPoly_SHA256에 대한 다음과 같은 개선사항을 정의합니다. 이는 일반적으로 [NOISE](https://noiseprotocol.org/noise.html) 섹션 13의 가이드라인을 따릅니다.

1) 평문 임시 키들은 [Elligator2](https://elligator.cr.yp.to/)로 인코딩됩니다.

2) 응답에는 평문 태그가 접두사로 붙습니다.

3) 페이로드 형식은 메시지 1, 2, 그리고 데이터 단계에 대해 정의됩니다. 물론 이것은 Noise에서 정의되지 않습니다.

모든 메시지에는 [I2NP](/docs/specs/i2np/) Garlic Message 헤더가 포함됩니다. 데이터 단계는 Noise 데이터 단계와 유사하지만 호환되지 않는 암호화를 사용합니다.

### 암호화 유형

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키(one-time ephemeral key)
- s = 정적 키(static key)
- p = 메시지 페이로드(message payload)

일회성 및 비제한(Unbound) 세션은 Noise N 패턴과 유사합니다.

```

<- s
  ...
  e es p ->

```
Bound 세션은 Noise IK 패턴과 유사합니다.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Noise Protocol Framework

현재 ElGamal/AES+SessionTag 프로토콜은 단방향입니다. 이 계층에서 수신자는 메시지가 어디서 왔는지 알 수 없습니다. 아웃바운드와 인바운드 세션은 연관되지 않습니다. 확인 응답은 clove의 DeliveryStatusMessage(GarlicMessage로 래핑됨)를 사용하여 대역 외에서 처리됩니다.

단방향 프로토콜에는 상당한 비효율성이 있습니다. 모든 응답도 비용이 많이 드는 'New Session' 메시지를 사용해야 합니다. 이로 인해 대역폭, CPU, 메모리 사용량이 증가합니다.

단방향 프로토콜에는 보안상의 약점도 있습니다. 모든 세션은 ephemeral-static DH를 기반으로 합니다. 리턴 경로가 없으면 Bob이 자신의 정적 키를 ephemeral 키로 "ratchet"할 방법이 없습니다. 메시지의 출처를 알 수 없으면 아웃바운드 메시지에 수신된 ephemeral 키를 사용할 방법이 없으므로, 초기 응답도 ephemeral-static DH를 사용합니다.

이 제안에서는 양방향 프로토콜을 생성하기 위한 두 가지 메커니즘인 "pairing"과 "binding"을 정의합니다. 이러한 메커니즘은 향상된 효율성과 보안을 제공합니다.

### 프레임워크 추가 사항

ElGamal/AES+SessionTags와 마찬가지로, 모든 인바운드 및 아웃바운드 세션은 특정 컨텍스트 내에 있어야 하며, 이는 router의 컨텍스트이거나 특정 로컬 목적지의 컨텍스트입니다. Java I2P에서 이 컨텍스트를 Session Key Manager라고 합니다.

세션은 컨텍스트 간에 공유되어서는 안 됩니다. 그렇게 되면 다양한 로컬 destination들 간의 상관관계나 로컬 destination과 router 간의 상관관계를 허용하게 되기 때문입니다.

주어진 destination이 ElGamal/AES+SessionTags와 이 제안서를 모두 지원하는 경우, 두 유형의 세션이 컨텍스트를 공유할 수 있습니다. 아래 섹션 1c)를 참조하십시오.

### 핸드셰이크 패턴

발신자(Alice)에서 아웃바운드 세션이 생성될 때, 응답이 예상되지 않는 경우(예: raw 데이터그램)를 제외하고는 새로운 인바운드 세션이 생성되어 아웃바운드 세션과 쌍을 이룹니다.

새로운 인바운드 세션은 응답이 요청되지 않는 경우(예: 원시 데이터그램)가 아닌 이상 항상 새로운 아웃바운드 세션과 쌍을 이룹니다.

응답이 요청되고 원격 목적지나 router에 바인딩된 경우, 해당 새로운 아웃바운드 세션이 그 목적지나 router에 바인딩되며, 해당 목적지나 router에 대한 이전 아웃바운드 세션을 대체합니다.

인바운드 및 아웃바운드 세션을 페어링하면 DH 키를 래칫할 수 있는 기능을 갖춘 양방향 프로토콜이 제공됩니다.

### 세션

주어진 목적지나 router에 대해서는 단 하나의 아웃바운드 세션만 존재합니다. 주어진 목적지나 router로부터는 여러 개의 현재 인바운드 세션이 있을 수 있습니다. 일반적으로 새로운 인바운드 세션이 생성되고 해당 세션에서 트래픽이 수신되면(이는 ACK 역할을 함), 다른 세션들은 1분 정도 내에 비교적 빠르게 만료되도록 표시됩니다. 이전에 전송된 메시지(PN) 값이 확인되며, 이전 인바운드 세션에서 수신되지 않은 메시지가 (윈도우 크기 내에서) 없다면, 이전 세션은 즉시 삭제될 수 있습니다.

발신자(Alice)에서 아웃바운드 세션이 생성되면, 이는 원격 Destination(Bob)에 바인딩되며, 페어링된 인바운드 세션 역시 원격 Destination에 바인딩됩니다. 세션이 ratchet되면서 원격 Destination에 계속 바인딩된 상태를 유지합니다.

수신자(Bob)에서 인바운드 세션이 생성될 때, Alice의 선택에 따라 원격 Destination(Alice)에 바인딩될 수 있습니다. Alice가 New Session 메시지에 바인딩 정보(그녀의 정적 키)를 포함하면, 세션은 해당 destination에 바인딩되고, 아웃바운드 세션이 생성되어 동일한 Destination에 바인딩됩니다. 세션들이 래칫팅되면서, 원격 Destination에 계속 바인딩된 상태를 유지합니다.

### 세션 컨텍스트

일반적인 스트리밍 사례의 경우, Alice와 Bob이 다음과 같이 프로토콜을 사용할 것으로 예상됩니다:

- Alice는 새로운 아웃바운드 세션을 새로운 인바운드 세션과 페어링하며, 둘 다 원격 목적지(Bob)에 바인딩됩니다.
- Alice는 바인딩 정보와 서명, 그리고 응답 요청을 Bob에게 보내는 New Session 메시지에 포함합니다.
- Bob은 새로운 인바운드 세션을 새로운 아웃바운드 세션과 페어링하며, 둘 다 원격 목적지(Alice)에 바인딩됩니다.
- Bob은 페어링된 세션에서 새로운 DH 키로의 래칫과 함께 Alice에게 응답(ack)을 보냅니다.
- Alice는 Bob의 새로운 키로 새로운 아웃바운드 세션으로 래칫하며, 기존 인바운드 세션과 페어링됩니다.

인바운드 세션을 원격 Destination에 바인딩하고, 인바운드 세션을 동일한 Destination에 바인딩된 아웃바운드 세션과 페어링함으로써 두 가지 주요 이점을 얻을 수 있습니다:

1) Bob이 Alice에게 보내는 초기 응답은 ephemeral-ephemeral DH를 사용합니다

2) Alice가 Bob의 응답을 받고 ratchet한 후, Alice에서 Bob으로의 모든 후속 메시지는 ephemeral-ephemeral DH를 사용합니다.

### 인바운드 및 아웃바운드 세션 페어링

ElGamal/AES+SessionTags에서 LeaseSet이 garlic clove로 묶이거나 태그가 전달될 때, 송신 router는 ACK를 요청합니다. 이는 DeliveryStatus 메시지를 포함하는 별도의 garlic clove입니다. 추가 보안을 위해 DeliveryStatus 메시지는 Garlic 메시지로 래핑됩니다. 이 메커니즘은 프로토콜 관점에서 대역 외(out-of-band) 방식입니다.

새로운 프로토콜에서는 인바운드와 아웃바운드 세션이 쌍을 이루므로, 대역 내에서 ACK를 가질 수 있습니다. 별도의 clove가 필요하지 않습니다.

명시적 ACK는 단순히 I2NP 블록이 없는 Existing Session 메시지입니다. 그러나 대부분의 경우 역방향 트래픽이 있기 때문에 명시적 ACK를 피할 수 있습니다. 구현체에서는 스트리밍이나 애플리케이션 계층이 응답할 시간을 주기 위해 명시적 ACK를 보내기 전에 짧은 시간(아마 100ms 정도)을 기다리는 것이 바람직할 수 있습니다.

구현체들은 I2NP 블록이 처리된 후까지 ACK 전송을 지연해야 합니다. Garlic Message에 lease set이 포함된 Database Store Message가 들어있을 수 있기 때문입니다. ACK를 라우팅하려면 최신 lease set이 필요하고, 바인딩 정적 키를 검증하려면 원단 목적지(lease set에 포함됨)가 필요합니다.

### 세션 및 목적지 바인딩

아웃바운드 세션은 항상 인바운드 세션보다 먼저 만료되어야 합니다. 아웃바운드 세션이 만료되고 새로운 세션이 생성되면, 새로운 쌍을 이루는 인바운드 세션도 함께 생성됩니다. 기존 인바운드 세션이 있었다면, 해당 세션은 만료되도록 허용됩니다.

### 바인딩과 페어링의 이점

미정

### 메시지 ACK

우리는 사용되는 암호화 구성 요소에 해당하는 다음 함수들을 정의합니다.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### 세션 타임아웃

### 멀티캐스트

[I2NP](/docs/specs/i2np/)에 명세된 Garlic Message는 다음과 같습니다. 중간 홉들이 새로운 암호화와 기존 암호화를 구별할 수 없도록 하는 것이 설계 목표이므로, 길이 필드가 중복되더라도 이 형식은 변경될 수 없습니다. 이 형식은 전체 16바이트 헤더로 표시되지만, 사용되는 전송 방식에 따라 실제 헤더는 다른 형식일 수 있습니다.

복호화되면 데이터에는 일련의 Garlic Clove들과 추가 데이터가 포함되며, 이는 Clove Set이라고도 알려져 있습니다.

자세한 내용과 전체 사양은 [I2NP](/docs/specs/i2np/)를 참조하세요.

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### 정의

15년 넘게 사용된 현재 메시지 형식은 ElGamal/AES+SessionTags입니다. ElGamal/AES+SessionTags에서는 두 가지 메시지 형식이 있습니다:

1) 새 세션: - 514바이트 ElGamal 블록 - AES 블록 (최소 128바이트, 16의 배수)

2) 기존 세션: - 32바이트 Session Tag - AES 블록 (최소 128바이트, 16의 배수)

128로의 최소 패딩은 Java I2P에서 구현된 대로이지만 수신 시에는 강제되지 않습니다.

이러한 메시지들은 길이 필드를 포함하는 I2NP garlic 메시지에 캡슐화되므로, 길이를 알 수 있습니다.

16으로 나누어떨어지지 않는 길이에 대한 패딩이 정의되어 있지 않으므로, New Session은 항상 (mod 16 == 2)이고, Existing Session은 항상 (mod 16 == 0)입니다. 이를 수정해야 합니다.

수신자는 먼저 처음 32바이트를 Session Tag로 조회를 시도합니다. 발견되면 AES 블록을 복호화합니다. 발견되지 않고 데이터가 최소 (514+16) 길이인 경우, ElGamal 블록 복호화를 시도하고, 성공하면 AES 블록을 복호화합니다.

### 1) 메시지 형식

Signal Double Ratchet에서 헤더는 다음을 포함합니다:

- DH: 현재 래칫 공개 키
- PN: 이전 체인 메시지 길이
- N: 메시지 번호

Signal의 "sending chains"는 우리의 tag sets와 대략 동등합니다. session tag를 사용함으로써 대부분을 제거할 수 있습니다.

New Session에서는 암호화되지 않은 헤더에 공개 키만 넣습니다.

기존 세션에서는 헤더에 세션 태그를 사용합니다. 세션 태그는 현재 ratchet 공개 키와 메시지 번호에 연결됩니다.

신규 세션과 기존 세션 모두에서 PN과 N은 암호화된 본문에 있습니다.

Signal에서는 지속적으로 래칭이 발생합니다. 새로운 DH 공개 키는 수신자가 래칭하고 새로운 공개 키를 다시 전송하도록 요구하며, 이는 또한 수신된 공개 키에 대한 승인 역할도 합니다. 이는 우리에게는 너무 많은 DH 연산이 될 것입니다. 따라서 우리는 수신된 키의 승인과 새로운 공개 키의 전송을 분리합니다. 새로운 DH 공개 키에서 생성된 세션 태그를 사용하는 모든 메시지는 ACK를 구성합니다. 우리는 키를 다시 설정하고자 할 때만 새로운 공개 키를 전송합니다.

DH가 ratchet해야 하는 최대 메시지 수는 65535개입니다.

세션 키를 전달할 때, 세션 태그도 함께 전달해야 하는 대신 세션 키로부터 "Tag Set"을 도출합니다. Tag Set은 최대 65536개의 태그를 가질 수 있습니다. 하지만 수신자는 모든 가능한 태그를 한 번에 생성하는 대신 "미리보기(look-ahead)" 전략을 구현해야 합니다. 마지막으로 수신된 유효한 태그 이후 최대 N개의 태그만 생성합니다. N은 최대 128개일 수 있지만, 32개 또는 그보다 적은 수가 더 나은 선택일 수 있습니다.

### 현재 메시지 형식 검토

새 세션 일회용 공개 키 (32바이트) 암호화된 데이터 및 MAC (나머지 바이트)

New Session 메시지는 송신자의 정적 공개 키를 포함할 수도 있고 포함하지 않을 수도 있습니다. 포함된 경우, 역방향 세션이 해당 키에 바인딩됩니다. 응답이 예상되는 경우, 즉 스트리밍 및 응답 가능한 데이터그램의 경우 정적 키가 포함되어야 합니다. 원시 데이터그램의 경우에는 포함되지 않아야 합니다.

New Session 메시지는 단방향 Noise [NOISE](https://noiseprotocol.org/noise.html) 패턴 "N"(정적 키가 전송되지 않는 경우) 또는 양방향 패턴 "IK"(정적 키가 전송되는 경우)와 유사합니다.

### 암호화된 데이터 형식 검토

길이는 96 + 페이로드 길이입니다. 암호화된 형식:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 새로운 세션 태그와 Signal과의 비교

임시 키(ephemeral key)는 32바이트이며, Elligator2로 인코딩됩니다. 이 키는 절대 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

### 1a) 새로운 세션 형식

복호화되었을 때, Alice의 X25519 정적 키, 32바이트.

### 1b) 새로운 세션 형식 (바인딩 포함)

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 적습니다. 페이로드는 DateTime 블록을 포함해야 하며 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식 및 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 새로운 세션 임시 키

응답이 필요하지 않은 경우, static key는 전송되지 않습니다.

길이는 96 + 페이로드 길이입니다. 암호화된 형식:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 정적 키

Alice의 ephemeral key. ephemeral key는 32바이트이며, Elligator2로 인코딩되고 little endian 방식입니다. 이 키는 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

### 페이로드

Flags 섹션은 아무것도 포함하지 않습니다. 바인딩이 있는 New Session 메시지의 static key와 동일한 길이여야 하므로 항상 32바이트입니다. Bob은 32바이트가 모두 0인지 테스트하여 그것이 static key인지 flags 섹션인지 판단합니다.

TODO 여기에 필요한 플래그가 있나요?

### 1c) 새로운 세션 형식 (바인딩 없음)

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16바이트 적습니다. 페이로드는 DateTime 블록을 포함해야 하며 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식 및 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 새 세션 임시 키

단일 메시지만 전송될 것으로 예상되는 경우, 세션 설정이나 정적 키가 필요하지 않습니다.

길이는 96 + 페이로드 길이입니다. 암호화된 형식:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Flags Section 복호화된 데이터

일회용 키는 32바이트이며, Elligator2로 인코딩되고 리틀 엔디안 방식을 사용합니다. 이 키는 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

### 페이로드

Flags 섹션은 아무것도 포함하지 않습니다. 바인딩을 사용하는 New Session 메시지의 static key와 동일한 길이여야 하므로 항상 32바이트입니다. Bob은 32바이트가 모두 0인지 테스트하여 static key인지 flags 섹션인지 판단합니다.

TODO 여기에 필요한 플래그가 있나요?

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) 일회성 형식 (바인딩이나 세션 없음)

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 작습니다. 페이로드는 DateTime 블록을 포함해야 하며 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식과 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 새 세션 일회용 키

### Flags Section 복호화된 데이터

이것은 수정된 프로토콜 이름을 가진 IK용 표준 [NOISE](https://noiseprotocol.org/noise.html)입니다. IK 패턴(바인드된 세션)과 N 패턴(언바인드된 세션) 모두에 동일한 초기화자를 사용한다는 점에 주목하세요.

프로토콜 이름이 수정된 이유는 두 가지입니다. 첫째, 임시 키들이 Elligator2로 인코딩되었음을 나타내기 위함이고, 둘째, 태그 값을 혼합하기 위해 두 번째 메시지 이전에 MixHash()가 호출됨을 나타내기 위함입니다.

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### 페이로드

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) 새 세션 메시지용 KDF들

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### 초기 ChainKey를 위한 KDF

이는 Noise "N" 패턴이지만, 바운드 세션과 동일한 "IK" 초기화자를 사용한다는 점에 주목하세요.

새로운 세션 메시지는 정적 키가 복호화되고 모든 값이 0인지 확인하기 위해 검사되기 전까지는 Alice의 정적 키를 포함하고 있는지 여부를 식별할 수 없습니다. 따라서 수신자는 모든 새로운 세션 메시지에 대해 "IK" 상태 머신을 사용해야 합니다. 정적 키가 모두 0인 경우 "ss" 메시지 패턴을 건너뛰어야 합니다.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### 플래그/정적 키 섹션 암호화된 내용을 위한 KDF

단일 New Session 메시지에 대한 응답으로 하나 이상의 New Session Reply가 전송될 수 있습니다. 각 reply는 해당 세션의 TagSet에서 생성된 태그로 시작됩니다.

New Session Reply는 두 부분으로 구성됩니다. 첫 번째 부분은 앞에 태그가 붙은 Noise IK handshake의 완성입니다. 첫 번째 부분의 길이는 56바이트입니다. 두 번째 부분은 데이터 단계 페이로드입니다. 두 번째 부분의 길이는 16 + 페이로드 길이입니다.

전체 길이는 72 + 페이로드 길이입니다. 암호화된 형식:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 페이로드 섹션을 위한 KDF (Alice 정적 키 포함)

태그는 아래의 DH 초기화 KDF에서 초기화된 Session Tags KDF에서 생성됩니다. 이는 응답을 세션과 연관시킵니다. DH 초기화의 Session Key는 사용되지 않습니다.

### 페이로드 섹션을 위한 KDF (Alice 정적 키 제외)

Bob의 ephemeral key. ephemeral key는 32바이트이며, Elligator2로 인코딩되고 little endian 형식입니다. 이 키는 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

### 1g) 새 세션 응답 형식

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 적습니다. 페이로드는 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식 및 추가 요구사항은 아래 페이로드 섹션을 참조하십시오.

### 세션 태그

하나 이상의 태그가 TagSet에서 생성되며, 이는 New Session 메시지의 chainKey를 사용하여 아래 KDF로 초기화됩니다.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### 새 세션 응답 임시 키

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### 페이로드

이는 분할 후 첫 번째 기존 세션 메시지와 같지만 별도의 태그가 없습니다. 또한 위의 해시를 사용하여 페이로드를 NSR 메시지에 바인딩합니다.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### Reply TagSet을 위한 KDF

응답의 크기에 따라 각각 고유한 임시 키를 가진 여러 NSR 메시지가 응답으로 전송될 수 있습니다.

Alice와 Bob은 모든 NS 및 NSR 메시지에 대해 새로운 임시 키를 사용해야 합니다.

Alice는 Existing Session (ES) 메시지를 보내기 전에 Bob의 NSR 메시지 중 하나를 받아야 하며, Bob은 ES 메시지를 보내기 전에 Alice로부터 ES 메시지를 받아야 합니다.

Bob의 NSR Payload Section에서 가져온 ``chainKey``와 ``k``는 초기 ES DH Ratchets(양방향, DH Ratchet KDF 참조)의 입력값으로 사용됩니다.

Bob은 Alice로부터 수신한 ES 메시지에 대해서만 기존 세션(Existing Sessions)을 유지해야 합니다. 다른 생성된 인바운드 및 아웃바운드 세션들(여러 NSR용)은 주어진 세션에 대해 Alice의 첫 번째 ES 메시지를 수신한 후 즉시 파기되어야 합니다.

### Reply Key Section 암호화된 내용을 위한 KDF

세션 태그 (8바이트) 암호화된 데이터 및 MAC (아래 섹션 3 참조)

### 페이로드 섹션 암호화된 콘텐츠를 위한 KDF

암호화됨:

```

+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 bytes, cleartext

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 참고사항

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16만큼 적습니다. 형식과 요구사항은 아래 payload 섹션을 참조하세요.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) 기존 세션 형식

형식: 32바이트 공개 키와 개인 키, little-endian.

정당화: [NTCP2](/docs/specs/ntcp2/)에서 사용됩니다.

### 형식

표준 Noise handshake에서 각 방향의 초기 handshake 메시지는 평문으로 전송되는 ephemeral key로 시작합니다. 유효한 X25519 키는 무작위 데이터와 구별 가능하므로, 중간자가 이러한 메시지를 무작위 세션 태그로 시작하는 Existing Session 메시지와 구별할 수 있습니다. [NTCP2](/docs/specs/ntcp2/) ([Proposal 111](/proposals/111-ntcp-2/))에서는 out-of-band 정적 키를 사용하는 저오버헤드 XOR 함수를 사용하여 키를 난독화했습니다. 그러나 여기서의 위협 모델은 다릅니다. 우리는 어떤 중간자도 어떤 수단을 사용하여 트래픽의 목적지를 확인하거나 초기 handshake 메시지를 Existing Session 메시지와 구별할 수 있도록 허용하지 않으려고 합니다.

따라서 [Elligator2](https://elligator.cr.yp.to/)를 사용하여 New Session 및 New Session Reply 메시지의 임시 키를 변환하여 균등 랜덤 문자열과 구별할 수 없도록 합니다.

### 페이로드

32바이트 공개키 및 개인키. 인코딩된 키는 리틀 엔디안입니다.

[Elligator2](https://elligator.cr.yp.to/)에서 정의된 바와 같이, 인코딩된 키들은 254개의 무작위 비트와 구별할 수 없습니다. 우리는 256개의 무작위 비트(32바이트)가 필요합니다. 따라서 인코딩과 디코딩은 다음과 같이 정의됩니다:

인코딩:

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
디코딩:

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

OBEP와 IBGW가 트래픽을 분류하는 것을 방지하는 데 필요합니다.

### 2a) Elligator2

Elligator2는 평균 키 생성 시간을 두 배로 늘립니다. 개인 키의 절반이 Elligator2로 인코딩하기에 부적합한 공개 키를 생성하기 때문입니다. 또한, 생성기가 적합한 키 쌍을 찾을 때까지 계속 재시도해야 하므로 키 생성 시간은 지수 분포를 가진 무제한적입니다.

이 오버헤드는 적합한 키들의 풀을 유지하기 위해 별도의 스레드에서 미리 키 생성을 수행하여 관리할 수 있습니다.

generator는 적합성을 판단하기 위해 ENCODE_ELG2() 함수를 수행합니다. 따라서 generator는 다시 계산할 필요가 없도록 ENCODE_ELG2()의 결과를 저장해야 합니다.

또한, 부적합한 키들은 Elligator2가 사용되지 않는 [NTCP2](/docs/specs/ntcp2/)에 사용되는 키 풀에 추가될 수 있습니다. 이렇게 하는 것의 보안 문제는 TBD입니다.

### 형식

[NTCP2](/docs/specs/ntcp2/)에서와 동일한 ChaCha20과 Poly1305를 사용하는 AEAD입니다. 이는 TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)에서도 유사하게 사용되는 [RFC-7539](https://tools.ietf.org/html/rfc7539)에 해당합니다.

### 정당화

New Session 메시지의 AEAD 블록에 대한 암호화/복호화 함수의 입력:

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### 참고사항

Existing Session 메시지에서 AEAD 블록의 암호화/복호화 함수에 대한 입력값:

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

암호화 함수의 출력, 복호화 함수의 입력:

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### 새 세션 및 새 세션 응답 입력

- ChaCha20은 스트림 암호이므로 평문을 패딩할 필요가 없습니다.
  추가 키스트림 바이트는 폐기됩니다.

- 암호의 키(256비트)는 SHA256 KDF를 통해 합의됩니다.
  각 메시지에 대한 KDF의 세부사항은 아래 별도 섹션에 있습니다.

- ChaChaPoly 프레임은 I2NP 데이터 메시지에 캡슐화되어 있기 때문에 크기가 알려져 있습니다.

- 모든 메시지에 대해,
  패딩은 인증된
  데이터 프레임 내부에 있습니다.

### 기존 세션 입력

AEAD 검증에 실패한 모든 수신 데이터는 폐기되어야 합니다. 응답은 반환되지 않습니다.

### 암호화된 형식

[NTCP2](/docs/specs/ntcp2/)에서 사용됩니다.

### 참고사항

이전과 같이 session tag를 여전히 사용하지만, ratchet을 사용하여 생성합니다. Session tag에는 구현하지 않은 rekey 옵션도 있었습니다. 따라서 이중 ratchet과 같지만 두 번째 것은 구현하지 않았습니다.

여기서는 Signal의 Double Ratchet과 유사한 것을 정의합니다. 세션 태그는 수신자와 송신자 측에서 결정론적이고 동일하게 생성됩니다.

대칭 키/태그 래칫(ratchet)을 사용함으로써 송신자 측에서 세션 태그를 저장하기 위한 메모리 사용량을 제거합니다. 또한 태그 세트를 전송하는 대역폭 소비도 제거합니다. 수신자 측 사용량은 여전히 상당하지만, 세션 태그를 32바이트에서 8바이트로 줄여 더욱 감소시킬 수 있습니다.

Signal에서 지정된(그리고 선택적인) 헤더 암호화는 사용하지 않으며, 대신 세션 태그를 사용합니다.

DH ratchet을 사용함으로써 우리는 ElGamal/AES+SessionTags에서는 구현되지 않았던 전방향 보안성(forward secrecy)을 달성합니다.

참고: New Session 일회용 공개 키는 ratchet의 일부가 아니며, 유일한 기능은 Alice의 초기 DH ratchet 키를 암호화하는 것입니다.

### AEAD 오류 처리

Double Ratchet은 각 메시지 헤더에 태그를 포함시켜 손실되거나 순서가 바뀐 메시지를 처리합니다. 수신자는 태그의 인덱스를 조회하며, 이것이 메시지 번호 N입니다. 메시지에 PN 값을 가진 Message Number 블록이 포함되어 있다면, 수신자는 이전 태그 세트에서 해당 값보다 높은 모든 태그를 삭제할 수 있으며, 건너뛴 메시지가 나중에 도착할 경우를 대비해 이전 태그 세트에서 건너뛴 태그들은 보관합니다.

### 정당성

이러한 래칫을 구현하기 위해 다음과 같은 데이터 구조와 함수를 정의합니다.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

태그셋

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchet하지만 Signal만큼 빠르지는 않습니다. 우리는 수신된 키의 ack를 새 키 생성과 분리합니다. 일반적인 사용에서 Alice와 Bob은 각각 New Session에서 즉시 ratchet(두 번)하지만, 다시는 ratchet하지 않습니다.

참고로 ratchet은 단일 방향용이며, 해당 방향에 대한 새로운 세션 태그 / 메시지 키 ratchet 체인을 생성합니다. 양방향에 대한 키를 생성하려면 두 번 ratchet해야 합니다.

새로운 키를 생성하고 전송할 때마다 ratchet합니다. 새로운 키를 받을 때마다 ratchet합니다.

Alice는 바인딩되지 않은 아웃바운드 세션을 생성할 때 한 번 래칫하며, 인바운드 세션은 생성하지 않습니다(바인딩되지 않은 것은 응답 불가능합니다).

Bob은 바운드되지 않은 인바운드 세션을 생성할 때 한 번 ratchet하며, 해당하는 아웃바운드 세션을 생성하지 않습니다(바운드되지 않은 세션은 응답할 수 없습니다).

Alice는 Bob의 New Session Reply (NSR) 메시지 중 하나를 받을 때까지 Bob에게 New Session (NS) 메시지를 계속 보냅니다. 그런 다음 NSR의 Payload Section KDF 결과를 세션 ratchet의 입력으로 사용하고(DH Ratchet KDF 참조), Existing Session (ES) 메시지를 보내기 시작합니다.

수신된 각 NS 메시지에 대해 Bob은 새로운 인바운드 세션을 생성하며, 응답 Payload Section의 KDF 결과를 새로운 인바운드 및 아웃바운드 ES DH Ratchet의 입력으로 사용합니다.

각 응답이 필요할 때마다, Bob은 페이로드에 응답을 담은 NSR 메시지를 Alice에게 전송합니다. Bob은 모든 NSR에 대해 새로운 임시 키를 사용해야 합니다.

Bob은 해당 아웃바운드 세션에서 ES 메시지를 생성하고 전송하기 전에 인바운드 세션 중 하나에서 Alice로부터 ES 메시지를 받아야 합니다.

Alice는 Bob으로부터 NSR 메시지를 수신하기 위해 타이머를 사용해야 합니다. 타이머가 만료되면 세션을 제거해야 합니다.

KCI 및/또는 리소스 고갈 공격을 피하기 위해, 공격자가 Alice가 NS 메시지를 계속 보내도록 하기 위해 Bob의 NSR 응답을 드롭하는 경우, Alice는 타이머 만료로 인한 일정 횟수의 재시도 후에는 Bob에게 New Session을 시작하는 것을 피해야 합니다.

Alice와 Bob은 각각 수신된 모든 NextKey 블록에 대해 DH ratchet을 수행합니다.

Alice와 Bob은 각 DH ratchet 후에 새로운 태그 세트와 두 개의 대칭 키 ratchet을 생성합니다. 주어진 방향에서 각각의 새로운 ES 메시지에 대해 Alice와 Bob은 세션 태그와 대칭 키 ratchet을 진행시킵니다.

초기 핸드셰이크 이후 DH ratchet의 빈도는 구현에 따라 달라집니다. 프로토콜에서는 ratchet이 필요하기 전까지 최대 65535개의 메시지 제한을 두고 있지만, 더 빈번한 ratcheting(메시지 수, 경과 시간 또는 둘 다 기준)은 추가적인 보안을 제공할 수 있습니다.

바운드 세션에서 최종 handshake KDF 이후, Bob과 Alice는 결과로 나온 CipherState에서 Noise Split() 함수를 실행하여 인바운드 및 아웃바운드 세션에 대한 독립적인 대칭 및 태그 체인 키를 생성해야 합니다.

#### KEY AND TAG SET IDS

키와 태그 세트 ID 번호는 키와 태그 세트를 식별하는 데 사용됩니다. 키 ID는 NextKey 블록에서 전송되거나 사용된 키를 식별하는 데 사용됩니다. 태그 세트 ID는 ACK 블록에서 (메시지 번호와 함께) 확인응답되는 메시지를 식별하는 데 사용됩니다. 키와 태그 세트 ID 모두 단일 방향의 태그 세트에 적용됩니다. 키와 태그 세트 ID 번호는 순차적이어야 합니다.

각 방향의 세션에서 사용되는 첫 번째 태그 세트에서는 태그 세트 ID가 0입니다. NextKey 블록이 전송되지 않았으므로 키 ID가 없습니다.

DH ratchet을 시작하려면, 송신자는 키 ID가 0인 새로운 NextKey 블록을 전송합니다. 수신자는 키 ID가 0인 새로운 NextKey 블록으로 응답합니다. 그러면 송신자는 태그 세트 ID가 1인 새로운 태그 세트를 사용하기 시작합니다.

후속 태그 세트는 유사하게 생성됩니다. NextKey 교환 후에 사용되는 모든 태그 세트의 경우, 태그 세트 번호는 (1 + Alice의 키 ID + Bob의 키 ID)입니다.

키와 태그 세트 ID는 0부터 시작하여 순차적으로 증가합니다. 최대 태그 세트 ID는 65535입니다. 최대 키 ID는 32767입니다. 태그 세트가 거의 소진되면, 태그 세트 발신자는 NextKey 교환을 시작해야 합니다. 태그 세트 65535가 거의 소진되면, 태그 세트 발신자는 New Session 메시지를 전송하여 새로운 세션을 시작해야 합니다.

스트리밍 최대 메시지 크기가 1730이고 재전송이 없다고 가정할 때, 단일 태그 세트를 사용한 이론적 최대 데이터 전송량은 1730 * 65536 ~= 108 MB입니다. 실제 최대값은 재전송으로 인해 더 낮아질 것입니다.

사용 가능한 모든 65536개의 태그 세트를 사용한 이론적 최대 데이터 전송량은 세션을 폐기하고 교체해야 하기 전까지 64K * 108 MB ~= 6.9 TB입니다.

#### DH RATCHET MESSAGE FLOW

태그 집합에 대한 다음 키 교환은 해당 태그들의 발신자(아웃바운드 태그 집합의 소유자)가 시작해야 합니다. 수신자(인바운드 태그 집합의 소유자)가 응답합니다. 애플리케이션 계층에서의 일반적인 HTTP GET 트래픽의 경우, Bob이 더 많은 메시지를 보내고 키 교환을 시작하여 먼저 래칫팅을 수행할 것입니다. 아래 다이어그램이 이를 보여줍니다. Alice가 래칫팅할 때는 동일한 과정이 역순으로 발생합니다.

NS/NSR 핸드셰이크 후에 사용되는 첫 번째 태그 세트는 태그 세트 0입니다. 태그 세트 0이 거의 소진되면, 태그 세트 1을 생성하기 위해 양방향으로 새로운 키를 교환해야 합니다. 그 후에는 새로운 키가 한 방향으로만 전송됩니다.

태그 세트 2를 생성하기 위해, 태그 발송자는 새 키를 보내고 태그 수신자는 확인응답으로 자신의 이전 키의 ID를 보냅니다. 양측 모두 DH를 수행합니다.

태그 세트 3을 생성하기 위해, 태그 발신자는 자신의 이전 키의 ID를 전송하고 태그 수신자에게 새로운 키를 요청합니다. 양쪽 모두 DH를 수행합니다.

후속 태그 세트는 태그 세트 2와 3처럼 생성됩니다. 태그 세트 번호는 (1 + 송신자 키 ID + 수신자 키 ID)입니다.

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
아웃바운드 tagset에 대한 DH ratchet이 완료되고 새로운 아웃바운드 tagset이 생성된 후에는 즉시 사용되어야 하며, 기존 아웃바운드 tagset은 삭제할 수 있습니다.

인바운드 tagset에 대한 DH ratchet이 완료되고 새로운 인바운드 tagset이 생성된 후, 수신자는 두 tagset 모두에서 태그를 수신하고, 약 3분 정도의 짧은 시간 후에 기존 tagset을 삭제해야 합니다.

태그 세트와 키 ID 진행의 요약은 아래 표에 있습니다. *는 새로운 키가 생성됨을 나타냅니다.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
키와 태그 집합 ID 번호는 순차적이어야 합니다.

#### DH INITIALIZATION KDF

이것은 단일 방향에 대한 DH_INITIALIZE(rootKey, k)의 정의입니다. 이는 tagset과 필요시 후속 DH ratchet에 사용될 "next root key"를 생성합니다.

DH 초기화를 세 곳에서 사용합니다. 첫째, New Session Replies용 태그 세트를 생성하는 데 사용합니다. 둘째, Existing Session 메시지에서 사용할 각 방향별로 하나씩 두 개의 태그 세트를 생성하는 데 사용합니다. 마지막으로, DH Ratchet 이후에 추가 Existing Session 메시지를 위해 단일 방향으로 새로운 태그 세트를 생성하는 데 사용합니다.

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

이는 tagset이 소진되기 전에 NextKey 블록에서 새로운 DH 키가 교환된 후 사용됩니다.

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### 메시지 번호

Signal에서처럼 모든 메시지에 대한 래칫(ratchet). 세션 태그 래칫은 대칭 키 래칫과 동기화되지만, 수신자 키 래칫은 메모리 절약을 위해 "지연"될 수 있습니다.

송신자는 전송되는 각 메시지에 대해 한 번씩 ratchet합니다. 추가 태그를 저장할 필요는 없습니다. 송신자는 또한 현재 체인에서 메시지의 메시지 번호인 'N'에 대한 카운터를 유지해야 합니다. 'N' 값은 전송되는 메시지에 포함됩니다. Message Number 블록 정의를 참조하세요.

수신자는 최대 윈도우 크기만큼 ratchet를 앞당기고 세션과 연결된 "tag set"에 태그를 저장해야 합니다. 수신되면 저장된 태그는 폐기될 수 있으며, 이전에 수신되지 않은 태그가 없다면 윈도우를 진행시킬 수 있습니다. 수신자는 각 세션 태그와 연결된 'N' 값을 유지하고, 전송된 메시지의 번호가 이 값과 일치하는지 확인해야 합니다. Message Number 블록 정의를 참조하십시오.

#### KDF

이것은 RATCHET_TAG()의 정의입니다.

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### 샘플 구현

Signal에서와 같이 모든 메시지에 대한 래칫. 각 대칭 키는 연관된 메시지 번호와 세션 태그를 가집니다. 세션 키 래칫은 대칭 태그 래칫과 동기화되지만, 수신자 키 래칫은 메모리 절약을 위해 "뒤처질" 수 있습니다.

전송기는 전송되는 각 메시지마다 한 번씩 ratchet됩니다. 추가 키를 저장할 필요가 없습니다.

수신자가 session tag를 받으면, 아직 연관된 키까지 대칭 키 ratchet을 앞으로 돌리지 않았다면, 연관된 키까지 "따라잡아야" 합니다. 수신자는 아직 받지 않은 이전 tag들에 대한 키들을 캐시할 것입니다. 일단 받으면, 저장된 키는 폐기될 수 있으며, 이전에 받지 않은 tag가 없다면 윈도우를 앞으로 이동시킬 수 있습니다.

효율성을 위해 session tag과 대칭 키 ratchet은 분리되어 있어 session tag ratchet이 대칭 키 ratchet보다 앞서 실행될 수 있습니다. 이는 또한 session tag들이 네트워크를 통해 전송되기 때문에 추가적인 보안을 제공합니다.

#### KDF

이것은 RATCHET_KEY()의 정의입니다.

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) DH Ratchet

이것은 ElGamal/AES+SessionTags 명세서에 정의된 AES 섹션 형식을 대체합니다.

이는 [NTCP2](/docs/specs/ntcp2/) 명세에서 정의된 것과 동일한 블록 형식을 사용합니다. 개별 블록 타입은 다르게 정의됩니다.

구현자들이 코드를 공유하도록 권장하는 것이 파싱 문제로 이어질 수 있다는 우려가 있습니다. 구현자들은 코드 공유의 장점과 위험을 신중하게 고려하고, 두 컨텍스트에서 순서 및 유효한 블록 규칙이 다르도록 보장해야 합니다.

### Payload Section Decrypted data

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 작습니다. 모든 블록 유형이 지원됩니다. 일반적인 내용에는 다음 블록들이 포함됩니다:

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

암호화된 프레임에는 0개 이상의 블록이 있습니다. 각 블록은 1바이트 식별자, 2바이트 길이, 그리고 0바이트 이상의 데이터를 포함합니다.

확장성을 위해, 수신자는 알려지지 않은 타입 번호를 가진 블록들을 반드시 무시해야 하며, 이를 패딩으로 처리해야 합니다.

암호화된 데이터는 16바이트 인증 헤더를 포함하여 최대 65535바이트이므로, 암호화되지 않은 데이터의 최대 크기는 65519바이트입니다.

(Poly1305 인증 태그는 표시되지 않음):

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

New Session 메시지에서 DateTime 블록은 필수이며, 첫 번째 블록이어야 합니다.

기타 허용되는 블록:

- Garlic Clove (타입 11)
- Options (타입 5)
- Padding (타입 254)

New Session Reply 메시지에서는 블록이 필요하지 않습니다.

기타 허용된 블록:

- Garlic Clove (타입 11)
- Options (타입 5)
- Padding (타입 254)

다른 블록은 허용되지 않습니다. 패딩이 있는 경우 마지막 블록이어야 합니다.

기존 세션 메시지에서는 블록이 필요하지 않으며, 다음 요구사항을 제외하고는 순서가 지정되지 않습니다:

Termination이 있는 경우, Padding을 제외하고 마지막 블록이어야 합니다. Padding이 있는 경우, 마지막 블록이어야 합니다.

단일 프레임에는 여러 개의 Garlic Clove 블록이 있을 수 있습니다. 단일 프레임에는 최대 두 개의 Next Key 블록이 있을 수 있습니다. 단일 프레임에서는 여러 개의 Padding 블록이 허용되지 않습니다. 다른 블록 유형들은 단일 프레임에 여러 블록을 가질 가능성이 낮지만 금지되어 있지는 않습니다.

### DateTime

만료 시각. 재전송 방지를 돕습니다. Bob은 이 타임스탬프를 사용하여 메시지가 최근 것인지 검증해야 합니다. Bob은 시간이 유효한 경우 재전송 공격을 방지하기 위해 Bloom filter 또는 다른 메커니즘을 구현해야 합니다. 일반적으로 New Session 메시지에만 포함됩니다.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Session Tag Ratchet

[I2NP](/docs/specs/i2np/)에서 명시된 단일 복호화된 Garlic Clove로, 사용되지 않거나 중복되는 필드를 제거하도록 수정되었습니다. 경고: 이 형식은 ElGamal/AES용과 상당히 다릅니다. 각 clove는 별도의 페이로드 블록입니다. Garlic Clove는 블록 간이나 ChaChaPoly 프레임 간에 단편화될 수 없습니다.

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
주의사항:

- 구현자는 블록을 읽을 때, 잘못된 형식이나 악의적인 데이터가
  다음 블록으로의 읽기 오버런을 발생시키지 않도록 보장해야 합니다.

- [I2NP](/docs/specs/i2np/)에서 명시된 Clove Set 형식은 사용되지 않습니다.
  각 clove는 자체 블록에 포함됩니다.

- I2NP 메시지 헤더는 9바이트이며, [NTCP2](/docs/specs/ntcp2/)에서 사용되는 것과 동일한 형식을 가집니다.

- [I2NP](/docs/specs/i2np/)의 Garlic Message 정의에서 Certificate, Message ID, Expiration은 포함되지 않습니다.

- [I2NP](/docs/specs/i2np/)의 Garlic Clove 정의에서 Certificate, Clove ID, Expiration은 포함되지 않습니다.

정당화:

- 인증서는 전혀 사용되지 않았습니다.
- 별도의 메시지 ID와 clove ID는 전혀 사용되지 않았습니다.
- 별도의 만료 시간은 전혀 사용되지 않았습니다.
- 기존 Clove Set 및 Clove 형식과 비교한 전체적인 절약은
  clove 1개의 경우 약 35바이트, clove 2개의 경우 54바이트,
  clove 3개의 경우 73바이트입니다.
- 블록 형식은 확장 가능하며 새로운 블록 타입으로
  새로운 필드를 추가할 수 있습니다.

### Termination

구현은 선택 사항입니다. 세션을 중단합니다. 이것은 프레임에서 패딩이 아닌 마지막 블록이어야 합니다. 이 세션에서는 더 이상 메시지가 전송되지 않습니다.

NS 또는 NSR에서는 허용되지 않습니다. Existing Session 메시지에만 포함됩니다.

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) 대칭 키 래칫

구현되지 않음, 추가 연구 필요. 업데이트된 옵션을 전달. 옵션에는 세션에 대한 다양한 매개변수가 포함됨. 자세한 정보는 아래의 Session Tag Length Analysis 섹션을 참조.

options 블록은 more_options가 존재할 수 있으므로 가변 길이일 수 있습니다.

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW는 송신자가 수신자에게 제공하는 수신자의 인바운드 태그 윈도우(최대 lookahead)에 대한 권장사항입니다. RITW는 송신자가 사용할 계획인 인바운드 태그 윈도우(최대 lookahead)에 대한 송신자의 선언입니다. 그러면 각 측은 최소값이나 최대값 또는 기타 계산을 기반으로 lookahead를 설정하거나 조정합니다.

참고사항:

- 기본이 아닌 세션 태그 길이에 대한 지원은 hopefully
  결코 필요하지 않을 것입니다.
- 태그 윈도우는 Signal 문서에서 MAX_SKIP입니다.

이슈:

- 옵션 협상은 TBD입니다.
- 기본값은 TBD입니다.
- 패딩과 지연 옵션은 NTCP2에서 복사되었지만,
  해당 옵션들은 그곳에서 완전히 구현되거나 연구되지 않았습니다.

### Message Numbers

구현은 선택 사항입니다. 이전 태그 집합(PN)의 길이(전송된 메시지 수)입니다. 수신자는 이전 태그 집합에서 PN보다 높은 태그를 즉시 삭제할 수 있습니다. 수신자는 이전 태그 집합에서 PN보다 작거나 같은 태그를 짧은 시간(예: 2분) 후에 만료시킬 수 있습니다.

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
참고사항:

- 최대 PN은 65535입니다.
- PN의 정의는 Signal의 정의에서 1을 뺀 것과 같습니다.
  이는 Signal이 하는 것과 비슷하지만, Signal에서는 PN과 N이 헤더에 있습니다.
  여기서는 암호화된 메시지 본문에 있습니다.
- 이전 tag set이 없었기 때문에 tag set 0에서는 이 블록을 전송하지 마십시오.

### 5) 페이로드

다음 DH ratchet 키는 페이로드에 있으며 선택사항입니다. 우리는 매번 ratchet을 수행하지 않습니다. (이는 헤더에 있고 매번 전송되는 signal과는 다릅니다)

첫 번째 ratchet의 경우, Key ID = 0입니다.

NS 또는 NSR에서는 허용되지 않습니다. 기존 세션 메시지에만 포함됩니다.

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
참고사항:

- Key ID는 해당 태그 세트에 사용되는 로컬 키에 대한 증분 카운터로, 0부터 시작합니다.
- ID는 키가 변경되지 않는 한 변경되어서는 안 됩니다.
- 엄격히 필요하지는 않을 수 있지만, 디버깅에 유용합니다.
  Signal은 key ID를 사용하지 않습니다.
- 최대 Key ID는 32767입니다.
- 양방향 태그 세트가 동시에 ratcheting하는 드문 경우에는, 프레임에 두 개의 Next Key 블록이 포함됩니다. 하나는 순방향 키용이고 다른 하나는 역방향 키용입니다.
- 키와 태그 세트 ID 번호는 순차적이어야 합니다.
- 자세한 내용은 위의 DH Ratchet 섹션을 참조하십시오.

### Payload Section 복호화된 데이터

이것은 ack 요청 블록이 수신된 경우에만 전송됩니다. 여러 메시지를 ack하기 위해 여러 ack가 존재할 수 있습니다.

NS 또는 NSR에서는 허용되지 않습니다. 기존 세션 메시지에만 포함됩니다.

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
참고사항:

- 태그 세트 ID와 N은 확인 응답되는 메시지를 고유하게 식별합니다.
- 각 방향으로 세션에서 사용되는 첫 번째 태그 세트에서, 태그 세트 ID는 0입니다.
- NextKey 블록이 전송되지 않았으므로 키 ID가 없습니다.
- NextKey 교환 후 사용되는 모든 태그 세트의 경우, 태그 세트 번호는 (1 + Alice의 키 ID + Bob의 키 ID)입니다.

### 암호화되지 않은 데이터

in-band ack를 요청합니다. Garlic Clove에서 out-of-band DeliveryStatus Message를 대체하기 위해서입니다.

명시적인 ack가 요청되면, 현재 tagset ID와 메시지 번호(N)가 ack 블록에 반환됩니다.

NS 또는 NSR에서는 허용되지 않습니다. 기존 세션 메시지에만 포함됩니다.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### 블록 순서 규칙

모든 패딩은 AEAD 프레임 내부에 있습니다. TODO AEAD 내부의 패딩은 협상된 매개변수를 대략적으로 준수해야 합니다. TODO Alice는 NS 메시지에서 요청된 tx/rx 최소/최대 매개변수를 보냈습니다. TODO Bob은 NSR 메시지에서 요청된 tx/rx 최소/최대 매개변수를 보냈습니다. 업데이트된 옵션은 데이터 단계 중에 전송될 수 있습니다. 위의 옵션 블록 정보를 참조하세요.

존재하는 경우, 이는 프레임의 마지막 블록이어야 합니다.

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
참고사항:

- 전체가 0인 패딩은 암호화될 것이므로 문제없습니다.
- 패딩 전략은 추후 결정 예정입니다.
- 패딩 전용 프레임이 허용됩니다.
- 패딩 기본값은 0-15바이트입니다.
- 패딩 매개변수 협상에 대해서는 옵션 블록을 참조하세요
- 최소/최대 패딩 매개변수에 대해서는 옵션 블록을 참조하세요
- 협상된 패딩 위반 시 router 응답은 구현에 따라 달라집니다.

### 날짜시간

구현체들은 향후 호환성을 위해 알 수 없는 블록 유형을 무시해야 합니다.

### Garlic Clove

- 패딩 길이는 메시지별로 결정되고 길이 분포를 추정하거나, 무작위 지연이 추가되어야 합니다. 이러한 대응책은 DPI에 대응하기 위해 포함되어야 하며, 그렇지 않으면 메시지 크기로 인해 전송 프로토콜이 I2P 트래픽을 전송하고 있다는 것이 드러날 수 있습니다. 정확한 패딩 방식은 향후 작업 영역이며, 부록 A에서 이 주제에 대한 자세한 정보를 제공합니다.

## Typical Usage Patterns

### 종료

이것은 가장 일반적인 사용 사례이며, 대부분의 비HTTP 스트리밍 사용 사례들도 이 사용 사례와 동일할 것입니다. 작은 초기 메시지가 전송되고, 응답이 뒤따르며, 양방향으로 추가 메시지들이 전송됩니다.

HTTP GET은 일반적으로 단일 I2NP 메시지에 들어맞습니다. Alice는 응답 leaseSet을 묶어서 단일 새 Session 메시지로 작은 요청을 보냅니다. Alice는 새 키로의 즉시 ratchet을 포함합니다. 목적지에 바인딩하기 위한 서명을 포함합니다. 확인 응답(ack)은 요청되지 않습니다.

Bob이 즉시 ratchet합니다.

Alice는 즉시 ratchet합니다.

해당 세션들과 함께 계속됩니다.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### 옵션

Alice는 세 가지 옵션이 있습니다:

1) HTTP GET에서와 같이 첫 번째 메시지만 전송 (window size = 1). 권장하지 않음.

2) streaming window까지 전송하되, 동일한 Elligator2로 인코딩된 cleartext public key를 사용합니다. 모든 메시지는 동일한 next public key (ratchet)를 포함합니다. 이는 모두 동일한 cleartext로 시작하기 때문에 OBGW/IBEP에게 보일 것입니다. 과정은 1)과 동일하게 진행됩니다. 권장하지 않습니다.

3) 권장 구현.    스트리밍 윈도우까지 전송하되, 각각에 대해 서로 다른 Elligator2로 인코딩된 평문 공개 키(세션)를 사용합니다.    모든 메시지는 동일한 다음 공개 키(ratchet)를 포함합니다.    모두 서로 다른 평문으로 시작하기 때문에 OBGW/IBEP에는 보이지 않습니다.    Bob은 모든 메시지가 동일한 다음 공개 키를 포함한다는 것을 인식해야 하며,    모든 메시지에 동일한 ratchet으로 응답해야 합니다.    Alice는 해당 다음 공개 키를 사용하여 계속 진행합니다.

옵션 3 메시지 플로우:

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### 메시지 번호

단일 응답이 예상되는 단일 메시지입니다. 추가 메시지나 응답이 전송될 수 있습니다.

HTTP GET과 유사하지만, 세션 태그 창 크기와 수명에 대한 더 작은 옵션을 제공합니다. ratchet을 요청하지 않을 수도 있습니다.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### 다음 DH Ratchet 공개 키

응답이 예상되지 않는 다수의 익명 메시지.

이 시나리오에서는 Alice가 세션을 요청하지만 바인딩은 하지 않습니다. 새 세션 메시지가 전송됩니다. 응답 LS는 번들되지 않습니다. 응답 DSM이 번들됩니다 (이것이 번들된 DSM이 필요한 유일한 사용 사례입니다). 다음 키는 포함되지 않습니다. 응답이나 ratchet이 요청되지 않습니다. Ratchet이 전송되지 않습니다. 옵션은 세션 태그 윈도우를 0으로 설정합니다.

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### 확인

응답이 예상되지 않는 단일 익명 메시지.

일회성 메시지가 전송됩니다. 응답 LS나 DSM은 번들되지 않습니다. 다음 키는 포함되지 않습니다. 응답이나 ratchet이 요청되지 않습니다. Ratchet이 전송되지 않습니다. 옵션은 세션 태그 윈도우를 0으로 설정합니다.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Ack 요청

장기간 지속되는 세션은 해당 시점부터 순방향 비밀성을 유지하기 위해 언제든지 ratchet하거나 ratchet을 요청할 수 있습니다. 세션은 세션당 전송 메시지 한계(65535개)에 접근할 때 반드시 ratchet해야 합니다.

## Implementation Considerations

### 패딩

기존 ElGamal/AES+SessionTag 프로토콜과 마찬가지로, 구현체는 세션 태그 저장을 제한하고 메모리 고갈 공격으로부터 보호해야 합니다.

권장되는 몇 가지 전략은 다음과 같습니다:

- 저장되는 세션 태그 수에 대한 하드 리미트
- 메모리 압박 상황에서 유휴 인바운드 세션의 적극적인 만료
- 단일 원격 목적지에 바인딩되는 인바운드 세션 수 제한
- 메모리 압박 상황에서 세션 태그 윈도우의 적응형 축소 및 사용되지 않는 오래된 태그 삭제
- 메모리 압박 상황에서 요청되더라도 래칫 수행 거부

### 다른 블록 타입

권장 매개변수 및 시간 초과:

- NSR tagset 크기: 12 tsmin 및 tsmax
- ES tagset 0 크기: tsmin 24, tsmax 160
- ES tagset (1+) 크기: 160 tsmin 및 tsmax
- NSR tagset 타임아웃: 수신자 3분
- ES tagset 타임아웃: 송신자 8분, 수신자 10분
- 이전 ES tagset 제거 시점: 3분 후
- 태그 N의 Tagset look ahead: min(tsmax, tsmin + N/4)
- 태그 N의 Tagset trim behind: min(tsmax, tsmin + N/4) / 2
- 다음 키 전송 태그: TBD
- tagset 수명 후 다음 키 전송: TBD
- NS 수신 후 세션 교체 시점: 3분 후
- 최대 클록 스큐: -5분 ~ +2분
- NS 리플레이 필터 지속 시간: 5분
- 패딩 크기: 0-15바이트 (기타 전략은 TBD)

### 향후 작업

다음은 수신 메시지를 분류하기 위한 권장사항입니다.

### X25519 Only

이 프로토콜만 사용하는 터널에서는 현재 ElGamal/AES+SessionTags로 수행되는 것처럼 식별을 수행합니다:

먼저, 초기 데이터를 session tag로 취급하고, session tag를 조회합니다. 발견되면, 해당 session tag와 연결된 저장된 데이터를 사용하여 복호화합니다.

찾을 수 없는 경우, 초기 데이터를 DH 공개 키와 nonce로 취급합니다. DH 연산과 지정된 KDF를 수행하고, 나머지 데이터를 복호화를 시도합니다.

### HTTP GET

이 프로토콜과 ElGamal/AES+SessionTags를 모두 지원하는 터널에서는 들어오는 메시지를 다음과 같이 분류합니다:

ElGamal/AES+SessionTags 사양의 결함으로 인해 AES 블록이 임의의 non-mod-16 길이로 패딩되지 않습니다. 따라서 Existing Session 메시지의 길이를 mod 16으로 나눈 나머지는 항상 0이고, New Session 메시지의 길이를 mod 16으로 나눈 나머지는 항상 2입니다 (ElGamal 블록이 514바이트 길이이므로).

길이를 16으로 나눈 나머지가 0 또는 2가 아닌 경우, 초기 데이터를 session tag로 취급하고 해당 session tag를 조회합니다. 찾은 경우, 해당 session tag와 연결된 저장된 데이터를 사용하여 복호화합니다.

찾을 수 없고 길이를 16으로 나눈 나머지가 0 또는 2가 아닌 경우, 초기 데이터를 DH public key와 nonce로 처리합니다. DH 연산과 지정된 KDF를 수행하고, 나머지 데이터의 복호화를 시도합니다. (상대적인 트래픽 혼합과 X25519 및 ElGamal DH 연산의 상대적 비용을 기반으로, 이 단계는 대신 마지막에 수행될 수 있습니다)

그렇지 않고, 길이를 16으로 나눈 나머지가 0이면, 초기 데이터를 ElGamal/AES session tag로 처리하고 해당 session tag를 조회합니다. 찾을 경우, 해당 session tag와 연결된 저장된 데이터를 사용하여 복호화합니다.

찾을 수 없고, 데이터가 최소 642(514 + 128)바이트 길이이며, 길이를 16으로 나눈 나머지가 2인 경우, 초기 데이터를 ElGamal 블록으로 처리합니다. 나머지 데이터의 복호화를 시도합니다.

ElGamal/AES+SessionTag 사양이 non-mod-16 패딩을 허용하도록 업데이트되면, 작업을 다르게 수행해야 할 것입니다.

### HTTP POST

초기 구현들은 상위 계층에서의 양방향 트래픽에 의존합니다. 즉, 구현들은 반대 방향의 트래픽이 곧 전송될 것이라고 가정하며, 이는 ECIES 계층에서 필요한 응답을 강제로 발생시킵니다.

그러나 특정 트래픽은 단방향이거나 매우 낮은 대역폭을 가질 수 있어서, 적시에 응답을 생성할 상위 계층 트래픽이 없을 수 있습니다.

NS 및 NSR 메시지 수신은 응답이 필요하며, ACK Request 및 Next Key 블록 수신 역시 응답이 필요합니다.

정교한 구현에서는 응답이 필요한 이러한 메시지 중 하나를 받을 때 타이머를 시작할 수 있으며, 짧은 시간(예: 1초) 내에 역방향 트래픽이 전송되지 않으면 ECIES 계층에서 "빈"(Garlic Clove 블록 없음) 응답을 생성할 수 있습니다.

NS 및 NSR 메시지에 대한 응답에 더욱 짧은 타임아웃을 적용하여 트래픽을 효율적인 ES 메시지로 가능한 한 빨리 전환하는 것도 적절할 수 있습니다.

## Analysis

### 응답 가능한 데이터그램

각 방향에서 처음 두 메시지에 대한 메시지 오버헤드는 다음과 같습니다. 이는 ACK 전에 각 방향으로 하나의 메시지만 있거나, 추가 메시지들이 기존 세션 메시지로 추측적으로 전송되는 것으로 가정합니다. 전달된 세션 태그의 추측적 ack이 없다면, 기존 프로토콜의 오버헤드는 훨씬 높습니다.

새로운 프로토콜의 분석에서는 패딩이 없다고 가정합니다. 번들된 leaseSet은 없다고 가정합니다.

### 다중 원시 데이터그램

새 세션 메시지, 각 방향에서 동일:

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
기존 세션 메시지, 각 방향 동일:

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### 단일 원시 데이터그램

Alice-to-Bob 새 세션 메시지:

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Bob에서 Alice로의 새 세션 응답 메시지:

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
기존 세션 메시지, 각 방향 동일:

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### 장기 지속 세션

총 4개의 메시지 (각 방향으로 2개씩):

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
핸드셰이크만:

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
장기 총계 (핸드셰이크 제외):

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO 제안서가 안정화된 후 이 섹션을 업데이트하세요.

다음 암호화 연산들이 New Session과 New Session Reply 메시지를 교환하기 위해 각 당사자에게 필요합니다:

- HMAC-SHA256: HKDF당 3개, 총계 미정
- ChaChaPoly: 각각 2개
- X25519 키 생성: Alice 2개, Bob 1개
- X25519 DH: 각각 3개
- 서명 검증: 1개 (Bob)

Alice는 바운드 세션당 최소 5개의 ECDH를 계산하며, Bob에게 보내는 각 NS 메시지에 대해 2개, Bob의 각 NSR 메시지에 대해 3개를 계산합니다.

Bob도 바운드 세션당 6개의 ECDH를 계산하며, Alice의 NS 메시지 각각에 대해 3개, 자신의 NSR 메시지 각각에 대해 3개를 계산합니다.

각 기존 세션(Existing Session) 메시지에 대해 각 당사자가 수행해야 하는 암호화 작업은 다음과 같습니다:

- HKDF: 2
- ChaChaPoly: 1

### 방어

현재 세션 태그 길이는 32바이트입니다. 아직 해당 길이에 대한 정당성을 찾지 못했지만, 아카이브 연구를 계속하고 있습니다. 위의 제안서는 새로운 태그 길이를 8바이트로 정의합니다. 8바이트 태그를 정당화하는 분석은 다음과 같습니다:

세션 태그 래칫(session tag ratchet)은 무작위로 균등하게 분산된 태그를 생성하는 것으로 가정됩니다. 특정 세션 태그 길이에 대한 암호학적 이유는 없습니다. 세션 태그 래칫은 대칭 키 래칫(symmetric key ratchet)과 동기화되지만 독립적인 출력을 생성합니다. 두 래칫의 출력은 서로 다른 길이일 수 있습니다.

따라서 유일한 우려사항은 session tag 충돌입니다. 구현체들이 두 세션 모두로 복호화를 시도하여 충돌을 처리하려 하지 않을 것으로 가정합니다. 구현체들은 단순히 태그를 이전 세션이나 새 세션 중 하나와 연결하며, 다른 세션에서 해당 태그로 수신된 모든 메시지는 복호화 실패 후 폐기됩니다.

목표는 충돌 위험을 최소화할 수 있을 만큼 충분히 크면서도 메모리 사용량을 최소화할 수 있을 만큼 작은 세션 태그 길이를 선택하는 것입니다.

이는 구현체가 메모리 고갈 공격을 방지하기 위해 세션 태그 저장을 제한한다고 가정합니다. 이는 또한 공격자가 충돌을 생성할 가능성을 크게 줄일 것입니다. 아래의 구현 고려사항 섹션을 참조하십시오.

최악의 경우를 가정하면, 초당 64개의 새로운 인바운드 세션을 처리하는 바쁜 서버가 있다고 하자. 인바운드 세션 태그 수명을 15분(현재와 동일하며, 아마도 줄여야 할 것)이라고 가정한다. 인바운드 세션 태그 윈도우를 32라고 가정한다. 64 * 15 * 60 * 32 = 1,843,200개의 태그. 현재 Java I2P의 최대 인바운드 태그 수는 750,000개이며, 우리가 아는 한 이 수치에 도달한 적이 없다.

백만 분의 1 (1e-6) 세션 태그 충돌 목표는 아마도 충분할 것입니다. 혼잡으로 인해 도중에 메시지가 드롭될 확률이 그보다 훨씬 높습니다.

참조: https://en.wikipedia.org/wiki/Birthday_paradox 확률 표 섹션.

32바이트 session tag(256비트)를 사용하면 session tag 공간은 1.2e77입니다. 확률 1e-18로 충돌이 발생할 확률에는 4.8e29개의 항목이 필요합니다. 확률 1e-6으로 충돌이 발생할 확률에는 4.8e35개의 항목이 필요합니다. 각각 32바이트인 180만 개의 tag는 총 약 59MB입니다.

16바이트 session tag (128비트)를 사용하면 session tag 공간은 3.4e38입니다. 확률이 1e-18인 충돌 확률을 위해서는 2.6e10개의 항목이 필요합니다. 확률이 1e-6인 충돌 확률을 위해서는 2.6e16개의 항목이 필요합니다. 각각 16바이트인 180만 개의 태그는 총 약 30MB입니다.

8바이트 session tag(64비트)를 사용할 때 session tag 공간은 1.8e19입니다. 충돌 확률이 1e-18인 경우 6.1개의 항목이 필요합니다. 충돌 확률이 1e-6인 경우 6.1e6(6,100,000)개의 항목이 필요합니다. 각각 8바이트인 180만 개의 tag는 총 약 15MB입니다.

610만 개의 활성 태그는 우리의 최악의 경우 추정치인 180만 태그보다 3배 이상 많습니다. 따라서 충돌 확률은 백만 분의 일 미만이 될 것입니다. 따라서 우리는 8바이트 세션 태그가 충분하다고 결론지었습니다. 이는 전송 태그가 저장되지 않기 때문에 2배 감소에 더하여 저장 공간의 4배 감소를 가져옵니다. 따라서 우리는 ElGamal/AES+SessionTags에 비해 세션 태그 메모리 사용량을 8배 줄일 수 있습니다.

이러한 가정이 틀릴 경우 유연성을 유지하기 위해 옵션에 session tag 길이 필드를 포함하여 기본 길이가 세션별로 재정의될 수 있도록 할 것입니다. 절대적으로 필요하지 않는 한 동적 tag 길이 협상은 구현하지 않을 예정입니다.

구현체는 최소한 세션 태그 충돌을 인식하고, 이를 우아하게 처리하며, 충돌 횟수를 로그에 기록하거나 카운트해야 합니다. 여전히 극히 드물긴 하지만, ElGamal/AES+SessionTags보다는 훨씬 더 발생할 가능성이 높으며, 실제로 일어날 수 있습니다.

### 매개변수

초당 세션 수를 두 배(128)로, 태그 윈도우를 두 배(64)로 사용하면 태그가 4배(740만 개)가 됩니다. 백만 분의 일 충돌 확률의 최대값은 610만 개 태그입니다. 12바이트(또는 10바이트) 태그는 훨씬 큰 여유를 제공할 것입니다.

하지만 백만 분의 일의 충돌 확률이 좋은 목표일까요? 경로상에서 드롭될 확률보다 훨씬 큰 값은 별로 유용하지 않습니다. Java의 DecayingBloomFilter에 대한 거짓 양성(false-positive) 목표는 대략 만 분의 일이지만, 천 분의 일이라도 심각한 우려사항은 아닙니다. 목표를 만 분의 일로 줄임으로써 8바이트 태그로도 충분한 여유가 있습니다.

### 분류

발신자는 태그와 키를 즉석에서 생성하므로 저장소가 필요하지 않습니다. 이는 ElGamal/AES에 비해 전체 저장 요구사항을 절반으로 줄입니다. ECIES 태그는 ElGamal/AES의 32바이트 대신 8바이트입니다. 이는 전체 저장 요구사항을 또 다른 4배 요인만큼 줄입니다. 태그별 세션 키는 합리적인 손실률에서 최소화되는 "gaps"을 제외하고는 수신자에서 저장되지 않습니다.

태그 만료 시간의 33% 단축은 짧은 세션 시간을 가정할 때 추가로 33%의 절약 효과를 가져옵니다.

따라서 ElGamal/AES 대비 총 공간 절약은 10.7배, 즉 92%입니다.

## Related Changes

### X25519만

ECIES Destinations에서의 데이터베이스 조회: [제안 154](/proposals/154-ecies-lookups)를 참조하세요. 이는 현재 릴리스 0.9.46용 [I2NP](/docs/specs/i2np/)에 통합되었습니다.

이 제안은 X25519 공개 키를 leaseSet과 함께 게시하기 위해 LS2 지원이 필요합니다. [I2NP](/docs/specs/i2np/)의 LS2 사양에는 변경이 필요하지 않습니다. 모든 지원은 0.9.38에서 구현된 [Proposal 123](/proposals/123-new-netdb-entries)에서 설계, 명시, 구현되었습니다.

### X25519 공유와 ElGamal/AES+SessionTags

없음. 이 제안은 LS2 지원과 I2CP 옵션에서 활성화될 속성 설정이 필요합니다. [I2CP](/docs/specs/i2cp/) 사양에는 변경 사항이 필요하지 않습니다. 모든 지원은 0.9.38에서 구현된 [Proposal 123](/proposals/123-new-netdb-entries)에서 설계, 명세화 및 구현되었습니다.

ECIES를 활성화하는 데 필요한 옵션은 I2CP, BOB, SAM 또는 i2ptunnel에 대한 단일 I2CP 속성입니다.

일반적인 값은 ECIES 전용의 경우 i2cp.leaseSetEncType=4이고, ECIES와 ElGamal 듀얼 키의 경우 i2cp.leaseSetEncType=4,0입니다.

### 프로토콜 계층 응답

이 섹션은 [Proposal 123](/proposals/123-new-netdb-entries)에서 복사되었습니다.

SessionConfig 매핑의 옵션:

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

이 제안은 릴리스 0.9.38부터 지원되는 LS2가 필요합니다. [I2CP](/docs/specs/i2cp/) 사양에는 변경 사항이 필요하지 않습니다. 모든 지원은 0.9.38에서 구현된 [Proposal 123](/proposals/123-new-netdb-entries)에서 설계, 명세화 및 구현되었습니다.

### 오버헤드

이중 키로 LS2를 지원하는 모든 router (0.9.38 이상)는 이중 키를 가진 대상과의 연결을 지원해야 합니다.

ECIES 전용 목적지는 암호화된 조회 응답을 받기 위해 floodfill의 대부분이 0.9.46으로 업데이트되어야 합니다. [제안서 154](/proposals/154-ecies-lookups)를 참조하세요.

ECIES 전용 destination은 ECIES 전용이거나 이중 키를 사용하는 다른 destination과만 연결할 수 있습니다.
