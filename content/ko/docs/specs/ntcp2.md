---
title: "NTCP2 전송"
description: "router 간 연결을 위한 Noise 기반 TCP 전송"
slug: "ntcp2"
category: "전송 계층"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## 개요

NTCP2는 [NTCP](/docs/transport/ntcp)의 다양한 형태의 자동화된 식별 및 공격에 대한 저항성을 향상시키는 인증된 키 합의 프로토콜입니다.

NTCP2는 유연성과 NTCP와의 공존을 위해 설계되었습니다. NTCP와 동일한 포트에서 지원되거나, 다른 포트에서 지원되거나, NTCP 지원 없이 단독으로 지원될 수 있습니다. 자세한 내용은 아래 Published Router Info 섹션을 참조하세요.

다른 I2P transport들과 마찬가지로, NTCP2는 I2NP 메시지의 지점간(router간) transport용으로만 정의됩니다. 범용 데이터 파이프가 아닙니다.

NTCP2는 버전 0.9.36부터 지원됩니다. 배경 논의와 추가 정보를 포함한 원본 제안서는 [Prop111](/proposals/111-ntcp-2)을 참조하세요.

## Noise Protocol Framework

NTCP2는 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 33, 2017-10-04)를 사용합니다. Noise는 [SSU](/docs/transport/ssu) 프로토콜의 기반이 되는 Station-To-Station 프로토콜 [STS](#references)과 유사한 특성을 가지고 있습니다. Noise 용어에서 Alice는 개시자(initiator)이고, Bob은 응답자(responder)입니다.

NTCP2는 Noise 프로토콜 Noise_XK_25519_ChaChaPoly_SHA256을 기반으로 합니다. (초기 키 유도 함수의 실제 식별자는 I2P 확장을 나타내는 "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"입니다 - 아래 KDF 1 섹션 참조) 이 Noise 프로토콜은 다음 기본 요소들을 사용합니다:

- Handshake Pattern: XK Alice가 Bob에게 자신의 키를 전송 (X) Alice는 이미 Bob의 정적 키를 알고 있음 (K)
- DH Function: X25519 [RFC-7748](https://tools.ietf.org/html/rfc7748)에 명시된 대로 32바이트 키 길이를 가진 X25519 DH.
- Cipher Function: ChaChaPoly [RFC-7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8에 명시된 AEAD_CHACHA20_POLY1305. 12바이트 nonce, 처음 4바이트는 0으로 설정.
- Hash Function: SHA256 I2P에서 이미 광범위하게 사용되는 표준 32바이트 해시.

## 프레임워크에 추가된 사항

NTCP2는 Noise_XK_25519_ChaChaPoly_SHA256에 대한 다음과 같은 개선 사항을 정의합니다. 이는 일반적으로 [NOISE](https://noiseprotocol.org/noise.html) 섹션 13의 가이드라인을 따릅니다.

1) 평문 임시 키들은 알려진 키와 IV를 사용하여 AES 암호화로 난독화됩니다. 2) 무작위 평문 패딩이 메시지 1과 2에 추가됩니다. 평문 패딩은 핸드셰이크 해시(MixHash) 계산에 포함됩니다. 메시지 2와 메시지 3 파트 1에 대한 아래 KDF 섹션을 참조하세요. 무작위 AEAD 패딩이 메시지 3과 데이터 단계 메시지에 추가됩니다. 3) TCP를 통한 Noise에 필요하고 obfs4에서와 같이 2바이트 프레임 길이 필드가 추가됩니다. 이는 데이터 단계 메시지에서만 사용됩니다. 메시지 1과 2 AEAD 프레임은 고정 길이입니다. 메시지 3 파트 1 AEAD 프레임은 고정 길이입니다. 메시지 3 파트 2 AEAD 프레임 길이는 메시지 1에서 지정됩니다. 4) 2바이트 프레임 길이 필드는 obfs4에서와 같이 SipHash-2-4로 난독화됩니다. 5) 페이로드 형식은 메시지 1, 2, 3과 데이터 단계에 대해 정의됩니다. 물론 이것들은 프레임워크에서 정의되지 않습니다.

## 메시지

모든 NTCP2 메시지는 길이가 65537바이트 이하입니다. 메시지 형식은 Noise 메시지를 기반으로 하며, 프레이밍과 구별 불가능성을 위한 수정이 가해졌습니다. 표준 Noise 라이브러리를 사용하는 구현체는 수신된 메시지를 Noise 메시지 형식으로 변환하거나 그 반대로 변환하기 위해 전처리가 필요할 수 있습니다. 모든 암호화된 필드는 AEAD 암호문입니다.

