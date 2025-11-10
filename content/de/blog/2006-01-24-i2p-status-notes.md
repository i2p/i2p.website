---
title: "I2P-Statushinweise für 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Netzwerkstatus-Update, neuer tunnel-Build-Prozess für 0.6.2 und Zuverlässigkeitsverbesserungen"
categories: ["status"]
---

Hi zusammen, der Dienstag kommt immer wieder...

* Index

1) Netzstatus 2) Neuer Build-Prozess 3) ???

* 1) Net status

Die vergangene Woche hat dem Netzwerk nicht viele Änderungen gebracht, die meisten Nutzer (77%) sind auf die neueste Release-Version aktualisiert. Dennoch stehen einige umfangreiche Änderungen an, die mit dem neuen tunnel-Aufbauprozess zusammenhängen, und diese Änderungen werden für diejenigen, die helfen, die unveröffentlichten Builds zu testen, zu einigen Problemen führen. Insgesamt sollten Nutzer der Releases jedoch weiterhin mit einem recht zuverlässigen Betrieb rechnen.

* 2) New build process

Als Teil der tunnel-Überarbeitung für 0.6.2 ändern wir das im router verwendete Verfahren, um sich besser an wechselnde Bedingungen anzupassen und die Last sauberer zu handhaben. Dies ist ein Vorläufer zur Integration der neuen Strategien zur Peer-Auswahl und der neuen Kryptographie für die tunnel-Erstellung und ist vollständig abwärtskompatibel. Allerdings bereinigen wir dabei einige der Eigenheiten im tunnel-Aufbauprozess, und auch wenn einige dieser Eigenheiten geholfen haben, manche Zuverlässigkeitsprobleme zu kaschieren, könnten sie zu einem weniger als optimalen Kompromiss zwischen Anonymität und Zuverlässigkeit geführt haben. Konkret wurden bei katastrophalen Ausfällen fallback 1 hop tunnels verwendet - der neue Prozess wird stattdessen Unerreichbarkeit bevorzugen, anstatt fallback tunnels zu verwenden, was bedeutet, dass Nutzer mehr Zuverlässigkeitsprobleme sehen werden. Zumindest werden sie sichtbar sein, bis die Ursache des tunnel-Zuverlässigkeitsproblems behoben ist.

Jedenfalls gewährleistet der Build-Prozess derzeit keine akzeptable Zuverlässigkeit, aber sobald das der Fall ist, werden wir es euch allen in einem Release ausrollen.

* 3) ???

Ich weiß, dass ein paar andere an verschiedenen verwandten Aufgaben arbeiten, aber ich überlasse es ihnen, uns die Neuigkeiten mitzuteilen, wenn sie es für angebracht halten.  Wie auch immer, wir sehen uns alle in ein paar Minuten beim Meeting!

=jr
