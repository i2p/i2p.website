---
title: "I2P Statusnotizen für 2004-10-05"
date: 2004-10-05
author: "jr"
description: "Wöchentliches I2P-Status-Update zu Release 0.4.1.1, Analyse der Netzwerkstatistiken, Plänen für die Streaming-Bibliothek in 0.4.2 und dem mitgelieferten eepserver"
categories: ["status"]
---

Hi zusammen, es ist Zeit für das wöchentliche Update

## Index:

1. 0.4.1.1 status
2. Pretty pictures
3. 0.4.1.2 and 0.4.2
4. Bundled eepserver
5. ???

## 1) 0.4.1.1 status

Nach einer ziemlich holprigen 0.4.1-Veröffentlichung (und dem anschließenden schnellen 0.4.1.1-Update) scheint das Netz wieder normal zu laufen - derzeit sind um die 50 Peers aktiv, und sowohl irc als auch eepsites(I2P Sites) sind erreichbar. Der größte Teil der Probleme wurde durch unzureichende Tests des neuen Transports außerhalb von Laborbedingungen verursacht (z. B. Sockets, die zu merkwürdigen Zeiten ausfallen, übermäßige Verzögerungen usw.). Beim nächsten Mal, wenn wir Änderungen auf dieser Ebene vornehmen müssen, werden wir sicherstellen, dass wir sie vor der Veröffentlichung breiter testen.

## 2) Hübsche Bilder

In den letzten Tagen sind in CVS eine ganze Reihe von Updates eingeflossen, und eine der Neuerungen war eine neue Stat-Logging-Komponente, mit der wir die rohen Statistikdaten einfach während sie erzeugt werden extrahieren können, statt uns mit den groben Durchschnittswerten auf /stats.jsp herumzuschlagen. Damit habe ich einige zentrale Statistiken auf einigen routers überwacht, und wir kommen dem Aufspüren der verbleibenden Stabilitätsprobleme näher. Die rohen Statistiken sind ziemlich umfangreich (ein 20-stündiger Lauf auf ducks Rechner erzeugte fast 60MB Daten), aber genau dafür haben wir hübsche Bilder - `http://dev.i2p.net/~jrandom/stats/`

Die Y-Achse der meisten davon ist in Millisekunden, während die X-Achse in Sekunden ist. Es gibt ein paar interessante Punkte. Erstens ist client.sendAckTime.png eine ziemlich gute Annäherung an die Verzögerung eines einzelnen Round-Trips (Round-Trip-Zeit, RTT), da die Ack-Nachricht zusammen mit der Nutzlast gesendet wird und dann den gesamten Pfad des tunnel zurücklegt – daher hatten die allermeisten der fast 33.000 erfolgreich gesendeten Nachrichten eine Round-Trip-Zeit von unter 10 Sekunden. Wenn wir anschließend client.sendsPerFailure.png zusammen mit client.sendAttemptAverage.png betrachten, sehen wir, dass die 563 fehlgeschlagenen Sendungen fast alle bis zur maximal zulässigen Anzahl von Wiederholungen gesendet wurden (5 mit einem Soft-Timeout von 10s pro Versuch und 60s Hard-Timeout), während die meisten der anderen Versuche beim ersten oder zweiten Mal erfolgreich waren.

Ein weiteres interessantes Bild ist client.timeout.png, das eine von mir aufgestellte Hypothese stark in Zweifel zieht – nämlich dass die Fehler beim Senden von Nachrichten mit einer Art lokaler Überlastung korrelierten. Die dargestellten Daten zeigen, dass die Auslastung der eingehenden Bandbreite stark variierte, als Fehler auftraten, es keine konsistenten Spitzen bei der lokalen Sendeverarbeitungszeit gab und offenbar überhaupt kein Muster in Bezug auf die tunnel-Testlatenz zu erkennen war.

Die Dateien dbResponseTime.png und dbResponseTime2.png ähneln der client.sendAckTime.png, außer dass sie sich auf netDb-Nachrichten statt auf End-to-End-Client-Nachrichten beziehen.

Die transport.sendMessageFailedLifetime.png zeigt, wie lange wir eine Nachricht lokal zurückhalten, bevor wir sie aus irgendeinem Grund als fehlgeschlagen markieren (zum Beispiel, weil ihr Ablauf erreicht ist oder der anvisierte Peer nicht erreichbar ist). Einige Fehlschläge sind unvermeidlich, aber dieses Bild zeigt, dass eine erhebliche Anzahl direkt nach dem lokalen Sende-Timeout (10s) fehlschlägt. Dagegen können wir ein paar Dinge tun: - erstens können wir die Shitlist (Sperrliste) adaptiver machen- den Zeitraum, für den ein Peer auf der Shitlist steht, exponentiell erhöhen, statt pauschal jeweils 4 Minuten. (dies wurde bereits in CVS eingecheckt) - zweitens können wir Nachrichten vorsorglich fehlschlagen lassen, wenn es ohnehin so aussieht, als würden sie fehlschlagen. Dazu hält jede Verbindung ihre Sende-Rate nach, und immer wenn ihrer Warteschlange eine neue Nachricht hinzugefügt wird, wird die Nachricht sofort verworfen, wenn die Anzahl der bereits in der Warteschlange stehenden Bytes, geteilt durch die Sende-Rate, die verbleibende Zeit bis zum Ablauf überschreitet. Diese Metrik könnten wir auch heranziehen, um zu entscheiden, ob über einen Peer weitere tunnel-Anfragen akzeptiert werden.

