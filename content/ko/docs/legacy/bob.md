---
title: "BOB - Basic Open Bridge"
description: "목적지 관리를 위한 더 이상 사용되지 않는 API"
slug: "bob"
aliases:
  - "/ko/docs/api/bob"
  - "/ko/docs/api/bob/"
  - "/ko/bob"
  - "/ko/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## 경고 - 더 이상 사용되지 않음

새로운 애플리케이션에서는 사용하지 마세요. 여기에 명시된 BOB는 DSA-SHA1 서명 유형만 지원합니다. BOB는 새로운 서명 유형이나 기타 고급 기능을 지원하도록 확장되지 않을 예정입니다. 새로운 애플리케이션은 [SAM V3](/docs/api/samv3)을 사용해야 합니다.

BOB 지원은 릴리스 1.7.0 (2022-02)부터 Java I2P 새로운 설치에서 제거되었습니다. 버전 1.6.1 이하로 원래 설치된 Java I2P에서는 업데이트 후에도 여전히 작동하지만, 지원되지 않으며 언제든지 중단될 수 있습니다. BOB는 2025-05 현재 i2pd에서 여전히 지원되지만, 위에서 언급한 이유로 애플리케이션들은 여전히 SAMv3로 마이그레이션해야 합니다. 여기에 문서화된 API에 대한 i2pd가 지원하는 확장 사항은 [i2pd 문서](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/)를 참조하세요.

현재 BOB의 좋은 아이디어 대부분이 SAMv3에 통합되었으며, SAMv3는 더 많은 기능과 실제 사용 사례를 제공합니다. BOB는 일부 설치에서 여전히 작동할 수 있지만(위 참조), SAMv3에서 사용할 수 있는 고급 기능들을 지원받지 못하며 i2pd를 제외하고는 본질적으로 지원되지 않습니다.

## BOB API용 언어 라이브러리

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## 개요

`KEYS` = 공개키+개인키 키 쌍, BASE64 형식

`KEY` = 공개 키, BASE64 형식

`ERROR`는 암시된 바와 같이 `"ERROR "+DESCRIPTION+"\n"` 메시지를 반환하며, 여기서 `DESCRIPTION`은 무엇이 잘못되었는지를 나타냅니다.

`OK`는 `"OK"`를 반환하며, 반환할 데이터가 있는 경우 같은 줄에 표시됩니다. `OK`는 명령이 완료되었음을 의미합니다.

`DATA` 라인에는 요청한 정보가 포함되어 있습니다. 요청당 여러 개의 `DATA` 라인이 있을 수 있습니다.

**참고:** help 명령은 규칙에 예외가 있는 유일한 명령입니다... 실제로 아무것도 반환하지 않을 수 있습니다! 이는 의도적인 것으로, help는 애플리케이션 명령이 아닌 사람을 위한 명령이기 때문입니다.

## 연결 및 버전

모든 BOB 상태 출력은 라인별로 이루어집니다. 라인은 시스템에 따라 \\n 또는 \\r\\n으로 종료될 수 있습니다. 연결 시 BOB은 두 줄을 출력합니다:

```
BOB version
OK
```
현재 버전은: 00.00.10

이전 버전에서는 대문자 16진수 숫자를 사용했으며 I2P 버전 관리 표준을 준수하지 않았습니다. 후속 버전에서는 0-9 숫자만 사용하는 것이 권장됩니다.

### 버전 히스토리

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## 명령어

**주의사항:** 명령어에 대한 **최신** 세부사항은 내장된 도움말 명령어를 사용하시기 바랍니다. localhost 2827에 telnet으로 접속하여 help를 입력하면 각 명령어에 대한 전체 문서를 확인할 수 있습니다.

명령어는 절대 사용이 중단되거나 변경되지 않지만, 새로운 명령어가 때때로 추가됩니다.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
설정이 완료되면 모든 TCP 소켓이 필요에 따라 블록될 수 있고 실제로 블록되며, 명령 채널로 추가 메시지를 주고받을 필요가 없습니다. 이를 통해 router가 스트림 속도를 조절할 수 있어 SAM처럼 OOM으로 폭발하지 않습니다. SAM은 많은 스트림을 하나의 소켓으로 밀어넣거나 빼내려다 막히면서 문제가 생기는데, 이는 연결이 많을 때 확장성이 떨어집니다!

이 특정 인터페이스의 또 다른 장점은 이를 인터페이스하기 위한 코드 작성이 SAM보다 훨씬 쉽다는 것입니다. 설정 후에는 다른 처리가 필요하지 않습니다. 구성이 너무 간단해서 nc (netcat)와 같은 매우 단순한 도구로도 어떤 애플리케이션을 가리킬 수 있습니다. 여기서 중요한 점은 애플리케이션의 작동 시간과 중단 시간을 스케줄링할 수 있고, 이를 위해 애플리케이션을 수정하거나 심지어 애플리케이션을 중단할 필요도 없다는 것입니다. 대신 말 그대로 destination을 "연결 해제"하고 다시 "연결"할 수 있습니다. 브리지를 다시 가동할 때 동일한 IP/포트 주소와 destination 키가 사용되는 한, 일반적인 TCP 애플리케이션은 신경 쓰지 않고 알아차리지도 못할 것입니다. 단순히 속게 될 뿐입니다 -- destination에 도달할 수 없고 아무것도 들어오지 않는다고 말이죠.

