---
title: "Leistung"
description: "I2P-Netzwerk-Performance: Geschwindigkeit, Verbindungen und Ressourcenverwaltung"
slug: "performance"
aliases:
  - "/de/about/performance/future"
  - "/de/about/performance/future/"
  - "/de/about/performance/history"
  - "/de/about/performance/history/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## I2P Netzwerk-Performance: Geschwindigkeit, Verbindungen und Ressourcenverwaltung

Das I2P-Netzwerk ist vollständig dynamisch. Jeder Client ist anderen Knoten bekannt und testet lokal bekannte Knoten auf Erreichbarkeit und Kapazität. Nur erreichbare und leistungsfähige Knoten werden in einer lokalen NetDB gespeichert. Während des tunnel-Aufbauprozesses werden die besten Ressourcen aus diesem Pool ausgewählt, um tunnels zu erstellen. Da das Testen kontinuierlich stattfindet, ändert sich der Pool der Knoten. Jeder I2P-Knoten kennt einen anderen Teil der NetDB, was bedeutet, dass jeder router eine andere Auswahl an I2P-Knoten hat, die für tunnels verwendet werden können. Selbst wenn zwei router die gleiche Teilmenge bekannter Knoten haben, werden die Tests für Erreichbarkeit und Kapazität wahrscheinlich unterschiedliche Ergebnisse zeigen, da die anderen router möglicherweise gerade unter Last stehen, wenn ein router testet, aber frei sind, wenn der zweite router testet.

Dies erklärt, warum jeder I2P-Knoten verschiedene Knoten zum Aufbau von tunnels verwendet. Da jeder I2P-Knoten unterschiedliche Latenz und Bandbreite hat, haben tunnels (die über diese Knoten aufgebaut werden) unterschiedliche Latenz- und Bandbreitenwerte. Und da jeder I2P-Knoten verschiedene tunnels aufgebaut hat, haben keine zwei I2P-Knoten die gleichen tunnel-Sets.

Ein Server/Client wird als "destination" (Ziel) bezeichnet und jede destination hat mindestens einen eingehenden und einen ausgehenden tunnel. Der Standard sind 3 Hops pro tunnel. Das summiert sich zu 12 Hops (also 12 verschiedene I2P-Knoten) für eine vollständige Roundtrip-Verbindung Client-Server-Client.

Jedes Datenpaket wird durch 6 andere I2P-Knoten geleitet, bis es den Server erreicht:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
und auf dem Rückweg 6 verschiedene I2P-Knoten:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
Datenverkehr im Netzwerk benötigt eine ACK-Bestätigung, bevor neue Daten gesendet werden. Es muss gewartet werden, bis eine ACK vom Server zurückkommt: Daten senden, auf ACK warten, weitere Daten senden, auf ACK warten. Da sich die RTT (RoundTripTime) aus der Latenz jedes einzelnen I2P-Knotens und jeder Verbindung auf dieser Rundreise zusammensetzt, dauert es normalerweise 1-3 Sekunden, bis eine ACK-Bestätigung zum Client zurückkommt. Aufgrund des TCP- und I2P-Transport-Designs hat ein Datenpaket eine begrenzte Größe. Zusammen setzen diese Bedingungen eine maximale Bandbreite pro tunnel von 20-50 kByte/s fest. Wenn jedoch NUR EIN Hop im tunnel nur 5 kB/s Bandbreite zur Verfügung hat, ist der gesamte tunnel auf 5 kB/s begrenzt, unabhängig von der Latenz und anderen Einschränkungen.

Verschlüsselung, Latenz und die Art, wie ein tunnel gebaut wird, macht es ziemlich kostspielig in Bezug auf CPU-Zeit, einen tunnel zu erstellen. Deshalb darf ein Ziel nur maximal 6 IN- und 6 OUT-tunnels haben, um Daten zu transportieren. Mit maximal 50 kb/s pro tunnel könnte ein Ziel etwa 300 kb/s Datenverkehr insgesamt nutzen (in der Realität könnte es mehr sein, wenn kürzere tunnels mit geringer oder keiner Anonymität verwendet werden). Verwendete tunnels werden alle 10 Minuten verworfen und neue werden gebaut. Dieser Wechsel von tunnels und manchmal Clients, die herunterfahren oder ihre Verbindung zum Netzwerk verlieren, wird manchmal tunnels und Verbindungen unterbrechen. Ein Beispiel dafür kann im IRC2P-Netzwerk bei Verbindungsverlusten (Ping-Timeout) oder bei der Verwendung von eepget beobachtet werden.

