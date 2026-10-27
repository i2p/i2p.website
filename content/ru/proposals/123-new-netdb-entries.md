---
title: "Новые записи netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Открыть"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Статус

Части этого предложения завершены и реализованы в версиях 0.9.38 и 0.9.39.   Общие структуры, I2CP, I2NP и другие спецификации   обновлены, чтобы отразить поддерживаемые изменения.

Завершённые части всё ещё могут быть подвергнуты незначительным изменениям.   Другие части предложения всё ещё находятся в разработке   и могут быть существенно пересмотрены.

Поиск сервисов (типы 9 и 11) имеет низкий приоритет,   не запланирован и может быть вынесен в отдельное предложение.

## Обзор

Это обновление и объединение следующих 4 предложений:

- 110 LS2
- 120 Meta LS2 для массового мультихоминга
- 121 Зашифрованный LS2
- 122 Неаутентифицированный поиск сервисов (аникастинг)

Эти предложения в основном независимы, но для ясности мы определяем и используем   общий формат для нескольких из них.

Следующие предложения частично связаны:

- 140 Невидимый мультихоминг (несовместим с этим предложением)
- 142 Новый шаблон криптографии (для новых симметричных криптосистем)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 для зашифрованного LS2
- 150 Протокол Garlic Farm
- 151 ECDSA Blinding

## Предложение

Это предложение определяет 5 новых типов DatabaseEntry и процесс   их хранения и извлечения из сетевой базы данных,   а также метод подписи и проверки этих подписей.

### Цели

- Обратная совместимость
- LS2 должен работать со старым стилем мультихоминга
- Не требуется новая криптография или примитивы для поддержки
- Сохранение разделения криптографии и подписи; поддержка всех текущих и будущих версий
- Поддержка опциональных оффлайн-ключей для подписи
- Уменьшение точности временных меток для снижения фингерпринтинга
- Включение новых криптосистем для назначений
- Поддержка массового мультихоминга
- Исправление нескольких проблем с существующим зашифрованным LS
- Опциональное маскирование (blinding) для уменьшения видимости floodfill-узлами
- Зашифрованный LS поддерживает как одноключевую, так и многоключевую с возможностью отзыва схему
- Поиск сервисов для упрощения поиска outproxy, DHT-загрузки приложений и других задач
- Не нарушать работу существующих систем, зависящих от 32-байтовых хешей назначений, например, bittorrent
- Добавить гибкость в leasesets через свойства, как в routerinfos
- Поместить опубликованную временную метку и переменное время истечения в заголовок, чтобы это работало даже  
  если содержимое зашифровано (не выводить временную метку из самого раннего лиза)
- Все новые типы находятся в том же пространстве DHT и в тех же местах, что и существующие leasesets,  
  чтобы пользователи могли перейти со старого LS на LS2,  
  или переключаться между LS2, Meta и Encrypted,  
  не меняя назначение или хеш.
- Существующее назначение может быть переведено на оффлайн-ключи,  
  или обратно на онлайн-ключи, без изменения назначения или хеша.

### Нецели / Вне области

- Новый алгоритм вращения DHT или генерация общего случайного числа
- Конкретный новый тип шифрования и end-to-end схема шифрования  
  будут определены в отдельном предложении.  
  Никакая новая криптография здесь не определяется и не обсуждается.
- Новое шифрование для RIs или построения туннелей.  
  Будет в отдельном предложении.
- Методы шифрования, передачи и приёма сообщений I2NP DLM / DSM / DSRM.  
  Не меняются.
- Как генерировать и поддерживать Meta, включая межузловую коммуникацию, управление, отказоустойчивость и координацию.  
  Поддержка может быть добавлена в I2CP, i2pcontrol или новый протокол.  
  Это может быть стандартизировано или нет.
- Как реализовать и управлять туннелями с длительным сроком действия или отменять существующие туннели.  
  Это крайне сложно, и без этого невозможно реализовать разумное плавное завершение работы.
- Изменения модели угроз
- Формат хранения оффлайн, или методы хранения/извлечения/обмена данными.
- Детали реализации здесь не обсуждаются и остаются на усмотрение каждого проекта.

### Обоснование

LS2 добавляет поля для изменения типа шифрования и будущих изменений протокола.

Зашифрованный LS2 исправляет несколько проблем безопасности существующего зашифрованного LS,   используя асимметричное шифрование всего набора лизов.

Meta LS2 обеспечивает гибкий, эффективный, надёжный и масштабируемый мультихоминг.

Запись сервиса и Список сервисов обеспечивают anycast-сервисы, такие как поиск имён   и загрузка DHT.

### Типы данных NetDB

Номера типов используются в сообщениях I2NP Database Lookup/Store.

Колонка end-to-end указывает, отправляются ли запросы/ответы назначению в сообщении Garlic.

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
### Примечания

- Типы поиска в настоящее время используют биты 3-2 в сообщении Database Lookup.  
  Любые дополнительные типы потребуют использования бита 4.

- Все типы хранения нечётные, так как старшие биты в поле типа сообщения Database Store  
  игнорируются старыми маршрутизаторами.  
  Мы предпочитаем, чтобы разбор завершался с ошибкой как LS, а не как сжатый RI.

- Должен ли тип быть явным, неявным или ни тем, ни другим в данных, охватываемых подписью?

### Процесс поиска/хранения

Типы 3, 5 и 7 могут быть возвращены в ответ на стандартный запрос leaseset (тип 1).   Тип 9 никогда не возвращается в ответ на запрос.   Тип 11 возвращается в ответ на новый тип поиска сервиса (тип 11).

