---
title: "SAMv3"
description: "Java dışı I2P uygulamaları için Basit Anonim Mesajlaşma protokolü"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM, I2P ile etkileşim kurmak için basit bir istemci protokolüdür. SAM, Java dışı uygulamaların I2P ağına bağlanması için önerilen protokoldür ve birden fazla yönlendirici uygulaması tarafından desteklenir. Java uygulamaları doğrudan streaming veya I2CP API'lerini kullanmalıdır.

SAM sürüm 3, I2P 0.7.3 sürümünde (Mayıs 2009) tanıtıldı ve kararlı, desteklenen bir arayüzdür. 3.1 sürümü de kararlıdır ve kesinlikle önerilen imza türü seçeneğini destekler. Daha yeni 3.x sürümleri gelişmiş özellikleri destekler. i2pd'nin şu anda çoğu 3.2 ve 3.3 özelliğini desteklemediğine dikkat edin.

Alternatifler: [SOCKS](/docs/api/socks), [Akış](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (eski)](/docs/api/bob). Kullanımdan kaldırılan sürümler: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Bilinen SAM Kütüphaneleri

Uyarı: Bunlardan bazıları çok eski olabilir veya desteklenmeyebilir. Aşağıda belirtilmedikçe, hiçbir tanesi I2P projesi tarafından test edilmemiş, incelenmemiş veya sürdürülmüştür. Kendi araştırmanızı yapın.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Hızlı Başlangıç

Temel bir yalnızca TCP'ye dayalı, eşten eşe uygulama uygulamak için istemcinin aşağıdaki komutları desteklemesi gerekir:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Geri kalan tüm komutlar için gereklidir
- `DEST GENERATE SIGNATURE_TYPE=7` - Özel anahtarımızı ve hedefimizi oluşturmak için
- `NAMING LOOKUP NAME=...` - .i2p adreslerini hedeflere dönüştürmek için
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - STREAM CONNECT ve STREAM ACCEPT için gereklidir
- `STREAM CONNECT ID=... DESTINATION=...` - Giden bağlantılar oluşturmak için
- `STREAM ACCEPT ID=...` - Gelen bağlantıları kabul etmek için

## Geliştiriciler için Genel Rehberlik

### Uygulama Tasarımı

SAM oturumları (veya I2P içinde tünel havuzları ya da tünel kümeleri) uzun ömürlü olacak şekilde tasarlanmıştır. Çoğu uygulamanın yalnızca başlangıçta oluşturulup çıkışta kapatılan bir oturuma ihtiyacı olacaktır. Tor'dan farklı olarak, I2P'de devreler hızlı bir şekilde oluşturulup atılamaz. Uygulamanızı eş zamanlı olarak bir veya iki oturumdan fazla kullanacak şekilde tasarlamadan veya oturumları hızlıca oluşturup yok etmeden önce dikkatlice düşünün ve I2P geliştiricileriyle görüşün. Çoğu tehdit modeli, her bağlantı için benzersiz bir oturum gerektirmez.

Ayrıca, uygulama ayarlarınızın (ve kullanıcılarınıza yönlendirici ayarları hakkında verdiğiniz rehberliğin veya bir yönlendirici paketliyorsanız yönlendiricinin öntanımlı ayarlarının) kullanıcılarınızın ağa tükettiklerinden daha fazla kaynak katkıda bulunmasını sağlayacak şekilde ayarlandığından emin olun. I2P eşten eşe bir ağdır ve popüler bir uygulama ağı sürekli tıkanıklığa sürüklerse ağ hayatta kalamaz.

### Uyumluluk ve Test Etme

Java I2P ve i2pd yönlendirici uygulamaları bağımsızdır ve davranış, özellik desteği ve varsayılanlarda küçük farklılıklar içerir. Lütfen uygulamanızı her iki yönlendiricinin de en son sürümüyle test edin.

i2pd SAM varsayılan olarak etkindir; Java I2P SAM etkin değildir. Kullanıcılarınıza Java I2P'de SAM'ı nasıl etkinleştireceklerine dair talimatlar verin (yönlendirici konsolundaki /configclients üzerinden), ve/veya ilk bağlantı başarısız olursa kullanıcıya "I2P'nin çalıştığından ve SAM arayüzünün etkin olduğundan emin olun" gibi açıklayıcı bir hata mesajı gösterin.

Java I2P ve i2pd yönlendiricileri tünel miktarları için farklı varsayılan değerlere sahiptir. Java varsayılanı 2 iken, i2pd varsayılanı 5'tir. Genellikle düşük ila orta bant genişliği ve düşük ila orta bağlantı sayısına sahip sistemler için 2 veya 3 yeterlidir. Java I2P ve i2pd yönlendiricileriyle tutarlı performans elde etmek için LİNK OLUŞTUR (SESSION CREATE) mesajında tünel miktarını belirtin. Aşağıya bakın.

