---
title: "Alte Tunnel-Implementierung"
description: "Historische Dokumentation der ursprünglichen tunnel-Implementierung von I2P vor Version 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/de/docs/historical/tunnel-alt"
  - "/de/docs/historical/tunnel-alt/"
  - "/de/tunnel"
  - "/de/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Hinweis: Veraltet - NICHT verwendet! Ersetzt in 0.6.1.10 - siehe [aktuelle Implementierung](/docs/specs/tunnel-implementation) für die aktive Spezifikation.**

## 1) Tunnel-Übersicht {#tunnel.overview}

Innerhalb von I2P werden Nachrichten in eine Richtung durch einen virtuellen tunnel aus Peers geleitet, wobei alle verfügbaren Mittel genutzt werden, um die Nachricht an den nächsten Hop weiterzuleiten. Nachrichten kommen am Gateway des tunnels an, werden für den Pfad gebündelt und an den nächsten Hop im tunnel weitergeleitet, der die Gültigkeit der Nachricht verarbeitet und überprüft und sie an den nächsten Hop weitersendet, und so weiter, bis sie den tunnel-Endpunkt erreicht. Dieser Endpunkt nimmt die vom Gateway gebündelten Nachrichten und leitet sie wie angewiesen weiter - entweder an einen anderen router, an einen anderen tunnel auf einem anderen router oder lokal.

Tunnels funktionieren alle gleich, können aber in zwei verschiedene Gruppen unterteilt werden - eingehende Tunnels und ausgehende Tunnels. Die eingehenden Tunnels haben ein nicht vertrauenswürdiges Gateway, das Nachrichten nach unten zum tunnel-Ersteller weiterleitet, der als tunnel-Endpunkt dient. Bei ausgehenden Tunnels dient der tunnel-Ersteller als Gateway und leitet Nachrichten zum entfernten Endpunkt weiter.

Der Ersteller des tunnels wählt genau aus, welche Peers am tunnel teilnehmen werden, und stellt jedem die notwendigen Konfigurationsdaten zur Verfügung. Sie können in der Länge von 0 Hops (wo das Gateway auch der Endpunkt ist) bis zu 7 Hops (wo es 6 Peers nach dem Gateway und vor dem Endpunkt gibt) variieren. Es ist beabsichtigt, es sowohl für Teilnehmer als auch für Dritte schwer zu machen, die Länge eines tunnels zu bestimmen, oder sogar für kollidierende Teilnehmer zu bestimmen, ob sie überhaupt Teil desselben tunnels sind (abgesehen von der Situation, wo kollidierende Peers nebeneinander im tunnel stehen). Nachrichten, die beschädigt wurden, werden ebenfalls so schnell wie möglich verworfen, um die Netzwerklast zu reduzieren.

Über ihre Länge hinaus gibt es zusätzliche konfigurierbare Parameter für jeden tunnel, die verwendet werden können, wie etwa eine Drosselung der Größe oder Häufigkeit der übermittelten Nachrichten, wie Padding verwendet werden soll, wie lange ein tunnel in Betrieb sein soll, ob Störnachrichten eingefügt werden sollen, ob Fragmentierung verwendet werden soll und welche Stapelverarbeitungsstrategien, falls vorhanden, eingesetzt werden sollen.

In der Praxis wird eine Reihe von tunnel-Pools für verschiedene Zwecke verwendet - jedes lokale Client-Ziel hat seinen eigenen Satz von eingehenden tunnels und ausgehenden tunnels, die so konfiguriert sind, dass sie seinen Anonymitäts- und Leistungsanforderungen entsprechen. Zusätzlich unterhält der router selbst eine Reihe von Pools für die Teilnahme an der netDb und für die Verwaltung der tunnels selbst.

I2P ist ein von Natur aus paketvermitteltes Netzwerk, auch mit diesen tunnels, wodurch es mehrere parallel laufende tunnels nutzen kann, was die Widerstandsfähigkeit erhöht und die Last verteilt. Außerhalb der I2P-Kernschicht steht eine optionale Ende-zu-Ende-Streaming-Bibliothek für Client-Anwendungen zur Verfügung, die TCP-ähnliche Funktionen bereitstellt, einschließlich Nachrichtenumsortierung, Neuübertragung, Überlastungskontrolle usw.

