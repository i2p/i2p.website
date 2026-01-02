---
title: "Geliştirici Yönergeleri ve Kodlama Stili"
description: "I2P'ye katkıda bulunmak için uçtan uca yönergeler: iş akışı, sürüm döngüsü, kodlama stili, günlükleme, lisanslama ve sorun yönetimi"
slug: "dev-guidelines"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Önce [Yeni Geliştiriciler Kılavuzu](/docs/develop/new-developers/)'nu okuyun.

## Temel Yönergeler ve Kodlama Stili

Aşağıdakilerin çoğu, açık kaynak projelerde veya ticari bir programlama ortamında çalışmış olan herkes için sağduyu gerektiren konular olmalıdır. Aşağıdakiler çoğunlukla ana geliştirme dalı i2p.i2p için geçerlidir. Diğer dallar, eklentiler ve harici uygulamalar için yönergeler önemli ölçüde farklı olabilir; rehberlik için ilgili geliştiriciyle görüşün.

### Topluluk

- Lütfen sadece kod yazmayın. Mümkünse, aşağıdakiler dahil olmak üzere diğer geliştirme faaliyetlerine katılın: IRC ve i2pforum.i2p üzerinde geliştirme tartışmaları ve destek; test etme; hata bildirimi ve yanıtlar; dokümantasyon; kod incelemeleri; vb.
- Aktif geliştiriciler IRC `#i2p-dev` kanalında periyodik olarak erişilebilir olmalıdır. Mevcut sürüm döngüsünün farkında olun. Özellik dondurma, etiket dondurma ve bir sürüm için check-in son tarihi gibi sürüm kilometre taşlarına uyun.

### Sürüm Döngüsü

Normal sürüm döngüsü 10-16 hafta olup, yılda dört sürüm yapılır. Aşağıda tipik bir 13 haftalık döngü içindeki yaklaşık son tarihler yer almaktadır. Her sürüm için gerçek son tarihler, sürüm yöneticisi tarafından tüm ekiple istişare edildikten sonra belirlenir.

- Önceki sürümden 1–2 gün sonra: Trunk'a check-in yapılmasına izin verilir.
- Önceki sürümden 2–3 hafta sonra: Diğer dallardan trunk'a büyük değişikliklerin aktarılması için son tarih.
- Sürümden 4–5 hafta önce: Yeni ana sayfa bağlantıları talep etmek için son tarih.
- Sürümden 3–4 hafta önce: Özellik dondurma. Büyük yeni özellikler için son tarih.
- Sürümden 2–3 hafta önce: Varsa yeni ana sayfa bağlantı taleplerini gözden geçirmek için proje toplantısı düzenlenir.
- Sürümden 10–14 gün önce: String dondurma. Çevrilmiş (etiketlenmiş) string'lerde daha fazla değişiklik yapılmaz. String'ler Transifex'e gönderilir, çeviri son tarihi Transifex'te duyurulur.
- Sürümden 10–14 gün önce: Özellik son tarihi. Bu tarihten sonra yalnızca hata düzeltmeleri. Artık özellik, refactoring veya temizleme yapılmaz.
- Sürümden 3–4 gün önce: Çeviri son tarihi. Çeviriler Transifex'ten çekilir ve check-in yapılır.
- Sürümden 3–4 gün önce: Check-in son tarihi. Bu tarihten sonra sürüm oluşturucusunun izni olmadan check-in yapılmaz.
- Sürümden saatler önce: Kod inceleme son tarihi.

### Git

