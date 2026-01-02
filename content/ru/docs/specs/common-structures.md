---
title: "Общие структуры"
description: "Общие типы данных и форматы сериализации, используемые во всех спецификациях I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

Этот документ определяет базовые структуры данных, используемые во всех протоколах I2P, включая [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/) и другие. Эти общие структуры обеспечивают совместимость между различными реализациями I2P и уровнями протоколов.

### Основные изменения с версии 0.9.58

- ElGamal и DSA-SHA1 признаны устаревшими для Router Identities (используйте X25519 + EdDSA)
- Постквантовая поддержка ML-KEM проходит бета-тестирование (включается по выбору начиная с 2.10.0)
- Параметры service record (запись службы) стандартизированы ([Proposal 167](/proposals/167-service-records/), реализовано в 0.9.66)
- Спецификации сжимаемого padding (дополнение) завершены ([Proposal 161](/ru/proposals/161-ri-dest-padding/), реализовано в 0.9.57)

---

## Общие спецификации типов

### Целое число

**Описание:** Представляет неотрицательное целое число в сетевом порядке байтов (big-endian).

**Содержимое:** от 1 до 8 байт, представляющих беззнаковое целое.

**Использование:** Длины полей, счётчики, идентификаторы типов и числовые значения во всех протоколах I2P.

---

### Дата

**Описание:** Метка времени, представляющая количество миллисекунд с начала эпохи Unix (1 января 1970 00:00:00 GMT).

**Содержимое:** 8-байтовое целое число (unsigned long)

**Специальные значения:** - `0` = Неопределённая или нулевая дата - Максимальное значение: `0xFFFFFFFFFFFFFFFF` (год 584 942 417 355)

**Примечания по реализации:** - Всегда часовой пояс UTC/GMT - Требуется точность до миллисекунд - Используется для истечения срока действия аренды, публикации RouterInfo и проверки меток времени

---

### Строка

**Описание:** Строка в кодировке UTF-8 с префиксом длины.

**Формат:**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Ограничения:** - Максимальная длина: 255 байт (не символов — многобайтные последовательности UTF-8 учитываются как несколько байт) - Длина может быть равна нулю (пустая строка) - Завершающий нулевой байт НЕ включён - Строка НЕ завершается нулевым байтом

**Важно:** последовательности UTF-8 могут использовать несколько байт на символ. Строка из 100 символов может превысить лимит в 255 байт, если используются многобайтовые символы.

---

## Структуры криптографических ключей

### Открытый ключ

**Описание:** Открытый ключ для асимметричного шифрования. Тип и длина ключа зависят от контекста или указаны в Key Certificate (сертификате ключа).

**Тип по умолчанию:** ElGamal (устарел для Router Identities с версии 0.9.58)

**Поддерживаемые типы:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Требования к реализации:**

