---
title: "Постквантовые криптографические протоколы"
aliases:
  - "/proposals/169-pq-crypto"
  - "/proposals/169-pq-crypto/"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Открыть"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.70"
toc: true
---

### Состояние

| Протокол / Функция | Статус |
|--------------------|--------|
| Ratchet | Завершено в Java I2P и i2pd |
| NTCP2 | Бета Q1 2026 |
| SSU2 | Внедрение начинается в ближайшее время, Бета Q23 2026 |
| MLDSA SigTypes | Низкий приоритет, вероятно 2027+ |
## Обзор

Хотя исследования и конкурс подходящих постквантовых (PQ) криптографических алгоритмов ведутся уже десять лет, выбор стал ясен лишь недавно.

Мы начали изучать последствия PQ криптографии в 2022 году [zzz.i2p](http://zzz.i2p/topics/3294).

Стандарты TLS добавили поддержку гибридного шифрования за последние два года, и теперь оно используется для значительной части зашифрованного трафика в интернете благодаря поддержке в Chrome и Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST недавно завершил работу и опубликовал рекомендуемые алгоритмы для постквантовой криптографии [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Несколько распространенных криптографических библиотек теперь поддерживают стандарты NIST или выпустят такую поддержку в ближайшем будущем.

И [Cloudflare](https://blog.cloudflare.com/pq-2024/), и [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) рекомендуют немедленно начать миграцию. См. также FAQ по постквантовой криптографии NSA за 2022 год [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P должен быть лидером в области безопасности и криптографии. Сейчас самое время реализовать рекомендуемые алгоритмы. Используя нашу гибкую систему типов шифрования и типов подписей, мы добавим типы для гибридной криптографии, а также для постквантовых и гибридных подписей.

## Цели

- Выбрать алгоритмы, устойчивые к квантовым атакам
- Добавить только PQ и гибридные алгоритмы в протоколы I2P там, где это уместно
- Определить множественные варианты
- Выбрать лучшие варианты после реализации, тестирования, анализа и исследований
- Добавить поддержку постепенно и с обратной совместимостью

## Не-цели

- Не изменять односторонние протоколы шифрования (Noise N)
- Не отказываться от SHA256, в ближайшем будущем не подвержен угрозе от PQ
- Не выбирать окончательные предпочтительные варианты на данный момент

## Модель угроз

- Router'ы на OBEP или IBGW, возможно действующие сообща,
  сохраняющие garlic сообщения для последующей расшифровки (forward secrecy)
- Наблюдатели сети,
  сохраняющие транспортные сообщения для последующей расшифровки (forward secrecy)
- Участники сети, подделывающие подписи для RI, LS, streaming, датаграмм
  или других структур

## Затронутые протоколы

Мы будем изменять следующие протоколы примерно в порядке разработки. Общее развертывание, вероятно, будет происходить с конца 2025 года до середины 2027 года. Подробности см. в разделе "Приоритеты и развертывание" ниже.

| Протокол / Функция | Статус |
|--------------------|--------|
| Hybrid MLKEM Ratchet и LS | Одобрено 2025-06; бета 2025-08; релиз 2025-11 |
| Hybrid MLKEM NTCP2 | Протестировано в живой сети, Одобрено 2026-02; цель для беты 2026-05; цель для релиза 2026-08 |
| Hybrid MLKEM SSU2 | Одобрено 2026-02; цель для беты 2026-08; цель для релиза 2026-11 |
| MLDSA SigTypes 12-14 | Предложение стабильно, но может быть не завершено до 2027 года |
| MLDSA Dests | Протестировано в живой сети, требует обновления сети для поддержки floodfill |
| Hybrid SigTypes 15-17 | Предварительно |
| Hybrid Dests | |
## Дизайн

Мы будем поддерживать стандарты NIST FIPS 203 и 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), которые основаны на CRYSTALS-Kyber и CRYSTALS-Dilithium (версии 3.1, 3 и более старые), но НЕ совместимы с ними.

### Обмен ключами

Мы будем поддерживать гибридный обмен ключами в следующих протоколах:

| Протокол | Тип Noise | Поддержка только PQ? | Поддержка гибридного? |
|----------|-----------|----------------------|-----------------------|
| NTCP2    | XK        | нет                  | да                    |
| SSU2     | XK        | нет                  | да                    |
| Ratchet  | IK        | нет                  | да                    |
| TBM      | N         | нет                  | нет                   |
| NetDB    | N         | нет                  | нет                   |
PQ KEM предоставляет только эфемерные ключи и не поддерживает напрямую рукопожатия со статическими ключами, такие как Noise XK и IK.

Noise N не использует двусторонний обмен ключами и поэтому не подходит для гибридного шифрования.

Таким образом, мы будем поддерживать только гибридное шифрование для NTCP2, SSU2 и Ratchet. Мы определим три варианта ML-KEM согласно [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), всего для 3 новых типов шифрования. Гибридные типы будут определены только в сочетании с X25519.

Новые типы шифрования:

| Тип | Код |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Накладные расходы будут существенными. Типичные размеры сообщений 1 и 2 (для XK и IK) в настоящее время составляют около 100 байт (до любой дополнительной полезной нагрузки). Это увеличится в 8-15 раз в зависимости от алгоритма.

### Подписи

Мы будем поддерживать PQ и гибридные подписи в следующих структурах:

Таким образом, мы будем поддерживать как PQ-только, так и гибридные подписи. Мы определим три варианта ML-DSA как в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), три гибридных варианта с Ed25519 и три PQ-только варианта с предварительным хешированием только для SU3-файлов, итого 9 новых типов подписей. Гибридные типы будут определены только в сочетании с Ed25519. Мы будем использовать стандартный ML-DSA, НЕ варианты с предварительным хешированием (HashML-DSA), за исключением SU3-файлов.

| Тип | Поддержка только PQ? | Поддержка гибридного? |
|------|---------------------|----------------------|
| RouterInfo | да | да |
| LeaseSet | да | да |
| Streaming SYN/SYNACK/Close | да | да |
| Repliable Datagrams | да | да |
| Datagram2 (prop. 163) | да | да |
| I2CP create session msg | да | да |
| SU3 файлы | да | да |
| X.509 сертификаты | да | да |
| Java keystores | да | да |
Мы будем использовать "хеджированный" или рандомизированный вариант подписи, а не "детерминистический" вариант, как определено в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) разделе 3.4. Это гарантирует, что каждая подпись будет отличаться, даже при подписи одних и тех же данных, и обеспечивает дополнительную защиту от атак по побочным каналам. См. раздел примечаний по реализации ниже для получения дополнительной информации о выборе алгоритмов, включая кодирование и контекст.

