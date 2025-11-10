---
title: "I2P Dev Meeting - November 11, 2003"
date: 2003-11-11
author: "jrand0m"
description: "I2P-Entwicklertreffen zu den Themen router-Status, Roadmap-Updates, native modPow-Implementierung, GUI-Installer und Diskussionen zur Lizenzierung"
categories: ["meeting"]
---

(Courtesy of the wayback machine http://www.archive.org/)

## Kurzer Überblick

<p class="attendees-inline"><strong>Anwesend:</strong> dish, dm, jrand0m, MrEcho, nop</p>

(Meeting-Protokoll bearbeitet, um zu verbergen, dass iip mitten im Meeting abgestürzt ist und es viele Ping-Timeouts gab; daher versucht nicht, dies als zusammenhängende Erzählung zu lesen)

## Sitzungsprotokoll

<div class="irc-log"> [22:02] &lt;jrand0m&gt; Tagesordnung [22:02] &lt;jrand0m&gt; 0) willkommen [22:02] &lt;jrand0m&gt; 1) i2p router [22:02] &lt;jrand0m&gt; 1.1) Status [22:02] &lt;jrand0m&gt; 1.2) Änderungen an der Roadmap [22:02] &lt;jrand0m&gt; 1.3) offene Teilprojekte [22:02] &lt;jrand0m&gt; 2) native modPow [22:03] &lt;jrand0m&gt; 2) GUI-Installer [22:03] &lt;jrand0m&gt; 3) IM [22:03] &lt;jrand0m&gt; 4) Namensdienst [22:03] &lt;MrEcho&gt; ich habe diesen .c-Code gesehen [22:03] &lt;jrand0m&gt; 5) Lizenzierung [22:03] &lt;jrand0m&gt; 6) sonstiges? [22:03] &lt;jrand0m&gt; 0) willkommen [22:03] &lt;jrand0m&gt; hi. [22:03] &lt;nop&gt; hi [22:03] &lt;jrand0m&gt; Meeting 2^6 [22:04] &lt;jrand0m&gt; hast du noch Punkte für die Tagesordnung, nop? [22:04] &lt;jrand0m&gt; ok, 1.1) router-Status [22:04] &lt;jrand0m&gt; wir sind bei 0.2.0.3 und soweit ich gehört habe, ist es funktionsfähig [22:04] &lt;MrEcho&gt; &gt; 0.2.0.3 [22:04] &lt;MrEcho&gt; oder? [22:05] &lt;MrEcho&gt; ich lasse es laufen .. scheint ok [22:05] &lt;nop&gt; nein [22:05] &lt;jrand0m&gt; es gab kleine Commits nach dem 0.2.0.3-Release, nichts, was ein Release rechtfertigt [22:05] &lt;nop&gt; ich versuche nur, aufzuholen [22:05] &lt;jrand0m&gt; cool [22:06] &lt;jrand0m&gt; angesichts der Erfahrungen und Rückmeldungen zu 0.2.0.x wurde die Roadmap aktualisiert, damit der Betrieb weniger ressourcenintensiv ist [22:06] &lt;jrand0m&gt; (sprich, damit Leute Webserver / etc. betreiben können und es nicht ihre CPU frisst) [22:06] &lt;jrand0m&gt; konkret (weiter zu Punkt 1.2): http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap [22:06] &lt;MrEcho&gt; was mir aufgefallen ist: die meisten router verwenden: TransportStyle: PHTTP [22:07] &lt;MrEcho&gt; schaltet es automatisch auf phttp oder versucht es zuerst tcp [22:07] &lt;jrand0m&gt; hmm, die meisten router sollten PHTTP unterstützen, und wenn sie eingehende Verbindungen akzeptieren können, sollten sie auch TCP unterstützen [22:07] &lt;jrand0m&gt; wenn irgend möglich, verwendet es TCP [22:07] &lt;jrand0m&gt; PHTTP wird etwa 1000-mal teurer gewichtet als TCP [22:08] &lt;jrand0m&gt; (siehe GetBidsJob, das jeden Transport fragt, wie viel es kosten würde, eine Nachricht an einen Peer zu senden) [22:08] &lt;jrand0m&gt; (und siehe TCPTransport.getBid und PHTTPTransport.getBid für die verwendeten Werte) [22:08] &lt;MrEcho&gt; ok [22:08] &lt;jrand0m&gt; verwendest du PHTTP häufig zum Senden und Empfangen von Nachrichten? [22:09] &lt;jrand0m&gt; (das könnte ein Zeichen sein, dass dein TCP-Listener nicht erreichbar ist) [22:09] &lt;MrEcho&gt; ich habe die URLs auf meiner Seite nicht eingetragen [22:09] &lt;jrand0m&gt; ah 'k. [22:09] &lt;MrEcho&gt; ohh ist es [22:10] &lt;jrand0m&gt; ok, ja, meine router haben offene TCP-Verbindungen zu dir [22:10] &lt;dm&gt; wie gastfreundlich von ihnen. [22:10] * jrand0m ist froh, dass ihr mich dazu gebracht habt, routerConsole.html zu implementieren, damit wir nicht in den Logs nach diesem Mist wühlen müssen [22:11] &lt;MrEcho&gt; gibt es ein Timeout-Ding, sodass es, wenn es nicht mit tcp verbindet, auf phttp geht? und wie ist das Timing dafür [22:11] &lt;jrand0m&gt; aber wie auch immer, die große Änderung an der Roadmap ist, dass 0.2.1 das AES+SessionTag-Zeug implementieren wird [22:11] &lt;MrEcho&gt; oder könnten wir das als Einstellung haben? [22:11] &lt;jrand0m&gt; wenn es ein TCP connection refused / host not found / etc. bekommt, schlägt dieser Versuch sofort fehl und es probiert das nächste verfügbare Bid [22:12] &lt;MrEcho&gt; also keine Retries [22:12] &lt;jrand0m&gt; phttp hat ein Timeout von 30 Sekunden, iirc [22:12] &lt;jrand0m&gt; kein Grund zum erneuten Versuch. Entweder du hast eine offene TCP-Verbindung und kannst die Daten senden, oder eben nicht :) [22:12] &lt;MrEcho&gt; lol ok [22:13] &lt;MrEcho&gt; wird es danach jedes Mal tcp versuchen oder das überspringen und einfach phttp für die nächste Verbindung nehmen? [22:13] &lt;jrand0m&gt; im Moment versucht es jedes Mal tcp. [22:13] &lt;jrand0m&gt; die Transports speichern noch keine Historien [22:13] &lt;MrEcho&gt; ok, cool [22:14] &lt;jrand0m&gt; (aber wenn ein Peer 4-mal fehlschlägt, wird er für 8 Minuten auf die schwarze Liste gesetzt) [22:14] &lt;MrEcho&gt; sobald die Gegenseite die phttp-Nachricht bekommt, sollte sie sich per tcp mit dem router verbinden, der die Nachricht gesendet hat, richtig? [22:14] &lt;jrand0m&gt; korrekt. Sobald irgendeine tcp-Verbindung aufgebaut ist, kann sie verwendet werden. [22:14] &lt;jrand0m&gt; (aber wenn beide Peers nur phttp haben, werden sie natürlich nur phttp verwenden) [22:15] &lt;MrEcho&gt; das würde bedeuten, dass es zu nichts eine tcp-Verbindung herstellen konnte [22:15] &lt;MrEcho&gt; .. aber ja [22:16] &lt;MrEcho&gt; ich wünschte, es gäbe einen Weg darum herum [22:16] &lt;jrand0m&gt; nein, einer meiner router hat keine TCP-Adresse – nur PHTTP. Aber ich baue TCP-Verbindungen zu Peers auf, die TCP-Adressen haben. [22:16] &lt;jrand0m&gt; (und dann können sie Nachrichten über diese TCP-Verbindung zurückschicken, statt mir langsamere PHTTP-Nachrichten zu senden) [22:17] &lt;jrand0m&gt; oder meinst du das nicht? [22:17] &lt;MrEcho&gt; ja, ich habe mich verwechselt [22:17] &lt;jrand0m&gt; alles klar, kein Problem [22:18] &lt;jrand0m&gt; siehe die aktualisierte Roadmap für aktualisierte Zeitplan-Informationen ((Link: http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap)http://wiki.invisiblenet.net/iip-wiki?I2PRoadmap) [22:18] &lt;jrand0m&gt; ok, 1.3) offene Teilprojekte [22:19] &lt;jrand0m&gt; ich habe endlich einen Haufen aus der To-do-Liste meines PalmPilots ins Wiki gestellt unter (Link: http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects)http://wiki.invisiblenet.net/iip-wiki?OpenSubprojects [22:19] &lt;jrand0m&gt; also wenn dir langweilig ist und du nach Code-Projekten suchst... :) [22:19] &lt;MrEcho&gt; boah [22:20] &lt;MrEcho&gt; hab schon 2 [22:20] &lt;dish&gt; Du hast einen Palmpilot, das ist elitär [22:20] &lt;MrEcho&gt; meiner ist gestorben [22:20] &lt;jrand0m&gt; mihi&gt; da ist ein Punkt drin bzgl. des I2PTunnel, der einen Gedanken beschreibt, den ich vor einer Weile hatte [22:20] &lt;MrEcho&gt; weiß nicht, was damit los ist [22:21] &lt;jrand0m&gt; ja, ich hatte früher Palms, aber kürzlich wurde mir dieser hier für die Sache gespendet ;) [22:21] &lt;dish&gt; Könnte es einen Tagesordnungspunkt im Meeting geben, um zu besprechen, wann UserX das letzte Mal etwas geschrieben hat [22:21] &lt;MrEcho&gt; das verdammte Ding geht nicht mal mehr an [22:21] &lt;MrEcho&gt; lol [22:22] &lt;jrand0m&gt; Ich glaube, UserX hat seit 4 oder 5 Monaten nichts gesagt ;) [22:22] &lt;MrEcho&gt; ist das ein Bot oder so etwas? [22:22] &lt;dish&gt; Was haben sie vor 5 Monaten gesagt? [22:22] &lt;MrEcho&gt; ich wette, das ist ein bitchx, der auf irgendeiner Kiste läuft, auf die er früher Zugriff hatte .. und den er vergessen hat [22:22] &lt;jrand0m&gt; dass sie nächste Woche mit Kommentaren zum anonCommFramework (alter Name von i2p) zurückkommen würden ;) [22:23] &lt;dish&gt; haha [22:23] &lt;jrand0m&gt; aber ich vermute, er ist beschäftigt. So ist das Leben [22:23] &lt;jrand0m&gt; ok, 2) native modPow [22:23] &lt;MrEcho&gt; ich habe diesen c-code gesehen [22:24] &lt;jrand0m&gt; ich habe eine Stub-.c- und eine Java-Klasse zusammengebastelt, um zu zeigen, wie etwas wie GMP oder eine andere MPI-Bibliothek integriert werden könnte, aber es funktioniert offensichtlich nicht [22:25] &lt;jrand0m&gt; gut wäre, wenn wir ein kleines Paket aus C-Klassen und der dazugehörigen trivialen Java-Wrapper-Klasse hätten, das wir für windows, osx, *bsd, linux bauen und unter der GPL paketieren könnten

