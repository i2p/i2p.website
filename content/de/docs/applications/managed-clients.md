---
title: "Verwaltete Clients"
description: "Wie router-verwaltete Anwendungen mit dem ClientAppManager und dem Port-Mapper integrieren"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Überblick

Einträge in [`clients.config`](/docs/specs/configuration/#clients-config) teilen dem Router mit, welche Anwendungen beim Start gestartet werden sollen. Jeder Eintrag kann als **managed** Client (bevorzugt) oder als **unmanaged** Client ausgeführt werden. Managed Clients arbeiten mit dem `ClientAppManager` zusammen, welcher:

- Instanziiert die Anwendung und verfolgt den Lebenszyklusstatus für die Router-Konsole
- Stellt dem Benutzer Start-/Stopp-Steuerelemente zur Verfügung und erzwingt saubere Herunterfahrvorgänge beim Router-Exit
- Hostet eine schlanke **Client-Registry** und einen **Port-Mapper**, damit Anwendungen die Dienste der anderen erkennen können

Unmanaged Clients rufen einfach eine `main()`-Methode auf; verwenden Sie sie nur für Legacy-Code, der nicht modernisiert werden kann.

## 2. Implementierung eines Managed Client

Managed Clients müssen entweder `net.i2p.app.ClientApp` (für benutzerorientierte Anwendungen) oder `net.i2p.router.app.RouterApp` (für Router-Erweiterungen) implementieren. Stellen Sie einen der unten aufgeführten Konstruktoren bereit, damit der Manager Kontext- und Konfigurationsargumente übergeben kann:

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
Das `args`-Array enthält die in `clients.config` oder in einzelnen Dateien in `clients.config.d/` konfigurierten Werte. Erweitern Sie nach Möglichkeit die Hilfsklassen `ClientApp` / `RouterApp`, um die Standard-Lebenszyklus-Verkabelung zu erben.

### 2.1 Lifecycle Methods

Verwaltete Clients müssen Folgendes implementieren:

- `startup()` - Initialisierung durchführen und umgehend zurückkehren. Muss mindestens einmal `manager.notify()` aufrufen, um vom INITIALIZED-Zustand zu wechseln.
- `shutdown(String[] args)` - Ressourcen freigeben und Hintergrund-Threads stoppen. Muss mindestens einmal `manager.notify()` aufrufen, um den Zustand auf STOPPING oder STOPPED zu ändern.
- `getState()` - der Konsole mitteilen, ob die Anwendung läuft, startet, stoppt oder fehlgeschlagen ist

Der Manager ruft diese Methoden auf, wenn Benutzer mit der Konsole interagieren.

### 2.2 Advantages

- Genaue Statusberichte in der Router-Konsole
- Saubere Neustarts ohne Leaking von Threads oder statischen Referenzen
- Geringerer Speicher-Footprint nach dem Stoppen der Anwendung
- Zentralisiertes Logging und Fehlerberichterstattung über den injizierten Kontext

## 3. Unmanaged Clients (Fallback Mode)

Wenn die konfigurierte Klasse kein Managed Interface implementiert, startet der Router sie durch Aufruf von `main(String[] args)` und kann den resultierenden Prozess nicht verfolgen. Die Konsole zeigt begrenzte Informationen an und Shutdown-Hooks werden möglicherweise nicht ausgeführt. Reservieren Sie diesen Modus für Skripte oder einmalige Dienstprogramme, die die Managed APIs nicht nutzen können.

## 4. Client Registry

Verwaltete und nicht verwaltete Clients können sich beim Manager registrieren, damit andere Komponenten eine Referenz über den Namen abrufen können:

```java
manager.register(this);
```
Die Registrierung verwendet den Rückgabewert von `getName()` des Clients als Registry-Schlüssel. Bekannte Registrierungen umfassen `console`, `i2ptunnel`, `Jetty`, `outproxy` und `update`. Rufen Sie einen Client mit `ClientAppManager.getRegisteredApp(String name)` ab, um Funktionen zu koordinieren (zum Beispiel die Konsole, die Jetty nach Statusdetails abfragt).

Beachten Sie, dass Client-Registry und Port-Mapper separate Systeme sind. Die Client-Registry ermöglicht die Inter-Applikations-Kommunikation durch Namensauflösung, während der Port-Mapper Dienstnamen auf Host:Port-Kombinationen für Service Discovery abbildet.

## 3. Unverwaltete Clients (Fallback-Modus)

Der Port-Mapper bietet ein einfaches Verzeichnis für interne TCP-Dienste. Registrieren Sie Loopback-Ports, damit Mitarbeiter fest codierte Adressen vermeiden:

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Oder mit expliziter Host-Angabe:

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Suchen Sie Dienste mit `PortMapper.getPort(String name)` (gibt -1 zurück, falls nicht gefunden) oder `getPort(String name, int defaultPort)` (gibt Standardwert zurück, falls nicht gefunden). Prüfen Sie den Registrierungsstatus mit `isRegistered(String name)` und rufen Sie den registrierten Host mit `getActualHost(String name)` ab.

Allgemeine Port-Mapper-Service-Konstanten aus `net.i2p.util.PortMapper`:

- `SVC_CONSOLE` - Router-Konsole (Standardport 7657)
- `SVC_HTTP_PROXY` - HTTP-Proxy (Standardport 4444)
- `SVC_HTTPS_PROXY` - HTTPS-Proxy (Standardport 4445)
- `SVC_I2PTUNNEL` - I2PTunnel-Manager
- `SVC_SAM` - SAM-Bridge (Standardport 7656)
- `SVC_SAM_SSL` - SAM-Bridge SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - BOB-Bridge (Standardport 2827)
- `SVC_EEPSITE` - Standard-eepsite (Standardport 7658)
- `SVC_HTTPS_EEPSITE` - HTTPS-eepsite
- `SVC_IRC` - IRC-Tunnel (Standardport 6668)
- `SVC_SUSIDNS` - SusiDNS

Hinweis: `httpclient`, `httpsclient` und `httpbidirclient` sind i2ptunnel-Tunneltypen (verwendet in der `tunnel.N.type`-Konfiguration), keine Port-Mapper-Servicekonstanten.

## 4. Client-Registry

### 2.1 Lifecycle-Methoden

Ab Version 0.9.42 unterstützt der Router die Aufteilung der Konfiguration in einzelne Dateien innerhalb des Verzeichnisses `clients.config.d/`. Jede Datei enthält Eigenschaften für einen einzelnen Client, wobei alle Eigenschaften mit `clientApp.0.` beginnen:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
Dies ist der empfohlene Ansatz für Neuinstallationen und Plugins.

### 2.2 Vorteile

Aus Gründen der Abwärtskompatibilität verwendet das traditionelle Format eine fortlaufende Nummerierung:

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Erforderlich:** - `main` - Vollständiger Klassenname, der ClientApp oder RouterApp implementiert, oder eine statische `main(String[] args)`-Methode enthält

**Optional:** - `name` - Anzeigename für die Router-Konsole (Standard ist der Klassenname) - `args` - Durch Leerzeichen oder Tabulator getrennte Argumente (unterstützt Zeichenketten in Anführungszeichen) - `delay` - Sekunden vor dem Start (Standard 120) - `onBoot` - Erzwingt `delay=0`, falls true - `startOnLoad` - Aktiviert/deaktiviert den Client (Standard true)

**Plugin-spezifisch:** - `stopargs` - Argumente, die beim Herunterfahren übergeben werden - `uninstallargs` - Argumente, die bei der Plugin-Deinstallation übergeben werden - `classpath` - Kommagetrennte zusätzliche Classpath-Einträge

**Variablenersetzung für Plugins:** - `$I2P` - I2P-Basisverzeichnis - `$CONFIG` - Benutzerkonfigurationsverzeichnis (z.B. ~/.i2p) - `$PLUGIN` - Plugin-Verzeichnis - `$OS` - Betriebssystemname - `$ARCH` - Architekturname

## 5. Port Mapper

- Bevorzugen Sie verwaltete Clients; greifen Sie nur dann auf nicht verwaltete zurück, wenn es absolut notwendig ist.
- Halten Sie Initialisierung und Herunterfahren schlank, damit Konsolenoperationen reaktionsfähig bleiben.
- Verwenden Sie beschreibende Registry- und Port-Namen, damit Diagnosetools (und Endbenutzer) verstehen, was ein Dienst tut.
- Vermeiden Sie statische Singletons - verlassen Sie sich auf den injizierten Kontext und Manager, um Ressourcen zu teilen.
- Rufen Sie `manager.notify()` bei allen Zustandsübergängen auf, um einen genauen Konsolenstatus aufrechtzuerhalten.
- Wenn Sie in einer separaten JVM ausgeführt werden müssen, dokumentieren Sie, wie Logs und Diagnosen der Hauptkonsole zugänglich gemacht werden.
- Erwägen Sie für externe Programme die Verwendung von ShellService (hinzugefügt in Version 1.7.0), um die Vorteile verwalteter Clients zu nutzen.

## 6. Konfigurationsformat

Verwaltete Clients wurden in **Version 0.9.4** (17. Dezember 2012) eingeführt und bleiben die empfohlene Architektur bis zur **Version 2.10.0** (9. September 2025). Die Kern-APIs sind über diesen Zeitraum hinweg stabil geblieben, ohne dass es zu Breaking Changes gekommen ist:

- Konstruktor-Signaturen unverändert
- Lifecycle-Methoden (startup, shutdown, getState) unverändert
- ClientAppManager-Registrierungsmethoden unverändert
- PortMapper-Registrierungs- und Lookup-Methoden unverändert

Bemerkenswerte Verbesserungen: - **0.9.42 (2019)** - clients.config.d/ Verzeichnisstruktur für einzelne Konfigurationsdateien - **1.7.0 (2021)** - ShellService hinzugefügt zur Zustandsverfolgung externer Programme - **2.10.0 (2025)** - Aktuelle Version ohne Änderungen an der managed client API

Das nächste Major-Release wird Java 17+ als Minimum voraussetzen (Infrastrukturanforderung, keine API-Änderung).

## References

- [clients.config-Spezifikation](/docs/specs/configuration/#clients-config)
- [Spezifikation der Konfigurationsdatei](/docs/specs/configuration/)
- [I2P Technische Dokumentation - Übersicht](/docs/)
- [ClientAppManager Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [PortMapper Javadoc](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [ClientApp-Schnittstelle](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [RouterApp-Schnittstelle](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Alternative Javadoc (stabil)](https://docs.i2p-projekt.de/javadoc/)
- [Alternative Javadoc (Clearnet-Spiegel)](https://eyedeekay.github.io/javadoc-i2p/)

> **Hinweis:** Das I2P-Netzwerk hostet eine umfassende Dokumentation unter http://idk.i2p/javadoc-i2p/, für deren Zugriff ein I2P-Router erforderlich ist. Für Clearnet-Zugriff verwenden Sie den oben genannten GitHub Pages Mirror.
