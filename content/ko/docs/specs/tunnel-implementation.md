---
title: "Tunnel 구현"
description: "I2P tunnel 운영, 구축 및 메시지 처리 명세서"
slug: "tunnel-implementation"
aliases:
  - "/ko/docs/specs/implementation"
  - "/ko/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

이 페이지는 현재 tunnel 구현에 대해 설명합니다.

## Tunnel 개요 {#tunnel.overview}

I2P 내에서 메시지는 피어들의 가상 tunnel을 통해 한 방향으로 전달되며, 다음 홉으로 메시지를 전달하기 위해 사용 가능한 모든 수단을 활용합니다. 메시지는 tunnel의 *gateway*에 도착하여 고정 크기의 tunnel 메시지로 묶이거나 분할된 후, tunnel의 다음 홉으로 전달됩니다. 다음 홉은 메시지를 처리하고 유효성을 검증한 후 그 다음 홉으로 전송하며, 이 과정이 tunnel 끝점에 도달할 때까지 반복됩니다. 그 *끝점*은 gateway에서 묶인 메시지를 받아 지시된 대로 전달합니다 - 다른 router로, 다른 router의 다른 tunnel로, 또는 로컬로 전달합니다.

모든 tunnel은 동일하게 작동하지만, 두 개의 서로 다른 그룹으로 분류될 수 있습니다 - inbound tunnel과 outbound tunnel입니다. inbound tunnel은 신뢰할 수 없는 gateway를 가지고 있으며, 이 gateway는 tunnel endpoint 역할을 하는 tunnel 생성자를 향해 메시지를 전달합니다. outbound tunnel의 경우, tunnel 생성자가 gateway 역할을 하여 원격 endpoint로 메시지를 전달합니다.

tunnel의 생성자는 tunnel에 참여할 피어들을 정확히 선택하고, 각각에게 필요한 설정 데이터를 제공합니다. tunnel은 임의의 홉 수를 가질 수 있습니다. 참여자나 제3자가 tunnel의 길이를 결정하거나, 심지어 공모하는 참여자들이 자신들이 동일한 tunnel의 일부인지 여부를 결정하는 것을 어렵게 만드는 것이 목적입니다 (공모하는 피어들이 tunnel에서 서로 인접해 있는 상황은 제외).

실제로는 서로 다른 목적을 위해 일련의 tunnel 풀들이 사용됩니다 - 각 로컬 클라이언트 목적지는 자체적인 인바운드 tunnel과 아웃바운드 tunnel 세트를 가지며, 이는 익명성과 성능 요구사항을 충족하도록 구성됩니다. 또한 router 자체는 netDb 참여와 tunnel 자체 관리를 위한 일련의 풀들을 유지합니다.

I2P는 이러한 tunnel들과 함께 본질적으로 패킷 교환 네트워크로, 여러 tunnel이 병렬로 실행되도록 하여 복원력을 높이고 부하를 분산시킬 수 있습니다. 핵심 I2P 레이어 외부에는 클라이언트 애플리케이션을 위한 선택적인 종단간 스트리밍 라이브러리가 제공되며, 메시지 재정렬, 재전송, 혼잡 제어 등을 포함한 TCP와 유사한 동작을 제공합니다.

I2P tunnel 용어에 대한 개요는 [tunnel 개요 페이지](/docs/overview/tunnel-routing)에 있습니다.

## 터널 작동 (메시지 처리) {#tunnel.operation}

### 개요

터널이 구축된 후, [I2NP 메시지](/docs/specs/i2np)가 처리되어 터널을 통과합니다. 터널 운영에는 네 가지 구별되는 프로세스가 있으며, 터널 내의 다양한 피어들이 이를 담당합니다.

