---
title: "Garlic Routing"
description: "I2P에서 garlic routing 용어, 아키텍처 및 최신 구현 이해하기"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. 개요

**Garlic routing**은 I2P의 핵심 혁신 기술 중 하나로, 계층화된 암호화, 메시지 번들링, 그리고 단방향 터널을 결합합니다. 개념적으로 **onion routing**과 유사하지만, 여러 개의 암호화된 메시지("cloves")를 단일 봉투("garlic")로 묶는 방식으로 모델을 확장하여 효율성과 익명성을 향상시킵니다.

*garlic routing*이라는 용어는 [Roger Dingledine의 Free Haven 석사 논문](https://www.freehaven.net/papers.html)(2000년 6월, §8.1.1)에서 [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/)이 만들었습니다. I2P 개발자들은 2000년대 초반에 이 용어를 채택하여 메시지 번들링 강화와 단방향 전송 모델을 반영했으며, 이는 Tor의 회선 교환 방식 설계와 구별됩니다.

> **요약:** Garlic routing = 계층화된 암호화 + 메시지 번들링 + 단방향 터널을 통한 익명 전달.

---

## 2. "Garlic" 용어

역사적으로, *garlic*이라는 용어는 I2P 내에서 세 가지 다른 맥락으로 사용되어 왔습니다:

1. **계층화된 암호화** – tunnel 수준의 onion 방식 보호  
2. **여러 메시지 번들링** – "garlic message" 내부의 여러 "clove"들  
3. **종단간 암호화** – 이전에는 *ElGamal/AES+SessionTags*, 현재는 *ECIES‑X25519‑AEAD‑Ratchet*

아키텍처는 그대로 유지되지만, 암호화 방식은 완전히 현대화되었습니다.

---

## 3. 계층적 암호화

Garlic routing은 onion routing과 근본적인 원리를 공유합니다: 각 router는 암호화 계층 중 하나만 복호화하여 다음 hop만 알 뿐 전체 경로는 알지 못합니다.

그러나 I2P는 양방향 회로가 아닌 **단방향 터널**을 구현합니다:

- **Outbound tunnel**: 생성자로부터 메시지를 전송합니다
- **Inbound tunnel**: 생성자에게 메시지를 다시 전달합니다

완전한 왕복 통신(Alice ↔ Bob)은 네 개의 tunnel을 사용합니다: Alice의 outbound → Bob의 inbound, 그 다음 Bob의 outbound → Alice의 inbound. 이 설계는 양방향 회로에 비해 **상관관계 데이터 노출을 절반으로 줄입니다**.

터널 구현 세부사항은 [Tunnel Specification](/docs/specs/implementation)과 [Tunnel Creation (ECIES)](/docs/specs/implementation) 명세를 참조하세요.

---

## 4. 여러 메시지 묶기 ("Cloves")

Freedman의 원래 garlic routing은 하나의 메시지 내에 여러 개의 암호화된 "bulbs"를 묶는 것을 구상했습니다. I2P는 이를 **garlic message** 내부의 **cloves**로 구현합니다 — 각 clove는 자체적인 암호화된 전달 지침과 대상(router, destination 또는 tunnel)을 가집니다.

Garlic 번들링은 I2P가 다음을 수행할 수 있게 합니다:

- 확인 응답과 메타데이터를 데이터 메시지와 결합  
- 관찰 가능한 트래픽 패턴 감소  
- 추가 연결 없이 복잡한 메시지 구조 지원

![Garlic Message Cloves](/images/garliccloves.png)   *그림 1: 여러 개의 clove를 포함하는 Garlic Message, 각 clove는 자체 전달 지시사항을 가지고 있음.*

일반적인 정향(clove)에는 다음이 포함됩니다:

1. **전송 상태 메시지** — 전송 성공 또는 실패를 확인하는 승인 메시지.  
   기밀성을 유지하기 위해 자체 garlic 레이어로 감싸집니다.
2. **데이터베이스 저장 메시지** — 피어가 netDb를 다시 조회하지 않고 응답할 수 있도록 자동으로 번들된 LeaseSet.

Clove는 다음과 같은 경우에 번들로 묶입니다:

- 새로운 LeaseSet이 게시되어야 함
- 새로운 세션 태그가 전달됨
- 최근에 번들이 발생하지 않음 (기본값으로 약 1분)

Garlic 메시지는 여러 암호화된 구성 요소를 단일 패킷으로 효율적인 종단 간 전달을 달성합니다.

---

## 5. 암호화 발전

### 5.1 Historical Context

초기 문서(≤ v0.9.12)는 *ElGamal/AES+SessionTags* 암호화를 설명했습니다:   - **ElGamal 2048비트**로 래핑된 AES 세션 키   - 페이로드 암호화를 위한 **AES‑256/CBC**   - 메시지당 한 번 사용되는 32바이트 세션 태그

해당 암호화 시스템은 **더 이상 사용되지 않습니다**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

2019년부터 2023년 사이에 I2P는 ECIES‑X25519‑AEAD‑Ratchet으로 완전히 마이그레이션되었습니다. 최신 스택은 다음 구성 요소를 표준화합니다:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
ECIES 마이그레이션의 이점:

- 메시지별 래칫 키를 통한 **전방향 비밀성(Forward secrecy)**  
- ElGamal 대비 **축소된 페이로드 크기**  
- 암호 해독 기술 발전에 대한 **회복력**  
- 미래의 양자 내성 하이브리드와의 **호환성** (제안 169 참조)

추가 세부 사항: [ECIES 사양](/docs/specs/ecies) 및 [EncryptedLeaseSet 사양](/docs/specs/encryptedleaseset)을 참조하세요.

---

## 6. LeaseSets and Garlic Bundling

Garlic 엔벨로프는 목적지 도달 가능성을 게시하거나 업데이트하기 위해 leaseSet을 자주 포함합니다.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
모든 LeaseSet은 특수 라우터가 유지하는 *floodfill DHT*를 통해 배포됩니다. 게시는 메타데이터 상관관계를 줄이기 위해 검증되고, 타임스탬프가 찍히며, 속도 제한이 적용됩니다.

자세한 내용은 [Network Database 문서](/docs/specs/common-structures)를 참조하십시오.

---

## 7. Modern “Garlic” Applications within I2P

Garlic 암호화와 메시지 번들링은 I2P 프로토콜 스택 전반에 걸쳐 사용됩니다:

1. **터널 생성 및 사용** — 홉(hop)별 계층화된 암호화  
2. **종단 간 메시지 전달** — 복제 확인응답(cloned-acknowledgment)과 LeaseSet clove가 포함된 번들 garlic 메시지  
3. **Network Database 게시** — 프라이버시를 위해 garlic 봉투로 래핑된 LeaseSet  
4. **SSU2 및 NTCP2 전송** — Noise 프레임워크와 X25519/ChaCha20 기본 요소를 사용한 하위 계층 암호화

따라서 Garlic routing은 *암호화 계층화 방법*이자 *네트워크 메시징 모델*입니다.

---

## 6. LeaseSets과 Garlic Bundling

I2P의 문서 허브는 [여기에서 확인할 수 있으며](/docs/), 지속적으로 유지 관리됩니다. 관련된 최신 명세서는 다음과 같습니다:

- [ECIES 명세서](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel 생성 (ECIES)](/docs/specs/implementation) — 현대적인 tunnel 구축 프로토콜
- [I2NP 명세서](/docs/specs/i2np) — I2NP 메시지 형식
- [SSU2 명세서](/docs/specs/ssu2) — SSU2 UDP 전송
- [공통 구조](/docs/specs/common-structures) — netDb 및 floodfill 동작

학술적 검증: Hoang et al. (IMC 2018, USENIX FOCI 2019)과 Muntaka et al. (2025)은 I2P 설계의 아키텍처 안정성과 운영 복원력을 확인했습니다.

---

## 7. I2P 내의 현대적인 "Garlic" 애플리케이션

진행 중인 제안:

- **제안 169:** 하이브리드 양자 내성 암호화 (ML-KEM 512/768/1024 + X25519)  
- **제안 168:** Transport 대역폭 최적화  
- **데이터그램 및 스트리밍 업데이트:** 향상된 혼잡 제어

향후 적응 방식에는 Freedman이 원래 설명한 사용되지 않은 전달 옵션을 기반으로 추가적인 메시지 지연 전략이나 garlic 메시지 수준에서의 다중 터널 중복성이 포함될 수 있습니다.

---

## 8. 현재 문서 및 참고 자료

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
