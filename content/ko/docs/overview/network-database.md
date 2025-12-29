---
title: "네트워크 데이터베이스"
description: "I2P의 분산 네트워크 데이터베이스(netDb) 이해 - router 연락처 정보와 destination(종단 식별자) 조회를 위한 특화된 분산 해시 테이블(DHT)"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. 개요

**netDb**(I2P의 특수 목적 분산 네트워크 데이터베이스)은 두 가지 유형의 데이터만을 포함합니다: - **RouterInfos** – router 연락 정보 - **LeaseSets** – 목적지 연락 정보

모든 데이터는 암호학적으로 서명되어 있으며 검증 가능합니다. 각 항목에는 더 이상 유효하지 않은 항목을 제거하고 오래된 항목을 교체하기 위한 liveliness information(항목의 생존/유효 상태를 나타내는 정보)이 포함되어 있어, 특정 유형의 공격으로부터 보호합니다.

배포에는 **floodfill**(네트워크 전역으로 데이터를 확산해 채우는 방식) 메커니즘이 사용되며, 일부 routers가 분산 데이터베이스를 유지 관리합니다.

---

## 2. RouterInfo (router 정보, netDb 항목)

router들이 다른 router에 연락해야 할 때, 다음을 포함하는 **RouterInfo** 번들을 교환합니다:

- **Router 식별자** – 암호화 키, 서명 키, 인증서
- **연결 주소** – router에 접속하는 방법
- **게시 타임스탬프** – 이 정보가 게시된 시점
- **임의 텍스트 옵션** – 기능 플래그와 설정
- **암호학적 서명** – 진정성을 증명

### 2.1 기능 플래그

router는 자신의 RouterInfo에 문자 코드로 기능을 표시합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 대역폭 분류

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 네트워크 ID 값

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 RouterInfo 통계

Routers는 네트워크 분석을 위해 선택적 건전성 통계를 게시합니다: - Exploratory tunnel(탐색용 tunnel) 구축 성공/거부/시간 초과 비율 - 1시간 평균 participating tunnel(중계 참여 tunnel) 수

통계는 `stat_(statname).(statperiod)` 형식을 따르며 값은 세미콜론으로 구분됩니다.

**예시 통계:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers는 또한 다음을 게시할 수 있습니다: `netdb.knownLeaseSets` 및 `netdb.knownRouters`

### 2.5 패밀리 옵션

릴리스 0.9.24부터 routers는 family(패밀리) 소속을 선언할 수 있습니다(동일 운영자):

- **family**: 패밀리 이름
- **family.key**: 서명 유형 코드와 base64로 인코딩된 서명용 공개키를 이어붙인 값
- **family.sig**: 패밀리 이름과 32바이트 router 해시에 대한 서명

같은 family(동일 운영자임을 선언한 router 그룹)에 속한 여러 router는 단일 tunnel에서 함께 사용되지 않는다.

### 2.6 RouterInfo 만료

- 가동 후 첫 1시간 동안 만료 없음
- 저장된 RouterInfos(라우터 정보)가 25개 이하인 경우 만료 없음
- 로컬 개수가 증가할수록 만료 기간이 짧아짐 (라우터가 120대 미만일 때 72시간; 300대일 때 약 30시간)
- SSU 소개자는 약 1시간 후 만료
- Floodfills는 모든 로컬 RouterInfos에 대해 1시간 만료 시간을 사용

---

## 3. LeaseSet(I2P에서 목적지가 메시지를 받기 위해 사용하는 인바운드 tunnel 정보를 담은 공개 레코드)

**LeaseSets** 는 특정 목적지에 대한 tunnel 진입 지점을 문서화하며, 다음을 명시합니다:

- **Tunnel 게이트웨이 router의 식별자**
- **4바이트 tunnel ID**
- **Tunnel 만료 시간**

LeaseSets에는 다음이 포함됩니다: - **Destination** (목적지) – 암호화 키, 서명 키, 인증서 - **추가 암호화 공개 키** – 종단 간 garlic encryption을 위해 - **추가 서명 공개 키** – 무효화를 위한 용도(현재는 사용되지 않음) - **암호학적 서명**

