---
title: "2018 için Üst Düzey Yol Haritası"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018, yeni protokollerin, yeni işbirliklerinin ve daha net bir odağın yılı olacak."
categories: ["roadmap"]
---

34C3'te tartıştığımız pek çok şeyden biri, gelecek yıl nelere odaklanmamız gerektiğiydi. Özellikle, mutlaka tamamladığımızdan emin olmak istediklerimiz ile olsa gerçekten harika olur dediğimiz şeyler arasında netlik sağlayan ve her iki kategori için de yeni gelenleri dahil etmeye yardımcı olabilecek bir yol haritası istedik. İşte üzerinde karar kıldıklarımız:

## Öncelik: Yeni kripto(grafi!)

Mevcut primitives (ilkel yapıtaşları) ve protokollerin birçoğu hâlâ 2005 dolaylarından kalma özgün tasarımlarını koruyor ve iyileştirmeye ihtiyaç duyuyor. Bir dizi açık önerimiz yıllardır mevcut, ancak kaydedilen ilerleme yavaş oldu. Bunun 2018 için en önemli önceliğimiz olması gerektiği konusunda hepimiz hemfikir olduk. Temel bileşenler şunlardır:

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

Bu önceliğe yönelik çalışmalar birkaç alana ayrılır:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Bu alanların tümünde gerekli çalışmalar yapılmadan, yeni protokol spesifikasyonlarını tüm ağ genelinde kullanıma sunamayız.

## Olması güzel: Kod yeniden kullanımı

Yukarıdaki çalışmaya şimdi başlamanın faydalarından biri, son birkaç yılda kendi protokollerimiz için belirlediğimiz hedeflerin çoğunu karşılayan basit protokoller ve protokol çerçeveleri oluşturmak üzere bağımsız çabalar yürütülmüş olması ve bunların daha geniş topluluk tarafından benimsenmiş olmasıdır. Bu çalışmadan yararlanarak bir "çarpan etkisi" elde ederiz:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Özellikle önerilerimde [Noise Protocol Framework](https://noiseprotocol.org/) ve [SPHINX paket formatı](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)'ndan yararlanacağım. Bunlar için I2P dışında birkaç kişiyle işbirliği ayarladım!

## Öncelik: Clearnet (açık internet) işbirliği

Bu konuda, yaklaşık son altı aydır yavaş yavaş ilgi topluyoruz. PETS2017, 34C3 ve RWC2018 boyunca, daha geniş toplulukla işbirliğini nasıl geliştirebileceğimize dair çok iyi görüşmeler yaptım. Bu, yeni protokoller için mümkün olduğunca fazla inceleme alabilmemizi sağlamak açısından gerçekten önemli. Gördüğüm en büyük engel, şu anda I2P geliştirme işbirliğinin büyük bölümünün bizzat I2P’nin içinde gerçekleşmesi; bu da katkıda bulunmak için gereken çabayı önemli ölçüde artırıyor.

Bu alandaki iki öncelik şunlardır:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Nice-to-have (olsa iyi olur) olarak sınıflandırılan diğer hedefler:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

I2P dışındaki kişilerle yapılacak işbirliklerinin, sürtünmeyi en aza indirmek için, tamamen GitHub üzerinden yürütüleceğini bekliyorum.

## Öncelik: Uzun ömürlü sürümler için hazırlık

I2P artık Debian Sid’de (onların kararsız deposu) ve yaklaşık bir buçuk yıl içinde kararlı hale gelecek; ayrıca Nisan ayında çıkacak bir sonraki LTS sürümüne dahil edilmek üzere Ubuntu deposuna da alındı. Yıllarca kullanımda kalacak I2P sürümlerimiz olmaya başlayacak ve ağdaki varlıklarını yönetebildiğimizden emin olmamız gerekiyor.

Buradaki öncelikli hedefimiz, bir sonraki Debian kararlı sürümüne yetişmek için önümüzdeki yıl içinde mümkün olduğunca çok sayıda yeni protokolü kullanıma sunmaktır. Birden fazla yıla yayılan devreye alma gerektirenler için, ileri uyumluluk değişikliklerini olabildiğince erken entegre etmeliyiz.

## Öncelik: Mevcut uygulamaların eklentiye dönüştürülmesi

Debian modeli, ayrı bileşenler için ayrı paketlere sahip olunmasını teşvik eder. Şu anda birlikte paketlenmiş Java uygulamalarının çekirdek Java router'dan ayrılmasının çeşitli nedenlerle faydalı olacağı konusunda hemfikir olduk:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Önceki önceliklerle birlikte ele alındığında, bu, ana I2P projesini örneğin Linux çekirdeğine benzer bir yöne daha fazla kaydırıyor. Ağın kendisine odaklanmaya daha fazla zaman ayıracağız; ağı kullanan uygulamalara odaklanma işini üçüncü taraf geliştiricilere bırakacağız (API'ler ve kütüphaneler üzerinde son birkaç yılda yaptığımız çalışmalar sayesinde bu artık kayda değer ölçüde daha kolay).

