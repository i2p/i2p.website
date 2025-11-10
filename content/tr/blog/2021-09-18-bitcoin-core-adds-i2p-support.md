---
title: "Bitcoin Core I2P desteği ekledi!"
date: 2021-09-18
author: "idk"
description: "Yeni bir kullanım senaryosu ve artan benimsenmenin bir göstergesi"
categories: ["general"]
API_Translate: doğru
---

Aylarca süren çalışmaların ardından, Bitcoin Core I2P için resmi destek ekledi! I2P üzerinden Bitcoin düğümleri, hem I2P hem de clearnet (açık internet) içinde faaliyet gösteren düğümlerin yardımıyla Bitcoin düğümlerinin geri kalanıyla tam olarak etkileşim kurabilir ve bu da onları Bitcoin ağında birinci sınıf katılımcılar haline getirir. Bitcoin gibi büyük toplulukların, I2P’nin kendilerine sağlayabileceği, dünya genelindeki insanlara gizlilik ve erişilebilirlik sunan avantajları fark etmesini görmek heyecan verici.

## Nasıl Çalışır

I2P desteği SAM API aracılığıyla otomatik olarak sağlanır. Bu aynı zamanda heyecan verici bir haber, çünkü I2P'nin özellikle iyi olduğu bazı noktaları öne çıkarıyor; örneğin, uygulama geliştiricilerine I2P bağlantılarını programatik ve kolay bir şekilde kurma olanağı tanıması. Bitcoin-over-I2P kullanıcıları, SAM API'yi etkinleştirip Bitcoin'i I2P etkinleştirilmiş şekilde çalıştırarak hiçbir manuel yapılandırma olmadan I2P'yi kullanabilir.

## I2P Router'ınızı yapılandırma

Bitcoin'e anonim bağlantı sağlamak için bir I2P Router kurarken, SAM API'nin etkinleştirilmesi gerekir. Java I2P'de, http://127.0.0.1:7657/configclients adresine gidip "Start" düğmesine tıklayarak SAM Application Bridge'i başlatmalısınız. Ayrıca, "Run at Startup" kutusunu işaretleyip "Save Client Configuration." düğmesine tıklayarak SAM Application Bridge'i varsayılan olarak etkinleştirmek isteyebilirsiniz.

i2pd'de, SAM API normalde varsayılan olarak etkindir, ancak değilse, şunu ayarlamalısınız:

```
sam.enabled=true
```
i2pd.conf dosyanızda.

## Anonimlik ve Bağlantı için Bitcoin Düğümünüzün Yapılandırılması

Bitcoin'i anonim modda başlatmak hâlâ Bitcoin Veri Dizini'ndeki bazı yapılandırma dosyalarını düzenlemeyi gerektirir; bu dizin Windows'ta %APPDATA%\Bitcoin, Linux'ta ~/.bitcoin ve Mac OSX'te ~/Library/Application Support/Bitcoin/ şeklindedir. Ayrıca I2P desteğinin mevcut olması için en az 22.0.0 sürümü gerekir.

Bu talimatları izledikten sonra, I2P bağlantıları için I2P’yi ve .onion ile clearnet (açık internet) bağlantıları için Tor’u kullanan, böylece tüm bağlantılarınızın anonim olduğu özel bir Bitcoin düğümüne sahip olmalısınız. Kolaylık olması için, Windows kullanıcıları Başlat menüsünü açıp "Run." ifadesini arayarak Bitcoin Veri Dizini’ni açmalıdır. Run penceresinde "%APPDATA%\Bitcoin" yazın ve Enter tuşuna basın.

Bu dizinde "i2p.conf." adlı bir dosya oluşturun. Windows'ta, Windows'un dosyaya varsayılan bir dosya uzantısı eklemesini önlemek için, kaydederken dosya adının etrafına tırnak işaretleri eklediğinizden emin olun. Dosya, aşağıdaki I2P ile ilgili Bitcoin yapılandırma seçeneklerini içermelidir:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Ardından, "tor.conf." adlı başka bir dosya oluşturmalısınız. Dosya aşağıdaki Tor ile ilgili yapılandırma seçeneklerini içermelidir:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Son olarak, bu yapılandırma seçeneklerini Veri Dizini'nde bulunan ve "bitcoin.conf" adı verilen Bitcoin yapılandırma dosyanıza "dahil" etmeniz gerekecek. Bu iki satırı bitcoin.conf dosyanıza ekleyin:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Artık Bitcoin düğümünüz yalnızca anonim bağlantılar kullanacak şekilde yapılandırılmıştır. Uzak düğümlere doğrudan bağlantıları etkinleştirmek için, aşağıdakilerle başlayan satırları kaldırın:

```
onlynet=
```
Bitcoin düğümünüzün anonim olmasını gerektirmiyorsanız bunu yapabilirsiniz ve bu, anonim kullanıcıların Bitcoin ağının geri kalanına bağlanmasına yardımcı olur.
