---
title: "Tunnel 운영 가이드"
description: "I2P tunnels를 통해 트래픽을 생성, 암호화 및 전송하기 위한 통합 사양."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Scope:** 이 가이드는 tunnel 구현, 메시지 형식, 그리고 두 가지 tunnel 생성 사양(ECIES 및 레거시 ElGamal)을 통합합니다. 기존 딥 링크는 위의 별칭을 통해 계속 작동합니다.

## Tunnel 모델 {#tunnel-model}

I2P는 *단방향 tunnels*을 통해 페이로드를 전달합니다: 이는 단일 방향으로 트래픽을 운반하는 routers의 순서 있는 집합입니다. 두 목적지 간의 완전한 왕복 통신에는 네 개의 tunnels(발신 2개, 수신 2개)가 필요합니다.

용어는 [Tunnel 개요](/docs/overview/tunnel-routing/)부터 살펴보고, 운용 세부 사항은 이 가이드를 참고하세요.

### 메시지 라이프사이클 {#message-lifecycle}

1. tunnel **게이트웨이**는 하나 이상의 I2NP 메시지를 일괄 처리하고, 이를 분할하며, 전달 지시를 작성한다.
2. 게이트웨이는 페이로드를 고정 크기(1024&nbsp;B)의 tunnel 메시지로 캡슐화하고, 필요 시 패딩을 추가한다.
3. 각 **참여자**는 이전 홉을 검증하고, 자신의 암호화 계층을 적용하며, `{nextTunnelId, nextIV, encryptedPayload}`를 다음 홉으로 전달한다.
4. tunnel **엔드포인트**는 마지막 계층을 제거하고, 전달 지시를 처리하며, 조각을 재조립하고, 재구성된 I2NP 메시지를 전달한다.

중복 감지는 IV(초기화 벡터)와 첫 번째 암호문 블록의 배타적 OR 결과를 키로 사용하는 감쇠형 블룸 필터를 이용하여 IV 교체에 기반한 태깅 공격을 방지한다.

### 역할 한눈에 보기 {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### 암호화 워크플로우 {#encryption-workflow}

- **인바운드 tunnels:** 게이트웨이가 자신의 레이어 키로 한 번 암호화하고, 다운스트림 참가자들은 생성자가 최종 페이로드를 복호화할 때까지 계속 암호화를 덧씌운다.
- **아웃바운드 tunnels:** 게이트웨이는 각 홉의 암호화에 대한 역연산을 미리 적용하여, 그 결과 각 참가자가 암호화한다. 엔드포인트가 암호화하면, 게이트웨이가 보낸 원래 평문이 드러난다.

양방향 모두 `{tunnelId, IV, encryptedPayload}`를 다음 홉으로 전달한다.

---

## Tunnel 메시지 형식 {#tunnel-message-format}

tunnel 게이트웨이는 페이로드 길이를 숨기고 홉 단위 처리를 단순화하기 위해 I2NP 메시지를 여러 개의 고정 크기 봉투로 분할한다.

### 암호화된 레이아웃 {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – 다음 홉을 위한 32비트 식별자(0이 아니며, 각 빌드 사이클마다 변경됨).
- **IV(초기화 벡터)** – 메시지마다 선택되는 16바이트 AES IV.
- **암호화된 페이로드** – 1008바이트의 AES-256-CBC 암호문.

총 크기: 1028 바이트.

### 복호화된 레이아웃 {#decrypted-layout}

한 홉이 자신의 암호화 계층을 제거한 후:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **체크섬**은 복호화된 블록을 검증합니다.
- **패딩**은 0이 아닌 임의의 바이트로 이루어지며 마지막은 0 바이트로 종료됩니다.
- **전달 지침**은 엔드포인트(종단점)에게 각 프래그먼트를 어떻게 처리할지 알려줍니다(로컬 전달, 다른 tunnel로 전달 등).
- **프래그먼트**는 하위의 I2NP 메시지를 운반합니다; 엔드포인트는 이를 상위 계층으로 전달하기 전에 재조립합니다.

### 처리 단계 {#processing-steps}

1. 게이트웨이는 I2NP 메시지를 단편화하여 큐에 넣고, 재조립을 위해 부분 조각을 잠시 보관합니다.
2. 게이트웨이는 적절한 레이어 키로 페이로드를 암호화하고, tunnel ID와 IV(초기화 벡터)를 설정합니다.
3. 각 참가자는 IV(AES-256/ECB)를 암호화한 다음 페이로드(AES-256/CBC)를 암호화하고, 이어서 IV를 재암호화한 후 메시지를 전달합니다.
4. 엔드포인트는 역순으로 복호화한 뒤 체크섬을 검증하고, 전달 지시를 처리하여 조각을 재조립합니다.

---

## Tunnel 생성 (ECIES-X25519) {#tunnel-creation-ecies}

최신 routers는 ECIES-X25519 키를 사용해 tunnels을 구축하여 빌드 메시지를 축소하고 전방향 보안성을 가능하게 합니다.

