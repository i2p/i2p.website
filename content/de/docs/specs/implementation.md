---
title: "Leitfaden für den Tunnelbetrieb"
description: "Vereinheitlichte Spezifikation zum Aufbau, zur Verschlüsselung und zum Transport von Datenverkehr über I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Geltungsbereich:** Dieser Leitfaden fasst die tunnel-Implementierung, das Nachrichtenformat und beide Spezifikationen für die tunnel-Erstellung (ECIES und veraltetes ElGamal) zusammen. Bestehende Deep Links funktionieren weiterhin über die oben genannten Aliase.

## Tunnelmodell {#tunnel-model}

I2P leitet Nutzdaten durch *unidirektionale tunnels* weiter: geordnete Sequenzen von routers, die den Datenverkehr nur in eine Richtung transportieren. Ein vollständiger Hin- und Rückweg zwischen zwei Zielen erfordert vier tunnels (zwei ausgehend, zwei eingehend).

Beginnen Sie mit der [Tunnel-Übersicht](/docs/overview/tunnel-routing/) für die Terminologie und verwenden Sie dann diesen Leitfaden für die operativen Details.

### Lebenszyklus von Nachrichten {#message-lifecycle}

1. Das tunnel-**Gateway** bündelt eine oder mehrere I2NP-Nachrichten, fragmentiert sie und schreibt Zustellanweisungen.
2. Das Gateway kapselt die Nutzlast in eine tunnel-Nachricht fester Größe (1024&nbsp;B) ein und füllt bei Bedarf mit Padding auf.
3. Jeder **Teilnehmer** verifiziert den vorherigen Hop, wendet seine Verschlüsselungsschicht an und leitet {nextTunnelId, nextIV, encryptedPayload} an den nächsten Hop weiter.
4. Der tunnel-**Endpunkt** entfernt die letzte Schicht, wertet die Zustellanweisungen aus, setzt Fragmente wieder zusammen und gibt die rekonstruierten I2NP-Nachrichten weiter.

Die Duplikaterkennung verwendet einen zeitlich verfallenden Bloom-Filter, dessen Schlüssel das XOR aus dem IV (Initialisierungsvektor) und dem ersten Chiffrierblock ist, um Tagging-Angriffe auf Basis von IV‑Vertauschungen zu verhindern.

### Rollen im Überblick {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Verschlüsselungs-Workflow {#encryption-workflow}

- **Inbound tunnels:** das Gateway verschlüsselt einmal mit seinem Layer-Schlüssel; nachgelagerte Teilnehmer verschlüsseln weiter, bis der Ersteller die endgültige Nutzlast entschlüsselt.
- **Outbound tunnels:** das Gateway wendet vorab das Inverse der Verschlüsselung jedes einzelnen Hops an, sodass jeder Teilnehmer verschlüsselt. Wenn der Endpunkt verschlüsselt, wird der ursprüngliche Klartext des Gateways offengelegt.

In beiden Richtungen wird `{tunnelId, IV, encryptedPayload}` an den nächsten Hop weitergeleitet.

---

## Tunnel-Nachrichtenformat {#tunnel-message-format}

Tunnel-Gateways fragmentieren I2NP-Nachrichten in Umschläge fester Größe, um die Nutzlastlänge zu verbergen und die Verarbeitung pro Sprung zu vereinfachen.

### Verschlüsseltes Layout {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – 32-Bit-Bezeichner für den nächsten Hop (ungleich Null, rotiert bei jedem Build-Zyklus).
- **IV** – 16-Byte AES IV, pro Nachricht gewählt.
- **Verschlüsselte Nutzlast** – 1008 Bytes AES-256-CBC-Chiffrat.

Gesamtgröße: 1028 Byte.

### Entschlüsseltes Layout {#decrypted-layout}

