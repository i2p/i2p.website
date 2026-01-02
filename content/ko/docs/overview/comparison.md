---
title: "I2P와 다른 프라이버시 네트워크 비교"
description: "I2P의 독특한 설계 장점을 강조하는 현대적인 기술 및 철학적 비교"
slug: "comparison"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 개요

오늘날 여러 주요 프라이버시 및 익명성 네트워크가 존재하며, 각각 다른 설계 목표와 위협 모델을 가지고 있습니다. Tor, Lokinet, GNUnet, Freenet 모두 프라이버시 보호 통신에 대한 가치 있는 접근 방식을 제공하지만, **I2P는 네트워크 내 hidden services와 P2P 애플리케이션에 완전히 최적화된 유일한 프로덕션 수준의 패킷 교환 네트워크로 두드러집니다.**

아래 표는 2025년 기준 이러한 네트워크들의 주요 아키텍처 및 운영상의 차이점을 요약합니다.

---

## 프라이버시 네트워크 비교 (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature / Network</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>I2P</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Tor</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Lokinet</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>Freenet (Hyphanet)</strong></th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);"><strong>GNUnet</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Primary Focus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services, P2P applications</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Clearnet anonymity via exits</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid VPN + hidden services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed storage & publishing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Research framework, F2F privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Architecture</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully distributed, packet-switched</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Centralized directory, circuit-switched</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched LLARP with blockchain coordination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DHT-based content routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DHT & F2F topology (R5N)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Routing Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels (inbound/outbound)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bidirectional circuits (3 hops)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched over staked nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key-based routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random walk + DHT hybrid</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Directory / Peer Discovery</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed Kademlia netDB with floodfills</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9 hardcoded directory authorities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blockchain + Oxen staking</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Heuristic routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed hash routing (R5N)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encryption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet (ChaCha20/Poly1305)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES + RSA/ECDH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Curve25519/ChaCha20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom symmetric encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519/Curve25519</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Participation Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All routers route traffic (democratic)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Small relay subset, majority are clients</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only staked nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-selectable trust mesh</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional F2F restriction</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic Handling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched, multi-path, load-balanced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Circuit-switched, fixed path per circuit</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switched, incentivized</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File chunk propagation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message batching and proof-of-work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Garlic Routing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (message bundling & tagging)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial (message batches)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ No</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Exit to Clearnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Limited (discouraged)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core design goal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (VPN-style exits)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not applicable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not applicable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Built-In Apps</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PSnark, I2PTunnel, SusiMail, I2PBote</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tor Browser, OnionShare</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lokinet GUI, SNApps</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Freenet UI</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">GNUnet CLI tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized for internal services, 1–3s RTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized for exits, ~200–500ms RTT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low latency, staked node QoS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High latency (minutes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental, inconsistent</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Anonymity Set Size</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">~55,000 active routers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Millions of daily users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">&lt;1,000 service nodes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Thousands (small core)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hundreds (research only)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Scalability</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Horizontal via floodfill rotation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Centralized bottleneck (directory)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Dependent on token economics</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Limited by routing heuristics</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Research-scale only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Funding Model</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Volunteer-driven nonprofit</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Major institutional grants</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto-incentivized (OXEN)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Volunteer community</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Academic research</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>License / Codebase</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (Java/C++/Go)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C++)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (Java)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source (C)</td>
    </tr>
  </tbody>
</table>
---

## I2P가 프라이버시 우선 설계에서 선두를 달리는 이유

### 1. **Packet Switching > Circuit Switching**

Tor의 회선 교환 모델은 트래픽을 고정된 3홉 경로에 바인딩합니다. 이는 브라우징에는 효율적이지만 장기 실행 내부 서비스에는 취약합니다. I2P의 **packet-switched tunnel**은 메시지를 여러 동시 경로로 전송하여 혼잡이나 장애를 자동으로 우회 라우팅함으로써 더 나은 가동 시간과 부하 분산을 제공합니다.

### 2. **Unidirectional Tunnels**

I2P는 인바운드와 아웃바운드 트래픽을 분리합니다. 이는 각 참여자가 통신 흐름의 **절반**만 볼 수 있음을 의미하며, 타이밍 상관관계 공격을 훨씬 어렵게 만듭니다. Tor, Lokinet 등은 요청과 응답이 동일한 경로를 공유하는 양방향 회로를 사용하는데, 더 단순하지만 추적이 더 쉽습니다.

### 3. **Fully Distributed netDB**

Tor의 9개 디렉토리 권한 서버는 네트워크 토폴로지를 정의합니다. I2P는 순환하는 floodfill router들이 유지하는 자가 조직화된 **Kademlia DHT**를 사용하여 중앙 제어 지점이나 조정 서버를 제거합니다.

### 1. **패킷 스위칭 > 회선 스위칭**

I2P는 **garlic routing**을 통해 onion routing을 확장하여 여러 암호화된 메시지를 하나의 컨테이너로 묶습니다. 이를 통해 메타데이터 유출과 대역폭 오버헤드를 줄이는 동시에 확인응답, 데이터 및 제어 메시지의 효율성을 향상시킵니다.

### 2. **단방향 터널**

모든 I2P router는 다른 사용자를 위해 라우팅을 수행합니다. 전담 릴레이 운영자나 특권 노드는 없으며, 대역폭과 신뢰성에 따라 각 노드가 얼마나 라우팅에 기여하는지 자동으로 결정됩니다. 이러한 민주적 접근 방식은 복원력을 구축하고 네트워크가 성장함에 따라 자연스럽게 확장됩니다.

### 3. **완전 분산형 netDB**

I2P의 12-홉 왕복 경로(인바운드 6 + 아웃바운드 6)는 Tor의 6-홉 히든 서비스 회로보다 더 강력한 연결 불가 추적성을 제공합니다. 양측 당사자 모두 내부에 있기 때문에, 연결은 출구 병목 현상을 완전히 회피하여 더 빠른 내부 호스팅과 네이티브 애플리케이션 통합(I2PSnark, I2PTunnel, I2PBote)을 제공합니다.

---

## Architectural Takeaways

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Design Principle</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">I2P Advantage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Decentralization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No trusted authorities; netDB managed by floodfill peers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic Separation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels prevent request/response correlation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptability</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Packet-switching allows per-message load balancing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Efficiency</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Garlic routing reduces metadata and increases throughput</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Inclusiveness</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All peers route traffic, strengthening anonymity set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Focus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Built specifically for hidden services and in-network communication</td>
    </tr>
  </tbody>
</table>
---

## When to Use Each Network

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Network</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous web browsing (clearnet access)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous hosting, P2P, or DApps</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Anonymous file publishing and storage</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Freenet (Hyphanet)</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">VPN-style private routing with staking</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Lokinet</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Academic experimentation and research</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>GNUnet</strong></td>
    </tr>
  </tbody>
</table>
---

## Summary

**I2P의 아키텍처는 독보적으로 프라이버시 우선**입니다—디렉토리 서버 없음, 블록체인 의존성 없음, 중앙화된 신뢰 없음. **단방향 tunnel, 패킷 교환 라우팅, garlic 메시지 번들링, 분산 피어 발견**의 조합은 오늘날 익명 호스팅 및 P2P 통신을 위한 가장 기술적으로 진보된 시스템입니다.

> I2P는 "Tor의 대안"이 아닙니다. 이는 프라이버시 네트워크 *외부*가 아닌 *내부*에서 일어나는 일을 위해 구축된 다른 종류의 네트워크입니다.
