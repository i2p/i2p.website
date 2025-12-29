---
title: "Leistung"
description: "I2P-Netzwerkleistung: wie es sich heute verhält, historische Verbesserungen und Ideen für zukünftige Optimierungen"
slug: "performance"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## I2P Netzwerk-Performance: Geschwindigkeit, Verbindungen und Ressourcenverwaltung

Das I2P-Netzwerk ist vollständig dynamisch. Jeder Client ist anderen Knoten bekannt und testet lokal bekannte Knoten auf Erreichbarkeit und Kapazität. Nur erreichbare und leistungsfähige Knoten werden in einer lokalen NetDB gespeichert. Während des Tunnel-Aufbauprozesses werden die besten Ressourcen aus diesem Pool ausgewählt, um Tunnel aufzubauen. Da das Testen kontinuierlich stattfindet, ändert sich der Pool der Knoten. Jeder I2P-Knoten kennt einen anderen Teil der NetDB, was bedeutet, dass jeder Router eine andere Menge von I2P-Knoten hat, die für Tunnel verwendet werden können. Selbst wenn zwei Router die gleiche Teilmenge bekannter Knoten haben, werden die Tests auf Erreichbarkeit und Kapazität wahrscheinlich unterschiedliche Ergebnisse zeigen, da die anderen Router möglicherweise gerade unter Last stehen, wenn ein Router testet, aber frei sind, wenn der zweite Router testet.

Dies beschreibt, warum jeder I2P-Knoten unterschiedliche Knoten zum Aufbau von Tunnels verwendet. Da jeder I2P-Knoten eine unterschiedliche Latenz und Bandbreite hat, weisen Tunnels (die über diese Knoten aufgebaut werden) unterschiedliche Latenz- und Bandbreitenwerte auf. Und da jeder I2P-Knoten unterschiedliche Tunnels aufgebaut hat, haben keine zwei I2P-Knoten die gleichen Tunnel-Sets.

Ein Server/Client wird als "Destination" bezeichnet und jede Destination verfügt über mindestens einen eingehenden und einen ausgehenden Tunnel. Die Standardeinstellung beträgt 3 Hops pro Tunnel. Dies summiert sich auf 12 Hops (12 verschiedene I2P-Knoten) für einen vollständigen Roundtrip Client → Server → Client.

Jedes Datenpaket wird durch 6 andere I2P-Knoten gesendet, bis es den Server erreicht:

client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server

und auf dem Rückweg 6 verschiedene I2P-Knoten:

server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client

Datenverkehr im Netzwerk benötigt ein ACK, bevor neue Daten gesendet werden; er muss warten, bis ein ACK vom Server zurückkommt: Daten senden, auf ACK warten, weitere Daten senden, auf ACK warten. Da sich die RTT (Round Trip Time) aus der Latenz jedes einzelnen I2P-Knotens und jeder Verbindung auf dieser Hin- und Rückstrecke zusammensetzt, dauert es normalerweise 1–3 Sekunden, bis ein ACK zum Client zurückkommt. Aufgrund des Designs von TCP und I2P-Transport hat ein Datenpaket eine begrenzte Größe. Zusammen setzen diese Bedingungen eine maximale Bandbreite pro Tunnel von etwa 20–50 kB/s. Wenn jedoch nur ein Hop im Tunnel nur 5 kB/s Bandbreite zur Verfügung hat, ist der gesamte Tunnel auf 5 kB/s begrenzt, unabhängig von der Latenz und anderen Einschränkungen.

Verschlüsselung, Latenz und die Art und Weise, wie ein Tunnel aufgebaut wird, machen es sehr rechenintensiv, einen Tunnel zu erstellen. Deshalb darf eine Destination maximal 6 eingehende und 6 ausgehende Tunnels für den Datentransport haben. Mit maximal 50 kB/s pro Tunnel könnte eine Destination ungefähr 300 kB/s Traffic insgesamt nutzen (in Wirklichkeit könnte es mehr sein, wenn kürzere Tunnels mit geringer oder keiner Anonymität verwendet werden). Benutzte Tunnels werden alle 10 Minuten verworfen und neue werden aufgebaut. Dieser Wechsel von Tunnels und manchmal Clients, die herunterfahren oder ihre Verbindung zum Netzwerk verlieren, führen manchmal zu unterbrochenen Tunnels und Verbindungen. Ein Beispiel dafür ist im IRC2P Network beim Verbindungsverlust (Ping Timeout) oder bei der Verwendung von eepget zu sehen.

