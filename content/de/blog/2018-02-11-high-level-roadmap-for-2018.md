---
title: "Übergeordnete Roadmap für 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 wird das Jahr neuer Protokolle, neuer Kooperationen und eines präziseren Fokus"
categories: ["roadmap"]
---

Eines der vielen Dinge, die wir auf dem 34C3 besprochen haben, war, worauf wir uns im kommenden Jahr konzentrieren sollten. Insbesondere wollten wir eine Roadmap, die klar macht, was wir auf jeden Fall erledigen wollen, im Gegensatz zu dem, was lediglich wünschenswert wäre, und die außerdem dabei hilft, Neulinge in beide Kategorien einzuarbeiten. Hier ist, was dabei herausgekommen ist:

## Priorität: Neue Krypto(grafie!)

Viele der aktuellen Primitive und Protokolle behalten noch ihre ursprünglichen Entwürfe aus der Zeit um 2005 bei und müssen verbessert werden. Wir haben seit mehreren Jahren eine Reihe offener Vorschläge mit Ideen, doch das Vorankommen war schleppend. Wir waren uns alle einig, dass dies 2018 unsere höchste Priorität sein muss. Die Kernkomponenten sind:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

Die Arbeit an dieser Priorität gliedert sich in mehrere Bereiche:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Wir können neue Protokollspezifikationen nicht im gesamten Netzwerk ausrollen, ohne an all diesen Bereichen zu arbeiten.

## Wünschenswert: Wiederverwendung von Code

