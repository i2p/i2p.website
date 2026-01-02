---
title: "ECIES Hedeflerinden Veri Tabanı Aramaları"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Kapalı"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Not
ECIES'den ElG'ye uygulamaları 0.9.46'da gerçekleştirildi ve teklif aşaması kapandı.
Resmi spesifikasyon için [I2NP](/docs/specs/i2np/)'ye bakın.
Bu teklif, arka plan bilgileri için hala referans alınabilir.
Anahtarlar dahil ECIES'den ECIES'ye uygulama 0.9.48 itibarıyla gerçekleştirilmiştir.
Temel alınan anahtarlarla ECIES'den ECIES'ye bölümü yeniden açılabilir veya gelecekteki bir teklife dahil edilebilir.

## Genel Bakış

### Tanımlar

- AEAD: ChaCha20/Poly1305
- DLM: I2NP Veri Tabanı Arama Mesajı
- DSM: I2NP Veri Tabanı Depolama Mesajı
- DSRM: I2NP Veri Tabanı Arama Cevabı Mesajı
- ECIES: ECIES-X25519-AEAD-Ratchet (öneri 144)
- ElG: ElGamal
- ENCRYPT(k, n, payload, ad): [ECIES](/docs/specs/ecies/)'de tanımlandığı gibi
- LS: Kira seti
- lookup: I2NP DLM
- reply: I2NP DSM veya DSRM

### Özet

Bir LS için bir floodfill'e DLM gönderirken, DLM genellikle cevabın etiketlenmesi, AES ile şifrelenmesi ve tünel boyunca hedefe gönderilmesi gerektiğini belirtir.
AES ile şifrelenmiş cevaplar desteği 0.9.7'de eklendi.

AES ile şifrelenen cevaplar, ElG'nin büyük kripto yükünü en aza indirmek için 0.9.7'de belirtildi ve çünkü etiketler/AES tesisini ElGamal/AES+SessionTags'te yeniden kullandığı için.
Ancak, IBEP'de kimlik doğrulaması olmadığından, AES cevapları kaldırılabilir ve ileriye dönük olarak gizli değildir.

[ECIES](/docs/specs/ecies/) hedefleri ile, öneri 144'ün amacı, artık 32 bayt etiketleri ve AES şifre çözmeyi desteklememeleridir.
Özellikler o teklifte kasıtlı olarak dahil edilmedi.

Bu teklif, DLM'de ECIES şifreli cevapları talep etmek için yeni bir seçeneği belgeler.

### Amaçlar

- Şifrelenmiş bir cevabın bir tünel üzerinden bir ECIES hedefine talep edildiğinde, DLM için yeni bayraklar
- Cevap için, müracaat edenin (hedefin) anahtarının bozulması kimliğine bürünmeye karşı ileriye dönük gizlilik ve gönderen kimlik doğrulaması ekleyin.
- İstek sahibinin anonim olarak kalmasını sağlamak
- Kripto yükünü en aza indirmek

### Amaçlar Dışında

- Aramanın (DLM) şifreleme veya güvenlik özelliklerinde değişiklik yok.
  Arama, yalnızca isteyen anahtarının bozulması için ileriye dönük gizliliğe sahiptir.
  Şifreleme floodfill'in statik anahtarına yapılır.
- Yanıt verenin (floodfill'in) anahtarının bozulmasına karşı ileriye dönük gizlilik veya gönderen kimlik doğrulama sorunları yok.
  Floodfill, herkesten gelen aramalara yanıt verecek bir genel veri tabanıdır.
- Bu teklifte ECIES routerları tasarlamayın.
  Bir router'ın X25519 genel anahtarının nereye gideceği TBD.

## Alternatifler

ECIES hedeflerine cevapları şifrelemek için tanımlanmış bir yolun yokluğunda, birkaç alternatif vardır:

1) Şifrelenmiş cevapları talep etmeyin. Cevaplar şifresiz olacaktır.
Java I2P şu anda bu yaklaşımı kullanıyor.

