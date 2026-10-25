---
title: "NTCP (NIO-tabanlı TCP)"
description: "I2P için eski Java NIO tabanlı TCP taşıma protokolü, NTCP2 ile değiştirildi"
slug: "ntcp"
aliases:
  - "/tr/docs/transport/ntcp"
  - "/tr/docs/transport/ntcp/"
  - "/tr/docs/ntcp"
  - "/tr/docs/ntcp/"
  - "/tr/ntcp"
  - "/tr/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

KULLANIM DIŞI, ARTIK DESTEKLENMİYOR. 0.9.40 2019-05 sürümünden itibaren varsayılan olarak devre dışı bırakıldı. 0.9.50 2021-05 sürümünden itibaren destek kaldırıldı. [NTCP2](/docs/specs/ntcp2) ile değiştirildi. NTCP, I2P 0.6.1.22 sürümünde tanıtılan Java NIO tabanlı bir taşıma protokolüdür. Java NIO (new I/O), eski TCP taşıma protokolünün bağlantı başına 1 thread sorunlarından muzdarip değildir. NTCP-over-IPv6, 0.9.8 sürümünden itibaren desteklenmektedir.

Varsayılan olarak, NTCP, SSU tarafından otomatik olarak algılanan IP/Port'u kullanır. config.jsp'de etkinleştirildiğinde, SSU harici adres değiştiğinde veya güvenlik duvarı durumu değiştiğinde NTCP'yi bilgilendirir/yeniden başlatır. Artık statik IP veya dyndns hizmeti olmadan gelen TCP'yi etkinleştirebilirsiniz.

