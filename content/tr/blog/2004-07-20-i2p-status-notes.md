---
title: "2004-07-20 için I2P Durum Notları"
date: 2004-07-20
author: "jr"
description: "0.3.2.3 sürümünü, kapasite değişikliklerini, web sitesi güncellemelerini ve güvenlik hususlarını kapsayan haftalık durum güncellemesi"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3 ve yol haritası**

Geçen hafta 0.3.2.3 sürümünün yayımlanmasının ardından, yükseltme konusunda harika iş çıkardınız - artık yalnızca iki istisna kaldı (biri 0.3.2.2'de ve biri de epey geride, 0.3.1.4'te :). Son birkaç gündür ağ her zamankinden daha güvenilir - insanlar irc.duck.i2p üzerinde saatlerce kalıyor, eepsites(I2P Sites) üzerinden yapılan büyük dosya indirmeleri başarıyla tamamlanıyor ve genel eepsite(I2P Site) erişilebilirliği oldukça iyi. İşler iyi gidiyor ve sizi tetikte tutmak istediğim için, birkaç temel kavramda değişiklik yapmaya karar verdim ve bunları bir iki gün içinde 0.3.3 sürümüyle dağıtıma alacağız.

Zaman çizelgemizle ilgili, koyduğumuz tarihleri tutturup tutturamayacağımızı merak eden birkaç kişinin yorumları üzerine, palmpilot'umda bulunan yol haritasını yansıtacak şekilde web sitesini muhtemelen güncellemem gerektiğine karar verdim ve öyle yaptım [1]. Tarihler sarktı ve bazı maddeler kaydırıldı, ancak plan geçen ay tartışılanla hâlâ aynı [2].

0.4, bahsedilen dört sürüm ölçütünü (işlevsel, güvenli, anonim ve ölçeklenebilir) karşılayacaktır, ancak 0.4.2'den önce NAT'lerin ve güvenlik duvarlarının arkasında bulunan çok az kişi katılabilecektir ve 0.4.3'ten önce, diğer routers ile çok sayıda TCP bağlantısını sürdürmenin ek yükü nedeniyle ağın büyüklüğüne fiili bir üst sınır olacaktır.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Son bir haftadır ya da öylesi, #i2p’deki insanlar, güvenilirlik sıralamalarımızın tamamen keyfi oluşu (ve bunun son birkaç sürümde yol açtığı sıkıntılar) hakkında ara sıra söylenip durduğumu duydular. Bu yüzden güvenilirlik kavramını tamamen ortadan kaldırdık, yerine kapasite ölçümünü getirdik — "bir peer (eş) bizim için ne kadar katkı sağlayabilir?" Bu durum, peer seçimi ve peer profilleme kodunun genelinde (ve elbette router konsolunda) yansıma etkilerine yol açtı, ancak bunun dışında çok fazla bir şey değişmedi.

Bu değişiklik hakkında daha fazla bilgiye güncellenmiş eş seçimi sayfasından [3] ulaşabilirsiniz, ve 0.3.3 yayınlandığında, hepiniz etkisini bizzat görebileceksiniz (son birkaç gündür bununla oynuyorum, bazı ayarları kurcalıyorum, vb.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) web sitesi güncellemeleri**

Son bir haftadır, web sitesi yeniden tasarımı [4] üzerinde önemli ilerlemeler kaydediyoruz - navigasyonu basitleştiriyor, bazı önemli sayfaları düzenliyor, eski içeriği içe aktarıyor ve bazı yeni yazılar yazıyoruz [5]. Siteyi yayına almaya neredeyse hazırız, ancak yapılması gereken hâlâ birkaç şey var.

Bugün erken saatlerde duck siteyi gözden geçirdi ve eksik olan sayfaların envanterini çıkardı; bugün öğleden sonraki güncellemelerden sonra ise, ya ele alabileceğimizi ya da üstlenecek gönüllüler bulabileceğimizi umduğum birkaç bekleyen sorun var:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Bunun dışında, sitenin canlıya alınmaya neredeyse hazır olduğunu düşünüyorum. Bu konuda önerisi ya da endişesi olan var mı?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) saldırılar ve savunmalar**

Connelly, ağın güvenliği ve anonimliğinde açık bulmaya çalışmak için birkaç yeni yaklaşım geliştirdi ve bunu yaparken işleri nasıl iyileştirebileceğimize dair bazı yollarla da karşılaştı. Bahsettiği tekniklerin bazı yönleri I2P ile tam örtüşmese de, belki sizler bunları genişleterek ağa daha ileri düzeyde saldırmak için kullanılabilecek yollar görebilirsiniz? Hadi, bir deneyin :)

**5) ???**

Bu akşamki toplantıdan önce hatırlayabildiklerim aşağı yukarı bu kadar - gözden kaçırdığım başka bir şey varsa lütfen çekinmeden dile getirin. Neyse, birkaç dakika içinde #i2p'de görüşürüz.

=jr
