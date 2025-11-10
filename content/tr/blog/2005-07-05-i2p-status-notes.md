---
title: "I2P 2005-07-05 için Durum Notları"
date: 2005-07-05
author: "jr"
description: "SSU taşımadaki ilerleme, tunnel IV saldırısının azaltılması ve HMAC-MD5 ile SSU MAC optimizasyonunu kapsayan haftalık güncelleme"
categories: ["status"]
---

Selam millet, haftanın o zamanı geldi,

* Index

1) Geliştirme durumu 2) Tunnel IV'leri (başlatma vektörleri) 3) SSU MAC'leri (Mesaj Kimlik Doğrulama Kodları) 4) ???

* 1) Dev status

Bir hafta daha, “SSU taşıma katmanında çok ilerleme kaydedildi” diyen bir başka mesaj ;) Yerel değişikliklerim kararlı ve CVS’e gönderildi (HEAD şu anda 0.5.0.7-9’da), fakat henüz bir sürüm yok. O cephede yakında daha fazla haber. SSU ile ilgisi olmayan değişikliklerin ayrıntıları tarihçe [1]’de, ancak SSU ile ilgili değişiklikleri şimdilik o listenin dışında tutuyorum, çünkü SSU henüz geliştirici olmayan hiç kimse tarafından kullanılmıyor (ve geliştiriciler i2p-cvs@’i okuyor :)

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD

* 2) Tunnel IVs

Son birkaç gündür dvorak, tunnel şifrelemesine saldırmanın farklı yolları üzerine ara sıra düşünceler paylaşıyor ve bunların çoğu zaten ele alınmış olsa da, katılımcıların bir çift iletiyi etiketleyerek bunların aynı tunnel içinde olduğunu belirlemesine olanak tanıyacak bir senaryo bulmayı başardık. Çalışma biçimi şöyleydi: önceki eş (peer) bir iletinin üzerinden geçmesine izin veriyor, daha sonra da o ilk tunnel iletisinin IV’sini ve ilk veri bloğunu alıp yeni bir iletinin içine yerleştiriyordu. Bu yeni ileti elbette bozuk olurdu, ancak IV’ler farklı olduğundan bir yeniden oynatma (replay) gibi görünmezdi. İlerleyen aşamada, ikinci eş de o iletiyi basitçe atabilirdi; böylece tunnel uç noktası saldırıyı tespit edemezdi.

Bu durumun arkasındaki temel sorunlardan biri, bir tunnel iletisini tunnel boyunca ilerlerken, bir dizi saldırıya kapı açmadan doğrulamanın bir yolu olmamasıdır (bu amaca epey yaklaşan bir yöntem için daha önceki bir tunnel şifreleme önerisine [2] bakın, ancak bu öneride olasılık varsayımları pek sağlam değildir ve tunnel'lar üzerinde bazı yapay kısıtlamalar dayatır).

[2] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel.html?rev=HEAD

Bununla birlikte, ana hatları verilen bu belirli saldırıyı bertaraf etmenin çok basit bir yolu var - tek başına IV yerine, Bloom filtresinden geçirilen benzersiz tanımlayıcı olarak xor(IV, ilk veri bloğu)'nu kullanmak. Bu şekilde, aracı eşler kopyayı görür ve ikinci işbirlikçi eşe ulaşmadan önce atarlar. Bu savunmayı içerecek şekilde CVS güncellendi, ancak mevcut ağ boyutu göz önüne alındığında bunun pratik bir tehdit olduğundan çok, ama çok şüphe duyuyorum; bu yüzden bunu tek başına bir sürüm olarak yayımlamıyorum.

Bu, diğer zamanlama veya trafik şekillendirme saldırılarının uygulanabilirliğini etkilemez; yine de, gördüğümüzde kolayca ele alınabilecek saldırıları bertaraf etmek en iyisidir.

* 3) SSU MACs

Spesifikasyonda [3] açıklandığı gibi, SSU transport her iletilen datagram için bir MAC (mesaj kimlik doğrulama kodu) kullanır. Bu, her I2NP mesajıyla gönderilen doğrulama özeti (ve ayrıca istemci mesajlarındaki uçtan uca doğrulama özetleri) dışında ilave bir kontroldür. Şu anda, spesifikasyon ve kod kısaltılmış bir HMAC-SHA256 kullanıyor - MAC’in yalnızca ilk 16 baytını iletip doğruluyor. Bu da *öhhöm* biraz israf, zira HMAC işlemi içinde SHA256 özetini iki kez kullanıyor, her seferinde 32 baytlık bir özet üzerinde çalışıyor ve SSU transport için yakın zamanda yapılan profil analizi bunun CPU yükü açısından kritik yolun yakınlarında olduğunu gösteriyor. Bu nedenle, HMAC-SHA256-128’i düz bir HMAC-MD5(-128) ile değiştirmeyi biraz kurcaladım - MD5’in açıkça SHA256 kadar güçlü olmadığını biliyoruz, ancak zaten SHA256’yı MD5 ile aynı boyuta kısalttığımız için çakışma için gereken kaba kuvvet miktarı da aynı (2^64 deneme). Şu anda bununla oynuyorum ve hızlanma kayda değer (2KB paketlerde SHA256’ya göre HMAC aktarım hızında 3 katından fazlasını elde ediyorum), bu yüzden muhtemelen bununla canlıya geçebiliriz. Ya da biri bunu yapmamamız için harika bir gerekçe (veya daha iyi bir alternatif) bulabilirse, değiştirmesi de yeterince basit (yalnızca tek satır kod).

[3] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 4) ???

Şimdilik bu kadar; her zamanki gibi, düşüncelerinizi ve endişelerinizi istediğiniz zaman paylaşmaktan çekinmeyin. junit yüklü olmayanlar için CVS HEAD artık yeniden derlenebilir durumda (şimdilik testleri i2p.jar’dan çıkardım, ancak test ant target ile hâlâ çalıştırılabilir) ve 0.6 testleri hakkında yakında daha fazla haber bekliyorum (şu anda colo box (kolokasyon sunucusu) gariplikleriyle boğuşuyorum - kendi arayüzlerime telnet ile bağlanmak yerelde başarısız oluyor (işe yarar bir errno olmadan), uzaktan çalışıyor; hem de herhangi bir iptables ya da başka filtre olmadan. harika). Evde hâlâ internet erişimim yok, bu yüzden bu akşam bir toplantıda olamayacağım, ama belki gelecek hafta.

=jr