- Dağıtık kaynak kontrol sistemleri hakkında temel bir anlayışa sahip olun, daha önce git kullanmamış olsanız bile. Gerekirse yardım isteyin. Bir kez gönderildikten sonra, check-in'ler kalıcıdır; geri alma yoktur. Lütfen dikkatli olun. Daha önce git kullanmadıysanız, küçük adımlarla başlayın. Bazı küçük değişiklikleri check-in yapın ve nasıl gittiğini görün.
- Değişikliklerinizi check-in yapmadan önce test edin. Check-in‑önce‑test geliştirme modelini tercih ediyorsanız, kendi hesabınızda kendi geliştirme dalınızı kullanın ve iş bittiğinde bir MR oluşturun. Build'i bozmayın. Regresyonlara neden olmayın. Buna neden olursanız (olur), lütfen değişikliğinizi gönderdikten sonra uzun süre ortadan kaybolmayın.
- Değişikliğiniz önemsiz değilse veya insanların test etmesini istiyorsanız ve değişikliğinizin test edilip edilmediğini bilmek için iyi test raporlarına ihtiyacınız varsa, `history.txt` dosyasına bir check-in yorumu ekleyin ve `RouterVersion.java` dosyasındaki build revizyonunu artırın.
- Sürüm döngüsünün geç aşamalarında ana i2p.i2p dalına büyük değişiklikler check-in yapmayın. Bir proje birkaç günden fazla sürecekse, git'te kendi hesabınızda kendi dalınızı oluşturun ve geliştirmeyi orada yapın, böylece sürümleri engellemezsiniz.
- Büyük değişiklikler için (genel olarak konuşursak, 100 satırdan fazla veya üçten fazla dosyaya dokunan), kendi GitLab hesabınızda yeni bir dala check-in yapın, bir MR oluşturun ve bir gözden geçiren atayın. MR'ı kendinize atayın. Gözden geçiren onayladıktan sonra MR'ı kendiniz birleştirin.
- Ana I2P_Developers hesabında WIP dalları oluşturmayın (i2p.www hariç). WIP kendi hesabınıza aittir. İş bittiğinde bir MR oluşturun. Ana hesaptaki tek dallar, bir nokta sürümü gibi gerçek fork'lar için olmalıdır.
- Geliştirmeyi şeffaf bir şekilde ve topluluğu göz önünde bulundurarak yapın. Sık sık check-in yapın. Yukarıdaki yönergeleri göz önünde bulundurarak mümkün olduğunca sık ana dala check-in yapın veya birleştirin. Kendi dalınızda/hesabınızda büyük bir proje üzerinde çalışıyorsanız, insanlara haber verin böylece takip edebilir, inceleyebilir, test edebilir ve yorum yapabilirler.

### Kodlama Stili

