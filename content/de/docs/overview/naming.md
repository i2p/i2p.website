---
title: "Namensgebung und Adressbuch"
description: "Wie I2P menschenlesbare Hostnamen auf Ziele abbildet"
slug: "naming"
aliases:
  - "/de/docs/specs/naming"
  - "/de/docs/specs/naming/"
  - "/de/docs/naming"
  - "/de/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Übersicht

I2P wird mit einer generischen Namensgebungsbibliothek und einer Basis-Implementierung ausgeliefert, die dafür entwickelt wurde, mit einer lokalen Namen-zu-Ziel-Zuordnung zu arbeiten, sowie einer Add-on-Anwendung namens [Adressbuch](#address-book). I2P unterstützt auch [Base32-Hostnamen](#base32-names) ähnlich wie Tors .onion-Adressen.

Das Adressbuch ist ein web-of-trust-basiertes sicheres, verteiltes und menschenlesbares Namenssystem, das nur den Anspruch auf globale Eindeutigkeit aller menschenlesbaren Namen opfert, indem es nur lokale Eindeutigkeit vorschreibt. Während alle Nachrichten in I2P kryptographisch durch ihr Ziel adressiert werden, können verschiedene Personen lokale Adressbucheinträge für "Alice" haben, die auf unterschiedliche Ziele verweisen. Menschen können trotzdem neue Namen entdecken, indem sie veröffentlichte Adressbücher von Peers importieren, die in ihrem web of trust spezifiziert sind, durch das Hinzufügen von Einträgen, die von Dritten bereitgestellt werden, oder (falls einige Personen eine Reihe von veröffentlichten Adressbüchern mit einem First-Come-First-Serve-Registrierungssystem organisieren) können Menschen wählen, diese Adressbücher als Nameserver zu behandeln und damit traditionelles DNS zu emulieren.

HINWEIS: Für die Begründung hinter dem I2P-Benennungssystem, häufige Argumente dagegen und mögliche Alternativen siehe die Seite zur [Benennungsdiskussion](/docs/legacy/naming/).

---

## Komponenten des Benennungssystems

Es gibt keine zentrale Namensautorität in I2P. Alle Hostnamen sind lokal.

Das Benennungssystem ist recht einfach und der größte Teil davon ist in Anwendungen implementiert, die extern zum Router sind, aber mit der I2P-Distribution gebündelt werden. Die Komponenten sind:

1. Der lokale [Naming-Service](#naming-services), der Abfragen durchführt und auch [Base32-Hostnamen](#base32-names) verarbeitet.
2. Der [HTTP-Proxy](#http-proxy), der den Router nach Abfragen fragt und den Benutzer zu entfernten Jump-Services weiterleitet, um bei fehlgeschlagenen Abfragen zu helfen.
3. HTTP-[Host-Add-Formulare](#host-add-services), die es Benutzern ermöglichen, Hosts zu ihrer lokalen hosts.txt hinzuzufügen.
4. HTTP-[Jump-Services](#jump-services), die ihre eigenen Abfragen und Weiterleitungen bereitstellen.
5. Die [Adressbuch](#address-book)-Anwendung, die externe Host-Listen, die über HTTP abgerufen werden, mit der lokalen Liste zusammenführt.
6. Die [SusiDNS](#susidns)-Anwendung, die eine einfache Web-Oberfläche für die Adressbuch-Konfiguration und Anzeige der lokalen Host-Listen ist.

---

## Namensauflösungsdienste

Alle Ziele in I2P sind 516-Byte (oder längere) Schlüssel. (Um genauer zu sein, es ist ein 256-Byte öffentlicher Schlüssel plus ein 128-Byte Signaturschlüssel plus ein 3-oder-mehr-Byte Zertifikat, was in Base64-Darstellung 516 oder mehr Bytes entspricht. Nicht-null [Certificates](/docs/legacy/naming/#certificates) werden jetzt zur Angabe des Signaturtyps verwendet. Daher sind Zertifikate in kürzlich generierten Zielen mehr als 3 Bytes groß.

Wenn eine Anwendung (i2ptunnel oder der HTTP-Proxy) auf ein Ziel über den Namen zugreifen möchte, führt der router eine sehr einfache lokale Suche durch, um diesen Namen aufzulösen.

### Hosts.txt Namensservice

Der hosts.txt Naming Service führt eine einfache lineare Suche durch Textdateien durch. Dieser Naming Service war bis zur Version 0.8.8 der Standard, als er durch den Blockfile Naming Service ersetzt wurde. Das hosts.txt Format war zu langsam geworden, nachdem die Datei auf Tausende von Einträgen angewachsen war.

Es führt eine lineare Suche durch drei lokale Dateien durch, in der Reihenfolge, um Hostnamen nachzuschlagen und sie in einen 516-Byte-Zielschlüssel umzuwandeln. Jede Datei ist in einem einfachen [Konfigurationsdateiformat](/docs/specs/configuration/), mit hostname=base64, eine pro Zeile. Die Dateien sind:

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Blockfile Naming Service

Der Blockfile Naming Service speichert mehrere "Adressbücher" in einer einzigen Datenbankdatei namens hostsdb.blockfile. Dieser Naming Service ist seit Release 0.8.8 der Standard.

Eine blockfile ist einfach eine Festplattenspeicherung von mehreren sortierten Maps (Schlüssel-Wert-Paaren), implementiert als Skiplists. Das blockfile-Format ist auf der [Blockfile-Seite](/docs/specs/blockfile/) spezifiziert. Es ermöglicht schnelle Destination-Suche in einem kompakten Format. Während der blockfile-Overhead erheblich ist, werden die Destinations in binärer Form gespeichert und nicht in Base 64 wie im hosts.txt-Format. Zusätzlich bietet die blockfile die Möglichkeit zur Speicherung beliebiger Metadaten (wie Hinzufügungsdatum, Quelle und Kommentare) für jeden Eintrag, um erweiterte Adressbuch-Funktionen zu implementieren. Der Speicherbedarf der blockfile ist eine moderate Steigerung gegenüber dem hosts.txt-Format, und die blockfile bietet etwa 10-fache Reduzierung der Suchzeiten.

Bei der Erstellung importiert der Naming Service Einträge aus den drei Dateien, die vom hosts.txt Naming Service verwendet werden. Die Blockdatei ahmt die vorherige Implementierung nach, indem sie drei Maps verwaltet, die in der Reihenfolge durchsucht werden und privatehosts.txt, userhosts.txt und hosts.txt genannt werden. Sie verwaltet auch eine Reverse-Lookup-Map, um schnelle Reverse-Lookups zu implementieren.

### Andere Naming Service-Einrichtungen

Die Suche ist nicht zwischen Groß- und Kleinschreibung unterscheidend. Der erste Treffer wird verwendet, und Konflikte werden nicht erkannt. Es gibt keine Durchsetzung von Benennungsregeln bei Suchanfragen. Suchanfragen werden für einige Minuten zwischengespeichert. Base 32-Auflösung wird [unten beschrieben](#base32-names). Für eine vollständige Beschreibung der Naming Service API siehe die [Naming Service Javadocs](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). Diese API wurde in Version 0.8.7 erheblich erweitert, um Hinzufügungen und Entfernungen, Speicherung beliebiger Eigenschaften mit dem Hostnamen und andere Funktionen bereitzustellen.

### Alternative und experimentelle Namensdienste

Der Naming-Service wird mit der Konfigurationseigenschaft `i2p.naming.impl=class` spezifiziert. Andere Implementierungen sind möglich. Zum Beispiel gibt es eine experimentelle Einrichtung für Echtzeit-Lookups (ähnlich DNS) über das Netzwerk innerhalb des routers. Für weitere Informationen siehe die [Alternativen auf der Diskussionsseite](/docs/legacy/naming/#alternatives).

Der HTTP-Proxy führt eine Suche über den router für alle Hostnamen durch, die auf '.i2p' enden. Andernfalls leitet er die Anfrage an einen konfigurierten HTTP-Outproxy weiter. Daher müssen in der Praxis alle HTTP (I2P Site) Hostnamen auf die Pseudo-Top-Level-Domain '.i2p' enden.

Wenn der router den Hostnamen nicht auflösen kann, gibt der HTTP-Proxy eine Fehlerseite an den Benutzer zurück mit Links zu mehreren "Jump"-Diensten. Siehe unten für Details.

---

## .i2p.alt Domain

Wir haben zuvor [beantragt, die .i2p TLD zu reservieren](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/), gemäß den in [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html) spezifizierten Verfahren. Jedoch wurde dieser Antrag und alle anderen abgelehnt, und RFC 6761 wurde als "Fehler" erklärt.

Nach jahrelanger Arbeit des GNUnet-Teams und anderen wurde die .alt-Domain Ende 2023 als TLD für besondere Verwendung in [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) reserviert. Obwohl es keine offiziellen, von der IANA sanktionierten Registrare gibt, haben wir die Domain .i2p.alt beim primären inoffiziellen Registrar [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html) registriert. Dies hindert andere nicht daran, die Domain zu verwenden, sollte aber dazu beitragen, dies zu verhindern.

Ein Vorteil der .alt Domain ist, dass DNS-Resolver theoretisch keine .alt-Anfragen weiterleiten werden, sobald sie sich zur Einhaltung von RFC 9476 aktualisieren, was DNS-Lecks verhindert. Für die Kompatibilität mit .i2p.alt Hostnamen sollten I2P-Software und -Dienste aktualisiert werden, um diese Hostnamen zu verarbeiten, indem die .alt TLD entfernt wird. Diese Updates sind für die erste Hälfte von 2024 geplant.

Derzeit gibt es keine Pläne, .i2p.alt zur bevorzugten Form für die Anzeige und den Austausch von I2P-Hostnamen zu machen. Dies ist ein Thema für weitere Forschung und Diskussion.

---

## Adressbuch

### Eingehende Abonnements und Zusammenführung

Die Adressbuch-Anwendung ruft regelmäßig die hosts.txt-Dateien anderer Benutzer ab und führt sie nach mehreren Überprüfungen mit der lokalen hosts.txt zusammen. Namenskonflikte werden nach dem Prinzip "Wer zuerst kommt, mahlt zuerst" gelöst.

Das Abonnieren der hosts.txt-Datei eines anderen Benutzers bedeutet, ihm ein gewisses Maß an Vertrauen entgegenzubringen. Sie möchten nicht, dass er beispielsweise eine neue Site "kapert", indem er schnell seinen eigenen Schlüssel für eine neue Site einträgt, bevor er den neuen Host-/Schlüsseleintrag an Sie weitergibt.

Aus diesem Grund ist standardmäßig nur die Subscription `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)` konfiguriert, die eine Kopie der hosts.txt enthält, die in der I2P-Version enthalten ist. Benutzer müssen zusätzliche Subscriptions in ihrer lokalen Adressbuch-Anwendung konfigurieren (über subscriptions.txt oder [SusiDNS](#susidns)).

Einige andere öffentliche Adressbuch-Abonnement-Links:

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Die Betreiber dieser Dienste können verschiedene Richtlinien für die Auflistung von Hosts haben. Die Aufnahme in diese Liste stellt keine Befürwortung dar.

### Benennungsregeln

Obwohl es hoffentlich keine technischen Beschränkungen innerhalb von I2P für Hostnamen gibt, setzt das Adressbuch mehrere Einschränkungen für Hostnamen durch, die aus Abonnements importiert werden. Dies geschieht aus grundlegenden typographischen Gründen und zur Kompatibilität mit Browsern sowie aus Sicherheitsgründen. Die Regeln sind im Wesentlichen dieselben wie die in RFC2396 Abschnitt 3.2.2. Hostnamen, die gegen diese Regeln verstoßen, werden möglicherweise nicht an andere router weitergegeben.

Benennungsregeln:

- Namen werden beim Import in Kleinbuchstaben umgewandelt.
- Namen werden nach der Umwandlung in Kleinbuchstaben auf Konflikte mit bestehenden Namen in der vorhandenen userhosts.txt und hosts.txt (aber nicht privatehosts.txt) überprüft.
- Dürfen nach der Umwandlung in Kleinbuchstaben nur [a-z] [0-9] '.' und '-' enthalten.
- Dürfen nicht mit '.' oder '-' beginnen.
- Müssen mit '.i2p' enden.
- Maximal 67 Zeichen, einschließlich '.i2p'.
- Dürfen nicht '..' enthalten.
- Dürfen nicht '.-' oder '-.' enthalten (ab 0.6.1.33).
- Dürfen nicht '--' enthalten, außer in 'xn--' für IDN.
- Base32-Hostnamen (*.b32.i2p) sind für base 32 Verwendung reserviert und dürfen daher nicht importiert werden.
- Bestimmte für die Projektnutzung reservierte Hostnamen sind nicht erlaubt (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p und andere)
- Hostnamen, die mit 'www.' beginnen, sind unerwünscht und werden von einigen Registrierungsdiensten abgelehnt. Einige addressbook-Implementierungen entfernen automatisch 'www.'-Präfixe bei Anfragen. Die Registrierung von 'www.example.i2p' ist daher unnötig, und die Registrierung eines anderen Ziels für 'www.example.i2p' und 'example.i2p' wird 'www.example.i2p' für einige Benutzer unerreichbar machen.
- Schlüssel werden auf base64-Gültigkeit überprüft.
- Schlüssel werden auf Konflikte mit bestehenden Schlüsseln in hosts.txt (aber nicht privatehosts.txt) überprüft.
- Minimale Schlüssellänge 516 Bytes.
- Maximale Schlüssellänge 616 Bytes (um Zertifikate bis zu 100 Bytes zu berücksichtigen).

Jeder Name, der über ein Abonnement empfangen wird und alle Prüfungen besteht, wird über den lokalen Namensdienst hinzugefügt.

Beachten Sie, dass die '.'-Symbole in einem Hostnamen keine Bedeutung haben und keine tatsächliche Benennungs- oder Vertrauenshierarchie darstellen. Wenn der Name 'host.i2p' bereits existiert, hindert nichts jemanden daran, einen Namen 'a.host.i2p' zu seiner hosts.txt hinzuzufügen, und dieser Name kann von anderen Adressbüchern importiert werden. Methoden zur Verweigerung von Subdomains für Nicht-Domain-'Besitzer' (Zertifikate?), sowie die Wünschbarkeit und Durchführbarkeit dieser Methoden, sind Themen für zukünftige Diskussionen.

Internationale Domainnamen (IDN) funktionieren auch in i2p (unter Verwendung der punycode 'xn--' Form). Um IDN .i2p Domainnamen korrekt in der Adressleiste von Firefox angezeigt zu bekommen, fügen Sie 'network.IDN.whitelist.i2p (boolean) = true' in about:config hinzu.

Da die Adressbuch-Anwendung die privatehosts.txt überhaupt nicht verwendet, ist diese Datei in der Praxis der einzige geeignete Ort, um private Aliase oder "Kosenamen" für Websites zu platzieren, die bereits in hosts.txt stehen.

### Erweiterte Abonnement-Feed-Format

Ab Version 0.9.26 können Abonnement-Seiten und Clients ein erweiteres hosts.txt-Feed-Protokoll unterstützen, das Metadaten einschließlich Signaturen enthält. Dieses Format ist rückwärtskompatibel mit dem Standard-hosts.txt-Format hostname=base64destination. Siehe [die Spezifikation](/docs/specs/subscription/) für Details.

### Ausgehende Abonnements

Das Adressbuch wird die zusammengeführte hosts.txt an einem Ort veröffentlichen (traditionell hosts.txt im Home-Verzeichnis der lokalen I2P Site), damit andere darauf für ihre Abonnements zugreifen können. Dieser Schritt ist optional und standardmäßig deaktiviert.

### Hosting- und HTTP-Transport-Probleme

Die Adressbuch-Anwendung speichert zusammen mit eepget die vom Webserver des Abonnements zurückgegebenen Etag- und/oder Last-Modified-Informationen. Dies reduziert die benötigte Bandbreite erheblich, da der Webserver beim nächsten Abruf eine '304 Not Modified'-Antwort zurückgibt, wenn sich nichts geändert hat.

Allerdings wird die gesamte hosts.txt heruntergeladen, falls sie sich geändert hat. Siehe unten für eine Diskussion zu diesem Problem.

Hosts, die eine statische hosts.txt oder eine entsprechende CGI-Anwendung bereitstellen, werden nachdrücklich ermutigt, einen Content-Length-Header und entweder einen Etag- oder Last-Modified-Header zu liefern. Stellen Sie außerdem sicher, dass der Server bei Bedarf eine '304 Not Modified'-Antwort sendet. Dies wird die Netzwerkbandbreite drastisch reduzieren und die Wahrscheinlichkeit von Beschädigungen verringern.

---

## Host-Dienste hinzufügen

Ein Host-Add-Service ist eine einfache CGI-Anwendung, die einen Hostnamen und einen Base64-Schlüssel als Parameter entgegennimmt und diese zu ihrer lokalen hosts.txt hinzufügt. Wenn andere router diese hosts.txt abonniert haben, wird der neue Hostname/Schlüssel durch das Netzwerk verbreitet.

Es wird empfohlen, dass Host-Hinzufügungsdienste mindestens die gleichen Beschränkungen durchsetzen, die von der oben aufgeführten Adressbuch-Anwendung auferlegt werden. Host-Hinzufügungsdienste können zusätzliche Beschränkungen für Hostnamen und Schlüssel auferlegen, zum Beispiel:

- Eine Begrenzung der Anzahl von 'Subdomains'.
- Autorisierung für 'Subdomains' durch verschiedene Methoden.
- Hashcash oder signierte Zertifikate.
- Redaktionelle Überprüfung von Hostnamen und/oder Inhalten.
- Kategorisierung von Hosts nach Inhalten.
- Reservierung oder Ablehnung bestimmter Hostnamen.
- Beschränkungen der Anzahl von Namen, die in einem bestimmten Zeitraum registriert werden.
- Verzögerungen zwischen Registrierung und Veröffentlichung.
- Anforderung, dass der Host zur Überprüfung erreichbar ist.
- Ablauf und/oder Widerruf.
- IDN-Spoofing-Ablehnung.

---

## Jump Services

Ein Jump-Service ist eine einfache CGI-Anwendung, die einen Hostnamen als Parameter entgegennimmt und eine 301-Weiterleitung zur entsprechenden URL mit einem angehängten `?i2paddresshelper=key`-String zurückgibt. Der HTTP-Proxy wird den angehängten String interpretieren und diesen Schlüssel als das tatsächliche Ziel verwenden. Zusätzlich wird der Proxy diesen Schlüssel zwischenspeichern, sodass der Address Helper bis zum Neustart nicht mehr erforderlich ist.

Beachten Sie, dass die Nutzung eines Jump-Services, wie bei Abonnements auch, ein gewisses Maß an Vertrauen voraussetzt, da ein Jump-Service einen Benutzer böswillig zu einem falschen Ziel weiterleiten könnte.

Um den besten Service zu bieten, sollte ein Jump-Service mehrere hosts.txt-Anbieter abonnieren, damit seine lokale Host-Liste aktuell ist.

---

## SusiDNS

SusiDNS ist einfach eine Web-Oberfläche zur Konfiguration von Adressbuch-Abonnements und zum Zugriff auf die vier Adressbuch-Dateien. Die eigentliche Arbeit wird von der 'Adressbuch'-Anwendung erledigt.

Derzeit gibt es nur wenig Durchsetzung der Adressbuch-Namensregeln innerhalb von SusiDNS, sodass ein Benutzer lokal Hostnamen eingeben kann, die von den Adressbuch-Abonnement-Regeln abgelehnt würden.

---

## Base32-Namen

I2P unterstützt Base32-Hostnamen ähnlich zu Tors .onion-Adressen. Base32-Adressen sind viel kürzer und einfacher zu handhaben als die vollständigen 516-Zeichen langen Base64-Destinations oder Addresshelper. Beispiel: `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

In Tor ist die Adresse 16 Zeichen (80 Bits) lang, oder die Hälfte des SHA-1-Hash. I2P verwendet 52 Zeichen (256 Bits), um den vollständigen SHA-256-Hash darzustellen. Die Form ist {52 Zeichen}.b32.i2p. Tor hat einen [Vorschlag](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013), zu einem identischen Format von {52 Zeichen}.onion für ihre Hidden Services zu wechseln. Base32 ist im Naming Service implementiert, der den router über I2CP abfragt, um das leaseSet zu suchen und das vollständige Destination zu erhalten. Base32-Lookups sind nur erfolgreich, wenn das Destination aktiv ist und ein leaseSet veröffentlicht. Da die Auflösung eine netDb-Suche erfordern kann, kann sie erheblich länger dauern als eine lokale Adressbuch-Suche.

Base32-Adressen können an den meisten Stellen verwendet werden, wo Hostnamen oder vollständige Ziele verwendet werden, jedoch gibt es einige Ausnahmen, wo sie fehlschlagen können, wenn der Name nicht sofort aufgelöst wird. I2PTunnel wird beispielsweise fehlschlagen, wenn der Name nicht zu einem Ziel aufgelöst wird.

---

## Erweiterte Base32-Namen

Extended base 32 Namen wurden in Version 0.9.40 eingeführt, um verschlüsselte lease sets zu unterstützen. Adressen für verschlüsselte leaseSets werden durch 56 oder mehr kodierte Zeichen identifiziert, nicht einschließlich der ".b32.i2p" (35 oder mehr dekodierte Bytes), verglichen mit 52 Zeichen (32 Bytes) für traditionelle base 32 Adressen. Siehe Vorschläge 123 und 149 für zusätzliche Informationen.

Standard Base 32 ("b32") Adressen enthalten den Hash des Ziels. Dies funktioniert nicht für verschlüsselte ls2 (Vorschlag 123).

Sie können keine traditionelle Base32-Adresse für ein verschlüsseltes LS2 (Vorschlag 123) verwenden, da sie nur den Hash des Ziels enthält. Sie stellt nicht den ungeblendeten öffentlichen Schlüssel zur Verfügung. Clients müssen den öffentlichen Schlüssel des Ziels, den Signaturtyp, den geblendeten Signaturtyp und einen optionalen geheimen oder privaten Schlüssel kennen, um das leaseSet abzurufen und zu entschlüsseln. Daher ist eine Base32-Adresse allein unzureichend. Der Client benötigt entweder das vollständige Ziel (welches den öffentlichen Schlüssel enthält) oder den öffentlichen Schlüssel für sich allein. Wenn der Client das vollständige Ziel in einem Adressbuch hat und das Adressbuch eine Rückwärtssuche nach Hash unterstützt, dann kann der öffentliche Schlüssel abgerufen werden.

Also brauchen wir ein neues Format, das den öffentlichen Schlüssel anstelle des Hashes in eine base32-Adresse einfügt. Dieses Format muss auch den Signaturtyp des öffentlichen Schlüssels und den Signaturtyp des Blinding-Schemas enthalten.

Dieser Abschnitt dokumentiert ein neues b32-Format für diese Adressen. Obwohl wir während Diskussionen auf dieses neue Format als "b33"-Adresse verwiesen haben, behält das tatsächliche neue Format das übliche ".b32.i2p"-Suffix bei.

### Erstellung und Kodierung

Konstruiere einen Hostnamen von {56+ Zeichen}.b32.i2p (35+ Zeichen in binär) wie folgt. Erstelle zuerst die binären Daten, die base 32 kodiert werden sollen:

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Nachbearbeitung und Prüfsumme:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Alle ungenutzten Bits am Ende der b32 müssen 0 sein. Es gibt keine ungenutzten Bits für eine Standard-56-Zeichen-(35-Byte-)Adresse.

### Dekodierung und Verifikation

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Secret und Private Key Bits

Die secret- und private-key-Bits werden verwendet, um Clients, Proxies oder anderen clientseitigen Code zu signalisieren, dass der secret- und/oder private-key benötigt wird, um das leaseSet zu entschlüsseln. Bestimmte Implementierungen können den Benutzer auffordern, die erforderlichen Daten bereitzustellen, oder Verbindungsversuche ablehnen, wenn die erforderlichen Daten fehlen.

### Notizen

- Das XOR der ersten 3 Bytes mit dem Hash bietet eine begrenzte Prüfsummen-Funktionalität und stellt sicher, dass alle base32-Zeichen am Anfang randomisiert sind. Nur wenige Flag- und Sigtype-Kombinationen sind gültig, daher wird jeder Tippfehler wahrscheinlich eine ungültige Kombination erzeugen und abgelehnt.
- Im üblichen Fall (1-Byte-Sigtypes, kein Secret, keine Pro-Client-Authentifizierung) wird der Hostname {56 Zeichen}.b32.i2p sein und zu 35 Bytes dekodiert, genau wie bei Tor.
- Tors 2-Byte-Prüfsumme hat eine 1/64K False-Negative-Rate. Mit 3 Bytes, abzüglich einiger ignorierter Bytes, nähert sich unsere Rate 1 zu einer Million, da die meisten Flag/Sigtype-Kombinationen ungültig sind.
- Adler-32 ist eine schlechte Wahl für kleine Eingaben und zum Erkennen kleiner Änderungen. Wir verwenden stattdessen CRC-32. CRC-32 ist schnell und weit verbreitet verfügbar.
- Obwohl außerhalb des Bereichs dieser Spezifikation, müssen router und/oder Clients die Zuordnung von öffentlichem Schlüssel zu Destination und umgekehrt merken und (wahrscheinlich persistent) zwischenspeichern.
- Unterscheide alte von neuen Varianten anhand der Länge. Alte b32-Adressen sind immer {52 Zeichen}.b32.i2p. Neue sind {56+ Zeichen}.b32.i2p
- Tor-Diskussionsthread [ist hier](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Erwarte nicht, dass 2-Byte-Sigtypes jemals auftreten, wir sind erst bei 13. Keine Notwendigkeit, jetzt zu implementieren.
- Das neue Format kann in Jump-Links (und von Jump-Servern bereitgestellt) verwendet werden, falls gewünscht, genau wie b32.
- Jedes Secret, privater Schlüssel oder öffentlicher Schlüssel länger als 32 Bytes würde die DNS-maximale Label-Länge von 63 Zeichen überschreiten. Browser kümmern sich wahrscheinlich nicht darum.
- Keine Rückwärtskompatibilitätsprobleme. Längere b32-Adressen werden in alter Software nicht zu 32-Byte-Hashes konvertiert werden können.
