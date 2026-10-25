---
title: "SAM V1 명세서"
description: "레거시 Simple Anonymous Messaging 프로토콜 버전 1 (더 이상 사용되지 않음)"
slug: "sam"
aliases:
  - "/ko/docs/api/sam"
  - "/ko/docs/api/sam/"
  - "/ko/sam"
  - "/ko/sam/"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
---

## 경고 - 사용 중단됨 - 지원되지 않음 - [SAMv3](/docs/api/samv3) 사용

아래에는 I2P와 상호 작용하기 위한 간단한 클라이언트 프로토콜의 버전 1이 명시되어 있습니다. 더 새로운 대안들: [SAM V2](/docs/api/samv2), [SAM V3](/docs/api/samv3), [BOB](/docs/api/bob).

## SAMv1 API용 언어 라이브러리

- C
- C#
- Perl
- Python

라이브러리들은 I2P 소스 저장소에 있습니다.

### I2P 0.9.14 변경사항

보고된 버전은 "1.0"으로 유지됩니다.

- DEST GENERATE은 이제 SIGNATURE_TYPE 매개변수를 지원합니다.
- HELLO VERSION의 MIN 매개변수는 이제 선택사항입니다.
- HELLO VERSION의 MIN과 MAX 매개변수는 이제 "3"과 같은 한 자리 버전을 지원합니다.

## 버전 1 프로토콜

클라이언트 애플리케이션은 SAM bridge와 통신하며, SAM bridge는 모든 I2P 기능을 처리합니다 (가상 스트림을 위한 streaming lib 사용, 또는 비동기 메시지를 위한 I2CP 직접 사용).

모든 클라이언트<-->SAM bridge 통신은 단일 TCP 소켓을 통해 암호화되지 않고 인증되지 않습니다. SAM bridge에 대한 접근은 방화벽이나 다른 수단을 통해 보호되어야 합니다 (bridge에서 연결을 허용하는 IP에 대한 ACL을 가질 수도 있습니다).

이러한 모든 SAM 메시지는 일반 ASCII로 한 줄에 전송되며, 개행 문자(\\n)로 종료됩니다. 아래에 표시된 형식은 단순히 가독성을 위한 것이며, 각 메시지의 처음 두 단어는 특정 순서를 유지해야 하지만, key=value 쌍의 순서는 변경될 수 있습니다(예: "ONE TWO A=B C=D" 또는 "ONE TWO C=D A=B" 모두 완전히 유효한 구조입니다). 또한 프로토콜은 대소문자를 구분합니다.

SAM 메시지는 UTF-8로 해석됩니다. Key=value 쌍은 단일 공백으로 구분되어야 합니다. 값에 공백이 포함된 경우 큰따옴표로 묶을 수 있습니다. 예: key="long value text". 이스케이프 메커니즘은 없습니다.

통신은 세 가지 구별되는 형태를 가질 수 있습니다:

- [가상 스트림](/docs/api/streaming)
- [응답 가능한 데이터그램](/docs/specs/datagrams#repliable) (FROM 필드가 있는 메시지)
- [익명 데이터그램](/docs/specs/datagrams#raw) (원시 익명 메시지)

## SAM 연결 핸드셰이크

클라이언트와 브리지가 프로토콜 버전에 합의하기 전까지는 SAM 통신이 발생할 수 없으며, 이는 클라이언트가 HELLO를 보내고 브리지가 HELLO REPLY를 보내는 방식으로 수행됩니다:

```
HELLO VERSION MIN=$min MAX=$max
```
그리고

```
HELLO REPLY RESULT=$result VERSION=1.0
```
I2P 0.9.14부터 MIN 매개변수는 선택사항입니다. MAX 매개변수는 반드시 제공되어야 하며 버전 1을 사용하려면 "1" 이상이고 "2" 미만이어야 합니다.

RESULT 값은 다음 중 하나일 수 있습니다:

- `OK`
- `NOVERSION`

## SAM 세션

SAM 세션은 클라이언트가 SAM bridge에 소켓을 열고, 핸드셰이크를 수행하고, SESSION CREATE 메시지를 전송함으로써 생성되며, 소켓이 연결 해제되면 세션이 종료됩니다.

각 I2P Destination은 한 번에 하나의 SAM 세션에서만 사용할 수 있으며, 이러한 형태 중 하나만 사용할 수 있습니다 (다른 형태를 통해 수신된 메시지는 삭제됩니다).

클라이언트가 브리지로 보내는 SESSION CREATE 메시지는 다음과 같습니다:

```
SESSION CREATE
        STYLE={STREAM,DATAGRAM,RAW}
        DESTINATION={$name,TRANSIENT}
        [DIRECTION={BOTH,RECEIVE,CREATE}]
        [option=value]*
```
DESTINATION은 메시지/스트림을 송수신할 때 사용할 destination을 지정합니다. $name이 주어지면, SAM bridge는 자체 로컬 저장소(sam.keys 파일)에서 연결된 destination(및 개인 키)을 찾습니다. 해당 이름과 일치하는 연결이 존재하지 않으면 새로운 것을 생성합니다. destination이 TRANSIENT로 지정되면 항상 새로운 것을 생성합니다.

DESTINATION은 식별자이며, Base 64로 인코딩된 데이터가 *아님*을 유의하세요. Destination을 지정하려면 [SAM V3](/docs/api/samv3)를 사용해야 합니다.

DIRECTION은 STREAM 세션에서만 지정할 수 있으며, 클라이언트가 스트림을 생성하거나 수신하거나 둘 다 할 것인지를 브릿지에 알려줍니다. 이것이 지정되지 않으면 BOTH로 간주됩니다. DIRECTION=RECEIVE일 때 아웃바운드 스트림을 생성하려고 시도하면 오류가 발생해야 하며, DIRECTION=CREATE일 때 인바운드 스트림은 무시됩니다.

제공된 추가 옵션들은 SAM bridge에서 해석되지 않는 경우 I2P 세션 구성에 전달되어야 합니다 (예: "tunnels.depthInbound=0"). 이러한 옵션들은 아래에 문서화되어 있습니다.

SAM bridge 자체는 I2P를 통해 어떤 router와 통신해야 하는지 이미 구성되어 있어야 합니다 (필요한 경우 i2cp.tcp.host=localhost 및 i2cp.tcp.port=7654와 같은 재정의를 제공하는 방법이 있을 수 있습니다).

세션 생성 메시지를 받은 후, SAM bridge는 다음과 같이 세션 상태 메시지로 응답합니다:

```
SESSION STATUS
        RESULT=$result
        DESTINATION={$name,TRANSIENT}
        [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

- `OK`
- `DUPLICATED_DEST`
- `I2P_ERROR`
- `INVALID_KEY`

OK가 아닌 경우, MESSAGE는 세션을 생성할 수 없는 이유에 대한 사람이 읽을 수 있는 정보를 포함해야 합니다.

$name이 찾을 수 없고 임시 목적지가 대신 생성되더라도 경고가 표시되지 않는다는 점에 유의하세요. 실제 임시 base 64 목적지는 응답에서 출력되지 않으며, SESSION CREATE에서 제공된 $name 또는 TRANSIENT가 출력됩니다. 이러한 기능이 필요하다면 [SAM V3](/docs/api/samv3)을 사용해야 합니다.

## SAM 가상 스트림

가상 스트림은 신뢰성 있게 순서대로 전송되는 것이 보장되며, 실패 및 성공 알림이 가능한 즉시 제공됩니다.

STYLE=STREAM으로 세션을 설정한 후, 클라이언트와 SAM bridge 모두 아래 나열된 대로 스트림을 관리하기 위해 다양한 메시지를 비동기적으로 주고받을 수 있습니다:

```
STREAM CONNECT
       ID=$id
       DESTINATION=$destination
```
이것은 로컬 목적지에서 지정된 피어로의 새로운 가상 연결을 설정하고, 세션 범위의 고유 ID로 표시합니다. 고유 ID는 1부터 (2^31-1)까지의 ASCII base 10 정수입니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이며, 서명 타입에 따라 516개 이상의 base 64 문자(바이너리로는 387바이트 이상)입니다.

SAM bridge는 스트림 상태 메시지로 이에 응답해야 합니다:

```
STREAM STATUS
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `INVALID_KEY`
- `TIMEOUT`

RESULT가 OK이면, 지정된 destination이 활성화되어 있고 연결을 승인했다는 의미입니다. 연결이 불가능한 경우(타임아웃 등), RESULT에는 적절한 오류 값이 포함됩니다(선택적으로 사람이 읽을 수 있는 MESSAGE가 함께 제공됨).

수신 측에서 SAM bridge는 클라이언트에게 다음과 같이 알립니다:

```
STREAM CONNECTED
       DESTINATION=$destination
       ID=$id
```
이는 주어진 destination이 클라이언트와 가상 연결을 생성했음을 알려줍니다. 다음 데이터 스트림은 주어진 고유 ID로 표시되며, 이 ID는 -1부터 -(2^31-1)까지의 ASCII base 10 정수입니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64로, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리로는 387바이트 이상)입니다.

클라이언트가 가상 연결에서 데이터를 전송하려고 할 때, 다음과 같이 수행합니다:

```
STREAM SEND
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
이것은 가상 연결을 통해 peer에게 전송되는 버퍼에 지정된 데이터를 추가합니다. 전송 크기 $numBytes는 개행 문자 후에 포함되는 8비트 바이트 수로, 1부터 32768(32KB)까지 가능합니다.

그러면 SAM bridge는 메시지를 가능한 한 빠르고 효율적으로 전달하기 위해 최선을 다할 것이며, 경우에 따라 여러 SEND 메시지를 함께 버퍼링할 수도 있습니다. 데이터 전달 중 오류가 발생하거나 원격 측에서 연결을 닫으면, SAM bridge는 클라이언트에게 다음과 같이 알립니다:

```
STREAM CLOSED
       RESULT=$result
       ID=$id
       [MESSAGE=...]
```
RESULT 값은 다음 중 하나일 수 있습니다:

- `OK`
- `CANT_REACH_PEER`
- `I2P_ERROR`
- `PEER_NOT_FOUND`
- `TIMEOUT`

연결이 다른 peer에 의해 정상적으로 종료된 경우, $result는 OK로 설정됩니다. $result가 OK가 아닌 경우, MESSAGE는 "peer unreachable" 등과 같은 설명 메시지를 전달할 수 있습니다. 클라이언트가 연결을 종료하고자 할 때마다, SAM bridge에 close 메시지를 보냅니다:

```
STREAM CLOSE
       ID=$id
```
그러면 bridge는 필요한 것을 정리하고 해당 ID를 폐기합니다 - 더 이상 해당 ID로 메시지를 보내거나 받을 수 없습니다.

통신의 다른 쪽에서, 피어가 일부 데이터를 전송했고 클라이언트가 이를 사용할 수 있을 때마다, SAM 브리지는 즉시 이를 전달합니다:

```
STREAM RECEIVED
       ID=$id
       SIZE=$numBytes\n[$numBytes of data]
```
모든 스트림은 SAM bridge와 클라이언트 간의 연결이 끊어지면 암묵적으로 닫힙니다.

## SAM 응답 가능한 데이터그램

I2P는 본질적으로 FROM 주소를 포함하지 않지만, 사용의 편의를 위해 응답 가능한 데이터그램이라는 추가 계층이 제공됩니다. 이는 FROM 주소를 포함하는 최대 31744바이트의 순서가 없고 신뢰할 수 없는 메시지입니다(헤더 자료를 위해 최대 1KB를 남겨둠). 이 FROM 주소는 SAM에 의해 내부적으로 인증되며(목적지의 서명 키를 사용하여 소스를 확인), 재생 공격 방지 기능을 포함합니다.

최소 크기는 1입니다. 최상의 전달 신뢰성을 위해서는 약 11KB의 최대 크기를 권장합니다.

STYLE=DATAGRAM으로 SAM 세션을 설정한 후, 클라이언트는 SAM bridge에 다음을 전송할 수 있습니다:

```
DATAGRAM SEND
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
데이터그램이 도착하면, 브리지는 다음을 통해 클라이언트에게 전달합니다:

```
DATAGRAM RECEIVED
         DESTINATION=$destination
         SIZE=$numBytes\n[$numBytes of data]
```
$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이며, 서명 타입에 따라 516개 이상의 base 64 문자(바이너리로 387바이트 이상)입니다.

SAM bridge는 클라이언트에게 인증 헤더나 기타 필드를 노출하지 않으며, 오직 발신자가 제공한 데이터만을 전달합니다. 이는 세션이 종료될 때까지 (클라이언트가 연결을 끊음으로써) 계속됩니다.

## SAM 익명 데이터그램

I2P의 대역폭을 최대한 활용하여, SAM은 클라이언트가 익명 데이터그램을 송수신할 수 있도록 하며, 인증 및 응답 정보는 클라이언트 자체에서 처리하도록 합니다. 이러한 데이터그램은 신뢰할 수 없고 순서가 보장되지 않으며, 최대 32768바이트까지 가능합니다.

최소 크기는 1입니다. 최적의 전송 신뢰성을 위해 권장되는 최대 크기는 약 11 KB입니다.

STYLE=RAW로 SAM 세션을 설정한 후, 클라이언트는 SAM bridge에 다음을 전송할 수 있습니다:

```
RAW SEND
    DESTINATION=$destination
    SIZE=$numBytes\n[$numBytes of data]
```
$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이며, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리로 387바이트 이상)입니다.

