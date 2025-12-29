---
title: "저수준 암호학"
description: "I2P 전반에서 사용되는 대칭형, 비대칭형, 및 서명 프리미티브(기본 구성 요소)의 요약"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **상태:** 이 페이지는 레거시 "Low-level Cryptography Specification"(저수준 암호화 명세)을 요약합니다. 최신 I2P 릴리스(2.10.0, 2025년 10월)는 새로운 암호 프리미티브로의 마이그레이션을 완료했습니다. 구현 세부사항은 [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), 및 [Tunnel Creation (ECIES)](/docs/specs/implementation/)와 같은 전용 명세를 참고하십시오.

## 발전 스냅샷

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## 비대칭키 암호화

### X25519(타원곡선 디피-헬만(ECDH) 키 합의 방식)

- NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 및 X25519 기반 tunnel 생성에 사용됩니다.  
- Noise protocol framework(노이즈 프로토콜 프레임워크)를 통해 컴팩트한 키, 상수 시간 연산, 그리고 순방향 기밀성을 제공합니다.  
- 32바이트 키와 효율적인 키 교환으로 128비트 보안 강도를 제공합니다.

### ElGamal (레거시)

- 구형 routers와의 하위 호환성을 위해 유지됩니다.  
- 생성기 2를 사용하는 2048비트 Oakley Group 14 소수(RFC 3526) 위에서 동작합니다.  
- AES 세션 키와 IV(초기화 벡터)를 514바이트 길이의 암호문으로 암호화합니다.  
- 인증된 암호화와 전방향 보안이 없으며, 모든 최신 엔드포인트는 ECIES(타원곡선 통합 암호체계)로 이전했습니다.

## 대칭키 암호화

### ChaCha20/Poly1305 (스트림 암호 ChaCha20과 메시지 인증 코드 Poly1305를 결합한 AEAD 알고리즘)

- NTCP2, SSU2, ECIES 전반에서 사용되는 기본 인증 암호 프리미티브.  
- AES 하드웨어 지원 없이도 AEAD 보안과 높은 성능을 제공.  
- RFC 7539에 따라 구현됨 (256‑bit 키, 96‑bit 논스, 128‑bit 태그).

### AES‑256/CBC (레거시)

- 여전히 tunnel 계층 암호화에 사용되며, 그 블록 암호 구조가 I2P의 계층형 암호화 모델에 부합합니다.  
- PKCS#5 패딩과 홉별 IV(초기화 벡터) 변환을 사용합니다.  
- 장기 검토가 예정되어 있지만, 암호학적으로는 여전히 안전합니다.

## 서명

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## 해시와 키 파생

- **SHA‑256:** DHT(분산 해시 테이블) 키, HKDF(HMAC 기반 키 파생 함수), 그리고 레거시 서명에 사용됩니다.  
- **SHA‑512:** EdDSA/RedDSA와 Noise의 HKDF 파생 과정에서 사용됩니다.  
- **HKDF‑SHA256:** ECIES(타원 곡선 통합 암호화 체계), NTCP2, SSU2에서 세션 키를 파생합니다.  
- 매일 교체되는 SHA‑256 파생값은 netDb에서 RouterInfo와 LeaseSet의 저장 위치를 보호합니다.

## 전송 계층 요약

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
두 전송 프로토콜 모두 Noise_XK handshake pattern(Noise 프로토콜의 XK 방식 핸드셰이크)을 사용하여 링크 수준의 순방향 비밀성과 재생 공격 방지를 제공합니다.

## Tunnel 계층 암호화

- 각 홉별 계층형 암호화를 위해 AES‑256/CBC를 계속 사용한다.  
- 아웃바운드 게이트웨이는 반복적인 AES 복호화를 수행한다; 각 홉은 자신의 레이어 키와 IV(초기화 벡터) 키를 사용해 다시 암호화한다.  
- 이중 IV 암호화는 상관관계 및 확인 공격을 완화한다.  
- AEAD(부가데이터가 포함된 인증 암호)로의 전환은 검토 중이지만 현재로서는 계획되어 있지 않다.

## 양자내성 암호

- I2P 2.10.0에서는 **실험적 하이브리드 포스트‑양자 암호화**를 도입합니다.  
- 테스트를 위해 Hidden Service Manager에서 수동으로 활성화할 수 있습니다.  
- X25519와 양자내성 KEM(키 캡슐화 메커니즘)을 결합합니다(하이브리드 모드).  
- 기본값이 아니며 연구 및 성능 평가를 목적으로 합니다.

## 확장성 프레임워크

- 암호화 및 서명 *유형 식별자*는 여러 프리미티브를 병행 지원할 수 있게 합니다.  
- 현재 매핑은 다음과 같습니다:  
  - **암호화 유형:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **서명 유형:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- 이 프레임워크는 네트워크 분할 없이 포스트‑양자 방식 등을 포함한 향후 업그레이드를 가능하게 합니다.

## 암호학적 구성

- **전송 계층:** X25519 + ChaCha20/Poly1305 (Noise 프레임워크).  
- **Tunnel 계층:** 익명성을 위한 AES‑256/CBC 계층형 암호화.  
- **종단 간:** 기밀성과 전방향 보안을 위한 ECIES‑X25519‑AEAD‑Ratchet.  
- **데이터베이스 계층:** 인증을 위한 EdDSA/RedDSA 서명.

이들 계층은 결합되어 심층 방어를 제공한다: 한 계층이 침해되더라도 다른 계층들이 기밀성과 비연결성을 유지한다.

## 요약

I2P 2.10.0의 암호화 스택은 다음을 중심으로 합니다:

- **Curve25519 (X25519)** 키 교환용  
- **ChaCha20/Poly1305** 대칭 암호화용  
- **EdDSA / RedDSA** 서명용  
- **SHA‑256 / SHA‑512** 해싱 및 키 파생용  
- **실험적 양자내성 하이브리드 모드** 향후 호환성 확보용

레거시 ElGamal, AES‑CBC, DSA는 하위 호환성을 위해 유지되지만 더 이상 활성 전송이나 암호화 경로에서는 사용되지 않습니다.
