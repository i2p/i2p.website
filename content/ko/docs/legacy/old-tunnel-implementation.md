---
title: "기존 Tunnel 구현"
description: "0.6.1.10 이전 I2P의 원래 tunnel 구현에 대한 역사적 문서"
slug: "old-tunnel-implementation"
aliases:
  - "/ko/docs/historical/tunnel-alt"
  - "/ko/docs/historical/tunnel-alt/"
  - "/ko/tunnel"
  - "/ko/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**참고: 폐기됨 - 사용되지 않음! 0.6.1.10에서 교체됨 - 활성 사양은 [현재 구현](/docs/specs/tunnel-implementation)을 참조하세요.**

## 1) Tunnel 개요 {#tunnel.overview}

I2P 내에서 메시지는 피어들의 가상 tunnel을 통해 한 방향으로 전달되며, 다음 홉으로 메시지를 전달하기 위해 사용 가능한 모든 수단을 활용합니다. 메시지는 tunnel의 게이트웨이에 도착하여 경로에 맞게 번들로 묶인 후, tunnel의 다음 홉으로 전달됩니다. 이 홉은 메시지를 처리하고 유효성을 검증한 후 다음 홉으로 전송하며, 이런 식으로 tunnel 엔드포인트에 도달할 때까지 계속됩니다. 해당 엔드포인트는 게이트웨이에서 번들로 묶인 메시지를 받아 지시에 따라 전달합니다 - 다른 router로, 다른 router의 다른 tunnel로, 또는 로컬로 전달합니다.

tunnel은 모두 동일하게 작동하지만, 두 개의 다른 그룹으로 구분할 수 있습니다 - 인바운드 tunnel과 아웃바운드 tunnel입니다. 인바운드 tunnel은 신뢰할 수 없는 게이트웨이를 가지고 있으며, 이 게이트웨이는 tunnel 엔드포인트 역할을 하는 tunnel 생성자쪽으로 메시지를 전달합니다. 아웃바운드 tunnel의 경우, tunnel 생성자가 게이트웨이 역할을 하여 원격 엔드포인트로 메시지를 전달합니다.

tunnel의 생성자는 tunnel에 참여할 피어들을 정확히 선택하고, 각 피어에게 필요한 설정 데이터를 제공합니다. tunnel은 0홉(게이트웨이가 동시에 엔드포인트인 경우)부터 7홉(게이트웨이 이후와 엔드포인트 이전에 6개의 피어가 있는 경우)까지 다양한 길이를 가질 수 있습니다. 참여자나 제3자가 tunnel의 길이를 판단하기 어렵게 만들고, 심지어 공모하는 참여자들조차 자신들이 동일한 tunnel의 일부인지 전혀 알 수 없도록 하는 것이 목적입니다(공모하는 피어들이 tunnel에서 서로 인접한 경우는 제외). 손상된 메시지들은 가능한 한 빨리 폐기되어 네트워크 부하를 줄입니다.

길이 외에도 각 tunnel에 사용할 수 있는 추가 구성 가능한 매개변수들이 있습니다. 예를 들어 전달되는 메시지의 크기나 빈도에 대한 제한, 패딩 사용 방법, tunnel이 얼마나 오래 작동해야 하는지, chaff 메시지 삽입 여부, 단편화 사용 여부, 그리고 어떤 배치 전략을 사용할지 등이 있습니다.

실제로는 서로 다른 목적을 위해 일련의 tunnel 풀들이 사용됩니다 - 각 로컬 클라이언트 목적지는 자체적인 인바운드 tunnel과 아웃바운드 tunnel 세트를 가지며, 이는 익명성과 성능 요구사항을 충족하도록 구성됩니다. 또한 router 자체도 네트워크 데이터베이스 참여와 tunnel 자체 관리를 위한 일련의 풀들을 유지합니다.

