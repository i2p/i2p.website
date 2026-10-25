---
title: "Tek Yönlü Tunnel'lar"
description: "I2P'nin tek yönlü tunnel tasarımının tarihsel özeti"
slug: "unidirectional"
aliases:
  - "/tr/unidirectional-tunnels"
  - "/tr/unidirectional-tunnels/"
lastUpdated: "2016-11"
accurateFor: "0.9.27"
---

## Genel Bakış

Bu sayfa I2P'nin tek yönlü tunnel'larının kökenlerini ve tasarımını açıklar. Daha fazla bilgi için bakınız:

- [Tunnel genel bakış sayfası](/docs/overview/tunnel-routing)
- [Tunnel spesifikasyonu](/docs/specs/tunnel-implementation)
- [Tunnel oluşturma spesifikasyonu](/docs/specs/tunnel-creation)
- [Tunnel tasarım tartışması](/docs/discussions/tunnel)
- [Eş seçimi](/docs/overview/peer-selection)

## İnceleme

Tek yönlü tunnel'ların avantajları konusunda yayınlanmış herhangi bir araştırmadan haberdar olmamamıza rağmen, çift yönlü bir tunnel üzerinden tespit edilmesi oldukça mümkün olan istek/yanıt desenini tespit etmeyi zorlaştırdıkları görülüyor. Birkaç uygulama ve protokol, özellikle HTTP, verileri bu şekilde aktarır. Trafiğin hedefine ve geri dönüşte aynı rotayı takip etmesi, yalnızca zamanlama ve trafik hacmi verilerine sahip olan bir saldırgan için bir tunnel'ın aldığı yolu çıkarsamayı kolaylaştırabilir. Yanıtın farklı bir yol boyunca geri gelmesi, bunu zorlaştırdığı tartışılabilir.

Dahili bir saldırgan veya çoğu harici saldırganla uğraşırken, I2P'nin tek yönlü tunnel'ları, çift yönlü devrelerle maruz kalacak trafikten yarı kadar trafik verisi ortaya çıkarır - sadece akışların kendisine bakarak - bir HTTP isteği ve yanıtı Tor'da aynı yolu takip ederken, I2P'de isteği oluşturan paketler bir veya daha fazla giden tunnel üzerinden çıkar ve yanıtı oluşturan paketler bir veya daha fazla farklı gelen tunnel üzerinden geri gelir.

Gelen ve giden iletişim için iki ayrı tunnel kullanma stratejisi mevcut olan tek teknik değildir ve anonimlik açısından sonuçları vardır. Olumlu tarafta, ayrı tunnel'lar kullanarak bir tunnel'daki katılımcılara analiz için maruz kalan trafik verilerini azaltır - örneğin, bir web tarayıcısından giden tunnel'daki eşler yalnızca bir HTTP GET trafiğini görürken, gelen tunnel'daki eşler tunnel boyunca iletilen yükü görür. Çift yönlü tunnel'larla, tüm katılımcılar örneğin bir yönde 1KB gönderildiği, ardından diğer yönde 100KB gönderildiği gerçeğine erişim sahibi olur. Olumsuz tarafta, tek yönlü tunnel'ları kullanmak profillenmesi ve hesaba katılması gereken iki eş grubunun olduğu anlamına gelir ve öncül saldırıların artan hızını ele almak için ek dikkat gösterilmelidir. Tunnel havuzlama ve oluşturma süreci (eş seçimi ve sıralama stratejileri) öncül saldırı endişelerini en aza indirmelidir.

## Anonimlik