## 2) tunnel-Betrieb {#tunnel.operation}

Der tunnel-Betrieb umfasst vier verschiedene Prozesse, die von verschiedenen Peers im tunnel übernommen werden. Zunächst sammelt das tunnel-Gateway eine Anzahl von tunnel-Nachrichten und verarbeitet sie vor zu etwas für die tunnel-Übertragung. Als nächstes verschlüsselt das Gateway diese vorverarbeiteten Daten und leitet sie an den ersten Hop weiter. Dieser Peer und nachfolgende tunnel-Teilnehmer entfernen eine Schicht der Verschlüsselung, überprüfen die Integrität der Nachricht und leiten sie dann an den nächsten Peer weiter. Schließlich kommt die Nachricht am Endpunkt an, wo die vom Gateway gebündelten Nachrichten wieder aufgeteilt und wie angefordert weitergeleitet werden.

Tunnel-IDs sind 4-Byte-Zahlen, die an jedem Hop verwendet werden - Teilnehmer wissen, auf welche tunnel ID sie bei Nachrichten hören müssen und mit welcher tunnel ID diese an den nächsten Hop weitergeleitet werden sollen. Tunnels selbst sind kurzlebig (derzeit 10 Minuten), aber je nach Zweck des tunnels und obwohl nachfolgende tunnels möglicherweise mit derselben Reihenfolge von Peers erstellt werden, ändert sich die tunnel ID jedes Hops.

### 2.1) Nachrichtenvorverarbeitung {#tunnel.preprocessing}

Wenn das Gateway Daten durch den tunnel übertragen möchte, sammelt es zunächst null oder mehr I2NP-Nachrichten (nicht mehr als 32KB), wählt aus, wie viel Padding verwendet wird, und entscheidet, wie jede I2NP-Nachricht vom tunnel-Endpunkt behandelt werden soll, wobei diese Daten in die rohe tunnel-Nutzlast kodiert werden:

- 2-Byte vorzeichenlose Ganzzahl, die die Anzahl der Padding-Bytes angibt
- so viele zufällige Bytes
- eine Reihe von null oder mehr { Anweisungen, Nachricht } Paaren

Die Anweisungen sind wie folgt kodiert:

- 1 Byte Wert:
  ```
  Bits 0-1: Zustellungstyp
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     Bit 2: Verzögerung enthalten?  (1 = wahr, 0 = falsch)
     Bit 3: fragmentiert?  (1 = wahr, 0 = falsch)
     Bit 4: erweiterte Optionen?  (1 = wahr, 0 = falsch)
  Bits 5-7: reserviert
  ```
- falls der Zustellungstyp TUNNEL war, eine 4 Byte tunnel ID
- falls der Zustellungstyp TUNNEL oder ROUTER war, ein 32 Byte router Hash
- falls das Flag "Verzögerung enthalten" wahr ist, ein 1 Byte Wert:
  ```
     Bit 0: Typ (0 = strikt, 1 = zufällig)
  Bits 1-7: Verzögerungsexponent (2^Wert Minuten)
  ```
- falls das Flag "fragmentiert" wahr ist, eine 4 Byte Nachrichten-ID und ein 1 Byte Wert:
  ```
  Bits 0-6: Fragmentnummer
     Bit 7: ist letztes?  (1 = wahr, 0 = falsch)
  ```
- falls das Flag "erweiterte Optionen" wahr ist:
  ```
  = eine 1 Byte Optionsgröße (in Bytes)
  = entsprechend viele Bytes
  ```
- 2 Byte Größe der I2NP Nachricht

Die I2NP-Nachricht wird in ihrer Standardform codiert, und die vorverarbeitete Nutzlast muss auf ein Vielfaches von 16 Bytes aufgefüllt werden.

### 2.2) Gateway-Verarbeitung {#tunnel.gateway}