I2P는 이러한 tunnel들과 함께 본질적으로 패킷 스위칭 네트워크로, 병렬로 실행되는 여러 tunnel을 활용하여 복원력을 높이고 부하를 분산할 수 있습니다. 핵심 I2P 계층 외부에는 클라이언트 애플리케이션을 위한 선택적 엔드 투 엔드 스트리밍 라이브러리가 제공되며, 메시지 재정렬, 재전송, 혼잡 제어 등을 포함한 TCP와 유사한 작업을 지원합니다.

## 2) Tunnel 운영 {#tunnel.operation}

Tunnel 작동에는 tunnel의 다양한 피어들이 담당하는 네 가지 구별되는 프로세스가 있습니다. 먼저, tunnel gateway는 여러 tunnel 메시지를 축적하고 이를 tunnel 전달을 위한 형태로 전처리합니다. 다음으로, 해당 gateway는 전처리된 데이터를 암호화한 후 첫 번째 홉으로 전달합니다. 해당 피어와 후속 tunnel 참가자들은 암호화 계층을 해독하고, 메시지의 무결성을 검증한 후 다음 피어로 전달합니다. 결국 메시지는 엔드포인트에 도착하며, 여기서 gateway에 의해 번들된 메시지들이 다시 분리되어 요청된 대로 전달됩니다.

Tunnel ID는 각 홉에서 사용되는 4바이트 숫자입니다 - 참여자들은 어떤 tunnel ID로 메시지를 수신해야 하는지, 그리고 다음 홉으로 전달할 때 어떤 tunnel ID를 사용해야 하는지를 알고 있습니다. Tunnel 자체는 수명이 짧으며(현재 10분), tunnel의 목적에 따라 달라지지만, 동일한 피어 시퀀스를 사용하여 후속 tunnel이 구축될 수 있더라도 각 홉의 tunnel ID는 변경됩니다.

### 2.1) 메시지 전처리 {#tunnel.preprocessing}

gateway가 터널을 통해 데이터를 전송하려고 할 때, 먼저 0개 이상의 I2NP 메시지들을 수집하고(최대 32KB까지), 사용할 패딩의 양을 선택하며, 각 I2NP 메시지가 터널 endpoint에서 어떻게 처리되어야 하는지를 결정한 후, 그 데이터를 원시 터널 페이로드로 인코딩합니다:

- 패딩 바이트 수를 지정하는 2바이트 부호 없는 정수
- 그만큼의 랜덤 바이트들
- 0개 이상의 { 명령어, 메시지 } 쌍들의 연속

지시사항은 다음과 같이 인코딩됩니다:

- 1 바이트 값:
  ```
  비트 0-1: 전달 유형
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     비트 2: 지연 포함? (1 = true, 0 = false)
     비트 3: 분할됨? (1 = true, 0 = false)
     비트 4: 확장 옵션? (1 = true, 0 = false)
  비트 5-7: 예약됨
  ```
- 전달 유형이 TUNNEL인 경우, 4 바이트 tunnel ID
- 전달 유형이 TUNNEL 또는 ROUTER인 경우, 32 바이트 router 해시
- 지연 포함 플래그가 true인 경우, 1 바이트 값:
  ```
     비트 0: 유형 (0 = 엄격함, 1 = 무작위화됨)
  비트 1-7: 지연 지수 (2^값 분)
  ```
- 분할된 플래그가 true인 경우, 4 바이트 메시지 ID와 1 바이트 값:
  ```
  비트 0-6: 분할 번호
     비트 7: 마지막인가? (1 = true, 0 = false)
  ```
- 확장 옵션 플래그가 true인 경우:
  ```
  = 1 바이트 옵션 크기 (바이트 단위)
  = 해당 크기만큼의 바이트
  ```
- I2NP 메시지의 2 바이트 크기

I2NP 메시지는 표준 형식으로 인코딩되며, 전처리된 페이로드는 16바이트의 배수로 패딩되어야 합니다.

