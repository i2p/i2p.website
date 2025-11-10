---
title: "I2P-Entwicklertreffen, 5. August 2003"
date: 2003-08-05
author: "nop"
description: "52. I2P-Entwicklertreffen zum Status der Java-Entwicklung, zu Kryptografie-Updates und zu den Fortschritten beim SDK"
categories: ["meeting"]
---

<h2 id="quick-recap">Kurze Zusammenfassung</h2>

<p class="attendees-inline"><strong>Anwesend:</strong> hezekiah, jeremiah, jrand0m, mihi, nop, thecrypto</p>

<h2 id="meeting-log">Sitzungsprotokoll</h2>

<div class="irc-log"> <nop>	ok, Sitzung gestartet <nop>	was steht auf der Tagesordnung -->	logger (logger@anon.iip) ist #iip-dev beigetreten -->	Anon02 (~anon@anon.iip) ist #iip-dev beigetreten <hezekiah>	Tue Aug  5 21:03:10 UTC 2003 <hezekiah>	Willkommen zur n-ten iip-dev-Sitzung. <hezekiah>	Was steht auf der Tagesordnung? <thecrypto>	Tue Aug  5 21:02:44 UTC 2003 <thecrypto>	mit einem NTP Stratum-2 synchronisiert :) <hezekiah>	Tue Aug  5 21:03:13 UTC 2003 -->	ptm (~ptm@anon.iip) ist #iip-dev beigetreten <hezekiah>	Gerade mit NIST synchronisiert. :) <mihi>	diese Synchronisation hilft nicht bei iip-Verzögerungen ;) <jrand0m>	nop: Dinge, die ich besprochen sehen will: Java-Entwicklungsstatus, 	  Java-Krypto-Status, Python-Entwicklungsstatus, SDK-Status, Namensdienst <hezekiah>	(Wechseln wir etwa _schon_ zum Namensdienst?) <jrand0m>	keine Designs, du Wichser, das ist co's Schpeel.  red einfach über Zeug, 	  wenn's was zu reden gibt. <hezekiah>	Ah *	jrand0m legt den LART weg <jrand0m>	sonst noch was auf der Tagesordnung? <jrand0m>	oder legen wir los? <hezekiah>	Nun, mir fällt nichts weiter ein. <hezekiah>	Ah! <hezekiah>	Oh! <jrand0m>	ok.  Java-Entwicklungsstatus: <hezekiah>	Gut. <--	mrflibble hat den Kanal verlassen (Ping-Timeout) <nop>	ok <nop>	Tagesordnung <nop>	1) Willkommen <jrand0m>	Stand heute gibt es eine Java-Client-API mit einem Stub-Java router, 	  die miteinander sprechen können.  Außerdem gibt es eine Anwendung namens ATalk, 	  die anonymes IM + Dateitransfer erlaubt. <nop>	2) IIP 1.1-Ausfälle <nop>	3) I2P <nop>	4) Das Ende mit Kommentaren und so Zeug *	jrand0m geht zurück in die Ecke <nop>	sorry 	  joeyo jrand0m Aug 05 17:08:24 * hezekiah gibt jrand0m eine Narrenkappe zum 	  Tragen in der Ecke. ;-) <nop>	sorry dafür <nop>	hab nicht gesehen, dass ihr da schon angefangen habt <nop>	vielleicht sollte ich in die Ecke gehen <hezekiah>	lol <jrand0m>	kein Problem.  Punkt 1) *	hezekiah setzt nop auch eine Narrenkappe auf. :) <nop>	ok, willkommen allerseits <nop>	bla bla <nop>	2) IIP 1.1-Ausfälle -->	mrflibble (mrflibble@anon.iip) ist #iip-dev beigetreten <hezekiah>	Die 52. iip-dev-Sitzung und all der gute Kram! <nop>	der Server hatte kürzlich Probleme mit den Festplattensektoren und wurde 	  ersetzt <nop>	ich plane, den verfluchten Server in eine stabilere Umgebung mit 	  Redundanz zu verlegen <nop>	und möglicherweise die Kontrolle über mehrere ircd-Server zu delegieren <nop>	weiß nicht <nop>	das ist zu diskutieren <--	Anon02 hat den Kanal verlassen (EOF vom Client) <nop>	hoffentlich bleiben unsere Server jetzt online, da die Festplatte ersetzt wurde <nop>	sorry für die Unannehmlichkeiten, Leute <nop>	3) I2P - Jrand0m, leg los <nop>	komm aus der Ecke, jrand0m *	hezekiah geht rüber in die Ecke, zieht jrand0m von seinem Stuhl, zerrt ihn 	  zum Podium, nimmt ihm die Narrenkappe ab und drückt ihm das Mikro in die Hand. *	nop geht in diese Ecke, um seinen Platz einzunehmen <hezekiah>	lol! <jrand0m>	sorry, zurück *	nop schnappt sich die Narrenkappe von hezekiah *	nop setzt sie sich auf *	nop applaudiert für jrand0m *	jrand0m schaut sich einfach die Show an <jrand0m>	äh... hm ok <hezekiah>	jrand0m: i2p, Java-Status, usw. Rede, Mann! <jrand0m>	also, Stand heute gibt es eine Java-Client-API mit einem Stub-Java 	  router, die miteinander sprechen können.  Außerdem gibt es eine Anwendung 	  namens ATalk, die anonymes IM + Dateitransfer erlaubt. <hezekiah>	Schon Dateitransfer!? <jrand0m>	si sr <hezekiah>	Wow. <hezekiah>	Ich hänge wohl hinterher. <jrand0m>	aber nicht gerade elegant <hezekiah>	lol <jrand0m>	es nimmt eine Datei und wirft sie in eine Nachricht <hezekiah>	Autsch. <nop>	wie lange hat der 1.8 mb lokale Transfer gedauert? <jrand0m>	Ich habe es mit einer 4K-Datei und einer 1.8Mb-Datei getestet <jrand0m>	ein paar Sekunden <nop>	nice <nop>	:) <hezekiah>	Macht das Java-Zeug schon echte Verschlüsselung, oder 	  fälscht es das immer noch? <nop>	fake <nop>	sogar ich weiß das <nop>	:) <jrand0m>	Ich habe es vorgewärmt, indem ich erst mit mir selbst geredet habe 	  [z. B. ein Fenster zum anderen, 'hi' sagen], sodass es sich nicht mit dem Overhead 	  des ersten elg herumschlagen musste <jrand0m>	genau, es ist größtenteils gefakt <thecrypto>	das meiste der Verschlüsselung ist fake <thecrypto>	daran wird aber gearbeitet <hezekiah>	Natürlich. :) <jrand0m>	auf jeden Fall. <jrand0m>	in der Hinsicht, magst du uns ein Update geben, thecrypto? <thecrypto>	nun, aktuell bin ich mit ElGamal und SHA256 fertig <thecrypto>	gerade arbeite ich daran, Primzahlen für DSA zu generieren <thecrypto>	ich schicke 5 raus und dann können wir einfach eine auswählen <hezekiah>	nop: Hattest du nicht Primzahl(en) für DSA in Aussicht? <thecrypto>	Wir haben auch ein paar Benchmarks zu ElGamal und SHA256 <thecrypto>	Und sie sind alle schnell <jrand0m>	neueste Benchmarks mit elg: <jrand0m>	Durchschnittliche Zeit für die Schlüsselgenerierung: 4437	gesamt: 443759	min: 	  872	   max: 21110	   Keygen/Sekunde: 0 <jrand0m>	Ver- schlüsselungszeit Durchschnitt    : 356	gesamt: 35657	min: 	  431	   max: 611	   Verschlüsselung Bps: 179 <jrand0m>	Ent- schlüsselungszeit Durchschnitt    : 983	gesamt: 98347	min: 	  881	   max: 2143	   Entschlüsselung Bps: 65

