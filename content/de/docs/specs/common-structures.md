---
title: "Gemeinsame Strukturen"
description: "Gemeinsame Datentypen und Serialisierungsformate, die in I2P-Spezifikationen verwendet werden"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Übersicht

Dieses Dokument definiert die grundlegenden Datenstrukturen, die in allen I2P-Protokollen verwendet werden, einschließlich [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) und weiteren. Diese gemeinsamen Strukturen gewährleisten die Interoperabilität zwischen verschiedenen I2P-Implementierungen und Protokollschichten.

### Wichtige Änderungen seit 0.9.58

- ElGamal und DSA-SHA1 für Router-Identitäten als veraltet markiert (verwenden Sie X25519 + EdDSA)
- Unterstützung für Post-Quanten-ML-KEM (Mechanismus zur Schlüsselkapselung) im Beta-Test (per Opt-in ab 2.10.0)
- Service-Record-Optionen (Service Record = Dienst-Eintrag) standardisiert ([Proposal 167](/proposals/167-service-records/), implementiert in 0.9.66)
- Spezifikationen für komprimierbares Padding (Auffüllung) finalisiert ([Proposal 161](/de/proposals/161-ri-dest-padding/), implementiert in 0.9.57)

---

## Allgemeine Typspezifikationen

### Ganzzahl

**Beschreibung:** Stellt eine nichtnegative ganze Zahl in Netzwerk-Byte-Reihenfolge (Big-Endian) dar.

**Inhalt:** 1 bis 8 Bytes, die eine vorzeichenlose Ganzzahl darstellen.

**Verwendung:** Feldlängen, Anzahlen, Typkennungen und numerische Werte in sämtlichen I2P-Protokollen.

---

### Datum

**Beschreibung:** Zeitstempel, der die Millisekunden seit der Unix-Epoche (1. Januar 1970, 00:00:00 GMT) angibt.

**Inhalt:** 8-Byte-Ganzzahl (unsigned long)

**Spezielle Werte:** - `0` = Undefiniertes oder Null-Datum - Maximalwert: `0xFFFFFFFFFFFFFFFF` (Jahr 584.942.417.355)

**Hinweise zur Implementierung:** - Immer UTC/GMT als Zeitzone - Millisekundengenauigkeit erforderlich - Wird für den Ablauf von Leases (Einträge in einem leaseSet mit Ablaufzeit), die Veröffentlichung der RouterInfo (Metadaten über einen Router) und die Validierung von Zeitstempeln verwendet

---

### Zeichenkette

**Beschreibung:** UTF-8-kodierte Zeichenkette mit Längenpräfix.

**Format:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Einschränkungen:** - Maximale Länge: 255 Bytes (nicht Zeichen - mehrbytige UTF-8-Sequenzen zählen als mehrere Bytes) - Länge kann 0 sein (leere Zeichenkette) - Nullterminator NICHT enthalten - Zeichenkette ist NICHT nullterminiert

**Wichtig:** UTF-8-Sequenzen können mehrere Bytes pro Zeichen verwenden. Eine Zeichenkette mit 100 Zeichen kann das 255-Byte-Limit überschreiten, wenn mehrbyteige Zeichen verwendet werden.

---

## Kryptografische Schlüsselstrukturen

### Öffentlicher Schlüssel

**Beschreibung:** Öffentlicher Schlüssel für asymmetrische Verschlüsselung. Schlüsseltyp und -länge sind kontextabhängig oder in einem Schlüsselzertifikat angegeben.

**Standardtyp:** ElGamal (seit 0.9.58 für Router Identities veraltet)

**Unterstützte Typen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Implementierungsanforderungen:**

1. **X25519 (Typ 4) - Aktueller Standard:**
   - Wird für ECIES-X25519-AEAD-Ratchet-Verschlüsselung verwendet
   - Seit 0.9.48 für Router-Identitäten verpflichtend
   - Little-endian-Kodierung (im Gegensatz zu anderen Typen)
   - Siehe [ECIES](/docs/specs/ecies/) und [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Typ 0) - Legacy:**
   - Seit 0.9.58 für Router-Identitäten veraltet
   - Für Destinations (Ziele) weiterhin gültig (Feld seit 0.6/2005 ungenutzt)
   - Verwendet konstante Primzahlen, die in der [ElGamal-Spezifikation](/docs/specs/cryptography/) definiert sind
   - Unterstützung wird zur Wahrung der Abwärtskompatibilität beibehalten

