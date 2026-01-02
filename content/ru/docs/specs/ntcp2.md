---
title: "Транспорт NTCP2"
description: "TCP-транспорт на основе Noise для соединений router-to-router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Обзор

NTCP2 заменяет устаревший транспорт NTCP рукопожатием на базе протокола Noise, которое устойчиво к фингерпринтингу трафика, шифрует поля длины и поддерживает современные наборы шифров. Routers могут запускать NTCP2 вместе с SSU2 как два обязательных транспортных протокола в сети I2P. NTCP (версия 1) был объявлен устаревшим в 0.9.40 (май 2019) и полностью удалён в 0.9.50 (май 2021).

## Фреймворк протоколов Noise

NTCP2 использует фреймворк протокола Noise [Ревизия 33, 2017-10-04](https://noiseprotocol.org/noise.html) с расширениями, специфичными для I2P:

- **Шаблон**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Расширенный идентификатор**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (для инициализации KDF (функции выработки ключей))
- **Функция DH**: X25519 (RFC 7748) - 32-байтные ключи, кодирование little-endian
- **Шифр**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - 12-байтный nonce (одноразовое значение): первые 4 байта — нули, последние 8 байт — счетчик (little-endian)
  - Максимальное значение nonce: 2^64 - 2 (соединение должно быть завершено до достижения 2^64 - 1)
- **Хеш-функция**: SHA-256 (32-байтный вывод)
- **MAC**: Poly1305 (16-байтный тег аутентификации)

### Расширения, специфичные для I2P

1. **AES-обфускация**: Эфемерные ключи зашифрованы с помощью AES-256-CBC с использованием хеша router Боба и опубликованного IV
2. **Случайный паддинг**: Паддинг в открытом виде в сообщениях 1-2 (аутентифицирован), паддинг AEAD в сообщениях 3+ (зашифрован)
3. **Обфускация длины SipHash-2-4**: Двухбайтовые длины кадров побитово складываются по XOR с выходом SipHash
4. **Структура кадров**: Кадры с префиксом длины для фазы данных (совместимость с потоковой передачей по TCP)
5. **Блочно-ориентированные полезные данные**: Структурированный формат данных с типизированными блоками

## Последовательность рукопожатия

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Рукопожатие из трех сообщений

1. **SessionRequest** - замаскированный эфемерный ключ Алисы, параметры, подсказки по padding (заполнению)
2. **SessionCreated** - замаскированный эфемерный ключ Боба, зашифрованные параметры, padding
3. **SessionConfirmed** - зашифрованный статический ключ Алисы и RouterInfo (два AEAD-фрейма)

### Шаблоны сообщений Noise

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Уровни аутентификации:** - 0: Без аутентификации (кто угодно мог отправить) - 2: Аутентификация отправителя, устойчивая к key-compromise impersonation (KCI, подмене личности при компрометации ключа)

**Уровни конфиденциальности:** - 1: Эфемерный получатель (прямая секретность, без аутентификации получателя) - 2: Известный получатель, прямая секретность только при компрометации отправителя - 5: Сильная прямая секретность (эфемерный-эфемерный + эфемерный-статический DH (Диффи — Хеллман))

## Спецификации сообщений

### Обозначения ключей

- `RH_A` = Router Hash для Алисы (32 байта, SHA-256)
- `RH_B` = Router Hash для Боба (32 байта, SHA-256)
- `||` = Оператор конкатенации
- `byte(n)` = Один байт со значением n
- Все многобайтовые целые числа — **биг-эндиан** (если не указано иное)
- Ключи X25519 — **литтл-эндиан** (32 байта)

### Аутентифицированное шифрование (ChaCha20-Poly1305)

**Функция шифрования:**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Параметры:** - `key`: 32-байтный ключ шифрования из KDF (функции деривации ключа) - `nonce`: 12 байт (4 нулевых байта + 8-байтный счётчик, little-endian) - `associatedData`: 32-байтный хеш в фазе рукопожатия; нулевой длины в фазе передачи данных - `plaintext`: Данные для шифрования (0+ байт)

**Вывод:** - Шифротекст: той же длины, что и открытый текст - MAC: 16 байт (аутентификационный тег Poly1305)

**Управление Nonce (одноразовым числом):** - Счетчик начинается с 0 для каждого экземпляра шифра - Увеличивается при каждой операции AEAD в данном направлении - Отдельные счетчики для Alice→Bob и Bob→Alice на этапе передачи данных - Соединение должно быть завершено до того, как счетчик достигнет 2^64 - 1

## Сообщение 1: SessionRequest

Алиса инициирует соединение с Бобом.

**Операции Noise**: `e, es` (генерация и обмен эфемерными ключами)

### Необработанный формат

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Ограничения по размеру:** - Минимум: 80 байт (32 AES + 48 AEAD) - Максимум: 65535 байт всего - **Особый случай**: Максимум 287 байт при подключении к адресам "NTCP" (определение версии)

### Расшифрованное содержимое

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Блок опций (16 байт, big-endian (старший байт первым))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Критические поля:** - **Идентификатор сети** (начиная с 0.9.42): Быстрое отклонение соединений между разными сетями - **m3p2len**: Точный размер части 2 сообщения 3 (должен совпадать при отправке)

### Функция выработки ключа (KDF-1)

**Инициализация протокола:**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Операции MixHash:**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Операция MixKey (es pattern, шаблон рукопожатия ephemeral-static):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Примечания по реализации

1. **AES Obfuscation**: Используется только для устойчивости к DPI (глубокая инспекция пакетов); любой, у кого есть хеш router Боба и IV (инициализационный вектор), может расшифровать X
2. **Replay Prevention**: Боб должен кэшировать значения X (или их зашифрованные эквиваленты) не менее 2*D секунд (D = макс. рассинхронизация часов)
3. **Timestamp Validation**: Боб должен отклонять соединения с |tsA - current_time| > D (обычно D = 60 секунд)
4. **Curve Validation**: Боб должен проверить, что X — корректная точка X25519
5. **Fast Rejection**: Боб может проверить X[31] & 0x80 == 0 до расшифрования (у корректных ключей X25519 старший бит сброшен)
6. **Error Handling**: При любом сбое Боб закрывает соединение отправкой TCP RST после случайной задержки и чтения случайного числа байтов
7. **Buffering**: Алиса должна сбрасывать весь буфер сообщения (включая паддинг) сразу для эффективности

## Сообщение 2: SessionCreated

Боб отвечает Алисе.

**Операции Noise**: `e, ee` (эфемерно-эфемерный Диффи-Хеллман)

### Необработанный формат

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Расшифрованное содержимое

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Блок параметров (16 байт, big-endian (старший байт первым))

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Функция выработки ключей (KDF-2)

**Операции MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**Операция MixKey (шаблон ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Очистка памяти:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Примечания по реализации

1. **Цепной режим AES**: Шифрование Y использует состояние AES-CBC из сообщения 1 (не сбрасывается)
2. **Защита от повторов**: Алиса должна кэшировать значения Y как минимум в течение 2*D секунд
3. **Проверка метки времени**: Алиса должна отклонять, если |tsB - current_time| > D
4. **Проверка кривой**: Алиса должна проверить, что Y — корректная точка X25519
5. **Обработка ошибок**: Алиса закрывает соединение, посылая TCP RST, при любой ошибке
6. **Буферизация**: Боб должен сбрасывать всё сообщение целиком за один раз

## Сообщение 3: SessionConfirmed (подтверждение сеанса)

Алиса подтверждает сеанс и отправляет RouterInfo (данные о router в I2P).

**Операции Noise**: `s, se` (раскрытие статического ключа и статический-эфемерный DH)

### Структура из двух частей

Сообщение 3 состоит из **двух отдельных AEAD-фреймов**:

1. **Часть 1**: Фиксированный 48-байтовый кадр с зашифрованным статическим ключом Алисы
2. **Часть 2**: Кадр переменной длины с RouterInfo, параметрами и заполнением

### Необработанный формат

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Ограничения по размеру:** - Часть 1: Ровно 48 байт (32 байта открытого текста + 16 байт MAC) - Часть 2: Длина указана в сообщении 1 (поле m3p2len) - Общий максимум: 65535 байт (часть 1 максимум 48, значит часть 2 максимум 65487)

### Расшифрованное содержимое

**Часть 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Часть 2:**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Функция вывода ключей (KDF-3)

**Часть 1 (шаблон s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Часть 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Очистка памяти:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Примечания по реализации

1. **Проверка RouterInfo**: Боб должен проверить подпись, метку времени и согласованность ключей
2. **Сопоставление ключа**: Боб должен удостовериться, что статический ключ Алисы в части 1 совпадает с ключом в RouterInfo
3. **Расположение статического ключа**: Ищите совпадающий параметр "s" в NTCP или NTCP2 RouterAddress
4. **Порядок блоков**: RouterInfo должен идти первым, Options — вторым (если есть), Padding — последним (если есть)
5. **Планирование длины**: Алиса должна убедиться, что m3p2len в сообщении 1 в точности соответствует длине части 2
6. **Буферизация**: Алиса должна сбросить буфер, отправив обе части вместе одной отправкой TCP
7. **Необязательное связывание**: Алиса может сразу добавить кадр фазы данных для повышения эффективности

## Фаза данных

После завершения рукопожатия все сообщения используют кадры AEAD (аутентифицированное шифрование с дополнительными данными) переменной длины с обфусцированными полями длины.

### Функция выработки ключей (фаза данных)

**Функция Split (протокол Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Деривация ключа SipHash:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Структура кадра

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Ограничения фрейма:** - Минимум: 18 байт (2 байта обфусцированной длины + 0 байт открытого текста + 16 байт MAC) - Максимум: 65537 байт (2 байта обфусцированной длины + 65535 байт данных фрейма) - Рекомендуется: Несколько КБ на фрейм (минимизировать задержку на стороне получателя)

### Маскировка длины с помощью SipHash

**Назначение**: Предотвратить идентификацию средствами DPI (глубокая проверка пакетов) границ кадров

**Алгоритм:**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Декодирование:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Примечания:** - Отдельные цепочки IV (инициализационный вектор) для каждого направления (Alice→Bob и Bob→Alice) - Если SipHash возвращает uint64, используйте 2 младших байта в качестве маски - Преобразуйте uint64 в следующий IV в виде байтов в формате little-endian

### Формат блока

Каждый кадр содержит ноль или более блоков:

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Ограничения по размеру:** - Максимальный кадр: 65535 байт (включая MAC (код аутентификации сообщения)) - Максимальное пространство под блоки: 65519 байт (кадр - 16-байтовый MAC) - Максимальный размер одного блока: 65519 байт (3-байтовый заголовок + 65516 байт данных)

### Типы блоков

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Правила упорядочивания блоков:** - **Сообщение 3, часть 2**: RouterInfo, Параметры (необязательно), Заполнение (необязательно) - НИКАКИХ других типов - **Фаза данных**: Любой порядок, кроме:   - Заполнение ДОЛЖНО быть последним блоком, если присутствует   - Завершение ДОЛЖНО быть последним блоком (кроме Заполнения), если присутствует - Несколько блоков I2NP допускаются в одном кадре - Несколько блоков Заполнения НЕ допускаются в одном кадре

### Тип блока 0: DateTime

Синхронизация времени для обнаружения рассинхронизации часов.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Реализация**: Округляйте до ближайшей секунды, чтобы предотвратить накопление смещения часов.

### Тип блока 1: Параметры

Параметры паддинга и формирования трафика.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Коэффициенты паддинга** (число с фиксированной точкой 4.4, value/16.0): - `tmin`: Минимальный коэффициент паддинга при передаче (0.0 - 15.9375) - `tmax`: Максимальный коэффициент паддинга при передаче (0.0 - 15.9375) - `rmin`: Минимальный коэффициент паддинга при приёме (0.0 - 15.9375) - `rmax`: Максимальный коэффициент паддинга при приёме (0.0 - 15.9375)

**Примеры:** - 0x00 = 0% заполнения - 0x01 = 6.25% заполнения - 0x10 = 100% заполнения (соотношение 1:1) - 0x80 = 800% заполнения (соотношение 8:1)

**Фиктивный трафик:** - `tdmy`: Максимальная скорость, которую готовы отправлять (2 байта, среднее в байтах/с) - `rdmy`: Запрашиваемая скорость приёма (2 байта, среднее в байтах/с)

**Вставка задержки:** - `tdelay`: Максимальная задержка, которую готов вставить (2 байта, среднее значение в миллисекундах) - `rdelay`: Запрашиваемая задержка (2 байта, среднее значение в миллисекундах)

**Рекомендации:** - Минимальные значения указывают на желаемую устойчивость к анализу трафика - Максимальные значения указывают на ограничения пропускной способности - Отправитель должен соблюдать максимальные значения, указанные получателем - Отправитель может учитывать минимальные значения получателя в пределах ограничений - Механизм принуждения отсутствует; реализации могут различаться

### Тип блока 2: RouterInfo (структура с информацией о router)

Доставка RouterInfo для пополнения netdb и выполнения flooding (массовой рассылки).

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Использование:**

**В сообщении 3, часть 2** (рукопожатие): - Алиса отправляет свой RouterInfo (информация о router) Бобу - Flood bit (флаг распространения в netDb) обычно равен 0 (локальное хранение) - RouterInfo НЕ сжат gzip

**Во время Data Phase (этап передачи данных):** - Любая из сторон может отправить свой обновлённый RouterInfo - Бит Flood = 1: запросить распространение через floodfill (если получатель — floodfill) - Бит Flood = 0: только локальное хранение в netdb

**Требования к проверке:** 1. Проверьте, что тип подписи поддерживается 2. Проверьте подпись RouterInfo 3. Проверьте, что метка времени находится в допустимых пределах 4. Для рукопожатия: Проверьте, что статический ключ соответствует параметру "s" адреса NTCP2 5. Для фазы данных: Проверьте, что хэш router соответствует пиру сеанса 6. Распространяйте только RouterInfos с опубликованными адресами

**Примечания:** - Нет механизма ACK (используйте I2NP DatabaseStore с токеном ответа при необходимости) - Может содержать сторонние RouterInfos (при использовании floodfill) - НЕ сжато gzip (в отличие от I2NP DatabaseStore)

### Тип блока 3: сообщение I2NP

Сообщение I2NP с укороченным 9-байтным заголовком.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Отличия от NTCP1:** - Срок действия: 4 байта (секунды) против 8 байт (миллисекунды) - Длина: опущена (выводится из длины блока) - Контрольная сумма: опущена (AEAD (аутентифицированное шифрование с дополнительными данными) обеспечивает целостность) - Заголовок: 9 байт против 16 байт (сокращение на 44%)

**Фрагментация:** - Сообщения I2NP НЕ ДОЛЖНЫ фрагментироваться между блоками - Сообщения I2NP НЕ ДОЛЖНЫ фрагментироваться между кадрами - В одном кадре допускается несколько блоков I2NP

### Тип блока 4: Завершение

Явное закрытие соединения с указанием кода причины.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Коды причин:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Правила:** - Termination (блок завершения) ДОЛЖЕН быть последним блоком, не являющимся блоком заполнения, в кадре - Не более одного блока завершения на кадр - Отправителю следует закрыть соединение после отправки - Получателю следует закрыть соединение после получения

**Обработка ошибок:** - Ошибки рукопожатия: обычно закрывать с TCP RST (без блока завершения) - Ошибки AEAD на этапе передачи данных: случайный тайм-аут + случайное чтение, затем отправить блок завершения - См. раздел "AEAD Error Handling" для процедур безопасности

### Тип блока 254: Заполнение

Случайный паддинг (добавление случайных данных) для противодействия анализу трафика.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Правила:** - Паддинг ДОЛЖЕН быть последним блоком в фрейме, если он присутствует - Паддинг нулевой длины допускается - В каждом фрейме допускается только один блок паддинга - Допускаются фреймы, содержащие только паддинг - Следует придерживаться согласованных параметров из блока Options

**Паддинг в сообщениях 1-2:** - Вне фрейма AEAD (аутентифицированное шифрование с дополнительными данными) (в открытом виде) - Включён в хеш-цепочку следующего сообщения (аутентифицировано) - Подмена обнаруживается, когда проверка AEAD следующего сообщения завершается с ошибкой

**Заполнение в сообщении 3+ и в фазе передачи данных:** - Внутри фрейма AEAD (зашифровано и аутентифицировано) - Используется для формирования трафика и маскировки размера

## Обработка ошибок AEAD

**Критические требования безопасности:**

### Фаза рукопожатия (сообщения 1–3)

**Известный размер сообщения:** - Размеры сообщений заранее определены или явно указаны - Сбой аутентификации AEAD однозначно обнаруживается

**Ответ Боба на сбой сообщения 1:** 1. Установить случайный таймаут (диапазон зависит от реализации, рекомендуется 100–500 мс) 2. Прочитать случайное число байтов (диапазон зависит от реализации, рекомендуется 1–64 КБ) 3. Закрыть соединение с помощью TCP RST (без ответа) 4. Временно занести исходный IP-адрес в чёрный список 5. Отслеживать повторяющиеся сбои для долгосрочных блокировок

**Ответ Алисы на ошибку сообщения 2:** 1. Немедленно закрыть соединение с помощью TCP RST 2. Не отвечать Бобу

**Ответ Боба на сбой сообщения 3:** 1. Немедленно закрыть соединение отправкой TCP RST 2. Не отвечать Алисе

### Фаза данных

**Обфусцированный размер сообщения:** - Поле длины обфусцировано с помощью SipHash - Недопустимая длина или сбой AEAD может указывать на:   - Зондирование атакующим   - Повреждение данных в сети   - Рассинхронизированный IV (инициализирующий вектор) SipHash   - Злонамеренный пир

**Ответ на ошибку AEAD (аутентифицированное шифрование с дополнительными данными) или ошибку длины:** 1. Установить случайный таймаут (рекомендуется 100-500 мс) 2. Прочитать случайное количество байтов (рекомендуется 1KB-64KB) 3. Отправить блок завершения с кодом причины 4 (сбой AEAD) или 9 (ошибка фрейминга) 4. Закрыть соединение

**Предотвращение атаки типа «оракул расшифрования»:** - Никогда не раскрывать тип ошибки пиру до истечения случайного тайм-аута - Никогда не пропускать проверку длины перед проверкой AEAD - Рассматривать недопустимую длину так же, как ошибку AEAD - Использовать одинаковый путь обработки ошибок для обеих ошибок

**Соображения по реализации:** - Некоторые реализации могут продолжать работу после ошибок AEAD, если они редки - Прекращать работу после повторяющихся ошибок (рекомендуемый порог: 3-5 ошибок в час) - Баланс между восстановлением после ошибок и безопасностью

## Опубликованный RouterInfo (информация о маршрутизаторе)

### Формат адреса Router

Поддержка NTCP2 анонсируется через опубликованные записи RouterAddress (адрес маршрутизатора) с определёнными параметрами.

**Стиль транспорта:** - `"NTCP2"` - NTCP2 только на этом порту - `"NTCP"` - И NTCP, и NTCP2 на этом порту (автоопределение)   - **Примечание**: поддержка NTCP (v1) удалена в 0.9.50 (май 2021)   - стиль "NTCP" теперь устарел; используйте "NTCP2"

### Обязательные параметры

**Все опубликованные адреса NTCP2:**

1. **`host`** - IP-адрес (IPv4 или IPv6) или имя хоста
   - Формат: стандартная запись IP или доменное имя
   - Может быть опущен для routers только с исходящими соединениями или скрытых routers

2. **`port`** - номер TCP-порта
   - Формат: целое число, 1-65535
   - Можно опустить для router, работающих только на исходящую связь, или скрытых

3. **`s`** - Статический открытый ключ (X25519)
   - Формат: закодирован в Base64, 44 символа
   - Кодировка: алфавит Base64 I2P
   - Источник: 32-байтный открытый ключ X25519, little-endian (младший порядок байтов)

4. **`i`** - Вектор инициализации (IV) для AES
   - Формат: закодировано в Base64, 24 символа
   - Кодировка: алфавит Base64 I2P
   - Источник: 16-байтовый IV, big-endian (старший байт первым)

5. **`v`** - Версия протокола
   - Формат: целое число или целые числа, разделённые запятыми
   - Текущее: `"2"`
   - Будущее: `"2,3"` (должны быть в числовом порядке)

**Необязательные параметры:**

6. **`caps`** - Возможности (начиная с 0.9.50)
   - Формат: строка символов, обозначающих возможности
   - Значения:
     - `"4"` - возможность исходящих соединений по IPv4
     - `"6"` - возможность исходящих соединений по IPv6
     - `"46"` - и IPv4, и IPv6 (рекомендуемый порядок)
   - Не требуется, если `host` опубликован
   - Полезно для скрытых/за межсетевым экраном routers

7. **`cost`** - Приоритет адреса
   - Формат: целое число, 0-255
   - Меньшие значения = более высокий приоритет
   - Рекомендуется: 5-10 для обычных адресов
   - Рекомендуется: 14 для неопубликованных адресов

### Примеры записей RouterAddress (адрес маршрутизатора)

**Опубликованный IPv4-адрес:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Скрытый Router (только исходящий):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router с двойным стеком:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Важные правила:** - Несколько адресов NTCP2 с **одним и тем же портом** ДОЛЖНЫ использовать **идентичные** значения `s`, `i` и `v` - Разные порты могут использовать разные ключи - Двухстековые routers должны публиковать отдельные адреса IPv4 и IPv6

### Неопубликованный адрес NTCP2

**Для routers в режиме Outbound-Only:**

Если router не принимает входящие соединения NTCP2, но инициирует исходящие соединения, он ДОЛЖЕН всё равно публиковать RouterAddress со следующими параметрами:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Назначение:** - Позволяет Бобу проверить статический ключ Алисы во время рукопожатия - Требуется для проверки RouterInfo (информация о router) в сообщении 3, часть 2 - Не требуются `i`, `host` или `port` (только исходящее)

**Альтернатива:** - Добавьте `s` и `v` к уже опубликованному адресу "NTCP" или SSU

### Ротация открытого ключа и вектора инициализации (IV)

**Критическая политика безопасности:**

**Общие правила:** 1. **Никогда не выполняйте ротацию, пока router работает** 2. **Сохраняйте ключ и IV (инициализационный вектор)** между перезапусками 3. **Отслеживайте предыдущий простой**, чтобы определить допустимость ротации

**Минимальное время простоя перед ротацией:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Дополнительные триггеры:** - Изменение локального IP-адреса: может вызывать ротацию независимо от простоя - Router "rekey" (смена ключей; новый Router Hash): генерация новых ключей

**Обоснование:** - Предотвращает раскрытие времени перезапуска через смену ключей - Позволяет кэшированным RouterInfos естественным образом устаревать - Поддерживает стабильность сети - Снижает количество неудачных попыток подключения

**Реализация:** 1. Сохранять ключ, IV (вектор инициализации) и метку времени последнего завершения работы в постоянном хранилище 2. При запуске вычислить downtime = current_time - last_shutdown 3. Если downtime > минимума для типа router, можно выполнить ротацию 4. Если IP изменился или происходит смена ключей, можно выполнить ротацию 5. В противном случае повторно использовать предыдущие ключ и IV

**Ротация IV (вектор инициализации):** - Подчиняется тем же правилам, что и ротация ключа - Присутствует только в опубликованных адресах (не в скрытых routers) - Рекомендуется менять IV при каждом изменении ключа

## Определение версии

**Контекст:** Когда `transportStyle="NTCP"` (устаревший), Bob поддерживает как NTCP v1, так и v2 на одном порту и должен автоматически определять версию протокола.

**Алгоритм обнаружения:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Быстрая проверка старшего бита (MSB):** - Перед расшифрованием AES проверьте: `encrypted_X[31] & 0x80 == 0` - У валидных ключей X25519 старший бит сброшен - Сбой, вероятно, указывает на NTCP1 (старый транспортный протокол I2P) (или атаку) - При сбое реализуйте устойчивость к зондированию (случайный таймаут + чтение)

**Требования к реализации:**

1. **Обязанности Алисы:**
   - При подключении к адресу "NTCP" ограничьте размер сообщения 1 не более 287 байтов
   - Буферизуйте и сбросьте всё сообщение 1 целиком за один раз
   - Повышает вероятность доставки одним TCP-пакетом

2. **Ответственность Боба:**
   - Буферизовать полученные данные до определения версии
   - Реализовать корректную обработку таймаутов
   - Использовать TCP_NODELAY для быстрого определения версии
   - Буферизовать и затем целиком сбросить сообщение 2 сразу после определения версии

**Соображения безопасности:** - Атаки сегментацией: Боб должен быть устойчив к сегментации TCP - Зондирующие атаки: реализуйте случайные задержки и по-байтовое чтение при сбоях - Предотвращение DoS: ограничьте число одновременных ожидающих установления соединений - Тайм-ауты чтения: как на каждое чтение, так и общий (защита от «slowloris» — атака, при которой клиент удерживает соединение открытым, передавая данные крайне медленно)

## Рекомендации по смещению часов

**Поля временных меток:** - Сообщение 1: `tsA` (метка времени Алисы) - Сообщение 2: `tsB` (метка времени Боба) - Сообщение 3+: необязательные блоки DateTime

**Максимальное расхождение (D):** - Обычно: **±60 секунд** - Настраивается в каждой реализации - Расхождение > D, как правило, фатально

### Обработка на стороне Боба (Сообщение 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Обоснование:** Отправка сообщения 2 даже при расхождении часов позволяет Алисе диагностировать проблемы с системным временем.

### Обработка на стороне Алисы (сообщение 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Корректировка RTT:** - Вычтите половину RTT из рассчитанного смещения - Учитывает задержку распространения в сети - Более точная оценка смещения

### Обработка Бобом (Сообщение 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Синхронизация времени

**Блоки DateTime (фаза данных):** - Периодически отправляйте блок DateTime (тип 0) - Получатель может использовать для корректировки часов - Округляйте метку времени до ближайшей секунды (чтобы предотвратить смещение)

**Внешние источники времени:** - NTP (Network Time Protocol) - Синхронизация системных часов - Время консенсуса сети I2P

**Стратегии корректировки часов:** - Если локальные часы неверны: скорректируйте системное время или используйте смещение - Если часы пиров стабильно неверны: зафиксируйте проблему на стороне пира - Отслеживайте статистику рассинхронизации для мониторинга состояния сети

## Свойства безопасности

### Прямая секретность

**Достигается посредством:** - Эфемерного обмена ключами Диффи-Хеллмана (X25519) - Трех операций DH: es, ee, se (шаблон Noise XK) - Уничтожения эфемерных ключей после завершения рукопожатия

**Прогрессия конфиденциальности:** - Сообщение 1: Уровень 2 (прямая секретность при компрометации отправителя) - Сообщение 2: Уровень 1 (эфемерный получатель) - Сообщение 3+: Уровень 5 (сильная прямая секретность)

**Совершенная прямая секретность:** - Компрометация долгосрочных статических ключей НЕ раскрывает сессионные ключи прошлых сессий - Каждая сессия использует уникальные эфемерные ключи - Эфемерные закрытые ключи никогда не используются повторно - Очистка памяти после согласования ключей

**Ограничения:** - Сообщение 1 уязвимо, если статический ключ Боба скомпрометирован (но сохраняется прямая секретность в случае компрометации Алисы) - Возможны атаки воспроизведения для сообщения 1 (смягчаются меткой времени и кэшем повторов)

### Аутентификация

**Взаимная аутентификация:** - Алиса аутентифицируется статическим ключом в сообщении 3 - Боб аутентифицируется владением статическим закрытым ключом (неявно из успешного рукопожатия)

**Устойчивость к Key Compromise Impersonation (KCI; имитация при компрометации ключа):** - Уровень аутентификации 2 (устойчив к KCI) - Злоумышленник не может выдать себя за Alice, даже имея статический закрытый ключ Alice (без её эфемерного ключа) - Злоумышленник не может выдать себя за Bob, даже имея статический закрытый ключ Bob (без его эфемерного ключа)

**Проверка статического ключа:** - Алиса заранее знает статический ключ Боба (из RouterInfo) - Боб проверяет, что статический ключ Алисы соответствует RouterInfo в сообщении 3 - Предотвращает атаки типа «человек посередине»

### Устойчивость к анализу трафика

**Контрмеры против DPI:** 1. **Сокрытие с помощью AES:** Эфемерные ключи зашифрованы, данные выглядят случайными 2. **Сокрытие длины с SipHash:** Длины фреймов не в открытом виде 3. **Случайное заполнение (padding):** Переменные размеры сообщений, нет фиксированных шаблонов 4. **Зашифрованные фреймы:** Вся полезная нагрузка зашифрована алгоритмом ChaCha20

**Предотвращение атак повторов:** - Проверка метки времени (±60 секунд) - Кэш повторов для эфемерных ключей (время жизни 2*D) - Инкрементирование Nonce (одноразовое число) предотвращает повтор пакетов в рамках сеанса

**Устойчивость к зондированию:** - Случайные тайм-ауты при ошибках AEAD - Случайное чтение байтов перед закрытием соединения - Отсутствие ответов при ошибках рукопожатия - Занесение IP-адресов в черный список при повторных сбоях

**Рекомендации по паддингу:** - Сообщения 1-2: паддинг в открытом виде (аутентифицированный) - Сообщение 3+: зашифрованный паддинг внутри фреймов AEAD (шифрование с аутентификацией и ассоциированными данными) - Согласованные параметры паддинга (Options block — блок параметров) - Разрешены фреймы только с паддингом

### Противодействие атакам отказа в обслуживании

**Ограничения соединений:** - Максимальное количество активных соединений (зависит от реализации) - Максимальное количество незавершённых рукопожатий (например, 100-1000) - Ограничения на число соединений с одного IP-адреса (например, 3-10 одновременно)

**Защита ресурсов:** - операции DH (обмен ключами Диффи — Хеллмана) ограничены по частоте (ресурсоёмные) - таймауты чтения для каждого сокета и общий - защита от "Slowloris" (общие лимиты времени) - занесение IP в чёрный список за злоупотребления

**Быстрое отклонение:** - Несоответствие идентификатора сети → немедленное закрытие - Некорректная точка X25519 → быстрая проверка старшего бита до расшифрования - Метка времени вне допустимого диапазона → закрытие без вычислений - Сбой AEAD (аутентифицированное шифрование с дополнительными данными) → без ответа, случайная задержка

**Устойчивость к зондированию:** - Случайный таймаут: 100-500 мс (зависит от реализации) - Случайный объём чтения: 1KB-64KB (зависит от реализации) - Нет информации об ошибках для атакующего - Закрытие соединения TCP RST (без рукопожатия FIN)

### Криптографическая безопасность

**Алгоритмы:** - **X25519**: 128-битная стойкость, DH на эллиптических кривых (Curve25519) - **ChaCha20**: потоковый шифр с ключом 256 бит - **Poly1305**: информационно-теоретически стойкий MAC - **SHA-256**: 128-битная стойкость к коллизиям, 256-битная стойкость к нахождению прообраза - **HMAC-SHA256**: PRF (псевдослучайная функция) для деривации ключей

**Размеры ключей:** - Статические ключи: 32 байта (256 бит) - Эфемерные ключи: 32 байта (256 бит) - Ключи шифрования: 32 байта (256 бит) - MAC (код аутентификации сообщения): 16 байт (128 бит)

**Известные проблемы:** - В ChaCha20 повторное использование nonce (одноразового номера) катастрофично (предотвращается увеличением счётчика) - У X25519 есть проблемы малых подгрупп (смягчаются проверкой кривой) - SHA-256 теоретически уязвим к атаке расширения длины (не эксплуатируется в HMAC)

**Неизвестно о каких-либо уязвимостях (по состоянию на октябрь 2025 года):** - Noise Protocol Framework (фреймворк протоколов Noise) широко исследован - ChaCha20-Poly1305 используется в TLS 1.3 - X25519 является стандартом в современных протоколах - Нет практических атак на конструкцию

## Ссылки

### Основные спецификации

- **[Спецификация NTCP2](/docs/specs/ntcp2/)** - Официальная спецификация I2P
- **[Предложение 111](/proposals/111-ntcp-2/)** - Исходный документ проектирования с обоснованием
- **[Noise Protocol Framework (фреймворк протокола Noise)](https://noiseprotocol.org/noise.html)** - Редакция 33 (2017-10-04)

### Криптографические стандарты

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Эллиптические кривые для обеспечения безопасности (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 и Poly1305 для протоколов IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (объявляет устаревшим RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC: хеширование с ключом для аутентификации сообщений
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 для приложений хеш-функций

### Связанные спецификации I2P

- **[Спецификация I2NP](/docs/specs/i2np/)** - формат сообщений протокола сети I2P
- **[Общие структуры](/docs/specs/common-structures/)** - форматы RouterInfo, RouterAddress
- **[Транспорт SSU](/docs/legacy/ssu/)** - транспорт UDP (исходный, теперь SSU2)
- **[Предложение 147](/proposals/147-transport-network-id-check/)** - проверка идентификатора транспортной сети (0.9.42)

### Ссылки по реализации

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Эталонная реализация (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Реализация на C++
- **[Примечания к выпуску I2P](/blog/)** - История версий и обновления

### Исторический контекст

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Послужил источником вдохновения для фреймворка Noise
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Подключаемый транспорт (пример обфускации длины на базе SipHash)

## Рекомендации по реализации

### Обязательные требования

**Для соответствия требованиям:**

1. **Реализовать полное рукопожатие:**
   - Поддержать все три сообщения с корректными цепочками KDF (функция выработки ключей)
   - Проверять все теги AEAD (аутентифицированное шифрование с дополнительными данными)
   - Проверять, что точки на кривой X25519 (эллиптическая кривая X25519) корректны

2. **Реализовать фазу данных:**
   - Обфускация длины с помощью SipHash (в обоих направлениях)
   - Все типы блоков: 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Корректное управление nonce (одноразовое значение) (отдельные счётчики)

3. **Функции безопасности:**
   - Защита от повторов (кэширование эфемерных ключей в течение 2*D)
   - Проверка меток времени (по умолчанию ±60 секунд)
   - Случайное заполнение в сообщениях 1-2
   - Обработка ошибок AEAD со случайными таймаутами

4. **Публикация RouterInfo:**
   - Публиковать статический ключ ("s"), вектор инициализации (IV) ("i") и версию ("v")
   - Выполнять ротацию ключей согласно политике
   - Поддерживать поле возможностей ("caps") для скрытых routers

5. **Совместимость с сетью:**
   - Поддерживать поле идентификатора сети (в настоящее время — 2 для mainnet (основная сеть))
   - Обеспечивать совместимость с существующими реализациями на Java и i2pd
   - Поддерживать как IPv4, так и IPv6

### Рекомендуемые практики

**Оптимизация производительности:**

1. **Стратегия буферизации:**
   - Сбрасывать сообщения полностью сразу (сообщения 1, 2, 3)
   - Использовать TCP_NODELAY для сообщений рукопожатия
   - Буферизовать несколько блоков данных в один кадр
   - Ограничить размер кадра до нескольких КБ (минимизировать задержку у получателя)

2. **Управление соединениями:**
   - Переиспользуйте соединения, когда возможно
   - Реализуйте пул соединений
   - Отслеживайте состояние соединений (DateTime blocks — временные блокировки)

3. **Управление памятью:**
   - Обнуляйте конфиденциальные данные после использования (эфемерные ключи, результаты DH (Диффи-Хеллман))
   - Ограничивайте число параллельных рукопожатий (предотвращение DoS-атак)
   - Используйте пулы памяти для частых выделений

**Укрепление безопасности:**

1. **Устойчивость к зондированию:**
   - Случайные тайм-ауты: 100-500 мс
   - Случайные чтения байтов: 1 КБ-64 КБ
   - Занесение IP-адресов в черный список при повторных сбоях
   - Без подробностей об ошибках для пиров

2. **Ограничения ресурсов:**
   - Максимальное число соединений на IP-адрес: 3-10
   - Максимальное число ожидающих рукопожатий: 100-1000
   - Таймауты чтения: 30-60 секунд на операцию
   - Общий таймаут соединения: 5 минут на рукопожатие

3. **Управление ключами:**
   - Постоянное хранение статического ключа и вектора инициализации (IV)
   - Безопасная генерация случайных чисел (криптографически стойкий генератор случайных чисел)
   - Строгое соблюдение политик ротации
   - Никогда не переиспользовать эфемерные ключи

**Мониторинг и диагностика:**

1. **Метрики:**
   - Доли успешных/неудачных рукопожатий
   - Частота ошибок AEAD
   - Распределение смещения часов
   - Статистика длительности соединений

2. **Логирование:**
   - Логировать ошибки рукопожатия с кодами причин
   - Логировать события смещения часов
   - Логировать заблокированные IP-адреса
   - Никогда не логировать конфиденциальный ключевой материал

3. **Тестирование:**
   - Модульные тесты для цепочек KDF (функций выработки ключа)
   - Интеграционные тесты с другими реализациями
   - Фаззинг обработки пакетов
   - Нагрузочное тестирование на устойчивость к DoS-атакам

### Распространённые ошибки

**Критические ошибки, которых следует избегать:**

1. **Повторное использование Nonce (одноразового числа):**
   - Никогда не сбрасывайте счетчик nonce в середине сеанса
   - Используйте отдельные счетчики для каждого направления
   - Завершайте сеанс до достижения 2^64 - 1

2. **Ротация ключей:**
   - Никогда не выполняйте ротацию ключей, пока router работает
   - Никогда не переиспользуйте эфемерные ключи между сеансами
   - Соблюдайте правила минимального времени простоя

3. **Обработка временных меток:**
   - Никогда не принимать истекшие временные метки
   - Всегда вносить поправку на RTT (время кругового прохода) при расчете смещения
   - Округлять метки времени DateTime до секунд

4. **Ошибки AEAD:**
   - Никогда не раскрывайте тип ошибки атакующему
   - Всегда используйте случайный таймаут перед закрытием
   - Обрабатывайте недопустимую длину так же, как ошибку AEAD

5. **Заполнение:**
   - Никогда не отправляйте заполнение вне согласованных границ
   - Всегда размещайте блок заполнения последним
   - Никогда не используйте несколько блоков заполнения в одном кадре

6. **RouterInfo (метаданные router):**
   - Всегда проверяйте, что статический ключ соответствует данным в RouterInfo
   - Никогда не рассылайте RouterInfo без опубликованных адресов
   - Всегда проверяйте подписи

### Методология тестирования

**Модульные тесты:**

1. **Криптографические примитивы:**
   - Тестовые векторы для X25519, ChaCha20, Poly1305, SHA-256
   - Тестовые векторы для HMAC-SHA256
   - Тестовые векторы для SipHash-2-4

2. **Цепочки KDF:**
   - Тесты с эталонными ответами для всех трёх сообщений
   - Проверить передачу ключа цепочки
   - Тест генерации вектора инициализации (IV) для SipHash

3. **Разбор сообщений:**
   - Декодирование корректных сообщений
   - Отклонение некорректных сообщений
   - Граничные условия (пустое сообщение, максимальный размер)

**Интеграционные тесты:**

1. **Рукопожатие:**
   - Успешный обмен из трёх сообщений
   - Отклонение при смещении часов
   - Обнаружение атаки повторного воспроизведения
   - Отклонение некорректного ключа

2. **Фаза данных:**
   - Передача сообщений I2NP
   - Обмен RouterInfo (информация о router)
   - Обработка заполнения
   - Сообщения завершения

3. **Совместимость:**
   - Тестирование с Java I2P
   - Тестирование с i2pd
   - Тестирование IPv4 и IPv6
   - Тестирование опубликованных и скрытых routers

**Тесты безопасности:**

1. **Негативные тесты:**
   - Недопустимые теги AEAD (аутентифицированное шифрование с дополнительными данными)
   - Повторно переданные сообщения
   - Атаки на основе смещения часов
   - Некорректно сформированные кадры

2. **Тесты DoS:**
   - Флуд соединениями
   - Атаки Slowloris
   - Истощение CPU (чрезмерные DH-вычисления)
   - Истощение памяти

3. **Фаззинг:**
   - Случайные сообщения рукопожатия
   - Случайные кадры фазы данных
   - Случайные типы и размеры блоков
   - Недопустимые криптографические значения

### Переход с NTCP

**Для поддержки устаревшего NTCP (теперь удалено):**

NTCP (version 1) был удалён в I2P 0.9.50 (май 2021 года). Все текущие реализации должны поддерживать NTCP2. Исторические примечания:

1. **Переходный период (2018–2021):**
   - 0.9.36: NTCP2 представлен (по умолчанию отключён)
   - 0.9.37: NTCP2 включён по умолчанию
   - 0.9.40: NTCP объявлён устаревшим
   - 0.9.50: NTCP удалён

2. **Определение версии:**
   - Поле transportStyle (тип транспорта) со значением "NTCP" указывало на поддержку обеих версий
   - Поле transportStyle со значением "NTCP2" указывало на поддержку только NTCP2
   - Автоматическое определение по размеру сообщения (287 против 288 байт)

3. **Текущее состояние:**
   - Все router должны поддерживать NTCP2
   - "NTCP" transportStyle устарел
   - Используйте исключительно "NTCP2" transportStyle

## Приложение A: шаблон Noise XK

**Стандартный шаблон Noise XK:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Интерпретация:**

- `<-` : Сообщение от респондента (Боба) к инициатору (Алисе)
- `->` : Сообщение от инициатора (Алисы) к респонденту (Бобу)
- `s` : Статический ключ (долгосрочный ключ идентичности)
- `rs` : Удалённый статический ключ (статический ключ пира, известный заранее)
- `e` : Эфемерный ключ (специфичный для сеанса, создаётся по требованию)
- `es` : Эфемерный-Статический DH (Диффи — Хеллман) (эфемерный Алисы × статический Боба)
- `ee` : Эфемерный-Эфемерный DH (эфемерный Алисы × эфемерный Боба)
- `se` : Статический-Эфемерный DH (статический Алисы × эфемерный Боба)

**Последовательность согласования ключа:**

1. **Предсообщение:** Алиса знает статический открытый ключ Боба (из RouterInfo)
2. **Сообщение 1:** Алиса отправляет эфемерный ключ, выполняет es DH
3. **Сообщение 2:** Боб отправляет эфемерный ключ, выполняет ee DH
4. **Сообщение 3:** Алиса раскрывает статический ключ, выполняет se DH

**Свойства безопасности:**

- Алиса аутентифицирована: Да (на основании сообщения 3)
- Боб аутентифицирован: Да (по наличию статического закрытого ключа)
- Прямая секретность: Да (эфемерные ключи уничтожаются)
- KCI resistance (устойчивость к имперсонации при компрометации ключа): Да (уровень аутентификации 2)

## Приложение B: кодирование Base64

**Алфавит Base64 в I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Отличия от стандартного Base64:** - Символы 62–63: `-~` вместо `+/` - Дополнение: то же самое (`=`) или опускается в зависимости от контекста

**Использование в NTCP2:** - Статический ключ ("s"): 32 байта → 44 символа (без дополнения) - IV ("i"): 16 байт → 24 символа (без дополнения)

**Пример кодирования:**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Приложение C: Анализ захвата пакетов

**Идентификация трафика NTCP2:**

1. **Рукопожатие TCP:**
   - Стандартные TCP SYN, SYN-ACK, ACK
   - Порт назначения обычно 8887 или аналогичный

2. **Сообщение 1 (SessionRequest — запрос сеанса):**
   - Первые прикладные данные от Алисы
   - 80-65535 байт (обычно несколько сотен)
   - Выглядит как случайные данные (эфемерный ключ, зашифрованный AES)
   - 287 байт максимум при подключении к адресу "NTCP"

3. **Сообщение 2 (SessionCreated — «создание сессии»):**
   - Ответ от Боба
   - 80-65535 байт (обычно несколько сотен)
   - Также похоже на случайные данные

4. **Сообщение 3 (SessionConfirmed):**
   - От Alice
   - 48 байт + переменная часть (размер RouterInfo (информация о router) + заполнение)
   - Обычно 1-4 КБ

5. **Фаза данных:**
   - Кадры переменной длины
   - Поле длины замаскировано (выглядит случайным)
   - Зашифрованная полезная нагрузка
   - Padding (выравнивание данными) делает размер непредсказуемым

**Обход DPI:** - Отсутствуют незашифрованные заголовки - Отсутствуют фиксированные шаблоны - Поля длины замаскированы - Случайный паддинг нарушает работу эвристик, основанных на размере

**Сравнение с NTCP:** - Сообщение 1 в NTCP всегда 288 байт (идентифицируемо) - Размер сообщения 1 в NTCP2 варьируется (не идентифицируемо) - В NTCP были распознаваемые шаблоны - NTCP2 спроектирован для противодействия глубокой инспекции пакетов (DPI)

## Приложение D: История версий

**Ключевые вехи:**

- **0.9.36** (23 августа 2018 г.): Введён NTCP2, по умолчанию отключён
- **0.9.37** (4 октября 2018 г.): NTCP2 включён по умолчанию
- **0.9.40** (20 мая 2019 г.): NTCP объявлен устаревшим
- **0.9.42** (27 августа 2019 г.): Добавлено поле Network ID (идентификатор сети; Proposal 147)
- **0.9.50** (17 мая 2021 г.): NTCP удалён, добавлена поддержка capabilities (флагов возможностей)
- **2.10.0** (9 сентября 2025 г.): Последний стабильный релиз

**Стабильность протокола:** - Нет изменений, нарушающих совместимость, с 0.9.50 - Продолжаются улучшения устойчивости к зондированию - Фокус на производительности и надежности - Постквантовая криптография в разработке (не включена по умолчанию)

**Текущий статус транспортов:** - NTCP2: Обязательный транспорт TCP - SSU2: Обязательный транспорт UDP - NTCP (v1): Удалён - SSU (v1): Удалён
