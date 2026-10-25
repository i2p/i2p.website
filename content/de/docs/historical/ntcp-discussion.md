---
title: "NTCP Diskussion"
description: "Historische Diskussion über NTCP vs SSU Transportprotokolle von März 2007"
slug: "ntcp-discussion"
aliases:
  - "/de/docs/discussions/ntcp"
  - "/de/docs/discussions/ntcp/"
  - "/de/ntcp_discussion"
  - "/de/ntcp_discussion/"
lastUpdated: "2007-03"
accurateFor: "historical"
---

Im Folgenden ist eine Diskussion über NTCP aufgeführt, die im März 2007 stattfand. Sie wurde nicht aktualisiert, um die aktuelle Implementierung widerzuspiegeln. Für die aktuelle NTCP-Spezifikation siehe [die NTCP2-Seite](/docs/specs/ntcp2).

## NTCP vs. SSU Diskussion, März 2007 {#ntcp-ssu}

### NTCP-Fragen

(angepasst aus einer IRC-Diskussion zwischen zzz und cervantes)

Warum wird NTCP gegenüber SSU bevorzugt, hat NTCP nicht höhere Overhead- und Latenzwerte? Es hat bessere Zuverlässigkeit.

Leidet die Streaming-Bibliothek über NTCP nicht unter den klassischen TCP-über-TCP-Problemen? Was wäre, wenn wir einen wirklich einfachen UDP-Transport für von der Streaming-Bibliothek stammenden Verkehr hätten? Ich denke, SSU sollte der sogenannte wirklich einfache UDP-Transport sein - aber es erwies sich als zu unzuverlässig.

### "NTCP Considered Harmful" Analyse von zzz {#harmful}

Veröffentlicht im neuen Syndie, 25.03.2007. Dies wurde veröffentlicht, um Diskussionen anzuregen, nehmen Sie es nicht zu ernst.

**Zusammenfassung:** NTCP hat eine höhere Latenz und mehr Overhead als SSU und bricht eher zusammen, wenn es mit der streaming lib verwendet wird. Allerdings wird Traffic mit einer Präferenz für NTCP gegenüber SSU geroutet und dies ist derzeit fest kodiert.

#### Diskussion

Wir haben derzeit zwei Transports, NTCP und SSU. Wie derzeit implementiert, hat NTCP niedrigere "Gebote" als SSU und wird daher bevorzugt, außer in dem Fall, wo eine etablierte SSU-Verbindung, aber keine etablierte NTCP-Verbindung für einen Peer besteht.

SSU ist ähnlich wie NTCP, da es Bestätigungen, Timeouts und Neuübertragungen implementiert. Allerdings ist SSU I2P-Code mit strengen Beschränkungen bei den Timeouts und verfügbaren Statistiken zu Rundlaufzeiten, Neuübertragungen usw. NTCP basiert auf Java NIO TCP, welches eine Black Box ist und vermutlich RFC-Standards implementiert, einschließlich sehr langer maximaler Timeouts.

Der Großteil des Verkehrs innerhalb von I2P stammt aus streaming-lib (HTTP, IRC, Bittorrent), welches unsere Implementierung von TCP ist. Da der Transport auf niedrigerer Ebene aufgrund der niedrigeren Gebote im Allgemeinen NTCP ist, unterliegt das System dem wohlbekannten und gefürchteten Problem von TCP-over-TCP http://sites.inka.de/~W1011/devel/tcp-tcp.html , bei dem sowohl die höheren als auch die niedrigeren TCP-Schichten gleichzeitig Übertragungswiederholungen durchführen, was zum Zusammenbruch führt.

Im Gegensatz zu dem oben verlinkten PPP-über-SSH-Szenario haben wir mehrere Hops für die untere Schicht, die jeweils durch eine NTCP-Verbindung abgedeckt sind. Daher ist jede NTCP-Latenz im Allgemeinen viel geringer als die Latenz der höheren Streaming-Bibliothek. Dies verringert die Wahrscheinlichkeit eines Kollaps.

