---
title: "Jpackage ve I2P-Zero kullanarak I2P’nin benimsenmesini ve Onboarding’i (ilk kullanım sürecini) iyileştirme"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "I2P'yi kurmanın ve uygulamanıza entegre etmenin çok yönlü ve yeni ortaya çıkan yöntemleri"
categories: ["general"]
API_Translate: doğru
---

For the majority of I2P's existence, it's been an application that runs with the help of a Java Virtual Machine that is already installed on the platform. This has always been the normal way to distribute Java applications, but it leads to a complicated installation procedure for many people. To make things even more complicated, the "right answer" to making I2P easy to install on any given platform might not be the same as any other platform. For example, I2P is quite simple to install with standard tools on Debian and Ubuntu based operating systems, because we can simply list the required Java components as "Required" by our package, however on Windows or OSX, there is no such system allowing us to make sure that a compatible Java is installed.

En bariz çözüm Java kurulumunu kendimiz yönetmek olurdu, ancak bu, I2P'nin kapsamı dışında, eskiden başlı başına bir sorundu. Ancak Java'nın son sürümlerinde, birçok Java yazılımı için bu sorunu çözme potansiyeline sahip yeni bir dizi seçenek ortaya çıktı. Bu heyecan verici aracın adı **"Jpackage."**

## I2P-Zero ve Bağımlılık Gerektirmeyen I2P Kurulumu

Bağımlılıksız bir I2P paketi oluşturma yönündeki ilk çok başarılı girişim, Monero projesi tarafından aslen Monero kripto para birimiyle kullanılmak üzere oluşturulan I2P-Zero idi. Bu proje, bir I2P uygulamasıyla kolayca paketlenebilecek genel amaçlı bir I2P router oluşturmadaki başarısı nedeniyle bizi çok heyecanlandırdı. Özellikle Reddit’te, pek çok kişi bir I2P-Zero router kurulumunun basitliğini tercih ettiklerini ifade ediyor.

Bu, modern Java araçlarını kullanarak kurulumu kolay, bağımlılıksız bir I2P paketinin mümkün olduğunu bize gerçekten kanıtladı, ancak I2P-Zero'nun kullanım senaryosu bizimkinden biraz farklıydı. Bu, "8051" numaralı kontrol portunu kullanarak kolayca kontrol edebilecekleri bir I2P router’a ihtiyaç duyan gömülü uygulamalar için en uygunudur. Bir sonraki adımımız, teknolojiyi genel amaçlı I2P uygulamasına uyarlamak olacaktı.

## OSX'teki Uygulama Güvenliği Değişiklikleri I2P IzPack Installer'ı etkiliyor

Sorun, Mac OSX’in son sürümlerinde daha da acil hâle geldi; .jar formatında gelen "Classic" yükleyicisini kullanmak artık eskisi kadar kolay değil. Bunun nedeni, uygulamanın Apple yetkilileri tarafından "Notarized" (Apple’ın Notary Service onayı) olmaması ve bir güvenlik riski olarak görülmesidir. **Ancak**, Jpackage, Apple yetkilileri tarafından "Notarized" olabilen bir .dmg dosyası üretebilir ve bu da sorunumuzu pratik biçimde çözer.

Zlatinb tarafından oluşturulan yeni I2P .dmg yükleyicisi, kullanıcıların artık Java'yı kendilerinin kurmasını gerektirmemesi ve standart OSX kurulum araçlarını belirlenen şekilde kullanması sayesinde, I2P'nin OSX'e kurulmasını hiç olmadığı kadar kolaylaştırıyor. Yeni .dmg yükleyicisi, Mac OSX üzerinde I2P'yi kurmayı şimdiye kadarki en kolay hale getiriyor.

[dmg](https://geti2p.net/en/download/mac) dosyasını indirin

## Geleceğin I2P'si kolay kurulur

Kullanıcılardan en sık duyduğum şeylerden biri, I2P'nin benimsenmesini istiyorsa insanlar için kullanımı kolay olması gerektiğidir. Pek çok tanıdık Reddit kullanıcısının sözleriyle söylersek, "Tor Browser benzeri" bir kullanıcı deneyimi istiyorlar. Kurulum, karmaşık ve hataya açık "kurulum sonrası" adımlar gerektirmemelidir. Pek çok yeni kullanıcı, tarayıcı yapılandırmalarıyla kapsamlı ve eksiksiz bir şekilde uğraşmaya hazır değil. Bu sorunu çözmek için, Firefox'u I2P için otomatik olarak "hemen çalışır" hale getiren I2P Profile Bundle'ı oluşturduk. Geliştikçe güvenlik özellikleri eklendi ve I2P'nin kendisiyle entegrasyonu iyileştirildi. En son sürümünde, **ayrıca** Jpackage destekli, eksiksiz bir I2P Router'ı da paketler. I2P Firefox Profile artık Windows için tam teşekküllü bir I2P dağıtımıdır; geriye kalan tek bağımlılık Firefox'un kendisidir. Bu, Windows'ta I2P kullanıcıları için eşi benzeri görülmemiş bir kullanım kolaylığı sağlayacaktır.

[Yükleyiciyi](https://geti2p.net/en/download#windows) edinin