### 3.1 LeaseSet 종류

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 LeaseSet 만료

일반적인 LeaseSet은 포함된 lease(경로 임대 항목) 중 가장 늦은 만료 시점에 만료된다. LeaseSet2의 만료 시점은 헤더에 명시된다. EncryptedLeaseSet과 MetaLeaseSet의 만료 시점은 달라질 수 있으며, 최대값이 강제 적용될 수 있다.

---

## 4. 부트스트래핑

분산형 netDb에 참여하려면 최소한 하나의 피어 참조가 필요합니다. **Reseeding**(초기 피어 정보를 받아오는 과정)은 자원봉사자들의 netDb 디렉터리에서 RouterInfo 파일(`routerInfo-$hash.dat`)을 가져옵니다. 최초 실행 시에는 무작위로 선택된 하드코딩된 URL에서 자동으로 가져옵니다.

---

## 5. Floodfill 메커니즘

floodfill netDb는 단순한 분산 저장 방식을 사용한다: 데이터를 가장 가까운 floodfill 피어에게 전송한다. floodfill가 아닌 피어가 store(저장) 메시지를 보내면, floodfill 피어는 특정 키에 가장 가까운 floodfill 피어의 일부에게 이를 전달한다.

Floodfill 참여는 RouterInfo에서 기능 플래그(`f`)로 표시됩니다.

### 5.1 Floodfill 옵트인 요건

Tor의 하드코딩된 신뢰할 수 있는 디렉터리 서버와 달리, I2P의 floodfill(특정 router가 netDb 정보를 저장·배포하는 역할) 집합은 **신뢰되지 않는** 상태이며 시간이 지남에 따라 변합니다.

Floodfill은 다음 요구 사항을 충족하는 고대역폭 router에서만 자동으로 활성화됩니다: - 최소 128 KBytes/sec의 공유 대역폭 (수동 구성) - 추가 건전성 테스트를 통과해야 함 (발신 메시지 큐 지연 시간, 작업 지연)

현재 자동 옵트인으로 인해 약 **6%의 네트워크 floodfill 참여**가 나타납니다.

수동으로 설정된 floodfill(네트워크 데이터베이스를 유지·배포하는 특수 노드)은 자동으로 자원봉사하는 노드들과 함께 존재한다. floodfill 수가 임계값 아래로 떨어지면, 대역폭이 높은 router가 자동으로 자원봉사한다. floodfill이 너무 많아지면, 해당 router들은 스스로 floodfill 역할을 해제한다.

### 5.2 Floodfill 역할

netDb 저장 요청을 수락하고 쿼리에 응답하는 것 외에도, floodfills는 표준 router 기능을 수행합니다. 일반적으로 대역폭이 더 높아 더 많은 tunnel에 참여하지만, 이는 데이터베이스 서비스와 직접적인 관련은 없습니다.

---

## 6. Kademlia 근접성 메트릭

netDb는 XOR 기반의 **Kademlia 방식** 거리 측정법을 사용한다. RouterIdentity(라우터 식별자) 또는 Destination(목적지)의 SHA256 해시가 Kademlia 키를 생성한다(LS2 Encrypted LeaseSets의 경우는 제외되며, 이 경우 type byte 3와 blinded public key(블라인드 처리된 공개키)를 합친 값의 SHA256을 사용한다).

### 6.1 키 공간 회전

Sybil attack(다중 신원 위조 공격)의 비용을 높이기 위해, `SHA256(key)` 대신 시스템은 다음을 사용합니다:

```
SHA256(key + yyyyMMdd)
```
여기서 날짜는 8바이트 ASCII 형식의 UTC 날짜입니다. 이렇게 하면 **routing key**(라우팅 키)가 생성되며, UTC 자정마다 매일 변경됩니다—이를 **keyspace rotation**(키스페이스 회전)이라고 합니다.

라우팅 키는 I2NP 메시지에서 절대 전송되지 않으며, 오직 로컬 거리 판정에만 사용된다.

---

## 7. Network Database(네트워크 데이터베이스) 분할

