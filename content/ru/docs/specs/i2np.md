---
title: "Сетевой протокол I2P (I2NP)"
description: "Форматы сообщений router-to-router, приоритеты и ограничения по размеру в I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

Сетевой протокол I2P (I2NP) определяет, как routers обмениваются сообщениями, выбирают транспорты и перемешивают трафик при сохранении анонимности. Он функционирует между **I2CP** (клиентским API) и транспортными протоколами (**NTCP2** и **SSU2**).

I2NP — это уровень выше транспортных протоколов I2P. Это протокол уровня router-to-router (взаимодействия между router), используемый для: - Запросов к сетевой базе данных и ответов - Создания tunnels - Зашифрованных сообщений с данными для router и клиента

Сообщения I2NP могут быть отправлены по схеме «точка-точка» к другому router или анонимно через tunnels к тому router.

Router помещает исходящие задания в очередь, используя локальные приоритеты. Более высокие номера приоритетов обрабатываются первыми. Всё, что выше стандартного приоритета данных tunnel (400), считается срочным.

### Текущие транспорты

I2P теперь использует **NTCP2** (TCP) и **SSU2** (UDP) как для IPv4, так и для IPv6. Оба транспортных протокола используют: - **X25519** для обмена ключами (фреймворк протоколов Noise) - **ChaCha20/Poly1305** для аутентифицированного шифрования (AEAD) - **SHA-256** для хэширования

**Устаревшие транспорты удалены:** - NTCP (оригинальный TCP) был удалён из Java router в релизе 0.9.50 (май 2021) - SSU v1 (оригинальный UDP) был удалён из Java router в релизе 2.4.0 (декабрь 2023) - SSU v1 был удалён из i2pd в релизе 2.44.0 (ноябрь 2022)

По состоянию на 2025 год сеть полностью перешла на транспорты на основе Noise (фреймворка криптографических протоколов) без какой-либо поддержки устаревших транспортов.

---

## Система нумерации версий

**ВАЖНО:** В I2P используется двойная система версионирования, которую необходимо чётко понимать:

### Релизные версии (для пользователей)

Это версии, которые пользователи видят и скачивают: - 0.9.50 (май 2021) - Последний релиз ветки 0.9.x - **1.5.0** (август 2021) - Первый релиз ветки 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (в 2021–2022 гг.) - **2.0.0** (ноябрь 2022) - Первый релиз ветки 2.x - с 2.1.0 по 2.9.0 (в 2023–2025 гг.) - **2.10.0** (8 сентября 2025) - Текущий релиз

### Версии API (совместимость протоколов)

Это внутренние номера версий, публикуемые в поле "router.version" в свойствах RouterInfo (структура с информацией о router): - 0.9.50 (май 2021) - **0.9.51** (август 2021) - версия API для релиза 1.5.0 - с 0.9.52 по 0.9.66 (продолжается в релизах 2.x) - **0.9.67** (сентябрь 2025) - версия API для релиза 2.10.0

**Ключевой момент:** Не было НИКАКИХ релизов с номерами 0.9.51–0.9.67. Эти номера существуют только как идентификаторы версии API. I2P перешёл с релиза 0.9.50 напрямую на 1.5.0.

### Таблица соответствия версий

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Скоро:** Релиз 2.11.0 (запланирован на декабрь 2025 года) потребует Java 17+ и по умолчанию включит постквантовую криптографию.

---

## Версии протоколов

Все router должны публиковать свою версию протокола I2NP в поле "router.version" в свойствах RouterInfo. Это поле — версия API, указывающая уровень поддержки различных функций протокола I2NP, и оно не обязательно совпадает с фактической версией router.

Альтернативные (не на Java) routers, если они желают публиковать какую-либо информацию о версии конкретной реализации router, должны делать это в другом свойстве. Допускаются версии, отличные от перечисленных ниже. Поддержка будет определяться на основе численного сравнения; например, 0.9.13 означает поддержку возможностей 0.9.12.

**Примечание:** Свойство "coreVersion" больше не публикуется в информации о router и никогда не использовалось для определения версии протокола I2NP.

### Сводка возможностей версий API

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Примечание:** Существуют также особенности, связанные с транспортом, и вопросы совместимости. Подробнее см. документацию по транспортам NTCP2 и SSU2.

---

## Заголовок сообщения

I2NP использует логическую структуру 16-байтового заголовка, тогда как современные транспортные протоколы (NTCP2 и SSU2) используют укороченный 9-байтовый заголовок, исключающий избыточные поля размера и контрольной суммы. Поля остаются концептуально идентичными.

### Сравнение форматов заголовков

**Стандартный формат (16 байт):**

