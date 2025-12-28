---
title: "BOB – Basic Open Bridge (Temel Açık Köprü)"
description: "Destination (I2P'de hedef/kimlik) yönetimi için kullanımdan kaldırılmış API (kullanımdan kaldırıldı)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Uyarı:** BOB yalnızca eski DSA-SHA1 imza türünü destekler. Java I2P, **1.7.0 (2022-02)** sürümünde BOB'u dağıtmayı bıraktı; BOB yalnızca 1.6.1 veya daha önceki sürümlerle başlatılmış kurulumlarda ve bazı i2pd derlemelerinde bulunmaktadır. Yeni uygulamalar [SAM v3](/docs/api/samv3/) **kullanmalıdır**.

## Dil Bağlamaları

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Protokol Notları

- `KEYS`, base64 bir destination'ı (I2P adresi; açık + özel anahtarlar) ifade eder.  
- `KEY`, base64 bir açık anahtardır.  
- `ERROR` yanıtları `ERROR <description>\n` biçimindedir.  
- `OK`, komutun tamamlandığını belirtir; isteğe bağlı veriler aynı satırda yer alır.  
- `DATA` satırları, son `OK`'tan önce ek çıktıyı akış halinde iletir.

`help` komutu tek istisnadır: “böyle bir komut yok” olduğunu bildirmek için hiçbir şey döndürmeyebilir.

## Bağlantı Karşılama Mesajı

BOB, satır sonu karakteriyle sonlandırılmış ASCII satırlar (LF veya CRLF) kullanır. Bağlantı kurulduğunda şunu gönderir:

```
BOB <version>
OK
```
Geçerli sürüm: `00.00.10`. Önceki yapılar büyük harfli onaltılık basamaklar ve standart dışı numaralandırma kullanırdı.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## Temel Komutlar

> Tam komut ayrıntıları için `telnet localhost 2827` kullanarak bağlanın ve `help` komutunu çalıştırın.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## Kullanımdan Kaldırma Özeti

- BOB modern imza türleri, şifrelenmiş LeaseSets veya taşıma katmanı özellikleri için destek sunmaz.
- API dondurulmuştur; yeni komutlar eklenmeyecektir.
- Hâlâ BOB'a dayanan uygulamalar mümkün olan en kısa sürede SAM v3'e geçmelidir.