원시 데이터그램이 도착하면, 브리지는 다음을 통해 클라이언트에게 전달합니다:

```
RAW RECEIVED
    SIZE=$numBytes\n[$numBytes of data]
```
## SAM 유틸리티 기능

다음 메시지는 클라이언트가 이름 해석을 위해 SAM bridge에 쿼리하는 데 사용할 수 있습니다:

```
NAMING LOOKUP
       NAME=$name
```
이에 대한 답변은

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE=$message]
```
RESULT 값은 다음 중 하나일 수 있습니다:

- `OK`
- `INVALID_KEY`
- `KEY_NOT_FOUND`

NAME=ME인 경우, 응답에는 현재 세션에서 사용되는 destination이 포함됩니다 (TRANSIENT destination을 사용하는 경우 유용함). $result가 OK가 아닌 경우, MESSAGE에는 "bad format" 등과 같은 설명 메시지가 포함될 수 있습니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64이며, 서명 유형에 따라 516개 이상의 base 64 문자(바이너리로 387바이트 이상)입니다.

다음 메시지를 사용하여 공개 및 개인 base64 키를 생성할 수 있습니다:

```
DEST GENERATE
```
다음과 같이 응답됩니다

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
I2P 0.9.14부터 선택적 매개변수 SIGNATURE_TYPE이 지원됩니다. SIGNATURE_TYPE 값은 [Key Certificates](/docs/specs/common-structures#type_Certificate)에서 지원하는 임의의 이름(예: ECDSA_SHA256_P256, 대소문자 구분 없음) 또는 숫자(예: 1)일 수 있습니다. 기본값은 DSA_SHA1입니다.

$destination은 [Destination](/docs/specs/common-structures#type_Destination)의 base 64 형태로, 서명 타입에 따라 516개 이상의 base 64 문자(바이너리로는 387바이트 이상)입니다.

$privkey는 [Destination](/docs/specs/common-structures#type_Destination) 다음에 [Private Key](/docs/specs/common-structures#type_PrivateKey), 그 다음에 [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)를 연결한 것의 base 64 인코딩으로, 서명 타입에 따라 884개 이상의 base 64 문자(바이너리로 663바이트 이상)입니다.

## RESULT 값들

다음은 RESULT 필드가 가질 수 있는 값들과 그 의미입니다:

| 값 | 의미 |
|-------|---------|
| `OK` | 작업이 성공적으로 완료됨 |
| `CANT_REACH_PEER` | 피어가 존재하지만 연결할 수 없음 |
| `DUPLICATED_DEST` | 지정된 Destination이 이미 사용 중임 |
| `I2P_ERROR` | 일반적인 I2P 오류 (예: I2CP 연결 끊김 등) |
| `INVALID_KEY` | 지정된 키가 유효하지 않음 (잘못된 형식 등) |
| `KEY_NOT_FOUND` | 네이밍 시스템이 주어진 이름을 해결할 수 없음 |
| `PEER_NOT_FOUND` | 네트워크에서 피어를 찾을 수 없음 |
| `TIMEOUT` | 이벤트를 기다리는 중 타임아웃 (예: 피어 응답) |
## Tunnel, I2CP, 그리고 Streaming 옵션

이러한 옵션들은 SAM SESSION CREATE 라인의 끝에 name=value 쌍으로 전달될 수 있습니다.

모든 세션은 [터널 길이와 같은 I2CP 옵션](/docs/protocol/i2cp#options)을 포함할 수 있습니다. STREAM 세션은 [Streaming lib 옵션](/docs/api/streaming#options)을 포함할 수 있습니다. 옵션 이름과 기본값은 해당 참조 문서를 확인하세요.

## Base 64 참고사항

Base 64 인코딩은 I2P 표준 Base 64 알파벳 "A-Z, a-z, 0-9, -, ~"을 사용해야 합니다.

## 클라이언트 라이브러리 구현

클라이언트 라이브러리는 C, C++, C#, Perl, Python용으로 제공됩니다. 이들은 I2P 소스 패키지의 apps/sam/ 디렉토리에 있습니다.

## 기본 SAM 설정

기본 SAM 포트는 7656입니다. SAM은 I2P Router에서 기본적으로 활성화되지 않습니다. router console의 클라이언트 구성 페이지나 clients.config 파일에서 수동으로 시작하거나 자동 시작하도록 구성해야 합니다.
