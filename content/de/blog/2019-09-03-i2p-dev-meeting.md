---
title: "I2P Dev Meeting - September 03, 2019"
date: 2019-09-03
author: "zzz"
description: "Protokoll des I2P-Entwicklertreffens vom 3. September 2019."
categories: ["meeting"]
---

## Kurze Zusammenfassung

<p class="attendees-inline"><strong>Anwesend:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Sitzungsprotokoll

<div class="irc-log">                Hinweis: Die Zeilen von sadie sind im Meeting nicht durchgekommen, unten eingefügt.

20:00:00 <zzz> 0) Hi
20:00:00 <zzz> 1) 0.9.42 Release-Status (zzz)
20:00:00 <zzz> 2) I2P Browser "labs" Projektstatus (sadie, meeh)
20:00:00 <zzz> 3) Outproxy Anwendungsfälle / Status (sadie)
20:00:00 <zzz> 4) 0.9.43 Entwicklungsstatus (zzz)
20:00:00 <zzz> 5) Status der Vorschläge (zzz)
20:00:00 <zzz> 6) Status-Scrum (zlatinb)
20:00:04 <zzz> 0) Hi
20:00:06 <zzz> hi
20:00:17 <zlatinb> hi
20:00:30 <zzz> 1) 0.9.42 Release-Status (zzz)
20:00:48 <zzz> Das Release lief letzte Woche ziemlich reibungslos
20:00:56 <zzz> Es sind nur noch wenige Dinge offen
20:01:27 <zzz> die GitHub-Bridge wieder zum Laufen bringen (nextloop), das Debian-sid-Paket (mhatta) und die Android-Client-Bibliothek, die wir für 41 vergessen haben (meeh)
20:01:37 <zzz> nextloop, meeh, habt ihr ETAs für diese Punkte?
20:03:06 <zzz> Sonst noch etwas zu 1) ?
20:04:02 <zzz> 2) I2P Browser "labs" Projektstatus (sadie, meeh)
20:04:25 <zzz> sadie, meeh, wie ist der Status, und was ist der nächste Meilenstein?          <sadie> Beta 5 sollte am Freitag erscheinen, aber es gab einige Probleme. Es sieht so aus, als wären einige bereit https://i2bbparts.meeh.no/i2p-browser/ aber ich musste wirklich von meeh den nächsten Termin dafür hören          <sadie> Die Lab-Seite wird bis Ende dieser Woche live sein. Der nächste Browser-Meilenstein wird die Besprechung der Konsolenanforderungen für das Beta 6-Release sein
20:05:51 <zzz> Sonst noch etwas zu 2) ?
20:06:43 <zzz> 3) Outproxy Anwendungsfälle / Status (sadie)
20:06:57 <zzz> sadie, wie ist der Status, und was ist der nächste Meilenstein?          <sadie> Jeder kann unseren Sitzungsnotizen in Ticket 2472 folgen. Wir haben über den Status der Anwendungsfälle entschieden und eine Liste von Anforderungen erstellt. Der nächste Meilenstein werden Nutzeranforderungen für einen Friends-and-Family-Anwendungsfall sowie Entwicklungsanforderungen für Friends and Family und den allgemeinen Anwendungsfall sein, um zu sehen, wo sie sich überschneiden
20:08:05 <zzz> Sonst noch etwas zu 3) ?
20:08:19 <eyedeekay> Sorry, ich bin zu spät
20:09:01 <zzz> 4) 0.9.43 Entwicklungsstatus (zzz)
20:09:21 <zzz> Wir starten gerade in den 43er Zyklus, den wir in etwa 7 Wochen veröffentlichen wollen
20:09:40 <zzz> Wir haben die Roadmap auf der Website aktualisiert, werden aber noch weitere Punkte hinzufügen
20:10:06 <zzz> Ich habe einige IPv6-Bugs behoben und die tunnel-AES-Verarbeitung beschleunigt
20:10:30 <zzz> Bald werde ich mich der neuen Blinding-Info I2CP-Nachricht zuwenden
20:10:59 <zzz> eyedeekay, zlatinb, habt ihr noch etwas zu .43 hinzuzufügen?
20:11:46 <eyedeekay> Nein, ich glaube nicht
20:12:02 <zlatinb> wahrscheinlich mehr Testnetz-Themen
20:12:32 <zzz> Ja, wir haben noch ein paar weitere jogger-Tickets, die wir uns ansehen müssen, bezüglich SSU
20:12:48 <zzz> Sonst noch etwas zu 4) ?
20:14:00 <zzz> 5) Status der Vorschläge (zzz)
20:14:20 <zzz> Unser Hauptfokus liegt auf dem sehr komplexen neuen Verschlüsselungs‑Vorschlag 144
20:14:48 <zzz> Wir haben in den letzten Wochen gute Fortschritte gemacht und den Vorschlag selbst wesentlich aktualisiert
20:15:35 <zzz> Es gibt noch ein paar Aufräumarbeiten und Lücken zu füllen, aber ich bin zuversichtlich, dass er in einem ausreichend guten Zustand ist, sodass wir bald mit der Implementierung einiger Unittests beginnen könnten, vielleicht bis Ende des Monats
20:16:17 <zzz> Außerdem bekommt die Blinding-Info-Nachricht für Vorschlag 123 (encrypted LS2) noch einmal Aufmerksamkeit, nachdem ich in der nächsten Woche mit der Implementierung beginne
20:16:52 <zzz> Außerdem erwarten wir bald ein Update zu Vorschlag 152 (tunnel build messages) von chisana
20:17:27 <zzz> Wir haben Vorschlag 147 (cross-network prevention) letzten Monat abgeschlossen, und sowohl i2p als auch i2pd haben das implementiert und im .42-Release
20:18:23 <zzz> Die Dinge kommen also voran; auch wenn 144 langsam und einschüchternd wirkt, macht es dennoch gute Fortschritte
20:18:27 <zzz> Sonst noch etwas zu 5) ?
20:20:00 <zzz> 6) Status-Scrum (zlatinb)
20:20:05 <zzz> Leg los, zlatinb
20:20:42 <zlatinb> Hi, bitte sagt in wenigen Worten: 1) Woran ihr seit dem letzten Scrum gearbeitet habt 2) Was ihr nächsten Monat vorhabt 3) Habt ihr Blocker oder braucht Hilfe. Sagt EOT, wenn fertig
20:21:23 <zlatinb> ich: 1) Verschiedene Experimente im Testnetz, um Massenübertragungen zu beschleunigen 2) mehr Testnetz-Arbeit auf einem hoffentlich größeren Server/Netz 3) keine Blocker EOT
20:22:15 <zzz> 1) Bugfixes, die Konfigurations-Split-Änderung, .42-Release, Vorschläge, DEFCON-Workshops (siehe meinen Reisebericht im i2pforum und auf unserer Website)
20:23:56 <zzz> 2) Bugfixes, Vorschlag 144, Blinding-Info-Nachricht, Beschleunigungen, Unterstützung bei der Outproxy-Forschung, den durch den Konfig.-Split kaputtgegangenen SSL-Assistenten reparieren
20:24:20 <zzz> mehr IPv6-Fixes
20:24:38 <zzz> 3) keine Blocker EOT
20:24:50 <eyedeekay> 1) Seit dem letzten Scrum habe ich an Bugfixes, der Website, am Outproxy-Vorschlag und an Dingen rund um i2ptunnels gearbeitet. 2) Fortsetzen der Umstrukturierung und Verbesserung der Darstellung der Website. Arbeit am Voranbringen des Outproxy-Vorschlags 3) keine Blocker EOT          <sadie> 1) FOCI besucht, Finanzierungsoptionen recherchiert, mich mit potenziellen Geldgebern getroffen, ein Treffen mit Tails (inklusive Mhatta) gehabt, an I2P Browser-Branding gearbeitet, Website-Updates mit IDK, kleine Änderungen an der Konsole für das letzte Release vorgenommen          <sadie> 2) Im nächsten Monat arbeite ich an Förderanträgen, Verbesserungen an Konsole und Website, Einrichtungsassistent, Teilnahme an Our Networks in Toronto, I2P Browser- und Outproxy-Forschung voranbringen          <sadie> 3) keine Blocker EOT
20:25:29 <zlatinb> scrum.setTimeout( 60 * 1000 );
20:27:04 <zzz> ok, Timeout
20:27:10 <zlatinb> ScrumTimeoutException
20:27:41 <zzz> Letzter Aufruf an sadie meeh nextloop, um auf 1)-3) zurückzukommen
20:27:52 <zzz> Weitere Themen für das Meeting?
20:28:47 * zzz greift nach dem baffer
20:30:00 * zzz ***bafs*** das Meeting ist geschlossen </div>
