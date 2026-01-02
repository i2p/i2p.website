---
title: "Bakımcınızla Tanışın: StormyCloud"
date: 2022-09-07
author: "sadie"
description: "StormyCloud Outproxy'nin bakımcılarıyla bir röportaj"
categories: ["general"]
---

## StormyCloud Inc. ile bir görüşme

En son [I2P Java sürümü](https://geti2p.net/en/blog/2022/08/22/1.9.0-Release) ile birlikte, mevcut outproxy (çıkış vekil sunucusu) olan false.i2p, yeni I2P kurulumları için yeni StormyCloud outproxy ile değiştirildi. Router’larını güncelleyen kişiler için, Stormycloud hizmetine geçiş hızlıca yapılabilir.

Hidden Services Manager'da hem Outproxies hem de SSL Outproxies alanlarını exit.stormycloud.i2p olarak ayarlayın ve sayfanın altındaki kaydet düğmesine tıklayın.

## StormyCloud Inc kimdir?

**StormyCloud Inc.'nin Misyonu**

İnternet erişimini evrensel bir insan hakkı olarak savunmak. Bunu yaparak, grup kullanıcıların elektronik gizliliğini korur ve bilgiye sınırsız erişimi teşvik edip böylece fikirlerin sınırlar ötesinde özgürce alışverişini sağlayarak topluluk oluşturur. Bu hayati önemdedir; çünkü dünyada olumlu bir fark yaratmak için elimizdeki en güçlü araç İnternettir.

**Vizyon Bildirimi**

Evrendeki herkese özgür ve açık İnternet sağlamada öncü olmak, çünkü İnternet erişimi temel bir insan hakkıdır ([https://stormycloud.org/about-us/](https://stormycloud.org/about-us/))

Dustin ile merhaba demek ve gizlilik, StormyCloud gibi hizmetlere duyulan ihtiyaç ve şirketi I2P'ye çeken şey hakkında daha fazla konuşmak için görüştüm.

**StormyCloud'u başlatma fikrine ne ilham verdi?**

2021’in sonlarıydı, /r/tor subreddit’indeydim. Tor’un nasıl kullanılacağına dair bir başlıkta yanıt veren biri, ailesiyle iletişimde kalmak için Tor’a güvendiğinden bahsediyordu. Ailesi Amerika Birleşik Devletleri’nde yaşıyordu, ancak kendisi o sırada internet erişiminin çok kısıtlı olduğu bir ülkede yaşıyordu. Kiminle iletişim kurduğuna ve ne söylediğine çok dikkatli olması gerekiyordu. Bu nedenlerle Tor’a güveniyordu. Ben de insanlarla korku ya da kısıtlama olmadan nasıl iletişim kurabildiğimi ve bunun herkes için de böyle olması gerektiğini düşündüm.

StormyCloud'un amacı, bunu yapabilmeleri için olabildiğince çok insana yardımcı olmaktır.

**StormyCloud'u hayata geçirirken karşılaşılan bazı zorluklar neler oldu?**

Maliyet — akıl almaz derecede yüksek. Yaptığımız işin ölçeği ev ağında yapılabilecek bir şey olmadığı için veri merkezi seçeneğini tercih ettik. Ekipman giderleri ve tekrarlayan barındırma maliyetleri var.

Kâr amacı gütmeyen kuruluşu kurma sürecinde, Emerald Onion'ın izinden gittik ve bazı belgeleri ile çıkardıkları derslerden yararlandık. Tor topluluğunun çok yararlı pek çok kaynağı mevcuttur.

**Hizmetlerinize yönelik tepki nasıl oldu?**

Temmuz ayında tüm hizmetlerimiz genelinde 1,5 milyar DNS sorgusu karşıladık. İnsanlar herhangi bir kayıt tutulmamasını takdir ediyor. Veri zaten mevcut değil ve insanlar bunu seviyor.

**outproxy (dış vekil sunucu) nedir?**

Outproxy (dışa çıkış vekil sunucusu), Tor'un çıkış düğümlerine benzer; clearnet (normal internet) trafiğinin I2P ağı üzerinden aktarılabilmesini sağlar. Başka bir deyişle, I2P kullanıcılarının internete I2P ağının sağladığı güvenlik üzerinden erişmesine olanak tanır.

**StormyCloud I2P Outproxy'yi (çıkış vekil sunucusu) özel kılan nedir?**

Öncelikle multi-homed (birden fazla ağ bağlantısına sahip) durumdayız; bu da outproxy (I2P'den clearnet'e çıkış vekili) trafiğini sunan birkaç sunucumuz olduğu anlamına gelir. Bu, hizmetin topluluk için her zaman erişilebilir olmasını sağlar. Sunucularımızdaki tüm günlükler her 15 dakikada bir silinir. Bu, hem kolluk birimlerinin hem de bizim herhangi bir veriye erişemememizi sağlar. Outproxy üzerinden Tor .onion bağlantılarını ziyaret etmeyi destekliyoruz ve outproxy hizmetimiz oldukça hızlıdır.

**Gizliliği nasıl tanımlarsınız? Yetki aşımı ve veri işleme konusunda gördüğünüz bazı sorunlar nelerdir?**

Gizlilik, yetkisiz erişime karşı korunmuş olmaktır. Şeffaflık önemlidir; örneğin opt-in (kullanıcının açık onay vererek katılması) — buna GDPR gereklilikleri örnektir.

Konum verilerine [mahkeme kararı olmaksızın erişim](https://www.eff.org/deeplinks/2022/08/fog-revealed-guided-tour-how-cops-can-browse-your-location-data) için kullanılan verileri istifleyen büyük şirketler var. İnsanların özel olduğunu düşündüğü ve öyle de olması gereken alanlara, örneğin fotoğraflara veya mesajlara, teknoloji şirketlerinin aşırı müdahalesi var.

İletişiminizi nasıl güvende tutacağınız ve bunun için hangi araçların ya da uygulamaların yardımcı olacağı konusunda bilgilendirme çalışmalarını sürdürmek önemlidir. Mevcut tüm bilgilerle nasıl etkileşim kurduğumuz da önemlidir. Güvenmeli, ama doğrulamalıyız.

**I2P, StormyCloud'un Misyon ve Vizyon Beyanı ile nasıl uyar?**

I2P açık kaynaklı bir projedir ve sunduğu özellikler StormyCloud Inc.'in misyonuyla uyumludur. I2P, trafik ve iletişim için bir gizlilik ve koruma katmanı sağlar ve proje, herkesin gizlilik hakkı olduğuna inanır.

Tor topluluğundaki insanlarla konuşurken 2022’nin başlarında I2P’den haberdar olduk ve projenin yaptıklarından hoşlandık. Tor’a benzer görünüyordu.

I2P’yi ve yeteneklerini tanıtırken, güvenilir bir outproxy (çıkış vekil sunucusu) gereksinimi olduğunu gördük. Outproxy hizmetini oluşturmak ve sağlamaya başlamak için I2P topluluğundaki kişilerden çok büyük destek aldık.

**Sonuç**

Çevrimiçi yaşamlarımızda özel kalması gerekenlerin gözetlenmesine dair farkındalık ihtiyacı sürüyor. Her türlü veri toplama rızaya dayalı olmalı ve mahremiyet varsayılan olmalıdır.

Trafiğimizin ya da iletişimimizin rızamız olmadan izlenmeyeceğine güvenemediğimiz durumlarda, neyse ki tasarımı gereği trafiği anonimleştiren ve konumlarımızı gizleyen ağlara erişebiliyoruz.

İhtiyaç duyduklarında insanların internete daha güvenli erişebilmesi için Tor ve I2P için outproxies (I2P dış proxy'leri) veya düğümler sağlayan StormyCloud'a ve herkese teşekkür ederim. Herkes için daha sağlam bir gizlilik ekosistemi oluşturmak üzere bu birbirini tamamlayan ağların yetenekleri arasında köprüler kuran daha fazla insan görmeyi dört gözle bekliyorum.

StormyCloud Inc.'in hizmetleri hakkında daha fazla bilgi edinmek için [https://stormycloud.org/](https://stormycloud.org/) adresini ziyaret edin ve [https://stormycloud.org/donate/](https://stormycloud.org/donate/) üzerinden bağış yaparak çalışmalarına destek olun.
