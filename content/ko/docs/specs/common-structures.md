---
title: "공통 구조"
description: "I2P 사양 전반에서 사용되는 공통 데이터 타입과 직렬화 형식"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

이 문서는 [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) 등을 포함한 모든 I2P 프로토콜 전반에서 사용되는 기본 데이터 구조를 명세합니다. 이러한 공통 구조는 서로 다른 I2P 구현체 및 프로토콜 계층 간 상호 운용성을 보장합니다.

### 0.9.58 이후 주요 변경 사항

- Router Identities에서 ElGamal 및 DSA-SHA1 사용 중단됨 (X25519 + EdDSA 사용)
- Post-quantum(양자 이후) ML-KEM 지원이 베타 테스트 중 (2.10.0부터 opt-in(사용자 선택 활성화))
- 서비스 레코드 옵션 표준화 ([Proposal 167](/proposals/167-service-records/), 0.9.66에서 구현됨)
- 압축 가능한 패딩 사양 최종 확정 ([Proposal 161](/ko/proposals/161-ri-dest-padding/), 0.9.57에서 구현됨)

---

## 공통 타입 명세

### 정수

**설명:** 네트워크 바이트 순서(big-endian, 빅 엔디언)로 표현된 음이 아닌 정수를 나타냅니다.

**내용:** 부호 없는 정수를 나타내는 1~8바이트.

**용도:** I2P 프로토콜 전반에서 사용되는 필드 길이, 개수, 유형 식별자 및 숫자 값.

---

### 날짜

**설명:** 유닉스 에포크(1970년 1월 1일 00:00:00 GMT) 이후 경과한 밀리초를 나타내는 타임스탬프.

**내용:** 8바이트 정수 (unsigned long)

**특수 값:** - `0` = 미정의 또는 null 날짜 - 최대값: `0xFFFFFFFFFFFFFFFF` (연도 584,942,417,355)

**구현 참고 사항:** - 항상 UTC/GMT 시간대 사용 - 밀리초 단위 정밀도 필요 - 리스 만료, RouterInfo 게시 및 타임스탬프 검증에 사용

---

### 문자열

**설명:** 길이 접두어가 있는 UTF-8 인코딩 문자열.

**형식:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**제약 사항:** - 최대 길이: 255 바이트 (문자 수 기준이 아님 - 멀티바이트 UTF-8 시퀀스는 여러 바이트로 계산됨) - 길이는 0일 수 있음 (빈 문자열) - 널 종료 문자는 포함되지 않음 - 문자열은 널로 종료되지 않음

**중요:** UTF-8에서는 문자 하나가 여러 바이트로 구성될 수 있습니다. 100개의 문자로 이루어진 문자열도 멀티바이트 문자를 사용하는 경우 255바이트 제한을 초과할 수 있습니다.

---

## 암호학적 키 구조

### 공개키

**설명:** 비대칭 암호화를 위한 공개 키. 키 유형과 길이는 컨텍스트에 따라 달라지거나 Key Certificate(키 인증서)에 지정됩니다.

**기본 유형:** ElGamal (0.9.58부터 Router 식별자용으로 더 이상 권장되지 않음)

**지원되는 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**구현 요구사항:**

