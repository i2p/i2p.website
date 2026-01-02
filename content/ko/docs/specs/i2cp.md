---
title: "I2P 클라이언트 프로토콜 (I2CP)"
description: "애플리케이션이 I2P router와 세션, tunnels, LeaseSets를 협상하는 방법"
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

I2CP는 I2P router와 임의의 클라이언트 프로세스 사이의 하위 수준 제어 프로토콜이다. 이는 책임의 엄격한 분리를 정의한다:

- **Router**: 라우팅, 암호화, tunnel 수명 주기, 네트워크 데이터베이스 작업을 관리합니다
- **클라이언트**: 익명성 속성을 선택하고, tunnel을 구성하며, 메시지를 전송/수신합니다

모든 통신은 단일 TCP 소켓(선택적으로 TLS로 래핑됨)을 통해 이루어지며, 비동기식, 풀 듀플렉스 동작을 가능하게 합니다.

**Protocol Version**: I2CP는 초기 연결 수립 시 전송되는 프로토콜 버전 바이트 `0x2A`(10진수 42)를 사용합니다. 이 버전 바이트는 프로토콜 도입 이후로 변함없이 안정적으로 유지되고 있습니다.

**현재 상태**: 본 사양은 2025-09에 릴리스된 router 버전 0.9.67(API 버전 0.9.67)에 대해 정확합니다.

## 구현 컨텍스트

### Java 구현체

레퍼런스 구현은 Java I2P에 포함되어 있습니다: - 클라이언트 SDK: `i2p.jar` 패키지 - Router 구현: `router.jar` 패키지 - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

클라이언트와 router가 동일한 JVM에서 실행될 때, I2CP 메시지는 직렬화 없이 Java 객체로 전달됩니다. 외부 클라이언트는 TCP를 통해 직렬화된 프로토콜을 사용합니다.

### C++ 구현

i2pd (C++ I2P router)는 클라이언트 연결을 위해 외부적으로 I2CP(클라이언트와 router 간 통신 프로토콜)도 구현합니다.

### 비 Java 클라이언트

완전한 I2CP 클라이언트 라이브러리에 대해서는 **알려진 비 Java 구현이 없습니다**. Java가 아닌 애플리케이션은 대신 상위 수준 프로토콜을 사용해야 합니다:

- **SAM (Simple Anonymous Messaging) v3**: 여러 언어용 라이브러리가 있는 소켓 기반 인터페이스
- **BOB (Basic Open Bridge)**: SAM의 더 간단한 대안

이러한 상위 수준 프로토콜은 I2CP의 복잡성을 내부적으로 처리하고, TCP와 유사한 연결을 위한 스트리밍 라이브러리와 UDP와 유사한 연결을 위한 데이터그램 라이브러리도 제공합니다.

## 연결 설정

### 1. TCP 연결

router의 I2CP 포트에 연결: - 기본값: `127.0.0.1:7654` - router 설정에서 구성 가능 - 선택적 TLS 래퍼(원격 연결의 경우 강력히 권장)

### 2. 프로토콜 핸드셰이크

**1단계**: 프로토콜 버전 바이트 `0x2A`를 전송

**2단계**: 시계 동기화

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
router는 현재 타임스탬프와 I2CP API 버전 문자열을 반환합니다(0.8.7부터).

**3단계**: 인증(활성화된 경우)

0.9.11부터 인증은 다음을 포함하는 Mapping을 통해 GetDateMessage에 포함될 수 있습니다: - `i2cp.username` - `i2cp.password`

0.9.16부터 인증이 활성화된 경우, 다른 어떤 메시지가 전송되기 전에 GetDateMessage(날짜 요청 메시지)를 통해 **반드시** 완료되어야 합니다.

**4단계**: 세션 생성

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**5단계**: Tunnel 준비 신호

```
Router → Client: RequestVariableLeaseSetMessage
```
이 메시지는 인바운드 tunnel이 구축되었음을 나타냅니다. router는 적어도 하나의 인바운드 tunnel과 하나의 아웃바운드 tunnel이 존재하기 전에는 이를 전송하지 않습니다.

**6단계**: LeaseSet 게시

```
Client → Router: CreateLeaseSet2Message
```
이 시점에서 세션은 메시지 송수신을 위해 완전히 동작합니다.

## 메시지 흐름 패턴

### 발신 메시지 (클라이언트가 원격 목적지로 보냄)

