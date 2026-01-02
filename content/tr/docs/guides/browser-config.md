---
title: "Web Tarayıcı Yapılandırması"
description: "Masaüstü ve Android'de popüler tarayıcıları I2P'nin HTTP/HTTPS proxy'lerini kullanacak şekilde yapılandırma"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: dokümantasyon
---

Bu kılavuz, yaygın tarayıcıların I2P'nin yerleşik HTTP proxy'si üzerinden trafik göndermesi için nasıl yapılandırılacağını gösterir. Safari, Firefox ve Chrome/Chromium tarayıcılarını ayrıntılı adım adım talimatlarla kapsar.

**Önemli Notlar**:

- I2P'nin varsayılan HTTP proxy'si `127.0.0.1:4444` adresini dinler.
- I2P, I2P ağı içindeki trafiği korur (.i2p siteleri).
- Tarayıcınızı yapılandırmadan önce I2P router'ınızın çalıştığından emin olun.

## Safari (macOS)

Safari, macOS'ta sistem genelindeki proxy ayarlarını kullanır.

### Step 1: Open Network Settings

1. **Safari**'yi açın ve **Safari → Ayarlar** (veya **Tercihler**) menüsüne gidin
2. **Gelişmiş** sekmesine tıklayın
3. **Proxy'ler** bölümünde **Ayarları Değiştir...** seçeneğine tıklayın

Bu, Mac'inizin Sistem Ağ Ayarları'nı açacaktır.

![Safari Gelişmiş Ayarlar](/images/guides/browser-config/accessi2p_1.png)

### Adım 1: Ağ Ayarlarını Açın

1. Ağ ayarlarında, **Web Proxy (HTTP)** seçeneğinin kutusunu işaretleyin
2. Aşağıdakileri girin:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. Ayarlarınızı kaydetmek için **Tamam**'a tıklayın

![Safari Proxy Yapılandırması](/images/guides/browser-config/accessi2p_2.png)

Artık Safari'de `.i2p` sitelerine göz atabilirsiniz!

**Not**: Bu proxy ayarları, macOS sistem proxy'lerini kullanan tüm uygulamaları etkileyecektir. I2P tarayıcı kullanımını izole etmek istiyorsanız, ayrı bir kullanıcı hesabı oluşturmayı veya yalnızca I2P için farklı bir tarayıcı kullanmayı düşünün.

## Firefox (Desktop)

Firefox, sistemden bağımsız kendi proxy ayarlarına sahiptir, bu da onu özel I2P taraması için ideal kılar.

### Adım 2: HTTP Proxy'yi Yapılandırın

1. Sağ üstteki **menü düğmesine** (☰) tıklayın
2. **Ayarlar**'ı seçin

