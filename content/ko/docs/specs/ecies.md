---
title: "ECIES-X25519-AEAD-Ratchet"
description: "I2P 종단 간 암호화를 위한 타원곡선 통합 암호화 방식"
slug: "ecies"
aliases:
  - "/ko/docs/specs/ecies-x25519-aead-ratchet"
  - "/ko/docs/specs/ecies-x25519-aead-ratchet/"
category: "프로토콜"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## 참고

네트워크 배포가 완료되었습니다. 사소한 수정이 있을 수 있습니다. 배경 논의 및 추가 정보를 포함한 원래 제안서는 [Prop144](/proposals/144-ecies-x25519/)를 참조하십시오.

다음 기능들은 0.9.66 버전 기준으로 구현되지 않았습니다:

- MessageNumbers, Options, 및 Termination 블록
- 프로토콜 계층 응답
- Zero static key
- 멀티캐스트

이 프로토콜의 MLKEM PQ Hybrid 버전은 [ECIES-HYBRID](/docs/specs/ecies-hybrid/)를 참조하세요.

## 개요

이것은 ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/)를 대체하는 새로운 종단 간 암호화 프로토콜입니다.

다음과 같은 이전 작업에 기반합니다:

- Common structures spec [Common](/docs/specs/common-structures/)
- LS2를 포함한 [I2NP](/docs/specs/i2np/) spec
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> 새로운 비대칭 암호화 개요
- 저수준 암호화 개요 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 새로운 netDb 항목들
- 142 새로운 암호화 템플릿
- [Noise](https://noiseprotocol.org/noise.html) 프로토콜
- [Signal](https://signal.org/docs/specifications/doubleratchet/) double ratchet 알고리즘

목적지 간 종단 간 통신을 위한 새로운 암호화를 지원합니다.

이 설계는 Signal의 이중 래칫(double ratchet)을 통합한 Noise 핸드셰이크와 데이터 단계를 사용합니다.

이 명세서에서 Signal과 Noise에 대한 모든 참조는 배경 정보용입니다. 이 명세서를 이해하거나 구현하는 데 Signal과 Noise 프로토콜에 대한 지식은 필요하지 않습니다.

이 사양은 버전 0.9.46부터 지원됩니다.

## 명세서

이 설계는 Signal의 이중 래칫을 통합한 Noise 핸드셰이크와 데이터 단계를 사용합니다.

### 암호화 설계 요약

재설계해야 할 프로토콜의 다섯 가지 부분이 있습니다:

- 1\) 새로운 세션 컨테이너 형식과 기존 세션 컨테이너 형식이 새로운 형식으로 대체됩니다.
- 2\) ElGamal(256바이트 공개 키, 128바이트 개인 키)이 ECIES-X25519(32바이트 공개 및 개인 키)로 대체됩니다.
- 3\) AES가 AEAD_ChaCha20_Poly1305(아래에서는 ChaChaPoly로 줄여서 표기)로 대체됩니다.
- 4\) SessionTags가 본질적으로 암호화된 동기화 PRNG인 ratchet으로 대체됩니다.
- 5\) ElGamal/AES+SessionTags 사양에서 정의된 AES 페이로드가 NTCP2와 유사한 블록 형식으로 대체됩니다.

다섯 가지 변경 사항 각각은 아래에 별도의 섹션으로 구성되어 있습니다.

### 암호화 타입

crypto type (LS2에서 사용)은 4입니다. 이는 little-endian 32바이트 X25519 공개 키와 여기서 명시된 종단간 프로토콜을 나타냅니다.

암호화 타입 0은 ElGamal입니다. 암호화 타입 1-3은 ECIES-ECDH-AES-SessionTag를 위해 예약되어 있으며, 제안서 145 [Prop145](/proposals/145-ecies-ecdh-aes/)를 참조하세요.

### Noise Protocol Framework

이 프로토콜은 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (개정판 34, 2018-07-11)에 기반한 요구사항을 제공합니다. Noise는 [SSU](/docs/transport/ssu/) 프로토콜의 기반이 되는 Station-To-Station 프로토콜 [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol)과 유사한 속성을 가지고 있습니다. Noise 용어로 Alice는 개시자(initiator)이고 Bob은 응답자(responder)입니다.

이 사양은 Noise protocol Noise_IK_25519_ChaChaPoly_SHA256을 기반으로 합니다. (초기 키 파생 함수의 실제 식별자는 I2P 확장을 나타내기 위해 "Noise_IKelg2_25519_ChaChaPoly_SHA256"입니다 - 아래 KDF 1 섹션 참조) 이 Noise protocol은 다음 프리미티브를 사용합니다:

- Interactive Handshake Pattern: IK Alice가 즉시 자신의
  정적 키를 Bob에게 전송 (I) Alice는 이미 Bob의 정적 키를 알고 있음 (K)
- One-Way Handshake Pattern: N Alice가 자신의 정적 키를
  Bob에게 전송하지 않음 (N)
- DH Function: X25519 [RFC-7748](https://tools.ietf.org/html/rfc7748)에서 명시된
  32바이트 키 길이를 가진 X25519 DH.
- Cipher Function: ChaChaPoly [RFC-7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8에서 명시된
  AEAD_CHACHA20_POLY1305. 12바이트 nonce, 처음 4바이트는 0으로 설정.
  [NTCP2](/docs/specs/ntcp2/)와 동일함.
- Hash Function: SHA256 I2P에서 이미 광범위하게 사용되는
  표준 32바이트 해시.

#### 프레임워크에 추가된 기능

이 사양은 Noise_IK_25519_ChaChaPoly_SHA256에 대한 다음과 같은 개선사항을 정의합니다. 이는 일반적으로 [NOISE](https://noiseprotocol.org/noise.html) 섹션 13의 가이드라인을 따릅니다.

1) 평문 임시 키는 다음으로 인코딩됩니다

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) 응답은 평문 태그로 시작됩니다. 3) 페이로드 형식은 메시지 1, 2, 그리고 데이터 단계에 대해 정의됩니다.

    Of course, this is not defined in Noise.

모든 메시지에는 [I2NP](/docs/specs/i2np/) garlic 메시지 헤더가 포함됩니다. 데이터 단계는 Noise 데이터 단계와 유사하지만 호환되지 않는 암호화를 사용합니다.

### 핸드셰이크 패턴

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 ephemeral 키
- s = 정적 키
- p = 메시지 페이로드

일회성 및 언바운드 세션은 Noise N 패턴과 유사합니다.

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
#### 보안 속성