**i2cp.messageReliability=none 설정 시**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**i2cp.messageReliability=BestEffort 설정 시**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### 수신 메시지 (Router가 클라이언트로 전달)

**i2cp.fastReceive=true인 경우** (0.9.4부터 기본값):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**i2cp.fastReceive=false로 설정 시** (사용 중단됨):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
최신 클라이언트는 항상 빠른 수신 모드를 사용해야 합니다.

## 공통 자료 구조

### I2CP 메시지 헤더

모든 I2CP 메시지는 이 공통 헤더를 사용합니다:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **본문 길이**: 4바이트 정수, 메시지 본문 길이만 (헤더 제외)
- **유형**: 1바이트 정수, 메시지 유형 식별자
- **메시지 본문**: 0바이트 이상, 형식은 메시지 유형에 따라 달라짐

**메시지 크기 제한**: 최대 약 64 KB.

### 세션 ID

router에서 세션을 고유하게 식별하는 2바이트 정수.

**특수 값**: `0xFFFF`는 "세션 없음"을 나타냅니다(설정된 세션 없이 호스트명 조회에 사용).

### 메시지 ID

세션 내의 메시지를 고유하게 식별하기 위해 router가 생성하는 4바이트 정수.

**중요**: 메시지 ID는 전역적으로 **고유하지** 않으며, 세션 내에서만 고유합니다. 또한 클라이언트가 생성한 nonce(임의 일회성 값)와도 구별됩니다.

### 페이로드 형식

메시지 페이로드는 표준 10바이트 gzip 헤더를 사용해 gzip으로 압축됩니다:
- 시작은 다음과 같습니다: `0x1F 0x8B 0x08` (RFC 1952)
- 0.7.1부터: gzip 헤더의 사용되지 않는 부분에는 프로토콜, from-port, to-port 정보가 포함됩니다
- 이는 동일한 목적지에서 스트리밍과 데이터그램을 모두 사용할 수 있게 합니다

**압축 제어**: 압축을 비활성화하려면 `i2cp.gzip=false`로 설정하세요(gzip effort(압축 노력 수준)을 0으로 설정). gzip 헤더는 여전히 포함되지만, 압축 오버헤드는 최소화됩니다.

### SessionConfig 구조체

클라이언트 세션에 대한 구성을 정의합니다:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**중요 요구사항**: 1. **Mapping은 키 기준으로 정렬되어 있어야 합니다** 서명 검증을 위해 2. **Creation Date**는 router의 현재 시간으로부터 ±30초 이내여야 합니다 3. **Signature**는 Destination(목적지)의 SigningPrivateKey로 생성됩니다

**Offline Signatures(오프라인 서명)** (0.9.38 기준):

offline signing(오프라인 서명)을 사용하는 경우, 매핑에는 다음이 포함되어야 합니다: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

그 후 임시 SigningPrivateKey(서명용 개인 키)에 의해 서명이 생성됩니다.

## 코어 구성 옵션

### Tunnel 구성

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**참고**: - `quantity` 값이 6을 초과하면 0.9.0+를 실행 중인 피어가 필요하며 리소스 사용량이 크게 증가합니다 - 고가용성 서비스의 경우 `backupQuantity`를 1-2로 설정하십시오 - Zero-hop tunnels는 지연 시간을 줄이는 대신 익명성을 희생하지만 테스트에는 유용합니다

### 메시지 처리

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**메시지 신뢰성**: - `None`: router 확인 응답 없음 (스트리밍 라이브러리의 기본값, 0.8.1부터) - `BestEffort`: Router가 수락 + 성공/실패 알림을 보냄 - `Guaranteed`: 미구현됨 (현재는 BestEffort처럼 동작)

**메시지별 재정의** (0.9.14부터): - `messageReliability=none`인 세션에서 0이 아닌 nonce(임의 일회성 값)를 설정하면 해당 특정 메시지에 대한 전달 확인 알림을 요청합니다 - `BestEffort` 세션에서 nonce=0으로 설정하면 해당 메시지에 대한 전달 확인 알림이 비활성화됩니다

### LeaseSet(목적지의 수신 터널 정보를 담은 레코드) 구성

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### 레거시 ElGamal/AES 세션 태그

다음 옵션은 레거시 ElGamal 암호화에만 해당됩니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**참고**: ECIES-X25519 클라이언트는 다른 ratchet mechanism(래칫 메커니즘)을 사용하며 이 옵션들을 무시합니다.

