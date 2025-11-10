---
title: "Şifreli LeaseSet"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Genel Bakış

Bu öneri, LeaseSet'lerin şifrelenme mekanizmasının yeniden tasarlanması hakkında.


## Motivasyon

Mevcut şifreli LS korkunç ve güvensiz. Bunu ben tasarladım ve uyguladım.

Nedenler:

- AES CBC şifreli
- Herkes için tek AES anahtarı
- Lease tarihlerinin süresi hala ortada
- Şifreleme genel anahtarı hala ortada


## Tasarım

### Hedefler

- Her şeyin opak hale getirilmesi
- Her alıcı için anahtarlar


### Strateji

GPG/OpenPGP'ye benzer şekilde yapın. Her alıcı için simetrik bir anahtarı asimetrik olarak şifreleyin. Veri, bu asimetrik anahtarla çözülecek. Bkz. örneğin [RFC-4880-S5.1]_
Eğer küçük ve hızlı bir algoritma bulabilirsek.

Küçük ve hızlı olan bir asimetrik şifreleme bulmak zor. ElGamal 514 bayt'ta bu durumda biraz sıkıntılı. Daha iyisini yapabiliriz.

Bkz. örneğin http://security.stackexchange.com/questions/824...

Bu, az sayıda alıcı (veya aslında, anahtarlar) için çalışır; yine de anahtarları isterseniz birden fazla kişiye dağıtabilirsiniz.


## Şartname

- Hedef
- Yayınlanma zaman damgası
- Süre sonu
- Bayraklar
- Verinin uzunluğu
- Şifreli veri
- İmza

Şifreli veriler, bazı şifreleme türü belirleyicileri ile öne eklenebilir veya eklenmeyebilir.


## Referanslar

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