2) Yalnızca ECIES hedefleri için 32 bayt etiket ve AES ile şifrelenmiş cevapları desteklemeye ekleyin ve her zamanki gibi AES ile şifrelenmiş cevapları isteyin. i2pd şu anda bu yaklaşımı kullanıyor.

3) Her zamanki gibi AES ile şifrelenmiş cevapları isteyin, ancak cevapları router'a keşif tünellerinden geri yönlendirin.
Java I2P şu anda bazı durumlarda bu yaklaşımı kullanıyor.

4) İkili ElG ve ECIES hedefleri için her zamanki gibi AES ile şifrelenmiş cevapları isteyin. Java I2P şu anda bu yaklaşımı kullanıyor.
i2pd henüz çift kripto hedeflerini uygulamadı.

## Tasarım

- Yeni DLM formatı, ECIES ile şifrelenmiş cevapları belirtmek için bayraklar alanına bir bit ekleyecektir.
  ECIES ile şifrelenmiş cevaplar, ekli bir etiket ve bir ChaCha/Poly yükü ve MAC ile [ECIES](/docs/specs/ecies/) Mevcut Oturum mesajı formatını kullanacaktır.

- İki varyant tanımlayın. Bir DH işleminin mümkün olmadığı ElG routerları için bir tane ve DH işleminin mümkün olduğu ve ek güvenlik sağlayabilecek gelecek ECIES routerları için bir tane. Daha fazla inceleme için.

DH, ElG routerlarından cevaplar için mümkün değildir çünkü X25519 genel anahtarı yayınlanmaz.

## Spesifikasyon

[I2NP](/docs/specs/i2np/) DLM (Veri Tabanı Arama) spesifikasyonunda, aşağıdaki değişiklikleri yapın.

Yeni şifreleme seçenekleri için bayrak biti 4 "ECIESFlag" ekleyin.

```text
flags ::
       bit 4: ECIESFlag
               0.9.46 sürümünden önce göz ardı edilir
               0.9.46 sürümünden itibaren:
               0  => şifresiz veya ElGamal cevabı gönder
               1  => ekli anahtarla ChaCha/Poly şifrelenmiş cevap gönder
                     (etiket ekli olup olmadığı bit 1'e bağlıdır)
```

Bayrak biti 4, cevap şifreleme modunu belirlemek için bit 1 ile birlikte kullanılır.
Bayrak biti 4 yalnızca 0.9.46 veya daha yüksek sürümdeki routerlara gönderilirken ayarlanmalıdır.

Aşağıdaki tabloda, 
"DH n/a" cevabın şifrelenmediği anlamına gelir. 
"DH no" cevabın anahtarlarının istekte dahil edildiği anlamına gelir.
"DH yes" cevabın anahtarlarının DH işlemi ile türetildiği anlamına gelir.

| Bayrak bitleri 4,1 | From Dest | To Router | Reply | DH? | notes |
|-------------------|-----------|-----------|-------|-----|-------|
| 0 0                | Any       | Any       | no enc| n/a | mevcut |
| 0 1                | ElG       | ElG       | AES   | no  | mevcut |
| 0 1                | ECIES     | ElG       | AES   | no  | i2pd geçici çözümü |
| 1 0                | ECIES     | ElG       | AEAD  | no  | bu teklif |
| 1 0                | ECIES     | ECIES     | AEAD  | no  | 0.9.49 |
| 1 1                | ECIES     | ECIES     | AEAD  | yes | gelecek |

### ElG’den ElG’ye

ElG hedefi bir ElG routera bir arama gönderir.

Yeni bit 4 için kontrol yapılması için küçük değişiklikler. Mevcut ikili formatta değişiklik yok.

İsteyen anahtar üretimi (açıklama):

```text
reply_key :: CSRNG(32) 32 bayt rastgele veri
  reply_tags :: Her biri CSRNG(32) 32 bayt rastgele veridir
```

Mesaj formatı (ECIESFlag için kontrol ekle):

