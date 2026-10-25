---
title: "Eski Tunnel Uygulaması"
description: "0.6.1.10 sürümünden önce I2P'nin orijinal tunnel uygulamasının tarihsel belgelendirmesi"
slug: "old-tunnel-implementation"
aliases:
  - "/tr/docs/historical/tunnel-alt"
  - "/tr/docs/historical/tunnel-alt/"
  - "/tr/tunnel"
  - "/tr/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Not: Eskimiş - KULLANILMIYOR! 0.6.1.10'da değiştirildi - aktif spesifikasyon için [mevcut uygulama](/docs/specs/tunnel-implementation) bölümüne bakın.**

## 1) Tunnel genel bakış {#tunnel.overview}

I2P içinde, mesajlar tek yönlü olarak sanal bir peer tüneli boyunca iletilir ve mesajı bir sonraki hop'a geçirmek için mevcut olan her türlü yöntem kullanılır. Mesajlar tunnel'ın gateway'inde gelir, yol için paketlenir ve tunnel'daki bir sonraki hop'a iletilir; bu hop mesajı işler, geçerliliğini doğrular ve tunnel endpoint'ine ulaşana kadar bir sonraki hop'a gönderir. Bu endpoint, gateway tarafından paketlenmiş mesajları alır ve talimat verildiği şekilde iletir - ya başka bir router'a, başka bir router üzerindeki başka bir tunnel'a ya da yerel olarak.

Tunnel'lar aynı şekilde çalışır, ancak iki farklı gruba ayrılabilir - gelen tunnel'lar ve giden tunnel'lar. Gelen tunnel'larda, mesajları tunnel yaratıcısına doğru ileten güvenilmez bir gateway bulunur ve tunnel yaratıcısı tunnel endpoint'i olarak görev yapar. Giden tunnel'larda ise, tunnel yaratıcısı gateway olarak görev yapar ve mesajları uzak endpoint'e iletir.

Tunnel'ın yaratıcısı, tunnel'a hangi eşlerin katılacağını tam olarak seçer ve her birine gerekli yapılandırma verilerini sağlar. Bunlar uzunluk olarak 0 hop'tan (gateway'in aynı zamanda uç nokta olduğu durum) 7 hop'a kadar (gateway'den sonra ve uç noktadan önce 6 eşin bulunduğu durum) değişebilir. Amaç, hem katılımcılar hem de üçüncü taraflar için bir tunnel'ın uzunluğunu belirlemeyi zorlaştırmak, hatta işbirliği yapan katılımcıların aynı tunnel'ın parçası olup olmadıklarını belirlemelerini bile zorlaştırmaktır (işbirliği yapan eşlerin tunnel içinde yan yana oldukları durum hariç). Bozulmuş mesajlar da mümkün olan en kısa sürede bırakılır, böylece ağ yükü azaltılır.

Uzunluklarının ötesinde, her tunnel için kullanılabilecek ek yapılandırılabilir parametreler vardır; örneğin teslim edilen mesajların boyutu veya sıklığı üzerindeki kısıtlama, dolgunun nasıl kullanılacağı, bir tunnel'ın ne kadar süre çalışır durumda kalacağı, sahte mesajların enjekte edilip edilmeyeceği, parçalama kullanılıp kullanılmayacağı ve hangi toplu işleme stratejilerinin kullanılacağı.

Uygulamada, farklı amaçlar için bir dizi tunnel havuzu kullanılır - her yerel istemci hedefinin kendi gelen tunnel'ları ve giden tunnel'ları vardır ve bunlar anonimlik ile performans gereksinimlerini karşılayacak şekilde yapılandırılır. Ayrıca, router'ın kendisi network veritabanına katılım sağlamak ve tunnel'ların kendilerini yönetmek için bir dizi havuz tutar.

