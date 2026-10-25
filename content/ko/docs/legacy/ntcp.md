---
title: "NTCP (NIO 기반 TCP)"
description: "I2P용 레거시 Java NIO 기반 TCP 전송 방식, NTCP2로 대체됨"
slug: "ntcp"
aliases:
  - "/ko/docs/transport/ntcp"
  - "/ko/docs/transport/ntcp/"
  - "/ko/docs/ntcp"
  - "/ko/docs/ntcp/"
  - "/ko/ntcp"
  - "/ko/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

더 이상 지원되지 않는 폐기된 기능입니다. 2019년 5월 0.9.40 버전부터 기본적으로 비활성화되었습니다. 2021년 5월 0.9.50 버전에서 지원이 완전히 제거되었습니다. [NTCP2](/docs/specs/ntcp2)로 대체되었습니다. NTCP는 I2P 릴리스 0.6.1.22에서 도입된 Java NIO 기반 전송 방식입니다. Java NIO(새로운 I/O)는 기존 TCP 전송의 연결당 1개 스레드 문제를 겪지 않습니다. NTCP-over-IPv6은 버전 0.9.8부터 지원됩니다.

기본적으로 NTCP는 SSU에서 자동 감지된 IP/포트를 사용합니다. config.jsp에서 활성화되면, SSU는 외부 주소가 변경되거나 방화벽 상태가 변경될 때 NTCP에 알리고 재시작합니다. 이제 고정 IP나 dyndns 서비스 없이도 인바운드 TCP를 활성화할 수 있습니다.

I2P 내의 NTCP 코드는 신뢰할 수 있는 전송을 위해 기본 Java TCP 전송을 사용하기 때문에 상대적으로 가볍습니다(SSU 코드 크기의 1/4).

## Router 주소 명세 {#ra}

다음 속성들이 netDb에 저장됩니다.

- **Transport name:** NTCP
- **host:** IP (IPv4 또는 IPv6).
  단축된 IPv6 주소("::" 포함)가 허용됩니다.
  호스트 이름은 이전에 허용되었지만, 릴리스 0.9.32부터 사용이 권장되지 않습니다. proposal 141을 참조하세요.
- **port:** 1024 - 65535

## NTCP 프로토콜 명세서

### 표준 메시지 형식

연결이 설정된 후, NTCP transport는 간단한 체크섬과 함께 개별 I2NP 메시지를 전송합니다. 암호화되지 않은 메시지는 다음과 같이 인코딩됩니다:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
그런 다음 데이터는 AES/256/CBC로 암호화됩니다. 암호화를 위한 세션 키는 설정 과정에서 협상됩니다 (Diffie-Hellman 2048 bit 사용). 두 router 간의 설정은 EstablishState 클래스에서 구현되며 아래에서 자세히 설명됩니다. AES/256/CBC 암호화를 위한 IV는 이전 암호화된 메시지의 마지막 16바이트입니다.

전체 메시지 길이(6바이트의 크기 및 체크섬 바이트 포함)를 16의 배수로 만들기 위해 0-15바이트의 패딩이 필요합니다. 현재 최대 메시지 크기는 16KB입니다. 따라서 현재 최대 데이터 크기는 16KB - 6, 즉 16378바이트입니다. 최소 데이터 크기는 1바이트입니다.

### 시간 동기화 메시지 형식

특별한 경우 중 하나는 sizeof(data)가 0인 메타데이터 메시지입니다. 이 경우 암호화되지 않은 메시지는 다음과 같이 인코딩됩니다:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
총 길이: 16바이트. 시간 동기화 메시지는 약 15분 간격으로 전송됩니다. 메시지는 표준 메시지와 동일하게 암호화됩니다.

### 체크섬

