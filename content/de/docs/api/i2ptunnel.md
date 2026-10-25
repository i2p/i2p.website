---
title: "I2PTunnel"
description: "Werkzeug zur Schnittstelle mit und Bereitstellung von Diensten auf I2P"
slug: "i2ptunnel"
aliases:
  - "/de/i2ptunnel"
  - "/de/i2ptunnel/"
  - "/de/i2ptunnel_migration"
  - "/de/i2ptunnel_migration/"
  - "/de/i2ptunnel_services"
  - "/de/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Überblick {#overview}

I2PTunnel ist ein Werkzeug zur Anbindung an I2P und zur Bereitstellung von Diensten im I2P-Netzwerk. Das Ziel eines I2PTunnel kann mittels eines [Hostnamens](/docs/overview/naming), [Base32](/docs/overview/naming#base32) oder eines vollständigen 516-Byte destination keys definiert werden. Ein eingerichteter I2PTunnel wird auf Ihrem Client-Rechner als localhost:port verfügbar sein. Wenn Sie einen Dienst im I2P-Netzwerk bereitstellen möchten, erstellen Sie einfach einen I2PTunnel zur entsprechenden ip_address:port. Ein entsprechender 516-Byte destination key wird für den Dienst generiert und dieser wird im gesamten I2P-Netzwerk verfügbar. Eine Web-Oberfläche zur I2PTunnel-Verwaltung ist unter [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/) verfügbar.

## Standard-Dienste {#default-services}

### Server Tunnels {#default-server-tunnels}

- **I2P Webserver** - Ein tunnel, der auf einen Jetty-Webserver zeigt, der auf
  [localhost:7658](http://localhost:7658) läuft, für bequemes und schnelles Hosting auf I2P.
  Das Dokumentenverzeichnis ist:
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, was sich erweitert zu: `C:\Users\**benutzername**\AppData\Local\I2P\I2P Site\docroot`

### Client-Tunnel {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - Ein HTTP-Proxy zum anonymen Durchsuchen von I2P und dem regulären Internet über I2P. Das Durchsuchen des Internets über I2P verwendet einen zufälligen Proxy, der durch die Option "Outproxies:" angegeben wird.
- **Irc2P** - *localhost:6668* - Ein IRC-tunnel zum standardmäßigen anonymen IRC-Netzwerk, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - SSH-Zugang zum Projekt-Git-Repository
- **smtp.postman.i2p** - *localhost:7659* - Ein SMTP-Dienst, bereitgestellt von postman unter hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - Der dazugehörige POP-Dienst von postman unter hq.postman.i2p

## Konfiguration {#configuration}

[I2PTunnel-Konfiguration](/docs/specs/configuration)

## Client-Modi {#client-modes}

### Standard {#client-modes-standard}

Öffnet einen lokalen TCP-Port, der sich mit einem Dienst (wie HTTP, FTP oder SMTP) auf einem Ziel innerhalb von I2P verbindet. Der tunnel wird zu einem zufälligen Host aus der durch Kommas getrennten (", ") Liste von Zielen geleitet.

### HTTP {#client-mode-http}

Ein HTTP-Client tunnel. Der tunnel verbindet sich mit dem Ziel, das durch die URL in einer HTTP-Anfrage angegeben ist. Unterstützt Proxying ins Internet, wenn ein Outproxy bereitgestellt wird. Entfernt folgende Header aus HTTP-Verbindungen:

- **Accept\*:** (nicht einschließlich "Accept" und "Accept-Encoding") da sie stark zwischen Browsern variieren und als Identifikationsmerkmal verwendet werden können.
- **Referer:**
- **Via:**
- **From:**

Der HTTP-Client-Proxy bietet eine Reihe von Diensten zum Schutz des Benutzers und zur Verbesserung der Benutzererfahrung.

**Request-Header-Verarbeitung:** - Entfernung datenschutzproblematischer Header - Weiterleitung zu lokalem oder entferntem Outproxy - Outproxy-Auswahl, Caching und Erreichbarkeitsverfolgung - Hostname-zu-Ziel-Lookups - Host-Header-Ersetzung zu b32 - Header hinzufügen um Unterstützung für transparente Dekomprimierung anzuzeigen - Erzwinge connection: close - RFC-konforme Proxy-Unterstützung - RFC-konforme Hop-by-Hop-Header-Verarbeitung und -Entfernung - Optionale Digest- und Basic-Benutzername/Passwort-Authentifizierung - Optionale Outproxy-Digest- und Basic-Benutzername/Passwort-Authentifizierung - Pufferung aller Header vor der Weiterleitung für bessere Effizienz - Jump-Server-Links - Jump-Response-Verarbeitung und Formulare (Address Helper) - Blinded-b32-Verarbeitung und Credential-Formulare - Unterstützt Standard-HTTP- und HTTPS-Anfragen (CONNECT)

**Verarbeitung von Antwort-Headern:** - Prüfung, ob Antwort dekomprimiert werden soll - Erzwinge Verbindung: schließen - RFC-konforme Hop-by-Hop-Header-Verarbeitung und -Entfernung - Pufferung aller Header vor Weiterleitung für bessere Effizienz

**HTTP-Fehlerantworten:** - Für viele häufige und weniger häufige Fehler, damit der Benutzer weiß, was passiert ist - Über 20 einzigartige übersetzte, gestylte und formatierte Fehlerseiten für verschiedene Fehler - Interner Webserver zum Bereitstellen von Formularen, CSS, Bildern und Fehlern

#### Transparente Antwort-Komprimierung {#transparent-response-compression}

Die i2ptunnel-Antwortenkompression wird mit dem HTTP-Header angefordert:

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

Die Serverseite entfernt diesen Hop-by-Hop-Header, bevor sie die Anfrage an den Webserver sendet. Der aufwendige Header mit allen q-Werten ist nicht notwendig; Server sollten einfach überall im Header nach "x-i2p-gzip" suchen.

Die Serverseite bestimmt anhand der vom Webserver empfangenen Header, einschließlich Content-Type, Content-Length und Content-Encoding, ob die Antwort komprimiert werden soll, um zu bewerten, ob die Antwort komprimierbar ist und die zusätzliche CPU-Leistung rechtfertigt. Wenn die Serverseite die Antwort komprimiert, fügt sie den folgenden HTTP-Header hinzu:

- **Content-Encoding:** x-i2p-gzip

Wenn dieser Header in der Antwort vorhanden ist, dekomprimiert der HTTP-Client-Proxy ihn transparent. Die Client-Seite entfernt diesen Header und entpackt ihn mit gunzip, bevor die Antwort an den Browser gesendet wird. Beachten Sie, dass wir immer noch die zugrunde liegende gzip-Komprimierung auf der I2CP-Ebene haben, die weiterhin wirksam ist, wenn die Antwort auf der HTTP-Ebene nicht komprimiert ist.

Dieses Design und die aktuelle Implementierung verletzen RFC 2616 in mehreren Punkten:

- X-Accept-Encoding ist kein Standard-Header
- Führt kein Dechunking/Chunking pro Hop durch; es überträgt Chunking Ende-zu-Ende
- Überträgt Transfer-Encoding-Header Ende-zu-Ende
- Verwendet Content-Encoding, nicht Transfer-Encoding, um die Kodierung pro Hop zu spezifizieren
- Verbietet x-i2p-Gzipping, wenn Content-Encoding gesetzt ist (aber das wollen wir wahrscheinlich sowieso nicht)
- Die Serverseite komprimiert das serverseitig gesendete Chunking mit gzip, anstatt Dechunk-Gzip-Rechunk und Dechunk-Gunzip-Rechunk durchzuführen
- Der gzippte Inhalt wird danach nicht in Chunks aufgeteilt. RFC 2616 erfordert, dass alle Transfer-Encoding außer "identity" in Chunks aufgeteilt werden
- Da es kein Chunking außerhalb (nach) dem Gzip gibt, ist es schwieriger, das Ende der Daten zu finden, was jede Implementierung von Keepalive erschwert
- RFC 2616 besagt, dass Content-Length nicht gesendet werden darf, wenn Transfer-Encoding vorhanden ist, aber wir tun es. Die Spezifikation besagt, Content-Length zu ignorieren, wenn Transfer-Encoding vorhanden ist, was die Browser tun, also funktioniert es für uns

Änderungen zur Implementierung einer standardskonformen Hop-by-Hop-Komprimierung auf rückwärtskompatible Weise sind ein Thema für weitere Untersuchungen. Jede Änderung an dechunk-gzip-rechunk würde einen neuen Kodierungstyp erfordern, möglicherweise x-i2p-gzchunked. Dies wäre identisch mit Transfer-Encoding: gzip, müsste aber aus Kompatibilitätsgründen anders signalisiert werden. Jede Änderung würde einen formellen Vorschlag erfordern.

#### Transparente Anfrage-Komprimierung {#transparent-request-compression}

Nicht unterstützt, obwohl POST davon profitieren würde. Beachten Sie, dass wir immer noch die zugrunde liegende gzip-Komprimierung auf der I2CP-Ebene haben.

#### Persistenz {#persistence}

Die Client- und Server-Proxies unterstützen derzeit keine RFC 2616 HTTP persistenten Sockets auf einem der drei Hops (Browser-Socket, I2P-Socket, Server-Socket). Connection: close Header werden an jedem Hop eingefügt. Änderungen zur Implementierung von Persistenz werden untersucht. Diese Änderungen sollten standardkonform und rückwärtskompatibel sein und würden keinen formellen Vorschlag erfordern.

#### Pipelining {#pipelining}

Die Client- und Server-Proxys unterstützen derzeit kein RFC 2616 HTTP-Pipelining und es gibt keine Pläne, dies zu tun. Moderne Browser unterstützen kein Pipelining über Proxys, da die meisten Proxys es nicht korrekt implementieren können.

#### Kompatibilität {#compatibility}

Proxy-Implementierungen müssen korrekt mit anderen Implementierungen auf der anderen Seite funktionieren. Client-Proxies sollten ohne einen HTTP-bewussten Server-Proxy (d.h. einen Standard-tunnel) auf der Serverseite funktionieren. Nicht alle Implementierungen unterstützen x-i2p-gzip.

#### User Agent {#user-agent}

Je nachdem, ob der tunnel einen outproxy verwendet oder nicht, wird er den folgenden User-Agent anhängen:

- *Outproxy:* **User-Agent:** Verwendet den User-Agent einer aktuellen Firefox-Version unter Windows
- *Interne I2P-Nutzung:* **User-Agent:** MYOB/6.66 (AN/ON)

### IRC-Client {#client-mode-irc}

Erstellt eine Verbindung zu einem zufälligen IRC-Server, der durch die kommagetrennte (", ") Liste von Zielen angegeben wird. Aus Anonymitätsgründen ist nur eine auf einer Whitelist stehende Teilmenge von IRC-Befehlen erlaubt.

Die folgende Erlaubnisliste gilt für Befehle, die vom IRC-Server an den IRC-Client eingehen.

**Zulassungsliste:** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

Es gibt auch eine Erlaubnisliste für Befehle, die vom IRC-Client zum IRC-Server gesendet werden. Diese ist aufgrund der Anzahl an IRC-Verwaltungsbefehlen recht umfangreich. Siehe den IRCFilter.java-Quellcode für Details.

Der ausgehende Filter modifiziert auch die folgenden Befehle, um identifizierende Informationen zu entfernen: - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

Ermöglicht die Verwendung des I2P routers als SOCKS-Proxy.

### SOCKS IRC {#client-mode-socks-irc}

Ermöglicht die Verwendung des I2P routers als SOCKS-Proxy mit der Befehlswhitelist, die durch den [IRC](#client-mode-irc) Client-Modus spezifiziert wird.

### CONNECT {#client-mode-connect}

Erstellt einen HTTP-Tunnel und verwendet die HTTP-Anfragemethode "CONNECT", um einen TCP-Tunnel aufzubauen, der normalerweise für SSL und HTTPS verwendet wird.

### Streamr {#client-mode-streamr}

Erstellt einen UDP-Server, der an einen Streamr-Client I2PTunnel angebunden ist. Der Streamr-Client-Tunnel wird sich bei einem Streamr-Server-Tunnel anmelden.

![Streamr-Diagramm](/images/I2PTunnel-streamr.png)

## Server-Modi {#server-modes}

### Standard {#server-mode-standard}

Erstellt ein Ziel zu einer lokalen ip:port mit einem offenen TCP-Port.

### HTTP {#server-mode-http}

Erstellt eine Destination zu einem lokalen HTTP-Server ip:port. Unterstützt gzip für Anfragen mit Accept-encoding: x-i2p-gzip, antwortet mit Content-encoding: x-i2p-gzip bei solchen Anfragen.

Der HTTP-Server-Proxy bietet eine Reihe von Diensten, um das Hosting einer Website einfacher und sicherer zu machen und eine bessere Benutzererfahrung auf der Client-Seite zu bieten.

**Request-Header-Verarbeitung:** - Header-Validierung - Header-Spoofing-Schutz - Header-Größenprüfungen - Optionale inproxy- und User-Agent-Ablehnung - X-I2P-Header hinzufügen, damit der Webserver weiß, woher die Anfrage kam - Host-Header-Ersetzung zur Vereinfachung von Webserver-vhosts - Erzwinge connection: close - RFC-konforme hop-by-hop Header-Verarbeitung und -Entfernung - Pufferung aller Header vor Weiterleitung zur Effizienzsteigerung

**DDoS-Schutz:** - POST-Drosselung - Timeouts und Slowloris-Schutz - Zusätzliche Drosselung erfolgt im Streaming für alle tunnel-Typen

**Verarbeitung der Antwort-Header:** - Entfernung einiger datenschutzproblematischer Header - Überprüfung von MIME-Typ und anderen Headern zur Bestimmung der Antwort-Komprimierung - Erzwingung von connection: close - RFC-konforme Verarbeitung und Entfernung von Hop-by-Hop-Headern - Pufferung aller Header vor der Weiterleitung für bessere Effizienz

**HTTP-Fehlerantworten:** - Für viele häufige und nicht so häufige Fehler sowie bei Drosselung, damit der clientseitige Benutzer weiß, was passiert ist

**Transparente Antwort-Komprimierung:** - Der Webserver und/oder die I2CP-Schicht können komprimieren, aber der Webserver tut dies oft nicht, und es ist am effizientesten, auf einer hohen Schicht zu komprimieren, auch wenn I2CP ebenfalls komprimiert. Der HTTP-Server-Proxy arbeitet kooperativ mit dem clientseitigen Proxy zusammen, um Antworten transparent zu komprimieren.

### HTTP Bidirektional {#server-mode-http-bidir}

*Veraltet*

Funktioniert sowohl als I2PTunnel HTTP Server als auch als I2PTunnel HTTP Client ohne Outproxy-Funktionen. Eine Beispielanwendung wäre eine Webanwendung, die Client-ähnliche Anfragen stellt, oder das Loopback-Testen einer I2P-Site als Diagnosewerkzeug.

### IRC Server {#server-mode-irc}

Erstellt ein Ziel, das die Registrierungssequenz eines Clients filtert und den destination key des Clients als Hostname an den IRC-Server weitergibt.

### Streamr {#server-mode-streamr}

Ein UDP-Client, der sich mit einem Medienserver verbindet, wird erstellt. Der UDP-Client ist mit einem Streamr-Server I2PTunnel gekoppelt.
