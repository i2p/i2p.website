---
title: "Software Update Spezifikation"
description: "Spezifikation für den I2P Software-Update-Mechanismus, SU3-Dateiformat und News-Feed"
slug: "updates"
aliases:
  - "/de/updates"
  - "/de/updates/"
category: "Design"
lastUpdated: "2025-04"
accurateFor: "0.9.65"
---

## Überblick

I2P verwendet ein einfaches, aber sicheres System für automatische Software-Updates. Die router-Konsole lädt regelmäßig eine Nachrichtendatei von einer konfigurierbaren I2P-URL herunter. Es gibt eine fest codierte Backup-URL, die auf die Projekt-Website zeigt, falls der Standard-Nachrichten-Host des Projekts ausfällt.

Der Inhalt der Nachrichtendatei wird auf der Startseite der router-Konsole angezeigt. Zusätzlich enthält die Nachrichtendatei die neueste Versionsnummer der Software. Wenn die Version höher als die Versionsnummer des routers ist, wird dem Benutzer eine Anzeige eingeblendet, dass ein Update verfügbar ist.

Der Router kann optional die neue Version herunterladen oder herunterladen und installieren, wenn er entsprechend konfiguriert ist.

## Alte News-Datei-Spezifikation

Dieses Format wird ab Version 0.9.17 durch das su3-News-Format ersetzt.

Die news.xml-Datei kann die folgenden Elemente enthalten:

```
<i2p.news date="$Date: 2010-01-22 00:00:00 $" />
<i2p.release version="0.7.14" date="2010/01/22" minVersion="0.6" />
```
Die Parameter im i2p.release-Eintrag sind wie folgt. Alle Schlüssel sind nicht case-sensitiv. Alle Werte müssen in Anführungszeichen eingeschlossen werden.

**date** : Das Veröffentlichungsdatum der Router-Version. Nicht verwendet. Format nicht spezifiziert.

**minJavaVersion** : Die mindestens erforderliche Java-Version zum Ausführen der aktuellen Version. Seit Release 0.9.9.

**minVersion** : Die minimal erforderliche router-Version für ein Update auf die aktuelle Version. Wenn ein router älter ist, muss der Benutzer zunächst (manuell?) auf eine Zwischenversion aktualisieren. Ab Version 0.9.9.

**su3Clearnet** : Eine oder mehrere HTTP-URLs, unter denen die .su3-Update-Datei im Clearnet (nicht-I2P) zu finden ist. Mehrere URLs müssen durch ein Leerzeichen oder Komma getrennt werden. Ab Version 0.9.9.

**su3SSL** : Eine oder mehrere HTTPS-URLs, wo die .su3-Update-Datei im Clearnet (nicht-I2P) gefunden werden kann. Mehrere URLs müssen durch ein Leerzeichen oder Komma getrennt werden. Seit Release 0.9.9.

**sudTorrent** : Der Magnet-Link für den .sud (non-pack200) Torrent des Updates. Ab Release 0.9.4.

**su2Torrent** : Der Magnet-Link für den .su2 (pack200) Torrent des Updates. Ab Release 0.9.4.

**su3Torrent** : Der Magnet-Link für den .su3 (neues Format) Torrent des Updates. Seit Version 0.9.9.

**version** : Erforderlich. Die neueste verfügbare aktuelle router-Version.

Die Elemente können innerhalb von XML-Kommentaren eingefügt werden, um eine Interpretation durch Browser zu verhindern. Das i2p.release Element und die Version sind erforderlich. Alle anderen sind optional. HINWEIS: Aufgrund von Parser-Einschränkungen muss ein vollständiges Element auf einer einzigen Zeile stehen.

## Update-Datei-Spezifikation

Ab Release 0.9.9 wird die signierte Update-Datei mit dem Namen i2pupdate.su3 das unten spezifizierte "su3"-Dateiformat verwenden. Genehmigte Release-Signierer werden 4096-Bit-RSA-Schlüssel verwenden. Die X.509-Public-Key-Zertifikate für diese Signierer werden in den Router-Installationspaketen verteilt. Die Updates können Zertifikate für neue, genehmigte Signierer enthalten und/oder eine Liste von Zertifikaten zum Löschen zwecks Widerruf enthalten.