(hier schwerwiegende iip-Fehlfunktion einfügen)

[22:38] &lt;MrEcho&gt; Das Letzte, was ich gesehen habe, war: [13:25] &lt;jrand0m&gt; ok, 2) native modPow
[22:38] &lt;jrand0m&gt; Hi MrEcho
[22:38] &lt;jrand0m&gt; ja, sieht so aus, als wäre ein Haupt-Proxy abgestürzt
[22:39] &lt;jrand0m&gt; Ich gebe ihm noch 2 Minuten, bevor ich neu starte
[22:39] &lt;MrEcho&gt; k
[22:39] &lt;MrEcho&gt; für $25 einmalig kann ich vollständiges Java auf thenidus.net bekommen ... eine meiner Sites
[22:40] &lt;jrand0m&gt; $25?  Die verlangen Geld dafür, Software zu installieren?
[22:40] &lt;MrEcho&gt; Keine Ahnung eigentlich .. es ist ein Paket
[22:40] &lt;MrEcho&gt; rede gerade mit meinem Freund
[22:40] &lt;jrand0m&gt; Ich bin mir nicht sicher, ob der Code schon stabil genug ist, um loszugehen und eine Menge Colo-Plätze zu mieten, um dort routers aufzustellen.  Noch nicht :)
[22:41] &lt;dm&gt; Paket wovon?
[22:41] &lt;MrEcho&gt; java - jsp
[22:41] &lt;jrand0m&gt; ok, ich sende noch mal, was ich vorher geschickt habe:
[22:41] &lt;jrand0m&gt; Ich habe ein Stub-.c und eine Java-Klasse zusammengestellt, um zu zeigen, wie etwas wie GMP oder eine andere MPI-Bibliothek integriert werden könnte, aber es funktioniert offensichtlich nicht
[22:41] &lt;jrand0m&gt; Gut wäre, wenn wir ein kleines Paket aus C-Klassen und der zugehörigen trivialen Java-Wrapper-Klasse hätten, das wir für Windows, OSX, *BSD, Linux bauen und unter GPL (oder weniger restriktiver Lizenz) paketieren könnten
[22:41] &lt;jrand0m&gt; Mit der neuen Roadmap, die AES+SessionTag als meinen aktuellen Action Item setzt, ist das jedoch nicht mehr ganz so kritisch wie zuvor.
[22:42] &lt;jrand0m&gt; Wenn aber jemand damit loslegen möchte, wäre das großartig (und ich bin sicher, ein weiteres Projekt, das wir alle kennen, wäre an so einer Paketierung interessiert)
[22:43] &lt;dm&gt; frazaa?
[22:43] &lt;jrand0m&gt; heh, auf gewisse Weise ;)
[22:44] &lt;jrand0m&gt; ok, 3) GUI-Installer
[22:44] &lt;jrand0m&gt; MrEcho&gt; hi
[22:44] &lt;MrEcho&gt; :)
[22:44] &lt;MrEcho&gt; hehe
[22:44] &lt;MrEcho&gt; es kommt voran
[22:44] &lt;jrand0m&gt; cool
[22:44] &lt;MrEcho&gt; nichts Besonderes
[22:45] &lt;MrEcho&gt; Ich habe ein paar richtig coole Ideen, um es richtig schick zu machen .. aber das ist noch ein gutes Stück hin
[22:45] &lt;jrand0m&gt; Ich habe mich gefragt, ob der Installer hinzufügen sollte: 1) eine Option, die Seeds automatisch von http://.../i2pdb/ zu holen 2) automatisch die http://.../i2p/squid.dest zu holen und auch eine runSquid.bat/runSquid.sh zu erstellen?
[22:45] &lt;jrand0m&gt; word
[22:46] &lt;jrand0m&gt; Ja, wir wollen den Installer so einfach wie möglich halten – an welchen Schnickschnack hast du gedacht?
[22:46] &lt;MrEcho&gt; Frage ist .. wenn man java -jar installer ausführt, geht es standardmäßig in den Non-GUI-Modus, wegen der Art, wie du die Dinge eingerichtet hast
[22:46] &lt;MrEcho&gt; Wie bekommen wir es hin, dass, wenn man die JAR-Datei doppelklickt, die GUI geladen wird?
[22:47] &lt;jrand0m&gt; install.jar &lt;-- nongui,  installgui.jar &lt;-- gui
[22:47] &lt;jrand0m&gt; separater Code, separate Pakete
[22:47] &lt;MrEcho&gt; Fancy im Sinne von Dingen, die man vielleicht gar nicht bemerkt .. aber es wird schön und aufgeräumt
[22:47] &lt;jrand0m&gt; cool
[22:47] &lt;MrEcho&gt; ah ok
[22:48] &lt;jrand0m&gt; (oder install &lt;-- gui installcli &lt;-- cli.  Wir werden sehen, wie sich die Dinge entwickeln)
[22:49] &lt;jrand0m&gt; Noch etwas zur GUI, oder springen wir zu Punkt 4)?
[22:49] &lt;jrand0m&gt; (Hast du einen groben Zeitrahmen im Kopf?  Kein Druck, nur neugierig)
[22:51] &lt;MrEcho&gt; Im Moment keine Ahnung
[22:51] &lt;jrand0m&gt; cool
[22:51] &lt;jrand0m&gt; ok, 4) IM
[22:51] &lt;jrand0m&gt; thecrypto ist nicht da, also.....
[22:51] &lt;jrand0m&gt; 5) Naming Service
[22:51] &lt;jrand0m&gt; wiht ist auch nicht hier...
[22:51] &lt;jrand0m&gt; ping
[22:52] &lt;dish&gt; Du liegst bei der Nummerierung der Tagesordnung daneben
[22:52] &lt;dish&gt; 3) IM
[22:52] &lt;jrand0m&gt; Ja, ich hatte früher zwei Tagesordnungspunkte mit der Nummer 2
[22:52] &lt;dish&gt; 4) Naming
[22:52] &lt;dish&gt; ;)
[22:52] &lt;jrand0m&gt; (native modPow und GUI-Installer)
[22:52] &lt;jrand0m&gt; Siehst du, wir sind dynamisch und so
[22:59] &lt;jrand0m&gt; Ok, fürs Protokoll mache ich wohl weiter
[22:59] &lt;jrand0m&gt; 6) Lizenzierung
[23:00] &lt;jrand0m&gt; Ich denke darüber nach, weniger restriktiv als die GPL zu sein.  Wir verwenden etwas MIT-Code, plus eine weitere Datei ist GPL (aber das ist nur das Base64-Encoding und kann trivial ersetzt werden).  Ansonsten liegt das gesamte übrige Copyright entweder bei mir oder bei thecrypto.
[23:00] * dish schaut sich den I2P tunnel-Teil des Codes von mihi an
[23:01] &lt;jrand0m&gt; Ach stimmt, mihi hat das als GPL veröffentlicht, aber er kann es auch als etwas anderes veröffentlichen, wenn er möchte
[23:01] &lt;jrand0m&gt; (aber I2PTunnel ist im Grunde eine Drittanbieter-App und kann sich lizenzieren, wie es will)
[23:02] &lt;jrand0m&gt; (obwohl er, da das I2P SDK GPL ist, gezwungen war, GPL zu sein)
[23:02] &lt;MrEcho&gt; Verdammt, wurde auch Zeit
[23:02] &lt;jrand0m&gt; Weiß ich nicht.  Lizenzierung ist nicht meine Stärke, aber ich tendiere zumindest dazu, auf die LGPL zu wechseln
[23:02] * dish veröffentlicht die 10–20 Zeilen Änderung am I2P HTTP Client mihi-Code unter welcher Lizenz auch immer mihi hat
[23:03] &lt;jrand0m&gt; hehe :)
[23:06] &lt;jrand0m&gt; Wie auch immer, 7) Sonstiges?
[23:07] &lt;jrand0m&gt; Hat jemand Fragen / Bedenken / Ideen bzgl. i2p?
[23:07] &lt;dish&gt; Lass mich fragen
[23:07] &lt;dish&gt; Hat das I2P irgendeine Gruppennamen-Funktion?
[23:07] &lt;jrand0m&gt; Gruppennamen-Funktion?
[23:07] &lt;dm&gt; Team Discovery Channel!
[23:07] &lt;MrEcho&gt; lol
[23:08] &lt;dish&gt; Also, wenn man ein privates oder separates Netzwerk haben möchte, aber sich einige router irgendwie vermischen, würden ohne Gruppennamen die beiden Netzwerke zusammenwachsen
[23:08] &lt;MrEcho&gt; er denkt an waste
[23:08] &lt;jrand0m&gt; ah
[23:08] &lt;dish&gt; Ich weiß nicht, warum man das wollen würde, aber ich frage nur für den Fall
[23:08] &lt;jrand0m&gt; Ja, ganz am Anfang beim Netzwerkdesign habe ich damit gespielt
[23:09] &lt;jrand0m&gt; Das ist fortgeschrittener, als wir es jetzt brauchen (oder in der relativ nahen Zukunft [6–12 Monate]), könnte aber später integriert werden
[23:09] &lt;dish&gt; Oder ist das eine schlechte Idee, weil es besser ist, ein großes Netzwerk zu behalten
[23:09] &lt;dm&gt; i2pisdead
[23:09] &lt;jrand0m&gt; heh dm
[23:10] &lt;nop&gt; halt die Klappe
[23:10] &lt;jrand0m&gt; Nein, dish, das ist eine gute Idee
[23:10] &lt;dm&gt; nop: harter Kerl?
[23:10] &lt;jrand0m&gt; Das ist im Wesentlichen das, was Release 0.2.3 ist -- restricted routes (eingeschränkte Routen)
[23:10] &lt;jrand0m&gt; (aka du hast eine kleine private (vertrauenswürdige) Menge an Peers und willst nicht, dass jeder weiß, wer sie sind, willst aber trotzdem mit ihnen kommunizieren können)
[23:15] &lt;jrand0m&gt; Ok, noch etwas?
[23:15] &lt;nop&gt; Nee, ich bin nur witzig
[23:18] &lt;dm&gt; Witzbold?
[23:20] &lt;jrand0m&gt; Ok, nun, /interessantes/ Meeting, mit ein paar iip-Abstürzen mittendrin ;)
[23:21] * jrand0m *baf*s das Meeting zu Ende </div>