I2P, bu tunnel'lar ile birlikte bile doğası gereği paket anahtarlamalı bir ağdır ve paralel çalışan birden fazla tunnel'dan yararlanabilir, dayanıklılığı artırır ve yükü dengeler. Temel I2P katmanının dışında, istemci uygulamaları için isteğe bağlı uçtan uca akış kütüphanesi mevcuttur ve TCP benzeri işleyiş sunar; mesaj yeniden sıralama, yeniden iletim, tıkanıklık kontrolü vb. dahil.

## 2) Tunnel işletimi {#tunnel.operation}

Tunnel işlemi, tunnel içindeki çeşitli eşler tarafından üstlenilen dört ayrı süreçten oluşur. İlk olarak, tunnel gateway'i bir dizi tunnel mesajı toplar ve bunları tunnel teslimi için ön işleme tabi tutar. Ardından, bu gateway ön işlenmiş veriyi şifreler ve ilk hop'a iletir. Bu eş ve sonraki tunnel katılımcıları şifrelemenin bir katmanını açar, mesajın bütünlüğünü doğrular ve sonra bir sonraki eşe iletir. Sonunda mesaj, gateway tarafından paketlenen mesajların tekrar ayrıştırıldığı ve talep edildiği gibi iletildiği uç noktaya ulaşır.

Tunnel ID'leri, her hop'ta kullanılan 4 baytlık sayılardır - katılımcılar hangi tunnel ID ile mesajları dinleyeceklerini ve bu mesajların bir sonraki hop'a hangi tunnel ID ile iletilmesi gerektiğini bilirler. Tunnel'ların kendileri kısa ömürlüdür (şu anda 10 dakika), ancak tunnel'ın amacına bağlı olarak ve sonraki tunnel'lar aynı peer dizisi kullanılarak oluşturulabilse de, her hop'un tunnel ID'si değişecektir.

### 2.1) Mesaj ön işleme {#tunnel.preprocessing}

Gateway, tunnel üzerinden veri iletmek istediğinde, önce sıfır veya daha fazla I2NP mesajı toplar (32KB'tan fazla olmamak üzere), ne kadar dolgu kullanılacağını seçer ve her I2NP mesajının tunnel uç noktası tarafından nasıl işleneceğine karar vererek bu veriyi ham tunnel yüküne kodlar:

- Dolgu baytlarının sayısını belirten 2 baytlık işaretsiz tamsayı
- o kadar rastgele bayt
- sıfır veya daha fazla { talimat, mesaj } çifti serisi

Talimatlar aşağıdaki şekilde kodlanır:

- 1 bayt değer:
  ```
  bit 0-1: teslimat türü
           (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
    bit 2: gecikme dahil mi?  (1 = doğru, 0 = yanlış)
    bit 3: parçalanmış mı?  (1 = doğru, 0 = yanlış)
    bit 4: genişletilmiş seçenekler?  (1 = doğru, 0 = yanlış)
  bit 5-7: ayrılmış
  ```
- teslimat türü TUNNEL ise, 4 bayt tunnel ID
- teslimat türü TUNNEL veya ROUTER ise, 32 bayt router hash
- gecikme dahil bayrağı doğru ise, 1 bayt değer:
  ```
    bit 0: tür (0 = kesin, 1 = rastgele)
  bit 1-7: gecikme üssü (2^değer dakika)
  ```
- parçalanmış bayrağı doğru ise, 4 bayt mesaj ID'si ve 1 bayt değer:
  ```
  bit 0-6: parça numarası
    bit 7: son mu?  (1 = doğru, 0 = yanlış)
  ```
- genişletilmiş seçenekler bayrağı doğru ise:
  ```
  = 1 bayt seçenek boyutu (bayt cinsinden)
  = o kadar bayt
  ```
- I2NP mesajının 2 bayt boyutu

I2NP mesajı standart formunda kodlanır ve ön işlemden geçirilmiş yük 16 baytın katlarına tamamlanmalıdır.

### 2.2) Gateway işleme {#tunnel.gateway}

Mesajların dolgulu yük haline ön işlemden geçirilmesinden sonra, gateway yükü sekiz anahtarla şifreler, her eşin yükün bütünlüğünü herhangi bir zamanda doğrulayabilmesi için bir sağlama toplamı bloğu ve tunnel uç noktasının sağlama toplamı bloğunun bütünlüğünü doğrulaması için uçtan uca doğrulama bloğu oluşturur. Spesifik detaylar aşağıda yer almaktadır.

Kullanılan şifreleme, çözümlemenin yalnızca verileri CBC modunda AES ile işlemek, mesajın belirli sabit bir kısmının SHA256'sını hesaplamak (16. bayttan $size-144'e kadar) ve bu hash'in ilk 16 baytını checksum bloğunda aramak şeklinde yapılmasını sağlar. Sabit sayıda hop tanımlanmıştır (8 peer) böylece mesajı ne tunnel içindeki konumu sızdırmadan ne de katmanlar soyulurken mesajın sürekli "küçülmesine" neden olmadan doğrulayabiliriz. 8 hop'tan kısa tunnel'lar için, tunnel yaratıcısı fazla hop'ların yerini alacak ve kendi anahtarlarıyla şifre çözecektir (outbound tunnel'lar için bu başlangıçta yapılır, inbound tunnel'lar için ise sonda).

