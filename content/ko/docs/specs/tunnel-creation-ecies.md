---
title: "Tunnel 생성 사양 (ECIES-X25519)"
description: "전방향 보안을 위해 ECIES-X25519 암호화 기본 요소를 사용한 tunnel Build 메시지 암호화."
slug: "tunnel-creation-ecies"
aliases:
  - "/ko/docs/specs/tunnel-creation-ecies-spec"
  - "/ko/docs/specs/tunnel-creation-ecies-spec/"
category: "프로토콜"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## 개요

이 문서는 [ECIES-X25519](/docs/specs/ecies/)에서 도입된 암호화 기본 요소를 사용하는 Tunnel Build 메시지 암호화를 명시합니다. 이는 router를 ElGamal에서 ECIES-X25519 키로 변환하는 전체 제안 [Prop156](/proposals/156/)의 일부입니다.

두 가지 버전이 지정되어 있습니다. 첫 번째는 ElGamal router와의 호환성을 위해 기존의 빌드 메시지와 빌드 레코드 크기를 사용합니다. 이 사양은 릴리스 0.9.48부터 구현되었으며 현재는 더 이상 사용되지 않습니다. 두 번째는 두 개의 새로운 빌드 메시지와 더 작은 빌드 레코드 크기를 사용하며, ECIES router에서만 사용할 수 있습니다. 이 사양은 릴리스 0.9.51부터 구현되었습니다.

ElGamal + AES256에서 ECIES + ChaCha20으로 네트워크를 전환하는 목적으로, ElGamal과 ECIES router가 혼재된 tunnel이 필요합니다. 혼합 tunnel hop을 처리하기 위한 사양이 제공됩니다. ElGamal hop의 형식, 처리 또는 암호화에는 변경사항이 없습니다. 이 형식은 호환성을 위해 요구되는 대로 tunnel 빌드 레코드의 동일한 크기를 유지합니다.

ElGamal tunnel 생성자는 홉당 임시 X25519 키페어를 생성하고, ECIES 홉을 포함하는 tunnel 생성을 위해 이 규격을 따릅니다.

이 문서는 ECIES-X25519 tunnel 구축을 명시합니다. ECIES router에 필요한 모든 변경 사항의 개요는 제안서 156 [Prop156](/proposals/156/)을 참조하세요. 긴 레코드 사양 개발에 대한 추가 배경 정보는 제안서 152 [Prop152](/proposals/152/)를 참조하세요. 짧은 레코드 사양 개발에 대한 추가 배경 정보는 제안서 157 [Prop157](/proposals/157/)을 참조하세요.

### 암호화 기본 요소

이 명세를 구현하는 데 필요한 기본 요소들은 다음과 같습니다:

- [암호화](/docs/specs/cryptography/)에서와 같은 AES-256-CBC
- STREAM ChaCha20 함수: ENCRYPT(k, iv, plaintext) 및 DECRYPT(k, iv, ciphertext) - [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) 및 [RFC-7539](https://tools.ietf.org/html/rfc7539)에서와 같음
- STREAM ChaCha20/Poly1305 함수: ENCRYPT(k, n, plaintext, ad) 및 DECRYPT(k, n, ciphertext, ad) - [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), 및 [RFC-7539](https://tools.ietf.org/html/rfc7539)에서와 같음
- X25519 DH 함수 - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같음
- HKDF(salt, ikm, info, n) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같음

다른 곳에 정의된 기타 Noise 함수들:

- MixHash(d) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이
- MixKey(d) - [NTCP2](/docs/specs/ntcp2/) 및 [ECIES-X25519](/docs/specs/ecies/)에서와 같이

## 설계

### Noise 프로토콜 프레임워크

이 사양은 Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (개정 34, 2018-07-11)를 기반으로 한 요구사항을 제공합니다. Noise 용어에서 Alice는 개시자(initiator)이고, Bob은 응답자(responder)입니다.

이는 Noise 프로토콜 Noise_N_25519_ChaChaPoly_SHA256을 기반으로 합니다. 이 Noise 프로토콜은 다음 기본 요소들을 사용합니다:

- One-Way Handshake Pattern: N - Alice는 자신의 정적 키를 Bob에게 전송하지 않습니다 (N)
- DH Function: X25519 - [RFC-7748](https://tools.ietf.org/html/rfc7748)에 명시된 32바이트 키 길이를 가진 X25519 DH
- Cipher Function: ChaChaPoly - [RFC-7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8에 명시된 AEAD_CHACHA20_POLY1305. 12바이트 nonce이며, 처음 4바이트는 0으로 설정됩니다. [NTCP2](/docs/specs/ntcp2/)와 동일합니다
- Hash Function: SHA256 - I2P에서 이미 광범위하게 사용되는 표준 32바이트 해시

### 핸드셰이크 패턴

핸드셰이크는 [Noise](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드

빌드 요청은 Noise N 패턴과 동일합니다. 이는 또한 [NTCP2](/docs/specs/ntcp2/)에서 사용되는 XK 패턴의 첫 번째 메시지(세션 요청)와도 동일합니다.

```
<- s
  ...
  e es p ->
```
### 요청 암호화

빌드 요청 레코드는 tunnel 생성자에 의해 생성되고 개별 홉에 대해 비대칭 암호화됩니다. 요청 레코드의 이 비대칭 암호화는 현재 [Cryptography](/docs/specs/cryptography/)에 정의된 ElGamal을 사용하며 SHA-256 체크섬을 포함합니다. 이 설계는 전방향 보안을 제공하지 않습니다.

ECIES 설계는 ECIES-X25519 ephemeral-static DH와 함께 단방향 Noise 패턴 "N"을 사용하며, HKDF와 ChaCha20/Poly1305 AEAD를 통해 forward secrecy, 무결성, 인증을 제공합니다. Alice는 tunnel 구축 요청자입니다. tunnel의 각 홉은 Bob입니다.

### 응답 암호화

빌드 응답 레코드는 홉 생성자에 의해 생성되고 생성자에게 대칭 암호화됩니다. ElGamal 응답 레코드의 이 대칭 암호화는 SHA-256 체크섬이 앞에 붙은 AES입니다. 이 설계는 전방향 보안(forward-secret)을 제공하지 않습니다.

ECIES 응답은 무결성과 인증을 위해 ChaCha20/Poly1305 AEAD를 사용합니다.

## 긴 레코드 사양

참고: 더 이상 사용되지 않으며 폐기되었습니다. 아래에 명시된 Short Record 형식을 사용하세요.

### 빌드 요청 레코드

암호화된 BuildRequestRecord는 호환성을 위해 ElGamal과 ECIES 모두에서 528바이트입니다.

#### 요청 레코드 암호화되지 않음

이것은 ECIES-X25519 router들을 위한 tunnel BuildRequestRecord의 명세입니다. 변경 사항 요약:

- 사용하지 않는 32바이트 router 해시 제거
- 요청 시간을 시간에서 분으로 변경
- 향후 가변 tunnel 시간을 위한 만료 필드 추가
- 플래그를 위한 더 많은 공간 추가
- 추가 빌드 옵션을 위한 매핑 추가
- AES-256 응답 키와 IV는 홉 자체의 응답 레코드에 사용되지 않음
- 암호화 오버헤드가 적기 때문에 암호화되지 않은 레코드가 더 김

요청 레코드에는 ChaCha 응답 키가 포함되어 있지 않습니다. 이러한 키들은 KDF에서 파생됩니다. 아래를 참조하세요.

모든 필드는 빅 엔디안입니다.

암호화되지 않은 크기: 464 바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
flags 필드는 [Tunnel-Creation](/docs/specs/tunnel-creation/)에서 정의된 것과 동일하며 다음을 포함합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
비트 7은 해당 홉이 인바운드 게이트웨이(IBGW)가 될 것임을 나타냅니다. 비트 6은 해당 홉이 아웃바운드 엔드포인트(OBEP)가 될 것임을 나타냅니다. 두 비트 모두 설정되지 않은 경우, 해당 홉은 중간 참여자가 됩니다. 두 비트가 동시에 설정될 수는 없습니다.

요청 만료 시간은 향후 가변 tunnel 지속 시간을 위한 것입니다. 현재는 600(10분)만 지원됩니다.

tunnel 빌드 옵션은 [Common](/docs/specs/common-structures/)에 정의된 Mapping 구조입니다. 현재 정의된 유일한 옵션은 대역폭 매개변수용이며, API 0.9.65 기준으로 자세한 내용은 아래를 참조하십시오. Mapping 구조가 비어있는 경우, 이는 0x00 0x00 두 바이트입니다. Mapping의 최대 크기(길이 필드 포함)는 296바이트이며, Mapping 길이 필드의 최대값은 294입니다.

#### 요청 레코드 암호화됨

임시 공개 키(little-endian)를 제외한 모든 필드는 big-endian입니다.

암호화된 크기: 528 바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### 응답 레코드 구축

암호화된 BuildReplyRecord는 호환성을 위해 ElGamal과 ECIES 모두에서 528바이트입니다.

#### 응답 레코드 암호화되지 않음

이는 ECIES-X25519 router들을 위한 tunnel BuildReplyRecord의 명세서입니다. 변경 사항 요약:

- 빌드 응답 옵션에 대한 매핑 추가
- 암호화되지 않은 레코드는 암호화 오버헤드가 적기 때문에 더 길다

ECIES 응답은 ChaCha20/Poly1305로 암호화됩니다.

모든 필드는 빅 엔디안입니다.

암호화되지 않은 크기: 512바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel 빌드 응답 옵션은 [Common](/docs/specs/common-structures/)에 정의된 Mapping 구조입니다. 현재 정의된 유일한 옵션은 대역폭 매개변수에 대한 것으로, API 0.9.65부터 적용되며, 자세한 내용은 아래를 참조하세요. Mapping 구조가 비어있으면 0x00 0x00 2바이트입니다. Mapping의 최대 크기(길이 필드 포함)는 511바이트이며, Mapping 길이 필드의 최대값은 509입니다.

응답 바이트는 핑거프린팅을 방지하기 위해 [Tunnel-Creation](/docs/specs/tunnel-creation/)에서 정의된 다음 값 중 하나입니다:

- 0x00 (허용)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### 응답 레코드 암호화됨

암호화된 크기: 528 바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
ECIES 레코드로의 완전한 전환 후, 범위 패딩 규칙은 요청 레코드와 동일합니다.

### 레코드의 대칭 암호화

혼합 터널은 ElGamal에서 ECIES로의 전환 과정에서 허용되며 필요합니다. 전환 기간 동안 ECIES 키로 키를 생성하는 라우터의 수가 증가할 것입니다.

대칭 암호화 전처리는 동일한 방식으로 실행됩니다:

- "encryption":
  - cipher가 복호화 모드로 실행
  - 요청 레코드가 전처리에서 미리 복호화됨 (암호화된 요청 레코드를 숨김)
- "decryption":
  - cipher가 암호화 모드로 실행
  - 요청 레코드가 참여자 hop에 의해 암호화됨 (다음 평문 요청 레코드를 드러냄)
- ChaCha20은 "모드"가 없으므로 단순히 세 번 실행됨:
  - 전처리에서 한 번
  - hop에서 한 번
  - 최종 응답 처리에서 한 번

혼합 tunnel이 사용될 때, tunnel 생성자는 BuildRequestRecord의 대칭 암호화를 현재 홉과 이전 홉의 암호화 유형을 기반으로 해야 합니다.

각 hop은 BuildReplyRecord들과 VariableTunnelBuildMessage (VTBM)의 다른 레코드들을 암호화하기 위해 자체적인 암호화 유형을 사용할 것입니다.

응답 경로에서 endpoint (발신자)는 각 hop의 응답 키를 사용하여 [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)을 해제해야 합니다.

명확한 예시로, ElGamal로 둘러싸인 ECIES를 사용하는 아웃바운드 tunnel을 살펴보겠습니다:

- 송신자 (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

모든 BuildRequestRecord는 암호화된 상태입니다 (ElGamal 또는 ECIES 사용).

AES256/CBC 암호는 사용될 때 여전히 각 레코드에 대해 사용되며, 여러 레코드 간 체이닝은 하지 않습니다.

마찬가지로 ChaCha20은 전체 VTBM에 걸쳐 스트리밍하는 것이 아니라 각 레코드를 암호화하는 데 사용됩니다.

요청 레코드들은 송신자(OBGW)에 의해 전처리됩니다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:
  - H2의 reply key (ChaCha20)
  - H1의 reply key (AES256/CBC)
- H2의 레코드는 다음을 사용하여 "암호화"됩니다:
  - H1의 reply key (AES256/CBC)
- H1의 레코드는 대칭 암호화 없이 전송됩니다

H2만이 응답 암호화 플래그를 확인하고, 그 뒤에 AES256/CBC가 따라오는 것을 확인합니다.

각 hop에서 처리된 후, 레코드들은 "복호화된" 상태가 됩니다:

- H3의 레코드는 다음을 사용하여 "복호화"됩니다:
  - H3의 reply key (AES256/CBC)
- H2의 레코드는 다음을 사용하여 "복호화"됩니다:
  - H3의 reply key (AES256/CBC)
  - H2의 reply key (ChaCha20-Poly1305)
- H1의 레코드는 다음을 사용하여 "복호화"됩니다:
  - H3의 reply key (AES256/CBC)
  - H2의 reply key (ChaCha20)
  - H1의 reply key (AES256/CBC)

tunnel 생성자, 즉 Inbound Endpoint (IBEP)는 응답을 후처리합니다:

- H3의 레코드는 다음을 사용하여 "암호화"됩니다:
  - H3의 응답 키 (AES256/CBC)
- H2의 레코드는 다음을 사용하여 "암호화"됩니다:
  - H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20-Poly1305)
- H1의 레코드는 다음을 사용하여 "암호화"됩니다:
  - H3의 응답 키 (AES256/CBC)
  - H2의 응답 키 (ChaCha20)
  - H1의 응답 키 (AES256/CBC)

### 요청 레코드 키

이러한 키들은 ElGamal BuildRequestRecord에 명시적으로 포함됩니다. ECIES BuildRequestRecord의 경우, tunnel 키와 AES 응답 키가 포함되지만, ChaCha 응답 키는 DH 교환에서 파생됩니다. router 정적 ECIES 키의 세부사항은 [Prop156](/proposals/156/)을 참조하세요.

다음은 이전에 요청 레코드에서 전송된 키를 파생하는 방법에 대한 설명입니다.

#### 초기 ck와 h를 위한 KDF

이것은 표준 프로토콜 이름을 가진 패턴 "N"에 대한 표준 [NOISE](https://noiseprotocol.org/noise.html)입니다.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
(31 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
// Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
h = protocol_name || 0

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by all routers.
```
#### Request Record를 위한 KDF

ElGamal tunnel 생성자는 tunnel의 각 ECIES 홉에 대해 임시 X25519 키 쌍을 생성하고, 자신의 BuildRequestRecord를 암호화하기 위해 위의 방식을 사용합니다. ElGamal tunnel 생성자는 ElGamal 홉으로 암호화할 때 이 사양 이전의 방식을 사용합니다.

ECIES tunnel 생성자는 [Tunnel-Creation](/docs/specs/tunnel-creation/)에서 정의된 방식을 사용하여 각 ElGamal hop의 공개키로 암호화해야 합니다. ECIES tunnel 생성자는 ECIES hop으로 암호화할 때 위의 방식을 사용합니다.

이는 tunnel 홉이 동일한 암호화 유형의 암호화된 레코드만을 볼 수 있음을 의미합니다.

ElGamal 및 ECIES tunnel 생성자의 경우, ECIES hop으로 암호화하기 위해 hop당 고유한 임시 X25519 키쌍을 생성합니다.

**중요**: Ephemeral keys는 ECIES hop별로, 그리고 빌드 레코드별로 고유해야 합니다. 고유한 키를 사용하지 않으면 공모하는 hop들이 동일한 tunnel에 있음을 확인할 수 있는 공격 벡터가 생깁니다.

```
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
hesk = GENERATE_PRIVATE()
hepk = DERIVE_PUBLIC(hesk)

// MixHash(hepk)
// || below means append
h = SHA256(h || hepk);

// up until here, can all be precalculated by each router
// for all incoming build requests

// Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
sesk = GENERATE_PRIVATE()
sepk = DERIVE_PUBLIC(sesk)

// MixHash(sepk)
h = SHA256(h || sepk);

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
// Sender performs an X25519 DH with Hop's static public key.
// Each Hop, finds the record w/ their truncated identity hash,
// and extracts the Sender's ephemeral key preceding the encrypted record.
sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
// Save for Reply Record KDF
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
plaintext = 464 byte build request record
ad = h
ciphertext = ENCRYPT(k, n, plaintext, ad)

End of "es" message pattern.

// MixHash(ciphertext)
// Save for Reply Record KDF
h = SHA256(h || ciphertext)
```
`replyKey`, `layerKey` 및 `layerIV`는 여전히 ElGamal 레코드 내에 포함되어야 하며, 무작위로 생성될 수 있습니다.

### 응답 레코드 암호화

응답 레코드는 ChaCha20/Poly1305로 암호화됩니다.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## 짧은 레코드 명세서

이 명세는 두 개의 새로운 I2NP tunnel 구축 메시지인 Short Tunnel Build Message (유형 25)와 Outbound Tunnel Build Reply Message (유형 26)를 사용합니다.

tunnel 생성자와 생성된 tunnel의 모든 홉은 ECIES-X25519를 지원해야 하며, 최소 버전 0.9.51이어야 합니다. 응답 tunnel의 홉(아웃바운드 빌드의 경우) 또는 아웃바운드 tunnel의 홉(인바운드 빌드의 경우)에는 특별한 요구사항이 없습니다.

암호화된 요청 및 응답 레코드는 218바이트가 되며, 다른 모든 빌드 메시지의 528바이트와 비교됩니다.

평문 요청 레코드는 154바이트가 되며, 이는 ElGamal 레코드의 222바이트, 위에서 정의한 ECIES 레코드의 464바이트와 비교됩니다.

일반 텍스트 응답 레코드는 202바이트이며, 이는 ElGamal 레코드의 496바이트 및 위에서 정의된 ECIES 레코드의 512바이트와 비교됩니다.

응답 암호화는 홉 자체 레코드에 대해서는 ChaCha20/Poly1305를 사용하고, 빌드 메시지의 다른 레코드들에 대해서는 ChaCha20(ChaCha20/Poly1305가 아님)을 사용합니다.

요청 레코드는 HKDF를 사용하여 레이어와 응답 키를 생성함으로써 더 작아질 것이며, 따라서 이들은 요청에 명시적으로 포함되지 않습니다.

### 메시지 흐름

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### 참고사항

메시지의 garlic 래핑은 OBEP(인바운드 빌드의 경우) 또는 IBGW(아웃바운드 빌드의 경우)로부터 메시지를 숨깁니다. 이는 권장되지만 필수는 아닙니다. OBEP와 IBGW가 동일한 router인 경우에는 필요하지 않습니다.

### 짧은 빌드 요청 레코드

짧은 암호화된 BuildRequestRecord는 218바이트입니다.

#### 짧은 요청 레코드 암호화되지 않음

긴 레코드에서의 변경사항 요약:

- 암호화되지 않은 길이를 464바이트에서 154바이트로 변경
- 암호화된 길이를 528바이트에서 218바이트로 변경
- 레이어 및 응답 키와 IV 제거, 이들은 KDF에서 생성될 예정

요청 레코드에는 ChaCha 응답 키가 포함되어 있지 않습니다. 이러한 키는 KDF에서 파생됩니다. 아래를 참조하세요.

모든 필드는 빅 엔디안입니다.

암호화되지 않은 크기: 154바이트.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
flags 필드는 [Tunnel-Creation](/docs/specs/tunnel-creation/)에서 정의된 것과 동일하며 다음을 포함합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
비트 7은 해당 홉이 인바운드 게이트웨이(IBGW)가 될 것임을 나타냅니다. 비트 6은 해당 홉이 아웃바운드 엔드포인트(OBEP)가 될 것임을 나타냅니다. 어느 비트도 설정되지 않은 경우, 해당 홉은 중간 참여자가 됩니다. 두 비트 모두 동시에 설정될 수는 없습니다.

레이어 암호화 유형: 0은 AES용 (현재 tunnel에서와 같이); 1은 미래용 (ChaCha?)

요청 만료는 향후 가변 tunnel 지속 시간을 위한 것입니다. 현재 지원되는 유일한 값은 600(10분)입니다.

생성자 임시 공개 키는 빅 엔디안 형식의 ECIES 키입니다. 이는 IBGW 레이어와 응답 키 및 IV를 위한 KDF에 사용됩니다. 이것은 Inbound Tunnel Build 메시지의 평문 레코드에만 포함됩니다. 이 레이어에서는 빌드 레코드를 위한 DH가 없기 때문에 필수적입니다.

tunnel 구성 옵션은 [Common](/docs/specs/common-structures/)에서 정의된 Mapping 구조입니다. 현재 정의된 유일한 옵션은 대역폭 매개변수이며, API 0.9.65 기준으로 자세한 내용은 아래를 참조하세요. Mapping 구조가 비어있는 경우, 이는 0x00 0x00 두 바이트입니다. Mapping의 최대 크기(길이 필드 포함)는 98바이트이며, Mapping 길이 필드의 최대값은 96입니다.

#### 짧은 요청 레코드 암호화됨

임시 공개 키가 리틀 엔디안인 것을 제외하고 모든 필드는 빅 엔디안입니다.

암호화된 크기: 218바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### 짧은 빌드 응답 레코드

짧은 암호화된 BuildReplyRecord는 218바이트입니다.

#### 짧은 응답 레코드 암호화되지 않음

긴 레코드에서의 변경 사항 요약:

- 암호화되지 않은 길이를 512바이트에서 202바이트로 변경
- 암호화된 길이를 528바이트에서 218바이트로 변경

ECIES 응답은 ChaCha20/Poly1305로 암호화됩니다.

모든 필드는 빅 엔디안입니다.

암호화되지 않은 크기: 202바이트.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
tunnel build reply options은 [Common](/docs/specs/common-structures/)에서 정의된 Mapping 구조입니다. 현재 정의된 유일한 옵션은 대역폭 매개변수에 대한 것으로, API 0.9.65 기준이며, 자세한 내용은 아래를 참조하십시오. Mapping 구조가 비어있다면, 이는 두 바이트 0x00 0x00입니다. Mapping의 최대 크기(길이 필드 포함)는 201바이트이며, Mapping 길이 필드의 최대값은 199입니다.

응답 바이트는 핑거프린팅을 방지하기 위해 [Tunnel-Creation](/docs/specs/tunnel-creation/)에서 정의된 다음 값 중 하나입니다:

- 0x00 (수락)
- 30 (TUNNEL_REJECT_BANDWIDTH)

지원되지 않는 옵션에 대한 거부를 나타내기 위해 추가적인 응답 값이 향후 정의될 수 있습니다.

#### 짧은 응답 레코드 암호화

암호화된 크기: 218바이트

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

터널 빌드 레코드 암호화/복호화 후 Noise 상태에서 chaining key (ck)를 사용하여 다음 키들을 도출합니다: OBEP용 응답 키, AES 레이어 키, AES IV 키 및 garlic 응답 키/태그.

Reply keys: KDF가 OBEP와 non-OBEP hop에서 약간 다르다는 점을 주목하세요. long record와 달리 reply key에 ck의 왼쪽 부분을 사용할 수 없는데, 이는 마지막이 아니며 나중에 사용될 것이기 때문입니다. reply key는 AEAD/ChaCha20/Poly1305를 사용하여 해당 record를 암호화하고 ChaCha20을 사용하여 다른 record들에 reply하는 데 사용됩니다. 둘 다 동일한 키를 사용합니다. nonce는 0부터 시작하는 메시지 내 record의 위치입니다. 자세한 내용은 아래를 참조하세요.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
참고: OBEP에서 IV 키에 대한 KDF는 응답이 garlic encryption되지 않은 경우에도 다른 홉들과는 다릅니다.

#### 레코드 암호화

hop 자체의 응답 레코드는 ChaCha20/Poly1305로 암호화됩니다. 이는 위의 긴 레코드 사양과 동일하지만, 'n'이 항상 0이 아니라 레코드 번호 0-7이라는 점이 다릅니다. [RFC-7539](https://tools.ietf.org/html/rfc7539)를 참조하세요.

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
다른 레코드들은 각 홉에서 ChaCha20(ChaCha20/Poly1305가 아님)을 사용하여 반복적이고 대칭적으로 암호화됩니다. 이는 AES를 사용하고 레코드 번호를 사용하지 않는 위의 긴 레코드 사양과 다릅니다.

레코드 번호는 IV의 4바이트 위치에 배치됩니다. ChaCha20은 4-11바이트에 리틀 엔디안 논스가 있는 12바이트 IV를 사용하기 때문입니다. [RFC-7539](https://tools.ietf.org/html/rfc7539)를 참조하세요.

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

메시지의 garlic 래핑은 OBEP(인바운드 빌드의 경우) 또는 IBGW(아웃바운드 빌드의 경우)로부터 메시지를 숨깁니다. 이는 권장되지만 필수는 아닙니다. OBEP와 IBGW가 같은 router인 경우에는 필요하지 않습니다.

생성자가 ECIES IBGW에 암호화하여 전송하는 인바운드 Short Tunnel Build Message의 garlic encryption은 [ECIES-ROUTERS](/docs/specs/ecies-routers/)에 정의된 대로 Noise 'N' 암호화를 사용합니다.

OBEP에 의한 Outbound Tunnel Build Reply Message의 garlic encryption은 생성자에게 암호화되며, 위 KDF에서 생성된 32바이트 garlic reply key와 8바이트 garlic reply tag를 사용하는 기존 세션 메시지를 사용합니다. 형식은 [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), 그리고 [ECIES-X25519](/docs/specs/ecies/)의 Database Lookups에 대한 응답으로 지정된 것과 같습니다.

#### 레이어 암호화

이 사양서는 빌드 요청 레코드에 레이어 암호화 타입 필드를 포함합니다. 현재 지원되는 유일한 레이어 암호화는 타입 0이며, 이는 AES입니다. 이는 레이어 키와 IV 키가 빌드 요청 레코드에 포함되지 않고 위의 KDF에서 파생된다는 점을 제외하면 이전 사양서와 동일합니다.

예를 들어 ChaCha20과 같은 새로운 계층 암호화 유형을 추가하는 것은 추가 연구 주제이며, 현재 이 명세서의 일부가 아닙니다.

## 구현 참고사항

- 오래된 router들은 홉의 암호화 타입을 확인하지 않고 ElGamal로 암호화된 레코드를 전송합니다. 일부 최신 router들은 버그가 있어서 다양한 형태의 잘못된 레코드를 전송합니다. 구현자들은 CPU 사용량을 줄이기 위해 가능하면 DH 연산 이전에 이러한 레코드를 감지하고 거부해야 합니다.

### 빌드 기록

빌드 레코드 순서는 무작위화되어야 하므로, 중간 홉들은 tunnel 내에서 자신의 위치를 알 수 없습니다.

권장되는 최소 빌드 레코드 수는 4개입니다. 홉보다 더 많은 빌드 레코드가 있는 경우, 랜덤 또는 구현별 데이터를 포함하는 "가짜" 레코드를 추가해야 합니다. 인바운드 tunnel 빌드의 경우, 올바른 16바이트 해시 접두사와 실제 X25519 임시 키를 가진 원래 router에 대한 "가짜" 레코드가 항상 하나 있어야 합니다. 그렇지 않으면 가장 가까운 홉이 다음 홉이 발신자임을 알게 됩니다.

"가짜" 레코드의 나머지 부분은 랜덤 데이터이거나, 발신자가 빌드에 대한 데이터를 자신에게 보내기 위해 임의의 형식으로 암호화될 수 있으며, 이는 아마도 대기 중인 빌드에 대한 저장 요구사항을 줄이기 위한 것일 수 있습니다.

인바운드 tunnel의 발신자는 이전 홉에서 자신의 "가짜" 레코드가 수정되지 않았음을 검증하는 방법을 사용해야 합니다. 이는 익명성 해제에도 사용될 수 있기 때문입니다. 발신자는 레코드의 체크섬을 저장하고 검증하거나, 레코드에 체크섬을 포함하거나, AEAD 암호화/복호화 함수를 사용할 수 있으며, 이는 구현에 따라 달라집니다. 16바이트 해시 접두사나 기타 빌드 레코드 내용이 수정된 경우, router는 해당 tunnel을 폐기해야 합니다.

아웃바운드 tunnel의 가짜 레코드와 인바운드 tunnel의 추가 가짜 레코드는 이러한 요구사항이 없으며, 어떤 홉에도 보이지 않으므로 완전히 무작위 데이터일 수 있습니다. 그러나 발신자가 이들이 수정되지 않았음을 검증하는 것은 여전히 바람직할 수 있습니다.

## Tunnel 대역폭 매개변수

### 개요

지난 몇 년간 새로운 프로토콜, 암호화 유형, 혼잡 제어 개선을 통해 네트워크 성능을 향상시키면서, 비디오 스트리밍과 같은 더 빠른 애플리케이션이 가능해지고 있습니다. 이러한 애플리케이션들은 클라이언트 tunnel의 각 홉에서 높은 대역폭을 필요로 합니다.

그러나 참여하는 router들은 tunnel 구축 메시지를 받을 때 해당 tunnel이 얼마나 많은 대역폭을 사용할지에 대한 정보를 가지고 있지 않습니다. 이들은 모든 참여 tunnel들이 사용하는 현재 총 대역폭과 참여 tunnel들에 대한 총 대역폭 제한을 기반으로만 tunnel을 수락하거나 거부할 수 있습니다.

요청하는 router들은 각 홉에서 얼마나 많은 대역폭이 사용 가능한지에 대한 정보도 가지고 있지 않습니다.

또한, router들은 현재 tunnel에서 인바운드 트래픽을 제한할 방법이 없습니다. 이는 서비스의 과부하나 DDoS 공격 시에 매우 유용할 것입니다.

tunnel 구축 요청 및 응답 메시지의 tunnel 대역폭 매개변수는 이러한 기능에 대한 지원을 추가합니다. 추가 배경 정보는 [Prop168](/proposals/168/)을 참조하세요. 이러한 매개변수는 API 0.9.65부터 정의되었지만, 구현에 따라 지원이 달라질 수 있습니다. 긴 ECIES 구축 레코드와 짧은 ECIES 구축 레코드 모두에 대해 지원됩니다.

### 빌드 요청 옵션

다음 세 가지 옵션은 레코드의 tunnel 구축 옵션 매핑 필드에 설정될 수 있습니다: 요청하는 router는 이 중 일부, 전부, 또는 아무것도 포함하지 않을 수 있습니다.

- m := 이 tunnel에 필요한 최소 대역폭 (문자열로 된 KBps 양의 정수)
- r := 이 tunnel에 요청된 대역폭 (문자열로 된 KBps 양의 정수)
- l := 이 tunnel의 대역폭 제한; IBGW에만 전송됨 (문자열로 된 KBps 양의 정수)

제약 조건: m <= r <= l

참여하는 router는 "m"이 지정되었지만 최소한 그만큼의 대역폭을 제공할 수 없는 경우 tunnel을 거부해야 합니다.

요청 옵션은 해당하는 암호화된 빌드 요청 레코드에서 각 참여자에게 전송되며, 다른 참여자들에게는 보이지 않습니다.

### 빌드 응답 옵션

다음 옵션은 응답이 ACCEPTED일 때 레코드의 tunnel build reply options 매핑 필드에 설정될 수 있습니다:

- b := 이 tunnel에 사용 가능한 대역폭 (문자열로 표현된 양의 정수 KBps)

제약조건: b >= m

참여하는 router는 빌드 요청에서 "m" 또는 "r"이 지정된 경우 이를 포함해야 합니다. 값은 지정된 경우 "m" 값 이상이어야 하지만, "r" 값이 지정된 경우 그보다 작거나 클 수 있습니다.

참여하는 router는 터널을 위해 최소한 이 정도의 대역폭을 예약하고 제공하려고 시도해야 하지만, 이것이 보장되지는 않습니다. Router들은 10분 후의 상황을 예측할 수 없으며, 참여 트래픽은 router 자체의 트래픽과 tunnel들보다 낮은 우선순위를 가집니다.

Router는 필요한 경우 사용 가능한 대역폭을 초과 할당할 수도 있으며, tunnel의 다른 홉에서 이를 거부할 수 있으므로 이는 아마도 바람직할 것입니다.

이러한 이유로 참여하는 router의 응답은 최선의 노력을 다한 약속으로 취급되어야 하지만, 보장은 아닙니다.

응답 옵션은 해당하는 암호화된 빌드 응답 레코드에서 요청하는 router로 전송되며, 다른 참가자들에게는 보이지 않습니다.

### 구현 참고사항

대역폭 매개변수는 tunnel 계층에서 참여하는 router들에서 보이는 것으로, 즉 초당 고정 크기 1KB tunnel 메시지의 개수입니다. Transport (NTCP2 또는 SSU2) 오버헤드는 포함되지 않습니다.

이 대역폭은 클라이언트에서 보이는 대역폭보다 훨씬 많거나 적을 수 있습니다. Tunnel 메시지에는 ratchet과 스트리밍을 포함한 상위 계층의 오버헤드를 포함하여 상당한 오버헤드가 포함됩니다. 스트리밍 ack과 같은 간헐적인 소규모 메시지는 각각 1KB로 확장됩니다. 그러나 I2CP 계층에서의 gzip 압축은 대역폭을 상당히 줄일 수 있습니다.

요청하는 router에서 가장 간단한 구현 방법은 풀의 현재 tunnel들의 평균, 최소, 그리고/또는 최대 대역폭을 사용하여 요청에 포함할 값들을 계산하는 것입니다. 더 복잡한 알고리즘도 가능하며 이는 구현자에게 달려있습니다.

현재 클라이언트가 router에게 필요한 대역폭을 알려주기 위해 정의된 I2CP 또는 SAM 옵션은 없으며, 여기서도 새로운 옵션을 제안하지 않습니다. 필요한 경우 나중에 옵션이 정의될 수 있습니다.

구현체들은 사용 가능한 대역폭이나 기타 데이터, 알고리즘, 로컬 정책, 또는 로컬 구성을 사용하여 빌드 응답에서 반환되는 대역폭 값을 계산할 수 있습니다.

## 참고 자료

- [Common](/docs/specs/common-structures/)
- [암호학](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [다중 암호화](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Tunnel 생성](/docs/specs/tunnel-creation/)