Außerdem werden die Wahrscheinlichkeiten eines Zusammenbruchs verringert, wenn das TCP der unteren Schicht streng begrenzt ist mit niedrigen Timeouts und einer geringen Anzahl von Wiederholungsübertragungen im Vergleich zur höheren Schicht.

Die .28-Version erhöhte das maximale Streaming-Lib-Timeout von 10 Sek. auf 45 Sek., was die Situation erheblich verbesserte. Das SSU-Maximum-Timeout beträgt 3 Sek. Das NTCP-Maximum-Timeout liegt vermutlich bei mindestens 60 Sek., was der RFC-Empfehlung entspricht. Es gibt keine Möglichkeit, NTCP-Parameter zu ändern oder die Leistung zu überwachen. Der Zusammenbruch der NTCP-Schicht ist [Redakteur: Text verloren]. Möglicherweise würde ein externes Tool wie tcpdump helfen.

Beim Betrieb von .28 bleibt der von i2psnark gemeldete Upstream jedoch normalerweise nicht auf einem hohen Level. Er fällt oft auf 3-4 KBps ab, bevor er wieder ansteigt. Dies ist ein Zeichen dafür, dass es immer noch zu Zusammenbrüchen kommt.

SSU ist auch effizienter. NTCP hat höhere Overhead-Kosten und wahrscheinlich höhere Round-Trip-Zeiten. Bei der Verwendung von NTCP beträgt das Verhältnis von (tunnel output) / (i2psnark data output) mindestens 3,5 : 1. Bei einem Experiment, bei dem der Code so modifiziert wurde, dass SSU bevorzugt wird (die Konfigurationsoption i2np.udp.alwaysPreferred hat im aktuellen Code keine Wirkung), reduzierte sich das Verhältnis auf etwa 3 : 1, was auf eine bessere Effizienz hinweist.

Wie von den Streaming-Lib-Statistiken berichtet, haben sich die Dinge deutlich verbessert - die Lebensdauer-Fenstergröße stieg von 6,3 auf 7,5, die RTT sank von 11,5s auf 10s, die Sendungen pro Ack sanken von 1,11 auf 1,07.

Dass dies so effektiv war, war überraschend, da wir nur den Transport für den ersten von 3 bis 5 Hops verändert hatten, die die ausgehenden Nachrichten insgesamt nehmen würden.

Die Auswirkung auf ausgehende i2psnark-Geschwindigkeiten war aufgrund normaler Schwankungen nicht eindeutig. Außerdem wurde für das Experiment eingehendes NTCP deaktiviert. Die Auswirkung auf eingehende Geschwindigkeiten bei i2psnark war nicht eindeutig.

#### Vorschläge

1. **1A)** Das ist einfach -
   Wir sollten die Bid-Prioritäten umkehren, sodass SSU für den gesamten Verkehr bevorzugt wird, falls
   wir das tun können, ohne alle möglichen anderen Probleme zu verursachen. Dies wird die
   i2np.udp.alwaysPreferred Konfigurationsoption reparieren, damit sie funktioniert (entweder als true
   oder false).

2. **1B)** Alternative zu 1A), nicht so einfach -
   Wenn wir Traffic markieren können, ohne unsere Anonymitätsziele nachteilig zu beeinflussen, sollten
   wir streaming-lib generierten Traffic identifizieren und SSU dazu bringen, ein niedriges Gebot
   für diesen Traffic zu generieren. Dieses Tag muss mit der Nachricht durch jeden Hop
   mitgehen, damit die weiterleitenden router auch die SSU-Präferenz berücksichtigen.

3. **2)** Eine weitere Begrenzung von SSU (Reduzierung der maximalen Wiederholungsversuche von den aktuellen 10) ist wahrscheinlich sinnvoll, um die Wahrscheinlichkeit eines Zusammenbruchs zu verringern.

