---
title: "Transport Genel Bakış"
description: "Router'lar arası nokta-nokta iletişim için I2P'nin transport katmanına genel bakış"
slug: "transport"
aliases:
  - "/tr/transport"
  - "/tr/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## I2P'de Transport'lar

I2P'de "transport" (taşıma), iki router arasında doğrudan, noktadan noktaya iletişim için kullanılan bir yöntemdir. Transport'lar, dış saldırganlara karşı gizlilik ve bütünlük sağlamalı, aynı zamanda iletişim kurulan router'ın belirli bir mesajı alması gereken router olduğunu doğrulamalıdır.

I2P aynı anda birden fazla taşıma protokolünü destekler. Şu anda uygulanmış üç taşıma protokolü bulunmaktadır:

1. [NTCP](/docs/legacy/ntcp/), bir Java New I/O (NIO) TCP taşıma protokolü
2. [SSU](/docs/legacy/ssu/), veya Güvenli Yarı-güvenilir UDP
3. [NTCP2](/docs/specs/ntcp2/), NTCP'nin yeni bir sürümü

Her biri kimlik doğrulama, akış kontrolü, onaylar ve yeniden iletim ile bir "bağlantı" paradigması sağlar.

- [I2NP](/docs/specs/i2np/) mesajlarının güvenilir teslimatı. Transport protokolleri YALNIZCA I2NP mesaj teslimatını destekler. Bunlar genel amaçlı veri kanalları değildir.
- Mesajların sıralı teslimatı tüm transport protokolleri tarafından garanti edilmez.
- Router'ın global iletişim bilgisi (RouterInfo) olarak yayınladığı, her transport için bir veya daha fazla router adresi setinin korunması. Her transport bu adreslerden birini kullanarak bağlanabilir; bu adresler IPv4 veya (0.9.8 sürümünden itibaren) IPv6 olabilir.
- Her giden mesaj için en iyi transport'un seçilmesi
- Giden mesajların öncelik sırasına göre kuyruğa alınması
- Router yapılandırmasına göre hem giden hem de gelen bant genişliği sınırlaması
- Transport bağlantılarının kurulması ve sonlandırılması
- Noktadan-noktaya iletişimin şifrelenmesi
- Her transport için bağlantı sınırlarının korunması, bu sınırlar için çeşitli eşiklerin uygulanması ve duruma dayalı operasyonel değişiklikler yapabilmesi için eşik durumunun router'a iletilmesi
- UPnP (Universal Plug and Play) kullanarak güvenlik duvarı port açma
- İşbirlikçi NAT/Güvenlik Duvarı geçişi
- UPnP, gelen bağlantıları inceleme ve ağ cihazlarını listeleme dahil çeşitli yöntemlerle yerel IP tespiti
- Transport'lar arasında güvenlik duvarı durumu ve yerel IP'nin, ve bunlardaki değişikliklerin koordinasyonu
- Güvenlik duvarı durumu ve yerel IP'nin, ve bunlardaki değişikliklerin router'a ve kullanıcı arayüzüne iletilmesi
- NTP'ye yedek olarak router'ın saatini periyodik olarak güncellemek için kullanılan konsensüs saatinin belirlenmesi
- Her peer için durumun korunması; bağlı olup olmadığı, yakın zamanda bağlı olup olmadığı ve son denemede erişilebilir olup olmadığı dahil
- Yerel kural setine göre geçerli IP adreslerinin nitelendirilmesi
- Router tarafından tutulan otomatik ve manuel yasaklı peer listelerinin onurlandırılması ve bu peer'lara giden ve gelen bağlantıların reddedilmesi

---

I2P'deki transport alt sistemi aşağıdaki hizmetleri sağlar:

## Transport Hizmetleri

---

- Bir router yayınlanmış adreslere sahip değildir, bu nedenle "gizli" olarak kabul edilir ve gelen bağlantıları alamaz
- Bir router güvenlik duvarının arkasındadır ve bu nedenle NAT geçişinde yardımcı olacak işbirlikçi eşler veya "introducers" listesi içeren bir SSU adresi yayınlar (ayrıntılar için [SSU spesifikasyonuna](/docs/legacy/ssu/) bakın)
- Bir router güvenlik duvarının arkasında değildir veya NAT portları açıktır; doğrudan erişilebilir IP ve portları içeren hem NTCP hem de SSU adreslerini yayınlar.