## 예시

다음 예제에서는 두 개의 destination을 가진 매우 간단한 로컬 루프백 연결을 설정하겠습니다. Destination "mouth"는 INET 슈퍼서버 데몬의 CHARGEN 서비스가 될 것입니다. Destination "ear"는 텔넷으로 접속할 수 있는 로컬 포트가 되며, 여기서 예쁜 ASCII 테스트 문자들이 쏟아져 나오는 것을 볼 수 있습니다.

### 세션 대화 예제

간단한 telnet 127.0.0.1 2827이 작동합니다.

- A = 애플리케이션
- C = BOB의 명령 응답.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**위의 목적지 키를 기록해 두세요. 귀하의 키는 다를 것입니다!**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
이 시점에서는 오류가 없었으며, "mouth"라는 별명을 가진 destination이 설정되었습니다. 제공된 destination에 연결하면, 실제로는 `19/TCP`의 `CHARGEN` 서비스에 연결됩니다.

이제 나머지 절반을 진행하여 실제로 이 목적지에 연결할 수 있도록 하겠습니다.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
이제 우리가 해야 할 일은 127.0.0.1의 포트 37337로 telnet 접속하여, 연결하고자 하는 destination key나 주소록의 호스트 주소를 보내는 것입니다. 이 경우 "mouth"에 연결하려고 하니, key를 붙여넣기만 하면 연결됩니다.

**참고:** 명령 채널의 "quit" 명령은 SAM과 달리 tunnel을 연결 해제하지 않습니다.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
이런 출력이 몇 번 나타난 후, `Control-]`를 누르세요

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
다음과 같은 일이 일어났습니다...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
I2P SITES에도 연결할 수 있습니다!

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
꽤 멋지지 않나요? 원한다면 다른 잘 알려진 I2P SITES를 시도해보거나, 존재하지 않는 사이트들도 시도해보면서 다양한 상황에서 어떤 종류의 출력이 나오는지 감을 잡아보세요. 대부분의 경우, 오류 메시지들은 무시하는 것이 좋습니다. 이러한 메시지들은 애플리케이션에게는 의미가 없으며, 오직 사람이 디버깅할 때만 표시되는 것입니다.

### 정리하기

이제 모든 작업이 완료되었으므로 대상을 종료하겠습니다.

먼저 어떤 destination 닉네임들이 있는지 살펴보겠습니다.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
좋습니다, 여기 있네요. 먼저 "mouth"를 제거해봅시다.

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
이제 "ear"를 제거하려면, 이것은 너무 빨리 타이핑할 때 일어나는 일이며, 일반적인 ERROR 메시지가 어떻게 생겼는지 보여줍니다.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## 조용한 모드

브리지의 수신 측 예제는 매우 간단하기 때문에 보여드리지 않겠습니다. 두 가지 가능한 설정이 있으며, "quiet" 명령으로 전환할 수 있습니다.

기본값은 조용하지 않으며(NOT quiet), 수신 소켓으로 들어오는 첫 번째 데이터는 연결을 만드는 destination입니다. 이는 BASE64 주소 뒤에 개행 문자가 따라오는 한 줄로 구성됩니다. 그 이후의 모든 것은 애플리케이션이 실제로 소비할 데이터입니다.

조용한 모드에서는 일반적인 인터넷 연결로 생각하면 됩니다. 추가 데이터가 전혀 들어오지 않습니다. 마치 일반 인터넷에 평범하게 연결된 것과 같습니다. 이 모드는 router 콘솔 터널 설정 페이지에서 사용할 수 있는 것과 유사한 형태의 투명성을 허용하므로, 예를 들어 BOB를 사용하여 destination을 웹 서버에 연결할 때 웹 서버를 전혀 수정할 필요가 없습니다.

## BOB의 장점

이를 위해 BOB을 사용하는 장점은 앞서 논의한 바와 같습니다. 애플리케이션의 임의 가동 시간을 예약하거나, 다른 머신으로 리디렉션하는 등의 작업이 가능합니다. 이것의 한 가지 용도는 router에서 destination까지의 연결 상태 추정을 혼란시키려는 경우일 수 있습니다. 완전히 다른 프로세스로 destination을 중지하고 시작하여 서비스에 임의의 연결/해제 시간을 만들 수 있습니다. 이렇게 하면 해당 서비스에 연결하는 기능만 중지하게 되고, 서비스를 종료하고 다시 시작하는 번거로움을 피할 수 있습니다. 업데이트를 수행하는 동안 LAN의 다른 머신으로 리디렉션하거나, 실행 중인 상황에 따라 백업 머신 세트를 가리키는 등 다양한 활용이 가능합니다. BOB으로 할 수 있는 일은 오직 여러분의 상상력에 의해서만 제한됩니다.
