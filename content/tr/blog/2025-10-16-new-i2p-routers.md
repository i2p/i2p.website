---
title: "Yeni I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Rust'taki emissary ve Go'daki go-i2p'nin de aralarında bulunduğu birden fazla yeni I2P router gerçekleme ortaya çıkıyor; bu da gömülü kullanım ve ağ çeşitliliği için yeni olanaklar sunuyor."
API_Translate: doğru
---

I2P geliştirme çalışmaları için heyecan verici bir dönem; topluluğumuz büyüyor ve artık birden fazla yeni, tam işlevli I2P router prototipi ortaya çıkıyor! Bu gelişmeden ve bu haberi sizinle paylaşmaktan büyük heyecan duyuyoruz.

## Bu, ağa nasıl yardımcı olur?

I2P router'ları yazmak, spesifikasyon belgelerimizin yeni I2P router'ları üretmek için kullanılabileceğini kanıtlamamıza yardımcı olur, kodu yeni analiz araçlarına açar ve genel olarak ağın güvenliğini ve birlikte çalışabilirliğini iyileştirir. Birden fazla I2P router'ının olması, potansiyel hataların tek tip olmaması anlamına gelir; bir router'a yönelik bir saldırı başka bir router'da çalışmayabilir, böylece bir monokültür sorunundan kaçınılır. Ancak uzun vadede, belki de en heyecan verici olasılık embedding (gömme)dir.

## Gömme nedir?

I2P bağlamında, embedding (gömme), arka planda çalışan bağımsız bir router gerektirmeden, bir I2P router'ını doğrudan başka bir uygulamanın içine dahil etme yoludur. Bu, I2P'yi kullanımı daha kolay hale getirebileceğimiz bir yöntemdir; yazılımı daha erişilebilir kılarak ağın büyümesini kolaylaştırır. Java ve C++ her ikisi de kendi ekosistemleri dışında kullanılmalarının zor olması sorunundan muzdariptir; C++ tarafında kırılgan, elle yazılmış C bindings (C bağlamaları) gerekirken, Java tarafında ise JVM dışı bir uygulamadan bir JVM uygulamasıyla iletişim kurmanın zahmeti vardır.

Birçok açıdan bu durum oldukça normal olsa da, I2P'yi daha erişilebilir kılmak için iyileştirilebileceğine inanıyorum. Diğer diller bu sorunlara daha zarif çözümler sunuyor. Elbette, Java ve C++ router'lar (yönlendiriciler) için mevcut yönergeleri her zaman göz önünde bulundurmalı ve kullanmalıyız.

## elçi karanlıktan belirir

Ekibimizden tamamen bağımsız olarak, altonen adlı bir geliştirici, emissary adlı Rust ile yazılmış bir I2P uygulaması geliştirdi. Henüz oldukça yeni ve Rust bize yabancı olmasına rağmen, bu ilgi çekici proje büyük umut vadediyor. emissary adlı projeyi hayata geçirdiği için altonen'i tebrik ederiz; oldukça etkilendik.

### Why Rust?

Rust kullanmanın başlıca nedeni, Java veya Go kullanmanın nedeniyle temelde aynıdır. Rust, bellek yönetimine sahip ve büyük, son derece hevesli bir topluluğu olan derlenen bir programlama dilidir. Rust ayrıca C programlama diline yönelik binding'ler (bağlamalar) üretmek için gelişmiş özellikler sunar; bu binding'ler, diğer dillere kıyasla bakımı daha kolay olabilir ve yine de Rust'ın güçlü bellek güvenliği özelliklerini devralır.

### Do you want to get involved with emissary?

emissary, Github'da altonen tarafından geliştirilmektedir. Depoyu şu adreste bulabilirsiniz: [altonen/emissary](https://github.com/altonen/emissary). Rust ayrıca, popüler Rust ağ kitaplıklarıyla uyumlu kapsamlı SAMv3 istemci kitaplıklarından da yoksundur; bir SAMv3 kitaplığı yazmak harika bir başlangıç noktasıdır.

