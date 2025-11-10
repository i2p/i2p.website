---
title: "I2P önerisi #165: SSU2 düzeltmesi"
number: "165"
author: "weko, orignal, the Anonymous, zzz"
created: "2024-01-19"
lastupdated: "2024-11-17"
status: "Açık"
thread: "http://i2pforum.i2p/viewforum.php?f=13"
target: "0.9.62"
---

Öneri, weko, orignal, the Anonymous ve zzz tarafından hazırlanmıştır.


### Genel Bakış

Bu belge, SSU2'deki güvenlik açıklarından yararlanan bir saldırının ardından SSU2'ye yönelik değişiklikler önermektedir. Birincil hedef, güvenliği artırmak ve Dağıtık Hizmet Engelleme (DDoS) saldırılarını ve anonimlikten çıkarmaya yönelik girişimleri önlemektir.

### Tehdit modeli

Bir saldırgan, yeni sahte RI'lar (yönlendirici yoktur) oluşturur: normal RI'dır, ancak adres, port, s ve i anahtarlarını gerçek Bob'un yönlendiricisinden alır, ardından ağı doldurur. Gerçek olduğunu düşündüğümüz bu yönlendiriciye bağlanmaya çalıştığımızda, Alice olarak bu adrese bağlanabiliriz, ancak bunun gerçek Bob'un RI ile yapıldığından emin olamayız. Bu mümkündür ve Dağıtık Hizmet Engelleme saldırısı için kullanılmıştır (büyük miktarda böyle RI oluşturup ağı doldur), ayrıca bu, iyi yönlendiricileri suçlayarak ve saldırganın yönlendiricilerini suçlamayarak anonimlikten çıkarma saldırılarını da kolaylaştırabilir. Eğer birden fazla RI ile IP'yi yasaklarsak (bunun yerine tünel kurmayı bu RI'larla aynı yönlendiriciye daha iyi dağıtmak yerine).

### Olası düzeltmeler

#### 1. Değişiklik öncesi eski yönlendiriciler için destekle düzeltme

.. _overview-1:

Genel Bakış
^^^^^^^^

Eski yönlendiricilerle SSU2 bağlantılarını desteklemek için bir geçici çözüm.

Davranış
^^^^^^^^

Bob'un yönlendirici profili 'doğrulanmış' bayrağına sahip olmalıdır, bu bayrak tüm yeni yönlendiriciler (henüz profili olmayan) için varsayılan olarak yanlıştır. 'Doğrulanmış' bayrağı yanlış olduğunda, Alice olarak Bob ile SSU2 bağlantılarını asla yapmayız - RI'de emin olamayız. Bob bize (Alice) NTCP2 veya SSU2 ile bağlanırsa veya biz (Alice) Bob'a NTCP2 ile bir kez bağlandıysak (bu durumlarda Bob'un RouterIdent'ini doğrulayabiliriz) - bayrak doğru olarak ayarlanır.

Sorunlar
^^^^^^^^

Böylece, sahte SSU2-yalnızca RI doldurmasıyla ilgili bir sorun var: bunu kendimiz doğrulayamıyoruz ve gerçek yönlendiricinin bizimle bağlantı kurmasını beklemek zorunda kalıyoruz.

#### 2. Bağlantı oluştururken RouterIdent doğrulama

.. _overview-2:

Genel Bakış
^^^^^^^^

SessionRequest ve SessionCreated için "RouterIdent" bloğu ekleyin.

RouterIdent bloğunun olası formatı
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 bayt bayraklar, 32 bayt RouterIdent. Flag_0: alıcının RouterIdent'i ise 0; göndericinin RouterIdent'i ise 1

Davranış
^^^^^^^^

Alice (yapmalı(1), yapabilir(2)) yükte RouterIdent bloğu Flag_0 = 0 ve Bob'un RouterIdent'ini gönderir. Bob (yapmalı(3), yapabilir(4)) bunun kendi RouterIdent'i olup olmadığını kontrol eder, değilse: "Yanlış RouterIdent" nedeni ile oturumu sonlandırır, eğer kendi RouterIdent'i ise: Flag_0'da 1 ile RI bloğunu ve Bob'un RouterIdent'ini gönderir.

