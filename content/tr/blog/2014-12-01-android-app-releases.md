---
title: "Android uygulama sürümleri"
date: 2014-12-01
author: "str4d"
description: "I2P Android 0.9.17 ve Bote 0.3, web sitesinde, Google Play'de ve F-Droid'de yayınlandı."
categories: ["press"]
---

Android geliştirmemizle ilgili en son güncellemeleri paylaşmamın üzerinden epey zaman geçti ve bu arada birkaç I2P sürümü, bunlara karşılık gelen Android sürümleri olmadan yayımlandı. Nihayet, bekleyiş sona erdi!

## Yeni uygulama sürümleri

I2P Android ve Bote için yeni sürümler yayımlandı! Bunlar şu URL'lerden indirilebilir:

- [I2P Android 0.9.17](https://geti2p.net/en/download#android)
- [Bote 0.3](https://download.i2p.io/android/bote/releases/0.3/Bote.apk)

Bu sürümlerdeki başlıca değişiklik, Android’in yeni Material Design sistemine (Material tasarım sistemi) geçiştir. Material, diyelim ki “minimalist” tasarım becerilerine sahip (benim gibi) uygulama geliştiriciler için kullanması daha hoş uygulamalar geliştirmeyi çok daha kolay hale getirdi. I2P Android ayrıca alttaki I2P router’ını yeni yayımlanan 0.9.17 sürümüne güncelliyor. Bote, çok sayıda küçük iyileştirmenin yanı sıra birkaç yeni özellik getiriyor; örneğin artık QR kodları aracılığıyla yeni email destinations (e-posta hedefleri) ekleyebilirsiniz.

Son güncellememde belirttiğim gibi, uygulamaları imzalayan release key (yayın anahtarı) değişti. Bunun nedeni, I2P Android'in paket adını değiştirmemiz gerekmesiydi. Eski paket adı (`net.i2p.android.router`) Google Play'de zaten alınmıştı (kimin kullandığını hâlâ bilmiyoruz) ve I2P Android'in tüm dağıtımları için aynı paket adını ve imzalama anahtarını kullanmak istiyorduk. Bunu yapmak, bir kullanıcının uygulamayı önce I2P web sitesinden yükleyip, daha sonra web sitesi engellenirse Google Play üzerinden güncelleyebilmesi anlamına geliyor. Android işletim sistemi, paket adı değiştiğinde bir uygulamayı tamamen farklı kabul eder; bu yüzden bu fırsatı değerlendirerek imzalama anahtarının gücünü artırdık.

Yeni imzalama anahtarının parmak izi (SHA-256):

```
AD 1E 11 C2 58 46 3E 68 15 A9 86 09 FF 24 A4 8B C0 25 86 C2 36 00 84 9C 16 66 53 97 2F 39 7A 90
```
## Google Play

Birkaç ay önce, oradaki yayımlama sürecini test etmek için Norveç'te Google Play'de hem I2P Android'i hem de Bote'u yayımladık. Her iki uygulamanın da artık [Privacy Solutions](https://privacysolutions.no/) tarafından dünya genelinde yayımlandığını duyurmaktan memnuniyet duyuyoruz. Uygulamalara şu URL'lerden ulaşabilirsiniz:

- [I2P on Google Play](https://play.google.com/store/apps/details?id=net.i2p.android)
- [Bote on Google Play](https://play.google.com/store/apps/details?id=i2p.bote.android)

Küresel sürüm, çevirilerimizin bulunduğu ülkelerden başlayarak birkaç aşamada gerçekleştiriliyor. Buna kayda değer bir istisna Fransa’dır; kriptografik koda ilişkin ithalat düzenlemeleri nedeniyle bu uygulamaları henüz Google Play France üzerinden dağıtamıyoruz. Bu, TextSecure ve Orbot gibi diğer uygulamaları da etkileyen aynı sorundur.

## F-Droid

Sizi unuttuğumuzu sanmayın, F-Droid kullanıcıları! Yukarıdaki iki konuma ek olarak, kendi F-Droid depomuzu kurduk. Bu yazıyı telefonunuzda okuyorsanız, F-Droid'e eklemek için [buraya tıklayın](https://f-droid.i2p.io/repo?fingerprint=68E76561AAF3F53DD53BA7C03D795213D0CA1772C3FAC0159B50A5AA85C45DC6) (bu yalnızca bazı Android tarayıcılarında çalışır). Ya da, aşağıdaki URL'yi F-Droid depo listenize manuel olarak ekleyebilirsiniz:

https://f-droid.i2p.io/repo

Depo imzalama anahtarının parmak izini (SHA-256) elle doğrulamak veya depoyu eklerken girmek isterseniz, işte burada:

```
68 E7 65 61 AA F3 F5 3D D5 3B A7 C0 3D 79 52 13 D0 CA 17 72 C3 FA C0 15 9B 50 A5 AA 85 C4 5D C6
```
Ne yazık ki ana F-Droid deposundaki I2P uygulaması, F-Droid bakımcımız ortadan kaybolduğu için güncellenmedi. Bu ikili (binary) depoyu sürdürerek F-Droid kullanıcılarımızı daha iyi destekleyebileceğimizi ve onları güncel tutabileceğimizi umuyoruz. I2P'yi ana F-Droid deposundan zaten yüklediyseniz, yükseltmek istiyorsanız onu kaldırmanız gerekecek; çünkü imzalama anahtarı farklı olacaktır. F-Droid depomuzdaki uygulamalar, web sitemizde ve Google Play'de sunulanlarla aynı APK'lerdir; bu nedenle gelecekte bu kaynakların herhangi birini kullanarak yükseltebileceksiniz.
