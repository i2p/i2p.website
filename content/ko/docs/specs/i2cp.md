---
title: "I2P Client Protocol (I2CP)"
description: "애플리케이션이 I2P router와 세션, tunnel, leaseSet을 협상하는 방법."
slug: "i2cp"
aliases:
  - "/ko/docs/api/i2cp"
  - "/ko/docs/api/i2cp/"
  - "/ko/docs/specs/i2cp-spec"
  - "/ko/docs/specs/i2cp-spec/"
  - "/ko/i2cp_spec"
  - "/ko/i2cp_spec/"
category: "프로토콜"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## 개요

이것은 I2P Control Protocol (I2CP)의 사양으로, 클라이언트와 router 간의 저수준 인터페이스입니다. Java 클라이언트는 이 프로토콜을 구현하는 I2CP 클라이언트 API를 사용합니다.

I2CP를 구현하는 클라이언트 측 라이브러리의 Java가 아닌 구현체는 알려진 것이 없습니다. 또한 소켓 지향(스트리밍) 애플리케이션에는 스트리밍 프로토콜의 구현이 필요하지만, 이에 대한 Java가 아닌 라이브러리도 존재하지 않습니다. 따라서 Java가 아닌 클라이언트는 대신 여러 언어로 라이브러리가 존재하는 상위 계층 프로토콜인 SAM [SAMv3](/docs/api/samv3/)를 사용해야 합니다.

이것은 Java I2P router에서 내부적으로와 외부적으로 모두 지원되는 저수준 프로토콜입니다. 클라이언트와 router가 같은 JVM에 있지 않은 경우에만 프로토콜이 직렬화되며, 그렇지 않으면 I2CP 메시지 Java 객체들이 내부 JVM 인터페이스를 통해 전달됩니다. I2CP는 C++ router인 i2pd에서도 외부적으로 지원됩니다.

자세한 정보는 I2CP 개요 페이지 [I2CP](/docs/specs/i2cp/)에서 확인할 수 있습니다.

## 세션