기존의 Kademlia DHT(분산 해시 테이블)는 저장된 정보의 연결 불가능성을 보장하지 못한다. I2P는 **segmentation(분할)**을 구현하여 클라이언트 tunnel을 router와 연계하려는 공격을 방지한다.

### 7.1 세분화 전략

Routers는 다음을 추적함: - 엔트리가 client tunnel을 통해 도착했는지 또는 직접 도착했는지 - tunnel을 통해서라면 어떤 client tunnel/목적지인지 - 다수의 tunnel 경유 도착을 추적함 - 저장과 조회 응답을 구분함

Java와 C++ 구현은 둘 다 다음을 사용합니다: - router 컨텍스트에서 직접 조회/floodfill 작업을 위한 **"메인" netDb** - 클라이언트 컨텍스트에서 클라이언트 tunnel로 전송되는 엔트리를 수집하는 **"Client Network Databases"**(클라이언트 네트워크 데이터베이스) 또는 **"Sub-Databases"**(하위 데이터베이스)

클라이언트 netDbs는 클라이언트의 수명 동안에만 존재하며, 클라이언트 tunnel 항목만을 포함합니다. 클라이언트 tunnels에서 온 항목은 직접 수신과 중복될 수 없습니다.

각 netDb는 엔트리가 저장으로 도착했는지(조회 요청에 응답) 아니면 조회 응답으로 도착했는지(이전에 동일한 목적지로 저장한 적이 있을 때만 응답) 여부를 추적한다. 클라이언트는 메인 netDb 엔트리로는 질의에 절대 응답하지 않고, 클라이언트 네트워크 데이터베이스 엔트리로만 응답한다.

복합 전략은 클라이언트-router 연관 공격에 맞서 netDb를 **분할한다**.

---

## 8. 저장, 검증 및 조회

### 8.1 RouterInfo(라우터 정보)를 피어에 저장

NTCP 또는 SSU 전송 연결 초기화 중에 로컬 RouterInfo(라우터 정보) 교환을 포함하는 I2NP `DatabaseStoreMessage`.

### 8.2 피어에 대한 LeaseSet 저장

로컬 LeaseSet을 포함하는 I2NP `DatabaseStoreMessage`는 Destination 트래픽에 번들된 garlic encryption으로 암호화된 메시지를 통해 주기적으로 교환되며, LeaseSet 조회 없이도 응답할 수 있도록 한다.

### 8.3 Floodfill 선택

`DatabaseStoreMessage`는 현재 라우팅 키에 가장 가까운 floodfill로 전송됩니다. 가장 가까운 floodfill은 로컬 데이터베이스 검색을 통해 찾습니다. 실제로 가장 가까운 것이 아니더라도, 플러딩은 여러 floodfills로 전송하여 이를 "더 가까운" 곳으로 퍼뜨립니다.

전통적인 Kademlia는 삽입 전에 "find-closest"(가장 가까운 노드 탐색) 검색을 사용한다. I2NP에는 그러한 메시지가 없지만, routers는 진정한 최근접 피어 발견을 보장하기 위해 최하위 비트를 뒤집은 (`key ^ 0x01`) 값으로 반복 검색을 수행할 수 있다.

### 8.4 Floodfills로의 RouterInfo 저장

Routers는 floodfill에 직접 연결해 Reply Token(응답 토큰)이 0이 아닌 I2NP `DatabaseStoreMessage`를 보내 RouterInfo(라우터 정보)를 게시한다. 메시지는 end-to-end garlic encryption이 적용되지 않는다(직접 연결, 중간 경유지 없음). floodfill은 Reply Token을 Message ID로 사용해 `DeliveryStatusMessage`로 응답한다.

router는 exploratory tunnel을 통해 RouterInfo를 보낼 수도 있다 (연결 제한, 비호환성, IP 은닉). floodfill(네트워크 데이터베이스를 담당하는 노드)은 과부하 상태에서는 이러한 저장 요청을 거부할 수 있다.

### 8.5 Floodfills로의 LeaseSet 저장

LeaseSet 저장은 RouterInfo보다 더 민감하다. router는 LeaseSet이 자신과 연관되지 않도록 반드시 방지해야 한다.

