---
title: "StormyCloud Outproxy hizmetine nasıl geçilir"
date: 2022-08-04
author: "idk"
description: "StormyCloud Outproxy Service'e Nasıl Geçilir"
categories: ["general"]
API_Translate: doğru
---

## StormyCloud Outproxy Hizmetine Nasıl Geçilir

**Yeni, Profesyonel Bir Outproxy (dış vekil sunucu)**

Yıllardır, I2P, güvenilirliği giderek azalan tek bir varsayılan outproxy (dışa çıkış proxy'si) olan `false.i2p` ile hizmet alıyordu. Bu yükün bir kısmını almak için birkaç rakip ortaya çıkmış olsa da, çoğunlukla bir I2P gerçekleştirmesinin tüm istemcilerine varsayılan olarak hizmet vermeyi gönüllü olarak üstlenemiyorlar. Bununla birlikte, Tor çıkış düğümleri işleten profesyonel, kâr amacı gütmeyen bir kuruluş olan StormyCloud, I2P topluluğu üyeleri tarafından test edilmiş yeni, profesyonel bir outproxy hizmeti başlattı ve bu hizmet yaklaşan sürümde yeni varsayılan outproxy olacak.

**StormyCloud kimdir**

Kendi sözleriyle, StormyCloud şöyle:

> StormyCloud Inc'in misyonu: İnternet erişimini evrensel bir insan hakkı olarak savunmak. Bunu yaparken, grup kullanıcıların elektronik gizliliğini korur ve bilgiye sınırsız erişimi teşvik ederek, böylece fikirlerin sınırlar ötesinde serbestçe değişimini sağlayarak topluluk oluşturur. Bu hayati önemdedir çünkü dünyada olumlu bir fark yaratmak için kullanılabilecek en güçlü araç İnternettir.

> Donanım: Tüm donanımımız bize aittir ve şu anda bir Tier 4 veri merkezinde donanımımızı barındırıyoruz. Şu anda 10GBps uplink’imiz var ve çok fazla değişikliğe gerek kalmadan 40GBps’e yükseltme seçeneğimiz bulunuyor. Kendimize ait ASN (Otonom Sistem Numarası) ve IP space (IP adres alanı) mevcut (IPv4 & IPv6).

StormyCloud hakkında daha fazla bilgi edinmek için [web sitesini](https://www.stormycloud.org/) ziyaret edin.

Veya, onları [I2P](http://stormycloud.i2p/) üzerinde ziyaret edin.

**I2P'de StormyCloud Outproxy'ye (dış vekil sunucusu) geçiş**

StormyCloud outproxy'ye *bugün* geçmek için [the Hidden Services Manager](http://127.0.0.1:7657/i2ptunnel/edit?tunnel=0) (Gizli Servisler Yöneticisi) sayfasını ziyaret edebilirsiniz. Oraya ulaştığınızda, **Outproxies** ve **SSL Outproxies** değerlerini `exit.stormycloud.i2p` olarak değiştirmelisiniz. Bunu yaptıktan sonra, sayfanın en altına kadar kaydırın ve "Save" düğmesine tıklayın.

**StormyCloud'a teşekkürler**

Yüksek kaliteli outproxy (I2P dışa çıkış vekil sunucusu) hizmetlerini I2P ağı için gönüllü olarak sağlamayı üstlendiği için StormyCloud’a teşekkür etmek isteriz.