4. **3)** Wir benötigen weitere Studien zu den Vor- und Nachteilen eines semi-zuverlässigen Protokolls
   unterhalb der Streaming-Bibliothek. Sind Neuübertragungen über einen einzelnen Hop vorteilhaft
   und ein großer Gewinn oder sind sie schlimmer als nutzlos?
   Wir könnten ein neues SUU (secure unreliable UDP) entwickeln, aber das ist wahrscheinlich nicht lohnenswert. Wir
   könnten möglicherweise einen Message-Typ ohne Bestätigungserfordernis in SSU hinzufügen, wenn wir gar keine
   Neuübertragungen für Streaming-lib-Traffic wollen. Sind eng begrenzte
   Neuübertragungen wünschenswert?

5. **4)** Der Code für priorisiertes Senden in .28 ist nur für NTCP. Bisher haben meine Tests nicht viel Nutzen für SSU-Prioritäten gezeigt, da die Nachrichten nicht lange genug in der Warteschlange stehen, damit Prioritäten etwas bewirken. Aber weitere Tests sind nötig.

6. **5)** Das neue Streaming-Lib Maximum-Timeout von 45s ist wahrscheinlich immer noch zu niedrig.
   Das TCP RFC besagt 60s. Es sollte wahrscheinlich nicht kürzer sein als das zugrunde liegende NTCP Maximum-Timeout (vermutlich 60s).

### Antwort von jrandom {#jrandom-response}

Veröffentlicht in neuem Syndie, 27.03.2007

Im Großen und Ganzen bin ich offen dafür, damit zu experimentieren, aber denken Sie daran, warum NTCP überhaupt da ist - SSU versagte bei einem Congestion Collapse. NTCP "funktioniert einfach", und während 2-10% Übertragungswiederholungsraten in normalen Single-Hop-Netzwerken bewältigt werden können, ergibt das bei uns eine 40% Übertragungswiederholungsrate bei 2-Hop-Tunneln. Wenn Sie einige der gemessenen SSU-Übertragungswiederholungsraten einbeziehen, die wir damals vor der NTCP-Implementierung sahen (10-30+%), ergibt das eine 83% Übertragungswiederholungsrate. Vielleicht wurden diese Raten durch das niedrige 10-Sekunden-Timeout verursacht, aber eine so starke Erhöhung würde uns schaden (denken Sie daran, multiplizieren Sie mit 5 und Sie haben die Hälfte der Strecke).

Im Gegensatz zu TCP haben wir kein Feedback vom tunnel, um zu wissen, ob die Nachricht angekommen ist - es gibt keine tunnel-level ACKs. Wir haben End-to-End-ACKs, aber nur für eine kleine Anzahl von Nachrichten (immer wenn wir neue Session-Tags verteilen) - von den 1.553.591 Client-Nachrichten, die mein router gesendet hat, haben wir nur bei 145.207 davon versucht, sie zu bestätigen. Die anderen könnten stillschweigend fehlgeschlagen oder perfekt erfolgreich gewesen sein.

Ich bin nicht überzeugt von dem TCP-über-TCP-Argument für uns, besonders wenn es über die verschiedenen Pfade aufgeteilt wird, über die wir übertragen. Messungen auf I2P können mich natürlich vom Gegenteil überzeugen.

> *Das NTCP maximale Zeitlimit liegt vermutlich bei mindestens 60 Sekunden, was der RFC-Empfehlung entspricht. Es gibt keine Möglichkeit, NTCP-Parameter zu ändern oder die Leistung zu überwachen.*

Das stimmt, aber Netzverbindungen erreichen dieses Niveau nur, wenn etwas wirklich Schlimmes vor sich geht - das Retransmission-Timeout bei TCP liegt oft im Bereich von zehn oder hunderten von Millisekunden. Wie foofighter darauf hinweist, haben sie über 20 Jahre Erfahrung und Fehlerbehebung in ihren TCP-Stacks, plus eine milliardenschwere Industrie, die Hardware und Software optimiert, um gut zu funktionieren, je nach dem, was sie tun.

