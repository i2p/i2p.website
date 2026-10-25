---
title: "양자 후 암호화 프로토콜"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "열기"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### 상태

| 프로토콜 / 기능 | 상태 |
|--------------------|--------|
| Ratchet | Java I2P와 i2pd에서 완료 |
| NTCP2 | 2026년 1분기 베타 |
| SSU2 | 곧 구현 시작, 2026년 2-3분기 베타 |
| MLDSA SigTypes | 우선순위 낮음, 아마 2027년 이후 |
## 개요

적절한 양자 후 암호화(PQ) 기술에 대한 연구와 경쟁이 10년간 진행되어 왔지만, 선택지가 명확해진 것은 최근의 일입니다.

우리는 2022년에 PQ 암호화의 영향에 대해 살펴보기 시작했습니다 [zzz.i2p](http://zzz.i2p/topics/3294).

TLS 표준은 지난 2년간 하이브리드 암호화 지원을 추가했으며, Chrome과 Firefox의 지원으로 인해 현재 인터넷의 암호화된 트래픽 중 상당 부분에서 사용되고 있습니다 [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST는 최근 양자 후 암호학(post-quantum cryptography)을 위한 권장 알고리즘을 최종 확정하고 발표했습니다 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). 여러 일반적인 암호화 라이브러리들이 현재 NIST 표준을 지원하거나 가까운 미래에 지원을 출시할 예정입니다.

[Cloudflare](https://blog.cloudflare.com/pq-2024/)와 [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) 모두 즉시 마이그레이션을 시작할 것을 권장합니다. 2022년 NSA PQ FAQ [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)도 참조하세요. I2P는 보안과 암호화 분야의 리더가 되어야 합니다. 지금이 권장 알고리즘을 구현할 때입니다. 유연한 암호화 타입과 서명 타입 시스템을 사용하여 하이브리드 암호화, 그리고 PQ 및 하이브리드 서명을 위한 타입을 추가할 예정입니다.

## 목표

- PQ 저항 알고리즘 선택
- 적절한 I2P 프로토콜에 PQ 전용 및 하이브리드 알고리즘 추가
- 여러 변형 정의
- 구현, 테스트, 분석 및 연구 후 최적의 변형 선택
- 점진적으로 지원 추가하고 하위 호환성 유지

## 비목표

- 단방향(Noise N) 암호화 프로토콜을 변경하지 마세요
- SHA256에서 벗어나지 마세요. 단기적으로 PQ에 의해 위협받지 않습니다
- 현재로서는 최종 선호 변형을 선택하지 마세요

## 위협 모델

- OBEP나 IBGW의 router들이 공모하여 
  나중에 복호화하기 위해 garlic 메시지를 저장 (전진 보안성)
- 네트워크 관찰자들이
  나중에 복호화하기 위해 전송 메시지를 저장 (전진 보안성)
- 네트워크 참가자들이 RI, LS, streaming, datagram 또는
  기타 구조에 대한 서명을 위조

## 영향받는 프로토콜

다음 프로토콜들을 대략적인 개발 순서에 따라 수정할 예정입니다. 전체적인 출시는 2025년 말부터 2027년 중반까지 진행될 것으로 예상됩니다. 자세한 내용은 아래의 우선순위 및 출시 섹션을 참조하세요.

| 프로토콜 / 기능 | 상태 |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | 2025-06 승인; 2025-08 베타; 2025-11 릴리스 |
| Hybrid MLKEM NTCP2 | 라이브 네트워크에서 테스트됨, 2026-02 승인; 2026-05 베타 목표; 2026-08 릴리스 목표 |
| Hybrid MLKEM SSU2 | 2026-02 승인; 2026-08 베타 목표; 2026-11 릴리스 목표 |
| MLDSA SigTypes 12-14 | 제안이 안정적이나 2027년까지 최종 확정되지 않을 수 있음 |
| MLDSA Dests | 라이브 네트워크에서 테스트됨, floodfill 지원을 위한 네트워크 업그레이드 필요 |
| Hybrid SigTypes 15-17 | 예비 단계 |
| Hybrid Dests | |
## 설계

CRYSTALS-Kyber와 CRYSTALS-Dilithium(버전 3.1, 3 및 이전 버전)을 기반으로 하지만 호환되지 않는 NIST FIPS 203 및 204 표준 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)을 지원할 예정입니다.

### 키 교환

다음 프로토콜에서 하이브리드 키 교환을 지원할 예정입니다:

| 프로토콜 | Noise 타입 | PQ 전용 지원? | 하이브리드 지원? |
|---------|------------|---------------|-----------------|
| NTCP2   | XK         | no            | yes             |
| SSU2    | XK         | no            | yes             |
| Ratchet | IK         | no            | yes             |
| TBM     | N          | no            | no              |
| NetDB   | N          | no            | no              |
PQ KEM은 임시 키만 제공하며, Noise XK 및 IK와 같은 정적 키 핸드셰이크를 직접 지원하지 않습니다.

Noise N은 양방향 키 교환을 사용하지 않으므로 하이브리드 암호화에 적합하지 않습니다.

따라서 우리는 NTCP2, SSU2, 그리고 Ratchet에 대해서만 하이브리드 암호화를 지원할 것입니다. [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서와 같이 3개의 ML-KEM 변형을 정의하여 총 3개의 새로운 암호화 유형을 만들 것입니다. 하이브리드 유형은 X25519와 결합된 형태로만 정의됩니다.

새로운 암호화 유형은 다음과 같습니다:

| 타입 | 코드 |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
오버헤드가 상당할 것입니다. 일반적인 메시지 1과 2의 크기(XK 및 IK용)는 현재 약 100바이트입니다(추가 페이로드 제외). 이는 알고리즘에 따라 8배에서 15배까지 증가할 것입니다.

### 서명

다음 구조에서 PQ 및 하이브리드 서명을 지원할 예정입니다:

따라서 PQ 전용과 하이브리드 서명을 모두 지원할 예정입니다. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의된 대로 3개의 ML-DSA 변형, Ed25519와의 3개 하이브리드 변형, 그리고 SU3 파일 전용 prehash를 사용한 3개의 PQ 전용 변형을 정의하여 총 9개의 새로운 서명 유형을 만들 것입니다. 하이브리드 유형은 Ed25519와의 조합으로만 정의됩니다. SU3 파일을 제외하고는 pre-hash 변형(HashML-DSA)이 아닌 표준 ML-DSA를 사용할 것입니다.

| 유형 | PQ만 지원? | 하이브리드 지원? |
|------|------------------|-----------------|
| RouterInfo | 예 | 예 |
| LeaseSet | 예 | 예 |
| Streaming SYN/SYNACK/Close | 예 | 예 |
| Repliable Datagrams | 예 | 예 |
| Datagram2 (prop. 163) | 예 | 예 |
| I2CP create session msg | 예 | 예 |
| SU3 파일 | 예 | 예 |
| X.509 인증서 | 예 | 예 |
| Java keystores | 예 | 예 |
[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 섹션 3.4에서 정의된 대로 "deterministic" 변형이 아닌 "hedged" 또는 무작위화된 서명 변형을 사용할 것입니다. 이는 동일한 데이터에 대해서도 각 서명이 다르도록 보장하며, 사이드 채널 공격에 대한 추가적인 보호를 제공합니다. 인코딩과 컨텍스트를 포함한 알고리즘 선택에 대한 추가 세부사항은 아래의 구현 노트 섹션을 참조하십시오.

새로운 서명 유형은 다음과 같습니다:

X.509 인증서와 기타 DER 인코딩은 [IETF 초안](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에 정의된 복합 구조와 OID를 사용할 것입니다.

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
오버헤드가 상당할 것입니다. 일반적인 Ed25519 destination과 router identity 크기는 391바이트입니다. 이는 알고리즘에 따라 3.5배에서 6.8배까지 증가할 것입니다. Ed25519 서명은 64바이트입니다. 이는 알고리즘에 따라 38배에서 76배까지 증가할 것입니다. 일반적인 서명된 RouterInfo, LeaseSet, 응답 가능한 데이터그램, 그리고 서명된 스트리밍 메시지는 약 1KB입니다. 이는 알고리즘에 따라 3배에서 8배까지 증가할 것입니다.

새로운 destination과 router identity 유형에는 패딩이 포함되지 않으므로 압축할 수 없습니다. 전송 중에 gzip으로 압축되는 destination과 router identity의 크기는 알고리즘에 따라 12배에서 38배까지 증가할 것입니다.

Destination의 경우, 새로운 서명 타입들이 leaseSet의 모든 암호화 타입과 함께 지원됩니다. 키 인증서의 암호화 타입을 NONE (255)으로 설정하세요.

### 유효한 조합

RouterIdentities의 경우, ElGamal 암호화 유형은 더 이상 사용되지 않습니다. 새로운 서명 유형은 X25519 (타입 4) 암호화에서만 지원됩니다. 새로운 암호화 유형은 RouterAddresses에서 표시됩니다. key certificate의 암호화 유형은 계속해서 타입 4로 유지됩니다.

SHA3-256, SHAKE128, SHAKE256에 대한 테스트 벡터는 [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)에서 확인할 수 있습니다.

### 새로운 암호화 필요

- ML-KEM (이전 CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (이전 CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (이전 Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) SHAKE128에만 사용됨
- SHA3-256 (이전 Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 및 SHAKE256 (SHA3-128과 SHA3-256의 XOF 확장) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Java bouncycastle 라이브러리는 위의 모든 것을 지원합니다. C++ 라이브러리 지원은 OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)에 있습니다.

우리는 [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+)를 지원하지 않을 것입니다. ML-DSA보다 훨씬 더 느리고 큽니다. 또한 곧 출시될 FIPS206 (Falcon)도 지원하지 않을 것입니다. 아직 표준화되지 않았기 때문입니다. NIST에서 표준화하지 않은 NTRU나 다른 PQ 후보들도 지원하지 않을 것입니다.

### 대안

순수 PQ 암호화를 위한 Wireguard (IK) 적용에 대한 연구 [논문](https://eprint.iacr.org/2020/379.pdf)이 있지만, 해당 논문에는 여러 미해결 문제들이 있습니다. 나중에 이 접근법은 PQ Wireguard를 위한 Rosenpass [Rosenpass](https://rosenpass.eu/) [백서](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)로 구현되었습니다.

### Rosenpass

Rosenpass는 사전 공유된 Classic McEliece 460896 정적 키(각각 500 KB)와 Kyber-512(본질적으로 MLKEM-512) 임시 키를 사용하는 Noise KK 유사 핸드셰이크를 사용합니다. Classic McEliece 암호문은 188바이트에 불과하고 Kyber-512 공개 키와 암호문이 합리적이므로, 두 핸드셰이크 메시지 모두 표준 UDP MTU에 맞습니다. PQ KK 핸드셰이크의 출력 공유 키(osk)는 표준 Wireguard IK 핸드셰이크의 입력 사전 공유 키(psk)로 사용됩니다. 따라서 총 두 개의 완전한 핸드셰이크가 있으며, 하나는 순수 PQ이고 다른 하나는 순수 X25519입니다.

우리는 XK와 IK 핸드셰이크를 대체하기 위해 이런 것들을 할 수 없습니다. 왜냐하면:

백서에는 많은 좋은 정보가 있으며, 아이디어와 영감을 얻기 위해 이를 검토할 예정입니다. TODO.

- KK를 수행할 수 없습니다. Bob이 Alice의 정적 키를 가지고 있지 않기 때문입니다
- 500KB 정적 키는 너무 큽니다
- 추가 왕복 통신은 원하지 않습니다

다음과 같이 공통 구조 문서 [/docs/specs/common-structures/](/docs/specs/common-structures/)의 섹션과 테이블을 업데이트하세요:

## 사양

### 공통 구조

새로운 Public Key 유형은 다음과 같습니다:

#### 이슈

하이브리드 공개키는 X25519 키입니다. KEM 공개키는 Alice에서 Bob으로 전송되는 임시 PQ 키입니다. 인코딩과 바이트 순서는 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서 정의됩니다.

| 유형 | 공개 키 길이 | 버전 | 사용법 |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM768_X25519 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM1024_X25519 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM512 | 800 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM768 | 1184 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM1024 | 1568 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM512_CT | 768 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM768_CT | 1088 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM1024_CT | 1568 | 0.9.xx | 제안서 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| NONE | 0 | 0.9.xx | 제안서 169 참조, PQ 서명 유형이 있는 destination 전용, RI나 leaseSet에는 사용 안 함 |
MLKEM*_CT 키는 실제로는 공개키가 아니며, Noise 핸드셰이크에서 Bob이 Alice에게 보내는 "암호문"입니다. 완전성을 위해 여기에 나열되었습니다.

새로운 Private Key 유형은 다음과 같습니다:

#### PrivateKey

하이브리드 개인 키는 X25519 키입니다. KEM 개인 키는 Alice 전용입니다. KEM 인코딩과 바이트 순서는 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서 정의됩니다.

| 타입 | 개인 키 길이 | 버전 | 사용 |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | proposal 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM768_X25519 | 32 | 0.9.xx | proposal 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM1024_X25519 | 32 | 0.9.xx | proposal 169 참조, leaseSet 전용, RI나 Destination에는 사용 안 함 |
| MLKEM512 | 1632 | 0.9.xx | proposal 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM768 | 2400 | 0.9.xx | proposal 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
| MLKEM1024 | 3168 | 0.9.xx | proposal 169 참조, 핸드셰이크 전용, leaseSet, RI, Destination에는 사용 안 함 |
새로운 Signing Public Key 유형들은 다음과 같습니다:

#### SigningPublicKey

하이브리드 서명 공개 키는 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 키 다음에 PQ 키가 오는 형태입니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 정의됩니다.

| 유형 | 길이 (바이트) | 버전 | 사용법 |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | 제안서 169 참조 |
| MLDSA65 | 1952 | 0.9.xx | 제안서 169 참조 |
| MLDSA87 | 2592 | 0.9.xx | 제안서 169 참조 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | 제안서 169 참조 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | 제안서 169 참조 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | 제안서 169 참조 |
| MLDSA44ph | 1344 | 0.9.xx | SU3 파일 전용, netDb 구조체에는 사용 안 함 |
| MLDSA65ph | 1984 | 0.9.xx | SU3 파일 전용, netDb 구조체에는 사용 안 함 |
| MLDSA87ph | 2624 | 0.9.xx | SU3 파일 전용, netDb 구조체에는 사용 안 함 |
새로운 서명 개인키 유형은 다음과 같습니다:

#### SigningPrivateKey

하이브리드 서명 개인 키는 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 키 다음에 PQ 키가 오는 형태입니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 정의됩니다.

| 유형 | 길이 (바이트) | 버전 | 사용법 |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | proposal 169 참조 |
| MLDSA65 | 4032 | 0.9.xx | proposal 169 참조 |
| MLDSA87 | 4896 | 0.9.xx | proposal 169 참조 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | proposal 169 참조 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | proposal 169 참조 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | proposal 169 참조 |
| MLDSA44ph | 2592 | 0.9.xx | SU3 파일용만, netDb 구조용 아님. proposal 169 참조 |
| MLDSA65ph | 4064 | 0.9.xx | SU3 파일용만, netDb 구조용 아님. proposal 169 참조 |
| MLDSA87ph | 4928 | 0.9.xx | SU3 파일용만, netDb 구조용 아님. proposal 169 참조 |
새로운 서명 타입들은 다음과 같습니다:

하이브리드 서명은 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 서명 다음에 PQ 서명이 오는 형태입니다. 하이브리드 서명은 두 서명을 모두 검증하여 확인되며, 둘 중 하나라도 실패하면 전체가 실패합니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 정의됩니다.

#### 서명

새로운 서명 공개 키 유형은 다음과 같습니다:

| 타입 | 길이 (바이트) | 버전 | 사용법 |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | proposal 169 참조 |
| MLDSA65 | 3309 | 0.9.xx | proposal 169 참조 |
| MLDSA87 | 4627 | 0.9.xx | proposal 169 참조 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | proposal 169 참조 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | proposal 169 참조 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | proposal 169 참조 |
| MLDSA44ph | 2484 | 0.9.xx | SU3 파일에만 사용, netDb 구조에는 사용하지 않음. proposal 169 참조 |
| MLDSA65ph | 3373 | 0.9.xx | SU3 파일에만 사용, netDb 구조에는 사용하지 않음. proposal 169 참조 |
| MLDSA87ph | 4691 | 0.9.xx | SU3 파일에만 사용, netDb 구조에는 사용하지 않음. proposal 169 참조 |
새로운 암호화 공개 키 유형은 다음과 같습니다:

#### 키 인증서

하이브리드 서명 공개 키는 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)에서와 같이 Ed25519 키 다음에 PQ 키가 오는 형태입니다. 인코딩과 바이트 순서는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 정의됩니다.

| 유형 | 유형 코드 | 총 공개 키 길이 | 버전 | 용도 |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | proposal 169 참조 |
| MLDSA65 | 13 | 1952 | 0.9.xx | proposal 169 참조 |
| MLDSA87 | 14 | 2592 | 0.9.xx | proposal 169 참조 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | proposal 169 참조 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | proposal 169 참조 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | proposal 169 참조 |
| MLDSA44ph | 18 | n/a | 0.9.xx | SU3 파일에만 사용 |
| MLDSA65ph | 19 | n/a | 0.9.xx | SU3 파일에만 사용 |
| MLDSA87ph | 20 | n/a | 0.9.xx | SU3 파일에만 사용 |
Hybrid 또는 PQ 서명 유형을 가진 목적지의 경우, 암호화 유형으로 NONE (타입 255)을 사용하지만, 암호화 키는 없으며 전체 384바이트 메인 섹션은 서명 키를 위한 것입니다.

| 타입 | 타입 코드 | 전체 공개 키 길이 | 도입 버전 | 사용법 |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에서는 사용 불가 |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에서는 사용 불가 |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | 제안서 169 참조, leaseSet 전용, RI나 Destination에서는 사용 불가 |
| NONE | 255 | 0 | 0.9.xx | 제안서 169 참조 |
하이브리드 키 유형은 키 인증서에 포함되지 않으며, leaseSet에만 포함됩니다.

패딩 없음. 전체 길이는 7 + 전체 키 길이입니다. 키 인증서 길이는 4 + 초과 키 길이입니다.

#### Destination 크기

다음은 새로운 Destination 타입들의 길이입니다. 모든 타입의 Enc 타입은 NONE (타입 255)이며 암호화 키 길이는 0으로 처리됩니다. 전체 384바이트 섹션이 서명 공개 키의 첫 번째 부분에 사용됩니다. 참고: 이는 ECDSA_SHA512_P521과 RSA 서명 타입의 사양과는 다릅니다. 해당 타입들에서는 사용하지 않음에도 불구하고 destination에서 256바이트 ElGamal 키를 유지했습니다.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

MLDSA44에 대한 1319바이트 destination 바이트 스트림 예제:

MLDSA44에 대한 예시 1351바이트 router identity 바이트 스트림:

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### RouterIdent 크기

다음은 새로운 Destination 타입들의 길이입니다. 모든 타입의 암호화 타입은 X25519 (타입 4)입니다. X25519 공개 키 이후의 전체 352바이트 섹션이 서명 공개 키의 첫 번째 부분에 사용됩니다. 패딩은 없습니다. 총 길이는 39 + 총 키 길이입니다. 키 인증서 길이는 4 + 초과 키 길이입니다.

핸드셰이크는 [Noise Protocol](https://noiseprotocol.org/noise.html) 핸드셰이크 패턴을 사용합니다.

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| 타입 | 타입 코드 | 총 공개 키 길이 | 메인 | 초과 | 총 RouterIdent 길이 |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

hybrid forward secrecy (hfs)를 위한 XK와 IK에 대한 다음 수정 사항들은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 5에서 명시된 대로입니다:

e1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에 명시된 바와 같이 다음과 같이 정의됩니다:

#### split()을 위한 KDF

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Noise 식별자

ekem1 패턴은 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) 섹션 4에서 명시된 바와 같이 다음과 같이 정의됩니다:

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) 새 세션 형식 (바인딩 포함)

이 섹션은 IK와 XK 프로토콜 모두에 적용됩니다.

### 핸드셰이크 패턴

하이브리드 핸드셰이크는 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 정의되어 있습니다. Alice에서 Bob으로의 첫 번째 메시지는 메시지 페이로드 앞에 캡슐화 키인 e1을 포함합니다. 이는 추가적인 정적 키로 처리되며, (Alice로서) EncryptAndHash()를 호출하거나 (Bob으로서) DecryptAndHash()를 호출합니다. 그 다음 메시지 페이로드를 일반적인 방식으로 처리합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 임시 키
- s = 정적 키
- p = 메시지 페이로드
- e1 = Alice에서 Bob으로 전송되는 일회용 임시 PQ 키
- ekem1 = Bob에서 Alice로 전송되는 KEM 암호문

[FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에서 정의된 대로 사용되는 암호화 구성 요소에 해당하는 다음 함수들을 정의합니다.

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
(encap_key, decap_key) = PQ_KEYGEN()

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
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

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
### Noise Handshake KDF

#### 1b) 새 세션 형식 (바인딩 포함)

- 0-RTT ratchet 데이터 전송을 중단해야 하는가 (LS 제외)?
- 0-RTT 데이터를 전송하지 않는다면 ratchet을 IK에서 XK로 전환해야 하는가?

#### 개요

kem_shared_key = DECAPS(ciphertext, decap_key)

encap_key와 ciphertext 모두 Noise 핸드셰이크 메시지 1과 2의 ChaCha/Poly 블록 내부에서 암호화된다는 점에 유의하세요. 이들은 핸드셰이크 과정의 일부로 복호화됩니다.

Bob에서 Alice로의 두 번째 메시지는 메시지 페이로드 앞에 ekem1과 암호문을 포함합니다. 이는 추가적인 정적 키로 처리되며, (Bob으로서) EncryptAndHash()를 호출하거나 (Alice로서) DecryptAndHash()를 호출합니다. 그런 다음 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다. 그 후 평소와 같이 메시지 페이로드를 처리합니다.

#### 정의된 ML-KEM 연산

XK의 경우: 'es' 메시지 패턴 이후이고 페이로드 이전에 다음을 추가합니다:

또는

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

IK의 경우: 'es' 메시지 패턴 이후 그리고 's' 메시지 패턴 이전에 다음을 추가:

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

XK의 경우: 'es' 메시지 패턴 이후 페이로드 이전에 다음을 추가합니다:

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

또는

kem_shared_key는 MixHash()를 통해 체이닝 키와 혼합됩니다. 자세한 내용은 아래를 참조하세요.

#### Message 1을 위한 Alice KDF

XK의 경우: 'ee' 메시지 패턴 이후, 페이로드 이전에 다음을 추가합니다:

또는

IK의 경우: 'ee' 메시지 패턴 이후이고 'se' 메시지 패턴 이전에 다음을 추가:

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
#### 메시지 1에 대한 Bob KDF

XK의 경우: 'ee' 메시지 패턴 이후, 페이로드 이전에 다음을 추가합니다:

또는

IK의 경우: 'es' 메시지 패턴 이후와 's' 메시지 패턴 이전에 다음을 추가:

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
#### 메시지 2를 위한 Bob KDF

ECIES-Ratchet 명세 [/docs/specs/ecies/](/docs/specs/ecies/)를 다음과 같이 업데이트하세요:

또는

암호화된 형식:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 메시지 2에 대한 Alice KDF

'ee' 메시지 패턴 이후 (그리고 IK의 경우 'ss' 메시지 패턴 이전)에 다음을 추가하십시오:

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

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### 메시지 3을 위한 KDF (XK만 해당)

변경되지 않음

#### Noise 식별자

변경되지 않음

### 래칫

변경사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 빈 페이로드를 가지고, 두 번째 섹션에 페이로드를 가집니다. ML-KEM을 사용하면 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ 암호문을 포함합니다. 두 번째 섹션은 빈 페이로드를 가집니다. 세 번째 섹션은 페이로드를 포함합니다.

#### 긴 헤더

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 짧은 헤더

변경사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 정적 키를, 두 번째 섹션에 페이로드를 포함했습니다. ML-KEM에서는 이제 세 개의 섹션이 있습니다. 첫 번째 섹션은 암호화된 PQ 공개 키를 포함합니다. 두 번째 섹션은 정적 키를 포함합니다. 세 번째 섹션은 페이로드를 포함합니다.

복호화된 형식:

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

| 타입 | 타입 코드 | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
페이로드는 DateTime 블록을 포함해야 하므로, 최소 페이로드 크기는 7입니다. 최소 메시지 1 크기는 이에 따라 계산될 수 있습니다.

#### 1g) 새 세션 응답 형식

변경 사항: 현재 NTCP2는 ChaCha 섹션의 옵션만을 포함합니다. ML-KEM과 함께, ChaCha 섹션은 암호화된 PQ 공개 키도 포함하게 됩니다.

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
메시지 2는 일반적으로 0이 아닌 페이로드를 가지지만, ratchet 사양 [/docs/specs/ecies/](/docs/specs/ecies/)에서는 이를 요구하지 않으므로 최소 페이로드 크기는 0입니다. 최소 메시지 2 크기는 이에 따라 계산될 수 있습니다.

### NTCP2

NTCP2 사양 [/docs/specs/ntcp2/](/docs/specs/ntcp2/)을 다음과 같이 업데이트하세요:

#### 노이즈 식별자

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

추가 정보는 아래의 게시된 주소 섹션을 참조하세요.

변경 사항: 현재 NTCP2는 ChaCha 섹션의 옵션만 포함합니다. ML-KEM을 사용하면 ChaCha 섹션에 암호화된 PQ 공개 키도 포함됩니다.

암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

Alice의 경우, 메시지가 Noise로 암호화된 후 X의 AES 난독화 이전에 X[31] |= 0x7f를 설정합니다.

Bob의 경우, X의 AES 난독화 해제 후 X[31] & 0x80을 테스트합니다. 비트가 설정되어 있으면 X[31] &= 0x7f로 클리어하고 PQ 연결로 Noise를 통해 복호화합니다. 비트가 클리어되어 있으면 평소와 같이 비PQ 연결로 Noise를 통해 복호화합니다.

다른 router 주소와 포트에서 광고되는 PQ NTCP2의 경우, 이는 필수가 아닙니다.

원본 내용:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
원시 내용:

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

크기:

| 유형 | 유형 코드 | X 길이 | 메시지 1 길이 | 메시지 1 암호화 길이 | 메시지 1 복호화 길이 | PQ 키 길이 | 옵션 길이 |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
크기:

#### 2) SessionCreated

참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4를 유지하며, 지원 여부는 router 주소에 표시됩니다.

원본 내용:

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
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
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

| 유형 | 유형 코드 | Y 길이 | Msg 2 길이 | Msg 2 Enc 길이 | Msg 2 Dec 길이 | PQ CT 길이 | opt 길이 |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
크기:

#### 3) SessionConfirmed

참고: 타입 코드는 내부 용도로만 사용됩니다. Router는 타입 4를 유지하며, 지원 여부는 router 주소에 표시됩니다.

#### 키 유도 함수 (KDF) (데이터 단계용)

참고: 타입 코드는 내부 용도로만 사용됩니다. Router는 타입 4를 유지하며, 지원 여부는 router 주소에 표시됩니다.

#### 게시된 주소

변경 없음

non-PQ, 방화벽이 없는 경우와 동일한 주소/포트를 사용합니다. PQ 변형은 하나만 지원됩니다. router 주소에 평소와 같이 v=2와 MLKEM 512/768/1024를 나타내는 새 파라미터 pq=[3|4|5]를 게시합니다. Alice는 세션 요청에서 ephemeral key의 MSB(key[31] & 0x80)를 설정하여 하이브리드 연결임을 나타냅니다. 위를 참조하십시오. 이전 router들은 pq 파라미터를 무시하고 평소처럼 non-pq로 연결합니다.

비PQ와 다른 주소/포트, 또는 PQ 전용, 방화벽이 없는 환경은 지원되지 않습니다. 이는 비PQ NTCP2가 비활성화될 때까지, 즉 지금부터 몇 년 후까지 구현되지 않을 것입니다. 비PQ가 비활성화되면 여러 PQ 변형이 지원될 수 있지만, 주소당 하나만 지원됩니다. router 주소에서 MLKEM 512/768/1024를 나타내기 위해 v=[3|4|5]를 게시합니다. Alice는 ephemeral key의 MSB를 설정하지 않습니다. 이전 router들은 v 매개변수를 확인하고 이 주소를 지원되지 않는 것으로 건너뜁니다.

방화벽 주소 (IP 게시 안함): router 주소에서 v=2를 게시합니다 (평소와 같이). pq 매개변수를 게시할 필요는 없습니다.

Alice는 자신의 router 정보에서 pq 지원을 광고하는지 여부나 동일한 변형을 광고하는지 여부에 관계없이, Bob이 게시하는 PQ 변형을 사용하여 PQ Bob에 연결할 수 있습니다.

#### 최대 패딩

현재 사양에서 메시지 1과 2는 "적절한" 양의 패딩을 갖도록 정의되어 있으며, 0-31바이트 범위가 권장되고 최대값은 지정되지 않았습니다.

Java I2P는 non-PQ 연결에 대해 최대 256바이트 패딩을 구현하지만, 이는 이전에 문서화되지 않았습니다.

정의된 메시지 크기를 최대 패딩으로 사용합니다. 즉, 최대 패딩은 PQ connections에서 메시지 크기를 두 배로 만들며, 다음과 같습니다:

| Message Max Padding | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|-----------|-----------|------------|
| Session Request  |       880   |     1264   |    1648  |
| Session Created  |       848   |     1136   |    1616	 |
### SSU2

SSU2 사양 [/docs/specs/ssu2/](/docs/specs/ssu2/)을 다음과 같이 업데이트하세요:

#### 노이즈 식별자

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

MLKEM-1024는 키가 너무 커서 표준 1500바이트 데이터그램에 맞지 않기 때문에 SSU2에서 지원되지 않습니다.

#### 새 세션 크기

긴 헤더는 32바이트입니다. 이는 세션이 생성되기 전에 Token Request, SessionRequest, SessionCreated, 그리고 Retry에 사용됩니다. 또한 세션 외부의 Peer Test 및 Hole Punch 메시지에도 사용됩니다.

다음 메시지들에서는 긴 헤더의 ver(버전) 필드를 3 또는 4로 설정하여 MLKEM-512 또는 MLKEM-768을 나타냅니다.

- (0) 세션 요청
- (1) 세션 생성됨
- (9) 재시도
- (10) 토큰 요청
- (11) 홀 펀치

원본 내용:

- (7) Peer Test (세션 외 메시지 5-7)

암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

IP 오버헤드를 포함하지 않은 크기:

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

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### 난독화

변경되지 않음

#### SessionRequest (타입 0)

변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다. ML-KEM을 사용하면 ChaCha 섹션에 암호화된 PQ 공개 키도 포함됩니다.

스푸핑 방지를 위한 KDF 변경: Proposal 165 [Prop165]_에서 제기된 문제들을 해결하기 위해, 다른 해결책으로 Session Request에 대한 KDF를 수정합니다. 이는 PQ 세션에만 적용됩니다. 비-PQ 세션에 대한 KDF는 변경되지 않습니다.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
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
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
원시 내용:

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
참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원 여부는 router 주소에 표시됩니다.

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 | | | | |
크기:

MLKEM768_X25519의 최소 MTU: IPv4의 경우 약 1316, IPv6의 경우 1336.

원시 콘텐츠:

#### SessionCreated (타입 1)

변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다. ML-KEM을 사용하면 ChaCha 섹션에 암호화된 PQ 공개 키도 포함됩니다.

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
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
암호화되지 않은 데이터 (Poly1305 인증 태그는 표시되지 않음):

| 유형 | 유형 코드 | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 | | | | |
크기:

MLKEM768_X25519의 최소 MTU: IPv4의 경우 약 1316, IPv6의 경우 1336.

다음 블록들은 버전 필드를 포함합니다. 이들은 (non-PQ Bob과의 호환성을 위해) 버전 2를 유지하며, PQ에 대해 버전 3/4로 변경되지 않습니다.

#### SessionConfirmed (타입 2)

변경되지 않음

#### 데이터 단계를 위한 KDF

변경되지 않음

#### Relay 및 Peer Test

변경되지 않음

- SAMv3
- Bittorrent
- 개발자 가이드라인
- 네이밍 / 주소록 / 점프 서버
- 기타 문서

PQ 서명: Relay 블록, Peer Test 블록, 그리고 Peer Test 메시지는 모두 서명을 포함합니다. 안타깝게도 PQ 서명은 MTU보다 큽니다. 현재 Relay나 Peer Test 블록 또는 메시지를 여러 UDP 패킷에 걸쳐 분할하는 메커니즘이 없습니다. 프로토콜은 분할을 지원하도록 확장되어야 합니다. 이는 별도의 제안(TBD)에서 수행될 예정입니다. 이것이 완료될 때까지 Relay와 Peer Test는 지원되지 않습니다.

#### 게시된 주소

모든 경우에 평소와 같이 SSU2 전송 이름을 사용하세요. MLKEM-1024는 지원되지 않습니다.

Alice는 자신의 router 정보에서 pq 지원을 광고하는지 여부나 동일한 변형을 광고하는지 여부와 관계없이, Bob이 게시하는 PQ 변형을 사용하여 PQ Bob에 연결할 수 있습니다.

non-PQ와 다른 주소/포트, 또는 PQ 전용, 방화벽이 없는 환경은 지원되지 않습니다. 이는 몇 년 후 non-PQ SSU2가 비활성화될 때까지 구현되지 않을 예정입니다. non-PQ가 비활성화되면 하나 또는 두 개의 PQ 변형이 지원됩니다. router 주소에서 v=[3|4|3,4]를 게시하여 MLKEM 512/768/둘 다를 나타냅니다. 이전 버전의 router들은 v 매개변수를 확인하고 이 주소를 지원되지 않는 것으로 건너뛸 것입니다.

방화벽으로 보호된 주소 (IP가 공개되지 않음): router 주소에서 v=2를 게시합니다 (평소와 같이). 릴레이를 지원하기 위해 방화벽으로 보호된 주소에서는 pq 매개변수를 반드시 게시해야 합니다.

Alice는 자신의 router 정보에서 pq 지원을 광고하는지 여부나 동일한 변형을 광고하는지 여부에 관계없이, Bob이 게시하는 PQ 변형을 사용하여 PQ Bob에 연결할 수 있습니다.

#### MTU

TODO: 서명 복사를 피하기 위해 서명/검증을 정의하는 더 효율적인 방법이 있는가?

### 스트리밍

할 일

### SU3 파일

[IETF 초안](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) 섹션 8.1은 구현 복잡성과 보안 감소로 인해 X.509 인증서에서 HashML-DSA를 허용하지 않으며 HashML-DSA에 대한 OID를 할당하지 않습니다.

SU3 파일의 PQ 전용 서명의 경우, 인증서에 대해 [IETF 초안](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)에 정의된 non-prehash 변형의 OID를 사용합니다. SU3 파일의 하이브리드 서명은 정의하지 않는데, 파일을 두 번 해시해야 할 수도 있기 때문입니다(HashML-DSA와 X2559가 동일한 해시 함수 SHA512를 사용하긴 하지만). 또한 X.509 인증서에서 두 개의 키와 서명을 연결하는 것은 완전히 비표준입니다.

Ed25519를 사용한 SU3 파일 서명은 허용하지 않으며, Ed25519ph 서명을 정의했지만 이에 대한 OID에 합의하지 않았고 사용하지도 않았습니다.

일반 서명 유형은 SU3 파일에서 허용되지 않습니다. ph (prehash) 변형을 사용하세요.

새로운 최대 Destination 크기는 2599바이트(base 64로는 3468바이트)가 됩니다.

### 기타 사양

새로운 최대 Destination 크기는 2599(base 64에서는 3468)입니다.

크기 증가 (바이트):

- 메시지 1이 919바이트 미만이면, 현재 ratchet 프로토콜입니다.
- 메시지 1이 919바이트 이상이면, MLKEM512_X25519일 가능성이 높습니다.
  먼저 MLKEM512_X25519를 시도하고, 실패하면 현재 ratchet 프로토콜을 시도하세요.

## 오버헤드 분석

### 키 교환

속도:

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
[Cloudflare](https://blog.cloudflare.com/pq-2024/)에서 보고된 속도:

Java에서의 예비 테스트 결과:

| 유형 | 상대적 속도 |
|------|----------------|
| X25519 DH/keygen | 기준선 |
| MLKEM512 | 2.25배 빠름 |
| MLKEM768 | 1.5배 빠름 |
| MLKEM1024 | 1배 (동일) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% 느림 |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% 느림 |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% 느림 |
크기:

| 타입 | 상대적 DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | 기준선 | 기준선 | 기준선 |
| MLKEM512 | 29배 빠름 | 22배 빠름 | 17배 빠름 |
| MLKEM768 | 17배 빠름 | 14배 빠름 | 9배 빠름 |
| MLKEM1024 | 12배 빠름 | 10배 빠름 | 6배 빠름 |
### 서명

#### 크기

속도:

| 타입 | 공개키 | 서명 | 키+서명 | RIdent | Dest | RInfo | LS/Streaming/Datagram (각 메시지) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### 속도

Java에서의 예비 테스트 결과:

| 유형 | 상대적 서명 속도 | 검증 |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5배 느림 | 2배 빠름 |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
크기:

| 타입 | 상대적 서명 속도 | 검증 | 키 생성 |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | 기준선 | 기준선 | 기준선 |
| MLDSA44 | 4.6배 느림 | 1.7배 빠름 | 2.6배 빠름 |
| MLDSA65 | 8.1배 느림 | 동일 | 1.5배 빠름 |
| MLDSA87 | 11.1배 느림 | 1.5배 느림 | 동일 |
## 보안 분석

NIST 보안 카테고리는 [NIST 발표자료](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) 슬라이드 10에 요약되어 있습니다. 예비 기준: 하이브리드 프로토콜의 경우 최소 NIST 보안 카테고리는 2이고, PQ 전용의 경우 3이어야 합니다.

| 카테고리 | 보안 수준 |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### 핸드셰이크

NIST 보안 카테고리 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

이 제안서는 하이브리드 및 PQ 전용 서명 유형을 모두 정의합니다. MLDSA44 하이브리드가 MLDSA65 PQ 전용보다 바람직합니다. MLDSA65 및 MLDSA87의 키와 서명 크기는 적어도 처음에는 우리에게 너무 클 것 같습니다.

| 알고리즘 | 보안 카테고리 |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### 서명

NIST 보안 카테고리 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

3가지 암호화 방식과 9가지 서명 유형을 정의하고 구현할 예정이지만, 개발 과정에서 성능을 측정하고 구조 크기 증가로 인한 영향을 추가로 분석할 계획입니다. 또한 다른 프로젝트와 프로토콜의 개발 동향을 지속적으로 연구하고 모니터링할 것입니다.

| 알고리즘 | 보안 범주 |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## 유형 환경설정

개발 및 테스트 후에는 각 사용 사례에 대해 선호되는 유형이나 기본값을 정할 예정입니다. 선택 시에는 대역폭, CPU, 그리고 예상 보안 수준 간의 절충점을 고려해야 합니다. 모든 유형이 모든 사용 사례에 적합하거나 허용되는 것은 아닐 수 있습니다.

예비 설정은 다음과 같으며, 변경될 수 있습니다:

암호화: MLKEM768_X25519

Signatures: MLDSA44_EdDSA_SHA512_Ed25519

예비 제한 사항은 다음과 같으며, 변경될 수 있습니다:

서명: MLDSA87 및 하이브리드 변형은 아마도 너무 클 것이고; MLDSA65 및 하이브리드 변형은 너무 클 수 있음

Bouncycastle, BoringSSL, WolfSSL 라이브러리들이 현재 MLKEM과 MLDSA를 지원합니다. OpenSSL 지원은 2025년 4월 8일 3.5 릴리스에서 제공될 예정입니다 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## 구현 참고사항

### 라이브러리 지원

Java I2P에서 적용한 southernstorm.com Noise 라이브러리는 하이브리드 핸드셰이크에 대한 예비 지원을 포함하고 있었지만, 사용되지 않아 제거했습니다. [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)에 맞춰 다시 추가하고 업데이트해야 합니다.

[FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 섹션 3.4에 정의된 대로 "결정적" 변형이 아닌 "헤지드" 또는 무작위화된 서명 변형을 사용할 것입니다. 이는 같은 데이터에 대해서도 각 서명이 다르도록 보장하며, 사이드 채널 공격에 대한 추가적인 보호를 제공합니다. [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에서 "헤지드" 변형이 기본값이라고 명시하고 있지만, 다양한 라이브러리에서는 그렇지 않을 수도 있습니다. 구현자들은 서명에 "헤지드" 변형이 사용되도록 확인해야 합니다.

### 서명 변형

우리는 일반적인 서명 프로세스(Pure ML-DSA Signature Generation이라고 함)를 사용하며, 이는 메시지를 내부적으로 0x00 || len(ctx) || ctx || message로 인코딩합니다. 여기서 ctx는 0x00..0xFF 크기의 선택적 값입니다. 우리는 선택적 컨텍스트를 사용하지 않습니다. len(ctx) == 0입니다. 이 프로세스는 [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithm 2 step 10과 Algorithm 3 step 5에 정의되어 있습니다. 일부 공개된 테스트 벡터는 메시지가 인코딩되지 않는 모드 설정이 필요할 수 있습니다.

크기 증가는 NetDB 저장, 스트리밍 핸드셰이크 및 기타 메시지에 대해 훨씬 더 많은 tunnel 단편화를 야기할 것입니다. 성능 및 안정성 변화를 확인하세요.

### 신뢰성

router info와 leaseSet의 바이트 크기를 제한하는 모든 코드를 찾아서 확인하세요.

### 구조체 크기

RAM이나 디스크에 저장되는 최대 LS/RI를 검토하고 가능하면 줄여서 저장 공간 증가를 제한하세요. floodfill에 대한 최소 대역폭 요구사항을 높일까요?

### NetDB

메시지 1(새 세션 메시지)의 길이 확인을 기반으로 동일한 터널에서 여러 프로토콜을 자동 분류/감지할 수 있어야 합니다. MLKEM512_X25519를 예로 들면, 메시지 1 길이는 현재 ratchet 프로토콜보다 816바이트 더 크며, 최소 메시지 1 크기(DateTime 페이로드만 포함)는 919바이트입니다. 현재 ratchet을 사용하는 대부분의 메시지 1 크기는 816바이트 미만의 페이로드를 가지므로 비하이브리드 ratchet으로 분류할 수 있습니다. 큰 메시지는 아마도 드문 POST일 것입니다.

### 래칫

#### 공유 터널

따라서 권장하는 전략은 다음과 같습니다:

이를 통해 이전에 동일한 목적지에서 ElGamal과 ratchet을 지원했던 것처럼, 동일한 목적지에서 표준 ratchet과 hybrid ratchet을 효율적으로 지원할 수 있습니다. 따라서 동일한 목적지에 대해 듀얼 프로토콜을 지원할 수 없는 경우보다 훨씬 빠르게 MLKEM hybrid 프로토콜로 마이그레이션할 수 있으며, 기존 목적지에 MLKEM 지원을 추가할 수 있습니다.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

필수 지원 조합은 다음과 같습니다:

다음 조합들은 복잡할 수 있으며, 지원이 필수는 아니지만 구현에 따라 지원될 수 있습니다:

- 하나 이상의 MLKEM
- ElG + 하나 이상의 MLKEM
- X25519 + 하나 이상의 MLKEM
- ElG + X25519 + 하나 이상의 MLKEM

동일한 destination에서 여러 MLKEM 알고리즘(예: MLKEM512_X25519와 MLKEM_768_X25519)을 지원하려고 시도하지 않을 수 있습니다. 하나만 선택하세요. 하지만 이는 우리가 선호하는 MLKEM 변형을 선택하는 것에 달려 있으므로 HTTP client tunnel이 하나를 사용할 수 있습니다. 구현에 따라 달라집니다.

- Noise Hash 선택 - SHA256을 유지할 것인지 업그레이드할 것인지?
  SHA256은 향후 20-30년 동안은 안전하며, PQ(양자 컴퓨팅)의 위협을 받지 않을 것으로 예상됩니다.
  [NIST 발표자료](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)와 [NCCOE 발표자료](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)를 참조하세요.
  SHA256이 깨진다면 우리는 더 심각한 문제들(netDb)을 겪게 될 것입니다.
- NTCP2 별도 포트, 별도 router 주소
- SSU2 relay / peer test
- SSU2 버전 필드
- SSU2 router 주소 버전

동일한 destination에서 세 가지 알고리즘(예: X25519, MLKEM512_X25519, MLKEM769_X25519)을 지원하려고 시도할 수 있습니다. 분류 및 재시도 전략이 너무 복잡할 수 있습니다. 구성 및 구성 UI가 너무 복잡할 수 있습니다. 구현에 따라 다릅니다.

동일한 목적지에서 ElGamal과 hybrid 알고리즘을 모두 지원하려고 시도하지는 않을 것입니다. ElGamal은 구식이고, ElGamal + hybrid만 사용하는 것(X25519 없이)은 별로 의미가 없습니다. 또한 ElGamal과 Hybrid New Session Message는 모두 크기가 크므로, 분류 전략에서 종종 두 복호화를 모두 시도해야 하는데 이는 비효율적입니다. 구현에 따라 달라집니다.

클라이언트는 동일한 터널에서 X25519 및 하이브리드 프로토콜에 대해 같거나 다른 X25519 정적 키를 사용할 수 있으며, 이는 구현에 따라 달라집니다.

ECIES 사양에서는 New Session Message 페이로드에 garlic 메시지를 포함할 수 있으며, 이를 통해 초기 스트리밍 패킷(보통 HTTP GET)을 클라이언트의 leaseSet과 함께 0-RTT로 전달할 수 있습니다. 그러나 New Session Message 페이로드는 전방향 보안성을 제공하지 않습니다. 이 제안서는 ratchet의 향상된 전방향 보안성을 강조하고 있으므로, 구현체들은 첫 번째 Existing Session Message까지 스트리밍 페이로드 또는 전체 스트리밍 메시지의 포함을 연기할 수도 있고, 연기해야 할 수도 있습니다. 이는 0-RTT 전달을 포기하는 대신에 이루어질 것입니다. 전략은 트래픽 유형이나 tunnel 유형, 또는 예를 들어 GET 대 POST에 따라 달라질 수도 있습니다. 구현에 따라 결정됩니다.

#### 순방향 보안성

동일한 목적지에서 MLKEM, MLDSA 또는 둘 다 사용하면 위에서 설명한 바와 같이 New Session Message의 크기가 극적으로 증가합니다. 이는 여러 개의 1024바이트 tunnel 메시지로 분할되어야 하는 터널을 통한 New Session Message 전송의 신뢰성을 현저히 감소시킬 수 있습니다. 전송 성공률은 조각 수의 지수에 비례합니다. 구현체는 0-RTT 전송을 희생하더라도 메시지 크기를 제한하는 다양한 전략을 사용할 수 있습니다. 구현에 따라 달라집니다.

#### 새 세션 크기

세션 요청에서 임시 키의 MSB(key[31] & 0x80)를 설정하여 이것이 하이브리드 연결임을 나타냅니다. 이를 통해 동일한 포트에서 표준 NTCP와 하이브리드 NTCP를 모두 실행할 수 있습니다. 하나의 하이브리드 변형만 지원되며, router 주소에 광고됩니다. 예를 들어, v=2,3 또는 v=2,4 또는 v=2,5입니다.

### NTCP2

Alice로서, PQ 연결의 경우, 난독화 전에 X[31] |= 0x80을 설정합니다. 이는 X를 유효하지 않은 X25519 공개 키로 만듭니다. 난독화 후, AES-CBC가 이를 무작위화합니다. 난독화 후 X의 MSB는 무작위가 됩니다.

#### 난독화

Bob으로서, 난독화 해제 후 (X[31] & 0x80) != 0인지 테스트합니다. 만약 그렇다면, 이는 PQ 연결입니다.

NTCP2-PQ에 필요한 최소 router 버전은 미정입니다.

참고: 타입 코드는 내부 사용 전용입니다. Router는 타입 4로 유지되며, 지원은 router 주소에 표시됩니다.

크기:

### SSU2

우리는 긴 헤더의 버전 필드를 사용하여 MLKEM512의 경우 3으로, MLKEM768의 경우 4로 설정합니다. 주소에서 v=2,3,4면 충분할 것입니다.

참고: 타입 코드는 내부 사용 전용입니다. router는 타입 4를 유지하며, 지원 여부는 router 주소에 표시됩니다.

크기:

## Router 호환성

### 전송 이름

모든 경우에 NTCP2와 SSU2 전송 이름을 평소대로 사용하십시오.

### Router 암호화 유형

권장하지 않습니다. router 유형에 맞는 위에 나열된 새로운 전송만 사용하세요. 구형 router는 연결하거나, tunnel을 구축하거나, netDb 메시지를 보낼 수 없습니다. 기본적으로 활성화하기 전에 디버그하고 지원을 보장하려면 여러 릴리스 주기가 필요합니다. 아래 대안들보다 배포 기간이 1년 이상 연장될 수 있습니다.

#### Type 5/6/7 Router

권장됨. PQ가 X25519 정적 키나 N 핸드셰이크 프로토콜에 영향을 주지 않으므로, router를 타입 4로 유지하고 새로운 전송 방식만 광고할 수 있습니다. 기존 router들은 여전히 연결하고, tunnel을 구축하고, netDb 메시지를 보낼 수 있습니다.

#### Type 4 Router

MLKEM-768은 보안과 키 길이의 최적 균형을 제공하므로 Ratchet, NTCP2, SSU2에 권장됩니다.

#### 권장사항

구버전 router들은 RI를 검증하므로 연결하거나, 터널을 구축하거나, netDb 메시지를 전송할 수 없습니다. 기본적으로 활성화하기 전에 지원을 디버그하고 보장하려면 여러 릴리스 주기가 필요할 것입니다. enc. type 5/6/7 출시와 동일한 문제가 발생할 것이며, 위에 나열된 type 4 enc. type 출시 대안보다 출시가 1년 이상 연장될 수 있습니다.

### Router 서명 타입

#### Type 12-17 Router

대안 없음.

이들은 이전 타입 4 X25519 키를 가진 LS에 존재할 수 있습니다. 이전 router들은 알 수 없는 키들을 무시할 것입니다.

### LS 암호화 타입

#### 타입 5-7 LS 키

Destination은 여러 키 타입을 지원할 수 있지만, 각 키로 메시지 1의 시행착오 복호화를 수행해야만 합니다. 각 키에 대한 성공적인 복호화 횟수를 유지하고 가장 많이 사용된 키를 먼저 시도함으로써 오버헤드를 완화할 수 있습니다. Java I2P는 동일한 destination에서 ElGamal+X25519에 대해 이 전략을 사용합니다.

Router들은 leaseSet 서명을 검증하므로 타입 12-17 대상에 연결하거나 leaseSet을 받을 수 없습니다. 기본적으로 활성화하기 전에 디버깅하고 지원을 보장하는 데 여러 릴리스 주기가 필요할 것입니다.

### 목적지 서명 유형

#### Type 12-17 Dests

대안이 없습니다.

이들은 이전 타입 4 X25519 키를 가진 LS에 존재할 수 있습니다. 이전 router들은 알 수 없는 키들을 무시할 것입니다.

## 우선순위 및 배포

가장 중요한 데이터는 ratchet으로 암호화된 종단 간 트래픽입니다. tunnel 홉 사이의 외부 관찰자로서는 tunnel 암호화와 전송 암호화로 두 번 더 암호화되어 있습니다. OBEP와 IBGW 사이의 외부 관찰자로서는 전송 암호화로 한 번 더 암호화되어 있습니다. OBEP 또는 IBGW 참여자로서는 ratchet이 유일한 암호화입니다. 그러나 tunnel이 단방향이므로, ratchet 핸드셰이크에서 두 메시지를 모두 캡처하려면 동일한 router에 OBEP와 IBGW가 구축되지 않는 한 공모하는 router들이 필요합니다.

합리적인 기간(예: 몇 달) 내에 인증 키를 해독한 다음 거의 실시간으로 인증을 가장하거나 복호화하는 PQ 위협 모델은 훨씬 더 먼 미래의 일일까요? 그리고 그때가 바로 PQC static key로 마이그레이션하고 싶은 시점일 것입니다.

따라서 가장 초기의 PQ 위협 모델은 OBEP/IBGW가 나중에 복호화하기 위해 트래픽을 저장하는 것입니다. 우리는 먼저 하이브리드 래칫을 구현해야 합니다.

Ratchet이 최우선입니다. Transport가 그 다음이고, Signature가 가장 낮은 우선순위입니다.

서명 배포는 암호화 배포보다 1년 이상 늦어질 것입니다. 이는 하위 호환성이 불가능하기 때문입니다. 또한 업계에서 MLDSA 채택은 CA/Browser Forum과 인증 기관에 의해 표준화될 것입니다. CA는 먼저 현재 사용할 수 없는 하드웨어 보안 모듈(HSM) 지원이 필요합니다 [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). CA/Browser Forum이 복합 서명 지원 또는 요구 여부를 포함하여 구체적인 매개변수 선택에 대한 결정을 주도할 것으로 예상합니다 [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

X25519에서 했던 것처럼, 하나씩 차례로 시도해보는 방식으로 입증할 수 있어야 합니다.

X25519에서 했던 것처럼, 하나씩 차례대로 시도해보는 것만으로도 증명할 수 있을 것입니다.

| 마일스톤 | 목표 |
|-----------|--------|
| Ratchet 베타 | 2025년 말 |
| 최적 암호화 유형 선택 | 2026년 초 |
| NTCP2 베타 | 2026년 초 |
| SSU2 베타 | 2026년 중반 |
| Ratchet 프로덕션 | 2026년 중반 |
| Ratchet 기본값 | 2026년 말 |
| 서명 베타 | 2026년 말 |
| NTCP2 프로덕션 | 2026년 말 |
| SSU2 프로덕션 | 2027년 초 |
| 최적 서명 유형 선택 | 2027년 초 |
| NTCP2 기본값 | 2027년 초 |
| SSU2 기본값 | 2027년 중반 |
| 서명 프로덕션 | 2027년 중반 |
## 마이그레이션

따라서, 가장 초기의 PQ 위협 모델은 OBEP/IBGW가 나중에 복호화하기 위해 트래픽을 저장하는 것입니다. 우리는 먼저 하이브리드 래칫을 구현해야 합니다.

Ratchet이 최우선순위입니다. Transport가 그 다음이고, Signature가 가장 낮은 우선순위입니다.

## 문제점

SHA256은 향후 20~30년 동안 안전할 것으로 예상되며, 양자내성(PQ) 위협도 받지 않습니다. [NIST 발표 자료](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) 및 [NCCOE 발표 자료](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)를 참조하세요. SHA256이 깨진다면 네트워크 데이터베이스(netdb) 등 더 심각한 문제가 발생할 것입니다.

## 참고 자료

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
