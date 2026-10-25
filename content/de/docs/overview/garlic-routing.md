---
title: "Garlic Routing"
description: "Verständnis der garlic routing Terminologie, Architektur und Implementierung in I2P"
slug: "garlic-routing"
aliases:
  - "/de/how_garlicrouting"
  - "/de/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Garlic Routing und "Garlic"-Terminologie

Die Begriffe "garlic routing" und "garlic encryption" werden oft eher ungenau verwendet, wenn auf I2Ps Technologie Bezug genommen wird. Hier erklären wir die Geschichte der Begriffe, die verschiedenen Bedeutungen und die Verwendung von "Garlic"-Methoden in I2P.

"Garlic routing" wurde erstmals von [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) in Roger Dingledines Free Haven [Master's thesis](https://www.freehaven.net/papers.html) Abschnitt 8.1.1 (Juni 2000) geprägt, abgeleitet vom [Onion Routing](https://www.onion-router.net/).

"Garlic" wurde möglicherweise ursprünglich von I2P-Entwicklern verwendet, weil I2P eine Form der Bündelung implementiert, wie Freedman sie beschreibt, oder einfach um allgemeine Unterschiede zu Tor zu betonen. Die spezifische Begründung könnte der Geschichte verloren gegangen sein. Im Allgemeinen kann der Begriff "garlic" bei der Bezugnahme auf I2P eines von drei Dingen bedeuten:

1. Schichtweise Verschlüsselung
2. Bündelung mehrerer Nachrichten
3. ElGamal/AES-Verschlüsselung

Leider war die Verwendung der "garlic"-Terminologie in I2P über die vergangenen Jahre nicht immer präzise; daher wird der Leser gewarnt, wenn er auf diesen Begriff stößt. Hoffentlich wird die folgende Erklärung die Dinge klären.

### Mehrschichtige Verschlüsselung

Onion routing ist eine Technik zum Aufbau von Pfaden oder Tunneln durch eine Reihe von Peers und zur anschließenden Nutzung dieser Tunnel. Nachrichten werden vom Absender wiederholt verschlüsselt und dann von jedem Hop entschlüsselt. Während der Aufbauphase werden jedem Peer nur die Routing-Anweisungen für den nächsten Hop preisgegeben. Während der Betriebsphase werden Nachrichten durch den Tunnel geleitet, und die Nachricht sowie ihre Routing-Anweisungen werden nur dem Endpunkt des Tunnels preisgegeben.

Dies ähnelt der Art, wie Mixmaster (siehe [Netzwerkvergleiche](/docs/overview/comparison/)) Nachrichten sendet - eine Nachricht wird genommen, mit dem öffentlichen Schlüssel des Empfängers verschlüsselt, diese verschlüsselte Nachricht wird genommen und erneut verschlüsselt (zusammen mit Anweisungen, die den nächsten Sprung spezifizieren), und dann wird diese resultierende verschlüsselte Nachricht wieder genommen und so weiter, bis sie eine Verschlüsselungsschicht pro Sprung entlang des Pfades hat.

In diesem Sinne ist "garlic routing" als allgemeines Konzept identisch mit "onion routing". Wie es in I2P implementiert ist, gibt es natürlich mehrere Unterschiede zur Implementierung in Tor; siehe unten. Dennoch gibt es wesentliche Ähnlichkeiten, sodass I2P von einer [großen Menge akademischer Forschung zu onion routing](https://www.onion-router.net/Publications.html), [Tor und ähnlichen Mixnets](https://freehaven.net/anonbib/topic.html) profitiert.

### Bündelung mehrerer Nachrichten

Michael Freedman definierte "garlic routing" als Erweiterung des onion routing, bei dem mehrere Nachrichten zusammengebündelt werden. Er nannte jede Nachricht eine "bulb" (Zwiebel). Alle Nachrichten, jede mit ihren eigenen Zustellungsanweisungen, werden am Endpunkt offengelegt. Dies ermöglicht die effiziente Bündelung eines onion routing "reply block" mit der ursprünglichen Nachricht.

Dieses Konzept ist in I2P implementiert, wie unten beschrieben. Unser Begriff für garlic "Zwiebeln" ist "Knoblauchzehen". Es können beliebig viele Nachrichten enthalten sein, anstatt nur einer einzigen Nachricht. Dies ist ein wesentlicher Unterschied zum onion routing, das in Tor implementiert ist. Es ist jedoch nur einer von vielen großen architektonischen Unterschieden zwischen I2P und Tor; vielleicht reicht es allein nicht aus, um eine Änderung der Terminologie zu rechtfertigen.

Ein weiterer Unterschied zu der von Freedman beschriebenen Methode ist, dass der Pfad unidirektional ist - es gibt keinen "Wendepunkt" wie beim Onion Routing oder bei Mixmaster-Antwortblöcken, was den Algorithmus erheblich vereinfacht und eine flexiblere und zuverlässigere Zustellung ermöglicht.

### ElGamal/AES-Verschlüsselung

In manchen Fällen kann „garlic encryption" einfach [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) Verschlüsselung (ohne mehrere Schichten) bedeuten.

---

## "Garlic"-Methoden in I2P

Nachdem wir verschiedene "Garlic"-Begriffe definiert haben, können wir sagen, dass I2P garlic routing, Bündelung und Verschlüsselung an drei Stellen verwendet:

1. Zum Aufbau und Routing durch Tunnel (geschichtete Verschlüsselung)
2. Zur Bestimmung des Erfolgs oder Misserfolgs der Ende-zu-Ende-Nachrichtenzustellung (Bündelung)
3. Zur Veröffentlichung einiger netDb-Einträge (Dämpfung der Wahrscheinlichkeit eines erfolgreichen Traffic-Analyse-Angriffs) (ElGamal/AES)

Es gibt auch bedeutende Möglichkeiten, wie diese Technik zur Verbesserung der Netzwerkleistung eingesetzt werden kann, indem Transport-Latenz/Durchsatz-Kompromisse ausgenutzt und Daten über redundante Pfade verzweigt werden, um die Zuverlässigkeit zu erhöhen.

### Tunnel-Aufbau und Routing

In I2P sind tunnels unidirektional. Jede Partei baut zwei tunnels auf, einen für ausgehenden und einen für eingehenden Verkehr. Daher werden vier tunnels für eine einzelne Hin- und Rücknachricht benötigt.

Tunnels werden mit mehrschichtiger Verschlüsselung aufgebaut und verwendet. Dies wird auf der [tunnel Implementierungsseite](/docs/specs/tunnel-implementation/) beschrieben. Wir verwenden [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) für die Verschlüsselung.

Tunnel sind ein universeller Mechanismus zum Transport aller [I2NP-Nachrichten](/docs/specs/i2np/), und Garlic Messages werden nicht zum Aufbau von Tunneln verwendet. Wir bündeln nicht mehrere I2NP-Nachrichten in eine einzige Garlic Message zum Entpacken am ausgehenden tunnel-Endpunkt; die tunnel-Verschlüsselung ist ausreichend.

### Ende-zu-Ende-Nachrichten-Bündelung

Auf der Schicht oberhalb der tunnel übermittelt I2P End-to-End-Nachrichten zwischen [Destinations](/docs/specs/common-structures/). Genau wie innerhalb eines einzelnen tunnel verwenden wir [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) für die Verschlüsselung. Jede Client-Nachricht, die über die [I2CP interface](/docs/api/i2cp/) an den router übermittelt wird, wird zu einer einzelnen Garlic Clove mit eigenen Delivery Instructions innerhalb einer Garlic Message. Delivery Instructions können eine Destination, einen Router oder einen Tunnel spezifizieren.

Im Allgemeinen enthält eine Garlic Message nur eine einzige Clove. Der Router wird jedoch regelmäßig zwei zusätzliche Cloves in die Garlic Message bündeln:

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Eine Delivery Status Message**, mit Delivery Instructions, die festlegen, dass sie als Bestätigung an den ursprünglichen router zurückgesendet wird. Dies ist ähnlich dem "reply block" oder "reply onion", die in den Referenzen beschrieben werden. Sie wird verwendet, um den Erfolg oder Misserfolg der Ende-zu-Ende-Nachrichtenzustellung zu bestimmen. Der ursprüngliche router kann beim Ausbleiben der Delivery Status Message innerhalb des erwarteten Zeitraums das Routing zur entfernten Destination ändern oder andere Maßnahmen ergreifen.

2. **Eine Database Store Message**, die ein leaseSet für die ursprüngliche Destination enthält, mit Delivery Instructions, die den Router des entfernten Endes spezifizieren. Durch das periodische Bündeln eines leaseSet stellt der Router sicher, dass das entfernte Ende in der Lage sein wird, die Kommunikation aufrechtzuerhalten. Andernfalls müsste das entfernte Ende einen floodfill-Router nach dem netDb-Eintrag abfragen, und alle leaseSets müssten in der netDb veröffentlicht werden, wie auf der [Seite zur netDb](/docs/specs/common-structures/) erklärt.

Standardmäßig werden die Delivery Status und Database Store Messages gebündelt, wenn sich das lokale LeaseSet ändert, wenn zusätzliche Session Tags übermittelt werden, oder wenn die Nachrichten in der vorherigen Minute nicht gebündelt wurden.

Offensichtlich werden die zusätzlichen Nachrichten derzeit für spezifische Zwecke gebündelt und sind nicht Teil eines allgemeinen Routing-Schemas.

Ab Release 0.9.12 wird die Delivery Status Message vom Absender in eine weitere Garlic Message eingepackt, sodass der Inhalt verschlüsselt ist und für Router auf dem Rückweg nicht sichtbar ist.

### Speicherung in der Floodfill Network Database

Wie auf der [network database Seite](/docs/specs/common-structures/) erklärt, werden lokale LeaseSets an floodfill router in einer Database Store Message gesendet, die in eine Garlic Message eingebettet ist, damit sie für das ausgehende Gateway des tunnels nicht sichtbar ist.

---

## Zukünftige Arbeiten

Der Garlic Message Mechanismus ist sehr flexibel und bietet eine Struktur zur Implementierung vieler Arten von Mixnet-Zustellmethoden. Zusammen mit der ungenutzten Verzögerungsoption in den Zustellanweisungen der Tunnel-Nachrichten ist ein breites Spektrum von Stapelverarbeitungs-, Verzögerungs-, Misch- und Routing-Strategien möglich.

Insbesondere gibt es Potenzial für viel mehr Flexibilität am Endpunkt des ausgehenden tunnels. Nachrichten könnten möglicherweise von dort zu einem von mehreren tunnels weitergeleitet werden (wodurch Punkt-zu-Punkt-Verbindungen minimiert werden), oder per Multicast an mehrere tunnels für Redundanz oder Streaming von Audio und Video gesendet werden.

Solche Experimente können mit der Notwendigkeit kollidieren, Sicherheit und Anonymität zu gewährleisten, wie etwa die Einschränkung bestimmter Routing-Pfade, die Beschränkung der Arten von I2NP-Nachrichten, die entlang verschiedener Pfade weitergeleitet werden dürfen, und die Durchsetzung bestimmter Ablaufzeiten für Nachrichten.

Als Teil der ElGamal/AES-Verschlüsselung enthält eine garlic message eine vom Absender festgelegte Menge an Füllbytes, wodurch der Absender aktive Gegenmaßnahmen gegen Verkehrsanalyse ergreifen kann. Dies wird derzeit nicht verwendet, abgesehen von der Anforderung, auf ein Vielfaches von 16 Bytes aufzufüllen.

Verschlüsselung zusätzlicher Nachrichten zu und von den [floodfill routers](/docs/specs/common-structures/).

---

## Referenzen

- Der Begriff garlic routing wurde erstmals in Roger Dingledines Free Haven [Master's thesis](https://www.freehaven.net/papers.html) (Juni 2000) geprägt, siehe Abschnitt 8.1.1 von [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/).
- [Onion Router Publications](https://www.onion-router.net/Publications.html)
- [Onion Routing (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Tor Project](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Onion routing wurde erstmals 1996 in [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) von David M. Goldschlag, Michael G. Reed und Paul F. Syverson beschrieben.