Şifrelemede zor olan kısım, o karmaşık checksum bloğunu oluşturmaktır; bu da temelde her adımda payload'ın hash'inin nasıl görüneceğini bulmayı, bu hash'leri rastgele sıralamayı, ardından bu rastgele sıralanmış hash'lerin her birinin her adımda nasıl görüneceğinin bir matrisini oluşturmayı gerektirir. Gateway'in kendisi, ilk hop'un önceki hop'un gateway olduğunu anlayamaması için checksum bloğu içindeki eşlerden biriymiş gibi davranmalıdır. Bunu biraz görselleştirmek için:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
Yukarıdaki örnekte, P[7] tunnel'dan geçirilen orijinal veriyle aynıdır (ön işlemden geçmiş mesajlar), ve V[7] ise peer7'de şifre çözme işleminden sonra görülen eH[0-7]'nin SHA256'sının ilk 16 baytıdır. Matristeki hash'den "yukarıda" bulunan hücreler için, değerleri altındaki hücreyi, altındaki peer'ın anahtarıyla şifreleyerek elde edilir ve solundaki sütunun sonunu IV olarak kullanır. Matristeki hash'den "aşağıda" bulunan hücreler için ise, üstlerindeki hücreye eşittir, mevcut peer'ın anahtarıyla şifresi çözülür ve o satırdaki önceki şifrelenmiş bloğun sonu IV olarak kullanılır.

Bu randomize edilmiş sağlama bloğu matrisi ile, her peer payload'ın hash'ini bulabilecek veya eğer orada değilse, mesajın bozuk olduğunu bilebilecektir. CBC modu kullanarak dolaştırma, sağlama bloklarının kendilerinin etiketlenmesi zorluğunu artırır, ancak etiketlenmiş verilerden sonraki sütunlar zaten bir peer'da payload'ı kontrol etmek için kullanıldıysa, bu etiketlemenin kısa süre tespit edilmeden kalması hala mümkündür. Her durumda, tunnel endpoint'i (peer 7) herhangi bir sağlama bloğunun etiketlenip etiketlenmediğini kesin olarak bilir, çünkü bu durum doğrulama bloğunu (V[7]) bozar.

IV[0] rastgele 16 baytlık bir değerdir ve IV[i], H(D(IV[i-1], K[i-1]) xor IV_WHITENER) değerinin ilk 16 baytıdır. Yol boyunca aynı IV'yi kullanmayız çünkü bu önemsiz gizli anlaşmaya olanak tanır ve anahtar sızıntısını engellemek için IV'yi yaymak üzere şifresi çözülmüş değerin hash'ini kullanırız. IV_WHITENER sabit 16 baytlık bir değerdir.

