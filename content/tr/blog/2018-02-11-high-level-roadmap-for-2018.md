---
title: "2018 için Üst Düzey Yol Haritası"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018, yeni protokollerin, yeni işbirliklerinin ve daha rafine bir odağın yılı olacak."
categories: ["roadmap"]
---

34C3'te tartıştığımız birçok şeyden biri, gelecek yıl nelere odaklanmamız gerektiğiydi. Özellikle, mutlaka tamamlamak istediğimiz şeylerle olsa çok iyi olur dediğimiz şeyleri açıkça ayıran bir yol haritası istedik ve her iki kategoriye de yeni gelenleri sürece dahil etmeye yardımcı olabilmeyi amaçladık. İşte ortaya koyduklarımız:

## Öncelik: Yeni kripto(grafi!)

Mevcut primitives (temel yapıtaşları) ve protokollerin çoğu hâlâ 2005 dolaylarından kalma orijinal tasarımlarını koruyor ve iyileştirmeye ihtiyaç duyuyor. Birkaç yıldır çeşitli fikirleri içeren çok sayıda açık önerimiz var, ancak ilerleme yavaş oldu. Hepimiz bunun 2018 için en yüksek önceliğimiz olması gerektiği konusunda hemfikir olduk. Temel bileşenler şunlardır:

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

Bu öncelik kapsamındaki çalışmalar birkaç alana ayrılır:

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Bu alanların tümünde çalışma yapmadan, tüm ağ genelinde yeni protokol spesifikasyonlarını yayımlayamayız.

## Olması güzel: Kodun yeniden kullanımı

Yukarıdaki çalışmaya şimdi başlamanın faydalarından biri, son birkaç yılda kendi protokollerimiz için belirlediğimiz hedeflerin çoğunu karşılayan basit protokoller ve protokol çerçeveleri oluşturmak üzere bağımsız çabalar yürütülmüş olması ve bunların daha geniş toplulukta ivme kazanmış olmasıdır. Bu çalışmadan yararlanarak bir "kuvvet çarpanı" etkisi elde ediyoruz:

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Özellikle önerilerim [Noise Protocol Framework](https://noiseprotocol.org/)'tan ve [SPHINX packet format](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html)'tan yararlanacak. Bunlar için I2P dışında birkaç kişiyle işbirliği konusunda anlaşmış durumdayım!

## Öncelik: Clearnet işbirliği

On that topic, we've been slowly building interest over the last six months or so. Across PETS2017, 34C3, and RWC2018, I've had some very good discussions about ways in which we can improve collaboration with the wider community. This is really important to ensure we can garner as much review as possible for new protocols. The biggest blocker I've seen is the fact that the majority of I2P development collaboration currently happens inside I2P itself, which significantly increases the effort required to contribute.

Bu alandaki iki öncelik şunlardır:

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Zorunlu olmayan, olması tercih edilen diğer hedefler:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

I2P dışındaki kişilerle yapılacak işbirliklerinin, sürtünmeyi en aza indirmek için tamamen GitHub üzerinden yürütüleceğini bekliyorum.

## Öncelik: Uzun ömürlü sürümlere hazırlık

I2P artık Debian Sid’de (onların unstable deposu) yer alıyor; bu sürüm yaklaşık bir buçuk yıl içinde kararlı hale gelecek ve ayrıca Nisan ayında çıkacak bir sonraki LTS sürümüne dahil edilmek üzere Ubuntu deposuna da alındı. Uzun yıllar boyunca kullanımda kalacak I2P sürümlerimiz olacak ve ağda varlıklarını yönetebildiğimizden emin olmamız gerekiyor.

Buradaki birincil hedef, bir sonraki Debian kararlı sürümüne yetişmek için, önümüzdeki yıl içinde yeni protokollerin mümkün olduğunca çoğunu devreye almaktır. Birden çok yıla yayılan devreye alma gerektirenler için, ileri uyumluluk değişikliklerini olabildiğince erken dahil etmeliyiz.

## Öncelik: Mevcut uygulamaların eklentileştirilmesi

Debian modeli, ayrı bileşenler için ayrı paketlere sahip olunmasını teşvik eder. Halihazırda birlikte paketlenmiş Java uygulamalarının çekirdek Java router'dan ayrıştırılmasının birkaç nedenle faydalı olacağı konusunda hemfikir olduk:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Önceki önceliklerle birlikte, bu durum ana I2P projesini, örneğin Linux çekirdeğinde olduğu gibi, o yöne daha fazla yaklaştırıyor. Ağın kendisine odaklanmaya daha fazla zaman ayıracağız; ağı kullanan uygulamalara odaklanmayı ise üçüncü taraf geliştiricilere bırakacağız (bu, son birkaç yılda API'ler ve kütüphaneler üzerinde yaptığımız çalışmaların ardından önemli ölçüde daha kolay).

