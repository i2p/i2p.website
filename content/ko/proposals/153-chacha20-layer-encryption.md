---
title: "ChaCha 터널 레이어 암호화"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## 개요

이 제안서는 제안서 152: ECIES 터널의 변경 사항을 기반으로 하며 이를 필요로 합니다.

ECIES-X25519 터널에 대한 BuildRequestRecord 형식을 지원하는 홉을 통해 구축된 터널만 이 사양을 구현할 수 있습니다.

이 사양은 터널 레이어 암호화 유형을 나타내고, 레이어 AEAD 키 전송을 위한 터널 빌드 옵션 형식을 필요로 합니다.

### 목표

이 제안서의 목표는 다음과 같습니다:

- 확립된 터널 IV 및 레이어 암호화를 위해 AES256/ECB+CBC를 ChaCha20으로 대체
- 홉 간 AEAD 보호를 위해 ChaCha20-Poly1305 사용
- 비터널 참가자에 의해 기존 터널 레이어 암호화로부터 탐지되지 않음
- 전체 터널 메시지 길이에 대한 변경 없음

### 확립된 터널 메시지 처리

이 섹션은 다음의 변경 사항을 설명합니다:

- 아웃바운드 및 인바운드 게이트웨이 전처리 및 암호화
- 참가자 암호화 및 후처리
- 아웃바운드 및 인바운드 엔드포인트 암호화 및 후처리

현재 터널 메시지 처리에 대한 개요는 [Tunnel Implementation](/docs/tunnels/implementation/) 사양을 참조하십시오.

ChaCha20 레이어 암호화를 지원하는 라우터에 대한 변경만 논의합니다.

혼합 터널에서 AES 레이어 암호화에 대한 변경은 고려하지 않습니다. 안전한 프로토콜이 마련되기 전까지 128비트 AES IV를 64비트 ChaCha20 nonce로 변환하는 것이 필요합니다. 블룸 필터가 전체 IV의 고유성을 보장하지만, 고유 IV의 첫 번째 절반은 동일할 수 있습니다.

이는 레이어 암호화가 터널의 모든 홉에 대해 균일해야 하며, 터널 생성 과정에서 터널 빌드 옵션을 사용하여 확립되어야 함을 의미합니다.

모든 게이트웨이 및 터널 참가자는 두 개의 독립된 nonce의 유효성을 검사하기 위한 블룸 필터를 유지해야 합니다.

이 제안서 전반에 걸쳐 언급된 ``nonceKey``는 AES 레이어 암호화에서 사용되는 ``IVKey``를 대신합니다. 이는 제안서 152의 동일한 KDF를 사용하여 생성됩니다.

### 홉 간 메시지의 AEAD 암호화

각 연속적인 홉 쌍에 대해 고유한 ``AEADKey``가 추가로 생성되어야 합니다.
이 키는 연속적인 홉 간에 ChaCha20-Poly1305 암호화 및 암호 해독에 사용됩니다.

터널 메시지는 Poly1305 MAC을 수용하기 위해 내부 암호화 프레임의 길이를 16바이트 줄여야 합니다.

메시지에 직접 AEAD를 사용할 수 없으며, 이는 아웃바운드 터널에 의해 필요한 반복적인 암호 해독이 필요하기 때문입니다.
반복적인 암호 해독은 이제 사용하는 방식으로 ChaCha20으로만 달성할 수 있습니다.

```text
+----+----+----+----+----+----+----+----+
  |    Tunnel ID      |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | tunnelNonce cont. |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  |  obfsNonce cont.  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Encrypted Data              +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  Tunnel ID :: `TunnelId`
         4 bytes
         다음 홉의 ID

  tunnelNonce ::
         8 bytes
         터널 레이어 nonce

  obfsNonce ::
         8 bytes
         터널 레이어 nonce 암호화 nonce

  Encrypted Data ::
         992 bytes
         암호화된 터널 메시지

  Poly1305 MAC ::
         16 bytes

  total size: 1028 Bytes
```