### 2.2) Gateway 처리 {#tunnel.gateway}

메시지를 패딩된 페이로드로 전처리한 후, gateway는 8개의 키로 페이로드를 암호화하여 각 피어가 언제든지 페이로드의 무결성을 확인할 수 있도록 체크섬 블록을 구축하고, tunnel 엔드포인트가 체크섬 블록의 무결성을 확인할 수 있도록 종단간 검증 블록을 만듭니다. 구체적인 세부사항은 다음과 같습니다.

사용되는 암호화는 복호화 시 단순히 CBC 모드의 AES로 데이터를 처리하고, 메시지의 특정 고정 부분(바이트 16부터 $size-144까지)의 SHA256을 계산한 다음, 체크섬 블록에서 해당 해시의 첫 16바이트를 검색하기만 하면 되도록 구성되어 있습니다. tunnel에서의 위치를 노출하거나 레이어가 벗겨지면서 메시지가 지속적으로 "축소"되는 일 없이 메시지를 검증할 수 있도록 고정된 홉 수(8개 피어)가 정의되어 있습니다. 8홉보다 짧은 tunnel의 경우, tunnel 생성자가 초과 홉의 역할을 대신하여 자신의 키로 복호화를 수행합니다(outbound tunnel의 경우 처음에, inbound tunnel의 경우 마지막에 수행됩니다).

암호화에서 어려운 부분은 얽힌 체크섬 블록을 구축하는 것인데, 이는 본질적으로 각 단계에서 페이로드의 해시가 어떻게 보일지 알아내고, 그 해시들을 무작위로 정렬한 다음, 무작위로 정렬된 각 해시가 각 단계에서 어떻게 보일지에 대한 행렬을 구축해야 합니다. gateway 자체는 첫 번째 홉이 이전 홉이 gateway였다는 것을 알 수 없도록 체크섬 블록 내의 피어 중 하나인 것처럼 가장해야 합니다. 이를 좀 더 시각적으로 나타내면:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
위에서 P[7]은 tunnel을 통과하는 원본 데이터(전처리된 메시지)와 동일하고, V[7]은 peer7에서 복호화 후 볼 수 있는 eH[0-7]의 SHA256 중 첫 16바이트입니다. 해시보다 "위쪽"에 있는 매트릭스 셀들의 경우, 그들의 값은 아래쪽 셀을 아래쪽 peer의 키로 암호화하여 도출되며, 왼쪽 열의 끝을 IV로 사용합니다. 해시보다 "아래쪽"에 있는 매트릭스 셀들의 경우, 현재 peer의 키로 복호화된 위쪽 셀과 동일하며, 해당 행의 이전 암호화된 블록의 끝을 사용합니다.

이러한 무작위화된 체크섬 블록 매트릭스를 통해 각 peer는 페이로드의 해시를 찾을 수 있거나, 해시가 없다면 메시지가 손상되었음을 알 수 있습니다. CBC 모드를 사용한 얽힘은 체크섬 블록 자체에 대한 태깅의 어려움을 증가시키지만, 태그된 데이터 이후의 열이 이미 peer에서 페이로드를 확인하는 데 사용되었다면 해당 태깅이 잠시 탐지되지 않을 수도 있습니다. 어떤 경우든, tunnel 엔드포인트(peer 7)는 체크섬 블록 중 어느 것이든 태그되었는지 확실히 알 수 있는데, 이는 검증 블록(V[7])을 손상시킬 것이기 때문입니다.

IV[0]은 무작위 16바이트 값이며, IV[i]는 H(D(IV[i-1], K[i-1]) xor IV_WHITENER)의 첫 16바이트입니다. 경로를 따라 동일한 IV를 사용하지 않는데, 이는 간단한 공모를 허용하기 때문이며, 키 누출을 방해하기 위해 복호화된 값의 해시를 사용하여 IV를 전파합니다. IV_WHITENER는 고정된 16바이트 값입니다.

