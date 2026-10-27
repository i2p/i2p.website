---
title: "ECIES Tunnels"
aliases:
  - "/ru/proposals/152-ecies-config"
  - "/ru/proposals/152-ecies-config/"
  - "/ru/proposals/152"
  - "/ru/proposals/152/"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Примечание

Сетевое развертывание и тестирование в процессе. Возможны незначительные правки. См. [SPEC](/docs/specs/tunnel-implementation/) для официальной спецификации.

## Обзор

В этом документе предлагаются изменения шифрования сообщений создания туннеля с использованием криптографических примитивов, введенных [ECIES-X25519](/docs/specs/ecies/). Это часть общего предложения [Предложение 156](/proposals/156-ecies-routers) по переходу маршрутизаторов с ElGamal на ключи ECIES-X25519.

Для целей перехода сети с ElGamal + AES256 на ECIES + ChaCha20 необходимы туннели со смешанными узлами ElGamal и ECIES. Предоставлены спецификации обработки прыжков в смешанных туннелях. Никаких изменений в формат, обработку или шифрование прыжков ElGamal вноситься не будет.

Создателям туннелей ElGamal потребуется создавать временные ключевые пары X25519 на каждый прыжок и следовать данной спецификации при создании туннелей, содержащих прыжки ECIES.

В этом предложении описываются изменения, необходимые для создания туннелей ECIES-X25519. Для общего обзора всех изменений, необходимых для маршрутизаторов ECIES, см. предложение 156 [Предложение 156](/proposals/156-ecies-routers).

В этом предложении сохраняется тот же размер записей создания туннеля, что требуется для совместимости. Более мелкие записи и сообщения будут реализованы позже — см. [Предложение 157](/proposals/157-new-tbm).

### Криптографические примитивы

Новые криптографические примитивы не вводятся. Примитивы, необходимые для реализации этого предложения:

- AES-256-CBC как в [Cryptography](/docs/specs/cryptography/)
- STREAM ChaCha20/Poly1305 функции:
  ENCRYPT(k, n, plaintext, ad) и DECRYPT(k, n, ciphertext, ad) — как в [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) и [RFC-7539](https://tools.ietf.org/html/rfc7539)
- X25519 DH функции — как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) — как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)

Другие функции Noise, определённые в других местах:

- MixHash(d) — как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) — как в [NTCP2](/docs/specs/ntcp2/) и [ECIES-X25519](/docs/specs/ecies/)

### Цели

- Увеличение скорости криптографических операций
- Замена ElGamal + AES256/CBC на примитивы ECIES для BuildRequestRecords и BuildReplyRecords туннеля.
- Без изменений размера зашифрованных BuildRequestRecords и BuildReplyRecords (528 байт) для совместимости
- Без новых сообщений I2NP
- Сохранение размера зашифрованной записи создания туннеля для совместимости
- Добавление сквозной секретности для сообщений создания туннеля.
- Добавление аутентифицированного шифрования
- Обнаружение переупорядочивания BuildRequestRecords узлами
- Повышение разрешения временной метки, чтобы можно было уменьшить размер фильтра Блума
- Добавление поля истечения срока действия туннеля, чтобы стали возможны разные сроки жизни туннелей (только для полностью ECIES-туннелей)
- Добавление расширяемого поля опций для будущих функций
- Повторное использование существующих криптографических примитивов
- Улучшение безопасности сообщений создания туннеля, где это возможно, при сохранении совместимости
- Поддержка туннелей со смешанными узлами ElGamal/ECIES
- Улучшение защиты от атак «маркировки» (tagging) на сообщениях создания туннеля
- Узлам не нужно знать тип шифрования следующего прыжка до обработки сообщения создания туннеля,
  так как у них может не быть RI следующего узла в этот момент
- Максимальная совместимость с текущей сетью
- Без изменений в шифровании AES запросов/ответов для создания туннеля на маршрутизаторах ElGamal
- Без изменений в «слоевом» шифровании AES туннеля, для этого см. [Предложение 153](/proposals/153-chacha20-layer-encryption)
- Продолжение поддержки как 8-записных TBM/TBRM, так и переменных VTBM/VTBRM
- Не требует одновременного обновления всей сети («flag day»)

