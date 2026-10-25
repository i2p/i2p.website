---
title: "I2NP-Übersicht"
description: "Überblick über das I2P-Netzwerkprotokoll (I2NP) – Nachrichtenformat, Typen, Prioritäten und Größenbeschränkungen."
slug: "i2np-overview"
aliases:
  - "/de/docs/protocol/i2np"
  - "/de/docs/protocol/i2np/"
category: "Protokolle"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Übersicht

Das I2P-Netzwerkprotokoll (I2NP), das zwischen I2CP und den verschiedenen I2P-Transportprotokollen liegt, verwaltet das Routing und die Vermischung von Nachrichten zwischen Routern sowie die Auswahl der zu verwendenden Transporte, wenn mit einem Peer kommuniziert wird, für den mehrere gemeinsame Transporte unterstützt werden.

## I2NP-Definition

I2NP-(I2P-Netzwerkprotokoll-)Nachrichten können für Ein-Sprung-, Router-zu-Router-, Punkt-zu-Punkt-Nachrichten verwendet werden. Durch Verschlüsselung und Einbetten von Nachrichten in andere Nachrichten können sie sicher über mehrere Zwischenstationen an das endgültige Ziel gesendet werden. Die Priorität wird nur lokal am Ursprungsort verwendet, d. h. beim Warten auf den Ausgangsversand.

Die unten aufgeführten Prioritäten sind möglicherweise nicht aktuell und können sich ändern. Die Implementierung der Prioritätswarteschlangen kann variieren.

## Nachrichtenformat {#format}

Die folgende Tabelle legt den traditionellen 16-Byte-Header fest, der in NTCP verwendet wird. Die SSU- und NTCP2-Transportschichten verwenden modifizierte Header.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Type</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unique ID</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Checksum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Payload</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 - 61.2KB</td>
</tr>
</table>
Obwohl die maximale Nutzlastgröße nominell 64 KB beträgt, wird die Größe weiter durch die Methode eingeschränkt, I2NP-Nachrichten in mehrere 1-KB-Tunnelnachrichten aufzuteilen, wie auf der [Tunnel-Implementierungsseite](/docs/specs/tunnel-implementation/) beschrieben.

Die maximale Anzahl an Fragmenten beträgt 64, und die Nachricht ist möglicherweise nicht perfekt ausgerichtet, sodass die Nachricht nominell in 63 Fragmenten Platz haben muss.

Die maximale Größe eines anfänglichen Fragments beträgt 956 Bytes (unter der Annahme des TUNNEL-Liefermodus); die maximale Größe eines nachfolgenden Fragments beträgt 996 Bytes. Daher beträgt die maximale Größe ungefähr 956 + (62 × 996) = 62708 Bytes oder 61,2 KB.

Zusätzlich können die Transportschichten zusätzliche Beschränkungen aufweisen. Die NTCP-Begrenzung liegt bei 16KB - 6 = 16378 Bytes. Die SSU-Begrenzung beträgt etwa 32 KB. Die NTCP2-Begrenzung liegt bei etwa 64KB - 20 = 65516 Bytes, was höher ist als das, was ein Tunnel unterstützen kann.

Beachten Sie, dass dies nicht die Grenzwerte für Datagramme sind, die der Client wahrnimmt, da der Router ein Antwort-LeaseSet und/oder Sitzungstags zusammen mit der Client-Nachricht in einer Garlic-Nachricht bündeln kann. Das LeaseSet und die Tags können zusammen etwa 5,5 KB hinzufügen. Daher beträgt die aktuelle Datagramm-Grenze etwa 10 KB. Diese Grenze wird in einer zukünftigen Version erhöht werden.

## Nachrichtentypen {#types}

Eine höhere Prioritätsnummer bedeutet eine höhere Priorität. Der Großteil des Datenverkehrs besteht aus TunnelDataMessages (Priorität 400), sodass alles darüber im Wesentlichen hohe Priorität hat und alles darunter niedrige Priorität. Beachten Sie außerdem, dass viele Nachrichten im Allgemeinen über explorative Tunnel und nicht über Client-Tunnel weitergeleitet werden und sich daher möglicherweise nicht in derselben Warteschlange befinden, es sei denn, die ersten Hops liegen zufällig auf demselben Peer.

Außerdem werden nicht alle Nachrichtentypen unverschlüsselt gesendet. Beispielsweise umfasst der Router beim Testen eines Tunnels eine DeliveryStatusMessage, die in eine GarlicMessage eingepackt ist, die wiederum in eine DataMessage eingepackt ist.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Length</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Priority</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Comments</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookupMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">May vary</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseSearchReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Typ. 161</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Size is 65 + 32*(number of hashes) where typically, the hashes for three floodfill routers are returned.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseStoreMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">Varies</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">460</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary. Size is 898 bytes for a typical 2-lease leaseSet. RouterInfo structures are compressed, and size varies; however there is a continuing effort to reduce the amount of data published in a RouterInfo.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4 - 62080</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">425</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority may vary on a per-destination basis</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DeliveryStatusMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Used for message replies, and for testing tunnels - generally wrapped in a GarlicMessage</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/overview/garlic-routing/">GarlicMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generally wrapped in a DataMessage - but when unwrapped, given a priority of 100 by the forwarding router</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="/docs/specs/tunnel-creation/">TunnelBuildReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">4224</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelDataMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1028</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The most common message. Priority for tunnel participants, outbound endpoints, and inbound gateways was reduced to 200 as of release 0.6.1.33. Outbound gateway messages (i.e. those originated locally) remains at 400.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">TunnelGatewayMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300/400</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">500</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">VariableTunnelBuildReplyMessage</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">1057 - 4225</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">300</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Shorter TunnelBuildReplyMessage as of 0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Others (Types 0, 4-9, 12)</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: right;">0, 4-9, 12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Obsolete, Unused</td>
</tr>
</table>
## Tunnel-Test

Ab API-Version 0.9.68 vom Februar 2026 ist ein Tunnel-Test erforderlich, da Router es erlaubt ist, an Tunneln teilzunehmen, die nach den ersten zwei Minuten keinen Datenverkehr erhalten haben.

## Vollständige Protokollspezifikation

Siehe die [I2NP-Spezifikationsseite](/docs/specs/i2np/) für die vollständige Protokollspezifikation. Siehe auch die [Spezifikationsseite für gemeinsame Datenstrukturen](/docs/specs/common-structures/).

## Zukünftige Arbeiten

Es ist nicht klar, ob das derzeitige Prioritätenschema allgemein wirksam ist und ob die Prioritäten für verschiedene Nachrichten weiter angepasst werden sollten. Dies ist ein Thema für weitere Forschung, Analyse und Tests.
