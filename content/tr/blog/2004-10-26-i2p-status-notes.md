---
title: "2004-10-26 tarihli I2P Durum Notları"
date: 2004-10-26
author: "jr"
description: "Ağ kararlılığı, streaming kitaplığının geliştirilmesi, mail.i2p ilerlemesi ve BitTorrent'teki gelişmeler hakkında haftalık I2P durum güncellemesi"
categories: ["status"]
---

Selam millet, haftalık güncelleme zamanı

## Dizin

1. Net status
2. Streaming lib
3. mail.i2p progress
4. ???

## 1) Ağ durumu

Nazara değdirmek istemem ama, son bir haftadır ağ neredeyse eskisi gibi - irc için oldukça istikrarlı, eepsites(I2P Sites) güvenilir biçimde yükleniyor, ancak büyük dosyalar hâlâ çoğu zaman kaldığı yerden devam ettirmeyi gerektiriyor. Özetle, bildirilecek yeni bir şey yok, bildirilecek yeni bir şey olmadığı gerçeği dışında.

Ah, bulduğumuz bir şey de şuydu: Jetty HTTP resume (kaldığı yerden devam etme) özelliğini desteklese de, bunu yalnızca HTTP 1.1 için yapıyor. Bu çoğu tarayıcı ve indirme aracı için sorun değil, *hariç* wget - wget, devam isteğini HTTP 1.0 olarak gönderiyor. Bu yüzden, büyük dosyaları indirirken curl veya HTTP 1.1 resume destekleyen başka bir araç kullanın (derinlemesine inceleyip bir çözüm buldukları için duck ve ardvark'a teşekkürler!)

## 2) Akış kitaplığı

Ağ oldukça kararlı olduğundan, zamanımın neredeyse tamamını yeni akış kitaplığı üzerinde çalışmaya harcadım. Henüz tamamlanmamış olsa da, önemli ilerleme kaydedildi - temel senaryoların hepsi gayet iyi çalışıyor, kayan pencereler self-clocking (kendinden zamanlama) açısından iyi iş çıkarıyor ve yeni kitaplık, istemci açısından eskisinin yerine bir drop-in replacement (doğrudan yerine konulabilir ikame) olarak çalışıyor (yine de iki akış kitaplığı birbirleriyle konuşamıyor).

Son birkaç gündür daha ilginç bazı senaryolar üzerinde çalışıyorum. Bunların en önemlisi gecikmeli ağ; bunu, alınan mesajlara gecikmeler enjekte ederek simüle ediyoruz - ya basit bir 0-30s rastgele gecikme ya da kademeli bir gecikme (zamanın %80'inde 0-10s gecikme, %10'unda 10-20s gecikme, %5'inde 20-30s, %3'ünde 30-40s, %4'ünde 40-50s). Bir diğer önemli test ise mesajların rastgele düşürülmesi oldu - bu I2P üzerinde yaygın olmamalı, ancak bununla başa çıkabilmeliyiz.

Genel performans oldukça iyi, ancak bunu canlı ağa devreye almadan önce hâlâ yapılacak çok iş var. Bu güncelleme muazzam derecede güçlü olduğu için 'tehlikeli' olacak - eğer berbat bir şekilde yanlış yapılırsa, bir anda kendi kendimizi DDoS edebiliriz, ama doğru yapılırsa, şöyle diyeyim, çok büyük bir potansiyel var (az vaat et, fazlasını sun).

Bunu söylemişken ve ağ oldukça 'kararlı durumda' olduğundan, yeterince test edilmemiş bir şeyi yayınlamak için acelem yok. Yeni bir haber olduğunda paylaşacağım.

## 3) mail.i2p ilerlemesi

postman ve ekibi i2p üzerinden e-posta konusunda uzun zamandır yoğun biçimde çalışıyorlar (bkz. www.postman.i2p) ve yolda heyecan verici gelişmeler var - belki postman'ın bizim için bir güncellemesi vardır?

Bu arada, webmail arayüzü taleplerini anlıyor ve hak veriyorum, ancak postman şu anda posta sisteminin arka ucunda bazı güzel geliştirmeler üzerinde çalışmakla meşgul. Bununla birlikte bir alternatif de kendi web sunucunuza *yerel olarak* bir webmail arayüzü kurmaktır - JSP/servlet tabanlı webmail yazılımları mevcut. Bu da, örneğin `http://localhost:7657/mail/` adresinde kendi yerel webmail arayüzünüzü çalıştırmanıza olanak tanır.

Ortalarda pop3 hesaplarına erişmek için bazı açık kaynak betikler olduğunu biliyorum, bu da işin yarısını hallediyor - belki birileri pop3 ve kimlik doğrulamalı SMTP’yi destekleyenlerini bulmak için etrafa bir göz atabilir mi? hadi ama, yapmak istediğini biliyorsun!

## 4) ???

Tamam, şimdilik söyleyeceklerim bu kadar - birkaç dakika içinde toplantıya uğrayın ve neler olup bittiğini bize haber verin.

=jr
