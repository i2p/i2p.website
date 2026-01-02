---
title: "Netzwerkdatenbank"
description: "I2Ps verteilte Netzwerkdatenbank (netDb) verstehen - eine spezialisierte DHT für router-Kontaktinformationen und Destination-Abfragen"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Übersicht

Die **netDb** ist eine spezialisierte verteilte Datenbank, die nur zwei Arten von Daten enthält: - **RouterInfos** – Router-Kontaktinformationen - **LeaseSets** – Destination-Kontaktinformationen

Alle Daten sind kryptografisch signiert und verifizierbar. Jeder Eintrag enthält Liveness-Informationen (Informationen zur Betriebsbereitschaft), um veraltete Einträge zu verwerfen und überholte zu ersetzen, wodurch gegen bestimmte Angriffsarten geschützt wird.

Die Verteilung verwendet einen **floodfill**-Mechanismus, bei dem eine Teilmenge der routers die verteilte Datenbank verwaltet.

---

## 2. RouterInfo (Router-Informationen)

Wenn routers andere routers kontaktieren müssen, tauschen sie **RouterInfo**-Bündel (Router-Informationen) aus, die Folgendes enthalten:

- **Router-Identität** – Verschlüsselungsschlüssel, Signaturschlüssel, Zertifikat
- **Kontaktadressen** – wie der Router erreicht werden kann
- **Zeitstempel der Veröffentlichung** – wann diese Informationen veröffentlicht wurden
- **Freitextoptionen** – Fähigkeits-Flags und Einstellungen
- **Kryptografische Signatur** – weist die Authentizität nach

### 2.1 Fähigkeits-Flags

Router geben ihre Fähigkeiten mittels Buchstaben-Codes in ihrer RouterInfo (Router-Informationsdatensatz) bekannt:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Klassifizierungen der Bandbreite

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Netzwerk-ID-Werte

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 RouterInfo (Router-Informationen) Statistiken

Routers veröffentlichen optionale Zustandsstatistiken zur Netzwerkanalyse: - Erfolgs-/Ablehnungs-/Timeout-Raten beim Aufbau von Exploratory tunnels (Erkundungs-tunnels) - 1‑Stunden-Durchschnitt der Anzahl teilnehmender tunnels

Statistiken folgen dem Format `stat_(statname).(statperiod)` mit durch Semikolons getrennten Werten.

**Beispielstatistiken:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers können außerdem veröffentlichen: `netdb.knownLeaseSets` und `netdb.knownRouters`

### 2.5 Familienoptionen

Seit Version 0.9.24 können routers ihre Familienzugehörigkeit (gleicher Betreiber) angeben:

- **family**: Familienname
- **family.key**: Signaturtyp-Code, verkettet mit dem Base64-kodierten öffentlichen Signaturschlüssel
- **family.sig**: Signatur über den Familiennamen und den 32-Byte router-Hash

Mehrere router derselben Familie werden nicht in einem einzelnen tunnel verwendet.

### 2.6 Ablauf der RouterInfo (Router-Informationen)

- Kein Ablauf während der ersten Stunde der Betriebszeit
- Kein Ablauf bei 25 oder weniger gespeicherten RouterInfos
- Ablaufzeit verkürzt sich mit wachsender lokaler Anzahl (72 Stunden bei <120 Router; ~30 Stunden bei 300 Router)
- SSU-Introducer (Vermittler) laufen nach ~1 Stunde ab
- Floodfills verwenden eine Ablaufzeit von 1 Stunde für alle lokalen RouterInfos

---

## 3. LeaseSet (veröffentlichter Datensatz mit Informationen zu Endpunkten eingehender tunnel und Schlüsseln zur Erreichbarkeit eines Ziels)

**LeaseSets** dokumentieren die Einstiegspunkte von Tunneln für bestimmte Ziele und spezifizieren:

- **Tunnel-Gateway-router-Identität**
- **4-Byte tunnel-ID**
- **Ablaufzeit für den Tunnel**

LeaseSets umfassen: - **Destination** – Verschlüsselungsschlüssel, Signaturschlüssel, Zertifikat - **Zusätzlicher öffentlicher Verschlüsselungsschlüssel** – für Ende-zu-Ende garlic encryption - **Zusätzlicher öffentlicher Signaturschlüssel** – vorgesehen für Widerruf (derzeit ungenutzt) - **Kryptografische Signatur**