1. 먼저, tunnel gateway가 여러 I2NP 메시지를 수집하고 이를 전달용 tunnel 메시지로 전처리합니다.
2. 다음으로, 해당 gateway가 전처리된 데이터를 암호화한 후 첫 번째 홉으로 전달합니다.
3. 해당 피어와 후속 tunnel 참가자들이 암호화 레이어를 해제하고 중복이 아님을 확인한 후 다음 피어로 전달합니다.
4. 마침내, tunnel 메시지가 엔드포인트에 도착하면 gateway에서 원래 번들링된 I2NP 메시지들이 재조립되어 요청된 대로 전달됩니다.

중간 tunnel 참가자들은 자신이 인바운드 또는 아웃바운드 tunnel에 있는지 알지 못합니다. 이들은 항상 다음 홉을 위해 "암호화"를 수행합니다. 따라서 우리는 대칭 AES 암호화의 장점을 활용하여 아웃바운드 tunnel 게이트웨이에서 "복호화"를 수행하여 평문이 아웃바운드 엔드포인트에서 드러나도록 합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### 게이트웨이 처리 {#tunnel.gateway}

#### 메시지 전처리 {#tunnel.preprocessing}

tunnel gateway의 기능은 [I2NP messages](/docs/specs/i2np)를 분할하고 고정 크기의 [tunnel messages](/docs/specs/tunnel-message)로 패킹한 후 tunnel message들을 암호화하는 것입니다. Tunnel message는 다음을 포함합니다:

- 4바이트 Tunnel ID
- 16바이트 IV (초기화 벡터)
- 체크섬
- 필요한 경우 패딩
- 하나 이상의 { 전달 지시사항, I2NP 메시지 조각 } 쌍

Tunnel ID는 각 홉에서 사용되는 4바이트 숫자입니다 - 참여자들은 어떤 tunnel ID로 메시지를 수신해야 하는지, 그리고 다음 홉으로 전달할 때 어떤 tunnel ID를 사용해야 하는지 알고 있으며, 각 홉은 메시지를 수신할 tunnel ID를 선택합니다. Tunnel 자체는 수명이 짧습니다(10분). 동일한 피어 순서를 사용하여 후속 tunnel을 구축하더라도 각 홉의 tunnel ID는 변경됩니다.

경로를 따라 메시지 크기를 조정하여 적대자가 메시지에 태그를 붙이는 것을 방지하기 위해, 모든 tunnel 메시지는 고정된 1024바이트 크기입니다. 더 큰 I2NP 메시지를 수용하고 더 작은 메시지를 더 효율적으로 지원하기 위해, gateway는 더 큰 I2NP 메시지를 각 tunnel 메시지 내에 포함된 조각으로 분할합니다. endpoint는 짧은 시간 동안 조각들로부터 I2NP 메시지를 재구성하려고 시도하지만, 필요에 따라 이를 폐기합니다.

자세한 내용은 [tunnel 메시지 사양](/docs/specs/tunnel-message)에 있습니다.

### Gateway 암호화

메시지를 패딩된 페이로드로 전처리한 후, 게이트웨이는 무작위 16바이트 IV 값을 생성하고, 필요에 따라 이를 반복적으로 암호화하며 tunnel 메시지와 함께 암호화한 다음, {tunnelID, IV, 암호화된 tunnel 메시지} 튜플을 다음 홉으로 전달합니다.

gateway에서의 암호화가 어떻게 수행되는지는 tunnel이 inbound인지 outbound인지에 따라 달라집니다. inbound tunnel의 경우, 단순히 무작위 IV를 선택하고, 후처리 및 업데이트하여 gateway용 IV를 생성한 후 자신의 레이어 키와 함께 해당 IV를 사용하여 전처리된 데이터를 암호화합니다. outbound tunnel의 경우 tunnel 내 모든 홉에 대한 IV와 레이어 키를 사용하여 (암호화되지 않은) IV와 전처리된 데이터를 반복적으로 복호화해야 합니다. outbound tunnel 암호화의 결과는 각 피어가 암호화할 때 엔드포인트가 초기 전처리된 데이터를 복구한다는 것입니다.

### 참가자 처리 {#tunnel.participant}

