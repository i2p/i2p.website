---
title: "SOCKS 프록시"
description: "I2P의 SOCKS tunnel을 안전하게 사용하기 (2.10.0 업데이트)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **주의:** SOCKS tunnel은 애플리케이션 페이로드를 정제하지 않고 그대로 전달합니다. 많은 프로토콜이 IP, 호스트명 또는 기타 식별자를 유출합니다. 익명성에 대해 검증된 소프트웨어에서만 SOCKS를 사용하십시오.

---

## 1. 개요

I2P는 **I2PTunnel 클라이언트**를 통해 아웃바운드 연결을 위한 **SOCKS 4, 4a, 5** 프록시를 지원합니다. 이를 통해 일반 애플리케이션이 I2P 목적지에 접근할 수 있지만 **클리어넷에는 접근할 수 없습니다**. **SOCKS outproxy가 없으며**, 모든 트래픽은 I2P 네트워크 내에 머물러 있습니다.

### 구현 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**지원되는 주소 유형:** - `.i2p` 호스트명 (주소록 항목) - Base32 해시 (`.b32.i2p`) - Base64 또는 일반 인터넷 지원 없음

---

## 2. 보안 위험 및 제한사항

### 애플리케이션 계층 유출

SOCKS는 애플리케이션 계층 아래에서 작동하므로 프로토콜을 정제할 수 없습니다. 많은 클라이언트(예: 브라우저, IRC, 이메일)는 IP 주소, 호스트명 또는 시스템 세부 정보를 노출하는 메타데이터를 포함합니다.

일반적인 정보 유출에는 다음이 포함됩니다: - 메일 헤더 또는 IRC CTCP 응답의 IP 주소   - 프로토콜 페이로드의 실명/사용자명   - OS 지문이 포함된 User-agent 문자열   - 외부 DNS 쿼리   - WebRTC 및 브라우저 원격 측정

**I2P는 이러한 유출을 방지할 수 없습니다**—이는 tunnel 계층 위에서 발생합니다. **감사된 클라이언트**에서만 익명성을 위해 설계된 SOCKS를 사용하세요.

### 공유 터널 신원

여러 애플리케이션이 하나의 SOCKS 터널을 공유하는 경우, 동일한 I2P destination identity를 공유하게 됩니다. 이는 서로 다른 서비스 간에 상관관계 분석이나 핑거프린팅을 가능하게 합니다.

**완화 방법:** 각 애플리케이션에 대해 **공유되지 않는 터널(non-shared tunnels)**을 사용하고 **영구 키(persistent keys)**를 활성화하여 재시작 시에도 일관된 암호화 식별자를 유지하세요.

### UDP 모드 스텁 처리됨

SOCKS5의 UDP 지원은 구현되어 있지 않습니다. 프로토콜은 UDP 기능을 알리지만, 호출은 무시됩니다. TCP 전용 클라이언트를 사용하십시오.

### 설계상 Outproxy 없음

Tor와 달리, I2P는 SOCKS 기반 clearnet outproxy를 제공하지 **않습니다**. 외부 IP에 접근하려는 시도는 실패하거나 신원을 노출시킬 수 있습니다. outproxy가 필요한 경우 HTTP 또는 HTTPS 프록시를 사용하세요.

---

## 3. 역사적 맥락

개발자들은 오랫동안 익명 사용을 위한 SOCKS 사용을 권장하지 않았습니다. 내부 개발자 토론 및 2004년 [Meeting 81](/ko/blog/2004/03/16/i2p-dev-meeting-march-16-2004/)과 [Meeting 82](/ko/blog/2004/03/23/i2p-dev-meeting-march-23-2004/)에서:

> "임의의 트래픽을 전달하는 것은 안전하지 않으며, 익명성 소프트웨어 개발자로서 우리는 최종 사용자의 안전을 최우선으로 고려해야 합니다."

SOCKS 지원은 호환성을 위해 포함되었지만 프로덕션 환경에서는 권장되지 않습니다. 거의 모든 인터넷 애플리케이션은 익명 라우팅에 적합하지 않은 민감한 메타데이터를 유출합니다.

---

## 4. 설정

### Java I2P

1. [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)를 엽니다
2. **"SOCKS 4/4a/5"** 유형의 새 클라이언트 tunnel을 생성합니다
3. 옵션을 구성합니다:
   - 로컬 포트 (사용 가능한 포트)
   - Shared client: 앱별로 별도의 신원을 사용하려면 *비활성화*
   - Persistent key: 키 상관관계를 줄이려면 *활성화*
4. tunnel을 시작합니다

### i2pd

i2pd는 기본적으로 `127.0.0.1:4447`에서 활성화된 SOCKS5 지원을 포함합니다. `i2pd.conf`의 `[SOCKSProxy]` 섹션에서 포트, 호스트 및 tunnel 매개변수를 조정할 수 있습니다.

---

## 5. 개발 일정

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
SOCKS 모듈 자체는 2013년 이후 주요 프로토콜 업데이트가 없었지만, 주변 tunnel 스택은 성능 및 암호화 개선을 받았습니다.

---

## 6. 권장 대안

**프로덕션**, **공개**, 또는 **보안 중요** 애플리케이션의 경우, SOCKS 대신 공식 I2P API 중 하나를 사용하세요:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
이러한 API는 적절한 목적지 격리, 암호화 신원 제어, 그리고 향상된 라우팅 성능을 제공합니다.

---

## 7. OnionCat / GarliCat

OnionCat은 GarliCat 모드(`fd60:db4d:ddb5::/48` IPv6 범위)를 통해 I2P를 지원합니다. 여전히 작동하지만 2019년 이후 개발이 제한적입니다.

**사용 시 주의사항:** - SusiDNS에서 수동으로 `.oc.b32.i2p` 설정 필요   - 고정 IPv6 할당 필요   - I2P 프로젝트에서 공식적으로 지원하지 않음

고급 VPN-over-I2P 설정에만 권장됩니다.

---

## 8. 모범 사례

SOCKS를 반드시 사용해야 하는 경우: 1. 애플리케이션별로 별도의 tunnel을 생성하세요. 2. 공유 클라이언트 모드를 비활성화하세요. 3. 영구 키를 활성화하세요. 4. SOCKS5 DNS 확인을 강제하세요. 5. 유출에 대한 프로토콜 동작을 감사하세요. 6. 클리어넷 연결을 피하세요. 7. 유출에 대한 네트워크 트래픽을 모니터링하세요.

---

## 9. 기술 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. 결론

I2P의 SOCKS 프록시는 기존 TCP 애플리케이션과의 기본적인 호환성을 제공하지만 **강력한 익명성 보장을 위해 설계되지 않았습니다**. 통제되고 감사된 테스트 환경에서만 사용해야 합니다.

> 실제 배포 환경에서는 **SAM v3** 또는 **Streaming API**로 마이그레이션하세요. 이러한 API는 애플리케이션 식별자를 격리하고, 최신 암호화 기술을 사용하며, 지속적인 개발이 이루어지고 있습니다.

---

### 추가 자료

- [공식 SOCKS 문서](/docs/api/socks/)  
- [SAM v3 사양](/docs/api/samv3/)  
- [Streaming Library 문서](/docs/specs/streaming/)  
- [I2PTunnel 참조](/docs/specs/implementation/)  
- [I2P 개발자 문서](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [커뮤니티 포럼](https://i2pforum.net)
