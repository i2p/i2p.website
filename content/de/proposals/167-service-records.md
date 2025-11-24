---
title: "Service Records in LS2"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Closed"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
---

## Status
Genehmigt in der 2. Überprüfung am 2025-04-01; Spezifikationen wurden aktualisiert; noch nicht implementiert.


## Überblick

I2P fehlt ein zentrales DNS-System.
Jedoch ermöglicht das Adressbuch zusammen mit dem b32-Hostname-System
dem Router, vollständige Ziele nachzuschlagen und Lease-Sets abzurufen, die
eine Liste von Gateways und Schlüsseln enthalten, damit Clients eine Verbindung zu diesem Ziel herstellen können.

Somit ähneln Lease-Sets in gewisser Hinsicht einem DNS-Eintrag. Aktuell gibt es jedoch keine Möglichkeit,
herauszufinden, ob dieser Host irgendwelche Dienste unterstützt, entweder an diesem Zielort oder einem anderen,
ähnlich DNS SRV-Einträgen [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

Die erste Anwendung hierfür könnte Peer-to-Peer-E-Mail sein.
Weitere mögliche Anwendungen: DNS, GNS, Key-Server, Zertifizierungsstellen, Zeitserver,
Bittorrent, Kryptowährungen, andere Peer-to-Peer-Anwendungen.


## Verwandte Vorschläge und Alternativen

### Service-Listen

Der LS2-Vorschlag 123 [Prop123](/en/proposals/123-new-netdb-entries/) definierte 'Serviceaufzeichnungen', die anzeigten, dass ein Ziel an einem globalen Dienst teilnimmt. Die Floodfills würden diese Aufzeichnungen
zu globalen 'Service-Listen' zusammenführen.
Dies wurde aufgrund von Komplexität, mangelnder Authentifizierung,
Sicherheits- und Spam-Bedenken nie implementiert.

Dieser Vorschlag unterscheidet sich insofern, als er eine Nachschlagefunktion für einen Dienst für ein bestimmtes Ziel bereitstellt,
nicht einen globalen Pool von Zielen für einen globalen Dienst.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) schlägt vor, dass jeder seinen eigenen DNS-Server betreibt.
Dieser Vorschlag ist komplementär, da wir Serviceaufzeichnungen verwenden könnten, um anzugeben,
dass GNS (oder DNS) unterstützt wird, mit einem standardisierten Dienstnamen "domain" auf Port 53.

### Dot well-known

In [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) wird vorgeschlagen, dass Dienste über eine HTTP-Anfrage
an /.well-known/i2pmail.key nachgeschlagen werden. Dies erfordert, dass jeder Dienst eine zugehörige
Website haben muss, um den Schlüssel zu hosten. Die meisten Benutzer betreiben keine Websites.

Ein Workaround ist, dass wir voraussetzen könnten, dass ein Dienst für eine b32-Adresse tatsächlich
auf dieser b32-Adresse ausgeführt wird. So dass das Suchen nach dem Dienst für example.i2p erfordert,
die HTTP-Abrufung von http://example.i2p/.well-known/i2pmail.key, aber
ein Dienst für aaa...aaa.b32.i2p erfordert diese Abfrage nicht, er kann einfach direkt verbunden werden.

Aber es gibt dort eine Mehrdeutigkeit, weil example.i2p auch durch seinen b32 angesprochen werden kann.

### MX-Einträge

SRV-Einträge sind lediglich eine generische Version von MX-Einträgen für jeden Dienst.
"_smtp._tcp" ist der "MX"-Eintrag.
Es besteht keine Notwendigkeit für MX-Einträge, wenn wir SRV-Einträge haben, und allein MX-Einträge
bieten keinen generischen Eintrag für jeden Dienst.


## Design

Service-Einträge werden im Optionsabschnitt in LS2 [LS2](/en/docs/spec/common-structures/) platziert.
Der LS2-Optionsabschnitt wird derzeit nicht verwendet.
Nicht unterstützt für LS1.
Dies ähnelt dem Tunnelbandbreiten-Vorschlag [Prop168](/en/proposals/168-tunnel-bandwidth/),

