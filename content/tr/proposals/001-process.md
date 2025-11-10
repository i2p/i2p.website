---
title: "I2P Öneri Süreci"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Genel Bakış

Bu belge, I2P spesifikasyonlarını nasıl değiştireceğinizi, I2P önerilerinin nasıl çalıştığını ve I2P önerileri ile spesifikasyonlar arasındaki ilişkiyi açıklar.

Bu belge Tor öneri sürecinden adapte edilmiştir ve aşağıdaki içeriğin çoğu orijinal olarak Nick Mathewson tarafından yazılmıştır.

Bu bir bilgilendirici belgedir.

## Motivasyon

Önceden, I2P spesifikasyonlarını güncelleme sürecimiz nispeten resmi değildi: geliştirme forumunda bir öneri sunar ve değişiklikleri tartışırdık, sonra fikir birliğine varır ve taslak değişikliklerle spesifikasyonu yamalardık (bu sırayı takip etmek zorunda değildik) ve son olarak değişiklikleri uygulardık.

Bu süreç birkaç soruna yol açmıştır.

İlk olarak, süreç en verimli haliyle bile, eski süreç spesifikasyonun kodla uyumlu olmamasına neden olabiliyordu. En kötü durumlar ise uygulamanın ertelendiği durumlardı: spesifikasyon ve kod, sürümler boyunca uyumsuz kalabiliyordu.

İkinci olarak, tartışmaya katılmak zordu, çünkü tartışma dizisinin hangi bölümlerinin önerinin bir parçası olduğu veya spesifikasyona hangi değişikliklerin uygulandığı her zaman net değildi. Geliştirme forumları, ayrıca sadece I2P içinde erişilebilir, bu da önerilerin yalnızca I2P kullanan kişiler tarafından görüntülenebileceği anlamına gelir.

Üçüncü olarak, bazı önerileri unutmak çok kolaydı, çünkü forum dizisi listesinde birkaç sayfa geriye gömülebilirlerdi.

## Spesifikasyonları şimdi nasıl değiştiririz

Öncelikle, birisi bir öneri belgesi yazar. Bu, yapılması gereken değişikliği ayrıntılı olarak açıklamalı ve nasıl uygulanacağına dair bir fikir vermelidir. Yeterince ayrıntılı hale geldiğinde, bir öneri olur.

Bir RFC gibi, her öneriye bir numara verilir. RFC'lerin aksine, öneriler zamanla değişebilir ve nihayet kabul edilene veya reddedilene kadar aynı numarayı saklayabilir. Her önerinin geçmişi I2P web sitesi deposunda saklanacaktır.

Öneri depoya girer girmez, ilgili dizide tartışmalı ve fikir birliğine vardığımızda iyi bir fikir olduğu ve uygulanabilir kadar ayrıntılı olduğu kabul edilene kadar geliştirilmelidir. Bu gerçekleştiğinde, öneriyi uygular ve spesifikasyonlara ekleriz. Bu nedenle, spesifikasyonlar I2P protokolü için kanonik belgeler olarak kalır: hiçbir öneri, uygulanan bir özellik için hiçbir zaman kanonik belge olamaz.

(Bu süreç, I2P önerilerinin uygulamadan sonra spesifikasyonlara yeniden entegre edildiği ana istisna dışında, Python Geliştirme Süreci'ne oldukça benzer, oysa PEP'ler *yeni* spesifikasyon haline gelir.)

### Küçük değişiklikler

Kod hemen hemen hemen yazılabiliyorsa spesifikasyona doğrudan küçük değişiklikler yapmak veya bir kod değişikliği gerekmiyorsa, kozmetik değişiklikler yapmak hala kabul edilebilir. Bu belge, mevcut geliştiricilerin *niyetini* yansıtır, gelecekte her zaman bu süreci kullanacağımıza dair kalıcı bir vaat değil: gerçekten heyecanlanma ve kafein ya da M&M destekli tüm gece süren bir hack oturumunda bir şeyler uygulama hakkımızı saklı tutarız.

## Yeni öneriler nasıl eklenir

Bir öneri sunmak için, geliştirme forumunda paylaşın veya öneriyi ekli bir bilet girin.

