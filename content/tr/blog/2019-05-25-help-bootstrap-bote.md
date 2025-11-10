---
title: "I2P-Bote bootstrap (önyükleme) sürecine yardım ederek nasıl gönüllü olunur"
date: 2019-05-20
author: "idk"
description: "I2P-Bote'un başlatılmasına yardımcı olun!"
categories: ["development"]
---

İnsanların birbirleriyle özel olarak mesajlaşmalarına yardımcı olmanın kolay bir yolu, yeni Bote kullanıcılarının kendi I2P-Bote peer'lerini başlatmak için kullanabileceği bir I2P-Bote peer'i (eş düğüm) çalıştırmaktır. Ne yazık ki şimdiye kadar, bir I2P-Bote önyükleme peer'ini kurma süreci gereğinden çok daha karmaşık ve anlaşılması güçtü. Oysa aslında son derece basit!

**I2P-bote nedir?**

I2P-bote, I2P üzerinde inşa edilmiş bir özel mesajlaşma sistemidir; iletilen mesajlar hakkında bilgi çıkarımını daha da zorlaştıran ek özelliklere sahiptir. Bu sayede, yüksek gecikmeye tolerans gösterirken ve gönderen çevrimdışı olduğunda mesajları iletmek için merkezi bir aktarıcıya (relay) bel bağlamadan, özel mesajları güvenli biçimde iletmek için kullanılabilir. Bu, neredeyse diğer tüm popüler özel mesajlaşma sistemlerinin tersine bir yaklaşım sunar; zira bu sistemler ya her iki tarafın da çevrimiçi olmasını gerektirir ya da çevrimdışı olan göndericiler adına mesajları ileten yarı güvenilir bir hizmete dayanır.

ya da, ELI5 (5 yaşındaymışım gibi açıklarsak): E-postaya benzer şekilde kullanılır, ancak e-postanın gizlilik kusurlarının hiçbirinden etkilenmez.

**Birinci Adım: I2P-Bote'yi yükleyin**

I2P-Bote bir I2P eklentisidir ve kurulumu çok kolaydır. Orijinal talimatlar [bote eepSite, bote.i2p](http://bote.i2p/install/) adresinde mevcuttur, ancak bunları clearnet (açık internet) üzerinden okumak isterseniz, bu talimatlar bote.i2p’in katkılarıyla sunulmaktadır:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Adım İki: I2P-Bote düğümünüzün base64 adresini alın**

Birinin takılıp kalabileceği kısım burası, ama endişelenmeyin. Talimatları bulmak biraz zor olsa da, aslında bu kolaydır ve koşullarınıza bağlı olarak kullanabileceğiniz çeşitli araçlar ve seçenekler vardır. Bootstrap düğümlerini gönüllü olarak çalıştırmaya yardımcı olmak isteyen kişiler için en iyi yol, bote tunnel tarafından kullanılan özel anahtar dosyasından gerekli bilgileri almaktır.

**Anahtarlar nerede?**

I2P-Bote, hedef anahtarlarını bir metin dosyasında saklar; Debian'da bu dosya `/var/lib/i2p/i2p-config/i2pbote/local_dest.key` konumundadır. Kullanıcının i2p'yi kurduğu Debian dışı sistemlerde anahtar `$HOME/.i2p/i2pbote/local_dest.key` içinde bulunur ve Windows'ta dosya `C:\ProgramData\i2p\i2pbote\local_dest.key` içinde bulunur.

**Yöntem A: Düz metin anahtarını base64 destination biçimine dönüştürün**

Düz metin bir anahtarı base64 destination (hedef adres) biçimine dönüştürmek için, anahtarı alıp yalnızca ondan destination kısmını ayırmak gerekir. Bunu düzgün şekilde yapmak için, aşağıdaki adımlar izlenmelidir:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Bu adımları sizin için gerçekleştirmek üzere çeşitli uygulamalar ve komut dosyaları mevcuttur. İşte bunlardan bazıları, ancak bu liste kesinlikle kapsamlı değildir:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Bu özellikler çeşitli I2P uygulama geliştirme kitaplıklarında da mevcuttur.

**Kısayol:**

bote düğümünüzün yerel destination'ı (hedef) bir DSA destination olduğundan, local_dest.key dosyasını ilk 516 baytta kalacak şekilde kısaltmak daha hızlıdır. Bunu kolayca yapmak için, Debian üzerinde I2P ile birlikte I2P-Bote çalışırken şu komutu çalıştırın:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Ya da, I2P sizin kullanıcı hesabınızda kuruluysa:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Yöntem B: Bir sorgu yapın**

Eğer bu biraz fazla iş gibi görünüyorsa, bir base32 address (base32 adresi) bulmaya yönelik mevcut yöntemlerden herhangi birini kullanarak Bote bağlantınızın base32 address'ini sorgulayıp base64 destination'ını (base64 hedef adresi) bulabilirsiniz. Bote düğümünüzün base32 address'i, Bote eklenti uygulaması altındaki "Connection" sayfasında, [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network) adresinde bulunur.

**Adım Üç: Bize Ulaşın!**

**Yeni düğümünüzle built-in-peers.txt dosyasını güncelleyin**

Artık I2P-Bote düğümünüz için doğru destination (hedef adres) elinizde olduğuna göre, son adım kendinizi [I2P-Bote burada](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) bulunan varsayılan eşler listesine eklemektir. Bunu, depoyu çatallayıp, adınızı yorum satırı olarak ekleyerek ve hemen altına 516 karakterlik destination’ınızı yazarak yapabilirsiniz, şu şekilde:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
ve bir pull request (çekme isteği) göndermek. Hepsi bu kadar; bu yüzden i2p'yi canlı, merkeziyetsiz ve güvenilir tutmaya yardımcı olun.
