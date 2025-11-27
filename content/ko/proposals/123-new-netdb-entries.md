---
title: "새로운 netDB 항목"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "열기"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## 상태

이 제안서의 일부가 완료되어 0.9.38과 0.9.39에서 구현되었습니다. Common Structures, I2CP, I2NP 및 기타 사양서들이 현재 지원되는 변경사항을 반영하도록 업데이트되었습니다.

완성된 부분들도 여전히 사소한 수정이 있을 수 있습니다. 이 제안서의 다른 부분들은 아직 개발 중이며 상당한 수정이 있을 수 있습니다.

Service Lookup (타입 9와 11)은 우선순위가 낮고 일정이 정해지지 않았으며, 별도의 제안서로 분리될 수 있습니다.

## 개요

다음 4개 제안서의 업데이트 및 통합 내용입니다:

- 110 LS2
- 120 대규모 멀티호밍을 위한 Meta LS2
- 121 암호화된 LS2
- 122 인증되지 않은 서비스 조회 (애니캐스팅)

이러한 제안들은 대부분 독립적이지만, 일관성을 위해 여러 제안에서 공통 형식을 정의하고 사용합니다.

다음 제안들은 어느 정도 관련이 있습니다:

- 140 Invisible Multihoming (이 제안과 호환되지 않음)
- 142 New Crypto Template (새로운 대칭 암호화용)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 for Encrypted LS2
- 150 Garlic Farm Protocol
- 151 ECDSA Blinding

## 제안서

이 제안은 5개의 새로운 DatabaseEntry 타입과 이를 netDb에 저장하고 검색하는 프로세스, 그리고 이를 서명하고 해당 서명을 검증하는 방법을 정의합니다.

### Goals

- 하위 호환성 지원
- LS2는 기존 스타일의 멀티호밍과 함께 사용 가능
- 지원을 위해 새로운 암호화 기법이나 기본 요소가 필요하지 않음
- 암호화와 서명의 분리를 유지하고 현재 및 미래의 모든 버전을 지원
- 선택적 오프라인 서명 키 지원
- 핑거프린팅을 줄이기 위해 타임스탬프 정확도 감소
- 목적지를 위한 새로운 암호화 기법 지원
- 대규모 멀티호밍 지원
- 기존 암호화된 LS의 여러 문제 수정
- floodfill에 의한 가시성을 줄이기 위한 선택적 블라인딩
- 암호화된 방식은 단일 키와 취소 가능한 다중 키를 모두 지원
- 아웃프록시의 쉬운 조회, 애플리케이션 DHT 부트스트랩 및 기타 용도를 위한 서비스 조회
- bittorrent와 같은 32바이트 바이너리 목적지 해시에 의존하는 기능을 손상시키지 않음
- routerinfo에서와 같이 속성을 통해 leaseSet에 유연성 추가
- 내용이 암호화되어도 작동하도록 게시 타임스탬프와 가변 만료 시간을 헤더에 배치
  (가장 이른 lease에서 타임스탬프를 도출하지 않음)
- 모든 새로운 타입들은 기존 leaseSet과 동일한 DHT 공간과 위치에 존재하므로,
  사용자가 목적지나 해시를 변경하지 않고도 기존 LS에서 LS2로 마이그레이션하거나
  LS2, Meta, Encrypted 간에 변경할 수 있음
- 기존 목적지는 목적지나 해시를 변경하지 않고도 오프라인 키를 사용하도록
  변환하거나 다시 온라인 키로 되돌릴 수 있음

### Non-Goals / Out-of-scope

- 새로운 DHT 순환 알고리즘 또는 공유 랜덤 생성
- 사용할 구체적인 새로운 암호화 유형 및 해당 새로운 유형을 사용하는 종단간 암호화 방식은
  별도의 제안서에서 다룰 예정입니다.
  여기서는 새로운 암호화 기술을 명시하거나 논의하지 않습니다.
- RI 또는 터널 구축을 위한 새로운 암호화.
  이는 별도의 제안서에서 다룰 예정입니다.
- I2NP DLM / DSM / DSRM 메시지의 암호화, 전송, 수신 방법.
  변경하지 않습니다.
- 백엔드 router 간 통신, 관리, 장애 조치, 조정을 포함한 Meta 생성 및 지원 방법.
  I2CP, i2pcontrol 또는 새로운 프로토콜에 지원이 추가될 수 있습니다.
  이는 표준화될 수도 있고 그렇지 않을 수도 있습니다.
- 더 긴 만료 시간을 가진 터널을 실제로 구현하고 관리하는 방법 또는 기존 터널을 취소하는 방법.
  이는 매우 어려우며, 이것 없이는 합리적인 우아한 종료를 할 수 없습니다.
- 위협 모델 변경사항
- 오프라인 저장 형식 또는 데이터를 저장/검색/공유하는 방법.
- 구현 세부사항은 여기서 논의하지 않으며 각 프로젝트에 맡깁니다.

### Justification

LS2는 암호화 유형 변경과 향후 프로토콜 변경을 위한 필드를 추가합니다.

암호화된 LS2는 전체 lease 세트의 비대칭 암호화를 사용하여 기존 암호화된 LS의 여러 보안 문제를 해결합니다.

Meta LS2는 유연하고 효율적이며 효과적인 대규모 멀티호밍을 제공합니다.

Service Record와 Service List는 네이밍 조회 및 DHT 부트스트래핑과 같은 애니캐스트 서비스를 제공합니다.

### 목표

타입 번호는 I2NP Database Lookup/Store 메시지에서 사용됩니다.

end-to-end 열은 쿼리/응답이 Garlic Message로 Destination에 전송되는지 여부를 나타냅니다.

기존 유형:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
새로운 유형:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### 비목표 / 범위 외

- 조회 유형은 현재 데이터베이스 조회 메시지의 비트 3-2에 있습니다.
  추가 유형은 비트 4를 사용해야 합니다.

- 모든 저장 유형은 홀수입니다. 데이터베이스 저장 메시지 유형 필드의 상위 비트가 구형 router에 의해 무시되기 때문입니다.
  압축된 RI로 파싱이 실패하는 것보다는 LS로 파싱이 실패하는 것을 선호합니다.

- 서명으로 보호되는 데이터에서 타입이 명시적이어야 하는가, 암시적이어야 하는가, 아니면 둘 다 아니어야 하는가?

### 정당화

타입 3, 5, 7은 표준 leaseset 조회(타입 1)에 대한 응답으로 반환될 수 있습니다. 타입 9는 조회에 대한 응답으로 절대 반환되지 않습니다. 타입 11은 새로운 서비스 조회 타입(타입 11)에 대한 응답으로 반환됩니다.

클라이언트 간 Garlic 메시지에서는 타입 3만 전송할 수 있습니다.

