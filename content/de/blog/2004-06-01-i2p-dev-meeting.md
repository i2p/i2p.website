---
title: "I2P-Entwicklertreffen - 01. Juni 2004"
date: 2004-06-01
author: "duck"
description: "Protokoll der I2P-Entwicklungsbesprechung vom 01. Juni 2004."
categories: ["meeting"]
---

## Kurze Zusammenfassung

<p class="attendees-inline"><strong>Anwesend:</strong> deer, duck, hypercubus, Masterboy, mihi, Nightblade, tessier, wilde</p>

## Sitzungsprotokoll

<div class="irc-log"> [22:59] &lt;duck&gt; Di Jun  1 21:00:00 UTC 2004 [23:00] &lt;duck&gt; Hi Leute! [23:00] &lt;mihi&gt; Hi duck [23:00] &lt;duck&gt; http://dev.i2p.net/pipermail/i2p/2004-June/000250.html [23:00] &lt;duck&gt; mein Vorschlag: [23:00] * Masterboy ist #i2p beigetreten

[23:00] <duck> 1) Code-Fortschritt
[23:00] <duck> 2) hervorgehobene Inhalte
[23:00] <duck> 3) Testnetz-Status
[23:00] <duck> 4) Prämien
[23:00] <duck> 5) ???
[23:00] <Masterboy> hi:)
[23:00] <duck> .
[23:01] <duck> Da jrandom nicht da ist, müssen wir es selbst machen
[23:01] <duck> (Ich weiß, dass er mitloggt und unsere Unabhängigkeit überprüft)
[23:01] <Masterboy> kein Problem:P
[23:02] <duck> Sofern es keine Probleme mit der Tagesordnung gibt, schlage ich vor, dass wir dabei bleiben
[23:02] <duck> auch wenn ich nicht viel machen kann, wenn ihr das nicht tut :)
[23:02] <duck> .
[23:02] <mihi> ;)
[23:02] <duck> 1) Code-Fortschritt
[23:02] <duck> nicht viel Code in cvs eingecheckt
[23:02] <duck> Ich habe diese Woche die Trophäe gewonnen: http://duck.i2p/duck_trophy.jpg
[23:03] * hypercubus hat noch keinen cvs account
[23:03] <Masterboy> und wer hat etwas eingecheckt?
[23:03] <duck> arbeitet jemand heimlich am Code?
[23:03] * Nightblade ist #I2P beigetreten

[23:03] &lt;hypercubus&gt; BrianR hat an ein paar Sachen gearbeitet
[23:04] &lt;hypercubus&gt; Ich habe vielleicht 20% des 0.4-Installers zusammengehackt
[23:04] &lt;duck&gt; hypercubus: wenn du was hast, dann liefere Diffs und $dev wird für dich committen
[23:04] &lt;duck&gt; natürlich gelten die strengen Lizenzvereinbarungen
[23:05] &lt;duck&gt; hypercubus: cool, irgendwelche Probleme / erwähnenswerte Dinge?
[23:06] &lt;hypercubus&gt; noch nicht, aber ich werde wahrscheinlich ein paar BSD-Leute brauchen, um die Pre-Installer-Shell-Skripte zu testen
[23:06] * duck dreht ein paar Steine um
[23:06] &lt;Nightblade&gt; ist es nur textbasiert
[23:07] &lt;mihi&gt; duck: welcher davon bist du auf duck_trophy.jpg?
[23:07] &lt;mihi&gt; ;)
[23:07] &lt;Nightblade&gt; luckypunk hat FreeBSD, außerdem hat mein ISP FreeBSD, aber deren Konfiguration ist irgendwie verhunzt
[23:07] &lt;Nightblade&gt; mein Webhost-ISP, nicht Comcast
[23:08] &lt;duck&gt; mihi: der linke mit der Brille. wilde ist der rechte Typ, der mir die Trophäe überreicht
[23:08] * wilde winkt
[23:08] &lt;hypercubus&gt; du hast die Wahl... wenn du Java installiert hast, kannst du den Pre-Installer ganz überspringen...    wenn du Java nicht installiert hast, kannst du den Linux-Binary- oder Win32-Binary-Pre-Installer (Konsolenmodus) ausführen, oder einen    generischen *nix-Skript-Pre-Installer (Konsolenmodus)
[23:08] &lt;hypercubus&gt; der Haupt-Installer bietet dir die Wahl zwischen Konsolenmodus und schickem GUI-Modus
[23:08] &lt;Masterboy&gt; ich werde bald FreeBSD installieren, also werde ich den Installer in Zukunft auch ausprobieren
[23:09] &lt;hypercubus&gt; ok, gut... wusste nicht, ob außer jrandom noch jemand es benutzt
[23:09] &lt;Nightblade&gt; unter FreeBSD wird Java als "javavm" statt als "java" aufgerufen
[23:09] &lt;hypercubus&gt; aus Sun-Quellen gebaut?
[23:09] &lt;mihi&gt; FreeBSD unterstützt Symlinks ;)
[23:10] &lt;hypercubus&gt; wie auch immer, der Binary-Pre-Installer ist zu 100% fertig
[23:10] &lt;hypercubus&gt; kompiliert mit gcj zu nativem Code
[23:11] &lt;hypercubus&gt; er fragt dich nur nach dem Installationsverzeichnis und besorgt dir eine JRE
[23:11] &lt;duck&gt; w00t
[23:11] &lt;Nightblade&gt; cool
[23:11] &lt;hypercubus&gt; jrandom paketiert eine angepasste JRE für i2p