I2P içindeki NTCP kodu, güvenilir teslimat için altta yatan Java TCP taşıma protokolünü kullandığından nispeten hafiftir (SSU kodunun 1/4'ü kadar).

## Router Adresi Spesifikasyonu {#ra}

Aşağıdaki özellikler ağ veritabanında saklanır.

- **Transport adı:** NTCP
- **host:** IP (IPv4 veya IPv6).
  Kısaltılmış IPv6 adresi ("::" ile) kabul edilir.
  Host adları daha önce izin veriliyordu, ancak 0.9.32 sürümü itibariyle kullanımdan kaldırıldı. Öneri 141'e bakınız.
- **port:** 1024 - 65535

## NTCP Protokol Spesifikasyonu

### Standart Mesaj Formatı

Kurulumdan sonra, NTCP transport basit bir checksum ile bireysel I2NP mesajları gönderir. Şifrelenmemiş mesaj şu şekilde kodlanır:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Veri daha sonra AES/256/CBC ile şifrelenir. Şifreleme için oturum anahtarı, kuruluş sırasında (Diffie-Hellman 2048 bit kullanılarak) görüşülür. İki router arasındaki kuruluş, EstablishState sınıfında uygulanır ve aşağıda detaylandırılır. AES/256/CBC şifrelemesi için IV, önceki şifrelenmiş mesajın son 16 baytıdır.

Toplam mesaj uzunluğunu (altı boyut ve sağlama toplamı baytı dahil) 16'nın katına getirmek için 0-15 bayt dolgu gereklidir. Maksimum mesaj boyutu şu anda 16 KB'dir. Bu nedenle maksimum veri boyutu şu anda 16 KB - 6 veya 16378 bayttır. Minimum veri boyutu 1'dir.

### Zaman Senkronizasyon Mesajı Formatı

Özel bir durum, sizeof(data) değerinin 0 olduğu metadata mesajıdır. Bu durumda, şifrelenmemiş mesaj şu şekilde kodlanır:

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Toplam uzunluk: 16 bayt. Zaman senkronizasyonu mesajı yaklaşık 15 dakikalık aralıklarla gönderilir. Mesaj, standart mesajlar gibi şifrelenir.

### Sağlama Toplamları

Standart ve zaman senkronizasyonu mesajları [ZLIB Spesifikasyonu](http://tools.ietf.org/html/rfc1950)'nda tanımlandığı gibi Adler-32 sağlama toplamını kullanır.

### Boşta Kalma Zaman Aşımı

Boşta kalma zaman aşımı ve bağlantı kapatma her endpoint'in takdirine bağlıdır ve değişiklik gösterebilir. Mevcut uygulama, bağlantı sayısı yapılandırılan maksimuma yaklaştıkça zaman aşımını düşürür ve bağlantı sayısı azken zaman aşımını artırır. Önerilen minimum zaman aşımı iki dakika veya daha fazladır ve önerilen maksimum zaman aşımı on dakika veya daha fazladır.

### RouterInfo Değişimi

Kurulumdan sonra ve bundan sonra her 30-60 dakikada bir, iki router genellikle DatabaseStoreMessage kullanarak RouterInfo'ları değiş tokuş etmelidir. Ancak, Alice kuyruktaki ilk mesajın bir DatabaseStoreMessage olup olmadığını kontrol etmelidir ki yinelenen bir mesaj göndermesin; bu durum floodfill router'a bağlanırken sıklıkla görülür.

### Kurulum Sırası

Establish durumunda, DH anahtarları ve imzaları değiş tokuş etmek için 4 aşamalı bir mesaj dizisi vardır. İlk iki mesajda 2048-bit Diffie Hellman değiş tokuşu gerçekleşir. Ardından, bağlantıyı doğrulamak için kritik verilerin imzaları değiş tokuş edilir.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### DH Anahtar Değişimi {#DH}

İlk 2048-bit DH anahtar değişimi, I2P'nin [ElGamal şifrelemesi](/docs/specs/cryptography#elgamal) için kullandığı aynı paylaşılan asal sayı (p) ve üreteci (g) kullanır.

DH anahtar değişimi aşağıda gösterilen bir dizi adımdan oluşur. Bu adımlar ile I2P router'lar arasında gönderilen mesajlar arasındaki eşleştirme kalın harflerle işaretlenmiştir.

1. Alice gizli bir x tamsayısı üretir. Ardından `X = g^x mod p` hesaplar.
2. Alice, X'i Bob'a gönderir **(Mesaj 1)**.
3. Bob gizli bir y tamsayısı üretir. Ardından `Y = g^y mod p` hesaplar.
4. Bob, Y'yi Alice'e gönderir. **(Mesaj 2)**
5. Alice artık `sessionKey = Y^x mod p` hesaplayabilir.
6. Bob artık `sessionKey = X^y mod p` hesaplayabilir.
7. Hem Alice hem de Bob artık paylaşılan bir `sessionKey = g^(x*y) mod p` anahtarına sahiptir.

sessionKey daha sonra **Mesaj 3** ve **Mesaj 4**'te kimliklerin değişimi için kullanılır. DH değişimi için üs (x ve y) uzunluğu [kriptografi sayfasında](/docs/specs/cryptography#exponent) belgelenmiştir.

#### Oturum Anahtarı Detayları

32 baytlık oturum anahtarı şu şekilde oluşturulur:

1. Değiştirilen DH anahtarını, pozitif minimal uzunlukta BigInteger bayt dizisi olarak alın (two's complement big-endian)
2. En anlamlı bit 1 ise (yani array[0] & 0x80 != 0), Java'nın BigInteger.toByteArray() gösterimi gibi başa bir 0x00 baytı ekleyin
3. Bu bayt dizisi 32 bayt veya daha büyükse, ilk (en anlamlı) 32 baytı kullanın
4. Bu bayt dizisi 32 baytten küçükse, 32 bayta genişletmek için sonuna 0x00 baytları ekleyin. *(son derece düşük ihtimal)*

#### Mesaj 1 (Oturum İsteği)

Bu DH isteğidir. Alice, Bob'un [network database](/docs/overview/network-database)'inde yayımlanmış olan [Router Info](/docs/specs/common-structures#struct_RouterInfo)'sunda bulunan [Router Identity](/docs/specs/common-structures#struct_RouterIdentity), IP adresi ve portuna zaten sahiptir. Alice, Bob'a şunu gönderir:

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
İçindekiler:

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Notlar:**

- Bob, kendi router hash'ini kullanarak HXxorHI'yi doğrular. Eğer doğrulanamazsa, Alice yanlış router'a bağlanmış demektir ve Bob bağlantıyı keser.

#### Mesaj 2 (Oturum Oluşturuldu)

Bu DH yanıtıdır. Bob Alice'e şunu gönderir:

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Şifrelenmemiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Şifrelenmiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Notlar:**

- Alice, tsB kullanılarak hesaplanan Bob ile saat farkı çok yüksekse bağlantıyı düşürebilir.

#### Mesaj 3 (Oturum Onayı A)

Bu Alice'in router kimliğini ve kritik verilerin imzasını içerir. Alice, Bob'a şunu gönderir:

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Şifrelenmemiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Şifrelenmiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Notlar:**

- Bob imzayı doğrular ve başarısızlık durumunda bağlantıyı keser.
- Bob, tsA kullanılarak hesaplanan Alice ile saat sapması çok yüksekse bağlantıyı kesebilir.
- Alice bu mesajın şifreli içeriğinin son 16 baytını bir sonraki mesaj için IV olarak kullanacaktır.
- 0.9.15 sürümüne kadar, router identity her zaman 387 bayt, imza her zaman 40 baytlık DSA imzası ve padding her zaman 15 bayttı. 0.9.16 sürümünden itibaren, router identity 387 bayttan daha uzun olabilir ve imza tipi ile uzunluğu Alice'in [Router Identity](/docs/specs/common-structures#struct_RouterIdentity)'sindeki [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) tipinden çıkarılır. Padding, tüm şifrelenmemiş içerik için 16 baytın katı olacak şekilde gerektiği kadardır.
- Mesajın toplam uzunluğu, Router Identity'yi okumak için kısmen çözmeden belirlenemez. Router Identity'nin minimum uzunluğu 387 bayt ve minimum Signature uzunluğu 40 (DSA için) olduğundan, minimum toplam mesaj boyutu 2 + 387 + 4 + (imza uzunluğu) + (16 bayta padding) veya DSA için 2 + 387 + 4 + 40 + 15 = 448'dir. Alıcı, gerçek Router Identity uzunluğunu belirlemek için çözmeden önce bu minimum miktarı okuyabilir. Router Identity'deki küçük Certificate'lar için bu muhtemelen tüm mesaj olacaktır ve mesajda ek bir çözme işlemi gerektiren başka bayt olmayacaktır.

#### Mesaj 4 (Oturum Onayı B)

Bu kritik verilerin imzasıdır. Bob, Alice'e şunu gönderir:

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Şifrelenmemiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Şifrelenmiş İçerikler:

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Notlar:**

- Alice imzayı doğrular ve başarısızlık durumunda bağlantıyı keser.
- Bob bu mesajın şifrelenmiş içeriğinin son 16 baytını bir sonraki mesaj için IV olarak kullanacak.
- 0.9.15 sürümü dahil olmak üzere, imza her zaman 40 baytlık bir DSA imzasıydı ve dolgu her zaman 8 bayttı. 0.9.16 sürümünden itibaren, imza türü ve uzunluğu Bob'un [Router Identity](/docs/specs/common-structures#struct_RouterIdentity)'sindeki [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) türü tarafından belirlenir. Dolgu, tüm şifrelenmemiş içeriğin 16 baytın katları olacak şekilde gerektiği kadar uygulanır.

#### Kurulduktan Sonra

Bağlantı kuruldu ve standart veya zaman senkronizasyonu mesajları değiştirilebilir. Sonraki tüm mesajlar, müzakere edilen DH oturum anahtarı kullanılarak AES ile şifrelenir. Alice, bir sonraki IV olarak mesaj #3'ün şifrelenmiş içeriğinin son 16 baytını kullanacaktır. Bob, bir sonraki IV olarak mesaj #4'ün şifrelenmiş içeriğinin son 16 baytını kullanacaktır.

### Bağlantı Kontrol Mesajı

Alternatif olarak, Bob bir bağlantı aldığında, bu bir kontrol bağlantısı olabilir (belki Bob'un birinden dinleyicisini doğrulamasını istemesi sonucunda). Check Connection şu anda kullanılmamaktadır. Ancak, kayıt için, kontrol bağlantıları aşağıdaki gibi biçimlendirilir. Bir kontrol bilgi bağlantısı şunları içeren 256 bayt alacaktır:

- 32 bayt yorumlanmayan, göz ardı edilen veri
- 1 bayt boyut
- yerel router'ın IP adresini oluşturan o kadar bayt (uzak tarafça ulaşıldığı şekliyle)
- yerel router'ın ulaşıldığı 2 bayt port numarası
- uzak tarafça bilinen 4 bayt i2p ağ zamanı (epoch'tan bu yana geçen saniyeler)
- 223. bayta kadar yorumlanmayan dolgu verisi
- yerel router'ın kimlik hash'i ile 32. bayttan 223. bayta kadar olan baytların SHA256'sının xor'u

Bağlantı kontrolü, 0.9.12 sürümü itibariyle tamamen devre dışı bırakılmıştır.

## Tartışma

Şimdi [NTCP Tartışma Sayfası](/docs/discussions/ntcp)'nda.

## Gelecek Çalışmalar {#future}

- Maksimum mesaj boyutu yaklaşık 32 KB'ye yükseltilmelidir.

- Sabit paket boyutları kümesi, veri parçalanmasını dış saldırganlara karşı daha fazla gizlemek için uygun olabilir, ancak o zamana kadar tunnel, garlic ve uçtan uca dolgulamanın çoğu ihtiyaç için yeterli olması gerekir.
  Ancak şu anda, sınırlı sayıda mesaj boyutu oluşturmak için sonraki 16-baytlık sınırın ötesinde dolgulamaya yönelik herhangi bir hüküm bulunmamaktadır.

- NTCP için bellek kullanımı (kernel'inkini de dahil ederek) SSU ile karşılaştırılmalıdır.

- Kuruluş mesajları, başlangıç paket boyutlarına dayalı I2P trafiği tanımlamasını engellemek için bir şekilde rastgele doldurulabilir mi?