Используется в устаревшем транспорте NTCP и когда сообщения I2NP инкапсулируются в другие сообщения (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Короткий формат для SSU (устаревший, 5 байт):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Краткий формат для NTCP2, SSU2 и ECIES-Ratchet Garlic Cloves (дольки в терминологии garlic encryption) (9 байт):**

Используется в современных транспортных протоколах и в garlic-сообщениях (сообщениях, объединяющих несколько сообщений), зашифрованных с помощью ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Сведения о полях заголовка

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Примечания по реализации

- При передаче по SSU (устаревший) включались только тип и 4-байтовое значение срока действия
- При передаче по NTCP2 или SSU2 используется 9-байтовый короткий формат
- Стандартный 16-байтовый заголовок обязателен для сообщений I2NP, вложенных в другие сообщения (Data, TunnelData, TunnelGateway, GarlicClove)
- Начиная с версии 0.8.12, проверка контрольной суммы в некоторых местах стека протокола отключена для повышения эффективности, но генерация контрольной суммы по-прежнему требуется для совместимости
- Короткое поле срока действия является беззнаковым и переполнится 7 февраля 2106 года. После этой даты для получения корректного времени необходимо добавлять смещение
- Для совместимости со старыми версиями всегда генерируйте контрольные суммы, даже если они могут не проверяться

---

## Ограничения по размеру

Сообщения tunnel фрагментируют полезную нагрузку I2NP на фрагменты фиксированного размера: - **Первый фрагмент:** приблизительно 956 байт - **Последующие фрагменты:** приблизительно по 996 байт каждый - **Максимум фрагментов:** 64 (пронумерованы 0-63) - **Максимальная полезная нагрузка:** приблизительно 61,200 байт (61.2 KB)

**Расчёт:** 956 + (63 × 996) = 63,704 байт — теоретический максимум, при практическом ограничении около 61,200 байт из-за накладных расходов.

### Исторический контекст

Старые транспортные протоколы имели более строгие ограничения на размер кадра: - NTCP: кадры размером 16 КБ - SSU: кадры примерно по 32 КБ

NTCP2 поддерживает фреймы размером примерно 65 КБ, но лимит фрагментации tunnel по‑прежнему применяется.

### Соображения по данным приложения

Garlic messages (чесночные сообщения) могут объединять LeaseSets, теги сессии или зашифрованные варианты LeaseSet2, уменьшая доступное место для полезной нагрузки.

**Рекомендация:** Датаграммы следует оставлять ≤ 10 KB для обеспечения надежной доставки. Сообщения, приближающиеся к пределу 61 KB, могут столкнуться со следующим: - Повышенная задержка из-за сборки после фрагментации - Повышенная вероятность недоставки - Большая подверженность анализу трафика

### Технические детали фрагментации

Каждое сообщение tunnel имеет размер ровно 1,024 байта (1 КБ) и содержит: - 4-байтовый ID tunnel - 16-байтовый вектор инициализации (IV) - 1,004 байта зашифрованных данных

Внутри зашифрованных данных, сообщения tunnel переносят фрагментированные сообщения I2NP с заголовками фрагментов, указывающими: - Номер фрагмента (0-63) - Является ли это первым или последующим фрагментом - Идентификатор всего сообщения для сборки

Первый фрагмент включает полный заголовок сообщения I2NP (16 байт), оставляя примерно 956 байт для полезной нагрузки. Последующие фрагменты не включают заголовок сообщения, что позволяет разместить примерно по 996 байт полезной нагрузки на фрагмент.

---

## Распространенные типы сообщений

Routers используют тип сообщения и приоритет для планирования исходящих операций. Значения с более высоким приоритетом обрабатываются первыми. Приведённые ниже значения соответствуют текущим значениям по умолчанию в Java I2P (по состоянию на версию API 0.9.67).

**Примечание:** Приоритеты зависят от реализации. За эталонными значениями приоритетов обратитесь к документации класса `OutNetMessage` в исходном коде Java I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Зарезервированные типы сообщений:** - Тип 0: Зарезервирован - Типы 4-9: Зарезервированы для будущего использования - Типы 12-17: Зарезервированы для будущего использования - Типы 224-254: Зарезервированы для экспериментальных сообщений - Тип 255: Зарезервирован для будущего расширения

### Примечания к типу сообщения

- Сообщения управляющей плоскости (DatabaseLookup, TunnelBuild и т. д.) обычно проходят через **исследовательские tunnels**, а не через клиентские tunnels, что позволяет назначать им независимые приоритеты
- Значения приоритета являются ориентировочными и могут различаться в зависимости от реализации
- TunnelBuild (21) и TunnelBuildReply (22) считаются устаревшими, но по-прежнему реализованы для совместимости с очень длинными tunnels (>8 хопов)
- Стандартный приоритет данных в tunnel — 400; все, что выше, рассматривается как срочное
- Типичная длина tunnel в текущей сети составляет 3–4 хопа, поэтому для построения большинства tunnels используются ShortTunnelBuild (218-байтовые записи) или VariableTunnelBuild (528-байтовые записи)

---

## Шифрование и обертывание сообщений

Routers часто инкапсулируют сообщения I2NP перед передачей, создавая несколько уровней шифрования. Сообщение DeliveryStatus может быть: 1. Заключено в GarlicMessage (зашифровано) 2. Внутри DataMessage 3. Внутри сообщения TunnelData (повторно зашифровано)

Каждый промежуточный узел расшифровывает только свой слой; конечный адресат получает доступ к самой внутренней полезной нагрузке.

### Алгоритмы шифрования

**Устаревшее (поэтапно выводится из эксплуатации):** - ElGamal/AES + SessionTags (теги сеанса) - ElGamal-2048 для асимметричного шифрования - AES-256 для симметричного шифрования - 32-байтовые SessionTags

**Текущее (стандарт по состоянию на API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD с ratcheting forward secrecy (механизм последовательного обновления ключей, обеспечивающий прямую секретность) - Фреймворк протокола Noise (Noise_IK_25519_ChaChaPoly_SHA256 для назначений) - 8-байтовые сеансовые теги (уменьшено с 32 байт) - Алгоритм Signal Double Ratchet для обеспечения прямой секретности - Введено в версии API 0.9.46 (2020) - Обязательно для всех routers начиная с версии API 0.9.58 (2023)

**Будущее (бета начиная с 2.10.0):** - Постквантовая гибридная криптография с использованием MLKEM (ML-KEM-768) в сочетании с X25519 - Гибридный ratchet (механизм пошагового обновления ключей), объединяющий классическое и постквантовое согласование ключей - Обратная совместимость с ECIES-X25519 - Станет настройкой по умолчанию в релизе 2.11.0 (декабрь 2025)

### Объявление ElGamal Router устаревшим

**CRITICAL:** ElGamal routers были объявлены устаревшими начиная с версии API 0.9.58 (релиз 2.2.0, март 2023). Поскольку рекомендуемая минимальная версия floodfill для запросов теперь 0.9.58, реализациям нет необходимости поддерживать шифрование для ElGamal floodfill routers.

**Однако:** назначения ElGamal по-прежнему поддерживаются для обратной совместимости. Клиенты, использующие шифрование ElGamal, по-прежнему могут обмениваться данными через ECIES routers.

### Подробности ECIES-X25519-AEAD-Ratchet

Это тип криптографии 4 в криптографической спецификации I2P. Он обеспечивает:

**Ключевые особенности:** - Прямая секретность благодаря ratcheting (механизм ратчета; новые ключи для каждого сообщения) - Сокращённое хранение меток сеанса (8 байт против 32 байт) - Несколько типов сеансов (Новый сеанс, Существующий сеанс, Одноразовый) - Основано на протоколе Noise Noise_IK_25519_ChaChaPoly_SHA256 - Интегрировано с алгоритмом Double Ratchet от Signal

**Криптографические примитивы:** - X25519 для согласования ключей Диффи-Хеллмана - ChaCha20 для потокового шифрования - Poly1305 для аутентификации сообщений (AEAD) - SHA-256 для хеширования - HKDF для вывода ключей

**Управление сеансами:** - Новый сеанс: Первичное подключение с использованием статического ключа назначения - Существующий сеанс: Последующие сообщения с использованием тегов сеанса - Одноразовый сеанс: Одно сообщение в сеансе для снижения накладных расходов

См. [спецификацию ECIES](/docs/specs/ecies/) и [Предложение 144](/proposals/144-ecies-x25519-aead-ratchet/) для получения полных технических сведений.

---

## Общие структуры

Следующие структуры являются элементами нескольких сообщений I2NP. Они не являются полными сообщениями.

### BuildRequestRecord (запись запроса построения) (ElGamal)

**УСТАРЕЛО.** Используется в текущей сети только если tunnel содержит ElGamal router. См. [ECIES Tunnel Creation](/docs/specs/implementation/) для современного формата.

**Назначение:** Одна запись в наборе из нескольких записей для запроса создания одного хопа в tunnel.

**Формат:**

Зашифровано с использованием ElGamal и AES (всего 528 байт):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
Структура, зашифрованная алгоритмом Эль-Гамаля (528 байт):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Структура незашифрованных данных (222 байта до шифрования):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Примечания:** - Шифрование ElGamal-2048 производит блок размером 514 байт, но два байта заполнения (в позициях 0 и 257) удаляются, в результате — 512 байт - См. [Спецификацию создания tunnel](/docs/specs/implementation/) для подробностей о полях - Исходный код: `net.i2p.data.i2np.BuildRequestRecord` - Константа: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (запись запроса на построение) (ECIES-X25519 Long)

Для ECIES-X25519 routers, представленных в версии API 0.9.48. Использует 528 байт для обеспечения обратной совместимости со смешанными tunnels.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Общий размер:** 528 байт (такой же, как у ElGamal, для совместимости)

См. [ECIES Tunnel Creation](/docs/specs/implementation/) для сведений о структуре открытого текста и подробностях шифрования.

### BuildRequestRecord (ECIES-X25519, короткий)

Только для routers ECIES-X25519, начиная с версии API 0.9.51 (релиз 1.5.0). Это текущий стандартный формат.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Общий размер:** 218 байт (снижение на 59% по сравнению с 528 байтами)

**Ключевое отличие:** Короткие записи получают ВСЕ ключи с помощью HKDF (функция выработки ключей), вместо того чтобы включать их явно в запись. Это включает: - Ключи слоя (для шифрования tunnel) - Ключи IV (для шифрования tunnel) - Ключи ответа (для build reply (ответа на построение)) - IV ответа (для build reply)

Все ключи выводятся с использованием механизма HKDF протокола Noise на основе общего секрета, полученного в результате обмена ключами X25519.

**Преимущества:** - 4 короткие записи умещаются в одном сообщении tunnel (873 байта) - 3 сообщения построения tunnel вместо отдельных сообщений для каждой записи - Снижены трафик и задержка - Те же свойства безопасности, что и у длинного формата

См. [Предложение 157](/proposals/157-new-tbm/) для обоснования и [Создание ECIES Tunnel](/docs/specs/implementation/) для полной спецификации.

**Исходный код:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Константа: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (запись ответа на построение, ElGamal)

**УСТАРЕЛО.** Используется только, если tunnel содержит ElGamal router.

**Назначение:** Отдельная запись в наборе из нескольких записей, содержащих ответы на запрос на построение.

**Формат:**

Зашифрованные данные (528 байт, тот же размер, что и BuildRequestRecord):

```
bytes 0-527 :: AES-encrypted record
```
Незашифрованная структура:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Коды ответа:** - `0` - Принято - `30` - Отклонено (превышение пропускной способности)

См. [Спецификацию создания tunnel](/docs/specs/implementation/) для подробностей о поле ответа.

### BuildResponseRecord (ECIES-X25519)

Для ECIES-X25519 routers — версия API 0.9.48+. Того же размера, что и соответствующий запрос (528 для длинного, 218 для короткого).

**Формат:**

Длинный формат (528 байт):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Короткий формат (218 байт):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Структура открытого текста (в обоих форматах):**

Содержит структуру Mapping (формат ключ-значение I2P) с:
- Код состояния ответа (обязательно)
- Параметр доступной пропускной способности ("b") (необязательно, добавлено в API 0.9.65)
- Другие необязательные параметры для будущих расширений

**Коды состояния ответа:** - `0` - Успех - `30` - Отклонено: превышение пропускной способности

См. [Создание ECIES Tunnel](/docs/specs/implementation/) для ознакомления с полной спецификацией.

### GarlicClove (долька сообщения «garlic»; ElGamal/AES)

**ПРЕДУПРЕЖДЕНИЕ:** Это формат, используемый для долек внутри чесночных сообщений, зашифрованных с помощью ElGamal. Формат чесночных сообщений и долек в ECIES-AEAD-X25519-Ratchet существенно отличается. См. [Спецификацию ECIES](/docs/specs/ecies/) для современного формата.

**Устарело для routers (API 0.9.58+), по-прежнему поддерживается для назначений.**

**Формат:**

Без шифрования:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```

См. [Garlic Routing](/docs/overview/garlic-routing/) (маршрутизация Garlic в I2P) для концептуального обзора.

### GarlicClove (долька garlic-сообщения) (ECIES-X25519-AEAD-Ratchet)

Для ECIES-X25519 routers и назначений — версия API 0.9.46+. Это текущий стандартный формат.

**ПРИНЦИПИАЛЬНОЕ ОТЛИЧИЕ:** ECIES garlic (механизм «чесночных» сообщений в I2P) использует совершенно иную структуру, основанную на блоках протокола Noise, а не на явных структурах clove (долек).

**Формат:**

Чесночные сообщения ECIES состоят из ряда блоков:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Типы блоков:** - `0` - Блок Garlic Clove (долька чеснока; содержит сообщение I2NP) - `1` - Блок даты и времени (метка времени) - `2` - Блок параметров (параметры доставки) - `3` - Блок заполнения - `254` - Блок завершения (не реализовано)

**Garlic Clove Block (блок «дольки чеснока», type 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Ключевые отличия от формата ElGamal:** - Использует 4-байтовое поле истечения (секунды с начала эпохи) вместо 8-байтового Date - Нет поля сертификата - Заключено в блочную структуру с типом и длиной - Сообщение целиком зашифровано с использованием ChaCha20/Poly1305 AEAD - Управление сессией через ratcheting (последовательное обновление ключей)

См. [спецификацию ECIES](/docs/specs/ecies/) для подробной информации о Noise Protocol Framework (фреймворк протокола Noise) и структурах блоков.

### Инструкции по доставке Garlic Clove (долька в garlic encryption)

Этот формат используется как для чесночных долек ElGamal, так и ECIES. В нём задаётся способ доставки вложенного сообщения.

**КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:** Эта спецификация предназначена ТОЛЬКО для "инструкций доставки" внутри Garlic Cloves (дольки чесночного сообщения). "Инструкции доставки" также используются внутри сообщений Tunnel, где формат существенно отличается. См. [Спецификацию сообщений Tunnel](/docs/specs/implementation/) для инструкций доставки tunnel. НЕ путайте эти два формата.

**Формат:**

Сеансовый ключ и задержка не используются и никогда не передаются, поэтому возможны три длины: - 1 байт (LOCAL) - 33 байта (ROUTER и DESTINATION) - 37 байт (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Типичные длины:** - ЛОКАЛЬНАЯ доставка: 1 байт (только флаг) - ROUTER / DESTINATION доставка: 33 байта (флаг + хеш) - TUNNEL доставка: 37 байт (флаг + хеш + tunnel ID)

**Описания типов доставки:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Примечания по реализации:** - Шифрование сеансового ключа не реализовано, и бит флага всегда равен 0 - Задержка реализована не полностью, и бит флага всегда равен 0 - Для доставки TUNNEL хэш идентифицирует шлюзовой router, а ID tunnel указывает, какой входящий tunnel - Для доставки DESTINATION (назначение), хэш — это SHA-256 публичного ключа назначения - Для доставки ROUTER хэш — это SHA-256 идентификатора router

---

## Сообщения I2NP

Полные спецификации для всех типов сообщений I2NP.

### Сводка типов сообщений

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Зарезервировано:** - Тип 0: зарезервирован - Типы 4-9: зарезервированы для будущего использования - Типы 12-17: зарезервированы для будущего использования - Типы 224-254: зарезервированы для экспериментальных сообщений - Тип 255: зарезервирован для будущего расширения

---

### DatabaseStore (тип 1)

**Назначение:** Незапрошенное сохранение в базе данных или ответ на успешный запрос DatabaseLookup (поиск в базе данных).

**Содержимое:** Несжатый LeaseSet, LeaseSet2, MetaLeaseSet или EncryptedLeaseSet, либо сжатый RouterInfo (информация о router).

**Формат с токеном ответа:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Формат при токене ответа == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**Примечания:** - В целях безопасности поля ответа игнорируются, если сообщение получено через tunnel - Ключ — это «реальный» хэш от RouterIdentity или Destination, а НЕ ключ маршрутизации - Типы 3, 5 и 7 (варианты LeaseSet2) были добавлены в выпуске 0.9.38 (API 0.9.38). См. [Предложение 123](/proposals/123-new-netdb-entries/) для подробностей - Эти типы следует отправлять только на routers с версией API 0.9.38 или выше - В качестве оптимизации для сокращения числа соединений: если тип — LeaseSet, включён токен ответа, ID ответного tunnel не равен нулю, и пара reply gateway/tunnelID найдена в LeaseSet как lease (элемент LeaseSet), получатель может перенаправить ответ на любой другой lease в LeaseSet - **Формат gzip RouterInfo:** Чтобы скрыть ОС и реализацию router, приведите формат к реализации router на Java, установив время модификации равным 0 и байт ОС — 0xFF, а XFL — 0x02 (максимальное сжатие, самый медленный алгоритм) согласно RFC 1952. Первые 10 байт: `1F 8B 08 00 00 00 00 00 02 FF`

**Исходный код:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (для структуры RouterInfo) - `net.i2p.data.LeaseSet` (для структуры LeaseSet)

---

### DatabaseLookup (Тип 2)

**Назначение:** Запрос на поиск записи в сетевой базе данных (netDb). Ответом будет либо DatabaseStore, либо DatabaseSearchReply.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Режимы шифрования ответов:**

**ПРИМЕЧАНИЕ:** ElGamal routers признаны устаревшими с версии API 0.9.58. Поскольку рекомендуемая минимальная версия floodfill для запросов теперь 0.9.58, реализациям не требуется реализовывать шифрование для ElGamal floodfill routers. Назначения ElGamal по‑прежнему поддерживаются.

Бит 4 флага (ECIESFlag) используется в сочетании с битом 1 (encryptionFlag) для определения режима шифрования ответа:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Без шифрования (флаги 0,0):**

reply_key, tags и reply_tags отсутствуют.

**ElG в ElG (флаги 0,1) - УСТАРЕВШЕЕ:**

Поддерживается начиная с 0.9.7, объявлено устаревшим начиная с 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES в ElG (флаги 1,0) - УСТАРЕЛО:**

Поддерживается с версии 0.9.46, помечено как устаревшее с версии 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
Ответ представляет собой сообщение ECIES Existing Session (существующий сеанс), как определено в [спецификации ECIES](/docs/specs/ecies/):

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES в ECIES (flags 1,0) - ТЕКУЩИЙ СТАНДАРТ:**

ECIES Destination (адрес назначения) или router отправляет запрос на поиск к ECIES router. Поддерживается начиная с 0.9.49.

Такой же формат, как у "ECIES to ElG" выше. Шифрование сообщения поиска определено в [ECIES Routers](/docs/specs/ecies/#routers). Запрашивающий анонимен.

**ECIES (схема шифрования на эллиптических кривых) в ECIES с DH (алгоритм Диффи — Хеллмана) (флаги 1,1) - БУДУЩЕЕ:**

Ещё не полностью определено. См. [Предложение 156](/proposals/156-ecies-routers/).

**Примечания:** - До версии 0.9.16 ключ мог относиться к RouterInfo или LeaseSet (одно и то же пространство ключей, нет флага для различения) - Зашифрованные ответы полезны только когда ответ проходит через tunnel - Число включённых тегов может быть больше одного, если реализованы альтернативные стратегии поиска в DHT - Ключ поиска и ключи исключения — это "реальные" хэши, НЕ маршрутизационные ключи - Типы 3, 5 и 7 (варианты LeaseSet2) могут возвращаться начиная с 0.9.38. См. [Proposal 123](/proposals/123-new-netdb-entries/) - **Примечания по exploratory lookup (исследовательский поиск):** exploratory lookup определяется как возвращающий список не-floodfill хэшей, близких к ключу. Однако реализации различаются: Java действительно выполняет поиск по ключу RI и, если он есть, возвращает DatabaseStore (сообщение I2NP); i2pd — нет. Поэтому не рекомендуется использовать exploratory lookup для ранее полученных хэшей

**Исходный код:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Шифрование: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Тип 3)

**Назначение:** Ответ на неудавшийся запрос DatabaseLookup (поиск в базе данных).

**Содержимое:** Список хэшей router, ближайших к запрошенному ключу.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Примечания:** - Хэш 'from' не аутентифицирован и ему нельзя доверять - Возвращаемые хэши узлов не обязательно ближе к ключу, чем запрашиваемый router. В ответах на обычные запросы это облегчает обнаружение новых floodfills и "обратный" поиск (дальше от ключа) для повышения устойчивости - Для исследовательских запросов ключ обычно генерируется случайно. Не-floodfill peer_hashes в ответе могут отбираться с использованием оптимизированного алгоритма (например, близкие, но не обязательно самые близкие узлы), чтобы избежать неэффективной сортировки всей локальной базы данных. Также могут использоваться стратегии кэширования. Это зависит от реализации - **Типичное количество возвращаемых хэшей:** 3 - **Рекомендуемое максимальное количество возвращаемых хэшей:** 16 - Ключ поиска, хэши узлов и хэш 'from' являются "реальными" хэшами, НЕ ключами маршрутизации - Если num равно 0, это означает, что более близкие узлы не найдены (тупик)

**Исходный код:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (тип 10)

**Назначение:** Простое подтверждение получения сообщения. Обычно создаётся отправителем сообщения и помещается в Garlic Message (тип сообщения «Garlic») вместе с самим сообщением, для последующего возврата получателем.

**Содержимое:** Идентификатор доставленного сообщения и время создания или поступления.

**Формат:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Примечания:** - Метка времени всегда устанавливается создателем на текущее время. Однако в коде есть несколько мест, где это используется, и в будущем их может стать больше - Это сообщение также используется как подтверждение установления сессии в SSU. В этом случае ID сообщения устанавливается в случайное число, а "время прибытия" устанавливается равным текущему общесетевому идентификатору, который равен 2 (т. е., `0x0000000000000002`) - DeliveryStatus (тип сообщения I2NP для подтверждения доставки) обычно оборачивается в GarlicMessage (агрегированное garlic-сообщение) и отправляется через tunnel, чтобы предоставить подтверждение, не раскрывая отправителя - Используется для тестирования tunnel с целью измерения задержки и надежности

**Исходный код:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Используется в: `net.i2p.router.tunnel.InboundEndpointProcessor` для тестирования tunnel

---

### GarlicMessage (сообщение I2NP «Garlic», тип 11)

**ПРЕДУПРЕЖДЕНИЕ:** Это формат, используемый для garlic messages (тип сообщений в I2P, в которых несколько сообщений объединяются в один), зашифрованных с помощью ElGamal. Формат для ECIES-AEAD-X25519-Ratchet garlic messages существенно отличается. См. [ECIES Specification](/docs/specs/ecies/) для современного формата.

**Назначение:** Используется для инкапсуляции нескольких зашифрованных сообщений I2NP.

**Содержимое:** после расшифрования — совокупность Garlic Cloves (долек) и дополнительных данных, также известная как Clove Set (набор долек).

**Зашифрованный формат:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Расшифрованные данные (Clove Set — набор долек):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
**Notes:** - When unencrypted, data contains one or more Garlic Cloves - The AES encrypted block is padded to a minimum of 128 bytes; with the 32-byte Session Tag, the minimum size of the encrypted message is 160 bytes; with the 4-byte length field, the minimum size of the Garlic Message is 164 bytes - Actual max length is less than 64 KB (practical limit around 61.2 KB for tunnel messages) - See [ElGamal/AES Specification](/docs/legacy/elgamal-aes/) for encryption details - See [Garlic Routing](/docs/overview/garlic-routing/) for conceptual overview - The 128 byte minimum size of the AES encrypted block is not currently configurable - The message ID is generally set to a random number on transmit and appears to be ignored on receive - The certificate could possibly be used for HashCash to "pay" for routing (future possibility) - **ElGamal encryption structure:** 32-byte session tag + ElGamal-encrypted session key + AES-encrypted payload

**Для формата ECIES-X25519-AEAD-Ratchet (текущий стандарт для routers):**

См. [спецификацию ECIES](/docs/specs/ecies/) и [предложение 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Исходный код:** - `net.i2p.data.i2np.GarlicMessage` - Шифрование: `net.i2p.crypto.elgamal.ElGamalAESEngine` (устарело) - Современное шифрование: `net.i2p.crypto.ECIES` пакеты

---

### TunnelData (Тип 18)

**Назначение:** Сообщение, отправляемое со шлюза tunnel или его участника к следующему участнику или конечной точке. Данные имеют фиксированную длину и содержат сообщения I2NP, которые фрагментируются, пакетируются, дополняются и шифруются.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Структура полезной нагрузки (1024 байта):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Примечания:** - ID сообщения I2NP для TunnelData устанавливается в новое случайное значение на каждом переходе - Формат сообщения tunnel (внутри зашифрованных данных) определён в [Спецификации сообщений tunnel](/docs/specs/implementation/) - Каждый переход расшифровывает один слой с использованием AES-256 в режиме CBC - Вектор инициализации (IV) обновляется на каждом переходе с использованием расшифрованных данных - Общий размер ровно 1,028 байт (4 tunnelId + 1024 data) - Это базовая единица трафика tunnel - Сообщения TunnelData переносят фрагментированные сообщения I2NP (GarlicMessage, DatabaseStore и т. д.)

**Исходный код:** - `net.i2p.data.i2np.TunnelDataMessage` - Константа: `TunnelDataMessage.DATA_LENGTH = 1024` - Обработка: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (шлюз tunnel; Тип 19)

**Назначение:** Инкапсулирует другое сообщение I2NP для отправки в tunnel через его входной шлюз.

**Формат:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Примечания:** - Полезная нагрузка представляет собой сообщение I2NP со стандартным 16-байтовым заголовком - Используется для внедрения сообщений в tunnels из локального router - Шлюз туннеля фрагментирует вложенное сообщение при необходимости - После фрагментации фрагменты инкапсулируются в сообщения TunnelData - TunnelGateway никогда не передаётся по сети; это внутренний тип сообщения, используемый до обработки tunnel

**Исходный код:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Обработка: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Тип 20)

**Назначение:** Используется в Garlic Messages (сообщения типа Garlic) и Garlic Cloves (вложенные «дольки» сообщения Garlic) для инкапсуляции произвольных данных (обычно данных приложения со сквозным шифрованием).

**Формат:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Примечания:** - Это сообщение не содержит маршрутной информации и никогда не отправляется "в необёрнутом виде" - Используется только внутри сообщений Garlic - Обычно содержит сквозно зашифрованные данные приложений (HTTP, IRC, email и т. д.) - Данные обычно представляют собой полезную нагрузку, зашифрованную ElGamal/AES или ECIES - Максимальная практическая длина составляет около 61.2 KB из-за ограничений фрагментации сообщений в tunnel

**Исходный код:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Тип 21)

**УСТАРЕЛО.** Используйте VariableTunnelBuild (тип 23) или ShortTunnelBuild (тип 25).

**Назначение:** Запрос на построение tunnel фиксированной длины на 8 хопов.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Примечания:** - Начиная с 0.9.48, может содержать ECIES-X25519 BuildRequestRecords (записи запросов на построение). См. [Создание tunnel ECIES](/docs/specs/implementation/) - Подробности см. в [Спецификации создания tunnel](/docs/specs/implementation/) - Идентификатор сообщения I2NP для данного сообщения должен быть установлен в соответствии со спецификацией создания tunnel - Хотя в сегодняшней сети встречается редко (заменено на VariableTunnelBuild), это всё ещё может использоваться для очень длинных tunnels и формально не объявлено устаревшим - Routers по-прежнему должны реализовывать это для совместимости - Фиксированный формат из 8 записей негибок и зря расходует полосу пропускания для более коротких tunnels

**Исходный код:** - `net.i2p.data.i2np.TunnelBuildMessage` - Константа: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Ответ на построение tunnel, Тип 22)

**УСТАРЕЛО.** Используйте VariableTunnelBuildReply (тип 24) или OutboundTunnelBuildReply (тип 26).

**Назначение:** Ответ на построение tunnel фиксированной длины для 8 хопов.

**Формат:**

Тот же формат, что и у TunnelBuildMessage, с BuildResponseRecords вместо BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Примечания:** - Начиная с 0.9.48, может содержать ECIES-X25519 BuildResponseRecords. См. [ECIES Tunnel Creation](/docs/specs/implementation/) - Подробности см. в [Tunnel Creation Specification](/docs/specs/implementation/) - Идентификатор сообщения I2NP для данного сообщения должен быть установлен в соответствии со спецификацией создания Tunnel - Хотя в нынешней сети встречается редко (заменён на VariableTunnelBuildReply), он всё ещё может использоваться для очень длинных tunnels и формально не объявлен устаревшим - Routers по-прежнему должны поддерживать это для совместимости

**Исходный код:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Тип 23)

**Назначение:** Построение tunnel переменной длины из 1-8 хопов. Поддерживает routers как на базе ElGamal, так и на базе ECIES-X25519.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Примечания:** - Начиная с 0.9.48, может содержать ECIES-X25519 BuildRequestRecords (записи запроса построения). См. [Создание ECIES tunnel](/docs/specs/implementation/) - Введено в router версии 0.7.12 (2009) - Не следует отправлять участникам tunnel с версиями ниже 0.7.12 - Подробности: см. [Спецификацию создания tunnel](/docs/specs/implementation/) - ID сообщения I2NP должен быть установлен в соответствии со спецификацией создания tunnel - **Типичное количество записей:** 4 (для 4-хопового tunnel) - **Типичный общий размер:** 1 + (4 × 528) = 2,113 байт - Это стандартное сообщение построения tunnel для ElGamal routers - ECIES routers обычно используют ShortTunnelBuild (сообщение короткого построения tunnel, тип 25) вместо этого

**Исходный код:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Тип 24)

**Назначение:** Ответ переменной длины на построение tunnel (туннель I2P) для 1-8 хопов. Поддерживает оба типа routers (маршрутизаторы I2P): ElGamal и ECIES-X25519.

**Формат:**

Тот же формат, что и у VariableTunnelBuildMessage, с BuildResponseRecords вместо BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Примечания:** - Начиная с 0.9.48, может содержать ECIES-X25519 BuildResponseRecords. См. [Создание Tunnel с ECIES](/docs/specs/implementation/) - Введено в версии router 0.7.12 (2009) - Не должно отправляться участникам tunnel с версией ниже 0.7.12 - Подробности см. в [Спецификации создания Tunnel](/docs/specs/implementation/) - Идентификатор сообщения I2NP должен быть установлен в соответствии со спецификацией создания tunnel - **Типичное количество записей:** 4 - **Типичный общий размер:** 2,113 байт

**Исходный код:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Тип 25)

**Назначение:** Короткие сообщения для построения tunnel только для ECIES-X25519 routers. Введены в версии API 0.9.51 (релиз 1.5.0, август 2021 г.). Это текущий стандарт для построения ECIES tunnel.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Примечания:** - Введено в router версии 0.9.51 (релиз 1.5.0, август 2021) - Не должно отправляться участникам tunnel в версиях API ранее 0.9.51 - См. [Создание ECIES Tunnel](/docs/specs/implementation/) для полной спецификации - См. [Предложение 157](/proposals/157-new-tbm/) для обоснования - **Типичное число записей:** 4 - **Типичный общий размер:** 1 + (4 × 218) = 873 байт - **Экономия полосы пропускания:** на 59% меньше, чем VariableTunnelBuild (формат построения tunnel с переменной длиной) (873 против 2,113 байт) - **Преимущество по производительности:** 4 короткие записи умещаются в одном сообщении tunnel; VariableTunnelBuild требует 3 сообщения tunnel - Теперь это стандартный формат построения tunnel для чистых ECIES-X25519 tunnel - Записи выводят ключи через HKDF, вместо того чтобы включать их явно

**Исходный код:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Константа: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Тип 26)

**Назначение:** Отправляется с исходящей конечной точки нового tunnel инициатору. Только для ECIES-X25519 routers. Введено в версии API 0.9.51 (релиз 1.5.0, август 2021).

**Формат:**

Тот же формат, что и у ShortTunnelBuildMessage, но с ShortBuildResponseRecords вместо ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Примечания:** - Введено в версии router 0.9.51 (релиз 1.5.0, август 2021) - См. [ECIES Tunnel Creation](/docs/specs/implementation/) для полной спецификации - **Типичное количество записей:** 4 - **Типичный общий размер:** 873 байт - Этот ответ отправляется от конечной точки исходящего tunnel (OBEP) обратно создателю tunnel через вновь созданный исходящий tunnel - Подтверждает, что все хопы приняли построение tunnel

**Исходный код:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Ссылки

### Официальные спецификации

- **[Спецификация I2NP](/docs/specs/i2np/)** - Полная спецификация формата сообщений I2NP
- **[Общие структуры](/docs/specs/common-structures/)** - Типы данных и структуры, используемые во всём I2P
- **[Создание tunnel](/docs/specs/implementation/)** - Создание tunnel на основе ElGamal (устарело)
- **[Создание tunnel ECIES](/docs/specs/implementation/)** - Создание tunnel на основе ECIES-X25519 (текущее)
- **[Сообщение tunnel](/docs/specs/implementation/)** - Формат сообщений tunnel и инструкции по доставке
- **[Спецификация NTCP2](/docs/specs/ntcp2/)** - Транспортный протокол TCP
- **[Спецификация SSU2](/docs/specs/ssu2/)** - Транспортный протокол UDP
- **[Спецификация ECIES](/docs/specs/ecies/)** - Шифрование ECIES-X25519-AEAD-Ratchet
- **[Спецификация криптографии](/docs/specs/cryptography/)** - Низкоуровневые криптографические примитивы
- **[Спецификация I2CP](/docs/specs/i2cp/)** - Спецификация клиентского протокола
- **[Спецификация дейтаграмм](/docs/api/datagrams/)** - Форматы Datagram2 и Datagram3

### Предложения


### Документация

- **[Маршрутизация Garlic](/docs/overview/garlic-routing/)** - Многоуровневое объединение сообщений
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Устаревшая схема шифрования
- **[Реализация tunnel](/docs/specs/implementation/)** - Фрагментация и обработка
- **[Сетевая база данных](/docs/specs/common-structures/)** - Распределенная хеш-таблица
- **[Транспорт NTCP2](/docs/specs/ntcp2/)** - Спецификация транспорта TCP
- **[Транспорт SSU2](/docs/specs/ssu2/)** - Спецификация транспорта UDP
- **[Техническое введение](/docs/overview/tech-intro/)** - Обзор архитектуры I2P

### Исходный код

- **[Репозиторий Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Официальная реализация на Java
- **[Зеркало на GitHub](https://github.com/i2p/i2p.i2p)** - Зеркало Java I2P на GitHub
- **[Репозиторий i2pd](https://github.com/PurpleI2P/i2pd)** - Реализация на C++

### Основные расположения исходного кода

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - Реализации сообщений I2NP - `core/java/src/net/i2p/crypto/` - Криптографические реализации - `router/java/src/net/i2p/router/tunnel/` - Обработка tunnel - `router/java/src/net/i2p/router/transport/` - Реализации транспорта

**Константы и значения:** - `I2NPMessage.MAX_SIZE = 65536` - Максимальный размер сообщения I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - Стандартный размер заголовка - `TunnelDataMessage.DATA_LENGTH = 1024` - Полезная нагрузка сообщения tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Длинная запись построения - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Короткая запись построения - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Максимальное число записей на одно построение

---

## Приложение A: Статистика сети и текущее состояние

### Состав сети (по состоянию на октябрь 2025 года)

- **Всего router'ов:** Примерно 60,000-70,000 (варьируется)
- **Floodfill router'ы:** Примерно 500-700 активных
- **Типы шифрования:**
  - ECIES-X25519: >95% router'ов
  - ElGamal: <5% router'ов (устаревший, только для совместимости)
- **Использование транспортов:**
  - SSU2: >60% основной транспорт
  - NTCP2: ~40% основной транспорт
  - Устаревшие транспорты (SSU1, NTCP): 0% (удалены)
- **Типы подписей:**
  - EdDSA (Ed25519): Подавляющее большинство
  - ECDSA: Небольшой процент
  - RSA: Запрещено (удалено)

### Минимальные требования к Router

- **Версия API:** 0.9.16+ (для совместимости EdDSA с сетью)
- **Рекомендуемый минимум:** API 0.9.51+ (сборки ECIES с короткими tunnel)
- **Текущий минимум для floodfills:** API 0.9.58+ (объявление router на ElGamal устаревшим)
- **Предстоящее требование:** Java 17+ (начиная с релиза 2.11.0, декабрь 2025)

### Требования к пропускной способности

- **Минимум:** 128 KBytes/sec (флаг N или выше) для floodfill
- **Рекомендуется:** 256 KBytes/sec (флаг O) или выше
- **Требования к floodfill:**
  - Минимальная пропускная способность 128 KB/sec
  - Стабильный аптайм (рекомендуется >95%)
  - Низкая задержка (<500ms до пиров)
  - Прохождение проверок состояния (время в очереди, задержка задач)

### Статистика Tunnel

- **Типичная длина tunnel:** 3-4 хопа
- **Максимальная длина tunnel:** 8 хопов (теоретически, редко используется)
- **Типичное время жизни tunnel:** 10 минут
- **Доля успешных построений tunnel:** >85% для routers с хорошей связностью
- **Формат сообщений для построения tunnel:**
  - ECIES routers: ShortTunnelBuild (218-байтовые записи)
  - Смешанные tunnels: VariableTunnelBuild (528-байтовые записи)

### Метрики производительности

- **Время построения tunnel:** 1-3 секунды (типично)
- **Сквозная задержка:** 0.5-2 секунды (типично, всего 6-8 хопов)
- **Пропускная способность:** ограничивается пропускной способностью tunnel (обычно 10-50 KB/sec на tunnel)
- **Максимальный размер датаграммы:** рекомендуется 10 KB (теоретический максимум 61.2 KB)

---

## Приложение B: Устаревшие и удалённые возможности

### Полностью удалено (больше не поддерживается)

- **Транспорт NTCP** - Удалён в релизе 0.9.50 (май 2021)
- **Транспорт SSU v1** - Удалён из Java I2P в релизе 2.4.0 (декабрь 2023)
- **Транспорт SSU v1** - Удалён из i2pd в релизе 2.44.0 (ноябрь 2022)
- **Типы подписей RSA** - Запрещены начиная с API 0.9.28

### Устаревшее (поддерживается, но не рекомендуется)

- **ElGamal routers** - Устарело начиная с API 0.9.58 (март 2023 г.)
  - Назначения ElGamal по-прежнему поддерживаются для обратной совместимости
  - Новые routers должны использовать исключительно ECIES-X25519
- **TunnelBuild (type 21)** - Устарело в пользу VariableTunnelBuild и ShortTunnelBuild
  - По-прежнему реализовано для очень длинных tunnels (>8 хопов)
- **TunnelBuildReply (type 22)** - Устарело в пользу VariableTunnelBuildReply и OutboundTunnelBuildReply
- **Шифрование ElGamal/AES** - Устарело в пользу ECIES-X25519-AEAD-Ratchet
  - По-прежнему используется для устаревших назначений
- **Длинные ECIES BuildRequestRecords (528 байт)** - Устарело в пользу короткого формата (218 байт)
  - По-прежнему используется для смешанных tunnels с ElGamal-хопами

### Сроки поддержки устаревших версий

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Приложение C: будущие разработки

### Постквантовая криптография

**Статус:** Бета, начиная с релиза 2.10.0 (сентябрь 2025), станет по умолчанию в релизе 2.11.0 (декабрь 2025)

**Реализация:** - Гибридный подход, сочетающий классический X25519 и постквантовый MLKEM (ML-KEM-768) - Обратная совместимость с существующей инфраструктурой ECIES-X25519 - Использует Signal Double Ratchet (двойной ратчет Signal) с классическим и постквантовым (PQ) ключевым материалом - Подробности см. в [Proposal 169](/proposals/169-pq-crypto/)

**Путь миграции:** 1. Релиз 2.10.0 (сентябрь 2025): доступно как бета-опция 2. Релиз 2.11.0 (декабрь 2025): включено по умолчанию 3. Будущие релизы: в конечном итоге станет обязательным

### Планируемые возможности

- **Улучшения IPv6** - Лучшая поддержка IPv6 и механизмы перехода
- **Ограничение пропускной способности для каждого tunnel** - Тонкое управление полосой пропускания для каждого tunnel
- **Расширенные метрики** - Улучшенный мониторинг производительности и диагностика
- **Оптимизации протокола** - Сниженные накладные расходы и повышенная эффективность
- **Улучшенный выбор floodfill (узлы, распространяющие netDb)** - Лучшее распределение netDb (сетевая база данных)

### Области исследований

- **Оптимизация длины tunnel** - Динамическая длина tunnel на основе модели угроз
- **Усовершенствованное заполнение** - Улучшения устойчивости к анализу трафика
- **Новые схемы шифрования** - Подготовка к угрозам квантовых вычислений
- **Контроль перегрузок** - Более эффективная обработка сетевой нагрузки
- **Поддержка мобильных устройств** - Оптимизации для мобильных устройств и сетей

---

## Приложение D: Рекомендации по реализации

### Для новых реализаций

**Минимальные требования:** 1. Поддерживать возможности API версии 0.9.51+ 2. Реализовать шифрование ECIES-X25519-AEAD-Ratchet 3. Поддерживать транспорты NTCP2 и SSU2 4. Реализовать сообщения ShortTunnelBuild (218-байтовые записи) 5. Поддерживать варианты LeaseSet2 (типы 3, 5, 7) 6. Использовать подписи EdDSA (Ed25519)

**Рекомендуется:** 1. Поддерживать гибридную постквантовую криптографию (по состоянию на 2.11.0) 2. Реализовать параметры пропускной способности для каждого tunnel (туннель) 3. Поддерживать форматы Datagram2 и Datagram3 4. Реализовать опции сервисных записей в LeaseSets 5. Следовать официальным спецификациям на /docs/specs/

**Не требуется:** 1. Поддержка ElGamal в router (устарело) 2. Поддержка устаревших транспортов (SSU1, NTCP) 3. Длинные ECIES BuildRequestRecords (528 байт для чистых ECIES tunnels) 4. сообщения TunnelBuild/TunnelBuildReply (используйте варианты Variable или Short)

### Тестирование и валидация

**Соответствие протоколу:** 1. Проверить совместимость с официальным Java I2P router 2. Проверить совместимость с i2pd C++ router 3. Проверить форматы сообщений на соответствие спецификациям 4. Протестировать циклы построения/разборки tunnel 5. Проверить шифрование/дешифрование с использованием тестовых векторов

**Тестирование производительности:** 1. Измерить долю успешного построения tunnel (должно быть >85%) 2. Протестировать с различными длинами tunnel (2-8 переходов) 3. Проверить фрагментацию и сборку 4. Тестировать под нагрузкой (несколько одновременных tunnel) 5. Измерить сквозную задержку

**Тестирование безопасности:** 1. Проверить реализацию шифрования (использовать тестовые векторы) 2. Проверить защиту от атак повторного воспроизведения 3. Проверить корректность обработки истечения срока действия сообщений 4. Проверить устойчивость к некорректно сформированным сообщениям 5. Проверить корректность генерации случайных чисел

### Распространённые подводные камни при реализации

1. **Неоднозначные форматы инструкций доставки** - Garlic clove (долька garlic‑сообщения) против tunnel‑сообщения
2. **Некорректная деривация ключей** - использование HKDF для коротких записей построения
3. **Обработка Message ID** - неправильная установка при построении tunnel
4. **Проблемы с фрагментацией** - игнорирование практического лимита 61.2 KB
5. **Ошибки порядка байтов** - Java использует big-endian (старший байт первым) для всех целых чисел
6. **Обработка истечения срока** - короткий формат переполняется 7 февраля 2106 года
7. **Генерация контрольной суммы** - требуется по-прежнему, даже если не проверяется
