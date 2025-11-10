---
title: "I2P Jpackages ilk güncellemelerini aldı"
date: 2021-11-02
author: "idk"
description: "Yeni, kurulumu daha kolay paketler yeni bir dönüm noktasına ulaştı"
categories: ["general"]
API_Translate: doğru
---

Birkaç ay önce, daha fazla kişi için I2P’nin kurulumunu ve yapılandırmasını kolaylaştırarak yeni kişilerin I2P ağına katılmasına yardımcı olacağını umduğumuz yeni paketler yayımladık. Harici bir JVM’den Jpackage’e geçerek kurulum sürecindeki onlarca adımı kaldırdık, hedef işletim sistemleri için standart paketler oluşturduk ve kullanıcıyı güvende tutmak için işletim sistemi tarafından tanınacak şekilde imzaladık. O zamandan beri, jpackage routers yeni bir dönüm noktasına ulaştı; ilk artımlı güncellemelerini almak üzereler. Bu güncellemeler, JDK 16 jpackage’i güncellenmiş bir JDK 17 jpackage ile değiştirecek ve yayından sonra yakaladığımız bazı küçük hatalar için düzeltmeler sağlayacak.

## Mac OS ve Windows için ortak güncellemeler

Tüm jpackaged I2P kurulum programları aşağıdaki güncellemeleri alır:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Lütfen mümkün olan en kısa sürede güncelleyin.

## I2P Windows Jpackage Güncellemeleri

Yalnızca Windows paketleri aşağıdaki güncellemeleri alır:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Değişikliklerin tam listesi için i2p.firefox içindeki changelog.txt dosyasına bakın.

## I2P Mac OS Jpackage Güncellemeleri

Yalnızca Mac OS paketleri aşağıdaki güncellemeleri alır:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Geliştirmenin özeti için i2p-jpackage-mac içindeki check-in kayıtlarına bakın.
