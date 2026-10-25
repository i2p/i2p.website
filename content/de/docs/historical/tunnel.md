---
title: "Tunnel-Diskussion"
description: "Historische Erkundung von tunnel-Padding, Fragmentierung und Build-Strategien"
slug: "tunnel"
aliases:
  - "/de/docs/discussions/tunnel"
  - "/de/docs/discussions/tunnel/"
  - "/de/tunnel_discussion"
  - "/de/tunnel_discussion/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Hinweis: Dieses Dokument enthält ältere Informationen über Alternativen zur aktuellen tunnel-Implementierung in I2P und Spekulationen über zukünftige Möglichkeiten. Für aktuelle Informationen siehe [die tunnel-Seite](/docs/specs/tunnel-implementation).

Diese Seite dokumentiert die aktuelle tunnel Build-Implementierung ab Release 0.6.1.10. Die ältere tunnel Build-Methode, die vor Release 0.6.1.10 verwendet wurde, ist auf [der alten tunnel-Seite](/docs/historical/tunnel-alt) dokumentiert.

### Konfigurationsalternativen {#config}

Neben ihrer Länge kann es zusätzliche konfigurierbare Parameter für jeden tunnel geben, die verwendet werden können, wie etwa eine Drosselung der Häufigkeit zugestellter Nachrichten, wie Padding verwendet werden soll, wie lange ein tunnel in Betrieb sein soll, ob Chaff-Nachrichten injiziert werden sollen und welche Batching-Strategien, falls vorhanden, eingesetzt werden sollen. Keiner davon ist derzeit implementiert.

### Padding-Alternativen {#tunnel.padding}

Verschiedene Tunnel-Padding-Strategien sind möglich, jede mit ihren eigenen Vorteilen:

- Kein Padding
- Padding auf eine zufällige Größe
- Padding auf eine feste Größe
- Padding auf das nächste KB
- Padding auf die nächste exponentielle Größe (2^n Bytes)

Diese Padding-Strategien können auf verschiedenen Ebenen eingesetzt werden, um die Preisgabe von Nachrichtengrößeninformationen gegenüber verschiedenen Angreifern zu verhindern. Nach der Sammlung und Überprüfung einiger Statistiken aus dem 0.4-Netzwerk sowie der Untersuchung der Anonymitäts-Kompromisse beginnen wir mit einer festen tunnel-Nachrichtengröße von 1024 Bytes. Innerhalb dieser werden jedoch die fragmentierten Nachrichten selbst vom tunnel überhaupt nicht gepaddet (obwohl sie bei End-to-End-Nachrichten als Teil der garlic-Verpackung gepaddet werden können).

### Fragmentierungsalternativen {#tunnel.fragmentation}

Um zu verhindern, dass Angreifer die Nachrichten entlang des Pfades durch Anpassung der Nachrichtengröße markieren können, haben alle tunnel-Nachrichten eine feste Größe von 1024 Bytes. Um größere I2NP-Nachrichten zu unterstützen und kleinere effizienter zu handhaben, teilt das Gateway größere I2NP-Nachrichten in Fragmente auf, die in jeder tunnel-Nachricht enthalten sind. Der Endpunkt wird versuchen, die I2NP-Nachricht für eine kurze Zeit aus den Fragmenten zu rekonstruieren, verwirft sie aber bei Bedarf.

Router haben viel Spielraum bei der Anordnung der Fragmente, ob sie ineffizient als diskrete Einheiten verpackt, für einen kurzen Zeitraum gebündelt werden, um mehr Nutzdaten in die 1024-Byte-Tunnel-Nachrichten zu packen, oder opportunistisch mit anderen Nachrichten aufgefüllt werden, die das Gateway senden wollte.

### Weitere Alternativen {#tunnel.alternatives}

#### Tunnel-Verarbeitung während des Betriebs anpassen {#tunnel.reroute}

Während der einfache Tunnel-Routing-Algorithmus für die meisten Fälle ausreichend sein sollte, gibt es drei Alternativen, die erforscht werden können:

- Einen anderen Peer als den Endpunkt vorübergehend als Terminierungspunkt für einen tunnel fungieren lassen, indem die am Gateway verwendete Verschlüsselung angepasst wird, um ihnen den Klartext der vorverarbeiteten I2NP-Nachrichten zu geben. Jeder Peer könnte prüfen, ob er den Klartext hat, und die Nachricht beim Empfang verarbeiten, als ob er ihn hätte.
- Routern, die an einem tunnel teilnehmen, erlauben, die Nachricht vor der Weiterleitung zu remixen - sie über einen der eigenen ausgehenden tunnels dieses Peers zu leiten, mit Anweisungen für die Zustellung an den nächsten Hop.
- Code implementieren, damit der tunnel-Ersteller den "nächsten Hop" eines Peers im tunnel neu definieren kann, was weitere dynamische Umleitungen ermöglicht.

#### Bidirektionale Tunnel verwenden {#tunnel.bidirectional}

Die aktuelle Strategie, zwei separate tunnel für eingehende und ausgehende Kommunikation zu verwenden, ist nicht die einzige verfügbare Technik und hat Auswirkungen auf die Anonymität. Auf der positiven Seite verringert die Verwendung separater tunnel die für Analysen durch tunnel-Teilnehmer zugänglichen Verkehrsdaten - beispielsweise würden Peers in einem ausgehenden tunnel von einem Webbrowser nur den Verkehr eines HTTP GET sehen, während die Peers in einem eingehenden tunnel die über den tunnel übermittelte Nutzlast sehen würden. Bei bidirektionalen tunneln hätten alle Teilnehmer Zugang zu der Tatsache, dass z.B. 1KB in eine Richtung gesendet wurde, dann 100KB in die andere. Auf der negativen Seite bedeutet die Verwendung unidirektionaler tunnel, dass es zwei Gruppen von Peers gibt, die profiliert und berücksichtigt werden müssen, und zusätzliche Sorgfalt ist erforderlich, um die erhöhte Geschwindigkeit von Predecessor-Angriffen zu adressieren. Der unten beschriebene tunnel-Pooling- und Aufbauprozess sollte die Sorgen bezüglich des Predecessor-Angriffs minimieren, obwohl es, falls gewünscht, nicht viel Aufwand wäre, sowohl die eingehenden als auch die ausgehenden tunnel entlang derselben Peers aufzubauen.

#### Backchannel-Kommunikation {#tunnel.backchannel}

Derzeit werden als IV-Werte zufällige Werte verwendet. Es ist jedoch möglich, dass dieser 16-Byte-Wert dazu verwendet wird, Kontrollnachrichten vom Gateway zum Endpunkt zu senden, oder bei ausgehenden tunneln, vom Gateway zu einem der Peers. Das eingehende Gateway könnte bestimmte Werte einmal im IV kodieren, welche der Endpunkt wiederherstellen könnte (da er weiß, dass der Endpunkt auch der Ersteller ist). Für ausgehende tunnel könnte der Ersteller bestimmte Werte an die Teilnehmer während der Tunnel-Erstellung liefern (z.B. "wenn du 0x0 als IV siehst, bedeutet das X", "0x1 bedeutet Y", usw.). Da das Gateway auf dem ausgehenden tunnel auch der Ersteller ist, können sie einen IV erstellen, sodass jeder der Peers den korrekten Wert erhält. Der tunnel-Ersteller könnte sogar dem eingehenden tunnel-Gateway eine Reihe von IV-Werten geben, welche dieses Gateway verwenden könnte, um genau einmal mit einzelnen Teilnehmern zu kommunizieren (obwohl dies Probleme bezüglich der Kollisionserkennung hätte).

Diese Technik könnte später verwendet werden, um Nachrichten während der Übertragung zu übermitteln oder um dem inbound gateway zu ermöglichen, dem Endpunkt mitzuteilen, dass er einem DoS-Angriff ausgesetzt ist oder anderweitig kurz vor dem Ausfall steht. Zum jetzigen Zeitpunkt gibt es keine Pläne, diesen Rückkanal zu nutzen.

#### Variable Größe Tunnel-Nachrichten {#tunnel.variablesize}

