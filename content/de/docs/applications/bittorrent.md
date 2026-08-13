---
title: "Bittorrent über I2P"
description: "Protokollspezifikationen für BitTorrent-Clients und -Tracker auf I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Es gibt mehrere BitTorrent-Clients und -Tracker auf I2P. Da I2P-Adressierung eine Destination anstelle einer IP-Adresse und eines Ports verwendet, sind geringfügige Änderungen an Tracker- und Client-Software für den Betrieb auf I2P erforderlich. Diese Änderungen sind unten spezifiziert. Beachten Sie sorgfältig die Richtlinien für die Kompatibilität mit älteren I2P-Clients und -Trackern.

Diese Seite spezifiziert Protokolldetails, die allen Clients und Trackern gemeinsam sind. Spezifische Clients und Tracker können andere einzigartige Funktionen oder Protokolle implementieren.

Wir begrüßen weitere Portierungen von Client- und Tracker-Software zu I2P.

---

## Allgemeine Anleitung für Entwickler

Die meisten Nicht-Java-Bittorrent-Clients werden sich über [SAMv3](/docs/api/samv3/) mit I2P verbinden. SAM-Sessions (oder innerhalb von I2P, tunnel pools oder Sets von tunnels) sind darauf ausgelegt, langlebig zu sein. Die meisten Bittorrent-Clients benötigen nur eine Session, die beim Start erstellt und beim Beenden geschlossen wird. I2P unterscheidet sich von Tor, wo Circuits schnell erstellt und verworfen werden können. Denken Sie sorgfältig nach und beraten Sie sich mit I2P-Entwicklern, bevor Sie Ihre Anwendung so gestalten, dass sie mehr als eine oder zwei gleichzeitige Sessions verwendet oder diese schnell erstellt und verwirft. Bittorrent-Clients dürfen nicht für jede Verbindung eine eigene Session erstellen. Gestalten Sie Ihren Client so, dass er dieselbe Session für Ankündigungen und Client-Verbindungen verwendet.

Bitte stellen Sie außerdem sicher, dass Ihre Client-Einstellungen (und die Anleitung für Benutzer bezüglich router-Einstellungen oder router-Standardwerte, falls Sie einen router bündeln) dazu führen, dass Ihre Benutzer mehr Ressourcen zum Netzwerk beitragen, als sie verbrauchen. I2P ist ein Peer-to-Peer-Netzwerk, und das Netzwerk kann nicht überleben, wenn eine beliebte Anwendung das Netzwerk in eine permanente Überlastung treibt.

Bieten Sie keine Unterstützung für BitTorrent über einen I2P-Outproxy zum Clearnet an, da dies wahrscheinlich blockiert wird. Wenden Sie sich für Beratung an die Outproxy-Betreiber.

Die Java I2P und i2pd router Implementierungen sind unabhängig und haben geringfügige Unterschiede im Verhalten, der Funktionsunterstützung und den Standardeinstellungen. Bitte testen Sie Ihre Anwendung mit der neuesten Version beider router.

i2pd SAM ist standardmäßig aktiviert; Java I2P SAM ist es nicht. Stellen Sie Ihren Benutzern Anweisungen zur Verfügung, wie SAM in Java I2P aktiviert wird (über /configclients in der router-Konsole), und/oder zeigen Sie dem Benutzer eine aussagekräftige Fehlermeldung an, wenn die erste Verbindung fehlschlägt, z.B. "stellen Sie sicher, dass I2P läuft und die SAM-Schnittstelle aktiviert ist".

Die Java I2P und i2pd router haben unterschiedliche Standardwerte für die Anzahl der tunnel. Der Java-Standard ist 2 und der i2pd-Standard ist 5. Für die meisten Anwendungen mit niedriger bis mittlerer Bandbreite und niedriger bis mittlerer Verbindungsanzahl sind 3 ausreichend. Bitte geben Sie die tunnel-Anzahl in der SESSION CREATE-Nachricht an, um eine konsistente Leistung mit den Java I2P und i2pd routern zu erzielen.

I2P unterstützt mehrere Signatur- und Verschlüsselungstypen. Aus Kompatibilitätsgründen verwendet I2P standardmäßig alte und ineffiziente Typen, daher sollten alle Clients neuere Typen spezifizieren.