Noise 용어를 사용하여, 설정 및 데이터 시퀀스는 다음과 같습니다: ([Noise](https://noiseprotocol.org/noise.html)의 페이로드 보안 속성)

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### XK와의 차이점

IK 핸드셰이크는 [NTCP2](/docs/specs/ntcp2/)와 [SSU2](/docs/specs/ssu2/)에서 사용되는 XK 핸드셰이크와 몇 가지 차이점이 있습니다.

- XK의 3개와 비교하여 총 4개의 DH 연산
- 첫 번째 메시지에서 발신자 인증: 페이로드가 발신자의 공개 키 소유자에게 속한다고 인증되지만, 키가 손상되었을 수 있음 (Authentication 1) XK는 Alice가 인증되기 전에 또 다른 라운드 트립이 필요함.
- 두 번째 메시지 후 완전한 순방향 비밀성 (Confidentiality 5). Bob은 완전한 순방향 비밀성을 가지고 두 번째 메시지 직후 즉시 페이로드를 보낼 수 있음. XK는 완전한 순방향 비밀성을 위해 또 다른 라운드 트립이 필요함.

요약하면, IK는 완전한 전방향 보안성(forward secrecy)을 가지고 Bob에서 Alice로 응답 페이로드를 1-RTT로 전달할 수 있게 하지만, 요청 페이로드는 전방향 보안성을 갖지 않습니다.

### 세션

ElGamal/AES+SessionTag 프로토콜은 단방향입니다. 이 계층에서 수신자는 메시지가 어디서 왔는지 알 수 없습니다. 아웃바운드와 인바운드 세션은 연결되지 않습니다. 확인응답은 clove 내의 DeliveryStatusMessage(GarlicMessage로 래핑됨)를 사용하여 대역 외에서 처리됩니다.

이 명세에서는 양방향 프로토콜을 생성하는 두 가지 메커니즘인 "페어링"과 "바인딩"을 정의합니다. 이러한 메커니즘들은 향상된 효율성과 보안을 제공합니다.

#### 세션 컨텍스트

ElGamal/AES+SessionTags와 마찬가지로, 모든 인바운드 및 아웃바운드 세션은 주어진 컨텍스트에 있어야 하며, 이는 router의 컨텍스트이거나 특정 로컬 목적지의 컨텍스트입니다. Java I2P에서 이 컨텍스트는 Session Key Manager라고 불립니다.

세션은 컨텍스트 간에 공유되어서는 안 됩니다. 이는 다양한 로컬 목적지 간의 상관관계나 로컬 목적지와 router 간의 상관관계를 허용할 수 있기 때문입니다.

주어진 목적지가 ElGamal/AES+SessionTags와 이 명세서를 모두 지원하는 경우, 두 유형의 세션이 컨텍스트를 공유할 수 있습니다. 아래 섹션 1c)를 참조하세요.

#### 인바운드와 아웃바운드 세션 페어링

발신자(Alice)에서 아웃바운드 세션이 생성될 때, 응답이 예상되지 않는 경우(예: 원시 데이터그램)를 제외하고는 새로운 인바운드 세션이 생성되어 아웃바운드 세션과 쌍을 이룹니다.

새로운 인바운드 세션은 응답이 요청되지 않는 경우(예: 원시 데이터그램)를 제외하고는 항상 새로운 아웃바운드 세션과 쌍을 이룹니다.

응답이 요청되고 원격 목적지 또는 router에 바인딩된 경우, 해당 새로운 아웃바운드 세션이 그 목적지 또는 router에 바인딩되며, 해당 목적지 또는 router에 대한 이전 아웃바운드 세션을 대체합니다.

인바운드와 아웃바운드 세션을 페어링하면 DH 키를 래칫팅할 수 있는 양방향 프로토콜을 제공합니다.

#### 세션과 목적지 바인딩

주어진 목적지나 router에 대해서는 단 하나의 아웃바운드 세션만 존재합니다. 주어진 목적지나 router로부터는 여러 개의 현재 인바운드 세션이 있을 수 있습니다. 일반적으로 새로운 인바운드 세션이 생성되고 해당 세션에서 트래픽이 수신되면(이는 ACK 역할을 함), 다른 세션들은 1분 정도 내에 비교적 빠르게 만료되도록 표시됩니다. 이전에 전송된 메시지(PN) 값이 확인되며, 이전 인바운드 세션에서 수신되지 않은 메시지가 (윈도우 크기 내에서) 없다면, 이전 세션은 즉시 삭제될 수 있습니다.

발신자(Alice)에서 아웃바운드 세션이 생성될 때, 이는 원격 Destination(Bob)에 바인딩되며, 쌍을 이루는 인바운드 세션도 동일한 원격 Destination에 바인딩됩니다. 세션이 래칫(ratchet)될 때도 원격 Destination에 계속 바인딩된 상태를 유지합니다.

수신자(Bob)에서 인바운드 세션이 생성될 때, Alice의 선택에 따라 원격 Destination(Alice)에 바인딩될 수 있습니다. Alice가 New Session 메시지에 바인딩 정보(그녀의 정적 키)를 포함하면, 세션은 해당 destination에 바인딩되고, 아웃바운드 세션이 생성되어 동일한 Destination에 바인딩됩니다. 세션이 ratchet되면서, 계속해서 원격 Destination에 바인딩된 상태를 유지합니다.

#### 바인딩과 페어링의 이점

일반적인 스트리밍 케이스의 경우, Alice와 Bob이 다음과 같이 프로토콜을 사용할 것으로 예상합니다:

- Alice는 새로운 아웃바운드 세션을 새로운 인바운드 세션과 페어링하며, 둘 다 원격 목적지(Bob)에 바인딩됩니다.
- Alice는 바인딩 정보와 서명, 그리고 응답 요청을 Bob에게 보내는 New Session 메시지에 포함시킵니다.
- Bob은 새로운 인바운드 세션을 새로운 아웃바운드 세션과 페어링하며, 둘 다 원격 목적지(Alice)에 바인딩됩니다.
- Bob은 페어링된 세션에서 새로운 DH 키로 ratchet하면서 Alice에게 응답(ack)을 보냅니다.
- Alice는 Bob의 새로운 키로 새로운 아웃바운드 세션으로 ratchet하며, 기존 인바운드 세션과 페어링합니다.

인바운드 세션을 원격 Destination에 바인딩하고, 인바운드 세션을 동일한 Destination에 바인딩된 아웃바운드 세션과 페어링함으로써 두 가지 주요 이점을 얻을 수 있습니다:

1) Bob이 Alice에게 보내는 초기 응답은 ephemeral-ephemeral DH를 사용합니다

2) Alice가 Bob의 응답을 받고 래칫을 수행한 후, Alice에서 Bob으로의 모든 후속 메시지는 ephemeral-ephemeral DH를 사용합니다.

#### 메시지 ACK

ElGamal/AES+SessionTags에서 LeaseSet이 garlic clove로 번들되거나 태그가 전달될 때, 송신 router는 ACK를 요청합니다. 이는 DeliveryStatus 메시지를 포함하는 별도의 garlic clove입니다. 추가 보안을 위해 DeliveryStatus 메시지는 Garlic 메시지로 래핑됩니다. 이 메커니즘은 프로토콜 관점에서 대역 외(out-of-band)입니다.

새로운 프로토콜에서는 인바운드와 아웃바운드 세션이 쌍을 이루므로, 대역 내에서 ACK를 가질 수 있습니다. 별도의 clove가 필요하지 않습니다.

명시적 ACK는 I2NP 블록이 없는 단순한 Existing Session 메시지입니다. 그러나 대부분의 경우 역방향 트래픽이 있기 때문에 명시적 ACK를 피할 수 있습니다. 구현체에서는 명시적 ACK를 보내기 전에 짧은 시간(아마도 100ms 정도)을 대기하여 스트리밍이나 애플리케이션 계층이 응답할 시간을 주는 것이 바람직할 수 있습니다.

구현체들은 또한 I2NP 블록이 처리될 때까지 ACK 전송을 지연시켜야 합니다. 왜냐하면 Garlic Message가 lease set이 포함된 Database Store Message를 담고 있을 수 있기 때문입니다. ACK를 라우팅하려면 최신 lease set이 필요하며, (lease set에 포함된) 원격 목적지는 바인딩 정적 키를 검증하는 데 필요합니다.

#### 세션 타임아웃

아웃바운드 세션은 항상 인바운드 세션보다 먼저 만료되어야 합니다. 아웃바운드 세션이 만료되고 새로운 세션이 생성되면, 새로운 쌍을 이루는 인바운드 세션도 함께 생성됩니다. 기존 인바운드 세션이 있었다면, 그 세션은 만료되도록 허용됩니다.

### 멀티캐스트

미정

### 정의

사용되는 암호화 구성 요소에 해당하는 다음 함수들을 정의합니다.

ZEROLEN

길이가 0인 바이트 배열

CSRNG(n)

암호학적으로 안전한 난수 생성기로부터의 n바이트 출력

    generator.

H(p, d)

개인화 문자열 p와 데이터를 입력받는 SHA-256 해시 함수

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

이전 해시 h와 새로운 데이터 d를 받는 SHA-256 해시 함수,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

에 명시된 ChaCha20/Poly1305 AEAD

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

X25519 공개키 합의 시스템. 32바이트의 개인키, 공개키

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

일부 입력 키를 받는 암호화 키 유도 함수

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

이전 chainKey와 새로운 데이터 d와 함께 HKDF()를 사용하고, 새로운

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) 메시지 형식

#### 현재 메시지 형식 검토

[I2NP](/docs/specs/i2np/)에 명시된 garlic 메시지는 다음과 같습니다. 중간 hop들이 새로운 암호화와 기존 암호화를 구별할 수 없도록 하는 것이 설계 목표이므로, 길이 필드가 중복되더라도 이 형식은 변경될 수 없습니다. 형식은 전체 16바이트 헤더로 표시되지만, 사용된 전송 방식에 따라 실제 헤더는 다른 형식일 수 있습니다.

복호화된 데이터는 일련의 Garlic Clove들과 추가 데이터를 포함하며, 이를 Clove Set이라고도 합니다.

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
#### 암호화된 데이터 형식 검토

ElGamal/AES+SessionTags에서는 두 가지 메시지 형식이 있습니다:

1\) 새 세션: - 514바이트 ElGamal 블록 - AES 블록 (최소 128바이트, 16의 배수)

2\) 기존 세션: - 32바이트 Session Tag - AES 블록 (최소 128바이트, 16의 배수)

이러한 메시지들은 길이 필드를 포함하는 I2NP garlic 메시지에 캡슐화되므로 길이를 알 수 있습니다.

수신자는 먼저 처음 32바이트를 Session Tag로 조회를 시도합니다. 찾으면 AES 블록을 복호화합니다. 찾지 못하고 데이터 길이가 최소 (514+16) 이상이면 ElGamal 블록 복호화를 시도하고, 성공하면 AES 블록을 복호화합니다.

#### 새로운 세션 태그와 Signal과의 비교

Signal Double Ratchet에서 헤더는 다음을 포함합니다:

- DH: 현재 ratchet 공개 키
- PN: 이전 체인 메시지 길이
- N: 메시지 번호

Signal의 "sending chains"는 우리의 태그 세트와 대략적으로 동등합니다. 세션 태그를 사용함으로써 우리는 그 대부분을 제거할 수 있습니다.

새 세션에서는 암호화되지 않은 헤더에 공개 키만 넣습니다.

기존 세션에서는 헤더에 세션 태그를 사용합니다. 세션 태그는 현재 ratchet 공개 키 및 메시지 번호와 연결됩니다.

새 세션과 기존 세션 모두에서 PN과 N은 암호화된 본문에 있습니다.

Signal에서는 모든 것이 지속적으로 래칫됩니다. 새로운 DH 공개키는 수신자가 래칫하고 새로운 공개키를 다시 보내도록 요구하며, 이는 수신된 공개키에 대한 ack 역할도 합니다. 이는 우리에게는 너무 많은 DH 연산이 될 것입니다. 따라서 우리는 수신된 키의 ack와 새로운 공개키의 전송을 분리합니다. 새로운 DH 공개키로부터 생성된 session tag를 사용하는 모든 메시지는 ACK를 구성합니다. 우리는 재키잉을 원할 때만 새로운 공개키를 전송합니다.

