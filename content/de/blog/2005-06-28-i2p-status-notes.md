---
title: "I2P-Statusnotizen für 2005-06-28"
date: 2005-06-28
author: "jr"
description: "Wöchentliches Update zu den Bereitstellungsplänen für den SSU-Transport, zum Abschluss der Prämie für Unit-Tests und zu Lizenzierungsüberlegungen sowie zum Status von Kaffe Java"
categories: ["status"]
---

Hi zusammen, es ist wieder Zeit für das wöchentliche Update

* Index

1) SSU-Status 2) Unit-Test-Status 3) Kaffe-Status 4) ???

* 1) SSU status

Es gab einige weitere Fortschritte am SSU-Transport, und meine derzeitige Einschätzung ist, dass wir es nach einigen weiteren Tests im Live-Netz als 0.6 ohne große Verzögerung ausrollen können. Die erste SSU-Version wird keine Unterstützung für Personen enthalten, die keine Portfreigabe in ihrer Firewall vornehmen oder ihr NAT anpassen können, aber das wird in 0.6.1 ausgerollt. Nachdem 0.6.1 veröffentlicht ist, getestet wurde und richtig rockt (aka 0.6.1.42), gehen wir zu 1.0 über.

Meine persönliche Neigung geht dahin, den TCP-Transport komplett zu streichen, sobald der SSU-Transport eingeführt wird, damit die Leute nicht beide aktiviert haben müssen (also sowohl TCP- als auch UDP-Ports weiterleiten) und damit die Entwickler keinen unnötigen Code pflegen müssen. Hat jemand dazu starke Meinungen?

* 2) Unit test status

Wie letzte Woche erwähnt, hat sich Comwiz gemeldet, um die erste Phase der Prämie für Unit-Tests zu beanspruchen (yay Comwiz!  danke auch an duck & zab für die Finanzierung der Prämie!). Der Code wurde in CVS eingecheckt und, abhängig von deinem lokalen Setup, kannst du die junit- und clover-Berichte erzeugen, indem du in das Verzeichnis i2p/core/java gehst und "ant test junit.report" ausführst (etwa eine Stunde warten...) und i2p/reports/core/html/junit/index.html ansiehst. Andererseits kannst du "ant useclover test junit.report clover.report" ausführen und i2p/reports/core/html/clover/index.html ansehen.

Der Nachteil beider Testreihen hängt mit diesem törichten Konzept zusammen, das die herrschende Klasse „Urheberrecht“ nennt. clover ist ein kommerzielles Produkt, auch wenn die Leute bei cenqua dessen kostenlose Nutzung durch Open-Source-Entwickler erlauben (und sie haben sich freundlicherweise bereit erklärt, uns eine Lizenz zu erteilen). Um die clover-Berichte zu erzeugen, muss clover lokal installiert sein - ich habe clover.jar in ~/.ant/lib/, neben meiner Lizenzdatei. Die meisten Leute werden clover nicht benötigen, und da wir die Berichte im Web veröffentlichen werden, geht durch die Nichtinstallation keine Funktionalität verloren.

Auf der anderen Seite bekommen wir die Schattenseite des Urheberrechts zu spüren, wenn wir das Unit-Test-Framework selbst berücksichtigen - junit steht unter der IBM Common Public License 1.0, die laut FSF [1] nicht GPL-kompatibel ist. Zwar haben wir selbst keinen GPL-Code (zumindest nicht im core oder dem router), aber mit Blick auf unsere Lizenzrichtlinie [2] ist es unser Ziel, die konkreten Bedingungen unserer Lizenzierung so zu gestalten, dass möglichst viele Menschen das, was entsteht, nutzen können, denn Anonymität liebt Gesellschaft.

[1] http://www.fsf.org/licensing/licenses/index_html#GPLIncompatibleLicenses [2] http://www.i2p.net/licenses

Da einige Leute aus unerfindlichen Gründen Software unter der GPL veröffentlichen, ergibt es Sinn, dass wir uns darum bemühen, ihnen die Nutzung von I2P ohne Einschränkungen zu ermöglichen. Das bedeutet zumindest, dass wir nicht zulassen können, dass die von uns bereitgestellte Funktionalität von CPL-lizenziertem Code abhängt (z. B. junit.framework.*). Ich würde das gern auch auf die Unit-Tests ausdehnen, aber JUnit scheint die Lingua franca der Test-Frameworks zu sein (und ich halte es angesichts unserer Ressourcen für alles andere als vernünftig, zu sagen: "hey, lasst uns unser eigenes Public-Domain-Unit-Test-Framework bauen!").

Vor diesem Hintergrund denke ich Folgendes. Wir werden junit.jar in CVS einchecken und es verwenden, wenn die Unit-Tests ausgeführt werden, aber die Unit-Tests selbst werden nicht in i2p.jar oder router.jar eingebaut und nicht mit Veröffentlichungen ausgeliefert. Gegebenenfalls könnten wir ein zusätzliches Set von JARs bereitstellen (i2p-test.jar und router-test.jar), aber diese wären nicht für GPL-lizenzierte Anwendungen nutzbar (da sie von junit abhängen).

=jr
