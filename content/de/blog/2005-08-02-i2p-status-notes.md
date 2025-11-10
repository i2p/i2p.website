---
title: "I2P Statusnotizen für 2005-08-02"
date: 2005-08-02
author: "jr"
description: "Verspätetes Update zum Status der Veröffentlichung 0.6, dem PeerTest-System, SSU-Introductions, Fehlerbehebungen an der I2PTunnel-Weboberfläche und mnet über I2P"
categories: ["status"]
---

Hallo zusammen, heute gibt es verspätete Notizen,

* Index:

1) 0.6 Status 2) PeerTest 3) SSU introductions 4) I2PTunnel Weboberfläche 5) mnet über i2p 6) ???

* 1) 0.6 status

Wie ihr alle gesehen habt, haben wir vor ein paar Tagen die Version 0.6 herausgebracht, und im Großen und Ganzen läuft es ziemlich gut. Einige der Transport-Verbesserungen seit 0.5.* haben Probleme mit der Implementierung der netDb offengelegt, aber Fehlerbehebungen für vieles davon befinden sich jetzt im Test (als Build 0.6-1) und werden in Kürze als 0.6.0.1 ausgerollt. Wir sind außerdem auf einige Probleme mit unterschiedlichen NAT- und Firewall-Konfigurationen gestoßen, ebenso wie auf MTU-Probleme bei einigen Nutzern - Probleme, die im kleineren Testnetz aufgrund der geringeren Zahl an Testern nicht auftraten. Für die schlimmsten Fälle wurden Workarounds hinzugefügt, aber eine langfristige Lösung steht bald bevor - Peer-Tests.

* 2) PeerTest

Mit 0.6.1 werden wir ein neues System einführen, um gemeinsam die öffentlichen IP-Adressen und Ports zu testen und zu konfigurieren. Dies ist in den Kern des SSU-Protokolls integriert und wird abwärtskompatibel sein. Im Wesentlichen ermöglicht es, dass Alice Bob fragt, wie ihre öffentliche IP-Adresse und Portnummer lautet, und Bob wiederum Charlie dazu veranlasst, ihre korrekte Konfiguration zu bestätigen oder herauszufinden, welche Einschränkung die ordnungsgemäße Funktion verhindert. Die Technik ist im Netz nichts Neues, ist aber eine neue Ergänzung der i2p-Codebasis und sollte die meisten gängigen Konfigurationsfehler beseitigen.

* 3) SSU introductions

Wie in der SSU-Protokollspezifikation beschrieben, wird es Funktionalität geben, die es Teilnehmern hinter Firewalls und NATs ermöglicht, vollständig am Netzwerk teilzunehmen, selbst wenn sie ansonsten keine unaufgeforderten UDP-Nachrichten empfangen könnten. Sie wird nicht in allen potenziellen Situationen funktionieren, aber die meisten abdecken. Es gibt Ähnlichkeiten zwischen den in der SSU-Spezifikation beschriebenen Nachrichten und den für den PeerTest notwendigen Nachrichten, sodass wir vielleicht, wenn die Spezifikation um diese Nachrichten ergänzt wird, die Introductions (Einführungsnachrichten) an die PeerTest-Nachrichten anhängen können. Auf jeden Fall werden wir diese Introductions in 0.6.2 bereitstellen, und auch das wird abwärtskompatibel sein.

* 4) I2PTunnel web interface

Einige Leute haben verschiedene Unstimmigkeiten in der I2PTunnel-Weboberfläche bemerkt und entsprechende Berichte eingereicht, und smeghead hat mit der Umsetzung der notwendigen Fehlerbehebungen begonnen – vielleicht kann er diese Aktualisierungen näher erläutern und einen voraussichtlichen Zeitrahmen dafür nennen?

* 5) mnet over i2p

Auch wenn ich nicht im Channel war, als die Diskussionen stattfanden, geht aus den Logs hervor, dass icepick einige Hacks vorgenommen hat, um mnet auf I2P zum Laufen zu bringen – wodurch der verteilte Datenspeicher von mnet eine widerstandsfähige Inhaltsveröffentlichung mit anonymem Betrieb ermöglichen würde. Ich weiß nicht allzu viel über den Fortschritt in dieser Hinsicht, aber es klingt so, als mache icepick gute Fortschritte bei der Anbindung an I2P über SAM und Twisted; vielleicht kann uns icepick dazu noch mehr erzählen?

* 6) ???

Okay, es ist noch viel mehr los als oben beschrieben, aber ich bin schon spät dran, also sollte ich wohl aufhören zu tippen und diese Nachricht rausschicken. Ich kann heute Abend für eine Weile online sein, falls jemand da ist, könnten wir uns so gegen 21:30 Uhr treffen (wann immer ihr das hier bekommt ;) in #i2p auf den üblichen irc-Servern {irc.duck.i2p, irc.postman.i2p, irc.freenode.net, irc.metropipe.net}.

Vielen Dank für Ihre Geduld und Ihre Hilfe dabei, die Dinge voranzubringen!

=jr
