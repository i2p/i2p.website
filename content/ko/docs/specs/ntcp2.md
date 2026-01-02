---
title: "NTCP2 전송"
description: "router 간 링크를 위한 Noise(프로토콜 프레임워크) 기반 TCP 전송"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## 개요

NTCP2는 트래픽 지문 식별에 대한 저항성을 갖고, 길이 필드를 암호화하며, 최신 암호군을 지원하는 Noise(보안 핸드셰이크 프레임워크) 기반 핸드셰이크로 기존 NTCP 전송을 대체합니다. Routers는 I2P 네트워크에서 필수인 두 가지 전송 프로토콜로서 SSU2와 함께 NTCP2를 실행할 수 있습니다. NTCP(버전 1)은 0.9.40(2019년 5월)에서 사용 중단되었으며 0.9.50(2021년 5월)에서 완전히 제거되었습니다.

## Noise Protocol Framework(노이즈 프로토콜 프레임워크)

NTCP2는 I2P 전용 확장과 함께 Noise Protocol Framework [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) (암호화 핸드셰이크 프로토콜 설계 프레임워크)를 사용합니다:

- **패턴**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **확장 식별자**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (KDF 초기화를 위해)
- **DH 함수**: X25519 (RFC 7748) - 32바이트 키, 리틀 엔디언 인코딩
- **암호**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12바이트 논스: 처음 4바이트는 0, 마지막 8바이트는 카운터(리틀 엔디언)
  - 최대 논스 값: 2^64 - 2 (연결은 2^64 - 1에 도달하기 전에 종료되어야 함)
- **해시 함수**: SHA-256 (32바이트 출력)
- **MAC**: Poly1305 (16바이트 인증 태그)

### I2P 전용 확장 기능

1. **AES 난독화**: 임시 키는 Bob의 router 해시와 공개된 IV를 사용하여 AES-256-CBC로 암호화됨
2. **임의 패딩**: 메시지 1-2에서는 평문 패딩(인증됨), 메시지 3+에서는 AEAD(연관 데이터 인증 암호) 패딩(암호화됨)
3. **SipHash-2-4 길이 난독화**: 2바이트 프레임 길이는 SipHash 출력과 XOR 처리됨
4. **프레임 구조**: 데이터 단계에서 길이 접두사 프레임(TCP 스트리밍 호환성)
5. **블록 기반 페이로드**: 타입이 지정된 블록으로 구성된 구조화된 데이터 형식

## 핸드셰이크 흐름

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### 3-메시지 핸드셰이크

1. **SessionRequest**(세션 요청) - 앨리스의 난독화된 임시 키, 옵션, 패딩 힌트
2. **SessionCreated**(세션 생성) - 밥의 난독화된 임시 키, 암호화된 옵션, 패딩
3. **SessionConfirmed**(세션 확인) - 앨리스의 암호화된 정적 키와 RouterInfo(router 정보) (AEAD(연관 데이터가 있는 인증 암호) 프레임 두 개)

### Noise(프로토콜 프레임워크) 메시지 패턴

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**인증 수준:** - 0: 인증 없음 (누구나 보냈을 수 있음) - 2: key-compromise impersonation (KCI, 키 손상 사칭)에 대한 저항성을 갖춘 발신자 인증

**기밀성 수준:** - 1: 일시적 수신자(전방향 보안(forward secrecy), 수신자 인증 없음) - 2: 확인된 수신자, 발신자 침해에 대해서만 전방향 보안 - 5: 강한 전방향 보안(ephemeral-ephemeral + ephemeral-static DH(Diffie-Hellman, 디피-헬만))

## 메시지 명세

### 키 표기법

- `RH_A` = Alice에 대한 Router 해시(32바이트, SHA-256)
- `RH_B` = Bob에 대한 Router 해시(32바이트, SHA-256)
- `||` = 연결 연산자
- `byte(n)` = 값이 n인 단일 바이트
- 모든 멀티바이트 정수는 별도 지정이 없는 한 **빅엔디언**
- X25519 키는 **리틀엔디언**(32바이트)

### 인증된 암호화 (ChaCha20-Poly1305)

**암호화 함수:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**매개변수:** - `key`: KDF(키 유도 함수)에서 파생된 32바이트 암호 키 - `nonce`: 12바이트(0 값 바이트 4개 + 8바이트 카운터, 리틀 엔디언) - `associatedData`: 핸드셰이크 단계에서는 32바이트 해시; 데이터 단계에서는 길이 0 - `plaintext`: 암호화할 데이터(0바이트 이상)

**출력:** - 암호문: 평문과 동일한 길이 - MAC: 16바이트 (Poly1305 인증 태그)

**논스 관리:** - 각 암호 인스턴스마다 카운터는 0에서 시작 - 해당 방향의 각 AEAD 연산마다 증가 - 데이터 단계에서 Alice→Bob 및 Bob→Alice에 대해 별도의 카운터 - 카운터가 2^64 - 1에 도달하기 전에 연결을 종료해야 함

## 메시지 1: SessionRequest(세션 요청)

앨리스가 밥과의 연결을 시작한다.

**Noise 연산**: `e, es` (임시 키 생성 및 교환)

### 원시 형식

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**크기 제한:** - 최소: 80바이트 (32 AES + 48 AEAD) - 최대: 총 65535바이트 - **특수한 경우**: "NTCP" 주소에 연결할 때 최대 287바이트 (버전 감지)

### 복호화된 콘텐츠

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 옵션 블록 (16바이트, 빅 엔디언)

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**중요 필드:** - **네트워크 ID** (since 0.9.42): 네트워크 간 연결을 신속하게 거부 - **m3p2len**: 메시지 3 파트 2의 정확한 크기(전송 시 일치해야 함)

### 키 유도 함수(KDF-1)

**프로토콜 초기화:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**MixHash(혼합 해시) 연산:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**MixKey 동작 (es 패턴):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### 구현 참고 사항

