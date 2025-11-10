---
title: "Akademische Forschung"
description: "Informationen und Richtlinien für die akademische Forschung im I2P-Netzwerk"
layout: "research"
aliases:
  - /en/research
  - /en/research/index
  - /en/research/questions
---

<div id="intro"></div>

## I2P Akademische Forschung

Es gibt eine große Forschungs-Community, die eine breite Palette von Anonymitätsaspekten untersucht. Um Anonymitätsnetzwerke weiter zu verbessern, halten wir es für wichtig, die bestehenden Probleme zu verstehen. Die Forschung im I2P-Netzwerk steckt noch in den Kinderschuhen, wobei sich die bisherige Arbeit stark auf andere Anonymitätsnetzwerke konzentriert hat. Dies bietet eine einzigartige Gelegenheit für originelle Forschungsbeiträge.

<div id="notes"></div>

## Hinweise an Forscher

### Prioritäten für defensive Forschung

Wir begrüßen Forschung, die uns hilft, das Netzwerk zu stärken und seine Sicherheit zu verbessern. Tests, die die I2P-Infrastruktur stärken, sind erwünscht und werden geschätzt.

### Kommunikationsrichtlinien für Forscher

Wir ermutigen Forscher dringend, ihre Forschungsideen frühzeitig mit dem Entwicklungsteam zu kommunizieren. Dies hilft:

- Potenzielle Überschneidungen mit bestehenden Projekten zu vermeiden
- Mögliche Schäden für das Netzwerk zu minimieren
- Test- und Datenerfassungsbemühungen zu koordinieren
- Sicherzustellen, dass die Forschung mit den Netzwerkzielen übereinstimmt

<div id="ethics"></div>

## Forschungsethik & Testleitlinien

### Allgemeine Grundsätze

Beim Forschen im I2P-Netzwerk bitte Folgendes beachten:

1. **Nutzen vs. Risiken der Forschung abwägen** - Überlegen, ob der potenzielle Nutzen Ihrer Forschung eventuelle Risiken für das Netzwerk oder seine Nutzer überwiegt
2. **Testnetz dem Live-Netz vorziehen** - Verwenden Sie nach Möglichkeit die Testnetzkonfiguration von I2P
3. **Nur notwendige Daten sammeln** - Nur die Mindestmenge an Daten sammeln, die für Ihre Forschung benötigt wird
4. **Veröffentlichte Daten sollen die Privatsphäre der Nutzer respektieren** - Alle veröffentlichten Daten sollten anonymisiert werden und die Privatsphäre der Nutzer respektieren

### Netzwerktestmethoden

Für Forscher, die im I2P testen müssen:

- **Testnetzkonfiguration verwenden** - I2P kann so konfiguriert werden, dass es auf einem isolierten Testnetz läuft
- **MultiRouter-Modus nutzen** - Mehrere Router-Instanzen auf einer einzelnen Maschine zum Testen betreiben
- **Router-Familie konfigurieren** - Ihre Forschungsrouter identifizierbar machen, indem Sie sie als Router-Familie konfigurieren

### Empfohlene Praktiken

- **Kontakt mit dem I2P-Team vor Tests im Live-Netz aufnehmen** - Kontaktieren Sie uns unter research@i2p.net, bevor Sie Tests im Live-Netz durchführen
- **Router-Familien-Konfiguration verwenden** - Dies macht Ihre Forschungsrouter für das Netzwerk transparent
- **Potenzielle Netzwerkstörungen vermeiden** - Tests so gestalten, dass negative Auswirkungen auf normale Nutzer minimiert werden

<div id="questions"></div>

## Offene Forschungsfragen

Die I2P-Community hat mehrere Bereiche identifiziert, in denen Forschung besonders wertvoll wäre:

### Netzwerkdatenbank

**Floodfills:**
- Gibt es andere Möglichkeiten, ein Brute-Forcing des Netzwerks durch erhebliche Kontrolle über Floodfills zu verhindern?
- Gibt es eine Möglichkeit, 'schlechte Floodfills' zu erkennen, zu kennzeichnen und möglicherweise zu entfernen, ohne dass dabei auf eine Form zentraler Autorität zurückgegriffen werden muss?

### Transports

- Wie könnten Paket-Neuübertragungsstrategien und Timeouts verbessert werden?
- Gibt es eine Möglichkeit, dass I2P Pakete obfuskiert und die Verkehrsanalyse effizienter reduziert?

### Tunnel und Ziele

**Peer-Auswahl:**
- Gibt es einen Weg, wie I2P die Peer-Auswahl effizienter oder sicherer durchführen könnte?
- Würde die Verwendung von GeoIP zur Priorisierung nahegelegener Peers die Anonymität negativ beeinflussen?

**Unidirektionale Tunnel:**
- Was sind die Vorteile unidirektionaler Tunnel gegenüber bidirektionalen Tunneln?
- Was sind die Kompromisse zwischen unidirektionalen und bidirektionalen Tunneln?

**Multihoming:**
- Wie effektiv ist Multihoming beim Lastenausgleich?
- Wie skaliert es?
- Was passiert, wenn mehr Router dasselbe Ziel hosten?
- Was sind die Anonymitätskompromisse?

### Nachrichtenweiterleitung

- Um wie viel wird die Effektivität von Timing-Angriffen durch Fragmentierung und Mischung von Nachrichten reduziert?
- Von welchen Mischstrategien könnte I2P profitieren?
- Wie können Hochlatenztechniken effektiv innerhalb oder neben unserem Niedriglatenznetzwerk eingesetzt werden?

### Anonymität

- Wie stark beeinträchtigt das Browser-Fingerprinting die Anonymität von I2P-Nutzern?
- Würde die Entwicklung eines Browser-Pakets den durchschnittlichen Nutzern zugutekommen?

### Netzwerkbezogen

- Welche Gesamtwirkung haben 'gierige Benutzer' auf das Netzwerk?
- Wären zusätzliche Schritte zur Förderung der Bandbreitenbeteiligung wertvoll?

<div id="contact"></div>

## Kontakt

Für Forschungsanfragen, Kooperationsmöglichkeiten oder um Ihre Forschungspläne zu besprechen, kontaktieren Sie uns bitte unter:

**Email:** research@i2p.net

Wir freuen uns darauf, mit der Forschungsgemeinschaft zusammenzuarbeiten, um das I2P-Netzwerk zu verbessern!