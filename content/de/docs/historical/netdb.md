---
title: "Diskussion zur Netzwerkdatenbank"
description: "Historische Notizen zu floodfill, Kademlia-Experimenten und zukünftiger Optimierung für die netDb"
slug: "netdb"
aliases:
  - "/de/docs/legacy/netdb"
  - "/de/docs/legacy/netdb/"
  - "/de/netdb_discussion"
  - "/de/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

HINWEIS: Das Folgende ist eine Diskussion der Geschichte der netDb-Implementierung und stellt keine aktuellen Informationen dar. Siehe [die Hauptseite der netDb](/docs/overview/network-database) für aktuelle Dokumentation.

## Verlauf {#status}

Die netDb wird mit einer einfachen Technik namens "floodfill" verteilt. Vor langer Zeit verwendete die netDb auch die Kademlia DHT als Fallback-Algorithmus. Allerdings funktionierte sie in unserer Anwendung nicht gut und wurde in Release 0.6.1.20 vollständig deaktiviert.

*(Adaptiert aus einem Beitrag von jrandom im alten Syndie, 26. Nov. 2005)*

Die floodfill netDb ist wirklich nur eine einfache und vielleicht vorübergehende Maßnahme, die den einfachstmöglichen Algorithmus verwendet - sende die Daten an einen Peer in der floodfill netDb, warte 10 Sekunden, wähle einen zufälligen Peer in der netDb aus und frage sie nach dem zu sendenden Eintrag, um dessen ordnungsgemäße Einfügung / Verteilung zu überprüfen. Wenn der Verifizierungs-Peer nicht antwortet oder sie den Eintrag nicht haben, wiederholt der Sender den Vorgang. Wenn der Peer in der floodfill netDb eine netDb-Speicherung von einem Peer erhält, der sich nicht in der floodfill netDb befindet, sendet er sie an alle Peers in der floodfill netDb.

Zu einem bestimmten Zeitpunkt war die Kademlia-Such-/Speicherfunktionalität noch vorhanden. Die Peers betrachteten die floodfill-Peers als immer „näher" zu jedem Schlüssel als jeden Peer, der nicht an der netDb teilnahm. Wir griffen auf die Kademlia-netDb zurück, wenn die floodfill-Peers aus irgendeinem Grund versagten. Allerdings wurde Kademlia dann vollständig deaktiviert (siehe unten).

In jüngerer Zeit wurde Kademlia Ende 2009 teilweise wieder eingeführt, um die Größe der netDb zu begrenzen, die jeder floodfill router speichern muss.

### Die Einführung des Floodfill-Algorithmus

Floodfill wurde in Version 0.6.0.4 eingeführt und behielt Kademlia als Backup-Algorithmus bei.

*(Adaptiert aus Beiträgen von jrandom im alten Syndie, 26. Nov. 2005)*

Wie ich oft gesagt habe, bin ich nicht besonders an eine spezifische Technologie gebunden - was für mich zählt, ist das, was Ergebnisse liefert. Während ich in den letzten Jahren an verschiedenen netDb-Ideen gearbeitet habe, haben die Probleme, mit denen wir in den letzten Wochen konfrontiert waren, einige davon auf die Spitze getrieben. Im Live-Netzwerk, mit dem netDb-Redundanzfaktor auf 4 Peers gesetzt (das bedeutet, wir senden einen Eintrag so lange an neue Peers, bis 4 davon bestätigen, dass sie ihn erhalten haben) und dem Timeout pro Peer auf das 4-fache der durchschnittlichen Antwortzeit dieses Peers gesetzt, senden wir **immer noch** im Durchschnitt an 40-60 Peers, bevor 4 den Store bestätigen. Das bedeutet, dass wir 36-56 mal so viele Nachrichten senden, wie eigentlich rausgehen sollten, wobei jede tunnels verwendet und dadurch 2-4 Links überquert. Darüber hinaus ist dieser Wert stark verzerrt, da die durchschnittliche Anzahl der Peers, an die bei einem 'fehlgeschlagenen' Store gesendet wurde (das bedeutet, weniger als 4 Leute haben die Nachricht nach 60 Sekunden des Nachrichtenversands bestätigt) im Bereich von 130-160 Peers lag.