gateway가 메시지를 전송하려고 할 때, 첫 번째 홉인 피어에 대한 올바른 행(보통 peer1.recv 행)을 내보내고 이를 완전히 전달합니다.

### 2.3) 참가자 처리 {#tunnel.participant}

tunnel의 참가자가 메시지를 받으면, 처음 16바이트를 IV로 사용하여 CBC 모드의 AES256으로 자신의 tunnel 키를 사용해 레이어를 해독합니다. 그런 다음 페이로드로 보이는 부분(16바이트부터 $size-144바이트까지)의 해시를 계산하고, 해독된 체크섬 블록 내에서 해당 해시의 처음 16바이트를 검색합니다. 일치하는 항목이 없으면 메시지가 폐기됩니다. 그렇지 않으면 IV를 해독하고, 그 값을 IV_WHITENER와 XOR한 다음, 그 해시의 처음 16바이트로 교체하여 IV를 업데이트합니다. 그 결과 메시지는 처리를 위해 다음 피어로 전달됩니다.

tunnel 수준에서 재생 공격을 방지하기 위해, 각 참여자는 tunnel의 생명주기 동안 수신된 IV들을 추적하여 중복을 거부합니다. 각 tunnel은 매우 짧은 수명(현재 10분)만 가지므로 필요한 메모리 사용량은 적어야 합니다. 전체 32KB 메시지로 tunnel을 통해 일정한 100KBps를 처리하면 1875개의 메시지가 생성되어 30KB 미만의 메모리가 필요합니다. Gateway와 endpoint는 tunnel에 포함된 I2NP 메시지의 메시지 ID와 만료 시간을 추적하여 재생을 처리합니다.

### 2.4) Endpoint 처리 {#tunnel.endpoint}

메시지가 tunnel 엔드포인트에 도달하면, 일반 참가자처럼 이를 복호화하고 검증합니다. 체크섬 블록이 유효한 일치를 보이면, 엔드포인트는 체크섬 블록 자체의 해시를 (복호화 후에 보이는 대로) 계산하고 이를 복호화된 검증 해시(마지막 16바이트)와 비교합니다. 검증 해시가 일치하지 않으면, 엔드포인트는 tunnel 참가자 중 하나의 태깅 시도를 기록하고 메시지를 폐기할 수 있습니다.

이 시점에서 tunnel 종단점은 게이트웨이에서 보낸 전처리된 데이터를 가지고 있으며, 이를 포함된 I2NP 메시지로 파싱하고 전달 지시사항에 따라 요청된 대로 전달할 수 있습니다.

### 2.5) 패딩 {#tunnel.padding}

여러 tunnel 패딩 전략이 가능하며, 각각 고유한 장점이 있습니다:

- 패딩 없음
- 임의 크기로 패딩
- 고정 크기로 패딩
- 가장 가까운 KB로 패딩
- 가장 가까운 지수 크기로 패딩 (2^n 바이트)

*어떤 방법을 사용할까? 패딩 없음이 가장 효율적이고, 랜덤 패딩은 현재 우리가 사용하는 방식이며, 고정 크기는 극단적인 낭비이거나 분할 구현을 강제할 것입니다. 가장 가까운 지수 크기로 패딩하는 방식(Freenet 방식)이 유망해 보입니다. 아마도 네트워크에서 메시지 크기에 대한 통계를 수집한 다음, 다른 전략들로부터 발생할 비용과 이익을 살펴봐야 할 것 같습니다.*

### 2.6) Tunnel 단편화 {#tunnel.fragmentation}

다양한 패딩 및 믹싱 방식에서, 익명성 관점에서 단일 I2NP 메시지를 여러 부분으로 분할하고, 각각을 서로 다른 터널 메시지를 통해 개별적으로 전달하는 것이 유용할 수 있습니다. 엔드포인트는 해당 분할을 지원할 수도 있고 지원하지 않을 수도 있으며(필요에 따라 프래그먼트를 폐기하거나 보관), 분할 처리는 즉시 구현되지 않을 예정입니다.