Transport alt sistemi, her biri bir transport yöntemi, IP ve port listeleyen bir dizi router adresi tutar. Bu adresler, ilan edilen iletişim noktalarını oluşturur ve router tarafından netDb'ye yayınlanır. Adresler ayrıca rastgele bir dizi ek seçenek içerebilir.

## Aktarım Adresleri

Her taşıma yöntemi birden fazla router adresi yayınlayabilir.

Tipik senaryolar şunlardır:

---

- Transport tercihlerinin yapılandırması
- Transport'un eşe zaten bağlı olup olmadığı
- Mevcut bağlantı sayısının çeşitli bağlantı limiti eşikleriyle karşılaştırılması
- Eşe yapılan son bağlantı denemelerinin başarısız olup olmadığı
- Mesajın boyutu, çünkü farklı transport'lar farklı boyut limitlerine sahiptir
- Eşin RouterInfo'sunda ilan ettiği şekilde, o transport için gelen bağlantıları kabul edip edemeyeceği
- Bağlantının dolaylı (introducers gerektiren) veya doğrudan olup olmayacağı
- Eşin RouterInfo'sunda ilan ettiği transport tercihi

Taşıma sistemi yalnızca [I2NP mesajları](/docs/specs/i2np/) iletir. Herhangi bir mesaj için seçilen taşıma, üst katman protokollerinden ve içerikten bağımsızdır (router veya istemci mesajları, harici bir uygulamanın I2P'ye bağlanmak için TCP veya UDP kullanıp kullanmadığı, üst katmanın [streaming kütüphanesi](/docs/api/streaming/) veya [datagramları](/docs/api/datagrams/) kullanıp kullanmadığı, vb.).

## Taşıma Seçimi

Her giden mesaj için, aktarım sistemi her aktarımdan "teklif" ister. En düşük (en iyi) değeri teklif eden aktarım, teklifi kazanır ve mesajı teslim etmek üzere alır. Bir aktarım teklif vermeyi reddedebilir.

Bir transport'un teklif verip vermeyeceği ve hangi değerle vereceği çok sayıda faktöre bağlıdır:

Genel olarak, bid değerleri iki router'ın herhangi bir zamanda yalnızca tek bir transport ile bağlı olacağı şekilde seçilir. Ancak bu bir gereklilik değildir.

- TLS/SSH benzeri bir taşıma protokolü
- Diğer tüm router'lar tarafından erişilemeyen router'lar için "dolaylı" taşıma protokolü ("kısıtlı rotalar"ın bir türü)
- Tor-uyumlu takılabilir taşıma protokolleri

---

Ek aktarım protokolleri geliştirilebilir, bunlar şunları içerir:

## Yeni Aktarım Yöntemleri ve Gelecekteki Çalışmalar

Her transport için varsayılan bağlantı sınırlarını ayarlama çalışmaları devam ediyor. I2P, herhangi bir router'ın diğer herhangi bir router'a bağlanabileceği varsayımıyla "mesh ağ" olarak tasarlanmıştır. Bu varsayım, bağlantı sınırlarını aşan router'lar ve kısıtlayıcı durum firewall'ları arkasında bulunan router'lar (kısıtlı rotalar) tarafından bozulabilir.

- TLS/SSH benzeri bir taşıma yöntemi
- Tüm diğer yönlendiriciler tarafından erişilemeyen yönlendiriciler için "dolaylı" bir taşıma yöntemi (sınırlı yolların bir biçimi)
- Tor ile uyumlu eklenebilir taşıma yöntemleri

Mevcut bağlantı limitleri, NTCP bağlantısı için bellek gereksinimlerinin SSU'ya göre daha yüksek olduğu varsayımına dayanarak, SSU için NTCP'ye göre daha yüksek tutulmuştur. Ancak, NTCP tamponları kısmen çekirdekte ve SSU tamponları Java heap'inde bulunduğundan, bu varsayımı doğrulamak zordur.

[Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) belgesini analiz edin ve taşıma katmanı dolgulamasının (padding) durumu nasıl iyileştirebileceğini görün.

[Protokol Gizlemeyi Kırmak ve İyileştirmek](http://www.iis.se/docs/hjelmvik_breaking.pdf) adlı çalışmayı inceleyin ve taşıma katmanı dolgusunun durumları nasıl iyileştirebileceğine bakın.
