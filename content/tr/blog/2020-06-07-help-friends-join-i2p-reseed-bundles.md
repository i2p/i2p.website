---
title: "Reseed paketlerini paylaşarak arkadaşlarınızın I2P'ye katılmasına yardımcı olun"
date: 2020-06-07
author: "idk"
description: "Reseed paketleri oluşturun, değiş tokuş edin ve kullanın"
categories: ["reseed"]
---

Yeni I2P routerların çoğu, bir reseed hizmetinin yardımıyla bootstrap işlemiyle ağa katılır. Ancak, I2P ağının geri kalanında merkeziyetsiz ve engellenemez bağlantılara verilen önem göz önüne alındığında, reseed hizmetleri merkezileştirilmiştir ve nispeten engellenmesi kolaydır. Yeni bir I2P router bootstrap yapamazsa, mevcut bir I2P router kullanarak çalışan bir "Reseed bundle" oluşturmak ve bir reseed hizmetine ihtiyaç duymadan bootstrap etmek mümkün olabilir.

Çalışır durumda bir I2P bağlantısına sahip bir kullanıcı, bir reseed dosyası (ağ başlatma amacıyla kullanılan dosya) oluşturarak ve bunu ona gizli veya engellenmemiş bir kanal üzerinden ileterek, engellenmiş bir router'ın ağa katılmasına yardımcı olabilir. Aslında, birçok durumda, halihazırda bağlı olan bir I2P router reseed engellemesinden hiç etkilenmez, bu nedenle **etrafta çalışan I2P router'ların bulunması, mevcut I2P router'ların yeni I2P router'lara gizli bir bootstrapping (başlatma) yöntemi sağlayarak yardımcı olabileceği anlamına gelir**.

## Reseed Paketi Oluşturma

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Dosyadan Reseed (yeniden tohumlama) gerçekleştirme

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