설정 순서는 다음과 같습니다:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Noise 용어를 사용하여, 설정 및 데이터 시퀀스는 다음과 같습니다: ([Noise](https://noiseprotocol.org/noise.html)의 페이로드 보안 속성)

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
세션이 설정되면 Alice와 Bob은 Data 메시지를 교환할 수 있습니다.

모든 메시지 유형(SessionRequest, SessionCreated, SessionConfirmed, Data 및 TimeSync)은 이 섹션에서 명시됩니다.

일부 표기법:

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### 인증된 암호화

세 개의 별도 인증된 암호화 인스턴스(CipherStates)가 있습니다. 하나는 핸드셰이크 단계 중에 사용되고, 두 개(송신 및 수신)는 데이터 단계에 사용됩니다. 각각은 KDF에서 생성된 고유한 키를 가집니다.

암호화/인증된 데이터는 다음과 같이 표현됩니다

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

암호화되고 인증된 데이터 형식.

암호화/복호화 함수에 대한 입력:

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
암호화 함수의 출력, 복호화 함수의 입력:

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
ChaCha20의 경우, 여기서 설명하는 내용은 [RFC-7539](https://tools.ietf.org/html/rfc7539)에 해당하며, 이는 TLS [RFC-7905](https://tools.ietf.org/html/rfc7905)에서도 유사하게 사용됩니다.

#### 주의사항

- ChaCha20은 스트림 암호이므로 평문을 패딩할 필요가 없습니다. 추가 키스트림 바이트는 폐기됩니다.
- 암호의 키(256비트)는 SHA256 KDF를 통해 합의됩니다. 각 메시지에 대한 KDF의 세부사항은 아래 별도 섹션에서 다룹니다.
- 메시지 1, 2, 그리고 메시지 3의 첫 번째 부분에 대한 ChaChaPoly 프레임은 크기가 알려져 있습니다. 메시지 3의 두 번째 부분부터는 프레임이 가변 크기입니다. 메시지 3 파트 1의 크기는 메시지 1에서 지정됩니다. 데이터 단계부터는 obfs4에서와 같이 SipHash로 난독화된 2바이트 길이가 프레임 앞에 붙습니다.
- 메시지 1과 2에서는 패딩이 인증된 데이터 프레임 외부에 있습니다. 패딩은 다음 메시지의 KDF에서 사용되므로 변조가 감지됩니다. 메시지 3부터는 패딩이 인증된 데이터 프레임 내부에 있습니다.

#### AEAD 오류 처리

- 메시지 1, 2, 그리고 메시지 3의 파트 1과 2에서는 AEAD 메시지 크기가 미리 알려져 있습니다. AEAD 인증 실패 시, 수신자는 추가 메시지 처리를 중단하고 응답 없이 연결을 닫아야 합니다. 이는 비정상적인 종료(TCP RST)여야 합니다.
- 프로빙 저항성을 위해, 메시지 1에서 AEAD 실패 후 Bob은 임의의 타임아웃(범위 TBD)을 설정하고 소켓을 닫기 전에 임의의 바이트 수(범위 TBD)를 읽어야 합니다. Bob은 반복적인 실패가 있는 IP들의 블랙리스트를 유지해야 합니다.
- 데이터 단계에서는 AEAD 메시지 크기가 SipHash로 "암호화"(난독화)됩니다. 복호화 오라클을 생성하지 않도록 주의해야 합니다. 데이터 단계 AEAD 인증 실패 시, 수신자는 임의의 타임아웃(범위 TBD)을 설정하고 임의의 바이트 수(범위 TBD)를 읽어야 합니다. 읽기 완료 후 또는 읽기 타임아웃 시, 수신자는 "AEAD failure" 이유 코드가 포함된 종료 블록과 함께 페이로드를 전송하고 연결을 닫아야 합니다.
- 데이터 단계에서 유효하지 않은 길이 필드 값에 대해서도 동일한 오류 조치를 취하세요.

### 키 유도 함수 (KDF) (핸드셰이크 메시지 1용)

KDF는 [RFC-2104](https://tools.ietf.org/html/rfc2104)에서 정의된 HMAC-SHA256(key, data)를 사용하여 DH 결과로부터 핸드셰이크 단계 암호 키 k를 생성합니다. 이는 Noise 사양에서 정확히 정의된 InitializeSymmetric(), MixHash(), MixKey() 함수들입니다.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice가 Bob에게 보냅니다.

Noise 콘텐츠: Alice의 임시 키 X Noise 페이로드: 16바이트 옵션 블록 Non-noise 페이로드: 랜덤 패딩

(Payload Security Properties from [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
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
X 값은 페이로드의 구별 불가능성과 고유성을 보장하기 위해 암호화되며, 이는 필요한 DPI 대응책입니다. 이를 위해 elligator2와 같은 더 복잡하고 느린 대안보다는 AES 암호화를 사용합니다. Bob의 router 공개 키로 비대칭 암호화를 하는 것은 너무 느릴 것입니다. AES 암호화는 Bob의 router 해시를 키로 사용하고 네트워크 데이터베이스에 게시된 Bob의 IV를 사용합니다.

AES 암호화는 DPI 저항을 위한 목적으로만 사용됩니다. Bob의 router 해시와 IV를 알고 있는 당사자는 누구든지 이 메시지의 X 값을 복호화할 수 있으며, 이들은 netDb에 공개되어 있습니다.

패딩은 Alice에 의해 암호화되지 않습니다. 타이밍 공격을 방지하기 위해 Bob이 패딩을 복호화해야 할 수도 있습니다.

원시 내용:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Options 블록: 참고: 모든 필드는 빅 엔디언입니다.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### 참고사항

- 게시된 주소가 "NTCP"인 경우, Bob은 같은 포트에서 NTCP와 NTCP2를 모두 지원합니다. 호환성을 위해 "NTCP"로 게시된 주소에 연결을 시작할 때, Alice는 패딩을 포함한 이 메시지의 최대 크기를 287바이트 이하로 제한해야 합니다. 이는 Bob의 자동 프로토콜 식별을 용이하게 합니다. "NTCP2"로 게시된 경우에는 크기 제한이 없습니다. 아래의 게시된 주소 및 버전 감지 섹션을 참조하세요.

- 초기 AES 블록의 고유한 X 값은 모든 세션에 대해 암호문이 다르도록 보장합니다.

- Bob은 타임스탬프 값이 현재 시간과 너무 큰 차이를 보이는 연결을 거부해야 합니다. 최대 델타 시간을 "D"라고 합니다. Bob은 이전에 사용된 핸드셰이크 값들의 로컬 캐시를 유지하고 중복을 거부하여 재생 공격을 방지해야 합니다. 캐시의 값들은 최소 2*D의 수명을 가져야 합니다. 캐시 값들은 구현에 따라 다르지만, 32바이트 X 값(또는 그 암호화된 동등물)을 사용할 수 있습니다.

- Diffie-Hellman 임시 키는 암호학적 공격을 방지하기 위해 절대 재사용되어서는 안 되며, 재사용 시 재전송 공격으로 간주되어 거부됩니다.

- "KE"와 "auth" 옵션은 호환 가능해야 합니다. 즉, 공유 비밀 K는 적절한 크기여야 합니다. 더 많은 "auth" 옵션이 추가되면, 이는 암묵적으로 "KE" 플래그의 의미를 다른 KDF나 다른 절단 크기를 사용하도록 변경할 수 있습니다.

- Bob은 여기서 Alice의 임시 키가 곡선 상의 유효한 점인지 검증해야 합니다.

- 패딩은 합리적인 양으로 제한되어야 합니다. Bob은 과도한 패딩이 있는 연결을 거부할 수 있습니다. Bob은 메시지 2에서 자신의 패딩 옵션을 지정할 것입니다. 최소/최대 가이드라인은 추후 결정 예정입니다. 최소 0에서 31바이트까지의 랜덤 크기? (분포는 구현에 따라 다름) Java 구현체들은 현재 패딩을 최대 256바이트로 제한하고 있습니다.

- AEAD, DH, 타임스탬프, 명백한 재전송, 또는 키 검증 실패를 포함한 모든 오류 발생 시, Bob은 추가 메시지 처리를 중단하고 응답하지 않은 채 연결을 닫아야 합니다. 이는 비정상적인 종료(TCP RST)여야 합니다. 탐지 저항성을 위해, AEAD 실패 후 Bob은 무작위 타임아웃(범위 미정)을 설정한 다음 소켓을 닫기 전에 무작위 바이트 수(범위 미정)를 읽어야 합니다.

- Bob은 복호화를 시도하기 전에 유효한 키에 대해 빠른 MSB 검사(X[31] & 0x80 == 0)를 수행할 수 있습니다. 높은 비트가 설정되어 있다면, AEAD 실패에 대한 것과 같이 탐지 저항을 구현하세요.

- DoS 완화: DH는 상대적으로 비용이 많이 드는 연산입니다. 이전 NTCP 프로토콜과 마찬가지로, router들은 CPU나 연결 고갈을 방지하기 위해 필요한 모든 조치를 취해야 합니다. 최대 활성 연결 수와 진행 중인 최대 연결 설정 수에 제한을 둡니다. 읽기 시간 제한을 강제합니다(읽기당 및 "slowloris"에 대한 총 시간 모두). 동일한 소스로부터의 반복적이거나 동시 연결을 제한합니다. 반복적으로 실패하는 소스에 대한 블랙리스트를 유지합니다. AEAD 실패에 응답하지 않습니다.

- 빠른 버전 감지 및 핸드셰이킹을 용이하게 하기 위해, 구현체는 Alice가 패딩을 포함하여 첫 번째 메시지의 전체 내용을 버퍼링한 후 한 번에 플러시하도록 해야 합니다. 이는 데이터가 단일 TCP 패킷에 포함될 가능성을 높이며(OS나 중간 장치에 의해 분할되지 않는 한), Bob이 모든 데이터를 한 번에 수신할 수 있게 합니다. 또한 구현체는 Bob이 패딩을 포함하여 두 번째 메시지의 전체 내용을 버퍼링한 후 한 번에 플러시하고, 세 번째 메시지의 전체 내용도 버퍼링한 후 한 번에 플러시하도록 해야 합니다. 이는 효율성을 위한 것이며 랜덤 패딩의 효과를 보장하기 위함입니다.

- "ver" 필드: 페이로드 사양을 포함한 전체 Noise 프로토콜, 확장 기능, NTCP 프로토콜로서 NTCP2를 나타냅니다. 이 필드는 향후 변경 사항에 대한 지원을 나타내는 데 사용될 수 있습니다.

- Message 3 part 2 길이: 이것은 SessionConfirmed 메시지에서 전송될 Alice의 Router Info와 선택적 패딩을 포함하는 두 번째 AEAD 프레임(16바이트 MAC 포함)의 크기입니다. router들이 주기적으로 자신의 Router Info를 재생성하고 재발행하므로, 메시지 3이 전송되기 전에 현재 Router Info의 크기가 변경될 수 있습니다. 구현체들은 다음 두 가지 전략 중 하나를 선택해야 합니다:

a\) 메시지 3에서 전송될 현재 Router Info를 저장하여 크기를 알 수 있도록 하고, 선택적으로 패딩을 위한 공간을 추가합니다;

b\) Router Info 크기의 가능한 증가를 허용할 수 있도록 지정된 크기를 충분히 늘리고, 메시지 3이 실제로 전송될 때 항상 패딩을 추가합니다. 어느 경우든 메시지 1에 포함된 "m3p2len" 길이는 메시지 3에서 전송될 때 해당 프레임의 크기와 정확히 일치해야 합니다.

- Bob은 메시지 1을 검증하고 패딩을 읽어들인 후 들어오는 데이터가 남아있으면 연결을 실패시켜야 합니다. Bob이 아직 메시지 2로 응답하지 않았으므로 Alice로부터 추가 데이터가 있어서는 안 됩니다.

- 네트워크 ID 필드는 교차 네트워크 연결을 빠르게 식별하는 데 사용됩니다. 이 필드가 0이 아니고 Bob의 네트워크 ID와 일치하지 않으면, Bob은 연결을 끊고 향후 연결을 차단해야 합니다. 테스트 네트워크로부터의 모든 연결은 다른 ID를 가져야 하며 테스트에 실패할 것입니다. 0.9.42부터 적용. 자세한 정보는 proposal 147을 참조하십시오.

- API 0.9.68 (릴리스 2.11.0)까지 Java I2P는 non-PQ 연결에 대해 최대 256바이트 패딩을 구현했지만, 이전에는 문서화되지 않았습니다.
  API 0.9.69 (릴리스 2.12.0)부터 Java I2P는 non-PQ 연결에 대해 MLKEM-512와 동일한 최대 패딩을 구현합니다. 최대 패딩은 880바이트입니다.

### 키 유도 함수 (KDF) (핸드셰이크 메시지 2 및 메시지 3 파트 1용)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob이 Alice에게 보냅니다.

Noise 콘텐츠: Bob의 임시 키 Y Noise 페이로드: 16바이트 옵션 블록 Non-noise 페이로드: 랜덤 패딩

(Payload Security Properties from [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
Y 값은 페이로드의 식별 불가능성과 고유성을 보장하기 위해 암호화되며, 이는 필수적인 DPI 대응책입니다. 이를 달성하기 위해 elligator2와 같은 더 복잡하고 느린 대안 대신 AES 암호화를 사용합니다. Alice의 router 공개키에 대한 비대칭 암호화는 너무 느릴 것입니다. AES 암호화는 Bob의 router 해시를 키로 사용하고, 메시지 1의 AES 상태(netDb에 게시된 Bob의 IV로 초기화됨)를 사용합니다.

AES 암호화는 DPI 저항을 위한 것입니다. Bob의 router 해시와 IV를 알고 있는 당사자는 네트워크 데이터베이스에 게시되어 있으며, 메시지 1의 처음 32바이트를 캡처했다면 이 메시지의 Y 값을 복호화할 수 있습니다.

원본 내용:

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### 참고사항

- Alice는 Bob의 ephemeral key가 여기서 곡선 위의 유효한 점인지 검증해야 합니다.
- 패딩은 합리적인 양으로 제한되어야 합니다. Alice는 과도한 패딩이 있는 연결을 거부할 수 있습니다. Alice는 메시지 3에서 자신의 패딩 옵션을 명시할 것입니다. 최소/최대 가이드라인은 추후 결정됩니다. 최소 0~31바이트에서 무작위 크기? (분포는 구현에 따라 다름)
- AEAD, DH, 타임스탬프, 명백한 재전송, 또는 키 검증 실패를 포함한 모든 오류에서 Alice는 추가 메시지 처리를 중단하고 응답 없이 연결을 종료해야 합니다. 이는 비정상 종료(TCP RST)여야 합니다.
- 신속한 핸드셰이킹을 용이하게 하기 위해, 구현체들은 Bob이 패딩을 포함한 첫 번째 메시지의 전체 내용을 버퍼링한 다음 한 번에 플러시하도록 보장해야 합니다. 이는 데이터가 단일 TCP 패킷에 포함될 가능성을 높이고(OS나 중간 장치에 의해 분할되지 않는 한), Alice가 모든 데이터를 한 번에 수신할 수 있게 합니다. 이는 효율성과 무작위 패딩의 효과를 보장하기 위함입니다.
- Alice는 메시지 2를 검증하고 패딩을 읽어들인 후 들어오는 데이터가 남아있다면 연결을 실패시켜야 합니다. Alice가 아직 메시지 3으로 응답하지 않았으므로 Bob으로부터 추가 데이터가 있어서는 안 됩니다.

Options 블록: 참고: 모든 필드는 빅 엔디안입니다.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### 노트

- Alice는 타임스탬프 값이 현재 시간과 너무 차이가 나는 연결을 거부해야 합니다. 최대 델타 시간을 "D"라고 합니다. Alice는 이전에 사용된 핸드셰이크 값들의 로컬 캐시를 유지하고 중복을 거부하여 재생 공격을 방지해야 합니다. 캐시의 값들은 최소 2*D의 수명을 가져야 합니다. 캐시 값들은 구현에 따라 다르지만, 32바이트 Y 값(또는 그에 상응하는 암호화된 값)을 사용할 수 있습니다.

- API 0.9.68 (릴리스 2.11.0)까지, Java I2P는 non-PQ 연결에 대해 최대 256바이트 패딩을 구현했으나, 이는 이전에 문서화되지 않았습니다.
  API 0.9.69 (릴리스 2.12.0)부터, Java I2P는 non-PQ 연결에 대해 MLKEM-512와 동일한 최대 패딩을 구현합니다. 최대 패딩은 848바이트입니다.

#### 문제

- 여기에 최소/최대 패딩 옵션을 포함할까요?

### handshake 메시지 3 파트 1에 대한 암호화, 메시지 2 KDF 사용)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### 키 유도 함수 (KDF) (핸드셰이크 메시지 3 파트 2용)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice가 Bob에게 보냅니다.

Noise 콘텐츠: Alice의 정적 키 Noise 페이로드: Alice의 RouterInfo 및 랜덤 패딩 Non-noise 페이로드: 없음

(페이로드 보안 속성은 [Noise](https://noiseprotocol.org/noise.html)에서 가져옴)

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
이것은 두 개의 ChaChaPoly 프레임을 포함합니다. 첫 번째는 Alice의 암호화된 정적 공개키입니다. 두 번째는 Noise 페이로드입니다: Alice의 암호화된 RouterInfo, 선택적 옵션들, 그리고 선택적 패딩입니다. 중간에 MixKey() 함수가 호출되기 때문에 서로 다른 키를 사용합니다.

원본 내용:

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### 참고사항

- Bob은 일반적인 Router Info 검증을 수행해야 합니다. 서명 유형이 지원되는지 확인하고, 서명을 검증하며, 타임스탬프가 범위 내에 있는지 확인하고, 기타 필요한 모든 검사를 수행해야 합니다.

- Bob은 첫 번째 프레임에서 수신한 Alice의 정적 키가 Router Info의 정적 키와 일치하는지 확인해야 합니다. Bob은 먼저 Router Info에서 일치하는 버전(v) 옵션을 가진 NTCP 또는 NTCP2 Router Address를 검색해야 합니다. 아래의 게시된 Router Info와 게시되지 않은 Router Info 섹션을 참조하세요.

- Bob이 자신의 netdb에 Alice의 RouterInfo의 이전 버전을 가지고 있다면, router info에 있는 정적 키가 양쪽에서 동일한지 확인하고(존재하는 경우), 이전 버전이 XXX보다 오래되지 않았는지 확인합니다(아래 키 회전 시간 참조)

- Bob은 여기서 Alice의 정적 키가 곡선 위의 유효한 점인지 검증해야 합니다.

- 패딩 매개변수를 지정하기 위해 옵션이 포함되어야 합니다.

- AEAD, RI, DH, 타임스탬프 또는 키 검증 실패를 포함한 모든 오류가 발생하면, Bob은 추가 메시지 처리를 중단하고 응답 없이 연결을 닫아야 합니다. 이는 비정상 종료(TCP RST)여야 합니다.

- 빠른 핸드셰이킹을 촉진하기 위해, 구현체들은 Alice가 두 AEAD 프레임을 모두 포함하여 세 번째 메시지의 전체 내용을 버퍼링한 다음 한 번에 플러시하도록 보장해야 합니다. 이는 (OS나 미들박스에 의해 분할되지 않는 한) 데이터가 단일 TCP 패킷에 포함되어 Bob이 한 번에 수신할 가능성을 높입니다. 이는 또한 효율성과 랜덤 패딩의 효과를 보장하기 위함입니다.

- 메시지 3 파트 2 프레임 길이: 이 프레임의 길이(MAC 포함)는 메시지 1에서 Alice가 전송합니다. 패딩을 위한 충분한 공간 확보에 대한 중요한 참고사항은 해당 메시지를 참조하세요.

- 메시지 3 파트 2 프레임 콘텐츠: 이 프레임의 형식은 데이터 단계 프레임의 형식과 동일하지만, 프레임의 길이는 메시지 1에서 Alice가 전송합니다. 데이터 단계 프레임 형식은 아래를 참조하세요. 프레임은 다음 순서로 1개에서 3개의 블록을 포함해야 합니다:

1)  Alice의 Router Info 블록 (필수)   2)  Options 블록 (선택사항)

3\) 패딩 블록 (선택사항) 이 프레임은 다른 블록 유형을 포함해서는 안 됩니다.

- Alice가 메시지 3의 끝에 데이터 단계 프레임을 추가하고(선택적으로 패딩 포함) 둘을 한 번에 보내는 경우, 관찰자에게는 하나의 큰 바이트 스트림으로 보이기 때문에 메시지 3 파트 2 패딩이 필요하지 않습니다. Alice는 일반적으로(항상은 아니지만) Bob에게 보낼 I2NP 메시지를 가지고 있으므로(그래서 그에게 연결한 것입니다), 효율성과 랜덤 패딩의 효과를 보장하기 위해 이 방법이 권장되는 구현입니다.

- 메시지 3 AEAD 프레임(부분 1과 2)의 이론적 최대 총 길이는 65535바이트이다. 부분 1은 48바이트이므로, 부분 2의 최대 프레임 길이는 65487이다. MAC을 제외한 부분 2의 최대 평문 길이는 65471이다.
경고: 일부 구현체는 훨씬 더 작은 길이를 강제 적용한다. Java I2P는 현재 총 길이를 4096바이트로 제한하고 있다. 과도한 패딩을 추가하지 마십시오.

### 키 유도 함수 (KDF) (데이터 단계용)

데이터 단계는 길이가 0인 연관 데이터 입력을 사용합니다.

KDF는 [RFC-2104](https://tools.ietf.org/html/rfc2104)에 정의된 HMAC-SHA256(key, data)을 사용하여 chaining key ck로부터 두 개의 cipher key k_ab와 k_ba를 생성합니다. 이는 Noise 스펙에서 정의된 Split() 함수와 정확히 동일합니다.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) 데이터 단계

Noise 페이로드: 아래에 정의된 바와 같이, 랜덤 패딩을 포함 Non-noise 페이로드: 없음

메시지 3의 두 번째 부분부터 시작하여, 모든 메시지는 앞에 2바이트 난독화된 길이가 붙은 인증되고 암호화된 ChaChaPoly "프레임" 안에 있습니다. 모든 패딩은 프레임 내부에 있습니다. 프레임 내부는 0개 이상의 "블록"을 가진 표준 형식입니다. 각 블록은 1바이트 타입과 2바이트 길이를 가집니다. 타입에는 날짜/시간, I2NP 메시지, 옵션, 종료, 패딩이 포함됩니다.

참고: Bob은 데이터 단계에서 Alice에게 보내는 첫 번째 메시지로 자신의 RouterInfo를 보낼 수 있지만, 반드시 그럴 필요는 없습니다.

(페이로드 보안 속성은 [Noise](https://noiseprotocol.org/noise.html)에서 가져옴)

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### 참고 사항

- 효율성을 위해 그리고 길이 필드의 식별을 최소화하기 위해, 구현체는 송신자가 길이 필드와 AEAD 프레임을 포함하여 데이터 메시지의 전체 내용을 버퍼링한 다음 한 번에 플러시하도록 보장해야 합니다. 이는 데이터가 (OS나 미들박스에 의해 분할되지 않는 한) 단일 TCP 패킷에 포함되고 상대방이 한 번에 수신할 가능성을 높입니다. 이는 또한 효율성과 랜덤 패딩의 효과를 보장하기 위함입니다.
- router는 AEAD 오류 시 세션을 종료하거나 계속 통신을 시도할 수 있습니다. 계속 진행하는 경우, router는 반복적인 오류 후에 종료해야 합니다.

#### SipHash 난독화된 길이

참조: [SipHash](https://www.131002.net/siphash/)

양측이 핸드셰이크를 완료하면, ChaChaPoly "프레임"으로 암호화되고 인증된 페이로드를 전송합니다.

각 프레임은 빅 엔디안 방식의 2바이트 길이 값이 앞에 붙습니다. 이 길이는 MAC을 포함하여 뒤따르는 암호화된 프레임 바이트 수를 지정합니다. 스트림에서 식별 가능한 길이 필드 전송을 피하기 위해, 프레임 길이는 데이터 단계 KDF에서 초기화된 SipHash에서 파생된 마스크와 XOR 연산하여 난독화됩니다. 두 방향은 KDF에서 고유한 SipHash 키와 IV를 가진다는 점에 주목하세요.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
수신자는 동일한 SipHash 키와 IV를 가지고 있습니다. 길이를 디코딩하는 것은 길이를 난독화하는 데 사용된 마스크를 도출하고 잘린 다이제스트를 XOR하여 프레임의 길이를 얻는 방식으로 수행됩니다. 프레임 길이는 MAC를 포함한 암호화된 프레임의 총 길이입니다.

#### 참고사항

- unsigned long 정수를 반환하는 SipHash 라이브러리 함수를 사용하는 경우, 최하위 2바이트를 Mask로 사용하세요. long 정수를 little endian으로 다음 IV로 변환하세요.

#### 원시 내용

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### 노트

- 수신자는 MAC을 확인하기 위해 전체 프레임을 받아야 하므로, 송신자는 프레임 크기를 최대화하기보다는 몇 KB로 제한하는 것이 권장됩니다. 이렇게 하면 수신자에서의 지연시간을 최소화할 수 있습니다.

#### 암호화되지 않은 데이터

암호화된 프레임에는 0개 이상의 블록이 있습니다. 각 블록은 1바이트 식별자, 2바이트 길이, 그리고 0개 이상의 데이터 바이트를 포함합니다.

확장성을 위해, 수신자는 알 수 없는 식별자를 가진 블록을 무시하고 패딩으로 처리해야 합니다.

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
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
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

handshake 메시지 3 파트 2에서 순서는 다음과 같아야 합니다: RouterInfo, 다음에 Options(있는 경우), 다음에 Padding(있는 경우). 다른 블록은 허용되지 않습니다.

데이터 단계에서 순서는 지정되지 않지만, 다음 요구사항은 예외입니다: 패딩이 있는 경우 마지막 블록이어야 합니다. 종료가 있는 경우 패딩을 제외하고 마지막 블록이어야 합니다.

하나의 프레임에 여러 개의 I2NP 블록이 있을 수 있습니다. 하나의 프레임에 여러 개의 패딩 블록은 허용되지 않습니다. 다른 블록 유형들은 하나의 프레임에 여러 블록을 가질 가능성이 낮지만, 금지되지는 않습니다.

#### DateTime

시간 동기화를 위한 특별한 경우:

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
참고: 구현체들은 네트워크에서 시계 편향을 방지하기 위해 가장 가까운 초 단위로 반올림해야 합니다.

#### 옵션

업데이트된 옵션을 전달합니다. 옵션에는 최소 및 최대 패딩이 포함됩니다.

옵션 블록은 가변 길이가 됩니다.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

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

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### 옵션 문제

- 옵션 형식은 미정입니다.
- 옵션 협상은 미정입니다.

#### RouterInfo

Alice의 RouterInfo를 Bob에게 전달합니다. 핸드셰이크 메시지 3 파트 2에서 사용됩니다. Alice의 RouterInfo를 Bob에게 전달하거나, Bob의 RouterInfo를 Alice에게 전달합니다. 데이터 단계에서 선택적으로 사용됩니다.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### 참고사항

- 데이터 단계에서 사용될 때, 수신자(Alice 또는 Bob)는 원래 전송된(Alice의 경우) 또는 전송 대상(Bob의 경우)과 동일한 Router Hash인지 검증해야 합니다. 그런 다음 로컬 I2NP DatabaseStore Message로 처리합니다. 서명을 검증하고, 더 최근 타임스탬프를 검증하고, 로컬 netDb에 저장합니다. 플래그 비트 0이 1이고 수신 측이 floodfill인 경우, 0이 아닌 응답 토큰이 있는 DatabaseStore Message로 처리하고 가장 가까운 floodfill들에게 플러딩합니다.
- Router Info는 gzip으로 압축되지 않습니다 (압축되는 DatabaseStore Message와는 달리)
- RouterInfo에 게시된 RouterAddress가 있지 않은 경우 플러딩을 요청해서는 안 됩니다. 수신 router는 RouterInfo에 게시된 RouterAddress가 없으면 RouterInfo를 플러딩하지 않아야 합니다.
- 구현자들은 블록을 읽을 때 잘못된 형식이거나 악의적인 데이터로 인해 다음 블록으로 읽기가 넘어가지 않도록 해야 합니다.
- 이 프로토콜은 RouterInfo가 수신, 저장 또는 플러딩되었다는 확인응답을 제공하지 않습니다(핸드셰이크나 데이터 단계 모두에서). 확인응답이 필요하고 수신자가 floodfill인 경우, 송신자는 대신 응답 토큰이 있는 표준 I2NP DatabaseStoreMessage를 전송해야 합니다.

#### 문제점

- I2NP DatabaseStoreMessage 대신 데이터 단계에서도 사용될 수 있습니다. 예를 들어, Bob이 데이터 단계를 시작하는 데 사용할 수 있습니다.
- floodfill에 의한 플러딩과 같이 DatabaseStoreMessage의 일반적인 대체제로서, 발신자가 아닌 다른 router들의 RI를 포함하는 것이 허용됩니까?

#### I2NP 메시지

수정된 헤더를 가진 단일 I2NP 메시지입니다. I2NP 메시지는 블록 간 또는 ChaChaPoly 프레임 간에 분할될 수 없습니다.

이는 표준 NTCP I2NP 헤더에서 처음 9바이트를 사용하고, 다음과 같이 헤더의 마지막 7바이트를 제거합니다: 만료 시간을 8바이트에서 4바이트로 단축(SSU와 동일하게 밀리초 대신 초 단위 사용), 2바이트 길이 제거(블록 크기 - 9 사용), 그리고 1바이트 SHA256 체크섬 제거.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### 참고사항

- 구현자는 블록을 읽을 때 잘못된 형태나 악의적인 데이터로 인해 다음 블록까지 읽기가 넘어가지 않도록 해야 합니다.

#### 종료

Noise는 명시적인 종료 메시지를 권장합니다. 원래 NTCP에는 없었습니다. 연결을 끊습니다. 이것은 프레임에서 패딩이 아닌 마지막 블록이어야 합니다.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### 주의사항

모든 이유가 실제로 사용되는 것은 아니며, 구현에 따라 다릅니다. 핸드셰이크 실패는 일반적으로 TCP RST로 연결을 닫는 결과를 가져옵니다. 위의 핸드셰이크 메시지 섹션의 참고사항을 참조하십시오. 나열된 추가 이유들은 일관성, 로깅, 디버깅 또는 정책 변경을 위한 것입니다.

#### 패딩

이는 AEAD 프레임 내부의 패딩을 위한 것입니다. 메시지 1과 2의 패딩은 AEAD 프레임 외부에 있습니다. 메시지 3과 데이터 단계의 모든 패딩은 AEAD 프레임 내부에 있습니다.

AEAD 내부의 패딩은 협상된 매개변수를 대략적으로 준수해야 합니다. Bob은 메시지 2에서 요청한 tx/rx 최소/최대 매개변수를 전송했습니다. Alice는 메시지 3에서 요청한 tx/rx 최소/최대 매개변수를 전송했습니다. 업데이트된 옵션들은 데이터 단계에서 전송될 수 있습니다. 위의 옵션 블록 정보를 참조하세요.

이 블록이 있는 경우, 프레임의 마지막 블록이어야 합니다.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### 참고 사항

- Size = 0이 허용됩니다.
- 패딩 전략은 미정입니다.
- 최소 패딩은 미정입니다.
- 패딩 전용 프레임이 허용됩니다.
- 패딩 기본값은 미정입니다.
- 패딩 매개변수 협상에 대해서는 옵션 블록을 참조하세요
- 최소/최대 패딩 매개변수에 대해서는 옵션 블록을 참조하세요
- Noise는 메시지를 64KB로 제한합니다. 더 많은 패딩이 필요한 경우 여러 프레임을 전송하세요.
- 협상된 패딩 위반에 대한 router 응답은 구현에 따라 다릅니다.

#### 기타 블록 타입

구현체는 향후 호환성을 위해 알 수 없는 블록 유형을 무시해야 하며, 메시지 3 파트 2에서는 알 수 없는 블록이 허용되지 않습니다.

#### 향후 작업

- 패딩 길이는 메시지별로 결정되고 길이 분포를 추정하거나, 무작위 지연을 추가해야 합니다. 이러한 대응책은 DPI에 저항하기 위해 포함되어야 하며, 그렇지 않으면 메시지 크기로 인해 전송 프로토콜이 I2P 트래픽을 전달하고 있음이 드러날 수 있습니다. 정확한 패딩 방식은 향후 연구 분야입니다.

### 5) 종료

연결은 정상적이거나 비정상적인 TCP 소켓 종료를 통해 종료되거나, Noise에서 권장하는 바와 같이 명시적인 종료 메시지를 통해 종료될 수 있습니다. 명시적인 종료 메시지는 위의 데이터 단계에서 정의됩니다.

정상 또는 비정상 종료 시, router는 핸드셰이크 임시 키, 대칭 암호화 키 및 관련 정보를 포함한 모든 메모리 내 임시 데이터를 제로화해야 합니다.

## 게시된 Router 정보

### 기능

릴리스 0.9.50부터 NTCP2 주소에서 SSU와 유사한 "caps" 옵션이 지원됩니다. "caps" 옵션에는 하나 이상의 기능을 게시할 수 있습니다. 기능은 임의의 순서로 배치할 수 있지만, 구현 간 일관성을 위해 "46" 순서를 권장합니다. 정의된 기능은 두 가지가 있습니다:

4: 아웃바운드 IPv4 기능을 나타냅니다. 호스트 필드에 IP가 게시된 경우 이 기능은 필요하지 않습니다. router가 숨겨져 있거나 NTCP2가 아웃바운드 전용인 경우 '4'와 '6'이 단일 주소에 결합될 수 있습니다.

6: 아웃바운드 IPv6 기능을 나타냅니다. IP가 호스트 필드에 게시된 경우 이 기능은 필요하지 않습니다. router가 숨겨져 있거나 NTCP2가 아웃바운드 전용인 경우, '4'와 '6'이 단일 주소에 결합될 수 있습니다.

### 게시된 주소

게시된 RouterAddress(RouterInfo의 일부)는 "NTCP" 또는 "NTCP2"의 프로토콜 식별자를 갖습니다.

RouterAddress는 현재 NTCP 프로토콜에서와 같이 "host"와 "port" 옵션을 포함해야 합니다.

RouterAddress는 NTCP2 지원을 나타내기 위해 세 가지 옵션을 포함해야 합니다:

- s=(Base64 키) 이 RouterAddress에 대한 현재 Noise static public key (s). 표준 I2P Base 64 알파벳을 사용하여 Base 64로 인코딩됨. 바이너리로 32바이트, Base 64 인코딩으로 44바이트, little-endian X25519 public key.
- i=(Base64 IV) 이 RouterAddress에 대한 메시지 1의 X 값을 암호화하기 위한 현재 IV. 표준 I2P Base 64 알파벳을 사용하여 Base 64로 인코딩됨. 바이너리로 16바이트, Base 64 인코딩으로 24바이트, big-endian.
- v=2 현재 버전 (2). "NTCP"로 게시될 때, 버전 1에 대한 추가 지원이 암시됨. 향후 버전에 대한 지원은 쉼표로 구분된 값(예: v=2,3)으로 제공됨. 구현체는 쉼표가 있는 경우 여러 버전을 포함하여 호환성을 확인해야 함. 쉼표로 구분된 버전들은 숫자 순서로 나열되어야 함.

Alice는 NTCP2 프로토콜을 사용하여 연결하기 전에 세 가지 옵션이 모두 존재하고 유효한지 확인해야 합니다.

"s", "i", "v" 옵션과 함께 "NTCP"로 게시될 때, router는 해당 호스트와 포트에서 NTCP와 NTCP2 프로토콜 모두에 대한 들어오는 연결을 수락해야 하며, 프로토콜 버전을 자동으로 감지해야 합니다.

"s", "i", "v" 옵션과 함께 "NTCP2"로 게시되면, router는 해당 호스트와 포트에서 NTCP2 프로토콜에 대한 들어오는 연결만을 수락합니다.

router가 NTCP1과 NTCP2 연결을 모두 지원하지만 들어오는 연결에 대한 자동 버전 감지를 구현하지 않는 경우, "NTCP"와 "NTCP2" 주소를 모두 광고해야 하며, "NTCP2" 주소에만 NTCP2 옵션을 포함해야 합니다. router는 NTCP2가 선호되도록 "NTCP2" 주소에 "NTCP" 주소보다 낮은 비용 값(높은 우선순위)을 설정해야 합니다.

여러 NTCP2 RouterAddress들이 ("NTCP" 또는 "NTCP2"로) 동일한 RouterInfo에 게시되는 경우 (추가 IP 주소나 포트를 위해), 동일한 포트를 지정하는 모든 주소들은 동일한 NTCP2 옵션과 값을 포함해야 합니다. 특히, 모든 주소들은 동일한 정적 키와 iv를 포함해야 합니다.

### 게시되지 않은 NTCP2 주소

만약 Alice가 들어오는 연결을 위해 자신의 NTCP2 주소를 ("NTCP" 또는 "NTCP2"로) 공개하지 않는다면, Bob이 메시지 3 파트 2에서 Alice의 RouterInfo를 받은 후 키를 검증할 수 있도록 정적 키와 NTCP2 버전만 포함하는 "NTCP2" router 주소를 공개해야 합니다.

- s=(Base64 key) 게시된 주소에 대해 위에서 정의된 대로입니다.
- v=2 게시된 주소에 대해 위에서 정의된 대로입니다.

이 router 주소는 아웃바운드 NTCP2 연결에 필요하지 않으므로 "i", "host" 또는 "port" 옵션을 포함하지 않습니다. 이 주소의 공개된 비용은 인바운드 전용이므로 엄격하게 중요하지 않지만, 다른 주소보다 비용이 더 높게(우선순위가 낮게) 설정되면 다른 router에게 도움이 될 수 있습니다. 권장 값은 14입니다.

Alice는 기존에 게시된 "NTCP" 주소에 단순히 "s"와 "v" 옵션을 추가할 수도 있습니다.

### 공개 키 및 IV 순환

RouterInfo의 캐싱으로 인해, router가 실행 중일 때는 공개된 주소에 있든 없든 관계없이 정적 공개 키나 IV를 회전해서는 안 됩니다. Router는 즉시 재시작한 후 재사용을 위해 이 키와 IV를 영구적으로 저장해야 하므로, 들어오는 연결이 계속 작동하고 재시작 시간이 노출되지 않습니다. Router는 마지막 종료 시간을 영구적으로 저장하거나 다른 방법으로 결정해야 하므로, 시작할 때 이전 다운타임을 계산할 수 있습니다.

재시작 시간 노출에 대한 우려로 인해, router가 이전에 상당한 시간(최소 몇 시간) 동안 다운되었던 경우 시작 시 이 키나 IV를 교체할 수 있습니다.

router가 게시된 NTCP2 RouterAddress들을 가지고 있는 경우 (NTCP 또는 NTCP2로), 로컬 IP 주소가 변경되거나 router가 "rekeys"하지 않는 한, 순환 전 최소 다운타임은 훨씬 길어야 하며, 예를 들어 한 달 정도여야 합니다.

router가 게시된 SSU RouterAddress는 있지만 NTCP2 (NTCP 또는 NTCP2로서)는 없는 경우, 로컬 IP 주소가 변경되었거나 router가 "rekeys"하지 않는 한, 로테이션 전 최소 다운타임은 더 길어야 하며, 예를 들어 하루가 되어야 합니다. 이는 게시된 SSU 주소에 introducer가 있는 경우에도 적용됩니다.

router가 게시된 RouterAddresses(NTCP, NTCP2, 또는 SSU)를 가지고 있지 않다면, router가 "rekeys"를 수행하지 않는 한 IP 주소가 변경되더라도 교체 전 최소 다운타임은 2시간 정도로 짧을 수 있습니다.

router가 다른 Router Hash로 "rekeys"하는 경우, 새로운 noise 키와 IV도 생성해야 합니다.

구현체들은 정적 공개 키나 IV를 변경하면 이전 RouterInfo를 캐시한 router들로부터의 NTCP2 연결 수신이 차단될 수 있음을 인지해야 합니다. RouterInfo 발행, tunnel 피어 선택(OBGW와 IB 최근접 홉 모두 포함), 0홉 tunnel 선택, 전송 선택, 그리고 기타 구현 전략들은 이를 반드시 고려해야 합니다.

IV 순환은 키 순환과 동일한 규칙을 따르지만, IV는 게시된 RouterAddress에서만 존재하므로 숨겨지거나 방화벽이 설정된 router에는 IV가 없습니다. 무엇이든 변경되면(버전, 키, 옵션?) IV도 함께 변경하는 것이 권장됩니다.

참고: 재키잉 이전의 최소 다운타임은 네트워크 상태를 보장하고 적당한 시간 동안 다운된 router의 재시딩을 방지하기 위해 수정될 수 있습니다.

## 버전 감지

"NTCP"로 게시될 때, router는 들어오는 연결에 대해 프로토콜 버전을 자동으로 감지해야 합니다.

이 감지는 구현에 따라 달라지지만, 다음은 일반적인 지침입니다.

들어오는 NTCP 연결의 버전을 감지하기 위해 Bob은 다음과 같이 진행합니다:

- 최소 64바이트를 기다림 (최소 NTCP2 메시지 1 크기)

- 초기 수신 데이터가 288바이트 이상이면, 수신 연결은 버전 1입니다.

- 288바이트 미만인 경우, 다음 중 하나

> - 더 많은 데이터를 위해 짧은 시간 대기 (NTCP2 광범위 채택 이전의 좋은 전략) 총 288바이트 이상 수신되면 NTCP 1입니다.   >   > - 버전 2로 디코딩의 첫 번째 단계들을 시도하고, 실패하면 더 많은 데이터를 위해 짧은 시간 대기 (NTCP2 광범위 채택 이후의 좋은 전략)   >   >   > - SessionRequest 패킷의 첫 32바이트 (X 키)를 키 RH_B를 사용한 AES-256으로 복호화합니다.   >   > - 곡선상의 유효한 점인지 확인합니다. 실패하면 NTCP 1을 위해 더 많은 데이터를 위해 짧은 시간 대기   >   > - AEAD 프레임을 확인합니다. 실패하면 NTCP 1을 위해 더 많은 데이터를 위해 짧은 시간 대기

NTCP 1에서 활성 TCP 세그멘테이션 공격을 감지할 경우 변경사항이나 추가 전략이 권장될 수 있음에 유의하세요.

신속한 버전 감지와 핸드셰이킹을 용이하게 하기 위해, 구현체들은 Alice가 패딩을 포함한 첫 번째 메시지의 전체 내용을 버퍼링한 후 한 번에 플러시하도록 보장해야 합니다. 이는 데이터가 단일 TCP 패킷에 포함될 가능성을 높이고(OS나 미들박스에 의해 분할되지 않는 한), Bob이 한 번에 모두 수신할 수 있도록 합니다. 이는 효율성과 랜덤 패딩의 효과를 보장하기 위한 것이기도 합니다. 이는 NTCP와 NTCP2 핸드셰이크 모두에 적용됩니다.

## 변형, 폴백, 그리고 일반적인 문제들

- Alice와 Bob이 모두 NTCP2를 지원하는 경우, Alice는 NTCP2로 연결해야 합니다.
- Alice가 어떤 이유로든 NTCP2를 사용하여 Bob에 연결하는 데 실패하면 연결이 실패합니다. Alice는 NTCP 1을 사용하여 다시 시도할 수 없습니다.

## 시계 오차 가이드라인

피어 타임스탬프는 처음 두 핸드셰이크 메시지인 Session Request와 Session Created에 포함됩니다. 두 피어 간의 시계 편차가 +/- 60초를 초과하면 일반적으로 치명적입니다. Bob이 자신의 로컬 시계가 잘못되었다고 생각하면, 계산된 편차나 외부 소스를 사용하여 시계를 조정할 수 있습니다. 그렇지 않으면, Bob은 최대 편차가 초과되더라도 단순히 연결을 닫는 것보다는 Session Created로 응답해야 합니다. 이를 통해 Alice가 Bob의 타임스탬프를 얻어 편차를 계산하고, 필요시 조치를 취할 수 있습니다. 이 시점에서 Bob은 Alice의 router 신원을 알지 못하지만, 리소스를 절약하기 위해 과도한 편차로 인한 반복적인 연결 시도 후 일정 기간 동안 Alice의 IP로부터의 들어오는 연결을 차단하는 것이 바람직할 수 있습니다.

Alice는 RTT의 절반을 빼서 계산된 클럭 스큐를 조정해야 합니다. Alice가 자신의 로컬 클럭이 잘못되었다고 생각하면, 계산된 스큐나 외부 소스를 사용하여 클럭을 조정할 수 있습니다. Alice가 Bob의 클럭이 잘못되었다고 생각하면, 일정 기간 동안 Bob을 차단할 수 있습니다. 어느 경우든 Alice는 연결을 종료해야 합니다.

만약 Alice가 Session Confirmed로 응답한다면 (아마도 skew가 60초 한계에 매우 가깝고, RTT로 인해 Alice와 Bob의 계산이 정확히 동일하지 않기 때문일 것), Bob은 RTT의 절반을 빼서 계산된 클록 skew를 조정해야 합니다. 조정된 클록 skew가 최대값을 초과하면, Bob은 클록 skew 이유 코드가 포함된 Disconnect 메시지로 응답하고 연결을 종료해야 합니다. 이 시점에서 Bob은 Alice의 router identity를 가지고 있으며, Alice를 일정 기간 동안 차단할 수 있습니다.

## 참고 자료

- [공통 구조](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [네트워크 데이터베이스](/docs/overview/network-database)
- [NOISE - Noise Protocol Framework](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - DH Groups](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentication and Authenticated Key Exchanges
