---
title: "2005-01-25 tarihli I2P Durum Notları"
date: 2005-01-25
author: "jr"
description: "0.5 sürümündeki tunnel yönlendirmesindeki ilerleme, SAM .NET portu, GCJ derlemesi ve UDP taşıma tartışmalarını kapsayan haftalık I2P geliştirme durum notları"
categories: ["status"]
---

Herkese selam, kısa bir haftalık durum güncellemesi

* Index

1) 0.5 durumu 2) sam.net 3) gcj ilerlemesi 4) udp 5) ???

* 1) 0.5 status

Geçen hafta boyunca 0.5 tarafında ciddi ilerlemeler kaydedildi. Daha önce tartıştığımız sorunlar çözüldü; bu da kriptografiyi kayda değer ölçüde basitleştirip tunnel'lerin döngüye girmesi sorununu ortadan kaldırdı. Yeni teknik [1] uygulandı ve birim testleri hazır. Sırada, bu tunnel'leri ana router'a entegre etmek için daha fazla kodu bir araya getiriyorum, ardından tunnel yönetimi ve havuzlama altyapısını oluşturacağım. Bunlar hazır olduktan sonra, bunu sim üzerinden çalıştıracağız ve sonunda burn-in testinden geçirmek için paralel bir ağa taşıyacağız; son dokunuşları yapıp 0.5 olarak adlandıracağız.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/tunnel-alt.html?rev=HEAD

* 2) sam.net

smeghead, SAM protokolünün .net’e yeni bir portunu hazırladı - c#, mono/gnu.NET uyumlu (yaşasın smeghead!). Bu, cvs’de i2p/apps/sam/csharp/ altında, nant ve diğer yardımcılarla birlikte - artık tüm .net geliştiricileri i2p ile hacklemeye başlayabilir :)

* 3) gcj progress

smeghead kesinlikle büyük bir ivme yakalamış durumda - son kontrolümüzde, bazı değişikliklerle router en son gcj [2] build'inde derleniyor (w00t!).  Henüz çalışmıyor, ancak gcj'nin bazı iç sınıf yapılarıyla ilgili kafa karışıklığını aşmak için yapılan değişiklikler kesinlikle bir ilerleme.    Belki smeghead bize bir güncelleme verebilir?

[2] http://gcc.gnu.org/java/

* 4) udp

Burada söylenecek pek bir şey yok, yine de Nightblade, neden UDP’yi tercih ettiğimizi sorarak forumda ilginç bir dizi endişe [3] gündeme getirdi. Benim yanıtımda belirttiğim sorunları nasıl ele alabileceğimize dair başka önerileriniz varsa ya da benzer endişeleriniz bulunuyorsa, lütfen siz de katkıda bulunun!

[3] http://forum.i2p.net/viewtopic.php?t=280

* 5) ???

Evet, tamam, notlarda yine geç kaldım, maaşımdan kesin ;)  Neyse, çok şey oluyor, o yüzden ya toplantı için kanala uğrayın, sonrasında yayımlanan günlükleri kontrol edin, ya da söyleyecek bir şeyiniz varsa listeye yazın.  Ah, bu arada, pes ettim ve i2p [4] içinde bir blog açtım.

=jr [4] http://jrandom.dev.i2p/ (anahtar http://dev.i2p.net/i2p/hosts.txt içinde)