DH가 ratchet해야 하는 최대 메시지 수는 65535개입니다.

세션 키를 전달할 때, 세션 태그도 함께 전달해야 하는 대신 세션 키로부터 "Tag Set"을 도출합니다. Tag Set은 최대 65536개의 태그를 포함할 수 있습니다. 그러나 수신자는 가능한 모든 태그를 한 번에 생성하기보다는 "미리 보기" 전략을 구현해야 합니다. 마지막으로 수신된 유효한 태그 이후 최대 N개의 태그만 생성하세요. N은 최대 128개일 수 있지만, 32개 또는 그보다 적은 수가 더 나은 선택일 수 있습니다.

### 1a) 새로운 세션 형식

새 세션 일회용 공개 키 (32바이트) 암호화된 데이터 및 MAC (나머지 바이트)

New Session 메시지는 발신자의 정적 공개 키를 포함할 수도 있고 포함하지 않을 수도 있습니다. 포함된 경우, 역방향 세션은 해당 키에 바인딩됩니다. 응답이 예상되는 경우, 즉 스트리밍 및 응답 가능한 데이터그램의 경우 정적 키가 포함되어야 합니다. 원시 데이터그램의 경우에는 포함되지 않아야 합니다.

New Session 메시지는 단방향 Noise [NOISE](https://noiseprotocol.org/noise.html) 패턴 "N"(정적 키가 전송되지 않는 경우) 또는 양방향 패턴 "IK"(정적 키가 전송되는 경우)와 유사합니다.

### 1b) 새로운 세션 형식 (바인딩 포함)

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
#### 새 세션 임시 키

임시 키는 32바이트이며, Elligator2로 인코딩됩니다. 이 키는 절대 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

#### 정적 키

복호화되었을 때, Alice의 X25519 정적 키, 32바이트.

#### 페이로드

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16바이트 적습니다. 페이로드는 반드시 DateTime 블록을 포함해야 하며, 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식과 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 1c) 새로운 세션 형식 (바인딩 없음)

응답이 필요하지 않은 경우, 정적 키는 전송되지 않습니다.

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
#### 새 세션 임시 키

Alice의 임시 키. 임시 키는 32바이트이며, Elligator2로 인코딩되고 리틀 엔디안 형식입니다. 이 키는 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

#### 플래그 섹션 복호화된 데이터

Flags 섹션은 아무것도 포함하지 않습니다. 바인딩이 있는 New Session 메시지의 정적 키와 동일한 길이여야 하므로 항상 32바이트입니다. Bob은 32바이트가 모두 0인지 테스트하여 정적 키인지 flags 섹션인지 판단합니다.

TODO 여기에 필요한 플래그가 있나요?

#### 페이로드

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16바이트 적습니다. 페이로드는 반드시 DateTime 블록을 포함해야 하며, 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식과 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 1d) 일회성 형식 (바인딩이나 세션 없음)

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
#### 새 세션 일회용 키

일회용 키는 32바이트이며, Elligator2로 인코딩되고 리틀 엔디안 형식입니다. 이 키는 절대 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

#### 플래그 섹션 복호화된 데이터

Flags 섹션은 아무것도 포함하지 않습니다. 바인딩이 있는 New Session 메시지의 정적 키와 동일한 길이여야 하므로 항상 32바이트입니다. Bob은 32바이트가 모두 0인지 테스트하여 정적 키인지 flags 섹션인지 판단합니다.

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
#### 페이로드

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 작습니다. 페이로드는 DateTime 블록을 포함해야 하며 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식 및 추가 요구사항은 아래 페이로드 섹션을 참조하세요.

### 1f) 새 세션 메시지를 위한 KDF들

#### 초기 ChainKey를 위한 KDF

이것은 수정된 프로토콜 이름을 가진 IK용 표준 [NOISE](https://noiseprotocol.org/noise.html)입니다. IK 패턴(바운드 세션)과 N 패턴(언바운드 세션) 모두에 동일한 초기화자를 사용한다는 점에 주목하세요.

프로토콜 이름이 수정된 이유는 두 가지입니다. 첫째, ephemeral key들이 Elligator2로 인코딩되었음을 나타내기 위해서이고, 둘째, 태그 값을 혼합하기 위해 두 번째 메시지 전에 MixHash()가 호출됨을 나타내기 위해서입니다.

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
#### 플래그/정적 키 섹션 암호화 콘텐츠용 KDF

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
#### 페이로드 섹션을 위한 KDF (Alice 정적 키 포함)

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
#### 페이로드 섹션용 KDF (Alice 정적 키 제외)

이는 Noise "N" 패턴이지만, bound 세션과 동일한 "IK" 초기화자를 사용한다는 점에 유의하세요.

New Session 메시지는 정적 키가 복호화되고 모든 값이 0인지 확인하기 위해 검사되기 전까지는 Alice의 정적 키를 포함하고 있는지 여부를 식별할 수 없습니다. 따라서 수신자는 모든 New Session 메시지에 대해 "IK" 상태 머신을 사용해야 합니다. 정적 키가 모두 0인 경우 "ss" 메시지 패턴을 건너뛰어야 합니다.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) 새로운 세션 응답 형식

하나 이상의 New Session Reply가 단일 New Session 메시지에 대한 응답으로 전송될 수 있습니다. 각 응답에는 세션의 TagSet에서 생성된 태그가 앞에 붙습니다.

New Session Reply는 두 부분으로 구성됩니다. 첫 번째 부분은 앞에 태그가 붙은 Noise IK 핸드셰이크의 완료입니다. 첫 번째 부분의 길이는 56바이트입니다. 두 번째 부분은 데이터 단계 페이로드입니다. 두 번째 부분의 길이는 16 + 페이로드 길이입니다.

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
#### 세션 태그

태그는 아래 DH 초기화 KDF에서 초기화된 Session Tags KDF에서 생성됩니다. 이는 응답을 세션과 연관시킵니다. DH 초기화의 Session Key는 사용되지 않습니다.

#### 새 세션 응답 임시 키

Bob의 임시 키입니다. 임시 키는 32바이트이며, Elligator2로 인코딩되고 리틀 엔디안 방식을 사용합니다. 이 키는 재사용되지 않으며, 재전송을 포함하여 각 메시지마다 새로운 키가 생성됩니다.

#### 페이로드

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 바이트 적습니다. 페이로드는 일반적으로 하나 이상의 Garlic Clove 블록을 포함합니다. 형식 및 추가 요구사항은 아래 페이로드 섹션을 참조하십시오.

#### Reply TagSet을 위한 KDF

하나 이상의 태그가 TagSet에서 생성되며, 이는 New Session 메시지의 chainKey를 사용하여 아래 KDF로 초기화됩니다.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### Reply Key Section 암호화된 콘텐츠를 위한 KDF

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
#### 페이로드 섹션 암호화된 콘텐츠를 위한 KDF

이것은 분할 후 첫 번째 Existing Session 메시지와 유사하지만, 별도의 태그가 없습니다. 또한 위의 해시를 사용하여 페이로드를 NSR 메시지에 바인딩합니다.

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
### 참고 사항

응답의 크기에 따라 각각 고유한 임시 키를 가진 여러 NSR 메시지가 응답으로 전송될 수 있습니다.

Alice와 Bob은 모든 NS 및 NSR 메시지에 대해 새로운 임시 키를 사용해야 합니다.

Alice는 Existing Session (ES) 메시지를 보내기 전에 Bob의 NSR 메시지 중 하나를 받아야 하며, Bob은 ES 메시지를 보내기 전에 Alice로부터 ES 메시지를 받아야 합니다.

Bob의 NSR Payload Section에서 가져온 `chainKey`와 `k`는 초기 ES DH Ratchets(양방향, DH Ratchet KDF 참조)의 입력값으로 사용됩니다.

Bob은 Alice로부터 받은 ES 메시지에 대해서만 기존 세션을 유지해야 합니다. 다른 생성된 인바운드 및 아웃바운드 세션들(여러 NSR에 대한)은 주어진 세션에 대해 Alice의 첫 번째 ES 메시지를 받은 후 즉시 소멸되어야 합니다.

### 1h) 기존 세션 형식

세션 태그 (8바이트) 암호화된 데이터 및 MAC (아래 3절 참조)

#### 형식

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
#### 페이로드

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16바이트 적습니다. 형식과 요구사항은 아래 페이로드 섹션을 참조하세요.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

형식: 32바이트 공개 키 및 개인 키, 리틀 엔디안.

### 2a) Elligator2

표준 Noise 핸드셰이크에서 각 방향의 초기 핸드셰이크 메시지는 평문으로 전송되는 임시 키로 시작됩니다. 유효한 X25519 키는 무작위 데이터와 구별 가능하기 때문에, 중간자 공격자는 이러한 메시지를 무작위 세션 태그로 시작하는 기존 세션 메시지와 구별할 수 있습니다. [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/))에서는 키를 난독화하기 위해 대역 외 정적 키를 사용한 저비용 XOR 함수를 사용했습니다. 하지만 여기서의 위협 모델은 다릅니다. 우리는 중간자 공격자가 어떤 수단을 사용하든 트래픽의 목적지를 확인하거나 초기 핸드셰이크 메시지를 기존 세션 메시지와 구별하는 것을 허용하고 싶지 않습니다.

