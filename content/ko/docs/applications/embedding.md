---
title: "애플리케이션에 I2P 임베딩하기"
description: "앱에 I2P router를 책임감 있게 번들링하기 위한 실용적인 가이드 업데이트"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

애플리케이션에 I2P를 번들링하는 것은 사용자를 온보딩하는 강력한 방법입니다. 단, router가 책임감 있게 구성되어 있을 때만 가능합니다.

## 1. 라우터 팀과 협력

- 번들링하기 전에 **Java I2P**와 **i2pd** 유지관리자에게 연락하세요. 그들은 여러분의 기본 설정을 검토하고 호환성 문제를 강조할 수 있습니다.
- 스택에 맞는 router 구현을 선택하세요:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **기타 언어** → router를 번들링하고 [SAM v3](/docs/api/samv3/) 또는 [I2CP](/docs/specs/i2cp/)를 사용하여 통합
- router 바이너리와 의존성(Java 런타임, ICU 등)에 대한 재배포 조건을 확인하세요.

## 2. 권장 구성 기본값

"소비하는 것보다 더 많이 기여하기"를 목표로 하세요. 최신 기본 설정은 네트워크 건강성과 안정성을 우선시합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### 참여 터널은 여전히 필수적입니다

참여 터널을 비활성화하지 **마십시오**.

1. 중계하지 않는 router는 자체 성능이 저하됩니다.
2. 네트워크는 자발적인 용량 공유에 의존합니다.
3. 커버 트래픽(중계된 트래픽)은 익명성을 향상시킵니다.

**공식 최소 요구사항:** - 공유 대역폭: ≥ 12 KB/s   - Floodfill 자동 참여: ≥ 128 KB/s   - 권장사항: 인바운드 터널 2개 / 아웃바운드 터널 2개 (Java I2P 기본값)

## 3. 지속성 및 리시딩

지속적인 상태 디렉토리(`netDb/`, 프로필, 인증서)는 실행 사이에 보존되어야 합니다.

지속성 없이는, 사용자들이 매번 시작할 때마다 리시드를 트리거하게 되어 성능이 저하되고 리시드 서버의 부하가 증가합니다.

지속성이 불가능한 경우 (예: 컨테이너 또는 임시 설치):

1. 설치 프로그램에 **1,000–2,000개의 router info**를 포함시키세요.
2. 공개 서버의 부하를 줄이기 위해 하나 이상의 맞춤형 reseed 서버를 운영하세요.

구성 변수: - 기본 디렉토리: `i2p.dir.base` - 설정 디렉토리: `i2p.dir.config` - 리시딩을 위한 `certificates/` 포함.

## 4. 보안 및 노출

- router console (`127.0.0.1:7657`)을 로컬 전용으로 유지하세요.
- UI를 외부에 노출할 경우 HTTPS를 사용하세요.
- 필요하지 않은 경우 외부 SAM/I2CP를 비활성화하세요.
- 포함된 플러그인을 검토하고 앱이 지원하는 것만 제공하세요.
- 원격 콘솔 접근 시 항상 인증을 포함하세요.

**2.5.0 이후 도입된 보안 기능:** - 애플리케이션 간 NetDB 격리 (2.4.0+)   - DoS 완화 및 Tor 차단 목록 (2.5.1)   - NTCP2 프로빙 저항 (2.9.0)   - Floodfill 라우터 선택 개선 (2.6.0+)

## 5. 지원되는 API (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
모든 공식 문서는 `/docs/api/` 하위에 위치합니다 — 이전 `/spec/samv3/` 경로는 **존재하지 않습니다**.

## 6. 네트워킹 및 포트

일반적인 기본 포트: - 4444 – HTTP 프록시   - 4445 – HTTPS 프록시   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Router Console   - 7658 – 로컬 I2P 사이트   - 6668 – IRC 프록시   - 9000–31000 – 임의 router 포트 (UDP/TCP 인바운드)

라우터는 처음 실행할 때 임의의 인바운드 포트를 선택합니다. 포트 포워딩은 성능을 향상시키지만, UPnP가 자동으로 이를 처리할 수 있습니다.

## 7. 최근 변경사항 (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. 사용자 경험 및 테스트

- I2P가 무엇을 하는지, 왜 대역폭이 공유되는지 설명합니다.
- router 진단 정보(대역폭, tunnel, reseed 상태)를 제공합니다.
- Windows, macOS, Linux(저사양 RAM 환경 포함)에서 번들을 테스트합니다.
- **Java I2P**와 **i2pd** 피어 모두와의 상호 운용성을 검증합니다.
- 네트워크 연결 끊김 및 비정상 종료로부터의 복구를 테스트합니다.

## 9. 커뮤니티 리소스

- 포럼: [i2pforum.net](https://i2pforum.net) 또는 I2P 내부에서 `http://i2pforum.i2p`.  
- 코드: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (Irc2P 네트워크): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` 미확인; 존재하지 않을 수 있습니다.  
  - 채널이 호스팅되는 네트워크(Irc2P vs ilita.i2p)를 명확히 하세요.

책임감 있는 임베딩은 사용자 경험, 성능, 네트워크 기여 간의 균형을 맞추는 것을 의미합니다. 이러한 기본값을 사용하고, router 관리자들과 동기화를 유지하며, 출시 전에 실제 환경 부하에서 테스트하세요.
