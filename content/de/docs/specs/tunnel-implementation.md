---
title: "Tunnel-Implementierung"
description: "Spezifikation des I2P tunnel-Betriebs, -Aufbaus und der Nachrichtenverarbeitung"
slug: "tunnel-implementation"
aliases:
  - "/de/docs/specs/implementation"
  - "/de/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Diese Seite dokumentiert die aktuelle tunnel-Implementierung.

## Tunnel Übersicht {#tunnel.overview}

Innerhalb von I2P werden Nachrichten in eine Richtung durch einen virtuellen tunnel von Peers weitergeleitet, wobei alle verfügbaren Mittel genutzt werden, um die Nachricht an den nächsten Hop weiterzuleiten. Nachrichten erreichen das *gateway* des tunnels, werden gebündelt und/oder in Tunnel-Nachrichten fester Größe fragmentiert und an den nächsten Hop im tunnel weitergeleitet, der die Nachricht verarbeitet und deren Gültigkeit überprüft und sie an den nächsten Hop weitersendet, und so weiter, bis sie den tunnel-Endpunkt erreicht. Dieser *Endpunkt* nimmt die vom gateway gebündelten Nachrichten und leitet sie wie angewiesen weiter - entweder an einen anderen router, an einen anderen tunnel auf einem anderen router oder lokal.

Tunnels funktionieren alle gleich, können aber in zwei verschiedene Gruppen unterteilt werden - eingehende tunnels und ausgehende tunnels. Die eingehenden tunnels haben ein nicht vertrauenswürdiges Gateway, das Nachrichten zum tunnel-Ersteller weiterleitet, der als tunnel-Endpunkt dient. Bei ausgehenden tunnels dient der tunnel-Ersteller als Gateway und leitet Nachrichten an den entfernten Endpunkt weiter.

Der Ersteller des tunnels wählt genau aus, welche Peers am tunnel teilnehmen werden, und stellt jedem die notwendigen Konfigurationsdaten zur Verfügung. Sie können eine beliebige Anzahl von Hops haben. Es ist beabsichtigt, es sowohl für Teilnehmer als auch für Dritte schwer zu machen, die Länge eines tunnels zu bestimmen, oder sogar für kollidierende Teilnehmer zu bestimmen, ob sie überhaupt Teil desselben tunnels sind (außer in der Situation, wo kollidierende Peers im tunnel nebeneinander stehen).

In der Praxis werden eine Reihe von tunnel-Pools für verschiedene Zwecke verwendet - jede lokale Client-Destination hat ihre eigenen eingehenden tunnels und ausgehenden tunnels, die konfiguriert sind, um ihre Anonymitäts- und Leistungsanforderungen zu erfüllen. Zusätzlich unterhält der router selbst eine Reihe von Pools für die Teilnahme an der netDb und für die Verwaltung der tunnels selbst.

I2P ist ein von Natur aus paketgeschaltetes Netzwerk, selbst mit diesen tunnels, was es ermöglicht, mehrere parallel laufende tunnels zu nutzen, wodurch die Widerstandsfähigkeit erhöht und die Last ausbalanciert wird. Außerhalb der Kern-I2P-Schicht steht eine optionale Ende-zu-Ende-Streaming-Bibliothek für Client-Anwendungen zur Verfügung, die TCP-ähnliche Funktionalität bereitstellt, einschließlich Nachrichtenumordnung, Neuübertragung, Staukontrolle usw.

Eine Übersicht der I2P tunnel-Terminologie finden Sie [auf der tunnel-Übersichtsseite](/docs/overview/tunnel-routing).

## Tunnel-Betrieb (Nachrichtenverarbeitung) {#tunnel.operation}

### Überblick

Nachdem ein tunnel erstellt wurde, werden [I2NP messages](/docs/specs/i2np) verarbeitet und durch ihn geleitet. Der Tunnel-Betrieb umfasst vier verschiedene Prozesse, die von verschiedenen Peers im tunnel übernommen werden.

1. Zuerst sammelt das tunnel gateway eine Anzahl
   von I2NP-Nachrichten und verarbeitet sie zu tunnel-Nachrichten für
   die Zustellung vor.
2. Als nächstes verschlüsselt dieses gateway die vorverarbeiteten Daten und
   leitet sie an den ersten Hop weiter.
