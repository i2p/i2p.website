---
title: "새로운 netDB 항목"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "열기"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## 상태

이 제안의 일부는 완료되어 0.9.38 및 0.9.39 버전에 구현되었습니다.   공통 구조, I2CP, I2NP 및 기타 사양은   현재 지원되는 변경 사항을 반영하도록 업데이트되었습니다.

완료된 부분도 여전히 사소한 수정이 있을 수 있습니다.   이 제안의 다른 부분은 여전히 개발 중이며   상당한 수정이 있을 수 있습니다.

서비스 조회 (유형 9 및 11)는 우선순위가 낮으며   일정이 정해지지 않았으며, 별도의 제안으로 분리될 수 있습니다.

## 개요

이 문서는 다음 4개의 제안을 업데이트하고 통합한 것입니다:

- 110 LS2
- 120 대규모 멀티호밍을 위한 메타 LS2
- 121 암호화된 LS2
- 122 인증되지 않은 서비스 조회 (애니캐스팅)

이 제안들은 대부분 독립적이지만, 일관성을 위해   여러 제안에서 공통 형식을 정의하고 사용합니다.

다음 제안들은 다소 관련이 있습니다:

- 140 보이지 않는 멀티호밍 (이 제안과 불호환)
- 142 새로운 대칭 암호를 위한 새로운 암호 템플릿
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 암호화된 LS2를 위한 B32
- 150 마늘 농장 프로토콜
- 151 ECDSA 블라인딩

## 제안

이 제안은 5개의 새로운 DatabaseEntry 유형과   네트워크 데이터베이스에 저장하고 검색하는 절차,   그리고 서명하고 그 서명을 검증하는 방법을 정의합니다.

### 목표

- 하위 호환성 유지
- 기존 스타일의 멀티호밍에서도 LS2 사용 가능
- 지원을 위해 새로운 암호나 원시 요소가 필요하지 않음
- 암호와 서명의 분리 유지; 현재 및 미래 모든 버전 지원
- 선택적 오프라인 서명 키 지원
- 지문 추적을 줄이기 위해 타임스탬프 정확도 감소
- 목적지에 대한 새로운 암호화 지원
- 대규모 멀티호밍 지원
- 기존 암호화된 LS의 여러 문제 해결
- 플러드필이 볼 수 있는 가시성 감소를 위한 선택적 블라인딩
- 암호화된 LS는 단일 키와 여러 철회 가능한 키 모두 지원
- 아웃프록시, 애플리케이션 DHT 부트스트랩 등에서 더 쉬운 조회를 위한 서비스 조회
- 비트토런트 등 32바이트 이진 목적지 해시에 의존하는 기능을 깨뜨리지 않음
- 라우터정보에서처럼 속성을 통해 leaseset의 유연성 추가
- 내용이 암호화되어 있어도 작동하도록 게시 타임스탬프와 가변 만료를 헤더에 포함 (가장 이른 임대에서 타임스탬프를 유도하지 않음)
- 모든 새로운 유형은 기존 leaseset과 동일한 DHT 공간 및 위치에 존재하여, 사용자가 기존 LS에서 LS2로 마이그레이션하거나 LS2, 메타, 암호화된 LS2 간 전환 시 목적지나 해시를 변경하지 않아도 됨
- 기존 목적지를 오프라인 키로 전환하거나 다시 온라인 키로 전환할 때 목적지나 해시를 변경하지 않아도 됨

### 비목표 / 범위 외

- 새로운 DHT 회전 알고리즘 또는 공유 난수 생성
- 새로운 암호화 유형과 그 유형을 사용하는 종단 간 암호화 방식은 별도의 제안에 포함됨. 여기에서는 새로운 암호를 지정하거나 논의하지 않음
- RI 또는 터널 생성을 위한 새로운 암호화. 별도의 제안에 포함됨
- I2NP DLM / DSM / DSRM 메시지의 암호화, 전송, 수신 방법. 변경 없음
- 메타를 생성하고 지원하는 방법, 백엔드 라우터 간 통신, 관리, 장애 조치 및 조정 포함. I2CP, i2pcontrol 또는 새로운 프로토콜에 지원이 추가될 수 있음. 표준화 여부는 미정
- 장기간 만료되는 터널을 실제로 구현하고 관리하거나 기존 터널을 취소하는 방법. 매우 어렵고, 이를 없이는 합리적인 점진적 종료가 불가능함
- 위협 모델 변경
- 오프라인 저장 형식 또는 데이터 저장/검색/공유 방법
- 구현 세부 사항은 여기서 논의하지 않으며 각 프로젝트에 맡김

### 정당성

LS2는 암호화 유형 변경 및 향후 프로토콜 변경을 위한 필드를 추가합니다.

암호화된 LS2는 전체 임대 집합을 비대칭 암호화하여 기존 암호화된 LS의 여러 보안 문제를 해결합니다.

메타 LS2는 유연하고 효율적이며 효과적인 대규모 멀티호밍을 제공합니다.

서비스 레코드 및 서비스 목록은 이름 조회 및 DHT 부트스트래핑과 같은 애니캐스트 서비스를 제공합니다.

### NetDB 데이터 유형

유형 번호는 I2NP 데이터베이스 조회/저장 메시지에서 사용됩니다.

종단 간(end-to-end) 열은 마늘 메시지에서 목적지로 쿼리/응답이 전송되는지를 나타냅니다.

기존 유형:

| NetDB 데이터 | 조회 유형 | 저장 유형 |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| 탐색용     | 3           | DSRM       |
새로운 유형:

| NetDB 데이터     | 조회 유형 | 저장 유형 | 표준 LS2 헤더? | 종단 간 전송? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | 예               | 예               |
| 암호화된 LS2   | 1           | 5          | 아니오            | 아니오            |
| 메타 LS2       | 1           | 7          | 예               | 아니오            |
| 서비스 레코드  | n/a         | 9          | 예               | 아니오            |
| 서비스 목록    | 4           | 11         | 아니오            | 아니오            |
### 참고 사항

- 조회 유형은 현재 데이터베이스 조회 메시지의 비트 3-2에 사용됩니다. 추가 유형은 비트 4를 사용해야 합니다.

- 이전 라우터는 데이터베이스 저장 메시지 유형 필드의 상위 비트를 무시하므로 모든 저장 유형은 홀수입니다. RI 압축 형식보다 LS로 파싱이 실패하는 것이 더 낫습니다.

- 서명이 적용되는 데이터에서 유형이 명시적, 암시적, 아니면 둘 다 아닌지 여부?

### 조회/저장 절차

