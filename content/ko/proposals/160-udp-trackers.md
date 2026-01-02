---
title: "UDP 트래커"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "닫힘"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## 상태

2025-06-24 검토에서 승인됨. 사양은 [UDP specification](/docs/specs/udp-bittorrent-announces/)에서 확인할 수 있습니다. zzzot 0.20.0-beta2에서 구현됨. API 0.9.67부터 i2psnark에서 구현됨. 다른 구현체의 상태는 해당 문서를 확인하세요.

## 개요

이 제안은 I2P에서 UDP tracker 구현에 관한 것입니다.

### Change History

I2P에서 UDP tracker에 대한 예비 제안이 2014년 5월 우리의 [bittorrent 사양 페이지](/docs/applications/bittorrent/)에 게시되었습니다. 이는 우리의 공식적인 제안 프로세스보다 앞서 있었고, 구현되지 않았습니다. 이 제안은 2022년 초에 작성되었으며 2014년 버전을 단순화합니다.

이 제안서는 응답 가능한 datagram에 의존하므로, 2023년 초에 [Datagram2 제안서](/proposals/163-datagram2/) 작업을 시작하면서 보류되었습니다. 해당 제안서는 2025년 4월에 승인되었습니다.

이 제안서의 2023년 버전은 "호환성"과 "빠른" 두 가지 모드를 명시했습니다. 추가 분석 결과 빠른 모드는 안전하지 않으며, 많은 수의 torrent를 가진 클라이언트에게는 비효율적일 것으로 밝혀졌습니다. 또한 BiglyBT는 호환성 모드에 대한 선호를 표명했습니다. 이 모드는 표준 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)를 지원하는 모든 tracker 또는 클라이언트에서 구현하기가 더 쉬울 것입니다.

호환성 모드는 클라이언트 측에서 처음부터 구현하기에는 더 복잡하지만, 2023년에 시작된 예비 코드가 있습니다.

따라서 여기의 현재 버전은 빠른 모드를 제거하고 "호환성"이라는 용어를 제거하여 더욱 단순화되었습니다. 현재 버전은 새로운 Datagram2 형식으로 전환하고, UDP announce 확장 프로토콜 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에 대한 참조를 추가합니다.

또한 이 프로토콜의 효율성 향상을 확장하기 위해 연결 응답에 연결 ID 수명 필드가 추가됩니다.

## Motivation

일반 사용자 기반과 특히 bittorrent 사용자 수가 계속 증가함에 따라, tracker들이 과부하되지 않도록 tracker와 announce를 더 효율적으로 만들어야 합니다.

Bittorrent는 2008년 BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)에서 UDP tracker를 제안했으며, 현재 clearnet상의 대부분의 tracker들이 UDP 전용입니다.

데이터그램과 스트리밍 프로토콜의 대역폭 절약을 계산하기는 어렵습니다. 응답 가능한 요청은 스트리밍 SYN과 거의 같은 크기이지만, HTTP GET에 600바이트의 거대한 URL 매개변수 문자열이 있기 때문에 페이로드는 약 500바이트 더 작습니다. 원시 응답은 스트리밍 SYN ACK보다 훨씬 작아서 트래커의 아웃바운드 트래픽을 크게 줄여줍니다.

또한 데이터그램은 스트리밍 연결보다 메모리 내 상태를 훨씬 적게 요구하므로, 구현별 메모리 감소 효과가 있어야 합니다.

[/proposals/169-pq-crypto/](/proposals/169-pq-crypto/)에서 구상된 Post-Quantum 암호화 및 서명은 destination, leaseSet, 스트리밍 SYN 및 SYN ACK를 포함한 암호화되고 서명된 구조의 오버헤드를 상당히 증가시킬 것입니다. I2P에서 PQ 암호화가 채택되기 전에 가능한 한 이러한 오버헤드를 최소화하는 것이 중요합니다.

## 동기

이 제안서는 [/docs/api/datagrams/](/docs/api/datagrams/)에 정의된 대로 repliable datagram2, repliable datagram3, 그리고 raw datagram을 사용합니다. Datagram2와 Datagram3은 제안서 163 [/proposals/163-datagram2/](/proposals/163-datagram2/)에서 정의된 repliable datagram의 새로운 변형입니다. Datagram2는 재생 공격 저항성과 오프라인 서명 지원을 추가합니다. Datagram3은 기존 datagram 형식보다 작지만 인증 기능이 없습니다.