peer가 tunnel 메시지를 받으면, 해당 메시지가 이전과 동일한 이전 hop에서 왔는지 확인합니다 (첫 번째 메시지가 tunnel을 통과할 때 초기화됨). 이전 peer가 다른 router이거나 메시지가 이미 수신된 적이 있다면, 메시지는 폐기됩니다. 그러면 참가자는 수신된 IV를 자신의 IV 키를 사용하여 AES256/ECB로 암호화하여 현재 IV를 결정하고, 해당 IV를 참가자의 레이어 키와 함께 사용하여 데이터를 암호화한 다음, 현재 IV를 자신의 IV 키를 사용하여 다시 AES256/ECB로 암호화하고, 튜플 {nextTunnelId, nextIV, encryptedData}를 다음 hop으로 전달합니다. 이러한 IV의 이중 암호화(사용 전후 모두)는 특정 유형의 확인 공격을 방어하는 데 도움이 됩니다.

중복 메시지 탐지는 메시지 IV에 대한 감쇠 블룸 필터로 처리됩니다. 각 router는 참여하고 있는 모든 tunnel에 대해 수신된 메시지의 IV와 첫 번째 블록의 XOR을 포함하는 단일 블룸 필터를 유지하며, 10-20분 후(tunnel이 만료될 때)에 확인된 항목을 삭제하도록 수정됩니다. 블룸 필터의 크기와 사용되는 매개변수는 무시할 수 있는 거짓 양성 확률로 router의 네트워크 연결을 충분히 포화시킬 수 있습니다. 블룸 필터에 입력되는 고유 값은 IV와 첫 번째 블록의 XOR이므로, tunnel 내의 비순차적 공모 피어들이 IV와 첫 번째 블록을 바꿔서 다시 보내는 방식으로 메시지를 태깅하는 것을 방지합니다.

### 엔드포인트 처리 {#tunnel.endpoint}

tunnel의 마지막 홉에서 tunnel 메시지를 수신하고 검증한 후, 엔드포인트가 게이트웨이에 의해 인코딩된 데이터를 복구하는 방법은 tunnel이 인바운드인지 아웃바운드인지에 따라 달라집니다. 아웃바운드 tunnel의 경우, 엔드포인트는 다른 참가자들과 마찬가지로 자신의 레이어 키로 메시지를 암호화하여 전처리된 데이터를 노출시킵니다. 인바운드 tunnel의 경우, 엔드포인트는 또한 tunnel 생성자이므로 각 단계의 레이어 키와 IV 키를 역순으로 사용하여 IV와 메시지를 반복적으로 복호화할 수 있습니다.

이 시점에서 tunnel 종단점은 게이트웨이가 보낸 전처리된 데이터를 가지고 있으며, 이를 포함된 I2NP 메시지로 파싱하여 전달 지침에 따라 요청된 대로 전달할 수 있습니다.

## 터널 구축 {#tunnel.building}

tunnel을 구축할 때, 생성자는 각 홉에 필요한 구성 데이터와 함께 요청을 보내고 tunnel을 활성화하기 전에 모든 홉이 동의할 때까지 기다려야 합니다. 요청은 암호화되어 특정 정보(tunnel 계층이나 IV 키 등)를 알아야 하는 피어만이 해당 데이터에 접근할 수 있습니다. 또한 tunnel 생성자만이 피어의 응답에 접근할 수 있습니다. tunnel을 생성할 때 염두에 두어야 할 세 가지 중요한 차원이 있습니다: 어떤 피어들이 사용되는지(그리고 어디서), 요청이 어떻게 전송되는지(그리고 응답이 어떻게 수신되는지), 그리고 어떻게 유지되는지입니다.

### 피어 선택 {#tunnel.peerselection}

두 가지 터널 유형인 인바운드와 아웃바운드를 넘어서, 서로 다른 터널에 사용되는 두 가지 피어 선택 방식이 있습니다 - 탐색용(exploratory)과 클라이언트용입니다. 탐색용 터널은 네트워크 데이터베이스 유지보수와 터널 유지보수 모두에 사용되며, 클라이언트 터널은 종단 간 클라이언트 메시지에 사용됩니다.

