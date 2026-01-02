---
title: "NTCP Tartışması"
description: "NTCP ve SSU taşıma protokollerini karşılaştıran tarihsel notlar ve önerilen ince ayar fikirleri"
slug: "ntcp"
layout: "single"
reviewStatus: "needs-review"
---

## NTCP ve SSU Tartışması (Mart 2007)

### NTCP Soruları

_zzz ve cervantes arasında geçen bir IRC konuşmasından uyarlanmıştır._

- **NTCP, ek yük ve gecikme ekliyormuş gibi görünürken neden SSU'ya göre önceliklidir?**  
  NTCP genellikle özgün SSU uygulamasına göre daha iyi güvenilirlik sağlar.
- **NTCP üzerinden akış iletimi klasik TCP-over-TCP collapse'a (TCP üzerinde TCP katmanlamasının neden olduğu performans çökmesi) takılır mı?**  
  Muhtemelen, ancak SSU hafif UDP seçeneği olarak tasarlanmıştı ve pratikte yeterince güvenilir olmadığı ortaya çıktı.

### “NTCP Zararlı Kabul Edilir” (zzz, 25 Mart 2007)

Özet: NTCP'nin daha yüksek gecikmesi ve ek yükü ağ tıkanıklığına neden olabilir; yine de yönlendirme, teklif puanları SSU'dan daha düşük olacak şekilde sabit kodlandığı için NTCP'yi tercih ediyor. Analiz birkaç noktayı gündeme getirdi:


#### 2007 başlığındaki öneriler

1. **Taşıma önceliklerini tersine çevirin**; böylece router'lar SSU'yu tercih eder (`i2np.udp.alwaysPreferred` ayarını eski hâline getirerek).
2. **Streaming (akış) trafiğini etiketleyin**; böylece SSU, anonimliği zedelemeden yalnızca etiketlenmiş iletiler için daha düşük teklifte bulunsun.
3. **SSU yeniden iletim sınırlarını sıkılaştırın**; çökme riskini azaltmak için.
4. **Yarı güvenilir underlays (alt katmanlar) inceleyin**; streaming library (akış kitaplığı) altında yapılan yeniden iletimlerin net bir fayda olup olmadığını belirlemek için.
5. **Öncelik kuyruklarını ve zaman aşımlarını gözden geçirin**—örneğin, NTCP ile uyumlu hâle getirmek için streaming zaman aşımlarını 45 s'i aşacak şekilde artırmak.

### jrandom'un yanıtı (27 Mart 2007)

Başlıca karşı argümanlar:

- NTCP'nin var olma nedeni, erken SSU dağıtımlarının congestion collapse (ağ tıkanıklığı kaynaklı çöküş) yaşamasıdır. Her atlama başına mütevazı yeniden iletim oranları bile çok atlamalı tunnel'lar boyunca katlanarak artabilir.
- tunnel düzeyi onaylar olmadan, iletilerin yalnızca bir kısmı uçtan uca teslim durumu alır; başarısızlıklar fark edilmeyebilir.
- TCP tıkanıklık denetimi onlarca yıllık iyileştirmelere sahiptir; NTCP bunlardan olgun TCP yığınları aracılığıyla yararlanır.
- SSU'yu tercih ederken gözlemlenen verimlilik artışları, protokole özgü içsel avantajlardan ziyade router kuyruklama davranışını yansıtıyor olabilir.
- Daha büyük streaming zaman aşımı değerleri halihazırda kararlılığı iyileştiriyordu; büyük değişikliklere geçmeden önce daha fazla gözlem ve veri teşvik edildi.

Tartışma, sonraki taşıma ince ayarlarının geliştirilmesine yardımcı oldu, ancak modern NTCP2/SSU2 mimarisini yansıtmıyor.
