---
title: "스트리밍 프로토콜"
description: "대부분의 I2P 애플리케이션에서 사용되는 TCP와 유사한 신뢰성 있는 전송 방식"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## 개요

I2P Streaming Library(I2P에서 신뢰성·순서 보장·인증을 제공하는 스트림 전송 라이브러리)는 I2P의 비신뢰성 메시지 계층 위에서 신뢰성 있고 순서가 보장되며 인증된 데이터 전달을 제공합니다 — IP 위의 TCP와 유사합니다. 이는 웹 브라우징, IRC, 이메일, 파일 공유 등 거의 모든 대화형 I2P 애플리케이션에서 사용됩니다.

이는 I2P의 고지연 익명 tunnels 전체에 걸쳐 신뢰할 수 있는 전송, 혼잡 제어, 재전송 및 흐름 제어를 보장합니다. 각 스트림은 목적지 간에 종단 간으로 완전히 암호화됩니다.

---

## 핵심 설계 원칙

스트리밍 라이브러리는 **one-phase connection setup**(단일 단계 연결 설정)을 구현하며, SYN, ACK 및 FIN 플래그가 동일한 메시지에서 데이터 페이로드를 실을 수 있다. 이는 고지연 환경에서 왕복 횟수를 최소화한다 — 작은 HTTP 트랜잭션은 단 한 번의 왕복으로 완료될 수 있다.

혼잡 제어와 재전송은 TCP를 본떴지만 I2P의 환경에 맞게 조정되었습니다. 윈도 크기는 바이트 기반이 아니라 메시지 기반이며, tunnel 지연 시간과 오버헤드에 맞게 최적화되어 있습니다. 이 프로토콜은 TCP의 AIMD(가산적 증가/승법적 감소) 알고리즘과 유사하게 느린 시작, 혼잡 회피, 지수적 백오프를 지원합니다.

---

## 아키텍처

스트리밍 라이브러리는 애플리케이션과 I2CP 인터페이스 사이에서 동작합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
대부분의 사용자는 I2PSocketManager, I2PTunnel 또는 SAMv3를 통해 이에 접근합니다. 라이브러리는 destination(목적지) 관리, tunnel 사용 및 재전송을 투명하게 처리합니다.

---

## 패킷 형식

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### 헤더 세부 정보

- **Stream IDs**: 로컬 및 원격 스트림을 고유하게 식별하는 32비트 값.
- **Sequence Number**: SYN에서는 0에서 시작하며, 메시지마다 증가합니다.
- **Ack Through**: N까지의 모든 메시지를 확인(ACK)하며, 부정 확인(NACK) 목록에 있는 것들은 제외합니다.
- **Flags**: 상태와 동작을 제어하는 비트마스크.
- **Options**: RTT, MTU 및 프로토콜 협상을 위한 가변 길이 목록.

### 주요 플래그

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## 흐름 제어와 신뢰성

Streaming은 TCP의 바이트 기반 방식과 달리 **message-based windowing**(메시지 기반 윈도우 제어)을 사용합니다. 전송 중으로 허용되는 ACK 미수신 패킷 수는 현재 윈도우 크기와 같습니다(기본값 128).

### 메커니즘

- **혼잡 제어:** 슬로 스타트와 AIMD(가산적 증가·곱셈적 감소) 기반 혼잡 회피.  
- **Choke/Unchoke(초크/언초크):** 버퍼 점유율 기반의 흐름 제어 신호.  
- **재전송:** RFC 6298 기반의 RTO 계산과 지수 백오프.  
- **중복 필터링:** 메시지 순서가 재정렬될 수 있는 환경에서도 신뢰성을 보장.

일반적인 설정 값:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## 연결 설정

1. **개시자**는 SYN을 보낸다(선택적으로 페이로드와 FROM_INCLUDED 포함).  
2. **응답자**는 SYN+ACK로 응답한다(페이로드가 포함될 수 있음).  
3. **개시자**는 연결 성립을 확인하는 최종 ACK를 보낸다.

선택적 초기 payload(페이로드)는 핸드셰이크가 완전히 완료되기 전에 데이터 전송을 가능하게 합니다.

---

## 구현 세부사항

### 재전송과 타임아웃

재전송 알고리즘은 **RFC 6298**을 준수합니다.   - **초기 RTO:** 9s   - **최소 RTO:** 100ms   - **최대 RTO:** 45s   - **Alpha(알파):** 0.125   - **Beta(베타):** 0.25

### 제어 블록 공유

동일한 피어에 대한 최근 연결은 이전 RTT(왕복 시간)와 윈도우 데이터를 재사용하여 초기 램프업을 더 빠르게 하고, “콜드 스타트” 지연을 피합니다. 제어 블록은 몇 분 후 만료됩니다.

### MTU 및 단편화

- 기본 MTU: **1730 바이트** (I2NP 메시지 두 개를 담을 수 있음).  
- ECIES(타원곡선 통합 암호 방식) 대상: **1812 바이트** (오버헤드 감소).  
- 지원되는 최소 MTU: 512 바이트.

페이로드 크기에는 22바이트 최소 스트리밍 헤더가 포함되지 않습니다.

---

## 버전 이력

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## 애플리케이션 수준 사용

### Java 예제

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### SAMv3 및 i2pd 지원

- **SAMv3**: Java가 아닌 클라이언트를 위한 STREAM 및 DATAGRAM 모드를 제공합니다.  
- **i2pd**: 구성 파일 옵션(예: `i2p.streaming.maxWindowSize`, `profile` 등)을 통해 동일한 스트리밍 매개변수를 노출합니다.

---

## 스트리밍과 데이터그램 중에서 선택하기

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## 보안과 포스트-양자 미래

스트리밍 세션은 I2CP 계층에서 종단 간으로 암호화됩니다.   포스트-양자 하이브리드 암호화(ML-KEM + X25519)는 2.10.0에서 실험적으로 지원되지만 기본적으로 비활성화되어 있습니다.

---

## 참고 자료

- [스트리밍 API 개요](/docs/specs/streaming/)  
- [스트리밍 프로토콜 명세](/docs/specs/streaming/)  
- [I2CP 명세](/docs/specs/i2cp/)  
- [제안 144: 스트리밍 MTU 계산](/proposals/144-ecies-x25519-aead-ratchet/)  
- [I2P 2.10.0 릴리스 노트](/ko/blog/2025/09/08/i2p-2.10.0-release/)