1. **AES 난독화**: DPI(딥 패킷 검사) 회피 목적에만 사용됨; Bob의 router 해시와 IV를 가진 누구나 X를 복호화할 수 있음
2. **재생 공격 방지**: Bob은 최소 2*D초 동안 X 값(또는 암호화된 동등값)을 캐시해야 함 (D = 최대 시계 스큐)
3. **타임스탬프 검증**: Bob은 |tsA - current_time| > D 인 연결을 거부해야 함 (일반적으로 D = 60초)
4. **곡선 검증**: Bob은 X가 유효한 X25519 점인지 검증해야 함
5. **빠른 거부**: 복호화 전에 Bob은 X[31] & 0x80 == 0 여부를 확인할 수 있음 (유효한 X25519 키는 MSB(최상위 비트)가 클리어되어 있음)
6. **오류 처리**: 어떤 실패가 발생해도, 임의의 타임아웃과 임의의 바이트를 읽은 뒤 TCP RST로 연결을 종료함
7. **버퍼링**: 효율을 위해 Alice는 전체 메시지(패딩 포함)를 한 번에 플러시해야 함

## 메시지 2: SessionCreated(세션 생성됨)

Bob이 Alice에게 응답한다.

**Noise 연산**: `e, ee` (ephemeral-ephemeral DH; 일회용-일회용 Diffie-Hellman)

### 원시 형식

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 복호화된 콘텐츠

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 옵션 블록 (16바이트, 빅엔디언)

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### 키 유도 함수(KDF-2)

**MixHash 연산:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**MixKey 연산 (ee pattern, ee 패턴):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**메모리 정리:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### 구현 참고사항

1. **AES 체이닝**: Y 암호화는 메시지 1의 AES-CBC(암호 블록 연쇄 모드) 상태를 사용한다(초기화하지 않음)
2. **재생 공격 방지**: Alice는 최소 2*D초 동안 Y 값을 캐시해야 한다
3. **타임스탬프 검증**: Alice는 |tsB - current_time| > D 인 경우 거부해야 한다
4. **타원곡선 검증**: Alice는 Y가 유효한 X25519(타원곡선 Diffie-Hellman(ECDH) 키 교환 방식) 점인지 확인해야 한다
5. **오류 처리**: 실패가 발생하면 Alice는 TCP RST(연결 재설정 플래그)로 연결을 닫는다
6. **버퍼링**: Bob은 전체 메시지를 한 번에 플러시해야 한다

## 메시지 3: SessionConfirmed(세션 확인)

Alice는 세션을 확인하고 RouterInfo(router 정보)를 전송한다.

**Noise 연산**: `s, se` (정적 키 공개 및 정적-에페메럴 DH)

### 두 부분 구조

메시지 3은 **별도의 AEAD(연관 데이터가 포함된 인증된 암호화) 프레임 두 개**로 구성됩니다:

1. **부분 1**: Alice의 암호화된 정적 키를 포함한 고정된 48바이트 프레임
2. **부분 2**: RouterInfo(라우터 정보), 옵션 및 패딩을 포함한 가변 길이 프레임

### 원시 형식

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**크기 제한:** - 파트 1: 정확히 48바이트 (32바이트 평문 + 16바이트 MAC) - 파트 2: 메시지 1에서 지정된 길이 (m3p2len 필드) - 총 최대: 65535바이트 (파트 1 최대 48, 따라서 파트 2 최대 65487)

### 복호화된 콘텐츠

**파트 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**2부:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### 키 파생 함수(KDF-3)

**파트 1 (s 패턴):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**2부(se 패턴):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**메모리 정리:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### 구현 참고 사항

1. **RouterInfo(라우터 정보) 검증**: Bob은 서명, 타임스탬프, 키의 일관성을 검증해야 한다
2. **키 일치**: Bob은 파트 1에 있는 Alice의 정적 키가 RouterInfo의 키와 일치하는지 검증해야 한다
3. **정적 키 위치**: NTCP 또는 NTCP2 RouterAddress(라우터 주소)에서 일치하는 "s" 매개변수를 찾는다
4. **블록 순서**: RouterInfo는 첫 번째여야 하고, Options는 두 번째(있는 경우), Padding은 마지막(있는 경우)이어야 한다
5. **길이 계획**: Alice는 메시지 1의 m3p2len이 파트 2 길이와 정확히 일치하도록 해야 한다
6. **버퍼링**: Alice는 두 파트를 하나의 TCP 전송으로 함께 보내도록 플러시해야 한다
7. **선택적 체이닝**: 효율을 위해 Alice는 즉시 data phase frame(데이터 단계 프레임)을 이어붙일 수 있다

## 데이터 단계

핸드셰이크가 완료된 후에는 모든 메시지가 난독화된 길이 필드를 가진 가변 길이 AEAD(연관 데이터가 포함된 인증 암호화) 프레임을 사용합니다.

### 키 파생 함수(데이터 단계)

**Split 함수(Noise 프로토콜):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**SipHash 키 파생:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### 프레임 구조

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**프레임 제약 조건:** - 최소: 18바이트 (2바이트 난독화된 길이 + 0바이트 평문 + 16바이트 MAC(메시지 인증 코드)) - 최대: 65537바이트 (2바이트 난독화된 길이 + 65535바이트 프레임) - 권장: 프레임당 수 KB (수신 지연을 최소화)

### SipHash 길이 난독화

**목적**: DPI(딥 패킷 검사)가 프레임 경계를 식별하는 것을 방지

**알고리즘:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**디코딩:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**참고:** - 각 방향(Alice→Bob 및 Bob→Alice)에 대해 별도의 IV(초기화 벡터) 체인을 사용 - SipHash가 uint64를 반환하는 경우, 최하위 2바이트를 마스크로 사용 - uint64를 little-endian 바이트로 변환하여 다음 IV로 사용

### 블록 형식

각 프레임에는 0개 이상의 블록이 포함됩니다:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**크기 제한:** - 최대 프레임: 65535 바이트 (MAC 포함) - 최대 블록 공간: 65519 바이트 (프레임 - 16바이트 MAC) - 최대 단일 블록: 65519 바이트 (3바이트 헤더 + 65516바이트 데이터)

### 블록 유형

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**블록 순서 규칙:** - **메시지 3 파트 2**: RouterInfo(라우터 정보), 옵션 (선택 사항), 패딩 (선택 사항) - 다른 유형은 없음 - **데이터 단계**: 다음 예외를 제외하고 임의 순서:   - 패딩은 존재하는 경우 반드시 마지막 블록이어야 함   - 종료는 존재하는 경우(패딩 제외) 반드시 마지막 블록이어야 함 - 프레임당 I2NP 블록 여러 개 허용 - 프레임당 패딩 블록 여러 개는 허용되지 않음

