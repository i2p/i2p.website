---
title: "Tünel Yönlendirme"
description: "I2P tünel terminolojisi, oluşturumu ve yaşam döngüsüne genel bakış"
slug: "tunnel-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Genel Bakış

I2P, geçici, tek yönlü tüneller oluşturur — şifrelenmiş trafiği ileten yönlendiricilerin sıralı dizileridir. Tüneller **inbound** (gelen, mesajlar oluşturucuya doğru akar) veya **outbound** (giden, mesajlar oluşturucudan uzağa akar) olarak sınıflandırılır.

Tipik bir değişimde Alice'in mesajı, giden tünellerinden biri üzerinden yönlendirilir, giden uç noktaya Bob'un gelen tünellerinden birinin ağ geçidine iletmesi talimatı verilir ve ardından Bob mesajı gelen uç noktasında alır.

![Alice giden tüneli üzerinden Bob'un gelen tüneline bağlanıyor](/images/tunnelSending.png)

- **A**: Giden Gateway (Alice)
- **B**: Giden Katılımcı
- **C**: Giden Uç Nokta
- **D**: Gelen Gateway
- **E**: Gelen Katılımcı
- **F**: Gelen Uç Nokta (Bob)

Tunnel'ların sabit 10 dakikalık bir ömrü vardır ve mesaj boyutu veya zamanlama desenlerine dayalı trafik analizini önlemek için 1024 bayt (tunnel başlığı dahil 1028 bayt) sabit boyutlu mesajlar taşırlar.

## Tunnel Sözlüğü

- **Tunnel gateway (Tünel ağ geçidi):** Bir tüneldeki ilk router. Gelen tüneller için, bu router'ın kimliği yayınlanan [LeaseSet](/docs/specs/common-structures/) içinde görünür. Giden tüneller için, gateway başlangıç router'ıdır (yukarıdaki A ve D).
- **Tunnel endpoint (Tünel uç noktası):** Bir tüneldeki son router (yukarıdaki C ve F).
- **Tunnel participant (Tünel katılımcısı):** Bir tüneldeki ara router (yukarıdaki B ve E). Katılımcılar kendi konumlarını veya tünel yönünü belirleyemez.
- **n-hop tunnel (n-atlamalı tünel):** Router'lar arası atlama sayısı.
  - **0-hop:** Gateway ve endpoint aynı router'dır – minimum anonimlik.
  - **1-hop:** Gateway doğrudan endpoint'e bağlanır – düşük gecikme, düşük anonimlik.
  - **2-hop:** Keşif tünelleri için varsayılan; dengeli güvenlik/performans.
  - **3-hop:** Güçlü anonimlik gerektiren uygulamalar için önerilir.
- **Tunnel ID:** Her router ve her atlama için benzersiz olan 4 byte'lık tamsayı, oluşturucu tarafından rastgele seçilir. Her atlama farklı ID'ler üzerinde alır ve iletir.

## Tünel Oluşturma Bilgileri

Gateway, katılımcı ve endpoint rollerini dolduran router'lar, Tunnel Build Message içinde farklı kayıtlar alır. Modern I2P iki yöntemi destekler:

- **ElGamal** (eski, 528-bayt kayıtlar)
- **ECIES-X25519** (güncel, 218-bayt kayıtlar Short Tunnel Build Message – STBM aracılığıyla)

### Information Distributed to Participants

**Gateway alır:** - Tunnel katman anahtarı (tunnel türüne bağlı olarak AES-256 veya ChaCha20 anahtarı) - Tunnel IV anahtarı (başlatma vektörlerini şifrelemek için) - Yanıt anahtarı ve yanıt IV'si (derleme yanıtı şifrelemesi için) - Tunnel ID (yalnızca gelen gateway'ler için) - Sonraki atlama kimlik hash'i ve tunnel ID'si (terminal değilse)

**Ara katılımcılar şunları alır:** - Kendi atlamaları için tunnel katman anahtarı ve IV anahtarı - Tunnel ID ve sonraki atlama bilgisi - Oluşturma yanıtı şifrelemesi için yanıt anahtarı ve IV

**Uç noktalar şunları alır:** - Tunnel katmanı ve IV anahtarları - Yanıt router'ı ve tunnel kimliği (yalnızca giden uç noktalar) - Yanıt anahtarı ve IV (yalnızca giden uç noktalar)

Tüm detaylar için [Tunnel Oluşturma Spesifikasyonu](/docs/specs/implementation/) ve [ECIES Tunnel Oluşturma Spesifikasyonu](/docs/specs/implementation/) bölümlerine bakın.

## Tunnel Pooling

Router'lar yedeklilik ve yük dağılımı için tünelleri **tünel havuzları** halinde gruplar. Her havuz, birinin başarısız olması durumunda yük devretmeye olanak tanıyan birden fazla paralel tünel tutar. Dahili olarak kullanılan havuzlar **exploratory tunnel**'lardır (keşif tünelleri), uygulama özelindeki havuzlar ise **client tunnel**'lardır (istemci tünelleri).

