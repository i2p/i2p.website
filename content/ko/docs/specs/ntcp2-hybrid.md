---
title: "PQ 하이브리드 NTCP2"
description: "ML-KEM을 사용한 NTCP2 전송 프로토콜의 양자 내성 하이브리드 변형"
slug: "ntcp2-hybrid"
lastupdated: "2026-10"
category: "전송 계층"
accurateFor: "0.9.71"
---

### 상태

베타 2026년 1분기, 출시 2026년 2분기

## 개요

이것은 Proposal 169에서 설계된 NTCP2 전송 프로토콜의 하이브리드 포스트 양자(post-quantum) 변형입니다. 추가적인 배경 정보는 해당 제안서를 참조하십시오.

PQ Hybrid NTCP2는 표준 NTCP2와 동일한 주소 및 포트에서만 정의됩니다. 다른 포트에서의 운영이나 표준 NTCP2 지원 없이 운영하는 것은 허용되지 않으며, 표준 NTCP2가 deprecated(더 이상 사용되지 않음)되는 수년 후까지는 허용되지 않을 것입니다.

이 명세서는 PQ Hybrid(후양자 하이브리드)를 지원하기 위해 표준 NTCP2에 필요한 변경 사항만을 문서화합니다. 기본 구현 세부 사항은 NTCP2 명세서를 참조하십시오.

## 설계

우리는 CRYSTALS-Kyber 및 CRYSTALS-Dilithium(버전 3.1, 3 및 이전 버전)을 기반으로 하지만 이와 호환되지 않는 NIST FIPS 203 및 204 표준 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)을 지원합니다.

### 키 교환

PQ KEM은 임시 키(ephemeral keys)만 제공하며, Noise XK 및 IK와 같은 정적 키(static-key) 핸드셰이크를 직접 지원하지 않습니다. 암호화 유형은 PQ Hybrid Ratchet에서 사용되는 것과 동일하며, 공통 구조 문서 [/docs/specs/common-structures/](/docs/specs/common-structures/)에 정의되어 있습니다. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서와 마찬가지로, 하이브리드(Hybrid) 유형은 X25519와의 조합으로만 정의됩니다.

암호화 유형은 다음과 같습니다:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 Version</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
### 합법적 조합

새로운 암호화 유형은 RouterAddresses에 표시됩니다. 키 인증서의 암호화 유형은 계속해서 유형 4로 유지됩니다.

## 사양

### 핸드셰이크 패턴