## 암호화 유형

I2CP는 `i2cp.leaseSetEncType` 옵션을 통해 여러 종단 간 암호화 방식을 지원합니다. 최신 및 구형 피어 모두를 지원하기 위해 여러 타입을 쉼표로 구분하여 지정할 수 있습니다.

### 지원되는 암호화 유형

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**권장 구성**:

```
i2cp.leaseSetEncType=4,0
```
이는 X25519(곡선25519 기반 키 교환 방식, 권장)을 제공하며, 호환성을 위해 ElGamal(공개키 암호 방식)로 폴백합니다.

### 암호화 유형 상세 정보

**유형 0 - ElGamal/AES+SessionTags**: - 2048비트 ElGamal 공개 키(256바이트) - AES-256 대칭 암호화 - 32바이트 session tags(세션 태그)를 묶음 단위로 전송 - 높은 CPU, 대역폭 및 메모리 오버헤드 - 네트워크 전반에서 단계적으로 폐지 중

**타입 4 - ECIES-X25519-AEAD-Ratchet**: - X25519 키 교환(32바이트 키) - ChaCha20/Poly1305 AEAD - Signal 스타일의 double ratchet(이중 래칫) - 8바이트 세션 태그(ElGamal 대비 32바이트) - 태그는 동기화된 PRNG(의사난수 생성기)를 통해 생성됨(사전에 전송하지 않음) - ~92% 오버헤드 감소(ElGamal 대비) - 현행 I2P의 표준(대부분의 router가 이를 사용)

**유형 5-6 - 포스트-양자 하이브리드**: - X25519와 ML-KEM (NIST FIPS 203, 모듈 격자 기반 키 캡슐화 메커니즘)을 결합 - 양자 내성 보안을 제공 - 균형 잡힌 보안/성능을 위한 ML-KEM-768 - 최대 보안을 위한 ML-KEM-1024 - 포스트-양자(PQ) 키 자료로 인해 메시지 크기가 더 큼 - 네트워크 지원은 아직 배포 진행 중

### 마이그레이션 전략

I2P 네트워크는 ElGamal(유형 0)에서 X25519(유형 4)로 적극적으로 전환 중입니다: - NTCP → NTCP2 (완료) - SSU → SSU2 (완료) - ElGamal tunnels → X25519 tunnels (완료) - ElGamal 종단 간 → ECIES-X25519 (대부분 완료)

## LeaseSet2 및 고급 기능

### LeaseSet2 옵션 (0.9.38부터)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Blinded Addresses(블라인딩 주소)

0.9.39부터 Destination(연결 대상 식별자)은 주기적으로 변경되는 "blinded"(블라인딩 처리된) 주소(b33 형식)를 사용할 수 있습니다: - 비밀번호 보호를 위해 `i2cp.leaseSetSecret`가 필요합니다 - 클라이언트별 인증은 선택 사항입니다 - 자세한 내용은 proposal 123 및 149를 참조하세요

### 서비스 레코드(0.9.66부터)

