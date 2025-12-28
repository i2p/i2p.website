---
title: "암호화된 leaseSet을 위한 B32"
description: "암호화된 LS2 leaseSet용 Base 32 주소 형식"
slug: "b32encrypted"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "구현됨"
---

## 개요

표준 Base 32("b32") 주소는 목적지의 해시를 포함합니다. 이는 암호화된 LS2(LeaseSet2) (제안 123)에는 작동하지 않습니다.

암호화된 LS2 (proposal 123)는 destination(I2P 목적지 식별자)의 해시만을 포함하므로, 기존의 base 32 주소를 사용할 수 없다. non-blinded 공개키는 제공되지 않는다. 클라이언트가 leaseset(경로 임대 정보 묶음)을 가져와 복호화하려면, destination의 공개키, 서명 유형, blinded(블라인드 처리된) 서명 유형, 그리고 선택적인 비밀값(secret) 또는 개인키를 알고 있어야 한다. 따라서 base 32 주소만으로는 충분하지 않다. 클라이언트는 공개키를 포함하는 전체 destination 또는 공개키 자체 가운데 하나가 필요하다. 클라이언트의 주소록에 전체 destination이 있고, 그 주소록이 해시로 역조회를 지원한다면 공개키를 가져올 수 있다.

이 형식은 해시 대신 공개 키를 base32 주소에 넣습니다. 또한 이 형식에는 공개 키의 서명 유형과 블라인딩 스킴의 서명 유형이 포함되어야 합니다.

이 문서는 이러한 주소에 대한 b32 형식을 정의합니다. 논의 중에는 이 새로운 형식을 "b33" 주소라고 불러 왔지만, 실제 새로운 형식은 통상적인 ".b32.i2p" 접미사를 그대로 유지합니다.

## 구현 상태

제안 123(새 netDB 엔트리)은 버전 0.9.43(2019년 10월)에서 완전히 구현되었다. 암호화된 LS2(LeaseSet2) 기능 세트는 주소 지정 형식이나 암호 사양에 하위 호환성을 깨는 변경 없이 버전 2.10.0(2025년 9월)까지 안정적으로 유지되었다.

주요 구현 이정표: - 0.9.38: 오프라인 키를 사용하는 표준 LS2에 대한 Floodfill 지원 - 0.9.39: RedDSA(서명 알고리즘) 서명 유형 11 및 기본 암호화/복호화 - 0.9.40: B32 주소 지정에 대한 완전한 지원(Proposal 149) - 0.9.41: X25519(타원곡선 키 교환 알고리즘) 기반 클라이언트별 인증 - 0.9.42: 모든 블라인딩 기능 가동 - 0.9.43: 완전한 구현 선언(2019년 10월)

## 설계

- 새 형식에는 블라인딩 해제된 공개 키, 블라인딩 해제된 서명 유형, 그리고 블라인드된 서명 유형이 포함됩니다.
- 비공개 링크를 위해 secret(비밀 값) 및/또는 개인 키 요구 사항을 선택적으로 지정합니다.
- 기존 ".b32.i2p" 접미사를 사용하지만 길이는 더 깁니다.
- 오류 검출을 위한 체크섬을 포함합니다.
- 암호화된 leaseSet의 주소는 인코딩된 문자 56자 이상(디코딩된 35바이트 이상)으로 식별되며, 이는 기존 base 32 주소의 52자(32바이트)와 대비됩니다.

## 명세

### 생성과 인코딩

다음과 같이 {56자 이상}.b32.i2p (바이너리로는 35자 이상) 형식의 호스트명을 구성합니다:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
후처리 및 체크섬:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
b32 끝의 사용되지 않은 비트는 모두 0이어야 합니다. 표준 56자(35바이트) 주소에는 사용되지 않은 비트가 없습니다.

### 디코딩 및 검증

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### 비밀키와 개인 키 비트

비밀 키 및 개인 키 비트 플래그는 leaseset(목적지의 수신 터널 정보를 담는 I2P 데이터 구조)을 복호화하는 데 비밀 키 및/또는 개인 키가 필요함을 클라이언트, 프록시 또는 기타 클라이언트 측 코드에 알리기 위해 사용된다. 특정 구현에서는 사용자에게 필요한 데이터를 제공하도록 요청하거나, 필요한 데이터가 없을 경우 연결 시도를 거부할 수 있다.

이 비트들은 표시 용도로만 사용됩니다. 보안을 훼손할 수 있으므로 비밀 키 또는 개인 키를 B32 주소 자체에 절대 포함해서는 안 됩니다.

## 암호학적 세부 사항

### 블라인딩 스킴

이 블라인딩 스킴은 Ed25519와 ZCash의 설계를 바탕으로 한 RedDSA(서명 체계)를 사용하여, SHA-512를 사용해 Ed25519 곡선 위에서 Red25519 서명을 생성합니다. 이 접근법은 블라인딩된 공개키가 소수 차수 부분군에 머무르도록 보장하여, 일부 대안적 설계에서 나타나는 보안상의 우려를 피합니다.

Blinded keys(블라인딩된 키)는 UTC 날짜를 기준으로 매일 다음 공식을 사용해 순환됩니다:

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
DHT(분산 해시 테이블) 저장 위치는 다음과 같이 계산됩니다:

```
SHA256(type_byte || blinded_public_key)
```
### 암호화

