---
title: "Přehled I2NP"
description: "Přehled protokolu sítě I2P (I2NP) – formát zpráv, typy, priority a omezení velikosti."
slug: "i2np-overview"
aliases:
  - "/cs/docs/protocol/i2np"
  - "/cs/docs/protocol/i2np/"
  - "/cs/i2np"
  - "/cs/i2np/"
category: "Protocols"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Přehled

I2P síťový protokol (I2NP), který je umístěn mezi I2CP a různými přenosovými protokoly I2P, spravuje směrování a mixování zpráv mezi směrovači, stejně jako výběr přenosových protokolů pro komunikaci se sousedem, pokud je podporováno více společných přenosových protokolů.

## Definice I2NP

Zprávy I2NP (I2P Network Protocol) lze použít pro zprávy typu jedno skoknutí, směrovač-směrovač, bod-bod. Šifrováním a zabalením zpráv do jiných zpráv je lze bezpečným způsobem odeslat přes více skoků až k cílovému místu určení. Priorita se používá pouze lokálně na původním místě, tj. při zařazování do fronty pro odchozí doručení.

Uvedené priority nemusí být aktuální a mohou být změněny. Implementace fronty priorit se může lišit.

## Formát zprávy {#format}

Následující tabulka uvádí tradiční 16bajtovou hlavičku používanou v NTCP. Přenosy SSU a NTCP2 používají upravené hlavičky.

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
I když je maximální velikost dat nominálně 64 KB, skutečná velikost je dále omezena způsobem fragmentace zpráv I2NP do více 1 KB velkých tunelových zpráv, jak je popsáno na [stránce s popisem implementace tunelů](/docs/specs/tunnel-implementation/).

Maximální počet fragmentů je 64 a zpráva nemusí být dokonale zarovnána, takže musí teoreticky vejít do 63 fragmentů.

Maximální velikost počátečního fragmentu je 956 bajtů (za předpokladu doručování přes TUNNEL); maximální velikost následného fragmentu je 996 bajtů. Celková maximální velikost je tedy přibližně 956 + (62 × 996) = 62708 bajtů, neboli 61,2 KB.

Kromě toho mohou mít přenosy další omezení. Limit NTCP je 16 KB - 6 = 16378 bajtů. Limit SSU je přibližně 32 KB. Limit NTCP2 je přibližně 64 KB - 20 = 65516 bajtů, což je vyšší hodnota, než jakou může tunel podporovat.

Vezměte prosím na vědomí, že to nejsou limity pro datagramy, které vidí klient, protože směrovač může seskupit reply leaseset a/nebo session tags spolu se zprávou klienta do jedné garlic zprávy. Leaseset a tagy dohromady mohou přidat přibližně 5,5 KB. Aktuální limit pro datagramy je proto přibližně 10 KB. Tento limit bude zvýšen v budoucí verzi.

## Typy zpráv {#types}

Vyšší číslo priority znamená vyšší prioritu. Většina provozu jsou TunnelDataMessages (priorita 400), takže cokoli nad 400 je v podstatě vysoká priorita a cokoli pod tím je nízká priorita. Dále si také povšimněte, že mnoho zpráv je obecně směrováno přes průzkumné tunely, nikoli klientské tunely, a proto nemusí být ve stejné frontě, pokud se první skoky náhodou neshodují na stejném peeru.

Také ne všechny typy zpráv jsou odesílány nešifrovaně. Například při testování tunelu router zabalí DeliveryStatusMessage, která je zabalena v GarlicMessage, která je zase zabalena v DataMessage.

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
## Testování tunelu

Testování tunelů je vyžadováno od verze API 0.9.68 z února 2026, protože směrovače mají povoleno odmítat účast na tunelech, které po prvních dvou minutách neobdržely žádný provoz.

## Kompletní specifikace protokolu

Kompletní specifikaci protokolu najdete na stránce [specifikace I2NP](/docs/specs/i2np/). Viz také stránka [specifikace běžných datových struktur](/docs/specs/common-structures/).

## Budoucí práce

Není jasné, zda je současný systém priorit obecně účinný a zda by měly být priority jednotlivých zpráv dále upraveny. Toto je téma pro další výzkum, analýzu a testování.
