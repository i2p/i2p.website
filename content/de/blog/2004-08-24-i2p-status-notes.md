---
title: "I2P-Statusnotizen für 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Wöchentliches I2P-Status-Update mit Informationen zum Release 0.3.4.3, zu neuen Funktionen der router-Konsole, zum Fortschritt bei 0.4 sowie zu verschiedenen Verbesserungen"
categories: ["status"]
---

Hallo zusammen, heute gibt es viele Updates

## Stichwortverzeichnis

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 Status

Die Version 0.3.4.3 ist letzten Freitag erschienen und seitdem läuft es ziemlich gut. Es gab einige Probleme mit neu eingeführtem tunnel testing und Peer-Auswahl-Code, aber nach einigen Anpassungen seit der Veröffentlichung ist es ziemlich solide. Ich weiß nicht, ob der IRC-Server schon auf der neuen Revision läuft, daher müssen wir uns im Allgemeinen auf Tests mit eepsites(I2P Sites) und den HTTP-Outproxies (squid.i2p und www1.squid.i2p) verlassen. Große (>5MB) Dateiübertragungen in der Version 0.3.4.3 sind immer noch nicht zuverlässig genug, aber in meinen Tests haben die seitdem vorgenommenen Änderungen die Situation weiter verbessert.

Auch das Netzwerk wächst – wir haben heute früher am Tag 45 gleichzeitige Benutzer erreicht und liegen seit einigen Tagen konstant im Bereich von 38–44 Benutzern (w00t)! Das ist derzeit eine gesunde Zahl, und ich überwache die gesamte Netzwerkaktivität, um nach Gefahren Ausschau zu halten. Beim Wechsel auf die Version 0.4 möchten wir die Benutzerbasis schrittweise auf etwa die Marke von 100 router erhöhen und noch etwas mehr testen, bevor wir weiter wachsen. Zumindest ist das mein Ziel aus Entwicklersicht.

### 1.1) timestamper

Eines der richtig großartigen Dinge, die sich mit dem Release 0.3.4.3 geändert haben und das ich völlig vergessen habe zu erwähnen, war ein Update des SNTP-Codes. Dank der Großzügigkeit von Adam Buckley, der zugestimmt hat, seinen SNTP-Code unter der BSD-Lizenz zu veröffentlichen, haben wir die alte Timestamper app in das core I2P SDK übernommen und vollständig mit unserer Uhr integriert. Das bedeutet drei Dinge: 1. Sie können die timestamper.jar löschen (der Code ist jetzt in i2p.jar) 2. Sie können die zugehörigen clientApp-Zeilen aus Ihrer config entfernen 3. Sie können Ihre config aktualisieren, um die neuen Zeitsynchronisierungsoptionen zu verwenden

Die neuen Optionen in der router.config sind einfach, und die Standardwerte sollten gut genug sein (das trifft besonders zu, da die meisten von Ihnen sie unabsichtlich verwenden :)

Zum Festlegen der Liste der abzufragenden SNTP-Server:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Zum Deaktivieren der Zeitsynchronisierung (nur wenn Sie ein NTP-Guru sind und wissen, dass die Uhr Ihres Betriebssystems *immer* richtig geht - das Ausführen von "windows time" ist NICHT ausreichend):

```
time.disabled=true
```
Sie brauchen kein „Timestamper-Passwort“ mehr, da alles direkt im Code integriert ist (ach, die Freuden von BSD vs GPL :)

### 1.2) new router console authentication

Das ist nur relevant für diejenigen unter Ihnen, die die neue router-Konsole betreiben, aber wenn Sie sie auf einer öffentlichen Schnittstelle lauschen lassen, möchten Sie vielleicht die integrierte HTTP Basic-Authentifizierung nutzen. Ja, die HTTP Basic-Authentifizierung ist lächerlich schwach - sie schützt nicht vor jemandem, der Ihr Netzwerk mitschneidet oder sich per Brute-Force Zutritt verschafft, aber sie hält den Gelegenheitsschnüffler fern. Wie dem auch sei, um sie zu verwenden, fügen Sie einfach die Zeile hinzu

```
consolePassword=blah
```
in Ihre router.config. Sie müssen den router leider neu starten, da dieser Parameter von Jetty nur einmal (beim Start) eingelesen wird.

## 2) 0.4 status

Wir machen große Fortschritte beim Release 0.4 und hoffen, in der nächsten Woche ein paar Vorabversionen herauszubringen. Wir feilen jedoch noch an einigen Details, daher haben wir den Upgrade-Prozess noch nicht abschließend ausgearbeitet. Das Release wird abwärtskompatibel sein, also sollte das Update nicht allzu problematisch sein. Haltet die Ohren offen, dann wisst ihr, wann es so weit ist.

### 1.1) Zeitstempelgenerator

Hypercubus macht große Fortschritte bei der Integration des Installationsprogramms, einer Systray-Anwendung (Infobereich der Taskleiste) und von Code zur Dienstverwaltung. Kurz gesagt, werden mit der Version 0.4 alle Windows-Benutzer automatisch ein kleines Systray-Symbol (Iggy!) haben, wobei sie dieses über die Webkonsole deaktivieren (und/oder wieder aktivieren) können. Außerdem werden wir den JavaService wrapper mitliefern, der uns allerlei coole Dinge ermöglicht, etwa I2P beim Systemstart auszuführen (oder auch nicht), bei bestimmten Bedingungen automatisch neu zu starten, bei Bedarf einen harten JVM-Neustart durchzuführen, Stacktraces zu erzeugen und noch allerlei andere Goodies.

