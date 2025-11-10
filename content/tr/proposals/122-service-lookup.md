---
title: "Hizmet Arama"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Reddedildi"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Genel Bakış

Bu, tam anlamıyla her şeyin kabul edildiği bir netdb önerisidir. Ayrıca anycast olarak da bilinir. Bu, önerilen 4. LS2 alt türü olacaktır.


## Motivasyon

Amacınız çıkış proxy'nizi, GNS düğümünüzü, Tor geçidinizi veya bir Bittorrent DHT, imule, i2phex veya Seedless başlatıcısı vb. olarak tanıtmak olsaydı, bu bilgileri ayrı bir başlatma veya bilgi katmanı kullanmak yerine netDB'de saklayabilirdiniz.

Kimse sorumlu olmadığı için, devasa çoklu barındırma ile olduğu gibi imzalı resmi bir listeye sahip olamazsınız. Bu yüzden kaydınızı bir floodfill'e yayımlamanız yeterli olacaktır. Floodfill bunları toplayacak ve sorgulara yanıt olarak gönderecektir.


## Örnek

Hizmetiniz "GNS" olsaydı, floodfill'e bir veritabanı kaydı gönderirdiniz:

- "GNS"nin Hash'i
- hedef
- yayın tarihi
- son kullanma (iptal için 0)
- port
- imza

Biri bir arama yaptığında, bu kayıtların bir listesini geri alırlardı:

- "GNS"nin Hash'i
- Floodfill'in hash'i
- Zaman damgası
- kayıt sayısı
- kayıtların listesi
- floodfill'in imzası

Son kullanma süreleri nispeten uzun olacaktır, en azından saatler.


## Güvenlik etkileri

Dezavantajı, bunun Bittorrent DHT'ye veya daha da kötüsüne dönüşebilme olasılığıdır. En azından floodfill'ler depolamaları ve sorguları ciddi şekilde sınırlamalıdır. Daha yüksek sınırlamalar için onaylanmış hizmet adlarını beyaz listeye alabiliriz. Ayrıca beyaz listede olmayan hizmetleri tamamen yasaklayabiliriz.

Tabii ki, günümüzün netDB'si bile kötüye kullanıma açıktır. RI veya LS'ye benzer göründüğü ve imza doğrulandığı sürece netDB'de keyfi veri depolayabilirsiniz. Ancak bu, bunu çok daha kolay hale getirecektir.
