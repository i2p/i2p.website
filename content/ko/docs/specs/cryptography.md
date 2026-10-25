---
title: "저수준 암호화 명세"
description: "I2P에서 사용되는 암호화 알고리즘의 저수준 세부사항"
slug: "cryptography"
aliases:
  - "/ko/how_cryptography"
  - "/ko/how_cryptography/"
category: "설계"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## 개요

> **참고:** 이 문서는 대부분 구식입니다. 현재 사양에 대해서는 다음 문서를 참조하십시오: > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

이 페이지는 I2P의 암호화에 대한 저수준 세부사항을 명시합니다.

I2P 내에서 사용되는 여러 암호화 알고리즘이 있습니다. I2P의 원래 설계에서는 각 타입별로 하나씩만 있었습니다 - 하나의 대칭 알고리즘, 하나의 비대칭 알고리즘, 하나의 서명 알고리즘, 그리고 하나의 해싱 알고리즘. 더 많은 알고리즘을 추가하거나 보다 안전한 알고리즘으로 마이그레이션할 수 있는 규정은 없었습니다.

최근 몇 년 동안 우리는 이전 버전과 호환되는 방식으로 여러 기본 요소와 조합을 지원하는 프레임워크를 추가했습니다. 다양한 키와 서명 길이를 가진 수많은 서명 알고리즘이 "signature types"로 정의됩니다. 비대칭 및 대칭 암호화의 조합을 사용하고 다양한 키 길이를 가진 종단 간 암호화 방식은 "encryption types"로 정의됩니다.

I2P의 다양한 프로토콜과 데이터 구조에는 서명 유형 및/또는 암호화 유형을 지정하는 필드가 포함되어 있습니다. 이러한 필드는 유형 정의와 함께 키 및 서명 길이와 이를 사용하는 데 필요한 암호화 기본 요소를 정의합니다. 서명 및 암호화 유형의 정의는 [공통 구조 사양](/docs/specs/common-structures)에 있습니다.

기존 I2P 프로토콜인 NTCP, SSU, 그리고 ElGamal/AES+SessionTags는 ElGamal 비대칭 암호화와 AES 대칭 암호화의 조합을 사용합니다. 더 새로운 프로토콜인 NTCP2와 ECIES-X25519-AEAD-Ratchet은 X25519 키 교환과 ChaCha20/Poly1305 대칭 암호화의 조합을 사용합니다.

- ECIES-X25519-AEAD-Ratchet이 ElGamal/AES+SessionTags를 대체했습니다.
- NTCP2가 NTCP를 대체했습니다.
- SSU2가 SSU를 대체했습니다.
- X25519 tunnel 생성이 ElGamal tunnel 생성을 대체했습니다.

## 비대칭 암호화

I2P의 원래 비대칭 암호화 알고리즘은 ElGamal입니다. 여러 곳에서 사용되는 새로운 알고리즘은 ECIES X25519 DH 키 교환입니다.

모든 ElGamal 사용을 X25519로 마이그레이션하는 과정에 있습니다.

NTCP (ElGamal 포함)는 NTCP2 (X25519 포함)로 마이그레이션되었습니다. ElGamal/AES+SessionTag는 ECIES-X25519-AEAD-Ratchet으로 마이그레이션되고 있습니다.

### X25519

X25519 사용법의 자세한 내용은 [NTCP2](/docs/specs/ntcp2)와 [ECIES](/docs/specs/ecies)를 참조하세요.

### ElGamal

ElGamal은 I2P의 여러 곳에서 사용됩니다:

- router 간 TunnelBuild 메시지를 암호화하기 위해
- LeaseSet의 암호화 키를 사용하는 ElGamal/AES+SessionTag의 일부로서 종단 간(destination 간) 암호화를 위해
- ElGamal/AES+SessionTag의 일부로서 floodfill router에 전송되는 일부 netDb 저장 및 쿼리의 암호화를 위해(destination-to-router 또는 router-to-router).