### 1.2) neue Authentifizierung der router-Konsole

Eines der großen Updates im Release 0.4 wird eine Überarbeitung des jbigi-Codes sein, die die von Iakin für Freenet vorgenommenen Änderungen zusammenführt sowie Iakins neue native Bibliothek "jcpuid" einbezieht. Die jcpuid-Bibliothek funktioniert nur auf x86-Architekturen und ermittelt in Kombination mit etwas neuem jbigi-Code, welches das 'richtige' jbigi ist, das geladen werden soll. Daher werden wir ein einziges jbigi.jar ausliefern, das alle haben werden, und daraus das 'richtige' für den aktuellen Rechner auswählen. Selbstverständlich können Benutzer weiterhin ihr eigenes natives jbigi bauen und damit das, was jcpuid vorgibt, übersteuern (bauen Sie es einfach und kopieren Sie es in Ihr I2P-Installationsverzeichnis, oder nennen Sie es "jbigi" und legen Sie es in eine .jar-Datei in Ihrem classpath). Aufgrund der Aktualisierungen ist es *nicht* abwärtskompatibel - beim Upgrade müssen Sie entweder Ihr eigenes jbigi neu bauen oder Ihre vorhandene native Bibliothek entfernen (damit der neue jcpuid-Code die richtige auswählen kann).

### 2.3) i2paddresshelper

oOo hat ein wirklich praktisches Hilfsprogramm zusammengestellt, mit dem Leute eepsites (I2P-Seiten) besuchen können, ohne ihre hosts.txt zu aktualisieren. Es ist in CVS eingecheckt und wird im nächsten Release bereitgestellt, aber es könnte sinnvoll sein, Links entsprechend zu aktualisieren (cervantes hat das [i2p] bbcode von forum.i2p aktualisiert, um es mit einem "Try it [i2p]" Link zu unterstützen).

Im Grunde genommen erstellen Sie einfach einen Link zur eepsite(I2P Site) mit einem beliebigen Namen Ihrer Wahl und hängen dann einen speziellen URL-Parameter an, der das Ziel angibt:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Hinter den Kulissen ist es ziemlich sicher - du kannst keine andere Adresse fälschen, und der Name wird nicht dauerhaft in der hosts.txt gespeichert, aber dadurch kannst du Bilder usw., die auf eepsites(I2P-Seiten) verlinkt sind, sehen, was mit dem alten Trick `http://i2p/base64/` nicht möglich wäre. Wenn du "wowthisiscool.i2p" immer verwenden können möchtest, um diese Site zu erreichen, musst du den Eintrag natürlich weiterhin in deine hosts.txt eintragen (bis das MyI2P address book ausgerollt wird ;)

## 3) AMOC vs. restricted routes

Mule hat einige Ideen zusammengetragen und mich gedrängt, manche Dinge zu erklären, und dabei hat er Fortschritte gemacht, mich dazu zu bewegen, die gesamte AMOC-Idee neu zu bewerten. Konkret: Wenn wir eine der Beschränkungen aufgeben, die ich unserer Transportschicht auferlegt habe - wodurch wir Bidirektionalität voraussetzen können -, könnten wir den gesamten AMOC-Transport verwerfen und stattdessen einen grundlegenden Betriebsmodus mit eingeschränkten Routen implementieren (wobei die Grundlagen für weiter fortgeschrittene Techniken mit eingeschränkten Routen, wie vertrauenswürdige Peers und multihop router tunnels, für später bleiben).

Wenn wir diesen Weg gehen, würde das bedeuten, dass Personen hinter Firewalls, NATs usw. ohne Konfigurationsaufwand am Netzwerk teilnehmen könnten, und es würde zugleich einige der Anonymitätseigenschaften von eingeschränkten Routen bieten. Im Gegenzug würde das wahrscheinlich eine umfassende Überarbeitung unserer Roadmap nach sich ziehen, aber wenn wir es sicher umsetzen können, würde es uns eine Menge Zeit sparen und die Änderung wäre es allemal wert.

Wir möchten jedoch nichts überstürzen und müssen die Auswirkungen auf Anonymität und Sicherheit sorgfältig prüfen, bevor wir uns auf diesen Weg festlegen. Das werden wir tun, nachdem 0.4 veröffentlicht ist und reibungslos läuft, es besteht also keine Eile.

## 2) 0.4 Status

Wie man hört, macht aum gute Fortschritte - ich weiß nicht, ob er beim Meeting mit einem Update dabei sein wird, aber er hat uns heute Morgen auf #i2p eine kurze Nachricht hinterlassen:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Juhu.

## 5) pages of note

Ich möchte nur auf zwei neue Ressourcen hinweisen, die sich I2P-Nutzerinnen und -Nutzer vielleicht ansehen möchten - DrWoo hat eine Seite mit einer Vielzahl an Informationen für Personen zusammengestellt, die anonym surfen möchten, und Luckypunk hat ein Howto veröffentlicht, in dem er seine Erfahrungen mit einigen JVMs unter FreeBSD beschreibt. Hypercubus hat außerdem die Dokumentation zum Testen der noch nicht veröffentlichten Service- & Systray-Integration bereitgestellt.

## 6) ???

Ok, das ist alles, was ich im Moment zu sagen habe - schaut heute Abend um 21 Uhr GMT beim Meeting vorbei, wenn ihr noch etwas ansprechen möchtet.

=jr
