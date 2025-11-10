---
title: "I2P-Entwicklertreffen"
date: 2003-07-15
author: "nop"
description: "I2P-Entwicklungstreffen mit Projekt-Updates und technischen Diskussionen"
categories: ["meeting"]
---

(Mit freundlicher Genehmigung der Wayback Machine http://www.archive.org/)

## Kurze Zusammenfassung

<p class="attendees-inline"><strong>Anwesend:</strong> gott, hezekiah, jeremiah, jrand0m, mihi, Neo, nop, WinBear</p>

## Sitzungsprotokoll

<div class="irc-log"> --- Log geöffnet Tue Jul 15 17:46:47 2003 17:46 < gott> yo. 17:46 <@nop> nur ein kurzer Hinweis zu meinem Schweigen 17:46 <@hezekiah> Tue Jul 15 21:46:49 UTC 2003 17:47 <@hezekiah> OK. Das iip-dev-Meeting hat begonnen. 17:47 <@hezekiah> Ist es das 48. oder 49.? 17:47 < jrand0m> nop> deshalb ist es entscheidend, dass wir die router-Architektur so schnell wie möglich festzurren. Ich verstehe, dass verschiedene Leute unterschiedlich schnell arbeiten, und wir müssen segmentieren, damit verschiedene Komponenten entsprechend vorankommen können 17:47 < mihi> 49. 17:47 <@hezekiah> OK! Willkommen zum 49. iip-dev-Meeting! 17:47 < jrand0m> Ich habe noch drei Tage in meinem Job, danach werde ich 90+ Stunden/ 	Woche dafür aufwenden, das hier zum Laufen zu bringen 17:48 < jrand0m> Ich weiß und erwarte nicht, dass alle das können, 	deshalb müssen wir segmentieren 17:48 < jrand0m> hi hezekiah :) 17:48 <@hezekiah> lol 17:48 <@nop> um dem zu widersprechen 17:48 <@hezekiah> Ich warte eine Minute. Dann können wir die Agenda machen. :) 17:48 <@nop> die Sicherheit der router-Architektur hängt auch davon ab, dass ihr 	nicht übereilt vorgeht 17:49 <@nop> wenn wir das tun 17:49 <@nop> übersehen wir Dinge 17:49 <@nop> was uns später eine große Sauerei aufräumen lassen könnte 17:49 -!- Rain [Rain@anon.iip] hat den Kanal verlassen [I Quit] 17:49 < jrand0m> nop> widerspreche. Wir können trotzdem die App-Schicht und die APIs 	bauen, ohne den router zu implementieren (oder auch nur zu wissen, wie das Netzwerk funktionieren wird) 17:49 <@nop> Dem stimme ich zu 17:50 <@nop> Ich spreche speziell vom zugrunde liegenden Netzwerk 17:50 < jrand0m> wenn wir uns auf die API einigen können, die ich herumgeschickt habe, 	dann ist das die Segmentierung, die wir brauchen 17:50 < jrand0m> richtig, router-Implementierung und Netzwerkdesign sind noch nicht fertig 17:50 <@nop> ok 17:50 <@nop> oh, mit deiner API kann ich bisher definitiv übereinstimmen 17:51 <@hezekiah> jrand0m: Ein Problem. 17:51 < jrand0m> leg los, hezekiah 17:51 <@hezekiah> Es wird anders aussehen, wenn du es in C implementierst. 17:51 < jrand0m> nicht allzu anders 17:51 < gott> oh je 17:51 < jrand0m> weniger Großbuchstaben und die Objekte durch Structs ersetzen 17:51 < gott> in welchen Sprachen überlegen die Leute, es zu implementieren? 17:51 < jrand0m> (für die API) 17:51 <@hezekiah> Ähm, jrand0m? Es gibt kein 'byte[]' in C. 17:51 < jrand0m> gott> lies die Mail-Archive für einige Beispielantworten dazu 17:52 <@hezekiah> Du wirst höchstwahrscheinlich void*-Zeiger mit einem Integer verwenden, um die 	Länge anzugeben. 17:52 < jrand0m> hezekiah> dann unsigned int[] 17:52 < gott> jrand0m: ausnahmsweise ein Glaubenskrieg, an dem ich nicht beteiligt bin 17:52 <@hezekiah> Wenn ich mich richtig erinnere (hilf mir mal kurz, nop), kann man 	aus einer Funktion nicht einfach ein unsigned int[] zurückgeben. 17:53 <@hezekiah> gott: im Gegensatz wozu? Pseudocode? 17:53 < jrand0m> genau, syntaktische Änderungen. Aber ja, wenn es echte 	Unterschiede gibt, müssen wir die ASAP klären. (also, heute) Vielleicht 	wäre jetzt ein guter Zeitpunkt, die E-Mail von mir mit dem Titel "high level 	router architecture and API" anzuschauen und zu besprechen? 17:54 <@hezekiah> nop? UserX? Seid ihr dabei? 17:54 < jrand0m> nicht allzu anders, aber trotzdem anders, ja. 	Deshalb habe ich in der heutigen E-Mail Java API gesagt :) 17:54 -!- WinBear [WinBear@anon.iip] ist #iip-dev beigetreten 17:55 <@nop> moment 17:55 <@nop> lese oben nach 17:55 -!- mihi_2 [~none@anon.iip] ist #iip-dev beigetreten 17:55 -!- mihi ist jetzt als nickthief60234 bekannt 17:55 -!- mihi_2 ist jetzt als mihi bekannt 17:55 < jrand0m> wb mihi 17:55 < gott> btw, wird das hier live mitgeloggt? 17:55 -!- nickthief60234 [~none@anon.iip] hat das Gespräch verlassen [EOF From client] 17:55 <@hezekiah> gott: Ja. 17:55 < mihi> Redundanz rockt ;) 17:55 < gott> Dann lese ich es später. 17:55 -!- gott [~gott@anon.iip] hat #iip-dev verlassen [gott] 17:56 <@nop> ok 17:56 <@nop> ja 17:56 < WinBear> jrand0m: hi 17:56 <@nop> definitiv Unterschiede 17:56 <@nop> was wir brauchen 17:56 < jrand0m> heya WinBear 17:56 <@nop> ist ein Team bestimmter Entwickler, das die zentralen API-Level- 	Steuerungen für diese Sprachen schreibt 17:56 <@nop> wir wissen, dass jrand0m Java übernehmen kann 17:56 <@nop> und sich wahrscheinlich auch mit thecrypto zusammentun kann 17:56 <@nop> und hezekiah und die Crew können C machen 17:56 <@nop> und jeremiah, wenn er will 17:56 <@nop> kann Python machen 17:56 <@hezekiah> Ich kann auch C++! ;-) 17:56 <@nop> ok 17:56 <@nop> C++ auch 17:57 <@hezekiah> lol 17:57 <@nop> C++ wird wahrscheinlich 17:57 <@nop> mit C funktionieren 17:57 <@nop> wenn du es nicht mit Templates vollpackst 17:57 < jrand0m> heh 17:57 <@hezekiah> lol 17:57 <@hezekiah> Eigentlich kann MSVC C- und C++-Objektdateien linken, 	gcc scheint das nicht zu mögen. 17:57 <@nop> sprich, bleib bei Structs, die mit C kompatibel sind, oder ist das 	nicht machbar 17:57 < jrand0m> erste Frage, davor: Welche Anwendungen werden 	diese APIs nutzen? Ich kenne Apps, die Java verwenden wollen, wird iproxy in C sein? 17:58 <@hezekiah> nop: Ich glaube nicht, dass C und C++ objektkompatibel sind. 17:58 <@nop> ok 17:58 <@hezekiah> nop: C++ wird sich mit C nicht viel besser vertragen als Java. 17:58 <@nop> nun, vielleicht könnte USerX C machen 17:58 <@nop> und du übernimmst C++ 17:58 <@hezekiah> We don 17:58 <@nop> ? 17:58 <@hezekiah> müssen nicht einmal C++ _machen_, wenn ihr nicht wollt. Es ist 	nur so, dass ich es bevorzuge. 17:59 <@nop> nun, die Sache ist 17:59 <@nop> es gibt viele C++-Entwickler 17:59 <@nop> besonders in der Microsoft-Welt 17:59 <@hezekiah> Auch in der Linux-Welt. (siehe: KDE und Qt.) 17:59 < jrand0m> C und C++ sind binärkompatibel, wenn du einfach .so oder .a 	machst 17:59 < jrand0m> (btw) 18:00 <@nop> kann C ein guter Platzhalter für C++ sein, sprich C++-Entwickler würden 	mit einer C-API leichter umgehen als ein C-Entwickler mit einer C++-API? 18:00 <@hezekiah> jrand0m: Ja. Du kannst wahrscheinlich Bibliotheken ... aber wenn 	du kannst 18:00 <@hezekiah> jrand0m: nicht einmal Klassen verwenden kannst, verfehlt das 	irgendwie den Zweck. 18:00 <@nop> richtig 18:00 <@nop> bleiben wir bei C 18:01 <@nop> denn C++-Coder können eine C-Bibliothek immer noch recht einfach aufrufen 18:01 <@hezekiah> Wenn ein Modul die Funktionen eines anderen aufrufen muss, dann sie 	sollten beide besser dieselbe Sprache haben. 18:01 <@hezekiah> nop: C++-Coder kennen C gut genug ... obwohl es 	Arbeit kosten könnte, wenn sie C nie /gelernt/ haben. 18:02 <@hezekiah> Allerdings kennen C-Coder C++ nicht, da C nur eine 	Teilmenge von C++ ist. 18:02 -!- logger_ [~logger@anon.iip] ist #iip-dev beigetreten 18:02 -!- Topic for #iip-dev: Logfiles werden nach dem Meeting online sein: 	http://wiki.invisiblenet.net/?Meetings 18:02 [Benutzer #iip-dev] 18:02 [@hezekiah] [+Ehud    ] [ leenookx] [ moltar] [ tek    ] 18:02 [@nop     ] [ jeremiah] [ logger_ ] [ Neo   ] [ WinBear] 18:02 [@UserX   ] [ jrand0m ] [ mihi    ] [ ptsc  ] 18:02 -!- Irssi: #iip-dev: Insgesamt 14 Nicks [3 Ops, 0 Halfops, 1 Voices, 10 normale] 18:02 < jrand0m> richtig 18:02 -!- Irssi: Beitritt zu #iip-dev wurde in 9 Sek. synchronisiert 18:02 < jrand0m> (mit JMS :) 18:02 <@nop> yep 18:03 -!- Du heißt jetzt logger 18:03 < jrand0m> ok, können wir zuerst die Gesamtarchitektur prüfen, um zu sehen, ob 	die APIs überhaupt relevant sind? 18:03 <@nop> gut  18:04 < jrand0m> :) 18:04 < jrand0m> ok, sieh dir die E-Mail an, die ich mit der routerArchitecture.png 	geschickt habe. Gedanken zu dieser Trennung? 18:04 -!- tek [~tek@anon.iip] hat das Gespräch verlassen [] 18:05 < WinBear> jrand0m: ist das im Wiki? 18:05 < jrand0m> WinBear> nein, auf der Mailingliste, obwohl die Archive 	down sind. lass mich das ins Wikki hinzufügen 18:06 <@hezekiah> Korrigiert mich, wenn ich falsch liege ... 18:07 <@hezekiah> ... aber es sieht so aus, als hätten wir 3 separate APIs, 	die so ähnlich wie möglich sind. 18:07 <@hezekiah> Richtig? 18:07 < jrand0m> ja, hezekiah 18:07 <@hezekiah> Da jede API in einer anderen Sprache ist, werden sie 	dann jeweils eigene Implementierungen haben? 18:07 < jrand0m> ja 18:07 <@hezekiah> Oder gibt es eine Möglichkeit, dass Java oder Python auf eine C-Bibliothek zugreifen? 18:08 < jrand0m> ja, aber diesen Weg wollen wir nicht gehen 18:08 < mihi> für Java: JNI 18:08 <@hezekiah> Also ist die Rede davon, dass Java, C, C++, Python, etc. zusammen 	arbeiten, hinfällig, da sie das nie tun werden? 18:08 < jrand0m> wie hänge ich ein Bild ans Wiki an? 18:08 <@hezekiah> Jede API hat ihr eigenes Backend, geschrieben in dieser Sprache. 18:08 < jrand0m> nein hezekiah, schau dir das Diagramm an 18:09 <@hezekiah> Oh, klar! 18:09 <@hezekiah> Die APIs sind nicht mit einem Backend gelinkt. 18:10 <@hezekiah> Sie sprechen über Sockets. 18:10 < jrand0m> si sr 18:10 <@hezekiah> Das ist trotzdem noch etwas verwirrend. 18:10 <@hezekiah> Gib mir eine Sekunde. :) 18:11 <@hezekiah> OK. Was ist das Ding, das mit 'transport' beschriftet ist? 18:11 < jrand0m> zum Beispiel bidirektionaler HTTP-Transport, SMTP-Transport, 	einfacher Socket-Transport, pollender HTTP-Socket usw. 18:11 < jrand0m> das Ding, das Bytes zwischen routern bewegt 18:12 <@hezekiah> OK. 18:12 <@hezekiah> Das Diagramm, das ich mir anschaue, zeigt also den Computer einer Person. 18:12 <@hezekiah> Er hat einen router, der über die Transports 	mit den Computern anderer Leute spricht. 18:12 < jrand0m> korrekt 18:12 <@hezekiah> Person 1 (Alice) hat 2 Anwendungen laufen. 18:12 <@hezekiah> Eine in C, die andere in Java. 18:13 <@hezekiah> Beide sind mit einer Bibliothek gelinkt (das ist die API). 18:13 < jrand0m> beide sind mit separaten Bibliotheken „gelinkt“ (die APIs) 18:13 <@nop> einfaches Konzept 18:13 <@nop> ja 18:13 <@hezekiah> Diese Bibliotheken nehmen Eingaben aus dem Programm, verschlüsseln sie, 	und senden sie über Sockets (UNIX oder TCP) an den router ... der ein weiteres 	Programm ist, das Alice ausführt. 18:13 < jrand0m> korrekt 18:14 <@hezekiah> OK. Es ist also ein bisschen so, als würde isproxy in zwei Teile gesplittet. 18:14 < jrand0m> Bingo :) 18:14 <@hezekiah> Ein Teil ist Low-End und in C geschrieben, und der andere ist 	High-End und in was auch immer. 18:14 < jrand0m> genau 18:14 <@hezekiah> OK. Ich hab’s verstanden. :) 18:14 < jrand0m> w00t 18:14 <@hezekiah> Also muss keine Sprache mit einer anderen Sprache kompatibel sein. 18:14 < jrand0m> WinBear> sorry, ich kann es nicht ins Wiki werfen, da es nur 	Text nimmt :/ 18:15 <@hezekiah> Da sie alle über Sockets mit dem router kommunizieren, 	könntest du für den Entwurf genauso gut eine API in PASCAL schreiben. 18:15 <@nop> ja 18:15 <@nop> beliebig 18:15 < jrand0m> richtig 18:15 <@nop> es kann beliebige Sockets handhaben 18:15 < jrand0m> allerdings müssen einige Dinge standardisiert werden (z. B. die Daten- 	strukturen für Destination (Zieladresse), Lease (Lease‑Eintrag) usw.) 18:15 < WinBear> jrand0m: ich glaube, ich verstehe es in etwa, basierend darauf, was hezekiah sagt 18:15 < jrand0m> word 18:16 <@hezekiah> jrand0m: Richtig. Die Struktur und Reihenfolge der Bytes, die 	über diesen Socket gehen, ist irgendwo in einem Design festgelegt 18:16 <@hezekiah> irgendwo. 18:17 <@hezekiah> Aber du kannst immer noch beliebig implementieren, wie diese Bytes gesendet und 	empfangen werden. 18:17 <@nop> WinBear: Es ist genau dieselbe Art, wie der IRC-Client mit isproxy 	arbeitet 18:17 < jrand0m> genau 18:17 <@hezekiah> Gut. 18:17 <@hezekiah> Ich verstehe es jetzt. :) 18:17 -!- moltar [~me@anon.iip] hat #iip-dev verlassen [moltar] 18:17 <@nop> nun 18:17 <@nop> nicht ganz genau 18:17 <@hezekiah> Uh oh. 18:17 <@nop> aber stell dir vor, wie das funktioniert 18:17 <@nop> dann verstehst du beliebige Sockets 18:17 <@nop> isproxy leitet nur weiter 18:17 <@nop> und liefert aus 18:18 <@nop> jetzt, jrand0m 18:18 <@nop> kurze Frage 18:18 < jrand0m> si sr? 18:18 <@nop> ist diese API nur für neue Anwendungen gedacht, die für dieses Netzwerk 	entwickelt werden 18:18 -!- mode/#iip-dev [+v logger] durch hezekiah 18:18 < WinBear> nop: wobei das Highlevel den IRC-Client ersetzt? 18:18 < jrand0m> nop> ja. obwohl ein SOCKS5-Proxy diese API ebenfalls nutzen könnte 18:18 <@nop> oder kann es einen Mittelsmann geben, der bereits existierende 	Standard-Clients ermöglicht 18:18 <@nop> zum Beispiel 18:19 <@nop> sodass wir nur den Mittelsmann -> API schreiben müssten 18:19 < jrand0m> (aber beachte, dass es keinen 'lookup'-Dienst gibt - 	kein DNS für dieses Netzwerk) 18:19 < jrand0m> korrekt 18:19 <@nop> damit wir z. B. Mozilla unterstützen können usw. 18:19 <@nop> sodass sie einfach Plugins coden können 18:19 < jrand0m> nop> ja 18:19 <@nop> ok 18:19 <@nop> oder Transports :) 18:20 < jrand0m> (z. B. hat der SOCKS5 die HTTP-Outproxies fest verdrahtet auf 	destination1, destination2 und destination3) 18:20 <@nop> ok 18:20 < WinBear> ich glaube, ich verstehe es 18:21 < jrand0m> w00t 18:21 < jrand0m> ok, eines der Dinge, über die ich in diesem Design nachdenken musste, 	war, die privaten Schlüssel im Speicherbereich der App zu behalten – der router nie 	die privaten Schlüssel einer Destination in die Hände bekommt. 18:21 <@hezekiah> Also kann die Anwendung Rohdaten über das I2P-Netzwerk 	senden, indem sie sie an die API schickt, und muss sich um den Rest nicht kümmern. 18:22 <@hezekiah> Richtig? 18:22 < jrand0m> das bedeutet, die APIs müssen den End-to-End-Teil 	der Kryptographie implementieren 18:22 < jrand0m> genau, hezekiah 18:22 <@hezekiah> OK. 18:22 <@nop> ja 18:22 <@nop> das ist die Idee 18:22 <@nop> es erledigt das für dich 18:22 <@nop> du rufst nur den Hook auf 18:23 <@hezekiah> Eine kurze Frage: 18:23 <@hezekiah> Dieser 'router' muss über seine Transports offensichtlich ein bestimmtes Protokoll 	sprechen. 18:23 < jrand0m> korrekt 18:23 <@hezekiah> Also ist es möglich, mehrere Implementierungen des 	routers bereitzustellen ... 18:23 < jrand0m> ja 18:24 <@hezekiah> ... solange sie alle dasselbe Protokoll sprechen. 18:24 < jrand0m> (deshalb hat die Spez Platzhalter für bitbuckets) 18:24 < jrand0m> right 18:24 <@hezekiah> Also hast du einen router in Java, und einen in C, und einen 	in PASCAL. 18:24  * jrand0m verzieht das Gesicht 18:24 < jrand0m> aber ja 18:24 <@hezekiah> Und alle können miteinander reden, da sie über 	TCP/IP mit demselben Protokoll sprechen. 18:24  * WinBear springt 18:24 <@hezekiah> jrand0m: Und ja. Ich erinnere mich auch nicht übermäßig 	gern an meine PASCAL-Zeiten. 18:25 < jrand0m> nun, Pascal kann z. B. über den TCP-Transport mit dem in C sprechen, 	und der in C kann über den HTTP-Transport mit dem in Java sprechen 18:25 <@hezekiah> Richtig. 18:25 < jrand0m> (Transports sprechen mit gleichartigen Transports, router verwalten 	die zwischen ihnen zugestellten Nachrichten, kümmern sich aber nicht darum, wie sie zugestellt werden) 18:26 <@hezekiah> Mein Punkt war, dass das Protokoll dasselbe ist; daher spielt es 	keine Rolle, in welcher Sprache jemandes router implementiert ist. 18:26 < jrand0m> right 18:26 <@hezekiah> Cool. 18:26 < jrand0m> jetzt verstehst du, warum ich bei all den C-gegen-Java-etc.-Debatten "who cares" 	gesagt habe?  :) 18:26 <@hezekiah> Jap. 18:26 <@hezekiah> lol 18:27 <@hezekiah> Da muss ich dir Respekt zollen, jrand0m. Das wird es sehr 	angenehm für Entwickler machen, Programme für dieses Netzwerk zu schreiben. 18:27 < jrand0m> heh, nun, die API ist nicht ganz originell.  so funktioniert 	Message Oriented Middleware (MOM) (nachrichtenorientierte Middleware) 18:27 <@hezekiah> Und man könnte sogar router bauen, die auf bestimmte 	plattformspezifische Funktionen spezialisiert sind (wie 64-bit CPU's). 18:28 < jrand0m> absolut 18:28 <@hezekiah> jrand0m: Bescheiden bist du auch! ;-) 18:28 <@hezekiah> Nun, sieht für mich gut aus. 18:28 < jrand0m> ok, UserX, nop, ergibt diese Trennung Sinn? 18:28 <@nop> natürlich 18:28 <@nop> ist userx noch hier 18:29 <@hezekiah> Er ist seit 1:26 untätig. 18:29 < jrand0m> ’k.  Also dann haben wir zwei Aufgaben: das Netzwerk designen, und 	designen, wie die API funktioniert. 18:29 <@nop> richtig 18:29 <@hezekiah> Kurze einfache Frage: Die APIs machen End-to-End-Krypto. Machen 	die router Krypto von Knoten zu Knoten ? 18:29 <@nop> ja 18:30 < jrand0m> ja 18:30 < jrand0m> (Transportebene) 18:30 <@hezekiah> Gut. :) 18:30 <@nop> hezekiah: in dieser Hinsicht ist es dem, was wir bisher haben, sehr ähnlich 18:30 <@nop> in that aspect 18:31 < jrand0m> ok.. äh, verdammt, thecrypto ist nicht da für Kommentare zum 	Performance-Modell. 18:31 < Neo> und für die Paranoiden: Die Apps können die pgp encryption machen, bevor 	es die API erreicht ;) 18:31 < jrand0m> absolut, neo 18:31 < jrand0m> Ich war sogar versucht, die End to end crypto aus 	der API herauszulassen und es den Apps zu überlassen... 18:31 <@hezekiah> jrand0m: Das wäre gemein. 18:31 < jrand0m> heheh 18:32 <@hezekiah> BTW, die APIs und der router kommunizieren über Sockets. 18:32 <@hezekiah> Unter UNIX: Werden sie UNIX-Sockets oder lokale TCP/IP- 	Sockets verwenden? 18:32 < jrand0m> wahrscheinlich einfach lokale tcp/ip für die Einfachheit 18:32 <@nop> moment 18:32 <@hezekiah> (Ich nehme an, man könnte einen router bauen, der beides akzeptiert.) 18:33  * hezekiah mag dieses austauschbare Teile-Setup wirklich 18:33 <@nop> wenn du kurz wartest 18:34 <@hezekiah> Warte ... :) 18:34 <@nop> rufe ich thecrypto bei ihm zuhause an 18:34 <@nop> mal sehen, ob er online kommen kann 18:34 < jrand0m> hehe word 18:34 <@hezekiah> lol 18:34  * hezekiah setzt einen starken italienischen Akzent auf 18:34 <@hezekiah> Nop ha' got ... CONNECTIONS! 18:34 < jeremiah> lo 18:34 <@nop> hey jeremiah 18:35 < jrand0m> heya jeremiah 18:35 <@nop> würdest du auf API-Ebene bei einer Python-API helfen 18:35 < jeremiah> klar 18:35  * jeremiah liest den Backlog 18:35 < jrand0m> heh word 18:35  * nop ruft an 18:36 <@nop> er ist nicht zuhause 18:36 <@nop> er ist in einer Stunde zurück 18:36 < jrand0m> ’k, hat sonst noch jemand die .xls gelesen und/oder Kommentare zu 	dem Modell? 18:37 <@hezekiah> Ich habe die .xls gelesen ... aber ich kenne mich mit p2p nicht 	so gut aus, daher war das meiste über meinem Horizont. 18:37 <@hezekiah> UserX ist gut in dem Kram. 18:37 <@nop> Ich muss es noch lesen 18:37 < jrand0m> (btw, MorphMix hatte verrückte Zahlen... sie meinten, 	dass sie erwarten könnten, dass zufällige Hosts im Netz durchschnittlich 	20-150ms Pingzeiten haben, statt der 3-500, die ich erwartet hatte) 18:37 < jrand0m> coo' 18:37 <@nop> ist es StarOffice oder OpenOffice? 18:37 < jrand0m> OpenOffice, aber ich habe es nach .xls exportiert 18:37 <@nop> was ist Excel? 18:37 < jrand0m> korrekt 18:38 <@hezekiah> BTW, zur API ... 18:38 < jrand0m> si sr? 18:38 <@hezekiah> ... in C wäre boolean ein int. 18:38 <@nop> welche E-Mail 18:38 <@nop> hezekiah: ja 18:38 <@hezekiah> Die Klassen würden als Strukturzeiger übergeben werden. 18:38 <@nop> es sei denn, du typedef’st boolean 18:39 <@hezekiah> Und die Funktionen, die byte[] verwenden, würden ein void* mit 	einem zusätzlichen Parameter nutzen, der die Länge des Puffers angibt. 18:39 <@nop> hezekiah: du bist pingelig :) 18:39 < jrand0m> nop> ich kann auf die Archive nicht zugreifen, daher bin ich nicht sicher, 	wie die Betreffzeile war, aber es war letzte Woche... 18:39 <@nop> heb dir das für später auf 18:39 <@hezekiah> nop: Pingelig? 18:39 < jrand0m> heh, ja, ihr, die an der C-API arbeiten, könnt dieses Detail ausarbeiten 18:39  * jeremiah ist mit dem Backlog fertig 18:39 <@nop> wie heißt die Datei 18:39 <@hezekiah> nop: Ich versuche nur, all die Dinge zu finden, die anders sind, 	damit wir sie, wie jrand0m es wollte, ausbügeln können. 18:40 <@hezekiah> Ich versuche, hilfreich zu sein. :) 18:40 <@nop> hezekiah: ja, wahrscheinlich außerhalb der Meeting-Zeit 18:40 < jrand0m> nop> simple_latency.xls 18:40 <@hezekiah> boolean sendMessage(Destination dest, byte[] payload); 18:40 <@hezekiah>  wäre 18:40 <@hezekiah> int sendMessage(Destination dest, void* payload, int length); 18:40 <@hezekiah> . 18:40 <@hezekiah> byte[]  recieveMessage(int msgId); 18:40 <@hezekiah>  das könnte entweder sein: 18:41 <@hezekiah> void*  recieveMessage(int msgId, int* length); 18:41 <@hezekiah>  oder 18:41 <@nop> jrand0m: got it 18:41 <@hezekiah> void recieveMessage(int msgId, void* buf, int* length); 18:41 <@hezekiah>  oder 18:41 < jrand0m> hezekia: warum nicht typedef struct { int length; void* data; 	} Payload; 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId)l 18:41 <@hezekiah> DataBlock* recieveMessage(int msgId); 18:41 < jeremiah> wo ist diese xls? 18:41 <@nop> oh iip-dev 18:41 <@hezekiah> jrand0m: Das Struct, das du gerade erwähnt hast, ist im Grunde das, was 	DataBlock ist. 18:42 < jrand0m> word, hezekiah 18:42 <@nop> Betreff more models 18:42 <@hezekiah> Wahrscheinlich hätte die C-Version DataBlocks. 18:43 <@hezekiah> Darüber hinaus ist nur zu beachten, dass jedes 	„Interface“ einfach ein Satz von Funktionen wäre. 18:43 <@hezekiah> nop: Habe ich alle Unterschiede gefunden, die es in 	einer C-API geben würde? 18:43 < jrand0m> richtig.  vielleicht #include "i2psession.h" oder so 18:43 < jeremiah> gibt es eine Mockup-Python-API? 18:44 < jrand0m> nein jeremiah, ich kenne Python nicht wirklich :/ 18:44 <@nop> Ich müsste die Java-API noch einmal durchsehen, aber ich würde sagen, dass 	du genau richtig liegst 18:44 < jrand0m> aber sie wäre wahrscheinlich der Java-API ähnlich, da Python OO ist 18:44 < jeremiah> cool, ich kann eine von der C-Version ableiten 18:44  * nop ist kein Java-Typ 18:44 < jrand0m> cool, jeremiah 18:44 < jeremiah> ist die C-API in dem Ding, das du vor ein paar Tagen geschickt hast? 18:44 <@hezekiah> Ja. Python sollte mit der Java-API umgehen können. 18:44 < jrand0m> jeremiah> das war die Java-Version 18:45 < jrand0m> oh, die Java-Version war heute 18:45 < jrand0m> die ältere war sprachunabhängig 18:45 <@hezekiah> Hmm 18:45 <@nop> UserX sagt, er sollte bei der C-API helfen können 18:45 < jrand0m> word 18:45 <@nop> er ist im Moment bei der Arbeit beschäftigt 18:46 < jrand0m> coo' 18:46 <@hezekiah> Noch eine letzte Anmerkung: Bei der C-API würde wahrscheinlich 	jede Funktion ein structure* auf die Struktur nehmen, deren „Interface“ sie in Java ist. 18:46 <@nop> hezekiah: loos good 18:46 <@nop> sieht gut aus 18:46 <@hezekiah> I2PSession       createSession(String keyFileToLoadFrom, 	Properties options); 18:46 <@hezekiah>  wäre: 18:46 <@nop> Java und seine nicht-nativen Datentypen 18:46 <@hezekiah> I2PSession* createSession(I2PClient* client, char* 	keyFileToLoadFrom, Properties* options); 18:46 <@nop> ;) 18:46 < jrand0m> hehe 18:46 < jrand0m> genau, hezekiah 18:47 < jeremiah> berücksichtigen wir Unicode? 18:47 <@hezekiah> Wie auch immer, wenn ihr mit diesen Unterschieden leben könnt, sollten die 	C- und die Java-API darüber hinaus identisch sein. 18:47 <@hezekiah> nop? Unicode? :) 18:47 < jrand0m> UTF8, wenn nicht UTF16 18:48 <@hezekiah> Vielleicht sollte Unicode auf Anwendungsebene behandelt werden. 18:48 < jrand0m> richtig, der Zeichensatz gehört komplett zum Inhalt der Nachricht 18:48 <@hezekiah> Oh. 18:48 < jeremiah> ok 18:48 <@hezekiah> Java-Strings sind Unicode, oder, jrand0m? 18:48 < jrand0m> die Bitbuckets werden alle bitgenau definiert 18:48 < jrand0m> ja, hezekiah 18:48 < jrand0m> (es sei denn, man weist sie explizit an, die Zeichensätze zu ändern) 18:49 <@hezekiah> Also wäre der String, der an die Java-API gesendet wird, anders als 	der, der an die C-API gesendet wird, sofern die C-API Strings nicht in Unicode 	implementiert. 18:49 < jrand0m> nicht relevant 18:49 <@hezekiah> OK. 18:49 < jrand0m> (app->API != API->router.  Wir definieren nur API->router) 18:49 <@hezekiah> Was ich sagen will, ist Folgendes, jrand0m: 18:50 <@hezekiah> Wenn ich mein Passwort mit der Java-API setze, geht es an den 	router und dann irgendwohin nach draußen. 18:50 < jrand0m> password?  du meinst, du erstellst eine Destination? 18:50 <@hezekiah> Dann findet er einen anderen router, der es an eine andere API 	schickt (?) die in C implementiert ist. 18:50 <@hezekiah>   void            setPassphrase(String old, String new); 18:50 <@hezekiah> Diese Funktion. 18:51 < jrand0m> hezekiah> das ist das administrative Passwort, um auf die 	administrativen Methoden des routers zuzugreifen 18:51 <@hezekiah> Ah 18:51 <@hezekiah> Gelangen irgendwelche Funktionen in der API, die Java-Strings verwenden, 	am Ende mit diesem String zu einer anderen API? 18:51 < jrand0m> 99.9% der Apps werden nur I2PSession verwenden, nicht I2PAdminSession 18:51 <@nop> außerdem: Alles, was der router transportiert, wird für die 	Übertragung im Netzwerk konvertiert, korrekt? 18:51 <@hezekiah> Falls ja, sollten wir wahrscheinlich Unicode verwenden. 18:51 <@nop> Unicode wäre nicht relevant 18:52 < jrand0m> hezekiah> nein.  alle inter-router-Informationen werden durch 	Bitbuckets definiert 18:52 <@hezekiah> OK. 18:52 < jrand0m> korrekt, nop, auf der Transportebene 18:52 <@hezekiah> (Ich nehme an, ein Bitbucket ist einfach ein binärer Puffer, richtig?) 18:53 < jrand0m> ein Bitbucket ist eine Festlegung, dass das erste Bit X 	bedeutet, das zweite Bit Y, die Bits 3–42 Z usw. 18:53 < jrand0m> (z. B. wollen wir für den Zertifikate-Bitbucket vielleicht X.509 verwenden)</div>

