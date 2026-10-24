---
title: "PQ Hybrid SSU2"
description: "Постквантовый гибридный вариант транспортного протокола SSU2 с использованием ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Транспорты"
accurateFor: "0.9.71"
---

### Статус

Бета Q2 2026, релиз Q3 2026

## Обзор

Это гибридный пост-квантовый вариант транспортного протокола SSU2, разработанный в рамках Proposal 169. Дополнительные сведения см. в этом предложении.

PQ Hybrid SSU2 определяется только на том же адресе и порту, что и стандартный SSU2. Работа на другом порту или без поддержки стандартного SSU2 не разрешена и не будет разрешена в течение нескольких лет, пока стандартный SSU2 не будет признан устаревшим.

Данная спецификация описывает только изменения, необходимые для поддержки PQ Hybrid в стандартном SSU2. Подробности базовой реализации см. в спецификации SSU2.

## Дизайн

Мы поддерживаем стандарты NIST FIPS 203 и 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), которые основаны на CRYSTALS-Kyber и CRYSTALS-Dilithium (версии 3.1, 3 и более ранние), но НЕ совместимы с ними.

### Обмен ключами

PQ KEM обеспечивает только эфемерные ключи и не поддерживает напрямую рукопожатия со статическими ключами, такие как Noise XK и IK. Типы шифрования совпадают с используемыми в PQ Hybrid Ratchet и определены в документе общих структур [/docs/specs/common-structures/](/docs/specs/common-structures/); как и в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), гибридные типы определяются только в сочетании с X25519.

Типы шифрования:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Допустимые комбинации

Новые типы шифрования указываются в RouterAddresses. Тип шифрования в ключевом сертификате по-прежнему будет иметь тип 4.

## Спецификация

### Паттерны рукопожатия

