---
title: "I2P-Statusnotizen vom 2006-05-09"
date: 2006-05-09
author: "jr"
description: "0.6.1.18-Release mit Verbesserungen der Netzwerkstabilität, einem neuen Entwicklungsserver 'baz' und Herausforderungen bei der Windows-Kompatibilität von GCJ"
categories: ["status"]
---

Hallo zusammen, der Dienstag ist wieder einmal da.

* Index

1) Netzstatus und 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Nach einer weiteren Woche des Testens und der Feinabstimmung haben wir heute Nachmittag eine neue Version veröffentlicht, die uns in eine stabilere Umgebung bringen sollte, von der aus wir Verbesserungen vornehmen können. Wahrscheinlich werden wir jedoch erst viel davon merken, wenn sie breit ausgerollt ist, daher müssen wir vielleicht ein paar Tage abwarten, um zu sehen, wie es läuft, aber die Messungen werden natürlich fortgesetzt.

Ein Aspekt der neuesten Builds und Releases, den zzz neulich angesprochen hat, war, dass die Erhöhung der Anzahl der backup tunnels jetzt einen erheblichen Einfluss haben kann, wenn sie gleichzeitig mit der Reduzierung der Anzahl der parallel tunnels erfolgt. Wir erstellen keine neuen leases, bis wir eine ausreichende Anzahl von live tunnels haben, sodass die backup tunnels im Falle eines Ausfalls eines live tunnels schnell bereitgestellt werden können, was die Häufigkeit verringert, mit der ein Client ohne eine aktive lease bleibt. Das ist allerdings nur ein Feintuning am Symptom, und das neueste Release sollte helfen, die Grundursache anzugehen.

* 2) baz

"baz", die neue Maschine, die bar gespendet hat, ist endlich angekommen, ein amd64-Turion-Laptop (mit winxp auf dem Boot-Laufwerk und ein paar weiteren Betriebssystemen, die über die externen Laufwerke in Aussicht stehen). Ich habe in den letzten Tagen auch daran gearbeitet und versucht, ein paar Deployment-Ideen darauf zu testen. Ein Problem, auf das ich dabei stoße, ist allerdings, gcj unter Windows zum Laufen zu bringen. Genauer gesagt: ein gcj mit einem modernen gnu/classpath. Nach allem, was man hört, sieht es allerdings nicht gut aus – man kann es entweder nativ unter mingw bauen oder von Linux aus cross-kompilieren, aber es gibt Probleme, etwa dass es mit einem Segmentierungsfehler (Segfault) abstürzt, sobald eine Ausnahme (Exception) eine DLL-Grenze überschreitet. Wenn also java.io.File (befindet sich in libgcj.dll) eine Exception wirft und diese von etwas in net.i2p.* (befindet sich in libi2p.dll oder i2p.exe) abgefangen wird, *zack*, weg ist die App.

Ja, das sieht nicht besonders gut aus. Die gcj-Leute wären zwar sehr interessiert, wenn jemand bei der win32-Entwicklung einspringen und helfen könnte, aber tragfähige Unterstützung scheint nicht unmittelbar bevorzustehen. Es sieht also so aus, als müssten wir damit planen, unter Windows weiterhin eine Sun JVM zu verwenden, während wir auf *nix (Unix-ähnliche Systeme) gcj/kaffe/sun/ibm/etc unterstützen. Ich nehme an, das ist allerdings gar nicht so schlimm, denn gerade die *nix-Nutzer haben Probleme, JVMs zu paketieren und zu verteilen.

* 3) ???

Ok, ich bin schon zu spät fürs Meeting, also sollte ich das hier beenden und rüber zum IRC-Fenster wechseln, schätze ich... bis gleich ;)

=jr