der Optionen für Tunnel-Bau-Einträge definiert.

Um eine Dienstadresse für einen bestimmten Hostnamen oder b32 nachzuschlagen, holt der Router die
Lease-Set und schaut den Service-Eintrag in den Eigenschaften nach.

Der Dienst kann auf demselben Ziel wie das LS selbst gehostet werden, oder er kann
einen anderen Hostnamen/b32 referenzieren.

Wenn das Zielziel für den Dienst ein anderes ist, muss das Ziel-LS auch
einen Service-Eintrag enthalten, der auf sich selbst verweist und anzeigt, dass es den Dienst unterstützt.

Das Design erfordert keine spezielle Unterstützung oder Caching oder Änderungen in den Floodfills.
Nur der Lease-Set- Herausgeber und der Client, der einen Service-Eintrag nachschlägt,
müssen diese Änderungen unterstützen.

Kleine I2CP- und SAM-Erweiterungen werden vorgeschlagen, um den Abruf von
Service-Einträgen durch Clients zu erleichtern.



## Spezifikation

### LS2-Option-Spezifikation

LS2-Optionen MÜSSEN nach Schlüssel sortiert sein, damit die Signatur unveränderlich ist.

Definiert wie folgt:

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Der symbolische Name des gewünschten Dienstes. Muss kleingeschrieben sein. Beispiel: "smtp".
  Erlaubte Zeichen sind [a-z0-9-] und dürfen nicht mit einem '-' beginnen oder enden.
  Standardkennungen aus [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) oder Linux /etc/services müssen verwendet werden, wenn dort definiert.
- proto := Das Transportprotokoll des gewünschten Dienstes. Muss kleingeschrieben sein, entweder "tcp" oder "udp".
  "tcp" bedeutet Streaming und "udp" bedeutet beantwortbare Datagramme.
  Protokollindikatoren für rohe Datagramme und datagram2 können später definiert werden.
  Erlaubte Zeichen sind [a-z0-9-] und dürfen nicht mit einem '-' beginnen oder enden.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := Zeit zum Leben, ganzzahlige Sekunden. Positive ganze Zahl. Beispiel: "86400".
  Ein Minimum von 86400 (ein Tag) wird empfohlen, siehe den Abschnitt Empfehlungen unten für Details.
- priority := Die Priorität des Zielhosts, kleinerer Wert bedeutet bevorzugter. Nichtnegative ganze Zahl. Beispiel: "0"
  Nur nützlich, wenn mehr als ein Eintrag, aber erforderlich, auch wenn nur ein Eintrag.
- weight := Ein relatives Gewicht für Einträge mit derselben Priorität. Höherer Wert bedeutet, dass mehr Chancen bestehen, ausgewählt zu werden. Nichtnegative ganze Zahl. Beispiel: "0"
  Nur nützlich, wenn mehr als ein Eintrag, aber erforderlich, auch wenn nur ein Eintrag.
- port := Der I2CP-Port, auf dem der Dienst zu finden ist. Nichtnegative ganze Zahl. Beispiel: "25"
  Port 0 wird unterstützt, aber nicht empfohlen.
- target := Der Hostname oder b32 des Ziels, das den Dienst bereitstellt. Ein gültiger Hostname wie in [NAMING](/en/docs/naming/). Muss klein geschrieben sein.
  Beispiel: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" oder "example.i2p".
  b32 wird empfohlen, es sei denn, der Hostname ist "gut bekannt", d.h. in offiziellen oder Standard-Adressbüchern.
- appoptions := beliebiger Text, der speziell für die Anwendung ist, darf kein " " oder "," enthalten. Die Kodierung erfolgt in UTF-8.

### Beispiele


In LS2 für aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, zeigt auf einen SMTP-Server:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

In LS2 für aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, zeigt auf zwei SMTP-Server:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

