---
title: "Yeni Çevirmen Rehberi"
description: "I2P web sitesine ve router konsoluna Transifex veya manuel yöntemler kullanarak nasıl çeviri katkısı yapılır"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

I2P'yi dünya çapında daha fazla insana ulaştırmak için yardım etmek ister misiniz? Çeviri, projeye yapabileceğiniz en değerli katkılardan biridir. Bu kılavuz, router konsolu çevirme sürecinde size rehberlik edecektir.

## Çeviri Yöntemleri

Çevirilere katkıda bulunmanın iki yolu vardır:

### Yöntem 1: Transifex (Önerilen)

**Bu, I2P'yi çevirmenin en kolay yoludur.** Transifex, çeviriyi basit ve erişilebilir kılan web tabanlı bir arayüz sağlar.

1. [Transifex](https://www.transifex.com/otf/I2P/) adresinden kayıt olun
2. I2P çeviri ekibine katılma isteği gönderin
3. Doğrudan tarayıcınızda çeviri yapmaya başlayın

Teknik bilgi gerekmez - sadece kaydolun ve çeviriye başlayın!

### Yöntem 2: Manuel Çeviri

Git ve yerel dosyalarla çalışmayı tercih eden çevirmenler için veya henüz Transifex'te kurulmamış diller için.

**Gereksinimler:** - Git sürüm kontrol sistemi bilgisi - Metin düzenleyici veya çeviri aracı (POEdit önerilir) - Komut satırı araçları: git, gettext

**Kurulum:** 1. [IRC'de #i2p-dev](/contact/#irc) kanalına katılın ve kendinizi tanıtın 2. Wiki'deki çeviri durumunu güncelleyin (erişim için IRC'de sorun) 3. Uygun repository'yi klonlayın (aşağıdaki bölümlere bakın)

---

## Router Konsolu Çevirisi

Router konsolu, I2P'yi çalıştırdığınızda gördüğünüz web arayüzüdür. Onu çevirmek, İngilizce ile rahat olmayan kullanıcılara yardımcı olur.

### Transifex Kullanımı (Önerilir)

1. [Transifex üzerinde I2P](https://www.transifex.com/otf/I2P/) sayfasına gidin
2. Router console projesini seçin
3. Dilinizi seçin
4. Çeviriye başlayın

### Manuel Router Konsolu Çevirisi

**Ön Koşullar:** - Web sitesi çevirisiyle aynı (git, gettext) - GPG anahtarı (commit erişimi için) - İmzalanmış geliştirici anlaşması

**Ana I2P deposunu klonlayın:**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Çevrilecek dosyalar:**

Router konsolu çeviriye ihtiyaç duyan yaklaşık 15 dosya içermektedir:

1. **Temel arayüz dosyaları:**
   - `apps/routerconsole/locale/messages_*.po` - Ana konsol mesajları
   - `apps/routerconsole/locale-news/messages_*.po` - Haber mesajları

2. **Proxy dosyaları:**
   - `apps/i2ptunnel/locale/messages_*.po` - Tunnel yapılandırma arayüzü

3. **Uygulama yerel ayarları:**
   - `apps/susidns/locale/messages_*.po` - Adres defteri arayüzü
   - `apps/susimail/locale/messages_*.po` - E-posta arayüzü
   - Diğer uygulamaya özel yerel ayar dizinleri

4. **Dokümantasyon dosyaları:**
   - `installer/resources/readme/readme_*.html` - Kurulum bilgi dosyası
   - Çeşitli uygulamalardaki yardım dosyaları

**Çeviri iş akışı:**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Çalışmanızı gönderin:** - [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) üzerinde birleştirme isteği oluşturun - Veya dosyaları IRC üzerinden geliştirme ekibi ile paylaşın

---

## Çeviri Araçları

### POEdit (Şiddetle Tavsiye Edilir)

[POEdit](https://poedit.net/), .po çeviri dosyaları için özel bir düzenleyicidir.

**Özellikler:** - Çeviri çalışması için görsel arayüz - Çeviri bağlamını gösterir - Otomatik doğrulama - Windows, macOS ve Linux için kullanılabilir

### Metin Editörleri

Herhangi bir metin düzenleyici de kullanabilirsiniz: - VS Code (i18n eklentileri ile) - Sublime Text - vim/emacs (terminal kullanıcıları için)

### Kalite Kontrolleri

Göndermeden önce: 1. **Biçimlendirmeyi kontrol edin:** `%s` ve `{0}` gibi yer tutucuların değişmeden kaldığından emin olun 2. **Çevirilerinizi test edin:** I2P'yi kurun ve çalıştırarak nasıl göründüklerini görün 3. **Tutarlılık:** Dosyalar arasında terminoloji tutarlılığını koruyun 4. **Uzunluk:** Bazı dizgeler arayüzde alan kısıtlamalarına sahiptir

---

## Çevirmenler için İpuçları

### Genel Kurallar

- **Tutarlı olun:** Yaygın terimler için belgeler boyunca aynı çevirileri kullanın
- **Biçimlendirmeyi koruyun:** HTML etiketlerini, yer tutucuları (`%s`, `{0}`) ve satır sonlarını olduğu gibi bırakın
- **Bağlam önemlidir:** Bağlamı anlamak için kaynak İngilizce metni dikkatlice okuyun
- **Soru sorun:** Bir şey belirsizse IRC veya forumları kullanın

### Yaygın I2P Terimleri

Bazı terimler İngilizce olarak kalmalı veya dikkatlice harf çevriminden geçirilmelidir:

- **I2P** - Olduğu gibi bırakın
- **eepsite** - I2P web sitesi (dilinizde açıklama gerektirebilir)
- **tunnel** - Bağlantı yolu ("devre" gibi Tor terminolojisinden kaçının)
- **netDb** - Ağ veritabanı
- **floodfill** - Router türü
- **destination** - I2P adres uç noktası

### Çevirilerinizi Test Etme

1. Çevirilerinizle I2P'yi derleyin
2. Router konsolu ayarlarından dili değiştirin
3. Kontrol etmek için tüm sayfalarda gezinin:
   - Metinlerin UI öğelerine sığdığından
   - Bozuk karakterlerin olmadığından (kodlama sorunları)
   - Çevirilerin bağlama uygun olduğundan

---

## Sık Sorulan Sorular

### Çeviri süreci neden bu kadar karmaşık?

Süreç, versiyon kontrolü (git) ve standart çeviri araçları (.po dosyaları) kullanır çünkü:

1. **Hesap Verebilirlik:** Kimin neyi ne zaman değiştirdiğini takip edin
2. **Kalite:** Değişiklikleri yayına geçmeden önce inceleyin
3. **Tutarlılık:** Uygun dosya biçimlendirme ve yapısını koruyun
4. **Ölçeklenebilirlik:** Çevirileri birden fazla dilde verimli bir şekilde yönetin
5. **İşbirliği:** Birden fazla çevirmen aynı dil üzerinde çalışabilir

### Programlama becerisine ihtiyacım var mı?

**Hayır!** Transifex kullanıyorsanız, sadece şunlara ihtiyacınız var: - Hem İngilizce hem de hedef dilinizde akıcılık - Bir web tarayıcısı - Temel bilgisayar becerileri

Manuel çeviri için temel komut satırı bilgisi gereklidir, ancak kodlama gerekmez.

### Ne kadar sürer?

- **Router konsolu:** Tüm dosyalar için yaklaşık 15-20 saat
- **Bakım:** Yeni dizeleri güncellemek için ayda birkaç saat

### Birden fazla kişi tek bir dil üzerinde çalışabilir mi?

Evet! Koordinasyon çok önemli: - Otomatik koordinasyon için Transifex kullanın - Manuel çalışma için #i2p-dev IRC kanalında iletişim kurun - İşi bölümler veya dosyalar halinde bölüştürün

### Dilim listede yoksa ne olur?

Transifex üzerinden talep edin veya IRC'de ekiple iletişime geçin. Geliştirme ekibi yeni bir dili hızlıca ayarlayabilir.

### Çevirilerimi göndermeden önce nasıl test edebilirim?

- Çevirilerinizle I2P'yi kaynaktan derleyin
- Yerel olarak kurun ve çalıştırın
- Konsol ayarlarından dili değiştirin

---

## Yardım Alma

### IRC Desteği

Şunlar için [IRC'de #i2p-dev](/contact/#irc) kanalına katılın: - Çeviri araçlarıyla ilgili teknik yardım - I2P terminolojisi hakkında sorular - Diğer çevirmenlerle koordinasyon - Geliştiricilerden doğrudan destek

### Forumlar

- [I2P Forumları](http://i2pforum.net/)'nda çeviri tartışmaları
- I2P İçinde: zzz.i2p üzerinde çeviri forumu (I2P router gerektirir)

### Belgeler

- [Transifex Belgeleri](https://docs.transifex.com/)
- [POEdit Belgeleri](https://poedit.net/support)
- [gettext Kılavuzu](https://www.gnu.org/software/gettext/manual/)

---

## Tanıma

Tüm çevirmenler şu yerlerde belirtilir: - I2P router konsolu (Hakkında sayfası) - Web sitesi katkıda bulunanlar sayfası - Git commit geçmişi - Sürüm duyuruları

Çalışmanız, dünya çapında insanların I2P'yi güvenli ve özel bir şekilde kullanmasına doğrudan yardımcı oluyor. Katkılarınız için teşekkür ederiz!

---

## Sonraki Adımlar

Çeviriye başlamaya hazır mısınız?

1. **Yönteminizi seçin:**
   - Hızlı başlangıç: [Transifex'te kaydolun](https://www.transifex.com/otf/I2P/)
   - Manuel yaklaşım: [IRC'de #i2p-dev'e](/contact/#irc) katılın

2. **Küçük başlayın:** Sürece aşina olmak için birkaç dize çevirin

3. **Yardım isteyin:** IRC veya forumlarda yardım istemekten çekinmeyin

**I2P'yi herkes için erişilebilir hale getirmeye yardımcı olduğunuz için teşekkür ederiz!**
