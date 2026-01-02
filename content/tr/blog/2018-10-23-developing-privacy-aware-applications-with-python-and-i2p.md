---
title: "Python ve I2P ile gizliliğe duyarlı uygulamalar geliştirme"
date: 2018-10-23
author: "villain"
description: "Python ile I2P uygulama geliştirmenin temel kavramları"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P), gizlilik odaklı uygulamalar geliştirmek için bir çerçeve sağlar. Bu, normal İnternetin üzerinde çalışan bir sanal ağdır; bu ağda ana makineler "gerçek" IP adreslerini ifşa etmeden veri alışverişi yapabilir. I2P ağı içindeki bağlantılar, *I2P destinations* (I2P hedefleri) adı verilen sanal adresler arasında kurulur. Gereksinim duyduğunuz kadar çok hedefe sahip olmak mümkündür; hatta her bağlantı için yeni bir hedef kullanabilirsiniz; bunlar karşı tarafa gerçek IP adresi hakkında herhangi bir bilgi açıklamaz.

Bu makale, I2P uygulamaları geliştirirken bilinmesi gereken temel kavramları açıklar. Kod örnekleri, yerleşik asenkron framework (yazılım çatısı) asyncio kullanılarak Python ile yazılmıştır.

## SAM API'yi etkinleştirme ve i2plib kurulumu

I2P, istemci uygulamalarına birçok farklı API sunar. Normal istemci-sunucu uygulamaları I2PTunnel, HTTP ve Socks vekil sunucularını kullanabilir; Java uygulamaları genellikle I2CP kullanır. Python gibi diğer dillerle geliştirme yapmak için en iyi seçenek [SAM](/docs/api/samv3/)’dir. Orijinal Java istemci uygulamasında SAM varsayılan olarak devre dışıdır, bu yüzden onu etkinleştirmemiz gerekir. Router Console’da "I2P internals" -> "Clients" sayfasına gidin. "Run at Startup" seçeneğini işaretleyin ve "Start" düğmesine, ardından "Save Client Configuration" düğmesine basın.

![SAM API'yi Etkinleştir](https://geti2p.net/images/enable-sam.jpeg)

[C++ gerçekleştirmesi i2pd](https://i2pd.website)'de SAM varsayılan olarak etkindir.

SAM API için [i2plib](https://github.com/l-n-s/i2plib) adlı kullanışlı bir Python kütüphanesi geliştirdim. Bunu pip ile yükleyebilir veya kaynak kodunu GitHub'dan manuel olarak indirebilirsiniz.

```bash
pip install i2plib
```
Bu kitaplık, Python'un yerleşik [asenkron çerçevesi asyncio](https://docs.python.org/3/library/asyncio.html) ile çalışır, bu nedenle kod örneklerinin olay döngüsü içinde çalışan async fonksiyonlardan (coroutine'lerden) alındığını lütfen unutmayın. i2plib kullanımına ilişkin ek örnekler [kaynak kod deposunda](https://github.com/l-n-s/i2plib/tree/master/docs/examples) bulunabilir.

## I2P Destination (hedef adres) ve oturum oluşturma

I2P destination (I2P hedefi), tam anlamıyla şifreleme ve kriptografik imza anahtarlarından oluşan bir kümedir. Bu kümedeki açık anahtarlar I2P ağına yayınlanır ve IP adresleri yerine bağlantı kurmak için kullanılır.

Bir [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination) şu şekilde oluşturulur:

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
base32 adresi, diğer eşlerin ağdaki tam Destination (I2P uç nokta kimliği) bilgisini keşfetmek için kullandığı bir karmadır. Programınızda bu Destination'ı kalıcı bir adres olarak kullanmayı planlıyorsanız, *dest.private_key.data* içindeki ikili veriyi yerel bir dosyaya kaydedin.

Artık bir SAM oturumu oluşturabilirsiniz; bu, kelimenin tam anlamıyla Destination (I2P Hedefi) öğesini I2P'de çevrimiçi hale getirmek anlamına gelir:

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Önemli bir not: Destination (I2P hedef adresi), *session_writer* soketi açık tutulduğu sürece çevrimiçi kalacaktır. Kapatmak isterseniz, *session_writer.close()* çağırabilirsiniz.

## Giden bağlantılar kurma

Artık Destination (Hedef) çevrimiçi olduğuna göre, onu diğer eşlere bağlanmak için kullanabilirsiniz. Örneğin, "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p" adresine bu şekilde bağlanır, bir HTTP GET isteği gönderir ve yanıtı okursunuz (bu, "i2p-projekt.i2p" web sunucusudur):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## Gelen bağlantıları kabul etme

Giden bağlantılar kurmak oldukça basit olsa da, bağlantı kabul ederken önemli bir ayrıntı vardır. Yeni bir istemci bağlandığında, SAM API istemcinin base64 ile kodlanmış Destination'ını içeren bir ASCII dizesini sokete gönderir. Destination ve veri tek bir parça halinde gelebileceği için bunun farkında olmalısınız.

Basit bir PING-PONG sunucusu şöyle görünür. Gelen bağlantıyı kabul eder, istemcinin Destination (Hedef) bilgisini *remote_destination* değişkenine kaydeder ve "PONG" dizesini geri gönderir:

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## Daha fazla bilgi

Bu makale, TCP benzeri bir Akış (Streaming) protokolünün kullanımını açıklar. SAM API ayrıca datagram göndermek ve almak için UDP benzeri bir protokol sağlar. Bu özellik i2plib'e daha sonra eklenecektir.

Bu sadece temel bir bilgidir, ancak I2P kullanarak kendi projenize başlamanız için yeterlidir. Invisible Internet, her türlü gizlilik odaklı uygulama geliştirmek için harika bir araçtır. Ağ tarafından dayatılan tasarım kısıtları yoktur; bu uygulamalar hem istemci-sunucu hem de P2P olabilir.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
