---
title: "Eski Tunnel İmplementasyonu (Eski)"
description: "I2P 0.6.1.10'dan önce kullanılan tunnel tasarımının arşivlenmiş açıklaması."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Eski durum:** Bu içerik yalnızca tarihsel referans amacıyla saklanmaktadır. I2P&nbsp;0.6.1.10'dan önce dağıtılan tunnel sistemini belgeler ve modern geliştirmede kullanılmamalıdır. Üretime yönelik rehberlik için [güncel gerçekleştirim](/docs/specs/implementation/)'e bakın.

Özgün tunnel alt sistemi de tek yönlü tunnel'lar kullanıyordu, ancak mesaj düzeni, yinelenenlerin tespiti ve inşa stratejisi açısından farklıydı. Karşılaştırmayı kolaylaştırmak için aşağıdaki pek çok bölüm, kullanımdan kaldırılmış belgenin yapısını yansıtır.

## 1. Tunnel'e Genel Bakış

- Tunnels, oluşturucu tarafından seçilen eşlerden oluşan sıralı diziler olarak oluşturulurdu.
- Tunnel uzunlukları 0–7 atlama arasında değişirdi; dolgu, hız sınırlama ve chaff (örtü trafiği) üretimi için çeşitli ayarlar vardı.
- Inbound tunnels, güvenilmeyen bir ağ geçidinden oluşturucuya (uç nokta) mesajları iletirdi; outbound tunnels ise veriyi oluşturucudan dışarı gönderirdi.
- Tunnel ömürleri 10 dakikaydı; bunun ardından yeni tunnels oluşturulurdu (çoğu zaman aynı eşler kullanılır, ancak farklı tunnel ID'leri atanırdı).

## 2. Eski Tasarımda İşleyiş

### 2.1 Mesaj Ön İşleme

Geçitler ≤32&nbsp;KB I2NP yükü biriktirdi, dolgu seçti ve şu içeriği içeren bir yük üretti:

- İki baytlık bir dolgu uzunluğu alanı ve aynı sayıda rastgele bayt
- Teslimat hedeflerini, parçalamayı ve isteğe bağlı gecikmeleri tanımlayan `{instructions, I2NP message}` çiftlerinden oluşan bir dizi
- 16 baytlık hizalama sınırına kadar doldurulmuş tam I2NP mesajları

Teslimat talimatları yönlendirme bilgilerini bit alanlarına paketliyordu (teslimat türü, gecikme bayrakları, parçalama bayrakları ve isteğe bağlı uzantılar). Parçalanmış iletiler 4 baytlık bir ileti kimliği ve ayrıca bir indeks/son parça bayrağı taşıyordu.

### 2.2 Ağ Geçidi Şifrelemesi

Eski tasarım, şifreleme aşaması için tunnel uzunluğunu sekiz atlamaya sabitlemişti. Ağ geçitleri, her atlamanın yükü küçültmeden bütünlüğü doğrulayabilmesi için AES-256/CBC ve sağlama toplamı bloklarını katmanladı. Sağlama toplamının kendisi, iletinin içine gömülü SHA-256’tan türetilmiş bir bloktu.

### 2.3 Katılımcı Davranışı

Katılımcılar, gelen tunnel ID'lerini izledi, bütünlüğü erkenden doğruladı ve iletmeden önce yinelenenleri attı. Dolgu ve doğrulama blokları mesaja gömülü olduğundan, atlama sayısından bağımsız olarak mesaj boyutu sabit kaldı.

### 2.4 Uç Nokta İşleme

Uç noktalar, katmanlı blokların şifresini ardışık olarak çözdü, sağlama toplamlarını doğruladı ve yükü, sonraki iletim için kodlanmış talimatlar ile I2NP iletileri olarak yeniden ayırdı.

## 3. Tunnel Oluşturma (Kullanımdan Kaldırılmış Süreç)


## 4. Bant Daraltma ve Karıştırma Kavramları

Eski doküman, sonraki sürümlere yön veren birkaç strateji önerdi:

- Ağ tıkanıklığı kontrolü için Weighted Random Early Discard (WRED)
- Son dönemdeki kullanımın hareketli ortalamalarına dayalı tunnel başına hız sınırlamaları
- İsteğe bağlı chaff (sahte trafik) ve toplu işleme kontrolleri (tam olarak uygulanmamıştır)

## 5. Arşivlenmiş Alternatifler

Orijinal belgenin bazı bölümleri, hiçbir zaman devreye alınmamış fikirleri inceliyordu:

- Her atlama başına işlemi azaltmak için checksum bloklarını kaldırmak
- Eş (peer) bileşimini değiştirmek için akış ortasında tunnels üzerinde teleskoplama yapmak
- Çift yönlü tunnels kullanmaya geçmek (nihayetinde reddedildi)
- Daha kısa hash'ler veya farklı padding (dolgu) düzenleri kullanmak

Bu fikirler, değerli bir tarihsel bağlam olarak önemini koruyor, ancak modern kod tabanını yansıtmıyor.

## Referanslar

- Özgün eski belge arşivi (0.6.1.10 öncesi)
- [Tunnel'e Genel Bakış](/docs/overview/tunnel-routing/) güncel terminoloji için
- [Eş Profilleme ve Seçimi](/docs/overview/tunnel-routing#peer-selection/) modern sezgisel yöntemler için