18:53 <@hezekiah> Damit hatte ich noch nie zu tun.
18:54 <@hezekiah> Darum kümmere ich mich, wenn es so weit ist. :)
18:54 < jrand0m> heh, genau
18:55 < jrand0m> ok, die vier Dinge, die ich heute ansprechen wollte: *router 	Architektur, *Leistungsmodell, *Angriffsanalyse, *psyc.  Das erste haben wir 	erledigt, thecrypto ist offline, also verschieben wir das vielleicht (es sei denn, du hast 	Überlegungen zum Modell, nop?)
18:57 <@hezekiah> Ähm ... jrand0m. Ich habe noch eine Frage.
18:57 < jeremiah> jrand0m: wo ist die neueste Version der Netzwerkspezifikation? ist 	es die, die du am 13. verschickt hast?
18:57 < jrand0m> si sr?
18:57 <@hezekiah> Nun, die router-Architektur lässt die APIs Schlüssel 	/von der Anwendung an sie gesendet/ verarbeiten.
18:57 < jrand0m> jeremiah> ja
18:57 <@nop> Im Moment nicht
18:58 <@hezekiah> Also ... der einzige Weg, wie die API den Schlüssel erhält, ist 	über createSession.
18:58 < jrand0m> hezekiah> der router  erhält öffentliche Schlüssel und Signaturen, 	keine privaten Schlüssel
18:58 < jrand0m> genau
18:58 <@hezekiah> Aber dafür ist eine Datei erforderlich.
18:58 < jrand0m> die Schlüssel werden in einer Datei oder im Speicher der API gespeichert
18:58 < jrand0m> ja
18:58 <@hezekiah> Wenn die Anwendung einen Schlüssel erzeugt, warum kann sie ihn nicht einfach 	über einen Puffer an die API senden?
18:59 <@hezekiah> Muss sie ihn wirklich in einer Datei speichern und dann den 	Dateinamen angeben?
18:59 < jrand0m> nein, es kann im Speicher sein, wenn du möchtest
18:59 <@hezekiah> Dafür gibt es in der API aber keine Funktion.
18:59 <@hezekiah> War nur ein Gedanke.
19:00 <@hezekiah> Wenn der Schlüssel nur einmal erzeugt und dann sehr, sehr oft verwendet wird (wie GPG-Schlüssel), dann ergibt eine Datei Sinn.
19:00 -!- mihi [none@anon.iip] hat den Kanal verlassen [tschau zusammen, es wird spät...]
19:00 <@hezekiah> Wenn er jedoch häufiger erzeugt wird, wäre es vielleicht schön, 	ihn direkt über irgendeine Struktur oder einen Puffer 	an die API senden zu können
19:00 <@hezekiah> .
19:01 < jrand0m> ja, er wird einmal und nur einmal erzeugt (es sei denn, du trägst 	einen Aluhut)
19:02 < jrand0m> allerdings kannst du mit createDestination(keyFileToSaveTo) 	diesen Schlüssel erzeugen
19:02 <@hezekiah> OK.
19:02 <@hezekiah> Es gibt also wirklich keinen Bedarf, 	direkt von der App zur API zu übertragen. Eine Datei reicht aus.
19:03 <@hezekiah> Also, wo waren wir, bevor ich so unhöflich unterbrochen habe? :)
19:06 < jeremiah> also arbeiten wir gerade nur an der router-API, nicht 	an der Client-API, richtig?
19:06 < jrand0m> nun, wir überspringen vorerst die Performance-Analyse 	(hoffentlich bekommen wir dazu etwas Geplänkel auf der Mailingliste, bevor nächste 	Woche ist?).  und wahrscheinlich dasselbe bzgl. Angriffsanalyse (es sei denn, jemand hat die 	neue Spezifikation gelesen und Kommentare)
19:07 <@hezekiah> Da wir das überspringen, worüber sollen wir 	jetzt sprechen?
19:07 <@hezekiah> Psyc?
19:07 < jrand0m> außer jemand hat noch andere Punkte, die er ansprechen möchte...?
19:08 <@hezekiah> Nun, ausnahmsweise ist mein Kommentarloch (auch berüchtigt als 	Mund bekannt) leer.
19:08 < jrand0m> hehe
19:09 < jrand0m> ok, hat jemand Gedanken dazu, wie die IRC-Seite der Dinge 	funktionieren wird und ob psyc relevant oder nützlich sein könnte?
19:09 < jeremiah> Nebenbemerkung (hat mich genervt): Wireds "Wired, Tired, 	Expired"-Liste hatte Waste als 'wired'
19:09 < jrand0m> heh
19:09 < jrand0m> ist dir klar, wie sehr wir alle umhauen werden?
19:09 < jeremiah> jep
19:09 <@hezekiah> jrand0m: Das setzt voraus, dass wir das zum Laufen bringen.
19:10 < jrand0m> Ich garantiere, dass es funktionieren wird.
19:10 <@hezekiah> Da draußen gibt es viele andere gescheiterte Versuche.
19:10 < jrand0m> Ich habe meinen Job gekündigt, um daran zu arbeiten.
19:10 <@hezekiah> Dann werden wir alle umhauen. :)
19:10 <@hezekiah> Ja. Wie kommt dann Brot auf den Tisch?
19:10 <@hezekiah> GPL-Code bezahlt sich nicht gut. ;-)
19:10 < jrand0m> heh
19:11 <@hezekiah> Was psyc angeht ... ich sage es mal so:
19:11 <@hezekiah> Das erste Mal habe ich davon gehört, als du uns 	dazu gemailt hast.
19:11 < jrand0m> scheiße, ich war nicht derjenige, der es gefunden hat :)
19:11 <@hezekiah> Allerdings ist IRC wahrscheinlich eines der (wenn nicht /das/ 	meistverbreiteten) Chat-Protokolle überhaupt.
19:11 <@hezekiah> Die Leute werden IRC-Apps LANGE bevor sie überhaupt /wissen/, 	was psyc ist, haben wollen.
19:11 <@hezekiah> jrand0m: Ups. Sorry. Das Detail hatte ich vergessen. :)
19:12 < jrand0m> nicht laut psyc.  deren Geschichte geht glaube ich bis 86 zurück
19:12 <@hezekiah> Worauf es hinausläuft: Die Überlegenheit des Protokolls ist 	nicht so relevant wie die Frage, wer es benutzt.
19:12 <@hezekiah> Ihre _Geschichte_ mag so weit zurückreichen.
19:12 <@hezekiah> Aber wie viele Leute _nutzen_ Psyc?
19:12 < jeremiah> ja, wenn es sie seit einem Jahr nach meiner Geburt gibt 	(hust) und sie immer noch nicht so groß sind
19:12 <@hezekiah> Mein Punkt ist: Selbst wenn es ein besseres Protokoll ist, 	benutzen die meisten Leute IRC.
19:13 <@hezekiah> Wir können das beste I2P-Netzwerk des Planeten bauen ...
19:13 -!- Ehud [logger@anon.iip] hat den Kanal verlassen [Ping-Timeout]
19:14 < jeremiah> kann jemand kurz erklären, warum uns das kümmert? Ich dachte, IRC 	wäre nur eine mögliche Anwendung, aber das Netzwerk ist flexibel genug, 	auch psyc zu unterstützen, wenn es das wollte
19:14 <@hezekiah> Genau.
19:14 <@hezekiah> Psyc kann gebaut werden ...
19:14 <@hezekiah> ... aber ich sage, wir sollten zuerst IRC machen, weil es 	mehr Leute nutzen.