### 2.7) 대안 {#tunnel.alternatives}

#### 2.7.1) 체크섬 블록 사용하지 않기 {#tunnel.nochecksum}

위 과정의 한 가지 대안은 체크섬 블록을 완전히 제거하고 검증 해시를 페이로드의 일반 해시로 대체하는 것입니다. 이렇게 하면 tunnel 게이트웨이에서의 처리가 단순화되고 각 홉에서 144바이트의 대역폭을 절약할 수 있습니다. 반면에 tunnel 내의 공격자들은 메시지 크기를 외부 관찰자들과 나중 tunnel 참여자들이 공모하여 쉽게 추적할 수 있는 크기로 간단하게 조정할 수 있습니다. 이러한 손상은 또한 메시지를 전달하는 데 필요한 전체 대역폭의 낭비를 초래할 것입니다. 홉별 검증이 없으면 극도로 긴 tunnel을 구축하거나 tunnel에 루프를 만들어 과도한 네트워크 리소스를 소모하는 것도 가능할 것입니다.

#### 2.7.2) 중간 경로에서 tunnel 처리 조정 {#tunnel.reroute}

단순한 터널 라우팅 알고리즘이 대부분의 경우에 충분해야 하지만, 탐구할 수 있는 세 가지 대안이 있습니다:

- tunnel 내 임의의 hop에서 지정된 시간 또는 무작위 기간 동안 메시지를 지연시킵니다. 이는 체크섬 블록의 해시를 예를 들어 해시의 첫 8바이트로 대체하고 일부 지연 명령을 추가하여 달성할 수 있습니다. 또는 명령이 참가자에게 실제로 원시 페이로드를 있는 그대로 해석하도록 지시하고, 메시지를 버리거나 경로를 따라 계속 전달하도록 할 수 있습니다(이 경우 엔드포인트에서 chaff 메시지로 해석됩니다). 이 방법의 후반부는 게이트웨이가 다른 hop에서 평문 페이로드를 생성하도록 암호화 알고리즘을 조정해야 하지만, 큰 문제는 되지 않을 것입니다.

- tunnel에 참여하는 router들이 메시지를 전달하기 전에 재조합할 수 있도록 허용 - 다음 홉으로의 전달 지시사항을 포함하여 해당 peer의 자체 아웃바운드 tunnel 중 하나를 통해 바운싱. 이는 제어된 방식(위의 지연과 같은 경로상 지시사항 포함) 또는 확률적으로 사용될 수 있음.

- tunnel 생성자가 tunnel 내에서 피어의 "next hop"을 재정의할 수 있는 코드를 구현하여 추가적인 동적 리디렉션을 허용합니다.

#### 2.7.3) 양방향 tunnel 사용 {#tunnel.bidirectional}

인바운드와 아웃바운드 통신에 두 개의 별도 tunnel을 사용하는 현재 전략은 유일한 기법이 아니며, 익명성에 영향을 미칩니다. 긍정적인 측면에서는, 별도의 tunnel을 사용함으로써 tunnel 참가자들에게 분석을 위해 노출되는 트래픽 데이터를 줄입니다. 예를 들어, 웹 브라우저의 아웃바운드 tunnel에 있는 피어들은 HTTP GET의 트래픽만 볼 수 있고, 인바운드 tunnel의 피어들은 tunnel을 통해 전달되는 페이로드를 보게 됩니다. 양방향 tunnel의 경우, 모든 참가자들이 예를 들어 한 방향으로 1KB가 전송되고 다른 방향으로 100KB가 전송되었다는 사실에 접근할 수 있습니다. 부정적인 측면에서는, 단방향 tunnel을 사용한다는 것은 프로파일링하고 고려해야 할 두 세트의 피어가 있다는 것을 의미하며, 선행자 공격(predecessor attack)의 증가된 속도를 해결하기 위해 추가적인 주의가 필요합니다. 아래에 설명된 tunnel 풀링과 구축 프로세스는 선행자 공격에 대한 우려를 최소화해야 하지만, 만약 원한다면 동일한 피어들을 따라 인바운드와 아웃바운드 tunnel을 모두 구축하는 것도 큰 문제가 되지 않을 것입니다.