따라서 [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)를 사용하여 New Session 및 New Session Reply 메시지의 임시 키를 변환하여 균등한 랜덤 문자열과 구별할 수 없도록 합니다.

#### 형식

32바이트 공개 키와 개인 키. 인코딩된 키는 리틀 엔디언입니다.

[Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)에서 정의된 바와 같이, 인코딩된 키들은 254개의 랜덤 비트와 구별할 수 없습니다. 우리는 256개의 랜덤 비트(32바이트)가 필요합니다. 따라서 인코딩과 디코딩은 다음과 같이 정의됩니다:

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
#### 참고사항

Elligator2는 평균 키 생성 시간을 두 배로 늘립니다. 개인 키의 절반이 Elligator2로 인코딩하기에 적합하지 않은 공개 키를 생성하기 때문입니다. 또한 적합한 키 쌍을 찾을 때까지 생성기가 계속 재시도해야 하므로, 키 생성 시간은 지수 분포를 따르며 상한이 없습니다.

이러한 오버헤드는 적절한 키들의 풀을 유지하기 위해 별도의 스레드에서 키 생성을 미리 수행함으로써 관리할 수 있습니다.

생성기는 적합성을 결정하기 위해 ENCODE_ELG2() 함수를 수행합니다. 따라서 생성기는 다시 계산할 필요가 없도록 ENCODE_ELG2()의 결과를 저장해야 합니다.

또한, 부적합한 키들은 Elligator2가 사용되지 않는 [NTCP2](/docs/specs/ntcp2/)에 사용되는 키 풀에 추가될 수 있습니다. 이렇게 하는 것의 보안 문제는 아직 결정되지 않았습니다.

### 3) AEAD (ChaChaPoly)