### 블록 유형 0: DateTime

clock skew(클록 간 시간 불일치) 감지를 위한 시간 동기화.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**구현**: 시계 오차 누적을 방지하기 위해 가장 가까운 초로 반올림합니다.

### 블록 유형 1: 옵션

패딩 및 트래픽 셰이핑 매개변수.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**패딩 비율** (4.4 고정소수점 값, value/16.0): - `tmin`: 송신 최소 패딩 비율 (0.0 - 15.9375) - `tmax`: 송신 최대 패딩 비율 (0.0 - 15.9375) - `rmin`: 수신 최소 패딩 비율 (0.0 - 15.9375) - `rmax`: 수신 최대 패딩 비율 (0.0 - 15.9375)

**예시:** - 0x00 = 0% 패딩 - 0x01 = 6.25% 패딩 - 0x10 = 100% 패딩 (1:1 비율) - 0x80 = 800% 패딩 (8:1 비율)

**더미 트래픽:** - `tdmy`: 보내기를 허용하는 최대치 (2바이트, 초당 바이트 평균) - `rdmy`: 수신 요청치 (2바이트, 초당 바이트 평균)

**지연 삽입:** - `tdelay`: 삽입하려는 최대치 (2바이트, 밀리초 평균) - `rdelay`: 요청된 지연 (2바이트, 밀리초 평균)

**지침:** - 최소값은 원하는 트래픽 분석 저항성을 나타낸다 - 최대값은 대역폭 제약을 나타낸다 - 송신자는 수신자의 최대값을 존중해야 한다 - 송신자는 제약 내에서 수신자의 최소값을 존중할 수 있다 - 강제 메커니즘은 없음; 구현은 달라질 수 있음

### 블록 유형 2: RouterInfo

netdb 구축 및 flooding(브로드캐스트식 전파)을 위한 RouterInfo 배포.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**사용법:**

**메시지 3 파트 2에서** (핸드셰이크): - Alice가 자신의 RouterInfo(라우터 정보)를 Bob에게 보냄 - Flood bit는 보통 0(로컬 저장) - RouterInfo는 gzip으로 압축되지 않음

**데이터 단계에서:** - 양측 중 어느 한쪽은 업데이트된 RouterInfo를 보낼 수 있음 - Flood bit(플러드 비트) = 1: floodfill 배포를 요청(수신자가 floodfill인 경우) - Flood bit = 0: 로컬 netdb 저장만

**검증 요구 사항:** 1. 서명 유형이 지원되는지 확인 2. RouterInfo 서명 확인 3. 타임스탬프가 허용 범위 내에 있는지 확인 4. 핸드셰이크의 경우: 정적 키가 NTCP2 주소의 "s" 매개변수와 일치하는지 확인 5. 데이터 단계의 경우: router 해시가 세션 피어와 일치하는지 확인 6. 공개된 주소가 있는 RouterInfos만 전파

**참고:** - ACK 메커니즘 없음(필요한 경우 reply token(응답 토큰)과 함께 I2NP DatabaseStore 사용) - 제3자 RouterInfos(라우터 정보)를 포함할 수 있음(floodfill 사용) - gzip으로 압축되지 않음(I2NP DatabaseStore와 달리)

### 블록 유형 3: I2NP 메시지

축약된 9바이트 헤더를 가진 I2NP 메시지.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**NTCP1과의 차이점:** - 만료 시각: 4바이트(초) vs 8바이트(밀리초) - 길이: 생략됨(블록 길이에서 도출 가능) - 체크섬: 생략됨(AEAD가 무결성을 제공) - 헤더: 9바이트 vs 16바이트(44% 감소)

**단편화:** - I2NP 메시지는 블록 간 분할되어서는 안 됩니다 - I2NP 메시지는 프레임 간 분할되어서는 안 됩니다 - 프레임당 여러 I2NP 블록이 허용됩니다

### 블록 유형 4: 종료

사유 코드를 포함한 명시적 연결 종료.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**사유 코드:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**규칙:** - 종료 블록은 프레임 내에서 패딩이 아닌 마지막 블록이어야 함 - 프레임당 종료 블록은 최대 1개 - 송신자는 전송 후 연결을 닫는 것이 바람직함 - 수신자는 수신 후 연결을 닫는 것이 바람직함

**오류 처리:** - 핸드셰이크 오류: 일반적으로 TCP RST로 종료(종료 블록 없음) - 데이터 단계 AEAD 오류: 무작위 타임아웃 + 무작위 읽기, 그런 다음 종료 전송 - 보안 절차는 "AEAD Error Handling" 섹션을 참조하십시오

### 블록 유형 254: 패딩

트래픽 분석 저항성을 위한 무작위 패딩.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**규칙:** - 패딩이 존재하는 경우 프레임 내에서 마지막 블록이어야 함 - 길이가 0인 패딩은 허용됨 - 프레임당 패딩 블록은 하나만 허용됨 - 패딩만 있는 프레임은 허용됨 - Options 블록에서 협상된 매개변수를 준수해야 함

**메시지 1-2의 패딩:** - AEAD(연관 데이터가 있는 인증된 암호화) 프레임 바깥(평문) - 다음 메시지의 해시 체인에 포함됨(인증됨) - 다음 메시지의 AEAD가 실패하면 변조가 탐지됨

**메시지 3+ 및 데이터 단계의 패딩:** - AEAD 프레임 내부(암호화 및 인증됨) - 트래픽 셰이핑과 크기 은폐에 사용됨

## AEAD 오류 처리

**핵심 보안 요구사항:**

### 핸드셰이크 단계 (메시지 1-3)

**알려진 메시지 크기:** - 메시지 크기는 미리 정해지거나 사전에 지정됨 - AEAD(연관 데이터가 있는 인증 암호화) 인증 실패는 모호하지 않음

**Bob의 메시지 1 실패에 대한 대응:** 1. 임의의 타임아웃 설정(범위는 구현에 따라 다름, 권장 100–500ms) 2. 임의의 바이트 수 읽기(범위는 구현에 따라 다름, 권장 1KB–64KB) 3. TCP RST로 연결 종료(응답 없이) 4. 소스 IP를 일시적으로 차단 목록에 추가 5. 장기 차단을 위해 반복된 실패를 추적

**메시지 2 실패에 대한 Alice의 대응:** 1. TCP RST로 즉시 연결을 종료 2. Bob에게 응답하지 않음

