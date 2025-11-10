---
title: "I2P Yaz Geliştirme 2017: Daha Fazla Hız!"
date: 2017-06-01
author: "str4d"
description: "Bu yılki Summer Dev, ağ için metrik toplama ve performans iyileştirmelerine odaklanacak."
categories: ["summer-dev"]
---

Yılın o zamanı yine geldi! I2P'nin belirli bir yönüne odaklanarak onu ileriye taşımayı amaçladığımız yaz geliştirme programımıza başlıyoruz. Önümüzdeki üç ay boyunca, hem yeni katkıda bulunanları hem de mevcut topluluk üyelerini bir görev seçip onunla eğlenmeleri için teşvik edeceğiz!

Geçen yıl, API araçlarını iyileştirerek ve I2P üzerinde çalışan uygulamalara ek iyileştirmeler yaparak, kullanıcıların ve geliştiricilerin I2P’den faydalanmasına yardımcı olmaya odaklandık. Bu yıl ise, herkesi etkileyen bir alanda çalışarak kullanıcı deneyimini iyileştirmek istiyoruz: performans.

Her ne kadar soğan yönlendirmeli ağlar sıklıkla "düşük gecikmeli" ağlar olarak adlandırılsa da, trafiğin ek bilgisayarlar üzerinden yönlendirilmesi kayda değer bir ek yük oluşturur. I2P'nin tek yönlü tunnel tasarımı, varsayılan olarak iki Destinations arasındaki bir gidiş-dönüşün toplam on iki katılımcıyı içereceği anlamına gelir! Bu katılımcıların performansını iyileştirmek, hem uçtan uca bağlantıların gecikmesini azaltmaya hem de ağ genelinde tunnel kalitesini artırmaya yardımcı olacaktır.

## DAHA FAZLA hız!

Bu yılki geliştirme programımız dört bileşenden oluşacak:

### Measure

Bir temel ölçüt olmadan performansı iyileştirip iyileştirmediğimizi bilemeyiz! I2P ile ilgili kullanım ve performans verilerini gizliliği koruyan bir şekilde toplamak için bir metrik sistemi oluşturacağız ve ayrıca çeşitli kıyaslama araçlarını I2P üzerinden çalışacak şekilde uyarlayacağız (örn. iperf3).

### Ölçüm

Mevcut kodumuzun performansını iyileştirmek için, örneğin tunnels içinde yer almanın getirdiği ek yükü azaltmak amacıyla, büyük bir alan var. Kriptografik ilkelere, ağ taşıma protokollerine (hem bağlantı katmanında hem de uçtan uca), eş profillemesine ve tunnel yol seçimine yönelik olası iyileştirmelere bakacağız.

### En iyi duruma getir

I2P ağının ölçeklenebilirliğini artırmaya yönelik birden fazla açık önerimiz var (örn. Prop115, Prop123, Prop124, Prop125, Prop138, Prop140). Bu öneriler üzerinde çalışacağız ve nihai hale getirilenleri çeşitli ağ router'larında uygulamaya başlayacağız.

### İlerleme

I2P, üzerinde çalıştığı internet gibi paket anahtarlamalı bir ağdır. Bu, paketleri nasıl yönlendirdiğimiz konusunda hem performans hem de gizlilik açısından önemli bir esneklik sağlar. Bu esnekliğin büyük bir kısmı henüz keşfedilmemiştir! Bant genişliğini artırmaya yönelik çeşitli clearnet (açık internet) tekniklerinin I2P’ye nasıl uygulanabileceği ve bunların ağ katılımcılarının gizliliğini nasıl etkileyebileceği üzerine araştırmaları teşvik etmek istiyoruz.

## Take part in Summer Dev!

Bu alanlarda gerçekleştirmek istediğimiz daha pek çok fikirimiz var. Gizlilik ve anonimlik yazılımları üzerinde çalışmak, protokoller tasarlamak (kriptografik veya başka türde), ya da geleceğe dönük fikirleri araştırmak ilginizi çekiyorsa - IRC'de veya Twitter'da gelin bizimle sohbet edin! Topluluğumuza yeni katılanları her zaman memnuniyetle karşılarız. Ayrıca katkıda bulunan tüm yeni kişilere I2P çıkartmaları da göndereceğiz!

İlerledikçe burada paylaşacağız, ancak ilerlememizi Twitter'da #I2PSummer etiketiyle takip edebilir ve kendi fikir ve çalışmalarınızı paylaşabilirsiniz. Yaz gelsin!
