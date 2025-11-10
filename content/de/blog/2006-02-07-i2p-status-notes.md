---
title: "I2P-Statushinweise für 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Fortschritte bei den PRE-Netzwerktests, Optimierung mit kurzem Exponenten für die ElGamal-Verschlüsselung und I2Phex 0.1.1.37 mit gwebcache-Unterstützung"
categories: ["status"]
---

Hallo zusammen, es ist wieder Dienstag.

* Index

1) Netzstatus 2) _PRE Netzfortschritt 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

Im Live-Netz hat es in der letzten Woche keine wesentlichen Änderungen gegeben, daher hat sich der Status des Live-Netzes nicht viel geändert. Andererseits...

* 2) _PRE net progress

Letzte Woche habe ich begonnen, rückwärtsinkompatiblen Code für das Release 0.6.1.10 in einem separaten Branch in CVS (i2p_0_6_1_10_PRE) einzuchecken, und eine Gruppe von Freiwilligen hat bei der Erprobung geholfen. Dieses neue _PRE Netzwerk kann nicht mit dem Live-Netz kommunizieren und bietet keine nennenswerte Anonymität (da es weniger als 10 Peers gibt). Mit den Pen-Register-Protokollen aus diesen routers konnten einige erhebliche Fehler sowohl im neuen als auch im alten Code aufgespürt und beseitigt werden, auch wenn die weiteren Tests und Verbesserungen andauern.

Ein Aspekt der neuen Kryptografie für die tunnel-Erstellung ist, dass der Ersteller die aufwändige asymmetrische Verschlüsselung für jeden Hop im Voraus durchführen muss, während die alte tunnel-Erstellung die Verschlüsselung nur dann durchführte, wenn der vorherige Hop zugestimmt hat, am tunnel teilzunehmen. Diese Verschlüsselung konnte 400–1000 ms oder mehr dauern, abhängig sowohl von der lokalen CPU-Leistung als auch von der Länge des tunnel (für jeden Hop wird eine vollständige ElGamal-Verschlüsselung durchgeführt). Eine Optimierung, die derzeit im _PRE net verwendet wird, ist die Verwendung eines kurzen Exponenten [1] – anstatt ein 2048-Bit-‚x‘ als ElGamal-Schlüssel zu verwenden, nutzen wir ein 228-Bit-‚x‘, was die empfohlene Länge ist, um dem Aufwand des Diskreten-Logarithmus-Problems zu entsprechen. Dadurch ist die Verschlüsselungszeit pro Hop um eine Größenordnung gesunken, allerdings wirkt es sich nicht auf die Entschlüsselungszeit aus.

Es gibt viele widersprüchliche Ansichten zur Verwendung kurzer Exponenten, und im allgemeinen Fall ist das nicht sicher; nach allem, was ich in Erfahrung bringen konnte, sollte die Ordnung von q jedoch in Ordnung sein, da wir eine feste sichere Primzahl (Oakley-Gruppe 14 [2]) verwenden. Wenn dazu jemand weitere Gedanken in dieser Richtung hat, würde ich gerne mehr hören.

Die eine große Alternative besteht darin, auf 1024-Bit-Verschlüsselung umzusteigen (in der wir dann vielleicht einen kurzen 160-Bit-Exponenten verwenden könnten).  Das könnte unabhängig davon sinnvoll sein, und falls die 2048-Bit-Verschlüsselung im _PRE net zu problematisch ist, könnten wir den Wechsel innerhalb des _PRE net vollziehen.  Andernfalls könnten wir bis zum Release 0.6.1.10 warten, wenn die neue Kryptografie breiter ausgerollt ist, um zu sehen, ob es notwendig ist.  Viel mehr Informationen werden folgen, falls ein solcher Wechsel wahrscheinlich erscheint.

[1] "Über die Diffie-Hellman-Schlüsselvereinbarung mit kurzen Exponenten" -     van Oorschot, Weiner bei EuroCrypt 96.  gespiegelt unter     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

Jedenfalls gibt es große Fortschritte im _PRE net, wobei der Großteil der Kommunikation darüber im #i2p_pre-Channel auf irc2p stattfindet.

* 3) I2Phex 0.1.1.37

Complication hat den neuesten I2Phex-Code zusammengeführt und gepatcht, um gwebcaches zu unterstützen, kompatibel mit Rawn's pycache port. Das bedeutet, dass Nutzer I2Phex herunterladen, installieren, auf "Connect to the network" klicken und nach ein oder zwei Minuten einige Referenzen zu bestehenden I2Phex-Peers erhalten und ins Netz gehen. Kein Ärger mehr mit dem manuellen Verwalten von i2phex.hosts-Dateien oder dem manuellen Austauschen von Schlüsseln (w00t)! Standardmäßig gibt es zwei gwebcaches, aber sie können geändert oder ein dritter hinzugefügt werden, indem die Eigenschaften i2pGWebCache0, i2pGWebCache1 oder i2pGWebCache2 in i2phex.cfg angepasst werden.

Gute Arbeit, Complication und Rawn!

* 4) ???

Das war’s fürs Erste, was auch gut ist, denn ich bin schon zu spät fürs Meeting :) Bis gleich in #i2p

=jr