### NetDB 데이터 타입

타입 3, 7, 9는 모두 공통 형식을 가집니다::

표준 LS2 헤더   - 아래에 정의된 대로

타입별 부분   - 각 부분에서 아래 정의된 대로

표준 LS2 서명:   - 서명 키의 sig type에 의해 암시된 길이

타입 5 (암호화)는 Destination으로 시작하지 않으며 다른 형식을 가집니다. 아래를 참조하세요.

타입 11 (Service List)은 여러 Service Record들의 집합이며 다른 형식을 가집니다. 아래를 참조하세요.

### 참고사항

TBD

## Standard LS2 Header

타입 3, 7, 9는 아래에 명시된 표준 LS2 헤더를 사용합니다:

### 조회/저장 과정

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### 형식

- Unpublished/published: 데이터베이스 스토어를 종단 간 전송할 때 사용하며, 전송하는 router가 이 leaseSet을 다른 곳으로 보내지 말아야 함을 나타내고자 할 때 사용합니다. 현재 이 상태를 유지하기 위해 휴리스틱을 사용하고 있습니다.

- Published: leaseset의 '버전'을 결정하는 데 필요한 복잡한 로직을 대체합니다. 현재 버전은 마지막으로 만료되는 lease의 만료 시간이며, 게시하는 router는 오래된 lease만 제거하는 leaseset을 게시할 때 해당 만료 시간을 최소 1ms씩 증가시켜야 합니다.

- Expires: netdb 항목의 만료 시간이 마지막으로 만료되는 leaseSet보다 더 이르게 설정될 수 있도록 허용합니다. leaseSet이 최대 11분의 만료 시간을 유지할 것으로 예상되는 LS2에는 유용하지 않을 수 있지만, 다른 새로운 타입들에는 필요합니다 (아래의 Meta LS와 Service Record 참조).

- 오프라인 키는 선택사항이며, 초기/필수 구현 복잡성을 줄이기 위한 것입니다.

### 개인정보보호/보안 고려사항

- 타임스탬프 정확도를 더욱 줄일 수 있지만 (10분?) 버전 번호를 추가해야 할 것입니다. 이는 순서 보존 암호화가 없다면 멀티호밍을 깨뜨릴 수 있습니다. 아마도 타임스탬프 없이는 할 수 없을 것입니다.

- 대안: 3바이트 타임스탬프 (epoch / 10분), 1바이트 버전, 2바이트 만료

- 데이터/서명에서 타입이 명시적인가 암시적인가? 서명을 위한 "Domain" 상수?

### Notes

- Router는 초당 한 번 이상 LS를 게시해서는 안 됩니다.
  만약 그렇게 한다면, 이전에 게시된 LS보다 게시 타임스탬프를 1씩 인위적으로 증가시켜야 합니다.

- Router 구현체들은 매번 검증을 피하기 위해 임시 키와 서명을 캐시할 수 있습니다. 특히 floodfill들과 장기간 연결의 양 끝에 있는 router들이 이것으로부터 이익을 얻을 수 있습니다.

- 오프라인 키와 서명은 장기간 지속되는 destination에만 적합합니다.
  즉, 클라이언트가 아닌 서버에 사용해야 합니다.

## New DatabaseEntry types

### 형식

기존 LeaseSet으로부터의 변경사항:

- 게시된 타임스탬프, 만료 타임스탬프, 플래그, 속성 추가
- 암호화 유형 추가
- 해지 키 제거

다음으로 조회

    Standard LS flag (1)
저장 위치

    Standard LS2 type (3)
저장 위치

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
일반적인 만료

    10 minutes, as in a regular LS.
게시자

    Destination

### 정당화

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### 문제점

- Properties: 향후 확장 및 유연성을 위해 사용됩니다.
  나머지 데이터의 파싱에 필요할 경우를 대비하여 맨 앞에 배치됩니다.

- 여러 암호화 유형/공개 키 쌍은
  새로운 암호화 유형으로의 전환을 용이하게 하기 위한 것입니다. 다른 방법은
  현재 DSA 및 EdDSA 목적지에 대해 하는 것처럼
  동일한 tunnel을 사용하여 여러 leaseSet을 게시하는 것입니다.
  tunnel에서 들어오는 암호화 유형의 식별은
  기존 세션 태그 메커니즘 및/또는 각 키를 사용한 시행착오 복호화로
  수행될 수 있습니다. 들어오는 메시지의 길이도
  단서를 제공할 수 있습니다.

### 참고사항

이 제안은 종단 간 암호화 키에 대해 leaseset의 공개 키를 계속 사용하며, 현재와 같이 Destination의 공개 키 필드는 사용하지 않은 채로 둡니다. 암호화 유형은 Destination 키 인증서에 지정되지 않으며, 0으로 유지됩니다.

거부된 대안은 Destination 키 인증서에서 암호화 타입을 지정하고, Destination의 공개 키를 사용하며, leaseset의 공개 키는 사용하지 않는 것입니다. 우리는 이를 수행할 계획이 없습니다.

LS2의 이점:

- 실제 공개 키의 위치는 변경되지 않습니다.
- 암호화 유형이나 공개 키는 Destination을 변경하지 않고도 변경될 수 있습니다.
- 사용되지 않는 폐기 필드를 제거합니다
- 이 제안서의 다른 DatabaseEntry 유형과의 기본 호환성
- 여러 암호화 유형 허용

LS2의 단점:

- RouterInfo와 공개키 위치 및 암호화 타입이 다름
- leaseset에서 사용되지 않는 공개키를 유지함
- 네트워크 전체에서 구현이 필요함; 대안으로, floodfill에서 허용하는 경우 실험적 
  암호화 타입을 사용할 수 있음
  (하지만 실험적 서명 타입 지원에 관한 관련 제안 136 및 137 참조).
  대안 제안은 실험적 암호화 타입에 대해 구현 및 테스트하기 더 쉬울 수 있음.

### New Encryption Issues

이 중 일부는 이 제안서의 범위를 벗어나지만, 아직 별도의 암호화 제안서가 없기 때문에 현재로서는 여기에 메모를 남겨둡니다. ECIES 제안서 144번과 145번도 참조하세요.

- 암호화 유형은 곡선, 키 길이, 그리고 종단 간 방식의 조합을 나타내며,
  KDF와 MAC가 있는 경우 이를 포함합니다.

- 우리는 키 길이 필드를 포함했으므로, LS2가 알려지지 않은 암호화 유형에 대해서도 floodfill에 의해 파싱 및 검증 가능합니다.

