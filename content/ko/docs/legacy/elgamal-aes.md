---
title: "ElGamal/AES + SessionTag(세션 태그) 암호화"
description: "ElGamal, AES, SHA-256, 일회용 세션 태그를 결합한 레거시 종단 간 암호화"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **상태:** 이 문서는 레거시 ElGamal/AES+SessionTag 암호화 프로토콜을 설명합니다. 최신 I2P 버전(2.10.0+)이 [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) (라쳇 기반 암호화 방식)을 사용하므로, 하위 호환성 유지를 위해서만 계속 지원됩니다. ElGamal 프로토콜은 사용 중단(deprecated)되었으며, 역사적 및 상호운용성 목적을 위해서만 보존됩니다.

## 개요

ElGamal/AES+SessionTag는 garlic messages(I2P에서 여러 하위 메시지를 하나의 캡슐로 묶어 전송하는 메시지 형식)에 대한 I2P의 원래 종단 간 암호화 메커니즘을 제공했다. 이는 다음을 결합했다:

- **ElGamal (2048비트)** — 키 교환용
- **AES-256/CBC** — 페이로드 암호화용
- **SHA-256** — 해싱 및 IV(초기화 벡터) 도출용
- **Session Tags (세션 태그, 32 bytes)** — 일회용 메시지 식별자용

이 프로토콜은 지속적인 연결을 유지하지 않고도 router와 Destination(목적지)이 안전하게 통신할 수 있도록 했다. 각 세션은 대칭 AES 키를 설정하기 위해 비대칭 ElGamal 키 교환을 사용했고, 이어서 해당 세션을 참조하는 경량의 "tagged" 메시지를 주고받았다.

## 프로토콜 동작

### 세션 수립(새 세션)

새로운 세션은 두 개의 섹션이 포함된 메시지로 시작되었습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
ElGamal(엘가말) 블록 내부의 평문은 다음과 같이 구성되어 있었다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### 기존 세션 메시지

세션이 수립되면, 발신자는 캐시된 세션 태그를 사용하여 **existing-session** 메시지를 보낼 수 있었다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Routers는 전달된 태그를 약 **15분** 동안 캐시했으며, 그 시간이 지나면 사용되지 않은 태그는 만료되었다. 상관관계 공격을 방지하기 위해 각 태그는 정확히 **한 메시지**에만 유효했다.

### AES로 암호화된 블록 형식

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Routers는 새 세션의 경우 Pre-IV(사전 초기화 벡터), 기존 세션의 경우 세션 태그로부터 유도된 세션 키와 IV(초기화 벡터)를 사용하여 복호화한다. 복호화 후에는 평문 페이로드의 SHA-256 해시를 다시 계산하여 무결성을 검증한다.

## 세션 태그 관리

- 태그는 **단방향**입니다: Alice → Bob 태그는 Bob → Alice에서 재사용할 수 없습니다.
- 태그는 약 **15분** 후 만료됩니다.
- Routers는 대상별 **세션 키 관리자**를 유지하여 태그, 키, 만료 시간을 추적합니다.
- 애플리케이션은 [I2CP 옵션](/docs/specs/i2cp/)을 통해 태그 동작을 제어할 수 있습니다:
  - **`i2cp.tagThreshold`** — 보충하기 전에 캐시된 태그의 최소 개수
  - **`i2cp.tagCount`** — 메시지당 새 태그 수

이 메커니즘은 메시지 간 비연결성을 유지하면서 고비용의 ElGamal 핸드셰이크를 최소화했다.

## 구성 및 효율성

Session tags(암호화 세션을 식별하기 위한 일시적 태그)은 I2P의 지연이 크고 순서가 보장되지 않는 전송 전반에서 효율성을 개선하기 위해 도입되었습니다. 일반적인 구성에서는 **메시지당 태그 40개**를 전달하여 약 1.2 KB의 오버헤드가 추가되었습니다. 애플리케이션은 예상되는 트래픽에 따라 전달 동작을 조정할 수 있었습니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
router는 주기적으로 만료된 태그를 제거하고 사용되지 않는 세션 상태를 정리하여 메모리 사용량을 줄이고 태그 플러딩 공격을 완화합니다.

## 제한 사항

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
이러한 단점들은 [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) 프로토콜 설계의 직접적인 동기가 되었으며, 이 프로토콜은 완전 순방향 기밀성, 인증된 암호화, 그리고 효율적인 키 교환을 제공합니다.

## 사용 중단 및 마이그레이션 상태

- **도입:** 초기 I2P 릴리스 (0.6 이전)
- **사용 중단:** ECIES-X25519(타원곡선 기반 암호화 방식) 도입과 함께 (0.9.46 → 0.9.48)
- **제거:** 2.4.0부터 더 이상 기본값이 아님 (2023년 12월)
- **지원:** 레거시 호환성 전용

최신 router와 destination(목적지)는 이제 **암호 타입 4 (ECIES-X25519)**를 **타입 0 (ElGamal/AES)** 대신 광고한다. 레거시 프로토콜은 구버전 피어와의 상호 운용성을 위해 여전히 지원되지만, 새로운 배포에는 사용해서는 안 된다.

## 역사적 맥락

ElGamal/AES+SessionTag는 I2P 초기 암호 아키텍처의 토대였다. 그 하이브리드 설계는 일회용 session tag(세션 태그)와 단방향 세션 같은 혁신을 도입했고, 이는 이후 프로토콜에 영향을 미쳤다. 이러한 아이디어의 상당수는 결정적 래칫과 하이브리드 포스트-양자 키 교환 같은 현대적 구성으로 발전했다.
