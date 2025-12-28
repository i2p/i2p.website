---
title: "UDP BitTorrent announce(트래커 상태 보고 및 피어 목록 요청)"
description: "I2P에서의 UDP 기반 BitTorrent 트래커 announce(트래커에 클라이언트 상태를 알리는 요청) 프로토콜 사양"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

이 명세서는 I2P에서의 UDP BitTorrent announce(트래커와 통신하기 위해 클라이언트가 보내는 상태 알림 요청) 프로토콜을 문서화한다. I2P에서의 BitTorrent 전반적인 명세는 [I2P 상의 BitTorrent 문서](/docs/applications/bittorrent/)를 참조하라. 이 명세의 개발 배경과 추가 정보는 [Proposal 160](/proposals/160-udp-trackers/)을 참조하라.

이 프로토콜은 2025년 6월 24일 공식 승인되었으며, 2025년 9월 8일 출시된 I2P 버전 2.10.0(API 0.9.67)에 구현되었습니다. 현재 I2P 네트워크에서는 여러 운영 환경 트래커와 i2psnark 클라이언트의 완전한 지원과 함께 UDP 트래커 지원이 정상적으로 동작합니다.

## 설계

본 사양서는 [I2P Datagram Specification](/docs/api/datagrams/)에 정의된 repliable datagram(회신 가능한 데이터그램)인 Datagram2와 Datagram3, 그리고 원시 데이터그램을 사용합니다. Datagram2와 Datagram3는 [Proposal 163](/proposals/163-datagram2/)에 정의된 repliable datagram의 변형입니다. Datagram2는 재플레이 공격 방지와 오프라인 서명 지원을 추가합니다. Datagram3는 기존 데이터그램 형식보다 더 작지만, 인증은 제공하지 않습니다.

### BEP(비트토렌트 개선 제안) 15

참고로, [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)에 정의된 메시지 흐름은 다음과 같습니다:

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
IP 주소 스푸핑을 방지하기 위해 연결 단계가 필요합니다. 트래커는 클라이언트가 이후 announce 요청에서 사용하는 연결 ID를 반환합니다. 이 연결 ID는 기본적으로 클라이언트 측에서는 1분, 트래커 측에서는 2분 후에 만료됩니다.

I2P는 기존의 UDP를 지원하는 클라이언트 코드베이스에의 도입 용이성, 효율성, 그리고 아래에서 논의되는 보안상의 이유로, BEP 15(BitTorrent Enhancement Proposal 15, 비트토렌트 개선 제안 15)와 동일한 메시지 흐름을 사용합니다:

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
이는 스트리밍(TCP) announce 메시지에 비해 잠재적으로 큰 대역폭 절감을 제공합니다. Datagram2(I2P 데이터그램 메시지 유형)는 스트리밍 SYN과 크기가 거의 비슷하지만, 원시 응답은 스트리밍 SYN ACK보다 훨씬 더 작습니다. 이후 요청은 Datagram3(I2P 데이터그램 메시지 유형)을 사용하며, 이후 응답은 원시 형식입니다.

announce 요청은 트래커가 연결 ID를 announce 목적지나 해시와 매핑하는 대규모 테이블을 유지할 필요가 없도록 Datagram3(데이터그램3 형식)로 전송된다. 대신, 트래커는 발신자 해시, 현재 타임스탬프(일정 주기에 기반), 그리고 비밀 값을 사용해 연결 ID를 암호학적으로 생성할 수 있다. announce 요청을 수신하면, 트래커는 연결 ID를 검증한 뒤, Datagram3 발신자 해시를 송신 대상으로 사용한다.

### 연결 수명

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)은 클라이언트에서는 연결 ID(connection ID)가 1분 후, 트래커에서는 2분 후에 만료된다고 명시한다. 이는 설정으로 변경할 수 없다. 따라서 클라이언트가 announce(트래커 통지)를 배치 처리하여 1분짜리 시간 창 안에 모두 수행하지 않는 한, 잠재적인 효율 향상은 제한된다. i2psnark는 현재 announce를 배치 처리하지 않고, 트래픽 급증을 피하기 위해 이를 분산시킨다. 고급 사용자가 한 번에 수천 개의 토렌트를 실행하는 것으로 보고되며, 그렇게 많은 announce를 1분 안에 몰아넣는 것은 현실적이지 않다.

여기서는 connect response를 확장하여 선택적 연결 수명 필드를 추가할 것을 제안한다. 해당 필드가 없으면 기본값은 1분이다. 그렇지 않은 경우, 초 단위로 지정된 수명을 클라이언트가 사용해야 하며, 트래커는 연결 ID를 1분 더 유지한다.

### BEP 15(비트토렌트 개선 제안 15)과의 호환성

