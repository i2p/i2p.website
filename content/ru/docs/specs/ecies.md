---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Схема интегрированного шифрования на эллиптических кривых для сквозного шифрования I2P"
slug: "ecies"
aliases:
  - "/ru/docs/specs/ecies-x25519-aead-ratchet"
  - "/ru/docs/specs/ecies-x25519-aead-ratchet/"
category: "Протоколы"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Примечание

Развертывание сети завершено. Возможны незначительные изменения. См. [Prop144](/proposals/144-ecies-x25519/) для ознакомления с исходным предложением, включая обсуждение предпосылок и дополнительную информацию.

Следующие функции не реализованы по состоянию на версию 0.9.66:

- Блоки MessageNumbers, Options и Termination
- Ответы на уровне протокола
- Нулевой статический ключ
- Многоадресная рассылка

Для версии MLKEM PQ Hybrid этого протокола см. [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Обзор

Это новый протокол сквозного шифрования для замены ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Основывается на предыдущих работах следующим образом:

- Спецификация общих структур [Common](/docs/specs/common-structures/)
- Спецификация [I2NP](/docs/specs/i2np/) включая LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> обзор новой асимметричной криптографии
- Низкоуровневый обзор криптографии [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Новые записи netDb
- 142 Новый криптографический шаблон
- Протокол [Noise](https://noiseprotocol.org/noise.html)
- Алгоритм двойного трещотки [Signal](https://signal.org/docs/specifications/doubleratchet/)

Он поддерживает новое шифрование для сквозной связи между destination и destination.

Дизайн использует рукопожатие Noise и фазу данных, включающую двойной ratchet от Signal.

Все ссылки на Signal и Noise в данной спецификации приведены исключительно для справочной информации. Знание протоколов Signal и Noise не требуется для понимания или реализации данной спецификации.

Данная спецификация поддерживается начиная с версии 0.9.46.

## Спецификация

Дизайн использует рукопожатие Noise и фазу данных, включающую двойной ratchet от Signal.

### Обзор криптографического дизайна

Существует пять частей протокола, которые необходимо переработать:

- 1\) Форматы контейнеров новых и существующих сессий заменяются на
  новые форматы.
- 2\) ElGamal (открытые ключи 256 байт, закрытые ключи 128 байт)
  заменяется на ECIES-X25519 (открытые и закрытые ключи по 32 байта)
- 3\) AES заменяется на AEAD_ChaCha20_Poly1305 (сокращенно
  ChaChaPoly ниже)
- 4\) SessionTags будут заменены на ratchets (храповики), которые по сути являются
  криптографическими синхронизированными PRNG.
- 5\) Полезная нагрузка AES, как определено в спецификации
  ElGamal/AES+SessionTags, заменяется на блочный формат, аналогичный
  используемому в NTCP2.

Каждое из пяти изменений имеет свой раздел ниже.

### Тип шифрования

Тип шифрования (используемый в LS2) равен 4. Это указывает на 32-байтовый открытый ключ X25519 в формате little-endian и сквозной протокол, описанный здесь.

Тип шифрования 0 — это ElGamal. Типы шифрования 1-3 зарезервированы для ECIES-ECDH-AES-SessionTag, см. предложение 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Фреймворк протокола Noise

Этот протокол предоставляет требования на основе Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Редакция 34, 2018-07-11). Noise имеет схожие свойства с протоколом Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), который является основой для протокола [SSU](/docs/transport/ssu/). В терминологии Noise, Алиса является инициатором, а Боб — отвечающей стороной.

Данная спецификация основана на протоколе Noise Noise_IK_25519_ChaChaPoly_SHA256. (Фактический идентификатор для начальной функции выведения ключей - "Noise_IKelg2_25519_ChaChaPoly_SHA256" для обозначения расширений I2P - см. раздел KDF 1 ниже) Этот протокол Noise использует следующие примитивы:

- Interactive Handshake Pattern: IK Алиса немедленно передает свой
  статический ключ Бобу (I) Алиса уже знает статический ключ Боба (K)
- One-Way Handshake Pattern: N Алиса не передает свой статический ключ
  Бобу (N)
- DH Function: X25519 X25519 DH с длиной ключа 32 байта, как
  указано в [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Cipher Function: ChaChaPoly AEAD_CHACHA20_POLY1305, как указано в
  [RFC-7539](https://tools.ietf.org/html/rfc7539) раздел 2.8. 12-байтовый nonce, с
  первыми 4 байтами, установленными в ноль. Идентично тому, что используется в
  [NTCP2](/docs/specs/ntcp2/).
- Hash Function: SHA256 Стандартный 32-байтовый хеш, уже широко используемый
  в I2P.

#### Дополнения к Framework

Данная спецификация определяет следующие усовершенствования для Noise_IK_25519_ChaChaPoly_SHA256. В целом они следуют рекомендациям из раздела 13 [NOISE](https://noiseprotocol.org/noise.html).

1)  Открытые эфемерные ключи кодируются с помощью

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) Ответ имеет префикс в виде открытого тега. 3) Формат полезной нагрузки определен для сообщений 1, 2 и фазы данных.

    Of course, this is not defined in Noise.

Все сообщения включают заголовок [I2NP](/docs/specs/i2np/) Garlic Message. Фаза данных использует шифрование, похожее на фазу данных Noise, но не совместимое с ней.

### Шаблоны рукопожатий

