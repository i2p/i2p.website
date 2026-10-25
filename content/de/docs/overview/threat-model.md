---
title: "I2P's Bedrohungsmodell"
description: "Analyse der in I2Ps Design berücksichtigten Angriffe und der vorhandenen Schutzmaßnahmen"
slug: "threat-model"
aliases:
  - "/de/how_threatmodel"
  - "/de/how_threatmodel/"
lastUpdated: "2010-11"
accurateFor: "0.8.1"
---

## Was meinen wir mit "anonym"?

Ihr Grad der Anonymität kann beschrieben werden als "wie schwer es für jemanden ist, Informationen herauszufinden, die Sie nicht preisgeben möchten" — wer Sie sind, wo Sie sich befinden, mit wem Sie kommunizieren oder sogar wann Sie kommunizieren. "Perfekte" Anonymität ist hier kein sinnvolles Konzept — Software wird Sie nicht ununterscheidbar von Personen machen, die keine Computer benutzen oder nicht im Internet sind. Stattdessen arbeiten wir daran, ausreichende Anonymität zu bieten, um die realen Bedürfnisse all derer zu erfüllen, denen wir helfen können — von jenen, die einfach nur Websites durchstöbern, bis hin zu denen, die Daten austauschen, bis zu jenen, die eine Entdeckung durch mächtige Organisationen oder Staaten befürchten.

Die Frage, ob I2P ausreichende Anonymität für Ihre speziellen Bedürfnisse bietet, ist schwer zu beantworten, aber diese Seite wird Ihnen hoffentlich dabei helfen, diese Frage zu beantworten, indem sie erforscht, wie I2P unter verschiedenen Angriffen funktioniert, damit Sie entscheiden können, ob es Ihren Anforderungen entspricht.

Wir begrüßen weitere Forschung und Analyse zu I2P's Widerstandsfähigkeit gegen die unten beschriebenen Bedrohungen. Mehr Überprüfung der vorhandenen Literatur (von der sich vieles auf Tor konzentriert) und Originalarbeit mit Fokus auf I2P ist erforderlich.

---

## Netzwerktopologie-Zusammenfassung

I2P baut auf den Ideen vieler [anderer](/docs/overview/comparison/) Systeme auf, aber einige wichtige Punkte sollten beim Studium der entsprechenden Literatur beachtet werden:

- **I2P ist ein freies Route-Mixnet** — der Nachrichten-Ersteller definiert explizit den Pfad, über den Nachrichten gesendet werden (der ausgehende tunnel), und der Nachrichten-Empfänger definiert explizit den Pfad, über den Nachrichten empfangen werden (der eingehende tunnel).
- **I2P hat keine offiziellen Ein- und Ausstiegspunkte** — alle Peers nehmen vollständig am Mix teil, und es gibt keine Netzwerkschicht-Ein- oder -Aus-Proxies (allerdings existieren auf der Anwendungsschicht einige wenige Proxies).
- **I2P ist vollständig verteilt** — es gibt keine zentralen Kontrollen oder Autoritäten. Man könnte einige router so modifizieren, dass sie Mix-Kaskaden betreiben (tunnels aufbauen und die Schlüssel ausgeben, die zur Kontrolle der Weiterleitung am tunnel-Endpunkt notwendig sind) oder verzeichnisbasiertes Profiling und Auswahl durchführen, alles ohne die Kompatibilität mit dem Rest des Netzwerks zu brechen, aber dies ist natürlich nicht notwendig (und könnte sogar die eigene Anonymität beeinträchtigen).

Wir haben dokumentierte Pläne zur Implementierung von nichttrivialen Verzögerungen und Batching-Strategien, deren Existenz nur dem jeweiligen Hop oder tunnel-Gateway bekannt ist, das die Nachricht empfängt. Dies ermöglicht es einem größtenteils niedrig-latenten Mixnet, Cover-Traffic für Kommunikation mit höherer Latenz (z.B. E-Mail) bereitzustellen. Wir sind uns jedoch bewusst, dass erhebliche Verzögerungen erforderlich sind, um sinnvollen Schutz zu bieten, und dass die Implementierung solcher Verzögerungen eine erhebliche Herausforderung darstellen wird. Es ist zu diesem Zeitpunkt nicht klar, ob wir diese Verzögerungsfunktionen tatsächlich implementieren werden.

Theoretisch können Router entlang des Nachrichtenpfads eine beliebige Anzahl von Hops einfügen, bevor sie die Nachricht an den nächsten Peer weiterleiten, obwohl die aktuelle Implementierung dies nicht tut.

---

## Das Bedrohungsmodell

