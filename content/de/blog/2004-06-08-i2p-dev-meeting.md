---
title: "I2P-Entwicklertreffen - 8. Juni 2004"
date: 2004-06-08
author: "duck"
description: "Protokoll des I2P-Entwicklertreffens vom 08. Juni 2004."
categories: ["meeting"]
---

## Kurze Zusammenfassung

<p class="attendees-inline"><strong>Anwesend:</strong> cervantes, deer, duck, fvw, hypercubus, mihi, Nightblade, Sonium, ugha_node</p>

## Sitzungsprotokoll

<div class="irc-log"> 21:02:08 &lt;duck&gt; Tue Jun  8 21:02:08 UTC 2004 21:02:21 &lt;duck&gt; Zeit fürs Meeting 21:02:33 &lt;duck&gt; Der Bericht steht unter http://dev.i2p.net/pipermail/i2p/2004-June/000268.html 21:02:39 &lt;duck&gt; aber ich habe bei der Nummerierung einen Fehler gemacht 21:02:45 &lt;duck&gt; also wird der erste Punkt 5 übersprungen 21:02:53 &lt;hypercubus&gt; juhu! 21:03:03  * duck tut etwas Eis in sein Bier 21:03:14  * mihi würde die erste #5 in #4 umbenennen ;) 21:03:27 &lt;hypercubus&gt; nee, lass uns nächste Woche einfach zwei Punkt 4 haben ;-) 21:03:37  * duck benennt 'hypercubus' in 'mihi' um 21:03:48 &lt;hypercubus&gt; juhu! 21:03:49 &lt;duck&gt; ok 21:03:53 &lt;duck&gt; * 1) libsam 21:04:02 &lt;duck&gt; Ist Nightblade im Channel? 21:04:39 &lt;duck&gt; (inaktiv     : 0 Tage 0 Stunden 0 Min 58 Sek) 21:05:03 &lt;hypercubus&gt; ;-) 21:05:53  * duck holt sich das Mikrofon zurück 21:06:15 &lt;duck&gt; Nightblade hat eine SAM-Bibliothek für C / C++ geschrieben 21:06:23 &lt;duck&gt; bei mir lässt es sich kompilieren.. aber mehr kann ich nicht sagen :) 21:06:37 &lt;mihi&gt; keine Testfälle? ;) 21:07:06 &lt;duck&gt; falls es irgendwelche rFfreebsd-Nutzer gibt, könnte Nightblade an euch interessiert sein 21:07:08 &lt;ugha_node&gt; Die strstr-Aufrufe haben mich im Code wirklich genervt. ;) 21:07:27 &lt;ugha_node&gt; duck: Was ist ein rFfreebsd? 21:07:42 &lt;duck&gt; wie ich freebsd getippt habe 21:08:00 &lt;mihi&gt; rm -rF freebsd? 21:08:29 &lt;ugha_node&gt; Schade, dass -F mit rm nicht funktioniert. 21:08:30 &lt;duck&gt; ugha_node: ist BSD-lizenziert; also reparier's 21:08:41 &lt;fvw&gt; klingt vernünftig für mich :). Leider habe ich meine letzte freebsd-Kiste vor einer Weile deinstalliert. Ich                  habe jedoch Accounts auf den Kisten anderer Leute und bin bereit, Testfälle auszuführen. 21:08:43 &lt;ugha_node&gt; duck: Könnte sein. :) 21:08:50 &lt;duck&gt; (verdammt BSD-Hippies) 21:09:09 &lt;duck&gt; oh, schön und kurz, frank 21:09:17 &lt;duck&gt; noch weitere libsam-Kommentare? 21:09:49 &lt;duck&gt; fvw: Ich denke, Nightblade wird dich kontaktieren, wenn er Bedarf hat 21:09:50  * fvw murrt über völlig vernünftiges Unix-Verhalten, das seinen IRC-Client abgeschossen hat. 21:10:02 &lt;duck&gt; aber da seine E-Mail eine Woche alt war, hat er vielleicht schon etwas gefunden 21:10:17 &lt;mihi&gt; fvw: ? 21:10:24 &lt;fvw&gt; ja, falls jemand auf mein Angebot eingehen wollte, habe ich das irgendwie verpasst. Schickt                  mir gern eine E-Mail oder so. 21:10:42  * duck springt zu #2 21:10:46 &lt;hypercubus&gt; ähm, wohin? ;-) 21:10:54 &lt;duck&gt; 2) i2p und das normale Web mit einem Browser nutzen 21:10:57 &lt;fvw&gt; frische Installation, ich habe meiner zsh noch nicht gesagt, im Hintergrund laufendem Kram keinen HUP zu schicken.                  &lt;/offtopic&gt;

