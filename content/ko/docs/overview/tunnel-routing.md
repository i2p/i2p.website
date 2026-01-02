---
title: "터널 라우팅"
description: "I2P 터널 용어, 구성 및 생명주기 개요"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

I2P는 임시적이고 단방향인 tunnel을 구축합니다 — 암호화된 트래픽을 전달하는 router들의 순서가 정해진 시퀀스입니다. Tunnel은 **inbound**(메시지가 생성자를 향해 흐름) 또는 **outbound**(메시지가 생성자로부터 멀어지는 방향으로 흐름)로 분류됩니다.

일반적인 교환 과정에서 Alice의 메시지는 그녀의 아웃바운드 tunnel 중 하나를 통해 전송되고, 아웃바운드 엔드포인트는 Bob의 인바운드 tunnel 중 하나의 게이트웨이로 메시지를 전달하도록 지시받으며, 그 후 Bob은 자신의 인바운드 엔드포인트에서 메시지를 수신합니다.

![Alice가 자신의 아웃바운드 터널을 통해 Bob의 인바운드 터널로 연결하는 모습](/images/tunnelSending.png)

- **A**: Outbound Gateway (Alice)
- **B**: Outbound Participant
- **C**: Outbound Endpoint
- **D**: Inbound Gateway
- **E**: Inbound Participant
- **F**: Inbound Endpoint (Bob)

터널은 10분의 고정된 수명을 가지며, 메시지 크기나 타이밍 패턴을 기반으로 한 트래픽 분석을 방지하기 위해 1024바이트(tunnel 헤더를 포함하면 1028바이트)의 고정 크기 메시지를 전송합니다.

## 터널 용어집

- **Tunnel gateway:** 터널의 첫 번째 router. 인바운드 터널의 경우, 이 router의 신원이 게시된 [LeaseSet](/docs/specs/common-structures/)에 나타납니다. 아웃바운드 터널의 경우, gateway는 시작 router입니다 (위의 A와 D).
- **Tunnel endpoint:** 터널의 마지막 router (위의 C와 F).
- **Tunnel participant:** 터널의 중간 router (위의 B와 E). Participant는 자신의 위치나 터널 방향을 알 수 없습니다.
- **n-hop tunnel:** router 간 홉 수.
  - **0-hop:** Gateway와 endpoint가 동일한 router – 최소 익명성.
  - **1-hop:** Gateway가 endpoint에 직접 연결 – 낮은 지연시간, 낮은 익명성.
  - **2-hop:** 탐색 터널의 기본값; 보안과 성능의 균형.
  - **3-hop:** 강력한 익명성이 필요한 애플리케이션에 권장.
- **Tunnel ID:** router당 및 홉당 고유한 4바이트 정수로, 생성자가 무작위로 선택합니다. 각 홉은 서로 다른 ID로 수신하고 전달합니다.

## 터널 구축 정보

gateway, participant, endpoint 역할을 수행하는 라우터들은 Tunnel Build Message 내에서 서로 다른 레코드를 받습니다. 현대 I2P는 두 가지 방법을 지원합니다:

- **ElGamal** (레거시, 528바이트 레코드)
- **ECIES-X25519** (현재, Short Tunnel Build Message – STBM을 통한 218바이트 레코드)

### Information Distributed to Participants

**게이트웨이가 수신하는 것:** - Tunnel 계층 키 (터널 유형에 따라 AES-256 또는 ChaCha20 키) - Tunnel IV 키 (초기화 벡터 암호화용) - 응답 키 및 응답 IV (빌드 응답 암호화용) - Tunnel ID (인바운드 게이트웨이만 해당) - 다음 홉 식별 해시 및 tunnel ID (종단이 아닌 경우)

**중간 참여자가 받는 정보:** - 자신의 홉에 대한 터널 레이어 키와 IV 키 - Tunnel ID와 다음 홉 정보 - 빌드 응답 암호화를 위한 응답 키와 IV

**엔드포인트가 수신하는 정보:** - Tunnel 레이어 및 IV 키 - 응답 router 및 tunnel ID (아웃바운드 엔드포인트만 해당) - 응답 키 및 IV (아웃바운드 엔드포인트만 해당)

자세한 내용은 [Tunnel Creation Specification](/docs/specs/implementation/) 및 [ECIES Tunnel Creation Specification](/docs/specs/implementation/)을 참조하세요.

## Tunnel Pooling

라우터는 중복성과 부하 분산을 위해 터널을 **터널 풀**로 그룹화합니다. 각 풀은 여러 개의 병렬 터널을 유지하여 하나가 실패할 때 장애 조치를 허용합니다. 내부적으로 사용되는 풀은 **탐색 터널(exploratory tunnels)**이며, 애플리케이션별 풀은 **클라이언트 터널(client tunnels)**입니다.

