---
title: "Tunnel 메시지 명세"
description: "I2P에서 tunnel 메시지 형식에 대한 사양"
slug: "tunnel-message"
aliases:
  - "/ko/docs/legacy/tunnel-message"
  - "/ko/docs/legacy/tunnel-message/"
  - "/ko/tunnel_message_spec"
  - "/ko/tunnel_message_spec/"
category: "설계"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## 개요

이 문서는 tunnel 메시지의 형식을 명시합니다. tunnel에 대한 일반적인 정보는 [tunnel 문서](/docs/specs/tunnel-implementation)를 참조하세요.

## 메시지 전처리

*tunnel gateway*는 터널의 입구이자 첫 번째 홉입니다. 아웃바운드 터널의 경우, gateway는 터널의 생성자입니다. 인바운드 터널의 경우, gateway는 터널 생성자의 반대편 끝에 위치합니다.

게이트웨이는 [I2NP](/docs/specs/i2np) 메시지를 조각화하고 tunnel 메시지로 결합하여 *전처리*합니다.

I2NP 메시지는 0부터 거의 64KB까지 가변 크기인 반면, tunnel 메시지는 약 1KB의 고정 크기입니다. 고정된 메시지 크기는 메시지 크기 관찰로부터 가능한 여러 유형의 공격을 제한합니다.

tunnel 메시지가 생성된 후, [tunnel 문서](/docs/specs/tunnel-implementation)에 설명된 대로 암호화됩니다.

### Tunnel 메시지 (암호화됨)

다음은 암호화 후 tunnel 데이터 메시지의 내용입니다.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4바이트. 다음 홉의 ID, 0이 아님.

**IV** :: : 16바이트. 초기화 벡터.

**Encrypted Data** :: : 1008바이트. 암호화된 tunnel 메시지.

**전체 크기: 1028바이트**

### Tunnel 메시지 (복호화됨)

이는 복호화된 tunnel 데이터 메시지의 내용입니다.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4바이트. 다음 홉의 ID, 0이 아님.

**IV** :: : 16바이트. 초기화 벡터.

**Checksum** :: : 4바이트. (메시지 내용(0바이트 이후) + IV)의 SHA256 해시의 첫 4바이트.

**Nonzero padding** :: : 0개 이상의 바이트. 패딩을 위한 랜덤한 0이 아닌 데이터.

**Zero** :: : 1바이트. 값 0x00.

**전송 지시사항** :: TunnelMessageDeliveryInstructions : 길이는 다양하지만 일반적으로 7, 39, 43, 또는 47바이트입니다. 프래그먼트와 프래그먼트의 라우팅을 나타냅니다.

**메시지 조각** :: : 1~996바이트, 실제 최대값은 전달 지시 크기에 따라 달라집니다. 부분 또는 전체 I2NP Message입니다.

**전체 크기: 1028 바이트**

#### 참고 사항

- 패딩이 있는 경우, 지시/메시지 쌍 앞에 위치해야 합니다. 끝에 패딩을 넣을 수 있는 규정은 없습니다.
- 체크섬은 패딩이나 제로 바이트를 포함하지 않습니다. 첫 번째 전달 지시부터 시작하는 메시지를 가져와서 IV를 연결하고, 그것의 해시를 계산합니다.

## Tunnel 메시지 전달 지침

명령어는 단일 제어 바이트로 인코딩되며, 필요한 추가 정보가 뒤따릅니다. 해당 제어 바이트의 첫 번째 비트(MSB)는 헤더의 나머지 부분을 어떻게 해석할지 결정합니다 - 설정되지 않은 경우, 메시지는 단편화되지 않았거나 메시지의 첫 번째 조각입니다. 설정된 경우, 이는 후속 조각입니다.

