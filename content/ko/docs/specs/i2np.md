---
title: "I2NP 사양"
description: "router 간 통신을 위한 I2P Network Protocol (I2NP) 메시지 형식, 우선순위 및 공통 구조"
slug: "i2np"
aliases:
  - "/ko/spec/i2np"
  - "/ko/spec/i2np/"
  - "/ko/i2np_spec"
  - "/ko/i2np_spec/"
category: "프로토콜"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## 개요

I2P Network Protocol (I2NP)은 I2P 전송 프로토콜 위의 계층입니다. 이는 router 간 프로토콜입니다. 네트워크 데이터베이스 조회 및 응답, tunnel 생성, 그리고 암호화된 router 및 클라이언트 데이터 메시지에 사용됩니다. I2NP 메시지는 다른 router에 점대점으로 전송되거나, tunnel을 통해 해당 router에 익명으로 전송될 수 있습니다.

## 프로토콜 버전 {#versions}

모든 router는 RouterInfo 속성의 "router.version" 필드에 자신의 I2NP 프로토콜 버전을 게시해야 합니다. 이 버전 필드는 API 버전으로, 다양한 I2NP 프로토콜 기능에 대한 지원 수준을 나타내며, 반드시 실제 router 버전과 일치하지는 않습니다.

대안적인 (non-Java) router들이 실제 router 구현에 대한 버전 정보를 게시하려는 경우, 다른 속성에서 그렇게 해야 합니다. 아래 나열된 것 이외의 버전도 허용됩니다. 지원은 숫자 비교를 통해 결정됩니다. 예를 들어, 0.9.13은 0.9.12 기능에 대한 지원을 의미합니다. "coreVersion" 속성은 더 이상 router 정보에 게시되지 않으며, I2NP 프로토콜 버전 결정에 사용된 적이 없다는 점에 유의하십시오.

I2NP 프로토콜 버전에 대한 기본 요약은 다음과 같습니다. 자세한 내용은 아래를 참조하십시오.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
NTCP 및 SSU transport 관련 기능과 호환성 문제도 있다는 점을 참고하세요. 자세한 내용은 NTCP와 SSU transport 문서를 확인하시기 바랍니다.

## 공통 구조 {#structures}

다음 구조들은 여러 I2NP 메시지의 구성 요소입니다. 이들은 완전한 메시지가 아닙니다.

### I2NP 메시지 헤더 {#struct-I2NPMessageHeader}

#### 설명

체크섬, 만료 날짜 등과 같은 중요한 정보를 포함하는 모든 I2NP 메시지의 공통 헤더입니다.

#### 목차

상황에 따라 세 가지 별도 형식이 사용됩니다. 하나의 표준 형식과 두 개의 단축 형식입니다.