Das ist wahnsinnig, besonders für ein Netzwerk mit vielleicht nur 250 Peers.

Die einfachste Antwort wäre zu sagen "na klar jrandom, es ist kaputt. reparier es", aber das trifft nicht ganz den Kern des Problems. Im Einklang mit einer anderen aktuellen Bemühung ist es wahrscheinlich, dass wir eine erhebliche Anzahl von Netzwerkproblemen aufgrund eingeschränkter Routen haben - Peers, die nicht mit anderen Peers kommunizieren können, oft aufgrund von NAT- oder Firewall-Problemen. Wenn beispielsweise die K Peers, die einem bestimmten netDb-Eintrag am nächsten sind, hinter einer 'eingeschränkten Route' stehen, so dass die netDb-Store-Nachricht sie erreichen könnte, aber die netDb-Lookup-Nachricht eines anderen Peers nicht, wäre dieser Eintrag im Wesentlichen unerreichbar. Wenn man diesen Gedanken etwas weiter verfolgt und die Tatsache berücksichtigt, dass einige eingeschränkte Routen mit feindlicher Absicht erstellt werden, wird klar, dass wir uns genauer mit einer langfristigen netDb-Lösung befassen müssen.

Es gibt einige Alternativen, aber zwei sind besonders erwähnenswert. Die erste besteht darin, die netDb einfach als Kademlia DHT mit einer Teilmenge des gesamten Netzwerks zu betreiben, bei der alle diese Peers extern erreichbar sind. Peers, die nicht an der netDb teilnehmen, stellen weiterhin Anfragen an diese Peers, erhalten aber keine unaufgeforderten netDb-Store- oder Lookup-Nachrichten. Die Teilnahme an der netDb wäre sowohl selbstselektiv als auch benutzerausschließend - Router würden wählen, ob sie eine Kennzeichnung in ihrer routerInfo veröffentlichen, die angibt, ob sie teilnehmen möchten, während jeder Router auswählt, welche Peers er als Teil der netDb behandeln möchte (Peers, die diese Kennzeichnung veröffentlichen, aber niemals nützliche Daten bereitstellen, würden ignoriert und somit effektiv aus der netDb ausgeschlossen).

Eine weitere Alternative ist ein Rückgriff auf die Vergangenheit, zurück zur DTSTTCPW (Do The Simplest Thing That Could Possibly Work) Mentalität - eine floodfill netDb, aber wie die obige Alternative, die nur eine Teilmenge des gesamten Netzwerks verwendet. Wenn ein Benutzer einen Eintrag in die floodfill netDb veröffentlichen möchte, sendet er ihn einfach an einen der teilnehmenden router, wartet auf eine ACK, und fragt dann 30 Sekunden später einen anderen zufälligen Teilnehmer in der floodfill netDb ab, um zu überprüfen, ob er ordnungsgemäß verteilt wurde. Wenn ja, großartig, und wenn nicht, einfach den Vorgang wiederholen. Wenn ein floodfill router einen netDb store erhält, bestätigt er sofort mit ACK und reiht den netDb store für alle seine bekannten netDb peers in die Warteschlange ein. Wenn ein floodfill router eine netDb lookup erhält, antwortet er mit den Daten, falls er sie hat, aber wenn nicht, antwortet er mit den Hashes für, sagen wir, 20 andere peers in der floodfill netDb.

