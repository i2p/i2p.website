---
title: "Datagram2 Protokolü"
number: "163"
author: "zzz, orijinal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Kapalı"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Durum

2025-04-15 tarihli incelemede onaylanmıştır.
Spesifikasyonlara dahil edilmiştir.
Java I2P'de API 0.9.66 itibariyle uygulanmıştır.
Durum için uygulama dokümantasyonunu kontrol edin.


## Genel Bakış

[Prop123](/proposals/123-new-netdb-entries/) 'den bağımsız bir öneri olarak çıkarılmıştır.

Çevrimdışı imzalar, yanıtlanabilir datagram işlemede doğrulanamaz.
Çevrimdışı imzalandığını belirtmek için bir bayrağa ihtiyaç var ama bayrak koyacak yer yok.

Yeni bir I2CP protokol numarası ve formatı gerektirir,
[DATAGRAMS](/docs/api/datagrams/) spesifikasyonuna eklenmelidir.
Buna "Datagram2" diyelim.


## Amaçlar

- Çevrimdışı imzalar için destek ekle
- Tekrar direnci ekle
- İmzalar olmadan seçenek ekle
- Esneklik sağlamak için bayraklar ve seçenekler alanları ekle


## Amaç Dışı Kalanlar

Tıkanıklık kontrolü vb. için tam uçtan uca protokol desteği.
Bu, Datagram2'nin üzerine veya bir alternatifi olarak inşa edilirdi, ki bu düşük seviye bir protokoldür.
Yüksek performanslı bir protokolü sadece Datagram2'nin üzerine tasarlamak mantıklı olmaz,
çünkü from alanı ve imza ek yükünden dolayı.
Bu tür bir protokol, önce Datagram2 ile bir el sıkışması yapmalı, ardından
RAW datagramlarına geçmelidir.


## Motivasyon

2019 yılında tamamlanan LS2 çalışmalarının kalanı.

Datagram2'yi kullanan ilk uygulamanın
i2psnark ve zzzot'ta uygulandığı gibi, bittorrent UDP duyuruları olması beklenmektedir,
bkz. [Prop160](/proposals/160-udp-trackers/).


## Yanıtlanabilir Datagram Spesifikasyonu

Referans için, işte [Datagrams](/docs/api/datagrams/) 'dan kopyalanan yanıtlanabilir datagramlar için spesifikasyonun bir incelemesi.
Yanıtlanabilir datagramlar için standart I2CP protokol numarası PROTO_DATAGRAM (17)'dir.

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//

  from :: bir `Destination`
          uzunluk: 387+ bayt
          Datagramın oluşturucusu ve imzalayanı

  signature :: bir `Signature`
               İmza türü $from'un imzalama genel anahtar türüyle eşleşmelidir
               uzunluk: İmza türü tarafından belirtilen şekilde 40+ bayt.
               Varsayılan DSA_SHA1 anahtar türü için:
                  SHA-256 hash'inin DSA `Signature`'ı.
               Diğer anahtar türleri için:
                  Verinin `Signature`'ı.
               İmza, $from'un imzalama genel anahtarı ile doğrulanabilir

  payload ::  Veriler
              Uzunluk: 0 ile yaklaşık 31,5 KB (+/- notlar)

  Toplam uzunluk: Payload uzunluğu + 423+