Nach der Vorverarbeitung von Nachrichten in eine gepolsterte Nutzlast verschlüsselt das Gateway die Nutzlast mit den acht Schlüsseln und erstellt einen Prüfsummenblock, damit jeder Peer die Integrität der Nutzlast jederzeit überprüfen kann, sowie einen Ende-zu-Ende-Verifizierungsblock für den tunnel-Endpunkt zur Überprüfung der Integrität des Prüfsummenblocks. Die spezifischen Details folgen.

Die verwendete Verschlüsselung ist so konzipiert, dass die Entschlüsselung lediglich erfordert, die Daten mit AES im CBC-Modus zu verarbeiten, den SHA256 eines bestimmten festen Teils der Nachricht zu berechnen (Bytes 16 bis $size-144) und nach den ersten 16 Bytes dieses Hashes im Prüfsummenblock zu suchen. Es ist eine feste Anzahl von Hops definiert (8 Peers), sodass wir die Nachricht verifizieren können, ohne dabei die Position im tunnel preiszugeben oder die Nachricht kontinuierlich "schrumpfen" zu lassen, während Schichten abgezogen werden. Für tunnels, die kürzer als 8 Hops sind, übernimmt der tunnel-Ersteller den Platz der überschüssigen Hops und entschlüsselt mit seinen Schlüsseln (bei ausgehenden tunnels wird dies am Anfang gemacht, bei eingehenden tunnels am Ende).

Der schwierige Teil bei der Verschlüsselung ist die Erstellung dieses verschachtelten Prüfsummenblocks, was im Wesentlichen erfordert herauszufinden, wie der Hash der Nutzdaten bei jedem Schritt aussehen wird, diese Hashes zufällig zu ordnen und dann eine Matrix zu erstellen, die zeigt, wie jeder dieser zufällig geordneten Hashes bei jedem Schritt aussehen wird. Das Gateway selbst muss so tun, als wäre es einer der Peers innerhalb des Prüfsummenblocks, damit der erste Hop nicht erkennen kann, dass der vorherige Hop das Gateway war. Um dies zu veranschaulichen:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
Im obigen Beispiel ist P[7] dasselbe wie die ursprünglichen Daten, die durch den tunnel geleitet werden (die vorverarbeiteten Nachrichten), und V[7] sind die ersten 16 Bytes des SHA256 von eH[0-7], wie sie auf peer7 nach der Entschlüsselung zu sehen sind. Für Zellen in der Matrix, die "höher" als der Hash stehen, wird ihr Wert abgeleitet, indem die Zelle darunter mit dem Schlüssel für den peer darunter verschlüsselt wird, wobei das Ende der Spalte links davon als IV verwendet wird. Für Zellen in der Matrix, die "niedriger" als der Hash stehen, sind sie gleich der Zelle darüber, entschlüsselt mit dem Schlüssel des aktuellen peers, wobei das Ende des vorherigen verschlüsselten Blocks in dieser Zeile verwendet wird.

Mit dieser randomisierten Matrix von Checksum-Blöcken kann jeder Peer den Hash der Nutzdaten finden, oder falls dieser nicht vorhanden ist, erkennen, dass die Nachricht beschädigt ist. Die Verflechtung durch die Verwendung des CBC-Modus erhöht die Schwierigkeit beim Markieren der Checksum-Blöcke selbst, aber es ist immer noch möglich, dass diese Markierung kurzzeitig unentdeckt bleibt, wenn die Spalten nach den markierten Daten bereits zur Überprüfung der Nutzdaten bei einem Peer verwendet wurden. In jedem Fall weiß der tunnel-Endpunkt (Peer 7) mit Sicherheit, ob einer der Checksum-Blöcke markiert wurde, da dies den Verifizierungsblock (V[7]) beschädigen würde.

Der IV[0] ist ein zufälliger 16-Byte-Wert, und IV[i] sind die ersten 16 Bytes von H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Wir verwenden nicht denselben IV entlang des Pfades, da dies triviale Kollusion ermöglichen würde, und wir nutzen den Hash des entschlüsselten Wertes zur IV-Fortpflanzung, um Schlüsselleckagen zu erschweren. IV_WHITENER ist ein fester 16-Byte-Wert.

Wenn das Gateway die Nachricht senden möchte, exportiert es die richtige Zeile für den Peer, der der erste Hop ist (normalerweise die peer1.recv Zeile) und leitet diese vollständig weiter.

