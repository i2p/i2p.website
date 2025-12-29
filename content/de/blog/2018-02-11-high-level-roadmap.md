---
title: "Übergeordnete Roadmap für 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 wird das Jahr neuer Protokolle, neuer Kooperationen und einer verfeinerten Fokussierung."
categories: ["roadmap"]
---

Eines der vielen Themen, die wir auf dem 34C3 besprochen haben, war, worauf wir uns im kommenden Jahr konzentrieren sollten. Insbesondere wollten wir eine Roadmap, die klar macht, was wir unbedingt erledigen wollen, gegenüber dem, was lediglich wünschenswert wäre, und die außerdem dabei hilft, Neulinge in beide Kategorien einzuarbeiten. Hier ist, was wir uns überlegt haben:

## Priorität: Neue Krypto(grafie!)

Viele der aktuellen Primitive und Protokolle behalten noch immer ihre ursprünglichen Entwürfe aus etwa 2005 bei und müssen verbessert werden. Wir haben seit mehreren Jahren eine Reihe offener Vorschläge mit Ideen vorliegen, doch die Fortschritte waren langsam. Wir waren uns alle einig, dass dies 2018 unsere oberste Priorität sein muss. Die Kernkomponenten sind:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

Die Arbeit an dieser Priorität gliedert sich in mehrere Bereiche:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Wir können neue Protokollspezifikationen nicht im gesamten Netzwerk veröffentlichen, ohne an all diesen Bereichen zu arbeiten.

## Wünschenswert: Code-Wiederverwendung

Einer der Vorteile, die oben genannte Arbeit jetzt zu beginnen, besteht darin, dass es in den letzten Jahren unabhängige Bemühungen gab, einfache Protokolle und Protokoll-Frameworks zu entwickeln, die viele der Ziele erreichen, die wir für unsere eigenen Protokolle haben, und die in der breiteren Community an Akzeptanz gewonnen haben. Durch die Nutzung dieser Arbeit erzielen wir einen Multiplikatoreffekt:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

