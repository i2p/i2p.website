---
title: "ChaCha Tünel Katmanı Şifrelemesi"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Open"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Özet

Bu öneri, öneri 152'den türetilir ve onun değişikliklerini gerektirir: ECIES Tünelleri.

Sadece ECIES-X25519 tünelleri için BuildRequestRecord formatını destekleyen geçişler aracılığıyla oluşturulan tüneller bu spesifikasyonu uygulayabilir.

Bu spesifikasyon, tünel katmanı şifreleme türünü belirtmek ve katman AEAD anahtarlarını iletmek için Tünel Oluşturma Seçenekleri formatını gerektirir.

### Hedefler

Bu önerinin hedefleri şunlardır:

- Kurulmuş tünel IV ve katmanı şifreleme için AES256/ECB+CBC'nin yerine ChaCha20'yi kullanmak
- Ara-hop AEAD koruması için ChaCha20-Poly1305'i kullanmak
- Mevcut tünel katmanı şifrelemesinden tünel dışı katılımcılar tarafından fark edilemez olmak
- Genel tünel mesajı uzunluğunda değişiklik yapmamak

### Kurulmuş Tünel Mesajı İşleme

Bu bölümde şunlardaki değişiklikler anlatılmaktadır:

- Giden ve Gelen Ağ Geçidi ön işleme + şifreleme
- Katılımcı şifreleme + son işleme
- Giden ve Gelen Uç Nokta şifreleme + son işleme

Geçerli tünel mesajı işleme hakkında genel bilgi için, [Tunnel Implementation](/docs/specs/implementation/) spesifikasyonuna bakınız.

Sadece ChaCha20 katman şifrelemesini destekleyen yönlendiriciler için değişiklikler tartışılmaktadır.

AES katman şifrelemesiyle karışık tünel için hiçbir değişiklik düşünülmemektedir, bir 128-bit AES IV'yi 64-bit ChaCha20 nonce'ına güvenli bir şekilde dönüştürmek için bir protokol geliştirilene kadar. Tam IV'nin benzersizliği için Bloom filtreleri garanti eder, ancak benzersiz IV'lerin ilk yarısı aynı olabilir.

Bu, tüneldeki tüm geçişler için katman şifrelemesinin uniform olması gerektiği ve tünel oluşturma sürecinde tünel oluşturma seçenekleri kullanılarak kurulması gerektiği anlamına gelir.

Tüm ağ geçitleri ve tünel katılımcılarının iki bağımsız nonce'ı doğrulamak için bir Bloom filtresi sürdürmesi gerekecektir.

Bu öneri boyunca bahsedilen ``nonceKey`` , AES katman şifrelemede kullanılan ``IVKey`` yerine geçmektedir.
152 numaralı öneriden aynı KDF kullanılarak üretilmiştir.

### Hop-to-Hop Mesajlarının AEAD Şifrelemesi

Her ardışık geçiş çifti için ek bir benzersiz ``AEADKey`` üretilmesi gerekecektir.
Bu anahtar, iç ChaCha20 ile şifrelenmiş tünel mesajını ChaCha20-Poly1305 şifrelemek ve çözmek için ardışık geçişler tarafından kullanılacaktır.

Tünel mesajlarının, Poly1305 MAC'ini barındırmak için iç şifreli çerçevenin uzunluğunu 16 bayt azaltması gerekecektir.

AEAD, mesajlar üzerinde doğrudan kullanılamaz, çünkü dışa giden tüneller tarafından yinelemeli şifre çözme gereklidir.
Mevcut kullanıldığı şekilde yinelemeli şifre çözme, ancak AEAD olmadan ChaCha20 kullanılarak başarılabilir.

.. raw:: html

  {% highlight lang='dataspec' -%}