우리는 IETF [RFC-3526](http://tools.ietf.org/html/rfc3526)에서 제공하는 2048 ElGamal 암호화 및 복호화를 위한 공통 소수를 사용합니다. 현재 우리는 ElGamal을 단일 블록에서 IV와 세션 키를 암호화하는 데만 사용하며, 그 뒤에 해당 키와 IV를 사용한 AES 암호화된 페이로드가 이어집니다.

암호화되지 않은 ElGamal은 다음을 포함합니다:

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
H(data)는 ElGamal 블록에서 암호화된 데이터의 SHA256이며, 앞에 0이 아닌 무작위 바이트가 붙습니다. 이 바이트는 0.9.28부터 실제로 무작위입니다. 그 이전에는 항상 0xFF였습니다. 향후 플래그로 사용될 가능성이 있습니다. 블록에서 암호화된 데이터는 최대 222바이트까지 가능합니다. 평문이 222바이트보다 작은 경우 암호화된 데이터에 상당한 수의 0이 포함될 수 있으므로, 상위 계층에서 평문을 무작위 데이터로 222바이트까지 패딩하는 것이 권장됩니다. 총 길이: 일반적으로 255바이트입니다.

암호화된 ElGamal에는 다음이 포함됩니다:

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
각 암호화된 부분은 정확히 257바이트 크기로 맞추기 위해 앞에 0으로 채워집니다. 총 길이: 514바이트. 일반적인 사용에서 상위 계층은 평문 데이터를 222바이트로 패딩하여 255바이트의 암호화되지 않은 블록을 만듭니다. 이것은 두 개의 256바이트 암호화된 부분으로 인코딩되며, 이 계층에서 각 부분 앞에 1바이트의 0 패딩이 있습니다.

ElGamal 코드 [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)을 참조하세요.

공유 소수는 2048비트 키를 위한 Oakley 소수입니다 [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3):

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
또는 16진수 값으로:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
2를 생성원으로 사용합니다.

#### 짧은 지수 {#exponent}

표준 지수 크기는 2048비트(256바이트)이고 I2P PrivateKey는 전체 256바이트이지만, 일부 경우에는 226비트(28.25바이트)의 짧은 지수 크기를 사용합니다. 이는 Oakley 소수와 함께 사용하기에 안전해야 합니다 [vanOorschot1996] [BENCHMARKS].

또한 [Koshiba2004]는 이 sci.crypt 스레드 [SCI.CRYPT]에 따르면 이를 지원하는 것으로 보입니다. PrivateKey의 나머지 부분은 0으로 패딩됩니다.

릴리스 0.9.8 이전에는 모든 router가 짧은 지수를 사용했습니다. 릴리스 0.9.8부터 64비트 x86 router는 전체 2048비트 지수를 사용합니다. 현재 매우 느린 하드웨어의 소수 router를 제외하고는 모든 router가 전체 지수를 사용하며, 이들은 프로세서 부하 우려로 인해 계속 짧은 지수를 사용하고 있습니다. 이러한 플랫폼에서 더 긴 지수로의 전환은 향후 연구 주제입니다.

#### 폐기

ElGamal 공격에 대한 네트워크의 취약성과 더 긴 비트 길이로 전환하는 것의 영향에 대해 연구해야 합니다. 어떤 변경이든 하위 호환성을 유지하기는 매우 어려울 수 있습니다.

## 대칭 암호화

I2P의 원래 대칭 암호화 알고리즘은 AES입니다. 여러 곳에서 사용되는 최신 알고리즘은 AEAD(Authenticated Encryption with Associated Data) ChaCha20/Poly1305입니다.

우리는 모든 AES 사용을 ChaCha20/Poly1305로 마이그레이션하는 과정에 있습니다.

NTCP (AES 사용)은 NTCP2 (ChaCha20/Poly1305 사용)로 마이그레이션되었습니다. ElGamal/AES+SessionTag는 ECIES-X25519-AEAD-Ratchet로 마이그레이션되고 있습니다.

### ChaCha20/Poly1305

ChaCha20/Poly1305 사용의 세부 사항은 [NTCP2](/docs/specs/ntcp2)와 [ECIES](/docs/specs/ecies)를 참조하세요.

### AES

AES는 다음과 같은 여러 경우에 대칭 암호화에 사용됩니다:

- DH 키 교환 후 SSU transport 암호화를 위해 ("Transports" 섹션 참조)
- ElGamal/AES+SessionTag의 일부로서 종단간(destination-to-destination) 암호화를 위해
- ElGamal/AES+SessionTag의 일부로서 floodfill router에게 전송되는 일부 netDb 저장 및 쿼리의 암호화를 위해 (destination-to-router 또는 router-to-router)
- router가 자신의 tunnel을 통해 자기 자신에게 보내는 주기적 tunnel 테스트 메시지의 암호화를 위해

우리는 256비트 키와 128비트 블록을 가진 AES를 CBC 모드에서 사용합니다. 사용되는 패딩은 IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, 섹션 8.1 (블록 타입 02용))에 명시되어 있습니다. 이 경우, 패딩은 16바이트 블록에 맞추기 위해 의사무작위로 생성된 옥텟으로 구성됩니다. 구체적으로, CBC 코드 [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)과 Cryptix AES 구현 [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), 그리고 ElGamalAESEngine.getPadding 함수 [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)에서 찾을 수 있는 패딩을 참조하십시오.