Gateway mesajı göndermek istediğinde, ilk atlama olan eş için doğru satırı dışa aktarır (genellikle peer1.recv satırı) ve bunu tamamen iletir.

### 2.3) Katılımcı işleme {#tunnel.participant}

Bir tunnel katılımcısı bir mesaj aldığında, tunnel anahtarları ile AES256'yı CBC modunda kullanarak bir katmanı şifreler ve ilk 16 baytı IV olarak kullanır. Daha sonra payload olarak gördüklerinin (16. bayttan $size-144'e kadar olan baytlar) hash'ini hesaplar ve bu hash'in ilk 16 baytını şifresi çözülmüş checksum bloğu içinde arar. Eğer eşleşme bulunamazsa, mesaj atılır. Aksi takdirde, IV şifresi çözülerek, bu değer IV_WHITENER ile XOR'lanarak ve hash'inin ilk 16 baytı ile değiştirilerek güncellenir. Ortaya çıkan mesaj daha sonra işlenmek üzere bir sonraki peer'a iletilir.

Tunnel seviyesinde tekrar saldırılarını önlemek için, her katılımcı tunnel'ın yaşam süresi boyunca alınan IV'leri takip eder ve kopyaları reddeder. Gereken bellek kullanımı minimal olmalıdır, çünkü her tunnel'ın çok kısa bir yaşam süresi vardır (şu anda 10dk). Tam 32KB mesajları ile tunnel üzerinden sabit 100KBps, 1875 mesaj verir ve 30KB'dan az bellek gerektirir. Gateway'ler ve endpoint'ler, tunnel içindeki I2NP mesajlarında mesaj ID'lerini ve son kullanma tarihlerini takip ederek tekrarları ele alır.

### 2.4) Endpoint işleme {#tunnel.endpoint}

Bir mesaj tunnel uç noktasına ulaştığında, normal bir katılımcı gibi şifresini çözer ve doğrular. Checksum bloğu geçerli bir eşleşmeye sahipse, uç nokta daha sonra checksum bloğunun kendisinin (şifre çözme sonrası görüldüğü gibi) hash'ini hesaplar ve bunu şifresi çözülmüş doğrulama hash'i (son 16 byte) ile karşılaştırır. Eğer bu doğrulama hash'i eşleşmezse, uç nokta tunnel katılımcılarından biri tarafından yapılan etiketleme girişimini not eder ve muhtemelen mesajı atar.

Bu noktada, tunnel uç noktası gateway tarafından gönderilen önceden işlenmiş verilere sahiptir ve bu verileri dahil edilen I2NP mesajlarına ayrıştırabilir ve teslimat talimatlarında istendiği gibi iletebilir.

### 2.5) Doldurma {#tunnel.padding}

Birkaç tunnel dolgu stratejisi mümkündür, her birinin kendi avantajları vardır:

- Dolgu yok
- Rastgele boyuta dolgu
- Sabit boyuta dolgu
- En yakın KB'ye dolgu
- En yakın üstel boyuta dolgu (2^n bayt)

*Hangisini kullanmalı? dolgu yok en verimli olanıdır, rastgele dolgu şu anda sahip olduğumuz şeydir, sabit boyut ya aşırı bir israf olur ya da bizi parçalama uygulamaya zorlar. En yakın üstel boyuta dolgu yapmak (Freenet gibi) umut verici görünüyor. Belki de ağda hangi boyutta mesajların olduğuna dair bazı istatistikler toplamalı, sonra farklı stratejilerden hangi maliyetler ve faydaların çıkacağını görmeliyiz?*

### 2.6) Tunnel parçalanması {#tunnel.fragmentation}

Çeşitli doldurma ve karıştırma şemaları için, tek bir I2NP mesajını birden fazla parçaya bölerek her birini farklı tunnel mesajları aracılığıyla ayrı ayrı teslim etmek anonimlik açısından yararlı olabilir. Uç nokta bu parçalamayı destekleyebilir veya desteklemeyebilir (parçaları gerektiği gibi atabilir veya bekletebilir) ve parçalama işlemi hemen uygulanmayacaktır.

