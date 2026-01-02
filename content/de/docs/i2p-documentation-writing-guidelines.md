---
title: "Richtlinien zum Verfassen der I2P-Dokumentation"
description: "Stellen Sie Konsistenz, Genauigkeit und Barrierefreiheit in der gesamten technischen I2P-Dokumentation sicher"
slug: "writing-guidelines"
lastUpdated: "2025-10"
---

**Zweck:** Konsistenz, Genauigkeit und Barrierefreiheit in der technischen I2P-Dokumentation sicherstellen

---

## Grundprinzipien

### 1. Alles überprüfen

**Niemals etwas annehmen oder raten.** Alle technischen Aussagen müssen anhand folgender Quellen verifiziert werden: - Aktueller I2P-Quellcode (https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master) - Offizielle API-Dokumentation (https://i2p.github.io/i2p.i2p/  - Konfigurationsspezifikationen [/docs/specs/](/docs/) - Aktuelle Versionshinweise [/releases/](/categories/release/)

**Beispiel für eine korrekte Verifizierung:**

```markdown
❌ BAD: "The ClientApp interface probably requires three constructor parameters."
✅ GOOD: "The ClientApp interface requires this constructor signature: 
         public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)"
```
### 2. Klarheit vor Kürze

Schreiben Sie für Entwicklerinnen und Entwickler, die I2P möglicherweise zum ersten Mal kennenlernen. Erklären Sie die Konzepte umfassend, statt Vorwissen vorauszusetzen.

**Beispiel:**

```markdown
❌ BAD: "Use the port mapper for service discovery."
✅ GOOD: "The port mapper offers a simple directory for internal TCP services. 
         Register loopback ports so other applications can discover your service 
         without hardcoded addresses."
```
### 3. Barrierefreiheit zuerst

Die Dokumentation muss für Entwickler im Clearnet (normales Internet) zugänglich sein, obwohl I2P ein Overlay-Netzwerk ist. Stellen Sie stets über das Clearnet zugängliche Alternativen zu I2P-internen Ressourcen bereit.

---

## Technische Richtigkeit

### API- und Schnittstellendokumentation

**Immer angeben:** 1. Vollständige Paketnamen bei der ersten Erwähnung: `net.i2p.app.ClientApp` 2. Vollständige Methodensignaturen mit Rückgabetypen 3. Parameternamen und -typen 4. Erforderliche vs. optionale Parameter

**Beispiel:**

```markdown
The `startup()` method has signature `void startup() throws IOException` and must 
execute without blocking. The method must call `ClientAppManager.notify()` at least 
once to transition from INITIALIZED state.
```
### Konfigurationseigenschaften

Beim Dokumentieren von Konfigurationsdateien: 1. Exakte Eigenschaftsnamen angeben 2. Dateizeichenkodierung angeben (UTF-8 für I2P-Konfigurationsdateien) 3. Vollständige Beispiele bereitstellen 4. Standardwerte dokumentieren 5. Version vermerken, in der Eigenschaften eingeführt/geändert wurden

**Beispiel:**

```markdown
### clients.config Properties

**Required:**
- `clientApp.N.main` - Full class name (no default)

**Optional:**
- `clientApp.N.delay` - Seconds before starting (default: 120)
- `clientApp.N.onBoot` - Forces delay=0 if true (default: false, added in 0.9.4)
```
### Konstanten und Aufzählungen

Verwenden Sie beim Dokumentieren von Konstanten die tatsächlichen Namen im Code:

```markdown
❌ BAD: "Common registrations include console, i2ptunnel, Jetty, sam, and bob"

✅ GOOD: "Common port mapper service constants from `net.i2p.util.PortMapper`:
- `SVC_CONSOLE` - Router console (default port 7657)
- `SVC_HTTP_PROXY` - HTTP proxy (default port 4444)
- `SVC_SAM` - SAM bridge (default port 7656)"
```
### Ähnliche Konzepte voneinander unterscheiden

I2P hat mehrere sich überschneidende Systeme. Stellen Sie immer klar, welches System Sie dokumentieren:

**Beispiel:**

```markdown
Note that client registry and port mapper are separate systems:
- **ClientAppManager registry** enables inter-application communication by name lookup
- **PortMapper** maps service names to host:port combinations for service discovery
- **i2ptunnel tunnel types** are configuration values (tunnel.N.type), not service registrations
```
---

## Dokumentations-URLs und Referenzen

### Regeln für die Erreichbarkeit von URLs

1. **Primäre Referenzen** sollten im Clearnet erreichbare URLs verwenden
2. **I2P-interne URLs** (.i2p-Domains) müssen Hinweise zur Erreichbarkeit enthalten
3. **Immer Alternativen bereitstellen**, wenn auf I2P-interne Ressourcen verlinkt wird

**Vorlage für I2P-interne URLs:**

```markdown
> **Note:** The I2P network hosts comprehensive documentation at http://idk.i2p/javadoc-i2p/ 
> which requires an I2P router for access. For clearnet access, use the GitHub Pages 
> mirror at https://eyedeekay.github.io/javadoc-i2p/
```
### Empfohlene I2P-Referenz-URLs

**Offizielle Spezifikationen:** - [Konfiguration](/docs/specs/configuration/) - [Plugin](/docs/specs/plugin/) - [Dokumentenindex](/docs/)

**API-Dokumentation (jeweils die aktuellste wählen):** - Aktuellste: https://i2p.github.io/i2p.i2p/ (API 0.9.66 mit Stand I2P 2.10.0) - Clearnet-Spiegel: https://eyedeekay.github.io/javadoc-i2p/

**Quellcode:** - GitLab (offiziell): https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master - GitHub-Spiegel: https://github.com/i2p/i2p.i2p

### Standards für Linkformate

```markdown
✅ GOOD: [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
✅ GOOD: [Configuration Specification](https://geti2p.net/spec/configuration)

❌ BAD: See the ClientApp docs at http://idk.i2p/...
❌ BAD: [link](url) with no descriptive text
```
---

## Versionsverfolgung

### Dokumentmetadaten

Jedes technische Dokument sollte im frontmatter (Metadaten-Block am Dokumentanfang) Versionsmetadaten enthalten:

```markdown
---
title: "Document Title"
description: "Brief description"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
**Felddefinitionen:** - `lastUpdated`: Jahr und Monat, in dem das Dokument zuletzt überprüft/aktualisiert wurde - `accurateFor`: I2P-Version, gegen die das Dokument verifiziert wurde - `reviewStatus`: Eines von "draft", "needs-review", "verified", "outdated"

### Versionsverweise im Inhalt

Bei Versionsangaben: 1. Setze die aktuelle Version in **Fettschrift**: "**Version 2.10.0** (September 2025)" 2. Gib bei historischen Verweisen sowohl die Versionsnummer als auch das Datum an 3. Führe die API-Version, falls relevant, getrennt von der I2P-Version auf

**Beispiel:**

```markdown
Managed clients were introduced in **version 0.9.4** (December 17, 2012) and 
remain the recommended architecture as of **version 2.10.0** (September 9, 2025). 
The current API version is **0.9.66**.
```
### Änderungen im Laufe der Zeit dokumentieren

Für Funktionen, die sich weiterentwickelt haben:

```markdown
**Version history:**
- **0.9.4 (December 2012)** - Managed clients introduced
- **0.9.42 (2019)** - clients.config.d/ directory structure added
- **1.7.0 (2021)** - ShellService added for external program tracking
- **2.10.0 (September 2025)** - Current release, no API changes to managed clients
```
### Abkündigungshinweise

Beim Dokumentieren veralteter Funktionen:

```markdown
> **Deprecated:** This feature was deprecated in version X.Y.Z and will be removed 
> in version A.B.C. Use [alternative feature](link) instead.
```
---

## Terminologiestandards

### Offizielle I2P-Begriffe

Verwenden Sie diese exakten Begriffe durchgängig:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct Term</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Avoid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P node, I2P client (ambiguous)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">eepsite</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P website, hidden service (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">connection, circuit (Tor term)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">netDb</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">network database, DHT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lease set</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination info</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">address, endpoint</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">base64 destination</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P address, .i2p address</td>
    </tr>
  </tbody>
</table>
### Terminologie für verwaltete Clients

Bei der Dokumentation verwalteter Clients:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use This</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">managed application</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unmanaged client</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">legacy client, static client</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ClientAppManager</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application manager, client manager</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">lifecycle methods</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">state methods, control methods</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">client registry</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">application registry, name service</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port mapper</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">port registry, service directory</td>
    </tr>
  </tbody>
</table>
### Konfigurationsbegriffe

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Correct</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Incorrect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.cfg, client.config</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>clients.config.d/</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">clients.d/, config.d/</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.cfg</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.config</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel.config</td>
    </tr>
  </tbody>
</table>
### Paket- und Klassennamen

Verwenden Sie bei der ersten Erwähnung immer den vollqualifizierten Namen, danach die Kurzform:

```markdown
The `net.i2p.app.ClientApp` interface requires implementation of three lifecycle 
methods. When a ClientApp starts, the manager calls `startup()`...
```
---

## Codebeispiele und Formatierung

### Java-Codebeispiele

Verwenden Sie eine korrekte Syntaxhervorhebung und vollständige Beispiele:

```markdown
### Example: Registering with Port Mapper

\`\`\`java
// Register HTTP proxy service
context.portMapper().register(
    PortMapper.SVC_HTTP_PROXY, 
    "127.0.0.1", 
    4444
);

// Later, retrieve the port
int port = context.portMapper().getPort(PortMapper.SVC_HTTP_PROXY);
if (port == -1) {
    // Service not registered
}
\`\`\`
```
**Anforderungen an Codebeispiele:** 1. Kommentare hinzufügen, die wichtige Zeilen erklären 2. Fehlerbehandlung zeigen, wo relevant 3. Realistische Variablennamen verwenden 4. I2P-Codekonventionen einhalten (Einrückung mit 4 Leerzeichen) 5. Import-Anweisungen angeben, falls nicht aus dem Kontext ersichtlich

### Konfigurationsbeispiele

Vollständige, gültige Konfigurationsbeispiele anzeigen:

```markdown
### Example: clients.config.d/ Entry

File: `clients.config.d/00-console.config`

\`\`\`properties
# Router console configuration
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
\`\`\`
```
### Beispiele für die Kommandozeile

Verwenden Sie `$` für Benutzerbefehle, `#` für root:

```markdown
\`\`\`bash
# Install I2P on Debian/Ubuntu
$ sudo apt-get install i2p

# Start the router
$ i2prouter start
\`\`\`
```
### Inline-Code

Verwenden Sie Backticks für: - Methodennamen: `startup()` - Klassennamen: `ClientApp` - Eigenschaftsnamen: `clientApp.0.main` - Dateinamen: `clients.config` - Konstanten: `SVC_HTTP_PROXY` - Paketnamen: `net.i2p.app`

---

## Tonfall und Stimme

### Professionell, aber zugänglich

Schreiben Sie für ein technisches Fachpublikum, ohne herablassend zu wirken:

```markdown
❌ BAD: "Obviously, you should implement the startup() method."
✅ GOOD: "Managed clients must implement the startup() method to initialize resources."

❌ BAD: "Even a junior dev knows you need to call notify()."
✅ GOOD: "The manager requires at least one notify() call during startup to track state transitions."
```
### Aktiv

Verwenden Sie die Aktivform für mehr Klarheit:

```markdown
❌ PASSIVE: "The ClientAppManager is notified by the client when state changes."
✅ ACTIVE: "The client notifies ClientAppManager when state changes."
```
### Imperativ für Anweisungen

Verwenden Sie direkte Imperative in prozeduralen Inhalten:

```markdown
✅ "Implement these three lifecycle methods:"
✅ "Call manager.notify() after changing state."
✅ "Register services using context.portMapper().register()"
```
### Unnötigen Fachjargon vermeiden

Begriffe bei der ersten Erwähnung erläutern:

```markdown
✅ GOOD: "The netDb (network database) stores information about I2P routers and destinations."
❌ BAD: "Query the netDb for peer info." (no explanation)
```
### Richtlinien zur Zeichensetzung

1. **Keine Em-Dashes (Geviertstriche)** - stattdessen normale Bindestriche, Kommas oder Semikolons verwenden
2. Oxford-Komma in Aufzählungen verwenden: "console, i2ptunnel, and Jetty"
3. **Punkte innerhalb von Codeblöcken** nur, wenn es grammatisch notwendig ist
4. **Serielle Listen** verwenden Semikolons, wenn Elemente Kommas enthalten

---

## Dokumentstruktur

### Standardreihenfolge der Abschnitte

Für die API-Dokumentation:

1. **Übersicht** - was die Funktion tut, warum sie existiert
2. **Implementierung** - wie man sie implementiert/verwendet
3. **Konfiguration** - wie man sie konfiguriert
4. **API-Referenz** - detaillierte Beschreibungen von Methoden und Eigenschaften
5. **Beispiele** - vollständige, lauffähige Beispiele
6. **Bewährte Vorgehensweisen** - Tipps und Empfehlungen
7. **Versionsverlauf** - wann eingeführt, Änderungen im Laufe der Zeit
8. **Referenzen** - Links zu verwandter Dokumentation

### Überschriftenhierarchie

Verwenden Sie semantische Überschriftenebenen:

```markdown
# Document Title (h1 - only one per document)

## Major Section (h2)

### Subsection (h3)

#### Detail Section (h4)

**Bold text for emphasis within sections**
```
### Informationskästen

Verwenden Sie Blockzitate für besondere Hinweise:

```markdown
> **Note:** Additional information that clarifies the main content.

> **Warning:** Important information about potential issues or breaking changes.

> **Deprecated:** This feature is deprecated and will be removed in version X.Y.Z.

> **Status:** Current implementation status or version information.
```
### Listen und Organisation

**Ungeordnete Listen** für nicht-sequenzielle Elemente:

```markdown
- First item
- Second item
- Third item
```
**Geordnete Listen** für sequentielle Schritte:

```markdown
1. First step
2. Second step
3. Third step
```
**Definitionslisten** für Begriffserläuterungen:

```markdown
**Term One**
: Explanation of term one

**Term Two**  
: Explanation of term two
```
---

## Häufige Fallstricke, die es zu vermeiden gilt

### 1. Verwechslungsgefahr mit ähnlichen Systemen

**Nicht verwechseln:** - ClientAppManager-Register vs. PortMapper - i2ptunnel tunnel-Typen vs. PortMapper-Dienstkonstanten - ClientApp vs. RouterApp (verschiedene Kontexte) - Verwaltete vs. nicht verwaltete Clients

**Stelle immer klar, welches System** du besprichst:

```markdown
✅ "Register with ClientAppManager using manager.register(this) for name-based lookup."
✅ "Register with PortMapper using context.portMapper().register() for port discovery."
```
### 2. Veraltete Versionsverweise

**Nicht:** - Alte Versionen als "aktuell" bezeichnen - Auf veraltete API-Dokumentation verlinken - In Beispielen veraltete Methodensignaturen verwenden

**Zu erledigen:** - Vor der Veröffentlichung die Versionshinweise prüfen - Überprüfen, ob die API-Dokumentation der aktuellen Version entspricht - Beispiele aktualisieren, damit sie die aktuellen bewährten Verfahren verwenden

### 3. Unerreichbare URLs

**Nicht:** - Nur auf .i2p Domains ohne Clearnet-Alternativen verlinken - Defekte oder veraltete Dokumentations-URLs verwenden - Auf lokale file:// Pfade verlinken

**Das sollten Sie tun:** - Stellen Sie für alle I2P-internen Links Clearnet-Alternativen bereit - Überprüfen Sie vor der Veröffentlichung, dass URLs erreichbar sind - Verwenden Sie dauerhafte URLs (geti2p.net, kein temporäres Hosting)

### 4. Unvollständige Codebeispiele

**Nicht:** - Fragmente ohne Kontext zeigen - Fehlerbehandlung weglassen - Undefinierte Variablen verwenden - Import-Anweisungen auslassen, wenn sie nicht offensichtlich sind

**Das sollten Sie tun:** - Zeigen Sie vollständige, kompilierbare Beispiele - Fügen Sie die erforderliche Fehlerbehandlung ein - Erklären Sie, was jede wichtige Zeile bewirkt - Testen Sie die Beispiele vor der Veröffentlichung

### 5. Mehrdeutige Aussagen

```markdown
❌ "Some applications register services."
✅ "Applications implementing ClientApp may register with ClientAppManager 
   using manager.register(this) to enable name-based lookup."

❌ "Configuration files go in the config directory."
✅ "Modern I2P installations store client configurations in 
   $I2P/clients.config.d/ as individual files."
```
---

## Markdown-Konventionen

### Dateibenennung

Verwende kebab-case (Kleinbuchstaben mit Bindestrichen) für Dateinamen: - `managed-clients.md` - `port-mapper-guide.md` - `configuration-reference.md`

### Frontmatter-Format (Metadatenblock am Dokumentanfang)

Immer YAML-Frontmatter einfügen:

```yaml
---
title: "Document Title"
description: "Brief description under 160 characters"
slug: "url-slug"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "verified"
---
```
### Linkformatierung

**Interne Links** (innerhalb der Dokumentation):

```markdown
See [clients.config specification](https://geti2p.net/spec/configuration#clients-config)
```
**Externe Links** (zu anderen Ressourcen):

```markdown
For more details, see [ClientApp Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html)
```
**Links zu Code-Repositories**:

```markdown
View source: [ClientApp.java](https://i2pgit.org/I2P_Developers/i2p.i2p/src/branch/master/core/java/src/net/i2p/app/ClientApp.java)
```
### Tabellenformatierung

Verwenden Sie Tabellen im GitHub‑Flavored Markdown (eine von GitHub erweiterte Markdown-Variante):

```markdown
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `main` | String | (required) | Full class name |
| `delay` | Integer | 120 | Seconds before start |
| `onBoot` | Boolean | false | Force immediate start |
```
### Sprach-Tags für Codeblöcke

Geben Sie für die Syntaxhervorhebung immer die Sprache an:

```markdown
\`\`\`java
// Java code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`properties
# Configuration files
\`\`\`

\`\`\`xml
<!-- XML files -->
\`\`\`
```
---

## Review-Checkliste

Bevor Sie die Dokumentation veröffentlichen, überprüfen Sie:

- [ ] Alle technischen Aussagen sind anhand des Quellcodes oder der offiziellen Dokumentation verifiziert
- [ ] Versionsnummern und Datumsangaben sind aktuell
- [ ] Alle URLs sind aus dem Clearnet erreichbar (oder Alternativen werden bereitgestellt)
- [ ] Codebeispiele sind vollständig und getestet
- [ ] Die Terminologie folgt den I2P-Konventionen
- [ ] Keine Em-Dashes (normale Bindestriche oder andere Satzzeichen verwenden)
- [ ] Frontmatter ist vollständig und korrekt
- [ ] Die Überschriftenhierarchie ist semantisch (h1 → h2 → h3)
- [ ] Listen und Tabellen sind korrekt formatiert
- [ ] Der Abschnitt Referenzen enthält alle zitierten Quellen
- [ ] Das Dokument folgt den Strukturleitlinien
- [ ] Der Ton ist professionell, aber zugänglich
- [ ] Ähnliche Konzepte werden klar voneinander abgegrenzt
- [ ] Keine defekten Links oder Referenzen
- [ ] Konfigurationsbeispiele sind gültig und aktuell

---

**Feedback:** Falls Sie Probleme feststellen oder Vorschläge zu diesen Richtlinien haben, reichen Sie diese bitte über die offiziellen I2P-Entwicklungskanäle ein.