**메시지 3 실패에 대한 Bob의 응답:** 1. TCP RST(TCP 재설정)로 즉시 연결 종료 2. Alice에게 응답 없음

### 데이터 단계

**난독화된 메시지 크기:** - 길이 필드는 SipHash(경량 MAC 함수)로 난독화됨 - 잘못된 길이이거나 AEAD(연관 데이터가 있는 인증된 암호화) 실패는 다음을 의미할 수 있음:   - 공격자 프로빙(탐색)   - 네트워크 손상   - 비동기화된 SipHash IV(초기화 벡터)   - 악의적인 피어

**AEAD(연관 데이터가 있는 인증 암호화) 또는 길이 오류에 대한 응답:** 1. 임의의 타임아웃을 설정한다 (권장 100-500ms) 2. 임의의 바이트 수를 읽는다 (권장 1KB-64KB) 3. 사유 코드 4(AEAD 실패) 또는 9(프레이밍 오류)가 포함된 종료 블록을 전송한다 4. 연결을 종료한다

**복호화 오라클 방지:** - 임의의 타임아웃이 지나기 전에는 피어에게 오류 유형을 절대 공개하지 말 것 - AEAD(연관 데이터 인증 암호화) 검사를 수행하기 전에 길이 검증을 절대로 건너뛰지 말 것 - 유효하지 않은 길이는 AEAD 실패와 동일하게 취급할 것 - 두 오류 모두에 대해 동일한 오류 처리 경로를 사용할 것

**구현 시 고려사항:** - AEAD(인증된 연관 데이터 암호화) 오류가 드물다면 일부 구현은 계속 진행할 수 있음 - 반복적으로 오류가 발생할 경우 종료 (권장 임계값: 시간당 3-5회 오류) - 오류 복구와 보안 간 균형 유지

## 게시된 RouterInfo

### Router 주소 형식

NTCP2 지원 여부는 특정 옵션이 포함된 공개된 RouterAddress 항목을 통해 고지됩니다.

**전송 방식:** - `"NTCP2"` - 이 포트에서 NTCP2만 사용 - `"NTCP"` - 이 포트에서 NTCP와 NTCP2 모두 사용(자동 감지)   - **참고**: NTCP (v1) 지원은 0.9.50(2021년 5월)에서 제거됨   - "NTCP" 스타일은 이제 사용 중단됨; "NTCP2"를 사용하세요

### 필수 옵션

**모든 공개된 NTCP2 주소:**

1. **`host`** - IP 주소(IPv4 또는 IPv6) 또는 호스트 이름
   - 형식: 표준 IP 표기법 또는 도메인 이름
   - 아웃바운드 전용 또는 숨겨진 router의 경우 생략할 수 있음

2. **`port`** - TCP 포트 번호
   - 형식: 정수, 1-65535
   - 아웃바운드 전용 또는 숨겨진 router에서는 생략될 수 있음

3. **`s`** - 정적 공개 키 (X25519)
   - 형식: Base64 인코딩, 44자
   - 인코딩: I2P Base64 알파벳
   - 원본: 32바이트 X25519 공개 키, little-endian(리틀 엔디언)

4. **`i`** - AES용 초기화 벡터(IV)
   - 형식: Base64로 인코딩된, 24자
   - 인코딩: I2P Base64 알파벳
   - 원본: 16바이트 IV, 빅엔디언

5. **`v`** - 프로토콜 버전
   - 형식: 정수 또는 쉼표로 구분된 정수들
   - 현재: `"2"`
   - 향후: `"2,3"` (숫자 순서여야 함)

**선택적 옵션:**

6. **`caps`** - Capabilities(기능) (0.9.50부터)
   - 형식: capability 문자로 이루어진 문자열
   - 값:
     - `"4"` - IPv4 아웃바운드 기능
     - `"6"` - IPv6 아웃바운드 기능
     - `"46"` - IPv4와 IPv6 모두 (권장 순서)
   - `host`가 공개된 경우 필요 없음
   - 숨겨진/방화벽 뒤에 있는 routers에 유용함

7. **`cost`** - 주소 우선순위
   - 형식: 정수, 0-255
   - 값이 낮을수록 = 우선순위가 높음
   - 권장: 일반 주소의 경우 5-10
   - 권장: 미공개 주소의 경우 14

### RouterAddress 엔트리 예시

**공개된 IPv4 주소:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**숨겨진 Router (아웃바운드 전용):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**듀얼 스택 Router:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**중요 규칙:** - **동일한 포트**를 사용하는 여러 NTCP2 주소는 `s`, `i`, `v` 값이 반드시 **동일해야** 합니다 - 서로 다른 포트는 서로 다른 키를 사용할 수 있습니다 - 듀얼스택 router는 IPv4와 IPv6 주소를 별도로 게시해야 합니다

### 공개되지 않은 NTCP2 주소

**아웃바운드 전용 Routers의 경우:**

router가 수신 NTCP2 연결을 허용하지 않지만 송신 연결은 개시하는 경우에도, 여전히 다음을 포함하는 RouterAddress(라우터 주소 정보)를 발행해야 한다:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**목적:** - 핸드셰이크 중 Bob이 Alice의 정적 키를 검증할 수 있도록 함 - 메시지 3 파트 2의 RouterInfo 검증에 필요 - `i`, `host`, `port`가 필요 없음 (아웃바운드 전용)

**대안:** - 기존에 공개된 "NTCP" 또는 SSU 주소에 `s`와 `v`를 추가합니다

### 공개 키 및 IV(초기화 벡터) 로테이션

**중요 보안 정책:**

**일반 규칙:** 1. **router가 실행 중일 때는 절대 rotate(교체)하지 마십시오** 2. **키와 IV(초기화 벡터)를 영구적으로 저장** 재시작 간에도 3. **이전 다운타임을 추적** rotation 적용 가능 여부를 판단하기 위해

**로테이션 전에 필요한 최소 다운타임:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**추가 트리거:** - 로컬 IP 주소 변경: 다운타임 여부와 상관없이 변경될 수 있음 - Router "rekey" (새 Router Hash): 새 키 생성

**근거:** - 키 변경을 통해 재시작 시간을 노출하는 것을 방지 - 캐시된 RouterInfos(라우터 정보 객체)가 자연스럽게 만료되도록 허용 - 네트워크 안정성을 유지 - 실패한 연결 시도를 줄임

