---
title: "Daha Küçük Tünel Yapı Mesajları"
number: "157"
author: "zzz, orjinal"
created: "2020-10-09"
lastupdated: "2021-07-31"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2957"
target: "0.9.51"
toc: true
---

## Not
Uygulandı, API sürüm 0.9.51'den itibaren.
Ağ dağıtımı ve test süreci devam ediyor.
Küçük revizyonlara tabi olabilir.
Nihai spesifikasyon için [I2NP](/docs/specs/i2np/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerine bakınız.

## Genel Bakış

### Özet

Şu anda şifrelenmiş tünel Yapı İstek ve Yanıt kayıtlarının boyutu 528'dir.
Tipik Değişken Tünel Yapı ve Değişken Tünel Yapı Yanıt mesajları için,
toplam boyut 2113 bayttır. Bu mesaj, ters yol için üç 1KB tünel
mesajına bölünmektedir.

ECIES-X25519 yönlendiricileri için 528 baytlık kayıt formatındaki değişiklikler [Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde belirtilmiştir.
Bir tünelde ElGamal ve ECIES-X25519 yönlendiricilerinin karışımı için, kayıt boyutunun
528 bayt olarak kalması gerekmektedir. Ancak, bir tüneldeki tüm yönlendiriciler ECIES-X25519 ise,
yeni, daha küçük bir yapı kaydı mümkün olabilir, çünkü ECIES-X25519 şifrelemesinin ElGamal'a göre
çok daha az ek yükü vardır.

Daha küçük mesajlar bant genişliğinden tasarruf sağlar. Ayrıca, mesajlar bir tünel mesajına
sığabilirse, ters yol üç kat daha verimli olur.

Bu öneri, yeni istek ve yanıt kayıtlarını ve yeni Yapı İstek ve Yapı Yanıt mesajlarını tanımlar.

Tünel oluşturucu ve oluşturulan tüneldeki tüm adımlar ECIES-X25519 olmalı ve en az 0.9.51 sürümüne sahip olmalıdır.
Bu öneri, ağdaki yönlendiricilerin çoğunluğu ECIES-X25519 olana kadar faydalı olmayacaktır.
Bu durumun 2021 yılı sonuna kadar gerçekleşmesi beklenmektedir.

### Hedefler

Ek hedefler için [Prop152](/proposals/152-ecies-tunnels/) ve [Prop156](/proposals/156-ecies-routers/) belgelerine bakınız.

- Daha küçük kayıtlar ve mesajlar
- Gelecekteki seçenekler için yeterli alanı koruma, [Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde olduğu gibi
- Ters yol için bir tünel mesajına sığma
- Sadece ECIES adımlarını destekleme
- [Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde uygulanan iyileştirmeleri koruma
- Mevcut ağ ile maksimum uyumluluk
- Giden yapı yanıt mesajlarını IBGW'den gizleme
- Ağın tamamının "flag day" yükseltmesi gerektirmeme
- Riski en aza indirmek için kademeli uygulama
- Mevcut kriptografik ilkeleri yeniden kullanma

### Hedef Olmayanlar

Ek hedef olmayanlar için [Prop156](/proposals/156-ecies-routers/) belgesine bakınız.

- Karışık ElGamal/ECIES tünelleri gerektirmemek
- Katman şifreleme değişiklikleri, bunun için [Prop153](/proposals/153-chacha20-layer-encryption/) belgesine bakınız
- Kripto operasyonlarının hızlandırılmaması. ChaCha20 ve AES'in benzer olduğu varsayılmakta,
  en azından söz konusu küçük veri boyutları için, hatta AESNI ile bile.

## Tasarım

### Kayıtlar

Hesaplamalar için ek bölüme bakınız.

Şifreli istek ve yanıt kayıtları 218 bayt olacaktır, şu anki 528 bayta kıyasla.

Düz metin istek kayıtları 154 bayt olacaktır,
ElGamal kayıtları için şu anki 222 bayt ve
[Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde tanımlanan ECIES kayıtları için 464 bayta kıyasla.

Düz metin yanıt kayıtları 202 bayt olacaktır,
ElGamal kayıtları için şu anki 496 bayt ve
[Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde tanımlanan ECIES kayıtları için 512 bayta kıyasla.

Yanıt şifrelemesi ChaCha20 olacaktır (ChaCha20/Poly1305 DEĞİL),
dolayısıyla düz metin kayıtlarının 16 bayt çokluğunda olmasına gerek yoktur.

İstek kayıtları, katman ve yanıt anahtarlarını oluşturmak için HKDF kullanılarak daha küçük hale getirilecektir,
bu nedenle açıkça isteğe dahil edilmeleri gerekmemektedir.

### Tünel Yapı Mesajları

Her ikisi de mevcut Değişken mesajlarla aynı bir baytlık kayıt sayısı alanına sahip "değişken" olacaktır.

#### ShortTunnelBuild: Tür 25

Tipik uzunluk (4 kayıt ile): 873 bayt

Giden tünel yapıları için kullanıldığında,
bu mesajın orijinatör tarafından sarımsaklanması önerilir (ama gerekli değildir),
giden geçide (teslimat talimatları YÖNLENDİRİCİ) hedeflenerek,
giden yapı mesajlarını OBEP'den gizlemek için.
IBGW mesajı şifre çözer,
yanıtı doğru slota koyar,
ve ShortTunnelBuildMessage'ı bir sonraki adıma gönderir.

Kayıt uzunluğu, sarımsak şifrelenmiş STBM'nin
bir tünel mesajına sığması için seçilmiştir. Aşağıdaki ek bölümüne bakınız.

#### OutboundTunnelBuildReply: Tür 26

Yeni bir OutboundTunnelBuildReply mesajı tanımlıyoruz.
Bu yalnızca giden tünel yapıları için kullanılır.
Amacı, giden yapı yanıt mesajlarını IBGW'den gizlemektir.
OBEP tarafından sarımsak şifrelenmelidir, orijinatöre hedef alan
(teslimat talimatları TÜNEL).
OBEP tünel yapı mesajını şifre çözer,
bir OutboundTunnelBuildReply mesajı oluşturur
ve yanıtı açık metin alanına koyar.
Diğer kayıtlar diğer slotlara yerleştirilir.
Ardından sarımsak şifreleyerek mesajı türev simetrik anahtarlarla orijinatöre gönderir.

#### Notlar

OTBRM ve STBM'yi sarımsak şifreleyerek,
çift tünellerin IBGW ve OBEP ile uyumluluğu ile ilgili herhangi bir olası
sorunu da önleriz.

### Mesaj Akışı


```
STBM: Kısa tünel yapı mesajı (tür 25)
  OTBRM: Giden tünel yapı yanıt mesajı (tür 26)

  A-B-C Giden Yapı
  D-E-F üzerinden Yanıt

                  Yeni Tünel
           STBM      STBM      STBM
  Oluşturucu ------> A ------> B ------> C ---\
                                     OBEP   \
                                            | Sarımsaklanmış
                                            | OTBRM
                                            | (TÜNEL teslimatı)
                                            | OBEP'ten
                                            | oluşturucuya
                Mevcut Tünel             /
  Oluşturucu <-------F---------E-------- D <--/
                                     IBGW

  D-E-F Giden Yapı
  A-B-C üzerinden Gönderildi

                Mevcut Tünel
  Oluşturucu ------> A ------> B ------> C ---\
                                    OBEP    \
                                            | Sarımsaklanmış (isteğe bağlı)
                                            | STBM
                                            | (ROUTER teslimatı)
                                            | oluşturucudan
                  Yeni Tünel                | IBGW'ye
            STBM      STBM      STBM        /
  Oluşturucu <------ F <------ E <------ D <--/
                                     IBGW

```

### Kayıt Şifreleme

İstek ve yanıt kayıt şifrelemesi: [Prop152](/proposals/152-ecies-tunnels/) ve [Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) belgelerinde tanımlandığı gibi.

Diğer slotlar için yanıt kayıt şifrelemesi: ChaCha20.

### Katman Şifreleme

Şu anda, bu spesifikasyonla oluşturulan tüneller için katman şifreleme değişikliği planlanmamaktadır; tüm tüneller için şu anda kullanılan AES olarak kalacaktır.

Katman şifrelemesinin ChaCha20'ye değiştirilmesi ek araştırmalar için bir konudur.

### Yeni Tünel Veri Mesajı

Şu anda, bu spesifikasyonla oluşturulan tüneller için kullanılan 1KB Tünel Veri Mesajını değiştirme planı yoktur.

Bu tüneller üzerinden kullanmak için daha büyük veya değişken boyutlu yeni bir I2NP mesajı tanıtmak bu öneriyle birlikte yararlı olabilir.
Bu, büyük mesajlar için ek yükü azaltacaktır.
Bu ek araştırmalar için bir konudur.

## Spesifikasyon

### Kısa İstek Kaydı

#### Kısa İstek Kaydı Şifre Değiştirilmemiş

Bu, ECIES-X25519 yönlendiricileri için tünel BuildRequestRecord'un önerilen spesifikasyonudur.
[Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) 'dan değişikliklerin özeti:

- Şifrelenmemiş uzunluğu 464'ten 154 bayta değiştir
- Şifrelenmiş uzunluğu 528'den 218 bayta değiştir
- Katman ve yanıt anahtarlarını ve IV'leri kaldır, bunlar split() ve bir KDF'den oluşturulacak

İstek kaydı herhangi bir ChaCha yanıt anahtarı içermez.
Bu anahtarlar bir KDF'den türetilir. Aşağıya bakınız.

Tüm alanlar büyük-endian'dır.

Şifrelenmemiş boyut: 154 bayt.


```
bytes     0-3: mesajları almak için tünel kimliği, sıfır olmayan
  bytes     4-7: bir sonraki tünel kimliği, sıfır olmayan
  bytes    8-39: bir sonraki yönlendirici kimlik karma değeri
  byte       40: bayraklar
  bytes   41-42: daha fazla bayrak, kullanılmayan, uyumluluk için 0 olarak ayarlanır
  byte       43: katman şifreleme türü
  bytes   44-47: istek zamanı (epoktan itibaren dakikalar olarak, aşağı yuvarlanır)
  bytes   48-51: istek süresi (oluşturulmadan itibaren saniye olarak)
  bytes   52-55: bir sonraki mesaj kimliği
  bytes    56-x: tünel yapı seçenekleri (Haritalama)
  bytes     x-x: bayraklar veya seçenekler tarafından belirtilen diğer veriler
  bytes   x-153: rastgele dolgu (aşağıya bakınız)

```

Bayraklar alanı [Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) 'da tanımlandığı gibi ve aşağıdakileri içerir::

 Bit sırası: 76543210 (bayt 7 MSB'dir)
 bit 7: ayarlanırsa, herkesten mesajlara izin ver
 bit 6: ayarlanırsa, herkese mesaj gönder ve yanıtı
        belirtilen bir sonraki adıma bir Tünel Yapı Yanıt Mesajı'nda gönder
 bitler 5-0: Tanımlanmadı, gelecekteki seçeneklerle
             uyumluluk için 0 olarak ayarlanmalıdır

Bit 7, hop'un bir girişi ağ geçidi (IBGW) olacağını belirtir. Bit 6
hop'un bir çıkış uç noktası (OBEP) olacağını belirtir. İki bit de
birlikte ayarlanamaz.

Katman şifreleme türü: AES için 0 (mevcut tünellerde olduğu gibi);
Gelecek kullanımda 1 (ChaCha?)

İstek süresi, gelecekteki değişken tünel süresi içindir.
Şu anda, desteklenen tek değer 600'dür (10 dakika).

oluşturucu geçici genel anahtarı bir ECIES anahtarıdır, büyük-endian.
Bu, IBGW katman ve yanıt anahtarları ve IV'leri için bir KDF için kullanılır.
Bu yalnızca gelen bir Tünel Yapı mesajında düz metin kaydında bulunur.
Bu gereklidir çünkü bu katmanda bir DH için yapı kaydı yoktur.

tünel yapı seçenekleri, [Common](/docs/specs/common-structures/) 'da tanımlandığı gibi bir Haritalama yapısıdır.
Bu, gelecekteki kullanım içindir. Şu anda tanımlanmış seçenek yoktur.
Haritalama yapısı boşsa, bu iki bayttır 0x00 0x00.
Haritalamanın maksimum boyutu (uzunluk alanı dahil) 98 bayttır,
ve Haritalama uzunluk alanının maksimum değeri 96'dır.

#### Kısa İstek Kaydı Şifrelenmiş

Tüm alanlar büyük-endian'dır, geçici genel anahtar hariç, o küçük-endian'dır.

Şifrelenmiş boyut: 218 bayt


```
bytes    0-15: Hop'un kesilmiş kimlik karma değeri
  bytes   16-47: Gönderenin geçici X25519 genel anahtarı
  bytes  48-201: ChaCha20 ile şifrelenmiş Kısa Yapı İstek Kaydı
  bytes 202-217: Poly1305 MAC

```

### Kısa Yanıt Kaydı

#### Kısa Yanıt Kaydı Şifre Değiştirilmemiş

Bu, ECIES-X25519 yönlendiricileri için tünel Kısa Yapı Yanıt Kaydı'nın önerilen spesifikasyonudur.
[Tunnel-Creation-ECIES](/docs/specs/implementation/#tunnel-creation-ecies) 'dan değişikliklerin özeti:

- Şifrelenmemiş uzunluğu 512'den 202 bayta değiştir
- Şifrelenmiş uzunluğu 528'den 218 bayta değiştir

ECIES yanıtları ChaCha20/Poly1305 ile şifrelenmiştir.

Tüm alanlar büyük-endian'dır.

Şifrelenmemiş boyut: 202 bayt.


```
bytes    0-x: Tünel Yapı Yanıt Seçenekleri (Haritalama)
  bytes    x-x: seçenekler tarafından belirtilen diğer veriler
  bytes  x-200: Rastgele dolgu (aşağıya bakınız)
  byte     201: Yanıt bayt

```

Tünel yapı yanıt seçenekleri [Common](/docs/specs/common-structures/) 'da tanımlandığı gibi bir Haritalama yapısıdır.
Bu, gelecekteki kullanım içindir. Şu anda tanımlanmış seçenek yoktur.
Haritalama yapısı boşsa, bu iki bayttır 0x00 0x00.
Haritalamanın maksimum boyutu (uzunluk alanı dahil) 201 bayttır,
ve Haritalama uzunluk alanının maksimum değeri 199'dur.

Yanıt baytı aşağıdaki değerlerden biridir
[Tunnel-Creation](/docs/specs/implementation/#tunnel-creation-ecies) 'da tanımlandığı gibi parmak izi bırakmamak için:

- 0x00 (kabul)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Kısa Yanıt Kaydı Şifrelenmiş

Şifrelenmiş boyut: 218 bayt


```
bytes   0-201: ChaCha20 ile şifrelenmiş Kısa Yapı Yanıt Kaydı
  bytes 202-217: Poly1305 MAC

```

### KDF

Aşağıdaki KDF bölümüne bakınız.


### ShortTunnelBuild
I2NP Tür 25

Bu mesaj orta adımlara, OBEP'ye ve IBEP'ye (oluşturucu) gönderilir.
IBGW'ye gönderilemez (sarımsak kaplı Gelen Tünel Yapı'yı kullanın).
OBEP tarafından alındığında, OutboundTunnelBuildReply'a dönüştürülür,
sarımsak sarılır ve oluşturucuya gönderilir.


```
+----+----+----+----+----+----+----+----+
  | num| ShortBuildRequestRecords...
  +----+----+----+----+----+----+----+----+

  num ::
         1 bayt `Tamsayı`
         Geçerli değerler: 1-8

  kayıt boyutu: 218 bayt
  toplam boyut: 1+$num*218
```

#### Notlar

* Tipik kayıt sayısı 4'tür, toplam boyut 873.


### OutboundTunnelBuildReply
I2NP Tür 26

Bu mesaj yalnızca OBEP tarafından bir mevcut gelen tünel üzerinden IBEP'ye (oluşturucu) gönderilir.
Başka hiçbir adıma gönderilemez.
Her zaman sarımsak şifrelenmiştir.


```
+----+----+----+----+----+----+----+----+
  | num|                                  |
  +----+                                  +
  |      ShortBuildReplyRecords...        |
  +----+----+----+----+----+----+----+----+

  num ::
         Total number of records,
         1 bayt `Tamsayı`
         Geçerli değerler: 1-8

  ShortBuildReplyRecords ::
         Şifreli kayıtlar
         length: num * 218

  şifreli kayıt boyutu: 218 bayt
  toplam boyut: 1+$num*218
```

#### Notlar

* Tipik kayıt sayısı 4'tür, toplam boyut 873.
* Bu mesaj sarımsakla şifrelenmelidir.

### KDF

Tünel yapı kaydı şifreleme/şifre çözme sonrası Gürültü durumundan ck'yi kullanarak aşağıdaki anahtarları türetiriz: yanıt anahtarı, AES katman anahtarı, AES IV anahtarı ve OBEP için sarımsak yanıt anahtarı/etiketi.

Yanıt anahtarı:
Uzun kayıtlardan farklı olarak, yanıt anahtarı için ck'nin sol tarafını kullanamayız çünkü bu son değil ve daha sonra kullanılacak.
Yanıt anahtarı, AEAD/Chaha20/Poly1305 kullanarak yanıt kaydını şifrelemek ve Chacha20 ile diğer kayıtları yanıtlarken kullanılır.
Her ikisi de aynı anahtarı kullanır, nonce mesajdaki kaydın pozisyonudur, 0'dan başlayarak.


```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
  replyKey = keydata[32:63]
  ck = keydata[0:31]

  Katman anahtarı:
  Katman anahtarı şimdilik her zaman AES'dir, ancak aynı KDF Chacha20'den de kullanılabilir.

  keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
  layerKey = keydata[32:63]

  OBEP kaydı olmayan IV anahtarı:
  ivKey = keydata[0:31]
  çünkü bu, son olacak

  OBEP kaydı için IV anahtarı:
  ck = keydata[0:31]
  keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
  ivKey = keydata[32:63]
  ck = keydata[0:31]

  OBEP sarımsak yanıt anahtarı/etiketi:
  keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
  replyKey = keydata[32:63]
  replyTag = keydata[0:7]

```

## Gerekçe

Bu tasarım mevcut kriptografik ilkelere, protokollere ve koda tekrar kullanımı en üst düzeye çıkarır.

Bu tasarım riski en aza indirir.

ChaCha20, Java testlerinde küçük kayıtlar için AES'den biraz daha hızlıdır.
ChaCha20, verilerin boyutları 16'nın katı olmasını gerektirmez.

## Uygulama Notları

- Mevcut değişken tünel yapı mesajı ile olduğu gibi,
  4 kayıt kadar küçük mesajlar önerilmez.
  Tipik varsayılan 3 adımdır.
  Giren tüneller, son adımın son olduğunu bilmemesi için
  bir fazla kayıtla oluşturulmalıdır.
  Böylece orta adımlar bir tünelin giren mi yoksa çıkan mı olduğunu bilmesin,
  çıkan tüneller de 4 kayıtla oluşturulmalıdır.

## Sorunlar

## Geçiş

Uygulama, test etme ve kullanıma alma birkaç sürüm alacak
ve yaklaşık bir yıl sürecek. Aşamalar aşağıdaki gibidir.
Her bir aşamanın belirli bir sürüme atanması henüz belirlenmemiştir
ve gelişim hızına bağlıdır.

Her I2P uygulaması için uygulama ve geçişin ayrıntıları
değişebilir.

Tünel oluşturucu, oluşturulan tüneldeki tüm adımların ECIES-X25519 olduğundan, VE en az TBD sürümüne sahip olduğundan emin olmalıdır.
Tünel oluşturucu ECIES-X25519 olmak zorunda değildir; ElGamal olabilir.
Ancak, oluşturucu ElGamal ise, en yakın hop'a oluşturucu olduğunu belirtir.
Bu nedenle, pratikte, bu tüneller yalnızca ECIES yönlendiriciler tarafından oluşturulmalıdır.

Paired tünelin OBEP veya IBGW'si ECIES veya
herhangi bir özel sürümde olmak zorunda OLMAMALIDIR.
Yeni mesajlar sarımsakla kaplanır ve paired tünelin OBEP veya IBGW'sinde görülmez.

Aşama 1: Uygulama, varsayılan olarak etkin değil

Aşama 2 (bir sonraki sürüm): Varsayılan olarak etkinleştirilmiş

Geriye dönük uyumluluk sorunları yoktur. Yeni mesajlar yalnızca bunları destekleyen yönlendiricilere gönderilebilir.

## Ek

Şifrelenmemiş giden STBM için sarımsak yükü olmadan, ITBM kullanmazsak:


```
Mevcut 4-slot boyut: 4 * 528 + ek yük = 3 tünel mesajı

  4-slot yapım mesajı bir tünel mesajına sığacak şekilde, yalnızca ECIES:

  1024
  - 21 parça başlığı
  ----
  1003
  - 35 parçalanmamış YÖNLENDİRİCİ teslimat talimatı
  ----
  968
  - 16 I2NP başlığı
  ----
  952
  - 1 slot sayısı
  ----
  951
  / 4 slot
  ----
  237 Yeni şifreli yapı kaydı boyutu (şu anki 528'e kıyasla)
  - 16 kesilmiş hash
  - 32 geçici anahtar
  - 16 MAC
  ----
  173 açık metin yapı kaydı maksimum (şu anki 222'ye kıyasla)

```

ITBM kullanmazsak, gelen STBM için sarımsak yükü ile:


```
Mevcut 4-slot boyut: 4 * 528 + ek yük = 3 tünel mesajı

  4-slot sarımsak şifrelenmiş yapı mesajı bir tünel mesajına sığacak şekilde, yalnızca ECIES:

  1024
  - 21 parça başlığı
  ----
  1003
  - 35 parçalanmamış YÖNLENDİRİCİ teslimat talimatı
  ----
  968
  - 16 I2NP başlığı
  -  4 uzunluk
  ----
  948
  - 32 bayt geçici anahtar
  ----
  916
  - 7 bayt Tarih ve Saat bloğu
  ----
  909
  - 3 bayt Sarımsak bloğu ek yükü
  ----
  906
  - 9 bayt I2NP başlığı
  ----
  897
  - 1 bayt Sarımsak YEREL teslimat talimatı
  ----
  896
  - 16 bayt Poly1305 MAC
  ----
  880
  - 1 slot sayısı
  ----
  879
  / 4 slot
  ----
  219 Yeni şifreli yapı kaydı boyutu (şu anki 528'e kıyasla)
  - 16 kesilmiş hash
  - 32 geçici anahtar
  - 16 MAC
  ----
  155 açık metin yapı kaydı maksimum (şu anki 222'ye kıyasla)

```

Notlar:

Kullanılmayan dolgu öncesi mevcut yapı kaydı açık metin boyutu: 193

Tam yönlendirici karma değerinin kaldırılması ve anahtar/IV'lerin HKDF tarafından oluşturulması,
gelecekteki seçenekler için bolca alan açacaktır.
Her şey HKDF ise, gerekli açık metin alanı yaklaşık 58 bayt (herhangi bir seçenek olmadan).

Sarımsak sarılı OTBRM, sarımsak sarılı STBM'den biraz daha küçük olacaktır,
çünkü teslimat talimatları YEREL'dir, YÖNLENDİRİCİ değil,
herhangi bir TARİH ve SAAT bloğu dahil edilmez ve
bir 'N' mesajının tam kapsamlı geçici anahtarı yerine 8 bayt etiket kullanır.


