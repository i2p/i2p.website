---
title: "ECIES 목적지에서 데이터베이스 조회"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Closed"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## 주의
ECIES에서 ElG로의 구현은 0.9.46에 완료되었으며 제안 단계는 종료되었습니다.
공식 사양은 [I2NP](/docs/specs/i2np/)를 참조하십시오.
배경 정보를 위해 이 제안을 참조할 수 있습니다.
포함된 키를 이용한 ECIES에서 ECIES로의 구현은 0.9.48 이후로 완료되었습니다.
ECIES에서 ECIES (파생 키) 섹션은 앞으로의 제안에서 다시 열리거나 통합될 수 있습니다.

## 개요

### 정의

- AEAD: ChaCha20/Poly1305
- DLM: I2NP 데이터베이스 조회 메시지
- DSM: I2NP 데이터베이스 저장 메시지
- DSRM: I2NP 데이터베이스 검색 응답 메시지
- ECIES: ECIES-X25519-AEAD-Ratchet (제안 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): [ECIES](/docs/specs/ecies/)에서 정의된 바와 같이
- LS: Leaseset
- 조회: I2NP DLM
- 응답: I2NP DSM 또는 DSRM

### 요약

플러드필로 DLM을 보낼 때, DLM은 일반적으로 응답이 태그를 지정하고, AES로 암호화되며 대상 터널로 전송되도록 지정합니다.
AES 암호화 응답에 대한 지원은 0.9.7에 추가되었습니다.

AES 암호화 응답은 ElG의 큰 암호화 오버헤드를 최소화하기 위해 0.9.7에 명시되었으며, ElGamal/AES+SessionTags의 태그/AES 기능을 재사용하기 때문에 적용되었습니다.
그러나 AES 응답은 IBEP에서 인증되지 않으므로 변조될 수 있으며 응답은 순방향 비밀성이 없습니다.

[ECIES](/docs/specs/ecies/) 목적을 사용할 때, 제안 144의 의도는 더 이상 목적지가 32바이트 태그 및 AES 복호화를 지원하지 않는 것입니다.
구체적인 사항들은 그 제안서에 의도적으로 포함되지 않았습니다.

이 제안서는 DLM에 ECIES 암호화 응답을 요청하는 새로운 옵션을 문서화합니다.

### 목표

- ECIES 목적지로 터널을 통해 암호화된 응답이 요청될 때 DLM에 대한 새로운 플래그
- 요청자의 (목적지) 키 손상의 사칭 저항성을 갖춘 송신자 인증과 순방향 비밀성을 응답에 추가
- 요청자의 익명성 유지
- 암호화 오버헤드 최소화

### 비목표

- 조회(DLM)의 암호화 또는 보안 속성에는 변화 없음.
  조회는 요청자 키 손상에 대한 순방향 비밀성을 가지고 있습니다.
  암호화는 플러드필의 정적 키에 적용됩니다.
- 응답자의 (플러드필의) 키 손상에 대한 사칭 저항성을 가지는 순방향 비밀성이나 송신자 인증 문제 없음.
  플러드필은 공공 데이터베이스로 누구의 조회에도 응답할 것입니다.
- 이 제안을 통해 ECIES 라우터를 설계하지 않음.
  라우터의 X25519 공개 키 위치는 결정되지 않았습니다.

## 대안

ECIES 목적지에 응답을 암호화하는 방법이 정의되어 있지 않은 경우, 몇 가지 대안이 있습니다.

1) 암호화된 응답을 요청하지 않습니다. 응답은 암호화되지 않습니다. Java I2P는 현재 이 접근 방식을 사용합니다.

2) ECIES 전용 목적지에 32바이트 태그 및 AES 암호화 응답에 대한 지원을 추가하고, 일상적인 AES 암호화 응답을 요청합니다. i2pd는 현재 이 방식을 사용합니다.

3) 일반적으로 AES 암호화 응답을 요청하되, 탐색 큐를 통해 라우터로 다시 라우팅합니다. Java I2P는 일부 경우에 이 방식을 사용합니다.

4) ElG와 ECIES 이중 목적지를 위해, 일상적인 AES 암호화 응답을 요청합니다. Java I2P는 현재 이 방식을 사용합니다. i2pd는 아직 이중 암호 목적지를 구현하지 않았습니다.

## 설계

- 새로운 DLM 형식은 ECIES 암호화 응답을 지정하기 위해 플래그 필드에 비트를 추가할 것입니다. ECIES 암호화 응답은 [ECIES](/docs/specs/ecies/) 기존 세션 메시지 형식을 사용할 것이며, 태그를 앞에 붙이고 ChaCha/Poly 페이로드 및 MAC을 포함합니다.

- 두 가지 변형을 정의합니다. DH 연산이 불가능한 ElG 라우터에 대한 것과, DH 연산이 가능하고 추가 보안을 제공할 수 있는 미래의 ECIES 라우터에 대한 것입니다. 추가 연구가 필요합니다.