```text
reply_key ::
       32 bayt `OturumAnahtarı` big-endian
       yalnızca encryptionFlag == 1 VE ECIESFlag == 0 ise dahil edilir, yalnızca 0.9.7 sürümünden itibaren

  tags ::
       1 bayt `Tamsayı`
       geçerli aralık: 1-32 (genellikle 1)
       ardından gelen cevap etiketlerinin sayısı
       yalnızca encryptionFlag == 1 VE ECIESFlag == 0 ise dahil edilir, yalnızca 0.9.7 sürümünden itibaren

  reply_tags ::
       bir veya daha fazla 32 bayt `OturumTag`'i (genellikle bir)
       yalnızca encryptionFlag == 1 VE ECIESFlag == 0 ise dahil edilir, yalnızca 0.9.7 sürümünden itibaren
```

### ECIES’den ElG’ye

ECIES hedefi bir ElG routera bir arama gönderir.
0.9.46 itibarıyla desteklenir.

reply_key ve reply_tags alanları, bir ECIES ile şifrelenmiş cevap için yeniden tanımlanır.

İsteyen anahtar üretimi:

```text
reply_key :: CSRNG(32) 32 bayt rastgele veri
  reply_tags :: Her biri CSRNG(8) 8 bayt rastgele veri
```

Mesaj formatı:
reply_key ve reply_tags alanlarını aşağıdaki şekilde yeniden tanımlayın:

```text
reply_key ::
       32 bayt ECIES `OturumAnahtarı` big-endian
       yalnızca encryptionFlag == 0 VE ECIESFlag == 1 ise dahil edilir, yalnızca 0.9.46 sürümünden itibaren

  tags ::
       1 bayt `Tamsayı`
       gerekli değer: 1
       ardından gelen cevap etiketlerinin sayısı
       yalnızca encryptionFlag == 0 VE ECIESFlag == 1 ise dahil edilir, yalnızca 0.9.46 sürümünden itibaren

  reply_tags ::
       bir 8 bayt ECIES `OturumTag`
       yalnızca encryptionFlag == 0 VE ECIESFlag == 1 ise dahil edilir, yalnızca 0.9.46 sürümünden itibaren
```

Cevap, [ECIES](/docs/specs/ecies/)'de tanımlandığı gibi bir ECIES Mevcut Oturum mesajıdır.

```text
tag :: 8 bayt reply_tag

  k :: 32 bayt oturum anahtarı
     Cevabın anahtarı.

  n :: 0

  ad :: 8 bayt reply_tag

  payload :: Düz metin veriler, DSM veya DSRM.

  şifreli metin = ENCRYPT(k, n, payload, ad)
```

### ECIES’den ECIES’ye (0.9.49)

ECIES hedefi veya routerı, bir ECIES routerına eklenmiş cevap anahtarlarıyla bir arama gönderir.
0.9.49 itibarıyla desteklenir.

ECIES routerları 0.9.48'de tanıtıldı, bkz. [Prop156](/proposals/156-ecies-routers/).
0.9.49 itibarıyla, ECIES hedefleri ve routerlar "ECIES’den ElG’ye" bölümündeki ile aynı formatı kullanabilir, istek içinde cevap anahtarları dahil edilmiştir.
Arama, talep sahibinin anonim olduğu için [ECIES](/docs/specs/ecies/)'deki "tek seferlik format"ı kullanacaktır.

Yeni bir yöntemle türetilen anahtarlar için, bir sonraki bölüme bakın.

### ECIES’den ECIES’ye (gelecek)

ECIES hedefi veya routerı, bir ECIES routerına bir arama gönderir ve cevap anahtarları DH'den türetilir.
Tam olarak tanımlanmamış veya desteklenmiyor, uygulama TBD.

Arama, talep sahibinin anonim olduğu için [ECIES](/docs/specs/ecies/)'deki "tek seferlik format"ı kullanacaktır.

reply_key alanını aşağıdaki gibi yeniden tanımlayın. Bağlı etiketler yok.
Aşağıdaki KDF'de etiketler oluşturulacaktır.

Bu bölüm tamamlanmamış ve daha fazla çalışma gerektirir.

```text
reply_key ::
       32 bayt X25519 ephemeral `GenelAnahtar` istek sahibine ait, little-endian
       yalnızca encryptionFlag == 1 VE ECIESFlag == 1 ise dahil edilir, yalnızca 0.9.TBD sürümünden itibaren
```