```


## Tasarım

- Yeni protokol 19 - Seçenekli yanıtlanabilir datagram tanımlayın.
- Yeni protokol 20 - İmza olmadan yanıtlanabilir datagram tanımlayın.
- Çevrimdışı imzalar ve gelecekteki genişleme için bayrak alanı ekleyin
- Daha kolay işleme için imzayı veri yükünün sonuna taşıyın
- Yanıtlanabilir datagram veya akış olarak yorumlandığında imza doğrulaması başarısız olacak şekilde farklı bir imza spesifikasyonu.
  Bu, imzayı veri yükünün sonuna taşıyarak,
  ve imza fonksiyonuna hedef hash'i dahil ederek gerçekleştirilir.
- [Prop164](/proposals/164-streaming/) 'de akış için yapıldığı gibi, datagramlar için tekrar önleme ekleyin.
- Keyfi seçenekler için bölüm ekleyin
- [Common](/docs/specs/common-structures/) ve [Streaming](/docs/specs/streaming/) 'den çevrimdışı imza formatını yeniden kullanın.
- Çevrimdışı imza bölümü, değişken uzunlukta
  veri yükü ve imza bölümleri öncesinde olmalıdır, çünkü bu imzanın uzunluğunu belirtir.


## Spesifikasyon

### Protokol

Datagram2 için yeni I2CP protokol numarası 19'dur.
Bunu [I2CP](/docs/specs/i2cp/) 'ye PROTO_DATAGRAM2 olarak ekleyin.

Datagram3 için yeni I2CP protokol numarası 20'dir.
Bunu [I2CP](/docs/specs/i2cp/) 'ye PROTO_DATAGRAM2 olarak ekleyin.


### Datagram2 Formatı

Aşağıdaki şekilde [DATAGRAMS](/docs/api/datagrams/) 'e Datagram2 ekleyin:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: bir `Destination`
          uzunluk: 387+ bayt
          Datagramın oluşturucusu ve (çevrimdışı imzalanmamışsa) imzalayanı

  flags :: (2 bayt)
           Bit sırası: 15 14 ... 3 2 1 0
           Bit 3-0: Versiyon: 0x02 (0 0 1 0)
           Bit 4: Eğer 0 ise, seçenek yok; eğer 1 ise, seçenek eşlemesi dahil edilir
           Bit 5: Eğer 0 ise, çevrimdışı imza yok; eğer 1 ise, çevrimdışı imzalanmış
           Bit 15-6: kullanılmaz, gelecekteki kullanımlar için uyumluluk amacıyla 0'a ayarlayın

  options :: (varsa 2+ bayt)
           Eğer bayrak seçeneklerin mevcut olduğunu belirtiyorsa, keyfi metin seçenekleri içeren bir `Mapping`

  offline_signature ::
               Eğer bayrak çevrimdışı anahtarları belirtiyorsa, çevrimdışı imza bölümü,
               Ortak Yapılar Spesifikasyonu'nda belirtildiği gibi,
               aşağıdaki 4 alanla. Uzunluk: çevrimdışı ve çevrimdışı
               imza türlerine göre değişir, genellikle Ed25519 için 102 bayt
               Bu bölüm, çevrimdışı olarak oluşturulabilir ve oluşturulmalıdır.

    expires :: Geçerlilik süresi sonu zaman damgası
               (4 bayt, büyük endian, epoch'tan bu yana saniye, 2106'da sıfırlanır)

    sigtype :: Geçici imza türü (2 bayt, büyük endian)

    pubkey :: Geçici imza genel anahtarı (uzunluk imza türü tarafından belirtilir),
              genellikle Ed25519 imza türü için 32 bayt.

    offsig :: bir `Signature`
              Geçerlilik süresi sonu zaman damgasının, geçici imza türünün
              ve genel anahtarın, hedef genel anahtarı ile imzası,
              uzunluk: İmza türü tarafından belirtilen şekilde 40+ bayt, genellikle
              Ed25519 imza türü için 64 bayt.

  payload ::  Veriler
              Uzunluk: notlara bakınız, 0 ile yaklaşık 61 KB arası

  signature :: bir `Signature`
               İmza türü $from'un imzalama genel anahtar türüyle (çevrimdışı
               imza yoksa) veya geçici imza türüyle (çevrimdışı imzalanmışsa
               eşleşmelidir)
               uzunluk: İmza türü tarafından belirtilen şekilde 40+ bayt, genellikle
               Ed25519 imza türü için 64 bayt.
               Aşağıda belirtilen alanlar ve veriler için imza.
               İmza `$from`un imzalama genel anahtarı ile (çevrimdışı
               imza yoksa) veya geçici genel anahtar ile (çevrimdışı
               imzalanmışsa) doğrulanır.

```

Toplam uzunluk: minimum 433 + veri yükü uzunluğu;
çevrimdışı imzalar olmadan X25519 göndericileri için tipik uzunluk:
457 + veri yükü uzunluğu.
Mesaj, I2CP katmanında genellikle gzip ile sıkıştırılır,
bu da sıkıştırılabilir durumda olan gönderen için önemli tasarruflar sağlar.

Not: Çevrimdışı imza formatı, Ortak Yapılar [Common](/docs/specs/common-structures/) ve [Streaming](/docs/specs/streaming/) 'deki ile aynıdır.

### İmzalar

İmza, aşağıdaki alanları içerir.

- Önsöz: Hedef destinasyonun 32 baytlık hashi (datagramda dahil değildir)
- bayraklar
- seçenekler (varsa)
- çevrimdışı imza (varsa)
- veri

