---
title: "IPv6 Peer Testing"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Closed"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Überblick

Dieser Vorschlag zielt darauf ab, SSU Peer Testing für IPv6 zu implementieren.
Implementiert in 0.9.27.

## Motivation

Wir können nicht zuverlässig feststellen und verfolgen, ob unsere IPv6-Adresse durch eine Firewall blockiert wird.

Als wir vor Jahren die IPv6-Unterstützung hinzugefügt haben, gingen wir davon aus, dass IPv6 nie durch eine Firewall blockiert wird.

In letzter Zeit, in Version 0.9.20 (Mai 2015), haben wir den Erreichbarkeitsstatus von v4/v6 intern aufgeteilt (Ticket #1458).
Siehe dieses Ticket für umfangreiche Informationen und Links.

Wenn Sie sowohl v4 als auch v6 blockiert haben, können Sie einfach im TCP-Konfigurationsbereich auf /confignet einstellen, dass Firewalled erzwungen wird.

Wir haben kein Peer Testing für v6. Es ist im SSU-Spezifikationsdokument verboten.
Wenn wir die v6-Erreichbarkeit nicht regelmäßig testen können, können wir nicht sinnvoll zwischen dem Erreichbarkeitszustand von v6 wechseln.
Übrig bleibt uns das Raten, dass wir erreichbar sind, wenn wir eine eingehende Verbindung erhalten, und das Raten, dass wir es nicht sind, wenn wir längere Zeit keine eingehende Verbindung erhalten haben.
Das Problem ist, dass man, sobald man als nicht erreichbar erklärt wird, seine v6-IP nicht mehr veröffentlicht und dann keine weiteren (nachdem das RI in der netdb aller abgelaufen ist) erhält.

## Design

Peer Testing für IPv6 implementieren, indem vorherige Einschränkungen entfernt werden, dass Peer Testing nur für IPv4 erlaubt war.
Die Peer-Test-Nachricht hat bereits ein Feld für die IP-Länge.

## Spezifikation

Im Abschnitt "Capabilities" der SSU-Übersicht die folgende Ergänzung machen:

Bis Version 0.9.26 war Peer Testing für IPv6-Adressen nicht unterstützt,
und die 'B'-Fähigkeit, falls vorhanden für eine IPv6-Adresse, musste ignoriert werden.
Ab Version 0.9.27 wird Peer Testing für IPv6-Adressen unterstützt, und
das Vorhandensein oder Fehlen der 'B'-Fähigkeit in einer IPv6-Adresse
zeigt tatsächliche Unterstützung (oder mangelnde Unterstützung) an.

In den Peer-Testing-Abschnitten der SSU-Übersicht und SSU-Spezifikation folgende Änderungen vornehmen:

IPv6-Hinweise:
Bis zur Veröffentlichung 0.9.26 wurde nur das Testen von IPv4-Adressen unterstützt.
Daher musste alle Alice-Bob- und Alice-Charlie-Kommunikation über IPv4 erfolgen.
Bob-Charlie-Kommunikation konnte jedoch über IPv4 oder IPv6 erfolgen.
Die Adresse von Alice, wie sie in der PeerTest-Nachricht angegeben ist, musste 4 Bytes betragen.
Ab der Veröffentlichung 0.9.27 wird das Testen von IPv6-Adressen unterstützt, und die Alice-Bob- und Alice-Charlie-Kommunikation kann über IPv6 erfolgen,
falls Bob und Charlie dies mit einer 'B'-Fähigkeit in ihrer veröffentlichten IPv6-Adresse angeben.

Alice sendet die Anfrage an Bob unter Verwendung einer bestehenden Sitzung über das Transportmittel (IPv4 oder IPv6), das sie testen möchte.
Wenn Bob eine Anfrage von Alice über IPv4 erhält, muss Bob einen Charlie auswählen, der eine IPv4-Adresse angibt.
Wenn Bob eine Anfrage von Alice über IPv6 erhält, muss Bob einen Charlie auswählen, der eine IPv6-Adresse angibt.
Die tatsächliche Bob-Charlie-Kommunikation kann über IPv4 oder IPv6 erfolgen (d.h. unabhängig von Alices Adresstyp).

## Migration

Router können entweder:

1) Ihre Version nicht auf 0.9.27 oder höher erhöhen

2) Die 'B'-Fähigkeit aus allen veröffentlichten IPv6-SSU-Adressen entfernen

3) IPv6 Peer Testing implementieren
