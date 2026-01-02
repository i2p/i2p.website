---
title: "Plugin-Paketformat"
description: ".xpi2p / .su3 Regeln für die Paketierung von I2P-Plugins"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Übersicht

I2P-Plugins sind signierte Archive, die die router-Funktionalität erweitern. Sie werden als `.xpi2p`- oder `.su3`-Dateien ausgeliefert, in `~/.i2p/plugins/<name>/` (oder unter Windows in `%APPDIR%\I2P\plugins\<name>\`) installiert und mit vollen router-Berechtigungen ohne Sandboxing ausgeführt.

### Unterstützte Plugin-Typen

- Konsolen-Webanwendungen
- Neue eepsites mit cgi-bin, Webanwendungen
- Konsolen-Themes
- Konsolen-Übersetzungen
- Java-Programme (im selben Prozess oder in einer separaten JVM)
- Shell-Skripte und native Binärdateien

### Sicherheitsmodell

**KRITISCH:** Plugins laufen in derselben JVM mit identischen Berechtigungen wie der I2P router. Sie haben uneingeschränkten Zugriff auf: - Dateisystem (Lesen und Schreiben) - Router APIs und interner Zustand - Netzwerkverbindungen - Ausführung externer Programme

Plugins sollten als vollständig vertrauenswürdiger Code behandelt werden. Benutzer müssen vor der Installation die Plugin-Quellen und -Signaturen verifizieren.

---

## Dateiformate

### SU3-Format (dringend empfohlen)

**Status:** Aktiv, bevorzugtes Format seit I2P 0.9.15 (September 2014)

Das Format `.su3` bietet: - **RSA-4096-Signaturschlüssel** (im Vergleich zu DSA-1024 in xpi2p) - Signatur im Dateiheader gespeichert - Magische Zahl: `I2Psu3` - Bessere Vorwärtskompatibilität

**Struktur:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### XPI2P-Format (Legacy, veraltet)

**Status:** Unterstützt zur Abwärtskompatibilität, nicht für neue Plugins empfohlen

Das `.xpi2p`-Format verwendet ältere kryptografische Signaturen:
- **DSA-1024-Signaturen** (veraltet gemäß NIST-800-57)
- 40-Byte-DSA-Signatur, der ZIP-Datei vorangestellt
- Erfordert das Feld `key` in plugin.config

**Struktur:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Migrationspfad:** Bei der Migration von xpi2p zu su3 stellen Sie während der Übergangsphase sowohl `updateURL` als auch `updateURL.su3` bereit. Moderne routers (0.9.15+) bevorzugen SU3 automatisch.

---

## Archivstruktur und plugin.config

### Erforderliche Dateien

**plugin.config** - Standard-I2P-Konfigurationsdatei mit Schlüssel-Wert-Paaren

### Erforderliche Eigenschaften

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Beispiele für Versionsformate:** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Gültige Trennzeichen: `.` (Punkt), `-` (Bindestrich), `_` (Unterstrich)

### Optionale Metadaten-Eigenschaften

#### Informationen anzeigen

- `date` - Veröffentlichungsdatum (Zeitstempel als Java long)
- `author` - Entwicklername (`user@mail.i2p` empfohlen)
- `description` - Englische Beschreibung
- `description_xx` - Lokalisierte Beschreibung (xx = Sprachcode)
- `websiteURL` - Plugin-Homepage (`http://foo.i2p/`)
- `license` - Lizenzkennung (z. B. "Apache-2.0", "GPL-3.0")

#### Konfiguration aktualisieren

- `updateURL` - XPI2P-Update-URL (veraltet)
- `updateURL.su3` - SU3-Update-URL (bevorzugt)
- `min-i2p-version` - Erforderliche Mindestversion von I2P
- `max-i2p-version` - Maximal kompatible I2P-Version
- `min-java-version` - Mindest-Java-Version (z. B. `1.7`, `17`)
- `min-jetty-version` - Mindest-Jetty-Version (verwenden Sie `6` für Jetty 6+)
- `max-jetty-version` - Maximale Jetty-Version (verwenden Sie `5.99999` für Jetty 5)

#### Installationsverhalten

- `dont-start-at-install` - Standardwert `false`. Wenn `true`, erfordert manuellen Start
- `router-restart-required` - Standardwert `false`. Informiert den Benutzer, dass nach dem Update ein Neustart erforderlich ist
- `update-only` - Standardwert `false`. Schlägt fehl, wenn das Plugin noch nicht installiert ist
- `install-only` - Standardwert `false`. Schlägt fehl, wenn das Plugin bereits installiert ist
- `min-installed-version` - Erforderliche Mindestversion für das Update
- `max-installed-version` - Maximale Version, die aktualisiert werden kann
- `disableStop` - Standardwert `false`. Blendet die Stopp-Schaltfläche aus, wenn `true`

#### Konsolenintegration

- `consoleLinkName` - Text für den Link in der Zusammenfassungsleiste der Konsole
- `consoleLinkName_xx` - Lokalisierter Linktext (xx = Sprachcode)
- `consoleLinkURL` - Ziel des Links (z. B. `/appname/index.jsp`)
- `consoleLinkTooltip` - Tooltip-Text (unterstützt seit 0.7.12-6)
- `consoleLinkTooltip_xx` - Lokalisierter Tooltip
- `console-icon` - Pfad zu einem 32x32-Icon (unterstützt seit 0.9.20)
- `icon-code` - Base64-codiertes 32x32-PNG für Plugins ohne Webressourcen (seit 0.9.25)

#### Plattformanforderungen (nur Anzeige)

- `required-platform-OS` - Betriebssystemanforderung (nicht erzwungen)
- `other-requirements` - Zusätzliche Anforderungen (z. B. "Python 3.8+")

#### Abhängigkeitsverwaltung (nicht implementiert)

- `depends` - kommagetrennte Plugin-Abhängigkeiten
- `depends-version` - Versionsanforderungen für Abhängigkeiten
- `langs` - Inhalte des Sprachpakets
- `type` - Plugin-Typ (app/theme/locale/webapp)

### Variablenersetzung in Update-URLs

**Funktionsstatus:** Verfügbar seit I2P 1.7.0 (0.9.53)

Sowohl `updateURL` als auch `updateURL.su3` unterstützen plattformspezifische Variablen:

**Variablen:** - `$OS` - Betriebssystem: `windows`, `linux`, `mac` - `$ARCH` - Architektur: `386`, `amd64`, `arm64`

**Beispiel:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Ergebnis unter Windows AMD64:**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Dies ermöglicht einzelne plugin.config-Dateien für plattformspezifische Builds.

---

## Verzeichnisstruktur

### Standardlayout

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Verzeichniszwecke

**console/locale/** - JAR-Dateien mit Ressourcenbündeln für I2P-Basisübersetzungen - Plugin-spezifische Übersetzungen sollten in `console/webapps/*.war` oder `lib/*.jar` liegen

**console/themes/** - Jedes Unterverzeichnis enthält ein vollständiges Konsolen-Theme - Automatisch zum Theme-Suchpfad hinzugefügt

**console/webapps/** - `.war`-Dateien zur Konsolenintegration - Wird automatisch gestartet, sofern nicht in `webapps.config` deaktiviert - Der WAR-Name muss nicht mit dem Plugin-Namen übereinstimmen

**eepsite/** - Vollständige eepsite mit eigener Jetty-Instanz - Erfordert eine `jetty.xml`-Konfiguration mit Variablenersetzung - Siehe zzzot- und pebble-Plugin-Beispiele

**lib/** - JAR-Bibliotheken für Plugins - Im Klassenpfad über `clients.config` oder `webapps.config` angeben

---

## Webapp-Konfiguration

### webapps.config-Format

Standard-I2P-Konfigurationsdatei zur Steuerung des Verhaltens der Web-App.

**Syntax:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Wichtige Hinweise:** - Vor router 0.7.12-9 verwenden Sie `plugin.warname.startOnLoad` zur Kompatibilität - Vor API 0.9.53 funktionierte der Klassenpfad nur, wenn der WAR-Name mit dem Plugin-Namen übereinstimmte - Seit 0.9.53+ funktioniert der Klassenpfad für jeden Webanwendungsnamen

### Bewährte Verfahren für Webanwendungen

1. **ServletContextListener-Implementierung**
   - `javax.servlet.ServletContextListener` zur Bereinigung implementieren
   - Oder `destroy()` im Servlet überschreiben
   - Stellt eine ordnungsgemäße Beendigung während Aktualisierungen und beim Stoppen des router sicher

2. **Bibliotheksverwaltung**
   - Gemeinsam genutzte JARs in `lib/` ablegen, nicht innerhalb der WAR
   - Über den Klassenpfad in `webapps.config` referenzieren
   - Ermöglicht die getrennte Installation/Aktualisierung von Plugins

3. **Konflikte mit Bibliotheken vermeiden**
   - Bündeln Sie niemals Jetty-, Tomcat- oder Servlet-JARs
   - Bündeln Sie niemals JARs aus der Standard-I2P-Installation
   - Prüfen Sie den Classpath-Abschnitt auf Standardbibliotheken

4. **Kompilierungsanforderungen**
   - Keine `.java`- oder `.jsp`-Quelldateien einbeziehen
   - Alle JSPs vorkompilieren, um Startverzögerungen zu vermeiden
   - Es kann nicht von der Verfügbarkeit eines Java-/JSP-Compilers ausgegangen werden

5. **Servlet-API-Kompatibilität**
   - I2P unterstützt Servlet 3.0 (seit 0.9.30)
   - **Annotation-Scanning wird NICHT unterstützt** (@WebContent)
   - Der traditionelle Deployment-Deskriptor `web.xml` ist erforderlich

6. **Jetty-Version**
   - Aktuell: Jetty 9 (I2P 0.9.30+)
   - Verwenden Sie `net.i2p.jetty.JettyStart` als Abstraktionsschicht
   - Schützt vor Änderungen der Jetty-API

---

## Client-Konfiguration

### clients.config-Format

Definiert Clients (Dienste), die vom Plugin gestartet werden.

**Grundlegender Client:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Client mit Stoppen/Deinstallieren:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Eigenschaftsreferenz

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Variablenersetzung

Die folgenden Variablen werden in `args`, `stopargs`, `uninstallargs` und `classpath` ersetzt:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Verwaltete vs. nicht verwaltete Clients

**Verwaltete Clients (empfohlen seit 0.9.4):** - Instanziiert von ClientAppManager - Verwaltet Referenz- und Zustandsverfolgung - Einfacheres Lebenszyklus-Management - Besseres Speichermanagement

**Nicht verwaltete Clients:** - Vom router gestartet, keine Zustandsverfolgung - Müssen mehrere Start-/Stopp-Aufrufe ordnungsgemäß behandeln - Zur Koordination statische Zustandsinformationen oder PID-Dateien verwenden - Beim Herunterfahren des router aufgerufen (seit 0.7.12-3)

### ShellService (seit 0.9.53 / 1.7.0)

Verallgemeinerte Lösung zum Ausführen externer Programme mit automatischer Zustandsverfolgung.

**Funktionen:** - Verwaltet den Prozesslebenszyklus - Kommuniziert mit ClientAppManager - Automatische PID-Verwaltung - Plattformübergreifende Unterstützung

**Verwendung:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Für plattformspezifische Skripte:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternative (veraltet):** Schreibe einen Java-Wrapper, der den Betriebssystemtyp prüft, und rufe `ShellCommand` mit der entsprechenden `.bat`- oder `.sh`-Datei auf.

---

## Installationsprozess

### Installationsablauf für Benutzer

1. Benutzer fügt die Plugin-URL auf der Plugin-Konfigurationsseite der Router Console (`/configplugins`) ein
2. Router lädt die Plugin-Datei herunter
3. Signaturprüfung (schlägt fehl, wenn der Schlüssel unbekannt ist und der Strict-Modus aktiviert ist)
4. ZIP-Integritätsprüfung
5. Extrahieren und Parsen von `plugin.config`
6. Überprüfung der Versionskompatibilität (`min-i2p-version`, `min-java-version`, usw.)
7. Erkennung von Konflikten bei Webapp-Namen
8. Vorhandenes Plugin stoppen, falls es sich um ein Update handelt
9. Verzeichnisvalidierung (muss unter `plugins/` liegen)
10. Alle Dateien in das Plugin-Verzeichnis extrahieren
11. `plugins.config` aktualisieren
12. Plugin starten (außer wenn `dont-start-at-install=true`)

### Sicherheit und Vertrauen

**Schlüsselverwaltung:** - First-key-seen (erstmals gesehener Schlüssel) Vertrauensmodell für neue Signierer - Nur die Schlüssel von jrandom und zzz sind mitgeliefert - Seit 0.9.14.1 werden unbekannte Schlüssel standardmäßig abgelehnt - Eine erweiterte Eigenschaft kann dies für Entwicklungszwecke außer Kraft setzen

**Installationsbeschränkungen:** - Archive dürfen ausschließlich in das Plugin-Verzeichnis entpackt werden - Das Installationsprogramm lehnt Pfade außerhalb von `plugins/` ab - Plugins können nach der Installation auf Dateien an anderen Orten zugreifen - Kein Sandboxing oder Privilegien-Trennung

---

## Aktualisierungsmechanismus

### Ablauf der Aktualisierungsprüfung

1. Router liest `updateURL.su3` (bevorzugt) oder `updateURL` aus plugin.config
2. HTTP HEAD oder partielle GET-Anfrage, um die Bytes 41-56 abzurufen
3. Versionsstring aus der entfernten Datei extrahieren
4. Mit der installierten Version vergleichen, mithilfe von VersionComparator
5. Falls neuer, den Benutzer auffordern oder automatisch herunterladen (abhängig von den Einstellungen)
6. Plugin stoppen
7. Update installieren
8. Plugin starten (sofern die Benutzereinstellung nicht geändert wurde)

### Versionsvergleich

Versionen werden als durch Punkt/Bindestrich/Unterstrich getrennte Komponenten interpretiert: - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Maximale Länge:** 16 Bytes (muss mit dem SUD/SU3-Header übereinstimmen)

### Bewährte Verfahren für Aktualisierungen

1. Bei Releases die Versionsnummer immer erhöhen
2. Update-Pfad von der vorherigen Version testen
3. Bei größeren Änderungen `router-restart-required` berücksichtigen
4. Während der Migration sowohl `updateURL` als auch `updateURL.su3` bereitstellen
5. Für Tests ein Suffix der Buildnummer verwenden (`1.2.3-456`)

---

## Klassenpfad und Standardbibliotheken

### Immer im Klassenpfad verfügbar

Die folgenden JAR-Dateien aus `$I2P/lib` sind für I2P 0.9.30+ immer im Klassenpfad:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Besondere Hinweise

**commons-logging.jar:** - Seit 0.9.30 leer - Vor 0.9.30: Apache Tomcat JULI - Vor 0.9.24: Commons Logging + JULI - Vor 0.9: Nur Commons Logging

**jasper-compiler.jar:** - Seit Jetty 6 (0.9) leer

**systray4j.jar:** - Entfernt in 0.9.26

### Nicht im Klassenpfad (muss angegeben werden)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Spezifikation des Klassenpfads

**In clients.config:**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**In webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Wichtig:** Seit 0.7.13-3 sind Klassenpfade threadspezifisch, nicht JVM-weit. Geben Sie für jeden Client den vollständigen Klassenpfad an.

---

## Anforderungen an die Java-Version

### Aktuelle Anforderungen (Oktober 2025)

**I2P 2.10.0 und älter:** - Mindestens: Java 7 (erforderlich seit 0.9.24, Januar 2016) - Empfohlen: Java 8 oder höher

**I2P 2.11.0 und neuer (BEVORSTEHEND):** - **Mindestanforderung: Java 17+** (angekündigt in den Versionshinweisen zu 2.9.0) - Warnung zwei Versionen im Voraus gegeben (2.9.0 → 2.10.0 → 2.11.0)

### Kompatibilitätsstrategie für Plugins

**Für maximale Kompatibilität (bis einschließlich I2P 2.10.x):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Für Funktionen ab Java 8:**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Für Funktionen in Java 11+:**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Vorbereitung auf 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Bewährte Praktiken für die Kompilierung

**Beim Kompilieren mit einem neueren JDK für eine ältere Zielversion:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Dies verhindert die Verwendung von APIs, die in der Ziel-Java-Version nicht verfügbar sind.

---

## Pack200-Komprimierung - VERALTET

### Kritisches Update: Pack200 nicht verwenden

**Status:** Veraltet und entfernt

Die ursprüngliche Spezifikation empfahl nachdrücklich die Pack200-Komprimierung zur Reduzierung der Größe um 60-65 %. **Dies ist nicht mehr gültig.**

**Zeitleiste:** - **JEP 336:** Pack200 in Java 11 als veraltet markiert (September 2018) - **JEP 367:** Pack200 in Java 14 entfernt (März 2020)

**Die offizielle Spezifikation für I2P-Updates besagt:** > "JAR- und WAR-Dateien im ZIP-Archiv werden nicht mehr mit pack200 komprimiert, wie oben für 'su2'-Dateien dokumentiert, da neuere Java-Laufzeitumgebungen dies nicht mehr unterstützen."

**Was ist zu tun:**

1. **pack200 umgehend aus den Build-Prozessen entfernen**
2. **Standard-ZIP-Komprimierung verwenden**
3. **Alternativen in Betracht ziehen:**
   - ProGuard/R8 zur Code-Verkleinerung
   - UPX für native Binärdateien
   - Moderne Kompressionsalgorithmen (zstd, brotli), sofern ein eigener Entpacker bereitgestellt wird

**Für bestehende Plugins:** - Alte routers (0.7.11-5 bis einschließlich Java 10) können pack200 weiterhin entpacken - Neue routers (Java 11+) können pack200 nicht entpacken - Plugins ohne pack200-Komprimierung neu veröffentlichen

---

## Signaturschlüssel und Sicherheit

### Schlüsselgenerierung (SU3-Format)

Verwenden Sie das Skript `makeplugin.sh` aus dem Repository i2p.scripts:

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Wichtige Details:** - Algorithmus: RSA_SHA512_4096 - Format: X.509-Zertifikat - Speicherformat: Java-Keystore-Format

### Signieren von Plugins

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Bewährte Verfahren für das Schlüsselmanagement

1. **Einmal generieren, für immer schützen**
   - Routers lehnen doppelte Schlüsselnamen mit unterschiedlichen Schlüsseln ab
   - Routers lehnen doppelte Schlüssel mit unterschiedlichen Schlüsselnamen ab
   - Updates werden abgelehnt, wenn Schlüssel und Name nicht übereinstimmen

2. **Sichere Speicherung**
   - Sicheres Backup des Keystores erstellen
   - Starke Passphrase verwenden
   - Niemals in die Versionsverwaltung committen

3. **Schlüsselrotation**
   - Wird von der aktuellen Architektur nicht unterstützt
   - Langfristige Schlüsselnutzung einplanen
   - Multisignaturverfahren für die Teamentwicklung in Betracht ziehen

### Veraltete DSA-Signierung (XPI2P)

**Status:** Funktionsfähig, aber veraltet

Vom xpi2p-Format verwendete DSA-1024-Signaturen: - 40-Byte-Signatur - 172 base64-Zeichen langer öffentlicher Schlüssel - NIST-800-57 empfiehlt mindestens (L=2048, N=224) - I2P verwendet schwächere (L=1024, N=160)

**Empfehlung:** Verwenden Sie stattdessen SU3 (I2P-Update-Paketformat) mit RSA-4096.

---

## Richtlinien für die Plugin-Entwicklung

### Wesentliche bewährte Verfahren

1. **Dokumentation**
   - Ein klares README mit Installationsanleitung bereitstellen
   - Konfigurationsoptionen und Standardwerte dokumentieren
   - Bei jeder Veröffentlichung ein Änderungsprotokoll beifügen
   - Erforderliche I2P/Java-Versionen angeben

2. **Größenoptimierung**
   - Nur erforderliche Dateien einschließen
   - Niemals router JARs bündeln
   - Installations- vs. Update-Pakete trennen (Bibliotheken in lib/)
   - ~~Pack200-Kompression verwenden~~ **VERALTET - Standard-ZIP verwenden**

3. **Konfiguration**
   - Niemals `plugin.config` zur Laufzeit ändern
   - Verwenden Sie eine separate Konfigurationsdatei für Laufzeiteinstellungen
   - Dokumentieren Sie die erforderlichen router-Einstellungen (SAM-Ports, tunnels, usw.)
   - Respektieren Sie die vorhandene Konfiguration des Benutzers

4. **Ressourcennutzung**
   - Aggressiven Bandbreitenverbrauch als Voreinstellung vermeiden
   - Angemessene Grenzen für die CPU-Auslastung implementieren
   - Ressourcen beim Beenden bereinigen
   - Daemon-Threads dort verwenden, wo es angebracht ist

5. **Tests**
   - Installieren/Aktualisieren/Deinstallieren auf allen Plattformen testen
   - Updates von der vorherigen Version testen
   - Während der Updates das Stoppen/Neustarten der Webapp überprüfen
   - Mit der minimal unterstützten I2P-Version testen

6. **Dateisystem**
   - Schreiben Sie niemals in `$I2P` (kann schreibgeschützt sein)
   - Schreiben Sie Laufzeitdaten in `$PLUGIN` oder `$CONFIG`
   - Verwenden Sie `I2PAppContext` zum Auffinden von Verzeichnissen
   - Gehen Sie nicht von einem bestimmten `$CWD`-Pfad aus (aktuelles Arbeitsverzeichnis)

7. **Kompatibilität**
   - Standard-I2P-Klassen nicht duplizieren
   - Klassen bei Bedarf erweitern, nicht ersetzen
   - `min-i2p-version`, `min-jetty-version` in plugin.config prüfen
   - Mit älteren I2P-Versionen testen, falls diese unterstützt werden

8. **Shutdown-Handhabung**
   - Ordnungsgemäße `stopargs` in clients.config implementieren
   - Shutdown-Hooks registrieren: `I2PAppContext.addShutdownTask()`
   - Mehrfache Start/Stop-Aufrufe sauber behandeln
   - Alle Threads auf Daemon-Modus setzen

9. **Sicherheit**
   - Alle externen Eingaben validieren
   - Niemals `System.exit()` aufrufen
   - Die Privatsphäre der Benutzer respektieren
   - Sichere Programmierpraktiken befolgen

10. **Lizenzierung**
    - Plugin-Lizenz klar angeben
    - Lizenzen der mitgelieferten Bibliotheken respektieren
    - Erforderliche Namensnennung beifügen
    - Zugang zum Quellcode bereitstellen, falls erforderlich

### Erweiterte Überlegungen

**Zeitzonenbehandlung:** - Router setzt die JVM-Zeitzone auf UTC - Tatsächliche Zeitzone des Benutzers: `I2PAppContext`-Eigenschaft `i2p.systemTimeZone`

**Verzeichniserkennung:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Versionsnummerierung:** - Verwende semantische Versionierung (major.minor.patch) - Füge eine Build-Nummer für Tests hinzu (1.2.3-456) - Stelle sicher, dass die Version bei Updates monoton steigt

**Zugriff auf router-Klassen:** - Generell Abhängigkeiten von `router.jar` vermeiden - Stattdessen öffentliche APIs in `i2p.jar` verwenden - Künftiges I2P könnte den Zugriff auf router-Klassen einschränken

**Vermeidung von JVM-Abstürzen (historisch):** - Behoben in 0.7.13-3 - Classloader korrekt verwenden - Aktualisieren von JARs in einem laufenden Plugin vermeiden - Bei Bedarf so auslegen, dass beim Update ein Neustart erfolgt

---

## Eepsite-Plugins

### Übersicht

Plugins können vollständige eepsites mit eigenen Jetty- und I2PTunnel-Instanzen bereitstellen.

### Architektur

**Nicht versuchen:** - In eine bestehende eepsite zu installieren - Mit der Standard-eepsite des router zusammenzuführen - Von der Verfügbarkeit einer einzelnen eepsite auszugehen

**Stattdessen:** - Neue I2PTunnel-Instanz starten (über die Kommandozeile) - Neue Jetty-Instanz starten - Beide in `clients.config` konfigurieren

### Beispielstruktur

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Variablensubstitution in jetty.xml

Verwenden Sie die Variable `$PLUGIN` für Pfade:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Der Router führt während des Plugin-Starts eine Ersetzung durch.

### Beispiele

Referenzimplementierungen: - **zzzot-Plugin** - Torrent-Tracker - **pebble-Plugin** - Blog-Plattform

Beide sind auf der Plugin-Seite von zzz verfügbar (I2P-intern).

---

## Konsolenintegration

### Links der Übersichtsleiste

Klickbaren Link zur Zusammenfassungsleiste der Routerkonsole hinzufügen:

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Lokalisierte Versionen:

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Konsolensymbole

**Image-Datei (seit 0.9.20):**

```properties
console-icon=/myicon.png
```
Pfad relativ zu `consoleLinkURL`, falls angegeben (seit 0.9.53), andernfalls relativ zum Webapp-Namen.

**Eingebettetes Icon (seit 0.9.25):**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Erzeugen mit:

```bash
base64 -w 0 icon-32x32.png
```
Oder Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Anforderungen: - 32x32 Pixel - PNG-Format - Base64-kodiert (keine Zeilenumbrüche)

---

## Internationalisierung

### Übersetzungspakete

**Für I2P-Basisübersetzungen:** - JARs in `console/locale/` ablegen - Beinhalten Resource-Bundles für bestehende I2P-Apps - Benennung: `messages_xx.properties` (xx = Sprachcode)

**Für pluginspezifische Übersetzungen:** - In `console/webapps/*.war` aufnehmen - Oder in `lib/*.jar` aufnehmen - Den Standardansatz mit dem Java ResourceBundle (Ressourcenbündel) verwenden

### Lokalisierte Zeichenketten in plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Unterstützte Felder: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Übersetzung des Konsolen-Themes

Themes in `console/themes/` werden automatisch zum Suchpfad für Themes hinzugefügt.

---

## Plattformspezifische Plugins

### Ansatz mit separaten Paketen

Verwenden Sie für jede Plattform unterschiedliche Plugin-Namen:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Ansatz der Variablenersetzung

Eine einzelne plugin.config mit Plattformvariablen:

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
In der Datei clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Betriebssystemerkennung zur Laufzeit

Java-Ansatz für bedingte Ausführung:

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Fehlerbehebung

### Häufige Probleme

**Plugin startet nicht:** 1. Überprüfe die I2P-Versionskompatibilität (`min-i2p-version`) 2. Überprüfe die Java-Version (`min-java-version`) 3. Überprüfe die router-Protokolle auf Fehler 4. Überprüfe, ob alle erforderlichen JARs im Classpath vorhanden sind

**Webapp nicht erreichbar:** 1. Bestätigen Sie, dass `webapps.config` die Webapp nicht deaktiviert 2. Prüfen Sie die Jetty-Versionskompatibilität (`min-jetty-version`) 3. Stellen Sie sicher, dass `web.xml` vorhanden ist (Annotation-Scanning wird nicht unterstützt) 4. Prüfen Sie auf konfliktierende Webapp-Namen

**Update schlägt fehl:** 1. Prüfen, ob die Versionsnummer erhöht wurde 2. Prüfen, ob die Signatur mit dem Signierschlüssel übereinstimmt 3. Sicherstellen, dass der Plugin-Name der installierten Version entspricht 4. Einstellungen `update-only`/`install-only` überprüfen

**Externes Programm lässt sich nicht beenden:** 1. ShellService für die automatische Lebenszyklusverwaltung verwenden 2. Ordnungsgemäße Behandlung von `stopargs` implementieren 3. Bereinigung der PID-Datei überprüfen 4. Prozessbeendigung überprüfen

### Debug-Protokollierung

Debug-Logging im router aktivieren:

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Protokolle prüfen:

```
~/.i2p/logs/log-router-0.txt
```
---

## Referenzinformationen

### Offizielle Spezifikationen

- [Plugin-Spezifikation](/docs/specs/plugin/)
- [Konfigurationsformat](/docs/specs/configuration/)
- [Update-Spezifikation](/docs/specs/updates/)
- [Kryptografie](/docs/specs/cryptography/)

### I2P-Versionsgeschichte

**Aktuelle Version:** - **I2P 2.10.0** (8. September 2025)

**Wichtige Veröffentlichungen seit 0.9.53:** - 2.10.0 (Sep 2025) - Ankündigung für Java 17+ - 2.9.0 (Jun 2025) - Warnung zu Java 17+ - 2.8.0 (Okt 2024) - Tests zu Post-Quanten-Kryptografie - 2.6.0 (Mai 2024) - Sperrung von I2P-over-Tor - 2.4.0 (Dez 2023) - NetDB-Sicherheitsverbesserungen - 2.2.0 (Mär 2023) - Überlastkontrolle - 2.1.0 (Jan 2023) - Netzwerkverbesserungen - 2.0.0 (Nov 2022) - SSU2-Transportprotokoll - 1.7.0/0.9.53 (Feb 2022) - ShellService, Variablensubstitution - 0.9.15 (Sep 2014) - SU3-Format eingeführt

**Versionsnummerierung:** - 0.9.x-Serie: Bis einschließlich Version 0.9.53 - 2.x-Serie: Ab 2.0.0 (Einführung von SSU2)

### Entwicklerressourcen

**Quellcode:** - Haupt-Repository: https://i2pgit.org/I2P_Developers/i2p.i2p - GitHub-Spiegel: https://github.com/i2p/i2p.i2p

**Plugin-Beispiele:** - zzzot (BitTorrent-Tracker) - pebble (Blog-Plattform) - i2p-bote (serverlose E-Mail) - orchid (Tor-Client) - seedless (Peer-Austausch)

**Build-Tools:** - makeplugin.sh - Schlüsselgenerierung und Signierung - Im i2p.scripts-Repository zu finden - Automatisiert die Erstellung und Verifizierung von su3

### Community-Unterstützung

**Foren:** - [I2P Forum](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (I2P-intern)

**IRC/Chat:** - #i2p-dev auf OFTC - I2P IRC im Netzwerk

---

## Anhang A: Vollständiges Beispiel für plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Anhang B: Vollständiges clients.config-Beispiel

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Anhang C: Vollständiges webapps.config-Beispiel

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Anhang D: Migrations-Checkliste (von 0.9.53 auf 2.10.0)

### Erforderliche Änderungen

- [ ] **Pack200-Komprimierung aus dem Build-Prozess entfernen**
  - pack200-Aufgaben aus Ant-/Maven-/Gradle-Skripten entfernen
  - Vorhandene Plugins ohne pack200 erneut veröffentlichen

- [ ] **Java-Versionsanforderungen überprüfen**
  - Erwägen, für neue Funktionen Java 11+ vorauszusetzen
  - Planen, in I2P 2.11.0 Java 17+ zur Voraussetzung zu machen
  - Die `min-java-version` in plugin.config aktualisieren

- [ ] **Dokumentation aktualisieren**
  - Pack200-Verweise entfernen
  - Java-Versionsanforderungen aktualisieren
  - I2P-Versionsverweise aktualisieren (0.9.x → 2.x)

### Empfohlene Änderungen

- [ ] **Kryptografische Signaturen stärken**
  - Von XPI2P (I2P-Plugin-Paketformat) zu SU3 (signiertes I2P-Update-/Datenpaketformat) migrieren, falls noch nicht geschehen
  - RSA-4096-Schlüssel für neue Plugins verwenden

- [ ] **Neue Funktionen nutzen (bei Verwendung von 0.9.53+)**
  - Verwenden Sie die Variablen `$OS` / `$ARCH` für plattformspezifische Updates
  - Verwenden Sie ShellService (Dienst zum Ausführen externer Programme) für externe Programme
  - Verwenden Sie den verbesserten Webapp-Classpath (Klassenpfad der Webanwendung; funktioniert mit jedem warname [Name der WAR-Datei])

- [ ] **Kompatibilität testen**
  - Mit I2P 2.10.0 testen
  - Mit Java 8, 11, 17 überprüfen
  - Unter Windows, Linux, macOS prüfen

### Optionale Erweiterungen

- [ ] Einen korrekten ServletContextListener implementieren
- [ ] Lokalisierte Beschreibungen hinzufügen
- [ ] Ein Konsolensymbol bereitstellen
- [ ] Die Handhabung des Herunterfahrens verbessern
- [ ] Umfassende Protokollierung hinzufügen
- [ ] Automatisierte Tests schreiben
