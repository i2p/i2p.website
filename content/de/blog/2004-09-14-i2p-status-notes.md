---
title: "I2P-Statusnotizen für 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Wöchentliches I2P-Status-Update mit Informationen zum Release 0.4.0.1, zu Aktualisierungen des Bedrohungsmodells, Verbesserungen an der Website, Änderungen an der Roadmap sowie zum Entwicklungsbedarf für Client-Anwendungen"
categories: ["status"]
---

Hi zusammen, es ist wieder so weit.

## Stichwortverzeichnis:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Seit dem Release 0.4.0.1 am vergangenen Mittwoch läuft es im Netz ziemlich gut – mehr als zwei Drittel des Netzwerks haben aktualisiert, und es sind zwischen 60 und 80 Router im Netzwerk aktiv. Die IRC-Verbindungsdauer variiert, aber in letzter Zeit sind Verbindungen von 4-12 Stunden normal. Allerdings gab es einige Berichte über Merkwürdigkeiten beim Starten unter OS/X, doch ich glaube, dass auch dort Fortschritte gemacht werden.

## 2) Aktualisierungen des Bedrohungsmodells

Wie in der Antwort auf Tonis Beitrag erwähnt, gab es eine ziemlich umfassende Überarbeitung des Bedrohungsmodells. Der Hauptunterschied besteht darin, dass ich statt der früheren, eher ad-hoc gehaltenen Behandlung der Bedrohungen versucht habe, einigen der in der Fachliteratur vorgeschlagenen Taxonomien zu folgen. Das größte Problem für mich war, Wege zu finden, die tatsächlichen, von Menschen einsetzbaren Techniken in die angebotenen Muster einzuordnen – häufig passte ein einzelner Angriff in mehrere unterschiedliche Kategorien. Insofern bin ich nicht wirklich zufrieden damit, wie die Informationen auf dieser Seite vermittelt werden, aber es ist besser als zuvor.

## 3) Website-Aktualisierungen

Dank der Hilfe von Curiosity haben wir mit einigen Updates an der Website begonnen - das Sichtbarste davon kannst du direkt auf der Startseite sehen. Das sollte Leuten helfen, die zufällig auf I2P stoßen und gleich auf Anhieb wissen wollen, was zum Teufel dieses I2P-Ding ist, statt sich mühsam durch die verschiedenen Seiten zu wühlen. Wie auch immer, Fortschritt, immer weiter :)

## 4) Fahrplan

Apropos Fortschritt, ich habe endlich eine überarbeitete Roadmap zusammengestellt, auf Grundlage dessen, was aus meiner Sicht implementiert werden muss, sowie dessen, was erreicht werden muss, um den Bedürfnissen der Nutzer gerecht zu werden. Die wichtigsten Änderungen an der alten Roadmap sind:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Die anderen für verschiedene 0.4.*-Versionen vorgesehenen Punkte sind bereits implementiert worden. Allerdings gibt es noch eine weitere Sache, die aus der Roadmap gestrichen wurde...

## 5) Client-Anwendungen

Wir brauchen Client-Anwendungen. Anwendungen, die ansprechend, sicher, skalierbar und anonym sind. I2P leistet für sich genommen nicht viel, es ermöglicht lediglich, dass zwei Endpunkte anonym miteinander kommunizieren. Zwar bietet I2PTunnel ein verdammt vielseitiges Schweizer Taschenmesser, aber Werkzeuge dieser Art sind im Grunde nur für die Technikbegeisterten unter uns wirklich interessant. Wir brauchen mehr als das - wir brauchen etwas, das es den Menschen ermöglicht, das zu tun, was sie tatsächlich tun wollen, und das ihnen hilft, es besser zu tun. Wir brauchen einen Grund für Menschen, I2P zu nutzen, der über das bloße Argument hinausgeht, dass es sicherer ist.

Bisher habe ich MyI2P angepriesen, um diesem Bedarf gerecht zu werden – ein verteiltes Blogging-System mit einer LiveJournal-ähnlichen Oberfläche. Kürzlich habe ich auf der Liste einige der Funktionen innerhalb von MyI2P diskutiert. Ich habe es jedoch aus der Roadmap herausgenommen, da es einfach zu viel Arbeit für mich ist, das umzusetzen und dem I2P‑Basisnetzwerk gleichzeitig die nötige Aufmerksamkeit zu geben (wir sind ohnehin schon extrem ausgelastet).

Es gibt noch einige andere Apps, die sehr vielversprechend sind. Stasher würde eine bedeutende Infrastruktur für verteilte Datenspeicherung bereitstellen, aber ich bin mir nicht sicher, wie es damit vorangeht. Selbst mit Stasher bräuchte es jedoch eine ansprechende Benutzeroberfläche (auch wenn einige FCP-Apps möglicherweise damit arbeiten könnten).

IRC ist ebenfalls ein leistungsfähiges System, weist aufgrund der serverbasierten Architektur jedoch Einschränkungen auf. oOo hat daran gearbeitet, transparentes DCC zu implementieren, sodass der IRC-Teil vielleicht für öffentlichen Chat und DCC für private Dateiübertragungen oder serverlosen Chat genutzt werden könnte.