21:11:09 &lt;fvw&gt; hypercubus: Ich stehe, glaube ich, auf der öffentlichen Mailinglisten-Benutzerliste. fvw.i2p@var.cx
21:12:11 &lt;duck&gt; da gab es etwas darüber, alle TLDs zu deiner Proxy-Ausnahmeliste im Browser hinzuzufügen
21:12:23 &lt;fvw&gt; muss das diskutiert werden? Ich glaube, das wurde weitgehend auf der                  Mailingliste abgehandelt.
21:12:24 &lt;duck&gt; Ich halte das für einen dreckigen Hack
21:12:36 &lt;fvw&gt; ja, das wurde erwähnt. Willkommen zurück.
21:12:47 &lt;duck&gt; fvw: Ich hab den Thread nicht gelesen :)
21:13:12 &lt;duck&gt; okay, wenn du das nicht diskutieren willst, weiter zu #3
21:13:19 &lt;duck&gt; * 3) Chat-Kanal
21:13:23 &lt;hypercubus&gt; cervantes' Skript funktioniert perfekt unter Konqueror 3.2.2, Firefox 0.8 und                         Opera 7.51, alle für Gentoo mit KDE 3.2.2
21:13:39  * mihi markiert #4
21:13:55 &lt;duck&gt; #i2p-chat ist hier ein alternativer Kanal für Off-Topic-Chat und leichten Support
21:14:08 &lt;duck&gt; Ich weiß nicht, wer ihn registriert hat
21:14:12 &lt;hypercubus&gt; ich war's
21:14:17 &lt;duck&gt; also besser vorsichtig sein :)
21:14:22 &lt;fvw&gt; ähm, es gibt kein #4, nur zwei #5 :)
21:14:33 &lt;hypercubus&gt; Ich habe Glück, wenn ich mich an das Passwort erinnere, wenn ich es brauche ;-)
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Kanal: #i2p-chat
21:14:33 &lt;mihi&gt; [22:27] -ChanServ-      Kontakt: hypercubus <<ONLINE>>

