---
title: "2006-01-17 için I2P Durum Notları"
date: 2006-01-17
author: "jr"
description: "0.6.1.9 ile ağ durumu, tunnel oluşturma şifreleme iyileştirmeleri ve Syndie blog arayüzü güncellemeleri"
categories: ["status"]
---

Selam millet, yine salı

* Index

1) Ağ durumu ve 0.6.1.9 2) Tunnel oluşturma kriptografisi 3) Syndie blogları 4) ???

* 1) Net status and 0.6.1.9

0.6.1.9 yayımlandı ve ağın %70’i yükseltildi; dahil edilen hata düzeltmelerinin çoğu beklendiği gibi çalışıyor ve raporlar, yeni hız profillemesinin bazı iyi eşleri seçtiğini belirtiyor. Hızlı eşlerde %50-70 CPU kullanımıyla 300KBps’i aşan sürdürülebilir aktarım hızları duyduğum oldu; diğer router'lar 100-150KBps aralığında, 1-5KBps’i zorlayanlara kadar iniyor. Yine de kayda değer düzeyde router identity churn (sık değişim) var; görünen o ki, bunu azaltacağını düşündüğüm hata düzeltmesi işe yaramamış (ya da churn meşru).

* 2) Tunnel creation crypto

Sonbaharda, tunnel'lerimizi nasıl kurduğumuz ve Tor tarzı teleskopik tunnel oluşturma ile I2P tarzı keşif amaçlı tunnel oluşturma arasındaki ödünleşimler [1] hakkında çok fazla tartışma vardı. Bu süreçte, Tor tarzı teleskopik oluşturmanın [3] sorunlarını ortadan kaldıran, I2P'nin tek yönlü avantajlarını koruyan ve gereksiz başarısızlıkları azaltan bir kombinasyon [2] geliştirdik. O sırada birçok başka şey de olduğundan, yeni kombinasyonun uygulanması ertelendi, ancak artık 0.6.2 sürümüne yaklaşırken, bu sırada zaten tunnel oluşturma kodunu elden geçirmemiz gerekiyor, bunu netleştirmenin zamanı geldi.

Geçen gün yeni tunnel kriptografisi için bir taslak şartname hazırlayıp syndie bloguma gönderdim ve bunu gerçekten uygularken ortaya çıkan birkaç küçük değişikliğin ardından, CVS’de [4] bir şartname oluşturduk. Bunu uygulayan temel bir kod da CVS’de [5] mevcut, ancak henüz gerçek tunnel oluşturma için entegre edilmiş değil. Canı sıkılan varsa, şartname hakkında geri bildirim almaktan memnun olurum. Bu arada, yeni tunnel oluşturma kodu üzerinde çalışmaya devam edeceğim.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html ve     önyükleme saldırılarıyla ilgili başlıklara bakın [2] http://dev.i2p.net/pipermail/i2p/2005-October/001064.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001057.html [4] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD [5] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/java/src/net/                        i2p/router/tunnel/BuildMessageTest.java

* 3) Syndie blogs

Daha önce belirtildiği gibi, bu yeni 0.6.1.9 sürümü, Syndie blog arayüzünde cervantes’in yeni stil düzeni ve her kullanıcının blog bağlantılarını ve logosunu seçebilmesi (örn. [6]) dahil olmak üzere köklü yenilemeler içeriyor. Profil sayfanızdaki "configure your blog" bağlantısına tıklayarak soldaki bu bağlantıları yönetebilirsiniz; bu sizi http://localhost:7657/syndie/configblog.jsp adresine götürür. Orada değişikliklerinizi yaptıktan sonra, bir sonraki sefer bir gönderiyi bir arşive yüklediğinizde, bu bilgiler başkalarının erişimine sunulacaktır.

[6] http://syndiemedia.i2p.net/     blog.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=

* 4) ???

Toplantıya zaten 20 dakika geç kaldığıma göre, kısa kessem iyi olacak. Birkaç başka şeyin daha olduğunu biliyorum ama bunları burada saymak yerine, tartışmak isteyen geliştiriciler toplantıya uğrayıp gündeme getirsinler. Neyse, şimdilik bu kadar, #i2p üzerinde görüşürüz!

=jr
