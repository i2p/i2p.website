---
title: "I2P-Statushinweise für 2005-03-22"
date: 2005-03-22
author: "jr"
description: "Wöchentliche Notizen zum Entwicklungsstand von I2P zu Release 0.5.0.3, zur Implementierung der Nachrichtenbündelung für tunnel und zu automatischen Update-Tools"
categories: ["status"]
---

Hi zusammen, kurzes Status-Update

* Index

1) 0.5.0.3 2) Batching (Bündelung) 3) Aktualisierung 4) ???

* 0.5.0.3

Das neue Release ist draußen, und die meisten von euch haben ziemlich schnell aktualisiert – danke! Es gab einige Fehlerbehebungen für verschiedene Probleme, aber nichts Revolutionäres – die größte Änderung war, Nutzer der Versionen 0.5 und 0.5.0.1 vom Netz auszuschließen. Seitdem verfolge ich das Verhalten des Netzes und analysiere, was passiert, und obwohl es einige Verbesserungen gab, gibt es immer noch Dinge, die bereinigt werden müssen.

In den nächsten ein bis zwei Tagen wird es ein neues Release geben, mit einer Fehlerbehebung für ein Problem, auf das bisher noch niemand gestoßen ist, das aber den neuen Batching-Code funktionsunfähig macht. Außerdem wird es einige Tools geben, um den Aktualisierungsprozess entsprechend den Einstellungen der Nutzer zu automatisieren, sowie weitere kleinere Anpassungen.

* batching

Wie ich in meinem Blog erwähnt habe, gibt es Spielraum, die benötigte Bandbreite und die Anzahl der Nachrichten im Netz drastisch zu reduzieren, indem wir eine sehr einfache Bündelung (Batching) von tunnel-Nachrichten vornehmen - anstatt jede I2NP-Nachricht, unabhängig von ihrer Größe, in eine eigene tunnel-Nachricht zu packen, können wir durch das Einfügen einer kurzen Verzögerung bis zu 15 oder mehr innerhalb einer einzigen tunnel-Nachricht bündeln. Die größten Vorteile ergeben sich bei Diensten, die kleine Nachrichten verwenden (z. B. IRC), während große Dateiübertragungen davon kaum betroffen sind. Der Code für das Batching wurde implementiert und getestet, aber leider gibt es im Live-Netz einen Bug, der dazu führen würde, dass innerhalb einer tunnel-Nachricht alle I2NP-Nachrichten bis auf die erste verloren gehen. Deshalb werden wir eine Zwischenveröffentlichung mit dieser Fehlerbehebung herausbringen, gefolgt von der Batching-Veröffentlichung etwa eine Woche später.

* updating

In dieser Zwischenversion werden wir einen Teil des oft diskutierten 'autoupdate'-Codes ausliefern. Wir haben die Werkzeuge, um periodisch nach authentischen Update-Ankündigungen zu prüfen, das Update wahlweise anonym oder nicht anonym herunterzuladen und es dann entweder zu installieren oder einfach einen Hinweis auf der router console anzuzeigen, der Ihnen mitteilt, dass es bereit ist und auf die Installation wartet. Das Update selbst wird nun smeghead's neues signiertes Update-Format verwenden, das im Wesentlichen aus dem Update plus einer DSA-Signatur besteht. Die zur Überprüfung dieser Signatur verwendeten Schlüssel werden mit I2P gebündelt und sind zudem auf der router console konfigurierbar.

Das Standardverhalten besteht darin, einfach regelmäßig nach Update-Ankündigungen zu prüfen, aber nicht darauf zu reagieren - stattdessen wird auf der Router-Konsole lediglich eine Ein-Klick-Funktion "Update now" angezeigt. Es wird viele weitere Szenarien für unterschiedliche Nutzerbedürfnisse geben, aber hoffentlich werden sie alle über eine neue Konfigurationsseite abgedeckt.

* ???

Ich fühle mich etwas angeschlagen, daher geht das Obige nicht wirklich auf alle Details dazu ein, was gerade los ist.  Kommt einfach beim Meeting vorbei und füllt die Lücken :)

Oh, nur am Rande: Ich werde in den nächsten ein bis zwei Tagen auch einen neuen PGP-Schlüssel für mich herausgeben (da dieser bald abläuft...), also haltet die Augen offen.

=jr