## Olması iyi olur: Uygulama iyileştirmeleri

Üzerinde çalışmak istediğimiz, ancak diğer önceliklerimiz nedeniyle şu anda geliştirici zamanı ayıramadığımız bir dizi uygulama düzeyinde iyileştirme var. Bu alanda yeni katkıcılar görmeyi çok isteriz! Yukarıdaki bağımsızlaştırma tamamlandığında, birinin belirli bir uygulama üzerinde ana Java router'dan bağımsız olarak çalışması önemli ölçüde daha kolay olacaktır.

Yardım almak istediğimiz uygulamalardan biri I2P Android'dir. Onu çekirdek I2P sürümleriyle güncel tutacağız ve elimizden geldiğince hataları düzelteceğiz, ancak hem altta yatan kodu hem de kullanılabilirliği iyileştirmek için yapılabilecek çok şey var.

## Öncelik: Susimail ve I2P-Bote'nin kararlılığının sağlanması

Bununla birlikte, kısa vadede özellikle Susimail ve I2P-Bote düzeltmeleri üzerinde çalışmak istiyoruz (bunlardan bazıları 0.9.33 sürümüne eklendi). Son birkaç yılda diğer I2P uygulamalarına göre üzerlerinde daha az çalışıldı; bu nedenle kod tabanlarını beklenen düzeye getirmeye ve yeni katkıda bulunanların kolayca dahil olabilmesini sağlamaya biraz zaman ayırmak istiyoruz!

## Olması iyi olur: Bilet triyajı

Çeşitli I2P alt sistemleri ve uygulamalarında çok sayıda birikmiş iş kaydımız (ticket) var. Yukarıda belirtilen kararlılık çalışmasının bir parçası olarak, daha eski ve uzun süredir devam eden sorunlarımızdan bazılarını temizlemeyi çok isteriz. Daha da önemlisi, yeni katkıda bulunanların üzerinde çalışabilecekleri uygun iş kayıtlarını bulabilmeleri için iş kayıtlarımızın doğru şekilde düzenlenmiş olduğundan emin olmak istiyoruz.

## Öncelik: Kullanıcı desteği

Yukarıda değinilenlerin özellikle odaklanacağımız bir yönü, sorun bildirmek için zaman ayıran kullanıcılarla iletişimde kalmak olacak. Teşekkür ederiz! Geri bildirim döngüsünü ne kadar kısaltabilirsek, yeni kullanıcıların karşılaştığı sorunları o kadar hızlı çözebiliriz ve topluluğa katılmaya devam etmeleri de o kadar olası olur.

## Yardımınızı çok isteriz!

Tüm bunlar çok iddialı görünüyor ve öyle de! Ancak yukarıdaki maddelerin birçoğu örtüşüyor ve dikkatli planlamayla bunlarda ciddi bir ilerleme sağlayabiliriz.

Eğer yukarıdaki hedeflerden herhangi birine yardımcı olmakla ilgileniyorsanız, bizimle sohbet edin! Bizi OFTC ve Freenode'da (#i2p-dev) ve Twitter'da (@GetI2P) bulabilirsiniz.
