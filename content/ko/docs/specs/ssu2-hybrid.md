---
title: "PQ 하이브리드 SSU2"
description: "ML-KEM을 사용하는 SSU2 전송 프로토콜의 포스트 양자 하이브리드 변형"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "전송 계층"
accurateFor: "0.9.71"
---

### 상태

베타 2026년 2분기, 출시 2026년 3분기

## 개요

이것은 Proposal 169에서 설계된 SSU2 전송 프로토콜의 하이브리드 포스트 양자(post-quantum) 변형입니다. 추가적인 배경 정보는 해당 제안서를 참조하십시오.

PQ Hybrid SSU2는 표준 SSU2와 동일한 주소 및 포트에서만 정의됩니다. 다른 포트에서의 운영이나 표준 SSU2 지원 없이는 허용되지 않으며, 표준 SSU2가 더 이상 사용되지 않게 될 수 년 후까지도 허용되지 않을 것입니다.

이 명세서는 PQ Hybrid를 지원하기 위해 표준 SSU2에 필요한 변경 사항만을 문서화합니다. 기본 구현 세부 사항은 SSU2 명세서를 참조하십시오.

## 설계

우리는 CRYSTALS-Kyber 및 CRYSTALS-Dilithium(버전 3.1, 3 및 이전 버전)을 기반으로 하지만 이와 호환되지 않는 NIST FIPS 203 및 204 표준 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)을 지원합니다.

### 키 교환

PQ KEM은 임시 키(ephemeral keys)만 제공하며, Noise XK 및 IK와 같은 정적 키(static-key) 핸드셰이크를 직접 지원하지 않습니다. 암호화 타입은 PQ Hybrid Ratchet에서 사용되는 것과 동일하며, [공통 구조 문서](/docs/specs/common-structures/)에 정의되어 있습니다. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)과 마찬가지로, 하이브리드(Hybrid) 타입은 X25519와의 조합으로만 정의됩니다.

암호화 유형은 다음과 같습니다:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### 합법적인 조합

새로운 암호화 유형은 RouterAddresses에 표시됩니다. key certificate의 암호화 유형은 계속해서 type 4로 유지됩니다.

## 사양

### 핸드셰이크 패턴

