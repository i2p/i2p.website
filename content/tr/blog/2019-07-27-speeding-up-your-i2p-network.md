---
title: "I2P ağınızı hızlandırma"
date: 2019-07-27
author: "mhatta"
description: "I2P ağınızı hızlandırma"
categories: ["tutorial"]
---

*Bu gönderi, mhatta'nın için aslen oluşturulmuş materyalden doğrudan uyarlanmıştır* [Medium blogu](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Asıl gönderinin hakkı ona aittir. Bazı yerlerde* *I2P'nin eski sürümlerini güncelmiş gibi andığı kısımlar güncellendi ve hafif bir* *düzenlemeden geçirildi. -idk*

Başlatıldıktan hemen sonra, I2P çoğu zaman biraz yavaş görünür. Bu doğru; hepimiz nedenini biliyoruz: doğası gereği, [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) (gizliliğe odaklı bir yönlendirme tekniği) gizliliğe sahip olabilmeniz için interneti kullanma konusundaki tanıdık deneyime ek yük getirir, ancak bu da birçok, hatta çoğu I2P hizmeti için verilerinizin varsayılan olarak 12 atlamadan geçmesi gerektiği anlamına gelir.

![Çevrimiçi anonimlik araçlarının analizi](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Ayrıca, Tor'dan farklı olarak, I2P esas olarak kapalı bir ağ olarak tasarlanmıştır. I2P içinde [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) veya diğer kaynaklara kolayca erişebilirsiniz, ancak I2P üzerinden [clearnet (açık internet)](https://en.wikipedia.org/wiki/Clearnet_(networking)) web sitelerine erişmeniz amaçlanmamıştır. Clearnet'e erişmek için [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network))'un çıkış düğümlerine benzer birkaç I2P "outproxies" (çıkış proxy'leri) vardır, ancak clearnet'e gitmek, halihazırda içeri 6 atlama, dışarı 6 atlama olan bağlantıda fiilen *ek bir* atlama sayıldığından bunların çoğunu kullanmak çok yavaştır.

Birkaç sürüm öncesine kadar, bu sorunla başa çıkmak daha da zordu; çünkü birçok I2P router kullanıcısı, router'larının bant genişliği ayarlarını yapılandırmakta zorluk yaşıyordu. Yapabilen herkes bant genişliği ayarlarını doğru şekilde ayarlamak için zaman ayırırsa, bu yalnızca sizin bağlantınızı değil, I2P ağının tamamını da iyileştirir.

## Bant genişliği sınırlarını ayarlama

I2P bir eşler arası ağ olduğundan, ağ bant genişliğinizin bir kısmını diğer eşlerle paylaşmanız gerekir. Ne kadarını paylaşacağınızı "I2P Bandwidth Configuration" içinde seçebilirsiniz ("I2P Router Console" içindeki "Applications and Configuration" bölümündeki "Configure Bandwidth" düğmesi veya http://localhost:7657/config).

![I2P Bant Genişliği Yapılandırması](https://geti2p.net/images/blog/bandwidthmenu.png)

48 KBps gibi çok düşük bir paylaşılan bant genişliği sınırı görüyorsanız, muhtemelen paylaşılan bant genişliği ayarınızı varsayılandan değiştirmemişsinizdir. Bu blog yazısının uyarlandığı materyalin asıl yazarının belirttiği gibi, I2P, kullanıcı bağlantısında sorunlara yol açmamak için kullanıcı bunu ayarlayana kadar varsayılan olarak çok düşük bir paylaşılan bant genişliği sınırına sahiptir.

Ancak pek çok kullanıcı hangi bant genişliği ayarlarını değiştirmesi gerektiğini tam olarak bilemeyebileceğinden, [I2P 0.9.38 sürümü](https://geti2p.net/en/download) bir Yeni Kurulum Sihirbazı sundu. Bu sihirbaz bir Bant Genişliği Testi içerir, bu test M-Lab'in [NDT](https://www.measurementlab.net/tests/ndt/) testi sayesinde bant genişliğini otomatik olarak tespit eder ve I2P'nin bant genişliği ayarlarını buna göre ayarlar.

Sihirbazı yeniden çalıştırmak isterseniz, örneğin İnternet servis sağlayıcınızda bir değişiklikten sonra veya I2P'yi 0.9.38 sürümünden önce kurduğunuz için, onu 'Setup' bağlantısından 'Help & FAQ' sayfasında yeniden başlatabilir veya sihirbaza doğrudan http://localhost:7657/welcome adresinden erişebilirsiniz.

!["Setup"u bulabiliyor musunuz?](https://geti2p.net/images/blog/sidemenu.png)

Sihirbazı kullanmak basittir, sadece "Next"e tıklamaya devam edin. Bazen M-Lab'ın seçtiği ölçüm sunucuları hizmet dışı olur ve test başarısız olur. Böyle bir durumda, "Previous"a tıklayın (web tarayıcınızın "back" düğmesini kullanmayın), ardından tekrar deneyin.

![Bant Genişliği Test Sonuçları](https://geti2p.net/images/blog/bwresults.png)

## I2P'yi sürekli çalıştırma

Bant genişliğini ayarladıktan sonra bile bağlantınız hâlâ yavaş olabilir. Dediğim gibi, I2P bir P2P ağıdır. I2P router'ınızın diğer eşler tarafından keşfedilmesi ve I2P ağına entegre olması biraz zaman alacaktır. Router'ınız iyi biçimde entegre olabilecek kadar uzun süre çalışmazsa ya da sık sık düzgün kapatma yapmadan kapatıyorsanız, ağ oldukça yavaş kalacaktır. Öte yandan, I2P router'ınızı ne kadar uzun süre kesintisiz çalıştırırsanız, bağlantınız o kadar hızlı ve daha kararlı olur ve ağda bant genişliği payınızın daha fazlası kullanılır.

Ancak, birçok kişi I2P router'ını çalışır durumda tutamayabilir. Böyle bir durumda, I2P router'ı yine de VPS gibi uzak bir sunucuda çalıştırıp ardından SSH ile port yönlendirme kullanabilirsiniz.