유형 3, 5, 7은 표준 leaseset 조회(유형 1)에 대한 응답으로 반환될 수 있습니다.   유형 9는 조회에 대한 응답으로 절대 반환되지 않습니다.   유형 11은 새로운 서비스 조회 유형(유형 11)에 대한 응답으로 반환됩니다.

클라이언트 간 마늘 메시지에는 유형 3만 전송될 수 있습니다.

### 형식

유형 3, 7, 9는 모두 다음 공통 형식을 사용합니다::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
표준 LS2 헤더

유형별 부분

### 개인정보/보안 고려사항

표준 LS2 서명:

## 표준 LS2 헤더

유형 5(암호화된)는 목적지로 시작하지 않으며 다른 형식을 가집니다. 아래 참조.

### 형식

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
### 정당성

  - 아래에 정의됨

  - 아래 각 부분에 정의됨

  - 서명 키의 서명 유형에 따라 암시되는 길이

- 게시되지 않음/게시됨: 종단 간 데이터베이스 저장을 보낼 때, 보내는 라우터가 이 leaseset을 다른 사람에게 보내지 않도록 표시하려 할 수 있음. 현재는 이 상태를 유지하기 위해 휴리스틱을 사용하고 있음.

### 문제점

- 게시됨: leaseset의 '버전'을 결정하기 위해 필요한 복잡한 논리를 대체함. 현재 버전은 가장 늦게 만료되는 임대의 만료 시간이며, 게시 라우터는 오래된 임대만 제거하는 leaseset을 게시할 때 최소 1ms 이상 만료 시간을 증가시켜야 함.

- 만료: netdb 항목의 만료를 마지막으로 만료되는 leaseset보다 일찍 설정할 수 있음. LS2에서는 leaseset이 11분 최대 만료로 유지될 것으로 예상되므로 유용하지 않을 수 있지만, 다른 새로운 유형(아래 메타 LS 및 서비스 레코드 참조)에서는 필요함.

- 오프라인 키는 초기/필수 구현 복잡성을 줄이기 위해 선택 사항임.

### 참고 사항

- 타임스탬프 정확도를 더 줄일 수 있음 (10분?) 하지만 버전 번호를 추가해야 함. 이는 멀티호밍을 깰 수 있음. 순서 보존 암호화가 없으면 타임스탬프 없이도 할 수 없음.

- 대안: 3바이트 타임스탬프 (에포크 / 10분), 1바이트 버전, 2바이트 만료

- 유형이 데이터/서명에서 명시적 또는 암시적인가? 서명을 위한 "도메인" 상수?

## 새로운 DatabaseEntry 유형

### LeaseSet 2

유형 11(서비스 목록)은 여러 서비스 레코드의 집합이며 다른 형식을 가집니다. 아래 참조.

- 라우터는 1초에 한 번 이상 LS를 게시해서는 안 됩니다.  
  만약 그렇게 한다면, 이전에 게시된 LS보다 게시 타임스탬프를 인위적으로 1초 증가시켜야 합니다.

TBD

    Standard LS flag (1)
유형 3, 7, 9는 아래에 명시된 표준 LS2 헤더를 사용합니다:

    Standard LS2 type (3)
기존 LeaseSet과의 변경 사항:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
조회:

    10 minutes, as in a regular LS.
저장:

    Destination

### 형식

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
### 정당성

- 라우터 구현은 검증을 매번 하지 않도록 일시적 키와 서명을 캐시할 수 있습니다. 특히 플러드필과 장기간 연결의 양 끝에 있는 라우터가 이로부터 이득을 볼 수 있습니다.

- 오프라인 키와 서명은 장기간 존재하는 목적지(즉, 서버)에만 적합하며, 클라이언트에는 적합하지 않습니다.

### 논의

저장 위치:

일반적인 만료:

게시자:

- 게시 타임스탬프, 만료 타임스탬프, 플래그 및 속성 추가
- 암호화 유형 추가
- 철회 키 제거

이 제안은 종단 간 암호화 키로 leaseset의 공개 키를 계속 사용하며, 현재와 마찬가지로 목적지의 공개 키 필드는 사용하지 않습니다. 목적지 키 인증서에는 암호화 유형이 지정되지 않으며, 0으로 유지됩니다.

- 속성: 향후 확장성과 유연성. 나머지 데이터 파싱에 필요할 수 있으므로 먼저 배치됨.

### 새로운 암호화 문제

거부된 대안은 목적지 키 인증서에 암호화 유형을 지정하고, 목적지의 공개 키를 사용하며, leaseset의 공개 키를 사용하지 않는 것입니다. 우리는 이를 계획하지 않습니다.

- 여러 암호화 유형/공개 키 쌍은 새로운 암호화 유형으로의 전환을 용이하게 함. 다른 방법은 DSA 및 EdDSA 목적지를 위해 현재 수행하는 것처럼 동일한 터널을 사용하여 여러 leaseset을 게시하는 것임. 터널에서 들어오는 암호화 유형의 식별은 기존 세션 태그 메커니즘과/또는 각 키를 사용한 시험적 복호화로 수행할 수 있음. 들어오는 메시지의 길이도 단서를 제공할 수 있음.

- 실제 공개 키의 위치가 변경되지 않음
- 목적지를 변경하지 않고도 암호화 유형이나 공개 키를 변경할 수 있음
- 사용되지 않는 철회 필드 제거
- 이 제안의 다른 DatabaseEntry 유형과의 기본 호환성
- 여러 암호화 유형 허용

- 공개 키 및 암호화 유형의 위치가 RouterInfo와 다름
- leaseset에서 사용되지 않는 공개 키 유지
- 네트워크 전체에서 구현 필요; 대안으로, 실험적 암호화 유형을 허용하는 플러드필이 허용하는 경우 실험적 암호화 유형을 사용할 수 있음 (실험적 서명 유형 지원에 관한 관련 제안 136 및 137 참조). 대안 제안은 실험적 암호화 유형에 대해 구현하고 테스트하기 더 쉬울 수 있음.

### 참고 사항

- 암호화 유형은 곡선, 키 길이, 종단 간 방식을 포함한 조합을 나타내며, 필요한 경우 KDF 및 MAC도 포함됨.

- 알 수 없는 암호화 유형에 대해서도 LS2가 파싱 가능하고 플러드필에 의해 검증 가능하도록 키 길이 필드를 포함했습니다.