![Firefox Ayarları](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Ayarlar arama kutusuna **"proxy"** yazın
2. **Ağ Ayarları**'na kaydırın
3. **Ayarlar...** düğmesine tıklayın

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Adım 1: Ayarları Açın

1. **Manuel vekil sunucu yapılandırması**'nı seçin
2. Aşağıdakileri girin:
   - **HTTP Proxy**: `127.0.0.1` **Port**: `4444`
3. **SOCKS Host** alanını boş bırakın (özellikle SOCKS proxy'ye ihtiyacınız olmadığı sürece)
4. Yalnızca SOCKS proxy kullanıyorsanız **Proxy DNS when using SOCKS** seçeneğini işaretleyin
5. Kaydetmek için **Tamam**'a tıklayın

![Firefox Manuel Proxy Yapılandırması](/images/guides/browser-config/accessi2p_5.png)

Artık Firefox'ta `.i2p` sitelerine göz atabilirsiniz!

**İpucu**: I2P tarama için ayrılmış ayrı bir Firefox profili oluşturmayı düşünün. Bu, I2P taramanızı normal taramadan izole tutar. Bir profil oluşturmak için Firefox adres çubuğuna `about:profiles` yazın.

## Chrome / Chromium (Desktop)

Chrome ve Chromium tabanlı tarayıcılar (Brave, Edge, vb.) genellikle Windows ve macOS'ta sistem proxy ayarlarını kullanır. Bu kılavuz Windows yapılandırmasını gösterir.

### Adım 2: Proxy Ayarlarını Bulun

1. Sağ üst köşedeki **üç nokta menüsüne** (⋮) tıklayın
2. **Settings** seçeneğini seçin

![Chrome Ayarları](/images/guides/browser-config/accessi2p_6.png)

### Adım 3: Manuel Proxy Yapılandırması

1. Ayarlar arama kutusuna **"proxy"** yazın
2. **Bilgisayarınızın proxy ayarlarını aç** seçeneğine tıklayın

![Chrome Proxy Araması](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Bu, Windows Ağ ve İnternet ayarlarını açacaktır.

1. **Manuel proxy kurulumu**'na kadar aşağı kaydırın
2. **Ayarla**'ya tıklayın

![Windows Proxy Kurulumu](/images/guides/browser-config/accessi2p_8.png)

### Adım 1: Chrome Ayarlarını Açın

1. **Proxy sunucusu kullan** seçeneğini **Açık** konuma getirin
2. Aşağıdakileri girin:
   - **Proxy IP adresi**: `127.0.0.1`
   - **Port**: `4444`
3. İsteğe bağlı olarak, **"Şununla başlayan adresler için proxy sunucusu kullanma"** bölümüne istisnalar ekleyin (örn., `localhost;127.*`)
4. **Kaydet**'e tıklayın

![Chrome Proxy Yapılandırması](/images/guides/browser-config/accessi2p_9.png)

Artık Chrome'da `.i2p` sitelerine göz atabilirsiniz!

**Not**: Bu ayarlar Windows'ta tüm Chromium tabanlı tarayıcıları ve diğer bazı uygulamaları etkiler. Bundan kaçınmak için, bunun yerine özel bir I2P profili ile Firefox kullanmayı düşünün.

### Adım 2: Proxy Ayarlarını Açın

Linux'ta, sistem ayarlarını değiştirmekten kaçınmak için Chrome/Chromium'u proxy bayraklarıyla başlatabilirsiniz:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Veya bir masaüstü başlatıcı betiği oluşturun:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
`--user-data-dir` bayrağı I2P taraması için ayrı bir Chrome profili oluşturur.

## Firefox (Masaüstü)

Modern "Fenix" Firefox sürümleri varsayılan olarak about:config ve eklentileri kısıtlar. IceRaven, seçilmiş bir eklenti setini etkinleştiren ve proxy kurulumunu basitleştiren bir Firefox türevi (fork) yazılımdır.

Uzantı tabanlı yapılandırma (IceRaven):

1) Eğer zaten IceRaven kullanıyorsanız, önce tarayıcı geçmişini temizlemeyi düşünün (Menü → Geçmiş → Geçmişi Sil). 2) Menü → Eklentiler → Eklenti Yöneticisi'ni açın. 3) "I2P Proxy for Android and Other Systems" uzantısını yükleyin. 4) Tarayıcı artık I2P üzerinden proxy kullanacaktır.

Bu eklenti, [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/)'dan kurulduğunda Fenix öncesi Firefox tabanlı tarayıcılarda da çalışır.

Firefox Nightly'da geniş eklenti desteğini etkinleştirmek, [Mozilla tarafından belgelenen](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/) ayrı bir süreç gerektirir.

## Internet Explorer / Windows System Proxy

Windows'ta sistem proxy diyalogu IE için geçerlidir ve Chromium tabanlı tarayıcılar sistem ayarlarını miras aldığında kullanılabilir.

1) "Ağ ve İnternet Ayarları" → "Proxy" açın. 2) "LAN için bir proxy sunucusu kullan" seçeneğini etkinleştirin. 3) HTTP için adres `127.0.0.1`, port `4444` olarak ayarlayın. 4) İsteğe bağlı olarak "Yerel adresler için proxy sunucusunu atla" seçeneğini işaretleyin.