Рукопожатия используют шаблоны рукопожатий [Noise](https://noiseprotocol.org/noise.html).

Используется следующее соответствие букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения

Одноразовые и несвязанные сессии похожи на паттерн Noise N.

```
<- s
...
e es p ->
```
Связанные сессии похожи на паттерн Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Свойства безопасности

Используя терминологию Noise, последовательность установления соединения и передачи данных следующая: (Свойства безопасности полезной нагрузки из [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Отличия от XK

IK рукопожатия имеют несколько отличий от XK рукопожатий, используемых в [NTCP2](/docs/specs/ntcp2/) и [SSU2](/docs/specs/ssu2/).

- Четыре операции DH всего по сравнению с тремя для XK
- Аутентификация отправителя в первом сообщении: Полезная нагрузка аутентифицируется
  как принадлежащая владельцу публичного ключа отправителя, хотя
  ключ мог быть скомпрометирован (Аутентификация 1). XK требует еще один
  круговой обход прежде чем Алиса будет аутентифицирована.
- Полная прямая секретность (Конфиденциальность 5) после второго сообщения. Боб
  может отправить полезную нагрузку сразу после второго сообщения с полной
  прямой секретностью. XK требует еще один круговой обход для полной прямой
  секретности.

В итоге, IK позволяет доставить полезную нагрузку ответа от Боба к Алисе за 1-RTT с полной прямой секретностью, однако полезная нагрузка запроса не обладает прямой секретностью.

### Сессии

Протокол ElGamal/AES+SessionTag является однонаправленным. На этом уровне получатель не знает, откуда пришло сообщение. Исходящие и входящие сессии не связаны между собой. Подтверждения передаются по внеполосному каналу с использованием DeliveryStatusMessage (обернутого в GarlicMessage) в clove.

Для данной спецификации мы определяем два механизма для создания двунаправленного протокола - "сопряжение" и "привязка". Эти механизмы обеспечивают повышенную эффективность и безопасность.

#### Контекст сессии

Как и в случае с ElGamal/AES+SessionTags, все входящие и исходящие сессии должны находиться в определенном контексте — либо в контексте router'а, либо в контексте конкретного локального назначения. В Java I2P этот контекст называется Session Key Manager.

Сессии не должны разделяться между контекстами, поскольку это позволило бы установить корреляцию между различными локальными назначениями или между локальным назначением и router.

Когда данное назначение поддерживает как ElGamal/AES+SessionTags, так и данную спецификацию, оба типа сессий могут использовать общий контекст. См. раздел 1c) ниже.

#### Сопряжение входящих и исходящих сессий

Когда исходящая сессия создается у инициатора (Alice), создается новая входящая сессия и связывается с исходящей сессией, если только не ожидается ответа (например, необработанные датаграммы).

Новая входящая сессия всегда связывается с новой исходящей сессией, за исключением случаев, когда ответ не требуется (например, для сырых датаграмм).

Если запрашивается ответ и он привязан к удаленному назначению или router, то эта новая исходящая сессия привязывается к этому назначению или router и заменяет любую предыдущую исходящую сессию к этому назначению или router.

Связывание входящих и исходящих сессий обеспечивает двунаправленный протокол с возможностью ротации DH ключей.

#### Привязка сессий и назначений

Существует только одна исходящая сессия к определенному пункту назначения или router. Может быть несколько текущих входящих сессий от определенного пункта назначения или router. Как правило, когда создается новая входящая сессия и на этой сессии получен трафик (который служит подтверждением ACK), любые другие сессии будут помечены для истечения относительно быстро, в течение минуты или около того. Проверяется значение предыдущих отправленных сообщений (PN), и если в предыдущей входящей сессии нет неполученных сообщений (в пределах размера окна), предыдущая сессия может быть удалена немедленно.

Когда исходящая сессия создается у инициатора (Алиса), она привязывается к удаленному Destination (Боб), и любая парная входящая сессия также будет привязана к удаленному Destination. По мере того как сессии продвигаются (ratchet), они продолжают оставаться привязанными к удаленному Destination.

Когда входящая сессия создается у получателя (Bob), она может быть привязана к удаленному назначению (Alice) по выбору Alice. Если Alice включает информацию о привязке (свой статический ключ) в сообщение New Session, сессия будет привязана к этому назначению, и будет создана исходящая сессия, привязанная к тому же назначению. По мере развития сессий через ratchet, они продолжают оставаться привязанными к удаленному назначению.

#### Преимущества привязки и сопряжения

Для обычного случая потоковой передачи мы ожидаем, что Алиса и Боб будут использовать протокол следующим образом:

- Алиса связывает свою новую исходящую сессию с новой входящей сессией, обе
  привязанные к удаленному адресату (Бобу).
- Алиса включает информацию о привязке и подпись, а также запрос ответа,
  в сообщение New Session, отправленное Бобу.
- Боб связывает свою новую входящую сессию с новой исходящей сессией, обе
  привязанные к удаленному адресату (Алисе).
- Боб отправляет ответ (подтверждение) Алисе в связанной сессии, с ratchet
  к новому DH ключу.
- Алиса выполняет ratchet к новой исходящей сессии с новым ключом Боба, связанной
  с существующей входящей сессией.

Привязывая входящую сессию к удаленному Destination и соединяя входящую сессию с исходящей сессией, привязанной к тому же Destination, мы получаем два основных преимущества:

1)  Первоначальный ответ от Боба к Алисе использует ephemeral-ephemeral DH

2) После того как Алиса получает ответ Боба и выполняет ratchet, все последующие сообщения от Алисы к Бобу используют эфемерный-эфемерный DH.

#### Подтверждения сообщений (ACK)

В ElGamal/AES+SessionTags, когда LeaseSet объединяется как garlic clove, или доставляются теги, отправляющий router запрашивает ACK. Это отдельный garlic clove, содержащий сообщение DeliveryStatus. Для дополнительной безопасности сообщение DeliveryStatus оборачивается в Garlic Message. Этот механизм является внеполосным с точки зрения протокола.

В новом протоколе, поскольку входящие и исходящие сессии связаны в пары, мы можем иметь ACK внутри полосы. Отдельный clove не требуется.

Явное подтверждение ACK — это просто сообщение Existing Session без блока I2NP. Однако в большинстве случаев явного ACK можно избежать, поскольку есть обратный трафик. Для реализаций может быть желательно подождать короткое время (возможно, сто миллисекунд) перед отправкой явного ACK, чтобы дать streaming или прикладному слою время для ответа.

Реализации также должны будут отложить отправку любого ACK до тех пор, пока не будет обработан блок I2NP, поскольку Garlic Message может содержать Database Store Message с lease set. Актуальный lease set будет необходим для маршрутизации ACK, а удаленный пункт назначения (содержащийся в lease set) будет необходим для проверки привязанного статического ключа.

#### Таймауты сессий

Исходящие сессии должны всегда истекать раньше входящих сессий. Когда исходящая сессия истекает и создается новая, также будет создана новая парная входящая сессия. Если была старая входящая сессия, ей будет позволено истечь.

### Многоадресная рассылка

Будет определено позже

### Определения

Мы определяем следующие функции, соответствующие используемым криптографическим строительным блокам.

ZEROLEN

байтовый массив нулевой длины

CSRNG(n)

n-байтовый вывод из криптографически стойкого генератора случайных чисел

    generator.

H(p, d)

Хеш-функция SHA-256, которая принимает строку персонализации p и данные

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Хеш-функция SHA-256, которая принимает предыдущий хеш h и новые данные d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

AEAD ChaCha20/Poly1305, как указано в

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Система согласования открытых ключей X25519. Закрытые ключи размером 32 байта, открытые

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Криптографическая функция выведения ключа, которая принимает некоторый входной ключ

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Используйте HKDF() с предыдущим chainKey и новыми данными d, и установите новый

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Формат сообщения

#### Обзор текущего формата сообщений

Garlic Message, как указано в [I2NP](/docs/specs/i2np/), выглядит следующим образом. Поскольку целью дизайна является то, что промежуточные узлы не могут отличить новую криптографию от старой, этот формат не может изменяться, даже если поле длины является избыточным. Формат показан с полным 16-байтовым заголовком, хотя фактический заголовок может быть в другом формате, в зависимости от используемого транспорта.

После расшифровки данные содержат серию Garlic Cloves и дополнительные данные, также известные как Clove Set.

См. [I2NP](/docs/specs/i2np/) для подробностей и полной спецификации.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Обзор формата зашифрованных данных

В ElGamal/AES+SessionTags существует два формата сообщений:

1\) Новая сессия: - 514-байтовый блок ElGamal - блок AES (минимум 128 байт, кратный 16)

2\) Существующая сессия: - 32 байта Session Tag - блок AES (минимум 128 байт, кратно 16)

Эти сообщения инкапсулируются в I2NP garlic message, которое содержит поле длины, поэтому длина известна.

Получатель сначала пытается найти первые 32 байта как Session Tag. Если найден, он расшифровывает блок AES. Если не найден, и данные имеют длину не менее (514+16), он пытается расшифровать блок ElGamal, и если это удается, расшифровывает блок AES.

#### Новые теги сессий и сравнение с Signal

В Signal Double Ratchet заголовок содержит:

- DH: Текущий открытый ключ ratchet
- PN: Длина сообщения предыдущей цепочки
- N: Номер сообщения

«Цепочки отправки» Signal примерно эквивалентны нашим наборам тегов. Используя тег сессии, мы можем исключить большую часть этого.

В New Session мы помещаем только публичный ключ в незашифрованный заголовок.

В существующей сессии мы используем тег сессии для заголовка. Тег сессии связан с текущим публичным ключом ratchet и номером сообщения.

В новых и существующих сессиях PN и N находятся в зашифрованном теле.

В Signal происходит постоянное переключение ключей. Новый публичный ключ DH требует от получателя переключения и отправки нового публичного ключа обратно, что также служит подтверждением получения публичного ключа. Для нас это было бы слишком много операций DH. Поэтому мы разделяем подтверждение полученного ключа и передачу нового публичного ключа. Любое сообщение, использующее тег сессии, сгенерированный из нового публичного ключа DH, является подтверждением. Мы передаем новый публичный ключ только тогда, когда хотим сменить ключ.

Максимальное количество сообщений до того, как DH должен выполнить ratchet, составляет 65535.

При доставке сеансового ключа мы выводим "Набор тегов" из него, вместо того чтобы также доставлять теги сессии. Набор тегов может содержать до 65536 тегов. Однако получатели должны реализовать стратегию "упреждающего просмотра", а не генерировать все возможные теги сразу. Генерируйте не более N тегов после последнего корректно полученного тега. N может составлять максимум 128, но 32 или даже меньше может быть лучшим выбором.

