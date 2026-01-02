---
title: "Low-level Cryptography"
description: "Summary of the symmetric, asymmetric, and signature primitives used across I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Status:** This page condenses the legacy "Low-level Cryptography Specification". Modern I2P releases (2.10.0, October 2025) have completed the migration to new cryptographic primitives. Use specialized specs such as [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), and [Tunnel Creation (ECIES)](/docs/specs/implementation/) for implementation details.

## Evolution Snapshot

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

## Asymmetric Encryption

### X25519

- Used for NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2, and X25519-based tunnel creation.  
- Provides compact keys, constant-time operations, and forward secrecy via the Noise protocol framework.  
- Offers 128-bit security with 32-byte keys and efficient key exchange.

### ElGamal (Legacy)

- Retained for backward compatibility with older routers.  
- Operates over the 2048-bit Oakley Group 14 prime (RFC 3526) with generator 2.  
- Encrypts AES session keys plus IVs in 514-byte ciphertexts.  
- Lacks authenticated encryption and forward secrecy; all modern endpoints have migrated to ECIES.

## Symmetric Encryption

### ChaCha20/Poly1305

- Default authenticated encryption primitive across NTCP2, SSU2, and ECIES.  
- Provides AEAD security and high performance without AES hardware support.  
- Implemented per RFC 7539 (256‑bit key, 96‑bit nonce, 128‑bit tag).

### AES‑256/CBC (Legacy)

- Still used for tunnel layer encryption, where its block‑cipher structure fits I2P’s layered encryption model.  
- Uses PKCS#5 padding and per‑hop IV transformations.  
- Scheduled for long‑term review but remains cryptographically sound.

## Signatures

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

## Hash and Key Derivation

- **SHA‑256:** Used for DHT keys, HKDF, and legacy signatures.  
- **SHA‑512:** Used by EdDSA/RedDSA and in Noise HKDF derivations.  
- **HKDF‑SHA256:** Derives session keys in ECIES, NTCP2, and SSU2.  
- Daily‑rotating SHA‑256 derivations secure RouterInfo and LeaseSet storage locations in the netDb.

## Transport Layer Summary

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

Both transports provide link‑level forward secrecy and replay protection, using the Noise_XK handshake pattern.

## Tunnel Layer Encryption

- Continues to use AES‑256/CBC for per‑hop layered encryption.  
- Outbound gateways perform iterative AES decryption; each hop re‑encrypts using its layer key and IV key.  
- Double‑IV encryption mitigates correlation and confirmation attacks.  
- Migration to AEAD is under study but not currently planned.

## Post‑Quantum Cryptography

- I2P 2.10.0 introduces **experimental hybrid post‑quantum encryption**.  
- Enabled manually via Hidden Service Manager for testing.  
- Combines X25519 with a quantum‑resistant KEM (hybrid mode).  
- Not default; intended for research and performance evaluation.

## Extensibility Framework

- Encryption and signature *type identifiers* allow parallel support for multiple primitives.  
- Current mappings include:  
  - **Encryption types:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Signature types:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- This framework enables future upgrades, including post‑quantum schemes, without network splits.

## Cryptographic Composition

- **Transport layer:** X25519 + ChaCha20/Poly1305 (Noise framework).  
- **Tunnel layer:** AES‑256/CBC layered encryption for anonymity.  
- **End‑to‑end:** ECIES‑X25519‑AEAD‑Ratchet for confidentiality and forward secrecy.  
- **Database layer:** EdDSA/RedDSA signatures for authenticity.  

These layers combine to provide defense‑in‑depth: even if one layer is compromised, others maintain confidentiality and unlinkability.

## Summary

I2P 2.10.0’s cryptographic stack centers on:  

- **Curve25519 (X25519)** for key exchange  
- **ChaCha20/Poly1305** for symmetric encryption  
- **EdDSA / RedDSA** for signatures  
- **SHA‑256 / SHA‑512** for hashing and derivation  
- **Experimental post‑quantum hybrid modes** for forward compatibility  

Legacy ElGamal, AES‑CBC, and DSA remain for backward compatibility but are no longer used in active transports or encryption paths.