이 설계는 기존 클라이언트와 트래커에서 필요한 변경을 최소화하기 위해 가능한 한 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와의 호환성을 유지합니다.

유일하게 요구되는 변경 사항은 announce response(announce 요청에 대한 응답) 내 피어 정보의 형식뿐입니다. connect response(connect 요청에 대한 응답)에 lifetime 필드를 추가하는 것은 필수는 아니지만, 위에서 설명했듯 효율성 향상을 위해 강력히 권장됩니다.

### 보안 분석

UDP 알림 프로토콜의 중요한 목표는 주소 스푸핑을 방지하는 것이다. 클라이언트는 실제로 존재해야 하며, 실제 leaseset을 포함해야 한다. Connect Response를 수신하려면 인바운드 tunnels를 보유하고 있어야 한다. 이러한 tunnels는 zero-hop으로 즉시 구축될 수도 있지만, 그렇게 하면 생성자가 노출된다. 이 프로토콜은 그 목표를 달성한다.

### 문제

이 프로토콜은 blinded destinations(블라인드된 목적지)를 지원하지 않지만, 이를 지원하도록 확장될 수 있습니다. 아래를 참조하십시오.

## 명세서

### 프로토콜 및 포트

회신 가능한 Datagram2는 I2CP protocol 19를 사용하며, 회신 가능한 Datagram3은 I2CP protocol 20을 사용합니다. 원시 데이터그램(raw datagrams)은 I2CP protocol 18을 사용합니다. 요청은 Datagram2 또는 Datagram3일 수 있습니다. 응답은 항상 원시 형식(raw)입니다. I2CP protocol 17을 사용하는 구형 회신 가능 데이터그램("Datagram1") 형식은 요청이나 응답에 절대 사용해서는 안 되며, 요청/응답 포트에서 수신될 경우 반드시 폐기되어야 합니다. 참고로 Datagram1 protocol 17은 여전히 DHT 프로토콜에서 사용됩니다.

요청은 announce URL(announce용 URL)에서 I2CP "to port"(목적지 포트)를 사용합니다. 아래를 참조하세요. 요청의 "from port"(발신 포트)는 클라이언트가 선택하지만 0이 아니어야 하며, 응답을 쉽게 분류할 수 있도록 DHT(분산 해시 테이블)에 사용하는 포트와는 달라야 합니다. 트래커는 잘못된 포트로 수신된 요청을 거부해야 합니다.

응답은 요청에서 지정된 I2CP "to port"(대상 포트)를 사용합니다. 응답의 "from port"(발신 포트)는 요청의 "to port"입니다.

### 알림 URL

announce URL 형식은 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)에 명시되어 있지 않지만, clearnet(일반 공개 인터넷)에서와 마찬가지로 UDP announce URL은 "udp://host:port/path" 형태입니다. 경로는 무시되며 비어 있을 수 있지만, clearnet에서는 일반적으로 "/announce"입니다. :port 부분은 항상 포함되어야 합니다; 그러나 ":port" 부분이 생략된 경우, clearnet에서 흔히 쓰이는 포트이므로 기본 I2CP 포트 6969를 사용하십시오. 또한 CGI 매개변수 &a=b&c=d 가 덧붙을 수 있으며; 이는 announce 요청에서 처리되어 제공될 수 있습니다. [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)을 참조하십시오. 매개변수나 경로가 없다면, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에서 암시된 바와 같이 마지막 / 역시 생략할 수 있습니다.

### 데이터그램 형식

모든 값은 네트워크 바이트 순서(빅 엔디언)로 전송됩니다. 패킷이 정확히 특정한 크기일 것이라고 기대하지 마십시오. 향후 확장으로 인해 패킷 크기가 증가할 수 있습니다.

#### 연결 요청

클라이언트에서 트래커로. 16바이트. 반드시 응답 가능한 Datagram2여야 합니다. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일합니다. 변경 없음.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### 연결 응답

트래커에서 클라이언트로. 16 또는 18 바이트. 반드시 raw 데이터여야 한다. 아래에 명시된 사항을 제외하면 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일하다.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
응답은 요청에서 "from port"로 수신한 값을 I2CP의 "to port"로 설정하여 반드시 전송해야 합니다.

lifetime 필드는 선택 사항이며, 초 단위로 클라이언트에서의 connection_id 수명을 나타냅니다. 기본값은 60이며, 지정하는 경우 최소값도 60입니다. 최대값은 65535로, 약 18시간에 해당합니다. 트래커는 클라이언트 수명보다 60초 더 길게 connection_id를 유지해야 합니다.

#### 공지 요청

클라이언트에서 트래커로. 최소 98바이트. 반드시 회신 가능한 Datagram3(데이터그램 버전 3)이어야 합니다. 아래에 명시된 사항을 제외하면 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일합니다.