3. Dieser Peer und nachfolgende tunnel-
   Teilnehmer entpacken eine Schicht der Verschlüsselung, überprüfen, dass es sich nicht
   um ein Duplikat handelt, und leiten es dann an den nächsten Peer weiter.
4. Schließlich kommen die tunnel-Nachrichten am Endpunkt an, wo die I2NP-Nachrichten,
   die ursprünglich vom gateway gebündelt wurden, wieder zusammengesetzt und wie
   angefordert weitergeleitet werden.

Zwischenliegende tunnel-Teilnehmer wissen nicht, ob sie sich in einem eingehenden oder ausgehenden tunnel befinden; sie "verschlüsseln" immer für den nächsten Hop. Daher nutzen wir die symmetrische AES-Verschlüsselung, um am ausgehenden tunnel-Gateway zu "entschlüsseln", sodass der Klartext am ausgehenden Endpunkt preisgegeben wird.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Gateway-Verarbeitung {#tunnel.gateway}

#### Nachrichtenvorverarbeitung {#tunnel.preprocessing}

Die Funktion eines tunnel gateways ist es, [I2NP messages](/docs/specs/i2np) zu fragmentieren und in tunnel messages mit fester Größe zu packen sowie die tunnel messages zu verschlüsseln. Tunnel messages enthalten folgendes:

- Eine 4 Byte Tunnel ID
- Ein 16 Byte IV (Initialisierungsvektor)
- Eine Prüfsumme
- Auffüllung, falls erforderlich
- Ein oder mehrere { Zustellungsanweisung, I2NP Nachrichtenfragment } Paare

Tunnel-IDs sind 4-Byte-Zahlen, die an jedem Hop verwendet werden - die Teilnehmer wissen, auf welche Tunnel-ID sie bei Nachrichten hören müssen und mit welcher Tunnel-ID diese an den nächsten Hop weitergeleitet werden sollen, und jeder Hop wählt die Tunnel-ID, auf der er Nachrichten empfängt. Tunnel selbst sind kurzlebig (10 Minuten). Selbst wenn nachfolgende Tunnel mit derselben Sequenz von Peers aufgebaut werden, ändert sich die Tunnel-ID jedes Hops.

Um zu verhindern, dass Angreifer die Nachrichten entlang des Pfades markieren, indem sie die Nachrichtengröße anpassen, haben alle tunnel-Nachrichten eine feste Größe von 1024 Bytes. Um größere I2NP-Nachrichten zu berücksichtigen und kleinere effizienter zu unterstützen, teilt das Gateway größere I2NP-Nachrichten in Fragmente auf, die in jeder tunnel-Nachricht enthalten sind. Der Endpunkt wird versuchen, die I2NP-Nachricht aus den Fragmenten für eine kurze Zeit zu rekonstruieren, wird sie jedoch bei Bedarf verwerfen.

Details finden sich in der [tunnel message Spezifikation](/docs/specs/tunnel-message).

### Gateway-Verschlüsselung

Nach der Vorverarbeitung der Nachrichten in eine aufgefüllte Nutzlast erstellt das Gateway einen zufälligen 16-Byte-IV-Wert, verschlüsselt diesen und die tunnel-Nachricht iterativ nach Bedarf und leitet das Tupel {tunnelID, IV, verschlüsselte tunnel-Nachricht} an den nächsten Hop weiter.

Wie die Verschlüsselung am Gateway durchgeführt wird, hängt davon ab, ob es sich um einen eingehenden oder einen ausgehenden Tunnel handelt. Bei eingehenden Tunnels wählen sie einfach einen zufälligen IV aus, bearbeiten und aktualisieren ihn nach, um den IV für das Gateway zu generieren, und verwenden diesen IV zusammen mit ihrem eigenen Schichtschlüssel, um die vorverarbeiteten Daten zu verschlüsseln. Bei ausgehenden Tunnels müssen sie iterativ den (unverschlüsselten) IV und die vorverarbeiteten Daten mit dem IV und den Schichtschlüsseln für alle Hops im Tunnel entschlüsseln. Das Ergebnis der ausgehenden Tunnel-Verschlüsselung ist, dass wenn jeder Peer sie verschlüsselt, der Endpunkt die ursprünglichen vorverarbeiteten Daten wiederherstellen wird.

### Teilnehmer-Verarbeitung {#tunnel.participant}

Wenn ein Peer eine tunnel-Nachricht erhält, überprüft er, dass die Nachricht vom selben vorherigen Hop wie zuvor kam (initialisiert, wenn die erste Nachricht durch den tunnel kommt). Falls der vorherige Peer ein anderer router ist oder die Nachricht bereits gesehen wurde, wird die Nachricht verworfen. Der Teilnehmer verschlüsselt dann den empfangenen IV mit AES256/ECB unter Verwendung seines IV-Schlüssels, um den aktuellen IV zu bestimmen, verwendet diesen IV mit dem Layer-Schlüssel des Teilnehmers zur Verschlüsselung der Daten, verschlüsselt den aktuellen IV erneut mit AES256/ECB unter Verwendung seines IV-Schlüssels und leitet dann das Tupel {nextTunnelId, nextIV, encryptedData} an den nächsten Hop weiter. Diese doppelte Verschlüsselung des IV (sowohl vor als auch nach der Verwendung) hilft dabei, eine bestimmte Klasse von Bestätigungsangriffen zu adressieren.

Die Erkennung von doppelten Nachrichten wird durch einen sich verschlechternden Bloom-Filter für Nachrichten-IVs behandelt. Jeder router führt einen einzigen Bloom-Filter, der das XOR des IV und des ersten Blocks der empfangenen Nachricht für alle tunnel enthält, an denen er teilnimmt. Dieser wird so modifiziert, dass gesehene Einträge nach 10-20 Minuten verworfen werden (wenn die tunnel abgelaufen sind). Die Größe des Bloom-Filters und die verwendeten Parameter sind ausreichend, um die Netzwerkverbindung des routers mehr als zu sättigen, bei einer vernachlässigbaren Wahrscheinlichkeit für falsch positive Ergebnisse. Der eindeutige Wert, der in den Bloom-Filter eingespeist wird, ist das XOR des IV und des ersten Blocks, um zu verhindern, dass nicht aufeinanderfolgende kollaborierende Peers im tunnel eine Nachricht markieren können, indem sie sie mit vertauschtem IV und ersten Block erneut senden.

### Endpoint-Verarbeitung {#tunnel.endpoint}

Nachdem eine tunnel-Nachricht am letzten Hop im tunnel empfangen und validiert wurde, hängt die Art, wie der Endpunkt die vom Gateway codierten Daten wiederherstellt, davon ab, ob es sich um einen inbound oder outbound tunnel handelt. Bei outbound tunnels verschlüsselt der Endpunkt die Nachricht mit seinem Schichtschlüssel genau wie jeder andere Teilnehmer und legt dabei die vorverarbeiteten Daten frei. Bei inbound tunnels ist der Endpunkt auch der tunnel-Ersteller, sodass er lediglich iterativ den IV und die Nachricht entschlüsseln kann, indem er die Schicht- und IV-Schlüssel jedes Schritts in umgekehrter Reihenfolge verwendet.

An diesem Punkt hat der tunnel-Endpunkt die vorverarbeiteten Daten erhalten, die vom Gateway gesendet wurden, welche er dann in die enthaltenen I2NP-Nachrichten aufteilen und gemäß den Anweisungen in ihren Zustellungsanweisungen weiterleiten kann.

## Tunnel-Erstellung {#tunnel.building}

Beim Aufbau eines tunnels muss der Ersteller eine Anfrage mit den notwendigen Konfigurationsdaten an jeden der Hops senden und warten, bis alle zustimmen, bevor der tunnel aktiviert wird. Die Anfragen sind verschlüsselt, sodass nur die Peers, die eine Information benötigen (wie den tunnel-Layer oder IV-Schlüssel), diese Daten haben. Zusätzlich hat nur der tunnel-Ersteller Zugriff auf die Antwort des Peers. Es gibt drei wichtige Dimensionen zu beachten bei der Erstellung der tunnels: welche Peers verwendet werden (und wo), wie die Anfragen gesendet werden (und Antworten empfangen werden), und wie sie gewartet werden.

### Peer-Auswahl {#tunnel.peerselection}

Über die zwei Arten von tunneln - eingehende und ausgehende - hinaus gibt es zwei Stile der Peer-Auswahl, die für verschiedene tunnel verwendet werden - exploratory und client. Exploratory tunnel werden sowohl für die Wartung der Netzwerkdatenbank als auch für die Tunnel-Wartung verwendet, während client tunnel für End-to-End-Client-Nachrichten verwendet werden.

#### Exploratory Tunnel Peer-Auswahl {#tunnel.selection.exploratory}

Explorative tunnel werden aus einer zufälligen Auswahl von Peers aus einer Teilmenge des Netzwerks erstellt. Die jeweilige Teilmenge variiert je nach lokalem router und dessen tunnel-Routing-Anforderungen. Im Allgemeinen werden die explorativen tunnel aus zufällig ausgewählten Peers erstellt, die in der Profilkategorie "nicht ausgefallen, aber aktiv" des Peers stehen. Der sekundäre Zweck der tunnel, neben dem reinen tunnel-Routing, besteht darin, unterausgelastete Peers mit hoher Kapazität zu finden, damit diese für die Verwendung in Client-tunnels befördert werden können.

Die explorative Peer-Auswahl wird weiter auf der [Seite über Peer-Profiling und -Auswahl](/docs/overview/peer-selection) besprochen.

#### Client Tunnel Peer-Auswahl {#tunnel.selection.client}

Client-Tunnel werden mit strengeren Anforderungen erstellt - der lokale Router wählt Peers aus seiner "schnell und hohe Kapazität" Profilkategorie aus, damit Leistung und Zuverlässigkeit den Bedürfnissen der Client-Anwendung entsprechen. Es gibt jedoch mehrere wichtige Details über diese grundlegende Auswahl hinaus, die beachtet werden sollten, abhängig von den Anonymitätsbedürfnissen des Clients.

Die Client-Peer-Auswahl wird ausführlicher auf der [Peer-Profiling- und Auswahlseite](/docs/overview/peer-selection) behandelt.

#### Peer-Reihenfolge innerhalb von Tunneln {#ordering}

Peers sind innerhalb von tunnels geordnet, um mit dem [predecessor attack](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([2008 Update](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)) umzugehen.

Um den Vorgänger-Angriff zu vereiteln, hält die tunnel-Auswahl die ausgewählten Peers in einer strikten Reihenfolge - wenn A, B und C in einem tunnel für einen bestimmten tunnel-Pool sind, ist der Hop nach A immer B, und der Hop nach B ist immer C.

Die Anordnung wird implementiert, indem für jeden tunnel pool beim Start ein zufälliger 32-Byte-Schlüssel generiert wird. Peers sollten nicht in der Lage sein, die Anordnung zu erraten, da ein Angreifer andernfalls zwei router-Hashes mit großem Abstand zueinander erstellen könnte, um die Wahrscheinlichkeit zu maximieren, an beiden Enden eines tunnels zu stehen. Peers werden nach XOR-Distanz des SHA256-Hash von (dem Hash des Peers verknüpft mit dem zufälligen Schlüssel) vom zufälligen Schlüssel sortiert:

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Da jeder tunnel pool einen anderen zufälligen Schlüssel verwendet, ist die Reihenfolge innerhalb eines einzelnen Pools konsistent, jedoch nicht zwischen verschiedenen Pools. Neue Schlüssel werden bei jedem router-Neustart generiert.

### Request Delivery {#tunnel.request}

Ein Multi-Hop-Tunnel wird mit einer einzigen Build-Nachricht erstellt, die wiederholt entschlüsselt und weitergeleitet wird. In der Terminologie von [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) handelt es sich dabei um "nicht-interaktives" teleskopisches Tunnel-Building.

Diese Methode zur Vorbereitung, Übertragung und Antwort von tunnel-Anfragen ist [darauf ausgelegt](/docs/specs/tunnel-creation), die Anzahl der preisgegeben Vorgänger zu reduzieren, die Anzahl der übertragenen Nachrichten zu verringern, ordnungsgemäße Konnektivität zu verifizieren und den Nachrichtenzählungsangriff der traditionellen teleskopischen tunnel-Erstellung zu vermeiden. (Diese Methode, die Nachrichten sendet, um einen tunnel durch den bereits etablierten Teil des tunnels zu erweitern, wird im Paper "Hashing it out" als "interaktive" teleskopische tunnel-Erstellung bezeichnet.)

Die Details von tunnel-Anfrage- und Antwortnachrichten sowie deren Verschlüsselung [sind hier spezifiziert](/docs/specs/tunnel-creation).

Peers können Tunnel-Erstellungsanfragen aus verschiedenen Gründen ablehnen, wobei eine Serie von vier zunehmend schwerwiegenden Ablehnungen bekannt ist: probabilistische Ablehnung (aufgrund der Annäherung an die Kapazität des routers oder als Reaktion auf eine Flut von Anfragen), vorübergehende Überlastung, Bandbreiten-Überlastung und kritischer Ausfall. Wenn diese empfangen werden, werden sie vom Tunnel-Ersteller interpretiert, um das Profil des betreffenden routers entsprechend anzupassen.

Für weitere Informationen zur Peer-Bewertung siehe die [Peer Profiling and Selection Seite](/docs/overview/peer-selection).

### Tunnel-Pools {#tunnel.pooling}

Um einen effizienten Betrieb zu ermöglichen, verwaltet der router eine Reihe von tunnel-Pools, von denen jeder eine Gruppe von tunneln für einen bestimmten Zweck mit ihrer eigenen Konfiguration verwaltet. Wenn ein tunnel für diesen Zweck benötigt wird, wählt der router zufällig einen aus dem entsprechenden Pool aus. Insgesamt gibt es zwei explorative tunnel-Pools - einen eingehenden und einen ausgehenden - die jeweils die Standardkonfiguration des routers verwenden. Zusätzlich gibt es ein Paar von Pools für jedes lokale Ziel - einen eingehenden und einen ausgehenden tunnel-Pool. Diese Pools verwenden die Konfiguration, die angegeben wird, wenn sich das lokale Ziel über [I2CP](/docs/specs/i2cp) mit dem router verbindet, oder die Standardeinstellungen des routers, falls nichts angegeben ist.

Jeder Pool hat in seiner Konfiguration einige wichtige Einstellungen, die definieren, wie viele tunnels aktiv gehalten werden sollen, wie viele Backup-tunnels im Falle eines Ausfalls bereitgehalten werden sollen, wie lang die tunnels sein sollen, ob diese Längen randomisiert werden sollen, sowie alle anderen Einstellungen, die bei der Konfiguration einzelner tunnels erlaubt sind. Konfigurationsoptionen sind auf der [I2CP-Seite](/docs/specs/i2cp) spezifiziert.

### Tunnel-Längen und Standardwerte {#length}

[Auf der tunnel Übersichtsseite](/docs/overview/tunnel-routing#length).

### Vorausschauende Build-Strategie und Priorität {#strategy}

Der Aufbau von Tunnels ist kostspielig, und Tunnels laufen nach einer festen Zeit nach ihrem Aufbau ab. Wenn jedoch ein Pool keine Tunnels mehr hat, ist das Destination praktisch tot. Außerdem kann die Erfolgsrate beim Tunnel-Aufbau stark variieren, abhängig von sowohl lokalen als auch globalen Netzwerkbedingungen. Daher ist es wichtig, eine vorausschauende, adaptive Aufbaustrategie zu verfolgen, um sicherzustellen, dass neue Tunnels erfolgreich aufgebaut werden, bevor sie benötigt werden, ohne zu viele Tunnels zu bauen, sie zu früh zu bauen oder zu viel CPU oder Bandbreite für das Erstellen und Senden der verschlüsselten Aufbau-Nachrichten zu verbrauchen.

Für jedes Tupel {exploratory/client, in/out, Länge, Längenabweichung} führt der router Statistiken über die Zeit, die für einen erfolgreichen tunnel-Aufbau erforderlich ist. Anhand dieser Statistiken berechnet er, wie lange vor dem Ablauf eines tunnels er mit dem Versuch beginnen sollte, einen Ersatz zu erstellen. Wenn sich die Ablaufzeit nähert, ohne dass ein erfolgreicher Ersatz erstellt wurde, startet er mehrere Aufbauversuche parallel und erhöht dann bei Bedarf die Anzahl der parallelen Versuche.

Um die Bandbreite und CPU-Nutzung zu begrenzen, beschränkt der router auch die maximale Anzahl ausstehender Build-Versuche über alle Pools hinweg. Kritische Builds (die für explorative tunnel und für Pools, denen die tunnel ausgegangen sind) werden priorisiert.

## Tunnel Message Throttling {#tunnel.throttling}

Obwohl die Tunnel innerhalb von I2P einer leitungsvermittelten Netzwerkarchitektur ähneln, basiert alles innerhalb von I2P strikt auf Nachrichten - Tunnel sind lediglich buchhalterische Tricks, die dabei helfen, die Zustellung von Nachrichten zu organisieren. Es werden keine Annahmen bezüglich der Zuverlässigkeit oder Reihenfolge von Nachrichten gemacht, und Übertragungswiederholungen werden höheren Ebenen überlassen (z.B. der I2P-Client-Ebenen-Streaming-Bibliothek). Dies ermöglicht es I2P, Drosselungstechniken zu nutzen, die sowohl in paketvermittelten als auch in leitungsvermittelten Netzwerken verfügbar sind. Zum Beispiel kann jeder Router den gleitenden Durchschnitt verfolgen, wie viele Daten jeder Tunnel verwendet, dies mit allen Durchschnittswerten kombinieren, die von anderen Tunneln verwendet werden, an denen der Router teilnimmt, und in der Lage sein, zusätzliche Tunnel-Teilnahmeanfragen basierend auf seiner Kapazität und Auslastung anzunehmen oder abzulehnen. Andererseits kann jeder Router einfach Nachrichten verwerfen, die seine Kapazität überschreiten, und dabei die Forschung nutzen, die im normalen Internet verwendet wird.

In der aktuellen Implementierung verwenden router eine gewichtete zufällige frühe Verwerfungsstrategie (WRED). Für alle teilnehmenden router (interner Teilnehmer, eingehender Gateway und ausgehender Endpunkt) beginnt der router damit, einen Teil der Nachrichten zufällig zu verwerfen, wenn sich die Bandbreitenlimits nähern. Je näher der Verkehr an die Limits herankommt oder diese überschreitet, desto mehr Nachrichten werden verworfen. Für einen internen Teilnehmer werden alle Nachrichten fragmentiert und aufgefüllt und haben daher die gleiche Größe. Am eingehenden Gateway und ausgehenden Endpunkt wird die Verwerfungsentscheidung jedoch auf der vollständigen (zusammengeführten) Nachricht getroffen, und die Nachrichtengröße wird berücksichtigt. Größere Nachrichten werden eher verworfen. Außerdem werden Nachrichten eher am ausgehenden Endpunkt als am eingehenden Gateway verworfen, da diese Nachrichten nicht so "weit fortgeschritten" in ihrer Reise sind und daher die Netzwerkkosten für das Verwerfen dieser Nachrichten geringer sind.

## Zukünftige Arbeiten {#future}

### Mischen/Stapelverarbeitung {#tunnel.mixing}

Welche Strategien könnten am Gateway und an jedem Hop verwendet werden, um Nachrichten zu verzögern, neu zu ordnen, umzuleiten oder aufzufüllen? In welchem Umfang sollte dies automatisch erfolgen, wie viel sollte als tunnel- oder hop-spezifische Einstellung konfiguriert werden, und wie sollte der tunnel-Ersteller (und damit der Benutzer) diesen Vorgang kontrollieren? All dies bleibt ungeklärt und muss für eine zukünftige Version ausgearbeitet werden.

### Padding

Die Padding-Strategien können auf verschiedenen Ebenen eingesetzt werden, um die Preisgabe von Nachrichtengrößeninformationen an verschiedene Angreifer zu verhindern. Die aktuelle feste Tunnel-Nachrichtengröße beträgt 1024 Bytes. Innerhalb dieser werden die fragmentierten Nachrichten selbst jedoch überhaupt nicht vom Tunnel gepaddet, obwohl sie bei End-to-End-Nachrichten als Teil der garlic-Verpackung gepaddet werden können.

### WRED

WRED-Strategien haben einen erheblichen Einfluss auf die Ende-zu-Ende-Leistung und die Vermeidung von Netzwerküberlastungszusammenbrüchen. Die aktuelle WRED-Strategie sollte sorgfältig evaluiert und verbessert werden.