Cevap, [ECIES](/docs/specs/ecies/) üzerinde tanımlanmış bir ECIES Mevcut Oturum mesajıdır.
Tüm tanımlar için [ECIES](/docs/specs/ecies/)'e bakın.

```text
// Alice'in X25519 geçici anahtarları
  // aesk = Alice geçici özel anahtarı
  aesk = GENERATE_PRIVATE()
  // aepk = Alice geçici genel anahtarı
  aepk = DERIVE_PUBLIC(aesk)
  // Bob'un X25519 statik anahtarları
  // bsk = Bob özel statik anahtarı
  bsk = GENERATE_PRIVATE()
  // bpk = Bob genel statik anahtarı
  // bpk RouterIdentity'nin bir parçası olabilir veya RouterInfo'da yayınlanabilir (TBD)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey nereden ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = Payload Bölümünden chainKey
  2) k, Yeni Oturum KDF'den veya split()'ten

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Çıktı 1: kullanılmamış
  unused = keydata[0:31]
  // Çıktı 2: Alice'den Bob'a iletimler için yeni oturum etiketi ve simetrik anahtar rachetleri
  // başlatmak için zincir anahtar
  ck = keydata[32:63]

  // oturum etiketi ve simetrik anahtar zincir anahtarları
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: [ECIES](/docs/specs/ecies/)'deki RATCHET_TAG() tarafından üretilen 8 bayt etiket

  k :: [ECIES](/docs/specs/ecies/)'deki RATCHET_KEY() tarafından üretilen 32 bayt anahtar

  n :: Etiketin dizini. Genellikle 0.

  ad :: 8 bayt etiket

  payload :: Düz metin veriler, DSM veya DSRM.

  şifreli metin = ENCRYPT(k, n, payload, ad)
```

### Cevap formatı

Bu mevcut oturum mesajıdır,
[I2NP](/docs/specs/i2np/) içinde tanımlandığı gibi, aşağıda referans için kopyalanmıştır.

```text
+----+----+----+----+----+----+----+----+
  |       Oturum Etiketi                    |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Yük Bölümü                +
  |       ChaCha20 şifreli veri          |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Mesaj Doğrulama Kodu       |
  +              (MAC)                    +
  |             16 bayt                  |
  +----+----+----+----+----+----+----+----+

  Oturum Etiketi :: 8 bayt, açık metin

  Yük Bölümü şifreli veri :: kalan veri eksi 16 bayt

  MAC :: Poly1305 mesaj doğrulama kodu, 16 bayt
```

## Gerekçe

Cevap şifreleme parametreleri önce 0.9.7'de arama içinde tanıtıldı ve bunlar biraz katman ihlali gibi. Verimlilik için bu şekilde yapılır.
Ama aynı zamanda aramanın anonim olmasından dolayı.

Arama formatını şifreleme türü alanıyla genel yapabiliriz ama bu muhtemelen yapmaya değerinden fazla sorun yaratır.

Yukarıdaki öneri en kolay olanı ve arama formatındaki değişiklikleri en aza indirir.

## Notlar

ElG routerlarına yapılan veri tabanı aramaları ve depolamaları alışıldığı gibi ElGamal/AESSessionTag ile şifrelenmelidir.

## Sorunlar

İki ECIES cevap seçeneğinin güvenliği üzerinde daha fazla analiz gereklidir.

## Geçiş

Geriye dönük uyumluluk sorunları yok. Routerları, RouterInfo'da bir router.version'u 0.9.46 veya daha yeni olarak reklam ederse, bu özelliği desteklemek zorundadır.
Routerlar, 0.9.46'dan düşük bir sürüme sahip routerlara yeni bayraklarla bir DatabaseLookup göndermemelidir.
Yanlışlıkla ayarlanmamış bit 1 ve ayarlanmış bit 4 ile bir veri tabanı arama mesajı desteklenmeyen bir routera gönderilirse,
sağlanan anahtar ve etiketi muhtemelen göz ardı edecek ve cevabı şifresiz olarak gönderecektir.
