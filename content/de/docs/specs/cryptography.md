---
title: "Kryptografie auf niedriger Ebene"
description: "Zusammenfassung der in I2P verwendeten symmetrischen, asymmetrischen und Signatur-Primitive"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Status:** Diese Seite fasst die veraltete „Low-level Cryptography Specification“ zusammen. Moderne I2P-Versionen (2.10.0, Oktober 2025) haben die Umstellung auf neue kryptografische Primitive abgeschlossen. Verwenden Sie spezielle Spezifikationen wie [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/) und [Tunnel Creation (ECIES)](/docs/specs/implementation/) für Implementierungsdetails.

## Evolution-Snapshot

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
## Asymmetrische Verschlüsselung

### X25519 (Schlüsselaustauschverfahren über die elliptische Kurve Curve25519)

- Wird verwendet für NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 und die Erstellung von X25519-basierten tunnel.  
- Bietet kompakte Schlüssel, zeitkonstante Operationen und Vorwärtsgeheimnis über das Noise-Protokoll-Framework.  
- Bietet 128-Bit-Sicherheit mit 32-Byte-Schlüsseln und effizientem Schlüsselaustausch.

### ElGamal (veraltet)

- Zur Abwärtskompatibilität mit älteren routers beibehalten.  
- Arbeitet über die 2048‑Bit Oakley Group 14‑Primzahl (RFC 3526) mit Generator 2.  
- Verschlüsselt AES‑Sitzungsschlüssel plus IVs in 514‑Byte‑Geheimtexten.  
- Unterstützt weder authentifizierte Verschlüsselung noch Vorwärtsgeheimnis; alle modernen Endpunkte sind auf ECIES migriert.

## Symmetrische Verschlüsselung

### ChaCha20/Poly1305

- Standard‑Primitiv für authentifizierte Verschlüsselung in NTCP2, SSU2 und ECIES.  
- Bietet AEAD‑Sicherheit (authentifizierte Verschlüsselung mit zusätzlichen Daten) und hohe Leistung ohne AES‑Hardwareunterstützung.  
- Implementiert gemäß RFC 7539 (256‑Bit‑Schlüssel, 96‑Bit‑Nonce, 128‑Bit‑Tag).

### AES‑256/CBC (veraltet)

- Wird weiterhin für die Verschlüsselung auf der tunnel‑Schicht verwendet, da dessen Blockchiffre‑Struktur zum geschichteten Verschlüsselungsmodell von I2P passt.  
- Verwendet PKCS#5‑Padding und per‑Hop‑IV‑Transformationen.  
- Für eine langfristige Überprüfung vorgesehen, bleibt aber kryptografisch solide.

## Signaturen

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
## Hash- und Schlüsselableitung

- **SHA‑256:** Wird für DHT-Schlüssel, HKDF und veraltete Signaturen verwendet.  
- **SHA‑512:** Wird von EdDSA/RedDSA und in Noise‑HKDF‑Ableitungen verwendet.  
- **HKDF‑SHA256:** Leitet Sitzungsschlüssel in ECIES, NTCP2 und SSU2 ab.  
- Täglich rotierende SHA‑256‑Ableitungen sichern die Speicherorte von RouterInfo und LeaseSet in der netDb.

## Zusammenfassung der Transportschicht

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
Beide Transporte bieten Vorwärtsgeheimnis auf Link‑Ebene und Schutz vor Replay‑Angriffen, unter Verwendung des Noise_XK‑Handshake‑Musters.

## Tunnel-Schicht-Verschlüsselung

- Verwendet weiterhin AES‑256/CBC für die mehrschichtige Verschlüsselung pro Hop.  
- Ausgehende Gateways führen iterative AES‑Entschlüsselung durch; jeder Hop verschlüsselt mit seinem Layer‑Schlüssel und IV‑Schlüssel erneut.  
- Doppelte‑IV‑Verschlüsselung mindert Korrelations- und Bestätigungsangriffe.  
- Eine Migration zu AEAD (Authentifizierte Verschlüsselung mit zugehörigen Daten) wird untersucht, ist derzeit jedoch nicht geplant.

## Post-Quanten-Kryptografie

- I2P 2.10.0 führt **experimentelle hybride Post‑Quanten‑Verschlüsselung** ein.  
- Zum Testen manuell über den Hidden Service Manager (Verwaltung für versteckte Dienste) aktiviert.  
- Kombiniert X25519 mit einem quantenresistenten KEM (Hybridmodus).  
- Nicht standardmäßig aktiv; gedacht für Forschung und Leistungsbewertung.

## Erweiterbarkeits-Framework

- Verschlüsselungs- und Signatur-*Typkennungen* ermöglichen die parallele Unterstützung mehrerer Kryptoprimitive.  
- Aktuelle Zuordnungen umfassen:  
  - **Verschlüsselungstypen:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Signaturtypen:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Dieses Framework ermöglicht zukünftige Upgrades, einschließlich Post‑Quanten‑Verfahren, ohne Aufspaltung des Netzwerks.

## Kryptografische Zusammensetzung

- **Transportschicht:** X25519 + ChaCha20/Poly1305 (Noise framework (Kryptografie‑Framework)).  
- **Tunnel‑Schicht:** AES‑256/CBC‑Schichtverschlüsselung für Anonymität.  
- **Ende‑zu‑Ende:** ECIES‑X25519‑AEAD‑Ratchet (Schlüsselwechsel‑Mechanismus) für Vertraulichkeit und Vorwärtsgeheimnis.  
- **Datenbank‑Schicht:** EdDSA/RedDSA‑Signaturen für Authentizität.

Diese Schichten wirken zusammen und ermöglichen eine Verteidigung in der Tiefe: Selbst wenn eine Schicht kompromittiert wird, bewahren die anderen Vertraulichkeit und Nichtverknüpfbarkeit.

## Zusammenfassung

Der kryptografische Stack von I2P 2.10.0 konzentriert sich auf:

- **Curve25519 (X25519)** für Schlüsselaustausch  
- **ChaCha20/Poly1305** für symmetrische Verschlüsselung  
- **EdDSA / RedDSA** für Signaturen  
- **SHA‑256 / SHA‑512** für Hashing und Ableitung  
- **Experimentelle Post‑Quanten‑Hybridmodi** für Vorwärtskompatibilität

Die veralteten Verfahren ElGamal, AES‑CBC und DSA werden aus Gründen der Abwärtskompatibilität zwar beibehalten, jedoch in aktiven Transporten oder Verschlüsselungspfaden nicht mehr verwendet.