### 3.1 LeaseSet-Varianten

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 LeaseSet-Ablaufzeit

Normale LeaseSets (I2P-Datenstruktur für Erreichbarkeitsinformationen) laufen zum spätesten Ablaufzeitpunkt ihrer enthaltenen Leases ab. Die Ablaufzeit von LeaseSet2 ist im Header angegeben. Die Ablaufzeiten von EncryptedLeaseSet und MetaLeaseSet können variieren; ein Maximalwert kann erzwungen werden.

---

## 4. Bootstrapping (Startinitialisierung)

Die dezentrale netDb benötigt mindestens einen Peer-Verweis, um eingebunden zu werden. **Reseeding** (Initialbefüllung der netDb) ruft RouterInfo-Dateien (`routerInfo-$hash.dat`) aus den netDb-Verzeichnissen von Freiwilligen ab. Beim ersten Start wird automatisch von zufällig ausgewählten, hartcodierten URLs abgerufen.

---

## 5. Floodfill-Mechanismus

Die floodfill netDb verwendet eine einfache verteilte Speicherung: Man sendet Daten an den nächstgelegenen floodfill-Peer. Wenn Peers, die keine floodfills sind, Daten zur Speicherung senden, leiten floodfills sie an eine Teilmenge der floodfill-Peers weiter, die dem jeweiligen Schlüssel am nächsten liegt.

Die floodfill-Teilnahme wird in der RouterInfo als Fähigkeits-Flag (`f`) angegeben.

### 5.1 Anforderungen für das Floodfill-Opt-In

Im Gegensatz zu Tors hartkodierten, vertrauenswürdigen Verzeichnisservern ist I2Ps floodfill-Menge **nicht vertrauenswürdig** und ändert sich im Laufe der Zeit.

Floodfill wird automatisch nur auf routers mit hoher Bandbreite aktiviert, die diese Anforderungen erfüllen: - Mindestens 128 KBytes/sec freigegebene Bandbreite (manuell konfiguriert) - Zusätzliche Integritätsprüfungen müssen bestanden werden (Wartezeit der ausgehenden Nachrichtenwarteschlange, Job-Verzögerung)

Das derzeitige automatische Opt-in führt zu ungefähr **6% floodfill-Beteiligung im Netzwerk**.

Manuell konfigurierte floodfills (spezielle Router für die Verteilung der netDb) existieren parallel zu automatisch freiwillig aktivierten floodfills. Wenn die Anzahl der floodfills unter einen Schwellenwert fällt, melden sich Router mit hoher Bandbreite automatisch als floodfill. Wenn es zu viele floodfills gibt, geben sie ihren floodfill-Status wieder auf.

### 5.2 Floodfill-Rollen

Über das Annehmen von netDb-Speicherungen und das Beantworten von Abfragen hinaus erfüllen floodfills die üblichen Aufgaben als router. Ihre höhere Bandbreite führt typischerweise zu mehr tunnel-Teilnahme, steht jedoch nicht in direktem Zusammenhang mit den Datenbankdiensten.

---

## 6. Kademlia-Nähemetrik

Die netDb (Netzwerkdatenbank) verwendet eine XOR-basierte **Kademlia-ähnliche** Distanzmessung. Der SHA256-Hash von RouterIdentity oder Destination erzeugt den Kademlia-Schlüssel (ausgenommen LS2 Encrypted LeaseSets, die SHA256 über das Typ-Byte 3 plus den verblindeten öffentlichen Schlüssel verwenden).

### 6.1 Rotation des Schlüsselraums

Um die Kosten eines Sybil-Angriffs zu erhöhen, verwendet das System anstelle von `SHA256(key)`:

```
SHA256(key + yyyyMMdd)
```
wobei das Datum ein 8-Byte-ASCII-UTC-Datum ist. Dadurch entsteht der **Routing-Schlüssel**, der sich täglich um Mitternacht UTC ändert—genannt **Schlüsselraum-Rotation**.

Routing-Schlüssel werden in I2NP-Nachrichten niemals übertragen; sie werden nur zur lokalen Distanzbestimmung verwendet.

