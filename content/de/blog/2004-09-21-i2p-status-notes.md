---
title: "I2P-Statusnotizen vom 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Wöchentliches I2P-Status-Update über den Entwicklungsfortschritt, Verbesserungen beim TCP-Transport und die neue userhosts.txt-Funktion"
categories: ["status"]
---

Hallo zusammen, ein kurzes Update diese Woche

## Stichwortverzeichnis

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Entwicklungsstatus

Das Netzwerk war in der letzten Woche ziemlich stabil, sodass ich meine Zeit auf das 0.4.1-Release konzentrieren konnte - den TCP-Transport zu überarbeiten, Unterstützung für die Erkennung von IP-Adressen hinzuzufügen und dieses alte "target changed identities"-Ding zu entfernen. Das sollte außerdem die Notwendigkeit von dyndns-Einträgen überflüssig machen.

Es wird nicht die ideale 0-Klick-Einrichtung für Nutzer hinter NATs oder Firewalls sein – sie müssen weiterhin die Portweiterleitung einrichten, damit sie eingehende TCP-Verbindungen empfangen können. Es sollte jedoch weniger fehleranfällig sein. Ich gebe mein Bestes, es abwärtskompatibel zu halten, aber ich mache in dieser Hinsicht keine Versprechen. Mehr Neuigkeiten, sobald es fertig ist.

## 2) Neue userhosts.txt vs. hosts.txt

In der nächsten Version werden wir die häufig gewünschte Unterstützung für zwei hosts.txt-Dateien haben - eine, die während Upgrades (oder von `http://dev.i2p.net/i2p/hosts.txt`) überschrieben wird, und eine, die der Benutzer lokal pflegen kann. In der nächsten Version (oder CVS HEAD) können Sie die Datei "userhosts.txt" bearbeiten, die vor hosts.txt nach Einträgen geprüft wird - bitte nehmen Sie Ihre lokalen Änderungen dort vor, da der Aktualisierungsvorgang hosts.txt überschreiben wird (nicht jedoch userhosts.txt).

## 3) ???

Wie schon erwähnt, gibt es diese Woche nur ein paar kurze Notizen. Habt ihr sonst noch etwas, das ihr ansprechen wollt? Kommt in ein paar Minuten einfach zur Besprechung vorbei.

=jr
