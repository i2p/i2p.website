---
title: "데이터그램"
description: "I2CP 위에서의 인증된, 응답 가능한, 그리고 원시 메시지 형식"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## 개요

데이터그램은 [I2CP](/docs/specs/i2cp/) 위에서 그리고 스트리밍 라이브러리와 병렬로 메시지 지향 통신을 제공합니다. 이를 통해 연결 지향 스트림 없이도 **응답 가능**, **인증됨**, 또는 **원시** 패킷을 사용할 수 있습니다. Router는 NTCP2 또는 SSU2가 트래픽을 전송하는지 여부와 관계없이 데이터그램을 I2NP 메시지와 tunnel 메시지로 캡슐화합니다.

핵심 동기는 애플리케이션(트래커, DNS 리졸버 또는 게임 등)이 발신자를 식별하는 자체 포함 패킷을 전송할 수 있도록 하는 것입니다.

> **2025년 신규 사항:** I2P 프로젝트는 **Datagram2 (프로토콜 19)** 및 **Datagram3 (프로토콜 20)**을 승인하여, 10년 만에 처음으로 재생 공격 방지 및 낮은 오버헤드의 응답 가능한 메시징을 추가했습니다.

---

## 1. 프로토콜 상수

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
프로토콜 19와 20은 **제안서 163 (2025년 4월)**에서 공식화되었습니다. 이들은 하위 호환성을 위해 Datagram1 / RAW와 공존합니다.

---

## 2. 데이터그램 유형

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### 일반적인 디자인 패턴

- **요청 → 응답:** 서명된 Datagram2(요청 + nonce)를 전송하고, 원시 또는 Datagram3 응답(nonce 에코)을 수신합니다.
- **고빈도/저오버헤드:** Datagram3 또는 RAW를 선호합니다.
- **인증된 제어 메시지:** Datagram2.
- **레거시 호환성:** Datagram1은 여전히 완전히 지원됩니다.

---

## 3. Datagram2 및 Datagram3 세부사항 (2025)

### Datagram2 (프로토콜 19)

Datagram1의 향상된 대체 버전. 특징: - **재생 공격 방지:** 4바이트 재생 방지 토큰. - **오프라인 서명 지원:** 오프라인 서명된 Destination에서 사용 가능. - **확장된 서명 범위:** destination 해시, 플래그, 옵션, 오프라인 서명 블록, 페이로드 포함. - **포스트 양자 대응:** 향후 ML-KEM 하이브리드와 호환. - **오버헤드:** 약 457바이트 (X25519 키 기준).

### Datagram3 (프로토콜 20)

원시 타입과 서명된 타입 간의 격차를 메웁니다. 기능: - **서명 없이 응답 가능:** 발신자의 32바이트 해시 + 2바이트 플래그 포함. - **최소한의 오버헤드:** 약 34바이트. - **재생 공격 방어 없음** — 애플리케이션에서 구현해야 합니다.

두 프로토콜 모두 API 0.9.66 기능이며 릴리스 2.9.0부터 Java router에 구현되었습니다. i2pd 또는 Go 구현은 아직 없습니다 (2025년 10월 기준).

---

## 4. 크기 및 단편화 제한

- **Tunnel 메시지 크기:** 1 028 바이트 (4 B Tunnel ID + 16 B IV + 1 008 B 페이로드).  
- **초기 프래그먼트:** 956 B (일반적인 TUNNEL 전달).  
- **후속 프래그먼트:** 996 B.  
- **최대 프래그먼트:** 63–64.  
- **실용적 한계:** ≈ 62 708 B (~61 KB).  
- **권장 한계:** 안정적인 전달을 위해 ≤ 10 KB (이를 초과하면 드롭이 기하급수적으로 증가함).

**오버헤드 요약:** - Datagram1 ≈ 427 B (최소).   - Datagram2 ≈ 457 B.   - Datagram3 ≈ 34 B.   - 추가 계층 (I2CP gzip 헤더, I2NP, Garlic, Tunnel): + 최악의 경우 ~5.5 KB.

---

## 5. I2CP / I2NP 통합

메시지 경로: 1. 애플리케이션이 데이터그램 생성 (I2P API 또는 SAM을 통해).   2. I2CP가 gzip 헤더(`0x1F 0x8B 0x08`, RFC 1952) 및 CRC-32 체크섬으로 래핑.   3. 프로토콜 + 포트 번호가 gzip 헤더 필드에 저장됨.   4. Router가 I2NP 메시지로 캡슐화 → Garlic clove → 1 KB tunnel 단편화.   5. 단편들이 outbound → 네트워크 → inbound tunnel을 통과.   6. 재조립된 데이터그램이 프로토콜 번호에 기반하여 애플리케이션 핸들러로 전달됨.