표준 16바이트 형식은 이 메시지의 타입을 지정하는 1바이트 [Integer](/docs/specs/common-structures/#integer), 그 다음에 message-id를 지정하는 4바이트 [Integer](/docs/specs/common-structures/#integer)를 포함합니다. 그 후에는 만료 [Date](/docs/specs/common-structures/#date)가 있고, 메시지 페이로드의 길이를 지정하는 2바이트 [Integer](/docs/specs/common-structures/#integer)가 따라오며, 첫 번째 바이트로 잘린 [Hash](/docs/specs/common-structures/#hash)가 이어집니다. 그 후에 실제 메시지 데이터가 따라옵니다.

짧은 형식은 밀리초 단위의 8바이트 만료 시간 대신 초 단위의 4바이트 만료 시간을 사용합니다. 짧은 형식은 체크섬이나 크기를 포함하지 않으며, 이들은 상황에 따라 캡슐화에 의해 제공됩니다.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### 참고 사항

- [SSU](/docs/transports/ssu/)를 통해 전송될 때는 16바이트 표준 헤더가 사용되지 않습니다. 1바이트 타입과 4바이트 만료 시간(초 단위)만 포함됩니다. 메시지 ID와 크기는 SSU 데이터 패킷 형식에 통합됩니다. 복호화 과정에서 오류가 감지되므로 체크섬은 필요하지 않습니다.

- [NTCP2](/docs/specs/ntcp2/) 또는 [SSU2](/docs/specs/ssu2/)를 통해 전송될 때는 16바이트 표준 헤더가 사용되지 않습니다. 1바이트 타입, 4바이트 메시지 id, 그리고 4바이트 만료 시간(초 단위)만 포함됩니다. 크기는 NTCP2 및 SSU2 데이터 패킷 형식에 통합됩니다. 복호화 과정에서 오류가 감지되므로 체크섬은 필요하지 않습니다.

- 표준 헤더는 다른 메시지와 구조체(Data, TunnelData, TunnelGateway, GarlicClove) 내에 포함된 I2NP 메시지에도 필요합니다. 릴리스 0.8.12부터 오버헤드를 줄이기 위해 프로토콜 스택의 일부 지점에서 체크섬 검증이 비활성화되었습니다. 그러나 이전 버전과의 호환성을 위해 체크섬 생성은 여전히 필요합니다. 원격 router의 버전이 알려진 프로토콜 스택의 지점을 결정하여 체크섬 생성을 비활성화할 수 있는 방법은 향후 연구 주제입니다.

- 짧은 만료 시간은 부호가 없으며 2106년 2월 7일에 순환됩니다. 해당 날짜부터는 올바른 시간을 얻기 위해 오프셋을 추가해야 합니다.

- 구현체는 만료 시간이 너무 먼 미래로 설정된 메시지를 거부할 수 있습니다. 권장되는 최대 만료 시간은 미래 60초입니다.

### BuildRequestRecord {#struct-BuildRequestRecord}

더 이상 사용되지 않으며, 현재 네트워크에서는 tunnel에 ElGamal router가 포함된 경우에만 사용됩니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

#### 설명

tunnel에서 한 개의 hop 생성을 요청하기 위한 여러 레코드 세트 중 하나의 레코드입니다. 자세한 내용은 [tunnel 개요](/docs/specs/tunnel-implementation/)와 [ElGamal tunnel 생성 사양](/docs/specs/tunnel-creation/)을 참조하세요.

ECIES-X25519 BuildRequestRecord에 대해서는 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하십시오.

#### 목차 (ElGamal)

메시지를 받을 [TunnelId](/docs/specs/common-structures/#tunnelid), 그 다음에 우리의 [RouterIdentity](/docs/specs/common-structures/#routeridentity)의 [Hash](/docs/specs/common-structures/#hash)가 옵니다. 그 후에 다음 router의 [RouterIdentity](/docs/specs/common-structures/#routeridentity)의 [TunnelId](/docs/specs/common-structures/#tunnelid)와 [Hash](/docs/specs/common-structures/#hash)가 따라옵니다.

ElGamal 및 AES 암호화됨:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal 암호화:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
평문:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### 참고 사항

- 512바이트 암호화된 레코드에서, ElGamal 데이터는 514바이트 ElGamal 암호화 블록 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)의 1-256바이트와 258-513바이트를 포함합니다. 블록의 두 패딩 바이트(위치 0과 257의 0 바이트)는 제거됩니다.

- 필드 내용에 대한 자세한 사항은 [tunnel 생성 명세](/docs/specs/tunnel-creation/)를 참조하세요.

### BuildResponseRecord {#struct-BuildResponseRecord}

DEPRECATED, ElGamal router가 포함된 tunnel에서만 현재 네트워크에서 사용됩니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

#### 설명

빌드 요청에 대한 응답이 포함된 여러 레코드 세트 중 하나의 레코드입니다. 자세한 내용은 [tunnel 개요](/docs/specs/tunnel-implementation/)와 [ElGamal tunnel 생성 사양](/docs/specs/tunnel-creation/)을 참조하세요.

ECIES-X25519 BuildResponseRecords에 대해서는 [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

#### 목차 (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### 참고사항

- 랜덤 데이터 필드는 향후 혼잡도나 피어 연결 정보를 요청자에게 다시 반환하는 데 사용될 수 있습니다.

- reply 필드에 대한 자세한 내용은 [터널 생성 사양](/docs/specs/tunnel-creation/)을 참조하세요.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

ECIES-X25519 router에만 해당하며, API 버전 0.9.51부터 적용됩니다. 암호화 시 218바이트입니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)를 참조하세요.

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

ECIES-X25519 router 전용, API 버전 0.9.51부터. 암호화 시 218바이트. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) 참조.

