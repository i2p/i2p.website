---
title: "주소록 구독 피드 명령어"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Closed"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
toc: true
---

## 노트
네트워크 배포 완료.
공식 명세는 [SPEC](/docs/specs/subscription/)를 참조하십시오.


## 개요

이 제안서는 주소 구독 피드에 명령어를 확장하여, 네임 서버가 호스트명 소유자로부터 엔트리 업데이트를 방송할 수 있게 하는 것입니다.
버전 0.9.26에 구현되었습니다.


## 동기

현재 hosts.txt 구독 서버는 hosts.txt 형식으로 데이터를 전송할 뿐입니다, 이는 다음과 같습니다:

  ```text
  example.i2p=b64destination
  ```

여기에는 몇 가지 문제가 있습니다:

- 호스트명 소유자는 그들의 호스트명과 관련된 대상(Destination)을 업데이트할 수 없습니다
  (예를 들어, 서명 키를 더 강력한 유형으로 업그레이드할 수 있도록).
- 호스트명 소유자는 임의로 호스트명을 포기할 수 없습니다; 그들은 해당 대상의 비공개 키를
  새로운 소유자에게 직접 제공해야 합니다.
- 서브도메인이 해당 기본 호스트명에 의해 제어되고 있음을 인증할 수 있는 방법이 없습니다;
  이는 현재 일부 네임 서버에 의해 개별적으로만 시행됩니다.


## 설계

이 제안서는 hosts.txt 형식에 여러 명령 행을 추가합니다. 이러한 명령을 통해 네임 서버는 여러 추가 기능을 제공하도록 서비스를 확장할 수 있습니다. 이 제안서를 구현한 클라이언트는 일반 구독 과정을 통해 이러한 기능을 청취할 수 있게 됩니다.

모든 명령 행은 해당 대상에서 서명해야 합니다. 이는 변경 사항이 호스트명 소유자의 요청에 의해서만 이루어지도록 보장합니다.


## 보안 영향

이 제안서는 익명성에 영향을 미치지 않습니다.

대상 키를 제어할 수 없는 위험이 증가할 수 있으며, 이를 얻은 사람이 관련 호스트명에 대해 변경할 수 있기 때문에 그렇습니다. 그러나 이는 누군가가 대상을 얻었을 때 호스트명을 가장하고 그 트래픽을 (부분적으로) 인수할 수 있는 현 상황과 다르지 않습니다. 증가된 위험은 또한 만약 대상이 손상되었다고 믿는 경우 호스트명 소유자에게 호스트명과 관련된 대상을 변경할 수 있는 능력을 제공함으로써 완충됩니다; 이는 현재 시스템에서는 불가능합니다.


## 명세

### 새로운 행 유형

이 제안서는 두 개의 새로운 행 유형을 추가합니다:

1. 추가 및 변경 명령어:

     ```text
     example.i2p=b64destination#!key1=val1#key2=val2 ...
     ```

2. 제거 명령어:

     ```text
     #!key1=val1#key2=val2 ...
     ```

#### 정렬
피드는 반드시 순서 대로이거나 완전하지는 않습니다. 예를 들어, 변경 명령이 추가 명령 앞에 있을 수 있으며, 추가 명령 없이 있을 수 있습니다.

키는 어느 순서로든 나올 수 있습니다. 중복 키는 허용되지 않습니다. 모든 키와 값은 대소문자를 구분합니다.


### 공통 키

모든 명령어에 요구됨:

sig
  서명 키를 사용한 B64 서명

두 번째 호스트명 및/또는 대상 참조:

oldname
  두 번째 호스트명 (새로운 것 또는 변경된 것)
olddest
  두 번째 b64 대상 (새로운 것 또는 변경된 것)
oldsig
  nolddest의 서명 키를 사용한 두 번째 b64 서명

다른 공통 키:

action
  명령어
name
  호스트명, example.i2p=b64dest로 앞서지 않은 경우만 존재
dest
  b64 대상, example.i2p=b64dest로 앞서지 않은 경우만 존재
date
  epoch 이후 초 단위
expires
  epoch 이후 초 단위


### 명령어

"Add" 명령어를 제외한 모든 명령어는 "action=command" 키/값을 포함해야 합니다.

이전 클라이언트와의 호환성을 위해 대부분의 명령어는 example.i2p=b64dest로 시작됩니다. 변경 사항의 경우 이는 항상 새로운 값입니다. 어떤 오래된 값도 키/값 섹션에 포함됩니다.

나열된 키는 필수입니다. 모든 명령어는 여기 정의되지 않은 추가적인 키/값 항목을 포함할 수 있습니다.

#### 호스트명 추가
example.i2p=b64dest로 시작
  예, 이는 새로운 호스트명과 대상입니다.
action
  포함되지 않음, 이는 묵시적입니다.
sig
  서명

예시:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### 호스트명 변경
example.i2p=b64dest로 시작
  예, 이는 새로운 호스트명과 오래된 대상입니다.
