---
title: "Alternatif I2P İstemcileri"
description: "Topluluk tarafından sürdürülen I2P istemci uygulamaları (2025 için güncellenmiş)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Ana I2P istemci uygulaması **Java** kullanır. Belirli bir sistemde Java kullanamıyor veya kullanmayı tercih etmiyorsanız, topluluk üyeleri tarafından geliştirilen ve sürdürülen alternatif I2P istemci uygulamaları mevcuttur. Bu programlar, farklı programlama dilleri veya yaklaşımlar kullanarak aynı temel işlevselliği sağlar.

---

## Karşılaştırma Tablosu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**Web Sitesi:** [https://i2pd.website](https://i2pd.website)

**Açıklama:** i2pd (*I2P Daemon*) C++ ile geliştirilmiş tam özellikli bir I2P istemcisidir. Uzun yıllardır (yaklaşık 2016'dan beri) üretim ortamında kullanım için kararlı durumdadır ve topluluk tarafından aktif olarak sürdürülmektedir. i2pd, I2P ağ protokollerini ve API'lerini tam olarak uygular, bu da Java I2P ağıyla tamamen uyumlu olmasını sağlar. Bu C++ router genellikle Java çalışma ortamının bulunmadığı veya istenmediği sistemlerde hafif bir alternatif olarak kullanılır. i2pd, yapılandırma ve izleme için yerleşik web tabanlı bir konsol içerir. Platformlar arası çalışır ve birçok paketleme formatında mevcuttur — hatta Android için bile bir i2pd sürümü bulunmaktadır (örneğin, F-Droid üzerinden).

---

## Go-I2P (Go)

**Depo:** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**Açıklama:** Go-I2P, Go programlama dilinde yazılmış bir I2P istemcisidir. I2P router'ının bağımsız bir uygulamasıdır ve Go'nun verimliliği ve taşınabilirliğinden yararlanmayı amaçlar. Proje aktif geliştirme aşamasındadır, ancak hala erken aşamadadır ve henüz tüm özellikleri tamamlanmamıştır. 2025 itibariyle, Go-I2P deneysel olarak kabul edilmektedir — topluluk geliştiricileri tarafından aktif olarak üzerinde çalışılmaktadır, ancak daha fazla olgunlaşana kadar üretim ortamında kullanılması önerilmez. Go-I2P'nin amacı, geliştirme tamamlandığında I2P ağı ile tam uyumlu, modern ve hafif bir I2P router sağlamaktır.

---

## I2P+ (Java çatalı)

**Web sitesi:** [https://i2pplus.github.io](https://i2pplus.github.io)

**Açıklama:** I2P+, standart Java I2P istemcisinin topluluk tarafından sürdürülen bir çatallamasıdır (fork). Yeni bir dilde yeniden uygulama değil, ek özellikler ve optimizasyonlarla geliştirilmiş Java router'ının bir sürümüdür. I2P+, resmi I2P ağıyla tamamen uyumlu kalırken geliştirilmiş kullanıcı deneyimi ve daha iyi performans sunmaya odaklanır. Yenilenmiş bir web konsolu arayüzü, daha kullanıcı dostu yapılandırma seçenekleri ve çeşitli optimizasyonlar (örneğin, geliştirilmiş torrent performansı ve özellikle güvenlik duvarı arkasındaki router'lar için daha iyi ağ eşleri yönetimi) sunar. I2P+, resmi I2P yazılımı gibi bir Java ortamı gerektirir, dolayısıyla Java olmayan ortamlar için bir çözüm değildir. Ancak, Java'ya sahip olan ve ekstra yeteneklere sahip alternatif bir yapı isteyen kullanıcılar için I2P+ cazip bir seçenek sunar. Bu çatallama, upstream I2P sürümleriyle güncel tutulmaktadır (sürüm numaralandırmasına "+" ekleyerek) ve projenin web sitesinden edinilebilir.
