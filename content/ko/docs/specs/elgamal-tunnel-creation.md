---
title: "터널 생성 사양 (ElGamal)"
description: "X25519로 대체된 레거시 ElGamal 기반 tunnel 구축 사양"
slug: "elgamal-tunnel-creation"
aliases:
  - "/ko/tunnel-alt-creation"
  - "/ko/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 개요 {#tunnelcreate-overview}

참고: 사용 중단됨 - 이것은 ElGamal tunnel 구축 사양입니다. 현재 방법은 [X25519 tunnel 구축 사양](/docs/specs/tunnel-creation-ecies)을 참조하세요.

이 문서는 "비대화형 망원경" 방식을 사용하여 터널을 생성하는 데 사용되는 암호화된 터널 구축 메시지의 세부 사항을 명시합니다. 피어 선택 및 순서 지정 방법을 포함한 프로세스 개요는 터널 구축 문서 [TUNNEL-IMPL](/docs/specs/tunnel-implementation)를 참조하십시오.

tunnel 생성은 tunnel 내 peer들의 경로를 따라 전달되는 단일 메시지에 의해 수행되며, 이 메시지는 제자리에서 다시 작성되어 tunnel 생성자에게 다시 전송됩니다. 이 단일 tunnel 메시지는 가변적인 수의 레코드들(최대 8개)로 구성되며, tunnel 내 각 잠재적 peer마다 하나씩 할당됩니다. 개별 레코드들은 경로상의 특정 peer만이 읽을 수 있도록 비대칭적으로(ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) 암호화되며, 각 홉에서 추가적인 대칭 암호화 계층(AES [CRYPTO-AES](/docs/specs/cryptography#AES))이 추가되어 비대칭적으로 암호화된 레코드가 적절한 시점에만 노출되도록 합니다.

### 레코드 수 {#number}

모든 레코드가 유효한 데이터를 포함해야 하는 것은 아닙니다. 예를 들어, 3-hop tunnel의 빌드 메시지는 참가자들로부터 tunnel의 실제 길이를 숨기기 위해 더 많은 레코드를 포함할 수 있습니다. 두 가지 빌드 메시지 유형이 있습니다. 원래의 Tunnel Build Message ([TBM](/docs/specs/i2np#msg-tunnelbuild))는 8개의 레코드를 포함하며, 이는 실용적인 모든 tunnel 길이에 대해 충분합니다. 더 새로운 Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild))는 1개에서 8개의 레코드를 포함합니다. 발신자는 메시지 크기와 원하는 tunnel 길이 난독화 수준 사이에서 균형을 맞출 수 있습니다.

현재 네트워크에서 대부분의 tunnel은 2홉 또는 3홉 길이입니다. 현재 구현에서는 4홉 이하의 tunnel을 구축하기 위해 5-record VTBM을 사용하고, 더 긴 tunnel의 경우 8-record TBM을 사용합니다. 5-record VTBM은 (단편화될 때 세 개의 1KB tunnel 메시지에 맞춰짐) 네트워크 트래픽을 줄이고 구축 성공률을 높입니다. 왜냐하면 작은 메시지일수록 삭제될 가능성이 낮기 때문입니다.

응답 메시지는 빌드 메시지와 같은 타입과 길이여야 합니다.

### 요청 레코드 명세 {#tunnelcreate-requestrecord}

I2NP 사양서 [BRR](/docs/specs/i2np#struct-buildrequestrecord)에도 명시되어 있습니다.

레코드의 평문, 요청받는 hop에게만 보임:

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
다음 tunnel ID와 다음 router identity hash 필드는 tunnel의 다음 홉을 지정하는 데 사용되지만, 아웃바운드 tunnel 엔드포인트의 경우에는 재작성된 tunnel 생성 응답 메시지가 전송되어야 할 위치를 지정합니다. 또한, 다음 메시지 ID는 해당 메시지(또는 응답)가 사용해야 할 메시지 ID를 지정합니다.

tunnel layer key, tunnel IV key, reply key, 그리고 reply IV는 각각 생성자가 생성한 무작위 32바이트 값으로, 이 빌드 요청 레코드에서만 사용됩니다.

flags 필드에는 다음이 포함됩니다:

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
비트 7은 해당 hop이 inbound gateway (IBGW)가 될 것임을 나타냅니다. 비트 6은 해당 hop이 outbound endpoint (OBEP)가 될 것임을 나타냅니다. 두 비트 모두 설정되지 않은 경우, 해당 hop은 중간 참가자가 됩니다. 두 비트가 동시에 설정될 수는 없습니다.

#### 요청 레코드 생성

모든 홉은 0이 아닌 임의의 Tunnel ID를 받습니다. 현재 홉과 다음 홉의 Tunnel ID가 채워집니다. 모든 레코드는 임의의 tunnel IV key, reply IV, layer key, reply key를 받습니다.

#### Request Record 암호화 {#encryption}

그 평문 레코드는 홉의 공개 암호화 키로 ElGamal 2048 암호화 [CRYPTO-ELG](/docs/specs/cryptography#elgamal)되어 528바이트 레코드로 포맷됩니다:

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
512바이트 암호화된 레코드에서 ElGamal 데이터는 514바이트 ElGamal 암호화 블록 [CRYPTO-ELG](/docs/specs/cryptography#elgamal)의 1-256바이트와 258-513바이트를 포함합니다. 블록에서 두 개의 패딩 바이트(위치 0과 257의 제로 바이트)는 제거됩니다.

cleartext가 전체 필드를 사용하므로 `SHA256(cleartext) + cleartext` 이외의 추가 패딩은 필요하지 않습니다.

각 528바이트 레코드는 해당 홉에서만 router identity가 평문으로 표시되도록 반복적으로 암호화됩니다(각 홉에 대한 reply key와 reply IV를 사용하여 AES 복호화 사용).

### 홉 처리 및 암호화 {#tunnelcreate-hopprocessing}

hop이 TunnelBuildMessage를 수신하면, 메시지에 포함된 레코드들을 살펴보며 자신의 identity hash(16바이트로 단축)로 시작하는 레코드를 찾습니다. 그 다음 해당 레코드에서 ElGamal 블록을 복호화하고 보호된 평문을 검색합니다. 이 시점에서 AES-256 응답 키를 Bloom filter에 입력하여 tunnel 요청이 중복되지 않는지 확인합니다. 중복되거나 유효하지 않은 요청은 삭제됩니다. 현재 시간 또는 시간 초반인 경우 이전 시간으로 스탬프되지 않은 레코드는 삭제되어야 합니다. 예를 들어, 타임스탬프의 시간을 가져와서 전체 시간으로 변환한 다음, 현재 시간보다 65분 이상 늦거나 5분 이상 빠르면 유효하지 않습니다. Bloom filter는 최소 1시간(클록 스큐를 허용하기 위해 몇 분 추가) 이상의 지속 시간을 가져야 하므로, 레코드의 시간 타임스탬프를 확인하여 거부되지 않은 현재 시간의 중복 레코드가 필터에 의해 거부됩니다.

tunnel에 참여하기로 동의할지 여부를 결정한 후, 요청이 포함되어 있던 레코드를 암호화된 응답 블록으로 교체합니다. 다른 모든 레코드는 포함된 응답 키와 IV를 사용하여 AES-256으로 암호화됩니다 [CRYPTO-AES](/docs/specs/cryptography#AES). 각각은 동일한 응답 키와 응답 IV를 사용하여 개별적으로 AES/CBC 암호화됩니다. CBC 모드는 레코드 간에 연속적으로(체인) 적용되지 않습니다.

각 hop은 자신의 응답만을 알고 있습니다. 만약 동의한다면, 다른 모든 hop들이 동의했는지 알 수 없기 때문에 사용되지 않더라도 만료될 때까지 tunnel을 유지할 것입니다.

#### 응답 레코드 사양 {#tunnelcreate-replyrecord}

현재 홉이 자신의 레코드를 읽은 후, 터널 참여에 동의하는지 여부를 명시하는 응답 레코드로 교체하며, 동의하지 않는 경우 거부 이유를 분류합니다. 이는 단순히 1바이트 값으로, 0x0은 터널 참여에 동의함을 의미하고, 더 높은 값은 더 높은 수준의 거부를 의미합니다.

다음과 같은 거부 코드들이 정의되어 있습니다:

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

router 종료와 같은 다른 원인들을 피어들로부터 숨기기 위해, 현재 구현에서는 거의 모든 거부에 대해 TUNNEL_REJECT_BANDWIDTH를 사용합니다.

응답은 암호화된 블록에서 전달된 AES 세션 키로 암호화되며, 전체 레코드 크기에 도달하기 위해 495바이트의 랜덤 데이터로 패딩됩니다. 패딩은 상태 바이트 앞에 위치합니다:

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
이는 I2NP 사양 [BRR](/docs/specs/i2np#struct-buildrequestrecord)에도 설명되어 있습니다.

### Tunnel 빌드 메시지 준비 {#tunnelcreate-requestpreparation}

새로운 Tunnel Build Message를 구축할 때, 모든 Build Request Record들을 먼저 구축하고 ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)을 사용하여 비대칭 암호화해야 합니다. 그런 다음 각 레코드는 경로상의 앞선 홉들의 응답 키와 IV를 사용하여 AES [CRYPTO-AES](/docs/specs/cryptography#AES)로 선제적으로 복호화됩니다. 해당 복호화는 역순으로 실행되어야 하므로, 비대칭 암호화된 데이터가 선행 홉이 암호화한 후 올바른 홉에서 평문으로 나타날 수 있습니다.

개별 요청에 필요하지 않은 초과 레코드는 생성자에 의해 단순히 랜덤 데이터로 채워집니다.

### Tunnel Build Message 전달 {#tunnelcreate-requestdelivery}

outbound tunnel의 경우, 전달은 tunnel 생성자로부터 첫 번째 홉까지 직접 수행되며, 생성자가 tunnel의 또 다른 홉인 것처럼 TunnelBuildMessage를 패키징합니다. inbound tunnel의 경우, 전달은 기존의 outbound tunnel을 통해 수행됩니다. outbound tunnel은 일반적으로 구축 중인 새 tunnel과 동일한 풀에서 가져옵니다. 해당 풀에서 사용 가능한 outbound tunnel이 없으면 outbound 탐색 tunnel이 사용됩니다. 시작 시 outbound 탐색 tunnel이 아직 존재하지 않을 때는 가짜 0-hop outbound tunnel이 사용됩니다.

### Tunnel Build Message Endpoint 처리 {#tunnelcreate-endpointhandling}

아웃바운드 터널 생성을 위해, 요청이 아웃바운드 엔드포인트에 도달할 때 ('누구에게나 메시지 허용' 플래그로 결정됨), 홉은 평상시와 같이 처리되어 레코드 대신 응답을 암호화하고 다른 모든 레코드들을 암호화하지만, TunnelBuildMessage를 전달할 '다음 홉'이 없기 때문에, 대신 암호화된 응답 레코드들을 TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) 또는 VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply))에 넣고 (메시지 유형과 레코드 수는 요청과 일치해야 함) 요청 레코드 내에 지정된 응답 터널로 전달합니다. 해당 응답 터널은 다른 메시지와 마찬가지로 Tunnel Build Reply Message를 터널 생성자에게 다시 전달합니다 [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). 그런 다음 터널 생성자는 아래에 설명된 대로 이를 처리합니다.

응답 tunnel은 생성자에 의해 다음과 같이 선택됩니다: 일반적으로 구축 중인 새로운 아웃바운드 tunnel과 같은 풀의 인바운드 tunnel입니다. 해당 풀에서 인바운드 tunnel을 사용할 수 없는 경우, 인바운드 탐색 tunnel이 사용됩니다. 시작 시 인바운드 탐색 tunnel이 아직 존재하지 않을 때는 가짜 0-hop 인바운드 tunnel이 사용됩니다.

inbound tunnel 생성의 경우, 요청이 inbound 엔드포인트(tunnel 생성자라고도 함)에 도달하면 명시적인 Tunnel Build Reply Message를 생성할 필요가 없으며, router는 아래와 같이 각 응답을 처리합니다.

### Tunnel Build Reply Message Processing {#tunnelcreate-replyprocessing}

응답 레코드를 처리하기 위해, 생성자는 각 레코드를 개별적으로 AES 복호화하기만 하면 됩니다. 이때 피어 이후 tunnel의 각 홉에 대한 응답 키와 IV를 역순으로 사용합니다. 이렇게 하면 해당 피어가 tunnel 참여에 동의하는지 또는 거부하는 이유가 무엇인지를 명시하는 응답이 노출됩니다. 모든 피어가 동의하면 tunnel이 생성된 것으로 간주되어 즉시 사용할 수 있지만, 누군가 거부하면 tunnel은 폐기됩니다.

합의와 거부는 각 peer의 프로필 [PEER-SELECTION](/docs/overview/peer-selection)에 기록되어, 향후 peer tunnel 용량 평가에 사용됩니다.

## 역사 및 참고사항 {#tunnelcreate-notes}

이 전략은 predecessor attack에 관해 I2P 메일링 리스트에서 Michael Rogers, Matthew Toseland (toad), 그리고 jrandom 간의 토론 중에 나왔습니다. [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html)를 참조하세요. 이는 2006-02-16에 릴리스 0.6.1.10에서 도입되었으며, 이는 I2P에서 비호환 변경이 이루어진 마지막 시점이었습니다.

참고 사항:

- 이 설계는 tunnel 내의 두 적대적인 peer가 동일한 tunnel 내에 있다는 것을 감지하기 위해 하나 이상의 요청 또는 응답 레코드에 태깅하는 것을 방지하지는 않지만, 이러한 행위는 tunnel 생성자가 응답을 읽을 때 감지될 수 있어 해당 tunnel이 유효하지 않은 것으로 표시되게 합니다.

- 이 설계는 비대칭 암호화된 섹션에 작업 증명을 포함하지 않지만, 16바이트 identity hash를 절반으로 줄이고 나머지 부분을 최대 2^64 비용의 hashcash 함수로 대체할 수 있습니다.

- 이 설계만으로는 tunnel 내의 두 적대적인 peer가 타이밍 정보를 사용하여 자신들이 같은 tunnel에 있는지 판단하는 것을 방지할 수 없습니다. 배치 및 동기화된 요청 전달을 사용하면 도움이 될 수 있습니다(요청을 배치로 묶어 (ntp 동기화된) 분 단위로 전송). 그러나 이렇게 하면 peer들이 요청을 지연시키고 나중에 tunnel에서 그 지연을 감지하여 요청에 '태그'를 달 수 있게 됩니다. 작은 시간 창 내에 전달되지 않은 요청을 삭제하는 것이 효과적일 수 있지만(높은 수준의 시계 동기화가 필요함), 또는 개별 hop이 요청을 전달하기 전에 랜덤 지연을 주입하는 방법도 있을 것입니다.

- 요청에 태깅하는 치명적이지 않은 방법이 있나요?

- 1시간 해상도의 타임스탬프는 재생 공격 방지를 위해 사용됩니다. 이 제약은 0.9.16 릴리스까지 강제되지 않았습니다.

## 향후 작업 {#future}

- 현재 구현에서 발신자는 자신을 위해 하나의 레코드를 비워둡니다. 따라서 n개의 레코드를 가진 메시지는 n-1 홉의 터널만 구축할 수 있습니다. 이는 인바운드 터널에서는 필요한 것으로 보입니다(마지막에서 두 번째 홉이 다음 홉의 해시 접두사를 볼 수 있는 경우), 하지만 아웃바운드 터널에서는 그렇지 않습니다. 이는 연구하고 검증해야 할 사항입니다. 익명성을 손상시키지 않고 남은 레코드를 사용할 수 있다면 그렇게 해야 합니다.

- 위 노트에서 설명된 가능한 태깅 및 타이밍 공격에 대한 추가 분석.

- VTBM만 사용하고, 이를 지원하지 않는 이전 피어들은 선택하지 마십시오.

- Build Request Record는 tunnel 수명이나 만료 시간을 지정하지 않습니다;
  각 hop은 10분 후에 tunnel을 만료시키며, 이는 네트워크 전체의
  하드코딩된 상수입니다. 플래그 필드의 비트를 사용하고 패딩에서 4(또는 8)
  바이트를 가져와 수명이나 만료 시간을 지정할 수 있습니다. 요청자는
  모든 참가자가 이를 지원하는 경우에만 이 옵션을 지정할 것입니다.

## 참고 자료 {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