- Kodun çoğu boyunca kodlama stili girinti için 4 boşluktur. Tab kullanmayın. Kodu yeniden biçimlendirmeyin. IDE'niz veya editörünüz her şeyi yeniden biçimlendirmek istiyorsa, kontrol altına alın. Bazı yerlerde kodlama stili farklıdır. Sağduyuyu kullanın. Değiştirdiğiniz dosyadaki stili taklit edin.
- Tüm yeni public ve package-private sınıflar ve metodlar Javadocs gerektirir. `@since` sürüm-numarası ekleyin. Yeni private metodlar için Javadocs'lar arzu edilir.
- Eklenen herhangi bir Javadocs için doclint hatası veya uyarısı olmamalıdır. Kontrol etmek için Oracle Java 14 veya üzeri ile `ant javadoc` çalıştırın. Tüm parametrelerin `@param` satırları, tüm void olmayan metodların `@return` satırları, fırlatıldığı belirtilen tüm istisnaların `@throws` satırları olmalı ve HTML hatası olmamalıdır.
- `core/` (i2p.jar) içindeki sınıflar ve i2ptunnel'ın bazı bölümleri resmi API'mizin bir parçasıdır. Bu API'ye dayanan birkaç tree-dışı plugin ve diğer uygulamalar vardır. Uyumluluğu bozan herhangi bir değişiklik yapmamaya dikkat edin. Genel fayda sağlamadıkça API'ye metodlar eklemeyin. API metodları için Javadocs'lar açık ve eksiksiz olmalıdır. API'yi ekler veya değiştirirseniz, web sitesindeki belgeleri de güncelleyin (i2p.www dalı).
- Uygun yerlerde çeviri için string'leri etiketleyin, bu tüm UI string'leri için geçerlidir. Gerçekten gerekli olmadıkça mevcut etiketli string'leri değiştirmeyin, çünkü mevcut çevirileri bozar. Çevirmenlerin sürümden önce güncelleme şansı olması için sürüm döngüsündeki etiket dondurmasından sonra etiketli string'ler eklemeyin veya değiştirmeyin.
- Mümkün olduğunca generics ve concurrent sınıflar kullanın. I2P yüksek düzeyde çok thread'li bir uygulamadır.
- FindBugs/SpotBugs tarafından yakalanan yaygın Java tuzaklarına aşina olun. Daha fazla bilgi için `ant findbugs` çalıştırın.
- 0.9.47 sürümünden itibaren I2P'yi derlemek ve çalıştırmak için Java 8 gereklidir. Gömülü alt sistemlerde Java 7 veya 8 sınıflarını veya metodlarını kullanmayın: addressbook, core, i2ptunnel.jar (UI olmayan), mstreaming, router, routerconsole (sadece haberler), streaming. Bu alt sistemler yalnızca Java 6 gerektiren Android ve gömülü uygulamalar tarafından kullanılır. Tüm sınıflar Android API 14'te mevcut olmalıdır. Bu alt sistemlerde Java 7 dil özellikleri, mevcut Android SDK sürümü tarafından destekleniyorsa ve Java 6 uyumlu koda derlendiyse kabul edilebilir.
- Try-with-resources gömülü alt sistemlerde kullanılamaz çünkü çalışma zamanında `java.lang.AutoCloseable` gerektirir ve bu Android API 19'a (KitKat 4.4) kadar mevcut değildir.
- `java.nio.file` paketi gömülü alt sistemlerde kullanılamaz çünkü Android API 26'ya (Oreo 8) kadar mevcut değildir.
- Yukarıdaki sınırlamalar dışında, Java 8 sınıfları, metodları ve yapıları yalnızca şu alt sistemlerde kullanılabilir: BOB, desktopgui, i2psnark, i2ptunnel.war (UI), jetty‑i2p.jar, jsonrpc, routerconsole (haberler hariç), SAM, susidns, susimail, systray.
- Plugin yazarları `plugin.config` dosyası aracılığıyla herhangi bir minimum Java sürümü gerektirebilir.
- İlkel tipler ve sınıflar arasında açıkça dönüştürme yapın; autoboxing/unboxing'e güvenmeyin.
- `URL` kullanmayın. `URI` kullanın.
- `Exception` yakalamayın. `RuntimeException` ve checked exception'ları ayrı ayrı yakalayın.
- `String.getBytes()` metodunu UTF‑8 charset argümanı olmadan kullanmayın. Ayrıca `DataHelper.getUTF8()` veya `DataHelper.getASCII()` kullanabilirsiniz.
- Dosyaları okurken veya yazarken her zaman UTF‑8 charset belirtin. `DataHelper` yardımcı programları faydalı olabilir.
- `String.toLowerCase()` veya `String.toUpperCase()` kullanırken her zaman bir locale (örneğin `Locale.US`) belirtin. `String.equalsIgnoreCase()` kullanmayın, çünkü locale belirtilemez.
- `String.split()` kullanmayın. `DataHelper.split()` kullanın.
- Tarih ve saatleri biçimlendirmek için kod eklemeyin. `DataHelper.formatDate()` ve `DataHelper.formatTime()` kullanın.
- `InputStream`'lerin ve `OutputStream`'lerin finally bloklarında kapatıldığından emin olun.
- Tüm `for` ve `while` blokları için, tek satır olsa bile `{}` kullanın. `if`, `else` veya `if-else` bloğundan herhangi biri için `{}` kullanırsanız, tüm bloklar için kullanın. `} else {` tek bir satıra koyun.
- Alanları mümkün olan her yerde `final` olarak belirtin.
- `I2PAppContext`, `RouterContext`, `Log` veya router veya context öğelerine yapılan diğer referansları static alanlarda saklamayın.
- Constructor'larda thread başlatmayın. `Thread` yerine `I2PAppThread` kullanın.

### Günlükleme

Aşağıdaki yönergeler router, web uygulamaları ve tüm eklentiler için geçerlidir.

