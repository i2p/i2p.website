---
title: "I2P Hakkında"
description: "Görünmez İnternet Projesi - anonim iletişim için tasarlanmış, tamamen şifrelenmiş, eşler arası bir katman ağı hakkında bilgi edinin."
tagline: "Görünmez İnternet Projesi"
type: "about"
layout: "about"
established: "2002"
---

Görünmez İnternet Projesi 2002 yılında başladı. Projenin vizyonu I2P Ağı'nın "en yüksek seviyede tam anonimlik, gizlilik ve güvenlik sağlamasıydı. Merkezi olmayan ve eşler arası internet, ISP'nizin trafiğinizi kontrol etme endişesini ortadan kaldırır. Bu, insanların kesintisiz aktiviteler yapmasına ve güvenlik ve hatta internete bakışımızı değiştirmesine olanak tanıyacak, genel anahtar şifrelemesi, IP steganografisi ve mesaj doğrulaması kullanarak. Olması gereken internet yakında olacak."

O zamandan beri I2P, çeşitli uygulamalara yüksek düzeyde gizlilik, güvenlik ve kimlik doğrulama sağlama yeteneğine sahip tam bir ağ protokolleri suiti belirlemek ve uygulamak üzere evrim geçirmiştir.

## I2P Ağı

I2P ağı, tamamen şifrelenmiş bir eşler arası katman ağıdır. Bir gözlemci bir mesajın içeriğini, kaynağını veya varış noktasını göremez. Hiç kimse trafiğin nereden geldiğini, nereye gittiğini veya içeriğinin ne olduğunu göremez. Ayrıca I2P taşımaları, sansürcüler tarafından tanıma ve engellemeye karşı direnç sunar. Ağ, trafiği yönlendirmek için eşlere güvendiği için konuma dayalı engelleme, ağın büyümesiyle birlikte bir zorluğa dönüşür. Ağdaki her yönlendirici, ağı anonim hale getirmeye katkıda bulunur. Güvenli olmayacak durumlar dışında, herkes ağ trafiğini göndermeye ve almaya katılır.

## I2P Ağına Nasıl Bağlanılır?

Ana yazılım (Java) ağı tanıtan ve buna bağlantıyı sürdüren bir yönlendirici içerir. Ayrıca deneyiminizi ve iş akışınızı kişiselleştirmek için uygulamalar ve yapılandırma seçenekleri sağlar. [belgelerimizden](/docs/) daha fazla bilgi edinin.

## I2P Ağında Neler Yapabilirim?

Ağ, hizmetler, uygulamalar ve ağ yönetimi için bir uygulama katmanı sağlar. Ağ ayrıca İnternet'ten (Açık ağ) içeriklerin kendin barındırılması ve yansıtılmasına izin veren benzersiz bir DNS'ye sahiptir. I2P ağının işlevi, internetin yaptığı gibi çalışır. Java yazılımı, bir BitTorrent istemcisi, e-posta ve statik bir web sitesi şablonu içerir. Diğer uygulamalar, yönlendirici konsolunuza kolayca eklenebilir.

## Ağın Genel Görünümü

I2P, kurduğu tüneller ve taşıdığı iletişimler için çeşitli özellikler elde etmek için kriptografi kullanır. I2P tünelleri, [NTCP2](/docs/specs/ntcp2/) ve [SSU2](/docs/specs/ssu2/) taşımalarını kullanarak üzerinden taşınan trafiği gizler. Bağlantılar, yönlendiriciden yönlendiriciye ve istemciden istemciye (uçtan uca) şifrelenmiştir. Tüm bağlantılar için ileriye dönük gizlilik sağlanır. I2P kriptografik olarak adreslendiği için, I2P ağ adresleri kendinden doğrulamalı olup, yalnızca onları oluşturan kullanıcıya aittir.

Ağ, eşler ("yönlendiriciler") ve tek yönlü gelen ve giden sanal tünellerden oluşur. Yönlendiriciler, mevcut taşıma mekanizmaları (TCP, UDP) üzerine kurulmuş protokoller kullanarak birbirleriyle mesajlar iletir. İstemci uygulamalarının mesaj gönderip alabilmesine olanak tanıyan kendi kriptografik kimlikleri ("Hedef") vardır. Bu istemciler, herhangi bir yönlendiriciye bağlanabilir ve ağ üzerinden mesaj göndermek ve almak için kullanılacak tünellerin geçici tahsisatını ("kira") yetkilendirebilirler. I2P, yönlendirme ve iletişim bilgilerini güvenli bir şekilde dağıtmak için Kademlia DHT'nin bir modifikasyonunu kullanarak kendi dahili ağ veritabanına sahiptir.

## Merkeziyetsizlik ve I2P Ağı Hakkında

I2P ağı neredeyse tamamen merkezsizdir, bunun tek istisnası "Reseed Sunucuları" olarak adlandırılanlardır. Bu, DHT (Dağıtılmış Hash Tablosu) bootstrap problemini ele almak içindir. Temelde, ağ katılımcısı olmayanların bulup başlamak için kullanabileceği en az bir kalıcı bootstrap düğümü işletmeden çıkmanın iyi ve güvenilir bir yolu yoktur. Ağa bağlandıktan sonra, bir yönlendirici yalnızca "keşif" tünelleri oluşturarak eşleri keşfeder, ancak başlangıç bağlantısını yapmak için bir reseed sunucu, yeni bir yönlendiriciyi ağa bağlayıp başlatmak için gereklidir. Reseed sunucuları, yeni bir yönlendiricinin kendilerinden bir reseed indirdiğini gözlemleyebilir, ancak I2P ağındaki trafik hakkında başka hiçbir şey gözlemleyemezler.

## Karşılaştırmalar

Anonim iletişim üzerinde çalışan başka birçok uygulama ve proje mevcuttur ve I2P, bunların çoğunun çabalarından ilham almıştır. Bu, anonimlik kaynaklarının kapsamlı bir listesi değildir - hem [freehaven'in Anonimlik Bibliyografisi](http://freehaven.net/anonbib/topic.html) hem de [GNUnet'in ilgili projeleri](https://www.gnunet.org/links/) bu amaca iyi hizmet eder. Bununla birlikte, birkaç sistem daha fazla karşılaştırma için öne çıkmaktadır. I2P'nin diğer anonim ağlarla nasıl karşılaştırıldığını daha fazla öğrenmek için [detaylı karşılaştırma belgelerimize](/docs/overview/comparison/) bakın.
