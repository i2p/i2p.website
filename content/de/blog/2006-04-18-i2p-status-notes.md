---
title: "I2P-Statusnotizen für 2006-04-18"
date: 2006-04-18
author: "jr"
description: "0.6.1.16 Netzwerkverbesserungen, Analyse des congestion collapse (Zusammenbruch durch Netzwerküberlastung) bei der tunnel-Erstellung und Updates zur Feedspace-Entwicklung"
categories: ["status"]
---

Hallo zusammen, es ist wieder Dienstag – Zeit für unsere wöchentlichen Statusnotizen.

* Index

1) Netzstatus und 0.6.1.16 2) Tunnel-Erstellung und Überlastung 3) Feedspace 4) ???

* 1) Net status and 0.6.1.16

Da inzwischen 70 % des Netzwerks auf 0.6.1.16 aktualisiert sind, zeichnet sich gegenüber früheren Releases eine Verbesserung ab, und da die in diesem Release behobenen Probleme nun aus dem Weg sind, haben wir einen klareren Blick auf unseren nächsten Engpass.  Für alle, die noch nicht auf 0.6.1.16 sind, bitte so bald wie möglich aktualisieren, da frühere Releases Anfragen zur Erstellung von tunnels willkürlich ablehnen (selbst wenn der router über ausreichende Ressourcen verfügt, um an mehr tunnels teilzunehmen).

* 2) Tunnel creation and congestion

Im Moment scheint es, als erlebten wir etwas, das man wohl am besten als congestion collapse (Kollaps durch Überlastung) beschreiben kann - Anfragen zur tunnel-Erstellung werden abgelehnt, weil router wenig Bandbreite haben, also werden in der Hoffnung, andere router mit freien Ressourcen zu finden, noch mehr Anfragen zur tunnel-Erstellung gesendet, was jedoch nur die genutzte Bandbreite erhöht. Dieses Problem gibt es seit der Umstellung auf die neue Kryptografie für die tunnel-Erstellung in 0.6.1.10 und es lässt sich im Wesentlichen darauf zurückführen, dass wir keine pro Hop Rückmeldungen über Beitritt/Ablehnung erhalten, bis (oder genauer gesagt, *es sei denn*) die Anfrage und die Antwort den Weg durch zwei tunnels zurückgelegt haben. Wenn einer dieser Peers die Nachricht nicht weiterleitet, wissen wir nicht, welcher Peer die Weiterleitung nicht durchgeführt hat, welche Peers zugestimmt haben und welche Peers die Anfrage ausdrücklich abgelehnt haben.

Wir begrenzen bereits die Anzahl der gleichzeitig in Bearbeitung befindlichen Anfragen zur tunnel-Erstellung (und Tests zeigen, dass eine Erhöhung des Timeouts nicht hilft), daher reicht Nagles traditionelle Lösung nicht aus. Ich probiere derzeit ein paar Anpassungen an unserem Anfragenverarbeitungs-Code aus, um die Häufigkeit des stillen Verwerfens von Anfragen (im Gegensatz zu expliziten Ablehnungen) zu verringern, sowie an unserem Anfragenerzeugungs-Code, um die Parallelität unter Last zu reduzieren. Außerdem probiere ich einige weitere Verbesserungen aus, die die Erfolgsraten beim tunnel-Aufbau deutlich erhöhen, auch wenn diese noch nicht für den sicheren Einsatz bereit sind.

Es ist Licht am Ende des tunnel zu sehen, und ich weiß Ihre Geduld zu schätzen, an unserer Seite zu bleiben, während wir vorankommen. Ich rechne damit, dass wir später in dieser Woche ein weiteres Release veröffentlichen, um einige der Verbesserungen auszurollen; danach werden wir den Zustand des Netzes neu bewerten, um zu sehen, ob der Überlastungskollaps angegangen wurde.

* 3) Feedspace

Frosk hat unermüdlich an Feedspace gearbeitet und ein paar Seiten auf der Trac-Seite aktualisiert, darunter ein neues Übersichts-Dokument, eine Liste offener Aufgaben, einige DB-Details und mehr. Schau doch bei http://feedspace.i2p/ vorbei, um über die neuesten Änderungen auf dem Laufenden zu bleiben, und bombardiere Frosk bei nächster Gelegenheit vielleicht mit Fragen :)

* 4) ???

Das ist so ziemlich alles, was ich im Moment besprechen kann, aber kommt heute Abend (20:00 UTC) gerne bei #i2p zu unserem Treffen vorbei, um noch ein wenig weiterzuplaudern!

=jr