<hezekiah>	min und max: sind die in Sekunden? <jrand0m>	beachte, dass die Bps nicht wirklich aussagekräftig sind, da wir nur 	  64 Bytes ver-/entschlüsseln <thecrypto>	ms <jrand0m>	nein, sorry, das sind alles Millisekunden <hezekiah>	Cool. :) <hezekiah>	Und das ist in Java gemacht? <thecrypto>	ja <thecrypto>	reines Java <hezekiah>	OK. Ich bin offiziell beeindruckt. :) <jrand0m>	100%.  P4 1.8 <thecrypto>	bei mir sind sie auf meinem 800 MHz etwa gleich <hezekiah>	Wie kann ich dieselben Tests machen? <jrand0m>	sha256 Benchmark: <jrand0m>	Short Message Time Average  : 0 total: 0	min: 0	max: 	  0  Bps: NaN <jrand0m>	Medium Message Time Average : 1 total: 130	min: 0	max: 	  10 Bps: 7876923 <jrand0m>	Long Message Time Average   : 146	total: 14641	min: 	  130	   max: 270	   Bps: 83037 <thecrypto>	führe das ElGamalBench-Programm aus <hezekiah>	OK. <hezekiah>	Ich suche es mal. <jrand0m>	(kurz: ~10 Bytes, mittel ~10KB, lang ~ 1MB) <jrand0m>	java -cp i2p.jar ElGamalBench <jrand0m>	(nachdem man "ant all" ausgeführt hat) <hezekiah>	jrand0m: Danke. :) <jrand0m>	kein Problem <thecrypto>	Das NaN-Ding bedeutet, dass es so schnell ist, dass wir am Ende durch 0 	  teilen — so schnell ist es :) <hezekiah>	Was ist der SHA-Bench? <jrand0m>	java -cp i2p.jar SHA256Bench -->	Neo (anon@anon.iip) ist #iip-dev beigetreten <hezekiah>	OK. <jrand0m>	wir werden die wahrscheinlich in main()-Methoden der 	  zugehörigen Engines verschieben wollen, aber im Moment sind sie dort gut aufgehoben <hezekiah>	Mal sehen, wie schnell das alles auf einem AMD K6-2 333 MHz ist (was 	  ein Chip ist, der nicht gerade für seine Integer-Arithmetik bekannt ist.) <jrand0m>	heh <jrand0m>	ok, also bleiben noch DSA und AES übrig, richtig? <jrand0m>	das ist alles ziemlich abgefahren, thecrypto.  gute arbeit. <thecrypto>	jup <jrand0m>	kann ich dich nach einer ETA für die anderen beiden nerven?  ;) <hezekiah>	Wenn das auf meiner Kiste annähernd so schnell ist wie auf deiner, 	  musst du mir zeigen, wie du das machst. ;-) <thecrypto>	DSA sollte fast fertig sein, sobald ich Primzahlen bereit habe <nop>	hezekiah, hast du sslcrypto für Python ausprobiert <thecrypto>	ein bisschen Code vom Primzahlgenerator und ähnlichen Sachen herüberkopieren 	  und dann ist es erledigt <nop>	das von dem Link <hezekiah>	nop: sslcrypto bringt uns nichts. <hezekiah>	nop: Es implementiert weder ElGamal _noch_ AES _noch_ sha256. <thecrypto>	AES ist größtenteils fertig, nur gibt es irgendwo noch einen Fehler, den 	  ich gerade zu finden und zu beseitigen versuche; sobald ich den habe, ist es fertig <jrand0m>	thecrypto> also bis Freitag DSA keygen, sign, verify und AES encrypt, 	  decrypt für Eingaben beliebiger Größe? <nop>	das auf McNabs Seite nicht? <thecrypto>	ja <nop>	mist <thecrypto>	sollte Freitag werden <thecrypto>	höchstwahrscheinlich Donnerstag <jrand0m>	thecrypto> schließt das den UnsignedBigInteger-Kram mit ein? <thecrypto>	ich werde das Meeting nächste Woche wegen Sommercamp verpassen, und 	  danach bin ich wieder da <thecrypto>	jrand0m: wahrscheinlich nicht <jrand0m>	ok. <jrand0m>	also ist vorerst die Interoperabilität zwischen Java und Python 	  b0rked. <jrand0m>	für Krypto, wohlgemerkt. ---	Notify: jeremiah ist online (anon.iip). -->	jeremiah (~chatzilla@anon.iip) ist #iip-dev beigetreten <jrand0m>	(also für Signaturen, Schlüssel, Verschlüsselung und Entschlüsselung)