Только тип 3 может быть отправлен в сообщении Garlic от клиента к клиенту.

### Формат

Типы 3, 7 и 9 имеют общий формат::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
Стандартный заголовок LS2

Часть, специфичная для типа

### Рассмотрение вопросов конфиденциальности/безопасности

Стандартная подпись LS2:

## Стандартный заголовок LS2

Тип 5 (зашифрованный) не начинается с назначения и имеет   другой формат. См. ниже.

### Формат

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
### Обоснование

  - как определено ниже

  - как определено ниже для каждого типа

  - Длина определяется типом подписи ключа подписи

- Неопубликованный/опубликованный: Для использования при отправке сообщения Database Store end-to-end,  
  отправляющий маршрутизатор может указать, что этот leaseset не должен  
  отправляться другим. В настоящее время мы используем эвристику для поддержания этого состояния.

### Проблемы

- Опубликованный: Заменяет сложную логику определения 'версии' leaseset.  
  В настоящее время версия — это срок действия последнего истекающего лиза,  
  и маршрутизатор, публикующий leaseset, который только удаляет старый лиз,  
  должен увеличить этот срок как минимум на 1 мс.

- Истекает: Позволяет сроку действия записи netdb быть раньше, чем у  
  его последнего истекающего leaseset. Может быть не полезно для LS2, где ожидается, что leasesets  
  будут иметь максимальный срок действия 11 минут, но  
  для других новых типов это необходимо (см. Meta LS и Service Record ниже).

- Оффлайн-ключи являются опциональными, чтобы уменьшить начальную/требуемую сложность реализации.

### Примечания

- Можно ещё больше уменьшить точность временной метки (10 минут?), но тогда нужно добавить  
  номер версии. Это может нарушить мультихоминг, если у нас нет порядкового шифрования?  
  Вероятно, нельзя обойтись без временных меток вообще.

- Альтернатива: 3-байтовая временная метка (эпоха / 10 минут), 1-байтовая версия, 2-байтовый срок истечения

- Является ли тип явным или неявным в данных / подписи? "Доменные" константы для подписи?

## Новые типы DatabaseEntry

### LeaseSet 2

Тип 11 (Service List) — это агрегация нескольких Service Records и имеет   другой формат. См. ниже.

- Маршрутизаторы не должны публиковать LS чаще одного раза в секунду.  
  Если они это делают, они должны искусственно увеличить опубликованную временную метку на 1  
  по сравнению с ранее опубликованным LS.

TBD

    Standard LS flag (1)
Типы 3, 7 и 9 используют стандартный заголовок LS2, определённый ниже:

    Standard LS2 type (3)
Изменения по сравнению с существующим LeaseSet:

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Поиск с помощью

    10 minutes, as in a regular LS.
Хранение с помощью

    Destination

### Формат

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
### Обоснование

- Реализации маршрутизаторов могут кэшировать временные ключи и подпись,  
  чтобы избежать проверки каждый раз. В частности, floodfill-узлы и маршрутизаторы на  
  обоих концах долгоживущих соединений могут выиграть от этого.

- Оффлайн-ключи и подпись подходят только для долгоживущих назначений,  
  т.е. серверов, а не клиентов.

### Обсуждение

Хранение в

Типичное истечение

Публикуется

- Добавлены опубликованная временная метка, временная метка истечения, флаги и свойства
- Добавлен тип шифрования
- Удалён ключ отзыва

Это предложение продолжает использовать публичный ключ в leaseset как   ключ end-to-end шифрования и оставляет поле публичного ключа в   назначении неиспользуемым, как сейчас. Тип шифрования не указан   в сертификате ключа назначения, он останется 0.

- Свойства: Будущее расширение и гибкость.  
  Размещены первыми на случай, если они необходимы для разбора остальных данных.

### Новые проблемы шифрования

Отклонённая альтернатива — указать тип шифрования в сертификате ключа назначения,   использовать публичный ключ в назначении и не использовать публичный ключ   в leaseset. Мы не планируем этого делать.

- Несколько пар тип/публичный ключ шифрования  
  для упрощения перехода на новые типы шифрования. Другой способ —  
  публиковать несколько leasesets, возможно, используя одни и те же туннели,  
  как мы делаем сейчас для назначений DSA и EdDSA.  
  Определение входящего типа шифрования на туннеле  
  может быть выполнено с помощью существующего механизма session tag,  
  и/или пробного расшифрования с каждым ключом. Длина входящих  
  сообщений также может дать подсказку.

- Местоположение фактического публичного ключа не меняется.
- Тип шифрования или публичный ключ могут меняться без изменения назначения.
- Удаляется неиспользуемое поле отзыва
- Базовая совместимость с другими типами DatabaseEntry в этом предложении
- Позволяет использовать несколько типов шифрования

- Местоположение публичного ключа и типа шифрования отличается от RouterInfo
- Сохраняется неиспользуемый публичный ключ в leaseset
- Требует реализации по всей сети; в альтернативе могут использоваться экспериментальные  
  типы шифрования, если разрешены floodfill-узлами  
  (но см. связанные предложения 136 и 137 о поддержке экспериментальных типов подписей).  
  Альтернативное предложение может быть проще в реализации и тестировании для экспериментальных типов шифрования.

### Примечания

- Тип шифрования представляет комбинацию  
  кривой, длины ключа и end-to-end схемы,  
  включая KDF и MAC, если есть.

- Мы включили поле длины ключа, чтобы LS2 был  
  разбираемым и проверяемым floodfill-узлом даже для неизвестных типов шифрования.