#### 폐기 예정

AES 공격에 대한 네트워크의 취약성과 더 긴 비트 길이로 전환할 때의 영향에 대해 연구해야 합니다. 어떤 변경 사항이든 하위 호환성을 유지하는 것은 매우 어려울 수 있습니다.

## 서명 {#sig}

다양한 키 길이와 서명 길이를 가진 수많은 서명 알고리즘이 서명 유형에 의해 정의됩니다. 더 많은 서명 유형을 추가하는 것은 비교적 쉽습니다.

EdDSA-SHA512-Ed25519는 현재 기본 서명 알고리즘입니다. DSA는 서명 유형 지원을 추가하기 전의 원래 알고리즘으로, 여전히 네트워크에서 사용되고 있습니다.

### DSA

서명은 [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)에 구현된 1024 비트 [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) (L=1024, N=160)를 사용하여 생성되고 검증됩니다. DSA는 ElGamal보다 서명에서 훨씬 빠르기 때문에 선택되었습니다.

#### SEED

160비트:

```
86108236b8526e296e923a4015b4282845b572cc
```
#### 카운터

```
33
```
#### DSA 소수 (p)

1024 비트:

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### DSA 몫 (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### DSA 생성기 (g)

1024 비트:

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
SigningPublicKey는 1024비트입니다. SigningPrivateKey는 160비트입니다.

#### 폐기

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)에서는 2010년 이후 사용을 위해 최소한 (L=2048, N=224)를 권장합니다. 이는 주어진 키의 "cryptoperiod" 또는 수명에 의해 어느 정도 완화될 수 있습니다.

소수는 2003년에 선택되었으며, 이 수를 선택한 사람(TheCrypto)은 현재 더 이상 I2P 개발자가 아닙니다. 따라서 우리는 선택된 소수가 '강한 소수'인지 알지 못합니다. 향후 목적을 위해 더 큰 소수가 선택된다면, 이는 강한 소수여야 하며, 우리는 구성 과정을 문서화할 것입니다.

## 새로운 서명 알고리즘

릴리스 0.9.12부터 router는 1024비트 DSA보다 더 안전한 추가 서명 알고리즘을 지원합니다. 첫 번째 사용은 Destination용이었으며, Router Identity 지원은 릴리스 0.9.16에서 추가되었습니다. 기존 Destination은 이전 서명에서 새로운 서명으로 마이그레이션할 수 없지만, 여러 Destination을 가진 단일 tunnel에 대한 지원이 있어 새로운 서명 유형으로 전환할 수 있는 방법을 제공합니다. 서명 유형은 Destination과 Router Identity에 인코딩되어 있어, 언제든지 새로운 서명 알고리즘이나 곡선이 추가될 수 있습니다.

현재 지원되는 서명 유형은 다음과 같습니다:

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (널리 사용되지 않음)
- ECDSA-SHA512-P521 (널리 사용되지 않음)
- EdDSA-SHA512-Ed25519 (릴리스 0.9.15부터 기본값)
- RedDSA-SHA512-Ed25519 (릴리스 0.9.39부터)

추가 서명 유형은 애플리케이션 계층에서만 사용되며, 주로 su3 파일의 서명 및 검증을 위해 사용됩니다. 이러한 서명 유형은 다음과 같습니다:

- RSA-SHA256-2048 (널리 사용되지 않음)
- RSA-SHA384-3072 (널리 사용되지 않음)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (릴리스 0.9.25부터; 널리 사용되지 않음)

### ECDSA

ECDSA는 표준 NIST 곡선과 표준 SHA-2 해시를 사용합니다.

우리는 0.9.16 - 0.9.19 릴리스 기간 동안 새로운 목적지를 ECDSA-SHA256-P256으로 마이그레이션했습니다. Router Identity에 대한 사용은 릴리스 0.9.16부터 지원되며 기존 router들의 마이그레이션은 2015년에 이루어졌습니다.

### RSA

공개 지수 F4 = 65537을 사용하는 표준 RSA PKCS#1 v1.5 (RFC 2313).

RSA는 현재 router 업데이트, 리시딩, 플러그인, 뉴스를 포함한 모든 대역 외 신뢰할 수 있는 콘텐츠의 서명에 사용됩니다. 서명은 "su3" 형식 [UPDATES]에 내장됩니다. 4096비트 키가 권장되며 알려진 모든 서명자가 사용하고 있습니다. RSA는 네트워크 내 Destination이나 Router Identity에서 사용되지 않으며, 사용할 계획도 없습니다.

