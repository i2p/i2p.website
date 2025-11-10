---
title: "I2P Statusnotizen für 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Wöchentliches I2P-Statusupdate zur Performance des Releases 0.3.4, zur Entwicklung der neuen Webkonsole und zu verschiedenen Anwendungsprojekten"
categories: ["status"]
---

Hi zusammen, bringen wir dieses Status-Update schnell hinter uns

## Stichwortverzeichnis:

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) 0.3.4 Status

Mit der 0.3.4-Veröffentlichung letzte Woche funktioniert das neue Netz ziemlich gut - irc-Verbindungen halten jeweils mehrere Stunden am Stück und das Abrufen von eepsite(I2P Site) scheint ziemlich zuverlässig zu sein. Der Durchsatz ist insgesamt noch niedrig, wenn auch leicht verbessert (früher sah ich konstant 4-5KBps, jetzt sehe ich konstant 5-8KBps). oOo hat ein Paar Skripte veröffentlicht, die die irc-Aktivität zusammenfassen, einschließlich der Round-Trip-Zeit für Nachrichten und der Verbindungslebensdauer (basierend auf hypercubus' bogobot, der kürzlich in CVS committed wurde)

## 2) Vorgesehen für 0.3.4.1

Wie jeder mit 0.3.4 bemerkt hat, war ich *cough* ein wenig zu ausführlich in meinem Logging, was in cvs behoben wurde. Außerdem habe ich, nachdem ich einige Werkzeuge geschrieben hatte, um die ministreaming-Bibliothek zu belasten, eine 'choke' (Begrenzung) hinzugefügt, damit sie nicht Unmengen an Speicher verschlingt (sie blockiert, wenn versucht wird, mehr als 128KB Daten in den Puffer eines Streams zu schreiben, sodass beim Senden einer großen Datei dein router nicht die gesamte Datei in den Speicher lädt). Ich denke, das wird bei den OutOfMemory-Problemen helfen, die die Leute beobachtet haben, aber ich werde noch zusätzlichen Überwachungs- / Debugging-Code hinzufügen, um das zu verifizieren.

## 3) Neue Webkonsole / I2PTunnel-Controller

Zusätzlich zu den oben genannten Änderungen für 0.3.4.1 haben wir die erste Version der neuen Konsole für den router fertiggestellt und für erste Tests bereit. Aus mehreren Gründen werden wir sie allerdings noch nicht als Teil der Standardinstallation mitliefern, daher wird es Anleitungen geben, wie man sie zum Laufen bringt, wenn die 0.3.4.1-Revision in ein paar Tagen herauskommt. Wie ihr gesehen habt, bin ich wirklich schlecht im Webdesign, und wie viele von euch schon seit Längerem sagen, sollte ich aufhören, an der Anwendungsschicht herumzuspielen, und mich darauf konzentrieren, den Kern und den router absolut stabil zu bekommen. Während die neue Konsole bereits vieles von der gewünschten Funktionalität bietet (den router vollständig über einige einfache Webseiten konfigurieren, eine schnelle und gut lesbare Zusammenfassung des Zustands des router anbieten, die Möglichkeit bereitstellen, verschiedene I2PTunnel-Instanzen zu erstellen / zu bearbeiten / zu stoppen / zu starten), brauche ich wirklich Hilfe von Leuten, die sich mit dem Webbereich gut auskennen.

In der neuen Webkonsole kommen Standard-JSP, CSS und einfache JavaBeans zum Einsatz, die den router / I2PTunnels nach Daten abfragen und Anfragen verarbeiten. Sie sind alle in zwei .war-Dateien gebündelt und in einem integrierten Jetty-Webserver bereitgestellt (der über die clientApp.*-Zeilen des router gestartet werden muss). Die Haupt-JSPs und -Beans der router-Konsole sind technisch ziemlich solide, allerdings sind die neuen JSPs und Beans, die ich zur Verwaltung von I2PTunnel-Instanzen erstellt habe, eher etwas zusammengeflickt.

## 4) 0.4-Sachen

Neben der neuen Weboberfläche wird die Version 0.4 auch hypercubus’ neues Installationsprogramm enthalten, das wir allerdings noch nicht wirklich integriert haben. Wir müssen außerdem noch einige groß angelegte Simulationen durchführen (insbesondere den Umgang mit asymmetrischen Anwendungen wie IRC und outproxies (Ausgangs-Proxys ins reguläre Internet)). Zusätzlich gibt es einige Aktualisierungen, die ich bei kaffe/classpath durchbringen muss, damit wir die neue Web-Infrastruktur auf Open-Source-JVMs zum Laufen bekommen. Außerdem muss ich noch weitere Dokumentation zusammenstellen (eine zur Skalierbarkeit und eine weitere, die die Sicherheit/Anonymität in einigen gängigen Szenarien analysiert). Wir möchten auch alle Verbesserungen, die Sie vorschlagen, in die neue Web-Konsole integrieren.

Ach, und behebe auch gleich alle Bugs, die du mit aufspürst :)

## 5) Andere Entwicklungsaktivitäten

Auch wenn beim grundlegenden I2P-System bereits viel Fortschritt erzielt wurde, ist das nur die halbe Geschichte - viele von euch leisten großartige Arbeit an Anwendungen und Bibliotheken, um I2P nützlich zu machen. Ich habe im Chat-Verlauf einige Fragen dazu gesehen, wer woran arbeitet. Um diese Informationen zugänglich zu machen, folgt hier alles, was ich dazu weiß (wenn ihr an etwas arbeitet, das nicht aufgeführt ist und ihr es teilen möchtet, wenn ich mich irre oder wenn ihr euren Fortschritt diskutieren wollt, meldet euch bitte!).

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

Das ist alles, was mir im Moment einfällt - kommt später heute Abend beim Treffen vorbei, um über Kram zu quatschen. Wie immer um 21 Uhr GMT auf #i2p auf den üblichen Servern.

=jr
