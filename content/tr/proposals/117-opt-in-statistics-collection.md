---
title: "İsteğe Bağlı İstatistik Toplama"
number: "117"
author: "zab"
created: "2015-11-04"
lastupdated: "2015-11-04"
status: "Taslak"
thread: "http://zzz.i2p/topics/1981"
---

## Genel Bakış

Bu öneri, ağ istatistikleri için isteğe bağlı bir otomatik raporlama sistemi hakkında.

## Motivasyon

Şu anda, birkaç ağ parametresi tahminle belirlenmiştir. Bunların bazılarının
ağın genel performansını hız, güvenilirlik gibi açılardan iyileştirmek için
ayarlanabileceği düşünülmektedir. Ancak, yeterli araştırma yapılmadan bunların
değiştirilmesi oldukça risklidir.

## Tasarım

Yönlendirici, ağ genelindeki özellikleri analiz etmek için kullanılabilecek geniş
bir istatistik koleksiyonunu destekler. İhtiyacımız olan şey, bu istatistikleri
merkezi bir yerde toplayan otomatik bir raporlama sistemidir. Doğal olarak, bu
isteğe bağlı olacaktır, çünkü anonimliği büyük ölçüde yok eder. (Gizlilik
dostu istatistikler zaten stats.i2p adresine raporlanmaktadır) Genel bir
örnek olarak, 30.000 büyüklüğündeki bir ağ için, 300 raporlayan yönlendiriciden
oluşan bir örneklem yeterince temsil edici olabilir.
