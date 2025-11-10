---
title: "I2P Jpackages erhalten ihr erstes Update"
date: 2021-11-02
author: "idk"
description: "Neue, leichter zu installierende Pakete erreichen einen neuen Meilenstein"
categories: ["general"]
API_Translate: wahr
---

Vor einigen Monaten haben wir neue Pakete veröffentlicht, die neuen Nutzern den Einstieg in das I2P-Netzwerk erleichtern sollen, indem sie die Installation und Konfiguration von I2P für mehr Menschen vereinfachen. Wir haben Dutzende Schritte aus dem Installationsprozess entfernt, indem wir von einer externen JVM auf ein Jpackage umgestellt, Standardpakete für die Zielbetriebssysteme erstellt und sie so signiert haben, dass das Betriebssystem sie erkennt, um die Nutzer zu schützen. Seitdem haben die jpackage routers einen neuen Meilenstein erreicht: Sie werden in Kürze ihre ersten inkrementellen Updates erhalten. Diese Updates werden das JDK 16 jpackage durch ein aktualisiertes JDK 17 jpackage ersetzen und Korrekturen für einige kleine Fehler enthalten, die wir nach der Veröffentlichung entdeckt haben.

## Gemeinsame Aktualisierungen für Mac OS und Windows

Alle jpackaged I2P-Installationsprogramme erhalten die folgenden Aktualisierungen:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Bitte so bald wie möglich aktualisieren.

## I2P-Windows-Jpackage-Updates

Windows only packages recieve the following updates:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Eine vollständige Liste der Änderungen finden Sie in der changelog.txt in i2p.firefox

## I2P Mac OS Jpackage-Aktualisierungen

Nur Mac-OS-Pakete erhalten die folgenden Aktualisierungen:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Eine Zusammenfassung der Entwicklung finden Sie in den Checkins von i2p-jpackage-mac.