내부 홉(선행 및 후속 홉 포함)은 이전 홉의 AEAD 레이어를 암호 해독하고 다음 홉에 AEAD 레이어를 암호화하기 위해 두 개의 ``AEADKeys``를 갖게 됩니다.

모든 내부 홉 참가자는 BuildRequestRecords에 64바이트 추가 키 자료를 포함합니다.

아웃바운드 엔드포인트와 인바운드 게이트웨이는 서로 간의 메시지를 터널 레이어로 암호화하지 않기 때문에 추가적인 32바이트의 키데이터만 필요합니다.

아웃바운드 게이트웨이는 ``outAEAD`` 키를 생성하며, 이는 첫 번째 아웃바운드 홉의 ``inAEAD`` 키와 동일합니다.

인바운드 엔드포인트는 ``inAEAD`` 키를 생성하며, 이는 최종 인바운드 홉의 ``outAEAD`` 키와 동일합니다.

내부 홉은 수신 메시지를 AEAD 암호 해독하고 발신 메시지를 암호화하기 위해 사용될 ``inAEADKey`` 및 ``outAEADKey``를 수신합니다.

예를 들어, OBGW, A, B, OBEP와 같은 터널의 내부 홉에서는:

- A의 ``inAEADKey``는 OBGW의 ``outAEADKey``와 동일합니다.
- B의 ``inAEADKey``는 A의 ``outAEADKey``와 동일합니다.
- B의 ``outAEADKey``는 OBEP의 ``inAEADKey``와 동일합니다.

키는 홉 쌍 간에 고유합니다. 따라서 OBEP의 ``inAEADKey``는 A의 ``inAEADKey``와 다르고,
A의 ``outAEADKey``는 B의 ``outAEADKey``와 다릅니다.

### 게이트웨이 및 터널 생성 프로세스

게이트웨이는 지침-프래그먼트 프레임 후에 Poly1305 MAC을 위해 공간을 예약하여 메시지를 동일한 방식으로 분할하고 번들할 것입니다.

AEAD 프레임(및 MAC 포함)을 포함하는 내부 I2NP 메시지는 프래그먼트에 걸쳐 분할될 수 있지만,
드롭된 프래그먼트는 엔드포인트에서 AEAD 암호화 해제 실패(MAC 검증 실패)로 이어질 것입니다.

### 게이트웨이 전처리 및 암호화

터널이 ChaCha20 레이어 암호화를 지원할 때, 게이트웨이는 메시지 세트당 두 개의 64비트 nonce를 생성합니다.

인바운드 터널:

- IV 및 터널 메시지(들) ChaCha20으로 암호화하기
- 터널 수명의 ``tunnelNonce``와 ``obfsNonce`` 8바이트 사용
- ``tunnelNonce`` 암호화를 위한 8바이트 ``obfsNonce`` 사용
- 2^(64 - 1) - 1개의 메시지 세트 전의 터널 파괴: 2^63 - 1 = 9,223,372,036,854,775,807

  - 64비트 nonce의 충돌을 피하기 위한 nonce 제한
  - 이론적으로 도달할 수 불가능한 nonce 제한, 이는 약 ~15,372,286,728,091,294 메시지/초 동안 10분 터널에 걸쳐 있습니다.

- 기대되는 요소 수에 따라 블룸 필터 조정 (128 메시지/초, 1024 메시지/초? TBD)

터널의 인바운드 게이트웨이(IBGW)는 다른 터널의 아웃바운드 엔드포인트(OBEP)로부터 수신된 메시지를 처리합니다.

이 시점에서는, 가장 바깥쪽 메시지 레이어는 포인트-투-포인트 전송 암호화를 사용하여 암호화되어 있습니다.
I2NP 메시지 헤더는 터널 레이어에서 OBEP와 IBGW에 보입니다.
내부 I2NP 메시지는 종단간 세션 암호화를 사용하여 통합갈릭 마늘에 래핑되어 있습니다.