## Alte Update-Datei-Spezifikation

Dieses Format ist seit Version 0.9.9 veraltet.

Die signierte Update-Datei, traditionell i2pupdate.sud genannt, ist einfach eine Zip-Datei mit einem vorangestellten 56-Byte-Header. Der Header enthält:

- Eine 40-Byte DSA [Signature](/docs/specs/common-structures#signature)
- Eine 16-Byte I2P-Version in UTF-8, bei Bedarf mit nachfolgenden Nullen aufgefüllt

Die Signatur deckt nur das Zip-Archiv ab - nicht die vorangestellte Version. Die Signatur muss mit einem der DSA [SigningPublicKey](/docs/specs/common-structures#signingpublickey) übereinstimmen, die im router konfiguriert sind, welcher eine fest kodierte Standardliste von Schlüsseln der aktuellen Projekt-Release-Manager hat.

Für Versionenvergleichszwecke enthalten Versionsfelder [0-9]*, Feldtrennzeichen sind '-', '_' und '.', und alle anderen Zeichen werden ignoriert.

Ab Version 0.8.8 muss die Version auch als Zip-Datei-Kommentar in UTF-8 angegeben werden, ohne die nachfolgenden Nullen. Der aktualisierende Router überprüft, dass die Version im Header (die nicht von der Signatur abgedeckt ist) mit der Version im Zip-Datei-Kommentar übereinstimmt, der von der Signatur abgedeckt ist. Dies verhindert die Fälschung der Versionsnummer im Header.

## Download und Installation

Der router lädt zunächst den Header der Update-Datei von einer konfigurierbaren Liste von I2P-URLs herunter, verwendet dabei den eingebauten HTTP-Client und Proxy, und überprüft, dass die Version neuer ist. Dies verhindert das Problem von Update-Hosts, die nicht die neueste Datei haben. Der router lädt dann die vollständige Update-Datei herunter. Der router überprüft, dass die Update-Datei-Version vor der Installation neuer ist. Er überprüft natürlich auch die Signatur und stellt sicher, dass der Zip-Datei-Kommentar mit der Header-Version übereinstimmt, wie oben erklärt.

Die Zip-Datei wird extrahiert und als "i2pupdate.zip" in das I2P-Konfigurationsverzeichnis (~/.i2p unter Linux) kopiert.

Ab Release 0.7.12 unterstützt der router Pack200-Dekompression. Dateien innerhalb des Zip-Archivs mit der Endung .jar.pack oder .war.pack werden transparent zu einer .jar- oder .war-Datei dekomprimiert. Update-Dateien, die .pack-Dateien enthalten, werden traditionell mit der Endung '.su2' benannt. Pack200 verkleinert die Update-Dateien um etwa 60%.

Ab Release 0.8.7 löscht der router die Dateien libjbigi.so und libjcpuid.so, wenn das ZIP-Archiv eine lib/jbigi.jar-Datei enthält, damit die neuen Dateien aus jbigi.jar extrahiert werden.

Ab Release 0.8.12 löscht der router die dort aufgelisteten Dateien, wenn das Zip-Archiv eine Datei deletelist.txt enthält. Das Format ist:

- Ein Dateiname pro Zeile
- Alle Dateinamen sind relativ zum Installationsverzeichnis; keine absoluten Dateinamen erlaubt, keine Dateien, die mit ".." beginnen
- Kommentare beginnen mit '#'

Der router löscht dann die Datei deletelist.txt.

## SU3 Datei-Spezifikation

Diese Spezifikation wird für router-Updates ab Version 0.9.9, für reseed-Daten ab Version 0.9.14, für Plugins ab Version 0.9.15 und für die News-Datei ab Version 0.9.17 verwendet.

### Probleme mit dem vorherigen .sud/.su2-Format

- Keine magische Nummer oder Flags
- Keine Möglichkeit, Kompression, pack200 oder nicht, oder Signatur-Algorithmus anzugeben
- Version ist nicht von der Signatur abgedeckt, daher wird sie durchgesetzt, indem sie im Zip-Datei-Kommentar (für router-Dateien) oder in der plugin.config-Datei (für Plugins) stehen muss
- Unterzeichner nicht spezifiziert, daher muss der Verifizierer alle bekannten Schlüssel ausprobieren
- Signatur-vor-Daten-Format erfordert zwei Durchgänge zur Dateierzeugung

### Ziele

- Behebe die oben genannten Probleme
- Migration zu einem sichereren Signaturalgorithmus
- Versionsinformationen im gleichen Format und Offset beibehalten für Kompatibilität mit bestehenden Versionsprüfern
- Einstufige Signaturverifikation und Dateiextraktion

### Spezifikation

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0-5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic number "I2Psu3"</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">su3 file format version = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8-9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature type: 0x0000 = DSA-SHA1, 0x0001 = ECDSA-SHA256-P256, 0x0002 = ECDSA-SHA384-P384, 0x0003 = ECDSA-SHA512-P521, 0x0004 = RSA-SHA256-2048, 0x0005 = RSA-SHA384-3072, 0x0006 = RSA-SHA512-4096, 0x0008 = EdDSA-SHA512-Ed25519ph</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10-11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature length, e.g. 40 (0x0028) for DSA-SHA1. Must match that specified for the <a href="/docs/specs/common-structures#signature">Signature</a> type.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version length (in bytes not chars, including padding), must be at least 16 (0x10) for compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID length (in bytes not chars)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16-23</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content length (not including header or sig)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">File type: 0x00 = zip file, 0x01 = xml file (0.9.15), 0x02 = html file (0.9.17), 0x03 = xml.gz file (0.9.17), 0x04 = txt.gz file (0.9.28), 0x05 = dmg file (0.9.51), 0x06 = exe file (0.9.51)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">27</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content type: 0x00 = unknown, 0x01 = router update, 0x02 = plugin or plugin update, 0x03 = reseed data, 0x04 = news feed (0.9.15), 0x05 = blocklist feed (0.9.28)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">28-39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">unused = 0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40-55+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version, UTF-8 padded with trailing 0x00, 16 bytes minimum, length specified at byte 13. Do not append 0x00 bytes if the length is 16 or more.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ID of signer, (e.g. "zzz@mail.i2p") UTF-8, not padded, length specified at byte 15</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content: Length specified in header at bytes 16-23, Format specified in header at byte 25, Content specified in header at byte 27</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">xx+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature: Length is specified in header at bytes 10-11, covers everything starting at byte 0</td>
    </tr>
  </tbody>
</table>
Alle nicht verwendeten Felder müssen für Kompatibilität mit zukünftigen Versionen auf 0 gesetzt werden.

### Signatur-Details

Die Signatur umfasst den gesamten Header beginnend bei Byte 0 bis zum Ende des Inhalts. Wir verwenden rohe Signaturen. Nehmen Sie den Hash der Daten (unter Verwendung des Hash-Typs, der durch den Signaturtyp bei den Bytes 8-9 impliziert wird) und übergeben Sie diesen an eine "rohe" Signatur- oder Verifizierungsfunktion (z.B. "NONEwithRSA" in Java).

Obwohl Signaturverifikation und Inhaltsextraktion in einem Durchgang implementiert werden können, muss eine Implementierung die ersten 10 Bytes lesen und puffern, um den Hash-Typ zu bestimmen, bevor die Verifikation gestartet wird.

Signaturlängen für die verschiedenen Signaturtypen sind in der [Signature](/docs/specs/common-structures#signature) Spezifikation angegeben. Fülle die Signatur bei Bedarf mit führenden Nullen auf. Siehe die [Kryptographie-Details-Seite](/docs/specs/cryptography#sig) für Parameter der verschiedenen Signaturtypen.

### Notizen

Der Inhaltstyp spezifiziert die Vertrauensdomäne. Für jeden Inhaltstyp verwalten Clients eine Sammlung von X.509-Public-Key-Zertifikaten für Parteien, denen vertraut wird, diesen Inhalt zu signieren. Nur Zertifikate für den angegebenen Inhaltstyp dürfen verwendet werden. Das Zertifikat wird über die ID des Signierers gesucht. Clients müssen verifizieren, dass der Inhaltstyp dem für die Anwendung erwarteten entspricht.

Alle Werte sind in Netzwerk-Byte-Reihenfolge (Big Endian).

Für eine Python-Implementierung von Raw RSA-Signaturen, die mit Java "NONEwithRSA" kompatibel ist, siehe [diesen Stack Overflow-Artikel](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530).

## SU3 Router Update Datei Spezifikation

### SU3 Details

- SU3 Content Type: 1 (ROUTER UPDATE)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Die Router-Version

Jar- und War-Dateien in der Zip-Datei werden nicht mehr mit pack200 komprimiert, wie oben für "su2"-Dateien dokumentiert, da aktuelle Java-Laufzeitumgebungen dies nicht mehr unterstützen.

### Notizen

- Für Releases ist die SU3-Version die "Basis"-router-Version, z.B. "0.9.20".
- Für Entwicklungsbuilds, die ab Release 0.9.20 unterstützt werden, ist die SU3-Version die "vollständige" router-Version, z.B. "0.9.20-5" oder "0.9.20-5-rc". Siehe RouterVersion.java im [I2P-Quellcode](https://github.com/i2p/i2p.i2p).

## SU3 Reseed-Datei Spezifikation

Ab Version 0.9.14 werden Reseed-Daten im "su3" Dateiformat übertragen.

### Ziele

- Signierte Dateien mit starken Signaturen und vertrauenswürdigen Zertifikaten, um Man-in-the-Middle-Angriffe zu verhindern, die Opfer in ein separates, nicht vertrauenswürdiges Netzwerk booten könnten.
- Verwendung des su3-Dateiformats, das bereits für Updates und Plugins verwendet wird
- Einzelne komprimierte Datei zur Beschleunigung des Reseeding, da das Abrufen von 200 Dateien langsam war

### Spezifikation

1. Die Datei muss "i2pseeds.su3" heißen. Ab Version 0.9.42 sollte der Anforderer einen Query-String "?netid=2" an die Anfrage-URL anhängen, unter der Annahme der aktuellen Netzwerk-ID 2. Dies kann verwendet werden, um netzwerkübergreifende Verbindungen zu verhindern. Testnetzwerke sollten eine andere Netzwerk-ID festlegen. Siehe Vorschlag 147 für Details.
2. Die Datei muss sich im selben Verzeichnis wie die router infos auf dem Webserver befinden.
3. Ein router wird zunächst versuchen, (Index-URL)/i2pseeds.su3 abzurufen; falls das fehlschlägt, wird er die Index-URL abrufen und dann die einzelnen router info-Dateien herunterladen, die in den Links gefunden wurden.

### SU3 Details

- SU3 Content Type: 3 (RESEED)
- SU3 File Type: 0 (ZIP)
- SU3 Version: Sekunden seit der Epoche, in ASCII (date +%s). Läuft NICHT über in 2038 oder 2106.
- Router-Info-Dateien in der ZIP-Datei müssen auf der "obersten Ebene" sein. Keine Verzeichnisse sind in der ZIP-Datei enthalten.
- Router-Info-Dateien müssen "routerInfo-(44 Zeichen base 64 router Hash).dat" benannt werden, wie im alten Reseed-Mechanismus. Das I2P base 64 Alphabet muss verwendet werden.

### Hinweise

- Warnung: Mehrere Reseeds sind bekanntermaßen über IPv6 nicht erreichbar. Das Erzwingen oder Bevorzugen von IPv4 wird empfohlen.
- Warnung: Einige Reseeds verwenden selbstsignierte CA-Zertifikate. Implementierungen müssen diese CAs beim Reseeding entweder importieren und als vertrauenswürdig einstufen oder die selbstsignierten Reseeds aus der Reseed-Liste ausschließen.
- Reseed-Signaturschlüssel werden an Implementierungen als selbstsignierte X.509-Zertifikate mit RSA-4096-Schlüsseln (Signaturtyp 6) verteilt. Implementierungen sollten die gültigen Daten in den Zertifikaten durchsetzen.

## SU3 Plugin-Datei-Spezifikation

Ab Version 0.9.15 können Plugins im "su3"-Dateiformat verpackt werden.

### SU3 Details

- SU3 Content Type: 2 (PLUGIN)
- SU3 File Type: 0 (ZIP) - Siehe die [Plugin-Spezifikation](/docs/specs/plugin) für Details.
- SU3 Version: Die Plugin-Version, muss mit der in plugin.config übereinstimmen.

Jar- und war-Dateien in der ZIP-Datei sollten nicht mit pack200 komprimiert werden, wie oben für "su2"-Dateien dokumentiert, da aktuelle Java-Laufzeitumgebungen dies nicht mehr unterstützen.

## SU3 News-Datei-Spezifikation

Ab Version 0.9.17 werden die Neuigkeiten im "su3"-Dateiformat bereitgestellt.

### Ziele

- Signierte Nachrichten mit starken Signaturen und vertrauenswürdigen Zertifikaten
- Verwendung des su3-Dateiformats, das bereits für Updates, Reseeding und Plugins verwendet wird
- Standard-XML-Format zur Verwendung mit Standard-Parsern
- Standard-Atom-Format zur Verwendung mit Standard-Feed-Readern und -Generatoren
- Bereinigung und Überprüfung von HTML vor der Anzeige in der Konsole
- Geeignet für einfache Implementierung auf Android und anderen Plattformen ohne HTML-Konsole

### SU3 Details

- SU3 Content Type: 4 (NEWS)
- SU3 File Type: 1 (XML) oder 3 (XML.GZ)
- SU3 Version: Sekunden seit der Epoche, in ASCII (date +%s). Läuft NICHT über in 2038 oder 2106.
- Dateiformat: XML oder gzip-komprimiertes XML, enthält einen [RFC 4287](https://tools.ietf.org/html/rfc4287) (Atom) XML Feed. Zeichensatz muss UTF-8 sein.

### Atom Feed Details

Die folgenden `<feed>`-Elemente werden verwendet:

**`<entry>`** : Ein Nachrichteneintrag. Siehe unten.

**`<i2p:release>`** : I2P-Update-Metadaten. Siehe unten.

**`<i2p:revocations>`** : Zertifikatswiderrufe. Siehe unten.

**`<i2p:blocklist>`** : Sperrlisten-Daten. Siehe unten.

**`<updated>`** : Erforderlich. Zeitstempel für den Feed (entsprechend [RFC 4287](https://tools.ietf.org/html/rfc4287) Abschnitt 3.3 und [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Atom-Eintrag-Details

Jeder Atom `<entry>` im News-Feed kann geparst und in der Router-Konsole angezeigt werden. Die folgenden Elemente werden verwendet:

**`<author>`** : Optional. Enthält `<name>` - Der Name des Eintragsautors.

**`<content>`** : Erforderlich. Inhalt, muss type="xhtml" sein. Das XHTML wird mit einer Whitelist erlaubter Elemente und einer Blacklist nicht erlaubter Attribute bereinigt. Clients können ein Element, den umschließenden Eintrag oder den gesamten Feed ignorieren, wenn ein nicht-whitelistetes Element angetroffen wird.

**`<link>`** : Optional. Link für weitere Informationen.

**`<summary>`** : Optional. Kurze Zusammenfassung, geeignet für einen Tooltip.

**`<title>`** : Erforderlich. Titel des Nachrichteneintrags.

**`<updated>`** : Erforderlich. Zeitstempel für diesen Eintrag (entsprechend [RFC 4287](https://tools.ietf.org/html/rfc4287) Abschnitt 3.3 und [RFC 3339](https://tools.ietf.org/html/rfc3339)).

### Atom i2p:release Details

Es muss mindestens eine `<i2p:release>`-Entität im Feed vorhanden sein. Jede enthält die folgenden Attribute und Entitäten:

**date (Attribut)** : Erforderlich. Zeitstempel für diesen Eintrag (entsprechend [RFC 4287](https://tools.ietf.org/html/rfc4287) Abschnitt 3.3 und [RFC 3339](https://tools.ietf.org/html/rfc3339)). Das Datum kann auch im verkürzten Format yyyy-mm-dd (ohne das 'T') angegeben werden; dies ist das "full-date"-Format in RFC 3339. In diesem Format wird die Zeit für jede Verarbeitung als 00:00:00 UTC angenommen.

**minJavaVersion (Attribut)** : Falls vorhanden, die mindestens erforderliche Java-Version zum Ausführen der aktuellen Version.

**minVersion (Attribut)** : Falls vorhanden, die minimale Version des routers, die erforderlich ist, um auf die aktuelle Version zu aktualisieren. Wenn ein router älter ist als diese, muss der Benutzer (manuell?) zuerst auf eine Zwischenversion aktualisieren.

**`<i2p:version>`** : Erforderlich. Die neueste verfügbare aktuelle Router-Version.

**`<i2p:update>`** : Eine Update-Datei (eine oder mehrere). Sie muss mindestens ein untergeordnetes Element enthalten.   - type (Attribut): "sud", "su2" oder "su3". Muss eindeutig über alle `<i2p:update>`-Elemente hinweg sein.   - `<i2p:clearnet>`: Direkte Download-Links außerhalb des Netzwerks (null oder mehr). href (Attribut): Ein Standard-Clearnet-http-Link.   - `<i2p:clearnetssl>`: Direkte Download-Links außerhalb des Netzwerks (null oder mehr). href (Attribut): Ein Standard-Clearnet-https-Link.   - `<i2p:torrent>`: Magnet-Link innerhalb des Netzwerks. href (Attribut): Ein Magnet-Link.   - `<i2p:url>`: Direkte Download-Links innerhalb des Netzwerks (null oder mehr). href (Attribut): Ein http .i2p Link innerhalb des Netzwerks.

### Atom i2p:revocations Details

Diese Entität ist optional und es gibt höchstens eine `<i2p:revocations>`-Entität im Feed. Diese Funktion wird ab Release 0.9.26 unterstützt.

Das `<i2p:revocations>`-Element enthält ein oder mehrere `<i2p:crl>`-Elemente. Das `<i2p:crl>`-Element enthält die folgenden Attribute:

**updated (Attribut)** : Erforderlich. Zeitstempel für diesen Eintrag (gemäß [RFC 4287](https://tools.ietf.org/html/rfc4287) Abschnitt 3.3 und [RFC 3339](https://tools.ietf.org/html/rfc3339)). Das Datum kann auch im gekürzten Format yyyy-mm-dd (ohne das 'T') vorliegen; dies ist das "full-date"-Format in RFC 3339. In diesem Format wird die Zeit für jede Verarbeitung als 00:00:00 UTC angenommen.

**id (Attribut)** : Erforderlich. Eine eindeutige ID für den Ersteller dieser CRL.

**(entity content)** : Erforderlich. Eine standardmäßige base 64 kodierte Certificate Revocation List (CRL) mit Zeilenumbrüchen, beginnend mit der Zeile '-----BEGIN X509 CRL-----' und endend mit der Zeile '-----END X509 CRL-----'. Siehe [RFC 5280](https://tools.ietf.org/html/rfc5280) für weitere Informationen zu CRLs.

### Atom i2p:blocklist Details

Diese Entität ist optional und es gibt höchstens eine `<i2p:blocklist>`-Entität im Feed. Diese Funktion ist für die Implementierung in Version 0.9.28 geplant.

Die `<i2p:blocklist>`-Entität enthält eine oder mehrere `<i2p:block>`- oder `<i2p:unblock>`-Entitäten, eine "updated"-Entität und die Attribute "signer" und "sig":

**signer (Attribut)** : Erforderlich. Eine eindeutige ID (UTF-8) für den öffentlichen Schlüssel, der zum Signieren dieser Blocklist verwendet wird.

**sig (Attribut)** : Erforderlich. Eine Signatur im Format code:b64sig, wobei code die ASCII-Signaturtypnummer ist und b64sig die base64-kodierte Signatur (I2P-Alphabet). Siehe unten für die Spezifikation der zu signierenden Daten.

**`<updated>`** : Erforderlich. Zeitstempel für die Blocklist (gemäß [RFC 4287](https://tools.ietf.org/html/rfc4287) Abschnitt 3.3 und [RFC 3339](https://tools.ietf.org/html/rfc3339)). Das Datum kann auch im gekürzten Format yyyy-mm-dd (ohne das 'T') angegeben werden; dies ist das "full-date" Format in RFC 3339. In diesem Format wird die Zeit für jede Verarbeitung als 00:00:00 UTC angenommen.

**`<i2p:block>`** : Optional, mehrere Einträge sind erlaubt. Ein einzelner Eintrag, entweder eine literale IPv4- oder IPv6-Adresse, oder ein 44-Zeichen base 64 router hash (I2P-Alphabet). IPv6-Adressen können in abgekürzter Form vorliegen (mit "::"). Unterstützung für Einträge mit einer Netzmaske, z.B. x.y.0.0/16, ist optional. Unterstützung für Hostnamen ist optional.

**`<i2p:unblock>`** : Optional, mehrere Einträge sind erlaubt. Gleiches Format wie `<i2p:block>`.

**Signatur-Spezifikation:** Um die zu signierenden oder zu verifizierenden Daten zu generieren, verketten Sie die folgenden Daten in ASCII-Kodierung: Die aktualisierte Zeichenkette gefolgt von einem Zeilenwechsel (ASCII 0x0a), dann jeden Block-Eintrag in der empfangenen Reihenfolge mit einem Zeilenwechsel nach jedem, dann jeden Unblock-Eintrag in der empfangenen Reihenfolge mit einem Zeilenwechsel nach jedem.

## Blocklist-Datei-Spezifikation

TBD, nicht implementiert, siehe Vorschlag 130. Blocklist-Updates werden in der News-Datei übermittelt, siehe oben.

## Zukünftige Arbeiten

- Der router-Updatemechanismus ist Teil der Web-router-Konsole. Derzeit gibt es keine Möglichkeit für Updates eines eingebetteten routers ohne router-Konsole.

## Referenzen

- **[CRYPTO-SIG]** [Kryptographie - Signaturen](/docs/specs/cryptography#sig)
- **[I2P-SRC]** [I2P Quellcode](https://github.com/i2p/i2p.i2p)
- **[PLUGIN]** [Plugin-Spezifikation](/docs/specs/plugin)
- **[Python]** [Python RSA Raw Signaturen](https://stackoverflow.com/questions/59573121/python-rsa-sign-a-string-with-nonewithrsa/68301530#68301530)
- **[RFC-3339]** [RFC 3339 - Datum und Zeit](https://tools.ietf.org/html/rfc3339)
- **[RFC-4287]** [RFC 4287 - Atom Syndication Format](https://tools.ietf.org/html/rfc4287)
- **[RFC-5280]** [RFC 5280 - Certificate Revocation Lists](https://tools.ietf.org/html/rfc5280)
- **[Signature]** [Signatur-Typ](/docs/specs/common-structures#signature)
- **[SigningPublicKey]** [SigningPublicKey-Typ](/docs/specs/common-structures#signingpublickey)
