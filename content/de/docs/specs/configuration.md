---
title: "Router-Konfiguration"
description: "Konfigurationsoptionen und Formate für I2P routers und Clients"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Übersicht

Dieses Dokument bietet eine umfassende technische Spezifikation der I2P-Konfigurationsdateien, die vom router und verschiedenen Anwendungen verwendet werden. Es umfasst Spezifikationen zu Dateiformaten, Eigenschaftsdefinitionen sowie Implementierungsdetails, die anhand des I2P-Quellcodes und der offiziellen Dokumentation verifiziert wurden.

### Geltungsbereich

- Router-Konfigurationsdateien und -formate
- Konfigurationen von Client-Anwendungen
- I2PTunnel tunnel-Konfigurationen
- Spezifikationen und Implementierung von Dateiformaten
- Versionsspezifische Funktionen und Abkündigungen (Deprecations)

### Hinweise zur Implementierung

Konfigurationsdateien werden mithilfe der Methoden `DataHelper.loadProps()` und `storeProps()` in der I2P-Kernbibliothek gelesen und geschrieben. Das Dateiformat unterscheidet sich erheblich von dem in I2P-Protokollen verwendeten serialisierten Format (siehe [Spezifikation für gemeinsame Strukturen - Typzuordnung](/docs/specs/common-structures/#type-mapping)).

---

## Allgemeines Format der Konfigurationsdatei

I2P-Konfigurationsdateien folgen einem modifizierten Java-Properties-Format mit spezifischen Ausnahmen und Einschränkungen.

### Formatspezifikation

Basierend auf [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) mit den folgenden wesentlichen Unterschieden:

#### Kodierung

- **MUSS** UTF-8-Kodierung verwenden (NICHT ISO-8859-1 wie bei Standard-Java-Properties)
- Implementierung: Verwendet die Hilfsfunktion `DataHelper.getUTF8()` für alle Dateioperationen

#### Escape-Sequenzen

- Es werden **KEINE** Escape-Sequenzen erkannt (einschließlich Backslash `\`)
- Zeilenfortsetzung wird **NICHT** unterstützt
- Backslash-Zeichen werden wörtlich behandelt

#### Kommentarzeichen

- `#` leitet einen Kommentar an beliebiger Position in einer Zeile ein
- `;` leitet einen Kommentar **nur** ein, wenn es in Spalte 1 steht
- `!` leitet **NICHT** einen Kommentar ein (anders als bei Java Properties)

#### Schlüssel-Wert-Trennzeichen

- `=` ist das **EINZIGE** gültige Schlüssel-Wert-Trennzeichen
- `:` wird **NICHT** als Trennzeichen erkannt
- Leerraum wird **NICHT** als Trennzeichen erkannt

#### Umgang mit Whitespace (Leerraum)

- Führender und nachfolgender Leerraum wird bei Schlüsseln **NICHT** entfernt
- Führender und nachfolgender Leerraum **WIRD** bei Werten entfernt

#### Zeilenverarbeitung

- Zeilen ohne `=` werden ignoriert (als Kommentare oder leere Zeilen behandelt)
- Leere Werte (`key=`) werden seit Version 0.9.10 unterstützt
- Schlüssel mit leeren Werten werden normal gespeichert und abgerufen

#### Zeichenbeschränkungen

**Schlüssel dürfen NICHT enthalten**: - `#` (Raute/Nummernzeichen) - `=` (Gleichheitszeichen) - `\n` (Zeilenumbruchzeichen) - Dürfen nicht mit `;` beginnen (Semikolon)

**Werte dürfen NICHT enthalten**: - `#` (Raute/Nummernzeichen) - `\n` (Zeilenumbruchzeichen) - dürfen nicht mit `\r` (Wagenrücklauf) beginnen oder enden - dürfen nicht mit Leerraum beginnen oder enden (wird automatisch entfernt)

### Dateisortierung

Konfigurationsdateien müssen nicht nach Schlüsseln sortiert sein. Die meisten I2P-Anwendungen sortieren jedoch die Schlüssel beim Schreiben von Konfigurationsdateien alphabetisch, um Folgendes zu erleichtern: - Manuelle Bearbeitung - Diff-Vorgänge in der Versionskontrolle - Menschliche Lesbarkeit

### Implementierungsdetails

#### Konfigurationsdateien lesen

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Verhalten**: - Liest UTF-8-kodierte Dateien - Erzwingt alle oben beschriebenen Formatregeln - Validiert die Zeichenbeschränkungen - Gibt ein leeres Properties-Objekt zurück, wenn die Datei nicht existiert - Löst bei Lesefehlern eine `IOException` aus

#### Erstellen von Konfigurationsdateien

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Verhalten**: - Schreibt UTF-8-kodierte Dateien - Sortiert Schlüssel alphabetisch (außer wenn OrderedProperties verwendet wird) - Setzt die Dateiberechtigungen auf Modus 600 (nur Lesen/Schreiben für den Benutzer) ab Version 0.8.1 - Wirft `IllegalArgumentException` bei ungültigen Zeichen in Schlüsseln oder Werten - Wirft `IOException` bei Schreibfehlern

#### Formatvalidierung

Die Implementierung führt eine strikte Validierung durch: - Schlüssel und Werte werden auf unzulässige Zeichen geprüft - Ungültige Einträge führen bei Schreibvorgängen zu Ausnahmen - Beim Lesen werden fehlerhafte Zeilen stillschweigend ignoriert (Zeilen ohne `=`)

### Formatbeispiele

#### Gültige Konfigurationsdatei

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Ungültige Konfigurationsbeispiele

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Kernbibliothek und router-Konfiguration

### Client-Konfiguration (clients.config)

**Speicherort**: `$I2P_CONFIG_DIR/clients.config` (veraltet) oder `$I2P_CONFIG_DIR/clients.config.d/` (modern)   **Konfigurationsoberfläche**: Router-Konsole unter `/configclients`   **Formatänderung**: Version 0.9.42 (August 2019)

#### Verzeichnisstruktur (Version 0.9.42+)

Seit Version 0.9.42 wird die Standarddatei clients.config automatisch in einzelne Konfigurationsdateien aufgeteilt:

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Migrationsverhalten**: - Beim ersten Start nach einem Upgrade auf 0.9.42+ wird die monolithische Datei automatisch aufgeteilt - Eigenschaften in den aufgeteilten Dateien erhalten das Präfix `clientApp.0.` - Das alte Format wird weiterhin zur Wahrung der Rückwärtskompatibilität unterstützt - Das Split-Format ermöglicht modulare Paketierung und Plugin-Management

#### Eigenschaftsformat

Zeilen haben das Format `clientApp.x.prop=val`, wobei `x` die App-Nummer ist.

**Anforderungen an die App-Nummerierung**: - MUSS mit 0 beginnen - MUSS fortlaufend sein (keine Lücken) - Die Reihenfolge bestimmt die Startsequenz

#### Erforderliche Eigenschaften

##### Haupt

- **Typ**: String (vollqualifizierter Klassenname)
- **Erforderlich**: Ja
- **Beschreibung**: Der Konstruktor oder die `main()`-Methode in dieser Klasse wird abhängig vom Client-Typ (verwaltet vs. nicht verwaltet) aufgerufen
- **Beispiel**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Optionale Eigenschaften

##### Name

- **Typ**: String
- **Erforderlich**: Nein
- **Beschreibung**: Anzeigename, der in der Router-Konsole angezeigt wird
- **Beispiel**: `clientApp.0.name=Router Console`

##### Argumente

- **Typ**: String (durch Leerzeichen oder Tabulator getrennt)
- **Erforderlich**: Nein
- **Beschreibung**: Argumente, die an den Konstruktor der Hauptklasse oder an die Methode main() übergeben werden
- **Anführungszeichen**: Argumente, die Leerzeichen oder Tabulatoren enthalten, können mit `'` oder `"` in Anführungszeichen gesetzt werden
- **Beispiel**: `clientApp.0.args=-d $CONFIG/eepsite`

##### Verzögerung

- **Typ**: Integer (Sekunden)
- **Erforderlich**: Nein
- **Standardwert**: 120
- **Beschreibung**: Sekunden, die vor dem Start des Clients gewartet werden
- **Übersteuerungen**: Wird durch `onBoot=true` überschrieben (setzt Verzögerung auf 0)
- **Besondere Werte**:
  - `< 0`: Warten, bis der router den RUNNING-Zustand erreicht, dann sofort in einem neuen Thread starten
  - `= 0`: Sofort im selben Thread ausführen (Ausnahmen werden an die Konsole weitergereicht)
  - `> 0`: Nach Verzögerung in neuem Thread starten (Ausnahmen werden protokolliert, nicht weitergereicht)

##### onBoot

- **Typ**: Boolesch
- **Erforderlich**: Nein
- **Standardwert**: false
- **Beschreibung**: Erzwingt eine Verzögerung von 0 und setzt eine explizite Verzögerungseinstellung außer Kraft
- **Anwendungsfall**: Startet kritische Dienste sofort beim router-Start

##### startOnLoad

- **Typ**: Boolesch
- **Erforderlich**: Nein
- **Standardwert**: true
- **Beschreibung**: Ob der Client überhaupt gestartet werden soll
- **Anwendungsfall**: Clients deaktivieren, ohne die Konfiguration zu entfernen

#### Pluginspezifische Eigenschaften

Diese Eigenschaften werden nur von Plugins verwendet (nicht von Kern-Clients):

##### stopargs

- **Typ**: String (durch Leerzeichen oder Tabulator getrennt)
- **Beschreibung**: Argumente, die zum Stoppen des Clients übergeben werden
- **Variablenersetzung**: Ja (siehe unten)

##### uninstallargs

- **Typ**: String (durch Leerzeichen oder Tabulator getrennt)
- **Beschreibung**: Argumente, die zur Deinstallation des Clients übergeben werden
- **Variablenersetzung**: Ja (siehe unten)

##### Klassenpfad

- **Typ**: String (kommagetrennte Pfade)
- **Beschreibung**: Zusätzliche Classpath-Elemente für den Client
- **Variablenersetzung**: Ja (siehe unten)

#### Variablensubstitution (nur für Plugins)

Die folgenden Variablen werden in `args`, `stopargs`, `uninstallargs` und `classpath` für Plugins ersetzt:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Hinweis**: Die Variablenersetzung wird nur für Plugins durchgeführt, nicht für Kern-Clients.

#### Client-Typen

##### Verwaltete Clients

- Der Konstruktor wird mit den Parametern `RouterContext` und `ClientAppManager` aufgerufen
- Der Client muss die Schnittstelle `ClientApp` implementieren
- Der Lebenszyklus wird vom router gesteuert
- Kann dynamisch gestartet, gestoppt und neu gestartet werden

##### Nicht verwaltete Clients

- Methode `main(String[] args)` wird aufgerufen
- Wird in einem separaten Thread ausgeführt
- Lebenszyklus wird nicht vom router verwaltet
- Veralteter Client-Typ

#### Beispielkonfiguration

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Logger-Konfiguration (logger.config)

**Speicherort**: `$I2P_CONFIG_DIR/logger.config`   **Konfigurationsoberfläche**: Router-Konsole unter `/configlogging`

#### Eigenschaftsreferenz

##### Konfiguration des Konsolenpuffers

###### logger.consoleBufferSize

- **Typ**: Ganzzahl
- **Standard**: 20
- **Beschreibung**: Maximale Anzahl von Protokollmeldungen, die in der Konsole gepuffert werden
- **Bereich**: 1-1000 empfohlen

##### Datums- und Zeitformatierung

###### logger.dateFormat

- **Typ**: String (SimpleDateFormat-Muster)
- **Standardwert**: Aus dem Systemgebietsschema
- **Beispiel**: `HH:mm:ss.SSS`
- **Dokumentation**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Protokollierungsstufen

###### logger.defaultLevel

- **Typ**: Enum
- **Standardwert**: ERROR
- **Werte**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Beschreibung**: Standard-Protokollierungsstufe für alle Klassen

###### logger.minimumOnScreenLevel

- **Typ**: Enum (Aufzählungstyp)
- **Standard**: CRIT
- **Werte**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Beschreibung**: Mindeststufe für Meldungen, die auf dem Bildschirm angezeigt werden

###### logger.record.{class}

- **Typ**: Aufzählungstyp
- **Werte**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Beschreibung**: Überschreiben der Protokollierungsstufe pro Klasse
- **Beispiel**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Anzeigeoptionen

###### logger.displayOnScreen

- **Typ**: Boolesch
- **Standard**: true
- **Beschreibung**: Ob Protokollmeldungen in der Konsolenausgabe angezeigt werden

###### logger.dropDuplicates

- **Typ**: Boolescher Wert
- **Standardwert**: true
- **Beschreibung**: Doppelte aufeinanderfolgende Logmeldungen verwerfen

###### logger.dropOnOverflow

- **Typ**: Boolesch
- **Standardwert**: false
- **Beschreibung**: Verwirft Nachrichten, wenn der Puffer voll ist (statt zu blockieren)

##### Flush-Verhalten

###### logger.flushInterval

- **Typ**: Ganzzahl (Sekunden)
- **Standardwert**: 29
- **Seit**: Version 0.9.18
- **Beschreibung**: Wie häufig der Log-Puffer auf die Festplatte geschrieben wird

##### Formatkonfiguration

###### logger.format

- **Typ**: String (Zeichenfolge)
- **Beschreibung**: Formatvorlage für Lognachrichten
- **Formatzeichen**:
  - `d` = Datum/Uhrzeit
  - `c` = Klassenname
  - `t` = Thread-Name
  - `p` = Priorität (Protokollebene)
  - `m` = Nachricht
- **Beispiel**: `dctpm` ergibt `[Zeitstempel] [Klasse] [Thread] [Stufe] Nachricht`

##### Kompression (Version 0.9.56+)

###### logger.gzip

- **Typ**: Boolesch
- **Standardwert**: false
- **Seit**: Version 0.9.56
- **Beschreibung**: Aktiviert gzip-Komprimierung für rotierte Protokolldateien

###### logger.minGzipSize

- **Typ**: Integer (Bytes)
- **Standardwert**: 65536
- **Seit**: Version 0.9.56
- **Beschreibung**: Minimale Dateigröße, ab der eine Komprimierung ausgelöst wird (Standardwert: 64 KB)

##### Dateiverwaltung

###### logger.logBufferSize

- **Typ**: Integer (Bytes)
- **Standardwert**: 1024
- **Beschreibung**: Maximale Anzahl von Nachrichten, die gepuffert werden, bevor der Puffer geleert wird

###### logger.logFileName

- **Typ**: String (Dateipfad)
- **Standardwert**: `logs/log-@.txt`
- **Beschreibung**: Namensmuster für Logdateien (`@` wird durch die Rotationsnummer ersetzt)

###### logger.logFilenameOverride

- **Typ**: String (Dateipfad)
- **Beschreibung**: Überschreibt den Logdateinamen (deaktiviert das Rotationsschema)

###### logger.logFileSize

- **Typ**: Zeichenkette (Größe mit Einheit)
- **Standardwert**: 10M
- **Einheiten**: K (Kilobyte), M (Megabyte), G (Gigabyte)
- **Beispiel**: `50M`, `1G`

###### logger.logRotationLimit

- **Typ**: Ganzzahl
- **Standardwert**: 2
- **Beschreibung**: Höchste Rotationsdateinummer (log-0.txt bis einschließlich log-N.txt)

#### Beispielkonfiguration

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Plugin-Konfiguration

#### Individuelle Plugin-Konfiguration (plugins/*/plugin.config)

**Speicherort**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Format**: Standardformat für I2P-Konfigurationsdateien   **Dokumentation**: [Plugin-Spezifikation](/docs/specs/plugin/)

##### Erforderliche Eigenschaften

###### Name

- **Typ**: String
- **Erforderlich**: Ja
- **Beschreibung**: Anzeigename des Plugins
- **Beispiel**: `name=I2P Plugin Example`

###### Schlüssel

- **Typ**: String (öffentlicher Schlüssel)
- **Erforderlich**: Ja (bei SU3-signierten Plugins weglassen)
- **Beschreibung**: Öffentlicher Signierschlüssel des Plugins zur Verifikation
- **Format**: Base64-kodierter Signierschlüssel

###### Unterzeichner

- **Typ**: String
- **Erforderlich**: Ja
- **Beschreibung**: Identität des Plugin-Unterzeichners
- **Beispiel**: `signer=user@example.i2p`

###### Version

- **Typ**: String (VersionComparator-Format)
- **Erforderlich**: Ja
- **Beschreibung**: Plugin-Version für die Update-Prüfung
- **Format**: Semantische Versionierung oder benutzerdefiniertes, vergleichbares Format
- **Beispiel**: `version=1.2.3`

##### Anzeigeeigenschaften

###### Datum

- **Typ**: Long (Unix-Zeitstempel in Millisekunden)
- **Beschreibung**: Veröffentlichungsdatum des Plugins

###### Autor

- **Typ**: String
- **Beschreibung**: Name des Plugin-Autors

###### websiteURL

- **Typ**: Zeichenkette (URL)
- **Beschreibung**: URL der Plugin-Website

###### updateURL

- **Typ**: String (URL)
- **Beschreibung**: Update-Prüf-URL für das Plugin

###### updateURL.su3

- **Typ**: Zeichenkette (URL)
- **Seit**: Version 0.9.15
- **Beschreibung**: Update-URL im SU3-Format (bevorzugt)

###### Beschreibung

- **Typ**: String
- **Beschreibung**: Englische Plugin-Beschreibung

###### description_{language}

- **Typ**: String
- **Beschreibung**: Lokalisierte Plugin-Beschreibung
- **Beispiel**: `description_de=Deutsche Beschreibung`

###### Lizenz

- **Typ**: String
- **Beschreibung**: Plugin-Lizenzkennung
- **Beispiel**: `license=Apache 2.0`

##### Installationseigenschaften

###### Nicht automatisch nach der Installation starten

- **Typ**: Boolesch
- **Standardwert**: false
- **Beschreibung**: Automatischen Start nach der Installation verhindern

###### router-Neustart erforderlich

- **Typ**: Boolesch
- **Standardwert**: false
- **Beschreibung**: Nach der Installation ist ein Neustart des router erforderlich

###### Nur-Installation

- **Typ**: Boolesch
- **Standardwert**: false
- **Beschreibung**: Nur einmalig installieren (keine Updates)

###### nur aktualisieren

- **Typ**: Boolesch
- **Standardwert**: false
- **Beschreibung**: Nur vorhandene Installation aktualisieren (keine Neuinstallation)

##### Beispiel-Plugin-Konfiguration

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Globale Plugin-Konfiguration (plugins.config)

**Ort**: `$I2P_CONFIG_DIR/plugins.config`   **Zweck**: Installierte Plugins global aktivieren/deaktivieren

##### Eigenschaftsformat

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Plugin-Name aus plugin.config
- `startOnLoad`: Ob das Plugin beim Start von router gestartet werden soll

##### Beispiel

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Konfiguration von Webanwendungen (webapps.config)

**Pfad**: `$I2P_CONFIG_DIR/webapps.config`   **Zweck**: Webanwendungen aktivieren/deaktivieren und konfigurieren

#### Eigenschaftsformat

##### webapps.{name}.startOnLoad

- **Typ**: Boolesch
- **Beschreibung**: Ob die Webapp beim Start des router gestartet werden soll
- **Format**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Typ**: String (durch Leerzeichen oder Kommas getrennte Pfade)
- **Beschreibung**: Zusätzliche Klassenpfad-Einträge für die Webapp
- **Format**: `webapps.{name}.classpath=[paths]`

#### Variablenersetzung

Pfade unterstützen die folgenden Variablenersetzungen:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Auflösung des Klassenpfads

- **Kern-Webapps**: Pfade relativ zu `$I2P/lib`
- **Plugin-Webapps**: Pfade relativ zu `$CONFIG/plugins/{appname}/lib`

#### Beispielkonfiguration

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Router-Konfiguration (router.config)

**Speicherort**: `$I2P_CONFIG_DIR/router.config`   **Konfigurationsoberfläche**: Router-Konsole unter `/configadvanced`   **Zweck**: Zentrale Router-Einstellungen und Netzwerkparameter

#### Konfigurationskategorien

##### Netzwerkkonfiguration

Bandbreiteneinstellungen:

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Transportkonfiguration:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Router-Verhalten

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Konsolenkonfiguration

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Zeiteinstellungen

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Hinweis**: Die Router-Konfiguration ist umfangreich. Siehe die Router-Konsole unter `/configadvanced` für die vollständige Referenz aller Eigenschaften.

---

## Konfigurationsdateien für Anwendungen

### Adressbuch-Konfiguration (addressbook/config.txt)

**Speicherort**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Anwendung**: SusiDNS   **Zweck**: Auflösung von Hostnamen und Adressbuchverwaltung

#### Dateispeicherorte

##### Router-Adressbuch

- **Standard**: `../hosts.txt`
- **Beschreibung**: Hauptadressbuch (systemweite Hostnamen)
- **Format**: Standardformat der Hosts-Datei

##### privatehosts.txt

- **Pfad**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Beschreibung**: Private Hostnamen-Zuordnungen
- **Priorität**: Höchste (setzt alle anderen Quellen außer Kraft)

##### userhosts.txt

- **Speicherort**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Beschreibung**: Vom Benutzer hinzugefügte Hostnamen-Zuordnungen
- **Verwaltung**: Über die SusiDNS-Oberfläche

##### hosts.txt

- **Speicherort**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Beschreibung**: Heruntergeladenes öffentliches Adressbuch
- **Quelle**: Abonnement-Feeds

#### Namensdienst

##### BlockfileNamingService (Standard seit 0.8.8)

Speicherformat: - **Datei**: `hostsdb.blockfile` - **Speicherort**: `$I2P_CONFIG_DIR/addressbook/` - **Leistung**: ~10x schnellere Abfragen als hosts.txt - **Format**: Binäres Datenbankformat

Legacy-Namensdienst: - **Format**: Nur-Text hosts.txt - **Status**: Veraltet, aber weiterhin unterstützt - **Anwendungsfall**: manuelle Bearbeitung, Versionskontrolle

#### Regeln für Hostnamen

I2P-Hostnamen müssen den folgenden Anforderungen entsprechen:

1. **TLD-Anforderung**: Muss mit `.i2p` enden
2. **Maximale Länge**: Insgesamt 67 Zeichen
3. **Zeichensatz**: `[a-z]`, `[0-9]`, `.` (Punkt), `-` (Bindestrich)
4. **Schreibweise**: Nur Kleinbuchstaben
5. **Startbeschränkungen**: Darf nicht mit `.` oder `-` beginnen
6. **Verbotene Muster**: Darf `..`, `.-` oder `-.` nicht enthalten (seit 0.6.1.33)
7. **Reserviert**: Base32-Hostnamen `*.b32.i2p` (52 Zeichen von base32.b32.i2p)

##### Gültige Beispiele

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Ungültige Beispiele

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Abonnementverwaltung

##### subscriptions.txt

- **Speicherort**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Format**: Eine URL pro Zeile
- **Standard**: `http://i2p-projekt.i2p/hosts.txt`

##### Abonnement-Feed-Format (seit 0.9.26)

Erweitertes Feed-Format mit Metadaten:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Metadaten-Eigenschaften: - `added`: Datum, an dem der Hostname hinzugefügt wurde (Format YYYYMMDD) - `src`: Quellbezeichner - `sig`: Optionale Signatur

**Abwärtskompatibilität**: Einfaches hostname=destination-Format wird weiterhin unterstützt.

#### Beispielkonfiguration

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### I2PSnark-Konfiguration (i2psnark.config.d/i2psnark.config)

**Pfad**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Anwendung**: I2PSnark BitTorrent-Client   **Konfigurationsoberfläche**: Web-GUI unter http://127.0.0.1:7657/i2psnark

#### Verzeichnisstruktur

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Hauptkonfiguration (i2psnark.config)

Minimale Standardkonfiguration:

```properties
i2psnark.dir=i2psnark
```
Zusätzliche Eigenschaften, die über die Weboberfläche verwaltet werden:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Individuelle Torrent-Konfiguration

**Speicherort**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Format**: Einstellungen pro Torrent   **Verwaltung**: Automatisch (über Web-GUI)

Eigenschaften umfassen: - Torrent-spezifische Upload-/Download-Einstellungen - Dateiprioritäten - Tracker-Informationen - Grenzwerte für Peers

**Hinweis**: Torrent-Konfigurationen werden hauptsächlich über die Weboberfläche verwaltet. Manuelles Bearbeiten wird nicht empfohlen.

#### Organisation der Torrent-Daten

Die Datenspeicherung ist von der Konfiguration getrennt:

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### I2PTunnel Konfiguration (i2ptunnel.config)

**Speicherort**: `$I2P_CONFIG_DIR/i2ptunnel.config` (veraltet) oder `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (modern)   **Konfigurationsoberfläche**: Router-Konsole unter `/i2ptunnel`   **Formatänderung**: Version 0.9.42 (August 2019)

#### Verzeichnisstruktur (Version 0.9.42+)

Ab Version 0.9.42 wird die Standarddatei i2ptunnel.config automatisch aufgeteilt:

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Kritischer Formatunterschied**: - **Monolithisches Format**: Eigenschaften mit dem Präfix `tunnel.N.` - **Getrenntes Format**: Eigenschaften **NICHT** mit Präfix (z. B. `description=`, nicht `tunnel.0.description=`)

#### Migrationsverhalten

Beim ersten Start nach dem Upgrade auf 0.9.42: 1. Vorhandene i2ptunnel.config wird eingelesen 2. Einzelne tunnel-Konfigurationen werden in i2ptunnel.config.d/ erstellt 3. In den aufgeteilten Dateien werden die Präfixe der Eigenschaften entfernt 4. Originaldatei wird gesichert 5. Altes Format wird weiterhin zur Abwärtskompatibilität unterstützt

#### Konfigurationsabschnitte

Die I2PTunnel-Konfiguration ist im Abschnitt [I2PTunnel-Konfigurationsreferenz](#i2ptunnel-configuration-reference) weiter unten ausführlich dokumentiert. Die Eigenschaftsbeschreibungen gelten sowohl für monolithische (`tunnel.N.property`) als auch für getrennte (`property`) Formate.

---

## I2PTunnel-Konfigurationsreferenz

Dieser Abschnitt bietet eine umfassende technische Referenz für alle I2PTunnel-Konfigurationseigenschaften. Eigenschaften werden im getrennten Format dargestellt (ohne das Präfix `tunnel.N.`). Für das monolithische Format sind allen Eigenschaften `tunnel.N.` voranzustellen, wobei N die tunnel-Nummer ist.

**Wichtig**: Eigenschaften, die als `tunnel.N.option.i2cp.*` beschrieben sind, sind in I2PTunnel implementiert und werden über andere Schnittstellen wie das I2CP‑Protokoll oder die SAM API **NICHT** unterstützt.

### Grundlegende Eigenschaften

#### tunnel.N.description (Beschreibung)

- **Typ**: String
- **Kontext**: Alle Tunnel
- **Beschreibung**: Menschlich lesbare Tunnelbeschreibung für die Anzeige in der Benutzeroberfläche
- **Beispiel**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (Name)

- **Typ**: String
- **Kontext**: Alle tunnels
- **Erforderlich**: Ja
- **Beschreibung**: Eindeutiger tunnel-Bezeichner und Anzeigename
- **Beispiel**: `name=I2P HTTP Proxy`

#### tunnel.N.type (Typ)

- **Typ**: Enum (Aufzählungstyp)
- **Kontext**: Alle tunnel
- **Erforderlich**: Ja
- **Werte**:
  - `client` - Allgemeiner Client tunnel
  - `httpclient` - HTTP-Proxy-Client
  - `ircclient` - IRC-Client tunnel
  - `socksirctunnel` - SOCKS-IRC-Proxy
  - `sockstunnel` - SOCKS-Proxy (Version 4, 4a, 5)
  - `connectclient` - CONNECT-Proxy-Client
  - `streamrclient` - Streamr-Client
  - `server` - Allgemeiner Server tunnel
  - `httpserver` - HTTP-Server tunnel
  - `ircserver` - IRC-Server tunnel
  - `httpbidirserver` - Bidirektionaler HTTP-Server
  - `streamrserver` - Streamr-Server

#### tunnel.N.interface (Schnittstelle)

- **Typ**: Zeichenkette (IP-Adresse oder Hostname)
- **Kontext**: Nur für Client tunnels
- **Standardwert**: 127.0.0.1
- **Beschreibung**: Lokale Schnittstelle zum Binden für eingehende Verbindungen
- **Sicherheitshinweis**: Das Binden an 0.0.0.0 erlaubt Verbindungen von außen
- **Beispiel**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Typ**: Ganzzahl
- **Kontext**: Nur Client tunnels
- **Bereich**: 1-65535
- **Beschreibung**: Lokaler Port, auf dem auf Client-Verbindungen gelauscht wird
- **Beispiel**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Typ**: String (IP-Adresse oder Hostname)
- **Kontext**: Nur für Server tunnels
- **Beschreibung**: Lokaler Server, an den Verbindungen weitergeleitet werden sollen
- **Beispiel**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Typ**: Ganzzahl
- **Kontext**: Nur Server tunnels
- **Bereich**: 1-65535
- **Beschreibung**: Port auf dem targetHost, zu dem eine Verbindung hergestellt werden soll
- **Beispiel**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Typ**: String (durch Komma oder Leerzeichen getrennte Ziele)
- **Kontext**: Nur Client-Tunnels
- **Format**: `destination[:port][,destination[:port]]`
- **Beschreibung**: I2P-Ziel(e), mit dem/denen eine Verbindung hergestellt werden soll
- **Beispiele**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Typ**: String (IP-Adresse oder Hostname)
- **Standard**: 127.0.0.1
- **Beschreibung**: I2CP-Schnittstellenadresse des I2P router
- **Hinweis**: Wird ignoriert, wenn im router-Kontext ausgeführt
- **Beispiel**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Typ**: Ganzzahl
- **Standard**: 7654
- **Bereich**: 1-65535
- **Beschreibung**: I2CP-Port des I2P-Routers
- **Hinweis**: Wird ignoriert, wenn im Router-Kontext ausgeführt wird
- **Beispiel**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Typ**: Boolesch
- **Standardwert**: true
- **Beschreibung**: Ob der Tunnel gestartet werden soll, wenn I2PTunnel geladen wird
- **Beispiel**: `startOnLoad=true`

### Proxy‑Konfiguration

#### tunnel.N.proxyList (proxyList)

- **Typ**: Zeichenkette (durch Kommas oder Leerzeichen getrennte Hostnamen)
- **Kontext**: Nur HTTP- und SOCKS-Proxys
- **Beschreibung**: Liste der Outproxy-Hosts
- **Beispiel**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Serverkonfiguration

#### tunnel.N.privKeyFile (privKeyFile)

- **Type**: String (Dateipfad)
- **Context**: Server und persistente Client tunnels
- **Description**: Datei mit persistenten Privatschlüsseln der Destination (I2P-Adresse)
- **Path**: Absolut oder relativ zum I2P-Konfigurationsverzeichnis
- **Example**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Typ**: Zeichenkette (Hostname)
- **Kontext**: Nur für HTTP-Server
- **Standard**: Base32-Hostname des Ziels
- **Beschreibung**: Host-Header-Wert, der an den lokalen Server übergeben wird
- **Beispiel**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Typ**: String (Hostname)
- **Kontext**: Nur für HTTP-Server
- **Beschreibung**: Überschreibt den virtuellen Host für einen bestimmten eingehenden Port
- **Anwendungsfall**: Mehrere Websites auf unterschiedlichen Ports hosten
- **Beispiel**: `spoofedHost.8080=site1.example.i2p`

### Clientspezifische Optionen

#### tunnel.N.sharedClient (sharedClient)

- **Typ**: Boolesch
- **Kontext**: Nur Client tunnels
- **Standardwert**: false
- **Beschreibung**: Ob mehrere Clients diesen tunnel gemeinsam nutzen können
- **Beispiel**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Typ**: Boolesch
- **Kontext**: Nur für Client tunnels
- **Standardwert**: false
- **Beschreibung**: Zielschlüssel über Neustarts hinweg speichern und wiederverwenden
- **Konflikt**: Schließt sich mit `i2cp.newDestOnResume=true` gegenseitig aus
- **Beispiel**: `option.persistentClientKey=true`

### I2CP-Optionen (I2PTunnel-Implementierung)

**Wichtig**: Diese Eigenschaften haben das Präfix `option.i2cp.`, werden jedoch **in I2PTunnel implementiert**, nicht in der I2CP-Protokollschicht. Sie sind nicht über I2CP- oder SAM-APIs verfügbar.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Typ**: Boolesch
- **Kontext**: Nur Client-tunnels
- **Standardwert**: false
- **Beschreibung**: Erstellt den tunnel erst bei der ersten Verbindung
- **Anwendungsfall**: Ressourcen für selten genutzte tunnels sparen
- **Beispiel**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Typ**: Boolesch
- **Kontext**: Nur Client tunnels
- **Standardwert**: false
- **Erfordert**: `i2cp.closeOnIdle=true`
- **Konflikt**: Schließt sich gegenseitig aus mit `persistentClientKey=true`
- **Beschreibung**: Neue Destination (Zieladresse) nach Ablauf des Inaktivitäts-Timeouts erstellen
- **Beispiel**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Typ**: String (base64-kodierter Schlüssel)
- **Kontext**: Nur für Server-tunnels
- **Beschreibung**: Persistenter privater Verschlüsselungsschlüssel für das leaseSet
- **Anwendungsfall**: Konsistentes verschlüsseltes leaseSet über Neustarts hinweg beibehalten
- **Beispiel**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Typ**: String (sigtype:base64)
- **Kontext**: Nur Server-Tunnel
- **Format**: `sigtype:base64key`
- **Beschreibung**: Dauerhafter privater Signaturschlüssel für das leaseSet
- **Beispiel**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Serverspezifische Optionen

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Typ**: Boolesch
- **Kontext**: Gilt nur für Server tunnels
- **Standardwert**: false
- **Beschreibung**: Für jedes entfernte I2P-Ziel eine eindeutige lokale IP verwenden
- **Anwendungsfall**: Client-IPs in Server-Protokollen nachverfolgen
- **Sicherheitshinweis**: Kann die Anonymität verringern
- **Beispiel**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Typ**: String (hostname:port)
- **Kontext**: Nur für Server tunnels
- **Beschreibung**: targetHost/targetPort für eingehenden Port NNNN überschreiben
- **Anwendungsfall**: Portbasiertes Routing zu verschiedenen lokalen Diensten
- **Beispiel**: `option.targetForPort.8080=localhost:8080`

### Thread-Pool-Konfiguration

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Typ**: Boolesch
- **Kontext**: Nur für Server tunnels
- **Standard**: true
- **Beschreibung**: Thread-Pool zur Verbindungsverwaltung verwenden
- **Hinweis**: Für Standardserver immer false (ignoriert)
- **Beispiel**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Typ**: Ganzzahl
- **Kontext**: Nur für Server tunnels
- **Standardwert**: 65
- **Beschreibung**: Maximale Thread-Pool-Größe
- **Hinweis**: Wird bei Standardservern ignoriert
- **Beispiel**: `option.i2ptunnel.blockingHandlerCount=100`

### HTTP-Client-Optionen

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Typ**: Boolesch
- **Kontext**: Nur für HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: SSL-Verbindungen zu .i2p-Adressen zulassen
- **Beispiel**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Typ**: Boolesch
- **Kontext**: Nur für HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: Address Helper-Links (Hilfslinks zur Adressauflösung) in Proxy-Antworten deaktivieren
- **Beispiel**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Typ**: String (durch Kommas oder Leerzeichen getrennte URLs)
- **Kontext**: nur für HTTP-Clients
- **Beschreibung**: Jump-Server-URLs zur Auflösung von Hostnamen
- **Beispiel**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Typ**: Boolesch
- **Kontext**: Nur für HTTP-Clients
- **Standard**: false
- **Beschreibung**: Sende Accept-*‑Header (außer Accept und Accept-Encoding)
- **Beispiel**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Typ**: Boolesch
- **Kontext**: Nur HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: Referer-Header durch den Proxy weiterleiten
- **Datenschutzhinweis**: Kann Informationen preisgeben
- **Beispiel**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Typ**: Boolesch
- **Kontext**: nur für HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: User-Agent-Header über den Proxy weiterleiten
- **Datenschutzhinweis**: Kann Informationen über den Browser preisgeben
- **Beispiel**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Typ**: Boolesch
- **Kontext**: Nur HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: Via-Header durch den Proxy weiterreichen
- **Beispiel**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Typ**: String (durch Kommas oder Leerzeichen getrennte Destinations (Ziele))
- **Kontext**: Nur HTTP-Clients
- **Beschreibung**: Netzwerkinterne SSL-Outproxies für HTTPS
- **Beispiel**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Typ**: Boolesch
- **Kontext**: Nur HTTP-Clients
- **Standardwert**: true
- **Beschreibung**: Registrierte lokale Outproxy-Plugins (Ausgangsproxy) verwenden
- **Beispiel**: `option.i2ptunnel.useLocalOutproxy=true`

### HTTP-Client-Authentifizierung

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Typ**: Enum (Aufzählungstyp)
- **Kontext**: Nur für HTTP-Clients
- **Standardwert**: false
- **Werte**: `true`, `false`, `basic`, `digest`
- **Beschreibung**: Lokale Authentifizierung für den Proxyzugriff erfordern
- **Hinweis**: `true` entspricht `basic`
- **Beispiel**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Typ**: String (32 Zeichen, hexadezimale Darstellung in Kleinbuchstaben)
- **Kontext**: Nur HTTP-Clients
- **Erfordert**: `proxyAuth=basic` oder `proxyAuth=digest`
- **Beschreibung**: MD5-Hash des Passworts für den Benutzer USER
- **Veraltet**: Stattdessen SHA-256 verwenden (0.9.56+)
- **Beispiel**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Typ**: String (64 Zeichen, hexadezimal in Kleinbuchstaben)
- **Kontext**: Nur HTTP-Clients
- **Erfordert**: `proxyAuth=digest`
- **Seit**: Version 0.9.56
- **Standard**: RFC 7616
- **Beschreibung**: SHA-256-Hash des Passworts für den Benutzer USER
- **Beispiel**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Outproxy-Authentifizierung

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Typ**: Boolesch
- **Kontext**: nur für HTTP-Clients
- **Standardwert**: false
- **Beschreibung**: Authentifizierung an den Outproxy (I2P-Proxy ins Clearnet) senden
- **Beispiel**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Typ**: String
- **Kontext**: Nur HTTP-Clients
- **Erfordert**: `outproxyAuth=true`
- **Beschreibung**: Benutzername für die outproxy-Authentifizierung (Proxy ins Clearnet)
- **Beispiel**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Typ**: Zeichenfolge
- **Kontext**: Nur HTTP-Clients
- **Erfordert**: `outproxyAuth=true`
- **Beschreibung**: Passwort für die Outproxy-Authentifizierung
- **Sicherheit**: Im Klartext gespeichert
- **Beispiel**: `option.outproxyPassword=secret`

### SOCKS-Client-Optionen

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Typ**: String (durch Kommas oder Leerzeichen getrennte Ziele)
- **Kontext**: Nur für SOCKS-Clients
- **Beschreibung**: Netzinterne Outproxies (Proxy-Server für Verbindungen aus dem I2P-Netz ins Clearnet) für nicht spezifizierte Ports
- **Beispiel**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Typ**: String (Ziele, durch Kommas oder Leerzeichen getrennt)
- **Kontext**: nur SOCKS-Clients
- **Beschreibung**: Outproxies (Ausgangsproxies) im Netzwerk speziell für Port NNNN
- **Beispiel**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Typ**: Enum
- **Kontext**: Nur SOCKS-Clients
- **Standard**: socks
- **Seit**: Version 0.9.57
- **Werte**: `socks`, `connect` (HTTPS)
- **Beschreibung**: Typ des konfigurierten outproxy (Ausgangs-Proxy ins Clearnet)
- **Beispiel**: `option.outproxyType=connect`

### HTTP-Server-Optionen

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Typ**: Ganzzahl
- **Kontext**: Nur für HTTP-Server
- **Standard**: 0 (unbegrenzt)
- **Beschreibung**: Maximale Anzahl POST-Anfragen von einer Destination (I2P-Adresse) pro postCheckTime
- **Beispiel**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Typ**: Ganzzahl
- **Kontext**: Nur für HTTP-Server
- **Standard**: 0 (unbegrenzt)
- **Beschreibung**: Maximale Anzahl an POSTs von allen Zielen pro postCheckTime
- **Beispiel**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Typ**: Ganzzahl (Sekunden)
- **Kontext**: Nur für HTTP-Server
- **Standardwert**: 300
- **Beschreibung**: Zeitfenster zur Überprüfung der POST-Limits
- **Beispiel**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Typ**: Ganzzahl (Sekunden)
- **Kontext**: Nur für HTTP-Server
- **Standardwert**: 1800
- **Beschreibung**: Sperrzeit für ein einzelnes Ziel nach Überschreitung von maxPosts
- **Beispiel**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Typ**: Ganzzahl (Sekunden)
- **Kontext**: Nur für HTTP-Server
- **Standardwert**: 600
- **Beschreibung**: Sperrdauer, nachdem maxTotalPosts überschritten wurde
- **Beispiel**: `option.postTotalBanTime=1200`

### HTTP-Server-Sicherheitsoptionen

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Typ**: Boolesch
- **Kontext**: Nur HTTP-Server
- **Standard**: false
- **Beschreibung**: Verbindungen ablehnen, die anscheinend über einen inproxy (Eingangs-Proxy ins I2P‑Netz) erfolgen
- **Beispiel**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Typ**: Boolesch
- **Kontext**: Nur für HTTP-Server
- **Standard**: false
- **Seit**: Version 0.9.25
- **Beschreibung**: Verbindungen mit Referer-Header zurückweisen
- **Beispiel**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Typ**: Boolesch
- **Kontext**: Nur für HTTP-Server
- **Standardwert**: false
- **Seit**: Version 0.9.25
- **Erfordert**: Eigenschaft `userAgentRejectList`
- **Beschreibung**: Verbindungen mit übereinstimmendem User-Agent ablehnen
- **Beispiel**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Typ**: String (kommagetrennte Vergleichsmuster)
- **Kontext**: Nur HTTP-Server
- **Seit**: Version 0.9.25
- **Groß-/Kleinschreibung**: Groß-/Kleinschreibung beachten
- **Besonderes**: "none" (seit 0.9.33) entspricht einem leeren User-Agent
- **Beschreibung**: Liste von User-Agent-Mustern, die abgelehnt werden
- **Beispiel**: `option.userAgentRejectList=Mozilla,Opera,none`

### IRC-Serveroptionen

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Typ**: String (Hostname-Muster)
- **Kontext**: Nur für IRC-Server
- **Standard**: `%f.b32.i2p`
- **Token**:
  - `%f` = Vollständiger base32-Ziel-Hash
  - `%c` = Verschleierter Ziel-Hash (siehe cloakKey)
- **Beschreibung**: Hostname-Format, das an den IRC-Server gesendet wird
- **Beispiel**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Typ**: Zeichenkette (Passphrase)
- **Kontext**: Nur für IRC-Server
- **Standard**: Zufällig je Sitzung
- **Einschränkungen**: Keine Anführungszeichen oder Leerzeichen
- **Beschreibung**: Passphrase für gleichbleibende Hostname-Verschleierung
- **Anwendungsfall**: Dauerhafte Benutzer-Nachverfolgung über Neustarts und Server hinweg
- **Beispiel**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Typ**: Enum (Aufzählungstyp)
- **Kontext**: Nur für IRC-Server
- **Standard**: user
- **Werte**: `user`, `webirc`
- **Beschreibung**: Authentifizierungsmethode für IRC-Server
- **Beispiel**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Typ**: String (Passwort)
- **Kontext**: Nur für IRC-Server
- **Erfordert**: `method=webirc`
- **Einschränkungen**: Keine Anführungszeichen oder Leerzeichen
- **Beschreibung**: Passwort für die Authentifizierung des WEBIRC-Protokolls
- **Beispiel**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Typ**: Zeichenkette (IP-Adresse)
- **Kontext**: Nur für IRC-Server
- **Erfordert**: `method=webirc`
- **Beschreibung**: Gefälschte IP-Adresse für das WEBIRC-Protokoll
- **Beispiel**: `option.ircserver.webircSpoofIP=10.0.0.1`

### SSL/TLS-Konfiguration

#### tunnel.N.option.useSSL (option.useSSL)

- **Typ**: Boolesch
- **Standardwert**: false
- **Kontext**: Alle tunnels
- **Verhalten**:
  - **Server**: SSL für Verbindungen zum lokalen Server verwenden
  - **Clients**: SSL von lokalen Clients verlangen
- **Beispiel**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Typ**: String (Dateipfad)
- **Kontext**: Nur Client tunnels
- **Standardwert**: `i2ptunnel-(random).ks`
- **Pfad**: Relativ zu `$(I2P_CONFIG_DIR)/keystore/`, falls nicht absolut
- **Automatisch erstellt**: Erstellt, falls nicht vorhanden
- **Beschreibung**: Keystore-Datei, die den SSL-Privatschlüssel enthält
- **Beispiel**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Typ**: String (Passwort)
- **Kontext**: Nur Client tunnels
- **Standard**: changeit
- **Automatisch generiert**: Zufälliges Passwort, wenn neuer Keystore erstellt wird
- **Beschreibung**: Passwort für den SSL-Keystore
- **Beispiel**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Typ**: String (Alias)
- **Kontext**: Nur Client tunnels
- **Automatisch generiert**: Erstellt, wenn ein neuer Schlüssel generiert wird
- **Beschreibung**: Alias für privaten Schlüssel im Keystore
- **Beispiel**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Typ**: String (Passwort)
- **Kontext**: Nur für Client tunnels
- **Automatisch generiert**: Zufälliges Passwort, wenn neuer Schlüssel erstellt wird
- **Beschreibung**: Passwort für den privaten Schlüssel im keystore (Schlüsselspeicher)
- **Beispiel**: `option.keyPassword=keypass123`

### Allgemeine I2CP- und Streaming-Optionen

Alle `tunnel.N.option.*`-Eigenschaften (oben nicht ausdrücklich dokumentiert) werden an die I2CP-Schnittstelle und die Streaming-Bibliothek weitergeleitet, wobei das Präfix `tunnel.N.option.` entfernt wird.

**Wichtig**: Diese sind von I2PTunnel-spezifischen Optionen getrennt. Siehe: - [I2CP-Spezifikation](/docs/specs/i2cp/) - [Spezifikation der Streaming-Bibliothek](/docs/specs/streaming/)

Beispielhafte Streaming-Optionen:

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Vollständiges Tunnelbeispiel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Versionsverlauf und Funktions-Zeitleiste

### Version 0.9.10 (2013)

**Feature**: Unterstützung für leere Werte in Konfigurationsdateien - Schlüssel mit leeren Werten (`key=`) werden jetzt unterstützt - Zuvor ignoriert oder führten zu Parsing-Fehlern

### Version 0.9.18 (2015)

**Funktion**: Konfiguration des Flush-Intervalls des Loggers - Eigenschaft: `logger.flushInterval` (Standard 29 Sekunden) - Reduziert die Festplatten-I/O bei Beibehaltung einer akzeptablen Protokoll-Latenz

### Version 0.9.23 (November 2015)

**Wichtige Änderung**: Java 7 ist Mindestvoraussetzung - Unterstützung für Java 6 beendet - Erforderlich für weitere Sicherheitsupdates

### Version 0.9.25 (2015)

**Funktionen**: Sicherheitsoptionen für HTTP-Server - `tunnel.N.option.rejectReferer` - Verbindungen mit Referer-Header ablehnen - `tunnel.N.option.rejectUserAgents` - Bestimmte User-Agent-Header ablehnen - `tunnel.N.option.userAgentRejectList` - Abzuweisende User-Agent-Muster - **Anwendungsfall**: Crawler und unerwünschte Clients eindämmen

### Version 0.9.33 (Januar 2018)

**Funktion**: Erweiterte User-Agent-Filterung - `userAgentRejectList`-String "none" entspricht einem leeren User-Agent - Weitere Fehlerbehebungen für i2psnark, i2ptunnel, streaming, SusiMail

### Version 0.9.41 (2019)

**Abkündigung**: BOB-Protokoll aus Android entfernt - Android-Nutzer müssen auf SAM oder I2CP umsteigen

### Version 0.9.42 (August 2019)

**Wesentliche Änderung**: Aufteilung der Konfigurationsdateien - `clients.config` in die Verzeichnisstruktur `clients.config.d/` aufgeteilt - `i2ptunnel.config` in die Verzeichnisstruktur `i2ptunnel.config.d/` aufgeteilt - Automatische Migration beim ersten Start nach dem Upgrade - Ermöglicht modulare Paketierung und Plugin-Management - Altes monolithisches Format weiterhin unterstützt

**Zusätzliche Funktionen**: - SSU-Leistungsverbesserungen - Verhinderung netzwerkübergreifender Verbindungen (Proposal 147) - Erste Unterstützung für Verschlüsselungstypen

### Version 0.9.56 (2021)

**Funktionen**: Verbesserungen bei Sicherheit und Protokollierung - `logger.gzip` - Gzip-Komprimierung für rotierte Protokolldateien (Standard: false) - `logger.minGzipSize` - Mindestgröße für die Komprimierung (Standard: 65536 Bytes) - `tunnel.N.option.proxy.auth.USER.sha256` - SHA-256-Digest-Authentifizierung (RFC 7616) - **Sicherheit**: SHA-256 ersetzt MD5 für die Digest-Authentifizierung

### Version 0.9.57 (Januar 2023)

**Funktion**: SOCKS-Outproxy-Typkonfiguration - `tunnel.N.option.outproxyType` - Outproxy-Typ auswählen (socks|connect) - Standard: socks - HTTPS CONNECT-Unterstützung für HTTPS-Outproxies

### Version 2.6.0 (Juli 2024)

**Inkompatible Änderung**: I2P-over-Tor blockiert - Verbindungen von IP-Adressen von Tor-Exit-Knoten werden jetzt abgelehnt - **Grund**: Beeinträchtigt die I2P-Leistung, verschwendet Ressourcen von Tor-Exits - **Auswirkungen**: Nutzer, die über Tor-Exit-Knoten auf I2P zugreifen, werden blockiert - Nicht-Exit-Relays und Tor-Clients sind nicht betroffen

### Version 2.10.0 (September 2025 - aktuell)

**Hauptfunktionen**: - **Post-Quanten-Kryptografie** verfügbar (optional über Hidden Service Manager aktivierbar) - **UDP-Tracker-Unterstützung** für I2PSnark zur Reduzierung der Tracker-Last - **Stabilität im Hidden Mode**-Verbesserungen zur Verringerung der RouterInfo-Erschöpfung - Netzwerkverbesserungen für überlastete router - Verbessertes UPnP/NAT-Traversal - NetDB-Verbesserungen mit aggressiver leaseSet-Entfernung - Reduzierungen der Beobachtbarkeit von router-Ereignissen

**Konfiguration**: Keine neuen Konfigurationseigenschaften hinzugefügt

**Kritische bevorstehende Änderung**: Die nächste Version (voraussichtlich 2.11.0 oder 3.0.0) wird Java 17 oder höher erfordern

---

## Veraltete Funktionen und inkompatible Änderungen

### Kritische Abkündigungen

#### I2P-over-Tor-Zugriff (Version 2.6.0+)

- **Status**: BLOCKIERT seit Juli 2024
- **Auswirkung**: Verbindungen von IP-Adressen von Tor-Exitknoten werden abgelehnt
- **Begründung**: Beeinträchtigt die Leistung des I2P-Netzwerks, ohne Vorteile für die Anonymität zu bieten
- **Betrifft**: Nur Tor-Exitknoten, nicht Relays oder normale Tor-Clients
- **Alternative**: I2P oder Tor getrennt nutzen, nicht kombiniert

#### MD5-Digest-Authentifizierung

- **Status**: Veraltet (verwenden Sie SHA-256)
- **Eigenschaft**: `tunnel.N.option.proxy.auth.USER.md5`
- **Grund**: MD5 kryptografisch gebrochen
- **Ersatz**: `tunnel.N.option.proxy.auth.USER.sha256` (seit 0.9.56)
- **Zeitleiste**: MD5 weiterhin unterstützt, aber nicht empfohlen

### Änderungen der Konfigurationsarchitektur

#### Monolithische Konfigurationsdateien (Version 0.9.42+)

- **Betroffen**: `clients.config`, `i2ptunnel.config`
- **Status**: Veraltet zugunsten einer getrennten Verzeichnisstruktur
- **Migration**: Automatisch beim ersten Start nach dem Upgrade auf 0.9.42
- **Kompatibilität**: Altes Format funktioniert weiterhin (abwärtskompatibel)
- **Empfehlung**: Für neue Konfigurationen das getrennte Format verwenden

### Anforderungen an die Java-Version

#### Unterstützung für Java 6

- **Beendet**: Version 0.9.23 (November 2015)
- **Minimum**: Java 7 seit 0.9.23 erforderlich

#### Java-17-Voraussetzung (bevorstehend)

- **Status**: KRITISCHE ANSTEHENDE ÄNDERUNG
- **Ziel**: Nächste Hauptversion nach 2.10.0 (voraussichtlich 2.11.0 oder 3.0.0)
- **Aktuelles Minimum**: Java 8
- **Erforderliche Maßnahme**: Auf die Migration zu Java 17 vorbereiten
- **Zeitplan**: Wird mit den Versionshinweisen bekanntgegeben

### Entfernte Funktionen

#### BOB Protokoll (Android)

- **Entfernt**: Seit Version 0.9.41
- **Plattform**: Nur Android
- **Alternative**: SAM- oder I2CP-Protokolle
- **Desktop**: BOB auf Desktop-Plattformen weiterhin verfügbar

### Empfohlene Migrationen

1. **Authentifizierung**: Von MD5-Digest-Authentifizierung zu SHA-256-Digest-Authentifizierung migrieren
2. **Konfigurationsformat**: Auf eine getrennte Verzeichnisstruktur für Clients und tunnels migrieren
3. **Java-Laufzeitumgebung**: Upgrade auf Java 17 vor dem nächsten Major-Release einplanen
4. **Tor-Integration**: I2P nicht über Tor-Exit-Knoten routen

---

## Referenzen

### Offizielle Dokumentation

- [I2P-Konfigurationsspezifikation](/docs/specs/configuration/) - Offizielle Spezifikation des Konfigurationsdateiformats
- [I2P-Plugin-Spezifikation](/docs/specs/plugin/) - Plugin-Konfiguration und Paketierung
- [I2P Gemeinsame Strukturen - Typzuordnung](/docs/specs/common-structures/#type-mapping) - Serialisierungsformat für Protokolldaten
- [Java-Properties-Format](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Grundlegende Formatspezifikation

### Quellcode

- [I2P Java Router-Repository](https://github.com/i2p/i2p.i2p) - GitHub-Spiegel
- [I2P Developers Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p) - Offizielles I2P-Quellcode-Repository
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Implementierung der Ein-/Ausgabe für Konfigurationsdateien

### Ressourcen der Community

- [I2P Forum](https://i2pforum.net/) - Aktive Community-Diskussionen und Support
- [I2P Website](/) - Offizielle Projekt-Website

### API-Dokumentation

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - API-Dokumentation zu Methoden für Konfigurationsdateien

### Status der Spezifikation

- **Letzte Aktualisierung der Spezifikation**: Januar 2023 (Version 0.9.57)
- **Aktuelle I2P-Version**: 2.10.0 (September 2025)
- **Technische Genauigkeit**: Die Spezifikation bleibt bis einschließlich 2.10.0 korrekt (keine inkompatiblen Änderungen (breaking changes))
- **Wartung**: Lebendes Dokument, das aktualisiert wird, wenn das Konfigurationsformat geändert wird