+----+----+----+----+----+----+----+----+
  |    Tünel Kimliği   |   tünelNochazı  |
  +----+----+----+----+----+----+----+----+
  | tünelNochazı devamı|    obfsNochazı  |
  +----+----+----+----+----+----+----+----+
  | obfsNochazı devamı |                 |
  +----+----+----+----+                 +
  |                                       |
  +           Şifreli Veri                +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |     Poly1305 MAC   |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  Tünel Kimliği :: `TunnelId`
         4 bayt
         bir sonraki geçişin kimliği

  tünelNochazı ::
         8 bayt
         tünel katmanı nonce'ı

  obfsNochazı ::
         8 bayt
         tünel katmanı nonce şifreleme nonce'ı

  Şifreli Veri ::
         992 bayt
         şifreli tünel mesajı

  Poly1305 MAC ::
         16 bayt

  toplam boyut: 1028 Bayt
```

İç geçişler (önceki ve sonraki geçişlerle birlikte), önceki geçişlerin AEAD katmanını çözmek ve ardından gelen geçişe AEAD katmanını şifrelemek için ``AEADKey`` 'e sahip olacaktır.

Tüm iç geçiş katılımcıları BuildRequestRecords'larında 64 ek baytlık anahtar malzemesine sahip olacaktır.

Giden Uç Nokta ve Gelen Ağ Geçidi yalnızca ek 32 baytlık anahtar verisi gerektirir, çünkü aralarında mesajları şifrelemezler.

Giden Ağ Geçidi, ilk giden geçişin ``inAEAD`` anahtarı ile aynı olan ``outAEAD`` anahtarını oluşturur.

Gelen Uç Nokta, son gelen geçişin ``outAEAD`` anahtarı ile aynı olan ``inAEAD`` anahtarını oluşturur.

İç geçişler, AEAD katmanını çözmek için kullanılmak üzere ``inAEADKey`` ve giden mesajları şifrelemek için ``outAEADKey`` alacaktır.

Bir tünelde iç geçişler OBGW, A, B, OBEP olacak örnekte:

- A'nın ``inAEADKey`` 'i OBGW'in ``outAEADKey`` 'i ile aynıdır
- B'nin ``inAEADKey`` 'i A'nın ``outAEADKey`` 'i ile aynıdır
- B'nin ``outAEADKey`` 'i OBEP'in ``inAEADKey`` 'i ile aynıdır

Anahtarlar geçiş çiftlerine özgüdür, bu yüzden OBEP'in ``inAEADKey`` 'i A'nın ``inAEADKey`` 'inden farklı olacaktır,
A'nın ``outAEADKey`` 'i B'nin ``outAEADKey`` 'inden farklı olacaktır, vb.

### Ağ Geçidi ve Tünel Yaratıcı Mesaj İşleme

Ağ Geçitleri, Poly1305 MAC için talimatlar-fragman çerçevesinden sonra yer ayırarak aynı şekilde mesajları parçalayacak ve paketleyecektir.

AEAD çerçeveleri (MAC dahil) içeren iç I2NP mesajları parçalara bölünebilir,
ancak herhangi bir düşen parça, uç noktada başarısız AEAD şifre çözme (başarısız MAC doğrulama) ile sonuçlanacaktır.

### Ağ Geçidi Ön İşleme ve Şifreleme

Tüneller ChaCha20 katman şifrelemesini desteklediğinde, ağ geçitleri mesaj seti başına iki 64-bit nonce üretecektir.

Gelen tüneller:

- IV ve tünel mesajı/m(esajl)arı ChaCha20 ile şifreleyin
- Tünellerin ömrü boyunca 8 baytlık ``tünelNonce`` ve ``obfsNonce`` kullanın
- ``tünelNonce`` şifrelemesi için 8 baytlık ``obfsNonce`` kullanın
- 2^(64 - 1) - 1 mesaj setinden önce tüneli yok edin: 2^63 - 1 = 9,223,372,036,854,775,807

  - Çakışma önlemek için nonce limiti
  - Limite ulaşılması neredeyse olanaksız, çünkü bu 10 dakikalık tüneller için ~15,372,286,728,091,294 msg/s'nin üstünde olacaktır.

- Mantıklı bir beklenen eleman sayısına (128 msg/sn, 1024 msg/sn? TBD) dayalı Bloom filtresini ayarlayın

Tünelin Gelen Ağ Geçidi (IBGW), başka bir tünelin Giden Uç Nokta (OBEP)'ından alınan mesajları işler.

Bu noktada, en dıştaki mesaj katmanı nokta-üzeri-nokta taşıma şifrelemesi kullanılarak şifrelenmiştir.
I2NP mesaj başlıkları, tünel katmanında, OBEP ve IBGW'ye görünür.
İç I2NP mesajları, uçtan uca oturum şifrelemesi kullanılarak sarılmıştır.

IBGW, mesajları uygun formatta tünel mesajları haline getirir ve aşağıda belirtildiği şekilde şifreler:

```text