### Нецели

- Полная переработка сообщений создания туннеля, требующая «flag day».
- Уменьшение сообщений создания туннеля (требует всех прыжков ECIES и нового предложения)
- Использование опций создания туннеля, как определено в [Предложение 143](/proposals/143-build-message-options), требуется только для малых сообщений
- Двунаправленные туннели — для этого см. [Предложение 119](/proposals/119-bidirectional-tunnels)
- Уменьшение сообщений создания туннеля — для этого см. [Предложение 157](/proposals/157-new-tbm)

## Модель угроз

### Цели проектирования

- Ни один из узлов не может определить инициатора туннеля.

- Промежуточные узлы не должны определять направление туннеля
  или свою позицию в туннеле.

- Ни один узел не может читать содержимое других запросов или ответов, кроме
  усечённого хэша маршрутизатора и временного ключа для следующего узла

- Ни один участник обратного туннеля для исходящего создания не может читать записи ответов.

- Ни один участник исходящего туннеля для входящего создания не может читать записи запросов,
  за исключением того, что OBEP может видеть усечённый хэш маршрутизатора и временный ключ для IBGW

### Атаки маркировки (tagging)

Основная цель проектирования создания туннеля — затруднить маршрутизаторам X и Y, действующим сообща, определить, что они находятся в одном туннеле. Если маршрутизатор X находится на прыжке m, а маршрутизатор Y — на прыжке m+1, они, очевидно, узнают это. Но если маршрутизатор X на прыжке m, а маршрутизатор Y на прыжке m+n при n>1, это должно быть намного сложнее.

Атаки маркировки — это когда промежуточный узел X изменяет сообщение создания туннеля таким образом, что маршрутизатор Y может обнаружить изменение, когда сообщение дойдёт до него. Цель — чтобы любое изменённое сообщение было отброшено маршрутизатором между X и Y до того, как достигнет Y. Для изменений, которые не были отброшены до маршрутизатора Y, создатель туннеля должен обнаружить повреждение в ответе и отбросить туннель.

Возможные атаки:

- Изменение записи создания
- Замена записи создания
- Добавление или удаление записи создания
- Переупорядочивание записей создания

TODO: Предотвращает ли текущая схема все эти атаки?

## Проектирование

### Фреймворк протокола Noise

Это предложение определяет требования на основе фреймворка протокола Noise [NOISE](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11). В терминологии Noise, Алиса — инициатор, а Боб — ответчик.

Это предложение основано на протоколе Noise Noise_N_25519_ChaChaPoly_SHA256. Этот протокол Noise использует следующие примитивы:

- Односторонний шаблон рукопожатия: N
  Алиса не передаёт свой статический ключ Бобу (N)