Mit einer begrenzten Anzahl von Zielen und einer begrenzten Anzahl von Tunneln pro Ziel verwendet ein I2P-Knoten nur eine begrenzte Anzahl von Tunneln über andere I2P-Knoten hinweg. Wenn beispielsweise ein I2P-Knoten im obigen kleinen Beispiel "hop1" ist, sieht er nur einen teilnehmenden Tunnel, der vom Client ausgeht. Summiert man das gesamte I2P-Netzwerk auf, könnte nur eine relativ begrenzte Anzahl teilnehmender Tunnel mit insgesamt begrenzter Bandbreite aufgebaut werden. Verteilt man diese begrenzten Zahlen auf die Anzahl der I2P-Knoten, steht nur ein Bruchteil der verfügbaren Bandbreite/Kapazität zur Nutzung bereit.

Um anonym zu bleiben, sollte ein Router nicht vom gesamten Netzwerk zum Aufbau von Tunneln verwendet werden. Wenn ein Router als Tunnel-Router für alle I2P-Knoten fungiert, wird er zu einem sehr realen zentralen Ausfallpunkt sowie zu einem zentralen Punkt zum Sammeln von IPs und Daten von Clients. Aus diesem Grund verteilt das Netzwerk den Datenverkehr im Tunnel-Aufbauprozess über mehrere Knoten.

Ein weiterer Aspekt für die Performance ist die Art und Weise, wie I2P das Mesh-Netzwerk handhabt. Jeder Verbindungs-Hop nutzt eine TCP- oder UDP-Verbindung auf I2P-Knoten. Bei 1000 Verbindungen sieht man 1000 TCP-Verbindungen. Das ist ziemlich viel, und einige Heim- und kleine Büro-Router erlauben nur eine geringe Anzahl von Verbindungen. I2P versucht, diese Verbindungen auf unter 1500 pro UDP- und pro TCP-Typ zu begrenzen. Dies begrenzt auch die Menge an Traffic, die über einen I2P-Knoten geroutet wird.

Wenn ein Node erreichbar ist und eine Bandbreiteneinstellung von >128 kB/s geteilt hat sowie 24/7 erreichbar ist, sollte er nach einiger Zeit für Teilnahme-Traffic verwendet werden. Wenn er zwischenzeitlich offline ist, wird das Testen eines I2P-Nodes durch andere Nodes diesen als nicht erreichbar melden. Dies blockiert einen Node für mindestens 24 Stunden auf anderen Nodes. Die anderen Nodes, die diesen Node als offline getestet haben, werden ihn also 24 Stunden lang nicht für den Aufbau von Tunneln verwenden. Deshalb ist Ihr Traffic nach einem Neustart/Herunterfahren Ihres I2P-Routers für mindestens 24 Stunden niedriger.

Zusätzlich müssen andere I2P-Knoten einen I2P-Router kennen, um ihn auf Erreichbarkeit und Kapazität zu testen. Dieser Prozess kann beschleunigt werden, wenn Sie mit dem Netzwerk interagieren, beispielsweise durch die Nutzung von Anwendungen oder den Besuch von I2P-Sites, was zu mehr Tunnel-Aufbau und damit zu mehr Aktivität und Erreichbarkeit für Tests durch Knoten im Netzwerk führt.

## Leistungshistorie (Auswahl)

Im Laufe der Jahre hat I2P eine Reihe bemerkenswerter Leistungsverbesserungen erfahren:

### Native math

Implementiert über JNI-Bindings zur GNU MP-Bibliothek (GMP), um BigInteger `modPow` zu beschleunigen, welches zuvor die CPU-Zeit dominierte. Erste Ergebnisse zeigten dramatische Geschwindigkeitssteigerungen bei Public-Key-Kryptographie. Siehe: /misc/jbigi/

### Garlic wrapping a "reply" LeaseSet (tuned)

