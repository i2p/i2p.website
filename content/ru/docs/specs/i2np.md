---
title: "Спецификация I2NP"
description: "Форматы сообщений протокола сети I2P (I2NP), приоритеты и общие структуры для связи между router'ами."
slug: "i2np"
aliases:
  - "/ru/spec/i2np"
  - "/ru/spec/i2np/"
category: "Протоколы"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Обзор

Сетевой протокол I2P (I2NP) — это уровень над транспортными протоколами I2P. Это протокол взаимодействия между router'ами. Он используется для запросов и ответов к сетевой базе данных netDb, для создания tunnel'ов и для зашифрованных сообщений данных от router'ов и клиентов. Сообщения I2NP могут отправляться напрямую от точки к точке другому router'у или анонимно через tunnel'ы к этому router'у.

## Версии протокола {#versions}

Все router должны публиковать версию своего протокола I2NP в поле "router.version" в свойствах RouterInfo. Это поле версии является версией API, указывающей уровень поддержки различных функций протокола I2NP, и не обязательно соответствует фактической версии router.

Если альтернативные (не-Java) router желают публиковать любую информацию о версии фактической реализации router, они должны делать это в другом свойстве. Разрешены версии, отличные от перечисленных ниже. Поддержка будет определяться через числовое сравнение; например, 0.9.13 подразумевает поддержку функций 0.9.12. Обратите внимание, что свойство "coreVersion" больше не публикуется в информации router и никогда не использовалось для определения версии протокола I2NP.

Базовое описание версий протокола I2NP представлено ниже. Подробности смотрите далее.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Обратите внимание, что также существуют функции, связанные с транспортом, и вопросы совместимости; подробности смотрите в документации по транспортам NTCP и SSU.

## Общие структуры {#structures}

Следующие структуры являются элементами нескольких I2NP сообщений. Они не являются полными сообщениями.

### Заголовок I2NP-сообщения {#struct-I2NPMessageHeader}

#### Описание

Общий заголовок для всех I2NP сообщений, который содержит важную информацию, такую как контрольная сумма, дата истечения срока действия и т.д.

#### Содержание

Используются три отдельных формата в зависимости от контекста: один стандартный формат и два коротких формата.