<nop>	hmm vielleicht sollten wir uns mehr auf C/C++ konzentrieren
<thecrypto>	nun, sobald wir es vollständig zum Laufen gebracht haben, können wir sicherstellen, dass sowohl Java als auch Python miteinander sprechen können
<jrand0m>	während du weg bist, schaue ich mir die unsigned-Sachen an.
<jeremiah>	kann mir jemand einen Backlog mailen? jeremiah@kingprimate.com
<hezekiah>	jeremiah: Gib mir eine Minute. :)
<jrand0m>	nop> haben wir Entwickler für C/C++?
<nop>	Ich habe einen, ja
<nop>	und Hezekiah, das wissen wir, könnte es tun
<jrand0m>	oder vielleicht können wir ein Status-Update zum Python-Dev von hezekiah + jeremiah bekommen, um zu sehen, wann wir mehr Leute für die C/C++-Entwicklung haben
<jrand0m>	stimmt, natürlich. aber hez+jeremiah arbeiten im Moment an Python (oder?)
<hezekiah>	Ja.
<--	mrflibble hat den Kanal verlassen (Ping-Timeout)
<hezekiah>	Ich mache dem armen jeremiah irgendwie jede Menge Schwierigkeiten.
<nop>	Ich meinte nur, falls Python nicht schnell genug ist
<hezekiah>	Python ist hauptsächlich dafür da, dass ich dieses Netzwerk verstehe.
<nop>	ahh
<hezekiah>	Sobald ich es im Wesentlichen so weit habe, dass es der kompletten Spezifikation folgt, beabsichtige ich, es an jeremiah zu übergeben, damit er damit macht, was er für richtig hält.
<hezekiah>	Es soll keine Killer-Implementierung der Spezifikation sein.
<hezekiah>	(Wenn ich das wollte, würde ich C++ verwenden.)
<jeremiah>	nun, es gibt eigentlich keine wirklich prozessorintensiven Teile der App, soweit ich mich erinnere, abgesehen von Krypto, und idealerweise wird das sowieso in C erledigt, oder?
<jrand0m>	sicher, jeremiah. hängt alles von der App ab
-->	mrflibble (mrflibble@anon.iip) ist #iip-dev beigetreten
<hezekiah>	jeremiah: Theoretisch.
<jrand0m>	also, wo stehen wir auf der Python-Seite? Client-API, nur lokaler router, usw.?
<jeremiah>	die Python-Implementierung wird uns auch zeigen, welche Optimierungen wir von Anfang an vornehmen könnten... Ich würde sie gern aktuell halten oder, wenn möglich, der C-Implementierung voraus sein, so weit ich kann
<hezekiah>	jrand0m: OK. Hier ist, was ich habe.
<hezekiah>	In _theory_ sollte der router alle Nicht-Admin-Nachrichten von einem Client verarbeiten können.
<hezekiah>	Allerdings habe ich noch keinen Client, daher konnte ich es noch nicht debuggen (d. h. es gibt noch Bugs.)
<hezekiah>	Ich arbeite gerade am Client.
<jrand0m>	'k. wenn du die Signaturprüfung deaktivieren kannst, sollten wir jetzt den Java-Client dagegen laufen lassen können
<hezekiah>	Ich hoffe, das in ein bis zwei Tagen fertig zu haben, abgesehen von Admin-Nachrichten.
<jrand0m>	das können wir nach dem Meeting testen
<hezekiah>	jrand0m: OK.
<jeremiah>	Seit dem letzten Meeting habe ich mich größtenteils mit Kram aus der realen Welt beschäftigt; ich kann an der Client-API arbeiten, habe nur versucht, mein Denken mit dem von hezekiah zu synchronisieren
<jrand0m>	cool
<hezekiah>	jeremiah: Weißt du was, warte einfach.
<hezekiah>	jeremiah: Ich werfe dir wahrscheinlich gerade zu viel Neues hin, um es sofort zu bewältigen.
<jeremiah>	hezekiah: genau, ich wollte sagen, dass du wahrscheinlich einfach loslegen und die Basis-Sachen implementieren solltest
<hezekiah>	jeremiah: In absehbarer Zeit wird es stabilisiert sein und du kannst anfangen, es zu verfeinern. (Es gibt viele TODO-Kommentare, die Hilfe brauchen.)
<jeremiah>	und dann kann ich es später erweitern, sobald ich den Überblick habe
<hezekiah>	Ganz genau.
<hezekiah>	Du darfst den ganzen Code warten. :)
<jrand0m>	cool. also ETA 1–2 Wochen für einen funktionierenden Python router + Client-API?
<hezekiah>	Ich fahre nächste Woche in den Urlaub, also wahrscheinlich.
<hezekiah>	Wird es bald mehr Details zu router-zu-router geben?
<jrand0m>	nein.
<jrand0m>	nun, ja.
<jrand0m>	aber nein.
<hezekiah>	lol
<jeremiah>	hezekiah: wie lange ist der Urlaub?
<hezekiah>	1 Woche.
<jeremiah>	ok
<jrand0m>	(aka sobald das SDK rausgeht, fließen 100% meiner Zeit in I2NP (I2P‑Netzwerkprotokoll))
<hezekiah>	Ich hoffe, die gesamte Nicht-Admin-Funktionalität geschrieben zu haben, bevor ich in den Urlaub fahre
<hezekiah>	.
<jrand0m>	aber kurz nachdem du zurück bist, gehst du aufs College, richtig?
<hezekiah>	I2NP?
<hezekiah>	Richtig.
<jrand0m>	Netzwerkprotokoll
<hezekiah>	Ich habe nach dem Urlaub etwa 1 Woche.
<hezekiah>	Dann bin ich weg.
<hezekiah>	Und meine Freizeit fällt wie ein Stein.
<jrand0m>	diese 1 Woche sollte also nur Debugging sein
<jeremiah>	Ich kann aber am Code arbeiten, während hez weg ist
<jrand0m>	genau
<jrand0m>	wie sieht dein Sommer aus, jeremiah?
<hezekiah>	jeremiah: Vielleicht kannst du diese Admin-Funktionen zum Laufen bringen?