LeaseSet2는 서비스 레코드 옵션을 지원합니다(제안 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
형식은 DNS SRV 레코드 스타일을 따르되 I2P에 맞게 조정되었습니다.

## 여러 세션 (0.9.21 이후)

하나의 I2CP 연결로 여러 세션을 유지할 수 있습니다:

**기본 세션**: 한 연결에서 처음 생성된 세션 **하위 세션**: 기본 세션의 tunnel 풀을 공유하는 추가 세션

### Subsession(하위 세션) 특성

1. **공유된 tunnel**: 기본과 동일한 인바운드/아웃바운드 tunnel 풀을 사용
2. **공유된 암호화 키**: 동일한 LeaseSet 암호화 키를 사용해야 함
3. **서로 다른 서명 키**: 서로 다른 Destination(목적지 식별자) 서명 키를 사용해야 함
4. **익명성 보장 없음**: 기본 세션과 명확히 연결됨 (동일한 router, 동일한 tunnel)

### 서브세션 사용 사례

다양한 서명 유형을 사용하는 목적지와의 통신을 활성화합니다: - 기본: EdDSA 서명(최신) - 하위 세션: DSA 서명(레거시 호환성)

### Subsession(하위 세션) 라이프사이클

**생성**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**소멸**: - 하위 세션 소멸: 기본 세션은 그대로 유지됨 - 기본 세션 소멸: 모든 하위 세션을 소멸하고 연결을 종료 - DisconnectMessage(연결 해제 메시지): 모든 세션을 소멸

### 세션 ID 처리

대부분의 I2CP 메시지에는 세션 ID 필드가 포함됩니다. 예외: - DestLookup / DestReply (사용 중단됨, HostLookup / HostReply 사용) - GetBandwidthLimits / BandwidthLimits (응답이 세션에 종속되지 않음)

**중요**: 응답을 요청과 확정적으로 매칭할 수 없으므로, 클라이언트는 CreateSession(세션 생성) 메시지를 동시에 여러 개 보류 중 상태로 두지 않아야 합니다.

## 메시지 카탈로그

### 메시지 유형 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**범례**: C = 클라이언트, R = Router

### 핵심 메시지 세부 정보

#### CreateSessionMessage (유형 1)

**목적**: 새 I2CP 세션 개시

**내용**: SessionConfig 구조체

**응답**: SessionStatusMessage (세션 상태 메시지) (status=Created 또는 Invalid)

**요구 사항**: - SessionConfig의 Date는 router 시간의 ±30초 이내여야 합니다 - 서명 검증을 위해 매핑은 키 기준으로 정렬되어야 합니다 - Destination(목적지)에 대해 이미 활성 세션이 존재해서는 안 됩니다

#### RequestVariableLeaseSetMessage (유형 37)

**Purpose**: Router가 인바운드 tunnels에 대한 클라이언트 권한 부여를 요청합니다

**내용**: - 세션 ID - leases(I2P에서 목적지로 가는 터널과 만료 시간을 포함한 엔트리)의 개수 - Lease 구조체 배열(각각 개별 만료 시간 포함)

**응답**: CreateLeaseSet2Message(LeaseSet2 생성 메시지)

**의미**: 이는 세션이 정상적으로 동작 중임을 알리는 신호입니다. router는 다음 조건이 충족된 후에만 이를 전송합니다: 1. 인바운드 tunnel이 최소 1개 구축됨 2. 아웃바운드 tunnel이 최소 1개 구축됨

**타임아웃 권장사항**: 세션 생성 후 5분 이상이 지나도 이 메시지를 수신하지 못한 경우, 클라이언트는 세션을 종료해야 합니다.

#### CreateLeaseSet2Message (유형 41)

**목적**: 클라이언트가 LeaseSet(서비스 접속 정보 집합)을 네트워크 데이터베이스(netDb)에 게시한다

**내용**: - 세션 ID - LeaseSet 타입 바이트 (1, 3, 5, 또는 7) - LeaseSet 또는 LeaseSet2 또는 EncryptedLeaseSet 또는 MetaLeaseSet - 개인 키 개수 - 개인 키 목록 (LeaseSet의 각 공개 키당 하나, 같은 순서)

**개인 키**: 수신되는 garlic 메시지(여러 개의 메시지를 하나로 묶어 전달하는 I2P 메시지 형식)를 복호화하는 데 필요합니다. 형식:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**참고**: 다음을 처리하지 못하는 사용 중단된 CreateLeaseSetMessage(LeaseSet 생성 메시지) (type 4)을 대체합니다: - LeaseSet2(LeaseSet의 2세대 형식) 변형 - ElGamal이 아닌 암호화 - 여러 암호화 유형 - 암호화된 LeaseSets - 오프라인 서명 키

#### SendMessageExpiresMessage (유형 36)

**목적**: 만료 시간 및 고급 옵션을 지정하여 메시지를 목적지로 전송

**Content**: - 세션 ID - 목적지 - 페이로드 (gzip으로 압축됨) - 논스 (4바이트) - 플래그 (2바이트) - 아래 참조 - 만료 시각 (6바이트, 8바이트에서 잘림)

**플래그 필드** (2바이트, 비트 순서 15...0):

**비트 15-11**: 미사용, 반드시 0이어야 함

**비트 10-9**: 메시지 신뢰성 오버라이드 (미사용, 대신 nonce(논스, 한 번만 사용하는 값)를 사용)

**비트 8**: LeaseSet을 포함하지 않음 - 0: Router는 garlic(가릴릭, I2P의 다중 페이로드 메시지 방식) 안에 LeaseSet을 포함할 수 있음 - 1: LeaseSet을 포함하지 않음

**비트 7-4**: 낮은 태그 임계값 (ElGamal(엘가말 암호)에만 해당, ECIES(타원곡선 통합 암호 방식)에서는 무시됨)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**비트 3-0**: 필요한 경우 전송할 태그(ElGamal에서만 사용되며, ECIES에서는 무시됨)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage(메시지 상태 메시지) (유형 22)

**목적**: 클라이언트에게 메시지 전달 상태를 알림

**내용**: - 세션 ID - 메시지 ID (router에서 생성됨) - 상태 코드 (1 바이트) - 크기 (4 바이트, status=0인 경우에만 해당) - 논스 (4 바이트, 클라이언트의 SendMessage 논스와 일치)

**상태 코드** (발신 메시지):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**성공 코드**: 1, 2, 4, 6 **실패 코드**: 그 외 모두

**상태 코드 0** (사용 중단됨): 사용 가능한 메시지 (수신, 빠른 수신 기능 비활성화됨)

#### HostLookupMessage (호스트 조회 메시지, 유형 38)

**목적**: 호스트명 또는 해시로 목적지 조회 (DestLookup을 대체)

**Content**: - 세션 ID (세션이 없으면 0xFFFF) - 요청 ID (4바이트) - 밀리초 단위의 타임아웃 (4바이트, 권장 최소값: 10000) - 요청 유형 (1바이트) - 조회 키 (해시, 호스트명 문자열 또는 Destination(목적지))

**요청 유형**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
유형 2-4는 가능한 경우 LeaseSet 옵션(제안 167)을 반환합니다.

**응답**: HostReplyMessage

#### HostReplyMessage (호스트 응답 메시지) (유형 39)

**목적**: HostLookupMessage(호스트 조회 메시지)에 대한 응답

**내용**: - 세션 ID - 요청 ID - 결과 코드(1바이트) - 목적지(성공 시 포함되며, 특정 실패 시에도 포함될 수 있음) - 매핑(조회 유형 2-4에만 해당하며, 비어 있을 수 있음)

**결과 코드**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (블라인딩 정보 메시지) (유형 42)

**목적**: router에게 blinded destination(블라인드된 목적지)의 인증 요구사항을 알림 (0.9.43부터)

**내용**: - 세션 ID - 플래그(1바이트) - 엔드포인트 유형(1바이트): 0=Hash, 1=호스트명, 2=Destination(목적지 식별자), 3=SigType+Key - 블라인드 서명 유형(2바이트) - 만료 시간(4바이트, epoch 이후 초 단위) - 엔드포인트 데이터(유형에 따라 다름) - 개인 키(32바이트, 플래그 비트 0이 설정된 경우에만) - 조회 비밀번호(String, 플래그 비트 4가 설정된 경우에만)

**플래그** (비트 순서 76543210):

- **비트 0**: 0=모두, 1=클라이언트별
- **비트 3-1**: 인증 방식(비트 0=1인 경우): 000=DH(디피-헬만), 001=PSK(사전 공유 키)
- **비트 4**: 1=비밀값 필요
- **비트 7-5**: 사용되지 않음, 0으로 설정

**응답 없음**: Router는 조용히 처리합니다

**Use Case**: 블라인드 목적지(b33 주소)로 전송하기 전에, 클라이언트는 다음 중 하나를 반드시 수행해야 합니다: 1. HostLookup을 통해 b33 주소를 조회하거나, 2. BlindingInfo 메시지를 전송

목적지가 인증을 요구하는 경우, BlindingInfo는 필수입니다.

#### ReconfigureSessionMessage (유형 2)

**목적**: 생성 후 세션 설정 업데이트

**내용**: - 세션 ID - SessionConfig (변경된 옵션만 필요)

**응답**: SessionStatusMessage(세션 상태 메시지) (status=Updated or Invalid)

**참고**: - router는 새 구성을 기존 구성과 병합합니다 - Tunnel 옵션 (`inbound.*`, `outbound.*`)은 항상 적용됩니다 - 일부 옵션은 세션 생성 후 변경할 수 없을 수 있습니다 - 날짜는 router 시간의 ±30초 이내여야 합니다 - 매핑은 키 기준으로 정렬되어야 합니다

#### DestroySessionMessage (유형 3)

**목적**: 세션 종료

**내용**: 세션 ID

**예상 응답**: SessionStatusMessage (status=Destroyed)

**실제 동작** (Java I2P 0.9.66까지): - Router는 SessionStatus(Destroyed)를 절대 보내지 않음 - 세션이 남아 있지 않은 경우: DisconnectMessage 전송 - subsessions(하위 세션)이 남아 있는 경우: 응답 없음

**중요**: Java I2P의 동작은 명세와 다릅니다. 구현체는 각 subsession(하위 세션)을 종료할 때 주의해야 합니다.

#### DisconnectMessage(연결 해제 메시지) (유형 30)

**목적**: 연결이 곧 종료될 것임을 알림

**내용**: 사유 문자열

**효과**: 해당 연결의 모든 세션이 종료되고, 소켓이 닫힙니다

**구현**: 주로 Java I2P에서 router → 클라이언트

## 프로토콜 버전 연혁

### 버전 감지

I2CP 프로토콜 버전은 0.8.7부터 Get/SetDate 메시지에서 교환된다. 이전 버전의 router에서는 버전 정보를 확인할 수 없다.

**버전 문자열**: "core" API 버전을 의미하며, 반드시 router 버전인 것은 아닙니다.

### 기능 연대표

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## 보안 고려 사항

### 인증

**기본값**: 인증이 필요하지 않음 **선택 사항**: 사용자 이름/비밀번호 인증 (0.9.11부터) **필수**: 활성화되면 다른 메시지 전에 인증이 완료되어야 함 (0.9.16부터)

**원격 연결**: 자격 증명과 개인 키를 보호하기 위해 항상 TLS (`i2cp.SSL=true`)를 사용하세요.

### 시계 오차

SessionConfig Date는 router 시간과 ±30초 이내여야 하며, 그렇지 않으면 세션이 거부됩니다. 동기화하려면 Get/SetDate를 사용하십시오.

### 개인 키 관리

CreateLeaseSet2Message(LeaseSet2 생성 메시지)에는 수신 메시지를 복호화하기 위한 비밀 키가 포함되어 있습니다. 이 키들은 다음과 같아야 합니다: - 안전하게 전송(원격 연결에는 TLS 사용) - router에서 안전하게 저장 - 침해되었을 때 교체

### 메시지 만료

명시적 만료 시간을 설정하려면 SendMessageExpires (SendMessage가 아님)을 항상 사용하세요. 이렇게 하면: - 메시지가 무기한으로 대기열에 쌓이는 것을 방지합니다 - 리소스 사용량을 줄입니다 - 신뢰성을 향상시킵니다

### 세션 태그 관리

**ElGamal** (사용 중단됨): - 태그는 일괄로 전송되어야 함 - 태그 손실 시 복호화 실패 발생 - 높은 메모리 오버헤드

**ECIES-X25519** (타원 곡선 통합 암호 방식의 하나, Curve25519 기반) (현재): - 동기화된 의사난수 생성기(PRNG)를 통해 태그 생성 - 사전 전송 불필요 - 메시지 손실에 강함 - 오버헤드가 크게 낮음

## 모범 사례

### 클라이언트 개발자를 위한

1. **빠른 수신 모드 사용**: 항상 `i2cp.fastReceive=true`로 설정하세요 (또는 기본값을 사용)

2. **ECIES-X25519(타원곡선 기반 키 교환/암호화 스위트)을 우선 사용**: 호환성을 유지하면서 최상의 성능을 위해 `i2cp.leaseSetEncType=4,0`로 설정하세요

3. **만료를 명시적으로 설정**: SendMessageExpires를 사용하고, SendMessage는 사용하지 마십시오

4. **Subsessions(하위 세션)을 신중하게 다루세요**: subsessions은 목적지 간 익명성을 제공하지 않는다는 점에 유의하세요

5. **세션 생성 시간 초과**: 5분 이내에 RequestVariableLeaseSet을 수신하지 못하면 세션을 파기한다

6. **구성 매핑 정렬**: SessionConfig에 서명하기 전에 항상 Mapping 키를 정렬하세요

7. **적절한 Tunnel 개수 사용**: 필요한 경우가 아니면 `quantity` > 6로 설정하지 마세요

8. **Java가 아닌 환경에서는 SAM/BOB(외부 애플리케이션을 I2P에 연결하는 프로토콜)를 고려하세요**: I2CP를 직접 사용하는 대신 SAM을 구현하세요

### Router 개발자를 위한

1. **날짜 유효성 검사**: SessionConfig 일시에 대해 ±30초 허용 오차 범위를 강제 적용

2. **메시지 크기 제한**: 최대 메시지 크기를 ~64 KB로 강제합니다

3. **다중 세션 지원**: 0.9.21 사양에 따라 subsession(하위 세션) 지원을 구현한다

4. **RequestVariableLeaseSet(가변 leaseSet 요청)을 신속히 전송**: inbound 및 outbound tunnel이 모두 존재한 이후에만

5. **더 이상 권장되지 않는 메시지 처리**: 허용하되 ReceiveMessageBegin/End 사용은 지양

6. **ECIES-X25519 지원**: (타원곡선 기반 하이브리드 암호 방식의 X25519 변형) 신규 배포에서는 type 4 암호화를 우선적으로 사용하십시오

## 디버깅 및 문제 해결

### 일반적인 문제

**세션 거부됨(유효하지 않음)**: - 시계 오차를 확인(±30초 이내여야 함) - 매핑이 키 기준으로 정렬되어 있는지 확인 - Destination(목적지)가 이미 사용 중이 아닌지 확인

**No RequestVariableLeaseSet**: - Router가 tunnel 구축 중일 수 있습니다 (최대 5분까지 기다리세요) - 네트워크 연결 문제를 확인하세요 - 충분한 피어 연결이 있는지 확인하세요

**메시지 전달 실패**: - 구체적인 실패 원인을 파악하려면 MessageStatus 코드를 확인 - 원격 LeaseSet이 게시되어 있고 최신 상태인지 확인 - 호환되는 암호화 유형을 사용하고 있는지 확인

**Subsession(하위 세션) 문제**: - 기본 세션이 먼저 생성되었는지 확인 - 암호화 키가 동일한지 확인 - 서명 키가 서로 다른지 확인

### 진단 메시지

**GetBandwidthLimits**: router 용량을 조회 **HostLookup**: 이름 해석과 LeaseSet 가용성을 테스트 **MessageStatus**: 종단 간 메시지 전달을 추적

## 관련 명세

- **공통 구조**: /docs/specs/common-structures/
- **I2NP (네트워크 프로토콜)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **tunnel 생성**: /docs/specs/implementation/
- **스트리밍 라이브러리**: /docs/specs/streaming/
- **데이터그램 라이브러리**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## 참조된 제안서

- [제안 123](/proposals/123-new-netdb-entries/): 암호화된 LeaseSets 및 인증
- [제안 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [제안 149](/proposals/149-b32-encrypted-ls2/): 블라인드 주소 형식(b33)
- [제안 152](/proposals/152-ecies-tunnels/): X25519 tunnel 생성
- [제안 154](/proposals/154-ecies-lookups/): ECIES 목적지에서의 데이터베이스 조회
- [제안 156](/proposals/156-ecies-routers/): Router의 ECIES-X25519로의 마이그레이션
- [제안 161](/ko/proposals/161-ri-dest-padding/): Destination 패딩 압축
- [제안 167](/proposals/167-service-records/): LeaseSet 서비스 레코드
- [제안 169](/proposals/169-pq-crypto/): 포스트-양자 하이브리드 암호(ML-KEM)

## Javadoc 레퍼런스

- [I2CP 패키지](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [클라이언트 API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## 사용 중단 요약

### 사용 중단된 메시지(사용하지 마십시오)

- **CreateLeaseSetMessage** (유형 4): CreateLeaseSet2Message를 사용하십시오
- **RequestLeaseSetMessage** (유형 21): RequestVariableLeaseSetMessage를 사용하십시오
- **ReceiveMessageBeginMessage** (유형 6): 빠른 수신 모드를 사용하십시오
- **ReceiveMessageEndMessage** (유형 7): 빠른 수신 모드를 사용하십시오
- **DestLookupMessage** (유형 34): HostLookupMessage를 사용하십시오
- **DestReplyMessage** (유형 35): HostReplyMessage를 사용하십시오
- **ReportAbuseMessage** (유형 29): 미구현

### 사용 중단된 옵션

- ElGamal 암호화 (type 0): ECIES-X25519 (type 4)로 이전
- DSA 서명: EdDSA 또는 ECDSA로 이전
- `i2cp.fastReceive=false`: 항상 빠른 수신 모드를 사용
