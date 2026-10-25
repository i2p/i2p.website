---
title: "네트워크 데이터베이스"
description: "I2P의 분산 네트워크 데이터베이스(netDb) 이해하기 - router 연락처 정보 및 목적지 조회를 위한 특수한 DHT"
slug: "network-database"
aliases:
  - "/ko/how_networkdatabase"
  - "/ko/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## 개요

I2P의 netDb는 특수한 분산 데이터베이스로, 단 두 가지 유형의 데이터만 포함합니다 - router 연락처 정보(**RouterInfos**)와 목적지 연락처 정보(**LeaseSets**). 각 데이터는 해당 당사자에 의해 서명되고 이를 사용하거나 저장하는 모든 사람에 의해 검증됩니다. 또한 데이터에는 생존성 정보가 포함되어 있어 관련 없는 항목을 제거하고, 새로운 항목이 오래된 항목을 대체하며, 특정 유형의 공격으로부터 보호할 수 있습니다.

netDb는 "floodfill"이라고 하는 간단한 기법으로 분산되며, 모든 router의 하위 집합인 "floodfill router"가 분산 데이터베이스를 유지합니다.

---

## RouterInfo

I2P router가 다른 router에 연결하려고 할 때, 몇 가지 핵심 데이터를 알아야 합니다. 이 모든 데이터는 router에 의해 번들로 묶이고 서명되어 "RouterInfo"라고 불리는 구조체가 되며, 이는 router의 신원에 대한 SHA256을 키로 하여 배포됩니다. 구조체 자체에는 다음이 포함됩니다:

- router의 신원 정보 (암호화 키, 서명 키, 그리고 인증서)
- 연결 가능한 연락처 주소들
- 게시된 시간
- 임의의 텍스트 옵션 집합
- 신원의 서명 키로 생성된 위 내용의 서명

### 예상 옵션

다음 텍스트 옵션들은 엄격히 필수는 아니지만, 존재할 것으로 예상됩니다:

- **caps** (능력 플래그 - floodfill 참여, 대략적인 대역폭, 인지된 도달 가능성을 나타내는 데 사용)
  - **D**: 중간 정도 혼잡 (릴리스 0.9.58부터)
  - **E**: 높은 혼잡 (릴리스 0.9.58부터)
  - **f**: Floodfill
  - **G**: 모든 tunnel 거부 (릴리스 0.9.58부터)
  - **H**: 숨김
  - **K**: 12 KBps 미만 공유 대역폭
  - **L**: 12 - 48 KBps 공유 대역폭 (기본값)
  - **M**: 48 - 64 KBps 공유 대역폭
  - **N**: 64 - 128 KBps 공유 대역폭
  - **O**: 128 - 256 KBps 공유 대역폭
  - **P**: 256 - 2000 KBps 공유 대역폭 (릴리스 0.9.20부터, 아래 참고사항 참조)
  - **R**: 도달 가능
  - **U**: 도달 불가능
  - **X**: 2000 KBps 초과 공유 대역폭 (릴리스 0.9.20부터, 아래 참고사항 참조)

"공유 대역폭" == (공유 %) * min(인바운드 대역폭, 아웃바운드 대역폭)

오래된 router와의 호환성을 위해, router는 여러 개의 대역폭 문자를 게시할 수 있습니다. 예를 들어 "PO"와 같이 말입니다.

참고: P와 X 대역폭 클래스 간의 경계는 구현자의 선택에 따라 2000 또는 2048 KBps일 수 있습니다.

- **netId** = 2 (기본 네트워크 호환성 - router는 다른 netId를 가진 피어와의 통신을 거부합니다)
- **router.version** (새로운 기능과 메시지들과의 호환성을 판단하는 데 사용됨)

R/U 기능에 대한 참고사항: router는 현재 도달 가능성 상태가 알려지지 않은 경우가 아니라면 일반적으로 R 또는 U 기능을 게시해야 합니다. R은 router가 최소한 하나의 전송 주소에서 직접 도달 가능함을 의미합니다(introducer가 필요하지 않고, 방화벽이 없음). U는 router가 어떤 전송 주소에서도 직접 도달할 수 없음을 의미합니다.

더 이상 사용되지 않는 옵션들: - ~~coreVersion~~ (사용된 적 없음, 릴리스 0.9.24에서 제거됨) - ~~stat_uptime~~ = 90m (버전 0.7.9부터 사용되지 않음, 릴리스 0.9.24에서 제거됨)

이 값들은 다른 router들이 기본적인 결정을 내리는 데 사용됩니다. 이 router에 연결해야 할까요? 이 router를 통해 tunnel을 라우팅해야 할까요? 특히 대역폭 기능 플래그는 router가 tunnel 라우팅을 위한 최소 임계값을 충족하는지 판단하는 데만 사용됩니다. 최소 임계값을 넘으면, 광고된 대역폭은 사용자 인터페이스 표시, 디버깅 및 네트워크 분석을 제외하고는 router 내 어디에서도 사용되거나 신뢰되지 않습니다.

유효한 NetID 번호:

| 용도 | NetID 번호 |
|-------|--------------|
| 예약됨 | 0 |
| 예약됨 | 1 |
| 현재 네트워크 (기본값) | 2 |
| 미래 네트워크 예약 | 3 - 15 |
| 포크 및 테스트 네트워크 | 16 - 254 |
| 예약됨 | 255 |
### 추가 옵션