## Olması iyi olur: Uygulama iyileştirmeleri

Üzerinde çalışmak istediğimiz bir dizi uygulama düzeyi iyileştirme var, ancak diğer önceliklerimiz nedeniyle bunu yapacak gerekli geliştirici zamanına şu anda sahip değiliz. Bu, yeni katkıcılar görmeyi çok istediğimiz bir alan! Yukarıdaki ayrıklaştırma tamamlandığında, birinin belirli bir uygulama üzerinde ana Java router'dan bağımsız olarak çalışması önemli ölçüde daha kolay olacaktır.

Yardım almayı çok istediğimiz bu tür uygulamalardan biri I2P Android’dir. Bunu çekirdek I2P sürümleriyle güncel tutacağız ve elimizden geldiğince hataları düzelteceğiz, ancak hem altta yatan kodu hem de kullanılabilirliği iyileştirmek için yapılabilecek çok şey var.

## Öncelik: Susimail ve I2P-Bote'nin stabilizasyonu

Bununla birlikte, yakın vadede özellikle Susimail ve I2P-Bote için düzeltmeler üzerinde çalışmak istiyoruz (bunların bir kısmı 0.9.33'e girdi). Son birkaç yılda bu projeler, diğer I2P uygulamalarına kıyasla daha az geliştirme gördüler; bu yüzden kod tabanlarını standart bir seviyeye getirmeye ve yeni katkıda bulunanların hızlıca dahil olabilmesini sağlamaya zaman ayırmak istiyoruz!

## Olması iyi olur: Ticket triage (önceliklendirme)

Bir dizi I2P alt sistemi ve uygulamasında çok sayıda birikmiş ticket (iş kaydı) var. Yukarıdaki stabilizasyon çabasının bir parçası olarak, uzun süredir devam eden eski sorunlarımızdan bazılarını ele alıp çözmek isteriz. Daha da önemlisi, yeni katkıda bulunanların üzerinde çalışabilecekleri uygun ticket’ları bulabilmeleri için ticket’larımızın doğru şekilde düzenlendiğinden emin olmak istiyoruz.

## Öncelik: Kullanıcı desteği

Yukarıdakilerden odaklanacağımız noktalardan biri, sorun bildirmek için zaman ayıran kullanıcılarla iletişimde kalmaktır. Teşekkür ederiz! Geri bildirim döngüsünü ne kadar kısaltabilirsek, yeni kullanıcıların karşılaştığı sorunları o kadar hızlı çözebiliriz ve topluluğa katılımlarını sürdürmeleri de o kadar olası hale gelir.

## Yardımınızı çok isteriz!


Hepsi çok iddialı görünüyor; gerçekten de öyle! Ancak yukarıdaki maddelerin birçoğu örtüşüyor ve dikkatli planlamayla bunlarda ciddi ilerleme kaydedebiliriz.

Yukarıdaki hedeflerden herhangi birine yardımcı olmakla ilgileniyorsanız, bizimle sohbet etmeye gelin! Bizi OFTC ve Freenode'da (#i2p-dev) ile Twitter'da (@GetI2P) bulabilirsiniz.
