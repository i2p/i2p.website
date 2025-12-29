---
title: "암호화된 LeaseSet"
description: "비공개 Destinations(목적지 식별자)용 접근 제어된 LeaseSet 형식"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

이 문서는 암호화된 LeaseSet2 (LS2)의 블라인딩, 암호화 및 복호화를 명세한다. 암호화된 LeaseSet은 I2P netDb(네트워크 데이터베이스)에서 은닉 서비스 정보의 접근 제어가 적용된 게시를 제공한다.

**주요 기능:** - 전방향 기밀성을 위한 일일 키 순환 - 이중 계층 클라이언트 인가(DH(디피-헬만) 기반 및 PSK(사전 공유 키) 기반) - AES 하드웨어 지원이 없는 장치에서의 성능을 위한 ChaCha20 암호화 - key blinding(키 블라인딩)을 적용한 Red25519 서명 - 프라이버시 보존형 클라이언트 멤버십

**관련 문서:** - [공통 구조 명세](/docs/specs/common-structures/) - 암호화된 LeaseSet(리스셋: I2P 목적지의 연결 정보 묶음) 구조 - [제안 123: 새로운 netDB(I2P 네트워크 데이터베이스) 항목](/proposals/123-new-netdb-entries/) - 암호화된 LeaseSets에 대한 배경 - [네트워크 데이터베이스 문서](/docs/specs/common-structures/) - NetDB 사용

---

## 버전 이력 및 구현 현황

### 프로토콜 개발 타임라인

**버전 번호 지정에 대한 중요 참고 사항:**   I2P는 두 가지 별도의 버전 번호 체계를 사용합니다: - **API/Router 버전:** 0.9.x 계열 (기술 사양에서 사용) - **제품 릴리스 버전:** 2.x.x 계열 (공개 릴리스에 사용)

기술 사양서는 API 버전(예: 0.9.41)을 참조하고, 반면 최종 사용자는 제품 버전(예: 2.10.0)을 보게 됩니다.

### 구현 마일스톤

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### 현재 상태

- ✅ **프로토콜 상태:** 2019년 6월 이후 안정적이며 변경되지 않음
- ✅ **Java I2P:** 버전 0.9.40+에서 완전히 구현됨
- ✅ **i2pd (C++):** 버전 2.58.0+에서 완전히 구현됨
- ✅ **상호운용성:** 구현 간 완전한 상호운용성
- ✅ **네트워크 배포:** 6년 이상의 운영 경험으로 프로덕션 준비 완료

---

## 암호학적 정의

### 표기법 및 관례

- `||` 는 연결(이어붙이기)을 나타냅니다
- `mod L` 는 Ed25519의 차수(order) L에 대한 모듈러 감소를 나타냅니다
- 달리 명시되지 않는 한 모든 바이트 배열은 네트워크 바이트 순서(빅엔디언)입니다
- 리틀엔디언 값은 명시적으로 표시됩니다

### 암호학적으로 안전한 난수 생성기(n)

**암호학적으로 안전한 난수 생성기**

키 자료 생성에 적합한 암호학적으로 안전한 난수 데이터를 `n`바이트 생성합니다.

**보안 요구사항:** - 암호학적으로 안전해야 함(키 생성에 적합해야 함) - 네트워크 상에서 인접한 바이트 시퀀스가 노출되더라도 안전해야 함 - 구현체는 잠재적으로 신뢰할 수 없는 소스에서 나온 출력값은 해시 처리하는 것이 좋음

