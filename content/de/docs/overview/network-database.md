---
title: "Die Network Database"
description: "Verständnis der verteilten Netzwerkdatenbank (netDb) von I2P - eine spezialisierte DHT für router-Kontaktinformationen und Ziel-Lookups"
slug: "network-database"
aliases:
  - "/de/how_networkdatabase"
  - "/de/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Überblick

I2Ps netDb ist eine spezialisierte verteilte Datenbank, die nur zwei Arten von Daten enthält - router-Kontaktinformationen (**RouterInfos**) und Ziel-Kontaktinformationen (**LeaseSets**). Jedes Datenstück wird von der entsprechenden Partei signiert und von jedem, der es verwendet oder speichert, verifiziert. Zusätzlich enthalten die Daten Lebendigkeitsinformationen, die es ermöglichen, irrelevante Einträge zu verwerfen, neuere Einträge durch ältere zu ersetzen und Schutz vor bestimmten Angriffsklassen zu bieten.

Die netDb wird mit einer einfachen Technik namens "floodfill" verteilt, bei der eine Teilmenge aller router, die "floodfill router" genannt werden, die verteilte Datenbank verwaltet.

---

## RouterInfo

Wenn ein I2P router einen anderen router kontaktieren möchte, muss er einige wichtige Daten kennen - die alle vom router in einer Struktur namens "RouterInfo" gebündelt und signiert werden, die mit dem SHA256-Hash der router-Identität als Schlüssel verteilt wird. Die Struktur selbst enthält:

- Die Identität des routers (ein Verschlüsselungsschlüssel, ein Signaturschlüssel und ein Zertifikat)
- Die Kontaktadressen, unter denen er erreicht werden kann
- Wann dies veröffentlicht wurde
- Eine Reihe von beliebigen Textoptionen
- Die Signatur der obigen Angaben, erstellt durch den Signaturschlüssel der Identität

### Erwartete Optionen

Die folgenden Textoptionen sind zwar nicht zwingend erforderlich, sollten aber vorhanden sein:

- **caps** (Capability-Flags - verwendet zur Anzeige der floodfill-Teilnahme, ungefähren Bandbreite und wahrgenommenen Erreichbarkeit)
  - **D**: Mittlere Überlastung (seit Release 0.9.58)
  - **E**: Hohe Überlastung (seit Release 0.9.58)
  - **f**: floodfill
  - **G**: Lehnt alle tunnel ab (seit Release 0.9.58)
  - **H**: Versteckt
  - **K**: Unter 12 KBps geteilte Bandbreite
  - **L**: 12 - 48 KBps geteilte Bandbreite (Standard)
  - **M**: 48 - 64 KBps geteilte Bandbreite
  - **N**: 64 - 128 KBps geteilte Bandbreite
  - **O**: 128 - 256 KBps geteilte Bandbreite
  - **P**: 256 - 2000 KBps geteilte Bandbreite (seit Release 0.9.20, siehe Hinweis unten)
  - **R**: Erreichbar
  - **U**: Nicht erreichbar
  - **X**: Über 2000 KBps geteilte Bandbreite (seit Release 0.9.20, siehe Hinweis unten)

"Geteilte Bandbreite" == (Anteil %) * min(eingehende Bandbreite, ausgehende Bandbreite)

Aus Kompatibilitätsgründen mit älteren Routern kann ein Router mehrere Bandbreiten-Kennbuchstaben veröffentlichen, zum Beispiel "PO".

Hinweis: Die Grenze zwischen den Bandbreitenklassen P und X kann entweder 2000 oder 2048 KBps betragen, je nach Entscheidung des Implementierers.

- **netId** = 2 (Grundlegende Netzwerkkompatibilität - Ein router wird die Kommunikation mit einem Peer verweigern, der eine andere netId hat)
- **router.version** (Wird verwendet, um die Kompatibilität mit neueren Funktionen und Nachrichten zu bestimmen)

Hinweise zu R/U-Fähigkeiten: Ein router sollte normalerweise die R- oder U-Fähigkeit veröffentlichen, es sei denn, der Erreichbarkeitsstatus ist derzeit unbekannt. R bedeutet, dass der router direkt erreichbar ist (keine Introducer erforderlich, nicht durch eine Firewall blockiert) über mindestens eine Transportadresse. U bedeutet, dass der router NICHT direkt erreichbar ist über JEDE Transportadresse.

Veraltete Optionen: - ~~coreVersion~~ (Nie verwendet, entfernt in Release 0.9.24) - ~~stat_uptime~~ = 90m (Nicht verwendet seit Version 0.7.9, entfernt in Release 0.9.24)

Diese Werte werden von anderen Routern für grundlegende Entscheidungen verwendet. Sollen wir uns mit diesem Router verbinden? Sollen wir versuchen, einen Tunnel durch diesen Router zu leiten? Das Bandbreiten-Fähigkeits-Flag wird insbesondere nur dazu verwendet, zu bestimmen, ob der Router einen Mindestgrenzwert für das Routing von Tunneln erfüllt. Oberhalb des Mindestgrenzwerts wird die beworbene Bandbreite nirgendwo im Router verwendet oder vertraut, außer für die Anzeige in der Benutzeroberfläche und für Debugging und Netzwerkanalyse.

Gültige NetID-Nummern:

| Verwendung | NetID-Nummer |
|------------|--------------|
| Reserviert | 0 |
| Reserviert | 1 |
| Aktuelles Netzwerk (Standard) | 2 |
| Reservierte zukünftige Netzwerke | 3 - 15 |
| Forks und Testnetzwerke | 16 - 254 |
| Reserviert | 255 |
### Zusätzliche Optionen