Nachdem ein Hop (Zwischenknoten) seine Verschlüsselungsschicht entfernt:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Prüfsumme** verifiziert den entschlüsselten Block.
- **Padding (Auffüllung)** besteht aus zufälligen Nicht-Null-Bytes, die durch ein Nullbyte abgeschlossen werden.
- **Zustellanweisungen** geben dem Endpunkt vor, wie jedes Fragment zu behandeln ist (lokal zustellen, an einen anderen tunnel weiterleiten, usw.).
- **Fragmente** transportieren die zugrunde liegenden I2NP-Nachrichten; der Endpunkt setzt sie wieder zusammen, bevor er sie an höhere Schichten weitergibt.

### Verarbeitungsschritte {#processing-steps}

1. Gateways fragmentieren und reihen I2NP-Nachrichten in Warteschlangen ein; dabei halten sie Teilfragmente kurzzeitig zur späteren Wiederzusammensetzung vor.
2. Das Gateway verschlüsselt die Nutzlast mit den passenden Layer-Schlüsseln und fügt die tunnel ID sowie die IV (Initialisierungsvektor) ein.
3. Jeder Teilnehmer verschlüsselt die IV (AES-256/ECB) und anschließend die Nutzlast (AES-256/CBC), verschlüsselt danach die IV erneut und leitet die Nachricht weiter.
4. Der Endpunkt entschlüsselt in umgekehrter Reihenfolge, verifiziert die Prüfsumme, verarbeitet die Zustellanweisungen und setzt die Fragmente wieder zusammen.

---

## Tunnel-Erstellung (ECIES-X25519) {#tunnel-creation-ecies}

Moderne routers bauen tunnels mit ECIES-X25519-Schlüsseln, wodurch die Aufbau-Nachrichten kleiner werden und Vorwärtsgeheimnis ermöglicht wird.

- **Build-Nachricht:** Eine einzelne I2NP-Nachricht `TunnelBuild` (oder `VariableTunnelBuild`) transportiert 1–8 verschlüsselte Build-Einträge, je einen pro Hop.
- **Layer-Schlüssel:** Ersteller leiten pro Hop Layer-, IV- und Reply-Schlüssel mittels HKDF (HMAC-basierte Schlüsselableitungsfunktion) aus der statischen X25519-Identität des Hops und dem ephemeren Schlüssel des Erstellers ab.
- **Verarbeitung:** Jeder Hop entschlüsselt seinen Eintrag, validiert Anforderungs-Flags, schreibt den Reply-Block (Erfolg oder detaillierter Fehlercode), verschlüsselt die verbleibenden Einträge erneut und leitet die Nachricht weiter.
- **Antworten:** Der Ersteller erhält eine mit garlic encryption umhüllte Antwortnachricht. Als fehlgeschlagen markierte Einträge enthalten einen Schweregradcode, damit der router den Peer profilieren kann.
- **Kompatibilität:** router können aus Gründen der Abwärtskompatibilität weiterhin ältere ElGamal-Builds akzeptieren, aber neue tunnels verwenden standardmäßig ECIES (integriertes Verschlüsselungsschema auf elliptischen Kurven).

> Für Konstanten zu den einzelnen Feldern und Anmerkungen zur Schlüsselableitung siehe die ECIES-Vorschlagshistorie und den router-Quellcode; dieser Leitfaden behandelt den operativen Ablauf.

---

## Erstellung veralteter Tunnel (ElGamal-2048) {#tunnel-creation-elgamal}

Das ursprüngliche tunnel-Aufbauformat verwendete öffentliche ElGamal-Schlüssel. Moderne routers halten zur Abwärtskompatibilität eine begrenzte Unterstützung aufrecht.

> **Status:** Veraltet. Hier als historische Referenz und für alle, die mit älteren Versionen kompatible Werkzeuge warten, beibehalten.

