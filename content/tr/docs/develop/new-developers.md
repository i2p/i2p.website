---
title: "Yeni Geliştirici Kılavuzu"
description: "I2P'ye katkıda bulunmaya nasıl başlanır: çalışma materyalleri, kaynak kodu, derleme, fikirler, yayınlama, topluluk, çeviriler ve araçlar"
slug: "new-developers"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
notes: çeviri bölümünü güncelle
---

I2P üzerinde çalışmaya başlamak mı istiyorsunuz? Harika! İşte web sitesine veya yazılıma katkıda bulunmaya, geliştirme yapmaya veya çeviri oluşturmaya başlamak için hızlı bir kılavuz.

Kodlamaya henüz hazır değil misiniz? Önce [katılmayı](/get-involved/) deneyin.

## Java'yı Tanıyın

I2P router'ı ve gömülü uygulamaları ana geliştirme dili olarak Java kullanır. Java konusunda deneyiminiz yoksa, [Thinking in Java](https://chenweixiang.github.io/docs/Thinking_in_Java_4th_Edition.pdf) kitabına göz atabilirsiniz

"How intro", diğer "how" belgelerini, teknik giriş belgesini ve ilgili dokümanları inceleyin:

- Tanıtım: [I2P'ye Giriş](/docs/overview/intro/)
- Dokümantasyon merkezi: [Dokümantasyon](/docs/)
- Teknik tanıtım: [Teknik Tanıtım](/docs/overview/tech-intro/)

Bunlar size I2P'nin nasıl yapılandırıldığına ve farklı işlevlerinin neler olduğuna dair iyi bir genel bakış sunacaktır.

## I2P Kodunu Edinme

I2P router veya gömülü uygulamalar üzerinde geliştirme yapmak için kaynak kodunu edinmeniz gerekir.

### Mevcut yöntemimiz: Git

I2P'nin resmi Git hizmetleri vardır ve kendi GitLab sunucumuzdan Git üzerinden katkı kabul eder:

- I2P İçinde: <http://git.idk.i2p>
- I2P Dışında: <https://i2pgit.org>

Ana depoyu klonlayın:

```
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
```
GitHub'da salt okunur bir yansı da mevcuttur:

- GitHub yansıması: [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p)

```
git clone https://github.com/i2p/i2p.i2p.git
```
## I2P Kurulumu

Kodu derlemek için Sun/Oracle Java Development Kit 6 veya üzeri, ya da eşdeğer bir JDK (Sun/Oracle JDK 6 şiddetle önerilir) ve Apache Ant sürüm 1.7.0 veya üzeri gereklidir. Ana I2P kodu üzerinde çalışıyorsanız, `i2p.i2p` dizinine girin ve derleme seçeneklerini görmek için `ant` komutunu çalıştırın.

Console çevirilerini oluşturmak veya üzerinde çalışmak için GNU gettext paketinden `xgettext`, `msgfmt` ve `msgmerge` araçlarına ihtiyacınız var.

Yeni uygulamalar üzerinde geliştirme yapmak için [uygulama geliştirme kılavuzuna](/docs/develop/applications/) bakın.

## Geliştirme Fikirleri

Fikirler için proje TODO listesine veya GitLab'daki sorun listesine bakın:

- GitLab sorunları: [i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)

## Sonuçları Erişilebilir Hale Getirme

Commit yetkisi gereksinimleri için lisanslar sayfasının altına bakın. `i2p.i2p`'ye kod koymak için bunlara ihtiyacınız var (web sitesi için gerekli değil!).

- [Lisanslar sayfası](/docs/develop/licenses#commit)

## Bizi Tanıyın!

Geliştiriciler IRC'de takılırlar. Onlara çeşitli ağlar ve I2P dahili ağları üzerinden ulaşılabilir. Bakılması gereken olağan yer `#i2p-dev`'dir. Kanala katılın ve merhaba deyin! Ayrıca düzenli geliştiriciler için ek [yönergelerimiz](/docs/develop/dev-guidelines/) de bulunmaktadır.

## Çeviriler

Web sitesi ve router konsolu çeviricileri: Sonraki adımlar için [Yeni Çevirmenlerin Rehberi](/docs/develop/new-translators/)'ne bakın.

## Araçlar

I2P, çoğunlukla açık kaynak araç setleri kullanılarak geliştirilen açık kaynak bir yazılımdır. I2P projesi yakın zamanda YourKit Java Profiler için bir lisans edindi. Açık kaynak projeler, YourKit'in proje web sitesinde referans gösterilmesi koşuluyla ücretsiz lisans almaya hak kazanır. I2P kod tabanında profilleme yapmak istiyorsanız lütfen bizimle iletişime geçin.

YourKit, açık kaynak projelerini tam özellikli profil oluşturucularıyla nazikçe desteklemektedir. YourKit, LLC, Java ve .NET uygulamaları için profil oluşturmaya yönelik yenilikçi ve akıllı araçların yaratıcısıdır. YourKit'in önde gelen yazılım ürünlerine bir göz atın:

- [YourKit Java Profiler](http://www.yourkit.com/java/profiler/index.jsp)
- [YourKit .NET Profiler](http://www.yourkit.com/.net/profiler/index.jsp)
