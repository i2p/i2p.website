---
title: "포스트 양자 암호 프로토콜"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Open"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## 개요

적합한 포스트 양자(PQ) 암호화에 대한 연구와 경쟁은 10년 동안 진행되어 왔지만, 선택지가 최근까지 명확해지지 않았습니다.

2022년 [FORUM](http://zzz.i2p/topics/3294)에 PQ 암호의 영향을 조사하기 시작했습니다.

TLS 표준은 지난 2년 동안 하이브리드 암호화 지원을 추가했으며, 이는 크롬과 파이어폭스의 지원으로 인해 인터넷에서 암호화된 트래픽에서 상당한 비중을 차지하게 되었습니다 [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST는 최근 포스트 양자 암호화에 대한 권장 알고리즘을 최종화 및 발표했습니다 [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). 여러 일반적인 암호화 라이브러리는 이제 NIST 표준을 지원하거나 가까운 미래에 지원을 발표할 것입니다.

[CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) 및 [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)는 즉시 마이그레이션을 시작할 것을 권장합니다. 2022년 NSA PQ FAQ [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)도 참조하십시오. I2P는 보안과 암호화의 선두주자여야 합니다. 이제 권장 알고리즘을 구현할 때입니다. 우리의 유연한 암호 유형 및 서명 유형 시스템을 사용하여 하이브리드 암호화 및 PQ와 하이브리드 서명을 위한 유형을 추가할 것입니다.


## 목표

- PQ 저항 알고리즘 선택
- 적합한 경우 I2P 프로토콜에 PQ 전용 및 하이브리드 알고리즘 추가
- 여러 변형 정의
- 구현, 테스트, 분석 및 연구 후 최적의 변형 선택
- 점진적 지원 추가 및 하위 호환성 유지


## 비목표

- 단방향(Noise N) 암호화 프로토콜 변경 안 함
- SHA256에서 이동하지 않음, PQ에 의해 단기적으로 위협받지 않음
- 이 시점에서 최종 선호 변형 선택 안 함


## 위협 모델

- OBEP 또는 IBGW의 라우터가 협조하여 나중에 해독을 위해 마늘 메시지 저장(전방 시크릿)
- 네트워크 관찰자가 나중에 해독을 위해 전송 메시지를 저장(전방 시크릿)
- 네트워크 참가자가 RI, LS, 스트리밍, 데이터그램 또는 기타 구조를 위한 서명을 위조함


## 영향을 받는 프로토콜

개발 순서에 대략 맞춰 다음 프로토콜을 수정할 것입니다. 전체 롤아웃은 아마도 2025년 말부터 2027년 중반까지 진행될 것입니다. 자세한 내용은 우선순위 및 롤아웃 섹션을 참조하십시오.


| 프로토콜 / 기능                   상태 |  |
| ------------------------------ | --- |
| 하이브리드 MLKEM Ratchet 및 LS         승 | 2026-0 |
| 하이브리드 MLKEM NTCP2 | 일부 세부 |
| 하이브리드 MLKEM SSU2 | 일부 세부 |
| MLDSA SigTypes 12-14 |  |
| MLDSA Dests |  |
| 하이브리드 SigTypes 15-17 | 초기 단계 |
| 하이브리드 Dests |  |




## 설계

NIST FIPS 203 및 204 표준 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)을 지원할 것이며,
이 표준은 CRYSTALS-Kyber 및 CRYSTALS-Dilithium(버전 3.1, 3 및 그 이전 버전) 기반이지만 호환되지 않습니다.



### 키 교환

하이브리드 키 교환을 다음 프로토콜에서 지원할 것입니다:

| 프로토콜 | 형  지원 PQ 전 | 하이브리드 지원? |  |
| ---- | ---------- | --------- | --- |
| NTCP2 | XK | 아니오 | 예 |
| SSU2 | XK | 아니오 | 예 |
| Ratchet | IK | 아니오 | 예 |
| TBM | N | 아니오 | 아니오 |
| NetDB | N | 아니오 | 아니오 |


PQ KEM은 차동 키만 제공하며, Noise XK 및 IK와 같은 정적 키 핸드셰이크를 직접 지원하지 않습니다.

Noise N은 양방향 키 교환을 사용하지 않으므로 하이브리드 암호화에 적합하지 않습니다.

따라서 NTCP2, SSU2, 및 Ratchet에 대해서만 하이브리드 암호화를 지원할 것입니다.
[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의된 대로 세 가지 ML-KEM 변형을 정의하여 총 3개의 새로운 암호화 유형을 제공합니다.
하이브리드 유형은 X25519와의 조합으로만 정의됩니다.

새로운 암호화 유형은 다음과 같습니다:

| 유형 |  |
| --- | --- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


오버헤드는 상당할 것입니다. 현재 메시지 1 및 2의 일반적인 크기(XK 및 IK)는 약 100바이트입니다(추가 페이로드 전).
이는 알고리즘에 따라 8배에서 15배로 증가합니다.


### 서명

다음 구조에서 PQ 및 하이브리드 서명을 지원할 것입니다:

| 유형 | PQ 전용?   하이브리드 | ? |
| --- | -------------- | --- |
| RouterInfo | 예 |  |
| LeaseSet | 예 |  |
| Streaming SYN/SYNACK/Close | 예 |  |
| Repliable Datagrams | 예 |  |
| Datagram2 (prop. 163) | 예 |  |
| I2CP create session msg | 예 |  |
| SU3 files | 예 |  |
| X.509 certificates | 예 |  |
| Java keystores | 예 |  |


따라서 PQ 전용 및 하이브리드 서명 모두를 지원할 것입니다.
[FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의된 대로 세 가지 ML-DSA 변형을 정의하고,
Ed25519와 함께 세 가지 하이브리드 변형을 정의하며,
SU3 파일 전용의 prehash가 있는 세 가지 PQ 전용 변형을 정의하여
총 9개의 새로운 서명 유형을 제공합니다.
하이브리드 유형은 Ed25519와의 조합으로만 정의됩니다.
표준 ML-DSA를 사용할 것이며, SU3 파일을 위한 pre-hash 변형(HashML-DSA)은 사용하지 않습니다.

"hedged" 또는 랜덤 서명 변형을 사용할 것이며,
"determinstic" 변형은 사용하지 않습 as [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) 섹션 3.4에 정의되어 있습니다.
이것은 동일한 데이터에 대해서도 각 서명이 다르게 하여
사이드 채널 공격에 대한 추가 보호를 제공합니다.
알고리즘 선택에 대한 추가 세부 정보는 아래 구현 노트 섹션을 참조하십시오
(인코딩 및 컨텍스트 포함).

새로운 서명 유형은 다음과 같습니다:

| 유형 |  |
| --- | --- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


X.509 인증서 및 기타 DER 인코딩은 [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/)에 정의된 합성 구조 및 OID를 사용할 것입니다.

오버헤드는 상당할 것입니다. 일반적인 Ed25519 목적지 및 라우터 ID 크기는 391바이트입니다.
이들은 알고리즘에 따라 3.5배에서 6.8배로 증가합니다.
Ed25519 서명 크기는 64바이트입니다.
이들은 알고리즘에 따라 38배에서 76배로 증가합니다.
일반적으로 서명된 RouterInfo, LeaseSet, 재응답 데이터그램 및 서명된 스트리밍 메시지는 약 1KB입니다.
이들은 알고리즘에 따라 3배에서 8배로 증가합니다.

새로운 목적지 및 라우터 ID 유형은 패딩을 포함하지 않으므로 압축할 수 없습니다.
전송 중 압축된 목적지 및 라우터 ID의 크기는 알고리즘에 따라 12배에서 38배로 증가합니다.



### 합법적 조합

목적지의 경우, 새로운 서명 유형은 리즈셋의 모든 암호화 유형으로 지원됩니다.
키 인증서에서 암호화 유형을 NONE(255)으로 설정합니다.

RouterIdentifiers의 경우 ElGamal 암호 유형은 사용이 중단됩니다.
새로운 서명 유형은 X25519(유형 4) 암호화 만 지원합니다.
새로운 암호화 유형은 RouterAddresses에 표시됩니다.
키 인증서의 암호화 유형은 계속해서 유형 4가 됩니다.



### 필요한 새로운 암호

- ML-KEM(이전 CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA(이전 CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128(이전 Keccak-256) [FIPS202]_ SHAKE128에만 사용
- SHA3-256(이전 Keccak-512) [FIPS202]_
- SHAKE128 및 SHAKE256(SHA3-128 및 SHA3-256의 XOF 확장) [FIPS202]_

SHA3-256, SHAKE128 및 SHAKE256의 테스트 벡터는 [NIST-VECTORS]_에 있습니다.

Java Bouncycastle 라이브러리는 위의 모든 것을 지원합니다.
C++ 라이브러리 지원은 OpenSSL 3.5 [OPENSSL]_에 있습니다.


### 대안

[FIPS205]_ (Sphincs+)는 ML-DSA보다 훨씬 느리고 크기 때문에 지원하지 않을 것입니다. 향후의 FIPS206 (Falcon)은 아직 표준화되지 않았기 때문에 지원하지 않을 것입니다. NTRU 또는 NIST에 의해 표준화되지 않은 기타 PQ 후보도 지원하지 않을 것입니다.


Rosenpass
`````````

Wireguard (IK) 를 순수 PQ 암호로 변환하는 몇 가지 연구가 있습니다 [PQ-WIREGUARD]_.
그러나 해당 논문에는 몇 가지 열린 질문이 있습니다.
나중에 이 접근 방법은 PQ Wireguard를 위한 Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_로 구현되었습니다.

Rosenpass는 preshared Classic McEliece 460896 정적 키(각 500 KB)와 Kyber-512(본질적으로 MLKEM-512) 일시적인 키를 사용합니다.
Classic McEliece의 암호 텍스트가 188바이트에 불과하고, Kyber-512 공개 키와 암호 텍스트가 적절하기 때문에
두 핸드셰이크 메시지는 표준 UDP MTU에 맞습니다.
PQ KK 핸드셰이크에서 얻은 공유 키(osk)는 표준 Wireguard IK 핸드셰이크의 입력 preshared 키(psk)로 사용됩니다.
결국, 두 가지 완전한 핸드셰이크가 있으며, 하나는 순수 PQ이고 다른 하나는 순수 X25519입니다.

우리는 XK 및 IK 핸드셰이크를 다음 이유로 교체하지 않을 것입니다:

- 우리는 KK를 사용할 수 없습니다, Bob은 Alice의 정적 키가 없습니다
- 500KB 정적 키는 너무 큽니다
- 우리는 추가 왕복이 필요하지 않습니다

백서에는 많은 유용한 정보가 있으며, 우리는 아이디어와 영감을 얻기 위해 검토할 것입니다. TODO.



## 명세

### 공통 구조

공통 구조 문서 [COMMON](https://geti2p.net/spec/common-structures)의 섹션 및 테이블을 다음과 같이 업데이트합니다:


공개 키
````````````````

새로운 공개 키 유형은 다음과 같습니다:

| 유형 | 키 길이         이후 | 사용법 |  |
| --- | --------------- | --- | --- |
| MLKEM512_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM768_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM1024_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM512 | 800 | 0.9.xx | 제안서 1 |
| MLKEM768 | 1184 | 0.9.xx | 제안서 1 |
| MLKEM1024 | 1568 | 0.9.xx | 제안서 1 |
| MLKEM512_CT | 768 | 0.9.xx | 제안서 1 |
| MLKEM768_CT | 1088 | 0.9.xx | 제안서 1 |
| MLKEM1024_CT | 1568 | 0.9.xx | 제안서 1 |
| NONE | 0 | 0.9.xx | 제안서 1 |


하이브리드 공개 키는 X25519 키입니다.
KEM 공개 키는 Alice에서 Bob으로 전송되는 일시적인 PQ 키입니다.
인코딩 및 바이트 순서는 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의되어 있습니다.

MLKEM*_CT 키는 실제로 공개 키가 아니며, Noise 핸드셰이크에서 Bob에서 Alice로 보내는 "암호 텍스트"입니다.
완성도를 위해 여기 목록화했습니다.



개인 키
````````````````

새로운 개인 키 유형은 다음과 같습니다:

| 유형 | 키 길이         이후 | 사용법 |  |
| --- | --------------- | --- | --- |
| MLKEM512_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM768_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM1024_X25519 | 32 | 0.9.xx | 제안서 1 |
| MLKEM512 | 1632 | 0.9.xx | 제안서 1 |
| MLKEM768 | 2400 | 0.9.xx | 제안서 1 |
| MLKEM1024 | 3168 | 0.9.xx | 제안서 1 |


하이브리드 개인 키는 X25519 키입니다.
KEM 개인 키는 Alice만을 위한 것입니다.
KEM 인코딩 및 바이트 순서는 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의되어 있습니다.





서명 공개 키
````````````````

새로운 서명 공개 키 유형은 다음과 같습니다:

| 유형 | (바이트)   이후 | 법 |  |
| --- | ---------- | --- | --- |
| MLDSA44 | 1312 | 0.9.xx | 제안서 1 |
| MLDSA65 | 1952 | 0.9.xx | 제안서 1 |
| MLDSA87 | 2592 | 0.9.xx | 제안서 1 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | 제안서 1 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | 제안서 1 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | 제안서 1 |
| MLDSA44ph | 1344 | 0.9.xx | SU3 파 |
| MLDSA65ph | 1984 | 0.9.xx | SU3 파 |
| MLDSA87ph | 2624 | 0.9.xx | SU3 파 |


하이브리드 서명 공개 키는 [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/)에서 정의된 대로 Ed25519 키와 PQ 키가 결합된 것입니다.
인코딩 및 바이트 순서는 [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의되어 있습니다.


서명 개인 키
`````````````````

새로운 서명 개인 키 유형은 다음과 같습니다:

| 유형 | (바이트)   이후 | 법 |  |
| --- | ---------- | --- | --- |
| MLDSA44 | 2560 | 0.9.xx | 제안서 1 |
| MLDSA65 | 4032 | 0.9.xx | 제안서 1 |
| MLDSA87 | 4896 | 0.9.xx | 제안서 1 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | 제안서 1 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | 제안서 1 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | 제안서 1 |
| MLDSA44ph | 2592 | 0.9.xx | SU3 파 |
| MLDSA65ph | 4064 | 0.9.xx | SU3 파 |
| MLDSA87ph | 4928 | 0.9.xx | SU3 파 |


하이브리드 서명 개인 키는 [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/)에서 정의된 대로 Ed25519 키와 PQ 키가 결합된 것입니다.
인코딩 및 바이트 순서는 [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의되어 있습니다.


서명
``````````

새로운 서명 유형은 다음과 같습니다:

| 유형 | (바이트)   이후 | 법 |  |
| --- | ---------- | --- | --- |
| MLDSA44 | 2420 | 0.9.xx | 제안서 1 |
| MLDSA65 | 3309 | 0.9.xx | 제안서 1 |
| MLDSA87 | 4627 | 0.9.xx | 제안서 1 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | 제안서 1 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | 제안서 1 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | 제안서 1 |
| MLDSA44ph | 2484 | 0.9.xx | SU3 파 |
| MLDSA65ph | 3373 | 0.9.xx | SU3 파 |
| MLDSA87ph | 4691 | 0.9.xx | SU3 파 |


하이브리드 서명은 [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/)에 정의된 대로 Ed25519 서명과 PQ 서명을 결합한 것입니다.
하이브리드 서명은 두 서명을 확인하고 둘 중 하나가 실패하면 실패로 처리됩니다.
인코딩 및 바이트 순서는 [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)에 정의되어 있습니다.



키 인증서
````````````````

새로운 서명 공개 키 유형은 다음과 같습니다:

| 유형 | 코드      총 | 키 길이         이후   사용법 |  |  |
| --- | --------- | --------------------- | --- | --- |
| MLDSA44 | 12 | 1312 | 0.9.xx | 제안서 1 |
| MLDSA65 | 13 | 1952 | 0.9.xx | 제안서 1 |
| MLDSA87 | 14 | 2592 | 0.9.xx | 제안서 1 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | 제안서 1 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | 제안서 1 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | 제안서 1 |




새로운 암호 공개 키 유형은 다음과 같습니다:

| 유형 | 코드      총 | 키 길이         이후   사용법 |  |  |
| --- | --------- | --------------------- | --- | --- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | 제안서 1 |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | 제안서 1 |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | 제안서 1 |
| NONE | 255 | 0 | 0.9.xx | 제안서 1 |



하이브리드 키 유형은 결코 키 인증서에 포함되지 않으며; 오직 리즈셋에만 포함됩니다.

하이브리드 또는 PQ 서명 유형의 경우, 암호화 유형에 NONE(유형 255)을 사용하고, crypto key가 없으며,
전체 384바이트 메인 섹션은 서명 키에 사용됩니다.


목적지 크기
``````````````````

다음은 새로운 목적지 유형의 길이입니다.
모든 것은 암호화 유형이 NONE(유형 255)이며, 암호화 키 길이는 0으로 처리됩니다.
전체 384바이트 섹션이 서명 공개 키의 첫 번째 부분에 사용됩니다.
참고: ECDSA_SHA512_P521 및 RSA 서명 유형의 경우 사용되지 않는 256바이트 ElGamal 키를 목적지에 유지한 규격과 다릅니다.

패딩 없음.
총 길이는 7 + 총 키 길이입니다.
키 인증서 길이는 4 + 초과 키 길이입니다.

예제 1319바이트 목적지 바이트 스트림을 MLDSA44에 대해:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]



| 유형 | 코드      총 | 키 길이         메인    초과 | 총 목적지 | 이 |  |
| --- | --------- | --------------------- | ----- | --- | --- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |




RouterIdent 크기
``````````````````

다음은 새로운 목적지 유형의 길이입니다.
모든 것은 X25519(유형 4)로서 암호화 유형입니다.
X28819 공개 키 뒤의 전체 352바이트 섹션은 서명 공개 키의 첫 번째 부분에 사용됩니다.
패딩 없음.
총 길이는 39 + 총 키 길이입니다.
키 인증서 길이는 4 + 초과 키 길이입니다.

예제 1351바이트 라우터 ID 바이트 스트림을 MLDSA44에 대해:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]



| 유형 | 코드      총 | 키 길이         메인    초과 | 총 Rou | rIdent | 이 |
| --- | --------- | --------------------- | ----- | ------ | --- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |




### 핸드셰이크 패턴

핸드셰이크는 [Noise]_ 핸드셰이크 패턴을 사용합니다.

다음 문자 매핑이 사용됩니다:

- e = 일회용 일시적 키
- s = 정적 키
- p = 메시지 페이로드
- e1 = 하나의 일시적인 PQ 키, Alice에서 Bob으로 전송
- ekem1 = KEM 암호 텍스트, Bob에서 Alice로 전송

하이브리드 전방 시크릿(hfs)에 대한 XK 및 IK 수정은
[Noise-Hybrid]_ 섹션 5에 지정되어 있습니다:

```dataspec

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

  e1 및 ekem1은 암호화됩니다. 아래의 패턴 정의를 참조하십시오.
  참고: e1 및 ekem1은 크기가 다릅니다(X25519와 다름)

```

e1 패턴은 다음과 같이 정의됩니다, [Noise-Hybrid]_ 섹션 4에 지정됨:

```dataspec

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


ekem1 패턴은 다음과 같이 정의됩니다, [Noise-Hybrid]_ 섹션 4에 지정됨:

```dataspec

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

문제들
``````

- 핸드셰이크 해시 함수를 변경해야 할까요? [Choosing-Hash]_ 참조하십시오.
  SHA256은 PQ에 의해 위협받지 않아도 됩니다, 그러나 해시 함수를 업그레이드하려 한다면,
  지금이 다른 것들을 변경하는 동안이 적기입니다.
  현재 IETF SSH 제안서 [SSH-HYBRID]_는 MLKEM768을 SHA256과 함께 사용하고,
  MLKEM1024를 SHA384와 함께 사용하는 것입니다. 그 제안서에는
  보안 고려사항에 대한 토론이 포함되어 있습니다.
- 0-RTT ratchet 데이터를 보내는 것을 그만두어야 할까요(LS 제외)?
- 0-RTT 데이터를 보내지 않는다면 ratchet을 IK에서 XK로 전환해야 할까요?


개요
````````

이 섹션은 IK 및 XK 프로토콜에 적용됩니다.

하이브리드 핸드셰이크는 [Noise-Hybrid]_에 정의되어 있습니다.
Alice에서 Bob으로의 첫 번째 메시지는 e1, 캡슐화 키를 메시지 페이로드 전에 포함합니다.
이는 추가 정적 키로 처리되며, EncryptAndHash()을 호출합니다(Alice가).
그러나 Bob은 캡슐화 키를 구조적으로 무시합니다.
그 후, 메시지 페이로드를 평소대로 처리합니다.

Bob에서 Alice로의 두 번째 메시지는 ekem1, 암호 텍스트를 메시지 페이로드 전에 포함합니다.
추가 정적 키로 처리되며, EncryptAndHash()을 호출합니다(Bob이).
또한 캡슐화 키를 사용하여 kem_shared_key를 계산하고 MixKey(kem_shared_key)를 호출합니다.
그 후, 메시지 페이로드를 평소대로 처리합니다.


정의된 ML-KEM 연산
```````````````````

[FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)에 정의된 대로
암호 학적 building blocks에 해당하는 다음 함수를 정의합니다.

(encap_key, decap_key) = PQ_KEYGEN()
    Alice는 캡슐화 및 디캡슐화 키를 생성합니다
    캡슐화 키는 메시지 1에서 전송됩니다.
    encap_key 및 decap_key 크기는 ML-KEM 변형에 기반합니다.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob은 메시지 1에서 받은 암호 텍스트를 사용하여
    암호 텍스트 및 공유 키를 계산합니다.
    암호 텍스트는 메시지 2에서 전송됩니다.
    암호 텍스트 크기는 ML-KEM 변형에 기반합니다.
    kem_shared_key는 항상 32바이트입니다.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice는 메시지 2에서 받은 암호 텍스트를 사용하여
    공유 키를 계산합니다.
    kem_shared_key는 항상 32바이트입니다.

encap_key와 암호 텍스트는 Noise 핸드셰이크 메시지 1 및 2
내에서 ChaCha/Poly 블록 안에 암호화됩니다.
그들은 핸드셰이크 과정의 일부로 해독될 것입니다.

kem_shared_key는 MixHash()을 사용하여 체인 키에 혼합됩니다.
자세한 내용은 아래를 참조하십시오.


Alice를 위한 메시지 1의 KDF
`````````````````````````

XK: 'es' 메시지 패턴 이후, 페이로드 전에 추가:

또는

IK: 'es' 메시지 패턴 이후, 's' 메시지 패턴 전에 추가:

```text
이것은 "e1" 메시지 패턴:
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


  "e1" 메시지 패턴의 끝.

  참고: 다음 섹션(XK의 경우 페이로드 또는 IK의 경우 정적 키)의 경우,
  keydata와 체인 키는 동일하게 유지되고,
  n은 이제 1이 됩니다(비하이브리드의 경우 0 대신).

```


Bob을 위한 메시지 1의 KDF
`````````````````````````

XK: 'es' 메시지 패턴 이후, 페이로드 전에 추가:

또는

IK: 'es' 메시지 패턴 이후, 's' 메시지 패턴 전에 추가:

```text
이것은 "e1" 메시지 패턴:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  "e1" 메시지 패턴의 끝.

  참고: 다음 섹션(XK의 경우 페이로드 또는 IK의 경우 정적 키)의 경우,
  keydata와 체인 키는 동일하게 유지되고,
  n은 이제 1이 됩니다(비하이브리드의 경우 0 대신).

```


Bob을 위한 메시지 2의 KDF
`````````````````````````

XK: 'ee' 메시지 패턴 이후, 페이로드 전에 추가:

또는

IK: 'ee' 메시지 패턴 이후, 'se' 메시지 패턴 전에 추가:

```text
이것은 "ekem1" 메시지 패턴:

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

  "ekem1" 메시지 패턴의 끝.

```


Alice를 위한 메시지 2의 KDF
`````````````````````````

'ee' 메시지 패턴 이후(IK의 경우 'ss' 메시지 패턴 전에):

```text
이것은 "ekem1" 메시지 패턴:

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

  "ekem1" 메시지 패턴의 끝.

```


메시지 3을 위한 KDF (XK만 해당)
```````````````````````````
변경되지 않음


분할()에 대한 KDF
```````````````````
변경되지 않음



### Ratchet

ECIES-Ratchet 명세 [ECIES](https://geti2p.net/spec/ecies)를 다음과 같이 업데이트하십시오:


Noise 식별자
`````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"



1b) 새로운 세션 형식(바인딩 포함)
`````````````````````````````````````

변경 사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 정적 키를 포함했고, 두 번째 섹션에 페이로드를 포함했습니다.
ML-KEM으로 인해 세 섹션이 있습니다.
첫 번째 섹션에는 암호화된 PQ 공개 키가 들어 있습니다.
두 번째 섹션에는 정적 키가 들어 있습니다.
세 번째 섹션에는 페이로드가 들어 있습니다.


암호화된 형식:

```dataspec
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

```dataspec
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

| 유형 | 코드  X 길이 | 메시지 1 | 이  메시지 1 | 화 길이  메시지 1 복 | 길이  PQ 키 길이 | l 길이 |  |
| --- | -------- | ----- | -------- | ------------- | ----------- | ---- | --- |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


페이로드는 DateTime 블록을 포함해야하므로, 최소 페이로드 크기는 7입니다. 최소 메시지 1 크기는 이에 따라 계산될 수 있습니다.



1g) 새로운 세션 응답 형식
````````````````````````````

변경 사항: 현재 ratchet은 첫 번째 ChaCha 섹션에 빈 페이로드를 가지고 있으며, 두 번째 섹션에 페이로드를 가지고 있습니다.
ML-KEM으로 인해 세 섹션이 있습니다.
첫 번째 섹션에는 암호화된 PQ 암호 텍스트가 들어 있습니다.
두 번째 섹션에는 빈 페이로드가 들어 있습니다.
세 번째 섹션에는 페이로드가 들어 있습니다.


암호화된 형식:

```dataspec
+----+----+----+----+----+----+----+----+
  |       세션 태그   8 바이트           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        일시적 공개 키                +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 암호화된 ML-KEM 암호 텍스트  |
  +      (아래 표에서 길이 참조)          +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 메시지 인증 코드 (MAC)     |
  +  (MAC) 암호 텍스트 섹션               +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 메시지 인증 코드 (MAC)     |
  +  (MAC) 키 섹션 (데이터 없음)         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            페이로드 섹션             +
  |       ChaCha20 암호화된 데이터       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 메시지 인증 코드 (MAC)     |
  +         (MAC) 페이로드 섹션           +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+


```

복호화된 형식:

```dataspec
페이로드 부분 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM 암호 텍스트              +
  |                                       |
  +      (아래 표에서 길이 참조)          +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  페이로드 부분 2:

  빈 페이로드

  페이로드 부분 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            페이로드 섹션             +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

크기:

| 유형 | 코드  Y 길이 | 시지 2 | 메시지 2 암 | 길이 메시지 2 복호화 | 이  PQ CT 길이 | t 길이 |  |
| --- | -------- | ---- | ------- | ------------ | ----------- | ---- | --- |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


참고: 메시지 2는 일반적으로 0이 아닌 페이로드를 가집니다.
ratchet 명세서 [ECIES](https://geti2p.net/spec/ecies)에서는 이를 요구하지 않으므로 페이로드의 최소 크기는 0입니다.
최소 메시지 2 크기는 이에 따라 계산될 수 있습니다.



### NTCP2

NTCP2 명세를 다음과 같이 업데이트하십시오 [NTCP2](https://geti2p.net/spec/ntcp2) :


Noise 식별자
`````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


1) SessionRequest
``````````````````

변경 사항: 현재 NTCP2는 ChaCha 섹션에 옵션만 포함합니다.
ML-KEM으로, ChaCha 섹션은 암호화된 PQ 공개 키도 포함할 것입니다.


원시 콘텐츠:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        RH_B로 난독 처리               +
  |       AES-CBC-256 암호화된 X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly 프레임 (MLKEM)           |
  +      (아래 표에서 길이 참조)          +
  |   메시지 1 KDF로 정의된 k             |
  +   n = 0                               +
  |   연관된 데이터를 위한 KDF 참조       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly 프레임 (옵션)            |
  +         32 bytes                      +
  |   메시지 1 KDF로 정의된 k             |
  +   n = 0                               +
  |   연관된 데이터를 위한 KDF 참조       |
  +----+----+----+----+----+----+----+----+
  |     암호화되지 않은 인증 패딩        |
  ~         (선택 사항)                  ~
  |     옵션 블록에서 정의된 길이         |
  +----+----+----+----+----+----+----+----+

  이전과 동일하지만 두 번째 ChaChaPoly 프레임 추가

```

암호화되지 않은 데이터(Poly1305 인증 태그는 표시되지 않음):

```dataspec
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
  +      (아래 표에서 길이 참조)          +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               옵션                    |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     암호화되지 않은 인증 패딩        |
  +         (선택 사항)                  +
  |     옵션 블록에서 정의된 길이         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+



```

크기:

| 유형 | 코드  X 길이 | 시지 1 | 메시지 1 암 | 길이 메시지 1 복호화 | 이  PQ 키 길이  o | 길이 |  |
| --- | -------- | ---- | ------- | ------------ | ------------- | --- | --- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


참고: 유형 코드는 내부용으로만 사용됩니다. 라우터는 계속해서 유형 4로 남으며, 지원은 라우터 주소에서 표시됩니다.


2) SessionCreated
``````````````````

변경 사항: 현재 NTCP2는 ChaCha 섹션에 옵션만 포함합니다.
ML-KEM으로, ChaCha 섹션은 암호화된 PQ 공개 키도 포함할 것입니다.


원시 콘텐츠:

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        RH_B로 난독 처리               +
  |       AES-CBC-256 암호화된 Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly 프레임 (MLKEM)            |
  +   암호화되고 인증된 데이터            +
  -      (아래 표에서 길이 참조)          -
  +   메시지 2 KDF로 정의된 k             +
  |   n = 0; 연관된 데이터를 위한       +
  +   KDF 참조                            +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly 프레임 (옵션)             |
  +   암호화되고 인증된 데이터            +
  -           32 bytes                    -
  +   메시지 2 KDF로 정의된 k             +
  |   n = 0; 연관된 데이터를 위한       +
  +   KDF 참조                            +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     암호화되지 않은 인증 패딩        |
  +         (선택 사항)                  +
  |     옵션 블록에서 정의된 길이         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  이전과 동일하지만 두 번째 ChaChaPoly 프레임 추가

```

암호화되지 않은 데이터(Poly1305 인증 태그는 표시되지 않음):

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM 암호 텍스트          |
  +      (아래 표에서 길이 참조)          +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               옵션                    |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     암호화되지 않은 인증 패딩        |
  +         (선택 사항)                  +
  |     옵션 블록에서 정의된 길이         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

크기:

| 유형 | 코드  Y 길이 | 시지 2 | 메시지 2 암 | 길이 메시지 2 복호화 | 이  PQ CT 길이 | t 길이 |  |
| --- | -------- | ---- | ------- | ------------ | ----------- | ---- | --- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


참고: 유형 코드는 내부용으로만 사용됩니다. 라우터는 계속해서 유형 4로 남으며, 지원은 라우터 주소에서 표시됩니다.



3) SessionConfirmed
```````````````````

변경되지 않음


데이터 페이즈를 위해 KDF
````````````````````````````````

변경되지 않음




### SSU2

SSU2 명세를 다음과 같이 업데이트하십시오 [SSU2](https://geti2p.net/spec/ssu2) :


Noise 식별자
`````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


긴 헤더
`````````````
긴 헤더는 32바이트입니다. 세션 생성 전에 사용됩니다, 토큰 요청, SessionRequest, SessionCreated 및 Retry에 사용됩니다.
세션 외부의 Peer Test 및 Hole Punch 메시지에도 사용됩니다.

TODO: 버전 필드를 내부적으로 사용하여 3을 MLKEM512, 4를 MLKEM768로 사용할 수 있습니다.
이를 유형 0 및 1에만 하거나 6가지 유형 모두에 할 수 있습니까?


헤더 암호화 전:

```dataspec

+----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 바이트, 부호 없는 빅 엔디안 정수

  Packet Number :: 4 바이트, 부호 없는 빅 엔디안 정수

  type :: 메시지 유형 = 0, 1, 7, 9, 10, 또는 11

  ver :: 프로토콜 버전, 2
         TODO: 버전 필드를 내부적으로 사용하여 3을 MLKEM512, 4를 MLKEM768로 사용할 수 있습니다.

  id :: 1 바이트, 네트워크 ID (현재 2, 테스트 네트워크 제외)

  flag :: 1 바이트, 사용되지 않음, 미래 호환성을 위해 0으로 설정

  Source Connection ID :: 8 바이트, 부호 없는 빅 엔디안 정수

  Token :: 8 바이트, 부호 없는 빅 엔디안 정수

```


짧은 헤더
`````````````
변경되지 않음


SessionRequest (유형 0)
```````````````````````

변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다.
ML-KEM으로, ChaCha 섹션은 암호화된 PQ 공개 키도 포함할 것입니다.


원시 콘텐츠:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  Bob intro key로 암호화됨            +
  |    헤더 암호화 KDF 참조              |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  Bob intro key n=0으로 암호화됨      +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 암호화됨            +
  |       Bob intro key n=0으로           |
  +              (32 bytes)               +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 암호화된 데이터 (MLKEM)   +
  +          (길이 다양)                 +
  |  Session Request를 위한 KDF로 정의된 k +
  +  n = 0                                +
  |  연관된 데이터를 위한 KDF 참조       +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 암호화된 데이터 (페이로드) +
  +          (길이 다양)                 +
  |  Session Request를 위한 KDF로 정의된 k +
  +  n = 0                                +
  |  연관된 데이터를 위한 KDF 참조       +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 바이트)      +
  +----+----+----+----+----+----+----+----+


```

암호화되지 않은 데이터(Poly1305 인증 태그는 표시되지 않음):

```dataspec
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
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (아래 표에서 길이 참조)          +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise 페이로드 (블록 데이터)     +
  +          (길이 다양)                 +
  |     허용 블록을 위한 아래 표 참조      +
  +----+----+----+----+----+----+----+----+


```

크기(IP 오버헤드를 포함하지 않음):

| 유형 | 코드  X 길이 | 메시지 1 | 이  메시지 1 | 화 길이 메시지 1 복호 | 길이  PQ 키 길이 | 길이 |  |
| --- | -------- | ----- | -------- | ------------- | ----------- | --- | --- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 |  |  |  |  |


참고: 유형 코드는 내부용으로만 사용됩니다. 라우터는 계속해서 유형 4로 남으며, 지원은 라우터 주소에서 표시됩니다.

MLKEM768_X25519에 대한 최소 MTU:
IPv4의 경우 약 1316, IPv6의 경우 약 1336.



SessionCreated (유형 1)
``````````````````````````
변경 사항: 현재 SSU2는 ChaCha 섹션에 블록 데이터만 포함합니다.
ML-KEM으로, ChaCha 섹션은 암호화된 PQ 공개 키도 포함할 것입니다.


원시 콘텐츠:

```dataspec
+----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  Bob intro key 및                     +
  | 유도 키로 암호화됨, 헤더 암호화 KDF 참조 +
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  유도 키 n=0으로 암호화됨             +
  +  헤더 암호화 KDF 참조                 +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 암호화됨           +
  |       유도 키 n=0으로                +
  +              (32 bytes)               +
  +  헤더 암호화 KDF 참조                 +
  +                                       +
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 데이터 (MLKEM)             |
  +   암호화되고 인증된 데이터           +
  +  크기 다양                            +
  +  메시지 2를 위한 KDF로 정의된 k       +
  +  n = 0; 연관된 데이터를 위한       +
  +  KDF 참조                              +
  +                                       +
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 데이터 (페이로드)         +
  +   암호화되고 인증된 데이터           +
  +  크기 다양                            +
  +  메시지 2를 위한 KDF로 정의된 k       +
  +  n = 0; 연관된 데이터를 위한       +
  +  KDF 참조                              +
  +                                       +
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)       +
  +----+----+----+----+----+----+----+----+


```

암호화되지 않은 데이터(Poly1305 인증 태그는 표시되지 않음):

```dataspec
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
  |                  Y                    +
  +              (32 bytes)               +
  +----------------+----------------------+
  |           ML-KEM 암호 텍스트            |
  +      (아래 표에서 길이 참조)            +
  +                                       +
  +---------------------------------------+
  |     Noise 페이로드 (블록 데이터)       |
  +          (길이 다양)                  +
  +      허용 블록을 위한 아래 표 참조     +
  +----+----+----+----+----+----+----+----+

```

크기(IP 오버헤드를 포함하지 않음):

| 유형 | 코드  Y 길이 | 시지 2 | 메시지 2 암 | 길이  메시지 2 복호 | 길이  PQ CT 길이 | l 길이 |  |
| --- | -------- | ---- | ------- | ------------ | ------------ | ---- | --- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | 너무 큼 |  |  |  |  |


참고: 유형 코드는 내부용으로만 사용됩니다. 라우