Bir fikir önerildiğinde, düzgün formatlanmış (aşağıya bakın) bir taslak mevcut olduğunda ve aktif geliştirme topluluğunda bu fikrin değerlendirilmesi gerektiğine dair kabaca bir fikir birliği bulunduğunda, öneri editörleri resmi olarak öneriyi ekleyecektir.

Mevcut öneri editörleri zzz ve str4d'dir.

## Bir öneride neler olmalı

Her önerinin başlık kısmında şu alanlar bulunmalıdır:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- `author` alanı bu önerinin yazarlarının isimlerini içermelidir.
- `thread` alanı, bu önerinin ilk olarak yayınlandığı geliştirici forum başlığına veya bu önerinin tartışılması için oluşturulmuş yeni bir başlığa bir bağlantı olmalıdır.
- `lastupdated` alanı başlangıçta `created` alanına eşit olmalı ve öneri değiştirildiğinde güncellenmelidir.

Gerektiğinde ayarlanması gereken alanlar:

```
:supercedes:
:supercededby:
:editor:
```

- `supercedes` alanı, bu önerinin yerini alacağı tüm önerilerin virgülle ayrılmış bir listesidir. Bu öneriler Reddedilmiş olarak işaretlenmeli ve `supercededby` alanı bu önerinin numarasına ayarlanmalıdır.
- `editor` alanı, önerinin içeriğini önemli ölçüde değiştirmeyen önemli değişiklikler yapıldığında ayarlanmalıdır. İçerik önemli ölçüde değiştiriliyorsa, ya ek bir `author` eklenmelidir ya da bu öneri yerine geçen yeni bir öneri oluşturulmalıdır.

Bu alanlar isteğe bağlı ancak önerilir:

```
:target:
:implementedin:
```

- `target` alanı, önerinin uygulanmasının umulduğu sürümü (eğer Açık veya Kabul Edilmişse) tanımlamalıdır.
- `implementedin` alanı, önerinin uygulandığı sürümü (eğer Tamamlanmış veya Kapatılmışsa) tanımlamalıdır.

Önerinin gövdesi, önerinin ne hakkında olduğunu, ne yaptığını ve hangi durumda olduğunu açıklayan bir Genel Bakış bölümü ile başlamalıdır.

Genel Bakış'tan sonra, öneri daha serbest biçimli hale gelir. Uzunluğuna ve karmaşıklığına bağlı olarak, öneri gerektiği şekilde bölümlere ayrılabilir veya kısa bir söylev formatını takip edebilir. Her öneri, Kabul Edilmeden önce en azından aşağıdaki bilgileri içermelidir, ancak bilgiler bu isimlerdeki bölümlerde olmak zorunda değildir.

**Motivasyon**
: Önerinin çözmeye çalıştığı sorun nedir? Bu sorun neden önemlidir? Birkaç yaklaşım mümkünse, neden bu yolu seçelim?

**Tasarım**
: Yeni veya değiştirilen özelliklerin yüksek düzeyde bir görünümü, yeni veya değiştirilen özelliklerin nasıl çalıştığı, birbirleriyle nasıl çalıştığı ve I2P'nin geri kalanı ile nasıl etkileşimde bulundukları. Bu, önerinin ana gövdesidir. Bazı öneriler yalnızca bir Motivasyon ve Tasarımla başlayacaktır ve Tasarım yaklaşık olarak doğru görünene kadar bir spesifikasyona bekleyecektir.

**Güvenlik etkileri**
: Önerilen değişikliklerin anonimlik üzerindeki etkileri, bu etkilerin ne kadar iyi anlaşıldığı ve benzeri konular.

**Spesifikasyon**
: Önerinin uygulanması için I2P spesifikasyonlarına eklenmesi gerekenlerin ayrıntılı bir tanımı. Bu, sonunda spesifikasyonların içereceği kadar ayrıntılı olmalıdır: bağımsız programcıların, spesifikasyonları temel alarak önerinin birbirleriyle uyumlu uygulamalarını yazabilmeleri mümkün olmalıdır.