### 2.7) Alternatifler {#tunnel.alternatives}

#### 2.7.1) Checksum bloğu kullanma {#tunnel.nochecksum}

Yukarıdaki sürecin bir alternatifi, checksum bloğunu tamamen kaldırmak ve doğrulama hash'ini payload'un düz bir hash'i ile değiştirmektir. Bu, tunnel gateway'de işlemeyi basitleştirir ve her hop'ta 144 bayt bant genişliği tasarrufu sağlar. Öte yandan, tunnel içindeki saldırganlar, daha sonraki tunnel katılımcılarına ek olarak işbirliği yapan harici gözlemciler tarafından kolayca izlenebilecek bir boyuta mesaj boyutunu önemsiz bir şekilde ayarlayabilirler. Bozulma aynı zamanda mesajı iletmek için gerekli olan tüm bant genişliğinin boşa harcanmasına da neden olur. Hop başına doğrulama olmadan, aşırı uzun tunnel'lar oluşturarak veya tunnel'a döngüler ekleyerek aşırı ağ kaynaklarının tüketilmesi de mümkün olur.

#### 2.7.2) Tunnel işlemeyi akış ortasında ayarlama {#tunnel.reroute}

Basit tunnel yönlendirme algoritması çoğu durum için yeterli olsa da, keşfedilebilecek üç alternatif bulunmaktadır:

- Bir tunnel içindeki mesajı rastgele bir hop'ta belirtilen bir süre boyunca veya rastgele bir periyot için geciktirin. Bu, checksum bloğundaki hash'i örneğin hash'in ilk 8 baytı ile değiştirip ardından bazı gecikme talimatları ekleyerek gerçekleştirilebilir. Alternatif olarak, talimatlar katılımcıya ham payload'ı olduğu gibi yorumlamasını ve mesajı ya atmasını ya da yol boyunca iletmeye devam etmesini söyleyebilir (burada endpoint tarafından chaff mesajı olarak yorumlanacaktır). Bunun son kısmı, gateway'in şifreleme algoritmasını farklı bir hop'ta cleartext payload üretecek şekilde ayarlamasını gerektirir, ancak çok sorun olmamalıdır.

- Bir tunnel'a katılan router'ların mesajı iletmeden önce yeniden karıştırmasına izin ver - o eşin kendi giden tunnel'larından biri aracılığıyla sektirerek, bir sonraki atlamaya teslim talimatları taşıyarak. Bu, kontrollü bir şekilde (yukarıdaki gecikmeler gibi yol üzerinde talimatlarla) veya olasılıksal olarak kullanılabilir.

- Tunnel oluşturucusunun bir peer'ın tunnel içindeki "sonraki atlama" noktasını yeniden tanımlamasını sağlayan kodu uygulayın, böylece daha fazla dinamik yönlendirmeye izin verin.

#### 2.7.3) İki yönlü tunnel'ları kullanın {#tunnel.bidirectional}

Gelen ve giden iletişim için iki ayrı tunnel kullanma mevcut stratejisi mevcut tek teknik değildir ve anonimlik açısından etkileri vardır. Olumlu tarafı, ayrı tunnel'lar kullanarak bir tunnel'daki katılımcılara analiz için maruz kalan trafik verilerini azaltmasıdır - örneğin, bir web tarayıcısından giden tunnel'daki eşler yalnızca bir HTTP GET trafiğini görürken, gelen tunnel'daki eşler tunnel boyunca iletilen yükü görür. Çift yönlü tunnel'larda, tüm katılımcılar örneğin bir yönde 1KB gönderildiği, sonra diğer yönde 100KB gönderildiği gerçeğine erişim sahibi olurlar. Olumsuz tarafı, tek yönlü tunnel'lar kullanmanın profillenmesi ve hesaba katılması gereken iki set eş olduğu anlamına gelmesi ve predecessor saldırılarının artan hızını ele almak için ek özen gösterilmesi gerektiğidir. Aşağıda özetlenen tunnel havuzlama ve oluşturma süreci predecessor saldırısı endişelerini minimize etmelidir, ancak arzu edilirse, hem gelen hem de giden tunnel'ları aynı eşler boyunca oluşturmak fazla zahmet olmayacaktır.