- 제안될 첫 번째 새로운 암호화 유형은
  아마도 ECIES/X25519일 것입니다. 엔드투엔드에서 사용되는 방식
  (ElGamal/AES+SessionTag의 약간 수정된 버전이나
  ChaCha/Poly와 같은 완전히 새로운 방식)은
  하나 이상의 별도 제안서에서 명시될 예정입니다.
  ECIES 제안서 144와 145도 참조하세요.

### LeaseSet 2

- lease의 8바이트 만료 시간이 4바이트로 변경됨.

- 만약 우리가 취소 기능을 구현한다면, expires 필드를 0으로 설정하거나,
  lease를 0개로 하거나, 또는 둘 다 사용할 수 있습니다. 별도의 취소 키는 필요하지 않습니다.

- 암호화 키는 서버 선호도 순서대로 정렬되며, 가장 선호하는 것이 먼저 나옵니다.
  기본 클라이언트 동작은 지원되는 암호화 유형을 가진 첫 번째 키를 선택하는 것입니다. 클라이언트는 암호화 지원, 상대적 성능 및 기타 요소를 기반으로 다른 선택 알고리즘을 사용할 수 있습니다.

### 형식

목표:

- 블라인딩 추가
- 여러 서명 유형 허용
- 새로운 암호화 프리미티브 불필요
- 각 수신자에게 선택적 암호화, 취소 가능
- Standard LS2 및 Meta LS2의 암호화만 지원

암호화된 LS2는 종단 간 garlic 메시지로 전송되지 않습니다. 위의 표준 LS2를 사용하세요.

기존 암호화된 LeaseSet에서의 변경사항:

- 보안을 위해 전체를 암호화
- AES만으로가 아닌 안전한 암호화 사용
- 각 수신자에게 개별적으로 암호화

다음으로 조회

    Standard LS flag (1)
저장 위치

    Encrypted LS2 type (5)
저장 위치

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
일반적인 만료

    10 minutes, as in a regular LS, or hours, as in a meta LS.
게시자

    Destination


### 정당화

암호화된 LS2에 사용되는 암호학적 구성 요소에 해당하는 다음 함수들을 정의합니다:

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### 토론

암호화된 LS2 형식은 세 개의 중첩된 계층으로 구성됩니다:

- 저장 및 검색에 필요한 평문 정보를 포함하는 외부 계층.
- 클라이언트 인증을 처리하는 중간 계층.
- 실제 LS2 데이터를 포함하는 내부 계층.

전체 형식은 다음과 같습니다::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

암호화된 LS2는 블라인드 처리됩니다. Destination은 헤더에 포함되지 않습니다. DHT 저장 위치는 SHA-256(sig type || blinded public key)이며, 매일 순환됩니다.

위에서 지정된 표준 LS2 헤더를 사용하지 않습니다.

#### Layer 0 (outer)

유형

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Blinded Public Key 서명 유형

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

블라인드 공개 키

    Length as implied by sig type

게시 타임스탬프

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

만료

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

플래그

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

임시 키 데이터

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

서명

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

플래그

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH 클라이언트 인증 데이터

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

PSK 클라이언트 인증 데이터

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

유형

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

데이터

    LeaseSet2 data for the given type.

    Includes the header and signature.


### 새로운 암호화 문제

다음은 Ed25519와 [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)를 기반으로 한 키 블라인딩 방식입니다. Re25519 서명은 Ed25519 곡선을 사용하며, 해시에는 SHA-512를 사용합니다.