### 1a) Новый формат сессии

Новый одноразовый публичный ключ сессии (32 байта) Зашифрованные данные и MAC (остальные байты)

Сообщение New Session может содержать или не содержать статический публичный ключ отправителя. Если он включен, обратная сессия привязывается к этому ключу. Статический ключ следует включать, если ожидаются ответы, то есть для потоковой передачи и датаграмм с возможностью ответа. Его не следует включать для обычных датаграмм.

Сообщение New Session похоже на односторонний Noise [NOISE](https://noiseprotocol.org/noise.html) паттерн "N" (если статический ключ не отправляется) или двусторонний паттерн "IK" (если статический ключ отправляется).

### 1b) Новый формат сессии (с привязкой)

Длина составляет 96 + длина полезной нагрузки. Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key                    +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Новый эфемерный ключ сессии

Эфемерный ключ имеет длину 32 байта и кодируется с помощью Elligator2. Этот ключ никогда не используется повторно; новый ключ генерируется для каждого сообщения, включая повторные передачи.

#### Статический ключ

После расшифровки, статический ключ X25519 Алисы, 32 байта.

#### Полезная нагрузка

Зашифрованная длина - это оставшаяся часть данных. Расшифрованная длина на 16 меньше зашифрованной длины. Полезная нагрузка должна содержать блок DateTime и обычно содержит один или несколько блоков Garlic Clove. См. раздел полезной нагрузки ниже для формата и дополнительных требований.

### 1c) Новый формат сессии (без привязки)

Если ответ не требуется, статический ключ не отправляется.

Длина составляет 96 + длина полезной нагрузки. Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Новый эфемерный ключ сессии

Эфемерный ключ Алисы. Эфемерный ключ составляет 32 байта, закодирован с помощью Elligator2, little endian. Этот ключ никогда не используется повторно; новый ключ генерируется для каждого сообщения, включая повторные передачи.

#### Секция флагов Расшифрованные данные

Секция Flags не содержит ничего. Она всегда составляет 32 байта, поскольку должна быть той же длины, что и статический ключ для сообщений New Session с привязкой. Bob определяет, является ли это статическим ключом или секцией flags, проверяя, являются ли все 32 байта нулевыми.

TODO нужны ли здесь какие-либо флаги?

#### Полезная нагрузка

Зашифрованная длина — это оставшаяся часть данных. Расшифрованная длина на 16 меньше зашифрованной длины. Полезная нагрузка должна содержать блок DateTime и обычно будет содержать один или несколько блоков Garlic Clove. См. раздел полезной нагрузки ниже для формата и дополнительных требований.

### 1d) Одноразовый формат (без привязки или сессии)

Если ожидается отправка только одного сообщения, настройка сессии или статический ключ не требуются.

Длина составляет 96 + длина полезной нагрузки. Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Новый одноразовый ключ сессии

Одноразовый ключ имеет длину 32 байта, закодирован с помощью Elligator2, little endian. Этот ключ никогда не используется повторно; новый ключ генерируется для каждого сообщения, включая повторные передачи.

#### Раздел флагов Расшифрованные данные

Раздел Flags не содержит ничего. Он всегда составляет 32 байта, поскольку должен иметь такую же длину, как статический ключ для сообщений New Session с привязкой. Bob определяет, является ли это статическим ключом или разделом flags, проверяя, все ли 32 байта равны нулю.

TODO нужны ли здесь какие-либо флаги?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Полезная нагрузка

Зашифрованная длина — это оставшаяся часть данных. Расшифрованная длина на 16 байт меньше зашифрованной длины. Полезная нагрузка должна содержать блок DateTime и обычно содержит один или несколько блоков Garlic Clove. См. раздел полезной нагрузки ниже для формата и дополнительных требований.

### 1f) KDF для сообщения новой сессии

#### KDF для начального ChainKey

Это стандартный [NOISE](https://noiseprotocol.org/noise.html) для IK с модифицированным именем протокола. Обратите внимание, что мы используем один и тот же инициализатор как для паттерна IK (привязанные сессии), так и для паттерна N (непривязанные сессии).

Название протокола изменено по двум причинам. Во-первых, чтобы указать, что эфемерные ключи кодируются с помощью Elligator2, и во-вторых, чтобы указать, что MixHash() вызывается перед вторым сообщением для смешивания значения тега.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF для зашифрованного содержимого раздела флагов/статического ключа

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF для секции полезной нагрузки (со статическим ключом Alice)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF для секции полезной нагрузки (без статического ключа Alice)

Обратите внимание, что это шаблон Noise "N", но мы используем тот же инициализатор "IK", что и для связанных сессий.

Сообщения New Session не могут быть идентифицированы как содержащие статический ключ Алисы или нет, пока статический ключ не будет расшифрован и проверен на предмет того, содержит ли он все нули. Поэтому получатель должен использовать конечный автомат "IK" для всех сообщений New Session. Если статический ключ состоит из всех нулей, шаблон сообщения "ss" должен быть пропущен.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Формат ответа на новую сессию

В ответ на одно сообщение New Session может быть отправлено один или несколько ответов New Session Reply. Каждый ответ предваряется тегом, который генерируется из TagSet для сессии.

Ответ на новую сессию состоит из двух частей. Первая часть представляет собой завершение рукопожатия Noise IK с добавленным в начале тегом. Длина первой части составляет 56 байт. Вторая часть представляет собой полезную нагрузку фазы данных. Длина второй части составляет 16 + длина полезной нагрузки.

Общая длина составляет 72 + длина полезной нагрузки. Зашифрованный формат:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Тег сессии

Тег генерируется в KDF сессионных тегов, как инициализировано в KDF инициализации DH ниже. Это связывает ответ с сессией. Ключ сессии из инициализации DH не используется.

#### Эфемерный ключ ответа новой сессии

Эфемерный ключ Боба. Эфемерный ключ имеет длину 32 байта, закодирован с помощью Elligator2, в формате little endian. Этот ключ никогда не используется повторно; новый ключ генерируется для каждого сообщения, включая повторные передачи.

#### Полезная нагрузка

Зашифрованная длина — это остальная часть данных. Расшифрованная длина на 16 меньше зашифрованной длины. Полезная нагрузка обычно содержит один или несколько блоков Garlic Clove. Формат и дополнительные требования см. в разделе полезной нагрузки ниже.

#### KDF для Reply TagSet

Один или несколько тегов создаются из TagSet, который инициализируется с использованием KDF ниже, используя chainKey из сообщения New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF для зашифрованного содержимого секции ключа ответа

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF для зашифрованного содержимого секции полезной нагрузки

Это похоже на первое сообщение Existing Session после разделения, но без отдельного тега. Кроме того, мы используем хеш, указанный выше, чтобы привязать полезную нагрузку к сообщению NSR.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Примечания

В ответ может быть отправлено несколько NSR сообщений, каждое с уникальными эфемерными ключами, в зависимости от размера ответа.

Алиса и Боб должны использовать новые эфемерные ключи для каждого сообщения NS и NSR.

Алиса должна получить одно из NSR сообщений Боба перед отправкой сообщений Existing Session (ES), а Боб должен получить ES сообщение от Алисы перед отправкой ES сообщений.

`chainKey` и `k` из NSR Payload Section Боба используются в качестве входных данных для начальных ES DH Ratchets (в обоих направлениях, см. DH Ratchet KDF).

Боб должен сохранять только существующие сессии для ES-сообщений, полученных от Алисы. Любые другие созданные входящие и исходящие сессии (для множественных NSR) должны быть немедленно уничтожены после получения первого ES-сообщения Алисы для данной сессии.

### 1h) Формат существующей сессии

Тег сессии (8 байт) Зашифрованные данные и MAC (см. раздел 3 ниже)

#### Формат

Зашифровано:

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Полезная нагрузка

Зашифрованная длина — это оставшаяся часть данных. Расшифрованная длина на 16 меньше зашифрованной длины. См. раздел полезной нагрузки ниже для формата и требований.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Формат: 32-байтные публичный и приватный ключи, little-endian.

### 2a) Elligator2

В стандартных handshake-процедурах Noise начальные сообщения handshake в каждом направлении начинаются с эфемерных ключей, которые передаются в открытом виде. Поскольку валидные ключи X25519 можно отличить от случайных данных, злоумышленник, находящийся посередине, может отличить эти сообщения от сообщений Existing Session, которые начинаются со случайных тегов сессии. В [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)) мы использовали низконакладную функцию XOR с использованием внеполосного статического ключа для обфускации ключа. Однако здесь модель угроз отличается; мы не хотим позволить любому MitM использовать любые средства для подтверждения назначения трафика или для различения начальных сообщений handshake от сообщений Existing Session.

Поэтому [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) используется для преобразования эфемерных ключей в сообщениях New Session и New Session Reply таким образом, чтобы они были неотличимы от равномерно случайных строк.

#### Формат

32-байтовые открытые и закрытые ключи. Закодированные ключи имеют формат little endian.

Как определено в [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), закодированные ключи неотличимы от 254 случайных битов. Нам требуется 256 случайных битов (32 байта). Поэтому кодирование и декодирование определяются следующим образом:

Кодирование:

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Декодирование:

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Примечания

Elligator2 удваивает среднее время генерации ключей, поскольку половина приватных ключей приводит к открытым ключам, которые не подходят для кодирования с помощью Elligator2. Кроме того, время генерации ключей неограничено и имеет экспоненциальное распределение, поскольку генератор должен продолжать повторные попытки до тех пор, пока не будет найдена подходящая пара ключей.

Эти накладные расходы можно контролировать, выполняя генерацию ключей заранее в отдельном потоке для поддержания пула подходящих ключей.

Генератор выполняет функцию ENCODE_ELG2() для определения пригодности. Поэтому генератор должен сохранять результат ENCODE_ELG2(), чтобы не пришлось вычислять его снова.

Кроме того, неподходящие ключи могут быть добавлены в пул ключей, используемых для [NTCP2](/docs/specs/ntcp2/), где Elligator2 не используется. Проблемы безопасности такого подхода требуют дальнейшего изучения.

### 3) AEAD (ChaChaPoly)

AEAD с использованием ChaCha20 и Poly1305, как и в [NTCP2](/docs/specs/ntcp2/). Это соответствует [RFC-7539](https://tools.ietf.org/html/rfc7539), который также аналогично используется в TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Входные данные для Новой Сессии и Ответа на Новую Сессию

Входные данные для функций шифрования/расшифровки блока AEAD в сообщении New Session:

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Входные данные существующей сессии

Входные данные для функций шифрования/дешифрования блока AEAD в сообщении Existing Session:

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Зашифрованный формат

Вывод функции шифрования, ввод функции расшифровки:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Примечания

- Поскольку ChaCha20 является потоковым шифром, открытые тексты не нуждаются в дополнении.
  Дополнительные байты потока ключей отбрасываются.
- Ключ для шифра (256 бит) согласуется посредством
  SHA256 KDF. Детали KDF для каждого сообщения приведены в отдельных
  разделах ниже.
- Фреймы ChaChaPoly имеют известный размер, поскольку они инкапсулированы в
  I2NP сообщение данных.
- Для всех сообщений дополнение находится внутри фрейма аутентифицированных данных.

#### Обработка ошибок AEAD

Все полученные данные, которые не прошли проверку AEAD, должны быть отброшены. Ответ не возвращается.

### 4) Ratchets

Мы по-прежнему используем теги сессий, как и раньше, но теперь мы используем ratchet для их генерации. У тегов сессий также была опция смены ключей, которую мы так и не реализовали. Это как двойной ratchet, но мы так и не сделали второй.

Здесь мы определяем нечто похожее на Double Ratchet от Signal. Теги сессии генерируются детерминированно и идентично как на стороне получателя, так и на стороне отправителя.

Используя симметричный ключ/тег ratchet, мы исключаем использование памяти для хранения session tags на стороне отправителя. Мы также исключаем потребление пропускной способности для отправки наборов тегов. Использование на стороне получателя по-прежнему значительно, но мы можем его дополнительно сократить, поскольку уменьшим session tag с 32 байт до 8 байт.

Мы не используем шифрование заголовков, как указано (и опционально) в Signal, вместо этого мы используем теги сессии.

Используя DH ratchet, мы достигаем прямой секретности, которая никогда не была реализована в ElGamal/AES+SessionTags.

Примечание: Одноразовый открытый ключ New Session не является частью ratchet, его единственная функция — зашифровать начальный DH ratchet ключ Алисы.

#### Номера сообщений

Double Ratchet обрабатывает потерянные или неупорядоченные сообщения, включая в заголовок каждого сообщения тег. Получатель ищет индекс тега, это номер сообщения N. Если сообщение содержит блок Message Number со значением PN, получатель может удалить любые теги выше этого значения в предыдущем наборе тегов, сохраняя при этом пропущенные теги из предыдущего набора тегов на случай, если пропущенные сообщения поступят позже.

#### Пример реализации

Мы определяем следующие структуры данных и функции для реализации этих ratchet.

TAGSET_ENTRY

Одна запись в TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Коллекция TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets, но не так быстро, как это делает Signal. Мы разделяем подтверждение полученного ключа от генерации нового ключа. При типичном использовании Алиса и Боб будут ratchet (дважды) сразу же в новой сессии, но больше ratchet делать не будут.

Обратите внимание, что ratchet предназначен для одного направления и генерирует цепочку ratchet для New Session tag / ключа сообщения для этого направления. Чтобы сгенерировать ключи для обоих направлений, необходимо выполнить ratchet дважды.

Вы выполняете ratchet каждый раз, когда генерируете и отправляете новый ключ. Вы выполняете ratchet каждый раз, когда получаете новый ключ.

Алиса выполняет ratchet один раз при создании несвязанной исходящей сессии, она не создает входящую сессию (несвязанная сессия не предполагает ответов).

Боб выполняет один ratchet при создании несвязанной входящей сессии и не создает соответствующую исходящую сессию (несвязанная сессия не поддерживает ответы).

Alice продолжает отправлять сообщения New Session (NS) Bob'у до получения одного из сообщений Bob'а New Session Reply (NSR). Затем она использует результаты KDF из Payload Section сообщения NSR в качестве входных данных для сессионных ratchet'ов (см. DH Ratchet KDF) и начинает отправлять сообщения Existing Session (ES).

Для каждого полученного NS сообщения Боб создает новую входящую сессию, используя результаты KDF из секции полезной нагрузки ответа в качестве входных данных для нового входящего и исходящего ES DH Ratchet.

Для каждого требуемого ответа Боб отправляет Алисе NSR сообщение с ответом в полезной нагрузке. Требуется, чтобы Боб использовал новые эфемерные ключи для каждого NSR.

Bob должен получить ES сообщение от Alice на одной из входящих сессий, прежде чем создавать и отправлять ES сообщения на соответствующей исходящей сессии.

Алиса должна использовать таймер для получения NSR сообщения от Боба. Если таймер истекает, сессия должна быть удалена.

Чтобы избежать KCI и/или атаки истощения ресурсов, при которой злоумышленник сбрасывает NSR ответы Боба, заставляя Алису продолжать отправлять NS сообщения, Алиса должна избегать запуска новых сессий с Бобом после определенного количества повторных попыток из-за истечения таймера.

Алиса и Боб каждый выполняют DH ratchet для каждого полученного блока NextKey.

Алиса и Боб генерируют новые наборы тегов и два симметричных ключевых ratchet после каждого DH ratchet. Для каждого нового ES сообщения в заданном направлении Алиса и Боб продвигают ratchet тегов сеанса и симметричных ключей.

Частота DH ratchets после первоначального рукопожатия зависит от реализации. Хотя протокол устанавливает ограничение в 65535 сообщений до того, как потребуется ratchet, более частое выполнение ratcheting (на основе количества сообщений, истёкшего времени или и того, и другого) может обеспечить дополнительную безопасность.

После финального handshake KDF в связанных сессиях, Bob и Alice должны выполнить функцию Noise Split() на результирующем CipherState для создания независимых симметричных ключей и ключей цепочки тегов для входящих и исходящих сессий.

##### ИДЕНТИФИКАТОРЫ НАБОРОВ КЛЮЧЕЙ И ТЕГОВ

Номера идентификаторов ключей и наборов тегов используются для идентификации ключей и наборов тегов. Идентификаторы ключей используются в блоках NextKey для идентификации отправляемого или используемого ключа. Идентификаторы наборов тегов используются (вместе с номером сообщения) в блоках ACK для идентификации подтверждаемого сообщения. Идентификаторы как ключей, так и наборов тегов применяются к наборам тегов для одного направления. Номера идентификаторов ключей и наборов тегов должны быть последовательными.

В первых наборах тегов, используемых для сессии в каждом направлении, идентификатор набора тегов равен 0. Блоки NextKey не были отправлены, поэтому идентификаторы ключей отсутствуют.

Чтобы начать DH ratchet, отправитель передает новый блок NextKey с идентификатором ключа 0. Получатель отвечает новым блоком NextKey с идентификатором ключа 0. Затем отправитель начинает использовать новый набор тегов с идентификатором набора тегов 1.

Последующие наборы тегов генерируются аналогично. Для всех наборов тегов, используемых после обменов NextKey, номер набора тегов равен (1 + ID ключа Алисы + ID ключа Боба).

Идентификаторы ключей и наборов тегов начинаются с 0 и увеличиваются последовательно. Максимальный идентификатор набора тегов — 65535. Максимальный идентификатор ключа — 32767. Когда набор тегов почти исчерпан, отправитель набора тегов должен инициировать обмен NextKey. Когда набор тегов 65535 почти исчерпан, отправитель набора тегов должен инициировать новую сессию, отправив сообщение New Session.

При максимальном размере потокового сообщения 1730 и предполагая отсутствие повторных передач, теоретический максимум передачи данных с использованием одного набора тегов составляет 1730 * 65536 ~= 108 МБ. Фактический максимум будет меньше из-за повторных передач.

Теоретический максимальный объем передачи данных со всеми 65536 доступными наборами тегов, до того как сессия должна будет быть отброшена и заменена, составляет 64K * 108 МБ ~= 6,9 ТБ.

##### ПОТОК СООБЩЕНИЙ DH RATCHET

Следующий обмен ключами для набора тегов должен быть инициирован отправителем этих тегов (владельцем исходящего набора тегов). Получатель (владелец входящего набора тегов) ответит. Для типичного HTTP GET трафика на уровне приложения Боб отправит больше сообщений и первым выполнит храповик, инициировав обмен ключами; диаграмма ниже это показывает. Когда Алиса выполняет храповик, происходит то же самое, но наоборот.

Первый набор тегов, используемый после рукопожатия NS/NSR, это набор тегов 0. Когда набор тегов 0 почти исчерпан, новые ключи должны быть обменены в обоих направлениях для создания набора тегов 1. После этого новый ключ отправляется только в одном направлении.

Для создания набора тегов 2, отправитель тегов посылает новый ключ, а получатель тегов отправляет ID своего старого ключа в качестве подтверждения. Обе стороны выполняют DH.

Для создания набора тегов 3 отправитель тега отправляет ID своего старого ключа и запрашивает новый ключ у получателя тега. Обе стороны выполняют DH.

Последующие наборы тегов генерируются так же, как наборы тегов 2 и 3. Номер набора тегов равен (1 + ID ключа отправителя + ID ключа получателя).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
После завершения DH ratchet для исходящего tagset и создания нового исходящего tagset, он должен использоваться немедленно, а старый исходящий tagset может быть удален.

После завершения DH ratchet для входящего tagset и создания нового входящего tagset, получатель должен прослушивать теги в обоих tagset и удалить старый tagset через короткое время, примерно через 3 минуты.

Сводка по набору тегов и последовательности ID ключей приведена в таблице ниже. * указывает на то, что генерируется новый ключ.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Номера ID ключей и наборов тегов должны быть последовательными.

##### ИНИЦИАЛИЗАЦИЯ DH KDF

Это определение DH_INITIALIZE(rootKey, k) для одного направления. Оно создает набор тегов и "следующий корневой ключ" для использования в последующем DH ratchet при необходимости.

Мы используем DH-инициализацию в трёх местах. Во-первых, мы используем её для генерации набора тегов для ответов New Session. Во-вторых, мы используем её для генерации двух наборов тегов, по одному для каждого направления, для использования в сообщениях Existing Session. Наконец, мы используем её после DH Ratchet для генерации нового набора тегов в одном направлении для дополнительных сообщений Existing Session.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Это используется после обмена новыми DH ключами в блоках NextKey, до того как набор тегов будет исчерпан.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4б) Храповик меток сессии

Ratchets для каждого сообщения, как в Signal. Ratchet тега сессии синхронизирован с ratchet симметричного ключа, но ratchet ключа получателя может "отставать", чтобы экономить память.

Передатчик делает один поворот ratchet для каждого переданного сообщения. Никаких дополнительных тегов хранить не требуется. Передатчик также должен вести счетчик для 'N' - номера сообщения в текущей цепи. Значение 'N' включается в отправляемое сообщение. См. определение блока Message Number.

Получатель должен продвинуть ratchet вперед на максимальный размер окна и сохранить теги в "наборе тегов", который связан с сессией. После получения сохраненный тег может быть отброшен, и если нет предыдущих неполученных тегов, окно может быть продвинуто. Получатель должен хранить значение 'N', связанное с каждым тегом сессии, и проверять, что номер в отправленном сообщении соответствует этому значению. См. определение блока Message Number.

##### KDF

Это определение RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Симметричный ключевой храповик

Ratchets для каждого сообщения, как в Signal. Каждый симметричный ключ имеет связанный номер сообщения и тег сессии. Ratchet ключа сессии синхронизирован с симметричным ratchet тега, но ratchet ключа получателя может "отставать", чтобы сэкономить память.

Передатчик выполняет один поворот храпового механизма для каждого переданного сообщения. Дополнительные ключи хранить не требуется.

Когда получатель получает session tag, если он еще не продвинул симметричный key ratchet до соответствующего ключа, он должен "догнать" соответствующий ключ. Получатель, вероятно, будет кэшировать ключи для любых предыдущих тегов, которые еще не были получены. После получения сохраненный ключ может быть отброшен, и если нет предыдущих неполученных тегов, окно может быть продвинуто.

Для эффективности рatchet-механизмы для session tag и симметричного ключа разделены, что позволяет session tag ratchet опережать symmetric key ratchet. Это также обеспечивает дополнительную безопасность, поскольку session tag передаются по сети.

##### KDF

Это определение RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Полезная нагрузка

Это заменяет формат секции AES, определенный в спецификации ElGamal/AES+SessionTags.

Это использует тот же формат блоков, что определен в спецификации [NTCP2](/docs/specs/ntcp2/). Отдельные типы блоков определяются по-разному.

Существуют опасения, что поощрение разработчиков к совместному использованию кода может привести к проблемам с парсингом. Разработчики должны тщательно взвесить преимущества и риски совместного использования кода и убедиться, что правила порядка следования и валидных блоков различаются для этих двух контекстов.

#### Полезная нагрузка Секция Расшифрованные данные

Зашифрованная длина — это оставшаяся часть данных. Расшифрованная длина на 16 меньше зашифрованной длины. Поддерживаются все типы блоков. Типичное содержимое включает следующие блоки:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Незашифрованные данные

В зашифрованном фрейме содержится ноль или более блоков. Каждый блок содержит однобайтовый идентификатор, двухбайтовую длину и ноль или более байтов данных.

Для обеспечения расширяемости получатели ДОЛЖНЫ игнорировать блоки с неизвестными номерами типов и обрабатывать их как заполнение.

Зашифрованные данные имеют максимальный размер 65535 байт, включая 16-байтовый заголовок аутентификации, поэтому максимальный размер незашифрованных данных составляет 65519 байт.

(Тег аутентификации Poly1305 не показан):

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Правила упорядочивания блоков

В сообщении New Session блок DateTime является обязательным и должен быть первым блоком.

Другие разрешенные блоки:

- Garlic Clove (тип 11)
- Опции (тип 5)
- Заполнение (тип 254)

В сообщении New Session Reply блоки не требуются.

Другие разрешенные блоки:

- Garlic Clove (тип 11)
- Опции (тип 5)
- Заполнение (тип 254)

Никакие другие блоки не разрешены. Заполнение (padding), если присутствует, должно быть последним блоком.

В сообщении Existing Session блоки не являются обязательными, и порядок не определен, за исключением следующих требований:

Блок завершения, если присутствует, должен быть последним блоком, за исключением блока заполнения. Блок заполнения, если присутствует, должен быть последним блоком.

В одном фрейме может быть несколько блоков Garlic Clove. В одном фрейме может быть до двух блоков Next Key. Несколько блоков Padding в одном фрейме не допускается. Другие типы блоков, вероятно, не будут иметь несколько блоков в одном фрейме, но это не запрещено.

#### DateTime

Время истечения. Помогает предотвратить повторные атаки. Bob должен проверить, что сообщение является недавним, используя эту временную метку. Bob должен реализовать фильтр Блума или другой механизм для предотвращения повторных атак, если время действительно. Bob также может использовать более раннюю проверку обнаружения повторов для дублирующегося эфемерного ключа (до или после декодирования Elligator2) для обнаружения и отбрасывания недавних дублирующихся NS-сообщений до расшифровки. Обычно включается только в сообщения New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Garlic Clove

Одна расшифрованная Garlic Clove, как указано в [I2NP](/docs/specs/i2np/), с модификациями для удаления неиспользуемых или избыточных полей. Предупреждение: Этот формат значительно отличается от формата для ElGamal/AES. Каждая clove является отдельным блоком полезной нагрузки. Garlic Cloves не могут быть фрагментированы между блоками или между кадрами ChaChaPoly.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Примечания:

- Разработчики должны обеспечить, что при чтении блока, неправильно сформированные или
  вредоносные данные не приведут к переполнению при чтении в следующий блок.
- Формат Clove Set, указанный в [I2NP](/docs/specs/i2np/), не
  используется. Каждый clove содержится в своем собственном блоке.
- Заголовок I2NP сообщения составляет 9 байт, с идентичным форматом тому,
  что используется в [NTCP2](/docs/specs/ntcp2/).
- Certificate, Message ID и Expiration из определения Garlic Message
  в [I2NP](/docs/specs/i2np/) не включены.
- Certificate, Clove ID и Expiration из определения Garlic Clove
  в [I2NP](/docs/specs/i2np/) не включены.

#### Завершение

Реализация опциональна. Закрыть сессию. Это должен быть последний блок без заполнения в кадре. В этой сессии больше не будет отправлено сообщений.

Не разрешено в NS или NSR. Включается только в сообщения Existing Session.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Опции

НЕ РЕАЛИЗОВАНО, требует дальнейшего изучения. Передача обновленных опций. Опции включают различные параметры для сессии. См. раздел "Анализ длины тега сессии" ниже для получения дополнительной информации.

Блок параметров может иметь переменную длину, так как может присутствовать more_options.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

more_options :: Format undefined, for future use
```
SOTW — это рекомендация отправителя получателю для окна входящих тегов получателя (максимальное упреждение). RITW — это декларация отправителя о размере окна входящих тегов (максимальное упреждение), которое он планирует использовать. Затем каждая сторона устанавливает или корректирует упреждение на основе минимального или максимального значения или другого расчёта.

Примечания:

- Поддержка нестандартной длины тегов сессии, будем надеяться, никогда не потребуется.
- Окно тегов соответствует MAX_SKIP в документации Signal.

Проблемы:

- Согласование параметров еще предстоит определить.
- Значения по умолчанию еще предстоит определить.
- Параметры заполнения и задержки скопированы из NTCP2, но эти параметры
  там еще не полностью реализованы или изучены.

#### Номера сообщений

Реализация является опциональной. Длина (количество отправленных сообщений) в предыдущем наборе тегов (PN). Получатель может немедленно удалить теги больше PN из предыдущего набора тегов. Получатель может удалить теги меньше или равные PN из предыдущего набора тегов через короткое время (например, 2 минуты).

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Примечания:

- Максимальный PN равен 65535.
- Определения PN равны определению Signal, минус один.
  Это похоже на то, что делает Signal, но в Signal PN и N находятся в
  заголовке. Здесь они находятся в зашифрованном теле сообщения.
- Не отправляйте этот блок в наборе тегов 0, потому что предыдущего набора
  тегов не было.

#### Следующий публичный ключ DH Ratchet

Следующий ключ DH ratchet находится в полезной нагрузке и является необязательным. Мы не выполняем ratchet каждый раз. (Это отличается от Signal, где он находится в заголовке и отправляется каждый раз)

Для первого ratchet, Key ID = 0.

Не разрешено в NS или NSR. Включается только в сообщения Existing Session.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Примечания:

- Key ID является инкрементным счетчиком для локального ключа, используемого для данного набора тегов, начиная с 0.
- ID не должен изменяться, если только не изменится ключ.
- Возможно, это не является строго необходимым, но полезно для отладки. Signal не использует key ID.
- Максимальный Key ID равен 32767.
- В редких случаях, когда наборы тегов в обоих направлениях ротируются одновременно, кадр будет содержать два блока Next Key, один для прямого ключа и один для обратного ключа.
- Номера ID ключей и наборов тегов должны быть последовательными.
- Подробности см. в разделе DH Ratchet выше.

#### Подтверждение

Это отправляется только в случае получения блока запроса подтверждения. Может присутствовать несколько подтверждений для подтверждения нескольких сообщений.

Не разрешено в NS или NSR. Включается только в сообщения Existing Session.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Примечания:

- ID набора тегов и N уникально идентифицируют подтверждаемое сообщение.
- В первых наборах тегов, используемых для сессии в каждом направлении, ID набора тегов равен 0.
- Блоки NextKey не были отправлены, поэтому ID ключей отсутствуют.
- Для всех наборов тегов, используемых после обменов NextKey, номер набора тегов равен (1 + ID ключа Alice + ID ключа Bob).

#### Запрос подтверждения

Запросить внутриполосное подтверждение. Для замены внеполосного сообщения DeliveryStatus в Garlic Clove.

Если запрашивается явное подтверждение, текущий ID набора тегов и номер сообщения (N) возвращаются в блоке подтверждения.

Не разрешено в NS или NSR. Включается только в сообщения Existing Session.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Заполнение

Все заполнение находится внутри AEAD фреймов. TODO Заполнение внутри AEAD должно примерно соответствовать согласованным параметрам. TODO Alice отправила свои запрошенные параметры tx/rx min/max в сообщении NS. TODO Bob отправил свои запрошенные параметры tx/rx min/max в сообщении NSR. Обновленные опции могут быть отправлены во время фазы данных. См. информацию о блоке опций выше.

Если присутствует, это должен быть последний блок в кадре.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Примечания:

- Заполнение нулями допустимо, поскольку данные будут зашифрованы.
- Стратегии заполнения пока не определены.
- Кадры, содержащие только заполнение, разрешены.
- Заполнение по умолчанию составляет 0-15 байт.
- См. блок опций для согласования параметров заполнения
- См. блок опций для параметров минимального/максимального заполнения
- Реакция router на нарушение согласованных параметров заполнения
  зависит от реализации.

#### Другие типы блоков

Реализации должны игнорировать неизвестные типы блоков для обеспечения прямой совместимости.

#### Будущая работа

- Длина заполнения должна определяться либо для каждого сообщения отдельно на основе оценок распределения длин, либо должны добавляться случайные задержки. Эти контрмеры должны быть включены для противодействия DPI, поскольку размеры сообщений иначе могли бы выдать, что трафик I2P передается транспортным протоколом. Точная схема заполнения является областью будущей работы, Приложение A предоставляет дополнительную информацию по данной теме.

## Типичные шаблоны использования

### HTTP GET

Это наиболее типичный случай использования, и большинство случаев потокового вещания не по HTTP будут идентичны этому случаю. Отправляется небольшое начальное сообщение, следует ответ, и дополнительные сообщения отправляются в обоих направлениях.

HTTP GET обычно помещается в одно I2NP сообщение. Alice отправляет небольшой запрос с одним новым Session сообщением, включая reply leaseset. Alice включает немедленный ratchet к новому ключу. Включает подпись для привязки к получателю. Подтверждение не запрашивается.

Боб немедленно выполняет ratchet.

Alice немедленно выполняет ratchet.

Продолжает работу с этими сеансами.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

У Алисы есть три варианта:

1)  Отправить только первое сообщение (размер окна = 1), как в HTTP GET. Не

    recommended.
2)  Отправить до streaming window, но используя тот же Elligator2-encoded

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Рекомендуемая реализация. Отправлять до размера окна потока, но используя

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Поток сообщений варианта 3:

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Датаграмма с возможностью ответа

Одиночное сообщение с ожидаемым одиночным ответом. Дополнительные сообщения или ответы могут быть отправлены.

Похоже на HTTP GET, но с меньшими опциями для размера окна тегов сессии и времени жизни. Возможно, не запрашивать ratchet.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Множественные необработанные датаграммы

Несколько анонимных сообщений, без ожидания ответов.

В этом сценарии Алиса запрашивает сессию, но без привязки. Отправляется сообщение новой сессии. LeaseSet ответа не прилагается. Прилагается DSM ответа (это единственный случай использования, который требует приложенных DSM). Следующий ключ не включается. Ответ или ratchet не запрашивается. Ratchet не отправляется. Опции устанавливают окно тегов сессии в ноль.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Одиночная Raw датаграмма

Одиночное анонимное сообщение, ответ на которое не ожидается.

Одноразовое сообщение отправлено. Ответный LS или DSM не включены. Следующий ключ не включен. Ответ или ratchet не запрашивается. Ratchet не отправляется. Опции устанавливают окно session tags в ноль.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Долгоживущие сессии

Долгоживущие сессии могут выполнять ratchet или запрашивать ratchet в любое время для поддержания прямой секретности с этого момента времени. Сессии должны выполнять ratchet при приближении к лимиту отправленных сообщений на сессию (65535).

## Особенности реализации

### Защита

Как и в случае с существующим протоколом ElGamal/AES+SessionTag, реализации должны ограничивать хранение session tag и защищаться от атак истощения памяти.

Некоторые рекомендуемые стратегии включают:

- Жесткий лимит на количество сохраняемых тегов сессий
- Агрессивное истечение срока действия неактивных входящих сессий при нехватке памяти
- Ограничение на количество входящих сессий, привязанных к одному удаленному назначению
- Адаптивное сокращение окна тегов сессии и удаление старых неиспользуемых тегов при нехватке памяти
- Отказ от ratchet по запросу при нехватке памяти

### Параметры

Рекомендуемые параметры и таймауты:

- Размер набора тегов NSR: 12 tsmin и tsmax
- Размер набора тегов ES 0: tsmin 24, tsmax 160
- Размер набора тегов ES (1+): 160 tsmin и tsmax
- Таймаут набора тегов NSR: 3 минуты для получателя
- Таймаут набора тегов ES: 8 минут для отправителя, 10 минут для получателя
- Удаление предыдущего набора тегов ES через: 3 минуты
- Предварительный просмотр набора тегов для тега N: min(tsmax, tsmin + N/4)
- Обрезка набора тегов за тегом N: min(tsmax, tsmin + N/4) / 2
- Отправка следующего ключа на теге: 4096
- Отправка следующего ключа после времени жизни набора тегов: TBD
- Замена сессии при получении NS через: 3 минуты
- Максимальное расхождение часов: от -5 минут до +2 минут
- Продолжительность фильтра повторов NS: 5 минут
- Размер заполнения: 0-15 байт (другие стратегии TBD)

### Классификация

Ниже приведены рекомендации по классификации входящих сообщений.

#### Только X25519

В tunnel, который используется исключительно с этим протоколом, выполнять идентификацию так же, как это делается в настоящее время с ElGamal/AES+SessionTags:

Сначала обработайте исходные данные как тег сессии и найдите тег сессии. Если найден, расшифруйте, используя сохраненные данные, связанные с этим тегом сессии.

Если не найдено, обрабатывайте исходные данные как открытый ключ DH и nonce. Выполните операцию DH и указанную KDF, и попытайтесь расшифровать оставшиеся данные.

#### X25519 общий с ElGamal/AES+SessionTags

На tunnel, который поддерживает как данный протокол, так и ElGamal/AES+SessionTags, классифицируйте входящие сообщения следующим образом:

Из-за недостатка в спецификации ElGamal/AES+SessionTags блок AES не дополняется до случайной длины, не кратной 16. Поэтому длина сообщений Existing Session по модулю 16 всегда равна 0, а длина сообщений New Session по модулю 16 всегда равна 2 (поскольку блок ElGamal имеет длину 514 байт).

Если длина по модулю 16 не равна 0 или 2, обработайте исходные данные как session tag и найдите этот session tag. Если найден, расшифруйте, используя сохраненные данные, связанные с этим session tag.

Если не найден, и длина по модулю 16 не равна 0 или 2, обрабатывать исходные данные как публичный ключ DH и nonce. Выполнить операцию DH и указанную KDF, и попытаться расшифровать оставшиеся данные. (на основе относительного трафикового микса и относительной стоимости операций X25519 и ElGamal DH, этот шаг может быть выполнен последним)

Иначе, если длина по модулю 16 равна 0, обрабатывать исходные данные как session tag ElGamal/AES и искать этот session tag. Если найден, расшифровывать с использованием сохраненных данных, связанных с этим session tag.

Если не найден, и данные имеют длину не менее 642 (514 + 128) байт, и длина по модулю 16 равна 2, обрабатывать начальные данные как блок ElGamal. Попытаться расшифровать оставшиеся данные.

Обратите внимание, что если спецификация ElGamal/AES+SessionTag будет обновлена для поддержки дополнения не кратного 16, то всё нужно будет делать по-другому.

### Повторные передачи и переходы состояний

Уровень ratchet не выполняет повторные передачи и, за двумя исключениями, не использует таймеры для передач. Таймеры также требуются для тайм-аута набора тегов.

Таймеры передачи используются только для отправки NSR и для ответа с помощью ES, когда полученное ES содержит запрос ACK. Рекомендуемый тайм-аут составляет одну секунду. Почти во всех случаях верхний уровень (datagram или streaming) ответит, принудительно вызвав NSR или ES, и таймер может быть отменен. Если таймер срабатывает, отправьте пустую полезную нагрузку с NSR или ES.

#### Ответы уровня Ratchet

Начальные реализации полагаются на двунаправленный трафик на верхних уровнях. То есть реализации предполагают, что трафик в противоположном направлении вскоре будет передан, что заставит любой необходимый ответ на уровне ECIES.

Однако некоторый трафик может быть однонаправленным или иметь очень низкую пропускную способность, так что трафик более высокого уровня не генерирует своевременный ответ.

Получение сообщений NS и NSR требует ответа; получение блоков ACK Request и Next Key также требует ответа.

Реализации должны запускать таймер при получении одного из этих сообщений, требующих ответа, и генерировать "пустой" ответ (без блока Garlic Clove) на уровне ECIES, если обратный трафик не отправляется в течение короткого периода времени (например, 1 секунда).

Также может быть целесообразно использовать еще более короткий таймаут для ответов на сообщения NS и NSR, чтобы как можно скорее переключить трафик на эффективные сообщения ES.

#### NS привязка для NSR

На уровне ratchet, как Bob, Alice известна только по статическому ключу. Сообщение NS аутентифицировано ([Noise](https://noiseprotocol.org/noise.html) IK аутентификация отправителя 1). Однако этого недостаточно для того, чтобы уровень ratchet мог отправить что-либо Alice, поскольку сетевая маршрутизация требует полного Destination.

Прежде чем NSR может быть отправлен, полный Destination Алисы должен быть обнаружен либо слоем ratchet, либо протоколом более высокого уровня с поддержкой ответов - либо отвечающими [Datagrams](/docs/specs/datagrams/), либо [Streaming](/docs/specs/streaming/). После нахождения Leaseset для этого Destination, данный Leaseset будет содержать тот же статический ключ, что и содержащийся в NS.

Обычно верхний уровень ответит, заставляя выполнить поиск leaseset Алисы в сетевой базе данных по хешу назначения Алисы. Этот leaseset почти всегда будет найден локально, поскольку NS содержал блок garlic clove с сообщением Database Store, содержащим leaseset Алисы.

Чтобы Боб был готов отправить NSR на уровне ratchet и привязать ожидающую сессию к Destination Алисы, Боб должен "захватить" Destination при обработке полезной нагрузки NS. Если найдено сообщение Database Store, содержащее Leaseset с ключом, соответствующим статическому ключу в NS, ожидающая сессия теперь привязана к этому Destination, и Боб знает, куда отправить любой NSR, если истечет таймер ответа. Это рекомендуемая реализация.

Альтернативный подход заключается в поддержании кеша или базы данных, где статический ключ сопоставляется с Destination. Безопасность и практичность данного подхода является темой для дальнейшего изучения.

Ни данная спецификация, ни другие не требуют строго, чтобы каждый NS содержал leaseSet Алисы. Однако на практике это должно быть так. Рекомендуемый таймаут отправителя ES tagset (8 минут) короче максимального таймаута leaseSet (10 минут), поэтому может существовать небольшое окно времени, когда предыдущая сессия истекла, Алиса думает, что у Боба все еще есть её валидный leaseSet, и не отправляет новый leaseSet с новым NS. Это тема для дальнейшего изучения.

#### Множественные NS-сообщения

Если ответ NSR не получен до того, как верхний уровень (датаграмма или потоковый) отправит больше данных, возможно, в качестве повторной передачи, Алиса должна составить новый NS, используя новый эфемерный ключ. Не переиспользуйте эфемерный ключ из любого предыдущего NS. Алиса должна поддерживать дополнительное состояние рукопожатия и производный набор тегов приема для получения сообщений NSR в ответ на любой отправленный NSR.

Реализации могут ограничивать общее количество отправляемых NS сообщений или скорость отправки NS сообщений, либо путем постановки в очередь, либо путем отбрасывания сообщений верхнего уровня до их отправки.

В определенных ситуациях, при высокой нагрузке или в условиях определенных атак, может быть целесообразно для Bob поставить в очередь, отбросить или ограничить видимые NS сообщения без попытки их расшифровки, чтобы избежать атаки на истощение ресурсов.

Для каждого полученного NS, Боб генерирует исходящий tagset NSR, отправляет NSR, выполняет split(), и генерирует входящий и исходящий tagsets ES. Однако, Боб не отправляет никаких сообщений ES до тех пор, пока не будет получено первое сообщение ES на соответствующем входящем tagset. После этого Боб может отбросить все состояния handshake и tagsets для любых других полученных NS или отправленных NSR, либо позволить им истечь в ближайшее время. Не используйте tagsets NSR для сообщений ES.

Это тема для дальнейшего изучения - может ли Боб выбрать спекулятивную отправку ES сообщений сразу после NSR, даже до получения первого ES от Алисы. В определенных сценариях и паттернах трафика это могло бы существенно сэкономить полосу пропускания и процессорное время. Эта стратегия может основываться на эвристике, такой как паттерны трафика, процент полученных ES в tagset первой сессии или другие данные.

#### Множественные NSR сообщения

Для каждого полученного NS сообщения, до получения ES сообщения, Боб должен отвечать новым NSR, либо из-за отправки трафика верхнего уровня, либо из-за истечения таймера отправки NSR.

Каждый NSR использует состояние handshake и набор тегов, соответствующий входящему NS. Bob должен поддерживать состояние handshake и набор тегов для всех полученных NS сообщений до тех пор, пока не будет получено ES сообщение.

Реализации могут ограничивать общее количество отправляемых NSR сообщений или скорость отправки NSR сообщений путем постановки в очередь или отбрасывания сообщений более высокого уровня перед их отправкой. Эти ограничения могут применяться как при обработке входящих NS сообщений, так и при дополнительном исходящем трафике более высокого уровня.

В определенных ситуациях, при высокой нагрузке или в некоторых сценариях атак, может быть целесообразно для Alice поставить в очередь, отбросить или ограничить NSR сообщения без попытки расшифровки, чтобы избежать атаки на истощение ресурсов. Эти ограничения могут применяться как в общем по всем сессиям, так и для каждой сессии отдельно, или одновременно для обоих случаев.

После получения NSR Alice выполняет split() для получения сессионных ключей ES. Alice должна установить таймер и отправить пустое ES сообщение, если вышестоящий уровень не отправляет трафик, обычно в течение одной секунды.

Остальные входящие NSR tagsets могут быть удалены в ближайшее время или им может быть позволено истечь, но Алиса должна сохранить их на короткое время, чтобы расшифровать любые другие NSR сообщения, которые могут быть получены.

### Предотвращение повторных атак

Боб должен реализовать фильтр Блума или другой механизм для предотвращения атак повторного воспроизведения NS, если включенное DateTime недавнее, и отклонять NS сообщения, где DateTime слишком старое. Боб также может использовать более раннюю проверку обнаружения повторов для дублирующегося эфемерного ключа (либо до, либо после декодирования Elligator2) для обнаружения и отбрасывания недавних дублирующихся NS сообщений перед расшифровкой.

Сообщения NSR и ES имеют встроенную защиту от повторного воспроизведения, поскольку тег сессии используется только один раз.

Garlic сообщения также имеют защиту от повторных атак, если router реализует общесистемный фильтр Блума на основе ID I2NP сообщений.

## Связанные изменения

Поиск в базе данных от ECIES-адресатов: См. [Prop154](/proposals/154-ratchet/), теперь включено в [I2NP](/docs/specs/i2np/) для релиза 0.9.46.

Данная спецификация требует поддержки LS2 для публикации публичного ключа X25519 с leaseset. Никаких изменений в спецификации LS2 в [I2NP](/docs/specs/i2np/) не требуется. Вся поддержка была разработана, специфицирована и реализована в [Prop123](/proposals/123-new-netdb-entries/), реализованном в версии 0.9.38.

Данная спецификация требует установки свойства в опциях I2CP для включения. Вся поддержка была спроектирована, специфицирована и реализована в [Prop123](/proposals/123-new-netdb-entries/), внедренном в версии 0.9.38.

Опция, необходимая для включения ECIES, представляет собой единственное свойство I2CP для I2CP, BOB, SAM или i2ptunnel.

Типичные значения: i2cp.leaseSetEncType=4 только для ECIES, или i2cp.leaseSetEncType=4,0 для двойных ключей ECIES и ElGamal.

## Совместимость

Любой router, поддерживающий LS2 с двойными ключами (версия 0.9.38 или выше), должен поддерживать подключение к адресатам с двойными ключами.

Пункты назначения только с ECIES требуют, чтобы большинство floodfill были обновлены до версии 0.9.46 для получения зашифрованных ответов на запросы. См. [Prop154](/proposals/154-ratchet/).

Пункты назначения только с ECIES могут подключаться только к другим пунктам назначения, которые также работают только с ECIES или поддерживают двойные ключи.

## Ссылки

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrams](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - См. также [статью об Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) и код OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Аутентификация и обмен аутентифицированными ключами
- [Streaming](/docs/specs/streaming/)