이 프로토콜은 단일 TCP 연결을 통해 각각 2바이트 세션 ID를 가진 여러 "세션"을 처리하도록 설계되었지만, 다중 세션은 버전 0.9.21까지 구현되지 않았습니다. [아래의 다중세션 섹션](#multisession)을 참조하세요. 버전 0.9.21보다 이전 버전의 router에서는 단일 I2CP 연결에서 다중 세션을 사용하려고 시도하지 마세요.

또한 단일 클라이언트가 별도의 연결을 통해 여러 router와 통신할 수 있는 규정이 있는 것으로 보입니다. 이 기능은 아직 테스트되지 않았으며, 아마도 유용하지 않을 것입니다.

연결이 끊긴 후 세션을 유지하거나 다른 I2CP 연결에서 복구할 수 있는 방법은 없습니다. 소켓이 닫히면 세션도 삭제됩니다.

## 예제 메시지 시퀀스

참고: 아래 예제들은 클라이언트가 router에 처음 연결할 때 보내야 하는 Protocol Byte (0x2a)를 보여주지 않습니다. 연결 초기화에 대한 자세한 정보는 I2CP 개요 페이지 [I2CP](/docs/specs/i2cp/)에서 확인할 수 있습니다.

### 표준 세션 설정

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### 대역폭 제한 가져오기 (단순 세션)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### 목적지 조회 (간단한 세션)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### 발신 메시지

기존 세션, i2cp.messageReliability=none 설정

```
  Client                                           Router

                           --------------------->  Send Message Message

```
기존 세션, i2cp.messageReliability=none 및 0이 아닌 nonce 사용

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
기존 세션, i2cp.messageReliability=BestEffort 설정

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### 수신 메시지

기존 세션, i2cp.fastReceive=true와 함께 (0.9.4부터)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
기존 세션, i2cp.fastReceive=false 사용 (지원 중단됨)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### 멀티세션 참고사항 {#multisession}

router 버전 0.9.21부터 단일 I2CP 연결에서 다중 세션이 지원됩니다. 생성되는 첫 번째 세션이 "기본 세션"입니다. 추가 세션은 "하위 세션"입니다. 하위 세션은 공통 tunnel 세트를 공유하는 여러 목적지를 지원하는 데 사용됩니다. 초기 애플리케이션은 기본 세션이 ECDSA 서명 키를 사용하고, 하위 세션은 기존 eepsite와의 통신을 위해 DSA 서명 키를 사용하는 것입니다.

서브세션은 기본 세션과 동일한 인바운드 및 아웃바운드 터널 풀을 공유합니다. 서브세션은 기본 세션과 동일한 암호화 키를 사용해야 합니다. 이는 LeaseSet 암호화 키와 (사용되지 않는) Destination 암호화 키 모두에 적용됩니다. 서브세션은 destination에서 다른 서명 키를 사용해야 하므로, destination 해시가 기본 세션과 다릅니다. 서브세션이 기본 세션과 동일한 암호화 키와 터널을 사용하므로, 해당 Destination들이 동일한 router에서 실행되고 있음이 모든 이에게 명백하며, 따라서 일반적인 상관관계 방지 익명성 보장이 적용되지 않습니다.

서브세션은 일반적으로 CreateSession 메시지를 보내고 응답으로 SessionStatus 메시지를 받아 생성됩니다. 서브세션은 기본 세션이 생성된 후에 생성되어야 합니다. SessionStatus 응답에는 성공 시 기본 세션의 ID와 구별되는 고유한 세션 ID가 포함됩니다. CreateSession 메시지는 순서대로 처리되어야 하지만, CreateSession 메시지와 응답을 연관시킬 확실한 방법이 없으므로, 클라이언트는 여러 CreateSession 메시지를 동시에 대기 상태로 두어서는 안 됩니다. 서브세션의 SessionConfig 옵션은 기본 세션과 다를 경우 적용되지 않을 수 있습니다. 특히 서브세션은 기본 세션과 동일한 tunnel pool을 사용하므로 tunnel 옵션은 무시될 수 있습니다.

router는 각 Destination에 대해 별도의 RequestVariableLeaseSet 메시지를 클라이언트에 전송하며, 클라이언트는 각각에 대해 CreateLeaseSet 메시지로 응답해야 합니다. 두 Destination의 lease는 동일한 tunnel pool에서 선택되더라도 반드시 동일하지는 않습니다.

서브세션은 평소와 같이 DestroySession 메시지로 제거할 수 있습니다. 이는 주 세션을 제거하거나 I2CP 연결을 중단하지 않습니다. 하지만 주 세션을 제거하면 모든 서브세션이 제거되고 I2CP 연결이 중단됩니다. Disconnect 메시지는 모든 세션을 제거합니다.

대부분의 I2CP 메시지는 Session ID를 포함하지만 모든 메시지가 그런 것은 아닙니다. Session ID가 없는 메시지의 경우, 클라이언트는 router 응답을 적절히 처리하기 위해 추가 로직이 필요할 수 있습니다. DestLookup과 DestReply는 Session ID를 포함하지 않으므로, 대신 더 최신의 HostLookup과 HostReply를 사용하세요. GetBandwidthLimts와 BandwidthLimits는 session ID를 포함하지 않지만, 응답이 세션별로 특정되지는 않습니다.

### 버전 노트 {#notes}

클라이언트가 보내는 초기 프로토콜 버전 바이트(0x2a)는 변경될 것으로 예상되지 않습니다. 0.8.7 릴리스 이전에는 router의 버전 정보가 클라이언트에서 사용할 수 없어서 새로운 클라이언트가 오래된 router와 작동하지 못했습니다. 0.8.7 릴리스부터는 양측의 프로토콜 버전 문자열이 Get/Set Date Messages에서 교환됩니다. 앞으로 클라이언트는 이 정보를 사용하여 오래된 router와 올바르게 통신할 수 있습니다. 클라이언트와 router는 상대방이 지원하지 않는 메시지를 보내지 않아야 합니다. 일반적으로 지원되지 않는 메시지를 수신하면 세션을 끊기 때문입니다.

교환되는 버전 정보는 "코어" API 버전 또는 I2CP 프로토콜 버전이며, 반드시 router 버전과 일치하지는 않습니다.

I2CP 프로토콜 버전의 기본 요약은 다음과 같습니다. 자세한 내용은 아래를 참조하세요.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## 공통 구조 {#structures}

### I2CP 메시지 헤더 {#struct-I2CPMessageHeader}

#### 설명

메시지 길이와 메시지 유형을 포함하는 모든 I2CP 메시지의 공통 헤더입니다.

#### 목차

1.  메시지 본문의 길이를 지정하는 4바이트 [Integer](/docs/specs/common-structures/#integer)
2.  메시지 타입을 지정하는 1바이트 [Integer](/docs/specs/common-structures/#integer)
3.  I2CP 메시지 본문, 0바이트 이상

#### 참고사항

실제 메시지 길이 제한은 약 64 KB입니다.

### 메시지 ID {#struct-MessageId}

#### 설명

특정 시점에 특정 router에서 대기 중인 메시지를 고유하게 식별합니다. 이는 항상 router에 의해 생성되며 클라이언트에서 생성한 nonce와는 다릅니다.

#### 목차

1.  4 바이트 [Integer](/docs/specs/common-structures/#integer)

#### 참고사항

메시지 ID는 세션 내에서만 고유하며, 전역적으로 고유하지는 않습니다.

### 페이로드 {#struct-Payload}

#### 설명

이 구조는 하나의 Destination에서 다른 Destination으로 전달되는 메시지의 내용입니다.

#### 목차

1.  4바이트 [Integer](/docs/specs/common-structures/#integer) 길이
2.  그만큼의 바이트

#### 노트

페이로드는 I2CP 개요 페이지 [I2CP-FORMAT](/docs/specs/i2cp/#format)에 명시된 gzip 형식입니다.

실제 메시지 길이 제한은 약 64 KB입니다.

### 세션 설정 {#struct-SessionConfig}

#### 설명

특정 클라이언트 세션에 대한 구성 옵션을 정의합니다.

#### 목차

1.  [Destination](/docs/specs/common-structures/#destination)
2.  옵션의 [Mapping](/docs/specs/common-structures/#mapping)
3.  생성 [Date](/docs/specs/common-structures/#date)
4.  이전 3개 필드의 [Signature](/docs/specs/common-structures/#signature),
    [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)로 서명됨

#### 참고사항

- 옵션들은 I2CP 개요 페이지 [I2CP-OPTIONS](/docs/specs/i2cp/#options)에 명시되어 있습니다.
- [Mapping](/docs/specs/common-structures/#mapping)은 router에서 서명이 올바르게 검증될 수 있도록 키별로 정렬되어야 합니다.
- 생성 날짜는 router에서 처리될 때 현재 시간의 +/- 30초 이내여야 하며, 그렇지 않으면 설정이 거부됩니다.

#### 오프라인 서명

- [Destination](/docs/specs/common-structures/#destination)이 오프라인 서명된 경우,
  [Mapping](/docs/specs/common-structures/#mapping)에는 세 개의 옵션인
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, 그리고
  i2cp.leaseSetOfflineSignature가 포함되어야 합니다.
  [Signature](/docs/specs/common-structures/#signature)는 임시
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)에 의해 생성되고,
  i2cp.leaseSetTransientPublicKey에 지정된
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)로 검증됩니다.
  자세한 내용은 [I2CP-OPTIONS](/docs/specs/i2cp/#options)를 참조하십시오.

### 세션 ID {#struct-SessionId}

#### 설명

특정 시점에서 특정 router의 세션을 고유하게 식별합니다.

#### 목차

1.  2바이트 [Integer](/docs/specs/common-structures/#integer)

#### 참고사항

세션 ID 0xffff는 "세션 없음"을 나타내는 데 사용되며, 예를 들어 호스트명 조회 시에 사용됩니다.

## 메시지

[I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)도 참조하세요.

### 메시지 유형 {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### 설명

클라이언트에게 대역폭 제한이 무엇인지 알려주세요.

[GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage)에 대한 응답으로 Router에서 Client로 전송됩니다.

#### 목차

1.  4 byte [Integer](/docs/specs/common-structures/#integer) 클라이언트 인바운드 제한
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) 클라이언트 아웃바운드 제한
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Router 인바운드 제한
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Router 인바운드 버스트 제한
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Router 아웃바운드 제한
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Router 아웃바운드 버스트
    제한 (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Router 버스트 시간
    (초)
8.  9개의 4-byte [Integer](/docs/specs/common-structures/#integer) (정의되지 않음)

#### 참고사항

클라이언트 제한은 설정된 유일한 값일 수 있으며, 실제 router 제한이거나 router 제한의 백분율이거나 특정 클라이언트에 특화된 값일 수 있습니다. 이는 구현에 따라 다릅니다. router 제한으로 표시된 모든 값들은 구현에 따라 0일 수 있습니다. 릴리즈 0.7.2 기준입니다.

### BlindingInfoMessage {#BlindingInfoMessage}

#### 설명

Destination이 blinded 상태임을 router에 알리며, 선택적으로 조회 비밀번호와 복호화를 위한 개인 키를 포함할 수 있습니다. 자세한 내용은 제안서 123 및 149를 참조하십시오.

router는 목적지가 블라인드되어 있는지 알아야 합니다. 만약 블라인드되어 있고 비밀 또는 클라이언트별 인증을 사용한다면, 해당 정보도 가지고 있어야 합니다.

새로운 형식의 b32 주소("b33")에 대한 Host Lookup은 router에게 해당 주소가 블라인드되어 있음을 알려주지만, Host Lookup 메시지에서 비밀 키나 개인 키를 router에 전달할 메커니즘이 없습니다. Host Lookup 메시지를 확장하여 해당 정보를 추가할 수도 있지만, 새로운 메시지를 정의하는 것이 더 깔끔합니다.

이 메시지는 클라이언트가 router에게 알려주는 프로그래밍 방식을 제공합니다. 그렇지 않으면 사용자가 각 목적지를 수동으로 구성해야 합니다.

#### 사용법

클라이언트가 blinded destination으로 메시지를 보내기 전에, Host Lookup 메시지에서 "b33"를 조회하거나 Blinding Info 메시지를 보내야 합니다. blinded destination이 비밀 정보나 클라이언트별 인증을 요구하는 경우, 클라이언트는 Blinding Info 메시지를 보내야 합니다.

router는 이 메시지에 대한 응답을 보내지 않습니다. Client에서 Router로 전송됩니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  1바이트 [Integer](/docs/specs/common-structures/#integer) 플래그

> - 비트 순서: 76543210 > - 비트 0: 모든 클라이언트는 0, 클라이언트별은 1 > - 비트 3-1: 인증 방식, 비트 0이 클라이언트별로 1로 설정된 경우, >   그렇지 않으면 000 >   - 000: DH 클라이언트 인증 (또는 클라이언트별 인증 없음) >   - 001: PSK 클라이언트 인증 > - 비트 4: 비밀 키가 필요하면 1, 비밀 키가 필요하지 않으면 0 > - 비트 7-5: 사용하지 않음, 향후 호환성을 위해 0으로 설정

3.  1바이트 [Integer](/docs/specs/common-structures/#integer) 엔드포인트 타입

> - Type 0은 [Hash](/docs/specs/common-structures/#hash)입니다 > - Type 1은 hostname [String](/docs/specs/common-structures/#string)입니다 > - Type 2는 [Destination](/docs/specs/common-structures/#destination)입니다 > - Type 3은 Sig Type과 >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)입니다

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 byte [Integer](/docs/specs/common-structures/#integer) 에포크 이후 만료 초
6.  Endpoint: 지정된 데이터, 다음 중 하나

> - 타입 0: 32바이트 [Hash](/docs/specs/common-structures/#hash) > > - 타입 1: 호스트 이름 [String](/docs/specs/common-structures/#string) > > - 타입 2: 바이너리 [Destination](/docs/specs/common-structures/#destination) > >  > >  - 타입 3: 2바이트 [Integer](/docs/specs/common-structures/#integer) 서명 타입, 그 뒤에 > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (서명 타입에 따른 >       길이)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) 복호화 키 플래그 비트 0이 1로 설정된 경우에만 존재합니다. 32바이트 ECIES_X25519 개인 키, 리틀 엔디안
8.  [String](/docs/specs/common-structures/#string) 조회 비밀번호 플래그 비트 4가 1로 설정된 경우에만 존재합니다.

#### 참고사항

- 릴리스 0.9.43 기준.
- Hash 엔드포인트 유형은 router가 주소록에서 역방향 조회를 수행하여 Destination을 얻을 수 있는 경우가 아니라면 유용하지 않을 것입니다.
- 호스트명 엔드포인트 유형은 router가 주소록에서 조회를 수행하여 Destination을 얻을 수 있는 경우가 아니라면 유용하지 않을 것입니다.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

더 이상 사용되지 않습니다. LeaseSet2, 오프라인 키, 비ElGamal 암호화 유형, 다중 암호화 유형 또는 암호화된 LeaseSet에는 사용할 수 없습니다. 0.9.39 이상의 모든 router에서 CreateLeaseSet2Message를 사용하세요.

#### 설명

이 메시지는 [RequestLeaseSetMessage](#RequestLeaseSetMessage) 또는 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage)에 대한 응답으로 전송되며, I2NP Network Database에 게시되어야 하는 모든 [Lease](/docs/specs/common-structures/#lease) 구조를 포함합니다.

클라이언트에서 router로 전송됨.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) 또는 20바이트 무시됨
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### 참고사항

SigningPrivateKey는 signing key 유형이 DSA인 경우에만 LeaseSet 내의 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)와 일치합니다. 이는 LeaseSet 취소를 위한 것으로, 구현되지 않았으며 향후 구현될 가능성도 낮습니다. signing key 유형이 DSA가 아닌 경우, 이 필드는 20바이트의 랜덤 데이터를 포함합니다. 이 필드의 길이는 항상 20바이트이며, DSA가 아닌 signing private key의 길이와 같아지는 경우는 없습니다.

PrivateKey는 LeaseSet의 [PublicKey](/docs/specs/common-structures/#publickey)와 일치합니다. PrivateKey는 garlic 라우팅된 메시지를 복호화하는 데 필요합니다.

해지(Revocation)는 구현되지 않았습니다. 여러 router에 대한 연결은 어떤 클라이언트 라이브러리에서도 구현되지 않았습니다.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### 설명

이 메시지는 [RequestLeaseSetMessage](#RequestLeaseSetMessage) 또는 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage)에 대한 응답으로 전송되며, I2NP Network Database에 게시되어야 하는 모든 [Lease](/docs/specs/common-structures/#lease) 구조체들을 포함합니다.

클라이언트에서 라우터로 전송됩니다. 릴리스 0.9.39부터 지원됩니다. EncryptedLeaseSet에 대한 클라이언트별 인증은 0.9.41부터 지원됩니다. MetaLeaseSet은 아직 I2CP를 통해 지원되지 않습니다. 자세한 정보는 제안서 123을 참조하세요.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  뒤따를 leaseSet 타입의 1바이트.

> - Type 1은 [LeaseSet](/docs/specs/common-structures/#leaseset) (deprecated) > - Type 3은 [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Type 5는 [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Type 7은 [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) 또는
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) 또는
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) 또는
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  뒤따를 개인키 개수를 나타내는 1바이트 숫자.
5.  [PrivateKey](/docs/specs/common-structures/#privatekey) 목록. lease set의 각 공개키에 대해 하나씩, 동일한 순서로. (Meta LS2에는 없음)

> - 암호화 타입 (2바이트 [Integer](/docs/specs/common-structures/#integer)) > - 암호화 키 길이 (2바이트 [Integer](/docs/specs/common-structures/#integer)) > - 암호화 [PrivateKey](/docs/specs/common-structures/#privatekey) (지정된 바이트 수)

#### 참고사항

PrivateKeys는 LeaseSet의 각 [PublicKey](/docs/specs/common-structures/#publickey)와 일치합니다. PrivateKeys는 garlic 라우팅된 메시지를 복호화하는 데 필요합니다.

Encrypted LeaseSet에 대한 자세한 정보는 제안서 123을 참조하세요.

MetaLeaseSet의 내용과 형식은 예비적이며 변경될 수 있습니다. 여러 router의 관리에 대한 프로토콜은 지정되어 있지 않습니다. 자세한 정보는 제안서 123을 참조하십시오.

이전에 취소용으로 정의되었지만 사용되지 않은 서명 개인 키는 LS2에 존재하지 않습니다.

메시지 타입 40을 사용한 예비 버전이 0.9.38에 있었지만 형식이 변경되었습니다. 타입 40은 폐기되었으며 지원되지 않습니다. 타입 41은 0.9.39까지 유효하지 않습니다.

### CreateSessionMessage {#CreateSessionMessage}

#### 설명

이 메시지는 클라이언트에서 세션을 시작하기 위해 전송되며, 여기서 세션은 단일 Destination의 네트워크 연결로 정의됩니다. 해당 Destination에 대한 모든 메시지가 전달되고, 해당 Destination이 다른 모든 Destination으로 보내는 모든 메시지가 이를 통해 전송됩니다.

클라이언트에서 라우터로 전송됩니다. 라우터는 [SessionStatusMessage](#SessionStatusMessage)로 응답합니다.

#### 목차

1.  [세션 구성](#struct-sessionconfig)

#### 참고사항

- 이것은 클라이언트가 보내는 두 번째 메시지입니다. 이전에 클라이언트는
  [GetDateMessage](#GetDateMessage)를 보내고
  [SetDateMessage](#SetDateMessage) 응답을 받았습니다.
- Session Config의 Date가 router의 현재 시간과 너무 차이가 날 경우 (+/- 30초 초과), 
  세션은 거부됩니다.
- 이 Destination에 대해 router에 이미 세션이 있는 경우, 
  세션은 거부됩니다.
- Session Config의 [Mapping](/docs/specs/common-structures/#mapping)은 
  router에서 서명이 올바르게 검증될 수 있도록 키로 정렬되어야 합니다.

### DestLookupMessage {#DestLookupMessage}

#### 설명

클라이언트에서 router로 전송됩니다. router는 [DestReplyMessage](#DestReplyMessage)로 응답합니다.

#### 목차

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### 참고사항

릴리스 0.7 기준.

릴리스 0.8.3부터 여러 개의 미해결 조회가 지원되며, I2PSimpleSession과 표준 세션 모두에서 조회가 지원됩니다.

[HostLookupMessage](#HostLookupMessage)는 0.9.11 릴리스부터 권장됩니다.

### DestReplyMessage {#DestReplyMessage}

#### 설명

[DestLookupMessage](#DestLookupMessage)에 대한 응답으로 Router에서 Client로 전송됩니다.

#### 목차

1.  성공 시 [Destination](/docs/specs/common-structures/#destination), 또는
    실패 시 [Hash](/docs/specs/common-structures/#hash)

#### 참고사항

릴리스 0.7 기준.

릴리스 0.8.3부터는 조회가 실패한 경우에도 요청된 Hash가 반환되므로, 클라이언트가 여러 조회를 진행 중일 때 응답과 조회를 연관시킬 수 있습니다. Destination 응답을 요청과 연관시키려면 Destination의 Hash를 사용하세요. 릴리스 0.8.3 이전에는 실패 시 응답이 비어있었습니다.

### DestroySessionMessage {#DestroySessionMessage}

#### 설명

이 메시지는 세션을 종료하기 위해 클라이언트에서 전송됩니다.

클라이언트에서 router로 전송됩니다. router는 [SessionStatusMessage](#SessionStatusMessage) (Destroyed)로 응답해야 합니다. 그러나 아래의 중요한 참고사항을 확인하세요.

#### 목차

1.  [세션 ID](#struct-sessionid)

#### 참고사항

이 시점에서 router는 세션과 관련된 모든 리소스를 해제해야 합니다.

API 0.9.66을 통해, Java I2P router와 클라이언트 라이브러리는 이 명세서에서 상당히 벗어납니다. router는 SessionStatus(Destroyed) 응답을 절대 보내지 않습니다. 남은 세션이 없으면 [DisconnectMessage](#DisconnectMessage)를 보냅니다. 하위 세션이나 기본 세션이 남아있으면 응답하지 않습니다.

Java 클라이언트 라이브러리는 SessionStatus 메시지에 대해 모든 세션을 종료하고 재연결하는 방식으로 응답합니다.

여러 세션이 있는 연결에서 개별 하위 세션을 삭제하는 것은 다양한 router 및 클라이언트 구현에서 완전히 테스트되지 않았거나 작동하지 않을 수 있습니다. 주의하여 사용하세요.

구현체들은 primary session에 대한 destroy를 모든 subsession에 대한 destroy로 처리해야 하지만, 단일 subsession에 대한 destroy는 허용하고 연결을 열린 상태로 유지해야 합니다. 하지만 Java I2P는 현재 그렇게 하지 않습니다. Java I2P의 동작이 후속 릴리스에서 변경되면 여기에 문서화될 것입니다.

### DisconnectMessage {#DisconnectMessage}

#### 설명

다른 쪽에 문제가 있으며 현재 연결이 곧 종료될 것임을 알립니다. 이는 해당 연결의 모든 세션을 종료합니다. 소켓은 곧 닫힐 것입니다. router에서 클라이언트로 또는 클라이언트에서 router로 전송됩니다.

#### 목차

1.  이유 [String](/docs/specs/common-structures/#string)

#### 참고사항

적어도 Java I2P에서는 router에서 클라이언트 방향으로만 구현되어 있습니다.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### 설명

router가 현재 대역폭 제한이 무엇인지 상태를 요청합니다.

클라이언트에서 router로 전송됩니다. router는 [BandwidthLimitsMessage](#BandwidthLimitsMessage)로 응답합니다.

#### 목차

*없음*

#### 참고사항

릴리스 0.7.2 기준.

릴리스 0.8.3부터 I2PSimpleSession과 표준 세션 모두에서 지원됩니다.

### GetDateMessage {#GetDateMessage}

#### 설명

클라이언트에서 router로 전송됩니다. router는 [SetDateMessage](#SetDateMessage)로 응답합니다.

#### 목차

1.  I2CP API 버전 [String](/docs/specs/common-structures/#string)
2.  인증 [Mapping](/docs/specs/common-structures/#mapping) (선택사항, 릴리스 0.9.11부터)

#### 노트

- 일반적으로 프로토콜 버전 바이트를 전송한 후 클라이언트가 보내는 첫 번째 메시지입니다.
- 버전 문자열은 릴리스 0.8.7부터 포함됩니다. 이는 클라이언트와 router가 같은 JVM에 있지 않은 경우에만 유용합니다. 버전 문자열이 없다면, 클라이언트는 버전 0.8.6 이하입니다.
- 릴리스 0.9.11부터 인증 [Mapping](/docs/specs/common-structures/#mapping)이 i2cp.username 및 i2cp.password 키와 함께 포함될 수 있습니다. 이 메시지는 서명되지 않으므로 Mapping을 정렬할 필요가 없습니다. 0.9.10 이전 및 포함하여, 인증은 [Session Config](#struct-sessionconfig) Mapping에 포함되며, [GetDateMessage](#GetDateMessage), [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), 또는 [DestLookupMessage](#DestLookupMessage)에 대해서는 인증이 강제되지 않습니다. 활성화된 경우, 릴리스 0.9.16부터 다른 모든 메시지보다 먼저 [GetDateMessage](#GetDateMessage)를 통한 인증이 필요합니다. 이는 router 컨텍스트 외부에서만 유용합니다. 이는 호환되지 않는 변경사항이지만, 인증이 있는 router 컨텍스트 외부의 세션에만 영향을 미치므로 드물 것입니다.

### HostLookupMessage {#HostLookupMessage}

#### 설명

클라이언트에서 router로 전송됩니다. router는 [HostReplyMessage](#HostReplyMessage)로 응답합니다.

이는 [DestLookupMessage](#DestLookupMessage)를 대체하고 요청 ID, 타임아웃, 호스트 이름 조회 지원을 추가합니다. Hash 조회도 지원하므로, router가 이를 지원한다면 모든 조회에 사용할 수 있습니다. 호스트 이름 조회의 경우, router는 자체 컨텍스트의 네이밍 서비스를 쿼리합니다. 이는 클라이언트가 router의 컨텍스트 외부에 있을 때만 유용합니다. router 컨텍스트 내부에서는 클라이언트가 네이밍 서비스를 직접 쿼리해야 하며, 이것이 훨씬 더 효율적입니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  4 바이트 [Integer](/docs/specs/common-structures/#integer) 요청 ID
3.  4 바이트 [Integer](/docs/specs/common-structures/#integer) 타임아웃 (ms)
4.  1 바이트 [Integer](/docs/specs/common-structures/#integer) 요청 타입
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) 또는 호스트명
    [String](/docs/specs/common-structures/#string) 또는
    [Destination](/docs/specs/common-structures/#destination)

요청 유형:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
타입 2-4는 LeaseSet의 옵션 매핑이 HostReply 메시지에서 반환되도록 요청합니다. 제안서 167을 참조하세요.

#### 참고사항

- 릴리스 0.9.11부터 적용됩니다. 이전 router에서는 [DestLookupMessage](#DestLookupMessage)를 사용하세요.
- 세션 ID와 요청 ID는 [HostReplyMessage](#HostReplyMessage)에서 반환됩니다. 세션이 없는 경우 세션 ID로 0xFFFF를 사용하세요.
- 타임아웃은 해시 조회에 유용합니다. 권장 최소값은 10,000 (10초)입니다. 향후 원격 이름 서비스 조회에도 유용할 수 있습니다. 이 값은 빠르게 처리되어야 하는 로컬 호스트 이름 조회에서는 적용되지 않을 수 있습니다.
- Base 32 호스트 이름 조회가 지원되지만 먼저 해시로 변환하는 것이 선호됩니다.

### HostReplyMessage {#HostReplyMessage}

#### 설명

[HostLookupMessage](#HostLookupMessage)에 대한 응답으로 Router에서 Client로 전송됩니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  4 바이트 [Integer](/docs/specs/common-structures/#integer) 요청 ID
3.  1 바이트 [Integer](/docs/specs/common-structures/#integer) 결과 코드

> - 0: 성공 > - 1: 실패 > - 2: 조회 비밀번호 필요 (0.9.43부터) > - 3: 개인키 필요 (0.9.43부터) > - 4: 조회 비밀번호 및 개인키 필요 (0.9.43부터) > - 5: leaseSet 복호화 실패 (0.9.43부터) > - 6: leaseSet 조회 실패 (0.9.66부터) > - 7: 조회 유형 지원되지 않음 (0.9.66부터)

4.  [Destination](/docs/specs/common-structures/#destination), 결과 코드가 0일 때만 존재하며, 조회 타입 2-4에서도 반환될 수 있습니다. 아래를 참조하세요.
5.  [Mapping](/docs/specs/common-structures/#mapping), 결과 코드가 0일 때만 존재하며, 조회 타입 2-4에서만 반환됩니다. 0.9.66부터 적용. 아래를 참조하세요.

#### 조회 유형 2-4에 대한 응답

Proposal 167은 leaseset에서 모든 옵션을 반환하는 추가 조회 유형을 정의합니다(존재하는 경우). 조회 유형 2-4의 경우, 조회 키가 주소록에 있더라도 router는 leaseset을 가져와야 합니다.

성공하면 HostReply는 leaseset의 옵션 Mapping을 포함하며, 목적지 이후 항목 5로 포함됩니다. Mapping에 옵션이 없거나 leaseset이 버전 1인 경우에도 빈 Mapping(2바이트: 0 0)으로 포함됩니다. 서비스 레코드 옵션뿐만 아니라 leaseset의 모든 옵션이 포함됩니다. 예를 들어, 향후 정의될 매개변수에 대한 옵션도 존재할 수 있습니다. 반환되는 Mapping은 구현에 따라 정렬되거나 정렬되지 않을 수 있습니다.

leaseSet 조회 실패 시, 응답에는 새로운 오류 코드 6(leaseSet 조회 실패)이 포함되며 매핑은 포함되지 않습니다. 오류 코드 6이 반환될 때, Destination 필드는 있을 수도 있고 없을 수도 있습니다. 주소록에서 호스트명 조회가 성공했거나, 이전 조회가 성공하여 결과가 캐시되었거나, 조회 메시지에 Destination이 포함되어 있었던 경우(조회 유형 4)에는 Destination 필드가 존재할 것입니다.

조회 유형이 지원되지 않는 경우, 응답에는 새로운 오류 코드 7 (조회 유형 지원되지 않음)이 포함됩니다.

#### 주의사항

- 릴리즈 0.9.11부터 적용. [HostLookupMessage](#HostLookupMessage) 참고사항을 확인하세요.
- 세션 ID와 요청 ID는 [HostLookupMessage](#HostLookupMessage)의 것과 동일합니다.
- 결과 코드는 성공 시 0, 실패 시 1-255입니다. 1은 일반적인 실패를 나타냅니다. 0.9.43부터 "b33" 조회에 대한 확장 오류를 지원하기 위해 추가 실패 코드 2-5가 정의되었습니다. 자세한 내용은 제안서 123과 149를 참조하세요. 0.9.66부터 타입 2-4 조회에 대한 확장 오류를 지원하기 위해 추가 실패 코드 6-7이 정의되었습니다. 자세한 내용은 제안서 167을 참조하세요.

### MessagePayloadMessage {#MessagePayloadMessage}

#### 설명

메시지의 페이로드를 클라이언트에 전달합니다.

Router에서 Client로 전송됩니다. i2cp.fastReceive=true인 경우(기본값이 아님), 클라이언트는 [ReceiveMessageEndMessage](#ReceiveMessageEndMessage)로 응답합니다.

#### 목차

1.  [세션 ID](#struct-sessionid)
2.  [메시지 ID](#struct-messageid)
3.  [페이로드](#struct-payload)

#### 노트

### MessageStatusMessage {#MessageStatusMessage}

#### 설명

들어오거나 나가는 메시지의 전달 상태를 클라이언트에게 알립니다. Router에서 Client로 전송됩니다. 이 메시지가 들어오는 메시지가 사용 가능함을 나타내는 경우, 클라이언트는 [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage)로 응답합니다. 나가는 메시지의 경우, 이는 [SendMessageMessage](#SendMessageMessage) 또는 [SendMessageExpiresMessage](#SendMessageExpiresMessage)에 대한 응답입니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  router가 생성한 [Message ID](#struct-messageid)
3.  1바이트 [Integer](/docs/specs/common-structures/#integer) 상태
4.  4바이트 [Integer](/docs/specs/common-structures/#integer) 크기
5.  클라이언트가 이전에 생성한 4바이트 [Integer](/docs/specs/common-structures/#integer) nonce

#### 참고사항

버전 0.9.4까지 알려진 상태 값은 0은 메시지 사용 가능, 1은 수락됨, 2는 최선 노력 성공, 3은 최선 노력 실패, 4는 보장됨 성공, 5는 보장됨 실패입니다. 크기 Integer는 사용 가능한 메시지의 크기를 지정하며 status = 0일 때만 관련이 있습니다. 보장됨이 구현되지 않았음에도 불구하고 (최선 노력이 유일한 서비스), 현재 router 구현에서는 최선 노력 코드가 아닌 보장됨 상태 코드를 사용합니다.

router 버전 0.9.5부터 추가 상태 코드가 정의되었지만, 반드시 구현된 것은 아닙니다. 자세한 내용은 [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)를 참조하세요. 발신 메시지의 경우 코드 1, 2, 4, 6은 성공을 나타내며, 그 외의 모든 코드는 실패를 의미합니다. 반환되는 실패 코드는 다를 수 있으며 구현에 따라 다릅니다.

모든 상태 코드:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
status = 1 (승인됨)일 때, nonce는 [SendMessageMessage](#SendMessageMessage)의 nonce와 일치하며, 포함된 Message ID는 후속 성공 또는 실패 알림에 사용됩니다. 그렇지 않으면 nonce는 무시될 수 있습니다.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

사용 중단됨. i2pd에서 지원되지 않음.

#### 설명

router가 이전에 통지받은 메시지를 전달하도록 요청합니다. Client에서 Router로 전송됩니다. router는 [MessagePayloadMessage](#MessagePayloadMessage)로 응답합니다.

#### 목차

1.  [세션 ID](#struct-sessionid)
2.  [메시지 ID](#struct-messageid)

#### 참고 사항

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage)는 새로운 메시지가 수신 가능하다는 [MessageStatusMessage](#MessageStatusMessage)에 대한 응답으로 전송됩니다. [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage)에 지정된 메시지 ID가 유효하지 않거나 올바르지 않은 경우, router는 단순히 응답하지 않거나 [DisconnectMessage](#DisconnectMessage)를 다시 보낼 수 있습니다.

이는 릴리스 0.9.4부터 기본값인 "fast receive" 모드에서는 사용되지 않습니다.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

더 이상 사용되지 않음. i2pd에서 지원되지 않음.

#### 설명

메시지가 성공적으로 전달되었으며 router가 메시지를 폐기할 수 있음을 알립니다.

클라이언트에서 Router로 전송됨.

#### 목차

1.  [세션 ID](#struct-sessionid)
2.  [메시지 ID](#struct-messageid)

#### 참고사항

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage)는 [MessagePayloadMessage](#MessagePayloadMessage)가 메시지의 페이로드를 완전히 전달한 후에 전송됩니다.

이는 릴리스 0.9.4부터 기본값인 "fast receive" 모드에서는 사용되지 않습니다.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### 설명

클라이언트에서 router로 전송되어 세션 구성을 업데이트합니다. router는 [SessionStatusMessage](#SessionStatusMessage)로 응답합니다.

#### 목차

1.  [세션 ID](#struct-sessionid)
2.  [세션 구성](#struct-sessionconfig)

#### 주의사항

- 릴리스 0.7.1 기준입니다.
- Session Config의 Date가 router의 현재 시간과 너무 많이 차이날 경우 (+/- 30초 초과), 세션이 거부됩니다.
- Session Config의 [Mapping](/docs/specs/common-structures/#mapping)은 키별로 정렬되어야 router에서 서명이 올바르게 검증됩니다.
- 일부 구성 옵션은 [CreateSessionMessage](#CreateSessionMessage)에서만 설정할 수 있으며, 여기서의 변경 사항은 router에서 인식되지 않습니다. tunnel 옵션 inbound.\* 및 outbound.\*에 대한 변경 사항은 항상 인식됩니다.
- 일반적으로 router는 업데이트된 구성을 현재 구성과 병합해야 하므로, 업데이트된 구성에는 새로운 옵션이나 변경된 옵션만 포함하면 됩니다. 하지만 병합으로 인해 이 방식으로는 옵션을 제거할 수 없으며, 원하는 기본값으로 명시적으로 설정해야 합니다.

### ReportAbuseMessage {#ReportAbuseMessage}

사용 중단됨, 사용되지 않음, 지원되지 않음

#### 설명

상대방(클라이언트 또는 router)에게 공격을 받고 있음을 알리며, 특정 MessageId를 참조할 수 있습니다. router가 공격을 받고 있다면 클라이언트는 다른 router로 이전하기로 결정할 수 있고, 클라이언트가 공격을 받고 있다면 router는 자신의 router들을 재구축하거나 공격 메시지를 전달한 일부 피어들을 차단 목록에 추가할 수 있습니다.

router에서 클라이언트로 또는 클라이언트에서 router로 전송됩니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  1 바이트 [Integer](/docs/specs/common-structures/#integer) 남용 심각도 (0은 최소 남용, 255는 극도로 남용)
3.  이유 [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### 참고사항

사용되지 않음. 완전히 구현되지 않았음. router와 클라이언트 모두 [ReportAbuseMessage](#ReportAbuseMessage)를 생성할 수 있지만, 메시지를 수신했을 때 이를 처리하는 핸들러가 없음.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

더 이상 사용되지 않습니다. i2pd에서 지원되지 않습니다. Java I2P에서 버전 0.9.7 이상의 클라이언트에게는 전송되지 않습니다 (2013-07). RequestVariableLeaseSetMessage를 사용하세요.

#### 설명

클라이언트에게 특정 inbound tunnel 집합의 포함을 승인하도록 요청합니다. Router에서 Client로 전송됩니다. 클라이언트는 [CreateLeaseSetMessage](#CreateLeaseSetMessage)로 응답합니다.

세션에서 전송되는 이러한 메시지 중 첫 번째는 tunnel이 구축되어 트래픽을 처리할 준비가 되었다는 신호를 클라이언트에 보내는 것입니다. router는 최소한 하나의 인바운드 tunnel과 하나의 아웃바운드 tunnel이 구축될 때까지 이 첫 번째 메시지를 보내서는 안 됩니다. 클라이언트는 일정 시간이 지나도 첫 번째 메시지를 받지 못하면 타임아웃하고 세션을 종료해야 합니다 (권장: 5분 이상).

#### 목차

1.  [Session ID](#struct-sessionid)
2.  1 바이트 [Integer](/docs/specs/common-structures/#integer) tunnel 수
3.  다음 쌍들을 그 수만큼:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  종료 [Date](/docs/specs/common-structures/#date)

#### 참고사항

이는 모든 [Lease](/docs/specs/common-structures/#lease) 항목이 동시에 만료되도록 설정된 [LeaseSet](/docs/specs/common-structures/#leaseset)을 요청합니다. 클라이언트 버전 0.9.7 이상의 경우 [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage)가 사용됩니다.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### 설명

클라이언트가 특정 인바운드 터널 세트의 포함을 승인하도록 요청합니다.

Router에서 Client로 전송됩니다. 클라이언트는 [CreateLeaseSetMessage](#CreateLeaseSetMessage) 또는 [CreateLeaseSet2Message](#CreateLeaseSet2Message)로 응답합니다.

세션에서 전송되는 이러한 메시지 중 첫 번째는 tunnel이 구축되어 트래픽을 처리할 준비가 되었다는 신호를 클라이언트에게 보내는 것입니다. router는 최소한 하나의 인바운드 tunnel과 하나의 아웃바운드 tunnel이 구축될 때까지 이러한 메시지 중 첫 번째를 보내서는 안 됩니다. 클라이언트는 일정 시간 후에도 이러한 메시지 중 첫 번째를 받지 못하면 타임아웃하고 세션을 종료해야 합니다 (권장: 5분 이상).

#### 목차

1.  [Session ID](#struct-sessionid)
2.  1바이트 [Integer](/docs/specs/common-structures/#integer) tunnel 수
3.  그만큼의 [Lease](/docs/specs/common-structures/#lease) 항목들

#### 참고 사항

이는 각 [Lease](/docs/specs/common-structures/#lease)에 대해 개별 만료 시간을 가진 [LeaseSet](/docs/specs/common-structures/#leaseset)을 요청합니다.

릴리즈 0.9.7부터 적용됩니다. 해당 릴리즈 이전의 클라이언트는 [RequestLeaseSetMessage](#RequestLeaseSetMessage)를 사용하세요.

### SendMessageMessage {#SendMessageMessage}

#### 설명

클라이언트가 [Destination](/docs/specs/common-structures/#destination)에 메시지(페이로드)를 보내는 방법입니다. router는 기본 만료 시간을 사용합니다.

클라이언트에서 router로 전송됩니다. router는 [MessageStatusMessage](#MessageStatusMessage)로 응답합니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4바이트 [Integer](/docs/specs/common-structures/#integer) nonce

#### 참고사항

[SendMessageMessage](#SendMessageMessage)가 완전히 온전하게 도착하자마자, router는 전송을 위해 수락되었다는 [MessageStatusMessage](#MessageStatusMessage)를 반환해야 합니다. 해당 메시지는 여기서 전송된 것과 동일한 nonce를 포함할 것입니다. 나중에 세션 구성의 전송 보장에 따라, router는 상태를 업데이트하는 추가적인 [MessageStatusMessage](#MessageStatusMessage)를 다시 전송할 수도 있습니다.

릴리스 0.8.1부터 router는 i2cp.messageReliability=none인 경우 [MessageStatusMessage](#MessageStatusMessage)를 전송하지 않습니다.

릴리스 0.9.4 이전에는 nonce 값 0이 허용되지 않았습니다. 릴리스 0.9.4부터는 nonce 값 0이 허용되며, 이는 router에게 [MessageStatusMessage](#MessageStatusMessage)를 전송하지 말라고 지시합니다. 즉, 해당 메시지에 대해서만 i2cp.messageReliability=none으로 작동하는 것과 같습니다.

릴리스 0.9.14 이전에는 i2cp.messageReliability=none으로 설정된 세션에서 메시지별로 이를 재정의할 수 없었습니다. 릴리스 0.9.14부터는 i2cp.messageReliability=none으로 설정된 세션에서 클라이언트가 nonce를 0이 아닌 값으로 설정하여 배송 성공 또는 실패에 대한 [MessageStatusMessage](#MessageStatusMessage) 전달을 요청할 수 있습니다. router는 "accepted" [MessageStatusMessage](#MessageStatusMessage)는 보내지 않지만, 나중에 동일한 nonce와 성공 또는 실패 값을 포함한 [MessageStatusMessage](#MessageStatusMessage)를 클라이언트에게 보냅니다.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### 설명

클라이언트에서 router로 전송됩니다. [SendMessageMessage](#SendMessageMessage)와 동일하지만 만료 시간과 옵션이 포함됩니다.

#### 목차

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4바이트 [Integer](/docs/specs/common-structures/#integer) nonce
5.  2바이트 플래그 (옵션)
6.  만료 [Date](/docs/specs/common-structures/#date) (8바이트에서 6바이트로 단축)

#### 참고 사항

릴리스 0.7.1 기준.

"최선 노력" 모드에서는 SendMessageExpiresMessage가 완전히 온전하게 도착하자마자 router가 배송을 위해 수락되었다는 MessageStatusMessage를 반환해야 합니다. 해당 메시지에는 여기서 보낸 것과 동일한 nonce가 포함됩니다. 나중에 세션 구성의 배송 보장에 따라 router는 상태를 업데이트하는 또 다른 MessageStatusMessage를 추가로 다시 보낼 수 있습니다.

릴리스 0.8.1부터, router는 i2cp.messageReliability=none인 경우 Message Status Message를 전송하지 않습니다.

릴리스 0.9.4 이전에는 nonce 값이 0인 것이 허용되지 않았습니다. 릴리스 0.9.4부터는 nonce 값이 0인 것이 허용되며, 이는 router에게 Message Status Message를 전송하지 말라고 지시합니다. 즉, 해당 메시지에 대해서만 i2cp.messageReliability=none으로 설정된 것처럼 동작합니다.

릴리스 0.9.14 이전에는 i2cp.messageReliability=none으로 설정된 세션에서 메시지별로 이를 재정의할 수 없었습니다. 릴리스 0.9.14부터는 i2cp.messageReliability=none으로 설정된 세션에서 클라이언트가 nonce를 0이 아닌 값으로 설정하여 전송 성공 또는 실패에 대한 Message Status Message 전달을 요청할 수 있습니다. router는 "accepted" Message Status Message를 보내지 않지만, 나중에 동일한 nonce와 성공 또는 실패 값을 포함한 Message Status Message를 클라이언트에게 보냅니다.

#### 플래그 필드

릴리스 0.8.4부터 Date의 상위 2바이트는 플래그를 포함하도록 재정의되었습니다. 플래그는 하위 호환성을 위해 기본적으로 모두 0이어야 합니다. Date는 10889년까지 플래그 필드를 침범하지 않습니다. 플래그는 애플리케이션에서 LeaseSet 및/또는 ElGamal/AES Session Tags가 메시지와 함께 전달되어야 하는지에 대한 힌트를 router에 제공하는 데 사용할 수 있습니다. 이 설정은 프로토콜 오버헤드의 양과 메시지 전달의 신뢰성에 크게 영향을 미칩니다. 개별 플래그 비트는 릴리스 0.9.2부터 다음과 같이 정의됩니다. 정의는 변경될 수 있습니다. 플래그를 구성하려면 SendMessageOptions 클래스를 사용하십시오.

비트 순서: 15...0

비트 15-11

:   사용되지 않음, 반드시 0이어야 함

비트 10-9

:   메시지 신뢰성 오버라이드 (구현되지 않음, 제거 예정).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
비트 8

:   1이면, 이 메시지와 함께 garlic에 leaseSet을 묶지 않습니다. 만약

    0, the router may bundle a lease set at its discretion.

비트 7-4

:   낮은 태그 임계값. 사용 가능한 태그가 이 수보다 적으면,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
비트 3-0

:   필요한 경우 전송할 태그 수입니다. 이는 권고사항이며 강제사항이 아닙니다

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### 설명

클라이언트에게 세션 상태를 알려줍니다.

Router에서 Client로 전송되며, [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), 또는 [DestroySessionMessage](#DestroySessionMessage)에 대한 응답입니다. [CreateSessionMessage](#CreateSessionMessage)에 대한 응답을 포함하여 모든 경우에, router는 즉시 응답해야 합니다 (tunnel이 구축될 때까지 기다리지 마세요).

#### 목차

1.  [Session ID](#struct-sessionid)
2.  1 바이트 [Integer](/docs/specs/common-structures/#integer) 상태

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### 참고 사항

상태 값은 위에서 정의됩니다. 상태가 Created인 경우, Session ID는 나머지 세션에서 사용될 식별자입니다.

### SetDateMessage {#SetDateMessage}

#### 설명

현재 날짜와 시간. 초기 핸드셰이크의 일부로 Router에서 Client로 전송됩니다. 릴리스 0.9.20부터는 핸드셰이크 이후 언제든지 클라이언트에게 시계 변화를 알리기 위해 전송될 수도 있습니다.

#### 목차

1.  [Date](/docs/specs/common-structures/#date)
2.  I2CP API 버전 [String](/docs/specs/common-structures/#string)

#### 참고사항

이것은 일반적으로 router가 보내는 첫 번째 메시지입니다. 버전 문자열은 릴리스 0.8.7부터 포함되었습니다. 이는 클라이언트와 router가 동일한 JVM에 있지 않은 경우에만 유용합니다. 존재하지 않는다면, router는 버전 0.8.6 또는 이전 버전입니다.

동일한 JVM의 클라이언트에게는 추가 SetDate 메시지가 전송되지 않습니다.

## 참고 자료

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [I2CP 개요](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
