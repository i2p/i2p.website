---
title: "I2P-Statusnotizen vom 2005-09-13"
date: 2005-09-13
author: "jr"
description: "Wöchentliches Update zu SSU-Introductions für NAT-Hole-Punching (NAT-Traversal-Technik), zum Fortschritt der Unit-Test-Bounty, zur Diskussion über die Roadmap der Client-Apps und zur Entfernung des veralteten Modus für garantierte Zustellung"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für die wöchentlichen Statusnotizen

* Index

1) Netzstatus 2) SSU introductions / NAT hole punching 3) Prämien 4) Anweisungen für die Client-App 5) ???

* 1) Net status

We're still churning along with the 0.6.0.5 release on the net, and nearly everyone has upgraded, with many running one of the builds since then (CVS HEAD is 0.6.0.5-9 right now). Things are still working well on the whole, though there has been a substantial increase in network traffic from what I've observed, likely due to more i2p-bt or i2phex usage. Once of the irc servers had a bit of a bump last night, but the other held on fine and things seem to have recovered well. There have been substantial improvements in error handling and other features in the CVS builds however, so I expect we'll have a new release later this week.

* 2) SSU introductions / NAT hole punching

Die neuesten Builds in CVS enthalten Unterstützung für die lange diskutierten SSU introductions [1], wodurch wir dezentrales NAT-Hole-Punching für Nutzer durchführen können, die sich hinter einem NAT oder einer Firewall befinden, die sie nicht kontrollieren. Zwar wird symmetrisches NAT nicht unterstützt, aber der Großteil der Fälle wird abgedeckt. Rückmeldungen aus der Praxis sind gut, allerdings können nur Nutzer mit den neuesten Builds die hinter NAT befindlichen Nutzer kontaktieren – ältere Builds müssen warten, bis die Nutzer sie zuerst kontaktieren. Aus diesem Grund werden wir den Code früher als üblich in ein Release bringen, um die Zeit zu verkürzen, in der diese eingeschränkten Routen bestehen.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD#introduction

* 3) Bounties

Ich habe mir vorhin die i2p-cvs-Mailingliste angesehen und eine ganze Reihe von Commits von Comwiz bemerkt, die sich offenbar auf Phase 3 der Prämie für Unit-Tests [2] beziehen. Vielleicht kann uns Comwiz dazu beim Treffen heute Abend ein Status-Update geben.

[2] http://www.i2p.net/bounty_unittests

Am Rande: Auf Vorschlag einer anonymen Person habe ich die Hall of Fame [3] ein wenig aktualisiert, einschließlich der Zeitpunkte der Spenden, der Zusammenfassung mehrerer Spenden derselben Person sowie der Umrechnung der Beträge in eine einheitliche Währung. Nochmals vielen Dank an alle, die beigetragen haben, und falls falsche Informationen veröffentlicht wurden oder etwas fehlt, melden Sie sich bitte, dann wird es entsprechend aktualisiert.

[3] http://www.i2p.net/halloffame

* 4) Client app directions

Eine der neueren Anpassungen in den aktuellen CVS-Builds ist die Entfernung des alten Zustellungsmodus mode=guaranteed. Mir war nicht bewusst, dass ihn noch jemand verwendet (und das ist ohnehin völlig unnötig, da wir seit einem Jahr die vollständige Streaming-Bibliothek haben), aber als ich mir i2phex genauer ansah, fiel mir auf, dass dieses Flag gesetzt war. Mit dem aktuellen Build (und allen nachfolgenden Releases) wird i2phex einfach mode=best_effort verwenden, was hoffentlich seine Leistung verbessert.

Mein Anliegen dabei, das anzusprechen (abgesehen vom Hinweis für i2phex-Nutzer), ist zu fragen, was ihr auf der Client-Seite von I2P benötigt und ob ich einen Teil meiner Zeit darauf verwenden sollte, dabei zu helfen, einiges davon umzusetzen. Aus dem Stegreif sehe ich in verschiedenen Bereichen eine Menge zu tun:  = Syndie: vereinfachtes Posten, automatisierte Synchronisation, Datenimport, App-Integration (mit i2p-bt, susimail, i2phex usw.),    Unterstützung für Threading, um forumähnliches Verhalten zu ermöglichen, und mehr.  = eepproxy: verbesserter Durchsatz, Unterstützung für Pipelining  = i2phex: allgemeine Wartung (ich habe es nicht genug genutzt, um seine    Schwachstellen zu kennen)  = irc: verbesserte Resilienz, wiederkehrende irc-Server-Ausfälle erkennen und    ausgefallene Server meiden, CTCP-Aktionen lokal statt auf dem    Server filtern, DCC-Proxy  = Verbesserte x64-Unterstützung mit jbigi, jcpuid und dem Service-Wrapper  = Systray-Integration und das DOS-Fenster entfernen  = Verbesserte Bandbreitensteuerung für kurzzeitige Lastspitzen  = Verbesserte Überlaststeuerung für Netzwerk- und CPU-Überlastung sowie    Wiederherstellung.  = Mehr Funktionalität verfügbar machen und die verfügbaren Funktionen der    Router-Konsole für Drittanbieter-Apps dokumentieren  = Dokumentation für Client-Entwickler  = I2P-Einführungsdokumentation

Und über all das hinaus gibt es noch den Rest der Punkte auf der Roadmap [4] und der To-do-Liste [5]. Ich weiß, was wir technisch brauchen, aber ich weiß nicht, was *du* aus Anwendersicht brauchst. Sprich mit mir, was willst du?

[4] http://www.i2p.net/roadmap [5] http://www.i2p.net/todo

* 5) ???

Es gibt noch ein paar andere Dinge, die im router-Kern und im Bereich der App-Entwicklung passieren, über das oben Erwähnte hinaus, aber im Moment ist noch nicht alles bereit zur Nutzung. Wenn jemand etwas ansprechen möchte, kommt heute Abend um 20:00 UTC beim Meeting in #i2p vorbei!

=jr