// IBGW Bloom filteri için çakışma olmadığından emin olarak rastgele nonce'lar üretir
  tünelNonce = Random(len = 64-bit)
  obfsNonce = Random(len = 64-bit)
  // IBGW, tünel mesajlarının her birini tünelNonce ve layerKey ile ChaCha20 ile "şifreler"
  encMsg = ChaCha20(msg = tünel msg, nonce = tünelNonce, key = layerKey)

  // Her mesajın şifreli veri çerçevesini tünelNonce ve outAEADKey ile ChaCha20-Poly1305 şifreleyin
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tünelNonce, key = outAEADKey)
```

Tünel mesaj formatı hafifçe değiştirilecek, iki 8-baytlık nonce bir 16-bayt IV yerine kullanılacaktır.
``obfsNonce`` , tünelNonce'ın 8 baytına eklenir ve şifrelenmiş tünelNonce ve geçişin ``nonceKey`` 'i kullanılarak her geçiş tarafından şifrelenir.

Mesaj seti her geçiş için önceden çözüldükten sonra, Giden Ağ Geçidi ChaCha20-Poly1305 AEAD her tünel mesajının şifreli bölümünü ``tünelNonce`` ve ``outAEADKey`` 'i kullanarak şifreler.

Giden tüneller:

- Yinelemeli olarak tünel mesajlarını çöz
- Şifre önceden çözülmüş tünel mesajı şifreli çerçevelerini ChaCha20-Poly1305 ile şifrele
- Gelen tünellerle aynı kuralları kullan
- Gönderilen tünel mesajları seti başına rastgele nonce'lar üret

```text