### GarlicClove {#struct-GarlicClove}

경고: 이것은 ElGamal로 암호화된 garlic 메시지 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) 내의 garlic clove에 사용되는 형식입니다. ECIES-AEAD-X25519-Ratchet garlic 메시지와 garlic clove의 형식은 상당히 다릅니다. 사양은 [ECIES](/docs/specs/ecies/)를 참조하세요.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### 참고사항

- Clove는 절대 단편화되지 않습니다. Garlic Clove에서 사용될 때, Delivery Instructions 플래그 바이트의 첫 번째 비트는 암호화를 지정합니다. 이 비트가 0이면 clove는 암호화되지 않습니다. 1이면 clove는 암호화되며, 32바이트 Session Key가 플래그 바이트 바로 다음에 옵니다. Clove 암호화는 완전히 구현되지 않았습니다.

- [garlic routing 사양서](/docs/overview/garlic-routing/)도 참조하세요.

- 최대 길이는 모든 clove의 총 길이와 GarlicMessage의 최대 길이에 대한 함수입니다.

- 향후에는 인증서가 라우팅에 대한 "지불"을 위한 HashCash로 사용될 가능성이 있습니다.

- 메시지는 모든 I2NP 메시지가 될 수 있습니다 (GarlicMessage도 포함되지만 실제로는 사용되지 않음). 실제로 사용되는 메시지는 DataMessage, DeliveryStatusMessage, DatabaseStoreMessage입니다.

- Clove ID는 일반적으로 전송 시 임의의 숫자로 설정되며, 수신 시 중복을 확인합니다 (최상위 Message ID와 동일한 메시지 ID 공간 사용)

### Garlic Clove 전달 지침 {#struct-GarlicCloveDeliveryInstructions}

이는 ElGamal 암호화된 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)와 ECIES-AEAD-X25519-Ratchet 암호화된 [ECIES](/docs/specs/ecies/) garlic clove 모두에 사용되는 형식입니다.

이 명세는 Garlic Clove 내부의 Delivery Instructions에만 적용됩니다. "Delivery Instructions"는 Tunnel Message 내부에서도 사용되지만, 해당 형식은 상당히 다릅니다. 자세한 내용은 [Tunnel Message 문서](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)를 참조하세요. Tunnel Message Delivery Instructions에는 다음 명세를 사용하지 마세요!

세션 키와 지연은 사용되지 않고 절대 존재하지 않으므로, 가능한 세 가지 길이는 1(LOCAL), 33(ROUTER 및 DESTINATION), 37(TUNNEL) 바이트입니다.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## 메시지

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### 설명