#### 탐색 Tunnel 피어 선택 {#tunnel.selection.exploratory}

탐색용 tunnel들은 네트워크의 하위 집합에서 무작위로 선택된 피어들로 구축됩니다. 특정 하위 집합은 로컬 router와 해당 tunnel 라우팅 요구사항에 따라 달라집니다. 일반적으로 탐색용 tunnel들은 피어의 "실패하지 않지만 활성" 프로필 범주에 있는 무작위로 선택된 피어들로 구축됩니다. tunnel의 단순한 tunnel 라우팅을 넘어선 두 번째 목적은 활용도가 낮은 고용량 피어들을 찾아 클라이언트 tunnel에서 사용할 수 있도록 승격시키는 것입니다.

탐색적 피어 선택에 대한 자세한 내용은 [피어 프로파일링 및 선택 페이지](/docs/overview/peer-selection)에서 다룹니다.

#### 클라이언트 터널 피어 선택 {#tunnel.selection.client}

클라이언트 tunnel은 더 엄격한 요구사항 세트로 구축됩니다 - 로컬 router는 "빠르고 고용량" 프로필 카테고리에서 피어를 선택하여 성능과 신뢰성이 클라이언트 애플리케이션의 요구를 충족하도록 합니다. 그러나 클라이언트의 익명성 요구사항에 따라 해당 기본 선택을 넘어서 준수해야 할 몇 가지 중요한 세부 사항들이 있습니다.

클라이언트 피어 선택에 대한 자세한 내용은 [피어 프로파일링 및 선택 페이지](/docs/overview/peer-selection)에서 다루고 있습니다.

#### 터널 내 피어 순서 {#ordering}

tunnel 내에서 peer들은 [predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 업데이트](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf))에 대처하기 위해 순서가 정해집니다.

predecessor attack를 방지하기 위해, tunnel 선택은 피어들을 엄격한 순서로 유지합니다 - 특정 tunnel pool에서 A, B, C가 tunnel에 있다면, A 다음 홉은 항상 B이고, B 다음 홉은 항상 C입니다.

순서 결정은 시작 시 각 tunnel 풀에 대해 32바이트 랜덤 키를 생성하여 구현됩니다. 피어들은 순서를 추측할 수 없어야 하며, 그렇지 않으면 공격자가 tunnel의 양 끝에 위치할 가능성을 최대화하기 위해 서로 멀리 떨어진 두 개의 router 해시를 조작할 수 있습니다. 피어들은 (피어의 해시와 랜덤 키를 연결한 값)의 SHA256 해시가 랜덤 키로부터 얼마나 떨어져 있는지의 XOR 거리에 따라 정렬됩니다:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
각 tunnel pool은 서로 다른 랜덤 키를 사용하기 때문에, 단일 pool 내에서는 순서가 일관되지만 서로 다른 pool 간에는 일관되지 않습니다. 새로운 키는 각 router 재시작 시마다 생성됩니다.

### 요청 전달 {#tunnel.request}

멀티홉 tunnel은 반복적으로 복호화되고 전달되는 단일 빌드 메시지를 사용하여 구축됩니다. [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)의 용어로는, 이는 "비대화형" 망원경식 tunnel 구축입니다.

이 tunnel 요청 준비, 전달 및 응답 방법은 노출되는 전임자 수를 줄이고, 전송되는 메시지 수를 줄이며, 적절한 연결성을 검증하고, 기존의 망원경식 tunnel 생성의 메시지 카운팅 공격을 방지하도록 [설계](/docs/specs/tunnel-creation)되었습니다. (이미 구축된 tunnel의 일부를 통해 tunnel을 확장하기 위해 메시지를 보내는 이 방법은 "Hashing it out" 논문에서 "인터랙티브" 망원경식 tunnel 구축이라고 불립니다.)

