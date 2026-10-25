---
title: "SSU (Secure Semireliable UDP)"
description: "Спецификация оригинального транспортного протокола UDP (устарела, заменена на SSU2)"
slug: "ssu"
aliases:
  - "/ru/docs/transport/ssu"
  - "/ru/docs/transport/ssu/"
  - "/ru/docs/transports/ssu"
  - "/ru/docs/transports/ssu/"
  - "/ru/docs/specs/ssu-spec"
  - "/ru/docs/specs/ssu-spec/"
category: "Транспорты"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Обзор

УСТАРЕЛО - SSU был заменен на SSU2. Поддержка SSU была удалена из i2pd в релизе 2.44.0 (API 0.9.56) 2022-11. Поддержка SSU была удалена из Java I2P в релизе 2.4.0 (API 0.9.61) 2023-12.

См. [обзор SSU](/docs/transport/ssu/) для получения дополнительной информации.

## Обмен DH-ключами {#dh}

Первоначальный 2048-битный обмен ключами DH описан на [странице ключей SSU](/docs/transport/ssu/#keys). Этот обмен использует то же общее простое число, что и для [шифрования ElGamal](/docs/specs/cryptography/#elgamal) в I2P.

## Заголовок сообщения {#header}

Все UDP-дейтаграммы начинаются с 16-байтового MAC (кода аутентификации сообщения) и 16-байтового IV (вектора инициализации), за которыми следует полезная нагрузка переменного размера, зашифрованная соответствующим ключом. Используемый MAC — это HMAC-MD5, усеченный до 16 байт, а ключ — полный 32-байтовый ключ AES256. Конкретная конструкция MAC представляет собой первые 16 байт от:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
где '+' означает добавление, а '^' означает исключающее ИЛИ.

IV генерируется случайно для каждого пакета. encryptedPayload — это зашифрованная версия сообщения, начинающаяся с флагового байта (шифрование-затем-MAC). payloadLength, используемая в MAC, представляет собой 2-байтовое беззнаковое целое число в формате big endian. Обратите внимание, что protocolVersion равна 0, поэтому операция исключающего ИЛИ является холостой операцией. macKey — это либо ключ введения, либо ключ, построенный из обмененного DH ключа (подробности см. ниже), как указано для каждого сообщения ниже.

**ПРЕДУПРЕЖДЕНИЕ** - используемый здесь HMAC-MD5-128 является нестандартным, см. [подробности HMAC](/docs/specs/cryptography/#udp) для получения дополнительной информации.

Сама полезная нагрузка (то есть сообщение, начинающееся с байта флага) зашифрована AES256/CBC с использованием IV и sessionKey, с защитой от повторного воспроизведения, реализованной в её теле, что объясняется ниже.

protocolVersion представляет собой 2-байтное беззнаковое целое число в формате big endian и в настоящее время установлено в 0. Узлы, использующие другую версию протокола, не смогут связываться с этим узлом, хотя более ранние версии, не использующие этот флаг, смогут.

Исключающее ИЛИ от ((netid - 2) << 8) используется для быстрого определения межсетевых соединений. netid представляет собой 2-байтовое беззнаковое целое число в формате big endian и в настоящее время установлено равным 2. Начиная с версии 0.9.42. Дополнительную информацию см. в предложении 147. Поскольку текущий network ID равен 2, это не влияет на работу текущей сети и обеспечивает обратную совместимость. Любые соединения из тестовых сетей должны иметь другой ID и не пройдут проверку HMAC.

### Спецификация HMAC

- Внутреннее заполнение: 0x36...
- Внешнее заполнение: 0x5C...
- Ключ: 32 байта
- Функция хеш-дайджеста: MD5, 16 байт
- Размер блока: 64 байта
- Размер MAC: 16 байт
- Примеры реализации на C:
  - hmac.h в [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp в [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Пример реализации на Java:
  - I2PHMac.java в [I2P](https://github.com/i2p/i2p.i2p)

### Детали ключа сессии

32-байтовый ключ сеанса создается следующим образом:

1. Возьмите обмененный DH ключ, представленный как положительный массив байтов BigInteger минимальной длины (дополнительный код big-endian)
2. Если старший бит равен 1 (т.е. array[0] & 0x80 != 0), добавьте в начало байт 0x00, как в представлении Java BigInteger.toByteArray()
3. Если массив байтов больше или равен 32 байтам, используйте первые (старшие) 32 байта
4. Если массив байтов меньше 32 байтов, добавьте байты 0x00 в конец, чтобы расширить до 32 байтов. *Очень маловероятно - см. примечание ниже.*

### Детали MAC-ключа

32-байтный MAC ключ создается следующим образом:

1. Возьмите обмененный массив байтов DH ключа, дополненный байтом 0x00 при необходимости, из шага 2 в разделе Детали ключа сессии выше.
2. Если этот массив байтов больше или равен 64 байтам, MAC ключ представляет собой байты 33-64 из этого массива байтов.
3. Если этот массив байтов меньше 64 байтов, MAC ключ представляет собой SHA-256 хеш этого массива байтов. *Начиная с релиза 0.9.8. См. примечание ниже.*

#### Важное примечание

Код до выпуска 0.9.8 был сломан и не корректно обрабатывал массивы байтов DH ключей размером от 32 до 63 байт (шаги 3 и 4 выше), и соединение завершалось неудачей. Поскольку эти случаи никогда не работали, они были переопределены, как описано выше, для выпуска 0.9.8, и случай 0-32 байта также был переопределён. Поскольку номинальный обмениваемый DH ключ составляет 256 байт, вероятность того, что минимальное представление будет менее 64 байт, чрезвычайно мала.

### Формат заголовка

Внутри AES зашифрованной полезной нагрузки существует минимальная общая структура для различных сообщений - однобайтовый флаг и четырёхбайтовая временная метка отправки (секунды с начала unix эпохи).

Формат заголовка:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
Байт флага содержит следующие битовые поля:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Без rekeying и расширенных опций размер заголовка составляет 37 байт.

### Перегенерация ключей {#rekey}

Если установлен флаг rekey, то за временной меткой следуют 64 байта ключевого материала.

При смене ключей первые 32 байта ключевого материала подаются в SHA256 для создания нового ключа MAC, а следующие 32 байта подаются в SHA256 для создания нового ключа сессии, хотя ключи не используются немедленно. Другая сторона также должна ответить с установленным флагом смены ключей и тем же ключевым материалом. После того, как обе стороны отправили и получили эти значения, должны использоваться новые ключи, а предыдущие ключи должны быть отброшены. Может быть полезно сохранять старые ключи в течение короткого времени для обработки потери пакетов и изменения порядка.

ПРИМЕЧАНИЕ: Смена ключей в настоящее время не реализована.

### Расширенные параметры {#extend}

Если установлен флаг расширенных опций, добавляется однобайтовое значение размера опции, за которым следует соответствующее количество байтов расширенных опций. Расширенные опции всегда были частью спецификации, но не были реализованы до версии 0.9.24. При наличии формат опций специфичен для типа сообщения. См. документацию по сообщениям ниже о том, ожидаются ли расширенные опции для данного сообщения, и указанный формат. Хотя Java router'ы всегда распознавали флаг и длину опций, другие реализации этого не делали. Поэтому не отправляйте расширенные опции на router'ы старше версии 0.9.24.

## Заполнение

Все сообщения содержат 0 или более байт заполнения. Каждое сообщение должно быть дополнено до границы в 16 байт, как требуется [уровнем шифрования AES256](/docs/specs/cryptography/#AES).

До релиза 0.9.7 сообщения дополнялись только до следующей границы в 16 байт, и сообщения, не кратные 16 байтам, могли быть недействительными.

Начиная с версии 0.9.7, сообщения могут быть дополнены до любой длины, при условии соблюдения текущего MTU. Любые дополнительные 1-15 байт padding'а после последнего блока из 16 байт не могут быть зашифрованы или расшифрованы и будут проигнорированы. Однако полная длина и весь padding включаются в расчет MAC.

Начиная с релиза 0.9.8, передаваемые сообщения не обязательно должны быть кратны 16 байтам. Сообщение SessionConfirmed является исключением, см. ниже.

## Ключи

Подписи в сообщениях SessionCreated и SessionConfirmed генерируются с использованием [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) из [RouterIdentity](/docs/specs/common-structures/#routeridentity), которая распространяется внеполосно путем публикации в базе данных сети, и связанного [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey).

До релиза 0.9.15 алгоритм подписи всегда был DSA с 40-байтной подписью.

Начиная с релиза 0.9.16, алгоритм подписи может быть указан с помощью [KeyCertificate](/docs/specs/common-structures/#key-certificates) в [RouterIdentity](/docs/specs/common-structures/#routeridentity) Боба.

Как ключи введения, так и ключи сессии имеют длину 32 байта и определены в спецификации общих структур [SessionKey](/docs/specs/common-structures/#sessionkey). Ключ, используемый для MAC и шифрования, указан для каждого сообщения ниже.

Ключи введения доставляются через внешний канал (сетевая база данных), где они традиционно были идентичны хешу router до версии 0.9.47, но могут быть случайными начиная с версии 0.9.48.

## Примечания

### IPv6

Спецификация протокола поддерживает как 4-байтные IPv4, так и 16-байтные IPv6 адреса. SSU-over-IPv6 поддерживается начиная с версии 0.9.8. См. документацию по отдельным сообщениям ниже для получения подробностей о поддержке IPv6.

### Временные метки {#time}

В то время как большая часть I2P использует 8-байтовые временные метки [Date](/docs/specs/common-structures/#date) с разрешением в миллисекундах, SSU использует 4-байтовые беззнаковые целые временные метки с разрешением в одну секунду. Поскольку эти значения беззнаковые, они не будут переполняться до февраля 2106 года.

## Сообщения

Определено 10 сообщений (типов полезной нагрузки):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (тип 0) {#sessionrequest}

Это первое сообщение, отправляемое для установления сессии.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 304 (IPv4) или 320 (IPv6) байт (до дополнения non-mod-16)

#### Расширенные опции

Примечание: Реализовано в версии 0.9.24.

- Минимальная длина: 3 (байт длины опции + 2 байта)
- Длина опции: минимум 2
- 2 байта флагов:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Примечания

- Поддерживаются адреса IPv4 и IPv6.
- Неинтерпретированные данные могут быть использованы в будущем для проверочных задач.

### SessionCreated (тип 1) {#sessioncreated}

Это ответ на [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 368 байт (IPv4 или IPv6) (до выравнивания не кратного 16)

#### Заметки

- Поддерживаются IPv4 и IPv6 адреса.
- Если тег relay не равен нулю, Bob предлагает выступить в качестве introducer для
  Alice. Alice может впоследствии опубликовать адрес Bob и тег relay в
  базе данных сети.
- Для подписи Bob должен использовать свой внешний порт, так как именно его будет
  использовать Alice для проверки. Если NAT/брандмауэр Bob сопоставил его внутренний порт с
  другим внешним портом, и Bob об этом не знает, проверка Alice
  завершится неудачей.
- См. раздел [Keys](#keys) выше для подробностей о подписях. Alice уже имеет
  открытый ключ подписи Bob из базы данных сети.
- До версии 0.9.15 подпись всегда представляла собой 40-байтную DSA подпись, а
  дополнение всегда составляло 8 байт. Начиная с версии 0.9.16, тип и
  длина подписи подразумеваются типом [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) в
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) Bob. Дополнение выполняется до кратности 16 байтам.
- Это единственное сообщение, использующее intro ключ отправителя. Все остальные используют
  intro ключ получателя или установленный ключ сессии.
- Время подписи, по-видимому, не используется или не проверяется в текущей
  реализации.
- Неинтерпретируемые данные могут в будущем использоваться для вызовов.
- Расширенные опции в заголовке: не ожидаются, не определены.

### SessionConfirmed (тип 2) {#sessionconfirmed}

Это ответ на сообщение [SessionCreated](#sessioncreated) и последний шаг в установлении сессии. Может потребоваться несколько сообщений SessionConfirmed, если Router Identity необходимо фрагментировать.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Фрагмент 0 через F-2** (только если F > 1; в настоящее время не используется, см. примечания ниже):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Фрагмент F-1 (последний или единственный фрагмент):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Типичный размер включая заголовок в текущей реализации: 512 байт (с подписью Ed25519) или 480 байт (с подписью DSA-SHA1) (до выравнивания не кратного 16)

#### Заметки

- В текущей реализации максимальный размер фрагмента составляет 512 байт. Это
  должно быть расширено, чтобы более длинные подписи работали без фрагментации.
  Текущая реализация не обрабатывает корректно подписи, разделённые между
  двумя фрагментами.
- Типичный [RouterIdentity](/docs/specs/common-structures/#routeridentity) составляет 387 байт, поэтому фрагментация
  никогда не нужна. Если новая криптография расширит размер RouterIdentity,
  схему фрагментации необходимо тщательно протестировать.
- Отсутствует механизм для запроса или повторной доставки недостающих фрагментов.
- Поле общего количества фрагментов F должно быть установлено одинаково во всех фрагментах.
- Смотрите раздел [Keys](#keys) выше для подробностей о подписях DSA.
- Время подписания, по-видимому, не используется или не проверяется в текущей
  реализации.
- Поскольку подпись находится в конце, заполнение в последнем или единственном пакете
  должно дополнить общий пакет до кратного 16 байтам, иначе подпись
  не будет расшифрована корректно. Это отличается от всех других типов сообщений,
  где заполнение находится в конце.
- До релиза 0.9.15 подпись всегда была 40-байтовой подписью DSA. Начиная с
  релиза 0.9.16, тип и длина подписи определяются типом
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) в [RouterIdentity](/docs/specs/common-structures/#routeridentity) Алисы. Заполнение выполняется по
  необходимости до кратного 16 байтам.
- Расширенные опции в заголовке: Не ожидаются, не определены.

### SessionDestroyed (тип 8) {#sessiondestroyed}

Сообщение SessionDestroyed было реализовано (только для получения) в релизе 0.8.1 и отправляется начиная с релиза 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Это сообщение не содержит никаких данных. Типичный размер включая заголовок в текущей реализации: 48 байт (до дополнения до кратного 16)

#### Примечания

- Сообщения Destroy, полученные с intro key отправителя или получателя, будут игнорироваться.
- Расширенные опции в заголовке: Не ожидаются, не определены.

### RelayRequest (тип 3) {#relayrequest}

Это первое сообщение, отправленное от Alice к Bob для запроса знакомства с Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 96 байт (IP Alice не включен) или 112 байт (4-байтный IP Alice включен) (до выравнивания не-кратного-16)

#### Примечания

- IP-адрес включается только в том случае, если он отличается от адреса источника и порта пакета.
- Это сообщение может быть отправлено через IPv4 или IPv6.
  Если сообщение отправляется через IPv6 для IPv4 introduction,
  или (начиная с релиза 0.9.50) через IPv4 для IPv6 introduction,
  Alice должна включить свой introduction адрес и порт.
  Это поддерживается начиная с релиза 0.9.50.
- Если Alice включает свой адрес/порт, Bob может выполнить дополнительную проверку
  перед продолжением.
  - До релиза 0.9.24 Java I2P отклонял любой адрес или порт, который
    отличался от соединения.
- Challenge не реализован, размер challenge всегда равен нулю
- Ретрансляция для IPv6 поддерживается начиная с релиза 0.9.50.
- До релиза 0.9.12 всегда использовался intro key Bob'а. Начиная с релиза
  0.9.12 используется session key, если между Alice и Bob установлена сессия.
  На практике должна быть установленная сессия, поскольку Alice получит nonce
  (introduction tag) только из сообщения создания сессии, а Bob пометит
  introduction tag как недействительный после уничтожения сессии.
- Расширенные опции в заголовке: Не ожидаются, не определены.

### RelayResponse (тип 4) {#relayresponse}

Это ответ на [RelayRequest](#relayrequest) и отправляется от Боба к Алисе.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 64 (Alice IPv4) или 80 (Alice IPv6) байт (до дополнения не-кратного-16)

#### Примечания

- Это сообщение может быть отправлено через IPv4 или IPv6.
- IP-адрес/порт Alice — это видимый IP/порт, который Bob получил в RelayRequest (не обязательно IP, который Alice включила в RelayRequest),
  и может быть IPv4 или IPv6. Alice в настоящее время игнорирует их при получении.
- IP-адрес Charlie может быть IPv4 или, начиная с релиза 0.9.50, IPv6,
  поскольку это адрес, на который Alice будет
  отправлять SessionRequest после Hole Punch.
- Ретрансляция для IPv6 поддерживается начиная с релиза 0.9.50.
- До релиза 0.9.12 всегда использовался intro key Alice. Начиная с релиза
  0.9.12 используется session key, если между
  Alice и Bob установлена сессия.
- Расширенные опции в заголовке: не ожидаются, не определены.

### RelayIntro (тип 5) {#relayintro}

Это введение для Алисы, которое отправляется от Боба к Чарли.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 48 байт (до выравнивания по non-mod-16)

#### Примечания

- Для IPv4 IP-адрес Alice всегда составляет 4 байта, поскольку Alice пытается подключиться к Charlie через IPv4.
  Начиная с версии 0.9.50 поддерживается IPv6, и IP-адрес Alice может составлять 16 байт.
- Для IPv4 это сообщение должно быть отправлено через установленное IPv4-соединение,
  поскольку это единственный способ для Bob узнать IPv4-адрес Charlie для возврата Alice в RelayResponse.
  Начиная с версии 0.9.50 поддерживается IPv6, и это сообщение может быть отправлено через установленное IPv6-соединение.
- Начиная с версии 0.9.50 любой SSU-адрес, опубликованный с introducers, должен содержать "4" или "6" в опции "caps".
- Challenge не реализован, размер challenge всегда равен нулю
- Расширенные опции в заголовке: не ожидаются, не определены.

### Данные (тип 6) {#data}

Это сообщение используется для транспорта данных и подтверждения получения.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Данные:** 1 байт флагов (см. ниже); если включены явные ACK: 1 байт количества ACK, столько же 4-байтовых MessageId, полностью подтвержденных; если включены битовые поля ACK: 1 байт количества битовых полей ACK, столько же 4-байтовых MessageId + битовое поле ACK размером 1 или более байт (см. примечания); Если включены расширенные данные: 1 байт размера данных, столько же байт расширенных данных (в настоящее время не интерпретируются); 1 байт количества фрагментов (может быть ноль); Если не ноль, то столько же фрагментов сообщения.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Каждый фрагмент содержит: - 4 байта messageId - 3 байта информации о фрагменте:   - биты 23-17: номер фрагмента 0 - 127   - бит 16: isLast (1 = истина)   - биты 15-14: не используются, устанавливаются в 0 для совместимости с будущим использованием   - биты 13-0: размер фрагмента 0 - 16383 - столько байт данных фрагмента

Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Примечания к битовому полю ACK

Битовое поле использует 7 младших битов каждого байта, при этом старший бит указывает, следует ли за ним дополнительный байт битового поля (1 = да, 0 = текущий байт битового поля является последним). Эта последовательность 7-битных массивов представляет, был ли получен фрагмент - если бит равен 1, фрагмент был получен. Для пояснения, предполагая, что фрагменты 0, 2, 5 и 9 были получены, байты битового поля будут следующими:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Примечания

- Текущая реализация добавляет ограниченное количество дублированных подтверждений для
  сообщений, которые были подтверждены ранее, если есть свободное место.
- Если количество фрагментов равно нулю, это сообщение только с подтверждением или сообщение поддержания связи.
- Функция ECN не реализована, и бит никогда не устанавливается.
- В текущей реализации бит запроса ответа устанавливается, когда количество
  фрагментов больше нуля, и не устанавливается, когда фрагментов нет.
- Расширенные данные не реализованы и никогда не присутствуют.
- Получение множественных фрагментов поддерживается во всех релизах. Передача
  множественных фрагментов реализована в релизе 0.9.16.
- В текущей реализации максимальное количество фрагментов составляет 64 (максимальный номер фрагмента = 63).
- В текущей реализации максимальный размер фрагмента, конечно, меньше MTU.
- Будьте осторожны, чтобы не превысить максимальный MTU, даже если есть большое количество
  подтверждений для отправки.
- Протокол допускает фрагменты нулевой длины, но нет причин их отправлять.
- В SSU данные используют короткий 5-байтный заголовок I2NP, за которым следует полезная нагрузка
  сообщения I2NP вместо стандартного 16-байтного заголовка I2NP. Короткий заголовок I2NP
  состоит только из однобайтного типа I2NP и 4-байтного времени истечения в
  секундах. ID сообщения I2NP используется как ID сообщения для фрагмента.
  Размер I2NP собирается из размеров фрагментов. Контрольная сумма I2NP не
  требуется, поскольку целостность UDP-сообщения обеспечивается дешифрованием.
- ID сообщений не являются порядковыми номерами и не идут подряд. SSU не
  гарантирует доставку по порядку. Хотя мы используем ID сообщения I2NP как ID сообщения SSU,
  с точки зрения протокола SSU они являются случайными числами. Фактически,
  поскольку router использует единый фильтр Блума для всех узлов, ID сообщения
  должен быть действительно случайным числом.
- Поскольку порядковых номеров нет, невозможно быть уверенным, что подтверждение было
  получено. Текущая реализация регулярно отправляет большое количество
  дублированных подтверждений. Дублированные подтверждения не следует рассматривать как признак
  перегрузки.
- Примечания к битовому полю подтверждений: Получатель пакета данных не знает, сколько
  фрагментов в сообщении, если он не получил последний фрагмент.
  Поэтому количество байтов битового поля, отправленных в ответе, может быть меньше или больше
  чем количество фрагментов, деленное на 7. Например, если самый высокий
  фрагмент, который видел получатель, имеет номер 4, требуется отправить только один байт,
  даже если всего может быть 13 фрагментов. До 10 байтов (т.е. (64 / 7)
  + 1) может быть включено для каждого подтвержденного ID сообщения.
- Расширенные опции в заголовке: Не ожидаются, не определены.

### PeerTest (тип 7) {#peertest}

Подробности см. в [SSU Peer Testing](/docs/transport/ssu/#peerTesting). Примечание: тестирование IPv6 peer поддерживается начиная с релиза 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Используемый криптографический ключ (перечислены в порядке появления): 1. При отправке от Alice к Bob: sessionKey Alice/Bob 2. При отправке от Bob к Charlie: sessionKey Bob/Charlie 3. При отправке от Charlie к Bob: sessionKey Bob/Charlie 4. При отправке от Bob к Alice: sessionKey Alice/Bob (или для Bob до версии 0.9.52, introKey Alice) 5. При отправке от Charlie к Alice: introKey Alice, как получен в сообщении PeerTest от Bob 6. При отправке от Alice к Charlie: introKey Charlie, как получен в сообщении PeerTest от Charlie

Используемый MAC Key (перечислены в порядке возникновения): 1. При отправке от Alice к Bob: Alice/Bob MAC Key 2. При отправке от Bob к Charlie: Bob/Charlie MAC Key 3. При отправке от Charlie к Bob: Bob/Charlie MAC Key 4. При отправке от Bob к Alice: introKey Alice, как получено в сообщении PeerTest от Alice 5. При отправке от Charlie к Alice: introKey Alice, как получено в сообщении PeerTest от Bob 6. При отправке от Alice к Charlie: introKey Charlie, как получено в сообщении PeerTest от Charlie

Формат сообщения:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Типичный размер включая заголовок в текущей реализации: 80 байт (до выравнивания по non-mod-16)

#### Примечания

- При отправке Alice размер IP-адреса равен 0, IP-адрес отсутствует, а порт равен 0, поскольку Bob и Charlie не используют эти данные; цель состоит в том, чтобы определить истинный IP-адрес/порт Alice и сообщить Alice; Bob и Charlie не важно, что Alice думает о своем адресе.
- При отправке Bob или Charlie IP и порт присутствуют, а IP-адрес составляет 4 или 16 байт. Тестирование IPv6 поддерживается начиная с релиза 0.9.27.
- При отправке Charlie к Alice IP и порт указаны следующим образом:
  Первый раз (сообщение 5): запрошенные Alice IP и порт, полученные в сообщении 2.
  Второй раз (сообщение 7): фактические IP и порт Alice, с которых было получено сообщение 6.
- Примечания по IPv6: До релиза 0.9.26 включительно поддерживается только тестирование IPv4-адресов. Поэтому вся коммуникация Alice-Bob и Alice-Charlie должна происходить через IPv4. Коммуникация Bob-Charlie, однако, может происходить через IPv4 или IPv6. Адрес Alice, когда указан в сообщении PeerTest, должен составлять 4 байта.
  Начиная с релиза 0.9.27 поддерживается тестирование IPv6-адресов, и коммуникация Alice-Bob и Alice-Charlie может происходить через IPv6, если Bob и Charlie указывают поддержку с помощью возможности 'B' в своем опубликованном IPv6-адресе.
  Подробности см. в Предложении 126.
- Alice отправляет запрос к Bob, используя существующую сессию через транспорт (IPv4 или IPv6), который она желает протестировать.
  Когда Bob получает запрос от Alice через IPv4, Bob должен выбрать Charlie, который рекламирует IPv4-адрес.
  Когда Bob получает запрос от Alice через IPv6, Bob должен выбрать Charlie, который рекламирует IPv6-адрес.
  Фактическая коммуникация Bob-Charlie может происходить через IPv4 или IPv6 (т.е. независимо от типа адреса Alice).
- Пир должен поддерживать таблицу активных состояний тестирования (nonces). При получении сообщения PeerTest найти nonce в таблице. Если найден, это существующий тест, и вы знаете свою роль (Alice, Bob или Charlie). В противном случае, если IP отсутствует и порт равен 0, это новый тест, и вы Bob. В противном случае это новый тест, и вы Charlie.
- Начиная с релиза 0.9.15 Alice должна иметь установленную сессию с Bob и использовать ключ сессии.
- До версии API 0.9.52 в некоторых реализациях Bob отвечал Alice, используя intro key Alice, а не ключ сессии Alice/Bob, даже несмотря на то, что Alice и Bob имеют установленную сессию (с 0.9.15).
  Начиная с версии API 0.9.52 Bob будет корректно использовать ключ сессии во всех реализациях, и Alice должна отклонять сообщение, полученное от Bob с intro key Alice, если Bob имеет версию API 0.9.52 или выше.
- Расширенные опции в заголовке: не ожидаются, не определены.

### HolePunch {#holepunch}

HolePunch - это просто UDP-пакет без данных. Он не аутентифицирован и не зашифрован. Он не содержит заголовка SSU, поэтому не имеет номера типа сообщения. Он отправляется от Charlie к Alice как часть последовательности Introduction.

## Примеры датаграмм {#sampledatagrams}

### Минимальное сообщение данных

- без фрагментов, без ACK, без NACK и т.д.
- Размер: 39 байт

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Минимальное сообщение данных с полезной нагрузкой

- Размер: 46+fragmentSize байт

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Ссылки

- [AES шифрование](/docs/specs/cryptography/#AES)
- [Спецификация общих структур](/docs/specs/common-structures/)
- [Дата](/docs/specs/common-structures/#date)
- [ElGamal шифрование](/docs/specs/cryptography/#elgamal)
- [Детали HMAC](/docs/specs/cryptography/#udp)
- [Исходный код I2P](https://github.com/i2p/i2p.i2p)
- [Исходный код i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Обзор SSU](/docs/transport/ssu/)
- [Ключи SSU](/docs/transport/ssu/#keys)
- [Тестирование пиров SSU](/docs/transport/ssu/#peerTesting)
