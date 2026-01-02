---
title: "소프트웨어 업데이트 명세서"
description: "I2P routers를 위한 서명 기반 보안 업데이트 메커니즘 및 피드 구조"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

router는 I2P 네트워크를 통해 배포되는 서명된 뉴스 피드를 주기적으로 조회하여 업데이트를 자동으로 확인합니다. 새 버전이 공지되면, router는 암호학적으로 서명된 업데이트 아카이브(`.su3`)를 다운로드하여 설치를 위해 준비합니다. 이 시스템은 공식 릴리스를 **인증되고 위변조에 강한**, 그리고 **다중 채널** 방식으로 배포되도록 보장합니다.

I2P 2.10.0 기준으로, 업데이트 시스템은 다음을 사용합니다: - **RSA-4096 / SHA-512** 서명 - **SU3 컨테이너 형식** (레거시 SUD/SU2를 대체) - **중복 미러:** I2P 네트워크 내부 HTTP, clearnet HTTPS(일반 인터넷), 및 BitTorrent

---

## 1. 뉴스 피드

Routers는 새 버전과 보안 권고를 확인하기 위해 몇 시간마다 서명된 Atom 피드를 폴링합니다.   이 피드는 서명되어 `.su3` 파일로 배포되며, 여기에는 다음이 포함될 수 있습니다:

- `<i2p:version>` — 새 버전 번호  
- `<i2p:minVersion>` — 지원되는 최소 router 버전  
- `<i2p:minJavaVersion>` — 최소 필요 Java 런타임  
- `<i2p:update>` — 여러 다운로드 미러(I2P, HTTPS, 토렌트)를 나열  
- `<i2p:revocations>` — 인증서 폐기 데이터  
- `<i2p:blocklist>` — 침해된 피어에 대한 네트워크 수준의 차단 목록

### 피드 배포

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers는 I2P 피드를 우선 사용하지만, 필요할 경우 클리어넷이나 토렌트 배포로 전환할 수 있습니다.

---

## 2. 파일 형식

### SU3 (현재 표준)

0.9.9에서 도입된 SU3는 레거시 SUD 및 SU2 형식을 대체했다. 각 파일에는 헤더, 페이로드, 그리고 후행 서명이 포함된다.

**헤더 구조** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**서명 검증 단계** 1. 헤더를 파싱하고 서명 알고리즘을 식별합니다.   2. 저장된 서명자 인증서를 사용하여 해시와 서명을 검증합니다.   3. 서명자 인증서가 폐지되지 않았음을 확인합니다.   4. 내장된 버전 문자열을 페이로드 메타데이터와 비교합니다.

Routers에는 신뢰된 서명자 인증서(현재 **zzz** 및 **str4d**)가 포함되어 있으며, 서명되지 않았거나 철회된 출처는 모두 거부합니다.

### SU2 (폐기됨)

- Pack200로 압축된 JAR에 `.su2` 확장자를 사용했음.  
- Java 14에서 Pack200이 사용 중단됨(JEP 367) 이후 제거됨.  
- I2P 0.9.48+에서 비활성화됨; 이제 ZIP 압축으로 완전히 대체됨.

### SUD (레거시)

- 초기 DSA-SHA1로 서명된 ZIP 형식 (0.9.9 이전).  
- 서명자 ID나 헤더가 없고, 무결성이 제한적임.  
- 취약한 암호기술과 버전 강제 적용 부재로 대체됨.

---

## 3. 업데이트 워크플로우

### 3.1 헤더 검증

router는 전체 파일을 다운로드하기 전에 버전 문자열을 확인하기 위해 **SU3 header**만 가져옵니다.   이는 오래된 미러나 구버전으로 인해 대역폭이 낭비되는 것을 방지합니다.

### 3.2 전체 다운로드

헤더를 검증한 후, router는 전체 `.su3` 파일을 다음에서 다운로드합니다: - 네트워크 내 eepsite 미러 (선호됨)   - HTTPS 클리어넷 미러 (대체)   - BitTorrent (선택 사항, 피어 보조형 배포)

다운로드는 재시도, 타임아웃 처리, 미러 자동 전환 기능이 있는 표준 I2PTunnel HTTP 클라이언트를 사용합니다.

### 3.3 서명 검증

다운로드된 각 파일은 다음을 거칩니다: - **서명 확인:** RSA-4096/SHA512 검증   - **버전 일치 확인:** 헤더와 페이로드의 버전 일치 여부 확인   - **다운그레이드 방지:** 업데이트가 설치된 버전보다 최신임을 보장

유효하지 않거나 일치하지 않는 파일은 즉시 폐기됩니다.

### 3.4 설치 스테이징

검증이 완료되면: 1. ZIP의 내용을 임시 디렉터리에 압축 해제   2. `deletelist.txt`에 나열된 파일 삭제   3. `lib/jbigi.jar`가 포함되어 있으면 네이티브 라이브러리 교체   4. 서명자 인증서를 `~/.i2p/certificates/`로 복사   5. 다음 재시작 시 적용되도록 업데이트를 `i2pupdate.zip`으로 이동

업데이트는 다음 시작 시 자동으로 설치되거나, 사용자가 “지금 업데이트 설치”를 수동으로 실행하면 설치됩니다.

---

## 4. 파일 관리

### deletelist.txt

새 콘텐츠를 압축 해제하기 전에 제거해야 하는 더 이상 사용되지 않는 파일의 일반 텍스트 목록.

**규칙:** - 한 줄당 하나의 경로(상대 경로만 허용) - `#`로 시작하는 줄은 무시됨 - `..` 및 절대 경로는 거부됨

### 네이티브 라이브러리

오래되었거나 일치하지 않는 네이티브 바이너리를 방지하기 위해: - `lib/jbigi.jar`가 존재하면, 오래된 `.so` 또는 `.dll` 파일이 삭제됩니다   - 플랫폼별 라이브러리가 새로 추출되도록 보장됩니다

---

## 5. 인증서 관리

Router는 업데이트 또는 뉴스 피드의 철회 공지를 통해 **새 서명자 인증서**를 받을 수 있습니다.

- 새로운 `.crt` 파일이 인증서 디렉터리로 복사됩니다.  
- 폐기된 인증서는 향후 검증 전에 삭제됩니다.  
- 사용자의 수동 개입 없이 키 회전을 지원합니다.

모든 업데이트는 **air-gapped signing systems(에어갭 서명 시스템)**을 사용하여 오프라인에서 서명됩니다.   개인 키는 빌드 서버에 절대 저장되지 않습니다.

---

## 6. 개발자 지침

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
향후 릴리스에서는 양자내성 서명 통합(제안 169 참조)과 재현 가능한 빌드를 검토할 예정입니다.

---

## 7. 보안 개요

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. 버전 관리

- Router: **2.10.0 (API 0.9.67)**  
- 시맨틱 버전 관리(`Major.Minor.Patch` 사용).  
- 최소 버전 강제 적용으로 안전하지 않은 업그레이드를 방지합니다.  
- 지원되는 Java: **Java 8–17**. 향후 2.11.0+부터는 Java 17+가 필요합니다.

---
