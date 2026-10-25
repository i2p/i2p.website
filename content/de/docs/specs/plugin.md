---
title: "Plugin-Spezifikation"
description: ".xpi2p / .su3 Verpackungsregeln für I2P-Plugins"
slug: "plugin"
aliases:
  - "/de/plugin_spec"
  - "/de/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Überblick

Dieses Dokument spezifiziert ein .xpi2p-Dateiformat (wie das Firefox .xpi), aber mit einer einfachen plugin.config-Beschreibungsdatei anstelle einer XML install.rdf-Datei. Dieses Dateiformat wird sowohl für die erste Plugin-Installation als auch für Plugin-Updates verwendet.

Zusätzlich bietet dieses Dokument einen kurzen Überblick darüber, wie der router Plugins installiert, sowie Richtlinien und Leitfäden für Plugin-Entwickler.

Das grundlegende .xpi2p-Dateiformat ist dasselbe wie eine i2pupdate.sud-Datei (das Format, das für router-Updates verwendet wird), aber der Installer lässt den Benutzer das Addon installieren, auch wenn er den Schlüssel des Unterzeichners noch nicht kennt.

Ab Version 0.9.15 wird das SU3-Dateiformat unterstützt und ist bevorzugt. Dieses Format ermöglicht stärkere Signaturschlüssel.

> **Hinweis:** Wir empfehlen nicht mehr, Plugins im xpi2p-Format zu verteilen. Verwenden Sie das su3-Format.

Die Standardverzeichnisstruktur ermöglicht es Benutzern, die folgenden Arten von Addons zu installieren:

- Console-Webapps
- Neue eepsite mit cgi-bin, Webapps
- Console-Themes
- Console-Übersetzungen
- Java-Programme
- Java-Programme in einer separaten JVM
- Jedes Shell-Skript oder Programm

Ein Plugin installiert alle seine Dateien in `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` unter Windows). Der Installer verhindert die Installation an anderen Orten, obwohl das Plugin beim Ausführen auf Bibliotheken an anderen Stellen zugreifen kann.

Dies sollte nur als eine Möglichkeit betrachtet werden, um Installation, Deinstallation und Aktualisierung zu erleichtern und grundlegende Konflikte zwischen Plugins zu verringern.

Es gibt jedoch im Wesentlichen kein Sicherheitsmodell, sobald das Plugin läuft. Das Plugin läuft in derselben JVM und mit denselben Berechtigungen wie der Router und hat vollen Zugriff auf das Dateisystem, den Router, die Ausführung externer Programme usw.

## Details

foo.xpi2p ist eine signierte Update-Datei (sud), die Folgendes enthält:

Standard .sud-Header, der der Zip-Datei vorangestellt wird und Folgendes enthält:

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Zip-Datei mit folgendem Inhalt:

### plugin.config Datei

Diese Datei ist erforderlich. Es ist eine Standard-I2P-Konfigurationsdatei, die die folgenden Eigenschaften enthält:

#### Erforderliche Eigenschaften

Die folgenden vier sind erforderliche Eigenschaften. Die ersten drei müssen identisch mit denen im installierten Plugin für ein Update-Plugin sein.

-   **name** - Wird in diesem Verzeichnisnamen installiert. Für native Plugins möchten Sie möglicherweise separate Namen in verschiedenen Paketen - foo-windows und foo-linux, zum Beispiel.
-   **key** - DSA öffentlicher Schlüssel als 172 B64 Zeichen, die mit '=' enden. Weglassen für SU3-Format.
-   **signer** - yourname@mail.i2p empfohlen
-   **version** - Muss in einem Format vorliegen, das VersionComparator parsen kann, z.B. 1.2.3-4. Maximal 16 Bytes (muss mit sud-Version übereinstimmen). Gültige Zahlentrennzeichen sind '.', '-' und '_'. Diese muss größer sein als die im installierten Plugin für ein Update-Plugin.

#### Anzeigeeigenschaften