tunnel 요청 및 응답 메시지의 세부사항과 그 암호화는 [여기에 명시되어 있습니다](/docs/specs/tunnel-creation).

Peer들은 다양한 이유로 터널 생성 요청을 거부할 수 있지만, 점점 더 심각해지는 네 가지 거부 유형이 알려져 있습니다: 확률적 거부(router 용량 한계 접근 또는 요청 폭주에 대한 응답), 일시적 과부하, 대역폭 과부하, 그리고 중대한 장애입니다. 이러한 네 가지 거부가 수신되면, 터널 생성자는 이를 해석하여 해당 router의 프로필을 조정하는 데 도움이 되도록 활용합니다.

피어 프로파일링에 대한 자세한 내용은 [피어 프로파일링 및 선택 페이지](/docs/overview/peer-selection)를 참조하세요.

### Tunnel 풀 {#tunnel.pooling}

효율적인 운영을 위해 router는 일련의 tunnel pool을 유지 관리하며, 각각은 특정 목적으로 사용되는 tunnel 그룹을 자체 구성으로 관리합니다. 해당 목적으로 tunnel이 필요할 때 router는 적절한 pool에서 무작위로 하나를 선택합니다. 전체적으로 두 개의 탐색 tunnel pool이 있습니다 - 하나는 인바운드, 하나는 아웃바운드 - 각각 router의 기본 구성을 사용합니다. 또한 각 로컬 목적지에 대해 한 쌍의 pool이 있습니다 - 하나의 인바운드와 하나의 아웃바운드 tunnel pool입니다. 이러한 pool들은 로컬 목적지가 [I2CP](/docs/specs/i2cp)를 통해 router에 연결할 때 지정된 구성을 사용하거나, 지정되지 않은 경우 router의 기본값을 사용합니다.

각 풀은 구성 내에서 몇 가지 핵심 설정을 가지고 있으며, 이는 활성 상태로 유지할 tunnel의 수, 장애 시를 대비해 유지할 백업 tunnel의 수, tunnel의 길이, 이러한 길이를 무작위로 설정할지 여부, 그리고 개별 tunnel을 구성할 때 허용되는 기타 설정들을 정의합니다. 구성 옵션은 [I2CP 페이지](/docs/specs/i2cp)에 명시되어 있습니다.

### 터널 길이와 기본값 {#length}

