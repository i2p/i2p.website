---
title: "I2P Statusnotizen für 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Wöchentliches I2P-Status-Update über die Verschlechterung der Netzwerkleistung, die Release-Planung für 0.3.5, den Dokumentationsbedarf und die Fortschritte bei Stasher DHT"
categories: ["status"]
---

Na, Jungs und Mädels, es ist wieder Dienstag!

## Stichwortverzeichnis:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Nun, wie ihr alle bemerkt habt, ist zwar die Anzahl der Nutzer im Netzwerk ziemlich konstant geblieben, aber die Leistung hat sich in den letzten Tagen deutlich verschlechtert. Die Ursache dafür war eine Reihe von Bugs in der Peer-Auswahl und im Code für die Nachrichtenübermittlung, die sichtbar wurden, als es letzte Woche einen kleineren DoS-Angriff gab. Das Ergebnis war im Wesentlichen, dass die tunnels bei nahezu allen fortlaufend fehlgeschlagen sind, was einen gewissen Schneeballeffekt hat. Also nein, es liegt nicht nur an euch – das Netz war auch für den Rest von uns grauenhaft ;)

Die gute Nachricht ist jedoch, dass wir die Probleme ziemlich schnell behoben haben und sie seit letzter Woche in CVS sind, aber das Netzwerk wird für die Nutzer weiterhin mies sein, bis die nächste Version veröffentlicht ist. In diesem Sinne ...

## 2) 0.3.5 und 0.4

Auch wenn das nächste Release alle geplanten Neuerungen für das Release 0.4 enthalten wird (neues Installationsprogramm, neuer Weboberflächen-Standard, neue i2ptunnel-Schnittstelle, Systray & Windows-Dienst, Verbesserungen beim Threading, Fehlerbehebungen usw.), war aufschlussreich, wie sich das letzte Release im Laufe der Zeit verschlechtert hat. Ich möchte, dass wir bei diesen Releases langsamer vorgehen, ihnen Zeit geben, vollständiger ausgerollt zu werden und damit sich Kinderkrankheiten zeigen können. Während der Simulator die Grundlagen erkunden kann, hat er keine Möglichkeit, die natürlichen Netzwerkprobleme zu simulieren, die wir im Live-Netz sehen (zumindest noch nicht).

Daher wird das nächste Release 0.3.5 sein – hoffentlich das letzte 0.3.*-Release, aber vielleicht auch nicht, falls weitere Probleme auftreten. Rückblickend darauf, wie das Netzwerk lief, als ich im Juni offline war, begann nach etwa zwei Wochen die Stabilität nachzulassen. Daher denke ich, dass wir damit warten sollten, uns auf die nächste 0.4-Release-Stufe hochzustufen, bis wir mindestens zwei Wochen lang einen hohen Grad an Zuverlässigkeit aufrechterhalten können. Das heißt natürlich nicht, dass wir in der Zwischenzeit nicht weiterarbeiten.

Wie dem auch sei, wie letzte Woche erwähnt, arbeitet hypercubus unermüdlich am neuen Installationssystem und schlägt sich damit herum, dass ich ständig Dinge umstelle und Unterstützung für schräge Systeme verlange. Wir sollten die Dinge in den nächsten Tagen ausbügeln, um dann in wenigen Tagen ein 0.3.5-Release herauszubringen.

## 3) Dokumentation

Eines der wichtigen Dinge, die wir während dieses zweiwöchigen "Testzeitfensters" vor 0.4 tun müssen, ist, wie verrückt zu dokumentieren. Was ich mich frage, ist, was ihr meint, was in unserer Dokumentation fehlt - welche Fragen habt ihr, die wir beantworten müssen? Auch wenn ich gern sagen würde: "ok, now, go write those documents", bin ich realistisch, daher bitte ich euch nur, zu identifizieren, was diese Dokumente behandeln würden.

Zum Beispiel ist eines der Dokumente, an denen ich derzeit arbeite, eine Überarbeitung des Bedrohungsmodells, das ich inzwischen als eine Reihe von Anwendungsfällen beschreiben würde, die erklären, wie I2P den Bedürfnissen verschiedener Personen gerecht werden kann, einschließlich der Funktionalität, der Angreifer, die dieser Person Sorgen bereiten, und wie sie sich dagegen schützt.

Wenn Sie der Meinung sind, dass Ihre Frage kein ausführliches Dokument erfordert, formulieren Sie sie einfach als Frage, dann können wir sie in die FAQ aufnehmen.

## 4) stasher update

Aum war heute früher am Tag im Channel und brachte ein Update mit (während ich ihn mit Fragen löcherte):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Wie Sie sehen, haben wir jede Menge Fortschritte gemacht. Selbst wenn die Schlüssel oberhalb der DHT-Schicht validiert werden, ist das verdammt cool (meiner Meinung nach). Los, aum!

## 5) ???

Ok, das ist alles, was ich zu sagen habe (was gut ist, denn das Meeting beginnt in ein paar Augenblicken) ... schau mal vorbei und sag, was du willst!

=jr
