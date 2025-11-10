---
title: "I2P-Statusnotizen vom 2006-10-03"
date: 2006-10-03
author: "jr"
description: "Netzwerkleistungsanalyse, Untersuchung von CPU-Engpässen, Planung der Syndie-1.0-Veröffentlichung und Evaluierung verteilter Versionskontrollsysteme"
categories: ["status"]
---

Hallo zusammen, diese Woche verspätete Statusnotizen

* Index

1) Netzstatus 2) Router-Entwicklungsstatus 3) Syndie-Begründung (Fortsetzung) 4) Syndie-Entwicklungsstatus 5) Verteilte Versionsverwaltung 6) ???

* 1) Net status

In den vergangenen ein bis zwei Wochen war es auf irc und anderen Diensten ziemlich stabil, obwohl es bei dev.i2p/squid.i2p/www.i2p/cvs.i2p ein paar kleinere Störungen gab (aufgrund vorübergehender, betriebssystembezogener Probleme). Im Moment scheint sich alles in einem stabilen Zustand zu befinden.

* 2) Router dev status

Die Kehrseite der Syndie-Diskussion ist: „Was bedeutet das also für den router?“, und um das zu beantworten, lassen Sie mich kurz erklären, wo die Entwicklung des routers derzeit steht.

Alles in allem ist es meiner Ansicht nach die Performance des router, nicht seine Anonymitätseigenschaften, die ihn daran hindert, 1.0 zu erreichen. Zwar gibt es durchaus Anonymitätsaspekte zu verbessern, doch obwohl wir für ein anonymes Netzwerk eine ziemlich gute Performance erreichen, ist unsere Performance für eine breitere Nutzung nicht ausreichend. Außerdem werden Verbesserungen der Anonymität des Netzwerks seine Performance nicht verbessern (in den meisten Fällen, die mir einfallen, verringern Anonymitätsverbesserungen den Durchsatz und erhöhen die Latenz). Wir müssen zuerst die Performanceprobleme beheben, denn wenn die Performance unzureichend ist, ist das gesamte System unzureichend, unabhängig davon, wie stark seine Anonymitätstechniken sind.

Also, was bremst unsere Performance? Seltsamerweise scheint es unsere CPU-Auslastung zu sein. Bevor wir genau auf das Warum eingehen, zunächst ein wenig Hintergrund.

 - to prevent partitioning attacks, we all need to plausibly build
   our tunnels from the same pool of routers.
 - to allow the tunnels to be of manageable length (and source
   routed), the routers in that pool must be directly reachable by
   anyone.
 - the bandwidth costs of receiving and rejecting tunnel join
   requests exceeds the capacity of dialup users on burst.

Daher benötigen wir Ebenen von routers – einige weltweit erreichbar mit hohen Bandbreitengrenzen (tier A), andere nicht (tier B). Dies ist de facto bereits über die Kapazitätsinformationen in der netDb umgesetzt worden, und Stand vor ein oder zwei Tagen lag das Verhältnis von tier B zu tier A bei etwa 3 zu 1 (93 routers mit cap L, M, N oder O und 278 mit cap K).

Nun gibt es im Wesentlichen zwei knappe Ressourcen, die in Stufe A verwaltet werden müssen - Bandbreite und CPU. Bandbreite kann mit den üblichen Mitteln verwaltet werden (die Last auf einen großen Pool verteilen, einige Peers extrem große Mengen übernehmen lassen [z. B. solche mit T3-Leitungen], und einzelne tunnels und Verbindungen ablehnen oder drosseln).

Die Steuerung der CPU-Auslastung ist schwieriger. Der primäre CPU-Engpass, der auf Tier-A routers zu beobachten ist, ist die Entschlüsselung von tunnel build requests (Aufbauanfragen für tunnel). Große routers können (und werden) durch diese Aktivität vollständig in Anspruch genommen werden - zum Beispiel beträgt die über die gesamte Laufzeit durchschnittliche Zeit zur Entschlüsselung eines tunnel bei einem meiner routers 225ms, und die über die gesamte Laufzeit *durchschnittliche* Frequenz einer Entschlüsselung einer tunnel build request liegt bei 254 Ereignissen pro 60 Sekunden, also 4,2 pro Sekunde. Wenn man diese beiden Zahlen einfach miteinander multipliziert, zeigt sich, dass 95 % der CPU allein durch die Entschlüsselung von tunnel build requests beansprucht wird (und dabei sind die Spitzen in den Ereigniszahlen nicht berücksichtigt). Dieser router schafft es trotzdem irgendwie, gleichzeitig an 4-6000 tunnels teilzunehmen, wobei er ungefähr 80 % der entschlüsselten Anfragen akzeptiert.

