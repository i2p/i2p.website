---
title: "SSU2 명세서"
description: "보안 준신뢰형 UDP 전송 프로토콜 버전 2"
slug: "ssu2"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. 개요

SSU2는 I2P에서 보안적이고 준신뢰성을 갖춘 router 간 통신에 사용되는 UDP 기반 전송 계층 프로토콜이다. 이는 범용 전송 프로토콜이 아니라 **I2NP 메시지 교환**에 특화되어 있다.

### 핵심 기능

- Noise XK pattern(Noise 프로토콜의 XK 패턴)을 통한 인증된 키 교환
- DPI(패킷 심층 검사) 저항성을 위한 암호화된 헤더
- 중계와 hole-punching(홀 펀칭)을 사용하는 NAT(네트워크 주소 변환) 트래버설
- 연결 마이그레이션 및 주소 검증
- 선택적 경로 검증
- 순방향 기밀성 및 재생 공격 방지

### 레거시 및 호환성

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2 Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU1 Removed</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2.44.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56</td><td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.61</td></tr>
  </tbody>
</table>
SSU1은 공개 I2P 네트워크에서는 더 이상 사용되지 않습니다.

---

## 2. 암호학

SSU2(I2P 전송 프로토콜)는 I2P 특화 확장과 함께 **Noise_XK_25519_ChaChaPoly_SHA256**을 사용한다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Function</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie-Hellman</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (RFC 7748)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32-byte keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Cipher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (RFC 7539)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD encryption</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Used for key derivation and message integrity</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KDF</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HKDF-SHA256 (RFC 5869)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">For session and header keys</td></tr>
  </tbody>
</table>
헤더와 페이로드는 `mixHash()`를 통해 암호학적으로 결합된다. 구현 효율을 위해 모든 암호학적 프리미티브는 NTCP2와 ECIES(타원곡선 통합 암호화 체계)에서 공통으로 사용된다.

---

## 3. 메시지 개요

### 3.1 UDP 데이터그램 규칙

- 각 UDP 데이터그램에는 **정확히 하나의 SSU2 message**만 포함된다.  
- Session Confirmed 메시지(세션 확인 메시지)는 여러 데이터그램에 걸쳐 단편화될 수 있다.

**최소 크기:** 40 바이트   **최대 크기:** 1472 바이트 (IPv4) / 1452 바이트 (IPv6)

### 3.2 메시지 유형

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Header</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake initiation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Created</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake response</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">2</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Session Confirmed</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Final handshake, may be fragmented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.6rem;">16B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted I2NP message blocks</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT reachability testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token or rejection notice</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Request for validation token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">32B</td><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal signaling</td></tr>
  </tbody>
</table>
---

## 4. 세션 수립

### 4.1 표준 흐름 (유효 토큰)

