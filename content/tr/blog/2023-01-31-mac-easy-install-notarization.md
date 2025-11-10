---
title: "Mac Easy Install için Noter Onayı hakkında güncelleme"
date: 2023-01-31
author: "idk, sadie"
description: "Mac için Easy Install Bundle takılı kaldı"
categories: ["release"]
API_Translate: doğru
---

Mac için I2P Easy-Install Bundle (kolay kurulum paketi), bakımcısının ayrılması nedeniyle son iki sürümdür güncellemelerde duraksamalar yaşıyor. Mac için Easy-Install Bundle kullanan kullanıcıların, yakın zamanda indirme sayfasına yeniden eklenen klasik Java tarzı yükleyiciye geçmeleri önerilir. 1.9.0 sürümünde bilinen güvenlik sorunları vardır ve barındırma hizmetleri veya uzun vadeli herhangi bir kullanım için uygun değildir. Kullanıcıların mümkün olan en kısa sürede geçiş yapmaları tavsiye edilir. Easy-Install Bundle'ın ileri düzey kullanıcıları, paketi kaynak koddan derleyip yazılımı kendi imzalarıyla imzalayarak bunu aşabilir.

## MacOS için Notarization (Apple uygulama noter onayı) Süreci

Bir uygulamayı Apple kullanıcılarına dağıtma sürecinde birçok adım vardır. Bir uygulamanın .dmg olarak güvenli bir şekilde dağıtılabilmesi için, uygulamanın notarization (Apple tarafından yapılan uygulama onaylama süreci) işleminden geçmesi gerekir. Bir uygulamayı notarization için gönderebilmek için, geliştiricinin, biri kod imzalama için, diğeri de uygulamanın kendisini imzalamak için kullanılan sertifikaları içeren bir sertifika kümesi kullanarak uygulamayı imzalaması gerekir. Bu imzalama, derleme sürecinin belirli noktalarında, son kullanıcılara dağıtılan nihai .dmg paketinin oluşturulmasından önce gerçekleştirilmelidir.

I2P Java karmaşık bir uygulamadır ve bu nedenle, uygulamada kullanılan kod türlerini Apple'ın sertifikalarıyla eşleştirmek ve geçerli bir zaman damgası üretmek için imzalamanın nerede yapılması gerektiğini belirlemek deneme-yanılma sürecidir. Bu karmaşıklık nedeniyle, geliştiricilere yönelik mevcut dokümantasyon, ekibin başarılı bir notarization (Apple'ın uygulama noter onayı süreci) ile sonuçlanacak faktörlerin doğru kombinasyonunu anlamasına yardımcı olmakta yetersiz kalıyor.

Bu zorluklar, bu sürecin tamamlanmasına ilişkin zaman çizelgesini öngörmeyi zorlaştırıyor. Derleme ortamını temizleyip süreci uçtan uca izleyene kadar işi bitirdiğimizi bilemeyeceğiz. İyi haber şu ki, ilk denemede 50’den fazla olan hata sayısını notarizasyon sürecinde yalnızca 4’e kadar düşürdük ve bunun Nisan ayındaki bir sonraki sürümden önce ya da tam zamanında tamamlanacağını makul biçimde öngörebiliyoruz.

## Yeni macOS I2P Kurulumları ve Güncellemeleri için Seçenekler

Yeni I2P katılımcıları, macOS için 1.9.0 yazılımına yönelik Easy Installer'ı hâlâ indirebilir. Nisan sonuna doğru bir sürümü hazır etmeyi umuyorum. Notarizasyon başarılı olur olmaz en son sürüme güncellemeler kullanıma sunulacak.

Klasik kurulum seçeneği de mevcuttur. Bu, Java’nın ve I2P yazılımının .jar tabanlı yükleyici aracılığıyla indirilmesini gerektirecektir.

[Jar Kurulum Talimatları burada mevcuttur](https://geti2p.net/en/download/macos)

Easy-Install kullanıcıları, yerel olarak üretilmiş bir geliştirme derlemesi kullanarak en son sürüme güncelleyebilir.

[Kolay Kurulum Derleme Yönergeleri burada mevcuttur](https://i2pgit.org/i2p-hackers/i2p-jpackage-mac/-/blob/master/BUILD.md)

Ayrıca yazılımı kaldırmak, I2P yapılandırma dizinini silmek ve .jar yükleyicisini kullanarak I2P’yi yeniden yüklemek seçeneği de vardır.
