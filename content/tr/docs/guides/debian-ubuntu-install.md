---
title: "I2P'yi Debian ve Ubuntu'ya Kurma"
description: "I2P'yi Debian, Ubuntu ve türevlerinde resmi depolar kullanarak kurulum için eksiksiz kılavuz"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

I2P projesi, Debian, Ubuntu ve bunların türev dağıtımları için resmi paketler sağlamaktadır. Bu kılavuz, resmi depolarımızı kullanarak I2P kurulumu için kapsamlı talimatlar sunmaktadır.

---

Bu belge I2P'nin temel kavramlarını açıklamaktadır.

<div class="coming-soon-section">

## 🚀 Beta: Otomatik Kurulum (Deneysel)

**Hızlı otomatik kurulum isteyen ileri düzey kullanıcılar için:**

Bu tek satırlık komut dağıtımınızı otomatik olarak algılayacak ve I2P'yi kuracaktır. **Dikkatli kullanın** - çalıştırmadan önce [kurulum betiğini](https://i2p.net/installlinux.sh) inceleyin.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```
**Ne yapar:** - Linux dağıtımınızı algılar (Ubuntu/Debian) - Uygun I2P deposunu ekler - GPG anahtarlarını ve gerekli paketleri kurar - I2P'yi otomatik olarak kurar

⚠️ **Bu bir beta özelliğidir.** Manuel kurulumu tercih ediyorsanız veya her adımı anlamak istiyorsanız, aşağıdaki manuel kurulum yöntemlerini kullanın.

</div>