Leider muss dieser router, da seine CPU so stark ausgelastet ist, einen erheblichen Teil der tunnel-Aufbauanfragen verwerfen, noch bevor sie überhaupt entschlüsselt werden können (ansonsten würden die Anfragen so lange in der Warteschlange liegen, dass der ursprüngliche Anforderer sie selbst im Falle einer Annahme bereits als verloren betrachten oder als zu überlastet einstufen würde, um damit ohnehin noch etwas anfangen zu können). Vor diesem Hintergrund wirkt die 80%ige Annahmequote des router deutlich schlechter - im Laufe seiner Lebensdauer hat er rund 250.000 Anfragen entschlüsselt (was bedeutet, dass etwa 200.000 angenommen wurden), musste jedoch aufgrund einer CPU-Überlastung rund 430.000 Anfragen in der Entschlüsselungs-Warteschlange verwerfen (wodurch sich die 80%ige Annahmequote effektiv auf 30 % reduziert).

Die Lösungen scheinen darauf hinauszulaufen, die relevanten CPU-Kosten für die Entschlüsselung von tunnel-Anfragen zu verringern. Wenn wir die CPU-Zeit um eine Größenordnung reduzieren, würde das die Kapazität des tier A router erheblich erhöhen und damit Ablehnungen verringern (sowohl explizite als auch implizite, bedingt durch verworfene Anfragen). Das wiederum würde die Erfolgsrate beim tunnel-Aufbau erhöhen, die Häufigkeit von lease-Abläufen senken und dadurch die Bandbreitenbelastung im Netzwerk durch tunnel-Wiederaufbau reduzieren.

Eine Methode dafür wäre, die tunnel-Aufbauanfragen von 2048bit-Elgamal auf beispielsweise 1024bit oder 768bit umzustellen. Das Problem dabei ist jedoch, dass man, wenn man die Verschlüsselung einer tunnel-Aufbauanfrage-Nachricht bricht, den vollständigen tunnel-Pfad kennt. Selbst wenn wir diesen Weg gingen, wie viel würde uns das bringen? Eine Verbesserung der Entschlüsselungszeit um eine Größenordnung könnte durch eine Zunahme um eine Größenordnung im Verhältnis von Stufe B zu Stufe A (auch bekannt als das Freerider-Problem) zunichtegemacht werden, und dann säßen wir fest, da es keine Möglichkeit gäbe, auf 512- oder 256bit-Elgamal umzusteigen (und uns dabei noch im Spiegel anzusehen ;)

Eine Alternative wäre, schwächere Kryptografie zu verwenden, dabei jedoch auf den Schutz vor Paketzählangriffen zu verzichten, den wir mit dem neuen tunnel-Build-Prozess eingeführt haben. Das würde es uns erlauben, vollständig flüchtige, ausgehandelte Schlüssel in einem Tor-ähnlichen, teleskopischen tunnel zu verwenden (würde allerdings wiederum den Ersteller des tunnel trivialen passiven Paketzählangriffen aussetzen, die einen Dienst identifizieren).

Eine weitere Idee ist, noch explizitere Lastinformationen in der netDb zu veröffentlichen und zu nutzen, wodurch Clients Situationen wie die oben beschriebene genauer erkennen können, in der ein router mit hoher Bandbreite 60 % seiner Anforderungsnachrichten für tunnel verwirft, ohne sie sich überhaupt anzusehen. Es gibt einige Experimente, die sich in dieser Richtung lohnen, und sie lassen sich mit vollständiger Abwärtskompatibilität durchführen, sodass wir sie bald sehen sollten.