21:14:33 <mihi> [22:27] -ChanServ-    Alternate: cervantes <<ONLINE>> 21:14:37 <mihi> [22:27] -ChanServ-   Registered: vor 4 Tagen (0h 2m 41s) 21:15:12 <hypercubus> ich habe ein paar vertrauenswürdigen Leuten Op-Rechte gegeben, für den Fall, dass ich nicht da bin und es Ärger gibt 21:15:24 <duck> klingt gut 21:15:39 <duck> könnte ein bisschen Overkill sein 21:15:51 <hypercubus> man weiß ja nie im IRC ;-) 21:15:55 <duck> aber nachdem diese protogirl hier aufgetaucht ist, dachte ich, es wäre gut, diesen Channel aufzuräumen 21:16:03 <hypercubus> heh 21:16:27 <hypercubus> wir werden es ohnehin irgendwann in den nächsten Monaten sicher brauchen 21:16:34 <duck> jups 21:16:48 <duck> und dann werfen uns die freenode-Leute raus 21:16:55 <hypercubus> ;-) 21:17:13 <duck> sie mögen nichts, was nicht in ihrem Kampf geschrieben steht 21:17:16 <duck> äh 21:17:44  * duck wechselt zu $nextitem und löst mihis Breakpoint aus 21:17:47 <hypercubus> ich dachte, den neuen Channel mit Support zu verknüpfen würde ihn für freenode legitimieren 21:18:47 <duck> hypercubus: du könntest überrascht sein 21:19:04 <hypercubus> *hust* ich habe zugegeben nicht alle Policies gelesen... 21:19:24 <duck> das ist russisches Roulette 21:19:39 <hypercubus> hmm, hätte nicht gedacht, dass es ganz so schlimm ist 21:19:52  * duck ist gerade negativ drauf 21:19:54 <hypercubus> na gut, ich schaue, was wir tun können 21:20:09 <fvw> sorry, ich muss etwas verpasst haben. Warum sollte freenode uns rausschmeißen? 21:20:21  * duck schaut auf den Timeout-Zähler für mihis Breakpoint 21:20:32 <duck> fvw: sie konzentrieren sich auf Entwicklungs-Channels 21:20:35 <mihi> ? 21:20:53 <mihi> duck: der Breakpoint wird ausgelöst bei /^4).*/ 21:21:01 <duck> mihi: aber es gibt keine #4 21:21:06 <fvw> na und? i2p ist so alpha, dass im Moment sogar Support Entwicklung ist. 21:21:11 <fvw> (und nein, du darfst mich nicht zitieren) 21:21:36 <duck> fvw: du bist vielleicht nicht mit der Art von Diskussionen vertraut, die auf IIP stattgefunden haben 21:21:38 <hypercubus> ja, aber wir haben dafür gleich *2* Channels 21:21:45 <duck> und die vermutlich in #i2p-Channels stattfinden werden 21:22:04 <duck> ich bin mir ziemlich sicher, dass freenode das nicht schätzt. 21:22:10 <Nightblade> ich bin jetzt hier 21:22:49 <hypercubus> wir spenden ihnen eine Margarita-Maschine oder so 21:22:49 <mihi> duck: worauf beziehst du dich? die Floods? oder #cl? oder was? 21:23:08 <fvw> Diskussionen auf IIP oder Diskussionen auf #iip? Ich habe auf #iip nie etwas anderes gesehen als Devel und Support. Und Diskussionen auf IIP würden nach I2P umziehen, nicht nach #i2p@freenode. 21:23:09 <duck> alle Arten von politisch unkorrektem Gerede 21:23:36 <fvw> es gibt Margarita-Maschinen? Ooh, will ich haben. 21:23:54 <duck> na gut 21:24:38 <hypercubus> sollen wir Punkt 2) erneut besprechen? 21:24:58 <duck> hypercubus: was hast du zum Browser-Proxy hinzuzufügen? 21:25:18 <hypercubus> ups, Nummer 1... da nightblade uns gerade mit seiner Anwesenheit beehrt ;-) 21:25:33 <duck> Nightblade: wir haben uns die Freiheit genommen, libsam zu „diskutieren“ 21:25:42 <Nightblade> Ok, ich sage ein paar Zeilen 21:25:48 <hypercubus> aber ja, mir ist gerade eingefallen, dass ich noch etwas zum Browser-Ding hatte, was auf der Liste nicht angesprochen wurde 21:25:56 <duck> Nightblade: fvw hat uns gesagt, dass er vielleicht mit etwas FreeBSD-Testing helfen kann 21:26:20 <fvw> Ich habe keine FreeBSD-Maschine mehr, aber ich habe Accounts auf FreeBSD-Maschinen, gib mir Testfälle, und ich führe sie gerne aus. 21:27:02 <Nightblade> Ich habe angefangen, an einer C++-DHT zu arbeiten, die Libsam (C) verwendet. Bis jetzt bin ich nicht besonders weit gekommen, obwohl ich viel daran gearbeitet habe. Im Moment können Knoten in der DHT sich gegenseitig per SAM-Daten-Nachricht „anpingen“ 21:27:09 <Nightblade> dabei habe ich ein paar kleine Bugs in libsam gefunden 21:27:18 <Nightblade> wovon ich irgendwann in Zukunft eine neue Version posten werde 21:27:51 <ugha_node> Nightblade: Könntest du bitte diese 'strstr'-Aufrufe aus libsam entfernen? :) 21:27:52 <Nightblade> der Testfall ist: versuche, es zu kompilieren, und melde mir die Fehler 21:28:01 <Nightblade> was ist falsch an strstr 21:28:21 <ugha_node> Es ist nicht dafür gedacht, statt strcmp verwendet zu werden. 21:28:38 <Nightblade> ach ja, außerdem werde ich libsam auf Windows portieren, aber das ist nicht in naher Zukunft 21:29:07 <Nightblade> ist an der Art, wie ich es benutze, irgendetwas falsch, abgesehen von der Ästhetik? 21:29:15 <Nightblade> du kannst mir Änderungen schicken oder mir sagen, was du lieber tun würdest 21:29:19 <Nightblade> das schien einfach der einfachste Weg 21:29:21 <ugha_node> Nightblade: Ist mir nichts aufgefallen. 21:29:32 <fvw> strcmp ist natürlich effizienter als strstr. 21:29:36 <ugha_node> Aber ich bin nur drübergeflogen. 21:30:20 <ugha_node> fvw: Man kann gelegentlich Dinge ausnutzen, die strstr statt strcmp verwenden, aber das ist hier nicht der Fall. 21:31:22 <Nightblade> ja, jetzt sehe ich ein paar Stellen, wo ich es ändern kann 21:31:28 <fvw> das auch, aber ich nehme an, das hättest du bemerkt. Nun, eigentlich müsstest du strncmp verwenden, um diese Exploits zu verhindern. Aber das ist nebensächlich. 21:31:31 <Nightblade> ich erinnere mich nicht, warum ich es so gemacht habe 21:31:57 <ugha_node> fvw: Einverstanden. 21:32:27 <Nightblade> oh, jetzt erinnere ich mich, warum 21:32:40 <Nightblade> es ist ein bequemer Weg, die Länge für strncmp nicht ermitteln zu müssen 21:32:49 <duck> heh 21:32:52 <ugha_node> Nightblade: Heheh. 21:33:01 <fvw> use min(strlen(foo), sizeof(*foo)) 21:33:04 <hypercubus> soll die Tracht Prügel beginnen? 21:33:15 <fvw> Ich dachte, der Oralverkehr kommt zuerst? *duckt sich* 21:33:32 <fvw> gut, nächster Punkt, denke ich. Hypercube hatte einen Kommentar zum Proxying? 21:33:38 <hypercubus> heh 21:33:54 <duck> nur her damit! 21:34:03 <Nightblade> ich werde die Änderungen für die nächste Version machen – zumindest einige davon 21:34:25 <hypercubus> ok, das wurde vor ein paar Wochen im Channel kurz besprochen, aber ich finde, wir sollten es nochmal aufgreifen 21:34:48 <deer> * Sugadude meldet sich freiwillig, den Oralverkehr zu übernehmen. 21:34:59 <hypercubus> statt TLDs zur Sperrliste deines Browsers hinzuzufügen oder das Proxy-Skript zu verwenden, gibt es einen dritten Weg 21:35:29 <hypercubus> der anonymitätsmäßig nicht dieselben Nachteile wie die beiden anderen Ansätze haben sollte 21:36:17 <fvw> den ich dir zum Spottpreis von $29,99 verrate? Raus damit! 21:36:27 <hypercubus> und zwar, dass der eeproxy eingehende HTML-Seiten so umschreibt, dass die Seite in ein Frameset eingebettet wird...  21:36:58 <hypercubus> der Hauptframe würde den angeforderten HTTP-Inhalt enthalten, der andere Frame würde als Steuerleiste dienen 21:37:13 <hypercubus> und würde dir erlauben, das Proxying nach Belieben ein-/auszuschalten 21:37:40 <hypercubus> und dich außerdem warnen, vielleicht durch farbige Ränder oder eine andere Art von Hinweis, dass du nicht anonym surfst 21:37:54 <fvw> wie willst du verhindern, dass eine i2p-Site (mit JavaScript etc.) die Anonymität ausschaltet? 21:37:59  * duck versucht, jrandom-skill-level-of tolerance anzuwenden 21:37:59 <hypercubus> oder dass ein Link auf einer eepsite-Seite ins RealWeb(tm) führt 21:38:04 <duck> cool! mach es! 21:38:16 <fvw> du wirst trotzdem etwas fproxy-Ähnliches machen müssen oder etwas Nicht-Browser-gesteuertes zum Umschalten. 21:38:29 <ugha_node> fvw: Genau. 21:39:10 <hypercubus> deshalb werfe ich das hier nochmal in die Runde, vielleicht hat jemand Ideen, wie man das absichern kann 21:39:31 <hypercubus> aber imo ist das etwas, das für die meisten i2p-Endnutzer dringend nötig sein wird 21:39:33 <hypercubus> *Nutzer 21:40:04 <hypercubus> denn die TLD-/Proxy-Skript-/dedizierter-Browser-Ansätze sind vom normalen Netznutzer zu viel verlangt 21:40:29 <fvw> Langfristig halte ich ein fproxy-Äquivalent für die beste Idee. Aber das hat meiner Meinung nach definitiv keine Priorität, und ich glaube eigentlich nicht, dass das Browsen von Sites die i2p-Killer-App sein wird. 21:40:42 <Sonium> Was ist netDb überhaupt? 21:40:59 <duck> Sonium: Datenbank bekannter routers 21:41:10 <hypercubus> fproxy ist für die meisten Nutzer zu umständlich 21:41:32 <Sonium> beeinträchtigt so eine Datenbank nicht die Anonymität? 21:41:39 <hypercubus> meiner Meinung nach ist das ein Teil des Grundes, warum Freenet in der Nicht-Dev-Community nie richtig angekommen ist 21:41:41 <fvw> hypercube: nicht unbedingt. Proxy-Autokonfiguration ("PAC") kann es so einfach machen wie das Eintragen eines einzigen Werts in deiner Browser-Konfiguration. Ich denke, wir sollten nicht unterschätzen, dass in absehbarer Zukunft alle i2p-Nutzer zumindest ein bisschen computertechnisch versiert sein werden. (trotz aller Beweise auf freenet-support) 21:42:00 <ugha_node> Sonium: Nein, „böse Buben“ könnten diese Information ohnehin manuell sammeln. 21:42:21 <Sonium> aber wenn NetDb down ist, ist i2p down, oder? 21:42:29 <fvw> hypercubus: Nicht wirklich, ich denke, dass eher die Tatsache schuld ist, dass es seit Anfang 0.5 überhaupt nicht funktioniert hat. </offtopic time="once again">