Die allgemeine eepsite(I2P Site)-Funktionalität ist ebenfalls wichtig, und das, was wir derzeit haben, ist völlig unbefriedigend. Wie DrWoo anmerkt, gibt es mit der aktuellen Konfiguration erhebliche Anonymitätsrisiken, und obwohl oOo einige Patches eingebracht hat, die bestimmte Header filtern, bleibt noch viel Arbeit, bevor eepsites(I2P Sites) als sicher gelten können. Es gibt mehrere unterschiedliche Ansätze, das anzugehen; sie können alle funktionieren, erfordern jedoch allesamt Arbeit. Ich weiß, dass duck erwähnte, er habe jemanden, der an etwas arbeitet; allerdings weiß ich nicht, wie weit das ist oder ob es mit I2P gebündelt werden könnte, damit es alle nutzen können, oder nicht. Duck?

Ein weiteres Paar von Client-Apps, die helfen könnten, wäre entweder eine Swarming-Dateiübertragungs-App (ala BitTorrent) oder eine traditionellere Filesharing-App (ala DC/Napster/Gnutella/etc). Das ist, so vermute ich, was viele Leute wollen, aber es gibt bei jedem dieser Systeme Probleme. Sie sind jedoch gut bekannt, und das Portieren wäre möglicherweise nicht allzu aufwendig (vielleicht).

Okay, das oben Gesagte ist also nichts Neues – warum habe ich das alles angesprochen? Nun, wir müssen einen Weg finden, eine ansprechende, sichere, skalierbare und anonyme Client-Anwendung zu implementieren, und das wird nicht von selbst aus heiterem Himmel passieren. Ich habe eingesehen, dass ich es nicht allein schaffen werde, also müssen wir proaktiv sein und einen Weg finden, es zu realisieren.

Um das zu erreichen, denke ich, dass unser Bounty-System helfen könnte, aber ich glaube, einer der Gründe, warum wir in dieser Hinsicht (Leute, die an der Umsetzung einer Bounty arbeiten) nicht viel Aktivität gesehen haben, ist, dass sie zu sehr ausgelastet sind. Um die Ergebnisse zu erzielen, die wir brauchen, halte ich es für notwendig, zu priorisieren, was wir wollen, und unsere Anstrengungen auf den wichtigsten Punkt zu richten, 'den Anreiz zu erhöhen', um hoffentlich jemanden zu ermutigen, die Initiative zu ergreifen und an der Bounty zu arbeiten.

Meiner persönlichen Meinung nach wäre nach wie vor ein sicheres und verteiltes Blogsystem wie MyI2P am besten. Statt lediglich anonym Daten hin- und herzuschieben, bietet es eine Möglichkeit, Communities aufzubauen – die Lebensader jedes Entwicklungsprojekts. Darüber hinaus bietet es ein relativ hohes Signal-Rausch-Verhältnis, eine geringe Gefahr des Missbrauchs gemeinsamer Ressourcen und, ganz allgemein, eine geringe Netzwerklast. Es bietet allerdings nicht den vollen Funktionsumfang normaler Websites, doch den 1,8 Millionen aktiven LiveJournal-Nutzern scheint das nichts auszumachen.

Darüber hinaus wäre die Absicherung der eepsite(I2P Site)-Architektur meine nächste Priorität, wodurch Browser die erforderliche Sicherheit erhalten und Menschen eepsites(I2P Sites) von Haus aus bereitstellen können.

Dateiübertragung und verteilte Datenspeicherung sind ebenfalls unglaublich leistungsfähig, aber sie scheinen nicht so sehr auf die Community ausgerichtet zu sein, wie wir es uns für die erste normale Endnutzer-App wahrscheinlich wünschen.

Ich möchte, dass alle aufgeführten Apps schon gestern umgesetzt wären, ebenso wie tausend weitere Apps, von denen ich mir nicht einmal im Traum eine Vorstellung machen kann. Außerdem wünsche ich mir Weltfrieden, ein Ende des Hungers, die Abschaffung des Kapitalismus, Freiheit von Etatismus, Rassismus, Sexismus, Homophobie, ein Ende der hemmungslosen Zerstörung der Umwelt und all das andere Unheil. Doch wir sind nur eine begrenzte Zahl von Menschen, und wir können nur so viel schaffen. Daher müssen wir Prioritäten setzen und unsere Anstrengungen darauf konzentrieren, das zu erreichen, was wir erreichen können, statt untätig dazusitzen und von all dem überwältigt zu sein, was wir tun wollen.

Vielleicht können wir heute Abend im Meeting ein paar Ideen dazu besprechen, was wir tun sollten.

## 6) ???

Nun, das ist alles, was ich für den Moment habe, und hey, ich habe die Statusnotizen *vor* dem Meeting geschrieben! Also keine Ausreden, schaut um 21:00 Uhr GMT vorbei und bombardiert uns alle mit euren Ideen.

=jr
