---
title: "Гибридное шифрование ECIES-X25519-AEAD-Ratchet (криптографический «рэтчет»-механизм)"
description: "Постквантовый гибридный вариант протокола шифрования ECIES с использованием ML-KEM"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Статус реализации

**Текущее развертывание:** - **i2pd (реализация на C++)**: Полностью реализовано в версии 2.58.0 (сентябрь 2025) с поддержкой ML-KEM-512, ML-KEM-768 и ML-KEM-1024. Постквантовое сквозное шифрование включено по умолчанию при наличии OpenSSL 3.5.0 или новее. - **Java I2P**: Еще не реализовано на момент версий 0.9.67 / 2.10.0 (сентябрь 2025). Спецификация утверждена, реализация запланирована для будущих релизов.

В этой спецификации описана утверждённая функциональность, которая в настоящее время внедрена в i2pd и планируется к внедрению в реализациях Java I2P.

## Обзор

Это постквантовый гибридный вариант протокола ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Он представляет собой первую фазу Предложения 169 [Prop169](/proposals/169-pq-crypto/), вынесенную на утверждение. Общие цели, модели угроз, анализ, альтернативы и дополнительную информацию см. в указанном предложении.

Статус предложения 169: **Открыто** (первая фаза утверждена для реализации гибридной ECIES (схемы интегрированного шифрования на эллиптических кривых)).

Эта спецификация содержит только отличия от стандартной [ECIES](/docs/specs/ecies/) и должна читаться совместно с указанной спецификацией.

## Проектирование

Мы используем стандарт NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), который основан на CRYSTALS-Kyber (постквантовый KEM-алгоритм; версии 3.1, 3 и более ранние), но с ним не совместим.

Гибридные рукопожатия объединяют классический X25519 Diffie-Hellman с постквантовыми механизмами капсулирования ключей ML-KEM (постквантовый механизм капсулирования ключей, ранее известный как Kyber). Этот подход основан на концепциях гибридной прямой секретности, описанных в исследовании PQNoise и аналогичных реализациях в TLS 1.3, IKEv2 и WireGuard.

### Обмен ключами

Мы определяем гибридный обмен ключами для Ratchet (механизма ратчета). Постквантовая KEM (механизм капсуляции ключей) предоставляет только эфемерные ключи и напрямую не поддерживает рукопожатия со статическими ключами, такие как Noise IK.

Мы определяем три варианта ML-KEM (механизм капсуляции ключей на базе модульных решеток) как определено в [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), что в итоге дает три новых типа шифрования. Гибридные типы определены только в сочетании с X25519.

Новые типы шифрования:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Примечание:** MLKEM768_X25519 (тип 6) — рекомендуемый вариант по умолчанию, обеспечивающий надёжную постквантовую безопасность при разумных накладных расходах.

Накладные расходы значительны по сравнению с шифрованием только на X25519. Типичные размеры сообщений 1 и 2 (для IK pattern — шаблон IK в протоколе Noise) сейчас составляют около 96–103 байт (без дополнительной полезной нагрузки). Это увеличится примерно в 9–12 раз для MLKEM512, в 13–16 раз для MLKEM768 и в 17–23 раза для MLKEM1024, в зависимости от типа сообщения.

### Требуется новая криптография