추가 텍스트 옵션에는 router의 상태에 대한 소수의 통계가 포함되며, 이는 [stats.i2p](http://stats.i2p/)와 같은 사이트에서 네트워크 성능 분석 및 디버깅을 위해 집계됩니다. 이러한 통계는 tunnel 구축 성공률과 같이 개발자에게 중요한 데이터를 제공하도록 선택되었으며, 동시에 이러한 데이터 공개로 인한 부작용과 균형을 맞춥니다. 현재 통계는 다음으로 제한됩니다:

- 탐색 tunnel 구축 성공, 거부 및 타임아웃 비율
- 1시간 평균 참여 tunnel 수

이는 선택사항이지만, 포함된다면 네트워크 전체 성능 분석에 도움이 됩니다. API 0.9.58부터 이러한 통계는 다음과 같이 단순화되고 표준화되었습니다:

- 옵션 키는 stat_(statname).(statperiod) 형식입니다
- 옵션 값은 ';'로 구분됩니다
- 이벤트 카운트나 정규화된 백분율 통계는 4번째 값을 사용합니다; 처음 세 값은 사용되지 않지만 반드시 있어야 합니다
- 평균값 통계는 1번째 값을 사용하며, ';' 구분자는 필요하지 않습니다
- 통계 분석에서 모든 router의 동등한 가중치를 위해, 그리고 추가적인 익명성을 위해, router는 1시간 이상 가동된 후에만 이러한 통계를 포함해야 하며, RI가 게시될 때마다 16번에 한 번씩만 포함해야 합니다.

예제:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router들은 자신의 네트워크 데이터베이스에 있는 항목 수에 대한 추가 데이터를 게시할 수 있습니다. 이는 선택사항이지만, 포함된다면 네트워크 전체 성능 분석에 도움이 됩니다.

다음 두 옵션은 floodfill router가 게시하는 모든 RI에 포함되어야 합니다:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

예제:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
게시된 데이터는 router의 사용자 인터페이스에서 볼 수 있지만, 다른 router에서는 사용하거나 신뢰하지 않습니다.

### 패밀리 옵션

릴리스 0.9.24부터 router들은 동일한 엔티티에 의해 운영되는 "패밀리"의 일부라고 선언할 수 있습니다. 동일한 패밀리에 속한 여러 router들은 하나의 tunnel에서 사용되지 않습니다.

family 옵션들은 다음과 같습니다:

- **family** (패밀리 이름)
- **family.key** 패밀리의 [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey)의 서명 타입 코드 (ASCII 숫자)와 ':'가 연결되고, 그 뒤에 base 64로 인코딩된 Signing Public Key가 연결된 값
- **family.sig** ((UTF-8로 인코딩된 패밀리 이름)과 (32바이트 router 해시)가 연결된 값)의 서명을 base 64로 인코딩한 값

### RouterInfo 만료

RouterInfo는 정해진 만료 시간이 없습니다. 각 router는 RouterInfo 조회 빈도와 메모리 또는 디스크 사용량 사이의 균형을 맞추기 위해 자체 로컬 정책을 유지할 수 있습니다. 현재 구현에서는 다음과 같은 일반적인 정책들이 있습니다:

- 지속적으로 저장된 데이터가 오래된 것일 수 있으므로 가동 시간 첫 시간 동안에는 만료가 없습니다.
- RouterInfo가 25개 이하인 경우 만료가 없습니다.
- 로컬 RouterInfo 수가 증가함에 따라 적절한 RouterInfo 수를 유지하려는 시도로 만료 시간이 단축됩니다. 120개 미만의 router가 있을 때 만료 시간은 72시간이고, 300개의 router가 있을 때 만료 시간은 약 30시간입니다.
- [SSU](/docs/legacy/ssu/) introducer를 포함한 RouterInfo는 introducer 목록이 약 그 시간 내에 만료되므로 약 1시간 후에 만료됩니다.
- Floodfill은 유효한 RouterInfo가 자주 재게시되기 때문에 모든 로컬 RouterInfo에 대해 짧은 만료 시간(1시간)을 사용합니다.

### RouterInfo 영구 저장소

RouterInfo들은 재시작 후에도 사용할 수 있도록 주기적으로 디스크에 기록됩니다.

만료 시간이 긴 Meta LeaseSet을 지속적으로 저장하는 것이 바람직할 수 있습니다. 이는 구현에 따라 달라집니다.

### 참고 항목

- [RouterInfo 사양](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

netDb에서 배포되는 두 번째 데이터는 "LeaseSet"으로, 특정 클라이언트 목적지를 위한 **터널 진입점(lease) 그룹**을 문서화합니다. 이러한 각 lease는 다음 정보를 명시합니다:

- tunnel gateway router (해당 router의 identity를 지정하여)
- 메시지를 전송할 해당 router의 tunnel ID (4바이트 숫자)
- 해당 tunnel이 만료되는 시점

leaseSet 자체는 destination의 SHA256에서 파생된 키 아래 netDb에 저장됩니다. 한 가지 예외는 릴리스 0.9.38부터의 Encrypted LeaseSet(LS2)입니다. 타입 바이트(3) 다음에 blinded public key가 오는 SHA256이 DHT 키로 사용되며, 그 다음 평소와 같이 회전됩니다. 아래 Kademlia Closeness Metric 섹션을 참조하세요.

이러한 lease들 외에도, LeaseSet에는 다음이 포함됩니다:

- destination 자체 (암호화 키, 서명 키, 그리고 인증서)
- 추가 암호화 공개 키: garlic 메시지의 종단 간 암호화에 사용됨
- 추가 서명 공개 키: LeaseSet 폐기를 위해 의도되었지만, 현재는 사용되지 않음.
- 모든 LeaseSet 데이터의 서명, destination이 LeaseSet을 게시했음을 확인하기 위함.

- [Lease 사양](/docs/specs/common-structures/#struct_Lease)
- [LeaseSet 사양](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

릴리스 0.9.38부터 세 가지 새로운 유형의 leaseSet이 정의되었습니다: LeaseSet2, MetaLeaseSet, EncryptedLeaseSet. 아래를 참조하세요.

### 게시되지 않은 LeaseSet

나가는 연결에만 사용되는 목적지의 LeaseSet은 *미공개*됩니다. floodfill router에 게시를 위해 전송되지 않습니다. 웹 브라우징 및 IRC 클라이언트와 같은 "클라이언트" tunnel은 미공개됩니다. [I2NP 저장 메시지](#leaseset-storage-to-peers) 때문에 서버는 여전히 이러한 미공개 목적지로 메시지를 다시 보낼 수 있습니다.

### 취소된 LeaseSet들

LeaseSet은 lease가 0개인 새로운 LeaseSet을 게시하여 *폐기*될 수 있습니다. 폐기는 LeaseSet의 추가 서명 키로 서명되어야 합니다. 폐기는 완전히 구현되지 않았으며, 실용적인 용도가 있는지 불분명합니다. 이는 해당 서명 키의 유일한 계획된 용도이므로 현재는 사용되지 않습니다.

### LeaseSet2 (LS2)

릴리스 0.9.38부터 floodfill은 새로운 LeaseSet2 구조를 지원합니다. 이 구조는 기존 LeaseSet 구조와 매우 유사하며 동일한 목적을 수행합니다. 새로운 구조는 새로운 암호화 유형, 다중 암호화 유형, 옵션, 오프라인 서명 키 및 기타 기능을 지원하는 데 필요한 유연성을 제공합니다. 자세한 내용은 제안서 123을 참조하십시오.

### Meta LeaseSet (LS2)

릴리스 0.9.38부터 floodfill은 새로운 Meta LeaseSet 구조를 지원합니다. 이 구조는 DHT에서 다른 LeaseSet들을 참조하기 위한 트리 형태의 구조를 제공합니다. Meta LeaseSet을 사용하여 사이트는 공통 서비스를 제공하기 위해 여러 다른 Destination들이 사용되는 대규모 멀티홈 서비스를 구현할 수 있습니다. Meta LeaseSet의 항목들은 Destination 또는 다른 Meta LeaseSet들이며, 최대 18.2시간까지 긴 만료 시간을 가질 수 있습니다. 이 기능을 사용하면 공통 서비스를 호스팅하는 수백 또는 수천 개의 Destination을 실행하는 것이 가능해야 합니다. 자세한 내용은 proposal 123을 참조하세요.

### 암호화된 LeaseSet (LS1)

이 섹션에서는 고정된 대칭 키를 사용하여 leaseSet을 암호화하는 기존의 안전하지 않은 방법에 대해 설명합니다. 암호화된 leaseSet의 LS2 버전에 대해서는 아래를 참조하세요.

*암호화된* LeaseSet에서는 모든 Lease가 별도의 키로 암호화됩니다. lease는 키를 가진 사람만이 디코딩할 수 있으며, 따라서 해당 목적지는 키를 가진 사람만이 연락할 수 있습니다. LeaseSet이 암호화되었다는 직접적인 플래그나 다른 표시는 없습니다. 암호화된 LeaseSet은 널리 사용되지 않으며, 암호화된 LeaseSet의 사용자 인터페이스와 구현을 개선할 수 있는지에 대한 연구는 향후 과제입니다.

### 암호화된 LeaseSets (LS2)

릴리스 0.9.38부터 floodfill은 새로운 EncryptedLeaseSet 구조를 지원합니다. Destination이 숨겨지고, floodfill에는 블라인드된 공개 키와 만료 시간만 보입니다. 전체 Destination을 가진 사람만이 구조를 복호화할 수 있습니다. 구조는 Destination의 해시가 아닌 블라인드된 공개 키의 해시를 기반으로 한 DHT 위치에 저장됩니다. 자세한 내용은 제안서 123을 참조하세요.

### LeaseSet 만료

일반적인 LeaseSet의 경우, 만료 시간은 해당 lease들 중 가장 늦은 만료 시간입니다. 새로운 LeaseSet2 데이터 구조의 경우, 만료 시간은 헤더에 명시됩니다. LeaseSet2의 경우, 만료 시간은 해당 lease들의 가장 늦은 만료 시간과 일치해야 합니다. EncryptedLeaseSet과 MetaLeaseSet의 경우, 만료 시간은 다를 수 있으며, 최대 만료 시간이 적용될 수 있습니다(결정 예정).

### LeaseSet 영구 저장소

LeaseSet 데이터는 매우 빠르게 만료되므로 영구 저장이 필요하지 않습니다. 그러나 만료 시간이 긴 EncryptedLeaseSet 및 MetaLeaseSet 데이터의 영구 저장은 권장될 수 있습니다.

### 암호화 키 선택 (LS2)

LeaseSet2는 여러 암호화 키를 포함할 수 있습니다. 키들은 서버 선호도 순서대로 정렬되며, 가장 선호하는 것이 첫 번째입니다. 기본 클라이언트 동작은 지원되는 암호화 타입을 가진 첫 번째 키를 선택하는 것입니다. 클라이언트는 암호화 지원, 상대적 성능, 기타 요인들을 기반으로 다른 선택 알고리즘을 사용할 수 있습니다.

---

## 부트스트래핑

netDb는 분산화되어 있지만, 통합 프로세스가 당신을 연결시키기 위해서는 최소한 하나의 peer에 대한 참조가 필요합니다. 이는 활성 peer의 RouterInfo로 router를 "재시딩"하여 달성됩니다 - 구체적으로는 해당 peer의 `routerInfo-$hash.dat` 파일을 검색하여 `netDb/` 디렉토리에 저장하는 방식입니다. 누구든지 이러한 파일을 제공할 수 있으며 - 자신의 netDb 디렉토리를 공개함으로써 다른 사람들에게 제공할 수도 있습니다. 프로세스를 단순화하기 위해 자원봉사자들이 일반(non-i2p) 네트워크에서 자신의 netDb 디렉토리(또는 일부)를 공개하고, 이러한 디렉토리의 URL들이 I2P에 하드코딩되어 있습니다. router가 처음 시작될 때, 무작위로 선택된 이러한 URL 중 하나에서 자동으로 데이터를 가져옵니다.

---

## Floodfill

floodfill netDb는 간단한 분산 저장 메커니즘입니다. 저장 알고리즘은 단순합니다: floodfill router로 자신을 광고한 가장 가까운 피어에게 데이터를 전송합니다. floodfill netDb의 피어가 floodfill netDb에 속하지 않은 피어로부터 netDb store를 받으면, 해당 피어는 이를 floodfill netDb 피어들의 하위 집합에게 전송합니다. 선택되는 피어들은 특정 키에 대해 ([XOR-metric](#kademlia-closeness-metric)에 따라) 가장 가까운 피어들입니다.

누가 floodfill netDb의 일부인지 확인하는 것은 간단합니다 - 이는 각 router의 게시된 routerInfo에서 capability로 노출됩니다.

Floodfill은 중앙 권한이 없으며 "합의"를 형성하지 않습니다 - 단순한 DHT 오버레이만을 구현합니다.

### Floodfill Router 참여 선택

디렉토리 서버가 하드코딩되어 신뢰받고 알려진 주체에 의해 운영되는 Tor와 달리, I2P floodfill 피어 집합의 구성원들은 신뢰받을 필요가 없으며 시간이 지나면서 변경됩니다.

netDb의 신뢰성을 높이고 router에 대한 netDb 트래픽의 영향을 최소화하기 위해, floodfill은 높은 대역폭 제한으로 구성된 router에서만 자동으로 활성화됩니다. 높은 대역폭 제한을 가진 router들은 (기본값이 훨씬 낮기 때문에 수동으로 구성되어야 함) 지연시간이 낮은 연결에 있다고 가정되며, 24시간 내내 사용 가능할 가능성이 높습니다. floodfill router의 현재 최소 공유 대역폭은 128 KBytes/sec입니다.

또한, router가 floodfill 작동이 자동으로 활성화되기 전에 상태에 대한 여러 추가 테스트(아웃바운드 메시지 큐 시간, 작업 지연 등)를 통과해야 합니다.

현재 자동 옵트인 규칙에 따르면, 네트워크 내 router의 약 6%가 floodfill router입니다.

일부 피어는 floodfill로 수동 구성되지만, 다른 피어들은 단순히 고대역폭 router들로서 floodfill 피어의 수가 임계값 아래로 떨어질 때 자동으로 자원봉사에 나섭니다. 이는 공격으로 인해 대부분 또는 모든 floodfill을 잃어도 네트워크에 장기적인 손상이 발생하지 않도록 방지합니다. 반대로, 이러한 피어들은 너무 많은 floodfill이 존재할 때 스스로 floodfill 역할을 중단합니다.

### Floodfill Router 역할

floodfill router가 non-floodfill router에 추가로 제공하는 유일한 서비스는 netDb 저장 요청을 수락하고 netDb 쿼리에 응답하는 것입니다. 일반적으로 고대역폭을 가지고 있기 때문에, 더 많은 수의 tunnel에 참여할 가능성이 높지만(즉, 다른 사용자들을 위한 "릴레이" 역할), 이는 분산 데이터베이스 서비스와 직접적인 관련은 없습니다.

---

## Kademlia 근접성 메트릭

netDb는 근접성을 결정하기 위해 간단한 Kademlia 스타일의 XOR 메트릭을 사용합니다. Kademlia 키를 생성하기 위해 RouterIdentity 또는 Destination의 SHA256 해시가 계산됩니다. 한 가지 예외는 릴리스 0.9.38부터의 Encrypted LeaseSet(LS2)입니다. 타입 바이트(3) 다음에 블라인드된 공개 키가 이어지는 SHA256이 DHT 키로 사용되고, 그 후 평소처럼 회전됩니다.

이 알고리즘은 [시빌 공격](#sybil-attack-partial-keyspace)의 비용을 증가시키기 위해 수정되었습니다. 조회하거나 저장되는 키의 SHA256 해시 대신, 32바이트 이진 검색 키에 UTC 날짜를 8바이트 ASCII 문자열 yyyyMMdd로 표현하여 추가한 값의 SHA256 해시를 사용합니다. 즉, SHA256(key + yyyyMMdd)입니다. 이를 "라우팅 키"라고 하며, 매일 자정 UTC에 변경됩니다. 이런 방식으로 수정되는 것은 검색 키뿐이며, floodfill router 해시는 해당되지 않습니다. DHT의 일일 변환은 때때로 "키스페이스 로테이션"이라고 불리지만, 엄밀히 말해서는 로테이션이 아닙니다.

라우팅 키는 어떤 I2NP 메시지에서도 네트워크를 통해 전송되지 않으며, 거리 계산을 위해 로컬에서만 사용됩니다.

---

## 네트워크 데이터베이스 분할 - 하위 데이터베이스

전통적으로 Kademlia 스타일 DHT는 DHT의 특정 노드에 저장된 정보의 연결 불가능성을 보존하는 것에 관심이 없습니다. 예를 들어, 정보 조각이 DHT의 한 노드에 저장된 다음, 그 노드에서 무조건적으로 다시 요청될 수 있습니다. I2P 내에서 netDb를 사용할 때는 그렇지 않습니다. DHT에 저장된 정보는 그렇게 하는 것이 "안전한" 특정 알려진 상황에서만 공유될 수 있습니다. 이는 악의적인 행위자가 클라이언트 tunnel에 저장을 보낸 다음, 의심되는 클라이언트 tunnel의 "호스트"에서 직접 다시 요청하여 클라이언트 tunnel을 router와 연관시키려고 시도하는 공격 유형을 방지하기 위함입니다.

### 세그멘테이션 구조

I2P router는 몇 가지 조건이 충족되면 이러한 공격 유형에 대한 효과적인 방어를 구현할 수 있습니다. netDb 구현은 데이터베이스 항목이 클라이언트 tunnel을 통해 수신되었는지 아니면 직접 수신되었는지 추적할 수 있어야 합니다. 클라이언트 tunnel을 통해 수신된 경우, 클라이언트의 로컬 목적지를 사용하여 어떤 클라이언트 tunnel을 통해 수신되었는지도 추적해야 합니다. 항목이 여러 클라이언트 tunnel을 통해 수신된 경우, netDb는 해당 항목이 관찰된 모든 목적지를 추적해야 합니다. 또한 항목이 조회에 대한 응답으로 수신되었는지, 아니면 저장으로 수신되었는지도 추적해야 합니다.

Java와 C++ 구현 모두에서, 이는 직접적인 조회와 floodfill 작업을 위해 먼저 단일 "Main" netDb를 사용하여 달성됩니다. 이 메인 netDb는 router 컨텍스트에 존재합니다. 그런 다음, 각 클라이언트는 자체 버전의 netDb를 제공받으며, 이는 클라이언트 tunnel로 전송된 데이터베이스 항목을 캡처하고 클라이언트 tunnel로 전송된 조회에 응답하는 데 사용됩니다. 우리는 이를 "Client Network Databases" 또는 "Sub-Databases"라고 부르며, 이들은 클라이언트 컨텍스트에 존재합니다. 클라이언트가 운영하는 netDb는 클라이언트의 수명 동안만 존재하며 클라이언트의 tunnel과 통신되는 항목만을 포함합니다. 이는 클라이언트 tunnel로 전송된 항목이 router로 직접 전송된 항목과 겹치는 것을 불가능하게 만듭니다.

또한, 각 netDb는 데이터베이스 항목이 우리의 목적지 중 하나로 전송되어 수신된 것인지, 아니면 조회의 일부로 우리가 요청하여 수신된 것인지를 기억할 수 있어야 합니다. 데이터베이스 항목이 저장으로 수신된 경우, 즉 다른 router가 우리에게 보낸 경우, netDb는 다른 router가 키를 조회할 때 해당 항목에 대한 요청에 응답해야 합니다. 그러나 쿼리에 대한 응답으로 수신된 경우, netDb는 해당 항목이 이미 같은 목적지에 저장된 경우에만 항목에 대한 쿼리에 응답해야 합니다. 클라이언트는 메인 netDb의 항목으로 쿼리에 응답해서는 안 되며, 오직 자신의 클라이언트 네트워크 데이터베이스로만 응답해야 합니다.

이러한 전략들은 두 가지 모두 적용되도록 결합하여 사용되어야 합니다. 결합하면 netDb를 "세그먼트화"하고 공격으로부터 보호합니다.

---

## 저장, 검증, 및 조회 메커니즘

### 피어에 대한 RouterInfo 저장

로컬 RouterInfo를 포함하는 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage는 [NTCP](/docs/specs/ntcp2/) 또는 [SSU](/docs/specs/ssu2/) 전송 연결 초기화의 일부로 피어와 교환됩니다.

### 피어에 LeaseSet 저장

로컬 leaseSet을 포함하는 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage들은 관련 Destination의 일반 트래픽과 함께 garlic 메시지로 묶어서 피어들과 주기적으로 교환됩니다. 이를 통해 초기 응답과 후속 응답들을 적절한 Lease로 보낼 수 있으며, leaseSet 조회가 필요하지 않고 통신하는 Destination들이 leaseSet을 전혀 게시할 필요도 없습니다.

### Floodfill 선택

DatabaseStoreMessage는 저장되는 RouterInfo 또는 LeaseSet의 현재 라우팅 키에 가장 가까운 floodfill로 전송되어야 합니다. 현재 가장 가까운 floodfill은 로컬 데이터베이스 검색을 통해 찾습니다. 해당 floodfill이 실제로 가장 가깝지 않더라도, 다른 여러 floodfill들에게 전송하여 "더 가깝게" 플러딩할 것입니다. 이는 높은 수준의 내결함성을 제공합니다.

전통적인 Kademlia에서는 피어가 DHT에 아이템을 가장 가까운 대상에 삽입하기 전에 "find-closest" 검색을 수행합니다. verify 작업이 존재할 경우 더 가까운 floodfill들을 발견하는 경향이 있기 때문에, router는 정기적으로 게시하는 RouterInfo와 LeaseSet들에 대한 DHT "근처" 지식을 빠르게 향상시킬 것입니다. I2NP는 "find-closest" 메시지를 정의하지 않지만, 필요하다면 router는 DatabaseSearchReplyMessage에서 더 가까운 피어가 수신되지 않을 때까지 최하위 비트가 뒤바뀐 키(즉, key ^ 0x01)에 대해 반복적 검색을 수행할 수 있습니다. 이는 더 먼 피어가 netDb 아이템을 가지고 있더라도 진정한 가장 가까운 피어를 찾을 수 있도록 보장합니다.

### RouterInfo Storage to Floodfills

router는 floodfill router에 직접 연결하고 0이 아닌 Reply Token이 포함된 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage를 전송하여 자신의 RouterInfo를 게시합니다. 이 메시지는 직접 연결이므로 end-to-end garlic encryption되지 않습니다. 중간 router가 없고 (어차피 이 데이터를 숨길 필요도 없기 때문입니다). floodfill router는 Message ID가 Reply Token 값으로 설정된 [I2NP](/docs/specs/i2np/) DeliveryStatusMessage로 응답합니다.

일부 상황에서는 router가 탐색용 tunnel을 통해 RouterInfo DatabaseStoreMessage를 전송할 수도 있습니다. 예를 들어, 연결 제한, 연결 비호환성 또는 floodfill로부터 실제 IP를 숨기려는 목적 때문입니다. floodfill은 과부하 시점이나 다른 기준에 따라 그러한 저장을 받아들이지 않을 수 있습니다. RouterInfo의 비직접 저장을 명시적으로 불법으로 선언할지 여부는 추가 연구가 필요한 주제입니다.

### LeaseSet을 Floodfill에 저장

LeaseSet의 저장은 RouterInfo보다 훨씬 더 민감한데, router는 LeaseSet이 해당 router와 연관될 수 없도록 주의해야 하기 때문입니다.

router는 해당 Destination에 대한 아웃바운드 클라이언트 터널을 통해 0이 아닌 Reply Token을 포함한 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage를 전송하여 로컬 LeaseSet을 게시합니다. 이 메시지는 터널의 아웃바운드 엔드포인트로부터 메시지를 숨기기 위해 Destination의 Session Key Manager를 사용하여 종단간 garlic encryption됩니다. floodfill router는 Message ID를 Reply Token 값으로 설정한 [I2NP](/docs/specs/i2np/) DeliveryStatusMessage로 응답합니다. 이 메시지는 클라이언트의 인바운드 터널 중 하나로 다시 전송됩니다.

### 플러딩

모든 router와 마찬가지로, floodfill은 LeaseSet이나 RouterInfo를 로컬에 저장하기 전에 다양한 기준을 사용하여 검증합니다. 이러한 기준은 현재 부하, netDb 크기 및 기타 요인을 포함한 현재 상황에 따라 적응적이고 의존적일 수 있습니다. 모든 검증은 플러딩 전에 수행되어야 합니다.

floodfill router가 로컬 NetDb에 이전에 저장된 것보다 새로운 유효한 RouterInfo 또는 LeaseSet을 포함하는 DatabaseStoreMessage를 받은 후, 이를 "floods" 합니다. NetDb 항목을 flood하기 위해, NetDb 항목의 라우팅 키에 가장 가까운 여러 개의 (현재 3개) floodfill router들을 찾습니다. (라우팅 키는 RouterIdentity 또는 Destination의 SHA256 해시에 날짜(yyyyMMdd)가 추가된 것입니다.) 자신과 가장 가까운 곳이 아닌 키에 가장 가까운 곳으로 flooding함으로써, floodfill은 저장하는 router가 라우팅 키에 대한 DHT "neighborhood"에 대한 좋은 지식을 갖지 못했더라도 저장소가 올바른 위치에 도달하도록 보장합니다.

그러면 floodfill은 해당 피어들 각각에 직접 연결하여 Reply Token이 0인 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage를 전송합니다. 이는 직접 연결이므로 중간 라우터가 없어 메시지는 종단간 garlic 암호화되지 않습니다(어차피 이 데이터를 숨길 필요도 없습니다). Reply Token이 0이므로 다른 라우터들은 응답하거나 재전파하지 않습니다.

Floodfill은 tunnel을 통해 flood해서는 안 됩니다. DatabaseStoreMessage는 직접 연결을 통해 전송되어야 합니다.

Floodfill은 만료된 LeaseSet이나 한 시간 이상 전에 게시된 RouterInfo를 절대 flood해서는 안 됩니다.

### RouterInfo 및 LeaseSet 조회

[I2NP](/docs/specs/i2np/) DatabaseLookupMessage는 floodfill router로부터 netDb 항목을 요청하는 데 사용됩니다. 조회는 router의 아웃바운드 탐색 tunnel 중 하나를 통해 전송됩니다. 응답은 router의 인바운드 탐색 tunnel 중 하나를 통해 반환되도록 지정됩니다.

조회는 일반적으로 요청된 키에 가장 가까운 두 개의 "양호한"(연결이 실패하지 않는) floodfill router에 병렬로 전송됩니다.

floodfill router가 로컬에서 키를 찾으면 [I2NP](/docs/specs/i2np/) DatabaseStoreMessage로 응답합니다. floodfill router가 로컬에서 키를 찾지 못하면 해당 키에 가까운 다른 floodfill router들의 목록을 포함한 [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage로 응답합니다.

LeaseSet 조회는 릴리스 0.9.5부터 garlic encryption으로 종단간 암호화됩니다. RouterInfo 조회는 암호화되지 않으므로 클라이언트 tunnel의 outbound endpoint(OBEP)에 의한 도청에 취약합니다. 이는 ElGamal 암호화의 비용 때문입니다. RouterInfo 조회 암호화는 향후 릴리스에서 활성화될 수 있습니다.

릴리스 0.9.7부터 leaseSet 조회에 대한 응답(DatabaseStoreMessage 또는 DatabaseSearchReplyMessage)은 조회에 세션 키와 태그를 포함하여 암호화됩니다. 이는 응답 tunnel의 인바운드 게이트웨이(IBGW)로부터 응답을 숨깁니다. RouterInfo 조회에 대한 응답은 조회 암호화를 활성화하면 암호화됩니다.

(참조: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 아래 이탤릭체 용어들에 대한 섹션 2.2-2.3)

네트워크의 상대적으로 작은 규모와 flooding 중복성으로 인해, 조회는 보통 O(log n)이 아닌 O(1)입니다. router는 첫 번째 시도에서 답을 얻을 수 있을 만큼 키에 가까운 floodfill router를 알고 있을 가능성이 높습니다. 0.8.9 이전 릴리스에서는 router들이 2개의 조회 중복성을 사용했으며(즉, 서로 다른 피어에 대해 병렬로 2개의 조회가 수행됨), 조회를 위한 *재귀적*이나 *반복적* 라우팅은 구현되지 않았습니다. *쿼리 실패 가능성을 줄이기 위해* 쿼리는 *여러 경로를 통해 동시에* 전송되었습니다.

릴리스 0.8.9부터 조회 중복성 없는 *반복적 조회*가 구현되었습니다. 이는 모든 floodfill 피어가 알려지지 않은 상황에서도 훨씬 더 잘 작동하는 더 효율적이고 안정적인 조회 방식으로, 네트워크 성장에 대한 심각한 제한을 제거합니다. 네트워크가 성장하고 각 router가 floodfill 피어의 작은 부분집합만 알게 되면서 조회는 O(log n)이 됩니다. 피어가 키에 더 가까운 참조를 반환하지 않더라도, 견고성을 높이고 악의적인 floodfill이 키 공간의 일부를 블랙홀로 만드는 것을 방지하기 위해 조회는 다음으로 가장 가까운 피어와 계속됩니다. 조회는 전체 조회 시간 초과에 도달하거나 최대 피어 수가 쿼리될 때까지 계속됩니다.

*노드 ID*는 router 해시를 노드 ID와 Kademlia 키로 직접 사용하기 때문에 *검증 가능*합니다. 검색 키에 더 가깝지 않은 잘못된 응답은 일반적으로 무시됩니다. 현재 네트워크 크기를 고려할 때, router는 *목적지 ID 공간의 인근 영역에 대한 상세한 지식*을 가지고 있습니다.

### RouterInfo 저장소 검증

참고: RouterInfo 검증은 논문 [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf)에서 설명된 공격을 방지하기 위해 릴리스 0.9.7.1부터 비활성화되었습니다. 검증을 안전하게 수행할 수 있도록 재설계할 수 있는지는 명확하지 않습니다.

저장이 성공했는지 확인하기 위해 router는 단순히 약 10초간 기다린 후, 키에 가까운 다른 floodfill router(저장이 전송된 router가 아닌)에게 조회를 보냅니다. 조회는 router의 아웃바운드 탐색 tunnel 중 하나를 통해 전송됩니다. 조회는 아웃바운드 엔드포인트(OBEP)의 도청을 방지하기 위해 종단 간 garlic encryption으로 암호화됩니다.

### LeaseSet 저장소 검증

저장이 성공했는지 확인하기 위해, router는 단순히 약 10초 정도 기다린 다음, 키에 가까운 다른 floodfill router(저장이 전송된 router가 아닌)에게 조회를 보냅니다. 조회는 확인되고 있는 LeaseSet의 목적지를 위한 아웃바운드 클라이언트 tunnel 중 하나를 통해 전송됩니다. 아웃바운드 tunnel의 OBEP에 의한 스누핑을 방지하기 위해, 조회는 종단 간 garlic encryption됩니다. 응답은 클라이언트의 인바운드 tunnel 중 하나를 통해 반환되도록 지정됩니다.

릴리스 0.9.7부터, RouterInfo와 LeaseSet 조회에 대한 응답(DatabaseStoreMessage 또는 DatabaseSearchReplyMessage)은 응답 터널의 인바운드 게이트웨이(IBGW)로부터 응답을 숨기기 위해 암호화됩니다.

### 탐색

*Exploration*은 특별한 형태의 netDb 조회로, router가 새로운 router들에 대해 학습하려고 시도하는 것입니다. 이는 floodfill router에게 임의의 키를 찾는 [I2NP](/docs/specs/i2np/) DatabaseLookup Message를 전송함으로써 수행됩니다. 이 조회는 실패할 것이므로, floodfill은 일반적으로 해당 키에 가까운 floodfill router들의 해시를 포함하는 [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage로 응답할 것입니다. 요청하는 router가 이미 그러한 floodfill들을 알고 있을 가능성이 높고, 모든 floodfill router들을 DatabaseLookup Message의 "포함하지 않음" 필드에 추가하는 것은 비실용적이기 때문에, 이는 도움이 되지 않을 것입니다. exploration 쿼리의 경우, 요청하는 router는 DatabaseLookup Message에 특별한 플래그를 설정합니다. 그러면 floodfill은 요청된 키에 가까운 non-floodfill router들로만 응답할 것입니다.

### 조회 응답에 대한 참고사항

조회 요청에 대한 응답은 Database Store Message (성공 시) 또는 Database Search Reply Message (실패 시) 중 하나입니다. DSRM에는 응답의 출처를 나타내는 'from' router 해시 필드가 포함되어 있지만 DSM에는 없습니다. DSRM의 'from' 필드는 인증되지 않으므로 위조되거나 유효하지 않을 수 있습니다. 다른 응답 태그는 없습니다. 따라서 여러 요청을 병렬로 수행할 때 다양한 floodfill router들의 성능을 모니터링하기 어렵습니다.

---

## 멀티호밍

Destination은 동일한 개인 키와 공개 키(전통적으로 eepPriv.dat 파일에 저장됨)를 사용하여 여러 router에서 동시에 호스팅될 수 있습니다. 두 인스턴스 모두 주기적으로 서명된 LeaseSet을 floodfill 피어에 게시하므로, 데이터베이스 조회를 요청하는 피어에게는 가장 최근에 게시된 LeaseSet이 반환됩니다. LeaseSet은 (최대) 10분의 수명을 가지므로, 특정 인스턴스가 다운되더라도 중단 시간은 최대 10분이며, 일반적으로는 그보다 훨씬 짧습니다. 멀티호밍 기능은 검증되었으며 네트워크의 여러 서비스에서 사용되고 있습니다.

0.9.38 릴리스부터 floodfill들은 새로운 Meta LeaseSet 구조를 지원합니다. 이 구조는 DHT에서 다른 LeaseSet들을 참조하기 위한 트리 형태의 구조를 제공합니다. Meta LeaseSet을 사용하여 사이트는 공통 서비스를 제공하기 위해 여러 다른 Destination들이 사용되는 대규모 멀티홈 서비스를 구현할 수 있습니다. Meta LeaseSet의 항목들은 Destination이나 다른 Meta LeaseSet들이며, 최대 18.2시간까지의 긴 만료 시간을 가질 수 있습니다. 이 기능을 사용하면 공통 서비스를 호스팅하는 수백 또는 수천 개의 Destination들을 실행하는 것이 가능해야 합니다. 자세한 내용은 proposal 123을 참조하세요.

---

## 위협 분석

[위협 모델 페이지](/docs/overview/threat-model/#floodfill)에서도 논의되었습니다.

악의적인 사용자가 하나 이상의 floodfill router를 생성하고 이를 조작하여 잘못되거나 느리거나 응답하지 않도록 만들어 네트워크에 해를 끼치려 할 수 있습니다. 아래에서 몇 가지 시나리오를 논의합니다.

### 성장을 통한 일반적 완화

현재 네트워크에는 약 1700개의 floodfill router가 있습니다. 다음 공격들 대부분은 네트워크 크기와 floodfill router 수가 증가함에 따라 더 어려워지거나 영향이 줄어들 것입니다.

### 중복성을 통한 일반적 완화

flooding을 통해 모든 netdb 항목들은 키에 가장 가까운 3개의 floodfill router에 저장됩니다.

### 위조

모든 netDb 항목은 생성자에 의해 서명되므로, 어떤 router도 RouterInfo나 LeaseSet을 위조할 수 없습니다.

### 느리거나 응답하지 않음

각 router는 각 floodfill router에 대한 [피어 프로필](/docs/overview/peer-selection/)에서 확장된 통계 세트를 유지하며, 해당 피어의 다양한 품질 메트릭을 다룹니다. 이 세트에는 다음이 포함됩니다:

- 평균 응답 시간
- 요청된 데이터로 응답한 쿼리 비율
- 성공적으로 검증된 저장소 비율
- 마지막 성공한 저장소
- 마지막 성공한 조회
- 마지막 응답

router가 어떤 floodfill router가 키에 가장 가까운지 결정해야 할 때마다, 이러한 메트릭을 사용하여 어떤 floodfill router가 "좋은지" 판단합니다. "좋음"을 결정하는 데 사용되는 방법과 임계값은 상대적으로 새로운 것이며, 추가 분석과 개선의 대상입니다. 완전히 응답하지 않는 router는 빠르게 식별되어 회피되지만, 때때로만 악의적인 router는 다루기 훨씬 어려울 수 있습니다.

### 시빌 공격 (전체 키 공간)

공격자는 키스페이스 전체에 걸쳐 대량의 floodfill router를 생성하여 [시빌 공격](https://www.freehaven.net/anonbib/cache/sybil.pdf)을 수행할 수 있습니다.

(관련 사례로, 한 연구자가 최근 [대량의 Tor relay들](http://blog.torproject.org/blog/june-2010-progress-report)을 생성했습니다.) 성공한다면, 이는 전체 네트워크에 대한 효과적인 DOS 공격이 될 수 있습니다.

floodfill들이 위에서 설명한 피어 프로필 메트릭을 사용하여 "나쁨"으로 표시될 정도로 충분히 잘못 동작하지 않는다면, 이는 처리하기 어려운 시나리오입니다. Tor의 경우 의심스러운 relay들을 합의에서 수동으로 제거할 수 있어 relay 케이스에서 훨씬 더 민첩하게 대응할 수 있습니다. I2P 네트워크에 대한 몇 가지 가능한 대응 방안이 아래에 나열되어 있지만, 이 중 어느 것도 완전히 만족스럽지는 않습니다:

- 악성 router 해시나 IP 목록을 수집하고, 다양한 수단(콘솔 뉴스, 웹사이트, 포럼 등)을 통해 목록을 공지합니다. 사용자는 해당 목록을 수동으로 다운로드하여 로컬 "블랙리스트"에 추가해야 합니다.
- 네트워크의 모든 사용자에게 수동으로 floodfill을 활성화하도록 요청합니다 (Sybil 공격을 더 많은 Sybil로 대응)
- 하드코딩된 "악성" 목록이 포함된 새로운 소프트웨어 버전을 릴리스합니다
- "악성" peer를 자동으로 식별하기 위해 peer 프로필 지표와 임계값을 개선한 새로운 소프트웨어 버전을 릴리스합니다.
- 단일 IP 블록에 너무 많은 floodfill이 있을 경우 이를 제외하는 소프트웨어를 추가합니다
- 단일 개인이나 그룹이 제어하는 자동 구독 기반 블랙리스트를 구현합니다. 이는 본질적으로 Tor "consensus" 모델의 일부를 구현하게 됩니다. 하지만 불행히도 이는 단일 개인이나 그룹이 특정 router나 IP의 네트워크 참여를 차단하거나, 심지어 전체 네트워크를 완전히 종료하거나 파괴할 권력을 갖게 합니다.

이 공격은 네트워크 크기가 커질수록 더 어려워집니다.

### Sybil Attack (부분 키스페이스)

공격자는 keyspace에서 밀접하게 클러스터된 소수(8-15개)의 floodfill router를 생성하고 이러한 router들의 RouterInfo를 널리 배포함으로써 [시빌 공격](https://www.freehaven.net/anonbib/cache/sybil.pdf)을 시도할 수 있습니다. 그러면 해당 keyspace의 키에 대한 모든 조회와 저장이 공격자의 router 중 하나로 전달됩니다. 성공할 경우, 이는 예를 들어 특정 I2P 사이트에 대한 효과적인 DOS 공격이 될 수 있습니다.

키스페이스가 키의 암호화(SHA256) Hash에 의해 인덱싱되므로, 공격자는 키에 충분히 가까운 router hash를 충분히 얻을 때까지 반복적으로 router hash를 생성하는 무차별 대입 방법을 사용해야 합니다. 이에 필요한 계산 능력의 양은 네트워크 크기에 따라 달라지며, 아직 알려지지 않았습니다.

이 공격에 대한 부분적인 방어책으로, Kademlia "근접성"을 결정하는 데 사용되는 알고리즘은 시간에 따라 변화합니다. 키의 해시(즉, H(k))를 사용하여 근접성을 결정하는 대신, 현재 날짜 문자열이 추가된 키의 해시, 즉 H(k + YYYYMMDD)를 사용합니다. "routing key generator"라고 불리는 함수가 이를 수행하며, 원래 키를 "routing key"로 변환합니다. 다시 말해, 전체 netDb 키스페이스가 UTC 자정마다 매일 "회전"합니다. 부분 키스페이스 공격은 매일 재생성되어야 하는데, 회전 후에는 공격하는 router들이 더 이상 대상 키나 서로에게 가깝지 않게 되기 때문입니다.

이 공격은 네트워크 크기가 커질수록 더 어려워집니다. 하지만 최근 연구에 따르면 키스페이스 순환이 특별히 효과적이지 않다는 것이 입증되었습니다. 공격자는 미리 수많은 router 해시를 사전 계산할 수 있으며, 순환 후 30분 내에 키스페이스의 일부를 "eclipse"하기 위해서는 소수의 router만 있으면 충분합니다.

일일 keyspace 회전의 한 가지 결과는 회전 후 몇 분 동안 분산 네트워크 데이터베이스가 불안정해질 수 있다는 것입니다. 새로운 "가장 가까운" router가 아직 저장소를 받지 못했기 때문에 조회가 실패할 것입니다. 이 문제의 범위와 완화 방법(예: 자정의 netDb "핸드오프")은 추가 연구 주제입니다.

### 부트스트랩 공격

공격자는 reseed 웹사이트를 장악하거나 개발자들을 속여서 자신의 reseed 웹사이트를 router의 하드코딩된 목록에 추가하도록 함으로써, 새로운 router들이 격리되거나 대부분이 통제된 네트워크로 부팅되도록 시도할 수 있습니다.

여러 방어 방법이 가능하며, 이 중 대부분이 계획되어 있습니다:

- 리시딩을 위해 HTTPS에서 HTTP로의 폴백을 허용하지 않음. MITM 공격자가 간단히 HTTPS를 차단한 다음 HTTP에 응답할 수 있습니다.
- 설치 프로그램에 리시드 데이터 번들링

구현된 방어 기능:

- 단일 사이트만 사용하는 대신 여러 reseed 사이트에서 각각 RouterInfo의 부분집합을 가져오도록 reseed 작업을 변경
- 네트워크 외부의 reseed 모니터링 서비스를 생성하여 주기적으로 reseed 웹사이트를 폴링하고 데이터가 오래되었거나 네트워크의 다른 관점과 일치하지 않는지 확인
- 릴리스 0.9.14부터 reseed 데이터는 서명된 zip 파일로 번들화되며 다운로드 시 서명이 검증됩니다. 자세한 내용은 [su3 사양](/docs/specs/updates/#su3)을 참조하세요.

### 쿼리 캡처

또한 [lookup](#routerinfo-and-leaseset-lookup)을 참조하세요 (참고: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 섹션 2.2-2.3에서 아래 이탤릭체 용어들에 대한 설명)

부트스트랩 공격과 유사하게, floodfill router를 사용하는 공격자는 자신이 통제하는 router들의 참조를 반환함으로써 피어들을 자신이 제어하는 router 하위 집합으로 "유도"하려고 시도할 수 있습니다.

이것은 탐색을 통해 작동할 가능성이 낮습니다. 탐색은 빈도가 낮은 작업이기 때문입니다. Router들은 일반적인 tunnel 구축 활동을 통해 대부분의 피어 참조를 획득합니다. 탐색 결과는 일반적으로 몇 개의 router 해시로 제한되며, 각 탐색 쿼리는 임의의 floodfill router로 전달됩니다.

릴리스 0.8.9부터 *반복적 검색*이 구현되었습니다. 검색에 대한 [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage 응답으로 반환된 floodfill router 참조에 대해, 이러한 참조들이 검색 키에 더 가깝거나 (또는 다음으로 가장 가까운) 경우 이를 따라갑니다. 요청하는 router는 참조들이 키에 더 가깝다고 신뢰하지 않습니다 (즉, 이들은 *검증 가능하게 정확합니다*). 또한 검색은 더 가까운 키를 찾지 못했을 때 멈추지 않고, 타임아웃이나 최대 쿼리 수에 도달할 때까지 다음으로 가장 가까운 노드를 쿼리하여 계속됩니다. 이는 악의적인 floodfill이 키 공간의 일부를 블랙홀링하는 것을 방지합니다. 또한 일일 키스페이스 회전은 공격자가 원하는 키 공간 영역 내에서 router 정보를 재생성하도록 요구합니다. 이 설계는 [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)에서 설명된 쿼리 캡처 공격을 훨씬 더 어렵게 만듭니다.

### DHT 기반 릴레이 선택

(참조: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) 섹션 3)

이것은 floodfill과는 크게 관련이 없지만, tunnel을 위한 피어 선택의 취약점에 대한 논의는 [피어 선택 페이지](/docs/overview/peer-selection/)를 참조하세요.

### 정보 유출

(참고: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Section 3)

이 논문은 Torsk와 NISAN에서 사용되는 "Finger Table" DHT 조회의 약점을 다룹니다. 언뜻 보면 이것들이 I2P에는 적용되지 않는 것으로 보입니다. 첫째, Torsk와 NISAN의 DHT 사용은 I2P의 그것과 상당히 다릅니다. 둘째, I2P의 network database 조회는 [peer selection](/docs/overview/peer-selection/)과 [tunnel building](/docs/overview/tunnel-routing/) 프로세스와 느슨하게만 연관되어 있습니다; tunnel에는 이전에 알려진 peer만 사용됩니다. 또한 peer selection은 DHT 키 근접성이라는 개념과는 무관합니다.

이 중 일부는 실제로 I2P 네트워크가 훨씬 커졌을 때 더 흥미로울 수 있습니다. 현재는 각 router가 네트워크의 상당 부분을 알고 있어서, 네트워크 데이터베이스에서 특정 Router Info를 조회하는 것이 해당 router를 tunnel에서 사용하려는 향후 의도를 강하게 나타내지는 않습니다. 아마도 네트워크가 100배 더 클 때, 조회가 더 상관성이 있을 수 있을 것입니다. 물론 더 큰 네트워크는 Sybil 공격을 훨씬 어렵게 만듭니다.

그러나 I2P에서 DHT 정보 누출의 일반적인 문제는 추가 조사가 필요합니다. floodfill router들은 쿼리를 관찰하고 정보를 수집할 수 있는 위치에 있습니다. 확실히 *f* = 0.2 수준(논문에서 명시한 20% 악성 노드)에서는 우리가 설명하는 많은 Sybil 위협([여기](/docs/overview/threat-model/#sybil), [여기](#sybil-attack-full-keyspace) 그리고 [여기](#sybil-attack-partial-keyspace))이 여러 가지 이유로 문제가 될 것으로 예상됩니다.

---

## 역사

[netdb 토론 페이지로 이동됨](/docs/legacy/netdb/).

---

## 향후 작업

추가 netDb 조회 및 응답의 종단간 암호화.

조회 응답을 추적하기 위한 더 나은 방법들.
