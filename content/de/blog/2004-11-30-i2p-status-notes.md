---
title: "I2P-Statusnotizen für 2004-11-30"
date: 2004-11-30
author: "jr"
description: "Wöchentliches I2P-Status-Update zu den Releases 0.4.2 und 0.4.2.1, Entwicklungen bei mail.i2p, Fortschritten bei i2p-bt und Diskussionen zur eepsite-Sicherheit"
categories: ["status"]
---

Hallo zusammen

## Inhaltsverzeichnis

1. 0.4.2 and 0.4.2.1
2. mail.i2p
3. i2p-bt
4. eepsites(I2P Sites)
5. ???

## 1) 0.4.2 und 0.4.2.1

Seit wir endlich 0.4.2 veröffentlicht haben, sind die Zuverlässigkeit und der Durchsatz des Netzwerks eine Zeit lang deutlich gestiegen, bis wir über die ganz neuen, von uns verursachten Fehler gestolpert sind. Bei den meisten halten die IRC-Verbindungen stundenlang, doch für manche, die von den Problemen betroffen waren, war die Erfahrung recht holprig. Es gab jedoch eine ganze Reihe von Fehlerbehebungen, und später heute Abend oder spätestens morgen früh werden wir eine neue Version 0.4.2.1 zum Download bereitstellen.

## 2) mail.i2p

Heute habe ich von postman einen Zettel zugesteckt bekommen, in dem stand, dass er ein paar Dinge besprechen möchte - für mehr Infos siehe die Sitzungsprotokolle (oder, wenn du das vor der Sitzung liest, schau einfach vorbei).

## 3) i2p-bt

Einer der Nachteile der neuen Version ist, dass wir bei der i2p-bt-Portierung auf einige Probleme stoßen. Einige der Probleme wurden in der Streaming-Bibliothek identifiziert, gefunden und behoben, aber es ist weitere Arbeit erforderlich, um sie auf den Stand zu bringen, den wir benötigen.

## 4) eepsites(I2P-Seiten)

Im Laufe der letzten Monate gab es auf der Mailingliste, im Kanal und im Forum einige Diskussionen über Probleme damit, wie eepsites(I2P Sites) und der eepproxy funktionieren – in letzter Zeit wurden Probleme genannt, etwa wie und welche Header gefiltert werden; andere haben auf die Gefahren schlecht konfigurierter Browser hingewiesen, und es gibt auch DrWoos Seite, die viele der Risiken zusammenfasst. Ein besonders bemerkenswerter Punkt ist die Tatsache, dass einige Leute aktiv an Applets arbeiten, die den Computer des Nutzers kapern, wenn der Nutzer Applets nicht deaktiviert. (DEAKTIVIEREN SIE ALSO JAVA UND JAVASCRIPT IN IHREM BROWSER)

Das führt natürlich zu einer Diskussion darüber, wie wir Dinge absichern können. Ich habe Vorschläge gehört, einen eigenen Browser zu entwickeln oder einen mit vorkonfigurierten, sicheren Einstellungen mitzuliefern, aber seien wir realistisch - das ist viel mehr Arbeit, als hier irgendjemand auf sich nehmen wird. Allerdings gibt es drei weitere Lager:

1. Use a fascist HTML filter and tie it in with the proxy
2. Use a fascist HTML filter as part of a script that fetches pages for you
3. Use a secure macro language

Der erste Ansatz ist im Großen und Ganzen so wie das, was wir jetzt haben, außer dass wir die dargestellten Inhalte mit etwas wie muffin oder dem Anonymitätsfilter von freenet filtern. Der Nachteil dabei ist, dass weiterhin HTTP-Header offengelegt werden, sodass wir auch die HTTP-Ebene anonymisieren müssten.

Die zweite ist ähnlich dem, was man auf `http://duck.i2p/` mit dem CGIproxy sehen kann, oder alternativ dem, was man in Freenets fproxy sehen kann. Damit ist auch die HTTP-Seite abgedeckt.

Die dritte Option hat Vor- und Nachteile – sie ermöglicht uns, wesentlich überzeugendere Benutzeroberflächen zu verwenden (da wir einige als sicher bekannte JavaScript-Elemente usw. gefahrlos nutzen können), bringt jedoch den Nachteil fehlender Abwärtskompatibilität mit sich. Vielleicht wäre eine Kombination davon mit einem Filter sinnvoll, sodass sich die Makros in gefiltertem HTML einbetten lassen?

Wie dem auch sei, dies ist eine wichtige Entwicklungsarbeit und befasst sich mit einem der überzeugendsten Anwendungsfälle von I2P - sicheren und anonymen interaktiven Websites. Vielleicht hat jemand noch andere Ideen oder Informationen dazu, wie wir das Benötigte beschaffen können?

## 5) ???

Okay, ich komme zu spät zur Besprechung, also sollte ich das wohl unterschreiben und auf den Weg schicken, oder?

=jr [Mal sehen, ob ich gpg richtig zum Laufen bekomme...]