- Функция DH: X25519
  X25519 DH с длиной ключа 32 байта, как указано в [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Функция шифрования: ChaChaPoly
  AEAD_CHACHA20_POLY1305 как указано в [RFC-7539](https://tools.ietf.org/html/rfc7539) раздел 2.8.
  12-байтовый nonce, первые 4 байта установлены в ноль.
  Идентично тому, что в [NTCP2](/docs/specs/ntcp2/).

- Хэш-функция: SHA256
  Стандартный 32-байтовый хэш, уже широко используется в I2P.

#### Дополнения к фреймворку

Отсутствуют.

### Шаблоны рукопожатия

Рукопожатия используют шаблоны [Noise](https://noiseprotocol.org/noise.html).

Используется следующее буквенно-символьное соответствие:

- e = одноразовый временный ключ
- s = статический ключ
- p = полезная нагрузка

Запрос создания идентичен шаблону Noise N. Это также идентично первому сообщению (Session Request) в шаблоне XK, используемом в [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Шифрование запроса

Записи запроса создания туннеля создаются создателем туннеля и асимметрично шифруются для отдельного прыжка. Это асимметричное шифрование записей запроса в настоящее время — ElGamal, как определено в [Cryptography](/docs/specs/cryptography/) и содержит контрольную сумму SHA-256. Эта схема не является сквозной по секретности.

Новая схема будет использовать односторонний шаблон Noise "N" с ECIES-X25519 (временный-статический DH), с HKDF и AEAD ChaCha20/Poly1305 для сквозной секретности, целостности и аутентификации. Алиса — это инициатор создания туннеля. Каждый прыжок в туннеле — это Боб.

(Свойства безопасности полезной нагрузки)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Шифрование ответа

Записи ответа создания туннеля создаются создателем прыжков и симметрично шифруются для создателя. Это симметричное шифрование записей ответа в настоящее время — AES с предваряющей контрольной суммой SHA-256. и содержит контрольную сумму SHA-256. Эта схема не является сквозной по секретности.

Новая схема будет использовать AEAD ChaCha20/Poly1305 для целостности и аутентификации.

### Обоснование

Временный открытый ключ в запросе не нуждается в маскировке с помощью AES или Elligator2. Только предыдущий прыжок может его видеть, и он знает, что следующий прыжок использует ECIES.

Записям ответа не требуется полное асимметричное шифрование с другим DH.

## Спецификация

### Записи запроса создания

Зашифрованные BuildRequestRecords имеют размер 528 байт как для ElGamal, так и для ECIES, для совместимости.

#### Запись запроса, незашифрованная (ElGamal)

Для справки, это текущая спецификация записи BuildRequestRecord для маршрутизаторов ElGamal, взятая из [I2NP](/docs/specs/i2np/). Незашифрованные данные дополняются ненулевым байтом и хэшем SHA-256 данных перед шифрованием, как определено в [Cryptography](/docs/specs/cryptography/).

Все поля big-endian.

Незашифрованный размер: 222 байта

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Запись запроса, зашифрованная (ElGamal)

Для справки, это текущая спецификация записи BuildRequestRecord для маршрутизаторов ElGamal, взятая из [I2NP](/docs/specs/i2np/).

Зашифрованный размер: 528 байт

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Запись запроса, незашифрованная (ECIES)

Это предлагаемая спецификация записи BuildRequestRecord для маршрутизаторов ECIES-X25519. Краткое описание изменений:

- Удалён неиспользуемый 32-байтовый хэш маршрутизатора
- Изменение времени запроса с часов на минуты
- Добавление поля истечения срока для будущих переменных сроков жизни туннеля
- Добавление дополнительного места для флагов
- Добавление сопоставления (Mapping) для дополнительных опций создания
- Ключи ответа AES-256 не используются для собственной записи ответа прыжка
- Незашифрованная запись длиннее, так как накладные расходы на шифрование меньше

Запись запроса не содержит ключей ответа ChaCha. Эти ключи выводятся из KDF. См. ниже.

Все поля big-endian.

Незашифрованный размер: 464 байта

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Поле флагов такое же, как определено в [Tunnel Creation](/docs/specs/tunnel-implementation/) и содержит следующее::

```text
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Порядок битов: 76543210 (бит 7 — старший)  бит 7: если установлен, разрешает сообщения от любого  бит 6: если установлен, разрешает сообщения любому и отправляет ответ

биты 5-0: Не определены, должны быть установлены в 0 для совместимости с будущими опциями

Бит 7 указывает, что прыжок будет входным шлюзом (IBGW). Бит 6 указывает, что прыжок будет исходной точкой (OBEP). Если ни один бит не установлен, прыжок будет промежуточным участником. Оба не могут быть установлены одновременно.

#### Запись запроса, зашифрованная (ECIES)

Истечение срока запроса предназначено для будущих переменных сроков жизни туннеля. Сейчас единственное поддерживаемое значение — 600 (10 минут).

Опции создания туннеля — это структура Mapping, как определено в [Common Structures](/docs/specs/common-structures/). Это для будущего использования. Опции в настоящее время не определены. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) — 296 байт, а максимальное значение поля длины Mapping — 294.

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Записи ответа создания

Все поля big-endian, кроме временного открытого ключа, который little-endian.

#### Запись ответа, незашифрованная (ElGamal)

Зашифрованный размер: 528 байт

Зашифрованные BuildReplyRecords имеют размер 528 байт как для ElGamal, так и для ECIES, для совместимости.

Ответы ElGamal шифруются с помощью AES.

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Запись ответа, незашифрованная (ECIES)

Все поля big-endian.

- Добавление Mapping для опций ответа создания туннеля
- Незашифрованная запись длиннее, так как накладные расходы на шифрование меньше

Незашифрованный размер: 528 байт

Это предлагаемая спецификация записи BuildReplyRecord для маршрутизаторов ECIES-X25519. Краткое описание изменений:

Ответы ECIES шифруются с помощью ChaCha20/Poly1305.

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Все поля big-endian.

Незашифрованный размер: 512 байт

- 0x00 (принять)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Запись ответа, зашифрованная (ECIES)

Опции ответа создания туннеля — это структура Mapping, как определено в [Common Structures](/docs/specs/common-structures/). Это для будущего использования. Опции в настоящее время не определены. Если структура Mapping пуста, это два байта 0x00 0x00. Максимальный размер Mapping (включая поле длины) — 511 байт, а максимальное значение поля длины Mapping — 509.

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Байт ответа — один из следующих значений, как определено в [Tunnel Creation](/docs/specs/tunnel-implementation/), чтобы избежать фингерпринтинга:

### Симметричное шифрование записей

Зашифрованный размер: 528 байт

После полного перехода на записи ECIES, правила заполнения остаются такими же, как и для записей запроса.

- «шифрование»:

  - шифр работает в режиме расшифровки
  - записи запроса предварительно расшифровываются на этапе предварительной обработки (скрывая зашифрованные записи запроса)

- «расшифровка»:

  - шифр работает в режиме шифрования
  - записи запроса шифруются (раскрывая следующую запись запроса в открытом виде) узлами-участниками

- ChaCha20 не имеет «режимов», поэтому он просто запускается три раза:

  - один раз на предварительной обработке
  - один раз узлом
  - один раз при окончательной обработке ответа

Смешанные туннели разрешены и необходимы для перехода с ElGamal на ECIES. Во время переходного периода всё больше маршрутизаторов будет использовать ключи ECIES.

Предварительная обработка симметричной криптографии будет работать одинаково:

При использовании смешанных туннелей создатели туннелей должны основывать симметричное шифрование BuildRequestRecord на типе шифрования текущего и предыдущего прыжка.

Каждый прыжок будет использовать свой собственный тип шифрования для шифрования BuildReplyRecords и других записей в VariableTunnelBuildMessage (VTBM).

- Отправитель (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

На обратном пути конечная точка (отправитель) должна будет отменить [Multiple Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), используя ключ ответа каждого прыжка.

В качестве поясняющего примера рассмотрим исходящий туннель с ECIES, окружённый ElGamal:

Все BuildRequestRecords находятся в зашифрованном состоянии (с использованием ElGamal или ECIES).

AES256/CBC, при использовании, по-прежнему применяется к каждой записи отдельно, без объединения нескольких записей.

- Запись H3 «шифруется» с использованием:

  - ключа ответа H2 (ChaCha20)
  - ключа ответа H1 (AES256/CBC)

- Запись H2 «шифруется» с использованием:

  - ключа ответа H1 (AES256/CBC)

- Запись H1 отправляется без симметричного шифрования

Аналогично, ChaCha20 будет использоваться для шифрования каждой записи, а не потокового шифрования всего VTBM.

Записи запроса предварительно обрабатываются отправителем (OBGW):

- Запись H3 «расшифровывается» с использованием:

  - ключа ответа H3 (AES256/CBC)

- Запись H2 «расшифровывается» с использованием:

  - ключа ответа H3 (AES256/CBC)
  - ключа ответа H2 (ChaCha20-Poly1305)

- Запись H1 «расшифровывается» с использованием:

  - ключа ответа H3 (AES256/CBC)
  - ключа ответа H2 (ChaCha20)
  - ключа ответа H1 (AES256/CBC)

Только H2 проверяет флаг шифрования ответа и видит, что за ним следует AES256/CBC.

- Запись H3 «шифруется» с использованием:

  - ключа ответа H3 (AES256/CBC)

- Запись H2 «шифруется» с использованием:

  - ключа ответа H3 (AES256/CBC)
  - ключа ответа H2 (ChaCha20-Poly1305)

- Запись H1 «шифруется» с использованием:

  - ключа ответа H3 (AES256/CBC)
  - ключа ответа H2 (ChaCha20)
  - ключа ответа H1 (AES256/CBC)

### Ключи записи запроса (ECIES)

После обработки каждым прыжком записи находятся в «расшифрованном» состоянии:

Создатель туннеля, т.е. конечная точка входа (IBEP), постобрабатывает ответ:

#### KDF для начальных ck и h

Эти ключи явно включены в записи BuildRequestRecords ElGamal. Для записей BuildRequestRecords ECIES включены ключи туннеля и ключи ответа AES, но ключи ответа ChaCha выводятся из обмена DH. См. [Предложение 156](/proposals/156-ecies-routers) для деталей статических ключей ECIES маршрутизатора.

```text
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

Ниже приведено описание способа вывода ключей, ранее передаваемых в записях запроса.

Это стандартный [NOISE](https://noiseprotocol.org/noise.html) для шаблона "N" со стандартным именем протокола.

Создатели туннелей ElGamal генерируют временную пару ключей X25519 для каждого прыжка ECIES в туннеле и используют указанную выше схему для шифрования своей записи BuildRequestRecord. Создатели туннелей ElGamal будут использовать схему, описанную до этой спецификации, для шифрования прыжков ElGamal.

Создателям туннелей ECIES нужно будет шифровать каждый из открытых ключей прыжков ElGamal по схеме, определённой в [Tunnel Creation](/docs/specs/tunnel-implementation/). Создатели туннелей ECIES будут использовать указанную выше схему для шифрования прыжков ECIES.

Это означает, что прыжки будут видеть зашифрованные записи только от прыжков с тем же типом шифрования.

```text
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
Для создателей туннелей ElGamal и ECIES они будут генерировать уникальные временные пары ключей X25519 на прыжок для шифрования прыжков ECIES.

### Шифрование записи запроса (ElGamal)

**ВАЖНО**: Временные ключи должны быть уникальны для каждого прыжка ECIES и для каждой записи создания. Несоблюдение этого правила открывает вектор атаки для сообщающихся прыжков подтвердить, что они находятся в одном туннеле.

### Шифрование записи ответа (ECIES)

``replyKey``, ``layerKey`` и ``layerIV`` по-прежнему должны быть включены внутрь записей ElGamal и могут генерироваться случайным образом.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Шифрование записи ответа (ElGamal)

Как определено в [Tunnel Creation](/docs/specs/tunnel-implementation/). Никаких изменений в шифровании для прыжков ElGamal не вносится.

### Анализ безопасности

Запись ответа шифруется с помощью ChaCha20/Poly1305.

Как определено в [Tunnel Creation](/docs/specs/tunnel-implementation/). Никаких изменений в шифровании для прыжков ElGamal не вносится.

ElGamal не обеспечивает сквозную секретность для сообщений создания туннеля.

AES256/CBC находится в немного лучшем положении, будучи уязвимым только к теоретическому ослаблению из-за атаки с известным открытым текстом `biclique`.

Единственная известная практическая атака против AES256/CBC — это атака с оракулом заполнения, когда IV известен атакующему.

Атакующему нужно будет взломать шифрование ElGamal следующего прыжка, чтобы получить информацию о ключе AES256/CBC (ключ ответа и IV).

ElGamal значительно более ресурсоёмок по CPU, чем ECIES, что ведёт к возможному истощению ресурсов.

## Обоснование

ECIES, используемый с новыми временными ключами на каждую BuildRequestRecord или VariableTunnelBuildMessage, обеспечивает сквозную секретность.

## Примечания по реализации

* Старые маршрутизаторы не проверяют тип шифрования прыжка и будут отправлять зашифрованные ElGamal
  записи. Некоторые недавние маршрутизаторы имеют ошибки и будут отправлять различные типы повреждённых записей.
  Реализаторам следует обнаруживать и отклонять такие записи до операции DH,
  если возможно, чтобы снизить нагрузку на CPU.

## Проблемы

## Миграция

ChaCha20Poly1305 обеспечивает AEAD-шифрование, позволяя получателю проверить целостность сообщения до попытки расшифровки.

## Ссылки

* [Common](/docs/specs/common-structures/)
* [Cryptography](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Tunnel-Creation](/docs/specs/tunnel-implementation/#tunnel-creation-ecies)
* [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
