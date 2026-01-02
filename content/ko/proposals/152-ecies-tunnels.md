---
title: "ECIES Tunnels"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "닫힘"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## 참고

네트워크 배포 및 테스트가 진행 중입니다. 소폭의 수정이 있을 수 있습니다. 공식 명세는 [SPEC](/docs/specs/implementation/)을 참조하세요.

## 개요

이 문서는 [ECIES-X25519](/docs/specs/ecies/)에서 도입된 암호 프리미티브(기본 암호 구성 요소)를 사용하여 Tunnel Build 메시지 암호화를 변경하는 방안을 제안한다. 이는 routers를 ElGamal에서 ECIES-X25519 키로 전환하기 위한 전체 제안서 [Proposal 156](/proposals/156-ecies-routers)의 일부다.

네트워크를 ElGamal + AES256에서 ECIES + ChaCha20으로 전환하기 위해서는 ElGamal 및 ECIES routers가 혼재된 tunnels이 필요하다. 혼합된 tunnel 홉을 처리하기 위한 사양이 제공된다. ElGamal 홉의 형식, 처리, 암호화에는 어떤 변경도 가하지 않는다.

ElGamal(엘가말) tunnel 생성자들은 각 홉(hop)마다 임시 X25519 키 쌍을 생성해야 하며, ECIES(타원곡선 통합 암호화 방식) 홉을 포함하는 tunnels를 생성할 때 이 명세를 따라야 합니다.

이 제안서는 ECIES-X25519 Tunnel 구축에 필요한 변경 사항을 규정합니다. ECIES routers에 필요한 모든 변경 사항의 개요는 제안 156 [Proposal 156](/proposals/156-ecies-routers)을 참조하십시오.

이 제안은 호환성 요구 사항에 따라 tunnel 빌드 레코드의 크기를 동일하게 유지합니다. 더 작은 빌드 레코드와 메시지는 이후에 구현될 예정입니다 - [Proposal 157](/proposals/157-new-tbm)을 참조하세요.

### 암호학적 기본 요소

새로운 암호학적 프리미티브는 도입되지 않습니다. 이 제안을 구현하는 데 필요한 프리미티브는 다음과 같습니다:

