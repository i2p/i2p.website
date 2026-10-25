---
title: "Peer-Profilerstellung und -Auswahl"
description: "Wie I2P router Peers profilieren und für den Aufbau von tunnels auswählen"
slug: "peer-selection"
aliases:
  - "/de/how_peerselection"
  - "/de/how_peerselection/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## Hinweis

Diese Seite beschreibt die Java-I2P-Implementierung der Peer-Profilerstellung und -auswahl aus dem Jahr 2010. Obwohl sie noch weitgehend zutreffend ist, sind einige Details möglicherweise nicht mehr korrekt. Wir entwickeln die Strategien für Sperren, Blockierungen und Auswahl weiter, um neuere Bedrohungen, Angriffe und Netzwerkbedingungen zu bewältigen. Das aktuelle Netzwerk hat mehrere router-Implementierungen mit verschiedenen Versionen. Andere I2P-Implementierungen können völlig andere Profilerstellungs- und Auswahlstrategien haben oder überhaupt keine Profilerstellung verwenden.

## Übersicht {#overview}

### Peer-Profilerstellung {#profiling}

**Peer Profiling** ist der Prozess des Sammelns von Daten basierend auf der **beobachteten** Leistung anderer router oder Peers und der Klassifizierung dieser Peers in Gruppen. Profiling verwendet **keine** von dem Peer selbst veröffentlichten Leistungsdaten in der [Netzwerkdatenbank](/docs/overview/network-database).

Profile werden für zwei Zwecke verwendet:

1. Auswahl von Peers, über die unser Datenverkehr weitergeleitet wird, was unten besprochen wird
2. Auswahl von Peers aus der Gruppe der floodfill router für die Speicherung und Abfragen der Netzwerkdatenbank,
   was auf der Seite zur [Netzwerkdatenbank](/docs/overview/network-database) besprochen wird

### Peer-Auswahl {#selection}

**Peer-Auswahl** ist der Prozess der Auswahl, welche router im Netzwerk wir nutzen möchten, um unsere Nachrichten weiterzuleiten (welche Peers werden wir bitten, unseren tunnels beizutreten). Um dies zu erreichen, verfolgen wir, wie jeder Peer abschneidet (das "Profil" des Peers) und verwenden diese Daten, um zu schätzen, wie schnell sie sind, wie oft sie unsere Anfragen annehmen können und ob sie überlastet oder anderweitig nicht in der Lage zu sein scheinen, das, womit sie einverstanden sind, zuverlässig auszuführen.

