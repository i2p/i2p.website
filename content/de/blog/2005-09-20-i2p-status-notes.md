---
title: "I2P Statusnotizen vom 2005-09-20"
date: 2005-09-20
author: "jr"
description: "Wöchentliches Update zum Erfolg des 0.6.0.6-Releases mit SSU introductions, zum Sicherheitsupdate für I2Phex 0.1.1.27 und zum Abschluss der Colo-Migration"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) Migration 4) ???

* 1) 0.6.0.6

Mit dem Release 0.6.0.6 vom letzten Samstag haben wir im Live-Netz eine ganze Reihe neuer Komponenten im Einsatz, und ihr habt beim Upgrade großartige Arbeit geleistet – Stand vor ein paar Stunden haben fast 250 routers ein Upgrade durchgeführt! Auch das Netzwerk scheint gut zu laufen, und Introductions (Einführungsvorgänge) haben bisher funktioniert – ihr könnt eure eigene Introduction-Aktivität auf http://localhost:7657/oldstats.jsp nachverfolgen, indem ihr euch die udp.receiveHolePunch und udp.receiveIntroRelayResponse anschaut (sowie udp.receiveRelayIntro, für diejenigen hinter NATs).

Übrigens, der "Status: ERR-Reject" ist mittlerweile wirklich kein Fehler mehr, daher sollten wir ihn vielleicht in "Status: OK (NAT)" ändern?

Es gab einige Fehlerberichte zu Syndie. Zuletzt ist ein Bug aufgetreten, bei dem es nicht gelingt, sich mit entfernten Peers zu synchronisieren, wenn man es anweist, auf einmal zu viele Einträge herunterzuladen (weil ich unklugerweise HTTP GET statt POST verwendet habe). Ich werde Unterstützung für POST in EepGet hinzufügen, aber in der Zwischenzeit versuchen Sie, jeweils nur 20 oder 30 Beiträge abzurufen. Nebenbei bemerkt: Vielleicht kann jemand das JavaScript für die Seite remote.jsp erstellen, das „alle Beiträge dieses Nutzers abrufen“ anbietet und dabei automatisch alle Kontrollkästchen seines Blogs auswählt?

Man hört, dass OSX inzwischen out of the box einwandfrei funktioniert, und mit 0.6.0.6-1 ist x86_64 auch unter Windows und Linux einsatzfähig. Mir sind keine Berichte über Probleme mit den neuen .exe-Installern bekannt, also heißt das entweder, dass es gut läuft oder komplett schiefgeht :)

* 2) I2Phex 0.1.1.27

Angeregt durch einige Berichte über Unterschiede zwischen dem Quellcode und dem, was in legions Paketierung der Version 0.1.1.26 enthalten war, sowie Bedenken hinsichtlich der Sicherheit des nativen Closed-Source-Launchers, habe ich eine neue, mit launch4j [1] gebaute i2phex.exe zu cvs hinzugefügt und den neuesten Stand aus cvs gebaut und im I2P-Dateiarchiv [2] bereitgestellt. Es ist unbekannt, ob legion vor seiner Veröffentlichung weitere Änderungen an seinem Quellcode vorgenommen hat oder ob der von ihm veröffentlichte Quellcode tatsächlich dem entspricht, was er gebaut hat.

Aus Sicherheitsgründen kann ich weder die Verwendung des Closed-Source-Launchers von legion noch die der Version 0.1.1.26 empfehlen. Das Release auf der I2P-Website [2] enthält den neuesten Code aus cvs, ohne Änderungen.

Sie können den Build reproduzieren, indem Sie zunächst den I2P-Code auschecken und bauen, dann den I2Phex-Code auschecken und anschließend "ant makeRelease" ausführen:   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (Passwort: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

Die i2phex.exe in diesem ZIP-Archiv ist unter Windows nutzbar, indem man sie einfach ausführt, oder unter *nix/osx über "java -jar i2phex.exe". Sie setzt voraus, dass I2Phex in einem Verzeichnis neben I2P installiert ist - (z. B. C:\Program Files\i2phex\ und C:\Program Files\i2p\), da sie auf einige der jar-Dateien von I2P verweist.

Ich werde nicht einspringen, um I2Phex zu warten, aber ich werde zukünftige I2Phex-Veröffentlichungen auf der Website bereitstellen, wenn es Updates in cvs gibt. Wenn jemand an einer Webseite arbeiten möchte, die wir veröffentlichen können, um I2Phex zu beschreiben und vorzustellen (sirup, bist du da draußen?), mit Links zu sirup.i2p, nützlichen Forenbeiträgen, Legions Liste aktiver Peers, das wäre großartig.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip und     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (mit meinem Schlüssel signiert)

* 3) migration

Wir haben die Colocation-Server für die I2P-Dienste gewechselt, aber auf dem neuen Server sollte jetzt alles vollständig funktionsfähig sein - falls euch etwas Komisches auffällt, gebt mir bitte Bescheid!

* 4) ???

In letzter Zeit gab es viele interessante Diskussionen auf der i2p-Mailingliste, Adams schicken neuen SMTP-Proxy/Filter sowie einige gute Beiträge auf syndie (schon gloins Skin auf http://gloinsblog.i2p gesehen?). Ich arbeite derzeit an einigen Änderungen für ein paar seit Langem bestehende Probleme, die sind aber noch nicht unmittelbar zu erwarten. Wenn jemand noch etwas ansprechen und diskutieren möchte, schaut beim Treffen in #i2p um 20 Uhr GMT vorbei (in etwa 10 Minuten oder so).

=jr
