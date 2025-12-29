---
title: "전송 계층"
description: "I2P의 전송 계층 이해 - NTCP2와 SSU2를 포함한 router 간 점대점 통신 방식"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. 개요

I2P의 **transport**(전송 방식)은 router 간 직접적인 점대점 통신을 위한 방법이다. 이러한 메커니즘은 router 인증을 검증하는 동시에 기밀성과 무결성을 보장한다.

각 전송 프로토콜은 인증, 흐름 제어, 확인 응답, 재전송 기능을 갖춘 연결 모델을 사용하여 동작합니다.

---

## 2. 현재 전송 프로토콜

I2P는 현재 두 가지 주요 전송 프로토콜을 지원합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 레거시 트랜스포트 (사용 중단됨)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. 전송 서비스

전송 하위 시스템은 다음과 같은 서비스를 제공합니다:

### 3.1 메시지 전달

- 신뢰할 수 있는 [I2NP](/docs/specs/i2np/) 메시지 전달 (전송 계층이 I2NP 메시징만을 전담함)
- 전달 순서 보장은 보편적으로 **보장되지 않습니다**
- 우선순위 기반 메시지 대기열

### 3.2 연결 관리

- 연결 수립 및 종료
- 임계값 강제 적용을 포함한 연결 한도 관리
- 피어별 상태 추적
- 자동 및 수동 피어 차단 목록 강제 적용

### 3.3 네트워크 구성

- 전송 방식별 다중 router 주소 (IPv4 및 IPv6 지원, v0.9.8부터)
- UPnP 방화벽 포트 개방
- NAT/방화벽 트래버설 지원
- 여러 방법을 통한 로컬 IP 감지

### 3.4 보안

- 점대점 통신을 위한 암호화
- 로컬 규칙에 따른 IP 주소 검증
- 시계 합의 결정(NTP(네트워크 시간 프로토콜) 백업)

### 3.5 대역폭 관리

- 인바운드 및 아웃바운드 대역폭 제한
- 나가는 메시지를 위한 최적 전송 방식 선택

---

## 4. 전송 주소

서브시스템은 router 접속 지점 목록을 관리합니다:

- 전송 방식 (NTCP2, SSU2)
- IP 주소
- 포트 번호
- 선택적 매개변수

전송 방식별로 여러 개의 주소를 사용할 수 있습니다.

### 4.1 일반적인 주소 구성

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. 전송 프로토콜 선택

시스템은 상위 계층 프로토콜과 무관하게 [I2NP messages](/docs/specs/i2np/)를 위한 트랜스포트를 선택합니다. 선택 과정은 각 트랜스포트가 입찰가를 제출하고 가장 낮은 값이 낙찰되는 **입찰 시스템**을 사용합니다.

### 5.1 입찰 결정 요인

- 전송 방식 선호 설정
- 기존 피어 연결
- 현재 연결 수와 임계 연결 수
- 최근 연결 시도 이력
- 메시지 크기 제한
- 피어 RouterInfo(라우터 정보)의 전송 기능
- 연결의 직접성(직접 연결 대 introducer(중개자) 의존)
- 피어가 광고한 전송 선호도

일반적으로 두 routers는 동시에 단일 transport(전송 프로토콜) 연결만 유지하지만, 동시에 다중 transport 연결도 가능하다.

---

## 6. NTCP2

**NTCP2** (새 전송 프로토콜 2)는 I2P용 최신 TCP 기반 전송 프로토콜로, 버전 0.9.36에서 도입되었다.

### 6.1 주요 기능

- **Noise Protocol Framework**(암호 프로토콜 프레임워크)를 기반으로 함 (Noise_XK pattern)
- 키 교환을 위해 **X25519**를 사용
- 인증된 암호화를 위해 **ChaCha20/Poly1305**를 사용
- 해싱을 위해 **BLAKE2s**를 사용
- DPI (Deep Packet Inspection, 심층 패킷 검사)에 저항하기 위한 프로토콜 난독화
- 트래픽 분석에 대한 저항성을 위한 선택적 패딩

### 6.2 연결 설정

1. **세션 요청** (Alice → Bob): 임시 X25519 키 + 암호화된 페이로드
2. **세션 생성** (Bob → Alice): 임시 키 + 암호화된 확인
3. **세션 확인** (Alice → Bob): RouterInfo(라우터 정보)와의 최종 핸드셰이크