### BEP 15

참고로, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)에서 정의된 메시지 플로우는 다음과 같습니다:

```
Client                        Tracker
    Connect Req. ------------->
      <-------------- Connect Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
    Announce Req. ------------->
      <-------------- Announce Resp.
```
연결 단계는 IP 주소 스푸핑을 방지하기 위해 필요합니다. tracker는 클라이언트가 후속 announce에서 사용하는 연결 ID를 반환합니다. 이 연결 ID는 기본적으로 클라이언트에서 1분, tracker에서 2분 후에 만료됩니다.

I2P는 기존 UDP 지원 클라이언트 코드베이스에서의 채택 용이성, 효율성, 그리고 아래에서 논의되는 보안상의 이유로 BEP 15와 동일한 메시지 플로우를 사용할 것입니다:

```
Client                        Tracker
    Connect Req. ------------->       (Repliable Datagram2)
      <-------------- Connect Resp.   (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
    Announce Req. ------------->      (Repliable Datagram3)
      <-------------- Announce Resp.  (Raw)
             ...
```
이는 스트리밍(TCP) 공지보다 상당한 대역폭 절약을 제공할 수 있습니다. Datagram2는 스트리밍 SYN과 거의 같은 크기이지만, 원시 응답은 스트리밍 SYN ACK보다 훨씬 작습니다. 후속 요청은 Datagram3을 사용하며, 후속 응답은 원시 형태입니다.

announce 요청은 Datagram3이므로 tracker는 연결 ID를 announce 목적지나 해시에 매핑하는 대규모 매핑 테이블을 유지할 필요가 없습니다. 대신, tracker는 발신자 해시, 현재 타임스탬프(특정 간격 기반), 그리고 비밀 값으로부터 암호학적으로 연결 ID를 생성할 수 있습니다. announce 요청을 받으면, tracker는 연결 ID를 검증하고, Datagram3 발신자 해시를 전송 대상으로 사용합니다.

### 변경 이력

통합 애플리케이션(한 프로세스에서 router와 클라이언트가 함께 실행되는 경우, 예를 들어 i2psnark와 ZzzOT Java 플러그인)이나 I2CP 기반 애플리케이션(예를 들어 BiglyBT)의 경우, 스트리밍과 데이터그램 트래픽을 별도로 구현하고 라우팅하는 것이 간단해야 합니다. ZzzOT와 i2psnark가 이 제안을 구현하는 첫 번째 tracker와 클라이언트가 될 것으로 예상됩니다.

비통합 tracker와 클라이언트에 대해서는 아래에서 설명합니다.

#### Trackers

알려진 I2P tracker 구현체는 네 가지가 있습니다:

- zzzot, 통합 Java router 플러그인으로, opentracker.dg2.i2p 및 기타 여러 곳에서 실행 중
- tracker2.postman.i2p, Java router와 HTTP Server tunnel 뒤에서 실행되는 것으로 추정
- zzz가 포팅한 기존 C opentracker, UDP 지원은 주석 처리됨
- r4sas가 포팅한 새로운 C opentracker, opentracker.r4sas.i2p 및 기타 가능한 곳에서 실행 중,
  i2pd router와 HTTP Server tunnel 뒤에서 실행되는 것으로 추정

현재 HTTP 서버 tunnel을 사용하여 announce 요청을 수신하는 외부 tracker 애플리케이션의 경우, 구현이 상당히 어려울 수 있습니다. 데이터그램을 로컬 HTTP 요청/응답으로 변환하는 전용 tunnel을 개발할 수 있습니다. 또는 HTTP 요청과 데이터그램을 모두 처리하여 데이터그램을 외부 프로세스로 전달하는 전용 tunnel을 설계할 수도 있습니다. 이러한 설계 결정은 특정 router와 tracker 구현에 크게 의존하며, 본 제안서의 범위를 벗어납니다.

#### Clients