---

## 7. Segmentierung der Netzwerkdatenbank

Traditionelle Kademlia DHTs wahren die Unverkettbarkeit gespeicherter Informationen nicht. I2P verhindert Angriffe, die client tunnels mit routers in Verbindung bringen, durch die Implementierung von **Segmentierung**.

### 7.1 Segmentierungsstrategie

Routers verfolgen:
- Ob Einträge über Client tunnels oder direkt eingegangen sind
- Falls über tunnel, welcher Client tunnel/Ziel
- Mehrfache Eingänge über tunnel werden nachverfolgt
- Antworten auf Speicherung vs. Abfrage werden unterschieden

Sowohl Java- als auch C++-Implementierungen verwenden: - Eine **"Main" netDb** für direkte Abfragen/floodfill-Operationen im Router-Kontext - **"Client-Netzwerkdatenbanken"** oder **"Unterdatenbanken"** in Client-Kontexten, die Einträge erfassen, die an Client tunnels gesendet werden

Client-netDbs existieren nur für die Lebensdauer des Clients und enthalten ausschließlich Client-tunnel-Einträge. Einträge aus Client-tunnels dürfen sich nicht mit direkten Eingängen überschneiden.

Jede netDb verfolgt, ob Einträge als Stores eingegangen sind (antworten auf Lookup-Anfragen) oder als Lookup-Antworten (antworten nur, wenn sie zuvor für dasselbe Ziel gespeichert wurden). Clients beantworten Anfragen niemals mit Einträgen der Main-netDb, sondern nur mit Einträgen der Client-Netzwerkdatenbank.

Kombinierte Strategien **segmentieren** die netDb gegen Client-router-Assoziationsangriffe.

---

## 8. Speicherung, Überprüfung und Nachschlagen

### 8.1 Speicherung von RouterInfo bei Peers

I2NP `DatabaseStoreMessage`, die den Austausch der lokalen RouterInfo (Informationen über den Router) während der Initialisierung einer NTCP- oder SSU-Transportverbindung enthält.

### 8.2 Speicherung des LeaseSet (Lease-Datensatz) bei Peers

I2NP `DatabaseStoreMessage`, die das lokale LeaseSet enthalten, werden periodisch über mit garlic encryption (Garlic‑Verschlüsselung) verschlüsselte Nachrichten ausgetauscht, die mit dem Destination-Verkehr gebündelt sind, sodass Antworten ohne LeaseSet-Abfragen möglich sind.

### 8.3 Floodfill-Auswahl

`DatabaseStoreMessage` sendet an das floodfill, das dem aktuellen Routing-Schlüssel am nächsten ist. Das nächste floodfill wird über eine lokale Datenbanksuche ermittelt. Selbst wenn es nicht tatsächlich das nächstgelegene ist, bringt Flooding (Verteilungsverfahren) es "näher", indem an mehrere floodfills gesendet wird.

Das traditionelle Kademlia verwendet vor dem Einfügen eine „find-closest“-Suche. Während I2NP solche Nachrichten nicht unterstützt, können router eine iterative Suche mit invertiertem niederwertigsten Bit (`key ^ 0x01`) durchführen, um die tatsächlich nächstgelegenen Peers zu ermitteln.

### 8.4 Speicherung von RouterInfo bei Floodfills

Router veröffentlichen RouterInfo, indem sie sich direkt mit einem floodfill verbinden und eine I2NP `DatabaseStoreMessage` mit einem Antwort-Token ungleich Null senden. Die Nachricht ist nicht Ende-zu-Ende mit garlic encryption verschlüsselt (direkte Verbindung, keine Zwischenknoten). Der floodfill antwortet mit `DeliveryStatusMessage` und verwendet das Antwort-Token als Message-ID.

Routers können RouterInfo (Router-Informationsdatensatz) auch über einen exploratory tunnel (Erkundungs-Tunnel) senden (Verbindungsbeschränkungen, Inkompatibilität, IP-Verschleierung). Floodfills können solche Speicherungen bei Überlast ablehnen.

### 8.5 Speicherung des LeaseSets in Floodfills