[23:12] &lt;deer&gt; &lt;j&gt; . [23:12] &lt;Nightblade&gt; wenn du Java aus der freebsd ports collection installierst, verwendest du ein Wrapper-Skript namens    javavm [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;hypercubus&gt; wie auch immer, dieses Teil wird fast vollständig automatisiert sein [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;duck&gt; r: hör auf [23:12] &lt;deer&gt; &lt;r&gt; . [23:12] &lt;deer&gt; &lt;m&gt; . [23:13] &lt;deer&gt; &lt;m&gt; doofer irc-Server, unterstützt kein Pipelining :( [23:13] &lt;duck&gt; hypercubus: hast du eine ETA für uns? [23:14] &lt;deer&gt; &lt;m&gt; oops, the problem is "Nick change too fast" :( [23:14] &lt;hypercubus&gt; ich rechne immer noch damit, in weniger als einem Monat fertig zu sein, bevor 0.4 reif für die Veröffentlichung ist [23:14] &lt;hypercubus&gt; allerdings kompiliere ich gerade ein neues Betriebssystem für mein Entwicklungssystem, daher wird es ein paar Tage dauern,    bevor ich wieder am Installer weiterarbeite ;-) [23:14] &lt;hypercubus&gt; aber keine Sorge [23:15] &lt;duck&gt; ok. also nächste Woche mehr Neuigkeiten :) [23:15] &lt;duck&gt; sonst noch irgendwas programmiert? [23:15] &lt;hypercubus&gt; hoffentlich... es sei denn, der Stromversorger macht mir wieder einen Strich durch die Rechnung [23:16] * duck wechselt zu #2 [23:16] &lt;duck&gt; * 2) empfohlene Inhalte [23:16] &lt;duck&gt; jede Menge Streaming-Audio (ogg/vorbis) diese Woche gemacht [23:16] &lt;duck&gt; baffled betreibt seinen egoplay-Stream und ich lasse auch einen Stream laufen [23:16] &lt;Masterboy&gt; und es funktioniert ziemlich gut [23:17] &lt;duck&gt; auf unserer Seite bekommst du Infos, wie man es benutzt [23:17] &lt;hypercubus&gt; hast du grobe Statistiken für uns? [23:17] &lt;duck&gt; wenn du einen dort nicht aufgeführten Player benutzt und herausfindest, wie man ihn verwendet, schick sie mir bitte und ich    füge hinzu [23:17] &lt;Masterboy&gt; duck, wo ist der Link zu baffleds Stream auf deiner Seite? [23:17] &lt;Masterboy&gt; :P [23:17] &lt;duck&gt; hypercubus: 4kB/s geht ziemlich gut [23:18] &lt;duck&gt; und mit ogg ist es nicht zuuuuu schlecht [23:18] &lt;hypercubus&gt; aber das scheint trotzdem die durchschnittliche Geschwindigkeit zu sein? [23:18] &lt;duck&gt; meine Beobachtung ist, dass das das Maximum ist [23:18] &lt;duck&gt; aber das ist alles Feintuning an der Konfiguration [23:19] &lt;hypercubus&gt; irgendeine Idee, warum das das Maximum zu sein scheint? [23:19] &lt;hypercubus&gt; und ich rede hier nicht nur vom Streaming [23:19] &lt;hypercubus&gt; sondern auch von Downloads [23:20] &lt;Nightblade&gt; ich habe gestern ein paar große Dateien (ein paar Megabyte) von ducks Hosting    Service heruntergeladen und kam ebenfalls auf etwa 4kb-5kb [23:20] &lt;duck&gt; ich denke, das ist die RTT (Round-Trip Time) [23:20] &lt;Nightblade&gt; diese Chips-Filme [23:20] &lt;hypercubus&gt; 4-5 scheint eine Verbesserung gegenüber den ~3 zu sein, die ich konstant bekomme, seit ich i2p benutze

[23:20] &lt;Masterboy&gt; 4-5kb ist nicht schlecht..
[23:20] &lt;duck&gt; mit einer windowsize von 1 wirst du nicht viel schneller..
[23:20] &lt;duck&gt; windowsize&gt;1 Prämie: http://www.i2p.net/node/view/224
[23:21] &lt;duck&gt; mihi: vielleicht kannst du dazu etwas sagen?
[23:21] &lt;hypercubus&gt; aber es sind bemerkenswert konstante 3 kbps
[23:21] &lt;mihi&gt; wobei? windowsize&gt;1 mit ministreaming: du bist ein Zauberer, wenn du das schaffst ;)
[23:21] &lt;hypercubus&gt; keine Aussetzer in der Bandbreitenanzeige... eine ziemlich glatte Linie
[23:21] &lt;duck&gt; mihi: warum es bei 4kb/s so stabil ist
[23:21] &lt;mihi&gt; keine Ahnung. Ich höre keinen Ton :(
[23:22] &lt;duck&gt; mihi: bei allen Übertragungen über i2ptunnel
[23:22] &lt;Masterboy&gt; mihi, du musst das Ogg-Streaming-Plugin konfigurieren..
[23:22] &lt;mihi&gt; Masterboy:?
[23:23] &lt;mihi&gt; nein, innerhalb von i2ptunnel gibt es keine Geschwindigkeitsbegrenzung. Das muss am router liegen...
[23:23] &lt;duck&gt; meine Überlegung: maximale Paketgröße: 32kB, rtt (Round-Trip-Zeit) von 5 Sekunden: 32kB/5s =~ 6.5kb/s
[23:24] &lt;hypercubus&gt; klingt plausibel
[23:25] &lt;duck&gt; ok..
[23:25] &lt;duck&gt; anderer Inhalt:
[23:25] * hirvox ist #i2p beigetreten

[23:25] <duck> es gibt eine neue eepsite von Naughtious
[23:25] <duck> anonynanny.i2p
[23:25] <duck> der Schlüssel ist in CVS eingecheckt und er hat ihn in ughas Wiki gestellt
[23:25] * mihi hört "sitting in the ..." - duck++
[23:25] <Nightblade> sieh mal, ob du zwei oder drei Streams mit 4kb Geschwindigkeit öffnen kannst, dann kannst du erkennen, ob es am router oder an der Streaming-Bibliothek liegt
[23:26] <duck> Naughtious: bist du da? erzähl etwas über deinen Plan :)
[23:26] <Masterboy> ich habe gelesen, dass er Hosting anbietet
[23:26] <duck> Nightblade: ich habe 3 parallele Downloads von baffled probiert und bekam 3-4kB jeweils
[23:26] <Nightblade> ich seh schon
[23:27] <mihi> Nightblade: wie kannst du das dann feststellen?
[23:27] * mihi hört gern im "Stop&Go"-Modus ;)
[23:27] <Nightblade> nun, wenn es irgendeine Begrenzung im router gibt, die ihn nur 4kb auf einmal verarbeiten lässt
[23:27] <Nightblade> oder ob es etwas anderes ist
[23:28] <hypercubus> kann jemand diese anonynanny‑Site erklären? ich habe im Moment keinen laufenden i2p router
[23:28] <mihi> hypercubus: einfach ein Wiki oder etwas in der Art
[23:28] <duck> Plone‑CMS‑Setup, offene Registrierung
[23:28] <duck> erlaubt Datei-Upload und Website‑Sachen
[23:28] <duck> über die Weboberfläche
[23:28] <Nightblade> eine andere Sache wäre, den Durchsatz des "repliable datagram" (antwortfähiges Datagramm) zu testen, was soweit ich weiß (afaik) dasselbe ist wie die Streams, nur ohne ACKs
[23:28] <duck> vermutlich so ähnlich wie Drupal
[23:28] <hypercubus> ja, ich habe Plone schon betrieben
[23:29] <duck> Nightblade: ich habe darüber nachgedacht, airhook dafür zu verwenden
[23:29] <duck> aber bisher nur ein paar grundlegende Überlegungen
[23:29] <hypercubus> ist beim Wiki‑Inhalt alles erlaubt, oder konzentriert es sich auf etwas Bestimmtes?
[23:29] <Nightblade> ich glaube, airhook ist GPL‑lizenziert
[23:29] <duck> das Protokoll
[23:29] <duck> nicht der Code
[23:29] <Nightblade> ah :)
[23:30] <duck> hypercubus: er will qualitativ hochwertigen Inhalt und lässt dich den liefern :)
[23:30] <Masterboy> lad das beste pr0n von dir hoch, das du hast, hyper ;P
[23:30] <duck> ok
[23:30] * Masterboy wird das auch versuchen
[23:30] <hypercubus> ja, wer ein offenes Wiki betreibt, bittet geradezu um Qualitätsinhalte ;-)
[23:31] <duck> ok
[23:31] * duck wechselt zu #3
[23:31] <duck> * 3) Testnet-Status
[23:31] <Nightblade> Airhook geht elegant mit intermittierenden, unzuverlässigen oder verzögerten Netzwerken um  <-- hehe, keine optimistische Beschreibung von I2P!
[23:31] <duck> wie läuft es?
[23:32] <duck> lasst uns die Diskussion über Datagramme über i2p ans Ende setzen
[23:32] <tessier> ich laufe gern in offene Wikis und verlinke das hier: http://www.fissure.org/humour/pics/squirre   l.jpg
[23:32] <tessier> airhook rockt
[23:32] <tessier> ich habe es mir auch für den Aufbau eines p2p‑Netzwerks angesehen.
[23:32] <Nightblade> wirkt auf mich zuverlässig (#3)
[23:32] <Nightblade> das Beste, was ich bisher gesehen habe
[23:33] <duck> ja
[23:33] <mihi> funktioniert gut – zumindest für Stop&Go‑Audio‑Streaming
[23:33] <duck> ich sehe ziemlich beeindruckende Uptimes auf IRC
[23:33] <hypercubus> einverstanden... sehe viel mehr blaue Leute in meiner router‑Konsole
[23:33] <Nightblade> mihi: hörst du Techno? :)
[23:33] <duck> aber schwer zu sagen, da bogobot Verbindungen, die über 00:00 hinausgehen, offenbar nicht handhabt
[23:33] <tessier> Audio‑Streaming funktioniert bei mir großartig, aber das Laden von Websites braucht oft mehrere Versuche
[23:33] <Masterboy> ich habe den Eindruck, dass i2p nach 6 Stunden Nutzung sehr gut läuft in der 6. Stunde habe ich das IRC    7 Stunden lang benutzt und so lief mein router 13hours
[23:33] <duck> (*Tipp*)
[23:34] <hypercubus> duck: äh... heheh
[23:34] <hypercubus> ich könnte das wohl beheben
[23:34] <hypercubus> hast du das Logging auf täglich gestellt?
[23:34] <duck> hypercubus++
[23:34] <hypercubus> ich meine die Logrotation
[23:34] <duck> oh ja
[23:34] <duck> duck--
[23:34] <hypercubus> deshalb
[23:34] <Nightblade> ich war den ganzen Tag bei der Arbeit, habe meinen Computer eingeschaltet, i2p gestartet und war in nur wenigen Minuten auf ducks IRC‑Server
[23:35] <duck> ich habe einige seltsame DNFs gesehen
[23:35] <duck> sogar beim Verbinden mit meinen eigenen eepsites
[23:35] <duck> (http://dev.i2p.net/bugzilla/show_bug.cgi?id=74)
[23:35] <duck> ich denke, das verursacht derzeit die meisten Probleme
[23:35] <hypercubus> bogoparser analysiert nur Uptimes, die vollständig innerhalb einer einzelnen Logdatei liegen... wenn die    Logdatei also nur 24 Stunden umfasst, wird niemand als länger als 24 Stunden verbunden angezeigt
[23:35] <duck> Masterboy und ughabugha hatten das, glaube ich, auch...
[23:36] <Masterboy> jup
[23:36] <duck> (beheb es, und du gewinnst nächste Woche sicher die Trophäe!)
[23:37] <deer> <mihi> bogobot ist aufgeregt? ;)
[23:37] <Masterboy> ich habe meine Website ausprobiert und manchmal, wenn ich Aktualisieren drücke, nimmt sie die andere Route? und ich habe zu    warten, bis sie lädt, aber ich warte nie ;P ich drücke nochmal und dann erscheint sie sofort
[23:37] <deer> <mihi> ups, sry. vergessen, dass das hier 'gated' ist...
[23:38] <duck> Masterboy: dauern die Timeouts 61 Sekunden?
[23:39] <duck> mihi: bogobot jetzt auf wöchentliche Rotationen gestellt
[23:39] * mihi hat IRC verlassen ("tschüss, und habt ein schönes Meeting")
[23:40] <Masterboy> sorry, ich habe es auf meiner Website nicht nachgesehen wenn ich sie nicht sofort erreichen kann, drücke ich einfach Aktualisieren    und sie lädt sofort..
[23:40] <duck> hm
[23:40] <duck> nun, das muss behoben werden
[23:41] <duck> .... #4
[23:41] <Masterboy> ich glaube, die Route ist nicht jedes Mal dieselbe
[23:41] <duck> * 4) bounties (Prämien)
[23:41] <duck> Masterboy: lokale Verbindungen sollten verkürzt werden
[23:42] <duck> wilde hatte ein paar Bounty‑Gedanken... bist du da?
[23:42] <Masterboy> vielleicht ist es ein Peer‑Selection‑Bug
[23:42] <wilde> ich bin nicht sicher, ob das wirklich für die Agenda war
[23:42] <duck> oh
[23:42] <wilde> ok, aber die Gedanken waren ungefähr so:
[23:42] <Masterboy> ich denke, wenn wir öffentlich gehen, wird das Bounty‑System besser funktionieren
[23:43] <Nightblade> masterboy: ja, es gibt zwei tunnels für jede Verbindung, so verstehe ich es    nachdem ich die router.config gelesen habe
[23:43] <wilde> wir könnten diesen Monat nutzen, um etwas kleine Werbung für i2p zu machen und den Bounty‑Pool etwas zu erhöhen
[23:43] <Masterboy> ich sehe, dass das Mute‑Projekt gut läuft - sie haben 600$ bekommen und noch nicht viel programmiert ;P
[23:44] <wilde> gezielt an Freedom‑Communities, Krypto‑Leute, etc
[23:44] <Nightblade> ich glaube nicht, dass jrandom Werbung will
[23:44] <wilde> keine öffentliche Slashdot‑Aufmerksamkeit, nein
[23:44] <hypercubus> das habe ich auch beobachtet
[23:44] <Masterboy> ich will es wieder pushen - wenn wir öffentlich gehen, wird das System viel besser funktionieren ;P
[23:45] <wilde> Masterboy: Bounties könnten z. B. die Entwicklung von myi2p beschleunigen
[23:45] <Masterboy> und wie jr sagte no public till 1.0 and only some attention after 0.4
[23:45] <Masterboy> *schrieb
[23:46] <wilde> wenn wir etwa 500$+ für eine Bounty haben, könnten Leute tatsächlich ein paar Wochen davon leben
[23:46] <hypercubus> das Schwierige ist: Selbst wenn wir eine kleine Dev‑Community ansprechen, wie *hust* die Mute‑Devs, könnten diese    Leute i2p weiter verbreiten, als uns lieb wäre
[23:46] <Nightblade> jemand könnte eine Karriere daraus machen, i2p‑Bugs zu beheben
[23:46] <hypercubus> und zu früh
[23:46] <wilde> i2p‑Links sind bereits an vielen öffentlichen Stellen
[23:46] <Masterboy> du googelst, und du findest i2p

