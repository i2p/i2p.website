---
title: "I2NP Genel Bakış"
description: "I2P Ağ Protokolü (I2NP) genel bakış - mesaj formatı, türleri, öncelikleri ve boyut sınırlamaları."
slug: "i2np-overview"
aliases:
  - "/tr/docs/protocol/i2np"
  - "/tr/docs/protocol/i2np/"
category: "Protokoller"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Genel Bakış

I2CP ve çeşitli I2P taşıma protokolleri arasında yer alan I2P Ağ Protokolü (I2NP), yönlendiriciler arasındaki mesajların yönlendirilmesi ve karıştırılmasından sorumludur ve aynı zamanda bir eş ile iletişim kurarken birden fazla ortak taşıma protokolü desteklendiğinde hangi taşıma protokollerinin kullanılacağının seçilmesini sağlar.

## I2NP Tanımı

I2NP (I2P Ağ Protokolü) mesajları, tek sıçramalı, yönlendirici-yönlendirici, noktadan noktaya mesajlar için kullanılabilir. Mesajlar, diğer mesajların içine şifrelenerek ve sarılarak, çoklu sıçramalarla son hedefe güvenli bir şekilde gönderilebilir. Öncelik yalnızca orijinde yerel olarak kullanılır, yani giden teslimat için kuyruğa alınırken.

Aşağıda listelenen öncelikler güncel olmayabilir ve değişikliğe tabidir. Öncelik kuyruğu uygulaması değişiklik gösterebilir.

## İleti Biçimi {#format}

Aşağıdaki tablo NTCP'de kullanılan geleneksel 16 baytlık başlığı belirtir. SSU ve NTCP2 taşıma katmanları, değiştirilmiş başlıkları kullanır.

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
Maksimum yük boyutu nominal olarak 64KB olsa da, bu boyut [tünel uygulaması sayfasında](/docs/specs/tunnel-implementation/) açıklandığı gibi I2NP mesajlarının birden fazla 1KB'lık tünel mesajına parçalanma yöntemi tarafından daha da sınırlanır.

Parça sayısı en fazla 64 olabilir ve mesaj tam olarak hizalanmamış olabilir, bu yüzden mesaj nominal olarak 63 parçaya sığmalıdır.

İlk parçanın maksimum boyutu 956 bayttır (TUNNEL teslimat modu varsayılırsa); takip eden parçanın maksimum boyutu 996 bayttır. Bu nedenle maksimum boyut yaklaşık olarak 956 + (62 * 996) = 62708 bayt veya 61,2 KB'dır.

Ayrıca, aktarımlar ek sınırlamalara sahip olabilir. NTCP sınırı 16KB - 6 = 16378 bayttır. SSU sınırı yaklaşık 32 KB'dır. NTCP2 sınırı yaklaşık 64KB - 20 = 65516 bayttır ve bu, bir tünelin destekleyebileceğinden daha yüksektir.

İstemcinin gördüğü veri birimleri için bu sınırların geçerli olmadığını unutmayın, çünkü yönlendirici bir sarımsak mesajında istemci mesajıyla birlikte bir yanıt leaseset'i ve/veya oturum etiketlerini birleştirebilir. Leaseset ve etiketler birlikte yaklaşık 5,5 KB ekleyebilir. Bu nedenle geçerli veri birimi sınırı yaklaşık 10 KB'dir. Bu sınır gelecekteki bir sürümde artırılacaktır.

## Mesaj Türleri {#types}

Daha yüksek numaralı öncelik, daha yüksek önceliktir. Trafik büyük ölçüde TunnelDataMessages'tir (öncelik 400), bu yüzden 400'ün üzerindekiler temelde yüksek öncelikli, altındakiler ise düşük önceliklidir. Ayrıca, mesajların çoğu genellikle istemci tünelleri değil, keşif tünelleri aracılığıyla yönlendirilir ve bu nedenle ilk zıplayışlar aynı eş üzerinde olmazsa aynı kuyrukta olmayabilirler.

Ayrıca tüm mesaj türleri şifrelenmeden gönderilmemektedir. Örneğin bir tünel test edilirken, yönlendirici DeliveryStatusMessage'ı GarlicMessage içinde, GarlicMessage ise DataMessage içinde sarmalar.

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
## Tünel Testi

API sürümü 0.9.68 2026-02'den itibaren tünel testi gereklidir çünkü ilk iki dakika sonra herhangi bir trafiğe sahip olmayan tünel katılımcılarının yönlendiriciler tarafından bırakılması izin verilir.

## Tam Protokol Özelliği

Tam protokol belirtimini görmek için [I2NP Spesifikasyon sayfasına](/docs/specs/i2np/) bakın. Ayrıca [Ortak Veri Yapısı Spesifikasyonu sayfasına](/docs/specs/common-structures/) bakın.

## Gelecek Çalışmalar

Mevcut öncelik şemasının genel olarak etkili olup olmadığı ve çeşitli mesajlar için önceliklerin daha fazla ayarlanıp ayarlanmayacağı henüz açık değil. Bu, daha ileri araştırma, analiz ve testler için bir konudur.