#### 2.7.4) 더 작은 블록 크기 사용 {#tunnel.smallerhashes}

현재 우리의 AES 사용은 블록 크기를 16바이트로 제한하며, 이는 체크섬 블록 열 각각의 최소 크기를 제공합니다. 더 작은 블록 크기를 가진 다른 알고리즘을 사용하거나, 해시의 더 작은 부분으로 체크섬 블록을 안전하게 구성할 수 있다면 탐색해볼 가치가 있을 것입니다. 현재 각 홉에서 사용되는 16바이트는 충분히 적절할 것입니다.

## 3) Tunnel 구축 {#tunnel.building}

tunnel을 구축할 때, 생성자는 각 hop에 필요한 구성 데이터와 함께 요청을 보낸 다음, 잠재적 참여자가 동의하거나 동의하지 않는다는 응답을 기다려야 합니다. 이러한 tunnel 요청 메시지와 그 응답은 garlic encryption으로 래핑되어 키를 알고 있는 router만 해독할 수 있으며, 양방향으로 취하는 경로 역시 tunnel로 라우팅됩니다. tunnel을 생성할 때 염두에 두어야 할 세 가지 중요한 차원이 있습니다: 어떤 피어가 사용되는지(그리고 어디에), 요청이 어떻게 전송되는지(그리고 응답이 어떻게 수신되는지), 그리고 어떻게 유지되는지입니다.

### 3.1) Peer 선택 {#tunnel.peerselection}

두 가지 tunnel 유형인 인바운드와 아웃바운드 외에도, 서로 다른 tunnel에 사용되는 두 가지 피어 선택 방식이 있습니다 - 탐색형과 클라이언트형입니다. 탐색형 tunnel은 netDb 유지보수와 tunnel 유지보수 모두에 사용되며, 클라이언트 tunnel은 종단 간 클라이언트 메시지에 사용됩니다.

#### 3.1.1) 탐색 tunnel 피어 선택 {#tunnel.selection.exploratory}

탐색용 tunnel은 네트워크의 하위 집합에서 무작위로 선택된 피어들로 구성됩니다. 특정 하위 집합은 로컬 router와 그들의 tunnel 라우팅 요구사항에 따라 달라집니다. 일반적으로 탐색용 tunnel은 피어의 "실패하지 않지만 활성" 프로필 범주에 있는 무작위로 선택된 피어들로 구성됩니다. tunnel 라우팅 외에도 이러한 tunnel의 두 번째 목적은 활용도가 낮은 고용량 피어들을 찾아서 클라이언트 tunnel에서 사용하도록 승격시키는 것입니다.

#### 3.1.2) 클라이언트 tunnel 피어 선택 {#tunnel.selection.client}

클라이언트 tunnel은 더 엄격한 요구 사항으로 구축됩니다. 로컬 router는 "빠르고 고용량" 프로필 카테고리에서 피어를 선택하여 성능과 신뢰성이 클라이언트 애플리케이션의 요구 사항을 충족하도록 합니다. 그러나 클라이언트의 익명성 요구 사항에 따라 기본 선택을 넘어서 준수해야 할 몇 가지 중요한 세부 사항이 있습니다.