**구현:** 1. 키, IV(초기화 벡터), 마지막 종료 타임스탬프를 영구적으로 저장한다 2. 시작 시, downtime 값을 current_time - last_shutdown으로 계산한다 3. downtime가 router 유형의 최소값을 초과하면 키를 교체할 수 있다 4. IP가 변경되었거나 rekeying(키를 다시 생성하는 작업)이면 키를 교체할 수 있다 5. 그렇지 않으면 이전 키와 IV를 재사용한다

**IV 회전:** - 키 회전과 동일한 규칙이 적용됨 - 공개된 주소에만 존재함 (숨겨진 routers에는 해당 없음) - 키가 변경될 때마다 IV를 변경할 것을 권장

## 버전 감지

**맥락:** `transportStyle="NTCP"` (레거시)인 경우, Bob은 동일한 포트에서 NTCP v1과 v2를 모두 지원하며 프로토콜 버전을 자동으로 감지해야 합니다.

**탐지 알고리즘:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**빠른 MSB 검사:** - AES 복호화 전에 다음을 확인: `encrypted_X[31] & 0x80 == 0` - 유효한 X25519 키는 최상위 비트가 클리어되어 있음 - 실패 시 NTCP1(또는 공격)일 가능성이 높음 - 실패 시 probing resistance(탐침 방어) 구현(무작위 타임아웃 + 읽기)

**구현 요구 사항:**

1. **Alice의 책임:**
   - "NTCP" 주소에 연결할 때, 메시지 1의 크기를 최대 287바이트로 제한
   - 메시지 1 전체를 버퍼링하고 한 번에 플러시
   - 단일 TCP 패킷으로 전송될 가능성을 높임

2. **Bob의 책임:**
   - 버전을 판별하기 전에 수신된 데이터를 버퍼링할 것
   - 적절한 타임아웃 처리를 구현할 것
   - 빠른 버전 판별을 위해 TCP_NODELAY(Nagle algorithm 비활성화 옵션)을 사용할 것
   - 버전 판별 후 메시지 2 전체를 버퍼에 모아 한 번에 플러시할 것

**보안 고려사항:** - 세그멘테이션 공격: Bob은 TCP 세그멘테이션에 내성이 있어야 함 - 프로빙 공격: 실패 시 무작위 지연과 바이트 읽기를 구현 - DoS 방지: 대기 중인 동시 연결 수를 제한 - 읽기 타임아웃: 개별 읽기와 전체 둘 다 ("slowloris"(연결을 길게 유지하며 요청을 지연시켜 자원을 고갈시키는 공격) 방어)

## 시계 오차 지침

**타임스탬프 필드:** - 메시지 1: `tsA` (Alice의 타임스탬프) - 메시지 2: `tsB` (Bob의 타임스탬프) - 메시지 3+: 선택적 DateTime 블록

**최대 시간 오차(D):** - 일반적: **±60초** - 구현별로 설정 가능 - 시간 오차 > D는 일반적으로 치명적임

### Bob의 처리 (메시지 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**이유:** skew(클록 오차) 상태에서도 메시지 2를 보내면 Alice가 클록 문제를 진단할 수 있다.

### 앨리스의 처리 (메시지 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**RTT 조정:** - 계산된 스큐(시간 편차)에서 RTT의 절반을 빼기 - 네트워크 전파 지연을 반영 - 더 정확한 스큐 추정

### Bob의 처리 (메시지 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### 시간 동기화

**DateTime 블록(데이터 단계):** - 주기적으로 DateTime 블록 전송 (type 0) - 수신자는 시계 조정에 사용할 수 있음 - 타임스탬프를 가장 가까운 초로 반올림 (편향 방지)

**외부 시간 소스:** - NTP(네트워크 시간 프로토콜) - 시스템 시계 동기화 - I2P 네트워크 합의 시간

**클록 조정 전략:** - 로컬 클록이 잘못된 경우: 시스템 시간을 조정하거나 오프셋 사용 - 피어 클록이 지속적으로 잘못된 경우: 피어 문제로 플래그 지정 - 네트워크 건전성 모니터링을 위해 clock skew(시간 오차) 통계를 추적

## 보안 속성

### 순방향 기밀성

**다음 방식으로 달성:** - 임시 Diffie-Hellman 키 교환 (X25519) - 세 가지 DH 연산: es, ee, se (Noise XK pattern: Noise 프로토콜의 XK 패턴) - 핸드셰이크 완료 후 임시 키 파기

**기밀성 진행:** - 메시지 1: 레벨 2 (발신자 키 유출 시 forward secrecy(순방향 보안)) - 메시지 2: 레벨 1 (임시 수신자) - 메시지 3+: 레벨 5 (강력한 forward secrecy)

**완전 순방향 기밀성(Perfect Forward Secrecy, PFS):** - 장기 정적 키가 유출되어도 과거 세션 키는 공개되지 않습니다 - 각 세션은 고유한 임시 키를 사용합니다 - 임시 개인 키는 절대 재사용하지 않습니다 - 키 합의 후 메모리 정리

**제한 사항:** - Bob의 정적 키가 탈취되면 메시지 1은 취약해진다(단, Alice가 침해되더라도 Forward Secrecy(전방향 기밀성)은 유지됨) - 메시지 1에 대해 재전송 공격 가능(타임스탬프와 재전송 캐시로 완화됨)

### 인증

**상호 인증:** - Alice는 메시지 3의 정적 키로 인증됨 - Bob은 정적 개인 키를 보유함으로써 인증됨 (성공적인 핸드셰이크에서 암시됨)

**Key Compromise Impersonation (KCI, 키 손상에 의한 사칭) 저항성:** - 인증 레벨 2 (KCI에 내성) - 공격자는 Alice의 정적 개인 키만으로는 (Alice의 임시 키 없이) Alice를 사칭할 수 없음 - 공격자는 Bob의 정적 개인 키만으로는 (Bob의 임시 키 없이) Bob을 사칭할 수 없음

**정적 키 검증:** - Alice는 Bob의 정적 키를 미리 알고 있음(RouterInfo(라우터 정보)에서) - Bob은 메시지 3에서 Alice의 정적 키가 RouterInfo와 일치하는지 검증함 - 중간자 공격을 방지함

### 트래픽 분석에 대한 저항성

