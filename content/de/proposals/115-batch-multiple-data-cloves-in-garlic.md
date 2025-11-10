---
title: "Mehrere Datenzehen im Knoblauch bündeln"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Forschungsbedarf"
thread: "http://zzz.i2p/topics/1797"
---

## Übersicht

Dieser Vorschlag betrifft das Senden mehrerer Datenzehen innerhalb einer End-to-End-Knoblauchnachricht, anstatt nur einer.


## Motivation

Nicht klar.


## Erforderliche Änderungen

Die Änderungen wären in OCMOSJ und verwandten Hilfsklassen sowie im ClientMessagePool notwendig. Da es jetzt keine Warteschlange gibt, wären eine neue Warteschlange und eine gewisse Verzögerung erforderlich. Eine Bündelung müsste eine maximale Knoblauchgröße beachten, um ein Herunterfallen zu minimieren. Vielleicht 3KB? Man möchte die Dinge zuerst instrumentieren, um zu messen, wie oft dies verwendet werden würde.


## Überlegungen

Es ist unklar, ob dies irgendeinen nützlichen Effekt haben wird, da das Streaming bereits Bündelungen durchführt und das optimale MTU auswählt. Bündelung würde die Nachrichtengröße und die exponentielle Fallwahrscheinlichkeit erhöhen.

Die Ausnahme ist unkomprimierter Inhalt, der auf der I2CP-Ebene gezippt wird. Aber HTTP-Verkehr wird bereits auf einer höheren Ebene komprimiert, und Bittorrent-Daten sind normalerweise unkomprimierbar. Was bleibt also übrig? I2pd führt derzeit nicht die x-i2p-gzip-Komprimierung durch, sodass es dort erheblich mehr helfen könnte. Aber das erklärte Ziel, nicht ohne Tags auszukommen, wird besser durch eine ordnungsgemäße Fensterimplementierung in seiner Streaming-Bibliothek behoben.


## Kompatibilität

Dies ist rückwärtskompatibel, da der Knoblauchempfänger bereits alle empfangenen Zehen verarbeitet.