표준 및 시간 동기화 메시지는 [ZLIB 사양](http://tools.ietf.org/html/rfc1950)에 정의된 Adler-32 체크섬을 사용합니다.

### 유휴 시간 초과

유휴 타임아웃과 연결 종료는 각 엔드포인트의 재량에 따라 결정되며 달라질 수 있습니다. 현재 구현에서는 연결 수가 설정된 최대값에 접근할수록 타임아웃을 낮추고, 연결 수가 적을 때는 타임아웃을 높입니다. 권장 최소 타임아웃은 2분 이상이며, 권장 최대 타임아웃은 10분 이상입니다.

### RouterInfo 교환

연결이 설정된 후, 그리고 이후 30-60분마다 두 router는 일반적으로 DatabaseStoreMessage를 사용하여 RouterInfo를 교환해야 합니다. 하지만 Alice는 중복 메시지를 보내지 않도록 대기열의 첫 번째 메시지가 DatabaseStoreMessage인지 확인해야 합니다. 이는 floodfill router에 연결할 때 자주 발생하는 경우입니다.

### 연결 설정 시퀀스

연결 확립 상태에서는 DH 키와 서명을 교환하기 위한 4단계 메시지 시퀀스가 있습니다. 처음 두 메시지에서는 2048비트 Diffie Hellman 교환이 이루어집니다. 그런 다음 연결을 확인하기 위해 중요한 데이터의 서명이 교환됩니다.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH 키 교환 {#DH}

초기 2048비트 DH 키 교환은 I2P의 [ElGamal 암호화](/docs/specs/cryptography#elgamal)에 사용되는 것과 동일한 공유 소수(p)와 생성자(g)를 사용합니다.

DH 키 교환은 아래에 표시된 여러 단계로 구성됩니다. 이러한 단계와 I2P router들 간에 전송되는 메시지 간의 매핑은 굵은 글씨로 표시되어 있습니다.

1. Alice는 비밀 정수 x를 생성합니다. 그런 다음 `X = g^x mod p`를 계산합니다.
2. Alice는 X를 Bob에게 보냅니다 **(메시지 1)**.
3. Bob은 비밀 정수 y를 생성합니다. 그런 다음 `Y = g^y mod p`를 계산합니다.
4. Bob은 Y를 Alice에게 보냅니다. **(메시지 2)**
5. 이제 Alice는 `sessionKey = Y^x mod p`를 계산할 수 있습니다.
6. 이제 Bob은 `sessionKey = X^y mod p`를 계산할 수 있습니다.
7. 이제 Alice와 Bob 모두 공유 키 `sessionKey = g^(x*y) mod p`를 가지게 됩니다.

그런 다음 sessionKey는 **메시지 3**과 **메시지 4**에서 신원을 교환하는 데 사용됩니다. DH 교환에 대한 지수(x 및 y) 길이는 [암호화 페이지](/docs/specs/cryptography#exponent)에 문서화되어 있습니다.

#### 세션 키 세부 정보

32바이트 세션 키는 다음과 같이 생성됩니다:

1. 교환된 DH 키를 양의 최소 길이 BigInteger 바이트 배열(2의 보수 빅엔디안)로 표현합니다
2. 최상위 비트가 1인 경우 (즉, array[0] & 0x80 != 0), Java의 BigInteger.toByteArray() 표현과 같이 0x00 바이트를 앞에 추가합니다
3. 해당 바이트 배열이 32바이트 이상인 경우, 처음(최상위) 32바이트를 사용합니다
4. 해당 바이트 배열이 32바이트 미만인 경우, 0x00 바이트를 추가하여 32바이트로 확장합니다. *(거의 발생하지 않음)*

#### 메시지 1 (세션 요청)

이것은 DH 요청입니다. Alice는 이미 [네트워크 데이터베이스](/docs/overview/network-database)에 게시된 Bob의 [Router Info](/docs/specs/common-structures#struct_RouterInfo)에 포함된 Bob의 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), IP 주소, 그리고 포트를 가지고 있습니다. Alice는 Bob에게 다음을 보냅니다:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
목차:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**참고사항:**

- Bob은 자신의 router 해시를 사용하여 HXxorHI를 검증합니다. 검증되지 않으면 Alice가 잘못된 router에 연결한 것이므로 Bob은 연결을 끊습니다.

#### 메시지 2 (세션 생성됨)

이것은 DH 응답입니다. Bob이 Alice에게 보냅니다:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
암호화되지 않은 내용:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
암호화된 내용:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**참고:**

- Alice는 tsB를 사용하여 계산된 Bob과의 시계 편차가 너무 클 경우 연결을 끊을 수 있습니다.

#### 메시지 3 (세션 확인 A)

이는 Alice의 router 신원과 중요한 데이터의 서명을 포함합니다. Alice가 Bob에게 보내는 것:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
암호화되지 않은 내용:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
암호화된 내용:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**참고:**

- Bob은 서명을 검증하고, 실패 시 연결을 끊습니다.
- Bob은 tsA를 사용하여 계산된 Alice와의 클럭 스큐가 너무 클 경우 연결을 끊을 수 있습니다.
- Alice는 이 메시지의 암호화된 내용 중 마지막 16바이트를 다음 메시지의 IV로 사용합니다.
- 릴리스 0.9.15까지는 router identity가 항상 387바이트였고, 서명은 항상 40바이트 DSA 서명이었으며, 패딩은 항상 15바이트였습니다. 릴리스 0.9.16부터는 router identity가 387바이트보다 길 수 있고, 서명 타입과 길이는 Alice의 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity)에 있는 [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey)의 타입에 의해 결정됩니다. 패딩은 전체 암호화되지 않은 내용이 16바이트의 배수가 되도록 필요한 만큼 추가됩니다.
- 메시지의 총 길이는 Router Identity를 읽기 위해 부분적으로 복호화하지 않고는 결정할 수 없습니다. Router Identity의 최소 길이는 387바이트이고, 최소 서명 길이는 40바이트(DSA의 경우)이므로, 최소 총 메시지 크기는 2 + 387 + 4 + (서명 길이) + (16바이트로의 패딩), 즉 DSA의 경우 2 + 387 + 4 + 40 + 15 = 448바이트입니다. 수신자는 실제 Router Identity 길이를 결정하기 위해 복호화하기 전에 최소한의 양을 읽을 수 있습니다. Router Identity의 작은 Certificate들의 경우, 이것이 아마 전체 메시지가 될 것이고, 추가적인 복호화 작업이 필요한 더 많은 바이트가 메시지에 없을 것입니다.

#### 메시지 4 (세션 확인 B)

이것은 중요한 데이터의 서명입니다. Bob이 Alice에게 보냅니다:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
암호화되지 않은 내용:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
암호화된 내용:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**참고 사항:**

- Alice는 서명을 검증하고, 실패 시 연결을 끊습니다.
- Bob은 이 메시지의 암호화된 내용의 마지막 16바이트를 다음 메시지의 IV로 사용합니다.
- 0.9.15 릴리스까지는 서명이 항상 40바이트 DSA 서명이었고 패딩이 항상 8바이트였습니다. 0.9.16 릴리스부터는 서명 타입과 길이가 Bob의 [Router Identity](/docs/specs/common-structures#struct_RouterIdentity)에 있는 [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey)의 타입에 의해 암시됩니다. 패딩은 전체 암호화되지 않은 내용을 16바이트의 배수로 만들기 위해 필요한 만큼 적용됩니다.

#### 설치 후

연결이 설정되고, 표준 또는 시간 동기화 메시지가 교환될 수 있습니다. 이후의 모든 메시지는 협상된 DH 세션 키를 사용하여 AES 암호화됩니다. Alice는 메시지 #3의 암호화된 내용의 마지막 16바이트를 다음 IV로 사용합니다. Bob은 메시지 #4의 암호화된 내용의 마지막 16바이트를 다음 IV로 사용합니다.

### 연결 확인 메시지

또는 Bob이 연결을 받을 때, 이것은 확인 연결일 수 있습니다 (Bob이 누군가에게 자신의 listener를 검증해달라고 요청한 것일 수도 있습니다). Check Connection은 현재 사용되지 않습니다. 하지만 기록을 위해, 확인 연결들은 다음과 같이 형식이 지정됩니다. 확인 정보 연결은 다음 내용을 포함하는 256바이트를 받게 됩니다:

- 32바이트의 해석되지 않는 무시되는 데이터
- 1바이트 크기
- 로컬 router의 IP 주소를 구성하는 해당 바이트 수 (원격 측에서 도달하는 주소)
- 로컬 router가 도달된 2바이트 포트 번호
- 원격 측에서 알려진 4바이트 i2p 네트워크 시간 (epoch 이후 초)
- 223바이트까지의 해석되지 않는 패딩 데이터
- 로컬 router의 identity hash와 32바이트부터 223바이트까지의 SHA256의 xor

연결 확인 기능은 릴리스 0.9.12부터 완전히 비활성화되었습니다.

## 토론

이제 [NTCP 토론 페이지](/docs/discussions/ntcp)에서 확인할 수 있습니다.

## 향후 작업 {#future}

- 최대 메시지 크기는 약 32 KB로 증가되어야 합니다.

- 고정된 패킷 크기 세트는 외부 공격자로부터 데이터 분할을 더욱 숨기는 데 적절할 수 있지만, 그때까지는 대부분의 요구사항에 대해 tunnel, garlic, 그리고 종단 간 패딩이 충분해야 합니다.
  하지만 현재로서는 제한된 수의 메시지 크기를 만들기 위해 다음 16바이트 경계를 넘어서는 패딩에 대한 규정이 없습니다.

- NTCP의 메모리 사용률(커널 포함)을 SSU와 비교해야 합니다.

- 초기 패킷 크기를 기반으로 한 I2P 트래픽 식별을 방해하기 위해 설립 메시지를 무작위로 패딩할 수 있는 방법이 있습니까?
