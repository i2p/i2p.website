---
title: "Зашифрованный LeaseSet"
description: "Формат LeaseSet с контролем доступа для приватных назначений"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

В этом документе описываются ослепление, шифрование и расшифрование зашифрованного LeaseSet2 (LS2). Зашифрованные LeaseSets обеспечивают публикацию с контролем доступа информации о скрытом сервисе в сетевой базе данных I2P.

**Ключевые возможности:** - Ежедневная ротация ключей для обеспечения прямой секретности - Двухуровневая авторизация клиентов (на основе DH и на основе PSK) - Шифрование ChaCha20 для повышения производительности на устройствах без аппаратной поддержки AES - Подписи Red25519 с ослеплением ключей - Сохранение конфиденциальности состава клиентов

**Связанная документация:** - [Спецификация общих структур](/docs/specs/common-structures/) - Структура зашифрованного LeaseSet (набор данных для установления соединения с назначением) - [Предложение 123: новые записи netDB (распределённая сетевая база данных I2P)](/proposals/123-new-netdb-entries/) - Общие сведения о зашифрованных LeaseSets - [Документация по сетевой базе данных](/docs/specs/common-structures/) - Использование NetDB

---

## История версий и статус реализации

### Хронология разработки протокола

**Важное примечание о нумерации версий:**   I2P использует две отдельные схемы нумерации версий: - **Версия API/Router:** серия 0.9.x (используется в технических спецификациях) - **Версия продуктового релиза:** серия 2.x.x (используется для публичных релизов)

Технические спецификации ссылаются на версии API (например, 0.9.41), тогда как конечные пользователи видят версии продукта (например, 2.10.0).

### Вехи реализации

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### Текущее состояние

- ✅ **Состояние протокола:** стабильное и неизменное с июня 2019 года
- ✅ **Java I2P:** полностью реализован начиная с версии 0.9.40+
- ✅ **i2pd (C++):** полностью реализован начиная с версии 2.58.0+
- ✅ **Совместимость:** полная между реализациями
- ✅ **Развёртывание в сети:** готово к промышленной эксплуатации, с 6+ годами опыта эксплуатации

---

## Криптографические определения

### Обозначения и соглашения

- `||` обозначает конкатенацию
- `mod L` обозначает взятие по модулю порядка Ed25519
- Все массивы байтов представлены в сетевом порядке байтов (big-endian, старший байт первым), если не указано иное
- Значения в формате little-endian (младший байт первым) указываются явно

### Генератор криптографически стойких случайных чисел (n)

**Криптографически стойкий генератор случайных чисел**

Генерирует `n` байт криптографически стойких случайных данных, подходящих для генерации ключевого материала.

**Требования к безопасности:** - Должен быть криптографически стойким (подходящим для генерации ключей) - Должен оставаться безопасным при раскрытии в сети соседних последовательностей байтов - Реализациям следует хешировать выходные данные, полученные из потенциально ненадёжных источников