Das ist also der Engpass im router/Netzwerk, so wie ich ihn derzeit sehe. Sämtliche Vorschläge dazu, wie wir damit umgehen können, würden sehr geschätzt.

* 3) Syndie rationale continued

Im Forum gibt es einen ausführlichen Beitrag zu Syndie und dazu, wie es ins Gesamtbild passt - sehen Sie ihn sich hier an: <http://forum.i2p.net/viewtopic.php?t=1910>

Außerdem möchte ich nur kurz zwei Ausschnitte aus der derzeit in Arbeit befindlichen Syndie-Dokumentation hervorheben. Zunächst aus irc (und der noch nicht veröffentlichten FAQ):

<bar> eine Frage, die ich mir gestellt habe, ist: Wer wird später die Eier haben, Syndie-Produktionsserver/-Archive zu hosten?  <bar> Werden die nicht genauso leicht aufzuspüren sein, wie es die eepsites(I2P Sites) heute sind?  <jrandom> öffentliche Syndie-Archive haben nicht die Möglichkeit, die in Foren veröffentlichten Inhalte zu *lesen*, es sei denn, die Foren veröffentlichen die Schlüssel dafür  <jrandom> und siehe den zweiten Absatz von usecases.html  <jrandom> natürlich werden diejenigen, die Archive hosten, bei einer rechtmäßigen Anordnung, ein Forum zu entfernen, dies wahrscheinlich tun  <jrandom> (aber dann können die Leute zu einem anderen Archiv umziehen, ohne den Betrieb des Forums zu stören)  <void> ja, du solltest erwähnen, dass die Migration auf ein anderes Medium nahtlos sein wird  <bar> wenn mein Archiv dichtmacht, kann ich mein ganzes Forum zu einem neuen hochladen, richtig?  <jrandom> ganz genau, bar  <void> sie können während der Migration zwei Methoden gleichzeitig verwenden  <void> und jeder kann die Medien synchronisieren  <jrandom> richtig, void

Der relevante Abschnitt der (noch nicht veröffentlichten) Syndie usecases.html ist:

Während viele verschiedene Gruppen oft Diskussionen in   einem Online-Forum organisieren möchten, kann die zentrale Struktur traditioneller Foren   (Websites, BBSes, usw.) problematisch sein. Zum Beispiel kann die Seite,   die das Forum hostet, durch Denial-of-Service-Angriffe   oder durch administrative Maßnahmen offline genommen werden. Außerdem bietet der einzelne Host   einen einfachen Ansatzpunkt, die Aktivitäten der Gruppe zu überwachen, sodass selbst dann,   wenn ein Forum pseudonym ist, diese Pseudonyme mit der IP-Adresse   verknüpft werden können, die einzelne Nachrichten gepostet oder gelesen hat.

Außerdem sind die Foren nicht nur dezentralisiert, sie sind ad-hoc organisiert und dennoch vollständig mit anderen Organisationstechniken kompatibel. Das bedeutet, dass eine kleine Gruppe von Personen ihr Forum mit einer Technik betreiben kann (die Nachrichten verteilen, indem sie sie auf einer Wiki-Seite eintragen), eine andere kann ihr Forum mit einer anderen Technik betreiben (indem sie ihre Nachrichten in einer verteilten Hashtabelle wie OpenDHT veröffentlichen, kennt jedoch eine Person beide Techniken, kann sie die beiden Foren miteinander synchronisieren. Dadurch können die Personen, die nur die Wiki-Seite kannten, mit den Personen sprechen, die nur den OpenDHT-Dienst kannten, ohne irgendetwas voneinander zu wissen. Noch weiter gefasst erlaubt Syndie einzelnen Zellen, ihre eigene Sichtbarkeit zu steuern, während sie über die gesamte Organisation hinweg kommunizieren.

* 4) Syndie dev status

In letzter Zeit gab es bei Syndie viele Fortschritte, wobei 7 Alpha-Versionen an Leute im IRC-Kanal verteilt wurden. Die meisten wesentlichen Probleme in der skriptfähigen Schnittstelle wurden angegangen, und ich hoffe, dass wir Syndie 1.0 noch im Laufe dieses Monats veröffentlichen können.

