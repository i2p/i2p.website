---
title: "I2P-Statusnotizen für 2005-07-12"
date: 2005-07-12
author: "jr"
description: "Wöchentliches Update zu Dienstwiederherstellung, Fortschritt der SSU-Tests und Analyse der I2CP-Kryptografie-Schicht zur potenziellen Vereinfachung"
categories: ["status"]
---

Hi zusammen, es ist wieder so weit

* Index

1) squid/www/cvs/dev.i2p wiederhergestellt 2) SSU-Tests 3) I2CP-Kryptografie 4) ???

* 1) squid/www/cvs/dev.i2p restored

Nachdem ich mir an mehreren Colocation-Servern die Zähne ausgebissen habe, wurden einige der alten Dienste wiederhergestellt - squid.i2p (einer der beiden Standard-Outproxies (Ausgangs-Proxys ins Clearnet)), www.i2p (ein sicherer Verweis auf www.i2p.net), dev.i2p (ein sicherer Verweis auf dev.i2p.net, wo sich die Mailinglisten-Archive, cvsweb und die Standard-netDb-Seeds befinden) und cvs.i2p (ein sicherer Verweis auf unseren CVS-Server - cvs.i2p.net:2401). Mein Blog ist immer noch abgetaucht, aber seine Inhalte sind ohnehin verloren gegangen, also wird es früher oder später einen Neuanfang geben müssen. Da diese Dienste jetzt wieder zuverlässig online sind, ist es an der Zeit, weiterzugehen zu den...

* 2) SSU testing

Wie in dem kleinen gelben Kasten auf jeder Routerkonsole erwähnt, haben wir mit der nächsten Runde von Live-Netzwerktests für SSU begonnen. Die Tests sind nicht für alle geeignet, aber wenn Sie experimentierfreudig sind und Ihnen etwas manuelle Konfiguration nichts ausmacht, sehen Sie sich die auf Ihrer Routerkonsole verlinkten Details an (http://localhost:7657/index.jsp). Es kann mehrere Testrunden geben, aber ich erwarte keine größeren Änderungen an SSU vor dem 0.6-Release (0.6.1 wird Unterstützung für diejenigen hinzufügen, die ihre Ports nicht weiterleiten können oder anderweitig keine eingehenden UDP-Verbindungen empfangen können).

* 3) I2CP crypto

Während ich die neuen Einführungsdokumente erneut durchgehe, habe ich etwas Schwierigkeiten, die zusätzliche Verschlüsselungsschicht innerhalb des I2CP SDK zu rechtfertigen. Die ursprüngliche Zielsetzung der I2CP-Krypto-Schicht war es, einen grundlegenden Ende-zu-Ende-Schutz für die übertragenen Nachrichten bereitzustellen und I2CP-Clients (aka I2PTunnel, the SAM bridge, I2Phex, azneti2p, etc) die Kommunikation über nicht vertrauenswürdige router zu ermöglichen. Im Verlauf der Implementierung ist der Ende-zu-Ende-Schutz der I2CP-Schicht jedoch redundant geworden, da alle Client-Nachrichten vom router Ende-zu-Ende innerhalb von garlic messages (Garlic-Nachrichten) verschlüsselt werden, wobei das leaseSet des Absenders und manchmal eine Zustellstatusmeldung gebündelt werden. Diese garlic layer bietet bereits eine Ende-zu-Ende-Verschlüsselung vom router des Absenders zum router des Empfängers - der einzige Unterschied besteht darin, dass sie nicht davor schützt, dass dieser router selbst bösartig ist.

Wenn ich mir jedoch die absehbaren Anwendungsfälle ansehe, kann ich mir kein plausibles Szenario vorstellen, in dem dem lokalen router nicht vertraut würde. Zumindest verbirgt die I2CP-Kryptografie nur den Inhalt der vom router gesendeten Nachricht - der router muss dennoch wissen, an welches Ziel sie gesendet werden soll. Falls erforderlich, können wir einen SSH/SSL I2CP-Listener hinzufügen, um es dem I2CP-Client und dem router zu ermöglichen, auf getrennten Rechnern zu arbeiten, oder Personen, die so etwas benötigen, können bestehende Tunneling-Tools verwenden.

Zur Wiederholung der derzeit verwendeten Kryptoschichten haben wir:  * Die Ende-zu-Ende-ElGamal/AES+SessionTag-Schicht von I2CP, die den Datenverkehr von
    der destination des Senders zur destination des Empfängers verschlüsselt.  * Die Ende-zu-Ende garlic encryption-Schicht des router
    (ElGamal/AES+SessionTag), die den Datenverkehr vom router des Senders zum
    router des Empfängers verschlüsselt.  * Die Verschlüsselungsschicht der tunnel für sowohl die inbound als auch die outbound
    tunnels an den Hops entlang jedes einzelnen (aber nicht zwischen dem outbound
    endpoint und dem inbound gateway).  * Die Transport-Verschlüsselungsschicht zwischen jedem router.

Ich möchte beim Entfernen einer dieser Schichten ziemlich vorsichtig sein, aber ich möchte unsere Ressourcen nicht mit unnötiger Arbeit verschwenden. Mein Vorschlag ist, die erste I2CP-Verschlüsselungsschicht wegzulassen (wobei natürlich weiterhin die Authentifizierung beibehalten wird, die während des I2CP-Sitzungsaufbaus, der leaseSet-Autorisierung und der Absenderauthentifizierung verwendet wird). Kann jemand einen Grund nennen, warum wir sie beibehalten sollten?

* 4) ???

Das war's fürs Erste, aber wie immer ist viel los. Auch diese Woche gibt es kein Treffen, aber wenn jemand etwas ansprechen möchte, zögert bitte nicht, es auf der Mailingliste oder im Forum zu posten. Außerdem, auch wenn ich den Scrollback (Chat-Verlauf) in #i2p lese, sollten allgemeine Fragen oder Anliegen stattdessen an die Liste geschickt werden, damit mehr Leute an der Diskussion teilnehmen können.

=jr
