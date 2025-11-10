---
title: "I2P-Statusnotizen vom 2005-07-05"
date: 2005-07-05
author: "jr"
description: "Wöchentliches Update zu den Fortschritten beim SSU-Transport, zur Abmilderung von tunnel-IV-Angriffen und zur SSU-MAC-Optimierung mit HMAC-MD5"
categories: ["status"]
---

Hallo zusammen, es ist wieder soweit,

* Index

1) Entwicklungsstatus 2) Tunnel IVs 3) SSU MACs 4) ???

* 1) Dev status

Schon wieder eine Woche, schon wieder eine Nachricht mit der Aussage "Es gab viel Fortschritt beim SSU-Transport" ;) Meine lokalen Änderungen sind stabil und wurden in CVS eingecheckt (HEAD steht bei 0.5.0.7-9), aber noch kein Release. Bald mehr Neuigkeiten dazu. Details zu den nicht-SSU-bezogenen Änderungen stehen in der History [1], allerdings lasse ich SSU-bezogene Änderungen bislang aus dieser Liste heraus, da SSU bisher von Nicht-Entwicklern noch nicht genutzt wird (und die Entwickler lesen i2p-cvs@ :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

In den letzten Tagen hat dvorak gelegentlich Überlegungen zu verschiedenen Möglichkeiten veröffentlicht, die tunnel-Kryptographie anzugreifen, und obwohl die meisten davon bereits behandelt waren, konnten wir ein Szenario ausarbeiten, das es Teilnehmern ermöglichen würde, ein Nachrichtenpaar zu markieren, um festzustellen, dass sie im selben tunnel sind. Die Funktionsweise war folgende: Der früher in der Kette liegende Peer ließ eine Nachricht an sich vorbeigehen und nahm später den IV (Initialisierungsvektor) und den ersten Datenblock aus dieser ersten tunnel-Nachricht heraus, um sie in eine neue einzusetzen. Diese neue wäre natürlich beschädigt, sähe aber nicht wie ein Wiederholungsangriff aus, da die IVs unterschiedlich wären. Weiter unten in der Kette könnte der zweite Peer diese Nachricht dann einfach verwerfen, sodass der tunnel-Endpunkt den Angriff nicht erkennen könnte.

Eines der Kernprobleme dabei ist, dass es keine Möglichkeit gibt, eine tunnel-Nachricht während ihres Weges durch den tunnel zu verifizieren, ohne eine ganze Reihe von Angriffen zu eröffnen (siehe einen früheren tunnel-Krypto-Vorschlag [2] für eine Methode, die dem nahekommt, aber mit ziemlich fragwürdigen Wahrscheinlichkeiten arbeitet und einige künstliche Beschränkungen den tunnels auferlegt).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Es gibt jedoch eine triviale Möglichkeit, den beschriebenen Angriff zu umgehen – behandle einfach xor(IV, first data block) als den eindeutigen Identifikator, der in den Bloom-Filter eingespeist wird, statt der IV allein. Auf diese Weise sehen Zwischen-Peers das Duplikat und verwerfen es, bevor es den zweiten kooperierenden Peer erreicht. CVS wurde aktualisiert, um diese Gegenmaßnahme aufzunehmen, obwohl ich sehr, sehr stark bezweifle, dass dies angesichts der aktuellen Netzwerkgröße eine praktische Bedrohung darstellt. Deshalb bringe ich es nicht als eigenständiges Release heraus.

Das beeinträchtigt jedoch nicht die Machbarkeit anderer Timing- oder Shaping-Angriffe, aber am besten gehen wir die einfach zu handhabenden Angriffe an, sobald wir sie sehen.

* 3) SSU MACs

Wie in der Spezifikation [3] beschrieben, verwendet der SSU-Transport für jedes übertragene Datagramm einen MAC. Dies kommt zusätzlich zu dem mit jeder I2NP-Nachricht gesendeten Prüf-Hash (sowie den Ende-zu-Ende-Prüf-Hashes bei Client-Nachrichten). Derzeit verwenden die Spezifikation und der Code einen gekürzten HMAC-SHA256 – wobei nur die ersten 16 Bytes des MAC übertragen und verifiziert werden. Das ist *hust* etwas verschwenderisch, da der HMAC den SHA256-Hash in seinem Ablauf zweimal verwendet, jeweils mit einem 32-Byte-Hash, und jüngstes Profiling des SSU-Transports darauf hindeutet, dass dies auf dem kritischen Pfad der CPU-Last liegt. Daher habe ich ein wenig damit experimentiert, HMAC-SHA256-128 durch ein schlichtes HMAC-MD5(-128) zu ersetzen – auch wenn MD5 eindeutig nicht so stark ist wie SHA256, kürzen wir SHA256 ohnehin auf dieselbe Größe wie MD5, sodass der für eine Kollision erforderliche Brute-Force-Aufwand derselbe ist (2^64 Versuche). Ich experimentiere derzeit damit, und der Geschwindigkeitszuwachs ist erheblich (mehr als das 3-Fache des HMAC-Durchsatzes bei 2KB-Paketen gegenüber SHA256), sodass wir das vielleicht stattdessen produktiv einsetzen. Oder wenn jemand einen triftigen Grund dagegen (oder eine bessere Alternative) hat, lässt es sich leicht austauschen (nur eine einzige Codezeile).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

Das war’s fürs Erste, und wie immer könnt ihr eure Gedanken und Bedenken jederzeit gern posten. CVS HEAD lässt sich jetzt wieder bauen für alle, die kein junit installiert haben (für den Moment habe ich die Tests aus i2p.jar herausgenommen, sie lassen sich aber weiterhin mit dem test ant target ausführen), und ich erwarte, dass es recht bald weitere Neuigkeiten zum 0.6-Testing geben wird (ich kämpfe im Moment noch mit den Merkwürdigkeiten der colo box (Server im Rechenzentrum) - Verbindungen per Telnet zu meinen eigenen Interfaces schlagen lokal fehl (ohne hilfreiches errno), funktionieren remote, und das alles ohne iptables oder andere Filter. Freude). Ich habe zu Hause immer noch keinen Netzzugang, daher werde ich heute Abend nicht beim Meeting dabei sein, aber vielleicht nächste Woche.

=jr
