---
title: "ECDSA 키 블라인딩"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## 동기

일부 사람들은 EdDSA나 RedDSA를 좋아하지 않습니다. 우리는 몇 가지 대안을 제시하고 그들이 ECDSA 서명을 블라인드할 수 있도록 해야 합니다.

## 개요

이 제안서는 ECDSA 서명 유형 1, 2, 3에 대한 키 블라인딩을 설명합니다.

## 제안

RedDSA와 동일한 방식으로 작동하지만 모든 것이 Big Endian입니다.
오직 동일한 서명 유형들만 허용됩니다. 예: 1->1, 2->2, 3->3.

### 정의

B
    커브의 베이스 포인트 

L
   타원 곡선의 그룹 순서. 커브의 속성.

DERIVE_PUBLIC(a)
    타원 곡선상의 B에 곱셈하여 비공개 키를 공개로 변환

alpha
    목적지를 아는 사람들이 아는 32바이트의 랜덤 숫자.

GENERATE_ALPHA(destination, date, secret)
    목적지와 비밀을 아는 사람들을 위해 현재 날짜에 대한 alpha 생성.

a
    목적지를 서명하는 데 사용되는 블라인드 처리되지 않은 32바이트 서명 비공개 키

A
    목적지의 블라인드 처리되지 않은 32바이트 서명 공개 키,
    = 해당 곡선에서 DERIVE_PUBLIC(a)

a'
    암호화된 임대 세트를 서명하는 데 사용되는 블라인드 처리된 32바이트 서명 비공개 키
    이 키는 유효한 ECDSA 비공개 키입니다.

A'
    목적지의 블라인드된 32바이트 ECDSA 서명 공개 키
    DERIVE_PUBLIC(a') 또는 A와 alpha로 생성할 수 있습니다.
    이 키는 곡선상 유효한 ECDSA 공개 키입니다.

H(p, d)
    개인화 문자열 p와 데이터 d를 받아들이는 SHA-256 해시 함수이며
    길이가 32바이트인 출력을 생성합니다.

    다음과 같이 SHA-256을 사용하십시오::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    암호학적 키 파생 함수로, 일부 입력 키 자료 ikm (좋은 엔트로피가 필요하지만 균일한 랜덤 문자열일 필요는 없음), 
    길이 32바이트의 소금, 그리고 컨텍스트별 'info' 값을 받아 n 바이트의 출력을 생성합니다. 이 출력은 키 자료로 사용하기 적합합니다.

    [RFC-5869](https://tools.ietf.org/html/rfc5869)에 명시된 대로 사용하고, HMAC 해시 함수는 [RFC-2104](https://tools.ietf.org/html/rfc2104)에 명시된 SHA-256을 사용합니다. 이는 SALT_LEN이 최대 32바이트임을 의미합니다.


### 블라인딩 계산

매일(UTC) 새로운 비밀 alpha와 블라인드된 키가 생성되어야 합니다.
비밀 alpha와 블라인드된 키는 다음과 같이 계산됩니다.

모든 당사자의 경우 GENERATE_ALPHA(destination, date, secret):

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret는 선택 사항이며, 없을 경우 길이는 0
  A = 목적지의 서명 공개 키
  stA = A의 서명 유형, 2 바이트 big endian (0x0001, 0x0002 또는 0x0003)
  stA' = 블라인드된 공개 키 A'의 서명 유형, 2 바이트 big endian, 항상 stA와 동일
  keydata = A || stA || stA'
  datestring = 현재 날짜 UTC에서 8바이트 ASCII YYYYMMDD
  secret = UTF-8 인코딩된 문자열
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // seed를 64바이트 big-endian 값으로 처리
  alpha = seed mod L
```


임대 세트를 게시하는 소유자를 위한 BLIND_PRIVKEY():

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = 목적지의 서명 비공개 키
  // 스칼라 산술을 사용한 덧셈
  블라인드 처리된 서명 비공개 키 = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  블라인드 처리된 서명 공개 키 = A' = DERIVE_PUBLIC(a')
```


임대 세트를 검색하는 클라이언트를 위한 BLIND_PUBKEY():

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = 목적지의 서명 공개 키
  // 그룹 요소를 사용한 덧셈 (곡선 위의 점들)
  블라인드 처리된 공개 키 = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


A' 계산의 두 방법 모두 요구대로 동일한 결과를 생성합니다.

## b33 주소

ECDSA의 공개 키는 (X,Y) 쌍이므로, 예를 들어 P256의 경우에는 RedDSA보다 32바이트가 더 긴 64바이트입니다.
따라서 b33 주소는 더 길어지거나 비트코인 지갑처럼 압축된 형식으로 공개 키를 저장할 수 있습니다.


## 참고 자료

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