- Первым новым типом шифрования, который будет предложен, вероятно, будет  
  ECIES/X25519. Как он используется end-to-end  
  (либо слегка изменённая версия ElGamal/AES+SessionTag,  
  либо что-то совершенно новое, например, ChaCha/Poly) будет определено  
  в одном или нескольких отдельных предложениях.  
  См. также предложения по ECIES 144 и 145.

### Зашифрованный LS2

Преимущества LS2:

- 8-байтовый срок истечения в лизах изменён на 4 байта.

Недостатки LS2:

Часть этого выходит за рамки данного предложения,   но пока помещаем заметки здесь, так как у нас ещё нет   отдельного предложения по шифрованию.   См. также предложения по ECIES 144 и 145.

- Если мы когда-нибудь реализуем отзыв, мы можем сделать это с помощью поля истечения ноль,  
  или нулевых лизов, или обоих. Отдельный ключ отзыва не нужен.

Цели:

    Standard LS flag (1)
Зашифрованный LS2 никогда не отправляется в end-to-end сообщении Garlic.   Используйте стандартный LS2, как указано выше.

    Encrypted LS2 type (5)
Изменения по сравнению с существующим зашифрованным LeaseSet:

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Поиск с помощью

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Хранение с помощью

    Destination


### Определения

Хранение в

Типичное истечение

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Публикуется

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Мы определяем следующие функции, соответствующие криптографическим строительным блокам, используемым   для зашифрованного LS2:

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

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

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Формат

SIG

- Ключи шифрования упорядочены по предпочтению сервера, наиболее предпочтительные первыми.  
  Поведение клиента по умолчанию — выбирать первый ключ с  
  поддерживаемым типом шифрования. Клиенты могут использовать другие алгоритмы выбора  
  на основе поддержки шифрования, относительной производительности и других факторов.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Формат зашифрованного LS2 состоит из трёх вложенных слоёв:

#### Слой 0 (внешний)

Общий формат выглядит так::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Обратите внимание, что зашифрованный LS2 маскируется. Назначение не находится в заголовке.   Место хранения в DHT — SHA-256(тип подписи || маскированный публичный ключ), и вращается ежедневно.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

НЕ использует стандартный заголовок LS2, указанный выше.

    Length as implied by sig type

Тип

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Тип публичного ключа с маскированием

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Маскированный публичный ключ

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Опубликованная временная метка

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

Истекает

    2 bytes, big endian

Флаги

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Данные временного ключа

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Слой 1 (средний)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

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

Подпись

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


Флаги

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Слой 2 (внутренний)

Данные аутентификации по DH

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Данные аутентификации по PSK

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Выведение ключа маскирования

innerCiphertext

Тип

#### Цели

- Добавить маскирование (blinding)
- Разрешить несколько типов подписей
- Не требовать новых криптографических примитивов
- Опционально шифровать для каждого получателя, отзываемо
- Поддерживать шифрование только стандартного LS2 и Meta LS2

#### Безопасность

Данные

#### Определения