### 2.3) Teilnehmer-Verarbeitung {#tunnel.participant}

Wenn ein Teilnehmer in einem tunnel eine Nachricht erhält, entschlüsselt er eine Schicht mit seinem tunnel-Schlüssel unter Verwendung von AES256 im CBC-Modus mit den ersten 16 Bytes als IV. Dann berechnet er den Hash dessen, was er als Payload sieht (Bytes 16 bis $size-144) und sucht nach den ersten 16 Bytes dieses Hashes innerhalb des entschlüsselten Prüfsummenblocks. Wenn keine Übereinstimmung gefunden wird, wird die Nachricht verworfen. Andernfalls wird der IV aktualisiert, indem er entschlüsselt wird, dieser Wert mit dem IV_WHITENER XOR-verknüpft wird und durch die ersten 16 Bytes seines Hashes ersetzt wird. Die resultierende Nachricht wird dann zur Verarbeitung an den nächsten Peer weitergeleitet.

Um Replay-Angriffe auf tunnel-Ebene zu verhindern, verfolgt jeder Teilnehmer die während der Lebensdauer des tunnels empfangenen IVs und weist Duplikate zurück. Der erforderliche Speicherverbrauch sollte gering sein, da jeder tunnel nur eine sehr kurze Lebensdauer hat (derzeit 10 Minuten). Ein konstanter Durchsatz von 100KBps durch einen tunnel mit vollen 32KB-Nachrichten würde 1875 Nachrichten ergeben und weniger als 30KB Speicher benötigen. Gateways und Endpunkte handhaben Replays, indem sie die Nachrichten-IDs und Ablaufzeiten der im tunnel enthaltenen I2NP-Nachrichten verfolgen.

### 2.4) Endpunkt-Verarbeitung {#tunnel.endpoint}

Wenn eine Nachricht den tunnel-Endpunkt erreicht, entschlüsselt und verifiziert er sie wie ein normaler Teilnehmer. Wenn der Prüfsummenblock eine gültige Übereinstimmung hat, berechnet der Endpunkt dann den Hash des Prüfsummenblocks selbst (wie nach der Entschlüsselung zu sehen) und vergleicht diesen mit dem entschlüsselten Verifikations-Hash (die letzten 16 Bytes). Wenn dieser Verifikations-Hash nicht übereinstimmt, nimmt der Endpunkt den Markierungsversuch durch einen der tunnel-Teilnehmer zur Kenntnis und verwirft möglicherweise die Nachricht.

An diesem Punkt hat der Tunnel-Endpunkt die vorverarbeiteten Daten, die vom Gateway gesendet wurden, welche er dann in die enthaltenen I2NP-Nachrichten aufteilen und entsprechend ihren Zustellungsanweisungen weiterleiten kann.

### 2.5) Padding {#tunnel.padding}

Verschiedene tunnel-Padding-Strategien sind möglich, jede mit ihren eigenen Vorteilen:

- Kein Padding
- Padding auf eine zufällige Größe
- Padding auf eine feste Größe
- Padding auf das nächstliegende KB
- Padding auf die nächstliegende exponentielle Größe (2^n Bytes)

*Welches verwenden? Kein Padding ist am effizientesten, zufälliges Padding ist das, was wir jetzt haben, feste Größe wäre entweder eine extreme Verschwendung oder würde uns zwingen, Fragmentierung zu implementieren. Padding auf die nächste exponentielle Größe (wie bei Freenet) scheint vielversprechend. Vielleicht sollten wir einige Statistiken im Netz sammeln, um zu sehen, welche Größe Nachrichten haben, und dann schauen, welche Kosten und Vorteile sich aus verschiedenen Strategien ergeben würden?*

### 2.6) Tunnel-Fragmentierung {#tunnel.fragmentation}

Für verschiedene Padding- und Mixing-Verfahren kann es aus Anonymitätssicht nützlich sein, eine einzelne I2NP-Nachricht in mehrere Teile zu fragmentieren, die jeweils separat durch verschiedene tunnel-Nachrichten übertragen werden. Der Endpunkt kann diese Fragmentierung unterstützen oder auch nicht (Fragmente nach Bedarf verwerfen oder zwischenspeichern), und die Behandlung von Fragmentierung wird nicht sofort implementiert werden.

