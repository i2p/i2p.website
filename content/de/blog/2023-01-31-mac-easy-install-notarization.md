---
title: "Update zur Notarisierung von Mac Easy Install"
date: 2023-01-31
author: "idk, sadie"
description: "Easy Install Bundle für Mac hängt"
categories: ["release"]
API_Translate: wahr
---

Das I2P Easy-Install-Bundle für Mac hat aufgrund des Weggangs seines Maintainers in den letzten zwei Releases keine Updates mehr erhalten. Nutzerinnen und Nutzern des Easy-Install-Bundles für Mac wird empfohlen, auf das klassische Installationsprogramm im Java-Stil umzusteigen, das vor Kurzem wieder auf der Download-Seite bereitgestellt wurde. Version 1.9.0 weist bekannte Sicherheitsprobleme auf und ist für das Hosten von Diensten oder jegliche langfristige Nutzung nicht geeignet. Es wird geraten, so bald wie möglich zu migrieren. Fortgeschrittene Nutzerinnen und Nutzer des Easy-Install-Bundles können dies umgehen, indem sie das Bundle aus dem Quellcode kompilieren und die Software selbst signieren.

## Der Notarisierungsprozess für macOS

Es gibt viele Schritte im Prozess der Verteilung einer Anwendung an Apple-Benutzer. Um eine Anwendung sicher als .dmg zu verteilen, muss die Anwendung einen Notarisierungsprozess bestehen. Um eine Anwendung zur Notarisierung einzureichen, muss ein Entwickler die Anwendung mit einem Satz von Zertifikaten signieren, der eines für Code-Signing und eines für das Signieren der Anwendung selbst umfasst. Diese Signierung muss zu bestimmten Zeitpunkten während des Build-Prozesses erfolgen, bevor das endgültige .dmg-Bundle, das an die Endbenutzer verteilt wird, erstellt werden kann.

I2P Java ist eine komplexe Anwendung, und deshalb ist es ein Prozess von Versuch und Irrtum, die in der Anwendung verwendeten Codearten mit den Zertifikaten von Apple abzugleichen und festzulegen, wo die Signierung erfolgen muss, um einen gültigen Zeitstempel zu erzeugen. Aufgrund dieser Komplexität reicht die vorhandene Dokumentation für Entwickler nicht aus, um dem Team zu helfen, die richtige Kombination von Faktoren zu verstehen, die zu einer erfolgreichen Notarisierung durch Apple führt.

Diese Schwierigkeiten machen den Zeitplan für den Abschluss dieses Prozesses schwer vorherzusagen. Wir werden erst wissen, dass wir fertig sind, wenn wir die Build-Umgebung bereinigen und den Prozess von Anfang bis Ende durchlaufen können. Die gute Nachricht ist, dass wir im Notarisierungsprozess nur noch 4 Fehler haben, gegenüber mehr als 50 beim ersten Versuch, und wir können vernünftigerweise davon ausgehen, dass er vor oder rechtzeitig zur nächsten Veröffentlichung im April abgeschlossen sein wird.

## Optionen für neue macOS-I2P-Installationen und Aktualisierungen

Neue I2P-Teilnehmende können weiterhin den Easy Installer für die macOS-Software 1.9.0 herunterladen. Ich hoffe, gegen Ende April ein Release fertig zu haben. Updates auf die neueste Version werden verfügbar sein, sobald die Notarisierung erfolgreich abgeschlossen wurde.

Die klassische Installationsoption ist ebenfalls verfügbar. Dies erfordert das Herunterladen von Java und der I2P-Software über den .jar-basierten Installer.

[Anweisungen zur JAR-Installation sind hier verfügbar](https://geti2p.net/en/download/macos)

Easy-Install-Benutzer können mithilfe eines lokal erstellten Entwicklungs-Builds auf die neueste Version aktualisieren.

[Die Easy-Install-Build-Anleitungen sind hier verfügbar](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Es besteht auch die Möglichkeit, die Software zu deinstallieren, das I2P-Konfigurationsverzeichnis zu entfernen und I2P mit dem .jar-Installer neu zu installieren.