전임자 공격(predecessor attack)을 우려하는 일부 클라이언트의 경우, tunnel 선택은 피어들을 엄격한 순서로 유지할 수 있습니다 - A, B, C가 tunnel에 있다면, A 다음의 홉은 항상 B이고, B 다음의 홉은 항상 C입니다. 덜 엄격한 순서도 가능한데, A 다음의 홉이 B일 수는 있지만 B가 A보다 앞에 올 수는 없도록 보장합니다. 기타 구성 옵션에는 인바운드 tunnel 게이트웨이와 아웃바운드 tunnel 엔드포인트만 고정하거나 MTBF 비율로 순환시키는 기능이 포함됩니다.

### 3.2) 요청 전달 {#tunnel.request}

위에서 언급했듯이, tunnel 생성자가 어떤 피어들이 tunnel에 포함되어야 하고 어떤 순서로 배치되어야 하는지 알게 되면, 생성자는 각 피어에 필요한 정보를 포함하는 일련의 tunnel 요청 메시지를 구성합니다. 예를 들어, 참여하는 tunnel들은 메시지를 수신해야 하는 4바이트 tunnel ID, 메시지를 전송해야 하는 4바이트 tunnel ID, 다음 홉의 신원에 대한 32바이트 해시, 그리고 tunnel에서 레이어를 제거하는 데 사용되는 32바이트 레이어 키를 받게 됩니다. 물론 아웃바운드 tunnel 엔드포인트에는 "다음 홉"이나 "다음 tunnel ID" 정보가 제공되지 않습니다. 그러나 인바운드 tunnel 게이트웨이에는 암호화되어야 하는 순서대로 8개의 레이어 키가 제공됩니다(위에서 설명한 대로). 응답을 허용하기 위해 요청에는 피어가 자신의 결정을 garlic encryption할 수 있는 무작위 세션 태그와 무작위 세션 키, 그리고 해당 garlic이 전송되어야 하는 tunnel이 포함됩니다. 위의 정보 외에도 tunnel에 적용할 스로틀링, 사용할 패딩이나 배치 전략 등과 같은 다양한 클라이언트별 옵션이 포함될 수 있습니다.

모든 요청 메시지를 구축한 후, 대상 router에 대해 garlic으로 래핑되어 탐색 tunnel을 통해 전송됩니다. 수신 시, 해당 피어는 참여할 수 있는지 또는 참여할 것인지를 결정하고, 응답 메시지를 생성하여 제공된 정보로 garlic 래핑과 tunnel 라우팅을 모두 수행합니다. tunnel 생성자가 응답을 수신하면, 해당 홉에서 tunnel이 유효한 것으로 간주됩니다(승인된 경우). 모든 피어가 승인하면, tunnel이 활성화됩니다.

### 3.3) 풀링 {#tunnel.pooling}

효율적인 운영을 위해 router는 일련의 tunnel pool들을 유지하며, 각 pool은 특정 목적을 위해 사용되는 tunnel 그룹을 자체 구성으로 관리합니다. 해당 목적을 위해 tunnel이 필요할 때, router는 적절한 pool에서 무작위로 하나를 선택합니다. 전체적으로 두 개의 탐색용 tunnel pool이 있습니다 - 하나는 인바운드용, 하나는 아웃바운드용이며, 각각 router의 탐색 기본값을 사용합니다. 또한 각 로컬 목적지마다 한 쌍의 pool이 있습니다 - 하나는 인바운드 tunnel용, 하나는 아웃바운드 tunnel용입니다. 이러한 pool들은 로컬 목적지가 router에 연결될 때 지정된 구성을 사용하거나, 지정되지 않은 경우 router의 기본값을 사용합니다.

각 풀은 설정 내에서 몇 가지 핵심 설정을 가지고 있으며, 활성 상태로 유지할 tunnel 개수, 장애 발생 시를 대비해 유지할 백업 tunnel 개수, tunnel 테스트 빈도, tunnel 길이, 길이를 무작위화할지 여부, 교체 tunnel 구축 빈도, 그리고 개별 tunnel을 구성할 때 허용되는 기타 모든 설정들을 정의합니다.