ChaCha20과 Poly1305를 사용하는 AEAD는 [NTCP2](/docs/specs/ntcp2/)와 동일합니다. 이는 [RFC-7539](https://tools.ietf.org/html/rfc7539)에 해당하며, TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)에서도 유사하게 사용됩니다.

#### 새 세션 및 새 세션 응답 입력

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
#### 기존 세션 입력

기존 세션 메시지에서 AEAD 블록의 암호화/복호화 함수에 대한 입력:

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
#### 암호화된 형식

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
#### 참고사항

- ChaCha20은 스트림 암호이므로 평문을 패딩할 필요가 없습니다.
  추가 키스트림 바이트는 버려집니다.
- 암호를 위한 키(256비트)는 SHA256 KDF를 통해 합의됩니다. 
  각 메시지에 대한 KDF의 세부사항은 아래 별도 섹션에서 다룹니다.
- ChaChaPoly 프레임은 I2NP 데이터 메시지에 캡슐화되므로 
  크기가 알려져 있습니다.
- 모든 메시지에서 패딩은 인증된 데이터 프레임 내부에 있습니다.

#### AEAD 오류 처리

AEAD 검증에 실패한 모든 수신 데이터는 폐기되어야 합니다. 응답이 반환되지 않습니다.

### 4) Ratchets

우리는 이전과 같이 세션 태그를 여전히 사용하지만, 래칫을 사용하여 생성합니다. 세션 태그에는 우리가 구현하지 않은 재키 옵션도 있었습니다. 따라서 이중 래칫과 같지만 두 번째 것은 수행하지 않았습니다.

여기서는 Signal의 Double Ratchet과 유사한 것을 정의합니다. 세션 태그는 수신자와 송신자 측에서 결정론적으로 동일하게 생성됩니다.

대칭 키/태그 래칫을 사용함으로써 송신자 측에서 세션 태그를 저장하는 메모리 사용량을 제거합니다. 또한 태그 세트 전송으로 인한 대역폭 소비도 제거합니다. 수신자 측 사용량은 여전히 상당하지만, 세션 태그를 32바이트에서 8바이트로 축소하여 추가로 줄일 수 있습니다.

Signal에서 명시된(그리고 선택적인) 헤더 암호화는 사용하지 않고, 대신 세션 태그를 사용합니다.

DH ratchet을 사용함으로써 우리는 전진 보안성(forward secrecy)을 달성하며, 이는 ElGamal/AES+SessionTags에서는 구현되지 않았던 기능입니다.

참고: New Session 일회용 공개 키는 ratchet의 일부가 아니며, 그 유일한 기능은 Alice의 초기 DH ratchet 키를 암호화하는 것입니다.

#### 메시지 번호

Double Ratchet은 각 메시지 헤더에 태그를 포함시켜 분실되거나 순서가 바뀐 메시지를 처리합니다. 수신자는 태그의 인덱스를 조회하여 메시지 번호 N을 확인합니다. 메시지에 PN 값이 있는 Message Number 블록이 포함된 경우, 수신자는 이전 태그 세트에서 해당 값보다 높은 태그들을 삭제할 수 있으며, 건너뛴 메시지들이 나중에 도착할 경우를 대비해 이전 태그 세트에서 건너뛴 태그들은 보관합니다.

#### 샘플 구현

이러한 래칫을 구현하기 위해 다음 데이터 구조와 함수들을 정의합니다.

TAGSET_ENTRY

TAGSET의 단일 항목입니다.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

TAGSET_ENTRIES의 모음입니다.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets이지만 Signal만큼 빠르지는 않습니다. 우리는 수신된 키의 확인응답과 새로운 키 생성을 분리합니다. 일반적인 사용에서 Alice와 Bob은 각각 New Session에서 즉시 ratchet을 (두 번) 수행하지만, 다시는 ratchet을 수행하지 않습니다.

ratchet은 단일 방향용이며, 해당 방향에 대한 New Session tag / message key ratchet 체인을 생성한다는 점에 주의하세요. 양방향에 대한 키를 생성하려면 두 번 ratchet해야 합니다.

새로운 키를 생성하고 전송할 때마다 ratchet합니다. 새로운 키를 받을 때마다 ratchet합니다.

Alice는 바인딩되지 않은 아웃바운드 세션을 생성할 때 한 번 래칫하며, 인바운드 세션은 생성하지 않습니다(바인딩되지 않은 세션은 응답할 수 없음).

Bob은 바인딩되지 않은 인바운드 세션을 생성할 때 한 번 래칫(ratchet)하며, 해당하는 아웃바운드 세션은 생성하지 않습니다(바인딩되지 않은 세션은 응답할 수 없음).

Alice는 Bob의 New Session Reply (NSR) 메시지 중 하나를 받을 때까지 계속해서 New Session (NS) 메시지를 Bob에게 보냅니다. 그런 다음 그녀는 NSR의 Payload Section KDF 결과를 세션 래칫의 입력으로 사용하고(DH Ratchet KDF 참조), Existing Session (ES) 메시지를 보내기 시작합니다.

수신된 각 NS 메시지에 대해, Bob은 새로운 인바운드 세션을 생성하며, 응답 Payload Section의 KDF 결과를 새로운 인바운드 및 아웃바운드 ES DH Ratchet의 입력으로 사용합니다.

필요한 각 응답에 대해, Bob은 페이로드에 응답을 담은 NSR 메시지를 Alice에게 보냅니다. Bob은 모든 NSR에 대해 새로운 임시 키를 사용해야 합니다.

Bob은 해당하는 아웃바운드 세션에서 ES 메시지를 생성하고 전송하기 전에, 인바운드 세션 중 하나에서 Alice로부터 ES 메시지를 받아야 합니다.

Alice는 Bob으로부터 NSR 메시지를 수신하기 위해 타이머를 사용해야 합니다. 타이머가 만료되면 세션이 제거되어야 합니다.

KCI 및/또는 리소스 고갈 공격을 방지하기 위해, 공격자가 Alice가 NS 메시지를 계속 보내도록 Bob의 NSR 응답을 드롭하는 상황에서, Alice는 타이머 만료로 인한 특정 횟수의 재시도 후에 Bob에 대한 새로운 세션 시작을 피해야 합니다.

Alice와 Bob은 각각 수신된 모든 NextKey 블록에 대해 DH ratchet을 수행합니다.

Alice와 Bob은 각 DH ratchet 후에 새로운 태그 세트와 두 개의 대칭 키 ratchet을 생성합니다. 주어진 방향에서 각각의 새로운 ES 메시지에 대해 Alice와 Bob은 세션 태그와 대칭 키 ratchet을 진행시킵니다.

초기 핸드셰이크 이후 DH ratchet의 빈도는 구현에 따라 달라집니다. 프로토콜에서는 ratchet이 필요하기 전에 65535개 메시지라는 제한을 두고 있지만, 더 빈번한 ratcheting(메시지 수, 경과 시간 또는 둘 다를 기반으로)은 추가적인 보안을 제공할 수 있습니다.

바인딩된 세션에서 최종 핸드셰이크 KDF 이후, Bob과 Alice는 결과 CipherState에서 Noise Split() 함수를 실행하여 인바운드 및 아웃바운드 세션에 대한 독립적인 대칭 키와 태그 체인 키를 생성해야 합니다.

##### 키 및 태그 세트 ID

키와 태그 세트 ID 번호는 키와 태그 세트를 식별하는 데 사용됩니다. 키 ID는 NextKey 블록에서 전송되거나 사용된 키를 식별하는 데 사용됩니다. 태그 세트 ID는 ACK 블록에서 (메시지 번호와 함께) 승인되는 메시지를 식별하는 데 사용됩니다. 키와 태그 세트 ID 모두 단일 방향의 태그 세트에 적용됩니다. 키와 태그 세트 ID 번호는 순차적이어야 합니다.

각 방향에서 세션에 사용되는 첫 번째 태그 세트에서 태그 세트 ID는 0입니다. NextKey 블록이 전송되지 않았으므로 키 ID가 없습니다.

DH ratchet을 시작하기 위해, 송신자는 키 ID가 0인 새로운 NextKey 블록을 전송합니다. 수신자는 키 ID가 0인 새로운 NextKey 블록으로 응답합니다. 그러면 송신자는 태그 세트 ID가 1인 새로운 태그 세트를 사용하기 시작합니다.

후속 태그 세트들도 유사하게 생성됩니다. NextKey 교환 후 사용되는 모든 태그 세트의 경우, 태그 세트 번호는 (1 + Alice의 키 ID + Bob의 키 ID)입니다.

키와 태그 세트 ID는 0에서 시작하여 순차적으로 증가합니다. 최대 태그 세트 ID는 65535입니다. 최대 키 ID는 32767입니다. 태그 세트가 거의 소진될 때, 태그 세트 발신자는 NextKey 교환을 시작해야 합니다. 태그 세트 65535가 거의 소진될 때, 태그 세트 발신자는 New Session 메시지를 전송하여 새로운 세션을 시작해야 합니다.

스트리밍 최대 메시지 크기가 1730이고 재전송이 없다고 가정할 때, 단일 태그 세트를 사용한 이론적 최대 데이터 전송량은 1730 * 65536 ~= 108 MB입니다. 실제 최대값은 재전송으로 인해 더 낮아집니다.

사용 가능한 모든 65536개의 태그 세트를 사용한 이론적 최대 데이터 전송량은 세션을 폐기하고 교체해야 하기 전까지 64K * 108 MB ~= 6.9 TB입니다.

##### DH RATCHET 메시지 플로우

태그 세트에 대한 다음 키 교환은 해당 태그의 발신자(아웃바운드 태그 세트의 소유자)가 시작해야 합니다. 수신자(인바운드 태그 세트의 소유자)가 응답합니다. 애플리케이션 계층에서 일반적인 HTTP GET 트래픽의 경우, Bob이 더 많은 메시지를 보내고 키 교환을 시작하여 먼저 래칫(ratchet)을 수행합니다. 아래 다이어그램이 이를 보여줍니다. Alice가 래칫을 수행할 때는 동일한 일이 반대로 발생합니다.

NS/NSR 핸드셰이크 이후에 사용되는 첫 번째 태그 세트는 태그 세트 0입니다. 태그 세트 0이 거의 소진되면, 태그 세트 1을 생성하기 위해 양방향으로 새로운 키를 교환해야 합니다. 그 이후에는 새로운 키가 한 방향으로만 전송됩니다.

태그 세트 2를 생성하기 위해, 태그 송신자는 새로운 키를 전송하고 태그 수신자는 승인으로 자신의 이전 키 ID를 전송합니다. 양측 모두 DH를 수행합니다.

태그 세트 3을 생성하기 위해, 태그 발신자는 자신의 이전 키 ID를 보내고 태그 수신자에게 새 키를 요청합니다. 양쪽 모두 DH를 수행합니다.

후속 태그 세트는 태그 세트 2와 3과 동일한 방식으로 생성됩니다. 태그 세트 번호는 (1 + 발신자 키 ID + 수신자 키 ID)입니다.

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
아웃바운드 tagset에 대한 DH ratchet이 완료되고 새로운 아웃바운드 tagset이 생성된 후에는 즉시 사용되어야 하며, 기존 아웃바운드 tagset은 삭제될 수 있습니다.

인바운드 tagset에 대한 DH ratchet이 완료되고 새로운 인바운드 tagset이 생성된 후, 수신자는 두 tagset 모두에서 태그를 수신 대기해야 하며, 약 3분 정도의 짧은 시간 후에 이전 tagset을 삭제해야 합니다.

태그 세트와 키 ID 진행의 요약은 아래 표에 있습니다. *는 새로운 키가 생성됨을 나타냅니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
키와 태그 세트 ID 번호는 순차적이어야 합니다.

##### DH 초기화 KDF

이것은 단일 방향에 대한 DH_INITIALIZE(rootKey, k)의 정의입니다. 이는 tagset과 필요한 경우 후속 DH ratchet에 사용될 "다음 루트 키"를 생성합니다.

우리는 세 곳에서 DH 초기화를 사용합니다. 첫째, New Session Replies를 위한 태그 세트를 생성하는 데 사용합니다. 둘째, Existing Session 메시지에서 사용할 각 방향별로 하나씩 두 개의 태그 세트를 생성하는 데 사용합니다. 마지막으로, DH Ratchet 후에 추가적인 Existing Session 메시지를 위해 단일 방향으로 새로운 태그 세트를 생성하는 데 사용합니다.

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
##### DH RATCHET KDF

이는 tagset이 소진되기 전에 NextKey 블록에서 새로운 DH 키가 교환된 후에 사용됩니다.

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
#### 4b) Session Tag Ratchet

Signal에서와 같이 모든 메시지에 대한 래칫. 세션 태그 래칫은 대칭 키 래칫과 동기화되지만, 수신자 키 래칫은 메모리를 절약하기 위해 "뒤처질" 수 있습니다.

송신자는 전송되는 각 메시지마다 한 번씩 래칫을 수행합니다. 추가 태그를 저장할 필요는 없습니다. 송신자는 또한 현재 체인에서 메시지의 메시지 번호인 'N'에 대한 카운터를 유지해야 합니다. 'N' 값은 전송되는 메시지에 포함됩니다. 메시지 번호 블록 정의를 참조하세요.

수신자는 최대 윈도우 크기만큼 ratchet을 앞으로 진행하고 세션과 연관된 "tag set"에 태그를 저장해야 합니다. 수신되면 저장된 태그는 폐기될 수 있으며, 이전에 수신되지 않은 태그가 없다면 윈도우를 앞으로 이동시킬 수 있습니다. 수신자는 각 세션 태그와 연관된 'N' 값을 유지해야 하며, 전송된 메시지의 번호가 이 값과 일치하는지 확인해야 합니다. Message Number 블록 정의를 참조하세요.

##### KDF

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
#### 4c) 대칭 키 래칫

Signal에서와 같이 모든 메시지에 대한 래칫. 각 대칭 키는 연관된 메시지 번호와 세션 태그를 가집니다. 세션 키 래칫은 대칭 태그 래칫과 동기화되지만, 수신자 키 래칫은 메모리 절약을 위해 "뒤처질" 수 있습니다.

전송기는 전송되는 각 메시지마다 한 번씩 래칫됩니다. 추가 키를 저장할 필요가 없습니다.

수신자가 session tag를 받으면, 아직 연관된 키까지 대칭 키 ratchet을 앞으로 진행하지 않았다면, 연관된 키에 "따라잡기"를 해야 합니다. 수신자는 아직 수신되지 않은 이전 tag들에 대한 키들을 캐시할 것입니다. 수신되면, 저장된 키는 폐기될 수 있으며, 이전에 수신되지 않은 tag가 없다면 윈도우를 앞으로 이동할 수 있습니다.

효율성을 위해 session tag와 대칭 키 래칫(ratchet)은 분리되어 있어서 session tag 래칫이 대칭 키 래칫보다 앞서 실행될 수 있습니다. 이는 session tag가 네트워크를 통해 전송되므로 추가적인 보안도 제공합니다.

##### KDF

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
### 5) 페이로드

이것은 ElGamal/AES+SessionTags 명세에서 정의된 AES 섹션 형식을 대체합니다.

이것은 [NTCP2](/docs/specs/ntcp2/) 명세에서 정의된 것과 동일한 블록 형식을 사용합니다. 개별 블록 유형은 다르게 정의됩니다.

구현자들에게 코드 공유를 권장하는 것이 파싱 문제로 이어질 수 있다는 우려가 있습니다. 구현자들은 코드 공유의 이점과 위험을 신중히 고려해야 하며, 두 컨텍스트에서 순서 및 유효한 블록 규칙이 다르다는 것을 확인해야 합니다.

#### 페이로드 섹션 복호화된 데이터

암호화된 길이는 데이터의 나머지 부분입니다. 복호화된 길이는 암호화된 길이보다 16 바이트 적습니다. 모든 블록 타입이 지원됩니다. 일반적인 내용에는 다음 블록들이 포함됩니다:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### 암호화되지 않은 데이터

암호화된 프레임에는 0개 이상의 블록이 있습니다. 각 블록은 1바이트 식별자, 2바이트 길이, 그리고 0바이트 이상의 데이터를 포함합니다.

확장성을 위해 수신자는 알려지지 않은 타입 번호를 가진 블록을 무시해야 하며(MUST), 이를 패딩으로 처리해야 합니다.

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
#### 블록 순서 규칙

New Session 메시지에서 DateTime 블록은 필수이며, 첫 번째 블록이어야 합니다.

기타 허용된 블록:

- Garlic Clove (타입 11)
- Options (타입 5)
- Padding (타입 254)

New Session Reply 메시지에서는 블록이 필요하지 않습니다.

기타 허용된 블록:

- Garlic Clove (type 11)
- 옵션 (type 5)
- 패딩 (type 254)

다른 블록은 허용되지 않습니다. 패딩이 있는 경우 마지막 블록이어야 합니다.

Existing Session 메시지에서는 블록이 필수가 아니며, 다음 요구사항을 제외하고는 순서가 지정되지 않습니다:

Termination이 있는 경우, Padding을 제외하고 마지막 블록이어야 합니다. Padding이 있는 경우, 마지막 블록이어야 합니다.

단일 프레임에는 여러 개의 Garlic Clove 블록이 있을 수 있습니다. 단일 프레임에는 최대 두 개의 Next Key 블록이 있을 수 있습니다. 단일 프레임에는 여러 개의 Padding 블록이 허용되지 않습니다. 다른 블록 유형은 단일 프레임에 여러 블록을 가질 가능성은 낮지만, 금지되지는 않습니다.

#### DateTime

만료 시간. 재생 공격 방지를 돕습니다. Bob은 이 타임스탬프를 사용하여 메시지가 최신인지 검증해야 합니다. 시간이 유효한 경우, Bob은 재생 공격을 방지하기 위해 Bloom filter나 다른 메커니즘을 구현해야 합니다. Bob은 또한 복호화 전에 최근 중복된 NS 메시지를 탐지하고 삭제하기 위해 중복된 임시 키(Elligator2 디코딩 전후 모두)에 대한 이전 재생 탐지 검사를 사용할 수도 있습니다. 일반적으로 New Session 메시지에만 포함됩니다.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

[I2NP](/docs/specs/i2np/)에서 명시된 단일 복호화된 Garlic Clove로, 사용되지 않거나 중복되는 필드들을 제거하도록 수정되었습니다. 경고: 이 형식은 ElGamal/AES용 형식과 상당히 다릅니다. 각 clove는 별도의 페이로드 블록입니다. Garlic Clove는 블록 간이나 ChaChaPoly 프레임 간에 분할될 수 없습니다.

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
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
참고사항:

- 구현자들은 블록을 읽을 때, 잘못된 형식이거나 악의적인 데이터가 다음 블록으로의 읽기 오버런을 일으키지 않도록 보장해야 합니다.
- [I2NP](/docs/specs/i2np/)에서 지정된 Clove Set 형식은 사용되지 않습니다. 각 clove는 자체 블록에 포함됩니다.
- I2NP 메시지 헤더는 9바이트이며, [NTCP2](/docs/specs/ntcp2/)에서 사용되는 것과 동일한 형식입니다.
- [I2NP](/docs/specs/i2np/)의 Garlic Message 정의에서 Certificate, Message ID, Expiration은 포함되지 않습니다.
- [I2NP](/docs/specs/i2np/)의 Garlic Clove 정의에서 Certificate, Clove ID, Expiration은 포함되지 않습니다.

#### 종료

구현은 선택 사항입니다. 세션을 드롭합니다. 이것은 프레임에서 패딩이 아닌 마지막 블록이어야 합니다. 이 세션에서는 더 이상 메시지가 전송되지 않습니다.

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
#### 옵션

구현되지 않음, 추가 연구 필요. 업데이트된 옵션을 전달합니다. 옵션에는 세션에 대한 다양한 매개변수가 포함됩니다. 자세한 내용은 아래 Session Tag Length Analysis 섹션을 참조하세요.

옵션 블록은 more_options가 존재할 수 있기 때문에 가변 길이일 수 있습니다.

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
SOTW는 수신자의 인바운드 태그 윈도우(최대 선행 처리 범위)에 대한 발신자의 권장 사항입니다. RITW는 발신자가 사용할 계획인 인바운드 태그 윈도우(최대 선행 처리 범위)에 대한 발신자의 선언입니다. 그런 다음 각 측은 최소값, 최대값 또는 기타 계산을 기반으로 선행 처리 범위를 설정하거나 조정합니다.

참고사항:

- 기본이 아닌 세션 태그 길이에 대한 지원은 hopefully 필요하지 않을 것입니다.
- 태그 윈도우는 Signal 문서에서 MAX_SKIP입니다.

문제:

- 옵션 협상은 미정입니다.
- 기본값은 미정입니다.
- 패딩 및 지연 옵션은 NTCP2에서 복사되었지만, 해당 옵션들은 아직 완전히 구현되거나 연구되지 않았습니다.

#### 메시지 번호

구현은 선택적입니다. 이전 태그 세트의 길이(전송된 메시지 수) (PN). 수신자는 이전 태그 세트에서 PN보다 높은 태그를 즉시 삭제할 수 있습니다. 수신자는 짧은 시간(예: 2분) 후에 이전 태그 세트에서 PN보다 작거나 같은 태그를 만료시킬 수 있습니다.

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
참고 사항:

- 최대 PN은 65535입니다.
- PN의 정의는 Signal의 정의와 같지만 1을 뺀 값입니다.
  이는 Signal에서 하는 것과 유사하지만, Signal에서는 PN과 N이
  헤더에 있습니다. 여기서는 암호화된 메시지 본문에 있습니다.
- 이전 태그 세트가 없었기 때문에 태그 세트 0에서는 이 블록을 전송하지 마십시오.

#### 다음 DH Ratchet 공개 키

다음 DH ratchet 키는 페이로드에 있으며, 선택사항입니다. 매번 ratchet하지는 않습니다. (이는 헤더에 있고 매번 전송되는 Signal과는 다릅니다)

첫 번째 래칫의 경우, Key ID = 0입니다.

NS 또는 NSR에서는 허용되지 않습니다. 기존 세션 메시지에서만 포함됩니다.

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

- Key ID는 해당 태그 세트에 사용되는 로컬 키의 증분 카운터로, 0부터 시작합니다.
- ID는 키가 변경되지 않는 한 변경되어서는 안 됩니다.
- 엄격히 필요한 것은 아닐 수 있지만, 디버깅에 유용합니다.
  Signal은 key ID를 사용하지 않습니다.
- 최대 Key ID는 32767입니다.
- 양방향의 태그 세트가 동시에 ratcheting하는 드문 경우에는, 프레임에 두 개의 Next Key 블록이 포함됩니다. 하나는 순방향 키용이고 하나는 역방향 키용입니다.
- 키와 태그 세트 ID 번호는 순차적이어야 합니다.
- 자세한 내용은 위의 DH Ratchet 섹션을 참조하십시오.

#### 확인

이것은 ack 요청 블록이 수신된 경우에만 전송됩니다. 여러 메시지를 ack하기 위해 여러 ack가 존재할 수 있습니다.

NS나 NSR에서는 허용되지 않습니다. 기존 세션 메시지에만 포함됩니다.

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

- tag set ID와 N이 확인응답되는 메시지를 고유하게 식별합니다.
- 각 방향의 세션에서 사용되는 첫 번째 tag set에서는 tag set ID가 0입니다.
- NextKey 블록이 전송되지 않았으므로 key ID가 없습니다.
- NextKey 교환 후 사용되는 모든 tag set의 경우, tag set 번호는 (1 + Alice의 key ID + Bob의 key ID)입니다.

#### Ack 요청

인밴드 ack를 요청합니다. Garlic Clove에서 아웃오브밴드 DeliveryStatus 메시지를 대체하기 위해 사용됩니다.

명시적인 ack가 요청되면, 현재 tagset ID와 메시지 번호(N)가 ack 블록에서 반환됩니다.

NS 또는 NSR에서는 허용되지 않습니다. Existing Session 메시지에만 포함됩니다.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### 패딩

모든 패딩은 AEAD 프레임 내부에 있습니다. TODO AEAD 내부의 패딩은 협상된 매개변수를 대략적으로 준수해야 합니다. TODO Alice는 NS 메시지에서 요청된 tx/rx 최소/최대 매개변수를 전송했습니다. TODO Bob은 NSR 메시지에서 요청된 tx/rx 최소/최대 매개변수를 전송했습니다. 업데이트된 옵션은 데이터 단계 중에 전송될 수 있습니다. 위의 옵션 블록 정보를 참조하십시오.

존재하는 경우, 이것은 프레임의 마지막 블록이어야 합니다.

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

- 모든 0으로 채우는 패딩은 암호화될 것이므로 문제없습니다.
- 패딩 전략은 추후 결정될 예정입니다.
- 패딩 전용 프레임이 허용됩니다.
- 패딩 기본값은 0-15바이트입니다.
- 패딩 매개변수 협상에 대해서는 옵션 블록을 참조하세요
- 최소/최대 패딩 매개변수에 대해서는 옵션 블록을 참조하세요
- 협상된 패딩 위반에 대한 router 응답은
  구현에 따라 다릅니다.

#### 기타 블록 유형

구현체들은 향후 호환성을 위해 알 수 없는 블록 타입들을 무시해야 합니다.

#### 향후 작업

- 패딩 길이는 메시지별로 결정되고 길이 분포를 추정하거나, 무작위 지연을 추가해야 합니다. 이러한 대응책은 DPI에 저항하기 위해 포함되어야 하는데, 그렇지 않으면 메시지 크기가 전송 프로토콜에 의해 I2P 트래픽이 전달되고 있음을 드러낼 수 있기 때문입니다. 정확한 패딩 방식은 향후 연구 영역이며, 부록 A에서 이 주제에 대한 자세한 정보를 제공합니다.

## 일반적인 사용 패턴

### HTTP GET

이는 가장 일반적인 사용 사례이며, 대부분의 비HTTP 스트리밍 사용 사례도 이 사용 사례와 동일할 것입니다. 작은 초기 메시지가 전송되고, 응답이 따르며, 양방향으로 추가 메시지가 전송됩니다.

HTTP GET은 일반적으로 단일 I2NP 메시지에 맞습니다. Alice는 응답 leaseSet을 번들링하여 단일 새 Session 메시지로 작은 요청을 보냅니다. Alice는 새 키로의 즉시 ratchet을 포함합니다. destination에 바인딩하기 위한 서명을 포함합니다. ack는 요청되지 않습니다.

Bob이 즉시 ratchet합니다.

Alice는 즉시 ratchet합니다.

해당 세션들을 계속 진행합니다.

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
### HTTP POST

Alice는 세 가지 옵션을 가지고 있습니다:

1)  HTTP GET처럼 첫 번째 메시지만 전송 (윈도우 크기 = 1). 아님

    recommended.
