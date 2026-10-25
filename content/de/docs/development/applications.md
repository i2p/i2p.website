---
title: "Anwendungsentwicklung"
description: "Warum I2P-spezifische Apps schreiben, Schlüsselkonzepte, Entwicklungsoptionen und ein Leitfaden für den Einstieg"
slug: "applications"
aliases:
  - "/de/docs/develop/applications"
  - "/de/docs/develop/applications/"
  - "/de/applications"
  - "/de/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Warum I2P-spezifischen Code schreiben?

Es gibt mehrere Möglichkeiten, Anwendungen in I2P zu nutzen. Mit [I2PTunnel](/docs/api/i2ptunnel/) können Sie reguläre Anwendungen verwenden, ohne explizite I2P-Unterstützung programmieren zu müssen. Dies ist sehr effektiv für Client-Server-Szenarien, in denen Sie sich mit einer einzelnen Website verbinden müssen. Sie können einfach einen tunnel mit I2PTunnel erstellen, um sich mit dieser Website zu verbinden, wie in Abbildung 1 gezeigt.

Wenn Ihre Anwendung verteilt ist, benötigt sie Verbindungen zu einer großen Anzahl von Peers. Bei Verwendung von I2PTunnel müssen Sie einen neuen tunnel für jeden Peer erstellen, den Sie kontaktieren möchten, wie in Abbildung 2 gezeigt. Dieser Prozess kann natürlich automatisiert werden, aber das Ausführen vieler I2PTunnel-Instanzen erzeugt einen großen Overhead. Darüber hinaus müssen Sie bei vielen Protokollen alle dazu zwingen, dieselben Ports für alle Peers zu verwenden — z.B. wenn Sie zuverlässig DCC-Chat ausführen möchten, müssen alle zustimmen, dass Port 10001 Alice ist, Port 10002 Bob ist, Port 10003 Charlie ist, und so weiter, da das Protokoll TCP/IP-spezifische Informationen (Host und Port) enthält.

Allgemeine Netzwerkanwendungen senden oft viele zusätzliche Daten, die zur Identifizierung von Benutzern verwendet werden könnten. Hostnamen, Portnummern, Zeitzonen, Zeichensätze usw. werden oft gesendet, ohne den Benutzer zu informieren. Daher kann das spezielle Design des Netzwerkprotokolls mit Blick auf Anonymität die Kompromittierung der Benutzeridentitäten vermeiden.

Es gibt auch Effizienzaspekte zu berücksichtigen, wenn man bestimmt, wie man über I2P interagiert. Die Streaming-Bibliothek und darauf aufbauende Anwendungen arbeiten mit Handshakes ähnlich wie TCP, während die zentralen I2P-Protokolle (I2NP und I2CP) strikt nachrichtenbasiert sind (wie UDP oder in manchen Fällen rohes IP). Der wichtige Unterschied ist, dass bei I2P die Kommunikation über ein langes, fettes Netzwerk läuft — jede Ende-zu-Ende-Nachricht wird nicht unerhebliche Latenzen haben, kann aber Nutzdaten von bis zu mehreren KB enthalten. Eine Anwendung, die nur eine einfache Anfrage und Antwort benötigt, kann jeglichen Zustand loswerden und die Latenz vermeiden, die durch die Startup- und Teardown-Handshakes entsteht, indem sie (best effort) Datagramme verwendet, ohne sich über MTU-Erkennung oder Fragmentierung von Nachrichten Gedanken machen zu müssen.

![Das Erstellen einer Server-Client-Verbindung mit I2PTunnel erfordert nur die Erstellung eines einzigen Tunnels.](/images/i2ptunnel_serverclient.png)

*Abbildung 1: Die Erstellung einer Server-Client-Verbindung mit I2PTunnel erfordert nur die Erstellung eines einzigen Tunnels.*

![Die Einrichtung von Verbindungen für Peer-to-Peer-Anwendungen erfordert eine sehr große Anzahl von tunnels.](/images/i2ptunnel_peertopeer.png)

*Abbildung 2: Das Einrichten von Verbindungen für Peer-to-Peer-Anwendungen erfordert eine sehr große Anzahl von tunnels.*

Zusammenfassend gibt es eine Reihe von Gründen, I2P-spezifischen Code zu schreiben:

- Das Erstellen einer großen Anzahl von I2PTunnel-Instanzen verbraucht eine nicht unerhebliche Menge an Ressourcen, was für verteilte Anwendungen problematisch ist (für jeden Peer wird ein neuer tunnel benötigt).
- Allgemeine Netzwerkprotokolle senden oft viele zusätzliche Daten, die zur Identifizierung von Benutzern verwendet werden können. Die spezielle Programmierung für I2P ermöglicht die Erstellung eines Netzwerkprotokolls, das solche Informationen nicht preisgibt und die Benutzer anonym und sicher hält.
- Netzwerkprotokolle, die für die Nutzung im normalen Internet entwickelt wurden, können auf I2P ineffizient sein, da es sich um ein Netzwerk mit viel höherer Latenz handelt.

I2P unterstützt eine Standard-[Plugin-Schnittstelle](/docs/specs/plugin/) für Entwickler, damit Anwendungen einfach integriert und verteilt werden können.

In Java geschriebene Anwendungen, die über eine HTML-Schnittstelle mittels der Standard-webapps/app.war zugänglich/ausführbar sind, können für die Aufnahme in die I2P-Distribution in Betracht gezogen werden.

---

## Wichtige Konzepte

Es gibt einige Änderungen, an die man sich gewöhnen muss, wenn man I2P verwendet:

### Destination ~= Host+Port

Eine auf I2P laufende Anwendung sendet Nachrichten von einem einzigartigen kryptographisch sicheren Endpunkt und empfängt Nachrichten an diesen — ein "destination". In TCP- oder UDP-Begriffen könnte ein destination (weitgehend) als Äquivalent zu einem Hostnamen plus Port-Nummer-Paar betrachtet werden, obwohl es einige Unterschiede gibt.