이후의 모든 데이터는 핸드셰이크에서 파생된 세션 키로 암호화됩니다.

자세한 내용은 [NTCP2 사양](/docs/specs/ntcp2/)을 참조하세요.

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2, 보안 반신뢰성 UDP 2)은 I2P를 위한 최신 UDP 기반 전송 프로토콜로, 버전 0.9.56에서 도입되었습니다.

### 7.1 주요 기능

- **Noise Protocol Framework**(암호 통신용 핸드셰이크 프레임워크)에 기반함 (Noise_XK pattern)
- 키 교환을 위해 **X25519**를 사용
- 인증된 암호화를 위해 **ChaCha20/Poly1305**를 사용
- 선택적 확인응답(SACK)을 사용하는 부분적 신뢰성 전송
- 홀 펀칭(hole punching) 및 릴레이/인트로덕션(relay/introduction)을 통한 NAT 트래버설
- 연결 마이그레이션 지원
- 경로 MTU 발견

### 7.2 SSU (레거시) 대비 장점

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
자세한 내용은 [SSU2 명세서](/docs/specs/ssu2/)를 참조하세요.

---

## 8. NAT 트래버설

두 전송 프로토콜은 방화벽 뒤에 있는 routers가 네트워크에 참여할 수 있도록 NAT traversal(NAT 환경에서의 연결 성립 기술)을 지원합니다.

### 8.1 SSU2 소개

router가 인바운드 연결을 직접 수신할 수 없을 때:

1. Router는 자신의 RouterInfo에 **introducer**(NAT 우회를 위한 중개 노드) 주소를 게시한다
2. 연결하려는 피어가 introducer에게 소개 요청을 보낸다
3. Introducer가 방화벽 뒤에 있는 router에 연결 정보를 중계한다
4. 방화벽 뒤의 router가 아웃바운드 연결을 시작한다 (hole punch(홀 펀칭))
5. 직접 통신이 확립됨

### 8.2 NTCP2 및 방화벽

NTCP2는 인바운드 TCP 연결이 필요합니다. NAT 뒤에 있는 routers는 다음을 수행할 수 있습니다:

- UPnP를 사용해 포트를 자동으로 엽니다
- 수동으로 포트 포워딩을 구성합니다
- 수신 연결에는 SSU2(SSU의 2세대 버전으로, I2P에서 사용되는 UDP 기반 전송 프로토콜)를 사용하고, 발신 연결에는 NTCP2를 사용합니다

---

## 9. 프로토콜 난독화

두 가지 최신 전송 프로토콜 모두 난독화 기능을 포함합니다:

- **무작위 패딩**을 사용하는 핸드셰이크 메시지
- **암호화된 헤더**가 프로토콜 시그니처(식별 패턴)를 노출하지 않음
- **가변 길이 메시지**로 트래픽 분석에 대응
- **고정된 패턴 없음** 연결 설정 시

> **Note**: 전송 계층 난독화는 I2P의 tunnel 아키텍처가 제공하는 익명성을 보완하지만 대체하지는 않습니다.

---

## 10. 향후 개발

계획된 연구 및 개선 사항에는 다음이 포함됩니다:

- **Pluggable transports(플러그형 전송)** – Tor 호환 트래픽 난독화 플러그인
- **QUIC 기반 전송** – QUIC 프로토콜의 이점 검토
- **연결 제한 최적화** – 최적의 피어 연결 제한에 대한 연구
- **강화된 패딩 전략** – 트래픽 분석 저항성 향상

---

## 11. 참고 문헌

- [NTCP2 명세](/docs/specs/ntcp2/) – Noise 기반 TCP 전송
- [SSU2 명세](/docs/specs/ssu2/) – 보안 반신뢰성 UDP 2
- [I2NP 명세](/docs/specs/i2np/) – I2P 네트워크 프로토콜 메시지
- [공통 구조체](/docs/specs/common-structures/) – RouterInfo 및 주소 구조체
- [역사적 NTCP 논의](/docs/ntcp/) – 레거시 전송 개발 역사
- [레거시 SSU 문서](/docs/legacy/ssu/) – 원래의 SSU 명세(사용 중단됨)
