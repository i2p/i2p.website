---
title: "BEP9 Bilgi Kurtarma"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Ölü"
thread: "http://zzz.i2p/topics/860"
---

## Genel Bakış

Bu öneri, BEP9'un I2P uygulamasına tam bilgi kurtarma eklemeyi ele almaktadır.

## Motivasyon

BEP9, torrent dosyasının tamamını göndermez ve böylece birkaç önemli sözlük öğesi kaybolur ve torrent dosyalarının toplam SHA1'ini değiştirir. Bu, maggot bağlantıları için kötü ve çünkü önemli bilgiler kaybolur, kötü bir durumdur. İzleyici listeleri, yorumlar ve diğer ek veriler kaybolur. Bu bilgiyi kurtarmanın bir yolu önemlidir ve torrent dosyasına mümkün olduğunca az ek bilgiyi eklemelidir. Aynı zamanda döngüsel bağımlı olmamalıdır. Kurtarma bilgisi mevcut istemcileri hiçbir şekilde etkilememelidir. İzleyicisiz olan torrentler (izleyici URL'si kelimenin tam anlamıyla 'trackerless') ek alan içermez, çünkü onlar maggot keşfi ve indirme protokolünü kullanmaya özeldir, bu da ilk başta bilgiyi asla kaybetmez.

## Çözüm

Yapılması gereken tek şey kaybedilecek bilgiyi sıkıştırmak ve info sözlüğünde depolamaktır.

### Uygulama
1. Normal bilgi sözlüğünü oluşturun.
2. Ana sözlüğü oluşturun ve info girişini dışarıda bırakın.
3. Ana sözlüğü bencode yapın ve gzip ile sıkıştırın.
4. Sıkıştırılmış ana sözlüğü bilgi sözlüğüne ekleyin.
5. Ana sözlüğe bilgi ekleyin.
6. Torrent dosyasını yazın.

### Kurtarma
1. Bilgi sözlüğündeki kurtarma girişini açın.
2. Kurtarma girişini bendocode ile çözün.
3. Bilgi sözlüğünü kurtarılan sözlüğe ekleyin.
4. Maggot-farkındalıklı istemciler için, artık SHA1'in doğru olduğunu doğrulayabilirsiniz.
5. Kurtarılan torrent dosyasını yazın.

## Tartışma

Yukarıda belirtilen yöntemi kullanarak, torrent dosyasının boyut artışı çok küçüktür, tipik olarak 200 ila 500 bayttır. Robert, yeni bilgi sözlüğü girişi ile gönderecek ve bu kapatılamayacak. İşte yapı:

```
ana sözlük {
    İzleyici dizeleri, yorumlar, vb...
    info : {
        info sözlüğü ve tüm diğer
        bilgileri çıkarılmış gzip edilmiş ana bencode sözlük
    }
}
```