## go-i2p is getting closer to completion

Yaklaşık 3 yıldır go-i2p üzerinde çalışıyorum; amacım, emekleme aşamasındaki bir kütüphaneyi, bellek açısından güvenli bir başka dil olan Go ile tamamen yazılmış, tam teşekküllü bir I2P router'a dönüştürmek. Son 6 ay kadar bir sürede, performans, güvenilirlik ve bakım yapılabilirliği artırmak için köklü biçimde yeniden yapılandırıldı.

### Why Go?

Rust ve Go pek çok ortak avantaja sahip olsa da, Go birçok bakımdan öğrenmesi çok daha basittir. Yıllardır, Go programlama dilinde I2P'yi kullanmak için mükemmel kütüphaneler ve uygulamalar mevcut; bunlara SAMv3.3 kütüphanelerinin en eksiksiz gerçekleştirimleri de dahildir. Ancak otomatik olarak yönetebileceğimiz bir I2P router olmadan (örneğin gömülü bir router), bu durum kullanıcılar için hâlâ bir engel teşkil eder. go-i2p'nin amacı bu boşluğu kapatmak ve Go ile çalışan I2P uygulama geliştiricileri için tüm pürüzleri ortadan kaldırmaktır.

### Neden Rust?

go-i2p şu anda ağırlıklı olarak eyedeekay tarafından Github üzerinde geliştirilmektedir ve topluluktan katkılara [go-i2p](https://github.com/go-i2p/) üzerinden açıktır. Bu ad alanı içinde aşağıdakiler gibi birçok proje bulunmaktadır:

#### Router Libraries

Bu kütüphaneleri, I2P router kütüphanelerimizi oluşturmak için geliştirdik. İncelemeyi kolaylaştırmak ve deneysel, özelleştirilmiş I2P router’lar inşa etmek isteyen diğer kişiler için yararlı olmalarını sağlamak amacıyla, birden çok, odaklı depo (repository) halinde dağıttık.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

I2P'yi bir XBox'ta çalıştırmak istiyorsanız, [C# ile bir I2P router](https://github.com/PeterZander/i2p-cs) yazmaya yönelik, şu anda atıl durumda bir proje var. Aslında kulağa oldukça hoş geliyor. Bu da tercihiniz değilse, altonen'in yaptığı gibi tamamen yeni bir tane geliştirebilirsiniz.

### emissary'e dahil olmak ister misiniz?

İstediğiniz herhangi bir nedenle bir I2P router yazabilirsiniz; bu özgür bir ağdır, ancak nedenini bilmek size yardımcı olacaktır. Güçlendirmek istediğiniz bir topluluk, I2P için uygun olduğunu düşündüğünüz bir araç ya da denemek istediğiniz bir strateji var mı? Hedefinizi netleştirerek nereden başlamanız gerektiğini ve "bitmiş" durumun nasıl görüneceğini belirleyin.

### Decide what language you want to do it in and why

Bir dili seçmeniz için bazı nedenler şunlardır:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Ancak o dilleri seçmemeniz için bazı nedenler şunlardır:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Yüzlerce programlama dili vardır ve hepsinde bakımı yapılan I2P kütüphaneleri ve routers görmekten memnuniyet duyarız. Ödünleşimlerinizi akıllıca seçin ve başlayın.

## go-i2p tamamlanmaya yaklaşıyor

İster Rust, Go, Java, C++ ya da başka bir dilde çalışmak isteyin, Irc2P üzerindeki #i2p-dev kanalından bizimle iletişime geçin. Oradan başlayın; sizi router (yönlendirici) odaklı kanallara dahil edelim. Ayrıca ramble.i2p üzerinde f/i2p, reddit üzerinde r/i2p ve GitHub ile git.idk.i2p üzerinde de yer alıyoruz. Yakında sizden haber almayı dört gözle bekliyoruz.
