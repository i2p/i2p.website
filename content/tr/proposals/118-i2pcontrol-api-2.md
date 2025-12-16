---
title: "I2PControl API 2"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Rejected"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Genel Bakış

Bu öneri, I2PControl için API2'yi özetlemektedir.

Bu öneri reddedildi ve uygulanmayacak çünkü geriye dönük uyumluluğu bozuyor.
Ayrıntılar için tartışma konusunun bağlantısına bakın.

### Geliştirici uyarısı!

Tüm RPC parametreleri artık küçük harfle olacak. Bu, API1 uygulamalarıyla
geriye dönük uyumluluğu *bozacaktır*. Bunun nedeni API2 ve üstü kullanıcılarına
mümkün olan en basit ve en tutarlı API'yi sağlamaktır.


## API 2 Özellikleri

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Parametreler

**`"id"`**

İstek numarası. Hangi isteğe hangi yanıtın verildiğini belirlemek için kullanılır.

**`"method_name"`**

Çağrılan RPC'nin adı.

**`"auth_token"`**

Oturum kimlik doğrulama belirteci. 'authenticate' çağrısı hariç her RPC ile sağlanması gerekir.

**`"method_parameter_value"`**

Yöntem parametresi. Bir yöntemin farklı seçeneklerini sunmak için kullanılır. 'get', 'set' ve bu tarz seçenekler gibi.

**`"result_value"`**

RPC'nin döndürdüğü değer. Türü ve içeriği metoda ve hangi metoda bağlıdır.


### Önekler

