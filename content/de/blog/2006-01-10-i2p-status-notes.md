---
title: "I2P-Statusnotizen für 2006-01-10"
date: 2006-01-10
author: "jr"
description: "Wöchentliches Update zu Algorithmen zur Durchsatzprofilierung, Verbesserungen der Syndie-Blogansicht, Fortschritten bei HTTP-Persistentverbindungen und zur Entwicklung von I2Phex gwebcache"
categories: ["status"]
---

Hallo zusammen, anscheinend ist schon wieder Dienstag

* Index

1) Netzstatus 2) Durchsatz-Profiling 3) Syndie-Blogs 4) persistente HTTP-Verbindungen 5) I2Phex gwebcache 6) ???

* 1) Net status

Die vergangene Woche brachte eine Menge Fehlerbehebungen und Verbesserungen in CVS, der aktuelle Build liegt bei 0.6.1.8-11. Das Netzwerk war ziemlich stabil, auch wenn einige Ausfälle bei verschiedenen i2p-Diensteanbietern gelegentlich zu einem Schluckauf führten. Wir sind die unnötig hohe router-Identitätsfluktuation in CVS endlich los, und es gibt einen neuen Bugfix am Kern, den zzz gestern eingebracht hat, der sehr vielversprechend klingt, aber wir müssen abwarten, wie sich das auswirkt. Zwei weitere große Themen der vergangenen Woche waren das neue durchsatzbasierte Speed-Profiling sowie größere Arbeiten an Syndies Blog-Ansicht. Was 0.6.1.9 angeht: Es sollte später in dieser Woche erscheinen, spätestens am Wochenende. Behaltet die üblichen Kanäle im Blick.

* 2) Throughput profiling

Wir haben einige neue Peer-Profiling-Algorithmen zur Überwachung des Durchsatzes getestet, aber in der letzten Woche oder so scheinen wir uns auf einen festgelegt zu haben, der sich als ziemlich gut erweist. Im Wesentlichen überwacht er den bestätigten Durchsatz einzelner tunnels über 1-minütige Zeiträume und passt entsprechend die Durchsatzschätzungen für die Peers an. Er versucht nicht, eine durchschnittliche Rate für einen Peer zu ermitteln, da dies sehr kompliziert ist, weil tunnels mehrere Peers umfassen und bestätigte Durchsatzmessungen oft mehrere tunnels erfordern. Stattdessen ermittelt er eine durchschnittliche Spitzenrate – konkret misst er die drei höchsten Raten, mit denen die tunnels des Peers übertragen konnten, und bildet daraus den Durchschnitt.

Im Kern bedeutet das, dass diese Raten, da sie über eine volle Minute gemessen werden, dauerhaft erzielbare Geschwindigkeiten sind, zu denen der Peer in der Lage ist, und da jeder Peer mindestens so schnell ist wie die End-to-End gemessene Rate, ist es sicher, jeden von ihnen als so schnell zu markieren. Wir hatten noch eine weitere Variante ausprobiert - den Gesamtdurchsatz eines Peers durch tunnels über verschiedene Zeiträume hinweg zu messen -, und das lieferte noch klarere Informationen zur Spitzenrate, benachteiligte aber stark jene Peers, die nicht bereits als "fast" markiert waren, da "fast"-Peers deutlich häufiger genutzt werden (client tunnels verwenden nur fast Peers). Das Ergebnis dieser Gesamtdurchsatzmessung war, dass sie für die ausreichend Belasteten hervorragende Daten lieferte; allerdings waren nur die fast Peers ausreichend belastet, und es gab kaum eine effektive Erkundung.

Die Verwendung von 1-Minuten-Intervallen und des Durchsatzes eines einzelnen tunnel scheint jedoch plausiblere Werte zu liefern. Dieser Algorithmus wird im nächsten Release zum Einsatz kommen.

* 3) Syndie blogs

Basierend auf einigen Rückmeldungen wurden in der Blogansicht von Syndie weitere Verbesserungen vorgenommen, wodurch sie sich deutlich von der Newsgroup-/Forum-ähnlichen Thread-Ansicht unterscheidet. Darüber hinaus gibt es jetzt eine völlig neue Möglichkeit, allgemeine Bloginformationen über die bestehende Syndie-Architektur zu definieren. Als Beispiel siehe den Standard-Blogbeitrag "about Syndie":  http://syndiemedia.i2p.net/blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=/1132012800001

Das ist nur der Anfang dessen, was wir tun können. Die nächste Version wird es dir ermöglichen, das Logo deines Blogs festzulegen, deine eigenen Links (zu Blogs, Beiträgen, Anhängen, beliebigen externen URLs) zu definieren und hoffentlich noch mehr Möglichkeiten zur Anpassung. Eine solche Anpassung ist die Verwendung von Icons pro Tag - ich würde gerne einen Satz Standard-Icons mitliefern, die mit Standard-Tags verwendet werden können, aber Nutzer werden für ihre eigenen Tags Icons definieren können, die in ihrem Blog verwendet werden, und sogar die Standard-Icons für die Standard-Tags überschreiben (wieder nur, wenn jemand ihren Blog betrachtet, versteht sich). Vielleicht sogar eine Stilkonfiguration, um Beiträge mit unterschiedlichen Tags unterschiedlich darzustellen (natürlich wären nur sehr spezifische Stil-Anpassungen erlaubt - keine beliebigen CSS-Exploits mit Syndie, vielen Dank auch :)

Es gibt noch vieles, was ich mit der Blog-Ansicht gerne machen würde, das im nächsten Release nicht enthalten sein wird, aber sie sollte ein guter Anstoß sein, damit die Leute mit einigen ihrer Funktionen herumspielen; hoffentlich könnt ihr mir dadurch zeigen, was *ihr* braucht, und nicht das, was ich denke, dass ihr wollt. Ich mag ein guter Coder sein, aber ich bin ein schlechter Hellseher.

* 4) HTTP persistent connections

zzz ist ein Maniac, ich sag's euch. Es gibt Fortschritte bei einem lange gewünschten Feature - Unterstützung für persistente HTTP-Verbindungen, die es erlaubt, mehrere HTTP-Anfragen über einen einzelnen Stream zu senden und im Gegenzug mehrere Antworten zu empfangen. Ich glaube, jemand hat das vor etwa zwei Jahren zum ersten Mal angefragt, und es könnte bei bestimmten Arten von eepsite(I2P Site) oder beim Outproxying eine Menge helfen. Ich weiß, die Arbeit ist noch nicht fertig, aber es geht voran. Hoffentlich kann zzz uns während des Meetings ein Status-Update geben.

* 5) I2Phex gwebcache

Ich habe Berichte über Fortschritte beim Wiedereinbau der gwebcache-Unterstützung in I2Phex gehört, aber ich weiß nicht, wie der Stand im Moment ist. Vielleicht kann Complication uns dazu heute Abend ein Update geben?

* 6) ???

Es ist eine Menge los, wie ihr seht, aber wenn es noch andere Dinge gibt, die ihr ansprechen und diskutieren möchtet, schaut in ein paar Minuten einfach beim Meeting vorbei und meldet euch. Nebenbei: Eine nette Seite, die ich mir in letzter Zeit ansehe, ist http://freedomarchive.i2p/ (für die Bequemen unter euch, die kein I2P installiert haben: Ihr könnt Tinos inproxy über http://freedomarchive.i2p.tin0.de/ verwenden). Wie auch immer, wir sehen uns in ein paar Minuten.

=jr