Aus netzwerkökonomischer Sicht betrachtet ist die floodfill netDb der ursprünglichen broadcast netDb sehr ähnlich, außer dass die Kosten für die Veröffentlichung eines Eintrags hauptsächlich von den Peers in der netDb getragen werden und nicht vom Herausgeber. Wenn wir das etwas weiter ausführen und die netDb wie eine Blackbox behandeln, können wir sehen, dass die gesamte von der netDb benötigte Bandbreite folgende ist:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
wobei:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Ein paar Werte einsetzen:

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Das wiederum skaliert linear mit N (bei 100.000 Peers muss die netDb in der Lage sein, netDb Store-Nachrichten mit insgesamt 2,5 MBps zu verarbeiten, oder bei 300 Peers 7,6 KBps).

Während die floodfill netDb dazu führen würde, dass jeder netDb-Teilnehmer nur einen kleinen Bruchteil der von Clients generierten netDb-Speicherungen direkt erhält, würden sie alle Einträge schließlich erhalten, sodass alle ihre Verbindungen in der Lage sein sollten, die vollen recvKBps zu verarbeiten. Im Gegenzug müssen sie alle `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` senden, um die anderen Peers synchron zu halten.

Eine floodfill netDb würde weder tunnel routing für den netDb-Betrieb noch eine spezielle Auswahl benötigen, welche Einträge sie 'sicher' beantworten kann, da die grundlegende Annahme ist, dass sie alle alles speichern. Und was die für die netDb erforderliche Festplattenspeichernutzung angeht, ist sie für jeden modernen Rechner immer noch ziemlich trivial und erfordert etwa 11MB für jeweils 1000 Peers `(N * (L + 1) * S)`.

Die Kademlia netDb würde diese Zahlen reduzieren und sie idealerweise auf K über M mal ihren Wert bringen, wobei K = der Redundanzfaktor und M die Anzahl der router in der netDb ist (z.B. 5/100, was eine recvKBps von 126KBps und 536MB bei 100.000 routern ergibt). Der Nachteil der Kademlia netDb ist jedoch die erhöhte Komplexität des sicheren Betriebs in einer feindlichen Umgebung.

Was ich jetzt vorhabe ist einfach eine floodfill netDb in unserem bestehenden Live-Netzwerk zu implementieren und einzusetzen, damit Peers, die es nutzen wollen, andere Peers auswählen können, die als Mitglieder markiert sind, und diese abfragen können anstatt die traditionellen Kademlia netDb Peers abzufragen. Die Bandbreiten- und Festplattenspeicher-Anforderungen sind in diesem Stadium trivial genug (7,6 KBps und 3 MB Festplattenspeicher) und es wird die netDb vollständig aus dem Debugging-Plan entfernen - verbleibende Probleme, die angegangen werden müssen, werden durch etwas verursacht, das nicht mit der netDb zusammenhängt.

Wie würden Peers ausgewählt werden, um dieses Flag zu veröffentlichen, das besagt, dass sie Teil der floodfill netDb sind? Zu Beginn könnte dies manuell als erweiterte Konfigurationsoption erfolgen (wird ignoriert, wenn der router nicht in der Lage ist, seine externe Erreichbarkeit zu überprüfen). Wenn zu viele Peers dieses Flag setzen, wie wählen die netDb-Teilnehmer aus, welche sie ausschließen sollen? Auch hier könnte es zu Beginn manuell als erweiterte Konfigurationsoption erfolgen (nach dem Entfernen von Peers, die nicht erreichbar sind). Wie vermeiden wir eine Partitionierung der netDb? Indem die router überprüfen, dass die netDb das flood fill ordnungsgemäß durchführt, durch Abfragen von K zufälligen netDb-Peers. Wie entdecken router, die nicht an der netDb teilnehmen, neue router zum Tunneln? Vielleicht könnte dies durch das Senden einer bestimmten netDb-Abfrage erfolgen, sodass der netDb-router nicht mit Peers in der netDb antworten würde, sondern mit zufälligen Peers außerhalb der netDb.