암호화된 leaseset은 암호화를 위해 ChaCha20 스트림 암호를 사용하며, AES 하드웨어 가속이 없는 장치에서 더 우수한 성능을 제공하기 때문에 선택되었습니다. 이 명세는 키 유도를 위해 HKDF를, 디피-헬먼 연산을 위해 X25519를 사용합니다.

암호화된 leasesets는 3계층 구조로 되어 있습니다:
- 외부 계층: 평문 메타데이터
- 중간 계층: 클라이언트 인증 (DH 또는 PSK 방식)
- 내부 계층: 리스 정보를 포함한 실제 LS2 데이터

### 인증 방법

클라이언트별 인증은 두 가지 방법을 지원합니다:

**DH 인증**: X25519 키 합의를 사용합니다. 각 승인된 클라이언트는 서버에 자신의 공개 키를 제공하고, 서버는 ECDH(타원 곡선 디피-헬만)에서 도출한 공유 비밀을 사용해 중간 레이어를 암호화합니다.

**PSK 인증**: 암호화를 위해 사전 공유 키를 직접 사용합니다.

B32 주소의 플래그 비트 2는 클라이언트별 인증이 필요한지 여부를 나타낸다.

## 캐싱

이 사양의 범위를 벗어나긴 하지만, routers와 클라이언트는 공개 키에서 목적지로의 매핑과 그 역방향 매핑을 기억하고 캐시(영구 저장 권장)해 두어야 한다.

blockfile naming service(블록파일 기반 명명 서비스)는 버전 0.9.8부터 I2P의 기본 주소록 시스템으로, 해시 기반의 신속한 조회를 제공하는 전용 역방향 조회 맵과 함께 여러 개의 주소록을 관리합니다. 이 기능은 초기에는 해시만 알려져 있을 때 암호화된 leaseSet을 조회하는 데 필수적입니다.

## 서명 유형

I2P 버전 2.10.0 기준으로 서명 유형은 0부터 11까지 정의되어 있다. 단일 바이트 인코딩이 표준으로 유지되며, 2바이트 인코딩도 가능하지만 실제로는 사용되지 않는다.

**일반적으로 사용되는 유형:** - Type 0 (DSA_SHA1): routers에서는 사용 중단, destinations(목적지)에서는 지원 - Type 7 (EdDSA_SHA512_Ed25519): router 식별자와 destinations의 현재 표준 - Type 11 (RedDSA_SHA512_Ed25519): blinding(블라인딩) 지원이 있는 암호화된 LS2 leasesets 전용

**중요 참고**: Ed25519 (type 7)와 Red25519 (type 11)만 암호화된 leasesets에 필요한 blinding(은닉 기법)을 지원합니다. 다른 서명 유형은 이 기능과 함께 사용할 수 없습니다.

유형 9-10(GOST algorithms, 러시아 국가 표준 암호 알고리즘)은 예약되어 있지만 아직 구현되지 않았습니다. 유형 4-6과 8은 오프라인 서명 키용으로 "offline only"로 표시되어 있습니다.

## 참고 사항

- 길이로 구형과 신형 형식을 구분하세요. 구형 b32 주소는 항상 {52자}.b32.i2p이고, 신형은 {56자 이상}.b32.i2p입니다
- base32 인코딩은 RFC 4648 표준을 따르며, 디코딩은 대소문자를 구분하지 않고 출력은 소문자 사용을 권장합니다
- 공개키가 더 큰 서명 유형(예: 132바이트 키의 ECDSA P521)을 사용할 경우 주소 길이가 200자를 초과할 수 있습니다
- 표준 b32와 마찬가지로, 원한다면 새 형식을 jump links(이름 해석용 링크)에서 사용할 수 있고 jump servers(제공 서버)에서 제공될 수도 있습니다
- 개인정보 보호 강화를 위해 blinded keys(블라인드 처리된 키)는 UTC 날짜를 기준으로 매일 순환(교체)됩니다
- 이 형식은 Tor의 rend-spec-v3.txt appendix A.2 접근 방식과 다르며, off-curve blinded public keys(타원곡선 위에 있지 않은 블라인드 공개키)와 관련해 잠재적인 보안 영향이 있을 수 있습니다

## 버전 호환성

이 명세는 I2P 0.9.47(2020년 8월)부터 2.10.0(2025년 9월)까지의 버전에 적용됩니다. 이 기간 동안 B32 addressing format(베이스32 주소 형식), 암호화된 LS2 구조(LeaseSet2), 또는 암호 구현에는 비호환 변경이 발생하지 않았습니다. 0.9.47에서 생성된 모든 주소는 현재 버전들과 완전한 호환성을 유지합니다.

## 참고 문헌

**CRC-32** - [CRC-32 (위키백과)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309: 스트림 제어 전송 프로토콜 체크섬](https://tools.ietf.org/html/rfc3309)

**I2P 명세** - [암호화된 LeaseSet 명세](/docs/specs/encryptedleaseset/) - [제안 123: 새로운 netDB 항목](/proposals/123-new-netdb-entries/) - [제안 149: 암호화된 LS2(LeaseSet 2)용 B32](/proposals/149-b32-encrypted-ls2/) - [공통 구조 명세](/docs/specs/common-structures/) - [이름 지정 및 주소록](/docs/overview/naming/)

**Tor 비교** - [Tor 토론 스레드 (설계 맥락)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**추가 자료** - [I2P 프로젝트](/) - [I2P 포럼](https://i2pforum.net) - [Java API 문서](http://docs.i2p-projekt.de/javadoc/)