- AES-256-CBC는 [Cryptography](/docs/specs/cryptography/)에서와 같이
- STREAM ChaCha20/Poly1305 함수:
  ENCRYPT(k, n, plaintext, ad) 및 DECRYPT(k, n, ciphertext, ad) - [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) 및 [RFC-7539](https://tools.ietf.org/html/rfc7539)에서와 같이
- X25519 DH 함수 - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이
- HKDF(salt, ikm, info, n) (HMAC 기반 키 파생 함수) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이

다른 곳에 정의된 기타 Noise 함수:

- MixHash(d) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이
- MixKey(d) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이

### 목표


### 비목표

- "flag day"(네트워크 전체가 동시에 전환해야 하는 날)이 필요한 tunnel 빌드 메시지의 전면 재설계.
- tunnel 빌드 메시지 축소 (모든 홉이 ECIES여야 하며 새로운 제안이 필요)
- [Proposal 143](/proposals/143-build-message-options)에서 정의된 tunnel 빌드 옵션 사용, 작은 메시지에만 필요
- 양방향 tunnel - 이에 대해서는 [Proposal 119](/proposals/119-bidirectional-tunnels) 참조
- 더 작은 tunnel 빌드 메시지 - 이에 대해서는 [Proposal 157](/proposals/157-new-tbm) 참조

## 위협 모델

### 설계 목표

- 어떤 홉도 tunnel의 생성자를 식별할 수 없다.

- 중간 홉은 tunnel의 방향이나
  tunnel 내에서 자신의 위치를 식별할 수 없어야 한다.

- 어떤 홉도 다른 요청 또는 응답 레코드의 어떤 내용도 읽을 수 없으며, 예외는
  다음 홉을 위한 절단된 router 해시와 임시 키뿐이다

- outbound build(아웃바운드 빌드)에 사용하는 reply tunnel(응답용 tunnel)의 어느 구성원도 어떠한 reply records(응답 레코드)도 읽을 수 없다.

- 인바운드 빌드를 위한 outbound tunnel의 구성원은 요청 레코드를 전혀 읽을 수 없으며,
  단, OBEP은 IBGW에 대한 잘린 router 해시와 임시 키는 볼 수 있다

### 태깅 공격

tunnel 구축 설계의 주요 목표 중 하나는 공모하는 router X와 Y가 자신들이 같은 tunnel에 있다는 사실을 알아차리기 더 어렵게 만드는 것이다. 만약 router X가 홉 m에 있고 router Y가 홉 m+1에 있다면, 그들은 당연히 이를 알 수 있다. 그러나 router X가 홉 m에 있고 router Y가 n>1인 경우 홉 m+n에 있다면, 이를 파악하는 것은 훨씬 더 어려워야 한다.

태깅 공격은 중간 홉 router X가 tunnel 빌드 메시지를 변경하여, 그 빌드 메시지가 도착했을 때 router Y가 그 변경을 감지할 수 있도록 만드는 공격이다. 목표는 변경된 모든 메시지가 router Y에 도달하기 전에 X와 Y 사이의 router에 의해 버려지도록 하는 것이다. router Y 이전에서 버려지지 않은 변경의 경우, tunnel 생성자는 응답에서 손상을 감지하고 해당 tunnel을 폐기해야 한다.

가능한 공격:

- build record(빌드 레코드) 변경
- build record 교체
- build record 추가 또는 제거
- build record 순서 재정렬

TODO: 현재 설계가 이러한 모든 공격을 방지하나요?

## 설계

### Noise 프로토콜 프레임워크

이 제안서는 Noise Protocol Framework(Noise 프로토콜 프레임워크) [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)을 기반으로 한 요구 사항을 규정합니다. Noise 용어로는 Alice는 initiator(개시자), Bob은 responder(응답자)입니다.

이 제안은 Noise 프로토콜 Noise_N_25519_ChaChaPoly_SHA256를 기반으로 합니다. 이 Noise 프로토콜은 다음과 같은 암호 프리미티브를 사용합니다:

- 단방향 핸드셰이크 패턴: N
  Alice는 자신의 정적 키를 Bob에게 전송하지 않는다 (N)

- DH 함수: X25519
  [RFC-7748](https://tools.ietf.org/html/rfc7748)에 규정된 대로 키 길이가 32바이트인 X25519 디피-헬먼(DH).

- 암호 함수: ChaChaPoly
  AEAD_CHACHA20_POLY1305는 [RFC-7539](https://tools.ietf.org/html/rfc7539) 2.8절에 규정된 대로입니다.
  12바이트 nonce(재사용되지 않는 값)이며, 처음 4바이트는 0으로 설정됩니다.
  [NTCP2](/docs/specs/ntcp2/)와 동일합니다.

- 해시 함수: SHA256
  표준 32바이트 해시로, 이미 I2P에서 광범위하게 사용되고 있습니다.

#### 프레임워크 추가 사항

없음.

### 핸드셰이크 패턴

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드

빌드 요청은 Noise N pattern(Noise 프로토콜의 N 패턴)과 동일합니다. 이는 [NTCP2](/docs/specs/ntcp2/)에서 사용되는 XK pattern(Noise 프로토콜의 XK 패턴)의 첫 번째(세션 요청) 메시지와도 동일합니다.

```text
<- s
  ...
  e es p ->
```
### 요청 암호화

빌드 요청 레코드는 tunnel 생성자가 생성하며 각 홉에 대해 비대칭 방식으로 암호화된다. 이러한 요청 레코드의 비대칭 암호화는 현재 [Cryptography](/docs/specs/cryptography/)에 정의된 ElGamal을 사용하며, SHA-256 체크섬을 포함한다. 이 설계는 forward secrecy(순방향 보안)를 제공하지 않는다.

새로운 설계는 단방향 Noise(암호 프로토콜 프레임워크) 패턴 "N"과 ECIES-X25519 ephemeral-static DH(임시-정적 Diffie-Hellman), HKDF(키 파생 함수), 그리고 ChaCha20/Poly1305 AEAD(인증된 암호)를 사용하여 전방 기밀성, 무결성 및 인증을 제공한다. Alice는 tunnel 빌드 요청자이다. tunnel의 각 홉은 Bob이다.

(페이로드 보안 속성)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### 응답 암호화

빌드 응답 레코드는 홉의 생성자가 만들고, 생성자만 복호화할 수 있도록 대칭키로 암호화된다. 현재 이 응답 레코드의 대칭 암호화에는 앞부분에 SHA-256 체크섬을 덧붙인 AES가 사용된다. 또한 SHA-256 체크섬을 포함한다. 이 설계는 forward-secret(전방 비밀성: 세션 키가 유출되어도 과거 트래픽의 기밀성이 유지되는 특성)이 아니다.

새로운 설계는 무결성과 인증을 위해 ChaCha20/Poly1305 AEAD(부가 데이터가 포함된 인증된 암호)를 사용할 것입니다.

### 정당성

요청에 포함된 임시 공개키는 AES로 암호화하거나 Elligator2(타원곡선 공개키를 난수처럼 보이게 하는 기법)로 위장할 필요가 없다. 그것을 볼 수 있는 것은 이전 홉뿐이며, 그 홉은 다음 홉이 ECIES(타원곡선 기반 통합 암호화 방식)를 사용한다는 것을 알고 있다.

응답 레코드에는 추가적인 DH(Diffie-Hellman 키 교환)를 수반한 완전한 비대칭 암호화가 필요하지 않습니다.

## 명세

### 빌드 요청 레코드

호환성을 위해 암호화된 BuildRequestRecords(tunnel 구축 요청 레코드)는 ElGamal과 ECIES 모두에 대해 528바이트입니다.

#### 암호화되지 않은 요청 레코드(ElGamal)

참고로, 이것은 [I2NP](/docs/specs/i2np/)에서 가져온 ElGamal routers용 tunnel BuildRequestRecord(빌드 요청 레코드)의 현재 명세입니다. 암호화되지 않은 데이터 앞에는 [Cryptography](/docs/specs/cryptography/)에 정의된 대로 0이 아닌 바이트와 암호화 이전 데이터의 SHA-256 해시가 붙습니다.

모든 필드는 빅엔디언 바이트 순서를 사용합니다.

암호화되지 않은 크기: 222 바이트

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### 암호화된 요청 레코드 (ElGamal(엘가말))

참고로, 이는 [I2NP](/docs/specs/i2np/)에서 가져온 ElGamal routers용 tunnel BuildRequestRecord의 현재 사양입니다.

암호화된 크기: 528 바이트

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### 암호화되지 않은 요청 레코드 (ECIES)

이는 ECIES-X25519 routers용 tunnel BuildRequestRecord에 대한 제안된 명세입니다. 변경 사항 요약:

- 사용되지 않는 32바이트 router 해시 제거
- 요청 시간을 시간 단위에서 분 단위로 변경
- 향후 가변 tunnel 시간을 위해 만료 필드 추가
- 플래그용 공간을 더 추가
- 추가적인 빌드 옵션을 위한 매핑 추가
- AES-256 응답 키와 IV(초기화 벡터)는 해당 홉의 자체 응답 레코드에는 사용되지 않음
- 암호화되지 않은 레코드는 암호화 오버헤드가 더 적기 때문에 더 길어짐

요청 레코드에는 ChaCha 응답 키가 전혀 포함되어 있지 않습니다. 해당 키들은 KDF(키 유도 함수)에서 파생됩니다. 아래를 참조하십시오.

모든 필드는 빅엔디언입니다.

암호화되지 않은 크기: 464 바이트

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
flags 필드는 [Tunnel 생성](/docs/specs/implementation/)에 정의된 것과 동일하며 다음을 포함합니다::

비트 순서: 76543210 (비트 7은 MSB(최상위 비트))  비트 7: 설정된 경우, 누구로부터 오는 메시지를 허용  비트 6: 설정된 경우, 누구에게든 메시지 전송을 허용하고, 응답을 the로 보낸다

        specified next hop in a Tunnel Build Reply Message
비트 5-0: 정의되지 않았으며, 향후 옵션과의 호환성을 위해 0으로 설정해야 합니다

비트 7은 해당 홉이 inbound gateway(IBGW, 수신 게이트웨이)임을 나타냅니다.  비트 6은 해당 홉이 outbound endpoint(OBEP, 송신 종단점)임을 나타냅니다.  두 비트가 모두 설정되지 않은 경우, 해당 홉은 중간 참여자입니다.  두 비트를 동시에 설정할 수는 없습니다.

요청 만료 시간은 향후 가변적인 tunnel 지속 시간을 지원하기 위한 것입니다. 현재로서는 지원되는 값은 600(10분)뿐입니다.

tunnel 빌드 옵션은 [Common Structures](/docs/specs/common-structures/)에 정의된 Mapping(매핑) 구조이다. 이는 향후 사용을 위해 예약되어 있다. 현재 정의된 옵션은 없다. Mapping 구조가 비어 있으면 이는 2바이트 0x00 0x00이다. Mapping의 최대 크기(길이 필드를 포함)는 296바이트이며, Mapping 길이 필드의 최대값은 294이다.

#### 암호화된 요청 레코드(ECIES, 타원곡선 통합 암호화 방식)

모든 필드는 빅 엔디언이지만, ephemeral public key(임시 공개키)만 리틀 엔디언입니다.

암호화된 크기: 528 바이트

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### 빌드 응답 레코드

호환성을 위해 ElGamal과 ECIES 모두에서 암호화된 BuildReplyRecords(빌드 응답 레코드)의 크기는 528바이트입니다.

#### 암호화되지 않은 응답 레코드(ElGamal)

ElGamal 응답은 AES로 암호화됩니다.

모든 필드는 빅 엔디언입니다.

암호화되지 않은 크기: 528 바이트

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### 비암호화 응답 레코드 (ECIES, 타원곡선 통합 암호화 체계)

이는 ECIES-X25519 routers용 tunnel BuildReplyRecord의 제안된 명세입니다. 변경 사항 요약:

- build reply options(빌드 응답 옵션)에 대한 매핑 추가
- 암호화되지 않은 레코드는 암호화 오버헤드가 적어 더 길다

ECIES(타원 곡선 기반 통합 암호화 방식) 응답은 ChaCha20/Poly1305로 암호화됩니다.

모든 필드는 big-endian(빅엔디언)입니다.

암호화되지 않은 크기: 512바이트

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
tunnel 빌드 응답 옵션은 [공통 구조체](/docs/specs/common-structures/)에서 정의된 Mapping(매핑) 구조체입니다. 이는 향후 사용을 위한 것입니다. 현재 정의된 옵션은 없습니다. Mapping 구조체가 비어 있으면 0x00 0x00 두 바이트로 표시됩니다. Mapping의 최대 크기(길이 필드를 포함)는 511바이트이며, Mapping 길이 필드의 최대값은 509입니다.

응답 바이트는 지문 식별(fingerprinting)을 피하기 위해 [Tunnel Creation](/docs/specs/implementation/)에 정의된 다음 값 중 하나입니다:

- 0x00 (수락)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### 암호화된 응답 레코드 (ECIES, 타원곡선 통합 암호화 방식)

암호화된 크기: 528 바이트

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
ECIES(타원 곡선 통합 암호화 방식) 레코드로 완전히 전환된 후에는 범위 패딩 규칙이 요청 레코드와 동일합니다.

### 레코드의 대칭키 암호화

ElGamal(공개키 암호 방식)에서 ECIES(타원곡선 통합 암호화 방식)로의 전환을 위해 혼합 tunnel은 허용되며, 또한 필수적입니다. 전환 기간 동안 ECIES 키로 키가 설정된 router의 수가 점차 증가할 것입니다.

대칭키 암호 전처리도 마찬가지로 수행됩니다:

- "암호화":

- 복호화 모드로 동작하는 암호 알고리즘
  - 전처리 단계에서 요청 레코드를 선제적으로 복호화(암호화된 요청 레코드를 은폐)

- "decryption":

- 암호화 알고리즘이 암호화 모드에서 동작
  - 참여 홉들이 요청 레코드를 암호화함(다음 평문 요청 레코드를 드러냄)

- ChaCha20에는 "모드"가 없으므로, 단순히 세 번 실행됩니다:

- 전처리에서 한 번
  - 홉에서 한 번
  - 최종 응답 처리 시 한 번

혼합형 tunnels이 사용되는 경우, tunnel 생성자는 BuildRequestRecord(빌드 요청 레코드)의 대칭 암호화를 현재 및 이전 홉의 암호화 유형에 따라 설정해야 한다.

각 홉은 BuildReplyRecords(응답 빌드 레코드) 및 VariableTunnelBuildMessage(VTBM, 가변 tunnel 빌드 메시지) 내의 다른 레코드를 암호화하기 위해 각자의 암호화 유형을 사용한다.

응답 경로에서는 엔드포인트(송신자)가 각 홉의 응답 키를 사용하여 [다중 암호화](https://en.wikipedia.org/wiki/Multiple_encryption)를 역순으로 해제해야 한다.

설명을 위해, ElGamal(엘가말 공개키 암호)로 둘러싸인 ECIES(타원 곡선 기반 통합 암호 방식)을 사용하는 아웃바운드 tunnel을 살펴보자:

- 송신자 (OBGW) -> ElGamal(엘가말 공개키 암호화) (H1) -> ECIES(타원 곡선 기반 통합 암호화 체계) (H2) -> ElGamal (H3)

모든 BuildRequestRecords(빌드 요청 레코드)는 암호화된 상태이다(ElGamal 또는 ECIES 사용).

AES256/CBC 암호 방식은 사용되는 경우에도 각 레코드 단위로만 사용되며, 여러 레코드에 걸쳐 체이닝되지 않는다.

마찬가지로, ChaCha20은 각 레코드를 암호화하는 데 사용되며, VTBM 전체에 걸쳐 스트리밍되지는 않습니다.

요청 레코드는 송신자(OBGW)에 의해 전처리된다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:

- H2의 응답 키 (ChaCha20)
  - H1의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "암호화"됩니다:

- H1의 응답 키 (AES256/CBC)

- H1의 레코드는 대칭 암호화 없이 전송된다

H2만 응답 암호화 플래그를 검사하고, 그 뒤에 AES256/CBC가 따라온다는 것을 확인한다.

각 홉에서 처리된 후, 레코드는 "복호화된" 상태가 됩니다:

- H3의 레코드는 다음을 사용하여 "복호화"됩니다:

- H3의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "복호화"됩니다:

- H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20-Poly1305)

- H1의 레코드는 다음을 사용하여 "복호화"된다:

- H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20)
  - H1의 응답 키 (AES256/CBC)

tunnel 생성자, 일명 Inbound Endpoint (IBEP, 수신 종단점)은 응답을 후처리한다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)

- H2의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20-Poly1305)