#### 2.7.4) Daha küçük blok boyutu kullan {#tunnel.smallerhashes}

Şu anda AES kullanımımız blok boyutunu 16 byte ile sınırlıyor, bu da her bir checksum blok sütunu için minimum boyutu belirliyor. Daha küçük blok boyutuna sahip başka bir algoritma kullanılsaydı veya hash'in daha küçük bölümleriyle checksum bloğunu güvenli bir şekilde oluşturmaya izin verebilseydi, bu araştırılmaya değer olabilirdi. Şu anda her hop'ta kullanılan 16 byte yeterinden fazla olmalıdır.

## 3) Tunnel oluşturma {#tunnel.building}

Bir tunnel oluştururken, yaratıcı her hop'a gerekli yapılandırma verilerini içeren bir istek göndermeli, ardından potansiyel katılımcının kabul ettiğini veya etmediğini belirten yanıtını beklemeli. Bu tunnel istek mesajları ve yanıtları garlic encryption ile sarmalanır böylece yalnızca anahtarı bilen router bunları çözebilir ve her iki yönde alınan yol da tunnel üzerinden yönlendirilir. Tunnel'ları üretirken akılda tutulması gereken üç önemli boyut vardır: hangi eşlerin kullanıldığı (ve nerede), isteklerin nasıl gönderildiği (ve yanıtların nasıl alındığı), ve nasıl sürdürüldükleri.

### 3.1) Peer seçimi {#tunnel.peerselection}

İki tunnel türünün - gelen ve giden - ötesinde, farklı tunneller için kullanılan iki peer seçim stili vardır - exploratory ve client. Exploratory tunneller hem network database bakımı hem de tunnel bakımı için kullanılırken, client tunneller uçtan uca client mesajları için kullanılır.

#### 3.1.1) Keşif tunnel eş seçimi {#tunnel.selection.exploratory}

Keşif tunnel'ları, ağın bir alt kümesinden rastgele seçilen eşler kullanılarak oluşturulur. Bu belirli alt küme, yerel router ve tunnel yönlendirme ihtiyaçlarına göre değişir. Genel olarak, keşif tunnel'ları eşin "başarısız olmayan ancak aktif" profil kategorisindeki rastgele seçilmiş eşlerden oluşturulur. Tunnel'ların yalnızca tunnel yönlendirmesinin ötesindeki ikincil amacı, az kullanılan yüksek kapasiteli eşleri bularak onları istemci tunnel'larında kullanım için yükseltebilmektir.

#### 3.1.2) İstemci tunnel eş seçimi {#tunnel.selection.client}

İstemci tunnel'ları daha katı gereksinimler seti ile oluşturulur - yerel router, performans ve güvenilirliğin istemci uygulamasının ihtiyaçlarını karşılayabilmesi için eş noktalarını "hızlı ve yüksek kapasiteli" profil kategorisinden seçecektir. Ancak, istemcinin anonimlik ihtiyaçlarına bağlı olarak, bu temel seçimin ötesinde uyulması gereken birkaç önemli detay daha vardır.

Saldırganların predecessor saldırısı düzenleme konusunda endişeli olan bazı istemciler için, tunnel seçimi eşleri katı bir düzende tutabilir - A, B ve C bir tunnel'da ise, A'dan sonraki atlama her zaman B'dir ve B'den sonraki atlama her zaman C'dir. Daha az katı bir sıralama da mümkündür, A'dan sonraki atlamanın B olabileceğini ancak B'nin asla A'dan önce olamayacağını garanti eder. Diğer yapılandırma seçenekleri arasında yalnızca gelen tunnel gateway'lerinin ve giden tunnel uç noktalarının sabit tutulması veya MTBF oranında döndürülmesi yer alır.