// Her mesaj seti için benzersiz, rastgele nonce'lar üret
  tünelNonce = Random(len = 64-bit)
  obfsNonce = Random(len = 64-bit)

  // Her geçiş için, önceki tünelNonce'ı geçerli geçişin IV anahtarıyla ChaCha20 ile şifrele
  tünelNonce = ChaCha20(msg = önceki tünelNonce, nonce = obfsNonce, key = geçişin nonceKey)

  // Her geçiş için, tünel mesajını geçerli geçişin tünelNonce ve layerKey ile ChaCha20 ile "çöz"
  decMsg = ChaCha20(msg = tünel msg(l), nonce = tünelNonce, key = geçişin layerKey)

  // Her geçiş için, obfsNonce'ı mevcut geçişin şifreli tünelNonce ve nonceKey ile ChaCha20 ile "çöz"
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tünelNonce, key = geçişin nonceKey)

  // Geçiş işlemlerinin ardından, her tünel mesajının "çözülmüş" veri çerçevesini ilk geçişin şifreli tünelNonce ve inAEADKey ile ChaCha20-Poly1305 ile şifrele
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = ilk geçişin şifreli tünelNonce, key = ilk geçişin inAEADKey / GW outAEADKey)
```

### Katılımcı İşleme

Katılımcılar, görülen mesajları aynı şekilde, azalan Bloom filtreleri kullanarak izleyecektir.

Tünel nonce'ları, ardışık olmayan ve işbirliği yapan geçişler tarafından doğrulama saldırılarını önlemek için her bir geçiş için bir kez şifrelenmelidir.

Geçişler, önceki ve sonraki geçişler arasında doğrulama saldırılarını önlemek için alınan nonce'ı şifreleyecektir,
yani işbirliği yapan, ardışık olmayan geçişlerin aynı tünele ait olduklarını anlayabilmeleri.

Katılımcılar, alınan ``tünelNonce`` ve ``obfsNonce`` 'ı doğrulamak için bunları tek tek Bloom filtresi karşısında benzersizlik açısından kontrol edeceklerdir.

Doğrulamadan sonra katılımcı:

- ChaCha20-Poly1305 ile her tünel mesajının AEAD şifreli metnini alınan ``tünelNonce`` ve kendi ``inAEADKey`` ile çözer
- ``nonceKey`` ve alınan ``obfsNonce`` ile ``tünelNonce`` 'ı ChaCha20 ile şifreler
- Her tünel mesajının şifreli veri çerçevesini ``layerKey`` ile şifreli ``tünelNonce`` ve kendi ``layerKey`` ile ChaCha20 ile şifreler
- Her tünel mesajının şifreli veri çerçevesini şifreli ``tünelNonce`` ve kendi ``outAEADKey`` ile ChaCha20-Poly1305 ile şifreler 
- ``nonceKey`` ve şifreli ``tünelNonce`` ile ``obfsNonce`` 'ı ChaCha20 ile şifreler
- Tuple {``nextTunnelId``, şifreli (``tünelNonce`` || ``obfsNonce``), AEAD şifreli metin || MAC} 'ı bir sonraki geçişe gönderir.

```text

// Doğrulama için, tünel geçişleri her alınan nonce'ın benzersizliğini Bloom filtresi ile kontrol etmelidir
  // Doğrulamanın ardından, ChaCha20-Poly1305 ile alınan tünelNonce ve inAEADKey ile tünel mesajının şifreli çerçevesini her AEAD çerçevesini açılacak şekilde çözün
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = alınan encMsg \|\| MAC, nonce = alınan tünelNonce, key = inAEADKey)

  // TünelNonce'ı obfsNonce ve geçişin nonceKey ile ChaCha20 ile şifrele
  tünelNonce = ChaCha20(msg = alınan tünelNonce, nonce = alınan obfsNonce, key = nonceKey)

  // Her tünel mesajının şifreli veri çerçevesini şifreli tünelNonce ve geçişin layerKey'i ile ChaCha20 ile şifrele
  encMsg = ChaCha20(msg = encTunMsg, nonce = tünelNonce, key = layerKey)

  // AEAD koruması için, her mesajın şifreli veri çerçevesini şifreli tünelNonce ve geçişin outAEADKey'i ile ChaCha20-Poly1305 ile şifreleyin
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tünelNonce, key = outAEADKey)

  // Alınan obfsNonce'ı, şifreli tünelNonce ve hop'un nonceKey ile ChaCha20 ile şifrele
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tünelNonce, key = nonceKey)
```

### Gelen Uç Nokta İşleme

ChaCha20 tünelleri için, her tünel mesajını çözmek için aşağıdaki şema kullanılacaktır:

- Alınan ``tünelNonce`` ve ``obfsNonce`` 'ı tek tek Bloom filtreleri karşısında doğrula
- Her tünel mesajının şifreli veri çerçevesi ve MAC'ini alınan ``tünelNonce`` ve ``inAEADKey`` ile çözün
- Tünel mesajının şifreli verisi ``tünelNonce`` ve ``layerKey`` ile ChaCha20 ile çözülecek
- ``nonceKey`` ile ``obfsNonce`` 'u ve alınıyormuş gibi ``tünelNonce`` , daha önceki ``obfsNonce`` 'ı elde edin
- Alınan ``tünelNonce`` 'ı, geçişin ``layerKey`` 'i ile şifreli ve ``tünelNonce`` ile çözün ve önceki geçişin ``layerKey`` 'i üzerinde ``obfsNonce`` 'u çözün.
- ``tünelNonce`` 'ı ve ``obfsNonce`` 'ı kullanarak her mesajın şifreli verisini çözün ve önceki geçişin ``layerKey`` 'i ile şifreli ``tünelNonce`` 'ı çözün
- Bu adımları tekrar edin ve tünelin başlangıcına kadar her geçişte, bu katmanlarla Alice-in-Wonderland tarzı ``tünelNonce`` ve ``obfsNonce`` 'ı çözün
- İlk turda yalnızca AEAD çerçeve deşifreleme gereklidir

```text