Новые типы подписей:

Сертификаты X.509 и другие кодировки DER будут использовать композитные структуры и OID, определенные в [черновике IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Тип | Код |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
Сертификаты X.509 и другие кодировки DER будут использовать составные структуры и OID, определённые в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Поскольку новые типы назначений и router identity не будут содержать заполнения, они не будут сжимаемыми. Размеры назначений и router identity, которые сжимаются gzip при передаче, увеличатся в 12-38 раз в зависимости от алгоритма.

Для Destinations новые типы подписей поддерживаются со всеми типами шифрования в leaseset. Установите тип шифрования в сертификате ключа на NONE (255).

### Допустимые Комбинации

Для RouterIdentities тип шифрования ElGamal устарел. Новые типы подписей поддерживаются только с шифрованием X25519 (тип 4). Новые типы шифрования будут указаны в RouterAddresses. Тип шифрования в сертификате ключа продолжит быть типом 4.

Тестовые векторы для SHA3-256, SHAKE128 и SHAKE256 доступны на сайте [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Требуется новая криптография

- ML-KEM (ранее CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (ранее CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (ранее Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Используется только для SHAKE128
- SHA3-256 (ранее Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 и SHAKE256 (расширения XOF для SHA3-128 и SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Обратите внимание, что библиотека Java bouncycastle поддерживает все вышеперечисленное. Поддержка библиотеки C++ находится в OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Мы не будем поддерживать [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), он намного медленнее и больше по размеру, чем ML-DSA. Мы не будем поддерживать готовящийся FIPS206 (Falcon), он еще не стандартизован. Мы не будем поддерживать NTRU или других кандидатов на постквантовую криптографию, которые не были стандартизованы NIST.

### Альтернативы

Существует исследовательская [статья](https://eprint.iacr.org/2020/379.pdf) по адаптации Wireguard (IK) для чистой PQ криптографии, но в этой статье остается несколько открытых вопросов. Позже этот подход был реализован как Rosenpass [Rosenpass](https://rosenpass.eu/) [техническая документация](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) для PQ Wireguard.

### Rosenpass

Rosenpass использует рукопожатие типа Noise KK с предварительно разделёнными статическими ключами Classic McEliece 460896 (по 500 КБ каждый) и эфемерными ключами Kyber-512 (по сути MLKEM-512). Поскольку шифротексты Classic McEliece составляют всего 188 байт, а открытые ключи и шифротексты Kyber-512 имеют разумный размер, оба сообщения рукопожатия помещаются в стандартный UDP MTU. Выходной разделяемый ключ (osk) из постквантового рукопожатия KK используется в качестве входного предварительно разделённого ключа (psk) для стандартного рукопожатия Wireguard IK. Таким образом, всего происходит два полных рукопожатия: одно чисто постквантовое и одно чисто X25519.

Мы не можем использовать ничего из этого для замены наших XK и IK handshake, потому что:

В техническом документе содержится много полезной информации, и мы изучим её для получения идей и вдохновения. TODO.

- Мы не можем использовать KK, у Боба нет статического ключа Алисы
- Статические ключи размером 500КБ слишком большие
- Мы не хотим дополнительного обмена сообщениями

Обновите разделы и таблицы в документе общих структур [/docs/specs/common-structures/](/docs/specs/common-structures/) следующим образом:

## Спецификация

### Общие структуры

Новые типы публичных ключей:

#### Проблемы

Гибридные публичные ключи представляют собой ключи X25519. Публичные ключи KEM представляют собой эфемерные PQ ключи, отправляемые от Алисы к Бобу. Кодирование и порядок байтов определены в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Тип | Длина публичного ключа | С версии | Использование |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | См. предложение 169, только для Leasesets, не для RI или Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | См. предложение 169, только для Leasesets, не для RI или Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | См. предложение 169, только для Leasesets, не для RI или Destinations |
| MLKEM512 | 800 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| MLKEM768 | 1184 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| MLKEM1024 | 1568 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| MLKEM512_CT | 768 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | См. предложение 169, только для рукопожатий, не для Leasesets, RI или Destinations |
| NONE | 0 | 0.9.xx | См. предложение 169, для destinations с типами PQ-подписей только, не для RI или Leasesets |
Ключи MLKEM*_CT на самом деле не являются публичными ключами, это "зашифрованный текст", отправляемый от Боба к Алисе в рукопожатии Noise. Они перечислены здесь для полноты картины.

Новые типы приватных ключей:

#### PrivateKey

Гибридные приватные ключи - это X25519 ключи. KEM приватные ключи предназначены только для Алисы. Кодирование KEM и порядок байтов определены в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Тип | Длина приватного ключа | С версии | Использование |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | См. предложение 169, только для leaseSet'ов, не для RouterInfo или Destination'ов |
| MLKEM768_X25519 | 32 | 0.9.xx | См. предложение 169, только для leaseSet'ов, не для RouterInfo или Destination'ов |
| MLKEM1024_X25519 | 32 | 0.9.xx | См. предложение 169, только для leaseSet'ов, не для RouterInfo или Destination'ов |
| MLKEM512 | 1632 | 0.9.xx | См. предложение 169, только для рукопожатий, не для leaseSet'ов, RouterInfo или Destination'ов |
| MLKEM768 | 2400 | 0.9.xx | См. предложение 169, только для рукопожатий, не для leaseSet'ов, RouterInfo или Destination'ов |
| MLKEM1024 | 3168 | 0.9.xx | См. предложение 169, только для рукопожатий, не для leaseSet'ов, RouterInfo или Destination'ов |
Новые типы открытых ключей для подписи:

#### SigningPublicKey

Гибридные открытые ключи для подписи представляют собой ключ Ed25519, за которым следует PQ ключ, как описано в [черновике IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Тип | Длина (байты) | С версии | Использование |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | См. предложение 169 |
| MLDSA65 | 1952 | 0.9.xx | См. предложение 169 |
| MLDSA87 | 2592 | 0.9.xx | См. предложение 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | См. предложение 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | См. предложение 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | См. предложение 169 |
| MLDSA44ph | 1344 | 0.9.xx | Только для файлов SU3, не для структур netDb |
| MLDSA65ph | 1984 | 0.9.xx | Только для файлов SU3, не для структур netDb |
| MLDSA87ph | 2624 | 0.9.xx | Только для файлов SU3, не для структур netDb |
Составные гибридные открытые ключи подписи состоят из PQ-ключа, за которым следует ключ Ed25519, как указано в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### SigningPrivateKey

Гибридные закрытые ключи подписи представляют собой ключ Ed25519, за которым следует PQ ключ, как описано в [черновике IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодировка и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Тип | Длина (байты) | С версии | Использование |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | См. предложение 169 |
| MLDSA65 | 4032 | 0.9.xx | См. предложение 169 |
| MLDSA87 | 4896 | 0.9.xx | См. предложение 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | См. предложение 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | См. предложение 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | См. предложение 169 |
| MLDSA44ph | 2592 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
| MLDSA65ph | 4064 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
| MLDSA87ph | 4928 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
Составные гибридные закрытые ключи подписи состоят из PQ-ключа, за которым следует ключ Ed25519, как указано в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

Закрытые ключи подписи никогда не передаются по сети. Приложения могут выбрать хранение 32-битного seed-значения, как рекомендовано в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/), вместо расширенного закрытого ключа размером в несколько килобайт. Это зависит от реализации.

#### Подпись

Новые типы подписей:

| Тип | Длина (байт) | С версии | Использование |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | См. предложение 169 |
| MLDSA65 | 3309 | 0.9.xx | См. предложение 169 |
| MLDSA87 | 4627 | 0.9.xx | См. предложение 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | См. предложение 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | См. предложение 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | См. предложение 169 |
| MLDSA44ph | 2484 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
| MLDSA65ph | 3373 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
| MLDSA87ph | 4691 | 0.9.xx | Только для файлов SU3, не для структур netDb. См. предложение 169 |
Составные гибридные подписи представляют собой подпись PQ, за которой следует подпись Ed25519, как указано в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Гибридные подписи проверяются путём проверки обеих подписей, и в случае неудачи одной из них проверка считается неудачной. Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Сертификаты ключей

Гибридные открытые ключи для подписи представляют собой ключ Ed25519, за которым следует PQ ключ, как описано в [черновике IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Тип | Код типа | Общая длина открытого ключа | С версии | Использование |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | См. предложение 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | См. предложение 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | См. предложение 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | См. предложение 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | См. предложение 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | См. предложение 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Только для файлов SU3 |
| MLDSA65ph | 19 | n/a | 0.9.xx | Только для файлов SU3 |
| MLDSA87ph | 20 | n/a | 0.9.xx | Только для файлов SU3 |
Новые типы криптографических публичных ключей:

| Тип | Код типа | Общая длина публичного ключа | С версии | Использование |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | См. предложение 169, только для LeaseSet, не для RI или Destination |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | См. предложение 169, только для LeaseSet, не для RI или Destination |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | См. предложение 169, только для LeaseSet, не для RI или Destination |
| NONE | 255 | 0 | 0.9.xx | См. предложение 169 |
Гибридные типы ключей НИКОГДА не включаются в сертификаты ключей; только в leaseSet.

Для адресатов с гибридным или PQ типами подписи используйте NONE (тип 255) для типа шифрования, но при этом отсутствует криптографический ключ, а все 384 байта основного раздела предназначены для ключа подписи.

#### Размеры назначений

Вот длины для новых типов Destination. Тип шифрования для всех - NONE (тип 255), и длина ключа шифрования считается равной 0. Вся 384-байтовая секция используется для первой части публичного ключа подписи. ПРИМЕЧАНИЕ: Это отличается от спецификации для типов подписей ECDSA_SHA512_P521 и RSA, где мы сохраняли 256-байтовый ключ ElGamal в destination, даже если он не использовался.

Без заполнения. Общая длина составляет 7 + общая длина ключа. Длина сертификата ключа — 4 + избыточная длина ключа.

Пример 1319-байтового потока байтов назначения для MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Тип | Код типа | Общая длина публичного ключа | Основная | Избыток | Общая длина Dest |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Размеры RouterIdent

Вот длины для новых типов Destination. Тип шифрования для всех — X25519 (тип 4). Вся 352-байтная секция после публичного ключа X25519 используется для первой части публичного ключа подписи. Без заполнения. Общая длина составляет 39 + общая длина ключа. Длина сертификата ключа составляет 4 + избыточная длина ключа.

Пример 1351-байтового потока байтов идентификатора маршрутизатора для MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Тип | Код типа | Общая длина публичного ключа | Основной | Избыток | Общая длина RouterIdent |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### Композитные подписи

Добавьте новую спецификацию для составных алгоритмов подписи следующим образом: составные гибридные подписи определяются, как указано в [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Однако, как обычно, открытые ключи и подписи в I2P не используют DER-кодирование.

Составные подписи всегда используют предварительное хеширование, поэтому потенциально большие сообщения не нужно обрабатывать дважды. Это внешний по отношению к алгоритму MLDSA процесс; мы используем стандартный MLDSA, а не HashML-DSA.

#### Алгоритм подписи

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Алгоритм проверки

То же, что и алгоритм подписи. Ошибка, если любая подпись не проходит проверку.

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Новый формат сессии (с привязкой)

[COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/) не определяет комбинацию MLDSA87 + Ed25519, предположительно из-за несоответствия в уровне стойкости. В нём определена комбинация MLDSA87 + Ed448 с использованием SHAKE256/64 в качестве функции предварительного хеширования. Эта комбинация в настоящее время не включена в данное предложение, поскольку мы в настоящее время не поддерживаем Ed448.

### Паттерны рукопожатия

Пожатия руки используют шаблоны рукопожатий [протокола Noise](https://noiseprotocol.org/noise.html).

Используется следующее соответствие букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения
- e1 = одноразовый эфемерный PQ ключ, отправленный от Alice к Bob
- ekem1 = шифротекст KEM, отправленный от Bob к Alice

Следующие модификации для XK и IK с гибридной сквозной секретностью (hfs) указаны в разделе 5 [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Шаблон e1 определяется следующим образом, как указано в разделе 4 [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
Шаблон ekem1 определяется следующим образом, как указано в разделе 4 [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
### Noise Handshake KDF

#### 1b) Новый формат сессии (с привязкой)

- Следует ли нам изменить хеш-функцию handshake? См. [сравнение](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 не уязвим к PQ, но если мы хотим обновить
  нашу хеш-функцию, сейчас самое время, пока мы меняем другие вещи.
  Текущее предложение IETF SSH [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) — использовать MLKEM768
  с SHA256 и MLKEM1024 с SHA384. Это предложение включает
  обсуждение соображений безопасности.
- Следует ли нам прекратить отправку 0-RTT ratchet данных (кроме LS)?
- Следует ли нам переключить ratchet с IK на XK, если мы не отправляем 0-RTT данные?

#### Обзор

Этот раздел применяется к протоколам IK и XK.

Гибридное рукопожатие определено в [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Первое сообщение от Алисы к Бобу содержит e1 — ключ инкапсуляции — перед полезной нагрузкой сообщения. Он обрабатывается как дополнительный статический ключ; примените к нему EncryptAndHash() (если вы Алиса) или DecryptAndHash() (если вы Боб). Затем обработайте полезную нагрузку сообщения обычным образом.

Второе сообщение от Боба к Алисе содержит ekem1, зашифрованный текст, перед полезной нагрузкой сообщения. Это рассматривается как дополнительный статический ключ; вызовите EncryptAndHash() для него (как Боб) или DecryptAndHash() (как Алиса). Затем вычислите kem_shared_key и вызовите MixKey(kem_shared_key). После этого обработайте полезную нагрузку сообщения как обычно.

#### Определённые операции ML-KEM

Мы определяем следующие функции, соответствующие криптографическим компонентам, используемым в соответствии с [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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

Обратите внимание, что encap_key и шифротекст зашифрованы внутри блоков ChaCha/Poly в сообщениях рукопожатия Noise 1 и 2. Они будут расшифрованы в ходе процесса рукопожатия.

kem_shared_key смешивается с chaining key при помощи MixHash(). Подробности см. ниже.

#### Alice KDF для сообщения 1

Для XK: после шаблона сообщения 'es' и перед полезной нагрузкой добавьте:

ИЛИ

Для IK: После шаблона сообщения 'ee' и перед шаблоном сообщения 'se', добавить:

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
#### Bob KDF для сообщения 1

Для XK: после шаблона сообщения 'es' и перед полезной нагрузкой добавьте:

ИЛИ

Для IK: После шаблона сообщения 'es' и перед шаблоном сообщения 's' добавьте:

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
#### KDF Боба для Сообщения 2

Для XK: после шаблона сообщения 'ee' и перед полезной нагрузкой добавьте:

ИЛИ

Зашифрованный формат:

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
#### Alice KDF для сообщения 2

После шаблона сообщения 'ee' (и перед шаблоном сообщения 'ss' для IK), добавить:

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
#### KDF для Сообщения 3 (только XK)

неизменный

#### KDF для split()

неизменный

### Храповик

Обновить спецификацию ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) следующим образом:

#### Длинный заголовок

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Короткий заголовок

Изменения: Текущий ratchet содержал статический ключ в первой секции ChaCha и полезную нагрузку во второй секции. С ML-KEM теперь есть три секции. Первая секция содержит зашифрованный PQ публичный ключ. Вторая секция содержит статический ключ. Третья секция содержит полезную нагрузку.

Расшифрованный формат:

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
```
Расшифрованный формат:

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Размеры:

| Тип | Код типа | Длина X | Длина сообщения 1 | Длина зашифр. сообщения 1 | Длина расшифр. сообщения 1 | Длина PQ ключа | Длина pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Обратите внимание, что полезная нагрузка должна содержать блок DateTime, поэтому минимальный размер полезной нагрузки составляет 7. Минимальные размеры сообщения 1 могут быть рассчитаны соответственно.

#### 1g) Формат ответа о новой сессии

Изменения: текущий ratchet имеет пустое полезное содержимое в первом разделе ChaCha и полезную нагрузку во втором разделе. При использовании ML-KEM теперь есть три раздела: первый содержит зашифрованный PQ-шифртекст, второй — пустое полезное содержимое, а третий — полезную нагрузку.

Зашифрованный формат:

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
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
```
Расшифрованный формат:

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Размеры:

| Тип | Код типа | Длина Y | Длина сообщения 2 | Длина зашифр. сообщения 2 | Длина расшифр. сообщения 2 | Длина PQ CT | Длина опций |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Обратите внимание, что хотя сообщение 2 обычно имеет ненулевую полезную нагрузку, спецификация ratchet [/docs/specs/ecies/](/docs/specs/ecies/) не требует этого, поэтому минимальный размер полезной нагрузки составляет 0. Минимальные размеры сообщения 2 могут быть рассчитаны соответственно.

### NTCP2

Обновите спецификацию NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) следующим образом:

#### Идентификаторы Noise

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Изменения: текущий NTCP2 содержит только параметры в одном разделе ChaCha. С ML-KEM появится новый раздел ChaCha перед параметрами, содержащий зашифрованный квантово-устойчивый открытый ключ.

Чтобы PQ и не-PQ NTCP2 могли поддерживаться на одном адресе и порту router'а, мы используем старший бит значения X (X25519 эфемерный открытый ключ) для обозначения PQ-соединения. Этот бит всегда сброшен для не-PQ соединений.

Примечание: поле версии в блоке опций сообщения 1 должно быть установлено в 2, даже для PQ-соединений.

Для Боба, после AES де-обфускации X, проверить X[31] & 0x80. Если бит установлен, очистить его с помощью X[31] &= 0x7f и расшифровать через Noise как PQ соединение. Если бит не установлен, расшифровать через Noise как обычное не-PQ соединение.

Для PQ NTCP2, анонсируемого на другом адресе и порту router'а, это не требуется.

Для получения дополнительной информации см. раздел "Опубликованные адреса" ниже.

Необработанное содержимое:

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Незашифрованные данные (тег аутентификации Poly1305 не показан):

```
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
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указываться в адресах router.

Размеры:

| Тип | Код типа | X длина | Длина сообщ. 1 | Длина зашифр. сообщ. 1 | Длина расшифр. сообщ. 1 | Длина PQ ключа | Длина опций |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

#### 2) SessionCreated

Необработанное содержимое:

Необработанное содержимое:

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Размеры:

```
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
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Размеры:

| Тип | Код типа | Длина Y | Длина Msg 2 | Длина Msg 2 Enc | Длина Msg 2 Dec | Длина PQ CT | Длина opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

#### 3) SessionConfirmed

Неизменно

#### Функция вывода ключей (KDF) (для фазы данных)

Неизменно

#### Опубликованные адреса

Во всех случаях используйте имя транспорта NTCP2 как обычно.

Используйте тот же адрес/порт, что и для non-PQ без firewall. Поддерживается только один вариант PQ. В адресе router опубликуйте v=2 (как обычно) и новый параметр pq=[3|4|5], чтобы указать MLKEM 512/768/1024. Alice устанавливает старший бит эфемерного ключа (key[31] & 0x80) в запросе сессии, чтобы указать, что это гибридное соединение. См. выше. Более старые router'ы проигнорируют параметр pq и подключатся без PQ, как обычно.

Адреса за firewall (IP не публикуется): В адресе router'а публикуйте v=2 (как обычно). Нет необходимости публиковать параметр pq.

Alice может подключиться к PQ Bob, используя PQ вариант, который публикует Bob, независимо от того, рекламирует ли Alice поддержку pq в информации своего router или рекламирует ли она тот же вариант.

В текущей спецификации сообщения 1 и 2 определены как имеющие "разумное" количество заполнения, с рекомендуемым диапазоном 0-31 байт и без указанного максимума.

#### Максимальное заполнение

Java I2P реализует максимум 256 байт заполнения для не-PQ соединений, однако это не было задокументировано ранее.

Используйте определенный размер сообщения как максимальное заполнение, то есть максимальное заполнение удвоит размер сообщения следующим образом:

Используйте заданный размер сообщения в качестве максимального заполнения, то есть максимальное заполнение удвоит размер сообщения для PQ-соединений, как показано ниже:

| Максимальное заполнение сообщения | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|-----------|-----------|------------|
| Session Request  |       880   |     1264   |    1648  |
| Session Created  |       848   |     1136   |    1616	 |
### SSU2

Обратите внимание, что MLKEM-1024 НЕ поддерживается для SSU2, поскольку ключи слишком большие, чтобы поместиться в стандартную датаграмму размером 1500 байт.

#### Идентификаторы Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Длинный заголовок составляет 32 байта. Он используется до создания сессии для сообщений Token Request, SessionRequest, SessionCreated и Retry. Он также используется для сообщений Peer Test и Hole Punch вне сессии.

#### Прямая секретность

В следующих сообщениях установите поле ver (версия) в длинном заголовке в 3 или 4, чтобы указать MLKEM-512 или MLKEM-768.

В следующих сообщениях устанавливайте поле ver (версия) в длинном заголовке равным 2, как обычно, даже если поддерживается MLKEM-512 или MLKEM-768. Реализации также могут устанавливать значение 3 или 4, если другая сторона это поддерживает, но это не обязательно. Реализации должны принимать любое значение от 2 до 4.

- (0) Запрос сеанса
- (1) Сеанс создан
- (9) Повтор (примечание: Повтор с завершением может содержать любую версию 2-4)
- (10) Запрос токена
- (11) Пробивка отверстия (Hole Punch)

Незашифрованные данные (тег аутентификации Poly1305 не показан):

- (7) Тест узла (сообщения вне сессии 5-7)

Размеры, не включая накладные расходы IP:

- Запрос ретрансляции
- Ответ ретрансляции
- Введение ретрансляции
- Тест пира

Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

неизменный

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
#### Размер новой сессии

неизменный

#### SessionRequest (Тип 0)

Изменение KDF для защиты от спуфинга: Для решения проблем, поднятых в Предложении 165 [Prop165]_, но с другим решением, мы модифицируем KDF для Session Request. Это касается только PQ-сессий. KDF для не-PQ сессий остается неизменным.

Исходное содержимое:

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
Минимальный MTU для MLKEM768_X25519: Около 1316 для IPv4 и 1336 для IPv6.

| Тип | Код типа | Длина X | Длина Msg 1 | Длина Msg 1 Enc | Длина Msg 1 Dec | Длина PQ ключа | Длина pl |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | н/д | слишком большой | | | | |
Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

Изменения: Текущий SSU2 содержит только блочные данные в секции ChaCha. С ML-KEM секция ChaCha также будет содержать зашифрованный PQ публичный ключ.

Незашифрованные данные (тег аутентификации Poly1305 не показан):

#### SessionCreated (Тип 1)

Исходное содержимое:

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
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
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
Размеры:

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
Размеры, не включая накладные расходы IP:

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | слишком велик | | | | |
Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

Изменения: Текущий SSU2 содержит только блочные данные в секции ChaCha. С ML-KEM секция ChaCha также будет содержать зашифрованный PQ публичный ключ.

PQ-подписи: блоки Relay, блоки Peer Test и сообщения Peer Test содержат подписи. К сожалению, PQ-подписи больше MTU. В настоящее время отсутствует механизм фрагментации блоков Relay или Peer Test или сообщений между несколькими UDP-пакетами. Протокол должен быть расширен для поддержки фрагментации. Это будет сделано в отдельном предложении (TBD). До завершения этой работы Relay и Peer Test поддерживаться не будут.

#### SessionConfirmed (Тип 2)

неизменный

#### KDF для фазы данных

неизменный

#### Тестирование реле и узлов

Следующие блоки содержат поля версии. Они останутся версии 2 (для совместимости с не-PQ Bob) и не изменятся на версию 3/4 для PQ.

- SAMv3
- Bittorrent
- Руководство для разработчиков
- Именование / адресная книга / jump-серверы
- Другая документация

Во всех случаях используйте имя транспорта SSU2 как обычно. MLKEM-1024 не поддерживается.

#### Опубликованные адреса

Используйте тот же адрес/порт, что и для non-PQ, non-firewalled. Поддерживается один или оба варианта PQ. В адресе router публикуйте v=2 (как обычно) и новый параметр pq=[3|4|3,4] для указания MLKEM 512/768/оба. Старые router проигнорируют параметр pq и подключатся non-pq как обычно.

Будьте осторожны, чтобы не превысить MTU при использовании MLKEM768. Минимальный MTU для SSU2 составляет 1280, что является размером сообщения 1 без заполнения. Не включайте заполнение в сообщение 1, если MTU Alice или Bob составляет 1280.

Адреса за файрволлом (IP не публикуется): В адресе router публикуйте v=2 (как обычно). Параметр pq ДОЛЖЕН быть опубликован в адресах за файрволлом для поддержки relay.

Алиса может подключиться к PQ Бобу, используя PQ вариант, который публикует Боб, независимо от того, рекламирует ли Алиса поддержку pq в своей информации router или рекламирует ли она тот же вариант.

В текущей спецификации сообщения 1 и 2 определены как имеющие "разумное" количество заполнения, с рекомендуемым диапазоном 0-31 байт и без указанного максимума.

#### MTU

Мы могли бы внутренне использовать поле версии и применять 3 для MLKEM512 и 4 для MLKEM768.

### Стриминг

Для сообщений 1 и 2, MLKEM768 увеличил бы размеры пакетов сверх минимального MTU в 1280. Вероятно, просто не будем поддерживать его для этого соединения, если MTU слишком низкий.

### SU3 файлы

Для сообщений 1 и 2 MLKEM1024 увеличит размеры пакетов сверх максимального MTU в 1500 байт. Это потребует фрагментации сообщений 1 и 2, что станет серьезным усложнением. Скорее всего, мы этого делать не будем.

Relay и Peer Test: См. выше

TODO: Существует ли более эффективный способ определения подписывания/верификации, чтобы избежать копирования подписи?

ЗАДАЧИ

[Черновик IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) раздел 8.1 запрещает использование HashML-DSA в сертификатах X.509 и не назначает OID для HashML-DSA из-за сложностей реализации и снижения безопасности.

### Другие спецификации

Новый максимальный размер Destination составит 2599 (3468 в base 64).

Обратите внимание, что мы запрещаем подписывание файлов SU3 с помощью Ed25519, и хотя мы определили подписывание Ed25519ph, мы никогда не согласовали для него OID и не использовали его.

- Если сообщение 1 меньше 919 байт, это текущий ratchet протокол.
- Если сообщение 1 больше или равно 919 байт, это вероятно MLKEM512_X25519.
  Сначала попробуйте MLKEM512_X25519, и если это не сработает, попробуйте текущий ratchet протокол.

## Анализ накладных расходов

### Обмен ключами

Обычные типы подписей не разрешены для файлов SU3; используйте варианты ph (prehash).

| Тип | Pubkey (Сообщение 1) | Cipertext (Сообщение 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Новый максимальный размер Destination будет 2599 (3468 в base 64).

Обновить другие документы, которые дают рекомендации по размерам Destination, включая:

| Тип | Относительная скорость |
|------|----------------|
| X25519 DH/keygen | базовая |
| MLKEM512 | в 2,25 раза быстрее |
| MLKEM768 | в 1,5 раза быстрее |
| MLKEM1024 | 1x (то же самое) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = на 22% медленнее |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = на 32% медленнее |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = на 50% медленнее |
Увеличение размера (байты):

| Тип | Относительное DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | базовый | базовый | базовый |
| MLKEM512 | в 29 раз быстрее | в 22 раза быстрее | в 17 раз быстрее |
| MLKEM768 | в 17 раз быстрее | в 14 раз быстрее | в 9 раз быстрее |
| MLKEM1024 | в 12 раз быстрее | в 10 раз быстрее | в 6 раз быстрее |
### Подписи

#### Размеры

Скорости согласно отчёту [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Тип | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (каждое сообщение) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | базовое | базовое |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Скорость

Обновить другие документы, которые дают рекомендации по размерам Destination, включая:

| Тип | Относительная скорость подписи | верификация |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | базовая | базовая |
| MLDSA44 | в 5 раз медленнее | в 2 раза быстрее |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Увеличение размера (байты):

| Тип | Относительная скорость подписи | верификация | генерация ключей |
|------|--------------------------------|-------------|------------------|
| EdDSA_SHA512_Ed25519 | базовая | базовая | базовая |
| MLDSA44 | в 4.6 раза медленнее | в 1.7 раза быстрее | в 2.6 раза быстрее |
| MLDSA65 | в 8.1 раза медленнее | такая же | в 1.5 раза быстрее |
| MLDSA87 | в 11.1 раза медленнее | в 1.5 раза медленнее | такая же |
## Анализ безопасности

Типичные размеры ключей, подписей, RIdent, Dest или увеличения размера (Ed25519 включён для справки) при условии типа шифрования X25519 для RI. Указано добавленное увеличение размера для Router Info, LeaseSet, отвечаемых датаграмм и каждого из двух пакетов потокового режима (SYN и SYN ACK). Текущие Destinations и Leasesets содержат повторяющееся заполнение и могут сжиматься при передаче. Новые типы не содержат заполнения и не будут сжиматься, что приведёт к значительно большему увеличению размера при передаче. См. раздел проектирования выше.

| Категория | Уровень безопасности |
|-----------|---------------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Рукопожатия

Скорости по данным [Cloudflare](https://blog.cloudflare.com/pq-2024/):

Предварительные результаты тестов на Java:

| Алгоритм | Категория безопасности |
|----------|------------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Подписи

Категории безопасности NIST кратко изложены в [презентации NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) на слайде 10. Предварительные критерии: Наша минимальная категория безопасности NIST должна быть 2 для гибридных протоколов и 3 для протоколов только с постквантовой криптографией.

Это все гибридные протоколы. Реализации должны предпочитать MLKEM768; MLKEM512 недостаточно безопасен.

| Алгоритм | Категория безопасности |
|----------|------------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Настройки типа

Категории безопасности NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

Данное предложение определяет как гибридные, так и только PQ типы подписей. Гибридный MLDSA44 предпочтительнее чем только PQ MLDSA65. Размеры ключей и подписей для MLDSA65 и MLDSA87 вероятно слишком велики для нас, по крайней мере поначалу.

Категории безопасности NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

Хотя мы определим и реализуем 3 криптографических и 9 типов подписей, мы планируем измерять производительность в процессе разработки и дополнительно анализировать влияние увеличенных размеров структур. Мы также продолжим исследования и мониторинг разработок в других проектах и протоколах.

После года или более разработки мы попытаемся остановиться на предпочтительном типе или настройке по умолчанию для каждого случая использования. Выбор потребует компромиссов между пропускной способностью, CPU и предполагаемым уровнем безопасности. Все типы могут быть не подходящими или не разрешенными для всех случаев использования.

Предварительные настройки следующие, могут быть изменены:

Шифрование: MLKEM768_X25519

## Примечания по реализации

### Поддержка библиотек

Подписи: MLDSA44_EdDSA_SHA512_Ed25519

Предварительные ограничения следующие, могут быть изменены:

### Варианты подписи

Шифрование: MLKEM1024_X25519 не разрешено для SSU2

Подписи: MLDSA87 и гибридный вариант вероятно слишком большие; MLDSA65 и гибридный вариант могут быть слишком большими

### Надежность

Библиотеки Bouncycastle, BoringSSL и WolfSSL теперь поддерживают MLKEM и MLDSA. Поддержка OpenSSL будет в их релизе 3.5 от 8 апреля 2025 года [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Размеры структур

Библиотека Noise от southernstorm.com, адаптированная для Java I2P, содержала предварительную поддержку гибридных рукопожатий, но мы удалили её как неиспользуемую; нам придётся добавить её обратно и обновить для соответствия [спецификации Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### NetDB

Мы будем использовать "защищенный" или рандомизированный вариант подписи, а не "детерминистический" вариант, как определено в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) раздел 3.4. Это гарантирует, что каждая подпись будет отличаться, даже при подписи одних и тех же данных, и обеспечивает дополнительную защиту от атак по побочным каналам. Хотя [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) указывает, что "защищенный" вариант является вариантом по умолчанию, это может быть или не быть правдой в различных библиотеках. Разработчики должны убедиться, что для подписи используется "защищенный" вариант.

### Храповик

#### Проблемы

Мы используем обычный процесс подписи (называемый Pure ML-DSA Signature Generation), который кодирует сообщение внутренне как 0x00 || len(ctx) || ctx || message, где ctx — это некоторое опциональное значение размером 0x00..0xFF. Мы не используем никакого опционального контекста. len(ctx) == 0. Этот процесс определён в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Алгоритм 2 шаг 10 и Алгоритм 3 шаг 5. Обратите внимание, что некоторые опубликованные тестовые векторы могут требовать установки режима, в котором сообщение не кодируется.

Увеличение размера приведет к гораздо большей фрагментации tunnel для хранилищ netDb, рукопожатий потоковой передачи и других сообщений. Проверьте изменения производительности и надежности.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Найдите и проверьте любой код, который ограничивает размер в байтах router info и leaseSet.

Пересмотреть и возможно уменьшить максимальное количество LS/RI, хранящихся в ОЗУ или на диске, чтобы ограничить рост объема хранилища. Увеличить минимальные требования к пропускной способности для floodfill-узлов?

- Более одного MLKEM
- ElG + один или более MLKEM
- X25519 + один или более MLKEM
- ElG + X25519 + один или более MLKEM

Автоматическая классификация/обнаружение множественных протоколов на одних и тех же туннелях должна быть возможна на основе проверки длины сообщения 1 (New Session Message). Используя MLKEM512_X25519 в качестве примера, длина сообщения 1 на 816 байт больше, чем в текущем ratchet протоколе, и минимальный размер сообщения 1 (с включением только полезной нагрузки DateTime) составляет 919 байт. Большинство размеров сообщения 1 в текущем ratchet имеют полезную нагрузку менее 816 байт, поэтому они могут быть классифицированы как не-гибридный ratchet. Крупные сообщения, вероятно, являются POST-запросами, которые встречаются редко.

- Выбор Noise Hash - остаться с SHA256 или обновиться?
  SHA256 должен быть хорош ещё 20-30 лет, не угрожает PQ,
  См. [презентацию NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) и [презентацию NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Если SHA256 сломан, у нас будут худшие проблемы (netdb).
- NTCP2 отдельный порт, отдельный адрес router
- SSU2 relay / peer test
- SSU2 поле версии
- SSU2 версия адреса router

Итак, рекомендуемая стратегия:

Это должно позволить нам эффективно поддерживать стандартный ratchet и гибридный ratchet на одном и том же назначении, точно так же, как мы ранее поддерживали ElGamal и ratchet на одном назначении. Поэтому мы можем перейти на гибридный протокол MLKEM гораздо быстрее, чем если бы мы не могли поддерживать двойные протоколы для одного назначения, поскольку мы можем добавить поддержку MLKEM к существующим назначениям.

Обязательные поддерживаемые комбинации:

Следующие комбинации могут быть сложными и НЕ обязательны к поддержке, но могут поддерживаться в зависимости от реализации:

#### Общие туннели

Мы можем не пытаться поддерживать несколько алгоритмов MLKEM (например, MLKEM512_X25519 и MLKEM_768_X25519) на одном и том же назначении. Выберите только один; однако это зависит от того, выберем ли мы предпочтительный вариант MLKEM, чтобы HTTP клиентские туннели могли использовать один из них. Зависит от реализации.

#### Размер новой сессии

Мы МОЖЕМ попытаться поддерживать три алгоритма (например X25519, MLKEM512_X25519 и MLKEM769_X25519) на одном и том же назначении. Классификация и стратегия повторных попыток могут быть слишком сложными. Конфигурация и пользовательский интерфейс конфигурации могут быть слишком сложными. Зависит от реализации.

### NTCP2

Мы, вероятно, НЕ будем пытаться поддерживать алгоритмы ElGamal и гибридные алгоритмы на одном и том же назначении. ElGamal устарел, а ElGamal + гибридный алгоритм только (без X25519) не имеет особого смысла. Кроме того, сообщения New Session для ElGamal и гибридных алгоритмов оба имеют большой размер, поэтому стратегии классификации часто должны были бы пробовать оба варианта расшифровки, что было бы неэффективно. Зависит от реализации.

#### Обфускация

Клиенты могут использовать одинаковые или разные статические ключи X25519 для протоколов X25519 и гибридного протокола на одних и тех же туннелях, в зависимости от реализации.

Спецификация ECIES позволяет включать Garlic Messages в полезную нагрузку New Session Message, что обеспечивает доставку начального streaming-пакета с нулевым RTT (0-RTT), обычно HTTP GET, вместе с leaseSet клиента. Однако полезная нагрузка New Session Message не обладает прямой секретностью. Поскольку данное предложение делает акцент на усиленной прямой секретности для ratchet, реализации могут или должны отложить включение streaming-полезной нагрузки или полного streaming-сообщения до первого Existing Session Message. Это произойдет за счет отказа от доставки 0-RTT. Стратегии также могут зависеть от типа трафика или типа tunnel, или от GET против POST, например. Зависит от реализации.

MLKEM, MLDSA или оба на одном и том же destination значительно увеличат размер сообщения New Session Message, как описано выше. Это может существенно снизить надежность доставки сообщений New Session Message через tunnel, где они должны быть фрагментированы на несколько сообщений tunnel размером 1024 байта. Успех доставки пропорционален экспоненциальному числу фрагментов. Реализации могут использовать различные стратегии для ограничения размера сообщения за счет доставки 0-RTT. Зависит от реализации.

Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

### SSU2

Мы устанавливаем MSB эфемерного ключа (key[31] & 0x80) в запросе сессии, чтобы указать, что это гибридное соединение. Это позволяет нам запускать как стандартный NTCP, так и гибридный NTCP на одном и том же порту. Поддерживался бы только один гибридный вариант, который рекламировался бы в адресе router. Например, v=2,3 или v=2,4 или v=2,5.

Как Bob, проверьте, если (X[31] & 0x80) != 0 после деобфускации. Если да, то это PQ соединение.

Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

## Совместимость router

### Названия транспортов

Минимальная версия router, необходимая для NTCP2-PQ, будет определена позже.

### Типы шифрования router

Мы используем поле версии в длинном заголовке и устанавливаем его в 3 для MLKEM512 и 4 для MLKEM768. v=2,3,4 в адресе будет достаточно.

#### Обфускация

Проверить и убедиться, что SSU2 может обрабатывать MLDSA-подписанный RI, фрагментированный на несколько пакетов (6-8?).

#### Маршрутизаторы типа 5/6/7

Примечание: Коды типов предназначены только для внутреннего использования. Router останутся типа 4, а поддержка будет указана в адресах router.

#### Routers типа 4

Во всех случаях используйте имена транспортов NTCP2 и SSU2 как обычно.

### Типы подписей router

#### Рекомендации

У нас есть несколько альтернатив для рассмотрения:

Не рекомендуется. Используйте только новые транспорты, перечисленные выше, которые соответствуют типу router. Старые router не могут подключаться, строить tunnel через них или отправлять netDb сообщения. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию. Может продлить развертывание на год или более по сравнению с альтернативами ниже.

### Типы шифрования LS

#### Router типа 12-17

Рекомендуется. Поскольку PQ не влияет на статический ключ X25519 или протоколы handshake N, мы можем оставить router как тип 4 и просто анонсировать новые транспорты. Старые router всё ещё смогут подключаться, строить tunnel через них или отправлять сообщения netDb.

MLKEM-768 рекомендуется для Ratchet, NTCP2 и SSU2, как лучший баланс безопасности и длины ключа.

### Типы подписей назначения

#### Ключи LS типа 5-7

Старые router'ы проверяют RI и поэтому не могут подключаться, строить tunnel'ы через них или отправлять netDb сообщения. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию. Будут те же проблемы, что и при развертывании enc. типа 5/6/7; может продлить развертывание на год или более по сравнению с альтернативой развертывания enc. типа 4, указанной выше.

Не рекомендуется. Используйте только новые транспорты, перечисленные выше, которые соответствуют типу router. Старые router не могут подключаться, строить tunnel через них или отправлять netDb сообщения. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию. Может продлить развертывание на год или более по сравнению с альтернативами ниже.

## Приоритеты и развертывание

Нет альтернатив.

Destinations могут поддерживать несколько типов ключей, но только путем пробной расшифровки сообщения 1 с каждым ключом. Накладные расходы можно снизить, ведя подсчет успешных расшифровок для каждого ключа и сначала пробуя наиболее используемый ключ. Java I2P использует эту стратегию для ElGamal+X25519 на одном и том же destination.

Роутеры проверяют подписи leaseSet и поэтому не могут подключиться или получить leaseSet для назначений типа 12-17. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию.

Альтернативы отсутствуют.

Наиболее ценными данными является сквозной трафик, зашифрованный с помощью ratchet. Для внешнего наблюдателя между хопами tunnel'а данные зашифрованы еще дважды — шифрованием tunnel'а и транспортным шифрованием. Для внешнего наблюдателя между OBEP и IBGW данные зашифрованы только еще раз транспортным шифрованием. Для участника OBEP или IBGW единственным шифрованием является ratchet. Однако, поскольку tunnel'ы однонаправленные, перехват обоих сообщений в ratchet handshake потребовал бы сговора router'ов, если только tunnel'ы не были построены с OBEP и IBGW на одном router'е.

Модель угроз PQ, связанная со взломом ключей аутентификации за разумный период времени (скажем, несколько месяцев) с последующей подменой аутентификации или расшифровкой в почти реальном времени, намного более отдалена? И вот тогда мы захотим перейти к статическим ключам PQC.

Работа над поддержкой подписей MLDSA в I2P приостановлена до конца 2027 или 2028 года, ожидая решений от органов по стандартизации по выбору алгоритмов, возможному уменьшению размеров ключей и/или подписей, а также стимулированию внедрения в отрасли. См. [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/), и [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Кроме того, внедрение MLDSA в отрасли будет стандартизировано IETF, CA/Browser Forum и центрами сертификации. Центрам сертификации сначала потребуется поддержка аппаратных модулей безопасности (HSM), которой в настоящее время нет [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Мы ожидаем, что IETF и CA/Browser Forum будут определять решения по конкретным параметрам, включая вопрос о поддержке или требовании составных подписей [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Веха | Целевая дата |
|-----------|--------|
| Ratchet бета | Конец 2025 |
| Выбор лучшего типа шифрования | Начало 2026 |
| NTCP2 бета | Начало 2026 |
| SSU2 бета | Середина 2026 |
| Ratchet продакшн | Середина 2026 |
| Ratchet по умолчанию | Конец 2026 |
| Подпись бета | Конец 2026 |
| NTCP2 продакшн | Конец 2026 |
| SSU2 продакшн | Начало 2027 |
| Выбор лучшего типа подписи | Начало 2027 |
| NTCP2 по умолчанию | Начало 2027 |
| SSU2 по умолчанию | Середина 2027 |
| Подпись продакшн | Середина 2027 |
## Миграция

Ratchet имеет наивысший приоритет. Транспорты следующие по приоритету. Подписи имеют самый низкий приоритет.

Развертывание подписей также произойдет на год или более позже развертывания шифрования, поскольку обратная совместимость невозможна. Кроме того, принятие MLDSA в индустрии будет стандартизовано CA/Browser Forum и центрами сертификации. ЦС сначала нужна поддержка аппаратных модулей безопасности (HSM), которая в настоящее время недоступна [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Мы ожидаем, что CA/Browser Forum будет определять решения по конкретному выбору параметров, включая поддержку или требование композитных подписей [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## Проблемы

SHA256 должен оставаться надёжным ещё 20-30 лет, он не под угрозой со стороны постквантовых атак. См. [презентацию NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) и [презентацию NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Если SHA256 будет взломан, у нас возникнут гораздо более серьёзные проблемы (netDb).

## Ссылки

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
