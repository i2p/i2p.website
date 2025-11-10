---
title: "Zurücksetzen der Nachricht für ElGamal/AES+SessionTags"
number: "124"
author: "Original"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Offen"
thread: "http://zzz.i2p/topics/2056"
---

## Übersicht

Dieser Vorschlag betrifft eine I2NP-Nachricht, die verwendet werden kann, um die Sitzungstags zwischen zwei Zielen zurückzusetzen.

## Motivation

Stellen Sie sich vor, ein Ziel hat eine Menge bestätigter Tags für ein anderes Ziel. Aber dieses Ziel wurde neu gestartet oder hat diese Tags auf andere Weise verloren. Das erste Ziel sendet weiterhin Nachrichten mit Tags, und das zweite Ziel kann sie nicht entschlüsseln. Das zweite Ziel sollte eine Möglichkeit haben, dem ersten Ziel mitzuteilen, die Tags zurückzusetzen (von vorne zu beginnen) durch eine zusätzliche Knoblauchzehe, ebenso wie es ein aktualisiertes LeaseSet sendet.

## Design

### Vorgeschlagene Nachricht

Diese neue Knoblauchzehe muss den Liefertyp "Ziel" mit einer neuen I2NP-Nachricht enthalten, die wie "Tags zurücksetzen" genannt wird und den Ident-Hash des Absenders enthält. Sie sollte einen Zeitstempel und eine Signatur enthalten.

Kann jederzeit gesendet werden, falls ein Ziel die Nachrichten nicht entschlüsseln kann.

### Verwendung

Wenn ich meinen Router neu starte und versuche, eine Verbindung zu einem anderen Ziel herzustellen, sende ich eine Knoblauchzehe mit meinem neuen LeaseSet und würde eine zusätzliche Knoblauchzehe mit dieser Nachricht senden, die meine Adresse enthält. Ein entferntes Ziel erhält diese Nachricht, löscht alle ausgehenden Tags zu mir und beginnt von vorne mit ElGamal.

Es ist ein ziemlich häufiger Fall, dass ein Ziel nur mit einem entfernten Ziel kommuniziert. Im Falle eines Neustarts sollte es diese Nachricht an alle zusammen mit der ersten Streaming- oder Datagramm-Nachricht senden.