Her hedef, I2CP seçenekleriyle (tünel sayısı, yedek sayısı, uzunluk ve QoS parametreleri) yapılandırılan ayrı gelen ve giden havuzları tutar. Router'lar tünel sağlığını izler, periyodik testler çalıştırır ve havuz boyutunu korumak için başarısız tünelleri otomatik olarak yeniden inşa eder.

## Tunnel Havuzu

**0-hop Tüneller** : Yalnızca makul inkar edilebilirlik sağlar. Trafik her zaman aynı router'da başlar ve sonlanır — anonim kullanım için önerilmez.

**1-hop Tünelleri**: Pasif gözlemcilere karşı temel anonimlik sağlar ancak bir saldırgan o tek hop'u kontrol ediyorsa savunmasızdır.

**2 sekmeli Tüneller** : İki uzak router içerir ve saldırı maliyetini önemli ölçüde artırır. Keşif havuzları için varsayılan ayardır.

**3 atlama Tünel**: Güçlü anonimlik koruması gerektiren uygulamalar için önerilir. Ekstra atlamalar anlamlı bir güvenlik kazancı olmadan gecikme ekler.

**Varsayılanlar**: Router'lar performans ve anonimlik dengesini sağlamak için **2 atlamalı** keşif tünelleri ve uygulamaya özgü **2 veya 3 atlamalı** istemci tünelleri kullanır.

## Tünel Uzunluğu

Router'lar periyodik olarak tünelleri test etmek için bir giden tünelden gelen bir tünele `DeliveryStatusMessage` göndererek test eder. Test başarısız olursa, her iki tünel de olumsuz profil ağırlığı alır. Ardışık başarısızlıklar bir tüneli kullanılamaz olarak işaretler; router daha sonra bir yedek oluşturur ve yeni bir LeaseSet yayınlar. Sonuçlar, [eş seçim sistemi](/docs/overview/tunnel-routing/) tarafından kullanılan eş kapasite metriklerine beslenir.

## Tünel Testi

Router'lar, etkileşimsiz bir **teleskoplama** yöntemi kullanarak tüneller oluşturur: tek bir Tunnel Build Message (Tünel Oluşturma Mesajı) atlama atlama yayılır. Her atlama kendi kaydının şifresini çözer, yanıtını ekler ve mesajı iletir. Son atlama, birleştirilmiş oluşturma yanıtını farklı bir yol üzerinden geri döndürerek korelasyonu önler. Modern uygulamalar ECIES için **Short Tunnel Build Messages (STBM)** ve eski yollar için **Variable Tunnel Build Messages (VTBM)** kullanır. Her kayıt, ElGamal veya ECIES-X25519 kullanılarak atlama başına şifrelenir.

## Tünel Oluşturma

Tünel trafiği çok katmanlı şifreleme kullanır. Mesajlar tünelden geçerken her atlama noktası bir şifreleme katmanı ekler veya kaldırır.

- **ElGamal tünelleri:** PKCS#5 dolgusu ile yükler için AES-256/CBC.
- **ECIES tünelleri:** Kimlik doğrulamalı şifreleme için ChaCha20 veya ChaCha20-Poly1305.

Her atlama iki anahtara sahiptir: bir **katman anahtarı** ve bir **IV anahtarı**. Router'lar IV'yi şifreler, yükü işlemek için kullanır, ardından iletmeden önce IV'yi yeniden şifreler. Bu çift IV şeması mesaj etiketlemeyi önler.

Giden ağ geçitleri tüm katmanları önceden şifreler, böylece tüm katılımcılar şifreleme ekledikten sonra uç noktalar düz metin alır. Gelen tüneller ters yönde şifreler. Katılımcılar tünel yönünü veya uzunluğunu belirleyemez.

## Tünel Şifreleme

- Ağ yük dengeleme için dinamik tunnel ömürleri ve uyarlanabilir havuz boyutlandırma
- Alternatif tunnel test stratejileri ve bireysel atlama tanılaması
- İsteğe bağlı proof-of-work veya bant genişliği sertifikası doğrulaması (API 0.9.65+ sürümünde uygulanmıştır)
- Uç nokta karıştırma için trafik şekillendirme ve chaff ekleme araştırması
- ElGamal'ın sürekli emekliye ayrılması ve ECIES-X25519'a geçiş

## Devam Eden Geliştirme

- [Tunnel Uygulama Spesifikasyonu](/docs/specs/implementation/)
- [Tunnel Oluşturma Spesifikasyonu (ElGamal)](/docs/specs/implementation/)
- [Tunnel Oluşturma Spesifikasyonu (ECIES-X25519)](/docs/specs/implementation/)
- [Tunnel Mesaj Spesifikasyonu](/docs/specs/implementation/)
- [Garlic Routing](/docs/overview/garlic-routing/)
- [I2P Ağ Veritabanı](/docs/specs/common-structures/)
- [Eş Profilleme ve Seçimi](/docs/overview/tunnel-routing/)
- [I2P Tehdit Modeli](/docs/overview/threat-model/)
- [ElGamal/AES + SessionTag Şifreleme](/docs/legacy/elgamal-aes/)
- [I2CP Seçenekleri](/docs/specs/i2cp/)