각 destination은 I2CP 옵션(터널 수, 백업 수, 길이 및 QoS 매개변수)으로 구성된 별도의 인바운드 및 아웃바운드 풀을 유지합니다. Router는 터널 상태를 모니터링하고, 주기적인 테스트를 실행하며, 풀 크기를 유지하기 위해 실패한 터널을 자동으로 재구축합니다.

## 터널 풀링

**0-hop Tunnel** : 그럴듯한 부인 가능성만 제공합니다. 트래픽은 항상 동일한 router에서 시작되고 종료됩니다 — 익명 사용에는 권장하지 않습니다.

**1-hop 터널**: 수동적 관찰자에 대해 기본적인 익명성을 제공하지만, 공격자가 해당 단일 홉을 제어하는 경우 취약합니다.

**2-홉 터널**: 두 개의 원격 라우터를 포함하며 공격 비용을 상당히 증가시킵니다. 탐색 풀의 기본값입니다.

**3-hop Tunnel**: 강력한 익명성 보호가 필요한 애플리케이션에 권장됩니다. 추가 hop은 의미 있는 보안 향상 없이 지연 시간만 증가시킵니다.

**기본값**: Router는 **2-hop** 탐색 tunnel과 애플리케이션별 **2 또는 3 hop** 클라이언트 tunnel을 사용하여 성능과 익명성의 균형을 맞춥니다.

## 터널 길이

Router는 outbound tunnel을 통해 inbound tunnel로 `DeliveryStatusMessage`를 전송하여 주기적으로 터널을 테스트합니다. 테스트가 실패하면 두 터널 모두 부정적인 프로파일 가중치를 받습니다. 연속적인 실패는 터널을 사용 불가능한 것으로 표시하며, router는 대체 터널을 재구축하고 새로운 LeaseSet을 게시합니다. 결과는 [peer 선택 시스템](/docs/overview/tunnel-routing/)에서 사용되는 peer 용량 메트릭에 반영됩니다.

## 터널 테스트

Router는 비대화형 **telescoping** 방식을 사용하여 tunnel을 구성합니다: 단일 Tunnel Build Message가 hop별로 전파됩니다. 각 hop은 자신의 레코드를 복호화하고, 응답을 추가한 후 메시지를 전달합니다. 최종 hop은 상관관계 분석을 방지하기 위해 다른 경로를 통해 집계된 빌드 응답을 반환합니다. 최신 구현에서는 ECIES를 위해 **Short Tunnel Build Messages (STBM)**를 사용하고 레거시 경로를 위해 **Variable Tunnel Build Messages (VTBM)**를 사용합니다. 각 레코드는 ElGamal 또는 ECIES-X25519를 사용하여 hop별로 암호화됩니다.

## 터널 생성

터널 트래픽은 다층 암호화를 사용합니다. 메시지가 터널을 통과할 때 각 홉(hop)은 암호화 계층을 추가하거나 제거합니다.

- **ElGamal tunnel:** PKCS#5 패딩을 사용한 페이로드에 대한 AES-256/CBC.
- **ECIES tunnel:** 인증된 암호화를 위한 ChaCha20 또는 ChaCha20-Poly1305.

각 홉에는 두 개의 키가 있습니다: **레이어 키**와 **IV 키**. Router들은 IV를 복호화하고, 이를 사용하여 페이로드를 처리한 다음, 전달하기 전에 IV를 다시 암호화합니다. 이 이중 IV 방식은 메시지 태깅을 방지합니다.

아웃바운드 게이트웨이는 모든 레이어를 미리 복호화하여 모든 참여자가 암호화를 추가한 후 엔드포인트가 평문을 받도록 합니다. 인바운드 터널은 반대 방향으로 암호화합니다. 참여자는 터널 방향이나 길이를 판별할 수 없습니다.

## 터널 암호화

- 네트워크 부하 분산을 위한 동적 tunnel 수명 및 적응형 풀 크기 조정
- 대체 tunnel 테스트 전략 및 개별 홉 진단
- 선택적 작업 증명 또는 대역폭 인증서 검증 (API 0.9.65+에서 구현됨)
- 엔드포인트 혼합을 위한 트래픽 셰이핑 및 chaff 삽입 연구
- ElGamal의 지속적인 폐기 및 ECIES-X25519로의 마이그레이션

## 지속적인 개발

- [Tunnel Implementation Specification](/docs/specs/implementation/)
- [Tunnel Creation Specification (ElGamal)](/docs/specs/implementation/)
- [Tunnel Creation Specification (ECIES-X25519)](/docs/specs/implementation/)
- [Tunnel Message Specification](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Network Database](/docs/specs/common-structures/)
- [Peer Profiling and Selection](/docs/overview/tunnel-routing/)
- [I2P 위협 모델](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag 암호화](/docs/legacy/elgamal-aes/)
- [I2CP 옵션](/docs/specs/i2cp/)