Die Speicherung von LeaseSets ist sensibler als die von RouterInfo. Router müssen verhindern, dass LeaseSets mit ihnen selbst in Verbindung gebracht werden.

Routers veröffentlichen LeaseSet über einen ausgehenden Client-tunnel mittels `DatabaseStoreMessage` mit einem von Null verschiedenen Reply-Token. Die Nachricht ist Ende-zu-Ende mit garlic encryption verschlüsselt, unter Verwendung des Session Key Managers der Destination (Verwaltung der Sitzungsschlüssel), sodass sie vor dem ausgehenden Endpunkt des tunnel verborgen bleibt. Floodfill antwortet mit einer `DeliveryStatusMessage`, die über einen eingehenden tunnel zurückgegeben wird.

### 8.6 Flooding-Prozess

Floodfills validieren RouterInfo/LeaseSet, bevor sie diese lokal speichern, anhand adaptiver Kriterien, die von der Auslastung, der netdb-Größe und anderen Faktoren abhängen.

Nach dem Empfang gültiger, neuerer Daten „fluten“ floodfills diese, indem sie die 3 floodfill router ermitteln, die dem Routing-Schlüssel am nächsten sind. Direkte Verbindungen senden eine I2NP `DatabaseStoreMessage` mit einem Antwort-Token von Null. Andere router antworten nicht oder fluten nicht erneut.

**Wichtige Einschränkungen:** - Floodfills dürfen nicht über tunnels fluten; nur direkte Verbindungen - Floodfills fluten niemals abgelaufenes LeaseSet oder RouterInfo, das vor über einer Stunde veröffentlicht wurde

### 8.7 RouterInfo- und LeaseSet-Abfrage

I2NP `DatabaseLookupMessage` fordert netdb-Einträge von floodfill routers an. Abfragen werden über einen ausgehenden exploratory tunnel (Erkundungstunnel) gesendet; Antworten geben den Rückweg über einen eingehenden exploratory tunnel an.

Abfragen werden in der Regel parallel an zwei "gute" floodfill routers gesendet, die dem angeforderten Schlüssel am nächsten sind.

- **Lokaler Treffer**: empfängt eine I2NP `DatabaseStoreMessage`-Antwort
- **Kein lokaler Treffer**: empfängt eine I2NP `DatabaseSearchReplyMessage` mit Verweisen auf andere floodfill router, die dem Schlüssel nahe sind

LeaseSet-Abfragen verwenden Ende-zu-Ende garlic encryption (seit 0.9.5). Abfragen von RouterInfo (I2P-Datenobjekt mit Router-Informationen) sind aufgrund des Rechenaufwands von ElGamal nicht verschlüsselt, wodurch sie anfällig für das Ausspähen des ausgehenden Endpunkts sind.

Ab Version 0.9.7 enthalten Lookup-Antworten einen Sitzungsschlüssel und ein Tag, sodass Antworten vor dem Eingangs-Gateway verborgen bleiben.

### 8.8 Iterative Abfragen

Vor 0.8.9: Zwei parallele redundante Abfragen ohne rekursives oder iteratives Routing.

Seit 0.8.9: **Iterative Suchvorgänge** ohne Redundanz implementiert — effizienter, zuverlässiger und geeignet für unvollständige Kenntnisse über floodfills. Wenn Netzwerke wachsen und routers weniger floodfills kennen, nähern sich die Suchvorgänge einer O(log n)-Komplexität an.

Iterative Abfragen werden auch ohne Verweise auf nähere Peers fortgesetzt und verhindern so böswilliges Black-holing (absichtliches Verschlucken von Anfragen). Die aktuellen Obergrenzen für die Anzahl der Abfragen und das Timeout gelten weiterhin.

### 8.9 Verifizierung

**RouterInfo (Router-Informationen) Verifizierung**: Seit Version 0.9.7.1 deaktiviert, um die in dem Paper "Practical Attacks Against the I2P Network" beschriebenen Angriffe zu verhindern.

**LeaseSet-Verifizierung**: Router warten ~10 Sekunden und führen dann ein Lookup bei einem anderen floodfill über einen outbound client tunnel durch. Ende-zu-Ende garlic encryption verbirgt dies vor dem outbound-Endpunkt. Antworten kommen über inbound tunnels zurück.

