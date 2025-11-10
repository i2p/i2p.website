---
title: "2005-09-20 için I2P Durum Notları"
date: 2005-09-20
author: "jr"
description: "SSU introductions ile 0.6.0.6 sürümünün başarıyla yayımlanması, I2Phex 0.1.1.27 güvenlik güncellemesi ve colo (ortak barındırma) taşınmasının tamamlanmasını kapsayan haftalık güncelleme"
categories: ["status"]
---

Merhaba millet, yine salı.

* Index:

1) 0.6.0.6 2) I2Phex 0.1.1.27 3) geçiş 4) ???

* 1) 0.6.0.6

Geçen cumartesi yayımlanan 0.6.0.6 sürümüyle birlikte, canlı ağda devrede bir dizi yeni bileşenimiz var ve hepiniz yükseltme konusunda harika iş çıkardınız - birkaç saat önce itibarıyla, neredeyse 250 router yükseltildi! Ağ da iyi gidiyor gibi görünüyor ve introductions (introduction mekanizması) şu ana kadar çalışıyor - http://localhost:7657/oldstats.jsp ile kendi introduction etkinliğinizi, udp.receiveHolePunch ve udp.receiveIntroRelayResponse metriklerine bakarak izleyebilirsiniz (NAT'lerin arkasında olanlar için udp.receiveRelayIntro da).

bu arada, "Status: ERR-Reject" artık gerçekten bir hata değil, bu yüzden belki bunu "Status: OK (NAT)" olarak değiştirmeliyiz?

Syndie ile ilgili birkaç hata bildirimi oldu. En son, ondan bir seferde çok fazla girdi indirmesini istediğinizde uzaktaki eşlerle senkronize olamamasına yol açan bir hata var (çünkü aptalca bir şekilde POST yerine HTTP GET kullandım). EepGet'e POST desteği ekleyeceğim, ama bu arada, bir seferde sadece 20 ya da 30 gönderi çekmeyi deneyin. Ayrıca, belki de birisi, blogundaki tüm onay kutularını otomatik olarak işaretleyerek "bu kullanıcıdan tüm gönderileri getir" diyen remote.jsp sayfası için bir javascript geliştirebilir?

Word on the street is that OSX works fine out of the box now, and with 0.6.0.6-1, x86_64 is operational too on both windows and linux. I haven't heard any reports of problems with the new .exe installers, so either that means its going well or failing completely :)

* 2) I2Phex 0.1.1.27

Kaynak ile legion'un paketlediği 0.1.1.26 sürümüne dahil edilenler arasındaki farklılıklara ilişkin bazı raporlar ve kapalı kaynak yerel (native) başlatıcının güvenliği konusundaki endişeler üzerine, launch4j [1] ile derlenmiş yeni bir i2phex.exe'yi cvs'ye ekledim ve cvs'deki en güncel sürümü derleyip i2p dosya arşivine [2] koydum. legion'un, sürümünü yayımlamadan önce kaynak kodunda başka değişiklikler yapıp yapmadığı ya da yayımladığı kaynak kodunun gerçekten derlediğiyle aynı olup olmadığı bilinmiyor.

Güvenlik gerekçeleriyle, ne legion'un kapalı kaynak kodlu launcher (başlatıcı) uygulamasının ne de 0.1.1.26 sürümünün kullanımını öneremem. I2P web sitesi [2] üzerindeki sürüm, değişiklik yapılmadan cvs'den gelen en güncel kodu içerir.

Önce I2P kodunu checkout edip derleyerek, ardından I2Phex kodunu checkout ederek, sonra da "ant makeRelease" komutunu çalıştırarak derlemeyi yeniden üretebilirsiniz:   mkdir ~/devi2p ; cd ~/devi2p/   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot login

# (parola: anoncvs)

cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2p   cd i2p ; ant build ; cd ..   cvs -d :pserver:anoncvs-PQcCzt6076/R7s880joybQ@xxxxxxxxxxxxxxxx/cvsroot co i2phex   cd i2phex/build ; ant makeRelease ; cd ../..   ls -l i2phex/release/i2phex-0.1.1.27.zip

Bu zip'in içindeki i2phex.exe, Windows'ta doğrudan çalıştırılarak, *nix/osx'te ise "java -jar i2phex.exe" komutuyla kullanılabilir. I2P'nin bazı jar dosyalarına başvurduğu için, I2Phex'in I2P'nin yanındaki bir dizine kurulmuş olmasına bağlıdır - (örn. C:\Program Files\i2phex\ ve C:\Program Files\i2p\).

I2Phex’in bakımını üstlenmiyorum, ama cvs’de güncellemeler olduğunda gelecekteki I2Phex sürümlerini web sitesine ekleyeceğim. Eğer biri onu açıklayan/tanıtan ve yayımlayabileceğimiz bir web sayfası üzerinde çalışmak isterse (sirup, orada mısın?), sirup.i2p’ye bağlantılar, yararlı forum gönderileri ve legion’un etkin eşler listesiyle birlikte, harika olurdu.

[1] http://launch4j.sourceforge.net/ [2] http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip ve     http://dev.i2p.net/i2p/i2phex-0.1.1.27.zip.sig (anahtarımla imzalanmıştır)

* 3) migration

I2P servisleri için colo (ortak barındırma) sunucularını değiştirdik, ancak artık yeni sunucuda her şey tamamen çalışır durumda olmalı - eğer garip bir şey görürseniz lütfen bana bildirin!

* 4) ???

Son zamanlarda i2p listesinde epey ilginç tartışmalar oldu; Adam’ın hoş yeni SMTP proxy/filtre aracı ve syndie’de bazı güzel yazılar da var (http://gloinsblog.i2p adresindeki gloin’in temasını gördünüz mü?). Şu anda uzun süredir devam eden bazı sorunlar için bazı değişiklikler üzerinde çalışıyorum, ancak bunlar yakın zamanda hazır olmayacak. Başka gündeme getirip tartışmak istediği bir şey olan olursa, GMT 20:00’de #i2p’deki toplantıya uğrayın (yaklaşık 10 dakika kadar sonra).

=jr