> *NTCP hat höheren Overhead und wahrscheinlich höhere Rundlaufzeiten. Bei der Verwendung von NTCP > beträgt das Verhältnis von (tunnel output) / (i2psnark data output) mindestens 3,5 : 1. > Bei einem Experiment, bei dem der Code so modifiziert wurde, dass SSU bevorzugt wird (die Konfigurationsoption > i2np.udp.alwaysPreferred hat im aktuellen Code keine Wirkung), reduzierte sich das Verhältnis > auf etwa 3 : 1, was auf eine bessere Effizienz hinweist.*

Das sind sehr interessante Daten, allerdings eher als eine Frage der router-Überlastung denn der Bandbreiteneffizienz - man müsste 3.5*$n*$NTCPRetransmissionPct ./. 3.0*$n*$SSURetransmissionPct vergleichen. Dieser Datenpunkt deutet darauf hin, dass es etwas im router gibt, das zu übermäßiger lokaler Warteschlangenbildung von Nachrichten führt, die bereits übertragen werden.

> *Lebensdauer-Fenstergröße erhöht von 6,3 auf 7,5, RTT reduziert von 11,5s auf 10s, Sendungen pro ACK reduziert von 1,11 auf 1,07.*

Beachten Sie, dass die Sends-per-ACK nur eine Stichprobe und keine vollständige Zählung ist (da wir nicht versuchen, jeden Send zu bestätigen). Es ist auch keine zufällige Stichprobe, sondern stattdessen werden Perioden der Inaktivität oder der Beginn eines Aktivitätsschubs stärker beprobt - anhaltende Last erfordert nicht viele ACKs.

Fenstergrößen in diesem Bereich sind immer noch viel zu niedrig, um den echten Nutzen von AIMD zu erhalten, und immer noch zu niedrig, um einen einzelnen 32KB BT-Chunk zu übertragen (eine Erhöhung des Mindestwerts auf 10 oder 12 würde das abdecken).

Dennoch sieht die wsize-Statistik vielversprechend aus - über welchen Zeitraum wurde das aufrechterhalten?

Für Testzwecke sollten Sie sich eigentlich StreamSinkClient/StreamSinkServer oder sogar TestSwarm in apps/ministreaming/java/src/net/i2p/client/streaming/ ansehen - StreamSinkClient ist eine CLI-Anwendung, die eine ausgewählte Datei an ein ausgewähltes Ziel sendet, und StreamSinkServer erstellt ein Ziel und schreibt alle an es gesendeten Daten aus (zeigt Größe und Übertragungszeit an). TestSwarm kombiniert beide - überflutet jeden, mit dem es sich verbindet, mit zufälligen Daten. Das sollte Ihnen die Werkzeuge geben, um die anhaltende Durchsatzkapazität über die streaming lib zu messen, im Gegensatz zu BT choke/send.

> *1A) Das ist einfach - > Wir sollten die Bid-Prioritäten umkehren, sodass SSU für den gesamten Traffic bevorzugt wird, falls > wir das tun können, ohne alle möglichen anderen Probleme zu verursachen. Das wird die > i2np.udp.alwaysPreferred Konfigurationsoption reparieren, damit sie funktioniert (entweder als true > oder false).*

Die Berücksichtigung von i2np.udp.alwaysPreferred ist in jedem Fall eine gute Idee - bitte zögern Sie nicht, diese Änderung zu committen. Lassen Sie uns jedoch noch etwas mehr Daten sammeln, bevor wir die Präferenzen umstellen, da NTCP hinzugefügt wurde, um einen durch SSU verursachten Congestion Collapse zu bewältigen.

> *1B) Alternative zu 1A), nicht so einfach - > Wenn wir Traffic markieren können, ohne unsere Anonymitätsziele nachteilig zu beeinflussen, sollten wir > von streaming-lib generierten Traffic identifizieren > und SSU ein niedriges Gebot für diesen Traffic generieren lassen. Dieses Tag muss mit > der Nachricht durch jeden Hop mitgehen, > damit die weiterleitenden Router ebenfalls die SSU-Präferenz berücksichtigen.*

