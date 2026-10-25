---
title: "SSU (Secure Semireliable UDP)"
description: "원래 UDP 전송 프로토콜 사양 (사용 중단됨, SSU2로 대체됨)"
slug: "ssu"
aliases:
  - "/ko/docs/transport/ssu"
  - "/ko/docs/transport/ssu/"
  - "/ko/docs/transports/ssu"
  - "/ko/docs/transports/ssu/"
  - "/ko/docs/specs/ssu-spec"
  - "/ko/docs/specs/ssu-spec/"
  - "/ko/udp_spec"
  - "/ko/udp_spec/"
category: "전송 계층"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## 개요

사용 중단됨 - SSU가 SSU2로 교체되었습니다. SSU 지원은 i2pd 릴리스 2.44.0 (API 0.9.56) 2022-11에서 제거되었습니다. SSU 지원은 Java I2P 릴리스 2.4.0 (API 0.9.61) 2023-12에서 제거되었습니다.

자세한 정보는 [SSU 개요](/docs/transport/ssu/)를 참조하세요.

## DH 키 교환 {#dh}

초기 2048비트 DH 키 교환은 [SSU Keys 페이지](/docs/transport/ssu/#keys)에 설명되어 있습니다. 이 교환은 I2P의 [ElGamal 암호화](/docs/specs/cryptography/#elgamal)에서 사용되는 것과 동일한 공유 소수를 사용합니다.

## 메시지 헤더 {#header}

모든 UDP 데이터그램은 16바이트 MAC(Message Authentication Code)와 16바이트 IV(Initialization Vector)로 시작하며, 그 뒤에 적절한 키로 암호화된 가변 크기 페이로드가 따라옵니다. 사용되는 MAC은 16바이트로 절단된 HMAC-MD5이며, 키는 전체 32바이트 AES256 키입니다. MAC의 구체적인 구조는 다음에서 처음 16바이트입니다:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
여기서 '+'는 추가를 의미하고 '^'는 배타적 논리합을 의미합니다.

IV는 각 패킷마다 무작위로 생성됩니다. encryptedPayload는 플래그 바이트부터 시작하는 메시지의 암호화된 버전입니다 (encrypt-then-MAC). MAC에서 사용되는 payloadLength는 2바이트 부호 없는 정수이며, 빅 엔디안입니다. protocolVersion이 0이므로 배타적 논리합(exclusive-or)은 아무 작업도 하지 않습니다. macKey는 introduction key이거나 교환된 DH 키로부터 구성되며 (아래 세부사항 참조), 각 메시지에 대해 아래에 명시된 대로 지정됩니다.

**경고** - 여기서 사용된 HMAC-MD5-128은 비표준이므로, 자세한 정보는 [HMAC 세부사항](/docs/specs/cryptography/#udp)을 참조하세요.

페이로드 자체(즉, 플래그 바이트로 시작하는 메시지)는 IV와 sessionKey를 사용하여 AES256/CBC로 암호화되며, 재전송 공격 방지는 본문 내에서 처리되며 아래에서 설명됩니다.

protocolVersion은 2바이트 부호 없는 정수이며, 빅 엔디안 방식으로 현재 0으로 설정되어 있습니다. 다른 프로토콜 버전을 사용하는 peer들은 이 peer와 통신할 수 없지만, 이 플래그를 사용하지 않는 이전 버전들은 통신이 가능합니다.

((netid - 2) << 8)의 배타적 OR은 네트워크 간 연결을 빠르게 식별하는 데 사용됩니다. netid는 2바이트 부호 없는 정수이며, 빅 엔디안 방식이고, 현재 2로 설정되어 있습니다. 0.9.42 버전부터입니다. 자세한 정보는 제안서 147을 참조하세요. 현재 네트워크 ID가 2이므로, 이는 현재 네트워크에서는 no-op이며 하위 호환성이 있습니다. 테스트 네트워크로부터의 연결은 다른 ID를 가져야 하며 HMAC 검증에 실패할 것입니다.

### HMAC 사양

- Inner padding: 0x36...
- Outer padding: 0x5C...
- Key: 32바이트
- Hash digest function: MD5, 16바이트
- Block size: 64바이트
- MAC size: 16바이트
- C 구현 예시:
  - [i2pd](https://github.com/PurpleI2P/i2pd)의 hmac.h
  - [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)의 I2PHMAC.cpp
- Java 구현 예시:
  - [I2P](https://github.com/i2p/i2p.i2p)의 I2PHMac.java

### 세션 키 세부사항

32바이트 세션 키는 다음과 같이 생성됩니다:

1. 교환된 DH 키를 양수 최소 길이 BigInteger 바이트 배열(2의 보수 빅 엔디안)로 나타냅니다
2. 최상위 비트가 1인 경우(즉, array[0] & 0x80 != 0), Java의 BigInteger.toByteArray() 표현과 같이 0x00 바이트를 앞에 추가합니다
3. 바이트 배열이 32바이트 이상인 경우, 첫 번째(최상위) 32바이트를 사용합니다
4. 바이트 배열이 32바이트 미만인 경우, 0x00 바이트를 추가하여 32바이트로 확장합니다. *매우 가능성이 낮음 - 아래 참고사항 참조.*

### MAC 키 세부사항

32바이트 MAC 키는 다음과 같이 생성됩니다:

1. 위의 세션 키 세부사항 2단계에서 교환된 DH 키 바이트 배열을 가져옵니다. 필요한 경우 0x00 바이트를 앞에 붙입니다.
2. 해당 바이트 배열이 64바이트 이상인 경우, MAC 키는 해당 바이트 배열의 33-64바이트입니다.
3. 해당 바이트 배열이 64바이트 미만인 경우, MAC 키는 해당 바이트 배열의 SHA-256 해시입니다. *릴리즈 0.9.8부터. 아래 참고사항 참조.*

#### 중요 사항

릴리스 0.9.8 이전의 코드는 손상되어 32바이트와 63바이트 사이의 DH 키 바이트 배열을 올바르게 처리하지 못했으며(위의 3단계와 4단계), 연결이 실패했습니다. 이러한 경우들은 전혀 작동하지 않았기 때문에 릴리스 0.9.8에서 위에서 설명한 대로 재정의되었고, 0-32바이트 경우도 마찬가지로 재정의되었습니다. 명목상 교환되는 DH 키가 256바이트이므로, 최소 표현이 64바이트 미만일 가능성은 극히 작습니다.

### 헤더 형식

AES 암호화된 페이로드 내에서 다양한 메시지들에는 최소한의 공통 구조가 있습니다 - 1바이트 플래그와 4바이트 전송 타임스탬프(유닉스 에포크 이후 초 단위)입니다.

헤더 형식은 다음과 같습니다:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
플래그 바이트는 다음과 같은 비트 필드를 포함합니다:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
rekeying과 확장 옵션 없이는 헤더 크기가 37바이트입니다.

### 키 재생성 {#rekey}

rekey 플래그가 설정된 경우, 타임스탬프 다음에 64바이트의 키 자료가 따라옵니다.

rekeying 시, 키 자료의 첫 32바이트는 SHA256에 입력되어 새로운 MAC 키를 생성하고, 다음 32바이트는 SHA256에 입력되어 새로운 세션 키를 생성하지만, 키들은 즉시 사용되지 않습니다. 상대방도 rekey 플래그를 설정하고 동일한 키 자료로 응답해야 합니다. 양쪽 모두 해당 값들을 송수신한 후에는 새로운 키들을 사용하고 이전 키들을 폐기해야 합니다. 패킷 손실과 순서 변경 문제를 해결하기 위해 이전 키들을 잠시 보관하는 것이 유용할 수 있습니다.

참고: Rekeying은 현재 구현되지 않았습니다.

### 확장 옵션 {#extend}

확장 옵션 플래그가 설정되면, 1바이트 옵션 크기 값이 추가되고, 그 다음에 해당 수만큼의 확장 옵션 바이트가 따라옵니다. 확장 옵션은 항상 사양의 일부였지만, 0.9.24 릴리스까지 구현되지 않았습니다. 존재할 때, 옵션 형식은 메시지 유형에 따라 다릅니다. 주어진 메시지에 대해 확장 옵션이 예상되는지 여부와 지정된 형식에 대해서는 아래의 메시지 문서를 참조하세요. Java router는 항상 플래그와 옵션 길이를 인식했지만, 다른 구현체들은 그렇지 않습니다. 따라서 0.9.24 릴리스보다 오래된 router에는 확장 옵션을 보내지 마세요.

## 패딩

모든 메시지는 0개 이상의 패딩 바이트를 포함합니다. [AES256 암호화 계층](/docs/specs/cryptography/#AES)에서 요구하는 대로 각 메시지는 16바이트 경계로 패딩되어야 합니다.

릴리스 0.9.7까지는 메시지가 다음 16바이트 경계까지만 패딩되었으며, 16바이트의 배수가 아닌 메시지는 유효하지 않을 가능성이 있었습니다.

릴리스 0.9.7부터 메시지는 현재 MTU가 준수되는 한 임의의 길이로 패딩될 수 있습니다. 16바이트의 마지막 블록을 넘어서는 추가 1-15 패딩 바이트는 암호화되거나 복호화될 수 없으며 무시됩니다. 그러나 전체 길이와 모든 패딩은 MAC 계산에 포함됩니다.

릴리스 0.9.8부터 전송되는 메시지는 반드시 16바이트의 배수일 필요가 없습니다. SessionConfirmed 메시지는 예외이며, 아래를 참조하세요.

## 키

SessionCreated 및 SessionConfirmed 메시지의 서명은 네트워크 데이터베이스에 게시하여 대역 외로 배포되는 [RouterIdentity](/docs/specs/common-structures/#routeridentity)의 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)와 관련된 [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)를 사용하여 생성됩니다.

릴리스 0.9.15까지는 서명 알고리즘이 항상 DSA였으며, 40바이트 서명을 사용했습니다.

릴리스 0.9.16부터 서명 알고리즘은 Bob의 [RouterIdentity](/docs/specs/common-structures/#routeridentity)에 있는 [KeyCertificate](/docs/specs/common-structures/#key-certificates)로 지정할 수 있습니다.

소개 키와 세션 키 모두 32바이트이며, Common structures 사양 [SessionKey](/docs/specs/common-structures/#sessionkey)에 의해 정의됩니다. MAC와 암호화에 사용되는 키는 아래 각 메시지에 대해 지정됩니다.

Introduction key는 외부 채널(네트워크 데이터베이스)을 통해 전달되며, 전통적으로 0.9.47 릴리스까지는 router Hash와 동일했지만, 0.9.48 릴리스부터는 무작위일 수 있습니다.

## 참고사항

### IPv6

프로토콜 사양에서는 4바이트 IPv4와 16바이트 IPv6 주소를 모두 허용합니다. SSU-over-IPv6는 버전 0.9.8부터 지원됩니다. IPv6 지원에 대한 자세한 내용은 아래 개별 메시지 문서를 참조하세요.

### 타임스탬프 {#time}

I2P의 대부분은 밀리초 해상도를 가진 8바이트 [Date](/docs/specs/common-structures/#date) 타임스탬프를 사용하지만, SSU는 1초 해상도를 가진 4바이트 부호 없는 정수 타임스탬프를 사용합니다. 이 값들이 부호 없는 정수이기 때문에, 2106년 2월까지는 롤오버되지 않습니다.

## 메시지

10개의 메시지(페이로드 타입)가 정의되어 있습니다:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (타입 0) {#sessionrequest}

이것은 세션을 설정하기 위해 전송되는 첫 번째 메시지입니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
메시지 형식:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
현재 구현에서 헤더를 포함한 일반적인 크기: 304(IPv4) 또는 320(IPv6) 바이트 (non-mod-16 패딩 이전)

#### 확장 옵션

참고: 0.9.24에서 구현됨.

- 최소 길이: 3 (옵션 길이 바이트 + 2바이트)
- 옵션 길이: 최소 2
- 2바이트 플래그:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### 참고 사항

- IPv4 및 IPv6 주소가 지원됩니다.
- 해석되지 않은 데이터는 향후 챌린지에 사용될 가능성이 있습니다.

### SessionCreated (타입 1) {#sessioncreated}

이는 [SessionRequest](#sessionrequest)에 대한 응답입니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
메시지 형식:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
현재 구현에서 헤더를 포함한 일반적인 크기: 368바이트 (IPv4 또는 IPv6) (non-mod-16 패딩 이전)

#### 참고사항

- IPv4와 IPv6 주소가 지원됩니다.
- relay tag가 0이 아닌 경우, Bob은 Alice를 위해 introducer 역할을 제공하고 있습니다. Alice는 이후 네트워크 데이터베이스에 Bob의 주소와 relay tag를 게시할 수 있습니다.
- 서명을 위해 Bob은 자신의 외부 포트를 사용해야 합니다. 이는 Alice가 검증에 사용할 포트이기 때문입니다. Bob의 NAT/방화벽이 내부 포트를 다른 외부 포트로 매핑했고 Bob이 이를 인지하지 못하는 경우, Alice의 검증이 실패합니다.
- 서명에 대한 자세한 내용은 위의 [Keys](#keys) 섹션을 참조하세요. Alice는 이미 네트워크 데이터베이스에서 Bob의 공개 서명 키를 가지고 있습니다.
- 릴리스 0.9.15까지는 서명이 항상 40바이트 DSA 서명이었고 패딩은 항상 8바이트였습니다. 릴리스 0.9.16부터는 서명 타입과 길이가 Bob의 [RouterIdentity](/docs/specs/common-structures/#routeridentity)에 있는 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)의 타입에 의해 암시됩니다. 패딩은 16바이트의 배수로 필요한 만큼 적용됩니다.
- 이는 송신자의 intro key를 사용하는 유일한 메시지입니다. 다른 모든 메시지는 수신자의 intro key 또는 설정된 세션 키를 사용합니다.
- 서명 시간은 현재 구현에서 사용되지 않거나 검증되지 않는 것으로 보입니다.
- 해석되지 않은 데이터는 향후 challenge용으로 사용될 가능성이 있습니다.
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않음.

### SessionConfirmed (타입 2) {#sessionconfirmed}

이것은 [SessionCreated](#sessioncreated) 메시지에 대한 응답이며 세션 설정의 마지막 단계입니다. Router Identity가 조각화되어야 하는 경우 여러 개의 SessionConfirmed 메시지가 필요할 수 있습니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0부터 F-2까지** (F > 1인 경우에만; 현재 사용되지 않음, 아래 참고사항 참조):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (마지막 또는 유일한 fragment):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
현재 구현에서 헤더를 포함한 일반적인 크기: 512바이트 (Ed25519 서명 포함) 또는 480바이트 (DSA-SHA1 서명 포함) (non-mod-16 패딩 이전)

#### 참고사항

- 현재 구현에서 최대 fragment 크기는 512바이트입니다. 더 긴 서명이 fragmentation 없이 작동할 수 있도록 이를 확장해야 합니다.
  현재 구현은 두 fragment에 걸쳐 분할된 서명을 올바르게 처리하지 않습니다.
- 일반적인 [RouterIdentity](/docs/specs/common-structures/#routeridentity)는 387바이트이므로 fragmentation이 필요하지 않습니다. 새로운 암호화가 RouterIdentity의 크기를 확장한다면
  fragmentation 체계를 신중히 테스트해야 합니다.
- 누락된 fragment를 요청하거나 재전송하는 메커니즘이 없습니다.
- 전체 fragment 필드 F는 모든 fragment에서 동일하게 설정되어야 합니다.
- DSA 서명에 대한 자세한 내용은 위의 [Keys](#keys) 섹션을 참조하세요.
- Signed-on time은 현재 구현에서 사용되지 않거나 검증되지 않는 것으로 보입니다.
- 서명이 끝에 있기 때문에 마지막 또는 유일한 패킷의 padding은
  전체 패킷을 16바이트의 배수로 맞춰야 하며, 그렇지 않으면 서명이 올바르게 복호화되지 않습니다. 이는 padding이 끝에 있는 다른 모든 메시지 유형과는 다릅니다.
- 릴리스 0.9.15까지 서명은 항상 40바이트 DSA 서명이었습니다.
  릴리스 0.9.16부터 서명 유형과 길이는 Alice의 [RouterIdentity](/docs/specs/common-structures/#routeridentity)에 있는 [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)의 유형으로 암시됩니다. padding은
  16바이트의 배수로 필요한 만큼 적용됩니다.
- 헤더의 확장 옵션: 예상되지 않으며 정의되지 않습니다.

### SessionDestroyed (타입 8) {#sessiondestroyed}

SessionDestroyed 메시지는 릴리스 0.8.1에서 구현되었으며(수신 전용), 릴리스 0.8.9부터 전송됩니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
이 메시지는 어떤 데이터도 포함하지 않습니다. 현재 구현에서 헤더를 포함한 일반적인 크기: 48바이트 (non-mod-16 패딩 이전)

#### 참고사항

- 송신자 또는 수신자의 intro key로 수신된 파기 메시지는 무시됩니다.
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않음.

### RelayRequest (타입 3) {#relayrequest}

이것은 Alice가 Bob에게 Charlie에 대한 소개를 요청하기 위해 보내는 첫 번째 메시지입니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
메시지 형식:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
헤더를 포함한 일반적인 크기, 현재 구현에서: 96바이트 (Alice IP 미포함) 또는 112바이트 (4바이트 Alice IP 포함) (non-mod-16 패딩 이전)

#### 참고사항

- IP 주소는 패킷의 소스 주소와 포트와 다른 경우에만 포함됩니다.
- 이 메시지는 IPv4 또는 IPv6를 통해 전송될 수 있습니다.
  IPv4 introduction을 위해 IPv6로 메시지가 전송되거나,
  (릴리스 0.9.50부터) IPv6 introduction을 위해 IPv4로 전송되는 경우,
  Alice는 자신의 introduction 주소와 포트를 포함해야 합니다.
  이는 릴리스 0.9.50부터 지원됩니다.
- Alice가 자신의 주소/포트를 포함하는 경우, Bob은 계속 진행하기 전에
  추가적인 검증을 수행할 수 있습니다.
  - 릴리스 0.9.24 이전에는 Java I2P가 연결과 다른 주소나 포트를 거부했습니다.
- Challenge는 구현되지 않았으며, challenge 크기는 항상 0입니다.
- IPv6에 대한 릴레이는 릴리스 0.9.50부터 지원됩니다.
- 릴리스 0.9.12 이전에는 Bob의 intro key가 항상 사용되었습니다. 릴리스 0.9.12부터는
  Alice와 Bob 사이에 설정된 세션이 있는 경우 session key가 사용됩니다.
  실제로는 설정된 세션이 있어야 합니다. Alice가 session created 메시지에서
  nonce(introduction tag)를 얻을 수 있고, Bob은 세션이 파괴되면
  introduction tag를 유효하지 않음으로 표시하기 때문입니다.
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않음.

### RelayResponse (타입 4) {#relayresponse}

이것은 [RelayRequest](#relayrequest)에 대한 응답이며 Bob에서 Alice로 전송됩니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
메시지 형식:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
현재 구현에서 헤더를 포함한 일반적인 크기: 64바이트(Alice IPv4) 또는 80바이트(Alice IPv6) (non-mod-16 패딩 이전)

#### 노트

- 이 메시지는 IPv4 또는 IPv6를 통해 전송될 수 있습니다.
- Alice의 IP 주소/포트는 Bob이 RelayRequest를 받은 명시적인 IP/포트이며 (Alice가 RelayRequest에 포함시킨 IP가 아닐 수 있음), IPv4 또는 IPv6일 수 있습니다. Alice는 현재 수신 시 이를 무시합니다.
- Charlie의 IP 주소는 IPv4이거나, 릴리스 0.9.50부터는 IPv6일 수 있으며, 이는 Alice가 Hole Punch 후에 SessionRequest를 보낼 주소입니다.
- IPv6에 대한 릴레이는 릴리스 0.9.50부터 지원됩니다.
- 릴리스 0.9.12 이전에는 Alice의 intro 키가 항상 사용되었습니다. 릴리스 0.9.12부터는 Alice와 Bob 간에 설정된 세션이 있는 경우 세션 키가 사용됩니다.
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않았습니다.

### RelayIntro (타입 5) {#relayintro}

이것은 Bob이 Charlie에게 보내는 Alice에 대한 소개입니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
메시지 형식:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
현재 구현에서 헤더를 포함한 일반적인 크기: 48바이트 (non-mod-16 패딩 이전)

#### 참고사항

- IPv4의 경우, Alice의 IP 주소는 항상 4바이트입니다. Alice가 IPv4를 통해 Charlie에 연결하려고 하기 때문입니다.
  릴리스 0.9.50부터 IPv6가 지원되며, Alice의 IP 주소는 16바이트일 수 있습니다.
- IPv4의 경우, 이 메시지는 설정된 IPv4 연결을 통해 전송되어야 합니다.
  Bob이 RelayResponse에서 Alice에게 반환할 Charlie의 IPv4 주소를 아는 유일한 방법이기 때문입니다.
  릴리스 0.9.50부터 IPv6가 지원되며, 이 메시지는 설정된 IPv6 연결을 통해 전송될 수 있습니다.
- 릴리스 0.9.50부터, introducer와 함께 게시되는 모든 SSU 주소는 "caps" 옵션에 "4" 또는 "6"을 포함해야 합니다.
- Challenge는 구현되지 않았으며, challenge 크기는 항상 0입니다
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않습니다.

### Data (타입 6) {#data}

이 메시지는 데이터 전송과 확인 응답에 사용됩니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**데이터:** 1바이트 플래그 (아래 참조); 명시적 ACK가 포함된 경우: 1바이트 ACK 수, 완전히 ACK되는 4바이트 MessageId들; ACK bitfield가 포함된 경우: 1바이트 ACK bitfield 수, 4바이트 MessageId들 + 1바이트 이상의 ACK bitfield (주석 참조); 확장 데이터가 포함된 경우: 1바이트 데이터 크기, 해당 바이트 수만큼의 확장 데이터 (현재 해석되지 않음); 1바이트 프래그먼트 수 (0일 수 있음); 0이 아닌 경우, 해당 수만큼의 메시지 프래그먼트들.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
각 fragment는 다음을 포함합니다: - 4바이트 messageId - 3바이트 fragment 정보:   - 비트 23-17: fragment # 0 - 127   - 비트 16: isLast (1 = true)   - 비트 15-14: 사용하지 않음, 향후 사용을 위한 호환성을 위해 0으로 설정   - 비트 13-0: fragment 크기 0 - 16383 - 해당 바이트 수만큼의 fragment 데이터

메시지 형식:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ACK 비트필드 참고사항

bitfield는 각 바이트의 하위 7비트를 사용하며, 상위 비트는 추가 bitfield 바이트가 뒤따르는지를 지정합니다 (1 = true, 0 = 현재 bitfield 바이트가 마지막). 이러한 7비트 배열의 시퀀스는 fragment가 수신되었는지 여부를 나타냅니다 - 비트가 1이면 fragment가 수신된 것입니다. 명확히 하기 위해, fragment 0, 2, 5, 9가 수신되었다고 가정하면, bitfield 바이트는 다음과 같습니다:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### 참고사항

- 현재 구현에서는 공간이 허용되는 경우 이전에 ack된 메시지에 대해 제한된 수의 중복 ack를 추가합니다.
- 프래그먼트 수가 0인 경우, 이는 ack 전용 또는 keepalive 메시지입니다.
- ECN 기능은 구현되지 않았으며, 비트는 설정되지 않습니다.
- 현재 구현에서는 프래그먼트 수가 0보다 클 때 want reply 비트가 설정되고, 프래그먼트가 없을 때는 설정되지 않습니다.
- Extended data는 구현되지 않았으며 존재하지 않습니다.
- 다중 프래그먼트 수신은 모든 릴리스에서 지원됩니다. 다중 프래그먼트 전송은 릴리스 0.9.16에서 구현되었습니다.
- 현재 구현에서는 최대 프래그먼트 수가 64개입니다 (최대 프래그먼트 번호 = 63).
- 현재 구현에서는 최대 프래그먼트 크기가 당연히 MTU보다 작습니다.
- 많은 수의 ACK를 전송해야 하는 경우에도 최대 MTU를 초과하지 않도록 주의하세요.
- 프로토콜은 길이가 0인 프래그먼트를 허용하지만 전송할 이유는 없습니다.
- SSU에서 데이터는 표준 16바이트 I2NP 헤더 대신 짧은 5바이트 I2NP 헤더와 그 뒤에 I2NP 메시지의 페이로드를 사용합니다. 짧은 I2NP 헤더는 1바이트 I2NP 유형과 4바이트 만료 시간(초)으로만 구성됩니다. I2NP 메시지 ID가 프래그먼트의 메시지 ID로 사용됩니다. I2NP 크기는 프래그먼트 크기로부터 조립됩니다. UDP 메시지 무결성이 복호화에 의해 보장되므로 I2NP 체크섬은 필요하지 않습니다.
- 메시지 ID는 시퀀스 번호가 아니며 연속적이지 않습니다. SSU는 순서대로 전달을 보장하지 않습니다. I2NP 메시지 ID를 SSU 메시지 ID로 사용하지만, SSU 프로토콜 관점에서 이들은 무작위 번호입니다. 실제로 router가 모든 피어에 대해 단일 Bloom 필터를 사용하므로, 메시지 ID는 실제 무작위 번호여야 합니다.
- 시퀀스 번호가 없기 때문에 ACK가 수신되었는지 확실하게 알 수 있는 방법이 없습니다. 현재 구현은 일상적으로 많은 양의 중복 ACK를 전송합니다. 중복 ACK는 혼잡의 표시로 받아들여져서는 안 됩니다.
- ACK Bitfield 참고사항: 데이터 패킷의 수신자는 마지막 프래그먼트를 받지 않는 한 메시지에 몇 개의 프래그먼트가 있는지 알 수 없습니다. 따라서 응답으로 전송되는 bitfield 바이트 수는 프래그먼트 수를 7로 나눈 값보다 적거나 많을 수 있습니다. 예를 들어, 수신자가 본 가장 높은 프래그먼트가 번호 4인 경우, 총 13개의 프래그먼트가 있을 수 있어도 1바이트만 전송하면 됩니다. ack된 각 메시지 ID에 대해 최대 10바이트 (즉, (64 / 7) + 1)까지 포함될 수 있습니다.
- 헤더의 확장 옵션: 예상되지 않으며, 정의되지 않았습니다.

### PeerTest (타입 7) {#peertest}

자세한 내용은 [SSU Peer Testing](/docs/transport/ssu/#peerTesting)을 참조하십시오. 참고: IPv6 peer testing은 릴리스 0.9.27부터 지원됩니다.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
사용된 암호화 키 (발생 순서대로 나열): 1. Alice에서 Bob으로 전송될 때: Alice/Bob sessionKey 2. Bob에서 Charlie로 전송될 때: Bob/Charlie sessionKey 3. Charlie에서 Bob으로 전송될 때: Bob/Charlie sessionKey 4. Bob에서 Alice로 전송될 때: Alice/Bob sessionKey (또는 0.9.52 이전 Bob의 경우, Alice의 introKey) 5. Charlie에서 Alice로 전송될 때: Bob으로부터 PeerTest 메시지에서 수신한 Alice의 introKey 6. Alice에서 Charlie로 전송될 때: Charlie로부터 PeerTest 메시지에서 수신한 Charlie의 introKey

사용된 MAC 키 (발생 순서대로 나열): 1. Alice에서 Bob으로 전송될 때: Alice/Bob MAC 키 2. Bob에서 Charlie로 전송될 때: Bob/Charlie MAC 키 3. Charlie에서 Bob으로 전송될 때: Bob/Charlie MAC 키 4. Bob에서 Alice로 전송될 때: Alice로부터 PeerTest 메시지에서 수신한 Alice의 introKey 5. Charlie에서 Alice로 전송될 때: Bob으로부터 PeerTest 메시지에서 수신한 Alice의 introKey 6. Alice에서 Charlie로 전송될 때: Charlie로부터 PeerTest 메시지에서 수신한 Charlie의 introKey

메시지 형식:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
현재 구현에서 헤더를 포함한 일반적인 크기: 80바이트 (non-mod-16 패딩 이전)

#### 주의사항

- Alice가 보낼 때: IP 주소 크기는 0이고, IP 주소는 없으며, 포트는 0입니다. Bob과 Charlie는 이 데이터를 사용하지 않기 때문입니다. 목적은 Alice의 실제 IP 주소/포트를 확인하고 Alice에게 알려주는 것입니다. Bob과 Charlie는 Alice가 자신의 주소를 어떻게 생각하는지는 신경쓰지 않습니다.
- Bob이나 Charlie가 보낼 때: IP와 포트가 존재하며, IP 주소는 4바이트 또는 16바이트입니다. IPv6 테스팅은 릴리스 0.9.27부터 지원됩니다.
- Charlie가 Alice에게 보낼 때, IP와 포트는 다음과 같습니다:
  첫 번째 (메시지 5): 메시지 2에서 수신된 Alice가 요청한 IP와 포트.
  두 번째 (메시지 7): 메시지 6이 수신된 실제 Alice의 IP와 포트.
- IPv6 참고사항: 릴리스 0.9.26까지는 IPv4 주소 테스팅만 지원됩니다. 따라서 모든 Alice-Bob과 Alice-Charlie 통신은 IPv4를 통해 이루어져야 합니다. 하지만 Bob-Charlie 통신은 IPv4 또는 IPv6를 통해 가능합니다. PeerTest 메시지에서 지정될 때 Alice의 주소는 4바이트여야 합니다.
  릴리스 0.9.27부터는 IPv6 주소 테스팅이 지원되며, Bob과 Charlie가 공개된 IPv6 주소에서 'B' 기능으로 지원을 표시하는 경우 Alice-Bob과 Alice-Charlie 통신이 IPv6를 통해 가능합니다.
  자세한 내용은 Proposal 126을 참조하세요.
- Alice는 테스트하고자 하는 전송(IPv4 또는 IPv6)을 통해 기존 세션을 사용하여 Bob에게 요청을 보냅니다.
  Bob이 IPv4를 통해 Alice로부터 요청을 받으면, Bob은 IPv4 주소를 광고하는 Charlie를 선택해야 합니다.
  Bob이 IPv6를 통해 Alice로부터 요청을 받으면, Bob은 IPv6 주소를 광고하는 Charlie를 선택해야 합니다.
  실제 Bob-Charlie 통신은 IPv4 또는 IPv6를 통해 가능합니다(즉, Alice의 주소 유형과 무관).
- 피어는 활성 테스트 상태(nonce) 테이블을 유지해야 합니다. PeerTest 메시지 수신 시 테이블에서 nonce를 찾습니다. 발견되면 기존 테스트이며 역할(Alice, Bob, 또는 Charlie)을 알 수 있습니다. 그렇지 않으면 IP가 없고 포트가 0인 경우 새 테스트이며 당신은 Bob입니다. 그 외의 경우 새 테스트이며 당신은 Charlie입니다.
- 릴리스 0.9.15부터 Alice는 Bob과 확립된 세션을 가지고 있어야 하며 세션 키를 사용해야 합니다.
- API 버전 0.9.52 이전에는 일부 구현에서 Bob이 Alice와 확립된 세션이 있음에도 불구하고(0.9.15부터) Alice/Bob 세션 키 대신 Alice의 intro 키를 사용하여 Alice에게 응답했습니다.
  API 버전 0.9.52부터 모든 구현에서 Bob이 올바르게 세션 키를 사용하며, Bob이 API 버전 0.9.52 이상인 경우 Alice는 Alice의 intro 키로 Bob으로부터 받은 메시지를 거부해야 합니다.
- 헤더의 확장 옵션: 예상되지 않음, 정의되지 않음.

### HolePunch {#holepunch}

HolePunch는 단순히 데이터가 없는 UDP 패킷입니다. 이는 인증되지 않고 암호화되지 않습니다. SSU 헤더를 포함하지 않으므로 메시지 타입 번호가 없습니다. 이는 Introduction 시퀀스의 일부로 Charlie에서 Alice로 전송됩니다.

## 샘플 데이터그램 {#sampledatagrams}

### 최소 데이터 메시지

- 단편화 없음, ACK 없음, NACK 없음 등
- 크기: 39바이트

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### 페이로드가 포함된 최소 데이터 메시지

- 크기: 46+fragmentSize 바이트

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## 참고 자료

- [AES 암호화](/docs/specs/cryptography/#AES)
- [공통 구조 사양](/docs/specs/common-structures/)
- [날짜](/docs/specs/common-structures/#date)
- [ElGamal 암호화](/docs/specs/cryptography/#elgamal)
- [HMAC 세부사항](/docs/specs/cryptography/#udp)
- [I2P 소스](https://github.com/i2p/i2p.i2p)
- [i2pd 소스](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [SSU 개요](/docs/transport/ssu/)
- [SSU 키](/docs/transport/ssu/#keys)
- [SSU 피어 테스팅](/docs/transport/ssu/#peerTesting)
