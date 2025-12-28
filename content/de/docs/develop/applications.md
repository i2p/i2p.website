---
title: "Anwendungsentwicklung"
description: "Warum I2P-spezifische Apps schreiben, Schlüsselkonzepte, Entwicklungsoptionen und ein einfacher Einstiegsleitfaden"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Warum I2P-spezifischen Code schreiben?

Es gibt mehrere Möglichkeiten, Anwendungen in I2P zu nutzen. Mit [I2PTunnel](/docs/api/i2ptunnel/) können Sie reguläre Anwendungen verwenden, ohne explizite I2P-Unterstützung programmieren zu müssen. Dies ist sehr effektiv für Client-Server-Szenarien, in denen Sie sich mit einer einzelnen Website verbinden müssen. Sie können einfach einen Tunnel mit I2PTunnel erstellen, um sich mit dieser Website zu verbinden, wie in Abbildung 1 dargestellt.

Wenn Ihre Anwendung verteilt ist, benötigt sie Verbindungen zu einer großen Anzahl von Peers. Mit I2PTunnel müssen Sie für jeden Peer, mit dem Sie Kontakt aufnehmen möchten, einen neuen Tunnel erstellen, wie in Abbildung 2 dargestellt. Dieser Prozess kann natürlich automatisiert werden, aber das Ausführen vieler I2PTunnel-Instanzen erzeugt einen erheblichen Overhead. Darüber hinaus müssen Sie bei vielen Protokollen alle Teilnehmer dazu zwingen, denselben Satz von Ports für alle Peers zu verwenden – z.B. wenn Sie zuverlässig DCC-Chat ausführen möchten, müssen sich alle darauf einigen, dass Port 10001 Alice ist, Port 10002 Bob ist, Port 10003 Charlie ist und so weiter, da das Protokoll TCP/IP-spezifische Informationen (Host und Port) enthält.

Allgemeine Netzwerkanwendungen senden oft viele zusätzliche Daten, die zur Identifizierung von Benutzern verwendet werden könnten. Hostnamen, Portnummern, Zeitzonen, Zeichensätze usw. werden oft ohne Information des Benutzers gesendet. Daher kann die Gestaltung des Netzwerkprotokolls mit speziellem Fokus auf Anonymität vermeiden, dass Benutzeridentitäten kompromittiert werden.

Es gibt auch Effizienzaspekte zu berücksichtigen, wenn man festlegt, wie man auf I2P interagiert. Die Streaming-Bibliothek und darauf aufbauende Komponenten arbeiten mit Handshakes ähnlich wie TCP, während die Kern-I2P-Protokolle (I2NP und I2CP) strikt nachrichtenbasiert sind (wie UDP oder in manchen Fällen rohes IP). Der wichtige Unterschied besteht darin, dass bei I2P die Kommunikation über ein Long-Fat-Network (Netzwerk mit hoher Bandbreite und hoher Latenz) erfolgt — jede Ende-zu-Ende-Nachricht weist erhebliche Latenzen auf, kann jedoch Nutzdaten von bis zu mehreren KB enthalten. Eine Anwendung, die eine einfache Anfrage und Antwort benötigt, kann jeglichen Zustand eliminieren und die durch Aufbau- und Abbau-Handshakes verursachte Latenz reduzieren, indem sie (Best-Effort-)Datagramme verwendet, ohne sich um MTU-Erkennung oder Fragmentierung von Nachrichten kümmern zu müssen.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
Zusammenfassend gibt es mehrere Gründe, I2P-spezifischen Code zu schreiben:

- Das Erstellen einer großen Anzahl von I2PTunnel-Instanzen verbraucht eine nicht unerhebliche Menge an Ressourcen, was für verteilte Anwendungen problematisch ist (für jeden Peer wird ein neuer tunnel benötigt).
- Allgemeine Netzwerkprotokolle senden oft viele zusätzliche Daten, die zur Identifizierung von Benutzern verwendet werden können. Die spezifische Programmierung für I2P ermöglicht die Erstellung eines Netzwerkprotokolls, das solche Informationen nicht preisgibt und Benutzer anonym und sicher hält.
- Netzwerkprotokolle, die für die Verwendung im regulären Internet konzipiert sind, können auf I2P ineffizient sein, da es sich um ein Netzwerk mit deutlich höherer Latenz handelt.

