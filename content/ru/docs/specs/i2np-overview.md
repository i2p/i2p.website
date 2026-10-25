---
title: "Обзор I2NP"
description: "Обзор сетевого протокола I2P (I2NP) — формат сообщений, типы, приоритеты и ограничения по размеру."
slug: "i2np-overview"
aliases:
  - "/ru/docs/protocol/i2np"
  - "/ru/docs/protocol/i2np/"
category: "Протоколы"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Обзор

Протокол сети I2P (I2NP), расположенный между I2CP и различными транспортными протоколами I2P, управляет маршрутизацией и перемешиванием сообщений между маршрутизаторами, а также выбором транспортов для использования при взаимодействии с узлом, с которым поддерживается несколько общих транспортов.

## Определение I2NP

Сообщения I2NP (I2P Network Protocol) могут использоваться для одношаговых, маршрутизатор-к-маршрутизатору, точечных сообщений. Шифруя и оборачивая сообщения в другие сообщения, их можно безопасно отправлять через несколько узлов до конечного пункта назначения. Приоритет используется только локально на исходном узле, т.е. при постановке в очередь для исходящей доставки.

Перечисленные ниже приоритеты могут быть устаревшими и подлежат изменению. Реализация очереди приоритетов может различаться.

## Формат сообщения {#format}

В следующей таблице указан традиционный 16-байтовый заголовок, используемый в NTCP. Транспорты SSU и NTCP2 используют изменённые заголовки.

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
Хотя номинальный максимальный размер полезной нагрузки составляет 64 КБ, фактический размер дополнительно ограничен методом фрагментации сообщений I2NP на несколько туннельных сообщений по 1 КБ, как описано на [странице реализации туннелей](/docs/specs/tunnel-implementation/).

Максимальное количество фрагментов — 64, и сообщение может быть не perfectly выровнено, поэтому сообщение должно умещаться в 63 фрагмента.

Максимальный размер начального фрагмента составляет 956 байт (при условии режима доставки TUNNEL); максимальный размер последующего фрагмента — 996 байт. Следовательно, максимальный размер составляет приблизительно 956 + (62 × 996) = 62708 байт или 61,2 КБ.

Кроме того, транспорты могут иметь дополнительные ограничения. Ограничение NTCP составляет 16 КБ - 6 = 16378 байт. Ограничение SSU составляет приблизительно 32 КБ. Ограничение NTCP2 составляет приблизительно 64 КБ - 20 = 65516 байт, что выше, чем может поддерживать туннель.

Обратите внимание, что это не пределы для датаграмм, которые видит клиент, поскольку маршрутизатор может объединить набор аренд (leaseset) и/или теги сеанса вместе с сообщением клиента в одном чесночном (garlic) сообщении. Набор аренд и теги вместе могут добавить около 5,5 КБ. Поэтому текущий предел датаграммы составляет около 10 КБ. Этот предел будет увеличен в одной из будущих версий.

## Типы сообщений {#types}

Чем выше номер приоритета, тем выше приоритет. Большая часть трафика — это TunnelDataMessages (приоритет 400), поэтому всё, что выше 400, по сути является высоким приоритетом, а всё, что ниже, — низким. Также обратите внимание, что многие сообщения обычно передаются через исследовательские туннели, а не клиентские, и поэтому могут находиться не в той же очереди, если первые прыжки случайно не приходятся на одного и того же пира.

Кроме того, не все типы сообщений отправляются без шифрования. Например, при тестировании туннеля маршрутизатор оборачивает сообщение DeliveryStatusMessage, которое, в свою очередь, оборачивается в GarlicMessage, а затем в DataMessage.

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
## Тестирование туннеля

Начиная с версии API 0.9.68 от 2026-02, требуется тестирование туннелей, поскольку маршрутизаторам разрешено отключать участие в туннелях, которые не получили трафик в течение первых двух минут.

## Полная спецификация протокола

Полные спецификации протокола доступны на странице [спецификации I2NP](/docs/specs/i2np/). Также см. страницу [спецификации общих структур данных](/docs/specs/common-structures/).

## Будущая работа

Неясно, насколько эффективна текущая схема приоритетов в целом и следует ли дополнительно корректировать приоритеты различных сообщений. Это тема для дальнейших исследований, анализа и тестирования.