Bei der Verwendung von SAM wird der Signaturtyp in den Befehlen DEST GENERATE und SESSION CREATE (für temporäre) angegeben. Alle Clients sollten SIGNATURE_TYPE=7 (Ed25519) setzen.

Der Verschlüsselungstyp wird im SAM SESSION CREATE-Befehl oder in i2cp-Optionen angegeben. Mehrere Verschlüsselungstypen sind erlaubt. Einige Tracker unterstützen ECIES-X25519, einige unterstützen ElGamal und einige unterstützen beide. Clients sollten i2cp.leaseSetEncType=4,0 (für ECIES-X25519 und ElGamal) setzen, damit sie sich mit beiden verbinden können.

DHT-Unterstützung erfordert SAMv3.3 PRIMARY und SUBSESSIONS für TCP und UDP über dieselbe Sitzung. Dies wird einen erheblichen Entwicklungsaufwand auf der Client-Seite erfordern, es sei denn, der Client ist in Java geschrieben. i2pd unterstützt derzeit kein SAMv3.3. libtorrent unterstützt derzeit kein SAMv3.3.

Ohne DHT-Unterstützung möchten Sie möglicherweise automatisch an eine konfigurierbare Liste bekannter offener Tracker ankündigen, damit Magnet-Links funktionieren. Konsultieren Sie I2P-Benutzer für Informationen über derzeit aktive offene Tracker und halten Sie Ihre Standardeinstellungen aktuell. Die Unterstützung der i2p_pex-Erweiterung wird ebenfalls dabei helfen, das Fehlen von DHT-Unterstützung zu kompensieren.

Für weitere Anleitungen an Entwickler, um sicherzustellen, dass Ihre Anwendung nur die benötigten Ressourcen verwendet, siehe bitte die [SAMv3-Spezifikation](/docs/api/samv3/) und [unseren Leitfaden zur Bündelung von I2P mit Ihrer Anwendung](/docs/applications/embedding/). Kontaktieren Sie I2P- oder i2pd-Entwickler für weitere Unterstützung.

---

## Ankündigungen

Clients fügen in der Regel einen gefälschten port=6881-Parameter in die Ankündigung ein, um die Kompatibilität mit älteren Trackern zu gewährleisten. Tracker können den Port-Parameter ignorieren und sollten ihn nicht voraussetzen.