I2Ps netDb unterscheidet sich stark von herkömmlichen lastragenden DHTs - sie trägt nur Netzwerk-Metadaten, keine tatsächlichen Nutzdaten, weshalb selbst eine netDb mit einem floodfill-Algorithmus eine beliebige Menge an I2P Site/IRC/bt/mail/syndie/etc.-Daten bewältigen kann. Wir können sogar einige Optimierungen vornehmen, während I2P wächst, um diese Last etwas weiter zu verteilen (möglicherweise durch das Weiterreichen von Bloom-Filtern zwischen den netDb-Teilnehmern, um zu sehen, was sie teilen müssen), aber es scheint, als könnten wir vorerst mit einer viel einfacheren Lösung auskommen.

Ein Fakt ist es wert, näher betrachtet zu werden - nicht alle leaseSets müssen in der netDb veröffentlicht werden! Tatsächlich müssen die meisten nicht veröffentlicht werden - nur diejenigen für Ziele, die unaufgeforderte Nachrichten empfangen werden (auch bekannt als Server). Das liegt daran, dass die garlic-verschlüsselten Nachrichten, die von einem Ziel zu einem anderen gesendet werden, bereits das leaseSet des Absenders bündeln, sodass jeder nachfolgende Sende-/Empfangsvorgang zwischen diesen beiden Zielen (innerhalb eines kurzen Zeitraums) ohne jegliche netDb-Aktivität funktioniert.

Also, zurück zu diesen Gleichungen: Wir können L von 5 auf etwa 0,1 ändern (unter der Annahme, dass nur 1 von 50 Zielen ein Server ist). Die vorherigen Gleichungen haben auch die Netzwerklast außer Acht gelassen, die für die Beantwortung von Client-Anfragen erforderlich ist, aber obwohl diese stark variabel ist (basierend auf der Benutzeraktivität), ist sie wahrscheinlich auch sehr unbedeutend im Vergleich zur Veröffentlichungshäufigkeit.

Trotzdem immer noch keine Zauberei, aber eine schöne Reduzierung von fast 1/5 der benötigten Bandbreite/des Speicherplatzes (vielleicht später noch mehr, je nachdem ob die routerInfo-Verteilung direkt als Teil der Peer-Etablierung oder nur über die netDb erfolgt).

### Die Deaktivierung des Kademlia-Algorithmus

Kademlia wurde in der Version 0.6.1.20 vollständig deaktiviert.

*(Adaptiert aus einer IRC-Unterhaltung mit jrandom 11/07)*

Kademlia erfordert ein Mindestmaß an Service, das die Grundausstattung nicht bieten konnte (Bandbreite, CPU), selbst nach dem Hinzufügen von Ebenen (reines Kad ist in diesem Punkt absurd). Kademlia würde einfach nicht funktionieren. Es war eine nette Idee, aber nicht für eine feindliche und instabile Umgebung.

### Aktueller Status

Die netDb spielt eine sehr spezifische Rolle im I2P-Netzwerk, und die Algorithmen wurden auf unsere Bedürfnisse abgestimmt. Das bedeutet auch, dass sie nicht für Anforderungen optimiert wurden, mit denen wir noch nicht konfrontiert waren. I2P ist derzeit ziemlich klein (einige hundert router). Es gab einige Berechnungen, dass 3-5 floodfill router in der Lage sein sollten, 10.000 Knoten im Netzwerk zu verwalten. Die netDb-Implementierung erfüllt unsere aktuellen Bedürfnisse mehr als ausreichend, aber es wird wahrscheinlich weitere Optimierungen und Fehlerbehebungen geben, wenn das Netzwerk wächst.

### Aktualisierung der Berechnungen 03-2008

Aktuelle Zahlen:

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
wobei:

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Änderungen in den Annahmen:

- L liegt jetzt bei etwa 0,5, verglichen mit 0,1 oben, aufgrund der Beliebtheit von i2psnark
  und anderen Anwendungen.