- Varsayılan log seviyesinde (WARN, INFO ve DEBUG) görüntülenmeyen herhangi bir mesaj için, mesaj statik bir string olmadığı sürece (birleştirme yok), gereksiz nesne yığılmasını önlemek için log çağrısından önce her zaman `log.shouldWarn()`, `log.shouldInfo()` veya `log.shouldDebug()` kullanın.
- Varsayılan log seviyesinde (ERROR, CRIT ve `logAlways()`) görüntülenebilecek log mesajları kısa, net ve teknik olmayan bir kullanıcı için anlaşılır olmalıdır. Bu, aynı zamanda görüntülenebilecek istisna nedeni metnini de içerir. Hatanın gerçekleşme olasılığı yüksekse (örneğin, form gönderme hatalarında) çeviri yapmayı düşünün. Aksi takdirde, çeviri gerekli değildir, ancak başka bir yerde çeviri için zaten etiketlenmiş bir stringi arayıp yeniden kullanmak faydalı olabilir.
- Varsayılan log seviyesinde görüntülenmeyen log mesajları (WARN, INFO ve DEBUG) geliştirici kullanımı için tasarlanmıştır ve yukarıdaki gereksinimlere sahip değildir. Ancak, WARN mesajları Android log sekmesinde mevcuttur ve sorunları gidermede kullanıcılara yardımcı olabilir, bu nedenle WARN mesajlarıyla da biraz özen gösterin.
- INFO ve DEBUG log mesajları, özellikle sık çalışan kod yollarında (hot code paths) dikkatli kullanılmalıdır. Geliştirme sırasında faydalı olsa da, test tamamlandıktan sonra bunları kaldırmayı veya yorum satırına almayı düşünün.
- stdout veya stderr'e (wrapper log) log yazmayın.

### Lisanslar

- Yalnızca kendinizin yazdığı kodu commit edin. Diğer kaynaklardan gelen herhangi bir kod veya kütüphane JAR dosyasını commit etmeden önce, neden gerekli olduğunu gerekçelendirin, lisansın uyumlu olduğunu doğrulayın ve sürüm yöneticisinden onay alın.
- Harici kod veya JAR dosyaları eklemek için onay alırsanız ve ikili dosyalar herhangi bir Debian veya Ubuntu paketinde mevcutsa, harici paketi kullanmak için derleme ve paketleme seçeneklerini uygulamalısınız. Değiştirilecek dosyaların kontrol listesi: `build.properties`, `build.xml`, `debian/control`, `debian/i2p-router.install`, `debian/i2p-router.links`, `debian/rules`, `sub-build.xml`.
- Harici kaynaklardan commit edilen herhangi bir görsel için, önce lisansın uyumlu olduğunu doğrulamak sizin sorumluluğunuzdadır. Commit yorumuna lisans ve kaynak bilgilerini dahil edin.

### Hatalar

- Sorunları yönetmek herkesin işidir; lütfen yardım edin. Yardım edebileceğiniz sorunlar için [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)'ı takip edin. Yapabiliyorsanız sorunlara yorum yapın, düzeltin ve kapatın.
- Yeni geliştiriciler sorunları düzelterek başlamalıdır. Bir düzeltmeniz olduğunda, yamanızı soruna ekleyin ve `review-needed` anahtar kelimesini ekleyin. İncelenip başarıyla onaylanana ve değişikliklerinizi kontrol edene kadar sorunu kapatmayın. Bunu birkaç ticket için sorunsuz bir şekilde yaptıktan sonra, yukarıdaki normal prosedürü izleyebilirsiniz.
- Düzelttiğinizi düşündüğünüzde bir sorunu kapatın. Ticket'ları doğrulamak ve kapatmak için bir test departmanımız yok. Düzelttiğinizden emin değilseniz, kapatın ve "Düzelttiğimi düşünüyorum, lütfen test edin ve hala bozuksa yeniden açın" diyen bir not ekleyin. Dev build numarası veya revizyon ile bir yorum ekleyin ve milestone'ı bir sonraki sürüme ayarlayın.