19:14 <@hezekiah> jrand0m, wir können ein großartiges I2P-Netzwerk aufbauen, aber die Leute werden es nicht 	benutzen, es sei denn, es bietet etwas, das sie wollen. 19:14 < jrand0m> jeremiah> der Grund, warum psyc interessant ist, ist, dass wir IRC vielleicht 	auf dieselbe Art implementieren wollen, wie psyc funktioniert
19:15 <@hezekiah> Daher sollten wir ihnen eine 'Killer-App' bieten.
19:15 < jeremiah> ok
19:15 < jrand0m> genau, IIP ist das Invisible IRC Project und wird es Leuten 	ermöglichen, IRC zu betreiben
19:16 < jrand0m> ohne zentralen Server (oder überhaupt irgendeinen Server, genau genommen), 	ist noch viel Denkarbeit nötig, um herauszufinden, wie IRC funktionieren wird. 	psyc hat darauf eine mögliche Antwort
19:16 < jrand0m> obwohl es auch andere gibt
19:17 <@hezekiah> Wie ich sagte, psyc könnte besser sein, aber die Leute wollen IRC benutzen, 	nicht psyc.
19:17 < jrand0m> und das werden sie
19:17 < jrand0m> sie werden irc benutzen
19:17 <@hezekiah> Es geht nur um Marketing, Baby! ;-)
19:17 < jeremiah> Ich versuche heute Abend die Spezifikation und etwas zu psyc zu lesen
19:17 < jrand0m> genau
19:17 <@hezekiah> lol
19:17 < jeremiah> Wollen wir uns morgen um 5:00 UTC treffen?
19:17 <@hezekiah> Nein?
19:18 < jeremiah> oder wann auch immer
19:18 < jrand0m> Ich bin 24x7 auf iip :)
19:18 < jeremiah> ja, aber ich esse
19:18 <@hezekiah> jrand0m: Ist mir aufgefallen.
19:18 < jrand0m> 05:00 utc oder 17:00 utc?
19:18 <@hezekiah> jeremiah: LOL!
19:18 <@hezekiah> Nun, das iip-dev-Meeting beginnt offiziell um 21:00 UTC.
19:18 -!- Ehud [~logger@anon.iip] ist #iip-dev beigetreten
19:19 < jeremiah> ok, ich habe 05:00 UTC nur gesagt, weil ich einfach Quatsch geredet habe
19:19 < jeremiah> wo ist mids?
19:19 <@hezekiah> mids hat das Projekt für eine Weile verlassen.
19:19 <@hezekiah> Warst du nicht vor ein paar Meetings dabei?
19:19 < jeremiah> ok
19:19 < jeremiah> wohl nicht
19:19 <@hezekiah> Wir hatten gewissermaßen eine Abschiedsparty als Teil der Tagesordnung.
19:19 < jeremiah> oh
19:20 <@hezekiah> OK ...
19:20 <@hezekiah> Steht noch etwas auf der Tagesordnung?
19:20  * jrand0m hat auf meiner nichts mehr
19:20 < jeremiah> zu psyc:
19:20 < jeremiah> wenn das ein psyc-Feature ist, ich weiß, du hast es vor 	einer Weile erwähnt
19:20  * hezekiah hatte überhaupt nie eine Tagesordnung
19:21 <@hezekiah> pace
19:21 <@hezekiah> place
19:21 < jeremiah> Ich glaube nicht, dass es eine kluge Idee ist, wenn jeder Benutzer 	jedem anderen im Raum eine Nachricht schickt
19:21 <@hezekiah> Da!
19:21 < jrand0m> jeremiah> also würdest du redundante nominierte Pseudoserver 	die Nachrichten weiterverteilen lassen?
19:21 < jrand0m> (pseudoservers = Peers im Kanal, die die Liste 	der Benutzer haben)
19:21 < jeremiah> Ich glaube auch nicht, dass 'broadcasting' so schlau ist, aber es