**DPI(딥 패킷 검사) 대응책:** 1. **AES 난독화:** 임시 키가 암호화되어 무작위처럼 보임 2. **SipHash 길이 난독화:** 프레임 길이는 평문이 아님 3. **무작위 패딩:** 메시지 크기가 가변적이며, 고정된 패턴이 없음 4. **암호화된 프레임:** 모든 페이로드는 ChaCha20으로 암호화됨

**리플레이(재전송) 공격 방지:** - 타임스탬프 검증(±60초) - ephemeral 키에 대한 replay 캐시(수명 2*D) - Nonce(일회용 임의값) 증가로 세션 내 패킷 재전송을 방지

**프로빙 저항성:** - AEAD(부가 데이터가 포함된 인증된 암호화) 실패 시 임의의 타임아웃 - 연결 종료 전에 임의의 바이트 읽기 - 핸드셰이크 실패 시 응답 없음 - 반복된 실패 시 IP 블랙리스트 등재

**패딩 지침:** - 메시지 1-2: 평문 패딩(인증됨) - 메시지 3+: AEAD(연관 데이터가 포함된 인증 암호) 프레임 내부의 암호화된 패딩 - 협상된 패딩 매개변수(Options 블록) - 패딩 전용 프레임 허용됨

### 서비스 거부(DoS) 완화

**연결 제한:** - 최대 활성 연결 수(구현에 따라 다름) - 대기 중인 핸드셰이크의 최대치(예: 100-1000) - IP당 연결 제한(예: 동시 3-10개)

**리소스 보호:** - DH 연산 속도 제한 (비용이 큼) - 소켓별 및 전체 읽기 타임아웃 - "Slowloris" 보호 (총 시간 제한) - 남용 방지를 위한 IP 블랙리스트

**빠른 거부:** - Network ID 불일치 → 즉시 종료 - 유효하지 않은 X25519 point(타원 곡선 X25519의 점) → 복호화 전에 빠른 최상위 비트(MSB) 검사 - 범위를 벗어난 타임스탬프 → 연산 없이 종료 - AEAD 실패 → 응답 없음, 무작위 지연

**프로빙 저항성:** - 임의 타임아웃: 100-500ms (구현에 따라 다름) - 임의 읽기: 1KB-64KB (구현에 따라 다름) - 공격자에게 오류 정보를 제공하지 않음 - TCP RST로 종료 (FIN 핸드셰이크 없음)

### 암호학적 보안

**알고리즘:** - **X25519**: 128비트 보안 강도, 타원곡선 DH (Curve25519) - **ChaCha20**: 256비트 키를 사용하는 스트림 암호 - **Poly1305**: 정보이론적으로 안전한 MAC - **SHA-256**: 128비트 충돌 저항성, 256비트 전이미지 저항성 - **HMAC-SHA256**: 키 파생용 PRF(의사난수 함수)

**키 크기:** - 정적 키: 32 바이트 (256 비트) - 임시 키: 32 바이트 (256 비트) - 암호화 키: 32 바이트 (256 비트) - MAC: 16 바이트 (128 비트)

**알려진 문제:** - ChaCha20 논스 재사용은 치명적입니다 (카운터 증가로 방지됨) - X25519에는 작은 부분군 문제가 있습니다 (곡선 검증으로 완화됨) - SHA-256은 이론적으로 길이 확장 공격에 취약합니다 (HMAC에서는 악용되지 않음)

**알려진 취약점 없음(2025년 10월 기준):** - Noise Protocol Framework(노이즈 프로토콜 프레임워크) 광범위하게 분석됨 - ChaCha20-Poly1305 TLS 1.3에 채택됨 - X25519 최신 프로토콜에서 표준 - 구성에 대한 실질적인 공격 없음

## 참고 자료

### 주요 명세

- **[NTCP2 명세](/docs/specs/ntcp2/)** - 공식 I2P 명세 문서
- **[Proposal 111](/proposals/111-ntcp-2/)** - 설계 근거를 담은 원래 설계 문서
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** (노이즈 프로토콜 프레임워크) - 리비전 33 (2017-10-04)

