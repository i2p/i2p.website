---
title: "Çift Yönlü Tüneller"
number: "119"
author: "orjinal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Araştırma Gerekiyor"
thread: "http://zzz.i2p/topics/2041"
---

## Genel Bakış

Bu öneri, I2P'de çift yönlü tünellerin uygulanması hakkındadır.


## Motivasyon

i2pd, şimdilik sadece diğer i2pd yönlendiricileri aracılığıyla çift yönlü tüneller sunacak. Ağ için bunlar, düzenli giriş ve çıkış tünelleri olarak görünecek.


## Tasarım

### Amaçlar

1. Tünel Oluşturma mesajlarının sayısını azaltarak ağ ve CPU kullanımını azaltmak
2. Bir katılımcının ayrılıp ayrılmadığını anında bilme yeteneği
3. Daha doğru profilleme ve istatistikler
4. Ara boşluklar olarak diğer karanlık ağları kullanma


### Tünel değişiklikleri

TunnelBuild
```````````
Tüneller, giriş tünelleriyle aynı şekilde inşa edilir. Yanıt mesajı gerekmemektedir.
"giriş" adı verilen, aynı zamanda IBGW ve OBEP olarak hizmet veren bir katılımcı türü vardır. Mesajın formatı VaribaleTunnelBuild ile aynıdır ancak ClearText farklı alanlar içerir::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Ayrıca, sonraki düğümün hangi karanlık ağa ait olduğunu belirten bir alan ve eğer I2P değilse ek bilgiler içerecektir.

TunnelTermination
`````````````````
Bir eş ayrılmak isterse, TunnelTermination mesajları oluşturur, bunları katman anahtarı ile şifreler ve "in" yönünde gönderir. Bir katılımcı böyle bir mesaj alırsa, kendi katman anahtarı ile tekrar şifreler ve bir sonraki eşe gönderir. Mesaj tünel sahibine ulaştığında eşlerden eşlere şifre çözümler ve şifresiz mesajı elde eder. Hangi katılımcının ayrıldığını öğrenir ve tüneli sonlandırır.