2) streaming window까지 전송하되, 동일한 Elligator2로 인코딩된 것을 사용

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3) 권장 구현. 스트리밍 윈도우까지 전송하되, 다음을 사용:

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

옵션 3 메시지 흐름:

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
### 응답 가능한 데이터그램

단일 메시지로, 단일 응답이 예상됩니다. 추가 메시지나 응답이 전송될 수 있습니다.

HTTP GET과 유사하지만 세션 태그 윈도우 크기와 수명에 대한 더 작은 옵션을 가집니다. ratchet을 요청하지 않을 수도 있습니다.

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
### 다중 원시 데이터그램

응답이 예상되지 않는 여러 개의 익명 메시지.

이 시나리오에서 Alice는 바인딩 없이 세션을 요청합니다. 새 세션 메시지가 전송됩니다. 응답 LS는 번들되지 않습니다. 응답 DSM이 번들됩니다 (이는 번들된 DSM이 필요한 유일한 사용 사례입니다). 다음 키는 포함되지 않습니다. 응답이나 ratchet이 요청되지 않습니다. ratchet이 전송되지 않습니다. 옵션은 세션 태그 윈도우를 0으로 설정합니다.

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
### 단일 원시 데이터그램

답장이 예상되지 않는 단일 익명 메시지입니다.