### 2.7) Alternativen {#tunnel.alternatives}

#### 2.7.1) Verwenden Sie keinen Checksum-Block {#tunnel.nochecksum}

Eine Alternative zu dem oben beschriebenen Prozess wäre es, den Prüfsummenblock komplett zu entfernen und den Verifikations-Hash durch einen einfachen Hash der Nutzdaten zu ersetzen. Dies würde die Verarbeitung am tunnel-Gateway vereinfachen und 144 Bytes Bandbreite an jedem Hop einsparen. Andererseits könnten Angreifer innerhalb des tunnels die Nachrichtengröße trivial auf eine anpassen, die von kollaborierenden externen Beobachtern zusätzlich zu späteren tunnel-Teilnehmern leicht nachverfolgbar ist. Die Beschädigung würde auch die Verschwendung der gesamten Bandbreite zur Folge haben, die für die Weiterleitung der Nachricht erforderlich ist. Ohne die Validierung pro Hop wäre es auch möglich, übermäßige Netzwerkressourcen zu verbrauchen, indem extrem lange tunnel gebaut werden oder Schleifen in den tunnel eingebaut werden.

#### 2.7.2) Tunnel-Verarbeitung während der Laufzeit anpassen {#tunnel.reroute}

Während der einfache Tunnel-Routing-Algorithmus für die meisten Fälle ausreichend sein sollte, gibt es drei Alternativen, die erforscht werden können:

- Eine Nachricht innerhalb eines tunnel an einem beliebigen Hop für entweder eine bestimmte Zeitspanne oder einen randomisierten Zeitraum verzögern. Dies könnte erreicht werden, indem der Hash im Checksum-Block durch z.B. die ersten 8 Bytes des Hash ersetzt wird, gefolgt von einigen Verzögerungsanweisungen. Alternativ könnten die Anweisungen dem Teilnehmer mitteilen, die rohe Payload tatsächlich so zu interpretieren, wie sie ist, und entweder die Nachricht zu verwerfen oder sie weiter den Pfad entlang zu leiten (wo sie vom Endpunkt als Chaff-Nachricht interpretiert würde). Der letztere Teil würde erfordern, dass das Gateway seinen Verschlüsselungsalgorithmus anpasst, um die Klartext-Payload an einem anderen Hop zu erzeugen, aber es sollte nicht viel Aufwand sein.

- Erlauben Sie Routern, die an einem tunnel teilnehmen, die Nachricht vor der Weiterleitung zu remixen - indem sie diese durch einen der eigenen ausgehenden tunnels des Peers leiten, mit Anweisungen für die Zustellung an den nächsten Hop. Dies könnte entweder auf kontrollierte Weise (mit unterwegs erteilten Anweisungen wie den oben genannten Verzögerungen) oder probabilistisch verwendet werden.

- Code für den tunnel creator implementieren, um den "next hop" eines Peers im tunnel neu zu definieren und weitere dynamische Umleitung zu ermöglichen.

#### 2.7.3) Bidirektionale tunnel verwenden {#tunnel.bidirectional}

Die aktuelle Strategie, zwei separate Tunnel für eingehende und ausgehende Kommunikation zu verwenden, ist nicht die einzige verfügbare Technik und hat Auswirkungen auf die Anonymität. Auf der positiven Seite verringert die Verwendung separater Tunnel die Verkehrsdaten, die zur Analyse den Teilnehmern in einem Tunnel zugänglich gemacht werden - zum Beispiel würden Peers in einem ausgehenden Tunnel von einem Webbrowser nur den Verkehr eines HTTP GET sehen, während die Peers in einem eingehenden Tunnel die über den Tunnel übertragene Nutzlast sehen würden. Bei bidirektionalen Tunneln hätten alle Teilnehmer Zugang zu der Tatsache, dass z.B. 1KB in eine Richtung gesendet wurden, dann 100KB in die andere. Auf der negativen Seite bedeutet die Verwendung unidirektionaler Tunnel, dass es zwei Gruppen von Peers gibt, die profiliert und berücksichtigt werden müssen, und zusätzliche Sorgfalt muss aufgewendet werden, um die erhöhte Geschwindigkeit von Vorgängerangriffen zu adressieren. Der unten beschriebene Tunnel-Pooling- und Aufbauprozess sollte die Sorgen über den Vorgängerangriff minimieren, obwohl es, falls gewünscht, nicht viel Aufwand wäre, sowohl die eingehenden als auch die ausgehenden Tunnel entlang derselben Peers aufzubauen.