Стандартный 16-байтовый формат содержит 1 байт [Integer](/docs/specs/common-structures/#integer), указывающий тип этого сообщения, за которым следует 4-байтовый [Integer](/docs/specs/common-structures/#integer), указывающий message-id. После этого идет дата истечения [Date](/docs/specs/common-structures/#date), за которой следует 2-байтовый [Integer](/docs/specs/common-structures/#integer), указывающий длину полезной нагрузки сообщения, за которым следует [Hash](/docs/specs/common-structures/#hash), усеченный до первого байта. После этого следуют фактические данные сообщения.

Короткие форматы используют 4-байтовое время истечения в секундах вместо 8-байтового времени истечения в миллисекундах. Короткие форматы не содержат контрольную сумму или размер, они предоставляются инкапсуляциями в зависимости от контекста.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Примечания

- При передаче через [SSU](/docs/transports/ssu/) 16-байтный стандартный заголовок не используется. Включаются только 1-байтный тип и 4-байтное время истечения в секундах. Идентификатор сообщения и размер встраиваются в формат пакета данных SSU. Контрольная сумма не требуется, поскольку ошибки обнаруживаются при расшифровке.

- При передаче через [NTCP2](/docs/specs/ntcp2/) или [SSU2](/docs/specs/ssu2/), 16-байтовый стандартный заголовок не используется. Включаются только 1-байтовый тип, 4-байтовый идентификатор сообщения и 4-байтовое время истечения в секундах. Размер встроен в форматы пакетов данных NTCP2 и SSU2. Контрольная сумма не требуется, поскольку ошибки обнаруживаются при расшифровке.

- Стандартный заголовок также требуется для I2NP сообщений, содержащихся в других сообщениях и структурах (Data, TunnelData, TunnelGateway и GarlicClove). Начиная с версии 0.8.12, для уменьшения накладных расходов, проверка контрольной суммы отключена в некоторых местах стека протоколов. Однако для совместимости со старыми версиями генерация контрольной суммы по-прежнему обязательна. Определение точек в стеке протоколов, где известна версия удаленного router'а и можно отключить генерацию контрольной суммы, является темой для будущих исследований.

- Короткое время истечения не имеет знака и обернется 7 февраля 2106 года. С этой даты необходимо добавить смещение для получения правильного времени.

- Реализации могут отклонять сообщения с истечением срока действия слишком далеко в будущем. Рекомендуемое максимальное время истечения — 60 секунд в будущем.

### BuildRequestRecord {#struct-BuildRequestRecord}

УСТАРЕЛО, используется в текущей сети только когда tunnel содержит ElGamal router. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Описание

Одна запись в наборе из нескольких записей для запроса создания одного хопа в tunnel. Для получения более подробной информации см. [обзор tunnel](/docs/specs/tunnel-implementation/) и [спецификацию создания tunnel ElGamal](/docs/specs/tunnel-creation/).

Для BuildRequestRecords ECIES-X25519 см. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Содержание (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) для получения сообщений, за которым следует [Hash](/docs/specs/common-structures/#hash) нашей [RouterIdentity](/docs/specs/common-structures/#routeridentity). После этого следуют [TunnelId](/docs/specs/common-structures/#tunnelid) и [Hash](/docs/specs/common-structures/#hash) [RouterIdentity](/docs/specs/common-structures/#routeridentity) следующего router'а.

Шифрование ElGamal и AES:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
Зашифровано ElGamal:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Открытый текст:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Примечания

- В 512-байтном зашифрованном записи данные ElGamal содержат байты 1-256 и 258-513 из 514-байтного зашифрованного блока ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Два байта заполнения из блока (нулевые байты в позициях 0 и 257) удаляются.

- См. [спецификацию создания tunnel](/docs/specs/tunnel-creation/) для получения подробностей о содержимом полей.

### BuildResponseRecord {#struct-BuildResponseRecord}

УСТАРЕЛО, используется в текущей сети только когда tunnel содержит ElGamal router. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Описание

Одна запись в наборе из нескольких записей с ответами на запрос построения. Для получения более подробной информации см. [обзор туннелей](/docs/specs/tunnel-implementation/) и [спецификацию создания туннелей ElGamal](/docs/specs/tunnel-creation/).

Для BuildResponseRecords ECIES-X25519 см. [Создание туннелей ECIES](/docs/specs/tunnel-creation-ecies/).

#### Содержание (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Примечания

- Поле случайных данных может в будущем использоваться для возврата информации о перегрузке или подключениях пиров обратно к запрашивающей стороне.

- См. [спецификацию создания туннелей](/docs/specs/tunnel-creation/) для подробностей о поле ответа.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Только для ECIES-X25519 router, начиная с версии API 0.9.51. 218 байт в зашифрованном виде. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Только для ECIES-X25519 router, начиная с версии API 0.9.51. 218 байт в зашифрованном виде. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Предупреждение: Это формат, используемый для garlic cloves внутри ElGamal-зашифрованных garlic сообщений [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Формат для ECIES-AEAD-X25519-Ratchet garlic сообщений и garlic cloves значительно отличается; см. [ECIES](/docs/specs/ecies/) для спецификации.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Примечания

- Cloves никогда не фрагментируются. При использовании в Garlic Clove первый бит байта флага Delivery Instructions указывает на шифрование. Если этот бит равен 0, clove не зашифрован. Если 1, clove зашифрован, и 32-байтовый Session Key сразу следует за байтом флага. Шифрование Clove не полностью реализовано.

- Смотрите также [спецификацию garlic routing](/docs/overview/garlic-routing/).

- Максимальная длина является функцией общей длины всех зубчиков и максимальной длины GarlicMessage.

- В будущем сертификат может быть использован для HashCash, чтобы "платить" за маршрутизацию.

- Сообщение может быть любым I2NP сообщением (включая GarlicMessage, хотя на практике это не используется). Сообщения, используемые на практике: DataMessage, DeliveryStatusMessage и DatabaseStoreMessage.

- Clove ID обычно устанавливается как случайное число при передаче и проверяется на дубликаты при получении (то же пространство идентификаторов сообщений, что и у Message ID верхнего уровня)

### Инструкции доставки Garlic Clove {#struct-GarlicCloveDeliveryInstructions}

Это формат, используемый как для зашифрованных ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal), так и для зашифрованных ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/) garlic cloves.

Данная спецификация предназначена только для инструкций доставки внутри Garlic Cloves. Обратите внимание, что "инструкции доставки" также используются внутри сообщений туннеля, где формат значительно отличается. См. [документацию по сообщениям туннеля](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) для получения подробной информации. НЕ используйте следующую спецификацию для инструкций доставки сообщений туннеля!

Ключ сессии и задержка не используются и никогда не присутствуют, поэтому возможны три длины: 1 (LOCAL), 33 (ROUTER и DESTINATION) и 37 (TUNNEL) байт.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Сообщения

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Описание

Незапрошенное сохранение базы данных или ответ на успешное сообщение [DatabaseLookup](#msg-DatabaseLookup)

#### Содержание

Несжатый LeaseSet, LeaseSet2, MetaLeaseSet или EncryptedLeaseset, или сжатая RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Примечания

- Для безопасности поля ответа игнорируются, если сообщение получено через tunnel.

- Ключ является "настоящим" хешем RouterIdentity или Destination, НЕ ключом маршрутизации.

- Типы 3, 5 и 7 доступны начиная с версии 0.9.38. См. предложение 123 для получения дополнительной информации. Эти типы следует отправлять только на router с версией 0.9.38 или выше.

- В качестве оптимизации для уменьшения количества соединений, если тип — это LeaseSet, токен ответа включен, ID туннеля ответа не равен нулю, и пара шлюз ответа/ID туннеля найдена в LeaseSet как lease, получатель может перенаправить ответ на любой другой lease в LeaseSet.

- Чтобы скрыть ОС router'а и его реализацию, соответствуйте Java-реализации router'а для gzip, устанавливая время модификации в 0 и байт ОС в 0xFF, а также установите XFL в 0x02 (максимальное сжатие, самый медленный алгоритм). См. RFC 1952. Первые 10 байт сжатой информации router'а будут (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Описание

Запрос на поиск элемента в сетевой базе данных. Ответом является либо [DatabaseStore](#msg-DatabaseStore), либо [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Содержание

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Шифрование ответов

ПРИМЕЧАНИЕ: ElGamal router устарели начиная с API 0.9.58. Поскольку рекомендуемая минимальная версия floodfill для запросов теперь 0.9.58, реализации не обязаны поддерживать шифрование для ElGamal floodfill router. ElGamal назначения по-прежнему поддерживаются.

Флаговый бит 4 используется в сочетании с битом 1 для определения режима шифрования ответа. Флаговый бит 4 должен устанавливаться только при отправке на router с версией 0.9.46 или выше. Подробности см. в предложениях 154 и 156.

В таблице ниже "DH n/a" означает, что ответ не зашифрован. "DH no" означает, что ключи ответа включены в запрос. "DH yes" означает, что ключи ответа выводятся из операции DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Без шифрования

reply_key, tags и reply_tags отсутствуют.

#### ElG to ElG

Поддерживается с версии 0.9.7. Устарел с версии 0.9.58. ElG назначение отправляет запрос на ElG router.

Генерация ключа запросчика:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Формат сообщения:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES в ElG

Поддерживается с версии 0.9.46. Устарело с версии 0.9.58. ECIES destination отправляет запрос на ElG router. Поля reply_key и reply_tags переопределены для ECIES-зашифрованного ответа.

Генерация ключа запрашивающей стороны:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Формат сообщения: Переопределить поля reply_key и reply_tags следующим образом:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
Ответ представляет собой сообщение ECIES Existing Session, как определено в [ECIES](/docs/specs/ecies/).

#### Формат ответа

Это существующее сообщение сессии, такое же как в [ECIES](/docs/specs/ecies/), скопировано ниже для справки.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Параметры AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES к ECIES (0.9.49)

ECIES назначение или router отправляет запрос на поиск к ECIES router. Поддерживается начиная с версии 0.9.49.

ECIES router были введены в версии 0.9.48, см. [Proposal 156](/proposals/156/). ECIES destinations и router могут использовать тот же формат, что и в разделе "ECIES to ElG" выше, с включением ключей ответа в запрос. Шифрование сообщений поиска указано в [ECIES-ROUTERS](/docs/specs/ecies-routers/). Запрашивающая сторона анонимна.

#### ECIES в ECIES (в будущем)

Эта опция пока полностью не определена. См. [Предложение 156](/proposals/156/).

#### Примечания

- До версии 0.9.16 ключ мог относиться к RouterInfo или LeaseSet, поскольку они находились в одном пространстве ключей, и не было флага для запроса только определенного типа данных.

- Флаг шифрования, ключ ответа и теги ответа начиная с версии 0.9.7.

- Зашифрованные ответы полезны только когда ответ передается через tunnel.

- Количество включенных тегов может быть больше одного, если реализованы альтернативные стратегии поиска в DHT (например, рекурсивные поиски).

- Ключ поиска и исключаемые ключи являются "настоящими" хешами, а НЕ ключами маршрутизации.

- Типы 3, 5 и 7 могут возвращаться начиная с релиза 0.9.38. См. предложение 123 для получения дополнительной информации.

- Примечания к исследовательскому поиску: Исследовательский поиск определяется как возврат списка не-floodfill хешей, близких к ключу. Однако, смотрите важные примечания для DatabaseSearchReply относительно вариантов реализации. Кроме того, данная спецификация никогда не разъясняла четко, должен ли получатель искать ключ поиска для RI и возвращать DatabaseStore вместо DSRM, если он присутствует. Java выполняет поиск; i2pd не выполняет. Поэтому не рекомендуется использовать исследовательский поиск для ранее полученных хешей.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Описание

Ответ на неудавшееся сообщение [DatabaseLookup](#msg-DatabaseLookup)

#### Содержание

Список хешей router'ов, наиболее близких к запрашиваемому ключу

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Примечания

- Хеш 'from' не аутентифицирован и ему нельзя доверять.

- Возвращаемые хеши узлов не обязательно ближе к ключу, чем router, к которому направлен запрос. Для ответов на обычные запросы это облегчает обнаружение новых floodfill и "обратный" поиск (дальше от ключа) для повышения надежности.

- Ключ для exploration lookup обычно генерируется случайным образом. Поэтому peer_hashes не-floodfill узлов в ответе могут быть выбраны с использованием оптимизированного алгоритма, такого как предоставление узлов, которые близки к ключу, но не обязательно самые близкие во всей локальной базе данных сети, чтобы избежать неэффективной сортировки или поиска по всей локальной базе данных. Также могут подходить другие стратегии, такие как кэширование. Это зависит от реализации.

- Типичное количество возвращаемых хешей: 3

- Рекомендуемое максимальное количество хэшей для возврата: 16

- Ключ поиска, хэши узлов и хэш отправителя являются "настоящими" хэшами, а НЕ ключами маршрутизации.

### DeliveryStatus {#msg-DeliveryStatus}

#### Описание

Простое подтверждение получения сообщения. Обычно создается отправителем сообщения и упаковывается в Garlic Message вместе с самим сообщением, чтобы быть возвращенным получателем.

Это сообщение также используется для тестирования туннелей, когда инициатор отправляет его через исходящий туннель во входящий туннель и обратно к себе. В этом случае оно также, как правило, обёрнуто в Garlic. Тестирование туннелей требуется, начиная с версии API 0.9.68 от 2026-02, поскольку маршрутизаторам разрешено отбрасывать участвующие туннели, которые не получили трафик в течение первых двух минут.

#### Содержание

Идентификатор доставленного сообщения, а также время его создания или получения.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Примечания

- Похоже, что временная метка всегда устанавливается создателем на текущее время. Однако в коде есть несколько случаев использования этого, и в будущем могут быть добавлены новые.

- Это сообщение также используется как подтверждение установления сессии в SSU [SSU-ED](/docs/transports/ssu/#establishDirect). В этом случае ID сообщения устанавливается в случайное число, а "время прибытия" устанавливается в текущий network-wide ID, который равен 2 (т.е. 0x0000000000000002).

### Garlic {#msg-Garlic}

Предупреждение: Это формат, используемый для зашифрованных ElGamal сообщений с чесночным шифрованием [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Формат сообщений с чесночным шифрованием и чесночными дольками на основе ECIES-AEAD-X25519-Ratchet значительно отличается; см. [ECIES](/docs/specs/ecies/) для спецификации.

#### Описание

Используется для объединения нескольких зашифрованных сообщений I2NP

#### Содержание

После расшифровки представляет собой серию [Garlic Cloves](#struct-GarlicClove) и дополнительные данные, также известные как Clove Set.

Зашифровано:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Расшифрованные данные, также известные как набор Clove:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Примечания

- Когда не зашифрованы, данные содержат один или более [Garlic Cloves](#struct-GarlicClove).

- Зашифрованный блок AES дополняется до минимума 128 байт; с 32-байтовым Session Tag минимальный размер зашифрованного сообщения составляет 160 байт; с 4 байтами длины минимальный размер Garlic Message составляет 164 байта.

- Фактическая максимальная длина меньше 64 КБ; см. [I2NP](/docs/protocol/i2np/).

- См. также [спецификацию ElGamal/AES](/docs/specs/elgamal-aes/).

- См. также [спецификацию garlic routing](/docs/overview/garlic-routing/).

- Минимальный размер блока, зашифрованного AES, в 128 байт в настоящее время не настраивается, однако минимальный размер DataMessage в GarlicClove в GarlicMessage с учетом служебных данных в любом случае составляет 128 байт. Настраиваемая опция для увеличения минимального размера может быть добавлена в будущем.

- ID сообщения обычно устанавливается в случайное число при передаче и, по-видимому, игнорируется при получении.

- В будущем сертификат потенциально может использоваться для HashCash для "оплаты" маршрутизации.

### TunnelData {#msg-TunnelData}

#### Описание

Сообщение, отправленное от шлюза или участника туннеля следующему участнику или конечной точке. Данные имеют фиксированную длину и содержат фрагментированные, сгруппированные, дополненные и зашифрованные сообщения I2NP.

#### Содержание

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Примечания

- ID I2NP сообщения для данного сообщения устанавливается в новое случайное число на каждом переходе.

- См. также [Спецификация сообщений tunnel](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Описание

Оборачивает другое сообщение I2NP для отправки в туннель на входном шлюзе туннеля.

#### Содержание

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Примечания

- Полезная нагрузка представляет собой I2NP сообщение со стандартным 16-байтовым заголовком.

### Данные {#msg-Data}

#### Описание

Используется сообщениями Garlic и дольками Garlic для упаковки произвольных данных.

#### Содержание

Целое число длины, за которым следуют непрозрачные данные.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Заметки

- Это сообщение не содержит информации о маршрутизации и никогда не будет отправлено "в незавёрнутом виде". Оно используется только внутри сообщений `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

УСТАРЕЛО, используйте [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Примечания

- Начиная с версии 0.9.48, также может содержать BuildRequestRecords ECIES-X25519, см. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- См. также [спецификацию создания туннелей](/docs/specs/tunnel-creation/).

- Идентификатор I2NP сообщения для данного сообщения должен быть установлен в соответствии со спецификацией создания tunnel.

- Хотя это сообщение редко встречается в современной сети, поскольку было заменено сообщением `VariableTunnelBuild`, оно может по-прежнему использоваться для очень длинных tunnel'ей и не является устаревшим. Router'ы должны реализовать его.

### TunnelBuildReply {#msg-TunnelBuildReply}

УСТАРЕЛО, используйте [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Примечания

- Начиная с версии 0.9.48, может также содержать BuildResponseRecords ECIES-X25519, см. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- См. также [спецификацию создания tunnel'ов](/docs/specs/tunnel-creation/).

- Идентификатор I2NP сообщения для данного сообщения должен быть установлен в соответствии со спецификацией создания tunnel.

- Хотя это сообщение редко встречается в современной сети, поскольку было заменено сообщением `VariableTunnelBuildReply`, оно все еще может использоваться для очень длинных tunnel'ов и не является устаревшим. Router'ы должны его реализовывать.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Примечания

- Начиная с версии 0.9.48, также может содержать ECIES-X25519 BuildRequestRecords, см. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Это сообщение было введено в версии router 0.7.12 и может не отправляться участникам tunnel более ранних версий.

- См. также [спецификацию создания tunnel'ей](/docs/specs/tunnel-creation/).

- Идентификатор I2NP сообщения для данного сообщения должен быть установлен согласно спецификации создания tunnel.

- Типичное количество записей в сегодняшней сети составляет 4, при общем размере 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Примечания

- Начиная с версии 0.9.48, может также содержать ECIES-X25519 BuildResponseRecords, см. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Это сообщение было введено в версии router 0.7.12 и может не отправляться участникам tunnel более ранних версий.

- См. также [спецификацию создания tunnel](/docs/specs/tunnel-creation/).

- Идентификатор I2NP сообщения для данного сообщения должен быть установлен в соответствии со спецификацией создания tunnel.

- Типичное количество записей в сегодняшней сети составляет 4, при общем размере 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Описание

Начиная с версии API 0.9.51, только для маршрутизаторов ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Примечания

- Начиная с версии 0.9.51. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Это сообщение было введено в версии router 0.9.51 и может не отправляться участникам tunnel более ранних версий.

- Типичное количество записей в сегодняшней сети составляет 4, общий размер 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Описание

Отправляется из исходящей точки нового туннеля инициатору. Начиная с версии API 0.9.51, только для маршрутизаторов с ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Примечания

- Начиная с версии 0.9.51. См. [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Типичное количество записей в современной сети составляет 4, общий размер — 873.

## Ссылки

- **[CRYPTO-ELG]** [Криптография - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Общие структуры - Дата](/docs/specs/common-structures/#date)
- **[ECIES]** [Спецификация ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Спецификация ECIES роутеров](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic маршрутизация](/docs/overview/garlic-routing/)
- **[Hash]** [Общие структуры - Хеш](/docs/specs/common-structures/#hash)
- **[I2NP]** [Протокол I2NP](/docs/protocol/i2np/)
- **[Integer]** [Общие структуры - Целое число](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Спецификация NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Предложение 156](/proposals/156/)
- **[Prop157]** [Предложение 157](/proposals/157/)
- **[RouterIdentity]** [Общие структуры - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [Транспорт SSU](/docs/transports/ssu/)
- **[SSU-ED]** [Транспорт SSU - Прямое установление](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Спецификация SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Инструкции доставки tunnel сообщений](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Спецификация создания tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Создание ECIES tunnel](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Реализация tunnel](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Спецификация tunnel сообщений](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Общие структуры - TunnelId](/docs/specs/common-structures/#tunnelid)
