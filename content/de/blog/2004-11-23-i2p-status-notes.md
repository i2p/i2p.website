---
title: "I2P-Statushinweise für 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Wöchentliches I2P-Status-Update über die Netzwerkwiederherstellung, den Testfortschritt der Streaming-Bibliothek, Pläne für die kommende Version 0.4.2 und Verbesserungen am Adressbuch"
categories: ["status"]
---

Hi zusammen, Zeit für ein Status-Update

## Inhaltsverzeichnis:

1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Netzstatus

Nach der 2–3-tägigen Phase in der letzten Woche, in der das Netzwerk ziemlich überlastet war, ist das Netzwerk wieder auf Kurs (wahrscheinlich, weil wir den Stresstest des Bittorrent-Ports eingestellt haben ;). Seitdem war das Netzwerk ziemlich zuverlässig - wir haben ein paar routers, die seit 30–40+ Tagen durchgehend laufen, aber IRC-Verbindungen hatten trotzdem ihre gelegentlichen Aussetzer. Andererseits...

## 2) Streaming-Bibliothek

Seit etwa einer Woche führen wir im Netzwerk deutlich mehr Live-Tests der Streaming-Bibliothek durch, und die Ergebnisse sehen ziemlich gut aus. Duck hat damit einen tunnel eingerichtet, den Leute nutzen konnten, um auf seinen IRC-Server zuzugreifen, und im Laufe einiger Tage hatte ich nur zwei unnötige Verbindungsabbrüche (was uns dabei half, einige Bugs aufzuspüren). Wir hatten außerdem eine i2ptunnel-Instanz, die auf einen squid outproxy zeigte, den Leute ausprobiert haben, und sowohl Durchsatz, Latenz als auch Zuverlässigkeit sind im Vergleich zur alten Bibliothek, die wir parallel betrieben haben, deutlich verbessert.

Alles in allem scheint die Streaming-Bibliothek in einem ausreichend guten Zustand für eine erste Veröffentlichung zu sein. Es gibt noch ein paar Dinge, die noch nicht fertig sind, aber sie ist eine deutliche Verbesserung gegenüber der alten Bibliothek, und wir müssen Ihnen ja einen Grund geben, später zu upgraden, oder? ;)

Eigentlich, nur um dich ein wenig zu necken (oder vielleicht zu inspirieren, dir einige Lösungen einfallen zu lassen), sind die Hauptdinge, die ich für die Streaming-Bibliothek auf uns zukommen sehe: - einige Algorithmen, um Überlastungs- und RTT-Informationen (Round-Trip-Zeit) zwischen Streams zu teilen (pro target destination (Zieladresse)? pro source destination? für alle lokalen destinations?) - weitere Optimierungen für interaktive Streams (der Schwerpunkt der aktuellen Implementierung liegt größtenteils auf Bulk-Streams) - explizitere Nutzung der neuen Funktionen der Streaming-Bibliothek in I2PTunnel, wodurch der per-tunnel Overhead reduziert wird. - Bandbreitenbegrenzung auf Client-Ebene (in eine oder beide Richtungen auf einem Stream oder möglicherweise gemeinsam über mehrere Streams). Das käme natürlich zusätzlich zur allgemeinen Bandbreitenbegrenzung durch den router. - verschiedene Steuerungen für destinations, um zu drosseln, wie viele Streams sie annehmen oder erstellen (wir haben etwas grundlegenden Code, aber größtenteils deaktiviert) - Zugriffskontrolllisten (nur Streams zu oder von bestimmten anderen bekannten destinations zulassen) - Web-Steuerung und Überwachung des Zustands der verschiedenen Streams sowie die Möglichkeit, sie explizit zu schließen oder zu drosseln

Euch fallen sicher auch noch andere Dinge ein, aber das ist nur eine kurze Liste von Dingen, die ich gern in der Streaming-Lib sehen würde, für die ich aber das Release 0.4.2 nicht verzögern werde. Wenn sich jemand für eines davon interessiert, bitte, gebt mir Bescheid!

## 3) 0.4.2

Also, wenn die Streaming-Bibliothek in gutem Zustand ist, wann gibt es das Release? Der aktuelle Plan ist, es bis Ende der Woche rauszubringen, vielleicht sogar schon morgen. Es gibt noch ein paar andere Dinge, die ich zuerst klären möchte, und die müssen natürlich getestet werden, bla bla bla.

Die große Änderung im Release 0.4.2 wird natürlich die neue Streaming-Bibliothek sein. Aus API-Sicht ist sie mit der alten Bibliothek identisch - I2PTunnel und SAM-Streams verwenden sie automatisch, aber auf Paketebene ist sie *nicht* abwärtskompatibel. Das bringt uns in ein interessantes Dilemma - es gibt nichts innerhalb von I2P, das uns dazu verpflichtet, 0.4.2 zu einem Pflicht-Upgrade zu machen, allerdings werden Personen, die nicht aktualisieren, I2PTunnel nicht nutzen können - keine eepsites(I2P Sites), kein IRC, kein Outproxy, keine E-Mail. Ich möchte unsere langjährigen Nutzer nicht verprellen, indem ich sie zu einem Upgrade zwinge, aber ich möchte sie auch nicht dadurch verprellen, dass alles Nützliche kaputtgeht ;)

Ich bin offen dafür, mich in die eine oder andere Richtung überzeugen zu lassen – es wäre relativ einfach, eine einzelne Codezeile zu ändern, sodass das 0.4.2-Release nicht mehr mit den älteren Releases kommuniziert, oder wir lassen es einfach so und die Leute aktualisieren dann, wenn sie auf die Website oder ins Forum gehen, um darüber herumzumeckern, dass alles kaputt ist. Was meint ihr?

## 4) AddressBook.py 0.3.1

Ragnarok hat eine neue Patch-Version für seine Adressbuch-App herausgebracht - siehe `http://ragnarok.i2p/` für weitere Informationen (oder vielleicht kann er uns im Meeting ein Update geben?)

## 5) ???

Ich weiß, dass noch viel mehr los ist – beim BitTorrent-Port, susimail, slackers neuem Hosting-Dienst, unter anderem. Hat sonst noch jemand etwas anzusprechen? Wenn ja, schaut in ~30m beim Meeting in #i2p auf den üblichen IRC-Servern vorbei!

=jr
