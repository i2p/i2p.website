---
title: "Verfahren zur Behandlung von Sicherheitslücken"
description: "I2Ps Verfahren zur Meldung und Reaktion auf Sicherheitslücken"
layout: "security-response"
---

<div id="contact"></div>

## Eine Sicherheitslücke melden

Haben Sie ein Sicherheitsproblem entdeckt? Melden Sie es an **security@i2p.net** (PGP empfohlen)

<a href="/keys/i2p-security-public.asc" download class="pgp-key-btn">PGP-Schlüssel herunterladen</a> | GPG-Schlüsselfingerabdruck: `40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941`

<div id="guidelines"></div>

## Forschungsrichtlinien

**Bitte NICHT:**
- Das aktive I2P-Netzwerk ausnutzen
- Social Engineering durchführen oder I2P-Infrastruktur angreifen
- Dienste für andere Nutzer stören

**Bitte:**
- Isolierte Testnetzwerke verwenden, wenn möglich
- Praktiken der koordinierten Offenlegung befolgen
- Uns vor Tests im aktiven Netzwerk kontaktieren

<div id="process"></div>

## Reaktionsprozess

### 1. Meldung eingegangen
- Antwort innerhalb von **3 Arbeitstagen**
- Antwortleiter zugewiesen
- Schweregradklassifikation (HOCH/MITTEL/NIEDRIG)

### 2. Untersuchung & Entwicklung
- Private Patch-Entwicklung über verschlüsselte Kanäle
- Tests im isolierten Netzwerk
- **HOHE Schweregrad:** Öffentliche Benachrichtigung innerhalb von 3 Tagen (keine Exploit-Details)

### 3. Veröffentlichung & Offenlegung
- Sicherheitsupdate bereitgestellt
- **90 Tage maximale** Frist zur vollständigen Offenlegung
- Optionale Forscheranerkennung in Ankündigungen

### Schweregradstufen

**HOCH** - Netzwerkweite Auswirkungen, sofortige Aufmerksamkeit erforderlich
**MITTEL** - Einzelne Router, zielgerichtete Ausnutzung
**NIEDRIG** - Begrenzte Auswirkungen, theoretische Szenarien

<div id="communication"></div>

## Sichere Kommunikation

Für alle Sicherheitsberichte PGP/GPG-Verschlüsselung verwenden:

```
Fingerabdruck: 40DF FE20 7D79 9BEC 3AE8 7DEA 5F98 BE91 176E 1941
```

In Ihrem Bericht enthalten:
- Detaillierte technische Beschreibung
- Schritte zur Reproduktion
- Proof-of-Concept-Code (falls zutreffend)

<div id="timeline"></div>

## Zeitplan

| Phase | Zeitrahmen |
|-------|------------|
| Erste Antwort | 0-3 Tage |
| Untersuchung | 1-2 Wochen |
| Entwicklung & Testen | 2-6 Wochen |
| Veröffentlichung | 6-12 Wochen |
| Volle Offenlegung | Maximal 90 Tage |

<div id="faq"></div>

## FAQ

**Werde ich Ärger bekommen, wenn ich berichte?**
Nein. Ein verantwortungsvolles Melden wird geschätzt und geschützt.

**Kann ich im aktiven Netzwerk testen?**
Nein. Verwenden Sie nur isolierte Testnetzwerke.

**Kann ich anonym bleiben?**
Ja, obwohl dies die Kommunikation erschweren kann.

**Gibt es eine Bug-Bounty?**
Derzeit nicht. I2P wird ehrenamtlich mit eingeschränkten Ressourcen betrieben.

<div id="examples"></div>

## Was melden

**Im Geltungsbereich:**
- I2P-Router-Schwachstellen
- Protokoll- oder Kryptographieprobleme
- Angriffe auf Netzwerkebene
- De-Anonymisierungstechniken
- Denial-of-Service-Probleme

**Außerhalb des Geltungsbereichs:**
- Anwendungen von Drittanbietern (Entwickler kontaktieren)
- Social Engineering oder physische Angriffe
- Bekannte/offengelegte Schwachstellen
- Rein theoretische Probleme

---

**Danke, dass Sie helfen, I2P sicher zu halten!**