Рукопожатия используют паттерны рукопожатий [Noise Protocol](https://noiseprotocol.org/noise.html).

Используется следующее отображение букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения
- e1 = одноразовый эфемерный PQ-ключ, отправляется от Alice к Bob
- ekem1 = шифртекст KEM, отправляется от Bob к Alice

Следующие модификации XK и IK для гибридной прямой секретности (hfs) соответствуют спецификации [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf), раздел 5:

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Паттерн e1 определяется следующим образом, как указано в разделе 4 [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Паттерн ekem1 определяется следующим образом, как указано в разделе 4 [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF для рукопожатия Noise

#### Обзор

Гибридное рукопожатие определено в [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Первое сообщение, от Alice к Bob, содержит e1 — ключ инкапсуляции — перед полезной нагрузкой сообщения. Он обрабатывается как дополнительный статический ключ: вызовите EncryptAndHash() для него (со стороны Alice) или DecryptAndHash() (со стороны Bob). Затем обработайте полезную нагрузку сообщения в обычном порядке.

Второе сообщение, от Bob к Alice, содержит ekem1 — зашифрованный текст — перед полезной нагрузкой сообщения. Он обрабатывается как дополнительный статический ключ: вызовите EncryptAndHash() для него (на стороне Bob) или DecryptAndHash() (на стороне Alice). Затем вычислите kem_shared_key и вызовите MixKey(kem_shared_key). После этого обработайте полезную нагрузку сообщения в обычном порядке.

#### Определённые операции ML-KEM

Мы определяем следующие функции, соответствующие криптографическим строительным блокам, используемым в соответствии с определением в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Обратите внимание, что как encap_key, так и шифртекст зашифрованы внутри блоков ChaCha/Poly в сообщениях Noise-рукопожатия 1 и 2. Они будут расшифрованы в ходе процесса рукопожатия.

kem_shared_key подмешивается в цепочечный ключ с помощью MixHash(). Подробности см. ниже.

#### KDF Алисы для Сообщения 1

После шаблона сообщения 'es' и перед полезной нагрузкой добавьте:

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF Боба для сообщения 1

После шаблона сообщения 'es' и перед полезной нагрузкой добавьте:

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF Боба для сообщения 2

Для XK: после паттерна сообщения «ee» и перед полезной нагрузкой добавить:

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF Алисы для сообщения 2

После шаблона сообщения 'ee' добавьте:

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF для сообщения 3

без изменений

#### KDF для split()

без изменений

### Детали рукопожатия

#### Идентификаторы Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Обратите внимание, что MLKEM-1024 НЕ поддерживается для SSU2, поскольку ключи слишком велики для размещения в стандартной датаграмме размером 1500 байт.

#### Длинный заголовок

Длинный заголовок занимает 32 байта. Он используется до установления сессии — для сообщений Token Request, SessionRequest, SessionCreated и Retry. Также он применяется для внесессионных сообщений Peer Test и Hole Punch.

В следующих сообщениях установите поле ver (версия) в длинном заголовке равным 3 или 4, чтобы указать MLKEM-512 или MLKEM-768.

- (0) Запрос сеанса
- (1) Сеанс создан
- (9) Повтор (примечание: Повтор с завершением может содержать любую версию 2-4)
- (10) Запрос токена
- (11) Пробивка отверстия (Hole Punch)

В следующих сообщениях устанавливайте поле ver (версия) в длинном заголовке равным 2, как обычно, даже если поддерживается MLKEM-512 или MLKEM-768. Реализации также могут устанавливать значение 3 или 4, если другая сторона поддерживает это, однако это не обязательно. Реализации должны принимать любое значение от 2 до 4.

- (7) Peer Test (внесессионные сообщения 5-7)

Обсуждение: Установка поля версии в значение 3 или 4 может не быть строго обязательной для всех типов сообщений, однако это способствует более раннему обнаружению ошибок при неподдерживаемых постквантовых соединениях. Сообщения Token Request и Retry (типы 9 и 10) должны иметь версии 3/4 для обеспечения согласованности. Сообщения Hole Punch (тип 11) могут не требовать подобной обработки, однако мы будем следовать той же схеме для единообразия. Сообщения Peer Test (тип 7) являются внесессионными и не указывают на намерение инициировать сессию.

- Relay Request (запрос ретрансляции)
- Relay Response (ответ ретрансляции)
- Relay Intro (представление через ретранслятор)
- Peer Test (тест узла)

До шифрования заголовка:

До шифрования заголовка:

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Короткий заголовок

без изменений

#### SessionRequest (Тип 0)

Изменения: в текущей реализации SSU2 раздел ChaCha содержит только блочные данные. С введением ML-KEM раздел ChaCha будет также содержать зашифрованный постквантовый открытый ключ.

Изменение KDF для защиты от спуфинга: для решения проблем, поднятых в Proposal 165 [Prop165]_, но с использованием иного подхода, мы модифицируем KDF для Session Request. Это применяется только для PQ-сессий. KDF для не-PQ-сессий остаётся без изменений.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Необработанное содержимое:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Незашифрованные данные (тег аутентификации Poly1305 не показан):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Размеры, без учёта IP-накладных расходов:

| Тип | Код типа | Длина X | Длина сообщ. 1 | Длина сообщ. 1 (зашифр.) | Длина сообщ. 1 (расшифр.) | Длина PQ-ключа | Длина pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | н/д | слишком большой | | | | |
Примечание: коды типов предназначены только для внутреннего использования. Routers останутся типа 4, а поддержка будет указана в адресах router.

Минимальный MTU для MLKEM768_X25519: 1318 для IPv4 и 1338 для IPv6. См. ниже.

Изменения: текущий SSU2 содержит только полезную нагрузку в одном разделе ChaCha. При использовании ML-KEM появится новый раздел ChaCha перед полезной нагрузкой, содержащий зашифрованный PQ-шифртекст.

#### SessionCreated (Тип 1)

Изменения: текущий SSU2 содержит только полезную нагрузку в одном разделе ChaCha. При использовании ML-KEM появится новый раздел ChaCha перед полезной нагрузкой, содержащий зашифрованный PQ-шифртекст.

Необработанное содержимое:

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Незашифрованные данные (тег аутентификации Poly1305 не показан):

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Размеры, без учёта IP-накладных расходов:

| Тип | Код типа | Длина Y | Длина Msg 2 | Длина зашифрованного Msg 2 | Длина расшифрованного Msg 2 | Длина PQ CT | Длина pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | н/д | слишком велико | | | | |
Примечание: коды типов предназначены только для внутреннего использования. Routers останутся типа 4, а поддержка будет указана в адресах router.

Минимальный MTU для MLKEM768_X25519: 1318 для IPv4 и 1338 для IPv6. См. ниже.

Максимальный размер: у Алисы еще нет RouterInfo Боба, и она не знает его опубликованный MTU. Для этого сообщения используйте временный MTU следующим образом. Для MLKEM512_X25519 используйте максимум из 1280 или размера полученного SessionRequest в качестве MTU. Для MLKEM768_X25519 используйте максимум из (1318 для IPv4 или 1338 для IPv6) или размера полученного SessionRequest в качестве MTU. Накладные расходы SessionCreated меньше, чем накладные расходы SessionRequest, поскольку шифротекст MLKEM меньше открытого ключа MLKEM. Это позволяет использовать диапазон размеров дополнения в SessionCreated, даже если в SessionRequest было мало или совсем не было дополнения.

#### SessionConfirmed (Тип 2)

без изменений

#### KDF для фазы передачи данных

без изменений

#### Ретрансляция и тестирование узлов

Следующие блоки содержат поля версии. Они останутся версии 2 (для совместимости с Bob без постквантовой защиты) и не будут изменены на версию 3/4 для постквантового режима.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Опубликованные адреса

Во всех случаях используйте имя транспорта SSU2 как обычно. MLKEM-1024 не поддерживается.

Используйте тот же адрес/порт, что и для не-PQ, не заблокированного брандмауэром варианта. Поддерживается один или оба PQ-варианта. В адресе router опубликуйте v=2 (как обычно) и новый параметр pq=[3|4|3,4|4,3], чтобы указать MLKEM 512/768/оба. Роутеры с MTU меньше минимального значения, указанного ниже, не должны публиковать параметр «pq», содержащий «4». Публикуйте 4,3 для указания предпочтения MLKEM-768 или 3,4 для указания предпочтения MLKEM-512. Фактическая версия определяется инициатором, и предпочтение может не учитываться. Роутеры с MTU меньше минимального значения, указанного ниже, не должны устанавливать соединение с использованием MLKEM768. Старые роутеры будут игнорировать параметр pq и подключаться в обычном не-PQ режиме.

Использование другого адреса/порта для не-PQ вариантов, или режим только-PQ без файрвола НЕ поддерживается. Эта функция не будет реализована до отключения не-PQ SSU2, что произойдёт через несколько лет. После отключения не-PQ будет поддерживаться один или оба PQ-варианта. В адресе router публикуйте v=[3|4|3,4|4,3], чтобы указать поддержку MLKEM 512/768/обоих вариантов. Старые router'ы проверят параметр v и пропустят этот адрес как неподдерживаемый.

Адреса за межсетевым экраном (IP не публикуется): в адресе router публикуется v=2 (как обычно). Параметр pq ДОЛЖЕН быть опубликован в адресах за межсетевым экраном для поддержки ретрансляции.

Алиса может подключиться к Bob с постквантовой поддержкой (PQ Bob), используя PQ-вариант, который публикует Bob, независимо от того, рекламирует ли Алиса поддержку PQ в своём router info и поддерживает ли она тот же вариант.

#### MTU

Соблюдайте осторожность, чтобы не превысить MTU при использовании MLKEM768. Минимальный MTU для MLKEM768_X25519 составляет 1318 для IPv4 и 1338 для IPv6 (при условии минимальной полезной нагрузки 10 байт с блоком DateTime и блоком Padding или RelayTagRequest). Минимальный MTU для SSU2 в целом равен 1280, поэтому не все узлы могут использовать MLKEM768. Не публикуйте и не используйте MLKEM768, если фактический MTU — как локальный, так и объявленный удалённым узлом — меньше минимального значения. Следите за тем, чтобы добавление padding не приводило к превышению локального или удалённого MTU для сообщений 1 или 2.

## Анализ накладных расходов

### Обмен ключами

Увеличение размера (байты):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Анализ безопасности

Категории безопасности NIST кратко изложены в [презентации NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) на слайде 10. Предварительные критерии: минимальная категория безопасности NIST должна быть не ниже 2 для гибридных протоколов и не ниже 3 для протоколов, использующих исключительно постквантовую криптографию (PQ-only).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Процедуры установления соединения (Handshakes)

Все это гибридные протоколы. Реализациям следует отдавать предпочтение MLKEM768; MLKEM512 недостаточно безопасен.

Категории безопасности NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Примечания по реализации

### Поддержка библиотек

Библиотеки Bouncycastle, BoringSSL и WolfSSL уже поддерживают MLKEM и MLDSA. Поддержка в OpenSSL появится в релизе 3.5, запланированном на 8 апреля 2025 года [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Идентификация входящего трафика

Мы устанавливаем старший бит эфемерного ключа (key[31] & 0x80) в запросе сессии, чтобы обозначить, что это гибридное соединение. Это позволяет запускать как стандартный NTCP, так и гибридный NTCP на одном и том же порту. Для входящих соединений поддерживается только один гибридный вариант, который и объявляется в адресе router. Например, pq=3 или pq=4.

## Совместимость роутеров

### Названия транспортов

Для Алисы при PQ-соединении перед обфускацией установите X[31] |= 0x80. Это делает X недопустимым открытым ключом X25519. После обфускации AES-CBC рандомизирует его. Старший бит X будет случайным после обфускации.

## Ссылки

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