[Tor의 rend-spec-v3.txt 부록 A.2](https://spec.torproject.org/rend-spec-v3)는 유사한 설계 목표를 가지고 있지만, 우리는 이를 사용하지 않습니다. 이는 해당 방식의 블라인드 공개 키가 소수 차수 부분군(prime-order subgroup)에서 벗어날 수 있으며, 이로 인한 보안상의 영향이 불분명하기 때문입니다.

#### Goals

- 블라인드되지 않은 목적지의 서명 공개 키는
  Ed25519 (sig type 7) 또는 Red25519 (sig type 11)이어야 함;
  다른 sig type은 지원되지 않음
- 서명 공개 키가 오프라인인 경우, 임시 서명 공개 키도 Ed25519여야 함
- 블라인딩은 계산상 단순함
- 기존 암호화 기본 요소 사용
- 블라인드된 공개 키는 블라인드 해제될 수 없음
- 블라인드된 공개 키는 Ed25519 곡선과 소수 차수 부분군에 있어야 함
- 블라인드된 공개 키를 도출하기 위해 목적지의 서명 공개 키를
  알아야 함 (전체 목적지는 필요하지 않음)
- 선택적으로 블라인드된 공개 키를 도출하는 데 필요한 추가 비밀 제공

#### Security

블라인딩 방식의 보안성을 위해서는 alpha의 분포가 블라인드되지 않은 개인 키와 동일해야 합니다. 그러나 Ed25519 개인 키(sig type 7)를 Red25519 개인 키(sig type 11)로 블라인드할 때 분포가 달라집니다. [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)의 요구사항을 충족하기 위해, Red25519(sig type 11)를 블라인드되지 않은 키에도 사용해야 "재무작위화된 공개 키와 해당 키 하에서의 서명이 재무작위화된 원래 키를 노출하지 않도록" 할 수 있습니다. 기존 destination에 대해서는 type 7을 허용하지만, 암호화될 새로운 destination에 대해서는 type 11을 권장합니다.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

알파

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

새로운 비밀 알파와 블라인드 키들은 매일 (UTC) 생성되어야 합니다. 비밀 알파와 블라인드 키들은 다음과 같이 계산됩니다.

GENERATE_ALPHA(destination, date, secret), 모든 당사자에 대해:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY(), leaseset을 게시하는 소유자용:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY(), leaseset을 검색하는 클라이언트들을 위해:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
두 방법으로 계산한 A' 값은 요구사항에 따라 동일한 결과를 산출합니다.

#### Signing

블라인딩되지 않은 leaseSet은 평소와 같이 블라인딩되지 않은 Ed25519 또는 Red25519 서명 개인키로 서명되고, 블라인딩되지 않은 Ed25519 또는 Red25519 서명 공개키(sig 유형 7 또는 11)로 검증됩니다.

서명 공개 키가 오프라인 상태인 경우, unblinded leaseset은 unblinded transient Ed25519 또는 Red25519 서명 개인 키로 서명되고 일반적인 방식대로 unblinded Ed25519 또는 Red25519 transient 서명 공개 키(sig types 7 또는 11)로 검증됩니다. 암호화된 leaseset의 오프라인 키에 대한 추가 참고사항은 아래를 참조하십시오.

암호화된 leaseSet의 서명을 위해 우리는 블라인드 키로 서명하고 검증하기 위한 [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) 기반의 Red25519를 사용합니다. Red25519 서명은 해시를 위해 SHA-512를 사용하여 Ed25519 곡선 위에서 동작합니다.

Red25519는 아래에 명시된 사항을 제외하고는 표준 Ed25519와 동일합니다.

#### Sign/Verify Calculations

암호화된 leaseset의 외부 부분은 Red25519 키와 서명을 사용합니다.

Red25519는 Ed25519와 거의 동일합니다. 두 가지 차이점이 있습니다:

Red25519 개인키는 난수에서 생성된 후 위에서 정의된 L로 모듈로 축소되어야 합니다. Ed25519 개인키는 난수에서 생성된 후 바이트 0과 31에 비트 마스킹을 사용하여 "클램핑"됩니다. 이는 Red25519에서는 수행되지 않습니다. 위에서 정의된 GENERATE_ALPHA() 및 BLIND_PRIVKEY() 함수는 mod L을 사용하여 적절한 Red25519 개인키를 생성합니다.

Red25519에서 서명을 위한 r 계산은 추가적인 랜덤 데이터를 사용하며, 개인 키의 해시가 아닌 공개 키 값을 사용합니다. 랜덤 데이터로 인해 동일한 키로 동일한 데이터에 서명하더라도 모든 Red25519 서명은 서로 다릅니다.

서명:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
검증:

```text
// same as in Ed25519
```
### 참고사항

#### Derivation of subcredentials

블라인딩 과정의 일환으로, 암호화된 LS2가 해당 Destination의 서명 공개 키를 알고 있는 사람만 복호화할 수 있도록 보장해야 합니다. 전체 Destination은 필요하지 않습니다. 이를 위해 서명 공개 키에서 credential을 파생시킵니다:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
개인화 문자열은 자격 증명이 평범한 Destination 해시와 같은 DHT 조회 키로 사용되는 어떤 해시와도 충돌하지 않도록 보장합니다.

주어진 블라인드 키에 대해, 우리는 서브크리덴셜을 도출할 수 있습니다:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
subcredential은 아래의 키 유도 과정에 포함되며, 이는 해당 키들을 Destination의 서명 공개 키에 대한 지식에 바인딩합니다.

#### Layer 1 encryption

먼저, 키 유도 프로세스의 입력이 준비됩니다:

```text
outerInput = subcredential || publishedTimestamp
```
다음으로, 무작위 솔트(salt)가 생성됩니다:

```text
outerSalt = CSRNG(32)
```
그런 다음 레이어 1을 암호화하는 데 사용되는 키가 도출됩니다:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
마지막으로, 레이어 1 평문이 암호화되고 직렬화됩니다:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

salt는 레이어 1 암호문에서 파싱됩니다:

```text
outerSalt = outerCiphertext[0:31]
```
그런 다음 레이어 1을 암호화하는 데 사용되는 키가 도출됩니다:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
마지막으로, 레이어 1 암호문이 복호화됩니다:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

클라이언트 인증이 활성화된 경우, ``authCookie``는 아래 설명된 대로 계산됩니다. 클라이언트 인증이 비활성화된 경우, ``authCookie``는 길이가 0인 바이트 배열입니다.

암호화는 레이어 1과 유사한 방식으로 진행됩니다:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

클라이언트 인증이 활성화된 경우, ``authCookie``는 아래에 설명된 대로 계산됩니다. 클라이언트 인증이 비활성화된 경우, ``authCookie``는 길이가 0인 바이트 배열입니다.

복호화는 레이어 1과 유사한 방식으로 진행됩니다:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### 암호화된 LS2

Destination에 대해 클라이언트 인증이 활성화되면, 서버는 암호화된 LS2 데이터를 복호화할 수 있도록 승인하는 클라이언트들의 목록을 유지합니다. 클라이언트별로 저장되는 데이터는 인증 메커니즘에 따라 달라지며, 각 클라이언트가 생성하여 보안이 확보된 대역 외 메커니즘을 통해 서버에 전송하는 어떤 형태의 키 자료를 포함합니다.

클라이언트별 인증을 구현하는 두 가지 대안이 있습니다:

#### DH client authorization

각 클라이언트는 DH 키쌍 ``[csk_i, cpk_i]``를 생성하고, 공개키 ``cpk_i``를 서버에 전송합니다.

서버 처리
^^^^^^^^^^^^^^^^^

서버는 새로운 ``authCookie``와 임시 DH 키페어를 생성합니다:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
그런 다음 각 인증된 클라이언트에 대해 서버는 ``authCookie``를 해당 공개 키로 암호화합니다:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
서버는 각 ``[clientID_i, clientCookie_i]`` 튜플을 ``epk``와 함께 암호화된 LS2의 레이어 1에 배치합니다.

클라이언트 처리
^^^^^^^^^^^^^^^^^

클라이언트는 자신의 개인 키를 사용하여 예상되는 클라이언트 식별자 ``clientID_i``, 암호화 키 ``clientKey_i``, 그리고 암호화 IV ``clientIV_i``를 도출합니다:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
그런 다음 클라이언트는 레이어 1 인증 데이터에서 ``clientID_i``를 포함하는 항목을 검색합니다. 일치하는 항목이 존재하면, 클라이언트는 이를 복호화하여 ``authCookie``를 얻습니다:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

각 클라이언트는 32바이트 비밀 키 ``psk_i``를 생성하고 이를 서버에 전송합니다. 또는 서버가 비밀 키를 생성하여 하나 이상의 클라이언트에게 전송할 수도 있습니다.

서버 처리
^^^^^^^^^^^^^^^^^

서버는 새로운 ``authCookie``와 salt를 생성합니다:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
그런 다음 인증된 각 클라이언트에 대해, 서버는 ``authCookie``를 해당 클라이언트의 사전 공유 키로 암호화합니다:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
서버는 각 ``[clientID_i, clientCookie_i]`` 튜플을 ``authSalt``와 함께 암호화된 LS2의 레이어 1에 배치합니다.

클라이언트 처리
^^^^^^^^^^^^^^^^^

클라이언트는 사전 공유 키를 사용하여 예상되는 클라이언트 식별자 ``clientID_i``, 암호화 키 ``clientKey_i``, 그리고 암호화 IV ``clientIV_i``를 도출합니다:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
그러면 클라이언트는 ``clientID_i``를 포함하는 항목에 대해 레이어 1 인증 데이터를 검색합니다. 일치하는 항목이 존재하면 클라이언트는 이를 복호화하여 ``authCookie``를 얻습니다:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

위의 두 클라이언트 인증 메커니즘 모두 클라이언트 멤버십에 대한 프라이버시를 제공합니다. Destination만 알고 있는 엔티티는 언제든지 구독 중인 클라이언트 수를 볼 수 있지만, 어떤 클라이언트가 추가되거나 해지되고 있는지는 추적할 수 없습니다.

서버는 암호화된 LS2를 생성할 때마다 클라이언트 순서를 무작위화해야 하며(SHOULD), 이는 클라이언트가 목록에서 자신의 위치를 알아내어 다른 클라이언트가 추가되거나 취소된 시점을 추론하는 것을 방지하기 위함입니다.

서버는 인증 데이터 목록에 임의의 항목을 삽입하여 구독한 클라이언트 수를 숨기는 것을 선택할 수 있습니다.

DH 클라이언트 인증의 장점
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 이 방식의 보안은 클라이언트 키 자료의 대역 외 교환에만 의존하지 않습니다. 클라이언트의 개인 키는 해당 장치를 떠날 필요가 없으므로, 대역 외 교환을 가로챌 수 있지만 DH 알고리즘을 깰 수 없는 공격자는 암호화된 LS2를 복호화하거나 클라이언트에게 부여된 접근 시간을 알아낼 수 없습니다.

DH 클라이언트 인증의 단점
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- N명의 클라이언트에 대해 서버 측에서 N + 1번의 DH 연산이 필요합니다.
- 클라이언트 측에서 1번의 DH 연산이 필요합니다.
- 클라이언트가 비밀 키를 생성해야 합니다.

PSK 클라이언트 인증의 장점 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - DH 연산이 필요하지 않습니다. - 서버가 비밀 키를 생성할 수 있습니다. - 원한다면 서버가 여러 클라이언트와 동일한 키를 공유할 수 있습니다.

PSK 클라이언트 인증의 단점
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 이 방식의 보안은 클라이언트 키 자료의 대역 외 교환에 결정적으로 의존합니다. 특정 클라이언트에 대한 교환을 가로챈 공격자는 해당 클라이언트가 인증된 모든 후속 암호화된 LS2를 해독할 수 있으며, 클라이언트의 액세스가 언제 취소되는지도 파악할 수 있습니다.

### 정의

제안서 149를 참조하세요.

비트토렌트에서는 암호화된 LS2를 사용할 수 없습니다. 32바이트인 컴팩트 announce 응답 때문입니다. 이 32바이트에는 해시만 포함되어 있습니다. leaseset이 암호화되어 있다는 표시나 서명 유형을 위한 공간이 없습니다.

### 형식

오프라인 키를 사용하는 암호화된 leaseSet의 경우, blinded 개인 키도 오프라인에서 생성되어야 하며, 매일 하나씩 생성해야 합니다.

암호화된 leaseset의 평문 부분에 선택적 오프라인 서명 블록이 있기 때문에, floodfill을 스크래핑하는 누구든지 이를 사용하여 며칠에 걸쳐 leaseset을 추적할 수 있습니다(하지만 복호화는 할 수 없음). 이를 방지하기 위해 키 소유자는 매일 새로운 임시 키도 생성해야 합니다. 임시 키와 블라인드 키 모두 미리 생성할 수 있으며, 일괄적으로 router에 전달할 수 있습니다.

이 제안서에서는 여러 개의 transient key와 blinded key를 패키징하여 클라이언트나 router에 제공하기 위한 파일 형식이 정의되지 않았습니다. 또한 이 제안서에서는 오프라인 키를 사용한 암호화된 leaseSet을 지원하기 위한 I2CP 프로토콜 확장도 정의되지 않았습니다.

### Notes

- 암호화된 leaseSet을 사용하는 서비스는 암호화된 버전을 floodfill에 게시합니다. 하지만 효율성을 위해, 인증된 후에는 (예: 화이트리스트를 통해) 래핑된 garlic 메시지에서 클라이언트에게 암호화되지 않은 leaseSet을 전송합니다.

- Floodfill은 남용을 방지하기 위해 최대 크기를 합리적인 값으로 제한할 수 있습니다.

- 복호화 후에는 내부 타임스탬프와 만료 시간이 최상위 레벨의 것과 일치하는지 등 여러 검사를 수행해야 합니다.

- ChaCha20이 AES 대신 선택되었습니다. AES 하드웨어 지원이 가능한 경우 속도는 비슷하지만, 저사양 ARM 기기와 같이 AES 하드웨어 지원이 없는 경우 ChaCha20이 2.5-3배 더 빠릅니다.

- 우리는 키 기반 BLAKE2b를 사용할 만큼 속도에 신경 쓰지 않습니다. BLAKE2b는 우리가 필요로 하는 가장 큰 n을 수용할 수 있을 만큼 충분히 큰 출력 크기를 가지고 있습니다 (또는 카운터 인수와 함께 원하는 키마다 한 번씩 호출할 수 있습니다). BLAKE2b는 SHA-256보다 훨씬 빠르며, 키 기반 BLAKE2b는 해시 함수 호출의 총 수를 줄일 수 있습니다.
  하지만 제안 148을 참조하세요. 여기서는 다른 이유로 BLAKE2b로 전환할 것을 제안하고 있습니다.
  [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html)를 참조하세요.

### Meta LS2

이는 멀티호밍을 대체하는 데 사용됩니다. 다른 leaseSet과 마찬가지로 이는 생성자에 의해 서명됩니다. 이는 목적지 해시의 인증된 목록입니다.

Meta LS2는 트리 구조의 최상위 노드이며, 경우에 따라서는 중간 노드이기도 합니다. 이는 여러 개의 항목을 포함하고 있으며, 각 항목은 대규모 멀티호밍을 지원하기 위해 LS, LS2, 또는 다른 Meta LS2를 가리킵니다. Meta LS2는 LS, LS2, 그리고 Meta LS2 항목들을 혼합해서 포함할 수 있습니다. 트리의 잎 노드는 항상 LS 또는 LS2입니다. 이 트리는 DAG(방향성 비순환 그래프)이며, 루프는 금지되어 있습니다. 검색을 수행하는 클라이언트는 반드시 루프를 감지하고 루프를 따라가기를 거부해야 합니다.

Meta LS2는 표준 LS 또는 LS2보다 훨씬 긴 만료 시간을 가질 수 있습니다. 최상위 레벨은 발행 날짜로부터 몇 시간 후에 만료될 수 있습니다. 최대 만료 시간은 floodfill과 클라이언트에 의해 강제되며, 이는 미정입니다.

Meta LS2의 사용 사례는 대규모 멀티호밍이지만, 라우터와 leaseSet 간의 상관관계에 대한 보호(라우터 재시작 시)는 현재 LS 또는 LS2로 제공되는 것 이상은 없습니다. 이는 상관관계 보호가 필요하지 않을 수도 있는 "facebook" 사용 사례와 동등합니다. 이 사용 사례는 오프라인 키가 필요할 것으로 보이며, 이는 트리의 각 노드에서 표준 헤더로 제공됩니다.

leaf router들, 중간 및 master Meta LS 서명자들 간의 조정을 위한 백엔드 프로토콜은 여기서 명시되지 않습니다. 요구사항은 매우 간단합니다 - 피어가 작동 중인지 확인하고, 몇 시간마다 새로운 LS를 게시하는 것입니다. 유일한 복잡성은 장애 시 최상위 레벨 또는 중간 레벨 Meta LS들을 위한 새로운 게시자를 선택하는 것입니다.

여러 라우터의 lease들을 결합하고 서명하여 단일 leaseset에 게시하는 혼합-매칭 leaseSet은 제안서 140 "invisible multihoming"에 문서화되어 있습니다. 이 제안서는 작성된 대로는 실행 불가능한데, 스트리밍 연결이 단일 라우터에 "sticky"하지 않기 때문입니다. http://zzz.i2p/topics/2335 를 참조하세요.

백엔드 프로토콜과 router 및 클라이언트 내부와의 상호작용은 보이지 않는 멀티호밍에 대해 상당히 복잡할 것입니다.

최상위 Meta LS에 대한 floodfill의 과부하를 방지하기 위해, 만료 시간은 최소 몇 시간으로 설정해야 합니다. 클라이언트는 최상위 Meta LS를 캐시해야 하며, 만료되지 않은 경우 재시작 후에도 이를 유지해야 합니다.

클라이언트가 트리를 탐색할 수 있도록 하는 알고리즘을 정의해야 하며, 여기에는 폴백 기능도 포함되어야 사용량이 분산될 수 있습니다. 해시 거리, 비용, 무작위성의 함수 형태가 되어야 합니다. 노드가 LS 또는 LS2와 Meta LS를 모두 가지고 있는 경우, 언제 해당 leaseSet들을 사용할 수 있는지, 그리고 언제 트리 탐색을 계속해야 하는지 알아야 합니다.

다음으로 조회

    Standard LS flag (1)
저장 위치

    Meta LS2 type (7)
다음 위치에 저장:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
일반적인 만료

    Hours. Max 18.2 hours (65535 seconds)
게시자

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
플래그 및 속성: 향후 사용을 위해

### Blinding Key 유도

- 이 서비스를 사용하는 분산 서비스는 서비스 목적지의 개인 키를 가진 하나 이상의 "마스터"를 갖게 됩니다. 이들은 (대역 외에서) 현재 활성 목적지 목록을 결정하고 Meta LS2를 게시합니다. 중복성을 위해 여러 마스터가 멀티홈(즉, 동시에 게시)으로 Meta LS2를 게시할 수 있습니다.

- 분산 서비스는 단일 destination으로 시작하거나 구식 멀티호밍을 사용한 다음, Meta LS2로 전환할 수 있습니다. 표준 LS 조회는 LS, LS2, 또는 Meta LS2 중 하나를 반환할 수 있습니다.

- 서비스가 Meta LS2를 사용할 때는 터널(lease)이 없습니다.

### Service Record

이는 목적지가 서비스에 참여하고 있다는 개별 레코드입니다. 참여자에서 floodfill로 전송됩니다. floodfill에서 개별적으로 전송되지는 않으며, 오직 Service List의 일부로만 전송됩니다. Service Record는 만료 시간을 0으로 설정하여 서비스 참여를 철회하는 데에도 사용됩니다.

이것은 LS2가 아니지만 표준 LS2 헤더와 서명 형식을 사용합니다.

다음으로 조회

    n/a, see Service List
저장하기

    Service Record type (9)
다음 위치에 저장:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
일반적인 만료

    Hours. Max 18.2 hours (65535 seconds)
게시자

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- expires가 모두 0이면, floodfill은 해당 레코드를 취소하고 더 이상 서비스 목록에 포함하지 않아야 합니다.

- Storage: floodfill은 이러한 레코드의 저장을 엄격하게 제한하고 해시당 저장되는 레코드 수와 만료 시간을 제한할 수 있습니다. 해시의 화이트리스트도 사용될 수 있습니다.

- 동일한 해시에서 다른 netdb 타입이 우선순위를 가지므로, 서비스 레코드는 LS/RI를 덮어쓸 수 없지만, LS/RI는 해당 해시의 모든 서비스 레코드를 덮어씁니다.

### Service List

이것은 LS2와는 전혀 다르며 다른 형식을 사용합니다.

서비스 목록은 floodfill에 의해 생성되고 서명됩니다. 누구나 floodfill에 Service Record를 게시하여 서비스에 참여할 수 있다는 점에서 인증되지 않은 방식입니다.

서비스 목록에는 전체 서비스 레코드가 아닌 단축 서비스 레코드가 포함됩니다. 이들은 서명을 포함하지만 전체 destination이 아닌 해시만 포함하므로, 전체 destination 없이는 검증할 수 없습니다.

서비스 목록의 보안성(있다면)과 바람직성은 아직 결정되지 않았습니다. Floodfill들은 서비스의 화이트리스트로 발행과 조회를 제한할 수 있지만, 해당 화이트리스트는 구현이나 운영자의 선호도에 따라 달라질 수 있습니다. 구현들 간에 공통적이고 기본적인 화이트리스트에 대한 합의를 달성하는 것은 불가능할 수도 있습니다.

위의 서비스 레코드에 서비스 이름이 포함되어 있다면 floodfill 운영자들이 이의를 제기할 수 있습니다. 해시만 포함되어 있다면 검증이 없으므로, 서비스 레코드가 다른 netDb 유형보다 먼저 "들어가서" floodfill에 저장될 수 있습니다.

다음으로 조회

    Service List lookup type (11)
저장 위치

    Service List type (11)
다음 위치에 저장:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
일반적인 만료

    Hours, not specified in the list itself, up to local policy
게시자

    Nobody, never sent to floodfill, never flooded.

### Format

위에서 명시한 표준 LS2 헤더를 사용하지 않습니다.

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
서비스 목록의 서명을 검증하려면:

- 서비스 이름의 해시를 앞에 추가
- 생성자의 해시를 제거
- 수정된 내용의 서명을 확인

각 Short Service Record의 서명을 검증하려면:

- 목적지 가져오기
- 서명 확인 (게시된 타임스탬프 + 만료 시간 + 플래그 + 포트 + 서비스 이름의 해시)

각 철회 기록(Revocation Record)의 서명을 검증하려면:

- 목적지 가져오기
- 서명 확인 (게시된 타임스탬프 + 4개의 zero 바이트 + flags + port + 서비스 이름의 Hash)

### Notes

- 알 수 없는 signature 유형을 지원할 수 있도록 sig type 대신 signature length를 사용합니다.

- 서비스 목록에는 만료가 없으며, 수신자는 정책이나 개별 레코드의 만료를 기반으로 자체적으로 결정할 수 있습니다.

- Service Lists는 플러딩되지 않으며, 개별 Service Records만 플러딩됩니다. 각 floodfill은 Service List를 생성하고, 서명하고, 캐시합니다. floodfill은 캐시 시간과 서비스 및 철회 레코드의 최대 개수에 대해 자체 정책을 사용합니다.

## Common Structures Spec Changes Required

### 암호화 및 처리

이 제안의 범위를 벗어남. ECIES 제안 144 및 145에 추가할 것.

### New Intermediate Structures

Lease2, MetaLease, LeaseSet2Header, OfflineSignature에 대한 새로운 구조를 추가합니다. 릴리스 0.9.38부터 적용됩니다.

### New NetDB Types

위 내용에서 각 새로운 leaseset 유형에 대한 구조를 추가합니다. LeaseSet2, EncryptedLeaseSet, MetaLeaseSet의 경우 릴리스 0.9.38부터 적용됩니다. Service Record와 Service List의 경우 예비 단계이며 일정이 미정입니다.

### New Signature Type

RedDSA_SHA512_Ed25519 타입 11을 추가합니다. 공개 키는 32바이트, 개인 키는 32바이트, 해시는 64바이트, 서명은 64바이트입니다.

## Encryption Spec Changes Required

이 제안의 범위를 벗어남. 제안서 144 및 145를 참조하세요.

## I2NP Changes Required

참고 사항: LS2는 최소 버전 이상의 floodfill에만 게시할 수 있습니다.

### Database Lookup Message

서비스 목록 조회 유형을 추가합니다.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### 클라이언트별 인증

모든 새로운 저장소 유형을 추가합니다.

### Changes

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP Changes Required

### I2CP Options

router 측에서 해석되는 새로운 옵션들, SessionConfig Mapping으로 전송됨:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
클라이언트 측에서 해석되는 새로운 옵션들:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session Config

오프라인 서명의 경우, i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, i2cp.leaseSetOfflineSignature 옵션이 필요하며, 서명은 임시 서명 개인키로 수행됩니다.

### Base 32 주소를 사용한 암호화된 LS

라우터에서 클라이언트로. 변경 사항 없음. 반환되는 leaseSet이 4바이트 타임스탬프를 가진 LS2이더라도 lease들은 8바이트 타임스탬프와 함께 전송됩니다. 응답은 Create Leaseset 또는 Create Leaseset2 메시지일 수 있음을 참고하세요.

### 오프라인 키를 사용한 암호화된 LS

Router에서 client로. 변경사항 없음. 반환되는 leaseset이 4바이트 타임스탬프를 가진 LS2일지라도, lease들은 8바이트 타임스탬프와 함께 전송됩니다. 응답은 Create Leaseset 또는 Create Leaseset2 메시지일 수 있음에 유의하세요.

### 참고사항

클라이언트에서 라우터로. Create Leaseset Message를 대신하여 사용할 새로운 메시지.

### Meta LS2

- 라우터가 저장 타입을 파싱하려면, 세션 설정에서 라우터에 미리 전달되지 않는 한 타입이 메시지에 포함되어야 합니다.
  일반적인 파싱 코드의 경우, 메시지 자체에 포함하는 것이 더 쉽습니다.

- 라우터가 개인키의 타입과 길이를 알기 위해서는,
  파서가 세션 설정에서 미리 타입을 알고 있지 않는 한
  개인키가 lease set 다음에 와야 합니다.
  공통 파싱 코드의 경우, 메시지 자체에서 이를 아는 것이 더 쉽습니다.

- 이전에 폐기용으로 정의되었지만 사용되지 않았던 서명 개인키는
  LS2에 존재하지 않습니다.

### 형식

Create Leaseset2 메시지의 메시지 타입은 41입니다.

### 참고사항

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### 서비스 기록

- 최소 라우터 버전은 0.9.39입니다.
- 메시지 타입 40을 사용한 예비 버전이 0.9.38에 있었지만 형식이 변경되었습니다.
  타입 40은 폐기되었으며 지원되지 않습니다.

### 형식

- 암호화된 LS와 메타 LS를 지원하기 위해 더 많은 변경사항이 필요합니다.

### 참고사항

클라이언트에서 라우터로. 새 메시지.

### 서비스 목록

- 라우터는 목적지가 블라인드 처리되어 있는지 알아야 합니다.
  만약 블라인드 처리되어 있고 시크릿 또는 클라이언트별 인증을 사용한다면,
  해당 정보도 함께 가지고 있어야 합니다.

- 새로운 형식의 b32 주소("b33")에 대한 Host Lookup은
  라우터에게 해당 주소가 블라인드 처리되었음을 알려주지만, Host Lookup 메시지에서
  시크릿이나 개인 키를 라우터에 전달할 메커니즘이 없습니다.
  Host Lookup 메시지를 확장하여 해당 정보를 추가할 수도 있지만,
  새로운 메시지를 정의하는 것이 더 깔끔합니다.

- 클라이언트가 router에게 알려줄 수 있는 프로그래밍적 방법이 필요합니다.
  그렇지 않으면 사용자가 각 destination을 수동으로 구성해야 합니다.

### 형식

클라이언트가 blinded destination에 메시지를 보내기 전에, Host Lookup 메시지에서 "b33"을 조회하거나 Blinding Info 메시지를 보내야 합니다. blinded destination에 비밀 키 또는 클라이언트별 인증이 필요한 경우, 클라이언트는 Blinding Info 메시지를 보내야 합니다.

router는 이 메시지에 대한 응답을 보내지 않습니다.

### 참고사항

Blinding Info Message의 메시지 타입은 42입니다.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### 키 인증서

- 최소 라우터 버전은 0.9.43입니다

### 새로운 중간 구조체

### 새로운 NetDB 타입

"b33" 호스트명의 조회를 지원하고 router가 필요한 정보를 가지고 있지 않은 경우 표시를 반환하기 위해, Host Reply Message에 대한 추가 결과 코드를 다음과 같이 정의합니다:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
1-255 값들은 이미 오류로 정의되어 있으므로, 역방향 호환성 문제는 없습니다.

### 새로운 서명 유형

라우터에서 클라이언트로. 새 메시지.

### Justification

클라이언트는 주어진 해시가 Meta LS로 해석될 것이라는 것을 사전에 알 수 없습니다.

Destination에 대한 leaseSet 조회가 Meta LS를 반환하면, router는 재귀 해결을 수행합니다. 데이터그램의 경우 클라이언트 측에서 알 필요가 없지만, SYN ACK에서 프로토콜이 destination을 확인하는 스트리밍의 경우 "실제" destination이 무엇인지 알아야 합니다. 따라서 새로운 메시지가 필요합니다.

### Usage

router는 메타 LS에서 사용되는 실제 목적지에 대한 캐시를 유지합니다. 클라이언트가 메타 LS로 해석되는 목적지에 메시지를 보낼 때, router는 마지막으로 사용된 실제 목적지에 대한 캐시를 확인합니다. 캐시가 비어있으면, router는 메타 LS에서 목적지를 선택하고 leaseSet을 조회합니다. leaseSet 조회가 성공하면, router는 해당 목적지를 캐시에 추가하고 클라이언트에게 Meta Redirect Message를 보냅니다. 이는 목적지가 만료되어 변경되어야 하는 경우가 아닌 한 한 번만 수행됩니다. 클라이언트도 필요한 경우 정보를 캐시해야 합니다. Meta Redirect Message는 모든 SendMessage에 대한 응답으로 전송되지 않습니다.

라우터는 버전 0.9.47 이상의 클라이언트에게만 이 메시지를 보냅니다.

클라이언트는 이 메시지에 대한 응답을 보내지 않습니다.

### 데이터베이스 조회 메시지

Meta Redirect Message의 메시지 타입은 43입니다.

### 변경사항

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### 데이터베이스 저장 메시지

Meta를 생성하고 지원하는 방법(라우터 간 통신 및 조정 포함)은 이 제안의 범위를 벗어납니다. 관련 제안 150을 참조하세요.

### 변경사항

오프라인 서명은 스트리밍이나 응답 가능한 데이터그램에서 검증될 수 없습니다. 아래 섹션을 참조하세요.

## Private Key File Changes Required

개인 키 파일(eepPriv.dat) 형식은 우리 사양의 공식적인 부분은 아니지만 [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)에 문서화되어 있으며 다른 구현체들도 이를 지원합니다. 이를 통해 개인 키를 다른 구현체로 이식할 수 있습니다.

일시적 공개 키와 오프라인 서명 정보를 저장하기 위해 변경이 필요합니다.

### Changes

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### I2CP 옵션

다음 옵션들에 대한 지원을 추가하세요:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

오프라인 서명은 현재 스트리밍에서 검증할 수 없습니다. 아래 변경 사항은 오프라인 서명 블록을 옵션에 추가합니다. 이를 통해 I2CP를 통해 이 정보를 검색할 필요가 없어집니다.

### 세션 설정

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Request LeaseSet 메시지

- 대안으로는 플래그만 추가하고 I2CP를 통해 임시 공개 키를 검색하는 것입니다
  (위의 Host Lookup / Host Reply Message 섹션 참조)

## 표준 LS2 헤더

오프라인 서명은 응답 가능한 데이터그램 처리에서 검증할 수 없습니다. 오프라인 서명되었음을 나타내는 플래그가 필요하지만 플래그를 넣을 곳이 없습니다. 완전히 새로운 프로토콜 번호와 형식이 필요할 것입니다.

### Request Variable Leaseset Message

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Create Leaseset2 메시지

- 대안으로는 플래그만 추가하고, I2CP를 통해 임시 공개 키를 검색하는 방법이 있습니다
  (위의 Host Lookup / Host Reply Message 섹션 참조)
- 플래그 바이트를 사용할 수 있게 되었으니 지금 추가해야 할 다른 옵션이 있나요?

## SAM V3 Changes Required

SAM은 DESTINATION base 64에서 오프라인 서명을 지원하도록 개선되어야 합니다.

### 근거

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
오프라인 서명은 STREAM과 RAW에서만 지원되며, DATAGRAM에서는 지원되지 않습니다(새로운 DATAGRAM 프로토콜을 정의할 때까지).

SESSION STATUS는 모든 비트가 0인 서명 개인 키와 SESSION CREATE에서 제공된 것과 정확히 동일한 오프라인 서명 데이터를 반환한다는 점에 유의하세요.

DEST GENERATE와 SESSION CREATE DESTINATION=TRANSIENT는 오프라인 서명된 destination을 생성하는 데 사용할 수 없습니다.

### 메시지 유형

버전을 3.4로 올릴 것인지, 아니면 3.1/3.2/3.3으로 유지해서 모든 3.2/3.3 관련 요소들을 요구하지 않고도 추가할 수 있도록 할 것인지?

기타 변경 사항은 미정입니다. 위의 I2CP Host Reply Message 섹션을 참조하세요.

## BOB Changes Required

BOB는 오프라인 서명 및/또는 Meta LS를 지원하도록 개선되어야 합니다. 이는 우선순위가 낮으며 아마도 명세화되거나 구현되지 않을 것입니다. SAM V3가 선호되는 인터페이스입니다.

## Publishing, Migration, Compatibility

LS2 (암호화된 LS2 제외)는 LS1과 동일한 DHT 위치에 게시됩니다. LS2가 다른 위치에 있지 않은 이상, LS1과 LS2를 모두 게시할 방법은 없습니다.

암호화된 LS2는 블라인드된 키 타입과 키 데이터의 해시에 게시됩니다. 이 해시는 LS1에서와 같이 일일 "라우팅 키"를 생성하는 데 사용됩니다.

LS2는 새로운 기능이 필요한 경우에만 사용됩니다 (새로운 암호화, 암호화된 LS, 메타데이터 등). LS2는 지정된 버전 이상의 floodfill에만 게시할 수 있습니다.

LS2를 게시하는 서버는 연결하는 모든 클라이언트가 LS2를 지원한다는 것을 알 수 있습니다. 서버는 garlic encryption에 LS2를 보낼 수 있습니다.

클라이언트는 새로운 암호화를 사용하는 경우에만 garlic에서 LS2를 전송합니다. 공유 클라이언트는 LS1을 무기한 사용할까요? TODO: 이전 암호화와 새로운 암호화를 모두 지원하는 공유 클라이언트를 어떻게 구현할 수 있을까요?

## Rollout

0.9.38은 오프라인 키를 포함한 표준 LS2에 대한 floodfill 지원을 포함합니다.

0.9.39는 LS2 및 Encrypted LS2에 대한 I2CP 지원, sig type 11 서명/검증, Encrypted LS2에 대한 floodfill 지원(오프라인 키 없이 sig type 7 및 11), 그리고 LS2 암호화/복호화(클라이언트별 인증 없이)를 포함합니다.

0.9.40은 클라이언트별 인증을 통한 LS2 암호화/복호화 지원, Meta LS2에 대한 floodfill 및 I2CP 지원, 오프라인 키를 사용한 암호화된 LS2 지원, 그리고 암호화된 LS2에 대한 b32 지원을 포함할 예정입니다.

## 새로운 DatabaseEntry 타입

암호화된 LS2 설계는 유사한 설계 목표를 가졌던 [Tor의 v3 숨겨진 서비스 디스크립터](https://spec.torproject.org/rend-spec-v3)에 크게 영향을 받았습니다.
