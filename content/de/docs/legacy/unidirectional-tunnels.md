---
title: "Unidirektionale Tunnel"
description: "Historische Zusammenfassung von I2Ps unidirektionalem Tunnel-Design"
slug: "unidirectional"
aliases:
  - "/de/unidirectional-tunnels"
  - "/de/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Überblick

Diese Seite beschreibt die Ursprünge und das Design der unidirektionalen Tunnel von I2P. Für weitere Informationen siehe:

- [Tunnel-Übersichtsseite](/docs/overview/tunnel-routing)
- [Tunnel-Spezifikation](/docs/specs/tunnel-implementation)
- [Tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation)
- [Tunnel-Design-Diskussion](/docs/discussions/tunnel)
- [Peer-Auswahl](/docs/overview/peer-selection)

## Überprüfung

Obwohl uns keine veröffentlichte Forschung zu den Vorteilen unidirektionaler tunnel bekannt ist, scheinen sie es schwieriger zu machen, ein Anfrage-/Antwort-Muster zu erkennen, was bei einem bidirektionalen tunnel durchaus möglich ist. Mehrere Anwendungen und Protokolle, insbesondere HTTP, übertragen Daten auf diese Weise. Wenn der Datenverkehr denselben Weg zu seinem Ziel und zurück nimmt, könnte es für einen Angreifer, der nur über Timing- und Datenverkehrsvolumen-Daten verfügt, einfacher werden, den Pfad eines tunnel zu erschließen. Dass die Antwort über einen anderen Pfad zurückkommt, macht es wohl schwieriger.

Bei der Auseinandersetzung mit einem internen Angreifer oder den meisten externen Angreifern setzen I2P's unidirektionale tunnel nur halb so viele Verkehrsdaten der Gefährdung aus, wie bei bidirektionalen Schaltkreisen durch die bloße Betrachtung der Datenströme selbst preisgegeben würden - eine HTTP-Anfrage und -Antwort würde in Tor denselben Pfad verfolgen, während in I2P die Pakete, aus denen die Anfrage besteht, über einen oder mehrere ausgehende tunnel hinausgehen und die Pakete, aus denen die Antwort besteht, über einen oder mehrere verschiedene eingehende tunnel zurückkommen würden.

Die Strategie, zwei separate Tunnel für eingehende und ausgehende Kommunikation zu verwenden, ist nicht die einzige verfügbare Technik und hat Auswirkungen auf die Anonymität. Auf der positiven Seite verringert die Verwendung separater Tunnel die Verkehrsdaten, die den Teilnehmern eines Tunnels zur Analyse zur Verfügung stehen - beispielsweise würden Peers in einem ausgehenden Tunnel von einem Webbrowser nur den Verkehr einer HTTP GET-Anfrage sehen, während die Peers in einem eingehenden Tunnel die über den Tunnel übertragene Nutzlast sehen würden. Bei bidirektionalen Tunneln hätten alle Teilnehmer Zugang zu der Tatsache, dass z.B. 1KB in eine Richtung gesendet wurden, dann 100KB in die andere. Auf der negativen Seite bedeutet die Verwendung unidirektionaler Tunnel, dass es zwei Gruppen von Peers gibt, die profiliert und berücksichtigt werden müssen, und zusätzliche Vorsicht ist geboten, um der erhöhten Geschwindigkeit von Vorgänger-Angriffen zu begegnen. Der tunnel-Pooling- und -Aufbauprozess (Peer-Auswahl- und Anordnungsstrategien) sollte die Sorgen bezüglich des Vorgänger-Angriffs minimieren.

## Anonymität