My proposals in particular will be leveraging the [Noise Protocol Framework](https://noiseprotocol.org/), and the [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). I have collaborations lined up with several people outside I2P for these!

## Priorität: Clearnet-Zusammenarbeit

Zu diesem Thema haben wir in den letzten sechs Monaten nach und nach Interesse aufgebaut. Bei PETS2017, 34C3 und RWC2018 habe ich sehr gute Gespräche darüber geführt, wie wir die Zusammenarbeit mit der breiteren Community verbessern können. Das ist wirklich wichtig, um sicherzustellen, dass wir für neue Protokolle so viel Begutachtung wie möglich einholen. Das größte Hindernis, das ich sehe, ist die Tatsache, dass der Großteil der Zusammenarbeit an der I2P-Entwicklung derzeit innerhalb von I2P selbst stattfindet, was den erforderlichen Aufwand, sich zu beteiligen, erheblich erhöht.

Die beiden Prioritäten in diesem Bereich sind:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Weitere Ziele, die als wünschenswert eingestuft sind:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Ich erwarte, dass die Zusammenarbeit mit Personen außerhalb von I2P vollständig über GitHub erfolgt, um Reibungsverluste zu minimieren.

## Priorität: Vorbereitung auf langlebige Veröffentlichungen

I2P ist jetzt in Debian Sid (deren „unstable“-Repository), das sich in etwa eineinhalb Jahren stabilisieren wird, und wurde zudem in das Ubuntu-Repository übernommen, um in die nächste LTS-Version im April aufgenommen zu werden. Wir werden künftig I2P-Versionen haben, die jahrelang im Umlauf bleiben, und müssen sicherstellen, dass wir mit ihrer Präsenz im Netzwerk umgehen können.

Das vorrangige Ziel ist es, im nächsten Jahr so viele der neuen Protokolle wie praktikabel auszurollen, um rechtzeitig die nächste stabile Debian-Version zu erreichen. Für diejenigen, die mehrjährige Rollouts erfordern, sollten wir die Änderungen zur Vorwärtskompatibilität so früh wie möglich integrieren.

## Priorität: Pluginisierung der aktuellen Apps

Das Debian-Modell fördert separate Pakete für separate Komponenten. Wir waren uns einig, dass es aus mehreren Gründen vorteilhaft wäre, die derzeit gebündelten Java-Anwendungen vom Kern des Java-routers zu entkoppeln:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

In Kombination mit den früheren Prioritäten verschiebt dies das Hauptprojekt von I2P stärker in Richtung z. B. des Linux-Kernels. Wir werden mehr Zeit darauf verwenden, uns auf das Netzwerk selbst zu konzentrieren, und überlassen es Entwicklern von Drittanbietern, sich auf Anwendungen zu konzentrieren, die das Netzwerk nutzen (etwas, das nach unserer Arbeit in den letzten Jahren an APIs und Bibliotheken deutlich einfacher geworden ist).

## Wünschenswert: App-Verbesserungen

Es gibt eine Reihe von Verbesserungen auf Anwendungsebene, an denen wir arbeiten möchten, für die uns angesichts unserer anderen Prioritäten derzeit jedoch nicht die notwendige Entwicklungszeit zur Verfügung steht. In diesem Bereich würden wir uns sehr über neue Mitwirkende freuen! Sobald die oben beschriebene Entkopplung abgeschlossen ist, wird es für jemanden deutlich einfacher, unabhängig vom Haupt-Java router an einer bestimmten Anwendung zu arbeiten.

Eine solche Anwendung, bei der wir uns über Unterstützung freuen würden, ist I2P Android. Wir werden es mit den I2P-Core-Veröffentlichungen auf dem neuesten Stand halten und Fehler nach Möglichkeit beheben, aber es gibt viel, das man tun könnte, um sowohl den zugrunde liegenden Code als auch die Benutzerfreundlichkeit zu verbessern.

## Priorität: Stabilisierung von Susimail und I2P-Bote

Abgesehen davon möchten wir in naher Zukunft gezielt an Fehlerbehebungen für Susimail und I2P-Bote arbeiten (einige davon sind bereits in 0.9.33 eingeflossen). An ihnen wurde in den letzten Jahren weniger gearbeitet als an anderen I2P-Apps, daher möchten wir etwas Zeit darauf verwenden, ihre Codebasen auf den aktuellen Stand zu bringen und es neuen Mitwirkenden leichter zu machen, einzusteigen!

## Wünschenswert: Ticket-Triage

Wir haben einen großen Backlog an Tickets in einer Reihe von I2P-Subsystemen und Apps. Im Rahmen der oben genannten Stabilisierungsbemühungen würden wir gerne einige unserer älteren, lange bestehenden Tickets bereinigen. Noch wichtiger ist uns, sicherzustellen, dass unsere Tickets korrekt organisiert sind, sodass neue Mitwirkende geeignete Tickets finden, an denen sie arbeiten können.

## Priorität: Benutzersupport

Ein Aspekt des oben Genannten, auf den wir uns konzentrieren werden, ist, mit den Nutzerinnen und Nutzern in Kontakt zu bleiben, die sich die Zeit nehmen, Probleme zu melden. Vielen Dank! Je kleiner wir die Feedbackschleife machen können, desto schneller können wir die Probleme lösen, mit denen neue Nutzerinnen und Nutzer konfrontiert sind, und desto wahrscheinlicher ist es, dass sie weiterhin in der Community aktiv bleiben.

## Wir würden uns über Ihre Hilfe freuen!


Das alles wirkt sehr ambitioniert, und das ist es auch! Aber viele der oben genannten Punkte überschneiden sich, und mit sorgfältiger Planung können wir daran erhebliche Fortschritte machen.

Wenn du daran interessiert bist, bei einem der oben genannten Ziele mitzuwirken, komm mit uns chatten! Du findest uns auf OFTC und Freenode (#i2p-dev) sowie auf Twitter (@GetI2P).
