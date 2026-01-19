---
title: "Akademik Araştırma"
description: "I2P ağı üzerinde akademik araştırmalar için bilgi ve yönergeler"
layout: "research"
---

<div id="intro"></div>

## I2P Akademik Araştırma

Anonimlik üzerine geniş bir yelpazede konuları araştıran büyük bir araştırma topluluğu bulunmaktadır. Anonim ağların gelişmeye devam etmesi için karşılaşılan sorunların anlaşılmasının önemli olduğuna inanıyoruz. I2P ağı üzerinde yapılan araştırmalar henüz emekleme aşamasındadır ve bugüne kadar yapılan araştırmaların çoğu diğer anonim ağlar üzerine odaklanmıştır. Bu, orijinal araştırma katkıları için benzersiz bir fırsat sunmaktadır.

<div id="notes"></div>

## Araştırmacılar İçin Notlar

### Savunmacı Araştırma Öncelikleri

Ağı güçlendirmemize ve güvenliğini artırmamıza yardımcı olacak araştırmaları memnuniyetle karşılıyoruz. I2P altyapısını güçlendiren testler teşvik edilmektedir ve takdir edilmektedir.

### Araştırma İletişim Yönergeleri

Araştırmacıları, araştırma fikirlerini erken dönemde geliştirme ekibiyle paylaşmaları için güçlü bir şekilde teşvik ediyoruz. Bu, aşağıdaki konularda yardımcı olur:

- Mevcut projelerle olası örtüşmelerin önlenmesi
- Ağa verilebilecek potansiyel zararların en aza indirilmesi
- Test ve veri toplama çabalarının koordinasyonu
- Araştırmanın ağ hedefleriyle uyumlu olmasını sağlama

<div id="ethics"></div>

## Araştırma Etiği & Test Yönergeleri

### Genel İlkeler

I2P üzerinde araştırma yaparken lütfen aşağıdakileri göz önünde bulundurun:

1. **Araştırmanın faydalarını ve risklerini değerlendirin** - Araştırmanızın potansiyel faydalarının ağ veya kullanıcıları için herhangi bir riskten daha ağır basıp basmadığını değerlendirin
2. **Canlı ağ yerine test ağını tercih edin** - Mümkün olduğunda I2P'nin test ağı yapılandırmasını kullanın
3. **Asgari gerekli verileri toplayın** - Araştırmanız için gereken asgari miktarda veri toplayın
4. **Yayımlanan verilerin kullanıcı gizliliğine saygı göstermesini sağlayın** - Yayımlanan veriler anonimize edilmeli ve kullanıcı gizliliğine saygı göstermelidir

### Ağ Testi Yöntemleri

I2P üzerinde test yapması gereken araştırmacılar için:

- **Test ağ yapılandırmasını kullanın** - I2P, izole bir test ağında çalışacak şekilde yapılandırılabilir
- **MultiRouter modunu kullanın** - Tek bir makinede birden fazla yönlendirici örneği çalıştırarak test yapın
- **Yönlendirici ailesi yapılandırmasını yapın** - Araştırma yönlendiricilerinizi bir yönlendirici ailesi olarak yapılandırarak tanınabilir hale getirin

### Tavsiye Edilen Uygulamalar

- **Canlı ağ testi öncesi I2P ekibiyle iletişime geçin** - Canlı ağ üzerinde herhangi bir test yapmadan önce research@i2p.net adresinden bizimle iletişime geçin
- **Yönlendirici ailesi yapılandırmasını kullanın** - Bu, araştırma yönlendiricilerinizi ağa şeffaf hale getirir
- **Potansiyel ağ müdahalesini önleyin** - Testlerinizi, düzenli kullanıcılar üzerindeki olumsuz etkileri en aza indirecek şekilde tasarlayın

<div id="questions"></div>

## Açık Araştırma Soruları

I2P topluluğu, araştırmanın özellikle değerli olacağı birkaç alan belirlemiştir:

### Ağ Veritabanı

**Floodfills:**
- Floodfill kontrolü aracılığıyla ağ brute-force saldırılarına karşı başka nasıl önlemler alınabilir?
- Merkeze bağlı bir otoriteye ihtiyaç duymadan 'kötü floodfill'leri tespit etmek, işaretlemek ve potansiyel olarak kaldırmak mümkün mü?

### Taşıma Yöntemleri

- Paket yeniden iletim stratejileri ve zaman aşımı süreleri nasıl iyileştirilebilir?
- I2P'nin paketleri gizlemesi ve trafik analizi azaltması daha verimli bir şekilde sağlanabilir mi?

### Tüneller ve Hedefler

**Eş Seçimi:**
- I2P'nin eş seçimini daha verimli veya güvenli bir şekilde gerçekleştirebilmesi mümkün mü?
- Yakın eşleri öne çıkaracak geoip kullanımı anonimliği olumsuz etkiler mi?

**Tek Yönlü Tüneller:**
- Tek yönlü tünellerin çift yönlü tünellere göre avantajları nelerdir?
- Tek yönlü ve çift yönlü tüneller arasındaki ödünleşimler nedir?

**Çoklu Konumlandırma:**
- Çoklu konumlandırma yük dengelemede ne kadar etkilidir?
- Nasıl ölçeklenir?
- Daha fazla yönlendirici aynı Hedefi barındırdıkça ne olur?
- Anonimlik üzerindeki ödünleşimler nelerdir?

### Mesaj Yönlendirme

- Mesajların parçalanması ve karıştırılması ile zamanlama saldırılarının etkinliği ne kadar azaltılır?
- I2P'nin faydalanabileceği karıştırma stratejileri nelerdir?
- Yüksek gecikmeli teknikler düşük gecikmeli ağla ne ölçüde etkili bir şekilde birleştirilebilir?

### Anonimlik

- Tarayıcı parmak izi tanımlama I2P kullanıcılarının anonimliği üzerinde ne kadar etkili?
- Bir tarayıcı paketi geliştirilmesi ortalama kullanıcılara fayda sağlar mı?

### Ağ İle İlgili

- 'Açgözlü kullanıcılar'ın ağ üzerindeki genel etkisi nedir?
- Bant genişliği katılımını teşvik edici ek adımlar değerli olur mu?

<div id="contact"></div>

## İletişim

Araştırma talepleri, iş birliği fırsatları veya araştırma planlarınızı tartışmak için lütfen bizimle iletişime geçin:

**E-posta:** research@i2p.net

I2P ağını geliştirmek için araştırma topluluğuyla birlikte çalışmayı dört gözle bekliyoruz!