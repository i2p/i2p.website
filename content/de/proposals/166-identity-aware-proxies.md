---
title: "I2P Vorschlag #166: Identitäts-/Hostbewusste Tunneltypen"
number: "166"
author: "eyedeekay"
created: "2024-05-27"
lastupdated: "2024-08-27"
status: "Offen"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.65"
toc: true
---

### Vorschlag für einen Host-bewussten HTTP-Proxy-Tunneltyp

Dies ist ein Vorschlag zur Behebung des „Shared Identity Problems“ bei der konventionellen Nutzung von HTTP-über-I2P durch die Einführung eines neuen HTTP-Proxy-Tunneltyps. Dieser Tunneltyp hat zusätzliches Verhalten, das dazu gedacht ist, das Tracking durch potenziell feindliche versteckte Dienstbetreiber gegen gezielte Benutzeragenten (Browser) und die I2P-Client-Anwendung selbst zu verhindern oder einzuschränken.

#### Was ist das „Shared Identity“-Problem?

Das „Shared Identity“-Problem tritt auf, wenn ein Benutzeragent in einem kryptografisch adressierten Overlay-Netzwerk eine kryptografische Identität mit einem anderen Benutzeragenten teilt. Dies geschieht beispielsweise, wenn ein Firefox und GNU Wget beide so konfiguriert sind, dass sie denselben HTTP-Proxy verwenden.

In diesem Szenario ist es dem Server möglich, die kryptografische Adresse (Destination), die zur Beantwortung der Aktivität verwendet wird, zu sammeln und zu speichern. Er kann dies als einen „Fingerprint“ behandeln, der aufgrund seines kryptografischen Ursprungs immer zu 100 % einzigartig ist. Das bedeutet, dass die Verlinkbarkeit, die durch das Shared Identity Problem beobachtet wird, perfekt ist.

Aber ist es ein Problem?
^^^^^^^^^^^^^^^^^^^^