In der Praxis gibt es drei Arten von Datenverkehr - tunnel-Aufbau/-Tests, netDb-Abfrage/-Antwort und Streaming-Lib-Verkehr. Das Netzwerk wurde so entwickelt, dass es sehr schwer ist, diese drei zu unterscheiden.

> *2) Eine weitere Einschränkung von SSU (Reduzierung der maximalen Neuübertragungen von den aktuellen > 10) ist wahrscheinlich sinnvoll, um die Wahrscheinlichkeit eines Zusammenbruchs zu verringern.*

Bei 10 Neuübertragungen sind wir bereits am Arsch, da stimme ich zu. Eine, vielleicht zwei Neuübertragungen sind auf der Transportschicht angemessen, aber wenn die andere Seite zu überlastet ist, um rechtzeitig zu bestätigen (selbst mit der implementierten SACK/NACK-Funktionalität), können wir nicht viel tun.

Meiner Ansicht nach müssen wir, um das Kernproblem wirklich zu lösen, herausfinden, warum der router so überlastet wird, dass er nicht rechtzeitig ACK senden kann (was, soweit ich herausgefunden habe, auf CPU-Konflikte zurückzuführen ist). Vielleicht können wir einige Dinge in der Verarbeitung des routers umstellen, um der Übertragung über einen bereits bestehenden tunnel eine höhere CPU-Priorität zu geben als der Entschlüsselung einer neuen tunnel-Anfrage? Allerdings müssen wir aufpassen, dass wir keine Aushungerung verursachen.

> *3) Wir benötigen weitere Untersuchungen zu den Vor- und Nachteilen eines semi-zuverlässigen Protokolls > unter der Streaming-Bibliothek. Sind Neuübertragungen über einen einzigen Hop vorteilhaft > und ein großer Gewinn oder sind sie schlimmer als nutzlos? > Wir könnten ein neues SUU (secure unreliable UDP) erstellen, aber das ist wahrscheinlich nicht der Aufwand wert. Wir > könnten vielleicht einen Nachrichtentyp ohne ACK-Anforderung in SSU hinzufügen, wenn wir überhaupt keine > Neuübertragungen von Streaming-Bibliotheks-Traffic wollen. Sind streng begrenzte > Neuübertragungen wünschenswert?*

Wäre es wert zu untersuchen - was wäre, wenn wir SSU-Neuübertragungen einfach deaktivieren würden? Das würde wahrscheinlich zu viel höheren Wiederversendungsraten der Streaming-Bibliothek führen, aber vielleicht auch nicht.

> *4) Der Prioritäts-Sendecode in .28 ist nur für NTCP. Bisher haben meine Tests nicht viel Nutzen für SSU-Prioritäten gezeigt, da die Nachrichten nicht lange genug in der Warteschlange stehen, damit Prioritäten etwas bewirken können. Aber weitere Tests sind erforderlich.*

Es gibt UDPTransport.PRIORITY_LIMITS und UDPTransport.PRIORITY_WEIGHT (berücksichtigt von TimedWeightedPriorityMessageQueue), aber derzeit sind die Gewichtungen fast alle gleich, sodass es keine Auswirkung gibt. Das könnte natürlich angepasst werden (aber wie Sie erwähnen, wenn es keine Warteschlangen gibt, spielt es keine Rolle).

> *5) Das neue Streaming-Lib-Maximum-Timeout von 45s ist wahrscheinlich immer noch zu niedrig. Das TCP RFC > sagt 60s. Es sollte wahrscheinlich nicht kürzer sein als das zugrunde liegende NTCP-Maximum-Timeout > (vermutlich 60s).*

Diese 45s sind jedoch das maximale Wiederübertragungstimeout der Streaming-Bibliothek, nicht das Stream-Timeout. TCP hat in der Praxis Wiederübertragungstimeouts, die um Größenordnungen geringer sind, obwohl ja, es kann auf Verbindungen über freiliegende Kabel oder Satellitenübertragungen bis zu 60s erreichen ;) Wenn wir das Wiederübertragungstimeout der Streaming-Bibliothek auf z.B. 75 Sekunden erhöhen würden, könnten wir ein Bier holen gehen, bevor eine Webseite lädt (besonders bei weniger als 98% zuverlässigem Transport). Das ist ein Grund, warum wir NTCP bevorzugen.

