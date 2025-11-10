---
title: "I2P-Entwicklertreffen, 19. August 2003"
date: 2003-08-19
author: "jrand0m"
description: "54. I2P-Entwicklertreffen zu SDK-Updates, I2NP-Überprüfung, Fortschritten bei der Kryptographie und dem Entwicklungsstand"
categories: ["meeting"]
---

<h2 id="quick-recap">Kurzüberblick</h2>

<p class="attendees-inline"><strong>Anwesend:</strong> cohesion, hezekiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Sitzungsprotokoll</h2>

<div class="irc-log"> --- Protokoll geöffnet Tue Aug 19 16:56:12 2003 17:00 -!- logger [logger@anon.iip] ist #iip-dev beigetreten 17:00 -!- Thema für #iip-dev: Wöchentliche IIP-Entwicklungsmeetings und andere 	 Gespräche unter Entwicklern finden hier statt. 17:00 [Benutzer #iip-dev] 17:00 [ cohesion] [ leenookx  ] [ mihi] [ shardy_  ] [ UserXClone] 17:00 [ Ehud    ] [ logger    ] [ nop ] [ thecrypto] [ velour    ] 17:00 [ hezekiah] [ lonelynerd] [ Rain] [ UserX    ] [ WinBear   ] 17:00 -!- Irssi: #iip-dev: Insgesamt 15 Nicks [0 ops, 0 halfops, 0 voices, 15 normal] 17:00 -!- Irssi: Beitritt zu #iip-dev wurde in 7 Sek. synchronisiert 17:00 < hezekiah> Alles klar! :) 17:00 < hezekiah> Beide Logger sind am Platz. :) 17:01 < thecrypto> ja! 17:03 < hezekiah> Hmmm ... 17:03 < hezekiah> Dieses Meeting sollte vor 3 Minuten anfangen. 17:03 < hezekiah> Frag mich, was los ist. 17:04 < thecrypto> na gut, wer ist idle 17:04 < hezekiah> jrand0m ist nicht mal online. 17:04 < hezekiah> nop ist seit 15 Minuten idle. 17:05 < nop> hi 17:05 < nop> sorry 17:05 < nop> Ich bin super beschäftigt bei der Arbeit 17:05 < mihi> [22:36] * jrand0m geht zum Abendessen, bin aber innerhalb 	 einer halben Stunde fürs Meeting zurück 17:05 -!- jrand0m [~jrandom@anon.iip] ist #iip-dev beigetreten 17:05 < hezekiah> Hi, jrand0m. 17:05 < nop> hi 17:05 < nop> ok, Folgendes 17:05 < nop> Ich darf bei der Arbeit gerade nicht auf IIP gesehen werden 17:05 < nop> also melde ich mich später bei euch 17:05 < nop> Hab gestern deswegen Ärger bekommen 17:05 < nop> also 17:05 < hezekiah> Tschüss, nop. 17:05 < thecrypto> tschüss 17:06 < nop> Ich bleibe im Channel 17:06 < nop> werde nur nicht auffallen :) 17:06 < hezekiah> jrand0m? Da du in letzter Zeit am meisten redest, gibt es 	 etwas, das du auf die Agenda für dieses Meeting setzen willst? 17:07 < jrand0m> zurück 17:08 < jrand0m> ok, die Pesto-Pasta war gut. 17:08 < jrand0m> lass mich das agenda-ähnliche Zeug raussuchen 17:09 -!- Lookaround [~chatzilla@anon.iip] ist #iip-dev beigetreten 17:09 < jrand0m> x.1) I2CP SDK-Änderungen x.2) I2NP Review x.3) Polling-HTTP- 	 Transport x.4) Dev-Status x.5) TODO x.6) Plan für die nächsten zwei Wochen 17:09 < jrand0m> (setze x auf die passende Nummer in der Agenda) 17:10 < thecrypto> du bist die agencda 17:10 < hezekiah> jrand0m: Ich habe nichts zu sagen, und nop kann 17:10 < hezekiah> nicht reden. 17:10 < jrand0m> lol 17:10 < hezekiah> UserX wird höchstwahrscheinlich nichts hinzufügen (tut er 	 normalerweise nicht), also gehört die Bühne dir. :0 17:10 < hezekiah> :) 17:10 < jrand0m> 'k.  loggen wir mit? 17:10 < jrand0m> heh 17:10 < hezekiah> Ich logge alles mit. 17:10 < jrand0m> cool.  ok.  0.1) willkommen. 17:10 < jrand0m> hi. 17:11 < jrand0m> 0.2) Mailingliste 17:11 < jrand0m> die Liste ist zzt. down, so bald wie möglich wieder da.  ihr werdet es merken :) 17:11 < jrand0m> In der Zwischenzeit Wiki oder IIP zum Kommunizieren nutzen. 17:11 < jrand0m> 1.1) I2CP SDK-Änderungen 17:12 < jrand0m> Das SDK wurde mit einigen Fehlerbehebungen aktualisiert, plus 	 ein paar neue Dinge in der Spez wurden eingeführt. 17:12 < jrand0m> Ich habe gestern mit den Infos an die Liste geschrieben. 17:13 < jrand0m> hezekiah/thecrypto/jeremiah> irgendwelche Fragen zu dem, was 	 ich gepostet habe, oder Gedanken zu einem Plan, die Änderungen zu 	 implementieren?  (oder andere Alternativen, die ich nicht bedacht habe?) 17:13 < hezekiah> Ich renne wie ein kopfloses Huhn herum, um mich fürs College 	 fertigzumachen. 17:13 < jrand0m> word, verstanden. 17:13 < hezekiah> Ich habe mir kurz angeschaut, was du geschrieben hast, aber 	 noch nicht wirklich die Änderungen an der Spez angesehen. 17:13 < jrand0m> Viel Zeit haben wir von dir nicht mehr, oder... 17:13 < hezekiah> Nicht bevor ich am College bin. 17:14 < hezekiah> Sobald ich dort bin, wird man wahrscheinlich mindestens eine 	 Woche nichts von mir hören, während ich mich eingewöhne. 17:14 < jrand0m> und sobald du da bist, gibt’s viel einzurichten 	 (iirc von damals, als ich zur Uni ging ;) 17:14 < jrand0m> heh word. 17:14 < hezekiah> Bis dahin sollte ich effizienter sein und mehr Zeit haben, 	 sodass ich coden kann. 17:14 < jrand0m> cool 17:14 < thecrypto> ich mache nur Krypto, also sind die Datenstrukturen meine 	 eigentliche Sorge; sobald ich den CTS-Modus fertig habe, arbeite ich 	 wahrscheinlich daran 17:14 < hezekiah> Jedenfalls, das ist meine Einschätzung. 17:14 < jrand0m> großartig, thecrypto 17:15 < jrand0m> ok, das Gute ist, dass das SDK einwandfrei funktioniert (mit 	 den von mihi gefundenen Bugs behoben [yay mihi!]) auch ohne die 	 Aktualisierung der Spez. 17:15 -!- arsenic [~none@anon.iip] ist #iip-dev beigetreten 17:16 < jrand0m> ok, weiter zu 1.2) I2NP Review 17:16 < jrand0m> hat jemand das Dokument gelesen? 17:16 < jrand0m> ;) 17:16 < hezekiah> Ich noch nicht. 17:16 < hezekiah> Wie gesagt, ich bin derzeit ein kopfloses Huhn. 17:17 < hezekiah> BTW jrand0m, offenbar magst du es, PDFs zu verschicken. 17:17 < jrand0m> kann jeder openoffice .swx lesen? 17:17 < hezekiah> Ich kann. 17:17 < jrand0m> [wenn ja, schicke ich swx] 17:17 -!- abesimpson [~k@anon.iip] ist #iip-dev beigetreten 17:17 < thecrypto> ich kann 17:17 < hezekiah> Ich kann in einem PDF mit KGhostView nicht nach Text suchen. 17:17 < hezekiah> Das ist echt übel. 17:17 < jrand0m> das ist Mist, hezekiah 17:17 -!- mrflibble [mrflibble@anon.iip] ist #iip-dev beigetreten 17:17 < hezekiah> Die Linux-Version von Adobe Acrobat ist auch nicht besonders 	 freundlich. 17:18 < jrand0m> ok, dann statt pdf OpenOffice-Format. 17:18 < hezekiah> Cool. 17:18 < jrand0m> äh, ok.  I2NP hat ein paar kleinere Änderungen an der 	 LeaseSet-Struktur (entsprechend der I2CP-Änderung, die ich vorhin gepostet 	 habe), aber ansonsten weitgehend fertig. 17:19 < hezekiah> jrand0m: Sind all diese Dokus im CVS von cathedral? 17:19 < nop> oh 17:19 < nop> darf ich kurz reingrätschen 17:19 < hezekiah> also Kopien der PDF-Dateien, die du an die Liste geschickt 	 hast, usw. 17:19 < hezekiah> nop: Nur zu. 17:19 < nop> das ist off-topic, aber wichtig 17:19 -!- ChZEROHag [hag@anon.iip] ist #iip-dev beigetreten 17:19 < nop> IIP-dev und die Mail sind gerade etwas durcheinander 17:19 < hezekiah> Ist mir aufgefallen. 17:19 < nop> also habt bitte etwas Geduld mit uns 17:20 < nop> wir versuchen, das zum Laufen zu bringen 17:20 < nop> aber es hat SpamAssassin eingebaut 17:20 < nop> was die gute Nachricht ist 17:20 < nop> :) 17:20 < nop> und eine Menge anderer Funktionen 17:20 < jrand0m> irgendeine ETA, nop, für die Liste? 17:20  * ChZEROHag steckt seine Nase rein 17:20 < jrand0m> (ich weiß, du bist beschäftigt, kein Nörgeln, nur Neugier) 17:20 < nop> hoffentlich bis morgen 17:20 < jrand0m> cool 17:20 < nop> der Mail-Admin arbeitet daran 17:21  * hezekiah merkt an, dass jrand0m die iip-dev-Liste _wirklich_ mag. ;-) 17:21 < nop> haha 17:21 < hezekiah> Go delta407! 17:21 < nop> wie auch immer 17:21 < jrand0m> es ist am besten, Entscheidungen öffentlich zu dokumentieren, 	 hezekiah ;) 17:21 < nop> zurück zu unserem regulären Programm 17:21 < jrand0m> heh 17:21 -!- nop heißt jetzt nop_afk 17:21 < hezekiah> jrand0m: Wo waren wir? 17:21 < jrand0m> ok, zu deiner Frage hezekiah> einige sind es, aber die 	 neuesten nicht.  Ich werde auf OpenOffice-Format umstellen. 17:21 < jrand0m> statt der PDFs 17:22 < hezekiah> OK. 17:22 < hezekiah> Es wäre echt cool, wenn alle Dokus im CVS wären. 17:22 < jrand0m> definitiv, und das werden sie 17:22 < hezekiah> Dann kann ich einfach aktualisieren und weiß, dass ich die 	 neueste Ausgabe habe. 17:22 < jrand0m> (es gibt drei Entwürfe, die es bisher nicht sind) 17:22 < hezekiah> (BTW, etwas off-topic, aber ist anonymer Zugriff auf 	 cathedral schon möglich?) 17:23 < jrand0m> noch nicht. 17:23 < jrand0m> ok, bis Freitag hoffe ich, einen weiteren Entwurf von I2NP in 	 vollständiger Form zu haben [aka keine ... mehr bei den Kademlia- 	 Erklärungsteilen und Beispiel-Implementierungsdetails] 17:24 < jrand0m> Es gibt keine wesentlichen Änderungen.  nur mehr 	 Ergänzungen zur Klarstellung. 17:24 < hezekiah> Sweet. 17:24 < hezekiah> Wird es Byte-Layouts für Datenstrukturen darin geben? 17:24 < jrand0m> 1.3) I2P Polling HTTP Transport Spezifikation 17:24 < jrand0m> nein, Byte-Layouts gehören in die Datenstrukturen-Spezifikation, 	 die ins Standardformat statt HTML konvertiert werden sollte 17:25 < jrand0m> (obwohl I2NP bereits alle nötigen Byte-Layouts hat) 17:25 < jrand0m> ((wenn du es liest *hust* ;) 17:25 < hezekiah> Gut. 17:25 < hezekiah> lol 17:25 < hezekiah> Sorry dafür. 17:25 < hezekiah> Wie gesagt, ich war echt beschäftigt. 17:25 < jrand0m> heh kein Problem, du gehst bald aufs College, du sollst 	 doch feiern :) 17:25 < hezekiah> Feiern? 17:25 < jrand0m> ok, 1.3) I2NP Polling HTTP Transport Spezifikation 17:25 < hezekiah> Hmmm ... ich bin wohl einfach seltsam. 17:25 < jrand0m> heh 17:26 < jrand0m> ok, ich habe versucht, das früher zu schicken, aber ich werde 	 es gleich committen.  Es ist ein Quick-and-Dirty-Transportprotokoll, das 	 zu I2NP passt, damit routers Daten hin und her senden können, ohne direkte 	 Verbindungen (z. B. Firewalls, Proxies, etc.) 17:27 < jrand0m> Ich HOFFE, jemand sieht, wie das funktioniert, und baut 	 ähnliche Transports (z. B. bidirektionales TCP, UDP, direktes HTTP, etc.) 17:27 -!- mihi [none@anon.iip] hat quit [Ping timeout] 17:27 < hezekiah> Hmmm, nun, ich don 17:27 < jrand0m> bevor wir I2NP zur Review rausgeben, müssen wir 	 Beispiel-Transports hinzufügen, damit Leute das Gesamtbild sehen 17:27 < hezekiah> denke nicht, dass ICH bald irgendwelche Transports bauen 	 werde. ;-) 17:27 -!- WinBear_ [~WinBear@anon.iip] ist #iip-dev beigetreten 17:27 < hezekiah> TCP funktioniert für Java und Python. 17:27 < hezekiah> (Zumindest client-to-router.) 17:27 < jrand0m> kein Problem, ich stelle es nur als To-do für Leute rein, die 	 beitragen wollen 17:28 < hezekiah> Richtig. 17:28 < jrand0m> stimmt, client-router hat andere Anforderungen als 	 router-router. 17:28 < jrand0m> ok, jedenfalls, 1.4) Dev-Status 17:28 < jrand0m> wie läuft's mit CBC, thecrypto? 17:28 < thecrypto> CBC ist eingecheckt 17:28 < jrand0m> w00000t 17:28 < thecrypto> CTS ist fast fertig 17:28 < hezekiah> thecrypto: Was ist CTS? 17:29 < thecrypto> ich muss nur rausfinden, wie ich es schön implementiere 17:29 < jrand0m> CTS steht für Ciphertext Stealing :) 17:29 < hezekiah> Ah! 17:29 < thecrypto> CipherText Stealing 17:29 -!- WinBear [WinBear@anon.iip] hat quit [EOF vom Client] 17:29 < jrand0m> hast du nops Referenz dazu geholt? 17:29 < hezekiah> OK. Wir verwenden CBC mit CTS statt Padding. 17:29 < hezekiah> Hmm. 17:29 < thecrypto> im Grunde sorgt es dafür, dass die Nachricht genau die 	 richtige Länge hat 17:29 < jrand0m> ist das für die Python-Seite machbar, hezekiah? 17:29 < hezekiah> Ich muss der Python-Krypto-Bibliothek, die ich benutze, wohl 	 kräftig auf die Sprünge helfen, damit sie CTS richtig nutzt. 17:30 < hezekiah> Ich habe CTS gegenüber Padding immer bevorzugt, aber ich 	 weiß nicht, was PyCrypt macht. 17:30 < jrand0m> Was kann Python von Haus aus, um die exakte Nachrichtengröße 	 wiederherzustellen? 17:30 < thecrypto> du musst nur ändern, wie du die letzten zwei Blöcke 	 verarbeitest 17:30 < hezekiah> Ich habe das Gefühl, dass diese Bibliothek grundlegend 	 überarbeitet werden wird. 17:30 < hezekiah> jrand0m: Das CBC-Zeug in Python ist transparent. Man schickt 	 einfach den Puffer an die Verschlüsselungsfunktion des AES-Objekts. 17:31 < hezekiah> Sie spuckt Chiffretext aus.