일회성 메시지가 전송됩니다. 응답 LS나 DSM이 번들로 포함되지 않습니다. 다음 키가 포함되지 않습니다. 응답이나 래칫이 요청되지 않습니다. 래칫이 전송되지 않습니다. 옵션에서 세션 태그 윈도우를 0으로 설정합니다.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### 장기 지속 세션

장기간 지속되는 세션은 해당 시점부터 전방향 보안성을 유지하기 위해 언제든지 ratchet을 수행하거나 ratchet을 요청할 수 있습니다. 세션은 세션당 전송된 메시지 한도(65535개)에 근접할 때 반드시 ratchet을 수행해야 합니다.

## 구현 고려사항

### 방어

기존 ElGamal/AES+SessionTag 프로토콜과 마찬가지로, 구현체들은 세션 태그 저장소를 제한하고 메모리 고갈 공격으로부터 보호해야 합니다.

권장되는 몇 가지 전략은 다음과 같습니다:

- 저장되는 세션 태그 수에 대한 하드 리미트
- 메모리 압박 상황에서 유휴 인바운드 세션의 적극적인 만료
- 단일 원격 목적지에 바인딩되는 인바운드 세션 수 제한
- 메모리 압박 시 세션 태그 윈도우의 적응적 축소 및 사용되지 않는 오래된 태그 삭제
- 메모리 압박 시 요청된 래칫 작업 거부

### 매개변수

권장 매개변수 및 시간 초과:

- NSR tagset 크기: 12 tsmin 및 tsmax
- ES tagset 0 크기: tsmin 24, tsmax 160
- ES tagset (1+) 크기: 160 tsmin 및 tsmax
- NSR tagset 타임아웃: 수신자 3분
- ES tagset 타임아웃: 송신자 8분, 수신자 10분
- 이전 ES tagset 제거 후: 3분
- 태그 N의 Tagset 미리보기: min(tsmax, tsmin + N/4)
- 태그 N의 Tagset 뒤쪽 정리: min(tsmax, tsmin + N/4) / 2
- 다음 키 전송 태그: 4096
- tagset 수명 후 다음 키 전송: TBD
- NS 수신 후 세션 교체: 3분 후
- 최대 클록 스큐: -5분에서 +2분
- NS 재생 필터 지속 시간: 5분
- 패딩 크기: 0-15바이트 (기타 전략 TBD)

### 분류

다음은 수신 메시지 분류에 대한 권장사항입니다.

#### X25519 전용

이 프로토콜만 사용하는 tunnel에서는 현재 ElGamal/AES+SessionTags로 수행되는 것과 같은 방식으로 식별을 수행합니다:

먼저, 초기 데이터를 session tag로 취급하고, session tag를 조회합니다. 찾았다면, 해당 session tag와 연결된 저장된 데이터를 사용하여 복호화합니다.

찾을 수 없는 경우, 초기 데이터를 DH 공개 키와 nonce로 처리합니다. DH 연산과 지정된 KDF를 수행하고, 남은 데이터의 복호화를 시도합니다.

#### ElGamal/AES+SessionTags와 공유되는 X25519

이 프로토콜과 ElGamal/AES+SessionTags를 모두 지원하는 tunnel에서 수신 메시지를 다음과 같이 분류합니다:

ElGamal/AES+SessionTags 사양의 결함으로 인해 AES 블록이 임의의 non-mod-16 길이로 패딩되지 않습니다. 따라서 기존 세션 메시지의 길이를 16으로 나눈 나머지는 항상 0이고, 새 세션 메시지의 길이를 16으로 나눈 나머지는 항상 2입니다 (ElGamal 블록이 514바이트 길이이므로).

길이를 16으로 나눈 나머지가 0이나 2가 아닌 경우, 초기 데이터를 session tag로 처리하고 해당 session tag를 찾아봅니다. 발견되면 그 session tag와 연결된 저장된 데이터를 사용하여 복호화합니다.

찾지 못하고 길이를 16으로 나눈 나머지가 0이나 2가 아닌 경우, 초기 데이터를 DH 공개 키와 nonce로 처리합니다. DH 연산과 지정된 KDF를 수행하고 남은 데이터의 복호화를 시도합니다. (상대적인 트래픽 혼합과 X25519 및 ElGamal DH 연산의 상대적 비용에 따라 이 단계는 마지막에 수행될 수도 있습니다)

그렇지 않고, 길이를 16으로 나눈 나머지가 0이면, 초기 데이터를 ElGamal/AES session tag로 취급하고 해당 session tag를 조회합니다. 발견되면, 그 session tag와 연관된 저장된 데이터를 사용하여 복호화합니다.

찾을 수 없고, 데이터가 최소 642(514 + 128)바이트 이상이며, 길이를 16으로 나눈 나머지가 2인 경우, 초기 데이터를 ElGamal 블록으로 처리합니다. 나머지 데이터의 복호화를 시도합니다.

ElGamal/AES+SessionTag 명세가 non-mod-16 패딩을 허용하도록 업데이트되면, 작업을 다르게 수행해야 할 것입니다.

### 재전송 및 상태 전환

ratchet 계층은 재전송을 수행하지 않으며, 두 가지 예외를 제외하고는 전송을 위한 타이머를 사용하지 않습니다. 타이머는 또한 tagset 타임아웃을 위해 필요합니다.

전송 타이머는 NSR을 전송할 때와 수신된 ES에 ACK 요청이 포함되어 있을 때 ES로 응답할 때만 사용됩니다. 권장 타임아웃은 1초입니다. 거의 모든 경우에서 상위 계층(데이터그램 또는 스트리밍)이 응답하여 NSR 또는 ES를 강제하므로 타이머가 취소될 수 있습니다. 타이머가 실행되면 NSR 또는 ES와 함께 빈 페이로드를 전송합니다.

#### 래칫 계층 응답

초기 구현들은 상위 계층에서의 양방향 트래픽에 의존합니다. 즉, 구현들은 반대 방향의 트래픽이 곧 전송될 것이라고 가정하며, 이는 ECIES 계층에서 필요한 응답을 강제하게 됩니다.

하지만 특정 트래픽은 단방향이거나 매우 낮은 대역폭을 가질 수 있어서, 적시에 응답을 생성할 상위 계층 트래픽이 없을 수 있습니다.

NS 및 NSR 메시지 수신 시 응답이 필요하며, ACK Request 및 Next Key 블록 수신 시에도 응답이 필요합니다.

구현체들은 응답이 필요한 이러한 메시지 중 하나를 받았을 때 타이머를 시작해야 하며, 짧은 시간(예: 1초) 내에 역방향 트래픽이 전송되지 않으면 ECIES 계층에서 "빈"(Garlic Clove 블록이 없는) 응답을 생성해야 합니다.

NS 및 NSR 메시지에 대한 응답에는 더욱 짧은 타임아웃을 적용하여 가능한 한 빨리 트래픽을 효율적인 ES 메시지로 전환하는 것이 적절할 수도 있습니다.

#### NSR을 위한 NS 바인딩

