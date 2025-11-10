---
title: "Çeviri Rehberi"
description: "Yönlendirici konsol ve web sitesini çevirerek I2P'nin dünya çapında erişilebilir olmasına yardımcı olun"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Genel Bakış

I2P yönlendirici konsol ve web sitesini kendi dilinize çevirerek I2P'nin dünya genelindeki kullanıcılara erişilebilir olmasına yardımcı olun. Çeviri sürekli bir süreçtir ve her büyüklükte katkı değerlidir.

## Çeviri Platformu

Tüm I2P çevirileri için **Transifex** kullanıyoruz. Bu, hem yeni başlayanlar hem de deneyimli çevirmenler için en kolay ve önerilen yöntemdir.

### Transifex ile Başlarken

1. [Transifex](https://www.transifex.com/) adresinde **bir hesap oluşturun**
2. **I2P projesine katılın**: [Transifex'te I2P](https://explore.transifex.com/otf/I2P/)
3. Dil ekibinize **katılma talebinde bulunun** (veya listede yoksa yeni bir dil talep edin)
4. Onaylandıktan sonra **çeviri yapmaya başlayın**

### Neden Transifex?

- **Kullanıcı dostu arayüz** - Teknik bilgi gerektirmez
- **Çeviri belleği** - Önceki çalışmalara dayanarak çeviri önerileri sunar
- **İşbirliği** - Dilinizdeki diğer çevirmenlerle çalışın
- **Kalite kontrolü** - İnceleme süreci doğruluğu sağlar
- **Otomatik güncellemeler** - Değişiklikler geliştirme ekibiyle senkronize edilir

## Neleri Çevirmeli

### Yönlendirici Konsolu (Öncelik)

I2P yönlendirici konsolu, kullanıcıların I2P'yi çalıştırırken etkileşime girdiği birincil arayüzdür. Onu çevirmek, kullanıcı deneyimi üzerinde en doğrudan etkiye sahiptir.

**Çevrilecek ana alanlar:**

- **Ana arayüz** - Gezinme, menüler, butonlar, durum mesajları
- **Yapılandırma sayfaları** - Ayar açıklamaları ve seçenekler
- **Yardım belgeleri** - Gömülü yardım dosyaları ve yardımcı notlar
- **Haberler ve güncellemeler** - Kullanıcılara gösterilen ilk haber akışı
- **Hata mesajları** - Kullanıcıya yönelik hata ve uyarı mesajları
- **Vekil yapılandırmaları** - HTTP, SOCKS ve tünel kurulum sayfaları

Tüm yönlendirici konsolu çevirileri Transifex üzerinde `.po` (gettext) formatında yönetilmektedir.

## Çeviri Yönergeleri

### Stil ve Üslup

- **Net ve öz** - I2P teknik kavramlar içerir; çevirileri basit tutun
- **Tutarlı terminoloji** - Aynı terimleri kullanın (çeviri belleğini kontrol edin)
- **Resmi vs. gayri resmi** - Dilinizin kurallarını takip edin
- **Biçimlendirmeyi koruyun** - `{0}`, `%s`, `<b>etiketler</b>` gibi yer tutucuları olduğu gibi bırakın

### Teknik Hususlar

- **Kodlama** - Her zaman UTF-8 kodlaması kullanın
- **Yer tutucular** - Değişken yer tutucuları çevirmeyin (`{0}`, `{1}`, `%s`, vb.)
- **HTML/Markdown** - HTML etiketlerini ve Markdown biçimlendirmesini koruyun
- **Bağlantılar** - Yerelleştirilmiş bir sürüm yoksa URL'leri değiştirmeyin
- **Kısaltmalar** - Çevirip çevirmemeyi veya orijinalini korumayı düşünün (ör. "KB/s", "HTTP")

### Çevirilerinizi Test Etme

Eğer bir I2P yönlendiricisi erişiminiz varsa:

1. Transifex'ten en yeni çeviri dosyalarını indirin
2. Bunları I2P kurulumunuza yerleştirin
3. Yönlendirici konsolunu yeniden başlatın
4. Çevirilerinizi bağlamda gözden geçirin
5. Herhangi bir sorun veya iyileştirme ihtiyacını bildirin

## Yardım Alma

### Topluluk Desteği

- **IRC Kanalı**: I2P IRC veya OFTC'de `#i2p-dev`
- **Forum**: I2P geliştirme forumları
- **Transifex Yorumları**: Çeviri dizgileri üzerinde doğrudan soru sorun

### Yaygın Sorular

**S: Ne sıklıkla çeviri yapmalıyım?**
Kendi temponuzda çeviri yapın. Birkaç dizgiyi çevirmek bile yardımcı olur. Proje devam ediyor.

**S: Dilim listede yoksa ne yapmalıyım?**
Transifex'te yeni bir dil talep edin. Talep varsa, ekip bunu ekleyecektir.

**S: Yalnız mı çevirmeliyim yoksa bir ekibe mi ihtiyacım var?**
Yalnız başlayabilirsiniz. Dilinize daha fazla çevirmen katıldıkça işbirliği yapabilirsiniz.

**S: Nelerin çevrilmesi gerektiğini nasıl bileceğim?**
Transifex, tamamlama yüzdelerini gösterir ve çevrilmemiş dizgileri işaretler.

**S: Mevcut bir çeviriyle ilgili anlaşmazlığım olursa ne yapmalıyım?**
Transifex'te iyileştirmeler önerin. İnceleme yapanlar değişiklikleri değerlendirecektir.

## İleri Düzey: Manuel Çeviri (Opsiyonel)

Kaynak dosyalara doğrudan erişim isteyen deneyimli çevirmenler için:

### Gereksinimler

- **Git** - Versiyon kontrol sistemi
- **POEdit** veya metin düzenleyici - `.po` dosyalarını düzenlemek için
- **Temel komut satırı** bilgisi

### Süreç

1. **Depoyu klonlayın**:
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Çeviri dosyalarını bulun**:
   - Yönlendirici konsolu: `apps/routerconsole/locale/`
   - `messages_xx.po` (burada `xx` dil kodunuzdur) dosyasını arayın

3. **Çevirileri düzenleyin**:
   - POEdit veya metin düzenleyici kullanın
   - UTF-8 kodlaması ile kaydedin

4. **Yerel test yapın** (eğer I2P yüklüyse)

5. **Değişiklikleri gönderin**:
   - [I2P Git](https://i2pgit.org/) üzerinde bir birleşme isteği oluşturun
   - Veya `.po` dosyanızı geliştirme ekibiyle paylaşın

**Not**: Çoğu çevirmen Transifex'i kullanmalıdır. Manuel çeviri yalnızca Git ve geliştirme akışlarına aşina olanlar içindir.

## Teşekkürler

Her çeviri, I2P'nin dünya çapındaki kullanıcılara daha erişilebilir olmasına yardımcı olur. Birkaç dizgi veya tüm bölümleri çevirseniz de, katkınız insanların çevrimiçi gizliliklerini korumasına gerçek bir fark yaratır.

**Başlamaya hazır mısınız?** [Transifex'te I2P'ye Katılın →](https://explore.transifex.com/otf/I2P/)