**Uyumluluk**
: Öneriyi takip eden I2P sürümleri, öneriyi takip etmeyen sürümlerle uyumlu olacak mı? Eğer öyleyse, uyumluluk nasıl sağlanacak? Genel olarak, uyumluluğu mümkün olduğunca düşürmemeye çalışırız; Mart 2008'den beri bir "bayrak günü" değişikliği yapmadık ve bir başkasını yapmak istemiyoruz.

**Uygulama**
: Öneri, I2P'nin mevcut mimarisi içinde uygulanması zor olacaksa, belge, çalışmasını sağlama konusunda bazı tartışmalar içerebilir. Gerçek yamalar, genel kopya dallarına gitmeli veya Trac'a yüklenmelidir.

**Performans ve ölçeklenebilirlik notları**
: Özellik, performans (RAM, CPU, bant genişliği) veya ölçeklenebilirlik üzerinde bir etkiye sahip olacaksa, bu etkinin ne kadar önemli olacağı konusunda bazı analizler yapılmalıdır, böylece gerçekten pahalı performans gerilemelerinden kaçınabiliriz ve önemsiz kazançlar hakkında zaman kaybetmekten kaçınabiliriz.

**Referanslar**
: Öneri dış belgelerden bahsediyorsa, bunlar listelenmelidir.

## Öneri durumu

**Açık**
: Tartışma altında bir öneri.

**Kabul Edildi**
: Öneri tamamlanmıştır ve uygulamayı amaçlıyoruz. Bu noktadan sonra, önerideki esaslı değişikliklerden kaçınılmalı ve sürecin bir yerde başarısız olduğunun bir belirtisi olarak görülmelidir.

**Tamamlanmış**
: Öneri kabul edilmiş ve uygulanmıştır. Bu noktadan sonra öneri değiştirilmemelidir.

**Kapatılmış**
: Öneri kabul edilmiş, uygulanmış ve ana spesifikasyon belgelerine entegre edilmiştir. Öneri bu noktadan sonra değiştirilmemelidir.

**Reddedildi**
: Açıklanan biçimde özelliği uygulamayacağız, ancak başka bir versiyon yapabiliriz. Ayrıntılar için belgede belirtilen yorumlara bakın. Öneri bu noktadan sonra değiştirilmemelidir; fikrin başka bir versiyonunu gündeme getirmek için yeni bir öneri yazın.

**Taslak**
: Bu henüz tamamlanmış bir öneri değil; belirgin eksik parçalar var. Lütfen bu durumda yeni bir öneri eklemeyin; bunları "fikirler" alt dizinine koyun.

**Revizyon Gerekiyor**
: Öneri fikri iyi, ancak öneri mevcut haliyle kabul edilmesini engelleyen ciddi sorunlara sahip. Ayrıntılar için belgede belirtilen yorumlara bakın.

**Ölü**
: Öneriye uzun süredir dokunulmadı ve yakında kimsenin tamamlayacak gibi görünmüyor. Yeni bir öneren bulursa tekrar "Açık" olabilir.

**Araştırma Gerekiyor**
: Önerinin iyi bir fikir olup olmadığını netleştirmek için çözülmesi gereken araştırma sorunları var.

**Meta**
: Bu bir öneri değil, öneriler hakkında bir belgede.

**Rezerv**
: Bu öneri şu anda uygulamayı planladığımız bir şey değil, ancak bir gün sunduğu gibi bir şey yapmaya karar verirsek onu canlandırmak isteyebiliriz.

**Bilgilendirici**
: Bu öneri, yaptığı şeyin son sözü. Biri bir alt sistem için yeni bir spesifikasyona kopyalayıp yapıştırana kadar bir spesifikasyon haline gelmeyecek.

Editörler, önerilerin doğru durumunu, kabaca fikir birliğine dayalı ve kendi takdirlerine bağlı olarak korurlar.

## Öneri numaralandırma

000-099 numaraları, özel ve meta-öneriler için ayrılmıştır. 100 ve üzeri sayılar gerçek öneriler için kullanılır. Numaralar geri dönüştürülmez.

## Referanslar

- [Tor Öneri Süreci](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