**Ссылки:** - [Соображения безопасности PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [Обсуждение в Tor Dev](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Хэш SHA-256 с персонализацией**

Хеш-функция с разделением доменов принимает: - `p`: строка персонализации (обеспечивает разделение доменов) - `d`: данные для хеширования

**Реализация:**

```
H(p, d) := SHA-256(p || d)
```
**Использование:** Обеспечивает криптографическое разделение доменов для предотвращения коллизионных атак между различными протокольными вариантами использования SHA-256.

### Потоковый шифр: ChaCha20

**Потоковый шифр: ChaCha20, как определено в разделе 2.4 RFC 7539**

**Параметры:** - `S_KEY_LEN = 32` (256-битный ключ) - `S_IV_LEN = 12` (96-битный nonce (одноразовое число)) - Начальный счетчик: `1` (RFC 7539 допускает 0 или 1; 1 рекомендуется для контекстов AEAD)

**ENCRYPT(k, iv, plaintext)**

Шифрует открытый текст, используя: - `k`: 32-байтовый ключ шифрования - `iv`: 12-байтовый nonce (одноразовое значение; ДОЛЖЕН быть уникальным для каждого ключа) - Возвращает шифртекст того же размера, что и открытый текст

**Свойство безопасности:** Весь шифртекст должен быть неотличим от случайных данных, если ключ секретен.

**РАСШИФРОВАТЬ(k, iv, ciphertext)**

Расшифровывает шифротекст, используя: - `k`: 32-байтный ключ шифрования - `iv`: 12-байтный nonce (одноразовое значение) - Возвращает открытый текст

**Обоснование выбора:** ChaCha20 выбран вместо AES, потому что: - в 2,5–3 раза быстрее, чем AES, на устройствах без аппаратного ускорения - реализацию с постоянным временем выполнения проще обеспечить - при наличии AES-NI безопасность и скорость сопоставимы

**Ссылки:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 и Poly1305 для протоколов IETF

### Подпись: Red25519 (схема цифровой подписи на основе Ed25519)

**Схема подписи: Red25519 (SigType 11) с Key Blinding (ослепление ключа)**

Red25519 основан на подписях Ed25519 над эллиптической кривой Ed25519, с использованием SHA-512 для хеширования и поддержкой ослепления ключа, как это определено в ZCash RedDSA (схема электронной подписи).

**Функции:**

#### DERIVE_PUBLIC(privkey)

Возвращает публичный ключ, соответствующий заданному закрытому ключу. - Использует стандартное скалярное умножение базовой точки Ed25519

#### SIGN(privkey, m)

Возвращает подпись, созданную закрытым ключом `privkey` для сообщения `m`.

**Различия в алгоритме подписи Red25519 по сравнению с Ed25519:** 1. **Random Nonce:** (одноразовое число) Использует 80 байт дополнительных случайных данных

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Это делает каждую подпись Red25519 уникальной, даже для одного и того же сообщения и ключа.

2. **Генерация закрытого ключа:** закрытые ключи Red25519 генерируются из случайных чисел и редуцируются `mod L`, вместо использования подхода Ed25519 с bit-clamping (фиксация отдельных битов).

#### VERIFY(pubkey, m, sig)

Проверяет подпись `sig` по открытому ключу `pubkey` и сообщению `m`. - Возвращает `true`, если подпись действительна, `false` в противном случае - Проверка идентична Ed25519

**Операции ослепления ключей:**

#### GENERATE_ALPHA(data, secret)

Генерирует параметр alpha для ослепления ключа. - `data`: Обычно содержит открытый ключ подписи и типы подписей - `secret`: Необязательный дополнительный секрет (нулевой длины, если не используется) - Результат имеет то же распределение, что и закрытые ключи Ed25519 (после редукции по модулю L)

#### BLIND_PRIVKEY(privkey, alpha)

Ослепляет закрытый ключ с использованием секрета `alpha`. - Реализация: `blinded_privkey = (privkey + alpha) mod L` - Использует скалярную арифметику в поле

#### BLIND_PUBKEY(pubkey, alpha)

Ослепляет открытый ключ с использованием секрета `alpha`. - Реализация: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Использует сложение элементов группы (точек) на кривой

**Критическое свойство:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Соображения безопасности:**

Из спецификации протокола ZCash, раздел 5.4.6.1: В целях безопасности alpha должна быть распределена так же, как закрытые ключи без ослепления. Это гарантирует, что "сочетание повторно рандомизированного открытого ключа и подписи(ей), выполненной(ых) этим ключом, не раскрывает ключ, из которого был получен повторно рандомизированный ключ."

**Поддерживаемые типы подписей:** - **Тип 7 (Ed25519):** Поддерживается для существующих назначений (обратная совместимость) - **Тип 11 (Red25519):** Рекомендуется для новых назначений с использованием шифрования - **Ослеплённые ключи:** Всегда используйте тип 11 (Red25519)

**Ссылки:** - [Спецификация протокола ZCash](https://zips.z.cash/protocol/protocol.pdf) - Раздел 5.4.6 RedDSA (схема цифровой подписи) - [Спецификация I2P Red25519](/docs/specs/red25519-signature-scheme/)

### Диффи‑Хеллман: X25519

**Диффи — Хеллман на эллиптических кривых: X25519**

Система согласования ключей на основе Curve25519.

**Параметры:** - Закрытые ключи: 32 байта - Открытые ключи: 32 байта - Значение общего секрета: 32 байта

**Функции:**

#### GENERATE_PRIVATE()

Генерирует новый 32-байтный закрытый ключ с использованием CSRNG (криптографически стойкого генератора случайных чисел).

#### DERIVE_PUBLIC(privkey)

Порождает 32-байтный открытый ключ из заданного закрытого ключа. - Использует скалярное умножение на Curve25519

#### DH(privkey, pubkey)

Выполняет согласование ключа по протоколу Диффи-Хеллмана. - `privkey`: Локальный 32-байтный закрытый ключ - `pubkey`: Удалённый 32-байтный открытый ключ - Возвращает: 32-байтный общий секрет

**Свойства безопасности:** - Предположение о вычислительной трудности задачи Диффи — Хеллмана на Curve25519 - Прямая секретность при использовании эфемерных ключей - Требуется константновременная реализация для предотвращения тайминговых атак

**Ссылки:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Эллиптические кривые для безопасности

### HKDF (функция выработки ключей на основе HMAC)

**Функция деривации ключей на основе HMAC**

Извлекает и расширяет ключевой материал из входного ключевого материала.

**Параметры:** - `salt`: максимум 32 байта (обычно 32 байта для SHA-256) - `ikm`: входной ключевой материал (любой длины, должен иметь хорошую энтропию) - `info`: контекстно-зависимая информация (разделение доменов) - `n`: длина выходных данных в байтах

**Реализация:**

Использует HKDF, как определено в RFC 5869, со следующими параметрами: - **Хеш-функция:** SHA-256 - **HMAC:** как указано в RFC 2104 - **Длина соли:** не более 32 байт (HashLen для SHA-256)

**Сценарий использования:**

```
keys = HKDF(salt, ikm, info, n)
```
**Разделение доменов:** Параметр `info` обеспечивает криптографическое разделение доменов между различными использованиями HKDF (функция выработки ключей на основе HMAC) в протоколе.

**Значения Verified Info:** - `"ELS2_L1K"` - шифрование уровня 1 (внешнее) - `"ELS2_L2K"` - шифрование уровня 2 (внутреннее) - `"ELS2_XCA"` - авторизация клиента по DH (Диффи-Хеллмана) - `"ELS2PSKA"` - авторизация клиента по PSK (предварительно разделённому ключу) - `"i2pblinding1"` - поколение Alpha

**Ссылки:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Спецификация HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Спецификация HMAC

---

## Спецификация формата

Зашифрованный LS2 состоит из трёх вложенных слоёв:

1. **Слой 0 (внешний):** Незашифрованная информация для хранения и извлечения
2. **Слой 1 (средний):** Данные аутентификации клиента (зашифрованы)
3. **Слой 2 (внутренний):** Собственно данные LeaseSet2 (зашифрованы)

**Общая структура:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Важно:** Зашифрованный LS2 использует ослеплённые ключи. Destination (адрес назначения) не указывается в заголовке. Место хранения в DHT (распределённая хеш-таблица) — `SHA-256(sig type || blinded public key)`, меняется ежедневно.

### Слой 0 (внешний) - открытый текст

Уровень 0 НЕ использует стандартный заголовок LS2. Он использует специальный формат, оптимизированный для blinded keys (ослеплённых ключей).

**Структура:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Поле Flags (2 байта, биты 15-0):** - **Бит 0:** индикатор офлайн-ключей   - `0` = Офлайн-ключей нет   - `1` = Офлайн-ключи присутствуют (далее следуют временные ключевые данные) - **Биты 1-15:** Зарезервировано, должно быть 0 для будущей совместимости

**Данные временного ключа (присутствуют, если бит флага 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Проверка подписи:** - **Без офлайн-ключей:** Проверяйте с использованием ослеплённого открытого ключа - **С офлайн-ключами:** Проверяйте с использованием временного открытого ключа

Подпись охватывает все данные от Type до outerCiphertext (включительно).

### Уровень 1 (Средний) - Авторизация клиента

**Расшифрование:** См. раздел [Шифрование уровня 1](#layer-1-encryption).

**Структура:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Поле флагов (1 байт, биты 7-0):** - **Бит 0:** Режим авторизации   - `0` = Нет авторизации на уровне клиента (для всех)   - `1` = Авторизация на уровне клиента (далее следует раздел авторизации) - **Биты 3-1:** Схема аутентификации (только если бит 0 = 1)   - `000` = Аутентификация клиента по DH   - `001` = Аутентификация клиента по PSK   - Остальные зарезервированы - **Биты 7-4:** Не используются, должны быть 0

**Данные авторизации клиента DH (флаги = 0x01, биты 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Запись authClient (40 байт):** - `clientID_i`: 8 байт - `clientCookie_i`: 32 байта (зашифрованный authCookie)

**Данные авторизации клиента PSK (флаги = 0x03, биты 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Запись authClient (40 байт):** - `clientID_i`: 8 байт - `clientCookie_i`: 32 байта (зашифрованный authCookie)

### Уровень 2 (внутренний) - данные LeaseSet

**Расшифрование:** См. раздел [Шифрование уровня 2](#layer-2-encryption).

**Структура:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
Внутренний слой содержит полную структуру LeaseSet2, включая: - заголовок LS2 - информация о Lease (запись с параметрами входящего туннеля) - подпись LS2

**Требования к проверке:** После расшифрования реализации должны проверить: 1. Внутренняя метка времени совпадает с внешней опубликованной меткой времени 2. Внутренний срок действия совпадает с внешним сроком действия 3. Подпись LS2 действительна 4. Данные Lease (запись в leaseSet) корректно сформированы

**Ссылки:** - [Спецификация общих структур](/docs/specs/common-structures/) - подробности формата LeaseSet2

---

## Выработка ключа ослепления

### Обзор

I2P использует additive key blinding scheme (аддитивную схему ослепления ключей) на основе Ed25519 и ZCash RedDSA. Ослеплённые ключи обновляются ежедневно (в полночь UTC) для обеспечения прямой секретности.

**Обоснование проектных решений:**

I2P сознательно решил НЕ использовать подход из Приложения A.2 файла Tor rend-spec-v3.txt. Согласно спецификации:

> "Мы не используем приложение A.2 из документа Tor rend-spec-v3.txt, которое имеет схожие цели проектирования, поскольку ослеплённые открытые ключи в нём могут находиться вне подгруппы простого порядка, что может иметь неизвестные последствия для безопасности."

Additive blinding (аддитивное ослепление) в I2P гарантирует, что ослеплённые ключи остаются в подгруппе простого порядка кривой Ed25519.

### Математические определения

**Параметры Ed25519:** - `B`: базовая точка Ed25519 (генератор) = `2^255 - 19` - `L`: порядок Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Ключевые переменные:** - `A`: Неослеплённый 32-байтовый открытый ключ подписи (в Destination) - `a`: Неослеплённый 32-байтовый закрытый ключ подписи - `A'`: Ослеплённый 32-байтовый открытый ключ подписи (используется в зашифрованном LeaseSet) - `a'`: Ослеплённый 32-байтовый закрытый ключ подписи - `alpha`: 32-байтовый фактор ослепления (секрет)

**Вспомогательные функции:**

#### LEOS2IP(x)

"Преобразование октетной строки Little-Endian (младший порядок байтов) в целое число"

Преобразует массив байтов в формате little-endian в целочисленное представление.

#### H*(x)

"Хеш и редукция"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Та же операция, что и при генерации ключа Ed25519.

### Поколение Альфа

**Ежедневная ротация:** Новое значение alpha (секретный параметр ослепления) и blinded keys (ослеплённые ключи) ДОЛЖНЫ быть сгенерированы каждый день в полночь по UTC (00:00:00 UTC).

**Алгоритм GENERATE_ALPHA(destination, date, secret):**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Проверенные параметры:** - Персонализация соли: "I2PGenerateAlpha" - Параметр info для HKDF: "i2pblinding1" - Выходные данные: 64 байта до редукции - Распределение alpha: распределено так же, как закрытые ключи Ed25519 после `mod L`

### Ослепление закрытого ключа

**Алгоритм BLIND_PRIVKEY(a, alpha):**

Для владельца назначения, публикующего зашифрованный LeaseSet:

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Критически важно:** Приведение `mod L` необходимо для сохранения корректного алгебраического соотношения между закрытым и открытым ключами.

### Ослепление открытого ключа

**Алгоритм BLIND_PUBKEY(A, alpha):**

Для клиентов, получающих и проверяющих зашифрованный LeaseSet:

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Математическая эквивалентность:**

Оба метода дают одинаковые результаты:

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
Это потому, что:

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Подписание с ослеплёнными ключами

**Неослеплённое подписание LeaseSet:**

Неослеплённый LeaseSet (отправляется непосредственно аутентифицированным клиентам) подписывается с использованием: - Стандартной подписи Ed25519 (тип 7) или Red25519 (тип 11) - Неослеплённого закрытого ключа для подписи - Проверяется с использованием неослеплённого открытого ключа

**С офлайн-ключами:** - Подписано временным закрытым ключом без ослепления - Проверено временным открытым ключом без ослепления - Оба должны иметь тип 7 или 11

**Подписание зашифрованного LeaseSet:**

Внешняя часть зашифрованного LeaseSet использует подписи Red25519 с ослеплёнными ключами.

**Алгоритм подписи Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Ключевые отличия от Ed25519:** 1. Использует 80 байт случайных данных `T` (не хэш закрытого ключа) 2. Использует значение открытого ключа напрямую (не хэш закрытого ключа) 3. Каждая подпись уникальна даже для одного и того же сообщения и ключа

**Проверка:**

То же, что и Ed25519:

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Соображения безопасности

**Альфа-дистрибутив:**

В целях безопасности alpha должна распределяться идентично неослеплённым закрытым ключам. При ослеплении Ed25519 (type 7) в Red25519 (type 11) распределения слегка отличаются.

**Рекомендация:** используйте Red25519 (type 11) как для неослеплённых, так и для ослеплённых ключей, чтобы соответствовать требованиям ZCash: "комбинация повторно рандомизированного открытого ключа и подписей, созданных с использованием этого ключа, не позволяет раскрыть исходный ключ, на основе которого он был повторно рандомизирован."

**Поддержка типа 7:** Ed25519 поддерживается для обеспечения обратной совместимости с существующими назначениями, но для новых шифрованных назначений рекомендуется тип 11.

**Преимущества ежедневной ротации:** - Прямая секретность: компрометация сегодняшнего ослеплённого ключа не раскрывает вчерашний ключ - Несвязываемость: ежедневная ротация предотвращает долгосрочное отслеживание через DHT - Разделение ключей: разные ключи для разных периодов времени

**Ссылки:** - [Спецификация протокола Zcash](https://zips.z.cash/protocol/protocol.pdf) - Раздел 5.4.6.1 - [Обсуждение Tor Key Blinding (ослепление ключа)](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Тикет Tor #8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Шифрование и обработка

### Деривация Subcredential (производного учетного идентификатора)

Перед шифрованием мы вычисляем credential (учетные данные) и subcredential (производные учетные данные), чтобы привязать зашифрованные слои к знанию открытого ключа подписи Destination (идентификатор назначения в I2P).

**Цель:** Обеспечить, чтобы только те, кто знает открытый ключ подписи Destination (адрес назначения в I2P), могли расшифровать зашифрованный LeaseSet. Полный Destination не требуется.

#### Вычисление учетных данных

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Разделение доменов:** Строка персонализации "credential" гарантирует, что этот хеш не будет конфликтовать с какими-либо ключами поиска в DHT или с другими применениями протокола.

#### Вычисление Subcredential (вспомогательных учетных данных)

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Назначение:** subcredential (подучётные данные) привязывает зашифрованный LeaseSet к: 1. Конкретному Destination (через учётные данные) 2. Конкретному ослеплённому ключу (через blindedPublicKey) 3. Конкретному дню (через ежедневную ротацию blindedPublicKey)

Это предотвращает атаки повторного воспроизведения и междневное связывание.

### Шифрование уровня 1

**Контекст:** Слой 1 содержит данные авторизации клиента и зашифрован ключом, производным от subcredential (дополнительные учетные данные).

#### Алгоритм шифрования

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Вывод:** `outerCiphertext` составляет `32 + len(outerPlaintext)` байт.

**Свойства безопасности:** - Соль обеспечивает уникальные пары ключ/IV (инициализационный вектор) даже при одинаковом subcredential (производные учетные данные) - Контекстная строка `"ELS2_L1K"` обеспечивает разделение доменов - ChaCha20 обеспечивает семантическую безопасность (шифртекст неотличим от случайных данных)

#### Алгоритм расшифрования

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Проверка:** После расшифровки убедитесь, что структура уровня 1 корректно сформирована, прежде чем переходить к уровню 2.

### Шифрование канального уровня

**Контекст:** Уровень 2 содержит фактические данные LeaseSet2 и зашифрован ключом, полученным из authCookie (если включена аутентификация для каждого клиента (per-client auth)) или из пустой строки (если нет).

#### Алгоритм шифрования

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Вывод:** `innerCiphertext` — это `32 + len(innerPlaintext)` байт.

**Привязка ключа:** - Если аутентификация клиента отсутствует: Привязан только к subcredential (дополнительные учетные данные) и метке времени - Если аутентификация клиента включена: Дополнительно привязан к authCookie (различается для каждого авторизованного клиента)

#### Алгоритм расшифрования

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Проверка:** После расшифровки: 1. Проверьте, что байт типа LS2 допустим (3 или 7) 2. Разберите структуру LeaseSet2 3. Проверьте, что внутренняя метка времени соответствует внешней опубликованной метке времени 4. Проверьте, что внутренний срок действия соответствует внешнему сроку действия 5. Проверьте подпись LeaseSet2

### Обзор уровня шифрования

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Процесс расшифровки:** 1. Проверить подпись уровня 0 с использованием ослеплённого открытого ключа 2. Расшифровать уровень 1, используя subcredential (дополнительные учетные данные) 3. Обработать данные авторизации (если есть), чтобы получить authCookie 4. Расшифровать уровень 2, используя authCookie и subcredential 5. Проверить и разобрать LeaseSet2

---

## Поклиентская авторизация

### Обзор

Когда включена авторизация для отдельных клиентов, сервер ведёт список авторизованных клиентов. У каждого клиента есть ключевой материал, который необходимо безопасно передать по отдельному каналу связи (вне основного).

**Два механизма авторизации:** 1. **DH (Диффи-Хеллман) авторизация клиента:** Более безопасная, использует согласование ключей X25519 2. **PSK (предварительно разделённый ключ) авторизация:** Проще, использует симметричные ключи

**Общие свойства безопасности:** - Конфиденциальность состава клиентов: наблюдатели видят число клиентов, но не могут идентифицировать конкретных клиентов - Анонимное добавление/удаление клиентов: невозможно отследить, когда конкретные клиенты добавляются или удаляются - Вероятность коллизии 8-байтового идентификатора клиента: ~1 на 18 квинтиллионов (пренебрежимо мала)

### Авторизация клиента на основе DH

**Обзор:** Каждый клиент генерирует пару ключей X25519 и отправляет свой открытый ключ серверу через безопасный канал out-of-band (вне основного канала). Сервер использует ephemeral DH (временный Диффи-Хеллман) для шифрования уникального authCookie для каждого клиента.

#### Генерация ключей клиента

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Преимущество в безопасности:** Закрытый ключ клиента никогда не покидает устройство клиента. Злоумышленник, перехвативший внеполосную передачу (out-of-band transmission), не сможет расшифровать будущие зашифрованные LeaseSets без взлома X25519 DH.

#### Обработка на сервере

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Структура данных уровня 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Рекомендации для сервера:** - Генерируйте новую эфемерную ключевую пару для каждого публикуемого зашифрованного LeaseSet - Случайно перемешивайте порядок клиентов, чтобы предотвратить отслеживание по позиции - Рассмотрите добавление фиктивных записей, чтобы скрыть истинное количество клиентов

#### Обработка клиентских запросов

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Обработка ошибок на стороне клиента:** - Если `clientID_i` не найден: доступ клиента был отозван или он никогда не был авторизован - Если расшифрование не удалось: повреждённые данные или неверные ключи (крайне редко) - Клиентам следует периодически повторно получать данные для обнаружения отзыва

### Авторизация клиента по PSK (предварительно согласованному ключу)

**Обзор:** У каждого клиента есть предварительно разделённый симметричный ключ длиной 32 байта (PSK — предварительно разделённый ключ). Сервер шифрует один и тот же authCookie с использованием PSK каждого клиента.

#### Генерация ключей

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Примечание по безопасности:** Один и тот же PSK (предварительно разделяемый ключ) может быть общим для нескольких клиентов при желании (создаёт "групповую" авторизацию).

#### Серверная обработка

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Структура данных уровня 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Обработка на стороне клиента

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Сравнение и рекомендации

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Рекомендации:** - **Используйте DH authorization (авторизацию на основе Диффи‑Хеллмана)** для приложений с повышенными требованиями к безопасности, где важна прямая секретность - **Используйте PSK authorization (авторизацию на основе предварительно согласованного ключа)** когда критична производительность или при управлении группами клиентов - **Никогда не используйте повторно PSKs** для разных сервисов или периодов времени - **Всегда используйте безопасные каналы** для распространения ключей (например, Signal, OTR, PGP)

### Соображения безопасности

**Конфиденциальность членства клиента:**

Оба механизма обеспечивают конфиденциальность принадлежности клиента посредством: 1. **Зашифрованных идентификаторов клиента:** 8-байтный clientID, полученный из вывода HKDF 2. **Неотличимых cookie (куки):** Все 32-байтные значения clientCookie выглядят случайными 3. **Отсутствия метаданных, привязанных к клиенту:** Невозможно определить, какая запись относится к какому клиенту

Наблюдатель может видеть:
- Количество авторизованных клиентов (из поля `clients`)
- Изменения количества клиентов со временем

Наблюдатель НЕ может видеть: - Какие конкретные клиенты авторизованы - Когда конкретные клиенты добавляются или удаляются (если количество остаётся прежним) - Любая информация, позволяющая идентифицировать клиента

**Рекомендации по рандомизации:**

Серверам следует случайным образом перемешивать порядок клиентов каждый раз, когда они генерируют зашифрованный LeaseSet:

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Преимущества:** - Не позволяет клиентам узнавать своё положение в списке - Предотвращает inference attacks (атаки по выводу) на основе изменений положения - Делает добавление/отзыв клиента неразличимыми

**Сокрытие количества клиентов:**

Серверы МОГУТ добавлять случайные фиктивные записи:

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Стоимость:** Фиктивные записи увеличивают размер зашифрованного LeaseSet (каждая по 40 байт).

**Ротация AuthCookie:**

Серверам СЛЕДУЕТ генерировать новый authCookie (токен аутентификации): - Каждый раз при публикации зашифрованного LeaseSet (набор параметров входящих туннелей) (обычно каждые несколько часов) - Сразу после отзыва доступа у клиента - По регулярному расписанию (например, ежедневно), даже если нет изменений у клиентов

**Преимущества:** - Ограничивает последствия, если authCookie скомпрометирован - Гарантирует, что отозванные клиенты быстро теряют доступ - Обеспечивает прямую секретность для уровня 2

---

## Адресация Base32 для зашифрованных LeaseSets

### Обзор

Традиционные адреса I2P в base32 содержат только хэш назначения (32 байта → 52 символа). Этого недостаточно для зашифрованных LeaseSets, потому что:

1. Клиентам нужен **неослеплённый открытый ключ**, чтобы вывести ослеплённый открытый ключ
2. Клиентам нужны **типы подписи** (неослеплённой и ослеплённой) для корректной деривации ключа
3. Сам по себе хэш не содержит этой информации

**Решение:** Новый формат base32, включающий типы открытого ключа и подписи.

### Спецификация формата адреса

**Декодированная структура (35 байт):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**Первые 3 байта (исключающее ИЛИ с контрольной суммой):**

Первые 3 байта содержат метаданные, к которым применена операция XOR (побитовое исключающее ИЛИ) с частями контрольной суммы CRC-32:

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Свойства контрольной суммы:** - Использует стандартный полином CRC-32 - Частота ложных отрицательных результатов: ~1 на 16 миллионов - Обнаруживает ошибки при опечатках в адресе - Не подходит для аутентификации (не является криптографически стойким)

**Закодированный формат:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Характеристики:** - Всего символов: 56 (35 байт × 8 бит ÷ 5 бит на символ) - Суффикс: ".b32.i2p" (как в традиционном base32) - Общая длина: 56 + 8 = 64 символа (не включая нулевой терминатор)

**Кодирование Base32:** - Алфавит: `abcdefghijklmnopqrstuvwxyz234567` (стандарт RFC 4648) - 5 неиспользуемых битов в конце ДОЛЖНЫ быть равны 0 - Нечувствительно к регистру (по соглашению — нижний регистр)

### Генерация адреса

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Разбор адресов

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Сравнение с традиционным Base32

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Ограничения использования

**Несовместимость с BitTorrent:**

Зашифрованные адреса LS2 (LeaseSet v2 — вторая версия LeaseSet) НЕ МОГУТ использоваться с компактными ответами на announce в BitTorrent:

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Проблема:** Компактный формат содержит только хэш (32 байта), при этом нет места для типов подписи или информации об открытом ключе.

**Решение:** Используйте полные ответы на announce-запросы или HTTP-трекеры, которые поддерживают полные адреса.

### Интеграция с адресной книгой

Если у клиента в адресной книге есть полный Destination (публичный адрес/идентификатор в I2P):

1. Хранить полный Destination (идентификатор назначения в I2P; включает открытый ключ)
2. Поддерживать обратный поиск по хешу
3. При обнаружении зашифрованного LS2 (LeaseSet v2 — формат leaseSet версии 2), получать открытый ключ из адресной книги
4. Новый формат base32 не требуется, если полный Destination уже известен

**Форматы адресной книги, поддерживающие зашифрованный LS2:** - hosts.txt с полными строками назначения - базы данных SQLite со столбцом назначения - форматы JSON/XML с полными данными назначения

### Примеры реализации

**Пример 1: Генерация адреса**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Пример 2: Разбор и валидация**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Пример 3: Преобразование из Destination (идентификатора назначения)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Соображения безопасности

**Конфиденциальность:** - Адрес Base32 раскрывает открытый ключ - Это сделано намеренно и требуется протоколом - НЕ раскрывает закрытый ключ и не подрывает безопасность - Открытые ключи по замыслу являются общедоступной информацией

**Устойчивость к коллизиям:** - CRC-32 обеспечивает лишь 32 бита устойчивости к коллизиям - Не является криптографически стойким (используйте только для обнаружения ошибок) - НЕ полагайтесь на контрольную сумму для аутентификации - По-прежнему требуется полная проверка назначения

**Проверка адреса:** - Всегда проверяйте контрольную сумму перед использованием - Отклоняйте адреса с недопустимыми типами подписи - Проверьте, что открытый ключ лежит на кривой (зависит от реализации)

**Ссылки:** - [Предложение 149: B32 для Encrypted LS2](/proposals/149-b32-encrypted-ls2/) - [Спецификация адресации B32](/docs/specs/b32-for-encrypted-leasesets/) - [Спецификация именования I2P](/docs/overview/naming/)

---

## Поддержка офлайн‑ключей

### Обзор

Офлайн-ключи позволяют основному ключу подписи оставаться офлайн (в холодном хранении), в то время как для повседневных операций используется временный ключ подписи. Это критически важно для сервисов с повышенными требованиями к безопасности.

**Особые требования к зашифрованному LS2:** - Временные ключи должны генерироваться офлайн - Ослеплённые закрытые ключи должны быть предварительно сгенерированы (по одному в день) - И временные, и ослеплённые ключи передаются партиями - Стандартизированный формат файла ещё не определён (TODO в спецификации)

### Структура офлайн-ключа

**Данные эфемерного ключа уровня 0 (когда бит 0 флага = 1):**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Что охватывает подпись:** Подпись в блоке офлайн-ключа охватывает: - Метка времени истечения срока действия (4 байта) - Тип подписи временного ключа (2 байта)   - Открытый ключ временной подписи (переменной длины)

Эта подпись проверяется с использованием **ослеплённого открытого ключа**, что доказывает, что сторона, обладающая ослеплённым закрытым ключом, санкционировала этот временный ключ.

### Процесс генерации ключей

**Для зашифрованного LeaseSet с офлайн-ключами:**

1. **Сгенерируйте временные пары ключей** (офлайн, в холодном хранилище):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Для каждого дня    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Для каждой даты    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# В полночь по UTC (или до публикации)

date = datetime.utcnow().date()

# Загрузить ключи на сегодня

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Используйте эти ключи для сегодняшнего зашифрованного LeaseSet (записи с перечнем входящих туннелей узла)

```

**Publishing Process:**

```python
# 1. Создайте внутренний LeaseSet2

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Зашифруйте уровень 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Создайте уровень 1 с данными авторизации

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Зашифруйте слой 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Создайте слой 0 с блоком офлайн-подписи

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Подписать слой 0 временным закрытым ключом

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Добавьте подпись и опубликуйте

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Генерируйте каждый день ОБА типа ключей — новые временные и новые blinded keys (ослепленные ключи)

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Пакет зашифрованного ключевого материала   - Охватываемый диапазон дат

OFFLINE_KEY_STATUS   - Количество оставшихся дней   - Дата истечения срока действия следующего ключа

REVOKE_OFFLINE_KEYS     - Диапазон дат для отзыва   - Новые ключи для замены (необязательно)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Включить зашифрованный LeaseSet (набор записей о входящих туннелях)

i2cp.encryptLeaseSet=true

# Необязательно: включите авторизацию клиента

i2cp.enableAccessList=true

# Необязательно: используйте авторизацию DH (по умолчанию — PSK)

i2cp.accessListType=0

# Необязательно: секрет ослепления (настоятельно рекомендуется)

i2cp.blindingSecret=your-secret-here

```

**API Usage Example:**

```java
// Создать зашифрованный LeaseSet EncryptedLeaseSet els = new EncryptedLeaseSet();

// Установить назначение els.setDestination(destination);

// Включить авторизацию для каждого клиента els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Добавьте авторизованных клиентов (публичные ключи DH) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Установите параметры ослепления els.setBlindingSecret("your-secret");

// Подписать и опубликовать els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Включить зашифрованный LeaseSet (описание входящих туннелей назначения)

encryptleaseset = true

# Необязательно: Тип авторизации клиента (0=DH, 1=PSK)

authtype = 0

# Необязательно: Секрет ослепления

secret = your-secret-here

# Необязательно: Авторизованные клиенты (по одному в строке, открытые ключи, закодированные в base64)

client.1 = открытый ключ клиента 1, закодированный в base64 client.2 = открытый ключ клиента 2, закодированный в base64

```

**API Usage Example:**

```cpp
// Создать зашифрованный LeaseSet auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Включить авторизацию для каждого клиента encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Добавить авторизованных клиентов for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Подписать и опубликовать encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Тестовый вектор 1: Ослепление ключа

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Ожидается: (сверить с эталонной реализацией)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Базовая точка Ed25519 (генератор)

B = 2**255 - 19

# Порядок Ed25519 (размер скалярного поля)

L = 2**252 + 27742317777372353535851937790883648493

# Значения типов подписи

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Длины ключей

PRIVKEY_SIZE = 32  # байт PUBKEY_SIZE = 32   # байт SIGNATURE_SIZE = 64  # байт

```

### ChaCha20 Constants

```python
# Параметры ChaCha20 (алгоритма потокового шифрования)

CHACHA20_KEY_SIZE = 32   # байт (256 бит) CHACHA20_NONCE_SIZE = 12  # байт (96 бит) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 допускает 0 или 1

```

### HKDF Constants

```python
# Параметры HKDF

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # байт (HashLen)

# Строки параметра info HKDF (разделение доменов)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# Строки персонализации для SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Размеры слоя 0 (внешнего)

BLINDED_SIGTYPE_SIZE = 2   # байта BLINDED_PUBKEY_SIZE = 32   # байта (для Red25519) PUBLISHED_TS_SIZE = 4      # байта EXPIRES_SIZE = 2           # байта FLAGS_SIZE = 2             # байта LEN_OUTER_CIPHER_SIZE = 2  # байта SIGNATURE_SIZE = 64        # байта (Red25519)

# Размеры блоков офлайн-ключа

OFFLINE_EXPIRES_SIZE = 4   # байт OFFLINE_SIGTYPE_SIZE = 2   # байт OFFLINE_SIGNATURE_SIZE = 64  # байт

# Размеры слоя 1 (среднего)

AUTH_FLAGS_SIZE = 1        # байт EPHEMERAL_PUBKEY_SIZE = 32  # байта (DH аутентификация) AUTH_SALT_SIZE = 32        # байта (PSK аутентификация) NUM_CLIENTS_SIZE = 2       # байта CLIENT_ID_SIZE = 8         # байт CLIENT_COOKIE_SIZE = 32    # байта AUTH_CLIENT_ENTRY_SIZE = 40  # байт (CLIENT_ID + CLIENT_COOKIE)

# Накладные расходы шифрования

SALT_SIZE = 32  # байт (добавляется в начало каждого зашифрованного слоя)

# Base32-адрес

B32_ENCRYPTED_DECODED_SIZE = 35  # bytes B32_ENCRYPTED_ENCODED_LEN = 56   # characters B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Открытый ключ назначения (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Пустой секрет

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 байт

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) по модулю L

```

**Expected Output:**
```
(Сверьте с эталонной реализацией) alpha = [64-байтовое шестнадцатеричное значение]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [сверить с тестовыми векторами RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # Все нули ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [44-байтовое шестнадцатеричное значение]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 байта unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 символов base32].b32.i2p

# Убедитесь, что проверка контрольной суммы выполняется корректно

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.