ElG 라우터로부터 응답에 대한 DH는 X25519 공개 키를 게시하지 않기 때문에 불가능합니다.

## 사양

[I2NP](/docs/specs/i2np/) DLM (DatabaseLookup) 사양에서 다음의 변경 사항을 적용합니다.

플래그 비트 4 "ECIESFlag"를 새로운 암호화 옵션을 위해 추가하십시오.

```text
flags ::
       bit 4: ECIESFlag
               버전 0.9.46 이전에는 무시됨
               버전 0.9.46부터:
               0  => 암호화되지 않거나 ElGamal 응답 전송
               1  => 포함된 키를 사용하여 ChaCha/Poly 암호화 응답 전송
                     (태그 포함 여부는 비트 1에 따라 다름)
```

플래그 비트 4는 비트 1과 조합하여 응답 암호화 모드를 결정합니다.
플래그 비트 4는 버전 0.9.46 이상으로 전송될 때만 설정되어야 합니다.

아래의 표에서,
"DH n/a"는 응답이 암호화되지 않음을 의미하며,
"DH no"는 응답 키가 요청에 포함되어 있음을 의미하며,
"DH yes"는 응답 키가 DH 연산에서 파생됨을 의미합니다.

=============  =========  =========  ======  ===  =======
Flag bits 4,1  From Dest  To Router  Reply   DH?  notes
=============  =========  =========  ======  ===  =======
0 0            Any        Any        no enc  n/a  현재
0 1            ElG        ElG        AES     no   현재
0 1            ECIES      ElG        AES     no   i2pd 해결책
1 0            ECIES      ElG        AEAD    no   이 제안
1 0            ECIES      ECIES      AEAD    no   0.9.49
1 1            ECIES      ECIES      AEAD    yes  미래
=============  =========  =========  ======  ===  =======

### ElG에서 ElG

ElG 목적지는 ElG 라우터에 조회를 보냅니다.

사양에 새로운 비트 4를 확인하는 사소한 변경 사항입니다.
기존 바이너리 형식에는 변경 사항이 없습니다.

요청자 키 생성 (명확히 설명):

```text
reply_key :: CSRNG(32) 32 바이트 랜덤 데이터
  reply_tags :: 각 CSRNG(32) 32 바이트 랜덤 데이터
```

메시지 형식 (ECIESFlag 확인 추가):

```text
reply_key ::
       32 byte `SessionKey` big-endian
       암호화Flag == 1 이고 ECIESFlag == 0 인 경우에만 포함, 버전 0.9.7 이후에만 적용

  tags ::
       1 byte `Integer`
       유효 범위: 1-32 (일반적으로 1)
       뒤따르는 응답 태그의 수
       암호화Flag == 1 이고 ECIESFlag == 0 인 경우에만 포함, 버전 0.9.7 이후에만 적용

  reply_tags ::
       하나 이상의 32 바이트 `SessionTag` (일반적으로 하나)
       암호화Flag == 1 이고 ECIESFlag == 0 인 경우에만 포함, 버전 0.9.7 이후에만 적용
```

### ECIES에서 ElG

ECIES 목적지는 ElG 라우터에 조회를 보냅니다.
0.9.46부터 지원됩니다.

ECIES 암호화 응답에 대한 reply_key 및 reply_tags 필드가 재정의됩니다.

요청자 키 생성:

```text
reply_key :: CSRNG(32) 32 바이트 랜덤 데이터
  reply_tags :: 각 CSRNG(8) 8 바이트 랜덤 데이터
```

메시지 형식:
reply_key 및 reply_tags 필드를 다음과 같이 재정의합니다:

```text
reply_key ::
       32 byte ECIES `SessionKey` big-endian
       암호화Flag == 0 이고 ECIESFlag == 1 인 경우에만 포함, 버전 0.9.46 이후에만 적용

  tags ::
       1 byte `Integer`
       요구되는 값: 1
       뒤따르는 응답 태그의 수
       암호화Flag == 0 이고 ECIESFlag == 1 인 경우에만 포함, 버전 0.9.46 이후에만 적용

  reply_tags ::
       8 byte ECIES `SessionTag`
       암호화Flag == 0 이고 ECIESFlag == 1 인 경우에만 포함, 버전 0.9.46 이후에만 적용
```

응답은 [ECIES](/docs/specs/ecies/)에서 정의된 대로 ECIES 기존 세션 메시지입니다.

