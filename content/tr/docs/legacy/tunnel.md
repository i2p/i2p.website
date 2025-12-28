---
title: "Tunnel Tartışması"
description: "tunnel dolgulaması, parçalama ve oluşturma stratejilerinin tarihsel incelenmesi"
slug: "tunnel"
layout: "single"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
reviewStatus: "needs-review"
---

> **Not:** Bu arşiv, I2P 0.9.41 öncesine ait spekülatif tasarım çalışmalarını içerir. Üretim uygulaması için [tunnel dokümantasyonunu](/docs/specs/implementation/) inceleyin.

## Yapılandırma Alternatifleri

Gelecekteki tunnel ayarlarına yönelik değerlendirilen fikirler şunları içeriyordu:

- Mesaj teslimi için frekans sınırlamaları
- Dolgu politikaları (chaff injection [sahte/boş trafik ekleme] dahil)
- Tunnel ömrü denetimleri
- Yük gönderimi için toplu iş ve kuyruk stratejileri

Bu seçeneklerin hiçbiri eski gerçekleştirimle birlikte sunulmadı.

## Dolgu Stratejileri

Ele alınan olası doldurma yaklaşımları:

- Hiç dolgu yok
- Rastgele uzunlukta dolgu
- Sabit uzunlukta dolgu
- En yakın kilobayta tamamlayan dolgu
- 2'nin kuvvetlerine göre dolgu (`2^n` bayt)

Erken ölçümler (sürüm 0.4), mevcut sabit 1024 baytlık tunnel mesajı boyutunu belirledi. Daha üst düzey garlic mesajları (I2P'de birden çok mesajın tek pakette birleştirilmesi tekniği) kendi dolgularını ekleyebilir.

## Parçalama

Mesaj uzunluğu aracılığıyla etiketleme saldırılarını önlemek için, tunnel mesajları 1024 baytta sabitlenir. Daha büyük I2NP yükleri ağ geçidi tarafından parçalara ayrılır; uç nokta, kısa bir zaman aşımı içinde parçaları yeniden birleştirir. Routers, göndermeden önce paketleme verimliliğini en üst düzeye çıkarmak için parçaları yeniden düzenleyebilir.

## Ek Alternatifler

### Tunnel işleme sürecinin ortasında ayarlama

Üç olasılık incelendi:

1. Bir ara atlamanın, şifreleri çözülmüş yüklere erişim izni vererek bir tunnel'i geçici olarak sonlandırmasına izin verin.
2. Katılımcı router'ların, bir sonraki atlamaya devam etmeden önce iletileri kendi giden tunnel'lerinden biri üzerinden göndererek “yeniden harmanlamasına” izin verin.
3. Tunnel oluşturucusunun bir eşin bir sonraki atlamasını dinamik olarak yeniden tanımlamasına olanak tanıyın.

### İki Yönlü Tunnels

Ayrı gelen ve giden tunnels kullanmak, herhangi bir eş kümesinin gözlemleyebileceği bilgiyi sınırlar (örn. bir GET isteğine karşılık büyük bir yanıt). Çift yönlü tunnels eş yönetimini basitleştirir ancak her iki yönde de eşzamanlı olarak tam trafik örüntülerini ifşa eder. Bu nedenle tek yönlü tunnels tercih edilen tasarım olarak kaldı.

### Arka Kanallar ve Değişken Boyutlar

Değişken tunnel mesaj boyutlarına izin vermek, işbirliği içinde olan eşler arasında (örneğin, seçilen boyutlar veya frekanslar üzerinden veriyi kodlayarak) örtük kanalların oluşturulmasına olanak tanır. Sabit boyutlu mesajlar, bu riski ilave dolgu yükü pahasına azaltır.

## Tunnel Oluşturma Alternatifleri

Kaynak: [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf)

### Eski “Paralel” Derleme Yöntemi

0.6.1.10 sürümünden önce, tunnel oluşturma istekleri her katılımcıya paralel olarak gönderilirdi. Bu yöntem [eski tunnel sayfasında](/docs/legacy/old-implementation/) belgelenmiştir.

### Tek Seferde Teleskopik Oluşturma (Mevcut Yöntem)

Modern yaklaşım, kısmen oluşturulmuş tunnel boyunca oluşturma iletilerini adım adım gönderir. Tor’un telescoping’ine (aşamalı kurulum tekniği) benzer olsa da, oluşturma iletilerini keşif tunnel'lar üzerinden yönlendirmek bilgi sızıntısını azaltır.

### “Etkileşimli” Telescoping (kademeli uzatma)

Açık gidiş-dönüşlerle her seferinde tek bir atlama inşa etmek, eşlerin mesajları saymasına ve tunnel içindeki konumlarını çıkarsamasına olanak tanır; bu nedenle bu yaklaşım reddedildi.

### Keşif Amaçlı Olmayan Yönetim Tunnels

Bir öneri, oluşturma trafiği için ayrı bir yönetim tunnels havuzu sürdürmekti. Bölünmüş router'lara yardımcı olabilse de, yeterli ağ entegrasyonu ile bunun gereksiz olduğu değerlendirildi.

### Keşif Teslimi (Eski)

0.6.1.10'dan önce, tekil tunnel istekleri garlic encryption ile şifrelenip keşif amaçlı tunnels üzerinden iletiliyor ve yanıtlar ayrı olarak geri dönüyordu. Bu strateji, mevcut one-shot telescoping method (tek atımlık teleskoplama yöntemi) ile değiştirildi.

## Ana noktalar

- Sabit boyutlu tunnel mesajları, boyuta dayalı etiketleme ve gizli kanallara karşı koruma sağlar, ek dolgu maliyetine rağmen.
- Alternatif dolgulama, parçalama ve oluşturma stratejileri incelendi, ancak anonimlikteki ödünler dikkate alındığında benimsenmedi.
- Tunnel tasarımı, verimlilik, gözlemlenebilirlik ve öncül (predecessor) ile tıkanıklık (congestion) saldırılarına karşı dayanıklılık arasında denge kurmaya devam ediyor.