Seit 0.9.7 werden Antworten so verschlüsselt, dass session key/tag hiding (Verbergen von Sitzungsschlüssel/-Tags) gegenüber dem Inbound-Gateway gewährleistet ist.

### 8.10 Erkundung

**Erkundung** umfasst einen netdb-Lookup mit zufälligen Schlüsseln, um neue router kennenzulernen. Floodfills antworten mit einer `DatabaseSearchReplyMessage`, die nicht-floodfill-router-Hashes enthält, die dem angeforderten Schlüssel nahe sind. Explorationsanfragen setzen ein spezielles Flag in `DatabaseLookupMessage`.

---

## 9. Multihoming

Destinations (I2P-Zielidentitäten), die identische private/öffentliche Schlüssel (im traditionellen `eepPriv.dat`) verwenden, können gleichzeitig auf mehreren router gehostet werden. Jede Instanz veröffentlicht regelmäßig signierte LeaseSets; das zuletzt veröffentlichte LeaseSet wird den Anfragenden zurückgegeben. Mit einer maximalen LeaseSet-Lebensdauer von 10 Minuten dauern Ausfälle höchstens ~10 Minuten.

Seit 0.9.38 unterstützen **Meta LeaseSets** große, multihomed Dienste, bei denen separate Destinations (I2P-Zieladressen) gemeinsame Dienste bereitstellen. Meta LeaseSet-Einträge sind Destinations oder andere Meta LeaseSets mit Ablaufzeiten von bis zu 18,2 Stunden und ermöglichen Hunderte/Tausende von Destinations, die gemeinsame Dienste hosten.

---

## 10. Bedrohungsanalyse

Etwa 1700 floodfill routers sind derzeit in Betrieb. Netzwerkwachstum macht die meisten Angriffe schwieriger oder weniger wirkungsvoll.

### 10.1 Allgemeine Gegenmaßnahmen

- **Wachstum**: Mehr floodfills (spezielle router zum Verteilen der netDb) machen Angriffe schwieriger oder weniger wirksam
- **Redundanz**: Alle netDb-Einträge (verteilte I2P-Netzdatenbank) werden durch Flooding auf den 3 floodfill routers gespeichert, die dem Schlüssel am nächsten sind
- **Signaturen**: Alle Einträge sind vom Ersteller signiert; Fälschungen sind unmöglich

### 10.2 Langsame oder nicht reagierende Router

Routers pflegen erweiterte Peer-Profil-Statistiken für floodfills: - Durchschnittliche Antwortzeit - Prozentsatz der beantworteten Anfragen - Prozentsatz erfolgreicher Store-Verifizierungen - Letzter erfolgreicher Store - Letztes erfolgreiches Lookup - Letzte Antwort

Routers verwenden diese Metriken bei der Bestimmung der „Güte“ zur Auswahl des nächsten floodfill. Vollständig nicht reagierende routers werden schnell identifiziert und gemieden; teilweise böswillige routers stellen eine größere Herausforderung dar.

### 10.3 Sybil-Angriff (vollständiger Schlüsselraum)

Angreifer könnten zahlreiche floodfill routers über den gesamten Schlüsselraum verteilt einrichten, als einen effektiven DOS-Angriff.

Wenn das Fehlverhalten nicht ausreicht für eine Einstufung als "bad", sind mögliche Reaktionen: - Erstellung von "bad" router-Hash/IP-Listen, angekündigt über Konsolen-News, Website, Forum - Netzwerkweite Aktivierung von floodfill ("Sybil mit mehr Sybil bekämpfen") - Neue Softwareversionen mit hart kodierten "bad"-Listen - Verbesserte Metriken und Schwellenwerte für Peer-Profile zur automatischen Identifizierung - IP-Block-Qualifikation, die mehrere floodfills innerhalb eines einzelnen IP-Blocks disqualifiziert - Automatische abonnementsbasierte Blacklist (ähnlich dem Tor-Konsens)

Größere Netzwerke erschweren dies.

### 10.4 Sybil-Angriff (partieller Schlüsselraum)

Angreifer könnten 8–15 floodfill routers eng beieinander im Schlüsselraum platzieren. Alle Nachschlage- und Speichervorgänge für diesen Schlüsselraum werden zu den router des Angreifers geleitet, wodurch DoS (Dienstverweigerung) gegen bestimmte I2P‑Sites ermöglicht wird.