### 3.2) İstek teslimi {#tunnel.request}

Yukarıda belirtildiği gibi, tunnel oluşturucu hangi eş düğümlerin bir tunnel'a hangi sırayla dahil edilmesi gerektiğini öğrendikten sonra, oluşturucu her biri o eş düğüm için gerekli bilgileri içeren bir dizi tunnel istek mesajı oluşturur. Örneğin, katılımcı tunnel'lar mesajları alacakları 4 baytlık tunnel ID'si, mesajları gönderecekleri 4 baytlık tunnel ID'si, bir sonraki hop'un kimliğinin 32 baytlık hash'i ve tunnel'dan bir katmanı kaldırmak için kullanılan 32 baytlık katman anahtarı verilir. Tabii ki, outbound tunnel uç noktalarına herhangi bir "sonraki hop" veya "sonraki tunnel ID" bilgisi verilmez. Ancak inbound tunnel gateway'lerine şifrelenmesi gereken sırayla 8 katman anahtarı verilir (yukarıda açıklandığı gibi). Yanıtlara izin vermek için, istek rastgele bir oturum etiketi ve eş düğümün kararını garlic encryption ile şifreleyebileceği rastgele bir oturum anahtarı ve o garlic'in gönderilmesi gereken tunnel'ı içerir. Yukarıdaki bilgilere ek olarak, tunnel'a hangi kısıtlamaların uygulanacağı, hangi dolgu veya toplu işlem stratejilerinin kullanılacağı gibi çeşitli istemciye özgü seçenekler dahil edilebilir.

Tüm istek mesajları oluşturulduktan sonra, hedef router için garlic encryption ile sarılır ve keşif tunnel'ı üzerinden gönderilir. Alındığında, o eş katılıp katılamayacağını veya katılmak isteyip istemediğini belirler, bir yanıt mesajı oluşturur ve sağlanan bilgilerle yanıtı hem garlic encryption ile sarar hem de tunnel routing yapar. Yanıt tunnel oluşturucusu tarafından alındığında, tunnel o hop üzerinde geçerli kabul edilir (eğer kabul edildiyse). Tüm eşler kabul ettiğinde, tunnel aktif hale gelir.

### 3.3) Havuzlama {#tunnel.pooling}

Verimli çalışmaya izin vermek için router, her biri kendi yapılandırmasına sahip belirli bir amaç için kullanılan tunnel gruplarını yöneten bir dizi tunnel havuzu tutar. Bu amaç için bir tunnel gerektiğinde, router uygun havuzdan rastgele birini seçer. Genel olarak, iki adet keşif tunnel havuzu vardır - biri gelen ve biri giden - her ikisi de router'ın keşif varsayılanlarını kullanır. Ayrıca, her yerel hedef için bir çift havuz bulunur - biri gelen ve biri giden tunnel. Bu havuzlar, yerel hedef router'a bağlandığında belirtilen yapılandırmayı veya belirtilmemişse router'ın varsayılanlarını kullanır.

Her havuzun konfigürasyonunda, kaç tunnel'ın aktif tutulacağını, arıza durumunda kaç yedek tunnel'ın bulundurulacağını, tunnel'ların ne sıklıkla test edileceğini, tunnel'ların ne kadar uzun olması gerektiğini, bu uzunlukların rastgele hale getirilip getirilmeyeceğini, yedek tunnel'ların ne sıklıkla inşa edilmesi gerektiğini ve ayrı tunnel'ları yapılandırırken izin verilen diğer ayarları tanımlayan birkaç anahtar ayar bulunur.

### 3.4) Alternatifler {#tunnel.building.alternatives}

