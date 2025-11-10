---
title: "I2P-Statusnotizen für den 19.04.2005"
date: 2005-04-19
author: "jr"
description: "Wöchentliches Update zu den anstehenden Fehlerbehebungen in 0.5.0.7, dem Fortschritt beim SSU UDP-Transport, Roadmap-Änderungen, die 0.6 auf Juni verschieben, und der Q-Entwicklung"
categories: ["status"]
---

Hallo zusammen, es ist wieder so weit,

* Index

1) Netzstatus 2) SSU-Status 3) Roadmap-Update 4) Q-Status 5) ???

* 1) Net status

In den knapp zwei Wochen seit der Veröffentlichung von 0.5.0.6 ist die Entwicklung überwiegend positiv, allerdings sind Dienstanbieter (eepsites(I2P Sites), ircd, etc) in letzter Zeit auf einige Fehler gestoßen. Während es bei den Clients gut aussieht, kann ein Server mit der Zeit in Situationen geraten, in denen ausfallende tunnels einen zu aggressiven Drosselungs-Code auslösen, wodurch der ordnungsgemäße Wiederaufbau und die Veröffentlichung des leaseSet verhindert werden.

There have been some fixes in CVS, among other things, and I expect that we'll have a new 0.5.0.7 out in the next day or so.

* 2) SSU status

Für diejenigen, die meinem (ach so spannenden) Blog nicht folgen: Es gab eine Menge Fortschritte beim UDP-Transport, und im Moment kann man ziemlich sicher sagen, dass der UDP-Transport nicht unser Durchsatz-Engpass sein wird :) Während ich diesen Code debuggt habe, habe ich die Gelegenheit genutzt, auch die Warteschlangen auf höheren Ebenen durchzugehen und Stellen zu finden, an denen wir unnötige Engpässe beseitigen können. Wie ich letzte Woche schon sagte, gibt es jedoch immer noch viel zu tun. Weitere Informationen wird es geben, wenn es weitere Informationen gibt.

* 3) Roadmap update

Es ist jetzt April, daher wurde die Roadmap [1] entsprechend aktualisiert - 0.5.1 gestrichen und einige Termine verschoben. Die größte Änderung ist, 0.6 von April auf Juni zu verschieben, auch wenn diese Änderung in Wirklichkeit nicht so groß ist, wie es scheint. Wie ich letzte Woche erwähnt habe, hat sich mein eigener Zeitplan etwas verschoben, und statt im Juni nach $somewhere umzuziehen, ziehe ich im Mai nach $somewhere um. Obwohl wir das Erforderliche für 0.6 schon diesen Monat fertig haben könnten, kommt es für mich nicht in Frage, ein derart großes Update zu veröffentlichen und dann einen Monat zu verschwinden, denn die Realität bei Software ist, dass es Fehler geben wird, die in Tests nicht entdeckt werden.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum legt bei Q ordentlich los und baut weitere Goodies für uns ein; die neuesten Screenshots sind auf seiner Seite [2] zu sehen. Er hat den Code außerdem auch in CVS eingecheckt (yay), sodass wir hoffentlich bald mit den Alpha-Tests beginnen können. Ich bin sicher, wir werden noch mehr von aum hören, mit Details dazu, wie man helfen kann, oder du kannst dich in die Goodies in CVS unter i2p/apps/q/ vertiefen.

[2] http://aum.i2p/q/

* 5) ???

Es war außerdem noch viel mehr los, mit lebhaften Diskussionen auf der Mailingliste, im Forum und im IRC. Ich werde das hier nicht zusammenfassen, da es nur noch ein paar Minuten bis zum Meeting sind, aber schau einfach vorbei, falls es etwas gibt, das bisher nicht besprochen wurde und das du ansprechen möchtest!

=jr