IBGW는 메시지를 적절히 형식화된 터널 메시지로 전처리하고, 다음과 같이 암호화합니다:

```text

// IBGW는 블룸 필터에서의 충돌을 피하기 위한 랜덤 nonce를 생성합니다.
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // IBGW는 터널 nonce 및 레이어 키를 사용하여 전처리된 터널 메시지 각각을 ChaCha20으로 암호화합니다.
  encMsg = ChaCha20(msg = 터널 msg, 숫자다리를 터널 nonce, 키 = 레이어 키)

  // ChaCha20-Poly1305 각 메시지의 암호화된 데이터 프레임을 터널 nonce 및 outAEADKey로 암호화합니다.
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

터널 메시지 형식은 16바이트 IV 대신 두 개의 8바이트 nonce를 사용하여 약간 변경될 것입니다.
nonce 암호화를 위해 사용되는 ``obfsNonce``는 8바이트 ``tunnelNonce``에 추가되어,
각 홉은 암호화된 ``tunnelNonce`` 및 홉의 ``nonceKey``를 사용하여 암호화합니다.

동작 예측된 각각의 홉에 대한 메시지 세트의 선암호 해독이 종료된 후, 아웃바운드 게이트웨이는
각 터널 메시지의 암호문 부분을 ``tunnelNonce`` 및 초기 홉의 ``outAEADKey``를 사용하여
ChaCha20-Poly1305 AEAD 암호화합니다.

아웃바운드 터널들:

- 터널 메시지 반복 해독하기
- ChaCha20-Poly1305 터널 메시지 암호화된 프레임의 선암호 해독
- 인바운드 터널과 동일한 레이어 nonce 규칙 사용
- 전송된 터널 메시지 세트당 무작위 nonce 생성하기

```text


// 메시지 세트당 고유하고 무작위 nonce를 생성하기
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // 각 홉에 대해, 이전 터널 nonce를 홉의 IV 키로 ChaCha20 처리
  tunnelNonce = ChaCha20(msg = 이전 터널 nonce, 숫자다리를 obfsNonce, 키 = 홉의 nonceKey)

  // 각 홉에 대해, 터널 메시지를 홉의 터널 nonce 및 레이어 키로 ChaCha20 "해독"하기
  decMsg = ChaCha20(msg = 터널 msg(s), 숫자다리를 tunnelNonce, 키 = 홉의 layerKey)

  // 각 홉에 대해, obfsNonce를 홉의 암호화된 tunnelNonce 및 nonceKey로 ChaCha20 "해독"하기
  obfsNonce = ChaCha20(msg = obfsNonce, 숫자다리를 tunnelNonce, 키 = 홉의 nonceKey)

  // 홉 처리 후, ChaCha20-Poly1305 각 터널 메시지의 "해독"된 데이터 프레임을 첫 번째 홉의 암호화된 tunnelNonce 및 inAEADKey로 암호화
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, 숫자다리를 첫 번째 홉의 암호화된 tunnelNonce, 키 = 첫 번째 홉의 inAEADKey / GW outAEADKey)
```

### 참가자 처리

참가자는 각각의 수신 nonce의 고유성을 위해 소멸하는 블룸 필터로 처리 메시지를 추적할 것입니다.

각 홉에서 터널 nonce를 한 번씩 암호화해야 합니다. 이는 비연속적 콜루징 홉들에 의해 발생할 수 있는 확인 공격을 방지하기 위한 조치입니다.

홉은 수신된 nonce를 암호화하여 이전 및 이후 홉 간의 확인 공격을 방지합니다. 이는 비연속적 콜루징 홉들 사이에서 터널에 속한지 여부를 알 수 있는 것을 방지합니다.

수신된 ``tunnelNonce`` 및 ``obfsNonce``를 검증하기 위해서 참가자는 각각의 nonce를 블룸 필터에서 중복으로 확인합니다.

검증 후, 참가자는 다음을 수행합니다:

- 각 터널 메시지의 AEAD 암호화된 데이터 프레임을 수신된 ``tunnelNonce`` 및 ``inAEADKey``로 ChaCha20-Poly1305 해독합니다.
- 수신된 ``obfsNonce`` 및 암호화된 ``tunnelNonce``와 함께 ``nonceKey``를 사용하여 ``tunnelNonce``를 ChaCha20으로 암호화합니다.
- 암호화된 ``tunnelNonce`` 및 루프의 ``layerKey``를 사용하여 각 터널 메시지의 암호화된 데이터 프레임을 ChaCha20으로 암호화합니다.
- 암호화된 ``tunnelNonce`` 및 루프의 ``outAEADKey``를 사용하여 각 터널 메시지의 암호화된 데이터 프레임을 ChaCha20-Poly1305로 암호화합니다.
- 암호화된 ``tunnelNonce`` 및 루프의 ``nonceKey``와 함께 ``obfsNonce``를 ChaCha20으로 암호화합니다.
- 다음 홉에 {``nextTunnelId``, 암호화된 (``tunnelNonce`` || ``obfsNonce``), AEAD 암호문 || MAC} 튜플을 전송합니다.

```text

