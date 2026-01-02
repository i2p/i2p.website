---
title: "ECIES-X25519-AEAD-Ratchet 하이브리드 암호화"
description: "ML-KEM(모듈 격자 기반 키 캡슐화 메커니즘)을 사용하는 ECIES 암호화 프로토콜의 양자 내성 하이브리드 변형"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 구현 현황

**현재 배포 현황:** - **i2pd (C++ 구현)**: ML-KEM-512, ML-KEM-768, ML-KEM-1024 지원과 함께 버전 2.58.0(2025년 9월)에 완전 구현되었습니다. OpenSSL 3.5.0 이상이 사용 가능한 경우 post-quantum(양자내성) 종단간 암호화가 기본적으로 활성화됩니다. - **Java I2P**: 버전 0.9.67 / 2.10.0(2025년 9월) 기준으로 아직 구현되지 않았습니다. 규격은 승인되었으며, 구현은 향후 릴리스에 포함될 예정입니다.

이 명세서는 현재 i2pd에 배포되어 있으며 Java I2P 구현에 도입이 예정된 승인된 기능을 설명합니다.

## 개요

이는 ECIES-X25519-AEAD-Ratchet 프로토콜 [ECIES](/docs/specs/ecies/)의 포스트-양자 하이브리드 변형이다. 이는 승인될 Proposal 169 [Prop169](/proposals/169-pq-crypto/)의 첫 번째 단계를 나타낸다. 전체 목표, 위협 모델, 분석, 대안, 추가 정보는 해당 제안을 참조하라.

Proposal 169 상태: **Open** (하이브리드 ECIES(타원 곡선 통합 암호 체계) 구현을 위한 1단계가 승인됨).

이 명세서는 표준 [ECIES](/docs/specs/ecies/)와의 차이점만을 포함하며, 해당 명세서와 함께 읽어야 합니다.

## 설계

우리는 NIST FIPS 203 표준 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final)을 사용하며, 이는 CRYSTALS-Kyber(포스트-양자 공개키 암호)를 기반으로 하지만, CRYSTALS-Kyber의 버전 3.1, 3 및 그 이전과는 호환되지 않습니다.

하이브리드 핸드셰이크는 기존의 X25519 Diffie-Hellman과 양자내성 ML-KEM 키 캡슐화 메커니즘을 결합한다. 이러한 접근법은 PQNoise 연구에 문서화된 하이브리드 전방 비밀성 개념과 TLS 1.3, IKEv2, WireGuard의 유사한 구현을 기반으로 한다.

### 키 교환

우리는 Ratchet(래칫)용 하이브리드 키 교환을 정의한다. Post-quantum KEM(포스트-양자 키 캡슐화 메커니즘)은 임시 키만 제공하며 Noise IK(Noise 프로토콜의 IK 패턴)와 같은 정적 키 기반 핸드셰이크를 직접적으로 지원하지 않는다.

본 사양에서는 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final)에 명시된 대로 세 가지 ML-KEM(모듈 격자 기반 키 캡슐화 메커니즘) 변형을 정의하며, 이에 따라 총 3개의 새로운 암호화 유형이 됩니다. 하이브리드 유형은 X25519와의 조합에서만 정의됩니다.

새로운 암호화 유형은 다음과 같습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**참고:** MLKEM768_X25519 (Type 6)은 합리적인 오버헤드로 강력한 포스트-양자 보안을 제공하는 권장 기본 변형입니다.

X25519 전용 암호화와 비교하면 오버헤드가 상당합니다. 일반적인 메시지 1과 2의 크기(IK pattern(Noise 핸드셰이크 패턴 중 하나) 기준)는 현재 약 96~103바이트(추가 페이로드 이전)입니다. 메시지 유형에 따라 MLKEM512의 경우 약 9~12배, MLKEM768의 경우 13~16배, MLKEM1024의 경우 17~23배로 증가합니다.

### 새로운 암호화 필요

