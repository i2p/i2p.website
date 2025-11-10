---
title: "Windows Easy-Install-Bundle 1.9.0 Veröffentlichung"
date: 2022-08-28
author: "idk"
description: "Windows Easy-Install Bundle 1.9.0 - Wichtige Stabilitäts-/Kompatibilitätsverbesserungen"
categories: ["release"]
API_Translate: wahr
---

## Dieses Update enthält den neuen 1.9.0 router und umfangreiche Verbesserungen der Benutzerfreundlichkeit für Bundle‑Nutzer

Diese Version enthält den neuen I2P 1.9.0 router und basiert auf Java 18.02.1.

Die alten Batch-Skripte wurden zugunsten einer flexibleren und stabileren Lösung direkt in jpackage ausgemustert. Dadurch sollten alle in den Batch-Skripten vorhandenen Fehler im Zusammenhang mit der Pfadermittlung und der korrekten Behandlung von Anführungszeichen in Pfaden behoben sein. Nach dem Upgrade können die Batch-Skripte gefahrlos gelöscht werden. Beim nächsten Update werden sie vom Installationsprogramm entfernt.

Ein Teilprojekt zur Verwaltung von Browser-Tools wurde gestartet: i2p.plugins.firefox, das über umfangreiche Möglichkeiten verfügt, I2P-Browser auf vielen Plattformen automatisch und stabil zu konfigurieren. Dieses wurde verwendet, um die Batch-Skripte zu ersetzen, fungiert aber auch als plattformübergreifendes I2P-Browser-Verwaltungstool. Beiträge sind hier willkommen: http://git.idk.i2p/idk/i2p.plugins.firefox im Quell-Repository.

Diese Version verbessert die Kompatibilität für extern ausgeführte I2P router, etwa solche, die vom IzPack installer bereitgestellt werden, sowie für router-Implementierungen Dritter wie i2pd. Durch die verbesserte Erkennung externer router werden weniger Systemressourcen benötigt, die Startzeit verbessert sich, und Ressourcenkonflikte werden verhindert.

Außerdem wurde das Profil auf die neueste Version des Arkenfox-Profils aktualisiert. I2P in Private Browsing und NoScript wurden ebenfalls aktualisiert. Das Profil wurde umstrukturiert, um die Bewertung verschiedener Konfigurationen für unterschiedliche Bedrohungsmodelle zu ermöglichen.
