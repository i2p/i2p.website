---
title: "Garlic Routing"
description: "Verständnis der garlic routing Terminologie, Architektur und modernen Implementierung in I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Überblick

**Garlic routing** bleibt eine der Kerninnovationen von I2P und kombiniert mehrschichtige Verschlüsselung, Nachrichtenbündelung und unidirektionale Tunnel. Obwohl konzeptionell ähnlich zu **Onion-Routing**, erweitert es das Modell, indem es mehrere verschlüsselte Nachrichten („Cloves", dt. Gewürznelken) in einem einzigen Umschlag („Garlic", dt. Knoblauch) bündelt, was Effizienz und Anonymität verbessert.

Der Begriff *garlic routing* wurde von [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) in [Roger Dingledines Free Haven Master's Thesis](https://www.freehaven.net/papers.html) (Juni 2000, §8.1.1) geprägt. I2P-Entwickler übernahmen den Begriff in den frühen 2000er Jahren, um die Bündelungserweiterungen und das unidirektionale Transportmodell widerzuspiegeln und es von Tors leitungsvermitteltem Design zu unterscheiden.

> **Zusammenfassung:** Garlic routing = mehrschichtige Verschlüsselung + Nachrichtenbündelung + anonyme Zustellung über unidirektionale tunnel.

---

## 2. Die "Garlic"-Terminologie

Historisch gesehen wurde der Begriff *garlic* in drei verschiedenen Kontexten innerhalb von I2P verwendet:

1. **Mehrschichtige Verschlüsselung** – tunnel-basierter Schutz im Onion-Stil  
2. **Bündelung mehrerer Nachrichten** – mehrere "cloves" innerhalb einer "garlic message"  
3. **Ende-zu-Ende-Verschlüsselung** – früher *ElGamal/AES+SessionTags*, jetzt *ECIES‑X25519‑AEAD‑Ratchet*

Während die Architektur intakt bleibt, wurde das Verschlüsselungsverfahren vollständig modernisiert.

---

## 3. Mehrschichtige Verschlüsselung

Garlic Routing teilt sein grundlegendes Prinzip mit Onion Routing: Jeder Router entschlüsselt nur eine Verschlüsselungsschicht und erfährt dadurch nur den nächsten Hop, aber nicht den vollständigen Pfad.

Allerdings implementiert I2P **unidirektionale Tunnel**, keine bidirektionalen Schaltkreise:

- **Outbound tunnel**: sendet Nachrichten vom Ersteller weg  
- **Inbound tunnel**: transportiert Nachrichten zurück zum Ersteller

Ein vollständiger Roundtrip (Alice ↔ Bob) verwendet vier Tunnel: Alices outbound → Bobs inbound, dann Bobs outbound → Alices inbound. Dieses Design **halbiert die Offenlegung von Korrelationsdaten** im Vergleich zu bidirektionalen Verbindungen.

Für Details zur Tunnel-Implementierung siehe die [Tunnel-Spezifikation](/docs/specs/implementation) und die [Tunnel Creation (ECIES)](/docs/specs/implementation) Spezifikation.

---

## 4. Bündelung mehrerer Nachrichten (Die "Cloves")

Freedmans ursprüngliches garlic routing sah vor, mehrere verschlüsselte "bulbs" (Zwiebeln) innerhalb einer Nachricht zu bündeln. I2P implementiert dies als **cloves** (Knoblauchzehen) innerhalb einer **garlic message** (Knoblauchnachricht) — jede clove hat ihre eigenen verschlüsselten Zustellanweisungen und ein Ziel (router, destination oder tunnel).

Garlic Bundling ermöglicht es I2P:

- Bestätigungen und Metadaten mit Datennachrichten kombinieren
- Beobachtbare Verkehrsmuster reduzieren
- Komplexe Nachrichtenstrukturen ohne zusätzliche Verbindungen unterstützen

![Garlic Message Cloves](/images/garliccloves.png)   *Abbildung 1: Eine Garlic Message, die mehrere Cloves enthält, jede mit eigenen Zustellungsanweisungen.*

Typische Gewürznelken umfassen:

1. **Delivery Status Message** — Bestätigungen, die den Erfolg oder Misserfolg der Zustellung bestätigen.  
   Diese werden in ihre eigene Garlic-Schicht eingebettet, um die Vertraulichkeit zu wahren.
2. **Database Store Message** — automatisch gebündelte LeaseSets, damit Peers antworten können, ohne die netDb erneut abfragen zu müssen.

Cloves werden gebündelt, wenn:

- Ein neues LeaseSet muss veröffentlicht werden  
- Neue Session-Tags werden übermittelt  
- Kürzlich ist keine Bündelung erfolgt (~1 Minute standardmäßig)

Garlic-Nachrichten ermöglichen die effiziente Ende-zu-Ende-Zustellung mehrerer verschlüsselter Komponenten in einem einzigen Paket.

---

## 5. Entwicklung der Verschlüsselung

### 5.1 Historical Context

Frühe Dokumentation (≤ v0.9.12) beschrieb *ElGamal/AES+SessionTags* Verschlüsselung:   - **ElGamal 2048‑bit** umschlossene AES-Sitzungsschlüssel   - **AES‑256/CBC** für Payload-Verschlüsselung   - 32‑Byte Session Tags, die einmal pro Nachricht verwendet werden

Dieses Kryptosystem ist **veraltet**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

Zwischen 2019 und 2023 migrierte I2P vollständig zu ECIES‑X25519‑AEAD‑Ratchet. Der moderne Stack standardisiert die folgenden Komponenten:

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
Vorteile der ECIES-Migration:

- **Forward Secrecy** durch Ratcheting-Schlüssel pro Nachricht  
- **Reduzierte Payload-Größe** im Vergleich zu ElGamal  
- **Widerstandsfähigkeit** gegen kryptoanalytische Fortschritte  
- **Kompatibilität** mit zukünftigen Post-Quantum-Hybriden (siehe Proposal 169)

Weitere Details: siehe die [ECIES-Spezifikation](/docs/specs/ecies) und [EncryptedLeaseSet-Spezifikation](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Garlic-Umschläge enthalten häufig LeaseSets, um die Erreichbarkeit von Zielen zu veröffentlichen oder zu aktualisieren.

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
Alle LeaseSets werden über die *floodfill DHT* verteilt, die von spezialisierten Routern gepflegt wird. Veröffentlichungen werden verifiziert, mit Zeitstempeln versehen und durch Ratenbegrenzung geschützt, um Metadaten-Korrelation zu verringern.

Siehe die [Network Database Dokumentation](/docs/specs/common-structures) für Details.

---

## 7. Modern “Garlic” Applications within I2P

Garlic-Verschlüsselung und Nachrichtenbündelung werden im gesamten I2P-Protokollstapel verwendet:

1. **Tunnel-Erstellung und -Nutzung** — geschichtete Verschlüsselung pro Hop  
2. **Ende-zu-Ende-Nachrichtenübermittlung** — gebündelte garlic messages mit Clone-Acknowledgment- und LeaseSet-Cloves  
3. **Network Database-Veröffentlichung** — LeaseSets in garlic envelopes verpackt für Datenschutz  
4. **SSU2- und NTCP2-Transporte** — Unterlagenverschlüsselung mittels Noise-Framework und X25519/ChaCha20-Primitiven

Garlic routing ist somit sowohl eine *Methode der Verschlüsselungsschichtung* als auch ein *Netzwerk-Messaging-Modell*.

---

## 6. LeaseSets und Garlic Bundling

Das Dokumentationszentrum von I2P ist [hier verfügbar](/docs/) und wird kontinuierlich gepflegt. Relevante aktuelle Spezifikationen umfassen:

- [ECIES Spezifikation](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Tunnel Creation (ECIES)](/docs/specs/implementation) — modernes tunnel build Protokoll
- [I2NP Spezifikation](/docs/specs/i2np) — I2NP Nachrichtenformate
- [SSU2 Spezifikation](/docs/specs/ssu2) — SSU2 UDP Transport
- [Common Structures](/docs/specs/common-structures) — netDb und floodfill Verhalten

Akademische Validierung: Hoang et al. (IMC 2018, USENIX FOCI 2019) und Muntaka et al. (2025) bestätigen die architektonische Stabilität und betriebliche Resilienz des I2P-Designs.

---

## 7. Moderne "Garlic"-Anwendungen innerhalb von I2P

Laufende Vorschläge:

- **Proposal 169:** Hybride Post-Quantum (ML-KEM 512/768/1024 + X25519)  
- **Proposal 168:** Optimierung der Transport-Bandbreite  
- **Datagram- und Streaming-Updates:** Verbesserte Überlastungsverwaltung

Zukünftige Anpassungen könnten zusätzliche Strategien zur Nachrichtenverzögerung oder Multi-Tunnel-Redundanz auf der garlic-message-Ebene umfassen, aufbauend auf ungenutzten Zustelloptionen, die ursprünglich von Freedman beschrieben wurden.

---

## 8. Aktuelle Dokumentation und Referenzen

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