Das I2P-Design begann 2003, nicht lange nach dem Aufkommen von [Onion Routing](http://www.onion-router.net), [Freenet](http://freenetproject.org/) und [Tor](https://www.torproject.org/). Unser Design profitiert erheblich von der Forschung, die zu dieser Zeit veröffentlicht wurde. I2P verwendet mehrere Onion-Routing-Techniken, daher profitieren wir weiterhin vom bedeutenden akademischen Interesse an Tor.

Basierend auf den Angriffen und Analysen aus der [Anonymitätsliteratur](http://freehaven.net/anonbib/topic.html) (hauptsächlich [Traffic Analysis: Protocols, Attacks, Design Issues and Open Problems](http://citeseer.ist.psu.edu/454354.html)) beschreibt das Folgende kurz eine Vielzahl von Angriffen sowie viele von I2P's Verteidigungsmaßnahmen. Wir aktualisieren diese Liste, um neue Angriffe hinzuzufügen, sobald sie identifiziert werden.

Enthalten sind einige Angriffe, die möglicherweise spezifisch für I2P sind. Wir haben nicht für alle diese Angriffe gute Antworten, jedoch forschen wir weiterhin und verbessern unsere Abwehrmaßnahmen.

Darüber hinaus sind viele dieser Angriffe deutlich einfacher, als sie sein sollten, aufgrund der bescheidenen Größe des aktuellen Netzwerks. Obwohl wir uns einiger Einschränkungen bewusst sind, die angegangen werden müssen, ist I2P darauf ausgelegt, Hunderttausende oder Millionen von Teilnehmern zu unterstützen. Während wir weiterhin das Bewusstsein verbreiten und das Netzwerk vergrößern, werden diese Angriffe viel schwieriger werden.

Die Seiten zu [Netzwerkvergleichen](/docs/overview/comparison/) und zur ["Garlic"-Terminologie](/docs/overview/garlic-routing/) können ebenfalls hilfreich sein.

### Brute-Force-Angriffe

Ein Brute-Force-Angriff kann von einem globalen passiven oder aktiven Gegner durchgeführt werden, der alle Nachrichten zwischen allen Knoten beobachtet und versucht zu korrelieren, welche Nachricht welchem Pfad folgt. Einen solchen Angriff gegen I2P durchzuführen sollte nicht trivial sein, da alle Peers im Netzwerk häufig Nachrichten senden (sowohl End-to-End- als auch Netzwerk-Wartungsnachrichten), und außerdem ändert eine End-to-End-Nachricht Größe und Daten entlang ihres Pfades. Zusätzlich hat der externe Gegner keinen Zugang zu den Nachrichten, da die Kommunikation zwischen den Routern sowohl verschlüsselt als auch gestreamt ist (wodurch zwei 1024-Byte-Nachrichten nicht von einer 2048-Byte-Nachricht zu unterscheiden sind).

Ein mächtiger Angreifer kann jedoch Brute-Force-Methoden einsetzen, um Trends zu erkennen — wenn er 5GB an ein I2P-Ziel senden und die Netzwerkverbindung aller überwachen kann, kann er alle Peers ausschließen, die keine 5GB Daten erhalten haben. Techniken zur Abwehr dieses Angriffs existieren, können aber unerschwinglich teuer sein (siehe: [Tarzan](http://citeseer.ist.psu.edu/freedman02tarzan.html)s Mimics oder konstanter Datenverkehr mit gleichbleibender Rate). Die meisten Nutzer sind nicht über diesen Angriff besorgt, da die Kosten für seine Durchführung extrem sind (und oft illegale Aktivitäten erfordern). Der Angriff ist jedoch weiterhin möglich, beispielsweise durch einen Beobachter bei einem großen ISP oder an einem Internet-Knotenpunkt. Diejenigen, die sich davor schützen wollen, sollten entsprechende Gegenmaßnahmen ergreifen, wie das Setzen niedriger Bandbreitenlimits und die Verwendung unveröffentlichter oder verschlüsselter leaseSets für I2P Sites. Andere Gegenmaßnahmen, wie nichttriviale Verzögerungen und eingeschränkte Routen, sind derzeit nicht implementiert.

Als teilweiser Schutz gegen einen einzelnen router oder eine Gruppe von routern, die versuchen, den gesamten Netzwerkverkehr zu routen, enthalten router Limits dafür, wie viele tunnel durch einen einzelnen Peer geleitet werden können. Während das Netzwerk wächst, können diese Limits weiter angepasst werden. Andere Mechanismen für Peer-Bewertung, -Auswahl und -Vermeidung werden auf der Peer-Auswahlseite besprochen.

### Timing-Angriffe

I2P-Nachrichten sind unidirektional und bedeuten nicht zwangsläufig, dass eine Antwort gesendet wird. Allerdings werden Anwendungen, die auf I2P aufbauen, höchstwahrscheinlich erkennbare Muster in der Häufigkeit ihrer Nachrichten aufweisen — beispielsweise wird eine HTTP-Anfrage eine kleine Nachricht sein, gefolgt von einer großen Abfolge von Antwortnachrichten, die die HTTP-Antwort enthalten. Unter Verwendung dieser Daten sowie einer umfassenden Sicht auf die Netzwerktopologie könnte ein Angreifer möglicherweise einige Verbindungen als zu langsam ausschließen, um die Nachricht weitergeleitet zu haben.

Diese Art von Angriff ist mächtig, aber ihre Anwendbarkeit auf I2P ist nicht offensichtlich, da die Variation bei Nachrichtenverzögerungen durch Warteschlangen, Nachrichtenverarbeitung und Drosselung oft die Zeit für die Weiterleitung einer Nachricht über eine einzelne Verbindung erreicht oder überschreitet — selbst wenn der Angreifer weiß, dass eine Antwort gesendet wird, sobald die Nachricht empfangen wurde. Es gibt jedoch einige Szenarien, die ziemlich automatische Antworten preisgeben — die Streaming-Bibliothek tut dies (mit SYN+ACK) ebenso wie der Nachrichtenmodus der garantierten Zustellung (mit DataMessage+DeliveryStatusMessage).

Ohne Protocol Scrubbing oder höhere Latenz können globale aktive Angreifer erhebliche Informationen erlangen. Daher könnten Personen, die sich wegen dieser Angriffe Sorgen machen, die Latenz erhöhen (durch nichttriviale Verzögerungen oder Batching-Strategien), Protocol Scrubbing einschließen oder andere fortgeschrittene tunnel-Routing-Techniken verwenden, aber diese sind in I2P nicht implementiert.

Referenzen: [Low-Resource Routing Attacks Against Anonymous Systems](http://www.cs.colorado.edu/department/publications/reports/docs/CU-CS-1025-07.pdf)

### Intersection-Angriffe

Intersection-Angriffe gegen Systeme mit niedriger Latenz sind äußerst wirkungsvoll — regelmäßig Kontakt mit dem Ziel aufnehmen und verfolgen, welche Peers im Netzwerk sind. Mit der Zeit, während sich die Knotenfluktuation vollzieht, wird der Angreifer bedeutsame Informationen über das Ziel erlangen, indem er einfach die Mengen der Peers schneidet, die online sind, wenn eine Nachricht erfolgreich durchgeht. Die Kosten dieses Angriffs steigen erheblich mit der Größe des Netzwerks, können aber in einigen Szenarien durchführbar sein.

Zusammenfassend lässt sich sagen, dass ein Angreifer erfolgreich sein könnte, wenn er sich gleichzeitig an beiden Enden Ihres tunnels befindet. I2P hat keine vollständige Abwehr dagegen bei Kommunikation mit geringer Latenz. Dies ist eine inhärente Schwäche des Onion-Routing mit geringer Latenz. Tor stellt einen [ähnlichen Haftungsausschluss](https://trac.torproject.org/projects/tor/wiki/TheOnionRouter/TorFAQ#Whatattacksremainagainstonionrouting) bereit.

Teilweise implementierte Schutzmaßnahmen in I2P:

- [Strikte Reihenfolge](/docs/specs/tunnel-implementation/#ordering) von Peers
- Peer-Profilerstellung und -auswahl aus einer kleinen Gruppe, die sich langsam ändert
- Begrenzungen der Anzahl von tunnels, die durch einen einzelnen Peer geleitet werden
- Verhinderung, dass Peers aus demselben /16 IP-Bereich Mitglieder eines einzelnen tunnels werden
- Für I2P-Sites oder andere gehostete Dienste unterstützen wir gleichzeitiges Hosting auf mehreren routern oder Multihoming

Selbst in ihrer Gesamtheit stellen diese Abwehrmaßnahmen keine vollständige Lösung dar. Außerdem haben wir einige Designentscheidungen getroffen, die unsere Anfälligkeit erheblich erhöhen könnten:

- Wir verwenden keine "guard nodes" mit geringer Bandbreite
- Wir nutzen tunnel-Pools, die aus mehreren tunnels bestehen, und der Datenverkehr kann von tunnel zu tunnel wechseln.
- Tunnels sind nicht langlebig; neue tunnels werden alle 10 Minuten aufgebaut.
- Tunnel-Längen sind konfigurierbar. Während 3-Hop-tunnels für vollständigen Schutz empfohlen werden, verwenden mehrere Anwendungen und Dienste standardmäßig 2-Hop-tunnels.

In Zukunft könnte es für Peers möglich sein, die sich erhebliche Verzögerungen leisten können (gemäß nichttrivialer Verzögerungen und Batch-Strategien). Darüber hinaus ist dies nur für Ziele relevant, von denen andere Personen wissen — eine private Gruppe, deren Ziel nur vertrauenswürdigen Peers bekannt ist, muss sich keine Sorgen machen, da ein Angreifer sie nicht "anpingen" kann, um den Angriff durchzuführen.

Referenz: [One Cell Enough](http://blog.torproject.org/blog/one-cell-enough)

### Denial of Service Angriffe

Es gibt eine ganze Reihe von Denial-of-Service-Angriffen, die gegen I2P möglich sind, jeder mit unterschiedlichen Kosten und Konsequenzen:

**Greedy user attack:** Das sind einfach Leute, die versuchen, deutlich mehr Ressourcen zu verbrauchen, als sie bereit sind beizutragen. Die Verteidigung dagegen ist:

- Setze Standardwerte so, dass die meisten Benutzer Ressourcen für das Netzwerk bereitstellen. In I2P leiten Benutzer standardmäßig Datenverkehr weiter. Im scharfen Gegensatz zu [anderen Netzwerken](/docs/overview/comparison/) leiten über 95% der I2P-Benutzer Datenverkehr für andere weiter.
- Biete einfache Konfigurationsoptionen, damit Benutzer ihren Beitrag (Anteilsprozentsatz) zum Netzwerk erhöhen können. Zeige leicht verständliche Metriken wie "Anteilsverhältnis" an, damit Benutzer sehen können, was sie beitragen.
- Erhalte eine starke Community mit Blogs, Foren, IRC und anderen Kommunikationsmitteln aufrecht.

**Starvation attack:** Ein feindlicher Benutzer könnte versuchen, dem Netzwerk zu schaden, indem er eine erhebliche Anzahl von Peers im Netzwerk erstellt, die nicht als unter der Kontrolle derselben Entität stehend identifiziert werden (wie bei Sybil). Diese Knoten entscheiden dann, dem Netzwerk keine Ressourcen zur Verfügung zu stellen, wodurch bestehende Peers gezwungen werden, eine größere Netzwerkdatenbank zu durchsuchen oder mehr tunnel anzufordern als notwendig sein sollte. Alternativ können die Knoten intermittierenden Service bieten, indem sie periodisch ausgewählten Traffic verwerfen oder Verbindungen zu bestimmten Peers verweigern. Dieses Verhalten kann von dem eines stark belasteten oder ausfallenden Knotens nicht zu unterscheiden sein. I2P geht mit diesen Problemen um, indem es Profile über die Peers führt, versucht, schlecht performende zu identifizieren und sie einfach ignoriert oder sie selten verwendet. Wir haben die Fähigkeit zur Erkennung und Vermeidung problematischer Peers erheblich verbessert; dennoch sind in diesem Bereich noch erhebliche Anstrengungen erforderlich.

**Flooding-Angriff:** Ein böswilliger Benutzer kann versuchen, das Netzwerk, einen Peer, ein Ziel oder einen tunnel zu überlasten. Netzwerk- und Peer-Flooding ist möglich, und I2P unternimmt nichts, um Standard-IP-Layer-Flooding zu verhindern. Das Überlasten eines Ziels mit Nachrichten durch das Senden einer großen Anzahl an die verschiedenen inbound tunnel Gateways des Ziels ist möglich, aber das Ziel wird dies sowohl durch den Inhalt der Nachricht als auch dadurch erkennen, dass die tunnel-Tests fehlschlagen. Dasselbe gilt für das Überlasten nur eines einzelnen tunnels. I2P hat keine Abwehrmechanismen gegen einen Netzwerk-Flooding-Angriff. Bei einem Ziel- und tunnel-Flooding-Angriff identifiziert das Ziel, welche tunnel nicht reagieren und baut neue auf. Neuer Code könnte auch geschrieben werden, um noch mehr tunnel hinzuzufügen, wenn der Client die größere Last bewältigen möchte. Wenn andererseits die Last mehr ist, als der Client bewältigen kann, kann er die tunnel anweisen, die Anzahl der Nachrichten oder Bytes zu drosseln, die sie weiterleiten sollen (sobald der erweiterte tunnel-Betrieb implementiert ist).

**CPU-Last-Angriff:** Es gibt derzeit einige Methoden für Personen, einen Peer ferngesteuert dazu aufzufordern, kryptographisch aufwändige Operationen durchzuführen, und ein feindlicher Angreifer könnte diese nutzen, um den Peer mit einer großen Anzahl solcher Anfragen zu überlasten und die CPU zu überfordern. Sowohl die Anwendung guter Engineering-Praktiken als auch die potenzielle Anforderung nichttrivialer Zertifikate (z.B. HashCash), die an diese aufwändigen Anfragen angehängt werden, sollten das Problem abmildern, obwohl es möglicherweise Raum für Angreifer gibt, verschiedene Implementierungsfehler auszunutzen.

**Floodfill DOS-Angriff:** Ein böswilliger Benutzer könnte versuchen, dem Netzwerk zu schaden, indem er zu einem floodfill router wird. Die aktuellen Abwehrmaßnahmen gegen unzuverlässige, zeitweilig ausfallende oder bösartige floodfill router sind mangelhaft. Ein floodfill router kann schlechte oder gar keine Antworten auf Anfragen liefern und kann auch die Kommunikation zwischen floodfill routern stören. Einige Abwehrmaßnahmen und Peer-Profiling sind implementiert, jedoch gibt es noch viel zu tun. Für weitere Informationen siehe die [Netzwerkdatenbank-Seite](/docs/specs/common-structures/).

### Tagging-Angriffe

Tagging-Angriffe — die Modifikation einer Nachricht, damit sie später weiter entlang des Pfades identifiziert werden kann — sind in I2P an sich unmöglich, da Nachrichten, die durch tunnel übertragen werden, signiert sind. Wenn jedoch ein Angreifer sowohl das inbound tunnel Gateway als auch ein Teilnehmer weiter entlang in diesem tunnel ist, können sie durch Kollusion die Tatsache identifizieren, dass sie sich im selben tunnel befinden (und vor der Hinzufügung eindeutiger Hop-IDs und anderen Updates konnten kolludierende Peers innerhalb desselben tunnel diese Tatsache ohne Aufwand erkennen). Ein Angreifer in einem outbound tunnel und einem beliebigen Teil eines inbound tunnel kann jedoch nicht kolludieren, da die tunnel-Verschlüsselung die Daten für die inbound und outbound tunnel separat auffüllt und modifiziert. Externe Angreifer können nichts tun, da die Verbindungen verschlüsselt und Nachrichten signiert sind.

### Partitionierungsangriffe

Partitionierungsangriffe — das Finden von Wegen, die Peers in einem Netzwerk zu trennen (technisch oder analytisch) — sind wichtig zu bedenken, wenn man es mit einem mächtigen Gegner zu tun hat, da die Größe des Netzwerks eine Schlüsselrolle bei der Bestimmung Ihrer Anonymität spielt. Technische Partitionierung durch das Kappen von Verbindungen zwischen Peers zur Erstellung fragmentierter Netzwerke wird durch I2Ps integrierte netDb adressiert, die Statistiken über verschiedene Peers führt, um bestehende Verbindungen zu anderen fragmentierten Abschnitten auszunutzen und so das Netzwerk zu heilen. Wenn der Angreifer jedoch alle Verbindungen zu unkontrollierten Peers trennt und das Ziel im Wesentlichen isoliert, wird keine netDb-Heilung das Problem lösen. An diesem Punkt kann der router nur noch hoffen zu bemerken, dass eine erhebliche Anzahl von zuvor zuverlässigen Peers nicht mehr verfügbar geworden ist und den Client darüber informieren, dass er vorübergehend getrennt ist (dieser Erkennungscode ist derzeit nicht implementiert).

Die analytische Partitionierung des Netzwerks durch das Suchen nach Unterschieden im Verhalten von Routern und Zielen und deren entsprechende Gruppierung ist ebenfalls ein sehr mächtiger Angriff. Zum Beispiel wird ein Angreifer, der die Netzwerkdatenbank [aberntet](#harvesting-attacks), wissen, wann ein bestimmtes Ziel 5 eingehende Tunnel in seinem LeaseSet hat, während andere nur 2 oder 3 haben, was dem Gegner ermöglicht, Clients potenziell nach der Anzahl der ausgewählten Tunnel zu partitionieren. Eine weitere Partitionierung ist möglich beim Umgang mit nichttrivialen Verzögerungen und Stapelverarbeitungsstrategien, da die Tunnel-Gateways und die besonderen Hops mit Verzögerungen ungleich null wahrscheinlich hervorstechen werden. Diese Daten sind jedoch nur für diese spezifischen Hops zugänglich, sodass der Angreifer für eine effektive Partitionierung in dieser Hinsicht einen bedeutenden Teil des Netzwerks kontrollieren müsste (und selbst dann wäre das nur eine probabilistische Partitionierung, da er nicht wissen würde, welche anderen Tunnel oder Nachrichten diese Verzögerungen haben).

Wird auch auf der [netDb-Seite](/docs/specs/common-structures/) diskutiert (Bootstrap-Angriff).

### Predecessor-Angriffe

Der Predecessor-Angriff sammelt passiv Statistiken in dem Versuch zu sehen, welche Peers "nah" am Ziel sind, indem er an ihren tunnels teilnimmt und den vorherigen oder nächsten Hop verfolgt (für ausgehende bzw. eingehende tunnels). Im Laufe der Zeit könnte ein Angreifer unter Verwendung einer perfekt zufälligen Stichprobe von Peers und zufälliger Anordnung sehen, welcher Peer statistisch häufiger als "näher" erscheint als die anderen, und dieser Peer wiederum wäre dort, wo sich das Ziel befindet.

I2P vermeidet dies auf vier Arten: Erstens werden die peers, die zur Teilnahme an tunnels ausgewählt werden, nicht zufällig im gesamten Netzwerk gesampelt — sie werden vom peer-Auswahlalgorithmus abgeleitet, der sie in Stufen unterteilt. Zweitens bedeutet bei [strikter Reihenfolge](/docs/specs/tunnel-implementation/#ordering) von peers in einem tunnel die Tatsache, dass ein peer häufiger auftaucht, nicht, dass er die Quelle ist. Drittens können selbst 0-Hop-tunnel mit permutierter tunnel-Länge (standardmäßig nicht aktiviert) plausible Abstreitbarkeit bieten, da die gelegentliche Variation des Gateways wie normale tunnel aussieht. Viertens wird bei eingeschränkten Routen (nicht implementiert) nur der peer mit einer eingeschränkten Verbindung zum Ziel jemals das Ziel kontaktieren, während Angreifer lediglich auf dieses Gateway treffen.

Die aktuelle Tunnel-Aufbaumethode wurde speziell entwickelt, um den Vorgänger-Angriff zu bekämpfen. Siehe auch [den Schnittmengen-Angriff](#intersection-attacks).

Referenzen: [Wright et al. 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf), welches eine Aktualisierung des [Vorgänger-Angriffspapiers von 2004](http://forensics.umass.edu/pubs/wright-tissec.pdf) ist.

### Harvesting-Angriffe

"Harvesting" bedeutet das Zusammenstellen einer Liste von Benutzern, die I2P verwenden. Es kann für rechtliche Angriffe verwendet werden und andere Angriffe unterstützen, indem einfach ein Peer betrieben wird, um zu sehen, mit wem er sich verbindet, und alle Referenzen zu anderen Peers zu sammeln, die gefunden werden können.

I2P selbst ist nicht mit wirksamen Abwehrmechanismen gegen diesen Angriff konzipiert, da es die verteilte Netzwerkdatenbank gibt, die genau diese Informationen enthält. Die folgenden Faktoren erschweren den Angriff in der Praxis etwas:

- Netzwerkwachstum wird es schwieriger machen, einen bestimmten Anteil des Netzwerks zu erlangen
- Floodfill router implementieren Abfragelimits als DOS-Schutz
- Der "Hidden Mode", der verhindert, dass ein router seine Informationen in der netDb veröffentlicht (aber auch verhindert, dass er Daten weiterleitet), wird derzeit nicht weit verbreitet genutzt, könnte aber verwendet werden.

In zukünftigen Implementierungen würden grundlegende und umfassende eingeschränkte Routen die Macht dieses Angriffs reduzieren, da die "versteckten" Peers ihre Kontaktadressen nicht in der netDb veröffentlichen — nur die tunnel, über die sie erreicht werden können (sowie ihre öffentlichen Schlüssel, usw.).

In Zukunft könnten Router GeoIP verwenden, um zu identifizieren, ob sie sich in einem bestimmten Land befinden, wo die Identifikation als I2P-Knoten riskant wäre. In diesem Fall könnte der Router automatisch den versteckten Modus aktivieren oder andere eingeschränkte Routing-Methoden anwenden.

### Identifizierung durch Verkehrsanalyse

Durch die Überwachung des eingehenden und ausgehenden Datenverkehrs eines routers könnte ein böswilliger ISP oder eine staatliche Firewall identifizieren, dass ein Computer I2P ausführt. Wie [oben](#harvesting-attacks) besprochen, ist I2P nicht spezifisch dafür entwickelt, zu verbergen, dass ein Computer I2P ausführt. Jedoch machen mehrere Designentscheidungen im Design der Transportschicht und Protokolle es etwas schwierig, I2P-Datenverkehr zu identifizieren:

- Zufällige Port-Auswahl
- Punkt-zu-Punkt-Verschlüsselung des gesamten Datenverkehrs
- DH-Schlüsselaustausch ohne Protokoll-Bytes oder andere unverschlüsselte konstante Felder
- Gleichzeitige Nutzung von TCP- und UDP-Transporten. UDP kann für manche Deep Packet Inspection (DPI)-Ausrüstung deutlich schwerer zu verfolgen sein.

In naher Zukunft planen wir, Traffic-Analyse-Probleme direkt anzugehen, indem wir die I2P-Transportprotokolle weiter verschleiern, möglicherweise einschließlich:

- Padding auf der Transportschicht zu zufälligen Längen, insbesondere während des Verbindungshandshakes
- Untersuchung von Paketgrößenverteilungs-Signaturen und zusätzliches Padding bei Bedarf
- Entwicklung zusätzlicher Transportmethoden, die SSL oder andere gängige Protokolle nachahmen
- Überprüfung von Padding-Strategien auf höheren Schichten, um zu sehen, wie sie die Paketgrößen auf der Transportschicht beeinflussen
- Überprüfung von Methoden, die von verschiedenen staatlichen Firewalls implementiert werden, um Tor zu blockieren
- Direkte Zusammenarbeit mit DPI- und Verschleierungsexperten

Referenz: [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf)

### Sybil-Angriffe

Sybil beschreibt eine Kategorie von Angriffen, bei denen der Angreifer beliebig große Mengen an kolludierenden Knoten erstellt und die erhöhte Anzahl nutzt, um andere Angriffe zu unterstützen. Wenn beispielsweise ein Angreifer in einem Netzwerk ist, in dem Peers zufällig ausgewählt werden und er eine 80%ige Chance haben möchte, einer dieser Peers zu sein, erstellt er einfach fünfmal so viele Knoten wie im Netzwerk vorhanden sind und würfelt. Wenn Identität kostenlos ist, kann Sybil eine sehr wirkungsvolle Technik für einen mächtigen Angreifer sein. Die primäre Technik, um dies zu adressieren, besteht einfach darin, Identität 'nicht kostenlos' zu machen — [Tarzan](http://www.pdos.lcs.mit.edu/tarzan/) (unter anderen) nutzt die Tatsache, dass IP-Adressen begrenzt sind, während IIP [HashCash](http://www.hashcash.org/) verwendete, um für die Erstellung einer neuen Identität zu 'berechnen'. Wir haben derzeit keine spezielle Technik implementiert, um Sybil zu adressieren, aber wir schließen Platzhalter-Zertifikate in die Datenstrukturen des routers und der Destination ein, die bei Bedarf ein HashCash-Zertifikat mit entsprechendem Wert enthalten können (oder ein anderes Zertifikat, das Knappheit beweist).

Das Erfordernis von HashCash-Zertifikaten an verschiedenen Stellen hat zwei Hauptprobleme:

- Aufrechterhaltung der Rückwärtskompatibilität
- Das klassische HashCash-Problem — die Auswahl von HashCash-Werten, die aussagekräftige Arbeitsnachweise auf High-End-Maschinen darstellen, während sie auf Low-End-Maschinen wie mobilen Geräten noch machbar bleiben.

Verschiedene Beschränkungen der Anzahl von Routern in einem bestimmten IP-Bereich begrenzen die Verwundbarkeit gegenüber Angreifern, die nicht die Möglichkeit haben, Maschinen in mehreren IP-Blöcken zu platzieren. Dies ist jedoch keine sinnvolle Verteidigung gegen einen mächtigen Gegner.

Siehe die [Netzwerkdatenbank-Seite](/docs/specs/common-structures/) für weitere Diskussion zu Sybil-Angriffen.

### Buddy-Erschöpfungsangriffe

(Referenz: [In Search of an Anonymous and Secure Lookup](http://www.eecs.berkeley.edu/~pmittal/publications/nisan-torsk-ccs10.pdf) Abschnitt 5.2)

Indem ein router sich weigert, tunnel-Build-Anfragen zu akzeptieren oder weiterzuleiten, außer an einen kollaborierenden Peer, könnte er sicherstellen, dass ein tunnel vollständig aus seinem Set kollaborierender router gebildet wird. Die Erfolgschancen werden erhöht, wenn es eine große Anzahl kollaborierender router gibt, d.h. ein [Sybil-Angriff](#sybil-attacks). Dies wird etwas durch unsere Peer-Profiling-Methoden gemildert, die zur Überwachung der Leistung von Peers verwendet werden. Dies ist jedoch ein mächtiger Angriff, da die Anzahl der router sich *f* = 0,2 oder 20% bösartigen Knoten nähert, wie in dem Papier spezifiziert. Die bösartigen router könnten auch Verbindungen zum Ziel-router aufrechterhalten und exzellente Weiterleitungsbandbreite für Traffic über diese Verbindungen bereitstellen, in einem Versuch, die vom Ziel verwalteten Profile zu manipulieren und attraktiv zu erscheinen. Weitere Forschung und Abwehrmaßnahmen könnten notwendig sein.

### Kryptographische Angriffe

Wir verwenden starke Kryptographie mit langen Schlüsseln und gehen von der Sicherheit der in I2P verwendeten branchenüblichen kryptographischen Primitive aus. Zu den Sicherheitsfeatures gehören die sofortige Erkennung veränderter Nachrichten entlang des Pfades, die Unmöglichkeit, nicht an Sie adressierte Nachrichten zu entschlüsseln, und der Schutz vor Man-in-the-Middle-Angriffen. Die 2003 gewählten Schlüsselgrößen waren damals recht konservativ und sind immer noch länger als die in [anderen Anonymitätsnetzwerken](https://torproject.org/) verwendeten. Wir denken nicht, dass die aktuellen Schlüssellängen unsere größte Schwachstelle sind, insbesondere bei traditionellen Gegnern unterhalb staatlicher Ebene; Bugs und die geringe Größe des Netzwerks sind viel beunruhigender. Natürlich werden alle kryptographischen Algorithmen irgendwann durch das Aufkommen schnellerer Prozessoren, kryptographische Forschung und Fortschritte bei Methoden wie Rainbow Tables, Clustern von Videospiel-Hardware usw. obsolet. Leider wurde I2P nicht mit einfachen Mechanismen konzipiert, um Schlüssel zu verlängern oder gemeinsame geheime Werte zu ändern, während die Rückwärtskompatibilität erhalten bleibt.

Die Aktualisierung der verschiedenen Datenstrukturen und Protokolle zur Unterstützung längerer Schlüssel wird schließlich angegangen werden müssen, und dies wird ein großes Unterfangen sein, genau wie es auch für [andere](https://torproject.org/) der Fall sein wird. Hoffentlich können wir durch sorgfältige Planung die Störungen minimieren und Mechanismen implementieren, um zukünftige Übergänge zu erleichtern.

In Zukunft werden mehrere I2P-Protokolle und Datenstrukturen das sichere Auffüllen von Nachrichten auf beliebige Größen unterstützen, sodass Nachrichten eine konstante Größe erhalten könnten oder garlic messages zufällig modifiziert werden könnten, sodass einige Cloves scheinbar mehr Subcloves enthalten als sie tatsächlich tun. Im Moment enthalten garlic-, tunnel- und End-to-End-Nachrichten jedoch einfaches zufälliges Padding.

### Floodfill-Anonymitätsangriffe

Zusätzlich zu den [oben](#denial-of-service-attacks) beschriebenen floodfill DOS-Angriffen sind floodfill router aufgrund ihrer Rolle in der netDb und der hohen Kommunikationsfrequenz mit den Teilnehmern einzigartig positioniert, um etwas über Netzwerkteilnehmer zu erfahren. Dies wird etwas gemildert, weil floodfill router nur einen Teil des gesamten Schlüsselraums verwalten und der Schlüsselraum täglich rotiert, wie auf der [network database Seite](/docs/specs/common-structures/) erklärt. Die spezifischen Mechanismen, durch die router mit floodfills kommunizieren, wurden sorgfältig entworfen. Diese Bedrohungen sollten jedoch weiter untersucht werden. Die spezifischen potenziellen Bedrohungen und entsprechenden Abwehrmaßnahmen sind ein Thema für zukünftige Forschung.

### Andere Network Database Angriffe

Ein feindlicher Benutzer könnte versuchen, das Netzwerk zu schädigen, indem er einen oder mehrere floodfill router erstellt und diese so konfiguriert, dass sie schlechte, langsame oder gar keine Antworten liefern. Mehrere Szenarien werden auf der [Netzwerkdatenbank-Seite](/docs/specs/common-structures/) diskutiert.

### Angriffe auf zentrale Ressourcen

Es gibt einige zentralisierte oder begrenzte Ressourcen (einige innerhalb von I2P, einige nicht), die angegriffen oder als Angriffsvektor genutzt werden könnten. Die Abwesenheit von jrandom ab November 2007, gefolgt vom Verlust des i2p.net Hosting-Services im Januar 2008, machte zahlreiche zentralisierte Ressourcen in der Entwicklung und dem Betrieb des I2P-Netzwerks deutlich, von denen die meisten inzwischen verteilt sind. Angriffe auf extern erreichbare Ressourcen beeinträchtigen hauptsächlich die Fähigkeit neuer Benutzer, uns zu finden, nicht den Betrieb des Netzwerks selbst.

- Die Website wird gespiegelt und verwendet DNS Round-Robin für externen öffentlichen Zugriff.
- Router unterstützen jetzt [mehrere externe reseed-Standorte](/docs/overview/faq/#reseed), jedoch könnten mehr reseed-Hosts benötigt werden, und die Behandlung unzuverlässiger oder bösartiger reseed-Hosts könnte verbessert werden.
- Router unterstützen jetzt mehrere Update-Datei-Standorte. Ein bösartiger Update-Host könnte eine riesige Datei liefern; die Größe muss begrenzt werden.
- Router unterstützen jetzt mehrere standardmäßig vertrauenswürdige Update-Signierer.
- Router handhaben jetzt besser mehrere unzuverlässige floodfill-Peers. Bösartige floodfills benötigen weitere Untersuchungen.
- Der Code wird jetzt in einem verteilten Versionskontrollsystem gespeichert.
- Router sind auf einen einzigen News-Host angewiesen, aber es gibt eine fest codierte Backup-URL, die auf einen anderen Host zeigt. Ein bösartiger News-Host könnte eine riesige Datei liefern; die Größe muss begrenzt werden.
- [Benennungssystem-Dienste](/docs/overview/naming/), einschließlich Adressbuch-Abonnement-Anbieter, Add-Host-Dienste und Jump-Dienste, könnten bösartig sein. Erhebliche Schutzmaßnahmen für Abonnements wurden in Version 0.6.1.31 implementiert, mit zusätzlichen Verbesserungen in nachfolgenden Versionen. Jedoch erfordern alle Benennungsdienste ein gewisses Maß an Vertrauen; siehe [die Benennungsseite](/docs/overview/naming/) für Details.
- Wir bleiben abhängig vom DNS-Dienst für i2p2.de; der Verlust davon würde erhebliche Störungen in unserer Fähigkeit verursachen, neue Nutzer anzuziehen, und würde das Netzwerk (kurz- bis mittelfristig) schrumpfen lassen, genau wie der Verlust von i2p.net.

### Entwicklungsangriffe

Diese Angriffe zielen nicht direkt auf das Netzwerk ab, sondern gehen gegen das Entwicklungsteam vor, indem sie entweder rechtliche Hürden für jeden einführen, der zur Entwicklung der Software beiträgt, oder indem sie alle verfügbaren Mittel nutzen, um die Entwickler dazu zu bringen, die Software zu untergraben. Herkömmliche technische Maßnahmen können diese Angriffe nicht abwehren, und wenn jemand das Leben oder die Existenzgrundlage eines Entwicklers bedrohen würde (oder auch nur einen Gerichtsbeschluss zusammen mit einer Schweigeanordnung unter Gefängnisandrohung erlassen würde), hätten wir ein großes Problem.

Jedoch helfen zwei Techniken dabei, sich gegen diese Angriffe zu verteidigen:

- Alle Komponenten des Netzwerks müssen Open Source sein, um Inspektion, Verifikation, Modifikation und Verbesserung zu ermöglichen. Wenn ein Entwickler kompromittiert wird, sollte die Community nach Bemerken eine Erklärung fordern und aufhören, die Arbeit dieses Entwicklers zu akzeptieren. Alle Commits in unser verteiltes Versionskontrollsystem sind kryptographisch signiert, und die Release-Packager verwenden ein Trust-List-System, um Modifikationen auf zuvor genehmigte zu beschränken.
- Entwicklung über das Netzwerk selbst, wodurch Entwickler anonym bleiben können, aber dennoch den Entwicklungsprozess absichern. Die gesamte I2P-Entwicklung kann über I2P erfolgen — mit einem verteilten Versionskontrollsystem, IRC-Chat, öffentlichen Webservern, Diskussionsforen (forum.i2p) und den Software-Distributionsseiten, die alle innerhalb von I2P verfügbar sind.

Wir pflegen auch Beziehungen zu verschiedenen Organisationen, die Rechtsberatung anbieten, falls eine Verteidigung notwendig werden sollte.

### Implementierungsangriffe (Bugs)

So sehr wir uns auch bemühen, die meisten nichttrivialen Anwendungen enthalten Fehler im Design oder in der Implementierung, und I2P ist keine Ausnahme. Es können Bugs vorhanden sein, die ausgenutzt werden könnten, um die Anonymität oder Sicherheit der über I2P laufenden Kommunikation auf unerwartete Weise anzugreifen. Um Angriffen auf das Design oder die verwendeten Protokolle standzuhalten, veröffentlichen wir alle Designs und Dokumentationen und bitten um Überprüfung und Kritik in der Hoffnung, dass viele Augen das System verbessern werden. Wir glauben nicht an Sicherheit durch Verschleierung.

Darüber hinaus wird der Code auf die gleiche Weise behandelt, mit wenig Abneigung gegen die Überarbeitung oder das Verwerfen von etwas, das nicht den Anforderungen des Softwaresystems entspricht (einschließlich der Einfachheit der Modifikation). Die Dokumentation des Designs und der Implementierung des Netzwerks und der Softwarekomponenten ist ein wesentlicher Bestandteil der Sicherheit, da es ohne sie unwahrscheinlich ist, dass Entwickler bereit wären, die Zeit aufzuwenden, um die Software ausreichend zu erlernen, um Schwächen und Fehler zu identifizieren.

Unsere Software enthält wahrscheinlich, insbesondere, Fehler im Zusammenhang mit Denial-of-Service durch Speichererschöpfungsfehler (OOMs), Cross-Site-Scripting (XSS) Problemen in der router-Konsole und anderen Schwachstellen gegenüber nicht-standardisierten Eingaben über die verschiedenen Protokolle.

I2P ist noch immer ein kleines Netzwerk mit einer kleinen Entwicklergemeinschaft und fast keinem Interesse von akademischen oder Forschungsgruppen. Daher fehlt uns die Analyse, die [andere Anonymitätsnetzwerke](https://torproject.org/) möglicherweise erhalten haben. Wir suchen weiterhin Menschen, die sich [beteiligen](/get-involved/) und helfen möchten.

---

## Weitere Abwehrmaßnahmen

### Sperrlisten

In gewissem Maße könnte I2P erweitert werden, um Peers zu vermeiden, die unter IP-Adressen operieren, die in einer Sperrliste aufgeführt sind. Mehrere Sperrlisten sind in Standardformaten verfügbar und listen Anti-P2P-Organisationen, potenzielle staatliche Gegner und andere auf.

Soweit aktive Peers tatsächlich in der eigentlichen Blockliste auftauchen, würde eine Blockierung durch nur eine Teilmenge von Peers dazu neigen, das Netzwerk zu segmentieren, Erreichbarkeitsprobleme zu verschärfen und die Gesamtzuverlässigkeit zu verringern. Daher würden wir uns auf eine bestimmte Blockliste einigen und diese standardmäßig aktivieren wollen.

Sperrlisten sind nur ein Teil (möglicherweise ein kleiner Teil) einer Reihe von Verteidigungsmaßnahmen gegen bösartiges Verhalten. Zum größten Teil leistet das Profiling-System gute Arbeit bei der Messung des router-Verhaltens, sodass wir nichts in der netDb vertrauen müssen. Es gibt jedoch noch mehr, was getan werden kann. Für jeden der Bereiche in der obigen Liste können wir Verbesserungen bei der Erkennung von bösartigem Verhalten vornehmen.

Wenn eine Blocklist an einem zentralen Ort mit automatischen Updates gehostet wird, ist das Netzwerk anfällig für einen [zentralen Ressourcenangriff](#central-resource-attacks). Das automatische Abonnieren einer Liste gibt dem Listenanbieter die Macht, das I2P-Netzwerk komplett abzuschalten.

Derzeit wird eine Standard-Blocklist mit unserer Software verteilt, die nur die IPs vergangener DOS-Quellen auflistet. Es gibt keinen automatischen Update-Mechanismus. Sollte ein bestimmter IP-Bereich ernsthafte Angriffe auf das I2P-Netzwerk durchführen, müssten wir die Benutzer bitten, ihre Blocklist manuell über externe Kommunikationswege wie Foren, Blogs usw. zu aktualisieren.
