---
title: "Mevcut web sitenizi I2P eepSite olarak nasıl sunabilirsiniz"
date: 2019-06-02
author: "idk"
description: "I2P Yansısı Sunma"
categories: ["tutorial"]
---

Bu blog yazısı, bir clear-net (açık internet) hizmetinin aynasını bir eepSite olarak çalıştırmaya yönelik genel bir rehber olarak tasarlanmıştır. Temel I2PTunnel tunnels hakkındaki önceki blog yazısını ayrıntılandırır.

Ne yazık ki, mevcut bir web sitesini bir eepSite olarak kullanılabilir hale getirmenin tüm olası durumlarını *tamamen* kapsamak muhtemelen imkânsızdır; sunucu tarafı yazılım yelpazesi fazlasıyla çeşitlidir, herhangi bir yazılımın belirli bir kurulumunun pratikteki kendine özgü özelliklerini saymıyorum bile. Bunun yerine, eepWeb'e veya diğer gizli hizmetlere dağıtılmak üzere bir hizmeti hazırlamanın genel sürecini, olabildiğince somut ve net bir şekilde aktarmaya çalışacağım.

Bu rehberin büyük bir kısmı, okuyucuyu bir sohbetin katılımcısı olarak ele alacaktır, özellikle gerçekten bunu kastettiğimde okura doğrudan hitap edeceğim(i.e. "one" yerine "you" kullanarak) ve sık sık bölümleri, okuyucunun soruyor olabileceğini düşündüğüm sorularla başlatacağım. Bu, sonuçta, tıpkı başka herhangi bir hizmeti barındırmak gibi bir yöneticinin kendisini "involved" sayması gereken bir "process".

**YASAL UYARILAR:**

Harika olurdu ama web sitelerini barındırmak için kullanılabilecek her bir yazılım türüne özel talimatlar vermem muhtemelen imkânsız. Bu nedenle, bu eğitim yazar açısından bazı varsayımlar, okur açısından ise eleştirel düşünme ve sağduyu gerektirir. Açık olmak gerekirse, **bu eğitimi takip eden kişinin halihazırda gerçek bir kimlik veya kuruluşa bağlanabilen bir açık web hizmeti işlettiğini varsaydım** ve dolayısıyla kendisini anonimleştirmiyor, yalnızca anonim erişim sunuyor.

Thus, **it makes no attempt whatsoever to anonymize** a connection from one server to another. If you want to run a new, un-linkable hidden service that hosts content not linked to you, then you should not be doing it from your own clearnet server or from your own house.
