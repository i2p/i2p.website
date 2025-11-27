---
title: "Новые записи netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Открыть"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Статус

Части данного предложения завершены и реализованы в версиях 0.9.38 и 0.9.39. Спецификации Common Structures, I2CP, I2NP и другие теперь обновлены, чтобы отражать изменения, которые поддерживаются в настоящее время.

Завершенные части всё ещё могут подвергаться незначительным изменениям. Другие части данного предложения всё ещё находятся в разработке и могут подвергаться существенным изменениям.

Service Lookup (типы 9 и 11) имеют низкий приоритет и не планируются, и могут быть выделены в отдельное предложение.

## Обзор

Это обновление и объединение следующих 4 предложений:

- 110 LS2
- 120 Meta LS2 для массивного мультихоминга
- 121 Зашифрованный LS2
- 122 Неаутентифицированный поиск сервиса (анкастинг)

Эти предложения в основном независимы, но для разумности мы определяем и используем общий формат для нескольких из них.

Следующие предложения в некоторой степени связаны:

- 140 Невидимый мультихоминг (несовместим с данным предложением)
- 142 Новый криптографический шаблон (для новой симметричной криптографии)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 для зашифрованных LS2
- 150 Протокол Garlic Farm
- 151 Слепая подпись ECDSA

## Предложение

Данное предложение определяет 5 новых типов DatabaseEntry и процесс их хранения в сетевой базе данных и извлечения из неё, а также метод их подписания и проверки этих подписей.

### Goals

- Обратная совместимость
- LS2 совместим со старым стилем multihoming
- Не требуется новая криптография или примитивы для поддержки
- Сохраняет разделение криптографии и подписи; поддерживает все текущие и будущие версии
- Включает опциональные offline ключи подписи
- Снижает точность временных меток для уменьшения fingerprinting
- Включает новую криптографию для destination'ов
- Включает массивный multihoming
- Исправляет множественные проблемы с существующими зашифрованными LS
- Опциональное blinding для снижения видимости со стороны floodfill'ов
- Зашифрованные поддерживают как однокнопочные, так и множественные отзывные ключи
- Service lookup для упрощения поиска outproxy, bootstrap DHT приложений,
  и других применений
- Не нарушает ничего, что зависит от 32-байтных бинарных хешей destination'ов, например bittorrent
- Добавляет гибкость к leaseSet'ам через свойства, как у нас есть в routerinfo
- Помещает опубликованную временную метку и переменное время истечения в заголовок, чтобы это работало даже
  если содержимое зашифровано (не выводить временную метку из самого раннего lease)
- Все новые типы находятся в том же DHT пространстве и тех же местах, что и существующие leaseSet'ы,
  чтобы пользователи могли мигрировать со старого LS на LS2,
  или переключаться между LS2, Meta и Encrypted,
  без изменения Destination или хеша.
- Существующий Destination может быть преобразован для использования offline ключей,
  или обратно к online ключам, без изменения Destination или хеша.

### Non-Goals / Out-of-scope

- Новый алгоритм ротации DHT или генерация общего случайного числа
- Конкретный новый тип шифрования и схема сквозного шифрования
  для использования этого нового типа будут в отдельном предложении.
  Никакой новой криптографии здесь не указано или не обсуждается.
- Новое шифрование для RI или построения tunnel.
  Это будет в отдельном предложении.
- Методы шифрования, передачи и приема I2NP DLM / DSM / DSRM сообщений.
  Не изменяются.
- Как генерировать и поддерживать Meta, включая межмаршрутизаторную связь backend, управление, переключение при отказах и координацию.
  Поддержка может быть добавлена в I2CP, или i2pcontrol, или новый протокол.
  Это может быть стандартизировано или нет.
- Как фактически реализовать и управлять tunnel с более длительным сроком действия, или отменять существующие tunnel.
  Это крайне сложно, и без этого невозможно корректно завершить работу.
- Изменения модели угроз
- Формат офлайн-хранения или методы для хранения/извлечения/совместного использования данных.
- Детали реализации здесь не обсуждаются и оставляются на усмотрение каждого проекта.

### Justification

LS2 добавляет поля для изменения типа шифрования и для будущих изменений протокола.

Зашифрованный LS2 исправляет несколько проблем безопасности существующего зашифрованного LS, используя асимметричное шифрование всего набора leases.

Meta LS2 обеспечивает гибкое, эффективное, действенное и крупномасштабное мультихоминг.

Service Record и Service List предоставляют anycast-сервисы, такие как поиск имен и начальная загрузка DHT.

### Цели

Номера типов используются в I2NP сообщениях Database Lookup/Store.

Столбец end-to-end указывает, отправляются ли запросы/ответы к Destination в Garlic Message.

Существующие типы:

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Новые типы:

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Не-цели / Вне области применения

- Типы поиска в настоящее время находятся в битах 3-2 в сообщении Database Lookup Message.
  Любые дополнительные типы потребуют использования бита 4.

- Все типы хранилищ являются нечетными, поскольку старшие биты в поле типа Database Store Message игнорируются старыми роутерами.
  Мы предпочли бы, чтобы парсинг завершался неудачей как LS, а не как сжатый RI.

- Должен ли тип быть явным или неявным, или ни тем, ни другим в данных, покрываемых подписью?

### Обоснование

Типы 3, 5 и 7 могут быть возвращены в ответ на стандартный поиск leaseset (тип 1). Тип 9 никогда не возвращается в ответ на поиск. Тип 11 возвращается в ответ на новый тип поиска службы (тип 11).

Только тип 3 может быть отправлен в Garlic сообщении клиент-клиент.