### Antwort von zzz {#zzz-response}

Gepostet in neues Syndie, 2007-03-31

> *Bei 10 Wiederholungsversuchen sind wir schon ziemlich am Ende, da stimme ich zu. Ein, vielleicht zwei > Wiederholungsversuche sind vernünftig, aus Sicht der Transportschicht, aber wenn die andere Seite > zu überlastet ist, um rechtzeitig zu bestätigen (selbst mit der implementierten SACK/NACK-Fähigkeit), > können wir nicht viel machen.* > > *Meiner Ansicht nach müssen wir, um das Kernproblem wirklich anzugehen, herausfinden, warum der > router so überlastet wird, dass er nicht rechtzeitig bestätigen kann (was, soweit ich herausgefunden habe, an > CPU-Konkurrenz liegt). Vielleicht können wir einige Dinge in der Verarbeitung des routers umorganisieren, um > der Übertragung eines bereits bestehenden tunnels eine höhere CPU-Priorität zu geben als der > Entschlüsselung einer neuen tunnel-Anfrage? Allerdings müssen wir aufpassen, dass wir keine > Verdrängung verursachen.*

Eine meiner wichtigsten Techniken zur Statistiksammlung ist das Aktivieren von net.i2p.client.streaming.ConnectionPacketHandler=DEBUG und das Beobachten der RTT-Zeiten und Fenstergrößen während sie vorbeigehen. Um einen Moment zu verallgemeinern, ist es üblich, 3 Arten von Verbindungen zu sehen: ~4s RTT, ~10s RTT und ~30s RTT. Das Ziel ist es, die 30s RTT-Verbindungen zu reduzieren. Wenn CPU-Konkurrenz die Ursache ist, dann könnte etwas Jonglieren helfen.

Die Reduzierung der SSU max retrans von 10 ist wirklich nur ein Stochern im Dunkeln, da wir keine guten Daten darüber haben, ob wir kollabieren, TCP-over-TCP-Probleme haben oder was auch immer, daher werden mehr Daten benötigt.

> *Untersuchenswert - was wäre, wenn wir einfach die Wiederübertragungen von SSU deaktivieren würden? Das würde > wahrscheinlich zu viel höheren Wiedersendraten der Streaming-Bibliothek führen, aber vielleicht auch nicht.*

Was ich nicht verstehe und worüber Sie vielleicht Klarheit schaffen könnten, sind die Vorteile von SSU-Wiederholungsübertragungen für Datenverkehr außerhalb der streaming-lib. Müssen tunnel-Nachrichten (zum Beispiel) ein semi-zuverlässiges Transport verwenden oder können sie ein unzuverlässiges oder halbwegs-zuverlässiges Transport verwenden (maximal 1 oder 2 Wiederholungsübertragungen, zum Beispiel)? Mit anderen Worten, warum Semi-Zuverlässigkeit?

> *(aber wie Sie erwähnen, wenn es keine Warteschlange gibt, spielt es keine Rolle).*

Ich habe Priority-Sending für UDP implementiert, aber es wurde etwa 100.000 Mal seltener aktiviert als der Code auf der NTCP-Seite. Vielleicht ist das ein Hinweis für weitere Untersuchungen oder ein Anhaltspunkt - ich verstehe nicht, warum es bei NTCP so viel häufiger zu Staus kommen würde, aber vielleicht ist das ein Hinweis darauf, warum NTCP schlechter abschneidet.

### Frage beantwortet von jrandom {#jrandom-followup}

Veröffentlicht auf neuem Syndie, 2007-03-31

