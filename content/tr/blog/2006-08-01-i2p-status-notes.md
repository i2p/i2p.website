---
title: "2006-08-01 için I2P Durum Notları"
date: 2006-08-01
author: "jr"
description: "Yüksek I2PSnark aktarım hızları, NTCP taşıma kararlılığı ve eepsite erişilebilirliğine ilişkin açıklamalarla güçlü ağ performansı"
categories: ["status"]
---

Herkese merhaba, bu akşamki toplantıdan önce kısa birkaç notu paylaşmanın zamanı geldi. Çeşitli sorularınız veya gündeme getirmek istediğiniz konular olabileceğinin farkındayım, bu yüzden her zamankinden daha esnek bir formatta ilerleyeceğiz. Öncelikle bahsetmek istediğim yalnızca birkaç nokta var.

* Network status

Ağın oldukça iyi işlediği görülüyor; oldukça büyük I2PSnark aktarım sürülerinin tamamlanması ve her bir router üzerinde oldukça kayda değer aktarım hızlarına ulaşılmasıyla - hiçbir sorun çıkmadan 650KBytes/sec ve 17,000 katılımcı tunnels gördüm. Spektrumun alt ucundaki routers da gayet iyi görünüyor, 2 hop tunnels ile ortalama 1KByte/sec’in altında kalarak eepsites(I2P Siteleri) gezebiliyor ve irc kullanabiliyorlar.

Yine de herkes için her şey güllük gülistanlık değil; ancak daha tutarlı ve daha kullanışlı bir performans sağlamak için router'ın davranışını güncellemek üzere çalışıyoruz.

* NTCP

Yeni NTCP aktarımı ("new" tcp), başlangıçtaki aksaklıklar ve pürüzler giderildikten sonra oldukça iyi gidiyor. Sık sorulan bir soruyu yanıtlamak gerekirse, uzun vadede, hem NTCP hem de SSU kullanımda olacak - yalnızca TCP'ye geri dönmüyoruz.

* eepsite(I2P Site) reachability

Unutmayın arkadaşlar, eepsites(I2P siteleri) yalnızca onu çalıştıran kişi onu açık tuttuğunda erişilebilir - kapalıysa, ona ulaşmak için yapabileceğiniz bir şey yok ;) Ne yazık ki son birkaç gündür orion.i2p erişilemiyor, ancak ağ kesinlikle hâlâ çalışıyor - ağ incelemesi ihtiyaçlarınız için belki inproxy.tino.i2p veya eepsites(I2P Sites).i2p uğrayın.

Neyse, daha pek çok şey oluyor, ancak burada bahsetmek biraz erken olur. Elbette, herhangi bir sorunuz veya endişeniz varsa, birkaç dakika içinde *öhm* haftalık geliştirme toplantımız için #i2p'ye uğrayın.

İlerlememize yardımcı olduğunuz için teşekkürler! =jr