- F liegt bei etwa 0,33, aber Fehler beim tunnel-Testing sind in 0.6.1.33 behoben, also wird es sich stark verbessern.
- Da die netDb etwa 2/3 5K routerInfos und 1/3 2K leaseSets enthält, ist S = 4K.
  Die RouterInfo-Größe schrumpft in 0.6.1.32 und 0.6.1.33, da wir unnötige Statistiken entfernen.
- R = tunnel-Build-Periode: 0,2 war sehr niedrig - es lag vielleicht bei 0,7 -
  aber Verbesserungen des Build-Algorithmus in 0.6.1.32 sollten es auf etwa 0,2 senken,
  wenn das Netzwerk aktualisiert wird. Nennen wir es jetzt 0,5 mit der Hälfte des Netzwerks bei .30 oder früher.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Das berücksichtigt nur die Speicher - was ist mit den Abfragen?

### Die Rückkehr des Kademlia-Algorithmus?

*(Adaptiert aus dem I2P-Meeting vom 2. Januar 2007)*

Die Kademlia netDb hat einfach nicht richtig funktioniert. Ist sie für immer tot oder wird sie zurückkommen? Falls sie zurückkommt, wären die Peers in der Kademlia netDb eine sehr begrenzte Teilmenge der router im Netzwerk (im Grunde eine erweiterte Anzahl von floodfill Peers, falls/wenn die floodfill Peers die Last nicht bewältigen können). Aber solange die floodfill Peers die Last bewältigen können (und andere Peers hinzugefügt werden können, die es können), ist es unnötig.

### Die Zukunft von Floodfill

*(Adaptiert aus einer IRC-Unterhaltung mit jrandom 11/07)*

Hier ist ein Vorschlag: Kapazitätsklasse O ist automatisch floodfill. Hmm. Es sei denn, wir sind sicher, könnten wir am Ende mit einer ausgefallenen Art enden, alle O-Klasse router zu DDoS'en. Das ist durchaus der Fall: wir wollen sicherstellen, dass die Anzahl der floodfill so klein wie möglich ist, während ausreichende Erreichbarkeit bereitgestellt wird. Wenn/falls netDb-Anfragen fehlschlagen, dann müssen wir die Anzahl der floodfill-Peers erhöhen, aber momentan bin ich mir keines netDb-Abrufproblems bewusst. Es gibt 33 "O"-Klasse-Peers laut meinen Aufzeichnungen. 33 ist /sehr viel/ für floodfill.

Also funktioniert floodfill am besten, wenn die Anzahl der Peers in diesem Pool fest begrenzt ist? Und die Größe des floodfill-Pools sollte nicht stark wachsen, auch wenn das Netzwerk selbst allmählich wächst? 3-5 floodfill-Peers können 10K router bewältigen, wenn ich mich richtig erinnere (ich habe eine Reihe von Zahlen dazu gepostet, die die Details in der alten syndie erklären). Klingt wie eine schwer zu erfüllende Anforderung mit automatischem Opt-in, besonders wenn Knoten, die sich anmelden, Daten von anderen nicht vertrauen können. z.B. "mal sehen, ob ich unter den Top 5 bin", und können nur Daten über sich selbst vertrauen (z.B. "ich bin definitiv O-Klasse und verschiebe 150 KB/s und bin seit 123 Tagen online"). Und Top 5 ist auch feindlich. Im Grunde ist es dasselbe wie die Tor-Verzeichnisserver - ausgewählt von vertrauenswürdigen Personen (also Entwicklern). Ja, im Moment könnte es durch Opt-in ausgenutzt werden, aber das wäre trivial zu erkennen und zu behandeln. Scheint, als bräuchten wir am Ende etwas Nützlicheres als Kademlia und nur einigermaßen leistungsfähige Peers sollten diesem Schema beitreten. N-Klasse und höher sollte eine große genug Menge sein, um das Risiko zu unterdrücken, dass ein Angreifer eine Dienstverweigerung verursacht, hoffe ich. Aber es müsste sich dann von floodfill unterscheiden, in dem Sinne, dass es keinen gewaltigen Traffic verursachen würde. Große Menge? Für eine DHT-basierte netDb? Nicht unbedingt DHT-basiert.