**무결성:** CRC-32 (I2CP에서) + 선택적 암호화 서명 (Datagram1/2). 데이터그램 자체 내에는 별도의 체크섬 필드가 없습니다.

---

## 6. 프로그래밍 인터페이스

### Java API

패키지 `net.i2p.client.datagram`에는 다음이 포함됩니다: - `I2PDatagramMaker` – 서명된 데이터그램을 생성합니다.   - `I2PDatagramDissector` – 발신자 정보를 검증하고 추출합니다.   - `I2PInvalidDatagramException` – 검증 실패 시 발생합니다.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`)은 Destination을 공유하는 앱들의 프로토콜 및 포트 멀티플렉싱을 관리합니다.

**Javadoc 접근:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (I2P 네트워크 전용) - [Javadoc 미러](https://eyedeekay.github.io/javadoc-i2p/) (일반 인터넷 미러) - [공식 Javadocs](http://docs.i2p-projekt.de/javadoc/) (공식 문서)

### SAM v3 지원

- SAM 3.2 (2016): PORT 및 PROTOCOL 매개변수 추가.  
- SAM 3.3 (2016): PRIMARY/하위세션 모델 도입; 하나의 Destination에서 스트림 + 데이터그램 허용.  
- Datagram2 / 3 세션 스타일 지원이 2025년 사양에 추가됨 (구현 대기 중).  
- 공식 사양: [SAM v3 Specification](/docs/api/samv3/)

### i2ptunnel 모듈

- **udpTunnel:** I2P UDP 앱을 위한 완전히 기능하는 기반 (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** A/V 스트리밍을 위해 작동 가능 (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** 2.10.0 기준 **기능하지 않음** (UDP stub만 존재).

> 범용 UDP의 경우 Datagram API 또는 udpTunnel을 직접 사용하세요—SOCKS UDP에 의존하지 마세요.

---

## 7. 생태계 및 언어 지원 (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P는 현재 전체 SAM 3.3 subsession과 Datagram2 API를 지원하는 유일한 router입니다.

---

## 8. 사용 예시 – UDP Tracker (I2PSnark 2.10.0)

Datagram2/3의 첫 실제 적용 사례:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
패턴은 보안과 성능의 균형을 맞추기 위해 인증된 데이터그램과 경량 데이터그램을 혼합하여 사용하는 것을 보여줍니다.

---

## 9. 보안 및 모범 사례

- 인증된 교환이나 재생 공격이 중요한 경우 Datagram2를 사용하세요.
- 적당한 신뢰 수준에서 빠른 응답 가능한 메시지에는 Datagram3를 선호하세요.
- 공개 브로드캐스트나 익명 데이터에는 RAW를 사용하세요.
- 안정적인 전송을 위해 페이로드를 ≤ 10 KB로 유지하세요.
- SOCKS UDP는 여전히 작동하지 않는다는 점을 유의하세요.
- 수신 시 항상 gzip CRC와 디지털 서명을 검증하세요.

---

## 10. 기술 사양

이 섹션에서는 저수준 데이터그램 형식, 캡슐화 및 프로토콜 세부 사항을 다룹니다.

### 10.1 프로토콜 식별

데이터그램 형식은 공통 헤더를 **공유하지 않습니다**. 라우터는 페이로드 바이트만으로는 타입을 추론할 수 없습니다.

여러 데이터그램 유형을 혼합하거나 데이터그램과 스트리밍을 결합할 때 다음을 명시적으로 설정하세요: - **프로토콜 번호** (I2CP 또는 SAM을 통해) - 선택적으로 **포트 번호** (애플리케이션이 서비스를 다중화하는 경우)

프로토콜을 설정하지 않은 상태(`0` 또는 `PROTO_ANY`)로 두는 것은 권장되지 않으며 라우팅 또는 전송 오류를 초래할 수 있습니다.

### 10.2 원시 데이터그램

응답 불가능한 데이터그램은 발신자나 인증 데이터를 포함하지 않습니다. 이들은 불투명한 페이로드로, 상위 레벨 데이터그램 API 외부에서 처리되지만 SAM과 I2PTunnel을 통해 지원됩니다.

**프로토콜:** `18` (`PROTO_DATAGRAM_RAW`)

**형식:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
페이로드 길이는 전송 제한에 의해 제약됩니다 (실질적 최대값 ≈32 KB, 종종 훨씬 적음).

### 10.3 Datagram1 (응답 가능한 데이터그램)

발신자의 **Destination**과 인증 및 응답 주소 지정을 위한 **Signature**를 포함합니다.

**프로토콜:** `17` (`PROTO_DATAGRAM`)

**오버헤드:** ≥427바이트 **페이로드:** 최대 ~31.5KB (전송 계층에 의해 제한됨)

**형식:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: Destination (387+ 바이트)
- `signature`: 키 타입과 일치하는 서명
  - DSA_SHA1의 경우: 페이로드의 SHA-256 해시에 대한 서명
  - 다른 키 타입의 경우: 페이로드에 대한 직접 서명

**참고:** - DSA가 아닌 타입의 서명은 I2P 0.9.14에서 표준화되었습니다. - LS2 (제안 123) 오프라인 서명은 현재 Datagram1에서 지원되지 않습니다.

### 10.4 Datagram2 형식

[Proposal 163](/proposals/163-datagram2/)에 정의된 대로 **재생 공격 방어**(replay resistance)를 추가한 개선된 응답 가능 데이터그램입니다.

**프로토콜:** `19` (`PROTO_DATAGRAM2`)

구현이 진행 중입니다. 애플리케이션은 중복 방지를 위해 nonce 또는 타임스탬프 검사를 포함해야 합니다.

### 10.5 Datagram3 형식

**응답 가능하지만 인증되지 않은** 데이터그램을 제공합니다. 내장된 destination과 서명 대신 라우터가 유지하는 세션 인증에 의존합니다.

**프로토콜:** `20` (`PROTO_DATAGRAM3`) **상태:** 0.9.66 버전부터 개발 중

다음과 같은 경우에 유용합니다: - destination이 큰 경우 (예: 양자 내성 키) - 다른 계층에서 인증이 발생하는 경우 - 대역폭 효율성이 중요한 경우

### 10.6 데이터 무결성

데이터그램 무결성은 I2CP 계층의 **gzip CRC-32 체크섬**으로 보호됩니다. 데이터그램 페이로드 형식 자체에는 명시적인 체크섬 필드가 존재하지 않습니다.

### 10.7 패킷 캡슐화

각 데이터그램은 단일 I2NP 메시지로 캡슐화되거나 **Garlic Message**의 개별 clove로 캡슐화됩니다. I2CP, I2NP, 그리고 tunnel 계층이 길이와 프레이밍을 처리하므로, 데이터그램 프로토콜 내부에는 구분자나 길이 필드가 없습니다.

### 10.8 포스트 양자(PQ) 고려사항

**Proposal 169** (ML-DSA 서명)가 구현되면, 서명 및 destination 크기가 극적으로 증가하여 약 455바이트에서 **≥3739바이트**로 늘어납니다. 이 변경사항은 데이터그램 오버헤드를 상당히 증가시키고 유효 페이로드 용량을 감소시킬 것입니다.

**Datagram3**은 세션 수준 인증(내장된 서명이 아닌)에 의존하므로, 양자 이후 I2P 환경에서 선호되는 설계가 될 가능성이 높습니다.

---

## 11. 참고 문헌

- [제안 163 – Datagram2 및 Datagram3](/proposals/163-datagram2/)
- [제안 160 – UDP Tracker 통합](/proposals/160-udp-trackers/)
- [제안 144 – Streaming MTU 계산](/proposals/144-ecies-x25519-aead-ratchet/)
- [제안 169 – 양자 내성 서명](/proposals/169-pq-crypto/)
- [I2CP 사양](/docs/specs/i2cp/)
- [I2NP 사양](/docs/specs/i2np/)
- [Tunnel 메시지 사양](/docs/specs/implementation/)
- [SAM v3 사양](/docs/api/samv3/)
- [i2ptunnel 문서](/docs/api/i2ptunnel/)

## 12. 변경 로그 주요 사항 (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. 요약

데이터그램 하위 시스템은 이제 완전히 인증된 방식부터 경량 원시 전송까지 다양한 스펙트럼을 제공하는 네 가지 프로토콜 변형을 지원합니다. 개발자는 보안이 중요한 사용 사례에는 **Datagram2**로, 효율적인 응답 가능 트래픽에는 **Datagram3**로 마이그레이션해야 합니다. 모든 이전 유형은 장기적인 상호 운용성을 보장하기 위해 여전히 호환됩니다.
