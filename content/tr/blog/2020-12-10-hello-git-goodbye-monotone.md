---
title: "Merhaba Git, Elveda Monotone"
date: 2020-12-10
author: "idk"
description: "Merhaba git, elveda mtn"
categories: ["Status"]
---

## Merhaba Git, Elveda Monotone

### The I2P Git Migration is nearly concluded

On yılı aşkın bir süredir I2P, sürüm kontrolü gereksinimlerini karşılamak için köklü Monotone hizmetine dayanıyordu, ancak son birkaç yılda dünyanın büyük bölümü artık evrensel hâle gelen Git sürüm kontrol sistemine geçti. Aynı süre zarfında I2P Ağı daha hızlı ve daha güvenilir hâle geldi ve Git'in kaldığı yerden devam edilememe sorununa yönelik erişilebilir geçici çözümler geliştirildi.

Bugün I2P için önemli bir dönüm noktasını işaret ediyor; çünkü eski mtn i2p.i2p dalını kapattık ve çekirdek Java I2P kütüphanelerinin geliştirilmesini resmen Monotone'dan Git'e taşıdık.

Geçmişte mtn kullanmamız sorgulanmış ve her zaman popüler bir tercih olmamış olsa da, Monotone’u kullanan belki de son proje olarak bu vesileyle, nerede olurlarsa olsunlar, Monotone geliştiricilerine — mevcut ve eski — geliştirdikleri yazılım için teşekkür etmek istiyorum.

## GPG Signing

I2P Projesi depolarına yapılan gönderimler, Merge Request (birleştirme isteği) ve Pull Request (çekme isteği) işlemleri de dahil olmak üzere, git commit’leriniz için GPG imzalamayı yapılandırmanızı gerektirir. Lütfen i2p.i2p’i fork etmeden ve herhangi bir şeyi depoya göndermeden önce git istemcinizi GPG imzalama için yapılandırın.

## GPG İmzalama

Resmi depo, https://i2pgit.org/i2p-hackers/i2p.i2p ve https://git.idk.i2p/i2p-hackers/i2p.i2p adreslerinde barındırılmaktadır, ancak Github'da https://github.com/i2p/i2p.i2p adresinde bir "Mirror" (ayna) da mevcuttur.

Artık git’e geçtiğimize göre, depoları kendi barındırdığımız Gitlab örneğimizden Github’a ve tekrar geri eşitleyebiliriz. Bu, Gitlab üzerinde bir merge request (birleştirme isteği) oluşturup gönderebileceğimiz ve birleştirildiğinde sonucunun Github ile eşitleneceği; ayrıca Github üzerindeki bir Pull Request (çekme isteği) birleştirildiğinde bunun Gitlab’da görüneceği anlamına gelir.

Bu, tercihinize bağlı olarak kodu bize Gitlab örneğimiz üzerinden veya Github üzerinden gönderebileceğiniz anlamına gelir; ancak I2P geliştiricilerinin daha fazlası Github’a göre Gitlab’ı düzenli olarak izlemektedir. Gitlab’a gönderilen MR’ların, Github’a gönderilen PR’lara göre daha erken birleştirilme olasılığı daha yüksektir.

## Resmi Depolar ve Gitlab/Github Senkronizasyonu

Git'e geçişe yardımcı olan herkese, özellikle de zzz, eche|on, nextloop ve site aynası işletmecilerimize tebrikler ve teşekkürler! Aramızdan bazıları Monotone'u özleyecek olsa da, Monotone, I2P geliştirmesine yeni başlayanlar ve mevcut katılımcılar için bir engel haline geldi ve dağıtık projelerini yönetmek için Git kullanan geliştiricilerin dünyasına katılmaktan heyecan duyuyoruz.