Routers는 0이 아닌 Reply Token을 포함한 `DatabaseStoreMessage`를 outbound client tunnel을 통해 전송하여 LeaseSet을 게시한다. 메시지는 Destination(목적지)의 Session Key Manager를 사용해 종단 간 garlic encryption으로 암호화되어, tunnel의 outbound endpoint에서 노출되지 않는다. Floodfill은 inbound tunnel을 통해 반환되는 `DeliveryStatusMessage`로 응답한다.

### 8.6 플러딩 프로세스

floodfill 노드들은 로컬에 저장하기 전에, 부하, netdb 크기 및 기타 요인에 따라 달라지는 적응형 기준을 사용하여 RouterInfo(라우터 정보)/LeaseSet을 검증한다.

유효한 더 최신 데이터를 수신하면, floodfill은 라우팅 키에 가장 가까운 floodfill routers 3개를 조회하여 이를 "flood"합니다. 직접 연결에서는 Reply Token(응답 토큰)이 0인 I2NP `DatabaseStoreMessage`를 전송합니다. 다른 routers는 응답하거나 다시 "flood"하지 않습니다.

**중요한 제약 사항:** - Floodfills는 tunnels을 통해 전파해서는 안 됨; 직접 연결만 사용 - Floodfills는 만료된 LeaseSet 또는 1시간 이상 전에 게시된 RouterInfo(router 정보)를 절대 전파하지 않음

### 8.7 RouterInfo 및 LeaseSet 조회

I2NP `DatabaseLookupMessage`는 floodfill routers로부터 netdb 항목을 요청한다. 조회는 아웃바운드 탐색용 tunnel을 통해 전송되며, 응답은 인바운드 탐색용 tunnel로 반환 경로를 지정한다.

조회 요청은 일반적으로 요청된 키에 가장 가까운 "양호한" floodfill routers 두 곳으로 병렬로 전송된다.

- **로컬 일치**: I2NP `DatabaseStoreMessage` 응답을 수신합니다
- **로컬 일치 없음**: 키에 가까운 다른 floodfill router 참조가 포함된 I2NP `DatabaseSearchReplyMessage`를 수신합니다

LeaseSet 조회는 종단 간 garlic encryption을 사용합니다(0.9.5부터). RouterInfo(router의 공개 정보 레코드) 조회는 ElGamal의 높은 오버헤드 때문에 암호화되지 않으며, 그 결과 outbound endpoint(아웃바운드 터널의 종료 지점)에서의 도청에 취약합니다.

0.9.7부터 조회 응답에는 세션 키와 태그가 포함되며, 인바운드 게이트웨이에서 응답을 볼 수 없도록 합니다.

### 8.8 반복적 조회

0.8.9 이전: 재귀적 또는 반복적 라우팅 없이 두 개의 병렬 중복 조회.

0.8.9 기준: **Iterative lookups**는 중복 없이 구현됨—더 효율적이고 신뢰성이 높으며, 불완전한 floodfill(플러드필) 정보 환경에 적합함. 네트워크가 커지고 router가 아는 floodfill의 수가 줄어들수록, 조회의 복잡도는 O(log n)에 가까워진다.

더 가까운 피어 참조가 없어도 반복적 조회는 계속되어 악의적 블랙홀링을 방지합니다. 현재 설정된 최대 쿼리 횟수와 타임아웃이 적용됩니다.

### 8.9 검증

**RouterInfo(라우터 정보) 검증**: "Practical Attacks Against the I2P Network" 논문에서 설명된 공격을 방지하기 위해 0.9.7.1부터 비활성화되었습니다.

**LeaseSet 검증**: Routers는 약 10초 동안 기다린 뒤, outbound client tunnel을 통해 다른 floodfill에서 조회한다. 종단 간 garlic encryption은 outbound endpoint에서 보이지 않도록 숨긴다. 응답은 inbound tunnels을 통해 돌아온다.

0.9.7부터, 응답은 인바운드 게이트웨이에 세션 키/태그가 노출되지 않도록 암호화된다.