qbittorrent 및 기타 libtorrent 기반 클라이언트와 같은 외부 SAM 기반 토렌트 클라이언트는 i2pd에서 지원되지 않는 [SAM v3.3](/docs/api/samv3/)이 필요합니다. 이는 DHT 지원에도 필요하며, 알려진 SAM 토렌트 클라이언트가 구현하기에는 충분히 복잡합니다. 이 제안의 SAM 기반 구현은 곧 기대되지 않습니다.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)는 연결 ID가 클라이언트에서 1분 후에, 트래커에서 2분 후에 만료되도록 지정합니다. 이는 설정할 수 없습니다. 이는 클라이언트가 1분 창 내에 모든 announce를 일괄 처리하지 않는 한 잠재적인 효율성 향상을 제한합니다. i2psnark는 현재 announce를 일괄 처리하지 않으며, 트래픽 버스트를 피하기 위해 분산시킵니다. 파워 유저들이 수천 개의 토렌트를 동시에 실행하고 있다고 보고되고 있으며, 그 많은 announce를 1분 안에 버스트시키는 것은 현실적이지 않습니다.

여기서는 연결 응답을 확장하여 선택적 연결 수명 필드를 추가할 것을 제안합니다. 존재하지 않는 경우 기본값은 1분입니다. 그렇지 않으면, 초 단위로 지정된 수명을 클라이언트가 사용하며, tracker는 연결 ID를 1분 더 유지합니다.

### Compatibility with BEP 15

이 설계는 기존 클라이언트와 tracker에서 필요한 변경사항을 제한하기 위해 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 가능한 한 호환성을 유지합니다.

필요한 유일한 변경사항은 announce 응답에서 peer 정보의 형식입니다. connect 응답에서 lifetime 필드를 추가하는 것은 필수는 아니지만 위에서 설명한 바와 같이 효율성을 위해 강력히 권장됩니다.

### BEP 15

UDP announce 프로토콜의 중요한 목표는 주소 스푸핑을 방지하는 것입니다. 클라이언트는 실제로 존재해야 하며 실제 leaseSet을 번들로 제공해야 합니다. Connect Response를 수신하기 위해 인바운드 터널을 가져야 합니다. 이러한 터널들은 제로홉이며 즉시 구축될 수 있지만, 그렇게 하면 생성자가 노출될 것입니다. 이 프로토콜은 해당 목표를 달성합니다.

### Tracker/Client 지원

- 이 제안은 blinded destination을 지원하지 않지만,
  향후 확장하여 지원할 수 있습니다. 아래를 참조하세요.

## 설계

### Protocols and Ports

Repliable Datagram2는 I2CP protocol 19를 사용합니다; repliable Datagram3는 I2CP protocol 20을 사용합니다; raw datagram은 I2CP protocol 18을 사용합니다. 요청은 Datagram2 또는 Datagram3가 될 수 있습니다. 응답은 항상 raw입니다. I2CP protocol 17을 사용하는 이전 repliable datagram("Datagram1") 형식은 요청이나 응답에 사용되어서는 안 되며; 요청/응답 포트에서 수신된 경우 삭제되어야 합니다. Datagram1 protocol 17은 여전히 DHT protocol에 사용된다는 점에 유의하십시오.

요청은 공지 URL의 I2CP "to port"를 사용합니다. 아래를 참조하세요. 요청 "from port"는 클라이언트가 선택하지만, 0이 아니어야 하고 DHT에서 사용하는 포트와는 다른 포트여야 응답을 쉽게 분류할 수 있습니다. 트래커는 잘못된 포트에서 수신된 요청을 거부해야 합니다.

응답은 요청의 I2CP "to port"를 사용합니다. 요청의 "from port"는 요청의 "to port"입니다.

### Announce URL

announce URL 형식은 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)에 명시되어 있지 않지만, clearnet에서와 마찬가지로 UDP announce URL은 "udp://host:port/path" 형태입니다. 경로는 무시되며 비어있을 수 있지만, clearnet에서는 일반적으로 "/announce"입니다. :port 부분은 항상 존재해야 하지만, ":port" 부분이 생략된 경우 기본 I2CP 포트인 6969를 사용합니다. 이는 clearnet에서 일반적인 포트이기 때문입니다. 또한 &a=b&c=d와 같은 cgi 매개변수가 추가될 수 있으며, 이들은 처리되어 announce 요청에서 제공될 수 있습니다. [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)을 참조하십시오. 매개변수나 경로가 없는 경우, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에서 암시하는 바와 같이 후행 /도 생략될 수 있습니다.

### 연결 수명

모든 값은 네트워크 바이트 순서(big endian)로 전송됩니다. 패킷이 정확히 특정 크기일 것으로 기대하지 마십시오. 향후 확장으로 인해 패킷 크기가 증가할 수 있습니다.