In LS2 für bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, zeigt auf sich selbst als SMTP-Server:

"_smtp._tcp" "0 999999 25"

Mögliches Format für das Weiterleiten von E-Mails (siehe unten):

"_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Grenzen


Das für LS2-Optionen verwendete Mapping-Datenstrukturformat begrenzt Schlüssel und Werte auf maximal 255 Byte (nicht Zeichen).
Mit einem b32-Ziel beträgt der optionvalue etwa 67 Byte, sodass nur 3 Einträge passen würden.
Vielleicht nur einer oder zwei mit einem langen appoptions-Feld oder bis zu vier oder fünf mit einem kurzen Hostnamen.
Dies sollte ausreichend sein; mehrere Einträge sollten selten sein.


### Unterschiede zu [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Keine abschließenden Punkte
- Kein Name nach dem Protokoll
- Kleinschreibung erforderlich
- Im Textformat mit durch Kommas getrennten Einträgen, nicht im binären DNS-Format
- Unterschiedliche Eintragstyp-Indikatoren
- Zusätzlicher appoptions-Feld


### Hinweise


Kein Wildcarding wie (Sternchen), (Sternchen)._tcp oder _tcp ist erlaubt.
Jeder unterstützte Dienst muss seinen eigenen Eintrag haben.



### Dienstnamen-Registry

Nicht standardisierte Kennungen, die nicht in [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) oder Linux /etc/services aufgelistet sind,
können angefordert und zur gemeinsamen Strukturspezifikation [LS2](/en/docs/spec/common-structures/) hinzugefügt werden.

Anwendungsspezifische Appoptions-Formate können dort ebenfalls hinzugefügt werden.


### I2CP-Spezifikation

Das [I2CP](/en/docs/spec/i2cp/) Protokoll muss erweitert werden, um Dienstabfragen zu unterstützen.
Zusätzliche MessageStatusMessage und/oder HostReplyMessage-Fehlercodes im Zusammenhang mit Dienstabfragen sind erforderlich.
Um die Nachschlagefunktion allgemein zu gestalten, nicht nur dienstaufzeichnungsspezifisch,
ist das Design so ausgelegt, dass der Abruf aller LS2-Optionen unterstützt wird.

Implementierung: Erweiterung von HostLookupMessage zur Aufnahme der Anfrage für
LS2-Optionen für Hash, Hostname und Ziel (Anfragetypen 2-4).
Erweiterung von HostReplyMessage zur Aufnahme der Optionen-Mapping, wenn angefordert.
Erweiterung von HostReplyMessage mit zusätzlichen Fehlercodes.

Options-Mappings können für kurze Zeit auf der Client- oder Routerseite, je nach Implementierung, zwischengespeichert oder negativ zwischengespeichert werden. Empfohlene maximale Zeit beträgt eine Stunde, es sei denn, die TTL der Serviceaufzeichnung ist kürzer.
Die Service-Aufzeichnungen können bis zur von der Anwendung, dem Client oder dem Router angegebenen TTL zwischengespeichert werden.

Erweiterung der Spezifikation wie folgt:

### Konfigurationsoptionen