- **빌드 메시지:** 단일 `TunnelBuild`(또는 `VariableTunnelBuild`) I2NP 메시지는 홉당 하나씩, 암호화된 빌드 레코드 1–8개를 담아 운반한다.
- **레이어 키:** 생성자는 홉의 정적 X25519 신원 키와 생성자의 에페메럴(임시) 키를 사용하여 HKDF로 홉별 레이어 키, IV, 회신 키를 도출한다.
- **처리:** 각 홉은 자신의 레코드를 복호화하고, 요청 플래그를 검증한 뒤, 회신 블록(성공 또는 상세 실패 코드)을 기록하고, 남은 레코드들을 재암호화하여 메시지를 다음으로 전달한다.
- **회신:** 생성자는 garlic encryption(갈릭 암호화)으로 래핑된 회신 메시지를 수신한다. 실패로 표시된 레코드에는 router가 피어를 프로파일링할 수 있도록 심각도 코드가 포함된다.
- **호환성:** router는 하위 호환성을 위해 여전히 레거시 ElGamal 빌드를 허용할 수 있지만, 새로운 tunnel은 기본적으로 ECIES를 사용한다.

> 필드별 상수와 키 파생 관련 노트는 ECIES(타원곡선 통합 암호화 방식) 제안 이력과 router 소스 코드를 참조하세요; 이 가이드는 동작 흐름을 다룹니다.

---

## 레거시 Tunnel 생성 (ElGamal-2048) {#tunnel-creation-elgamal}

원래 tunnel 빌드 형식은 ElGamal 공개 키를 사용했다. 최신 router들은 하위 호환성을 위해 제한적인 지원을 유지한다.

> **상태:** 폐기됨. 역사적 참고용 및 레거시 호환 도구를 유지 관리하는 이들을 위해 여기 보존되어 있습니다.

- **비대화형 망원경식 확장:** 단일 빌드 메시지가 전체 경로를 따라 이동한다. 각 홉은 자신에게 해당하는 528바이트 레코드를 복호화하고 메시지를 갱신한 뒤 이를 전달한다.
- **가변 길이:** Variable Tunnel Build Message (VTBM, 가변 Tunnel 빌드 메시지)은 1–8개의 레코드를 허용했다. 이전의 고정형 메시지는 tunnel 길이를 숨기기 위해 항상 8개의 레코드를 포함했다.
- **요청 레코드 레이아웃:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **플래그:** 비트 7은 inbound gateway (IBGW)를 나타내며; 비트 6은 outbound endpoint (OBEP)를 지정합니다. 둘은 서로 배타적입니다.
- **암호화:** 각 레코드는 해당 홉의 공개키로 ElGamal-2048로 암호화됩니다. 대칭 AES-256-CBC 계층화는 의도된 홉만 그 레코드를 읽을 수 있도록 보장합니다.
- **핵심 사실:** tunnel ID는 0이 아닌 32비트 값입니다; 생성자는 실제 tunnel 길이를 숨기기 위해 더미 레코드를 삽입할 수 있습니다; 신뢰성은 실패한 빌드를 재시도하는 데 달려 있습니다.

---

## Tunnel 풀과 수명 주기 {#tunnel-pools}

각 router는 탐색 트래픽과 각 I2CP 세션 각각에 대해 독립적인 수신 및 발신 tunnel 풀을 유지합니다.

- **피어 선택:** exploratory tunnel은 다양성을 높이기 위해 “active, not failing” 피어 버킷에서 선택하고; client tunnel은 빠르고 고용량의 피어를 선호합니다.
- **결정적 정렬:** 피어는 `SHA256(peerHash || poolKey)`와 풀의 랜덤 키 사이의 XOR 거리로 정렬됩니다. 키는 재시작 시 교체되어, 단일 실행 동안에는 안정성을 제공하면서 실행 간에는 predecessor attacks(선행자 공격)을 저해합니다.
- **수명 주기:** routers는 {mode, direction, length, variance} 튜플별로 과거 빌드 시간을 추적합니다. tunnel의 만료가 가까워지면 교체를 일찍 시작하고; 실패가 발생하면 router는 병렬 빌드를 늘리되, 진행 중인 시도 건수에는 상한을 둡니다.
- **구성 조절 항목:** 활성/백업 tunnel 개수, 홉 길이와 분산, zero-hop 허용, 빌드 속도 제한은 모두 풀별로 조정 가능합니다.

---

## 혼잡과 신뢰성 {#congestion}

tunnels는 회로와 유사하지만, routers는 그것들을 메시지 큐로 취급한다. 지연 시간을 일정 범위로 제한하기 위해 가중치 랜덤 조기 폐기(WRED)가 사용된다:

- 사용률이 설정된 한계값에 가까워질수록 드롭 확률이 상승합니다.
- 참여자들은 고정 크기 프래그먼트를 고려하며; 게이트웨이/엔드포인트는 결합된 프래그먼트 크기를 기준으로 드롭하여 큰 페이로드를 우선적으로 드롭합니다.
- 네트워크 자원 낭비를 최소화하기 위해 아웃바운드 엔드포인트가 다른 역할보다 먼저 드롭합니다.

보장된 전달은 [Streaming library(스트리밍 라이브러리)](/docs/specs/streaming/)와 같은 상위 계층에 맡겨집니다. 신뢰성이 필요한 애플리케이션은 재전송과 승인(acknowledgment)을 스스로 처리해야 합니다.

---

## 추가 참고 자료 {#further-reading}

- [단방향 Tunnels (역사적)](/docs/legacy/unidirectional-tunnels/)
- [피어 선택](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel 개요](/docs/overview/tunnel-routing/)
- [이전 Tunnel 구현](/docs/legacy/old-implementation/)