### 8.10 탐색

**탐색**은 새로운 router를 파악하기 위해 임의의 키로 netdb를 조회하는 과정을 수반한다. Floodfill은 요청된 키에 가까운, floodfill이 아닌 router 해시를 담은 `DatabaseSearchReplyMessage`로 응답한다. 탐색 쿼리는 `DatabaseLookupMessage`에 특수 플래그를 설정한다.

---

## 9. 멀티호밍

동일한 개인/공개 키(전통적인 `eepPriv.dat`)를 사용하는 Destination(통신 목적지 식별자)은 동시에 여러 router에서 호스팅될 수 있습니다. 각 인스턴스는 주기적으로 서명된 LeaseSet을 게시하며, 조회 요청자에게는 가장 최근에 게시된 LeaseSet이 반환됩니다. LeaseSet의 수명이 최대 10분이므로, 중단 기간은 길어도 약 10분을 넘지 않습니다.

0.9.38부터, **Meta LeaseSets**는 공통 서비스를 제공하는 별도의 Destinations(I2P 목적지 식별자)를 사용하여 대규모 멀티홈드 서비스를 지원합니다. Meta LeaseSet 항목은 Destinations 또는 다른 Meta LeaseSets이며, 만료 시간은 최대 18.2시간입니다. 이를 통해 공통 서비스를 호스팅하는 Destinations를 수백/수천 개까지 확장할 수 있습니다.

---

## 10. 위협 분석

약 1700개의 floodfill routers가 현재 운영 중입니다. 네트워크가 성장할수록 대부분의 공격은 수행하기 더 어려워지거나 영향이 줄어듭니다.

### 10.1 일반적인 완화책

- **성장**: floodfills가 많을수록 공격이 더 어렵거나 영향이 줄어듭니다
- **중복성**: 모든 netdb 항목은 플러딩을 통해 키에 가장 가까운 3개의 floodfill routers에 저장됩니다
- **서명**: 모든 항목은 생성자가 서명했으며, 위조는 불가능합니다

### 10.2 느리거나 응답하지 않는 router

Routers는 floodfills에 대한 확장된 피어 프로필 통계를 유지합니다: - 평균 응답 시간 - 쿼리 응답 비율 - 저장 검증 성공 비율 - 마지막으로 성공한 저장 - 마지막으로 성공한 조회 - 마지막 응답

Routers는 가장 가까운 floodfill을 선택하기 위한 "goodness"(적합도)를 결정할 때 이러한 메트릭을 사용한다. 완전히 응답하지 않는 Routers는 빠르게 식별되어 회피되며; 부분적으로 악의적인 Routers는 더 큰 도전 과제를 제기한다.

### 10.3 시빌 공격 (전체 키 공간)

공격자는 효과적인 서비스 거부(DoS) 공격의 일환으로 keyspace(키스페이스) 전반에 분산된 다수의 floodfill routers를 구축할 수 있다.

"bad"로 지정될 만큼 충분히 비정상적으로 동작하지 않는 경우에도 가능한 대응은 다음과 같다: - 콘솔 뉴스, 웹사이트, 포럼을 통해 공지된 bad router 해시/IP 목록을 취합 - 네트워크 전반의 floodfill 활성화("Sybil(시빌; 하나의 주체가 다수의 가짜 신원을 사용하는 공격)에는 더 많은 Sybil로 맞서기") - 하드코딩된 "bad" 목록을 포함한 새 소프트웨어 버전 - 자동 식별을 위한 피어 프로필 지표와 임계값 개선 - 단일 IP 블록 내 복수의 floodfill을 실격 처리하는 IP 블록 기준 - 자동 구독 기반 블랙리스트(Tor 컨센서스와 유사)

네트워크가 커질수록 이것은 더 어려워진다.

### 10.4 Sybil Attack(시빌 공격) (부분 키스페이스)

공격자는 keyspace(키스페이스; 키 공간)에서 서로 매우 가깝게 모여 있는 floodfill router를 8–15대 정도 만들 수 있습니다. 그 keyspace에 대한 모든 조회/저장 요청이 공격자 router로 향하게 되어, 특정 I2P 사이트에 대한 서비스 거부(DoS)가 가능해집니다.