1. **X25519 (Тип 4) - текущий стандарт:**
   - Используется для шифрования ECIES-X25519-AEAD-Ratchet
   - Обязателен для идентификаторов Router начиная с 0.9.48
   - Кодирование в little-endian (порядок байтов от младшего к старшему; в отличие от других типов)
   - См. [ECIES](/docs/specs/ecies/) и [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (тип 0) - устаревший:**
   - Устарел для Router Identities (идентификаторов router) с версии 0.9.58
   - По-прежнему действителен для Destinations (адресатов в I2P) (поле не используется с 0.6/2005)
   - Использует фиксированные простые числа, определённые в [ElGamal specification](/docs/specs/cryptography/)
   - Поддержка сохраняется для обратной совместимости

3. **MLKEM (постквантовый) - Бета:**
   - Гибридный подход объединяет ML-KEM с X25519
   - По умолчанию НЕ включено в 2.10.0
   - Требует ручной активации через Hidden Service Manager (менеджер скрытых сервисов)
   - См. [ECIES-HYBRID](/docs/specs/ecies/#hybrid) и [Предложение 169](/proposals/169-pq-crypto/)
   - Коды типов и спецификации могут быть изменены

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### Закрытый ключ

**Описание:** Закрытый ключ для асимметричного расшифрования, соответствующий типам PublicKey.

**Хранение:** Тип и длина определяются по контексту или хранятся отдельно в структурах данных/файлах ключей.

**Поддерживаемые типы:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Примечания по безопасности:** - Закрытые ключи ДОЛЖНЫ генерироваться с использованием криптографически стойких генераторов случайных чисел - Закрытые ключи X25519 используют scalar clamping (ограничение скаляра), как определено в RFC 7748 - Ключевой материал ДОЛЖЕН быть безопасно удалён из памяти, когда он больше не нужен

**Документация JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Сеансовый ключ

**Описание:** Симметричный ключ для AES-256 шифрования и расшифрования в tunnel и garlic encryption I2P.

**Содержимое:** 32 байта (256 бит)

**Использование:** - Шифрование на уровне Tunnel (AES-256/CBC с IV) - Шифрование сообщений (garlic encryption) - Сквозное шифрование сеанса

**Генерация:** необходимо использовать криптографически стойкий генератор случайных чисел.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Описание:** Открытый ключ для проверки подписи. Тип и длина указаны в сертификате ключа Destination (адрес назначения в I2P) или определяются из контекста.

**Тип по умолчанию:** DSA_SHA1 (устарел начиная с версии 0.9.58)

**Поддерживаемые типы:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Требования к реализации:**

1. **EdDSA_SHA512_Ed25519 (Тип 7) - текущий стандарт:**
   - По умолчанию для всех новых Router Identities и Destinations (назначений) с конца 2015 года
   - Использует кривую Ed25519 с хешированием SHA-512
   - 32-байтные открытые ключи, 64-байтные подписи
   - Кодирование little-endian (в отличие от большинства других типов)
   - Высокая производительность и безопасность

2. **RedDSA_SHA512_Ed25519 (Тип 11) - специализированный:**
   - Используется ТОЛЬКО для зашифрованных leasesets и blinding (криптографическое ослепление)
   - Никогда не используется для Router Identities или стандартных Destinations (назначений)
   - Ключевые отличия от EdDSA:
     - Закрытые ключи через приведение по модулю (не clamping (фиксирование битов))
     - Подписи включают 80 байт случайных данных
     - Использует открытые ключи напрямую (не хеши закрытых ключей)
   - См. [спецификация Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - Устаревшее:**
   - Помечено как устаревшее для Router Identities начиная с 0.9.58
   - Не рекомендуется для новых назначений
   - 1024-битная DSA с SHA-1 (известные слабости)
   - Поддержка сохраняется только для совместимости

4. **Многокомпонентные ключи:**
   - Когда состоят из двух элементов (например, координаты точки ECDSA X, Y)
   - Каждый элемент дополняется ведущими нулями до длины/2
   - Пример: 64-байтовый ключ ECDSA = 32-байтовый X + 32-байтовый Y

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Описание:** Закрытый ключ для создания подписей, соответствующий типам SigningPublicKey.

**Хранилище:** Тип и длина задаются при создании.

**Поддерживаемые типы:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Требования к безопасности:** - Генерируйте с использованием криптографически стойкого источника случайных чисел - Защищайте с помощью соответствующих механизмов контроля доступа - По завершении безопасно удаляйте из памяти - Для EdDSA: 32-байтовый seed хэшируется с помощью SHA-512, первые 32 байта становятся скаляром (clamped — клампирование, установка определённых битов) - Для RedDSA: иная генерация ключа (редуцирование по модулю вместо clamping)

**Документация JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)

---

### Подпись

**Описание:** Криптографическая подпись данных с использованием алгоритма подписи, соответствующего типу SigningPrivateKey.

**Тип и длина:** Выводятся из типа ключа, используемого для подписи.

**Поддерживаемые типы:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Примечания по формату:** - Многоэлементные подписи (например, значения R и S в ECDSA) дополняются ведущими нулями до длины/2 для каждого элемента - EdDSA и RedDSA используют кодирование с порядком байт little-endian (младший байт первым) - Все остальные типы используют кодирование с порядком байт big-endian (старший байт первым)

**Проверка:** - Используйте соответствующий SigningPublicKey - Следуйте спецификациям алгоритма подписи для данного типа ключа - Проверьте, что длина подписи соответствует ожидаемой для данного типа ключа

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Хэш

**Описание:** SHA-256 хэш данных, широко используемый в I2P для проверки целостности и идентификации.

**Содержимое:** 32 байта (256 бит)

**Использование:** - хэши Router Identity (структуры идентификации router) (ключи сетевой базы данных) - хэши Destination (адресата в I2P) (ключи сетевой базы данных) - идентификация шлюза tunnel в Leases (элементах LeaseSet) - проверка целостности данных - генерация Tunnel ID

**Алгоритм:** SHA-256, как определено в стандарте FIPS 180-4

**Документация JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Сессионный тег

**Описание:** Случайное число, используемое для идентификации сеанса и шифрования на основе тегов.

**Важно:** Размер тега сессии варьируется в зависимости от типа шифрования: - **ElGamal/AES+SessionTag:** 32 байта (устаревший) - **ECIES-X25519:** 8 байт (текущий стандарт)

**Текущий стандарт (ECIES, интегрированная схема шифрования на эллиптических кривых):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
См. [ECIES](/docs/specs/ecies/) и [ECIES-ROUTERS](/docs/specs/ecies/#routers) для получения подробных спецификаций.

**Устаревшее (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Генерация:** ДОЛЖЕН использовать криптографически стойкий генератор случайных чисел.

**Документация JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Описание:** Уникальный идентификатор позиции router в tunnel. Каждый хоп в tunnel имеет свой собственный TunnelId (идентификатор туннеля).

**Формат:**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Использование:** - Идентифицирует входящие/исходящие соединения tunnel на каждом router - Разный TunnelId на каждом переходе в цепочке tunnel - Используется в структурах Lease (элемент Lease — запись параметров доставки) для идентификации шлюзовых tunnel

**Особые значения:** - `0` = Зарезервировано для специальных нужд протокола (не используйте при нормальной работе) - TunnelIds локально значимы для каждого router

**Документация JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Спецификации сертификатов

### Сертификат

**Описание:** Контейнер для подтверждений, доказательства работы или криптографических метаданных, используемых во всём I2P.

**Формат:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Общий размер:** минимум 3 байта (NULL certificate — сертификат NULL), максимум 65538 байт

### Типы сертификатов

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Сертификат ключа (тип 5)

**Введение:** Версия 0.9.12 (декабрь 2013)

**Назначение:** Указывает нестандартные типы ключей и хранит дополнительные данные ключей сверх стандартной 384-байтной структуры KeysAndCert (структура ключей и сертификата).

**Структура полезной нагрузки:**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Критические замечания по реализации:**

1. **Порядок типов ключей:**
   - **ПРЕДУПРЕЖДЕНИЕ:** Тип ключа подписи идет ПЕРЕД типом криптографического ключа
   - Это неинтуитивно, но сохраняется ради совместимости
   - Порядок: SPKtype, CPKtype (не CPKtype, SPKtype)

2. **Структура ключевых данных в KeysAndCert:**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Расчёт избыточных данных ключа:**
   - Если Crypto Key > 256 байт: Excess = (Crypto Length - 256)
   - Если Signing Key > 128 байт: Excess = (Signing Length - 128)
   - Padding (дополнение) = max(0, 384 - Crypto Length - Signing Length)

**Примеры (криптографический ключ ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Требования к Router Identity:** - NULL-сертификат использовался до версии 0.9.15 - Сертификат ключа требуется для нестандартных типов ключей начиная с 0.9.16 - Ключи шифрования X25519 поддерживаются начиная с 0.9.48

**Требования к Destination (адрес назначения в I2P):** - NULL-сертификат ИЛИ Сертификат ключа (по необходимости) - Сертификат ключа обязателен для типов ключей подписи, отличных от значения по умолчанию, начиная с 0.9.12 - Поле открытого криптографического ключа не используется начиная с 0.6 (2005), но по-прежнему должно присутствовать

**Важные предупреждения:**

1. **Сертификат NULL против сертификата KEY:**
   - Сертификат KEY с типами (0,0), указывающими ElGamal+DSA_SHA1, допускается, но не рекомендуется
   - Всегда используйте сертификат NULL для ElGamal+DSA_SHA1 (каноническое представление)
   - Сертификат KEY с (0,0) на 4 байта длиннее и может вызвать проблемы совместимости
   - Некоторые реализации могут некорректно обрабатывать сертификаты KEY с (0,0)

2. **Проверка избыточных данных:**
   - Реализации ДОЛЖНЫ проверять, что длина сертификата соответствует ожидаемой длине для типов ключей
   - Отклонять сертификаты с избыточными данными, не соответствующими типам ключей
   - Не допускать наличия мусорных данных в конце после корректной структуры сертификата

**JavaDoc:** [Сертификат](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Сопоставление

**Описание:** Набор свойств «ключ–значение», используемый для конфигурации и метаданных.

**Формат:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Ограничения по размеру:** - Длина ключа: 0-255 байт (+ 1 байт длины) - Длина значения: 0-255 байт (+ 1 байт длины) - Общий размер отображения: 0-65535 байт (+ 2 байта поля размера) - Максимальный размер структуры: 65537 байт

**Критически важное требование к сортировке:**

Когда отображения присутствуют в **подписанных структурах** (RouterInfo (информация о router), RouterAddress (адрес router), Destination properties (свойства Destination), I2CP SessionConfig (конфигурация сессии I2CP)), записи ДОЛЖНЫ быть отсортированы по ключу для обеспечения инвариантности подписи:

1. **Метод сортировки:** Лексикографическое упорядочивание по значениям кодовых точек Unicode (эквивалентно Java String.compareTo())
2. **Чувствительность к регистру:** Ключи и значения, как правило, чувствительны к регистру (зависит от приложения)
3. **Повторяющиеся ключи:** НЕ допускаются в подписанных структурах (приведёт к ошибке проверки подписи)
4. **Кодировка символов:** побайтовое сравнение в UTF-8

**Почему важна сортировка:** - Подписи вычисляются по байтовому представлению - Разный порядок ключей приводит к разным подписям - Для неподписанных отображений сортировка не требуется, но следует придерживаться того же соглашения

**Примечания по реализации:**

1. **Избыточность кодирования:**
   - Присутствуют и разделители `=` и `;`, и байты длины строки
   - Это неэффективно, но сохранено ради совместимости
   - Байты длины имеют приоритет; разделители обязательны, но избыточны

2. **Поддержка символов:**
   - Несмотря на документацию, `=` и `;` ПОДДЕРЖИВАЮТСЯ внутри строк (это обрабатывается байтами длины)
   - Кодировка UTF-8 поддерживает весь Юникод
   - **Предупреждение:** I2CP использует UTF-8, но I2NP исторически некорректно обрабатывал UTF-8
   - По возможности используйте ASCII для сопоставлений I2NP ради максимальной совместимости

3. **Особые контексты:**
   - **RouterInfo/RouterAddress:** ДОЛЖНЫ быть отсортированы, без дубликатов
   - **I2CP SessionConfig:** ДОЛЖНЫ быть отсортированы, без дубликатов  
   - **Сопоставления приложений:** Сортировка рекомендуется, но не всегда обязательна

**Пример (параметры RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc:** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Спецификация общей структуры

### Ключи и сертификат

**Описание:** Базовая структура, объединяющая ключ шифрования, ключ подписи и сертификат. Используется как RouterIdentity, так и Destination.

**Структура:**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Выравнивание ключа:** - **Криптографический открытый ключ:** Выровнен в начале (байт 0) - **Заполнение:** Посередине (при необходимости) - **Открытый ключ подписи:** Выровнен в конце (с байта 256 по байт 383) - **Сертификат:** Начинается с байта 384

**Расчёт размера:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Рекомендации по генерации заполнения ([Предложение 161](/ru/proposals/161-ri-dest-padding/))

**Версия реализации:** 0.9.57 (январь 2023, релиз 2.1.0)

**Предпосылки:** - Для ключей, отличных от ElGamal+DSA, дополнение присутствует в 384-байтовой фиксированной структуре - Для Destinations (идентификаторов назначения), поле открытого ключа размером 256 байт не используется с версии 0.6 (2005) - Дополнение должно генерироваться так, чтобы хорошо сжиматься, при этом оставаясь безопасным

**Требования:**

1. **Минимальный объём случайных данных:**
   - Используйте не менее 32 байт криптографически стойких случайных данных
   - Это обеспечивает достаточный уровень энтропии для безопасности

2. **Стратегия сжатия:**
   - Повторяйте эти 32 байта по всему полю заполнения/открытого ключа
   - Протоколы, такие как I2NP Database Store, Streaming SYN, SSU2 handshake, используют сжатие
   - Существенная экономия пропускной способности без ущерба для безопасности

3. **Примеры:**

**Идентификатор Router (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destination (адрес назначения в I2P) (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Почему это работает:**
   - Хэш SHA-256 полной структуры по-прежнему содержит всю энтропию
   - Распределение DHT в netDb зависит только от хэша
   - Ключ подписи (32 байта EdDSA/X25519) обеспечивает 256 бит энтропии
   - Дополнительные 32 байта повторяющихся случайных данных = 512 бит суммарной энтропии
   - Более чем достаточно для криптографической стойкости

5. **Примечания по реализации:**
   - ОБЯЗАТЕЛЬНО хранить и передавать полную структуру размером 387+ байт
   - Хэш SHA-256 вычисляется по полной несжатой структуре
   - Сжатие применяется на уровне протокола (I2NP, Streaming, SSU2)
   - Обратно совместимо со всеми версиями, начиная с 0.6 (2005)

**JavaDoc:** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (идентификатор router-а)

**Описание:** Однозначно идентифицирует router в сети I2P. Структура идентична KeysAndCert (ключи и сертификат).

**Формат:** См. структуру KeysAndCert выше

**Текущие требования (по состоянию на 0.9.58):**

1. **Обязательные типы ключей:**
   - **Шифрование:** X25519 (тип 4, 32 байта)
   - **Подпись:** EdDSA_SHA512_Ed25519 (тип 7, 32 байта)
   - **Сертификат:** Key Certificate (тип 5)

2. **Устаревшие типы ключей:**
   - ElGamal (type 0) помечен как устаревший для Router Identities начиная с 0.9.58
   - DSA_SHA1 (type 0) помечен как устаревший для Router Identities начиная с 0.9.58
   - Их НЕ следует использовать для новых routers

3. **Типичный размер:**
   - X25519 + EdDSA с Key Certificate (сертификатом ключа) = 391 байт
   - 32 байта публичного ключа X25519
   - 320 байт заполнения (сжимаемого согласно [Proposal 161](/ru/proposals/161-ri-dest-padding/))
   - 32 байта публичного ключа EdDSA
   - 7 байт сертификата (3-байтовый заголовок + 4 байта типов ключей)

**Историческое развитие:** - До 0.9.16: Всегда NULL certificate (нулевой сертификат, тип 0) (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: Добавлена поддержка Key Certificate (сертификата ключа) - 0.9.48+: Поддерживаются ключи шифрования X25519 - 0.9.58+: ElGamal и DSA_SHA1 объявлены устаревшими

**Ключ netDb:** - RouterInfo индексируется по SHA-256-хешу полной RouterIdentity - Хеш вычисляется по всей структуре размером 391+ байт (включая padding (заполнение))

**См. также:** - Рекомендации по генерации заполнения ([Proposal 161](/ru/proposals/161-ri-dest-padding/)) - Спецификация Key Certificate (сертификата ключа) выше

**Документация Javadoc:** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Destination (адрес назначения в I2P)

**Описание:** Идентификатор конечной точки для безопасной доставки сообщений. Структурно идентичен структуре KeysAndCert (ключи и сертификат), но с иной семантикой использования.

**Формат:** См. структуру KeysAndCert выше

**Критическое отличие от RouterIdentity (идентификатора маршрутизатора):** - **Поле открытого ключа НЕ ИСПОЛЬЗУЕТСЯ и может содержать случайные данные** - Это поле не используется начиная с версии 0.6 (2005) - Изначально предназначалось для старого шифрования I2CP-to-I2CP (отключено) - В настоящее время используется только как инициализационный вектор для устаревшего шифрования LeaseSet

**Текущие рекомендации:**

1. **Ключ подписи:**
   - **Рекомендуется:** EdDSA_SHA512_Ed25519 (тип 7, 32 байта)
   - Альтернатива: типы ECDSA для совместимости со старыми версиями
   - Избегайте: DSA_SHA1 (устарело, не рекомендуется)

2. **Ключ шифрования:**
   - Поле не используется, но должно присутствовать
   - **Рекомендуется:** заполнить случайными данными в соответствии с [Предложением 161](/ru/proposals/161-ri-dest-padding/) (сжимаемыми)
   - Размер: Всегда 256 байт (слот ElGamal, хотя не используется для ElGamal)

3. **Сертификат:**
   - NULL certificate (нулевой сертификат) для ElGamal + DSA_SHA1 (только для устаревшего варианта)
   - Key Certificate (сертификат ключа) для всех остальных типов ключей подписи

**Типичное современное назначение:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Фактический ключ шифрования:** - Ключ шифрования для Destination (адресата в I2P) находится в **LeaseSet**, а не в Destination - LeaseSet содержит текущие открытые ключи шифрования - См. спецификацию LeaseSet2 по обработке ключей шифрования

**Ключ сетевой базы данных:** - LeaseSet индексируется по хешу SHA-256 от полного Destination (идентификатора назначения в I2P) - Хеш вычисляется по полной структуре размером 387+ байт

**JavaDoc:** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Структуры сетевой базы данных

### Lease (запись с информацией о входном туннеле и сроке действия)

**Описание:** Авторизует конкретный tunnel на приём сообщений для Destination (идентификатор назначения в I2P). Часть исходного формата LeaseSet (тип 1).

**Формат:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Общий размер:** 44 байта

**Использование:** - Используется только в оригинальном LeaseSet (тип 1, устаревший) - Для LeaseSet2 и более поздних вариантов вместо этого используйте Lease2

**Документация JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Тип 1)

**Описание:** Исходный формат LeaseSet. Содержит разрешённые tunnels и ключи для Destination (адрес назначения в I2P). Хранится в базе данных сети (netDb). **Статус: Устарело** (вместо этого используйте LeaseSet2).

**Структура:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Хранение базы данных:** - **Тип базы данных:** 1 - **Ключ:** хеш SHA-256 от Destination (идентификатор назначения) - **Значение:** полная структура LeaseSet

**Важные примечания:**

1. **Открытый ключ Destination (идентификатор назначения в I2P) не используется:**
   - Поле открытого ключа шифрования в Destination не используется
   - Ключ шифрования в LeaseSet является фактическим ключом шифрования

2. **Временные ключи:**
   - `encryption_key` временный (генерируется заново при запуске router)
   - `signing_key` временный (генерируется заново при запуске router)
   - Ни один из ключей не сохраняется между перезапусками

3. **Отзыв (не реализовано):**
   - `signing_key` предназначался для отзыва LeaseSet
   - Механизм отзыва так и не был реализован
   - LeaseSet с нулевым числом записей был задуман для отзыва, но не используется

4. **Версионирование/Временная метка:**
   - В LeaseSet нет явного поля метки времени `published`
   - Версия — это самый ранний срок истечения всех leases (элементов LeaseSet с указанием шлюза tunnel и времени истечения)
   - Новый LeaseSet принимается только если срок истечения lease более ранний

5. **Публикация сроков действия lease (запись в leaseSet):**
   - До 0.9.7: Все lease публиковались с одинаковым сроком действия (самым ранним)
   - С 0.9.7+: Публикуются фактические сроки действия отдельных lease
   - Это деталь реализации, не часть спецификации

6. **Нулевое количество leases:**
   - LeaseSet с нулём leases технически допустим
   - Предназначен для отзыва (не реализовано)
   - На практике не используется
   - Варианты LeaseSet2 требуют как минимум один Lease (арендная запись в I2P)

**Устарело:** LeaseSet типа 1 устарел. Новые реализации должны использовать **LeaseSet2 (тип 3)**, который обеспечивает: - Поле метки времени публикации (лучшее версионирование) - Поддержку нескольких ключей шифрования - Возможность офлайн-подписи - 4-байтовые сроки истечения элементов LeaseSet (вместо 8-байтовых) - Более гибкие параметры

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Варианты LeaseSet

### Lease2 (вторая версия записи Lease в составе LeaseSet)

**Описание:** Улучшенный формат Lease (элемент LeaseSet) с 4-байтовым сроком действия. Используется в LeaseSet2 (тип 3) и MetaLeaseSet (тип 7).

**Введение:** Версия 0.9.38 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Формат:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Общий размер:** 40 байт (на 4 байта меньше, чем исходный Lease (запись в leaseSet))

**Сравнение с исходным Lease (элементом leaseSet с параметрами входящего tunnel):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**Документация JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### Офлайновая подпись

**Описание:** Необязательная структура для предварительно подписанных временных ключей, позволяющая публиковать LeaseSet без онлайн-доступа к закрытому ключу подписи Destination (криптографическая идентичность/адрес в I2P).

**Введение:** Версия 0.9.38 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Формат:**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Назначение:** - Позволяет создавать LeaseSet офлайн - Защищает основной ключ назначения от онлайн-раскрытия - Временный ключ может быть отозван путём публикации нового LeaseSet без офлайн-подписи

**Сценарии использования:**

1. **Назначения повышенной безопасности:**
   - Мастер-ключ подписи хранится офлайн (HSM (аппаратный модуль безопасности), холодное хранение)
   - Временные ключи генерируются офлайн на ограничённые промежутки времени
   - Скомпрометированный временный ключ не раскрывает мастер-ключ

2. **Публикация зашифрованного LeaseSet:**
   - EncryptedLeaseSet может включать офлайн-подпись
   - Ослеплённый публичный ключ + офлайн-подпись обеспечивают дополнительную безопасность

**Соображения безопасности:**

1. **Управление сроком действия:**
   - Устанавливайте разумный срок действия (от нескольких дней до нескольких недель, а не лет)
   - Генерируйте новые временные ключи до истечения срока действия
   - Более короткий срок действия = выше безопасность, больше обслуживания

2. **Генерация ключей:**
   - Генерируйте временные ключи офлайн в защищённой среде
   - Подпишите их мастер-ключом офлайн
   - Передайте на онлайн router только подписанный временный ключ + подпись

3. **Отзыв:**
   - Опубликовать новый LeaseSet без офлайн-подписи для неявного отзыва
   - Или опубликовать новый LeaseSet с другим временным ключом

**Проверка подписи:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Примечания по реализации:** - Общий размер зависит от sigtype и типа ключа подписи Destination (идентификатора получателя в I2P) - Минимальный размер: 4 + 2 + 32 (ключ EdDSA) + 64 (подпись EdDSA) = 102 байта - Максимальный практический размер: ~600 байт (временный ключ RSA-4096 + подпись RSA-4096)

**Совместимо с:** - LeaseSet2 (тип 3) - EncryptedLeaseSet (тип 5) - MetaLeaseSet (тип 7)

**См. также:** [Предложение 123](/proposals/123-new-netdb-entries/) с подробным описанием протокола офлайн-подписи.

---

### LeaseSet2Header

**Описание:** Общая структура заголовка для LeaseSet2 (тип 3) и MetaLeaseSet (тип 7).

**Введение:** Версия 0.9.38 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Формат:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Минимальный общий размер:** 395 байт (без офлайн-подписи)

**Определения флагов (порядок битов: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Подробности флага:**

**Бит 0 - Offline Keys (офлайн-ключи):** - `0`: Нет офлайновой подписи, используется ключ подписи Destination (идентификатор назначения в I2P) для проверки подписи LeaseSet - `1`: Структура OfflineSignature (офлайновой подписи) следует сразу после поля flags

**Бит 1 - Неопубликовано:** - `0`: Стандартный опубликованный LeaseSet, должен быть распространён на floodfills - `1`: Неопубликованный LeaseSet (только на стороне клиента)   - НЕ должен распространяться, публиковаться или отправляться в ответ на запросы   - Если истёк срок действия, НЕ запрашивать в netdb замену (если также установлен бит 2)   - Используется для локальных tunnels или тестирования

**Бит 2 - Blinded (ослепление) (начиная с 0.9.42):** - `0`: Стандартный LeaseSet - `1`: Этот нешифрованный LeaseSet будет ослеплён и зашифрован при публикации   - Опубликованная версия будет EncryptedLeaseSet (тип 5)   - Если истёк срок действия, запросите **ослеплённое местоположение** в netdb для замены   - Также необходимо установить бит 1 в 1 (неопубликован + ослеплён)   - Используется для зашифрованных скрытых сервисов

**Ограничения срока действия:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Требования к временной метке публикации:**

LeaseSet (тип 1) не имел поля published, что для версионирования требовало поиска самого раннего истечения срока действия lease (запись о tunnel с временем истечения). LeaseSet2 добавляет явную метку времени `published` с точностью до одной секунды.

**Критически важное замечание по реализации:** - Routers ДОЛЖНЫ ограничивать частоту публикации LeaseSet до уровня **значительно реже, чем один раз в секунду** для каждого Destination - Если публикация происходит чаще, убедитесь, что каждый новый LeaseSet имеет время `published` как минимум на 1 секунду позже - Floodfills отклонят LeaseSet, если время `published` не новее текущей версии - Рекомендуемый минимальный интервал: 10-60 секунд между публикациями

**Примеры расчётов:**

**LeaseSet2 (максимум 11 минут):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (максимум 18,2 часа):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Версионирование:** - LeaseSet считается "более новым", если метка времени `published` больше - Floodfills хранят и распространяют только самую новую версию - Будьте внимательны, когда самый старый Lease (запись аренды туннеля) совпадает с самым старым Lease предыдущего LeaseSet

---

### LeaseSet2 (Тип 3)

**Описание:** Современный формат LeaseSet с несколькими ключами шифрования, офлайн-подписями и service records (записями сервиса). Текущий стандарт для скрытых сервисов I2P.

**Введение:** Версия 0.9.38 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Структура:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Хранилище базы данных:** - **Тип базы данных:** 3 - **Ключ:** хэш SHA-256 от назначения - **Значение:** Полная структура LeaseSet2

**Вычисление подписи:**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Порядок предпочтения ключей шифрования

**Для опубликованного (серверного) LeaseSet:** - Ключи перечислены в порядке предпочтений сервера (наиболее предпочтительные — первыми) - Клиенты, поддерживающие несколько типов, ДОЛЖНЫ соблюдать предпочтения сервера - Выберите первый поддерживаемый тип из списка - В общем случае типы ключей с более высоким номером (более новые) более безопасны/эффективны - Рекомендуемый порядок: перечисляйте ключи в обратном порядке по коду типа (новейшие первыми)

**Пример настройки сервера:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Для неопубликованного (клиентского) LeaseSet:** - Порядок ключей по сути не имеет значения (попытки соединения с клиентами редки) - Для единообразия придерживайтесь той же конвенции

**Выбор клиентского ключа:** - Учитывать предпочтение сервера (выбрать первый поддерживаемый тип) - Или использовать предпочтение, определённое реализацией - Или определить комбинированное предпочтение на основе возможностей обеих сторон

### Сопоставление параметров

**Требования:** - Параметры ДОЛЖНЫ быть отсортированы по ключу (лексикографический порядок, порядок байтов UTF-8) - Сортировка обеспечивает инвариантность подписи - Дублирующиеся ключи НЕ допускаются

**Стандартный формат ([Предложение 167](/proposals/167-service-records/)):**

Начиная с API 0.9.66 (июнь 2025, релиз 2.9.0), параметры сервисных записей соответствуют стандартизированному формату. См. [Proposal 167](/proposals/167-service-records/) для полной спецификации.

**Формат опции записи службы:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Примеры записей службы:**

**1. Самореферентный SMTP-сервер:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Один внешний SMTP-сервер:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Несколько SMTP-серверов (балансировка нагрузки):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Служба HTTP с параметрами приложения:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Рекомендации по TTL:** - Минимум: 86400 секунд (1 день) - Более длительный TTL снижает нагрузку на netdb от запросов - Баланс между сокращением числа запросов и распространением обновлений сервиса - Для стабильных сервисов: 604800 (7 дней) или дольше

**Примечания по реализации:**

1. **Ключи шифрования (по состоянию на 0.9.44):**
   - ElGamal (тип 0, 256 байт): совместимость со старыми версиями
   - X25519 (тип 4, 32 байта): текущий стандарт
   - Варианты MLKEM (Module-Lattice Key Encapsulation Mechanism — постквантовый механизм инкапсуляции ключей): постквантовые (бета, не финализированы)

2. **Проверка длины ключа:**
   - Floodfills и клиенты ДОЛЖНЫ уметь разбирать неизвестные типы ключей
   - Используйте поле keylen, чтобы пропускать неизвестные ключи
   - Не завершайте разбор с ошибкой, если тип ключа неизвестен

3. **Отметка времени публикации:**
   - См. примечания к LeaseSet2Header об ограничении частоты
   - Минимальный интервал между публикациями — 1 секунда
   - Рекомендуется: 10–60 секунд между публикациями

4. **Миграция типа шифрования:**
   - Поддержка нескольких ключей обеспечивает постепенную миграцию
   - Указывайте старые и новые ключи в переходный период
   - Удалите старый ключ после того, как пройдет достаточный период для обновления клиентов

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (метаданные Lease в I2P)

**Описание:** Структура Lease для MetaLeaseSet (вариант LeaseSet), способного ссылаться на другие LeaseSets вместо tunnels. Используется для балансировки нагрузки и избыточности.

**Введение:** Версия 0.9.38, запланировано к внедрению в 0.9.40 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Формат:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Общий размер:** 40 байт

**Тип записи (биты flags 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Сценарии использования:**

1. **Балансировка нагрузки:**
   - MetaLeaseSet (структура для балансировки, содержащая несколько записей MetaLease (мета-запись))
   - Каждая запись указывает на свой LeaseSet2 (расширенная версия LeaseSet в I2P)
   - Клиенты выбирают на основе поля cost

2. **Избыточность:**
   - Несколько записей, указывающих на резервные LeaseSets
   - Резервный вариант при недоступности основного LeaseSet

3. **Миграция сервиса:**
   - MetaLeaseSet (специальная структура, указывающая на LeaseSet в I2P) ссылается на новый LeaseSet
   - Обеспечивает плавный переход между Destinations (идентификаторами назначения в I2P)

**Использование поля Cost:** - Меньшее значение Cost = более высокий приоритет - Cost 0 = наивысший приоритет - Cost 255 = самый низкий приоритет - Клиенты ДОЛЖНЫ предпочитать записи с более низким значением Cost - Записи с одинаковым значением Cost могут балансироваться по нагрузке случайным образом

**Сравнение с Lease2:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Тип 7)

**Описание:** Вариант LeaseSet, содержащий записи MetaLease (тип записи, указывающей на другие LeaseSets), обеспечивающие косвенное обращение к другим LeaseSets. Используется для балансировки нагрузки, избыточности и миграции сервиса.

**Введение:** Определено в 0.9.38, запланировано к работе в 0.9.40 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Статус:** Спецификация завершена. Статус боевого развертывания следует проверить по текущим релизам I2P.

**Структура:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Хранилище базы данных:** - **Тип базы данных:** 7 - **Ключ:** SHA-256-хеш от Destination (идентификатор назначения в I2P) - **Значение:** Полная структура MetaLeaseSet (расширенная структура leaseSet)

**Вычисление подписи:**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Сценарии использования:**

**1. Балансировка нагрузки:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Аварийное переключение:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Миграция сервиса:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Многоуровневая архитектура:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Список отзыва:**

Список отзыва позволяет MetaLeaseSet (мета-структура LeaseSet) явно отзывать ранее опубликованные LeaseSets:

- **Назначение:** Пометить конкретные Destination (адрес назначения в I2P) как недействительными
- **Содержимое:** Хэши SHA-256 отозванных структур Destination
- **Использование:** Клиенты НЕ ДОЛЖНЫ использовать LeaseSets, хэш Destination которых присутствует в списке отзыва
- **Типичное значение:** Пусто (numr=0) в большинстве развёртываний

**Пример отзыва:**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Обработка истечения срока действия:**

MetaLeaseSet использует LeaseSet2Header с максимальным значением expires=65535 секунд (~18.2 часа):

- Гораздо дольше, чем LeaseSet2 (макс. ~11 минут)
- Подходит для относительно статической косвенной адресации
- LeaseSets, на которые ссылаются, могут иметь более короткий срок действия
- Клиенты должны проверять срок действия как MetaLeaseSet, так и LeaseSets, на которые он ссылается

**Сопоставление параметров:**

- Используйте тот же формат, что и у параметров LeaseSet2
- Может включать записи сервиса ([Предложение 167](/proposals/167-service-records/))
- ДОЛЖНЫ быть отсортированы по ключу
- Записи сервиса обычно описывают конечный сервис, а не структуру косвенной адресации

**Примечания по реализации клиента:**

1. **Процесс разрешения:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Кэширование:**
   - Кэшируйте как MetaLeaseSet, так и ссылочные LeaseSets
   - Проверяйте истечение срока действия на обоих уровнях
   - Отслеживайте публикацию обновлённого MetaLeaseSet

3. **Переключение при отказе (failover):**
   - Если предпочитаемая запись отказала, попробуйте запись со следующей наименьшей стоимостью
   - Рассмотрите возможность помечать отказавшие записи как временно недоступные
   - Периодически перепроверяйте на предмет восстановления

**Статус реализации:**

[Предложение 123](/proposals/123-new-netdb-entries/) отмечает, что некоторые разделы остаются «в разработке». Реализаторам следует: - Проверить готовность к промышленной эксплуатации в целевой версии I2P - Протестировать поддержку MetaLeaseSet (мета-тип записи leaseSet) перед развертыванием - Проверить наличие обновленных спецификаций в более новых релизах I2P

**Документация JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Тип 5)

**Описание:** Зашифрованный и ослеплённый LeaseSet для повышенной конфиденциальности. Видны только ослеплённый открытый ключ и метаданные; реальные leases (записи Lease) и ключи шифрования зашифрованы.

**Введение:** Определено в 0.9.38, работает в 0.9.39 (см. [Предложение 123](/proposals/123-new-netdb-entries/))

**Структура:**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Хранение в базе данных:** - **Тип базы данных:** 5 - **Ключ:** хеш SHA-256 от **ослеплённого Destination** (не исходного Destination — идентификатор сервиса в I2P) - **Значение:** Полная структура EncryptedLeaseSet

**Принципиальные отличия от LeaseSet2:**

1. **НЕ использует структуру LeaseSet2Header** (имеет схожие поля, но иной формат)
2. **Ослеплённый открытый ключ** вместо полного Destination (адрес назначения в I2P)
3. **Зашифрованная полезная нагрузка** вместо leases и ключей в открытом виде
4. **Ключ базы данных — хеш ослеплённого Destination, а не исходного Destination**

**Вычисление подписи:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Требование к типу подписи:**

**ОБЯЗАТЕЛЬНО использовать RedDSA_SHA512_Ed25519 (схема подписи RedDSA на Ed25519 с SHA-512; type 11):** - 32-байтные ослеплённые открытые ключи - 64-байтные подписи - Требуется для обеспечения свойств безопасности ослепления - См. [спецификацию Red25519](//docs/specs/red25519-signature-scheme/

**Ключевые отличия от EdDSA:** - Закрытые ключи получаются посредством модульного приведения (не clamping — фиксация некоторых битов) - Подписи включают 80 байт случайных данных - Напрямую используются открытые ключи (не хэши) - Обеспечивает безопасную операцию ослепления

**Ослепление и шифрование:**

Подробности см. в [спецификации EncryptedLeaseSet](/docs/specs/encryptedleaseset/):

**1. Ослепление ключа:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Расположение базы данных:**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Слои шифрования (трёхслойные):**

**Уровень 1 - слой аутентификации (доступ клиентов):** - Шифрование: поточный шифр ChaCha20 - Деривация ключей: HKDF с секретами для каждого клиента - Аутентифицированные клиенты могут расшифровать внешний слой

**Слой 2 - уровень шифрования:** - Шифрование: ChaCha20 - Ключ: выведен из DH (Диффи—Хеллман) между клиентом и сервером - Содержит сам LeaseSet2 или MetaLeaseSet

**Слой 3 - Внутренний LeaseSet (набор записей о входящих tunnels и ключах в I2P):** - Полный LeaseSet2 или MetaLeaseSet - Включает все tunnels, ключи шифрования, параметры - Доступен только после успешной расшифровки

**Выработка ключа шифрования:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Процесс обнаружения:**

**Для авторизованных клиентов:**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Для неавторизованных клиентов:** - Не могут расшифровать, даже если обнаружат EncryptedLeaseSet - Не могут определить исходный Destination (адрес назначения в I2P) из ослеплённой версии - Не могут сопоставить EncryptedLeaseSets между различными периодами ослепления (ежедневная ротация)

**Сроки действия:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Метка времени публикации:**

Те же требования, что и у LeaseSet2Header:
- Должно увеличиваться минимум на 1 секунду между публикациями
- Floodfills отклоняют, если не новее текущей версии
- Рекомендуется: 10–60 секунд между публикациями

**Подписи в автономном режиме с зашифрованными LeaseSets:**

Особые соображения при использовании офлайн-подписей: - Ослеплённый открытый ключ обновляется ежедневно - Офлайн-подпись должна ежедневно пересоздаваться с новым ослеплённым ключом - ИЛИ используйте офлайн-подпись во внутреннем LeaseSet (набор сведений для связи с сервисом в I2P), а не во внешнем EncryptedLeaseSet (зашифрованный LeaseSet) - См. примечания к [Предложению 123](/proposals/123-new-netdb-entries/)

**Примечания по реализации:**

1. **Авторизация клиентов:**
   - Можно авторизовать нескольких клиентов с разными ключами
   - У каждого авторизованного клиента есть уникальные учетные данные для расшифрования
   - Отозвать клиента можно, изменив ключи авторизации

2. **Ежедневная ротация ключей:**
   - Blinded keys (ослеплённые ключи) меняются в полночь по UTC
   - Клиенты должны ежедневно пересчитывать blinded Destination (адрес назначения в I2P)
   - Старые EncryptedLeaseSets (зашифрованные leaseSet в I2P) становятся недоступными для обнаружения после ротации

3. **Свойства конфиденциальности:**
   - Узлы floodfill не могут определить исходный Destination (идентификатор назначения в I2P)
   - Неавторизованные клиенты не могут получить доступ к сервису
   - Разные периоды blinding (ослепления) не могут быть связаны между собой
   - Отсутствуют метаданные в открытом виде, кроме сроков истечения

4. **Производительность:**
   - Клиенты должны выполнять ежедневное вычисление ослепления
   - Трёхслойное шифрование добавляет вычислительные накладные расходы
   - Рассмотрите кэширование расшифрованного внутреннего LeaseSet

**Соображения безопасности:**

1. **Управление ключами авторизации:**
   - Безопасно распространяйте клиентские учетные данные авторизации
   - Используйте уникальные учетные данные для каждого клиента для избирательного отзыва
   - Периодически обновляйте (ротируйте) ключи авторизации

2. **Синхронизация времени:**
   - Ежедневное blinding (ослепление) зависит от синхронизированных дат UTC
   - Смещение часов может приводить к ошибкам при поиске
   - Рассмотрите поддержку blinding за предыдущий/следующий день для повышения устойчивости к смещению часов

3. **Утечка метаданных:**
   - Поля Published и expires передаются в открытом виде
   - Анализ закономерностей может раскрыть характеристики сервиса
   - Если есть опасения, варьируйте интервалы публикации случайным образом

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Структуры Router

### RouterAddress (адрес Router)

**Описание:** Определяет информацию о подключении для router по конкретному транспортному протоколу.

**Формат:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**КРИТИЧЕСКОЕ - Поле срока действия:**

⚠️ **Поле срока действия ДОЛЖНО быть установлено во все нули (8 нулевых байт).**

- **Причина:** Начиная с версии 0.9.3, ненулевое значение Expiration (поле срока действия) приводит к сбою проверки подписи
- **История:** Expiration изначально не использовалось, всегда было null
- **Текущее состояние:** Поле снова стало распознаваться начиная с 0.9.12, но требуется дождаться обновления сети
- **Реализация:** Всегда устанавливается в 0x0000000000000000

Любое ненулевое значение срока действия приведёт к тому, что подпись RouterInfo не пройдёт проверку.

### Транспортные протоколы

**Текущие протоколы (по состоянию на 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Значения стиля транспорта:** - `"SSU2"`: Текущий транспорт на основе UDP - `"NTCP2"`: Текущий транспорт на основе TCP - `"NTCP"`: Устаревший, удалён (не использовать) - `"SSU"`: Устаревший, удалён (не использовать)

### Общие параметры

Все транспорты обычно включают:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Специфические для SSU2 параметры

См. [спецификацию SSU2](/docs/specs/ssu2/) для получения полной информации.

**Обязательные параметры:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Необязательные параметры:**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Пример SSU2 RouterAddress:**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Специфические параметры NTCP2

См. [спецификацию NTCP2](/docs/specs/ntcp2/) для получения полных сведений.

**Обязательные параметры:**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Необязательные параметры (начиная с 0.9.50):**

```
"caps" = Capability string
```
**Пример NTCP2 RouterAddress (адрес маршрутизатора):**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Примечания по реализации

1. **Значения стоимости:**
   - UDP (SSU2) обычно имеет более низкую стоимость (5-6) благодаря эффективности
   - TCP (NTCP2) обычно имеет более высокую стоимость (10-11) из-за накладных расходов
   - Более низкая стоимость = предпочитаемый транспорт

2. **Несколько адресов:**
   - Routers могут публиковать несколько записей RouterAddress
   - Разные транспорты (SSU2 и NTCP2)
   - Разные версии IP (IPv4 и IPv6)
   - Клиенты выбирают на основе стоимости и возможностей

3. **Имя хоста против IP:**
   - IP‑адреса предпочтительнее с точки зрения производительности
   - Имена хостов поддерживаются, но добавляют накладные расходы на разрешение DNS
   - Рассмотрите использование IP для публикуемых RouterInfos (объекты RouterInfo)

4. **Кодирование Base64:**
   - Все ключи и двоичные данные кодируются в Base64
   - Стандартный Base64 (RFC 4648)
   - Без padding (заполнения) и нестандартных символов

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**Описание:** Полная опубликованная информация о router, хранящаяся в сетевой базе данных. Содержит идентификатор, адреса и возможности.

**Формат:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Хранение в базе данных:** - **Тип базы данных:** 0 - **Ключ:** SHA-256-хеш от RouterIdentity - **Значение:** Полная структура RouterInfo

**Метка времени публикации:** - 8-байтная дата (миллисекунды с начала эпохи) - Используется для версионирования RouterInfo - Routers периодически публикуют новый RouterInfo - Floodfills сохраняют самую новую версию на основе опубликованной метки времени

**Сортировка адресов:** - **Исторически:** Очень старые routers требовали, чтобы адреса были отсортированы по значению SHA-256 их данных - **Текущее:** Сортировка НЕ требуется, реализовывать ради совместимости не имеет смысла - Адреса могут быть в любом порядке

**Поле размера пиров (историческое):** - **Всегда 0** в современной I2P - Предназначалось для ограниченных маршрутов (не реализовано) - При реализации за ним следовало бы соответствующее количество хэшей Router - В некоторых старых реализациях мог требоваться отсортированный список пиров

**Сопоставление параметров:**

Параметры ДОЛЖНЫ быть отсортированы по ключу. Стандартные параметры включают:

**Параметры возможностей:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Параметры сети:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Параметры статистики:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
См. [документацию по RouterInfo базы данных сети](/docs/specs/common-structures/#routerInfo) для полного списка стандартных параметров.

**Вычисление подписи:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**Типичный современный RouterInfo (информация о router):**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Примечания по реализации:**

1. **Несколько адресов:**
   - Routers обычно публикуют 1-4 адреса
   - Варианты IPv4 и IPv6
   - Транспорты SSU2 и/или NTCP2
   - Каждый адрес независим

2. **Версионирование:**
   - Более новая RouterInfo имеет более позднюю метку времени `published`
   - Routers публикуют заново каждые ~2 часа или при изменении адресов
   - Floodfills хранят и распространяют только самую новую версию

3. **Валидация:**
   - Проверьте подпись перед принятием RouterInfo (структура данных с информацией о router)
   - Проверьте, что поле expiration состоит из одних нулей в каждом RouterAddress (сетевой адрес router)
   - Проверьте, что отображение options отсортировано по ключу
   - Проверьте, что типы сертификата и ключа известны/поддерживаются

4. **Сетевая база данных:**
   - Floodfills хранят RouterInfo, индексированный по Hash(RouterIdentity)
   - Данные хранятся ~2 дня после последней публикации
   - Routers запрашивают floodfills, чтобы обнаружить другие routers

**Документация JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Примечания по реализации

### Порядок байтов (эндианность)

**По умолчанию: Big-Endian (сетевой порядок байтов)**

Большинство структур I2P используют порядок байтов big-endian (старший байт первым): - Все целочисленные типы (1-8 байт) - Метки времени - TunnelId - Префикс длины строки - Типы и длины сертификатов - Коды типов ключей - Поля размера сопоставления

**Исключение: Little-Endian (младший порядок байтов)**

Следующие типы ключей используют кодирование в формате **little-endian**: - **X25519** ключи шифрования (тип 4) - **EdDSA_SHA512_Ed25519** ключи подписи (тип 7) - **EdDSA_SHA512_Ed25519ph** ключи подписи (тип 8) - **RedDSA_SHA512_Ed25519** ключи подписи (тип 11)

**Реализация:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Версионирование структуры

**Никогда не полагайтесь на фиксированные размеры:**

Многие структуры имеют переменную длину: - RouterIdentity: 387+ байт (не всегда 387) - Destination: 387+ байт (не всегда 387) - LeaseSet2: значительно варьируется - Certificate: 3+ байт

**Всегда считывайте поля размеров:** - Длина сертификата в байтах 1-2 - Размер сопоставления в начале - KeysAndCert всегда вычисляется как 384 + 3 + certificate_length

**Проверка на лишние данные:** - Запретить лишние байты в конце после корректных структур - Проверять, что длины сертификатов соответствуют типам ключей - Требовать строгого соответствия ожидаемым длинам для типов фиксированного размера

### Актуальные рекомендации (октябрь 2025 года)

**Для новых идентичностей router:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ru/proposals/161-ri-dest-padding/)
```
**Для новых назначений:**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/ru/proposals/161-ri-dest-padding/)
```
**Для новых LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Для зашифрованных сервисов:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Устаревшие функции - не использовать

**Устаревшее шифрование:** - ElGamal (тип 0) для идентичностей Router (устарело в 0.9.58) - шифрование ElGamal/AES+SessionTag (используйте ECIES-X25519)

**Устаревшие типы подписи:** - DSA_SHA1 (тип 0) для идентификаторов Router (устарело в 0.9.58) - варианты ECDSA (типы 1-3) для новых реализаций - варианты RSA (типы 4-6) за исключением файлов SU3

**Устаревшие сетевые форматы:** - LeaseSet тип 1 (используйте LeaseSet2) - Lease (запись в LeaseSet; 44 байта, используйте Lease2) - Оригинальный формат истечения срока действия Lease

**Устаревшие транспорты:** - NTCP (удалён в 0.9.50) - SSU (удалён в 2.4.0)

**Устаревшие сертификаты:** - HASHCASH (тип 1) - HIDDEN (тип 2) - SIGNED (тип 3) - MULTIPLE (тип 4)

### Соображения безопасности

**Генерация ключей:** - Всегда используйте криптографически стойкие генераторы случайных чисел - Никогда не используйте повторно ключи в разных контекстах - Защищайте закрытые ключи соответствующими мерами контроля доступа - Надёжно стирайте ключевой материал из памяти по завершении работы

**Проверка подписи:** - Всегда проверяйте подписи, прежде чем доверять данным - Проверяйте, что длина подписи соответствует типу ключа - Проверяйте, что подписанные данные содержат ожидаемые поля - Для отсортированных отображений проверяйте порядок сортировки перед подписанием/проверкой

**Проверка временных меток:** - Проверить, что опубликованные времена разумны (не в далёком будущем) - Убедиться, что сроки действия lease (временная запись о доступности tunnel) не истекли - Учитывать допуск расхождения часов (обычно ±30 секунд)

**netDb (сетевая база данных):** - Проверять все структуры перед сохранением - Применять ограничения размера для предотвращения DoS-атак - Ограничивать частоту запросов и публикаций - Проверять, что ключи базы данных соответствуют хэшам структур

### Примечания по совместимости

**Обратная совместимость:** - ElGamal и DSA_SHA1 по-прежнему поддерживаются для устаревших routers - Типы ключей, помеченные как устаревшие, остаются работоспособными, но их использование не рекомендуется - Сжимаемый padding (выравнивающая вставка) ([Proposal 161](/ru/proposals/161-ri-dest-padding/)) обратно совместим вплоть до 0.6

**Совместимость с будущими версиями:** - Неизвестные типы ключей можно разбирать, используя поля длины - Неизвестные типы сертификатов можно пропускать, используя поле длины - Неизвестные типы подписей следует обрабатывать корректно - Реализации не должны аварийно завершаться при столкновении с неизвестными необязательными функциями

**Стратегии миграции:** - Поддержка одновременно старых и новых типов ключей на время перехода - LeaseSet2 может содержать несколько ключей шифрования - Офлайн-подписи обеспечивают безопасную ротацию ключей - MetaLeaseSet обеспечивает прозрачную миграцию сервиса

### Тестирование и валидация

**Проверка структуры:** - Проверьте, что все поля длины находятся в ожидаемых диапазонах - Проверьте, что структуры переменной длины корректно разбираются - Проверьте, что подписи успешно проходят проверку - Протестируйте со структурами минимального и максимального размера

**Пограничные случаи:** - Строки нулевой длины - Пустые отображения - Минимальное и максимальное число lease (записей в LeaseSet) - Сертификат с нулевой длиной полезной нагрузки - Очень крупные структуры (близкие к максимальным размерам)

**Совместимость:** - Тестировать на соответствие официальной реализации Java I2P - Проверять совместимость с i2pd - Тестировать с различным содержимым сетевой базы данных - Проверять на соответствие известным корректным тестовым векторам

---

## Ссылки

### Спецификации

- [Протокол I2NP](/docs/specs/i2np/)
- [Протокол I2CP](/docs/specs/i2cp/)
- [Транспорт SSU2](/docs/specs/ssu2/)
- [Транспорт NTCP2](/docs/specs/ntcp2/)
- [Протокол Tunnel](/docs/specs/implementation/)
- [Протокол датаграмм](/docs/api/datagrams/)

### Криптография

- [Обзор криптографии](/docs/specs/cryptography/)
- [Шифрование ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Шифрование ECIES-X25519](/docs/specs/ecies/)
- [ECIES для Routers](/docs/specs/ecies/#routers)
- [Гибридный ECIES (постквантовый)](/docs/specs/ecies/#hybrid)
- [Подписи Red25519](/docs/specs/red25519-signature-scheme/)
- [Зашифрованный LeaseSet](/docs/specs/encryptedleaseset/)

### Предложения

- [Предложение 123: Новые записи netDB](/proposals/123-new-netdb-entries/)
- [Предложение 134: Типы подписей ГОСТ](/proposals/134-gost/)
- [Предложение 136: Экспериментальные типы подписей](/proposals/136-experimental-sigtypes/)
- [Предложение 145: ECIES-P256](/proposals/145-ecies/)
- [Предложение 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Предложение 161: Генерация паддинга](/ru/proposals/161-ri-dest-padding/)
- [Предложение 167: Сервисные записи](/proposals/167-service-records/)
- [Предложение 169: Постквантовая криптография](/proposals/169-pq-crypto/)
- [Индекс всех предложений](/proposals/)

### Сетевая база данных

- [Обзор базы данных сети](/docs/specs/common-structures/)
- [Стандартные параметры RouterInfo](/docs/specs/common-structures/#routerInfo)

### Справочник по API JavaDoc

- [Базовый пакет данных](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Внешние стандарты

- **RFC 7748 (X25519):** Эллиптические кривые для обеспечения безопасности
- **RFC 7539 (ChaCha20):** ChaCha20 и Poly1305 для протоколов IETF
- **RFC 4648 (Base64):** Кодировки данных Base16, Base32 и Base64
- **FIPS 180-4 (SHA-256):** Стандарт безопасного хэширования
- **FIPS 204 (ML-DSA):** Стандарт цифровой подписи на основе модульных решёток
- [Реестр служб IANA](http://www.dns-sd.org/ServiceTypes.html)

### Ресурсы сообщества

- [Сайт I2P](/)
- [Форум I2P](https://i2pforum.net)
- [GitLab I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Зеркало I2P на GitHub](https://github.com/i2p/i2p.i2p)
- [Индекс технической документации](/docs/)

### Информация о выпуске

- [Релиз I2P 2.10.0](/ru/blog/2025/09/08/i2p-2.10.0-release/)
- [История релизов](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Журнал изменений](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Приложение: краткие справочные таблицы

### Краткая справка по типам ключей

**Текущий стандарт (рекомендуется для всех новых реализаций):** - **Шифрование:** X25519 (тип 4, 32 байта, little-endian) - **Подпись:** EdDSA_SHA512_Ed25519 (тип 7, 32 байта, little-endian)

**Устаревшее (поддерживается, но признано устаревшим):** - **Шифрование:** ElGamal (тип 0, 256 байт, big-endian (порядок от старшего байта к младшему)) - **Подписание:** DSA_SHA1 (тип 0, 20-байтовый закрытый / 128-байтовый открытый, big-endian)

**Специализированные:** - **Подпись (зашифрованный LeaseSet):** RedDSA_SHA512_Ed25519 (тип 11, 32 байта, little-endian)

**Постквантовое (бета, не финализировано):** - **Гибридное шифрование:** варианты MLKEM_X25519 (типы 5-7) - **Чисто постквантовое шифрование:** варианты MLKEM (коды типов еще не назначены)

### Краткий справочник по размерам структур

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Краткая справка по типу базы данных

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Краткая справка по транспортному протоколу

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Краткая справка по вехам версий

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/ru/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
