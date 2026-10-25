---
title: "주소록 구독 피드 명령어"
description: "호스트명 소유자로부터 항목 업데이트를 name server가 브로드캐스트할 수 있도록 하는 명령으로 주소 구독 피드를 확장하기 위한 사양."
slug: "subscription"
aliases:
  - "/ko/docs/specs/subscription-spec"
  - "/ko/docs/specs/subscription-spec/"
category: "형식"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## 개요

이 사양은 호스트명 소유자로부터 항목 업데이트를 브로드캐스트할 수 있도록 네임 서버를 활성화하기 위해 주소 구독 피드를 명령어로 확장합니다. 0.9.26에서 구현되었으며, 원래 제안서 112에서 제안되었습니다.

## 동기

이전에는 hosts.txt 구독 서버가 다음과 같은 hosts.txt 형식으로 데이터를 전송했습니다:

```
example.i2p=b64destination
```
이것에는 몇 가지 문제가 있습니다:

- 호스트네임 소유자는 자신의 호스트네임과 연관된 Destination을 업데이트할 수 없습니다 (예: 서명 키를 더 강력한 유형으로 업그레이드하기 위해).
- 호스트네임 소유자는 자신의 호스트네임을 임의로 포기할 수 없습니다; 해당 Destination 개인 키를 새로운 소유자에게 직접 전달해야 합니다.
- 서브도메인이 해당 기본 호스트네임에 의해 제어되는지 인증할 방법이 없습니다; 이는 현재 일부 네임 서버에서만 개별적으로 시행되고 있습니다.

## 설계

이 명세는 hosts.txt 형식에 여러 명령줄을 추가합니다. 이러한 명령을 통해 네임 서버는 서비스를 확장하여 다양한 추가 기능을 제공할 수 있습니다. 이 명세를 구현하는 클라이언트는 일반적인 구독 프로세스를 통해 이러한 기능을 수신할 수 있습니다.

모든 명령줄은 해당하는 Destination에 의해 서명되어야 합니다. 이는 호스트명 소유자의 요청에 의해서만 변경이 이루어지도록 보장합니다.

## 보안상의 영향

이 명세서는 익명성에 영향을 주지 않습니다.

Destination 키의 제어권을 잃을 위험이 증가하는데, 이는 누군가 그 키를 획득하면 이러한 명령을 사용하여 연관된 호스트명에 변경을 가할 수 있기 때문입니다. 하지만 이는 현재 상황보다 더 큰 문제가 되지는 않습니다. 현재도 누군가 Destination을 획득하면 호스트명을 위장하고 (부분적으로) 해당 트래픽을 장악할 수 있기 때문입니다. 증가된 위험은 호스트명 보유자가 Destination이 침해되었다고 판단할 경우 호스트명과 연관된 Destination을 변경할 수 있는 능력을 제공함으로써 균형을 이룹니다. 이는 현재 시스템으로는 불가능한 기능입니다.

## 사양

### 새로운 라인 유형

두 가지 새로운 유형의 라인이 있습니다:

1. Add 및 Change 명령어:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. 명령어 제거:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### 순서

피드는 반드시 순서대로 정렬되어 있거나 완전할 필요가 없습니다. 예를 들어, change 명령이 add 명령보다 앞 줄에 있거나, add 명령 없이 존재할 수 있습니다.

키는 어떤 순서로든 배치될 수 있습니다. 중복된 키는 허용되지 않습니다. 모든 키와 값은 대소문자를 구분합니다.

### 공통 키

모든 명령어에 필수:

**sig** : destination의 서명 키를 사용한 B64 서명

두 번째 호스트명 및/또는 목적지에 대한 참조:

**oldname** : 두 번째 호스트명 (신규 또는 변경됨)

**olddest** : 두 번째 b64 destination (새롭거나 변경된)

**oldsig** : olddest의 서명 키를 사용한 두 번째 b64 서명

기타 일반적인 키:

**action** : 명령어

**name** : 호스트명, `example.i2p=b64dest`가 앞에 없을 때만 존재

**dest** : b64 destination, `example.i2p=b64dest`가 앞에 오지 않은 경우에만 존재

**date** : 에포크(epoch) 이후의 초 단위

**expires** : 에포크(epoch) 이후의 초 단위

### 명령어

"Add" 명령을 제외한 모든 명령은 `action=command` 키/값을 포함해야 합니다.

구버전 클라이언트와의 호환성을 위해, 아래에 명시된 바와 같이 대부분의 명령어는 `example.i2p=b64dest` 형식으로 시작됩니다. 변경사항의 경우, 이는 항상 새로운 값입니다. 기존 값들은 key/value 섹션에 포함됩니다.

나열된 키는 필수입니다. 모든 명령은 여기서 정의되지 않은 추가 키/값 항목을 포함할 수 있습니다.

#### 호스트명 추가

**example.i2p=b64dest가 앞에 있음** : 예, 이것이 새로운 호스트 이름과 목적지입니다.

**action** : 포함되지 않음, 암시적으로 처리됩니다.

**sig** : 서명

예제:

```
example.i2p=b64dest#!sig=b64sig
```
#### 호스트명 변경

**example.i2p=b64dest가 앞에 있음** : 예, 이것은 새로운 호스트 이름과 기존 destination입니다.

