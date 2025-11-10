---
title: "NTCP Gizleme"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Genel Bakış

Bu öneri, NTCP taşımacılığını otomatik tanımlamaya karşı direncini artırmak için yenilemeye yönelik.

## Motivasyon

NTCP verileri, ilk mesajdan sonra şifrelenir (ve ilk mesaj rastgele veri gibi görünür), böylece protokol tanımlaması "yük analizi" yoluyla engellenir. Yine de "akış analizi" yoluyla protokol tanımlamasına karşı savunmasızdır. Bunun nedeni, ilk 4 mesajın (örneğin, el sıkışma) sabit uzunlukta olmasıdır (288, 304, 448 ve 48 bayt).

Her bir mesaja rastgele miktarda rastgele veri ekleyerek, bunu çok daha zor hale getirebiliriz.

## NTCP'ye Yapılan Değişiklikler

Bu oldukça ağır bir değişiklik, ancak DPI ekipmanları tarafından tespit edilmesini engeller.

288 baytlık mesaj 1'in sonuna şu veriler eklenecektir:

- 514 baytlık ElGamal şifrelenmiş blok
- Rastgele dolgu

ElG bloğu Bob'un açık anahtarına şifrelenmiştir. 222 bayta çözüldüğünde, içerir:
- 214 bayt rastgele dolgu
- 4 bayt 0 ayrılmış
- 2 bayt takip edecek dolgu uzunluğu
- 2 bayt protokol versiyonu ve bayraklar

Mesaj 2-4'te, dolgunun son iki baytı bundan sonra gelecek olan daha fazla dolgunun uzunluğunu gösterecektir.

ElG bloğunun mükemmel ileri gizlilik sağlamadığını, ancak içinde ilgi çekici bir şey olmadığını unutmayın.

Eğer 514 bayt çok fazlaysa, ElG kütüphanemizi daha küçük veri boyutlarını şifrelemesi için değiştirebilir miyiz? Her NTCP kurulumunda ElG şifrelemesi fazla mı?

Bu desteğin netdb RouterAddress içinde "version=2" seçeneği ile reklamı yapılacaktır. Eğer Mesaj 1'de yalnızca 288 bayt alınırsa, Alice'in sürüm 1 olduğu varsayılacak ve sonraki mesajlarda dolgu gönderilmeyecektir. Brandon'a göre bir MITM'in IP'yi 288 bayta böldüğü (çok olası olmasa da) iletişimi engelleyebilir.
