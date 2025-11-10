---
title: "NTCP2 구현 세부 사항"
date: 2018-08-20
author: "villain"
description: "I2P의 새로운 전송 프로토콜 구현 세부사항 및 기술 사양"
categories: ["development"]
---

I2P의 전송 프로토콜은 원래 약 15년 전에 개발되었습니다. 그 당시에는 전송되는 데이터를 숨기는 것이 주된 목표였지, 해당 프로토콜을 사용하고 있다는 사실 자체를 숨기는 것은 아니었습니다. 아무도 DPI(딥 패킷 검사)와 프로토콜 검열에 대한 방어를 진지하게 고려하지 않았습니다. 시간이 흐르면서, 기존 전송 프로토콜이 여전히 강력한 보안을 제공하고 있음에도 불구하고, 새로운 전송 프로토콜에 대한 요구가 생겼습니다. NTCP2는 현재의 검열 위협에 대응하도록 설계되었습니다. 주로, 패킷 길이에 대한 DPI 분석에 대응합니다. 또한 이 새로운 프로토콜은 최신 암호 기술 발전을 활용합니다. NTCP2는 [Noise Protocol Framework](https://noiseprotocol.org/noise.html)를 기반으로 하며, 해시 함수로는 SHA256을, 타원 곡선 Diffie-Hellman(DH) 키 교환으로는 x25519를 사용합니다.

NTCP2 프로토콜의 전체 명세는 [여기에서 확인할 수 있습니다](/docs/specs/ntcp2/).

## 새로운 암호 기술

NTCP2는 I2P 구현에 다음 암호화 알고리즘을 추가해야 한다:

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

원래 프로토콜인 NTCP와 비교하면, NTCP2는 DH 함수에 ElGamal 대신 x25519를 사용하고, AES-256-CBC/Adler32 대신 AEAD/Chaha20/Poly1305를 사용하며, 패킷의 길이 정보를 난독화하기 위해 SipHash를 사용합니다. NTCP2에서 사용되는 키 유도 함수는 더 복잡해져, 이제 HMAC-SHA256을 여러 차례 호출합니다.

*i2pd (C++) 구현 참고 사항: 위에서 언급된 모든 알고리즘은 SipHash를 제외하고 OpenSSL 1.1.0에 구현되어 있습니다. SipHash는 곧 출시될 OpenSSL 1.1.1 릴리스에 추가될 예정입니다. 현재 대부분의 시스템에서 사용되는 OpenSSL 1.0.2와의 호환성을 위해, i2pd 핵심 개발자인 [Jeff Becker](https://github.com/majestrate)가 누락된 암호 알고리즘의 독립형 구현을 기여했습니다.*

## RouterInfo 변경 사항

NTCP2는 기존의 두 키(암호화 키와 서명 키) 외에 세 번째 키(x25519)가 필요합니다. 이 키는 정적 키(static key)라고 하며, RouterInfo(라우터 정보) 내의 어느 주소에든 "s" 매개변수로 추가되어야 합니다. 이는 NTCP2의 발신자(Alice)와 응답자(Bob) 모두에게 요구됩니다. 예를 들어 IPv4와 IPv6처럼 둘 이상의 주소가 NTCP2를 지원하는 경우, "s"는 모두 동일해야 합니다. Alice의 주소는 "host"와 "port"를 설정하지 않고 "s" 매개변수만 포함해도 허용됩니다. 또한 "v" 매개변수가 필요하며, 현재는 항상 "2"로 설정됩니다.

NTCP2 주소는 별도의 NTCP2 주소로 선언하거나 추가 매개변수가 포함된 구형 NTCP 주소로 선언할 수 있으며, 이 경우 NTCP와 NTCP2 연결을 모두 허용합니다. Java I2P 구현은 두 번째 접근 방식을 사용하고, i2pd(C++ 구현)는 첫 번째를 사용합니다.

NTCP2 연결을 수락하는 노드는 새 연결을 설정할 때 공개 키의 초기화 벡터(IV)로 사용되는 "i" 매개변수를 포함하여 RouterInfo를 게시해야 한다.

## 연결 설정

연결을 수립하려면 양측 모두 임시(에페메랄) x25519 키 쌍을 생성해야 한다. 그 키들과 "static" 키를 기반으로 데이터 전송을 위한 키 집합을 파생시킨다. 양측은 상대방이 해당 static 키에 대한 개인 키를 실제로 보유하고 있는지, 그리고 그 static 키가 RouterInfo에 있는 것과 동일한지 확인해야 한다.

연결을 설정하기 위해 세 개의 메시지가 전송되고 있습니다:

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
각 메시지마다 «input key material(입력 키 자료)»라고 불리는 공통 x25519 키를 계산하며, 그 다음 MixKey 함수를 사용해 메시지 암호화 키를 생성합니다. 메시지를 교환하는 동안에는 ck (chaining key) 값을 유지합니다. 이 값은 데이터 전송용 키를 생성할 때 최종 입력으로 사용됩니다.

I2P의 C++ 구현에서 MixKey 함수는 대략 다음과 같습니다:

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
**SessionRequest** 메시지는 공개 x25519 Alice 키(32바이트), AEAD/Chacha20/Poly1305로 암호화된 데이터 블록(16바이트), 해시(16바이트), 그리고 끝부분의 일부 랜덤 데이터(패딩)로 구성됩니다. 패딩 길이는 암호화된 데이터 블록에 정의됩니다. 암호화된 블록에는 **SessionConfirmed** 메시지의 두 번째 부분의 길이도 포함됩니다. 데이터 블록은 Alice의 임시 키와 Bob의 정적 키에서 파생된 키로 암호화되고 서명됩니다. MixKey 함수의 초기 ck 값은 SHA256(Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256)으로 설정됩니다.

공개 x25519 키(32바이트)는 DPI(딥 패킷 검사)에 의해 탐지될 수 있으므로, Bob의 주소의 해시를 키로, RouterInfo의 "i" 매개변수를 초기화 벡터(IV)로 하여 AES-256-CBC 알고리즘으로 암호화된다.

**SessionCreated** 메시지는 **SessionRequest**와 동일한 구조를 가지며, 단 키는 양측의 임시 키를 기반으로 계산됩니다. **SessionRequest** 메시지의 공개 키를 암호화/복호화한 후 생성된 IV(초기화 벡터)는 임시 공개 키를 암호화/복호화하기 위한 IV로 사용됩니다.

**SessionConfirmed** 메시지는 두 부분으로 구성됩니다: 정적 공개 키와 Alice의 RouterInfo(라우터 정보). 이전 메시지들과의 차이점은 임시 공개 키가 **SessionCreated**와 동일한 키를 사용하여 AEAD/Chaha20/Poly1305로 암호화된다는 것입니다. 그 결과 메시지의 첫 번째 부분은 32바이트에서 48바이트로 증가합니다. 두 번째 부분 또한 AEAD/Chaha20/Poly1305로 암호화되지만, Bob의 임시 키와 Alice의 정적 키로부터 계산된 새로운 키를 사용합니다. RouterInfo 부분에는 무작위 데이터 패딩을 덧붙일 수도 있지만, 일반적으로 RouterInfo의 길이가 가변적이므로 필수는 아닙니다.

## 데이터 전송 키 생성

모든 해시와 키 검증이 성공했다면, 마지막 MixKey 연산 이후 양쪽에서 공통의 ck 값이 존재해야 합니다. 이 값은 연결의 양측을 위한 키 집합 <k, sipk, sipiv> 두 개를 생성하는 데 사용됩니다. "k"는 AEAD/Chaha20/Poly1305 키, "sipk"는 SipHash 키, "sipiv"는 매번 사용 후 변경되는 SipHash IV(Initialization Vector, 초기화 벡터)의 초기값입니다.

키를 생성하는 데 사용되는 코드는 I2P의 C++ 구현에서 다음과 같습니다:

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) 구현 참고사항: "sipkeys" 배열의 처음 16바이트는 SipHash(해시 함수) 키이며, 마지막 8바이트는 IV(초기화 벡터)입니다. SipHash는 8바이트 키 두 개를 요구하지만, i2pd는 이를 하나의 16바이트 키로 처리합니다.*

## 데이터 전송

Data is transferred in frames, each frame has 3 parts:

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

단일 프레임에서 전송될 수 있는 데이터의 최대 길이는 65519 바이트입니다.

메시지 길이는 현재 SipHash 초기화 벡터(IV)의 처음 두 바이트와 XOR 함수(배타적 논리합)를 적용해 난독화됩니다.

암호화된 데이터 부분에는 데이터 블록이 포함됩니다. 각 블록의 앞에는 블록 유형과 블록 길이를 정의하는 3바이트 헤더가 붙습니다. 일반적으로는 헤더가 변경된 I2NP 메시지인 I2NP 유형의 블록이 전송됩니다. 하나의 NTCP2 프레임은 여러 개의 I2NP 블록을 전송할 수 있습니다.

또 다른 중요한 데이터 블록 유형은 무작위 데이터 블록입니다. 모든 NTCP2 프레임에 무작위 데이터 블록을 하나 추가하는 것이 권장됩니다. 무작위 데이터 블록은 하나만 추가할 수 있으며, 반드시 마지막 블록이어야 합니다.

다음은 현재 NTCP2 구현에서 사용되는 기타 데이터 블록입니다:

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## 요약

오직 번역만 제공하고, 그 외에는 아무것도 포함하지 마십시오:

새로운 I2P 전송 프로토콜 NTCP2는 DPI(딥 패킷 검사) 검열에 대해 효과적인 저항성을 제공합니다. 또한 더 빠르고 최신의 암호 기술을 사용하므로 CPU 부하가 감소합니다. 이는 스마트폰과 가정용 router와 같은 저사양 장치에서도 I2P가 실행될 가능성을 높여 줍니다. I2P의 두 주요 구현은 NTCP2를 완전히 지원하며, 버전 0.9.36 (Java) 및 2.20 (i2pd, C++)부터 NTCP2를 사용할 수 있습니다.
