---
title: "Spezifikation für Software-Updates"
description: "Sicherer, signierter Update-Mechanismus und Feed-Struktur für I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Übersicht

router prüfen automatisch auf Updates, indem sie einen signierten News-Feed abfragen, der über das I2P-Netzwerk verteilt wird. Wenn eine neuere Version angekündigt wird, lädt der router ein kryptografisch signiertes Update-Archiv (`.su3`) herunter und bereitet es zur Installation vor.   Dieses System gewährleistet eine **authentifizierte, manipulationsresistente** und **mehrkanalige** Verteilung offizieller Veröffentlichungen.

Seit I2P 2.10.0 verwendet das Aktualisierungssystem: - **RSA-4096 / SHA-512** Signaturen - **SU3-Containerformat** (ersetzt das veraltete SUD/SU2) - **Redundante Spiegel:** netzwerkinternes HTTP, Clearnet-HTTPS und BitTorrent

---

## 1. Newsfeed

Routers rufen den signierten Atom-Feed alle paar Stunden ab, um neue Versionen und Sicherheitshinweise zu entdecken. Der Feed ist signiert und wird als `.su3`-Datei verteilt, die Folgendes enthalten kann:

- `<i2p:version>` — neue Versionsnummer  
- `<i2p:minVersion>` — unterstützte Mindestversion für den router  
- `<i2p:minJavaVersion>` — erforderliche Mindestversion der Java-Laufzeitumgebung  
- `<i2p:update>` — listet mehrere Download-Spiegel (I2P, HTTPS, torrent) auf  
- `<i2p:revocations>` — Daten zum Zertifikatswiderruf  
- `<i2p:blocklist>` — netzwerkweite Blocklisten für kompromittierte Peers

### Feed-Verteilung

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers bevorzugen den I2P-Feed, können bei Bedarf jedoch auf Clearnet- oder Torrent-Verteilung zurückgreifen.

---

## 2. Dateiformate

### SU3 (Aktueller Standard)

Mit Version 0.9.9 eingeführt, ersetzte SU3 die veralteten SUD- und SU2-Formate. Jede Datei enthält einen Header, Nutzdaten und eine abschließende Signatur.

**Header-Struktur** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Schritte zur Signaturüberprüfung** 1. Header parsen und Signaturalgorithmus identifizieren.   2. Hash und Signatur mithilfe des gespeicherten Unterzeichnerzertifikats verifizieren.   3. Bestätigen, dass das Zertifikat des Unterzeichners nicht widerrufen wurde.   4. Eingebetteten Versionsstring mit den Nutzlast-Metadaten vergleichen.

Routers werden mit Zertifikaten vertrauenswürdiger Unterzeichner (derzeit **zzz** und **str4d**) ausgeliefert und lehnen alle unsignierten oder widerrufenen Quellen ab.

### SU2 (Veraltet)

- Verwendete die Dateiendung `.su2` mit Pack200-komprimierten JAR-Dateien.  
- Entfernt, nachdem Java 14 Pack200 als veraltet markiert hat (JEP 367).  
- In I2P 0.9.48+ deaktiviert; jetzt vollständig durch ZIP-Kompression ersetzt.

### SUD (veraltet)

- Frühes DSA-SHA1-signiertes ZIP-Format (vor 0.9.9).  
- Keine Unterzeichner-ID oder Header, begrenzte Integrität.  
- Ersetzt aufgrund schwacher Kryptografie und fehlender Durchsetzung von Versionsanforderungen.

---

## 3. Aktualisierungs-Workflow

### 3.1 Header-Überprüfung

Router rufen nur den **SU3 header** ab, um den Versionsstring zu verifizieren, bevor sie vollständige Dateien herunterladen. Dies verhindert, dass Bandbreite für veraltete Mirror-Server oder veraltete Versionen verschwendet wird.

### 3.2 Vollständiger Download

Nach der Überprüfung des Headers lädt der router die vollständige `.su3`-Datei von: - netzinternen eepsite-Spiegeln (bevorzugt)   - HTTPS-Clearnet-Spiegeln (Ausweichlösung)   - BitTorrent (optionale peer-unterstützte Verteilung)

Downloads verwenden Standard-I2PTunnel-HTTP-Clients, mit Wiederholversuchen, Timeout-Behandlung und Fallback auf Spiegelserver.

### 3.3 Signaturprüfung

Jede heruntergeladene Datei durchläuft: - **Signaturprüfung:** RSA-4096/SHA512-Überprüfung   - **Versionsabgleich:** Abgleich von Header- und Nutzlast-Version   - **Schutz vor Downgrades:** Stellt sicher, dass das Update neuer ist als die installierte Version

Ungültige oder nicht übereinstimmende Dateien werden sofort verworfen.

### 3.4 Installations-Staging

Nach der Überprüfung: 1. ZIP-Inhalt in ein temporäres Verzeichnis entpacken   2. In `deletelist.txt` aufgeführte Dateien entfernen   3. Native Bibliotheken ersetzen, falls `lib/jbigi.jar` enthalten ist   4. Signierer-Zertifikate nach `~/.i2p/certificates/` kopieren   5. Update nach `i2pupdate.zip` verschieben, damit es beim nächsten Neustart angewendet wird

Das Update wird beim nächsten Start automatisch installiert oder wenn „Update jetzt installieren“ manuell ausgelöst wird.

---

## 4. Dateiverwaltung

### deletelist.txt

Eine Klartextliste veralteter Dateien, die vor dem Entpacken neuer Inhalte entfernt werden sollen.

**Regeln:** - Ein Pfad pro Zeile (nur relative Pfade) - Zeilen, die mit `#` beginnen, werden ignoriert - `..` und absolute Pfade werden abgelehnt

### Native Bibliotheken

Um veraltete oder nicht passende native Bibliotheken zu vermeiden: - Wenn `lib/jbigi.jar` existiert, werden alte `.so`- oder `.dll`-Dateien gelöscht   - Stellt sicher, dass plattformspezifische Bibliotheken frisch extrahiert werden

---

## 5. Zertifikatsverwaltung

Router können **neue Signaturzertifikate** durch Updates oder Widerrufe im Newsfeed erhalten.

- Neue `.crt`-Dateien werden in das Zertifikatsverzeichnis kopiert.  
- Widerrufene Zertifikate werden vor zukünftigen Überprüfungen gelöscht.  
- Unterstützt Schlüsselrotation, ohne manuelles Eingreifen des Benutzers zu erfordern.

Alle Updates werden offline mit **air-gapped signing systems** (physisch vom Netzwerk isolierte Signiersysteme) signiert. Private Schlüssel werden niemals auf Build-Servern gespeichert.

---

## 6. Entwicklerrichtlinien

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Zukünftige Releases werden die Integration von Post-Quanten-Signaturen (siehe Proposal 169) und reproduzierbare Builds untersuchen.

---

## 7. Sicherheitsübersicht

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Versionierung

- Router: **2.10.0 (API 0.9.67)**  
- Semantische Versionierung mit `Major.Minor.Patch`.  
- Erzwingung der Mindestversion verhindert unsichere Aktualisierungen.  
- Unterstütztes Java: **Java 8–17**. Künftig erfordert 2.11.0+ Java 17+.

---