### Floodfill TODO-Liste {#todo}

HINWEIS: Die folgenden Informationen sind nicht aktuell. Siehe [die Haupt-netDb-Seite](/docs/overview/network-database) für den aktuellen Status und eine Liste zukünftiger Arbeiten.

Das Netzwerk war am 13. März 2008 für ein paar Stunden auf nur einen floodfill reduziert (ca. 18:00 - 20:00 UTC), was viele Probleme verursachte.

Zwei Änderungen, die in 0.6.1.33 implementiert wurden, sollten die durch floodfill Peer-Entfernung oder -Wechsel verursachten Störungen reduzieren:

1. Randomisiere die floodfill-Peers, die für jede Suche verwendet werden.
   Dies wird dich schließlich an den fehlerhaften vorbeiführen.
   Diese Änderung behob auch einen bösen Bug, der manchmal den ff-Suchcode verrückt machte.
2. Bevorzuge die floodfill-Peers, die aktiv sind.
   Der Code vermeidet jetzt Peers, die auf der Sperrliste stehen, fehlschlagen oder seit einer halben Stunde nicht mehr gehört wurden, falls möglich.

Ein Vorteil ist der schnellere erste Kontakt zu einer I2P-Site (d.h. wenn Sie zuerst das leaseSet abrufen mussten). Das Lookup-Timeout beträgt 10s, wenn Sie also nicht damit beginnen, einen Peer zu fragen, der nicht erreichbar ist, können Sie 10s sparen.

Es *könnte* Anonymitätsauswirkungen bei diesen Änderungen geben. Zum Beispiel gibt es im floodfill **store** Code Kommentare, dass auf die schwarze Liste gesetzte Peers nicht vermieden werden, da ein Peer "schlecht" sein könnte und dann sehen würde, was passiert. Suchvorgänge sind viel weniger anfällig als Speicherungen - sie sind viel seltener und geben weniger preis. Also denken wir vielleicht, dass wir uns keine Sorgen machen müssen? Aber wenn wir die Änderungen anpassen möchten, wäre es einfach, trotzdem an einen Peer zu senden, der als "down" gelistet oder auf der schwarzen Liste steht, nur nicht als Teil der 2 zu zählen, an die wir senden (da wir nicht wirklich eine Antwort erwarten).

Es gibt mehrere Stellen, an denen ein floodfill Peer ausgewählt wird - diese Korrektur behandelt nur eine - von wem ein regulärer Peer sucht [2 zur gleichen Zeit]. Andere Stellen, an denen eine bessere floodfill Auswahl implementiert werden sollte:

1. An wen ein normaler Peer speichert [1 zur Zeit]
   (zufällig - muss Qualifikation hinzufügen, da Timeouts lang sind)
2. An wen ein normaler Peer sucht, um einen Speichervorgang zu verifizieren [1 zur Zeit]
   (zufällig - muss Qualifikation hinzufügen, da Timeouts lang sind)
3. Wen ein floodfill Peer als Antwort auf eine fehlgeschlagene Suche sendet (3 nächste zur Suche)
4. An wen ein floodfill Peer flutet (alle anderen floodfill Peers)
5. Die Liste der floodfill Peers, die im NTCP alle-6-Stunden "Flüstern" gesendet wird
   (obwohl dies möglicherweise nicht mehr notwendig ist aufgrund anderer floodfill Verbesserungen)

Vieles mehr könnte und sollte getan werden:

- Die "dbHistory"-Statistiken verwenden, um die Integration eines floodfill-Peers besser zu bewerten
- Die "dbHistory"-Statistiken verwenden, um sofort auf floodfill-Peers zu reagieren, die nicht antworten
- Intelligenter bei Wiederholungsversuchen sein - Wiederholungen werden von einer höheren Schicht behandelt, nicht in FloodOnlySearchJob, also macht sie eine weitere zufällige Sortierung und versucht es erneut, anstatt die floodfill-Peers, die wir gerade versucht haben, gezielt zu überspringen
- Integrationsstatistiken weiter verbessern
- Tatsächlich Integrationsstatistiken verwenden, anstatt nur floodfill-Anzeige in netDb
- Auch Latenz-Statistiken verwenden?
- Weitere Verbesserungen bei der Erkennung von fehlerhaften floodfill-Peers