키스페이스가 암호학적 SHA256 해시를 색인하므로, 공격자는 충분한 근접도를 가진 router를 생성하려면 무차별 대입(brute-force) 공격이 필요하다.

**방어**: Kademlia 근접성 알고리즘은 `SHA256(key + YYYYMMDD)`를 사용해 시간에 따라 변하며, UTC 자정에 매일 변경됩니다. 이러한 **keyspace rotation**(키스페이스 순환)은 공격을 매일 재생성하도록 강제합니다.

> **참고**: 최근 연구에 따르면 키스페이스 회전은 그다지 효과적이지 않습니다—공격자는 router 해시를 미리 계산할 수 있어, 회전 이후 30분 이내에 단지 몇 대의 router만으로 키스페이스의 일부를 eclipse(네트워크에서 대상 노드를 고립시키는 공격)할 수 있습니다.

일일 로테이션의 결과: 로테이션 후 수 분 동안 분산된 netdb의 신뢰성이 떨어지며—새로운 가장 가까운 router가 저장 항목을 받기 전에는 조회가 실패한다.

### 10.5 부트스트랩 공격

공격자는 reseed 웹사이트(신규 router의 초기 부트스트랩을 위해 네트워크 정보를 제공하는 웹사이트)를 장악하거나 개발자를 속여 악의적인 reseed 웹사이트를 추가하게 만들어, 새로운 router를 고립된/다수가 통제하는 네트워크로 부팅되도록 할 수 있습니다.

**구현된 방어책:** - 단일 사이트가 아닌 여러 reseed(네트워크 부트스트랩을 위한 초기 피어 정보 제공) 사이트에서 RouterInfo 하위집합을 가져옴 - 네트워크 외부에서 reseed 모니터링을 수행하여 사이트를 주기적으로 폴링함 - 0.9.14부터, reseed 데이터 번들은 서명된 zip 파일로 제공되며 다운로드된 서명으로 검증됨 (see [su3 사양](/docs/specs/updates))

### 10.6 쿼리 캡처

Floodfill routers가 반환된 참조를 통해 피어들을 공격자가 제어하는 routers로 "유도"할 수 있다.

낮은 빈도 때문에 탐색을 통해서는 가능성이 낮으며; routers는 주로 일반적인 tunnel 구축을 통해 피어 참조를 얻는다.

0.8.9부터 반복적 조회가 구현되었습니다. `DatabaseSearchReplyMessage`의 floodfill 참조는 조회 키에 더 가까운 경우 따라갑니다. 요청하는 routers는 참조의 근접성을 신뢰하지 않습니다. 악의적인 black-holing(트래픽을 흡수해 응답을 차단하는 공격)을 방지하기 위해, 더 가까운 키가 없더라도 타임아웃 또는 최대 질의 수에 도달할 때까지 조회를 계속합니다.

### 10.7 정보 유출

I2P에서의 DHT(분산 해시 테이블) 정보 유출은 추가 조사가 필요하다. floodfill routers는 질의를 관찰하여 정보를 수집할 수 있다. 악성 노드 비율이 20% 수준에 이르면, 앞서 설명한 Sybil(시빌) 공격 위협이 여러 가지 이유로 문제가 된다.

---

## 11. 향후 과제

- 추가 netDb 조회 및 응답에 대한 종단 간 암호화
- 향상된 조회 응답 추적 방법
- keyspace rotation(키 공간 회전) 신뢰성 문제에 대한 완화 방법

---

## 12. 참고 문헌

- [공통 구조체 명세](/docs/specs/common-structures/) – RouterInfo 및 LeaseSet(리스셋, I2P 목적지 도달을 위한 리스 집합) 구조체
- [I2NP 명세](/docs/specs/i2np/) – 데이터베이스 메시지 유형
- [제안 123: 새로운 netDb 항목](/proposals/123-new-netdb-entries) – LeaseSet2 명세
- [netDb 역사 논의](/docs/netdb/) – 개발 역사와 아카이브된 논의