3. **MLKEM (Post-Quanten) - Beta:**
   - Hybrider Ansatz kombiniert ML-KEM mit X25519
   - NICHT standardmäßig in 2.10.0 aktiviert
   - Erfordert manuelle Aktivierung über den Hidden Service Manager (Verwaltung verborgener Dienste)
   - Siehe [ECIES-HYBRID](/docs/specs/ecies/#hybrid) und [Proposal 169](/proposals/169-pq-crypto/)
   - Typcodes und Spezifikationen können sich ändern

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Privater Schlüssel

**Beschreibung:** Privater Schlüssel für asymmetrische Entschlüsselung, entsprechend den PublicKey-Typen.

**Speicherung:** Typ und Länge werden aus dem Kontext abgeleitet oder separat in Datenstrukturen/Schlüsseldateien gespeichert.

**Unterstützte Typen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Sicherheitshinweise:** - Privatschlüssel MÜSSEN mithilfe kryptografisch sicherer Zufallszahlengeneratoren erzeugt werden - X25519-Privatschlüssel verwenden scalar clamping (Skalarbegrenzung) wie in RFC 7748 definiert - Schlüsselmaterial MUSS sicher aus dem Speicher gelöscht werden, wenn es nicht mehr benötigt wird

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Sitzungsschlüssel

**Beschreibung:** Symmetrischer Schlüssel für AES-256-Verschlüsselung und -Entschlüsselung bei tunnel und garlic encryption von I2P.

**Inhalt:** 32 Bytes (256 Bits)

**Verwendung:** - Tunnel-Schichtverschlüsselung (AES-256/CBC mit IV) - Garlic-Nachrichtenverschlüsselung - Ende-zu-Ende-Sitzungsverschlüsselung

**Erzeugung:** MUSS einen kryptografisch sicheren Zufallszahlengenerator verwenden.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Beschreibung:** Öffentlicher Schlüssel zur Verifikation von Signaturen. Typ und Länge sind im Schlüsselzertifikat der Destination (I2P-Adresse) angegeben oder werden aus dem Kontext abgeleitet.

**Standardtyp:** DSA_SHA1 (ab 0.9.58 veraltet)

**Unterstützte Typen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Implementierungsanforderungen:**

1. **EdDSA_SHA512_Ed25519 (Typ 7) - Aktueller Standard:**
   - Voreinstellung für alle neuen Router-Identitäten und Destinations (Ziele) seit Ende 2015
   - Verwendet die Ed25519-Kurve mit SHA-512-Hashing
   - 32-Byte öffentliche Schlüssel, 64-Byte Signaturen
   - Little-Endian-Codierung (anders als die meisten anderen Typen)
   - Hohe Leistung und Sicherheit

2. **RedDSA_SHA512_Ed25519 (Typ 11) - Spezialisiert:**
   - NUR für verschlüsselte leasesets und Verblindung verwendet
   - Niemals für Router-Identitäten oder Standard-Destinations verwendet
   - Wesentliche Unterschiede zu EdDSA:
     - Private Schlüssel über modulare Reduktion (nicht Clamping)
     - Signaturen enthalten 80 Bytes Zufallsdaten
     - Verwendet öffentliche Schlüssel direkt (keine Hashes privater Schlüssel)
   - Siehe [Red25519-Spezifikation](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Typ 0) - Veraltet:**
   - Seit 0.9.58 für Router-Identitäten als veraltet markiert
   - Für neue Destinations (Zieladressen in I2P) nicht empfohlen
   - 1024-Bit DSA mit SHA-1 (bekannte Schwächen)
   - Unterstützung nur aus Kompatibilitätsgründen beibehalten

4. **Mehrteilige Schlüssel:**
   - Wenn aus zwei Elementen zusammengesetzt (z. B. ECDSA-Punkte X,Y)
   - Jedes Element wird auf die Länge/2 mit führenden Nullen aufgefüllt
   - Beispiel: 64-Byte-ECDSA-Schlüssel = 32-Byte X + 32-Byte Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Beschreibung:** Privater Schlüssel zum Erstellen von Signaturen, entsprechend den SigningPublicKey-Typen.

**Speicherung:** Typ und Länge werden bei der Erstellung festgelegt.

**Unterstützte Typen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Sicherheitsanforderungen:** - Mit einer kryptografisch sicheren Zufallsquelle erzeugen - Mit geeigneten Zugriffskontrollen schützen - Nach Abschluss sicher aus dem Speicher löschen - Für EdDSA: 32-Byte-Seed wird mit SHA-512 gehasht, die ersten 32 Bytes werden zum Skalar (geclamped) - Für RedDSA: Abweichende Schlüsselgenerierung (modulare Reduktion statt Clamping)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Signatur

**Beschreibung:** Kryptografische Signatur der Daten, unter Verwendung des dem Typ SigningPrivateKey entsprechenden Signaturalgorithmus.

**Typ und Länge:** Aus dem beim Signieren verwendeten Schlüsseltyp abgeleitet.

**Unterstützte Typen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Format-Hinweise:** - Signaturen mit mehreren Elementen (z. B. ECDSA-R- und -S-Werte) werden pro Element auf Länge/2 mit führenden Nullen aufgefüllt - EdDSA und RedDSA verwenden Little-Endian-Codierung - Alle anderen Typen verwenden Big-Endian-Codierung

**Verifizierung:** - Verwenden Sie den entsprechenden SigningPublicKey - Befolgen Sie die Spezifikationen des Signaturalgorithmus für den Schlüsseltyp - Prüfen Sie, dass die Signaturlänge der erwarteten Länge für den Schlüsseltyp entspricht

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Hashwert

**Beschreibung:** SHA-256-Hash von Daten, der in I2P durchgängig zur Integritätsprüfung und Identifizierung verwendet wird.

**Inhalt:** 32 Byte (256 Bit)

**Verwendung:** - Router Identity-Hashes (Netzwerkdatenbank-Schlüssel) - Destination-Hashes (Netzwerkdatenbank-Schlüssel) - Tunnel-Gateway-Identifizierung in Leases (Einträgen eines leaseSet) - Überprüfung der Datenintegrität - Erzeugung der Tunnel-ID

**Algorithmus:** SHA-256 wie in FIPS 180-4 definiert

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Session-Tag

**Beschreibung:** Zufallszahl zur Sitzungsidentifikation und tagbasierten Verschlüsselung.

**Wichtig:** Die Größe des Session-Tags variiert je nach Verschlüsselungstyp: - **ElGamal/AES+SessionTag:** 32 Bytes (veraltet) - **ECIES-X25519:** 8 Bytes (aktueller Standard)

**Aktueller Standard (ECIES, integriertes Verschlüsselungsschema mit elliptischen Kurven):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Siehe [ECIES](/docs/specs/ecies/) und [ECIES-ROUTERS](/docs/specs/ecies/#routers) für ausführliche Spezifikationen.

**Veraltet (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Erzeugung:** MUSS einen kryptographisch sicheren Zufallszahlengenerator verwenden.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Beschreibung:** Eindeutiger Bezeichner für die Position eines Routers in einem tunnel. Jeder Hop (Weiterleitungsschritt) in einem tunnel hat seine eigene TunnelId.

**Format:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Verwendung:** - Identifiziert eingehende/ausgehende tunnel-Verbindungen bei jedem router - Unterschiedliche TunnelId an jedem Sprung in der tunnel-Kette - Wird in Lease-Strukturen verwendet, um Gateway-tunnel zu identifizieren

**Spezielle Werte:** - `0` = Für spezielle Protokollzwecke reserviert (im Normalbetrieb vermeiden) - TunnelIds (Tunnel-IDs) haben für jeden router nur lokale Bedeutung

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Zertifikatspezifikationen

### Zertifikat

**Beschreibung:** Container für Quittungen, Proof-of-Work (Arbeitsnachweis) oder kryptografische Metadaten, die in ganz I2P verwendet werden.

**Format:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Gesamtgröße:** mindestens 3 Bytes (NULL-Zertifikat), bis zu 65538 Bytes maximal

### Zertifikatstypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Schlüsselzertifikat (Typ 5)

**Einführung:** Version 0.9.12 (Dezember 2013)

**Zweck:** Legt vom Standard abweichende Schlüsseltypen fest und speichert zusätzliche Schlüsseldaten, die über die standardmäßige 384-Byte-KeysAndCert-Struktur hinausgehen.

**Nutzlaststruktur:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Wichtige Implementierungshinweise:**

1. **Reihenfolge der Schlüsseltypen:**
   - **WARNUNG:** Der Typ des Signierschlüssels kommt VOR dem Typ des Kryptoschlüssels
   - Das ist kontraintuitiv, wird jedoch aus Kompatibilitätsgründen beibehalten
   - Reihenfolge: SPKtype, CPKtype (nicht CPKtype, SPKtype)

2. **Layout der Schlüsseldaten in KeysAndCert:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Berechnung überschüssiger Schlüsseldaten:**
   - Wenn Crypto Key > 256 Bytes: Excess = (Crypto Length - 256)
   - Wenn Signing Key > 128 Bytes: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Beispiele (ElGamal-Kryptoschlüssel):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Anforderungen an die Router-Identität:** - NULL-Zertifikat bis Version 0.9.15 verwendet - Schlüsselzertifikat für nicht standardmäßige Schlüsseltypen seit 0.9.16 erforderlich - X25519-Verschlüsselungsschlüssel seit 0.9.48 unterstützt

**Anforderungen an die Destination:** - NULL certificate (NULL-Zertifikat) ODER Key Certificate (Schlüsselzertifikat) (je nach Bedarf) - Key Certificate erforderlich für nicht standardmäßige Signaturschlüsseltypen seit 0.9.12 - Feld für den kryptografischen öffentlichen Schlüssel seit 0.6 (2005) ungenutzt, muss aber weiterhin vorhanden sein

**Wichtige Warnungen:**

1. **NULL vs. KEY-Zertifikat:**
   - Ein KEY-Zertifikat mit den Typen (0,0), das ElGamal+DSA_SHA1 angibt, ist erlaubt, wird aber nicht empfohlen
   - Verwenden Sie für ElGamal+DSA_SHA1 stets das NULL-Zertifikat (kanonische Darstellung)
   - Ein KEY-Zertifikat mit (0,0) ist 4 Bytes länger und kann zu Kompatibilitätsproblemen führen
   - Einige Implementierungen verarbeiten KEY-Zertifikate mit (0,0) möglicherweise nicht korrekt

2. **Validierung überschüssiger Daten:**
   - Implementierungen MÜSSEN überprüfen, dass die Zertifikatslänge mit der erwarteten Länge für die jeweiligen Schlüsseltypen übereinstimmt
   - Zertifikate mit überschüssigen Daten zurückweisen, die keinem Schlüsseltyp zuzuordnen sind
   - Nach einer gültigen Zertifikatsstruktur nachgestellten Datenmüll verbieten

**JavaDoc:** [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Zuordnung

**Beschreibung:** Sammlung von Schlüssel-Wert-Eigenschaften, die für Konfiguration und Metadaten verwendet wird.

**Format:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Größenlimits:** - Schlüssellänge: 0-255 Bytes (+ 1 Längenbyte) - Wertlänge: 0-255 Bytes (+ 1 Längenbyte) - Gesamtgröße der Zuordnung: 0-65535 Bytes (+ 2 Bytes des Größenfelds) - Maximale Strukturgröße: 65537 Bytes

**Kritische Sortieranforderung:**

Wenn Zuordnungen in **signierten Strukturen** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig) vorkommen, MÜSSEN die Einträge nach dem Schlüssel sortiert werden, um die Signaturinvarianz sicherzustellen:

1. **Sortiermethode:** Lexikografische Sortierung anhand von Unicode-Codepunktwerten (entspricht Java String.compareTo())
2. **Groß-/Kleinschreibung:** Schlüssel und Werte unterscheiden im Allgemeinen zwischen Groß- und Kleinschreibung (anwendungsabhängig)
3. **Doppelte Schlüssel:** in signierten Strukturen NICHT erlaubt (führt zu einem Fehler bei der Signaturprüfung)
4. **Zeichenkodierung:** Byteweiser Vergleich in UTF-8

**Warum Sortierung wichtig ist:** - Signaturen werden auf Basis der Byte-Darstellung berechnet - Unterschiedliche Schlüsselreihenfolgen erzeugen unterschiedliche Signaturen - Nicht signierte Zuordnungen erfordern keine Sortierung, sollten aber derselben Konvention folgen

**Implementierungshinweise:**

1. **Kodierungsredundanz:**
   - Sowohl die Trennzeichen `=` und `;` als auch String-Längen-Bytes sind vorhanden
   - Das ist ineffizient, wird jedoch aus Gründen der Kompatibilität beibehalten
   - Die Längen-Bytes sind maßgeblich; Trennzeichen sind erforderlich, aber redundant

2. **Zeichenunterstützung:**
   - Entgegen der Dokumentation WERDEN `=` und `;` innerhalb von Strings unterstützt (Längenbytes handhaben dies)
   - UTF-8-Codierung unterstützt den vollständigen Unicode-Zeichensatz
   - **Warnung:** I2CP verwendet UTF-8, aber I2NP hat historisch UTF-8 nicht korrekt behandelt
   - Verwenden Sie für I2NP-Zuordnungen nach Möglichkeit ASCII für maximale Kompatibilität

3. **Spezielle Kontexte:**
   - **RouterInfo/RouterAddress:** MUSS sortiert sein, keine Duplikate
   - **I2CP SessionConfig:** MUSS sortiert sein, keine Duplikate  
   - **Anwendungszuordnungen:** Sortierung empfohlen, aber nicht immer erforderlich

**Beispiel (RouterInfo-Optionen):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**Javadoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Spezifikation der gemeinsamen Struktur

### SchlüsselUndZertifikat

**Beschreibung:** Grundlegende Struktur, die Verschlüsselungsschlüssel, Signaturschlüssel und Zertifikat kombiniert. Wird sowohl als RouterIdentity (Router-Identität) als auch als Destination (Zieladresse) verwendet.

**Struktur:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Schlüsselausrichtung:** - **Öffentlicher Verschlüsselungsschlüssel:** Am Anfang ausgerichtet (Byte 0) - **Auffüllung:** In der Mitte (falls nötig) - **Öffentlicher Signaturschlüssel:** Am Ende ausgerichtet (Byte 256 bis Byte 383) - **Zertifikat:** Beginnt bei Byte 384

**Größenberechnung:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Richtlinien zur Generierung von Padding ([Vorschlag 161](/de/proposals/161-ri-dest-padding/))

**Implementierungsversion:** 0.9.57 (Januar 2023, Release 2.1.0)

**Hintergrund:** - Für Nicht-ElGamal+DSA-Schlüssel ist Padding in der festen 384-Byte-Struktur vorhanden - Bei Destinations (I2P-Zieladressen) ist das 256-Byte-Feld für den öffentlichen Schlüssel seit 0.6 (2005) ungenutzt - Padding sollte so erzeugt werden, dass es komprimierbar ist und dennoch sicher bleibt

**Voraussetzungen:**

1. **Minimale Zufallsdaten:**
   - Verwenden Sie mindestens 32 Byte kryptographisch sicherer Zufallsdaten
   - Dies liefert ausreichend Entropie für die Sicherheit

2. **Kompressionsstrategie:**
   - Die 32 Bytes im gesamten Padding-/Public-Key-Feld wiederholen
   - Protokolle wie I2NP Database Store, Streaming SYN, SSU2 handshake verwenden Kompression
   - Erhebliche Einsparungen bei der Bandbreite, ohne die Sicherheit zu beeinträchtigen

3. **Beispiele:**

**Router-Identität (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Zieladresse (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Warum das funktioniert:**
   - SHA-256-Hash der vollständigen Struktur enthält weiterhin die gesamte Entropie
   - DHT-Verteilung der Netzwerkdatenbank (netDb) hängt nur vom Hash ab
   - Signaturschlüssel (32 Bytes EdDSA/X25519) liefert 256 Bit Entropie
   - Zusätzliche 32 Bytes an wiederholten Zufallsdaten = 512 Bit Gesamtentropie
   - Mehr als ausreichend für kryptografische Sicherheit

5. **Implementierungshinweise:**
   - MUSS die vollständige Struktur mit 387+ Bytes speichern und übertragen
   - SHA-256-Hash wird über die vollständige, unkomprimierte Struktur berechnet
   - Kompression wird auf der Protokollebene angewendet (I2NP, Streaming, SSU2)
   - Abwärtskompatibel mit allen Versionen seit 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity

**Beschreibung:** Identifiziert eindeutig einen router im I2P-Netzwerk. Identische Struktur wie KeysAndCert.

**Format:** Siehe die oben stehende KeysAndCert-Struktur

**Aktuelle Anforderungen (Stand: 0.9.58):**

1. **Erforderliche Schlüsseltypen:**
   - **Verschlüsselung:** X25519 (Typ 4, 32 Bytes)
   - **Signatur:** EdDSA_SHA512_Ed25519 (Typ 7, 32 Bytes)
   - **Zertifikat:** Key Certificate (Typ 5)

2. **Veraltete Schlüsseltypen:**
   - ElGamal (Typ 0) seit 0.9.58 für Router-Identitäten als veraltet markiert
   - DSA_SHA1 (Typ 0) seit 0.9.58 für Router-Identitäten als veraltet markiert
   - Diese sollten für neue Router NICHT verwendet werden

3. **Typische Größe:**
   - X25519 + EdDSA mit Schlüsselzertifikat = 391 Bytes
   - 32 Bytes X25519-öffentlicher Schlüssel
   - 320 Bytes Padding (Auffüllung) (komprimierbar gemäß [Proposal 161](/de/proposals/161-ri-dest-padding/))
   - 32 Bytes EdDSA-öffentlicher Schlüssel
   - 7 Bytes Zertifikat (3-Byte-Header + 4-Byte-Schlüsseltypen)

**Historische Entwicklung:** - Vor 0.9.16: Immer NULL-Zertifikat (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Unterstützung für Schlüsselzertifikate hinzugefügt - 0.9.48+: X25519-Verschlüsselungsschlüssel unterstützt - 0.9.58+: ElGamal und DSA_SHA1 als veraltet markiert

**Schlüssel der Netzwerkdatenbank:** - RouterInfo (Router-Informationsstruktur) indiziert durch den SHA-256-Hash der vollständigen RouterIdentity (Router-Identität) - Hash über die gesamte 391+ Byte große Struktur berechnet (einschließlich Padding)

**Siehe auch:** - Richtlinien zur Padding-Generierung ([Proposal 161](/de/proposals/161-ri-dest-padding/)) - Spezifikation des Schlüsselzertifikats oben

**JavaDoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Ziel

**Beschreibung:** Endpunkt-Identifikator für die sichere Nachrichtenübermittlung. Strukturell identisch mit KeysAndCert, aber mit anderer Nutzungssemantik.

**Format:** Siehe die obenstehende KeysAndCert-Struktur

**Wesentlicher Unterschied zu RouterIdentity (Router-Identität):** - **Das Feld für den öffentlichen Schlüssel ist UNBENUTZT und kann Zufallsdaten enthalten** - Dieses Feld wird seit Version 0.6 (2005) nicht mehr verwendet - War ursprünglich für die alte I2CP-zu-I2CP-Verschlüsselung vorgesehen (deaktiviert) - Wird derzeit nur als IV (Initialisierungsvektor) für die veraltete LeaseSet-Verschlüsselung verwendet

**Aktuelle Empfehlungen:**

1. **Signaturschlüssel:**
   - **Empfohlen:** EdDSA_SHA512_Ed25519 (Signaturalgorithmus; Typ 7, 32 Bytes)
   - Alternative: ECDSA-Typen für Kompatibilität mit älteren Systemen
   - Vermeiden: DSA_SHA1 (veraltet, nicht empfohlen)

2. **Verschlüsselungsschlüssel:**
   - Feld ist ungenutzt, muss aber vorhanden sein
   - **Empfohlen:** Mit Zufallsdaten gemäß [Proposal 161](/de/proposals/161-ri-dest-padding/) füllen (komprimierbar)
   - Größe: Immer 256 Byte (ElGamal-Slot, obwohl nicht für ElGamal verwendet)

3. **Zertifikat:**
   - NULL-Zertifikat für ElGamal + DSA_SHA1 (nur für Altkompatibilität)
   - Schlüsselzertifikat für alle anderen Signaturschlüsseltypen

**Typische moderne Destination (Zieladresse):**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Tatsächlicher Verschlüsselungsschlüssel:** - Der Verschlüsselungsschlüssel für die Destination (Zieladresse) befindet sich im **LeaseSet**, nicht in der Destination - LeaseSet enthält die aktuellen öffentlichen Verschlüsselungsschlüssel - Siehe die LeaseSet2-Spezifikation zum Umgang mit Verschlüsselungsschlüsseln

**Netzwerkdatenbank-Schlüssel:** - LeaseSet mit dem SHA-256-Hash der vollständigen Destination (Zieladresse) als Schlüssel - Hash berechnet über die gesamte Struktur von 387+ Byte

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Strukturen der Netzwerkdatenbank

### Lease (zeitlich befristete Zuweisung)

**Beschreibung:** Autorisiert einen bestimmten tunnel, Nachrichten für eine Destination (I2P-Zieladresse) zu empfangen. Teil des ursprünglichen LeaseSet-Formats (Typ 1).

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Gesamtgröße:** 44 Bytes

**Verwendung:** - Nur im ursprünglichen LeaseSet verwendet (Typ 1, veraltet) - Für LeaseSet2 und spätere Varianten stattdessen Lease2 verwenden

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Typ 1) (I2P-Datensatz mit Erreichbarkeitsinformationen eines Ziels)

**Beschreibung:** Ursprüngliches LeaseSet-Format. Enthält autorisierte tunnels und Schlüssel für eine Destination (Zieladresse). In der Netzwerkdatenbank gespeichert. **Status: Veraltet** (verwenden Sie stattdessen LeaseSet2).

**Struktur:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Datenbankspeicherung:** - **Datenbanktyp:** 1 - **Schlüssel:** SHA-256-Hash der Destination - **Wert:** Vollständige LeaseSet-Struktur

**Wichtige Hinweise:**

1. **Öffentlicher Schlüssel der Destination (Zieladresse in I2P) ungenutzt:**
   - Das Feld für den öffentlichen Verschlüsselungsschlüssel in der Destination ist ungenutzt
   - Der Verschlüsselungsschlüssel im LeaseSet ist der eigentliche Schlüssel für die Verschlüsselung

2. **Temporäre Schlüssel:**
   - `encryption_key` ist temporär (wird beim Start des router neu generiert)
   - `signing_key` ist temporär (wird beim Start des router neu generiert)
   - Keiner der beiden Schlüssel ist über Neustarts hinweg persistent

3. **Widerruf (nicht implementiert):**
   - `signing_key` war für den Widerruf von LeaseSets vorgesehen
   - Ein Widerrufsmechanismus wurde nie implementiert
   - Ein Zero-lease LeaseSet war für den Widerruf vorgesehen, wird aber nicht verwendet

4. **Versionierung/Zeitstempel:**
   - LeaseSet hat kein explizites `published`-Zeitstempelfeld
   - Die Version ist die früheste Ablaufzeit aller Leases (zeitlich begrenzte Tunnelendpunkte)
   - Ein neues LeaseSet muss eine frühere Lease-Ablaufzeit haben, um akzeptiert zu werden

5. **Veröffentlichung von Lease-Ablaufzeiten:**
   - Pre-0.9.7: Alle Leases (zeitlich begrenzte Zugriffsberechtigung auf einen tunnel) mit demselben Ablaufzeitpunkt veröffentlicht (dem frühesten)
   - 0.9.7+: Tatsächliche individuelle Lease-Ablaufzeiten veröffentlicht
   - Dies ist ein Implementierungsdetail und nicht Teil der Spezifikation

6. **Keine Leases:**
   - LeaseSet mit null Leases ist technisch zulässig
   - Vorgesehen für Widerruf (nicht implementiert)
   - In der Praxis nicht verwendet
   - LeaseSet2-Varianten erfordern mindestens ein Lease

**Veraltet:** LeaseSet Typ 1 ist veraltet. Neue Implementierungen sollten **LeaseSet2 (Typ 3)** verwenden, das Folgendes bietet: - Feld für Veröffentlichungszeitstempel (bessere Versionierung) - Unterstützung mehrerer Verschlüsselungsschlüssel - Unterstützung für Offline-Signaturen - 4-Byte-Lease-Ablaufzeiten (statt 8 Byte) - Flexiblere Optionen

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## LeaseSet-Varianten

### Lease2

**Beschreibung:** Verbesseres Lease-Format mit 4-Byte-Ablaufzeit. Wird in LeaseSet2 (Typ 3) und MetaLeaseSet (Typ 7) verwendet.

**Einführung:** Version 0.9.38 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Gesamtgröße:** 40 Bytes (4 Bytes kleiner als die ursprüngliche Lease (Eintrag mit Ablaufzeit))

**Vergleich mit der ursprünglichen Lease (zeitlich begrenzter Eintrag innerhalb eines leaseSet):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### OfflineSignature

**Beschreibung:** Optionale Struktur für vorab signierte temporäre Schlüssel, die die Veröffentlichung des LeaseSet ohne Online-Zugriff auf den privaten Signaturschlüssel der Destination (I2P-Zieladresse) ermöglicht.

**Einführung:** Version 0.9.38 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Zweck:** - Ermöglicht die Offline-Erzeugung eines LeaseSet - Schützt den Hauptschlüssel der Destination (I2P-Adresse) vor der Online-Offenlegung - Der temporäre Schlüssel kann durch die Veröffentlichung eines neuen LeaseSet ohne Offline-Signatur widerrufen werden

**Anwendungsfälle:**

1. **Hochsicherheits-Ziele:**
   - Master-Signaturschlüssel offline gespeichert (HSM, Offline-Speicherung)
   - Temporäre Schlüssel werden offline für begrenzte Zeiträume erzeugt
   - Ein kompromittierter temporärer Schlüssel legt den Master-Schlüssel nicht offen

2. **Verschlüsselte LeaseSet-Veröffentlichung:**
   - EncryptedLeaseSet (verschlüsseltes LeaseSet) kann eine Offline-Signatur enthalten
   - Verblindeter öffentlicher Schlüssel + Offline-Signatur bieten zusätzliche Sicherheit

**Sicherheitsüberlegungen:**

1. **Ablaufmanagement:**
   - Angemessene Ablaufzeiten festlegen (Tage bis Wochen, nicht Jahre)
   - Vor Ablauf neue temporäre Schlüssel erzeugen
   - Kürzere Ablaufzeit = bessere Sicherheit, mehr Wartungsaufwand

2. **Schlüsselerzeugung:**
   - Temporäre Schlüssel offline in einer sicheren Umgebung erzeugen
   - Mit dem Master-Schlüssel offline signieren
   - Nur den signierten temporären Schlüssel + die Signatur an den online router übertragen

3. **Widerruf:**
   - Einen neuen LeaseSet ohne Offline-Signatur veröffentlichen, um implizit zu widerrufen
   - Oder einen neuen LeaseSet mit anderem temporären Schlüssel veröffentlichen

**Signaturprüfung:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Implementierungshinweise:** - Die Gesamtgröße variiert je nach Signaturtyp und Typ des Signaturschlüssels der Destination (Zieladresse) - Mindestgröße: 4 + 2 + 32 (EdDSA-Schlüssel) + 64 (EdDSA-Signatur) = 102 Bytes - Maximal sinnvolle Größe: ~600 Bytes (RSA-4096 temporärer Schlüssel + RSA-4096 Signatur)

**Kompatibel mit:** - LeaseSet2 (Typ 3) - EncryptedLeaseSet (Typ 5) - MetaLeaseSet (Typ 7)

**Siehe auch:** [Vorschlag 123](/proposals/123-new-netdb-entries/) für Details zum Offline-Signaturprotokoll.

---

### LeaseSet2Header

**Beschreibung:** Gemeinsame Header-Struktur für LeaseSet2 (Typ 3) und MetaLeaseSet (Typ 7).

**Einführung:** Version 0.9.38 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Minimale Gesamtgröße:** 395 Bytes (ohne Offline-Signatur)

**Flag-Definitionen (Bitreihenfolge: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Flag-Details:**

**Bit 0 - Offline-Schlüssel:** - `0`: Keine Offline-Signatur; verwenden Sie den Signaturschlüssel der Destination (I2P-Zielidentität), um die LeaseSet-Signatur zu verifizieren - `1`: Die OfflineSignature-Struktur folgt auf das Flags-Feld

**Bit 1 - Unveröffentlicht:** - `0`: Standardmäßig veröffentlichter LeaseSet, sollte an die floodfills geflutet werden - `1`: Unveröffentlichter LeaseSet (nur clientseitig)   - Sollte NICHT geflutet, veröffentlicht oder als Antwort auf Anfragen gesendet werden   - Wenn abgelaufen, NICHT netdb nach Ersatz abfragen (es sei denn, Bit 2 ist ebenfalls gesetzt)   - Wird für lokale tunnels oder Tests verwendet

**Bit 2 - Geblindet (seit 0.9.42):** - `0`: Standard-LeaseSet - `1`: Dieses unverschlüsselte LeaseSet wird bei der Veröffentlichung geblindet und verschlüsselt   - Die veröffentlichte Version wird ein EncryptedLeaseSet (Typ 5) sein   - Falls abgelaufen, den **geblindeten Ort** in netdb als Ersatz abfragen   - Bit 1 muss ebenfalls auf 1 gesetzt werden (unveröffentlicht + geblindet)   - Wird für verschlüsselte versteckte Dienste verwendet

**Ablaufgrenzen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Anforderungen an den Veröffentlichungszeitstempel:**

LeaseSet (Typ 1) hatte kein published-Feld, sodass für die Versionierung nach dem frühesten Lease-Ablauf gesucht werden musste. LeaseSet2 fügt einen expliziten `published`-Zeitstempel mit 1-Sekunden-Auflösung hinzu.

**Kritischer Implementierungshinweis:** - Routers MÜSSEN die Veröffentlichung von LeaseSets pro Destination (I2P-Adresse) **deutlich langsamer als einmal pro Sekunde** drosseln - Wenn schneller veröffentlicht wird, sicherstellen, dass jedes neue LeaseSet eine `published`-Zeit hat, die mindestens 1 Sekunde später liegt - Floodfills werden ein LeaseSet ablehnen, wenn die `published`-Zeit nicht neuer ist als die aktuelle Version - Empfohlenes Mindestintervall: 10-60 Sekunden zwischen Veröffentlichungen

**Berechnungsbeispiele:**

**LeaseSet2 (max. 11 Minuten):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (max. 18,2 Stunden):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Versionierung:** - LeaseSet gilt als "neuer", wenn der `published`-Zeitstempel größer ist - Floodfills speichern und verteilen nur die neueste Version - Achte darauf, wenn die älteste Lease (Eintrag im LeaseSet) mit der ältesten Lease des vorherigen LeaseSets übereinstimmt

---

### LeaseSet2 (Typ 3)

**Beschreibung:** Modernes LeaseSet-Format mit mehreren Verschlüsselungsschlüsseln, Offline-Signaturen und Dienstdatensätzen. Aktueller Standard für versteckte Dienste in I2P.

**Einführung:** Version 0.9.38 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Struktur:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Datenbankspeicherung:** - **Datenbanktyp:** 3 - **Schlüssel:** SHA-256-Hash der Destination (Zieladresse in I2P) - **Wert:** Vollständige LeaseSet2-Struktur

**Signaturberechnung:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Bevorzugungsreihenfolge für Verschlüsselungsschlüssel

**Für veröffentlichtes (Server) LeaseSet:** - Schlüssel in der Reihenfolge der Serverpräferenz aufgeführt (mit höchster Präferenz zuerst) - Clients, die mehrere Typen unterstützen, SOLLTEN die Serverpräferenz befolgen - Wählen Sie den ersten unterstützten Typ aus der Liste aus - Im Allgemeinen sind höher nummerierte (neuere) Schlüsseltypen sicherer/effizienter - Empfohlene Reihenfolge: Schlüssel in umgekehrter Reihenfolge nach Typcode auflisten (neueste zuerst)

**Beispielhafte Servereinstellung:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Für ein unveröffentlichtes (Client) LeaseSet:** - Die Schlüsselreihenfolge spielt praktisch keine Rolle (Verbindungen zu Clients werden nur selten versucht) - Aus Konsistenzgründen die gleiche Konvention beibehalten

**Auswahl des Client-Schlüssels:** - Serverpräferenz respektieren (ersten unterstützten Typ auswählen) - Oder implementierungsdefinierte Präferenz verwenden - Oder kombinierte Präferenz auf Grundlage der Fähigkeiten beider Seiten ermitteln

### Zuordnung von Optionen

**Anforderungen:** - Optionen MÜSSEN nach Schlüssel sortiert sein (lexikografisch, UTF-8-Byte-Reihenfolge) - Die Sortierung gewährleistet die Signatur-Invarianz - Doppelte Schlüssel sind NICHT erlaubt

**Standardformat ([Vorschlag 167](/proposals/167-service-records/)):**

Seit API 0.9.66 (Juni 2025, Release 2.9.0) folgen Service-Record-Optionen einem standardisierten Format. Siehe [Proposal 167](/proposals/167-service-records/) für die vollständige Spezifikation.

**Format der Service-Record-Option:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Beispiel-Serviceeinträge:**

**1. Selbstreferenzierender SMTP-Server:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Einzelner externer SMTP-Server:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Mehrere SMTP-Server (Lastverteilung):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. HTTP-Dienst mit App-Optionen:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**TTL-Empfehlungen:** - Minimum: 86400 Sekunden (1 Tag) - Längere TTL verringert die netdb-Abfragelast - Abwägung zwischen Reduzierung von Abfragen und Verbreitung von Dienst-Updates - Für stabile Dienste: 604800 (7 Tage) oder länger

**Implementierungshinweise:**

1. **Verschlüsselungsschlüssel (Stand 0.9.44):**
   - ElGamal (Typ 0, 256 Byte): Abwärtskompatibilität
   - X25519 (Typ 4, 32 Byte): Aktueller Standard
   - MLKEM-Varianten: Post-Quanten-Kryptografie (Beta, noch nicht finalisiert)

2. **Validierung der Schlüssellänge:**
   - Floodfills und Clients MÜSSEN in der Lage sein, unbekannte Schlüsseltypen zu parsen
   - Verwenden Sie das Feld keylen, um unbekannte Schlüssel zu überspringen
   - Das Parsen darf nicht fehlschlagen, wenn der Schlüsseltyp unbekannt ist

3. **Veröffentlichungszeitstempel:**
   - Siehe Hinweise im LeaseSet2Header zur Ratenbegrenzung
   - Mindestens 1 Sekunde Abstand zwischen Veröffentlichungen
   - Empfohlen: 10–60 Sekunden zwischen Veröffentlichungen

4. **Migration des Verschlüsselungstyps:**
   - Mehrere Schlüssel ermöglichen eine schrittweise Migration
   - Während der Übergangsphase sowohl alte als auch neue Schlüssel auflisten
   - Alten Schlüssel nach ausreichend langer Client-Aktualisierungsphase entfernen

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease

**Beschreibung:** Lease-Struktur für MetaLeaseSet, die statt tunnels andere LeaseSets referenzieren kann. Wird für Lastverteilung und Redundanz verwendet.

**Einführung:** Version 0.9.38, geplant lauffähig ab 0.9.40 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Gesamtgröße:** 40 Bytes

**Eintragstyp (Flags-Bits 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Anwendungsszenarien:**

1. **Lastverteilung:**
   - MetaLeaseSet mit mehreren MetaLease-Einträgen
   - Jeder Eintrag verweist auf ein anderes LeaseSet2
   - Clients wählen basierend auf dem Kostenfeld

2. **Redundanz:**
   - Mehrere Einträge, die auf Backup-LeaseSets verweisen
   - Fallback, falls primäres LeaseSet nicht verfügbar ist

3. **Service-Migration:**
   - MetaLeaseSet (spezielle LeaseSet) verweist auf ein neues LeaseSet
   - Ermöglicht einen nahtlosen Übergang zwischen Destinations (I2P-Adressen)

**Verwendung des Cost-Felds:** - Niedrigerer Cost-Wert = höhere Priorität - Cost 0 = höchste Priorität - Cost 255 = niedrigste Priorität - Clients SOLLTEN Einträge mit niedrigerem Cost-Wert bevorzugen - Einträge mit gleichem Cost-Wert können zufällig lastverteilt werden

**Vergleich mit Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Typ 7)

**Beschreibung:** LeaseSet-Variante, die MetaLease-Einträge (spezielle I2P-Struktur für indirekte Verweise) enthält und damit indirekte Verweise auf andere LeaseSets bereitstellt. Wird für Lastverteilung, Redundanz und Dienstmigration eingesetzt.

**Einführung:** Definiert in 0.9.38, geplant ab 0.9.40 einsatzbereit (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Status:** Spezifikation abgeschlossen. Der Status des Produktiveinsatzes sollte anhand der aktuellen I2P-Versionen überprüft werden.

**Struktur:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Datenbankspeicherung:** - **Datenbanktyp:** 7 - **Schlüssel:** SHA-256-Hash der Destination (Zielkennung) - **Wert:** Vollständige MetaLeaseSet-Struktur (erweiterte leaseSet-Struktur)

**Signaturberechnung:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Anwendungsfälle:**

**1. Lastverteilung:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Ausfallsicherung:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Dienstmigration:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Mehrschichtarchitektur:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Widerrufsliste:**

Die Widerrufsliste ermöglicht es MetaLeaseSet, zuvor veröffentlichte LeaseSets explizit zu widerrufen:

- **Zweck:** Bestimmte Destinations als nicht mehr gültig markieren
- **Inhalt:** SHA-256-Hashes widerrufener Destination-Strukturen
- **Verwendung:** Clients DÜRFEN KEINE LeaseSets verwenden, deren Destination-Hash in der Widerrufsliste erscheint
- **Typischer Wert:** Leer (numr=0) in den meisten Bereitstellungen

**Beispiel für einen Widerruf:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Ablaufbehandlung:**

MetaLeaseSet (Metadatensatz für leaseSet) verwendet LeaseSet2Header mit maximalem expires=65535 Sekunden (~18,2 Stunden):

- Viel länger als LeaseSet2 (max. ~11 Minuten)
- Geeignet für relativ statische indirekte Referenzierung
- Referenzierte LeaseSets können eine kürzere Ablaufzeit haben
- Clients müssen die Ablaufzeit sowohl von MetaLeaseSet als auch von den referenzierten LeaseSets prüfen

**Zuordnung der Optionen:**

- Dasselbe Format wie bei den LeaseSet2-Optionen verwenden
- Kann service records (Servicedatensätze) enthalten ([Vorschlag 167](/proposals/167-service-records/))
- MUSS nach Schlüssel sortiert sein
- Service records beschreiben typischerweise den letztendlichen Dienst, nicht die Indirektionsstruktur

**Hinweise zur Client-Implementierung:**

1. **Ablauf der Auflösung:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Zwischenspeicherung:**
   - Sowohl MetaLeaseSet als auch referenzierte LeaseSets zwischenspeichern
   - Ablaufzeiten beider Ebenen prüfen
   - Veröffentlichung eines aktualisierten MetaLeaseSet beobachten

3. **Failover (Ausfallsicherung):**
   - Fällt der bevorzugte Eintrag aus, versuche den mit den nächstniedrigeren Kosten
   - Erwäge, ausgefallene Einträge vorübergehend als nicht verfügbar zu markieren
   - Regelmäßig erneut prüfen, ob sie wieder verfügbar sind

**Implementierungsstatus:**

[Proposal 123](/proposals/123-new-netdb-entries/) stellt fest, dass Teile noch "in Entwicklung" sind. Implementierende sollten: - Die Produktionsreife in der Zielversion von I2P überprüfen - Die Unterstützung für MetaLeaseSet vor der Bereitstellung testen - Auf aktualisierte Spezifikationen in neueren I2P-Versionen prüfen

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (verschlüsseltes LeaseSet, Typ 5)

**Beschreibung:** Verschlüsseltes und verblindetes LeaseSet für verbesserte Privatsphäre. Nur der verblindete öffentliche Schlüssel und die Metadaten sind sichtbar; die tatsächlichen leases (Lease-Einträge) und Verschlüsselungsschlüssel sind verschlüsselt.

**Einführung:** Definiert seit 0.9.38, funktionsfähig seit 0.9.39 (siehe [Vorschlag 123](/proposals/123-new-netdb-entries/))

**Struktur:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Datenbankspeicherung:** - **Datenbanktyp:** 5 - **Schlüssel:** SHA-256-Hash der **verblindeten Destination (Zieladresse)** (nicht die ursprüngliche Destination) - **Wert:** Vollständige EncryptedLeaseSet-Struktur

**Kritische Unterschiede gegenüber LeaseSet2:**

1. **Verwendet NICHT die LeaseSet2Header-Struktur (I2P-Strukturbezeichnung)** (hat ähnliche Felder, aber einen anderen Aufbau)
2. **Verblindeter öffentlicher Schlüssel** statt vollständiger Destination (I2P-Adresse)
3. **Verschlüsselte Nutzlast** statt Klartext-Leases und -Schlüssel
4. **Datenbankschlüssel ist der Hash der verblindeten Destination**, nicht der ursprünglichen Destination

**Signaturberechnung:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Anforderung an den Signaturtyp:**

**MUSS RedDSA_SHA512_Ed25519 (type 11) verwenden:** - Verblindete öffentliche Schlüssel mit 32 Byte - Signaturen mit 64 Byte - Erforderlich für die Sicherheitseigenschaften der Verblindung - Siehe [Red25519-Spezifikation](//docs/specs/red25519-signature-scheme/

**Wesentliche Unterschiede zu EdDSA:** - Private Schlüssel mittels modularer Reduktion (kein Clamping) - Signaturen enthalten 80 Byte Zufallsdaten - Verwendet öffentliche Schlüssel direkt (keine Hashes) - Ermöglicht eine sichere Verblindung

**Verblindung und Verschlüsselung:**

Ausführliche Informationen finden Sie in der [EncryptedLeaseSet-Spezifikation](/docs/specs/encryptedleaseset/):

**1. Schlüssel-Blindierung:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Speicherort der Datenbank:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Verschlüsselungsschichten (drei Schichten):**

**Schicht 1 - Authentifizierungsschicht (Client-Zugriff):** - Verschlüsselung: ChaCha20-Stromchiffre - Schlüsselableitung: HKDF mit clientspezifischen Geheimnissen - Authentifizierte Clients können die äußere Schicht entschlüsseln

**Schicht 2 - Verschlüsselungsschicht:** - Verschlüsselung: ChaCha20 - Schlüssel: Abgeleitet aus DH (Diffie-Hellman-Schlüsselaustausch) zwischen Client und Server - Enthält das eigentliche LeaseSet2 oder MetaLeaseSet

**Schicht 3 - Inneres LeaseSet (Datensatz mit Adressen und Schlüsseln in I2P):** - Vollständiges LeaseSet2 oder MetaLeaseSet - Enthält alle tunnels, Verschlüsselungsschlüssel, Optionen - Nur nach erfolgreicher Entschlüsselung zugänglich

**Ableitung des Verschlüsselungsschlüssels:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Erkennungsprozess:**

**Für autorisierte Clients:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Für nicht autorisierte Clients:** - Können nicht entschlüsseln, selbst wenn sie den EncryptedLeaseSet (verschlüsselter LeaseSet) finden - Können die ursprüngliche Destination (Zieladresse) nicht aus der blinded version (verschleierte Version) bestimmen - Können EncryptedLeaseSets nicht über verschiedene blinding periods (Verschleierungszeiträume) hinweg verknüpfen (tägliche Rotation)

**Ablaufzeiten:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Veröffentlichter Zeitstempel:**

Gleiche Anforderungen wie bei LeaseSet2Header: - Muss sich zwischen Veröffentlichungen um mindestens 1 Sekunde erhöhen - Floodfills lehnen ab, wenn nicht neuer als die aktuelle Version - Empfohlen: 10-60 Sekunden zwischen Veröffentlichungen

**Offline-Signaturen mit verschlüsselten LeaseSets:**

Besondere Hinweise bei der Verwendung von Offline-Signaturen: - Der verblindete öffentliche Schlüssel rotiert täglich - Die Offline-Signatur muss täglich mit einem neuen verblindeten Schlüssel neu erstellt werden - ODER die Offline-Signatur auf dem inneren LeaseSet verwenden, nicht auf dem äußeren EncryptedLeaseSet - Siehe Hinweise zu [Proposal 123](/proposals/123-new-netdb-entries/) notes

**Implementierungshinweise:**

1. **Client-Autorisierung:**
   - Mehrere Clients können mit unterschiedlichen Schlüsseln autorisiert werden
   - Jeder autorisierte Client hat eindeutige Entschlüsselungs-Anmeldedaten
   - Zugriff eines Clients widerrufen, indem die Autorisierungsschlüssel geändert werden

2. **Tägliche Schlüsselrotation:**
   - Verblindete Schlüssel ändern sich um Mitternacht UTC
   - Clients müssen die verblindete Destination (I2P-Adresse) täglich neu berechnen
   - Alte EncryptedLeaseSets werden nach der Rotation nicht mehr auffindbar

3. **Datenschutzeigenschaften:**
   - Floodfills können die ursprüngliche Destination (Ziel-Adresse) nicht bestimmen
   - Nicht autorisierte Clients können nicht auf den Dienst zugreifen
   - Verschiedene blinding periods (Verschleierungszeiträume) können nicht miteinander verknüpft werden
   - Keine Klartext-Metadaten außer den Ablaufzeiten

4. **Leistung:**
   - Clients müssen täglich eine Blinding-Berechnung (Verblindung) durchführen
   - Dreischichtige Verschlüsselung erhöht den Rechenaufwand
   - Erwägen Sie, das entschlüsselte innere LeaseSet zwischenzuspeichern

**Sicherheitsüberlegungen:**

1. **Verwaltung von Autorisierungsschlüsseln:**
   - Berechtigungsnachweise für Clients sicher verteilen
   - Pro Client eindeutige Berechtigungsnachweise verwenden, um einen feingranularen Widerruf zu ermöglichen
   - Autorisierungsschlüssel regelmäßig rotieren

2. **Zeitsynchronisierung:**
   - Tägliches blinding (Verblindung) hängt vom synchronisierten UTC-Tagesdatum ab
   - Uhrabweichungen können zu Abfragefehlern führen
   - Erwägen Sie, das blinding des vorherigen/nächsten Tages zu unterstützen, um Toleranzen auszugleichen

3. **Metadaten-Leckage:**
   - Die Felder Published und expires liegen im Klartext vor
   - Musteranalyse kann Merkmale des Dienstes offenlegen
   - Veröffentlichungsintervalle zufällig variieren, wenn Bedenken bestehen

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Router-Strukturen

### RouterAddress

**Beschreibung:** Definiert Verbindungsinformationen für einen router mittels eines bestimmten Transportprotokolls.

**Format:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**KRITISCH - Ablauf-Feld:**

⚠️ **Das Ablauf-Feld MUSS auf lauter Nullen gesetzt werden (8 Null-Bytes).**

- **Grund:** Seit Version 0.9.3 führt eine von Null abweichende Ablaufzeit zu einem Fehler bei der Signaturprüfung
- **Historie:** Die Ablaufzeit wurde ursprünglich nicht verwendet, stets null
- **Aktueller Status:** Das Feld wird seit 0.9.12 wieder berücksichtigt, muss jedoch auf ein Netzwerk-Upgrade warten
- **Implementierung:** Immer auf 0x0000000000000000 setzen

Jede von Null verschiedene Ablaufzeit führt dazu, dass die RouterInfo-Signatur bei der Validierung fehlschlägt.

### Transportprotokolle

**Aktuelle Protokolle (Stand: 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Transportstil-Werte:** - `"SSU2"`: Aktueller UDP-basierter Transport - `"NTCP2"`: Aktueller TCP-basierter Transport - `"NTCP"`: Veraltet, entfernt (nicht verwenden) - `"SSU"`: Veraltet, entfernt (nicht verwenden)

### Allgemeine Optionen

Alle Transportprotokolle umfassen typischerweise:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### SSU2-spezifische Optionen

Ausführliche Informationen finden Sie in der [SSU2-Spezifikation](/docs/specs/ssu2/).

**Erforderliche Optionen:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Optionale Optionen:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Beispiel SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### NTCP2-spezifische Optionen

Ausführliche Details finden Sie in der [NTCP2-Spezifikation](/docs/specs/ntcp2/).

**Erforderliche Optionen:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Optionale Einstellungen (seit 0.9.50):**

```
"caps" = Capability string
```
**Beispiel für eine NTCP2 RouterAddress (Router-Adresse):**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Implementierungshinweise

1. **Kostenwerte:**
   - UDP (SSU2) typischerweise geringere Kosten (5-6) aufgrund der Effizienz
   - TCP (NTCP2) typischerweise höhere Kosten (10-11) aufgrund des Overheads
   - Niedrigere Kosten = bevorzugter Transport

2. **Mehrere Adressen:**
   - Router können mehrere RouterAddress-Einträge veröffentlichen
   - Verschiedene Transportprotokolle (SSU2 und NTCP2)
   - Verschiedene IP-Versionen (IPv4 und IPv6)
   - Clients wählen anhand von Kosten und Fähigkeiten

3. **Hostname gegenüber IP:**
   - IP-Adressen werden aus Leistungsgründen bevorzugt
   - Hostnamen werden unterstützt, verursachen jedoch zusätzlichen Aufwand durch DNS-Lookups
   - Erwägen Sie die Verwendung von IP für veröffentlichte RouterInfos (Router-Informationen)

4. **Base64-Kodierung:**
   - Alle Schlüssel und Binärdaten in Base64 kodiert
   - Standard-Base64 (RFC 4648)
   - Kein Padding und keine nicht standardkonformen Zeichen

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo (Router-Informationen)

**Beschreibung:** Vollständige, veröffentlichte Informationen über einen router, die in der Netzwerkdatenbank gespeichert sind. Enthält Identität, Adressen und Fähigkeiten.

**Format:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Datenbankspeicherung:** - **Datenbanktyp:** 0 - **Schlüssel:** SHA-256-Hash von RouterIdentity - **Wert:** vollständige RouterInfo-Struktur

**Veröffentlichter Zeitstempel:** - 8-Byte-Datum (Millisekunden seit der Unix-Epoche) - Wird für die Versionierung von RouterInfo verwendet - Routers veröffentlichen periodisch eine neue RouterInfo - Floodfills behalten die neueste Version basierend auf dem veröffentlichten Zeitstempel

**Adresssortierung:** - **Historisch:** Sehr alte routers erforderten, dass Adressen nach dem SHA-256 ihrer Daten sortiert wurden - **Aktuell:** Sortierung NICHT erforderlich, Implementierung zur Kompatibilität lohnt sich nicht - Adressen können in beliebiger Reihenfolge vorliegen

**Feld für Peer-Größe (historisch):** - **Immer 0** im modernen I2P - War für eingeschränkte Routen vorgesehen (nicht implementiert) - Wenn implementiert, würden in entsprechender Anzahl Router-Hashes folgen - Einige alte Implementierungen könnten eine sortierte Peer-Liste verlangt haben

**Zuordnung der Optionen:**

Optionen MÜSSEN nach Schlüssel sortiert sein. Zu den Standardoptionen gehören:

**Fähigkeitsoptionen:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Netzwerkoptionen:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Statistische Optionen:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Siehe [Dokumentation zu RouterInfo der Netzwerkdatenbank](/docs/specs/common-structures/#routerInfo) für die vollständige Liste der Standardoptionen.

**Signaturberechnung:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**Typische moderne RouterInfo (Router-Informationen):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Implementierungshinweise:**

1. **Mehrere Adressen:**
   - Router veröffentlichen in der Regel 1-4 Adressen
   - IPv4- und IPv6-Varianten
   - SSU2- und/oder NTCP2-Transporte
   - Jede Adresse ist unabhängig

2. **Versionierung:**
   - Eine neuere RouterInfo hat einen späteren `published`-Zeitstempel
   - Routers veröffentlichen etwa alle ~2 Stunden erneut oder wenn sich Adressen ändern
   - Floodfills (spezielle router, die netDb-Daten speichern und verteilen) speichern und verbreiten nur die neueste Version

3. **Validierung:**
   - Signatur prüfen, bevor RouterInfo (I2P-Router-Informationsdatensatz) akzeptiert wird
   - Prüfen, dass das Ablaufzeit-Feld in jeder RouterAddress (I2P-Routeradresse) nur aus Nullen besteht
   - Validieren, dass die Optionszuordnung nach Schlüssel sortiert ist
   - Prüfen, dass Zertifikat- und Schlüsseltypen bekannt und unterstützt sind

4. **Netzwerkdatenbank:**
   - Floodfills speichern RouterInfo, indiziert durch Hash(RouterIdentity)
   - Für ~2 Tage nach der letzten Veröffentlichung vorgehalten
   - Routers fragen floodfills ab, um andere routers zu entdecken

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Hinweise zur Implementierung

### Byte-Reihenfolge (Endianness)

**Standard: Big-Endian (Netzwerk-Byte-Reihenfolge)**

Die meisten I2P-Strukturen verwenden die Big-Endian-Byte-Reihenfolge: - Alle Integer-Typen (1-8 Bytes) - Zeitstempel (Datum) - TunnelId - String-Längenpräfix - Zertifikatstypen und -längen - Schlüsseltyp-Codes - Felder für Mapping-Größen

**Ausnahme: Little-Endian (Byte-Reihenfolge mit kleinstwertigem Byte zuerst)**

Die folgenden Schlüsseltypen verwenden die **Little-Endian**-Kodierung: - **X25519** Verschlüsselungsschlüssel (Typ 4) - **EdDSA_SHA512_Ed25519** Signaturschlüssel (Typ 7) - **EdDSA_SHA512_Ed25519ph** Signaturschlüssel (Typ 8) - **RedDSA_SHA512_Ed25519** Signaturschlüssel (Typ 11)

**Implementierung:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Versionierung von Strukturen

**Niemals feste Größen voraussetzen:**

Viele Strukturen haben variable Länge: - RouterIdentity (Router-Identität): 387+ Bytes (nicht immer 387) - Destination (Zieladresse): 387+ Bytes (nicht immer 387) - LeaseSet2 (LeaseSet der zweiten Generation): Variiert erheblich - Zertifikat: 3+ Bytes

**Immer Längenfelder lesen:** - Zertifikatslänge in den Bytes 1-2 - Größe des Mappings am Anfang - KeysAndCert berechnet sich immer als 384 + 3 + certificate_length

**Auf überschüssige Daten prüfen:** - Nach gültigen Strukturen nachgestellten Datenmüll verbieten - Validieren, dass die Zertifikatlängen den Schlüsseltypen entsprechen - Exakte erwartete Längen für Typen fester Größe erzwingen

### Aktuelle Empfehlungen (Oktober 2025)

**Für neue Router-Identitäten:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/de/proposals/161-ri-dest-padding/)
```
**Für neue Ziele:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/de/proposals/161-ri-dest-padding/)
```
**Für neue LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Für verschlüsselte Dienste:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Veraltete Funktionen - Nicht verwenden

**Veraltete Verschlüsselung:** - ElGamal (Typ 0) für Router-Identitäten (seit 0.9.58 veraltet) - ElGamal/AES+SessionTag-Verschlüsselung (verwenden Sie ECIES-X25519)

**Veraltete Signaturverfahren:** - DSA_SHA1 (Typ 0) für Router-Identitäten (seit 0.9.58 veraltet) - ECDSA-Varianten (Typen 1-3) für neue Implementierungen - RSA-Varianten (Typen 4-6) außer für SU3-Dateien

**Veraltete Netzwerkformate:** - LeaseSet Typ 1 (verwenden Sie LeaseSet2) - Lease (44 Bytes, verwenden Sie Lease2) - Ursprüngliches Lease-Ablaufformat

**Veraltete Transporte:** - NTCP (in 0.9.50 entfernt) - SSU (in 2.4.0 entfernt)

**Veraltete Zertifikate:** - HASHCASH (Typ 1) - HIDDEN (Typ 2) - SIGNED (Typ 3) - MULTIPLE (Typ 4)

### Sicherheitsaspekte

**Schlüsselgenerierung:** - Verwenden Sie stets kryptografisch sichere Zufallszahlengeneratoren - Verwenden Sie Schlüssel niemals wieder in unterschiedlichen Kontexten - Schützen Sie private Schlüssel mit geeigneten Zugriffskontrollen - Löschen Sie Schlüsselmaterial nach Gebrauch sicher aus dem Speicher

**Signaturprüfung:** - Signaturen immer prüfen, bevor Sie Daten vertrauen - Prüfen, dass die Signaturlänge dem Schlüsseltyp entspricht - Prüfen, dass die signierten Daten die erwarteten Felder enthalten - Bei sortierten Zuordnungen die Sortierreihenfolge vor dem Signieren/Verifizieren prüfen

**Zeitstempelvalidierung:** - Überprüfen, dass veröffentlichte Zeiten plausibel sind (nicht weit in der Zukunft) - Validieren, dass Lease-Ablaufzeiten nicht abgelaufen sind - Toleranz für Uhrenabweichung berücksichtigen (typisch ±30 Sekunden)

**Netzwerkdatenbank:** - Alle Strukturen vor dem Speichern validieren - Größenbeschränkungen durchsetzen, um DoS zu verhindern - Anfragen und Veröffentlichungen ratenbegrenzen - Überprüfen, dass die Datenbankschlüssel mit den Struktur-Hashes übereinstimmen

### Kompatibilitätshinweise

**Abwärtskompatibilität:** - ElGamal und DSA_SHA1 werden weiterhin für ältere routers unterstützt - Veraltete Schlüsseltypen bleiben funktionsfähig, werden jedoch nicht empfohlen - Komprimierbares Padding ([Proposal 161](/de/proposals/161-ri-dest-padding/)) abwärtskompatibel bis Version 0.6

**Vorwärtskompatibilität:** - Unbekannte Schlüsseltypen können anhand von Längenfeldern geparst werden - Unbekannte Zertifikatstypen können anhand der Länge übersprungen werden - Unbekannte Signaturtypen sollten fehlertolerant behandelt werden - Implementierungen sollten bei unbekannten optionalen Funktionen nicht fehlschlagen

**Migrationsstrategien:** - Während der Übergangsphase sowohl alte als auch neue Schlüsseltypen unterstützen - LeaseSet2 kann mehrere Verschlüsselungsschlüssel auflisten - Offline-Signaturen ermöglichen eine sichere Schlüsselrotation - MetaLeaseSet ermöglicht eine transparente Dienstmigration

### Tests und Validierung

**Strukturvalidierung:** - Überprüfen, ob alle Längenfelder innerhalb der erwarteten Bereiche liegen - Prüfen, dass Strukturen variabler Länge korrekt geparst werden - Validieren, dass Signaturen erfolgreich verifiziert werden - Mit Strukturen in Minimal- und Maximalgröße testen

**Randfälle:** - Zeichenketten der Länge Null - Leere Zuordnungen - Minimale und maximale Lease-Anzahlen (Lease: zeitlich begrenzter Eintrag in einem leaseSet) - Zertifikat mit Nutzlast der Länge Null - Sehr große Strukturen (nahe den maximalen Größen)

**Interoperabilität:** - Gegen die offizielle Java I2P-Implementierung testen - Kompatibilität mit i2pd prüfen - Mit verschiedenen netDb-Inhalten testen - Anhand bekannter gültiger Testvektoren validieren

---

## Referenzen

### Spezifikationen

- [I2NP-Protokoll](/docs/specs/i2np/)
- [I2CP-Protokoll](/docs/specs/i2cp/)
- [SSU2-Transport](/docs/specs/ssu2/)
- [NTCP2-Transport](/docs/specs/ntcp2/)
- [Tunnel-Protokoll](/docs/specs/implementation/)
- [Datagramm-Protokoll](/docs/api/datagrams/)

### Kryptographie

- [Kryptografie-Überblick](/docs/specs/cryptography/)
- [ElGamal/AES-Verschlüsselung](/docs/legacy/elgamal-aes/)
- [ECIES-X25519-Verschlüsselung](/docs/specs/ecies/)
- [ECIES für Router](/docs/specs/ecies/#routers)
- [ECIES-Hybrid (Post-Quanten)](/docs/specs/ecies/#hybrid)
- [Red25519-Signaturen](/docs/specs/red25519-signature-scheme/)
- [Verschlüsseltes LeaseSet](/docs/specs/encryptedleaseset/)

### Vorschläge

- [Vorschlag 123: Neue netDB-Einträge](/proposals/123-new-netdb-entries/)
- [Vorschlag 134: GOST-Signaturtypen](/proposals/134-gost/)
- [Vorschlag 136: Experimentelle Signaturtypen](/proposals/136-experimental-sigtypes/)
- [Vorschlag 145: ECIES-P256](/proposals/145-ecies/)
- [Vorschlag 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Vorschlag 161: Padding-Generierung](/de/proposals/161-ri-dest-padding/)
- [Vorschlag 167: Service-Einträge](/proposals/167-service-records/)
- [Vorschlag 169: Post-Quanten-Kryptografie](/proposals/169-pq-crypto/)
- [Index aller Vorschläge](/proposals/)

### Netzwerkdatenbank

- [Übersicht über die Network Database (Netzwerkdatenbank)](/docs/specs/common-structures/)
- [Standardoptionen für RouterInfo](/docs/specs/common-structures/#routerInfo)

### JavaDoc-API-Referenz

- [Kern-Daten-Paket](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Externe Standards

- **RFC 7748 (X25519):** Elliptische Kurven für Sicherheitszwecke
- **RFC 7539 (ChaCha20):** ChaCha20 und Poly1305 für IETF-Protokolle
- **RFC 4648 (Base64):** Die Datenkodierungen Base16, Base32 und Base64
- **FIPS 180-4 (SHA-256):** Sicherer Hash-Standard
- **FIPS 204 (ML-DSA):** Modul-Gitter-basierter Standard für digitale Signaturen
- [IANA-Diensteregister](http://www.dns-sd.org/ServiceTypes.html)

### Community-Ressourcen

- [I2P-Website](/)
- [I2P-Forum](https://i2pforum.net)
- [I2P-GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [I2P-GitHub-Spiegel](https://github.com/i2p/i2p.i2p)
- [Index der technischen Dokumentation](/docs/)

### Release-Informationen

- [I2P 2.10.0 Veröffentlichung](/de/blog/2025/09/08/i2p-2.10.0-release/)
- [Versionsgeschichte](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Änderungsprotokoll](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Anhang: Schnellreferenztabellen

### Kurzreferenz zu Schlüsseltypen

**Aktueller Standard (empfohlen für alle neuen Implementierungen):** - **Verschlüsselung:** X25519 (Typ 4, 32 Bytes, Little-Endian (Byte-Reihenfolge mit niederwertigem Byte zuerst)) - **Signierung:** EdDSA_SHA512_Ed25519 (Typ 7, 32 Bytes, Little-Endian)

**Legacy (unterstützt, aber veraltet):** - **Verschlüsselung:** ElGamal (Typ 0, 256 Byte, Big-Endian) - **Signatur:** DSA_SHA1 (Typ 0, 20-Byte privat / 128-Byte öffentlich, Big-Endian)

**Spezialisiert:** - **Signierung (Verschlüsselte LeaseSet):** RedDSA_SHA512_Ed25519 (Typ 11, 32 Byte, little-endian)

**Post-Quanten (Beta, noch nicht final):** - **Hybride Verschlüsselung:** MLKEM_X25519-Varianten (Typen 5-7) - **Reine Post-Quanten-Verschlüsselung:** MLKEM-Varianten (noch keine zugewiesenen Typcodes)

### Kurzreferenz zu Strukturgrößen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Kurzreferenz zu Datenbanktypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Kurzreferenz zum Transportprotokoll

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Schnellreferenz zu Versionsmeilensteinen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/de/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