Der ip-Parameter ist die Base 64-Kodierung der [Destination](/docs/specs/common-structures/#struct_Destination) des Clients, unter Verwendung des I2P Base 64-Alphabets [A-Z][a-z][0-9]-~. [Destinations](/docs/specs/common-structures/#struct_Destination) sind 387+ Bytes groß, daher ist die Base 64-Kodierung 516+ Bytes lang. Clients hängen im Allgemeinen ".i2p" an die Base 64 Destination an, um die Kompatibilität mit älteren Trackern zu gewährleisten. Tracker sollten ein angehängtes ".i2p" nicht voraussetzen.

Andere Parameter sind dieselben wie im Standard-BitTorrent.

Aktuelle Destinations für Clients sind 387 oder mehr Bytes (516 oder mehr in Base64-Kodierung). Ein vernünftiges Maximum, das vorerst angenommen werden kann, sind 475 Bytes. Da der Tracker das Base64 dekodieren muss, um kompakte Antworten zu liefern (siehe unten), sollte der Tracker wahrscheinlich fehlerhaftes Base64 beim Bekanntgeben dekodieren und zurückweisen.

Der Standard-Antworttyp ist nicht-kompakt. Clients können eine kompakte Antwort mit dem Parameter compact=1 anfordern. Ein Tracker kann, ist aber nicht verpflichtet, eine kompakte Antwort zurückzugeben, wenn sie angefordert wird. Hinweis: Alle beliebten Tracker unterstützen jetzt kompakte Antworten und mindestens einer erfordert compact=1 in der Ankündigung. Alle Clients sollten kompakte Antworten anfordern und unterstützen.

Entwickler neuer I2P-Clients werden dringend ermutigt, announces über ihren eigenen tunnel anstatt über den HTTP-Client-Proxy an Port 4444 zu implementieren. Dies ist sowohl effizienter als auch ermöglicht es dem Tracker, destination enforcement durchzusetzen (siehe unten).

Die Spezifikation für UDP-Ankündigungen wurde im Juni 2025 finalisiert. Die Unterstützung in verschiedenen I2P-Clients und Trackern wird im Laufe des Jahres 2025 eingeführt. Siehe unten für weitere Informationen.

---

## Nicht-kompakte Tracker-Antworten

Hinweis: Veraltet. Alle beliebten Tracker unterstützen jetzt kompakte Antworten und mindestens einer erfordert compact=1 in der Ankündigung. Alle Clients sollten kompakte Antworten anfordern und unterstützen.

Die nicht-kompakte Antwort ist genau wie im Standard-BitTorrent, mit einer I2P-"IP". Dies ist ein langer base64-kodierter "DNS-String", wahrscheinlich mit einem ".i2p"-Suffix.

Tracker enthalten in der Regel einen gefälschten Port-Schlüssel oder verwenden den Port aus dem Announce, um die Kompatibilität mit älteren Clients zu gewährleisten. Clients müssen den Port-Parameter ignorieren und sollten ihn nicht als erforderlich behandeln.

Der Wert des ip-Schlüssels ist die Base 64-Kodierung der [Destination](/docs/specs/common-structures/#struct_Destination) des Clients, wie oben beschrieben. Tracker hängen normalerweise ".i2p" an die Base 64-Destination an, falls es nicht in der announce ip enthalten war, um Kompatibilität mit älteren Clients zu gewährleisten. Clients sollten ein angehängtes ".i2p" in den Antworten nicht voraussetzen.

Andere Antwort-Schlüssel und -Werte sind dieselben wie im Standard-BitTorrent.

---

## Kompakte Tracker-Antworten

In der kompakten Antwort ist der Wert des "peers" Dictionary-Schlüssels eine einzelne Byte-Zeichenkette, deren Länge ein Vielfaches von 32 Bytes ist. Diese Zeichenkette enthält die verketteten [32-Byte-SHA-256-Hashes](/docs/specs/common-structures/#type_Hash) der binären [Destinations](/docs/specs/common-structures/#struct_Destination) der Peers. Dieser Hash muss vom Tracker berechnet werden, es sei denn, die Destination-Durchsetzung (siehe unten) wird verwendet, in welchem Fall der in den X-I2P-DestHash- oder X-I2P-DestB32-HTTP-Headern übermittelte Hash in Binärform umgewandelt und gespeichert werden kann. Der peers-Schlüssel kann fehlen oder der peers-Wert kann eine Länge von null haben.

Während die Unterstützung für kompakte Antworten sowohl für Clients als auch für Tracker optional ist, wird sie dringend empfohlen, da sie die nominale Antwortgröße um über 90% reduziert.

---

## Destination-Durchsetzung

Einige, aber nicht alle, I2P-BitTorrent-Clients kündigen über ihre eigenen tunnel an. Tracker können sich dafür entscheiden, Spoofing zu verhindern, indem sie dies verlangen und die [Destination](/docs/specs/common-structures/#struct_Destination) des Clients mithilfe von HTTP-Headern verifizieren, die vom I2PTunnel HTTP Server tunnel hinzugefügt werden. Die Header sind X-I2P-DestHash, X-I2P-DestB64 und X-I2P-DestB32, welche verschiedene Formate für dieselbe Information darstellen. Diese Header können vom Client nicht gefälscht werden. Ein Tracker, der Destinations durchsetzt, muss den ip-Announce-Parameter überhaupt nicht verlangen.

Da mehrere Clients den HTTP-Proxy anstelle ihres eigenen Tunnels für Ankündigungen verwenden, verhindert die Ziel-Durchsetzung die Nutzung durch diese Clients, es sei denn oder bis diese Clients zur Ankündigung über ihren eigenen Tunnel umgestellt werden.

Leider wird mit dem Wachstum des Netzwerks auch die Menge an Bösartigkeit zunehmen, daher erwarten wir, dass alle Tracker schließlich Ziele durchsetzen werden. Sowohl Tracker- als auch Client-Entwickler sollten sich darauf einstellen.

---

## Host-Namen ankündigen

Announce-URL-Hostnamen in Torrent-Dateien folgen im Allgemeinen den [I2P-Namensstandards](/docs/overview/naming/). Zusätzlich zu Hostnamen aus Adressbüchern und ".b32.i2p" Base 32-Hostnamen sollte die vollständige Base 64 Destination (mit oder ohne angehängtes ".i2p") unterstützt werden. Nicht-offene Tracker sollten ihren eigenen Hostnamen in jedem dieser Formate erkennen.

Um die Anonymität zu wahren, sollten Clients grundsätzlich Nicht-I2P-Announce-URLs in Torrent-Dateien ignorieren.

---

## Client-Verbindungen

Client-zu-Client-Verbindungen verwenden das Standardprotokoll über TCP. Es gibt derzeit keine bekannten I2P-Clients, die uTP-Kommunikation unterstützen.

I2P verwendet 387+ Byte [Destinations](/docs/specs/common-structures/#struct_Destination) für Adressen, wie oben erklärt.

Wenn der Client nur den Hash des Ziels hat (z.B. von einer kompakten Antwort oder PEX), muss er eine Suche durchführen, indem er ihn mit Base 32 kodiert, ".b32.i2p" anhängt und den Naming Service abfragt, der das vollständige Destination zurückgibt, falls verfügbar.

Wenn der Client eine vollständige Destination eines Peers hat, die er in einer nicht-kompakten Antwort erhalten hat, sollte er sie direkt beim Verbindungsaufbau verwenden. Konvertieren Sie eine Destination nicht zurück in einen Base 32 Hash für die Suche, dies ist ziemlich ineffizient.

---

## Netzwerkübergreifende Prävention

Um die Anonymität zu wahren, unterstützen I2P-Bittorrent-Clients im Allgemeinen keine Ankündigungen oder Peer-Verbindungen außerhalb von I2P. I2P-HTTP-Outproxies blockieren oft Ankündigungen. Es sind keine SOCKS-Outproxies bekannt, die Bittorrent-Traffic unterstützen.

Um die Nutzung durch Nicht-I2P-Clients über einen HTTP-Inproxy zu verhindern, blockieren I2P-Tracker oft Zugriffe oder Ankündigungen, die einen X-Forwarded-For HTTP-Header enthalten. Tracker sollten Standard-Netzwerk-Ankündigungen mit IPv4- oder IPv6-IPs ablehnen und sie nicht in Antworten ausliefern.

---

## PEX

I2P PEX basiert auf ut_pex. Da es keine formale Spezifikation von ut_pex zu geben scheint, könnte es notwendig sein, den libtorrent-Quellcode zur Hilfestellung zu überprüfen. Es ist eine Erweiterungsnachricht, die als "i2p_pex" im [Extension-Handshake](http://www.bittorrent.org/beps/bep_0010.html) identifiziert wird. Sie enthält ein bencoded Dictionary mit bis zu 3 Schlüsseln: "added", "added.f" und "dropped". Die added- und dropped-Werte sind jeweils eine einzelne Byte-Zeichenkette, deren Länge ein Vielfaches von 32 Bytes ist. Diese Byte-Zeichenketten sind die verketteten SHA-256-Hashes der binären [Destinations](/docs/specs/common-structures/#struct_Destination) der Peers. Dies ist das gleiche Format wie der peers Dictionary-Wert im oben spezifizierten i2p Compact Response Format. Der added.f-Wert, falls vorhanden, ist derselbe wie in ut_pex.

---

## DHT

DHT-Unterstützung ist im i2psnark-Client ab Version 0.9.2 enthalten. Vorläufige Unterschiede zu [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) werden unten beschrieben und können sich ändern. Kontaktieren Sie die I2P-Entwickler, wenn Sie einen Client mit DHT-Unterstützung entwickeln möchten.

Im Gegensatz zu Standard-DHT verwendet I2P DHT kein Bit im Options-Handshake oder in der PORT-Nachricht. Es wird mit einer Extension-Nachricht angekündigt, die als "i2p_dht" in [dem Extension-Handshake](http://www.bittorrent.org/beps/bep_0010.html) identifiziert wird. Sie enthält ein bencoded Dictionary mit zwei Schlüsseln, "port" und "rport", beide Ganzzahlen.

Der UDP (Datagramm) Port, der in den kompakten Knoteninformationen aufgeführt ist, wird zum Empfang von beantwortbaren (signierten) Datagrammen verwendet. Dies wird für Abfragen verwendet, außer für Ankündigungen. Wir nennen dies den "Query-Port". Dies ist der "port"-Wert aus der Erweiterungsnachricht. Abfragen verwenden [I2CP](/docs/specs/i2cp/) Protokollnummer 17.

Zusätzlich zu diesem UDP-Port verwenden wir einen zweiten Datagramm-Port, der dem Query-Port + 1 entspricht. Dieser wird verwendet, um unsignierte (rohe) Datagramme für Antworten, Fehler und Ankündigungen zu empfangen. Dieser Port bietet erhöhte Effizienz, da Antworten Token enthalten, die in der Query gesendet wurden, und nicht signiert werden müssen. Wir nennen dies den "Response-Port". Dies ist der "rport"-Wert aus der Extension-Nachricht. Er muss 1 + dem Query-Port entsprechen. Antworten und Ankündigungen verwenden [I2CP](/docs/specs/i2cp/) Protokollnummer 18.

Kompakte Peer-Informationen sind 32 Bytes (32-Byte-SHA256-Hash) anstelle von 4 Byte IP + 2 Byte Port. Es gibt keinen Peer-Port. In einer Antwort ist der "values"-Schlüssel eine Liste von Strings, die jeweils eine einzelne kompakte Peer-Information enthalten.

Kompakte Knoteninformationen sind 54 Bytes (20 Byte Node ID + 32 Byte SHA256 Hash + 2 Byte Port) anstelle von 20 Byte Node ID + 4 Byte IP + 2 Byte Port. In einer Antwort ist der "nodes"-Schlüssel eine einzige Byte-Zeichenkette mit verketteten kompakten Knoteninformationen.

Sichere Node-ID-Anforderung: Um verschiedene DHT-Angriffe zu erschweren, müssen die ersten 4 Bytes der Node-ID mit den ersten 4 Bytes des Ziel-Hash übereinstimmen, und die nächsten zwei Bytes der Node-ID müssen mit den nächsten zwei Bytes des Ziel-Hash übereinstimmen, die exklusiv-ODER-verknüpft mit dem Port sind.

In einer Torrent-Datei ist der "nodes"-Schlüssel des trackerlosen Torrent-Wörterbuchs noch zu bestimmen. Es könnte eine Liste von 32-Byte-Binärzeichenketten (SHA256-Hashes) anstelle einer Liste von Listen sein, die eine Host-Zeichenkette und eine Port-Ganzzahl enthalten. Alternativen: Eine einzelne Byte-Zeichenkette mit verketteten Hashes oder eine Liste nur aus Zeichenketten.

---

## Datagram (UDP) Tracker

Die Spezifikation für UDP announces in I2P wurde im Juni 2025 finalisiert. Unterstützung in verschiedenen I2P-Clients und Trackern wird später in 2025 ausgerollt. Unterschiede zu [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sind in [der UDP announce-Spezifikation](/docs/specs/udp-announces/) dokumentiert. Die Spezifikation erfordert auch Unterstützung für [die neuen Datagram 2/3-Formate](/docs/specs/datagrams/).

---

## Zusätzliche Informationen

Eine vorläufige Spezifikation zur Berechnung des erlaubten Fast-Set ist in [Vorschlag 172](/proposals/172-bep6-allowed-fast) enthalten.

---

## Zusätzliche Informationen

- I2P bittorrent Standards werden allgemein auf [zzz.i2p](http://zzz.i2p/) diskutiert.
- Eine Übersicht der aktuellen Tracker-Software-Funktionen ist [dort ebenfalls verfügbar](http://zzz.i2p/files/trackers.html).
- Die [I2P bittorrent FAQ](http://forum.i2p/viewtopic.php?t=2068)
- [DHT auf I2P Diskussion](http://zzz.i2p/topics/812)