Werte für die folgenden Eigenschaften werden auf /configplugins in der Router-Konsole angezeigt, falls vorhanden:

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` empfohlen
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Der Update-Checker wird die Bytes 41-56 an dieser URL überprüfen, um festzustellen, ob eine neuere Version verfügbar ist. Ab 1.7.0 (0.9.53) ist es möglich, die Variablen `$OS` und `$ARCH` in der URL zu verwenden. Nicht empfohlen. Nur verwenden, wenn Sie zuvor Plugins im xpi2p-Format verteilt haben.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - Der Speicherort der Update-Datei im su3-Format, ab 0.9.15. Ab 1.7.0 (0.9.53) ist es möglich, die Variablen `$OS` und `$ARCH` in der URL zu verwenden.
-   **description** - auf Englisch
-   **description_xx** - für Sprache xx
-   **license** - Die Plugin-Lizenz
-   **disableStop=true** - Standardwert false. Wenn true, wird der Stop-Button nicht angezeigt. Verwenden Sie dies, wenn keine Webapps und keine Clients mit stopargs vorhanden sind.

#### Eigenschaften der Konsolen-Zusammenfassungsleiste-Links

Die folgenden Eigenschaften werden verwendet, um einen Link in der Konsolen-Zusammenfassungsleiste hinzuzufügen:

-   **consoleLinkName** - wird zur Zusammenfassungsleiste hinzugefügt
-   **consoleLinkName_xx** - für Sprache xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - unterstützt ab 0.7.12-6
-   **consoleLinkTooltip_xx** - Sprache xx ab 0.7.12-6

#### Konsolen-Symbol-Eigenschaften

Die folgenden optionalen Eigenschaften können verwendet werden, um ein benutzerdefiniertes Symbol in der Konsole hinzuzufügen:

-   **console-icon** - unterstützt seit 0.9.20. Nur für webapps. Ein Pfad zu einem 32x32 Bild, z.B. /icon.png. Seit 1.7.0 (API 0.9.53) ist der Pfad relativ zur angegebenen URL, wenn consoleLinkURL angegeben ist. Andernfalls ist er relativ zum webapp-Namen. Gilt für alle webapps im Plugin.
-   **icon-code** - unterstützt seit 0.9.25. Bietet ein Konsolen-Icon für Plugins ohne Web-Ressourcen. Ein B64-String, der durch Aufrufen von `net.i2p.data.Base64 encode FILE` auf eine 32x32 PNG-Bilddatei erstellt wird.

#### Installationseigenschaften

Die folgenden Eigenschaften werden vom Plugin-Installer verwendet:

-   **type** - app/theme/locale/webapp/... (nicht implementiert, wahrscheinlich nicht notwendig)
-   **min-i2p-version** - Die Mindestversion von I2P, die dieses Plugin erfordert
-   **max-i2p-version** - Die Höchstversion von I2P, auf der dieses Plugin läuft
-   **min-java-version** - Die Mindestversion von Java, die dieses Plugin erfordert
-   **min-jetty-version** - unterstützt ab 0.8.13, verwende 6 für Jetty 6 Webapps
-   **max-jetty-version** - unterstützt ab 0.8.13, verwende 5.99999 für Jetty 5 Webapps
-   **required-platform-OS** - nicht implementiert - wird möglicherweise nur angezeigt, nicht überprüft
-   **other-requirements** - nicht implementiert, z.B. python x.y - wird nicht vom Installationsprogramm überprüft, nur dem Benutzer angezeigt
-   **dont-start-at-install=true** - Standard false. Startet das Plugin nicht, wenn es installiert oder aktualisiert wird.
-   **router-restart-required=true** - Standard false. Dies startet den router oder das Plugin bei einem Update nicht neu, es informiert nur den Benutzer, dass ein Neustart erforderlich ist.
-   **update-only=true** - Standard false. Falls true, schlägt fehl, wenn keine Installation vorhanden ist.
-   **install-only=true** - Standard false. Falls true, schlägt fehl, wenn eine Installation vorhanden ist.
-   **min-installed-version** - zu aktualisieren, falls eine Installation vorhanden ist
-   **max-installed-version** - zu aktualisieren, falls eine Installation vorhanden ist
-   **depends=plugin1,plugin2,plugin3** - nicht implementiert
-   **depends-version=0.3.4,,5.6.7** - nicht implementiert

#### Übersetzungseigenschaften

-   **langs=xx,yy,Klingon,...** - (nicht implementiert) (yy ist die Länderflagge)

### Anwendungsverzeichnisse und -dateien

Jedes der folgenden Verzeichnisse oder Dateien ist optional, aber etwas muss vorhanden sein, sonst passiert nichts:

**console/**

-   **locale/** - Nur JARs mit neuen Resource Bundles (Übersetzungen) für Apps in der I2P-Basisinstallation. Bundles für dieses Plugin sollten in console/webapp/foo.war oder lib/foo.jar platziert werden
-   **themes/** - Neue Themes für die router console. Platziere jedes Theme in einem Unterverzeichnis.
-   **webapps/** - (Siehe wichtige Hinweise unten zu webapps) .wars - Diese werden zur Installationszeit ausgeführt, außer sie sind in webapps.config deaktiviert. Der War-Name muss nicht mit dem Plugin-Namen übereinstimmen. Dupliziere keine War-Namen aus der I2P-Basisinstallation.
-   **webapps.config** - Gleiches Format wie die webapps.config des routers. Wird auch verwendet, um zusätzliche JARs in $PLUGIN/lib/ oder $I2P/lib für den webapp classpath anzugeben, mit `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Hinweis:** Vor Release 1.7.0 (API 0.9.53) wurde die classpath-Zeile nur geladen, wenn der warname dem Plugin-Namen entsprach. Ab API 0.9.53 funktioniert die classpath-Einstellung für jeden warname.