ratchet 계층에서 Bob으로서, Alice는 정적 키로만 알려져 있습니다. NS 메시지는 인증됩니다([Noise](https://noiseprotocol.org/noise.html) IK 발신자 인증 1). 그러나 네트워크 라우팅에는 완전한 Destination이 필요하므로, 이것만으로는 ratchet 계층이 Alice에게 무엇이든 보낼 수 있기에는 충분하지 않습니다.

NSR이 전송되기 전에, Alice의 전체 Destination은 ratchet 계층이나 상위 계층의 응답 가능한 프로토콜(응답 가능한 [Datagrams](/docs/specs/datagrams/) 또는 [Streaming](/docs/specs/streaming/))에 의해 발견되어야 합니다. 해당 Destination에 대한 Leaseset을 찾은 후, 그 Leaseset은 NS에 포함된 것과 동일한 정적 키를 포함하게 됩니다.

일반적으로, 상위 계층이 응답하여 Alice의 Destination Hash로 Alice의 Leaseset에 대한 네트워크 데이터베이스 조회를 강제합니다. 해당 Leaseset은 거의 항상 로컬에서 찾아집니다. 왜냐하면 NS에 Garlic Clove 블록이 포함되어 있고, 이 블록에는 Alice의 Leaseset을 포함하는 Database Store 메시지가 들어있기 때문입니다.

Bob이 ratchet-layer NSR을 보낼 준비를 하고 대기 중인 세션을 Alice의 Destination에 바인딩하려면, Bob은 NS 페이로드를 처리하는 동안 Destination을 "캡처"해야 합니다. NS의 정적 키와 일치하는 키를 가진 Leaseset을 포함하는 Database Store 메시지가 발견되면, 대기 중인 세션이 해당 Destination에 바인딩되고, Bob은 응답 타이머가 만료될 경우 NSR을 어디로 보낼지 알게 됩니다. 이것이 권장되는 구현 방법입니다.

대안적인 설계는 정적 키가 Destination에 매핑되는 캐시나 데이터베이스를 유지하는 것입니다. 이 접근법의 보안성과 실용성은 향후 연구 주제입니다.

이 명세서나 다른 명세서들도 모든 NS가 Alice의 LeaseSet을 포함해야 한다고 엄격하게 요구하지는 않습니다. 그러나 실제로는 포함해야 합니다. 권장되는 ES tagset 전송자 타임아웃(8분)이 최대 LeaseSet 타임아웃(10분)보다 짧기 때문에, 이전 세션이 만료되었지만 Alice는 Bob이 여전히 자신의 유효한 LeaseSet을 가지고 있다고 생각하여 새로운 NS와 함께 새로운 LeaseSet을 보내지 않는 작은 시간 간격이 있을 수 있습니다. 이는 추가 연구가 필요한 주제입니다.

#### 다중 NS 메시지

상위 계층(데이터그램 또는 스트리밍)이 재전송 등으로 더 많은 데이터를 보내기 전에 NSR 응답이 수신되지 않으면, Alice는 새로운 임시 키를 사용하여 새로운 NS를 구성해야 합니다. 이전 NS의 임시 키를 재사용하지 마십시오. Alice는 전송된 모든 NSR에 대한 응답으로 NSR 메시지를 수신하기 위해 추가 핸드셰이크 상태와 파생된 수신 tagset을 유지해야 합니다.

구현체는 전송되는 NS 메시지의 총 개수나 NS 메시지 전송 속도를 제한할 수 있으며, 이는 상위 계층 메시지가 전송되기 전에 대기열에 넣거나 삭제하는 방식으로 수행됩니다.

특정 상황에서, 높은 부하 상태이거나 특정 공격 시나리오 하에서는 리소스 고갈 공격을 피하기 위해 Bob이 복호화를 시도하지 않고 명백한 NS 메시지를 대기열에 넣거나, 삭제하거나, 제한하는 것이 적절할 수 있습니다.

수신된 각 NS에 대해, Bob은 NSR 아웃바운드 tagset을 생성하고, NSR을 전송하고, split()을 수행하며, 인바운드 및 아웃바운드 ES tagset을 생성합니다. 그러나 Bob은 해당 인바운드 tagset에서 첫 번째 ES 메시지가 수신될 때까지 ES 메시지를 전송하지 않습니다. 그 후, Bob은 수신된 다른 NS나 전송된 NSR에 대한 모든 핸드셰이크 상태와 tagset을 폐기하거나 곧 만료되도록 할 수 있습니다. ES 메시지에는 NSR tagset을 사용하지 마십시오.

Bob이 Alice로부터 첫 번째 ES를 수신하기 전이라도 NSR 직후 투기적으로 ES 메시지를 즉시 전송하도록 선택할 수 있는지는 추가 연구가 필요한 주제입니다. 특정 시나리오와 트래픽 패턴에서는 이것이 상당한 대역폭과 CPU를 절약할 수 있습니다. 이 전략은 트래픽 패턴, 첫 번째 세션의 tagset에서 수신된 ES의 비율, 또는 기타 데이터와 같은 휴리스틱을 기반으로 할 수 있습니다.

#### 다중 NSR 메시지

ES 메시지를 받을 때까지 수신된 각 NS 메시지에 대해, Bob은 상위 계층 트래픽 전송 또는 NSR 전송 타이머 만료로 인해 새로운 NSR로 응답해야 합니다.

각 NSR은 수신되는 NS에 해당하는 핸드셰이크 상태와 tagset을 사용합니다. Bob은 ES 메시지가 수신될 때까지 수신된 모든 NS 메시지에 대한 핸드셰이크 상태와 tagset을 유지해야 합니다.

구현체들은 전송되는 NSR 메시지의 총 개수나 NSR 메시지 전송 속도를 제한할 수 있습니다. 이는 상위 계층 메시지들이 전송되기 전에 큐에 넣거나 드롭하는 방식으로 이루어집니다. 이러한 제한은 수신되는 NS 메시지로 인해 발생하거나, 추가적인 상위 계층 아웃바운드 트래픽으로 인해 적용될 수 있습니다.

특정 상황에서, 높은 부하 상태이거나 특정 공격 시나리오 하에서는, 리소스 고갈 공격을 방지하기 위해 Alice가 복호화를 시도하지 않고 NSR 메시지를 큐에 넣거나, 버리거나, 제한하는 것이 적절할 수 있습니다. 이러한 제한은 모든 세션에 걸쳐 전체적으로, 세션별로, 또는 둘 다에 적용될 수 있습니다.

Alice가 NSR을 받으면, Alice는 split()을 수행하여 ES 세션 키를 도출합니다. Alice는 타이머를 설정하고, 상위 계층에서 트래픽을 보내지 않는 경우 일반적으로 1초 이내에 빈 ES 메시지를 전송해야 합니다.

다른 인바운드 NSR tagset들은 곧 제거되거나 만료되도록 허용될 수 있지만, Alice는 수신되는 다른 NSR 메시지들을 해독하기 위해 잠시 동안 그것들을 보관해야 합니다.

### 재생 공격 방지

Bob은 포함된 DateTime이 최근인 경우 NS 재생 공격을 방지하기 위해 Bloom filter 또는 다른 메커니즘을 구현해야 하며, DateTime이 너무 오래된 NS 메시지는 거부해야 합니다. Bob은 또한 복호화 이전에 최근의 중복 NS 메시지를 감지하고 폐기하기 위해 중복 임시 키(Elligator2 디코딩 전후)에 대한 이전 재생 탐지 검사를 사용할 수 있습니다.

NSR 및 ES 메시지는 세션 태그가 일회용이기 때문에 본질적으로 재전송 공격 방지 기능을 가지고 있습니다.

Garlic 메시지는 router가 I2NP 메시지 ID를 기반으로 한 router 전체 Bloom filter를 구현하는 경우 재생 공격 방지 기능도 제공합니다.

## 관련 변경사항

ECIES Destinations에서의 데이터베이스 조회: [Prop154](/proposals/154-ratchet/)를 참조하세요. 현재는 릴리스 0.9.46용 [I2NP](/docs/specs/i2np/)에 통합되어 있습니다.

이 사양은 leaseset과 함께 X25519 공개 키를 게시하기 위해 LS2 지원이 필요합니다. [I2NP](/docs/specs/i2np/)의 LS2 사양에는 변경 사항이 필요하지 않습니다. 모든 지원은 0.9.38에서 구현된 [Prop123](/proposals/123-new-netdb-entries/)에서 설계, 지정 및 구현되었습니다.

이 사양은 활성화되려면 I2CP 옵션에서 속성이 설정되어야 합니다. 모든 지원은 0.9.38에서 구현된 [Prop123](/proposals/123-new-netdb-entries/)에서 설계, 명시 및 구현되었습니다.

ECIES를 활성화하는 데 필요한 옵션은 I2CP, BOB, SAM 또는 i2ptunnel에 대한 단일 I2CP 속성입니다.

일반적인 값은 ECIES 전용의 경우 i2cp.leaseSetEncType=4이고, ECIES와 ElGamal 듀얼 키의 경우 i2cp.leaseSetEncType=4,0입니다.

## 호환성

dual key를 지원하는 LS2를 지원하는 모든 router(0.9.38 이상)는 dual key를 가진 destination으로의 연결을 지원해야 합니다.

ECIES 전용 목적지는 암호화된 조회 응답을 받기 위해 floodfill의 대부분이 0.9.46으로 업데이트되어야 합니다. [Prop154](/proposals/154-ratchet/)를 참조하세요.

ECIES 전용 destination은 ECIES 전용이거나 이중 키를 사용하는 다른 destination과만 연결할 수 있습니다.

## 참고 자료

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - [Elligator 기사](https://www.imperialviolet.org/2013/12/25/elligator.html) 및 OBFS4 코드도 참조
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
- [Streaming](/docs/specs/streaming/)