Ein [Papier von Hermann und Grothoff](http://grothoff.org/christian/i2p.pdf) erklärte, dass I2Ps unidirektionale tunnel "eine schlechte Designentscheidung zu sein scheinen".

Der Hauptpunkt des Papers ist, dass Deanonymisierungen bei unidirektionalen tunnels länger dauern, was ein Vorteil ist, aber dass ein Angreifer im unidirektionalen Fall sicherer sein kann. Daher behauptet das Paper, dass es überhaupt kein Vorteil ist, sondern ein Nachteil, zumindest bei langlebigen I2P Sites.

Diese Schlussfolgerung wird von dem Paper nicht vollständig unterstützt. Unidirektionale tunnels mildern eindeutig andere Angriffe ab und es ist nicht klar, wie das Risiko des im Paper beschriebenen Angriffs gegen Angriffe auf eine bidirektionale tunnel-Architektur abgewogen werden soll.

Diese Schlussfolgerung basiert auf einer willkürlichen Gewichtung (Kompromiss) zwischen Sicherheit und Zeit, die möglicherweise nicht in allen Fällen anwendbar ist. Beispielsweise könnte jemand eine Liste möglicher IPs erstellen und dann Vorladungen für jede einzelne ausstellen. Oder der Angreifer könnte jede einzelne per DDoS angreifen und durch einen einfachen Intersection-Angriff feststellen, ob die I2P Site ausfällt oder verlangsamt wird. Daher könnte "nah dran" gut genug sein, oder Zeit könnte wichtiger sein.

Die Schlussfolgerung basiert auf einer spezifischen Gewichtung der Bedeutung von Gewissheit gegenüber Zeit, und diese Gewichtung könnte falsch sein und ist definitiv diskutabel, insbesondere in einer realen Welt mit Vorladungen, Durchsuchungsbefehlen und anderen verfügbaren Methoden für eine endgültige Bestätigung.

Eine vollständige Analyse der Kompromisse zwischen unidirektionalen und bidirektionalen Tunneln liegt eindeutig außerhalb des Umfangs der Arbeit und wurde anderswo nicht durchgeführt. Zum Beispiel: Wie verhält sich dieser Angriff im Vergleich zu den zahlreichen möglichen Timing-Angriffen, die über Onion-Router-Netzwerke veröffentlicht wurden? Offensichtlich haben die Autoren diese Analyse nicht durchgeführt, falls es überhaupt möglich ist, sie effektiv durchzuführen.

Tor verwendet bidirektionale tunnel und hatte viel akademische Überprüfung. I2P verwendet unidirektionale tunnel und hatte sehr wenig Überprüfung. Bedeutet das Fehlen einer Forschungsarbeit, die unidirektionale tunnel verteidigt, dass es eine schlechte Designentscheidung ist, oder nur, dass es mehr Studien benötigt? Timing-Angriffe und verteilte Angriffe sind sowohl in I2P als auch in Tor schwer zu verteidigen. Die Designabsicht (siehe Referenzen oben) war, dass unidirektionale tunnel widerstandsfähiger gegen Timing-Angriffe sind. Jedoch präsentiert das Paper einen etwas anderen Typ von Timing-Angriff. Ist dieser Angriff, so innovativ er auch ist, ausreichend, um I2Ps tunnel-Architektur (und damit I2P als Ganzes) als "schlechtes Design" zu bezeichnen und damit implizit als klar unterlegen gegenüber Tor, oder ist es nur eine Designalternative, die eindeutig weitere Untersuchung und Analyse benötigt? Es gibt mehrere andere Gründe, I2P derzeit als unterlegen gegenüber Tor und anderen Projekten zu betrachten (kleine Netzwerkgröße, mangelnde Finanzierung, mangelnde Überprüfung), aber sind unidirektionale tunnel wirklich ein Grund?

Zusammenfassend ist "schlechte Designentscheidung" offenbar (da das Paper bidirektionale tunnel nicht als "schlecht" bezeichnet) eine Kurzform für "unidirektionale tunnel sind unzweifelhaft unterlegen gegenüber bidirektionalen tunneln", jedoch wird diese Schlussfolgerung nicht durch das Paper unterstützt.
