---
title: "Спецификация создания туннелей (ECIES-X25519)"
description: "Шифрование сообщений Tunnel Build с использованием криптографических примитивов ECIES-X25519 для обеспечения прямой секретности."
slug: "tunnel-creation-ecies"
aliases:
  - "/ru/docs/specs/tunnel-creation-ecies-spec"
  - "/ru/docs/specs/tunnel-creation-ecies-spec/"
category: "Протоколы"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Обзор

Этот документ определяет шифрование сообщений Tunnel Build с использованием криптографических примитивов, представленных в [ECIES-X25519](/docs/specs/ecies/). Это часть общего предложения [Prop156](/proposals/156/) по переводу router'ов с ключей ElGamal на ключи ECIES-X25519.

Определены две версии. Первая использует существующие build-сообщения и размер build record для совместимости с ElGamal router'ами. Эта спецификация была реализована в релизе 0.9.48 и теперь устарела. Вторая использует два новых build-сообщения и меньший размер build record и может использоваться только с ECIES router'ами. Эта спецификация реализована начиная с релиза 0.9.51.

Для целей перехода сети с ElGamal + AES256 на ECIES + ChaCha20 необходимы tunnel с смешанными ElGamal и ECIES router. Предоставляются спецификации для обработки смешанных переходов tunnel. Никаких изменений не будет внесено в формат, обработку или шифрование переходов ElGamal. Этот формат сохраняет тот же размер для записей построения tunnel, что необходимо для совместимости.

Создатели tunnel ElGamal будут генерировать эфемерные пары ключей X25519 для каждого hop и следовать данной спецификации для создания tunnel, содержащих ECIES hop.

Данный документ описывает построение tunnel с использованием ECIES-X25519. Для обзора всех изменений, необходимых для ECIES router, см. предложение 156 [Prop156](/proposals/156/). Для дополнительной информации о разработке спецификации длинных записей см. предложение 152 [Prop152](/proposals/152/). Для дополнительной информации о разработке спецификации коротких записей см. предложение 157 [Prop157](/proposals/157/).

### Криптографические примитивы

Примитивы, необходимые для реализации данной спецификации:

- AES-256-CBC как в [Cryptography](/docs/specs/cryptography/)
- Функции STREAM ChaCha20: ENCRYPT(k, iv, plaintext) и DECRYPT(k, iv, ciphertext) - как в [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) и [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Функции STREAM ChaCha20/Poly1305: ENCRYPT(k, n, plaintext, ad) и DECRYPT(k, n, ciphertext, ad) - как в [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/) и [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Функции X25519 DH - как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)

Другие функции Noise, определенные в других местах:

- MixHash(d) - как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)

## Дизайн

### Фреймворк протокола Noise

Данная спецификация содержит требования, основанные на Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11). В терминологии Noise, Alice является инициатором, а Bob — отвечающей стороной.

Он основан на протоколе Noise Noise_N_25519_ChaChaPoly_SHA256. Этот протокол Noise использует следующие примитивы:

- Односторонний паттерн рукопожатия: N - Алиса не передает свой статический ключ Бобу (N)
- Функция DH: X25519 - X25519 DH с длиной ключа 32 байта, как указано в [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Функция шифрования: ChaChaPoly - AEAD_CHACHA20_POLY1305, как указано в [RFC-7539](https://tools.ietf.org/html/rfc7539) раздел 2.8. 12-байтовый nonce, с первыми 4 байтами, установленными в ноль. Идентично тому, что в [NTCP2](/docs/specs/ntcp2/)
- Хэш-функция: SHA256 - Стандартный 32-байтовый хэш, уже широко используемый в I2P

### Шаблоны рукопожатия

Рукопожатия используют шаблоны рукопожатий [Noise](https://noiseprotocol.org/noise.html).

Используется следующее соответствие букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения

Запрос сборки идентичен шаблону Noise N. Это также идентично первому сообщению (Session Request) в шаблоне XK, используемом в [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Шифрование запросов

Записи запроса сборки создаются создателем туннеля и асимметрично шифруются для отдельного узла. Это асимметричное шифрование записей запроса в настоящее время использует ElGamal, как определено в [Cryptography](/docs/specs/cryptography/), и содержит контрольную сумму SHA-256. Эта конструкция не обладает прямой секретностью.

Дизайн ECIES использует односторонний Noise паттерн "N" с ECIES-X25519 эфемерно-статическим DH, с HKDF и ChaCha20/Poly1305 AEAD для обеспечения прямой секретности, целостности и аутентификации. Alice является инициатором построения туннеля. Каждый узел в туннеле является Bob.

### Шифрование ответов

Записи ответа сборки создаются создателем hops и симметрично шифруются для создателя. Это симметричное шифрование записей ответа ElGamal представляет собой AES с добавленной впереди контрольной суммой SHA-256. Эта конструкция не обеспечивает прямую секретность.

Ответы ECIES используют ChaCha20/Poly1305 AEAD для обеспечения целостности и аутентификации.

## Спецификация длинных записей

ПРИМЕЧАНИЕ: Устарело, не используется. Используйте формат Short Record, описанный ниже.

### Записи запросов на построение

Зашифрованные BuildRequestRecords имеют размер 528 байт как для ElGamal, так и для ECIES, для обеспечения совместимости.

#### Запись запроса не зашифрована

Это спецификация tunnel BuildRequestRecord для ECIES-X25519 router'ов. Краткое изложение изменений:

- Удалить неиспользуемый 32-байтный хеш router
- Изменить время запроса с часов на минуты
- Добавить поле истечения срока для будущего переменного времени tunnel
- Добавить больше места для флагов
- Добавить маппинг для дополнительных опций сборки
- AES-256 ключ ответа и IV не используются для собственной записи ответа hop
- Незашифрованная запись длиннее из-за меньших накладных расходов на шифрование

Запись запроса не содержит ключей ответа ChaCha. Эти ключи выводятся из KDF. См. ниже.

Все поля представлены в формате big-endian.

Незашифрованный размер: 464 байта

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
Поле flags такое же, как определено в [Tunnel-Creation](/docs/specs/tunnel-creation/) и содержит следующее:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Бит 7 указывает, что hop будет входящим шлюзом (IBGW). Бит 6 указывает, что hop будет исходящей конечной точкой (OBEP). Если ни один из битов не установлен, hop будет промежуточным участником. Оба бита не могут быть установлены одновременно.

Истечение срока запроса предназначено для будущей переменной продолжительности tunnel. На данный момент единственное поддерживаемое значение — 600 (10 минут).

Опции построения tunnel представляют собой структуру Mapping, как определено в [Common](/docs/specs/common-structures/). Единственные опции, определенные на данный момент, предназначены для параметров пропускной способности, начиная с API 0.9.65, подробности см. ниже. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) составляет 296 байт, а максимальное значение поля длины Mapping равно 294.

#### Запись запроса зашифрована

Все поля имеют порядок байтов big-endian, за исключением эфемерного открытого ключа, который имеет порядок little-endian.

Зашифрованный размер: 528 байт

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Создание записей ответа

Зашифрованные BuildReplyRecords имеют размер 528 байт как для ElGamal, так и для ECIES, для обеспечения совместимости.

#### Запись ответа не зашифрована

Это спецификация tunnel BuildReplyRecord для ECIES-X25519 router'ов. Краткое изложение изменений:

- Добавить сопоставление для параметров ответа сборки
- Незашифрованная запись длиннее из-за меньших накладных расходов на шифрование

Ответы ECIES шифруются с помощью ChaCha20/Poly1305.

Все поля имеют порядок байтов big-endian.

Нешифрованный размер: 512 байт

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Опции ответа на построение туннеля представляют собой структуру Mapping, как определено в [Common](/docs/specs/common-structures/). Единственными опциями, определенными в настоящее время, являются параметры пропускной способности, начиная с API 0.9.65, подробности см. ниже. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) составляет 511 байт, а максимальное значение поля длины Mapping составляет 509.

Байт ответа является одним из следующих значений, как определено в [Tunnel-Creation](/docs/specs/tunnel-creation/) для избежания фингерпринтинга:

- 0x00 (принять)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Запись ответа зашифрована

Зашифрованный размер: 528 байт

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
После полного перехода на записи ECIES правила диапазонного заполнения такие же, как для записей запросов.

### Симметричное шифрование записей

Смешанные tunnel разрешены и необходимы для перехода с ElGamal на ECIES. В переходный период все большее количество router будет использовать ключи ECIES.

Предварительная обработка симметричной криптографии будет выполняться таким же образом:

- "encryption":
  - шифр работает в режиме расшифровки
  - записи запросов предварительно расшифрованы при предобработке (скрывая зашифрованные записи запросов)
- "decryption":
  - шифр работает в режиме шифрования
  - записи запросов зашифрованы (раскрывая следующую запись запроса в открытом тексте) участвующими хопами
- ChaCha20 не имеет "режимов", поэтому он просто запускается три раза:
  - один раз при предобработке
  - один раз хопом
  - один раз при финальной обработке ответа

При использовании смешанных tunnel создатели tunnel должны будут основывать симметричное шифрование BuildRequestRecord на типе шифрования текущего и предыдущего перехода.

Каждый hop будет использовать свой собственный тип шифрования для шифрования BuildReplyRecords и других записей в VariableTunnelBuildMessage (VTBM).

На обратном пути конечная точка (отправитель) должна будет отменить [Множественное шифрование](https://en.wikipedia.org/wiki/Multiple_encryption), используя ключ ответа каждого узла.

В качестве поясняющего примера рассмотрим исходящий tunnel с ECIES, окружённым ElGamal:

- Отправитель (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Все BuildRequestRecords находятся в зашифрованном состоянии (с использованием ElGamal или ECIES).

Шифр AES256/CBC, когда используется, по-прежнему применяется для каждой записи, без связывания между несколькими записями.

Аналогично, ChaCha20 будет использоваться для шифрования каждой записи, а не для потокового шифрования всего VTBM.

Записи запросов предварительно обрабатываются Отправителем (OBGW):

- Запись H3 "шифруется" с использованием:
  - ключа ответа H2 (ChaCha20)
  - ключа ответа H1 (AES256/CBC)
- Запись H2 "шифруется" с использованием:
  - ключа ответа H1 (AES256/CBC)
- Запись H1 отправляется без симметричного шифрования

Только H2 проверяет флаг шифрования ответа и видит, что за ним следует AES256/CBC.

После обработки каждым узлом записи находятся в "расшифрованном" состоянии:

- Запись H3 "расшифровывается" с использованием:
  - Ключа ответа H3 (AES256/CBC)
- Запись H2 "расшифровывается" с использованием:
  - Ключа ответа H3 (AES256/CBC)
  - Ключа ответа H2 (ChaCha20-Poly1305)
- Запись H1 "расшифровывается" с использованием:
  - Ключа ответа H3 (AES256/CBC)
  - Ключа ответа H2 (ChaCha20)
  - Ключа ответа H1 (AES256/CBC)

Создатель tunnel'а, также известный как Inbound Endpoint (IBEP), постобрабатывает ответ:

- Запись H3 "шифруется" с использованием:
  - Ключа ответа H3 (AES256/CBC)
- Запись H2 "шифруется" с использованием:
  - Ключа ответа H3 (AES256/CBC)
  - Ключа ответа H2 (ChaCha20-Poly1305)
- Запись H1 "шифруется" с использованием:
  - Ключа ответа H3 (AES256/CBC)
  - Ключа ответа H2 (ChaCha20)
  - Ключа ответа H1 (AES256/CBC)

### Ключи записей запросов

Эти ключи явно включаются в ElGamal BuildRequestRecords. Для ECIES BuildRequestRecords включаются ключи tunnel и AES reply, но ключи ChaCha reply выводятся из DH обмена. См. [Prop156](/proposals/156/) для подробностей о статических ECIES ключах router.

Ниже приведено описание того, как вывести ключи, ранее переданные в записях запросов.

#### KDF для начальных ck и h

Это стандартный [NOISE](https://noiseprotocol.org/noise.html) для паттерна "N" со стандартным именем протокола.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
(31 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
// Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
h = protocol_name || 0

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by all routers.
```
#### KDF для записи запроса

ElGamal создатели tunnel генерируют эфемерную X25519 keypair для каждого ECIES hop в tunnel и используют вышеописанную схему для шифрования своего BuildRequestRecord. ElGamal создатели tunnel будут использовать схему, предшествующую данной спецификации, для шифрования к ElGamal hops.

Создатели туннелей ECIES должны будут шифровать для каждого из публичных ключей узла ElGamal, используя схему, определенную в [Tunnel-Creation](/docs/specs/tunnel-creation/). Создатели туннелей ECIES будут использовать вышеуказанную схему для шифрования к узлам ECIES.

Это означает, что tunnel-хопы будут видеть только зашифрованные записи своего же типа шифрования.

Для создателей туннелей ElGamal и ECIES они будут генерировать уникальные эфемерные пары ключей X25519 для каждого хопа при шифровании для хопов ECIES.

**ВАЖНО**: Эфемерные ключи должны быть уникальными для каждого ECIES hop и для каждой записи сборки. Неиспользование уникальных ключей открывает вектор атаки для сговаривающихся hop, позволяя им подтвердить, что они находятся в одном tunnel.

```
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
hesk = GENERATE_PRIVATE()
hepk = DERIVE_PUBLIC(hesk)

// MixHash(hepk)
// || below means append
h = SHA256(h || hepk);

// up until here, can all be precalculated by each router
// for all incoming build requests

// Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
sesk = GENERATE_PRIVATE()
sepk = DERIVE_PUBLIC(sesk)

// MixHash(sepk)
h = SHA256(h || sepk);

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
// Sender performs an X25519 DH with Hop's static public key.
// Each Hop, finds the record w/ their truncated identity hash,
// and extracts the Sender's ephemeral key preceding the encrypted record.
sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
// Save for Reply Record KDF
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
plaintext = 464 byte build request record
ad = h
ciphertext = ENCRYPT(k, n, plaintext, ad)

End of "es" message pattern.

// MixHash(ciphertext)
// Save for Reply Record KDF
h = SHA256(h || ciphertext)
```
`replyKey`, `layerKey` и `layerIV` по-прежнему должны быть включены в записи ElGamal и могут генерироваться случайным образом.

### Шифрование записи ответа

Запись ответа зашифрована с помощью ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Спецификация коротких записей

Эта спецификация использует два новых I2NP сообщения построения туннеля: Short Tunnel Build Message (тип 25) и Outbound Tunnel Build Reply Message (тип 26).

Создатель tunnel и все промежуточные узлы в созданном tunnel должны поддерживать ECIES-X25519 и быть версии не ниже 0.9.51. Промежуточные узлы в tunnel для ответа (для исходящей сборки) или исходящий tunnel (для входящей сборки) не имеют никаких требований.

Зашифрованные записи запросов и ответов будут составлять 218 байт по сравнению с 528 байтами для всех других сообщений сборки.

Записи запросов в открытом виде будут составлять 154 байта по сравнению с 222 байтами для записей ElGamal и 464 байтами для записей ECIES, как определено выше.

Записи ответа в открытом тексте будут составлять 202 байта по сравнению с 496 байтами для записей ElGamal и 512 байтами для записей ECIES, как определено выше.

Шифрование ответа будет использовать ChaCha20/Poly1305 для собственной записи узла (hop) и ChaCha20 (НЕ ChaCha20/Poly1305) для других записей в сообщении сборки.

Записи запросов будут уменьшены за счет использования HKDF для создания ключей уровня и ответа, поэтому они не будут явно включены в запрос.

### Поток сообщений

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Примечания

Garlic-упаковка сообщений скрывает их от OBEP (для входящей сборки) или IBGW (для исходящей сборки). Это рекомендуется, но не обязательно. Если OBEP и IBGW являются одним и тем же router, это не требуется.

### Короткие записи запросов на сборку

Короткие зашифрованные BuildRequestRecords составляют 218 байт.

#### Короткая запись запроса без шифрования

Сводка изменений по длинным записям:

- Изменить длину нешифрованных данных с 464 до 154 байт
- Изменить длину зашифрованных данных с 528 до 218 байт
- Удалить ключи слоев и ответов, а также IV, они будут генерироваться из KDF

Запись запроса не содержит ключей ответа ChaCha. Эти ключи получаются из KDF. См. ниже.

Все поля имеют порядок байтов big-endian.

Незашифрованный размер: 154 байта.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Поле флагов аналогично определённому в [Tunnel-Creation](/docs/specs/tunnel-creation/) и содержит следующее:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Бит 7 указывает, что хоп будет входящим шлюзом (IBGW). Бит 6 указывает, что хоп будет исходящей конечной точкой (OBEP). Если ни один из битов не установлен, хоп будет промежуточным участником. Оба бита не могут быть установлены одновременно.

Тип шифрования слоя: 0 для AES (как в текущих tunnel); 1 для будущего (ChaCha?)

Срок действия запроса предназначен для переменной продолжительности tunnel в будущем. На данный момент единственное поддерживаемое значение — 600 (10 минут).

Эфемерный открытый ключ создателя — это ECIES ключ в формате big-endian. Он используется для функции вывода ключей (KDF) для слоя IBGW и ключей ответа и векторов инициализации. Это включается только в запись открытого текста в сообщении Inbound Tunnel Build. Это требуется, поскольку на этом слое нет обмена Диффи-Хеллмана для записи сборки.

Опции построения tunnel представляют собой структуру Mapping, как определено в [Common](/docs/specs/common-structures/). Единственными опциями, определенными в настоящее время, являются параметры пропускной способности, начиная с API 0.9.65, подробности см. ниже. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) составляет 98 байт, а максимальное значение поля длины Mapping равно 96.

#### Зашифрованная краткая запись запроса

Все поля представлены в формате big-endian, за исключением эфемерного открытого ключа, который представлен в формате little-endian.

Зашифрованный размер: 218 байт

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Записи коротких ответов на построение

Короткие зашифрованные BuildReplyRecords имеют размер 218 байт.

#### Запись короткого ответа без шифрования

Сводка изменений из длинных записей:

- Изменить незашифрованную длину с 512 до 202 байт
- Изменить зашифрованную длину с 528 до 218 байт

ECIES ответы шифруются с помощью ChaCha20/Poly1305.

Все поля имеют прямой порядок байтов (big-endian).

Размер незашифрованных данных: 202 байта.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Опции ответа на построение tunnel представляют собой структуру Mapping, как определено в [Common](/docs/specs/common-structures/). Единственные опции, определенные на данный момент, предназначены для параметров пропускной способности, начиная с API 0.9.65, подробности см. ниже. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) составляет 201 байт, а максимальное значение поля длины Mapping равно 199.

Байт ответа принимает одно из следующих значений, как определено в [Tunnel-Creation](/docs/specs/tunnel-creation/) для предотвращения фингерпринтинга:

- 0x00 (принять)
- 30 (TUNNEL_REJECT_BANDWIDTH)

В будущем может быть определено дополнительное значение ответа для представления отклонения неподдерживаемых опций.

#### Зашифрованная запись короткого ответа

Размер зашифрованного: 218 байт

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Мы используем ключ связывания (ck) из состояния Noise после шифрования/расшифровки записи построения tunnel для вывода следующих ключей: ключ ответа, ключ слоя AES, ключ AES IV и ключ/тег ответа garlic encryption для OBEP.

Ключи ответа: Обратите внимание, что KDF немного отличается для OBEP и не-OBEP переходов. В отличие от длинных записей, мы не можем использовать левую часть ck для ключа ответа, поскольку это не последний переход и он будет использован позже. Ключ ответа используется для шифрования ответа этой записи с помощью AEAD/ChaCha20/Poly1305 и ChaCha20 для ответа другим записям. Оба используют один и тот же ключ. Nonce - это позиция записи в сообщении, начиная с 0. Подробности см. ниже.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Примечание: KDF для IV-ключа в OBEP отличается от KDF для других участков пути, даже если ответ не зашифрован с помощью garlic encryption.

#### Шифрование записей

Собственная запись ответа хопа шифруется с помощью ChaCha20/Poly1305. Это то же самое, что и в спецификации длинной записи выше, ЗА ИСКЛЮЧЕНИЕМ того, что 'n' — это номер записи 0-7, а не всегда 0. См. [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Остальные записи итеративно и симметрично шифруются на каждом узле с помощью ChaCha20 (НЕ ChaCha20/Poly1305). Это отличается от спецификации длинных записей выше, которая использует AES и не использует номер записи.

Номер записи помещается в IV на байте 4, поскольку ChaCha20 использует 12-байтный IV с little-endian nonce на байтах 4-11. См. [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

Garlic-обертывание сообщений скрывает их от OBEP (для входящей сборки) или IBGW (для исходящей сборки). Это рекомендуется, но не обязательно. Если OBEP и IBGW являются одним и тем же router, это не необходимо.

Garlic encryption входящего Short Tunnel Build Message создателем, зашифрованного для ECIES IBGW, использует шифрование Noise 'N', как определено в [ECIES-ROUTERS](/docs/specs/ecies-routers/).

Garlic encryption исходящего сообщения Tunnel Build Reply Message от OBEP, зашифрованного для создателя, использует сообщения Existing Session с 32-байтным ключом garlic reply key и 8-байтным тегом garlic reply tag из KDF выше. Формат соответствует спецификации для ответов на Database Lookups в [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/) и [ECIES-X25519](/docs/specs/ecies/).

#### Слоевое шифрование

Данная спецификация включает поле типа шифрования слоя в записи запроса на построение. Единственное шифрование слоя, которое в настоящее время поддерживается, это тип 0, то есть AES. Это не изменилось по сравнению с предыдущими спецификациями, за исключением того, что ключ слоя и ключ IV выводятся из указанной выше KDF, а не включаются в запись запроса на построение.

Добавление новых типов шифрования уровня, например ChaCha20, является темой для дополнительных исследований и в настоящее время не является частью данной спецификации.

## Примечания по реализации

- Старые router не проверяют тип шифрования hop и будут отправлять записи, зашифрованные ElGamal. Некоторые недавние router содержат ошибки и будут отправлять различные типы неправильно сформированных записей. Разработчики должны обнаруживать и отклонять эти записи до операции DH, если это возможно, чтобы снизить использование CPU.

### Записи сборки

Порядок записей сборки должен быть рандомизирован, чтобы промежуточные узлы не знали своего местоположения в tunnel.

Рекомендуемое минимальное количество записей сборки составляет 4. Если записей сборки больше, чем переходов, необходимо добавить "фиктивные" записи, содержащие случайные или специфичные для реализации данные. Для сборки входящих tunnel всегда должна быть одна "фиктивная" запись для исходного router с правильным 16-байтным префиксом хеша и настоящим эфемерным ключом X25519, иначе ближайший переход узнает, что следующий переход является инициатором.

Остальная часть "поддельной" записи может содержать случайные данные или может быть зашифрована в любом формате, чтобы инициатор мог отправить данные самому себе о сборке, возможно, для уменьшения требований к хранилищу для ожидающих сборок.

Инициаторы входящих tunnel должны использовать какой-либо метод для проверки того, что их "поддельная" запись не была изменена предыдущим узлом, поскольку это также может быть использовано для деанонимизации. Инициатор может сохранить и проверить контрольную сумму записи, или включить контрольную сумму в запись, или использовать функцию AEAD шифрования/расшифрования, в зависимости от реализации. Если 16-байтовый префикс хеша или другое содержимое записи сборки было изменено, router должен отбросить tunnel.

Поддельные записи для исходящих tunnel и дополнительные поддельные записи для входящих tunnel не имеют этих требований и могут содержать полностью случайные данные, поскольку они никогда не будут видны ни одному узлу. Тем не менее, отправителю может быть желательно проверить, что они не были изменены.

## Параметры пропускной способности tunnel

### Обзор

По мере того, как мы повышали производительность сети в течение последних нескольких лет с помощью новых протоколов, типов шифрования и улучшений контроля перегрузки, стали возможными более быстрые приложения, такие как потоковая передача видео. Эти приложения требуют высокой пропускной способности на каждом переходе в их клиентских tunnel.

Участвующие router, однако, не имеют никакой информации о том, какую пропускную способность будет использовать tunnel, когда они получают сообщение о построении tunnel. Они могут только принять или отклонить tunnel на основе текущей общей пропускной способности, используемой всеми участвующими tunnel, и общего лимита пропускной способности для участвующих tunnel.

Router'ы, выполняющие запросы, также не имеют информации о том, какая пропускная способность доступна на каждом узле.

Кроме того, router в настоящее время не имеют возможности ограничивать входящий трафик в tunnel. Это было бы весьма полезно во время перегрузки или DDoS-атак на сервис.

Параметры пропускной способности tunnel в сообщениях запроса и ответа на создание tunnel добавляют поддержку этих функций. См. [Prop168](/proposals/168/) для дополнительной информации. Эти параметры определены начиная с API 0.9.65, но поддержка может варьироваться в зависимости от реализации. Они поддерживаются как для длинных, так и для коротких записей сборки ECIES.

### Параметры запроса сборки

Следующие три опции могут быть установлены в поле mapping параметров построения туннеля записи: Запрашивающий router может включить любые, все или ни одной из них.

- m := минимальная пропускная способность, требуемая для этого tunnel (KBps положительное целое число в виде строки)
- r := запрашиваемая пропускная способность для этого tunnel (KBps положительное целое число в виде строки)
- l := ограничение пропускной способности для этого tunnel; отправляется только IBGW (KBps положительное целое число в виде строки)

Ограничение: m <= r <= l

Участвующий router должен отклонить tunnel, если указано "m" и он не может обеспечить как минимум такую пропускную способность.

Параметры запроса отправляются каждому участнику в соответствующей зашифрованной записи запроса на построение и не видны другим участникам.

### Опция Ответа Сборки

Следующая опция может быть установлена в поле mapping параметров ответа на построение tunnel в записи, когда ответ ACCEPTED:

- b := пропускная способность, доступная для этого tunnel (положительное целое число в KBps в виде строки)

Ограничение: b >= m

Участвующий router должен включить это, если в запросе сборки было указано "m" или "r". Значение должно быть не меньше значения "m", если оно указано, но может быть меньше или больше значения "r", если оно указано.

Участвующий router должен попытаться зарезервировать и предоставить как минимум такую пропускную способность для tunnel, однако это не гарантируется. Router'ы не могут предсказать условия на 10 минут вперед, а участвующий трафик имеет более низкий приоритет, чем собственный трафик и tunnel'и router'а.

Router-ы также могут при необходимости выделять больше доступной пропускной способности, чем имеется, и это, вероятно, желательно, поскольку другие промежуточные узлы в tunnel могут отклонить его.

По этим причинам ответ участвующего router следует рассматривать как обязательство по принципу "лучших усилий", но не как гарантию.

Параметры ответа отправляются запрашивающему router в соответствующей зашифрованной записи ответа на построение и не видны другим участникам.

### Примечания к реализации

Параметры пропускной способности отображаются на участвующих router'ах на уровне tunnel, то есть количество сообщений tunnel фиксированного размера 1 КБ в секунду. Накладные расходы транспорта (NTCP2 или SSU2) не учитываются.

Эта пропускная способность может быть намного больше или меньше пропускной способности, наблюдаемой у клиента. Сообщения tunnel содержат значительные накладные расходы, включая накладные расходы от верхних уровней, включая ratchet и streaming. Прерывистые небольшие сообщения, такие как подтверждения streaming, будут расширены до 1 КБ каждое. Однако сжатие gzip на уровне I2CP может существенно снизить пропускную способность.

Самая простая реализация на запрашивающем router заключается в использовании средней, минимальной и/или максимальной пропускной способности текущих tunnel в пуле для расчета значений, которые нужно поместить в запрос. Возможны более сложные алгоритмы, и их выбор остается на усмотрение разработчика.

В настоящее время не определены параметры I2CP или SAM, которые клиент мог бы использовать для указания router'у требуемой пропускной способности, и в данном документе не предлагается новых параметров. При необходимости параметры могут быть определены позднее.

Реализации могут использовать доступную пропускную способность или любые другие данные, алгоритм, локальную политику или локальную конфигурацию для вычисления значения пропускной способности, возвращаемого в ответе на запрос построения.

## Ссылки

- [Общие структуры](/docs/specs/common-structures/)
- [Криптография](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Множественное шифрование](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Создание tunnel](/docs/specs/tunnel-creation/)