// 확인을 위해, 터널 홉들은 수신된 각각의 nonce의 고유성을 블룸 필터에서 확인해야 합니다.
  // 확인 후, ChaCha20-Poly1305 터널 메시지의 암호화된 프레임을 힌트하여 AEAD 프레임을 해제합니다
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = 수신된 encMsg \|\| MAC, 숫자다리를 수신된 tunnelNonce, 키 = inAEADKey)

  // obfsNonce와 루프의 nonceKey를 사용하여 tunnelNonce를 ChaCha20으로 암호화합니다.
  tunnelNonce = ChaCha20(msg = 수신된 tunnelNonce, 숫자다리를 수신된 obfsNonce, 키 = nonceKey)

  // 터널 메시지의 암호화된 데이터 프레임을 터널 nonce 및 홉의 레이어 키로 ChaCha20 암호화합니다.
  encMsg = ChaCha20(msg = encTunMsg, 숫자다리를 tunnelNonce, 키 = layerKey)

  // AEAD 보호를 위해, 또한 터널 메시지의 암호화된 데이터 프레임을 ChaCha20-Poly1305로 암호화합니다.
  // 암호화된 터널 nonce 및 홉의 outAEADKey로.
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, 숫자다리를 tunnelNonce, 키 = outAEADKey)

  // 고속 nonce 및 홉의 nonceKey와 함께 수신된 obfsNonce를 ChaCha20으로 암호화합니다.
  obfsNonce = ChaCha20(msg = obfsNonce, 숫자다리를 tunnelNonce, 키 = nonceKey)
```

### 인바운드 엔드포인트 처리

ChaCha20 터널에 대해서는, 다음 체계를 사용하여 각 터널 메시지를 해독합니다:

- 수신된 ``tunnelNonce`` 및 ``obfsNonce``를 블룸 필터에 대해 독립적으로 확인합니다.
- 수신된 ``tunnelNonce`` 및 ``inAEADKey``을 사용하여 암호화된 데이터 프레임을 ChaCha20-Poly1305 해독합니다.
- 수신된 ``tunnelNonce`` 및 홉의 ``layerKey``를 사용하여 암호화된 데이터 프레임을 ChaCha20 해독합니다.
- 홉의 ``nonceKey`` 및 수신된 ``tunnelNonce``를 사용하여 ``obfsNonce``를 ChaCha20 해독하여 이전 ``obfsNonce``를 얻습니다.
- 홉의 ``nonceKey`` 및 해독된 ``obfsNonce``를 사용하여 수신된 ``tunnelNonce``를 ChaCha20 해독하여 이전 ``tunnelNonce``를 얻습니다.
- 해독된 ``tunnelNonce`` 및 이전 홉의 ``layerKey``를 사용하여 암호화된 데이터를 ChaCha20 해독합니다.
- 터널의 각 홉에 대한 nonce 및 레이어 해독을 반복하여 IBGW로 돌아옵니다.
- AEAD 프레임 해독은 첫 번째 라운드에서만 필요합니다.

```text

