---
title: "SSU 전송 (사용 중단됨)"
description: "SSU2 도입 이전에 사용되던 기존 UDP 전송"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **사용 중단됨:** SSU (Secure Semi-Reliable UDP)는 [SSU2](/docs/specs/ssu2/)로 대체되었습니다. Java I2P는 2.4.0 릴리스 (API 0.9.61)에서 SSU를 제거했고, i2pd는 2.44.0 (API 0.9.56)에서 제거했습니다. 이 문서는 역사적 참고용으로만 보관됩니다.

## 주요 내용

- I2NP 메시지를 암호화되고 인증된 점대점 방식으로 전달하는 UDP 전송.
- 2048비트 Diffie–Hellman 핸드셰이크(ElGamal과 동일한 소수 사용)에 의존했다.
- 각 데이터그램에는 16바이트 HMAC-MD5(비표준 축약 변형)와 16바이트 IV가 포함되었고, 그 뒤에 AES-256-CBC로 암호화된 페이로드가 이어졌다.
- 재전송 공격 방지와 세션 상태는 암호화된 페이로드 내부에서 추적되었다.

## 메시지 헤더

```
[16-byte MAC][16-byte IV][encrypted payload]
```
사용된 MAC(메시지 인증 코드) 계산: `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))`에 32바이트 MAC 키를 사용했다. 페이로드 길이는 MAC 계산 내에서 빅엔디언 16비트로 추가되었다. 프로토콜 버전의 기본값은 `0`, netId의 기본값은 `2`(메인 네트워크)였다.

## 세션 및 MAC 키

DH 공유 비밀에서 파생됨:

1. 공유 값을 빅엔디언 바이트 배열로 변환합니다(최상위 비트가 설정된 경우 `0x00`을 앞에 붙입니다).
2. 세션 키: 처음 32바이트(더 짧으면 0으로 채웁니다).
3. MAC 키: 바이트 33–64; 부족하면 공유 값의 SHA-256 해시로 대체합니다.

## 상태

Routers는 더 이상 SSU 주소를 광고하지 않습니다. 클라이언트는 SSU2 또는 NTCP2 전송 프로토콜로 이전해야 합니다. 과거 구현은 이전 릴리스에서 확인할 수 있습니다:

- `router/transport/udp` 아래에 있는 2.4.0 이전 Java 소스 코드
- 2.44.0 이전의 i2pd 소스 코드

현재 UDP 전송 동작에 대해서는 [SSU2 specification](/docs/specs/ssu2/)을 참조하세요.