- H1의 레코드는 다음을 사용하여 "암호화"됩니다:

- H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20)
  - H1의 응답 키 (AES256/CBC)

### 요청 레코드 키 (ECIES, 타원곡선 통합 암호화 체계)

이 키들은 ElGamal(엘가말) BuildRequestRecords(빌드 요청 레코드)에 명시적으로 포함됩니다. ECIES(타원 곡선 통합 암호 체계) BuildRequestRecords에서는 tunnel 키와 AES 응답 키가 포함되지만, ChaCha(스트림 암호) 응답 키는 DH(디피-헬먼) 교환으로부터 파생됩니다. router 정적 ECIES 키의 자세한 내용은 [제안 156](/proposals/156-ecies-routers)을 참조하세요.

아래는 이전에 요청 레코드를 통해 전송된 키를 도출하는 방법에 대한 설명입니다.

#### 초기 ck 및 h를 위한 KDF(키 유도 함수)

이는 패턴 "N"에 대한 표준 [NOISE](https://noiseprotocol.org/noise.html)이며, 표준 프로토콜 이름을 사용합니다.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### 요청 레코드용 KDF(키 유도 함수)

ElGamal tunnel 생성자는 tunnel 내 각 ECIES(타원곡선 기반 통합 암호 방식) 홉마다 임시 X25519(타원곡선 Diffie-Hellman 키 교환의 한 형태) 키 쌍을 생성하고, 위의 방식으로 자신의 BuildRequestRecord를 암호화한다. ElGamal tunnel 생성자는 ElGamal 홉에 대해서는 이 명세 이전의 방식을 사용해 암호화한다.

ECIES(타원 곡선 통합 암호화 체계) tunnel 생성자는 [Tunnel Creation](/docs/specs/implementation/)에 정의된 스킴을 사용하여 각 ElGamal(엘가말) 홉의 공개키로 암호화해야 합니다. ECIES tunnel 생성자는 ECIES 홉에 대한 암호화에 위 스킴을 사용합니다.

이는 tunnel 홉이 자기 암호화 유형에 해당하는 암호화된 레코드만 볼 수 있음을 의미합니다.

ElGamal 및 ECIES tunnel 생성자는 ECIES 홉으로 암호화하기 위해 홉마다 고유한 임시 X25519 키 쌍을 생성한다.

**중요**: 임시 키는 ECIES 홉마다, 그리고 각 build record(터널 구축 레코드)마다 고유해야 합니다. 고유한 키를 사용하지 않으면 공모하는 홉들이 자신들이 동일한 tunnel에 있음을 확인할 수 있는 공격 벡터가 열립니다.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
``replyKey``, ``layerKey`` 및 ``layerIV``는 여전히 ElGamal 레코드 내부에 포함되어야 하며, 무작위로 생성할 수 있습니다.

### 요청 레코드 암호화 (ElGamal, 엘가말 공개키 암호)

[Tunnel Creation](/docs/specs/implementation/)에 정의된 대로입니다. ElGamal 홉에 대한 암호화에는 변경 사항이 없습니다.

### 응답 레코드 암호화 (ECIES)

응답 레코드는 ChaCha20/Poly1305(스트림 암호 ChaCha20과 인증 알고리즘 Poly1305의 조합)로 암호화되어 있습니다.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### 응답 레코드 암호화 (ElGamal 공개키 암호 방식)

[Tunnel Creation](/docs/specs/implementation/)에 정의된 대로입니다. ElGamal 홉에 대한 암호화에는 변경 사항이 없습니다.

### 보안 분석

ElGamal은 Tunnel Build Messages에 대해 전방향 기밀성을 제공하지 않는다.

AES256/CBC는 상황이 약간 더 낫으며, 알려진 평문 `biclique` 공격으로 인한 이론적 약화에만 취약하다.

AES256/CBC에 대한 유일하게 알려진 실용적인 공격은 공격자가 IV(초기화 벡터)를 알고 있을 때 수행되는 패딩 오라클 공격이다.

공격자가 AES256/CBC 키 정보(회신 키와 IV(초기화 벡터))를 얻으려면 다음 홉의 ElGamal 암호화를 깨야 한다.

ElGamal(엘가말 암호)은 ECIES(타원곡선 통합 암호 방식)보다 훨씬 더 CPU 집약적이어서 잠재적으로 리소스 고갈을 초래할 수 있습니다.

ECIES는 BuildRequestRecord 또는 VariableTunnelBuildMessage마다 새로운 임시 키와 함께 사용될 때 순방향 보안을 제공합니다.

ChaCha20Poly1305(ChaCha20 스트림 암호와 Poly1305 메시지 인증 코드를 결합한 알고리즘)는 AEAD(연관 데이터가 있는 인증된 암호화)를 제공하여 수신자가 복호화를 시도하기 전에 메시지 무결성을 검증할 수 있다.

## 정당성

이 설계는 기존의 암호학적 프리미티브, 프로토콜, 그리고 코드를 최대한 재사용합니다. 이 설계는 위험을 최소화합니다.

## 구현 참고 사항

* 구형 routers는 홉의 암호화 유형을 확인하지 않고 ElGamal로 암호화된
  레코드를 보냅니다. 일부 최신 routers에는 버그가 있어 다양한 형태의 잘못된 레코드를 보낼 수 있습니다.
  구현자는 가능하다면 CPU 사용량을 줄이기 위해 DH(Diffie-Hellman) 연산 전에
  이러한 레코드를 탐지하고 거부해야 합니다.

## 문제

## 마이그레이션

[Proposal 156](/proposals/156-ecies-routers)을 참조하세요.

## 참고 문헌

* [공통](/docs/specs/common-structures/)
* [암호학](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [사양](/docs/specs/implementation/#tunnel-creation-ecies)
* [Tunnel 생성](/docs/specs/implementation/)
* [다중 암호화](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
