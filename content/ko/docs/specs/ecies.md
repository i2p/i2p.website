---
title: "ECIES-X25519-AEAD-Ratchet 암호화 명세"
description: "I2P용 타원곡선 통합 암호화 스킴 (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## 개요

### 목적

ECIES-X25519-AEAD-Ratchet는 I2P의 최신 종단 간 암호화 프로토콜로, 기존의 ElGamal/AES+SessionTags(세션 태그) 시스템을 대체합니다. 이는 순방향 기밀성, 인증된 암호화, 그리고 성능과 보안의 상당한 향상을 제공합니다.

### ElGamal/AES+SessionTags 대비 핵심 개선점

- **더 작은 키**: 32바이트 키 대 256바이트 ElGamal 공개 키 (87.5% 감소)
- **순방향 보안**: DH ratcheting(세션 키를 단계적으로 갱신해 선행 키 노출에 대비하는 기법)으로 달성 (기존 프로토콜에는 없음)
- **현대적 암호기술**: X25519 DH, ChaCha20-Poly1305 AEAD(인증 기능이 결합된 암호화 방식), SHA-256
- **인증된 암호화**: AEAD 구성으로 인증이 내장됨
- **양방향 프로토콜**: 쌍으로 묶인 수신/송신 세션 대 단방향의 기존 방식
- **효율적인 태그**: 8바이트 세션 태그 대 32바이트 태그 (75% 감소)
- **트래픽 난독화**: Elligator2 encoding(무작위처럼 보이도록 매핑하는 인코딩)으로 핸드셰이크가 무작위와 구분되지 않음

### 배포 상태

- **초기 릴리스**: 버전 0.9.46 (2020년 5월 25일)
- **네트워크 배포**: 2020년 기준 완료
- **현재 상태**: 성숙함, 널리 배포됨(운영 환경에서 5년 이상)
- **Router 지원**: 버전 0.9.46 이상 필요
- **Floodfill 요구 사항**: 암호화된 조회를 위해 거의 100% 채택 필요

### 구현 상태

**완전히 구현됨:** - 바인딩이 포함된 새 세션(NS) 메시지 - 새 세션 응답(NSR) 메시지 - 기존 세션(ES) 메시지 - DH ratchet(단계적 키 갱신 메커니즘) - 세션 태그 ratchet 및 대칭 키 ratchet - DateTime, NextKey, ACK, ACK Request, Garlic Clove(갈릭 클로브), 및 Padding 블록

**미구현(버전 0.9.50 기준):** - MessageNumbers 블록 (유형 6) - 옵션 블록 (유형 5) - 종료 블록 (유형 4) - 프로토콜 계층 자동 응답 - 정적 키 미사용 모드 - 멀티캐스트 세션

**참고**: 일부 기능이 추가되었을 수 있으므로 버전 1.5.0부터 2.10.0(2021-2025)까지의 구현 상태는 확인이 필요합니다.

---

## 프로토콜의 기초

### Noise Protocol Framework(Noise 프로토콜 프레임워크)