[23:47] &lt;hypercubus&gt; obskure öffentliche Orte ;-) (ich habe den I2P-Link auf einer Freesite gesehen... ich habe Glück, dass die verdammte Freesite    überhaupt geladen hat!)
[23:47] &lt;wilde&gt; http://en.wikipedia.org/wiki/I2p
[23:47] &lt;Masterboy&gt; aber ich stimme zu, dass es keine Werbung gibt, bis 0.4 fertig ist
[23:47] &lt;Masterboy&gt; waaaas???????
[23:47] &lt;wilde&gt; http://www.ovmj.org/GNUnet/links.php3?xlang=English
[23:48] &lt;Masterboy&gt; protol0l macht einen großartigen Job ;P
[23:48] &lt;Masterboy&gt; ;)))))) 
[23:48] &lt;hypercubus&gt; schöner Tippfehler ;-)
[23:48] &lt;wilde&gt; ok jedenfalls, ich stimme zu, dass wir I2P vorerst privat halten sollten (jr, lies dieses Log ;)
[23:49] &lt;Masterboy&gt; wer hat das gemacht?
[23:49] &lt;Masterboy&gt; ich denke, die Freenet-Crew-Diskussion hat mehr Aufmerksamkeit gebracht..
[23:50] &lt;Masterboy&gt; und dass jr mit toad diskutiert, gibt der breiten Öffentlichkeit viele Infos..
[23:50] &lt;Masterboy&gt; also wie in ughas Wiki - wir können alle jr dafür die Schuld geben ;P
[23:50] &lt;wilde&gt; ok jedenfalls, wir werden sehen, ob wir etwas $ reinholen können, ohne /. anzulocken.
[23:50] &lt;Masterboy&gt; einverstanden
[23:50] &lt;hypercubus&gt; die freenet-dev-Liste ist kaum das, was ich die "breite Öffentlichkeit" nenne ;-)
[23:50] &lt;wilde&gt; .
[23:51] &lt;hypercubus&gt; wilde: du wirst schneller als du denkst eine Menge $ haben ;-)
[23:51] &lt;wilde&gt; ach komm, sogar meine Mutter hat freenet-devl abonniert
[23:51] &lt;duck&gt; meine Mutter liest über gmame
[23:51] &lt;deer&gt; &lt;clayboy&gt; freenet-devl wird hier in Schulen gelehrt
[23:52] &lt;wilde&gt; .
[23:52] &lt;Masterboy&gt; also werden wir mehr Bounties sehen, sobald wir 0.4 stabil sind..
[23:53] &lt;Masterboy&gt; das ist nach 2 Monaten ;P
[23:53] &lt;wilde&gt; wohin ist dieser duck gegangen?
[23:53] &lt;duck&gt; danke, wilde
[23:53] &lt;hypercubus&gt; obwohl ich bisher der einzige Bounty-Einreicher bin, muss ich sagen, dass das Kopfgeld    keinen Einfluss auf meine Entscheidung hatte, die Herausforderung anzunehmen
[23:54] &lt;wilde&gt; hehe, das hätte es, wenn es 100x gewesen wäre
[23:54] &lt;duck&gt; du bist zu gut für die Welt
[23:54] &lt;Nightblade&gt; haha
[23:54] * duck wechselt zu #5
[23:54] &lt;hypercubus&gt; wilde, $100 bedeuten mir einen Scheiß ;-)
[23:54] &lt;duck&gt; 100 * 10 = 1000
[23:55] * duck pops("5 airhook")
[23:55] &lt;duck&gt; tessier: hast du damit irgendwelche Praxiserfahrung
[23:55] &lt;duck&gt; (http://www.airhook.org/)
[23:55] * Masterboy wird das mal ausprobieren:P
[23:56] &lt;duck&gt; Java-Implementierung (keine Ahnung, ob sie überhaupt funktioniert) http://cvs.ofb.net/airhook-j/
[23:56] &lt;duck&gt; Python-Implementierung (ein Chaos, hat früher funktioniert) http://cvs.sourceforge.net/viewcvs.py/khashmir   /khashmir/airhook.py
[23:58] * duck öffnet das Rant-Ventil
[23:58] &lt;Nightblade&gt; die j ist auch GPL
[23:58] &lt;duck&gt; portiere es in die pubdomain
[23:58] &lt;hypercubus&gt; amen
[23:58] &lt;Nightblade&gt; das gesamte Protokolldokument ist nur etwa 3 Seiten lang - so schwer kann das nicht sein
[23:59] &lt;Masterboy&gt; nichts ist schwer
[23:59] &lt;Masterboy&gt; es ist nur nicht einfach
[23:59] &lt;duck&gt; ich glaube jedoch nicht, dass es vollständig spezifiziert ist
[23:59] * hypercubus nimmt masterboys Glückskekse weg
[23:59] &lt;duck&gt; du musst vielleicht in den C-Code eintauchen, um eine Referenzimplementierung zu bekommen
[00:00] &lt;Nightblade&gt; ich würde es selbst machen, aber ich bin gerade mit anderem i2p-Kram beschäftigt
[00:00] &lt;Nightblade&gt; (und außerdem meinem Vollzeitjob)
[00:00] &lt;hypercubus&gt; duck: vielleicht ein Bounty dafür?
[00:00] &lt;Nightblade&gt; gibt's schon
[00:00] &lt;Masterboy&gt; ?
[00:00] &lt;Masterboy&gt; ahh Pseudonyms
[00:00] &lt;duck&gt; es könnte auf 2 Ebenen eingesetzt werden
[00:00] &lt;duck&gt; 1) als Transport neben TCP
[00:01] &lt;duck&gt; 2) als Protokoll zur Handhabung von Datagrammen innerhalb von i2cp/sam
[00:01] &lt;hypercubus&gt; das ist dann ernsthafte Überlegung wert
[00:01] &lt;hypercubus&gt; &lt;/obvious&gt;