```
Alice                        Bob
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.2 토큰 획득

```
Alice                        Bob
TokenRequest  ───────────────>
<──────────────  Retry (Token)
SessionRequest  ─────────────>
<──────────────  SessionCreated
SessionConfirmed ────────────>
```
### 4.3 잘못된 토큰

```
Alice                        Bob
SessionRequest ─────────────>
<──────────────  Retry (Termination)
```
---

## 5. 헤더 구조

### 5.1 긴 헤더 (32바이트)

세션 수립 전에 사용됨 (SessionRequest, Created, Retry, PeerTest, TokenRequest, HolePunch).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random unique ID</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random (ignored during handshake)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Version</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Always 2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NetID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">2 = main I2P network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved (0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Source Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random ID distinct from destination</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Token for address validation</td></tr>
  </tbody>
</table>
### 5.2 짧은 헤더 (16바이트)

수립된 세션에서 사용됩니다(SessionConfirmed, Data).

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Destination Connection ID</td><td style="border:1px solid var(--color-border); padding:0.6rem;">8</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Stable throughout session</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Packet Number</td><td style="border:1px solid var(--color-border); padding:0.6rem;">4</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Incrementing per message</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.6rem;">1</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Message type (2 or 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.6rem;">3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ACK/fragment flags</td></tr>
  </tbody>
</table>
---

## 6. 암호화

### 6.1 AEAD(연관 데이터가 있는 인증 암호화)

모든 페이로드는 **ChaCha20/Poly1305 AEAD**로 암호화됩니다:

```
ciphertext = ChaCha20_Poly1305_Encrypt(key, nonce, plaintext, associated_data)
```
- 논스: 12바이트 (0 4바이트 + 카운터 8바이트)
- 태그: 16바이트
- 연관 데이터: 무결성 바인딩을 위한 헤더를 포함

### 6.2 헤더 보호

헤더는 세션 헤더 키에서 유도된 ChaCha20 키스트림을 사용해 마스킹된다. 이는 모든 연결 ID와 패킷 필드가 무작위처럼 보이도록 해 DPI(Deep Packet Inspection, 심층 패킷 검사)에 대한 저항성을 제공한다.

### 6.3 키 유도

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Phase</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Initial</td><td style="border:1px solid var(--color-border); padding:0.6rem;">introKey + salt</td><td style="border:1px solid var(--color-border); padding:0.6rem;">handshake header key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Handshake</td><td style="border:1px solid var(--color-border); padding:0.6rem;">DH(X25519)</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey + AEAD key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Data phase</td><td style="border:1px solid var(--color-border); padding:0.6rem;">chainKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">TX/RX keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Key rotation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">oldKey</td><td style="border:1px solid var(--color-border); padding:0.6rem;">newKey</td></tr>
  </tbody>
</table>
---

## 7. 보안 및 리플레이 공격 방지

- 토큰은 IP별로 발급되며, 약 60초 후 만료됩니다.  
- 세션별 블룸 필터를 통해 재전송(Replay) 공격을 방지합니다.  
- 중복된 임시 키는 거부됩니다.  
- 헤더와 페이로드는 암호학적으로 결합되어 있습니다.

모든 router는 AEAD 인증에 실패했거나 버전 또는 NetID가 유효하지 않은 패킷을 폐기해야 한다.

---

## 8. 패킷 번호 매기기 및 세션 수명

각 방향은 자체 32비트 카운터를 유지합니다.   - 0에서 시작하며, 패킷마다 증가합니다.   - wrap(카운터가 최댓값을 넘겨 0으로 되돌아가는 현상)이 발생하면 안 됩니다; 2³²에 도달하기 전에 세션 rekey(세션 키 재설정) 또는 종료를 해야 합니다.

연결 ID는 마이그레이션 중을 포함하여 세션 전체 동안 변하지 않습니다.

---

## 9. 데이터 단계

- 유형 = 6 (데이터)
- 짧은 헤더 (16바이트)
- 페이로드에는 하나 이상의 암호화된 블록이 포함합니다:
  - ACK/NACK 목록
  - I2NP 메시지 조각
  - 패딩 (0–31바이트 임의값)
  - 종료 블록 (선택 사항)

선택적 재전송과 순서가 뒤바뀐 전달을 지원합니다. 신뢰성은 'semi-reliable'(준신뢰적) 수준으로 유지되며, 재시도 한도를 초과하면 누락된 패킷은 별도 알림 없이 폐기될 수 있습니다.

---

## 10. 릴레이 및 NAT 트래버설

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Peer Test</td><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Determines inbound reachability</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Retry</td><td style="border:1px solid var(--color-border); padding:0.6rem;">9</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Issues new token or rejection</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Token Request</td><td style="border:1px solid var(--color-border); padding:0.6rem;">10</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Requests new address token</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Hole Punch</td><td style="border:1px solid var(--color-border); padding:0.6rem;">11</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Coordinates NAT hole punching</td></tr>
  </tbody>
</table>
릴레이 router는 이러한 제어 메시지를 사용하여 제한적인 NAT(네트워크 주소 변환) 뒤에 있는 피어를 지원합니다.

---

## 11. 세션 종료

어느 쪽 피어든 Data message 내의 **Termination block**(종료 블록)을 사용하여 세션을 종료할 수 있다.   수신 즉시 리소스를 해제해야 한다.   재전송된 종료 패킷은 승인을 받은 후에는 무시해도 된다.

---

## 12. 구현 지침

Routers **MUST**: - version = 2 및 NetID = 2임을 검증한다.   - 40바이트 미만의 패킷이거나 AEAD(연관 데이터가 있는 인증된 암호화)가 유효하지 않은 경우 폐기한다.   - 120초 리플레이 캐시를 강제한다.   - 재사용된 토큰 또는 에페메랄 키를 거부한다.

Routers는 **권장합니다**: - 패딩 길이를 0–31바이트 범위에서 무작위로 설정합니다.   - 적응형 재전송을 사용합니다(RFC 6298).   - 마이그레이션 전에 피어별 경로 검증을 구현합니다.

---

## 13. 보안 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Achieved By</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Forward secrecy</td><td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 ephemeral keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Replay protection</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tokens + Bloom filter</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated encryption</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">KCI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Noise XK pattern</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">DPI resistance</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted headers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Relay + Hole Punch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;">Migration</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Static connection IDs</td></tr>
  </tbody>
</table>
---

## 14. 참고 문헌

- [제안 159 – SSU2](/proposals/159-ssu2/)
- [Noise 프로토콜 프레임워크](https://noiseprotocol.org/noise.html)
- [RFC 9000 – QUIC 전송](https://datatracker.ietf.org/doc/html/rfc9000)
- [RFC 9001 – QUIC용 TLS](https://datatracker.ietf.org/doc/html/rfc9001)
- [RFC 7539 – ChaCha20/Poly1305 AEAD(연관 데이터 인증 암호화)](https://datatracker.ietf.org/doc/html/rfc7539)
- [RFC 7748 – X25519 ECDH](https://datatracker.ietf.org/doc/html/rfc7748)
- [RFC 5869 – HKDF-SHA256](https://datatracker.ietf.org/doc/html/rfc5869)
