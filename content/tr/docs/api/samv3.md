---
title: "SAM v3"
description: "Java olmayan I2P uygulamaları için kararlı köprü protokolü"
slug: "samv3"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SAM v3 ("Simple Anonymous Messaging"), harici uygulamaların router'ı kendilerine gömmeden I2P ağı ile iletişim kurmasına olanak tanıyan mevcut **kararlı, router bağımsız API**'dir. **Akışlar**, **datagramlar** ve **ham mesajlar**'a birleşik erişim sağlar ve Java dışı yazılımlar için standart köprü katmanı olmaya devam eder.

## 1. Genel Bakış ve Amaç

SAM v3, geliştiricilerin hafif bir TCP/UDP protokolü kullanarak herhangi bir dilde I2P uyumlu yazılım oluşturmasını sağlar. Router iç yapısını soyutlayarak, TCP (7656) ve UDP (7655) üzerinden minimal bir komut seti sunar. Hem **Java I2P** hem de **i2pd**, SAM v3 spesifikasyonunun alt kümelerini uygular, ancak i2pd 2025 itibariyle hala çoğu 3.2 ve 3.3 uzantısından yoksundur.

## 2. Sürüm Geçmişi

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.7.3 (May 2009)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Streams + Datagrams; binary destinations; `SESSION CREATE STYLE=` parameter.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.1</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.14 (Jul 2014)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature type negotiation via `SIGNATURE_TYPE`; improved `DEST GENERATE`.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.24 (Jan 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per session encryption + tunnel options; `STREAM CONNECT ID` support.</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>3.3</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.25 (Mar 2016)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY / SUBSESSION architecture; multiplexing; improved datagrams.</td></tr>
  </tbody>
</table>
### İsimlendirme Notu

- **Java I2P** `PRIMARY/SUBSESSION` kullanır.
- **i2pd** ve **I2P+** geriye dönük uyumluluk için eski `MASTER/SUBSESSION` terminolojisini kullanmaya devam eder.

## 3. Temel İş Akışı

### Sürüm Görüşmesi

```
HELLO VERSION MIN=3.1 MAX=3.3
HELLO REPLY RESULT=OK VERSION=3.3
```
### Hedef Oluşturma

```
DEST GENERATE SIGNATURE_TYPE=7
```
- `SIGNATURE_TYPE=7` → **Ed25519 (EdDSA SHA512)**. I2P 0.9.15'ten itibaren şiddetle önerilir.

### Oturum Oluşturma

```
SESSION CREATE STYLE=STREAM DESTINATION=NAME     OPTION=i2cp.leaseSetEncType=4,0     OPTION=inbound.quantity=3     OPTION=outbound.quantity=3
```
- `i2cp.leaseSetEncType=4,0` → `4` X25519'dur (ECIES X25519 AEAD Ratchet) ve `0` uyumluluk için ElGamal yedektir.
- Tutarlılık için açık tünel miktarları: Java I2P varsayılanı **2**, i2pd varsayılanı **5**.

### Protokol İşlemleri

```
STREAM CONNECT ID=1 DESTINATION=b32address.i2p
STREAM SEND ID=1 SIZE=128
STREAM CLOSE ID=1
```
Temel mesaj türleri şunları içerir: `STREAM CONNECT`, `STREAM ACCEPT`, `STREAM FORWARD`, `DATAGRAM SEND`, `RAW SEND`, `NAMING LOOKUP`, `DEST LOOKUP`, `PING`, `QUIT`.

### Zarif Kapatma

```
QUIT
```
## 4. Uygulama Farklılıkları (Java I2P vs i2pd)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Java I2P 2.10.0</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">i2pd 2.58.0 (Sept&nbsp;2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SAM enabled by default</td><td style="border:1px solid var(--color-border); padding:0.5rem;">❌ Requires manual enable in router console</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✅ Enabled via `enabled=true` in `i2pd.conf`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default ports</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP 7656 / UDP 7655</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Same</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">AUTH / USER / PASSWORD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PING / PONG keepalive</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">QUIT / STOP / EXIT commands</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">FROM_PORT / TO_PORT / PROTOCOL</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PRIMARY/SUBSESSION support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 0.9.47)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Absent</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SESSION ADD / REMOVE</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 support</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ (since 2.9.0)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ Not implemented</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSL/TLS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✗ None</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Default tunnel quantities</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Inbound/outbound=5</td></tr>
  </tbody>
</table>
**Öneri:** Router'lar arası tutarlılığı sağlamak için tunnel miktarlarını her zaman açıkça belirtin.

## 5. Desteklenen Kütüphaneler (2025 Anlık Görünümü)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maintenance Status (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">libsam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Maintained by I2P Project (eyedeekay)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">i2psam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal updates since 2019</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/sam3">sam3</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active; migrated from `eyedeekay/sam3`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/go-i2p/onramp">onramp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actively maintained (2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2plib">i2plib</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Modern async replacement for `i2p.socket`</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">i2p.socket</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Abandoned (last release 2017)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://i2pgit.org/robin/Py2p">Py2p</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unverified/inactive</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">i2p-rs</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental; unstable API</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">@diva.exchange/i2p-sam</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">TypeScript / JS</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Most actively maintained (2024–2025)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/I2PSharp">I2PSharp</a></td><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Functional; light maintenance</td></tr>
  </tbody>
</table>
## 6. Yaklaşan ve Yeni Özellikler (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NAMING LOOKUP `OPTIONS=true`</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ Supported</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2 / Datagram3 formats</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✓ (Java only)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid crypto (ML KEM)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Optional</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java 17+ runtime requirement</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Planned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.11.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P over Tor blocking</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Improved floodfill selection</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Active</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0+</td></tr>
  </tbody>
</table>
## 7. Güvenlik ve Yapılandırma Notları

- SAM'ı yalnızca `127.0.0.1` adresine bağlayın.
- Kalıcı servisler için statik anahtarlarla **PRIMARY** oturumları kullanın.
- Özellik desteğini test etmek için `HELLO VERSION` kullanın.
- Router canlılığını doğrulamak için `PING` veya `NAMING LOOKUP` kullanın.
- Kimlik doğrulamasız uzak SAM bağlantılarından kaçının (i2pd'de TLS yok).

## 8. Referanslar ve Özellikler

- [SAM v3 Spesifikasyonu](/docs/api/samv3/)
- [SAM v2 (Eski)](/docs/legacy/samv2/)
- [Streaming Spesifikasyonu](/docs/specs/streaming/)
- [Datagram'lar](/docs/api/datagrams/)
- [Dokümantasyon Merkezi](/docs/)
- [i2pd Dokümantasyonu](https://i2pd.website/docs)

## 9. Özet

SAM v3, Java olmayan tüm I2P uygulamaları için **önerilen köprü protokolü** olmaya devam etmektedir. Kararlılık, diller arası bağlantılar ve router türleri arasında tutarlı performans sunar.

SAM ile geliştirme yaparken: - **Ed25519** imzalarını ve **X25519** şifrelemeyi kullanın. - `HELLO VERSION` aracılığıyla özellik desteğini dinamik olarak doğrulayın. - Özellikle hem Java I2P hem de i2pd router'larını desteklerken uyumluluk için tasarım yapın.