Während die Transportschicht ihre eigene feste oder variable Nachrichtengröße haben kann und dabei ihre eigene Fragmentierung verwendet, kann die tunnel-Schicht stattdessen tunnel-Nachrichten mit variabler Größe verwenden. Der Unterschied ist eine Frage der Bedrohungsmodelle - eine feste Größe auf der Transportschicht hilft dabei, die Informationen zu reduzieren, die externen Angreifern preisgegeben werden (obwohl die allgemeine Flussanalyse dennoch funktioniert), aber für interne Angreifer (also tunnel-Teilnehmer) ist die Nachrichtengröße sichtbar. tunnel-Nachrichten mit fester Größe helfen dabei, die Informationen zu reduzieren, die tunnel-Teilnehmern preisgegeben werden, verstecken aber nicht die Informationen, die tunnel-Endpunkten und Gateways preisgegeben werden. Ende-zu-Ende-Nachrichten mit fester Größe verstecken die Informationen, die allen Peers im Netzwerk preisgegeben werden.

Wie immer ist es eine Frage, gegen wen I2P zu schützen versucht. Tunnel-Nachrichten mit variabler Größe sind gefährlich, da sie es Teilnehmern ermöglichen, die Nachrichtengröße selbst als Rückkanal zu anderen Teilnehmern zu nutzen - z.B. wenn Sie eine 1337-Byte-Nachricht sehen, befinden Sie sich im selben tunnel wie ein anderer kollaborierender Peer. Selbst mit einer festen Menge erlaubter Größen (1024, 2048, 4096, etc.) existiert dieser Rückkanal weiterhin, da Peers die Häufigkeit jeder Größe als Träger verwenden könnten (z.B. zwei 1024-Byte-Nachrichten gefolgt von einer 8192). Kleinere Nachrichten verursachen zwar den Overhead der Header (IV, tunnel-ID, Hash-Anteil, etc.), aber größere Nachrichten mit fester Größe erhöhen entweder die Latenz (aufgrund von Batching) oder dramatisch den Overhead (aufgrund von Padding). Fragmentierung hilft dabei, den Overhead zu amortisieren, allerdings auf Kosten potentieller Nachrichtenverluste durch verlorene Fragmente.

Timing-Angriffe sind auch relevant bei der Bewertung der Wirksamkeit von Nachrichten mit fester Größe, obwohl sie eine umfassende Sicht auf Netzwerkaktivitätsmuster erfordern, um wirksam zu sein. Übermäßige künstliche Verzögerungen im tunnel werden vom tunnel-Ersteller aufgrund regelmäßiger Tests erkannt, was dazu führt, dass der gesamte tunnel verworfen und die Profile für Peers innerhalb desselben angepasst werden.

### Bauende Alternativen {#tunnel.building.alternatives}

Referenz: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

#### Alte Tunnel-Baumethode {#tunnel.building.old}

Die alte Methode zum Aufbau von Tunneln, die vor Version 0.6.1.10 verwendet wurde, ist auf [der alten Tunnel-Seite](/docs/historical/tunnel-alt) dokumentiert. Dies war eine "alles auf einmal" oder "parallele" Methode, bei der Nachrichten parallel an alle Teilnehmer gesendet wurden.

#### Einmaliger Teleskopischer Aufbau {#tunnel.building.oneshot}

HINWEIS: Dies ist die aktuelle Methode.