- **ML-KEM** (ранее CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Стандарт механизма инкапсуляции ключей на основе модульных решёток
- **SHA3-256** (ранее Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Часть стандарта SHA-3
- **SHAKE128 and SHAKE256** (расширения XOF (функции с расширяемой длиной выхода) к SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Функции с расширяемой длиной выхода

Тестовые векторы для SHA3-256, SHAKE128 и SHAKE256 доступны в [Программе по валидации криптографических алгоритмов NIST](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Поддержка библиотек:** - Java: библиотека Bouncycastle версии 1.79 и новее поддерживает все варианты ML-KEM и функции SHA3/SHAKE - C++: OpenSSL 3.5 и новее включает полную поддержку ML-KEM (релиз: апрель 2025 года) - Go: Доступно несколько библиотек для реализации ML-KEM и SHA3

## Спецификация

### Общие структуры

См. [спецификацию общих структур](/docs/specs/common-structures/) для сведений о длинах ключей и идентификаторах.

### Шаблоны рукопожатия

Рукопожатия используют шаблоны рукопожатий [Noise Protocol Framework](https://noiseprotocol.org/noise.html) с адаптациями, специфичными для I2P, обеспечивающими гибридную постквантовую безопасность.

Используется следующее сопоставление букв:

- **e** = одноразовый эфемерный ключ (X25519)
- **s** = статический ключ
- **p** = полезная нагрузка сообщения
- **e1** = одноразовый эфемерный PQ (постквантовый) ключ, отправляемый от Алисы Бобу (токен, специфичный для I2P)
- **ekem1** = шифротекст KEM (механизм инкапсуляции ключа), отправляемый от Боба Алисе (токен, специфичный для I2P)

**Важное примечание:** Имена шаблонов "IKhfs" и "IKhfselg2" и токены "e1" и "ekem1" — это I2P-специфичные адаптации, не задокументированные в официальной спецификации Noise Protocol Framework (фреймворк протокола Noise). Они представляют собой нестандартные определения для интеграции ML-KEM в шаблон Noise IK. Хотя гибридный подход X25519 + ML-KEM широко признан в исследованиях по постквантовой криптографии и других протоколах, используемая здесь специфическая терминология является I2P-специфичной.

Применяются следующие модификации к IK (шаблон рукопожатия Noise IK) для обеспечения гибридной прямой секретности:

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
Шаблон **e1** определяется следующим образом:

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
Шаблон **ekem1** определяется следующим образом:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Определённые операции ML-KEM (механизм капсулирования ключей на основе модульных решёток)

Мы определяем следующие функции, соответствующие криптографическим примитивам, определённым в [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Алиса создаёт ключи инкапсуляции и декапсуляции. Ключ инкапсуляции отправляется в сообщении NS. Размеры ключей:   - ML-KEM-512: encap_key = 800 байт, decap_key = 1632 байт   - ML-KEM-768: encap_key = 1184 байт, decap_key = 2400 байт   - ML-KEM-1024: encap_key = 1568 байт, decap_key = 3168 байт

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Боб вычисляет шифртекст и общий ключ, используя ключ инкапсуляции, полученный в сообщении NS. Шифртекст отправляется в сообщении NSR. Размеры шифртекста:   - ML-KEM-512: 768 байт   - ML-KEM-768: 1088 байт   - ML-KEM-1024: 1568 байт

kem_shared_key всегда имеет длину **32 байта** для всех трёх вариантов.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Алиса вычисляет общий ключ, используя ciphertext, полученный в сообщении NSR. Значение kem_shared_key всегда равно **32 байта**.

**Важно:** И encap_key, и шифртекст зашифрованы внутри блоков ChaCha20-Poly1305 в сообщениях 1 и 2 рукопожатия Noise. Они будут расшифрованы как часть процесса рукопожатия.

kem_shared_key смешивается в цепной ключ с помощью MixKey(). Подробности см. ниже.

### KDF (функция выработки ключа) рукопожатия Noise

#### Обзор

Гибридное рукопожатие сочетает классический X25519 ECDH с постквантовой ML-KEM (механизм инкапсуляции ключей). Первое сообщение, от Алисы к Бобу, содержит e1 (ключ инкапсуляции ML-KEM) перед полезной нагрузкой сообщения. Это рассматривается как дополнительный ключевой материал; вызовите EncryptAndHash() для него (со стороны Алисы) или DecryptAndHash() (со стороны Боба). Затем обработайте полезную нагрузку сообщения как обычно.

Второе сообщение, от Боба к Алисе, содержит ekem1 (шифротекст ML-KEM) перед полезной нагрузкой сообщения. Это рассматривается как дополнительный ключевой материал; примените EncryptAndHash() к нему (со стороны Боба) или DecryptAndHash() (со стороны Алисы). Затем вычислите kem_shared_key и вызовите MixKey(kem_shared_key). Затем обработайте полезную нагрузку сообщения как обычно.

#### Идентификаторы Noise (криптографический протокол)

Это строки инициализации Noise (специфичные для I2P):

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### KDF Алисы для сообщения NS

После шаблона сообщения 'es' и перед шаблоном сообщения 's' добавьте:

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
#### Bob KDF для сообщения NS

После шаблона сообщения 'es' и перед шаблоном сообщения 's' добавьте:

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
#### KDF (функция выработки ключей) Боба для сообщения NSR

После шаблона сообщения 'ee' и перед шаблоном сообщения 'se' добавьте:

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
```
#### KDF Алисы для сообщения NSR

После шаблона сообщения 'ee' и перед шаблоном сообщения 'ss' добавьте:

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
```
#### KDF (функция выработки ключа) для split()

Функция split() остаётся неизменной по сравнению со стандартной спецификацией ECIES (схема интегрированного шифрования на эллиптических кривых). После завершения рукопожатия:

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Это двунаправленные сеансовые ключи для продолжающегося обмена данными.

### Формат сообщения

#### Формат NS (New Session — новая сессия)

**Изменения:** Текущий ratchet (механизм ратчета) содержит статический ключ в первом разделе ChaCha20-Poly1305, а полезную нагрузку — во втором разделе. При использовании ML-KEM (схема согласования ключей на модульных решётках) теперь три раздела. В первом разделе находится зашифрованный открытый ключ ML-KEM (encap_key). Во втором разделе находится статический ключ. В третьем разделе находится полезная нагрузка.

**Размеры сообщений:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Примечание:** Полезная нагрузка должна содержать блок DateTime (не менее 7 байт: 1 байт — тип, 2 байта — размер, 4 байта — временная метка). Соответственно могут быть рассчитаны минимальные размеры NS. Таким образом, минимальный практический размер NS составляет 103 байта для X25519, а для гибридных вариантов лежит в диапазоне от 919 до 1687 байт.

Увеличения размера на 816, 1200 и 1584 байт для трёх вариантов ML-KEM объясняются тем, что они включают публичный ключ ML-KEM и 16-байтовый Poly1305 MAC для аутентифицированного шифрования.

#### Формат NSR (New Session Reply — ответ на новый сеанс)

**Изменения:** В текущем ratchet (механизм обновления ключей) первая секция ChaCha20-Poly1305 содержит пустую полезную нагрузку, а полезная нагрузка находится во второй секции. С ML-KEM теперь три секции. Первая секция содержит зашифрованный шифртекст ML-KEM. Вторая секция имеет пустую полезную нагрузку. Третья секция содержит полезную нагрузку.

**Размеры сообщений:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Увеличения размера на 784, 1104 и 1584 байта для трёх вариантов ML-KEM обусловлены тем, что они включают шифротекст ML-KEM и 16-байтовый Poly1305 MAC (код аутентификации сообщения) для аутентифицированного шифрования.

## Анализ накладных расходов

### Обмен ключами

Накладные расходы гибридного шифрования существенны по сравнению с использованием только X25519:

- **MLKEM512_X25519**: Примерное увеличение размера сообщения рукопожатия в 9-12x (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Примерное увеличение размера сообщения рукопожатия в 13-16x (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Примерное увеличение размера сообщения рукопожатия в 17-23x (NS: 17.5x, NSR: 23x)

Эти накладные расходы приемлемы ради дополнительных преимуществ постквантовой безопасности. Коэффициенты различаются в зависимости от типа сообщения, поскольку базовые размеры сообщений отличаются (для NS минимум 96 байт, для NSR минимум 72 байта).

### Соображения по пропускной способности

Для типичного установления сеанса с минимальными полезными данными: - Только X25519: ~200 байт всего (NS + NSR) - MLKEM512_X25519: ~1,800 байт всего (увеличение в 9 раз) - MLKEM768_X25519: ~2,500 байт всего (увеличение в 12,5 раза) - MLKEM1024_X25519: ~3,400 байт всего (увеличение в 17 раз)

После установления сеанса дальнейшее шифрование сообщений использует тот же формат передачи данных, что и в сеансах, использующих только X25519 (алгоритм обмена ключами на эллиптической кривой Curve25519), поэтому для последующих сообщений накладные расходы отсутствуют.

## Анализ безопасности

### Рукопожатия

Гибридное рукопожатие обеспечивает как классическую (X25519), так и постквантовую (ML-KEM) криптографическую стойкость. Злоумышленнику необходимо взломать **оба** механизма — классический ECDH (обмен ключами Диффи — Хеллмана на эллиптических кривых) и постквантовый KEM (механизм инкапсуляции ключа), — чтобы скомпрометировать сеансовые ключи.

Это обеспечивает: - **Текущая безопасность**: X25519 ECDH обеспечивает защиту от классических противников (128-битный уровень безопасности) - **Будущая безопасность**: ML-KEM обеспечивает защиту от квантовых противников (зависит от набора параметров) - **Гибридная безопасность**: Обе должны быть взломаны, чтобы скомпрометировать сеанс (уровень безопасности = максимум из обоих компонентов)

### Уровни безопасности

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Примечание:** Гибридный уровень стойкости ограничивается более слабым из двух компонентов. Во всех случаях X25519 обеспечивает 128-битную классическую стойкость. Если станет доступен криптографически значимый квантовый компьютер, уровень стойкости будет зависеть от выбранного набора параметров ML-KEM (модульно-решеточный механизм инкапсуляции ключа).

### Прямая секретность

Гибридный подход сохраняет свойства прямой секретности (forward secrecy). Сеансовые ключи получаются из двух эфемерных обменов ключами: X25519 и ML-KEM. Если после рукопожатия уничтожаются эфемерные закрытые ключи X25519 или ML-KEM, прошлые сеансы невозможно расшифровать даже в случае компрометации долговременных статических ключей.

Шаблон IK обеспечивает полную прямую секретность (уровень конфиденциальности Noise 5) после отправки второго сообщения (NSR).

## Настройки типов

Реализации должны поддерживать несколько гибридных типов и согласовывать наиболее сильный совместно поддерживаемый вариант. Порядок предпочтения должен быть следующим:

1. **MLKEM768_X25519** (Type 6) - Рекомендуемый выбор по умолчанию, оптимальный баланс безопасности и производительности
2. **MLKEM1024_X25519** (Type 7) - Максимальная безопасность для приложений с повышенными требованиями к безопасности
3. **MLKEM512_X25519** (Type 5) - Базовый уровень постквантовой безопасности для сценариев с ограниченными ресурсами
4. **X25519** (Type 4) - Только классическая криптография, резервный вариант для совместимости

**Обоснование:** MLKEM768_X25519 рекомендуется в качестве варианта по умолчанию, поскольку обеспечивает безопасность категории 3 по NIST (эквивалент AES-192), которая считается достаточной защитой от квантовых компьютеров, при этом сохраняются разумные размеры сообщений. MLKEM1024_X25519 обеспечивает более высокий уровень безопасности, но сопровождается существенно большими накладными расходами.

## Примечания по реализации

### Поддержка библиотек

- **Java**: Библиотека Bouncycastle версии 1.79 (август 2024 года) и новее поддерживает все требуемые варианты ML-KEM и функции SHA3/SHAKE. Используйте `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` для соответствия FIPS 203.
- **C++**: OpenSSL 3.5 (апрель 2025 года) и новее включает поддержку ML-KEM через интерфейс EVP_KEM. Это релиз долгосрочной поддержки, сопровождается до апреля 2030 года.
- **Go**: Доступно несколько сторонних библиотек для ML-KEM и SHA3, включая библиотеку CIRCL от Cloudflare.

### Стратегия миграции

Реализации должны: 1. Поддерживать как варианты только X25519 (кривая для ECDH), так и гибридные варианты ML-KEM (постквантовая схема согласования ключей) в переходный период 2. Предпочитать гибридные варианты, когда оба узла их поддерживают 3. Сохранять возможность отката на вариант только X25519 для обеспечения обратной совместимости 4. Учитывать ограничения пропускной способности сети при выборе варианта по умолчанию

### Совместно используемые Tunnels

Увеличение размеров сообщений может повлиять на использование общих tunnel. Реализациям следует учесть: - Объединять рукопожатия в пакеты, когда это возможно, чтобы распределить накладные расходы - Использовать более короткие сроки истечения для гибридных сеансов, чтобы сократить объём сохраняемого состояния - Отслеживать использование пропускной способности и соответствующим образом настраивать параметры - Реализовать контроль перегрузки для трафика установления сеанса

### Соображения по размеру новой сессии

Из-за увеличенного размера сообщений рукопожатия реализациям может понадобиться: - Увеличить размеры буферов для согласования сеанса (рекомендуется минимум 4 КБ) - Скорректировать значения таймаутов для более медленных соединений (учитывать ~в 3–17 раз более крупные сообщения) - Рассмотреть сжатие полезных данных в сообщениях NS/NSR - Реализовать обработку фрагментации, если это требуется транспортным уровнем

### Тестирование и валидация

Реализации должны проверять: - Корректную генерацию ключей ML-KEM, инкапсуляцию и декапсуляцию - Правильную интеграцию kem_shared_key в Noise KDF (функция выработки ключей протокола Noise) - Соответствие вычислений размеров сообщений спецификации - Совместимость с другими реализациями I2P router - Поведение при недоступности ML-KEM (резервный режим)

Тестовые векторы для операций ML-KEM доступны в NIST [Cryptographic Algorithm Validation Program](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

## Совместимость версий

**Нумерация версий I2P:** I2P поддерживает две параллельные схемы версионирования: - **Версия релиза Router**: формат 2.x.x (например, 2.10.0, выпущена в сентябре 2025 г.) - **Версия API/протокола**: формат 0.9.x (например, 0.9.67 соответствует router 2.10.0)

Данная спецификация ссылается на версию протокола 0.9.67, соответствующую релизу router 2.10.0 и новее.

**Матрица совместимости:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Ссылки

- **[ECIES]**: [Спецификация ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Предложение 169: постквантовая криптография](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - стандарт ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - стандарт SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Фреймворк протокола Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Спецификация общих структур](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 и Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Документация OpenSSL 3.5 по ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Криптографическая библиотека Java Bouncycastle](https://www.bouncycastle.org/)

---
