---
title: "I2P-Statusnotizen vom 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Weekly update covering network growth to 400-500 peers, Fortuna PRNG integration, GCJ native compilation support, i2psnark lightweight torrent client, and tunnel bootstrap attack analysis"
categories: ["status"]
---

Hallo zusammen, weitere Neuigkeiten von der Front

* Index

1) Netzstatus 2) Fortuna-Integration 3) GCJ-Status 4) i2psnark kehrt zurück 5) Mehr zum Bootstrapping (Initialisierung) 6) Virenuntersuchungen 7) ???

* 1) Net status

Die vergangene Woche war im Netz ziemlich gut – die Dinge scheinen recht stabil, der Durchsatz normal, und das Netz wächst weiter in den Bereich von 400–500 Peers hinein. Seit dem 0.6.1.3-Release gab es ebenfalls einige bedeutende Verbesserungen, und da sie Leistung und Zuverlässigkeit betreffen, rechne ich damit, dass wir später in dieser Woche ein 0.6.1.4-Release veröffentlichen werden.

* 2) Fortuna integration

Thanks to Casey Marshall's quick fix [1], we've been able to integrate GNU-Crypto's Fortuna [2] pseduorandom number generator. This removes the cause of much frustration with the blackdown JVM, and lets us work smoothly with GCJ. Integrating Fortuna into I2P was one of the main reasons smeghead developed "pants" (an 'ant' based 'portage'), so we've now had another successful pants usage :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Wie auf der Liste [3] erwähnt, können wir den router und die meisten Clients jetzt nahtlos mit GCJ [4] ausführen. Die Webkonsole selbst funktioniert noch nicht vollständig, daher müssen Sie Ihre eigene router-Konfiguration mit router.config vornehmen (obwohl es einfach funktionieren sollte und Ihre tunnels nach etwa einer Minute starten). Ich bin mir nicht ganz sicher, wie GCJ in unsere Release-Pläne passt, allerdings neige ich derzeit dazu, reine Java-Versionen zu verteilen, aber sowohl Java- als auch nativ kompilierte Versionen zu unterstützen. Es ist etwas mühsam, viele verschiedene Builds für unterschiedliche Betriebssysteme und Bibliotheksversionen usw. zu erstellen und zu verteilen. Hat jemand dazu starke Präferenzen?

Ein weiteres positives Merkmal der GCJ-Unterstützung ist die Möglichkeit, die Streaming-Bibliothek aus C/C++/Python/etc. zu verwenden. Ich weiß nicht, ob derzeit jemand an dieser Art von Integration arbeitet, aber es wäre wahrscheinlich lohnenswert. Wenn Sie Interesse haben, in diesem Bereich mitzuarbeiten, lassen Sie es mich bitte wissen!

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Obwohl i2p-bt der erste auf I2P portierte BitTorrent-Client war, der viel genutzt wurde, war eco schon vor langer Zeit mit seinem Port von snark [5] der eigentliche Vorreiter. Er blieb leider nicht auf dem neuesten Stand und behielt auch nicht die Kompatibilität mit den anderen anonymen BitTorrent-Clients bei, sodass er eine Zeit lang quasi verschwand. Letzte Woche jedoch hatte ich Schwierigkeiten mit Leistungsproblemen irgendwo in der i2p-bt<->sam<->streaming lib<->i2cp-Kette, also bin ich auf mjws ursprünglichen snark-Code umgestiegen und habe einen einfachen Port [6] vorgenommen, wobei ich alle Aufrufe von java.net.*Socket durch Aufrufe von I2PSocket*, InetAddresses durch Destinations und URLs durch Aufrufe von EepGet ersetzt habe. Das Ergebnis ist ein winziger Kommandozeilen-BitTorrent-Client (kompiliert etwa 60 KB), den wir nun zusammen mit dem I2P-Release ausliefern werden.

Ragnarok hat bereits begonnen, daran herumzuschrauben, um dessen Blockauswahlalgorithmus zu verbessern, und hoffentlich bekommen wir noch vor dem 0.6.2-Release sowohl eine Weboberfläche als auch Multitorrent-Unterstützung hinein. Wenn du mithelfen möchtest, melde dich! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

Die Mailingliste war in letzter Zeit ziemlich aktiv, unter anderem durch Michaels neue Simulationen und Analysen des tunnel-Aufbaus. Die Diskussion läuft noch, mit einigen guten Ideen von Toad, Tom und polecat, also schaut es euch an, wenn ihr Input zu den Abwägungen bei einigen anonymitätsbezogenen Designfragen geben wollt, die wir für das 0.6.2-Release überarbeiten werden [7].

Für diejenigen, die an etwas Eye-Candy interessiert sind, hat Michael ebenfalls etwas parat: eine Simulation dazu, wie wahrscheinlich der Angriff dich identifizieren kann - als Funktion des Prozentsatzes des Netzwerks, den sie kontrollieren [8], und als Funktion davon, wie aktiv dein tunnel ist [9]

(Gute Arbeit, Michael, danke!)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (dem Thread "i2p tunnel bootstrap attack" folgen) [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Es gab einige Diskussionen über mögliche Malware-Probleme, die zusammen mit einer bestimmten I2P‑fähigen Anwendung verbreitet werden, und Complication hat großartige Arbeit bei der Untersuchung geleistet. Die Daten sind öffentlich verfügbar, sodass Sie sich selbst ein Bild machen können. [10]

Vielen Dank, Complication, für all deine Recherchen dazu!

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Es ist jede Menge los, wie du siehst, aber da ich schon zu spät zum Meeting bin, sollte ich das hier wohl speichern und abschicken, oder? Wir sehen uns in #i2p :)

=jr