- Eine I2P destination ist selbst ein kryptographisches Konstrukt — alle an sie gesendeten Daten werden verschlüsselt, als gäbe es eine universelle Bereitstellung von IPsec mit dem (anonymisierten) Standort des Endpunkts signiert, als gäbe es eine universelle Bereitstellung von DNSSEC.
- I2P destinations sind mobile Identifikatoren — sie können von einem I2P router zu einem anderen verschoben werden (oder sogar „multihome" — gleichzeitig auf mehreren routern betrieben werden). Dies unterscheidet sich deutlich von der TCP- oder UDP-Welt, wo ein einzelner Endpunkt (Port) auf einem einzelnen Host bleiben muss.
- I2P destinations sind unschön und groß — im Hintergrund enthalten sie einen 2048-Bit-ElGamal-Public-Key für die Verschlüsselung, einen 1024-Bit-DSA-Public-Key für die Signierung und ein Zertifikat variabler Größe, das einen Arbeitsnachweis oder verblindete Daten enthalten kann.

Es gibt bereits Methoden, um diese langen und unschönen Ziele mit kurzen und schönen Namen zu bezeichnen (z.B. "irc.duck.i2p"), aber diese Techniken garantieren keine globale Eindeutigkeit (da sie lokal in einer Datenbank auf jedem Computer gespeichert werden) und der aktuelle Mechanismus ist nicht besonders skalierbar oder sicher (Updates der Hostliste werden über "Abonnements" von Naming-Diensten verwaltet). Möglicherweise wird es eines Tages ein sicheres, menschenlesbares, skalierbares und global eindeutiges Naming-System geben, aber Anwendungen sollten nicht darauf angewiesen sein, dass es vorhanden ist, da es Leute gibt, die nicht glauben, dass so etwas möglich ist. [Weitere Informationen zum Naming-System](/docs/overview/naming/) sind verfügbar.

Während die meisten Anwendungen nicht zwischen Protokollen und Ports unterscheiden müssen, *unterstützt* I2P diese durchaus. Komplexe Anwendungen können ein Protokoll, einen Ursprungsport und einen Zielport pro Nachricht angeben, um den Verkehr auf einem einzigen Ziel zu multiplexen. Siehe die [datagram page](/docs/api/datagrams/) für Details. Einfache Anwendungen arbeiten, indem sie auf "alle Protokolle" an "allen Ports" eines Ziels lauschen.

### Anonymität und Vertraulichkeit

I2P verfügt über transparente Ende-zu-Ende-Verschlüsselung und Authentifizierung für alle über das Netzwerk übertragenen Daten — wenn Bob an Alices destination sendet, kann nur Alices destination die Daten empfangen, und wenn Bob die Datagramm- oder Streaming-Bibliothek verwendet, weiß Alice mit Sicherheit, dass Bobs destination derjenige ist, der die Daten gesendet hat.

Natürlich anonymisiert I2P transparent die zwischen Alice und Bob gesendeten Daten, aber es kann nichts tun, um den Inhalt dessen zu anonymisieren, was sie senden. Wenn Alice beispielsweise Bob ein Formular mit ihrem vollständigen Namen, Personalausweisen und Kreditkartennummern sendet, kann I2P nichts dagegen tun. Daher sollten Protokolle und Anwendungen berücksichtigen, welche Informationen sie zu schützen versuchen und welche Informationen sie preisgeben möchten.

### I2P-Datagramme können bis zu mehrere KB groß sein

Anwendungen, die I2P-Datagramme verwenden (entweder rohe oder beantwortbare), können im Wesentlichen in Bezug auf UDP betrachtet werden — die Datagramme sind ungeordnet, best-effort und verbindungslos — aber im Gegensatz zu UDP müssen sich Anwendungen keine Gedanken über MTU-Erkennung machen und können einfach große Datagramme abfeuern. Während die Obergrenze nominell 32 KB beträgt, wird die Nachricht für den Transport fragmentiert, was die Zuverlässigkeit des Ganzen verringert. Datagramme über etwa 10 KB werden derzeit nicht empfohlen. Siehe die [Datagramm-Seite](/docs/api/datagrams/) für Details. Für viele Anwendungen sind 10 KB Daten ausreichend für eine gesamte Anfrage oder Antwort, was es ihnen ermöglicht, transparent in I2P als UDP-ähnliche Anwendung zu funktionieren, ohne Fragmentierung, Wiederholungen usw. schreiben zu müssen.

---

## Entwicklungsoptionen

Es gibt verschiedene Möglichkeiten, Daten über I2P zu senden, jede mit ihren eigenen Vor- und Nachteilen. Die streaming lib ist die empfohlene Schnittstelle, die von der Mehrzahl der I2P-Anwendungen verwendet wird.

### Streaming Lib

Die [vollständige Streaming-Bibliothek](/docs/api/streaming/) ist nun die Standardschnittstelle. Sie ermöglicht die Programmierung mit TCP-ähnlichen Sockets, wie im [Streaming-Entwicklungsleitfaden](#developing-with-the-streaming-library) erklärt.

### BOB

BOB ist die [Basic Open Bridge](/docs/legacy/bob/), die es einer Anwendung in jeder Sprache ermöglicht, Streaming-Verbindungen zu und von I2P herzustellen. Zum jetzigen Zeitpunkt fehlt die UDP-Unterstützung, aber UDP-Unterstützung ist für die nahe Zukunft geplant. BOB enthält auch mehrere Tools, wie die Generierung von Zielschlüsseln und die Überprüfung, dass eine Adresse den I2P-Spezifikationen entspricht. Aktuelle Informationen und Anwendungen, die BOB verwenden, finden Sie auf dieser [I2P-Seite](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM wird nicht empfohlen. SAM V2 ist okay, SAM V3 wird empfohlen.*

SAM ist das [Simple Anonymous Messaging](/docs/legacy/sam/) Protokoll, das es einer in jeder Sprache geschriebenen Anwendung ermöglicht, über einen einfachen TCP-Socket mit einer SAM-Brücke zu kommunizieren und diese Brücke den gesamten I2P-Verkehr multiplexen zu lassen, wobei die Verschlüsselung/Entschlüsselung und ereignisbasierte Behandlung transparent koordiniert werden. SAM unterstützt drei Betriebsarten:

- Streams, für den Fall, dass Alice und Bob Daten zuverlässig und in der richtigen Reihenfolge aneinander senden möchten
- Beantwortbare Datagramme, für den Fall, dass Alice Bob eine Nachricht senden möchte, auf die Bob antworten kann
- Rohe Datagramme, für den Fall, dass Alice die maximale Bandbreite und Leistung herausholen möchte und Bob es nicht wichtig ist, ob der Absender der Daten authentifiziert ist oder nicht (z.B. wenn die übertragenen Daten selbstauthentifizierend sind)

SAM V3 verfolgt dasselbe Ziel wie SAM und SAM V2, erfordert jedoch kein Multiplexing/Demultiplexing. Jeder I2P-Stream wird durch seinen eigenen Socket zwischen der Anwendung und der SAM-Bridge verwaltet. Außerdem können Datagramme von der Anwendung durch Datagramm-Kommunikation mit der SAM-Bridge gesendet und empfangen werden.

[SAM V2](/docs/legacy/samv2/) ist eine neue Version, die von imule verwendet wird und einige der Probleme in [SAM](/docs/legacy/sam/) behebt.

[SAM V3](/docs/api/samv3/) wird von imule seit Version 1.4.0 verwendet.

### I2PTunnel

Die I2PTunnel-Anwendung ermöglicht es Anwendungen, spezifische TCP-ähnliche tunnel zu Peers zu erstellen, indem sie entweder I2PTunnel 'Client'-Anwendungen erstellt (die auf einem bestimmten Port lauschen und sich mit einem spezifischen I2P-Ziel verbinden, wann immer ein Socket zu diesem Port geöffnet wird) oder I2PTunnel 'Server'-Anwendungen (die auf ein spezifisches I2P-Ziel lauschen und bei jeder neuen I2P-Verbindung zu einem bestimmten TCP-Host/Port weiterleiten). Diese Datenströme sind 8-Bit-sauber und werden durch dieselbe Streaming-Bibliothek authentifiziert und gesichert, die auch SAM verwendet, aber es gibt einen nicht unerheblichen Overhead beim Erstellen mehrerer eindeutiger I2PTunnel-Instanzen, da jede ihr eigenes eindeutiges I2P-Ziel und ihren eigenen Satz von tunneln, Schlüsseln usw. hat.

### SOCKS

I2P unterstützt einen SOCKS V4 und V5 Proxy. Ausgehende Verbindungen funktionieren gut. Eingehende (Server) und UDP-Funktionalität ist möglicherweise unvollständig und ungetestet.

### Ministreaming

*Entfernt*

Früher gab es eine einfache "ministreaming"-Bibliothek, aber jetzt enthält ministreaming.jar nur noch die Schnittstellen für die vollständige Streaming-Bibliothek.

### Datagramme

*Empfohlen für UDP-ähnliche Anwendungen*

Die [Datagram library](/docs/api/datagrams/) ermöglicht das Senden von UDP-ähnlichen Paketen. Es ist möglich zu verwenden:

- Beantwortbare Datagramme
- Roh-Datagramme

### I2CP

*Nicht empfohlen*

[I2CP](/docs/specs/i2cp/) selbst ist ein sprachunabhängiges Protokoll, aber um eine I2CP-Bibliothek in etwas anderem als Java zu implementieren, muss eine erhebliche Menge Code geschrieben werden (Verschlüsselungsroutinen, Objekt-Marshalling, asynchrone Nachrichtenbehandlung, etc.). Während jemand eine I2CP-Bibliothek in C oder etwas anderem schreiben könnte, wäre es höchstwahrscheinlich nützlicher, stattdessen die C SAM-Bibliothek zu verwenden.

### Webanwendungen

I2P wird mit dem Jetty-Webserver geliefert, und die Konfiguration zur Verwendung des Apache-Servers ist stattdessen unkompliziert. Jede Standard-Webanwendungstechnologie sollte funktionieren.

---

## Mit der Entwicklung beginnen — Eine einfache Anleitung

Die Entwicklung mit I2P erfordert eine funktionierende I2P-Installation und eine Entwicklungsumgebung Ihrer Wahl. Wenn Sie Java verwenden, können Sie die Entwicklung mit der [streaming library](#developing-with-the-streaming-library) oder der Datagram-Bibliothek beginnen. Bei Verwendung einer anderen Programmiersprache können SAM oder BOB verwendet werden.

### Entwicklung mit der Streaming Library

Das folgende Beispiel zeigt, wie TCP-ähnliche Client- und Server-Anwendungen mit der Streaming-Bibliothek erstellt werden.

Dies erfordert die folgenden Bibliotheken in Ihrem Klassenpfad:

- `$I2P/lib/streaming.jar`: Die streaming-Bibliothek selbst
- `$I2P/lib/mstreaming.jar`: Factory und Schnittstellen für die streaming-Bibliothek
- `$I2P/lib/i2p.jar`: Standard-I2P-Klassen, Datenstrukturen, API und Hilfsprogramme

Sie können diese aus einer I2P-Installation beziehen oder die folgenden Abhängigkeiten von Maven Central hinzufügen:

- `net.i2p:i2p`
- `net.i2p.client:streaming`

Die Netzwerkkommunikation erfordert die Verwendung von I2P-Netzwerk-Sockets. Um dies zu demonstrieren, werden wir eine Anwendung erstellen, bei der ein Client Textnachrichten an einen Server senden kann, der die Nachrichten ausgibt und sie zurück an den Client sendet. Mit anderen Worten, der Server wird als Echo fungieren.

Wir beginnen mit der Initialisierung der Serveranwendung. Dies erfordert das Abrufen eines I2PSocketManager und das Erstellen eines I2PServerSocket. Wir werden der I2PSocketManagerFactory nicht die gespeicherten Schlüssel für eine bestehende Destination bereitstellen, sodass sie eine neue Destination für uns erstellt. Daher werden wir den I2PSocketManager nach einer I2PSession fragen, damit wir die erstellte Destination herausfinden können, da wir diese Informationen später kopieren und einfügen müssen, damit der Client sich mit uns verbinden kann.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*Code-Beispiel 1: Initialisierung der Server-Anwendung.*

Sobald wir einen I2PServerSocket haben, können wir I2PSocket-Instanzen erstellen, um Verbindungen von Clients zu akzeptieren. In diesem Beispiel erstellen wir eine einzelne I2PSocket-Instanz, die nur einen Client gleichzeitig verarbeiten kann. Ein echter Server müsste mehrere Clients verarbeiten können. Dazu müssten mehrere I2PSocket-Instanzen erstellt werden, jede in separaten Threads. Nachdem wir die I2PSocket-Instanz erstellt haben, lesen wir Daten, geben sie aus und senden sie an den Client zurück.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*Codebeispiel 2: Verbindungen von Clients annehmen und Nachrichten verarbeiten.*

Wenn Sie den obigen Server-Code ausführen, sollte er etwa folgendes ausgeben (aber ohne die Zeilenendezeichen, es sollte nur ein riesiger Block von Zeichen sein):

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Dies ist die Base64-Darstellung der Server-Destination. Der Client benötigt diese Zeichenkette, um den Server zu erreichen.

Jetzt werden wir die Client-Anwendung erstellen. Auch hier sind mehrere Schritte für die Initialisierung erforderlich. Wieder müssen wir damit beginnen, einen I2PSocketManager zu erhalten. Wir werden diesmal keine I2PSession und keinen I2PServerSocket verwenden. Stattdessen werden wir die Server-Destination-Zeichenkette verwenden, um unsere Verbindung zu starten. Wir werden den Benutzer nach der Destination-Zeichenkette fragen und einen I2PSocket mit dieser Zeichenkette erstellen. Sobald wir einen I2PSocket haben, können wir beginnen, Daten an den Server zu senden und von ihm zu empfangen.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*Codebeispiel 3: Starten des Clients und Verbinden mit der Serveranwendung.*

Schließlich können Sie sowohl die Server- als auch die Client-Anwendung ausführen. Starten Sie zuerst die Server-Anwendung. Sie wird eine Destination-Zeichenkette ausgeben (wie oben gezeigt). Starten Sie als nächstes die Client-Anwendung. Wenn sie nach einer Destination-Zeichenkette fragt, können Sie die vom Server ausgegebene Zeichenkette eingeben. Der Client wird dann 'Hello I2P!' (zusammen mit einem Zeilenwechsel) an den Server senden, der die Nachricht ausgibt und zurück an den Client sendet.

Herzlichen Glückwunsch, Sie haben erfolgreich über I2P kommuniziert!

---

## Bestehende Anwendungen

Kontaktieren Sie uns, wenn Sie einen Beitrag leisten möchten.

- [I2P-Bote](http://i2pbote.i2p/) - kontaktiere HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Siehe auch alle Plugins auf [plugins.i2p](http://plugins.i2p/), die Anwendungen und den Quellcode auf [echelon.i2p](http://echelon.i2p/) sowie den Anwendungscode auf [git.repo.i2p](http://git.repo.i2p/).

Siehe auch die mitgelieferten Anwendungen in der I2P-Distribution - SusiMail und I2PSnark.

---

## Anwendungsideen

- NNTP-Server - gab es in der Vergangenheit einige, momentan keinen
- Jabber-Server - gab es in der Vergangenheit einige, und es gibt momentan einen, mit Zugang zum öffentlichen Internet
- PGP-Schlüsselserver und/oder Proxy
- Content Distribution / DHT-Anwendungen - feedspace wiederbeleben, dijjer portieren, nach Alternativen suchen
- Bei der [Syndie](http://syndie.i2p2.de/)-Entwicklung helfen
- Webbasierte Anwendungen - Der Himmel ist die Grenze für das Hosting von webserver-basierten Anwendungen wie Blogs, Pastebins, Speicher, Tracking, Feeds, etc. Jede Web- oder CGI-Technologie wie Perl, PHP, Python oder Ruby funktioniert.
- Einige alte Apps wiederbeleben, mehrere waren früher im i2p-Quellpaket enthalten - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
