---
title: "Sarımsakta Birden Fazla Veri Tanesi Paketleme"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Araştırma Gerekiyor"
thread: "http://zzz.i2p/topics/1797"
---

## Genel Bakış

Bu öneri, uçtan uca Sarımsak Mesajı içinde birden fazla Veri Sarımsak Tanesi
gönderme hakkındadır, sadece bir tane yerine.


## Motivasyon

Belli değil.


## Gerekli Değişiklikler

Değişiklikler OCMOSJ ve ilgili yardımcı sınıflarda, ve ClientMessagePool'da
olacaktır. Şu anda bir sıra olmadığından, yeni bir sıra ve biraz gecikme
gerekecek. Herhangi bir paketleme, düşmeyi en aza indirmek için maksimum sarımsak
boyutuna uymak zorunda kalacaktır. Belki 3KB? Bunun ne sıklıkla kullanılacağını
ölçmek için önce şeyleri enstrüman etmek isteyebiliriz.


## Düşünceler

Bu durumun herhangi bir faydalı etkisi olup olmayacağı belirsizdir, çünkü
akış zaten paketleme yapıyor ve en uygun MTU'yu seçiyor. Paketleme, mesaj
boyutunu artırır ve üstel düşme olasılığını artırır.

İstisna, I2CP katmanında gziple sıkıştırılmış sıkıştırılmamış içeriktir. Ancak
HTTP trafiği zaten üst katmanda sıkıştırılmıştır ve Bittorrent verisi genellikle
sıkıştırılamaz. Bu ne bırakıyor? I2pd şu anda x-i2p-gzip sıkıştırmasını yapmıyor,
bu yüzden burada çok daha fazla yardımcı olabilir. Ancak etiketlerin tükenmemesi
hedefi, akış kütüphanesinde doğru pencereleme uygulaması ile daha iyi çözülür.


## Uyumluluk

Bu geriye dönük uyumludur, çünkü sarımsak alıcısı zaten aldığı tüm taneleri
işleyecektir.
