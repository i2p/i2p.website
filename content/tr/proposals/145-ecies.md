---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Açık"
thread: "http://zzz.i2p/topics/2418"
---

## Motivasyon

ECIES-P256, ElGamal'dan çok daha hızlıdır. Zaten birkaç i2pd eepsite ECIES-P256 kripto türünü kullanmaktadır ve Java'nın onlarla iletişim kurabilmesi ve tersinin de mümkün olması gerekir. i2pd, 2.16.0 sürümünden (Java 0.9.32) bu yana bunu desteklemektedir.

## Genel Bakış

Bu teklif, kimliğin sertifika kısmında veya LeaseSet2'de ayrı bir şifreleme anahtarı türü olarak görünebilen yeni kripto türü ECIES-P256'yı tanıtır. RouterInfo, LeaseSet1 ve LeaseSet2'de kullanılabilir.


### ElGamal Anahtar Yerleri

Bir gözden geçirme olarak,
256 baytlık ElGamal genel anahtarları aşağıdaki veri yapılarında bulunabilir.
Ortak yapılar spesifikasyonuna başvurun.

- Bir Yönlendirici Kimliğinde
  Bu, yönlendiricinin şifreleme anahtarıdır.

- Bir Hedefte
  Hedefin genel anahtarı, eski i2cp'ten i2cp'ye şifreleme için kullanılırdı,
  bu, versiyon 0.6'da devre dışı bırakıldı, şu anda yalnızca
  LeaseSet şifrelemesi için IV için kullanılmaktadır, bu da eskimiştir.
  LeaseSet'teki genel anahtar bunun yerine kullanılır.

- Bir LeaseSet'te
  Bu, hedefin şifreleme anahtarıdır.

Yukarıdaki 3 durumda, ECIES genel anahtarı hâlâ 256 bayt tutar, ancak gerçek anahtar uzunluğu 64 bayttır.
Geri kalan rastgele doldurulmalı.

- Bir LS2'de
  Bu, hedefin şifreleme anahtarıdır. Anahtar boyutu 64 bayttır.


### Anahtar Sertifikalarındaki EncTypes

ECIES-P256 şifreleme türü 1'i kullanır.
Şifreleme türleri 2 ve 3, ECIES-P284 ve ECIES-P521 için ayrılmalıdır.


### Asimetrik Kripto Kullanımları

Bu teklif, ElGamal'ın yerine geçecek şeyleri tarif eder:

1) Tünel İnşa mesajları (anahtar RouterIdentity'dedir). ElGamal bloğu 512 bayttır
  
2) Müşteri Uçtan Uca ElGamal+AES/OturumEtiketi (anahtar LeaseSet'tedir, Hedef anahtarı kullanılmaz). ElGamal bloğu 514 bayttır

3) Netdb ve diğer I2NP mesajlarının yönlendirici-yönlendirici şifrelemesi. ElGamal bloğu 514 bayttır


### Hedefler

- Geriye dönük uyumlu
- Mevcut veri yapılarında değişiklik yok
- ElGamal'dan çok daha fazla CPU-verimli

### Hedef Dışı

- RouterInfo ve LeaseSet1, ElGamal ve ECIES-P256'yı birlikte yayınlayamaz

### Gerekçe

ElGamal/AES+OturumEtiketi motoru her zaman etiket eksikliğine takılır, bu da I2P iletişimlerinde dramatik performans düşüşüne yol açar.
Tünel oluşturma en ağır işlemdir çünkü oluşturucu her tünel oluşturma isteği için ElGamal şifrelemesini 3 kez çalıştırmak zorundadır.


## Gerekli Kriptografik Primitifler

1) EC P256 eğrisi anahtar üretimi ve DH

2) AES-CBC-256

3) SHA256


## Ayrıntılı Teklif

ECIES-P256 ile bir hedef, sertifikada kripto türü 1 ile kendini yayımlar.
Kimlikteki 256'nın ilk 64 baytı ECIES genel anahtarı olarak yorumlanmalı ve geri kalanı göz ardı edilmelidir.
LeaseSet'in ayrı şifreleme anahtarı, kimlikten anahtar türüne dayanır.

### ElGamal/AES+OturumEtiketleri için ECIES blok
ECIES bloku, ElGamal/AES+OturumEtiketleri için ElGamal bloğunun yerine geçer. Uzunluğu 514 bayttır.
Her biri 257 bayt olan iki kısımdan oluşur. 
İlk kısım sıfır ile başlar ve ardından 64 baytlık P256 geçici genel anahtarı, geri kalan 192 bayt rastgele doldurmadır.
İkinci kısım sıfır ile başlar ve ardından ElGamal'dakilerle aynı içeriği AES-CBC-256 şifreler.

### Tünel yapı kaydı için ECIES blok
Tünel yapı kaydı aynıdır, ancak bloklardaki ön sıfırlar olmadan.
Bir tünel, yönlendiricilerin kripto türlerinin herhangi bir kombinasyonu aracılığıyla olabilir ve bu her kayıt için yapılır.
Tünelin oluşturucusu, tünel katılımcısının yayımlanan kripto türüne bağlı olarak kayıtları şifreler, tünel katılımcısı kendi kripto türüne dayanarak çözer.


### AES-CBC-256 anahtarı
Bu, KDF'nin x koordinatı üzerinde SHA256 olduğu ECDH paylaşılan anahtar hesaplamasıdır.
Şifreci olarak Alice ve çözümleyici olarak Bob'u varsayın.
k, Alice'in rastgele seçilmiş geçici P256 özel anahtarı ve P, Bob'un genel anahtarıdır.
S, paylaşılan sırdır S(Sx, Sy)
Alice, S'yi P ile "anlaşarak" hesaplar, örneğin S = k*P.

K'nin Alice'in geçici genel anahtarı ve p'nin Bob'un özel anahtarı olduğunu varsayın.
Bob, alınan mesajın ilk bloğundan K'yi alır ve S = p*K olarak S'yi hesaplar

AES şifreleme anahtarı SHA256(Sx) ve iv Sy'dir.