17:31 < hezekiah> Ende der Geschichte.
17:31 < jrand0m> gilt D(E(data,key),key) == data, Byte für Byte, exakt 	 gleiche Größe?
17:31 < hezekiah> Wenn es daher auf die schräge Idee kommt, Padding statt CTS zu verwenden, 	 muss ich wohl unter die Haube und es fixen.
17:31 < jrand0m> (unabhängig von der Eingabegröße?)
17:31 -!- mihi [~none@anon.iip] ist #iip-dev beigetreten
17:31 < hezekiah> jrand0m: Ja. Das sollte so sein.
17:31 < jrand0m> hezekiah> wenn du dir genau ansehen könntest, welchen Algorithmus es 	 fürs Padding verwendet, wäre das super
17:32 < hezekiah> Genau.
17:32  * jrand0m ist zögerlich, eine Mod an einer Python-Krypto-Lib zu verlangen, wenn 	 die Lib bereits einen standardisierten und brauchbaren Mechanismus verwendet
17:32 < hezekiah> So oder so klingt CBC mit CTS gut.
17:32 < hezekiah> jrand0m: Diese Python-Krypto-Lib stinkt.
17:32 < jrand0m> heh 'k
17:33 < thecrypto> ich muss nur noch ausrechnen, wie ich mit den zwei Blöcken herumtrickse
17:33 < hezekiah> jrand0m: ElGamal muss komplett in 	 C neu geschrieben werden, nur um es schnell genug nutzbar zu machen.
17:33 < jrand0m> hezekiah> was ist der Benchmark für Python-ElG von 256 Bytes? 	 das wird pro dest-dest-Kommunikation nur einmal gemacht...
17:34 < jrand0m> (falls du das aus dem Stegreif weißt)
17:34 < hezekiah> Ich müsste das testen.
17:34 < hezekiah> Die Verschlüsselung dauert glaube ich nur ein oder zwei Sekunden
17:34 < jrand0m> < 5 Sek., < 2 Sek., > 10 Sek., > 30 Sek?
17:34 < thecrypto> ich werde vermutlich ein bisschen damit arbeiten
17:34 < hezekiah> Die Entschlüsselung liegt vielleicht irgendwo zwischen 5 und 10 Sekunden.
17:34 < jrand0m> cool.
17:35 < jrand0m> hezekiah> hast du mit jeremiah gesprochen oder irgendwelche 	 Neuigkeiten zum Status der Python-Client-API?
17:35 < hezekiah> thecrypto: Alles, was du tun müsstest, ist, ein C‑Modul 	 zu schreiben, das mit Python zusammenarbeitet.
17:35 < hezekiah> Keine Ahnung, was er so treibt.
17:35 < hezekiah> Ich habe seit meiner Rückkehr nicht mit ihm gesprochen.
17:35 < jrand0m> 'k
17:35 < jrand0m> sonst noch Gedanken zum Dev-Status?
17:36 < hezekiah> Ähm, nicht wirklich von mir.
17:36 < hezekiah> Ich habe meinen aktuellen Freizeitstatus schon erklärt.
17:36 < jrand0m> word.  verstanden
17:36 < hezekiah> Meine einzigen Pläne sind, die C‑API fertigzustellen und den Python router 	 wieder gemäß Spec auf Stand zu bringen.
17:37 < jrand0m> 'k
17:37 < hezekiah> Oh mein Gott!
17:37 < jrand0m> 1.4) ToDo
17:37 < jrand0m> ja, Sir?
17:37 < hezekiah> Die Python-Krypto-Lib implementiert weder CTS noch Padding!
17:37 < hezekiah> Das muss ich manuell machen.
17:37 < jrand0m> hmm?  erfordert es, dass die Daten ein Vielfaches von 16 Bytes sind?
17:37 < hezekiah> Jap.
17:38 < jrand0m> heh
17:38 < jrand0m> na gut.
17:38 < hezekiah> Der Python router verwendet derzeit Padding.
17:38 < jrand0m> ok.  hier sind ein paar offene Punkte, die erledigt werden müssen.
17:38 < hezekiah> Ich erinnere mich jetzt.
17:38 < hezekiah> Nun, let
17:38 < hezekiah> Seien wir in einer Sache ehrlich.
17:38 < hezekiah> Der Python router ist eigentlich nie dazu gedacht, wirklich benutzt zu werden.
17:39 < hezekiah> Er ist in erster Linie dafür gedacht, dass ich mit der 	 Spec sehr vertraut bin, und erreicht noch etwas anderes:
17:39 < hezekiah> Er zwingt den Java router, sich _exakt_ an die Spec zu halten.
17:39 < jrand0m> beides sehr wichtige Ziele.
17:39 < hezekiah> Manchmal hält sich der Java router nicht ganz daran, und dann 	 schreit der Python router Zeter und Mordio.
17:39 < hezekiah> Also muss er nicht wirklich schnell oder stabil sein.
17:39 < jrand0m> außerdem bin ich nicht sicher, ob er nicht doch mal im SDK verwendet wird
17:39 < jrand0m> richtig.  genau.
17:39 < jrand0m> die Python-Client-API ist allerdings etwas anderes
17:39 < hezekiah> Die Python-Client-API dagegen muss ordentlich sein.
17:40 < jrand0m> genau.
17:40 < hezekiah> Aber das ist jeremiahs Problem. :)
17:40 < hezekiah> Das habe ich ihm überlassen.
17:40 < jrand0m> die reinen lokalen SDK routers sind nur für Client-Dev-Zwecke
17:40 < jrand0m> lol
17:40 < jrand0m> ok, wie ich sagte... ;)
17:40 < hezekiah> ;-)
17:41 < jrand0m> - wir brauchen jemanden, der mit einer kleinen Webseite 	 für i2p anfängt, über die die verschiedenen I2P‑bezogenen Spezifikationen für 	 Peer Review veröffentlicht werden.
17:41 < jrand0m> Ich hätte das gern bis vor dem 1.9. fertig.
17:41 < hezekiah> OK. Ich sage gleich, dass ihr nicht wollt, dass ich das mache.
17:41 < hezekiah> Ich bin kein guter Webseitendesigner. :)
17:41 < jrand0m> ich auch nicht, falls hier jemand meinen flog gesehen hat ;)
17:41 < jrand0m> cohesion?  ;)
17:41 < hezekiah> lol
17:42 < hezekiah> Armer cohesion, immer bleibt die Drecksarbeit an ihm hängen. :-)
17:42  * cohesion liest das Backlog
17:42 < hezekiah> ;)
17:42 < jrand0m> heh
17:42 < cohesion> jrand0m: Ich mache das
17:42 < cohesion> me@jasonclinton.com
17:42 < cohesion> schick mir die Specs
17:42 < jrand0m> 'k, gracias.
17:42 < jrand0m> die Specs sind noch nicht alle fertig.
17:43 < jrand0m> aber die Inhalte, die dort stehen müssen, sind:
17:43 < cohesion> nun, was du hast und was du gerne online hättest
17:43 < jrand0m> -I2CP Spec, I2NP Spec, Polling HTTP Transport Spec, TCP 	 Transport Spec, Security Analysis, Performance Analysis, Data Structure Spec, 	 und ein Readme/Intro
17:44 < jrand0m> (diese 7 Dokumente werden im PDF- und/oder Textformat vorliegen)
17:44 < cohesion> k
17:44 < jrand0m> abgesehen vom Readme/Intro
17:45 < jrand0m> Ich hoffe, dass all diese Doks bis nächste Woche 	 (26.8.) fertig sind.  Gibt dir das genug Zeit, eine kleine Seite für einen Release am 1.9. zusammenzustellen?
17:46 < jrand0m> ok.  eine weitere Sache, die noch kommen muss, ist 	 ein I2P-Netzwerksimulator.
17:46 < jrand0m> sucht jemand ein CS‑Projekt?  ;)
17:46 < hezekiah> lol
17:46 < cohesion> jrand0m: ja, das ist machbar
17:47 < hezekiah> Ich erst in ein paar Jahren. ;-)
17:47 < jrand0m> cool cohesion
17:47 < thecrypto> nicht vor einem Jahr
17:47  * cohesion geht zurück an die Arbeit
17:47 < jrand0m> tnx cohesion
17:48 < jrand0m> ok, 1.6) die nächsten zwei Wochen.  Auf meinem Zettel steht, diese Specs, 	 Docs und Analysen bereitzustellen.  Ich werde posten &amp; committen, sobald ich kann.
17:48 < jrand0m> BITTE DIE SPECS LESEN UND KOMMENTIEREN
17:48 < jrand0m> :)
17:48 < hezekiah> jrand0m: Genau. Sobald ich Zeit habe, fange ich an zu lesen. :)
17:48 < jrand0m> Ich hätte es lieber, wenn die Leute Kommentare an die Liste posten, aber wenn 	 jemand anonym bleiben will, schickt mir die Kommentare privat, und ich poste die Antworten 	 anonym an die Liste.
17:49 < hezekiah> (Was meinst du, wie die ETA dafür ist, die OpenOffice-Dateien für die 	 Doks ins CVS zu bekommen?)
17:49 < jrand0m> Ich kann die neuesten Revs innerhalb von 10 Minuten nach Ende dieses 	 Meetings committen.
17:49 < hezekiah> Großartig. :)
17:50 < jrand0m> ok, das war’s zu 1.*.
17:50 < jrand0m> 2.x) Kommentare/Fragen/Bedenken/Rants?
17:50 < jrand0m> wie läuft die SDK‑Mod, mihi?
17:51 < jrand0m> oder bei irgendwem sonst?  :)
17:51 < hezekiah> jrand0m: Was ist diese SDK‑Mod, von der du sprichst?
17:52 < jrand0m> hezekiah> zwei Bugfixes am SDK, neulich committet (&amp; gepostet) 	 the other day
17:52 < hezekiah> Ah
17:52 < hezekiah> Nett.
17:52 < jrand0m> (Message-IDs rotieren, Writes synchronisieren)
17:52 < hezekiah> Nur die Java-Seite oder auch die Python-Seite?
17:52 < jrand0m> yo no hablo python.
17:53 < hezekiah> lol
17:53 < jrand0m> nicht sicher, ob die Bugs dort existieren.  rotierst du die Message-IDs 	 alle 255 Nachrichten und synchronisierst deine Writes?
17:54 < hezekiah> Ich glaube, der Python router macht beides
17:54 < jrand0m> cool.
17:54 < jrand0m> wir sagen dir Bescheid, wenn nicht ;)
17:54 < hezekiah> Was genau meinst du mit „synchronize your writes“?
17:55 < jrand0m> aka sicherstellen, dass nicht mehrere Nachrichten gleichzeitig an einen Client 	 geschrieben werden, wenn mehrere Clients gleichzeitig versuchen, ihm Nachrichten zu 	 senden.
17:55 < hezekiah> Alle Daten, die über die TCP‑Verbindung gesendet werden, gehen 	 in der Reihenfolge raus, in der sie entstanden sind.
17:56 < hezekiah> Also bekommst du nicht 1/2 von Nachricht A und dann 1/3 von Nachricht B.
17:56 < jrand0m> 'k
17:56 < hezekiah> Du bekommst Nachricht A und dann Nachricht B.
17:56 < hezekiah> OK ... wenn sonst niemand etwas sagen will, schlage ich vor, 	 wir vertagen das Meeting.
17:56 < mihi> mein einfaches TCP/IP über I2p scheint zu funktionieren...
17:56 < jrand0m> niiiiice!!
17:56  * mihi war ein bisschen am Idlen, sorry
17:57 < hezekiah> Hat sonst noch jemand etwas zu sagen?
17:57 < jrand0m> mihi> also können wir damit pserver laufen lassen?
17:57 < mihi> solange du nicht versuchst, auf einmal lotas Verbindungen zu erstellen.
17:57 < mihi> jrand0m: ich denke schon - ich konnte ge tgoogle darüber erreichen
17:57 < jrand0m> niiiice
17:57 < jrand0m> mihi++
17:57 < mihi> jrand0m-ava
17:57 < jrand0m> du hast also einen Outproxy und einen Inproxy?
17:58 < mihi> genau.
17:58 < jrand0m> cool
17:58 < mihi> das Ziel braucht Keys, die Quelle generiert sie bei Bedarf
17:58  * hezekiah reicht jrand0m den *baf*er. Zerschmetter das Ding, wenn du 	 fertig bist, Mann.
17:58 < jrand0m> richtig.  hoffentlich kann co's Naming Service dabei helfen, 	 sobald er fertig ist.
17:59 < jrand0m> ok cool.  mihi, sag mir oder sonst wem Bescheid, wenn wir 	 irgendwie helfen können :)
17:59 < mihi> fix das Ding mit den 128 msgids oder bau einen besseren GUARANTEED 	 Support
17:59  * jrand0m *baf*t nop_afk auf den Kopf, weil er einen echten Job hat
18:00 < mihi> jrand0m: baf-Missbrauch kostet 20 Jodeln
18:00 < jrand0m> lol
18:00 < jrand0m> besserer Guaranteed Support?
18:00 < jrand0m> (aka bessere Performance als die beschriebene?  wir fixen 	 das in der Impl)
18:00 < mihi> hast du meinen Testfall mit start_thread=end_thread=300 getestet?
18:01 < mihi> der erzeugt viele Nachrichten in eine Richtung, und dadurch werden 	 alle msgids aufgefressen...
18:01 < jrand0m> hmm, nein, hatte diese Nachricht nicht gesehen
18:01 < hezekiah> jrand0m: Wäre es sinnvoll, msgid auf 2 Bytes zu machen?
18:01  * jrand0m hat 200 / 201 ausprobiert, aber das ist mit dem neuesten Fix behoben
18:01 -!- cohesion [cohesion@anon.iip] hat den Kanal verlassen [unterwegs zum LUG-Meeting]
18:01 < mihi> welcher neueste?
18:01 < hezekiah> Dann hätten sie 65535 msgids (wenn du msgid 0 nicht zählst)
18:01 < hezekiah> .
18:02 < jrand0m> 2‑Byte‑Message‑IDs würden nicht schaden.  Mit 	 der Änderung bin ich einverstanden.
18:02 < jrand0m> mihi> die, die ich dir gemailt habe
18:02 < mihi> wenn du etwas Neueres hast als das, was du mir geschickt hast, schick es 	 (oder gib mir CVS‑Zugang)
18:03 < mihi> hmm, die fällt bei mir mit 200/201 durch (sowie mit 300)
18:03 < jrand0m> hmm.  ich werde noch etwas testen und debuggen und dir mailen, 	 was ich herausfinde.
18:03 < mihi> thx.
18:04 < jrand0m> ok.
18:04  * jrand0m erklärt das Meeting
18:04 < jrand0m> *baf*'ed
18:04  * hezekiah hängt den *baf*er ehrfürchtig auf seinen speziellen Haken.
18:05  * hezekiah dreht sich dann um, geht zur Tür hinaus und knallt sie hinter 	 sich zu. Der Baffer fällt vom Haken.
18:05 < hezekiah> ;-) --- Log geschlossen Tue Aug 19 18:05:36 2003 </div>