Hinzufügen des folgenden zu [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Optionen, die in die Lease-Set aufgenommen werden sollen. Nur für LS2 verfügbar.
nnn beginnt mit 0. Optionen-Wert enthält "key=value".
(Einschließlich der Anführungszeichen nicht einschließen)

Beispiel:
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### HostLookup-Nachricht


- Nachschlagetyp 2: Hash-Nachschlage, Anforderung des Options-Mappings
- Nachschlagetyp 3: Hostnamen-Nachschlage, Anforderung des Options-Mappings
- Nachschlagetyp 4: Ziel-Nachschlage, Anforderung des Options-Mappings

Für Nachschlagetyp 4 ist Element 5 ein Ziel.



HostReply-Nachricht
 ```````````````````

Für Nachschlagetypen 2-4 muss der Router das Lease-Set abrufen,
auch wenn der Nachschlaageschlüssel im Adressbuch vorhanden ist.

Wenn erfolgreich, enthält die HostReply die Optionen-Mapping
aus dem Lease-Set und schließt sie als Element 5 nach dem Ziel ein.
Wenn keine Optionen im Mapping vorhanden sind oder das Lease-Set Version 1 war,
wird es dennoch als leeres Mapping enthalten (zwei Bytes: 0 0).
Alle Optionen aus dem Lease-Set werden inkludiert, nicht nur die Service-Eintragsoptionen.
Beispielsweise können Optionen für in der Zukunft definierte Parameter vorhanden sein.

Bei einem Fehler beim Nachschlagen des Lease-Sets enthält die Antwort einen neuen Fehlercode 6 (Fehler beim Nachsuchen des Lease-Sets) und wird kein Mapping enthalten.
Wenn Fehlercode 6 zurückgegeben wird, kann das Feld "Ziel" vorhanden sein oder nicht.
Es wird vorhanden sein, wenn ein Hostnamen-Nachschlage im Adressbuch erfolgreich war,
oder wenn ein früheres Nachschlage erfolgreich war und das Ergebnis zwischengespeichert wurde,
oder wenn das Ziel im Lookup-Messag vorhanden war (Nachschlagetyp 4).

Wenn ein Nachschlagetyp nicht unterstützt wird,
enthält die Antwort einen neuen Fehlercode 7 (Nachschlagetyp nicht unterstützt).



### SAM-Spezifikation

Das [SAMv3](/en/docs/api/samv3/) Protokoll muss erweitert werden, um Dienstabfragen zu unterstützen.

NAMING LOOKUP wie folgt erweitern:

NAMING LOOKUP NAME=example.i2p OPTIONS=true fordert das Options-Mapping in der Antwort an.

NAME kann ein vollständiges base64-Ziel sein, wenn OPTIONS=true.

Wenn das Ziel-Nachschlage erfolgreich war und Optionen im Lease-Set vorhanden waren,
dann folgen in der Antwort nach dem Ziel
eine oder mehrere Optionen in der Form von OPTION:key=value.
Jede Option wird ein separates OPTION: Präfix haben.
Alle Optionen aus dem Lease-Set werden inkludiert, nicht nur die Service-Eintragsoptionen.
Beispielsweise können Optionen für in der Zukunft definierte Parameter vorhanden sein.
Beispiel:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Schlüssel, die '=' enthalten, sowie Schlüssel oder Werte, die einen Zeilenumbruch enthalten,
gelten als ungültig und das Schlüssel/Wert-Paar wird aus der Antwort entfernt.

Wenn keine Optionen im Lease-Set gefunden werden oder wenn das Lease-Set Version 1 war,
wird die Antwort keine Optionen enthalten.

Wenn OPTIONS=true in der Nachschlage enthalten war und das Lease-Set nicht gefunden wird, wird ein neuer Ergebniswert LEASESET_NOT_FOUND zurückgegeben.


## Alternative zum Naming-Lookup

Ein alternatives Design wurde erwogen, um die Nachschlage von Diensten
als vollständigen Hostnamen zu unterstützen, zum Beispiel _smtp._tcp.example.i2p,
durch Aktualisieren von [NAMING](/en/docs/naming/) zur Spezifikation der Behandlung von Hostnamen, die mit '_' beginnen.
Dies wurde aus zwei Gründen abgelehnt:

- I2CP- und SAM-Änderungen wären dennoch notwendig, um die TTL- und Port-Informationen an den Client weiterzugeben.
- Es wäre keine allgemeine Funktion, die verwendet werden könnte, um andere LS2
  Optionen abzurufen, die in der Zukunft definiert werden könnten.


## Empfehlungen

Server sollten eine TTL von mindestens 86400 angeben und den Standard-Port für die Anwendung.



## Erweiterte Funktionen

### Rekursive Nachschlagen

Es könnte wünschenswert sein, rekursive Nachschlagen zu unterstützen, bei denen jedes aufeinanderfolgende Lease-Set
auf einen Service-Eintrag überprüft wird, der auf ein anderes Lease-Set verweist, DNS-Stil.
Dies ist wahrscheinlich nicht notwendig, zumindest in einer ersten Implementierung.

TODO



### Anwendungsspezifische Felder

Es könnte wünschenswert sein, anwendungsspezifische Daten im Service-Eintrag zu haben.
Zum Beispiel könnte der Betreiber von example.i2p wünschen, dass E-Mail an example@mail.i2p weitergeleitet wird. Der "example@"-Teil müsste in einem separaten Feld des Service-Eintrags sein oder vom Ziel entfernt werden.

Auch wenn der Betreiber seinen eigenen E-Mail-Dienst betreibt, möchte er vielleicht angeben, dass
E-Mail an example@example.i2p gesendet werden sollte. Die meisten I2P-Dienste werden von einer einzelnen Person betrieben.
Ein separates Feld könnte hier ebenfalls nützlich sein.

TODO wie man dies auf generische Weise macht


### Erforderliche Änderungen für E-Mails

Nicht im Umfang dieses Vorschlags. Siehe [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) für eine Diskussion.


## Implementierungsnotizen

Caching von Service-Einträgen bis zur TTL kann vom Router oder der Anwendung vorgenommen werden,
je nach Implementierung. Ob persistent zwischengespeichert wird, ist ebenfalls implementierungsabhängig.

Abfragen müssen auch das Ziel-Leaseset nachschlagen und verifizieren, dass es einen "self"-Eintrag
enthält, bevor das Zielziel an den Client zurückgegeben wird.


## Sicherheitsanalyse

Da das Lease-Set signiert ist, werden alle darin enthaltenen Service-Einträge durch den Signaturschlüssel des Ziels authentifiziert.

Die Service-Einträge sind öffentlich und für Floodfills sichtbar, es sei denn, das Lease-Set wird verschlüsselt.
Jeder Router, der das Lease-Set anfordert, kann die Service-Einträge sehen.

Ein anderer SRV-Eintrag als "self" (d.h. ein Eintrag, der auf ein anderes Hostnamen/b32-Ziel verweist)
erfordert nicht die Zustimmung des anvisierten Hostnamen/b32.
Es ist nicht klar, ob eine Umleitung eines Dienstes zu einem beliebigen Ziel eine Art von
Angriff erleichtern könnte oder was der Zweck eines solchen Angriffs sein würde.
Dieser Vorschlag mildert jedoch einen solchen Angriff, indem er erfordert, dass das Ziel
auch einen "self"-SRV-Eintrag veröffentlicht. Implementierer müssen nach einem "self"-Eintrag
im Leaseset des Zieles suchen.


## Kompatibilität

LS2: Keine Probleme. Alle bekannten Implementierungen ignorieren derzeit das Optionsfeld in LS2,
und überspringen korrekt ein nicht leeres Optionsfeld.
Dies wurde in Tests sowohl von Java I2P als auch von i2pd während der Entwicklung von LS2 verifiziert.
LS2 wurde 0.9.38 im Jahr 2016 implementiert und wird von allen Router-Implementierungen gut unterstützt.
Das Design erfordert keine spezielle Unterstützung oder Caching oder Änderungen in den Floodfills.

Naming: '_' ist kein gültiges Zeichen in i2p-Hostnamen.

I2CP: Abfragetypen 2-4 sollten nicht an Router unterhalb der minimalen API-Version
gesendet werden, bei der es unterstützt wird (TBD).

SAM: Der Java SAM-Server ignoriert zusätzliche Schlüssel/Werte wie OPTIONS=true.
i2pd sollte dies ebenfalls tun, muss noch verifiziert werden.
SAM-Clients erhalten die zusätzlichen Werte in der Antwort nur, wenn sie mit OPTIONS=true angefordert werden.
Ein Versionssprung sollte nicht notwendig sein.