RPC adlandırma şeması, farklı API uygulamaları için satıcı önekleriyle CSS'de nasıl yapıldığına benzer
(i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
    i2p.XXX.YYY.ZZZ
    i2pd.XXX.YYY.ZZZ
    kovri.XXX.YYY.ZZZ
```

Satıcıya özel öneklerle ilgili genel amaç, bazı esneklik sağlamaktır
ve diğer tüm uygulamaların yetişmesini beklemek zorunda kalmadan yenilik yapmalarına izin vermek.
Bir RPC tüm uygulamalar tarafından gerçekleştirildiğinde, birden fazla öneki kaldırılabilir
ve bir sonraki API sürümünde çekirdek bir RPC olarak dahil edilebilir.


### Yöntem okuma kılavuzu

 * **rpc.method**

   * *parameter* [parametre türü]: [null], [number], [string], [boolean],
     [array] veya [object]. [object], {anahtar:değer} haritası olur.

Döndürür:
```text

  "return_value" [string] // RPC çağrısı tarafından döndürülen değer
```


### Yöntemler

* **authenticate** - Doğru bir şifre sağlandığında, bu yöntem size daha fazla erişim için bir belirteç ve desteklenen API seviyelerinin bir listesini sağlar.

  * *password* [string]:  Bu i2pcontrol uygulaması için şifre

    Döndürür:
```text
    [object]
    {
      "token" : [string], // Diğer tüm RPC yöntemleriyle sağlanacak belirteç
      "api" : [[int],[int], ...]  // Desteklenen API seviyelerinin listesi.
    }
```

* **control.** - i2p'yi kontrol et

  * **control.reseed** - Reseed işlemine başla

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

  * **control.restart** - i2p örneğini yeniden başlat

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

  * **control.restart.graceful** - i2p örneğini nazikçe yeniden başlat

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

  * **control.shutdown** - i2p örneğini kapat

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

  * **control.shutdown.graceful** - i2p örneğini nazikçe kapat

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

  * **control.update.find** - **BLOKE EDİCİ** İmzalı güncellemeleri ara

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      true [boolean] // İmzalı güncelleme mevcutsa doğru
```

  * **control.update.start** - Güncelleme sürecine başla

    * [nil]: Parametre gerekmiyor

    Döndürür:
```text
      [nil]
```

* **i2pcontrol.** - i2pcontrol yapılandırın

  * **i2pcontrol.address** - i2pcontrol'un dinlediği IP adresini al/ayarla.

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: "0.0.0.0" veya "192.168.0.1" gibi bir IP adresi olacak

    Döndürür:
```text
      [nil]
```

  * **i2pcontrol.password** - i2pcontrol şifresini değiştirin.

    * *set* [string]: Yeni şifreyi bu dizeye ayarlayın

    Döndürür:
```text
      [nil]
```

  * **i2pcontrol.port** - i2pcontrol'un dinlediği portu al/ayarla.

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      7650 [number]
```

    * *set* [number]: i2pcontrol'un dinlediği portu bu porta değiştirin

    Döndürür:
```text
      [nil]
```

* **settings.** - i2p örneği ayarlarını al/ayarla

  * **settings.advanced** - Gelişmiş ayarlar

    * *get*  [string]: Bu ayarın değerini al

    Döndürür:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    Döndürür:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: Bu ayarın değerini ayarla
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Döndürür:
```text
      [nil]
```

  * **settings.bandwidth.in** - Gelen bant genişliği ayarları
  * **settings.bandwidth.out** - Giden bant genişliği ayarları

    * *get* [nil]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0 [number]
```

    * *set* [number]: Bant genişliği sınırını ayarla

    Döndürür:
```text
     [nil]
```

  * **settings.ntcp.autoip** - NTCP için IP otomatik algılama ayarını al

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - NTCP sunucu adını al

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Yeni sunucu adını ayarla

    Döndürür:
```text
      [nil]
```

  * **settings.ntcp.port** - NTCP portu

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0 [number]
```

    * *set* [number]: Yeni NTCP portunu ayarla.

    Döndürür:
```text
      [nil]
```

    * *set* [boolean]: NTCP IP otomatik algılama ayarla

    Döndürür:
```text
      [nil]
```

  * **settings.ssu.autoip** - SSU için IP otomatik algılama ayarını yapılandırın

    * *get* [nil]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - SSU sunucu adını yapılandırın

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Yeni SSU sunucu adını ayarla

    Döndürür:
```text
      [nil]
```

  * **settings.ssu.port** - SSU portu

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0 [number]
```

    * *set* [number]: Yeni SSU portunu ayarla.

    Döndürür:
```text
      [nil]
```

    * *set* [boolean]: SSU IP otomatik algılama ayarla

    Döndürür:
```text
      [nil]
```

  * **settings.share** - Bant genişliği paylaşım yüzdesini al

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0 [number] // Bant genişliği paylaşım yüzdesi (0-100)
```

    * *set* [number]: Bant genişliği paylaşım yüzdesini ayarla (0-100)

    Döndürür:
```text
      [nil]
```

  * **settings.upnp** - UPNP'yi etkinleştir veya devre dışı bırak

    * *get* [nil]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      true [boolean]
```

    * *set* [boolean]: SSU IP otomatik algılama ayarla

    Döndürür:
```text
      [nil]
```

* **stats.** - i2p örneğinden istatistikler al

  * **stats.advanced** - Bu yöntem, örnek içinde tutulan tüm istatistiklere erişim sağlar.

    * *get* [string]:  Sağlanacak gelişmiş istatistiğin adı
    * *Optional:* *period* [number]:  İstenen istatistik için dönem

  * **stats.knownpeers** - Bilinen eşlerin sayısını döndürür
  * **stats.uptime** - Yönlendirici başlatıldığından itibaren geçen süreyi ms cinsinden döndürür
  * **stats.bandwidth.in** - Gelen bant genişliğini döndürür (ideal olarak son saniye için)
  * **stats.bandwidth.in.total** - Son yeniden başlatmadan bu yana alınan bayt sayısını döndürür
  * **stats.bandwidth.out** - Giden bant genişliğini döndürür (ideal olarak son saniye için)'
  * **stats.bandwidth.out.total** - Son yeniden başlatmadan bu yana gönderilen bayt sayısını döndürür'
  * **stats.tunnels.participating** - Şu anda katılım sağlanan tünel sayısını döndürür
  * **stats.netdb.peers.active** - Son zamanlarda iletişim kurduğumuz eşlerin sayısını döndürür
  * **stats.netdb.peers.fast** - 'Hızlı' eşlerin sayısını döndürür
  * **stats.netdb.peers.highcapacity** - 'Yüksek kapasiteli' eşlerin sayısını döndürür
  * **stats.netdb.peers.known** - Bilinen eşlerin sayısını döndürür

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0.0 [number]
```

* **status.** - i2p örneği durumunu al

  * **status.router** - Yönlendirici durumunu al

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      "status" [string]
```

  * **status.net** - Yönlendirici ağ durumunu al

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - i2p örneği şu anda bir floodfill mi

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      true [boolean]
```

  * **status.isreseeding** - i2p örneği şu anda yeniden tohumlanıyor mu

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      true [boolean]
```

  * **status.ip** - Bu i2p örneğinin algılanan genel IP'si

    * *get* [null]: Bu parametrenin ayarlanmasına gerek yoktur.

    Döndürür:
```text
      "0.0.0.0" [string]
```