요청하지 않은 데이터베이스 저장, 또는 성공적인 [DatabaseLookup](#msg-DatabaseLookup) 메시지에 대한 응답

#### 목차

압축되지 않은 LeaseSet, LeaseSet2, MetaLeaseSet, 또는 EncryptedLeaseset, 혹은 압축된 RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### 참고사항

- 보안을 위해, 메시지가 tunnel을 통해 수신된 경우 응답 필드는 무시됩니다.

- 키는 RouterIdentity 또는 Destination의 "실제" 해시이며, 라우팅 키가 아닙니다.

- 타입 3, 5, 7은 릴리스 0.9.38부터 사용됩니다. 자세한 정보는 제안서 123을 참조하세요. 이러한 타입들은 릴리스 0.9.38 이상의 router에만 전송되어야 합니다.

- 연결을 줄이기 위한 최적화로서, 타입이 LeaseSet이고 응답 토큰이 포함되어 있으며 응답 tunnel ID가 0이 아니고 응답 게이트웨이/tunnelID 쌍이 LeaseSet에서 lease로 발견되는 경우, 수신자는 응답을 LeaseSet의 다른 lease로 재라우팅할 수 있습니다.

- router OS와 구현을 숨기기 위해, 수정 시간을 0으로, OS 바이트를 0xFF로 설정하여 Java router 구현의 gzip과 일치시키고, XFL을 0x02(최대 압축, 가장 느린 알고리즘)로 설정합니다. RFC 1952를 참조하세요. 압축된 router 정보의 처음 10바이트는 다음과 같습니다(16진수): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### 설명

네트워크 데이터베이스에서 항목을 조회하는 요청입니다. 응답은 [DatabaseStore](#msg-DatabaseStore) 또는 [DatabaseSearchReply](#msg-DatabaseSearchReply)입니다.

#### 목차

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### 응답 암호화

참고: ElGamal router는 API 0.9.58부터 사용 중단되었습니다. 쿼리할 권장 최소 floodfill 버전이 이제 0.9.58이므로, 구현에서는 ElGamal floodfill router에 대한 암호화를 구현할 필요가 없습니다. ElGamal 목적지는 여전히 지원됩니다.

플래그 비트 4는 비트 1과 조합하여 응답 암호화 모드를 결정하는 데 사용됩니다. 플래그 비트 4는 버전 0.9.46 이상의 router에 전송할 때만 설정해야 합니다. 자세한 내용은 제안서 154와 156을 참조하세요.

아래 표에서 "DH n/a"는 응답이 암호화되지 않음을 의미합니다. "DH no"는 응답 키가 요청에 포함되어 있음을 의미합니다. "DH yes"는 응답 키가 DH 연산에서 파생됨을 의미합니다.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### 암호화 없음

reply_key, tags, 그리고 reply_tags가 존재하지 않습니다.

#### ElG to ElG

0.9.7부터 지원됨. 0.9.58부터 deprecated됨. ElG destination이 ElG router로 조회를 전송함.

요청자 키 생성:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
메시지 형식:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES에서 ElG로

0.9.46부터 지원됨. 0.9.58부터 사용 중단됨. ECIES destination이 ElG router에 조회를 보냄. reply_key와 reply_tags 필드는 ECIES 암호화된 응답을 위해 재정의됨.

요청자 키 생성:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
메시지 형식: reply_key 및 reply_tags 필드를 다음과 같이 재정의:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
응답은 [ECIES](/docs/specs/ecies/)에 정의된 ECIES 기존 세션 메시지입니다.

#### 응답 형식

이것은 기존 세션 메시지로, [ECIES](/docs/specs/ecies/)와 동일하며, 참조를 위해 아래에 복사되었습니다.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
AEAD 매개변수:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES에서 ECIES로 (0.9.49)

ECIES destination 또는 router가 ECIES router에 조회를 보냅니다. 0.9.49부터 지원됩니다.

ECIES router는 0.9.48에서 도입되었으며, [Proposal 156](/proposals/156/)을 참조하십시오. ECIES 목적지와 router는 위의 "ECIES to ElG" 섹션과 동일한 형식을 사용할 수 있으며, 요청에 응답 키가 포함됩니다. 조회 메시지 암호화는 [ECIES-ROUTERS](/docs/specs/ecies-routers/)에 명시되어 있습니다. 요청자는 익명입니다.

#### ECIES to ECIES (미래)

이 옵션은 아직 완전히 정의되지 않았습니다. [Proposal 156](/proposals/156/)을 참조하세요.

#### 참고사항

- 0.9.16 이전 버전에서는 RouterInfo 또는 LeaseSet에 대한 키일 수 있었습니다. 이들은 동일한 키 공간에 있었고, 특정 유형의 데이터만 요청하는 플래그가 없었기 때문입니다.

- 릴리스 0.9.7부터 암호화 플래그, 응답 키, 응답 태그.

- 암호화된 응답은 터널을 통한 응답일 때만 유용합니다.

- 대안 DHT 조회 전략(예: 재귀적 조회)이 구현된 경우 포함된 태그의 수가 1개보다 많을 수 있습니다.

- 조회 키와 제외 키는 "실제" 해시이며, 라우팅 키가 아닙니다.

- 타입 3, 5, 7은 릴리스 0.9.38부터 반환될 수 있습니다. 자세한 내용은 제안서 123을 참조하세요.

- 탐색적 조회 참고사항: 탐색적 조회는 키에 가까운 non-floodfill 해시 목록을 반환하도록 정의됩니다. 그러나 구현 변형에 대한 DatabaseSearchReply의 중요한 참고사항을 참조하십시오. 또한 이 사양은 수신자가 RI에 대한 검색 키를 조회하고 존재하는 경우 DSRM 대신 DatabaseStore를 반환해야 하는지에 대해 명확하게 설명한 적이 없습니다. Java는 조회를 수행하지만 i2pd는 그렇지 않습니다. 따라서 이전에 수신한 해시에 대해 탐색적 조회를 사용하는 것은 권장되지 않습니다.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### 설명

실패한 [DatabaseLookup](#msg-DatabaseLookup) 메시지에 대한 응답

#### 목차

요청된 키에 가장 가까운 router 해시 목록

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### 참고사항

- 'from' 해시는 인증되지 않았으므로 신뢰할 수 없습니다.

- 반환된 피어 해시가 반드시 쿼리되는 router보다 키에 더 가깝지는 않습니다. 일반 조회에 대한 응답의 경우, 이는 새로운 floodfill의 발견과 견고성을 위한 "역방향" 검색(키에서 더 멀리)을 용이하게 합니다.

- 탐색 조회를 위한 키는 일반적으로 무작위로 생성됩니다. 따라서 응답의 non-floodfill peer_hashes는 전체 로컬 네트워크 데이터베이스의 비효율적인 정렬이나 검색을 피하기 위해 키에 가깝지만 전체 로컬 네트워크 데이터베이스에서 반드시 가장 가까운 것은 아닌 피어를 제공하는 것과 같은 최적화된 알고리즘을 사용하여 선택될 수 있습니다. 캐싱과 같은 다른 전략도 적절할 수 있습니다. 이는 구현에 따라 달라집니다.

- 반환되는 해시의 일반적인 개수: 3

- 반환할 해시의 권장 최대 개수: 16

- 조회 키, 피어 해시, 그리고 from 해시는 "실제" 해시이며, 라우팅 키가 아닙니다.

### DeliveryStatus {#msg-DeliveryStatus}

#### 설명

간단한 메시지 확인 응답입니다. 일반적으로 메시지 발신자가 생성하며, 메시지 자체와 함께 Garlic Message로 래핑되어 목적지에서 반환됩니다.

이 메시지는 튜널 테스트에도 사용되며, 이 경우 발신자가 아웃바운드 튜널을 통해 인바운드 튜널로 보낸 후 다시 자신에게 되돌려 받는다. 이 용도에서도 일반적으로 Garlic 암호화(Garlic wrapping)가 적용된다. API 버전 0.9.68 2026-02부터 라우터는 처음 두 분 동안 트래픽을 수신하지 않은 참여 중인 튜널을 폐기할 수 있으므로, 튜널 테스트가 필수적으로 요구된다.

#### 목차

전달된 메시지의 ID와 생성 또는 도착 시간입니다.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### 참고사항

- 타임스탬프는 항상 생성자에 의해 현재 시간으로 설정되는 것으로 보입니다. 그러나 코드에서 이것의 여러 용도가 있으며, 향후 더 많이 추가될 수 있습니다.

- 이 메시지는 SSU [SSU-ED](/docs/transports/ssu/#establishDirect)에서 세션 설정 확인으로도 사용됩니다. 이 경우 메시지 ID는 임의의 숫자로 설정되고, "도착 시간"은 현재 네트워크 전체 ID인 2(즉, 0x0000000000000002)로 설정됩니다.

### Garlic {#msg-Garlic}

경고: 이것은 ElGamal로 암호화된 갈릭 메시지 [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)에 사용되는 형식입니다. ECIES-AEAD-X25519-Ratchet 갈릭 메시지 및 갈릭 클로브의 형식은 상당히 다르며, 사양은 [ECIES](/docs/specs/ecies/)를 참조하세요.

#### 설명

여러 개의 암호화된 I2NP 메시지를 래핑하는 데 사용됨

#### 목차

복호화했을 때, 일련의 [Garlic Clove](#struct-GarlicClove)와 추가 데이터로 구성되며, 이는 Clove Set이라고도 불립니다.

암호화됨:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
복호화된 데이터, 즉 클로브 세트(Clove Set):

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### 참고사항

- 암호화되지 않은 경우, 데이터는 하나 이상의 [Garlic Cloves](#struct-GarlicClove)를 포함합니다.

- AES 암호화된 블록은 최소 128바이트로 패딩됩니다; 32바이트 Session Tag와 함께 암호화된 메시지의 최소 크기는 160바이트입니다; 4바이트 길이와 함께 Garlic Message의 최소 크기는 164바이트입니다.

- 실제 최대 길이는 64 KB 미만입니다; [I2NP](/docs/protocol/i2np/)를 참조하세요.

- [ElGamal/AES 사양서](/docs/specs/elgamal-aes/)도 참조하세요.

- [garlic routing 명세서](/docs/overview/garlic-routing/)도 참조하세요.

- AES 암호화 블록의 128바이트 최소 크기는 현재 구성할 수 없습니다. 하지만 GarlicMessage 내 GarlicClove에 있는 DataMessage의 최소 크기는 오버헤드를 포함해서 어차피 128바이트입니다. 최소 크기를 늘리는 구성 가능한 옵션이 향후 추가될 수 있습니다.

- 메시지 ID는 일반적으로 전송 시 임의의 숫자로 설정되며 수신 시에는 무시되는 것으로 보입니다.

- 미래에는 인증서가 라우팅에 대한 "비용을 지불"하기 위한 HashCash로 사용될 수 있습니다.

### TunnelData {#msg-TunnelData}

#### 설명

터널의 게이트웨이 또는 참여자가 다음 참여자나 엔드포인트로 전송하는 메시지. 이 데이터는 고정된 길이를 가지며, 조각화되고, 묶이며, 패딩되며 암호화된 I2NP 메시지를 포함한다.

#### 목차

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### 참고 사항

- 이 메시지의 I2NP 메시지 ID는 각 홉에서 새로운 랜덤 번호로 설정됩니다.

- [Tunnel Message 명세서](/docs/legacy/tunnel-message/)도 참조하세요

### TunnelGateway {#msg-TunnelGateway}

#### 설명

터널의 수신 게이트웨이에서 터널로 전송할 다른 I2NP 메시지를 래핑합니다.

#### 목차

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### 참고사항

- 페이로드는 표준 16바이트 헤더가 있는 I2NP 메시지입니다.

### Data {#msg-Data}

#### 설명

Garlic 메시지와 Garlic Cloves에서 임의의 데이터를 래핑하는 데 사용됨.

#### 목차

정수 길이에 이어 불투명한 데이터가 오는 형식.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### 참고사항

- 이 메시지는 라우팅 정보를 포함하지 않으며 "unwrapped" 상태로 전송되지 않습니다. `Garlic` 메시지 내부에서만 사용됩니다.

### TunnelBuild {#msg-TunnelBuild}

사용 중단됨, [VariableTunnelBuild](#msg-VariableTunnelBuild) 사용

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### 주의사항

- 0.9.48부터는 ECIES-X25519 BuildRequestRecords도 포함할 수 있습니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- [tunnel 생성 명세서](/docs/specs/tunnel-creation/)도 참조하세요.

- 이 메시지의 I2NP 메시지 ID는 터널 생성 사양에 따라 설정되어야 합니다.

- 이 메시지는 `VariableTunnelBuild` 메시지로 대체되어 오늘날의 네트워크에서는 거의 볼 수 없지만, 매우 긴 tunnel에 대해서는 여전히 사용될 수 있으며 폐기되지 않았습니다. router는 반드시 구현해야 합니다.

### TunnelBuildReply {#msg-TunnelBuildReply}

사용 중단됨, [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply) 사용

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### 참고사항

- 0.9.48부터 ECIES-X25519 BuildResponseRecords도 포함할 수 있습니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- [터널 생성 사양서](/docs/specs/tunnel-creation/)도 참조하세요.

- 이 메시지의 I2NP 메시지 ID는 터널 생성 사양에 따라 설정되어야 합니다.

- 이 메시지는 `VariableTunnelBuildReply` 메시지로 대체되어 오늘날의 네트워크에서 거의 볼 수 없지만, 매우 긴 tunnel에 대해서는 여전히 사용될 수 있으며 폐기되지 않았습니다. router는 반드시 구현해야 합니다.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### 참고사항

- 0.9.48부터 ECIES-X25519 BuildRequestRecord도 포함할 수 있습니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- 이 메시지는 router 버전 0.7.12에서 도입되었으며, 해당 버전보다 이전 버전의 tunnel 참가자에게는 전송되지 않을 수 있습니다.

- [터널 생성 사양서](/docs/specs/tunnel-creation/)도 참고하세요.

- 이 메시지의 I2NP 메시지 ID는 tunnel 생성 사양에 따라 설정되어야 합니다.

- 오늘날 네트워크에서 일반적인 레코드 수는 4개이며, 총 크기는 2113입니다.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### 참고 사항

- 0.9.48 버전부터 ECIES-X25519 BuildResponseRecords도 포함할 수 있습니다. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- 이 메시지는 router 버전 0.7.12에서 도입되었으며, 해당 버전보다 이전 버전의 tunnel 참가자에게는 전송되지 않을 수 있습니다.

- [터널 생성 사양](/docs/specs/tunnel-creation/)도 참조하세요.

- 이 메시지의 I2NP 메시지 ID는 tunnel 생성 사양에 따라 설정되어야 합니다.

- 오늘날 네트워크에서 일반적인 레코드 수는 4개이며, 총 크기는 2113입니다.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### 설명

API 버전 0.9.51부터 ECIES-X25519 라우터에만 해당.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### 참고사항

- 0.9.51부터. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- 이 메시지는 router 버전 0.9.51에서 도입되었으며, 해당 버전보다 이전 버전의 tunnel 참가자에게는 전송되지 않을 수 있습니다.

- 현재 네트워크의 일반적인 레코드 수는 4개이며, 총 크기는 873입니다.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### 설명

새 터널의 아웃바운드 엔드포인트에서 발신자에게 전송됨. API 버전 0.9.51부터 ECIES-X25519 라우터에만 해당.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### 참고 사항

- 0.9.51부터. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/)을 참조하세요.

- 현재 네트워크에서 일반적인 레코드 수는 4개이며, 전체 크기는 873입니다.

## 참고 자료

- **[CRYPTO-ELG]** [암호화 - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [공통 구조 - Date](/docs/specs/common-structures/#date)
- **[ECIES]** [ECIES 명세](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [ECIES router 명세](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic 라우팅](/docs/overview/garlic-routing/)
- **[Hash]** [공통 구조 - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP 프로토콜](/docs/protocol/i2np/)
- **[Integer]** [공통 구조 - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [NTCP2 명세](/docs/specs/ntcp2/)
- **[Prop156]** [제안서 156](/proposals/156/)
- **[Prop157]** [제안서 157](/proposals/157/)
- **[RouterIdentity]** [공통 구조 - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU 전송](/docs/transports/ssu/)
- **[SSU-ED]** [SSU 전송 - Establish Direct](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [SSU2 명세](/docs/specs/ssu2/)
- **[TMDI]** [tunnel 메시지 전달 지침](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Tunnel 생성 명세](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [ECIES Tunnel 생성](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Tunnel 구현](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Tunnel 메시지 명세](/docs/legacy/tunnel-message/)
- **[TunnelId]** [공통 구조 - TunnelId](/docs/specs/common-structures/#tunnelid)
