---
title: "포스트 양자 암호화 프로토콜"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "열기"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## 개요

적합한 포스트 퀀텀(PQ) 암호화에 대한 연구와 경쟁이 10년간 진행되어 왔지만, 선택지들이 명확해진 것은 최근의 일입니다.

2022년에 PQ 암호화의 함의를 살펴보기 시작했습니다 [zzz.i2p](http://zzz.i2p/topics/3294).

TLS 표준은 지난 2년간 하이브리드 암호화 지원을 추가했으며, Chrome과 Firefox의 지원으로 인해 현재 인터넷상의 암호화된 트래픽의 상당 부분에 사용되고 있습니다 [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST는 최근 양자 후 암호학(post-quantum cryptography)을 위한 권장 알고리즘을 확정하여 발표했습니다 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). 여러 일반적인 암호학 라이브러리들이 현재 NIST 표준을 지원하거나 가까운 미래에 지원을 출시할 예정입니다.

[Cloudflare](https://blog.cloudflare.com/pq-2024/)와 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) 모두 즉시 마이그레이션을 시작할 것을 권장합니다. 2022년 NSA PQ FAQ [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)도 참조하십시오. I2P는 보안과 암호화 분야의 리더가 되어야 합니다. 지금이 권장 알고리즘을 구현할 때입니다. 유연한 암호화 타입과 서명 타입 시스템을 사용하여 하이브리드 암호화와 PQ 및 하이브리드 서명을 위한 타입을 추가할 것입니다.

## 목표

- PQ 저항 알고리즘 선택
- 적절한 경우 I2P 프로토콜에 PQ 전용 및 하이브리드 알고리즘 추가
- 여러 변형 정의
- 구현, 테스트, 분석 및 연구 후 최적의 변형 선택
- 점진적으로 지원 추가 및 하위 호환성 유지

## 비목표

- 단방향(Noise N) 암호화 프로토콜을 변경하지 마십시오
- SHA256에서 벗어나지 마십시오, 단기적으로 PQ의 위협을 받지 않습니다
- 현재 최종 선호 변형을 선택하지 마십시오

## 위협 모델

- OBEP 또는 IBGW의 router들이 공모하여
  나중에 복호화하기 위해 garlic 메시지를 저장하는 경우 (순방향 보안성)
- 네트워크 관찰자들이
  나중에 복호화하기 위해 전송 메시지를 저장하는 경우 (순방향 보안성)
- 네트워크 참여자들이 RI, LS, 스트리밍, 데이터그램
  또는 기타 구조에 대한 서명을 위조하는 경우

## 영향받는 프로토콜

다음 프로토콜들을 대략 개발 순서대로 수정할 예정입니다. 전체적인 출시는 2025년 말부터 2027년 중반까지 이루어질 것으로 예상됩니다. 자세한 내용은 아래 우선순위 및 출시 섹션을 참조하십시오.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## 설계

우리는 NIST FIPS 203 및 204 표준 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)을 지원할 예정입니다. 이 표준들은 CRYSTALS-Kyber 및 CRYSTALS-Dilithium(버전 3.1, 3 및 이전 버전)을 기반으로 하지만 호환되지 않습니다.

### Key Exchange

다음 프로토콜에서 하이브리드 키 교환을 지원할 예정입니다:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM은 임시 키만 제공하며, Noise XK 및 IK와 같은 정적 키 핸드셰이크를 직접 지원하지 않습니다.

Noise N은 양방향 키 교환을 사용하지 않으므로 하이브리드 암호화에 적합하지 않습니다.

따라서 우리는 NTCP2, SSU2, 그리고 Ratchet에 대해 하이브리드 암호화만을 지원할 것입니다. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서와 같이 세 가지 ML-KEM 변형을 정의하여 총 3개의 새로운 암호화 유형을 만들 것입니다. 하이브리드 유형은 X25519와 결합된 경우에만 정의됩니다.

새로운 암호화 유형은 다음과 같습니다:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
오버헤드가 상당할 것입니다. 현재 일반적인 메시지 1과 2의 크기(XK와 IK의 경우)는 약 100바이트입니다(추가 페이로드 제외). 알고리즘에 따라 8배에서 15배까지 증가할 것입니다.

### Signatures

다음 구조에서 PQ 및 하이브리드 서명을 지원할 예정입니다:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
따라서 우리는 PQ 전용 및 하이브리드 서명을 모두 지원할 예정입니다. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의된 대로 세 가지 ML-DSA 변형, Ed25519와의 세 가지 하이브리드 변형, 그리고 SU3 파일에만 사용되는 prehash를 포함한 세 가지 PQ 전용 변형을 정의하여 총 9가지의 새로운 서명 유형을 제공할 예정입니다. 하이브리드 유형은 Ed25519와의 조합으로만 정의됩니다. SU3 파일을 제외하고는 pre-hash 변형(HashML-DSA)이 아닌 표준 ML-DSA를 사용할 예정입니다.

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 섹션 3.4에서 정의된 "결정론적" 변형이 아닌 "헤지드" 또는 무작위화 서명 변형을 사용할 것입니다. 이는 동일한 데이터에 대해서도 각 서명이 다르도록 보장하며, 사이드 채널 공격에 대한 추가적인 보호를 제공합니다. 인코딩 및 컨텍스트를 포함한 알고리즘 선택에 대한 추가 세부사항은 아래 구현 노트 섹션을 참조하십시오.

새로운 서명 타입들은 다음과 같습니다:

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
X.509 인증서와 기타 DER 인코딩은 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에 정의된 복합 구조와 OID를 사용합니다.

오버헤드가 상당할 것입니다. 일반적인 Ed25519 destination과 router identity 크기는 391바이트입니다. 이들은 알고리즘에 따라 3.5배에서 6.8배까지 증가할 것입니다. Ed25519 서명은 64바이트입니다. 이들은 알고리즘에 따라 38배에서 76배까지 증가할 것입니다. 일반적으로 서명된 RouterInfo, LeaseSet, 응답 가능한 데이터그램, 그리고 서명된 스트리밍 메시지는 약 1KB입니다. 이들은 알고리즘에 따라 3배에서 8배까지 증가할 것입니다.

새로운 destination과 router identity 타입들은 패딩을 포함하지 않기 때문에 압축이 불가능합니다. 전송 중 gzip 압축되는 destination과 router identity의 크기는 알고리즘에 따라 12배에서 38배까지 증가할 것입니다.

### Legal Combinations

Destination의 경우, 새로운 서명 유형은 leaseSet의 모든 암호화 유형과 함께 지원됩니다. 키 인증서의 암호화 유형을 NONE (255)으로 설정하세요.

RouterIdentity의 경우, ElGamal 암호화 타입은 더 이상 사용되지 않습니다. 새로운 서명 타입들은 X25519 (타입 4) 암호화에서만 지원됩니다. 새로운 암호화 타입들은 RouterAddress에 표시될 것입니다. 키 인증서의 암호화 타입은 계속해서 타입 4가 될 것입니다.

### New Crypto Required

- ML-KEM (이전 명칭: CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (이전 명칭: CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (이전 명칭: Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) SHAKE128에만 사용됨
- SHA3-256 (이전 명칭: Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 및 SHAKE256 (SHA3-128과 SHA3-256의 XOF 확장) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

SHA3-256, SHAKE128, 그리고 SHAKE256에 대한 테스트 벡터는 [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)에서 확인할 수 있습니다.

Java bouncycastle 라이브러리는 위의 모든 기능을 지원합니다. C++ 라이브러리 지원은 OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)에서 제공됩니다.

### Alternatives

[FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)는 지원하지 않을 예정입니다. ML-DSA보다 훨씬 느리고 크기가 큽니다. 곧 출시될 FIPS206 (Falcon)도 지원하지 않을 예정입니다. 아직 표준화되지 않았기 때문입니다. NIST에서 표준화하지 않은 NTRU나 기타 PQ 후보들도 지원하지 않을 예정입니다.

### Rosenpass

Wireguard (IK)를 순수 PQ 암호화에 적용하는 연구 [paper](https://eprint.iacr.org/2020/379.pdf)가 있지만, 해당 논문에는 여러 미해결 질문들이 있습니다. 나중에 이 접근법은 PQ Wireguard용 Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)로 구현되었습니다.

Rosenpass는 사전 공유된 Classic McEliece 460896 정적 키(각각 500 KB)와 Kyber-512(본질적으로 MLKEM-512) 임시 키를 사용하는 Noise KK와 유사한 핸드셰이크를 사용합니다. Classic McEliece 암호문은 188바이트에 불과하고 Kyber-512 공개 키와 암호문은 적절한 크기이므로 두 핸드셰이크 메시지 모두 표준 UDP MTU에 맞습니다. PQ KK 핸드셰이크에서 나온 출력 공유 키(osk)는 표준 Wireguard IK 핸드셰이크의 입력 사전 공유 키(psk)로 사용됩니다. 따라서 총 두 개의 완전한 핸드셰이크가 있으며, 하나는 순수 PQ이고 하나는 순수 X25519입니다.

우리가 XK 및 IK handshake를 대체하기 위해 이 중 어떤 것도 할 수 없는 이유는 다음과 같습니다:

- KK를 수행할 수 없습니다. Bob이 Alice의 정적 키를 가지고 있지 않기 때문입니다
- 500KB 정적 키는 너무 큽니다
- 추가 라운드트립을 원하지 않습니다

백서에는 많은 유용한 정보가 있으며, 아이디어와 영감을 얻기 위해 검토할 예정입니다. TODO.

## Specification

### 키 교환

공통 구조 문서 [/docs/specs/common-structures/](/docs/specs/common-structures/)의 섹션과 테이블을 다음과 같이 업데이트하세요:

### 서명

새로운 Public Key 유형은 다음과 같습니다:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
하이브리드 공개키는 X25519 키입니다. KEM 공개키는 Alice에서 Bob으로 전송되는 임시 PQ 키입니다. 인코딩과 바이트 순서는 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의되어 있습니다.

MLKEM*_CT 키는 실제로는 공개키가 아니라, Noise 핸드셰이크에서 Bob이 Alice에게 보내는 "암호문"입니다. 완성도를 위해 여기에 나열되어 있습니다.

### 합법적인 조합

새로운 Private Key 유형은 다음과 같습니다:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
하이브리드 개인키는 X25519 키입니다. KEM 개인키는 Alice 전용입니다. KEM 인코딩 및 바이트 순서는 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의되어 있습니다.

### 새로운 암호화 필요

새로운 Signing Public Key 유형은 다음과 같습니다:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
하이브리드 서명 공개 키는 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 키 다음에 PQ 키가 오는 형태입니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 정의됩니다.

### 대안

새로운 Signing Private Key 유형은 다음과 같습니다:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
하이브리드 서명 개인 키는 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 키 다음에 PQ 키가 오는 형태입니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의되어 있습니다.

### Rosenpass

새로운 서명 유형은 다음과 같습니다:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
하이브리드 서명은 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 서명에 이어 PQ 서명이 따라오는 형태입니다. 하이브리드 서명은 두 서명을 모두 검증하여 확인되며, 둘 중 하나라도 실패하면 전체가 실패합니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의되어 있습니다.

### Key Certificates

새로운 Signing Public Key 유형은 다음과 같습니다:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
새로운 암호화 공개 키 유형은 다음과 같습니다:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
하이브리드 키 타입은 키 인증서에 절대 포함되지 않으며, leaseSet에만 포함됩니다.

Hybrid 또는 PQ 서명 유형을 가진 목적지의 경우, 암호화 유형에 NONE (유형 255)을 사용하지만, 암호화 키는 없으며, 전체 384바이트 메인 섹션은 서명 키를 위한 것입니다.

### 공통 구조

새로운 Destination 타입의 길이는 다음과 같습니다. 모든 타입의 암호화 타입은 NONE (타입 255)이며 암호화 키 길이는 0으로 처리됩니다. 전체 384바이트 섹션이 서명 공개 키의 첫 번째 부분에 사용됩니다. 참고: 이는 ECDSA_SHA512_P521 및 RSA 서명 타입에 대한 사양과 다릅니다. 해당 타입들에서는 사용하지 않더라도 destination에 256바이트 ElGamal 키를 유지했습니다.

패딩 없음. 전체 길이는 7 + 총 키 길이입니다. 키 인증서 길이는 4 + 초과 키 길이입니다.

MLDSA44에 대한 1319바이트 destination 바이트 스트림 예시:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

새로운 Destination 타입들의 길이는 다음과 같습니다. 모든 타입의 암호화 타입은 X25519 (타입 4)입니다. X25519 공개 키 이후의 전체 352바이트 섹션은 서명 공개 키의 첫 번째 부분에 사용됩니다. 패딩은 없습니다. 총 길이는 39 + 총 키 길이입니다. 키 인증서 길이는 4 + 초과 키 길이입니다.

MLDSA44에 대한 예시 1351바이트 router identity 바이트 스트림:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PrivateKey

핸드셰이크는 [Noise Protocol](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드
- e1 = 일회용 임시 PQ 키, Alice에서 Bob으로 전송
- ekem1 = KEM 암호문, Bob에서 Alice로 전송

하이브리드 순방향 보안(hfs)을 위한 XK와 IK에 대한 다음 수정 사항들은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 5에 명시된 바와 같습니다:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
e1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 대로 다음과 같이 정의됩니다:

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
ekem1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 바와 같이 다음과 같이 정의됩니다:

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### SigningPublicKey

#### Issues

- handshake 해시 함수를 변경해야 할까요? [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)을 참조하세요.
  SHA256은 PQ에 취약하지 않지만, 해시 함수를 업그레이드하려고 한다면
  다른 것들을 변경하고 있는 지금이 적절한 시기입니다.
  현재 IETF SSH 제안 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)은 MLKEM768과
  SHA256을 사용하고, MLKEM1024와 SHA384를 사용하는 것입니다. 해당 제안에는
  보안 고려 사항에 대한 논의가 포함되어 있습니다.
- 0-RTT ratchet 데이터 전송을 중단해야 할까요 (LS 제외)?
- 0-RTT 데이터를 전송하지 않는다면 ratchet을 IK에서 XK로 전환해야 할까요?

#### Overview

이 섹션은 IK와 XK 프로토콜 모두에 적용됩니다.

하이브리드 핸드셰이크는 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 정의되어 있습니다. Alice에서 Bob으로의 첫 번째 메시지는 메시지 페이로드 앞에 캡슐화 키인 e1을 포함합니다. 이것은 추가적인 정적 키로 처리되며, (Alice로서) `EncryptAndHash()`를 호출하거나 (Bob으로서) `DecryptAndHash()`를 호출합니다. 그런 다음 메시지 페이로드를 평상시와 같이 처리합니다.

Bob에서 Alice로의 두 번째 메시지는 메시지 페이로드 앞에 ekem1인 암호문을 포함합니다. 이것은 추가적인 정적 키로 처리됩니다. (Bob으로서) EncryptAndHash()를 호출하거나 (Alice로서) DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 그 후 메시지 페이로드를 평소와 같이 처리합니다.

#### Defined ML-KEM Operations

다음과 같이 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서 정의된 암호학적 구성 요소에 해당하는 함수들을 정의합니다.

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

encap_key와 ciphertext 모두 Noise handshake 메시지 1과 2의 ChaCha/Poly 블록 내에서 암호화된다는 점에 유의하세요. 이들은 handshake 과정의 일부로 복호화됩니다.

kem_shared_key는 MixHash()를 사용하여 chaining key에 혼합됩니다. 자세한 내용은 아래를 참조하세요.

#### Alice KDF for Message 1

XK의 경우: 'es' 메시지 패턴 이후 그리고 페이로드 이전에 추가:

또는

IK의 경우: 'es' 메시지 패턴 이후이고 's' 메시지 패턴 이전에 다음을 추가:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 1

XK의 경우: 'es' 메시지 패턴 이후이고 페이로드 이전에 다음을 추가합니다:

또는

IK의 경우: 'es' 메시지 패턴 이후 그리고 's' 메시지 패턴 이전에 다음을 추가:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### Bob KDF for Message 2

XK의 경우: 'ee' 메시지 패턴 이후와 페이로드 이전에 다음을 추가하세요:

또는

IK의 경우: 'ee' 메시지 패턴 이후 그리고 'se' 메시지 패턴 이전에 다음을 추가하세요:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### Alice KDF for Message 2

'ee' 메시지 패턴 이후에 (그리고 IK의 경우 'ss' 메시지 패턴 이전에), 다음을 추가합니다:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.
```
#### KDF for Message 3 (XK only)

변경되지 않음

#### KDF for split()

변경되지 않음

### SigningPrivateKey

다음과 같이 ECIES-Ratchet 명세서 [/docs/specs/ecies/](/docs/specs/ecies/)를 업데이트하세요:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

변경 사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 정적 키를, 두 번째 섹션에 페이로드를 포함하고 있었습니다. ML-KEM을 사용하면 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ 공개 키를 포함합니다. 두 번째 섹션은 정적 키를 포함합니다. 세 번째 섹션은 페이로드를 포함합니다.

암호화된 형식:

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
복호화된 형식:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
크기:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
페이로드에는 DateTime 블록이 포함되어야 하므로 최소 페이로드 크기는 7입니다. 최소 메시지 1 크기는 그에 따라 계산될 수 있습니다.

#### 1g) New Session Reply format

변경 사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 빈 페이로드를, 두 번째 섹션에 페이로드를 가집니다. ML-KEM을 사용하면 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ 암호문을 포함합니다. 두 번째 섹션은 빈 페이로드를 가집니다. 세 번째 섹션은 페이로드를 포함합니다.

암호화된 형식:

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |       ChaCha20 encrypted data         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
```
복호화된 형식:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
크기:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
메시지 2는 일반적으로 0이 아닌 페이로드를 가지지만, ratchet 사양 [/docs/specs/ecies/](/docs/specs/ecies/)에서는 이를 요구하지 않으므로 최소 페이로드 크기는 0입니다. 따라서 최소 메시지 2 크기를 그에 따라 계산할 수 있습니다.

### 서명

NTCP2 사양서 [/docs/specs/ntcp2/](/docs/specs/ntcp2/)를 다음과 같이 업데이트하세요:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

변경 사항: 현재 NTCP2는 ChaCha 섹션의 옵션들만 포함합니다. ML-KEM을 사용하면, ChaCha 섹션에는 암호화된 PQ 공개 키도 포함될 것입니다.

원시 내용:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
크기:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원은 router 주소에 표시됩니다.

#### 2) SessionCreated

변경사항: 현재 NTCP2는 ChaCha 섹션의 옵션들만 포함합니다. ML-KEM과 함께, ChaCha 섹션은 암호화된 PQ 공개 키도 포함하게 됩니다.

원시 내용:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
크기:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
참고: 유형 코드는 내부 사용 전용입니다. Router는 유형 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

#### 3) SessionConfirmed

변경되지 않음

#### Key Derivation Function (KDF) (for data phase)

변경되지 않음

### 키 인증서

SSU2 사양 [/docs/specs/ssu2/](/docs/specs/ssu2/)을 다음과 같이 업데이트하세요:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

긴 헤더는 32바이트입니다. 세션이 생성되기 전에 Token Request, SessionRequest, SessionCreated, Retry에 사용됩니다. 또한 세션 외 Peer Test와 Hole Punch 메시지에도 사용됩니다.

TODO: 내부적으로 version 필드를 사용하여 MLKEM512에는 3을, MLKEM768에는 4를 사용할 수 있습니다. 이것을 타입 0과 1에만 적용할지 아니면 모든 6개 타입에 적용할지요?

헤더 암호화 이전:

```

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

변경되지 않음

#### SessionRequest (Type 0)

변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다. ML-KEM을 사용하면 ChaCha 섹션에 암호화된 PQ 공개 키도 포함됩니다.

원본 내용:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
IP 오버헤드를 포함하지 않은 크기:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원 여부는 router 주소에서 표시됩니다.

MLKEM768_X25519의 최소 MTU: IPv4의 경우 약 1316, IPv6의 경우 1336.

#### SessionCreated (Type 1)

변경사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다. ML-KEM과 함께, ChaCha 섹션은 암호화된 PQ 공개 키도 포함하게 됩니다.

원본 내용:

```
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

```
+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
크기, IP 오버헤드 제외:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
참고: Type 코드는 내부 사용 전용입니다. Router는 type 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

MLKEM768_X25519의 최소 MTU: IPv4의 경우 약 1316, IPv6의 경우 1336.

#### SessionConfirmed (Type 2)

변경되지 않음

#### KDF for data phase

변경되지 않음

#### 문제점

Relay 블록, Peer Test 블록, 그리고 Peer Test 메시지는 모두 서명을 포함합니다. 안타깝게도 PQ 서명은 MTU보다 큽니다. 현재 Relay 또는 Peer Test 블록이나 메시지를 여러 UDP 패킷에 걸쳐 분할하는 메커니즘이 없습니다. 프로토콜은 분할을 지원하도록 확장되어야 합니다. 이는 별도의 제안서(TBD)에서 수행될 예정입니다. 이것이 완료될 때까지 Relay와 Peer Test는 지원되지 않습니다.

#### 개요

내부적으로 version 필드를 사용하여 MLKEM512에는 3을, MLKEM768에는 4를 사용할 수 있습니다.

메시지 1과 2의 경우, MLKEM768은 패킷 크기를 1280 최소 MTU를 초과하여 증가시킬 것입니다. MTU가 너무 낮다면 해당 연결에 대해서는 지원하지 않을 것 같습니다.

메시지 1과 2의 경우, MLKEM1024는 패킷 크기를 최대 MTU인 1500을 초과하도록 증가시킬 것입니다. 이는 메시지 1과 2의 분할이 필요하며, 큰 복잡성을 야기할 것입니다. 아마도 구현하지 않을 것입니다.

Relay 및 Peer Test: 위 참조

### 목적지 크기

TODO: signature를 복사하지 않고 signing/verification을 정의하는 더 효율적인 방법이 있는가?

### RouterIdent 크기

할 일

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) 섹션 8.1은 구현 복잡성과 보안성 저하로 인해 X.509 인증서에서 HashML-DSA를 허용하지 않으며 HashML-DSA에 대한 OID를 할당하지 않습니다.

SU3 파일의 PQ 전용 서명의 경우, 인증서에 대해 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)에서 정의된 non-prehash 변형의 OID를 사용합니다. 파일을 두 번 해시해야 할 수 있기 때문에(HashML-DSA와 X2559가 동일한 해시 함수 SHA512를 사용하더라도) SU3 파일의 하이브리드 서명은 정의하지 않습니다. 또한 X.509 인증서에서 두 개의 키와 서명을 연결하는 것은 완전히 비표준입니다.

SU3 파일의 Ed25519 서명은 허용하지 않으며, Ed25519ph 서명을 정의했지만 이에 대한 OID에 합의한 적이 없고 사용한 적도 없습니다.

일반적인 서명 유형은 SU3 파일에서 허용되지 않습니다. ph(프리해시) 변형을 사용하세요.

### 핸드셰이크 패턴

새로운 최대 Destination 크기는 2599바이트(base 64에서 3468바이트)가 됩니다.

Destination 크기에 대한 지침을 제공하는 다른 문서들을 업데이트하십시오:

- SAMv3
- Bittorrent
- 개발자 가이드라인
- 네이밍 / 주소록 / 점프 서버
- 기타 문서

## Overhead Analysis

### Noise Handshake KDF

크기 증가 (바이트):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
속도:

[Cloudflare](https://blog.cloudflare.com/pq-2024/)에서 보고된 속도:

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Java 예비 테스트 결과:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

크기:

일반적인 키, 서명, RIdent, Dest 크기 또는 크기 증가 (참고용으로 Ed25519 포함), RI에 대해 X25519 암호화 유형을 가정. Router Info, LeaseSet, 응답 가능한 데이터그램, 그리고 나열된 두 개의 스트리밍 패킷(SYN 및 SYN ACK) 각각에 대한 추가 크기. 현재 Destinations 및 Leasesets은 반복되는 패딩을 포함하고 전송 중 압축 가능합니다. 새로운 유형은 패딩을 포함하지 않으며 압축할 수 없어서, 전송 중 크기 증가가 훨씬 더 높아집니다. 위의 설계 섹션을 참조하세요.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
속도:

[Cloudflare](https://blog.cloudflare.com/pq-2024/)에서 보고된 속도:

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Java에서의 예비 테스트 결과:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

NIST 보안 카테고리는 [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 슬라이드 10에 요약되어 있습니다. 예비 기준: 하이브리드 프로토콜의 경우 최소 NIST 보안 카테고리는 2여야 하고, PQ 전용의 경우 3이어야 합니다.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

이것들은 모두 하이브리드 프로토콜입니다. 아마도 MLKEM768을 선호해야 할 것입니다. MLKEM512는 충분히 안전하지 않습니다.

NIST 보안 카테고리 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

이 제안서는 하이브리드 및 PQ 전용 서명 유형을 모두 정의합니다. MLDSA44 하이브리드가 MLDSA65 PQ 전용보다 바람직합니다. MLDSA65와 MLDSA87의 키 및 서명 크기는 적어도 처음에는 우리에게 너무 클 것 같습니다.

NIST 보안 카테고리 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

3가지 암호화 방식과 9가지 서명 유형을 정의하고 구현할 예정이지만, 개발 과정에서 성능을 측정하고 구조 크기 증가의 영향을 추가로 분석할 계획입니다. 또한 다른 프로젝트와 프로토콜의 개발 동향을 지속적으로 연구하고 모니터링할 것입니다.

1년 이상의 개발 후에 각 사용 사례에 대해 선호하는 유형 또는 기본값을 정하려고 할 것입니다. 선택에는 대역폭, CPU, 그리고 추정 보안 수준 간의 절충이 필요할 것입니다. 모든 유형이 모든 사용 사례에 적합하거나 허용되지는 않을 수 있습니다.

예비 설정은 다음과 같으며, 변경될 수 있습니다:

암호화: MLKEM768_X25519

서명: MLDSA44_EdDSA_SHA512_Ed25519

예비 제한사항은 다음과 같으며, 변경될 수 있습니다:

암호화: MLKEM1024_X25519는 SSU2에서 허용되지 않음

서명: MLDSA87 및 하이브리드 변형은 아마도 너무 클 것이고; MLDSA65 및 하이브리드 변형은 너무 클 수도 있음

## Implementation Notes

### Library Support

Bouncycastle, BoringSSL, WolfSSL 라이브러리들이 현재 MLKEM과 MLDSA를 지원합니다. OpenSSL 지원은 2025년 4월 8일 3.5 릴리스에서 제공될 예정입니다 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Java I2P에서 적용한 southernstorm.com Noise 라이브러리는 하이브리드 핸드셰이크에 대한 예비 지원을 포함하고 있었지만, 사용되지 않아 제거했습니다. [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 맞춰 다시 추가하고 업데이트해야 할 것입니다.

### Signing Variants

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 섹션 3.4에 정의된 바와 같이 "determinstic" 변형이 아닌 "hedged" 또는 무작위화된 서명 변형을 사용할 것입니다. 이는 동일한 데이터에 대해서도 각 서명이 다르도록 보장하며, 사이드 채널 공격에 대한 추가적인 보호를 제공합니다. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 "hedged" 변형이 기본값이라고 명시하고 있지만, 다양한 라이브러리에서는 그렇지 않을 수도 있습니다. 구현자들은 서명에 "hedged" 변형이 사용되도록 반드시 확인해야 합니다.

우리는 메시지를 내부적으로 0x00 || len(ctx) || ctx || message로 인코딩하는 일반적인 서명 프로세스(Pure ML-DSA Signature Generation이라고 함)를 사용합니다. 여기서 ctx는 0x00..0xFF 크기의 선택적 값입니다. 우리는 선택적 컨텍스트를 사용하지 않습니다. len(ctx) == 0입니다. 이 프로세스는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10과 Algorithm 3 step 5에 정의되어 있습니다. 일부 공개된 테스트 벡터는 메시지가 인코딩되지 않는 모드 설정이 필요할 수 있다는 점에 유의하십시오.

### Reliability

크기 증가는 NetDB 저장, 스트리밍 핸드셰이크 및 기타 메시지에 대해 훨씬 더 많은 tunnel 단편화를 초래할 것입니다. 성능 및 안정성 변화를 확인하세요.

### Structure Sizes

router info와 leaseSet의 바이트 크기를 제한하는 모든 코드를 찾고 확인하세요.

### NetDB

RAM이나 디스크에 저장되는 최대 LS/RI를 검토하고 가능한 경우 줄여서 저장 공간 증가를 제한하십시오. floodfill의 최소 대역폭 요구사항을 늘릴까요?

### Ratchet

#### 정의된 ML-KEM 연산

동일한 tunnel에서 여러 프로토콜의 자동 분류/탐지는 메시지 1(New Session Message)의 길이 확인을 기반으로 가능해야 합니다. MLKEM512_X25519를 예로 들면, 메시지 1 길이는 현재 ratchet 프로토콜보다 816바이트 더 크며, 최소 메시지 1 크기(DateTime 페이로드만 포함된 경우)는 919바이트입니다. 현재 ratchet을 사용하는 대부분의 메시지 1 크기는 페이로드가 816바이트 미만이므로 비하이브리드 ratchet으로 분류할 수 있습니다. 큰 메시지는 아마도 드문 POST일 것입니다.

따라서 권장하는 전략은 다음과 같습니다:

- 메시지 1이 919바이트 미만이면, 현재 ratchet 프로토콜입니다.
- 메시지 1이 919바이트 이상이면, MLKEM512_X25519일 가능성이 높습니다.
  MLKEM512_X25519를 먼저 시도하고, 실패하면 현재 ratchet 프로토콜을 시도하세요.

이를 통해 이전에 동일한 목적지에서 ElGamal과 ratchet을 지원했던 것처럼, 동일한 목적지에서 표준 ratchet과 하이브리드 ratchet을 효율적으로 지원할 수 있습니다. 따라서 동일한 목적지에 대해 이중 프로토콜을 지원할 수 없다면 가능했을 것보다 훨씬 더 빠르게 MLKEM 하이브리드 프로토콜로 마이그레이션할 수 있습니다. 기존 목적지에 MLKEM 지원을 추가할 수 있기 때문입니다.

지원되는 필수 조합은 다음과 같습니다:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

다음 조합들은 복잡할 수 있으며, 반드시 지원되어야 하는 것은 아니지만, 구현에 따라 지원될 수 있습니다:

- 하나 이상의 MLKEM
- ElG + 하나 이상의 MLKEM
- X25519 + 하나 이상의 MLKEM
- ElG + X25519 + 하나 이상의 MLKEM

동일한 destination에서 여러 MLKEM 알고리즘(예: MLKEM512_X25519와 MLKEM_768_X25519)을 지원하려고 시도하지 않을 수 있습니다. 하나만 선택하세요. 그러나 이는 선호하는 MLKEM 변형을 선택하는 것에 달려 있으므로 HTTP 클라이언트 tunnel이 하나를 사용할 수 있습니다. 구현에 따라 달라집니다.

동일한 목적지에서 세 가지 알고리즘(예: X25519, MLKEM512_X25519, MLKEM769_X25519)을 지원하려고 시도할 수 있습니다. 분류 및 재시도 전략이 너무 복잡할 수 있습니다. 구성 및 구성 UI가 너무 복잡할 수 있습니다. 구현에 따라 다릅니다.

동일한 목적지에서 ElGamal과 hybrid 알고리즘을 모두 지원하려고 시도하지는 않을 것입니다. ElGamal은 구식이며, ElGamal + hybrid만 사용하는 것(X25519 없이)은 별로 의미가 없습니다. 또한 ElGamal과 Hybrid New Session Messages는 모두 크기가 크므로, 분류 전략에서 종종 두 가지 복호화를 모두 시도해야 하는데 이는 비효율적입니다. 구현에 따라 달라집니다.

클라이언트는 동일한 터널에서 X25519 및 hybrid 프로토콜에 대해 동일하거나 다른 X25519 정적 키를 사용할 수 있으며, 이는 구현에 따라 달라집니다.

#### Message 1을 위한 Alice KDF

ECIES 명세서는 New Session Message 페이로드에서 Garlic Messages를 허용하며, 이는 일반적으로 HTTP GET인 초기 스트리밍 패킷을 클라이언트의 leaseset과 함께 0-RTT 전달할 수 있게 해줍니다. 그러나 New Session Message 페이로드는 forward secrecy를 제공하지 않습니다. 이 제안이 ratchet의 향상된 forward secrecy를 강조하고 있으므로, 구현체들은 첫 번째 Existing Session Message까지 스트리밍 페이로드나 전체 스트리밍 메시지의 포함을 연기할 수 있거나 연기해야 할 수 있습니다. 이는 0-RTT 전달을 포기하는 대가를 치르게 됩니다. 전략은 트래픽 유형이나 터널 유형, 또는 예를 들어 GET 대 POST에 따라 달라질 수도 있습니다. 구현체에 따라 결정됩니다.

#### 메시지 1을 위한 Bob KDF

동일한 목적지에서 MLKEM, MLDSA 또는 둘 다 사용하면 위에서 설명한 바와 같이 New Session Message의 크기가 크게 증가합니다. 이는 1024바이트 tunnel 메시지로 분할되어야 하는 터널을 통한 New Session Message 전송의 신뢰성을 크게 감소시킬 수 있습니다. 전송 성공률은 조각 수의 지수에 비례합니다. 구현체는 0-RTT 전송을 포기하는 대신 메시지 크기를 제한하는 다양한 전략을 사용할 수 있습니다. 구현에 따라 달라집니다.

### Ratchet

세션 요청에서 임시 키의 MSB(key[31] & 0x80)를 설정하여 이것이 하이브리드 연결임을 나타낼 수 있습니다. 이를 통해 동일한 포트에서 표준 NTCP와 하이브리드 NTCP를 모두 실행할 수 있습니다. 하나의 하이브리드 변형만 지원되며, router 주소에서 광고됩니다. 예를 들어, v=2,3 또는 v=2,4 또는 v=2,5와 같습니다.

그렇게 하지 않으면, 다른 전송 주소/포트와 "NTCP1PQ1"과 같은 새로운 프로토콜 이름이 필요합니다.

참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

할 일

### SSU2

다른 전송 주소/포트가 필요할 수도 있지만, 그렇지 않기를 바란다. 메시지 1에 대한 플래그가 있는 헤더가 있다. 내부적으로 버전 필드를 사용하여 MLKEM512에는 3을, MLKEM768에는 4를 사용할 수 있다. 주소에서 v=2,3,4만으로도 충분할 수 있다. 하지만 두 새로운 알고리즘에 대한 식별자가 필요하다: 3a, 3b?

SSU2가 여러 패킷(6-8개?)에 걸쳐 분할된 RI를 처리할 수 있는지 확인하고 검증하세요. i2pd는 현재 최대 2개의 분할만 지원합니까?

참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

할 일

## Router Compatibility

### Transport Names

버전 플래그를 사용하여 표준과 하이브리드를 동일한 포트에서 실행할 수 있다면, 새로운 전송 이름이 필요하지 않을 것입니다.

새로운 전송 이름이 필요한 경우, 다음과 같습니다:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
SSU2는 MLKEM1024를 지원할 수 없으며, 크기가 너무 큽니다.

### Router Enc. Types

고려할 수 있는 몇 가지 대안이 있습니다:

#### Bob KDF for Message 2

권장하지 않습니다. router 타입과 일치하는 위에 나열된 새로운 전송 방식만 사용하세요. 구형 router는 연결하거나, 터널을 구축하거나, netDb 메시지를 전송할 수 없습니다. 기본적으로 활성화하기 전에 디버그하고 지원을 보장하려면 여러 릴리스 주기가 필요할 것입니다. 아래 대안들보다 배포를 1년 이상 연장할 수 있습니다.

#### Message 2를 위한 Alice KDF

권장됨. PQ가 X25519 정적 키나 N handshake 프로토콜에 영향을 주지 않으므로, router를 타입 4로 유지하고 새로운 전송 방식만 알릴 수 있습니다. 기존 router들은 여전히 연결하고, tunnel을 구축하거나, netDb 메시지를 보낼 수 있습니다.

#### 메시지 3용 KDF (XK만 해당)

Type 4 router들은 NTCP2와 NTCP2PQ* 주소를 모두 광고할 수 있습니다. 이들은 동일한 정적 키와 다른 매개변수들을 사용할 수도 있고, 그렇지 않을 수도 있습니다. 이들은 아마도 서로 다른 포트에 있어야 할 것입니다. 동일한 포트에서 NTCP2와 NTCP2PQ* 프로토콜을 모두 지원하는 것은 매우 어려울 것입니다. 왜냐하면 Bob이 들어오는 Session Request 메시지를 분류하고 프레이밍할 수 있도록 해주는 헤더나 프레이밍이 없기 때문입니다.

별도의 포트와 주소는 Java에서는 어렵지만 i2pd에서는 간단할 것입니다.

#### split()를 위한 KDF

Type 4 router들은 SSU2와 SSU2PQ* 주소를 모두 광고할 수 있습니다. 추가된 헤더 플래그를 통해 Bob은 첫 번째 메시지에서 들어오는 전송 타입을 식별할 수 있습니다. 따라서 동일한 포트에서 SSU2와 SSUPQ*를 모두 지원할 수 있습니다.

이것들은 별도의 주소로 게시될 수 있거나 (i2pd가 이전 전환에서 했던 것처럼) PQ 지원을 나타내는 매개변수와 함께 동일한 주소에 게시될 수 있습니다 (Java i2p가 이전 전환에서 했던 것처럼).

동일한 주소이거나 다른 주소의 동일한 포트에 있는 경우, 이들은 동일한 정적 키와 기타 매개변수를 사용합니다. 다른 주소의 다른 포트에 있는 경우, 이들은 동일한 정적 키와 기타 매개변수를 사용할 수도 있고 그렇지 않을 수도 있습니다.

별도의 포트와 주소는 Java에서는 어려울 것이지만 i2pd에서는 간단합니다.

#### Recommendations

할 일

### NTCP2

#### Noise 식별자

구형 router들은 RI를 검증하므로 연결, 터널 구축, netDb 메시지 전송이 불가능합니다. 기본적으로 활성화하기 전에 디버깅하고 지원을 보장하려면 여러 릴리스 주기가 필요할 것입니다. enc. type 5/6/7 출시와 동일한 문제가 발생할 것이며, 위에 나열된 type 4 enc. type 출시 대안보다 출시가 1년 이상 연장될 수 있습니다.

대안 없음.

### LS Enc. Types

#### 1b) 새로운 세션 형식 (바인딩 포함)

이들은 오래된 타입 4 X25519 키와 함께 LS에 존재할 수 있습니다. 오래된 router들은 알 수 없는 키들을 무시할 것입니다.

Destination은 여러 키 유형을 지원할 수 있지만, 각 키로 메시지 1의 시행착오 복호화를 수행해야만 가능합니다. 각 키에 대한 성공적인 복호화 횟수를 유지하고 가장 많이 사용된 키를 먼저 시도함으로써 오버헤드를 완화할 수 있습니다. Java I2P는 동일한 destination에서 ElGamal+X25519에 대해 이 전략을 사용합니다.

### Dest. Sig. Types

#### 1g) 새로운 세션 응답 형식

Router들은 leaseSet 서명을 검증하므로 타입 12-17 목적지에 대해 연결하거나 leaseSet을 받을 수 없습니다. 기본적으로 활성화하기 전에 디버깅하고 지원을 보장하는 데 여러 릴리스 주기가 필요할 것입니다.

대안 없음.

## 명세

가장 중요한 데이터는 ratchet으로 암호화된 종단 간 트래픽입니다. tunnel hop 사이의 외부 관찰자로서는 tunnel 암호화와 전송 암호화로 두 번 더 암호화됩니다. OBEP와 IBGW 사이의 외부 관찰자로서는 전송 암호화로 한 번 더만 암호화됩니다. OBEP 또는 IBGW 참가자로서는 ratchet이 유일한 암호화입니다. 하지만 tunnel은 단방향이므로, ratchet 핸드셰이크에서 양쪽 메시지를 모두 캡처하려면 동일한 router에 OBEP와 IBGW가 구축되지 않은 이상 router들 간의 공모가 필요합니다.

현재 가장 우려스러운 PQ 위협 모델은 오늘의 트래픽을 저장해 두었다가 수년 후에 복호화하는 것입니다 (순방향 비밀성). 하이브리드 접근 방식이 이를 방어할 수 있을 것입니다.

합리적인 기간(예: 몇 달) 내에 인증 키를 해독한 후 인증을 가장하거나 거의 실시간으로 암호를 해독하는 PQ 위협 모델은 훨씬 더 먼 미래의 일인가요? 그리고 그때가 바로 PQC 정적 키로 마이그레이션하고자 하는 시점일 것입니다.

따라서 가장 초기의 PQ 위협 모델은 나중에 복호화하기 위해 트래픽을 저장하는 OBEP/IBGW입니다. 하이브리드 ratchet을 먼저 구현해야 합니다.

Ratchet이 가장 높은 우선순위입니다. Transport가 그 다음이고, Signature가 가장 낮은 우선순위입니다.

서명 도입은 암호화 도입보다 1년 이상 늦어질 예정입니다. 역호환성이 불가능하기 때문입니다. 또한 업계의 MLDSA 채택은 CA/Browser Forum과 인증 기관에 의해 표준화될 것입니다. CA는 먼저 하드웨어 보안 모듈(HSM) 지원이 필요하지만, 현재는 사용할 수 없습니다 [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). CA/Browser Forum이 복합 서명 지원 또는 요구 여부를 포함하여 구체적인 매개변수 선택에 대한 결정을 주도할 것으로 예상합니다 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

동일한 터널에서 기존 ratchet 프로토콜과 새로운 ratchet 프로토콜을 모두 지원할 수 없다면, 마이그레이션이 훨씬 더 어려워질 것입니다.

X25519에서 했던 것처럼, 하나씩 차례로 시도해보면 되는 것으로 입증되어야 합니다.

## Issues

- Noise Hash 선택 - SHA256을 유지할지 아니면 업그레이드할지?
  SHA256은 향후 20-30년간 안전할 것이며, PQ에 의해 위협받지 않음,
  [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) 및 [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 참조.
  SHA256이 손상되면 더 심각한 문제가 있음 (netDb).
- NTCP2 별도 포트, 별도 router 주소
- SSU2 중계 / 피어 테스트
- SSU2 버전 필드
- SSU2 router 주소 버전