Das Shared Identity-Problem ist ein Problem, wenn Benutzeragenten, die dasselbe Protokoll sprechen, Unverlinkbarkeit wünschen. [Es wurde erstmals im Kontext von HTTP in diesem Reddit
Thread](https://old.reddit.com/r/i2p/comments/579idi/warning_i2p_is_linkablefingerprintable/) erwähnt, wobei die gelöschten Kommentare dank
[pullpush.io](https://api.pullpush.io/reddit/search/comment/?link_id=579idi) zugänglich sind.
*Zu der Zeit* war ich einer der aktivsten Antworter, und *zu der Zeit* hielt ich das Problem für klein. In den letzten 8 Jahren hat sich die Situation und meine Meinung dazu geändert, und ich glaube jetzt, dass die Bedrohung durch bösartige Zielkorrelation erheblich wächst, da immer mehr Websites in der Lage sind, spezifische Benutzer zu „profilieren“.

Dieser Angriff hat eine sehr niedrige Einstiegshürde. Er erfordert nur, dass ein verborgener Dienstbetreiber mehrere Dienste betreibt. Für Angriffe auf zeitgleiche Besuche (Besuch mehrerer Websites gleichzeitig) ist dies die einzige Voraussetzung. Für nicht-zeitgleiche Verlinkungen muss einer dieser Dienste ein Dienst sein, der „Konten“ hostet, die zu einem einzelnen Benutzer gehören, der getrackt werden soll.

Derzeit kann jeder Dienstbetreiber, der Benutzerkonten hostet, diese mit Aktivitäten auf allen von ihm kontrollierten Websites korrelieren, indem er das Shared Identity-Problem ausnutzt. Mastodon, Gitlab oder sogar einfache Foren könnten getarnte Angreifer sein, solange sie mehr als einen Dienst betreiben und ein Interesse daran haben, ein Profil für einen Benutzer zu erstellen. Diese Überwachung könnte aus Verfolgungsgründen, finanziellem Gewinn oder aus nachrichtendienstlichen Gründen durchgeführt werden. Im Moment gibt es Dutzende von großen Betreibern, die diesen Angriff durchführen und bedeutsame Daten daraus gewinnen könnten. Wir vertrauen ihnen vorerst, dies nicht zu tun, aber Akteure, denen unsere Meinung egal ist, könnten leicht auftauchen.

Dies steht in direktem Zusammenhang mit einer ziemlich grundlegenden Form der Profilbildung im klaren Netz, bei der Organisationen Interaktionen auf ihrer Website mit Interaktionen in von ihnen kontrollierten Netzwerken korrelieren können. Auf I2P kann diese Technik aufgrund der einzigartigen kryptografischen Destination manchmal noch zuverlässiger sein, wenn auch ohne die zusätzliche Macht der Geolokalisierung.

Das Shared Identity-Problem ist nicht nützlich gegen einen Benutzer, der I2P ausschließlich zur Verschleierung der Geolokalisierung verwendet. Es kann auch nicht dazu verwendet werden, das Routing von I2P zu brechen. Es ist nur ein Problem des kontextuellen Identitätsmanagements.

-  Es ist unmöglich, das Shared Identity-Problem zu verwenden, um einen I2P-Benutzer zu geolokalisieren.
-  Es ist unmöglich, das Shared Identity-Problem zu verwenden, um I2P-Sitzungen zu verlinken, wenn sie nicht zeitgleich sind.

Es ist jedoch möglich, die Anonymität eines I2P-Benutzers in Umständen zu verschlechtern, die wahrscheinlich sehr häufig auftreten. Ein Grund, warum sie häufig sind, ist, dass wir die Verwendung von Firefox empfehlen, einem Webbrowser, der den „Tabbed“-Betrieb unterstützt.

-  Es ist *immer* möglich, einen Fingerabdruck aus dem Shared Identity-Problem in *jedem* Webbrowser zu erzeugen, der das Anfordern von Drittanbieter-Ressourcen unterstützt.
-  Das Deaktivieren von Javascript erreicht **nichts** gegen das Shared Identity-Problem.
-  Wenn ein Link zwischen nicht-zeitgleichen Sitzungen wie durch „traditionelles“ Browser-Fingerprinting hergestellt werden kann, kann die Shared Identity transitiv angewendet werden, was möglicherweise eine nicht-zeitgleiche Verlinkungsstrategie ermöglicht.
-  Wenn ein Link zwischen einer Aktivität im Klartext und einer I2P-Identität hergestellt werden kann, beispielsweise wenn das Ziel auf einer Seite sowohl mit einer I2P- als auch einer Klartext-Präsenz auf beiden Seiten eingeloggt ist, kann die Shared Identity transitiv angewendet werden, was möglicherweise eine vollständige Deanonymisierung ermöglicht.

Wie Sie die Schwere des Shared Identity-Problems bewerten, hängt davon ab, wo Sie (oder genauer gesagt, ein „Benutzer“ mit möglicherweise uninformierten Erwartungen) denken, dass die „kontextuelle Identität“ für die Anwendung liegt. Es gibt mehrere Möglichkeiten:

1. HTTP ist sowohl die Anwendung als auch die kontextuelle Identität - So funktioniert es jetzt. Alle HTTP-Anwendungen teilen eine Identität.
2. Der Prozess ist die Anwendung und die kontextuelle Identität - So funktioniert es, wenn eine Anwendung eine API wie SAMv3 oder I2CP verwendet, bei der eine Anwendung ihre Identität erstellt und ihre Lebensdauer steuert.
3. HTTP ist die Anwendung, aber der Host ist die kontextuelle Identität - Dies ist das Ziel dieses Vorschlags, bei dem jeder Host als potenzielle „Webanwendung“ behandelt wird und die Bedrohungsoberfläche entsprechend behandelt wird.

Ist es lösbar?
^^^^^^^^^^^^^^^

Es ist wahrscheinlich nicht möglich, einen Proxy zu erstellen, der intelligent auf jeden möglichen Fall reagiert, in dem sein Betrieb die Anonymität einer Anwendung schwächen könnte. Es ist jedoch möglich, einen Proxy zu erstellen, der intelligent auf eine spezifische Anwendung reagiert, die sich auf vorhersehbare Weise verhält. Beispielsweise wird in modernen Webbrowsern erwartet, dass Benutzer mehrere Tabs geöffnet haben, in denen sie mit mehreren Websites interagieren, die durch Hostnamen unterschieden werden.

Dies ermöglicht es uns, das Verhalten des HTTP-Proxys für diesen Typ von HTTP-Benutzeragenten zu verbessern, indem das Verhalten des Proxys dem Verhalten des Benutzeragenten entspricht, indem jeder Host bei Verwendung mit dem HTTP-Proxy seine eigene Destination erhält. Diese Änderung macht es unmöglich, das Shared Identity-Problem zur Ableitung eines Fingerprints zu verwenden, der zur Korrelation der Client-Aktivität mit 2 Hosts verwendet werden kann, da die 2 Hosts einfach keine Rückkehridentität mehr teilen.

Beschreibung:
^^^^^^^^^^^^

Ein neuer HTTP-Proxy wird erstellt und dem Hidden Services Manager (I2PTunnel) hinzugefügt. Der neue HTTP-Proxy wird als „Multiplexer“ von I2PSocketManagern fungieren. Der Multiplexer selbst hat keine Destination. Jeder einzelne I2PSocketManager, der Teil des Multiplex wird, hat seine eigene lokale Destination und seinen eigenen Tunnelpool. I2PSocketManager werden bei Bedarf vom Multiplexer erstellt, wobei die „Nachfrage“ der erste Besuch des neuen Hosts ist. Es ist möglich, die Erstellung der I2PSocketManagers vor dem Einfügen in den Multiplexer zu optimieren, indem man einen oder mehrere im Voraus erstellt und sie außerhalb des Multiplexers speichert. Dies kann die Leistung verbessern.

Ein zusätzlicher I2PSocketManager mit eigener Destination wird als Träger eines „Outproxy“ für jede Site eingerichtet, die keine I2P-Destination hat, beispielsweise jede Clearnet-Site. Dies macht effektiv die gesamte Nutzung von Outproxy zu einer einzigen kontextuellen Identität, mit dem Vorbehalt, dass die Konfiguration mehrerer Outproxies für den Tunnel die normale „Sticky“ Outproxy-Rotation verursacht, bei der jeder Outproxy nur Anforderungen für eine einzelne Site erhält. Dies ist *fast* das äquivalente Verhalten wie die Isolierung von HTTP-über-I2P-Proxys nach Destination im klaren Internet.

Ressourcenanforderungen:
''''''''''''''''''''''''

Der neue HTTP-Proxy erfordert zusätzliche Ressourcen im Vergleich zum bestehenden HTTP-Proxy. Er wird:

-  Potenziell mehr Tunnel und I2PSocketManager erstellen
-  Tunnel häufiger erstellen

Jeder dieser Punkte erfordert:

-  Lokale Rechenressourcen
-  Netzwerkressourcen von Peers

Einstellungen:
'''''''''

Um die Auswirkungen der erhöhten Ressourcennutzung zu minimieren, sollte der Proxy so konfiguriert werden, dass er möglichst wenig benötigt. Proxies, die Teil des Multiplexers sind (nicht der Hauptproxy), sollten so konfiguriert werden:

-  Multiplexed I2PSocketManager bauen 1 Tunnel ein, 1 Tunnel aus in ihren Tunnelpools
-  Multiplexed I2PSocketManager nehmen standardmäßig 3 Hops
-  Schließen von Sockets nach 10 Minuten Inaktivität
-  I2PSocketManager, die vom Multiplexer gestartet werden, teilen die Lebensdauer des Multiplexers. Multiplexed Tunnels werden nicht „zerstört“, bis der übergeordnete Multiplexer dies tut.

Diagramme:
^^^^^^^^^

Das untenstehende Diagramm stellt den aktuellen Betrieb des HTTP-Proxys dar, was der „Möglichkeit 1.“ unter dem Abschnitt „Ist es ein Problem“ entspricht. Wie Sie sehen können, interagiert der HTTP-Proxy direkt mit I2P-Sites, indem er nur eine Destination verwendet. In diesem Szenario ist HTTP sowohl die Anwendung als auch die kontextuelle Identität.

```text
**Aktuelle Situation: HTTP ist die Anwendung, HTTP ist die Kontextuelle Identität**
                                                          __-> Outproxy <-> i2pgit.org
                                                         /
   Browser <-> HTTP Proxy(eine Destination)<->I2PSocketManager <---> idk.i2p
                                                         \__-> translate.idk.i2p
                                                          \__-> git.idk.i2p
```

Das untenstehende Diagramm stellt den Betrieb eines host-bewussten HTTP-Proxys dar, was der „Möglichkeit 3.“ unter dem Abschnitt „Ist es ein Problem“ entspricht. In diesem Szenario ist HTTP die Anwendung, aber der Host definiert die kontextuelle Identität, wobei jede I2P-Site mit einem anderen HTTP-Proxy mit einer einzigartigen Destination pro Host interagiert. Dies verhindert, dass Betreiber mehrerer Sites feststellen können, wann dieselbe Person mehrere von ihnen betriebene Sites besucht.

```text
**Nach der Änderung: HTTP ist die Anwendung, Host ist die Kontextuelle Identität**
                                                        __-> I2PSocketManager(Destination A - Nur Outproxies) <--> i2pgit.org
                                                       /
   Browser <-> HTTP Proxy Multiplexer(Keine Destination) <---> I2PSocketManager(Destination B) <--> idk.i2p
                                                       \__-> I2PSocketManager(Destination C) <--> translate.idk.i2p
                                                        \__-> I2PSocketManager(Destination C) <--> git.idk.i2p
```

Status:
^^^^^^^

Eine funktionierende Java-Implementierung des host-bewussten Proxys, die mit einer älteren Version dieses Vorschlags übereinstimmt, ist unter idks Fork auf dem Branch verfügbar: i2p.i2p.2.6.0-browser-proxy-post-keepalive Link in Zitationen. Sie befindet sich in intensiver Überarbeitung, um die Änderungen in kleinere Abschnitte zu unterteilen.

Implementierungen mit unterschiedlichen Fähigkeiten wurden in Go unter Verwendung der SAMv3-Bibliothek geschrieben, sie könnten nützlich zum Einbetten in andere Go-Anwendungen oder für go-i2p sein, sind aber für Java I2P ungeeignet. Darüber hinaus fehlt ihnen eine gute Unterstützung für die interaktive Arbeit mit verschlüsselten LeaseSets.

Nachtrag: ``i2psocks``
                      

Einfaches Anwendungsorientiertes Isolieren anderer Arten von Clients ist möglich, ohne einen neuen Tunneltyp zu implementieren oder den vorhandenen I2P-Code zu ändern, indem bestehende I2PTunnel-Tools kombiniert werden, die bereits in der Datenschutzgemeinschaft weit verbreitet und getestet sind. Diese Methode setzt jedoch eine Annahme voraus, die weder für HTTP noch für viele andere potenzielle I2P-Clients zutrifft.

Vereinfacht erzeugt das folgende Skript einen anwendungsbewussten SOCKS5-Proxy und "socksified" den darunterliegenden Befehl:

```sh
#! /bin/sh
command_to_proxy="$@"
java -jar ~/i2p/lib/i2ptunnel.jar -wait -e 'sockstunnel 7695'
torsocks --port 7695 $command_to_proxy
```

Nachtrag: ``Beispielimplementierung des Angriffs``
                                                  

[Eine Beispielimplementierung des Shared Identity-Angriffs auf HTTP
Benutzeragenten](https://github.com/eyedeekay/colluding_sites_attack/)
existiert seit mehreren Jahren. Ein weiteres Beispiel ist im
``simple-colluder`` Unterverzeichnis von [idks prop166
Repository](https://git.idk.i2p/idk/i2p.host-aware-proxy) verfügbar. Diese
Beispiele sind absichtlich so gestaltet, dass sie demonstrieren, dass der Angriff funktioniert, und würden Änderungen (wenn auch kleinere) erfordern, um in einen echten Angriff verwandelt zu werden.

