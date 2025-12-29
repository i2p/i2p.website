---
title: "Häufig gestellte Fragen"
description: "Umfassende I2P FAQ: Router-Hilfe, Konfiguration, Reseeds, Privatsphäre/Sicherheit, Leistung und Fehlerbehebung"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## I2P Router Hilfe

### Auf welchen Systemen läuft I2P? {#systems}

I2P ist in der Programmiersprache Java geschrieben. Es wurde auf Windows, Linux, FreeBSD und OSX getestet. Eine Android-Portierung ist ebenfalls verfügbar.

In Bezug auf die Speichernutzung ist I2P standardmäßig so konfiguriert, dass es 128 MB RAM verwendet. Dies ist ausreichend für das Surfen und die Nutzung von IRC. Andere Aktivitäten können jedoch eine höhere Speicherzuweisung erfordern. Wenn man beispielsweise einen Router mit hoher Bandbreite betreiben, an I2P-Torrents teilnehmen oder Hidden Services mit hohem Datenverkehr bereitstellen möchte, ist eine größere Speichermenge erforderlich.

Was die CPU-Nutzung betrifft, wurde I2P erfolgreich auf bescheidenen Systemen wie der Raspberry Pi-Reihe von Einplatinencomputern getestet. Da I2P intensiv kryptografische Verfahren nutzt, ist eine leistungsstärkere CPU besser geeignet, um die von I2P erzeugte Arbeitslast sowie Aufgaben des restlichen Systems (d.h. Betriebssystem, GUI, andere Prozesse wie z.B. Webbrowsing) zu bewältigen.

Die Verwendung von Sun/Oracle Java oder OpenJDK wird empfohlen.

### Ist die Installation von Java erforderlich, um I2P zu verwenden? {#java}

Ja, Java ist erforderlich, um I2P Core zu verwenden. Wir haben Java in unseren Easy-Installern für Windows, Mac OSX und Linux enthalten. Wenn Sie die I2P-Android-App ausführen, benötigen Sie in den meisten Fällen auch eine Java-Laufzeitumgebung wie Dalvik oder ART.

### Was ist eine "I2P Site" und wie konfiguriere ich meinen Browser, damit ich sie nutzen kann? {#I2P-Site}

Eine I2P-Site ist eine normale Website, mit dem Unterschied, dass sie innerhalb von I2P gehostet wird. I2P-Sites haben Adressen, die wie normale Internetadressen aussehen und auf ".i2p" enden – in einer für Menschen lesbaren, nicht-kryptografischen Form, zum Nutzen der Benutzer. Die tatsächliche Verbindung zu einer I2P-Site erfordert Kryptografie, was bedeutet, dass I2P-Site-Adressen auch als lange "Base64"-Destinations und kürzere "B32"-Adressen existieren. Möglicherweise müssen Sie zusätzliche Konfigurationen vornehmen, um korrekt zu browsen. Zum Browsen von I2P-Sites müssen Sie den HTTP-Proxy in Ihrer I2P-Installation aktivieren und dann Ihren Browser so konfigurieren, dass er diesen verwendet. Für weitere Informationen konsultieren Sie den Abschnitt "Browser" weiter unten oder die Anleitung zur "Browser-Konfiguration".

### Was bedeuten die Aktiv x/y Zahlen in der Router-Konsole? {#active}

Auf der Peers-Seite in Ihrer Router-Konsole sehen Sie möglicherweise zwei Zahlen - Aktiv x/y. Die erste Zahl ist die Anzahl der Peers, an die Sie in den letzten Minuten eine Nachricht gesendet oder von denen Sie eine Nachricht empfangen haben. Die zweite Zahl ist die Anzahl der kürzlich gesehenen Peers, diese wird immer größer oder gleich der ersten Zahl sein.

### Mein Router hat sehr wenige aktive Peers, ist das in Ordnung? {#peers}

Ja, dies kann normal sein, besonders wenn der Router gerade erst gestartet wurde. Neue Router benötigen Zeit zum Hochfahren und zum Verbinden mit dem Rest des Netzwerks. Um die Netzwerkintegration, Betriebszeit und Leistung zu verbessern, überprüfen Sie diese Einstellungen:

- **Bandbreite teilen** - Wenn ein Router so konfiguriert ist, dass er Bandbreite teilt, wird er mehr Datenverkehr für andere Router weiterleiten, was dabei hilft, ihn in den Rest des Netzwerks zu integrieren und die Leistung der eigenen lokalen Verbindung verbessert. Dies kann auf der Seite [http://localhost:7657/config](http://localhost:7657/config) konfiguriert werden.
- **Netzwerkschnittstelle** - Stellen Sie sicher, dass auf der Seite [http://localhost:7657/confignet](http://localhost:7657/confignet) keine Schnittstelle angegeben ist. Dies kann die Leistung beeinträchtigen, es sei denn, Ihr Computer ist multi-homed mit mehreren externen IP-Adressen.
- **I2NP-Protokoll** - Stellen Sie sicher, dass der Router so konfiguriert ist, dass er Verbindungen über ein gültiges Protokoll für das Betriebssystem des Hosts und leere Netzwerk(Erweitert)-Einstellungen erwartet. Geben Sie keine IP-Adresse in das Feld 'Hostname' auf der Netzwerkkonfigurationsseite ein. Das hier ausgewählte I2NP-Protokoll wird nur verwendet, wenn Sie noch keine erreichbare Adresse haben. Die meisten Verizon 4G- und 5G-Drahtlosverbindungen in den Vereinigten Staaten blockieren beispielsweise UDP und können darüber nicht erreicht werden. Andere würden UDP zwangsweise verwenden, auch wenn es ihnen zur Verfügung steht. Wählen Sie eine sinnvolle Einstellung aus den aufgeführten I2NP-Protokollen.

### Ich bin gegen bestimmte Arten von Inhalten. Wie kann ich verhindern, dass ich sie verteile, speichere oder darauf zugreife? {#badcontent}

Standardmäßig ist keines dieser Inhalte installiert. Da I2P jedoch ein Peer-to-Peer-Netzwerk ist, kann es vorkommen, dass Sie versehentlich auf verbotene Inhalte stoßen. Hier ist eine Zusammenfassung, wie I2P verhindert, dass Sie ungewollt in Verstöße gegen Ihre Überzeugungen verwickelt werden.

- **Verteilung** - Der Datenverkehr ist intern im I2P-Netzwerk, Sie sind kein [Exit-Knoten](#exit) (in unserer Dokumentation als Outproxy bezeichnet).
- **Speicherung** - Das I2P-Netzwerk führt keine verteilte Speicherung von Inhalten durch, dies muss vom Benutzer speziell installiert und konfiguriert werden (zum Beispiel mit Tahoe-LAFS). Das ist eine Funktion eines anderen anonymen Netzwerks, [Freenet](http://freenetproject.org/). Durch den Betrieb eines I2P-routers speichern Sie keine Inhalte für andere.
- **Zugriff** - Ihr router wird keine Inhalte ohne Ihre ausdrückliche Anweisung anfordern.

### Ist es möglich, I2P zu blockieren? {#blocking}

Ja, bei weitem der einfachste und häufigste Weg ist das Blockieren von Bootstrap- oder "Reseed"-Servern. Das vollständige Blockieren des gesamten verschleierten Datenverkehrs würde ebenfalls funktionieren (obwohl dies viele, viele andere Dinge, die nicht I2P sind, beeinträchtigen würde und die meisten nicht bereit sind, so weit zu gehen). Im Fall der Reseed-Blockierung gibt es ein Reseed-Bundle auf Github; dessen Blockierung würde auch Github blockieren. Sie können Reseed über einen Proxy durchführen (viele können im Internet gefunden werden, wenn Sie nicht Tor verwenden möchten) oder Reseed-Bundles auf Freund-zu-Freund-Basis offline teilen.

### In `wrapper.log` sehe ich einen Fehler mit der Meldung "`Protocol family unavailable`" beim Laden der Router Console {#protocolfamily}

Dieser Fehler tritt häufig bei jeder netzwerkfähigen Java-Software auf Systemen auf, die standardmäßig für die Verwendung von IPv6 konfiguriert sind. Es gibt einige Möglichkeiten, dies zu lösen:

- Auf Linux-basierten Systemen können Sie `echo 0 > /proc/sys/net/ipv6/bindv6only` ausführen
- Suchen Sie nach den folgenden Zeilen in `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Wenn die Zeilen vorhanden sind, kommentieren Sie sie aus, indem Sie die "#"-Zeichen entfernen. Wenn die Zeilen nicht vorhanden sind, fügen Sie sie ohne die "#"-Zeichen hinzu.

Eine weitere Möglichkeit wäre, die `::1` aus `~/.i2p/clients.config` zu entfernen

**WARNUNG**: Damit Änderungen an `wrapper.config` wirksam werden, müssen Sie den Router und den Wrapper vollständig stoppen. Ein Klick auf *Neustart* in Ihrer Router-Konsole wird diese Datei NICHT neu einlesen! Sie müssen auf *Herunterfahren* klicken, 11 Minuten warten und dann I2P starten.

### Die meisten I2P-Sites innerhalb von I2P sind nicht erreichbar? {#down}

Wenn man jede I2P Site betrachtet, die jemals erstellt wurde, dann ja, die meisten sind nicht mehr erreichbar. Menschen und I2P Sites kommen und gehen. Ein guter Weg, um mit I2P anzufangen, ist eine Liste von I2P Sites zu überprüfen, die derzeit aktiv sind. [identiguy.i2p](http://identiguy.i2p) verfolgt aktive I2P Sites.

### Warum lauscht I2P auf Port 32000? {#port32000}

Der Tanuki Java Service Wrapper, den wir verwenden, öffnet diesen Port – gebunden an localhost – um mit der im JVM laufenden Software zu kommunizieren. Wenn die JVM gestartet wird, erhält sie einen Schlüssel, damit sie sich mit dem Wrapper verbinden kann. Nachdem die JVM ihre Verbindung zum Wrapper hergestellt hat, lehnt der Wrapper alle weiteren Verbindungen ab.

Weitere Informationen finden Sie in der [Wrapper-Dokumentation](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Wie konfiguriere ich meinen Browser? {#browserproxy}

Die Proxy-Konfiguration für verschiedene Browser befindet sich auf einer separaten Seite mit Screenshots. Fortgeschrittenere Konfigurationen mit externen Tools, wie dem Browser-Plugin FoxyProxy oder dem Proxy-Server Privoxy, sind möglich, könnten aber Lecks in Ihrer Konfiguration verursachen.

### Wie verbinde ich mich mit IRC innerhalb von I2P? {#irc}

Ein Tunnel zum Haupt-IRC-Server innerhalb von I2P, Irc2P, wird bei der Installation von I2P erstellt (siehe die [I2PTunnel-Konfigurationsseite](http://localhost:7657/i2ptunnel/index.jsp)) und wird automatisch gestartet, wenn der I2P-Router startet. Um sich zu verbinden, konfigurieren Sie Ihren IRC-Client so, dass er sich mit `localhost 6668` verbindet. Benutzer von HexChat-ähnlichen Clients können ein neues Netzwerk mit dem Server `localhost/6668` erstellen (denken Sie daran, "Proxy-Server umgehen" anzukreuzen, falls Sie einen Proxy-Server konfiguriert haben). Weechat-Benutzer können den folgenden Befehl verwenden, um ein neues Netzwerk hinzuzufügen:

```
/server add irc2p localhost/6668
```
### Wie richte ich meine eigene I2P Site ein? {#myI2P-Site}

Die einfachste Methode besteht darin, auf den [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/)-Link in der Router-Konsole zu klicken und einen neuen 'Server Tunnel' zu erstellen. Sie können dynamische Inhalte bereitstellen, indem Sie das Tunnel-Ziel auf den Port eines vorhandenen Webservers wie Tomcat oder Jetty setzen. Sie können auch statische Inhalte bereitstellen. Setzen Sie dazu das Tunnel-Ziel auf: `0.0.0.0 port 7659` und platzieren Sie den Inhalt im Verzeichnis `~/.i2p/eepsite/docroot/`. (Auf Nicht-Linux-Systemen kann sich dies an einem anderen Ort befinden. Überprüfen Sie die Router-Konsole.) Die 'eepsite'-Software ist Teil des I2P-Installationspakets und wird automatisch gestartet, wenn I2P gestartet wird. Die dabei erstellte Standardseite ist unter http://127.0.0.1:7658 erreichbar. Ihre 'eepsite' ist jedoch auch für andere über Ihre eepsite-Schlüsseldatei zugänglich, die sich hier befindet: `~/.i2p/eepsite/i2p/eepsite.keys`. Um mehr zu erfahren, lesen Sie die Readme-Datei unter: `~/.i2p/eepsite/README.txt`.

### Wenn ich zu Hause eine Website auf I2P hoste, die nur HTML und CSS enthält, ist das gefährlich? {#hosting}

Es hängt von Ihrem Gegner und Ihrem Bedrohungsmodell ab. Wenn Sie sich nur um unternehmerische "Datenschutz"-Verletzungen, typische Kriminelle und Zensur sorgen, dann ist es nicht wirklich gefährlich. Strafverfolgungsbehörden werden Sie wahrscheinlich trotzdem finden, wenn sie es wirklich wollen. Nur das Hosting zu betreiben, wenn Sie einen normalen (Internet-)Heimbrowser laufen haben, macht es wirklich schwierig herauszufinden, wer diesen Teil hostet. Bitte betrachten Sie das Hosting Ihrer I2P-Site genauso wie das Hosting jedes anderen Dienstes - es ist so gefährlich - oder sicher - wie Sie es selbst konfigurieren und verwalten.

Hinweis: Es gibt bereits eine Möglichkeit, das Hosting eines i2p-Dienstes (destination) vom i2p-Router zu trennen. Wenn Sie [verstehen, wie](/docs/overview/tech-intro#i2pservices) es funktioniert, können Sie einfach eine separate Maschine als Server für die Website (oder den Dienst) einrichten, die öffentlich zugänglich sein wird, und diese über einen [sehr] sicheren SSH-Tunnel an den Webserver weiterleiten oder ein gesichertes, gemeinsam genutztes Dateisystem verwenden.

### Wie findet I2P ".i2p"-Websites? {#addresses}

Die I2P-Adressbuch-Anwendung ordnet menschenlesbare Namen langfristigen Zielen (Destinations) zu, die mit Diensten verbunden sind, wodurch sie eher einer Hosts-Datei oder einer Kontaktliste ähnelt als einer Netzwerkdatenbank oder einem DNS-Dienst. Sie ist außerdem lokal ausgerichtet – es gibt keinen anerkannten globalen Namensraum, Sie entscheiden, worauf eine bestimmte .i2p-Domain letztendlich verweist. Der Mittelweg ist etwas, das als "Jump Service" bezeichnet wird und einen menschenlesbaren Namen bereitstellt, indem es Sie zu einer Seite weiterleitet, auf der Sie gefragt werden: "Geben Sie dem I2P-Router die Erlaubnis, $SITE_CRYPTO_KEY den Namen $SITE_NAME.i2p zu nennen" oder etwas in dieser Art. Sobald es in Ihrem Adressbuch ist, können Sie Ihre eigenen Jump-URLs generieren, um die Seite mit anderen zu teilen.

### Wie füge ich Adressen zum Adressbuch hinzu? {#addressbook}

Sie können keine Adresse hinzufügen, ohne zumindest die Base32- oder Base64-Adresse der Website zu kennen, die Sie besuchen möchten. Der „Hostname", der für Menschen lesbar ist, ist nur ein Alias für die kryptografische Adresse, die der Base32- oder Base64-Adresse entspricht. Ohne die kryptografische Adresse gibt es keine Möglichkeit, auf eine I2P-Site zuzugreifen – das ist beabsichtigt. Die Verteilung der Adresse an Personen, die sie noch nicht kennen, liegt normalerweise in der Verantwortung des Jump-Service-Anbieters. Der Besuch einer unbekannten I2P-Site löst die Verwendung eines Jump-Service aus. stats.i2p ist der zuverlässigste Jump-Service.

Wenn Sie eine Website über i2ptunnel hosten, hat diese noch keine Registrierung bei einem Jump-Service. Um ihr lokal eine URL zu geben, besuchen Sie die Konfigurationsseite und klicken Sie auf die Schaltfläche "Add to Local Address Book". Gehen Sie dann zu http://127.0.0.1:7657/dns, um die Addresshelper-URL nachzuschlagen und zu teilen.

### Welche Ports verwendet I2P? {#ports}

Die von I2P verwendeten Ports lassen sich in 2 Bereiche unterteilen:

1. Internetfähige Ports, die für die Kommunikation mit anderen I2P-Routern verwendet werden
2. Lokale Ports für lokale Verbindungen

Diese werden im Folgenden ausführlich beschrieben.

#### 1. Nach außen offene Ports

Hinweis: Seit Version 0.7.8 verwenden neue Installationen nicht mehr Port 8887; ein zufälliger Port zwischen 9000 und 31000 wird ausgewählt, wenn das Programm zum ersten Mal ausgeführt wird. Der ausgewählte Port wird auf der Router-[Konfigurationsseite](http://127.0.0.1:7657/confignet) angezeigt.

**AUSGEHEND**

- UDP vom zufälligen Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) aufgeführt ist, zu beliebigen entfernten UDP-Ports, mit Antwortmöglichkeit
- TCP von zufälligen hohen Ports zu beliebigen entfernten TCP-Ports
- Ausgehende UDP-Verbindungen auf Port 123, mit Antwortmöglichkeit. Dies ist für die interne Zeitsynchronisation von I2P erforderlich (über SNTP - Abfrage eines zufälligen SNTP-Hosts in pool.ntp.org oder eines anderen von Ihnen angegebenen Servers)

**EINGEHEND**

- (Optional, empfohlen) UDP zum Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) angegeben ist, von beliebigen Standorten
- (Optional, empfohlen) TCP zum Port, der auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) angegeben ist, von beliebigen Standorten
- Eingehende TCP-Verbindungen können auf der [Konfigurationsseite](http://127.0.0.1:7657/confignet) deaktiviert werden

#### 2. Lokale I2P-Ports

Lokale I2P-Ports lauschen standardmäßig nur auf lokale Verbindungen, außer wo anders angegeben:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### In meinem Adressbuch fehlen viele Hosts. Was sind gute Abonnement-Links? {#subscriptions}

Das Adressbuch befindet sich unter [http://localhost:7657/dns](http://localhost:7657/dns), wo weitere Informationen zu finden sind.

**Was sind gute Abonnement-Links für das Adressbuch?**

Sie können Folgendes versuchen:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### Wie kann ich von anderen Rechnern auf die Webkonsole zugreifen oder sie mit einem Passwort schützen? {#remote_webconsole}

Aus Sicherheitsgründen akzeptiert die Admin-Konsole des Routers standardmäßig nur Verbindungen über das lokale Interface.

Es gibt zwei Methoden, um remote auf die Konsole zuzugreifen:

1. SSH Tunnel
2. Konfigurieren Sie Ihre Konsole so, dass sie über eine öffentliche IP-Adresse mit Benutzernamen und Passwort verfügbar ist

Diese werden im Folgenden detailliert beschrieben:

**Methode 1: SSH-Tunnel**

Wenn Sie ein Unix-ähnliches Betriebssystem verwenden, ist dies die einfachste Methode für den Remote-Zugriff auf Ihre I2P-Konsole. (Hinweis: SSH-Server-Software ist auch für Systeme unter Windows verfügbar, zum Beispiel [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Sobald Sie SSH-Zugriff auf Ihr System konfiguriert haben, wird das Flag '-L' mit entsprechenden Argumenten an SSH übergeben - zum Beispiel:

```
ssh -L 7657:localhost:7657 (System_IP)
```
wobei '(System_IP)' durch die IP-Adresse Ihres Systems ersetzt wird. Dieser Befehl leitet Port 7657 (die Zahl vor dem ersten Doppelpunkt) an den Port 7657 des entfernten Systems (spezifiziert durch die Zeichenkette 'localhost' zwischen dem ersten und zweiten Doppelpunkt) weiter (die Zahl nach dem zweiten Doppelpunkt). Ihre entfernte I2P-Konsole ist nun auf Ihrem lokalen System unter 'http://localhost:7657' verfügbar und bleibt verfügbar, solange Ihre SSH-Sitzung aktiv ist.

Wenn Sie eine SSH-Sitzung starten möchten, ohne eine Shell auf dem entfernten System zu initiieren, können Sie das Flag '-N' hinzufügen:

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Methode 2: Konfigurieren Sie Ihre Konsole so, dass sie über eine öffentliche IP-Adresse mit Benutzername und Passwort erreichbar ist**

1. Öffnen Sie `~/.i2p/clients.config` und ersetzen Sie:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   durch:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   wobei Sie (System_IP) durch die öffentliche IP-Adresse Ihres Systems ersetzen

2. Gehen Sie zu [http://localhost:7657/configui](http://localhost:7657/configui) und fügen Sie bei Bedarf einen Konsolenbenutzernamen und ein Passwort hinzu - Das Hinzufügen eines Benutzernamens und Passworts wird dringend empfohlen, um Ihre I2P-Konsole vor unbefugtem Zugriff zu schützen, was zu einer De-Anonymisierung führen könnte.

3. Gehe zu [http://localhost:7657/index](http://localhost:7657/index) und klicke auf "Graceful restart", was die JVM neu startet und die Client-Anwendungen neu lädt

Nachdem das gestartet ist, sollten Sie nun in der Lage sein, Ihre Konsole remote zu erreichen. Laden Sie die Router-Konsole unter `http://(System_IP):7657` und Sie werden nach dem Benutzernamen und Passwort gefragt, die Sie in Schritt 2 oben angegeben haben, sofern Ihr Browser das Authentifizierungs-Popup unterstützt.

HINWEIS: Sie können 0.0.0.0 in der obigen Konfiguration angeben. Dies gibt eine Schnittstelle an, nicht ein Netzwerk oder eine Netzmaske. 0.0.0.0 bedeutet "an alle Schnittstellen binden", sodass es sowohl unter 127.0.0.1:7657 als auch unter jeder LAN/WAN-IP erreichbar sein kann. Seien Sie vorsichtig bei der Verwendung dieser Option, da die Konsole auf ALLEN auf Ihrem System konfigurierten Adressen verfügbar sein wird.

### Wie kann ich Anwendungen von meinen anderen Rechnern nutzen? {#remote_i2cp}

Bitte sehen Sie sich die vorherige Antwort für Anweisungen zur Verwendung von SSH Port Forwarding an und besuchen Sie auch diese Seite in Ihrer Konsole: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### Ist es möglich, I2P als SOCKS-Proxy zu verwenden? {#socks}

Der SOCKS-Proxy ist seit Version 0.7.1 funktionsfähig. SOCKS 4/4a/5 werden unterstützt. I2P verfügt nicht über einen SOCKS-Outproxy, daher ist die Nutzung auf I2P beschränkt.

Viele Anwendungen geben sensible Informationen preis, die Sie im Internet identifizieren könnten, und dies ist ein Risiko, dessen man sich bei der Verwendung des I2P-SOCKS-Proxys bewusst sein sollte. I2P filtert nur Verbindungsdaten, aber wenn das Programm, das Sie verwenden möchten, diese Informationen als Inhalt sendet, hat I2P keine Möglichkeit, Ihre Anonymität zu schützen. Beispielsweise senden einige E-Mail-Anwendungen die IP-Adresse des Rechners, auf dem sie laufen, an einen Mailserver. Wir empfehlen I2P-spezifische Werkzeuge oder Anwendungen (wie [I2PSnark](http://localhost:7657/i2psnark/) für Torrents) oder Anwendungen, von denen bekannt ist, dass sie sicher mit I2P verwendet werden können, einschließlich beliebter Plugins, die auf [Firefox](https://www.mozilla.org/) zu finden sind.

### Wie greife ich auf IRC, BitTorrent oder andere Dienste im regulären Internet zu? {#proxy_other}

Es gibt Dienste namens Outproxies, die zwischen I2P und dem Internet vermitteln, ähnlich wie Tor Exit Nodes. Die Standard-Outproxy-Funktionalität für HTTP und HTTPS wird von `exit.stormycloud.i2p` bereitgestellt und von StormyCloud Inc. betrieben. Sie wird im HTTP-Proxy konfiguriert. Um die Anonymität zusätzlich zu schützen, erlaubt I2P standardmäßig keine anonymen Verbindungen zum regulären Internet. Weitere Informationen finden Sie auf der Seite [Socks Outproxy](/docs/api/socks#outproxy).

---

## Reseeds

### Mein Router läuft seit mehreren Minuten und hat keine oder sehr wenige Verbindungen {#reseed}

Überprüfen Sie zunächst die [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) Seite in der Router Console – Ihre Netzwerkdatenbank. Wenn Sie keinen einzigen Router von innerhalb I2P aufgelistet sehen, die Konsole aber anzeigt, dass Sie hinter einer Firewall sein sollten, dann können Sie wahrscheinlich keine Verbindung zu den Reseed-Servern herstellen. Wenn Sie andere I2P-Router aufgelistet sehen, versuchen Sie, die Anzahl der maximalen Verbindungen unter [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) zu reduzieren – möglicherweise kann Ihr Router nicht viele Verbindungen verarbeiten.

### Wie führe ich ein manuelles Reseeding durch? {#manual_reseed}

Unter normalen Umständen verbindet I2P Sie automatisch mit dem Netzwerk über unsere Bootstrap-Links. Wenn eine gestörte Internetverbindung das Bootstrapping von Reseed-Servern scheitern lässt, ist eine einfache Möglichkeit zum Bootstrapping die Verwendung des Tor-Browsers (standardmäßig öffnet er localhost), der sehr gut mit [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed) funktioniert. Es ist auch möglich, einen I2P-router manuell zu reseeden.

Wenn Sie den Tor-Browser zum Reseeden verwenden, können Sie mehrere URLs auf einmal auswählen und fortfahren. Obwohl der Standardwert von 2 (von den mehreren URLs) auch funktioniert, wird es langsam sein.

---

## Privatsphäre-Sicherheit

### Ist mein Router ein "Exit Node" (Outproxy) zum regulären Internet? Ich möchte nicht, dass er einer ist. {#exit}

Nein, Ihr Router beteiligt sich am Transport von verschlüsseltem Ende-zu-Ende-Verkehr durch das I2P-Netzwerk zu einem zufälligen Tunnel-Endpunkt, normalerweise nicht zu einem Outproxy, aber es wird kein Verkehr zwischen Ihrem Router und dem Internet über die Transportschicht weitergeleitet. Als Endbenutzer sollten Sie keinen Outproxy betreiben, wenn Sie nicht über Kenntnisse in der System- und Netzwerkadministration verfügen.

### Ist es einfach, die Nutzung von I2P durch Analyse des Netzwerkverkehrs zu erkennen? {#detection}

I2P-Verkehr sieht normalerweise wie UDP-Verkehr aus, und nicht viel mehr – und es zu einem Ziel zu machen, dass er nicht viel mehr aussieht, ist ein Ziel. Es unterstützt auch TCP. Mit einigem Aufwand kann die passive Verkehrsanalyse möglicherweise den Verkehr als "I2P" klassifizieren, aber wir hoffen, dass die fortlaufende Entwicklung von Traffic Obfuscation dies weiter reduzieren wird. Selbst eine recht einfache Protokoll-Verschleierungsschicht wie obfs4 wird Zensoren daran hindern, I2P zu blockieren (es ist ein Ziel, das I2P verfolgt).

### Ist die Nutzung von I2P sicher? {#safe}

Es hängt von Ihrem persönlichen Bedrohungsmodell ab. Für die meisten Menschen ist I2P wesentlich sicherer als die Nutzung ohne jeglichen Schutz. Einige andere Netzwerke (wie Tor, mixminion/mixmaster) sind wahrscheinlich sicherer gegen bestimmte Gegner. Beispielsweise verwendet I2P-Verkehr kein TLS/SSL, sodass es nicht die „schwächstes Glied"-Probleme hat, die Tor hat. I2P wurde während des „Arabischen Frühlings" von vielen Menschen in Syrien genutzt, und in jüngster Zeit hat das Projekt ein stärkeres Wachstum bei kleineren sprachlichen Installationen von I2P im Nahen und Mittleren Osten verzeichnet. Das Wichtigste, was hier zu beachten ist: I2P ist eine Technologie und Sie benötigen eine Anleitung, um Ihre Privatsphäre/Anonymität im Internet zu verbessern. Überprüfen Sie auch Ihren Browser oder importieren Sie die Fingerprint-Suchmaschine, um Fingerprint-Angriffe mit einem sehr großen (bedeutet: typische Long-Tail-Verteilungen / sehr präzise diverse Datenstruktur) Datensatz über viele Umgebungsfaktoren zu blockieren, und verwenden Sie kein VPN, um alle Risiken zu reduzieren, die von ihm selbst ausgehen, wie das eigene TLS-Cache-Verhalten und die technische Konstruktion des Provider-Geschäfts, das leichter gehackt werden kann als ein eigenes Desktop-System. Möglicherweise ist die Verwendung eines isolierten Tor-V-Browsers mit seinen großartigen Anti-Fingerprint-Schutzmaßnahmen und einem umfassenden Appguard-Laufzeitschutz, der nur die notwendigen Systemkommunikationen zulässt, sowie eine letzte VM-Nutzung mit Anti-Spy-Deaktivierungsskripten und Live-CD, um jedes „nahezu dauerhaft mögliche Risiko" zu entfernen und alle Risiken durch eine abnehmende Wahrscheinlichkeit zu senken, eine gute Option in öffentlichen Netzwerken und individuellen Hochrisiko-Modellen und könnte das Beste sein, was Sie mit diesem Ziel für die I2P-Nutzung tun können.

### Ich sehe IP-Adressen aller anderen I2P-Knoten in der Router-Konsole. Bedeutet das, dass meine IP-Adresse für andere sichtbar ist? {#netdb_ip}

Ja, für andere I2P-Knoten, die Ihren Router kennen. Wir verwenden dies, um uns mit dem Rest des I2P-Netzwerks zu verbinden. Die Adressen befinden sich physisch in "routerInfos (Schlüssel-Wert-Objekten)", die entweder remote abgerufen oder von Peers empfangen werden. Die "routerInfos" enthalten einige Informationen (einige optional opportunistisch hinzugefügt), "vom Peer veröffentlicht", über den Router selbst für das Bootstrapping. In diesem Objekt befinden sich keine Daten über Clients. Ein genauerer Blick unter die Haube zeigt, dass jeder mit dem neuesten Typ der ID-Erstellung gezählt wird, genannt "SHA-256 Hashes (niedrig=Positiver Hash(-Schlüssel), hoch=Negativer Hash(+Schlüssel))". Das I2P-Netzwerk hat eine eigene Datenbank mit routerInfos, die während des Uploads und der Indizierung erstellt werden, aber dies hängt tief in der Realisierung der Schlüssel/Wert-Tabellen und der Netzwerktopologie sowie dem Auslastungszustand / Bandbreitenzustand und den Routing-Wahrscheinlichkeiten für die Speicherung in DB-Komponenten ab.

### Ist die Verwendung eines Outproxys sicher? {#proxy_safe}

Es kommt darauf an, wie Sie "sicher" definieren. Outproxies sind großartig, wenn sie funktionieren, aber leider werden sie freiwillig von Personen betrieben, die möglicherweise das Interesse verlieren oder nicht über die Ressourcen verfügen, um sie rund um die Uhr zu betreiben – bitte beachten Sie, dass es Zeiträume geben kann, in denen Dienste nicht verfügbar, unterbrochen oder unzuverlässig sind, und wir sind nicht mit diesem Dienst verbunden und haben keinen Einfluss darauf.

Die Outproxys selbst können Ihren Datenverkehr sehen, mit Ausnahme von Ende-zu-Ende-verschlüsselten HTTPS/SSL-Daten, genau wie Ihr Internetanbieter den Datenverkehr von Ihrem Computer sehen kann. Wenn Sie Ihrem Internetanbieter vertrauen, wäre es mit dem Outproxy nicht schlechter.

### Was ist mit "De-Anonymisierungs"-Angriffen? {#deanon}

Für eine sehr ausführliche Erklärung lesen Sie mehr in unseren Artikeln über das [Bedrohungsmodell](/docs/overview/threat-model). Im Allgemeinen ist eine De-Anonymisierung nicht trivial, aber möglich, wenn Sie nicht vorsichtig genug sind.

---

## Internetzugang/Leistung

### Ich kann über I2P nicht auf reguläre Internetseiten zugreifen. {#outproxy}

Das Proxying zu Internet-Seiten (eepsites, die ins Internet führen) wird als Dienst für I2P-Nutzer von Non-Block-Anbietern bereitgestellt. Dieser Dienst steht nicht im Mittelpunkt der I2P-Entwicklung und wird auf freiwilliger Basis angeboten. Eepsites, die auf I2P gehostet werden, sollten immer ohne Outproxy funktionieren. Outproxies sind eine Annehmlichkeit, aber sie sind von Natur aus weder perfekt noch ein großer Teil des Projekts. Beachten Sie, dass sie möglicherweise nicht den hochwertigen Service bieten können, den andere Dienste von I2P bereitstellen.

### Ich kann nicht auf https:// oder ftp:// Seiten über I2P zugreifen. {#https}

Der Standard-HTTP-Proxy unterstützt nur HTTP- und HTTPS-Outproxying.

### Warum verbraucht mein Router zu viel CPU? {#cpu}

Stellen Sie zunächst sicher, dass Sie die neueste Version aller I2P-bezogenen Komponenten haben – ältere Versionen enthielten unnötige CPU-intensive Codeabschnitte. Es gibt auch ein [Performance-Log](/docs/overview/performance), das einige der Leistungsverbesserungen in I2P im Laufe der Zeit dokumentiert.

### Meine aktiven Peers / bekannten Peers / teilnehmenden Tunnel / Verbindungen / Bandbreite schwanken stark im Zeitverlauf! Stimmt etwas nicht? {#vary}

Die allgemeine Stabilität des I2P-Netzwerks ist ein fortlaufender Forschungsbereich. Ein besonderer Schwerpunkt dieser Forschung liegt darauf, wie kleine Änderungen an Konfigurationseinstellungen das Verhalten des Routers verändern. Da I2P ein Peer-to-Peer-Netzwerk ist, haben die Aktionen anderer Peers einen Einfluss auf die Leistung Ihres Routers.

### Was macht Downloads, Torrents, Webbrowsing und alles andere auf I2P langsamer im Vergleich zum normalen Internet? {#slow}

I2P verfügt über verschiedene Schutzmaßnahmen, die zusätzliches Routing und weitere Verschlüsselungsebenen hinzufügen. Außerdem wird der Datenverkehr über andere Peers (Tunnels) geleitet, die ihre eigene Geschwindigkeit und Qualität haben – einige sind langsam, andere schnell. Dies führt zu einem erheblichen Overhead und Datenverkehr mit unterschiedlichen Geschwindigkeiten in verschiedene Richtungen. Durch das Design werden all diese Dinge I2P im Vergleich zu einer direkten Internetverbindung langsamer machen, aber wesentlich anonymer und dennoch für die meisten Anwendungsfälle schnell genug.

Nachfolgend wird ein Beispiel mit einer Erklärung präsentiert, um einen Kontext für die Überlegungen zu Latenz und Bandbreite bei der Verwendung von I2P zu bieten.

Betrachten Sie das untenstehende Diagramm. Es zeigt eine Verbindung zwischen einem Client, der eine Anfrage über I2P sendet, einem Server, der die Anfrage über I2P empfängt und dann ebenfalls über I2P antwortet. Der Pfad, den die Anfrage durchläuft, ist ebenfalls dargestellt.

Betrachten Sie im Diagramm die Kästchen mit den Bezeichnungen 'P', 'Q' und 'R' als einen ausgehenden Tunnel für 'A' und die Kästchen mit den Bezeichnungen 'X', 'Y' und 'Z' als einen ausgehenden Tunnel für 'B'. Ebenso repräsentieren die Kästchen mit den Bezeichnungen 'X', 'Y' und 'Z' einen eingehenden Tunnel für 'B', während die Kästchen mit den Bezeichnungen 'P_1', 'Q_1' und 'R_1' einen eingehenden Tunnel für 'A' darstellen. Die Pfeile zwischen den Kästchen zeigen die Richtung des Datenverkehrs. Der Text oberhalb und unterhalb der Pfeile gibt Beispiele für die Bandbreite zwischen einem Hop-Paar sowie Beispiele für Latenzen an.

Wenn sowohl Client als auch Server durchgehend 3-Hop-Tunnel verwenden, sind insgesamt 12 andere I2P-Router an der Weiterleitung des Datenverkehrs beteiligt. 6 Peers leiten den Datenverkehr vom Client zum Server weiter, der in einen ausgehenden 3-Hop-Tunnel von 'A' ('P', 'Q', 'R') und einen eingehenden 3-Hop-Tunnel zu 'B' ('X', 'Y', 'Z') aufgeteilt wird. Ebenso leiten 6 Peers den Datenverkehr vom Server zurück zum Client weiter.

Zunächst können wir die Latenz betrachten - die Zeit, die eine Anfrage eines Clients benötigt, um das I2P-Netzwerk zu durchqueren, den Server zu erreichen und zum Client zurückzukehren. Wenn wir alle Latenzen zusammenzählen, sehen wir:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Die gesamte Round-Trip-Zeit in unserem Beispiel beträgt 740 ms - sicherlich deutlich höher als das, was man normalerweise beim Surfen auf regulären Internetseiten sehen würde.

Zweitens können wir die verfügbare Bandbreite betrachten. Diese wird durch die langsamste Verbindung zwischen den Hops vom Client zum Server sowie bei der Übertragung von Datenverkehr vom Server zum Client bestimmt. Für Datenverkehr vom Client zum Server sehen wir in unserem Beispiel, dass die verfügbare Bandbreite zwischen den Hops 'R' & 'X' sowie den Hops 'X' & 'Y' 32 KB/s beträgt. Trotz höherer verfügbarer Bandbreite zwischen den anderen Hops werden diese Hops als Engpass fungieren und die maximal verfügbare Bandbreite für Datenverkehr von 'A' nach 'B' auf 32 KB/s begrenzen. Ebenso zeigt die Verfolgung des Pfades vom Server zum Client, dass es eine maximale Bandbreite von 64 KB/s gibt - zwischen den Hops 'Z_1' & 'Y_1', 'Y_1' & 'X_1' und 'Q_1' & 'P_1'.

Wir empfehlen, Ihre Bandbreitenlimits zu erhöhen. Dies hilft dem Netzwerk, indem die Menge an verfügbarer Bandbreite erhöht wird, was wiederum Ihre I2P-Erfahrung verbessert. Die Bandbreiteneinstellungen finden Sie auf der Seite [http://localhost:7657/config](http://localhost:7657/config). Bitte beachten Sie die Limits Ihrer Internetverbindung, die von Ihrem Internetanbieter vorgegeben werden, und passen Sie Ihre Einstellungen entsprechend an.

Wir empfehlen außerdem, eine ausreichende Menge an geteilter Bandbreite festzulegen - dies ermöglicht es, dass participating tunnels durch Ihren I2P-router geleitet werden. Das Zulassen von participating traffic hält Ihren router gut in das Netzwerk integriert und verbessert Ihre Übertragungsgeschwindigkeiten.

I2P ist ein laufendes Projekt. Viele Verbesserungen und Fehlerbehebungen werden implementiert, und im Allgemeinen wird die Verwendung der neuesten Version Ihre Leistung verbessern. Falls noch nicht geschehen, installieren Sie die neueste Version.

### Ich glaube, ich habe einen Fehler gefunden, wo kann ich ihn melden? {#bug}

Sie können alle Fehler/Probleme, auf die Sie stoßen, in unserem Bugtracker melden, der sowohl über das öffentliche Internet als auch über I2P verfügbar ist. Wir haben ein Diskussionsforum, das ebenfalls über I2P und das öffentliche Internet erreichbar ist. Sie können auch unserem IRC-Kanal beitreten: entweder über unser IRC-Netzwerk IRC2P oder auf Freenode.

- **Unser Bugtracker:**
  - Öffentliches Internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Im I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Unsere Foren:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Logs einfügen:** Sie können interessante Logs bei einem Paste-Dienst wie den im öffentlichen Internet verfügbaren Diensten im [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory) oder einem I2P-Paste-Dienst wie dieser [PrivateBin-Instanz](http://paste.crypthost.i2p) oder diesem [Javascript-freien Paste-Dienst](http://pasta-nojs.i2p) einfügen und auf IRC in #i2p nachfassen
- **IRC:** Treten Sie #i2p-dev bei und diskutieren Sie mit den Entwicklern auf IRC

Bitte fügen Sie relevante Informationen von der Router-Logs-Seite bei, die verfügbar ist unter: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Wir bitten Sie, den gesamten Text aus dem Abschnitt 'I2P Version and Running Environment' sowie alle Fehler oder Warnungen, die in den verschiedenen auf der Seite angezeigten Logs erscheinen, mit uns zu teilen.

---

### Ich habe eine Frage! {#question}

Großartig! Finden Sie uns auf IRC:

- auf `irc.freenode.net` Kanal `#i2p`
- auf `IRC2P` Kanal `#i2p`

oder poste im [Forum](http://i2pforum.i2p/) und wir werden es hier veröffentlichen (hoffentlich mit der Antwort).
