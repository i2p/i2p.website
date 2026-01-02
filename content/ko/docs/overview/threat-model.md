---
title: "I2P 위협 모델"
description: "I2P 설계에서 고려된 공격 목록 및 적용된 완화 조치"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. "익명"의 의미

I2P는 *실용적인 익명성*을 제공하며, 투명성을 제공하는 것은 아닙니다. 익명성은 적대자가 당신이 비공개로 유지하고자 하는 정보—당신이 누구인지, 어디에 있는지, 누구와 대화하는지—를 알아내기 어려운 정도로 정의됩니다. 절대적인 익명성은 불가능합니다. 대신 I2P는 전역적 수동 및 능동 적대자에 대해 **충분한 익명성**을 목표로 합니다.

귀하의 익명성은 I2P를 어떻게 구성하는지, 피어와 구독을 어떻게 선택하는지, 그리고 어떤 애플리케이션을 노출하는지에 따라 달라집니다.

---

## 2. 암호화 및 전송 진화 (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**현재 암호화 스위트 (Noise XK):** - **X25519** 키 교환용   - **ChaCha20/Poly1305 AEAD** 암호화용   - **Ed25519 (EdDSA-SHA512)** 서명용   - **SHA-256** 해싱 및 HKDF용   - 선택적 **ML-KEM 하이브리드** 포스트 양자 테스트용

모든 ElGamal 및 AES-CBC 사용은 폐기되었습니다. Transport는 전적으로 NTCP2 (TCP) 및 SSU2 (UDP)를 사용하며, 둘 다 IPv4/IPv6, forward secrecy (전방향 비밀성), DPI obfuscation (심층 패킷 검사 난독화)을 지원합니다.

---

## 3. 네트워크 아키텍처 요약

- **자유 경로 mixnet:** 송신자와 수신자가 각자 자신의 tunnel을 정의합니다.  
- **중앙 권한 없음:** 라우팅과 이름 지정이 탈중앙화되어 있으며, 각 router는 로컬 신뢰를 유지합니다.  
- **단방향 tunnel:** 인바운드와 아웃바운드가 분리되어 있습니다 (10분 수명).  
- **탐색 tunnel:** 기본적으로 2홉; 클라이언트 tunnel은 2–3홉입니다.  
- **Floodfill router:** 약 55,000개 노드 중 약 1,700개(약 6%)가 분산된 NetDB를 유지합니다.  
- **NetDB 순환:** 키스페이스는 UTC 자정에 매일 순환됩니다.  
- **Sub-DB 격리:** 2.4.0 버전부터 각 클라이언트와 router는 연결을 방지하기 위해 별도의 데이터베이스를 사용합니다.

---

## 4. 공격 범주 및 현재 방어 메커니즘

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. 현대적인 네트워크 데이터베이스 (NetDB)

**핵심 사실 (여전히 정확함):** - 수정된 Kademlia DHT가 RouterInfo와 LeaseSet을 저장합니다. - SHA-256 키 해싱; 10초 타임아웃으로 가장 가까운 2개의 floodfill에 병렬 쿼리를 수행합니다. - LeaseSet 수명 ≈ 10분 (LeaseSet2) 또는 18시간 (MetaLeaseSet).

**새로운 타입 (0.9.38 이후):** - **LeaseSet2 (타입 3)** – 다중 암호화 타입, 타임스탬프 적용.   - **EncryptedLeaseSet2 (타입 5)** – 비공개 서비스를 위한 블라인드 destination (DH 또는 PSK 인증).   - **MetaLeaseSet (타입 7)** – 멀티호밍 및 연장된 만료 시간.

**주요 보안 업그레이드 – Sub-DB 격리 (2.4.0):** - router↔client 연결 방지.   - 각 client와 router가 별도의 netDb 세그먼트 사용.   - 검증 및 감사 완료 (2.5.0).

---

## 6. 숨김 모드 및 제한된 경로

- **Hidden Mode:** 구현됨 (Freedom House 점수에 따라 엄격한 국가에서 자동 적용).  
    Router들은 RouterInfo를 공개하지 않으며 트래픽을 라우팅하지 않습니다.  
- **Restricted Routes:** 부분 구현됨 (기본 신뢰 전용 tunnel).  
    포괄적인 신뢰 피어 라우팅은 계획 중입니다 (3.0+).

절충안: 더 나은 프라이버시 ↔ 네트워크 용량 기여도 감소.

---