핸드셰이크는 [Noise Protocol](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키(ephemeral key)
- s = 정적 키(static key)
- p = 메시지 페이로드
- e1 = 일회용 임시 PQ 키, Alice에서 Bob으로 전송
- ekem1 = KEM 암호문(ciphertext), Bob에서 Alice로 전송

하이브리드 순방향 비밀성(hfs)을 위한 XK 및 IK의 다음 수정 사항은 [Noise HFS 사양](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 5에 명시된 대로입니다:

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

하이브리드 핸드셰이크는 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 정의되어 있습니다. Alice에서 Bob으로 전송되는 첫 번째 메시지에는 메시지 페이로드 앞에 캡슐화 키인 e1이 포함됩니다. 이는 추가적인 정적 키로 처리되며, (Alice의 경우) `EncryptAndHash()`를 호출하거나 (Bob의 경우) `DecryptAndHash()`를 호출합니다. 이후 메시지 페이로드는 일반적인 방식으로 처리됩니다.

Bob에서 Alice로 전송되는 두 번째 메시지에는 메시지 페이로드 앞에 암호문인 ekem1이 포함됩니다. 이는 추가적인 정적 키로 처리되며, (Bob의 경우) EncryptAndHash()를 호출하거나 (Alice의 경우) DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 이후 메시지 페이로드는 일반적인 방식으로 처리합니다.

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

XK의 경우: 'ee' 메시지 패턴 이후, 페이로드 이전에 다음을 추가합니다:

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
#### 메시지 2를 위한 Alice KDF

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
#### 메시지 3을 위한 KDF (XK 전용)

unchanged

#### split()을 위한 KDF

unchanged

### 핸드셰이크 세부 정보

#### Noise 식별자

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

변경 사항: 현재 NTCP2는 ChaCha 섹션의 옵션만 포함합니다. ML-KEM을 사용하면 ChaCha 섹션에 암호화된 PQ 공개 키도 포함됩니다.

PQ(양자 후 암호화)와 비-PQ NTCP2가 동일한 라우터 주소 및 포트에서 지원될 수 있도록, X 값(X25519 임시 공개 키)의 최상위 비트를 사용하여 해당 연결이 PQ 연결임을 표시합니다. 이 비트는 비-PQ 연결에서는 항상 설정되지 않습니다.

Alice의 경우, 메시지가 Noise에 의해 암호화된 후, X의 AES 난독화 이전에 X[31] |= 0x7f를 설정합니다.

Bob의 경우, X에 대한 AES 역난독화(de-obfuscation) 이후 X[31] & 0x80을 테스트합니다. 해당 비트가 설정되어 있으면 X[31] &= 0x7f로 비트를 지우고, PQ 연결로서 Noise를 통해 복호화합니다. 비트가 설정되어 있지 않으면, 평소와 같이 non-PQ 연결로서 Noise를 통해 복호화합니다.

다른 router 주소와 포트에 광고된 PQ NTCP2의 경우, 이는 필요하지 않습니다.

자세한 내용은 아래의 게시된 주소 섹션을 참조하십시오.

원시 내용:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
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

  Same as current specification except add a second ChaChaPoly frame
```
암호화되지 않은 데이터 (Poly1305 인증 태그 미표시):

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
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
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
```
참고: PQ 연결의 경우에도 메시지 1 옵션 블록의 version 필드는 반드시 2로 설정해야 합니다.

크기:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 1 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1232</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
참고: 타입 코드는 내부 용도로만 사용됩니다. router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

#### 2) SessionCreated

변경 사항: 현재의 NTCP2는 단일 ChaCha 섹션 내의 옵션들만 포함합니다. ML-KEM을 사용하면 옵션 이전에 새로운 ChaCha 섹션이 추가되며, 이 섹션에는 암호화된 양자내성(PQ) 암호문이 포함됩니다.

원시 내용:

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  -           16 bytes                    -
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
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

  Same as current specification except add a second ChaChaPoly frame
```
암호화되지 않은 데이터 (Poly1305 인증 태그 미표시):

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
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
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
```
크기:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Msg 2 Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">784</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1104</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pad</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
</tr>
</table>
참고: 타입 코드는 내부 용도로만 사용됩니다. router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

#### 3) SessionConfirmed

변경 없음

#### 키 파생 함수 (KDF) (데이터 단계용)

변경 없음

#### 게시된 주소

비-PQ, 방화벽 미적용 환경과 동일한 주소/포트를 사용합니다. 하나의 PQ 변형만 지원됩니다. router 주소에 v=2(기존과 동일)와 MLKEM 512/768/1024를 나타내는 새 파라미터 pq=[3|4|5]를 게시합니다. Alice는 세션 요청 시 임시 키(key[31] & 0x80)의 MSB를 설정하여 이것이 하이브리드 연결임을 나타냅니다. 위 내용을 참조하십시오. 구형 router는 pq 파라미터를 무시하고 기존과 동일하게 비-PQ 방식으로 연결합니다.

비-PQ와 다른 주소/포트를 사용하거나, PQ 전용이거나, 방화벽이 없는 구성은 지원되지 않습니다. 이 기능은 비-PQ NTCP2가 비활성화될 때까지, 즉 몇 년 후에는 구현되지 않을 것입니다. 비-PQ가 비활성화되면 여러 PQ 변형이 지원될 수 있지만, 주소당 하나만 허용됩니다. 지원될 경우, router 주소에서 MLKEM 512/768/1024를 나타내기 위해 `v=[3|4|5]`를 게시합니다. Alice는 임시 키의 최상위 비트(MSB)를 설정하지 않습니다. 구형 router는 `v` 파라미터를 확인하고 미지원 주소로 판단하여 해당 주소를 건너뜁니다.

방화벽 주소(공개된 IP 없음): router address에 v=2를 (평소와 같이) 게시합니다. pq 파라미터를 게시할 필요는 없습니다.

Alice는 자신의 router info에 PQ 지원을 광고하는지 여부나 동일한 변형을 광고하는지 여부와 관계없이, Bob이 게시한 PQ 변형을 사용하여 PQ Bob에 연결할 수 있습니다.

현재 명세에서 메시지 1과 2는 "적절한" 양의 패딩을 갖도록 정의되어 있으며, 0~31바이트의 범위가 권장되고 최대값은 별도로 지정되지 않습니다.

#### 최대 패딩

API 0.9.68 (릴리스 2.11.0)까지 Java I2P는 비-PQ 연결에 대해 최대 256바이트의 패딩을 구현했으나, 이는 이전에 문서화되지 않았습니다. API 0.9.69 (릴리스 2.12.0)부터 Java I2P는 비-PQ 연결에 대해 MLKEM-512와 동일한 최대 패딩을 구현합니다. 아래 표를 참조하십시오.

정의된 메시지 크기를 최대 패딩으로 사용합니다. 즉, PQ 연결의 경우 최대 패딩이 메시지 크기를 두 배로 늘리며, 내용은 다음과 같습니다:

크기 증가 (바이트):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message Max Padding</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (thru 0.9.68)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">non-PQ (as of 0.9.69)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-512</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-768</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">MLKEM-1024</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1264</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Session Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">848</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1168</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648</td>
</tr>
</table>
## 오버헤드 분석

### 키 교환

NIST 보안 카테고리는 [NIST 프레젠테이션](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 슬라이드 10에 요약되어 있습니다. 예비 기준: 하이브리드 프로토콜의 경우 최소 NIST 보안 카테고리 2, PQ 전용의 경우 최소 3을 충족해야 합니다.

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
## 보안 분석

이것들은 모두 하이브리드 프로토콜입니다. 구현체는 MLKEM768을 우선적으로 사용해야 하며, MLKEM512는 충분히 안전하지 않습니다.

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

NIST 보안 카테고리 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Bouncycastle, BoringSSL, WolfSSL 라이브러리는 현재 MLKEM 및 MLDSA를 지원합니다. OpenSSL 지원은 2025년 4월 8일 3.5 릴리스에 포함될 예정입니다 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## 구현 참고사항

### 라이브러리 지원

세션 요청에서 임시 키의 최상위 비트(key[31] & 0x80)를 설정하여 이것이 하이브리드 연결임을 나타냅니다. 이를 통해 표준 NTCP와 하이브리드 NTCP를 동일한 포트에서 함께 실행할 수 있습니다. 인바운드에 대해서는 하나의 하이브리드 변형만 지원되며, 이는 router 주소에 광고됩니다. 예를 들어, pq=3 또는 pq=4와 같습니다.

### 인바운드 트래픽 식별

Alice로서 PQ 연결의 경우, 난독화 이전에 X[31] |= 0x80을 설정합니다. 이렇게 하면 X가 유효하지 않은 X25519 공개 키가 됩니다. 난독화 이후에는 AES-CBC가 이를 무작위화합니다. 난독화 이후 X의 최상위 비트(MSB)는 무작위 값이 됩니다.

#### 난독화

Bob으로서, 난독화 해제 후 (X[31] & 0x80) != 0 인지 테스트합니다. 해당 조건이 참이면 PQ 연결입니다.

NTCP2-PQ에 필요한 최소 router 버전은 미정입니다.

NTCP2-PQ에 필요한 최소 라우터 버전은 아직 결정되지 않았습니다.

참고: 타입 코드는 내부 용도로만 사용됩니다. router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

## 라우터 호환성

### 전송 이름

모든 경우에 NTCP2 transport 이름을 평소와 같이 사용하십시오. 구버전 router는 pq 매개변수를 무시하고 표준 NTCP2로 평소와 같이 연결합니다.

## 참고 자료

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