action
  changename
oldname
  교체될 오래된 호스트명
sig
  서명

예시:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### 대상 변경
example.i2p=b64dest로 시작
  예, 이는 오래된 호스트명과 새로운 대상입니다.
action
  changedest
olddest
  교체될 오래된 대상
oldsig
  olddest을 사용한 서명
sig
  서명

예시:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 호스트명 별칭 추가
example.i2p=b64dest로 시작
  예, 이는 새로운 (별칭) 호스트명과 오래된 대상입니다.
action
  addname
oldname
  오래된 호스트명
sig
  서명

예시:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### 대상 별칭 추가
(암호 업그레이드를 위해 사용됨)

example.i2p=b64dest로 시작
  예, 이는 오래된 호스트명과 새로운 (대체) 대상입니다.
action
  adddest
olddest
  오래된 대상
oldsig
  olddest을 사용한 서명
sig
  dest을 사용한 서명

예시:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 서브도메인 추가
subdomain.example.i2p=b64dest로 시작
  예, 이는 새로운 호스트 서브도메인명과 대상입니다.
action
  addsubdomain
oldname
  상위 레벨 호스트명 (example.i2p)
olddest
  상위 레벨 대상 (예: example.i2p)
oldsig
  olddest을 사용한 서명
sig
  dest을 사용한 서명

예시:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### 메타데이터 업데이트
example.i2p=b64dest로 시작
  예, 이는 오래된 호스트명과 대상입니다.
action
  update
sig
  서명

(업데이트된 키를 여기에 추가)

예시:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### 호스트명 제거
example.i2p=b64dest로 시작
  아니오, 옵션에서 지정됩니다
action
  remove
name
  호스트명
dest
  대상
sig
  서명

예시:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### 이 대상을 가진 모든 항목 제거
example.i2p=b64dest로 시작
  아니오, 옵션에서 지정됩니다
action
  removeall
name
  오래된 호스트명, 조황만 제공
dest
  오래된 대상, 이 대상을 가진 모든 항목 제거
sig
  서명

예시:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```


### 서명

모든 명령어는 "sig=b64signature" 서명 키/값을 포함해야 하며, 서명키를 사용하여 다른 데이터에 대한 서명이 될 것입니다.

오래된 대성과 새로운 대상을 포함하는 명령어의 경우, oldsig=b64signature가 있어야 하며, oldname, olddest, 또는 둘 중 하나 이상이 포함되어야 합니다.

추가 또는 변경 명령어에서는 검증을 위한 공개 키가 추가되거나 변경될 대상에 있습니다.

일부 추가 또는 편집 명령어에서는 추가 대상이 참조될 수도 있습니다. 예를 들어, 별칭 추가, 대상 또는 호스트명 변경 시. 이 경우, 두 번째 서명이 포함되어 있어야 하며, 둘 다 검증되어야 합니다. 두 번째 서명은 "내부" 서명이며 먼저 서명되고 검증됩니다("외부" 서명이 제외되고). 클라이언트는 추가적인 검증을 통해 변경을 수용하기 위한 조치를 취해야 합니다.

oldsig는 항상 "내부" 서명입니다. 'oldsig' 또는 'sig' 키가 없는 상태에서 서명하고 검증하세요. sig는 항상 "외부" 서명입니다. 'oldsig' 키는 있지만 'sig' 키는 없는 상태에서 서명하고 검증합니다.

#### 서명을 위한 입력
서명을 생성하거나 서명을 확인하기 위해 바이트 스트림을 생성하려면 다음과 같이 시리얼화하세요:

- "sig" 키를 제거합니다
- oldsig로 확인하는 경우 "oldsig" 키도 제거합니다
- 추가 또는 변경 명령어에 대해서만 example.i2p=b64dest를 출력합니다
- 키가 남아 있는 경우 "#!"를 출력합니다
- UTF-8 키로 옵션을 정렬하여 중복 키가 있는 경우 실패합니다
- 각 키/값에 대해 key=value를 출력하고 마지막 키/값이 아닌 경우 '#'를 추가합니다

주석:

- 줄 바꿈을 출력하지 마세요
- 출력 인코딩은 UTF-8입니다
- 모든 대상 및 서명 인코딩은 I2P 알파벳을 사용하여 Base 64입니다
- 키와 값은 대소문자를 구분합니다
- 호스트명은 소문자여야 합니다


## 호환성

hosts.txt 형식에 있는 모든 새로운 행은 주석 문자로 구현되어 있어, 모든 이전 I2P 버전에서는 새로운 명령어를 주석으로 해석합니다.

I2P 라우터가 새로운 명세로 업데이트되면, 이전 주석을 다시 해석하지 않지만, 구독 피드를 통해 이후의 새로운 명령어를 듣기 시작할 것입니다. 따라서 이름 서버는 명령 항목을 지속적으로 유지하거나, 라우터가 모든 이전 명령어를 가져올 수 있도록 etag 지원을 활성화하는 것이 중요합니다.


