---
title: "Streaming Aktualisierungen"
number: "164"
author: "zzz"
created: "2023-01-24"
lastupdated: "2023-10-23"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/3541"
target: "0.9.58"
implementedin: "0.9.58"
toc: true
---

## Überblick

Java I2P- und i2pd-Router älter als API 0.9.58 (veröffentlicht im März 2023)
sind anfällig für einen Streaming SYN-Paket-Wiedergabeangriff.
Dies ist ein Protokolldesignproblem, kein Implementierungsfehler.

SYN-Pakete sind signiert, aber die Signatur des anfänglichen SYN-Pakets, das von Alice an Bob gesendet wird,
ist nicht an Bobs Identität gebunden, sodass Bob dieses Paket speichern und abspielen kann,
indem er es an ein Opfer Charlie sendet. Charlie wird denken, dass das Paket von
Alice stammt und ihr antworten. In den meisten Fällen ist das harmlos, aber
das SYN-Paket kann anfängliche Daten enthalten (wie ein GET oder POST), die
Charlie sofort verarbeiten wird.


## Design

Die Lösung besteht darin, dass Alice den Ziel-Hash von Bob in die signierten SYN-Daten einfügt.
Bob überprüft beim Empfang, dass dieser Hash mit seinem eigenen Hash übereinstimmt.

Jedes potenzielle Angriffsziel Charlie
überprüft diese Daten und lehnt das SYN ab, wenn es nicht mit seinem Hash übereinstimmt.

Durch die Verwendung des NACKs-Optionsfelds im SYN zur Speicherung des Hashs
ist die Änderung abwärtskompatibel, da NACKs nicht erwartet werden, im SYN-Paket enthalten zu sein und derzeit ignoriert werden.

Alle Optionen sind wie üblich durch die Signatur abgedeckt, sodass Bob den Hash
nicht umschreiben kann.

Wenn Alice und Charlie API 0.9.58 oder neuer sind, wird jeder Wiedergabeversuch von Bob abgelehnt.


## Spezifikation

Aktualisieren Sie die [Streaming-Spezifikation](/docs/specs/streaming/) um den folgenden Abschnitt hinzuzufügen:

### Wiedergabeverhinderung

Um zu verhindern, dass Bob einen Wiedergabeangriff nutzt, indem er ein gültiges, signiertes SYNCHRONIZE-Paket speichert,
das er von Alice empfangen hat, und es später an ein Opfer Charlie sendet,
muss Alice Bobs Ziel-Hash wie folgt im SYNCHRONIZE-Paket einfügen:

.. raw:: html

  {% highlight lang='dataspec' %}
Setzen Sie das NACK-Zählfeld auf 8
  Setzen Sie das NACKs-Feld auf Bobs 32-Byte-Ziel-Hash

{% endhighlight %}

Beim Empfang eines SYNCHRONIZE-Pakets, falls das NACK-Zählfeld 8 ist,
muss Bob das NACKs-Feld als 32-Byte-Ziel-Hash interpretieren
und muss überprüfen, dass es mit seinem Ziel-Hash übereinstimmt.
Er muss auch die Signatur des Pakets wie üblich überprüfen,
da diese das gesamte Paket einschließlich des NACK-Zähl- und NACKs-Felds abdeckt.
Wenn die NACK-Zählung 8 beträgt und das NACKs-Feld nicht übereinstimmt,
muss Bob das Paket verwerfen.

Dies ist für Versionen 0.9.58 und höher erforderlich.
Es ist abwärtskompatibel mit älteren Versionen,
da NACKs in einem SYNCHRONIZE-Paket nicht erwartet werden.
Ziele können und dürfen nicht wissen, welche Version das andere Ende verwendet.

Für das SYNCHRONIZE ACK-Paket, das von Bob an Alice gesendet wird, ist keine Änderung erforderlich;
fügen Sie in diesem Paket keine NACKs hinzu.


## Sicherheitsanalyse

Dieses Problem ist seit der Erstellung des Streaming-Protokolls im Jahr 2004 vorhanden.
Es wurde intern von I2P-Entwicklern entdeckt.
Wir haben keine Beweise dafür, dass das Problem jemals ausgenutzt wurde.
Die tatsächliche Erfolgschance einer Ausnutzung kann stark variieren
je nach Protokoll und Dienst auf Anwendungsebene.
Peer-to-Peer-Anwendungen sind wahrscheinlich stärker betroffen
als Client/Server-Anwendungen.


## Kompatibilität

Keine Probleme. Alle bekannten Implementierungen ignorieren derzeit das NACKs-Feld im SYN-Paket.
Und selbst wenn sie es nicht ignorieren und versuchen würden, es
als NACKs für 8 verschiedene Nachrichten zu interpretieren, wären diese Nachrichten nicht ausstehend
während des SYNCHRONIZE-Handshakes und die NACKs würden keinen Sinn ergeben.


## Migration

Implementierungen können jederzeit Unterstützung hinzufügen, es ist keine Koordination erforderlich.
Java I2P- und i2pd-Router implementierten dies in API 0.9.58 (veröffentlicht im März 2023).