Einer der Vorteile, die oben beschriebene Arbeit jetzt zu beginnen, besteht darin, dass es in den letzten Jahren unabhängige Bemühungen gab, einfache Protokolle und Protokoll-Frameworks zu entwickeln, die viele der Ziele erfüllen, die wir für unsere eigenen Protokolle verfolgen, und die in der breiteren Community an Akzeptanz gewonnen haben. Indem wir diese Arbeit nutzen, erzielen wir einen „Multiplikatoreffekt“:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Meine Vorschläge werden insbesondere das [Noise Protocol Framework](https://noiseprotocol.org/) sowie das [SPHINX-Paketformat](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html) nutzen. Dafür habe ich bereits Kooperationen mit mehreren Personen außerhalb von I2P vereinbart!

## Priorität: Zusammenarbeit im Clearnet

Zu diesem Thema haben wir in den letzten etwa sechs Monaten nach und nach Interesse aufgebaut. Bei PETS2017, dem 34C3 und der RWC2018 habe ich einige sehr gute Gespräche darüber geführt, wie wir die Zusammenarbeit mit der breiteren Community verbessern können. Das ist wirklich wichtig, um sicherzustellen, dass wir für neue Protokolle so viel Begutachtung wie möglich erhalten. Die größte Hürde, die ich gesehen habe, ist die Tatsache, dass der Großteil der Zusammenarbeit an der I2P-Entwicklung derzeit innerhalb von I2P selbst stattfindet, was den Aufwand, sich zu beteiligen, erheblich erhöht.

Die beiden Prioritäten in diesem Bereich sind:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Weitere Ziele, die als wünschenswert gelten:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Ich erwarte, dass die Zusammenarbeit mit Personen außerhalb von I2P vollständig auf GitHub erfolgt, um Reibung zu minimieren.

## Priorität: Vorbereitung auf langfristige Releases

I2P ist jetzt in Debian Sid (deren unstable-Repository), das sich voraussichtlich in etwa eineinhalb Jahren stabilisieren wird, und wurde außerdem in das Ubuntu-Repository übernommen, um in die nächste LTS-Veröffentlichung im April aufgenommen zu werden. Wir werden I2P-Versionen haben, die jahrelang im Umlauf bleiben, und müssen sicherstellen, dass wir mit ihrer Präsenz im Netzwerk umgehen können.

Das Hauptziel ist hier, im nächsten Jahr so viele der neuen Protokolle wie praktikabel auszurollen, rechtzeitig zur nächsten stabilen Debian-Veröffentlichung. Für diejenigen, die eine mehrjährige Einführung erfordern, sollten wir die Vorwärtskompatibilitätsänderungen so früh wie möglich integrieren.

## Priorität: Umstellung der aktuellen Apps auf Plugins

Das Debian-Modell befürwortet getrennte Pakete für getrennte Komponenten. Wir kamen überein, dass die Entkopplung der derzeit gebündelten Java-Anwendungen vom Kern des Java router aus mehreren Gründen vorteilhaft wäre:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

In Kombination mit den früheren Prioritäten rückt das Hauptprojekt I2P stärker in Richtung etwa des Linux-Kernels. Wir werden mehr Zeit darauf verwenden, uns auf das Netzwerk selbst zu konzentrieren, und es Entwicklern von Drittanbietern überlassen, sich auf Anwendungen zu konzentrieren, die das Netzwerk nutzen (was nach unserer Arbeit in den letzten Jahren an APIs und Bibliotheken erheblich einfacher ist).

## Wünschenswert: App-Verbesserungen

Es gibt eine ganze Reihe von Verbesserungen auf Anwendungsebene, an denen wir arbeiten möchten, für die wir aber angesichts unserer anderen Prioritäten derzeit keine Entwicklerkapazitäten haben. In diesem Bereich würden wir uns sehr über neue Mitwirkende freuen! Sobald die oben beschriebene Entkopplung abgeschlossen ist, wird es für jemanden deutlich einfacher, unabhängig vom Haupt-Java router an einer bestimmten Anwendung zu arbeiten.

Eine solche Anwendung, bei der wir sehr gerne Unterstützung hätten, ist I2P Android. Wir werden es mit den I2P-Kernversionen auf dem neuesten Stand halten und Fehler beheben, so gut wir können, aber es gibt noch viel, was getan werden könnte, um sowohl den zugrunde liegenden Code als auch die Benutzerfreundlichkeit zu verbessern.

## Priorität: Stabilisierung von Susimail und I2P-Bote

Abgesehen davon möchten wir in naher Zukunft gezielt an Fehlerbehebungen für Susimail und I2P-Bote arbeiten (einige davon sind bereits in 0.9.33 eingeflossen). In den letzten Jahren wurde an ihnen weniger gearbeitet als an anderen I2P-Apps, daher möchten wir Zeit investieren, ihre Codebasen auf den aktuellen Stand zu bringen und es neuen Mitwirkenden leichter zu machen, einzusteigen!

## Wünschenswert: Ticket-Triage

Wir haben einen großen Rückstand an Tickets in einer Reihe von I2P-Subsystemen und Apps. Im Rahmen der oben genannten Stabilisierungsbemühungen würden wir gerne einige unserer älteren, seit Langem offenen Issues bereinigen. Noch wichtiger ist uns, sicherzustellen, dass unsere Tickets korrekt organisiert sind, damit neue Mitwirkende geeignete Tickets finden, an denen sie arbeiten können.

## Priorität: Benutzersupport

Ein Aspekt des oben Genannten, auf den wir uns konzentrieren werden, ist, mit den Nutzerinnen und Nutzern in Kontakt zu bleiben, die sich die Zeit nehmen, Probleme zu melden. Vielen Dank! Je kürzer wir die Feedback-Schleife gestalten können, desto schneller können wir die Probleme lösen, auf die neue Nutzerinnen und Nutzer stoßen, und desto wahrscheinlicher ist es, dass sie sich weiterhin in der Community beteiligen.

## Wir würden uns sehr über Ihre Hilfe freuen!

Das alles wirkt sehr ambitioniert, und das ist es auch! Aber viele der oben genannten Punkte überschneiden sich, und mit sorgfältiger Planung können wir einen erheblichen Teil davon bewältigen.

Wenn Sie daran interessiert sind, bei einem der oben genannten Ziele mitzuhelfen, chatten Sie mit uns! Sie finden uns auf OFTC und Freenode (#i2p-dev) sowie auf Twitter (@GetI2P).