## 7. DoS 및 Floodfill 공격

**과거:** 2013년 UCSB 연구에서 Eclipse 및 Floodfill 장악이 가능함을 보여줌.   **현대적 방어 메커니즘:** - 일일 키스페이스 순환.   - Floodfill 제한 ≈ 500개, /16당 하나.   - 무작위 저장소 검증 지연.   - 최신 router 우선 (2.6.0).   - 자동 등록 수정 (2.9.0).   - 혼잡 인식 라우팅 및 lease 제한 (2.4.0+).

Floodfill 공격은 이론적으로는 가능하지만 실제로는 더 어렵습니다.

---

## 8. 트래픽 분석 및 검열

I2P 트래픽은 식별하기 어렵습니다: 고정 포트 없음, 평문 핸드셰이크 없음, 무작위 패딩 사용. NTCP2와 SSU2 패킷은 일반적인 프로토콜을 모방하고 ChaCha20 헤더 난독화를 사용합니다. 패딩 전략은 기본적이며(무작위 크기), 더미 트래픽은 구현되지 않았습니다(비용 문제). Tor exit 노드로부터의 연결은 2.6.0부터 차단됩니다(리소스 보호를 위해).

---

## 9. 지속적인 제한사항 (인지됨)

- 저지연 애플리케이션에 대한 타이밍 상관관계는 여전히 근본적인 위험 요소입니다.
- 알려진 공개 목적지에 대한 교차 공격은 여전히 강력합니다.
- Sybil 공격에 대한 완전한 방어 수단이 부족합니다 (HashCash가 강제되지 않음).
- 일정 속도 트래픽과 중요한 지연은 아직 구현되지 않았습니다 (3.0 계획).

이러한 제한 사항에 대한 투명성은 의도적입니다 — 사용자가 익명성을 과대평가하는 것을 방지합니다.

---

## 10. 네트워크 통계 (2025)

- 전 세계적으로 약 55,000개의 활성 router (2013년 7,000개에서 증가 ↑)  
- 약 1,700개의 floodfill router (~6%)  
- 기본적으로 95%가 tunnel 라우팅에 참여  
- 대역폭 등급: K (<12 KB/s) → X (>2 MB/s)  
- 최소 floodfill 속도: 128 KB/s  
- Router 콘솔 Java 8+ (필수), 다음 사이클에 Java 17+ 계획

---

## 11. 개발 및 중앙 리소스

- 공식 사이트: [geti2p.net](/)
- 문서: [Documentation](/docs/)  
- Debian 저장소: <https://deb.i2pgit.org> ( 2023년 10월에 deb.i2p2.de를 대체 )  
- 소스 코드: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + GitHub 미러  
- 모든 릴리스는 서명된 SU3 컨테이너 (RSA-4096, zzz/str4d 키)  
- 활성 메일링 리스트 없음; 커뮤니티는 <https://i2pforum.net> 및 IRC2P를 통해 운영  
- 업데이트 주기: 6–8주 안정 릴리스

---

## 12. 0.8.x 이후 보안 개선 사항 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. 알려진 미해결 또는 계획된 작업

- 포괄적인 제한된 경로 (신뢰할 수 있는 피어 라우팅) → 3.0 계획됨.  
- 타이밍 저항을 위한 비자명한 지연/배치 → 3.0 계획됨.  
- 고급 패딩 및 더미 트래픽 → 미구현.  
- HashCash 신원 확인 → 인프라는 존재하지만 비활성화됨.  
- R5N DHT 대체 → 제안만 존재.

---

## 14. 주요 참고 자료

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [I2P 공식 문서](/docs/)

---

## 15. 결론

I2P의 핵심 익명성 모델은 20년 동안 유지되어 왔습니다: 전역 고유성을 희생하여 지역적 신뢰와 보안을 확보하는 것입니다. ElGamal에서 X25519로, NTCP에서 NTCP2로, 그리고 수동 reseed에서 Sub-DB 격리까지, 프로젝트는 심층 방어와 투명성이라는 철학을 유지하면서 진화해 왔습니다.

많은 공격이 이론적으로는 모든 저지연 mixnet에 대해 여전히 가능하지만, I2P의 지속적인 강화는 이러한 공격을 점점 더 비실용적으로 만들고 있습니다. 네트워크는 그 어느 때보다 크고, 빠르며, 안전합니다. 하지만 여전히 자신의 한계에 대해 솔직합니다.