Jedenfalls weiter zum nächsten hübschen Bild - transport.sendProcessingTime.png. Darin sieht man, dass dieser bestimmte Rechner nur selten für große Latenz verantwortlich ist - typischerweise 10-100ms, auch wenn es gelegentlich Spitzen bis auf 1s oder mehr gibt.

Jeder in der Grafik tunnel.participatingMessagesProcessed.png dargestellte Punkt repräsentiert, wie viele Nachrichten über einen tunnel weitergeleitet wurden, an dem der router beteiligt war. In Kombination mit der durchschnittlichen Nachrichtengröße ergibt sich daraus eine geschätzte Netzwerklast, die der Peer für andere übernimmt.

Das letzte Bild ist tunnel.testSuccessTime.png und zeigt, wie lange es dauert, eine Nachricht über einen tunnel zu senden und durch einen anderen eingehenden tunnel wieder nach Hause zu bringen, was uns eine Schätzung darüber gibt, wie gut unsere tunnel sind.

Okay, genug hübscher Bilder fürs Erste. Sie können die Daten selbst mit jeder Version nach 0.4.1.1-6 erzeugen, indem Sie die Router-Konfigurationseigenschaft "stat.logFilters" auf eine kommagetrennte Liste von Stat-Namen setzen (holen Sie die Namen von der Seite /stats.jsp). Das wird in stats.log ausgegeben, die Sie weiterverarbeiten können mit

```
java -cp lib/i2p.jar net.i2p.stat.StatLogFilter stat.log
```
die es in separate Dateien für jede Statistik aufteilt, geeignet zum Laden in Ihr bevorzugtes Tool (z. B. gnuplot).

## 3) 0.4.1.2 und 0.4.2

Seit dem 0.4.1.1-Release gab es viele Aktualisierungen (eine vollständige Liste finden Sie in der Historie), aber bisher keine kritischen Fehlerbehebungen. Wir werden sie im nächsten Patch-Release 0.4.1.2 später in dieser Woche ausrollen, nachdem einige noch offene Fehler im Zusammenhang mit der automatischen IP-Erkennung behoben wurden.

Die nächste große Aufgabe wird dann sein, 0.4.2 zu erreichen, was derzeit als eine umfassende Überarbeitung der tunnel-Verarbeitung vorgesehen ist. Das wird eine Menge Arbeit bedeuten: die Überarbeitung der Verschlüsselung und der Nachrichtenverarbeitung sowie des tunnel-Pooling, aber es ist ziemlich kritisch, da ein Angreifer derzeit relativ leicht einige statistische Angriffe auf die tunnels durchführen könnte (z. B. predecessor (Vorgängerangriff) mit zufälliger Reihenfolge der tunnels oder netDb-Harvesting (Sammeln aus der netDb)).

dm stellte jedoch die Frage, ob es sinnvoll wäre, zuerst die Streaming-Bibliothek umzusetzen (derzeit für das Release 0.4.3 geplant). Der Vorteil wäre, dass das Netzwerk sowohl zuverlässiger würde als auch einen höheren Durchsatz hätte, was andere Entwickler dazu ermutigen würde, bei Client-Anwendungen loszulegen. Sobald das umgesetzt ist, könnte ich dann zur Überarbeitung der tunnel zurückkehren und die (für Benutzer nicht sichtbaren) Sicherheitsprobleme angehen.

Technisch gesehen sind die beiden für 0.4.2 und 0.4.3 geplanten Aufgaben orthogonal, und sie werden ohnehin beide erledigt, daher scheint es kaum Nachteile zu geben, diese zu vertauschen. Ich neige dazu, dm zuzustimmen, und sofern niemand Gründe nennen kann, 0.4.2 als das tunnel-Update und 0.4.3 als die Streaming-Bibliothek beizubehalten, werden wir sie vertauschen.

## 4) Mitgelieferter eepserver

Wie in den Versionshinweisen zu 0.4.1 erwähnt, haben wir die zum Betrieb einer eepsite(I2P-Seite) erforderliche Software und Konfiguration so gebündelt, dass sie sofort einsatzbereit ist - Sie können einfach eine Datei im Verzeichnis ./eepsite/docroot/ ablegen und die auf der router-Konsole angezeigte I2P destination (Zieladresse) teilen.

Einige Leute haben mich allerdings wegen meines Eifers für .war-Dateien angesprochen - die meisten Anwendungen erfordern leider ein wenig mehr Aufwand, als einfach eine Datei in das Verzeichnis ./eepsite/webapps/ zu legen. Ich habe eine kurze Anleitung zum Ausführen der Blogging-Engine blojsom zusammengestellt, und auf der Website von detonate können Sie sehen, wie das aussieht.

## 5) ???

Das ist so ziemlich alles, was ich im Moment habe - schau in 90 Minuten beim Meeting vorbei, wenn du darüber diskutieren willst.

=jr
