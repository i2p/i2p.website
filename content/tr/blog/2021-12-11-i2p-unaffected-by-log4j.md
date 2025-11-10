---
title: "I2P, log4j güvenlik açığından etkilenmez"
date: 2021-12-11
author: "idk, zzz"
description: "I2P log4j kullanmaz, dolayısıyla CVE-2021-44228'den etkilenmez."
categories: ["security"]
API_Translate: doğru
---

I2P, dün yayımlanan log4j sıfır gün (0-day) güvenlik açığı CVE-2021-44228'den etkilenmemektedir. I2P günlükleme için log4j kullanmaz; ancak log4j kullanımına ilişkin bağımlılıklarımızı, özellikle de jetty'yi gözden geçirmemiz gerekiyordu. Bu inceleme herhangi bir güvenlik açığı ortaya çıkarmamıştır.

Ayrıca tüm eklentilerimizi kontrol etmek de önemliydi. Eklentiler, log4j dahil kendi günlükleme sistemlerini beraberinde getirebilir. Çoğu eklentinin de log4j kullanmadığını, kullananların ise log4j'nin güvenlik açığı içeren bir sürümünü kullanmadığını tespit ettik.

Güvenlik açığı bulunan herhangi bir bağımlılık, eklenti veya uygulama bulamadık.

log4j'yi kullanan eklentiler için jetty ile birlikte bir log4j.properties dosyası paketliyoruz. Bu dosya yalnızca dahili olarak log4j ile loglama yapan eklentileri etkiler. Önerilen önlemi log4j.properties dosyasına ekledik. log4j'yi etkinleştiren eklentiler, güvenlik açığı bulunan özellik devre dışı bırakılmış olarak çalışacak. Herhangi bir yerde log4j 2.x kullanımına rastlamadığımız için, şu anda acil bir sürüm yayınlamayı planlamıyoruz.