connection_id는 connect 응답에서 받은 값 그대로입니다.

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
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 대비 변경 사항:

- key는 무시됩니다
- IP 주소는 사용되지 않습니다
- port는 아마 무시되지만 I2CP from port와 동일해야 합니다
- 옵션 섹션이 존재한다면, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에 정의된 대로입니다

응답은 요청에서 수신된 "from port"(발신 포트) 값이 지정하는 I2CP "to port"(목적지 포트)로 반드시 전송해야 한다. announce request(announce 요청)의 포트는 사용하지 마십시오.

#### Announce 응답

트래커에서 클라이언트로. 최소 20바이트. 반드시 raw(원시 데이터)여야 함. 아래에 명시된 사항을 제외하면 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일함.

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
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) 대비 변경 사항:

- 6바이트 IPv4+포트 또는 18바이트 IPv6+포트 대신, SHA-256 이진 피어 해시로 구성된 32바이트 크기의 "compact responses"(압축형 응답)들을 연속으로 반환합니다. TCP compact responses와 마찬가지로 포트는 포함하지 않습니다.

응답은 요청에서 "from port"로 전달된 값을 I2CP의 "to port"로 하여 반드시 전송해야 합니다. announce request(announce 요청)의 포트를 사용하지 마십시오.

I2P 데이터그램의 최대 크기는 약 64 KB로 매우 큽니다. 그러나 안정적인 전달을 위해서는 4 KB를 초과하는 데이터그램은 피하는 것이 좋습니다. 대역폭 효율을 위해 트래커는 최대 피어 수를 약 50개로 제한하는 것이 바람직합니다. 이는 여러 계층의 오버헤드가 붙기 전 기준으로 약 1600바이트짜리 패킷에 해당하며, 단편화 후에는 두 개의 tunnel 메시지 페이로드 제한 내에 들어가야 합니다.

BEP 15와 마찬가지로, 이후에 나열될 피어 주소의 개수(BEP 15에서는 IP/포트, 여기서는 해시값)를 나타내는 카운트는 포함되지 않습니다. BEP 15에서는 규정되어 있지 않지만, 모두 0으로 구성된 end-of-peers marker(피어 목록의 끝을 나타내는 마커)를 정의하여 피어 정보가 완료되었고 그 뒤에 일부 확장 데이터가 이어짐을 표시할 수 있습니다.

향후 해당 확장이 가능하도록, 클라이언트는 바이트가 모두 0인 32바이트 해시와 그 뒤따르는 모든 데이터를 무시해야 한다. 트래커는 해시가 모두 0인 경우의 announce(트래커에 대한 접속/상태 통지 요청)를 거부해야 하며, 해당 해시는 이미 Java routers에서 금지되어 있다.

#### 스크래핑

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html)의 scrape(트래커 통계 조회) 요청/응답은 이 명세에서 필수는 아니지만, 원한다면 아무 변경 없이 구현할 수 있다. 클라이언트는 먼저 connection ID를 획득해야 한다. scrape 요청은 항상 회신 가능한 Datagram3이다. scrape 응답은 항상 raw(원시 형식)이다.

#### 오류 응답

트래커에서 클라이언트로. 최소 8바이트(메시지가 비어 있는 경우). 반드시 raw여야 합니다. [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)와 동일합니다. 변경 없음.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## 확장 기능

확장 비트나 버전 필드는 포함되지 않습니다. 클라이언트와 트래커는 패킷이 특정 크기라고 가정해서는 안 됩니다. 이렇게 하면 호환성을 깨뜨리지 않고 추가 필드를 더할 수 있습니다. 필요한 경우 [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)에서 정의된 확장 형식을 사용할 것을 권장합니다.

연결 응답은 선택적 연결 ID 유효기간을 추가하도록 수정되었다.

blinded destination(블라인딩된 목적지) 지원이 필요하다면, [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) 형식(매개변수는 추후 결정 예정)을 사용하여 announce 요청의 끝에 블라인딩된 35바이트 주소를 추가하거나, 응답으로 블라인딩된 해시를 요청할 수 있다. 블라인딩된 35바이트 피어 주소 집합은 모두 0으로만 이루어진 32바이트 해시 뒤에 announce 응답의 끝에 추가될 수 있다.

## 구현 지침

통합되지 않았고 I2CP를 사용하지 않는 클라이언트와 트래커가 직면하는 과제에 대한 논의는 위의 설계 섹션을 참조하십시오.

### 클라이언트

특정 트래커 호스트명에 대해, 클라이언트는 HTTP URL보다 UDP URL을 선호해야 하며, 둘 모두에 announce(트래커에 클라이언트 상태를 통지하는 요청)를 보내서는 안 된다.