(1) Bob, eski yönlendiricileri desteklemez. (2) Bob, eski yönlendiricileri destekler ancak sahte RI'larla bağlantı kurmaya çalışan yönlendiricilerden gelen DDoS'un kurbanı olabilir. (3) Alice, eski yönlendiricileri desteklemez. (4) Alice, eski yönlendiricileri destekler ve hibrit bir şema kullanır: Eski yönlendiriciler için Düzeltme 1 ve yeni yönlendiriciler için Düzeltme 2. RI yeni sürüm derse, ancak bağlantı sırasında RouterIdent bloğunu almadık - RI'yi sonlandır ve kaldır.

.. _problems-1:

Sorunlar
^^^^^^^^

Bir saldırgan sahte yönlendiricilerini eski olarak gösterebilir ve (4) ile her durumda 'doğrulanmış' bayrak için beklemek zorundayız.

Notlar
^^^^^

32 baytlık RouterIdent yerine, muhtemelen 4 baytlık hash'in siphash'ini, bazı HKDF veya başka bir şeyi kullanabiliriz, bu yeterli olmalıdır.

#### 3. Bob i = RouterIdent ayarlar

.. _overview-3:

Genel Bakış
^^^^^^^^

Bob, kendi RouterIdent'ini i anahtarı olarak kullanır.

.. _behavior-1:

Davranış
^^^^^^^^

Bob (yapmalı(1), yapabilir(2)) kendi RouterIdent'ini SSU2 için i anahtarı olarak kullanır.

Alice ile (1) sadece i = Bob'un RouterIdent'i olduğunda bağlanır. Alice ile (2) hibrit şemayı (düzeltme 3 ve 1) kullanır: i = Bob'un RouterIdent'i ise bağlantıyı yapabiliriz, aksi takdirde önce doğrulamalıyız (bkz. düzeltme 1).

(1) Alice, eski yönlendiricileri desteklemez. (2) Alice, eski yönlendiricileri destekler.

.. _problems-2:

Sorunlar
^^^^^^^^

Bir saldırgan sahte yönlendiricilerini eski olarak gösterebilir ve (2) ile zaten her durumda 'doğrulanmış' bayrak için bekleme yapıyoruz.

.. _notes-1:

Notlar
^^^^^

RI boyutundan tasarruf etmek için, i anahtarı belirtilmediği durumlarda işlem ekle. Eğer varsa, i = RouterIdent. Bu durumda, Bob eski yönlendiricileri desteklemez.

#### 4. SessionRequest'in KDF'sine bir MixHash daha ekleyin

.. _overview-4:

Genel Bakış
^^^^^^^^

"SessionRequest" mesajının NOISE durumuna MixHash(Bob'un ident hash'i) ekleyin, örn. h = SHA256 (h || Bob'un ident hash'i). ENCRYPT veya DECRYPT için ad olarak kullanılan son MixHash olması gerekir. Ek bir SSU2 başlık bayrağı "Bob'un ident'ini doğrula" = 0x02 eklenmelidir.

.. _behavior-4:

Davranış
^^^^^^^^

- Alice, Bob'un RouterInfo'sundan Bob'un ident hash'i ile MixHash ekler ve ENCRYPT için ad olarak kullanır ve "Bob'un ident'ini doğrula" bayrağını ayarlar
- Bob, "Bob'un ident'ini doğrula" bayrağını kontrol eder ve kendi ident hash'i ile MixHash ekler ve DECRYPT için ad olarak kullanır. AEAD/Chacha20/Poly1305 başarısız olduğunda, Bob oturumu kapatır.

Eski yönlendiricilerle uyumluluk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice, Bob'un yönlendirici sürümünü kontrol etmeli ve bu öneriyi destekleyen asgari sürümü karşılıyorsa bu MixHash'i eklemeli ve "Bob'un ident'ini doğrula" bayrağını ayarlamalıdır. Yönlendirici eskiyse, Alice MixHash eklemez ve "Bob'un ident'ini doğrula" bayrağını ayarlamaz.
- Bob, "Bob'un ident'ini doğrula" bayrağını kontrol eder ve bu MixHash'i ekler. Eski yönlendirici bu bayrağı ayarlamaz ve bu MixHash eklenmemelidir.

.. _problems-4:

Sorunlar
^^^^^^^^

- Bir saldırgan, sahte yönlendiricileri eski sürüm olarak gösterebilir. Belirli bir noktada eski yönlendiricilerin özenle kullanılması ve başka yollarla doğrulanması gereklidir.


### Geriye dönük uyumluluk

Düzeltmelerde açıklanmıştır.


### Mevcut durum

i2pd: Düzeltme 1.