이 사양은 Tunnel Message 내부의 Delivery Instructions에만 적용됩니다. "Delivery Instructions"는 Garlic Clove 내부에서도 사용되지만, 그 형식은 상당히 다릅니다. 자세한 내용은 [I2NP 문서](/docs/specs/i2np#garlicclovedeliveryinstructions)를 참조하십시오. Garlic Clove Delivery Instructions에는 다음 사양을 사용하지 마십시오!

### 첫 번째 조각 전송 지침

첫 번째 바이트의 MSB가 0인 경우, 이는 초기 I2NP 메시지 조각이거나 완전한(조각화되지 않은) I2NP 메시지이며, 지시사항은 다음과 같습니다:

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1바이트. 비트 순서: 76543210   - 비트 7: 초기 조각 또는 조각화되지 않은 메시지를 지정하기 위해 0   - 비트 6-5: 전송 유형

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4: 지연 포함됨? 구현되지 않음, 항상 0. 1인 경우, 지연 바이트가 포함됨.
  - bit 3: 단편화됨? 0인 경우, 메시지가 단편화되지 않았으며, 뒤따르는 것이 전체 메시지임. 1인 경우, 메시지가 단편화되었으며, 지시사항에 Message ID가 포함됨.
  - bit 2: 확장 옵션? 구현되지 않음, 항상 0. 1인 경우, 확장 옵션이 포함됨.
  - bits 1-0: 예약됨, 향후 사용과의 호환성을 위해 0으로 설정

**Tunnel ID** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4바이트. 선택사항, 전송 유형이 TUNNEL인 경우에만 존재. 목적지 tunnel ID, 0이 아님.

**To Hash** :: : 32바이트. 선택사항, 배송 유형이 ROUTER 또는 TUNNEL인 경우 존재. ROUTER인 경우, router의 SHA256 해시. TUNNEL인 경우, 게이트웨이 router의 SHA256 해시.

**Delay** :: : 1바이트. 선택적, delay included 플래그가 설정된 경우 존재함. tunnel 메시지에서: 구현되지 않음, 절대 존재하지 않음; 원래 사양: 비트 7: 유형 (0 = strict, 1 = randomized), 비트 6-0: 지연 지수 (2^값 분).

**Message ID** :: : 4바이트. 선택사항으로, 이 메시지가 2개 이상의 조각 중 첫 번째인 경우에만 존재합니다 (즉, fragmented 비트가 1인 경우). 모든 조각이 단일 메시지에 속한다는 것을 고유하게 식별하는 ID입니다 (현재 구현에서는 I2NPMessageHeader.msg_id를 사용).

**확장 옵션** :: : 2바이트 이상. 선택사항으로, 확장 옵션 플래그가 설정된 경우에만 존재합니다. 구현되지 않음, 절대 존재하지 않음; 원래 사양: 1바이트 길이와 그만큼의 바이트.

**size** :: : 2바이트. 뒤따르는 fragment의 길이. 유효한 값: tunnel 메시지에서 1부터 약 960까지.

**총 길이:** 일반적인 길이는: - LOCAL 전달(tunnel 메시지)의 경우 3바이트 - ROUTER 전달의 경우 35바이트 또는 TUNNEL 전달(조각화되지 않은 tunnel 메시지)의 경우 39바이트 - ROUTER 전달의 경우 39바이트 또는 TUNNEL 전달(첫 번째 조각)의 경우 43바이트

### 후속 프래그먼트 전달 지침

첫 번째 바이트의 MSB가 1이면, 이는 후속 프래그먼트이며, 지시사항은 다음과 같습니다:

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1바이트. 비트 순서: 76543210. 이진수 1nnnnnnd:   - 비트 7: 이것이 후속 프래그먼트임을 나타내는 1   - 비트 6-1: nnnnnn은 1부터 63까지의 6비트 프래그먼트 번호   - 비트 0: d는 마지막 프래그먼트를 나타내는 1, 그렇지 않으면 0

**Message ID** :: : 4바이트. 이 fragment가 속한 fragment 시퀀스를 식별합니다. 이것은 초기 fragment(플래그 비트 7이 0으로 설정되고 플래그 비트 3이 1로 설정된 fragment)의 message ID와 일치합니다.

**size** :: : 2바이트. 뒤따르는 프래그먼트의 길이. 유효한 값: 1~996.

**전체 길이: 7바이트**

## 참고 사항

### I2NP 메시지 최대 크기

최대 I2NP 메시지 크기는 명목상 64 KB이지만, I2NP 메시지를 여러 개의 1 KB tunnel 메시지로 분할하는 방법에 의해 크기가 더욱 제한됩니다. 최대 분할 수는 64개이며, 초기 분할은 tunnel 메시지의 시작 부분에 완벽하게 정렬되지 않을 수 있습니다. 따라서 메시지는 명목상 63개 분할에 맞아야 합니다.

초기 fragment의 최대 크기는 956바이트입니다(TUNNEL 전송 모드 가정); 후속 fragment의 최대 크기는 996바이트입니다. 따라서 최대 크기는 대략 956 + (62 * 996) = 62708바이트, 즉 61.2KB입니다.

### 순서 지정, 배치, 패킹

Tunnel 메시지는 드롭되거나 재정렬될 수 있습니다. Tunnel 메시지를 생성하는 tunnel gateway는 I2NP 메시지를 조각화하고 조각들을 tunnel 메시지에 효율적으로 패킹하기 위해 어떤 배치, 믹싱 또는 재정렬 전략이든 자유롭게 구현할 수 있습니다. 일반적으로 최적의 패킹은 불가능합니다("패킹 문제"). Gateway들은 다양한 지연 및 재정렬 전략을 구현할 수 있습니다.

### 커버 트래픽

Tunnel 메시지는 커버 트래픽을 위해 패딩만 포함할 수 있습니다 (즉, 전달 지시사항이나 메시지 조각이 전혀 없음). 이는 구현되지 않았습니다.

## 참고 자료

- **[I2NP]** [I2NP Protocol](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [터널 구현](/docs/specs/tunnel-implementation)