### Типы данных NetDB

Типы 3, 7 и 9 имеют общий формат::

Стандартный заголовок LS2   - как определено ниже

Специфичная для типа часть   - как определено ниже в каждой части

Стандартная подпись LS2:   - Длина определяется типом подписи ключа подписания

Тип 5 (Зашифрованный) не начинается с Destination и имеет другой формат. См. ниже.

Тип 11 (Список сервисов) является агрегацией нескольких записей сервисов и имеет другой формат. См. ниже.

### Примечания

I notice that the text you provided is "TBD" (To Be Determined), which is typically a placeholder indicating that content hasn't been written yet. Since this is not actual content to translate, I'll return it as-is:

TBD

## Standard LS2 Header

Типы 3, 7 и 9 используют стандартный заголовок LS2, описанный ниже:

### Процесс поиска/сохранения

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Формат

- Unpublished/published: Для использования при отправке database store от конца до конца,
  отправляющий router может захотеть указать, что этот leaseset не должен быть
  отправлен другим. В настоящее время мы используем эвристику для поддержания этого состояния.

- Published: Заменяет сложную логику, необходимую для определения 'версии' 
  leaseset. В настоящее время версия является временем истечения последнего истекающего lease,
  и публикующий router должен увеличить это время истечения минимум на 1мс при
  публикации leaseset, который только удаляет более старый lease.

- Expires: Позволяет установить срок истечения записи netDb раньше, чем у её последнего истекающего leaseSet. Может быть не полезно для LS2, где leaseSet'ы ожидаются с максимальным сроком истечения в 11 минут, но для других новых типов это необходимо (см. Meta LS и Service Record ниже).

- Офлайн-ключи являются опциональными, чтобы снизить первоначальную/требуемую сложность реализации.

### Соображения конфиденциальности/безопасности

- Можно было бы ещё больше снизить точность timestamp (до 10 минут?), но пришлось бы добавить номер версии. Это могло бы нарушить multihoming, если только у нас нет шифрования с сохранением порядка? Вероятно, совсем без timestamp обойтись нельзя.

- Альтернатива: 3-байтовая временная метка (эпоха / 10 минут), 1-байтовая версия, 2-байтовый срок истечения

- Является ли тип явным или неявным в данных / подписи? Константы "Domain" для подписи?

### Notes

- Роутеры не должны публиковать leaseSet чаще одного раза в секунду.
  Если это происходит, они должны искусственно увеличить временную метку публикации на 1
  по сравнению с ранее опубликованным leaseSet.

- Реализации router могут кэшировать временные ключи и подпись, чтобы
  избежать верификации каждый раз. В частности, floodfill и router на
  обоих концах долгосрочных соединений могут получить выгоду от этого.

- Офлайн-ключи и подписи подходят только для долгоживущих destinations,
  т.е. серверов, а не клиентов.

## New DatabaseEntry types

### Формат

Изменения по сравнению с существующим LeaseSet:

- Добавить временную метку публикации, временную метку истечения, флаги и свойства
- Добавить тип шифрования
- Удалить ключ отзыва

Поиск с помощью

    Standard LS flag (1)
Сохранить с

    Standard LS2 type (3)
Хранить в

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Типичное истечение срока действия

    10 minutes, as in a regular LS.
Опубликовано

    Destination

### Обоснование

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Проблемы

- Properties: Будущее расширение и гибкость.
  Размещается первым на случай, если это необходимо для парсинга оставшихся данных.

- Множественные пары типов шифрования/открытых ключей предназначены
  для облегчения перехода к новым типам шифрования. Другой способ сделать это —
  опубликовать множественные leaseSet, возможно используя те же туннели,
  как мы делаем сейчас для DSA и EdDSA назначений.
  Идентификация входящего типа шифрования в туннеле
  может быть выполнена с помощью существующего механизма session tag,
  и/или пробной расшифровки с использованием каждого ключа. Длины входящих
  сообщений также могут предоставить подсказку.

### Примечания

Данное предложение продолжает использовать публичный ключ в leaseset для ключа сквозного шифрования и оставляет поле публичного ключа в Destination неиспользуемым, как это происходит сейчас. Тип шифрования не указывается в сертификате ключа Destination, он останется равным 0.

Отклоненной альтернативой является указание типа шифрования в сертификате ключа Destination, использование публичного ключа в Destination и неиспользование публичного ключа в leaseset. Мы не планируем этого делать.

Преимущества LS2:

- Расположение фактического публичного ключа не изменяется.
- Тип шифрования или публичный ключ могут изменяться без изменения Destination.
- Удаляет неиспользуемое поле отзыва
- Базовая совместимость с другими типами DatabaseEntry в данном предложении
- Позволяет использовать несколько типов шифрования

Недостатки LS2:

- Расположение открытого ключа и тип шифрования отличается от RouterInfo
- Сохраняет неиспользуемый открытый ключ в leaseset
- Требует реализации по всей сети; в качестве альтернативы могут использоваться экспериментальные
  типы шифрования, если это разрешено floodfill-узлами
  (но см. связанные предложения 136 и 137 о поддержке экспериментальных типов подписей).
  Альтернативное предложение может быть проще для реализации и тестирования экспериментальных типов шифрования.

### New Encryption Issues

Часть этого выходит за рамки данного предложения, но пока размещаем заметки здесь, поскольку у нас пока нет отдельного предложения по шифрованию. См. также предложения ECIES 144 и 145.

- Тип шифрования представляет комбинацию
  кривой, длины ключа и сквозной схемы,
  включая KDF и MAC, если они есть.