- **ML-KEM** (이전 명칭: CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - 모듈 격자 기반 키 캡슐화 메커니즘 표준
- **SHA3-256** (이전 명칭: Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - SHA-3 표준의 일부
- **SHAKE128 and SHAKE256** (SHA3에 대한 XOF 확장) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - 확장 가능한 출력 함수

SHA3-256, SHAKE128, SHAKE256에 대한 테스트 벡터는 [NIST Cryptographic Algorithm Validation Program(미국표준기술연구원(NIST) 암호 알고리즘 검증 프로그램)](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program)에서 제공됩니다.

**라이브러리 지원:** - Java: Bouncycastle 라이브러리 버전 1.79 이상은 모든 ML-KEM(모듈-격자 기반 키 캡슐화 메커니즘) 변형과 SHA3/SHAKE 함수를 지원 - C++: OpenSSL 3.5 이상에는 ML-KEM 전체 지원 포함(2025년 4월 릴리스) - Go: ML-KEM 및 SHA3 구현을 위한 여러 라이브러리 사용 가능

## 명세서

### 공통 구조

키 길이와 식별자에 대해서는 [Common Structures Specification](/docs/specs/common-structures/)을 참조하세요.

### 핸드셰이크 패턴

핸드셰이크는 하이브리드 포스트양자 보안을 위해 I2P에 특화된 변형을 적용한 [Noise Protocol Framework](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑을 사용합니다:

- **e** = 일회용 임시 키 (X25519)
- **s** = 정적 키
- **p** = 메시지 페이로드
- **e1** = 일회용 임시 PQ(후양자) 키, Alice가 Bob에게 전송됨 (I2P 전용 토큰)
- **ekem1** = KEM(키 캡슐화 메커니즘) 암호문, Bob이 Alice에게 전송됨 (I2P 전용 토큰)

**중요 참고:** 패턴 이름 "IKhfs"와 "IKhfselg2", 그리고 토큰 "e1"과 "ekem1"은 공식 Noise Protocol Framework(노이즈 프로토콜 프레임워크) 명세에 문서화되어 있지 않은 I2P 고유한 변형입니다. 이는 ML-KEM(양자내성 키 캡슐화 방식)을 Noise IK 패턴에 통합하기 위한 맞춤 정의를 나타냅니다. X25519 + ML-KEM 하이브리드 방식은 양자내성 암호 연구와 다른 프로토콜에서 널리 인정되고 있지만, 여기서 사용되는 구체적 명명법은 I2P에 특화되어 있습니다.

하이브리드 순방향 기밀성을 위해 IK에 다음과 같은 변경 사항이 적용됩니다:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
**e1** 패턴은 다음과 같이 정의됩니다:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
**ekem1** 패턴은 다음과 같이 정의됩니다:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### 정의된 ML-KEM 연산

우리는 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final)에 규정된 암호학적 구성 요소에 대응하는 다음 함수들을 정의한다.

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice는 캡슐화 키와 디캡슐화 키를 생성한다. 캡슐화 키는 NS 메시지로 전송된다. 키 크기:   - ML-KEM-512: encap_key = 800 바이트, decap_key = 1632 바이트   - ML-KEM-768: encap_key = 1184 바이트, decap_key = 2400 바이트   - ML-KEM-1024: encap_key = 1568 바이트, decap_key = 3168 바이트

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob은 NS 메시지에서 수신한 캡슐화 키를 사용해 암호문과 공유 키를 계산한다. 암호문은 NSR 메시지로 전송된다. 암호문 크기:   - ML-KEM-512: 768 바이트   - ML-KEM-768: 1088 바이트   - ML-KEM-1024: 1568 바이트

kem_shared_key는 세 가지 변형 모두에서 항상 **32바이트**입니다.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice는 NSR 메시지로 받은 ciphertext를 사용하여 공유 키를 계산한다. kem_shared_key는 항상 **32바이트**이다.

**중요:** encap_key와 암호문은 모두 Noise(암호 프로토콜 프레임워크) 핸드셰이크 메시지 1과 2의 ChaCha20-Poly1305 블록 내부에서 암호화되며, 핸드셰이크 과정의 일부로 복호화된다.

kem_shared_key는 MixKey()를 사용하여 chaining key(체이닝 키)에 혼합됩니다. 자세한 내용은 아래를 참조하세요.

### Noise 핸드셰이크 KDF(키 파생 함수)

#### 개요

하이브리드 핸드셰이크는 기존의 X25519 ECDH와 포스트-양자 ML-KEM(키 캡슐화 메커니즘)을 결합합니다. 첫 번째 메시지는 앨리스가 밥에게 보내는 것으로, 메시지 페이로드 앞에 e1(ML-KEM 캡슐화 키)을 포함합니다. 이는 추가 키 자료로 취급되며, 이에 대해 EncryptAndHash()(앨리스인 경우) 또는 DecryptAndHash()(밥인 경우)를 호출합니다. 그런 다음 평소와 같이 메시지 페이로드를 처리합니다.

두 번째 메시지(보낸 이: Bob, 받는 이: Alice)는 메시지 페이로드 앞에 ekem1(ML-KEM 암호문)을 포함합니다. 이는 추가적인 키 자료로 취급하며, 이에 대해 Bob은 EncryptAndHash()를, Alice는 DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 그 후 메시지 페이로드를 평소대로 처리합니다.

#### Noise(프로토콜 프레임워크) 식별자

다음은 Noise 초기화 문자열입니다(I2P 전용):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### Alice 측 NS 메시지용 KDF(키 유도 함수)

'es' 메시지 패턴 다음, 's' 메시지 패턴 이전에 다음을 추가하세요:

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
#### NS 메시지용 Bob 키 유도 함수

'es' 메시지 패턴 뒤, 's' 메시지 패턴 앞에 다음을 추가하십시오:

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
#### NSR 메시지를 위한 Bob KDF

'ee' 메시지 패턴 뒤에, 'se' 메시지 패턴 앞에 다음을 추가하십시오:

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
#### NSR 메시지를 위한 Alice 키 유도 함수

'ee' 메시지 패턴 이후, 'ss' 메시지 패턴 이전에 다음을 추가하세요:

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
#### split()를 위한 KDF(키 파생 함수)

split() 함수는 표준 ECIES(타원 곡선 통합 암호화 체계) 명세와 동일하게 유지됩니다. 핸드셰이크가 완료된 후:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
이는 지속적인 통신을 위한 양방향 세션 키입니다.

### 메시지 형식

#### NS (New Session, 새 세션) 형식

**변경 사항:** 현재 ratchet(순차적 키 갱신 메커니즘)은 첫 번째 ChaCha20-Poly1305(인증 암호화(AEAD) 알고리즘) 섹션에 정적 키를, 두 번째 섹션에 페이로드를 포함합니다. ML-KEM(양자 내성 키 캡슐화 메커니즘)을 사용하면 이제 세 개의 섹션으로 구성됩니다. 첫 번째 섹션에는 암호화된 ML-KEM 공개 키(encap_key)가 포함됩니다. 두 번째 섹션에는 정적 키가 포함됩니다. 세 번째 섹션에는 페이로드가 포함됩니다.

**메시지 크기:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**참고:** 페이로드에는 DateTime 블록(최소 7바이트: 1바이트 타입, 2바이트 크기, 4바이트 타임스탬프)이 포함되어야 합니다. 최소 NS 크기는 이에 따라 산출할 수 있습니다. 따라서 X25519의 실용적인 최소 NS 크기는 103바이트이고, 하이브리드 변형의 경우 919바이트에서 1687바이트까지입니다.

세 가지 ML-KEM(모듈 격자 기반 키 캡슐화 메커니즘) 변형에서 816, 1200, 1584바이트의 크기 증가는 ML-KEM 공개키와 인증된 암호화를 위한 16바이트 Poly1305 MAC(메시지 인증 코드) 때문입니다.

#### NSR (New Session Reply, 새 세션 응답) 형식

**변경 사항:** 현재 ratchet(키 갱신 메커니즘)은 첫 번째 ChaCha20-Poly1305(대칭 인증 암호 알고리즘) 섹션의 페이로드가 비어 있고, 두 번째 섹션에 페이로드가 있습니다. ML-KEM(양자내성 공개키 캡슐화 방식)을 사용하면 이제 섹션이 세 개입니다. 첫 번째 섹션에는 암호화된 ML-KEM 암호문이 들어 있습니다. 두 번째 섹션은 페이로드가 비어 있습니다. 세 번째 섹션에는 페이로드가 들어 있습니다.

**메시지 크기:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
세 가지 ML-KEM 변형의 크기 증가분 784, 1104, 1584바이트는 인증된 암호화를 위해 ML-KEM 암호문에 16바이트 Poly1305 MAC이 더해진 크기에 해당한다.

## 오버헤드 분석

### 키 교환

하이브리드 암호화의 오버헤드는 X25519-only와 비교하면 상당히 큽니다:

- **MLKEM512_X25519**: 핸드셰이크 메시지 크기가 약 9~12배 증가 (NS: 9.5배, NSR: 11.9배)
- **MLKEM768_X25519**: 핸드셰이크 메시지 크기가 약 13~16배 증가 (NS: 13.5배, NSR: 16.3배)
- **MLKEM1024_X25519**: 핸드셰이크 메시지 크기가 약 17~23배 증가 (NS: 17.5배, NSR: 23배)

추가된 포스트-양자 보안 이점을 고려하면 이 오버헤드는 수용할 만합니다. 배수는 메시지 유형마다 다른데, 기본 메시지 크기가 서로 다르기 때문입니다 (NS 최소 96바이트, NSR 최소 72바이트).

### 대역폭 고려사항

최소 페이로드로 일반적인 세션 수립 시: - X25519만: 총 ~200바이트 (NS + NSR) - MLKEM512_X25519: 총 ~1,800바이트 (9배 증가) - MLKEM768_X25519: 총 ~2,500바이트 (12.5배 증가) - MLKEM1024_X25519: 총 ~3,400바이트 (17배 증가)

세션 수립 후, 이후 전송되는 메시지의 암호화는 X25519 전용 세션과 동일한 데이터 전송 형식을 사용하므로 후속 메시지에 추가 오버헤드가 없습니다.

## 보안 분석

### 핸드셰이크

하이브리드 핸드셰이크는 전통적(X25519)과 양자 이후(ML-KEM(모듈-격자 기반 키 캡슐화 메커니즘)) 보안을 모두 제공합니다. 공격자가 세션 키를 노출시키려면 전통적 ECDH(타원 곡선 디피-헬만)와 양자 이후 KEM을 **둘 다** 깨뜨려야 합니다.

이는 다음을 제공합니다: - **현재 보안**: X25519 ECDH는 고전적(비양자) 공격자에 대해 보안을 제공합니다(128비트 보안 수준) - **미래 보안**: ML-KEM은 양자 공격자에 대한 보안을 제공합니다(매개변수 집합에 따라 달라짐) - **하이브리드 보안**: 세션을 손상시키려면 둘 모두가 깨져야 합니다(보안 수준 = 두 구성요소 중 최대값)

### 보안 수준

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**참고:** 하이브리드 보안 수준은 두 구성요소 중 더 약한 쪽의 수준을 넘지 못합니다. 모든 경우에 X25519는 고전 컴퓨팅 기준으로 128비트 보안 수준을 제공합니다. 암호학적으로 의미 있는 양자 컴퓨터가 사용 가능해질 경우, 보안 수준은 선택한 ML-KEM(모듈 격자 기반 키 캡슐화 메커니즘) 매개변수 세트에 따라 달라집니다.

### 순방향 기밀성

하이브리드 방식은 전방 비밀성 특성을 유지한다. 세션 키는 임시 X25519와 임시 ML-KEM 키 교환 모두로부터 파생된다. 핸드셰이크 이후 X25519 또는 ML-KEM의 임시 개인 키가 파기되면, 장기 정적 키가 유출되더라도 과거 세션은 복호화할 수 없다.

IK pattern(Noise 프로토콜의 핸드셰이크 패턴)은 두 번째 메시지(NSR)가 전송된 후 완전한 전방향 보안성(Noise Confidentiality level 5, Noise 프로토콜에서 정의된 기밀성 등급 5)을 제공한다.

## 유형 기본 설정

구현체는 여러 하이브리드 유형을 지원하고, 서로 지원하는 변형 중 가장 강력한 것을 협상해야 합니다. 선호 순서는 다음과 같아야 합니다:

1. **MLKEM768_X25519** (유형 6) - 권장 기본값으로, 보안과 성능의 균형이 가장 우수함
2. **MLKEM1024_X25519** (유형 7) - 민감한 애플리케이션을 위한 최고 수준의 보안
3. **MLKEM512_X25519** (유형 5) - 자원 제약 환경을 위한 기본 수준의 포스트-양자 보안
4. **X25519** (유형 4) - 기존(고전) 암호 전용, 호환성 유지를 위한 대체 옵션

**근거:** MLKEM768_X25519는 NIST 보안 수준 3(AES-192에 상응)을 제공하여 양자컴퓨터에 대해 충분한 보호를 제공하면서도 합리적인 메시지 크기를 유지하므로 기본값으로 권장됩니다. MLKEM1024_X25519는 더 높은 보안을 제공하지만 오버헤드가 상당히 증가합니다.

## 구현 참고 사항

### 라이브러리 지원

- **Java**: Bouncycastle 라이브러리 버전 1.79(2024년 8월) 이상은 필요한 모든 ML-KEM(양자내성 키 캡슐화 메커니즘 표준) 변형과 SHA3/SHAKE(해시/확장 가능 출력 함수)를 지원합니다. FIPS 203(미국 연방 정보 처리 표준 203) 준수를 위해 `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine`을 사용하십시오.
- **C++**: OpenSSL 3.5(2025년 4월) 이상은 EVP_KEM 인터페이스를 통해 ML-KEM 지원을 포함합니다. 이는 2030년 4월까지 유지 관리되는 장기 지원(Long Term Support) 릴리스입니다.
- **Go**: ML-KEM 및 SHA3용 타사 라이브러리가 여러 개 제공되며, 그중에는 Cloudflare의 CIRCL 라이브러리도 포함됩니다.

### 마이그레이션 전략

구현체는 다음을 따르는 것이 바람직하다: 1. 전환 기간 동안 X25519-only와 하이브리드 ML-KEM 변형을 모두 지원할 것 2. 두 피어 모두가 하이브리드 변형을 지원하는 경우 하이브리드 변형을 우선시할 것 3. 하위 호환성을 위해 X25519-only로의 fallback(대체 수단)을 유지할 것 4. 기본 변형을 선택할 때 네트워크 대역폭 제약을 고려할 것

### 공유된 Tunnels

증가한 메시지 크기가 공유 tunnel 사용에 영향을 줄 수 있습니다. 구현체는 다음을 고려해야 합니다: - 가능한 경우 핸드셰이크를 배치 처리하여 오버헤드 비용을 상쇄하기 - 저장된 상태를 줄이기 위해 하이브리드 세션의 만료 시간을 더 짧게 설정하기 - 대역폭 사용량을 모니터링하고 그에 따라 파라미터를 조정하기 - 세션 수립 트래픽에 대한 혼잡 제어를 구현하기

### 새 세션 크기 고려사항

더 큰 핸드셰이크 메시지로 인해, 구현체에서는 다음이 필요할 수 있습니다: - 세션 협상용 버퍼 크기 증가(최소 4KB 권장) - 느린 연결을 위한 타임아웃 값 조정(메시지가 약 3~17배 더 커짐을 감안) - NS/NSR 메시지의 페이로드 데이터에 대한 압축 고려 - 전송 계층에서 요구되는 경우 단편화 처리 구현

### 테스트 및 검증

구현체는 다음을 검증해야 합니다: - ML-KEM(모듈 격자 기반 키 캡슐화 메커니즘) 키 생성, 캡슐화, 디캡슐화의 정확성 - kem_shared_key가 Noise KDF(키 도출 함수)에 올바르게 통합되는지 - 메시지 크기 계산이 명세와 일치하는지 - 다른 I2P router 구현과의 상호 운용성 - ML-KEM을 사용할 수 없을 때의 폴백 동작

ML-KEM 연산에 대한 테스트 벡터는 NIST [Cryptographic Algorithm Validation Program(암호 알고리즘 검증 프로그램)](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program)에서 제공됩니다.

## 버전 호환성

**I2P 버전 번호 체계:** I2P는 두 가지 버전 번호 체계를 병행하여 유지합니다: - **Router 릴리스 버전**: 2.x.x 형식 (예: 2025년 9월에 릴리스된 2.10.0) - **API/프로토콜 버전**: 0.9.x 형식 (예: 0.9.67은 router 2.10.0에 해당)

이 명세서는 프로토콜 버전 0.9.67을 참조하며, 이는 router 2.10.0 릴리스 및 그 이후 버전에 해당합니다.

**호환성 매트릭스:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## 참고자료

- **[ECIES]**: [ECIES-X25519-AEAD-Ratchet 명세서](/docs/specs/ecies/)
- **[Prop169]**: [제안 169: 포스트-양자 암호](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - ML-KEM 표준](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - SHA-3 표준](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Noise 프로토콜 프레임워크](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [공통 구조 명세서](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 및 Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [OpenSSL 3.5 ML-KEM 문서](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bouncycastle 자바 암호화 라이브러리](https://www.bouncycastle.org/)

---