Zuvor erforderten Antworten häufig eine Netzwerkdatenbankabfrage für den LeaseSet des Absenders. Das Bündeln des LeaseSet des Absenders im initialen Garlic verbessert die Antwortlatenz. Dies wird jetzt selektiv durchgeführt (Beginn einer Verbindung oder wenn sich der LeaseSet ändert), um den Overhead zu reduzieren.

### Native Mathematik

Einige Validierungsschritte wurden früher im Transport-Handshake durchgeführt, um fehlerhafte Peers schneller abzulehnen (falsche Uhrzeiten, fehlerhafte NAT/Firewall, inkompatible Versionen), wodurch CPU und Bandbreite gespart werden.

### Garlic-Verpackung eines "Reply" LeaseSet (optimiert)

Verwenden Sie kontextbewusstes Tunnel-Testing: Vermeiden Sie das Testen von Tunneln, bei denen bereits bekannt ist, dass sie Daten übertragen; bevorzugen Sie Tests im Leerlauf. Dies reduziert den Overhead und beschleunigt die Erkennung fehlerhafter Tunnel.

### Effizientere TCP-Ablehnung

Das Beibehalten von Auswahlentscheidungen für eine bestimmte Verbindung reduziert die Auslieferung außerhalb der Reihenfolge und ermöglicht es der Streaming-Bibliothek, die Fenstergrößen zu erhöhen, wodurch der Durchsatz verbessert wird.

### Anpassungen für Tunnel-Tests

GZip oder Ähnliches für ausführliche Strukturen (z.B. RouterInfo-Optionen) reduziert die Bandbreite, wo es angebracht ist.

### Persistente Tunnel-/Lease-Auswahl

Ersatz für das vereinfachte „ministreaming"-Protokoll. Modernes Streaming umfasst selektive ACKs und Staukontrolle, die auf I2Ps anonyme, nachrichtenorientierte Infrastruktur zugeschnitten sind. Siehe: /docs/api/streaming/

## Future Performance Improvements (historical ideas)

Nachfolgend sind Ideen dokumentiert, die historisch als potenzielle Verbesserungen erfasst wurden. Viele sind veraltet, implementiert oder durch architektonische Änderungen überholt.

### Ausgewählte Datenstrukturen komprimieren

Verbessere die Art und Weise, wie Router Peers für den Tunnelbau auswählen, um langsame oder überlastete zu vermeiden, während gleichzeitig die Widerstandsfähigkeit gegen Sybil-Angriffe durch mächtige Angreifer erhalten bleibt.

### Vollständiges Streaming-Protokoll

Reduziere unnötige Exploration, wenn der Keyspace stabil ist; passe an, wie viele Peers bei Lookups zurückgegeben werden und wie viele gleichzeitige Suchen durchgeführt werden.

### Session Tag tuning and improvements (legacy)

Für das veraltete ElGamal/AES+SessionTag-Schema reduzieren intelligentere Ablauf- und Auffüllstrategien ElGamal-Fallbacks und verschwendete Tags.

### Bessere Peer-Profilierung und -Auswahl

Generiere Tags aus einem synchronisierten PRNG, der während der Etablierung einer neuen Session initialisiert wird, wodurch der Overhead pro Nachricht im Vergleich zu vorab zugestellten Tags reduziert wird.

### Netzwerkdatenbank-Tuning

Längere Tunnel-Lebensdauern in Verbindung mit Healing können den Rebuild-Overhead reduzieren; dies muss gegen Anonymität und Zuverlässigkeit abgewogen werden.

### Session Tag Anpassung und Verbesserungen (veraltet)

Ungültige Peers früher ablehnen und Tunneltests kontextbezogener gestalten, um Konflikte und Latenz zu reduzieren.

### SessionTag zu synchronisiertem PRNG migrieren (veraltet)

Selektives LeaseSet-Bündeln, komprimierte RouterInfo-Optionen und die Einführung des vollständigen Streaming-Protokolls tragen alle zu einer besseren wahrgenommenen Leistung bei.

Siehe auch:

- [Tunnel Routing](/docs/overview/tunnel-routing/)
- [Peer-Auswahl](/docs/overview/tunnel-routing/)
- [Transports](/docs/overview/transport/)
- [SSU2-Spezifikation](/docs/specs/ssu2/) und [NTCP2-Spezifikation](/docs/specs/ntcp2/)