- Мы включили поле длины ключа, чтобы LS2 можно было
  парсить и верифицировать floodfill'ом даже для неизвестных типов шифрования.

- Первым новым типом шифрования, который будет предложен,
  вероятно, станет ECIES/X25519. Как он будет использоваться end-to-end
  (либо слегка модифицированная версия ElGamal/AES+SessionTag,
  либо что-то совершенно новое, например ChaCha/Poly) будет определено
  в одном или нескольких отдельных предложениях.
  См. также предложения ECIES 144 и 145.

### LeaseSet 2

- Срок действия в 8 байт в lease изменен на 4 байта.

- Если мы когда-либо реализуем отзыв, мы можем сделать это с полем expires равным нулю,
  или нулевыми leases, или и тем, и другим. Нет необходимости в отдельном ключе отзыва.

- Ключи шифрования расположены в порядке предпочтения сервера, наиболее предпочтительный первым.
  Поведение клиента по умолчанию — выбрать первый ключ с
  поддерживаемым типом шифрования. Клиенты могут использовать другие алгоритмы выбора
  на основе поддержки шифрования, относительной производительности и других факторов.

### Формат

Цели:

- Добавить блайндинг
- Разрешить несколько типов подписей
- Не требовать новых криптографических примитивов
- Опционально шифровать для каждого получателя, с возможностью отзыва
- Поддерживать шифрование только Standard LS2 и Meta LS2

Зашифрованный LS2 никогда не отправляется в end-to-end garlic сообщении. Используйте стандартный LS2, как описано выше.

Изменения по сравнению с существующим зашифрованным LeaseSet:

- Зашифровать всё целиком для безопасности
- Безопасно зашифровать, не только с помощью AES.
- Зашифровать для каждого получателя

Поиск с помощью

    Standard LS flag (1)
Сохранить с

    Encrypted LS2 type (5)
Сохранить в

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Типичный срок действия

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Опубликовано

    Destination


### Обоснование

Мы определяем следующие функции, соответствующие криптографическим строительным блокам, используемым для зашифрованного LS2:

ГПСЧ(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

ПОТОК

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Обсуждение

Зашифрованный формат LS2 состоит из трех вложенных слоев:

- Внешний слой, содержащий необходимую информацию в открытом виде для хранения и извлечения.
- Средний слой, который обрабатывает аутентификацию клиента.
- Внутренний слой, который содержит фактические данные LS2.

Общий формат выглядит следующим образом::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Обратите внимание, что зашифрованный LS2 является замаскированным. Destination не находится в заголовке. Местоположение хранения DHT — SHA-256(sig type || замаскированный публичный ключ) и меняется ежедневно.

НЕ использует стандартный заголовок LS2, указанный выше.

#### Layer 0 (outer)

Тип

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Тип подписи скрытого открытого ключа

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Затемнённый открытый ключ

    Length as implied by sig type

Временная метка публикации

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Истекает

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Флаги

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Данные временного ключа

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Подпись

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Флаги

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

DH данные аутентификации клиента

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Данные аутентификации клиента PSK

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Тип

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Данные

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Новые проблемы с шифрованием

Мы используем следующую схему для ослепления ключей, основанную на Ed25519 и [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Подписи Re25519 работают на кривой Ed25519, используя SHA-512 для хеширования.

Мы не используем [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3), который имеет схожие цели проектирования, поскольку его затененные публичные ключи могут находиться вне подгруппы простого порядка, что создает неизвестные последствия для безопасности.

#### Goals

- Подписывающий открытый ключ в незашифрованном destination должен быть
  Ed25519 (тип подписи 7) или Red25519 (тип подписи 11);
  другие типы подписей не поддерживаются
- Если подписывающий открытый ключ находится в автономном режиме, временный подписывающий открытый ключ также должен быть Ed25519
- Blinding является вычислительно простым
- Использует существующие криптографические примитивы
- Зашифрованные открытые ключи не могут быть расшифрованы
- Зашифрованные открытые ключи должны находиться на кривой Ed25519 и подгруппе простого порядка
- Необходимо знать подписывающий открытый ключ destination
  (полный destination не требуется) для получения зашифрованного открытого ключа
- Опционально предоставляет дополнительный секрет, необходимый для получения зашифрованного открытого ключа

#### Security

Безопасность схемы блайндинга требует, чтобы распределение alpha было таким же, как у небланкированных приватных ключей. Однако когда мы блайндим приватный ключ Ed25519 (тип подписи 7) в приватный ключ Red25519 (тип подписи 11), распределение отличается. Для соответствия требованиям [zcash раздел 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), Red25519 (тип подписи 11) должен использоваться и для небланкированных ключей, чтобы "комбинация перерандомизированного публичного ключа и подписи(ей) под этим ключом не раскрывала ключ, из которого он был перерандомизирован." Мы разрешаем тип 7 для существующих destinations, но рекомендуем тип 11 для новых destinations, которые будут зашифрованы.

#### Definitions

Б

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

альфа

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

а

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

А

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

А'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

Новые секретные alpha и blinded ключи должны генерироваться каждый день (UTC). Секретный alpha и blinded ключи вычисляются следующим образом.

GENERATE_ALPHA(destination, date, secret), для всех сторон:

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
BLIND_PRIVKEY(), для владельца, публикующего leaseset:

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
BLIND_PUBKEY(), для клиентов, получающих leaseset:

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Оба метода вычисления A' дают одинаковый результат, как и требуется.

#### Signing

Незашифрованный leaseset подписывается незашифрованным приватным ключом подписи Ed25519 или Red25519 и проверяется незашифрованным публичным ключом подписи Ed25519 или Red25519 (типы подписи 7 или 11) как обычно.

Если публичный ключ подписи находится в автономном режиме, незашифрованный leaseset подписывается незашифрованным временным закрытым ключом подписи Ed25519 или Red25519 и проверяется с помощью незашифрованного временного публичного ключа подписи Ed25519 или Red25519 (типы подписи 7 или 11) как обычно. См. дополнительные примечания по автономным ключам для зашифрованных leasesets ниже.

Для подписи зашифрованного leaseset мы используем Red25519, основанный на [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) для подписи и проверки со скрытыми ключами. Подписи Red25519 используют кривую Ed25519 с SHA-512 для хеширования.

Red25519 идентичен стандартному Ed25519 за исключением указанного ниже.

#### Sign/Verify Calculations

Внешняя часть зашифрованного leaseset использует ключи и подписи Red25519.

Red25519 практически идентичен Ed25519. Существует два различия:

Приватные ключи Red25519 генерируются из случайных чисел и затем должны быть приведены по модулю L, где L определено выше. Приватные ключи Ed25519 генерируются из случайных чисел и затем "зажимаются" с использованием побитового маскирования байтов 0 и 31. Это не выполняется для Red25519. Функции GENERATE_ALPHA() и BLIND_PRIVKEY(), определенные выше, генерируют правильные приватные ключи Red25519 с использованием mod L.

В Red25519 вычисление r для подписи использует дополнительные случайные данные и использует значение открытого ключа, а не хеш закрытого ключа. Благодаря случайным данным каждая подпись Red25519 отличается, даже при подписании одних и тех же данных одним и тем же ключом.

Подписание:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Проверка:

```text
// same as in Ed25519
```
### Примечания

#### Derivation of subcredentials

В рамках процесса ослепления нам необходимо убедиться, что зашифрованный LS2 может быть расшифрован только тем, кто знает соответствующий открытый ключ подписи Destination. Полный Destination не требуется. Для достижения этого мы выводим учетные данные из открытого ключа подписи:

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Строка персонализации гарантирует, что учетные данные не конфликтуют с любым хешем, используемым в качестве ключа поиска DHT, таким как обычный хеш Destination.

Для данного замаскированного ключа мы затем можем получить подучётные данные:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Субкредентиал включается в процессы вывода ключей ниже, что связывает эти ключи со знанием публичного ключа подписи Destination.

#### Layer 1 encryption

Сначала подготавливается входная информация для процесса выведения ключа:

```text
outerInput = subcredential || publishedTimestamp
```
Далее генерируется случайная соль:

```text
outerSalt = CSRNG(32)
```
Затем выводится ключ, используемый для шифрования слоя 1:

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Наконец, открытый текст уровня 1 шифруется и сериализуется:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

Соль извлекается из зашифрованного текста 1-го уровня:

```text
outerSalt = outerCiphertext[0:31]
```
Затем выводится ключ, используемый для шифрования слоя 1:

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Наконец, шифртекст уровня 1 расшифровывается:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Когда авторизация клиента включена, ``authCookie`` вычисляется как описано ниже. Когда авторизация клиента отключена, ``authCookie`` представляет собой массив байтов нулевой длины.

Шифрование происходит аналогично уровню 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Когда авторизация клиента включена, ``authCookie`` вычисляется как описано ниже. Когда авторизация клиента отключена, ``authCookie`` является байтовым массивом нулевой длины.

Расшифровка выполняется аналогичным образом, как и для слоя 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Зашифрованная LS2

Когда авторизация клиентов включена для Destination, сервер поддерживает список клиентов, которым он разрешает расшифровывать зашифрованные данные LS2. Данные, хранящиеся для каждого клиента, зависят от механизма авторизации и включают в себя некую форму ключевого материала, который каждый клиент генерирует и отправляет серверу через безопасный внеполосный механизм.

Существует две альтернативы для реализации авторизации для каждого клиента:

#### DH client authorization

Каждый клиент генерирует DH пару ключей ``[csk_i, cpk_i]`` и отправляет открытый ключ ``cpk_i`` на сервер.

Обработка на сервере
^^^^^^^^^^^^^^^^^

Сервер генерирует новый ``authCookie`` и эфемерную DH пару ключей:

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Затем для каждого авторизованного клиента сервер шифрует ``authCookie`` его открытым ключом:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Сервер помещает каждый кортеж ``[clientID_i, clientCookie_i]`` в слой 1 зашифрованного LS2, вместе с ``epk``.

Обработка клиента
^^^^^^^^^^^^^^^^^

Клиент использует свой закрытый ключ для получения ожидаемого идентификатора клиента ``clientID_i``, ключа шифрования ``clientKey_i`` и вектора инициализации шифрования ``clientIV_i``:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Затем клиент ищет в данных авторизации уровня 1 запись, содержащую ``clientID_i``. Если соответствующая запись существует, клиент расшифровывает её для получения ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Каждый клиент генерирует секретный 32-байтный ключ ``psk_i`` и отправляет его на сервер. Альтернативно, сервер может сгенерировать секретный ключ и отправить его одному или нескольким клиентам.

Обработка на сервере
^^^^^^^^^^^^^^^^^

Сервер генерирует новый ``authCookie`` и соль:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Затем для каждого авторизованного клиента сервер шифрует ``authCookie`` своим заранее распределенным ключом:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Сервер помещает каждую пару ``[clientID_i, clientCookie_i]`` в слой 1 зашифрованного LS2 вместе с ``authSalt``.

Обработка клиента
^^^^^^^^^^^^^^^^^

Клиент использует свой предварительно разделенный ключ для получения ожидаемого идентификатора клиента ``clientID_i``, ключа шифрования ``clientKey_i`` и вектора инициализации шифрования ``clientIV_i``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Затем клиент ищет в данных авторизации уровня 1 запись, которая содержит ``clientID_i``. Если соответствующая запись существует, клиент расшифровывает её для получения ``authCookie``:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Оба механизма авторизации клиентов, описанные выше, обеспечивают приватность членства клиентов. Сущность, которая знает только Destination, может видеть, сколько клиентов подписано в любой момент времени, но не может отслеживать, какие клиенты добавляются или отзываются.

Серверы ДОЛЖНЫ рандомизировать порядок клиентов каждый раз при генерации зашифрованного LS2, чтобы предотвратить возможность клиентов узнать свою позицию в списке и делать выводы о том, когда другие клиенты были добавлены или исключены.

Сервер МОЖЕТ выбрать скрытие количества подписанных клиентов путем вставки случайных записей в список данных авторизации.

Преимущества авторизации клиента DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Безопасность схемы не зависит исключительно от внеполосного обмена ключевым   материалом клиента. Приватный ключ клиента никогда не должен покидать его устройство, и поэтому   противник, который способен перехватить внеполосный обмен, но не может взломать   алгоритм DH, не может расшифровать зашифрованный LS2 или определить, как долго клиенту предоставлен   доступ.

Недостатки DH авторизации клиентов
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Требует N + 1 DH операций на стороне сервера для N клиентов.
- Требует одну DH операцию на стороне клиента.
- Требует от клиента генерации секретного ключа.

Преимущества PSK авторизации клиента
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Не требует операций DH.
- Позволяет серверу генерировать секретный ключ.
- Позволяет серверу использовать один и тот же ключ для нескольких клиентов, если это необходимо.

Недостатки авторизации клиентов PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Безопасность схемы критически зависит от внеполосного обмена ключевым   материалом клиента. Противник, который перехватывает обмен для конкретного клиента, может расшифровать   любой последующий зашифрованный LS2, для которого этот клиент авторизован, а также определить,   когда доступ клиента отозван.

### Определения

См. предложение 149.

Вы не можете использовать зашифрованный LS2 для bittorrent из-за компактных ответов announce, которые составляют 32 байта. Эти 32 байта содержат только хеш. В них нет места для указания того, что leaseSet зашифрован, или типов подписи.

### Формат

Для зашифрованных leaseSet с офлайн-ключами, слепые приватные ключи также должны генерироваться офлайн, по одному для каждого дня.

Поскольку необязательный блок оффлайн-подписи находится в открытой части зашифрованного leaseset, любой, кто сканирует floodfill-узлы, может использовать это для отслеживания leaseset (но не для его расшифровки) в течение нескольких дней. Чтобы предотвратить это, владелец ключей должен также генерировать новые временные ключи для каждого дня. Как временные, так и слепые ключи могут быть сгенерированы заранее и переданы в router пакетом.

В данном предложении не определен формат файла для упаковки множественных временных и скрытых ключей и их предоставления клиенту или router. В данном предложении не определено улучшение протокола I2CP для поддержки зашифрованных leaseSet с автономными ключами.

### Notes

- Сервис, использующий зашифрованные leaseSet'ы, будет публиковать зашифрованную версию на
  floodfill'ы. Однако для эффективности он будет отправлять незашифрованные leaseSet'ы
  клиентам в обёрнутом garlic-сообщении после аутентификации (например, через whitelist).

- Floodfill могут ограничивать максимальный размер до разумного значения для предотвращения злоупотреблений.

- После расшифровки следует выполнить несколько проверок, включая соответствие
  внутренней временной метки и срока действия тем, что указаны на верхнем уровне.

- ChaCha20 был выбран вместо AES. Хотя скорости схожи при наличии аппаратной поддержки AES, ChaCha20 в 2,5-3 раза быстрее, когда аппаратная поддержка AES недоступна, например, на ARM-устройствах начального уровня.

- Мы недостаточно заботимся о скорости, чтобы использовать keyed BLAKE2b. Он имеет
  размер вывода, достаточно большой для размещения наибольшего n, который нам требуется (или мы можем вызвать его один раз для каждого
  желаемого ключа с аргументом счётчика). BLAKE2b намного быстрее, чем SHA-256, и
  keyed-BLAKE2b уменьшил бы общее количество вызовов хеш-функции.
  Однако, см. предложение 148, где предлагается переключиться на BLAKE2b по другим причинам.
  См. [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Это используется для замены multihoming. Как и любой leaseset, он подписан создателем. Это аутентифицированный список хешей назначений.

Meta LS2 является вершиной и, возможно, промежуточными узлами древовидной структуры. Он содержит несколько записей, каждая из которых указывает на LS, LS2 или другой Meta LS2 для поддержки масштабного multihoming. Meta LS2 может содержать смешанные записи LS, LS2 и Meta LS2. Листьями дерева всегда являются LS или LS2. Дерево представляет собой DAG; циклы запрещены; клиенты, выполняющие поиск, должны обнаруживать циклы и отказываться от их прохождения.

Meta LS2 может иметь значительно более длительный срок действия, чем стандартный LS или LS2. Верхний уровень может иметь срок действия через несколько часов после даты публикации. Максимальное время истечения срока действия будет принудительно применяться floodfill-узлами и клиентами, и пока не определено.

Случай использования для Meta LS2 — это массовый мультихоминг, но без дополнительной защиты от корреляции роутеров с leaseSet'ами (во время перезапуска роутера) по сравнению с той, что предоставляется сейчас с LS или LS2. Это эквивалентно случаю использования "facebook", который, вероятно, не нуждается в защите от корреляции. Этот случай использования, вероятно, требует offline-ключей, которые предоставляются в стандартном заголовке на каждом узле дерева.

Протокол back-end для координации между leaf router'ами, промежуточными и главными подписантами Meta LS здесь не определен. Требования крайне просты - просто проверить, что узел активен, и публиковать новый LS каждые несколько часов. Единственная сложность заключается в выборе новых издателей для Meta LSes верхнего или промежуточного уровня при сбое.

Комбинированные leaseSet-ы, где lease-ы от нескольких роутеров объединяются, подписываются и публикуются в одном leaseSet, описаны в предложении 140 "невидимое мультихоминг". Это предложение в написанном виде неосуществимо, поскольку потоковые соединения не будут "привязаны" к одному роутеру, см. http://zzz.i2p/topics/2335 .

Протокол бэкенда и взаимодействие с внутренними компонентами router и клиента были бы довольно сложными для невидимого мультихоминга.

Чтобы избежать перегрузки floodfill для Meta LS верхнего уровня, срок истечения должен составлять как минимум несколько часов. Клиенты должны кэшировать Meta LS верхнего уровня и сохранять его при перезапусках, если он не истёк.

Нам нужно определить алгоритм для клиентов по обходу дерева, включая резервные варианты, чтобы использование было распределено. Некоторая функция расстояния хэша, стоимости и случайности. Если узел имеет как LS или LS2, так и Meta LS, нам нужно знать, когда разрешено использовать эти leaseSet'ы, а когда продолжать обход дерева.

Поиск с помощью

    Standard LS flag (1)
Хранить с

    Meta LS2 type (7)
Хранить в

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Типичное истечение срока

    Hours. Max 18.2 hours (65535 seconds)
Опубликовано

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Флаги и свойства: для будущего использования

### Вывод ключа ослепления

- Распределенная служба, использующая это, будет иметь одного или нескольких "мастеров" с приватным ключом destination службы. Они будут (вне полосы) определять текущий список активных destination и публиковать Meta LS2. Для избыточности несколько мастеров могут использовать multihome (т.е. одновременно публиковать) Meta LS2.

- Распределённый сервис может начать с одного destination или использовать multihoming старого стиля, затем перейти на Meta LS2. Стандартный LS lookup может вернуть любой из LS, LS2 или Meta LS2.

- Когда сервис использует Meta LS2, у него нет туннелей (leases).

### Service Record

Это индивидуальная запись, указывающая, что пункт назначения участвует в сервисе. Она отправляется от участника к floodfill. Она никогда не отправляется индивидуально floodfill-узлом, а только как часть Списка Сервисов. Запись Сервиса также используется для отзыва участия в сервисе путем установки срока истечения в ноль.

Это не LS2, но используется стандартный формат заголовка и подписи LS2.

Поиск с помощью

    n/a, see Service List
Хранить с

    Service Record type (9)
Сохранить в

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Типичный срок действия

    Hours. Max 18.2 hours (65535 seconds)
Опубликовано

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Если expires содержит только нули, floodfill должен отозвать запись и больше не включать её в список сервисов.

- Хранение: Floodfill может строго ограничивать хранение этих записей и
  лимитировать количество записей, хранимых на один хеш, и время их истечения. Также может
  использоваться белый список хешей.

- Любой другой тип netdb с тем же хешем имеет приоритет, поэтому служебная запись никогда не может перезаписать LS/RI, но LS/RI перезапишет все служебные записи с этим хешем.

### Service List

Это совершенно не похоже на LS2 и использует другой формат.

Список сервисов создается и подписывается floodfill. Он не аутентифицирован в том смысле, что любой может присоединиться к сервису, опубликовав Service Record на floodfill.

Список Сервисов содержит Краткие Записи Сервисов, а не полные Записи Сервисов. Они содержат подписи, но только хеши, а не полные назначения, поэтому они не могут быть проверены без полного назначения.

Безопасность, если таковая имеется, и целесообразность списков сервисов остается неопределенной (TBD). Floodfill-узлы могли бы ограничить публикацию и поиск белым списком сервисов, но такой белый список может различаться в зависимости от реализации или предпочтений оператора. Возможно, не удастся достичь консенсуса относительно общего базового белого списка между различными реализациями.

Если имя сервиса включено в служебную запись выше, то операторы floodfill могут возразить; если включен только хеш, то проверки нет, и служебная запись может "попасть" раньше любого другого типа netdb и сохраниться в floodfill.

Поиск с помощью

    Service List lookup type (11)
Сохранить с

    Service List type (11)
Хранить в

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Типичное истечение срока действия

    Hours, not specified in the list itself, up to local policy
Опубликовано

    Nobody, never sent to floodfill, never flooded.

### Format

НЕ использует стандартный заголовок LS2, указанный выше.

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Для проверки подписи Списка Сервисов:

- добавить в начало хеш имени сервиса
- удалить хеш создателя
- Проверить подпись измененного содержимого

Для проверки подписи каждой записи Short Service Record:

- Получить назначение
- Проверить подпись (опубликованная временная метка + истекает + флаги + порт + хеш имени сервиса)

Для проверки подписи каждой записи отзыва:

- Получить место назначения
- Проверить подпись (опубликованная временная метка + 4 нулевых байта + флаги + порт + хеш
  имени сервиса)

### Notes

- Мы используем длину подписи вместо типа подписи, чтобы поддерживать неизвестные типы подписей.

- Список сервисов не имеет срока истечения, получатели могут принимать собственные
  решения на основе политики или истечения срока действия отдельных записей.

- Списки Сервисов не распространяются по всей сети, только отдельные Записи Сервисов. Каждый floodfill создает, подписывает и кэширует Список Сервисов. floodfill использует свою собственную политику для времени кэширования и максимального количества записей сервисов и отзыва.

## Common Structures Spec Changes Required

### Шифрование и обработка

Выходит за рамки данного предложения. Добавить к предложениям ECIES 144 и 145.

### New Intermediate Structures

Добавить новые структуры для Lease2, MetaLease, LeaseSet2Header и OfflineSignature. Действует начиная с релиза 0.9.38.

### New NetDB Types

Добавьте структуры для каждого нового типа leaseset, включенные выше. Для LeaseSet2, EncryptedLeaseSet и MetaLeaseSet действует с версии 0.9.38. Для Service Record и Service List - предварительные и незапланированные.

### New Signature Type

Добавить RedDSA_SHA512_Ed25519 тип 11. Открытый ключ — 32 байта; закрытый ключ — 32 байта; хеш — 64 байта; подпись — 64 байта.

## Encryption Spec Changes Required

Выходит за рамки данного предложения. См. предложения 144 и 145.

## I2NP Changes Required

Добавить примечание: LS2 может публиковаться только на floodfill с минимальной версией.

### Database Lookup Message

Добавьте тип поиска списка сервисов.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Авторизация для каждого клиента

Добавить все новые типы хранилищ.

### Changes

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## I2CP Changes Required

### I2CP Options

Новые опции, интерпретируемые на стороне роутера, отправляемые в SessionConfig Mapping:

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Новые опции, интерпретируемые на стороне клиента:

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Session Config

Обратите внимание, что для оффлайн подписей требуются опции i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey и i2cp.leaseSetOfflineSignature, и подпись выполняется временным приватным ключом подписи.

### Зашифрованные LS с адресами Base 32

От router к клиенту. Без изменений. Аренды отправляются с 8-байтовыми временными метками, даже если возвращаемый leaseSet будет LS2 с 4-байтовыми временными метками. Обратите внимание, что ответ может быть сообщением Create Leaseset или Create Leaseset2.

### Зашифрованный LS с офлайн ключами

Router к клиенту. Без изменений. Leases отправляются с 8-байтными временными метками, даже если возвращаемый leaseset будет LS2 с 4-байтными временными метками. Обратите внимание, что ответ может быть сообщением Create Leaseset или Create Leaseset2.

### Примечания

Клиент к роутеру. Новое сообщение, используемое вместо сообщения Create Leaseset Message.

### Meta LS2

- Чтобы router мог распознать тип хранилища, тип должен быть включен в сообщение,
  если только он не был передан router'у заранее в конфигурации сессии.
  Для общего кода парсинга проще иметь его в самом сообщении.

- Чтобы router знал тип и длину приватного ключа,
  он должен идти после lease set, если только парсер не знает тип заранее
  в конфигурации сессии.
  Для общего кода парсинга проще узнать это из самого сообщения.

- Закрытый ключ для подписи, ранее определенный для отзыва и неиспользуемый,
  отсутствует в LS2.

### Формат

Тип сообщения для сообщения Create Leaseset2 Message равен 41.

### Примечания

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Запись службы

- Минимальная версия маршрутизатора — 0.9.39.
- Предварительная версия с типом сообщения 40 была в версии 0.9.38, но формат был изменен.
  Тип 40 заброшен и не поддерживается.

### Формат

- Необходимы дополнительные изменения для поддержки зашифрованных и мета LS.

### Примечания

Клиент к роутеру. Новое сообщение.

### Список сервисов

- Роутер должен знать, является ли назначение blinded.
  Если оно является blinded и использует секретную или per-client аутентификацию,
  ему также необходимо иметь эту информацию.

- Host Lookup нового формата b32-адреса ("b33")
  сообщает роутеру, что адрес является скрытым (blinded), но не существует механизма
  для передачи секретного или приватного ключа роутеру в сообщении Host Lookup.
  Хотя мы могли бы расширить сообщение Host Lookup для добавления этой информации,
  более правильным решением будет определить новое сообщение.

- Нам нужен программный способ для клиента сообщить router'у.
  В противном случае пользователю пришлось бы вручную настраивать каждое назначение.

### Формат

Прежде чем клиент отправит сообщение в blinded destination, он должен либо найти "b33" в сообщении Host Lookup, либо отправить сообщение Blinding Info. Если blinded destination требует секрета или аутентификации для каждого клиента, клиент должен отправить сообщение Blinding Info.

Роутер не отправляет ответ на это сообщение.

### Примечания

Тип сообщения для Blinding Info Message равен 42.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Ключевые сертификаты

- Минимальная версия маршрутизатора router 0.9.43

### Новые промежуточные структуры

### Новые типы NetDB

Чтобы поддерживать поиск имён хостов "b33" и возвращать индикацию, если router не имеет необходимой информации, мы определяем дополнительные коды результатов для Host Reply Message следующим образом:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Значения 1-255 уже определены как ошибки, поэтому проблем с обратной совместимостью нет.

### Новый тип подписи

Маршрутизатор к клиенту. Новое сообщение.

### Justification

Клиент не знает a priori, что данный хеш будет разрешен в Meta LS.

Если поиск leaseset для Destination возвращает Meta LS, router выполнит рекурсивное разрешение. Для датаграмм клиентская сторона не должна знать об этом; однако для потоковой передачи, где протокол проверяет назначение в SYN ACK, он должен знать, что является "реальным" назначением. Поэтому нам нужно новое сообщение.

### Usage

Router поддерживает кеш для фактического пункта назначения, который используется из мета-LS. Когда клиент отправляет сообщение на пункт назначения, который разрешается в мета-LS, router проверяет кеш для последнего используемого фактического пункта назначения. Если кеш пуст, router выбирает пункт назначения из мета-LS и ищет leaseSet. Если поиск leaseSet успешен, router добавляет этот пункт назначения в кеш и отправляет клиенту Meta Redirect Message. Это делается только один раз, если только пункт назначения не истекает и не должен быть изменен. Клиент также должен кешировать информацию при необходимости. Meta Redirect Message НЕ отправляется в ответ на каждое SendMessage.

Роутер отправляет это сообщение только клиентам с версией 0.9.47 или выше.

Клиент не отправляет ответ на это сообщение.

### Сообщение запроса базы данных

Тип сообщения для Meta Redirect Message равен 43.

### Изменения

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Сообщение хранилища базы данных

Как генерировать и поддерживать Meta, включая межроутерную коммуникацию и координацию, выходит за рамки данного предложения. См. связанное предложение 150.

### Изменения

Офлайн подписи не могут быть проверены в потоковых или отвечаемых датаграммах. См. разделы ниже.

## Private Key File Changes Required

Формат файла приватного ключа (eepPriv.dat) не является официальной частью наших спецификаций, но он документирован в [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) и другие реализации его поддерживают. Это обеспечивает переносимость приватных ключей между различными реализациями.

Необходимы изменения для хранения временного публичного ключа и информации об автономной подписи.

### Changes

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Опции I2CP

Добавить поддержку следующих опций:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Оффлайн подписи в настоящее время не могут быть проверены в streaming. Изменение ниже добавляет блок оффлайн подписи в опции. Это позволяет избежать необходимости получения этой информации через I2CP.

### Конфигурация сессии

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Сообщение запроса LeaseSet

- Альтернативой является просто добавить флаг и получить транзитный публичный ключ через I2CP
  (См. разделы Host Lookup / Host Reply Message выше)

## Стандартный заголовок LS2

Автономные подписи не могут быть проверены при обработке датаграмм с возможностью ответа. Необходим флаг для указания автономной подписи, но нет места для размещения флага. Потребуется совершенно новый номер протокола и формат.

### Сообщение запроса переменного LeaseSet

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Создать сообщение Leaseset2

- Альтернативный вариант — просто добавить флаг и получить временный публичный ключ через I2CP
  (См. разделы Host Lookup / Host Reply Message выше)
- Какие-либо другие опции, которые мы должны добавить сейчас, когда у нас есть байты флагов?

## SAM V3 Changes Required

SAM должен быть улучшен для поддержки офлайн подписей в DESTINATION base 64.

### Обоснование

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Обратите внимание, что оффлайн-подписи поддерживаются только для STREAM и RAW, но не для DATAGRAM (пока мы не определим новый протокол DATAGRAM).

Обратите внимание, что SESSION STATUS будет возвращать приватный ключ подписи из всех нулей и данные оффлайн-подписи точно в том виде, в каком они были предоставлены в SESSION CREATE.

Обратите внимание, что DEST GENERATE и SESSION CREATE DESTINATION=TRANSIENT нельзя использовать для создания offline подписанного назначения.

### Тип сообщения

Повысить версию до 3.4, или оставить её на 3.1/3.2/3.3, чтобы её можно было добавить без необходимости всех компонентов 3.2/3.3?

Другие изменения уточняются. См. раздел I2CP Host Reply Message выше.

## BOB Changes Required

BOB должен был бы быть улучшен для поддержки оффлайн подписей и/или Meta LS. Это низкий приоритет и, вероятно, никогда не будет специфицировано или реализовано. SAM V3 является предпочтительным интерфейсом.

## Publishing, Migration, Compatibility

LS2 (кроме зашифрованной LS2) публикуется в том же DHT-расположении, что и LS1. Нет способа опубликовать одновременно LS1 и LS2, если только LS2 не будет находиться в другом расположении.

Зашифрованный LS2 публикуется по хешу типа замаскированного ключа и данных ключа. Этот хеш затем используется для генерации ежедневного "routing key", как в LS1.

LS2 будет использоваться только когда требуются новые функции (новая криптография, зашифрованный LS, мета и т.д.). LS2 может публиковаться только на floodfill указанной версии или выше.

Серверы, публикующие LS2, будут знать, что любые подключающиеся клиенты поддерживают LS2. Они могут отправлять LS2 в garlic.

Клиенты отправляли бы LS2 в garlic только при использовании новой криптографии. Общие клиенты использовали бы LS1 бесконечно? TODO: Как иметь общих клиентов, которые поддерживают и старую, и новую криптографию?

## Rollout

0.9.38 содержит поддержку floodfill для стандартных LS2, включая оффлайн ключи.

0.9.39 содержит поддержку I2CP для LS2 и Encrypted LS2, подписание/верификацию типа подписи 11, поддержку floodfill для Encrypted LS2 (типы подписей 7 и 11, без офлайн ключей), а также шифрование/дешифрование LS2 (без авторизации для отдельных клиентов).

0.9.40 планируется включить поддержку шифрования/расшифровки LS2 с авторизацией для каждого клиента, поддержку floodfill и I2CP для Meta LS2, поддержку зашифрованных LS2 с оффлайн-ключами и поддержку b32 для зашифрованных LS2.

## Новые типы DatabaseEntry

Дизайн зашифрованного LS2 во многом основан на [дескрипторах скрытых сервисов v3 Tor](https://spec.torproject.org/rend-spec-v3), которые имели схожие цели проектирования.