> **Hinweis:** Vor router Version 0.7.12-9 suchte der router nach `plugin.warname.startOnLoad` anstelle von `webapps.warname.startOnLoad`. Zur Kompatibilität mit älteren router-Versionen sollte ein Plugin, das eine War-Datei deaktivieren möchte, beide Zeilen enthalten.

**eepsite/**

(Siehe wichtige Hinweise unten zu eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - Der Installer muss hier Variablenersetzung durchführen, um den Pfad zu setzen. Der Standort und Name dieser Datei ist nicht wirklich wichtig, solange sie in clients.config gesetzt ist - es könnte praktischer sein, eine Ebene höher zu sein.

**lib/**

Legen Sie hier beliebige JAR-Dateien ab und geben Sie diese in einer Classpath-Zeile in console/webapps.config und/oder clients.config an

### clients.config-Datei

Diese Datei ist optional und spezifiziert Clients, die gestartet werden, wenn ein Plugin gestartet wird. Sie verwendet das gleiche Format wie die clients.config-Datei des routers. Siehe die clients.config-Konfigurationsdatei-Spezifikation für weitere Informationen über das Format und wichtige Details darüber, wie Clients gestartet und gestoppt werden.

-   **clientApp.0.stopargs=foo bar stop baz** - Falls vorhanden, wird die Klasse mit diesen Argumenten aufgerufen, um den Client zu stoppen. Alle Stop-Tasks werden ohne Verzögerung aufgerufen. Hinweis: Der router kann nicht erkennen, ob Ihre nicht verwalteten Clients laufen oder nicht.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Falls vorhanden, wird die Klasse mit diesen Argumenten kurz vor dem Löschen von $PLUGIN aufgerufen. Alle Deinstallations-Tasks werden ohne Verzögerung aufgerufen.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Der Plugin-Runner führt Variablenersetzung in den args- und stopargs-Zeilen wie folgt durch:
    -   `$I2P` - I2P Basis-Installationsverzeichnis
    -   `$CONFIG` - I2P Konfigurationsverzeichnis (typischerweise ~/.i2p)
    -   `$PLUGIN` - Installationsverzeichnis dieses Plugins (typischerweise ~/.i2p/plugins/appname)
    -   `$OS` - das Host-Betriebssystem in der Form `windows`, `linux`, `mac`
    -   `$ARCH` - die Host-Architektur in der Form `386`, `amd64`, `arm64`

(Siehe wichtige Hinweise unten zum Ausführen von Shell-Skripten oder externen Programmen)

## Plugin-Installer-Aufgaben

Dies listet auf, was passiert, wenn ein Plugin von I2P installiert wird.

1.  Die .xpi2p-Datei wird heruntergeladen.
2.  Die .sud-Signatur wird gegen gespeicherte Schlüssel verifiziert. Ab Version 0.9.14.1 schlägt die Installation fehl, wenn kein passender Schlüssel vorhanden ist, es sei denn, eine erweiterte Router-Eigenschaft ist gesetzt, um alle Schlüssel zu erlauben.
3.  Die Integrität der Zip-Datei wird überprüft.
4.  Die plugin.config-Datei wird extrahiert.
5.  Die I2P-Version wird überprüft, um sicherzustellen, dass das Plugin funktioniert.
6.  Es wird überprüft, dass Webapps nicht die bestehenden $I2P-Anwendungen duplizieren.
7.  Das bestehende Plugin wird gestoppt (falls vorhanden).
8.  Es wird überprüft, dass das Installationsverzeichnis noch nicht existiert, wenn update=false, oder gefragt, ob überschrieben werden soll.
9.  Es wird überprüft, dass das Installationsverzeichnis existiert, wenn update=true, oder gefragt, ob es erstellt werden soll.
10. Das Plugin wird in appDir/plugins/name/ entpackt.
11. Das Plugin wird zu plugins.config hinzugefügt.

## Plugin Starter-Aufgaben

Dies listet auf, was passiert, wenn Plugins gestartet werden. Zuerst wird plugins.config überprüft, um zu sehen, welche Plugins gestartet werden müssen. Für jedes Plugin:

1.  Prüfe clients.config und lade und starte jeden Eintrag (füge die konfigurierten JARs zum Klassenpfad hinzu).
2.  Prüfe console/webapp und console/webapp.config. Lade und starte erforderliche Einträge (füge die konfigurierten JARs zum Klassenpfad hinzu).
3.  Füge console/locale/foo.jar zum Übersetzungsklassenpfad hinzu, falls vorhanden.
4.  Füge console/theme zum Theme-Suchpfad hinzu, falls vorhanden.
5.  Füge den Link zur Zusammenfassungsleiste hinzu.

## Console-Webapp-Hinweise

Console-Webapps mit Hintergrundaufgaben sollten einen ServletContextListener implementieren (siehe seedless oder i2pbote als Beispiele) oder destroy() im Servlet überschreiben, damit sie gestoppt werden können. Ab router Version 0.7.12-3 werden Console-Webapps immer gestoppt, bevor sie neu gestartet werden, sodass Sie sich keine Sorgen über mehrere Instanzen machen müssen, solange Sie dies tun. Ebenfalls ab router Version 0.7.12-3 werden Console-Webapps beim Herunterfahren des routers gestoppt.

Bundeln Sie Bibliotheks-JARs nicht in der Webapp; legen Sie sie in lib/ ab und fügen Sie einen Classpath in webapps.config hinzu. Dann können Sie separate Installations- und Update-Plugins erstellen, wobei das Update-Plugin die Bibliotheks-JARs nicht enthält.

Bündeln Sie niemals Jetty, Tomcat oder Servlet-JARs in Ihr Plugin, da diese mit der Version in der I2P-Installation in Konflikt stehen können. Achten Sie darauf, keine konfliktverursachenden Bibliotheken zu bündeln.

Schließen Sie keine .java oder .jsp-Dateien ein; andernfalls wird Jetty diese bei der Installation neu kompilieren, was die Startzeit verlängert. Obwohl die meisten I2P-Installationen einen funktionierenden Java- und JSP-Compiler im Klassenpfad haben, ist dies nicht garantiert und funktioniert möglicherweise nicht in allen Fällen.

Für den Moment muss eine Webapp, die Klassenpfad-Dateien in $PLUGIN hinzufügen muss, denselben Namen wie das Plugin haben. Zum Beispiel muss eine Webapp im Plugin foo den Namen foo.war haben.

Obwohl I2P seit I2P-Release 0.9.30 Servlet 3.0 unterstützt, unterstützt es NICHT das Annotation-Scanning für @WebContent (keine web.xml-Datei). Mehrere zusätzliche Runtime-JARs wären erforderlich, und wir stellen diese nicht in einer Standardinstallation bereit. Kontaktieren Sie die I2P-Entwickler, wenn Sie Unterstützung für @WebContent benötigen.

## Eepsite Notizen

Es ist nicht klar, wie ein Plugin zu einer bestehenden eepsite installiert werden kann. Der router hat keine Verbindung zur eepsite, und sie läuft möglicherweise oder auch nicht, und es könnte mehr als eine geben. Besser ist es, eine eigene Jetty-Instanz und I2PTunnel-Instanz zu starten, für eine völlig neue eepsite.

Es kann eine neue I2PTunnel instanziieren (ähnlich wie es die i2ptunnel CLI macht), aber es wird natürlich nicht in der i2ptunnel GUI erscheinen, das ist eine andere Instanz. Aber das ist in Ordnung. Dann können Sie i2ptunnel und jetty zusammen starten und stoppen.

Verlassen Sie sich also nicht darauf, dass der router dies automatisch mit einer bestehenden eepsite zusammenführt. Das wird wahrscheinlich nicht passieren. Starten Sie ein neues I2PTunnel und Jetty von clients.config. Die besten Beispiele dafür sind die zzzot- und pebble-Plugins.

Wie bekommt man Pfad-Substitution in jetty.xml? Siehe zzzot und pebble Plugins als Beispiele.

## Client Start/Stopp Hinweise

Ab Version 0.9.4 unterstützt der router "verwaltete" Plugin-Clients. Verwaltete Plugin-Clients werden vom `ClientAppManager` instanziiert und gestartet. Der ClientAppManager behält eine Referenz auf den Client und erhält Updates über den Zustand des Clients. Verwaltete Plugin-Clients sind bevorzugt, da es viel einfacher ist, die Zustandsverfolgung zu implementieren und einen Client zu starten und zu stoppen. Es ist auch viel einfacher, statische Referenzen im Client-Code zu vermeiden, die nach dem Stoppen eines Clients zu übermäßigem Speicherverbrauch führen könnten. Siehe die Spezifikation der Konfigurationsdatei clients.config für weitere Informationen zum Schreiben eines verwalteten Clients.

Für "nicht verwaltete" Plugin-Clients hat der router keine Möglichkeit, den Zustand von Clients zu überwachen, die über clients.config gestartet wurden. Der Plugin-Autor sollte mehrfache Start- oder Stopp-Aufrufe möglichst elegant behandeln, indem er eine statische Zustandstabelle führt oder PID-Dateien verwendet, etc. Vermeiden Sie Logging oder Exceptions bei mehrfachen Starts oder Stopps. Dies gilt auch für einen Stopp-Aufruf ohne vorherigen Start. Ab router-Version 0.7.12-3 werden Plugins beim router-Shutdown gestoppt, was bedeutet, dass alle Clients mit stopargs in clients.config aufgerufen werden, unabhängig davon, ob sie zuvor gestartet wurden oder nicht.

## Shell-Skript und externe Programm-Hinweise

Um Shell-Skripte oder andere externe Programme auszuführen, schreiben Sie eine kleine Java-Klasse, die den Betriebssystemtyp überprüft und dann ShellCommand entweder auf der von Ihnen bereitgestellten .bat- oder .sh-Datei ausführt. Eine allgemeine Lösung hierfür wurde in I2P 1.7.0/0.9.53 hinzugefügt, der "ShellService", der Zustandsverfolgung für einen einzelnen Befehl durchführt und mit dem ClientAppManager kommuniziert.

Externe Programme werden nicht gestoppt, wenn der router stoppt, und eine zweite Kopie wird gestartet, wenn der router startet. Dies kann normalerweise durch die Verwendung eines ShellService zur Zustandsverfolgung behoben werden. Falls dies für Ihren Anwendungsfall nicht geeignet ist, könnten Sie eine Wrapper-Klasse oder ein Shell-Skript schreiben, das die übliche Speicherung der PID in einer PID-Datei durchführt und beim Start danach prüft.

## Andere Plugin-Richtlinien

-   Siehe i2p.scripts monotone Branch oder eines der Beispiel-Plugins auf zzz's Seite für das makeplugin.sh Shell-Skript. Dies automatisiert die meisten Aufgaben für Schlüsselerzeugung, Plugin su3-Dateierstellung und Verifizierung. Sie sollten dieses Skript in Ihren Plugin-Build-Prozess integrieren.
-   Pack200 von jars und wars wird für Plugins stark empfohlen, es verkleinert Plugins generell um 60-65%. Siehe eines der Beispiel-Plugins auf zzz's Seite für ein Beispiel. Pack200-Entpacken wird auf Routern 0.7.11-5 oder höher unterstützt, was im Wesentlichen alle router sind, die überhaupt Plugins unterstützen.
-   Plugins dürfen nicht versuchen, irgendwo in $I2P zu schreiben, da es schreibgeschützt sein kann, und das ist ohnehin keine gute Richtlinie.
-   Plugins dürfen in $CONFIG schreiben, aber es wird empfohlen, Dateien nur in $PLUGIN zu behalten. Alle Dateien in $PLUGIN werden bei der Deinstallation gelöscht.
-   $CWD kann überall sein; nehmen Sie nicht an, dass es sich an einem bestimmten Ort befindet, versuchen Sie nicht, Dateien relativ zu $CWD zu lesen oder zu schreiben. Für einen ShellService ist es immer das gleiche wie $PLUGIN.
-   Java-Programme sollten herausfinden, wo sie sich befinden, mit den Verzeichnis-Gettern in I2PAppContext.
-   Plugin-Verzeichnis ist `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, oder fügen Sie ein $PLUGIN-Argument in die args-Zeile in clients.config ein.
-   Alle Konfigurationsdateien müssen UTF-8 sein.
-   Um in einer separaten JVM zu laufen, verwenden Sie ShellCommand mit `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Als Alternative zu stopargs in clients.config kann ein Java-Client einen Shutdown-Hook mit `I2PAppContext.addShutdownTask()` registrieren. Dies würde jedoch ein Plugin beim Upgrade nicht herunterfahren, daher wird stopargs empfohlen. Setzen Sie auch alle erstellten Threads in den Daemon-Modus.
-   Schließen Sie keine Klassen ein, die die der Standardinstallation duplizieren. Erweitern Sie die Klassen falls notwendig.
-   Achten Sie auf die unterschiedlichen Classpath-Definitionen in wrapper.config zwischen alten und neuen Installationen.
-   Clients werden doppelte Schlüssel mit verschiedenen Schlüsselnamen ablehnen, und doppelte Schlüsselnamen mit verschiedenen Schlüsseln, und verschiedene Schlüssel oder Schlüsselnamen in Upgrade-Paketen. Sichern Sie Ihre Schlüssel. Generieren Sie sie nur einmal.
-   Ändern Sie die plugin.config-Datei nicht zur Laufzeit, da sie beim Upgrade überschrieben wird. Verwenden Sie eine andere Konfigurationsdatei im Verzeichnis zum Speichern der Laufzeit-Konfiguration.
-   Generell sollten Plugins keinen Zugriff auf $I2P/lib/router.jar benötigen. Greifen Sie nicht auf router-Klassen zu, außer Sie machen etwas Besonderes.
-   Da jede Version höher als die vorherige sein muss, könnten Sie Ihr Build-Skript verbessern, um eine Build-Nummer am Ende der Version hinzuzufügen.
-   Plugins dürfen niemals `System.exit()` aufrufen.
-   Bitte respektieren Sie Lizenzen, indem Sie die Lizenzanforderungen für jede Software erfüllen, die Sie bündeln.
-   Der router setzt die JVM-Zeitzone auf UTC. Falls ein Plugin die tatsächliche Zeitzone des Benutzers wissen muss, wird sie vom router in der I2PAppContext-Eigenschaft `i2p.systemTimeZone` gespeichert.

## Classpaths

Die folgenden JAR-Dateien in $I2P/lib können als Teil des Standard-Klassenpfads für alle I2P-Installationen angenommen werden, unabhängig davon, wie alt oder neu die ursprüngliche Installation ist.

Alle aktuellen öffentlichen APIs in i2p-JARs haben die seit-Release-Nummer in den Javadocs spezifiziert. Falls Ihr Plugin bestimmte Funktionen benötigt, die nur in neueren Versionen verfügbar sind, stellen Sie sicher, dass Sie die Eigenschaften min-i2p-version, min-jetty-version oder beide in der plugin.config-Datei setzen.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Die folgenden JAR-Dateien in $I2P/lib können bei allen I2P-Installationen als vorhanden angenommen werden, unabhängig davon, wie alt oder neu die ursprüngliche Installation ist, befinden sich aber nicht zwangsläufig im classpath:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Alles, was oben nicht aufgeführt ist, ist möglicherweise nicht im Klassenpfad aller Nutzer vorhanden, auch wenn Sie es in IHRER Version von i2p im Klassenpfad haben. Falls Sie eine JAR-Datei benötigen, die oben nicht aufgeführt ist, fügen Sie $I2P/lib/foo.jar zum Klassenpfad hinzu, der in clients.config oder webapps.config in Ihrem Plugin angegeben ist.

Früher wurde ein in clients.config angegebener classpath-Eintrag zum classpath für die gesamte JVM hinzugefügt. Ab Version 0.7.13-3 wurde dies jedoch mit Hilfe von Class Loadern behoben, und nun ist der in clients.config angegebene classpath, wie ursprünglich beabsichtigt, nur für den jeweiligen Thread bestimmt. Geben Sie daher den vollständigen erforderlichen classpath für jeden Client an.

## Java-Versions-Hinweise

I2P benötigt Java 7 seit Version 0.9.24 (Januar 2016). I2P benötigte Java 6 seit Version 0.9.12 (April 2014). Alle I2P-Benutzer auf der neuesten Version sollten eine 1.7 (7.0) JVM verwenden.

Wenn Ihr Plugin **nicht Version 1.7 erfordert**:

-   Stellen Sie sicher, dass alle Java- und JSP-Dateien mit source="1.6" target="1.6" kompiliert werden.
-   Stellen Sie sicher, dass alle mitgelieferten Bibliotheks-JARs ebenfalls für 1.6 oder niedriger sind.

Falls Ihr Plugin **1.7 benötigt**:

-   Beachten Sie das auf Ihrer Download-Seite.
-   Fügen Sie min-java-version=1.7 zu Ihrer plugin.config hinzu

In jedem Fall **müssen** Sie einen Bootclasspath setzen, wenn Sie mit Java 8 kompilieren, um Laufzeitabstürze zu verhindern.

## JVM stürzt beim Aktualisieren ab

Hinweis - das sollte jetzt alles behoben sein.

Die JVM neigt dazu abzustürzen, wenn jar-Dateien in einem Plugin aktualisiert werden, falls dieses Plugin seit dem Start von I2P gelaufen ist (auch wenn das Plugin später gestoppt wurde). Dies könnte mit der Class Loader-Implementierung in 0.7.13-3 behoben worden sein, aber möglicherweise auch nicht.

Das Sicherste ist, Ihr Plugin mit der jar-Datei innerhalb der war-Datei zu entwerfen (für eine Webapp), oder einen Neustart nach dem Update zu erfordern, oder die jar-Dateien in Ihrem Plugin nicht zu aktualisieren.

Aufgrund der Funktionsweise von Class Loadern innerhalb einer Webapp kann es _möglicherweise_ sicher sein, externe JARs zu verwenden, wenn Sie den Classpath in webapps.config angeben. Weitere Tests sind erforderlich, um dies zu überprüfen. Geben Sie den Classpath nicht mit einem 'fake' Client in clients.config an, wenn er nur für eine Webapp benötigt wird - verwenden Sie stattdessen webapps.config.

Am wenigsten sicher und offenbar die Quelle der meisten Abstürze sind Clients mit Plugin-JARs, die im Classpath in clients.config angegeben sind.

Dies sollte bei der ersten Installation kein Problem darstellen - Sie sollten niemals einen Neustart für die erste Installation eines Plugins benötigen.

## Referenzen

-   [Konfigurationsdatei-Spezifikation](/docs/specs/configuration)
-   [DSA-Kryptographie](/docs/specs/cryptography#DSA)
-   [Updates-Spezifikation](/docs/specs/updates)