#### 3.4.1) Teleskopik inşa {#tunnel.building.telescoping}

Keşif tünellerinin tunnel oluşturma mesajlarını göndermek ve almak için kullanılması konusunda ortaya çıkabilecek bir soru, bunun tünelin predecessor saldırılara karşı güvenlik açığını nasıl etkilediğidir. Bu tünellerin uç noktaları ve gateway'leri ağ üzerinde rastgele dağıtılacak olsa da (belki de tunnel oluşturucu bile bu kümeye dahil edilebilir), başka bir alternatif, istek ve yanıtları aktarmak için tunnel yollarının kendisini kullanmaktır; bu [TOR](https://www.torproject.org/)'da yapıldığı gibidir. Ancak bu, tunnel oluşturma sırasında sızıntılara yol açabilir ve eşlerin tunnel inşa edilirken zamanlama veya paket sayısını izleyerek tunnel içinde daha sonra kaç hop olduğunu keşfetmelerine olanak tanıyabilir. Bu sorunu en aza indirmek için teknikler kullanılabilir; örneğin bir sonraki hop'u inşa etmeye devam etmeden önce hop'ların her birini rastgele sayıda mesaj için uç nokta olarak ([2.7.2](#tunnel.reroute) bölümünde belirtildiği gibi) kullanmak.

#### 3.4.2) Yönetim için keşif dışı tunnel'lar {#tunnel.building.nonexploratory}

Tunnel oluşturma sürecine ikinci bir alternatif, router'a keşif yapmayan ek gelen ve giden havuzlar vererek bunları tunnel isteği ve yanıtı için kullanmaktır. Router'ın ağın iyi entegre edilmiş bir görünümüne sahip olduğu varsayılırsa, bu gerekli olmamalıdır, ancak router bir şekilde bölümlenmiş ise, tunnel yönetimi için keşif yapmayan havuzları kullanmak, hangi eşlerin router'ın bölümünde olduğu hakkındaki bilgi sızıntısını azaltacaktır.

## 4) Tunnel kısıtlaması {#tunnel.throttling}

I2P içindeki tunnellar devre anahtarlamalı bir ağa benzese de, I2P içindeki her şey kesinlikle mesaj tabanlıdır - tunnellar yalnızca mesajların teslimini organize etmeye yardımcı olan muhasebe hileleridir. Mesajların güvenilirliği veya sıralaması konusunda hiçbir varsayım yapılmaz ve yeniden iletimler daha üst seviyelerden (örneğin I2P'nin istemci katmanı streaming kütüphanesi) bırakılır. Bu, I2P'nin hem paket anahtarlamalı hem de devre anahtarlamalı ağlarda mevcut olan daraltma tekniklerinden yararlanmasına olanak tanır. Örneğin, her router, her tunnelın ne kadar veri kullandığının hareketli ortalamasını takip edebilir, bunu routerın katıldığı diğer tüm tunnellar tarafından kullanılan ortalamalarla birleştirebilir ve kapasitesi ile kullanımına dayalı olarak ek tunnel katılım isteklerini kabul edebilir veya reddedebilir. Diğer yandan, her router kapasitesini aşan mesajları basitçe düşürebilir ve normal İnternet'te kullanılan araştırmalardan yararlanabilir.

## 5) Karıştırma/toplu işleme {#tunnel.mixing}

Gateway'de ve her hop'ta mesajları geciktirmek, yeniden sıralamak, yeniden yönlendirmek veya padding yapmak için hangi stratejiler kullanılmalıdır? Bu işlemler ne ölçüde otomatik olarak yapılmalı, ne kadarı tunnel başına veya hop başına ayar olarak yapılandırılmalı ve tunnel'ın yaratıcısı (ve dolayısıyla kullanıcı) bu işlemi nasıl kontrol etmelidir? Tüm bunlar bilinmeyen olarak bırakılmış olup, gelecekteki bir sürümde çözülmesi için beklemektedir.