- **Nicht-interaktives Teleskopieren:** Eine einzelne Build-Nachricht durchläuft den gesamten Pfad. Jeder Hop entschlüsselt seinen 528-Byte-Datensatz, aktualisiert die Nachricht und leitet sie weiter.
- **Variable Länge:** Die Variable Tunnel Build Message (VTBM) erlaubte 1–8 Datensätze. Die frühere feste Nachricht enthielt stets acht Datensätze, um die Länge des tunnel zu verschleiern.
- **Layout des Anfragedatensatzes:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Flags:** Bit 7 kennzeichnet ein inbound gateway (IBGW; eingehendes Gateway); Bit 6 markiert einen outbound endpoint (OBEP; ausgehender Endpunkt). Sie schließen sich gegenseitig aus.
- **Verschlüsselung:** Jeder Eintrag ist mit dem öffentlichen Schlüssel des Hop (Weiterleitungsknoten) ElGamal‑2048‑verschlüsselt. Symmetrische AES‑256‑CBC‑Schichtung stellt sicher, dass nur der vorgesehene Hop seinen Eintrag lesen kann.
- **Wichtige Fakten:** tunnel IDs sind von Null verschiedene 32‑Bit‑Werte; Ersteller können Dummy‑Einträge einfügen, um die tatsächliche tunnel‑Länge zu verbergen; die Zuverlässigkeit hängt von Wiederholungsversuchen bei fehlgeschlagenen Builds ab.

---

## Tunnel-Pools und Lebenszyklus {#tunnel-pools}

Router unterhalten unabhängige eingehende und ausgehende tunnel-Pools für Erkundungsverkehr und für jede I2CP-Sitzung.

- **Peer-Auswahl:** exploratorische tunnels bedienen sich aus dem „active, not failing“-peer bucket (Gruppe), um Diversität zu fördern; Client-tunnels bevorzugen schnelle Peers mit hoher Kapazität.
- **Deterministische Reihenfolge:** Peers werden nach der XOR-Distanz zwischen `SHA256(peerHash || poolKey)` und dem zufälligen Schlüssel des Pools sortiert. Der Schlüssel wechselt beim Neustart, was innerhalb eines Laufs Stabilität bietet und Vorgängerangriffe über mehrere Läufe hinweg erschwert.
- **Lebenszyklus:** router erfassen historische Aufbauzeiten pro `{mode, direction, length, variance}`-Tupel. Wenn tunnels dem Ablauf nahekommen, beginnt der Ersatz frühzeitig; der router erhöht bei Fehlschlägen die Anzahl paralleler Aufbauvorgänge und begrenzt gleichzeitig die Anzahl ausstehender Versuche.
- **Konfigurationsoptionen:** Anzahl aktiver/Backup-tunnels, Hop-Länge und Varianz, Zero-Hop-Erlaubnisse (ohne Zwischenhop) sowie Grenzen für die Aufbau-Rate sind pro Pool einstellbar.

---

## Überlastung und Zuverlässigkeit {#congestion}

Obwohl tunnels Verbindungen ähneln, behandeln routers sie wie Nachrichtenwarteschlangen. Weighted Random Early Discard (WRED; gewichtetes zufälliges frühzeitiges Verwerfen) wird verwendet, um die Latenz begrenzt zu halten:

- Die Drop-Wahrscheinlichkeit steigt, wenn die Auslastung sich den konfigurierten Grenzwerten nähert.
- Teilnehmer berücksichtigen Fragmente fester Größe; Gateways/Endpunkte verwerfen anhand der Gesamtgröße der Fragmente und benachteiligen dabei große Nutzlasten zuerst.
- Ausgehende Endpunkte verwerfen früher als andere Rollen, um möglichst wenig Netzwerkressourcen zu verschwenden.

Garantierte Zustellung wird höheren Schichten wie der [Streaming library](/docs/specs/streaming/) überlassen. Anwendungen, die Zuverlässigkeit benötigen, müssen erneute Übertragungen und Bestätigungen selbst übernehmen.

---

## Weiterführende Informationen {#further-reading}

- [Unidirektionale Tunnels (historisch)](/docs/legacy/unidirectional-tunnels/)
- [Peer-Auswahl](/docs/overview/tunnel-routing#peer-selection/)
- [Tunnel-Übersicht](/docs/overview/tunnel-routing/)
- [Alte Tunnel-Implementierung](/docs/legacy/old-implementation/)
