---
title: "Hızlı Uzantı (BEP 6) Hedefleme-Hash Eş Kimliği ile Hızlıya İzin Verildi"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Taslak"
toc: true
---

## Genel Bakış

BEP 6 (Hızlı Eklenti), beş özelliği bir araya getirir: **Tümüne Sahip / Hiçbiri Yok**, **İstekleri Reddet**, **Öneriler** ve **İzin Verilen Hızlı**. İletim protokolü — anlaşma biti, mesaj kimlikleri ve choke anlambilimi — taşıma yönteminden bağımsızdır ve I2P akışında olduğu gibi doğrudan çalışır. BEP 6'nın I2P'ye doğrudan eşlenemeyen tek bölümü, eşin IPv4 adresi açısından tanımlandığı için **İzin Verilen Hızlı kümesi oluşturma**dır. I2P eşlerinin IP adresi yoktur; bunlar 32 baytlık hedef karmaları ile tanımlanır.

Bu öneri, aynı peer ve torrent için tüm I2P torrent istemcilerinin *aynı* izin verilen hızlı kümelerini oluşturmasını sağlayan, I2P yerel bir İzin Verilen Hızlı Küme oluşturma yöntemini standartlaştırır ve bu özelliği uygulamalar arasında faydalı (ve doğrulanabilir) hale getirir.

## Motivasyon

Yeni eşlerin BitTorrent'in "göze göz" mekanizmasının hızlanabilmesi için ilk birkaç parçaya ihtiyacı vardır. I2P üzerinde bu artış süreci açık internete göre daha yavaştır: bağlantı kurulumu ve parça teslimi yüksek gecikmeli tünellerin birkaç sıçramasını geçer, bu yüzden bağlanma ile ilk karşılıklı serbest bırakma arasındaki zaman dilimi daha uzundır. İzin Verilen Hızlı (Allowed Fast), bu zaman dilimine doğrudan saldıran bir yöntemdir — başlangıçtaki bir eşe boğulmuş (choked) olsa bile sınırlı sayıda parça gönderimine izin verilir, hemen veri alır ve daha erken karşılık vermeye başlayabilir.

Referans BEP 6, *gönderenin* parçaları *alıcıya* özgü seçmesini garanti etmek için kullanıcının IPv4 adresinden izin verilen hızlı kümeyi hesaplar (tek bir kullanıcı birden fazla IP ile birçok küme toplayamaz). I2P üzerinde, eşin hedef adresi aynı bağlama rolünü üstlenir ve her bağlantının iki ucunun da erişimine açıktır; bu da kümeyi *belirleyici ve yerel olarak doğrulanabilir* kılar — bu özellik, IP tabanlı şemanın sunamadığı bir özelliktir.

## BEP 6'ya Yapılan Değişiklikler

Hızlı Uzantı anlaşması ve dört mesaj türü olduğu gibi benimsenmiştir:

- Müzakere: son ayrılmış baytın üçüncü en düşük anlamlı biti, `reserved[7] |= 0x04`, her iki uçta da
- Hepsi Var `<len=0x0001><op=0x0E>`, Hiçbiri Yok `<len=0x0001><op=0x0F>`
- Parça Öner: `<len=0x0005><op=0x0D><index>`
- İsteği Reddet: `<len=0x000D><op=0x10><index><begin><length>`
- Hızlıya İzin Verildi: `<len=0x0005><op=0x11><index>`
- Her istek tam olarak bir yanıtla sonuçlanır (parça veya red); choke artık bekleyen istekleri örtük olarak reddetmez

Tek istisna, izin verilen hızlı küme oluşturmada, IP baytlarının eşin hedef karması baytlarıyla değiştirilmesidir.

### Sapma: IP'nin maskelenmesi yerine hash baytları

Referans BEP 6, adım (1):

```
x = 0xFFFFFF00 & ip
```
Bu, eşin IPv4 adresinin üç baytını alır ve **4. baytı sıfırlar**. Bu bir alt ağ sezgisel yöntemidir: aynı /24 içinde birden fazla IP edinebilen kullanıcılar, birden fazla izinli hızlı küme elde etmemelidir.

I2P versiyonumuz bunu, eşin 32 baytlık hedef adresinin ilk dört baytıyla değiştirir:

```
x = first 4 bytes of peer destination hash
```
Referans uygulamadan farkı:

> "Bu, IP'nin 3 baytı artı bir sıfır. Sen de hash'in 4 baytısın. BEP 6'dan farklı çünkü IP yok ve 4. bayt sıfırlanmıyor."

Bir I2P bağlantısının her iki ucu da zaten karşı tarafın hedef adresi karmasını bilmektedir (bu, bağlantının kurulduğu/kurulduğu adresidir), bu yüzden ek bir değiş tokuş, NAT keşfi veya harici IP tespiti gerekmez — I2P üzerinde bunlardan hiçbiri mevcut değildir.

### İzin verilen Hızlı üretim algoritması

`hash`, alıcı eşin 32 baytlık hedef karmasını, `infohash` torrentin 20 baytlık bilgi karmasını, `sz` torrentteki parça sayısını, `k` izin verilen hızlı kümedeki son parça sayısını (BEP 6'daki gibi 10), ve `a` çıktıyı temsil etsin:

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Notlar:

- Hedef hash'in 4 baytı, maskelenmiş IP'nin 3 baytını değiştirir. Tüm dört bayt hash entropy'sini taşır; sıfırlanmış olanı yoktur.
- BEP 6'da olduğu gibi, SHA1 zinciri parçalara ayrılan uzun bir sözde rastgele dizi üretir; `k = 10` referans varsayılanıyla eşleşir.
- Allowed Fast mesajı yalnızca bilgilendirme amaçlıdır: alıcı, gönderenin o parçaya sahip olduğu anlamını çıkarmamalıdır — sadece gönderenin tıkanmışken (choked) o parçayı sunacağını belirtir.

## Avantajlar

| Alan             | Fayda                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Başlangıç gecikmesi | Yeni eşler, çoklu zıplı I2P tüneli üzerinden daha yavaş olan tit-for-tat rampasını kısaltmak için engellenirken ilk parçaları çeker                                                                         |
| Belirlilik      | Küme, yalnızca hedef hash + infohash değerlerine bağlıdır, bu yüzden her uygulama aynı kümeyi hesaplar — IP tabanlı BEP 6'nın aksine, gönderenin alıcının IP'sini NAT nedeniyle farklı görebileceği durumlarda olduğu gibi |
| Doğrulanabilirlik    | Alıcı eş, kendi hedef hash'ini bildiği için kümeyi yerel olarak yeniden hesaplayabilir ve doğrulayabilir, böylece kötü niyetli davranan gönderenleri tespit edebilir                                                               |
| IP mekanizması yok  | NAT geçişi, dış IP keşfi veya alt ağ heuristiklerine gerek yok — I2P üzerinde imkansız ya da anlamsız olan tüm bu işlemlerden kurtarır                                                                             |
| Kimlik bağlama | Her hedef için yalnızca bir hızlı kümeye izin verilir. Birden fazla hedefe sahip kullanıcılar, her biri için ayrı ayrı birer küme alır — açık internet üzerinde IP maskesinin sağladığı aynı anti-oyun özelliği |
| Gizlilik          | Hesaplama sırasında hiçbir IP adresi iletilmez veya ima edilmez                                                                                                                               |
| Bant genişliği        | Büyük торрентlerde tam bit alanını Have All / Have None değiştirir; Reject gereksiz tekrar isteklerini ortadan kaldırır                                                                                       |
## Uygulama hususları

- **Eş kimliği**: eşin hedef karması, akış bağlantısından (oturumun hedefi) alınır ve her iki tarafın da kullandığı aynı değerdir. Giden bağlantılar için bağlandığınız hedefi kullanın; gelen bağlantılar için ise bağlantının geldiği hedefi kullanın.
- **Müzakere**: el sıkışma sırasında `reserved[7] |= 0x04` değerini gönderin; yalnızca eşin el sıkışmasında bu bit ayarlanmışsa Hızlı Uzantı mesajları gönderin; bir eş müzakere olmadan Hızlı Uzantı mesajları gönderirse bağlantıyı kapatın.
- **Hepsine Sahip / Hiçbirine Sahip**: el sıkışmadan hemen sonra bit alanı / Hepsine Sahip / Hiçbirine Sahip mesajlarından sadece birini gönderin. Çekirdekler için Hepsine Sahip, ilk parça alınıncaya kadar Hiçbirine Sahip kullanın.
- **Hızlı gönderim tarafı**: yalnızca gerçekten sahip olduğunuz parçaları duyurun; alıcı, boğulmuş olsa bile bu parçaları talep edebilir. *Sunulan* kümesini sınırlayın (örneğin, zaten `k` adetten fazla parça tutan bir eşten gelen "izin verilen hızlı" isteklerini reddedin; BEP 6 rehberliğine göre).
- **Hızlı alım tarafı**: gelen kümeyi saklayın; boğulmuş olsa bile bu parçalar için isteklere izin verin; isteğe bağlı olarak kendi hedef karmınız ve bilgi karması (infohash) kullanarak kümeyi yeniden hesaplayıp doğrulayın ve hesaplanan kümede olmayan parçaları dikkate almayın.
- **Reddetme**: her isteğin tam olarak bir yanıtı OLMALIDIR; boğulma durumunda, eşin sessiz kalmasını sağlayarak değil, izin verilen hızlı kümesinde olmayan tüm istekleri reddedin.
- **Küme boyutu**: uyumluluk için `k = 10` kullanın; eşler yük altında daha düşük bir `k` seçmekte serbesttir ancak her iki taraf da yalnızca sunmayı planladıkları şeyleri duyurmalıdır.
- **Parça sınırı**: `index = y % sz` ifadesinde torrentin toplam parça sayısı olan `sz` kullanılmalıdır; bir hash zinciri parça aralığına göre sınırlanmadığından, `sz`'den büyük veya eşit olan indisleri yok sayın (savunma amaçlı).
- **Geriye dönük uyumluluk**: hızlı biti müzakere etmeyen istemciler bu mesajları asla görmez; başka protokol değişikliği gerekmez.

## Referans uygulamaları

Algoritma küçük ve kendi içinde kapsamlı — herhangi bir dilde birkaç düzine satır. Aşağıdaki üç örnek de aynı girdiler için (`hash[0:4] ++ infohash`, SHA1 zinciri, `y % sz`, sınır `k = 10`) özdeş kümeyi hesaplar.

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Uyumluluk

- **Teli uyumlu**: anlaşma biti ve mesaj formatları açık internet BEP 6 ile bayt-bayt aynıdır; sadece set oluşturma girdisi farklıdır.
- **Ağlar arasında birlikte çalışılır değil**: bir I2P istemcisi ile açık internet istemcisi zaten birbirine bağlanamaz; sapma yalnızca eş kimlik baytlarını etkiler, asla tel formatını etkilemez.
- **I2P içinde**: bu öneriyi uygulayan herhangi bir istemci, aynı izin verilen Hızlı setlerini hesaplar ve bunları birbiriyle değiştirerek sunabilir ve doğrulayabilir. İzin Verilen Hızlı'ya (Allowed Fast) dikkat etmeyen istemciler bunu yalnızca bir işlem önerisi olarak değerlendirir ve yalnızca başlangıç faydasını kaybeder.

## Açık sorular

1. Küme boyutu `k` sabit olarak 10'da mı kalmalı, yoksa BEP 6'nın izin verdiği gibi istek yükü yüksekken daha düşük değerler alacak şekilde yük-eşgüdümlemeli mi olmalıdır?
2. Alıcılar, küme değerini kendi hedef karmaları ile karşılaştırıp uyuşmayan dizinleri reddetmeli mi (hatalı ya da kötü niyetli gönderenlere karşı koruma)? Önerilen: evet.
3. Gösterildiği gibi 4 baytlık *önek* (0-3. baytlar) mi seçilmeli, yoksa son 4 bayt mı? Her sabit 4 baytlık pencere aynı özellikleri verir; önek, referans kodun bayt sıralamasını doğal tutar (`hash[0:4]`).

## Önceki sanat

- Referans: [BEP 6 Hızlı Eklenti](https://www.bittorrent.org/beps/bep_0006.html)
- I2PSnark referans uygulaması: `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` içindeki `PeerState.sendAllowedFast()` / `generateAllowedFastSet()` (@since 0.9.71+)
- BEP 40 (kanonik eş önceliği) ve BEP 21 (kısmi paylaşımcılar) ile birlikte çalışır; her ikisi de I2PSnark tarafından desteklenir