<thecrypto>	Ich werde immer noch einen Monat Zeit haben, nachdem ich aus meinem Urlaub zurück bin, um 	  an den Sachen zu arbeiten
<jrand0m>	ein Leben haben, oder so sein wie der Rest von uns l00sers?  :)
<jeremiah>	vielleicht
<hezekiah>	100sers?
<hezekiah>	Was ist ein 100ser?
<jeremiah>	ich gehe am 22. aufs College, ansonsten kann ich entwickeln
<mihi>	hezekiah: ein Loser
<jeremiah>	und in der letzten Woche bevor ich gehe, werden all meine Freunde weg sein... so 	  kann ich in den Hyperdev-Modus gehen
<hezekiah>	mihi: Ah!
<jrand0m>	hehe
<hezekiah>	OK. Also, wo waren wir auf der Tagesordnung?
<hezekiah>	d. h. Was kommt als Nächstes?
<jrand0m>	SDK-Status
<jrand0m>	SDK == eine Client-Impl., eine nur lokale router-Impl., eine App, und Dokumentation.
<jrand0m>	Ich würde das gern bis nächsten Dienstag rausbringen.
<hezekiah>	jeremiah: Der Backlog ist unterwegs. Sorry, dass ich dich da vergessen habe. :)
<jeremiah>	danke
<jrand0m>	ok, co ist nicht da, also ist das Naming-Service-Zeug wahrscheinlich ein bisschen 	  fehl am Platz
<jrand0m>	wir können den Naming Service besprechen, nachdem er Spezifikationen veröffentlicht oder 	  er da ist
<jrand0m>	ok, das war’s zu I2P-Kram
<jrand0m>	hat sonst noch jemand I2P-Kram, oder gehen wir weiter zu:
<nop> 4) The End mit 	  Kommentaren und so
<hezekiah>	Mir fällt nichts ein.
<jrand0m>	Ich nehme an, jeder hat 	  http://www.cnn.com/2003/TECH/internet/08/05/anarchist.prison.ap/index.html gesehen?
<thecrypto>	hier nicht
<jrand0m>	(nop hat es hier vorhin gepostet)
<hezekiah>	Das Ding mit dem Typen, der verhaftet wurde, weil er auf eine Bombenbau-Seite 	  verlinkt hat?
<jrand0m>	ja
<jrand0m>	Die Relevanz dafür, I2P so bald wie möglich bereitzustellen, sollte offensichtlich sein ;)
<hezekiah>	OK! jeremiah, diese Logs sind jetzt verschickt.
<jeremiah>	danke
<jrand0m>	hat jemand Fragen / Kommentare / Gedanken / Frisbees, 	  oder haben wir ein rekordverdächtig kurzes Meeting?
*	thecrypto wirft eine Frisbee
<--	logger hat die Verbindung getrennt (Ping-Timeout)
<jrand0m>	verdammt, ihr seid heute alle so ruhig ;)
<mihi>	frage:
<mihi>	wo können Nicht-Devs euren Java-Code bekommen?
<jrand0m>	si sr?
<thecrypto>	noch nicht
<mihi>	404
<jrand0m>	das wird verfügbar gemacht, sobald wir release-ready sind.  aka der Source wird zusammen mit dem SDK rausgehen
<jrand0m>	heh
<jrand0m>	ja, wir benutzen SF nicht
<hezekiah>	nop: Ist es möglich, dass wir irgendwann anonymes CVS zum Laufen bekommen?
<hezekiah>	Zeit?
<--	mrflibble hat die Verbindung getrennt (Ping-Timeout)
<nop>	nun, ich würde einen Nicht-Standard-Port öffnen
<jrand0m>	hezekiah> das haben wir, sobald der Code die GPL-Lizenz enthält
<nop>	aber ich arbeite an viewcvs
<jrand0m>	aka nicht jetzt, da das GPL-Dokument dem Code noch nicht hinzugefügt wurde
<hezekiah>	jrand0m: Es ist in allen Python-Code-Verzeichnissen, und alle Python 	  Source-Dateien geben die Lizenz als GPL-2 an.
<jrand0m>	hezekiah> ist das auf der cathedral?
<hezekiah>	Ja.
<jrand0m>	ah, word.  i2p/core/code/python ?  oder ein anderes Modul?
*	jrand0m hat es dort noch nicht gesehen
<hezekiah>	Jedes Python-Code-Verzeichnis hat eine COPYING-Datei mit der 	  GPL-2, und jede Source-Datei hat die Lizenz auf GPL-2 gesetzt
<hezekiah>	Das ist i2p/router/python und i2p/api/python
<jrand0m>	'k
<jrand0m>	also, ja, bis nächsten Dienstag haben wir das SDK + öffentlichen Source-Zugang.
<hezekiah>	Cool.
<hezekiah>	Oder, wie du gern sagst, wikked. ;-)
<jrand0m>	heh
<jrand0m>	nada mas?
<hezekiah>	nada mas? Was heißt das!?
<jeremiah>	nichts weiter
*	jrand0m schlägt vor, du lernst an der Uni ein bisschen Spanisch
-->	mrflibble (mrflibble@anon.iip) ist #iip-dev beigetreten
<hezekiah>	Fragen, irgendwer?
<hezekiah>	Zum Ersten!
<--	ptm (~ptm@anon.iip) hat #iip-dev verlassen (ptm)
<hezekiah>	Zum Zweiten!
<--	mrflibble hat die Verbindung getrennt (Mr. Flibble sagt "Game over, Jungs")
<hezekiah>	Jetzt sprechen .. oder wartet, bis ihr später Lust habt zu sprechen!
<thecrypto>	okay, ich werde ElGamal noch weiter optimieren, also erwartet 	  in Zukunft noch schnellere ElGamal-Benchmarks
<jrand0m>	bitte fokussier dich auf DSA und AES, bevor du tunst... biiiiitteee :)
<thecrypto>	mach ich
<hezekiah>	Der Grund, warum er das macht, ist, dass ich den Leuten mal wieder Ärger mache. ;-)
<thecrypto>	ich mache DSA-Primzahlen
-->	mrflibble (mrflibble@anon.iip) ist #iip-dev beigetreten
<thecrypto>	nun, zumindest schreibe ich gerade das Programm, um DSA-Primzahlen zu erzeugen
<hezekiah>	ElGamal in Java mag einen AMD K-6 II 333 MHz nicht.
<hezekiah>	OK.
<hezekiah>	Fragerunde ist vorbei!
<jrand0m>	ok hez, wir sind durch.  willst du ein kleines Powwow machen, um den Java-Client 	  und die Arbeit am Python router hinzubekommen?
<hezekiah>	Bis nächste Woche, Bürger!
*	hezekiah haut den *baf*er runter
</div>