Zusätzliche Textoptionen umfassen eine kleine Anzahl von Statistiken über die Gesundheit des routers, die von Websites wie [stats.i2p](http://stats.i2p/) für Netzwerkleistungsanalyse und Fehlersuche aggregiert werden. Diese Statistiken wurden ausgewählt, um für die Entwickler entscheidende Daten bereitzustellen, wie tunnel-Aufbau-Erfolgsraten, während gleichzeitig der Bedarf an solchen Daten mit den Nebenwirkungen abgewogen wird, die durch die Preisgabe dieser Daten entstehen könnten. Aktuelle Statistiken beschränken sich auf:

- Erfolgs-, Ablehnungs- und Timeout-Raten beim Aufbau explorativer tunnel
- 1-Stunden-Durchschnitt der Anzahl teilnehmender tunnel

Diese sind optional, aber wenn sie enthalten sind, helfen sie bei der Analyse der netzwerkweiten Leistung. Ab API 0.9.58 sind diese Statistiken vereinfacht und standardisiert, wie folgt:

- Optionsschlüssel sind stat_(statistikname).(statistikzeitraum)
- Optionswerte sind durch ';' getrennt
- Statistiken für Ereigniszählungen oder normalisierte Prozentsätze verwenden den 4. Wert; die ersten drei Werte werden nicht verwendet, müssen aber vorhanden sein
- Statistiken für Durchschnittswerte verwenden den 1. Wert, und kein ';'-Trennzeichen ist erforderlich
- Für eine gleichmäßige Gewichtung aller router in der Statistikanalyse und für zusätzliche Anonymität sollten router diese Statistiken nur nach einer Betriebszeit von einer Stunde oder mehr einschließen, und nur einmal alle 16 Mal, wenn die RI veröffentlicht wird.

Beispiel:

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill router können zusätzliche Daten über die Anzahl der Einträge in ihrer Netzwerkdatenbank veröffentlichen. Diese sind optional, helfen aber, wenn sie enthalten sind, bei der Analyse der netzwerkweiten Leistung.

Die folgenden zwei Optionen sollten von floodfill routern in jeder veröffentlichten RI enthalten sein:

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Beispiel:

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Die veröffentlichten Daten können in der Benutzeroberfläche des routers eingesehen werden, werden aber von keinem anderen router verwendet oder als vertrauenswürdig eingestuft.

### Familienoptionen

Ab Version 0.9.24 können Router erklären, dass sie Teil einer "Familie" sind, die von derselben Einrichtung betrieben wird. Mehrere Router derselben Familie werden nicht in einem einzigen Tunnel verwendet.

Die Family-Optionen sind:

- **family** (Der Familienname)
- **family.key** Der Signaturtyp-Code des [Signing Public Key](/docs/specs/common-structures/#type_SigningPublicKey) der Familie (in ASCII-Ziffern) verkettet mit ':' verkettet mit dem Signing Public Key in Base 64
- **family.sig** Die Signatur von ((Familienname in UTF-8) verkettet mit (32 Byte router-Hash)) in Base 64

### RouterInfo-Ablauf

RouterInfos haben keine festgelegte Ablaufzeit. Jeder Router kann seine eigene lokale Richtlinie festlegen, um die Häufigkeit von RouterInfo-Abfragen gegen Speicher- oder Festplattenverbrauch abzuwägen. In der aktuellen Implementierung gibt es die folgenden allgemeinen Richtlinien:

- Es gibt kein Ablaufen während der ersten Betriebsstunde, da die persistent gespeicherten Daten alt sein könnten.
- Es gibt kein Ablaufen, wenn es 25 oder weniger RouterInfos gibt.
- Mit wachsender Anzahl lokaler RouterInfos verkürzt sich die Ablaufzeit, um zu versuchen, eine angemessene Anzahl von RouterInfos zu erhalten. Die Ablaufzeit bei weniger als 120 routern beträgt 72 Stunden, während die Ablaufzeit bei 300 routern etwa 30 Stunden beträgt.
- RouterInfos, die [SSU](/docs/legacy/ssu/) introducers enthalten, laufen in etwa einer Stunde ab, da die introducer-Liste in etwa dieser Zeit abläuft.
- Floodfills verwenden eine kurze Ablaufzeit (1 Stunde) für alle lokalen RouterInfos, da gültige RouterInfos häufig an sie erneut veröffentlicht werden.

### RouterInfo Persistente Speicherung

RouterInfos werden regelmäßig auf die Festplatte geschrieben, damit sie nach einem Neustart verfügbar sind.

Es kann wünschenswert sein, Meta LeaseSets mit langen Ablaufzeiten dauerhaft zu speichern. Dies ist implementierungsabhängig.

### Siehe auch

- [RouterInfo-Spezifikation](/docs/specs/common-structures/#struct_RouterInfo)
- [RouterInfo Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

Das zweite Datenstück, das in der netDb verteilt wird, ist ein "LeaseSet" - das eine Gruppe von **Tunnel-Einstiegspunkten (Leases)** für ein bestimmtes Client-Ziel dokumentiert. Jeder dieser Leases gibt die folgenden Informationen an:

- Der tunnel gateway router (durch Angabe seiner Identität)
- Die tunnel ID auf diesem router zum Senden von Nachrichten (eine 4-Byte-Nummer)
- Wann dieser tunnel ablaufen wird.

Das leaseSet selbst wird in der netDb unter dem Schlüssel gespeichert, der vom SHA256 des Ziels abgeleitet wird. Eine Ausnahme bilden Encrypted LeaseSets (LS2) ab Version 0.9.38. Der SHA256 des Typ-Bytes (3) gefolgt vom blinded public key wird für den DHT-Schlüssel verwendet und dann wie üblich rotiert. Siehe den Abschnitt Kademlia Closeness Metric unten.

Zusätzlich zu diesen Leases enthält das LeaseSet:

- Das Ziel selbst (ein Verschlüsselungsschlüssel, ein Signaturschlüssel und ein Zertifikat)
- Zusätzlicher öffentlicher Verschlüsselungsschlüssel: wird für End-to-End-Verschlüsselung von garlic messages verwendet
- Zusätzlicher öffentlicher Signaturschlüssel: vorgesehen für leaseSet-Widerruf, aber derzeit ungenutzt.
- Signatur aller leaseSet-Daten, um sicherzustellen, dass das Destination das leaseSet veröffentlicht hat.

- [Lease-Spezifikation](/docs/specs/common-structures/#struct_Lease)
- [LeaseSet-Spezifikation](/docs/specs/common-structures/#struct_LeaseSet)
- [Lease Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [LeaseSet Javadoc](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

Ab Version 0.9.38 sind drei neue Arten von LeaseSets definiert: LeaseSet2, MetaLeaseSet und EncryptedLeaseSet. Siehe unten.

### Unveröffentlichte LeaseSets

Ein LeaseSet für ein Ziel, das nur für ausgehende Verbindungen verwendet wird, ist *unveröffentlicht*. Es wird niemals zur Veröffentlichung an einen floodfill router gesendet. "Client"-tunnel, wie sie für Webbrowsing und IRC-Clients verwendet werden, sind unveröffentlicht. Server können dennoch Nachrichten an diese unveröffentlichten Ziele zurücksenden, aufgrund von [I2NP-Speichernachrichten](#leaseset-storage-to-peers).

### Widerrufene LeaseSets

Ein LeaseSet kann *widerrufen* werden, indem ein neues LeaseSet mit null Leases veröffentlicht wird. Widerrufe müssen durch den zusätzlichen Signaturschlüssel im LeaseSet signiert werden. Widerrufe sind nicht vollständig implementiert, und es ist unklar, ob sie einen praktischen Nutzen haben. Dies ist die einzige geplante Verwendung für diesen Signaturschlüssel, daher wird er derzeit nicht verwendet.

### LeaseSet2 (LS2)

Ab Version 0.9.38 unterstützen floodfills eine neue LeaseSet2-Struktur. Diese Struktur ist der alten LeaseSet-Struktur sehr ähnlich und dient demselben Zweck. Die neue Struktur bietet die Flexibilität, die erforderlich ist, um neue Verschlüsselungstypen, mehrere Verschlüsselungstypen, Optionen, Offline-Signaturschlüssel und andere Funktionen zu unterstützen. Siehe Vorschlag 123 für Details.

### Meta LeaseSet (LS2)

Ab Version 0.9.38 unterstützen floodfills eine neue Meta LeaseSet-Struktur. Diese Struktur stellt eine baumähnliche Struktur in der DHT bereit, um auf andere LeaseSets zu verweisen. Mit Meta LeaseSets kann eine Website große multihomed Services implementieren, bei denen mehrere verschiedene Destinations verwendet werden, um einen gemeinsamen Service bereitzustellen. Die Einträge in einem Meta LeaseSet sind Destinations oder andere Meta LeaseSets und können lange Ablaufzeiten haben, bis zu 18,2 Stunden. Mit dieser Funktion sollte es möglich sein, Hunderte oder Tausende von Destinations zu betreiben, die einen gemeinsamen Service hosten. Siehe Vorschlag 123 für Details.

### Verschlüsselte LeaseSets (LS1)

Dieser Abschnitt beschreibt die alte, unsichere Methode zur Verschlüsselung von LeaseSets mit einem festen symmetrischen Schlüssel. Siehe unten für die LS2-Version der verschlüsselten LeaseSets.

In einem *verschlüsselten* LeaseSet sind alle Leases mit einem separaten Schlüssel verschlüsselt. Die Leases können nur entschlüsselt und somit das Ziel nur von denjenigen kontaktiert werden, die den Schlüssel besitzen. Es gibt keine Kennzeichnung oder andere direkte Hinweise darauf, dass das LeaseSet verschlüsselt ist. Verschlüsselte LeaseSets werden nicht weit verbreitet verwendet, und es ist ein Thema für zukünftige Arbeiten zu erforschen, ob die Benutzeroberfläche und Implementierung von verschlüsselten LeaseSets verbessert werden könnte.

### Verschlüsselte LeaseSets (LS2)

Ab Release 0.9.38 unterstützen floodfills eine neue EncryptedLeaseSet-Struktur. Das Destination ist verborgen, und nur ein verblindeter öffentlicher Schlüssel und ein Ablaufzeitpunkt sind für den floodfill sichtbar. Nur diejenigen, die das vollständige Destination besitzen, können die Struktur entschlüsseln. Die Struktur wird an einem DHT-Standort gespeichert, der auf dem Hash des verblindeten öffentlichen Schlüssels basiert, nicht auf dem Hash des Destination. Siehe Vorschlag 123 für Details.

### LeaseSet-Ablauf

Für reguläre LeaseSets ist das Ablaufdatum die Zeit des spätesten Ablaufs ihrer Leases. Für die neuen LeaseSet2-Datenstrukturen wird das Ablaufdatum im Header angegeben. Für LeaseSet2 sollte das Ablaufdatum mit dem spätesten Ablauf seiner Leases übereinstimmen. Für EncryptedLeaseSet und MetaLeaseSet kann das Ablaufdatum variieren, und eine maximale Ablaufzeit könnte durchgesetzt werden - dies ist noch zu bestimmen.

### LeaseSet Persistente Speicherung

Keine dauerhafte Speicherung von LeaseSet-Daten ist erforderlich, da diese so schnell ablaufen. Jedoch kann eine dauerhafte Speicherung von EncryptedLeaseSet- und MetaLeaseSet-Daten mit langen Ablaufzeiten ratsam sein.

### Verschlüsselungsschlüssel-Auswahl (LS2)

LeaseSet2 kann mehrere Verschlüsselungsschlüssel enthalten. Die Schlüssel sind in der Reihenfolge der Server-Präferenz angeordnet, der bevorzugteste zuerst. Das Standard-Client-Verhalten ist, den ersten Schlüssel mit einem unterstützten Verschlüsselungstyp auszuwählen. Clients können andere Auswahlalgorithmen basierend auf Verschlüsselungsunterstützung, relativer Leistung und anderen Faktoren verwenden.

---

## Bootstrapping

Die netDb ist dezentralisiert, jedoch benötigen Sie mindestens eine Referenz zu einem Peer, damit der Integrationsprozess Sie einbindet. Dies wird durch "Reseeding" Ihres routers mit der RouterInfo eines aktiven Peers erreicht - konkret durch das Abrufen ihrer `routerInfo-$hash.dat`-Datei und deren Speicherung in Ihrem `netDb/`-Verzeichnis. Jeder kann Ihnen diese Dateien bereitstellen - Sie können sie sogar anderen zur Verfügung stellen, indem Sie Ihr eigenes netDb-Verzeichnis freigeben. Um den Prozess zu vereinfachen, veröffentlichen Freiwillige ihre netDb-Verzeichnisse (oder eine Teilmenge davon) im regulären (Nicht-I2P) Netzwerk, und die URLs dieser Verzeichnisse sind in I2P fest kodiert. Wenn der router zum ersten Mal startet, lädt er automatisch von einer dieser zufällig ausgewählten URLs herunter.

---

## Floodfill

Die floodfill netDb ist ein einfacher verteilter Speichermechanismus. Der Speicheralgorithmus ist simpel: Sende die Daten an den nächstgelegenen Peer, der sich selbst als floodfill router beworben hat. Wenn der Peer in der floodfill netDb eine netDb-Speicheranfrage von einem Peer erhält, der nicht in der floodfill netDb ist, sendet er sie an eine Teilmenge der floodfill netDb-Peers. Die ausgewählten Peers sind diejenigen, die am nächsten (gemäß der [XOR-Metrik](#kademlia-closeness-metric)) zu einem spezifischen Schlüssel sind.

Die Bestimmung, wer Teil der floodfill netDb ist, ist trivial - dies wird in den veröffentlichten routerInfo-Daten jedes routers als Fähigkeit offengelegt.

Floodfills haben keine zentrale Autorität und bilden keinen "Konsens" - sie implementieren nur ein einfaches DHT-Overlay.

### Floodfill Router Opt-in

Im Gegensatz zu Tor, wo die Directory-Server fest kodiert und vertrauenswürdig sind und von bekannten Entitäten betrieben werden, müssen die Mitglieder des I2P floodfill Peer-Sets nicht vertrauenswürdig sein und ändern sich über die Zeit.

Um die Zuverlässigkeit der netDb zu erhöhen und die Auswirkungen des netDb-Traffics auf einen router zu minimieren, wird floodfill automatisch nur auf routern aktiviert, die mit hohen Bandbreitenlimits konfiguriert sind. Router mit hohen Bandbreitenlimits (die manuell konfiguriert werden müssen, da die Standardeinstellung viel niedriger ist) werden als auf Verbindungen mit niedrigerer Latenz befindlich angenommen und sind eher 24/7 verfügbar. Die aktuelle Mindest-Share-Bandbreite für einen floodfill router beträgt 128 KBytes/sec.

Zusätzlich muss ein router mehrere weitere Tests zur Systemgesundheit bestehen (Warteschlangenzeit für ausgehende Nachrichten, Job-Verzögerung, etc.), bevor der floodfill-Betrieb automatisch aktiviert wird.

Mit den aktuellen Regeln für das automatische Opt-in sind ungefähr 6% der Router im Netzwerk floodfill Router.

Während einige Peers manuell als floodfill konfiguriert werden, sind andere einfach Router mit hoher Bandbreite, die sich automatisch melden, wenn die Anzahl der floodfill Peers unter einen Schwellenwert fällt. Dies verhindert langfristige Netzwerkschäden durch den Verlust der meisten oder aller floodfills durch einen Angriff. Im Gegenzug entziehen sich diese Peers ihre floodfill-Funktion, wenn zu viele floodfills vorhanden sind.

### Floodfill Router-Rollen

Die einzigen zusätzlichen Dienste eines floodfill routers gegenüber nicht-floodfill routern bestehen darin, netDb-Speicherungen zu akzeptieren und auf netDb-Abfragen zu antworten. Da sie im Allgemeinen über hohe Bandbreite verfügen, nehmen sie eher an einer großen Anzahl von tunnels teil (d.h. fungieren als "Relay" für andere), aber dies steht nicht in direktem Zusammenhang mit ihren verteilten Datenbankdiensten.

---

## Kademlia Nähe-Metrik

Die netDb verwendet eine einfache Kademlia-artige XOR-Metrik, um die Nähe zu bestimmen. Um einen Kademlia-Schlüssel zu erstellen, wird der SHA256-Hash der RouterIdentity oder Destination berechnet. Eine Ausnahme bilden Encrypted LeaseSets (LS2) seit Version 0.9.38. Der SHA256 des Type-Bytes (3) gefolgt vom blinded public key wird für den DHT-Schlüssel verwendet und dann wie üblich rotiert.

Eine Modifikation dieses Algorithmus wird vorgenommen, um die Kosten von [Sybil-Angriffen](#sybil-attack-partial-keyspace) zu erhöhen. Anstatt den SHA256-Hash des Schlüssels zu verwenden, der gesucht oder gespeichert wird, wird der SHA256-Hash des 32-Byte binären Suchschlüssels genommen, der mit dem UTC-Datum als 8-Byte ASCII-String yyyyMMdd angehängt wird, d.h. SHA256(key + yyyyMMdd). Dies wird als "routing key" bezeichnet und ändert sich jeden Tag um Mitternacht UTC. Nur der Suchschlüssel wird auf diese Weise modifiziert, nicht die floodfill router Hashes. Die tägliche Transformation der DHT wird manchmal als "keyspace rotation" bezeichnet, obwohl es sich nicht strikt um eine Rotation handelt.

Routing-Schlüssel werden niemals über das Netzwerk in einer I2NP-Nachricht übertragen, sie werden nur lokal zur Bestimmung der Entfernung verwendet.

---

## Network Database Segmentierung - Sub-Databases

Traditionell sind Kademlia-artige DHTs nicht darauf ausgelegt, die Unverknüpfbarkeit von Informationen zu bewahren, die auf einem bestimmten Knoten im DHT gespeichert sind. Zum Beispiel kann eine Information auf einem Knoten im DHT gespeichert und dann bedingungslos von diesem Knoten wieder abgerufen werden. Innerhalb von I2P und unter Verwendung der netDb ist dies nicht der Fall - im DHT gespeicherte Informationen dürfen nur unter bestimmten bekannten Umständen geteilt werden, wenn es "sicher" ist, dies zu tun. Dies soll eine Klasse von Angriffen verhindern, bei denen ein böswilliger Akteur versuchen kann, einen client tunnel mit einem router zu verknüpfen, indem er eine Speicherung an einen client tunnel sendet und diese dann direkt vom vermuteten "Host" des client tunnels wieder anfordert.

### Segmentierungsstruktur

I2P router können wirksame Abwehrmaßnahmen gegen diese Angriffsklasse implementieren, sofern einige Bedingungen erfüllt sind. Eine netDb-Implementierung sollte in der Lage sein, nachzuverfolgen, ob ein Datenbankeintrag über einen Client-Tunnel oder direkt empfangen wurde. Falls er über einen Client-Tunnel empfangen wurde, sollte sie auch nachverfolgen, über welchen Client-Tunnel er empfangen wurde, unter Verwendung des lokalen Ziels des Clients. Falls der Eintrag über mehrere Client-Tunnels empfangen wurde, sollte die netDb alle Ziele nachverfolgen, wo der Eintrag beobachtet wurde. Sie sollte auch nachverfolgen, ob ein Eintrag als Antwort auf eine Suche oder als Speichervorgang empfangen wurde.

In beiden Implementierungen, Java und C++, wird dies erreicht, indem zuerst eine einzige "Main" netDb für direkte Lookups und floodfill-Operationen verwendet wird. Diese Haupt-netDb existiert im router-Kontext. Dann erhält jeder Client seine eigene Version der netDb, die verwendet wird, um Datenbankeinträge zu erfassen, die an Client-tunnels gesendet werden, und um auf Lookups zu antworten, die über Client-tunnels gesendet werden. Wir nennen diese "Client Network Databases" oder "Sub-Databases" und sie existieren im Client-Kontext. Die vom Client betriebene netDb existiert nur für die Lebensdauer des Clients und enthält nur Einträge, die mit den tunnels des Clients kommuniziert werden. Dies macht es unmöglich, dass sich Einträge, die über Client-tunnels gesendet werden, mit Einträgen überschneiden, die direkt an den router gesendet werden.

Zusätzlich muss jede netDb sich merken können, ob ein Datenbankeintrag empfangen wurde, weil er an eines unserer Ziele gesendet wurde, oder weil er von uns als Teil einer Abfrage angefordert wurde. Wenn ein Datenbankeintrag als Store empfangen wurde, also wenn ein anderer router ihn an uns gesendet hat, dann sollte eine netDb auf Anfragen für den Eintrag antworten, wenn ein anderer router den Schlüssel nachschlägt. Wenn er jedoch als Antwort auf eine Abfrage empfangen wurde, dann sollte die netDb nur auf eine Abfrage für den Eintrag antworten, wenn der Eintrag bereits im selben Ziel gespeichert wurde. Ein Client sollte niemals Abfragen mit einem Eintrag aus der Haupt-netDb beantworten, sondern nur aus seiner eigenen Client-Netzwerkdatenbank.

Diese Strategien sollten kombiniert angewendet werden, damit beide zum Einsatz kommen. In Kombination "segmentieren" sie die netDb und sichern sie gegen Angriffe ab.

---

## Speicher-, Verifizierungs- und Nachschlagemechanismen

### RouterInfo-Speicherung an Peers

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages, die die lokale RouterInfo enthalten, werden mit Peers als Teil der Initialisierung einer [NTCP](/docs/specs/ntcp2/)- oder [SSU](/docs/specs/ssu2/)-Transportverbindung ausgetauscht.

### LeaseSet-Speicherung an Peers

[I2NP](/docs/specs/i2np/) DatabaseStoreMessages, die das lokale leaseSet enthalten, werden regelmäßig mit Peers ausgetauscht, indem sie in einer garlic-Nachricht zusammen mit normalem Traffic von der zugehörigen Destination gebündelt werden. Dies ermöglicht es, eine erste Antwort und spätere Antworten an einen entsprechenden Lease zu senden, ohne dass leaseSet-Lookups erforderlich sind oder die kommunizierenden Destinations überhaupt veröffentlichte leaseSets haben müssen.

### Floodfill-Auswahl

Die DatabaseStoreMessage sollte an den floodfill gesendet werden, der dem aktuellen routing key für die RouterInfo oder das LeaseSet, das gespeichert wird, am nächsten ist. Derzeit wird der nächstgelegene floodfill durch eine Suche in der lokalen Datenbank gefunden. Selbst wenn dieser floodfill nicht tatsächlich der nächste ist, wird er ihn "näher" weiterleiten, indem er ihn an mehrere andere floodfills sendet. Dies bietet ein hohes Maß an Fehlertoleranz.

In traditionellem Kademlia würde ein Peer eine "find-closest"-Suche durchführen, bevor er ein Element in der DHT zum nächstgelegenen Ziel einfügt. Da die Verify-Operation dazu neigt, nähere floodfills zu entdecken, falls diese vorhanden sind, wird ein router schnell sein Wissen über die DHT-"Nachbarschaft" für die RouterInfo und LeaseSets verbessern, die er regelmäßig veröffentlicht. Obwohl I2NP keine "find-closest"-Nachricht definiert, kann ein router, falls es notwendig wird, einfach eine iterative Suche nach einem Schlüssel mit dem umgeklappten niedrigstwertigen Bit durchführen (d.h. key ^ 0x01), bis keine näheren Peers in den DatabaseSearchReplyMessages empfangen werden. Dies stellt sicher, dass der wahrhaft nächstgelegene Peer gefunden wird, selbst wenn ein entfernterer Peer das netDb-Element hatte.

### RouterInfo-Speicherung zu Floodfills

Ein router veröffentlicht seine eigene RouterInfo, indem er sich direkt mit einem floodfill router verbindet und ihm eine [I2NP](/docs/specs/i2np/) DatabaseStoreMessage mit einem Reply Token ungleich null sendet. Die Nachricht ist nicht Ende-zu-Ende garlic encrypted, da es sich um eine direkte Verbindung handelt, sodass keine dazwischenliegenden router vorhanden sind (und es auch nicht nötig ist, diese Daten zu verbergen). Der floodfill router antwortet mit einer [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, wobei die Message ID auf den Wert des Reply Token gesetzt wird.

Unter bestimmten Umständen kann ein router die RouterInfo DatabaseStoreMessage auch über einen explorativen tunnel senden; zum Beispiel aufgrund von Verbindungsbeschränkungen, Verbindungsinkompatibilität oder dem Wunsch, die tatsächliche IP vor dem floodfill zu verbergen. Der floodfill akzeptiert eine solche Speicherung möglicherweise nicht bei Überlastung oder basierend auf anderen Kriterien; ob die nicht-direkte Speicherung einer RouterInfo explizit als illegal erklärt werden soll, ist ein Thema für weitere Studien.

### LeaseSet-Speicherung zu Floodfills

Die Speicherung von LeaseSets ist viel sensibler als die von RouterInfos, da ein router sicherstellen muss, dass das LeaseSet nicht mit dem router in Verbindung gebracht werden kann.

Ein router veröffentlicht ein lokales leaseSet, indem er eine [I2NP](/docs/specs/i2np/) DatabaseStoreMessage mit einem Reply Token ungleich null über einen ausgehenden Client-tunnel für diese Destination sendet. Die Nachricht ist Ende-zu-Ende mit garlic encryption verschlüsselt unter Verwendung des Session Key Managers der Destination, um die Nachricht vor dem Endpunkt des ausgehenden tunnels zu verbergen. Der floodfill router antwortet mit einer [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, wobei die Message ID auf den Wert des Reply Tokens gesetzt ist. Diese Nachricht wird an einen der eingehenden tunnels des Clients zurückgesendet.

### Flooding

Wie jeder router verwendet ein floodfill verschiedene Kriterien, um das leaseSet oder RouterInfo zu validieren, bevor es lokal gespeichert wird. Diese Kriterien können adaptiv sein und von den aktuellen Bedingungen abhängen, einschließlich der aktuellen Last, der netDb-Größe und anderen Faktoren. Alle Validierungen müssen vor dem Flooding durchgeführt werden.

Nachdem ein floodfill router eine DatabaseStoreMessage mit einer gültigen RouterInfo oder LeaseSet erhalten hat, die neuer ist als die zuvor in seiner lokalen NetDb gespeicherte, "flutet" er sie. Um einen NetDb-Eintrag zu fluten, sucht er mehrere (derzeit 3) floodfill router, die dem routing key des NetDb-Eintrags am nächsten sind. (Der routing key ist der SHA256-Hash der RouterIdentity oder Destination mit dem angehängten Datum (yyyyMMdd).) Durch das Fluten zu denjenigen, die dem Schlüssel am nächsten sind, und nicht zu sich selbst am nächsten, stellt der floodfill sicher, dass die Speicherung an den richtigen Ort gelangt, auch wenn der speichernde router kein gutes Wissen über die DHT-"Nachbarschaft" für den routing key hatte.

Der floodfill stellt dann eine direkte Verbindung zu jedem dieser Peers her und sendet ihm eine [I2NP](/docs/specs/i2np/) DatabaseStoreMessage mit einem Reply Token von null. Die Nachricht ist nicht end-to-end garlic verschlüsselt, da es sich um eine direkte Verbindung handelt und somit keine zwischenliegenden router vorhanden sind (außerdem besteht keine Notwendigkeit, diese Daten zu verbergen). Die anderen router antworten nicht und leiten die Nachricht nicht weiter, da das Reply Token null ist.

Floodfills dürfen nicht über Tunnel fluten; die DatabaseStoreMessage muss über eine direkte Verbindung gesendet werden.

Floodfills dürfen niemals ein abgelaufenes LeaseSet oder eine RouterInfo übertragen, die vor mehr als einer Stunde veröffentlicht wurde.

### RouterInfo und LeaseSet Lookup

Die [I2NP](/docs/specs/i2np/) DatabaseLookupMessage wird verwendet, um einen netDb-Eintrag von einem floodfill router anzufordern. Lookups werden über einen der ausgehenden exploratory tunnels des routers gesendet. Die Antworten sind so spezifiziert, dass sie über einen der eingehenden exploratory tunnels des routers zurückkehren.

Lookups werden im Allgemeinen parallel an die zwei "guten" (bei denen die Verbindung nicht fehlschlägt) floodfill router gesendet, die dem angeforderten Schlüssel am nächsten sind.

Wenn der Schlüssel lokal vom floodfill router gefunden wird, antwortet er mit einer [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Wenn der Schlüssel nicht lokal vom floodfill router gefunden wird, antwortet er mit einer [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage, die eine Liste anderer floodfill router enthält, die dem Schlüssel nahestehen.

LeaseSet-Abfragen sind seit Release 0.9.5 Ende-zu-Ende garlic encrypted. RouterInfo-Abfragen sind nicht verschlüsselt und daher anfällig für das Ausspähen durch den ausgehenden Endpunkt (OBEP) des Client-tunnels. Dies liegt an den Kosten der ElGamal-Verschlüsselung. Die Verschlüsselung von RouterInfo-Abfragen könnte in einer zukünftigen Version aktiviert werden.

Ab Version 0.9.7 werden Antworten auf eine LeaseSet-Suche (eine DatabaseStoreMessage oder eine DatabaseSearchReplyMessage) verschlüsselt, indem der Sitzungsschlüssel und das Tag in die Suche einbezogen werden. Dies verbirgt die Antwort vor dem eingehenden Gateway (IBGW) des Antworttunnels. Antworten auf RouterInfo-Suchen werden verschlüsselt, wenn wir die Suchverschlüsselung aktivieren.

(Referenz: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Abschnitte 2.2-2.3 für die unten kursiv gedruckten Begriffe)

Aufgrund der relativ geringen Größe des Netzwerks und der Flooding-Redundanz sind Lookups normalerweise O(1) anstatt O(log n). Ein Router kennt sehr wahrscheinlich einen floodfill Router, der nah genug am Schlüssel ist, um die Antwort beim ersten Versuch zu erhalten. In Versionen vor 0.8.9 verwendeten Router eine Lookup-Redundanz von zwei (das heißt, zwei Lookups wurden parallel zu verschiedenen Peers durchgeführt), und weder *rekursives* noch *iteratives* Routing für Lookups war implementiert. Anfragen wurden durch *mehrere Routen gleichzeitig* gesendet, um *die Wahrscheinlichkeit eines Anfragefehlers zu reduzieren*.

Ab Release 0.8.9 sind *iterative Lookups* ohne Lookup-Redundanz implementiert. Dies ist ein effizienterer und zuverlässigerer Lookup, der viel besser funktioniert, wenn nicht alle floodfill-Peers bekannt sind, und beseitigt eine ernste Beschränkung für das Netzwerkwachstum. Während das Netzwerk wächst und jeder router nur eine kleine Teilmenge der floodfill-Peers kennt, werden Lookups O(log n). Auch wenn der Peer keine Referenzen zurückgibt, die näher zum Schlüssel sind, wird der Lookup mit dem nächstnächsten Peer fortgesetzt, für zusätzliche Robustheit und um zu verhindern, dass ein bösartiger floodfill einen Teil des Schlüsselraums in ein schwarzes Loch verwandelt. Lookups werden fortgesetzt, bis ein Gesamt-Lookup-Timeout erreicht wird oder die maximale Anzahl von Peers abgefragt wurde.

*Node-IDs* sind *verifizierbar*, da wir den Router-Hash direkt sowohl als Node-ID als auch als Kademlia-Schlüssel verwenden. Falsche Antworten, die dem Suchschlüssel nicht näher sind, werden generell ignoriert. Bei der aktuellen Größe des Netzwerks hat ein Router *detailliertes Wissen über die Nachbarschaft des Ziel-ID-Raums*.

### RouterInfo Speicher-Verifizierung

Hinweis: Die RouterInfo-Verifizierung ist seit Release 0.9.7.1 deaktiviert, um den in der Arbeit [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf) beschriebenen Angriff zu verhindern. Es ist unklar, ob die Verifizierung so umgestaltet werden kann, dass sie sicher durchgeführt werden kann.

Um zu überprüfen, ob eine Speicherung erfolgreich war, wartet ein router einfach etwa 10 Sekunden und sendet dann eine Abfrage an einen anderen floodfill router, der nah am Schlüssel liegt (aber nicht an den, an den die Speicherung gesendet wurde). Abfragen werden über einen der ausgehenden exploratory tunnels des routers gesendet. Abfragen sind Ende-zu-Ende garlic verschlüsselt, um das Ausspähen durch den outbound endpoint (OBEP) zu verhindern.

### LeaseSet-Speicher-Verifizierung

Um zu überprüfen, ob eine Speicherung erfolgreich war, wartet ein router einfach etwa 10 Sekunden und sendet dann eine Anfrage an einen anderen floodfill router in der Nähe des Schlüssels (aber nicht an den, an den die Speicherung gesendet wurde). Anfragen werden über einen der ausgehenden Client-tunnel für das Ziel des LeaseSet gesendet, das überprüft wird. Um Schnüffelei durch den OBEP des ausgehenden tunnel zu verhindern, sind Anfragen End-to-End garlic encrypted. Die Antworten sind so spezifiziert, dass sie über einen der eingehenden tunnel des Clients zurückkommen.

Ab Release 0.9.7 werden Antworten sowohl für RouterInfo- als auch für LeaseSet-Lookups (eine DatabaseStoreMessage oder eine DatabaseSearchReplyMessage) verschlüsselt, um die Antwort vor dem inbound gateway (IBGW) des Antworttunnels zu verbergen.

### Erkundung

*Exploration* ist eine spezielle Form der netDb-Suche, bei der ein router versucht, neue router kennenzulernen. Dies geschieht, indem er einem floodfill router eine [I2NP](/docs/specs/i2np/) DatabaseLookup Message sendet und nach einem zufälligen Schlüssel sucht. Da diese Suche fehlschlagen wird, würde der floodfill normalerweise mit einer [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage antworten, die Hashes von floodfill routern enthält, die dem Schlüssel nahestehen. Dies wäre nicht hilfreich, da der anfragende router diese floodfills wahrscheinlich bereits kennt, und es wäre unpraktisch, alle floodfill router in das "don't include"-Feld der DatabaseLookup Message einzutragen. Bei einer Exploration-Anfrage setzt der anfragende router ein spezielles Flag in der DatabaseLookup Message. Der floodfill antwortet dann nur mit Nicht-floodfill routern, die dem angeforderten Schlüssel nahestehen.

### Hinweise zu Lookup-Antworten

Die Antwort auf eine Lookup-Anfrage ist entweder eine Database Store Message (bei Erfolg) oder eine Database Search Reply Message (bei Fehlschlag). Die DSRM enthält ein 'from' router hash Feld, um die Quelle der Antwort anzuzeigen; die DSM nicht. Das DSRM 'from' Feld ist nicht authentifiziert und kann gefälscht oder ungültig sein. Es gibt keine anderen Antwort-Tags. Daher ist es bei mehreren parallelen Anfragen schwierig, die Leistung der verschiedenen floodfill router zu überwachen.

---

## MultiHoming

Ziele können gleichzeitig auf mehreren Routern gehostet werden, indem dieselben privaten und öffentlichen Schlüssel verwendet werden (traditionell in eepPriv.dat-Dateien gespeichert). Da beide Instanzen regelmäßig ihre signierten LeaseSets an die floodfill-Peers veröffentlichen, wird das zuletzt veröffentlichte LeaseSet an einen Peer zurückgegeben, der eine Datenbankabfrage stellt. Da LeaseSets eine Lebensdauer von (höchstens) 10 Minuten haben, sollte eine bestimmte Instanz ausfallen, beträgt der Ausfall höchstens 10 Minuten und ist im Allgemeinen viel kürzer. Die Multihoming-Funktion wurde verifiziert und wird von mehreren Diensten im Netzwerk verwendet.

Ab Release 0.9.38 unterstützen floodfills eine neue Meta LeaseSet-Struktur. Diese Struktur bietet eine baumähnliche Struktur in der DHT, um auf andere LeaseSets zu verweisen. Mit Meta LeaseSets kann eine Site große multihomed Services implementieren, bei denen mehrere verschiedene Destinations verwendet werden, um einen gemeinsamen Service bereitzustellen. Die Einträge in einem Meta LeaseSet sind Destinations oder andere Meta LeaseSets und können lange Ablaufzeiten von bis zu 18,2 Stunden haben. Mit dieser Funktion sollte es möglich sein, Hunderte oder Tausende von Destinations zu betreiben, die einen gemeinsamen Service hosten. Siehe Vorschlag 123 für Details.

---

## Bedrohungsanalyse

Wird auch auf der [Seite zum Bedrohungsmodell](/docs/overview/threat-model/#floodfill) besprochen.

Ein feindlich gesinnter Benutzer könnte versuchen, das Netzwerk zu schädigen, indem er einen oder mehrere floodfill router erstellt und diese so konfiguriert, dass sie schlechte, langsame oder gar keine Antworten liefern. Einige Szenarien werden im Folgenden diskutiert.

### Allgemeine Schadensbegrenzung durch Wachstum

Es gibt derzeit etwa 1700 floodfill router im Netzwerk. Die meisten der folgenden Angriffe werden schwieriger oder haben weniger Auswirkungen, je mehr das Netzwerk wächst und die Anzahl der floodfill router zunimmt.

### Allgemeine Risikominderung durch Redundanz

Über Flooding werden alle netDb-Einträge auf den 3 floodfill-Routern gespeichert, die dem Schlüssel am nächsten sind.

### Fälschungen

Alle netdb-Einträge sind von ihren Erstellern signiert, sodass kein router eine RouterInfo oder ein leaseSet fälschen kann.

### Langsam oder reagiert nicht

Jeder Router führt einen erweiterten Statistiksatz im [Peer-Profil](/docs/overview/peer-selection/) für jeden floodfill Router, der verschiedene Qualitätsmetriken für diesen Peer abdeckt. Der Satz umfasst:

- Durchschnittliche Antwortzeit
- Prozentsatz der Anfragen, die mit den angeforderten Daten beantwortet wurden
- Prozentsatz der erfolgreich verifizierten Speicherungen
- Letzte erfolgreiche Speicherung
- Letzte erfolgreiche Suche
- Letzte Antwort

Jedes Mal, wenn ein router bestimmen muss, welcher floodfill router einem Schlüssel am nächsten ist, verwendet er diese Metriken, um zu bestimmen, welche floodfill router "gut" sind. Die Methoden und Schwellenwerte, die zur Bestimmung der "Güte" verwendet werden, sind relativ neu und unterliegen weiterer Analyse und Verbesserung. Während ein völlig nicht reagierender router schnell identifiziert und gemieden wird, können router, die nur manchmal bösartig sind, viel schwieriger zu handhaben sein.

### Sybil-Angriff (Vollständiger Schlüsselraum)

Ein Angreifer kann einen [Sybil-Angriff](https://www.freehaven.net/anonbib/cache/sybil.pdf) durchführen, indem er eine große Anzahl von floodfill routern erstellt, die über den gesamten Schlüsselraum verteilt sind.

(In einem verwandten Beispiel hat ein Forscher kürzlich eine [große Anzahl von Tor-Relays](http://blog.torproject.org/blog/june-2010-progress-report) erstellt.) Falls erfolgreich, könnte dies ein effektiver DOS-Angriff auf das gesamte Netzwerk sein.

Falls die floodfills nicht ausreichend schlecht funktionieren, um anhand der oben beschriebenen Peer-Profil-Metriken als "schlecht" markiert zu werden, ist dies ein schwierig zu handhabendes Szenario. Tors Reaktion kann im Fall von Relays viel wendiger sein, da verdächtige Relays manuell aus dem Konsens entfernt werden können. Einige mögliche Reaktionen für das I2P-Netzwerk sind unten aufgeführt, jedoch ist keine davon vollständig zufriedenstellend:

- Eine Liste schlechter router-Hashes oder IPs zusammenstellen und die Liste über verschiedene Kanäle ankündigen (Konsolen-News, Website, Forum, etc.); Benutzer müssten die Liste manuell herunterladen und zu ihrer lokalen "Blacklist" hinzufügen.
- Alle im Netzwerk bitten, floodfill manuell zu aktivieren (Sybil mit mehr Sybil bekämpfen)
- Eine neue Softwareversion veröffentlichen, die die fest einprogrammierte Liste "schlechter" Einträge enthält
- Eine neue Softwareversion veröffentlichen, die die Peer-Profil-Metriken und Schwellenwerte verbessert, um zu versuchen, die "schlechten" Peers automatisch zu identifizieren.
- Software hinzufügen, die floodfills disqualifiziert, wenn sich zu viele davon in einem einzigen IP-Block befinden
- Eine automatische abonnementbasierte Blacklist implementieren, die von einer einzelnen Person oder Gruppe kontrolliert wird. Dies würde im Wesentlichen einen Teil des Tor-"Consensus"-Modells implementieren. Leider würde es auch einer einzelnen Person oder Gruppe die Macht geben, die Teilnahme bestimmter router oder IPs im Netzwerk zu blockieren oder sogar das gesamte Netzwerk vollständig herunterzufahren oder zu zerstören.

Dieser Angriff wird schwieriger, je größer das Netzwerk wird.

### Sybil-Angriff (Partieller Schlüsselraum)

Ein Angreifer könnte einen [Sybil-Angriff](https://www.freehaven.net/anonbib/cache/sybil.pdf) durchführen, indem er eine kleine Anzahl (8-15) von floodfill-Routern erstellt, die im Schlüsselraum eng beieinander liegen, und die RouterInfos für diese Router weit verbreitet. Dann würden alle Lookups und Speichervorgänge für einen Schlüssel in diesem Schlüsselraum an einen der Router des Angreifers weitergeleitet werden. Falls erfolgreich, könnte dies beispielsweise ein effektiver DOS-Angriff auf eine bestimmte I2P-Site sein.

Da der Schlüsselraum durch den kryptographischen (SHA256) Hash des Schlüssels indiziert wird, muss ein Angreifer eine Brute-Force-Methode verwenden, um wiederholt router hashes zu generieren, bis er genügend hat, die ausreichend nah am Schlüssel liegen. Die dafür erforderliche Rechenleistung, die von der Netzwerkgröße abhängt, ist unbekannt.

Als teilweise Verteidigung gegen diesen Angriff variiert der Algorithmus zur Bestimmung der Kademlia-"Nähe" über die Zeit. Anstatt den Hash des Schlüssels (d.h. H(k)) zur Bestimmung der Nähe zu verwenden, nutzen wir den Hash des Schlüssels, der mit dem aktuellen Datumsstring angehängt wird, d.h. H(k + JJJJMMTT). Eine Funktion namens "routing key generator" macht dies, welche den ursprünglichen Schlüssel in einen "routing key" transformiert. Mit anderen Worten, der gesamte netDb-Schlüsselraum "rotiert" jeden Tag um Mitternacht UTC. Jeder Teilschlüsselraum-Angriff müsste jeden Tag neu generiert werden, denn nach der Rotation wären die angreifenden Router nicht länger nah zum Zielschlüssel oder zueinander.

Dieser Angriff wird schwieriger, je größer das Netzwerk wird. Neueste Forschung zeigt jedoch, dass die Keyspace-Rotation nicht besonders effektiv ist. Ein Angreifer kann zahlreiche router-Hashes im Voraus berechnen, und nur wenige router reichen aus, um einen Teil des Keyspace innerhalb einer halben Stunde nach der Rotation zu "eclipse" (zu verdunkeln).

Eine Folge der täglichen Keyspace-Rotation ist, dass die verteilte Netzwerkdatenbank für einige Minuten nach der Rotation unzuverlässig werden kann -- Lookups schlagen fehl, weil der neue "nächstgelegene" router noch keinen Store erhalten hat. Das Ausmaß des Problems und Methoden zur Schadensbegrenzung (zum Beispiel netDb "Handoffs" um Mitternacht) sind ein Thema für weitere Studien.

### Bootstrap-Angriffe

Ein Angreifer könnte versuchen, neue router in ein isoliertes oder mehrheitlich kontrolliertes Netzwerk zu starten, indem er eine Reseed-Website übernimmt oder die Entwickler dazu bringt, seine Reseed-Website zur fest programmierten Liste im router hinzuzufügen.

Mehrere Schutzmaßnahmen sind möglich und die meisten davon sind geplant:

- Fallback von HTTPS zu HTTP für das Reseeding nicht zulassen. Ein MITM-Angreifer könnte einfach HTTPS blockieren und dann auf HTTP antworten.
- Reseed-Daten im Installer bündeln

Implementierte Schutzmaßnahmen:

- Änderung der Reseed-Aufgabe, um eine Teilmenge von RouterInfos von mehreren Reseed-Sites abzurufen, anstatt nur eine einzige Site zu verwenden
- Erstellung eines netzwerkexternen Reseed-Überwachungsdienstes, der periodisch Reseed-Websites abfragt und überprüft, dass die Daten nicht veraltet oder inkonsistent mit anderen Netzwerkansichten sind
- Seit Release 0.9.14 werden Reseed-Daten in eine signierte ZIP-Datei gebündelt und die Signatur wird beim Download verifiziert. Siehe [die su3-Spezifikation](/docs/specs/updates/#su3) für Details.

### Abfrage-Erfassung

Siehe auch [Lookup](#routerinfo-and-leaseset-lookup) (Referenz: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Abschnitte 2.2-2.3 für die nachfolgend kursiv geschriebenen Begriffe)

Ähnlich wie bei einem Bootstrap-Angriff könnte ein Angreifer, der einen floodfill router verwendet, versuchen, Peers zu einer Teilmenge von Routern zu "lenken", die er kontrolliert, indem er deren Referenzen zurückgibt.

Dies wird wahrscheinlich nicht über Exploration funktionieren, da Exploration eine seltene Aufgabe ist. Router erhalten die Mehrheit ihrer Peer-Referenzen durch normale tunnel-Aufbauaktivitäten. Exploration-Ergebnisse sind im Allgemeinen auf wenige Router-Hashes beschränkt, und jede Exploration-Anfrage wird an einen zufälligen floodfill router gerichtet.

Ab Version 0.8.9 sind *iterative Suchen* implementiert. Für floodfill router-Referenzen, die in einer [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage-Antwort auf eine Suche zurückgegeben werden, werden diese Referenzen verfolgt, wenn sie näher (oder die nächst-näheren) zum Suchschlüssel sind. Der anfragende router vertraut nicht darauf, dass die Referenzen näher zum Schlüssel sind (d.h. sie sind *verifizierbar korrekt*). Die Suche stoppt auch nicht, wenn kein näherer Schlüssel gefunden wird, sondern setzt fort, indem der nächst-näheste Knoten abgefragt wird, bis das Timeout oder die maximale Anzahl von Abfragen erreicht ist. Dies verhindert, dass ein bösartiger floodfill einen Teil des Schlüsselraums in ein schwarzes Loch verwandelt. Außerdem erfordert die tägliche Schlüsselraum-Rotation, dass ein Angreifer eine router info innerhalb der gewünschten Schlüsselraum-Region neu generiert. Dieses Design stellt sicher, dass der in [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) beschriebene Query-Capture-Angriff viel schwieriger wird.

### DHT-basierte Relay-Auswahl

(Referenz: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Abschnitt 3)

Das hat nicht viel mit floodfill zu tun, aber siehe die [Peer-Auswahl-Seite](/docs/overview/peer-selection/) für eine Diskussion der Schwachstellen der Peer-Auswahl für tunnel.

### Informationslecks

(Referenz: [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Abschnitt 3)

Dieses Papier behandelt Schwächen in den "Finger Table" DHT-Lookups, die von Torsk und NISAN verwendet werden. Auf den ersten Blick scheinen diese nicht auf I2P zuzutreffen. Erstens unterscheidet sich die Verwendung von DHT durch Torsk und NISAN erheblich von der in I2P. Zweitens korrelieren I2Ps netDb-Lookups nur lose mit den [Peer-Auswahl](/docs/overview/peer-selection/)- und [tunnel building](/docs/overview/tunnel-routing/)-Prozessen; nur bereits bekannte Peers werden für tunnel verwendet. Außerdem steht die Peer-Auswahl in keinem Zusammenhang mit dem Konzept der DHT-Schlüssel-Nähe.

Einiges davon könnte tatsächlich interessanter werden, wenn das I2P-Netzwerk viel größer wird. Im Moment kennt jeder router einen großen Anteil des Netzwerks, sodass das Nachschlagen einer bestimmten Router Info in der netDb nicht stark darauf hindeutet, dass dieser router zukünftig in einem tunnel verwendet werden soll. Vielleicht ist die Suche korrelierender, wenn das Netzwerk 100-mal größer ist. Natürlich macht ein größeres Netzwerk einen Sybil-Angriff umso schwieriger.

Das allgemeine Problem der DHT-Informationsleckage in I2P bedarf jedoch weiterer Untersuchung. Die floodfill router befinden sich in der Position, Anfragen zu beobachten und Informationen zu sammeln. Sicherlich erwarten wir bei einem Level von *f* = 0,2 (20% böswillige Knoten, wie im Paper spezifiziert), dass viele der Sybil-Bedrohungen, die wir beschreiben ([hier](/docs/overview/threat-model/#sybil), [hier](#sybil-attack-full-keyspace) und [hier](#sybil-attack-partial-keyspace)), aus mehreren Gründen problematisch werden.

---

## Geschichte

[Verschoben zur netDb-Diskussionsseite](/docs/legacy/netdb/).

---

## Zukünftige Arbeiten

Ende-zu-Ende-Verschlüsselung von zusätzlichen netDb-Abfragen und -Antworten.

Bessere Methoden zur Verfolgung von Lookup-Antworten.