- 제안될 첫 번째 새로운 암호화 유형은 아마도 ECIES/X25519일 것입니다. 종단 간에서 어떻게 사용되는지 (ElGamal/AES+SessionTag의 약간 수정된 버전 또는 ChaCha/Poly와 같은 완전히 새로운 방식)는 하나 이상의 별도 제안에서 지정될 것입니다. ECIES 제안 144 및 145도 참조하세요.

### 암호화된 LS2

LS2의 장점:

- 임대의 8바이트 만료가 4바이트로 변경됨.

LS2의 단점:

이 일부는 이 제안의 범위를 벗어나지만, 아직 별도의 암호화 제안이 없으므로 잠시 여기에 메모를 남깁니다. ECIES 제안 144 및 145도 참조하세요.

- 철회를 구현한다면, 만료 필드를 0으로 설정하거나, 임대를 0개로 설정하거나, 둘 다 설정하는 방식으로 할 수 있음. 별도의 철회 키는 필요 없음.

목표:

    Standard LS flag (1)
암호화된 LS2는 종단 간 마늘 메시지에서 절대 전송되지 않습니다. 위의 표준 LS2를 사용하세요.

    Encrypted LS2 type (5)
기존 암호화된 LeaseSet과의 변경 사항:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
조회:

    10 minutes, as in a regular LS, or hours, as in a meta LS.
저장:

    Destination


### 정의

저장 위치:

일반적인 만료:

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

게시자:

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

암호화된 LS2에 사용되는 암호화 빌딩 블록에 해당하는 다음 함수를 정의합니다:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

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

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### 형식

SIG

- 암호화 키는 서버 선호도 순서대로, 가장 선호하는 키가 먼저 오도록 정렬됨. 기본 클라이언트 동작은 지원되는 암호화 유형 중 첫 번째 키를 선택하는 것입니다. 클라이언트는 암호화 지원, 상대적 성능 및 기타 요소에 따라 다른 선택 알고리즘을 사용할 수 있음.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

암호화된 LS2 형식은 세 개의 중첩된 계층으로 구성됩니다:

#### 계층 0 (외부)

전체 형식은 다음과 같습니다::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

암호화된 LS2는 블라인딩됨에 유의하세요. 헤더에 목적지가 없습니다. DHT 저장 위치는 SHA-256(sig 유형 || 블라인딩된 공개 키)이며, 매일 회전됨.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

위에 명시된 표준 LS2 헤더를 사용하지 않습니다.

    Length as implied by sig type

유형

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

블라인딩된 공개 키 서명 유형

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

블라인딩된 공개 키

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

게시 타임스탬프

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

만료

    2 bytes, big endian

플래그

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

일시적 키 데이터

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### 계층 1 (중간)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

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

서명

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


플래그

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### 계층 2 (내부)

DH 클라이언트 인증 데이터

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

PSK 클라이언트 인증 데이터

    LeaseSet2 data for the given type.

    Includes the header and signature.


### 블라인딩 키 도출

innerCiphertext

유형

#### 목표

- 블라인딩 추가
- 여러 서명 유형 허용
- 새로운 암호 원시 요소가 필요하지 않음
- 선택적으로 각 수신자에게 암호화, 철회 가능
- 표준 LS2 및 메타 LS2만 암호화 지원

#### 보안

데이터

#### 정의

Ed25519 및 [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)를 기반으로 한 다음 방식을 키 블라인딩에 사용합니다. Re25519 서명은 Ed25519 곡선에서 SHA-512를 해시로 사용합니다.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