> *gemessene SSU Übertragungswiederholungsraten, die wir früher gesehen haben, bevor NTCP implementiert wurde > (10-30+%)* > > Kann der router selbst das messen? Falls ja, könnte ein Transport basierend > auf gemessener Leistung ausgewählt werden? (d.h. wenn eine SSU Verbindung zu einem Peer eine > unvernünftig hohe Anzahl von Nachrichten verliert, NTCP bevorzugen beim Senden an diesen Peer)

Ja, es verwendet derzeit diese Statistik als einfache MTU-Erkennung (wenn die Wiederübertragungsrate hoch ist, wird die kleine Paketgröße verwendet, aber wenn sie niedrig ist, wird die große Paketgröße verwendet). Wir haben ein paar Dinge ausprobiert, als wir NTCP zum ersten Mal eingeführt haben (und als wir uns zum ersten Mal vom ursprünglichen TCP-Transport wegbewegt haben), die SSU bevorzugen, aber diesen Transport für einen Peer leicht fehlschlagen lassen würden, wodurch er auf NTCP zurückfallen würde. Allerdings könnte in dieser Hinsicht sicherlich mehr getan werden, obwohl es schnell kompliziert wird (wie/wann die Gebote angepasst/zurückgesetzt werden sollen, ob diese Präferenzen zwischen mehreren Peers geteilt werden sollen oder nicht, ob sie über mehrere Sessions mit demselben Peer geteilt werden sollen (und für wie lange), usw.).

### Antwort von foofighter {#foofighter}

Veröffentlicht in neuem Syndie, 2007-03-26

Wenn ich die Sache richtig verstanden habe, war der Hauptgrund für TCP (im Allgemeinen, sowohl die alte als auch die neue Variante), dass man sich keine Gedanken über die Programmierung eines guten TCP-Stacks machen musste. Was nicht unmöglich schwer richtig hinzubekommen ist... nur dass bestehende TCP-Stacks einen 20-jährigen Vorsprung haben.

Soweit ich weiß, gab es nicht viel tiefgreifende Theorie hinter der Bevorzugung von TCP gegenüber UDP, außer den folgenden Überlegungen:

- Ein nur-TCP-Netzwerk ist sehr abhängig von erreichbaren Peers (diejenigen, die eingehende Verbindungen durch ihr NAT weiterleiten können)
- Selbst wenn erreichbare Peers selten sind, lindert es die topologischen Knappheitsprobleme etwas, wenn sie eine hohe Kapazität haben
- UDP ermöglicht "NAT hole punching", wodurch Personen "pseudo-erreichbar" werden können (mit Hilfe von Introducers), die ansonsten nur ausgehende Verbindungen herstellen könnten
- Die "alte" TCP-Transport-Implementierung benötigte viele Threads, was ein Performance-Killer war, während der "neue" TCP-Transport gut mit wenigen Threads auskommt
- Router vom Set A versagen, wenn sie mit UDP überlastet werden. Router vom Set B versagen, wenn sie mit TCP überlastet werden.
- Es "fühlt sich an" (das heißt, es gibt einige Hinweise, aber keine wissenschaftlichen Daten oder Qualitätsstatistiken), dass A weiter verbreitet ist als B
- Einige Netzwerke übertragen Nicht-DNS-UDP-Datagramme mit richtig schlechter Qualität, während sie sich immer noch die Mühe machen, TCP-Streams zu übertragen.

Vor diesem Hintergrund erscheint eine kleine Vielfalt an Transportprotokollen (so viele wie nötig, aber nicht mehr) in beiden Fällen sinnvoll. Welches das Haupttransportprotokoll sein sollte, hängt von deren Leistung ab. Ich habe schlimme Sachen auf meiner Leitung gesehen, als ich versuchte, deren volle Kapazität mit UDP zu nutzen. Paketverluste auf dem Niveau von 35%.

Wir könnten definitiv versuchen, mit UDP- versus TCP-Prioritäten zu experimentieren, aber ich würde dabei zur Vorsicht mahnen. Ich würde dringend empfehlen, dass sie nicht zu radikal auf einmal geändert werden, da dies Dinge kaputt machen könnte.

### Antwort von zzz (an foofighter) {#zzz-foofighter}

