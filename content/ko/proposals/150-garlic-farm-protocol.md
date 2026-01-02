---
title: "Garlic Farm 프로토콜"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Open"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## 개요

이 문서는 JRaft 및 TCP 위의 "exts" 코드, "dmprinter" 샘플 애플리케이션 [JRAFT](https://github.com/datatechnology/jraft)를 기반으로 하는 Garlic Farm 와이어 프로토콜의 명세서입니다. JRaft는 Raft 프로토콜의 구현체입니다 [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

문서화된 와이어 프로토콜을 가진 구현체를 찾을 수 없었습니다. 그러나 JRaft 구현체는 코드 검토를 통해 그 프로토콜을 문서화할 수 있을 정도로 충분히 단순합니다. 이 제안서는 그 노력의 결과입니다.

이 프로토콜은 Meta LeaseSet에서 항목을 게시하는 라우터의 조정을 위한 백엔드가 될 것입니다. 제안서 123을 참조하세요.


## 목표

- 작은 코드 크기
- 기존 구현을 기반으로 함
- 직렬화된 자바 객체나 자바 특별 기능 또는 인코딩을 사용하지 않음
- 부트스트래핑은 범위 외임. 적어도 다른 서버 하나가 하드코딩되거나 이 프로토콜 외부에서 설정된 것으로 가정
- 외부 및 I2P 내 사용 사례 모두 지원


## 설계

Raft 프로토콜은 구체적인 프로토콜이 아닙니다. 상태 머신만 정의합니다. 따라서 JRaft의 구체적인 프로토콜을 문서화하고 그것을 기반으로 우리의 프로토콜을 설계합니다. JRaft 프로토콜에는 인증 핸드셰이크의 추가 외에 변경 사항이 없습니다.

Raft는 로그를 게시하는 역할을 하는 리더를 선출합니다. 로그는 Raft 구성 데이터 및 애플리케이션 데이터를 포함합니다. 애플리케이션 데이터는 각 서버의 라우터 상태 및 Meta LS2 클러스터의 대상지를 포함합니다. 서버들은 Meta LS2의 게시자와 내용을 결정하기 위해 공통 알고리즘을 사용합니다. Meta LS2의 게시자는 반드시 Raft 리더일 필요는 없습니다.


## 명세서

와이어 프로토콜은 SSL 소켓이나 비-SSL I2P 소켓 위에서 작동합니다. I2P 소켓은 HTTP 프록시를 통해 프록시됩니다. 클리어넷 비-SSL 소켓 지원은 없습니다.

### 핸드셰이크 및 인증

JRaft에 의해 정의되지 않음.

목표:

- 사용자/비밀번호 인증 방법
- 버전 식별자
- 클러스터 식별자
- 확장 가능
- I2P 소켓에 사용되는 경우 프록시의 용이성
- 서버를 Garlic Farm 서버로 불필요하게 노출하지 않음
- 완전한 웹 서버 구현이 필요 없는 간단한 프로토콜
- 일반적인 표준과 호환 가능하여, 원하는 경우 구현체에서 표준 라이브러리를 사용할 수 있음

우리는 websocket 유사한 핸드셰이크 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)와 HTTP Digest 인증을 사용할 것입니다 [RFC-2617](https://tools.ietf.org/html/rfc2617). RFC 2617의 기본 인증은 지원하지 않습니다. HTTP 프록시를 통해 프록시 되는 경우 [RFC-2616](https://tools.ietf.org/html/rfc2616)에 명시된 대로 프록시와 통신합니다.

#### 크리덴셜

사용자 이름과 비밀번호가 클러스터 별인지, 서버 별인지는 구현에 따라 다릅니다.


#### HTTP 요청 1

발신자는 다음을 전송합니다.

모든 라인은 HTTP 요구 사항에 따라 CRLF로 종료됩니다.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: close
  (여타 헤더는 무시됩니다)
  (빈 줄)

  CLUSTER는 클러스터의 이름입니다 (기본값 "farm")
  VERSION은 Garlic Farm 버전입니다 (현재 "1")
```


#### HTTP 응답 1

경로가 정확하지 않으면 수신자는 [RFC-2616](https://tools.ietf.org/html/rfc2616)에 명시된 대로 표준 "HTTP/1.1 404 Not Found" 응답을 전송할 것입니다.

경로가 정확하면 수신자는 [RFC-2617](https://tools.ietf.org/html/rfc2617)에 명시된 대로 WWW-Authenticate HTTP 다이제스트 인증 헤더를 포함한 표준 "HTTP/1.1 401 Unauthorized" 응답을 전송할 것입니다.

양쪽 당사자는 소켓을 닫습니다.


#### HTTP 요청 2

발신자는 [RFC-2617](https://tools.ietf.org/html/rfc2617) 와 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket) 에서처럼 다음을 전송합니다.

모든 라인은 HTTP 요구 사항에 따라 CRLF로 종료됩니다.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Host: (ip):(port)
  Cache-Control: no-cache
  Connection: keep-alive, Upgrade
  Upgrade: websocket
  (프록시된 경우 Sec-Websocket-* 헤더)
  Authorization: (RFC 2617에 명시된 HTTP 다이제스트 인증 헤더)
  (여타 헤더는 무시됩니다)
  (빈 줄)

  CLUSTER는 클러스터의 이름입니다 (기본값 "farm")
  VERSION은 Garlic Farm 버전입니다 (현재 "1")
```


#### HTTP 응답 2

인증이 정확하지 않으면 수신자는 [RFC-2617](https://tools.ietf.org/html/rfc2617)에 명시된 대로 또 다른 표준 "HTTP/1.1 401 Unauthorized" 응답을 전송할 것입니다.

인증이 정확하다면, 수신자는 [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)에 명시된 대로 다음 응답을 전송합니다.

모든 라인은 HTTP 요구 사항에 따라 CRLF로 종료됩니다.

```text
HTTP/1.1 101 Switching Protocols
  Connection: Upgrade
  Upgrade: websocket
  (Sec-Websocket-* 헤더)
  (여타 헤더는 무시됩니다)
  (빈 줄)
```

이후 이러한 응답이 수신되면 소켓은 열린 상태로 유지됩니다. 같은 소켓에서 아래에 정의된 Raft 프로토콜이 시작됩니다.


#### 캐싱

크리덴셜은 최소한 한 시간 동안 캐시되어야 하며,
그 이후의 연결들은 위의 "HTTP 요청 2"로 바로 건너뛸 수 있습니다.


### 메시지 유형

메시지에는 요청과 응답 두 가지 유형이 있습니다.
요청은 로그 항목을 포함할 수 있으며 가변 크기입니다;
응답은 로그 항목을 포함하지 않으며 고정 크기입니다.

메시지 유형 1-4는 Raft에서 정의한 표준 RPC 메시지입니다.
이는 핵심 Raft 프로토콜입니다.

메시지 유형 5-15는
JRaft가 정의한 확장 RPC 메시지로, 클라이언트, 동적인 서버 변경,
효율적인 로그 동기화를 지원합니다.

메시지 유형 16-17은 Raft 섹션 7에 정의된 로그 압축 RPC 메시지입니다.


| 메시지 | 번호 | 발신자 | 수신자 | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | 후보 | 팔로워 | 표준 Raft RPC; 로그 항목을 포함해서는 안 됨 |
| RequestVoteResponse | 2 | 팔로워 | 후보 | 표준 Raft RPC |
| AppendEntriesRequest | 3 | 리더 | 팔로워 | 표준 Raft RPC |
| AppendEntriesResponse | 4 | 팔로워 | 리더 / 클라이언트 | 표준 Raft RPC |
| ClientRequest | 5 | 클라이언트 | 리더 / 팔로워 | 응답은 AppendEntriesResponse; 애플리케이션 로그 항목만 포함해야 함 |
| AddServerRequest | 6 | 클라이언트 | 리더 | 단일 ClusterServer 로그 항목만 포함해야 함 |
| AddServerResponse | 7 | 리더 | 클라이언트 | 리더는 또한 JoinClusterRequest를 전송함 |
| RemoveServerRequest | 8 | 팔로워 | 리더 | 단일 ClusterServer 로그 항목만 포함해야 함 |
| RemoveServerResponse | 9 | 리더 | 팔로워 | |
| SyncLogRequest | 10 | 리더 | 팔로워 | 단일 LogPack 로그 항목만 포함해야 함 |
| SyncLogResponse | 11 | 팔로워 | 리더 | |
| JoinClusterRequest | 12 | 리더 | 새로운 서버 | 참여 초대; 단일 Configuration 로그 항목만 포함해야 함 |
| JoinClusterResponse | 13 | 새로운 서버 | 리더 | |
| LeaveClusterRequest | 14 | 리더 | 팔로워 | 클러스터를 떠나라는 명령 |
| LeaveClusterResponse | 15 | 팔로워 | 리더 | |
| InstallSnapshotRequest | 16 | 리더 | 팔로워 | Raft 섹션 7; 단일 SnapshotSyncRequest 로그 항목만 포함해야 함 |
| InstallSnapshotResponse | 17 | 팔로워 | 리더 | Raft 섹션 7 |


### 설정

HTTP 핸드셰이크 후, 설정 순서는 다음과 같습니다:

```text
새 서버 Alice              랜덤 팔로워 Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Bob이 리더임을 알리면, 아래와 같이 계속합니다.
  그렇지 않으면, Alice는 Bob과의 연결을 끊고 리더에게 연결해야 합니다.


  새 서버 Alice              리더 Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       또는 InstallSnapshotRequest
  SyncLogResponse  ------->
  또는 InstallSnapshotResponse
```

연결 해제 순서:

```text
팔로워 Alice              리더 Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

선거 순서:

```text
후보 Alice               팔로워 Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  Alice가 선거에서 이기면:

  리더 Alice                팔로워 Bob

  AppendEntriesRequest   ------->
  (하트비트)
          <---------   AppendEntriesResponse
```


### 정의

- 소스: 메시지의 발신자를 식별
- 목적지: 메시지의 수신자를 식별
- 용어: Raft 참고. 0으로 초기화되고 단조롭게 증가함
- 색인: Raft 참고. 0으로 초기화되고 단조롭게 증가함


### 요청

요청은 헤더와 하나 이상의 로그 항목을 포함합니다.
요청은 고정 크기 헤더와 가변 크기의 로그 항목을 포함합니다.


#### 요청 헤더

요청 헤더는 45 바이트로 구성됩니다. 모든 값은 부호 없는 빅 엔디안입니다.

```dataspec
메시지 유형:      1 바이트
  소스:            ID, 4 바이트 정수
  목적지:           ID, 4 바이트 정수
  용어:              현재 용어 (참고사항 참조), 8 바이트 정수
  마지막 로그 용어:     8 바이트 정수
  마지막 로그 색인:    8 바이트 정수
  커밋 색인:      8 바이트 정수
  로그 항목 크기:  총 크기(바이트), 4 바이트 정수
  로그 항목:       아래 참조, 지정된 총 길이
```


#### 참고사항

RequestVoteRequest에서는 용어가 후보의 용어입니다.
그 외에는, 리더의 현재 용어입니다.

AppendEntriesRequest에서는, 로그 항목 크기가 0일 때,
이 메시지는 하트비트(keepalive) 메시지입니다.


#### 로그 항목

로그에는 0개 이상의 로그 항목이 포함되어 있습니다.
각 로그 항목은 다음과 같습니다. 모든 값은 부호 없는 빅 엔디안입니다.

```dataspec
용어:           8 바이트 정수
  값 유형:     1 바이트
  항목 크기:     바이트 단위, 4 바이트 정수
  항목:          지정된 길이
```


#### 로그 내용

모든 값은 부호 없는 빅 엔디안입니다.

| 로그 값 유형 | 번호 |
| :--- | :--- |
| 애플리케이션 | 1 |
| 구성 | 2 |
| 클러스터 서버 | 3 |
| 로그팩 | 4 |
| 스냅샷동기화요청 | 5 |


#### 애플리케이션

애플리케이션 내용은 UTF-8로 인코딩된 [JSON](https://www.json.org/)입니다.
애플리케이션 레이어 부분을 참조하세요.


#### 구성

이는 리더가 새로운 클러스터 구성을 직렬화하고 피어들에게 복제하기 위해 사용됩니다.
0개 이상의 ClusterServer 구성을 포함합니다.


```dataspec
로그 색인:  8 바이트 정수
  마지막 로그 색인:  8 바이트 정수
  각 서버의 ClusterServer 데이터:
    ID:                4 바이트 정수
    엔드포인트 데이터 길이: 바이트 단위, 4 바이트 정수
    엔드포인트 데이터:  "tcp://localhost:9001" 형식의 ASCII 문자열, 지정된 길이
```


#### 클러스터 서버

클러스터 내 서버의 구성 정보입니다.
이는 AddServerRequest 또는 RemoveServerRequest 메시지에만 포함됩니다.

AddServerRequest 메시지에서 사용될 때:

```dataspec
ID:                4 바이트 정수
  엔드포인트 데이터 길이: 바이트 단위, 4 바이트 정수
  엔드포인트 데이터:     "tcp://localhost:9001" 형식의 ASCII 문자열, 지정된 길이
```


RemoveServerRequest 메시지에서 사용될 때:

```dataspec
ID:                4 바이트 정수
```


#### 로그팩

이것은 SyncLogRequest 메시지에만 포함됩니다.

다음은 전송 전에 gzip으로 압축됩니다:


```dataspec
색인 데이터 길이: 바이트 단위, 4 바이트 정수
  로그 데이터 길이:   바이트 단위, 4 바이트 정수
  색인 데이터:     각 색인에 대해 8 바이트, 지정된 길이
  로그 데이터:       지정된 길이
```


#### 스냅샷동기화요청

이것은 InstallSnapshotRequest 메시지에만 포함됩니다.

```dataspec
마지막 로그 색인:  8 바이트 정수
  마지막 로그 용어:   8 바이트 정수
  구성 데이터 길이: 바이트 단위, 4 바이트 정수
  구성 데이터:     지정된 길이
  오프셋:          데이터베이스 내 데이터의 오프셋, 바이트 단위, 8 바이트 정수
  데이터 길이:        바이트 단위, 4 바이트 정수
  데이터:            지정된 길이
  완료 여부:         완료되었으면 1, 그렇지 않으면 0 (1 바이트)
```


### 응답

모든 응답은 26 바이트이며, 다음과 같습니다. 모든 값은 부호 없는 빅 엔디안입니다.

```dataspec
메시지 유형:   1 바이트
  소스:         ID, 4 바이트 정수
  목적지:    보통 실제 목적지 ID (참고사항 참조), 4 바이트 정수
  용어:           현재 용어, 8 바이트 정수
  다음 색인:     리더의 마지막 로그 색인 + 1로 초기화됨, 8 바이트 정수
  수락 여부:    수락되면 1, 그렇지 않으면 0 (참고사항 참조), 1 바이트
```


#### 참고사항

목적지 ID는 보통 이 메시지의 실제 목적지입니다.
그러나 AppendEntriesResponse, AddServerResponse, RemoveServerResponse의 경우
현재 리더의 ID입니다.

RequestVoteResponse에서는 수락 여부가 후보자(요청자)에 대한 투표일 경우 1,
그렇지 않을 경우 0입니다.


## 애플리케이션 레이어

각 서버는 주기적으로 Application 데이터를 로그에 ClientRequest로 게시합니다.
Application 데이터는 각 서버의 라우터 상태 및 Meta LS2 클러스터의 대상을 포함합니다.
서버들은 Meta LS2의 게시자와 내용을 결정하기 위해 공통 알고리즘을 사용합니다.
로그에서 "최고의" 최근 상태를 가진 서버가 Meta LS2의 게시자입니다.
Meta LS2의 게시자는 반드시 Raft 리더일 필요는 없습니다.


### 애플리케이션 데이터 내용

애플리케이션 내용은 간단함과 확장 가능성을 위해 UTF-8로 인코딩된 [JSON](https://json.org/)입니다.
전체 명세서는 TBD입니다.
목표는 Meta LS2를 게시할 "최고의" 라우터를 결정할 수 있는 데이터를 제공하고,
게시자가 Meta LS2의 대상에 가중치를 부여할 충분한 정보를 갖도록 하는 것입니다.
데이터는 라우터 및 Destination 통계를 포함할 것입니다.

데이터는 첫 릴리스에서 지원되지 않는 다른 서버의 건강에 대한 원격 감지 데이터를
옵션으로 포함할 수 있습니다.

데이터는 첫 릴리스에서 지원되지 않는 관리 클라이언트에 의해 게시된 구성 정보를
옵션으로 포함할 수 있습니다.

"이름: 값"이 나열된 경우, 이는 JSON 맵 키와 값을 명시합니다.
그렇지 않으면, 명세가 TBD입니다.


클러스터 데이터 (최상위 레벨):

- 클러스터: 클러스터 이름
- 날짜: 이 데이터의 날짜 (길게, epoch 이후 ms)
- ID: Raft ID (정수)

구성 데이터 (구성):

- 모든 구성 매개변수

MetaLS 게시 상태 (메타):

- 대상: 메탈의 대상, base64
- 마지막 게시된 LS: 있으면, 마지막 게시된 메탈의 base64 인코딩
- 마지막 게시 시간: ms 단위, 없으면 0
- 게시 구성: 게시자 구성 상태 off/on/auto
- 게시 중: 메탈 게시자 상태 boolean true/false

라우터 데이터 (라우터):

- 마지막 게시된 RI: 있으면, 마지막 게시된 라우터 정보의 base64 인코딩
- 업타임: ms 단위
- 작업 지연
- 탐색 터널
- 참여 터널
- 설정된 대역폭
- 현재 대역폭

Destination (대상):
목록

Destination 데이터:

- 대상: 대상, base64
- 업타임: ms 단위
- 설정된 터널 수
- 현재 터널 수
- 설정된 대역폭
- 현재 대역폭
- 설정된 연결 수
- 현재 연결 수
- 블랙리스트 데이터

원격 라우터 감지 데이터:

- 마지막 RI 버전
- LS 가져오기 시간
- 연결 테스트 데이터
- 가장 가까운 플러드필 프로필 데이터
  어제, 오늘, 내일의 기간 동안

원격 대상 감지 데이터:

- 마지막 LS 버전
- LS 가져오기 시간
- 연결 테스트 데이터
- 가장 가까운 플러드필 프로필 데이터
  어제, 오늘, 내일의 기간 동안

Meta LS 감지 데이터:

- 마지막 버전
- 가져오기 시간
- 가장 가까운 플러드필 프로필 데이터
  어제, 오늘, 내일의 기간 동안


## 관리 인터페이스

TBD, 아마도 별도의 제안서가 필요할 것입니다.
첫 릴리스에 필수는 아닙니다.

관리 인터페이스의 요구사항:

- 여러 마스터 대상, 즉 여러 가상 클러스터(farms)에 대한 지원
- 공유 클러스터 상태에 대한 포괄적인 보기 제공 - 모든 회원이 게시한 통계, 현재 리더가 누구인지 등
- 클러스터에서 참여자 또는 리더 제거 강제 기능
- MetaLS 강제 게시 가능 (현재 노드가 게시자일 경우)
- MetaLS에서 해시를 제외시키는 기능 (현재 노드가 게시자일 경우)
- 대량 배포를 위한 설정 가져오기/내보내기 기능


## 라우터 인터페이스

TBD, 아마도 별도의 제안서가 필요할 것입니다.
i2pcontrol은 첫 릴리스에 필요하지 않으며, 세부 변경사항은 별도의 제안서에 포함될 것입니다.

Garlic Farm에서 라우터 API에 대한 요구사항 (in-JVM java 또는 i2pcontrol)

- getLocalRouterStatus()
- getLocalLeafHash(Hash masterHash)
- getLocalLeafStatus(Hash leaf)
- getRemoteMeasuredStatus(Hash masterOrLeaf) // 아마도 MVP에는 포함되지 않음
- publishMetaLS(Hash masterHash, List<MetaLease> contents) // 또는 서명된 MetaLeaseSet? 누가 서명?
- stopPublishingMetaLS(Hash masterHash)
- 인증 TBD


## 정당화

Atomix는 너무 크고 우리가 I2P를 통해 프로토콜을 라우팅할 수 있도록 하는 커스터마이징을 허용하지 않습니다. 또한, 그 와이어 형식은 문서화되어 있지 않으며, Java 직렬화에 의존합니다.


## 비고


## 문제점

- 클라이언트가 알 수 없는 리더에 관해 알아내고 연결할 방법이 없습니다.
  팔로워가 AppendEntriesResponse의 로그 항목에 구성을 전송하는 것은 작은 변경이 될 것입니다.


## 마이그레이션

호환성 문제 없음.


## 참고 문헌

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