Anders als bei einigen anderen anonymen Netzwerken ist die angegebene Bandbreite in I2P nicht vertrauenswürdig und wird **nur** dazu verwendet, Peers zu vermeiden, die sehr niedrige, für das Routing von tunnels unzureichende Bandbreite bewerben. Die gesamte Peer-Auswahl erfolgt durch Profilerstellung. Dies verhindert einfache Angriffe, bei denen Peers hohe Bandbreite beanspruchen, um große Mengen von tunnels zu erfassen. Es macht auch [Timing-Angriffe](/docs/overview/threat-model#timing) schwieriger.

Die Peer-Auswahl erfolgt sehr häufig, da ein router eine große Anzahl von Client- und explorativen tunnels unterhalten kann, und die Lebensdauer eines tunnels nur 10 Minuten beträgt.

### Weitere Informationen {#further-info}

Für weitere Informationen siehe das Papier [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf), das auf der [PET-CON 2009.1](http://web.archive.org/web/20100413184504/http://www.pet-con.org/index.php/PET_Convention_2009.1) präsentiert wurde. Siehe [unten](#notes) für Hinweise zu kleineren Änderungen seit der Veröffentlichung des Papiers.

## Profile {#profiles}

Jeder Peer hat eine Reihe von Datenpunkten, die über ihn gesammelt werden, einschließlich Statistiken darüber, wie lange er braucht, um auf eine netDb-Abfrage zu antworten, wie oft seine tunnel fehlschlagen und wie viele neue Peers er uns vorstellen kann, sowie einfache Datenpunkte wie wann wir zuletzt von ihm gehört haben oder wann der letzte Kommunikationsfehler aufgetreten ist.

Profile sind relativ klein, nur wenige KB. Um den Speicherverbrauch zu kontrollieren, verringert sich die Ablaufzeit der Profile, je mehr Profile vorhanden sind. Profile werden bis zum Herunterfahren des router im Speicher gehalten und dann auf die Festplatte geschrieben. Beim Start werden die Profile gelesen, sodass der router nicht alle Profile neu initialisieren muss, wodurch sich ein router nach dem Start schnell wieder in das Netzwerk integrieren kann.

## Peer-Zusammenfassungen {#summaries}

Während die Profile selbst als Zusammenfassung der Leistung eines Peers betrachtet werden können, unterteilen wir jede Zusammenfassung in vier einfache Werte, um eine effektive Peer-Auswahl zu ermöglichen. Diese Werte repräsentieren die Geschwindigkeit des Peers, seine Kapazität, wie gut er in das Netzwerk integriert ist und ob er ausfällt.

### Geschwindigkeit {#speed}

Die Geschwindigkeitsberechnung geht einfach durch das Profil und schätzt, wie viele Daten wir über einen einzelnen tunnel durch den Peer in einer Minute senden oder empfangen können. Für diese Schätzung betrachtet sie nur die Leistung der vorherigen Minute.

### Kapazität {#capacity}

Die Kapazitätsberechnung geht einfach durch das Profil und schätzt, wie viele tunnel der Peer bereit wäre, in einem bestimmten Zeitraum zu unterstützen. Für diese Schätzung betrachtet sie, wie viele tunnel-Build-Anfragen der Peer akzeptiert, abgelehnt und verworfen hat, und wie viele der zugesagten tunnel später fehlgeschlagen sind. Während die Berechnung zeitgewichtet ist, sodass jüngere Aktivitäten mehr zählen als spätere Aktivitäten, können Statistiken bis zu 48 Stunden alt einbezogen werden.

Das Erkennen und Vermeiden unzuverlässiger und nicht erreichbarer Peers ist von entscheidender Bedeutung. Da der tunnel-Aufbau und -Test die Beteiligung mehrerer Peers erfordern, ist es leider schwierig, die Ursache einer abgebrochenen Build-Anfrage oder eines Testfehlers eindeutig zu identifizieren. Der router weist jedem Peer eine Ausfallwahrscheinlichkeit zu und verwendet diese Wahrscheinlichkeit bei der Kapazitätsberechnung. Abbrüche und Testfehler werden viel höher gewichtet als Ablehnungen.

## Peer-Organisation {#organization}

Wie oben erwähnt, durchleuchten wir das Profil jedes Peers, um einige wichtige Berechnungen anzustellen, und basierend darauf ordnen wir jeden Peer in drei Gruppen ein - schnell, hohe Kapazität und standard.

Die Gruppierungen schließen sich nicht gegenseitig aus, noch sind sie unabhängig voneinander:

- Ein Peer wird als "high capacity" (hohe Kapazität) betrachtet, wenn seine Kapazitätsberechnung dem Median aller Peers entspricht oder diesen überschreitet.
- Ein Peer wird als "fast" (schnell) betrachtet, wenn er bereits "high capacity" ist und seine Geschwindigkeitsberechnung dem Median aller Peers entspricht oder diesen überschreitet.
- Ein Peer wird als "standard" betrachtet, wenn er nicht "high capacity" ist

### Gruppengröße-Limits {#group-limits}

Die Größe der Gruppen kann begrenzt sein.

- Die schnelle Gruppe ist auf 30 Peers begrenzt.
  Falls es mehr gäbe, werden nur die mit der höchsten Geschwindigkeitsbewertung in die Gruppe aufgenommen.
- Die Gruppe mit hoher Kapazität ist auf 75 Peers begrenzt (einschließlich der schnellen Gruppe).
  Falls es mehr gäbe, werden nur die mit der höchsten Kapazitätsbewertung in die Gruppe aufgenommen.
- Die Standardgruppe hat keine feste Begrenzung, ist aber etwas kleiner als die Anzahl der RouterInfos,
  die in der lokalen Netzwerkdatenbank gespeichert sind.
  Bei einem aktiven router im heutigen Netzwerk können etwa 1000 RouterInfos und 500 Peer-Profile
  (einschließlich derer in den schnellen und hochkapazitiven Gruppen) vorhanden sein.

## Neuberechnung und Stabilität {#recalculation}

Zusammenfassungen werden neu berechnet und Peers werden alle 45 Sekunden in Gruppen neu sortiert.

Die Gruppen sind in der Regel ziemlich stabil, das heißt, es gibt nicht viel "Fluktuation" in den Rangfolgen bei jeder Neuberechnung. Peers in den schnellen und hochkapazitiven Gruppen bekommen mehr Tunnel durch sich hindurch gebaut, was ihre Geschwindigkeits- und Kapazitätsbewertungen erhöht, wodurch ihre Präsenz in der Gruppe verstärkt wird.

## Peer-Auswahl {#peer-selection}

Der router wählt Peers aus den oben genannten Gruppen aus, um tunnels durch sie zu erstellen.

### Peer-Auswahl für Client-Tunnels {#client-tunnels}

Client-Tunnel werden für Anwendungsverkehr verwendet, beispielsweise für HTTP-Proxys und Webserver.

Um die Anfälligkeit für [einige Angriffe](http://blog.torproject.org/blog/one-cell-enough) zu reduzieren und die Leistung zu steigern, werden Peers für den Aufbau von Client-tunnels zufällig aus der kleinsten Gruppe ausgewählt, welche die "schnelle" Gruppe ist. Es gibt keine Bevorzugung bei der Auswahl von Peers, die zuvor bereits an einem tunnel für denselben Client beteiligt waren.

### Peer-Auswahl für Erkundungs-Tunnels {#exploratory-tunnels}

Exploratory tunnels werden für administrative router-Zwecke verwendet, wie z.B. für den Verkehr der Netzwerkdatenbank und zum Testen von Client-tunnels. Exploratory tunnels werden auch verwendet, um zuvor nicht verbundene router zu kontaktieren, weshalb sie "exploratory" genannt werden. Diese tunnels haben normalerweise eine geringe Bandbreite.

Peers für den Bau von explorativen tunneln werden im Allgemeinen zufällig aus der Standardgruppe ausgewählt. Wenn die Erfolgsrate dieser Bauversuche im Vergleich zur Erfolgsrate beim Bau von Client-tunneln niedrig ist, wählt der router stattdessen einen gewichteten Durchschnitt von Peers zufällig aus der Hochkapazitätsgruppe aus. Dies hilft dabei, eine zufriedenstellende Bauerfolgsrate aufrechtzuerhalten, selbst wenn die Netzwerkleistung schlecht ist. Es gibt keine Voreingenommenheit bei der Auswahl von Peers, die zuvor Teilnehmer in einem explorativen tunnel waren.

Da die Standardgruppe eine sehr große Teilmenge aller Peers umfasst, die der router kennt, werden explorative tunnel im Wesentlichen durch eine zufällige Auswahl aller Peers gebaut, bis die Erfolgsrate beim Bau zu niedrig wird.

### Beschränkungen {#restrictions}

Um einige einfache Angriffe zu verhindern und aus Leistungsgründen gelten die folgenden Einschränkungen:

- Zwei Peers aus dem gleichen /16 IP-Bereich dürfen nicht im selben tunnel sein.
- Ein Peer darf maximal an 33% aller vom router erstellten tunnel teilnehmen.
- Peers mit extrem geringer Bandbreite werden nicht verwendet.
- Peers, bei denen ein kürzlicher Verbindungsversuch fehlgeschlagen ist, werden nicht verwendet.

### Peer-Reihenfolge in Tunnels {#ordering}

Peers werden innerhalb von tunnels angeordnet, um mit dem [predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 Update](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)) umzugehen. Weitere Informationen finden sich auf der [tunnel-Seite](/docs/specs/tunnel-implementation#ordering).

## Zukünftige Arbeiten {#future}

- Weiterhin Geschwindigkeits- und Kapazitätsberechnungen nach Bedarf analysieren und optimieren
- Falls erforderlich eine aggressivere Ausschluss-Strategie implementieren, um die Speichernutzung bei wachsendem Netzwerk zu kontrollieren
- Gruppengröße-Limits evaluieren
- GeoIP-Daten verwenden, um bestimmte Peers ein- oder auszuschließen, falls konfiguriert

## Hinweise {#notes}

Für diejenigen, die das Papier [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf) lesen, beachten Sie bitte die folgenden geringfügigen Änderungen in I2P seit der Veröffentlichung des Papiers:

- Die Integration-Berechnung wird immer noch nicht verwendet
- Im Paper werden "groups" als "tiers" bezeichnet
- Der "Failing" tier wird nicht mehr verwendet
- Der "Not Failing" tier heißt jetzt "Standard"

## Referenzen {#references}

- [Peer Profiling and Selection in the I2P Anonymous Network](/pdf/I2P-PET-CON-2009.1.pdf)
- [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)
- [Tor Entry Guards](https://wiki.torproject.org/noreply/TheOnionRouter/TorFAQ#EntryGuards)
- [Murdoch 2007 Paper](http://freehaven.net/anonbib/#murdoch-pet2007)
- [Tune-up for Tor](http://www.crhc.uiuc.edu/~nikita/papers/tuneup-cr.pdf)
- [Low-resource Routing Attacks Against Tor](http://cs.gmu.edu/~mccoy/papers/wpes25-bauer.pdf)