Kürzlich abgeschlossen:

- [In Release 0.6.3]
  Automatisches Opt-in zu floodfill für einen bestimmten Prozentsatz von Klasse-O-Peers implementieren, basierend auf der Analyse des Netzwerks.
- [In Release 0.6.3]
  Fortsetzung der Reduzierung der netDb-Einträge, um floodfill-Traffic zu reduzieren -
  wir sind nun bei der minimalen Anzahl von Statistiken, die zur Überwachung des Netzwerks erforderlich sind.
- [In Release 0.6.3]
  Manuelle Liste von floodfill-Peers zum Ausschließen
  ([Blockierlisten](/docs/overview/threat-model#blocklist) nach router-Identität)
- [In Release 0.6.3]
  Bessere floodfill-Peer-Auswahl für Speicherungen:
  Peers vermeiden, deren netDb alt ist, oder die einen kürzlichen fehlgeschlagenen Speichervorgang hatten,
  oder die dauerhaft auf der Blacklist stehen.
- [In Release 0.6.4]
  Bereits verbundene floodfill-Peers für RouterInfo-Speicherungen bevorzugen, um
  die Anzahl direkter Verbindungen zu floodfill-Peers zu reduzieren.
- [In Release 0.6.5]
  Peers, die nicht mehr floodfill sind, senden ihre routerInfo als Antwort
  auf eine Abfrage, damit der router, der die Abfrage durchführt, weiß, dass er
  nicht mehr floodfill ist.
- [In Release 0.6.5]
  Weitere Abstimmung der Anforderungen zum automatischen Werden eines floodfill
- [In Release 0.6.5]
  Profilerstellung der Antwortzeit korrigieren, um schnelle floodfills zu bevorzugen
- [In Release 0.6.5]
  Blockierung verbessern
- [In Release 0.7]
  netDb-Erkundung korrigieren
- [In Release 0.7]
  Blockierung standardmäßig aktivieren, bekannte Störenfriede blockieren
- [Mehrere Verbesserungen in aktuellen Releases, eine kontinuierliche Anstrengung]
  Die Ressourcenanforderungen für High-Bandwidth- und floodfill-router reduzieren

Das ist eine lange Liste, aber es wird so viel Arbeit erfordern, um ein Netzwerk zu haben, das gegen DOS-Angriffe von vielen Peers resistent ist, die den floodfill-Schalter ein- und ausschalten. Oder so tun, als wären sie ein floodfill router. Nichts davon war ein Problem, als wir nur zwei ff router hatten, und beide waren 24/7 online. Wieder einmal hat jrandoms Abwesenheit uns auf Stellen hingewiesen, die Verbesserung benötigen.

Um bei diesem Vorhaben zu helfen, werden zusätzliche Profildaten für floodfill-Peers nun (seit Version 0.6.1.33) auf der "Profile"-Seite in der Router-Konsole angezeigt. Wir werden diese verwenden, um zu analysieren, welche Daten für die Bewertung von floodfill-Peers geeignet sind.

Das Netzwerk ist derzeit sehr widerstandsfähig, jedoch werden wir unsere Algorithmen zur Messung und Reaktion auf die Leistung und Zuverlässigkeit von floodfill-Peers weiter verbessern. Obwohl wir momentan noch nicht vollständig gegen die potenziellen Bedrohungen durch bösartige floodfills oder einen floodfill-DDOS gehärtet sind, ist der Großteil der Infrastruktur vorhanden, und wir sind gut positioniert, um bei Bedarf schnell zu reagieren.