**action** : changename

**oldname** : 교체될 기존 호스트명

**sig** : 서명

예시:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### 목적지 변경

**example.i2p=b64dest가 앞에 있음** : 예, 이것은 이전 호스트 이름과 새로운 destination입니다.

**action** : changedest

**olddest** : 교체될 기존 dest

**oldsig** : olddest를 사용한 서명

**sig** : 서명

예시:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 호스트명 별칭 추가

**example.i2p=b64dest가 앞에 있음** : 예, 이것은 새로운 (별칭) 호스트 이름과 이전 목적지입니다.

**action** : addname

**oldname** : 기존 호스트명

**sig** : 서명

예시:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Destination 별칭 추가

(암호화 업그레이드에 사용됨)

**example.i2p=b64dest가 앞에 있음** : 예, 이것은 이전 호스트 이름과 새로운 (대체) destination입니다.

**action** : adddest

**olddest** : 이전 dest

**oldsig** : olddest를 사용한 서명

**sig** : dest를 사용한 서명

예제:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 서브도메인 추가

**subdomain.example.i2p=b64dest로 시작**: 예, 이것은 새로운 호스트 하위 도메인 이름과 destination입니다.

**action** : addsubdomain

**oldname** : 상위 레벨 호스트명 (example.i2p)

**olddest** : 상위 레벨 대상 (예: example.i2p)

**oldsig** : olddest를 사용한 서명

**sig** : dest를 사용한 서명

예시:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 메타데이터 업데이트

**example.i2p=b64dest가 앞에 있음** : 예, 이것은 이전 호스트 이름과 목적지입니다.

**action** : update

**sig** : 서명

(여기에 업데이트된 키를 추가하세요)

예시:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### 호스트명 제거

**example.i2p=b64dest로 시작** : 아니오, 이것들은 옵션에서 지정됩니다

**action** : remove

**name** : 호스트명

**dest** : 목적지

**sig** : 서명

예시:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### 이 목적지로 모두 제거

**example.i2p=b64dest로 시작됨** : 아니오, 이것들은 옵션에서 지정됩니다

**action** : removeall

**name** : 이전 호스트명, 참고용으로만 사용

**dest** : 이전 dest, 이 dest를 가진 모든 항목이 제거됩니다

**sig** : 서명

예시:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### 서명

모든 명령에는 서명 키/값 `sig=b64signature`가 포함되어야 하며, 여기서 서명은 destination signing key를 사용하여 다른 데이터에 대한 서명입니다.

이전 목적지와 새로운 목적지를 포함하는 명령의 경우, `oldsig=b64signature`와 oldname, olddest 중 하나 또는 둘 다가 있어야 합니다.

Add 또는 Change 명령에서 검증용 공개 키는 추가되거나 변경될 Destination에 포함되어 있습니다.

일부 추가 또는 편집 명령에서는 별칭을 추가하거나 destination이나 호스트 이름을 변경할 때와 같이 추가 destination이 참조될 수 있습니다. 이 경우 두 번째 서명이 포함되어야 하며 둘 다 검증되어야 합니다. 두 번째 서명은 "내부" 서명이며 ("외부" 서명을 제외하고) 먼저 서명되고 검증됩니다. 클라이언트는 변경 사항을 검증하고 승인하기 위해 필요한 추가 작업을 수행해야 합니다.

oldsig는 항상 "내부" 서명입니다. 'oldsig' 또는 'sig' 키가 없는 상태에서 서명하고 검증합니다. sig는 항상 "외부" 서명입니다. 'oldsig' 키는 있지만 'sig' 키는 없는 상태에서 서명하고 검증합니다.

#### 서명을 위한 입력

서명을 생성하거나 검증하기 위한 바이트 스트림을 생성하려면 다음과 같이 직렬화하세요:

- "sig" 키 제거
- oldsig로 검증하는 경우, "oldsig" 키도 제거
- Add 또는 Change 명령어에서만 `example.i2p=b64dest` 출력
- 남은 키가 있으면 `#!` 출력
- UTF-8 키 순서로 옵션을 정렬하고, 중복 키가 있으면 실패
- 각 키/값에 대해 `key=value`를 출력하고, (마지막 키/값이 아닌 경우) `#` 추가

참고사항:

- 개행 문자를 출력하지 마세요
- 출력 인코딩은 UTF-8입니다
- 모든 destination과 서명 인코딩은 I2P 알파벳을 사용한 Base 64입니다
- 키와 값은 대소문자를 구분합니다
- 호스트 이름은 소문자여야 합니다

## 호환성

hosts.txt 형식의 모든 새로운 라인은 선행 주석 문자를 사용하여 구현되므로, 모든 이전 I2P 버전에서는 새로운 명령을 주석으로 해석합니다.

I2P router들이 새로운 사양으로 업데이트될 때, 기존 댓글들을 다시 해석하지는 않지만 구독 피드의 후속 가져오기에서 새로운 명령들을 수신하기 시작합니다. 따라서 네임 서버가 명령 항목들을 어떤 방식으로든 지속시키거나, router들이 모든 과거 명령들을 가져올 수 있도록 etag 지원을 활성화하는 것이 중요합니다.