Yanıtlanabilir datagramda, DSA_SHA1 anahtar türü için, imza
SHA-256 hash'inin değil, verinin bizzat kendisinin üzerindeydi;
burada, imza
alanlar üzerindedir (hash üzerinde DEĞİL), anahtar türü ne olursa olsun.


### ToHash Doğrulama

Alıcılar, imzayı (hedef hash'lerini kullanarak) doğrulamalı
ve başarısızlık durumunda datagramı reddetmelidir. Bu, tekrar önlemeye yöneliktir.


### Datagram3 Formatı

Aşağıdaki şekilde [DATAGRAMS](/docs/api/datagrams/) 'e Datagram3 ekleyin:

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: bir `Hash`
              uzunluk: 32 bayt
              Datagramın oluşturucusu

  flags :: (2 bayt)
           Bit sırası: 15 14 ... 3 2 1 0
           Bit 3-0: Versiyon: 0x03 (0 0 1 1)
           Bit 4: Eğer 0 ise, seçenek yok; eğer 1 ise, seçenek eşlemesi dahil edilir
           Bit 15-5: kullanılmaz, gelecekteki kullanımlar için uyumluluk amacıyla 0'a ayarlayın

  options :: (varsa 2+ bayt)
           Eğer bayrak seçeneklerin mevcut olduğunu belirtiyorsa, keyfi metin seçenekleri içeren bir `Mapping`

  payload ::  Veriler
              Uzunluk: notlara bakınız, 0 ile yaklaşık 61 KB arası

```

Toplam uzunluk: minimum 34 + veri yükü uzunluğu.


### SAM

SAMv3 spesifikasyonuna STYLE=DATAGRAM2 ve STYLE=DATAGRAM3 ekleyin.
Çevrimdışı imzalar hakkındaki bilgiyi güncelleyin.


### Ekstra Yük

Bu tasarım yanıtlanabilir datagramlara 2 bayt bayrak ek yükü ekler.
Bu kabul edilebilir.


## Güvenlik Analizi

Hedef hash'i imzaya dahil etmek, tekrar saldırılarını önlemede etkili olmalıdır.

Datagram3 formatı imzalar içermez, bu yüzden gönderici doğrulanamaz
ve tekrar saldırılarına açıktır. Gerekli tüm doğrulama uygulama katmanında veya yönlendirici tarafından tıklama katmanında yapılmalıdır.


## Notlar

- Pratik uzunluk, protokollerin daha alt katmanları tarafından sınırlıdır - tünel
  mesaj spesifikasyonu [TUNMSG](/docs/specs/tunnel-message/#notes) mesajları yaklaşık 61,2 KB ile sınırlar ve taşıma
  [TRANSPORT](/docs/transport/) şu anda mesajları yaklaşık 64 KB ile sınırlar, bu yüzden burada veri uzunluğu
  yaklaşık 61 KB ile sınırlıdır.
- Büyük datagramların güvenilirliği hakkında önemli notlara bakın [API](/docs/api/datagrams/).
  En iyi sonuçlar için veri yükünü yaklaşık 10 KB veya daha az ile sınırlayın.


## Uyumluluk

Yok. Uygulamalar, protokol ve/veya porta göre Datagram2 I2CP mesajlarını yönlendirecek şekilde
yeniden yazılmalı.
Yanlış yönlendirilmiş ve
Yanıtlanabilir datagram veya akış mesajları olarak yorumlanan Datagram2 mesajları,
imza, format veya her ikisine de dayalı olarak başarısız olur.


## Geçiş

Her UDP uygulaması ayrı ayrı destek tespit etmeli ve geçiş yapmalı.
En belirgin UDP uygulaması bittorrenttir.

### Bittorrent

Bittorrent DHT: Muhtemelen bir uzatma bayrağı gerek,
ör., i2p_dg2, BiglyBT ile koordine edin

Bittorrent UDP Anonsları [Prop160](/proposals/160-udp-trackers/): Baştan beri tasarımda.
Coordindate BiglyBT, i2psnark, zzzot ile

### Diğerleri

Bote: Geçiş yapma olasılığı düşük, aktif olarak bakımı yapılmıyor

Streamr: Kimse kullanmıyor, geçiş planlanmadı

SAM UDP uygulamaları: Bilinen yok


## Referanslar

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/transport/)
* [TUNMSG](/docs/specs/tunnel-message/#notes)
