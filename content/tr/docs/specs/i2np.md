---
title: "I2NP Spesifikasyonu"
description: "Router'dan router'a iletişim için I2P Network Protocol (I2NP) mesaj formatları, öncelikleri ve ortak yapıları."
slug: "i2np"
aliases:
  - "/tr/spec/i2np"
  - "/tr/spec/i2np/"
  - "/tr/i2np_spec"
  - "/tr/i2np_spec/"
category: "Protokoller"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Genel Bakış

I2P Network Protocol (I2NP), I2P aktarım protokollerinin üzerindeki katmandır. Bu bir router'dan router'a protokoldür. Network database sorgularında ve yanıtlarında, tunnel'lar oluşturmada ve şifrelenmiş router ile istemci veri mesajlarında kullanılır. I2NP mesajları başka bir router'a noktadan noktaya gönderilebilir veya o router'a tunnel'lar aracılığıyla anonim olarak gönderilebilir.

## Protokol Sürümleri {#versions}

Tüm router'lar I2NP protokol sürümlerini RouterInfo özelliklerindeki "router.version" alanında yayınlamalıdır. Bu sürüm alanı API sürümüdür, çeşitli I2NP protokol özelliklerine yönelik destek seviyesini gösterir ve mutlaka gerçek router sürümü olmak zorunda değildir.

Alternatif (Java olmayan) router'lar gerçek router uygulaması hakkında herhangi bir sürüm bilgisi yayınlamak isterse, bunu başka bir özellikte yapmaları gerekir. Aşağıda listelenenler dışındaki sürümlere de izin verilir. Destek sayısal karşılaştırma yoluyla belirlenecektir; örneğin, 0.9.13 sürümü 0.9.12 özelliklerini desteklediği anlamına gelir. "coreVersion" özelliğinin artık router bilgilerinde yayınlanmadığını ve I2NP protokol sürümünün belirlenmesi için hiçbir zaman kullanılmadığını unutmayın.

I2NP protokol sürümlerinin temel özeti aşağıdaki gibidir. Ayrıntılar için aşağıya bakınız.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Ayrıca taşıma ile ilgili özellikler ve uyumluluk sorunları da bulunmaktadır; ayrıntılar için NTCP ve SSU taşıma belgelerine bakınız.

## Ortak Yapılar {#structures}

Aşağıdaki yapılar birden fazla I2NP mesajının öğeleridir. Bunlar tam mesajlar değildir.

### I2NP Mesaj Başlığı {#struct-I2NPMessageHeader}

#### Açıklama

Tüm I2NP mesajlarına ortak başlık, kontrol toplamı, son kullanma tarihi vb. gibi önemli bilgileri içerir.

#### İçindekiler

Bağlama göre kullanılan üç ayrı format vardır; bir standart format ve iki kısa format.

