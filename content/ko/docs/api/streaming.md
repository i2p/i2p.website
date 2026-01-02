---
title: "스트리밍 프로토콜"
description: "대부분의 I2P 애플리케이션에서 사용하는 TCP 유사 전송 방식"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

**I2P Streaming Library**는 I2P의 메시지 계층 위에서 신뢰할 수 있고 순서가 보장되며 인증된 전송을 제공하며, 이는 **IP 위의 TCP**와 유사합니다. 이는 [I2CP protocol](/docs/specs/i2cp/) 위에 위치하며 HTTP 프록시, IRC, BitTorrent, 이메일을 포함한 거의 모든 대화형 I2P 애플리케이션에서 사용됩니다.

### 핵심 특성

- **SYN**, **ACK**, **FIN** 플래그를 사용한 단일 단계 연결 설정으로, 페이로드 데이터와 함께 번들링하여 왕복 횟수를 줄입니다.
- I2P의 높은 지연 환경에 맞게 조정된 슬로우 스타트 및 혼잡 회피 기능을 갖춘 **슬라이딩 윈도우 혼잡 제어**.
- 재전송 비용과 단편화 지연 간의 균형을 맞추는 패킷 압축(기본 4KB 압축 세그먼트).
- I2P destination 간 완전히 **인증되고 암호화된** **신뢰할 수 있는** 채널 추상화.

이 설계는 작은 HTTP 요청과 응답이 단일 왕복(round-trip)으로 완료될 수 있도록 합니다. SYN 패킷은 요청 페이로드를 전달할 수 있으며, 응답자의 SYN/ACK/FIN은 전체 응답 본문을 포함할 수 있습니다.

---

## API 기본 사항

Java 스트리밍 API는 표준 Java 소켓 프로그래밍을 그대로 반영합니다:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory`는 I2CP를 통해 router 세션을 협상하거나 재사용합니다.
- 키가 제공되지 않으면 새로운 destination이 자동으로 생성됩니다.
- 개발자는 `options` 맵을 통해 I2CP 옵션(예: tunnel 길이, 암호화 유형 또는 연결 설정)을 전달할 수 있습니다.
- `I2PSocket`과 `I2PServerSocket`은 표준 Java `Socket` 인터페이스를 그대로 따르므로 마이그레이션이 간단합니다.

전체 Javadocs는 I2P router console 또는 [여기](/docs/specs/streaming/)에서 확인할 수 있습니다.

---

## 설정 및 튜닝

socket manager를 생성할 때 다음과 같이 설정 속성을 전달할 수 있습니다:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### 주요 옵션

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### 워크로드별 동작

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
버전 0.9.4 이후의 새로운 기능으로는 거부 로그 억제, DSA 목록 지원(0.9.21), 필수 프로토콜 적용(0.9.36)이 있습니다. 2.10.0 이후 router에는 전송 계층에서 포스트 양자 하이브리드 암호화(ML-KEM + X25519)가 포함되어 있습니다.

---

## 프로토콜 세부사항

각 스트림은 **Stream ID**로 식별됩니다. 패킷은 TCP와 유사한 제어 플래그를 전달합니다: `SYNCHRONIZE`, `ACK`, `FIN`, `RESET`. 패킷은 데이터와 제어 플래그를 동시에 포함할 수 있어, 단기 연결의 효율성을 향상시킵니다.

### 연결 수명 주기

1. **SYN 전송** — 개시자가 선택적 데이터를 포함합니다.
2. **SYN/ACK 응답** — 응답자가 선택적 데이터를 포함합니다.
3. **ACK 완료** — 신뢰성과 세션 상태를 확립합니다.
4. **FIN/RESET** — 정상 종료 또는 강제 종료에 사용됩니다.

### 단편화 및 재정렬

I2P 터널은 지연과 메시지 재정렬을 야기하기 때문에, 라이브러리는 알려지지 않았거나 일찍 도착한 스트림의 패킷을 버퍼링합니다. 버퍼링된 메시지는 동기화가 완료될 때까지 저장되어 완전하고 순서대로 전달되도록 보장합니다.

### 프로토콜 강제 적용

`i2p.streaming.enforceProtocol=true` 옵션(0.9.36 이후 기본값)은 연결이 올바른 I2CP 프로토콜 번호를 사용하도록 보장하여, 하나의 destination을 공유하는 여러 하위 시스템 간의 충돌을 방지합니다.

---

## 상호 운용성 및 모범 사례

스트리밍 프로토콜은 **Datagram API**와 함께 제공되어, 개발자가 연결 지향 전송과 비연결 전송 중에서 선택할 수 있도록 합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### 공유 클라이언트

애플리케이션은 **공유 클라이언트**로 실행하여 기존 터널을 재사용할 수 있으며, 여러 서비스가 동일한 목적지를 공유할 수 있습니다. 이는 오버헤드를 줄이지만 서비스 간 상관관계 위험을 증가시키므로 주의해서 사용해야 합니다.

### 혼잡 제어

- 스트리밍 계층은 RTT 기반 피드백을 통해 네트워크 지연 시간과 처리량에 지속적으로 적응합니다.
- 라우터가 기여 피어(참여 tunnel 활성화)일 때 애플리케이션이 최상의 성능을 발휘합니다.
- TCP와 유사한 혼잡 제어 메커니즘은 느린 피어의 과부하를 방지하고 tunnel 전반에 걸쳐 대역폭 사용의 균형을 맞추는 데 도움을 줍니다.

### 지연 시간 고려사항

I2P는 수백 밀리초의 기본 지연 시간을 추가하므로, 애플리케이션은 왕복 횟수를 최소화해야 합니다. 가능한 경우 연결 설정과 함께 데이터를 묶어 전송하세요(예: SYN에 HTTP 요청 포함). 많은 작은 순차적 교환에 의존하는 설계는 피하세요.

---

## 테스트 및 호환성

- 완전한 호환성을 보장하기 위해 항상 **Java I2P**와 **i2pd** 모두에 대해 테스트하세요.
- 프로토콜이 표준화되어 있지만, 구현상의 사소한 차이가 존재할 수 있습니다.
- 이전 버전 router를 우아하게 처리하세요—많은 피어가 여전히 2.0 이전 버전을 실행하고 있습니다.
- `I2PSocket.getOptions()`와 `getSession()`을 사용하여 연결 통계를 모니터링하고 RTT 및 재전송 메트릭을 읽으세요.

성능은 터널 구성에 크게 의존합니다:   - **짧은 터널 (1–2 hops)** → 낮은 지연시간, 익명성 감소.   - **긴 터널 (3+ hops)** → 높은 익명성, RTT 증가.

---

## 주요 개선 사항 (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## 요약

**I2P Streaming Library**는 I2P 내 모든 신뢰할 수 있는 통신의 핵심입니다. 순서가 보장되고 인증되며 암호화된 메시지 전달을 보장하고, 익명 환경에서 TCP를 거의 그대로 대체할 수 있는 기능을 제공합니다.

최적의 성능을 달성하려면: - SYN+페이로드 번들링으로 왕복 횟수를 최소화하세요.   - 워크로드에 맞게 윈도우 및 타임아웃 매개변수를 조정하세요.   - 지연 시간에 민감한 애플리케이션의 경우 더 짧은 tunnel을 사용하세요.   - 피어에 과부하가 걸리지 않도록 혼잡 제어 친화적인 설계를 사용하세요.