#### 2.7.4) Kleinere Blockgröße verwenden {#tunnel.smallerhashes}

Derzeit beschränkt unsere Verwendung von AES unsere Blockgröße auf 16 Bytes, was wiederum die Mindestgröße für jede der Prüfsummenblock-Spalten vorgibt. Falls ein anderer Algorithmus mit einer kleineren Blockgröße verwendet würde oder anderweitig den sicheren Aufbau des Prüfsummenblocks mit kleineren Hash-Teilen ermöglichen könnte, wäre es möglicherweise wert, dies zu untersuchen. Die 16 Bytes, die derzeit bei jedem Hop verwendet werden, sollten mehr als ausreichend sein.

## 3) Tunnel-Aufbau {#tunnel.building}

Beim Aufbau eines tunnels muss der Ersteller eine Anfrage mit den notwendigen Konfigurationsdaten an jeden der Hops senden und dann warten, bis der potenzielle Teilnehmer antwortet und mitteilt, ob er zustimmt oder nicht zustimmt. Diese tunnel-Anfragenachrichten und ihre Antworten sind garlic-verpackt, sodass nur der router, der den Schlüssel kennt, sie entschlüsseln kann, und der Pfad in beide Richtungen wird ebenfalls über tunnel geroutet. Es gibt drei wichtige Dimensionen, die beim Erstellen der tunnel zu beachten sind: welche Peers verwendet werden (und wo), wie die Anfragen gesendet werden (und Antworten empfangen werden), und wie sie gewartet werden.

### 3.1) Peer-Auswahl {#tunnel.peerselection}

Neben den zwei Arten von Tunneln - eingehend und ausgehend - gibt es zwei Stile der Peer-Auswahl, die für verschiedene Tunnel verwendet werden - exploratory und client. Exploratory tunnels werden sowohl für die Wartung der Netzwerkdatenbank als auch für die Tunnel-Wartung verwendet, während client tunnels für Ende-zu-Ende-Client-Nachrichten verwendet werden.

#### 3.1.1) Peer-Auswahl für explorative tunnel {#tunnel.selection.exploratory}

Explorative tunnel werden aus einer zufälligen Auswahl von Peers aus einer Teilmenge des Netzwerks erstellt. Die jeweilige Teilmenge variiert je nach lokalem router und dessen tunnel-Routing-Anforderungen. Im Allgemeinen werden explorative tunnel aus zufällig ausgewählten Peers erstellt, die in die Profilkategorie "nicht fehlerhaft aber aktiv" des Peers fallen. Der sekundäre Zweck der tunnel, über das reine tunnel-Routing hinaus, besteht darin, unterausgelastete Peers mit hoher Kapazität zu finden, damit diese für die Verwendung in Client-tunnel befördert werden können.

#### 3.1.2) Client tunnel Peer-Auswahl {#tunnel.selection.client}

Client-Tunnel werden mit strengeren Anforderungen gebaut - der lokale router wählt Peers aus seiner "schnell und hohe Kapazität" Profilkategorie aus, damit Leistung und Zuverlässigkeit den Anforderungen der Client-Anwendung entsprechen. Es gibt jedoch mehrere wichtige Details über diese grundlegende Auswahl hinaus, die je nach den Anonymitätsbedürfnissen des Clients beachtet werden sollten.