Habe ich gerade "1.0" gesagt? Und ob! Auch wenn Syndie 1.0 eine textbasierte Anwendung sein wird und nicht einmal an die Benutzerfreundlichkeit anderer textbasierter Anwendungen (wie mutt oder tin) heranreichen wird, wird sie den vollen Funktionsumfang bieten, HTTP- und dateibasierte Syndizierungsstrategien ermöglichen und hoffentlich potenziellen Entwicklern Syndies Fähigkeiten aufzeigen.

Im Moment plane ich vorläufig ein Syndie-1.1-Release (damit die Leute ihre Archive und Lesegewohnheiten besser organisieren können) und vielleicht ein 1.2-Release, um einige Suchfunktionen zu integrieren (sowohl einfache Suchen als auch eventuell Lucenes Volltextsuche). Syndie 2.0 wird wahrscheinlich das erste GUI (grafische Benutzeroberfläche)-Release sein, wobei das Browser-Plugin mit 3.0 kommt. Unterstützung für zusätzliche Archive und Netzwerke zur Nachrichtenverteilung wird natürlich kommen, sobald sie implementiert ist (freenet, mixminion/mixmaster/smtp, opendht, gnutella, etc).

Mir ist jedoch klar, dass Syndie 1.0 nicht der große Wurf sein wird, den sich manche wünschen, da textbasierte Anwendungen wirklich eher etwas für Geeks sind, aber ich möchte versuchen, uns die Gewohnheit abzugewöhnen, "1.0" als endgültige Version zu betrachten, und sie stattdessen als einen Anfang zu betrachten.

* 5) Distributed version control

Bisher habe ich mit Subversion als VCS (Versionsverwaltungssystem) für Syndie herumprobiert, obwohl ich eigentlich nur in CVS und ClearCase wirklich versiert bin. Das liegt daran, dass ich die meiste Zeit offline bin, und selbst wenn ich online bin, ist die Einwahlverbindung langsam, sodass sich Subversions lokale diff/revert/etc als ziemlich praktisch erwiesen haben. Gestern hat mich void jedoch mit dem Vorschlag angestupst, dass wir uns stattdessen eines der verteilten Systeme ansehen.

Ich habe sie mir vor ein paar Jahren angesehen, als ich ein Versionskontrollsystem für I2P evaluiert habe, aber ich habe sie verworfen, weil ich ihre Offline-Funktionalität nicht brauchte (damals hatte ich eine gute Netzanbindung), sodass es sich nicht lohnte, sie zu lernen. Das ist inzwischen nicht mehr der Fall, daher schaue ich sie mir jetzt etwas genauer an.

- From what I can see, darcs, monotone, and codeville are the top

Kandidaten, und das patchbasierte VCS von darcs wirkt besonders attraktiv. Zum Beispiel kann ich die ganze Arbeit lokal erledigen und die gzip'ed & gpg'ed Diffs einfach per scp in ein Apache-Verzeichnis auf dev.i2p.net hochladen, und andere können ihre eigenen Änderungen beisteuern, indem sie ihre gzip'ed und gpg'ed Diffs an Orten ihrer Wahl veröffentlichen. Wenn es an der Zeit ist, einen Release zu taggen, würde ich ein darcs diff erstellen, das die Menge der in dem Release enthaltenen Patches angibt, und dieses .gz'ed/.gpg'ed diff wie die anderen hochladen (sowie natürlich auch die eigentlichen tar.bz2-, .exe- und .zip-Dateien bereitstellen ;)

Und, als besonders interessanter Punkt, können diese gzip- und gpg-verarbeiteten Diffs als Anhänge zu Syndie-Nachrichten gepostet werden, was es Syndie ermöglicht, sich selbst zu hosten.

Hat jemand Erfahrungen mit diesen Teilen? Irgendwelche Tipps?

* 6) ???

Diesmal nur 24 Bildschirmseiten Text (einschließlich des Forenbeitrags) ;) Leider konnte ich nicht am Treffen teilnehmen, aber wie immer freue ich mich, von euch zu hören, wenn ihr Ideen oder Vorschläge habt – postet sie einfach auf die Mailingliste, ins Forum, oder schaut im IRC vorbei.

=jr