### EdDSA 25519

curve 25519와 표준 512비트 SHA-2 해시를 사용하는 표준 EdDSA.

릴리스 0.9.15부터 지원됩니다.

Destination과 router Identity는 2015년 말에 마이그레이션되었습니다.

### RedDSA 25519

curve 25519와 표준 512비트 SHA-2 해시를 사용하는 표준 EdDSA이지만, 서로 다른 개인 키를 사용하고 서명에 약간의 수정이 가해집니다. 암호화된 leaseSet을 위한 방식입니다. 자세한 내용은 [EncryptedLeaseSet](/docs/specs/encryptedleaseset)과 [Red25519](/docs/specs/red25519)를 참조하세요.

릴리스 0.9.39부터 지원됩니다.

## 해시

해시는 서명 알고리즘에서 사용되고 네트워크의 DHT에서 키로 사용됩니다.

이전 서명 알고리즘은 SHA1과 SHA256을 사용합니다. 새로운 서명 알고리즘은 SHA512를 사용합니다. DHT는 SHA256을 사용합니다.

### SHA256

I2P 내의 DHT 해시는 표준 SHA256입니다.

#### 폐기

네트워크의 SHA-256 공격에 대한 취약성과 더 긴 해시로 전환하는 것의 영향에 대해 연구해야 합니다. 어떤 변경사항이든 하위 호환성을 유지하는 것은 매우 어려울 수 있습니다.

## 전송 방식

가장 낮은 프로토콜 계층에서, router 간 점대점 통신은 전송 계층 보안에 의해 보호됩니다.

NTCP2 연결은 X25519 Diffie-Hellman과 ChaCha20/Poly1305 인증 암호화를 사용합니다.

SSU와 더 이상 사용되지 않는 NTCP transport는 위에서 ElGamal에 대해 명시된 것과 동일한 공유 소수와 생성기를 사용하여 256바이트(2048비트) Diffie-Hellman 키 교환을 사용하고, 위에서 설명한 대칭 AES 암호화가 뒤따릅니다.

SSU는 SSU2로 마이그레이션될 예정입니다 (X25519 및 ChaCha20/Poly1305 사용).

모든 전송 방식은 전송 링크에서 완전 순방향 보안성 [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)을 제공합니다.

### NTCP2 연결 {#tcp}

NTCP2 연결은 X25519 Diffie-Hellman과 ChaCha20/Poly1305 인증 암호화, 그리고 Noise 프로토콜 프레임워크 [Noise](https://noiseprotocol.org/noise.html)를 사용합니다.

자세한 내용과 참조는 NTCP2 명세서 [NTCP2](/docs/specs/ntcp2)를 참조하세요.

### UDP 연결 {#udp}

SSU (UDP 전송)는 2048비트 Diffie-Hellman 교환을 통해 임시 세션 키에 합의한 후, 다른 router의 DSA 키를 사용한 station-to-station 인증과 함께 명시적 IV 및 MAC(HMAC-MD5-128)을 포함한 AES256/CBC로 각 패킷을 암호화하며, 각 네트워크 메시지는 로컬 무결성 검사를 위한 자체 해시를 가지고 있습니다.

자세한 내용은 SSU 사양서를 참조하십시오.

경고 - SSU에서 사용되는 I2P의 HMAC-MD5-128은 비표준인 것으로 보입니다. 초기 버전의 SSU는 HMAC-SHA256을 사용했으나, 성능상의 이유로 MD5-128로 전환되었지만 32바이트 버퍼 크기는 그대로 유지된 것으로 보입니다. 자세한 내용은 HMACGenerator.java와 2005-07-05 상태 노트를 참조하세요.

### NTCP 연결

NTCP는 더 이상 사용되지 않으며, NTCP2로 대체되었습니다.

NTCP 연결은 2048 Diffie-Hellman 구현을 통해 협상되었으며, router의 신원을 사용하여 station to station 합의를 진행한 후, 암호화된 프로토콜 특정 필드들이 이어지고, 모든 후속 데이터는 AES로 암호화되었습니다(위와 같이). ElGamalAES+SessionTag 대신 DH 협상을 수행하는 주된 이유는 '(완전한) 전방 비밀성' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)을 제공하기 때문이며, ElGamalAES+SessionTag는 이를 제공하지 않습니다.

## 참고 문헌

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Crypto++ 벤치마크, 원래 http://www.eskimo.com/~weidai/benchmarks.html (현재 사용 불가)에 있었으며, http://www.archive.org/에서 복구, 2008년 4월 23일자
- [Common](/docs/specs/common-structures) - 공통 구조 사양
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