Da der Schlüsselraum kryptografische SHA256-Hashes indiziert, müssen Angreifer Brute-Force einsetzen, um routers mit ausreichender Nähe im Schlüsselraum zu erzeugen.

**Verteidigung**: Der Kademlia-Algorithmus zur Nähebestimmung variiert im Zeitverlauf mithilfe von `SHA256(key + YYYYMMDD)` und ändert sich täglich um Mitternacht (UTC). Diese **Schlüsselraumrotation** erzwingt eine tägliche Neugenerierung des Angriffs.

> **Hinweis**: Jüngste Forschung zeigt, dass die Rotation des Schlüsselraums nicht besonders wirksam ist—Angreifer können router-Hashes vorberechnen und benötigen dann nur einige router, um Teilbereiche des Schlüsselraums innerhalb einer halben Stunde nach der Rotation zu kontrollieren.

Folge der täglichen Rotation: die verteilte netdb wird für einige Minuten nach der Rotation unzuverlässig—Abfragen schlagen fehl, bevor der neue nächstgelegene router Stores (Store-Nachrichten) erhält.

### 10.5 Bootstrap-Angriffe

Angreifer könnten Reseed-Websites (Websites zum Erstbezug von Netzwerkdaten) übernehmen oder Entwickler dazu verleiten, bösartige Reseed-Websites hinzuzufügen, sodass neue Router in isolierte/mehrheitskontrollierte Netzwerke booten.

**Implementierte Schutzmaßnahmen:** - Abruf von RouterInfo-Teilmengen von mehreren reseed-Sites (Bootstrap des I2P-Netzes) anstatt einer einzelnen Site - Netzwerkexternes reseed-Monitoring, das Sites periodisch abfragt - Seit 0.9.14 werden reseed-Datenpakete als signierte zip-Dateien bereitgestellt, mit Verifizierung der heruntergeladenen Signatur (siehe [su3 specification](/docs/specs/updates))

### 10.6 Abfrageerfassung

Floodfill routers könnten Peers über zurückgegebene Referenzen zu von Angreifern kontrollierten routers "lenken".

Es ist aufgrund der geringen Häufigkeit durch Erkundung unwahrscheinlich; router erhalten Peer-Referenzen hauptsächlich über den normalen tunnel-Aufbau.

Seit 0.8.9 sind iterative Lookups implementiert. floodfill-Referenzen in `DatabaseSearchReplyMessage` werden verfolgt, wenn sie dem Lookup-Schlüssel näher sind. Anfragende router vertrauen der Referenznähe nicht. Lookups werden trotz fehlender näherer Schlüssel bis zum Timeout bzw. bis zum Erreichen der maximalen Anzahl von Abfragen fortgesetzt, wodurch böswilliges Black-Holing (absichtliches Versenken von Anfragen ohne Antwort) verhindert wird.

### 10.7 Informationslecks

DHT-Informationslecks (verteilte Hashtabelle) in I2P erfordern weitere Untersuchungen. Floodfill routers beobachten Anfragen und sammeln dabei Informationen. Bei einem Anteil bösartiger Knoten von 20 % werden die zuvor beschriebenen Sybil-Angriffe aus mehreren Gründen problematisch.

---

## 11. Zukünftige Arbeiten

- Ende-zu-Ende-Verschlüsselung zusätzlicher netDb-Abfragen und -Antworten
- Bessere Methoden zur Nachverfolgung von Lookup-Antworten
- Methoden zur Abmilderung von Zuverlässigkeitsproblemen bei der Schlüsselraum-Rotation

---

## 12. Referenzen

- [Spezifikation allgemeiner Strukturen](/docs/specs/common-structures/) – RouterInfo- und LeaseSet-Strukturen
- [I2NP-Spezifikation](/docs/specs/i2np/) – Typen von Datenbanknachrichten
- [Vorschlag 123: Neue netDb-Einträge](/proposals/123-new-netdb-entries) – LeaseSet2-Spezifikation
- [Historische netDb-Diskussion](/docs/netdb/) – Entwicklungsgeschichte und archivierte Diskussionen