[Hermann ve Grothoff'un makalesi](http://grothoff.org/christian/i2p.pdf) I2P'nin tek yönlü tunnel'larının "kötü bir tasarım kararı gibi göründüğünü" belirtti.

Makalenin ana noktası, tek yönlü tunnel'larda kimlik tespit etme işlemlerinin daha uzun sürdüğü, bu da bir avantaj olsa da, saldırganın tek yönlü durumda daha kesin olabileceğidir. Bu nedenle makale, bunun hiç de bir avantaj olmadığını, özellikle uzun yaşam süreli I2P Site'lar için bir dezavantaj olduğunu iddia etmektedir.

Bu sonuç makale tarafından tam olarak desteklenmemektedir. Tek yönlü tunnel'lar açıkça diğer saldırıları hafifletir ve makaledeki saldırı riskinin çift yönlü tunnel mimarisi üzerindeki saldırılarla nasıl dengeleneceği net değildir.

Bu sonuç, tüm durumlarda geçerli olmayabilecek keyfi bir kesinlik ve zaman ağırlıklandırmasına (takas) dayanmaktadır. Örneğin, birisi olası IP'lerin bir listesini yapabilir ve her birine mahkeme celbi çıkarabilir. Ya da saldırgan her birini sırayla DDoS ile saldırabilir ve basit bir kesişim saldırısı yoluyla I2P Site'ın çöküp çökmediğini veya yavaşlayıp yavaşlamadığını görebilir. Bu nedenle yakın olmak yeterince iyi olabilir veya zaman daha önemli olabilir.

Sonuç, kesinlik ile zaman arasındaki önemin belirli bir ağırlıklandırılmasına dayanmaktadır ve bu ağırlıklandırma yanlış olabilir ve kesinlikle tartışılabilir, özellikle mahkeme celpnameleri, arama emirleri ve nihai doğrulama için mevcut diğer yöntemlerin bulunduğu gerçek dünyada.

Tek yönlü ve çift yönlü tunnel'ların ödünleşimlerinin tam bir analizi açıkça makalenin kapsamı dışındadır ve başka yerlerde de yapılmamıştır. Örneğin, bu saldırı onion-routed ağlar hakkında yayınlanan sayısız olası zamanlama saldırısıyla nasıl karşılaştırılır? Açıkça yazarlar bu analizi yapmamıştır, eğer bunu etkili bir şekilde yapmak mümkünse bile.

Tor çift yönlü tunnel'lar kullanır ve çok fazla akademik inceleme geçirmiştir. I2P tek yönlü tunnel'lar kullanır ve çok az inceleme geçirmiştir. Tek yönlü tunnel'ları savunan bir araştırma makalesinin olmaması bunun kötü bir tasarım seçimi olduğu anlamına mı gelir, yoksa sadece daha fazla çalışmaya mı ihtiyaç duyar? Zamanlama saldırıları ve dağıtık saldırılara karşı savunma yapmak hem I2P hem de Tor'da zordur. Tasarım amacı (yukarıdaki referanslara bakın) tek yönlü tunnel'ların zamanlama saldırılarına karşı daha dirençli olmasıydı. Ancak, makale biraz farklı bir zamanlama saldırısı türü sunuyor. Bu saldırı, ne kadar yenilikçi olursa olsun, I2P'nin tunnel mimarisini (ve dolayısıyla I2P'yi bir bütün olarak) "kötü tasarım" olarak etiketlemek ve ima yoluyla Tor'dan açıkça daha düşük göstermek için yeterli midir, yoksa bu sadece açıkça daha fazla araştırma ve analiz gerektiren bir tasarım alternatifi midir? I2P'yi şu anda Tor ve diğer projelerden daha düşük görmek için başka birçok neden vardır (küçük network boyutu, fon eksikliği, inceleme eksikliği) ama tek yönlü tunnel'lar gerçekten bir neden midir?

Özetle, "kötü tasarım kararı" görünüşe göre (makale çift yönlü tunnel'ları "kötü" olarak etiketlemediği için) "tek yönlü tunnel'lar kesinlikle çift yönlü tunnel'lardan daha kötüdür" ifadesinin kısaltması, ancak bu sonuç makale tarafından desteklenmemektedir.