Veröffentlicht in neuem Syndie, 2007-03-27

> *Soweit ich weiß, gab es nicht viel tiefgreifende Theorie hinter der Bevorzugung von TCP gegenüber UDP, außer den folgenden Überlegungen:*

Das sind alles berechtigte Punkte. Allerdings betrachten Sie die beiden Protokolle isoliert, anstatt darüber nachzudenken, welches Transportprotokoll am besten für ein bestimmtes höherstufiges Protokoll geeignet ist (d.h. mit oder ohne Streaming-Bibliothek).

Was ich sage ist, dass Sie die Streaming-Bibliothek berücksichtigen müssen.

Entweder die Einstellungen für alle ändern oder den Traffic der Streaming-Bibliothek anders behandeln.

Das ist, wovon mein Vorschlag 1B) spricht - eine unterschiedliche Präferenz für streaming-lib-Verkehr im Vergleich zu Nicht-streaming-lib-Verkehr zu haben (zum Beispiel tunnel build messages).

> *Vor diesem Hintergrund erscheint eine geringe Vielfalt von Transportprotokollen (so viele wie nötig, aber > nicht mehr) in beiden Fällen sinnvoll. Welches das Haupttransportprotokoll sein sollte, > hängt von deren Leistung ab. Ich habe böse Sachen auf meiner Leitung gesehen, als ich > versucht habe, deren volle Kapazität mit UDP zu nutzen. Paketverluste von 35%.*

Stimmt. Die neue Version .28 könnte die Dinge bei Paketverlust über UDP verbessert haben, oder vielleicht auch nicht.

Ein wichtiger Punkt - der Transport-Code merkt sich Ausfälle eines Transports. Wenn also UDP der bevorzugte Transport ist, wird er zuerst versucht, aber falls er für ein bestimmtes Ziel fehlschlägt, wird beim nächsten Versuch für dieses Ziel NTCP versucht, anstatt UDP erneut zu versuchen.

> *Wir könnten definitiv versuchen, mit UDP- versus TCP-Prioritäten zu experimentieren, aber ich würde dabei zur Vorsicht raten. Ich würde dringend empfehlen, sie nicht zu radikal auf einmal zu ändern, da dies Dinge kaputt machen könnte.*

Wir haben vier Einstellmöglichkeiten - die vier Gebotswerte (SSU und NTCP, für bereits verbundene und noch nicht verbundene). Wir könnten zum Beispiel SSU gegenüber NTCP nur dann bevorzugen, wenn beide verbunden sind, aber NTCP zuerst versuchen, wenn keiner der beiden Transporte verbunden ist.

Der andere Weg, es schrittweise zu machen, ist nur den Streaming-Lib-Verkehr zu verlagern (der 1B-Vorschlag), jedoch könnte das schwierig sein und Auswirkungen auf die Anonymität haben, das weiß ich nicht. Oder vielleicht den Verkehr nur für den ersten ausgehenden Hop verlagern (d.h. das Flag nicht an den nächsten Router weiterleiten), was dir nur teilweisen Nutzen bringt, aber anonymer und einfacher sein könnte.

## Ergebnisse der Diskussion {#results}

... und andere verwandte Änderungen im selben Zeitraum (2007):

- Bedeutende Optimierung der Streaming-Bibliothek-Parameter,
  die die ausgehende Leistung stark verbesserte, wurde in 0.6.1.28 implementiert
- Priority-Sending für NTCP wurde in 0.6.1.28 implementiert
- Priority-Sending für SSU wurde von zzz implementiert, aber nie eingecheckt
- Die erweiterte Transport-Bid-Kontrolle
  i2np.udp.preferred wurde in 0.6.1.29 implementiert.
- Pushback für NTCP wurde in 0.6.1.30 implementiert, in 0.6.1.31 aufgrund von Anonymitätsbedenken deaktiviert
  und in 0.6.1.32 mit Verbesserungen zur Behebung dieser Bedenken wieder aktiviert.
- Keiner von zzz's Vorschlägen 1-5 wurde implementiert.