I2P unterstützt eine Standard-[Plugins-Schnittstelle](/docs/plugins/) für Entwickler, damit Anwendungen einfach integriert und verteilt werden können.

In Java geschriebene Anwendungen, die über eine HTML-Schnittstelle mittels der Standard-webapps/app.war zugänglich/ausführbar sind, können für die Aufnahme in die I2P-Distribution in Betracht gezogen werden.

## Wichtige Konzepte

Es gibt einige Änderungen, an die man sich bei der Verwendung von I2P gewöhnen muss:

### Ziele

Eine Anwendung, die auf I2P läuft, sendet Nachrichten von und empfängt Nachrichten an einem eindeutigen kryptographisch sicheren Endpunkt – einer „destination". In TCP- oder UDP-Begriffen könnte eine destination (weitgehend) als Äquivalent eines Hostname-Port-Nummer-Paars betrachtet werden, obwohl es einige Unterschiede gibt.

- Ein I2P-Destination ist selbst ein kryptografisches Konstrukt — alle an ein Destination gesendeten Daten werden verschlüsselt, als ob es eine universelle Bereitstellung von IPsec gäbe, wobei der (anonymisierte) Standort des Endpunkts signiert wird, als ob es eine universelle Bereitstellung von DNSSEC gäbe.
- I2P-Destinations sind mobile Identifikatoren — sie können von einem I2P-Router zu einem anderen verschoben werden (oder sogar „Multihoming" betreiben — gleichzeitig auf mehreren Routern operieren). Dies unterscheidet sich deutlich von der TCP- oder UDP-Welt, wo ein einzelner Endpunkt (Port) auf einem einzigen Host bleiben muss.
- I2P-Destinations sind unhandlich und groß — im Hintergrund enthalten sie einen 2048-Bit-ElGamal-Public-Key für die Verschlüsselung, einen 1024-Bit-DSA-Public-Key für die Signierung und ein Zertifikat variabler Größe, das einen Proof-of-Work oder verblindete Daten enthalten kann.

Es gibt bestehende Möglichkeiten, diese langen und unhandlichen Zieladressen durch kurze und einprägsame Namen zu bezeichnen (z.B. "irc.duck.i2p"), aber diese Techniken garantieren keine globale Eindeutigkeit (da sie lokal in einer Datenbank auf dem Rechner jeder Person gespeichert werden) und der aktuelle Mechanismus ist nicht besonders skalierbar oder sicher (Aktualisierungen der Hostliste werden über "Abonnements" von Namensdiensten verwaltet). Möglicherweise wird es eines Tages ein sicheres, menschenlesbares, skalierbares und global eindeutiges Benennungssystem geben, aber Anwendungen sollten sich nicht darauf verlassen, dass es vorhanden ist. [Weitere Informationen zum Benennungssystem](/docs/overview/naming/) sind verfügbar.

Während die meisten Anwendungen nicht zwischen Protokollen und Ports unterscheiden müssen, unterstützt I2P diese *durchaus*. Komplexe Anwendungen können ein Protokoll, einen Quell-Port und einen Ziel-Port pro Nachricht angeben, um den Datenverkehr auf einem einzelnen Destination zu multiplexen. Details finden Sie auf der [Datagram-Seite](/docs/api/datagrams/). Einfache Anwendungen funktionieren, indem sie auf „alle Protokolle" und „alle Ports" eines Destination lauschen.

### Anonymität und Vertraulichkeit

I2P bietet transparente Ende-zu-Ende-Verschlüsselung und Authentifizierung für alle Daten, die über das Netzwerk übertragen werden — wenn Bob an Alices destination sendet, kann nur Alices destination die Daten empfangen, und wenn Bob die Datagramm- oder Streaming-Bibliothek verwendet, weiß Alice mit Sicherheit, dass Bobs destination derjenige ist, der die Daten gesendet hat.

Natürlich anonymisiert I2P transparent die Daten, die zwischen Alice und Bob gesendet werden, aber es tut nichts, um den Inhalt dessen zu anonymisieren, was sie senden. Wenn Alice beispielsweise Bob ein Formular mit ihrem vollständigen Namen, Ausweisdokumenten und Kreditkartennummern sendet, kann I2P nichts dagegen tun. Daher sollten Protokolle und Anwendungen im Hinterkopf behalten, welche Informationen sie schützen möchten und welche Informationen sie bereit sind preiszugeben.

### I2P-Datagramme können bis zu mehrere KB groß sein

Anwendungen, die I2P-Datagramme verwenden (entweder raw oder repliable), können im Wesentlichen im Sinne von UDP betrachtet werden – die Datagramme sind ungeordnet, best effort und verbindungslos – aber im Gegensatz zu UDP müssen sich Anwendungen nicht um MTU-Erkennung kümmern und können einfach große Datagramme versenden. Während die Obergrenze nominell 32 KB beträgt, wird die Nachricht für den Transport fragmentiert, was die Zuverlässigkeit des Ganzen verringert. Datagramme über etwa 10 KB werden derzeit nicht empfohlen. Siehe die [Datagramm-Seite](/docs/api/datagrams/) für Details. Für viele Anwendungen sind 10 KB Daten ausreichend für eine vollständige Anfrage oder Antwort, was es ihnen ermöglicht, transparent in I2P als UDP-ähnliche Anwendung zu operieren, ohne Fragmentierung, erneutes Senden usw. implementieren zu müssen.

## Entwicklungsoptionen

Es gibt verschiedene Möglichkeiten, Daten über I2P zu übertragen, jede mit ihren eigenen Vor- und Nachteilen. Die Streaming-Bibliothek ist die empfohlene Schnittstelle und wird von der Mehrheit der I2P-Anwendungen verwendet.

### Streaming-Bibliothek

Die [vollständige Streaming-Bibliothek](/docs/specs/streaming/) ist nun die Standardschnittstelle. Sie ermöglicht die Programmierung mit TCP-ähnlichen Sockets, wie im [Streaming-Entwicklungsleitfaden](#developing-with-the-streaming-library) erklärt.

### BOB

BOB ist die [Basic Open Bridge](/docs/legacy/bob/), die es einer Anwendung in jeder Sprache ermöglicht, Streaming-Verbindungen zu und von I2P herzustellen. Zum jetzigen Zeitpunkt fehlt die UDP-Unterstützung, aber UDP-Unterstützung ist für die nahe Zukunft geplant. BOB enthält auch mehrere Werkzeuge, wie z.B. die Generierung von Zielschlüsseln und die Überprüfung, ob eine Adresse den I2P-Spezifikationen entspricht. Aktuelle Informationen und Anwendungen, die BOB verwenden, finden Sie auf dieser [I2P-Website](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM wird nicht empfohlen. SAM V2 ist in Ordnung, SAM V3 wird empfohlen.*

SAM ist das [Simple Anonymous Messaging](/docs/legacy/sam/) Protokoll, das es einer Anwendung, die in einer beliebigen Sprache geschrieben wurde, ermöglicht, über einen einfachen TCP-Socket mit einer SAM-Bridge zu kommunizieren und diese Bridge den gesamten I2P-Verkehr multiplexen zu lassen, wobei die Verschlüsselung/Entschlüsselung und ereignisbasierte Verarbeitung transparent koordiniert werden. SAM unterstützt drei Betriebsarten:

- Streams, wenn Alice und Bob Daten zuverlässig und in der richtigen Reihenfolge aneinander senden möchten
- Beantwortbare Datagramme, wenn Alice Bob eine Nachricht senden möchte, auf die Bob antworten kann
- Raw-Datagramme, wenn Alice die maximal mögliche Bandbreite und Leistung herausholen möchte und Bob es nicht interessiert, ob der Absender der Daten authentifiziert ist oder nicht (z. B. wenn die übertragenen Daten selbstauthentifizierend sind)

SAMv3 verfolgt das gleiche Ziel wie SAM und SAM V2, erfordert jedoch kein Multiplexing/Demultiplexing. Jeder I2P-Stream wird durch seinen eigenen Socket zwischen der Anwendung und der SAM-Bridge verwaltet. Außerdem können Datagramme von der Anwendung durch Datagramm-Kommunikation mit der SAM-Bridge gesendet und empfangen werden.

[SAM V2](/docs/legacy/samv2/) ist eine neue Version, die von imule verwendet wird und einige der Probleme in [SAM](/docs/legacy/sam/) behebt.

[SAM V3](/docs/api/samv3/) wird von imule seit Version 1.4.0 verwendet.

### I2PTunnel

Die I2PTunnel-Anwendung ermöglicht es Anwendungen, spezifische TCP-ähnliche Tunnel zu Peers aufzubauen, indem entweder I2PTunnel-'Client'-Anwendungen erstellt werden (die auf einem bestimmten Port lauschen und sich mit einem bestimmten I2P-destination verbinden, sobald ein Socket zu diesem Port geöffnet wird) oder I2PTunnel-'Server'-Anwendungen (die auf einem bestimmten I2P-destination lauschen und bei jeder neuen I2P-Verbindung einen Outproxy zu einem bestimmten TCP-Host/Port herstellen). Diese Streams sind 8-Bit-sauber und werden durch dieselbe Streaming-Bibliothek authentifiziert und gesichert, die auch SAM verwendet, aber es gibt einen nicht trivialen Overhead bei der Erstellung mehrerer eindeutiger I2PTunnel-Instanzen, da jede ihre eigene eindeutige I2P-destination und ihre eigenen Tunnel, Schlüssel usw. hat.

### SOCKS

I2P unterstützt einen SOCKS V4 und V5 Proxy. Ausgehende Verbindungen funktionieren gut. Eingehende (Server-) und UDP-Funktionalität können unvollständig und ungetestet sein.

### Ministreaming

*Entfernt*

Es gab früher eine einfache "ministreaming"-Bibliothek, aber jetzt enthält ministreaming.jar nur noch die Schnittstellen für die vollständige Streaming-Bibliothek.

### Datagramme

*Empfohlen für UDP-ähnliche Anwendungen*

Die [Datagram-Bibliothek](/docs/api/datagrams/) ermöglicht das Senden von UDP-ähnlichen Paketen. Es ist möglich zu verwenden:

- Beantwortbare Datagramme
- Roh-Datagramme

### I2CP

*Nicht empfohlen*

[I2CP](/docs/specs/i2cp/) selbst ist ein sprachunabhängiges Protokoll, aber um eine I2CP-Bibliothek in einer anderen Sprache als Java zu implementieren, muss eine beträchtliche Menge an Code geschrieben werden (Verschlüsselungsroutinen, Objekt-Marshalling, asynchrone Nachrichtenverarbeitung usw.). Während jemand eine I2CP-Bibliothek in C oder einer anderen Sprache schreiben könnte, wäre es höchstwahrscheinlich nützlicher, stattdessen die C SAM-Bibliothek zu verwenden.

### Webanwendungen

I2P wird mit dem Jetty-Webserver geliefert, und die Konfiguration zur Verwendung des Apache-Servers ist stattdessen unkompliziert. Jede standardmäßige Webanwendungstechnologie sollte funktionieren.

## Beginnen Sie mit der Entwicklung – Eine einfache Anleitung

Die Entwicklung mit I2P erfordert eine funktionierende I2P-Installation und eine Entwicklungsumgebung Ihrer Wahl. Wenn Sie Java verwenden, können Sie die Entwicklung mit der [streaming library](#developing-with-the-streaming-library) oder der datagram library beginnen. Bei Verwendung einer anderen Programmiersprache können SAM oder BOB verwendet werden.

### Entwicklung mit der Streaming-Bibliothek

Unten finden Sie eine überarbeitete und modernisierte Version des Beispiels von der ursprünglichen Seite. Für das vollständige Beispiel siehe die Legacy-Seite oder unsere Java-Beispiele in der Codebasis.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Codebeispiel: einfacher Server, der Daten empfängt.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Codebeispiel: Client verbindet sich und sendet eine Zeile.*
