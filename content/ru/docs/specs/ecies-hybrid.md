---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Пост-квантовый гибридный вариант протокола шифрования ECIES с использованием ML-KEM"
slug: "ecies-hybrid"
category: "Протоколы"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Примечание

Реализация, тестирование и развертывание в процессе в различных реализациях router. Проверьте документацию этих реализаций для получения информации о статусе.

## Обзор

Это PQ-гибридный вариант протокола ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Это первая фаза общего предложения PQ [Prop169](/proposals/169-pq-crypto/), которая была одобрена. См. это предложение для ознакомления с общими целями, моделями угроз, анализом, альтернативами и дополнительной информацией.

Данная спецификация содержит только отличия от стандартного [ECIES](/docs/specs/ecies/) и должна читаться в сочетании с этой спецификацией.

## Дизайн

Мы поддерживаем стандарт NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), который основан на CRYSTALS-Kyber, но НЕ совместим с ним.

Гибридные рукопожатия выполняются в соответствии со спецификацией [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Обмен ключами

Мы определяем гибридный обмен ключами для Ratchet. PQ KEM предоставляет только эфемерные ключи и не поддерживает напрямую рукопожатия со статическими ключами, такие как Noise IK.

Мы определяем три варианта ML-KEM согласно [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), всего для 3 новых типов шифрования. Гибридные типы определены только в сочетании с X25519.

Новые типы шифрования:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
Накладные расходы будут существенными. Типичные размеры сообщений 1 и 2 (для IK) в настоящее время составляют около 100 байт (до любой дополнительной полезной нагрузки). Это увеличится в 8-15 раз в зависимости от алгоритма.

### Требуется новая криптография

- ML-KEM (ранее CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (ранее Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Используется только для SHAKE128
- SHA3-256 (ранее Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 и SHAKE256 (XOF расширения к SHA3-128 и SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Тестовые векторы для SHA3-256, SHAKE128 и SHAKE256 доступны на [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Обратите внимание, что библиотека Java bouncycastle поддерживает все вышеперечисленное. Поддержка библиотеки C++ доступна в OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Спецификация

### Общие структуры

См. спецификацию общих структур [COMMON](/docs/specs/common-structures/) для длины ключей и идентификаторов.

### Схемы рукопожатия

Рукопожатия используют паттерны handshake протокола [Noise](https://noiseprotocol.org/noise.html).

Используется следующее соответствие букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения
- e1 = одноразовый эфемерный PQ ключ, отправляемый от Alice к Bob
- ekem1 = шифротекст KEM, отправляемый от Bob к Alice

Следующие модификации XK и IK для гибридной прямой секретности (hfs) указаны в [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) разделе 5:

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Паттерн e1 определен следующим образом, как указано в [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) раздел 4:

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
Паттерн ekem1 определен следующим образом, как указано в [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) разделе 4:

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
### Определенные операции ML-KEM

Мы определяем следующие функции, соответствующие криптографическим строительным блокам, используемым в соответствии с определением в [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Алиса создает ключи инкапсуляции и декапсуляции. Ключ инкапсуляции отправляется в сообщении NS. Размеры encap_key и decap_key варьируются в зависимости от варианта ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Боб вычисляет зашифрованный текст и общий ключ, используя зашифрованный текст, полученный в сообщении NS. Зашифрованный текст отправляется в сообщении NSR. Размер зашифрованного текста варьируется в зависимости от варианта ML-KEM. kem_shared_key всегда составляет 32 байта.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Алиса вычисляет общий ключ, используя шифртекст, полученный в сообщении NSR. kem_shared_key всегда составляет 32 байта.

Обратите внимание, что как encap_key, так и ciphertext зашифрованы внутри блоков ChaCha/Poly в сообщениях рукопожатия Noise 1 и 2. Они будут расшифрованы в рамках процесса рукопожатия.

kem_shared_key смешивается с chaining key с помощью MixHash(). См. детали ниже.

### KDF рукопожатия Noise

#### Обзор

Гибридное рукопожатие определено в [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Первое сообщение от Алисы к Бобу содержит e1, ключ инкапсуляции, перед полезной нагрузкой сообщения. Это рассматривается как дополнительный статический ключ; вызовите EncryptAndHash() на нем (как Алиса) или DecryptAndHash() (как Боб). Затем обработайте полезную нагрузку сообщения как обычно.

Второе сообщение от Боба к Алисе содержит ekem1, зашифрованный текст, перед полезной нагрузкой сообщения. Это рассматривается как дополнительный статический ключ; вызовите EncryptAndHash() на нем (как Боб) или DecryptAndHash() (как Алиса). Затем вычислите kem_shared_key и вызовите MixKey(kem_shared_key). После этого обработайте полезную нагрузку сообщения как обычно.

#### Идентификаторы Noise

Это строки инициализации Noise:

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF для NS сообщения

После паттерна сообщения 'es' и перед паттерном сообщения 's' добавьте:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF для NS сообщения

После шаблона сообщения 'es' и перед шаблоном сообщения 's', добавьте:

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF для NSR сообщения

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
#### Alice KDF для NSR сообщения

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
#### KDF для split()

неизменный

### Формат сообщения

#### Формат NS

Изменения: Текущий ratchet содержал статический ключ в первой секции ChaCha и полезную нагрузку во второй секции. С ML-KEM теперь есть три секции. Первая секция содержит зашифрованный PQ публичный ключ. Вторая секция содержит статический ключ. Третья секция содержит полезную нагрузку.

Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Расшифрованный формат:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Размеры:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Обратите внимание, что полезная нагрузка должна содержать блок DateTime, поэтому минимальный размер полезной нагрузки составляет 7. Минимальные размеры NS могут быть рассчитаны соответственно.

#### Формат NSR

Изменения: Текущий ratchet имеет пустую полезную нагрузку для первой секции ChaCha и полезную нагрузку во второй секции. С ML-KEM теперь есть три секции. Первая секция содержит зашифрованный PQ шифротекст. Вторая секция имеет пустую полезную нагрузку. Третья секция содержит полезную нагрузку.

Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Расшифрованный формат:

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Размеры:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Обратите внимание, что хотя NSR обычно имеет ненулевую полезную нагрузку, спецификация ratchet [ECIES](/docs/specs/ecies/) этого не требует, поэтому минимальный размер полезной нагрузки составляет 0. Минимальные размеры NSR могут быть рассчитаны соответственно.

## Анализ накладных расходов

### Обмен ключами

Увеличение размера (байты):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Скорость:

Скорости по данным [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Анализ безопасности

Категории безопасности NIST суммированы в [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) слайд 10. Предварительные критерии: Наша минимальная категория безопасности NIST должна быть 2 для гибридных протоколов и 3 для PQ-only.

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
### Рукопожатия

Это все гибридные протоколы. Вероятно, стоит предпочесть MLKEM768; MLKEM512 недостаточно безопасен.

Категории безопасности NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Настройки типа

Рекомендуемый тип для первоначальной поддержки, основанный на категории безопасности и длине ключа:

MLKEM768_X25519 (тип 6)

## Примечания к реализации

### Поддержка библиотек

Библиотеки Bouncycastle, BoringSSL и WolfSSL теперь поддерживают MLKEM. Поддержка OpenSSL появится в их релизе 3.5 от 8 апреля 2025 года [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Общие туннели

Автоматическая классификация/обнаружение множественных протоколов в одних и тех же tunnel должна быть возможна на основе проверки длины сообщения 1 (New Session Message). Используя MLKEM512_X25519 в качестве примера, длина сообщения 1 на 816 байт больше, чем в текущем ratchet протоколе, а минимальный размер сообщения 1 (с включенной только DateTime полезной нагрузкой) составляет 919 байт. Большинство размеров сообщения 1 в текущем ratchet имеют полезную нагрузку менее 816 байт, поэтому их можно классифицировать как не-гибридный ratchet. Большие сообщения, вероятно, являются POST-запросами, которые встречаются редко.

Таким образом, рекомендуемая стратегия заключается в следующем:

- Если сообщение 1 содержит менее 919 байт, это текущий протокол ratchet.
- Если сообщение 1 содержит 919 байт или более, это вероятно MLKEM512_X25519. Сначала попробуйте MLKEM512_X25519, и если это не сработает, попробуйте текущий протокол ratchet.

Это должно позволить нам эффективно поддерживать стандартный ratchet и гибридный ratchet на одном и том же назначении, точно так же, как мы ранее поддерживали ElGamal и ratchet на одном и том же назначении. Таким образом, мы можем гораздо быстрее мигрировать к гибридному протоколу MLKEM, чем если бы мы не могли поддерживать двойные протоколы для одного и того же назначения, поскольку мы можем добавить поддержку MLKEM к существующим назначениям.

Обязательные поддерживаемые комбинации:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Следующие комбинации могут быть сложными и НЕ требуются для поддержки, но могут поддерживаться в зависимости от реализации:

- Более одного MLKEM
- ElG + один или более MLKEM
- X25519 + один или более MLKEM
- ElG + X25519 + один или более MLKEM

Не требуется поддерживать несколько алгоритмов MLKEM (например, MLKEM512_X25519 и MLKEM_768_X25519) для одного и того же назначения. Выберите только один. Зависит от реализации.

Не требуется поддерживать три алгоритма (например, X25519, MLKEM512_X25519 и MLKEM769_X25519) на одном и том же назначении. Классификация и стратегия повторных попыток могут быть слишком сложными. Конфигурация и пользовательский интерфейс конфигурации могут быть слишком сложными. Зависит от реализации.

Не требуется поддерживать алгоритмы ElGamal и гибридные алгоритмы на одном и том же пункте назначения. ElGamal устарел, а использование только ElGamal + гибридный (без X25519) не имеет особого смысла. Также сообщения New Session Message для ElGamal и гибридных алгоритмов являются объемными, поэтому стратегии классификации часто должны были бы пробовать оба варианта расшифровки, что было бы неэффективно. Зависит от реализации.

Клиенты могут использовать одинаковые или разные статические ключи X25519 для протоколов X25519 и гибридного на одних и тех же туннелях, в зависимости от реализации.

### Прямая секретность

Спецификация ECIES позволяет включать Garlic Messages в полезную нагрузку New Session Message, что обеспечивает доставку начального потокового пакета с 0-RTT, обычно HTTP GET, вместе с leaseset клиента. Однако полезная нагрузка New Session Message не обладает прямой секретностью. Поскольку данное предложение подчеркивает улучшенную прямую секретность для ratchet, реализации могут или должны отложить включение потоковой полезной нагрузки или полного потокового сообщения до первого Existing Session Message. Это будет происходить за счет доставки с 0-RTT. Стратегии также могут зависеть от типа трафика или типа tunnel, или от GET против POST, например. Зависит от реализации.

### Размер новой сессии

MLKEM существенно увеличит размер сообщения New Session Message, как описано выше. Это может значительно снизить надежность доставки сообщений New Session Message через туннели, где они должны быть фрагментированы на несколько tunnel-сообщений размером 1024 байта. Успешность доставки пропорциональна экспоненциальному числу фрагментов. Реализации могут использовать различные стратегии для ограничения размера сообщения за счет доставки 0-RTT. Зависит от реализации.

## Ссылки

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
