---
title: "주소 구독 피드 명령어"
description: "호스트명 보유자가 자신의 항목을 업데이트하고 관리할 수 있도록 하는 주소 구독 피드용 확장 기능"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## 개요

이 사양은 주소 구독 피드에 명령을 추가하여 네임 서버가 호스트네임 소유자로부터의 엔트리 업데이트를 브로드캐스트할 수 있도록 합니다. 처음에는 [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (2014년 9월)에서 제안되었고, 버전 0.9.26(2016년 6월)에서 구현되었으며, 네트워크 전반에 배포되었고 상태는 CLOSED입니다.

해당 시스템은 초기 구현 이후로 안정적이며 변경 없이 유지되어 왔고, I2P 2.10.0(Router API 0.9.65, 2025년 9월)에서도 계속 동일하게 동작하고 있습니다.

## 동기

이전에는 hosts.txt 구독 서버들이 단순한 hosts.txt 형식으로만 데이터를 전송했습니다:

```
example.i2p=b64destination
```
이 기본 형식은 여러 가지 문제를 초래했습니다:

- 호스트명 보유자는 자신의 호스트명에 연관된 Destination(목적지 식별자)을 업데이트할 수 없다(예: 서명 키를 더 강력한 서명 키 유형으로 업그레이드하기 위해).
- 호스트명 보유자는 임의로 자신의 호스트명을 포기할 수 없다. 해당 Destination의 개인 키를 새 보유자에게 직접 전달해야 한다.
- 서브도메인이 대응하는 기본 호스트명에 의해 관리되고 있음을 인증할 방법이 없다. 이는 현재 일부 네임 서버에서만 개별적으로 강제되고 있다.

## 설계

이 사양은 hosts.txt 형식에 명령 줄을 추가합니다. 이러한 명령을 통해 네임 서버는 서비스를 확장하여 추가 기능을 제공할 수 있습니다. 이 사양을 구현한 클라이언트는 일반적인 구독 절차를 통해 이러한 기능을 수신할 수 있습니다.

모든 명령 행은 해당 Destination(목적지 주소)에 의해 서명되어야 합니다. 이는 변경이 호스트네임 소유자의 요청이 있을 때에만 이루어지도록 보장합니다.

## 보안상의 함의

이 명세는 익명성에 영향을 미치지 않습니다.

누군가가 Destination key를 입수하면 이러한 명령을 사용해 연계된 모든 호스트명에 변경을 가할 수 있으므로, Destination key에 대한 통제권을 잃는 것과 관련된 위험이 증가한다. 그러나 이는 현행 상태와 비교해 더 큰 문제는 아니다. 현행 상태에서는 누군가 Destination(서비스 식별자)을 입수하면 호스트명을 사칭하고 그 트래픽을 (부분적으로) 가로챌 수 있기 때문이다. 이러한 위험 증가는, Destination이 침해되었다고 판단되는 경우 호스트명 보유자에게 해당 호스트명에 연계된 Destination을 변경할 수 있는 권한을 부여함으로써 상쇄된다. 이는 현행 시스템에서는 불가능하다.

## 명세

### 새로운 라인 유형

새로운 라인 유형이 두 가지 있습니다:

1. **Add 및 Change 명령:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **삭제 명령어:**

```
#!key1=val1#key2=val2...
```
#### 순서

피드는 반드시 순서가 맞거나 완전하다고 보장되지 않습니다. 예를 들어, change command가 add command보다 앞선 행에 나타나거나, add command 없이 나타날 수도 있습니다.

키는 어떤 순서로든 배치될 수 있습니다. 중복된 키는 허용되지 않습니다. 모든 키와 값은 대소문자를 구분합니다.

### 공통 키

**모든 명령에 공통적으로 필요한 사항:**

**sig** : destination(목적지)의 서명 키를 사용한 Base64 서명

**두 번째 호스트명 및/또는 목적지에 대한 참조:**

**oldname** : 또 다른 호스트명 (신규 또는 변경됨)

**olddest** : 두 번째 Base64 목적지(새로 생성되었거나 변경됨)

**oldsig** : olddest의 서명 키를 사용한 두 번째 Base64 서명

**기타 일반적인 키:**

**action** : 명령

**name** : 호스트 이름으로, `example.i2p=b64dest`가 앞에 오지 않은 경우에만 존재합니다

**dest** : Base64로 인코딩된 목적지로, `example.i2p=b64dest`가 앞에 오지 않은 경우에만 포함됩니다

**date** : epoch(유닉스 기준 시각) 이후부터 경과한 초 수

**expires** : epoch(유닉스 기준 시각) 이후 경과한 초 수

### 명령어

"Add" 명령을 제외한 모든 명령에는 `action=command` 키/값 쌍이 포함되어야 합니다.

구버전 클라이언트와의 호환성을 위해, 아래에 언급한 대로 대부분의 명령 앞에는 `example.i2p=b64dest`가 붙습니다. 변경 사항의 경우 표기된 값은 항상 새 값입니다. 이전 값은 키/값 섹션에 포함됩니다.

나열된 키는 필수입니다. 모든 명령은 여기에서 정의되지 않은 추가 키/값 항목을 포함할 수 있습니다.

#### 호스트 이름 추가

**앞에 example.i2p=b64dest가 붙음** : 예, 이것이 새로운 호스트명과 목적지입니다.

**action** : 포함되지 않습니다, 암시됩니다.

**sig** : 서명

예시:

```
example.i2p=b64dest#!sig=b64sig
```
#### 호스트 이름 변경

**example.i2p=b64dest가 앞에 붙은 경우** : 예, 이것은 새로운 호스트네임과 기존 destination(목적지)입니다.

**action** : changename

**oldname** : 교체될 이전 호스트 이름

**sig** : 서명

예시:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### 목적지 변경

**example.i2p=b64dest가 앞에 붙음** : 예, 이는 기존 호스트명과 새 목적지입니다.

**action** : changedest

**olddest** : 이전 목적지, 교체될 대상

**oldsig** : olddest를 사용한 디지털 서명

**sig** : 서명

예시:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 호스트명 별칭 추가

**example.i2p=b64dest가 앞에 붙음** : 예, 이것은 새(별칭) 호스트명과 이전 destination(목적지)입니다.

**action** : addname

**oldname** : 이전 호스트명

**sig** : 서명

예:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Destination(목적지) 별칭 추가

(암호화 업그레이드용)

**앞에 example.i2p=b64dest가 붙음** : 예, 이것은 기존 호스트명과 새로운(대체) 목적지입니다.

**action** : adddest

**olddest** : 이전 목적지

**oldsig** : olddest를 사용한 서명

**sig** : dest를 사용한 서명

예시:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 서브도메인 추가

**앞에 subdomain.example.i2p=b64dest가 붙음** : 예, 이것이 새로운 하위 도메인 이름과 destination(목적지 주소)입니다.

**action** : addsubdomain

**oldname** : 상위 수준 호스트명 (example.i2p)

**olddest** : 상위 수준 destination(목적지) (예: example.i2p)

**oldsig** : olddest를 사용한 서명

**sig** : dest를 사용한 서명

예시:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### 메타데이터 업데이트

**example.i2p=b64dest로 시작함** : 예, 이것은 이전의 호스트명과 목적지입니다.

**작업** : 업데이트

**sig** : 서명

(업데이트된 키가 있으면 여기에 추가하세요)

예시:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### 호스트 이름 제거

**앞에 example.i2p=b64dest를 붙임** : 아니요, 이는 옵션에서 지정됩니다

**동작** : 제거

**name** : 호스트 이름

**dest** : 목적지

**sig** : 서명

예시:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### 이 목적지를 사용하는 모든 항목 제거

**example.i2p=b64dest를 접두로 사용** : 아니요, 이는 옵션에서 지정됩니다

**action** : removeall

**dest** : 목적지

**sig** : 서명

예시:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### 서명

모든 명령은 해당하는 Destination(목적지 엔드포인트)에 의해 서명되어야 합니다. 두 개의 Destination이 포함된 명령은 두 개의 서명이 필요할 수 있습니다.

`oldsig`는 항상 "내부" 서명입니다. `oldsig`와 `sig` 키가 존재하지 않은 상태에서 서명하고 검증하십시오. `sig`는 항상 "외부" 서명입니다. `oldsig` 키는 존재하지만 `sig` 키는 존재하지 않는 상태에서 서명하고 검증하십시오.

#### 서명용 입력

서명 생성·검증용 바이트 스트림을 만들려면 다음과 같이 직렬화합니다:

1. `sig` 키를 제거합니다
2. `oldsig`로 검증하는 경우 `oldsig` 키도 제거합니다
3. Add 또는 Change 명령에서만 `example.i2p=b64dest`를 출력합니다
4. 키가 하나라도 남아 있으면 `#!`를 출력합니다
5. 옵션을 키의 UTF-8 순서로 정렬하고, 중복 키가 있으면 실패합니다
6. 각 키/값에 대해 `key=value`를 출력하고, 마지막 키/값이 아니라면 그 뒤에 `#`를 붙입니다

**참고 사항**

- 개행을 출력하지 마십시오
- 출력 인코딩은 UTF-8입니다
- 모든 destination(목적지 식별자) 및 서명 인코딩은 I2P 알파벳을 사용하는 Base 64입니다
- 키와 값은 대소문자를 구분합니다
- 호스트명은 소문자여야 합니다

#### 현재 서명 유형

I2P 2.10.0 기준으로, destinations(목적지)에 대해 다음과 같은 서명 유형이 지원됩니다:

- **EdDSA_SHA512_Ed25519** (Type 7): 0.9.15부터 Destination(목적지)에서 가장 일반적으로 사용됩니다. 32바이트 공개 키와 64바이트 서명을 사용합니다. 새로운 Destination에 권장되는 서명 유형입니다.
- **RedDSA_SHA512_Ed25519** (Type 13): Destination 및 암호화된 leaseSet에만 사용 가능합니다(0.9.39부터).
- 레거시 유형 (DSA_SHA1, ECDSA variants): 여전히 지원되지만 0.9.58부터 새로운 Router 식별자에 대해서는 사용 중단(deprecated)되었습니다.

참고: I2P 2.10.0부터 포스트-양자 암호 옵션을 사용할 수 있지만, 아직 기본 서명 유형은 아닙니다.

## 호환성

hosts.txt 형식의 모든 새로운 줄은 선행 주석 문자(`#!`)를 사용해 구현되므로, 모든 이전 I2P 버전은 새로운 명령을 주석으로 해석하고 문제 없이 무시합니다.

I2P router가 새로운 사양으로 업데이트되면, 기존 주석을 다시 해석하지는 않지만 이후에 자신의 구독 피드를 다시 가져올 때 새로운 명령을 수신하기 시작한다. 따라서 네임 서버는 명령 항목을 어떤 방식으로든 영속적으로 유지하거나, ETag(HTTP 엔터티 태그) 지원을 활성화하여 I2P router가 과거의 모든 명령을 가져올 수 있도록 하는 것이 중요하다.

## 구현 현황

**초기 배포:** 버전 0.9.26 (2016년 6월 7일)

**현재 상태:** I2P 2.10.0까지 안정적이며 변경되지 않음 (Router API 0.9.65, 2025년 9월)

**제안 상태:** 닫힘(네트워크 전역에 성공적으로 배포됨)

**구현 위치:** `apps/addressbook/java/src/net/i2p/addressbook/` I2P Java router에 있음

**핵심 클래스:** - `SubscriptionList.java`: 구독 처리 관리 - `Subscription.java`: 개별 구독 피드 처리 - `AddressBook.java`: 핵심 주소록 기능 - `Daemon.java`: 주소록 백그라운드 서비스

**기본 구독 URL:** `http://i2p-projekt.i2p/hosts.txt`

## 전송 세부 사항

구독은 조건부 GET을 지원하는 HTTP를 사용합니다:

- **ETag 헤더:** 효율적인 변경 감지를 지원합니다
- **Last-Modified 헤더:** 구독 업데이트 시간을 추적합니다
- **304 Not Modified:** 콘텐츠가 변경되지 않았을 때 서버는 이를 반환해야 합니다
- **Content-Length:** 모든 응답에 명시할 것을 강력히 권장합니다

I2P router는 적절한 캐시 지원과 함께 표준 HTTP 클라이언트 동작을 따릅니다.

## 버전 컨텍스트

**I2P 버전 관리 참고:** 1.5.0(2021년 8월) 버전 무렵부터 I2P는 0.9.x 버전 체계에서 시맨틱 버저닝(1.x, 2.x 등)으로 전환했습니다. 그러나 내부 Router API 버전은 하위 호환성을 위해 계속해서 0.9.x 번호 체계를 사용합니다. 2025년 10월 기준 현재 릴리스는 I2P 2.10.0이며 Router API 버전은 0.9.65입니다.

이 명세 문서는 원래 0.9.49 버전(2021년 2월)용으로 작성되었으며, 구독 피드 시스템이 0.9.26에서 처음 구현된 이후 변경되지 않았기 때문에 현재 버전 0.9.65 (I2P 2.10.0)에서도 여전히 완전히 정확합니다.

## 참고 자료

- [제안 112 (원문)](/proposals/112-addressbook-subscription-feed-commands/)
- [공식 명세](/docs/specs/subscription/)
- [I2P 네이밍 문서](/docs/overview/naming/)
- [공통 구조 명세](/docs/specs/common-structures/)
- [I2P 소스 코드 저장소](https://github.com/i2p/i2p.i2p)
- [I2P Gitea 저장소](https://i2pgit.org/I2P_Developers/i2p.i2p)

## 관련 개발

구독 피드 시스템 자체에는 변화가 없지만, I2P의 네이밍 인프라에서 관심을 가질 만한 관련 발전 사항은 다음과 같습니다:

- **확장된 Base32 이름** (0.9.40+): 암호화된 leasesets를 위한 56자 이상의 base32 주소를 지원합니다. 구독 피드 형식에는 영향을 주지 않습니다.
- **.i2p.alt TLD 등록** (RFC 9476, 2023년 말): 대체 TLD로서 .i2p.alt의 공식 GANA 등록. 향후 router 업데이트에서 .alt 접미사가 제거될 수 있으나, 구독 명령에는 변경이 필요하지 않습니다.
- **포스트-양자 암호** (2.10.0+): 사용 가능하지만 기본값은 아님. 구독 피드의 서명 알고리즘에 대해 향후 고려될 예정입니다.