Standart 16 bayt formatı, bu mesajın türünü belirten 1 bayt [Integer](/docs/specs/common-structures/#integer), ardından mesaj kimliğini belirten 4 bayt [Integer](/docs/specs/common-structures/#integer) içerir. Bundan sonra bir son kullanma [Date](/docs/specs/common-structures/#date), ardından mesaj yükünün uzunluğunu belirten 2 bayt [Integer](/docs/specs/common-structures/#integer), ardından ilk bayta kesilmiş bir [Hash](/docs/specs/common-structures/#hash) gelir. Bundan sonra gerçek mesaj verisi takip eder.

Kısa formatlar, 8 bayt milisaniye cinsinden süre sonu yerine 4 bayt saniye cinsinden süre sonu kullanır. Kısa formatlar bir sağlama toplamı veya boyut içermez, bunlar bağlama göre kapsülleme tarafından sağlanır.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Notlar

- [SSU](/docs/transports/ssu/) üzerinden iletildiğinde, 16-baytlık standart başlık kullanılmaz. Yalnızca 1-baytlık tür ve saniye cinsinden 4-baytlık son kullanma tarihi dahil edilir. Mesaj kimliği ve boyut, SSU veri paketi formatına dahil edilmiştir. Hatalar şifre çözme sırasında yakalandığından sağlama toplamı gerekli değildir.

- [NTCP2](/docs/specs/ntcp2/) veya [SSU2](/docs/specs/ssu2/) üzerinden iletildiğinde, 16 baytlık standart başlık kullanılmaz. Sadece 1 baytlık tip, 4 baytlık mesaj kimliği ve 4 baytlık saniye cinsinden sona erme süresi dahil edilir. Boyut, NTCP2 ve SSU2 veri paketi formatlarına dahil edilir. Hatalar şifre çözme sırasında yakalandığından sağlama toplamı gerekli değildir.

- Standart başlık, diğer mesajlar ve yapılar içinde yer alan I2NP mesajları için de gereklidir (Data, TunnelData, TunnelGateway ve GarlicClove). 0.8.12 sürümü itibariyle, ek yükü azaltmak için protokol yığınının bazı noktalarında checksum doğrulaması devre dışı bırakılmıştır. Ancak, eski sürümlerle uyumluluk için checksum oluşturma hala gereklidir. Protokol yığınında uzak router'ın sürümünün bilindiği ve checksum oluşturmanın devre dışı bırakılabileceği noktaların belirlenmesi gelecekteki araştırmalar için bir konudur.

- Kısa süre sonu imzasız olup 7 Şubat 2106'da döngüye girecektir. Bu tarihten itibaren doğru zamanı elde etmek için bir offset eklenmesi gerekir.

- Uygulamalar gelecekte çok uzak süre sonları olan mesajları reddedebilir. Önerilen maksimum süre sonu gelecekte 60 saniyedir.

### BuildRequestRecord {#struct-BuildRequestRecord}

KULLANIM DIŞI, mevcut ağda yalnızca bir tunnel ElGamal router içerdiğinde kullanılır. Bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Açıklama

Tunnel'da bir hop'un oluşturulmasını talep etmek için birden fazla kaydın bulunduğu bir setteki Tek Kayıt. Daha fazla ayrıntı için [tunnel genel bakış](/docs/specs/tunnel-implementation/) ve [ElGamal tunnel oluşturma spesifikasyonu](/docs/specs/tunnel-creation/) sayfalarına bakın.

ECIES-X25519 BuildRequestRecords için, [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) bölümüne bakın.

#### İçindekiler (ElGamal)

Mesajların alınacağı [TunnelId](/docs/specs/common-structures/#tunnelid), ardından [RouterIdentity](/docs/specs/common-structures/#routeridentity)'mizin [Hash](/docs/specs/common-structures/#hash)'i gelir. Bundan sonra bir sonraki router'ın [RouterIdentity](/docs/specs/common-structures/#routeridentity)'sinin [TunnelId](/docs/specs/common-structures/#tunnelid)'si ve [Hash](/docs/specs/common-structures/#hash)'i takip eder.

ElGamal ve AES şifrelenmiş:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal şifreli:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Düz Metin:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Notlar

- 512 baytlık şifrelenmiş kayıtta, ElGamal verisi 514 baytlık ElGamal şifrelenmiş bloğun 1-256 ve 258-513 baytlarını içerir [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Bloktan gelen iki dolgu baytı (0 ve 257 konumlarındaki sıfır baytları) kaldırılır.

- Alan içeriklerinin ayrıntıları için [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

### BuildResponseRecord {#struct-BuildResponseRecord}

KULLANIM DIŞI, mevcut ağda yalnızca bir tunnel ElGamal router içerdiğinde kullanılır. Bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Açıklama

Bir yapı isteğine yanıtlar içeren birden fazla kaydın bulunduğu bir setteki tek kayıt. Daha fazla ayrıntı için [tunnel genel bakışına](/docs/specs/tunnel-implementation/) ve [ElGamal tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

ECIES-X25519 BuildResponseRecords için, [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) bölümüne bakınız.

#### İçindekiler (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Notlar

- Rastgele veri alanı gelecekte, talep edene tıkanıklık veya eş bağlantı bilgilerini geri döndürmek için kullanılabilir.

- Reply alanı hakkında ayrıntılar için [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Yalnızca ECIES-X25519 router'lar için, API sürüm 0.9.51 itibariyle. Şifrelendiğinde 218 bayt. Bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Yalnızca ECIES-X25519 router'ları için, API sürüm 0.9.51 itibariyle. Şifrelendiğinde 218 bayt. Bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Uyarı: Bu, ElGamal-şifrelemeli garlic mesajları içindeki garlic clove'lar için kullanılan formattır [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). ECIES-AEAD-X25519-Ratchet garlic mesajları ve garlic clove'ları için format önemli ölçüde farklıdır; spesifikasyon için [ECIES](/docs/specs/ecies/) bölümüne bakın.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Notlar

- Clove'lar asla parçalanmaz. Garlic Clove içinde kullanıldığında, Delivery Instructions flag byte'ının ilk biti şifrelemeyi belirtir. Bu bit 0 ise, clove şifrelenmemiştir. 1 ise, clove şifrelenmiştir ve flag byte'ından hemen sonra 32 byte'lık bir Session Key gelir. Clove şifrelemesi tam olarak uygulanmamıştır.

- Ayrıca [garlic routing spesifikasyonuna](/docs/overview/garlic-routing/) bakın.

- Maksimum uzunluk, tüm clove'ların toplam uzunluğu ve GarlicMessage'ın maksimum uzunluğunun bir fonksiyonudur.

- Gelecekte, sertifika muhtemelen routing için "ödeme" yapmak amacıyla bir HashCash için kullanılabilir.

- Mesaj herhangi bir I2NP mesajı olabilir (GarlicMessage dahil, ancak bu pratikte kullanılmaz). Pratikte kullanılan mesajlar DataMessage, DeliveryStatusMessage ve DatabaseStoreMessage'dır.

- Clove ID genellikle gönderimde rastgele bir sayıya ayarlanır ve alımda duplikalar için kontrol edilir (üst seviye Message ID'leri ile aynı mesaj ID alanı)

### Garlic Clove Delivery Instructions {#struct-GarlicCloveDeliveryInstructions}

Bu format hem ElGamal-şifrelemeli [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) hem de ECIES-AEAD-X25519-Ratchet şifrelemeli [ECIES](/docs/specs/ecies/) garlic clove'ları için kullanılır.

Bu şartname yalnızca Garlic Clove'lar içindeki Delivery Instructions (Teslimat Talimatları) için geçerlidir. "Delivery Instructions"ların Tunnel Message'lar içinde de kullanıldığını ve bu durumda formatın önemli ölçüde farklı olduğunu unutmayın. Ayrıntılar için [Tunnel Message belgelerine](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) bakın. Tunnel Message Delivery Instructions için aşağıdaki şartnameyi KULLANMAYIN!

Session key ve delay kullanılmaz ve hiçbir zaman mevcut değildir, bu nedenle üç olası uzunluk 1 (LOCAL), 33 (ROUTER ve DESTINATION) ve 37 (TUNNEL) bayttır.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Mesajlar

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Açıklama

Talep edilmemiş bir veritabanı depolama işlemi veya başarılı bir [DatabaseLookup](#msg-DatabaseLookup) Mesajına yanıt

#### İçindekiler

Sıkıştırılmamış bir LeaseSet, LeaseSet2, MetaLeaseSet veya EncryptedLeaseset, ya da sıkıştırılmış bir RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Notlar

- Güvenlik için, mesaj bir tunnel üzerinden alındığında yanıt alanları göz ardı edilir.

- Anahtar, RouterIdentity veya Destination'ın "gerçek" hash'idir, routing anahtarı DEĞİLDİR.

- Tip 3, 5 ve 7, 0.9.38 sürümü itibariyle geçerlidir. Daha fazla bilgi için öneri 123'e bakın. Bu tipler yalnızca 0.9.38 veya daha yüksek sürümlü routerlara gönderilmelidir.

- Bağlantıları azaltmak için bir optimizasyon olarak, tür bir LeaseSet ise, yanıt token'ı dahil edilirse, yanıt tunnel ID'si sıfır değilse ve yanıt gateway/tunnelID çifti LeaseSet içinde bir lease olarak bulunursa, alıcı yanıtı LeaseSet içindeki herhangi bir başka lease'e yönlendirebilir.

- Router işletim sistemini ve uygulamasını gizlemek için, değişiklik zamanını 0'a ve işletim sistemi baytını 0xFF'e ayarlayarak Java router uygulamasının gzip kullanımını taklit edin, ve XFL'yi 0x02'ye (maksimum sıkıştırma, en yavaş algoritma) ayarlayın. RFC 1952'ye bakın. Sıkıştırılmış router bilgisinin ilk 10 baytı şu şekilde olacaktır (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Açıklama

Ağ veritabanında bir öğeyi arama isteği. Yanıt ya bir [DatabaseStore](#msg-DatabaseStore) ya da bir [DatabaseSearchReply](#msg-DatabaseSearchReply)'dir.

#### İçerik

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Yanıt Şifreleme

NOT: ElGamal router'lar API 0.9.58 itibariyle kullanımdan kaldırılmıştır. Sorgulanması önerilen minimum floodfill sürümü artık 0.9.58 olduğundan, uygulamaların ElGamal floodfill router'lar için şifreleme uygulaması gerekmemektedir. ElGamal hedefleri hala desteklenmektedir.

Flag bit 4, yanıt şifreleme modunu belirlemek için bit 1 ile birlikte kullanılır. Flag bit 4 sadece 0.9.46 veya daha yüksek sürümlü router'lara gönderirken ayarlanmalıdır. Ayrıntılar için öneri 154 ve 156'ya bakınız.

Aşağıdaki tabloda, "DH n/a" yanıtın şifrelenmediği anlamına gelir. "DH no" yanıt anahtarlarının istekte dahil edildiği anlamına gelir. "DH yes" yanıt anahtarlarının DH işleminden türetildiği anlamına gelir.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Şifreleme Yok

reply_key, tags ve reply_tags mevcut değil.

#### ElG'den ElG'ye

0.9.7 sürümünden itibaren desteklendi. 0.9.58 sürümünden itibaren kullanımdan kaldırıldı. ElG hedefi bir ElG router'ına arama gönderir.

İstek sahibi anahtar üretimi:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Mesaj formatı:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES'den ElG'ye

0.9.46 sürümünden itibaren desteklenir. 0.9.58 sürümünden itibaren kullanımdan kaldırılmıştır. ECIES destination bir ElG router'a arama gönderir. reply_key ve reply_tags alanları ECIES-şifreli yanıt için yeniden tanımlanır.

İstek sahibi anahtar oluşturma:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Mesaj formatı: reply_key ve reply_tags alanlarını aşağıdaki gibi yeniden tanımlayın:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
Yanıt, [ECIES](/docs/specs/ecies/) içinde tanımlandığı gibi bir ECIES Mevcut Oturum mesajıdır.

#### Yanıt formatı

Bu mevcut oturum mesajıdır, [ECIES](/docs/specs/ecies/) ile aynıdır, referans için aşağıda kopyalanmıştır.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
AEAD parametreleri:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES'den ECIES'e (0.9.49)

ECIES hedefi veya router'ı, bir ECIES router'a arama gönderir. 0.9.49 sürümünden itibaren desteklenmektedir.

ECIES router'lar 0.9.48 sürümünde tanıtıldı, bkz. [Öneri 156](/proposals/156/). ECIES hedefleri ve router'lar yukarıdaki "ECIES'den ElG'ye" bölümünde olduğu gibi aynı formatı kullanabilir, istekte yanıt anahtarları dahil edilir. Arama mesajı şifreleme [ECIES-ROUTERS](/docs/specs/ecies-routers/) belgesinde belirtilmiştir. İstek yapan anonim kalır.

#### ECIES'den ECIES'e (gelecek)

Bu seçenek henüz tam olarak tanımlanmamıştır. [Öneri 156](/proposals/156/) bölümüne bakınız.

#### Notlar

- 0.9.16 öncesinde, anahtar bir RouterInfo veya LeaseSet için olabilirdi, çünkü bunlar aynı anahtar alanındaydı ve yalnızca belirli bir veri türü talep etmek için herhangi bir bayrak yoktu.

- 0.9.7 sürümü itibariyle şifreleme bayrağı, yanıt anahtarı ve yanıt etiketleri.

- Şifrelenmiş yanıtlar yalnızca yanıt bir tunnel üzerinden geldiğinde yararlıdır.

- Alternatif DHT arama stratejileri (örneğin, özyinelemeli aramalar) uygulanırsa, dahil edilen etiket sayısı birden fazla olabilir.

- Arama anahtarı ve hariç tutma anahtarları "gerçek" hash'lerdir, yönlendirme anahtarları DEĞİL.

- Tip 3, 5 ve 7, sürüm 0.9.38 itibariyle döndürülebilir. Daha fazla bilgi için öneri 123'e bakın.

- Keşifsel arama notları: Bir keşifsel arama, anahtara yakın olan floodfill olmayan hash'lerin bir listesini döndürecek şekilde tanımlanmıştır. Ancak, uygulama varyantları için DatabaseSearchReply'nin önemli notlarına bakınız. Ayrıca, bu spesifikasyon alıcının bir RI için arama anahtarını araması ve mevcut ise DSRM yerine bir DatabaseStore döndürmesi gerekip gerekmediğini hiçbir zaman açık hale getirmemiştir. Java araştırmayı yapar; i2pd yapmaz. Bu nedenle, daha önce alınmış hash'ler için keşifsel arama kullanılması önerilmez.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Açıklama

Başarısız bir [DatabaseLookup](#msg-DatabaseLookup) Mesajına verilen yanıt

#### İçindekiler

İstenen anahtara en yakın router hash'lerinin listesi

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Notlar

- 'From' hash'i doğrulanmamıştır ve güvenilmez.

- Döndürülen peer hash'leri, sorgulanmakta olan router'dan anahtara mutlaka daha yakın değildir. Normal aramalar için yanıtlarda, bu durum yeni floodfill'lerin keşfedilmesini ve sağlamlık için "geriye doğru" arama yapılmasını (anahtardan daha uzak) kolaylaştırır.

- Keşif araması için anahtar genellikle rastgele oluşturulur. Bu nedenle, yanıtın floodfill olmayan peer_hash'leri, tüm yerel ağ veritabanının verimsiz bir sıralamasını veya aramasını önlemek için anahtara yakın olan ancak tüm yerel ağ veritabanında en yakın olması gerekmeyen eşler sağlamak gibi optimize edilmiş bir algoritma kullanılarak seçilebilir. Önbellekleme gibi diğer stratejiler de uygun olabilir. Bu implementasyona bağlıdır.

- Döndürülen tipik hash sayısı: 3

- Döndürülecek önerilen maksimum hash sayısı: 16

- Arama anahtarı, eş hash'leri ve kaynak hash'i "gerçek" hash'lerdir, yönlendirme anahtarları DEĞİLDİR.

### DeliveryStatus {#msg-DeliveryStatus}

#### Açıklama

Basit bir mesaj onayı. Genellikle mesaj gönderen tarafından oluşturulur ve mesajın kendisiyle birlikte bir Garlic Message içinde sarılarak hedef tarafından geri gönderilir.

Bu mesaj aynı zamanda tünel testi için de kullanılır; gönderen, mesajı giden bir tünele, ardından kendisine dönen gelen bir tünele gönderir. Bu uygulamada da mesaj genellikle Garlic şifrelemesiyle sarılmıştır. Tünel testi, API sürüm 0.9.68 2026-02'den itibaren gereklidir çünkü yönlendiriciler ilk iki dakika içinde herhangi bir trafiği almayan tünel katılımcılarını bırakmaya yetkilidir.

#### İçindekiler

Teslim edilen mesajın kimliği ve oluşturulma veya varış zamanı.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Notlar

- Zaman damgasının her zaman yaratıcı tarafından mevcut zamana ayarlandığı görülüyor. Ancak kodda bunun birkaç kullanımı var ve gelecekte daha fazlası eklenebilir.

- Bu mesaj aynı zamanda SSU [SSU-ED](/docs/transports/ssu/#establishDirect) içinde oturum kuruldu onayı olarak da kullanılır. Bu durumda, mesaj kimliği rastgele bir sayıya ayarlanır ve "varış zamanı" mevcut ağ çapındaki kimliğe ayarlanır, bu da 2'dir (yani 0x0000000000000002).

### Garlic {#msg-Garlic}

Uyarı: Bu, ElGamal ile şifrelenmiş sarımsak mesajları için kullanılan formattır [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). ECIES-AEAD-X25519-Ratchet sarımsak mesajları ve sarımsak kabuklarının formatı önemli ölçüde farklıdır; spesifikasyon için [ECIES](/docs/specs/ecies/) sayfasına bakın.

#### Açıklama

Birden fazla şifrelenmiş I2NP Mesajını sarmalamak için kullanılır

#### İçindekiler

Şifresi çözüldüğünde, [Sarımsak Dişleri](#struct-GarlicClove) serisi ve ek veriler, aynı zamanda Clove Set (Sarımsak Kümesi) olarak da bilinir.

Şifrelenmiş:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Şifresi çözülmüş veri, aynı zamanda Clove Set (Çivi Seti) olarak da bilinir:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Notlar

- Şifrelenmediğinde, veri bir veya daha fazla [Garlic Clove](#struct-GarlicClove) içerir.

- AES şifrelenmiş blok minimum 128 byte'a doldurulur; 32-byte Session Tag ile şifrelenmiş mesajın minimum boyutu 160 byte'tır; 4 uzunluk byte'ı ile Garlic Message'ın minimum boyutu 164 byte'tır.

- Gerçek maksimum uzunluk 64 KB'dan azdır; [I2NP](/docs/protocol/i2np/) bölümüne bakınız.

- Ayrıca [ElGamal/AES spesifikasyonuna](/docs/specs/elgamal-aes/) bakın.

- Ayrıca [garlic routing özelliklerini](/docs/overview/garlic-routing/) de inceleyin.

- AES şifrelenmiş bloğun 128 bayt minimum boyutu şu anda yapılandırılabilir değildir, ancak bir GarlicMessage içindeki bir GarlicClove içindeki bir DataMessage'ın overhead ile birlikte minimum boyutu zaten 128 bayttır. Minimum boyutu artırmak için yapılandırılabilir bir seçenek gelecekte eklenebilir.

- Mesaj ID'si genellikle iletim sırasında rastgele bir sayıya ayarlanır ve alma sırasında göz ardı ediliyor gibi görünür.

- Gelecekte, sertifika muhtemelen routing için "ödeme" yapmak üzere bir HashCash için kullanılabilir.

### TunnelData {#msg-TunnelData}

#### Açıklama

Bir tünelin geçidi veya katılanından bir sonraki katılan veya uç noktaya gönderilen mesaj. Veri sabit uzunlukta olup, parçalanmış, toplu hâle getirilmiş, doldurulmuş ve şifrelenmiş I2NP mesajlarını içerir.

#### İçindekiler

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Notlar

- Bu mesaj için I2NP mesaj kimliği her atlamada yeni bir rastgele sayıya ayarlanır.

- Ayrıca [Tunnel Mesaj Spesifikasyonu](/docs/legacy/tunnel-message/) bölümüne bakın

### TunnelGateway {#msg-TunnelGateway}

#### Açıklama

Bir tünelin giriş geçidi noktasına gönderilmek üzere başka bir I2NP mesajını sarmalar.

#### İçindekiler

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notlar

- Yük, standart 16-baytlık başlığa sahip bir I2NP mesajıdır.

### Veri {#msg-Data}

#### Açıklama

Sarımsak Mesajları ve Sarımsak Dilimleri tarafından keyfi verileri sarmalamak için kullanılır.

#### İçindekiler

Bir uzunluk Tamsayısı, ardından opak veri.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notlar

- Bu mesaj hiçbir yönlendirme bilgisi içermez ve asla "açılmamış" olarak gönderilmez. Sadece `Garlic` mesajları içinde kullanılır.

### TunnelBuild {#msg-TunnelBuild}

KULLANIMI BIRAKILDI, [VariableTunnelBuild](#msg-VariableTunnelBuild) kullanın

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Notlar

- 0.9.48 sürümünden itibaren, ECIES-X25519 BuildRequestRecords da içerebilir, bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Ayrıca [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

- Bu mesaj için I2NP mesaj ID'si, tunnel oluşturma spesifikasyonuna göre ayarlanmalıdır.

- Bu mesaj günümüz ağında nadiren görülse de, `VariableTunnelBuild` mesajı ile değiştirilmiş olmasına rağmen, çok uzun tunnel'lar için hala kullanılabilir ve kullanımdan kaldırılmamıştır. Router'lar uygulamalıdır.

### TunnelBuildReply {#msg-TunnelBuildReply}

KULLANIMI BIRAKILDI, [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply) kullanın

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Notlar

- 0.9.48 sürümünden itibaren, ECIES-X25519 BuildResponseRecords de içerebilir, bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Ayrıca [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) da bakın.

- Bu mesaj için I2NP mesaj kimliği, tunnel oluşturma spesifikasyonuna göre ayarlanmalıdır.

- Bu mesaj günümüzün ağında nadiren görülse de `VariableTunnelBuildReply` mesajı tarafından değiştirilmiş olmasına rağmen, çok uzun tunneller için hala kullanılabilir ve kullanımdan kaldırılmamıştır. Routerlar uygulamalıdır.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Notlar

- 0.9.48 sürümünden itibaren ECIES-X25519 BuildRequestRecords de içerebilir, bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Bu mesaj router sürümü 0.7.12'de tanıtıldı ve bu sürümden önceki tunnel katılımcılarına gönderilmeyebilir.

- Ayrıca [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

- Bu mesaj için I2NP mesaj kimliği, tunnel oluşturma spesifikasyonuna göre ayarlanmalıdır.

- Günümüz ağında tipik kayıt sayısı 4'tür ve toplam boyut 2113'tür.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Notlar

- 0.9.48 sürümünden itibaren, ECIES-X25519 BuildResponseRecords da içerebilir, bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Bu mesaj router sürüm 0.7.12'de tanıtıldı ve bu sürümden önceki tunnel katılımcılarına gönderilmeyebilir.

- Ayrıca [tunnel oluşturma spesifikasyonuna](/docs/specs/tunnel-creation/) bakın.

- Bu mesaj için I2NP mesaj kimliği, tunnel oluşturma spesifikasyonuna göre ayarlanmalıdır.

- Günümüz ağında tipik kayıt sayısı 4'tür ve toplam boyut 2113'tür.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Açıklama

Sadece ECIES-X25519 yönlendiriciler için, API sürümü 0.9.51 itibarıyla.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Notlar

- 0.9.51 itibariyle. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/) sayfasına bakın.

- Bu mesaj router sürüm 0.9.51'de tanıtıldı ve bu sürümden önceki tunnel katılımcılarına gönderilmeyebilir.

- Günümüz ağındaki tipik kayıt sayısı 4'tür ve toplam boyutu 873'tür.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Açıklama

Yeni bir tünelin giden ucu tarafından orijinatöre gönderildi. API sürümü 0.9.51'den itibaren yalnızca ECIES-X25519 yönlendiricileri için.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Notlar

- 0.9.51 itibariyle. Bkz. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Günümüzün ağında tipik kayıt sayısı 4'tür ve toplam boyut 873'tür.

## Referanslar

- **[CRYPTO-ELG]** [Kriptografi - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Ortak Yapılar - Tarih](/docs/specs/common-structures/#date)
- **[ECIES]** [ECIES Spesifikasyonu](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [ECIES Router'ları Spesifikasyonu](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Yönlendirme](/docs/overview/garlic-routing/)
- **[Hash]** [Ortak Yapılar - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP Protokolü](/docs/protocol/i2np/)
- **[Integer]** [Ortak Yapılar - Tamsayı](/docs/specs/common-structures/#integer)
- **[NTCP2]** [NTCP2 Spesifikasyonu](/docs/specs/ntcp2/)
- **[Prop156]** [Öneri 156](/proposals/156/)
- **[Prop157]** [Öneri 157](/proposals/157/)
- **[RouterIdentity]** [Ortak Yapılar - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU Taşıma](/docs/transports/ssu/)
- **[SSU-ED]** [SSU Taşıma - Doğrudan Bağlantı Kurma](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [SSU2 Spesifikasyonu](/docs/specs/ssu2/)
- **[TMDI]** [Tunnel Mesaj Teslimat Talimatları](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Tunnel Oluşturma Spesifikasyonu](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [ECIES Tunnel Oluşturma](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Tunnel Uygulaması](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Tunnel Mesaj Spesifikasyonu](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Ortak Yapılar - TunnelId](/docs/specs/common-structures/#tunnelid)