Eine Frage, die bezüglich der Verwendung der explorativen tunnel für das Senden und Empfangen von Tunnel-Erstellungsnachrichten aufkam, ist, wie sich dies auf die Anfälligkeit des tunnels für Vorgänger-Angriffe auswirkt. Während die Endpunkte und Gateways dieser tunnel zufällig im Netzwerk verteilt sind (möglicherweise sogar einschließlich des Tunnel-Erstellers in diesem Set), ist eine andere Alternative, die Tunnel-Pfade selbst zu verwenden, um die Anfrage und Antwort weiterzuleiten, wie es in [Tor](https://www.torproject.org/) gemacht wird. Dies kann jedoch zu Lecks während der Tunnel-Erstellung führen, wodurch Peers entdecken können, wie viele Hops sich später im tunnel befinden, indem sie das Timing oder die Paketanzahl während des Tunnel-Aufbaus überwachen.

#### "Interaktives" Teleskopisches Bauen {#tunnel.building.telescoping}

Baue die Hops einzeln nacheinander auf, mit einer Nachricht durch den bestehenden Teil des Tunnels für jeden. Hat große Probleme, da die Peers die Nachrichten zählen können, um ihre Position im Tunnel zu bestimmen.

#### Nicht-explorative Tunnel für die Verwaltung {#tunnel.building.nonexploratory}

Eine zweite Alternative zum tunnel-Erstellungsprozess besteht darin, dem router einen zusätzlichen Satz von nicht-explorativen eingehenden und ausgehenden Pools zu geben, die für die tunnel-Anfrage und -Antwort verwendet werden. Unter der Annahme, dass der router eine gut integrierte Sicht auf das Netzwerk hat, sollte dies nicht notwendig sein, aber wenn der router in irgendeiner Weise partitioniert war, würde die Verwendung von nicht-explorativen Pools für das tunnel-Management die Preisgabe von Informationen darüber reduzieren, welche Peers sich in der Partition des routers befinden.

#### Explorative Anfrage-Zustellung {#tunnel.building.exploratory}

Eine dritte Alternative, die bis I2P 0.6.1.10 verwendet wurde, verschlüsselt einzelne Tunnel-Anfragenachrichten per garlic encryption und übermittelt sie einzeln an die Hops, wobei sie durch explorative Tunnel übertragen werden und ihre Antwort über einen separaten explorativen Tunnel zurückkommt. Diese Strategie wurde zugunsten der oben beschriebenen aufgegeben.

#### Weitere Geschichte und Diskussion {#history}

Vor der Einführung der Variable Tunnel Build Message gab es mindestens zwei Probleme:

1. Die Größe der Nachrichten (verursacht durch ein Maximum von 8 Hops, während die typische tunnel-Länge 2 oder 3 Hops beträgt...
   und aktuelle Forschung zeigt, dass mehr als 3 Hops die Anonymität nicht verbessert);
2. Die hohe Ausfallrate beim Aufbau, insbesondere für lange (und explorative) tunnel, da alle Hops zustimmen müssen oder der tunnel verworfen wird.

Die VTBM hat #1 behoben und #2 verbessert.

Welterde hat Modifikationen der parallelen Methode vorgeschlagen, um eine Neukonfiguration zu ermöglichen. Sponge hat vorgeschlagen, 'Tokens' irgendeiner Art zu verwenden.

Jeder Student des tunnel-Baus muss die historischen Aufzeichnungen studieren, die zur aktuellen Methode führten, insbesondere die verschiedenen Anonymitätsschwachstellen, die in verschiedenen Methoden existieren können. Die Mail-Archive vom Oktober 2005 sind besonders hilfreich. Wie in [der tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation) angegeben, entstand die aktuelle Strategie während einer Diskussion in der I2P-Mailingliste zwischen Michael Rogers, Matthew Toseland (toad) und jrandom bezüglich des Predecessor-Angriffs.

#### Peer-Ordnungsalternativen {#ordering}

Eine weniger strenge Reihenfolge ist ebenfalls möglich, wodurch sichergestellt wird, dass zwar der Hop nach A B sein kann, B jedoch niemals vor A stehen darf. Weitere Konfigurationsoptionen umfassen die Möglichkeit, dass nur die Inbound-Tunnel-Gateways und Outbound-Tunnel-Endpunkte fest definiert oder basierend auf einer MTBF-Rate rotiert werden.

## Mixing/Batching {#tunnel.mixing}

Welche Strategien sollten am Gateway und an jedem Hop verwendet werden, um Nachrichten zu verzögern, neu zu ordnen, umzuleiten oder zu polstern? Inwieweit sollte dies automatisch erfolgen, wie viel sollte als tunnel- oder hop-spezifische Einstellung konfiguriert werden, und wie sollte der tunnel-Ersteller (und wiederum der Benutzer) diesen Vorgang steuern? All dies bleibt unbekannt und soll für eine zukünftige Version ausgearbeitet werden.