**참고자료:** - [PRNG(의사난수 생성기) 보안 고려사항](http://projectbullrun.org/dual-ec/ext-rand.html) - [Tor 개발자 토론](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**개인화가 적용된 SHA-256 해시**

도메인 분리가 적용된 해시 함수로 다음을 입력으로 받습니다: - `p`: 개인화 문자열(도메인 분리를 제공합니다) - `d`: 해시할 데이터

**구현:**

```
H(p, d) := SHA-256(p || d)
```
**Usage:** SHA-256의 서로 다른 프로토콜 용도 간 충돌 공격을 방지하기 위해 암호학적 도메인 분리를 제공합니다.

### 스트림: ChaCha20

**스트림 암호: RFC 7539 2.4절에 정의된 ChaCha20**

**매개변수:** - `S_KEY_LEN = 32` (256비트 키) - `S_IV_LEN = 12` (96비트 nonce(일회용 임의값)) - 초기 카운터: `1` (RFC 7539는 0 또는 1을 허용; AEAD 컨텍스트에서는 1을 권장)

**ENCRYPT(k, iv, plaintext)**

다음을 사용하여 평문을 암호화합니다: - `k`: 32바이트 암호 키 - `iv`: 12바이트 nonce(논스, 반드시 각 키마다 고유해야 함) - 평문과 동일한 크기의 암호문을 반환합니다

**보안 속성:** 키가 비밀이라면 전체 암호문은 무작위와 구별되지 않아야 한다.

**복호화(k, iv, ciphertext)**

다음을 사용해 암호문을 복호화합니다: - `k`: 32바이트 암호 키 - `iv`: 12바이트 논스 - 평문을 반환합니다

**설계 근거:** AES 대신 ChaCha20을 선택한 이유: - 하드웨어 가속이 없는 장치에서는 AES보다 2.5-3배 더 빠름 - 상수 시간 구현을 달성하기가 더 쉬움 - AES-NI(인텔의 AES 전용 명령어 집합) 사용이 가능한 경우에도 보안성과 속도가 비슷함

**참고 자료:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - IETF 프로토콜용 ChaCha20 및 Poly1305

### 서명: Red25519(Ed25519 기반 RedDSA 서명 알고리즘)

**서명 방식: Red25519 (SigType 11)와 Key Blinding(키 블라인딩: 서명 키에 난수를 적용해 원본 키 노출을 방지하는 기법)**

Red25519는 Ed25519 곡선 위의 Ed25519 서명을 기반으로 하며, 해싱에는 SHA-512를 사용하고, ZCash RedDSA에 명시된 대로 key blinding(키 블라인딩: 원본 키와의 연결을 숨기기 위해 키를 변형하는 기법)을 지원합니다.

**기능:**

#### DERIVE_PUBLIC(privkey)

주어진 개인 키에 해당하는 공개 키를 반환합니다. - 기준점에 대한 표준 Ed25519 스칼라 곱셈을 사용합니다

#### SIGN(privkey, m)

개인 키 `privkey`로 메시지 `m`에 대한 서명을 반환합니다.

**Ed25519와 비교한 Red25519의 서명 차이점:** 1. **무작위 논스:** 추가 80바이트의 무작위 데이터를 사용합니다

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
이로 인해 동일한 메시지와 키에 대해서도 모든 Red25519(서명 방식) 서명이 고유해집니다.

2. **개인 키 생성:** Red25519 개인 키는 난수로부터 생성된 뒤 `mod L`로 축약되며, Ed25519의 bit-clamping(비트들을 특정 패턴으로 고정하는 방식) 방식을 사용하지 않습니다.

#### VERIFY(pubkey, m, sig)

공개키 `pubkey`와 메시지 `m`에 대해 서명 `sig`를 검증합니다. - 서명이 유효하면 `true`를, 그렇지 않으면 `false`를 반환합니다 - 검증 방식은 Ed25519와 동일합니다

**키 블라인딩 작업:**

#### GENERATE_ALPHA(data, secret)

키 블라인딩을 위한 alpha를 생성합니다. - `data`: 일반적으로 서명 공개 키와 서명 유형을 포함합니다 - `secret`: 선택적 추가 비밀값(사용하지 않으면 길이 0바이트) - 결과는 Ed25519 개인 키와 동일한 분포를 가집니다(mod L 환원 후)

#### BLIND_PRIVKEY(privkey, alpha)

비밀값 `alpha`를 사용하여 개인 키를 블라인드 처리합니다. - 구현: `blinded_privkey = (privkey + alpha) mod L` - 체에서 스칼라 산술을 사용합니다

#### BLIND_PUBKEY(pubkey, alpha)

비밀값 `alpha`를 사용하여 공개키를 블라인딩합니다. - 구현: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - 곡선 위에서 군 원소(점) 덧셈을 사용합니다.

**핵심 속성:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**보안 고려사항:**

ZCash Protocol Specification 5.4.6.1절에 따르면: 보안을 위해 alpha는 블라인딩 해제된 개인 키와 동일한 분포를 가져야 한다. 이는 "재무작위화된 공개 키와 그 키로 생성된 서명(들)의 조합이, 해당 공개 키가 재무작위화되기 전의 원래 키를 드러내지 않는다"는 것을 보장한다.

**지원되는 서명 유형:** - **유형 7 (Ed25519):** 기존 destinations(목적지) 지원 (하위 호환성) - **유형 11 (Red25519):** 암호화를 사용하는 신규 destinations에 권장 - **Blinded keys(블라인드 키):** 항상 유형 11 (Red25519)을 사용

**참고 자료:** - [ZCash 프로토콜 명세서](https://zips.z.cash/protocol/protocol.pdf) - 섹션 5.4.6 RedDSA - [I2P Red25519 명세서](/docs/specs/red25519-signature-scheme/)

### DH(디피-헬먼 키 교환): X25519

**타원곡선 디피-헬만: X25519**

Curve25519 기반 공개 키 합의 시스템.

**매개변수:** - 개인 키: 32 바이트 - 공개 키: 32 바이트 - 공유 비밀 출력: 32 바이트

**기능:**

#### GENERATE_PRIVATE()

CSRNG(암호학적으로 안전한 난수 생성기)을 사용하여 새로운 32바이트 개인 키를 생성합니다.

#### DERIVE_PUBLIC(privkey)

주어진 비밀 키에서 32바이트 공개 키를 유도합니다. - Curve25519에서 스칼라 곱셈을 사용합니다

#### DH(privkey, pubkey)

디피-헬만 키 합의를 수행합니다. - `privkey`: 로컬 32바이트 개인 키 - `pubkey`: 원격 32바이트 공개 키 - 반환: 32바이트 공유 비밀

**보안 속성:** - Curve25519에서의 계산적 디피-헬먼 가정 - 임시 키 사용 시 전방향 기밀성 - 타이밍 공격을 방지하기 위해 상수 시간 구현 필요

**참고 문헌:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - 보안을 위한 타원곡선

### HKDF(HMAC 기반 추출-확장 키 파생 함수)

**HMAC 기반 키 파생 함수**

입력 키잉 재료에서 키 재료를 추출하고 확장합니다.

**매개변수:** - `salt`: 최대 32바이트(보통 SHA-256의 경우 32바이트) - `ikm`: 입력 키 재료(길이 제한 없음, 충분한 엔트로피 권장) - `info`: 컨텍스트별 정보(도메인 분리) - `n`: 출력 길이(바이트 단위)

**구현:**

RFC 5869에 명시된 대로 다음과 같은 설정으로 HKDF를 사용합니다: - **해시 함수:** SHA-256 - **HMAC:** RFC 2104에 명시된 대로 - **솔트 길이:** 최대 32바이트(SHA-256의 HashLen)

**사용 패턴:**

```
keys = HKDF(salt, ikm, info, n)
```
**도메인 분리:** `info` 매개변수는 프로토콜 내에서 HKDF의 서로 다른 사용 간에 암호학적 도메인 분리를 제공합니다.

**검증된 정보 값:** - `"ELS2_L1K"` - 레이어 1(외부) 암호화 - `"ELS2_L2K"` - 레이어 2(내부) 암호화 - `"ELS2_XCA"` - DH 클라이언트 인증 - `"ELS2PSKA"` - PSK 클라이언트 인증 - `"i2pblinding1"` - 알파 생성

**참고 자료:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - HKDF 명세 - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - HMAC 명세

---

## 형식 명세

암호화된 LS2(LeaseSet2, I2P의 2세대 leaseSet 형식)는 세 개의 중첩된 계층으로 구성된다:

1. **계층 0 (외부):** 저장 및 검색을 위한 평문 정보
2. **계층 1 (중간):** 클라이언트 인증 데이터(암호화됨)
3. **계층 2 (내부):** 실제 LeaseSet2(I2P의 목적지 정보 데이터 구조) 데이터(암호화됨)

**전체 구조:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**중요:** Encrypted LS2는 blinded keys(블라인딩된 키)를 사용합니다. Destination은 헤더에 포함되지 않습니다. DHT 저장 위치는 `SHA-256(sig type || blinded public key)`이며, 매일 변경됩니다.

### 레이어 0 (외부) - 평문

레이어 0은 표준 LS2 헤더를 사용하지 않습니다. 이는 blinded keys(블라인딩된 키: 원본 키를 숨기기 위해 변형한 키)에 최적화된 맞춤형 형식을 사용합니다.

**구조:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Flags 필드(2바이트, 비트 15-0):** - **비트 0:** 오프라인 키 표시자   - `0` = 오프라인 키 없음   - `1` = 오프라인 키 존재(임시 키 데이터가 뒤따름) - **비트 1-15:** 예약됨, 향후 호환성을 위해 0이어야 함

**임시 키 데이터 (플래그 비트 0 = 1인 경우에만 존재):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**서명 검증:** - **오프라인 키 없이:** 블라인드된 공개키로 검증 - **오프라인 키 사용:** 임시 공개키로 검증

서명은 Type부터 outerCiphertext까지의 모든 데이터를 포함한다(양 끝 포함).

### 레이어 1 (중간) - 클라이언트 인가

**복호화:** [레이어 1 암호화](#layer-1-encryption) 섹션을 참조하세요.

**구조:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**플래그 필드(1바이트, 비트 7-0):** - **비트 0:** 인가 모드   - `0` = 클라이언트별 인가 없음(모두 허용)   - `1` = 클라이언트별 인가(인가 섹션이 뒤따름) - **비트 3-1:** 인증 방식(비트 0 = 1인 경우에만)   - `000` = DH 클라이언트 인증   - `001` = PSK 클라이언트 인증   - 기타 값은 예약됨 - **비트 7-4:** 사용되지 않음, 0이어야 함

**DH 클라이언트 인증 데이터 (플래그 = 0x01, 비트 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient(인증 클라이언트) 항목 (40바이트):** - `clientID_i`: 8바이트 - `clientCookie_i`: 32바이트 (암호화된 authCookie(인증 쿠키))

**PSK 클라이언트 인증 데이터 (플래그 = 0x03, 비트 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**authClient 항목 (40바이트):** - `clientID_i`: 8바이트 - `clientCookie_i`: 32바이트 (암호화된 authCookie)

### 레이어 2 (내부) - LeaseSet 데이터

**복호화:** [Layer 2 Encryption](#layer-2-encryption) 섹션을 참조하세요.

**구조:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
내부 계층에는 다음을 포함한 전체 LeaseSet2(2세대 LeaseSet 형식) 구조체가 포함됩니다: - LS2 헤더 - Lease 정보 - LS2 서명

**검증 요구 사항:** 복호화 후, 구현은 다음을 검증해야 합니다: 1. 내부 타임스탬프가 외부에 게시된 타임스탬프와 일치함 2. 내부 만료 시간이 외부 만료 시간과 일치함 3. LS2 서명이 유효함 4. Lease(I2P에서 tunnel 엔드포인트 정보를 담는 항목) 데이터가 올바른 형식임

**참고 자료:** - [공통 구조 사양](/docs/specs/common-structures/) - LeaseSet2(I2P의 차세대 leaseSet 형식) 형식 상세

---

## 블라인딩 키 파생

### 개요

I2P는 Ed25519와 ZCash RedDSA를 기반으로 한 가법적 키 블라인딩(additive key blinding) 방식을 사용한다. 전방향 기밀성을 위해 블라인딩된 키는 매일(UTC 자정)에 교체된다.

**설계 근거:**

I2P는 Tor의 rend-spec-v3.txt Appendix A.2 접근 방식을 사용하지 않기로 명시적으로 선택했다. 명세에 따르면:

> "우리는 유사한 설계 목표를 가진 Tor의 rend-spec-v3.txt 부록 A.2를 사용하지 않는다. 그 방식의 블라인딩된 공개키가 소수 차수 부분군(prime-order subgroup)에 속하지 않을 수 있으며, 이에 따른 보안상의 영향은 알려져 있지 않기 때문이다."

I2P의 additive blinding(덧셈형 블라인딩)은 블라인딩된 키가 Ed25519 곡선의 소수 차수 부분군에 머무르도록 보장합니다.

### 수학적 정의

**Ed25519 매개변수:** - `B`: Ed25519의 기저점(생성원) = `2^255 - 19` - `L`: Ed25519의 위수 = `2^252 + 27742317777372353535851937790883648493`

**주요 변수:** - `A`: 블라인드 해제된 32바이트 서명 공개키 (Destination(목적지) 내) - `a`: 블라인드 해제된 32바이트 서명 개인키 - `A'`: 블라인드 처리된 32바이트 서명 공개키 (암호화된 LeaseSet에서 사용됨) - `a'`: 블라인드 처리된 32바이트 서명 개인키 - `alpha`: 32바이트 블라인딩 팩터 (비밀)

**도우미 함수:**

#### LEOS2IP(x)

"리틀 엔디언 옥텟 문자열을 정수로 변환"

바이트 배열을 리틀 엔디언에서 정수 표현으로 변환합니다.

#### H*(x)

"해시와 환원"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Ed25519(타원곡선 디지털 서명 알고리즘) 키 생성과 동일한 연산입니다.

### 알파 생성

**일일 로테이션:** 새로운 alpha(알파 값) 및 blinded keys(블라인딩 처리된 키)는 매일 UTC 자정(00:00:00 UTC)에 반드시 생성되어야 한다.

**GENERATE_ALPHA(destination, date, secret) 알고리즘:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**검증된 매개변수:** - 솔트 개인화: "I2PGenerateAlpha" - HKDF(HMAC 기반 키 유도 함수) 정보: "i2pblinding1" - 출력: mod L 적용 전 64바이트 - Alpha 분포: `mod L` 적용 후 Ed25519 개인 키와 동일한 분포

### 개인키 블라인딩

**BLIND_PRIVKEY(a, alpha) 알고리즘:**

암호화된 LeaseSet을 게시하는 목적지 소유자의 경우:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**중요:** 개인 키와 공개 키 사이의 올바른 대수적 관계를 유지하려면 `mod L` 환원이 필수적입니다.

### 공개 키 블라인딩

**BLIND_PUBKEY(A, alpha) 알고리즘:**

암호화된 LeaseSet을 조회하고 검증하는 클라이언트의 경우:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**수학적 동치:**

두 방법 모두 동일한 결과를 산출합니다:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
그 이유는 다음과 같습니다:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Blinded Keys(블라인딩된 키)를 사용한 서명

**블라인딩 해제된 LeaseSet 서명:**

블라인드되지 않은 LeaseSet(인증된 클라이언트에게 직접 전송됨)은 다음을 사용해 서명됩니다: - 표준 Ed25519(유형 7) 또는 Red25519(유형 11) 서명 - 블라인드되지 않은 서명용 개인 키 - 블라인드되지 않은 공개 키로 검증됨

**오프라인 키 사용 시:** - 블라인드 해제된 임시 개인 키로 서명 - 블라인드 해제된 임시 공개 키로 검증 - 둘 다 타입 7 또는 11이어야 함

**암호화된 LeaseSet 서명:**

암호화된 LeaseSet의 외부 부분은 blinded keys(블라인딩된 키)와 함께 Red25519 서명을 사용합니다.

**Red25519 서명 알고리즘:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Ed25519와의 주요 차이점:** 1. 개인 키의 해시가 아니라 80바이트의 임의 데이터 `T`를 사용 2. 공개 키 값을 직접 사용 (개인 키의 해시가 아님) 3. 동일한 메시지와 키에 대해서도 각 서명은 고유함

**검증:**

Ed25519와 동일:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### 보안 고려사항

**알파 배포:**

보안을 위해, alpha는 블라인딩되지 않은 개인 키와 동일한 분포여야 합니다. Ed25519(type 7)을 Red25519(type 11)로 블라인딩할 때, 분포가 약간 달라집니다.

**권장사항:** ZCash 요구사항을 충족하기 위해 언블라인드 키와 블라인드 키 모두에 Red25519 (type 11)를 사용하십시오: "재랜덤화된 공개키와 해당 키로 생성된 서명(들)의 조합은 그것이 재랜덤화되기 전의 원래 키를 드러내지 않는다."

**Type 7 지원:** Ed25519는 기존 Destination(목적지)과의 하위 호환성을 위해 지원되지만, 새로운 암호화된 Destination에는 type 11을 권장합니다.

**일일 로테이션의 이점:** - 전방향 기밀성: 오늘의 블라인딩된 키가 탈취되더라도 어제의 것은 노출되지 않음 - 비연결성: 일일 로테이션은 DHT(분산 해시 테이블)를 통한 장기 추적을 방지 - 키 분리: 기간별로 서로 다른 키 사용

**참고 자료:** - [Zcash 프로토콜 사양서](https://zips.z.cash/protocol/protocol.pdf) - 섹션 5.4.6.1 - [Tor 키 블라인딩 논의](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Tor 티켓 #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## 암호화 및 처리

### 하위 자격 증명 파생

암호화 전에, 암호화된 레이어가 Destination(I2P 목적지)의 서명 공개 키에 대한 지식에 결속되도록 자격 증명과 하위 자격 증명을 유도한다.

**목표:** Destination(I2P 목적지 식별자)의 서명 공개키를 아는 사람만 암호화된 LeaseSet을 복호화할 수 있도록 한다. 전체 Destination은 필요하지 않다.

#### 자격 증명 계산

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**도메인 분리:** `credential` 개인화 문자열은 이 해시가 DHT 조회 키나 다른 프로토콜 사용과 충돌하지 않도록 보장합니다.

#### Subcredential(하위 자격 증명) 계산

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**목적:** subcredential(하위 자격 증명)은 암호화된 LeaseSet을 다음에 바인딩합니다: 1. 특정 Destination(목적지) (credential(자격 증명)을 통해) 2. 특정 blinded key(블라인드된 키) (blindedPublicKey를 통해) 3. 특정 날짜 (blindedPublicKey의 일일 로테이션을 통해)

이는 재전송 공격과 서로 다른 날짜 간의 연계(링킹)를 방지합니다.

### 레이어 1 암호화

**컨텍스트:** 레이어 1에는 클라이언트 인가 데이터가 포함되어 있으며, subcredential(하위 자격 증명)에서 유도된 키로 암호화됩니다.

#### 암호화 알고리즘

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**출력:** `outerCiphertext`는 `32 + len(outerPlaintext)` 바이트입니다.

**보안 속성:** - Salt(해시 등에 추가하는 임의값)은 동일한 subcredential(하위 자격 증명)이어도 고유한 키/IV(초기화 벡터) 쌍을 보장함 - 컨텍스트 문자열 `"ELS2_L1K"`은 도메인 분리를 제공함 - ChaCha20은 의미론적 안전성(암호문이 난수와 구분되지 않음)을 제공함

#### 복호화 알고리즘

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**검증:** 복호화 후 레이어 1 구조가 올바른 형식인지 검증한 다음 레이어 2로 진행하십시오.

### 2계층 암호화

**맥락:** 레이어 2에는 실제 LeaseSet2 데이터가 포함되어 있으며, 클라이언트별 인증이 활성화된 경우 authCookie에서 파생된 키로, 그렇지 않으면 빈 문자열에서 파생된 키로 암호화된다.

#### 암호화 알고리즘

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**출력:** `innerCiphertext`는 `32 + len(innerPlaintext)` 바이트입니다.

**키 바인딩:** - 클라이언트 인증이 없는 경우: subcredential(하위 자격증명)과 타임스탬프에만 바인딩됨 - 클라이언트 인증이 활성화된 경우: authCookie에도 추가로 바인딩됨(승인된 각 클라이언트마다 다름)

#### 복호화 알고리즘

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**검증:** 복호화 후: 1. LS2 타입 바이트가 유효한지 검증 (3 또는 7) 2. LeaseSet2 구조를 파싱 3. 내부 타임스탬프가 외부 게시된 타임스탬프와 일치하는지 검증 4. 내부 만료 시간이 외부 만료 시간과 일치하는지 검증 5. LeaseSet2 서명을 검증

### 암호화 계층 요약

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**복호화 절차:** 1. 블라인드된 공개키로 레이어 0 서명을 검증 2. 하위 자격 증명(subcredential)을 사용하여 레이어 1을 복호화 3. 인가 데이터(있는 경우)를 처리하여 authCookie를 획득 4. authCookie와 하위 자격 증명을 사용하여 레이어 2를 복호화 5. LeaseSet2를 검증하고 구문 분석

---

## 클라이언트별 권한 부여

### 개요

클라이언트별 인가가 활성화되면, 서버는 인가된 클라이언트 목록을 유지합니다. 각 클라이언트는 out-of-band(별도 경로)로 안전하게 전송되어야 하는 키 자료를 보유합니다.

**두 가지 인가 메커니즘:** 1. **DH (Diffie-Hellman) 클라이언트 인가:** 더 안전하며, X25519 키 합의를 사용합니다 2. **PSK (사전 공유 키) 인가:** 더 단순하며, 대칭 키를 사용합니다

**공통 보안 속성:** - 클라이언트 구성원 프라이버시: 관찰자는 클라이언트 수는 볼 수 있지만 특정 클라이언트를 식별할 수 없음 - 익명 클라이언트 추가/철회: 특정 클라이언트가 언제 추가되거나 제거되는지 추적할 수 없음 - 8바이트 클라이언트 식별자 충돌 확률: ~18퀸틸리언(1.8×10^19)분의 1(무시 가능한 수준)

### DH(디피-헬먼) 클라이언트 인가

**개요:** 각 클라이언트는 X25519 키 쌍을 생성하고 자신의 공개 키를 보안 대역외 채널을 통해 서버로 전송한다. 서버는 ephemeral DH(일시적 디피-헬먼 키 교환)를 사용해 각 클라이언트마다 고유한 authCookie를 암호화한다.

#### 클라이언트 키 생성

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**보안상의 이점:** 클라이언트의 개인 키는 사용자의 장치를 절대 떠나지 않는다. 대역 외(out-of-band) 전송을 가로채는 공격자라도 X25519 DH를 깨뜨리지 않는 한, 향후 암호화된 LeaseSets를 복호화할 수 없다.

#### 서버 처리

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**계층 1 데이터 구조:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**서버 권장 사항:** - 게시되는 각 암호화된 LeaseSet마다 새로운 임시 키 쌍을 생성하세요 - 위치 기반 추적을 방지하기 위해 클라이언트 순서를 무작위로 섞으세요 - 실제 클라이언트 수를 숨기기 위해 더미 항목을 추가하는 것을 고려하세요

#### 클라이언트 처리

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**클라이언트 오류 처리:** - `clientID_i`를 찾을 수 없는 경우: 클라이언트 권한이 해지되었거나 처음부터 승인되지 않음 - 복호화에 실패한 경우: 데이터 손상 또는 잘못된 키(매우 드뭄) - 해지 여부를 감지하기 위해 클라이언트는 주기적으로 다시 가져와야 함

### PSK 클라이언트 인가

**개요:** 각 클라이언트는 사전 공유된 32바이트 대칭 키를 보유합니다. 서버는 각 클라이언트의 PSK(사전 공유 키)를 사용하여 동일한 authCookie를 암호화합니다.

#### 키 생성

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**보안 참고:** 원한다면 동일한 PSK(사전 공유 키)를 여러 클라이언트가 공유할 수 있습니다(“그룹” 인가를 생성합니다).

#### 서버 처리

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**계층 1 데이터 구조:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### 클라이언트 처리

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### 비교 및 권장 사항

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**권장 사항:** - **DH authorization(Diffie-Hellman 기반 인가) 사용** forward secrecy(순방향 기밀성)가 중요한 고보안 애플리케이션의 경우 - **PSK authorization(사전 공유 키 기반 인가) 사용** 성능이 중요하거나 클라이언트 그룹을 관리해야 하는 경우 - **PSK를 절대 재사용하지 말 것** 서로 다른 서비스나 기간에 걸쳐 - **항상 보안 채널 사용** 키 배포 시 (예: Signal, OTR, PGP)

### 보안 고려 사항

**클라이언트 구성원 프라이버시:**

두 메커니즘은 다음을 통해 클라이언트 멤버십의 프라이버시를 제공합니다: 1. **암호화된 클라이언트 식별자:** HKDF(키 유도 함수) 출력에서 파생된 8바이트 clientID 2. **구분 불가능한 쿠키:** 모든 32바이트 clientCookie 값은 무작위로 보임 3. **클라이언트별 메타데이터 없음:** 어떤 항목이 어느 클라이언트에 속하는지 식별할 방법이 없음

관찰자는 다음을 확인할 수 있습니다: - 허가된 클라이언트 수(`clients` 필드에서) - 시간 경과에 따른 클라이언트 수 변화

관찰자는 다음을 볼 수 없습니다: - 어떤 특정 클라이언트가 승인되었는지 - 특정 클라이언트가 언제 추가되거나 제거되었는지 (개수가 동일하게 유지되는 경우) - 클라이언트를 식별할 수 있는 모든 정보

**무작위화 권장 사항:**

서버는 암호화된 LeaseSet(I2P 목적지에 연결하기 위한 정보 집합)을 생성할 때마다 클라이언트 순서를 무작위화하는 것이 권장된다:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**장점:** - 클라이언트가 목록 내에서 자신의 위치를 알아내는 것을 방지합니다 - 위치 변경에 기반한 추론 공격을 방지합니다 - 클라이언트 추가/철회를 구분할 수 없게 합니다

**클라이언트 수 숨기기:**

서버는 임의의 더미 항목을 삽입할 수 있다:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**비용:** 더미 엔트리는 암호화된 LeaseSet의 크기를 증가시킵니다(엔트리당 40바이트).

**AuthCookie 로테이션:**

서버는 새 authCookie(인증 쿠키)를 생성하는 것이 권장된다:
- 암호화된 LeaseSet이 게시될 때마다(보통 몇 시간마다 한 번)
- 클라이언트의 권한을 취소한 직후
- 클라이언트 변경이 없더라도 정기 일정(예: 매일)에 맞춰

**장점:** - authCookie가 탈취되었을 때 노출 범위를 제한합니다 - 권한이 철회된 클라이언트가 신속히 접근 권한을 잃도록 보장합니다 - Layer 2에 대해 전방향 기밀성을 제공합니다

---

## 암호화된 LeaseSets(I2P 목적지 접근 정보 세트)용 Base32 주소 체계

### 개요

기존의 I2P base32 주소는 Destination(목적지)의 해시만 포함합니다(32 바이트 → 52 문자). 이는 암호화된 LeaseSets에 대해 충분하지 않은데, 그 이유는:

1. 클라이언트가 **블라인딩된 공개키**를 파생시키려면 **블라인딩되지 않은 공개키**가 필요합니다
2. 클라이언트는 적절한 키 파생을 위해 **서명 유형**(블라인딩되지 않은 것과 블라인딩된 것)이 필요합니다
3. 해시만으로는 이 정보를 제공하지 않습니다

**해결책:** 공개 키와 서명 유형을 포함하는 새로운 base32 형식.

### 주소 형식 사양

**디코딩된 구조 (35바이트):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**첫 3바이트 (체크섬과 XOR(배타적 논리합)):**

처음 3바이트에는 CRC-32 체크섬의 일부와 XOR(배타적 논리합)된 메타데이터가 포함된다:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**체크섬 속성:** - 표준 CRC-32 다항식을 사용 - 검출 실패 확률: 약 1/1,600만 - 주소 오타에 대한 오류 검출 기능 제공 - 인증 용도로는 사용할 수 없음(암호학적으로 안전하지 않음)

**인코딩된 형식:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**특징:** - 총 문자 수: 56 (35바이트 × 8비트 ÷ 문자당 5비트) - 접미사: ".b32.i2p" (기존의 base32와 동일) - 총 길이: 56 + 8 = 64자 (널 종료 문자 제외)

**Base32 인코딩:** - 알파벳: `abcdefghijklmnopqrstuvwxyz234567` (RFC 4648 표준) - 끝의 사용되지 않는 5비트는 반드시 0이어야 함 - 대소문자 구분 없음 (관례적으로 소문자 사용)

### 주소 생성

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### 주소 파싱

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### 기존 Base32와의 비교

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### 이용 제한

**BitTorrent 비호환성:**

암호화된 LS2 주소는 BitTorrent의 compact announce 응답과 함께 사용할 수 없습니다:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**문제:** Compact format(간결한 형식)에는 해시(32바이트)만 포함되어 있어 서명 유형이나 공개 키 정보를 위한 공간이 없습니다.

**해결 방법:** 전체 announce 응답을 사용하거나 전체 주소를 지원하는 HTTP 기반 트래커를 사용하세요.

### 주소록 통합

만약 클라이언트가 주소록에 전체 Destination(목적지)을 가지고 있다면:

1. 공개키를 포함한 전체 Destination(목적지)를 저장
2. 해시를 통한 역방향 조회 지원
3. 암호화된 LS2(leaseSet 2형식)를 만났을 때 주소록에서 공개키 가져오기
4. 전체 Destination을 이미 알고 있다면 새로운 base32 형식이 필요 없음

**암호화된 LS2(LeaseSet2)를 지원하는 주소록 형식:** - 전체 destination 문자열이 포함된 hosts.txt - destination 열이 있는 SQLite 데이터베이스 - 전체 destination 데이터가 포함된 JSON/XML 형식

### 구현 예시

**예제 1: 주소 생성**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**예제 2: 파싱 및 검증**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**예제 3: Destination(목적지: I2P의 엔드포인트 식별자)에서 변환**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### 보안 고려사항

**프라이버시:** - Base32 주소는 공개키를 드러냅니다 - 이는 의도된 동작이며 프로토콜에서 요구됩니다 - 개인키를 드러내거나 보안을 훼손하지는 않습니다 - 공개키는 설계상 공개 정보입니다

**충돌 저항성:** - CRC-32의 충돌 저항성은 32비트에 불과함 - 암호학적으로 안전하지 않음(오류 검출에만 사용) - 인증을 위해 체크섬에 절대 의존하지 말 것 - 완전한 목적지 검증은 여전히 필요함

**주소 검증:** - 사용 전에 항상 체크섬을 검증할 것 - 유효하지 않은 서명 유형의 주소는 거부할 것 - 공개 키가 타원 곡선 상에 있는지 확인할 것(구현별)

**참고 자료:** - [제안 149: 암호화된 LS2(leaseSet 2)용 B32](/proposals/149-b32-encrypted-ls2/) - [B32 주소 지정 사양](/docs/specs/b32-for-encrypted-leasesets/) - [I2P 이름 지정 사양](/docs/overview/naming/)

---

## 오프라인 키 지원

### 개요

오프라인 키를 사용하면 주 서명 키를 오프라인 상태(cold storage; 오프라인 보관)로 유지하면서, 일상적인 운영에는 임시 서명 키를 사용할 수 있습니다. 이는 보안 수준이 높은 서비스에 매우 중요합니다.

**암호화된 LS2(LeaseSet2, I2P의 새로운 leaseSet 형식) 특정 요구 사항:** - 임시 키는 오프라인에서 생성되어야 함 - 블라인딩된 개인 키는 사전 생성되어야 함(하루에 하나) - 임시 키와 블라인딩된 키 모두 일괄 전달 - 표준화된 파일 형식은 아직 정의되지 않음(명세에서 TODO)

### 오프라인 키 구조

**레이어 0 임시 키 데이터 (플래그 비트 0 = 1인 경우):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**서명 적용 범위:** 오프라인 키 블록의 서명은 다음을 포함합니다: - 만료 타임스탬프 (4바이트) - 일시적 서명 유형 (2바이트)   - 일시적 서명용 공개 키 (가변)

이 서명은 **블라인딩된 공개키**를 사용해 검증되며, 블라인딩된 개인키를 보유한 엔티티가 이 임시 키를 승인했음을 증명합니다.

### 키 생성 과정

**오프라인 키를 사용하는 암호화된 LeaseSet의 경우:**

1. **임시 키 쌍 생성** (오프라인, 콜드 스토리지에서):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# 각 날짜에 대해    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# 각 날짜에 대해    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# UTC 자정(또는 게시 전에)

date = datetime.utcnow().date()

# 오늘의 키 불러오기

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# 오늘의 암호화된 LeaseSet에는 이 키들을 사용하세요.

```

**Publishing Process:**

```python
# 1. 내부 LeaseSet2 생성

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. 2계층 암호화

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. 인가 데이터와 함께 레이어 1 생성

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. 레이어 1 암호화

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. 오프라인 서명 블록을 포함한 레이어 0 생성

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. 임시 개인 키로 레이어 0에 서명

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. 서명을 추가하고 게시

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# 매일 새로운 임시 키와 새로운 블라인딩된 키를 모두 생성하십시오

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - 암호화된 키 자료 묶음   - 포함되는 날짜 범위

OFFLINE_KEY_STATUS   - 남은 일수   - 다음 키 만료일

REVOKE_OFFLINE_KEYS     - 폐기할 날짜 범위   - 대체할 새 키(선택 사항)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# 암호화된 LeaseSet 활성화

i2cp.encryptLeaseSet=true

# 선택 사항: 클라이언트 인가 활성화

i2cp.enableAccessList=true

# 선택 사항: DH(디피-헬먼) 인증 사용(기본값은 PSK(사전 공유 키))

i2cp.accessListType=0

# 선택 사항: Blinding secret(주소 블라인딩에 사용하는 비밀값) (강력 권장)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// 암호화된 LeaseSet 생성 EncryptedLeaseSet els = new EncryptedLeaseSet();

// 목적지 설정 els.setDestination(destination);

// 클라이언트별 인가를 활성화 els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// 허가된 클라이언트(DH 공개 키) 추가: for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// blinding(블라인딩: I2P 목적지 공개키를 숨기는 기법) 매개변수를 설정 els.setBlindingSecret("your-secret");

// 서명하고 게시 els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# 암호화된 LeaseSet(목적지 접근 정보를 담는 I2P 데이터 구조) 활성화

encryptleaseset = true

# 선택 사항: 클라이언트 인증 유형(0=DH(디피-헬만), 1=PSK(사전 공유 키))

authtype = 0

# 선택 사항: Blinding secret(블라인딩용 비밀값)

secret = your-secret-here

# 선택 사항: 허용된 클라이언트(한 줄에 하나씩, base64로 인코딩된 공개 키)

client.1 = base64-인코딩된-클라이언트-공개키-1 client.2 = base64-인코딩된-클라이언트-공개키-2

```

**API Usage Example:**

```cpp
// 암호화된 LeaseSet 생성 auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// 클라이언트별 인가 활성화 encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// 허가된 클라이언트를 추가 for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// 서명하고 게시 encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# 테스트 벡터 1: 키 블라인딩

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# 예상: (레퍼런스 구현과 대조하여 검증)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Ed25519 기저점(생성점)

B = 2**255 - 19

# Ed25519의 차수(스칼라 필드 크기)

L = 2**252 + 27742317777372353535851937790883648493

# 서명 유형 값

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# 키 길이

PRIVKEY_SIZE = 32  # 바이트 PUBKEY_SIZE = 32   # 바이트 SIGNATURE_SIZE = 64  # 바이트

```

### ChaCha20 Constants

```python
# ChaCha20 매개변수

CHACHA20_KEY_SIZE = 32   # 바이트 (256 비트) CHACHA20_NONCE_SIZE = 12  # 바이트 (96 비트) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539에서는 0 또는 1을 허용함

```

### HKDF Constants

```python
# HKDF(HMAC 기반 키 파생 함수) 매개변수

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# HKDF(해시 기반 키 유도 함수) info 문자열(도메인 분리)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# SHA-256 개인화 문자열

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# 레이어 0(외부) 크기

BLINDED_SIGTYPE_SIZE = 2   # 바이트 BLINDED_PUBKEY_SIZE = 32   # 바이트 (Red25519용) PUBLISHED_TS_SIZE = 4      # 바이트 EXPIRES_SIZE = 2           # 바이트 FLAGS_SIZE = 2             # 바이트 LEN_OUTER_CIPHER_SIZE = 2  # 바이트 SIGNATURE_SIZE = 64        # 바이트 (Red25519)

# 오프라인 키 블록 크기

OFFLINE_EXPIRES_SIZE = 4   # 바이트 OFFLINE_SIGTYPE_SIZE = 2   # 바이트 OFFLINE_SIGNATURE_SIZE = 64  # 바이트

# 레이어 1(중간)의 크기

AUTH_FLAGS_SIZE = 1        # 바이트 EPHEMERAL_PUBKEY_SIZE = 32  # 바이트 (DH 인증) AUTH_SALT_SIZE = 32        # 바이트 (PSK 인증) NUM_CLIENTS_SIZE = 2       # 바이트 CLIENT_ID_SIZE = 8         # 바이트 CLIENT_COOKIE_SIZE = 32    # 바이트 AUTH_CLIENT_ENTRY_SIZE = 40  # 바이트 (CLIENT_ID + CLIENT_COOKIE)

# 암호화 오버헤드

SALT_SIZE = 32  # 바이트 (각 암호화된 레이어 앞에 추가됨)

# Base32 주소

B32_ENCRYPTED_DECODED_SIZE = 35  # 바이트 B32_ENCRYPTED_ENCODED_LEN = 56   # 문자 B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# 목적지 공개 키 (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Empty secret

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 바이트

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(레퍼런스 구현과 대조하여 검증) alpha = [64-바이트 16진수 값]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [RFC 7539 테스트 벡터와 대조하여 검증]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # 모두 0 ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44바이트 16진수 값]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32바이트 unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [base32 문자 56개].b32.i2p

# 체크섬이 올바르게 검증되는지 확인

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.