seems like it'll require _sehr viel_ Bandbreite für einen bestimmten Nutzer, der vielleicht über ein Modem online ist, und mit der Verzögerung durch das Senden von sagen wir ... 20 Nachrichten einzeln würde das die Unterhaltung durcheinanderbringen
19:21 < jeremiah> Ich kenne die beste Lösung nicht, vielleicht wäre das eine
19:22 < jeremiah> Ich denke, Direktnachrichten wären gut, wenn man sie wollte, aber es gibt Fälle, in denen es wahrscheinlich nicht so wichtig ist
19:22 <@hezekiah> Die Nachricht müsste mit dem privaten Schlüssel des Autors signiert werden, um die Authentizität zu garantieren.
19:22 <@hezekiah> Auch wenn dieses Thema noch lange keine Rolle spielen wird, denke ich, dass jeremiah einen Punkt hat
19:22 < jrand0m> hezekiah> das setzt voraus, dass Nutzer nachweisbare Kommunikation wollen :)
19:23 < jrand0m> auf jeden Fall.
19:23 <@hezekiah> Wenn ich eine Nachricht an 100 Nutzer in einem Channel senden müsste ...
19:23 < jeremiah> obwohl meine durchschnittliche Nachricht nur ein paar hundert Byte hat, sodass das Senden an Hunderte von Nutzern vielleicht nicht so schwer wäre
19:23 <@hezekiah> ... nun, meine Unterhaltung wäre /sehr/ langsam.
19:23 < jeremiah> vor allem, wenn man nicht auf eine Antwort wartet
19:23 <@hezekiah> 20K, um eine Nachricht zu senden.
19:23 <@hezekiah> Ich glaube nicht. :)
19:23 < jrand0m> nun, wenn es 100 Nutzer in einem Channel gibt, muss *irgendwer* 100 Nachrichten verschicken
19:23 < jeremiah> es sind 20k?
19:23 < jeremiah> oh, stimmt
19:23 <@hezekiah> 200 Nutzer
19:24 < jeremiah> hmm
19:24 < jeremiah> wären die router darin nicht gut?
19:24 < jeremiah> wir können doch einigermaßen sicher annehmen, dass sie eine ordentliche Bandbreite haben, oder?
19:24 <@hezekiah> Ich dachte, jede Person hätte eine 'router'-Implementierung
19:24 < jrand0m> nicht wirklich.  Wenn es Relays gibt, muss der Nominierungsmechanismus das berücksichtigen
19:24 < jrand0m> ja, hezekiah
19:24 < jeremiah> ich habe die Spezifikation nicht gelesen
19:25 < jrand0m> ein router ist dein lokaler router
19:25 <@hezekiah> Uff!
19:25 <@hezekiah> Ich verwechsele eure Nicks immer noch!
19:25 <@hezekiah> lol
19:25 < jrand0m> hehe
19:25 <@hezekiah> Ähm ... wohin ist nop verschwunden?
19:25 <@hezekiah> Oh.
19:26 <@hezekiah> Er ist noch da.
19:26 <@hezekiah> Ich dachte einen Moment, er wäre weg,
19:26 < jrand0m> aber jeremiah hat recht, psyc hat ein paar Ideen, die wir in Betracht ziehen könnten, auch wenn wir sie vielleicht verwerfen wollen
19:26 <@hezekiah> Lasst uns zuerst einfach das Netzwerk zum Laufen bringen.
19:26  * jrand0m trinkt darauf
19:26 <@hezekiah> Wenn du deinen Blick zu sehr auf die Ziellinie richtest, stolperst du über den Stein 3 Zoll vor dir.
19:27  * jeremiah fühlt sich inspiriert
19:27 <@hezekiah> lol
19:27 < jrand0m> Ich fände es wirklich großartig, wenn wir uns vornehmen könnten, die Netzwerkspezifikation bis nächste Woche durchzusehen und E-Mails an iip-dev zu schicken, wann immer jemand Gedanken oder Kommentare hat.  Bin ich verrückt?
19:27 <@hezekiah> nop? Hast du noch etwas zur Tagesordnung hinzuzufügen, oder vertagen wir?
19:27 <@hezekiah> jrand0m: Nun, ich weiß nicht, ob ich das bis nächste Woche alles lesen könnte, aber ich kann es versuchen. :)
19:27 < jrand0m> heh
19:28 < jrand0m> es sind zermürbende 15 Seiten ;)
19:28 <@hezekiah> 15 Seiten?
19:28 <@hezekiah> Es sah eher nach 120 aus!
19:29 < jrand0m> heh, na ja, hängt wohl von deiner Auflösung ab ;)
19:29 < jeremiah> er hat dort viele Anker drin, das lässt es riesig aussehen
19:29 < jrand0m> hehe
19:29 <@hezekiah> Die linke Seite hat VIEL mehr als 15 Links, Kumpel!
19:29 <@hezekiah> Rück raus!
19:29 <@hezekiah> Es sind mehr als 15. :)
19:29 <@hezekiah> Oh!
19:29 <@hezekiah> Das sind keine Seiten! Das sind nur Anker!
19:29 <@hezekiah> Ich bin gerettet!
19:30  * hezekiah fühlt sich wie ein Seemann, gerade vor dem Ertrinken gerettet
19:30 < jeremiah> Klasse, schlagt auf Band 4, Kapitel 2: Nachrichten-Byte-Struktur
19:30 < jrand0m> lol
19:30 <@hezekiah> lol
19:30 <@nop> vertagen
19:30 <@hezekiah> *baf*!
19:30 <@hezekiah> Nächste Woche, 21:00 UTC, gleicher Ort.
19:30 <@hezekiah> Wir sehen uns dort. :)
19:30 < jeremiah> bis dann --- Log geschlossen Tue Jul 15 19:30:51 2003 </div>
