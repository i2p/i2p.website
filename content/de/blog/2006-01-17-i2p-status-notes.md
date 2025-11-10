---
title: "I2P-Statusnotizen für 2006-01-17"
date: 2006-01-17
author: "jr"
description: "Netzwerkstatus mit 0.6.1.9, Verbesserungen der Kryptografie bei der Erstellung von tunnel und Aktualisierungen der Syndie-Blog-Oberfläche"
categories: ["status"]
---

Hi zusammen, es ist wieder Dienstag

* Index

1) Netzstatus und 0.6.1.9 2) Kryptografie für die Tunnel-Erstellung 3) Syndie-Blogs 4) ???

* 1) Net status and 0.6.1.9

Da 0.6.1.9 veröffentlicht wurde und 70 % des Netzwerks aktualisiert wurden, scheinen die meisten der enthaltenen Bugfixes wie erwartet zu funktionieren, und Berichten zufolge wählt das neue Speed-Profiling einige gute Peers aus. Ich habe von anhaltendem Durchsatz bei schnellen Peers von über 300KBps bei 50–70 % CPU-Auslastung gehört, während andere router im Bereich von 100–150KBps liegen, mit einem Abfall bis hin zu solchen, die 1–5KBps schaffen. Es gibt jedoch weiterhin erhebliche Fluktuation der router-Identität, daher scheint das Bugfix, von dem ich dachte, es würde das verringern, dies nicht getan zu haben (oder die Fluktuation ist legitim).

* 2) Tunnel creation crypto

Im Herbst gab es viele Diskussionen darüber, wie wir unsere tunnels aufbauen, sowie über die Abwägungen zwischen der teleskopischen tunnel-Erstellung im Tor‑Stil und der explorativen tunnel-Erstellung im I2P‑Stil [1]. Dabei haben wir eine Kombination [2] entwickelt, die die Probleme der teleskopischen tunnel-Erstellung im Tor‑Stil [3] beseitigt, die unidirektionalen Vorteile von I2P beibehält und unnötige Fehlversuche verringert. Da zu dieser Zeit viele andere Dinge anstanden, wurde die Umsetzung der neuen Kombination zunächst zurückgestellt, aber da wir uns nun dem 0.6.2‑Release nähern, bei dem wir den Code zur tunnel-Erstellung ohnehin überarbeiten müssen, ist es an der Zeit, das abschließend auszuarbeiten.

Ich habe neulich einen Entwurf einer Spezifikation für die neue tunnel-Kryptographie skizziert und in meinem Syndie-Blog veröffentlicht, und nach ein paar kleineren Änderungen, die sich bei der tatsächlichen Implementierung ergeben haben, liegt die Spezifikation jetzt in CVS [4] vor. Es gibt in CVS [5] auch grundlegenden Code, der das implementiert, allerdings ist er noch nicht in den tatsächlichen tunnel-Aufbau eingebunden. Falls sich jemand langweilt, würde ich mich über Feedback zur Spezifikation freuen. In der Zwischenzeit arbeite ich weiter am neuen Code für den tunnel-Aufbau.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html und     siehe die Threads zu den Bootstrap-Angriffen [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Wie zuvor erwähnt, bringt dieses neue Release 0.6.1.9 einige wesentliche Überarbeitungen der Syndie-Blogoberfläche mit sich, einschließlich des neuen Stylings von cervantes und der individuellen Auswahl der Blog-Links und des Logos durch jeden Benutzer (z. B. [6]). Sie können diese Links auf der linken Seite steuern, indem Sie auf Ihrer Profilseite den Link "configure your blog" anklicken, der Sie zu http://localhost:7657/syndie/configblog.jsp führt. Sobald Sie dort Ihre Änderungen vorgenommen haben, werden diese Informationen beim nächsten Mal, wenn Sie einen Beitrag in ein Archiv hochladen, anderen zur Verfügung gestellt.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Da ich schon 20 Minuten zu spät zum Meeting bin, sollte ich mich wohl kurz fassen. Ich weiß, dass noch ein paar andere Dinge laufen, aber statt sie hier auszubreiten, sollten Entwickler, die darüber sprechen möchten, beim Meeting vorbeischauen und sie zur Sprache bringen. Wie auch immer, das war’s fürs Erste, wir sehen uns auf #i2p!

=jr
