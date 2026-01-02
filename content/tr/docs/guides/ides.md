---
title: "I2P ile IDE Kullanımı"
description: "Eclipse ve NetBeans'i Gradle ve birlikte gelen proje dosyaları ile I2P geliştirme için yapılandırma"
slug: "ides"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: belgeler
reviewStatus: "needs-review"
---

<p> Ana I2P geliştirme dalı (<code>i2p.i2p</code>), geliştiricilerin Java geliştirme için yaygın olarak kullanılan iki IDE'yi (Eclipse ve NetBeans) kolayca kurmalarını sağlayacak şekilde yapılandırılmıştır. </p>

<h2>Eclipse</h2>

<p> Ana I2P geliştirme dalları (<code>i2p.i2p</code> ve ondan türetilen dallar), dalın Eclipse'te kolayca kurulmasını sağlamak için <code>build.gradle</code> dosyası içerir. </p>

<ol> <li> Güncel bir Eclipse sürümüne sahip olduğunuzdan emin olun. 2017'den daha yeni herhangi bir sürüm yeterli olacaktır. </li> <li> I2P dalını bir dizine (örneğin <code>$HOME/dev/i2p.i2p</code>) checkout edin. </li> <li> "File → Import..." seçeneğini ve ardından "Gradle" altında "Existing Gradle Project" seçeneğini seçin. </li> <li> "Project root directory:" için I2P dalının checkout edildiği dizini seçin. </li> <li> "Import Options" diyalogunda "Gradle Wrapper" seçeneğini işaretleyin ve Continue'ya basın. </li> <li> "Import Preview" diyalogunda proje yapısını inceleyebilirsiniz. "i2p.i2p" altında birden fazla proje görünmelidir. "Finish" düğmesine basın. </li> <li> Tamamlandı! Çalışma alanınız artık I2P dalındaki tüm projeleri içermeli ve derleme bağımlılıkları doğru şekilde ayarlanmış olmalıdır. </li> </ol>

<h2>NetBeans</h2>

<p> Ana I2P geliştirme dalları (<code>i2p.i2p</code> ve ondan türetilen dallar) NetBeans proje dosyalarını içerir. </p>

<!-- İçeriği minimal ve orijinaline yakın tutun; daha sonra güncellenecektir. -->
