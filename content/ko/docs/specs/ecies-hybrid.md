---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "ML-KEM을 사용한 ECIES 암호화 프로토콜의 양자 후 하이브리드 변형"
slug: "ecies-hybrid"
category: "프로토콜"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## 참고

다양한 router 구현체에서 구현, 테스트 및 배포가 진행 중입니다. 상태 확인을 위해서는 해당 구현체의 문서를 확인하십시오.

## 개요

이것은 ECIES-X25519-AEAD-Ratchet 프로토콜 [ECIES](/docs/specs/ecies/)의 PQ Hybrid 변형입니다. 이는 승인된 전체 PQ 제안 [Prop169](/proposals/169-pq-crypto/)의 첫 번째 단계입니다. 전체 목표, 위협 모델, 분석, 대안 및 추가 정보는 해당 제안을 참조하세요.

이 명세서는 표준 [ECIES](/docs/specs/ecies/)와의 차이점만을 포함하며, 해당 명세서와 함께 읽어야 합니다.

## 설계

우리는 CRYSTALS-Kyber를 기반으로 하지만 이와 호환되지 않는 NIST FIPS 203 표준 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)을 지원합니다.

Hybrid handshake는 [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 명시된 바와 같습니다.

### 키 교환

Ratchet을 위한 하이브리드 키 교환을 정의합니다. PQ KEM은 임시 키만 제공하며, Noise IK와 같은 정적 키 핸드셰이크를 직접 지원하지 않습니다.

[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서와 같이 3개의 ML-KEM 변형을 정의하여 총 3개의 새로운 암호화 타입을 만듭니다. 하이브리드 타입은 X25519와의 조합으로만 정의됩니다.

새로운 암호화 유형은 다음과 같습니다:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
오버헤드가 상당할 것입니다. 현재 일반적인 메시지 1과 2 크기(IK용)는 약 100바이트입니다(추가 페이로드 제외). 알고리즘에 따라 8배에서 15배까지 증가할 것입니다.

### 새로운 암호화 필요

- ML-KEM (이전 CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (이전 Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) SHAKE128에만 사용됨
- SHA3-256 (이전 Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128과 SHAKE256 (SHA3-128과 SHA3-256의 XOF 확장)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128, SHAKE256에 대한 테스트 벡터는 [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)에서 확인할 수 있습니다.

Java bouncycastle 라이브러리는 위의 모든 사항을 지원한다는 점에 유의하세요. C++ 라이브러리 지원은 OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)에서 제공됩니다.

## 사양

### 공통 구조

키 길이와 식별자에 대한 공통 구조 명세서 [COMMON](/docs/specs/common-structures/)를 참조하세요.

### 핸드셰이크 패턴

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드
- e1 = 일회용 임시 PQ 키, Alice에서 Bob으로 전송
- ekem1 = KEM 암호문, Bob에서 Alice로 전송

하이브리드 전진 비밀성(hfs)을 위한 XK 및 IK에 대한 다음 수정 사항은 [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 5에 명시된 바와 같습니다:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 패턴은 [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 바와 같이 다음과 같이 정의됩니다:

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
ekem1 패턴은 [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 대로 다음과 같이 정의됩니다:

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
### 정의된 ML-KEM 작업

[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서 정의된 대로 사용되는 암호학적 구성 요소에 해당하는 다음 함수들을 정의합니다.

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice가 캡슐화 및 탈캡슐화 키를 생성합니다. 캡슐화 키는 NS 메시지로 전송됩니다. encap_key와 decap_key 크기는 ML-KEM 변형에 따라 달라집니다.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob은 NS 메시지에서 받은 암호문을 사용하여 암호문과 공유 키를 계산합니다. 암호문은 NSR 메시지로 전송됩니다. 암호문 크기는 ML-KEM 변형에 따라 달라집니다. kem_shared_key는 항상 32바이트입니다.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice는 NSR 메시지에서 받은 암호문을 사용하여 공유 키를 계산합니다. kem_shared_key는 항상 32바이트입니다.

encap_key와 ciphertext 모두 Noise 핸드셰이크 메시지 1과 2에서 ChaCha/Poly 블록 내부에서 암호화된다는 점에 유의하세요. 이들은 핸드셰이크 과정의 일부로 복호화될 것입니다.

kem_shared_key는 MixHash()를 통해 chaining key에 혼합됩니다. 자세한 내용은 아래를 참조하세요.

### Noise Handshake KDF

#### 개요

하이브리드 핸드셰이크는 [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 정의되어 있습니다. Alice에서 Bob으로 보내는 첫 번째 메시지는 메시지 페이로드 앞에 캡슐화 키인 e1을 포함합니다. 이것은 추가 정적 키로 처리되므로, (Alice로서) EncryptAndHash()를 호출하거나 (Bob으로서) DecryptAndHash()를 호출합니다. 그런 다음 메시지 페이로드를 평소와 같이 처리합니다.

Bob에서 Alice로의 두 번째 메시지는 메시지 페이로드 앞에 ekem1과 암호문을 포함합니다. 이것은 추가적인 정적 키로 취급되며, (Bob으로서) EncryptAndHash()를 호출하거나 (Alice로서) DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 이후 메시지 페이로드를 평소와 같이 처리합니다.

#### Noise 식별자

다음은 Noise 초기화 문자열입니다:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### NS 메시지용 Alice KDF

'es' 메시지 패턴 이후 그리고 's' 메시지 패턴 이전에 다음을 추가하십시오:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NS 메시지를 위한 Bob KDF

'es' 메시지 패턴 다음과 's' 메시지 패턴 이전에 다음을 추가하세요:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### NSR 메시지용 Bob KDF

'ee' 메시지 패턴 다음과 'se' 메시지 패턴 이전에 다음을 추가하세요:

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
```
#### NSR 메시지를 위한 Alice KDF

'ee' 메시지 패턴 이후와 'ss' 메시지 패턴 이전에 다음을 추가하세요:

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
```
#### split()을 위한 KDF

변경되지 않음

### 메시지 형식

#### NS 형식

변경 사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 정적 키를 포함하고, 두 번째 섹션에 페이로드를 포함했습니다. ML-KEM을 사용하면 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ 공개 키를 포함합니다. 두 번째 섹션은 정적 키를 포함합니다. 세 번째 섹션은 페이로드를 포함합니다.

암호화된 형식:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
복호화된 형식:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
크기:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
페이로드는 DateTime 블록을 포함해야 하므로 최소 페이로드 크기는 7입니다. 최소 NS 크기는 이에 따라 계산할 수 있습니다.

#### NSR 형식

변경사항: 현재 ratchet은 첫 번째 ChaCha 섹션에는 빈 payload를, 두 번째 섹션에는 payload를 가지고 있습니다. ML-KEM을 사용하면 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ ciphertext를 포함합니다. 두 번째 섹션은 빈 payload를 가집니다. 세 번째 섹션은 payload를 포함합니다.

암호화된 형식:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
복호화된 형식:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
크기:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
NSR은 일반적으로 0이 아닌 페이로드를 가지지만, ratchet 사양 [ECIES](/docs/specs/ecies/)에서는 이를 요구하지 않으므로 최소 페이로드 크기는 0입니다. 최소 NSR 크기는 이에 따라 계산될 수 있습니다.

## 오버헤드 분석

### 키 교환

크기 증가 (바이트):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
속도:

[CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)에서 보고된 속도:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## 보안 분석

NIST 보안 카테고리는 [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 슬라이드 10에 요약되어 있습니다. 예비 기준: 하이브리드 프로토콜의 경우 최소 NIST 보안 카테고리는 2이고, PQ 전용의 경우 3이어야 합니다.

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

이들은 모두 하이브리드 프로토콜입니다. 아마도 MLKEM768을 선호해야 할 것입니다. MLKEM512는 충분히 안전하지 않습니다.

NIST 보안 범주 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
## 타입 기본 설정

보안 범주와 키 길이를 기반으로 한 초기 지원을 위한 권장 유형은 다음과 같습니다:

MLKEM768_X25519 (타입 6)

## 구현 참고사항

### 라이브러리 지원

Bouncycastle, BoringSSL, WolfSSL 라이브러리들이 현재 MLKEM을 지원합니다. OpenSSL 지원은 2025년 4월 8일 3.5 릴리스에 포함될 예정입니다 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### 공유 tunnel

동일한 tunnel에서 여러 프로토콜의 자동 분류/감지는 메시지 1(New Session Message)의 길이 확인을 기반으로 가능해야 합니다. MLKEM512_X25519를 예로 들면, 메시지 1의 길이는 현재 ratchet 프로토콜보다 816바이트 더 크며, 최소 메시지 1 크기(DateTime 페이로드만 포함)는 919바이트입니다. 현재 ratchet을 사용하는 대부분의 메시지 1 크기는 816바이트 미만의 페이로드를 가지므로, 이들은 비하이브리드 ratchet으로 분류될 수 있습니다. 큰 메시지들은 아마도 드문 POST일 것입니다.

따라서 권장되는 전략은 다음과 같습니다:

- 메시지 1이 919바이트 미만이면 현재 ratchet 프로토콜입니다.
- 메시지 1이 919바이트 이상이면 아마도 MLKEM512_X25519입니다. MLKEM512_X25519를 먼저 시도하고, 실패하면 현재 ratchet 프로토콜을 시도하세요.

이를 통해 이전에 같은 목적지에서 ElGamal과 ratchet을 지원했던 것처럼, 같은 목적지에서 표준 ratchet과 하이브리드 ratchet을 효율적으로 지원할 수 있습니다. 따라서 같은 목적지에 대해 이중 프로토콜을 지원할 수 없었다면 보다 훨씬 빠르게 MLKEM 하이브리드 프로토콜로 마이그레이션할 수 있습니다. 기존 목적지에 MLKEM 지원을 추가할 수 있기 때문입니다.

필수로 지원되는 조합은 다음과 같습니다:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

다음 조합들은 복잡할 수 있으며, 지원이 필수는 아니지만 구현에 따라 지원될 수 있습니다:

- 하나 이상의 MLKEM
- ElG + 하나 이상의 MLKEM
- X25519 + 하나 이상의 MLKEM
- ElG + X25519 + 하나 이상의 MLKEM

동일한 목적지에서 여러 MLKEM 알고리즘(예: MLKEM512_X25519 및 MLKEM_768_X25519)을 지원할 필요는 없습니다. 하나만 선택하세요. 구현에 따라 달라집니다.

동일한 destination에서 세 가지 알고리즘(예: X25519, MLKEM512_X25519, MLKEM769_X25519)을 모두 지원할 필요는 없습니다. 분류 및 재시도 전략이 너무 복잡할 수 있습니다. 구성 및 구성 UI가 너무 복잡할 수 있습니다. 구현에 따라 달라집니다.

동일한 목적지에서 ElGamal과 hybrid 알고리즘을 모두 지원할 필요는 없습니다. ElGamal은 더 이상 사용되지 않으며, ElGamal + hybrid만 사용하는 것(X25519 없이)은 별로 의미가 없습니다. 또한 ElGamal과 Hybrid New Session Message는 모두 크기가 크므로, 분류 전략에서 두 가지 복호화를 모두 시도해야 하는 경우가 많아 비효율적입니다. 구현에 따라 달라집니다.

클라이언트는 동일한 tunnel에서 X25519 프로토콜과 하이브리드 프로토콜에 대해 동일하거나 다른 X25519 정적 키를 사용할 수 있으며, 이는 구현에 따라 달라집니다.

### 전방향 완전 비밀성

ECIES 사양은 New Session Message 페이로드에서 Garlic Messages를 허용하며, 이는 일반적으로 HTTP GET인 초기 스트리밍 패킷을 클라이언트의 leaseset과 함께 0-RTT 전송할 수 있게 합니다. 하지만 New Session Message 페이로드는 순방향 비밀성을 제공하지 않습니다. 이 제안이 ratchet에 대한 강화된 순방향 비밀성을 강조하는 만큼, 구현체들은 첫 번째 Existing Session Message까지 스트리밍 페이로드 또는 전체 스트리밍 메시지의 포함을 연기할 수 있거나 연기해야 합니다. 이는 0-RTT 전송을 희생하는 대가가 될 것입니다. 전략은 또한 트래픽 유형이나 tunnel 유형, 또는 예를 들어 GET 대 POST에 따라 달라질 수 있습니다. 구현체에 따라 다릅니다.

### 새 세션 크기

MLKEM은 위에서 설명한 바와 같이 New Session Message의 크기를 극적으로 증가시킬 것입니다. 이는 tunnel을 통한 New Session Message 전달의 신뢰성을 크게 감소시킬 수 있는데, 메시지가 여러 개의 1024바이트 tunnel 메시지로 조각화되어야 하기 때문입니다. 전달 성공률은 조각 수의 지수에 비례합니다. 구현체들은 0-RTT 전달을 희생하더라도 메시지 크기를 제한하기 위해 다양한 전략을 사용할 수 있습니다. 구현체에 따라 다릅니다.

## 참고문헌

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