Für einige Clients, die sich Sorgen über Angreifer machen, die einen predecessor attack ausführen, kann die tunnel-Auswahl die ausgewählten Peers in einer strikten Reihenfolge beibehalten - wenn A, B und C in einem tunnel sind, ist der Hop nach A immer B, und der Hop nach B ist immer C. Eine weniger strikte Reihenfolge ist ebenfalls möglich, die sicherstellt, dass der Hop nach A zwar B sein kann, B aber niemals vor A stehen darf. Weitere Konfigurationsoptionen umfassen die Möglichkeit, dass nur die Eingangsgateways der eingehenden tunnel und die Endpunkte der ausgehenden tunnel fest oder nach einer MTBF-Rate rotiert werden.

### 3.2) Anfragezustellung {#tunnel.request}

Wie oben erwähnt, baut der tunnel-Ersteller, sobald er weiß, welche Peers in einen tunnel gehören und in welcher Reihenfolge, eine Reihe von tunnel-Anfragenachrichten auf, die jeweils die notwendigen Informationen für diesen Peer enthalten. Beispielsweise erhalten teilnehmende tunnels die 4-Byte-tunnel-ID, auf der sie Nachrichten empfangen sollen, die 4-Byte-tunnel-ID, auf der sie die Nachrichten senden sollen, den 32-Byte-Hash der Identität des nächsten Hops und den 32-Byte-Schichtschlüssel, der verwendet wird, um eine Schicht vom tunnel zu entfernen. Natürlich erhalten outbound tunnel-Endpunkte keine "nächster Hop"- oder "nächste tunnel-ID"-Informationen. Inbound tunnel-Gateways erhalten jedoch die 8 Schichtschlüssel in der Reihenfolge, in der sie verschlüsselt werden sollen (wie oben beschrieben). Um Antworten zu ermöglichen, enthält die Anfrage einen zufälligen Session-Tag und einen zufälligen Session-Schlüssel, mit dem der Peer seine Entscheidung per garlic encryption verschlüsseln kann, sowie den tunnel, an den diese garlic-Nachricht gesendet werden soll. Zusätzlich zu den oben genannten Informationen können verschiedene client-spezifische Optionen enthalten sein, wie z.B. welche Drosselung auf den tunnel angewendet werden soll, welche Padding- oder Batch-Strategien verwendet werden sollen, usw.

Nachdem alle Anfragenachrichten erstellt wurden, werden sie per garlic encryption für den Ziel-router verpackt und über einen explorativen tunnel gesendet. Nach dem Empfang bestimmt dieser Peer, ob er teilnehmen kann oder will, erstellt eine Antwortnachricht und verpackt die Antwort sowohl per garlic encryption als auch per tunnel-routing mit den bereitgestellten Informationen. Nach dem Empfang der Antwort beim tunnel-Ersteller wird der tunnel auf diesem Hop als gültig betrachtet (falls akzeptiert). Sobald alle Peers zugestimmt haben, ist der tunnel aktiv.

### 3.3) Pooling {#tunnel.pooling}

Um einen effizienten Betrieb zu ermöglichen, unterhält der router eine Reihe von tunnel-Pools, die jeweils eine Gruppe von tunnels für einen bestimmten Zweck mit ihrer eigenen Konfiguration verwalten. Wenn ein tunnel für diesen Zweck benötigt wird, wählt der router zufällig einen aus dem entsprechenden Pool aus. Insgesamt gibt es zwei explorative tunnel-Pools - einen eingehenden und einen ausgehenden - die jeweils die Erkundungsstandards des routers verwenden. Zusätzlich gibt es ein Paar von Pools für jedes lokale Ziel - einen eingehenden und einen ausgehenden tunnel. Diese Pools verwenden die Konfiguration, die beim Verbinden des lokalen Ziels mit dem router angegeben wurde, oder die Standards des routers, falls nicht spezifiziert.

Jeder Pool hat in seiner Konfiguration einige wichtige Einstellungen, die definieren, wie viele tunnel aktiv gehalten werden sollen, wie viele Backup-tunnel für den Fall eines Ausfalls bereitgehalten werden sollen, wie häufig die tunnel getestet werden sollen, wie lang die tunnel sein sollen, ob diese Längen randomisiert werden sollen, wie oft Ersatz-tunnel erstellt werden sollen, sowie alle anderen Einstellungen, die bei der Konfiguration einzelner tunnel erlaubt sind.