#### Connect Request

클라이언트에서 tracker로. 16바이트. 응답 가능한 Datagram2여야 함. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일. 변경사항 없음.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker에서 클라이언트로. 16바이트 또는 18바이트. 반드시 raw여야 합니다. 아래에 명시된 것을 제외하고는 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일합니다.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
응답은 요청 "from port"로 수신된 I2CP "to port"로 반드시 전송되어야 합니다.

lifetime 필드는 선택사항이며 connection_id 클라이언트 수명을 초 단위로 나타냅니다. 기본값은 60이고, 지정할 경우 최솟값은 60입니다. 최댓값은 65535 또는 약 18시간입니다. 트래커는 클라이언트 수명보다 60초 더 오래 connection_id를 유지해야 합니다.

#### Announce Request

클라이언트에서 tracker로. 최소 98바이트. 응답 가능한 Datagram3이어야 함. 아래 명시된 사항을 제외하고는 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일함.

connection_id는 connect 응답에서 수신된 값입니다.

```
Offset  Size            Name            Value
  0       64-bit integer  connection_id
  8       32-bit integer  action          1     // announce
  12      32-bit integer  transaction_id
  16      20-byte string  info_hash
  36      20-byte string  peer_id
  56      64-bit integer  downloaded
  64      64-bit integer  left
  72      64-bit integer  uploaded
  80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)로부터의 변경사항:

- key는 무시됨
- port는 아마 무시됨
- options 섹션이 있는 경우, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에서 정의된 대로

응답은 요청의 "from port"로 받은 I2CP "to port"로 반드시 전송되어야 합니다. announce 요청의 포트를 사용하지 마십시오.

#### Announce Response

트래커에서 클라이언트로. 최소 20바이트. raw 형식이어야 함. 아래 명시된 사항을 제외하고는 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일.

```
Offset  Size            Name            Value
  0           32-bit integer  action          1 // announce
  4           32-bit integer  transaction_id
  8           32-bit integer  interval
  12          32-bit integer  leechers
  16          32-bit integer  seeders
  20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
  ...                                           // Change from BEP 15
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)로부터의 변경사항:

- IPv4+포트 6바이트 또는 IPv6+포트 18바이트 대신, SHA-256 바이너리 피어 해시가 포함된 32바이트의 배수인 "compact responses"를 반환합니다.
  TCP compact responses와 마찬가지로 포트는 포함하지 않습니다.

응답은 요청의 "from port"로 수신된 I2CP "to port"로 반드시 전송되어야 합니다. announce 요청의 포트를 사용하지 마십시오.

I2P 데이터그램은 약 64 KB의 매우 큰 최대 크기를 가지지만, 안정적인 전송을 위해서는 4 KB보다 큰 데이터그램은 피해야 합니다. 대역폭 효율성을 위해 tracker들은 최대 피어 수를 약 50개 정도로 제한해야 하며, 이는 다양한 계층의 오버헤드를 제외하고 약 1600바이트 패킷에 해당하고, 단편화 후 two-tunnel-message 페이로드 제한 내에 있어야 합니다.

BEP 15에서와 같이, 뒤따르는 피어 주소(BEP 15의 경우 IP/포트, 여기서는 해시)의 개수가 포함되지 않습니다. BEP 15에서는 고려되지 않았지만, 모든 값이 0인 피어 종료 마커를 정의하여 피어 정보가 완료되었고 일부 확장 데이터가 따른다는 것을 나타낼 수 있습니다.

향후 확장이 가능하도록, 클라이언트는 32바이트 모두 0인 해시와 그 뒤에 오는 모든 데이터를 무시해야 합니다. 트래커는 모두 0인 해시로부터의 announce를 거부해야 하며, 해당 해시는 이미 Java router에서 금지되어 있습니다.

#### Scrape

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)의 Scrape 요청/응답은 이 제안서에서 필수사항은 아니지만, 원한다면 구현할 수 있으며 변경사항은 필요하지 않습니다. 클라이언트는 먼저 connection ID를 획득해야 합니다. scrape 요청은 항상 repliable Datagram3입니다. scrape 응답은 항상 raw입니다.

#### 트래커

Tracker에서 클라이언트로. 최소 8바이트 (메시지가 비어있는 경우). 반드시 raw여야 함. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일. 변경사항 없음.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

