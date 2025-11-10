---
title: "Wie Sie Ihre bestehende Website als I2P eepSite bereitstellen"
date: 2019-06-02
author: "idk"
description: "Bereitstellung eines I2P-Spiegels"
categories: ["tutorial"]
---

Dieser Blogbeitrag dient als allgemeine Anleitung zum Betrieb eines Spiegels eines Clearnet-Dienstes als eepSite. Er baut auf dem vorherigen Blogbeitrag über grundlegende I2PTunnel tunnels auf.

Leider ist es wahrscheinlich unmöglich, *vollständig* alle möglichen Fälle abzudecken, in denen eine bestehende Website als eepSite verfügbar gemacht wird; die Vielfalt der serverseitigen Software ist dafür einfach zu groß, ganz zu schweigen von den praktischen Besonderheiten jeder konkreten Bereitstellung. Stattdessen werde ich versuchen, so spezifisch wie möglich den allgemeinen Prozess zu vermitteln, einen Dienst für die Bereitstellung im eepWeb (I2P-Web) oder in anderen versteckten Diensten vorzubereiten.

Ein großer Teil dieses Leitfadens wird die Leserin oder den Leser als Gesprächspartner behandeln; insbesondere, wenn es mir ernst ist, werde ich die Leserin bzw. den Leser direkt ansprechen (d. h. „you“ statt „one“ verwenden), und ich werde Abschnitte häufig mit Fragen als Überschrift versehen, von denen ich glaube, dass sie sich die Leserin oder der Leser stellen könnte. Dies ist schließlich ein „Prozess“, in den sich eine Administratorin oder ein Administrator eingebunden fühlen muss – genau wie beim Hosten jedes anderen Dienstes.

**HAFTUNGSAUSSCHLÜSSE:**

So wünschenswert es auch wäre, es ist für mich wahrscheinlich unmöglich, für jede einzelne Art von Software, die man zum Hosten von Websites verwenden könnte, spezifische Anleitungen bereitzustellen. Daher erfordert dieses Tutorial einige Annahmen seitens des Autors und seitens des Lesers kritisches Denken sowie gesunden Menschenverstand. Um es klarzustellen, **ich gehe davon aus, dass die Person, die diesem Tutorial folgt, bereits einen Clearnet-Dienst betreibt, der einer realen Identität oder Organisation zuordenbar ist** und daher lediglich anonymen Zugang anbietet und sich selbst nicht anonymisiert.

Daher **wird keinerlei Anonymisierung versucht** bei einer Verbindung von einem Server zu einem anderen. Wenn Sie einen neuen, nicht zuordenbaren versteckten Dienst betreiben möchten, der Inhalte hostet, die nicht mit Ihnen in Verbindung gebracht werden, sollten Sie das nicht auf Ihrem eigenen Clearnet-Server oder von zu Hause aus tun.