21:42:44 &lt;fvw&gt; Sonium: man kann mehr als ein netdb haben (jeder kann eines betreiben)
21:42:58 &lt;hypercubus&gt; wir haben bereits pac, und auch wenn es aus technischer Sicht                         spektakulär funktioniert, wird es in der Realität nicht die Anonymität                         des Durchschnitts-Jog schützen
21:43:03 &lt;hypercubus&gt; *Durchschnitts-Joe
21:43:22 &lt;ugha_node&gt; fvw: Ähm.. Jeder router hat sein eigenes netDb.
21:43:42 &lt;duck&gt; ok. Ich kippe gleich um. Stellt sicher, das Meeting mit *baff* zu schließen, wenn ihr                   fertig seid
21:43:52 &lt;ugha_node&gt; I2P hat keine zentralen Abhängigkeiten mehr.
21:44:07 &lt;hypercubus&gt; ok, ich wollte diese Idee nur formell in die Logs bekommen ;-)
21:44:30 &lt;fvw&gt; ugha_node: ok, dann ein veröffentlichtes netdb. Ich betreibe tatsächlich (noch) keinen Knoten, ich                  bin mit der Terminologie nicht ganz vertraut.
21:44:34 &lt;ugha_node&gt; Hmm. Wollte mihi nicht etwas sagen?
21:45:05  * fvw füttert duck mit kaffeearomatisierter Schokolade, um ihn noch ein bisschen            länger wach und am Laufen zu halten.
21:45:07 &lt;mihi&gt; nein :)
21:45:21 &lt;mihi&gt; ist duck ein Netzwerkgerät? ;)
21:45:25 &lt;ugha_node&gt; mihi: Btw, nimmst du die Prämie für die Erhöhung der Fenstergröße an?
21:45:28  * fvw füttert duck mit alkoholhaltiger Schokolade, um ihn auf unbestimmte Zeit herunterzufahren.
21:45:30 &lt;hypercubus&gt; auf Schwedisch
21:45:52 &lt;mihi&gt; ugha_node: welche Prämie?
21:46:00 &lt;hypercubus&gt; okay, dann weiter zu 5), Rant-a-Rama? ;-)
21:46:13 &lt;ugha_node&gt; mihi: http://www.i2p.net/node/view/224
21:46:27  * duck isst etwas von fvws Schokolade
21:47:16 &lt;mihi&gt; ugha_node: definitiv nein; sorry
21:47:36 &lt;ugha_node&gt; mihi: Uh, okay. :(
21:48:33  * mihi hat vor einiger Zeit versucht, die "alte" Streaming-API zusammenzuhacken, aber die war zu            fehlerhaft...
21:48:53 &lt;mihi&gt; aber es wäre meiner Meinung nach einfacher, die zu reparieren, statt meine zu reparieren...
21:49:21 &lt;ugha_node&gt; Heh.
21:49:42 &lt;hypercubus&gt; so bescheiden
21:49:46 &lt;mihi&gt; weil sie bereits eine (kaputte) "reordering"-Unterstützung enthält
21:50:49 &lt;Sonium&gt; gibt es eine Möglichkeit, deer zu fragen, wie viele Leute im i2p-#i2p-Channel sind?
21:51:01 &lt;duck&gt; nein
21:51:08 &lt;hypercubus&gt; nö, aber ich kann das zu bogobot hinzufügen
21:51:08 &lt;Sonium&gt; :/
21:51:11 &lt;Nightblade&gt; !list
21:51:13 &lt;deer&gt; &lt;duck&gt; 10 Leute
21:51:13 &lt;hypercubus&gt; sobald ich den Installer fertig habe ;-)
21:51:24 &lt;Sonium&gt; !list
21:51:32 &lt;Sonium&gt; o_O
21:51:35 &lt;mihi&gt; Sonium ;)
21:51:38 &lt;ugha_node&gt; Das ist kein fserv-Channel!
21:51:39 &lt;Sonium&gt; das war ein Trick!
21:51:40 &lt;ugha_node&gt; :)
21:51:41 &lt;hypercubus&gt; sollte !who sein
21:51:44 &lt;deer&gt; &lt;duck&gt; ant duck identiguy Pseudonym ugha2p bogobot hirvox jrandom Sugadude                   unknown
21:51:48 &lt;cervantes&gt; ups, das Meeting verpasst
21:51:57 &lt;ugha_node&gt; !list
21:52:01 &lt;Nightblade&gt; !who
21:52:11 &lt;deer&gt; &lt;duck&gt; !who-your-mom
21:52:17 &lt;mihi&gt; !who !has !the !list ?
21:52:21 &lt;fvw&gt; !yesletsallspamthechannelwithinoperativecommands
21:52:33 &lt;Nightblade&gt; !ban fvw!*@*
21:52:42 &lt;mihi&gt; !ban *!*@*
21:52:50 &lt;hypercubus&gt; ich spüre, wie gleich der Richterhammer fällt
21:52:51 &lt;duck&gt; klingt nach einem guten Zeitpunkt, es zu schließen
21:52:55 &lt;Sonium&gt; btw, du solltest auch einen !8-Befehl implementieren, wie ihn chanserv hat
21:52:59 &lt;fvw&gt; gut, jetzt hätten wir das geklärt, lass uns sch.. ja. Genau.
21:53:00  * hypercubus ist hellsichtig
21:53:05 &lt;duck&gt; *BAFF*
21:53:11 &lt;Nightblade&gt; !baff
21:53:12 &lt;hypercubus&gt; meine Haare, meine Haare
21:53:24  * fvw zeigt auf hypercube und lacht. Deine Haare! Deine Haare! </div>