Mit einer begrenzten Anzahl von Zielen und einer begrenzten Anzahl von tunnels pro Ziel nutzt ein I2P-Knoten nur eine begrenzte Anzahl von tunnels über andere I2P-Knoten. Wenn beispielsweise ein I2P-Knoten "hop1" im obigen kleinen Beispiel ist, sehen wir nur 1 teilnehmenden tunnel, der vom Client ausgeht. Wenn wir das gesamte I2P-Netzwerk zusammenfassen, könnte nur eine ziemlich begrenzte Anzahl von teilnehmenden tunnels mit einer begrenzten Bandbreite insgesamt aufgebaut werden. Verteilt man diese begrenzten Zahlen auf die Anzahl der I2P-Knoten, steht nur ein Bruchteil der verfügbaren Bandbreite/Kapazität zur Nutzung zur Verfügung.

Um anonym zu bleiben, sollte ein router nicht vom gesamten Netzwerk zum Aufbau von tunnels verwendet werden. Wenn ein router als tunnel router für ALLE I2P-Knoten fungiert, wird er zu einem sehr realen zentralen Ausfallpunkt sowie zu einem zentralen Punkt, um IPs und Daten von Clients zu sammeln. Deshalb verteilt das Netzwerk den Verkehr auf Knoten im tunnel-Aufbauprozess.

Eine weitere Überlegung zur Leistung ist die Art, wie I2P mit Mesh-Netzwerken umgeht. Jeder Verbindungs-Hop nutzt eine TCP- oder UDP-Verbindung auf I2P-Knoten. Bei 1000 Verbindungen sieht man 1000 TCP-Verbindungen. Das ist ziemlich viel, und einige Heim- und kleine Büro-router erlauben nur eine geringe Anzahl von Verbindungen. I2P versucht, diese Verbindungen auf unter 1500 pro UDP- und pro TCP-Typ zu begrenzen. Dies begrenzt auch die Menge des Datenverkehrs, der über einen I2P-Knoten geleitet wird.

Wenn ein Knoten erreichbar ist und eine Bandbreiteneinstellung von >128 kbyte/sec geteilt hat und 24/7 erreichbar ist, sollte er nach einiger Zeit für den Durchgangsverkehr verwendet werden. Wenn er zwischenzeitlich ausfällt, werden die Tests eines I2P-Knotens durch andere Knoten diesen als nicht erreichbar melden. Dies blockiert einen Knoten für mindestens 24 Stunden auf anderen Knoten. Die anderen Knoten, die diesen Knoten als ausgefallen getestet haben, werden diesen Knoten also 24 Stunden lang nicht zum Aufbau von tunnels verwenden. Deshalb ist Ihr Verkehr nach einem Neustart/Herunterfahren Ihres I2P routers für mindestens 24 Stunden geringer.

Zusätzlich müssen andere I2P-Knoten einen I2P router kennen, um ihn auf Erreichbarkeit und Kapazität zu testen. Dieser Prozess kann beschleunigt werden, wenn Sie mit dem Netzwerk interagieren, beispielsweise durch die Nutzung von Anwendungen oder den Besuch von I2P-Seiten, was zu mehr tunnel-Aufbau und damit zu mehr Aktivität und Erreichbarkeit für Tests durch Knoten im Netzwerk führt.

---

## Leistungsverbesserungen

Für mögliche zukünftige Leistungsverbesserungen siehe [Zukünftige Leistungsverbesserungen](/docs/overview/performance#future).

Für vergangene Leistungsverbesserungen siehe die [Leistungshistorie](/docs/overview/performance#history).