// İlk tur için, her mesajın şifreli veri çerçevesini + MAC'ını sağlanan tünelNonce ve inAEADKey kullanarak ChaCha20-Poly1305 ile çözün
  msg = encTunMsg \|\| MAC
  tünelNonce = sağlanan tünelNonce
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tünelNonce, key = inAEADKey)

  // Tünel boyunca IBGW'ye kadar her geçiş için tekrarlayın
  // Her tur için, her mesajın şifreli veri çerçevesinde her geçişin katman şifrelemesini ChaCha20 ile çözülecek
  // Alınan tünelNonce'ı, her geçiş için önceki turda çözülen tünelNonce ile değiştirin
  decMsg = ChaCha20(msg = encTunMsg, nonce = tünelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tünelNonce, key = nonceKey)
  tünelNonce = ChaCha20(msg = tünelNonce, nonce = obfsNonce, key = nonceKey)
```

### ChaCha20+ChaCha20-Poly1305 Tünel Katmanı Şifrelemesi için Güvenlik Analizi

AES256/ECB+AES256/CBC'den ChaCha20+ChaCha20-Poly1305'e geçiş, bir dizi avantaj ve yeni güvenlik dikkate alması getirmektedir.

Güvenlik açısından en önemli husus, ChaCha20 ve ChaCha20-Poly1305 nonce'larının anahtarın kullanım süresi boyunca her mesaj için benzersiz olması gerektiğidir.

Aynı anahtarla farklı mesajlar üzerinde benzersiz nonce'lar kullanılmaması, ChaCha20 ve ChaCha20-Poly1305'yi kırar.

Eklenen ``obfsNonce`` , IBEP'nin her geçişte katman şifrelemesi için ``tünelNonce`` 'ı çözmesini ve önceki nonce'ı kurtarmasını sağlar.

``obfsNonce`` , ``tünelNonce`` ile birlikte tünel geçişlerine hiçbir yeni bilgi açıklamaz,
çünkü ``obfsNonce`` , şifreli ``tünelNonce`` kullanılarak şifrelenmiştir. Bu, IBEP'nin de ``tünelNonce`` 'ın önceki durumunu benzer şekilde kurtarmasını sağlar.

En büyük güvenlik avantajı, ChaCha20'ye karşı doğrulama veya oracle saldırılarının olmamasıdır ve geçişler arasında ChaCha20-Poly1305 kullanmak,
dış dünyadan Man-in-the-Middle saldırganlarına karşı AEAD koruması ekler.

AES256/ECB + AES256/CBC'ye karşı, anahtar tekrar kullanıldığında (örneğin tünel katmanı şifrelemede olduğu gibi) pratik oracle saldırıları mevcuttur.

AES256/ECB'ye karşı oracle saldırıları işe yaramaz, çünkü çift şifreleme kullanılır ve şifreleme tek bir blok üzerine yapılır (tünel IV).

AES256/CBC'ye karşı dolgu oracle saldırıları işe yaramaz, çünkü dolgu kullanılmaz. Tünel mesaj uzunluğu hiç
mod-16 olmadığında bile, AES256/CBC hala güvenli olurdu, çünkü kopya IV'ler reddedilir.

Her iki saldırı da aynı IV'yi kullanarak çoklu oracle çağrılarını engelleyerek durdurulur, çünkü kopya IV'ler reddedilir.

## Referanslar

* [Tunnel-Implementation](/docs/specs/implementation/)