### 3.4) Alternativen {#tunnel.building.alternatives}

#### 3.4.1) Teleskopisches Erstellen {#tunnel.building.telescoping}

Eine Frage, die bezüglich der Verwendung der explorativen tunnel für das Senden und Empfangen von Tunnel-Erstellungsnachrichten aufkommen könnte, ist, wie sich das auf die Anfälligkeit des tunnels für Vorgängerangriffe auswirkt. Während die Endpunkte und gateways dieser tunnel zufällig über das Netzwerk verteilt sein werden (möglicherweise sogar einschließlich des Tunnel-Erstellers in dieser Menge), ist eine andere Alternative, die Tunnel-Pfade selbst zu verwenden, um die Anfrage und Antwort weiterzuleiten, wie es in [TOR](https://www.torproject.org/) gemacht wird. Dies könnte jedoch zu Lecks während der Tunnel-Erstellung führen und Peers erlauben zu entdecken, wie viele Hops später im tunnel sind, indem sie das Timing oder die Paketanzahl überwachen, während der tunnel aufgebaut wird. Techniken könnten verwendet werden, um dieses Problem zu minimieren, wie zum Beispiel jeden der Hops als Endpunkte (gemäß [2.7.2](#tunnel.reroute)) für eine zufällige Anzahl von Nachrichten zu verwenden, bevor mit dem Aufbau des nächsten Hops fortgefahren wird.

#### 3.4.2) Nicht-explorative tunnels für das Management {#tunnel.building.nonexploratory}

Eine zweite Alternative zum tunnel-Erstellungsprozess besteht darin, dem router einen zusätzlichen Satz von nicht-explorativen eingehenden und ausgehenden Pools zu geben, die für die tunnel-Anfrage und -Antwort verwendet werden. Unter der Annahme, dass der router eine gut integrierte Sicht auf das Netzwerk hat, sollte dies nicht notwendig sein, aber wenn der router auf irgendeine Weise partitioniert war, würde die Verwendung nicht-explorativer Pools für das tunnel-Management die Preisgabe von Informationen darüber reduzieren, welche Peers sich in der Partition des routers befinden.

## 4) Tunnel-Drosselung {#tunnel.throttling}

Obwohl die tunnel innerhalb von I2P einer leitungsvermittelten Netzwerkstruktur ähneln, basiert alles innerhalb von I2P strikt auf Nachrichten - tunnel sind lediglich buchhalterische Tricks, um die Zustellung von Nachrichten zu organisieren. Es werden keine Annahmen bezüglich Zuverlässigkeit oder Reihenfolge von Nachrichten gemacht, und Wiederübertragungen werden höheren Ebenen überlassen (z.B. I2Ps Client-Layer-Streaming-Bibliothek). Dies ermöglicht es I2P, Drosselungstechniken zu nutzen, die sowohl bei paketvermittelten als auch bei leitungsvermittelten Netzwerken verfügbar sind. Beispielsweise kann jeder router den gleitenden Durchschnitt verfolgen, wie viele Daten jeder tunnel verwendet, dies mit allen Durchschnittswerten kombinieren, die von anderen tunneln verwendet werden, an denen der router beteiligt ist, und in der Lage sein, zusätzliche tunnel-Teilnahmeanfragen basierend auf seiner Kapazität und Auslastung zu akzeptieren oder abzulehnen. Andererseits kann jeder router einfach Nachrichten verwerfen, die seine Kapazität übersteigen, und dabei die Forschung nutzen, die im normalen Internet verwendet wird.

## 5) Mischung/Stapelverarbeitung {#tunnel.mixing}

Welche Strategien sollten am Gateway und an jedem Hop verwendet werden, um Nachrichten zu verzögern, neu zu ordnen, umzuleiten oder aufzufüllen? In welchem Umfang sollte dies automatisch geschehen, wie viel sollte als Einstellung pro tunnel oder pro Hop konfiguriert werden, und wie sollte der Ersteller des tunnels (und wiederum der Benutzer) diesen Vorgang steuern? All dies bleibt unbekannt und muss für eine zukünftige Version ausgearbeitet werden.
