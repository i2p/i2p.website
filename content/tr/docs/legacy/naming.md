---
title: "Adlandırma Tartışması"
description: "I2P'nin adlandırma modeli ve küresel DNS benzeri şemaların neden reddedildiğine ilişkin tarihsel tartışma"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Bağlam:** Bu sayfa, I2P’nin erken tasarım döneminden uzun süreli tartışmaları arşivler. Projenin, DNS tarzı sorgulara ya da çoğunluk oylamasına dayalı kayıt sistemlerine kıyasla yerel olarak güvenilen adres defterlerini neden tercih ettiğini açıklar. Güncel kullanım rehberi için [Adlandırma belgeleri](/docs/overview/naming/) bölümüne bakın.

## Elenen Alternatifler

I2P'nin güvenlik hedefleri, alışılagelmiş adlandırma şemalarını dışlar:

- **DNS tarzı ad çözümleme.** Arama yolundaki herhangi bir çözücü yanıtları sahteleyebilir veya sansürleyebilir. DNSSEC olsa bile, ele geçirilmiş registrars (kayıt operatörleri) veya sertifika otoriteleri hâlâ tek hata noktasıdır. I2P'de hedefler açık anahtarlardır—bir sorguyu ele geçirmek bir kimliği tamamen tehlikeye atar.
- **Oylamaya dayalı adlandırma.** Bir saldırgan sınırsız sayıda kimlik üretebilir (Sybil saldırısı) ve popüler adlar için oyları “kazanabilir”. İş ispatı önlemleri maliyeti artırır ama ağır bir koordinasyon yükü getirir.

Bunun yerine, I2P adlandırmayı bilinçli olarak taşıma katmanının üzerinde tutar. Birlikte gelen adlandırma kitaplığı, alternatif şemelerin bir arada var olabilmesini sağlayan bir hizmet sağlayıcı arayüzü sunar—kullanıcılar hangi adres defterlerine veya jump services (adres atlama hizmetleri) güveneceklerine kendileri karar verir.

## Yerel ve Küresel Adlar (jrandom, 2005)

- I2P içindeki adlar yerel olarak benzersizdir, ancak insan tarafından okunabilirdir. Sizin `boss.i2p` adınız başkasının `boss.i2p` adıyla eşleşmeyebilir; bu, tasarım gereğidir.
- Kötü niyetli bir aktör sizi bir adın işaret ettiği destination'ı (hizmetin kriptografik adresi) değiştirmeniz için kandırırsa, bir hizmeti fiilen ele geçirmiş olur. Adların küresel olarak benzersiz olmasını reddetmek bu tür bir saldırıyı önler.
- Adları yer imleri veya anlık mesajlaşma takma adları gibi düşünün—belirli adres defterlerine abone olarak ya da anahtarları elle ekleyerek hangi destination'lara güveneceğinizi siz seçersiniz.

## Yaygın İtirazlar ve Yanıtlar (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Verimlilik Fikirleri Tartışıldı

- Artımlı güncellemeler sunun (yalnızca son alımdan beri eklenen destinations (I2P hedef adresleri)).
- Tam hosts dosyalarının yanında (`recenthosts.cgi`) tamamlayıcı akışlar sunun.
- Akışları birleştirmek veya güven düzeylerine göre filtrelemek için (örneğin, `i2host.i2p`) betiklenebilir araçları keşfedin.

## Önemli Noktalar

- Güvenlik, küresel uzlaşıdan daha önemlidir: yerel olarak bakımı yapılan adres defterleri ele geçirilme riskini en aza indirir.
- Birden çok adlandırma yaklaşımı adlandırma API’si aracılığıyla birlikte var olabilir—kullanıcılar neye güveneceklerine kendileri karar verir.
- Tamamen merkeziyetsiz küresel adlandırma hâlâ açık bir araştırma sorunudur; güvenlik, insanlar tarafından hatırlanabilirlik ve küresel benzersizlik arasındaki ödünleşimler hâlâ [Zooko’nun üçgenini](https://zooko.com/distnames.html) yansıtır.

## Referanslar

- [Adlandırma belgeleri](/docs/overview/naming/)
- [Zooko’nun “İsimler: Merkeziyetsiz, Güvenli, İnsan için anlamlı: İkisini Seçin”](https://zooko.com/distnames.html)
- Örnek artımlı besleme: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
