---
title: "Protokol Yığını"
description: "I2P protokol yığını katmanlarının genel bakışı"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/tr/docs/develop/protocol-stack"
  - "/tr/docs/develop/protocol-stack/"
  - "/tr/protocols"
  - "/tr/protocols/"
---

I2P yığını, anonim iletişimi sağlayan katmanlı bir tasarımdır. Her katman, altındaki katmanların yeteneklerine ek olarak belirli özellikler ekler. Her bileşen hakkında ek ayrıntılar için [Teknik Dokümantasyon İndeksi](/docs/develop/overview)'ne bakın.

## İnternet Katmanı {#internet}

**IP** - Internet Protocol, normal internetteki hostları adreslemesine ve paketleri internet üzerinden en iyi çaba teslimatı kullanarak yönlendirmesine olanak tanır.

## Transport Katmanı {#transport}

- **TCP** - Transmission Control Protocol, paketlerin güvenilir ve sıralı teslimatına olanak tanır
- **UDP** - User Datagram Protocol, paketlerin güvenilmez ve sırasız teslimatına olanak tanır

## I2P Transport Katmanı {#i2p-transport}

Şifrelenmiş router'dan router'a bağlantılar (henüz anonim değil):

- **[NTCP2](/docs/specs/ntcp2)** - NIO tabanlı TCP taşıma protokolü
- **[SSU2](/docs/specs/ssu2)** - Güvenli Yarı-güvenilir UDP taşıma protokolü

## I2P Tunnel Katmanı {#tunnels}

Tam anonim şifrelenmiş tunnel bağlantıları sağlar:

- **[Tunnel mesajları](/docs/legacy/tunnel-message)** - Şifrelenmiş I2NP mesajları ve bunların teslimatı için şifrelenmiş talimatlar
- **[I2NP mesajları](/docs/specs/i2np)** - Çok atlamalı anonim yönlendirme için katmanlı şifreleme içeren protokol mesajları

## I2P Garlic Katmanı {#garlic}

Şifrelenmiş ve anonim uçtan uca I2P mesaj teslimatı sağlar:

- **[Garlic mesajları](/docs/overview/garlic-routing)** - Anonim teslimat için sarmalanmış I2NP mesajları

## I2P İstemci Katmanı {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol, uygulamaların router API'sini doğrudan kullanmak zorunda kalmadan I2P ağına erişmesine olanak tanır

## I2P Uçtan Uca Aktarım Katmanı {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - TCP'ye benzer şekilde güvenilir, sıralı teslimat sağlar
- **[Datagram Library](/docs/api/datagrams)** - UDP'ye benzer şekilde güvenilmez teslimat sağlar

## I2P Uygulama Arayüz Katmanı {#app-interface}

Uygulama geliştiricileri için isteğe bağlı arayüzler:

- **[I2PTunnel](/docs/api/i2ptunnel)** - TCP bağlantılarını I2P içine ve dışına tünel oluşturur
- **[SAMv3](/docs/api/samv3)** - Java olmayan uygulamalar için Basit Anonim Mesajlaşma protokolü

## I2P Uygulama Proxy Katmanı {#app-proxy}

Standart internet protokolleri için proxy'ler:

- **HTTP** - Web tarama proxy'si
- **IRC** - Internet Relay Chat proxy'si
- **[SOCKS](/docs/api/socks)** - SOCKS4/4a/5 proxy'si
- **Streamr** - UDP akış proxy'si

## Uygulamalar {#applications}

Uygulamalar I2P ile çeşitli katmanlarda arayüz oluşturabilir:

**Streaming/Datagram Uygulamaları:** - Streaming veya datagram kütüphanelerini doğrudan kullanan I2P-native uygulamalar

**SAM Uygulamaları:** - SAM protokolünü kullanan herhangi bir dildeki uygulamalar

**I2P'ye Özel Uygulamalar:** - I2P için özel olarak tasarlanmış uygulamalar (I2PSnark, SusiMail, vb.)

**Standart İnternet Uygulamaları:** - I2P proxy'leri kullanan normal uygulamalar (web tarayıcıları, IRC istemcileri, vb.)

## Yığın Diyagramı {#diagram}

![I2P Protocol Stack](/images/protocol_stack.png)

Not: SAM hem streaming kütüphanesini hem de datagramları kullanabilir.
