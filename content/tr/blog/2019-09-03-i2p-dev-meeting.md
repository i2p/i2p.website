---
title: "I2P Geliştirici Toplantısı - 03 Eylül 2019"
date: 2019-09-03
author: "zzz"
description: "03 Eylül 2019 tarihli I2P geliştirme toplantısı kaydı."
categories: ["meeting"]
---

## Kısa özet

<p class="attendees-inline"><strong>Katılanlar:</strong> eyedeekay, sadie, zlatinb, zzz</p>

## Toplantı Günlüğü

<div class="irc-log">                Not: Sadie'nin mesajları toplantı sırasında iletilmedi, aşağıya yapıştırıldı.

20:00:00 <zzz> 0) Merhaba
20:00:00 <zzz> 1) 0.9.42 sürüm durumu (zzz)
20:00:00 <zzz> 2) I2P Browser "labs" proje durumu (sadie, meeh)
20:00:00 <zzz> 3) Outproxy kullanım senaryoları / durum (sadie)
20:00:00 <zzz> 4) 0.9.43 geliştirme durumu (zzz)
20:00:00 <zzz> 5) Öneriler durumu (zzz)
20:00:00 <zzz> 6) Durum scrum'u (zlatinb)
20:00:04 <zzz> 0) Merhaba
20:00:06 <zzz> merhaba
20:00:17 <zlatinb> merhaba
20:00:30 <zzz> 1) 0.9.42 sürüm durumu (zzz)
20:00:48 <zzz> sürüm geçen hafta oldukça sorunsuz geçti
20:00:56 <zzz> sadece birkaç bekleyen konu var
20:01:27 <zzz> github bridge'i yeniden çalışır hale getirmek (nextloop), debian sid paketi (mhatta) ve 41 için unuttuğumuz android client lib (meeh)
20:01:37 <zzz> nextloop, meeh, bu maddeler için ETAlarınız var mı?
20:03:06 <zzz> 1) hakkında başka bir şey?
20:04:02 <zzz> 2) I2P Browser "labs" proje durumu (sadie, meeh)
20:04:25 <zzz> sadie, meeh, durum nedir ve bir sonraki kilometre taşı nedir?          <sadie> Beta 5 Cuma günü çıkacaktı, ancak bazı sorunlar oldu. Bazıları hazır görünüyor https://i2bbparts.meeh.no/i2p-browser/ ama bunun için bir sonraki son tarih konusunda meeh'ten gerçekten haber almam gerekiyordu          <sadie> Lab Sayfası bu haftanın sonuna kadar yayında olacak. Bir sonraki Browser kilometre taşı, beta 6 sürümü için konsol gereksinimlerinin tartışılması olacak
20:05:51 <zzz> 2) hakkında başka bir şey?
20:06:43 <zzz> 3) Outproxy kullanım senaryoları / durum (sadie)
20:06:57 <zzz> sadie, durum nedir ve bir sonraki kilometre taşı nedir?          <sadie> Toplantı notlarımızı 2472 numaralı bilette herkes takip edebilir. Kullanım durumu statülerine karar verdik ve gereksinimler listemiz var. Bir sonraki kilometre taşı, Friends and Family kullanım durumu için kullanıcı gereksinimleri ile Friends and Familiy ve Genel kullanım durumu için geliştirme gereksinimlerini, nerede örtüşebileceklerini görmek üzere belirlemek olacak
20:08:05 <zzz> 3) hakkında başka bir şey?
20:08:19 <eyedeekay> Üzgünüm, geç kaldım
20:09:01 <zzz> 4) 0.9.43 geliştirme durumu (zzz)
20:09:21 <zzz> yaklaşık 7 hafta içinde yayınlamayı planladığımız 43 döngüsüne yeni başlıyoruz
20:09:40 <zzz> web sitesindeki yol haritasını güncelledik ama birkaç madde daha ekleyeceğiz
20:10:06 <zzz> bazı IPv6 hatalarını düzeltiyorum ve tunnel AES işlemeyi hızlandırıyorum
20:10:30 <zzz> yakında dikkatimi yeni blinding info (kimlik gizleme bilgisi) I2CP mesajına çevireceğim
20:10:59 <zzz> eyedeekay, zlatinb, .43 hakkında ekleyeceğiniz bir şey var mı?
20:11:46 <eyedeekay> Hayır, sanmıyorum
20:12:02 <zlatinb> muhtemelen daha fazla test ağı işi
20:12:32 <zzz> evet, SSU ile ilgili bakmamız gereken birkaç jogger bileti daha var
20:12:48 <zzz> 4) hakkında başka bir şey?
20:14:00 <zzz> 5) Öneriler durumu (zzz)
20:14:20 <zzz> birincil odağımız, çok karmaşık yeni şifreleme önerisi 144 üzerinde
20:14:48 <zzz> son haftalarda iyi ilerleme kaydettik ve önerinin kendisinde önemli güncellemeler yaptık
20:15:35 <zzz> temizlenecek birkaç şey ve doldurulacak boşluklar var, ancak yakında, belki ay sonuna kadar, bazı birim test uygulamalarını kodlamaya başlayabilecek kadar iyi bir durumda olduğuna dair umutluyum
20:16:17 <zzz> ayrıca, öneri 123 (şifreli LS2) için blinding info mesajı, önümüzdeki hafta onu kodlamaya başladıktan sonra tekrar gözden geçirilecek
20:16:52 <zzz> ayrıca, yakında chisana'dan öneri 152 (tunnel build messages) hakkında bir güncelleme bekliyoruz
20:17:27 <zzz> geçen ay öneri 147'yi (ağlar arası önleme) tamamladık ve hem i2p hem i2pd bunu kodladı ve .42 sürümünde yer alıyor
20:18:23 <zzz> bu yüzden işler ilerliyor, 144 yavaş ve ürkütücü görünse bile, onunla da iyi ilerleme kaydediyoruz
20:18:27 <zzz> 5) hakkında başka bir şey?
20:20:00 <zzz> 6) Durum scrum'u (zlatinb)
20:20:05 <zzz> söz sende zlatinb
20:20:42 <zlatinb> Merhaba, lütfen birkaç kelimeyle söyleyin: 1) son scrum'dan beri ne yaptınız 2) gelecek ay ne yapmayı planlıyorsunuz 3) engelleyicileriniz var mı veya yardıma ihtiyacınız var mı. Bitirdiğinizde EOT deyin
20:21:23 <zlatinb> ben: 1) büyük aktarımları hızlandırmak için test ağında çeşitli deneyler 2) umarız daha büyük bir sunucu/ağ üzerinde daha fazla test ağı çalışması 3) engel yok EOT
20:22:15 <zzz> 1) hata düzeltmeleri, configuration split değişikliği, .42 sürümü, öneriler, DEFCON atölyeleri (i2pforum'daki ve web sitemizdeki gezi raporuma bakın)
20:23:56 <zzz> 2) hata düzeltmeleri, öneri 144, blinding info mesajı, hızlandırmalar, outproxy araştırmasına yardımcı olmak, conf. split tarafından bozulan SSL sihirbazını düzeltmek
20:24:20 <zzz> daha fazla IPv6 düzeltmesi
20:24:38 <zzz> 3) engel yok EOT
20:24:50 <eyedeekay> 1) Son scrum'dan beri hata düzeltmeleri, web sitesi, outproxy önerisi üzerinde çalışıyorum ve i2ptunnels ile ilgili şeyler yapıyorum. 2) Web sitesinin sunumunu yeniden düzenlemeye ve iyileştirmeye devam etmek. Outproxy önerisini ilerletmek üzerinde çalışmak 3) engel yok EOT          <sadie> 1) FOCI'ye katıldım, fonlama seçeneklerini araştırdım, potansiyel fon sağlayıcılarla görüştüm, Tails ile bir toplantı yaptım (Mhatta dahil), I2P Browser markalaşması üzerinde çalıştım, IDK ile web sitesi güncellemeleri, son sürüm için konsolda küçük değişiklikler yaptım          <sadie> 2) gelecek ay hibeler üzerinde çalışıyorum, konsol ve web sitesi iyileştirmeleri, kurulum sihirbazı, Toronto'daki Our Networks'e katılmak, I2P Browser ve OutProxy araştırmasını ilerletmek          <sadie> 3) engel yok EOT
20:25:29 <zlatinb> scrum.setTimeout( 60 * 1000 );
20:27:04 <zzz> tamam, zaman aşımına gidiyor
20:27:10 <zlatinb> ScrumTimeoutException
20:27:41 <zzz> sadie meeh nextloop için 1)-3)'e geri dönmeleri adına son çağrı
20:27:52 <zzz> toplantı için başka konu var mı?
20:28:47 * zzz baffer'ı yakalar
20:30:00 * zzz ***bafs*** toplantıyı kapattı </div>
