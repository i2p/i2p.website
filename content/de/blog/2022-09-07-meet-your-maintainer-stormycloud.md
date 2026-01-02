---
title: "Lernen Sie Ihren Maintainer kennen: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "Ein Interview mit den Maintainern des StormyCloud Outproxys"
categories: ["general"]
API_Translate: wahr
---

## Ein Gespräch mit StormyCloud Inc.

Mit der neuesten [I2P-Java-Version](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release) wurde der bestehende outproxy, false.i2p, für neue I2P-Installationen durch den neuen StormyCloud outproxy ersetzt. Für Personen, die ihren Router aktualisieren, kann der Wechsel zum Stormycloud-Dienst schnell vorgenommen werden.

Ändern Sie in Ihrem Hidden Services Manager sowohl Outproxies als auch SSL Outproxies auf exit.stormycloud.i2p und klicken Sie unten auf der Seite auf die Schaltfläche Speichern.

## Wer ist StormyCloud Inc.?

**Mission von StormyCloud Inc.**

Den Internetzugang als universelles Menschenrecht zu verteidigen. Damit schützt die Gruppe die elektronische Privatsphäre der Nutzer und stärkt die Gemeinschaft, indem sie unbeschränkten Zugang zu Informationen und damit den freien Austausch von Ideen über Grenzen hinweg fördert. Dies ist entscheidend, denn das Internet ist das mächtigste verfügbare Instrument, um positive Veränderungen in der Welt zu bewirken.

**Vision**

Ein Pionier bei der Bereitstellung eines freien und offenen Internets für alle im Universum zu werden, weil der Zugang zum Internet ein grundlegendes Menschenrecht ist ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Ich habe mich mit Dustin getroffen, um Hallo zu sagen und um ausführlicher über Datenschutz, den Bedarf an Diensten wie StormyCloud und darüber zu sprechen, was das Unternehmen dazu bewogen hat, sich I2P zuzuwenden.

**Was war die Inspiration hinter der Gründung von StormyCloud?**

Es war Ende 2021, ich war im Subreddit /r/tor. Dort hatte eine Person in einem Thread darüber, wie man Tor benutzt, geantwortet und berichtet, dass sie sich auf Tor verließ, um mit ihrer Familie in Kontakt zu bleiben. Ihre Familie lebte in den Vereinigten Staaten, doch die Person hielt sich damals in einem Land auf, in dem der Internetzugang stark eingeschränkt war. Sie musste sehr vorsichtig sein, mit wem sie kommunizierte und was sie sagte. Aus diesen Gründen verließ sich die Person auf Tor. Ich dachte darüber nach, wie ich ohne Angst oder Einschränkungen mit Menschen kommunizieren kann, und dass es für alle so sein sollte.

Das Ziel von StormyCloud ist es, so vielen Menschen wie möglich dabei zu helfen, das zu tun.

**Welche Herausforderungen gab es beim Aufbau von StormyCloud?**

Die Kosten — sie sind unglaublich hoch. Wir haben den Weg über ein Rechenzentrum gewählt, da der Umfang dessen, was wir tun, sich nicht in einem Heimnetzwerk realisieren lässt. Es fallen Hardwarekosten und wiederkehrende Hosting-Kosten an.

Beim Aufbau der gemeinnützigen Organisation sind wir dem Beispiel von Emerald Onion gefolgt und haben einige ihrer Dokumente und Erkenntnisse genutzt. Die Tor-Community stellt viele sehr hilfreiche Ressourcen bereit.

**Wie war die Resonanz auf Ihre Dienste?**

Im Juli haben wir über all unsere Dienste hinweg 1,5 Milliarden DNS-Anfragen beantwortet. Die Leute schätzen, dass keine Protokollierung stattfindet. Die Daten sind einfach nicht da, und das gefällt den Leuten.

**Was ist ein Outproxy?**

Ein outproxy (Ausgangs-Proxy) ist ähnlich wie die Exit-Knoten von Tor und ermöglicht, Clearnet-Verkehr (normaler Internetverkehr) über das I2P‑Netzwerk weiterzuleiten. Anders ausgedrückt, ermöglicht es I2P‑Nutzern, unter dem Schutz des I2P‑Netzwerks auf das Internet zuzugreifen.