### 3.4) 대안 {#tunnel.building.alternatives}

#### 3.4.1) 망원경식 구축 {#tunnel.building.telescoping}

터널 생성 메시지를 전송하고 수신하기 위해 탐색 터널을 사용하는 것과 관련하여 제기될 수 있는 한 가지 질문은 이것이 터널의 선행자 공격에 대한 취약성에 어떤 영향을 미치는지입니다. 이러한 터널의 끝점과 게이트웨이는 네트워크 전체에 무작위로 분산될 것이지만(터널 생성자도 해당 집합에 포함될 수 있음), 또 다른 대안은 [TOR](https://www.torproject.org/)에서 수행되는 것처럼 터널 경로 자체를 사용하여 요청과 응답을 전달하는 것입니다. 그러나 이는 터널 생성 중에 정보 누출로 이어질 수 있으며, 피어들이 터널이 구축되는 동안 타이밍이나 패킷 수를 모니터링하여 터널에서 나중에 얼마나 많은 홉이 있는지 발견할 수 있게 합니다. 다음 홉 구축을 계속하기 전에 무작위 수의 메시지에 대해 각 홉을 끝점으로 사용하는 것([2.7.2](#tunnel.reroute) 참조)과 같은 기술을 사용하여 이 문제를 최소화할 수 있습니다.

#### 3.4.2) 관리용 비탐색 tunnel {#tunnel.building.nonexploratory}

tunnel 구축 프로세스의 두 번째 대안은 router에게 비탐색적(non-exploratory) 인바운드 및 아웃바운드 풀의 추가 세트를 제공하여, tunnel 요청과 응답에 이를 사용하는 것입니다. router가 네트워크에 대한 잘 통합된 뷰를 가지고 있다고 가정하면 이는 필요하지 않을 것이지만, router가 어떤 방식으로든 분할되어 있다면, tunnel 관리를 위해 비탐색적 풀을 사용하는 것이 router의 파티션에 있는 피어들에 대한 정보 누출을 줄일 수 있을 것입니다.

## 4) Tunnel 스로틀링 {#tunnel.throttling}

I2P 내의 tunnel이 회선 교환 네트워크와 유사하지만, I2P 내의 모든 것은 엄격히 메시지 기반입니다 - tunnel은 단순히 메시지 전달을 체계화하는 데 도움이 되는 회계상의 기법일 뿐입니다. 메시지의 신뢰성이나 순서에 대한 가정은 하지 않으며, 재전송은 상위 계층(예: I2P의 클라이언트 계층 스트리밍 라이브러리)에 맡겨집니다. 이를 통해 I2P는 패킷 교환 네트워크와 회선 교환 네트워크 모두에서 사용할 수 있는 스로틀링 기법을 활용할 수 있습니다. 예를 들어, 각 router는 각 tunnel이 사용하는 데이터량의 이동 평균을 추적하고, 이를 해당 router가 참여하고 있는 다른 모든 tunnel의 평균과 결합하여, 자신의 용량과 사용률을 바탕으로 추가 tunnel 참여 요청을 수락하거나 거부할 수 있습니다. 반면에 각 router는 단순히 용량을 초과하는 메시지를 삭제할 수 있으며, 이는 일반 인터넷에서 사용되는 연구를 활용하는 것입니다.

## 5) 혼합/배칭 {#tunnel.mixing}

gateway와 각 hop에서 메시지를 지연, 재정렬, 재라우팅 또는 패딩하기 위해 어떤 전략을 사용해야 할까요? 이것을 어느 정도까지 자동으로 수행해야 하고, 얼마나 많은 부분을 tunnel별 또는 hop별 설정으로 구성해야 하며, tunnel 생성자(그리고 결국 사용자)가 이 작업을 어떻게 제어해야 할까요? 이 모든 것은 미지의 영역으로 남겨져 있으며, 향후 릴리스에서 해결될 예정입니다.