// 첫 번째 라운드의 경우, ChaCha20-Poly1305로 각 메시지의 암호화된 데이터 프레임 + MAC을 해독
  msg = encTunMsg \|\| MAC
  tunnelNonce = 수신된 tunnelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, 숫자다리를 tunnelNonce, 키 = inAEADKey)

  // 터널의 각 홉에 대해 IBGW로 되감는 동안 반복
  // 각 라운드에 대해, 각 메시지의 암호화된 데이터 프레임에서 홉의 레이어 암호화를 ChaCha20으로 해독
  // 각 홉에 대해 이전 라운드의 해독된 터널 nonce로 수신된 터널 nonce를 교체
  decMsg = ChaCha20(msg = encTunMsg, 숫자다리를 tunnelNonce, 키 = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, 숫자다리를 tunnelNonce, 키 = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, 숫자다리를 obfsNonce, 키 = nonceKey)
```

### ChaCha20+ChaCha20-Poly1305 터널 레이어 암호화에 대한 보안 분석

AES256/ECB+AES256/CBC에서 ChaCha20+ChaCha20-Poly1305로 전환함으로써 다양한 이점과 새로운 보안 고려사항이 발생합니다.

가장 중요한 보안 고려사항은 ChaCha20와 ChaCha20-Poly1305 nonce가 사용되는 동안 매 메시지마다 고유해야 한다는 것입니다.

동일한 키를 사용하여 다른 메시지에 고유하지 않은 nonce를 사용하면 ChaCha20과 ChaCha20-Poly1305가 손상됩니다.

``obfsNonce``를 추가하면, 각 홉의 레이어 암호화를 위해 IBEP가 ``tunnelNonce``를 해독하여 이전 nonce를 복구할 수 있습니다.

``tunnelNonce``와 함께 ``obfsNonce``는 터널 홉에 새로운 정보를 노출하지 않으므로, ``obfsNonce``는 암호화된 ``tunnelNonce``로 암호화되기 때문입니다.
이를 통해 IBEP는 이전 ``obfsNonce``를 복구할 수도 있습니다.

가장 큰 보안 장점은 ChaCha20에 대한 확인 또는 오라클 공격이 없으며, 홉 간 ChaCha20-Poly1305를 사용하면
바깥 대역 MitM 공격자로부터의 암호문 조작에 대한 AEAD 보호가 추가됩니다.

터널 레이어 암호화에서 키가 재사용될 때, AES256/ECB + AES256/CBC에 대한 실제적인 오라클 공격이 가능합니다.

AES256/ECB에 대한 오라클 공격은 두 번의 암호화가 사용되고 암호화는 단일 블록(터널 IV)에 적용되기 때문에 작동하지 않습니다.

AES256/CBC에 대한 패딩 오라클 공격은 패딩을 사용하지 않기 때문에 작동하지 않습니다. 만약 터널 메시지 길이가 비-모드-16 길이로 변경되더라도, 중복 IV가 거부되기 때문에 AES256/CBC는 여전히 취약하지 않습니다.

두 공격 또한 같은 IV를 사용한 다중 오라클 호출을 허용하지 않음으로 인해 차단됩니다. 이는 중복 IV가 거부되기 때문입니다.

## 참고 문헌

* [Tunnel-Implementation](/docs/tunnels/implementation/)