**Was ist das Besondere am StormyCloud I2P Outproxy?**

Zunächst sind wir multi-homed (mehrfach angebunden), was bedeutet, dass wir mehrere Server haben, die den outproxy-Datenverkehr abwickeln. Das stellt sicher, dass der Dienst für die Community jederzeit verfügbar ist. Alle Protokolle auf unseren Servern werden alle 15 Minuten gelöscht. Damit haben weder Strafverfolgungsbehörden noch wir selbst Zugriff auf irgendwelche Daten. Wir unterstützen den Aufruf von Tor-Onion-Links über den outproxy, und unser outproxy ist ziemlich schnell.

**Wie definieren Sie Privatsphäre? Welche Probleme sehen Sie bei Befugnisüberschreitungen und beim Umgang mit Daten?**

Privatsphäre ist Freiheit von unbefugtem Zugriff. Transparenz ist wichtig, etwa durch Opt-in — ein Beispiel dafür sind die Anforderungen der DSGVO.

Es gibt große Unternehmen, die Daten horten, die für den [Zugriff auf Standortdaten ohne richterlichen Beschluss](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data) genutzt werden. Tech-Unternehmen überschreiten Grenzen und dringen in Bereiche ein, die Menschen für privat halten und die es auch sein sollten, etwa Fotos oder Nachrichten.

Es ist wichtig, weiterhin Aufklärungsarbeit darüber zu leisten, wie man seine Kommunikation absichert und welche Tools oder Apps dabei helfen. Die Art und Weise, wie wir mit all den Informationen da draußen umgehen, ist ebenfalls wichtig. Vertrauen ist gut, Kontrolle ist besser.

**Wie fügt sich I2P in StormyClouds Missions- und Visionserklärung ein?**

I2P ist ein Open-Source-Projekt, und das, was es bietet, steht im Einklang mit der Mission von StormyCloud Inc. I2P bietet eine zusätzliche Ebene an Privatsphäre und Schutz für Datenverkehr und Kommunikation, und das Projekt ist der Auffassung, dass jeder ein Recht auf Privatsphäre hat.

Wir wurden Anfang 2022 auf I2P aufmerksam, als wir mit Leuten aus der Tor-Community sprachen, und uns gefiel, was das Projekt machte. Es schien Tor ähnlich zu sein.

Während unserer Einführung in I2P und seine Funktionen erkannten wir den Bedarf an einem zuverlässigen Outproxy (Proxy für den Zugang zum regulären Internet). Wir erhielten wirklich großartige Unterstützung von Menschen aus der I2P-Community, um den Outproxy-Dienst aufzubauen und bereitzustellen.

**Fazit**

Die Notwendigkeit, das Bewusstsein für die Überwachung dessen zu schärfen, was in unserem Online-Leben eigentlich privat sein sollte, besteht weiterhin. Jede Datenerhebung sollte auf Zustimmung beruhen, und Privatsphäre sollte selbstverständlich sein.

In Situationen, in denen wir nicht darauf vertrauen können, dass unser Datenverkehr oder unsere Kommunikation nicht ohne Zustimmung überwacht wird, haben wir glücklicherweise Zugang zu Netzwerken, die von vornherein darauf ausgelegt sind, den Datenverkehr zu anonymisieren und unsere Standorte zu verbergen.

Vielen Dank an StormyCloud und alle, die outproxies oder Knoten für Tor und I2P bereitstellen, damit Menschen bei Bedarf sicherer auf das Internet zugreifen können. Ich freue mich darauf, dass mehr Menschen die Möglichkeiten dieser sich ergänzenden Netzwerke kombinieren, um ein robusteres Ökosystem für Privatsphäre für alle zu schaffen.

Erfahren Sie mehr über die Dienstleistungen von StormyCloud Inc. unter [https://stormycloud.org/](https://stormycloud.org/) und unterstützen Sie die Arbeit von StormyCloud Inc. mit einer Spende unter [https://stormycloud.org/donate/](https://stormycloud.org/donate/).