[tunnel 개요 페이지에서](/docs/overview/tunnel-routing#length).

### 예측적 빌드 전략과 우선순위 {#strategy}

Tunnel 구축은 비용이 많이 들고, tunnel들은 구축된 후 정해진 시간이 지나면 만료됩니다. 하지만 tunnel이 부족한 풀이 생기면, 해당 Destination은 본질적으로 죽은 상태가 됩니다. 또한 tunnel 구축 성공률은 로컬 및 글로벌 네트워크 상황에 따라 크게 달라질 수 있습니다. 따라서 tunnel이 필요하기 전에 새로운 tunnel을 성공적으로 구축할 수 있도록 예측적이고 적응적인 구축 전략을 유지하는 것이 중요하며, 동시에 과도한 tunnel을 구축하거나, 너무 일찍 구축하거나, 암호화된 구축 메시지를 생성하고 전송하는 데 과도한 CPU나 대역폭을 소모하지 않도록 해야 합니다.

각 튜플 {exploratory/client, in/out, length, length variance}에 대해 router는 성공적인 tunnel 구축에 소요되는 시간에 대한 통계를 유지합니다. 이러한 통계를 사용하여 tunnel 만료 전 언제부터 대체 tunnel 구축 시도를 시작해야 하는지 계산합니다. 성공적인 대체 tunnel 없이 만료 시간이 다가오면, 여러 구축 시도를 병렬로 시작하고, 필요한 경우 병렬 시도 횟수를 증가시킵니다.

대역폭과 CPU 사용량을 제한하기 위해 router는 모든 풀에서 진행 중인 빌드 시도의 최대 개수도 제한합니다. 중요한 빌드(탐색용 tunnel과 tunnel이 부족한 풀을 위한 빌드)는 우선순위를 갖습니다.

## Tunnel 메시지 제한 {#tunnel.throttling}

I2P 내의 tunnel들이 회선 교환 네트워크와 유사해 보이지만, I2P 내의 모든 것은 엄격히 메시지 기반입니다 - tunnel들은 단순히 메시지 전달을 조직화하는 데 도움을 주는 회계적 기법일 뿐입니다. 메시지의 신뢰성이나 순서에 대해서는 어떤 가정도 하지 않으며, 재전송은 상위 계층(예: I2P의 클라이언트 계층 스트리밍 라이브러리)에 맡겨집니다. 이를 통해 I2P는 패킷 교환 네트워크와 회선 교환 네트워크 모두에서 사용 가능한 스로틀링 기법의 장점을 활용할 수 있습니다. 예를 들어, 각 router는 각 tunnel이 사용하고 있는 데이터 양의 이동 평균을 추적하고, 이를 해당 router가 참여하고 있는 다른 모든 tunnel들의 평균과 결합하여, 자신의 용량과 사용률을 기반으로 추가적인 tunnel 참여 요청을 수락하거나 거절할 수 있습니다. 반면에, 각 router는 단순히 자신의 용량을 초과하는 메시지를 드롭할 수 있으며, 이는 일반적인 인터넷에서 사용되는 연구를 활용하는 것입니다.

현재 구현에서 router들은 가중 랜덤 조기 폐기(WRED) 전략을 구현합니다. 모든 참여 router(내부 참여자, 인바운드 게이트웨이, 아웃바운드 엔드포인트)에 대해, router는 대역폭 제한에 근접할수록 메시지의 일부를 무작위로 폐기하기 시작합니다. 트래픽이 제한에 가까워지거나 초과하면 더 많은 메시지가 폐기됩니다. 내부 참여자의 경우 모든 메시지가 단편화되고 패딩되어 크기가 동일합니다. 그러나 인바운드 게이트웨이와 아웃바운드 엔드포인트에서는 완전한(통합된) 메시지에 대해 폐기 결정이 이루어지며 메시지 크기가 고려됩니다. 더 큰 메시지일수록 폐기될 가능성이 높습니다. 또한 아웃바운드 엔드포인트에서 메시지가 폐기될 가능성이 인바운드 게이트웨이보다 높습니다. 이는 해당 메시지들이 여행에서 그리 "멀리 진행되지" 않았기 때문에 이러한 메시지를 폐기하는 네트워크 비용이 더 낮기 때문입니다.

## 향후 과제 {#future}

### 혼합/배치 {#tunnel.mixing}

gateway와 각 hop에서 메시지를 지연, 재정렬, 재라우팅 또는 패딩하는 데 어떤 전략을 사용할 수 있을까요? 이것이 어느 정도까지 자동으로 수행되어야 하고, 얼마나 많은 부분이 tunnel별 또는 hop별 설정으로 구성되어야 하며, tunnel의 생성자(그리고 결국 사용자)가 이 작업을 어떻게 제어해야 할까요? 이 모든 것은 미지의 영역으로 남겨져 있으며, 먼 미래의 릴리스에서 해결될 예정입니다.

### 패딩

패딩 전략은 다양한 수준에서 사용될 수 있으며, 서로 다른 공격자들에게 메시지 크기 정보가 노출되는 것을 방지합니다. 현재 고정된 tunnel 메시지 크기는 1024바이트입니다. 하지만 이 안에서 분할된 메시지들 자체는 tunnel에 의해 전혀 패딩되지 않습니다. 다만 종단 간 메시지의 경우, garlic wrapping의 일부로 패딩될 수 있습니다.

### WRED

WRED 전략은 종단간 성능과 네트워크 혼잡 붕괴 방지에 상당한 영향을 미칩니다. 현재 WRED 전략은 신중히 평가되고 개선되어야 합니다.