```text
tag :: 8 byte reply_tag

  k :: 32 byte session key
     The reply_key.

  n :: 0

  ad :: The 8 byte reply_tag

  payload :: Plaintext data, the DSM or DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### ECIES에서 ECIES (0.9.49)

ECIES 목적지 또는 라우터가 ECIES 라우터로 조회를 보내며, 포함된 응답 키와 함께 합니다.
0.9.49부터 지원됩니다.

ECIES 라우터는 0.9.48에 도입되었습니다, [Prop156](/proposals/156-ecies-routers/)를 참조하십시오.
0.9.49부터 ECIES 목적지와 라우터는 "ECIES에서 ElG" 섹션의 형식을 동일하게 사용할 수 있으며, 요청에 포함된 응답 키를 사용합니다.
조회는 요청자가 익명이므로 [ECIES](/docs/specs/ecies/)에서 "일회성 형식"을 사용합니다.

새로운 파생 키 방식을 위한 방법은 다음 섹션을 참조하십시오.

### ECIES에서 ECIES (미래)

ECIES 목적지 또는 라우터가 ECIES 라우터로 조회를 보내며, 응답 키는 DH에서 파생됩니다.
완전히 정의되지 않았으며 지원되지 않습니다, 구현은 TBD입니다.

조회는 요청자가 익명이므로 [ECIES](/docs/specs/ecies/)에서 "일회성 형식"을 사용합니다.

reply_key 필드를 다음과 같이 재정의하십시오. 관련 태그는 없습니다.
태그는 아래 KDF에서 생성됩니다.

이 섹션은 불완전하며 추가 연구가 필요합니다.

```text
reply_key ::
       32 byte X25519 ephemeral `PublicKey` of the requester, little-endian
       암호화Flag == 1 이고 ECIESFlag == 1 인 경우에만 포함, 버전 0.9.TBD 이후에만 적용
```

응답은 [ECIES](/docs/specs/ecies/)에서 정의된 대로 ECIES 기존 세션 메시지입니다.
모든 정의는 [ECIES](/docs/specs/ecies/)을 참조하십시오.

```text
// Alice의 X25519 임시 키
  // aesk = Alice 임시 개인 키
  aesk = GENERATE_PRIVATE()
  // aepk = Alice 임시 공개 키
  aepk = DERIVE_PUBLIC(aesk)
  // Bob의 X25519 정적 키
  // bsk = Bob의 개인 정적 키
  bsk = GENERATE_PRIVATE()
  // bpk = Bob의 공개 정적 키
  // bpk는 RouterIdentity의 일부이거나 RouterInfo에 게시됨 (TBD)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey는 ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = Payload Section에서 온 chainKey
  2) 새로운 세션 KDF 또는 분할()에서 온 k

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // 출력 1: 사용되지 않음
  unused = keydata[0:31]
  // 출력 2: 새로운 세션 태그 및 대칭 키 일치기를 초기화하기 위한 체인 키
  // Alice에서 Bob으로 전송
  ck = keydata[32:63]

  // 세션 태그 및 대칭 키 체인 키
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: [ECIES](/docs/specs/ecies/)에서 RATCHET_TAG()로 생성된 8바이트 태그

  k :: [ECIES](/docs/specs/ecies/)에서 RATCHET_KEY()로 생성된 32바이트 키

  n :: 태그의 인덱스. 일반적으로 0.

  ad :: 8바이트 태그

  payload :: DSM 또는 DSRM, 평문 데이터.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### 응답 형식

기존 세션 메시지입니다,
[ECIES](/docs/specs/ecies/), 아래 복사한 참조를 위한 겁니다.

```text
+----+----+----+----+----+----+----+----+
  |       Session Tag                     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 암호화 데이터          |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 메시지 인증 코드              |
  +              (MAC)                    +
  |             16 바이트                 |
  +----+----+----+----+----+----+----+----+

  Session Tag :: 8 바이트, 클리어 텍스트

  Payload Section 암호화 데이터 :: 남은 데이터 16 바이트 제외

  MAC :: Poly1305 메시지 인증 코드, 16 바이트
```

## 정당화

0.9.7에 처음 도입된 조회에서의 응답 암호화 매개변수는 약간의 계층 위반입니다. 효율성 때문에 이렇게 적용됩니다.
또한 조회가 익명적이기 때문입니다.

조회 형식을 암호화 유형 필드처럼 일반화할 수도 있지만, 이는 아마 더 많은 문제를 야기할 것입니다.

위의 제안은 가장 쉽고 조회 형식 변경을 최소화합니다.

## 메모

ElG 라우터에 대한 데이터베이스 조회 및 저장은 여전히 ElGamal/AESSessionTag 암호화로 적용되어야 합니다.

## 문제점

두 가지 ECIES 응답 옵션의 보안에 대한 추가 분석이 필요합니다.

## 마이그레이션

호환성 관련 문제는 없습니다. RouterInfo에서 버전이 0.9.46 이상인 라우터는 이 기능을 지원해야 합니다.
라우터는 버전이 0.9.46 미만인 라우터에 새로운 플래그가 있는 DatabaseLookup을 보내서는 안됩니다.
실수로 플래그 비트 4가 설정되고 비트 1이 설정되지 않은 데이터베이스 조회 메시지가 지원되지 않는 라우터에 전송되면, 아마도 공급된 키와 태그를 무시하고 응답을 암호화되지 않은 상태로 전송할 것입니다.