이미 BEP 15(비트토렌트 개선 제안 15)를 지원하는 클라이언트는 약간의 수정만 필요합니다.

클라이언트가 DHT 또는 다른 데이터그램 프로토콜을 지원하는 경우, 응답이 해당 포트로 돌아오고 DHT 메시지와 섞이지 않도록 요청의 "from port"로 다른 포트를 선택하는 것이 좋습니다. 클라이언트는 응답으로 원시 데이터그램만 수신합니다. 트래커는 클라이언트에게 repliable datagram2(응답 가능한 데이터그램 형식)를 절대 보내지 않습니다.

기본 opentracker 목록을 사용하는 클라이언트는, 알려진 opentracker들이 UDP를 지원하는 것이 확인된 후 그 목록을 업데이트하여 UDP URL을 추가해야 합니다.

클라이언트는 요청 재전송 기능을 구현할 수도 있고, 하지 않을 수도 있다. 재전송을 구현하는 경우, 초기 타임아웃을 최소 15초로 설정하고, 각 재전송마다 타임아웃을 두 배로 늘려야 한다(지수적 백오프).

클라이언트는 오류 응답을 받은 후에는 백오프(재시도 간격을 늘려 부하를 줄이는 동작)해야 합니다.

### 트래커

기존에 BEP 15를 지원하는 트래커는 소규모 수정만 필요하다. 이 사양은 트래커가 동일한 포트에서 응답 가능한 datagram2(데이터그램 버전 2)와 datagram3(데이터그램 버전 3)의 수신을 지원해야 한다는 점에서 2014년 제안과 다르다.

트래커의 리소스 요구 사항을 최소화하기 위해, 이 프로토콜은 추후 검증을 위해 트래커가 클라이언트 해시를 연결 ID에 매핑해 저장해야 하는 어떠한 요구도 제거하도록 설계되었다. 이는 announce 요청 패킷이 회신 가능한 Datagram3(데이터그램 v3) 패킷이므로 발신자의 해시를 포함하고 있기 때문이다.

권장 구현은 다음과 같습니다:

- 현재 epoch(에폭)을 연결 수명을 해상도로 하여 양자화한 현재 시간으로 정의한다, `epoch = now / lifetime`.
- 8바이트 길이의 출력을 생성하는 암호학적 해시 함수 `H(secret, clienthash, epoch)`를 정의한다.
- 모든 연결에서 사용되는 무작위 상수 secret 값을 생성한다.
- connect 응답에 대해서는 `connection_id = H(secret, clienthash, epoch)`를 생성한다.
- announce 요청에 대해서는, 현재 epoch에서 `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`를 확인하여 수신한 연결 ID를 검증한다.

## 배포 상태

이 프로토콜은 2025년 6월 24일에 승인되었으며 2025년 9월 기준으로 I2P 네트워크에서 완전히 운영되고 있습니다.

### 현재 구현체들

**i2psnark**: 완전한 UDP 트래커 지원은 2025년 9월 8일에 릴리스된 I2P 2.10.0 버전(API 0.9.67)에 포함되어 있습니다. 이 버전 이후의 모든 I2P 설치에는 기본적으로 UDP 트래커 기능이 포함됩니다.

**zzzot tracker**: 0.20.0-beta2 버전 이상에서 UDP announces(트래커에 상태를 보고하고 피어를 조회하는 요청)를 지원합니다. 2025년 10월 기준, 다음 프로덕션 트래커가 가동 중입니다: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### 클라이언트 호환성 참고 사항

**SAM v3.3 제약사항**: SAM(Simple Anonymous Messaging, 단순 익명 메시징)을 사용하는 외부 BitTorrent 클라이언트는 Datagram2/3에 대한 SAM v3.3 지원이 필요합니다. 이는 Java I2P에서는 제공되지만, 현재 i2pd(C++ I2P 구현체)에서는 지원되지 않아 qBittorrent와 같은 libtorrent 기반 클라이언트에서의 채택을 제한할 수 있습니다.

**I2CP 클라이언트**: I2CP를 직접 사용하는 클라이언트(예: BiglyBT)는 SAM의 제한 없이 UDP 트래커 지원을 구현할 수 있습니다.

## 참고 자료

- **[BEP15]**: [BitTorrent UDP 트래커 프로토콜](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [UDP 트래커 프로토콜 확장](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [I2P 데이터그램 명세](/docs/api/datagrams/)
- **[Prop160]**: [UDP 트래커 제안](/proposals/160-udp-trackers/)
- **[Prop163]**: [Datagram2 제안](/proposals/163-datagram2/)
- **[SPEC]**: [I2P 상의 BitTorrent](/docs/applications/bittorrent/)