[00:02] &lt;Nightblade&gt; duck: Mir ist aufgefallen, dass das repliable datagram (beantwortbares Datagramm) in SAM eine maximale Größe von 31 KB hat, wohingegen der    Stream eine maximale Größe von 32 KB hat - was mich vermuten lässt, dass die Destination (I2P-Zieladresse) des Senders bei jedem Paket im    Repliable-Datagramm-Modus mitgeschickt wird und im Stream-Modus nur am Anfang -
[00:02] &lt;Masterboy&gt; nun, airhook cvs ist nicht sehr aktuell..
[00:03] &lt;Nightblade&gt; was mich denken lässt, dass es ineffizient wäre, ein Protokoll oben auf den repliable    Datagrammen über SAM aufzusetzen
[00:03] &lt;duck&gt; Die Nachrichtengröße von airhook ist 256 Byte, die von I2CP 32 KB, also musst du zumindest ein bisschen etwas ändern
[00:04] &lt;Nightblade&gt; eigentlich könntest du, wenn du das Protokoll in SAM machen wolltest, einfach das anonyme Datagramm    verwenden und das erste Paket die Destination des Senders enthalten lassen.... bla bla bla - ich habe viele Ideen, aber nicht    genug Zeit, sie zu coden
[00:06] &lt;duck&gt; andererseits hast du Probleme, Signaturen zu verifizieren
[00:06] &lt;duck&gt; also könnte dir jemand gefälschte Pakete schicken
[00:06] &lt;Masterboy&gt; Thema:::: SAM
[00:06] &lt;Masterboy&gt; ;P
[00:07] &lt;Nightblade&gt; stimmt
[00:08] &lt;Nightblade&gt; aber wenn du an diese Destination zurücksendest und keine Bestätigung kommt, wüsstest du, dass es    ein Faker war
[00:08] &lt;Nightblade&gt; es müsste einen Handshake geben
[00:08] &lt;duck&gt; aber dafür brauchst du Handshakes auf Anwendungsebene
[00:08] &lt;Nightblade&gt; nein, nicht wirklich
[00:09] &lt;Nightblade&gt; pack das einfach in eine Bibliothek für den Zugriff auf SAM
[00:09] &lt;Nightblade&gt; das ist allerdings eine schlechte Art, das zu machen
[00:09] &lt;Nightblade&gt; es so zu machen
[00:09] &lt;duck&gt; du könntest auch separate Tunnel verwenden
[00:09] &lt;Nightblade&gt; es sollte in die Streaming-Bibliothek gehören
[00:11] &lt;duck&gt; jup. ergibt Sinn
[00:12] &lt;duck&gt; ok
[00:12] &lt;duck&gt; ich fühl mich *baff*-ig
[00:13] &lt;Nightblade&gt; ja
[00:13] * duck *baffs* </div>