핸드셰이크는 [Noise Protocol](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드
- e1 = 일회용 임시 PQ 키, Alice에서 Bob으로 전송
- ekem1 = KEM 암호문, Bob에서 Alice로 전송

하이브리드 순방향 비밀성(hfs)을 위한 XK 및 IK에 대한 다음 수정 사항은 [Noise HFS 사양](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 5에 명시된 내용을 따릅니다:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 바와 같이 다음과 같이 정의됩니다:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 바와 같이 다음과 같이 정의됩니다:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### Noise 핸드셰이크 KDF

#### 개요

하이브리드 핸드셰이크는 [Noise HFS 명세](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 정의되어 있습니다. Alice에서 Bob으로 전송되는 첫 번째 메시지는 메시지 페이로드 앞에 캡슐화 키인 e1을 포함합니다. 이는 추가적인 정적 키로 처리됩니다. Alice의 경우 이에 대해 EncryptAndHash()를 호출하고, Bob의 경우 DecryptAndHash()를 호출합니다. 이후 메시지 페이로드는 일반적인 방식으로 처리합니다.

Bob에서 Alice로 전송되는 두 번째 메시지는 메시지 페이로드 앞에 ekem1(암호문)을 포함합니다. 이는 추가적인 정적 키로 처리됩니다. Bob의 경우 EncryptAndHash()를, Alice의 경우 DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 이후 메시지 페이로드를 일반적인 방식으로 처리합니다.

#### 정의된 ML-KEM 연산

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의된 암호화 구성 요소에 대응하는 다음 함수들을 정의합니다.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

encap_key와 암호문(ciphertext) 모두 Noise 핸드셰이크 메시지 1과 2의 ChaCha/Poly 블록 내부에서 암호화된다는 점에 유의하십시오. 이들은 핸드셰이크 과정의 일부로 복호화됩니다.

kem_shared_key는 MixHash()를 통해 체이닝 키에 혼합됩니다. 자세한 내용은 아래를 참조하십시오.

#### 메시지 1에 대한 Alice KDF

'es' 메시지 패턴 이후, 페이로드 이전에 다음을 추가합니다:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### 메시지 1에 대한 Bob KDF

'es' 메시지 패턴 이후, 페이로드 이전에 다음을 추가합니다:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### 메시지 2를 위한 Bob KDF

XK의 경우: 'ee' 메시지 패턴 이후 및 페이로드 이전에 다음을 추가합니다:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 메시지 2에 대한 Alice KDF

'ee' 메시지 패턴 이후에 다음을 추가합니다:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 메시지 3의 KDF

unchanged

#### split()을 위한 KDF

unchanged

### 핸드셰이크 세부 정보

#### Noise 식별자

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

MLKEM-1024은 키 크기가 표준 1500바이트 데이터그램에 맞지 않을 만큼 너무 크기 때문에 SSU2에서는 지원되지 **않습니다**.

#### Long Header

긴 헤더는 32바이트입니다. 세션이 생성되기 전, Token Request, SessionRequest, SessionCreated, Retry에 사용됩니다. 또한 세션 외부의 Peer Test 및 Hole Punch 메시지에도 사용됩니다.

다음 메시지에서, MLKEM-512 또는 MLKEM-768을 나타내기 위해 long header의 ver (version) 필드를 3 또는 4로 설정합니다.

- (0) 세션 요청
- (1) 세션 생성됨
- (9) 재시도
- (10) 토큰 요청
- (11) 홀 펀치

다음 메시지에서는 MLKEM-512 또는 MLKEM-768이 지원되는 경우에도 평소와 같이 긴 헤더의 ver (version) 필드를 2로 설정합니다. 구현체는 상대방이 지원하는 경우 값을 3 또는 4로 설정할 수도 있지만, 이는 필수 사항이 아닙니다. 구현체는 2~4 범위의 모든 값을 수락해야 합니다.

- (7) Peer Test (세션 외 메시지 5-7)

논의: 모든 메시지 유형에 대해 version 필드를 3 또는 4로 설정하는 것이 반드시 필요한 것은 아니지만, 이렇게 하면 지원되지 않는 포스트 양자(post-quantum) 연결에 대한 조기 오류 감지에 도움이 됩니다. Token Request 및 Retry(유형 9 및 10)는 일관성을 위해 버전 3/4를 사용해야 합니다. Hole Punch 메시지(유형 11)는 이러한 처리가 필요하지 않을 수 있지만, 통일성을 위해 동일한 패턴을 따릅니다. Peer Test 메시지(유형 7)는 세션 외부(out-of-session) 메시지로, 세션 시작 의도를 나타내지 않습니다.

- Relay Request (릴레이 요청)
- Relay Response (릴레이 응답)
- Relay Intro (릴레이 소개)
- Peer Test (피어 테스트)

헤더 암호화 이전:

헤더 암호화 이전:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

unchanged

#### SessionRequest (타입 0)

변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다. ML-KEM을 적용하면 ChaCha 섹션에 암호화된 PQ(후양자) 공개 키도 함께 포함됩니다.

스푸핑 방지를 위한 KDF 변경: Proposal 165 [Prop165]_에서 제기된 문제를 다른 방식으로 해결하기 위해, Session Request에 대한 KDF를 수정합니다. 이는 PQ 세션에만 적용됩니다. 비PQ 세션의 KDF는 변경되지 않습니다.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
원시 내용:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
암호화되지 않은 데이터 (Poly1305 인증 태그 미표시):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
IP 오버헤드를 제외한 크기:

| 유형 | 유형 코드 | X 길이 | 메시지 1 길이 | 메시지 1 암호화 길이 | 메시지 1 복호화 길이 | PQ 키 길이 | pl 길이 |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 | | | | |
참고: 타입 코드는 내부 사용 전용입니다. router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

MLKEM768_X25519의 최소 MTU: IPv4의 경우 1318, IPv6의 경우 1338. 아래를 참조하십시오.

변경 사항: 현재의 SSU2는 단일 ChaCha 섹션에 페이로드만 포함합니다. ML-KEM을 사용하면 페이로드 이전에 새로운 ChaCha 섹션이 추가되어, 그 안에 암호화된 양자내성(PQ) 암호문이 들어가게 됩니다.

#### SessionCreated (타입 1)

변경 사항: 현재의 SSU2는 단일 ChaCha 섹션에 페이로드만 포함합니다. ML-KEM을 사용하면 페이로드 이전에 새로운 ChaCha 섹션이 추가되어 암호화된 양자내성(PQ) 암호문을 포함하게 됩니다.

원시 내용:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
암호화되지 않은 데이터 (Poly1305 인증 태그 미표시):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
IP 오버헤드를 제외한 크기:

| 유형 | 유형 코드 | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 | | | | |
참고: 타입 코드는 내부 사용 전용입니다. router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

MLKEM768_X25519의 최소 MTU: IPv4의 경우 1318, IPv6의 경우 1338. 아래를 참조하십시오.

최대 크기: 앨리스는 아직 밥의 RouterInfo를 가지고 있지 않아서 그가 공개한 MTU를 알지 못합니다. 이 메시지의 경우, 다음 방법으로 임시 MTU를 사용하세요. MLKEM512_X25519의 경우, 1280 또는 수신된 SessionRequest 크기 중 더 큰 값을 MTU로 사용합니다. MLKEM768_X25519의 경우, (IPv4 기준 1318 또는 IPv6 기준 1338) 또는 수신된 SessionRequest 크기 중 더 큰 값을 MTU로 사용합니다. MLKEM 공개키보다 MLKEM 암호문이 더 작기 때문에, SessionCreated의 오버헤드는 SessionRequest의 오버헤드보다 작습니다. 이로 인해 SessionRequest에서 거의 또는 전혀 패딩을 사용하지 않았더라도 SessionCreated에서는 다양한 크기의 패딩을 사용할 수 있습니다.

#### SessionConfirmed (타입 2)

unchanged

#### 데이터 단계를 위한 KDF

unchanged

#### 릴레이 및 피어 테스트

다음 블록들은 버전 필드를 포함합니다. 이 필드들은 (PQ를 지원하지 않는 Bob과의 호환성을 위해) 버전 2를 유지하며, PQ를 위해 버전 3/4로 변경되지 않습니다.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### 게시된 주소

모든 경우에 SSU2 전송 이름을 평소대로 사용하십시오. MLKEM-1024는 지원되지 않습니다.

non-PQ, 방화벽 미설정 시와 동일한 주소/포트를 사용합니다. PQ 변형 중 하나 또는 둘 다 지원됩니다. router 주소에는 v=2(기존과 동일)와 MLKEM 512/768/둘 다를 나타내는 새 파라미터 pq=[3|4|3,4|4,3]을 게시합니다. 아래에 명시된 최소값보다 MTU가 작은 router는 "4"를 포함하는 "pq" 파라미터를 게시해서는 안 됩니다. MLKEM-768 선호를 나타내려면 4,3을, MLKEM-512 선호를 나타내려면 3,4를 게시합니다. 실제 버전은 개시자(initiator)가 결정하며, 선호 설정이 반드시 적용되지 않을 수 있습니다. 아래에 명시된 최소값보다 MTU가 작은 router는 MLKEM768을 사용하여 연결해서는 안 됩니다. 구버전 router는 pq 파라미터를 무시하고 기존과 동일하게 non-pq 방식으로 연결합니다.

비-PQ와 다른 주소/포트, 또는 PQ 전용, 방화벽 미적용 구성은 지원되지 않습니다. 이 기능은 비-PQ SSU2가 비활성화되는 수 년 후까지 구현되지 않을 예정입니다. 비-PQ가 비활성화되면 하나 또는 두 PQ 변형이 모두 지원됩니다. router address에서 MLKEM 512/768/둘 다를 나타내기 위해 v=[3|4|3,4|4,3]을 게시합니다. 구형 router는 v 파라미터를 확인하고 지원되지 않는 주소로 판단하여 건너뜁니다.

방화벽 주소 (IP 미공개): router address에서 평소와 같이 v=2를 공개합니다. 릴레이를 지원하기 위해 pq 파라미터는 방화벽 주소에 반드시 공개되어야 합니다.

Alice는 자신의 router info에 PQ 지원을 광고하는지 여부, 또는 동일한 변형을 광고하는지 여부에 관계없이, Bob이 게시한 PQ 변형을 사용하여 PQ Bob에 연결할 수 있습니다.

#### MTU

MLKEM768을 사용할 때 MTU를 초과하지 않도록 주의하십시오. MLKEM768_X25519의 최소 MTU는 IPv4의 경우 1318, IPv6의 경우 1338입니다 (DateTime과 Padding 또는 RelayTagRequest 블록을 포함한 최소 페이로드 10바이트 기준). 일반적으로 SSU2의 최소 MTU는 1280이므로, 모든 피어가 MLKEM768을 사용하지는 않을 수 있습니다. 실제 MTU가 최솟값보다 작은 경우, 로컬 또는 피어가 공지한 값 모두에서 MLKEM768을 게시하거나 사용하지 마십시오. 메시지 1 또는 2가 로컬 또는 원격 MTU를 초과하지 않도록 패딩 크기에 주의하십시오.

## 오버헤드 분석

### 키 교환

크기 증가 (바이트):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## 보안 분석

NIST 보안 카테고리는 [NIST 발표자료](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 슬라이드 10에 요약되어 있습니다. 예비 기준: 최소 NIST 보안 카테고리는 하이브리드 프로토콜의 경우 2, PQ 전용(양자 후 암호화만 사용)의 경우 3이어야 합니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### 핸드셰이크

이들은 모두 하이브리드 프로토콜입니다. 구현 시 MLKEM768을 우선적으로 사용해야 하며, MLKEM512는 충분히 안전하지 않습니다.

NIST 보안 카테고리 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## 구현 참고사항

### 라이브러리 지원

Bouncycastle, BoringSSL, WolfSSL 라이브러리는 현재 MLKEM 및 MLDSA를 지원합니다. OpenSSL 지원은 2025년 4월 8일 예정인 3.5 릴리스에 포함될 예정입니다 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### 인바운드 트래픽 식별

세션 요청에서 임시 키의 최상위 비트(key[31] & 0x80)를 설정하여 이것이 하이브리드 연결임을 나타냅니다. 이를 통해 동일한 포트에서 표준 NTCP와 하이브리드 NTCP를 모두 실행할 수 있습니다. 인바운드에 대해서는 하나의 하이브리드 변형만 지원되며, 이는 router 주소에 공지됩니다. 예를 들어, pq=3 또는 pq=4와 같이 표시됩니다.

## 라우터 호환성

### 전송 프로토콜 이름

Alice로서, PQ 연결의 경우 난독화 전에 X[31] |= 0x80을 설정합니다. 이로 인해 X는 유효하지 않은 X25519 공개 키가 됩니다. 난독화 후에는 AES-CBC가 이를 무작위화합니다. 난독화 후 X의 최상위 비트(MSB)는 무작위가 됩니다.

## 참고 문헌

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