ECIES-X25519-AEAD-Ratchet(ECIES, X25519, AEAD를 조합한 래쳇 방식)은 [Noise Protocol Framework](https://noiseprotocol.org/) (리비전 34, 2018-07-11)를 기반으로 하며, 특히 I2P 특화 확장을 적용한 **IK**(대화형, 원격 정적 키가 알려진) 핸드셰이크 패턴을 사용한다.

### Noise Protocol(비밀 통신용 암호 프로토콜 프레임워크) 식별자

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**식별자 구성 요소:** - `Noise` - 기본 프레임워크 - `IK` - 알려진 원격 정적 키와의 대화형 핸드셰이크 패턴 - `elg2` - 임시 키를 위한 Elligator2 인코딩(난독화 매핑 기법) (I2P 확장) - `+hs2` - 태그를 혼합하기 위해 두 번째 메시지 전에 호출되는 MixHash (I2P 확장) - `25519` - X25519 디피-헬만 함수 - `ChaChaPoly` - ChaCha20-Poly1305 AEAD 암호 - `SHA256` - SHA-256 해시 함수

### Noise 핸드셰이크 패턴

**IK 패턴 표기:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**토큰 의미:** - `e` - 임시 키 전송 - `s` - 정적 키 전송 - `es` - Alice의 임시 키와 Bob의 정적 키 간의 DH(Diffie-Hellman) - `ss` - Alice의 정적 키와 Bob의 정적 키 간의 DH - `ee` - Alice의 임시 키와 Bob의 임시 키 간의 DH - `se` - Bob의 정적 키와 Alice의 임시 키 간의 DH

### Noise(프로토콜 프레임워크)의 보안 속성

Noise 용어로 말하면 IK pattern(Noise 핸드셰이크 패턴의 하나)은 다음을 제공합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**인증 수준:** - **레벨 1**: 페이로드는 발신자의 정적 키 소유자의 것으로 인증되지만, 키 손상에 의한 사칭(KCI)에 취약함 - **레벨 2**: NSR 이후 KCI 공격에 대한 내성이 있음

**기밀성 수준:** - **레벨 2**: 발신자의 정적 키가 나중에 노출되더라도 순방향 기밀성 - **레벨 4**: 발신자의 임시 키가 나중에 노출되더라도 순방향 기밀성 - **레벨 5**: 양쪽의 임시 키가 모두 삭제된 후 완전한 순방향 기밀성

### IK와 XK의 차이점

IK 패턴(Noise 프로토콜의 핸드셰이크 패턴)은 NTCP2와 SSU2에서 사용되는 XK 패턴과 다릅니다:

1. **네 가지 DH 연산**: IK는 4개의 DH 연산(es, ss, ee, se)을 사용하며, XK는 3개
2. **즉시 인증**: 첫 번째 메시지에서 Alice가 인증됨(인증 수준 1)
3. **더 빠른 전방향 기밀성**: 두 번째 메시지(1-RTT) 후에 완전한 전방향 기밀성(수준 5) 달성
4. **트레이드오프**: 첫 번째 메시지의 페이로드는 전방향 기밀성이 아님(XK에서는 모든 페이로드가 전방향 기밀성임)

**Summary**: IK는 Bob의 응답을 완전한 전방향 보안성(forward secrecy) 하에 1-RTT로 전달할 수 있게 해주지만, 그 대가로 초기 요청에는 전방향 보안성이 적용되지 않는다.

### Signal Double Ratchet(시그널 이중 래칫) 개념

ECIES(타원 곡선 통합 암호화 방식)은 [Signal Double Ratchet 알고리즘](https://signal.org/docs/specifications/doubleratchet/)에서 개념을 채택합니다:

- **DH Ratchet**(디피-헬먼 래칫): 주기적으로 새로운 DH 키를 교환하여 순방향 기밀성을 제공합니다
- **Symmetric Key Ratchet**(대칭 키 래칫): 각 메시지마다 새로운 세션 키를 파생합니다
- **Session Tag Ratchet**(세션 태그 래칫): 결정론적으로 일회용 session tags를 생성합니다

**Signal과의 주요 차이점:** - **래칫을 덜 자주 수행**: I2P는 필요할 때만 래칫을 수행함(태그가 소진되기 직전이거나 정책에 따라) - **헤더 암호화 대신 세션 태그**: 암호화된 헤더 대신 결정적 태그를 사용 - **명시적 ACK(확인 응답)**: 역방향 트래픽에만 의존하지 않고 대역 내(in-band) ACK 블록을 사용 - **태그 래칫과 키 래칫 분리**: 수신자에게 더 효율적임(키 계산을 지연할 수 있음)

### Noise(프로토콜 프레임워크)용 I2P 확장


---

## 암호학적 프리미티브

### X25519 디피-헬만

**명세**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**주요 속성:** - **개인 키 크기**: 32 바이트 - **공개 키 크기**: 32 바이트 - **공유 비밀 크기**: 32 바이트 - **엔디언 방식**: 리틀 엔디언 - **곡선**: Curve25519

**작업:**

### X25519 GENERATE_PRIVATE()

무작위 32바이트 개인 키를 생성합니다:

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

해당하는 공개 키를 도출합니다:

```
pubkey = curve25519_scalarmult_base(privkey)
```
32바이트 리틀 엔디언 공개 키를 반환합니다.

### X25519 DH(privkey, pubkey)

Diffie-Hellman 키 합의를 수행합니다:

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
32바이트 길이의 공유 비밀을 반환합니다.

**Security Note**: 구현자는 공유 비밀이 모두 0인 값(약한 키)이 아님을 검증해야 한다. 이 경우에는 거부하고 핸드셰이크를 중단해야 한다.

### ChaCha20-Poly1305 AEAD(연관 데이터가 있는 인증된 암호화)

**명세**: [RFC 7539](https://tools.ietf.org/html/rfc7539) 섹션 2.8

**매개변수:** - **키 길이**: 32 바이트 (256 비트) - **논스 길이**: 12 바이트 (96 비트) - **MAC 길이**: 16 바이트 (128 비트) - **블록 크기**: 64 바이트 (내부)

**논스 형식:**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**AEAD(연관 데이터가 포함된 인증 암포화) 구성:**

AEAD(연관 데이터가 있는 인증 암호화)은 ChaCha20 스트림 암호와 Poly1305 MAC을 결합합니다:

1. 키와 논스로부터 ChaCha20 키스트림을 생성한다
2. 키스트림과 XOR하여 평문을 암호화한다
3. (연관 데이터 || 암호문)에 대해 Poly1305 MAC을 계산한다
4. 암호문에 16바이트 MAC을 추가한다

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

인증과 함께 평문을 암호화합니다:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**속성:** - 암호문은 평문과 동일한 길이입니다(스트림 암호) - 출력은 plaintext_length + 16바이트입니다(MAC 포함) - 키가 비밀인 경우 전체 출력은 무작위 데이터와 구별되지 않습니다 - MAC(메시지 인증 코드)는 연관 데이터와 암호문 모두를 인증합니다

### ChaCha20-Poly1305 복호화(k, n, ciphertext, ad)

복호화하고 인증을 검증합니다:

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**중요 보안 요구 사항:** - 동일한 키를 사용하는 각 메시지마다 논스(nonce)는 반드시 고유해야 합니다 - 논스는 재사용되어서는 안 됩니다 (재사용 시 치명적인 실패 발생) - MAC 검증은 타이밍 공격을 방지하기 위해 상수 시간 비교를 사용해야 합니다 - MAC 검증에 실패한 경우 반드시 전체 메시지를 거부해야 합니다 (부분 복호화 없음)

### SHA-256 해시 함수

**명세**: NIST FIPS 180-4

**속성:** - **출력 크기**: 32 바이트 (256 비트) - **블록 크기**: 64 바이트 (512 비트) - **보안 수준**: 128 비트 (충돌 저항성)

**작업:**

### SHA-256 H(p, d)

personalization string(개인화 문자열)을 사용한 SHA-256 해시:

```
H(p, d) := SHA256(p || d)
```
여기서 `||`는 연접을 나타내고, `p`는 개인화 문자열, `d`는 데이터이다.

### SHA-256 MixHash(d)

새 데이터로 누적 해시를 업데이트합니다:

```
h = SHA256(h || d)
```
Noise 핸드셰이크 전 과정에서 transcript hash(대화 기록 해시)를 유지하기 위해 사용됩니다.

### HKDF 키 파생

**사양**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**설명**: SHA-256을 사용하는 HMAC 기반 키 유도 함수

**매개변수:** - **해시 함수**: HMAC-SHA256 - **솔트 길이**: 최대 32 바이트 (SHA-256 출력 크기) - **출력 길이**: 가변 (최대 255 * 32 바이트)

**HKDF 함수:**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**일반적인 사용 패턴:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**ECIES에서 사용되는 Info 문자열:** - `"KDFDHRatchetStep"` - DH ratchet(일방향 상태 갱신 메커니즘) 키 유도 - `"TagAndKeyGenKeys"` - 태그 및 키 체인 키 초기화 - `"STInitialization"` - 세션 태그 ratchet 초기화 - `"SessionTagKeyGen"` - 세션 태그 생성 - `"SymmetricRatchet"` - 대칭 키 생성 - `"XDHRatchetTagSet"` - DH ratchet 태그 세트 키 - `"SessionReplyTags"` - NSR 태그 세트 생성 - `"AttachPayloadKDF"` - NSR 페이로드 키 유도

### Elligator2(엘리게이터2) 인코딩

**목적**: X25519 공개 키를 균일한 무작위 32바이트 문자열과 구분할 수 없도록 인코딩한다.

**명세**: [Elligator2 논문](https://elligator.cr.yp.to/elligator-20130828.pdf)

**문제**: 표준 X25519 공개 키는 식별 가능한 구조를 갖습니다. 관찰자는 내용이 암호화되어 있더라도 이러한 키를 감지하여 핸드셰이크 메시지를 식별할 수 있습니다.

**해결책**: Elligator2(타원 곡선 공개 키를 난수처럼 보이게 매핑하는 기법)는 유효한 X25519 공개 키의 약 50%와 난수처럼 보이는 254비트 문자열 사이에 일대일(전단사) 대응을 제공합니다.

**Elligator2(타원곡선 포인트를 균일한 난수처럼 매핑하는 기법)을 사용한 키 생성:**

### Elligator2 GENERATE_PRIVATE_ELG2()

Elligator2(공개 키를 난수처럼 보이게 인코딩하는 기법)로 인코딩 가능한 공개 키에 대응하는 개인 키를 생성합니다:

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**중요**: 무작위로 생성된 개인 키의 약 50%는 인코딩할 수 없는 공개 키를 생성합니다. 이러한 키는 폐기하고 재생성을 시도해야 합니다.

**성능 최적화**: 백그라운드 스레드에서 키를 미리 생성해 적합한 키 쌍 풀을 유지함으로써 핸드셰이크 중 지연을 방지합니다.

### Elligator2 ENCODE_ELG2(pubkey)

공개 키를 무작위처럼 보이는 32바이트로 인코딩합니다:

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**인코딩 세부사항:** - Elligator2(공개키를 무작위 데이터처럼 보이게 매핑하는 기법)는 254비트를 생성합니다(전체 256은 아님) - 바이트 31의 상위 2비트는 무작위 패딩입니다 - 결과는 32바이트 공간 전체에 균일하게 분포합니다 - 유효한 X25519(곡선25519 기반 키 교환) 공개키의 약 50%를 성공적으로 인코딩합니다

### Elligator2 DECODE_ELG2(encodedKey)

다시 원래의 공개 키로 디코딩됩니다:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**보안 속성:** - 인코딩된 키는 계산적으로 난수 바이트와 구별할 수 없다 - 어떠한 통계적 검정으로도 Elligator2로 인코딩된 키를 신뢰할 만하게 검출할 수 없다 - 디코딩은 결정적이다 (같은 인코딩된 키는 항상 같은 공개키를 생성한다) - 인코딩 가능한 부분집합에 속한 키의 ~50%에 대해서 인코딩은 전단사이다

**구현 노트:** - 핸드셰이크 중 재인코딩을 피하기 위해 생성 단계에서 인코딩된 키를 저장 - Elligator2(공개키를 난수처럼 보이게 매핑하는 기법) 생성 과정에서 부적합 판정된 키는 NTCP2에서 사용 가능(Elligator2가 필요하지 않음) - 백그라운드에서의 키 생성은 성능에 필수적 - 거부율 50%로 인해 평균 생성 시간이 두 배로 증가

---

## 메시지 형식

### 개요

ECIES(타원 곡선 통합 암호화 체계)는 세 가지 메시지 유형을 정의합니다:

1. **새 세션 (NS)**: Alice가 Bob에게 보내는 초기 핸드셰이크 메시지
2. **새 세션 응답 (NSR)**: Bob이 Alice에게 보내는 핸드셰이크 응답
3. **기존 세션 (ES)**: 이후의 모든 메시지(양방향)

모든 메시지는 추가적인 암호화 계층을 더해 I2NP Garlic Message(여러 메시지를 하나로 묶어 전달하는 I2P 메시지 형식) 포맷으로 캡슐화됩니다.

### I2NP Garlic 메시지 컨테이너

모든 ECIES(타원곡선 통합 암호 체계) 메시지는 표준 I2NP Garlic Message 헤더로 감싸집니다:

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**필드:** - `type`: 0x26 (Garlic Message(갈릭 메시지)) - `msg_id`: 4바이트 I2NP 메시지 ID - `expiration`: 8바이트 유닉스 타임스탬프(밀리초) - `size`: 2바이트 페이로드 크기 - `chks`: 1바이트 체크섬 - `length`: 4바이트 암호화된 데이터 길이 - `encrypted data`: ECIES(타원곡선 통합 암호 방식)로 암호화된 페이로드

**목적**: I2NP 계층의 메시지 식별 및 라우팅을 제공합니다. `length` 필드는 수신자가 암호화된 페이로드의 총 크기를 알 수 있도록 합니다.

### 새 세션 (NS) 메시지

New Session 메시지(새 세션 메시지)는 Alice가 Bob에게 새 세션을 개시한다. 이 메시지는 세 가지 변형으로 존재한다:

1. **바인딩 포함** (1b): 양방향 통신을 위해 Alice의 정적 키를 포함
2. **바인딩 없음** (1c): 단방향 통신을 위해 정적 키를 생략
3. **일회용** (1d): 세션 수립 없이 단일 메시지 모드

### 바인딩이 포함된 NS 메시지 (유형 1b)

**사용 사례**: 스트리밍, 응답 가능한 데이터그램, 응답이 필요한 모든 프로토콜

**총 길이**: 96 + payload_length 바이트

**형식**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**필드 세부 정보:**

**임시 공개키** (32바이트, 평문): - Alice의 1회용 X25519 공개키 - Elligator2로 인코딩됨 (무작위와 구분 불가능) - 각 NS 메시지마다 새로 생성됨 (재사용하지 않음) - 리틀엔디언 형식

**정적 키 섹션** (32바이트 암호화, MAC 포함 48바이트): - Alice의 X25519 정적 공개 키(32바이트) 포함 - ChaCha20으로 암호화됨 - Poly1305 MAC(16바이트)으로 인증됨 - Bob이 세션을 Alice의 목적지에 바인딩하는 데 사용

**페이로드 섹션** (가변 길이로 암호화됨, +16바이트 MAC): - Garlic Clove(서브메시지 단위) 및 기타 블록을 포함함 - 첫 번째 블록으로 DateTime 블록을 반드시 포함해야 함 - 보통 애플리케이션 데이터가 포함된 Garlic Clove 블록을 포함함 - immediate ratchet(즉시 래칫)을 위한 NextKey 블록을 포함할 수 있음 - ChaCha20으로 암호화됨 - Poly1305 MAC (16바이트)으로 인증됨

**보안 속성:** - 임시 키는 전방 기밀성 요소를 제공한다 - 정적 키는 Alice를 인증한다(목적지에 바인딩) - 각 섹션은 도메인 분리를 위해 별도의 MAC을 사용한다 - 전체 핸드셰이크는 2개의 DH 연산을 수행한다 (es, ss)

### 바인딩 없는 NS 메시지 (유형 1c)

**사용 사례**: 응답을 기대하지도 원하지도 않는 원시 데이터그램

**총 길이**: 96 + payload_length 바이트

**형식**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**핵심 차이점**: Flags 섹션은 정적 키 대신 0으로 채워진 32바이트를 포함합니다.

**판별**: Bob은 32바이트 구간을 복호화하고 모든 바이트가 0인지 확인해 메시지 유형을 판별한다: - 모두 0 → Unbound session (바인딩되지 않은 세션) (type 1c) - 0이 아님 → Bound session with static key (정적 키로 바인딩된 세션) (type 1b)

**속성:** - static key(정적 키)가 없으므로 Alice의 Destination(목적지)에 바인딩되지 않음 - Bob은 응답을 보낼 수 없음(Destination을 알 수 없음) - DH(디피-헬먼) 연산을 단 1회만 수행 - "IK"(상호 정적 키 인지 패턴) 대신 Noise "N" pattern(상대 정적 키 미인지 패턴)을 따름 - 응답이 전혀 필요하지 않을 때 더 효율적임

**플래그 섹션** (향후 사용을 위해 예약됨): 현재는 모두 0입니다. 향후 버전에서 feature negotiation(기능 협상)에 사용될 수 있습니다.

### NS 일회성 메시지 (Type 1d)

**사용 사례**: 세션 없이 회신도 기대하지 않는 단일 익명 메시지

**총 길이**: 96 + payload_length 바이트

**형식**: 바인딩 없는 NS와 동일함 (type 1c)

**구분**:  - Type 1c는 동일한 세션에서 여러 메시지를 보낼 수 있습니다 (ES 메시지가 뒤따릅니다) - Type 1d는 세션 수립 없이 정확히 하나의 메시지만 보냅니다 - 실제 구현에서는 초기에는 이를 동일하게 취급할 수 있습니다

**속성:** - 최대 익명성 (정적 키 없음, 세션 없음) - 양측 모두 세션 상태를 유지하지 않음 - Noise "N" 패턴을 따름 - 단일 DH(디피-헬만) 연산 (es)

### 새 세션 응답(NSR) 메시지

Bob은 Alice의 NS 메시지에 응답하여 하나 이상의 NSR 메시지를 전송한다. NSR은 Noise IK handshake(Noise 프로토콜의 IK 방식 핸드셰이크)를 완료하고 양방향 세션을 수립한다.

**총 길이**: 72 + payload_length 바이트

**형식**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**필드 세부 정보:**

**세션 태그** (8바이트, 평문): - NSR(약어) 태그 세트에서 생성됨 (KDF(키 유도 함수) 섹션 참조) - 이 응답을 Alice의 NS(약어) 메시지와 연관시킴 - Alice가 이 NSR이 어떤 NS에 응답하는지 식별할 수 있게 함 - 일회용 (재사용하지 않음)

**Ephemeral Public Key** (임시 공개키) (32바이트, 평문): - Bob의 일회용 X25519 공개키 - Elligator2로 인코딩됨 - 각 NSR 메시지마다 새로 생성됨 - 전송되는 각 NSR마다 서로 달라야 함

**키 섹션 MAC** (16바이트): - 빈 데이터(ZEROLEN)를 인증함 - Noise IK 프로토콜(se pattern: static-ephemeral 패턴)의 일부 - 해시 트랜스크립트(hash transcript)를 연관 데이터(associated data)로 사용 - NSR을 NS에 바인딩하는 데 핵심적

**Payload Section** (가변 길이): - garlic cloves(갈릭 메시지의 하위 메시지 단위)와 블록을 포함 - 보통 애플리케이션 계층 응답을 포함 - 비어 있을 수 있음(ACK-only NSR) - 최대 크기: 65519바이트(65535 - 16바이트 MAC)

**여러 개의 NSR 메시지:**

Bob은 하나의 NS에 대한 응답으로 여러 개의 NSR 메시지를 보낼 수 있습니다: - 각 NSR에는 고유한 임시 키가 있습니다 - 각 NSR에는 고유한 세션 태그가 있습니다 - Alice는 가장 먼저 수신된 NSR을 사용해 핸드셰이크를 완료합니다 - 다른 NSR들은 (패킷 손실 발생 시를 대비한) 중복입니다

**중요 타이밍:** - Alice는 ES 메시지를 보내기 전에 NSR을 하나 수신해야 합니다 - Bob은 ES 메시지를 보내기 전에 ES 메시지 하나를 수신해야 합니다 - NSR은 split() 연산을 통해 양방향 세션 키를 설정합니다

**보안 속성:** - Noise IK 핸드셰이크를 완료함 - 추가로 2개의 Diffie-Hellman(DH) 연산을 수행함(ee, se) - NS+NSR 전반에 걸쳐 총 4회의 DH 연산 - 상호 인증(Level 2)을 달성함 - NSR 페이로드에 대해 약한 Forward Secrecy(순방향 기밀성) (Level 4)을 제공함

### 기존 세션(ES) 메시지

NS/NSR 핸드셰이크 이후의 모든 메시지는 Existing Session(기존 세션) 형식을 사용한다. ES 메시지는 Alice와 Bob 모두에 의해 양방향으로 사용된다.

**총 길이**: 8 + payload_length + 16 바이트 (최소 24 바이트)

**형식**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**필드 세부 정보:**

**세션 태그** (8바이트, 평문): - 현재 발신 태그셋에서 생성됨 - 세션과 메시지 번호를 식별 - 수신자는 태그를 조회하여 세션 키와 논스를 찾음 - 일회용(각 태그는 정확히 한 번만 사용됨) - 형식: HKDF 출력의 처음 8바이트

**페이로드 섹션** (가변 길이): - Garlic Clove(garlic encryption에서의 개별 메시지 단위)와 블록을 포함 - 필수 블록 없음(비어 있을 수 있음) - 일반적인 블록: Garlic Clove, NextKey, ACK, ACK Request, Padding - 최대 크기: 65519 바이트 (65535 - 16 바이트 MAC)

**MAC** (16바이트): - Poly1305 인증 태그 - 전체 페이로드에 대해 계산됨 - 연관 데이터: 8바이트 세션 태그 - 올바르게 검증되어야 하며 그렇지 않으면 메시지가 거부됨

**태그 조회 과정:**

1. 수신자는 8바이트 태그를 추출한다
2. 현재의 모든 인바운드 태그셋에서 태그를 조회한다
3. 연관된 세션 키와 메시지 번호 N을 가져온다
4. 논스를 구성한다: `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. 태그를 연관 데이터로 하여 AEAD(연관 데이터가 있는 인증 암호화)를 사용해 페이로드를 복호화한다
6. 태그셋에서 태그를 제거한다(일회용)
7. 복호화된 블록을 처리한다

**세션 태그를 찾을 수 없음:**

태그가 어떤 태그 세트에서도 발견되지 않는 경우: - NS 메시지일 수 있음 → NS 복호화 시도 - NSR 메시지일 수 있음 → NSR 복호화 시도 - 순서가 뒤바뀐 ES일 수 있음 → 태그 세트 업데이트를 잠시 기다림 - 재전송 공격일 수 있음 → 거부 - 손상된 데이터일 수 있음 → 거부

**빈 페이로드:**

ES 메시지는 빈 페이로드(0바이트)를 가질 수 있습니다: - ACK 요청이 수신되었을 때 명시적인 ACK(확인 응답)으로 동작함 - 애플리케이션 데이터 없이 프로토콜 계층의 응답을 제공함 - 여전히 세션 태그를 소모함 - 상위 계층에서 즉시 보낼 데이터가 없을 때 유용함

**보안 속성:** - NSR 수신 후 완전한 전방향 기밀성(레벨 5) - AEAD(연관 데이터를 포함한 인증 암호)를 통한 인증 암호화 - 태그가 추가적인 연관 데이터로 작용 - ratchet(키 갱신 메커니즘)이 필요해지기 전에 태그 세트당 최대 65535개의 메시지

---

## 키 유도 함수

이 섹션에서는 ECIES(타원곡선 통합 암호화 방식)에서 사용되는 모든 KDF(키 파생 함수) 연산을 문서화하고, 완전한 암호학적 유도 과정을 보여 줍니다.

### 표기법과 상수

**상수:** - `ZEROLEN` - 길이가 0인 바이트 배열(빈 문자열) - `||` - 연결 연산자

**변수:** - `h` - 트랜스크립트의 누적 해시 (32바이트) - `chainKey` - HKDF용 체인 키 (32바이트) - `k` - 대칭 암호 키 (32바이트) - `n` - 논스 / 메시지 번호

**키:** - `ask` / `apk` - 앨리스의 정적 개인/공개 키 - `aesk` / `aepk` - 앨리스의 임시 개인/공개 키 - `bsk` / `bpk` - 밥의 정적 개인/공개 키 - `besk` / `bepk` - 밥의 임시 개인/공개 키

### NS 메시지 키 파생 함수

### KDF 1: 초기 체인 키

프로토콜 초기화 시 한 번 수행됨(사전에 계산 가능):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**결과:** - `chainKey` = 이후 모든 KDF(키 유도 함수)에 대한 초기 체이닝 키 - `h` = 초기 해시 트랜스크립트

### KDF 2: Bob의 정적 키 혼합

Bob은 이 작업을 한 번만 수행한다(모든 인바운드 세션에 대해 미리 계산할 수 있음):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3: 앨리스의 임시 키 생성

Alice는 각 NS 메시지마다 새로운 키를 생성합니다:

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4: NS 정적 키 섹션 (es DH, 일시적-정적 Diffie-Hellman)

앨리스의 정적 키를 암호화하기 위한 키를 파생한다:

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: NS 페이로드 섹션 (ss DH, 바인딩 전용)

바인딩된 세션의 경우, 페이로드 암호화를 위해 두 번째 DH(Diffie-Hellman 키 교환)를 수행하십시오:

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**중요 사항:**

1. **Bound vs Unbound**: 
   - Bound는 DH(Diffie-Hellman) 연산을 2회 수행함 (es + ss)
   - Unbound는 DH 연산을 1회 수행함 (es만)
   - Unbound는 새 키를 도출하는 대신 nonce(논스)를 증가시킴

2. **키 재사용 안전성**:
   - 서로 다른 논스(0 vs 1)는 키/논스 재사용을 방지한다
   - 서로 다른 연관 데이터(h가 다름)는 도메인 분리를 제공한다

3. **해시 트랜스크립트**:
   - `h`에는 이제 다음이 포함됩니다: protocol_name, 비어 있는 prologue, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - 이 트랜스크립트는 NS message(NS 메시지)의 모든 부분을 하나로 결합합니다

### NSR 응답 태그 집합 키 파생 함수

Bob은 NSR 메시지용 태그를 생성합니다:

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### NSR 메시지 KDF(키 파생 함수)

### KDF 6: NSR 임시 키 생성

Bob은 각 NSR에 대해 새로운 임시 키를 생성한다:

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7: NSR 키 섹션 (ee 및 se DH)

NSR 키 섹션에 사용할 키를 파생합니다:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**중요**: 이것으로 Noise IK 핸드셰이크가 완료됩니다. `chainKey`에는 이제 4가지 DH(디피-헬만) 연산(es, ss, ee, se)에서 나온 모든 값이 반영되어 있습니다.

### KDF 8: NSR 페이로드 섹션

NSR(특정 프로토콜/메시지 형식의 약어) 페이로드 암호화를 위한 키를 파생합니다:

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**중요 사항:**

1. **Split Operation(분할 연산)**: 
   - 각 방향마다 독립적인 키를 생성
   - Alice→Bob 및 Bob→Alice 간의 키 재사용을 방지

2. **NSR 페이로드 바인딩**:
   - `h`를 연관 데이터(associated data)로 사용하여 페이로드를 핸드셰이크에 바인딩
   - 별도의 KDF ("AttachPayloadKDF")가 도메인 분리를 제공

3. **ES(메시지) 준비 상태**:
   - NSR(메시지) 이후, 양측은 ES 메시지를 보낼 수 있다
   - Alice는 ES를 보내기 전에 NSR을 수신해야 한다
   - Bob은 ES를 보내기 전에 ES를 수신해야 한다

### ES 메시지 키 파생 함수

ES 메시지는 tagsets(태그셋)에서 미리 생성된 세션 키를 사용합니다:

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**수신 프로세스:**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### DH_INITIALIZE 함수

한 방향용 태그 집합을 생성합니다:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**사용 맥락:**

1. **NSR Tagset(태그셋)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Ratcheted(래칫) Tagsets**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## 래칫 메커니즘

ECIES(타원곡선 통합 암호 체계)는 서로 동기화된 세 가지 ratchet(래칫) 메커니즘을 사용하여 전방향 기밀성과 효율적인 세션 관리를 제공합니다.

### Ratchet(래칫) 개요

**세 가지 Ratchet(단계적 키 갱신 메커니즘) 유형:**

1. **DH 래칫**: 새로운 루트 키를 생성하기 위해 디피-헬만 키 교환을 수행한다
2. **세션 태그 래칫**: 일회용 세션 태그를 결정적으로 파생한다
3. **대칭 키 래칫**: 메시지 암호화를 위한 세션 키를 파생한다

**관계:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**주요 속성:**

- **송신자**: 필요할 때 태그와 키를 생성(저장 필요 없음)
- **수신자**: look-ahead window(선행 윈도우)를 위해 태그를 미리 생성(저장 필요)
- **동기화**: 태그 인덱스가 키 인덱스를 결정 (N_tag = N_key)
- **전방향 기밀성**: 주기적 DH ratchet(DH 래칫)으로 달성
- **효율성**: 수신자는 태그를 받을 때까지 키 계산을 지연할 수 있음

### DH Ratchet(디피-헬만 기반의 단계적 키 갱신 기법)

DH ratchet(디피-헬먼 기반 키 래칫 메커니즘)은 주기적으로 새로운 임시 키를 교환하여 전방향 기밀성을 제공합니다.

### DH Ratchet(디피-헬만 기반 키 래칫) 빈도

**필수 Ratchet(암호 프로토콜의 단계적 키 갱신 메커니즘) 조건:** - 태그 집합이 소진에 임박함 (태그 65535가 최대치) - 구현별 정책:   - 메시지 수 임계값 (예: 매 4096개 메시지마다)   - 시간 임계값 (예: 매 10분마다)   - 데이터 용량 임계값 (예: 매 100 MB마다)

**권장되는 첫 번째 Ratchet(세션 키를 순차적으로 갱신하는 메커니즘)**: 제한에 도달하지 않도록 태그 번호를 4096 전후로

**최대값:** - **최대 태그 세트 ID**: 65535 - **최대 키 ID**: 32767 - **태그 세트당 최대 메시지 수**: 65535 - **세션당 이론상 최대 데이터**: ~6.9 TB (64K 태그 세트 × 64K 메시지 × 평균 1730바이트)

### DH Ratchet(디피-헬만 래칫) 태그 및 키 ID

**초기 태그 세트** (핸드셰이크 이후): - 태그 세트 ID: 0 - NextKey(다음 키) 블록이 아직 전송되지 않았음 - 키 ID가 할당되지 않음

**첫 번째 래칫 이후**: - 태그 세트 ID: 1 = (1 + Alice의 키 ID + Bob의 키 ID) = (1 + 0 + 0) - Alice는 키 ID 0을 사용한 NextKey(다음 키)를 보냄 - Bob은 키 ID 0을 사용한 NextKey로 응답함

**후속 태그 세트**: - 태그 세트 ID = 1 + 송신자의 키 ID + 수신자의 키 ID - 예: 태그 세트 5 = (1 + sender_key_2 + receiver_key_2)

**태그 세트 진행 표:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = 이번 ratchet(래칫)에서 새 키가 생성됨

**키 ID 규칙:** - ID는 0부터 순차적으로 부여됩니다 - 새 키가 생성될 때에만 ID가 증가합니다 - 최대 키 ID는 32767(15비트)입니다 - 키 ID 32767 이후에는 새 세션이 필요합니다

### DH 래칫 메시지 흐름

**역할:** - **태그 송신자**: 아웃바운드 태그 집합을 소유하고, 메시지를 보냄 - **태그 수신자**: 인바운드 태그 집합을 소유하고, 메시지를 받음

**패턴:** 태그 발신자는 태그 세트가 거의 소진되었을 때 ratchet(키를 단계적으로 갱신하는 메커니즘)을 개시한다.

**메시지 흐름 다이어그램:**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Ratchet(래칫) 패턴:**

**짝수 번호 태그 세트 생성** (2, 4, 6, ...): 1. 송신자는 새 키를 생성한다 2. 송신자는 새 키와 함께 NextKey block을 전송한다 3. 수신자는 이전 키 ID와 함께 NextKey block을 전송한다 (ACK, 확인 응답) 4. 양측은 (새 송신자 키 × 이전 수신자 키)로 DH(디피-헬만 키 교환)를 수행한다

**홀수 번호 태그 세트 생성** (3, 5, 7, ...): 1. 송신자는 역방향 키를 요청함(요청 플래그가 설정된 NextKey 전송) 2. 수신자는 새 키를 생성 3. 수신자는 새 키가 포함된 NextKey 블록을 전송 4. 양측은 (이전 송신자 키 × 새 수신자 키)로 DH(디피-헬만)를 수행

### NextKey(다음 키) 블록 형식

자세한 NextKey(다음 키) 블록 사양은 Payload Format 섹션을 참조하십시오.

**핵심 요소:** - **플래그 바이트**:   - 비트 0: 키 존재(1) 또는 ID만(0)   - 비트 1: 역방향 키(1) 또는 정방향 키(0)   - 비트 2: 역방향 키 요청(1) 또는 요청 없음(0) - **키 ID**: 2바이트, 빅엔디언(0-32767) - **공개 키**: 32바이트 X25519 (비트 0 = 1인 경우)

**NextKey 블록 예시:**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### DH 래칫 키 파생 함수

새 키가 교환될 때:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**중요한 타이밍:**

**태그 송신자:** - 새 아웃바운드 태그 세트를 즉시 생성합니다 - 새 태그를 즉시 사용하기 시작합니다 - 기존 아웃바운드 태그 세트를 삭제합니다

**태그 수신자:** - 새로운 인바운드 태그 세트를 생성 - 유예 기간(3분) 동안 기존 인바운드 태그 세트를 유지 - 유예 기간 동안 기존 및 새 태그 세트의 태그를 모두 수락 - 유예 기간 후 기존 인바운드 태그 세트를 삭제

### DH 래칫 상태 관리

**송신자 상태:** - 현재 발신 태그 세트 - 태그 세트 ID 및 키 ID - 다음 루트 키(다음 ratchet(단계적 키 갱신 메커니즘)용) - 현재 태그 세트의 메시지 수

**수신자 상태:** - 현재 인바운드 태그 세트(유예 기간 동안에는 2개일 수 있음) - 누락 감지를 위한 이전 메시지 번호(PN) - 사전 생성된 태그의 look-ahead window(선행 창) - 다음 루트 키(다음 ratchet(암호 키를 단계적으로 갱신하는 메커니즘)용)

**상태 전이 규칙:**

1. **첫 번째 Ratchet(암호 키 갱신 메커니즘) 이전**:
   - 태그 세트 0 사용(NSR에서)
   - 키 ID가 할당되지 않음

2. **Ratchet(래칫) 초기화**:
   - 새 키 생성(이번 라운드에서 발신자가 생성하는 경우)
   - ES message에 NextKey block 전송
   - 새 아웃바운드 tag set 생성 전에 NextKey reply 대기

3. **Ratchet(래칫, 연속적 키 갱신 메커니즘) 요청 수신**:
   - 새 키 생성(이번 라운드에서 수신자가 생성자일 경우)
   - 수신한 키로 Diffie-Hellman(DH) 수행
   - 새 인바운드 태그 세트 생성
   - NextKey(다음 키) 응답 전송
   - 유예 기간 동안 기존 인바운드 태그 세트 유지

4. **Ratchet(래칫, 단계적 키 갱신) 완료**:
   - NextKey 응답 수신
   - 디피-헬만 키 교환 수행
   - 새 아웃바운드 태그 세트 생성
   - 새 태그 사용 시작

### 세션 태그 래칫

session tag ratchet(세션 태그를 위한 암호화 래칫 메커니즘)은 일회용 8바이트 세션 태그를 결정적으로 생성한다.

### Session Tag Ratchet(Session Tag를 전진 갱신하는 암호학적 메커니즘)의 목적

- 명시적 태그 전송을 대체함 (ElGamal은 32바이트 태그를 전송했음)
- 수신자가 look-ahead window(선행 윈도우)를 위해 태그를 사전 생성할 수 있게 함
- 송신자는 요청 시 생성함 (저장 필요 없음)
- 인덱스를 통해 symmetric key ratchet(대칭키 래칫, 단계적으로 대칭키를 갱신하는 메커니즘)과 동기화됨

### 세션 태그 래칫 공식

**초기화:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**태그 생성(태그 N에 대해):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**전체 시퀀스:**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Session Tag Ratchet(세션 태그를 단계적으로 교체하는 메커니즘) 송신자 구현

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**송신 프로세스:** 1. 각 메시지마다 `get_next_tag()`를 호출 2. 반환된 태그를 ES 메시지에 사용 3. 잠재적인 ACK(확인 응답) 추적을 위해 인덱스 N을 저장 4. 태그 저장이 필요 없음(필요 시 생성됨)

### 세션 태그 Ratchet(키 갱신 메커니즘) 수신자 구현

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**수신 프로세스:** 1. look-ahead window(선행 윈도우)용 태그를 미리 생성한다(예: 태그 32개) 2. 태그를 해시 테이블 또는 사전에 저장한다 3. 메시지가 도착하면 태그를 조회하여 인덱스 N을 얻는다 4. 저장소에서 태그를 제거한다(1회용) 5. 태그 수가 임계값 아래로 떨어지면 윈도우를 확장한다

### 세션 태그 사전 준비 전략

**목적**: 메모리 사용량과 순서가 어긋난 메시지 처리 간의 균형 조정

**권장 룩어헤드 크기:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**적응형 전방 탐색:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**뒤쪽 자르기:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**메모리 계산:**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Session Tag(세션 태그) 순서 뒤바뀜 처리

**시나리오**: 메시지가 순서대로 도착하지 않음

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**수신자 동작:**

1. tag_5 수신:
   - 조회: 인덱스 5에서 찾음
   - 메시지 처리
   - tag_5 제거
   - 최대 수신값: 5

2. tag_7 수신 (순서 어긋남):
   - 조회: 인덱스 7에서 발견
   - 메시지 처리
   - tag_7 제거
   - 최고 수신 번호: 7
   - 참고: tag_6은 여전히 저장소에 있음 (아직 수신되지 않음)

3. tag_6 수신(지연됨):
   - 조회: 인덱스 6에서 찾음
   - 메시지 처리
   - tag_6 제거
   - 최대 수신값: 7 (변경 없음)

4. tag_8 수신:
   - 조회: 인덱스 8에서 찾음
   - 메시지 처리
   - tag_8 제거
   - 가장 높은 수신 번호: 8

**윈도우 관리:** - 수신된 인덱스의 최댓값을 추적 - 누락된 인덱스(갭) 목록 유지 - 최댓값 인덱스를 기준으로 윈도우 확장 - 선택 사항: 타임아웃 후 오래된 갭 만료

### 대칭 키 래칫

symmetric key ratchet(대칭키 래칫)은 session tags(세션 태그)와 동기화된 32바이트 암호화 키를 생성합니다.

### Symmetric Key Ratchet(대칭 키 래칫)의 목적

- 각 메시지마다 고유한 암호화 키 제공
- session tag ratchet(세션 태그 래칫, 단계적 키 갱신 메커니즘)과 동기화됨(같은 인덱스)
- 송신자는 필요 시 생성 가능
- 수신자는 태그를 받을 때까지 생성을 지연할 수 있음

### 대칭 키 래칫 공식

**초기화:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**키 생성(키 N용):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**전체 시퀀스:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Symmetric Key Ratchet(대칭키 래칫) 송신자 구현

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**송신자 프로세스:** 1. 다음 태그와 해당 인덱스 N을 가져온다 2. 인덱스 N에 대한 키를 생성한다 3. 키를 사용하여 메시지를 암호화한다 4. 키 저장이 필요하지 않다

### 대칭 키 래칫 수신자 구현

**전략 1: 지연 생성 (권장)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**지연 생성 프로세스:** 1. 태그가 포함된 ES message(ES 메시지)를 수신 2. 태그를 조회해 인덱스 N을 얻음 3. (아직 생성되지 않았다면) 키 0부터 N까지 생성 4. 키 N으로 메시지를 복호화 5. Chain key(체인 키)는 이제 인덱스 N에 위치함

**장점:** - 메모리 사용량 최소화 - 필요할 때에만 키 생성 - 구현이 단순함

**단점:** - 최초 사용 시 0부터 N까지 모든 키를 생성해야 함 - 캐싱 없이는 순서가 뒤바뀐 메시지를 처리할 수 없음

**전략 2: 태그 윈도우 기반 사전 생성 (대안)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**사전 생성 프로세스:** 1. tag window(태그 윈도우)에 맞춰 키를 미리 생성 (예: 키 32개) 2. 메시지 번호로 인덱싱하여 키를 저장 3. 태그를 수신하면 해당 키를 조회 4. 태그가 사용됨에 따라 윈도우를 확장

**장점:** - 순서가 뒤바뀐 메시지도 자연스럽게 처리 - 빠른 키 조회(생성 지연 없음)

**단점:** - 메모리 사용량 증가 (키당 32바이트 대 태그당 8바이트) - 키를 태그와 동기화된 상태로 유지해야 함

**메모리 비교:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Session Tags(세션 태그)를 이용한 대칭 래칫 동기화

**중대한 요구 사항**: 세션 태그 인덱스는 대칭 키 인덱스와 반드시 동일해야 한다

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**실패 모드:**

동기화가 깨지면: - 복호화에 잘못된 키가 사용됨 - MAC(메시지 인증 코드) 검증 실패 - 메시지가 거부됨

**예방:** - 태그와 키에 동일한 인덱스를 항상 사용하십시오 - 어느 쪽의 ratchet(암호 키 발전 메커니즘)에서도 인덱스를 건너뛰지 마십시오 - 순서가 어긋난 메시지는 신중하게 처리하십시오

### 대칭 래칫 논스 구성

Nonce(논스)는 메시지 번호에서 파생됩니다:

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**예시:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**중요한 속성:** - nonce(논스)는 tagset(태그 집합) 내 각 메시지마다 고유합니다 - nonce는 절대 반복되지 않습니다(일회용 태그가 이를 보장합니다) - 8바이트 카운터는 2^64개의 메시지를 허용합니다(우리는 2^16만 사용합니다) - nonce 형식은 RFC 7539의 카운터 기반 구성과 일치합니다

---

## 세션 관리

### 세션 컨텍스트

모든 인바운드 및 아웃바운드 세션은 특정 컨텍스트에 속해야 합니다:

1. **Router 컨텍스트**: router 자체용 세션
2. **Destination 컨텍스트**: 특정 로컬 destination(I2P 목적지) (클라이언트 애플리케이션)을 위한 세션

**중요 규칙**: 상관관계 공격을 방지하기 위해 세션은 컨텍스트 간에 절대 공유되어서는 안 됩니다.

**구현:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Java I2P 구현:**

Java I2P에서, `SessionKeyManager` 클래스는 다음 기능을 제공합니다: - router마다 하나의 `SessionKeyManager` - 로컬 destination(목적지)마다 하나의 `SessionKeyManager` - 각 컨텍스트 내에서 ECIES(타원 곡선 기반 공개키 암호 방식)와 ElGamal(공개키 암호 체계) 세션을 분리하여 관리

### 세션 바인딩

**Binding**(바인딩)은 세션을 특정 원격단 목적지와 연관합니다.

### 바인딩된 세션

**특징:** - NS 메시지에 송신자의 정적 키 포함 - 수신자는 송신자의 목적지를 식별할 수 있음 - 양방향 통신을 가능하게 함 - 목적지당 단일 발신 세션 - 여러 수신 세션이 있을 수 있음(전환 중)

**사용 사례:** - 스트리밍 연결(TCP 유사) - 회신 가능한 데이터그램 - 요청/응답이 필요한 모든 프로토콜

**바인딩 프로세스:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**이점:** 1. **Ephemeral-Ephemeral DH**(일시적-일시적 디피-헬먼 키 교환): 응답은 ee DH를 사용함(완전한 순방향 기밀성) 2. **세션 연속성**: Ratchets(래칫 기반 키 갱신 메커니즘)가 동일한 목적지에 대한 바인딩을 유지 3. **보안**: 세션 하이재킹을 방지(정적 키로 인증됨) 4. **효율성**: 목적지당 단일 세션(중복 없음)

### 바인딩되지 않은 세션

**특징:** - NS 메시지에 고정 키가 없음(플래그 섹션은 모두 0) - 수신자는 발신자를 식별할 수 없음 - 단방향 통신만 가능 - 동일한 destination(목적지)에 여러 세션 허용

**사용 사례:** - 원시 데이터그램 (fire-and-forget(보낸 뒤 확인하지 않음)) - 익명 게시 - 방송형 메시징

**특성:** - 더 높은 익명성 (발신자 식별 없음) - 더 높은 효율 (핸드셰이크에서 1 DH 대 2 DH) - 응답 불가 (수신자가 어디로 응답해야 할지 모름) - session ratcheting(세션 키를 점진적으로 갱신하는 메커니즘) 없음 (일회성 또는 제한적 사용)

### 세션 페어링

**Pairing(페어링)** 은 양방향 통신을 위해 인바운드 세션과 아웃바운드 세션을 연결합니다.

### 페어링된 세션 생성

**Alice의 관점 (개시자):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Bob의 관점(응답자):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### 세션 페어링의 이점

1. **인밴드 ACK**: 별도의 clove(garlic encryption에서 개별 메시지 단위) 없이 메시지를 수신 확인할 수 있음
2. **효율적인 Ratcheting(세션 키를 단계적으로 갱신하는 래칫 기법)**: 양 방향이 함께 래칫을 진행함
3. **흐름 제어**: 쌍으로 연결된 세션 전반에 걸쳐 back-pressure(소비 속도에 맞춰 전송을 억제하는 메커니즘)를 구현할 수 있음
4. **상태 일관성**: 동기화된 상태를 더 쉽게 유지할 수 있음

### 세션 페어링 규칙

- 아웃바운드 세션은 페어링되지 않았을 수 있음 (바인딩되지 않은 NS)
- 바인딩된 NS의 인바운드 세션은 페어링되어야 함
- 페어링은 세션 생성 시에 이루어지며, 그 이후에는 이루어지지 않음
- 페어링된 세션은 동일한 목적지 바인딩을 가짐
- 래칫은 독립적으로 발생하지만 조율됨

### 세션 수명주기

### 세션 수명 주기: 생성 단계

**아웃바운드 세션 생성 (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**인바운드 세션 생성 (Bob):**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### 세션 수명 주기: 활성 단계

**상태 전이:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**활성 세션 유지 관리:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### 세션 수명주기: 만료 단계

**세션 타임아웃 값:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**만료 로직:**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**중요 규칙**: 동기화가 어긋나는 것을 방지하기 위해 아웃바운드 세션은 인바운드 세션보다 반드시 먼저 만료되어야 합니다.

**정상 종료:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### 복수의 NS 메시지

**시나리오**: Alice의 NS 메시지가 손실되었거나 NSR 응답이 손실된 경우.

**Alice의 동작:**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**중요한 속성:**

1. **고유한 임시 키**: 각 NS(핸드셰이크 시작 메시지)는 서로 다른 임시 키를 사용함
2. **독립적인 핸드셰이크**: 각 NS는 별도의 핸드셰이크 상태를 생성함
3. **NSR 연관**: NSR(해당 NS에 대한 응답 메시지) 태그는 어떤 NS에 대한 응답인지 식별함
4. **상태 정리**: NSR이 성공하면 사용되지 않은 NS 상태는 폐기됨

**공격 방지:**

리소스 고갈을 방지하기 위해:

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### 여러 NSR(NTCP2의 세션 요청 메시지) 메시지

**시나리오**: Bob이 여러 개의 NSR(응답 메시지)을 전송한다(예: 응답 데이터가 여러 메시지로 분할된 경우).

**Bob의 동작:**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**앨리스의 동작:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Bob의 정리:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**중요한 속성:**

1. **여러 개의 NSR 허용**: Bob은 NS당 여러 개의 NSR을 보낼 수 있다
2. **서로 다른 임시 키**: 각 NSR은 고유한 임시 키를 사용해야 한다
3. **동일한 NSR Tagset**: 하나의 NS에 대한 모든 NSR은 동일한 tagset(태그 집합)을 사용한다
4. **먼저 도착한 ES가 승리**: Alice의 첫 ES가 어떤 NSR이 성공했는지 결정한다
5. **ES 이후 정리**: Bob은 ES를 받은 후 사용되지 않은 상태를 폐기한다

### 세션 상태 머신

**전체 상태 다이어그램:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**상태 설명:**

- **NEW**: 아웃바운드 세션이 생성되었으며, 아직 NS를 보내지 않음
- **PENDING_REPLY**: NS를 전송했으며, NSR을 대기 중
- **AWAITING_ES**: NSR을 전송했으며, Alice로부터 첫 번째 ES를 대기 중
- **ESTABLISHED**: 핸드셰이크가 완료되어 ES를 송수신할 수 있음
- **ACTIVE**: ES 메시지를 활발히 교환 중
- **RATCHETING**: DH ratchet(디피-헬만 기반 키 갱신 래칫) 진행 중 (ACTIVE의 하위 상태)
- **EXPIRED**: 세션이 타임아웃되어 삭제 대기 중
- **TERMINATED**: 세션이 명시적으로 종료됨

---

## 페이로드 형식

모든 ECIES(타원곡선 통합 암호화 방식) 메시지(NS, NSR, ES)의 페이로드 섹션은 NTCP2와 유사한 블록 기반 형식을 사용합니다.

### 블록 구조

**일반 형식:**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 1바이트 - 블록 유형 번호
- `size`: 2바이트 - 빅엔디언 형태의 데이터 필드 크기 (0-65516)
- `data`: 가변 길이 - 블록별 데이터

**제약 사항:**

- 최대 ChaChaPoly(ChaCha20-Poly1305 조합) 프레임: 65535 바이트
- Poly1305 MAC(메시지 인증 코드): 16 바이트
- 블록 총합의 최대 크기: 65519 바이트 (65535 - 16)
- 단일 블록의 최대 크기: 65519 바이트 (3바이트 헤더 포함)
- 단일 블록 데이터의 최대 크기: 65516 바이트

### 블록 유형

**정의된 블록 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**알 수 없는 블록 처리:**

구현체는 알 수 없는 타입 번호의 블록을 반드시 무시하고 패딩으로 취급해야 한다. 이는 전방 호환성을 보장한다.

### 블록 순서 규칙

### NS 메시지 순서

**필수:** - DateTime 블록은 반드시 맨 앞에 와야 합니다

**허용됨:** - Garlic Clove (garlic 메시지를 구성하는 단위) (유형 11) - 옵션 (유형 5) - 구현된 경우 - 패딩 (유형 254)

**금지:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**유효한 NS 페이로드 예시:**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### NSR 메시지 순서

**필수:** - 없음 (페이로드는 비어 있을 수 있음)

**허용:** - Garlic Clove(garlic 메시지 내부의 개별 메시지 단위) (유형 11) - 옵션 (유형 5) - 구현된 경우 - 패딩 (유형 254)

**금지:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**유효한 NSR 페이로드 예시:**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
또는

```
(empty - ACK only)
```
### ES 메시지 순서

**필수:** - 없음 (페이로드가 비어 있을 수 있음)

**허용됨(순서는 무관):** - Garlic Clove (type 11) - NextKey (type 7) - ACK (type 8) - ACK Request (type 9) - Termination (type 4) - 구현된 경우 - MessageNumbers (type 6) - 구현된 경우 - Options (type 5) - 구현된 경우 - Padding (type 254)

**특별 규칙:** - Termination(종료) 블록은 반드시 마지막 블록이어야 함(단, Padding(패딩)이 있을 경우 Padding이 마지막) - Padding 블록은 반드시 마지막 블록이어야 함 - Garlic Cloves(Garlic 메시지의 하위 메시지) 다수 허용 - NextKey(다음 키) 블록은 최대 2개까지 허용(순방향 및 역방향) - Padding 블록 다수는 허용되지 않음

**유효한 ES 페이로드 예시:**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### DateTime 블록 (유형 0)

**목적**: replay(재전송 공격) 방지 및 clock skew(시계 오차) 검증을 위한 타임스탬프

**크기**: 7바이트 (3바이트 헤더 + 4바이트 데이터)

**형식:**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 0
- `size`: 4 (big-endian(빅엔디언))
- `timestamp`: 4바이트 - 초 단위의 유닉스 타임스탬프(부호 없는, big-endian)

**타임스탬프 형식:**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**유효성 검사 규칙:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**재전송 공격 방지:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**구현 참고 사항:**

1. **NS Messages**(NS 메시지): DateTime은 반드시 첫 번째 블록이어야 함
2. **NSR/ES Messages**(NSR/ES 메시지): DateTime은 일반적으로 포함되지 않음
3. **Replay Window**(리플레이 윈도우): 최소 권장값은 5분
4. **Bloom Filter**(블룸 필터): 효율적인 리플레이 탐지를 위해 권장됨
5. **Clock Skew**(시계 오차): 과거 5분, 미래 2분 허용

### Garlic Clove Block (garlic encryption에서 개별 클로브를 담는 블록) (유형 11)

**목적**: 전달을 위해 I2NP 메시지를 캡슐화합니다

**형식:**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 11
- `size`: clove(garlic encryption에서의 개별 메시지 단위)의 총 크기(가변)
- `Delivery Instructions`: I2NP 사양에 명시된 대로
- `type`: I2NP 메시지 유형(1바이트)
- `Message_ID`: I2NP 메시지 ID(4바이트)
- `Expiration`: 초 단위 Unix 타임스탬프(4바이트)
- `I2NP Message body`: 가변 길이의 메시지 데이터

**전달 지시 형식:**

**Local Delivery(로컬 전달)** (1바이트):

```
+----+
|0x00|
+----+
```
**목적지 전달** (33 바이트):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Router 전달** (33 바이트):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Tunnel 전달** (37 바이트):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**I2NP 메시지 헤더** (총 9바이트):

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: I2NP 메시지 유형 (Database Store, Database Lookup, Data 등)
- `msg_id`: 4바이트 메시지 식별자
- `expiration`: 4바이트 유닉스 타임스탬프 (초)

**ElGamal Clove 형식과의 중요한 차이점:**

1. **인증서 없음**: 인증서 필드를 생략함 (ElGamal(엘가말, 공개키 암호 방식)에서는 사용되지 않음)
2. **Clove ID 없음**: Clove(I2P 메시지 내부의 서브메시지 단위) ID를 생략함 (항상 0이었음)
3. **Clove 만료 시간 없음**: 대신 I2NP 메시지 만료 시간을 사용함
4. **간결한 헤더**: 9바이트 I2NP 헤더 vs 더 큰 ElGamal 형식
5. **각 Clove는 별도의 블록**: CloveSet(여러 Clove를 묶는 구조) 구조 없음

**여러 개의 Clove(클로브: 하나의 garlic 메시지 안에 포장되는 개별 하위 메시지 단위):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Cloves(garlic encryption 메시지의 하위 메시지 단위)에서 일반적인 I2NP 메시지 유형:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Clove(클로브, garlic 메시지의 하위 메시지) 처리:**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### NextKey 블록 (유형 7)

**목적**: DH ratchet(디피-헬만 기반 래칫) 키 교환

**형식 (키 존재 - 38바이트):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**형식 (Key ID만 - 6바이트):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**필드:**

- `blk`: 7
- `size`: 3 (ID만) 또는 35 (키 포함)
- `flag`: 1 바이트 - 플래그 비트
- `key ID`: 2 바이트 - 빅 엔디안 키 식별자(0-32767)
- `Public Key`: 32 바이트 - X25519 공개 키(리틀 엔디안), 플래그 비트 0 = 1인 경우

**플래그 비트:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**플래그 예시:**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**키 ID 규칙:**

- ID는 순차적임: 0, 1, 2, ..., 32767
- ID는 새 키가 생성될 때에만 증가함
- 다음 ratchet(래칫, 단계적 키 갱신 메커니즘) 전까지는 여러 메시지에 동일한 ID가 사용됨
- 최대 ID는 32767 (그 이후에는 새 세션을 시작해야 함)

**사용 예시:**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**처리 로직:**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**여러 개의 NextKey Blocks(다음 키 블록):**

양방향에서 동시에 ratcheting(키를 단계적으로 갱신하는 절차)을 수행할 때, 단일 ES message는 최대 2개의 NextKey blocks를 포함할 수 있습니다:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### ACK(확인 응답) 블록 (유형 8)

**목적**: 수신된 메시지에 대한 수신 확인을 in-band(동일 채널 내에서)으로 수행

**형식 (단일 ACK - 7바이트):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**형식 (여러 개의 ACK(확인 응답)):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 8
- `size`: 4 * ACK의 개수(최소 4)
- 각 ACK에 대해:
  - `tagsetid`: 2바이트 - 빅엔디언 태그 세트 ID (0-65535)
  - `N`: 2바이트 - 빅엔디언 메시지 번호 (0-65535)

**태그 세트 ID 결정:**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**단일 ACK(확인 응답) 예시:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**여러 ACK(승인) 예시:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**처리:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**ACK(승인 응답)을 언제 보낼지:**

1. **명시적 ACK Request**: ACK Request 블록에는 항상 응답
2. **LeaseSet 전달**: 발신자가 메시지에 LeaseSet을 포함할 때
3. **세션 설정**: NS/NSR을 ACK할 수 있음(프로토콜은 ES를 통한 암시적 ACK를 선호함)
4. **Ratchet(단계적 키 갱신 메커니즘) 확인**: NextKey 수신을 ACK할 수 있음
5. **애플리케이션 계층**: 상위 계층 프로토콜의 요구에 따라(예: Streaming)

**ACK(승인) 타이밍:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### ACK 요청 블록 (타입 9)

**목적**: 현재 메시지에 대한 인밴드 수신 확인을 요청

**형식:**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**필드:**

- `blk`: 9
- `size`: 1
- `flg`: 1바이트 - 플래그(현재 모든 비트는 미사용이며 0으로 설정됨)

**사용법:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**수신자 응답:**

ACK 요청을 수신했을 때:

1. **즉시 데이터가 있는 경우**: 즉시 응답에 ACK(확인 응답) 블록을 포함
2. **즉시 데이터가 없는 경우**: 타이머를 시작하고(예: 100ms), 타이머가 만료되면 ACK와 함께 빈 ES를 전송
3. **태그 세트 ID**: 현재 인바운드 태그세트 ID를 사용
4. **메시지 번호**: 수신된 세션 태그에 연관된 메시지 번호를 사용

**처리:**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**ACK 요청을 언제 사용해야 하나요:**

1. **중요한 메시지**: 반드시 확인되어야 하는 메시지
2. **LeaseSet 전달**: LeaseSet을 함께 묶어 보낼 때
3. **세션 래칫**: NextKey block(다음 키 블록)을 전송한 뒤
4. **전송 종료**: 송신자가 더 보낼 데이터는 없지만 확인을 원할 때

**사용하지 말아야 할 때:**

1. **Streaming Protocol**: 스트리밍 계층이 ACK를 처리합니다
2. **High Frequency Messages**: 모든 메시지마다 ACK 요청을 피하세요(오버헤드)
3. **Unimportant Datagrams**: 원시 데이터그램은 일반적으로 ACK가 필요하지 않습니다

### 종료 블록 (유형 4)

**상태**: 미구현

**목적**: 세션을 정상적으로 종료

**형식:**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 4
- `size`: 1바이트 이상
- `rsn`: 1바이트 - 이유 코드
- `addl data`: 선택적 추가 데이터 (형식은 이유에 따라 다름)

**사유 코드:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**사용 방법(구현되면):**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**규칙:**

- Padding(패딩)을 제외하면 반드시 마지막 블록이어야 함
- 존재하는 경우 Padding은 Termination(종료) 뒤에 반드시 와야 함
- NS 또는 NSR 메시지에서는 허용되지 않음
- ES 메시지에서만 허용됨

### 옵션 블록 (타입 5)

**상태**: 미구현

**목적**: 세션 매개변수 협상

**형식:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 5
- `size`: 21바이트 이상
- `ver`: 1바이트 - 프로토콜 버전(0이어야 함)
- `flg`: 1바이트 - 플래그(현재 모든 비트 미사용)
- `STL`: 1바이트 - 세션 태그 길이(8이어야 함)
- `STimeout`: 2바이트 - 세션 유휴 타임아웃(초, 빅 엔디언)
- `SOTW`: 2바이트 - 송신자 아웃바운드 태그 윈도우(빅 엔디언)
- `RITW`: 2바이트 - 수신자 인바운드 태그 윈도우(빅 엔디언)
- `tmin`, `tmax`, `rmin`, `rmax`: 각 1바이트 - 패딩 파라미터(4.4 고정소수점)
- `tdmy`: 2바이트 - 보내려는 최대 더미 트래픽(바이트/초, 빅 엔디언)
- `rdmy`: 2바이트 - 요청된 더미 트래픽(바이트/초, 빅 엔디언)
- `tdelay`: 2바이트 - 삽입하려는 최대 메시지 내부 지연(밀리초, 빅 엔디언)
- `rdelay`: 2바이트 - 요청된 메시지 내부 지연(밀리초, 빅 엔디언)
- `more_options`: 가변 길이 - 향후 확장

**패딩 매개변수 (4.4 고정소수점):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Tag Window Negotiation(태그 윈도우 협상):**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**기본값(옵션이 협상되지 않은 경우):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### MessageNumbers(메시지 번호) 블록 (유형 6)

**상태**: 미구현

**목적**: 이전 태그 세트에서 전송된 마지막 메시지를 표시하여 누락 감지를 가능하게 함

**형식:**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**필드:**

- `blk`: 6
- `size`: 2
- `PN`: 2바이트 - 이전 태그 세트의 마지막 메시지 번호(빅엔디언, 0-65535)

**PN (이전 번호) 정의:**

PN은 이전 태그 세트에서 보낸 마지막 태그의 인덱스입니다.

**사용법(구현되면):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**수신자 이점:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**규칙:**

- tag set(태그 세트) 0(이전 tag set 없음)에서는 절대 전송하면 안 됨
- ES 메시지에서만 전송됨
- 새로운 tag set의 최초 메시지(들)에서만 전송됨
- PN 값은 발신자 관점 기준임(발신자가 마지막으로 보낸 tag(태그))

**Signal과의 관계:**

Signal Double Ratchet(시그널 프로토콜의 더블 래칫 알고리즘)에서는 PN(이전 체인 길이)이 메시지 헤더에 포함된다. ECIES(타원곡선 통합 암호화 체계)에서는 암호화된 페이로드에 포함되며 선택 사항이다.

### 패딩 블록 (유형 254)

**목적**: 트래픽 분석 저항성과 메시지 크기 난독화

**형식:**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**필드:**

- `blk`: 254
- `size`: 0-65516 바이트 (빅엔디언)
- `padding`: 무작위 데이터 또는 0으로 채운 데이터

**규칙:**

- 반드시 메시지에서 마지막 블록이어야 함
- 여러 개의 패딩 블록은 허용되지 않음
- 길이가 0일 수 있음(3바이트 헤더만)
- 패딩 데이터는 0으로 채우거나 임의의 바이트일 수 있음

**기본 패딩:**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**트래픽 분석 저항 전략:**

**전략 1: 무작위 크기(기본값)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**전략 2: 배수로 반올림**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**전략 3: 고정 메시지 크기**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**전략 4: 협상된 패딩 (Options block(옵션 블록))**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**패딩 전용 메시지:**

메시지는 전적으로 패딩으로만 구성될 수 있습니다(애플리케이션 데이터 없음):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**구현 참고 사항:**

1. **올-제로 패딩**: 허용됨(ChaCha20(스트림 암호 알고리즘)에 의해 암호화됨)
2. **무작위 패딩**: 암호화 후에는 추가적인 보안을 제공하지 않지만 더 많은 엔트로피를 사용함
3. **성능**: 무작위 패딩 생성은 비용이 많이 들 수 있으므로 0 사용을 고려
4. **메모리**: 큰 패딩 블록은 대역폭을 소모하므로 최대 크기에 주의

---

## 구현 가이드

### 사전 준비 사항

**암호화 라이브러리:**

- **X25519**: libsodium, NaCl, 또는 Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+, 또는 Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle, 또는 언어의 내장 지원
- **Elligator2**: 라이브러리 지원이 제한적임; 사용자 정의 구현이 필요할 수 있음

**Elligator2(타원곡선 점을 무작위 데이터처럼 보이게 하는 매핑 기법) 구현:**

Elligator2(암호학적 매핑 기법)은 널리 구현되어 있지 않습니다. 옵션:

1. **OBFS4**: Tor의 obfs4 pluggable transport(플러그형 전송)는 Elligator2 구현을 포함합니다
2. **Custom Implementation**: [Elligator2 paper](https://elligator.cr.yp.to/elligator-20130828.pdf)를 기반으로 합니다
3. **kleshni/Elligator**: GitHub의 참조 구현

**Java I2P 참고:** Java I2P는 사용자 지정 Elligator2(암호학적 매핑 기법) 추가 기능이 포함된 net.i2p.crypto.eddsa 라이브러리를 사용합니다.

### 권장 구현 순서

**1단계: 핵심 암호 기술** 1. X25519 DH 키 생성 및 교환 2. ChaCha20-Poly1305 AEAD 암호화/복호화 3. SHA-256 해싱 및 MixHash 4. HKDF 키 파생 5. Elligator2 인코딩/디코딩(초기에는 테스트 벡터를 사용할 수 있음)

**2단계: 메시지 형식** 1. NS 메시지 (바인딩되지 않음) - 가장 단순한 형식 2. NS 메시지 (바인딩됨) - 정적 키 추가 3. NSR 메시지 4. ES 메시지 5. 블록 파싱 및 생성

**3단계: 세션 관리** 1. 세션 생성 및 저장 2. 태그 집합 관리(송신자와 수신자) 3. 세션 태그 ratchet(래칫: 단계적으로 키를 갱신하는 암호 메커니즘) 4. 대칭키 ratchet 5. 태그 조회 및 윈도우 관리

**4단계: DH 래칫팅** 1. NextKey 블록 처리 2. DH 래칫 KDF(키 유도 함수) 3. 래칫 이후 태그 세트 생성 4. 다중 태그 세트 관리

**5단계: 프로토콜 로직** 1. NS/NSR/ES 상태 머신 2. 재생 공격 방지 (DateTime(날짜/시간), Bloom filter(블룸 필터)) 3. 재전송 로직 (복수의 NS/NSR) 4. ACK(확인 응답) 처리

**6단계: 통합** 1. I2NP Garlic Clove(서브메시지 단위) 처리 2. LeaseSet 번들링 3. 스트리밍 프로토콜 통합 4. 데이터그램 프로토콜 통합

### 송신자 구현

**아웃바운드 세션 수명주기:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### 수신기 구현

**인바운드 세션 라이프사이클:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### 메시지 분류

**메시지 유형 구분:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### 세션 관리 모범 사례

**세션 저장소:**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**메모리 관리:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### 테스트 전략

**단위 테스트:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**통합 테스트:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**테스트 벡터:**

명세에 따른 테스트 벡터 구현:

1. **Noise IK Handshake** (Noise 프로토콜의 IK 핸드셰이크): 표준 Noise 테스트 벡터를 사용
2. **HKDF** (HMAC 기반 키 유도 함수): RFC 5869 테스트 벡터를 사용
3. **ChaCha20-Poly1305** (ChaCha20 스트림 암호와 Poly1305 인증을 결합한 AEAD 알고리즘): RFC 7539 테스트 벡터를 사용
4. **Elligator2** (타원곡선 공개키를 균일 분포처럼 위장하는 매핑): Elligator2 논문 또는 OBFS4의 테스트 벡터를 사용

**상호운용성 테스트:**

1. **Java I2P**: Java I2P 참조 구현을 대상으로 테스트
2. **i2pd**: C++ i2pd 구현을 대상으로 테스트
3. **패킷 캡처**: Wireshark dissector(프로토콜 해석기)를 사용해 메시지 형식을 검증(가능한 경우)
4. **교차 구현**: 서로 다른 구현 간 송수신이 가능한 테스트 하네스를 구축

### 성능 고려 사항

**키 생성:**

Elligator2(키를 무작위 바이트처럼 보이게 인코딩하는 기법) 키 생성은 연산 비용이 큽니다(거부율 50%):

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**태그 조회:**

O(1) 태그 조회를 위해 해시 테이블을 사용하십시오:

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**메모리 최적화:**

대칭 키 생성 연기:

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**배치 처리:**

여러 메시지를 일괄 처리:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## 보안 고려사항

### 위협 모델

**공격자의 능력:**

1. **수동 관찰자**: 모든 네트워크 트래픽을 관찰할 수 있음
2. **능동 공격자**: 메시지를 삽입, 수정, 드롭(폐기), 재전송(리플레이)할 수 있음
3. **침해된 노드**: router 또는 목적지를 침해할 수 있음
4. **트래픽 분석**: 트래픽 패턴에 대한 통계적 분석을 수행할 수 있음

**보안 목표:**

1. **기밀성**: 관찰자가 메시지 내용을 볼 수 없음
2. **인증**: 발신자 신원 검증 (바운드 세션의 경우)
3. **전방향 기밀성**: 키가 유출되더라도 과거 메시지는 비밀로 유지됨
4. **재생 공격 방지**: 이전 메시지를 재전송할 수 없음
5. **트래픽 난독화**: 핸드셰이크가 무작위 데이터와 구분되지 않음

### 암호학적 가정

**계산적 난이도 가정:**

1. **X25519 CDH**: Curve25519에서 계산적 디피-헬만 문제는 풀기 어렵다
2. **ChaCha20 PRF**: ChaCha20은 의사난수 함수(PRF)이다
3. **Poly1305 MAC**: Poly1305는 선택 메시지 공격에 대해 위조가 불가능하다
4. **SHA-256 CR**: SHA-256은 충돌 저항성을 가진다
5. **HKDF Security**: HKDF는 키를 추출하고 균일한 분포의 키로 확장한다

**보안 수준:**

- **X25519**: ~128비트 보안 강도 (곡선의 차수 2^252)
- **ChaCha20**: 256비트 키, 256비트 보안 강도
- **Poly1305**: 128비트 보안 강도 (충돌 확률 기준)
- **SHA-256**: 128비트 충돌 저항성, 256비트 전이미지 저항성

### 키 관리

**키 생성:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**키 저장소:**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**키 로테이션:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### 공격 완화 대책

### 재전송 공격 완화 기법

**DateTime(날짜/시간) 유효성 검사:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**NS 메시지용 블룸 필터:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Session Tag(세션 태그) 일회성 사용:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Key Compromise Impersonation (KCI, 키 손상 가장 공격) 완화 방안

**문제**: NS 메시지 인증은 KCI(키 손상 사칭 공격)에 취약함 (인증 수준 1)

**완화 조치**:

1. 가능한 한 빨리 NSR(인증 레벨 2)로 전환하세요
2. 보안에 민감한 작업에서는 NS 페이로드를 신뢰하지 마세요
3. 되돌릴 수 없는 작업을 수행하기 전에 NSR 확인을 기다리세요

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### 서비스 거부(DoS) 완화 대책

**NS 플러딩 방지:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**태그 저장 제한:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**적응형 자원 관리:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### 트래픽 분석 저항성

**Elligator2 Encoding(엘리게이터2 인코딩):**

핸드셰이크 메시지가 무작위 데이터와 구분되지 않도록 보장합니다:

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**패딩 전략:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**타이밍 공격:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### 구현상의 함정

**일반적인 실수:**

1. **Nonce(논스) 재사용**: (key, nonce) 쌍을 절대 재사용하지 마십시오
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# 좋음: 각 메시지마다 고유한 nonce(논스: 한 번만 사용하는 임의값)    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# 나쁨: 임시 키 재사용    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # 나쁨

# 좋음: 각 메시지마다 새 키    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# 나쁨: 비암호학적 난수 생성기    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # 안전하지 않음

# 좋음: 암호학적으로 안전한 RNG(난수 생성기)    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# 나쁨: Early-exit(조기 종료) 비교    if computed_mac == received_mac:  # 타이밍 누출

       pass
   
# 좋음: 상수 시간 비교    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# 나쁜 예: 검증 전에 복호화    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # 너무 늦음    if not mac_ok:

       return error
   
# 좋음: AEAD(부가 데이터가 있는 인증 암호화)는 복호화하기 전에 검증한다    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# 나쁨: 단순 삭제    del private_key  # 아직 메모리에 남아 있음

# 권장: 삭제 전에 덮어쓰기    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# 보안상 중요한 테스트 케이스

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# ECIES(타원곡선 통합 암호화 방식) 전용(신규 배포에 권장)

i2cp.leaseSetEncType=4

# 이중 키 (ECIES + ElGamal 호환성용)

i2cp.leaseSetEncType=4,0

# ElGamal 전용 (레거시, 권장되지 않음)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# 표준 LS2(LeaseSet2, 가장 일반적)

i2cp.leaseSetType=3

# 암호화된 LS2 (blinded destinations, 블라인드된 목적지)

i2cp.leaseSetType=5

# 메타 LS2 (여러 Destination(목적지))

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# ECIES(타원곡선 통합 암호화 방식)용 정적 키(선택 사항, 지정하지 않으면 자동 생성)

# Base64로 인코딩된 32바이트 X25519(타원 곡선 기반 키 교환 알고리즘) 공개 키

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# 서명 유형(LeaseSet용)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# router 간 ECIES

i2p.router.useECIES=true

```

**Build Properties:**

```java
// I2CP 클라이언트(Java)용 Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[제한]

# ECIES(타원곡선 통합 암호화 방식) 세션 메모리 제한

ecies.memory = 128M

[ecies]

# ECIES(타원 곡선 통합 암호화 체계) 활성화

enabled = true

# ECIES(타원곡선 통합 암호화 체계) 전용 또는 이중 키

compatibility = true  # true = dual-key(이중 키), false = ECIES-only(ECIES 전용)

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# ECIES(타원곡선 통합 암호 방식) 전용

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# ElGamal은 유지하면서 ECIES를 추가

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# 연결 유형 확인

i2prouter.exe status

# 또는

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# ElGamal 제거

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# I2P router 또는 애플리케이션을 재시작

systemctl restart i2p

# 또는

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# 문제가 발생하면 ElGamal(엘가말)만 사용하도록 되돌리기

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# 최대 인바운드 세션 수

i2p.router.maxInboundSessions=1000

# 최대 아웃바운드 세션 수

i2p.router.maxOutboundSessions=1000

# 세션 타임아웃 (초)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# 태그 저장 용량 제한 (KB)

i2p.ecies.maxTagMemory=10240  # 10 MB

# 룩어헤드 윈도우

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# ratchet(키를 단계적으로 갱신하는 암호화 메커니즘) 이전의 메시지

i2p.ecies.ratchetThreshold=4096

# 래칫까지 남은 시간(초)

i2p.ecies.ratchetTimeout=600  # 10분

```

### Monitoring and Debugging

**Logging:**

```properties
# ECIES(타원곡선 통합 암호 방식) 디버그 로깅 활성화

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# 예제

print("NS (bound, 1KB payload):", calculate_ns_size(1024, bound=True), "바이트")

# 출력: 1120 바이트

print("NSR (1KB payload):", calculate_nsr_size(1024), "bytes")

# 출력: 1096 바이트

print("ES (1KB 페이로드):", calculate_es_size(1024), "바이트")

# 출력: 1048 바이트

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---