Uygulamanızın yalnızca ihtiyaç duyduğu kaynakları kullandığından emin olmak için geliştiricilere yönelik daha fazla kılavuz için lütfen [uygulamanızla birlikte I2P'yi paketleme kılavuzumuza](/docs/applications/embedding) bakın.

### İmza ve Şifreleme Türleri

I2P, birden fazla imza ve şifreleme türünü destekler. Geriye dönük uyumluluk için SAM, eski ve verimsiz türlere öntanımlı olarak geçer, bu yüzden tüm istemciler daha yeni türleri belirtmelidir.

İmza türü, GEÇİCİ için DEST GENERATE ve SESSION CREATE komutlarında belirtilir. Tüm istemciler `SIGNATURE_TYPE=7` (Ed25519) olarak ayarlanmalıdır.

Şifreleme türü, OTURUM OLUŞTUR (SESSION CREATE) komutunda belirtilir. Birden fazla şifreleme türüne izin verilir. İstemciler, `i2cp.leaseSetEncType=4` (sadece ECIES-X25519 için) veya `i2cp.leaseSetEncType=6,4` (API 0.9.67 veya üzerini destekleyen yönlendiriciler için MLKEM-768 ve ECIES-X25519 için) ayarlamalıdır.

## Sürüm 3 Değişiklikleri

### Sürüm 3.0 Değişiklikleri

3.0 sürümü, I2P 0.7.3 sürümünde tanıtıldı. SAM v2, aynı I2P hedefindeki birkaç soketi *paralel* olarak yönetmenin bir yolunu sundu; yani istemci, bir soketteki verinin başarıyla gönderilmesini beklemeden başka bir sokette veri gönderebilir. Ancak tüm veri, istemci tarafından yönetilmesi oldukça karmaşık olan aynı istemci-SAM soketinden geçiyordu.

SAM v3, soketleri farklı bir şekilde yönetir: her *I2P soketi*, benzersiz bir istemci-SAM soketine eşleşir ve bu işlemi yönetmek çok daha basittir. Bu, [BOB](/docs/api/bob) ile benzerdir.

SAM v3 ayrıca I2P üzerinden veriagram göndermek için bir UDP portu sunar ve I2P veriagramlarını istemcinin veriagram sunucusuna geri iletebilir.

### Sürüm 3.1 Değişiklikleri

Sürüm 3.1, Java I2P 0.9.14 sürümünde (Temmuz 2014) tanıtıldı. SAM 3.1, SAM 3.0'a göre daha iyi imza türlerini desteklediği için önerilen en düşük SAM uygulamasıdır. i2pd ayrıca 3.1'in çoğu özelliğini destekler.

- DEST GENERATE ve SESSION CREATE artık bir SIGNATURE_TYPE parametresini destekliyor.
- HELLO VERSION içindeki MIN ve MAX parametreleri artık isteğe bağlıdır.
- HELLO VERSION içindeki MIN ve MAX parametreleri artık "3" gibi tek basamaklı sürümleri destekliyor.
- RAW SEND artık köprü soketinde destekleniyor.

### Sürüm 3.2 Değişiklikleri

Sürüm 3.2, Java I2P 0.9.24 sürümünde (Ocak 2016) tanıtıldı. i2pd'nin şu anda çoğu 3.2 özelliğini desteklemediğine dikkat edin.

#### I2CP Bağlantı Noktası ve Protokol Desteği

- OTURUM OLUŞTUR seçeneği FROM_PORT ve TO_PORT
- OTURUM OLUŞTUR STYLE=RAW seçeneği PROTOCOL
- AKIŞ BAĞLANTISI, DATAGRAM GÖNDER ve HAM GÖNDER seçenekleri FROM_PORT ve TO_PORT
- HAM GÖNDER seçeneği PROTOCOL
- DATAGRAM ALINDI, HAM ALINDI ve iletilen veya alınan akışlar ve yanıtlanabilir datagramlar, FROM_PORT ve TO_PORT içerir
- HAM oturum seçeneği HEADER=true, iletilen ham datagramların başına PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn içeren bir satır ekler
- Artık 7655 numaralı bağlantı üzerinden gönderilen datagramların ilk satırı herhangi bir 3.x sürümüyle başlayabilir
- 7655 numaralı bağlantı üzerinden gönderilen datagramların ilk satırı FROM_PORT, TO_PORT, PROTOCOL seçeneklerinden herhangi birini içerebilir
- HAM ALINDI, PROTOCOL=nnn değerini içerir

#### SSL ve Kimlik Doğrulama

- Yetkilendirme için HELLO parametrelerinde KULLANICI/ŞİFRE. [Aşağıya](#authorization) bakın.
- İsteğe bağlı yetkilendirme yapılandırması AUTH komutu ile. [Aşağıya](#authorization-configuration-sam-32-or-higher-optional-feature) bakın.
- Kontrol soketinde isteğe bağlı SSL/TLS desteği. [Aşağıya](#ssl) bakın.
- STREAM FORWARD seçeneği SSL=true

#### Çoklu iş parçacığı

- Aynı oturum kimliği üzerinde eşzamanlı bekleyen STREAM ACCEPT'lere izin verilir.

#### Komut Satırı Ayrıştırma ve Canlı Tutma

- Oturumu ve soketi kapatmak için isteğe bağlı komutlar: QUIT, STOP ve EXIT. [Aşağıya](#quitstopexitinvisible-sam-32-or-higher-optional-features) bakın.
- Komut ayrıştırması UTF-8'yi doğru şekilde işleyecektir.
- Komut ayrıştırması tırnak içindeki boşlukları güvenilir bir şekilde işler.
- Komut satırında tırnak işaretlerini kaçışlamak için bir ters eğik çizgi '\\' kullanılabilir.
- Sunucunun komutları test sürecini kolaylaştırmak için telnet üzerinden büyük harfe dönüştürmesi önerilir.
- PROTOCOL veya PROTOCOL= gibi boş seçenek değerlerine izin verilebilir, uygulamaya bağlıdır.
- Sürekli bağlantı için PING/PONG. Aşağıya bakın.
- Sunucular HELLO veya sonraki komutlar için zaman aşımı uygulayabilir, uygulamaya bağlıdır.

### Sürüm 3.3 Değişiklikleri

Sürüm 3.3, Java I2P 0.9.25 sürümünde (Mart 2016) tanıtıldı. i2pd'nin şu anda çoğu 3.3 özelliğini desteklemediğine dikkat edin.

- Aynı oturum aynı anda akışlar, datagramlar ve ham veri için kullanılabilir. Gelen paketler ve akışlar I2P protokolüne ve hedef portuna göre yönlendirilir. Aşağıdaki [BİRİNCİL oturumlar bölümüne](#sam-primary-sessions-v33-and-higher) bakın.
- DATAGRAM GÖNDER ve HAM GÖNDER artık SEND_TAGS, TAG_THRESHOLD, EXPIRES ve SEND_LEASESET seçeneklerini desteklemektedir. Aşağıdaki [datagram gönderme bölümüne](#sending-repliable-or-raw-datagrams) bakın.

### 2025-04 Değişiklikler

Nisan 2025'te burada belirtmeye iki öneri onaylanarak dahil edildi. Desteği gösteren bir sürüm değişikliği yoktur. Bazı uygulamalar henüz desteklemiyor ve diğer uygulamalarda destek ön karardır.

- Datagram 2/3 desteği (öneri 163). OTURUM OLUŞTUR ve OTURUM EKLE'de (alt oturumlar) belirtilir. Aşağıya bakın.
- LeaseSet seçeneklerinin alınması (öneri 167). AD ARAMA SEÇENEKLERİ=true ile belirtilir. Aşağıya bakın.

## Sürüm 3 Protokolü

### Basit Anonim Mesajlaşma (SAM) Sürüm 3.3 Özellikleri Genel Bakış

İstemci uygulaması, I2P işlevselliğinin tamamını yöneten SAM köprüsüyle konuşur (sanal akışlar için [akış kütüphanesi](/docs/api/streaming) veya datagramlar için doğrudan [I2CP](/docs/protocol/i2cp) kullanarak).

Varsayılan olarak, istemci ile SAM köprüsü arasındaki iletişim şifrelenmemiş ve kimliği doğrulanmamıştır. SAM köprüsü SSL/TLS bağlantılarını destekleyebilir; yapılandırma ve uygulama ayrıntıları bu belgenin kapsamı dışındadır. SAM 3.2'den itibaren, başlangıç el sıkışmasında isteğe bağlı kimlik doğrulama kullanıcı adı/parola parametreleri desteklenir ve köprü tarafından zorunlu kılınabilir.

I2P iletişimleri birkaç farklı biçimde olabilir:

- [Sanal akışlar](/docs/api/streaming)
- [Yanıtlamalı ve kimliği doğrulanmış veri birimleri](/docs/specs/datagrams#repliable) (FROM alanı içeren iletiler)
- [Anonim veri birimleri](/docs/specs/datagrams#raw) (ham anonim iletiler)
- [Datagram2](/docs/specs/datagrams#datagram2) (yeni bir yanıtlamalı ve kimliği doğrulanmış biçim)
- [Datagram3](/docs/specs/datagrams#datagram3) (yeni bir yanıtlamalı ancak kimliği doğrulanmamış biçim)

I2P iletişimleri, I2P oturumları tarafından desteklenir ve her I2P oturumu bir adrese (hedef olarak adlandırılır) bağlanır. Bir I2P oturumu yukarıdaki üç türden biriyle ilişkilidir ve [BİRİNCİL oturumlar](#sam-primary-sessions-v33-and-higher) kullanılmadığı sürece başka türdeki iletişimleri taşıyamaz.

### Kodlama ve Kaçış

Bu SAM mesajlarının tümü tek bir satırda gönderilir ve yeni satır karakteriyle (\\n) sonlandırılır. SAM 3.2'ye kadar yalnızca 7 bitlik ASCII destekleniyordu. SAM 3.2'den itibaren kodlama UTF-8 olmalıdır. Herhangi bir UTF8 ile kodlanmış anahtar veya değer düzgün çalışmalıdır.

Aşağıdaki bu belgede gösterilen biçimlendirme yalnızca okunabilirlik içindir ve her mesajdaki ilk iki kelimenin belirli sıralarında kalması gerekse de, anahtar=değer çiftlerinin sırası değişebilir (örneğin "ONE TWO A=B C=D" veya "ONE TWO C=D A=B" her ikisi de tamamen geçerli yapılardır). Ek olarak protokol büyük/küçük harfe duyarlıdır. Aşağıdaki örneklerde, istemci tarafından SAM köprüsüne gönderilen mesajlar "->" ile, SAM köprüsü tarafından istemciye gönderilen mesajlar ise "<-" ile işaretlenmiştir.

Temel komut veya yanıt satırı aşağıdaki formlardan birini alır:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
SAM 3.2'de yalnızca bazı yeni komutlar için BİR ALT KOMUTSIZ KOMUT desteklenir.

Anahtar=değer çiftleri tek bir boşlukla ayrılmalıdır. (SAM 3.2'den itibaren, birden fazla boşluk kullanılmasına izin verilir) Değerler boşluk içeriyorsa çift tırnak içine alınmalıdır, örneğin key="uzun değer metni". (SAM 3.2'den önce bazı uygulamalarda bu, güvenilir şekilde çalışmıyordu)

SAM 3.2'den önce kaçış mekanizması yoktu. SAM 3.2 itibarıyla çift tırnaklar bir ters eğik çizgiyle '\\', ters eğik çizgi ise iki ters eğik çizgiyle '\\\\' temsil edilebilir.

### Boş Değerler

SAM 3.2 itibarıyla, KEY, KEY= veya KEY="" gibi boş seçenek değerlerine izin verilebilir ve bu durum uygulamaya bağlıdır.

### Büyük/Küçük Harf Duyarlılığı

Belirtildiği gibi protokol, büyük/küçük harfe duyarlıdır. Telnet üzerinden test etmeyi kolaylaştırmak için sunucunun komutları büyük harfe dönüştürmesi önerilir ancak zorunlu değildir. Bu, örneğin "hello version" komutunun çalışmasına olanak tanır. Bu durum, uygulamaya bağlıdır. [I2CP](/docs/protocol/i2cp) seçeneklerinin bozulmasına neden olacağı için anahtarları veya değerleri büyük harfe dönüştürmeyin.

### SAM Bağlantı El Sıkışması

İstemci ve köprü, bir protokol sürümünde anlaşana kadar SAM iletişimi gerçekleşemez ve bu, istemcinin bir HELLO göndermesi ve köprünün bir HELLO REPLY göndermesiyle yapılır:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
ve

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
3.1 sürümünden itibaren (I2P 0.9.14), MIN ve MAX parametreleri isteğe bağlıdır. SAM, verilen MIN ve MAX sınırlamalarına göre mümkün olan en yüksek sürümü döndürür veya hiçbir sınırlama verilmemişse geçerli sunucu sürümünü döndürür.

Eğer SAM köprüsü uygun bir versiyon bulamazsa şu şekilde yanıt verir:

```
<- HELLO REPLY RESULT=NOVERSION
```
Eğer kötü bir istek formatı gibi bir hata oluşursa, şu şekilde yanıt verir:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

Sunucunun kontrol soketi, sunucu ve istemci tarafından yapılandırıldığı şekilde isteğe bağlı olarak SSL/TLS destekleyebilir. Uygulamalar diğer taşıma katmanlarını da sunabilir; bu, protokol tanımının kapsamı dışında kalır.

#### Yetkilendirme

Yetkilendirme için, istemci HELLO parametrelerine USER="xxx" PASSWORD="yyy" ekler. Kullanıcı adı ve parola için çift tırnak kullanımı önerilir ancak zorunlu değildir. Kullanıcı adı veya paroladaki bir çift tırnak işareti ters eğik çizgi ile kaçrılmalıdır. Başarısızlık durumunda sunucu bir I2P_ERROR ve mesaj ile yanıt verir. Yetkilendirme gerektiren SAM sunucularında SSL'nin etkinleştirilmesi önerilir.

#### Zaman Aşımı

Sunucular, HELLO veya sonraki komutlar için uygulamaya bağlı zaman aşımları uygulayabilir. İstemciler, bağlandıktan sonra HELLO ve bir sonraki komutu derhal göndermelidir.

HELLO alındadan önce bir zaman aşımı olursa, köprü şu şekilde yanıt verir:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
ve ardından bağlantıyı keser.

HELLO alındıktan sonra ancak bir sonraki komuttan önce zaman aşımı olursa, köprü şu şekilde yanıt verir:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
ve ardından bağlantıyı keser.

### I2CP Bağlantı Noktaları ve Protokolü

SAM 3.2 itibariyle, [I2CP](/docs/protocol/i2cp) portları ve protokolü, SAM istemcisi tarafından gönderici tarafından [I2CP](/docs/protocol/i2cp)'ye iletilmek üzere belirtilebilir ve SAM köprüsü, alınan [I2CP](/docs/protocol/i2cp) portu ve protokol bilgisini SAM istemcisine iletecektir.

FROM_PORT ve TO_PORT için geçerli aralık 0-65535'tir ve varsayılan değer 0'dır.

YALIN için belirtilebilecek PROTOCOL (protokol) değeri için geçerli aralık 0-255'tir ve varsayılan değer 18'dir.

SESSION komutları için belirtilen portlar ve protokol, bu oturum için varsayılan değerlerdir. Bireysel akışlar veya veriagramlar için belirtilen portlar ve protokol, oturum varsayılanlarının üzerine yazar. Alınan akışlar veya veriagramlar için belirtilen portlar ve protokol, [I2CP](/docs/protocol/i2cp)'den alınanlara göre gösterilir.

#### Standart IP'den Önemli Farklılıklar

I2CP portları, I2P soketleri ve veriagramları içindir. SAM'a bağlanan yerel soketlerinizle ilgisi yoktur.

- Port 0 geçerlidir ve özel bir anlamı vardır.
- 1-1023 arası portlar özel veya ayrıcalıklı değildir.
- Sunucular varsayılan olarak "tüm portlar" anlamına gelen port 0'da dinler.
- İstemciler varsayılan olarak "herhangi bir port" anlamına gelen port 0'a gönderim yapar.
- İstemciler varsayılan olarak "belirsiz" anlamına gelen port 0'dan gönderim yapar.
- Sunucular, port 0'da çalışan bir hizmete ve daha yüksek portlarda çalışan diğer hizmetlere sahip olabilir. Bu durumda port 0 hizmeti varsayılan olur ve gelen soket veya datagram portu başka bir hizmetle eşleşmiyorsa bu hizmete bağlanılır.
- Çoğu I2P hedefinde yalnızca bir hizmet çalışır; bu yüzden varsayılanları kullanabilir ve I2CP port yapılandırmasını göz ardı edebilirsiniz.
- I2CP portlarını belirtmek için SAM 3.2 veya 3.3 gereklidir.
- I2CP portlarına ihtiyacınız yoksa, SAM 3.2 veya 3.3'e de ihtiyacınız yoktur; 3.1 yeterlidir.
- Protokol 0 geçerlidir ve "herhangi bir protokol" anlamına gelir. Bu önerilmez ve büyük olasılıkla çalışmaz.
- I2P soketleri dahili bir bağlantı kimliği (ID) ile izlenir. Bu nedenle, dest:port:dest:port:protokol 5-lisine benzersiz olma zorunluluğu yoktur. Örneğin, iki hedef arasında aynı portlara sahip birden fazla soket olabilir. İstemciler, giden bir bağlantı için "boş port" seçmek zorunda değildir.

Birden fazla alt oturum içeren bir SAM 3.3 uygulaması geliştiriyorsanız, port ve protokolleri nasıl etkili kullanacağınızı dikkatlice düşünün. Daha fazla bilgi için [I2CP](/docs/protocol/i2cp) spesifikasyonuna bakın.

### SAM Oturumları

Bir SAM oturumu, istemcinin SAM köprüsüne bir soket açarak, el sıkışma gerçekleştirmesi ve SESSION CREATE (OTURUM OLUŞTUR) mesajı göndermesiyle oluşturulur ve soket bağlantısı kesildiğinde oturum sona erer.

Kayıtlı her I2P Hedefi, benzersiz bir oturum kimliği (veya takma ad) ile ilişkilidir. BİRİNCİL oturumlar için alt oturum kimlikleri de dahil olmak üzere oturum kimlikleri, SAM sunucusu üzerinde küresel olarak benzersiz olmalıdır. Diğer istemcilerle olası kimlik çakışmalarını önlemek için, istemcinin kimlikleri rastgele üretmesi en iyi uygulamadır.

Her oturum, aşağıdakilerle eşsiz şekilde ilişkilidir:

- istemcinin oturumu oluşturduğu soket
- kimliği (veya takma adı)

#### Oturum Oluşturma İsteği

Oturum oluşturma mesajı yalnızca bu formlardan birini kullanabilir (diğer formlar aracılığıyla alınan mesajlar hata mesajıyla yanıtlanır):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
HEDİS, mesaj/akışların gönderilmesi ve alınması için kullanılacak hedefi belirtir. $privkey, [Hedef](/docs/specs/common-structures#type_Destination) ile başlayan, ardından [Özel Anahtar](/docs/specs/common-structures#type_PrivateKey) ve ardından [İmza Özel Anahtarı](/docs/specs/common-structures#type_SigningPrivateKey)'nın birleştirilmesinin base 64 formatıdır ve isteğe bağlı olarak [Çevrimdışı İmza](/docs/specs/common-structures#struct_OfflineSignature) ile devam edebilir. Bu değer, ikili formatta 663 veya daha fazla bayt, base 64 formatında ise imza türüne bağlı olarak 884 veya daha fazla bayttır. İkili format, Özel Anahtar Dosyası bölümünde belirtilmiştir. Aşağıdaki Hedef Anahtarı Oluşturma bölümünde [Özel Anahtar](/docs/specs/common-structures#type_PrivateKey) hakkında ek notlara bakın.

İmzalama özel anahtarı tümüyle sıfır ise, [Çevrimdışı İmza](/docs/specs/common-structures#struct_OfflineSignature) bölümü takip eder. Çevrimdışı imzalar yalnızca STREAM ve RAW oturumlar için desteklenir. Çevrimdışı imzalar DESTINATION=TRANSIENT ile oluşturulamaz. Çevrimdışı imza bölümünün biçimi şöyledir:

1. Bitiş zaman damgası (4 bayt, büyük endian, epoch'tan beri geçen saniye cinsinden, 2106'da sıfırlanır)
2. Geçici İmzalama Ortak Anahtarı'nın imza türü (2 bayt, büyük endian)
3. Geçici İmzalama Ortak Anahtarı (geçici imza türüne göre belirlenen uzunlukta)
4. Yukarıdaki üç alanın çevrimdışı anahtar ile imzası (hedef imza türüne göre belirlenen uzunlukta)
5. Geçici İmzalama Özel Anahtarı (geçici imza türüne göre belirlenen uzunlukta)

Hedef TRANSIENT olarak belirtildiyse, SAM köprüsü yeni bir hedef oluşturur. Sürüm 3.1'den itibaren (I2P 0.9.14), hedef TRANSIENT ise isteğe bağlı bir SIGNATURE_TYPE parametresi desteklenir. SIGNATURE_TYPE değeri [Key Certificates](/docs/specs/common-structures#type_Certificate) tarafından desteklenen herhangi bir isim (örneğin ECDSA_SHA256_P256, büyük/küçük harf duyarsız) veya sayı (örneğin 1) olabilir. Varsayılan değer DSA_SHA1'dir ve bu istenen şey DEĞİLDİR. Çoğu uygulama için lütfen SIGNATURE_TYPE=7 olarak belirtin.

$nickname istemcinin seçimidir. Boşluk karakterlerine izin verilmez.

Verilen ek seçenekler, SAM köprüsü tarafından yorumlanmazsa I2P oturum yapılandırmasına iletilir (örneğin outbound.length=0).

Java I2P ve i2pd yönlendiricileri tünel miktarları için farklı varsayılan değerlere sahiptir. Java'nın varsayılan değeri 2, i2pd'nin varsayılan değeri ise 5'tir. Genellikle düşük ila orta bant genişliği ve düşük ila orta bağlantı sayısı için 2 veya 3 yeterlidir. Java I2P ve i2pd yönlendiricileriyle tutarlı performans elde etmek için, SESSION CREATE mesajında tünel miktarlarını belirtin; örneğin, inbound.quantity=3 outbound.quantity=3 seçeneklerini kullanın. Bu ve diğer seçenekler [aşağıdaki bağlantılarda belgelenmiştir](#tunnel-i2cp-and-streaming-options).

SAM köprüsünün kendisi zaten I2P üzerinden iletişim kuracağı yönlendiriciyle yapılandırılmış olmalıdır (ancak gerekirse geçersiz kılma yapmanın bir yolu olabilir, örneğin i2cp.tcp.host=localhost ve i2cp.tcp.port=7654).

#### Oturum Oluşturma Yanıtı

Oturum oluşturma iletisini aldıktan sonra SAM köprüsü, şu şekilde bir oturum durumu iletisiyle yanıt verecektir:

Oluşturma işlemi başarılı olduysa:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey, [Destination](/docs/specs/common-structures#type_Destination) yapısının ardından [Private Key](/docs/specs/common-structures#type_PrivateKey) ve ardından [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)'in birleştirilmesinin base 64 formatıdır; isteğe bağlı olarak [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature) bu yapıyı takip edebilir. Bu değer, ikili formatta 663 veya daha fazla bayt, base 64 formatında ise imza türüne göre 884 veya daha fazla bayt uzunluğundadır. İkili format, Private Key File belirtiminde tanımlanmıştır.

EĞER OTURUM OLUŞTUR (SESSION CREATE) tüm sıfırlardan oluşan bir imzalama özel anahtarı ve [Çevrimdışı İmza](/docs/specs/common-structures#struct_OfflineSignature) bölümü içeriyorsa, OTURUM DURUMU (SESSION STATUS) yanıtı aynı veriyi aynı biçimde içerecektir. Ayrıntılar için yukarıdaki OTURUM OLUŞTUR bölümüne bakın.

Takma ad zaten bir oturumla ilişkilendirilmişse:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Hedef zaten kullanımdaysa:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Hedef geçerli bir özel hedef anahtarı değilse:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Başka bir hata oluştuysa:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Eğer uygun değilse, OTURUM'un neden oluşturulamadığını belirten insanın okuyabileceği bilgiler MESAJ'da yer almalıdır.

Yönlendiricinin SESSION STATUS yanıtı vermeden önce tüpler oluşturduğuna dikkat edin. Bu işlem birkaç saniye sürebilir veya yönlendirici başlangıcında ya da yoğun ağ tıkanıklığında bir dakikadan fazla sürebilir. Başarısız olursa, yönlendirici birkaç dakika boyunca bir hata mesajı ile yanıt vermeyecektir. Yanıtı beklerken kısa bir zaman aşımı ayarlamayın. Tüp oluşturma işlemi devam ederken oturumu terk etmeyin ve yeniden denemeyin.

SAM oturumları, ilişkilendirildikleri soketle birlikte başlar ve soket kapatıldığında sona erer. Soket kapatıldığında oturum sona erer ve oturumu kullanan tüm iletişimler aynı anda kesilir. Aynı şekilde, oturum herhangi bir nedenle sona erdiğinde SAM köprüsü soketi kapatır.

### SAM Sanal Akışları

Sanal akışların güvenilir bir şekilde ve sırayla iletilmesi garanti edilir ve başarısızlık veya başarı bildirimi, mevcut hemen anında iletilir.

Akışlar, iki I2P hedefi arasındaki çift yönlü iletişim soketleridir ancak açılması bunlardan biri tarafından istenmelidir. Bundan sonra, SAM istemcisi bu istek için CONNECT komutlarını kullanır. FORWARD / ACCEPT komutları ise SAM istemcisi, diğer I2P hedeflerinden gelen istekleri dinlemek istediğinde kullanılır.

### SAM Sanal Akışları: BAĞLAN

Bir istemci, bir bağlantıyı şu şekilde ister:

- SAM köprüsü ile yeni bir soket açmak
- yukarıdakiyle aynı HELLO el sıkışmasını iletmek
- STREAM CONNECT komutunu göndermek

#### Bağlantı İsteği

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Bu, kimliği $nickname olan yerel oturumdan belirtilen eş düğüme yeni bir sanal bağlantı kurar.

Hedef, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 hâlidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteridir (ikili sistemde 387 veya daha fazla bayt).

**NOT:** Yaklaşık 2014'ten beri (SAM v3.1), Java I2P, $destination için hostname'leri ve b32 adreslerini desteklemektedir, ancak bu daha önce belgelenmemişti. Hostname'ler ve b32 adresleri, 0.9.48 sürümünden itibaren resmi olarak Java I2P tarafından desteklenmektedir. i2pd yönlendiricisi, 2.38.0 (0.9.50) sürümünden itibaren hostname'leri ve b32 adreslerini desteklemektedir. Her iki yönlendirici için de "b32" desteği, körleştirilmiş hedefler için genişletilmiş "b33" adreslerini de içermektedir.

#### Bağlantı Yanıtı

SILENT=true geçilirse, SAM köprüsü sokette başka hiçbir mesaj göndermez. Bağlantı başarısız olursa, soket kapatılır. Bağlantı başarılı olursa, mevcut soketten geçen tüm kalan veriler bağlı I2P hedefi eşine ileri ve geri iletilir.

SILENT=false ise, ki bu varsayılan değerdir, SAM köprüsü soketi iletmek veya kapatmakten önce istemcisine son bir mesaj gönderir:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
SONUÇ değeri şunlardan biri olabilir:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
EĞER SONUÇ "OK" ise, mevcut soketten geçen kalan tüm veriler bağlı I2P hedefi eşine ileri ve geri yönlendirilir. Eğer bağlantı mümkün değilse (zaman aşımı, vb.), SONUÇ uygun hata değerini (isteğe bağlı insan tarafından okunabilir BİLDİRİM ile birlikte) içerir ve SAM köprüsü soketi kapatır.

Yönlendirici akış bağlantı zaman aşımı dahili olarak yaklaşık bir dakikadır ve uygulamaya bağlıdır. Yanıt için beklerken daha kısa bir zaman aşımı ayarlamayın.

### SAM Sanal Akışları: KABUL ET

Bir istemci, gelen bağlantı isteğini şu şekilde bekler:

- SAM köprüsü ile yeni bir soket açmak
- yukarıdakiyle aynı HELLO el sıkışmasını iletmek
- STREAM ACCEPT komutunu göndermek

#### İsteği Kabul Et

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Bu, oturumun ${nickname} I2P ağından gelen bir gelen bağlantı isteğini dinlemesini sağlar. Oturumda etkin bir FORWARD olduğu sürece ACCEPT'e izin verilmez.

SAM 3.2'den itibaren, aynı oturum kimliği üzerinde (aynı port ile bile) birden fazla eşzamanlı bekleyen STREAM ACCEPT işlemine izin verilir. 3.2'den önce, eşzamanlı kabuller ALREADY_ACCEPTING ile başarısız olurdu. Not: Java I2P, 0.9.24 (2016-01) sürümünden itibaren SAM 3.1'de eşzamanlı ACCEPT işlemlerini desteklemektedir. i2pd de 2.50.0 (2023-12) sürümünden itibaren SAM 3.1'de eşzamanlı ACCEPT işlemlerini desteklemektedir.

#### Yanıtı Kabul Et

SILENT=true parametresi verilirse, SAM köprüsü sokette başka hiçbir mesaj göndermez. Eğer accept işlemi başarısız olursa, soket kapatılır. Accept işlemi başarılı olursa, mevcut soketten geçen tüm kalan veri, bağlı I2P hedefiyle ileri ve geri iletilir. Güvenilirlik için ve gelen bağlantılar için hedefi alabilmek amacıyla SILENT=false yapılması önerilir.

SILENT=false ise, ki bu varsayılan değerdir, SAM köprüsü şununla yanıt verir:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
SONUÇ değeri şunlardan biri olabilir:

```
OK
I2P_ERROR
INVALID_ID
```
Sonuç TAMAM değilse, soket SAM köprüsü tarafından hemen kapatılır. Sonuç TAMAM ise, SAM köprüsü başka bir I2P eşinden gelen bir bağlantı isteğini beklemeye başlar. Bir istek geldiğinde, SAM köprüsü bunu kabul eder ve:

SILENT=true parametresi verildiyse, SAM köprüsü istemci soketine başka hiçbir mesaj göndermeyecektir. Geçerli soketten geçen tüm kalan veri, bağlı I2P hedefi eşine ileri ve geri iletilir.

SILENT=false parametresi geçirildiyse, ki bu varsayılan değerdir, SAM köprüsü isteyen eşin base64 genel hedef anahtarını içeren ASCII bir satır ve yalnızca SAM 3.2 için ek bilgileri istemciye gönderir:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Bu '\\n' ile sonlandırılan satırdan sonra, geçerli soketten geçen tüm kalan veriler, eşlerden biri soketi kapatana kadar bağlı I2P hedefi eşine ileri ve geri iletilir.

#### Tamam'dan Sonra Hatalar

Nadir durumlarda, SAM köprüsü RESULT=OK gönderdikten sonra ancak bir bağlantı gelmeden ve $destination satırını istemciye göndermeden önce bir hata ile karşılaşabilir. Bu hatalar, yönlendirici kapatma, yönlendirici yeniden başlatma ve oturum kapatmayı içerebilir. Bu tür durumlarda, SILENT=false olduğunda, SAM köprüsü şu satırı gönderebilir (ancak göndermesi gerekmez, uygulamaya bağlıdır):

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
yuvayı hemen kapatmadan önce. Bu satır, elbette, geçerli bir Base 64 hedefi olarak çözülemez.

### SAM Sanal Akışları: İLET

Bir istemci, normal bir soket sunucusu kullanabilir ve I2P'den gelen bağlantı isteklerini bekleyebilir. Bunun için istemcinin şunları yapması gerekir:

- SAM köprüsüyle yeni bir soket açın
- yukarıdakiyle aynı HELLO el sıkışmasını iletin
- ileri yönlendirme komutunu gönderin

#### İleri İstek

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Bu, oturumun ${nickname} I2P ağından gelen gelen bağlantı isteklerini dinlemesini sağlar. Oturumda devam eden bir ACCEPT olduğu sürece İLETMEYE izin verilmez.

#### İleri Yanıt

SILENT varsayılan olarak false değerindedir. SILENT true ya da false olsun, SAM köprüsü her zaman bir STREAM STATUS (AKIM DURUMU) mesajı ile yanıt verir. SILENT=true olduğunda STREAM ACCEPT ve STREAM CONNECT işlemlerinden farklı bir davranış sergilediğine dikkat edin. STREAM STATUS mesajı şöyledir:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
SONUÇ değeri şunlardan biri olabilir:

```
OK
I2P_ERROR
INVALID_ID
```
$host, SAM'in bağlantı isteklerini ileteceği soket sunucusunun ana bilgisayar adı veya IP adresidir. Belirtilmemişse, SAM ileri yönlendirme komutunu veren soketin IP'sini alır.

$port, SAM'ın bağlantı isteklerini ileteceği soket sunucusunun port numarasıdır. Zorunludur.

I2P'den bir bağlantı isteği geldiğinde, SAM köprüsü $host:$port adresine bir soket bağlantısı açar. Eğer bu bağlantı 3 saniye içinde kabul edilirse, SAM I2P'den gelen bağlantıyı kabul eder ve ardından:

SILENT=true parametresi verildiyse, elde edilen mevcut soketten geçen tüm veriler bağlı I2P hedefi eşine ileri ve geri iletilir.

SILENT=false değeri geçirildiyse, ki bu varsayılan değerdir, SAM köprüsü elde edilen sokete, istekte bulunan eşin base64 genel hedef anahtarını ve yalnızca SAM 3.2 için ek bilgileri içeren bir ASCII satırı gönderir:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
Bu '\\n' ile sonlandırılan satırdan sonra, soket üzerinden geçen tüm kalan veriler, taraflardan biri soketi kapatana kadar bağlı I2P hedefi eşine ileri ve geri iletilir.

SAM 3.2 itibarıyla, SSL=true belirtilmişse, yönlendirme soketi SSL/TLS üzerinden yapılır.

İleri yönlendirme soketi kapatıldığı anda I2P yönlendiricisi gelen bağlantı isteklerini dinlemeyi bırakır.

### SAM Datagramları

SAMv3, yerel datagram soketleri üzerinden datagram göndermek ve almak için mekanizmalar sunar. Bazı SAMv3 uygulamaları ayrıca SAM köprü soketi üzerinden datagram gönderme/alma konusunda eski v1/v2 yöntemini de destekler. İkisi de aşağıda belgelenmiştir.

I2P dört tür datagramı destekler:

- Yanıtlanabilir ve kimliği doğrulanmış datagramlar, gönderenin hedefiyle öneklenir ve gönderenin imzasını içerir, böylece alıcı, gönderenin hedefinin sahte olup olmadığını doğrulayabilir ve datagrama yanıt verebilir. Yeni Datagram2 biçimi de yanıtlanabilir ve kimliği doğrulanmış durumdadır.
- Yeni Datagram3 biçimi yanıtlanabilir ancak kimliği doğrulanmamıştır. Gönderen bilgisi doğrulanmamıştır.
- Ham datagramlar, gönderenin hedefini veya bir imzayı içermemektedir.

Yanıtlamalı ve ham datagramlar için varsayılan I2CP portları tanımlanmıştır. Ham datagramlar için I2CP portu değiştirilebilir.

Yaygın bir protokol tasarım desenidir ki, yanıt verilebilir veriagramlar bir kimlik bilgisi eklenerek sunuculara gönderilir ve sunucu bu kimlik bilgisini içeren ham bir veriagramla yanıt verir, böylece yanıt istekle eşleştirilebilir. Bu tasarım deseni, yanıtlarda yanıt verilebilir veriagramların önemli maliyetini ortadan kaldırır. I2CP protokolleri ve portları konusundaki tüm seçimler uygulamaya özeldir ve tasarımcıların bu konuları dikkate almaları gerekir.

Aşağıdaki bölümde datagram MTU ile ilgili önemli notlara da bakın.

#### Yanıtlananabilir veya Ham Datagramlar Göndermek

I2P'nin doğası gereği bir GÖNDEREN adresi bulunmasa da, kullanım kolaylığı için GÖNDEREN adresi içeren ek bir katman sağlanır - en fazla 31744 bayt boyutunda, sırasız ve güvensiz iletiler olan yanıtlanabilir veriagramlar (başlık bilgisi için en fazla 1KB yer ayırır). Bu GÖNDEREN adresi, SAM tarafından içsel olarak kimlik doğrulamasına tabi tutulur (kaynağın doğrulanması için hedefin imzalama anahtarından yararlanılır) ve yeniden oynatma önleme içerir.

Minimum boyut 1'dir. Teslimat güvenilirliğini en iyi hale getirmek için önerilen maksimum boyut yaklaşık 11 KB'dır. Güvenilirlik, mesaj boyutuyla ters orantılıdır ve hatta muhtemelen üstel olarak azalır.

STYLE=DATAGRAM veya STYLE=RAW ile bir SAM oturumu kurulduktan sonra, istemci SAM'ın UDP portu (varsayılan olarak 7655) üzerinden yanıt verilebilir veya ham datagramlar gönderebilir.

Bu port üzerinden gönderilen bir datagramın ilk satırı aşağıdaki biçimde olmalıdır. Bu tamamı bir satırda yer alır (boşlukla ayrılmıştır), açıklık açısından birden fazla satırda gösterilmiştir:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0, SAM'ın sürümüdür. SAM 3.2'den beri herhangi bir 3.x sürümü kabul edilir.
- $nickname, kullanılacak DATAGRAM oturumunun kimliğidir
- Hedef, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 formatında ifade edilmiş hâli olan $destination değeridir ve bu değer imza türüne bağlı olarak 516 ya da daha fazla base 64 karakteri (ikili sistemde 387 veya daha fazla bayt) kapsar. **NOT:** Yaklaşık 2014 yılından beri (SAM v3.1 itibarıyla), Java I2P $destination için hostname'leri ve b32 adresleri desteklemektedir ancak bu özellik önceki yıllarda belgelenmemişti. Hostname'ler ve b32 adresleri, Java I2P'nin 0.9.48 sürümünden itibaren resmi olarak desteklenmektedir. i2pd yönlendiricisi şu anda hostname'leri ve b32 adresleri desteklememektedir; bu destek gelecekteki bir sürüme eklenebilir.
- Tüm seçenekler, OTURUM OLUŞTUR (SESSION CREATE) aşamasında belirtilen varsayılanları geçersiz kılan, veri birimi başına ayarlardır.
- 3.3 sürümüne ait SEND_TAGS, TAG_THRESHOLD, EXPIRES ve SEND_LEASESET seçenekleri, destekleniyorsa [I2CP](/docs/protocol/i2cp)'ye iletilir. Ayrıntılar için [I2CP spesifikasyonuna](/docs/protocol/i2cp#msg_SendMessageExpire) bakınız. SAM sunucusu tarafından bu seçeneklerin desteklenmesi zorunlu değildir ve desteklenmiyorsa bu seçenekler göz ardı edilir.
- bu satır '\\n' ile sonlandırılır.

İlk satır, kalan mesaj verisi belirtilen hedefe gönderilmeden önce SAM tarafından yok sayılacaktır.

Yanıtlanabilir ve ham datagram göndermenin alternatif bir yöntemi için bkz. [DATAGRAM SEND ve RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### SAM Cevap Verilebilir Datagramlar: Bir Datagram Alma

DURUM OLUŞTUR komutunda bir iletim BAĞLANTI NOKTASI belirtilmemişse, alınan veri birimleri, veri birimi oturumunun açıldığı soketten SAM tarafından yazılır. Bu, veri birimlerini alma konusunda v1/v2 ile uyumlu yoldur.

Bir datagram geldiğinde, köprü onu mesaj aracılığıyla istemciye teslim eder:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
Kaynak, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 formatındaki hâlidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteridir (ikili sistemde 387 veya daha fazla bayt).

SAM köprüsü, istemciye kimlik doğrulama başlıkları veya diğer alanları asla göstermez, yalnızca gönderenin sağladığı verileri iletir. Bu işlem, oturum kapatılana kadar (istemcinin bağlantıyı kesmesiyle) devam eder.

#### Ham veya Yanıtlanabilir Datagramların İletilmesi

Bir datagram oturumu oluştururken, istemci gelen mesajların belirtilen bir ip:port adresine iletilmesini SAM'den isteyebilir. Bunu PORT ve HOST seçenekleriyle CREATE komutunu vererek yapar:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey, [Destination](/docs/specs/common-structures#type_Destination)'in ardından [Private Key](/docs/specs/common-structures#type_PrivateKey)'in ve ardından [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)'in birleştirilmesinin base 64 formatıdır. İsteğe bağlı olarak [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature) da eklenir. Bu, imza türüne bağlı olarak 884 veya daha fazla base 64 karakteridir (ikili formatta 663 veya daha fazla bayt). İkili format, Private Key File bölümünde belirtilmiştir.

HAM, DATAGRAM2 ve DATAGRAM3 veri birimleri için çevrimdışı imzalar desteklenir ancak DATAGRAM için desteklenmez. Ayrıntılar için yukarıdaki OTURUM OLUŞTURMA bölümüne ve aşağıda yer alan DATAGRAM2/3 bölümüne bakın.

$host, SAM'ın veriagramları ileteceği veriagram sunucusunun ana bilgisayar adı veya IP adresidir. Verilmezse, SAM iletim komutunu veren soketin IP'sini alır.

$port, SAM'ın veriagramları ileteceği veriagram sunucusunun bağlantı noktası numarasıdır. $port ayarlanmazsa veriagramlar İLETİLMEZ ve v1/v2 ile uyumlu şekilde kontrol soketine alınır.

Verilen ek seçenekler, SAM köprüsü tarafından yorumlanmazsa I2P oturum yapılandırmasına iletilir (örneğin outbound.length=0). Bu seçenekler [aşağıda belgelenmiştir](#tunnel-i2cp-and-streaming-options).

İletilen yanıtlanabilir datagramlar her zaman base64 hedefiyle öneklenir, aşağıya bakın, Datagram3 hariç. Yanıtlanabilir bir datagram ulaştığında, köprü belirtilen ana bilgisayara:bağlantı noktasına aşağıdaki verileri içeren bir UDP paketi gönderir:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
İletilen ham datagramlar, bir önek olmadan belirtilen ana makine:bağlantı noktasına olduğu gibi iletilir. UDP paketi aşağıdaki verileri içerir:

```
$datagram_payload
```
SAM 3.2 itibariyle, OTURUM OLUŞTUR'da HEADER=true belirtildiğinde, iletilen ham datagram aşağıdaki gibi bir başlık satırı ile başlayacaktır:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 gösterimidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteridir (ikili gösterimde 387 veya daha fazla bayt).

#### SAM Anonim (Ham) Datagramlar

İstemcilerin kimlik doğrulama ve yanıt bilgilerini kendilerinin ele almasına olanak tanıyan SAM, I2P'nin bant genişliğinden en iyi şekilde yararlanırken anonim veriagramlar göndermesine ve almasına izin verir. Bu veriagramlar güvenilmez ve sırasızdır ve en fazla 32768 bayt olabilir.

Minimum boyut 1'dir. Teslimat güvenilirliği için önerilen maksimum boyut yaklaşık 11 KB'dır.

STYLE=RAW ile bir SAM oturumu kurulduktan sonra, istemci, [yanıt verilebilir veriagramlar gönderildiği](#sending-repliable-or-raw-datagrams) şekilde SAM köprüsü üzerinden anonim veriagramlar gönderebilir.

Veriagramları alma yöntemlerinin her ikisi de anonim veriagramlar için de kullanılabilir.

DURUM OLUŞTUR komutunda bir iletim BAĞLANTI NOKTASI belirtilmemişse, alınan veri birimleri, veri birimi oturumunun açıldığı soketten SAM tarafından yazılır. Bu, veri birimlerini alma konusunda v1/v2 ile uyumlu yoldur.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Anonim datagramlar bir ana bilgisayara:bağlantı noktasına iletilmek istendiğinde, köprü belirtilen ana bilgisayara:bağlantı noktasına aşağıdaki verileri içeren bir ileti gönderir:

```
$datagram_payload
```
SAM 3.2 itibariyle, OTURUM OLUŞTUR'da HEADER=true belirtildiğinde, iletilen ham datagram aşağıdaki gibi bir başlık satırı ile başlayacaktır:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Anonim datagram göndermenin alternatif bir yöntemi için bkz. [HAM GÖNDER](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Veri Birimi 2/3

Datagram 2/3, 2025 yılının başlarında belirlenen yeni biçimlerdir. Şu anda bilinen hiçbir uygulama mevcut değildir. Güncel durum için uygulama belgelerine bakın. Daha fazla bilgi için [belirtim'e](/docs/specs/datagrams) bakın.

Datagram 2/3 desteğini belirtmek için SAM sürümünü yükseltmeye yönelik şu anlık hiçbir plan yoktur. Bu, uygulamaların Datagram 2/3'ü desteklemek istemesi ama SAM v3.3 özelliklerini desteklememesi durumunda sorun yaratabilir. Herhangi bir sürüm değişikliği henüz belirlenmedi (TBD).

Datagram2 ve Datagram3'ün ikisi de yanıt verilebilir. Yalnızca Datagram2 kimliği doğrulanmış.

Datagram2, SAM açısından yanıt verilebilir datagramlarla aynıdır. İkisi de kimlik doğrulaması yapılır. Yalnızca I2CP biçimi ve imza farklıdır, ancak bu SAM istemcileri için görünmezdir. Datagram2 ayrıca çevrimdışı imzaları destekler, bu yüzden çevrimdışı imzalı hedefler tarafından kullanılabilir.

Yeni uygulamalar için geriye dönük uyumluluk gerektirmeyen Repliable veriagramlarının yerini Datagram2'nin alması amaçlanmıştır. Datagram2, Repliable veriagramlarda bulunmayan yeniden oynatma koruması sağlar. Geriye dönük uyumluluk gerekiyorsa, bir uygulama hem Datagram2 hem de Repliable'ı destekleyebilir ve bu, SAM 3.3 PRIMARY oturumlarında aynı oturumda desteklenebilir.

Datagram3, yanıt verilebilir ancak kimliği doğrulanmaz. I2CP biçimindeki 'from' alanı bir hedef değil, bir özet değeridir. SAM sunucusundan istemciye gönderilen $destination değeri 44 baytlık bir base64 özetidir. Yanıt için tam hedefe dönüştürmek üzere, bunu 32 baytlık ikili biçime base64'ten çözüp ardından 52 karaktere base32 ile kodlayın ve NAMING LOOKUP (isim arama) için ".b32.i2p" ekleyin. Her zamanki gibi, istemciler tekrarlanan NAMING LOOKUP işlemlerinden kaçınmak için kendi önbelleklerini korumalıdır.

Uygulama tasarımcıları, kimliği doğrulanmamış datagramların güvenlik etkilerini düşünerek son derece dikkatli olmalıdır.

#### V3 Datagram MTU Hususları

I2P Datagramları, tipik internet MTU'su olan 1500'den daha büyük olabilir. 516+ baytlık base64 hedefle öneklenmiş yerel olarak gönderilen datagramlar ve iletilen yanıtlanabilir datagramlar bu MTU'yu aşma eğilimindedir. Ancak Linux sistemlerinde localhost MTU'ları tipik olarak çok daha büyüktür, örneğin 65536. Localhost MTU'ları işletim sistemine göre değişir. I2P Datagramları asla 65536'dan büyük olmaz. Datagram boyutu uygulama protokolüne bağlıdır.

Eğer SAM istemcisi SAM sunucusuna yerel ise ve sistem daha büyük bir MTU'yu destekliyorsa, veriagramlar yerel olarak parçalanmaz. Ancak, SAM istemcisi uzakta ise, IPv4 veriagramları parçalanır ve IPv6 veriagramları başarısız olur (IPv6 UDP parçalamayı desteklemez).

İstemci kütüphanesi ve uygulama geliştiricileri, özellikle uzak SAM istemci-sunucu bağlantılarında parçalanmayı önlemek ve paket kaybını engellemek için bu konuların farkında olmalı ve önerileri belgelemelidir.

#### DATAGRAM GÖNDER, HAM GÖNDER (V1/V2 Uyumlu Datagram İşleme)

SAM V3'te, veriagram göndermenin tercih edilen yolu yukarıda belgelendiği gibi 7655 numaralı bağlantı noktasındaki veriagram soketini kullanmaktır. Ancak, cevap verilebilir veriagramlar, [SAM V1](/docs/api/sam) ve [SAM V2](/docs/api/samv2) belgelerinde açıklandığı gibi, SAM köprü soketi üzerinden doğrudan DATAGRAM SEND komutu kullanılarak gönderilebilir.

0.9.14 sürümü itibarıyla (sürüm 3.1), [SAM V1](/docs/api/sam) ve [SAM V2](/docs/api/samv2) belgelerinde belirtildiği gibi, anonim datagramlar RAW SEND komutunu kullanarak SAM köprü soketi üzerinden doğrudan gönderilebilir.

0.9.24 sürümünden itibaren (sürüm 3.2), DATAGRAM SEND ve RAW SEND, varsayılan portları geçersiz kılmak için FROM_PORT=nnnn ve/veya TO_PORT=nnnn parametrelerini içerebilir. 0.9.24 sürümünden itibaren (sürüm 3.2), RAW SEND, varsayılan protokolü geçersiz kılmak için PROTOCOL=nnn parametresini içerebilir.

Bu komutlar ID parametresini *desteklemez*. Datagramlar, uygun şekilde en son oluşturulan DATAGRAM veya RAW tarzı oturuma gönderilir. ID parametresi desteği gelecekteki bir sürümde eklenebilir.

DATAGRAM2 ve DATAGRAM3 biçimleri V1/V2 uyumlu şekilde *desteklenmez*.

### SAM BİRİNCİL Oturumlar (V3.3 ve üzeri)

*Sürüm 3.3, I2P 0.9.25 sürümünde tanıtıldı.*

*Bu belgenin daha önceki bir sürümünde, PRIMARY oturumlar MASTER oturumlar olarak bilinirdi. Hem `i2pd` hem de `I2P+` projelerinde hâlâ yalnızca MASTER oturumlar olarak bilinirler.*

SAM v3.3, aynı birincil oturumda akış, datagram ve ham alt oturumların çalıştırılmasını ve aynı türden birden fazla alt oturumun çalıştırılmasını destekler. Tüm alt oturum trafiği tek bir hedefi veya tünel kümesini kullanır. I2P'den gelen trafiğin yönlendirilmesi, alt oturumlar için port ve protokol seçeneklerine dayanır.

Çoklama alt oturumlar oluşturmak için öncelikle bir birincil oturum oluşturmalı ve ardından bu birincil oturuma alt oturumlar eklemelisiniz. Her alt oturumun benzersiz bir kimliği ve benzersiz bir dinleme protokolü ile bağlantı noktası olmalıdır. Alt oturumlar birincil oturumdan ayrıca kaldırılabilir.

Birincil bir oturum ve alt oturumların birleşimini kullanarak, SAM istemcisi tek bir tünel kümesi üzerinde birden fazla uygulamayı veya çeşitli protokoller kullanan tek bir gelişmiş uygulamayı destekleyebilir. Örneğin, bir bittorrent istemcisi, DHT iletişim için veriagram ve ham alt oturumlarla birlikte, eşten eşe bağlantılar için akış alt oturumu ayarlayabilir.

#### BİRİNCİL Oturum Oluşturma

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM köprüsü, [standart OTURUM OLUŞTURMA yanıtındaki gibi](#session-creation-response) başarı veya başarısızlık ile yanıt verecektir.

Birincil oturumda PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL veya HEADER seçeneklerini ayarlamayın. BİRİNCİL oturum kimliği veya kontrol soketi üzerinden herhangi bir veri gönderemezsiniz. STREAM CONNECT, DATAGRAM SEND vb. tüm komutlar ayrı bir sokette alt oturum kimliğini kullanmalıdır.

BİRİNCİL oturum yönlendiriciye bağlanır ve tünel oluşturur. SAM köprüsü yanıt verdiğinde, tünel oluşturma işlemi tamamlanmış olur ve oturum alt oturumların eklenmesi için hazır hâle gelir. Uzunluk, miktar ve takma ad gibi tünel parametreleriyle ilgili tüm [I2CP](/docs/protocol/i2cp) seçenekleri, birincil oturumun OTURUM OLUŞTUR (SESSION CREATE) komutunda sağlanmalıdır.

Tüm yardımcı komutlar birincil oturumda desteklenir.

Birincil oturum kapatıldığında, tüm alt oturumlar da kapatılır.

NOT: 0.9.47 sürümünden önce STYLE=MASTER kullanın. STYLE=PRIMARY, 0.9.47 sürümünden itibaren desteklenmektedir. Geriye dönük uyumluluk için MASTER hâlâ desteklenmektedir.

#### Alt Oturum Oluşturma

BİRİNCİL oturumun oluşturulduğu aynı kontrol soketini kullanarak:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
SAM köprüsü, [standart OTURUM OLUŞTURMA yanıtı](#session-creation-response) gibi başarı veya başarısızlık ile yanıt verecektir. Tüneller zaten birincil OTURUM OLUŞTURMA sırasında oluşturulduğundan, SAM köprüsü hemen yanıt vermelidir.

SESSION ADD işlemi sırasında DESTINATION seçeneğini ayarlamayın. Alt oturum, birincil oturumda belirtilen hedefi kullanacaktır. Tüm alt oturumlar kontrol soketine eklenmelidir, yani birincil oturumu oluşturduğunuz aynı bağlantıya.

Gelen verilerin doğru şekilde yönlendirilebilmesi için birden fazla alt oturumun seçenekleri yeterince benzersiz olmalıdır. Özellikle, aynı stildeki birden fazla oturumun farklı LISTEN_PORT seçenekleri olmalıdır (ve yalnızca RAW için LISTEN_PROTOCOL). Var olan bir alt oturumla aynı dinleme bağlantı noktasına ve protokole sahip bir SESSION ADD işlemi bir hata ile sonuçlanacaktır.

LISTEN_PORT, yani gelen veri için alınan (TO) bağlantı noktası, yerel I2P bağlantı noktasıdır. LISTEN_PORT belirtilmemişse, FROM_PORT değeri kullanılacaktır. LISTEN_PORT ve FROM_PORT belirtilmemişse, gelen yönlendirme yalnızca STYLE ve PROTOCOL'a göre yapılacaktır. LISTEN_PORT ve LISTEN_PROTOCOL için 0, yani herhangi bir değer anlamına gelir, joker karakterdir. Hem LISTEN_PORT hem de LISTEN_PROTOCOL 0 ise, bu alt oturum, başka bir alt oturuma yönlendirilmeyen gelen trafiğin varsayılanı olacaktır. Gelen akış trafiği (protokol 6), LISTEN_PROTOCOL'ü 0 olsa bile, asla RAW alt oturumuna yönlendirilmeyecektir. Bir RAW alt oturumu, LISTEN_PROTOCOL'ü 6 olarak ayarlayamaz. Gelen trafiğin protokolüne ve bağlantı noktasına eşleşen bir varsayılan veya alt oturum yoksa, bu veri atılacaktır.

Veri göndermek ve almak için birincil oturum kimliği yerine alt oturum kimliğini kullanın. AKIŞ BAĞLANTISI, DATAGRAM GÖNDER, vb. gibi tüm komutlar alt oturum kimliğini kullanmalıdır.

Tüm yardımcı komutlar bir birincil oturumda veya alt oturumda desteklenir. v1/v2 datagram/ham veri gönderimi/alımı bir birincil oturumda veya alt oturumlarda desteklenmez.

#### Bir Alt Oturumu Durdurma

BİRİNCİL oturumun oluşturulduğu aynı kontrol soketini kullanarak:

```
->  SESSION REMOVE
          ID=$nickname
```
Bu, bir alt oturumu birincil oturumdan kaldırır. OTURUM KALDIR (SESSION REMOVE) işlemi üzerinde başka hiçbir seçeneği ayarlamayın. Alt oturumlar, yani birincil oturumu oluşturduğunuz bağlantı üzerindeki kontrol soketi üzerinden kaldırılmalıdır. Bir alt oturum kaldırıldıktan sonra kapatılır ve veri göndermek veya almak için kullanılamaz hale gelir.

SAM köprüsü, [standart OTURUM OLUŞTURMA yanıtındaki gibi](#session-creation-response) başarı veya başarısızlık ile yanıt verecektir.

### SAM Yardımcı Komutları

Bazı yardımcı komutlar önceden var olan bir oturum gerektirir, bazıları ise gerektirmez. Ayrıntılar için aşağıya bakın.

#### Ana Bilgisayar Adı Araması

İstemci, isim çözümlemesi için SAM köprüsüne sorgu yapmak üzere aşağıdaki iletiyi kullanabilir:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
tarafından yanıtlanan

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
SONUÇ değeri şunlardan biri olabilir:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Eğer NAME=ME ise, yanıt geçerli oturum tarafından kullanılan hedefi içerecektir (GEÇİCİ bir tane kullanıyorsanız faydalıdır). Eğer $result OK değilse, MESSAGE, "hatalı biçim" gibi açıklayıcı bir mesaj içerebilir. INVALID_KEY, istekteki $name ile ilgili bir sorun olduğunu, muhtemelen geçersiz karakterler olduğunu ima eder.

$destination, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 gösterimidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteridir (ikili gösterimde 387 veya daha fazla bayt).

NAMING LOOKUP, önce bir oturum oluşturulmasını gerektirmez. Ancak bazı uygulamalarda, önbelleğe alınmamış ve ağ sorgusu gerektiren bir .b32.i2p araması, arama için kullanılabilir istemci tüneli bulunmadığından başarısız olabilir.

#### Ad Arama Seçenekleri

NAMING LOOKUP, servis aramalarını desteklemek için 0.9.66 sürümüyle birlikte genişletilmiştir. Destek, uygulamaya göre değişiklik gösterebilir. Ek bilgi için öneri 167'ye bakın.

NAMING LOOKUP NAME=example.i2p OPTIONS=true, yanıtta seçenekler eşlemesini talep eder. NAME, OPTIONS=true olduğunda tam bir base64 hedefi olabilir.

Hedef arama başarılı olur ve leaseSet'te seçenekler mevcutsa, yanıtta hedefin ardından OPTION:anahtar=değer biçiminde bir veya daha fazla seçenek bulunur. Her seçenek ayrı bir OPTION: ön ekine sahip olur. LeaseSet'teki tüm seçenekler, yalnızca hizmet kaydı seçenekleri değil, dahil edilir. Örneğin, gelecekte tanımlanmış parametreler için seçenekler mevcut olabilir. Örnek:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

'=' içeren anahtarlar ve satır sonu içeren anahtarlar veya değerler geçersiz kabul edilir ve anahtar/değer çifti yanıttan kaldırılır. Kiralama setinde (leaseset) hiçbir seçenek bulunamazsa veya kiralama seti sürüm 1 ise, yanıt hiçbir seçenek içermeyecektir. ARAMA=içinde OPTIONS=true varsa ve kiralama seti bulunamazsa, yeni bir sonuç değeri LEASESET_NOT_FOUND döndürülecektir.

#### Hedef Anahtar Oluşturma

Genel ve özel base64 anahtarları aşağıdaki mesaj kullanılarak oluşturulabilir:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
tarafından yanıtlanan

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
3.1 sürümünden itibaren (I2P 0.9.14), isteğe bağlı bir SIGNATURE_TYPE parametresi desteklenmektedir. SIGNATURE_TYPE değeri, [Anahtar Sertifikaları](/docs/specs/common-structures#type_Certificate) tarafından desteklenen herhangi bir isim (örneğin ECDSA_SHA256_P256, büyük-küçük harf duyarsız) veya sayı (örneğin 1) olabilir. Varsayılan değer DSA_SHA1'dir ve bu istenilen şey DEĞİLDİR. Çoğu uygulama için lütfen SIGNATURE_TYPE=7 olarak belirtin.

$destination, [Destination](/docs/specs/common-structures#type_Destination) yapısının base 64 gösterimidir ve imza türüne bağlı olarak 516 veya daha fazla base 64 karakteridir (ikili gösterimde 387 veya daha fazla bayt).

$privkey, [Destination](/docs/specs/common-structures#type_Destination) ile başlayan, ardından [Private Key](/docs/specs/common-structures#type_PrivateKey) ve sonra [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey)'in gelmesiyle elde edilen birleşimin base 64 formatıdır. Bu, imza türüne bağlı olarak 884 veya daha fazla base 64 karakteridir (ikili biçimde 663 veya daha fazla bayt). İkili biçim, Private Key File içinde belirtilmiştir.

256 baytlık ikili [Özel Anahtar](/docs/specs/common-structures#type_PrivateKey) hakkında notlar: Bu alan, 0.6 (2005) sürümünden beri kullanılmamaktadır. SAM uygulamaları bu alana rastgele veri veya tümü sıfır olan veri gönderebilir; base64 içindeki AAAA dizgisi nedeniyle endişelenmeyin. Çoğu uygulama base64 dizgisini basitçe saklayacak ve SESSION CREATE sırasında olduğu gibi geri döndürecektir veya ikili biçimde depolamak için çözecek, ardından SESSION CREATE için tekrar kodlayacaktır. Ancak uygulamalar base64'ü çözüp PrivateKeyFile spesifikasyonuna göre ikili veriyi ayrıştırabilir, 256 baytlık özel anahtar bölümünü atabilir ve SESSION CREATE için yeniden kodlarken yerine 256 bayt rastgele veri veya tümü sıfır olan veri koyabilir. PrivateKeyFile spesifikasyonundaki DİĞER tüm alanlar korunmalıdır. Bu işlem dosya sistemi depolamada 256 bayt tasarrufu sağlar ancak çoğu uygulama için zahmete değmeyebilir. Ek bilgi ve arka plan için 161 numaralı öneriye bakınız.

DEST GENERATE, önce bir oturum oluşturulmasını gerektirmez.

DEST GENERATE, çevrimdışı imzalarla bir hedef oluşturmak için kullanılamaz.

#### PING/PONG (SAM 3.2 veya üzeri)

İstemci veya sunucu şunu gönderebilir:

```
PING[ arbitrary text]
```
kontrol portunda, yanıt olarak:

```
PONG[ arbitrary text from the ping]
```
kontrol soketi canlı tutmak için kullanılacaktır. Makul bir süre içinde yanıt alınamazsa, her iki taraf da oturumu ve soketi kapatabilir, uygulamaya bağlıdır.

İstemciden bir PONG mesajı beklerken zaman aşımı oluşursa, köprü şu mesajı gönderebilir:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
ve ardından bağlantıyı kesin.

Köprüden bir PONG beklerken zaman aşımı oluşursa, istemci basitçe bağlantıyı keser.

PING/PONG, önce bir oturum oluşturulmasını gerektirmez.

#### ÇIK/ DUR/ AYRIL (SAM 3.2 veya üzeri, isteğe bağlı özellikler)

KOMUTLAR QUIT, STOP ve EXIT oturumu ve soketi kapatır. Uygulama, telnet üzerinden test etmeyi kolaylaştırmak için isteğe bağlıdır. Soket kapatılmadan önce herhangi bir yanıt olup olmayacağı (örneğin, bir OTURUM DURUMU mesajı) uygulamaya özeldir ve bu belgenin kapsamı dışındadır.

OTURUM AÇMA/DURDUR/ÇIKIŞ yapmak için önce bir oturum oluşturulması gerekmez.

#### YARDIM (isteğe bağlı özellik)

Sunucular HELP komutunu uygulayabilir. Telnet üzerinden test etmeyi kolaylaştırmak için bu uygulama isteğe bağlıdır. Çıktı biçimi ve çıktının sonunun tespiti uygulamaya özeldir ve bu spesifikasyonun kapsamı dışındadır.

HELP, önce bir oturum oluşturulmasını gerektirmez.

#### Yetkilendirme Yapılandırması (SAM 3.2 veya üzeri, isteğe bağlı özellik)

AUTH komutunu kullanarak yetkilendirme yapılandırması. SAM sunucusu, kimlik bilgilerinin kalıcı olarak depolanmasını kolaylaştırmak için bu komutları uygulayabilir. Bu komutlar dışında kimlik doğrulama yapılandırması, uygulamaya özgüdür ve bu belgenin kapsamı dışındadır.

- AUTH ENABLE, sonraki bağlantılar üzerinde yetkilendirmeyi etkinleştirir
- AUTH DISABLE, sonraki bağlantılar üzerinde yetkilendirmeyi devre dışı bırakır
- AUTH ADD USER="foo" PASSWORD="bar", bir kullanıcı/şifre ekler
- AUTH REMOVE USER="foo", bu kullanıcıyı kaldırır

Kullanıcı adı ve parola için çift tırnak kullanımı önerilir ancak zorunlu değildir. Kullanıcı adı veya paroladaki bir çift tırnak, ters eğik çizgi ile kaçışmalıdır. Başarısızlık durumunda sunucu bir I2P_ERROR ve bir mesaj ile yanıt verir.

OTURUM, önce bir oturum oluşturulmasını gerektirmez.

### SONUÇ Değerleri

Bu, RESULT alanının taşıyabileceği değerler ve anlamlarıdır:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Farklı uygulamalar, çeşitli senaryolarda hangi SONUÇ'un döndürüleceği konusunda tutarlı olmayabilir.

OK dışında bir SONUÇ ile gelen çoğu yanıt, ek bilgi içeren bir MESAJ da içerir. MESAJ genellikle sorun giderme konusunda yardımcı olur. Ancak MESAJ dizeleri uygulamaya bağlıdır, SAM sunucusu tarafından geçerli yerel ayara çevrilmiş olabilir ya da olmayabilir, istisnalar gibi iç uygulamaya özgü bilgiler içerebilir ve bildirim yapılmadan değiştirilebilir. SAM istemcileri MESAJ dizelerini kullanıcılara göstermeyi seçebilir, ancak bunlara dayanarak programatik kararlar vermemelidir çünkü bu kırılgan olur.

### Tünel, I2CP ve Akış Seçenekleri

Bu seçenekler SAM OTURUMU OLUŞTUR satırında ad=değer çiftleri olarak iletilebilir.

Tüm oturumlar, tünel uzunlukları ve miktarları gibi [I2CP seçeneklerini](/docs/protocol/i2cp#options) içerebilir. STREAM oturumları, [Akış kütüphanesi seçeneklerini](/docs/api/streaming#options) içerebilir.

Seçenek adları ve varsayılan değerler için bu referanslara bakın. Atıfta bulunulan belgeler Java yönlendirici uygulaması içindir. Varsayılanlar değiştirilebilir. Seçenek adları ve değerleri büyük/küçük harfe duyarlıdır. Diğer yönlendirici uygulamaları tüm seçenekleri desteklemeyebilir ve farklı varsayılanlara sahip olabilir; ayrıntılar için yönlendirici belgelerine başvurun.

### BASE 64 Notları

Base 64 kodlaması, I2P standart Base 64 alfabesi olan "A-Z, a-z, 0-9, -, ~" karakterlerini kullanmalıdır.

### Varsayılan SAM Kurulumu

Varsayılan SAM portu 7656'dır. SAM, Java I2P Yönlendiricisi'nde varsayılan olarak etkin değildir; yönlendirici konsolundaki istemcileri yapılandırma sayfasında veya clients.config dosyasında manuel olarak başlatılmalı veya otomatik başlatılacak şekilde yapılandırılmalıdır. Varsayılan SAM UDP portu 7655'tir ve 127.0.0.1 üzerinde dinler. Bu ayarlar, Java yönlendiricisinde, başlatmaya sam.udp.port=nnnnn ve/veya sam.udp.host=w.x.y.z argümanlarını ekleyerek veya OTURUM (SESSION) satırında değiştirilebilir.

Diğer yönlendiricilerdeki yapılandırma uygulamaya özeldir. [Buradaki i2pd yapılandırma kılavuzuna](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/) bakın.