1. **X25519 (Type 4) - 현재 표준:**
   - ECIES-X25519-AEAD-Ratchet 암호화에 사용됨
   - 0.9.48부터 Router 식별자에 필수
   - 리틀 엔디언 인코딩(다른 유형과 달리)
   - [ECIES](/docs/specs/ecies/) 및 [ECIES-ROUTERS](/docs/specs/ecies/#routers)를 참조하세요

2. **ElGamal (Type 0) - 레거시:**
   - 0.9.58부터 router 식별자에서 사용 중단됨
   - Destinations(목적지 식별자)에는 여전히 유효함 (해당 필드는 0.6/2005 이후 미사용)
   - [ElGamal 명세](/docs/specs/cryptography/)에 정의된 상수 소수를 사용함
   - 하위 호환성을 위해 지원을 유지함

3. **MLKEM (포스트 양자 키 캡슐화 메커니즘) - 베타:**
   - 하이브리드 방식은 ML-KEM과 X25519를 결합합니다
   - 2.10.0에서는 기본적으로 활성화되지 않습니다
   - Hidden Service Manager를 통해 수동으로 활성화해야 합니다
   - 자세한 내용은 [ECIES-HYBRID](/docs/specs/ecies/#hybrid) 및 [Proposal 169](/proposals/169-pq-crypto/)를 참조하세요
   - 타입 코드와 사양은 변경될 수 있습니다

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### 개인 키

**설명:** 비대칭 복호화를 위한 개인 키로, PublicKey 타입에 대응합니다.

**저장:** 유형과 길이는 문맥에서 추론되거나 데이터 구조/키 파일에 별도로 저장됩니다.

**지원되는 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**보안 참고 사항:** - 개인 키는 암호학적으로 안전한 난수 생성기를 사용해 반드시 생성해야 합니다 - X25519 개인 키는 RFC 7748에 정의된 scalar clamping(스칼라 클램핑: 비밀 키의 특정 비트를 마스킹해 스칼라를 정규화하는 과정)을 사용합니다 - 키 자료는 더 이상 필요하지 않을 때 메모리에서 반드시 안전하게 삭제해야 합니다

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### 세션 키

**설명:** I2P의 tunnel 및 garlic encryption에서 AES-256 암호화와 복호화를 위한 대칭 키.

**내용:** 32바이트 (256비트)

**용도:** - Tunnel 계층 암호화 (AES-256/CBC with IV) - Garlic 메시지 암호화 - 종단 간 세션 암호화

**생성:** 암호학적으로 안전한 난수 생성기를 반드시 사용해야 한다.

**JavaDoc(자바 문서):** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**설명:** 서명 검증을 위한 공개 키. 유형과 길이는 Destination(I2P 목적지)의 키 인증서에 명시되어 있거나, 문맥에서 추론됩니다.

**기본 유형:** DSA_SHA1 (0.9.58부터 사용 중단됨)

**지원되는 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**구현 요구 사항:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - 현재 표준:**
   - 2015년 말부터 모든 신규 Router Identity와 Destination(목적지)에 대한 기본값
   - SHA-512 해시와 Ed25519 곡선을 사용
   - 32바이트 공개키, 64바이트 서명
   - 리틀엔디언 인코딩(대부분의 다른 유형과 달리)
   - 높은 성능과 보안


3. **DSA_SHA1 (Type 0) - 레거시:**
   - 0.9.58부터 Router Identities에서는 사용 중단됨
   - 새로운 Destinations에는 권장되지 않음
   - SHA-1을 사용하는 1024비트 DSA(알려진 취약점 있음)
   - 호환성 유지를 위해서만 지원됨

4. **다중 요소 키:**
   - 두 개의 요소로 구성된 경우(예: ECDSA(타원 곡선 디지털 서명 알고리즘) 점 X,Y)
   - 각 요소는 선행 0으로 채워 길이/2가 되도록 패딩
   - 예: 64바이트 ECDSA 키 = 32바이트 X + 32바이트 Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**설명:** 서명을 생성하기 위한 개인 키로, SigningPublicKey(서명 공개키) 타입에 대응합니다.

**저장소:** 생성 시 유형과 길이가 지정됩니다.

**지원되는 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**보안 요구사항:** - 암호학적으로 안전한 난수 소스를 사용해 생성할 것 - 적절한 접근 제어로 보호할 것 - 사용 후 메모리에서 안전하게 삭제할 것 - EdDSA의 경우: 32바이트 시드를 SHA-512로 해시하고, 처음 32바이트를 스칼라로 사용(clamped, 클램핑) - RedDSA의 경우: 키 생성 방식이 다름(클램핑 대신 모듈러 감소)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### 서명

**Description:** 데이터에 대한 암호학적 서명으로, SigningPrivateKey 타입(서명용 개인 키 타입)에 해당하는 서명 알고리즘을 사용합니다.

**유형 및 길이:** 서명에 사용된 키 유형에서 유추됩니다.

**지원되는 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**형식 참고 사항:** - 다중 요소 서명(예: ECDSA R, S 값)은 각 요소를 선행 0으로 채워 length/2가 되도록 패딩됩니다 - EdDSA 및 RedDSA는 리틀 엔디언 인코딩을 사용합니다 - 그 밖의 모든 유형은 빅 엔디언 인코딩을 사용합니다

**검증:** - 해당하는 SigningPublicKey를 사용하십시오 - 키 유형에 맞는 서명 알고리즘 사양을 따르십시오 - 서명 길이가 해당 키 유형의 예상 길이와 일치하는지 확인하십시오

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### 해시

**설명:** 데이터의 SHA-256 해시로, 무결성 검증과 식별을 위해 I2P 전반에서 사용됩니다.

**내용:** 32 바이트 (256 비트)

**용도:** - Router Identity 해시(네트워크 데이터베이스 키) - Destination 해시(네트워크 데이터베이스 키) - Leases에서 Tunnel 게이트웨이 식별 - 데이터 무결성 검증 - Tunnel ID 생성

**알고리즘:** FIPS 180-4에 정의된 SHA-256

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### 세션 태그

**설명:** 세션 식별 및 태그 기반 암호화에 사용되는 난수.

**중요:** 세션 태그(Session Tag) 크기는 암호화 유형에 따라 달라집니다: - **ElGamal/AES+SessionTag:** 32 바이트 (레거시) - **ECIES-X25519:** 8 바이트 (현재 표준)

**현재 표준 (ECIES, 타원 곡선 통합 암호화 방식):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
자세한 사양은 [ECIES](/docs/specs/ecies/) 및 [ECIES-ROUTERS](/docs/specs/ecies/#routers)를 참조하세요.

**레거시 (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**생성:** 반드시 암호학적으로 안전한 난수 생성기를 사용해야 한다.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html) (세션 태그)

---

### TunnelId

**Description:** router의 tunnel 내 위치를 나타내는 고유 식별자입니다. tunnel의 각 홉은 고유한 TunnelId(터널에서 해당 홉의 위치를 나타내는 고유 ID)를 가집니다.

**형식:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**용도:** - 각 router에서 수신/송신 tunnel 연결을 식별합니다 - tunnel 체인의 각 홉마다 서로 다른 TunnelId - 게이트웨이 tunnel을 식별하기 위해 Lease 구조체에서 사용됩니다

**특수 값:** - `0` = 특수 프로토콜 용도로 예약됨(일반 운용에서는 사용을 피해야 함) - TunnelIds는 각 router에 대해 로컬에서만 유효합니다

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## 인증서 명세

### 인증서

**설명:** I2P 전반에서 사용되는 영수증, 작업 증명, 또는 암호학적 메타데이터를 담는 컨테이너.

**형식:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**총 크기:** 최소 3바이트(NULL 인증서), 최대 65538바이트

### 인증서 유형

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### 키 인증서(유형 5)

**소개:** 버전 0.9.12 (2013년 12월)

**Purpose:** 기본값이 아닌 키 유형을 지정하며, 표준 384바이트 KeysAndCert(키와 인증서) 구조를 넘어서는 초과 키 데이터를 저장합니다.

**페이로드 구조:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**중요 구현 참고 사항:**

1. **키 유형 순서:**
   - **경고:** 서명 키 유형이 암호화 키 유형보다 먼저 옵니다
   - 이는 직관에 반하지만 호환성을 위해 유지됩니다
   - 순서: SPKtype, CPKtype (CPKtype, SPKtype 아님)

2. **KeysAndCert(키와 인증서 데이터 구조)에서의 키 데이터 레이아웃:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **초과 키 데이터 계산:**
   - Crypto Key > 256 바이트인 경우: Excess = (Crypto Length - 256)
   - Signing Key > 128 바이트인 경우: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**예시 (ElGamal 암호 키):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Router Identity 요구사항:** - NULL certificate(NULL 인증서)는 버전 0.9.15까지 사용됨 - Key Certificate(키 인증서)는 기본이 아닌 키 유형에 0.9.16부터 필요함 - X25519 암호화 키는 0.9.48부터 지원됨

**Destination(목적지) 요구 사항:** - NULL 인증서 또는 키 인증서(필요한 경우) - 기본값이 아닌 서명 키 유형에는 0.9.12부터 키 인증서가 필요 - 암호화 공개 키 필드는 0.6(2005)부터 사용되지 않지만 여전히 존재해야 함

**중요한 경고:**

1. **NULL 대 KEY Certificate:**
   - ElGamal+DSA_SHA1을 지정하는 types (0,0)의 KEY certificate(키 인증서)는 허용되지만 권장되지 않습니다
   - ElGamal+DSA_SHA1의 경우 항상 NULL certificate(NULL 인증서)를 사용하세요(정규 표현)
   - (0,0)을 사용하는 KEY certificate는 4바이트 더 길며 호환성 문제를 일으킬 수 있습니다
   - 일부 구현체는 (0,0) KEY certificate를 올바르게 처리하지 못할 수 있습니다

2. **초과 데이터 검증:**
   - 구현체는 키 유형에 대해 기대되는 길이와 인증서 길이가 일치하는지 반드시 검증해야 한다
   - 키 유형과 부합하지 않는 초과 데이터가 포함된 인증서는 거부해야 한다
   - 유효한 인증서 구조 뒤에 이어지는 trailing garbage data(끝부분의 불필요한 잔여 데이터)를 금지해야 한다

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### 매핑

**설명:** 구성 및 메타데이터에 사용되는 키-값 속성 컬렉션.

**형식:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**크기 제한:** - 키 길이: 0-255 바이트 (+ 길이 바이트 1개) - 값 길이: 0-255 바이트 (+ 길이 바이트 1개) - 전체 매핑 크기: 0-65535 바이트 (+ 크기 필드 바이트 2개) - 구조체의 최대 크기: 65537 바이트

**핵심 정렬 요구사항:**

**서명된 구조체**(RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig)에서 매핑이 나타나는 경우, 서명 불변성을 보장하기 위해 항목은 키 순으로 반드시 정렬되어야 합니다:

1. **정렬 방법:** 유니코드 코드 포인트 값(Unicode code point values)을 사용한 사전식 정렬 (Java String.compareTo()와 동일)
2. **대소문자 구분:** 키와 값은 일반적으로 대소문자를 구분함(애플리케이션에 따라 다름)
3. **중복 키:** 서명된 구조에서는 허용되지 않음(서명 검증 실패 발생)
4. **문자 인코딩:** UTF-8 바이트 수준 비교

**정렬이 중요한 이유:** - 서명은 바이트 표현을 기준으로 계산됩니다 - 키의 순서가 다르면 서로 다른 서명이 생성됩니다 - 서명되지 않은 매핑은 정렬이 필수는 아니지만 같은 관례를 따르는 것이 권장됩니다

**구현 참고 사항:**

1. **인코딩 중복성:**
   - `=` 및 `;` 구분자와 문자열 길이 바이트가 모두 존재합니다
   - 이는 비효율적이지만 호환성을 위해 유지됩니다
   - 길이 바이트가 기준이며; 구분자는 필요하지만 중복입니다

2. **문자 지원:**
   - 문서와 달리, 문자열 내에서는 `=`과 `;`가 실제로 지원됩니다(길이 바이트가 이를 처리합니다)
   - UTF-8 인코딩은 전체 유니코드를 지원합니다
   - **경고:** I2CP는 UTF-8을 사용하지만, I2NP는 역사적으로 UTF-8을 올바르게 처리하지 못했습니다
   - 최대 호환성을 위해 가능한 경우 I2NP 매핑에는 ASCII를 사용하세요

3. **특수 컨텍스트:**
   - **RouterInfo/RouterAddress:** 반드시 정렬되어야 하며, 중복이 없어야 함
   - **I2CP SessionConfig:** 반드시 정렬되어야 하며, 중복이 없어야 함  
   - **애플리케이션 매핑:** 정렬을 권장하지만 항상 필요한 것은 아님

**예시 (RouterInfo 옵션):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## 공통 구조 명세

### 키와 인증서

**설명:** 암호화 키, 서명 키, 인증서를 결합한 기본 구조. RouterIdentity와 Destination 모두로 사용됩니다.

**구조:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**키 정렬:** - **암호화 공개 키:** 시작에 정렬됨 (바이트 0) - **패딩:** 중간에 (필요한 경우) - **서명 공개 키:** 끝에 정렬됨 (바이트 256부터 바이트 383까지) - **인증서:** 바이트 384부터 시작

**크기 계산:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### 패딩 생성 지침 ([Proposal 161](/ko/proposals/161-ri-dest-padding/))

**구현 버전:** 0.9.57 (2023년 1월, 릴리스 2.1.0)

**배경:** - ElGamal+DSA가 아닌 키의 경우, 384바이트 고정 길이 구조에 패딩이 존재함 - Destinations(목적지)의 경우, 256바이트 공개 키 필드는 0.6(2005)부터 사용되지 않음 - 패딩은 보안을 유지하면서도 압축 가능하도록 생성되어야 함

**요구 사항:**

1. **최소 난수 데이터:**
   - 암호학적으로 안전한 난수 데이터를 최소 32바이트 이상 사용하세요
   - 이는 보안을 위해 충분한 엔트로피를 제공합니다

2. **압축 전략:**
   - 패딩/공개 키 필드 전체에 걸쳐 해당 32바이트를 반복
   - I2NP Database Store, 스트리밍 SYN, SSU2 핸드셰이크와 같은 프로토콜은 압축을 사용
   - 보안을 저해하지 않으면서 상당한 대역폭 절감

3. **예시:**

**Router 신원 (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destination (목적지) (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **이 방법이 통하는 이유:**
   - 전체 구조의 SHA-256 해시는 여전히 모든 엔트로피를 포함합니다
   - 네트워크 데이터베이스 DHT(분산 해시 테이블) 분산은 오직 해시에만 의존합니다
   - 서명 키(32바이트 EdDSA/X25519)는 256비트의 엔트로피를 제공합니다
   - 추가적인 32바이트의 반복된 난수 데이터 = 총 512비트 엔트로피
   - 암호학적 강도 측면에서 충분하고도 남습니다

5. **구현 참고 사항:**
   - 387바이트 이상인 전체 구조체를 반드시 저장하고 전송해야 함
   - SHA-256 해시는 압축되지 않은 전체 구조체에 대해 계산됨
   - 압축은 프로토콜 계층(I2NP, Streaming, SSU2)에서 적용됨
   - 버전 0.6(2005) 이후의 모든 버전과 하위 호환

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (router 식별자)

**Description:** I2P 네트워크에서 router를 고유하게 식별합니다. KeysAndCert와 동일한 구조입니다.

**형식:** 위의 KeysAndCert 구조를 참조하세요

**현재 요구 사항(0.9.58 기준):**

1. **필수 키 유형:**
   - **암호화:** X25519 (타원 곡선 기반 키 교환 알고리즘) (type 4, 32 바이트)
   - **서명:** EdDSA_SHA512_Ed25519 (Ed25519 기반 EdDSA 서명 알고리즘) (type 7, 32 바이트)
   - **인증서:** 키 인증서 (type 5)

2. **사용 중단된 키 유형:**
   - ElGamal (type 0)은 0.9.58부터 Router Identities에서 사용 중단되었습니다
   - DSA_SHA1 (type 0)은 0.9.58부터 Router Identities에서 사용 중단되었습니다
   - 이러한 키는 새로운 router에는 절대 사용하면 안 됩니다

3. **일반적인 크기:**
   - Key Certificate를 포함한 X25519 + EdDSA = 391바이트
   - 32바이트 X25519 공개 키
   - 320바이트 패딩 ([Proposal 161](/ko/proposals/161-ri-dest-padding/)에 따라 압축 가능)
   - 32바이트 EdDSA 공개 키
   - 7바이트 인증서 (3바이트 헤더 + 4바이트 키 유형)

**변천사:** - 0.9.16 이전: 항상 NULL 인증서 사용 (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Key Certificate(키 인증서) 지원이 추가됨 - 0.9.48+: X25519 암호화 키 지원 - 0.9.58+: ElGamal 및 DSA_SHA1 더 이상 권장되지 않음

**네트워크 데이터베이스 키:** - RouterInfo는 완전한 RouterIdentity의 SHA-256 해시를 키로 사용 - 해시는 패딩을 포함한 391바이트+의 전체 구조에 대해 계산됨

**참고:** - 패딩 생성 지침 ([제안서 161](/ko/proposals/161-ri-dest-padding/)) - 위의 Key Certificate 사양

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### 목적지

**설명:** 보안 메시지 전달을 위한 엔드포인트 식별자. 구조적으로는 KeysAndCert와 동일하지만, 사용 의미가 다릅니다.

**형식:** 위의 KeysAndCert 구조를 참조하십시오

**RouterIdentity(라우터 식별자)와의 중요한 차이점:** - **공개 키 필드는 사용되지 않으며 임의의 데이터가 포함될 수 있습니다** - 이 필드는 버전 0.6 (2005)부터 사용되지 않았습니다 - 원래는 구식 I2CP-to-I2CP 암호화를 위한 것이었습니다(비활성화됨) - 현재는 더 이상 권장되지 않는 LeaseSet 암호화를 위한 IV(초기화 벡터)로만 사용됩니다

**현재 권장 사항:**

1. **서명 키:**
   - **권장:** EdDSA_SHA512_Ed25519 (유형 7, 32바이트)
   - 대안: 구버전 호환을 위한 ECDSA 유형
   - 지양: DSA_SHA1 (사용 중단됨, 권장하지 않음)

2. **암호화 키:**
   - 필드는 사용되지 않지만 반드시 존재해야 함
   - **권장:** [Proposal 161](/ko/proposals/161-ri-dest-padding/)에 따라 무작위 데이터로 채울 것(압축 가능)
   - 크기: 항상 256바이트(ElGamal에는 사용되지 않지만 ElGamal 슬롯)

3. **인증서:**
   - ElGamal + DSA_SHA1용 NULL 인증서(레거시 전용)
   - 기타 모든 서명 키 유형에 대한 키 인증서

**일반적인 최신 Destination(목적지):**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**실제 암호화 키:** - Destination(목적지)를 위한 암호화 키는 **LeaseSet**에 있으며, Destination에 있지 않다 - LeaseSet에는 현재 암호화 공개키가 포함되어 있다 - 암호화 키 처리는 LeaseSet2 사양을 참조하세요

**네트워크 데이터베이스 키:** - LeaseSet는 완전한 Destination(목적지)의 SHA-256 해시를 키로 사용 - 해시는 387바이트 이상인 전체 구조에 대해 계산됨

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## 네트워크 데이터베이스 구조

### Lease(리스; I2P에서 수신용 tunnel 정보를 담는 항목)

**설명:** 특정 tunnel에 Destination(목적지)에 대한 메시지를 수신할 수 있도록 권한을 부여합니다. 원래 LeaseSet 형식(type 1)의 일부입니다.

**형식:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**총 크기:** 44바이트

**사용:** - 원래 LeaseSet(유형 1, 사용 중단됨)에서만 사용됨 - LeaseSet2 및 이후 변형에서는 대신 Lease2를 사용

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (I2P에서 목적지에 도달 가능한 tunnel과 키 정보를 포함하는 데이터 구조) (Type 1)

**설명:** 기존 LeaseSet 형식. Destination(목적지)에 대한 승인된 tunnels 및 키를 포함합니다. 네트워크 데이터베이스(netDb)에 저장됩니다. **상태: 사용 중단됨** (대신 LeaseSet2를 사용하세요).

**구조:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**데이터베이스 저장소:** - **데이터베이스 유형:** 1 - **키:** Destination(목적지 식별자)의 SHA-256 해시 - **값:** 완전한 LeaseSet 구조

**중요한 참고 사항:**

1. **Destination(목적지 식별자) 공개 키는 사용되지 않음:**
   - Destination의 암호화용 공개 키 필드는 사용되지 않음
   - LeaseSet의 암호화 키가 실제 암호화 키임

2. **임시 키:**
   - `encryption_key`는 임시 키입니다 (router 시작 시 재생성됨)
   - `signing_key`는 임시 키입니다 (router 시작 시 재생성됨)
   - 두 키 모두 재시작해도 유지되지 않습니다

3. **철회(미구현):**
   - `signing_key`는 LeaseSet(I2P에서 목적지 접근 정보를 담는 데이터 구조) 철회를 위해 의도되었음
   - 철회 메커니즘은 한 번도 구현되지 않음
   - 리스가 0개인 LeaseSet은 철회를 위해 의도되었으나 사용되지 않음

4. **버전 관리/타임스탬프:**
   - LeaseSet에는 명시적인 `published` 타임스탬프 필드가 없다
   - 버전은 모든 lease(LeaseSet을 구성하는 개별 항목)의 만료 시각 중 가장 이른 값이다
   - 새로운 LeaseSet이 수락되려면 lease 만료 시각이 더 이른 값이어야 한다

5. **Lease(리스: leaseSet을 구성하는 항목) 만료 게시:**
   - 0.9.7 이전: 모든 lease를 동일한 만료 시간(가장 이른 시간)으로 게시
   - 0.9.7+: 개별 lease의 실제 만료 시간을 게시
   - 이는 구현상의 세부 사항이며, 명세의 일부가 아님

6. **Lease 0개:**
   - Lease(수신 터널 정보 항목)가 0개인 LeaseSet은 기술적으로 허용됩니다
   - 철회 용도로 의도되었음(미구현)
   - 실제로는 사용되지 않습니다
   - LeaseSet2 변형은 최소한 하나의 Lease가 필요합니다

**사용 중단:** LeaseSet type 1은 사용 중단되었습니다. 새 구현체는 **LeaseSet2 (type 3)**를 사용해야 하며, 다음을 제공합니다: - 발행 타임스탬프 필드(더 나은 버전 관리) - 다중 암호화 키 지원 - 오프라인 서명 기능 - 4바이트 리스(lease) 만료(8바이트 대비) - 더 유연한 옵션

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet 변형

### Lease2 (I2P의 LeaseSet2를 구성하는 개별 항목)

**Description:** 만료 시간을 4바이트로 표현하는 개선된 lease(리스) 형식. LeaseSet2 (type 3) 및 MetaLeaseSet (type 7)에서 사용됨.

**소개:** 버전 0.9.38 (자세한 내용은 [Proposal 123](/proposals/123-new-netdb-entries/) 참조)

**형식:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**총 크기:** 40바이트 (원래 Lease보다 4바이트 더 작음)

**원래 Lease(리스)와의 비교:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### 오프라인 서명

**Description:** 사전 서명된 임시 키를 위한 선택적 구조로, Destination(데스티네이션)의 개인 서명 키에 온라인으로 접근하지 않고도 LeaseSet을 게시할 수 있게 합니다.

**소개:** 버전 0.9.38 (자세한 내용은 [제안 123](/proposals/123-new-netdb-entries/) 참조)

**형식:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**목적:** - 오프라인 LeaseSet 생성을 가능하게 함 - Destination(목적지 식별자) 마스터 키를 온라인 노출로부터 보호 - 오프라인 서명 없이 새로운 LeaseSet을 게시하여 임시 키를 폐기할 수 있음

**사용 시나리오:**

1. **고보안 목적지:**
   - 마스터 서명 키는 오프라인에 보관 (HSM, 콜드 스토리지)
   - 제한된 기간 동안 사용할 임시 키를 오프라인에서 생성
   - 침해된 임시 키로 인해 마스터 서명 키가 노출되지 않음

2. **Encrypted LeaseSet 발행:**
   - EncryptedLeaseSet에는 오프라인 서명을 포함할 수 있습니다
   - Blinded public key(블라인딩된 공개키) + 오프라인 서명은 추가적인 보안을 제공합니다

**보안 고려사항:**

1. **만료 관리:**
   - 합리적인 만료 기간을 설정하세요(수년이 아닌 수일~수주)
   - 만료되기 전에 새로운 임시 키를 생성하세요
   - 짧은 만료 기간 = 더 나은 보안, 더 많은 유지관리

2. **키 생성:**
   - 보안된 환경에서 오프라인으로 임시 키 생성
   - 오프라인에서 마스터 키로 서명
   - 서명된 임시 키 + 서명만 온라인 router로 전송

3. **철회:**
   - 오프라인 서명 없이 새로운 LeaseSet을 게시하여 암묵적으로 철회
   - 또는 다른 transient key(일시적 키)를 사용한 새로운 LeaseSet을 게시

**서명 검증:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**구현 참고:** - 총 크기는 sigtype 및 Destination(목적지)의 서명 키 유형에 따라 달라집니다 - 최소 크기: 4 + 2 + 32 (EdDSA 키) + 64 (EdDSA 서명) = 102 바이트 - 실질적인 최대 크기: ~600 바이트 (RSA-4096 임시 키 + RSA-4096 서명)

**다음과 호환됩니다:** - LeaseSet2 (유형 3) - EncryptedLeaseSet (유형 5) - MetaLeaseSet (유형 7)

**참고:** 오프라인 서명 프로토콜에 대한 자세한 내용은 [제안 123](/proposals/123-new-netdb-entries/)을 참조하세요.

---

### LeaseSet2Header(LeaseSet2의 헤더)

**설명:** LeaseSet2(유형 3) 및 MetaLeaseSet(유형 7)에 대한 공통 헤더 구조.

**소개:** 버전 0.9.38 ([제안 123](/proposals/123-new-netdb-entries/) 참조)

**형식:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**최소 총 크기:** 395 바이트 (오프라인 서명 제외)

**플래그 정의 (비트 순서: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**플래그 세부 정보:**

**비트 0 - 오프라인 키:** - `0`: 오프라인 서명이 없으며, Destination(목적지)의 서명 키로 LeaseSet 서명을 검증 - `1`: OfflineSignature(오프라인 서명) 구조가 flags 필드 뒤에 이어짐

**비트 1 - 미게시:** - `0`: 표준으로 게시된 LeaseSet이며, floodfills로 전파되어야 함 - `1`: 미게시 LeaseSet (클라이언트 측 전용)   - 전파되거나 게시되거나 쿼리에 대한 응답으로 전송되어서는 안 됨   - 만료된 경우, 대체 항목을 찾기 위해 netdb를 쿼리하지 말 것(비트 2도 설정된 경우는 예외)   - 로컬 tunnels 또는 테스트용으로 사용

**비트 2 - Blinded(블라인드 처리) (0.9.42부터):** - `0`: 표준 LeaseSet - `1`: 이 암호화되지 않은 LeaseSet은 게시 시 blinded 및 암호화됩니다   - 게시된 버전은 EncryptedLeaseSet (type 5)입니다   - 만료되면 대체본을 위해 netdb의 **blinded location**을 조회합니다   - 비트 1도 1로 설정해야 합니다(미게시 + blinded)   - 암호화된 은닉 서비스에 사용됩니다

**만료 제한:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**발행 타임스탬프 요구사항:**

LeaseSet (타입 1)에는 published 필드가 없어 버전 관리를 위해 가장 이른 lease(리스: I2P의 임시 통신 경로 항목) 만료 시점을 찾아야 했다. LeaseSet2는 1초 해상도의 명시적인 `published` 타임스탬프를 추가한다.

**중요 구현 참고:** - Routers는 각 Destination(목적지 식별자)마다 LeaseSet 게시 빈도를 초당 한 번보다 훨씬 느리게 제한해야 한다 - 더 빠르게 게시해야 한다면, 각 새로운 LeaseSet의 `published` 시간이 최소 1초 이후가 되도록 보장하라 - `published` 시간이 현재 버전보다 더 새롭지 않으면 Floodfills는 LeaseSet을 거부한다 - 권장 최소 간격: 게시 간 10-60초

**계산 예제:**

**LeaseSet2 (최대 11분):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet(메타 leaseSet) (최대 18.2시간):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**버전 관리:** - `published` 타임스탬프가 더 크면 LeaseSet은 '더 최신'으로 간주됩니다 - Floodfills는 가장 최신 버전만 저장하고 전파합니다 - 가장 오래된 Lease(터널 임대 엔트리)가 이전 LeaseSet의 가장 오래된 Lease와 일치하는 경우에 주의하세요

---

### LeaseSet2 (유형 3)

**설명:** 여러 개의 암호화 키, 오프라인 서명 및 서비스 레코드를 지원하는 최신 LeaseSet(서비스 주소 데이터 구조) 형식입니다. I2P 히든 서비스의 현재 표준입니다.

**소개:** 버전 0.9.38 ([Proposal 123](/proposals/123-new-netdb-entries/) 참조)

**구조:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**데이터베이스 저장 방식:** - **데이터베이스 유형:** 3 - **키:** Destination(I2P 목적지 식별자)의 SHA-256 해시 - **값:** 완전한 LeaseSet2 구조체

**서명 계산:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### 암호화 키 선호 순서

**공개된 (서버) LeaseSet의 경우:** - 키는 서버 선호도 순으로 나열(가장 선호되는 것부터) - 여러 유형을 지원하는 클라이언트는 서버 선호도를 준수해야 한다 - 목록에서 지원되는 첫 번째 유형을 선택 - 일반적으로 번호가 더 높은(더 최신) 키 유형이 보안성과 효율성이 더 높다 - 권장 순서: 키를 유형 코드의 역순으로 나열(최신이 먼저)

**서버 설정 예시:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**게시되지 않은(클라이언트) LeaseSet:** - 키 순서는 실제로 중요하지 않습니다(클라이언트에 대한 연결 시도가 드뭅니다) - 일관성을 위해 동일한 관례를 따르십시오

**클라이언트 키 선택:** - 서버의 선호를 존중 (지원되는 유형 중 첫 번째를 선택) - 또는 구현에서 정의한 선호도 사용 - 또는 양측의 기능을 기반으로 결합된 선호도를 결정

### 옵션 매핑

**요구 사항:** - 옵션은 키 기준으로 반드시 정렬되어야 함 (사전식(lexicographic), UTF-8 바이트 순서) - 정렬은 서명 불변성을 보장함 - 중복 키는 허용되지 않음

**표준 형식 ([제안 167](/proposals/167-service-records/)):**

API 0.9.66(2025년 6월, 릴리스 2.9.0) 기준으로, service record(서비스 레코드) 옵션은 표준화된 형식을 따릅니다. 전체 사양은 [Proposal 167](/proposals/167-service-records/)을 참조하세요.

**서비스 레코드 옵션 형식:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**서비스 레코드 예시:**

**1. 자기-참조 SMTP 서버:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. 단일 외부 SMTP 서버:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. 여러 SMTP 서버(부하 분산):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. 앱 옵션이 있는 HTTP 서비스:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**TTL(Time To Live) 권장 사항:** - 최소: 86400초 (1일) - 더 긴 TTL은 netdb 쿼리 부하를 줄입니다 - 쿼리 감소와 서비스 업데이트 전파 간의 균형 - 안정적인 서비스의 경우: 604800 (7일) 이상

**구현 참고 사항:**

1. **암호화 키 (0.9.44 기준):**
   - ElGamal (유형 0, 256바이트): 레거시 호환성
   - X25519 (유형 4, 32바이트): 현재 표준
   - MLKEM 변형: 포스트-양자 (베타, 최종 확정 아님)

2. **키 길이 유효성 검사:**
   - Floodfills와 클라이언트는 알 수 없는 키 유형도 반드시 파싱할 수 있어야 합니다
   - 알 수 없는 키를 건너뛰기 위해 keylen 필드를 사용하세요
   - 키 유형이 알 수 없는 경우에도 파싱을 실패로 처리하지 마십시오

3. **발행 타임스탬프:**
   - 발행 속도 제한(rate-limiting)에 관한 LeaseSet2Header의 참고 사항을 참조하십시오
   - 발행 간 최소 증가 간격 1초
   - 권장: 발행 간 10-60초

4. **암호화 유형 마이그레이션:**
   - 여러 키 사용으로 점진적 마이그레이션 지원
   - 전환 기간 동안 기존 키와 새 키를 모두 나열
   - 충분한 클라이언트 업그레이드 기간 이후 기존 키 제거

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease

**설명:** tunnels 대신 다른 LeaseSets를 참조할 수 있는 MetaLeaseSet(메타 형태의 LeaseSet 유형)을 위한 Lease 구조. 부하 분산과 이중화를 위해 사용된다.

**소개:** 버전 0.9.38, 0.9.40에서 적용 예정 (참고 [Proposal 123](/proposals/123-new-netdb-entries/))

**형식:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**총 크기:** 40 바이트

**엔트리 유형 (플래그 비트 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**사용 시나리오:**

1. **부하 분산:**
   - 여러 MetaLease(개별 LeaseSet을 가리키는 엔트리) 엔트리가 포함된 MetaLeaseSet(여러 LeaseSet을 묶는 메타 집합)
   - 각 엔트리는 서로 다른 LeaseSet2(LeaseSet의 새로운 버전)를 가리킵니다
   - 클라이언트는 cost 필드를 기준으로 선택합니다

2. **이중화:**
   - 백업 LeaseSets를 가리키는 여러 항목
   - 기본 LeaseSet을 사용할 수 없을 때의 대체

3. **서비스 마이그레이션:**
   - MetaLeaseSet이 새로운 LeaseSet을 가리킴
   - Destinations(데스티네이션, I2P의 목적지/주소 식별자) 간 원활한 전환을 허용

**Cost 필드 사용:** - 낮은 Cost = 더 높은 우선순위 - Cost 0 = 가장 높은 우선순위 - Cost 255 = 가장 낮은 우선순위 - 클라이언트는 더 낮은 Cost의 항목을 선호하는 것이 권장됩니다 - 동일한 Cost의 항목은 무작위로 부하 분산될 수 있습니다

**Lease2와의 비교:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet(메타 리스셋) (유형 7)

**설명:** MetaLease(다른 LeaseSet에 대한 간접 참조를 제공하는 메타 항목) 항목을 포함하는 LeaseSet의 변형으로, 이를 통해 다른 LeaseSet에 대한 간접 참조를 제공합니다. 부하 분산, 중복성, 서비스 마이그레이션에 사용됩니다.

**소개:** 0.9.38에서 정의되었으며, 0.9.40에서 동작하도록 예정됨 ( [제안 123](/proposals/123-new-netdb-entries/) 참조)

**상태:** 명세가 완료되었습니다. 프로덕션 배포 상태는 현재 I2P 릴리스에서 확인해야 합니다.

**구조:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**데이터베이스 저장:** - **데이터베이스 유형:** 7 - **키:** Destination의 SHA-256 해시 - **값:** 완전한 MetaLeaseSet(메타 리스셋) 구조

**서명 계산:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**사용 시나리오:**

**1. 부하 분산:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Failover(장애 조치):**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. 서비스 마이그레이션:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. 다층 아키텍처:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**철회 목록:**

무효화 목록은 MetaLeaseSet(메타 LeaseSet)이 이전에 게시된 LeaseSets를 명시적으로 무효화할 수 있게 합니다:

- **목적:** 특정 Destination을 더 이상 유효하지 않도록 표시
- **내용:** 폐기된 Destination 구조체의 SHA-256 해시
- **사용:** Destination 해시가 폐기 목록에 포함된 LeaseSet은 클라이언트가 사용해서는 안 된다
- **일반적인 값:** 대부분의 배포에서 비어 있음(numr=0)

**예시 철회:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**만료 처리:**

MetaLeaseSet(메타 LeaseSet)은 최대 expires=65535초(약 18.2시간)인 LeaseSet2Header를 사용합니다:

- LeaseSet2보다 만료 시간이 훨씬 더 김(최대 ~11분)
- 상대적으로 정적인 간접 참조에 적합
- 참조된 LeaseSets의 만료 시간은 더 짧을 수 있음
- 클라이언트는 MetaLeaseSet(메타 LeaseSet)과 참조된 LeaseSets 둘 다의 만료 시간을 확인해야 함

**옵션 매핑:**

- LeaseSet2 옵션과 동일한 형식을 사용
- 서비스 레코드를 포함할 수 있음 ([Proposal 167](/proposals/167-service-records/))
- 반드시 키로 정렬되어야 함
- 서비스 레코드는 일반적으로 간접화 구조(indirection structure)가 아니라 최종 서비스(ultimate service)를 설명함

**클라이언트 구현 참고 사항:**

1. **해결 절차:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **캐싱:**
   - MetaLeaseSet(여러 LeaseSet을 묶어 참조하는 메타 세트)와 참조된 LeaseSets(목적지의 tunnel 라우팅 정보를 담은 데이터 세트) 모두를 캐시
   - 두 레벨 모두의 만료 여부를 확인
   - 업데이트된 MetaLeaseSet 게시를 모니터링

3. **장애 조치:**
   - 선호 엔트리가 실패하면, 다음으로 낮은 비용의 엔트리를 시도
   - 실패한 엔트리를 일시적으로 사용 불가로 표시하는 것을 고려
   - 복구 여부를 주기적으로 다시 확인

**구현 상태:**

[제안 123](/proposals/123-new-netdb-entries/)는 일부 부분이 “개발 중” 상태로 남아 있음을 명시합니다. 구현자들은 다음을 수행해야 합니다: - 대상 I2P 버전에서 운영 환경 투입 준비 여부를 확인 - 배포 전에 MetaLeaseSet(메타 leaseSet 구조) 지원을 테스트 - 최신 I2P 릴리스에서 업데이트된 사양이 있는지 확인

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (유형 5)

**Description:** 프라이버시 강화를 위해 암호화되고 블라인딩된 LeaseSet입니다. 블라인딩된 공개 키와 메타데이터만 보이며, 실제 리스와 암호화 키는 암호화되어 있습니다.

**소개:** 0.9.38에서 정의, 0.9.39에서 동작 ([Proposal 123](/proposals/123-new-netdb-entries/) 참조)

**구조:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**데이터베이스 저장소:** - **데이터베이스 유형:** 5 - **키:** **blinded Destination**(익명화 처리된 Destination)의 SHA-256 해시 (원래 Destination이 아님) - **값:** 완전한 EncryptedLeaseSet 구조체

**LeaseSet2와의 핵심 차이점:**

1. **LeaseSet2Header 구조를 사용하지 않습니다** (유사한 필드를 갖지만 레이아웃이 다름)
2. **블라인드된 공개 키**를 전체 Destination(I2P 목적지 식별자) 대신 사용
3. **암호화된 페이로드**를 평문의 leases와 키 대신 사용
4. **데이터베이스 키는 블라인드된 Destination의 해시입니다**, 원래 Destination이 아닙니다

**서명 계산:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**서명 유형 요구 사항:**

**반드시 RedDSA_SHA512_Ed25519 (type 11)을 사용해야 합니다:** - 32바이트 블라인딩된 공개키 - 64바이트 서명 - 블라인딩 보안 속성을 위해 필수 - 참조 [Red25519 specification](//docs/specs/red25519-signature-scheme/

**EdDSA와의 주요 차이점:** - 개인 키는 modular reduction(모듈러 환원)로 생성(clamping(클램핑) 아님) - 서명에 80바이트의 난수 데이터 포함 - 공개 키를 직접 사용(해시가 아님) - 안전한 blinding(블라인딩; 원본을 숨기기 위한 난수 마스킹) 연산을 가능하게 함

**블라인딩과 암호화:**

자세한 내용은 [EncryptedLeaseSet 사양](/docs/specs/encryptedleaseset/)을 참조하세요:

**1. 키 블라인딩:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. 데이터베이스 위치:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. 암호화 계층(3계층):**

**레이어 1 - 인증 레이어 (클라이언트 액세스):** - 암호화: ChaCha20 스트림 암호 - 키 파생: 클라이언트별 비밀값을 사용하는 HKDF(해시 기반 키 파생 함수) - 인증된 클라이언트는 외부 레이어를 복호화할 수 있음

**레이어 2 - 암호화 계층:** - 암호화: ChaCha20 - 키: 클라이언트와 서버 간 DH(디피-헬먼 키 교환)에서 파생 - 실제 LeaseSet2 또는 MetaLeaseSet을 포함

**레이어 3 - 내부 LeaseSet:** - 완전한 LeaseSet2 또는 MetaLeaseSet - 모든 tunnels, 암호화 키, 옵션 포함 - 성공적으로 복호화된 후에만 접근 가능

**암호화 키 파생:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**발견 과정:**

**인가된 클라이언트용:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**권한 없는 클라이언트의 경우:** - EncryptedLeaseSet(암호화된 leaseSet)을 찾아도 복호화할 수 없음 - 블라인딩된 버전만으로는 원래 Destination(I2P 목적지 주소)를 판별할 수 없음 - 서로 다른 블라인딩 기간(매일 로테이션) 간에는 EncryptedLeaseSets를 연계할 수 없음

**만료 시간:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**게시 타임스탬프:**

LeaseSet2Header와 동일한 요구사항: - 게시 간 타임스탬프는 최소 1초 이상 증가해야 함 - 현재 버전보다 최신이 아니면 floodfill(네트워크 데이터베이스를 유지·배포하는 노드)들이 거부함 - 권장: 게시 간 간격 10-60초

**암호화된 LeaseSets(목적지의 수신 tunnel 입구 정보 모음)와 함께하는 오프라인 서명:**

오프라인 서명 사용 시 특별 고려사항: - 블라인딩된 공개 키는 매일 순환됨 - 오프라인 서명은 새 블라인딩된 키로 매일 다시 생성해야 함 - 또는 외부 EncryptedLeaseSet이 아닌 내부 LeaseSet에 오프라인 서명을 사용 - [Proposal 123](/proposals/123-new-netdb-entries/) 노트 참고

**구현 참고 사항:**

1. **클라이언트 인가:**
   - 여러 클라이언트를 서로 다른 키로 인가할 수 있습니다
   - 각 인가된 클라이언트는 고유한 복호화 자격 증명을 가집니다
   - 인가 키를 변경하여 클라이언트의 접근 권한을 해지할 수 있습니다

2. **일일 키 로테이션:**
   - 블라인딩된 키는 UTC 기준 자정에 변경됩니다
   - 클라이언트는 매일 블라인딩된 Destination(목적지 식별자)을 재계산해야 합니다
   - 기존 EncryptedLeaseSets는 로테이션 후 더 이상 발견할 수 없게 됩니다

3. **프라이버시 특성:**
   - Floodfills는 원래 Destination(I2P 주소)를 판별할 수 없음
   - 권한이 없는 클라이언트는 서비스에 접근할 수 없음
   - 서로 다른 blinding(블라인딩) 기간은 연계될 수 없음
   - 만료 시간 외에는 평문 메타데이터가 없음

4. **성능:**
   - 클라이언트는 매일 blinding(블라인딩, 암호학적 가림) 계산을 수행해야 함
   - 3중 암호화로 인해 계산 오버헤드가 증가함
   - 복호화된 내부 LeaseSet을 캐싱하는 것을 고려

**보안 고려사항:**

1. **인가 키 관리:**
   - 클라이언트 인가 자격 증명을 안전하게 배포
   - 세밀한 단위의 철회를 위해 클라이언트별 고유 자격 증명 사용
   - 인가 키를 주기적으로 교체

2. **클록 동기화:**
   - Daily blinding(암호학적 가림 기법)은 동기화된 UTC 날짜에 의존함
   - 시계 오차는 조회 실패를 유발할 수 있음
   - 허용오차를 위해 전날/다음 날 blinding도 지원하는 것을 고려

3. **메타데이터 유출:**
   - Published 및 expires 필드는 평문이다
   - 패턴 분석으로 서비스 특성이 드러날 수 있다
   - 우려된다면 발행 간격을 무작위화하라

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router 구조

### RouterAddress (router 주소)

**설명:** 특정 전송 프로토콜을 통해 router의 연결 정보를 정의합니다.

**형식:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**치명적 - 만료 필드:**

⚠️ **만료 필드는 반드시 모두 0(제로)로 설정해야 합니다(0 값 바이트 8개).**

- **이유:** 릴리스 0.9.3 이후 0이 아닌 Expiration(만료 시간 필드) 값은 서명 검증 실패를 초래함
- **이력:** Expiration은 원래 사용되지 않았으며, 항상 null이었음
- **현재 상태:** 0.9.12 기준으로 필드가 다시 인식되었지만, 네트워크 업그레이드를 기다려야 함
- **구현:** 항상 0x0000000000000000으로 설정

만료 시간이 0이 아닌 경우 RouterInfo(라우터 정보 레코드) 서명 검증이 실패합니다.

### 전송 프로토콜

**현재 프로토콜(2.10.0 기준):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**전송 스타일 값:** - `"SSU2"`: 현재의 UDP 기반 전송 - `"NTCP2"`: 현재의 TCP 기반 전송 - `"NTCP"`: 레거시, 제거됨(사용하지 마십시오) - `"SSU"`: 레거시, 제거됨(사용하지 마십시오)

### 공통 옵션

모든 transports(전송 프로토콜)은 일반적으로 다음을 포함합니다:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### SSU2 전용 옵션

자세한 내용은 [SSU2 명세서](/docs/specs/ssu2/)를 참조하십시오.

**필수 옵션:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**선택적 옵션:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**SSU2 RouterAddress 예시:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### NTCP2 전용 옵션

자세한 내용은 [NTCP2 사양](/docs/specs/ntcp2/)을 참조하십시오.

**필수 옵션:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**선택 옵션(0.9.50부터):**

```
"caps" = Capability string
```
**NTCP2 RouterAddress 예시:**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### 구현 참고 사항

1. **비용 값:**
   - UDP (SSU2)는 효율성으로 인해 일반적으로 더 낮은 비용(5-6)
   - TCP (NTCP2)는 오버헤드로 인해 일반적으로 더 높은 비용(10-11)
   - 낮은 비용 = 선호되는 전송 방식

2. **다중 주소:**
   - Routers는 여러 개의 RouterAddress 항목을 게시할 수 있습니다
   - 서로 다른 전송 방식(SSU2 및 NTCP2)
   - 서로 다른 IP 버전(IPv4 및 IPv6)
   - 클라이언트는 비용과 기능을 기준으로 선택합니다

3. **호스트명 vs IP:**
   - 성능을 위해 IP 주소가 선호됨
   - 호스트명도 지원하지만 DNS 조회 오버헤드가 추가됨
   - RouterInfos(라우터 정보 데이터 구조)를 게시할 때는 IP 사용을 고려

4. **Base64 인코딩(Base64: 바이너리 데이터를 텍스트로 인코딩하는 방식):**
   - 모든 키 및 바이너리 데이터는 Base64로 인코딩한다
   - 표준 Base64(RFC 4648)
   - 패딩이나 비표준 문자를 사용하지 않음

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (router 정보)

**설명:** 네트워크 데이터베이스에 저장되는 router에 관한 공개 정보 일체입니다. 식별 정보, 주소, 기능을 포함합니다.

**형식:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**데이터베이스 저장소:** - **데이터베이스 유형:** 0 - **키:** RouterIdentity(라우터 식별자)의 SHA-256 해시 - **값:** 완전한 RouterInfo(라우터 정보) 구조체

**게시 타임스탬프:** - 8바이트 날짜(유닉스 epoch 이후 밀리초) - RouterInfo(라우터 정보) 버전 관리에 사용 - Routers는 주기적으로 새로운 RouterInfo를 게시 - Floodfills는 게시된 타임스탬프를 기준으로 최신 버전을 유지

**주소 정렬:** - **과거:** 매우 오래된 routers에서는 데이터의 SHA-256 기준으로 주소 정렬이 필요했습니다 - **현재:** 정렬은 필요하지 않으며, 호환성을 위해 구현할 가치가 없습니다 - 주소는 어떤 순서로든 가능합니다

**피어 크기 필드(역사적):** - 현대의 I2P에서는 **항상 0** - 제한된 경로를 위한 용도로 의도되었으나(미구현) - 구현되었다면, 그 수만큼의 Router 해시가 뒤따랐을 것임 - 일부 오래된 구현에서는 정렬된 피어 목록을 요구했을 수도 있음

**옵션 매핑:**

옵션은 키 기준으로 반드시 정렬되어야 합니다. 표준 옵션에는 다음이 포함됩니다:

**기능 옵션:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**네트워크 옵션:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**통계 옵션:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
표준 옵션의 전체 목록은 [네트워크 데이터베이스 RouterInfo(라우터 정보) 문서](/docs/specs/common-structures/#routerInfo)를 참조하세요.

**서명 연산:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**일반적인 최신 RouterInfo(router 정보):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**구현 참고 사항:**

1. **여러 주소:**
   - Routers는 일반적으로 1~4개의 주소를 공개함
   - IPv4 및 IPv6 변형
   - SSU2 및/또는 NTCP2 전송 프로토콜
   - 각 주소는 서로 독립적임

2. **버전 관리:**
   - 더 최신 RouterInfo(라우터 정보 레코드)는 `published` 타임스탬프가 더 최근이다
   - router는 ~2시간마다 또는 주소가 변경될 때 재게시한다
   - floodfill 노드는 최신 버전만 저장하고 전파한다

3. **검증:**
   - RouterInfo를 수락하기 전에 서명을 검증하십시오
   - 각 RouterAddress에서 expiration 필드가 모두 0인지 확인하십시오
   - options 매핑이 키 기준으로 정렬되어 있는지 검증하십시오
   - 인증서와 키 유형이 알려져 있고 지원되는지 확인하십시오

4. **네트워크 데이터베이스:**
   - floodfill들(특수 netDb 유지 노드)은 Hash(RouterIdentity)로 인덱싱된 RouterInfo를 저장함
   - 마지막 발행 이후 약 2일 동안 저장됨
   - routers는 다른 routers를 발견하기 위해 floodfill들에 질의함

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## 구현 참고 사항

### 바이트 순서(Endianness)

**기본값: 빅 엔디언 (네트워크 바이트 순서)**

대부분의 I2P 구조체는 빅엔디언 바이트 순서를 사용합니다: - 모든 정수형 (1-8 바이트) - 날짜 타임스탬프 - TunnelId(터널 ID) - 문자열 길이 접두부 - 인증서 유형과 길이 - 키 유형 코드 - 매핑 크기 필드

**예외: 리틀 엔디언**

다음 키 유형은 **리틀 엔디언** 인코딩을 사용합니다: - **X25519** 암호화 키(유형 4) - **EdDSA_SHA512_Ed25519** 서명 키(유형 7) - **EdDSA_SHA512_Ed25519ph** 서명 키(유형 8) - **RedDSA_SHA512_Ed25519** 서명 키(유형 11)

**구현:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### 구조체 버전 관리

**절대 고정된 크기를 가정하지 마십시오:**

여러 구조체는 길이가 가변적입니다: - RouterIdentity: 387+ 바이트 (항상 387인 것은 아님) - Destination: 387+ 바이트 (항상 387인 것은 아님) - LeaseSet2: 상당히 달라집니다 - Certificate: 3+ 바이트

**항상 크기 필드를 읽으십시오:** - 인증서 길이는 바이트 1-2에 - 매핑 크기는 시작 부분에 - KeysAndCert(키와 인증서 구조)는 항상 384 + 3 + certificate_length로 계산됩니다

**초과 데이터 점검:** - 유효한 구조 뒤에 후행 잡데이터(trailing garbage) 금지 - 인증서 길이가 키 유형과 일치하는지 검증 - 고정 크기 타입에 대해 예상된 길이에 정확히 일치하도록 강제

### 현재 권장사항(2025년 10월)

**신규 Router Identities(라우터 식별자)용:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ko/proposals/161-ri-dest-padding/)
```
**새로운 Destination(목적지)용:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ko/proposals/161-ri-dest-padding/)
```
**새로운 LeaseSets의 경우:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**암호화된 서비스의 경우:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### 사용 중단된 기능 - 사용하지 마십시오

**지원 중단된 암호화:** - Router Identities용 ElGamal (type 0) (0.9.58에서 지원 중단됨) - ElGamal/AES+SessionTag 암호화 (ECIES-X25519 사용)

**사용 중단된 서명:** - Router 식별자용 DSA_SHA1 (type 0) (0.9.58에서 사용 중단) - 새로운 구현용 ECDSA 변형(유형 1-3) - SU3 파일을 제외한 RSA 변형(유형 4-6)

**사용 중단된 네트워크 형식:** - LeaseSet 유형 1 (LeaseSet2 사용) - Lease (44바이트, Lease2 사용) - 기존 Lease 만료 형식

**사용 중단된 전송 프로토콜:** - NTCP (0.9.50에서 제거됨) - SSU (2.4.0에서 제거됨)

**사용 중단된 인증서:** - HASHCASH (유형 1) - HIDDEN (유형 2) - SIGNED (유형 3) - MULTIPLE (유형 4)

### 보안 고려 사항

**키 생성:** - 항상 암호학적으로 안전한 난수 생성기를 사용하십시오 - 서로 다른 컨텍스트 간에 키를 재사용하지 마십시오 - 개인 키를 적절한 접근 제어로 보호하십시오 - 작업이 끝나면 메모리에서 키 자료를 안전하게 삭제하십시오

**서명 검증:** - 데이터를 신뢰하기 전에 항상 서명을 검증할 것 - 서명 길이가 키 유형과 일치하는지 확인할 것 - 서명된 데이터에 예상되는 필드를 포함하는지 검증할 것 - 정렬된 매핑의 경우, 서명/검증 전에 정렬 순서를 검증할 것

**타임스탬프 검증:** - 발행 시각이 타당한지 확인(너무 먼 미래가 아님) - 리스 만료 시각이 이미 지나지 않았는지 검증 - 시계 오차 허용치를 고려(일반적으로 ±30초)

**네트워크 데이터베이스(netDb):** - 저장하기 전에 모든 데이터 구조를 검증한다 - 서비스 거부(DoS)를 방지하기 위해 크기 제한을 강제한다 - 질의와 발행에 빈도 제한을 적용한다 - 데이터베이스 키가 데이터 구조의 해시와 일치하는지 확인한다

### 호환성 참고 사항

**하위 호환성:** - ElGamal 및 DSA_SHA1은 레거시 router에서도 여전히 지원됩니다 - 더 이상 권장되지 않는 키 유형은 기능적으로는 계속 동작하지만 사용은 권장되지 않습니다 - Compressible padding(압축 가능한 패딩) ([Proposal 161](/ko/proposals/161-ri-dest-padding/))은 0.6 버전까지 하위 호환됩니다

**전방 호환성:** - 알 수 없는 키 유형은 길이 필드를 사용하여 파싱할 수 있다 - 알 수 없는 인증서 유형은 길이를 이용해 건너뛸 수 있다 - 알 수 없는 서명 유형은 무리 없이 처리해야 한다 - 구현자는 알 수 없는 선택적 기능 때문에 실패해서는 안 된다

**마이그레이션 전략:** - 전환 중 기존과 새로운 키 유형을 모두 지원 - LeaseSet2는 여러 암호화 키를 나열할 수 있음 - 오프라인 서명은 안전한 키 로테이션(주기적 교체)을 가능하게 함 - MetaLeaseSet은 투명한 서비스 마이그레이션을 가능하게 함

### 테스트 및 검증

**구조체 검증:** - 모든 길이 필드가 예상 범위 내에 있는지 확인 - 가변 길이 구조체가 올바르게 파싱되는지 점검 - 서명 검증이 성공하는지 검증 - 최소 및 최대 크기의 구조체로 테스트

**경계 사례:** - 길이가 0인 문자열 - 빈 매핑 - 최소 및 최대 리스 수 - 페이로드 길이가 0인 인증서 - 매우 큰 구조체(최대 크기에 근접)

**상호운용성:** - 공식 Java I2P 구현을 기준으로 테스트 - i2pd와의 호환성 검증 - 다양한 netDb(네트워크 데이터베이스) 내용으로 테스트 - 정상으로 알려진 테스트 벡터에 대해 검증

---

## 참고 자료

### 명세

- [I2NP 프로토콜](/docs/specs/i2np/)
- [I2CP 프로토콜](/docs/specs/i2cp/)
- [SSU2 전송](/docs/specs/ssu2/)
- [NTCP2 전송](/docs/specs/ntcp2/)
- [Tunnel 프로토콜](/docs/specs/implementation/)
- [데이터그램 프로토콜](/docs/api/datagrams/)

### 암호학

- [암호학 개요](/docs/specs/cryptography/)
- [ElGamal/AES 암호화](/docs/legacy/elgamal-aes/)
- [ECIES-X25519 암호화](/docs/specs/ecies/)
- [router용 ECIES](/docs/specs/ecies/#routers)
- [ECIES 하이브리드(포스트-양자)](/docs/specs/ecies/#hybrid)
- [Red25519 서명](/docs/specs/red25519-signature-scheme/)
- [암호화된 LeaseSet](/docs/specs/encryptedleaseset/)

### 제안서

- [제안 123: 새로운 netDB 항목](/proposals/123-new-netdb-entries/)
- [제안 134: GOST(러시아 국가표준 암호) 서명 유형](/proposals/134-gost/)
- [제안 136: 실험적 서명 유형](/proposals/136-experimental-sigtypes/)
- [제안 145: ECIES(타원곡선 통합 암호화 방식)-P256](/proposals/145-ecies/)
- [제안 156: ECIES Routers](/proposals/156-ecies-routers/)
- [제안 161: 패딩 생성](/ko/proposals/161-ri-dest-padding/)
- [제안 167: 서비스 레코드](/proposals/167-service-records/)
- [제안 169: 포스트-양자 암호](/proposals/169-pq-crypto/)
- [모든 제안 색인](/proposals/)

### 네트워크 데이터베이스

- [네트워크 데이터베이스 개요](/docs/specs/common-structures/)
- [RouterInfo 표준 옵션](/docs/specs/common-structures/#routerInfo)

### JavaDoc API 참조

- [코어 데이터 패키지](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### 외부 표준

- **RFC 7748 (X25519):** 보안을 위한 타원곡선
- **RFC 7539 (ChaCha20):** IETF 프로토콜을 위한 ChaCha20 및 Poly1305
- **RFC 4648 (Base64):** Base16, Base32 및 Base64 데이터 인코딩
- **FIPS 180-4 (SHA-256):** 보안 해시 표준
- **FIPS 204 (ML-DSA):** 모듈-격자 기반 디지털 서명 표준
- [IANA 서비스 레지스트리](http://www.dns-sd.org/ServiceTypes.html)

### 커뮤니티 자료

- [I2P 웹사이트](/)
- [I2P 포럼](https://i2pforum.net)
- [I2P GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P GitHub 미러](https://github.com/i2p/i2p.i2p)
- [기술 문서 색인](/docs/)

### 릴리스 정보

- [I2P 2.10.0 릴리스](/ko/blog/2025/09/08/i2p-2.10.0-release/)
- [릴리스 이력](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [변경 로그](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## 부록: 빠른 참조 표

### 키 유형 빠른 참조

**현재 표준(모든 신규 구현에 권장):** - **암호화:** X25519 (타입 4, 32바이트, 리틀엔디언) - **서명:** EdDSA_SHA512_Ed25519 (타입 7, 32바이트, 리틀엔디언)

**레거시 (지원되지만 더 이상 권장되지 않음):** - **암호화:** ElGamal (유형 0, 256바이트, 빅엔디언) - **서명:** DSA_SHA1 (유형 0, 20바이트 개인키 / 128바이트 공개키, 빅엔디언)

**특수:** - **서명(암호화된 LeaseSet(I2P 목적지의 inbound tunnel 정보 묶음)):** RedDSA_SHA512_Ed25519 (유형 11, 32바이트, 리틀 엔디언)

**포스트-양자 (베타, 최종 확정되지 않음):** - **하이브리드 암호화:** MLKEM_X25519 변형(타입 5-7) - **순수 PQ 암호화:** MLKEM 변형(아직 타입 코드가 할당되지 않음)

### 구조체 크기 빠른 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### 데이터베이스 유형 빠른 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### 전송 프로토콜 빠른 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### 버전 마일스톤 빠른 참조

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/ko/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