확장 비트나 버전 필드는 포함되지 않습니다. 클라이언트와 트래커는 패킷이 특정 크기라고 가정해서는 안 됩니다. 이러한 방식으로 호환성을 깨뜨리지 않고 추가 필드를 추가할 수 있습니다. 필요한 경우 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에 정의된 확장 형식이 권장됩니다.

연결 응답이 선택적 연결 ID 수명을 추가하도록 수정되었습니다.

blinded destination 지원이 필요한 경우, announce 요청 끝에 blinded 35바이트 주소를 추가하거나, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 형식을 사용하여 응답에서 blinded 해시를 요청할 수 있습니다 (매개변수는 추후 결정). blinded 35바이트 피어 주소 세트는 모두 0인 32바이트 해시 이후, announce 응답 끝에 추가될 수 있습니다.

## Implementation guidelines

통합되지 않은, I2CP가 아닌 클라이언트와 트래커의 문제점에 대한 논의는 위의 설계 섹션을 참조하세요.

### BEP 15와의 호환성

주어진 tracker 호스트명에 대해, 클라이언트는 HTTP URL보다 UDP를 선호해야 하며, 두 방식 모두에 announce해서는 안 됩니다.

기존 BEP 15 지원을 가진 클라이언트는 작은 수정만 필요합니다.

클라이언트가 DHT나 다른 datagram 프로토콜을 지원하는 경우, 응답이 해당 포트로 돌아와서 DHT 메시지와 섞이지 않도록 요청 "from port"로 다른 포트를 선택해야 합니다. 클라이언트는 응답으로 원시 datagram만 수신합니다. 트래커는 클라이언트에게 응답 가능한 datagram2를 보내지 않습니다.

기본 opentrackers 목록을 가진 클라이언트들은 알려진 opentrackers가 UDP를 지원하는 것으로 확인된 후 목록을 업데이트하여 UDP URL을 추가해야 합니다.

클라이언트는 요청의 재전송을 구현할 수도 있고 구현하지 않을 수도 있습니다. 재전송을 구현하는 경우, 최소 15초의 초기 타임아웃을 사용해야 하며, 각 재전송마다 타임아웃을 두 배로 늘려야 합니다(지수적 백오프).

클라이언트는 오류 응답을 받은 후 백오프해야 합니다.

### 보안 분석

기존 BEP 15 지원이 있는 tracker들은 작은 수정만 필요할 것입니다. 이 제안은 2014년 제안과 다른 점은 tracker가 동일한 포트에서 repliable datagram2와 datagram3 수신을 지원해야 한다는 것입니다.

tracker 리소스 요구사항을 최소화하기 위해, 이 프로토콜은 tracker가 나중에 검증하기 위해 클라이언트 해시와 연결 ID의 매핑을 저장해야 하는 요구사항을 제거하도록 설계되었습니다. 이는 announce 요청 패킷이 응답 가능한 Datagram3 패킷이므로 발신자의 해시를 포함하고 있기 때문에 가능합니다.

권장되는 구현은 다음과 같습니다:

- 현재 epoch를 연결 수명의 해상도를 가진 현재 시간으로 정의합니다,
  ``epoch = now / lifetime``.
- 8바이트 출력을 생성하는 암호화 해시 함수 ``H(secret, clienthash, epoch)``를 정의합니다.
- 모든 연결에 사용되는 랜덤 상수 secret을 생성합니다.
- 연결 응답의 경우, ``connection_id = H(secret,  clienthash, epoch)``를 생성합니다.
- announce 요청의 경우, 다음을 검증하여 현재 epoch에서 수신된 connection ID를 검증합니다
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

기존 클라이언트들은 UDP announce URL을 지원하지 않으며 이를 무시합니다.

기존 tracker들은 응답 가능하거나 원시 데이터그램의 수신을 지원하지 않으므로, 해당 데이터그램들은 삭제됩니다.

이 제안은 완전히 선택 사항입니다. 클라이언트나 트래커 모두 언제든지 이를 구현할 필요가 없습니다.

## Rollout

첫 번째 구현은 ZzzOT와 i2psnark에서 이루어질 것으로 예상됩니다. 이들은 이 제안의 테스트와 검증을 위해 사용될 것입니다.

테스트 및 검증이 완료된 후 필요에 따라 다른 구현들이 따를 예정입니다.
