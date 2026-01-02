---
title: "ElGamal/AES + SessionTag (Sitzungs-Tag) Verschlüsselung"
description: "Veraltete Ende-zu-Ende-Verschlüsselung, die ElGamal, AES, SHA-256 und einmalig verwendbare session tags (Sitzungs-Tags) kombiniert"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Status:** Dieses Dokument beschreibt das veraltete ElGamal/AES+SessionTag-Verschlüsselungsprotokoll. Es wird nur zur Wahrung der Abwärtskompatibilität weiterhin unterstützt, da moderne I2P-Versionen (2.10.0+) [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/) verwenden. Das ElGamal-Protokoll ist veraltet und wird ausschließlich aus historischen Gründen und zur Interoperabilität beibehalten.

## Übersicht

ElGamal/AES+SessionTag war I2Ps ursprünglicher Ende-zu-Ende-Verschlüsselungsmechanismus für garlic messages (in I2P gebündelte, gemeinsam übertragene Nachrichten). Es kombinierte:

- **ElGamal (2048-bit)** — für den Schlüsselaustausch
- **AES-256/CBC** — zur Nutzlastverschlüsselung
- **SHA-256** — für Hashing und Ableitung des IV (Initialisierungsvektors)
- **Session Tags (32 Byte)** — für einmalige Nachrichtenkennungen

Das Protokoll ermöglichte sichere Kommunikation zwischen router und Zielen, ohne dauerhafte Verbindungen aufrechtzuerhalten. Jede Sitzung verwendete einen asymmetrischen ElGamal-Austausch, um einen symmetrischen AES-Schlüssel zu etablieren, gefolgt von leichtgewichtigen "markierten" Nachrichten, die sich auf diese Sitzung bezogen.

## Funktionsweise des Protokolls

### Sitzungsaufbau (Neue Sitzung)

Eine neue Sitzung begann mit einer Nachricht, die zwei Abschnitte enthielt:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
Der Klartext innerhalb des ElGamal-Blocks bestand aus:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### Nachrichten für bestehende Sitzungen

Sobald eine Sitzung hergestellt war, konnte der Absender mithilfe zwischengespeicherter Sitzungs-Tags **existing-session**-Nachrichten senden:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Routers speicherten übermittelte Tags etwa **15 Minuten** lang im Cache, danach verfielen ungenutzte Tags. Tags waren jeweils genau für **eine Nachricht** gültig, um Korrelationsangriffe zu verhindern.

### AES-verschlüsseltes Blockformat

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Routers entschlüsseln mithilfe des Sitzungsschlüssels und des IV, der entweder aus dem Pre-IV (für neue Sitzungen) oder dem Session-Tag (für bestehende Sitzungen) abgeleitet wird. Nach der Entschlüsselung überprüfen sie die Integrität, indem sie den SHA-256-Hash der Klartext-Nutzlast neu berechnen.

## Verwaltung von Session-Tags

- Tags (kurzlebige Sitzungsschlüsselkennungen) sind **unidirektional**: Tags von Alice → Bob können nicht von Bob → Alice wiederverwendet werden.
- Tags laufen nach ungefähr **15 Minuten** ab.
- Routers führen pro Ziel Session-Key-Manager, um Tags, Schlüssel und Ablaufzeiten nachzuverfolgen.
- Anwendungen können das Tag-Verhalten über [I2CP-Optionen](/docs/specs/i2cp/) steuern:
  - **`i2cp.tagThreshold`** — Mindestanzahl zwischengespeicherter Tags, bevor nachgefüllt wird
  - **`i2cp.tagCount`** — Anzahl neuer Tags pro Nachricht

Dieser Mechanismus minimierte aufwändige ElGamal-Handshakes, während er die Nicht-Verknüpfbarkeit zwischen Nachrichten aufrechterhielt.

## Konfiguration und Effizienz

Session-Tags wurden eingeführt, um die Effizienz über I2Ps hochlatenzbehafteten, ungeordneten Transport zu verbessern. Eine typische Konfiguration lieferte **40 Tags pro Nachricht** und verursachte etwa 1,2 KB Overhead. Anwendungen konnten das Zustellverhalten abhängig vom erwarteten Datenverkehr anpassen:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
Router bereinigen regelmäßig abgelaufene Tags und entfernen ungenutzten Sitzungszustand, um die Speicherauslastung zu reduzieren und Tag-Flooding-Angriffe abzumildern.

## Einschränkungen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
Diese Schwächen führten direkt zur Entwicklung des [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)-Protokolls, das perfektes Vorwärtsgeheimnis, authentifizierte Verschlüsselung und einen effizienten Schlüsselaustausch bietet.

## Abkündigungs- und Migrationsstatus

- **Eingeführt:** Frühe I2P-Releases (vor 0.6)
- **Als veraltet markiert:** Mit der Einführung von ECIES-X25519 (ECIES mit X25519-Schlüsselvereinbarung) (0.9.46 → 0.9.48)
- **Entfernt:** Seit 2.4.0 nicht mehr Standard (Dezember 2023)
- **Unterstützt:** Nur zur Wahrung der Abwärtskompatibilität

Moderne routers und destinations (Ziele) geben jetzt **Kryptotyp 4 (ECIES-X25519)** statt **Typ 0 (ElGamal/AES)** bekannt. Das Legacy-Protokoll wird weiterhin unterstützt, um die Interoperabilität mit veralteten Peers zu gewährleisten, sollte jedoch nicht für neue Bereitstellungen verwendet werden.

## Historischer Kontext

ElGamal/AES+SessionTag war grundlegend für die frühe kryptografische Architektur von I2P. Sein hybrides Design führte Neuerungen ein, darunter einmalige session tags (Sitzungsmarken) und unidirektionale Sitzungen, die nachfolgende Protokolle beeinflussten. Viele dieser Ideen entwickelten sich zu modernen Konstruktionen wie deterministic ratchets (deterministische Ratchet-Mechanismen) und hybriden Post-Quanten-Schlüsselaustauschverfahren.
