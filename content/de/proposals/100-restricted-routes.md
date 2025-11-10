---
title: "Eingeschränkte Routen"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reservieren"
thread: "http://zzz.i2p/topics/114"
---

## Einführung


## Überlegungen

- Einen neuen Transport "IND" (indirekt) hinzufügen, der einen leaseSet-Hash in der
  RouterAddress-Struktur veröffentlicht: "IND: [key=aababababababababb]". Dieser Transport bietet
  die niedrigste Priorität, wenn der Ziel-Router ihn veröffentlicht. Um über
  diesen Transport zu einem Peer zu senden, holen Sie das leaseset wie gewohnt von einem ff Peer und senden es
  direkt an das Lease.

- Ein Peer, der IND bewirbt, muss eine Reihe von Tunneln zu einem anderen
  Peer aufbauen und pflegen. Dies sind keine explorativen Tunnel und keine Client-Tunnel, sondern eine zweite
  Reihe von Router-Tunneln.

  - 1-Hop ist ausreichend?
  - Wie wählt man Peers für diese Tunnel aus?
  - Sie müssen "nicht eingeschränkt" sein, aber wie weiß man das? Erreichbarkeits-
    Mapping? Grafentheorie, Algorithmen, Datenstrukturen könnten hier helfen. Muss darüber
    lesen. Siehe Tunnel TODO.

- Wenn Sie IND-Tunnel haben, muss Ihr IND-Transport bieten (mit niedriger Priorität), um
  Nachrichten über diese Tunnel zu senden.

- Wie man entscheidet, indirekte Tunnel zu aktivieren

- Wie man implementiert und testet, ohne die Tarnung auffliegen zu lassen
