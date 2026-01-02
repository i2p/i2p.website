---
title: "I2P için Git Bundle'ları"
description: "BitTorrent ve git bundle ile büyük depoları indirme ve dağıtma"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Ağ koşulları `git clone` işlemini güvenilmez hale getirdiğinde, depoları BitTorrent veya başka bir dosya aktarım yöntemi üzerinden **git bundle'ları** olarak dağıtabilirsiniz. Bir bundle, tüm depo geçmişini içeren tek bir dosyadır. İndirildikten sonra, yerel olarak ondan fetch yaparsınız ve ardından upstream remote'a geri dönersiniz.

## 1. Başlamadan Önce

Bir paket oluşturmak için **eksiksiz** bir Git klonu gereklidir. `--depth 1` ile oluşturulan sığ klonlar, sessizce çalışıyor gibi görünen ancak başkaları kullanmaya çalıştığında başarısız olan bozuk paketler üretir. Her zaman güvenilir bir kaynaktan (GitHub'daki [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), I2P Gitea örneği [i2pgit.org](https://i2pgit.org), veya I2P üzerinden `git.idk.i2p`) getirin ve paket oluşturmadan önce herhangi bir sığ klonu tam klona dönüştürmek için gerekirse `git fetch --unshallow` komutunu çalıştırın.

Mevcut bir paketi sadece kullanıyorsanız, sadece indirin. Özel bir hazırlık gerekmez.

## 2. Bir Paket İndirme

### Obtaining the Bundle File

Bundle dosyasını I2PSnark (I2P'ye yerleşik torrent istemcisi) veya I2P eklentili BiglyBT gibi diğer I2P uyumlu istemcileri kullanarak BitTorrent üzerinden indirin.

**Önemli**: I2PSnark yalnızca I2P ağı için özel olarak oluşturulmuş torrent'lerle çalışır. Standart clearnet torrent'ler uyumlu değildir çünkü I2P, IP adresleri ve portlar yerine Destination'lar (387+ bayt adresler) kullanır.

Bundle dosyasının konumu I2P kurulum türünüze bağlıdır:

- **Kullanıcı/manuel kurulumlar** (Java yükleyici ile kurulmuş): `~/.i2p/i2psnark/`
- **Sistem/daemon kurulumlar** (apt-get veya paket yöneticisi ile kurulmuş): `/var/lib/i2p/i2p-config/i2psnark/`

BiglyBT kullanıcıları indirdikleri dosyaları yapılandırılmış indirmeler dizininde bulacaktır.

### Cloning from the Bundle

**Standart yöntem** (çoğu durumda çalışır):

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Eğer `fatal: multiple updates for ref` hataları ile karşılaşırsanız (Git 2.21.0 ve sonraki sürümlerde global Git yapılandırmasında çakışan fetch refspec'leri bulunduğunda bilinen bir sorun), manuel başlatma yöntemini kullanın:

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternatif olarak, `--update-head-ok` bayrağını kullanabilirsiniz:

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Bundle Dosyasını Edinme

Bundle'dan klonladıktan sonra, gelecekteki fetch işlemlerinin I2P veya clearnet üzerinden gitmesi için klonunuzu canlı remote'a yönlendirin:

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Veya clearnet erişimi için:

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
I2P SSH erişimi için, I2P router konsolunuzda `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p` adresine işaret eden yapılandırılmış bir SSH istemci tüneline ihtiyacınız vardır (genellikle 7670 portu). Standart olmayan bir port kullanıyorsanız:

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Paketten Klonlama

Deponuzun **tam bir klon** (yüzeysel olmayan) ile tamamen güncel olduğundan emin olun:

```bash
git fetch --all
```
Eğer sığ bir klonunuz varsa, önce onu dönüştürün:

```bash
git fetch --unshallow
```
### Canlı Uzak Sunucuya Geçiş

**Ant derleme hedefini kullanma** (I2P kaynak ağacı için önerilir):

```bash
ant git-bundle
```
Bu, hem `i2p.i2p.bundle` (bundle dosyası) hem de `i2p.i2p.bundle.torrent` (BitTorrent metaverileri) dosyalarını oluşturur.

**git bundle'ı doğrudan kullanma**:

```bash
git bundle create i2p.i2p.bundle --all
```
Daha seçici paketler için:

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Dağıtmadan önce paketi her zaman doğrulayın:

```bash
git bundle verify i2p.i2p.bundle
```
Bu, bundle'ın geçerli olduğunu doğrular ve gerekli ön koşul commit'leri gösterir.

### Ön Koşullar

Paketi ve torrent meta verilerini I2PSnark dizininize kopyalayın:

**Kullanıcı kurulumları için**:

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Sistem kurulumları için**:

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark, .torrent dosyalarını saniyeler içinde otomatik olarak algılar ve yükler. Seed yapmaya başlamak için [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) adresindeki web arayüzüne erişin.

## 4. Creating Incremental Bundles

Periyodik güncellemeler için, son paketten bu yana yalnızca yeni commit'leri içeren artımlı paketler oluşturun:

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Kullanıcılar, temel depoyu zaten indirmişlerse artımlı paketten çekebilirler:

```bash
git fetch /path/to/update.bundle
```
Her zaman artımlı paketlerin beklenen önkoşul commit'leri gösterdiğini doğrulayın:

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Bundle'dan çalışan bir deponuz olduğunda, onu diğer Git klonları gibi kullanın:

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Ya da daha basit iş akışları için:

```bash
git fetch origin
git pull origin master
```
## 3. Bir Paket Oluşturma

- **Dayanıklı dağıtım**: Büyük depolar BitTorrent üzerinden paylaşılabilir; BitTorrent yeniden denemeleri, parça doğrulamayı ve devam etmeyi otomatik olarak yönetir.
- **Eşler arası önyükleme**: Yeni katkıda bulunanlar, klonlarını I2P ağındaki yakın eşlerden önyükleyebilir, ardından artımlı değişiklikleri doğrudan Git sunucularından alabilir.
- **Azaltılmış sunucu yükü**: Yansılar, özellikle büyük depolar veya yavaş ağ koşulları için canlı Git sunucuları üzerindeki baskıyı hafifletmek amacıyla periyodik paketler yayınlayabilir.
- **Çevrimdışı aktarım**: Paketler yalnızca BitTorrent ile değil, herhangi bir dosya aktarım yöntemiyle (USB sürücüler, doğrudan aktarımlar, sneakernet) çalışır.

Paketler canlı uzak sunucuların yerini almaz. Bunlar sadece ilk klonlama veya büyük güncellemeler için daha dayanıklı bir başlatma yöntemi sağlar.

## 7. Troubleshooting

### Paketi Oluşturma

**Sorun**: Bundle oluşturma başarılı oluyor ancak diğerleri bundle'dan klonlama yapamıyor.

**Sebep**: Kaynak klonunuz sığ (shallow) bir klon (`--depth` ile oluşturulmuş).

**Çözüm**: Paketler oluşturmadan önce tam klona dönüştürün:

```bash
git fetch --unshallow
```
### Paketinizi Doğrulama

**Sorun**: Bundle'dan klonlarken `fatal: multiple updates for ref` hatası.

**Sebep**: Git 2.21.0+ sürümü `~/.gitconfig` dosyasındaki global fetch refspec'leri ile çakışıyor.

**Çözümler**: 1. Manuel başlatma kullanın: `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. `--update-head-ok` bayrağını kullanın: `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Çakışan yapılandırmayı kaldırın: `git config --global --unset remote.origin.fetch`

### I2PSnark ile Dağıtım

**Sorun**: `git bundle verify` eksik önkoşulları bildiriyor.

**Neden**: Artımlı paket veya eksik kaynak klonu.

**Çözüm**: Ya önkoşul commit'lerini çekin ya da önce temel paketi kullanın, ardından artımlı güncellemeleri uygulayın.
