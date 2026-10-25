---
title: "SSU (Güvenli Yarı-Güvenilir UDP)"
description: "Orijinal UDP taşıma protokolü spesifikasyonu (kullanımdan kaldırıldı, SSU2 ile değiştirildi)"
slug: "ssu"
aliases:
  - "/tr/docs/transport/ssu"
  - "/tr/docs/transport/ssu/"
  - "/tr/docs/transports/ssu"
  - "/tr/docs/transports/ssu/"
  - "/tr/docs/specs/ssu-spec"
  - "/tr/docs/specs/ssu-spec/"
category: "Taşımalar"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Genel Bakış

KULLANIM DIŞI - SSU, SSU2 ile değiştirildi. SSU desteği i2pd'den 2.44.0 sürümünde (API 0.9.56) 2022-11'de kaldırıldı. SSU desteği Java I2P'den 2.4.0 sürümünde (API 0.9.61) 2023-12'de kaldırıldı.

Daha fazla bilgi için [SSU genel bakış](/docs/transport/ssu/) sayfasına bakın.

## DH Anahtar Değişimi {#dh}

İlk 2048-bit DH anahtar değişimi [SSU Keys sayfasında](/docs/transport/ssu/#keys) açıklanmıştır. Bu değişim, I2P'nin [ElGamal şifrelemesi](/docs/specs/cryptography/#elgamal) için kullanılan aynı paylaşılan asal sayıyı kullanır.

## Mesaj Başlığı {#header}

Tüm UDP datagramları 16 baytlık MAC (Message Authentication Code - Mesaj Kimlik Doğrulama Kodu) ve 16 baytlık IV (Initialization Vector - Başlatma Vektörü) ile başlar, ardından uygun anahtarla şifrelenmiş değişken boyutlu yük gelir. Kullanılan MAC, 16 bayta kısaltılmış HMAC-MD5'tir, anahtar ise tam 32 baytlık AES256 anahtarıdır. MAC'in spesifik yapısı şundan gelen ilk 16 bayttır:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
burada '+' ekleme ve '^' özel-veya anlamına gelir.

IV her paket için rastgele oluşturulur. encryptedPayload, bayrak baytı ile başlayan mesajın şifrelenmiş versiyonudur (encrypt-then-MAC). MAC'te kullanılan payloadLength, 2 baytlık işaretsiz tamsayıdır, big endian. protocolVersion 0 olduğu için exclusive-or işlemi etkisizdir (no-op). macKey ya introduction key'dir ya da değiştirilen DH anahtarından oluşturulur (aşağıdaki ayrıntılara bakın), her mesaj için aşağıda belirtildiği gibi.

**UYARI** - burada kullanılan HMAC-MD5-128 standart dışıdır, daha fazla bilgi için [HMAC ayrıntıları](/docs/specs/cryptography/#udp) bölümüne bakın.

Payload'un kendisi (yani, bayrak byte'ı ile başlayan mesaj) IV ve sessionKey ile AES256/CBC şifrelenir ve tekrar saldırı önleme (replay prevention) işlemi aşağıda açıklandığı gibi mesajın gövdesinde ele alınır.

protocolVersion, big endian formatında 2 baytlık işaretsiz bir tamsayıdır ve şu anda 0 olarak ayarlanmıştır. Farklı bir protokol sürümü kullanan eşler bu eşle iletişim kuramazken, bu bayrağı kullanmayan önceki sürümler iletişim kurabilir.

((netid - 2) << 8) değerinin exclusive OR'u, ağlar arası bağlantıları hızlı bir şekilde tanımlamak için kullanılır. netid, büyük endian formatında 2 baytlık işaretsiz bir tamsayıdır ve şu anda 2 olarak ayarlanmıştır. 0.9.42 sürümü itibariyle. Daha fazla bilgi için proposal 147'ye bakın. Mevcut network ID 2 olduğu için, bu mevcut ağ için hiçbir işlem yapmaz ve geriye dönük uyumludur. Test ağlarından gelen herhangi bir bağlantı farklı bir ID'ye sahip olmalıdır ve HMAC'te başarısız olacaktır.

### HMAC Spesifikasyonu

- İç dolgu: 0x36...
- Dış dolgu: 0x5C...
- Anahtar: 32 bayt
- Hash özet fonksiyonu: MD5, 16 bayt
- Blok boyutu: 64 bayt
- MAC boyutu: 16 bayt
- Örnek C implementasyonları:
  - [i2pd](https://github.com/PurpleI2P/i2pd) içinde hmac.h
  - [i2pcpp](http://git.repo.i2p/w/i2pcpp.git) içinde I2PHMAC.cpp
- Örnek Java implementasyonu:
  - [I2P](https://github.com/i2p/i2p.i2p) içinde I2PHMac.java

### Oturum Anahtarı Detayları

32-byte'lık oturum anahtarı şu şekilde oluşturulur:

1. Değiş tokuş edilen DH anahtarını, pozitif minimal uzunlukta
   BigInteger bayt dizisi (two's complement big-endian) olarak al
2. En önemli bit 1 ise (yani array[0] & 0x80 != 0),
   Java'nın BigInteger.toByteArray() gösterimi gibi
   başına bir 0x00 baytı ekle
3. Bayt dizisi 32 bayt veya daha fazla ise, ilk (en önemli) 32 baytı kullan
4. Bayt dizisi 32 baytan az ise, 32 bayta genişletmek için
   0x00 baytları ekle. *Çok düşük olasılık - Aşağıdaki nota bakın.*

### MAC Anahtar Detayları

32-baytlık MAC anahtarı aşağıdaki gibi oluşturulur:

1. Yukarıdaki Session Key Details'teki adım 2'den, gerekirse önüne 0x00 byte'ı eklenmiş olan değiş tokuş edilmiş DH key byte dizisini alın.
2. Eğer o byte dizisi 64 byte'tan büyük veya eşitse, MAC key o byte dizisinin 33-64 byte'larıdır.
3. Eğer o byte dizisi 64 byte'tan küçükse, MAC key o byte dizisinin SHA-256 Hash'idir. *0.9.8 sürümü itibariyle. Aşağıdaki nota bakınız.*

#### Önemli not

0.9.8 sürümünden önceki kod bozuktu ve 32 ile 63 bayt arasındaki DH anahtar bayt dizilerini doğru şekilde işlemiyordu (yukarıdaki 3. ve 4. adımlar) ve bağlantı başarısız oluyordu. Bu durumlar hiçbir zaman çalışmadığından, 0.9.8 sürümü için yukarıda açıklandığı şekilde yeniden tanımlandılar ve 0-32 bayt durumu da yeniden tanımlandı. Değiş tokuş edilen nominal DH anahtarı 256 bayt olduğundan, minimal gösterimin 64 bayttan az olma olasılığı son derece düşüktür.

### Başlık Formatı

AES şifrelenmiş yük içinde, çeşitli mesajlar için minimal bir ortak yapı bulunur - bir baytlık bayrak ve dört baytlık gönderim zaman damgası (unix epoch'undan bu yana geçen saniyeler).

Header formatı şu şekildedir:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
Bayrak baytı aşağıdaki bit alanlarını içerir:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Yeniden anahtarlama ve genişletilmiş seçenekler olmadan, başlık boyutu 37 bayttır.

### Anahtar Yenileme {#rekey}

Rekey bayrağı ayarlanmışsa, zaman damgasından sonra 64 bayt anahtar materyali gelir.

Yeniden anahtarlama yapılırken, anahtar materyalinin ilk 32 baytı yeni MAC anahtarını üretmek için SHA256'ya beslenir ve sonraki 32 bayt yeni oturum anahtarını üretmek için SHA256'ya beslenir, ancak anahtarlar hemen kullanılmaz. Diğer taraf da rekey bayrağı ayarlanmış olarak ve aynı anahtar materyali ile yanıt vermelidir. Her iki taraf da bu değerleri gönderip aldıktan sonra, yeni anahtarlar kullanılmalı ve önceki anahtarlar atılmalıdır. Paket kaybı ve yeniden sıralamayı ele almak için eski anahtarları kısa bir süre saklamak faydalı olabilir.

NOT: Yeniden anahtarlama şu anda uygulanmamıştır.

### Genişletilmiş Seçenekler {#extend}

Genişletilmiş seçenekler bayrağı ayarlanmışsa, bir baytlık seçenek boyutu değeri eklenir ve ardından o kadar genişletilmiş seçenek baytı gelir. Genişletilmiş seçenekler her zaman spesifikasyonun bir parçası olmuştur, ancak 0.9.24 sürümüne kadar uygulanmamıştır. Mevcut olduğunda, seçenek formatı mesaj tipine özeldir. Belirtilen mesaj için genişletilmiş seçeneklerin beklenip beklenmediği ve belirtilen format hakkında aşağıdaki mesaj belgelerine bakın. Java router'lar her zaman bayrağı ve seçenek uzunluğunu tanımış olsa da, diğer uygulamalar tanımamıştır. Bu nedenle, 0.9.24 sürümünden eski router'lara genişletilmiş seçenekler göndermeyin.

## Dolgulama

Tüm mesajlar 0 veya daha fazla dolgu baytı içerir. [AES256 şifreleme katmanının](/docs/specs/cryptography/#AES) gerektirdiği şekilde, her mesaj 16 bayt sınırına kadar doldurulmalıdır.

0.9.7 sürümüne kadar, mesajlar yalnızca sonraki 16 bayt sınırına kadar dolduruluyordu ve 16 baytın katı olmayan mesajlar geçersiz olabiliyordu.

0.9.7 sürümü itibariyle, mevcut MTU'ya uyulduğu sürece mesajlar herhangi bir uzunluğa kadar doldurulabilir. Son 16 baytlık bloğun ötesindeki fazladan 1-15 dolgu baytı şifrelenemiyor veya çözümlenemiyor ve göz ardı edilecek. Ancak tam uzunluk ve tüm dolgu MAC hesaplamasına dahil edilir.

Sürüm 0.9.8 itibariyle, iletilen mesajlar mutlaka 16 baytın katı olmak zorunda değildir. SessionConfirmed mesajı bir istisnadır, aşağıya bakınız.

## Anahtarlar

SessionCreated ve SessionConfirmed mesajlarındaki imzalar, ağ veritabanında yayınlayarak bant dışı olarak dağıtılan [RouterIdentity](/docs/specs/common-structures/#routeridentity) içindeki [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) ve ilişkili [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) kullanılarak oluşturulur.

0.9.15 sürümüne kadar, imza algoritması her zaman DSA idi ve 40 bayt imza kullanılıyordu.

0.9.16 sürümü itibariyle, imza algoritması Bob'un [RouterIdentity](/docs/specs/common-structures/#routeridentity)'sinde bir [KeyCertificate](/docs/specs/common-structures/#key-certificates) tarafından belirtilebilir.

Hem giriş anahtarları hem de oturum anahtarları 32 bayttır ve Ortak yapılar spesifikasyonu [SessionKey](/docs/specs/common-structures/#sessionkey) tarafından tanımlanır. MAC ve şifreleme için kullanılan anahtar, aşağıda her mesaj için belirtilmiştir.

Giriş anahtarları harici bir kanal (ağ veritabanı) aracılığıyla teslim edilir, burada geleneksel olarak 0.9.47 sürümüne kadar router Hash ile aynı olmuşlar, ancak 0.9.48 sürümünden itibaren rastgele olabilirler.

## Notlar

### IPv6

Protokol spesifikasyonu hem 4-bayt IPv4 hem de 16-bayt IPv6 adreslerini destekler. SSU-over-IPv6, 0.9.8 sürümünden itibaren desteklenmektedir. IPv6 desteği hakkındaki ayrıntılar için aşağıdaki bireysel mesajların belgelerine bakınız.

### Zaman Damgaları {#time}

I2P'nin çoğu milisaniye çözünürlüğünde 8-bayt [Date](/docs/specs/common-structures/#date) zaman damgaları kullanırken, SSU bir saniyelik çözünürlüğe sahip 4-bayt işaretsiz tamsayı zaman damgaları kullanır. Bu değerler işaretsiz olduğu için, Şubat 2106'ya kadar taşmayacaktır.

## Mesajlar

10 mesaj (payload türleri) tanımlanmıştır:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (tür 0) {#sessionrequest}

Bu, bir oturum kurmak için gönderilen ilk mesajdır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Mevcut implementasyonda başlık dahil tipik boyut: 304 (IPv4) veya 320 (IPv6) bayt (mod-16 olmayan padding öncesi)

#### Genişletilmiş seçenekler

Not: 0.9.24 sürümünde uygulanmıştır.

- Minimum uzunluk: 3 (seçenek uzunluk baytı + 2 bayt)
- Seçenek uzunluğu: minimum 2
- 2 bayt bayrakları:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Notlar

- IPv4 ve IPv6 adresleri desteklenir.
- Yorumlanmamış veriler gelecekte challenge'lar için kullanılabilir.

### SessionCreated (tip 1) {#sessioncreated}

Bu bir [SessionRequest](#sessionrequest)'e verilen yanıttır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Başlık dahil tipik boyut, mevcut uygulamada: 368 bayt (IPv4 veya IPv6) (mod-16 olmayan dolgu öncesi)

#### Notlar

- IPv4 ve IPv6 adresleri desteklenir.
- Eğer relay etiketi sıfır değilse, Bob Alice için introducer (tanıtıcı) görevi yapmayı teklif ediyor. Alice daha sonra Bob'un adresini ve relay etiketini network database'inde yayınlayabilir.
- İmza için Bob, external port'unu kullanmalıdır, çünkü Alice doğrulama için bunu kullanacaktır. Eğer Bob'un NAT/firewall'u internal port'unu farklı bir external port'a eşlediyse ve Bob bunun farkında değilse, Alice'in doğrulaması başarısız olacaktır.
- İmzalarla ilgili ayrıntılar için yukarıdaki [Keys](#keys) bölümüne bakın. Alice, Bob'un public signing key'ini zaten network database'inden almıştır.
- 0.9.15 sürümüne kadar, imza her zaman 40 byte'lık DSA imzasıydı ve padding her zaman 8 byte'tı. 0.9.16 sürümünden itibaren, imza türü ve uzunluğu Bob'un [RouterIdentity](/docs/specs/common-structures/#routeridentity)'sindeki [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) türü tarafından belirlenir. Padding, 16 byte'ın katları için gerektiği kadar yapılır.
- Bu, gönderenin intro key'ini kullanan tek mesajdır. Diğer tüm mesajlar alıcının intro key'ini veya kurulmuş session key'ini kullanır.
- Signed-on time mevcut uygulamada kullanılmıyor veya doğrulanmıyor gibi görünmektedir.
- Yorumlanmamış veriler gelecekte challenge'lar için kullanılabilir.
- Header'daki extended seçenekler: Beklenmez, tanımsızdır.

### SessionConfirmed (tip 2) {#sessionconfirmed}

Bu bir [SessionCreated](#sessioncreated) mesajına verilen yanıttır ve bir oturum kurmanın son adımıdır. Router Identity parçalanması gerekiyorsa birden fazla SessionConfirmed mesajı gerekebilir.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 ile F-2 arası** (sadece F > 1 ise; şu anda kullanılmıyor, aşağıdaki notlara bakın):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (son veya tek fragment):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Mevcut implementasyonda başlık dahil tipik boyut: 512 bayt (Ed25519 imzası ile) veya 480 bayt (DSA-SHA1 imzası ile) (non-mod-16 padding öncesi)

#### Notlar

- Mevcut implementasyonda, maksimum fragment boyutu 512 bayttır. Bu, daha uzun imzaların fragmentasyon olmadan çalışması için genişletilmelidir.
  Mevcut implementasyon, iki fragment arasında bölünen imzaları doğru şekilde işlememektedir.
- Tipik [RouterIdentity](/docs/specs/common-structures/#routeridentity) 387 bayttır, bu nedenle hiçbir zaman fragmentasyon gerekli değildir. Eğer yeni kripto RouterIdentity boyutunu genişletirse,
  fragmentasyon şeması dikkatli bir şekilde test edilmelidir.
- Eksik fragmentları talep etme veya yeniden teslim etme mekanizması yoktur.
- Toplam fragmentlar alanı F tüm fragmentlarda aynı şekilde ayarlanmalıdır.
- DSA imzalarıyla ilgili detaylar için yukarıdaki [Keys](#keys) bölümüne bakın.
- İmzalanma zamanı mevcut implementasyonda kullanılmamış veya doğrulanmamış görünmektedir.
- İmza sonda olduğu için, son veya tek paketteki dolgu
  toplam paketi 16 baytın katına tamamlamalıdır, aksi takdirde imza
  doğru şekilde deşifre edilmeyecektir. Bu, dolgunun sonda olduğu
  diğer tüm mesaj türlerinden farklıdır.
- 0.9.15 sürümüne kadar, imza her zaman 40 baytlık bir DSA imzasıydı.
  0.9.16 sürümünden itibaren, imza türü ve uzunluğu Alice'in [RouterIdentity](/docs/specs/common-structures/#routeridentity)'sindeki [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) türü tarafından ima edilmektedir. Dolgu
  16 baytın katına gerektiği kadar yapılır.
- Header'daki genişletilmiş seçenekler: Beklenmez, tanımlanmamış.

### SessionDestroyed (tip 8) {#sessiondestroyed}

SessionDestroyed mesajı 0.8.1 sürümünde uygulandı (yalnızca alma) ve 0.8.9 sürümünden itibaren gönderilmektedir.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Bu mesaj herhangi bir veri içermez. Mevcut uygulamada başlık dahil tipik boyut: 48 bayt (mod-16 olmayan dolgu öncesi)

#### Notlar

- Gönderenin veya alıcının intro key'i ile alınan destroy mesajları yok sayılacaktır.
- Başlıktaki genişletilmiş seçenekler: Beklenmez, tanımsız.

### RelayRequest (tip 3) {#relayrequest}

Bu, Alice'in Bob'a Charlie ile tanışma talebinde bulunmak için gönderdiği ilk mesajdır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Mevcut uygulamada başlık dahil tipik boyut: 96 bayt (Alice IP dahil değil) veya 112 bayt (4-baytlık Alice IP dahil) (mod-16 olmayan dolgulama öncesi)

#### Notlar

- IP adresi yalnızca paketin kaynak adresi ve portundan farklıysa dahil edilir.
- Bu mesaj IPv4 veya IPv6 üzerinden gönderilebilir.
  Mesaj IPv4 introduction için IPv6 üzerinden veya 
  (0.9.50 sürümünden itibaren) IPv6 introduction için IPv4 üzerinden gönderiliyorsa,
  Alice kendi introduction adresini ve portunu dahil etmelidir.
  Bu özellik 0.9.50 sürümünden itibaren desteklenmektedir.
- Alice adresini/portunu dahil ederse, Bob devam etmeden önce ek doğrulama gerçekleştirebilir.
  - 0.9.24 sürümünden önce, Java I2P bağlantıdan farklı olan herhangi bir adresi veya portu reddederdi.
- Challenge uygulanmamıştır, challenge boyutu her zaman sıfırdır
- IPv6 için relaying 0.9.50 sürümünden itibaren desteklenmektedir.
- 0.9.12 sürümünden önce, Bob'un intro key'i her zaman kullanılırdı. 0.9.12 sürümünden itibaren,
  Alice ve Bob arasında kurulmuş bir oturum varsa session key kullanılır. Pratikte,
  kurulmuş bir oturum olmalıdır, çünkü Alice nonce'ı (introduction tag) yalnızca
  oluşturulan oturum mesajından alabilir ve Bob, oturum yok edildiğinde introduction tag'ı
  geçersiz olarak işaretleyecektir.
- Header'daki extended seçenekleri: Beklenmez, tanımsızdır.

### RelayResponse (tür 4) {#relayresponse}

Bu bir [RelayRequest](#relayrequest) yanıtıdır ve Bob'dan Alice'e gönderilir.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Mevcut uygulamada başlık dahil tipik boyut: 64 (Alice IPv4) veya 80 (Alice IPv6) bayt (mod-16 olmayan dolgu öncesi)

#### Notlar

- Bu mesaj IPv4 veya IPv6 üzerinden gönderilebilir.
- Alice'in IP adresi/portu, Bob'un RelayRequest'i aldığı görünen IP/port'tur (Alice'in RelayRequest'te dahil ettiği IP olmak zorunda değildir),
  ve IPv4 veya IPv6 olabilir. Alice şu anda bunları alırken görmezden gelir.
- Charlie'nin IP adresi IPv4 olabilir, ya da 0.9.50 sürümü itibariyle IPv6 olabilir,
  çünkü bu Alice'in Hole Punch'tan sonra
  SessionRequest'i göndereceği adrestir.
- IPv6 için relaying (aktarım) 0.9.50 sürümü itibariyle desteklenmektedir.
- 0.9.12 sürümünden önce, Alice'in intro anahtarı her zaman kullanılırdı. 0.9.12 sürümü itibariyle,
  Alice ve Bob arasında kurulmuş bir oturum varsa session anahtarı kullanılır.
- Header'daki genişletilmiş seçenekler: Beklenmez, tanımsızdır.

### RelayIntro (tip 5) {#relayintro}

Bu, Bob tarafından Charlie'ye gönderilen Alice için tanıtımdır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Mevcut uygulamada başlık dahil tipik boyut: 48 bayt (mod-16 olmayan dolgu öncesi)

#### Notlar

- IPv4 için, Alice'in IP adresi her zaman 4 bayttır, çünkü Alice Charlie'ye IPv4 üzerinden bağlanmaya çalışmaktadır.
  0.9.50 sürümü itibariyle IPv6 desteklenmekte ve Alice'in IP adresi 16 bayt olabilmektedir.
- IPv4 için, bu mesaj kurulmuş bir IPv4 bağlantısı üzerinden gönderilmelidir,
  çünkü Bob'un Charlie'nin IPv4 adresini bilip RelayResponse içinde Alice'e geri döndürebilmesinin tek yolu budur.
  0.9.50 sürümü itibariyle IPv6 desteklenmekte ve bu mesaj kurulmuş bir IPv6 bağlantısı üzerinden gönderilebilmektedir.
- 0.9.50 sürümü itibariyle, introducers ile yayınlanan herhangi bir SSU adresi "caps" seçeneğinde "4" veya "6" içermelidir.
- Challenge uygulanmamıştır, challenge boyutu her zaman sıfırdır
- Header içindeki genişletilmiş seçenekler: Beklenmemektedir, tanımsızdır.

### Veri (tip 6) {#data}

Bu mesaj veri aktarımı ve onaylama için kullanılır.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Veri:** 1 byte bayraklar (aşağıya bakın); açık ACK'ler dahil edilmişse: 1 byte ACK sayısı, o kadar 4 byte MessageId tamamen ACK'leniyor; ACK bitfield'ları dahil edilmişse: 1 byte ACK bitfield sayısı, o kadar 4 byte MessageId + 1 veya daha fazla byte ACK bitfield (notlara bakın); Genişletilmiş veri dahil edilmişse: 1 byte veri boyutu, o kadar byte genişletilmiş veri (şu anda yorumlanmıyor); 1 byte fragment sayısı (sıfır olabilir); Sıfır değilse, o kadar mesaj fragmenti.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Her fragment şunları içerir: - 4 byte messageId - 3 byte fragment bilgisi:   - bit 23-17: fragment # 0 - 127   - bit 16: isLast (1 = doğru)   - bit 15-14: kullanılmayan, gelecekteki kullanımlarla uyumluluk için 0'a ayarlı   - bit 13-0: fragment boyutu 0 - 16383 - o kadar byte fragment verisi

Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### ACK Bitfield Notları

Bit alanı her baytın düşük 7 bitini kullanır, yüksek bit ise ek bir bit alanı baytının onu takip edip etmediğini belirtir (1 = doğru, 0 = mevcut bit alanı baytı sonuncudur). Bu 7 bitlik dizi dizileri bir parçanın alınıp alınmadığını temsil eder - eğer bir bit 1 ise, parça alınmıştır. Açıklığa kavuşturmak için, 0, 2, 5 ve 9 parçalarının alındığını varsayarsak, bit alanı baytları şu şekilde olacaktır:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Notlar

- Mevcut uygulama, eğer alan mevcutsa, daha önce onaylanmış mesajlar için sınırlı sayıda yinelenen onay ekler.
- Eğer parça sayısı sıfırsa, bu yalnızca onay veya canlı tutma mesajıdır.
- ECN özelliği uygulanmamıştır ve bit hiçbir zaman ayarlanmaz.
- Mevcut uygulamada, parça sayısı sıfırdan büyük olduğunda yanıt isteme biti ayarlanır ve parça olmadığında ayarlanmaz.
- Genişletilmiş veri uygulanmamıştır ve hiçbir zaman mevcut değildir.
- Çoklu parça alımı tüm sürümlerde desteklenir. Çoklu parça iletimi 0.9.16 sürümünde uygulanmıştır.
- Şu anda uygulandığı şekliyle, maksimum parça sayısı 64'tür (maksimum parça numarası = 63).
- Şu anda uygulandığı şekliyle, maksimum parça boyutu elbette MTU'dan küçüktür.
- Gönderilecek çok sayıda ACK olsa bile maksimum MTU'yu aşmamaya dikkat edin.
- Protokol sıfır uzunluklu parçalara izin verir ancak bunları göndermenin bir nedeni yoktur.
- SSU'da, veri standart 16 bayt I2NP başlığı yerine kısa 5 bayt I2NP başlığının ardından I2NP mesajının yükünü kullanır. Kısa I2NP başlığı yalnızca tek bayt I2NP türü ve saniye cinsinden 4 bayt sona erme süresinden oluşur. I2NP mesaj kimliği, parça için mesaj kimliği olarak kullanılır. I2NP boyutu parça boyutlarından birleştirilir. UDP mesaj bütünlüğü şifre çözme ile sağlandığından I2NP checksum gerekli değildir.
- Mesaj kimlikleri sıra numaraları değildir ve ardışık değildir. SSU sıralı teslimatı garanti etmez. I2NP mesaj kimliğini SSU mesaj kimliği olarak kullansak da, SSU protokolü açısından bunlar rastgele sayılardır. Aslında, router tüm eşler için tek bir Bloom filtresi kullandığından, mesaj kimliği gerçek bir rastgele sayı olmalıdır.
- Sıra numaraları olmadığından, bir ACK'ın alındığından emin olmanın yolu yoktur. Mevcut uygulama rutin olarak büyük miktarda yinelenen ACK gönderir. Yinelenen ACK'lar tıkanıklık göstergesi olarak alınmamalıdır.
- ACK Bitfield notları: Bir veri paketinin alıcısı, son parçayı almadıkça mesajda kaç parça olduğunu bilmez. Bu nedenle, yanıt olarak gönderilen bitfield bayt sayısı, parça sayısının 7'ye bölünmesinden az veya fazla olabilir. Örneğin, alıcının gördüğü en yüksek parça 4 numaralıysa, toplamda 13 parça olsa bile yalnızca bir bayt gönderilmesi gerekir. Onaylanan her mesaj kimliği için 10 bayta kadar (yani (64 / 7) + 1) dahil edilebilir.
- Başlıktaki genişletilmiş seçenekler: Beklenmez, tanımsızdır.

### PeerTest (tip 7) {#peertest}

Detaylar için [SSU Eş Testi](/docs/transport/ssu/#peerTesting) bölümüne bakın. Not: IPv6 eş testi 0.9.27 sürümünden itibaren desteklenmektedir.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Kullanılan Kripto Anahtar (oluşum sırasına göre listelenmiştir): 1. Alice'den Bob'a gönderildiğinde: Alice/Bob sessionKey 2. Bob'dan Charlie'ye gönderildiğinde: Bob/Charlie sessionKey 3. Charlie'den Bob'a gönderildiğinde: Bob/Charlie sessionKey 4. Bob'dan Alice'e gönderildiğinde: Alice/Bob sessionKey (veya 0.9.52 öncesi Bob için, Alice'in introKey'i) 5. Charlie'den Alice'e gönderildiğinde: Alice'in introKey'i, Bob'dan PeerTest mesajında alındığı gibi 6. Alice'den Charlie'ye gönderildiğinde: Charlie'nin introKey'i, Charlie'den PeerTest mesajında alındığı gibi

Kullanılan MAC Anahtarı (oluşum sırasına göre listelendi): 1. Alice'den Bob'a gönderildiğinde: Alice/Bob MAC Anahtarı 2. Bob'dan Charlie'ye gönderildiğinde: Bob/Charlie MAC Anahtarı 3. Charlie'den Bob'a gönderildiğinde: Bob/Charlie MAC Anahtarı 4. Bob'dan Alice'e gönderildiğinde: Alice'in introKey'i, Alice'den alınan PeerTest mesajında alındığı şekliyle 5. Charlie'den Alice'e gönderildiğinde: Alice'in introKey'i, Bob'dan alınan PeerTest mesajında alındığı şekliyle 6. Alice'den Charlie'ye gönderildiğinde: Charlie'nin introKey'i, Charlie'den alınan PeerTest mesajında alındığı şekliyle

Mesaj formatı:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Mevcut uygulamada başlık dahil tipik boyut: 80 bayt (mod-16 olmayan dolgu öncesi)

#### Notlar

- Alice tarafından gönderildiğinde, IP adresi boyutu 0'dır, IP adresi mevcut değildir ve port 0'dır, çünkü Bob ve Charlie veriyi kullanmaz; amaç Alice'in gerçek IP adresi/port'unu belirlemek ve Alice'e söylemektir; Bob ve Charlie, Alice'in kendi adresinin ne olduğunu düşündüğünü umursamaz.
- Bob veya Charlie tarafından gönderildiğinde, IP ve port mevcuttur ve IP adresi 4 veya 16 bayttır. IPv6 testi, 0.9.27 sürümü itibarıyla desteklenir.
- Charlie tarafından Alice'e gönderildiğinde, IP ve port şu şekildedir:
  İlk sefer (mesaj 5): Mesaj 2'de alındığı şekliyle Alice'in istediği IP ve port.
  İkinci sefer (mesaj 7): Mesaj 6'nın alındığı Alice'in gerçek IP ve port'u.
- IPv6 Notları: 0.9.26 sürümüne kadar, yalnızca IPv4 adreslerinin testi desteklenir. Bu nedenle, tüm Alice-Bob ve Alice-Charlie iletişimi IPv4 üzerinden olmalıdır. Ancak Bob-Charlie iletişimi IPv4 veya IPv6 üzerinden olabilir. Alice'in adresi, PeerTest mesajında belirtildiğinde, 4 bayt olmalıdır.
  0.9.27 sürümü itibarıyla, IPv6 adreslerinin testi desteklenir ve Bob ile Charlie yayınlanan IPv6 adreslerinde 'B' yetenekliliği ile destek belirtirse, Alice-Bob ve Alice-Charlie iletişimi IPv6 üzerinden olabilir.
  Ayrıntılar için Öneri 126'ya bakın.
- Alice, test etmek istediği transport (IPv4 veya IPv6) üzerinden mevcut bir oturum kullanarak Bob'a istek gönderir.
  Bob, Alice'den IPv4 üzerinden bir istek aldığında, Bob bir IPv4 adresi tanıtan bir Charlie seçmelidir.
  Bob, Alice'den IPv6 üzerinden bir istek aldığında, Bob bir IPv6 adresi tanıtan bir Charlie seçmelidir.
  Gerçek Bob-Charlie iletişimi IPv4 veya IPv6 üzerinden olabilir (yani Alice'in adres türünden bağımsızdır).
- Bir peer, aktif test durumlarının (nonce'ların) tablosunu tutmalıdır. Bir PeerTest mesajı alındığında, tabloda nonce'u arayın. Bulunursa, bu mevcut bir testtir ve rolünüzü bilirsiniz (Alice, Bob veya Charlie). Aksi takdirde, IP mevcut değilse ve port 0 ise, bu yeni bir testtir ve siz Bob'sınız. Aksi takdirde, bu yeni bir testtir ve siz Charlie'siniz.
- 0.9.15 sürümü itibarıyla, Alice'in Bob ile kurulmuş bir oturumu olmalı ve oturum anahtarını kullanmalıdır.
- API sürüm 0.9.52'den önce, bazı uygulamalarda Bob, Alice ve Bob'un kurulmuş bir oturumu olmasına rağmen (0.9.15'ten beri), Alice/Bob oturum anahtarı yerine Alice'in intro anahtarını kullanarak Alice'e yanıt veriyordu.
  API sürüm 0.9.52 itibarıyla, Bob tüm uygulamalarda oturum anahtarını doğru şekilde kullanacak ve Alice, Bob'un API sürümü 0.9.52 veya daha yüksekse, Bob'dan Alice'in intro anahtarıyla alınan mesajı reddetmelidir.
- Başlıktaki genişletilmiş seçenekler: Beklenmez, tanımsızdır.

### HolePunch {#holepunch}

HolePunch basitçe veri içermeyen bir UDP paketidir. Kimlik doğrulaması yapılmamış ve şifrelenmemiştir. SSU başlığı içermediği için mesaj türü numarası yoktur. Introduction dizisinin bir parçası olarak Charlie'den Alice'e gönderilir.

## Örnek Datagramlar {#sampledatagrams}

### Minimal veri mesajı

- fragman yok, ACK yok, NACK yok, vb.
- Boyut: 39 bayt

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Yük içeren minimal veri mesajı

- Boyut: 46+fragmentSize bayt

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Kaynakça

- [AES Şifreleme](/docs/specs/cryptography/#AES)
- [Ortak Yapılar Spesifikasyonu](/docs/specs/common-structures/)
- [Tarih](/docs/specs/common-structures/#date)
- [ElGamal Şifreleme](/docs/specs/cryptography/#elgamal)
- [HMAC Ayrıntıları](/docs/specs/cryptography/#udp)
- [I2P Kaynak Kodu](https://github.com/i2p/i2p.i2p)
- [i2pd Kaynak Kodu](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [İmza](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [SSU Genel Bakış](/docs/transport/ssu/)
- [SSU Anahtarları](/docs/transport/ssu/#keys)
- [SSU Peer Testing](/docs/transport/ssu/#peerTesting)
