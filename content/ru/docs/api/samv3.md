---
title: "SAM v3"
description: "Стабильный мостовой протокол для приложений I2P на других языках программирования"
slug: "samv3"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

SAM v3 ("Simple Anonymous Messaging") — это текущий **стабильный, не зависящий от реализации router API**, который позволяет внешним приложениям взаимодействовать с сетью I2P без встраивания самого router. Он обеспечивает унифицированный доступ к **потокам**, **датаграммам** и **сырым сообщениям**, оставаясь каноническим связующим слоем для программного обеспечения, написанного не на Java.

## 1. Обзор и назначение

SAM v3 позволяет разработчикам создавать приложения для I2P на любом языке программирования, используя легковесный протокол TCP/UDP. Он абстрагирует внутреннее устройство router, предоставляя минимальный набор команд через TCP (7656) и UDP (7655). И **Java I2P**, и **i2pd** реализуют подмножества спецификации SAM v3, хотя в i2pd по состоянию на 2025 год всё ещё отсутствует большинство расширений версий 3.2 и 3.3.

## 2. История версий

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
### Примечание по именованию

- **Java I2P** использует `PRIMARY/SUBSESSION`.
- **i2pd** и **I2P+** продолжают использовать устаревшую терминологию `MASTER/SUBSESSION` для обратной совместимости.

## 3. Основной рабочий процесс

### Согласование версии

```
HELLO VERSION MIN=3.1 MAX=3.3
HELLO REPLY RESULT=OK VERSION=3.3
```
### Создание Destination

```
DEST GENERATE SIGNATURE_TYPE=7
```
- `SIGNATURE_TYPE=7` → **Ed25519 (EdDSA SHA512)**. Настоятельно рекомендуется с версии I2P 0.9.15.

### Создание сессии

```
SESSION CREATE STYLE=STREAM DESTINATION=NAME     OPTION=i2cp.leaseSetEncType=4,0     OPTION=inbound.quantity=3     OPTION=outbound.quantity=3
```
- `i2cp.leaseSetEncType=4,0` → `4` — это X25519 (ECIES X25519 AEAD Ratchet), а `0` — резервный вариант ElGamal для совместимости.
- Явные количества туннелей для согласованности: по умолчанию в Java I2P — **2**, в i2pd — **5**.

### Операции протокола

```
STREAM CONNECT ID=1 DESTINATION=b32address.i2p
STREAM SEND ID=1 SIZE=128
STREAM CLOSE ID=1
```
Основные типы сообщений включают: `STREAM CONNECT`, `STREAM ACCEPT`, `STREAM FORWARD`, `DATAGRAM SEND`, `RAW SEND`, `NAMING LOOKUP`, `DEST LOOKUP`, `PING`, `QUIT`.

### Плавное завершение работы

```
QUIT
```
## 4. Различия в реализации (Java I2P vs i2pd)

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
**Рекомендация:** Всегда явно указывайте количество туннелей, чтобы обеспечить согласованность между роутерами.

## 5. Поддерживаемые библиотеки (состояние на 2025 год)

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
## 6. Предстоящие и новые функции (2024–2025)

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
## 7. Замечания по безопасности и настройке

- Привязывайте SAM только к `127.0.0.1`.
- Для постоянных сервисов используйте **PRIMARY** сессии со статическими ключами.
- Используйте `HELLO VERSION` для проверки поддержки функций.
- Используйте `PING` или `NAMING LOOKUP` для проверки работоспособности router.
- Избегайте неаутентифицированных удалённых SAM-подключений (в i2pd нет TLS).

## 8. Ссылки и спецификации

- [Спецификация SAM v3](/docs/api/samv3/)
- [SAM v2 (устаревший)](/docs/legacy/samv2/)
- [Спецификация Streaming](/docs/specs/streaming/)
- [Датаграммы](/docs/api/datagrams/)
- [Центр документации](/docs/)
- [Документация i2pd](https://i2pd.website/docs)

## 9. Резюме

SAM v3 остаётся **рекомендуемым протоколом моста** для всех приложений I2P, не использующих Java. Он обеспечивает стабильность, межъязыковые привязки и стабильную производительность на различных типах router.

При разработке с SAM: - Используйте подписи **Ed25519** и шифрование **X25519**. - Проверяйте поддержку функций динамически через `HELLO VERSION`. - Проектируйте с учётом совместимости, особенно при поддержке как Java I2P, так и i2pd router'ов.
