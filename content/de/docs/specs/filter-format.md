---
title: "Zugriffsfilter-Format"
description: "Syntax für Zugriffskontroll-Filterdateien für tunnel"
slug: "filter-format"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Zugriffsfilter ermöglichen I2PTunnel-Serverbetreibern, eingehende Verbindungen basierend auf der Quell-Destination (Zieladresse) und der zuletzt beobachteten Verbindungsrate zu erlauben, zu verweigern oder zu drosseln. Der Filter ist eine einfache Textdatei mit Regeln. Die Datei wird von oben nach unten gelesen und die **erste passende Regel gewinnt**.

> Änderungen an der Filterdefinition werden **beim tunnel-Neustart** wirksam. Einige Builds lesen dateibasierte Listen möglicherweise zur Laufzeit erneut ein, aber planen Sie einen Neustart ein, um zu gewährleisten, dass die Änderungen angewendet werden.

## Dateiformat

- Eine Regel pro Zeile.  
- Leere Zeilen werden ignoriert.  
- `#` beginnt einen Kommentar, der bis zum Ende der Zeile reicht.  
- Regeln werden der Reihe nach ausgewertet; die erste Übereinstimmung wird verwendet.

## Schwellenwerte

Ein **Schwellenwert** legt fest, wie viele Verbindungsversuche von einer einzelnen Destination (Zieladresse) innerhalb eines gleitenden Zeitfensters zulässig sind.

- **Numerisch:** `N/S` bedeutet, `N` Verbindungen pro `S` Sekunden zu erlauben. Beispiel: `15/5` erlaubt bis zu 15 Verbindungen alle 5 Sekunden. Der `N+1`-te Versuch innerhalb des Zeitfensters wird abgelehnt.  
- **Schlüsselwörter:** `allow` bedeutet keine Beschränkung. `deny` bedeutet immer ablehnen.

## Regelsyntax

Regeln haben folgende Form:

```
<threshold> <scope> <target>
```
Wobei:

- `<threshold>` ist `N/S`, `allow` oder `deny`  
- `<scope>` ist eines von `default`, `explicit`, `file` oder `record` (siehe unten)  
- `<target>` hängt vom Geltungsbereich ab

### Standardregel

Gilt, wenn keine andere Regel zutrifft. Es ist nur **eine** Standardregel zulässig. Wenn weggelassen, sind unbekannte Destinations (Zieladressen) uneingeschränkt zulässig.

```
15/5 default
allow default
deny default
```
### Explizite Regel

Adressiert eine bestimmte Destination (Zieladresse) über die Base32-Adresse (z. B. `example1.b32.i2p`) oder den vollständigen Schlüssel.

```
15/5 explicit example1.b32.i2p
deny explicit example2.b32.i2p
allow explicit example3.b32.i2p
```
### Dateibasierte Regel

Zielt auf **alle** Destinations (Zieladressen) ab, die in einer externen Datei aufgelistet sind. Jede Zeile enthält eine Destination; `#`-Kommentare und Leerzeilen sind zulässig.

```
15/5 file /var/i2p/throttled.txt
deny file /var/i2p/blocked.txt
allow file /var/i2p/trusted.txt
```
> Betriebshinweis: Einige Implementierungen lesen Dateilisten periodisch erneut ein. Wenn Sie eine Liste bearbeiten, während der tunnel läuft, rechnen Sie mit einer kurzen Verzögerung, bis die Änderungen erkannt werden. Starten Sie neu, um die Änderungen sofort anzuwenden.

### Rekorder (progressive Steuerung)

Ein **Recorder** überwacht Verbindungsversuche und schreibt Destinations (I2P-Zieladressen), die einen Schwellenwert überschreiten, in eine Datei. Diese Datei können Sie dann in einer `file`-Regel referenzieren, um bei zukünftigen Versuchen Drosselungen oder Sperren anzuwenden.

```
# Start permissive
allow default

# Record Destinations exceeding 30 connections in 5 seconds
30/5 record /var/i2p/aggressive.txt

# Apply throttling to recorded Destinations
15/5 file /var/i2p/aggressive.txt
```
> Überprüfen Sie die Recorder-Unterstützung in Ihrem Build, bevor Sie sich darauf verlassen. Verwenden Sie `file`-Listen für garantiertes Verhalten.

## Auswertungsreihenfolge

Spezifische Regeln zuerst, dann allgemeine. Ein gängiges Muster:

1. Explizite Zulassungen für vertrauenswürdige Peers  
2. Explizite Sperren für bekannte Missbraucher  
3. Dateibasierte Allow-/Deny-Listen  
4. Recorder (Aufzeichner) für progressive Drosselung  
5. Standardregel als Auffangregel

## Vollständiges Beispiel

```
# Moderate limits by default
30/10 default

# Always allow trusted peers
allow explicit friend1.b32.i2p
allow explicit friend2.b32.i2p

# Block known bad actors
deny file /var/i2p/blocklist.txt

# Throttle aggressive sources
15/5 file /var/i2p/throttle.txt

# Automatically populate the throttle list
60/5 record /var/i2p/throttle.txt
```
## Implementierungshinweise

- Der Zugriffsfilter arbeitet auf der tunnel-Ebene, vor der Anwendungs verarbeitung, sodass missbräuchlicher Datenverkehr frühzeitig abgewiesen werden kann.  
- Platzieren Sie die Filterdatei in Ihrem I2PTunnel-Konfigurationsverzeichnis und starten Sie den tunnel neu, um die Änderungen zu übernehmen.  
- Teilen Sie dateibasierte Listen über mehrere tunnels hinweg, wenn Sie eine einheitliche Richtlinie für alle Dienste wünschen.