[Tor의 rend-spec-v3.txt 부록 A.2](https://spec.torproject.org/rend-spec-v3)는 유사한 설계 목표를 가지지만, 그 블라인딩된 공개 키가 소수 차수 부분군에 있지 않을 수 있고, 보안 의미가 알려지지 않았기 때문에 사용하지 않습니다.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

블라인딩 방식의 보안은 알파의 분포가 블라인딩되지 않은 개인 키와 동일해야 함을 요구합니다. 그러나 Ed25519 개인 키(sig 유형 7)를 Red25519 개인 키(sig 유형 11)로 블라인딩할 때 분포가 다릅니다. [zcash 섹션 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)의 요구사항을 충족하기 위해, "재난수화된 공개 키와 그 키에 대한 서명의 조합이 재난수화된 키를 드러내지 않도록" Red25519(sig 유형 11)를 블라인딩되지 않은 키에도 사용해야 합니다. 기존 목적지에는 유형 7을 허용하지만, 암호화될 새로운 목적지에는 유형 11을 권장합니다.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### 블라인딩 계산

A'

LEOS2IP(x)

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
H*(x)

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
매일(UTC) 새로운 비밀 알파와 블라인딩된 키를 생성해야 합니다. 비밀 알파와 블라인딩된 키는 다음과 같이 계산됩니다.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
모든 당사자에 대한 GENERATE_ALPHA(destination, date, secret):

#### 서명

leaseset을 게시하는 소유자에 대한 BLIND_PRIVKEY():

leaseset을 검색하는 클라이언트에 대한 BLIND_PUBKEY():

두 가지 A' 계산 방법 모두 동일한 결과를 산출하며, 이는 요구됩니다.

블라인딩되지 않은 leaseset은 블라인딩되지 않은 Ed25519 또는 Red25519 서명 개인 키로 서명되며, 블라인딩되지 않은 Ed25519 또는 Red25519 서명 공개 키(sig 유형 7 또는 11)로 검증됩니다.

#### 서명/검증 계산

서명 공개 키가 오프라인인 경우, 블라인딩되지 않은 leaseset은 블라인딩되지 않은 일시적 Ed25519 또는 Red25519 서명 개인 키로 서명되며, 블라인딩되지 않은 Ed25519 또는 Red25519 일시적 서명 공개 키(sig 유형 7 또는 11)로 검증됩니다. 암호화된 leaseset에 대한 오프라인 키에 대한 추가 참고 사항은 아래 참조.

암호화된 leaseset의 서명을 위해, [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)를 기반으로 한 Red25519를 사용하여 블라인딩된 키로 서명하고 검증합니다. Red25519 서명은 Ed25519 곡선에서 SHA-512를 해시로 사용합니다.

Red25519는 표준 Ed25519와 동일하지만 아래에 명시된 부분을 제외하고는 동일합니다.

암호화된 leaseset의 외부 부분은 Red25519 키와 서명을 사용합니다.

Red25519는 Ed25519와 거의 동일합니다. 두 가지 차이점이 있습니다:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Red25519 개인 키는 난수에서 생성된 후 위에 정의된 L로 mod를 취해야 합니다. Ed25519 개인 키는 난수에서 생성된 후 바이트 0과 31에서 비트 마스킹을 사용하여 "클램핑"됩니다. Red25519에서는 이 작업을 수행하지 않습니다. 위에 정의된 GENERATE_ALPHA() 및 BLIND_PRIVKEY() 함수는 mod L을 사용하여 적절한 Red25519 개인 키를 생성합니다.

```text
// same as in Ed25519
```
### 암호화 및 처리

#### 하위 자격 증명 도출

Red25519에서 서명을 위한 r 계산은 추가 난수 데이터를 사용하며, 개인 키의 해시 대신 공개 키 값을 사용합니다. 난수 데이터로 인해 동일한 데이터를 동일한 키로 서명하더라도 모든 Red25519 서명이 다릅니다.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
서명:

검증:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
블라인딩 프로세스의 일부로, 암호화된 LS2는 해당 목적지의 서명 공개 키를 아는 자만이 복호화할 수 있도록 해야 합니다. 전체 목적지는 필요하지 않습니다. 이를 위해 서명 공개 키에서 자격 증명을 도출합니다:

#### 계층 1 암호화

개인화 문자열은 자격 증명이 일반 목적지 해시와 같은 DHT 조회 키로 사용되는 해시와 충돌하지 않도록 보장합니다.

```text
outerInput = subcredential || publishedTimestamp
```
주어진 블라인딩된 키에 대해 하위 자격 증명을 도출할 수 있습니다:

```text
outerSalt = CSRNG(32)
```
하위 자격 증명은 아래의 키 도출 프로세스에 포함되어, 해당 키를 목적지의 서명 공개 키에 대한 지식에 바인딩합니다.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
먼저, 키 도출 프로세스의 입력을 준비합니다:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### 계층 1 복호화

다음으로, 난수 솔트를 생성합니다:

```text
outerSalt = outerCiphertext[0:31]
```
그런 다음, 계층 1을 암호화하는 데 사용되는 키를 도출합니다:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
마지막으로, 계층 1 평문을 암호화하고 직렬화합니다:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### 계층 2 암호화

솔트는 계층 1 암호문에서 파싱됩니다:

그런 다음, 계층 1을 암호화하는 데 사용되는 키를 도출합니다:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### 계층 2 복호화

마지막으로, 계층 1 암호문을 복호화합니다:

클라이언트 인증이 활성화된 경우, 아래에 설명된 대로 ``authCookie``가 계산됩니다. 클라이언트 인증이 비활성화된 경우, ``authCookie``는 길이가 0인 바이트 배열입니다.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### 클라이언트별 인증

암호화는 계층 1과 유사한 방식으로 진행됩니다:

클라이언트 인증이 활성화된 경우, 아래에 설명된 대로 ``authCookie``가 계산됩니다. 클라이언트 인증이 비활성화된 경우, ``authCookie``는 길이가 0인 바이트 배열입니다.

#### DH 클라이언트 인증

복호화는 계층 1과 유사한 방식으로 진행됩니다:

목적지에 대해 클라이언트 인증이 활성화된 경우, 서버는 암호화된 LS2 데이터를 복호화하도록 승인된 클라이언트 목록을 유지합니다. 클라이언트별로 저장되는 데이터는 인증 메커니즘에 따라 달라지며, 각 클라이언트가 생성하고 안전한 비대칭 메커니즘을 통해 서버에 보내는 키 소재의 일부 형태를 포함합니다.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
클라이언트별 인증을 구현하는 두 가지 대안이 있습니다:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
각 클라이언트는 DH 키쌍 ``[csk_i, cpk_i]``를 생성하고 공개 키 ``cpk_i``를 서버에 보냅니다.

서버 처리 ^^^^^^^^^^^^^^^^^ 서버는 새로운 ``authCookie``와 일시적 DH 키쌍을 생성합니다:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
그런 다음, 승인된 각 클라이언트에 대해 서버는 공개 키로 ``authCookie``를 암호화합니다:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### 사전 공유 키 클라이언트 인증

서버는 각 ``[clientID_i, clientCookie_i]`` 튜플을 암호화된 LS2의 계층 1에 ``epk``와 함께 배치합니다.

클라이언트 처리 ^^^^^^^^^^^^^^^^^ 클라이언트는 개인 키를 사용하여 예상 클라이언트 식별자 ``clientID_i``, 암호화 키 ``clientKey_i``, 암호화 IV ``clientIV_i``를 도출합니다:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
그런 다음, 클라이언트는 ``clientID_i``를 포함하는 항목을 계층 1 인증 데이터에서 검색합니다. 일치하는 항목이 있으면, 클라이언트는 이를 복호화하여 ``authCookie``를 얻습니다:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
각 클라이언트는 비밀 32바이트 키 ``psk_i``를 생성하고 서버에 보냅니다. 또는 서버가 비밀 키를 생성하여 하나 이상의 클라이언트에게 보낼 수 있습니다.

서버 처리 ^^^^^^^^^^^^^^^^^ 서버는 새로운 ``authCookie``와 솔트를 생성합니다:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
그런 다음, 승인된 각 클라이언트에 대해 서버는 사전 공유 키로 ``authCookie``를 암호화합니다:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### 보안 고려사항

서버는 각 ``[clientID_i, clientCookie_i]`` 튜플을 암호화된 LS2의 계층 1에 ``authSalt``와 함께 배치합니다.

클라이언트 처리 ^^^^^^^^^^^^^^^^^ 클라이언트는 사전 공유 키를 사용하여 예상 클라이언트 식별자 ``clientID_i``, 암호화 키 ``clientKey_i``, 암호화 IV ``clientIV_i``를 도출합니다:

그런 다음, 클라이언트는 ``clientID_i``를 포함하는 항목을 계층 1 인증 데이터에서 검색합니다. 일치하는 항목이 있으면, 클라이언트는 이를 복호화하여 ``authCookie``를 얻습니다:

위의 두 클라이언트 인증 메커니즘 모두 클라이언트 멤버십에 대한 개인정보를 제공합니다. 목적지를 아는 자만이 현재 몇 명의 클라이언트가 구독 중인지 알 수 있지만, 어떤 클라이언트가 추가되거나 철회되는지는 추적할 수 없습니다.

- 보안을 위해 전체를 암호화
- AES만 사용하지 않고 안전하게 암호화
- 각 수신자에게 암호화

서버는 클라이언트가 목록에서 자신의 위치를 알거나 다른 클라이언트가 추가되거나 철회되는 것을 추론하지 못하도록 암호화된 LS2를 생성할 때마다 클라이언트 순서를 무작위로 해야 합니다.

- 저장 및 검색을 위한 필요한 평문 정보를 포함하는 외부 계층.
- 클라이언트 인증을 처리하는 중간 계층.
- 실제 LS2 데이터를 포함하는 내부 계층.

서버는 인증 데이터 목록에 무작위 항목을 삽입하여 구독 중인 클라이언트 수를 숨길 수 있습니다.

- 블라인딩되지 않은 목적지의 서명 공개 키는
  Ed25519(sig 유형 7) 또는 Red25519(sig 유형 11)여야 하며;
  다른 서명 유형은 지원되지 않음
- 서명 공개 키가 오프라인인 경우, 일시적 서명 공개 키도 Ed25519여야 함
- 블라인딩은 계산적으로 간단해야 함
- 기존 암호화 원시 요소 사용
- 블라인딩된 공개 키는 블라인딩 해제될 수 없어야 함
- 블라인딩된 공개 키는 Ed25519 곡선과 소수 차수 부분군에 있어야 함
- 블라인딩된 공개 키를 도출하기 위해 목적지의 서명 공개 키를 알아야 함
  (전체 목적지는 필요하지 않음)
- 선택적으로 블라인딩된 공개 키를 도출하기 위해 추가 비밀이 필요할 수 있음

DH 클라이언트 인증의 장점 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 이 방식의 보안은 클라이언트 키 소재의 비대칭 교환에만 의존하지 않습니다. 클라이언트의 개인 키는 장치를 떠날 필요가 없으므로, 비대칭 교환을 가로챌 수 있는 공격자가 DH 알고리즘을 깨지 못하면 암호화된 LS2를 복호화하거나 클라이언트가 얼마나 오래 액세스 권한을 부여받았는지 알 수 없습니다.

### Base 32 주소를 사용한 암호화된 LS

DH 클라이언트 인증의 단점 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PSK 클라이언트 인증의 장점 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### 오프라인 키를 사용한 암호화된 LS

PSK 클라이언트 인증의 단점 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

제안 149 참조.

비트토런트에는 암호화된 LS2를 사용할 수 없습니다. 컴팩트 공지 응답이 32바이트이기 때문입니다. 32바이트에는 해시만 포함되어 있습니다. leaseset이 암호화되었음을 나타내거나 서명 유형을 나타낼 공간이 없습니다.

### 참고 사항

- 서버 측에서 N 클라이언트에 대해 N + 1개의 DH 연산이 필요합니다.
- 클라이언트 측에서 하나의 DH 연산이 필요합니다.
- 클라이언트가 비밀 키를 생성해야 합니다.

- DH 연산이 필요하지 않습니다.
- 서버가 비밀 키를 생성할 수 있습니다.
- 원하는 경우 여러 클라이언트와 동일한 키를 공유할 수 있습니다.

- 이 방식의 보안은 클라이언트 키 소재의 비대칭 교환에 매우 의존합니다. 특정 클라이언트의 교환을 가로챈 공격자는 해당 클라이언트가 승인된 이후의 모든 후속 암호화된 LS2를 복호화할 수 있으며, 클라이언트의 액세스가 언제 철회되는지 알 수 있습니다.

- 암호화된 leaseset을 사용하는 서비스는 암호화된 버전을 플러드필에 게시합니다. 그러나 효율성을 위해, 인증 후 (예: 화이트리스트를 통해) 클라이언트에게 마늘 메시지에서 암호화되지 않은 leaseset을 보냅니다.

- 플러드필은 남용을 방지하기 위해 최대 크기를 합리적인 값으로 제한할 수 있습니다.

### 메타 LS2

오프라인 키를 사용한 암호화된 leaseset의 경우, 블라인딩된 개인 키도 매일 오프라인에서 생성되어야 합니다.

선택적 오프라인 서명 블록은 암호화된 leaseset의 평문 부분에 있으므로, 플러드필을 스크래핑하는 자는 이를 사용하여 leaseset을 여러 날에 걸쳐 추적할 수 있습니다 (복호화는 불가). 이를 방지하기 위해 키 소유자는 매일 새로운 일시적 키도 생성해야 합니다. 일시적 키와 블라인딩된 키 모두 미리 생성하여 라우터에 일괄적으로 전달할 수 있습니다.

이 제안에서는 여러 일시적 및 블라인딩된 키를 패키징하고 클라이언트 또는 라우터에 제공하기 위한 파일 형식을 정의하지 않습니다. 오프라인 키를 사용한 암호화된 leaseset을 지원하기 위한 I2CP 프로토콜 확장을 이 제안에서 정의하지 않습니다.

이것은 멀티호밍을 대체하는 데 사용됩니다. 다른 leaseset과 마찬가지로, 생성자가 서명합니다. 이것은 목적지 해시의 인증된 목록입니다.

메타 LS2는 트리 구조의 최상위 노드이자 중간 노드일 수 있습니다. LS, LS2 또는 다른 메타 LS2를 가리키는 여러 항목을 포함하여 대규모 멀티호밍을 지원합니다. 메타 LS2는 LS, LS2 및 메타 LS2 항목의 혼합을 포함할 수 있습니다. 트리의 리프는 항상 LS 또는 LS2입니다. 트리는 DAG입니다. 루프는 금지되며, 조회를 수행하는 클라이언트는 루프를 감지하고 따르지 않아야 합니다.

메타 LS2는 표준 LS 또는 LS2보다 훨씬 더 긴 만료 시간을 가질 수 있습니다. 최상위 수준은 게시 날짜 이후 몇 시간 후에 만료될 수 있습니다. 최대 만료 시간은 플러드필과 클라이언트에 의해 시행되며, TBD입니다.

메타 LS2의 사용 사례는 대규모 멀티호밍이지만, LS 또는 LS2가 현재 제공하는 것보다 라우터와 leaseset의 상관 관계(라우터 재시작 시)에 대한 보호가 더 많지 않습니다. 이것은 "페이스북" 사용 사례와 동일하며, 아마도 상관 관계 보호가 필요하지 않을 것입니다. 이 사용 사례는 아마도 오프라인 키가 필요할 것이며, 트리의 각 노드에서 표준 헤더에 제공됩니다.

리프 라우터, 중간 및 마스터 메타 LS 서명자 간의 조정을 위한 백엔드 프로토콜은 여기에서 지정되지 않습니다. 요구 사항은 매우 간단합니다 - 피어가 작동 중인지 확인하고 몇 시간마다 새 LS를 게시합니다. 유일한 복잡성은 장애 시 최상위 또는 중간 수준 메타 LS의 새 게시자를 선택하는 것입니다.

여러 라우터의 임대를 결합하고 서명하여 단일 leaseset에 게시하는 믹스 앤 매치 leaseset은 제안 140, "보이지 않는 멀티호밍"에서 문서화되어 있습니다. 이 제안은 작성된 대로 실현 불가능합니다. 스트리밍 연결이 단일 라우터에 "스티키"하지 않기 때문입니다. http://zzz.i2p/topics/2335 참조.

보이지 않는 멀티호밍의 경우 백엔드 프로토콜과 라우터 및 클라이언트 내부와의 상호 작용은 매우 복잡할 것입니다.

    Standard LS flag (1)
최상위 메타 LS의 플러드필을 과부하하지 않기 위해 만료 시간은 최소 몇 시간이어야 합니다. 클라이언트는 최상위 메타 LS를 캐시하고 만료되지 않은 경우 재시작 시에도 유지해야 합니다.

    Meta LS2 type (7)
클라이언트가 트리를 탐색하고, 폴백을 포함하여 사용이 분산되도록 하는 알고리즘을 정의해야 합니다. 해시 거리, 비용 및 무작위성의 일부 함수. 노드가 LS 또는 LS2와 메타 LS를 모두 가진 경우, 언제 이러한 leaseset을 사용할 수 있고 언제 트리를 계속 탐색해야 하는지 알아야 합니다.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
조회:

    Hours. Max 18.2 hours (65535 seconds)
저장:

    "master" Destination or coordinator, or intermediate coordinators

### 형식

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
저장 위치:

### 참고 사항

- 복호화 후, 내부 타임스탬프와 만료가 최상위 수준과 일치하는지 확인해야 합니다.

- AES보다 ChaCha20를 선택했습니다. AES 하드웨어 지원이 있는 경우 속도는 비슷하지만, AES 하드웨어 지원이 없는 경우(예: 저가형 ARM 장치) ChaCha20가 2.5-3배 더 빠릅니다.

- 속도에 너무 신경 쓰지 않아서 키가 있는 BLAKE2b를 사용하지 않습니다. 가장 큰 n 요구 사항을 수용할 만큼 충분한 출력 크기를 가지며 (또는 원하는 키마다 카운터 인수로 한 번 호출할 수 있음). BLAKE2b는 SHA-256보다 훨씬 빠르며, 키가 있는 BLAKE2b는 해시 함수 호출 총 수를 줄일 수 있습니다. 그러나 제안 148을 참조하세요. 여기서 다른 이유로 BLAKE2b로 전환하는 것이 제안됩니다. [안전한 키 도출 성능](https://www.lvh.io/posts/secure-key-derivation-performance.html) 참조.

### 서비스 레코드

일반적인 만료:

게시자:

플래그 및 속성: 향후 사용

    n/a, see Service List
이것은 목적지가 서비스에 참여하고 있다는 개별 레코드입니다. 참가자가 플러드필로 보냅니다. 개별적으로 플러드필이 보내는 것은 아니며, 서비스 목록의 일부로만 보냅니다. 서비스 레코드는 만료를 0으로 설정하여 서비스 참여를 철회하는 데에도 사용됩니다.

    Service Record type (9)
이것은 LS2가 아니지만 표준 LS2 헤더 및 서명 형식을 사용합니다.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
조회:

    Hours. Max 18.2 hours (65535 seconds)
저장:

    Destination

### 형식

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### 참고 사항

- 이 기능을 사용하는 분산 서비스는 서비스 목적지의 개인 키를 가진 하나 이상의 "마스터"를 가집니다. 그들은 (비대칭적으로) 현재 활성 목적지 목록을 결정하고 메타 LS2를 게시합니다. 중복성을 위해 여러 마스터가 메타 LS2를 멀티호밍(즉, 동시 게시)할 수 있습니다.

- 분산 서비스는 단일 목적지에서 시작하거나 기존 스타일의 멀티호밍을 사용한 다음 메타 LS2로 전환할 수 있습니다. 표준 LS 조회는 LS, LS2 또는 메타 LS2 중 하나를 반환할 수 있습니다.

- 서비스가 메타 LS2를 사용할 때, 터널(임대)이 없습니다.

### 서비스 목록

저장 위치:

일반적인 만료:

게시자:

이것은 LS2와 전혀 다르며 다른 형식을 사용합니다.

서비스 목록은 플러드필에 의해 생성되고 서명됩니다. 누구나 서비스 레코드를 플러드필에 게시하여 서비스에 가입할 수 있으므로 인증되지 않습니다.

서비스 목록은 전체 서비스 레코드가 아닌 짧은 서비스 레코드를 포함합니다. 이들은 서명을 포함하지만 해시만 포함하며 전체 목적지를 포함하지 않으므로 전체 목적지를 알지 않고는 검

    Service List lookup type (11)
유형 3, 7, 9는 아래에 명시된 표준 LS2 헤더를 사용합니다:

    Service List type (11)
기존 LeaseSet과의 변경 사항:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
조회:

    Hours, not specified in the list itself, up to local policy
저장:

    Nobody, never sent to floodfill, never flooded.

### 형식

암호화된 LS2 형식은 세 개의 중첩된 계층으로 구성됩니다:

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
Service List의 서명을 확인하려면:

- 만료가 모두 0이면, 플러드필은 레코드를 철회하고 더 이상 서비스 목록에 포함하지 않아야 합니다.

각 Short Service Record의 서명을 검증하려면:

- 저장: 플러드필은 이러한 레코드의 저장을 엄격히 제한하고 해시당 저장된 레코드 수와 만료를 제한할 수 있습니다. 해시의 화이트리스트도 사용할 수 있습니다.

각 Revocation Record의 서명을 검증하려면:

- 동일한 해시에 있는 다른 netdb 유형은 우선 순위를 가지므로, 서비스 레코드는 LS/RI를 덮어쓸 수 없지만, LS/RI는 해당 해시의 모든 서비스 레코드를 덮어씁니다.

### 참고 사항

- 알 수 없는 서명 유형을 지원할 수 있도록 sig 유형 대신 서명 길이를 사용합니다.

- 서비스 목록에는 만료가 없으며, 수신자는 정책 또는 개별 레코드의 만료를 기준으로 스스로 결정할 수 있습니다.

- Service List는 flooding되지 않으며, 개별 Service Record만 flooding됩니다. 각 floodfill은 Service List를 생성하고 서명하며 캐시합니다. floodfill은 캐시 시간과 service 및 revocation record의 최대 개수에 대해 자체 정책을 사용합니다.

## 공통 구조 명세에 필요한 변경 사항

### 키 인증서

이 제안의 범위를 벗어납니다. ECIES 제안 144 및 145에 추가하십시오.

### 새로운 중간 구조

Lease2, MetaLease, LeaseSet2Header, OfflineSignature에 대한 새 구조를 추가합니다. 0.9.38 릴리스부터 적용됩니다.

### 새로운 NetDB 유형

위에서 통합한 각각의 새로운 leaseset 유형에 대한 구조를 추가합니다. LeaseSet2, EncryptedLeaseSet, MetaLeaseSet의 경우 릴리스 0.9.38부터 유효합니다. Service Record와 Service List의 경우 예비 단계이며 일정은 미정입니다.

### 새 서명 유형

RedDSA_SHA512_Ed25519 Type 11 추가. 공개 키는 32바이트이고, 개인 키는 32바이트이며, 해시는 64바이트, 서명은 64바이트입니다.

## 암호화 명세 변경 필요

이 제안의 범위를 벗어납니다. 제안 144와 145를 참조하십시오.

## 필요한 I2NP 변경 사항

참고 추가: LS2는 최소 버전 이상의 floodfill에만 게시할 수 있습니다.

### 데이터베이스 조회 메시지

서비스 목록 조회 유형을 추가하십시오.

### 변경 사항

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### 데이터베이스 저장 메시지

모든 새로운 store 유형을 추가하십시오.

### 변경 사항

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
## 필요한 I2CP 변경 사항

### I2CP 옵션

라우터 측에서 해석되어 SessionConfig Mapping으로 전송되는 새 옵션:

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
클라이언트 측에서 해석되는 새 옵션:

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
### 세션 설정

참고로, 오프라인 서명의 경우 i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, i2cp.leaseSetOfflineSignature 옵션이 필요하며, 서명은 transient signing private key에 의해 수행됩니다.

### Leaseset 요청 메시지

Router에서 client로. 변경 사항 없음. leases는 8바이트 타임스탬프와 함께 전송되며, 반환되는 leaseset이 4바이트 타임스탬프를 사용하는 LS2이더라도 마찬가지입니다. 응답은 Create Leaseset 또는 Create Leaseset2 Message일 수 있습니다.

### Variable leaseSet 요청 메시지

Router에서 client로. 변경 사항 없음. leases는 8바이트 타임스탬프와 함께 전송되며, 반환되는 leaseset이 4바이트 타임스탬프를 사용하는 LS2이더라도 마찬가지입니다. 응답은 Create Leaseset 또는 Create Leaseset2 Message일 수 있습니다.

### Leaseset2 메시지 생성

클라이언트에서 router로. Create Leaseset Message 대신 사용할 새 메시지.

### 정당성

- router가 store type을 파싱하려면, 세션 설정에서 미리 router에 전달되지 않는 한 해당 type이 메시지 안에 있어야 합니다.
  일반적인 파싱 코드의 경우 메시지 자체에 포함시키는 것이 더 쉽습니다.

- router가 개인 키의 타입과 길이를 알기 위해서는,
  파서가 세션 구성에서 미리 타입을 알고 있지 않은 한, leaseSet 뒤에 있어야 합니다.
  일반적인 파싱 코드에서는 메시지 자체에서 알아내는 것이 더 쉽습니다.

- 이전에 폐기를 위해 정의되었으나 사용되지 않았던 서명 개인 키는 LS2에 존재하지 않는다.

### 메시지 유형

Create Leaseset2 메시지의 메시지 유형은 41입니다.

### 형식

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
### 참고 사항

- 최소 router 버전은 0.9.39입니다.
- 메시지 타입 40을 사용하는 예비 버전은 0.9.38에 있었지만 형식이 변경되었습니다.
  타입 40은 폐기되었으며 지원되지 않습니다.

### 문제점

- 암호화된 LS와 meta LS를 지원하려면 더 많은 변경이 필요합니다.

### 블라인딩 정보 메시지

클라이언트에서 router로. 새 메시지.

### 정당성

- router는 destination이 blinded인지 알아야 합니다.
  blinded 상태이고 secret 또는 클라이언트별 인증을 사용하는 경우,
  해당 정보도 가지고 있어야 합니다.

- 새 형식의 b32 주소("b33")에 대한 Host Lookup은 해당 주소가 blinded 상태임을 router에 알리지만, Host Lookup 메시지에서 secret 또는 private key를 router에 전달할 메커니즘은 없습니다. Host Lookup 메시지를 확장하여 해당 정보를 추가할 수도 있지만, 새 메시지를 정의하는 것이 더 깔끔합니다.

- 클라이언트가 router에 이를 알릴 수 있는 프로그래밍 방식이 필요합니다.
  그렇지 않으면 사용자가 각 destination을 수동으로 구성해야 합니다.

### 사용법

클라이언트가 blinded destination으로 메시지를 보내기 전에, Host Lookup 메시지에서 "b33"을 조회하거나 Blinding Info 메시지를 보내야 합니다. blinded destination에 secret 또는 클라이언트별 인증이 필요한 경우, 클라이언트는 Blinding Info 메시지를 보내야 합니다.

router는 이 메시지에 대한 응답을 보내지 않습니다.

### 메시지 유형

Blinding Info Message의 메시지 타입은 42입니다.

### 형식

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
### 참고 사항

- 최소 router 버전은 0.9.43입니다

### 문제점

### 호스트 응답 메시지 (enc)

"b33" 호스트명 조회를 지원하고 router가 필요한 정보를 가지고 있지 않은 경우 표시를 반환하기 위해, Host Reply Message에 대한 추가 결과 코드를 다음과 같이 정의합니다:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
1-255 값은 이미 오류로 정의되어 있으므로 하위 호환성 문제는 없습니다.

### 메타 리다이렉트 메시지

Router에서 클라이언트로. 새 메시지.

### 정당성

클라이언트는 주어진 Hash가 Meta LS로 해석될 것임을 사전에 알 수 없습니다.

Destination에 대한 leaseset 조회가 Meta LS를 반환하면 router가 재귀적 해석을 수행합니다. 데이터그램의 경우 클라이언트 측은 알 필요가 없습니다. 하지만 프로토콜이 SYN ACK에서 Destination을 확인하는 스트리밍의 경우에는 "실제" Destination이 무엇인지 알아야 합니다. 따라서 새로운 메시지가 필요합니다.

### 사용법

router는 meta LS에서 사용되는 실제 destination에 대한 캐시를 유지한다. 클라이언트가 meta LS로 확인되는 destination으로 메시지를 보내면, router는 마지막으로 사용된 실제 destination에 대해 캐시를 확인한다. 캐시가 비어 있으면 router는 meta LS에서 destination을 선택하고 leaseset을 조회한다. leaseset 조회가 성공하면 router는 해당 destination을 캐시에 추가하고 클라이언트에 Meta Redirect Message를 보낸다. 이는 destination이 만료되어 변경해야 하는 경우를 제외하면 한 번만 수행된다. 클라이언트도 필요한 경우 해당 정보를 캐시해야 한다. Meta Redirect Message는 모든 SendMessage에 대한 응답으로 전송되지 않는다.

router는 버전 0.9.47 이상인 클라이언트에만 이 메시지를 전송합니다.

클라이언트는 이 메시지에 대한 응답을 보내지 않습니다.

### 메시지 유형

Meta Redirect Message의 메시지 유형은 43입니다.

### 형식

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
### Meta 지원을 위한 변경 사항

router 간 통신 및 조정을 포함한 Meta 생성 및 지원 방법은 이 제안의 범위를 벗어납니다. 관련 제안 150을 참조하십시오.

### Offline Keys 지원을 위한 변경 사항

오프라인 서명은 streaming 또는 repliable datagrams에서 검증할 수 없습니다. 아래 섹션을 참조하십시오.

## 개인 키 파일 변경 필요

개인 키 파일(eepPriv.dat) 형식은 공식 사양의 일부는 아니지만 [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html)에 문서화되어 있으며 다른 구현에서도 지원합니다. 이를 통해 개인 키를 다른 구현으로 이식할 수 있습니다.

일시적 공개 키와 오프라인 서명 정보를 저장하기 위해 변경이 필요합니다.

### 변경 사항

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
### 개인 키 파일 CLI 변경 필요

다음 옵션에 대한 지원을 추가하십시오:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## 스트리밍 변경 필요

현재 스트리밍에서는 오프라인 서명을 검증할 수 없습니다. 아래 변경 사항은 옵션에 오프라인 서명 블록을 추가합니다. 이를 통해 I2CP를 통해 이 정보를 가져올 필요가 없어집니다.

### 변경 사항

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
### 참고 사항

- 대안은 플래그를 추가하고 I2CP를 통해 일시적 공개 키를 가져오는 것입니다
  (위의 Host Lookup / Host Reply Message 섹션 참조)

## Repliable Datagram 변경 필요

repliable datagram 처리에서는 오프라인 서명을 검증할 수 없습니다. 오프라인 서명되었음을 나타낼 flag가 필요하지만 flag를 넣을 곳이 없습니다. 완전히 새로운 프로토콜 번호와 형식이 필요할 것입니다.

### 변경 사항

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
### 참고 사항

- 대안으로 flag를 추가하고 I2CP를 통해 transient public key를 가져오는 방법이 있습니다. (위의 Host Lookup / Host Reply Message 섹션 참조)
- flag bytes가 있으니 이제 추가해야 할 다른 옵션이 있을까요?

## SAM V3 필수 변경 사항

SAM은 DESTINATION base 64에서 오프라인 서명을 지원하도록 개선되어야 합니다.

### 변경 사항

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
참고로, 오프라인 서명은 STREAM 및 RAW에서만 지원되며 DATAGRAM에서는 지원되지 않습니다(새로운 DATAGRAM 프로토콜을 정의할 때까지).

SESSION STATUS는 Signing Private Key를 모두 제로로 채워 반환하며, Offline Signature 데이터는 SESSION CREATE에서 제공된 그대로 반환한다는 점에 유의하십시오.

DEST GENERATE와 SESSION CREATE DESTINATION=TRANSIENT는 오프라인 서명된 destination을 생성하는 데 사용할 수 없음에 유의해야 합니다.

### 문제점

버전을 3.4로 올릴까요, 아니면 3.2/3.3 관련 내용을 모두 요구하지 않고 추가할 수 있도록 3.1/3.2/3.3에 그대로 둘까요?

기타 변경 사항은 TBD입니다. 위의 I2CP Host Reply Message 섹션을 참조하십시오.

## BOB 변경 필요 사항

BOB가 오프라인 서명 및/또는 Meta LS를 지원하도록 개선되어야 합니다. 이는 우선순위가 낮으며 아마 명세되거나 구현되지 않을 것입니다. SAM V3가 선호되는 인터페이스입니다.

## 게시, 마이그레이션, 호환성

암호화된 LS2를 제외한 LS2는 LS1과 동일한 DHT 위치에 게시됩니다. LS2가 다른 위치에 있지 않은 한 LS1과 LS2를 모두 게시할 방법은 없습니다.

Encrypted LS2는 blinded key type 및 key data의 hash에 게시됩니다. 그런 다음 이 hash는 LS1에서와 같이 일별 "routing key"를 생성하는 데 사용됩니다.

LS2는 새로운 기능(새로운 암호화, 암호화된 LS, meta 등)이 필요할 때만 사용됩니다. LS2는 지정된 버전 이상의 floodfills에만 게시할 수 있습니다.

LS2를 게시하는 서버는 접속하는 모든 클라이언트가 LS2를 지원한다는 것을 알 수 있습니다. 해당 서버는 garlic에 LS2를 전송할 수 있습니다.

클라이언트는 새로운 crypto를 사용하는 경우에만 garlics로 LS2를 전송할 것입니다. 공유 클라이언트는 LS1을 무기한 사용하게 됩니까? TODO: 이전 crypto와 새로운 crypto를 모두 지원하는 공유 클라이언트를 만들려면 어떻게 해야 합니까?

## 롤아웃

0.9.38에는 오프라인 키를 포함한 표준 LS2에 대한 floodfill 지원이 포함되어 있습니다.

0.9.39에는 LS2 및 Encrypted LS2에 대한 I2CP 지원, sig type 11 서명/검증, Encrypted LS2에 대한 floodfill 지원(sig type 7 및 11, offline keys 제외), 그리고 LS2 암호화/복호화(per-client authorization 제외)가 포함되어 있습니다.

0.9.40에는 클라이언트별 권한 부여를 통한 LS2 암호화/복호화 지원, Meta LS2에 대한 floodfill 및 I2CP 지원, 오프라인 키를 사용한 암호화된 LS2 지원, 암호화된 LS2에 대한 b32 지원이 포함될 예정입니다.

## 감사의 말

암호화된 LS2 설계는 유사한 설계 목표를 가진 [Tor의 v3 hidden service descriptor](https://spec.torproject.org/rend-spec-v3)의 영향을 크게 받았습니다.

## 참고 자료

* [Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, Bo-Yin Yang의 "고속 고보안 서명"](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