Мы используем следующую схему для маскирования ключа,   основанную на Ed25519 и [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   Подписи Re25519 делаются по кривой Ed25519 с использованием SHA-512 для хеширования.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Мы не используем [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3),   который имеет схожие цели проектирования, потому что его маскированные публичные ключи   могут находиться вне подгруппы простого порядка, с неизвестными последствиями для безопасности.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Безопасность схемы маскирования требует, чтобы   распределение alpha было таким же, как у немаскированных приватных ключей.   Однако, когда мы маскируем приватный ключ Ed25519 (тип подписи 7)   в приватный ключ Red25519 (тип подписи 11), распределение отличается.   Чтобы соответствовать требованиям [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   Red25519 (тип подписи 11) должен использоваться и для немаскированных ключей, чтобы   "комбинация переупорядоченного публичного ключа и подписей   под этим ключом не раскрывала ключ, из которого он был переупорядочен".   Мы разрешаем тип 7 для существующих назначений, но рекомендуем   тип 11 для новых назначений, которые будут зашифрованы.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Расчёты маскирования

A'

LEOS2IP(x)

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
H*(x)

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
Новый секрет alpha и маскированные ключи должны генерироваться каждый день (UTC).   Секрет alpha и маскированные ключи рассчитываются следующим образом.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), для всех сторон:

#### Подпись

BLIND_PRIVKEY(), для владельца, публикующего leaseset:

BLIND_PUBKEY(), для клиентов, получающих leaseset:

Оба метода расчёта A' дают одинаковый результат, как и требуется.

Немаскированный leaseset подписывается немаскированным приватным ключом Ed25519 или Red25519   и проверяется с помощью немаскированного публичного ключа Ed25519 или Red25519 (типы подписи 7 или 11) как обычно.

#### Расчёты подписи/проверки

Если публичный ключ подписи оффлайн,   немаскированный leaseset подписывается немаскированным временным приватным ключом Ed25519 или Red25519   и проверяется с помощью немаскированного публичного ключа Ed25519 или Red25519 (типы подписи 7 или 11) как обычно.   См. ниже дополнительные примечания об оффлайн-ключах для зашифрованных leasesets.

Для подписи зашифрованного leaseset мы используем Red25519, основанный на [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   для подписи и проверки с маскированными ключами.   Подписи Red25519 делаются по кривой Ed25519 с использованием SHA-512 для хеширования.

Red25519 идентичен стандартному Ed25519, за исключением указанных ниже различий.

Внешняя часть зашифрованного leaseset использует ключи и подписи Red25519.

Red25519 почти идентичен Ed25519. Есть два различия:

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Приватные ключи Red25519 генерируются из случайных чисел и затем должны быть приведены по модулю L, где L определено выше.   Приватные ключи Ed25519 генерируются из случайных чисел и затем "зажимаются" с помощью   побитовой маски для байтов 0 и 31. Это не делается для Red25519.   Функции GENERATE_ALPHA() и BLIND_PRIVKEY(), определённые выше, генерируют правильные   приватные ключи Red25519 с использованием mod L.

```text
// same as in Ed25519
```
### Шифрование и обработка

#### Выведение подучреждений

В Red25519, расчёт r для подписи использует дополнительные случайные данные,   и использует значение публичного ключа вместо хеша приватного ключа.   Из-за случайных данных, каждая подпись Red25519 разная, даже   при подписании одних и тех же данных тем же ключом.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Подпись:

Проверка:

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Как часть процесса маскирования, мы должны обеспечить, чтобы зашифрованный LS2 мог быть   расшифрован только тем, кто знает публичный ключ подписи соответствующего назначения.   Полное назначение не требуется.   Для этого мы выводим учреждение из публичного ключа подписи:

#### Шифрование слоя 1

Персонализированная строка гарантирует, что учреждение не будет конфликтовать с любым хешем, используемым   в качестве ключа поиска DHT, например, с обычным хешем назначения.

```text
outerInput = subcredential || publishedTimestamp
```
Для данного маскированного ключа мы можем затем вывести подучреждение:

```text
outerSalt = CSRNG(32)
```
Подучреждение включается в процессы выработки ключей ниже, что привязывает эти   ключи к знанию публичного ключа подписи назначения.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Сначала готовится вход для процесса выработки ключа:

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Расшифрование слоя 1

Затем генерируется случайная соль:

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
Наконец, открытый текст слоя 1 шифруется и сериализуется:

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Шифрование слоя 2

Соль парсится из шифротекста слоя 1:

Затем выводится ключ, используемый для шифрования слоя 1:

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Расшифрование слоя 2

Наконец, шифротекст слоя 1 расшифровывается:

Когда авторизация клиента включена, ``authCookie`` рассчитывается, как описано ниже.   Когда авторизация клиента отключена, ``authCookie`` — это массив байтов нулевой длины.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Авторизация на уровне клиента

Шифрование продолжается аналогично слою 1:

Когда авторизация клиента включена, ``authCookie`` рассчитывается, как описано ниже.   Когда авторизация клиента отключена, ``authCookie`` — это массив байтов нулевой длины.

#### Авторизация клиента по DH

Расшифрование продолжается аналогично слою 1:

Когда авторизация клиента включена для назначения, сервер поддерживает список   клиентов, которым разрешено расшифровывать данные зашифрованного LS2. Данные, хранимые на клиента,   зависят от механизма авторизации и включают некоторую форму ключевого материала, который каждый   клиент генерирует и отправляет серверу через безопасный внеполосный механизм.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Есть два варианта реализации авторизации на уровне клиента:

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Каждый клиент генерирует пару ключей DH ``[csk_i, cpk_i]`` и отправляет публичный ключ ``cpk_i``   на сервер.

Обработка сервером ^^^^^^^^^^^^^^^^^ Сервер генерирует новый ``authCookie`` и эфемерную пару ключей DH:

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Затем для каждого авторизованного клиента сервер шифрует ``authCookie`` его публичным ключом:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Авторизация клиента по предварительно разделяемому ключу (PSK)

Сервер помещает каждую пару ``[clientID_i, clientCookie_i]`` в слой 1   зашифрованного LS2 вместе с ``epk``.

Обработка клиентом ^^^^^^^^^^^^^^^^^ Клиент использует свой приватный ключ для вывода ожидаемого идентификатора клиента ``clientID_i``,   ключа шифрования ``clientKey_i`` и IV шифрования ``clientIV_i``:

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Затем клиент ищет в данных авторизации слоя 1 запись, содержащую   ``clientID_i``. Если совпадающая запись существует, клиент расшифровывает её, чтобы получить   ``authCookie``:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Каждый клиент генерирует секретный 32-байтовый ключ ``psk_i`` и отправляет его на сервер.   В качестве альтернативы, сервер может сгенерировать секретный ключ и отправить его одному или нескольким клиентам.

Обработка сервером ^^^^^^^^^^^^^^^^^ Сервер генерирует новый ``authCookie`` и соль:

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Затем для каждого авторизованного клиента сервер шифрует ``authCookie`` его предварительно разделяемым ключом:

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Рассмотрение вопросов безопасности

Сервер помещает каждую пару ``[clientID_i, clientCookie_i]`` в слой 1   зашифрованного LS2 вместе с ``authSalt``.

Обработка клиентом ^^^^^^^^^^^^^^^^^ Клиент использует свой предварительно разделяемый ключ для вывода ожидаемого идентификатора клиента ``clientID_i``,   ключа шифрования ``clientKey_i`` и IV шифрования ``clientIV_i``:

Затем клиент ищет в данных авторизации слоя 1 запись, содержащую   ``clientID_i``. Если совпадающая запись существует, клиент расшифровывает её, чтобы получить   ``authCookie``:

Оба механизма авторизации клиента выше обеспечивают конфиденциальность членства клиентов.   Сущность, знающая только назначение, может видеть, сколько клиентов подписано в данный момент,   но не может отслеживать, какие клиенты добавляются или отзываются.

- Зашифровать всё целиком для безопасности
- Надёжно шифровать, а не только с помощью AES.
- Шифровать для каждого получателя

Серверы ДОЛЖНЫ перемешивать порядок клиентов каждый раз при генерации зашифрованного LS2, чтобы   предотвратить клиентов от определения их позиции в списке и вывода, когда другие клиенты были добавлены или отозваны.

- Внешний слой, содержащий необходимую открытую информацию для хранения и извлечения.
- Средний слой, отвечающий за аутентификацию клиента.
- Внутренний слой, содержащий фактические данные LS2.

Сервер МОЖЕТ выбрать скрытие количества подписанных клиентов, вставляя случайные записи в список данных авторизации.

- Публичный ключ подписи в немаскированном назначении должен быть  
  Ed25519 (тип подписи 7) или Red25519 (тип подписи 11);  
  другие типы подписей не поддерживаются
- Если публичный ключ подписи оффлайн, временный публичный ключ подписи также должен быть Ed25519
- Маскирование вычислительно просто
- Использование существующих криптографических примитивов
- Маскированные публичные ключи не могут быть раскрыты
- Маскированные публичные ключи должны находиться на кривой Ed25519 и в подгруппе простого порядка
- Должно быть известно публичный ключ подписи назначения  
  (полное назначение не требуется) для вывода маскированного публичного ключа
- Опционально предоставить дополнительный секрет, необходимый для вывода маскированного публичного ключа

Преимущества авторизации клиента по DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Безопасность схемы не зависит исключительно от внеполосного обмена материалом ключа клиента.  
  Приватный ключ клиента никогда не должен покидать его устройство, и поэтому злоумышленник, способный перехватить внеполосный обмен, но не способный взломать алгоритм DH, не может расшифровать зашифрованный LS2 или определить, как долго клиенту разрешён доступ.

### Зашифрованный LS с адресами Base 32

Недостатки авторизации клиента по DH ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Преимущества авторизации клиента по PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### Зашифрованный LS с оффлайн-ключами

Недостатки авторизации клиента по PSK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

См. предложение 149.

Вы не можете использовать зашифрованный LS2 для bittorrent, из-за компактных ответов announce, которые имеют 32 байта.   32 байта содержат только хеш. Нет места для указания того, что   leaseset зашифрован, или типов подписей.

### Примечания

- Требует N + 1 операций DH на стороне сервера для N клиентов.
- Требует одной операции DH на стороне клиента.
- Требует, чтобы клиент сгенерировал секретный ключ.

- Не требует операций DH.
- Позволяет серверу генерировать секретный ключ.
- Позволяет серверу делиться одним и тем же ключом с несколькими клиентами, если необходимо.

- Безопасность схемы критически зависит от внеполосного обмена материалом ключа клиента.  
  Злоумышленник, перехвативший обмен для конкретного клиента, может расшифровать любые последующие зашифрованные LS2, для которых этот клиент авторизован, а также определить, когда доступ клиента отозван.

- Сервис, использующий зашифрованные leasesets, будет публиковать зашифрованную версию на  
  floodfill-узлах. Однако, для эффективности, он будет отправлять незашифрованные leasesets клиентам в  
  обёрнутом сообщении garlic, после аутентификации (например, по белому списку).

- Floodfill-узлы могут ограничить максимальный размер разумным значением, чтобы предотвратить злоупотребления.

### Meta LS2

Для зашифрованных leasesets с оффлайн-ключами маскированные приватные ключи также должны генерироваться оффлайн,   по одному на каждый день.

Поскольку опциональный блок оффлайн-подписи находится в открытой части зашифрованного leaseset,   любой, кто сканирует floodfill-узлы, может использовать это для отслеживания leaseset (но не расшифровки)   в течение нескольких дней.   Чтобы предотвратить это, владелец ключей должен генерировать новые временные ключи   также каждый день.   И временные, и маскированные ключи могут быть сгенерированы заранее и доставлены маршрутизатору   пакетом.

В этом предложении не определён формат файла для упаковки нескольких временных и   маскированных ключей и предоставления их клиенту или маршрутизатору.   В этом предложении не определено расширение протокола I2CP для поддержки   зашифрованных leasesets с оффлайн-ключами.

Используется для замены мультихоминга. Как и любой leaseset, подписывается создателем. Это аутентифицированный список хешей назначений.

Meta LS2 является вершиной, и возможно, промежуточными узлами,   деревообразной структуры.   Он содержит несколько записей, каждая из которых указывает на LS, LS2 или другой Meta LS2   для поддержки массового мультихоминга.   Meta LS2 может содержать смесь записей LS, LS2 и Meta LS2.   Листья дерева всегда являются LS или LS2.   Дерево является DAG; циклы запрещены; клиенты, выполняющие поиск, должны обнаруживать и   отказываться следовать по циклам.

Meta LS2 может иметь гораздо более длительный срок истечения, чем стандартный LS или LS2.   Верхний уровень может иметь срок истечения на несколько часов после даты публикации.   Максимальное время истечения будет обеспечиваться floodfill-узлами и клиентами, и определяется позже.

Использование Meta LS2 — это массовый мультихоминг, но без дополнительной   защиты от корреляции маршрутизаторов с leasesets (во время перезагрузки маршрутизатора), чем   предоставляется сейчас с LS или LS2.   Это эквивалентно "facebook" сценарию, которому, вероятно, не нужна   защита от корреляции. Этот сценарий, вероятно, нуждается в оффлайн-ключах,   которые предоставляются в стандартном заголовке на каждом узле дерева.

Протокол бэкенда для координации между маршрутизаторами-листьями, промежуточными и главными подписантами Meta LS   здесь не указан. Требования крайне просты — просто проверить, что пир работает,   и публиковать новый LS каждые несколько часов. Единственная сложность — выбор новых   публикователей для верхнего или промежуточного уровня Meta LS при сбое.

Смешанные leasesets, где лизы от нескольких маршрутизаторов объединяются, подписываются и публикуются   в одном leaseset, документируются в предложении 140, "невидимый мультихоминг".   Это предложение неприемлемо в написанном виде, потому что потоковые соединения не будут   "прилипать" к одному маршрутизатору, см. http://zzz.i2p/topics/2335 .

Протокол бэкенда и взаимодействие с внутренними компонентами маршрутизатора и клиента были бы   довольно сложными для невидимого мультихоминга.

    Standard LS flag (1)
Чтобы избежать перегрузки floodfill-узла для верхнего уровня Meta LS, срок истечения должен   быть не менее нескольких часов. Клиенты должны кэшировать верхний уровень Meta LS и сохранять   его между перезагрузками, если он не истёк.

    Meta LS2 type (7)
Нам нужно определить алгоритм для клиентов, чтобы обходить дерево, включая резервные варианты,   чтобы использование было распределено. Некоторая функция от хеш-расстояния, стоимости и случайности.   Если узел имеет и LS/LS2, и Meta LS, нам нужно знать, когда разрешено   использовать эти leasesets, а когда продолжать обход дерева.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Поиск с помощью

    Hours. Max 18.2 hours (65535 seconds)
Хранение с помощью

    "master" Destination or coordinator, or intermediate coordinators

### Формат

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
Хранение в

### Примечания

- После расшифровки следует выполнить несколько проверок, включая соответствие  
  внутренней временной метки и срока истечения тем, что на верхнем уровне.

- ChaCha20 был выбран вместо AES. Хотя скорости схожи при наличии аппаратной поддержки AES,  
  ChaCha20 в 2,5-3 раза быстрее, когда аппаратная поддержка AES отсутствует, например, на недорогих ARM-устройствах.

- Нам недостаточно важно быстродействие, чтобы использовать ключевой BLAKE2b. Он имеет достаточный размер выхода, чтобы вместить наибольшее n, которое нам нужно (или мы можем вызывать его один раз для каждого желаемого ключа с аргументом счётчика). BLAKE2b намного быстрее SHA-256, и  
  ключевой BLAKE2b сократил бы общее количество вызовов хеш-функции.  
  Однако, см. предложение 148, где предлагается перейти на BLAKE2b по другим причинам.  
  См. [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Запись службы

Типичное истечение

Публикуется

Флаги и свойства: для будущего использования

    n/a, see Service List
Типы 3, 7 и 9 используют стандартный заголовок LS2, определённый ниже:

    Service Record type (9)
Изменения по сравнению с существующим LeaseSet:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Поиск с помощью

    Hours. Max 18.2 hours (65535 seconds)
Хранение с помощью

    Destination

### Формат

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Примечания

- Рас

- Хранение: floodfill может строго ограничивать хранение этих записей и
  ограничивать количество записей, хранимых на один хэш, и срок их хранения. Также может
  использоваться белый список хэшей.

- Любой другой тип netdb с тем же хешем имеет приоритет, поэтому запись сервиса никогда не может
  перезаписать LS/RI, но LS/RI перезапишет все записи сервиса с этим хешем.

### Список сервисов

Это совсем не похоже на LS2 и использует другой формат.

Список сервисов создаётся и подписывается floodfill. Он неаутентифицирован в том смысле, что любой может присоединиться к сервису, опубликовав Service Record на floodfill.

Service List содержит Short Service Records, а не полные Service Records. Они содержат подписи, но только хэши, а не полные destination, поэтому их нельзя проверить без полного destination.

Безопасность (если таковая имеется) и целесообразность списков сервисов пока не определены. Floodfill могут ограничивать публикацию и поиск белым списком сервисов, но этот белый список может различаться в зависимости от реализации или предпочтений оператора. Возможно, не удастся достичь консенсуса относительно общего базового белого списка для всех реализаций.

Если имя службы включено в указанную выше запись службы, то операторы floodfill могут возразить; если включён только хеш, проверки нет, и запись службы может «попасть» раньше любого другого типа netdb и быть сохранена в floodfill.

TBD

    Service List lookup type (11)
Типы 3, 7 и 9 используют стандартный заголовок LS2, определённый ниже:

    Service List type (11)
Изменения по сравнению с существующим LeaseSet:

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Поиск с помощью

    Hours, not specified in the list itself, up to local policy
Хранение с помощью

    Nobody, never sent to floodfill, never flooded.

### Формат

Формат зашифрованного LS2 состоит из трёх вложенных слоёв:

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
Для проверки подписи списка сервисов:

- добавить хеш имени сервиса в начало
- удалить хеш создателя
- Проверить подпись изменённого содержимого

Для проверки подписи каждой Short Service Record:

- Получить destination
- Проверить подпись (published timestamp + expires + flags + port + Hash имени сервиса)

Для проверки подписи каждой Revocation Record:

- Получить destination
- Проверить подпись для (published timestamp + 4 нулевых байта + flags + port + Hash имени службы)

### Примечания

- Используется длина подписи вместо типа sig, чтобы поддерживать неизвестные
  типы подписей.

- У списка услуг нет срока действия; получатели могут принимать решения самостоятельно на основе политики или истечения срока действия отдельных записей.

- Списки сервисов не флудятся, флудятся только отдельные записи сервисов. Каждый
  floodfill создаёт, подписывает и кэширует список сервисов. Floodfill использует свою
  собственную политику для времени кэширования и максимального числа записей сервисов и отзывов.

## Требуемые изменения в спецификации Common Structures

### Сертификаты ключей

Вне рамок этого предложения. Следует добавить в предложения по ECIES 144 и 145.

### Новые промежуточные структуры

Добавлены новые структуры для Lease2, MetaLease, LeaseSet2Header и OfflineSignature. Вступает в силу с релиза 0.9.38.

### Новые типы NetDB

Добавить структуры для каждого нового типа leaseset, включённые в приведённый выше текст. Для LeaseSet2, EncryptedLeaseSet и MetaLeaseSet — действует начиная с релиза 0.9.38. Для Service Record и Service List — предварительно и без запланированного срока.

### Новый тип подписи

Добавить RedDSA_SHA512_Ed25519 Type 11. Публичный ключ — 32 байта; приватный ключ — 32 байта; хеш — 64 байта; подпись — 64 байта.

## Необходимые изменения спецификации шифрования

Вне рамок этого предложения. См. предложения 144 и 145.

## Требуемые изменения I2NP

Добавить примечание: LS2 можно публиковать только на floodfill с минимальной версией.

### Сообщение поиска в базе данных

Добавить тип поиска по списку сервисов.

### Изменения

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Сообщение Database Store

Добавьте все новые типы хранилищ.

### Изменения

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
## Требуемые изменения I2CP

### Параметры I2CP

Новые параметры, интерпретируемые на стороне router и передаваемые в SessionConfig Mapping:

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
### Конфигурация сессии

Обратите внимание, что для offline-подписей требуются параметры i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey и i2cp.leaseSetOfflineSignature, а подпись создаётся временным закрытым ключом подписи.

### Сообщение запроса leaseSet

От router к клиенту. Без изменений. Leases передаются с 8-байтовыми временными метками, даже если возвращаемый leaseset будет LS2 с 4-байтовыми временными метками. Обратите внимание, что ответом может быть сообщение Create Leaseset или Create Leaseset2.

### Сообщение запроса переменного leaseSet

От router к клиенту. Без изменений. Leases передаются с 8-байтовыми временными метками, даже если возвращаемый leaseset будет LS2 с 4-байтовыми временными метками. Обратите внимание, что ответом может быть сообщение Create Leaseset или Create Leaseset2.

### Создание сообщения Leaseset2

От клиента к router. Новое сообщение, используемое вместо Create Leaseset Message.

### Обоснование

- Чтобы router мог разобрать store type, тип должен присутствовать в сообщении, если только он не был передан router заранее в конфигурации сессии. Для общего кода разбора проще, когда он находится в самом сообщении.

- Чтобы router знал тип и длину закрытого ключа, ключ должен располагаться после lease set, если только парсер не знает тип заранее из конфигурации сессии. Для общего кода парсинга проще определять его из самого сообщения.

- Закрытый ключ подписи, ранее определённый для отзыва и не использовавшийся, отсутствует в LS2.

### Тип сообщения

Тип сообщения для Create Leaseset2 Message — 41.

### Формат

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
### Примечания

- Минимальная версия router — 0.9.39.
- Предварительная версия с типом сообщения 40 была в 0.9.38, но формат был изменён.
  Тип 40 заброшен и не поддерживается.

### Проблемы

- Для поддержки зашифрованных и meta LS требуется больше изменений.

### Сообщение с информацией о blinding

От клиента к router. Новое сообщение.

### Обоснование

- Router должен знать, является ли destination blinded.
  Если destination blinded и использует секретную аутентификацию или аутентификацию для каждого клиента,
  ему также нужна эта информация.

- Выполнение Host Lookup для b32-адреса нового формата («b33»)
  сообщает router о том, что адрес является blinded, но в сообщении Host Lookup
  нет механизма передачи секретного или приватного ключа router.
  Хотя можно было бы расширить сообщение Host Lookup, добавив эту информацию,
  чище определить новое сообщение.

- Нам нужен программный способ, позволяющий клиенту сообщить router.
  Иначе пользователю пришлось бы вручную настраивать каждый destination.

### Использование

Прежде чем клиент отправит сообщение на blinded destination, он должен либо найти "b33" с помощью сообщения Host Lookup, либо отправить сообщение Blinding Info. Если для blinded destination требуется секрет или аутентификация для каждого клиента, клиент обязан отправить сообщение Blinding Info.

router не отправляет ответ на это сообщение.

### Тип сообщения

Тип сообщения Blinding Info Message — 42.

### Формат

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
### Примечания

- Минимальная версия router — 0.9.43

### Проблемы

### Сообщение ответа хоста (enc)

Для поддержки поиска хостовых имён "b33" и возврата указания на то, что у router нет требуемой информации, мы определяем дополнительные коды результата для Host Reply Message следующим образом:

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Значения 1-255 уже определены как ошибки, поэтому проблемы с обратной совместимостью нет.

### Сообщение мета-перенаправления

От router к клиенту. Новое сообщение.

### Обоснование

Клиент заранее не знает, что данный хэш будет разрешаться в Meta LS.

Если поиск leaseSet для Destination возвращает Meta LS, router выполнит рекурсивное разрешение. Для датаграмм клиентской стороне знать это не требуется; однако для streaming, где протокол проверяет Destination в SYN ACK, необходимо знать, каким является «реальный» Destination. Поэтому нам нужно новое сообщение.

### Использование

Router поддерживает кеш фактического destination, используемого из meta LS. Когда клиент отправляет сообщение на destination, который разрешается в meta LS, router проверяет кеш на предмет последнего использованного фактического destination. Если кеш пуст, router выбирает destination из meta LS и выполняет поиск leaseset. Если поиск leaseset успешен, router добавляет этот destination в кеш и отправляет клиенту Meta Redirect Message. Это делается только один раз, если только destination не истечёт и его не потребуется изменить. Клиент также должен кешировать информацию при необходимости. Meta Redirect Message НЕ отправляется в ответ на каждое SendMessage.

Router отправляет это сообщение только клиентам с версией 0.9.47 или выше.

Клиент не отправляет ответ на это сообщение.

### Тип сообщения

Тип сообщения для Meta Redirect Message — 43.

### Формат

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
### Изменения для поддержки Meta

Как генерировать Meta и обеспечивать её поддержку, включая взаимодействие и координацию между router'ами, выходит за рамки данного предложения. См. связанное предложение 150.

### Изменения для поддержки Offline Keys

Офлайн-подписи невозможно проверить в streaming или в датаграммах с возможностью ответа. См. разделы ниже.

## Требуются изменения в файле закрытого ключа

Формат файла приватного ключа (eepPriv.dat) не является официальной частью наших спецификаций, но он описан в [Java I2P javadocs](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html), и другие реализации его поддерживают. Это обеспечивает переносимость приватных ключей между разными реализациями.

Необходимы изменения для хранения временного открытого ключа и информации об офлайн-подписи.

### Изменения

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
### Требуемые изменения CLI для файла приватного ключа

Добавить поддержку следующих параметров:

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Требуемые изменения потоковой передачи

Офлайн-подписи сейчас невозможно проверить в потоковом режиме. Приведённое ниже изменение добавляет блок офлайн-подписи в параметры. Это избавляет от необходимости получать эту информацию через I2CP.

### Изменения

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
### Примечания

- Альтернатива — просто добавить флаг и получить временный открытый ключ через I2CP
  (См. разделы Host Lookup / Host Reply Message выше)

## Необходимые изменения Repliable Datagram

Офлайн-подписи невозможно проверить при обработке repliable datagram. Нужен флаг, указывающий на офлайн-подпись, но нет места, куда его поместить. Потребуется полностью новый номер протокола и формат.

### Изменения

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
### Примечания

- Альтернатива — просто добавить флаг и получить временный открытый ключ через I2CP
  (см. разделы Host Lookup / Host Reply Message выше)
- Какие ещё опции следует добавить теперь, когда у нас есть байты флагов?

## Требуемые изменения в SAM V3

SAM должен быть доработан для поддержки офлайн-подписей в DESTINATION base 64.

### Изменения

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
Обратите внимание, что offline-подписи поддерживаются только для STREAM и RAW, но не для DATAGRAM (пока не будет определён новый протокол DATAGRAM).

Обратите внимание, что SESSION STATUS вернёт Signing Private Key, состоящий из всех нулей, и данные Offline Signature ровно в том виде, в каком они были переданы в SESSION CREATE.

Обратите внимание, что DEST GENERATE и SESSION CREATE DESTINATION=TRANSIENT не могут использоваться для создания офлайн-подписанного destination.

### Проблемы

Обновить версию до 3.4 или оставить на 3.1/3.2/3.3, чтобы можно было добавить без необходимости всего из 3.2/3.3?

Прочие изменения будут определены позже. См. раздел I2CP Host Reply Message выше.

## Изменения, необходимые BOB

BOB потребовалось бы доработать для поддержки offline-подписей и/или Meta LS. Это низкий приоритет, и, вероятно, это никогда не будет описано в спецификации или реализовано. Предпочтительным интерфейсом является SAM V3.

## Публикация, миграция, совместимость

LS2 (кроме зашифрованного LS2) публикуется в том же месте DHT, что и LS1. Невозможно опубликовать одновременно LS1 и LS2, если только LS2 не находится в другом месте.

Зашифрованный LS2 публикуется по хешу зашифрованного типа ключа и данных ключа. Этот хеш затем используется для генерации ежедневного "routing key", как в LS1.

LS2 будет использоваться только при необходимости новых функций (новая криптография, зашифрованный LS, meta и т.д.). LS2 можно публиковать только на floodfill указанной версии или выше.

Серверы, публикующие LS2, знали бы, что любые подключающиеся клиенты поддерживают LS2. Они могли бы отправлять LS2 в garlic.

Клиенты отправляли бы LS2 в garlic только при использовании новой криптографии. Общие клиенты использовали бы LS1 неограниченно долго? TODO: как сделать общих клиентов, поддерживающих как старую, так и новую криптографию?

## Развёртывание

В версии 0.9.38 реализована поддержка floodfill для стандартного LS2, включая офлайн-ключи.

0.9.39 содержит поддержку I2CP для LS2 и Encrypted LS2, подписывание/проверку sig type 11, поддержку floodfill для Encrypted LS2 (sig types 7 и 11, без offline keys), а также шифрование/расшифровку LS2 (без per-client authorization).

В версии 0.9.40 планируется поддержка шифрования/расшифровки LS2 с авторизацией для каждого клиента, поддержка floodfill и I2CP для Meta LS2, поддержка зашифрованных LS2 с офлайн-ключами, а также поддержка b32 для зашифрованных LS2.

## Благодарности

На дизайн зашифрованного LS2 большое влияние оказали [дескрипторы скрытых сервисов v3 в Tor](https://spec.torproject.org/rend-spec-v3), имевшие схожие цели проектирования.

## Ссылки

* [«Высокоскоростные высоконадёжные подписи» — Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe и Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
