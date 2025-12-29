---
title: "Nízkoúrovňová kryptografie"
description: "Souhrn symetrických, asymetrických a podpisových primitiv používaných napříč I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Stav:** Tato stránka stručně shrnuje zastaralou "Low-level Cryptography Specification". Moderní vydání I2P (2.10.0, říjen 2025) dokončila přechod na nová kryptografická primitiva. Pro implementační detaily použijte specializované specifikace, jako [ECIES](/docs/specs/ecies/), [Šifrované LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/), a [Tunnel Creation (ECIES)](/docs/specs/implementation/) pro implementační detaily.

## Snímek vývoje

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
## Asymetrické šifrování

### X25519 (algoritmus výměny klíčů ECDH nad eliptickou křivkou Curve25519)

- Používá se pro NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 a vytváření tunnel na bázi X25519.  
- Poskytuje kompaktní klíče, operace v konstantním čase a dopředné utajení prostřednictvím rámce protokolu Noise.  
- Nabízí 128bitovou bezpečnost s 32bajtovými klíči a efektivní výměnu klíčů.

### ElGamal (zastaralé)

- Zachováno kvůli zpětné kompatibilitě se staršími routery.  
- Operuje nad 2048bitovým prvočíslem Oakley Group 14 (RFC 3526) s generátorem 2.  
- Šifruje relanční klíče AES a IV (inicializační vektory) do šifrotextů o velikosti 514 bajtů.  
- Postrádá autentizované šifrování a dopředné utajení; všechny moderní koncové body přešly na ECIES.

## Symetrické šifrování

### ChaCha20/Poly1305 (AEAD šifra, kombinace ChaCha20 a Poly1305)

- Výchozí primitivum pro autentizované šifrování napříč NTCP2, SSU2 a ECIES.  
- Poskytuje zabezpečení AEAD a vysoký výkon i bez hardwarové podpory AES.  
- Implementováno dle RFC 7539 (256‑bitový klíč, 96‑bitová nonce (jednorázová hodnota), 128‑bitový autentizační tag).

### AES‑256/CBC (zastaralé)

- Stále se používá pro šifrování na vrstvě tunnelu, kde jeho struktura blokové šifry zapadá do vrstveného šifrovacího modelu I2P.  
- Používá PKCS#5 padding a transformace IV na každém hopu.  
- Je určeno k dlouhodobé revizi, ale nadále zůstává kryptograficky bezpečné.

## Podpisy

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
## Hašování a odvozování klíčů

- **SHA‑256:** Používá se pro klíče DHT (distribuovaná hašovací tabulka), HKDF (funkce odvozování klíčů na bázi HMAC) a starší podpisy.  
- **SHA‑512:** Používá se v EdDSA/RedDSA (schémata digitálních podpisů na eliptických křivkách) a při odvozeních HKDF v rámci Noise (kryptografický rámec pro handshaky).  
- **HKDF‑SHA256:** Odvozuje relační klíče v ECIES (integrované šifrování na eliptických křivkách), NTCP2 a SSU2.  
- Denně rotující odvození SHA‑256 zabezpečují lokace uložení RouterInfo a LeaseSet v netDb.

## Souhrn transportní vrstvy

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
Oba transporty poskytují dopředné utajení na linkové úrovni a ochranu proti replay útokům pomocí Noise_XK handshake pattern (vzor handshaku).

## Šifrování vrstvy tunnel

- Nadále používá AES‑256/CBC pro vrstvené šifrování na úrovni jednotlivých skoků.  
- Odchozí brány provádějí iterativní dešifrování AES; každý skok znovu šifruje pomocí svého klíče vrstvy a klíče IV (inicializační vektor).  
- Šifrování s dvojitým IV zmírňuje korelační a potvrzovací útoky.  
- Přechod na AEAD (autentizované šifrování s přidruženými daty) je zkoumán, ale aktuálně se neplánuje.

## Postkvantová kryptografie

- I2P 2.10.0 zavádí **experimentální hybridní post‑kvantové šifrování**.  
- Lze ručně povolit prostřednictvím Hidden Service Manager (Správce skrytých služeb) pro testování.  
- Kombinuje X25519 s kvantově odolným KEM (hybridní režim).  
- Není ve výchozím nastavení; je určeno pro výzkum a hodnocení výkonu.

## Rámec rozšiřitelnosti

- Šifrovací a podpisové *identifikátory typů* umožňují paralelní podporu více kryptografických primitiv.  
- Aktuální mapování zahrnuje:  
  - **Typy šifrování:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Typy podpisů:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Tento rámec umožňuje budoucí aktualizace, včetně postkvantových schémat, bez rozdělení sítě.

## Kryptografická kompozice

- **Transportní vrstva:** X25519 + ChaCha20/Poly1305 (rámec Noise).  
- **Vrstva tunnel:** AES‑256/CBC vrstvené šifrování pro anonymitu.  
- **End‑to‑end:** ECIES‑X25519‑AEAD‑Ratchet pro důvěrnost a dopředné utajení.  
- **Databázová vrstva:** podpisy EdDSA/RedDSA pro autenticitu.

Tyto vrstvy společně zajišťují obranu do hloubky: i když je jedna vrstva kompromitována, ostatní udrží důvěrnost a nepropojitelnost.

## Shrnutí

Kryptografický stack I2P 2.10.0 se soustředí na:

- **Curve25519 (X25519)** pro výměnu klíčů  
- **ChaCha20/Poly1305** pro symetrické šifrování  
- **EdDSA / RedDSA** pro podpisy  
- **SHA‑256 / SHA‑512** pro hašování a derivaci  
- **Experimentální post‑kvantové hybridní režimy** pro budoucí kompatibilitu

Starší ElGamal, AES‑CBC a DSA zůstávají kvůli zpětné kompatibilitě, ale již se nepoužívají v aktivních transportech ani v šifrovacích cestách.