### 암호화 표준

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - 보안용 타원 곡선 (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - IETF 프로토콜용 ChaCha20 및 Poly1305
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (RFC 7539를 대체함)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: 메시지 인증을 위한 키 기반 해시
- **[SipHash](https://www.131002.net/siphash/)** - 해시 함수 응용을 위한 SipHash-2-4

### 관련 I2P 명세

- **[I2NP 사양](/docs/specs/i2np/)** - I2P 네트워크 프로토콜 메시지 형식
- **[공통 구조체](/docs/specs/common-structures/)** - RouterInfo, RouterAddress 형식
- **[SSU 전송](/docs/legacy/ssu/)** - UDP 전송(원래 버전, 현재는 SSU2)
- **[제안 147](/proposals/147-transport-network-id-check/)** - 전송 네트워크 ID 확인(0.9.42)

### 구현 참고 자료

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - 참조 구현(Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - C++ 구현
- **[I2P 릴리스 노트](/blog/)** - 버전 기록 및 업데이트

### 역사적 맥락

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Noise 프레임워크의 영감이 된
- **[obfs4](https://gitlab.com/yawning/obfs4)** - 플러그형 트랜스포트 (SipHash 길이 난독화의 선례)

## 구현 지침

### 필수 요구 사항

**규정 준수를 위해:**

1. **완전한 핸드셰이크 구현:**
   - 올바른 KDF(키 파생 함수) 체인을 사용해 세 가지 메시지 모두 지원
   - 모든 AEAD(연관 데이터가 있는 인증된 암호화) 태그를 검증
   - X25519(ECDH 키 교환) 점이 유효한지 확인

2. **데이터 단계 구현:**
   - SipHash 길이 난독화 (양방향)
   - 모든 블록 타입: 0 (날짜/시간), 1 (옵션), 2 (RouterInfo), 3 (I2NP), 4 (종료), 254 (패딩)
   - 적절한 nonce(일회용 값) 관리 (분리된 카운터)

3. **보안 기능:**
   - 재생 공격 방지(2*D 동안 임시 키 캐시)
   - 타임스탬프 검증(기본값 ±60초)
   - 메시지 1-2에 무작위 패딩
   - 무작위 타임아웃을 사용하는 AEAD(부가 데이터가 포함된 인증된 암호화) 오류 처리

4. **RouterInfo(라우터 정보를 담는 데이터 구조) 게시:**
   - 정적 키 ("s"), IV ("i", 초기화 벡터) 및 버전 ("v")을 게시
   - 정책에 따라 키를 순환 교체
   - 숨겨진 router용 capabilities 필드 ("caps") 지원

5. **네트워크 호환성:**
   - 네트워크 ID 필드 지원(현재 메인넷에서는 2)
   - 기존 Java 및 i2pd 구현과 상호 운용
   - IPv4와 IPv6 모두 지원

### 권장 사항

**성능 최적화:**

1. **버퍼링 전략:**
   - 전체 메시지를 한 번에 플러시 (메시지 1, 2, 3)
   - 핸드셰이크 메시지에는 TCP_NODELAY 사용
   - 여러 데이터 블록을 단일 프레임으로 버퍼링
   - 프레임 크기를 몇 KB로 제한 (수신 측 지연시간 최소화)

2. **연결 관리:**
   - 가능한 경우 연결을 재사용하세요
   - 연결 풀링을 구현하세요
   - 연결 상태를 모니터링하세요 (DateTime blocks)

3. **메모리 관리:**
   - 사용 후 민감 데이터를 0으로 덮어쓰기(임시 키, DH 결과)
   - 동시 핸드셰이크 제한(DoS(서비스 거부) 방지)
   - 빈번한 할당에는 메모리 풀 사용

**보안 강화:**

1. **프로빙 저항성:**
   - 무작위 타임아웃: 100-500ms
   - 무작위 바이트 읽기: 1KB-64KB
   - 반복적인 실패 시 IP 블랙리스트 추가
   - 피어에게 오류 세부 정보를 제공하지 않음

2. **리소스 제한:**
   - IP당 최대 연결 수: 3-10
   - 대기 중인 핸드셰이크 최대 수: 100-1000
   - 읽기 타임아웃: 작업당 30-60초
   - 전체 연결 타임아웃: 핸드셰이크 완료까지 5분

3. **키 관리:**
   - 정적 키와 IV(초기화 벡터)의 영구 저장
   - 보안 난수 생성(암호학적 난수 생성기)
   - 키 로테이션 정책 엄수
   - 임시 키 절대 재사용 금지

**모니터링 및 진단:**

1. **지표:**
   - 핸드셰이크 성공/실패 비율
   - AEAD(Authenticated Encryption with Associated Data, 인증된 연계 데이터 암호화) 오류율
   - 시계 오차 분포
   - 연결 지속 시간 통계

2. **로깅:**
   - 이유 코드와 함께 핸드셰이크 실패를 로그에 기록
   - clock skew(시계 오차) 이벤트를 로그에 기록
   - 차단된 IP 주소를 로그에 기록
   - 민감한 키 재료는 절대로 로그에 기록하지 말 것

3. **테스트:**
   - KDF(키 파생 함수) 체인에 대한 단위 테스트
   - 다른 구현과의 통합 테스트
   - 패킷 처리용 퍼징
   - DoS(서비스 거부) 내성에 대한 부하 테스트

### 자주 하는 실수

**피해야 할 치명적인 오류:**

1. **Nonce(일회용 난수 값) 재사용:**
   - 세션 중간에 nonce 카운터를 절대 초기화하지 말 것
   - 송신/수신 각각에 대해 별도의 카운터를 사용할 것
   - 2^64 - 1에 도달하기 전에 세션을 종료할 것

2. **키 로테이션:**
   - router가 실행 중일 때는 키를 절대 교체(로테이션)하지 마십시오
   - 세션 간에 임시 키를 절대 재사용하지 마십시오
   - 최소 다운타임 규칙을 준수하십시오

3. **타임스탬프 처리:**
   - 만료된 타임스탬프는 절대 허용하지 않는다
   - 편차를 계산할 때는 항상 RTT(왕복 지연 시간)를 보정한다
   - DateTime 타임스탬프는 초 단위로 반올림한다

4. **AEAD(연관 데이터가 있는 인증된 암호화) 오류:**
   - 공격자에게 오류 유형을 절대 공개하지 말 것
   - 닫기 전에 항상 무작위 타임아웃을 사용할 것
   - 잘못된 길이는 AEAD 실패와 동일하게 처리할 것

5. **패딩:**
   - 합의된 범위를 벗어난 패딩은 절대 전송하지 않는다
   - 패딩 블록은 항상 마지막에 배치한다
   - 프레임당 여러 개의 패딩 블록을 절대 포함하지 않는다

6. **RouterInfo:**
   - 항상 정적 키가 RouterInfo와 일치하는지 확인하세요
   - 공개된 주소가 없는 RouterInfos는 절대 flood(대량 전파)하지 마세요
   - 항상 서명을 검증하세요

### 테스트 방법론

**단위 테스트:**

1. **암호학 기본 구성 요소:**
   - X25519, ChaCha20, Poly1305, SHA-256용 테스트 벡터
   - HMAC-SHA256 테스트 벡터
   - SipHash-2-4 테스트 벡터

2. **KDF 체인:**
   - 세 가지 메시지 모두에 대한 정답(known-answer) 테스트
   - 체이닝 키 전파 검증
   - SipHash IV 생성 테스트

3. **메시지 파싱:**
   - 유효한 메시지 디코딩
   - 잘못된 메시지 거부
   - 경계 조건(빈 입력, 최대 크기)

**통합 테스트:**

1. **핸드셰이크:**
   - 3-메시지 교환 성공
   - 시계 오차 거부
   - 리플레이 공격 감지
   - 유효하지 않은 키 거부

2. **데이터 단계:**
   - I2NP 메시지 전송
   - RouterInfo(router 정보) 교환
   - 패딩 처리
   - 종료 메시지

3. **상호운용성:**
   - Java I2P와의 상호운용성 테스트
   - i2pd와의 상호운용성 테스트
   - IPv4 및 IPv6 테스트
   - 공개된 및 숨겨진 router 테스트

**보안 테스트:**

1. **네거티브 테스트:**
   - 유효하지 않은 AEAD 태그
   - 리플레이된 메시지
   - Clock skew(시계 오차) 공격
   - 비정상 형식의 프레임

2. **DoS 테스트:**
   - 연결 플러딩
   - Slowloris 공격(느린 전송으로 연결을 붙잡아 두는 기법)
   - CPU 고갈(과도한 DH(디피-헬만) 연산)
   - 메모리 고갈

3. **퍼징:**
   - 무작위 핸드셰이크 메시지
   - 무작위 데이터 단계 프레임
   - 무작위 블록 유형과 크기
   - 유효하지 않은 암호학적 값

### NTCP에서의 마이그레이션

**레거시 NTCP 지원(현재 제거됨):**

I2P 0.9.50 (2021년 5월)에서 NTCP (버전 1, I2P 전송 프로토콜)가 제거되었습니다. 현재 모든 구현체는 NTCP2를 지원해야 합니다. 역사적 참고 사항:

1. **전환 기간(2018-2021):**
   - 0.9.36: NTCP2 도입(기본적으로 비활성화)
   - 0.9.37: NTCP2 기본적으로 활성화
   - 0.9.40: NTCP 사용 중단
   - 0.9.50: NTCP 제거

2. **버전 감지:**
   - "NTCP" transportStyle는 두 버전을 모두 지원함을 나타냄
   - "NTCP2" transportStyle는 NTCP2만 지원함을 나타냄
   - 메시지 크기를 통해 자동 감지(287 대 288 바이트)

3. **현재 상태:**
   - 모든 routers는 NTCP2를 지원해야 합니다
   - "NTCP" transportStyle(전송 스타일)은 더 이상 사용되지 않습니다
   - "NTCP2" transportStyle만 사용하십시오

## 부록 A: Noise XK Pattern(Noise 프로토콜의 XK 패턴)

**표준 Noise XK Pattern(Noise 프로토콜 프레임워크의 XK 패턴):**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**해석:**

- `<-` : 응답자(Bob)에서 개시자(Alice)로의 메시지
- `->` : 개시자(Alice)에서 응답자(Bob)로의 메시지
- `s` : 정적 키(장기 식별 키)
- `rs` : 원격 정적 키(피어의 정적 키, 사전에 알고 있음)
- `e` : 임시 키(세션별, 필요 시 생성)
- `es` : 임시-정적 DH (Alice 임시 × Bob 정적)
- `ee` : 임시-임시 DH (Alice 임시 × Bob 임시)
- `se` : 정적-임시 DH (Alice 정적 × Bob 임시)

**키 합의 절차:**

1. **사전 메시지:** Alice는 Bob의 정적 공개키를 알고 있음(RouterInfo에서)
2. **메시지 1:** Alice는 임시 키를 전송하고 es DH를 수행
3. **메시지 2:** Bob은 임시 키를 전송하고 ee DH를 수행
4. **메시지 3:** Alice는 정적 키를 공개하고 se DH를 수행

**보안 속성:**

- Alice 인증됨: 예 (메시지 3에 의해)
- Bob 인증됨: 예 (정적 개인 키를 보유함으로써)
- 전방향 기밀성: 예 (임시 키가 파기됨)
- KCI 저항성(키 손상 가장 공격에 대한 저항성): 예 (인증 수준 2)

## 부록 B: Base64 인코딩

**I2P Base64 알파벳:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**표준 Base64와의 차이점:** - 문자 62-63: `+/` 대신 `-~` - 패딩: 동일함 (`=`) 또는 문맥에 따라 생략

**NTCP2에서의 사용:** - 정적 키 ("s"): 32바이트 → 44문자 (패딩 없음) - IV ("i"): 16바이트 → 24문자 (패딩 없음)

**인코딩 예시:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## 부록 C: 패킷 캡처 분석

**NTCP2 트래픽 식별:**

1. **TCP 핸드셰이크:**
   - 표준 TCP SYN, SYN-ACK, ACK
   - 목적지 포트는 보통 8887 또는 비슷한 포트

2. **메시지 1 (SessionRequest):**
   - Alice가 보낸 첫 애플리케이션 데이터
   - 80-65535 바이트 (일반적으로 수백 바이트)
   - 무작위처럼 보임 (AES로 암호화된 임시 키)
   - "NTCP" 주소에 연결하는 경우 최대 287 바이트

3. **메시지 2 (SessionCreated):**
   - Bob의 응답
   - 80-65535바이트(일반적으로 수백 바이트)
   - 또한 무작위로 보입니다

4. **메시지 3 (SessionConfirmed(세션 확인)):**
   - Alice로부터
   - 48바이트 + 가변 길이(RouterInfo(router 정보 구조체) 크기 + 패딩)
   - 보통 1~4 KB

5. **데이터 단계:**
   - 가변 길이 프레임
   - 길이 필드 난독화(무작위처럼 보임)
   - 암호화된 페이로드
   - 패딩으로 인해 크기를 예측할 수 없음

**DPI(딥 패킷 검사) 우회:** - 평문 헤더 없음 - 고정된 패턴 없음 - 길이 필드 난독화 - 무작위 패딩으로 크기 기반 휴리스틱 무력화

**NTCP와의 비교:** - NTCP 메시지 1은 항상 288바이트(식별 가능) - NTCP2 메시지 1의 크기는 가변적임(식별 불가) - NTCP에는 식별 가능한 패턴이 있었음 - NTCP2는 DPI(딥 패킷 검사)에 저항하도록 설계됨

## 부록 D: 버전 이력

**주요 이정표:**

- **0.9.36** (2018년 8월 23일): NTCP2 도입, 기본값으로 비활성화
- **0.9.37** (2018년 10월 4일): NTCP2 기본값으로 활성화
- **0.9.40** (2019년 5월 20일): NTCP 사용 중단
- **0.9.42** (2019년 8월 27일): 네트워크 ID 필드 추가(제안 147)
- **0.9.50** (2021년 5월 17일): NTCP 제거, capabilities 지원 추가
- **2.10.0** (2025년 9월 9일): 최신 안정 버전

**프로토콜 안정성:** - 0.9.50 이후 호환성 파괴 변경 없음 - 프로빙(probing, 서비스 탐지 시도)에 대한 저항성 지속 개선 - 성능과 신뢰성에 집중 - 양자 이후 암호(Post-quantum cryptography) 개발 중 (기본값으로는 비활성화)

**현재 전송 프로토콜 상태:** - NTCP2: 필수 TCP 전송 프로토콜 - SSU2: 필수 UDP 전송 프로토콜 - NTCP (v1): 제거됨 - SSU (v1): 제거됨
