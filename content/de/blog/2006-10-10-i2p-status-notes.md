---
title: "I2P-Statusnotizen für 2006-10-10"
date: 2006-10-10
author: "jr"
description: "Release 0.6.1.26 mit positivem Feedback, Syndie 0.910a nähert sich Version 1.0, und Evaluierung einer verteilten Versionsverwaltung für Syndie"
categories: ["status"]
---

Hi zusammen, kurze Statusnotizen diese Woche

* Index

1) 0.6.1.26 und Netzwerkstatus 2) Syndie Entwicklungsstatus 3) Verteilte Versionsverwaltung erneut betrachtet 4) ???

* 1) 0.6.1.26 and network status

Neulich haben wir die neue Version 0.6.1.26 herausgebracht, die viele i2psnark-Verbesserungen von zzz und einige neue NTP-Sicherheitsprüfungen von Complication enthält, und die Rückmeldungen waren positiv. Das Netzwerk scheint leicht zu wachsen, ohne neue ungewöhnliche Effekte, obwohl manche Leute immer noch Schwierigkeiten haben, ihre tunnels aufzubauen (wie es schon immer der Fall war).

* 2) Syndie development status

Immer mehr Verbesserungen sind in der Pipeline; die aktuelle Alphaversion steht bei 0.910a. Die Feature-Liste für 1.0 ist so gut wie erfüllt, daher geht es derzeit vor allem um Fehlerbehebungen und Dokumentation. Schau doch bei #i2p vorbei, wenn du beim Testen helfen möchtest :)

Außerdem gab es im Channel einige Diskussionen über Entwürfe für die Syndie GUI - meerboop hat ein paar coole Ideen entwickelt und arbeitet daran, sie zu dokumentieren. Die Syndie GUI ist die Hauptkomponente des Syndie 2.0 Release, also je eher wir das ins Rollen bringen, desto eher übernehmen wir die Wel^W^W^W^W können wir Syndie unter die ahnungslosen Massen bringen.

Es gibt außerdem einen neuen Vorschlag in meinem Syndie-Blog zur Nachverfolgung von Fehlern und Funktionswünschen mithilfe von Syndie selbst. Der leichteren Zugänglichkeit halber habe ich einen Nur-Text-Export dieses Beitrags ins Web gestellt - Seite 1 ist unter <http://dev.i2p.net/~jrandom/bugsp1.txt> und Seite 2 ist unter <http://dev.i2p.net/~jrandom/bugsp2.txt>

* 3) Distributed version control revisited

Einer der Punkte, die für Syndie noch zu klären sind, ist, welches öffentliche Versionskontrollsystem verwendet werden soll, und wie bereits erwähnt, sind verteilte und Offline-Funktionalität notwendig. Ich habe mir das halbe Dutzend oder so der verfügbaren Open-Source-Systeme (darcs, mercurial, git/cogito, monotone, arch, bzr, codeville) angesehen, ihre Dokumentation durchforstet, sie ausprobiert und mit ihren Entwicklern gesprochen. Im Moment scheinen monotone und bzr in Bezug auf Funktionalität und Sicherheit am besten zu sein (bei nicht vertrauenswürdigen Repositories brauchen wir starke Kryptographie, um sicherzustellen, dass wir nur authentische Änderungen abrufen), und die enge Integration von Kryptographie in monotone wirkt sehr überzeugend. Ich arbeite mich allerdings noch durch die mehreren hundert Seiten Dokumentation, aber nach dem, was ich mit den monotone-Entwicklern besprochen habe, scheinen sie alles genau richtig zu machen.

Natürlich werden, egal für welches DVCS (verteiltes Versionskontrollsystem) wir uns letztlich entscheiden, alle Veröffentlichungen im einfachen Tarball-Format bereitgestellt, und Patches werden zur Prüfung im einfachen diff -uw-Format angenommen. Trotzdem würde ich von allen, die eine Mitarbeit an der Entwicklung in Betracht ziehen, gerne Ihre Meinungen und Präferenzen hören.

* 4) ???

Wie Sie sehen, ist wie immer eine Menge los. Auch in dem Thread „solve world hunger“ im Forum gab es weitere Diskussionen, also schauen Sie es sich unter <http://forum.i2p.net/viewtopic.php?t=1910> an

Wenn du noch etwas zu besprechen hast, komm doch heute Abend zu unserem Entwicklertreffen bei #i2p vorbei oder poste ins Forum oder auf die Mailingliste!

=jr