` markers.

Please share the English text you'd like me to translate to Turkish, and I'll provide the translation following all the rules specified.

## Ubuntu Kurulumu

Ubuntu ve resmi türevleri (Linux Mint, elementary OS, Trisquel, vb.) kolay kurulum ve otomatik güncellemeler için I2P PPA'sını (Personal Package Archive - Kişisel Paket Arşivi) kullanabilir.

### Method 1: Command Line Installation (Recommended)

Bu, Ubuntu tabanlı sistemlerde I2P kurulumu için en hızlı ve en güvenilir yöntemdir.

**Adım 1: I2P PPA'sını Ekleyin**

Bir terminal açın ve çalıştırın:

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Bu komut, I2P PPA'sını `/etc/apt/sources.list.d/` dizinine ekler ve depoyu imzalayan GPG anahtarını otomatik olarak içe aktarır. GPG imzası, paketlerin oluşturulduktan sonra kurcalanmadığını garanti eder.

**Adım 2: Paket listesini güncelleyin**

Sisteminizin paket veritabanını yeni PPA'yı içerecek şekilde yenileyin:

```bash
sudo apt-get update
```
Bu komut, yeni eklediğiniz I2P PPA dahil olmak üzere etkinleştirilmiş tüm depolardan en güncel paket bilgilerini alır.

**Adım 3: I2P'yi Kurun**

Şimdi I2P'yi kurun:

```bash
sudo apt-get install i2p
```
İşte bu kadar! I2P'yi nasıl başlatacağınızı ve yapılandıracağınızı öğrenmek için [Kurulum Sonrası Yapılandırma](#post-installation-configuration) bölümüne atlayın.

### Method 2: Using the Software Center GUI

Grafik arayüzü tercih ederseniz, Ubuntu'nun Yazılım Merkezi'ni kullanarak PPA'yı ekleyebilirsiniz.

**Adım 1: Yazılım ve Güncellemeler'i Açın**

Uygulamalar menünüzden "Yazılım ve Güncellemeler"i başlatın.

![Yazılım Merkezi Menüsü](/images/guides/debian/software-center-menu.png)

**Adım 2: Diğer Yazılımlara Git**

"Diğer Yazılım" sekmesini seçin ve yeni bir PPA yapılandırmak için alttaki "Ekle" düğmesine tıklayın.

![Diğer Yazılım Sekmesi](/images/guides/debian/software-center-addother.png)

**Adım 3: I2P PPA'sını Ekleyin**

PPA iletişim kutusuna şunu girin:

```
ppa:i2p-maintainers/i2p
```
![PPA Ekle İletişim Kutusu](/images/guides/debian/software-center-ppatool.png)

**Adım 4: Depo bilgilerini yeniden yükle**

Güncellenmiş depo bilgilerini indirmek için "Reload" düğmesine tıklayın.

![Yenile Düğmesi](/images/guides/debian/software-center-reload.png)

**Adım 5: I2P'yi Kurun**

Uygulamalar menünüzden "Yazılım" uygulamasını açın, "i2p" araması yapın ve Yükle'ye tıklayın.

![Yazılım Uygulaması](/images/guides/debian/software-center-software.png)

Kurulum tamamlandığında, [Kurulum Sonrası Yapılandırma](#post-installation-configuration) bölümüne geçin.

---


## Debian Installation

Debian ve türev dağıtımları (LMDE, Kali Linux, ParrotOS, Knoppix, vb.) `deb.i2p.net` adresindeki resmi I2P Debian deposunu kullanmalıdır.

### Important Notice

**`deb.i2p2.de` ve `deb.i2p2.no` adreslerindeki eski depolarımız artık kullanım ömrünü tamamlamıştır.** Bu eski depoları kullanıyorsanız, lütfen `deb.i2p.net` adresindeki yeni depoya geçiş yapmak için aşağıdaki talimatları izleyin.

### Prerequisites

Aşağıdaki tüm adımlar root erişimi gerektirir. Ya `su` komutuyla root kullanıcısına geçin ya da her komutun önüne `sudo` ekleyin.

### Yöntem 1: Komut Satırı Kurulumu (Önerilen)

**Adım 1: Gerekli paketleri yükleyin**

Gerekli araçların kurulu olduğundan emin olun:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Bu paketler güvenli HTTPS depo erişimi, dağıtım tespiti ve dosya indirmelerini etkinleştirir.

**Adım 2: I2P deposunu ekleyin**

Kullandığınız komut, Debian sürümünüze bağlıdır. Öncelikle hangi sürümü çalıştırdığınızı belirleyin:

```bash
cat /etc/debian_version
```
Dağıtımınızın kod adını (örn. Bookworm, Bullseye, Buster) belirlemek için bunu [Debian sürüm bilgileri](https://wiki.debian.org/LTS/) ile karşılaştırın.

**Debian Bullseye (11) veya daha yeni sürümler için:**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Bullseye-eşdeğeri veya daha yeni sürümlerdeki Debian türevleri için (LMDE, Kali, ParrotOS, vb.):**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Debian Buster (10) veya daha eski sürümler için:**

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Buster-eşdeğeri veya daha eski Debian türevleri için:**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Adım 3: Depo imzalama anahtarını indirin**

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
**Adım 4: Anahtar parmak izini doğrulayın**

Anahtara güvenmeden önce, parmak izinin resmi I2P imzalama anahtarıyla eşleştiğini doğrulayın:

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Çıktının bu parmak izini gösterdiğini doğrulayın:**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **Parmak izi eşleşmiyorsa devam etmeyin.** Bu, güvenliği ihlal edilmiş bir indirmeye işaret edebilir.

**Adım 5: Depo anahtarını yükleyin**

Doğrulanmış anahtar halkasını sistem anahtar halkaları dizinine kopyalayın:

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Yalnızca Debian Buster veya daha eski sürümler için**, ayrıca bir sembolik bağlantı (symlink) oluşturmanız gerekir:

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Adım 6: Paket listelerini güncelleyin**

Sistem paket veritabanınızı I2P deposunu içerecek şekilde yenileyin:

```bash
sudo apt-get update
```
**Adım 7: I2P'yi Kurun**

Hem I2P router'ını hem de keyring paketini kurun (bu, gelecekteki anahtar güncellemelerini almanızı sağlar):

```bash
sudo apt-get install i2p i2p-keyring
```
Harika! I2P artık kuruldu. [Kurulum Sonrası Yapılandırma](#post-installation-configuration) bölümüne devam edin.

---

## Post-Installation Configuration

I2P'yi yükledikten sonra, router'ı başlatmanız ve bazı ilk yapılandırmaları gerçekleştirmeniz gerekecektir.

### Yöntem 2: Yazılım Merkezi GUI Kullanımı

I2P paketleri, I2P router'ını çalıştırmak için üç yol sunar:

#### Option 1: On-Demand (Basic)

Gerektiğinde `i2prouter` betiğini kullanarak I2P'yi manuel olarak başlatın:

```bash
i2prouter start
```
**Önemli**: `sudo` kullanmayın veya bunu root olarak çalıştırmayın! I2P normal kullanıcınız olarak çalışmalıdır.

I2P'yi durdurmak için:

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

x86 olmayan bir sistemdeyseniz veya Java Service Wrapper platformunuzda çalışmıyorsa, şunu kullanın:

```bash
i2prouter-nowrapper
```
Tekrar belirtiyoruz, `sudo` **kullanmayın** veya root olarak çalıştırmayın.

#### Option 3: System Service (Recommended)

En iyi deneyim için, I2P'yi sistem başlangıcında, giriş yapmadan önce bile otomatik olarak başlayacak şekilde yapılandırın:

```bash
sudo dpkg-reconfigure i2p
```
Bu, bir yapılandırma iletişim kutusu açar. I2P'yi sistem hizmeti olarak etkinleştirmek için "Evet"i seçin.

**Bu önerilen yöntemdir** çünkü: - I2P başlangıçta otomatik olarak başlar - Router'ınız daha iyi ağ entegrasyonu sağlar - Ağ kararlılığına katkıda bulunursunuz - I2P ihtiyaç duyduğunuzda hemen kullanılabilir

### Initial Router Configuration

I2P'yi ilk kez başlattıktan sonra, ağa entegre olması birkaç dakika sürecektir. Bu sırada, şu temel ayarları yapılandırın:

#### 1. Configure NAT/Firewall

Optimum performans ve ağ katılımı için, I2P portlarını NAT/güvenlik duvarınızdan yönlendirin:

1. [I2P Router Console](http://127.0.0.1:7657/) sayfasını açın
2. [Ağ Yapılandırması sayfasına](http://127.0.0.1:7657/confignet) gidin
3. Listelenen port numaralarını not edin (genellikle 9000-31000 arası rastgele portlar)
4. Bu UDP ve TCP portlarını router/firewall'unuzda yönlendirin

Port yönlendirme konusunda yardıma ihtiyacınız varsa, [portforward.com](https://portforward.com) yönlendirici-özel kılavuzlar sağlar.

#### 2. Adjust Bandwidth Settings

Varsayılan bant genişliği ayarları muhafazakârdır. İnternet bağlantınıza göre bunları ayarlayın:

1. [Yapılandırma sayfasını](http://127.0.0.1:7657/config.jsp) ziyaret edin
2. Bant genişliği ayarları bölümünü bulun
3. Varsayılan değerler 96 KB/s indirme / 40 KB/s yükleme'dir
4. Daha hızlı bir internet bağlantınız varsa bu değerleri artırın (örneğin, tipik bir geniş bant bağlantısı için 250 KB/s indirme / 100 KB/s yükleme)

**Not**: Daha yüksek limitler belirlemek ağa yardımcı olur ve kendi performansınızı iyileştirir.

#### 3. Configure Your Browser

I2P sitelerine (eepsite'lara) ve servislerine erişmek için tarayıcınızı I2P'nin HTTP proxy'sini kullanacak şekilde yapılandırın:

Firefox, Chrome ve diğer tarayıcılar için detaylı kurulum talimatları için [Tarayıcı Yapılandırma Kılavuzumuzu](/docs/guides/browser-config) inceleyin.

---


## Debian Kurulumu

### Önemli Duyuru

- I2P'yi root olarak çalıştırmadığınızdan emin olun: `ps aux | grep i2p`
- Günlükleri kontrol edin: `tail -f ~/.i2p/wrapper.log`
- Java'nın kurulu olduğunu doğrulayın: `java -version`

### Ön Gereksinimler

Kurulum sırasında GPG anahtar hataları alırsanız:

1. Anahtarın parmak izini yeniden indirin ve doğrulayın (Yukarıdaki Adım 3-4)
2. Anahtar zinciri dosyasının doğru izinlere sahip olduğundan emin olun: `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Kurulum Adımları

I2P güncellemeleri almıyorsa:

1. Deponun yapılandırıldığını doğrulayın: `cat /etc/apt/sources.list.d/i2p.list`
2. Paket listelerini güncelleyin: `sudo apt-get update`
3. I2P güncellemelerini kontrol edin: `sudo apt-get upgrade`

### Migrating from old repositories

Eski `deb.i2p2.de` veya `deb.i2p2.no` depolarını kullanıyorsanız:

1. Eski depoyu kaldırın: `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Yukarıdaki [Debian Kurulumu](#debian-installation) adımlarını takip edin
3. Güncelleyin: `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

Tabii, çeviri için metni bekliyorum. Lütfen çevrilecek metni paylaşın.

## Next Steps

I2P kuruldu ve çalışıyor, şimdi:

- I2P sitelerine erişmek için [tarayıcınızı yapılandırın](/docs/guides/browser-config)
- Router'ınızı izlemek için [I2P router konsolunu](http://127.0.0.1:7657/) keşfedin
- Kullanabileceğiniz [I2P uygulamalarını](/docs/applications/) öğrenin
- Ağı anlamak için [I2P'nin nasıl çalıştığını](/docs/overview/tech-intro) okuyun

Görünmez İnternet'e Hoş Geldiniz!
