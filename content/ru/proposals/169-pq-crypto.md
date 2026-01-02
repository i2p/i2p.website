---
title: "Протоколы постквантовой криптографии"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Открыть"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Обзор

Хотя исследования и конкуренция за подходящую постквантовую (PQ) криптографию ведутся уже десятилетие, выбор стал очевидным лишь недавно.

Мы начали изучать последствия PQ криптографии в 2022 году [zzz.i2p](http://zzz.i2p/topics/3294).

Стандарты TLS добавили поддержку гибридного шифрования за последние два года, и теперь оно используется для значительной части зашифрованного трафика в интернете благодаря поддержке в Chrome и Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

NIST недавно завершил и опубликовал рекомендуемые алгоритмы для постквантовой криптографии [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Несколько распространённых криптографических библиотек теперь поддерживают стандарты NIST или выпустят поддержку в ближайшем будущем.

И [Cloudflare](https://blog.cloudflare.com/pq-2024/), и [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) рекомендуют начать миграцию немедленно. См. также FAQ NSA по постквантовой криптографии 2022 года [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P должен быть лидером в области безопасности и криптографии. Сейчас самое время реализовать рекомендованные алгоритмы. Используя нашу гибкую систему типов шифрования и типов подписей, мы добавим типы для гибридного шифрования, а также для постквантовых и гибридных подписей.

## Цели

- Выберите PQ-устойчивые алгоритмы
- Добавьте PQ-only и гибридные алгоритмы в протоколы I2P там, где это уместно
- Определите множественные варианты
- Выберите лучшие варианты после реализации, тестирования, анализа и исследования
- Добавьте поддержку постепенно и с обратной совместимостью

## Не-цели

- Не изменяйте односторонние (Noise N) протоколы шифрования
- Не отказывайтесь от SHA256, в ближайшем будущем не угрожает PQ
- Не выбирайте окончательные предпочтительные варианты в настоящее время

## Модель угроз

- Маршрутизаторы на OBEP или IBGW, возможно действующие сообща,
  сохраняющие garlic-сообщения для последующей расшифровки (forward secrecy)
- Наблюдатели сети,
  сохраняющие транспортные сообщения для последующей расшифровки (forward secrecy)
- Участники сети, подделывающие подписи для RI, LS, потоков, датаграмм
  или других структур

## Затронутые протоколы

Мы будем модифицировать следующие протоколы, примерно в порядке разработки. Общее внедрение, вероятно, будет проходить с конца 2025 года до середины 2027 года. Подробности смотрите в разделе «Приоритеты и внедрение» ниже.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Дизайн

Мы будем поддерживать стандарты NIST FIPS 203 и 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), которые основаны на CRYSTALS-Kyber и CRYSTALS-Dilithium (версии 3.1, 3 и более старые), но НЕ совместимы с ними.

### Key Exchange

Мы будем поддерживать гибридный обмен ключами в следующих протоколах:

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM предоставляет только эфемерные ключи и не поддерживает напрямую handshake-процедуры со статическими ключами, такие как Noise XK и IK.

Noise N не использует двусторонний обмен ключами и поэтому не подходит для гибридного шифрования.

Таким образом, мы будем поддерживать только гибридное шифрование для NTCP2, SSU2 и Ratchet. Мы определим три варианта ML-KEM согласно [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), что составит в общей сложности 3 новых типа шифрования. Гибридные типы будут определены только в сочетании с X25519.

Новые типы шифрования:

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
Накладные расходы будут существенными. Типичные размеры сообщений 1 и 2 (для XK и IK) в настоящее время составляют около 100 байт (до любой дополнительной полезной нагрузки). Это увеличится в 8-15 раз в зависимости от алгоритма.

### Signatures

Мы будем поддерживать PQ и гибридные подписи в следующих структурах:

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Таким образом, мы будем поддерживать как PQ-только, так и гибридные подписи. Мы определим три варианта ML-DSA как в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), три гибридных варианта с Ed25519, и три PQ-только варианта с prehash только для файлов SU3, всего 9 новых типов подписей. Гибридные типы будут определены только в сочетании с Ed25519. Мы будем использовать стандартный ML-DSA, НЕ варианты с pre-hash (HashML-DSA), за исключением файлов SU3.

Мы будем использовать "хеджированный" или рандомизированный вариант подписи, а не "детерминистический" вариант, как определено в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) разделе 3.4. Это гарантирует, что каждая подпись будет отличаться, даже при подписании одних и тех же данных, и обеспечивает дополнительную защиту от атак по побочным каналам. См. раздел с примечаниями по реализации ниже для получения дополнительной информации о выборе алгоритмов, включая кодирование и контекст.

Новые типы подписей:

| Type | Code |
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
Сертификаты X.509 и другие кодировки DER будут использовать композитные структуры и OID, определённые в [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

Накладные расходы будут существенными. Типичные размеры назначения Ed25519 и идентичности router составляют 391 байт. Они увеличатся в 3,5-6,8 раза в зависимости от алгоритма. Подписи Ed25519 составляют 64 байта. Они увеличатся в 38-76 раз в зависимости от алгоритма. Типичные подписанные RouterInfo, LeaseSet, отвечаемые датаграммы и подписанные потоковые сообщения составляют около 1КБ. Они увеличатся в 3-8 раз в зависимости от алгоритма.

Поскольку новые типы назначений и идентификаторов router не будут содержать дополнения, они не будут сжимаемыми. Размеры назначений и идентификаторов router, которые сжимаются gzip во время передачи, увеличатся в 12-38 раз в зависимости от алгоритма.

### Legal Combinations

Для Destinations новые типы подписей поддерживаются со всеми типами шифрования в leaseset. Установите тип шифрования в сертификате ключа в NONE (255).

Для RouterIdentities тип шифрования ElGamal является устаревшим. Новые типы подписей поддерживаются только с шифрованием X25519 (тип 4). Новые типы шифрования будут указаны в RouterAddresses. Тип шифрования в сертификате ключа будет по-прежнему типом 4.

### New Crypto Required

- ML-KEM (ранее CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (ранее CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (ранее Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Используется только для SHAKE128
- SHA3-256 (ранее Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 и SHAKE256 (расширения XOF для SHA3-128 и SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Тестовые векторы для SHA3-256, SHAKE128 и SHAKE256 доступны по адресу [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Обратите внимание, что библиотека Java bouncycastle поддерживает все вышеперечисленное. Поддержка библиотеки C++ доступна в OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

Мы не будем поддерживать [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), он намного медленнее и больше, чем ML-DSA. Мы не будем поддерживать предстоящий FIPS206 (Falcon), он еще не стандартизирован. Мы не будем поддерживать NTRU или других PQ-кандидатов, которые не были стандартизированы NIST.

### Rosenpass

Существуют некоторые исследования [paper](https://eprint.iacr.org/2020/379.pdf) по адаптации Wireguard (IK) для чистой PQ криптографии, но в этой статье есть несколько открытых вопросов. Позже этот подход был реализован как Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) для PQ Wireguard.

Rosenpass использует рукопожатие, подобное Noise KK, с предварительно распределёнными статическими ключами Classic McEliece 460896 (по 500 КБ каждый) и эфемерными ключами Kyber-512 (по сути MLKEM-512). Поскольку шифротексты Classic McEliece составляют всего 188 байт, а открытые ключи и шифротексты Kyber-512 имеют разумный размер, оба сообщения рукопожатия помещаются в стандартный UDP MTU. Выходной общий ключ (osk) из PQ KK рукопожатия используется как входной предварительно распределённый ключ (psk) для стандартного Wireguard IK рукопожатия. Таким образом, всего выполняется два полных рукопожатия: одно чисто PQ и одно чисто X25519.

Мы не можем сделать ничего из этого для замены наших XK и IK handshakes, потому что:

- Мы не можем выполнить KK, у Bob нет статического ключа Alice
- Статические ключи размером 500KB слишком большие
- Мы не хотим дополнительного round-trip

В whitepaper содержится много полезной информации, и мы изучим её в поисках идей и вдохновения. TODO.

## Specification

### Обмен ключами

Обновите разделы и таблицы в документе общих структур [/docs/specs/common-structures/](/docs/specs/common-structures/) следующим образом:

### Подписи

Новые типы открытых ключей:

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Гибридные публичные ключи представляют собой ключи X25519. Публичные ключи KEM — это эфемерные PQ-ключи, отправляемые от Алисы к Бобу. Кодирование и порядок байтов определены в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Ключи MLKEM*_CT на самом деле не являются публичными ключами, это "зашифрованный текст", отправляемый от Боба к Алисе в handshake Noise. Они перечислены здесь для полноты.

### Допустимые комбинации

Новые типы Private Key:

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Гибридные приватные ключи являются ключами X25519. Приватные ключи KEM предназначены только для Alice. Кодировка KEM и порядок байтов определены в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Требуется новая криптография

Новые типы открытых ключей подписи:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Гибридные публичные ключи подписи представляют собой ключ Ed25519, за которым следует PQ ключ, как описано в [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Альтернативы

Новые типы приватных ключей подписи:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Гибридные приватные ключи подписи представляют собой ключ Ed25519, за которым следует PQ ключ, как описано в [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Новые типы подписей:

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Гибридные подписи представляют собой подпись Ed25519, за которой следует PQ подпись, как описано в [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Гибридные подписи проверяются путем проверки обеих подписей, и проверка считается неудачной, если любая из них не прошла проверку. Кодирование и порядок байтов определены в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Новые типы открытых ключей подписи:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Новые типы криптографических открытых ключей:

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Гибридные типы ключей НИКОГДА не включаются в сертификаты ключей; только в leaseSet'ах.

Для destinations с типами подписи Hybrid или PQ используйте NONE (тип 255) для типа шифрования, но криптографический ключ отсутствует, и вся основная секция размером 384 байта предназначена для ключа подписи.

### Общие структуры

Вот длины для новых типов Destination. Тип шифрования для всех — NONE (тип 255), и длина ключа шифрования считается равной 0. Вся 384-байтовая секция используется для первой части открытого ключа подписи. ПРИМЕЧАНИЕ: Это отличается от спецификации для типов подписи ECDSA_SHA512_P521 и RSA, где мы сохраняли 256-байтовый ключ ElGamal в destination, даже если он не использовался.

Без заполнения. Общая длина составляет 7 + общая длина ключа. Длина сертификата ключа составляет 4 + избыточная длина ключа.

Пример 1319-байтового потока байтов назначения destination для MLDSA44:

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Вот длины для новых типов Destination. Тип шифрования для всех — X25519 (тип 4). Весь 352-байтный раздел после открытого ключа X25519 используется для первой части подписывающего открытого ключа. Без дополнения. Общая длина составляет 39 + общая длина ключа. Длина сертификата ключа составляет 4 + избыточная длина ключа.

Пример 1351-байтового потока байтов router identity для MLDSA44:

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### ПриватныйКлюч

Handshakes используют [Noise Protocol](https://noiseprotocol.org/noise.html) шаблоны handshake.

Используется следующее соответствие букв:

- e = одноразовый эфемерный ключ
- s = статический ключ
- p = полезная нагрузка сообщения
- e1 = одноразовый эфемерный PQ ключ, отправляемый от Alice к Bob
- ekem1 = шифротекст KEM, отправляемый от Bob к Alice

Следующие модификации XK и IK для гибридной прямой секретности (hfs) указаны в [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) разделе 5:

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
Шаблон e1 определяется следующим образом, как указано в разделе 4 [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf):

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
Паттерн ekem1 определён следующим образом, как указано в [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) разделе 4:

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
### SigningPublicKey

#### Issues

- Следует ли изменить хеш-функцию рукопожатия? См. [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 не уязвим к постквантовым атакам, но если мы хотим обновить
  нашу хеш-функцию, сейчас самое время, пока мы изменяем другие вещи.
  Текущее предложение IETF SSH [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) заключается в использовании MLKEM768
  с SHA256 и MLKEM1024 с SHA384. Это предложение включает
  обсуждение соображений безопасности.
- Следует ли прекратить отправку данных ratchet с 0-RTT (кроме LS)?
- Следует ли переключить ratchet с IK на XK, если мы не отправляем данные 0-RTT?

#### Overview

Этот раздел применим как к протоколам IK, так и к XK.

Гибридное рукопожатие определено в [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Первое сообщение, от Alice к Bob, содержит e1, ключ инкапсуляции, перед полезной нагрузкой сообщения. Это рассматривается как дополнительный статический ключ; вызовите EncryptAndHash() на нем (как Alice) или DecryptAndHash() (как Bob). Затем обработайте полезную нагрузку сообщения как обычно.

Второе сообщение, от Bob к Alice, содержит ekem1, зашифрованный текст, перед полезной нагрузкой сообщения. Это рассматривается как дополнительный статический ключ; вызовите EncryptAndHash() для него (как Bob) или DecryptAndHash() (как Alice). Затем вычислите kem_shared_key и вызовите MixKey(kem_shared_key). Затем обработайте полезную нагрузку сообщения как обычно.

#### Defined ML-KEM Operations

Мы определяем следующие функции, соответствующие криптографическим строительным блокам, используемым как определено в [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

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

Обратите внимание, что как encap_key, так и ciphertext зашифрованы внутри блоков ChaCha/Poly в сообщениях Noise handshake 1 и 2. Они будут расшифрованы в рамках процесса handshake.

kem_shared_key смешивается с ключом цепочки с помощью MixHash(). Подробности см. ниже.

#### Alice KDF for Message 1

Для XK: После шаблона сообщения 'es' и перед полезной нагрузкой добавить:

ИЛИ

Для IK: После паттерна сообщения 'es' и перед паттерном сообщения 's' добавить:

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
#### Bob KDF for Message 1

Для XK: После шаблона сообщения 'es' и перед полезной нагрузкой добавить:

ИЛИ

Для IK: После паттерна сообщения 'es' и перед паттерном сообщения 's' добавить:

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
#### Bob KDF for Message 2

Для XK: После паттерна сообщения 'ee' и перед полезной нагрузкой добавить:

ИЛИ

Для IK: После шаблона сообщения 'ee' и перед шаблоном сообщения 'se' добавить:

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
#### Alice KDF for Message 2

После шаблона сообщения 'ee' (и перед шаблоном сообщения 'ss' для IK), добавьте:

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
#### KDF for Message 3 (XK only)

неизменный

#### KDF for split()

неизменно

### SigningPrivateKey

Обновить спецификацию ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) следующим образом:

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Изменения: Текущий ratchet содержал статический ключ в первой секции ChaCha и полезную нагрузку во второй секции. С ML-KEM теперь есть три секции. Первая секция содержит зашифрованный PQ публичный ключ. Вторая секция содержит статический ключ. Третья секция содержит полезную нагрузку.

Зашифрованный формат:

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

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Обратите внимание, что полезная нагрузка должна содержать блок DateTime, поэтому минимальный размер полезной нагрузки составляет 7. Минимальные размеры сообщения 1 могут быть рассчитаны соответственно.

#### 1g) New Session Reply format

Изменения: Текущий ratchet имеет пустую полезную нагрузку для первой секции ChaCha и полезную нагрузку во второй секции. С ML-KEM теперь есть три секции. Первая секция содержит зашифрованный PQ ciphertext. Вторая секция имеет пустую полезную нагрузку. Третья секция содержит полезную нагрузку.

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Обратите внимание, что хотя сообщение 2 обычно будет иметь ненулевую полезную нагрузку, спецификация ratchet [/docs/specs/ecies/](/docs/specs/ecies/) этого не требует, поэтому минимальный размер полезной нагрузки составляет 0. Минимальные размеры сообщения 2 могут быть вычислены соответственно.

### Подпись

Обновить спецификацию NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) следующим образом:

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Изменения: Текущий NTCP2 содержит только опции в секции ChaCha. С ML-KEM секция ChaCha также будет содержать зашифрованный PQ публичный ключ.

Необработанное содержимое:

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
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
Размеры:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

#### 2) SessionCreated

Изменения: Текущий NTCP2 содержит только опции в разделе ChaCha. С ML-KEM раздел ChaCha также будет содержать зашифрованный PQ публичный ключ.

Исходное содержимое:

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Незашифрованные данные (тег аутентификации Poly1305 не показан):

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

#### 3) SessionConfirmed

Неизменно

#### Key Derivation Function (KDF) (for data phase)

Неизменно

### Сертификаты ключей

Обновить спецификацию SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) следующим образом:

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

Длинный заголовок составляет 32 байта. Он используется до создания сессии для сообщений Token Request, SessionRequest, SessionCreated и Retry. Он также используется для внесессионных сообщений Peer Test и Hole Punch.

TODO: Мы могли бы внутренне использовать поле версии и использовать 3 для MLKEM512 и 4 для MLKEM768. Делаем ли мы это только для типов 0 и 1 или для всех 6 типов?

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

неизменный

#### SessionRequest (Type 0)

Изменения: Текущий SSU2 содержит только блочные данные в секции ChaCha. С ML-KEM секция ChaCha также будет содержать зашифрованный PQ публичный ключ.

Исходное содержимое:

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
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
Размеры, не включая накладные расходы IP:

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

Минимальный MTU для MLKEM768_X25519: Около 1316 для IPv4 и 1336 для IPv6.

#### SessionCreated (Type 1)

Изменения: Текущий SSU2 содержит только блочные данные в секции ChaCha. С ML-KEM секция ChaCha будет также содержать зашифрованный постквантовый публичный ключ.

Исходное содержимое:

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
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Нешифрованные данные (тег аутентификации Poly1305 не показан):

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
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

Минимальный MTU для MLKEM768_X25519: Около 1316 для IPv4 и 1336 для IPv6.

#### SessionConfirmed (Type 2)

неизменный

#### KDF for data phase

неизменный

#### Проблемы

Блоки Relay, блоки Peer Test и сообщения Peer Test содержат подписи. К сожалению, PQ-подписи больше, чем MTU. В настоящее время отсутствует механизм фрагментации блоков Relay или Peer Test или сообщений на несколько UDP-пакетов. Протокол должен быть расширен для поддержки фрагментации. Это будет сделано в отдельном предложении, которое будет определено позже. До завершения этой работы Relay и Peer Test поддерживаться не будут.

#### Обзор

Мы могли бы внутренне использовать поле версии и использовать 3 для MLKEM512 и 4 для MLKEM768.

Для сообщений 1 и 2, MLKEM768 увеличил бы размер пакетов сверх минимального MTU 1280. Вероятно, просто не поддерживал бы это для такого соединения, если MTU было слишком низким.

Для сообщений 1 и 2, MLKEM1024 увеличил бы размеры пакетов сверх максимального MTU в 1500. Это потребовало бы фрагментации сообщений 1 и 2, и это было бы большим усложнением. Вероятно, делать этого не будем.

Relay и Peer Test: См. выше

### Размеры destination

TODO: Есть ли более эффективный способ определить подписание/верификацию, чтобы избежать копирования подписи?

### Размеры RouterIdent

TODO

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) раздел 8.1 запрещает HashML-DSA в сертификатах X.509 и не назначает OID для HashML-DSA из-за сложностей реализации и сниженной безопасности.

Для PQ-only подписей SU3 файлов используйте OID, определенные в [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) для вариантов без предварительного хеширования для сертификатов. Мы не определяем гибридные подписи SU3 файлов, потому что нам может потребоваться дважды хешировать файлы (хотя HashML-DSA и X2559 используют одну и ту же хеш-функцию SHA512). Также объединение двух ключей и подписей в сертификате X.509 было бы совершенно нестандартным.

Обратите внимание, что мы не разрешаем подписывание файлов SU3 с помощью Ed25519, и хотя мы определили подписывание Ed25519ph, мы никогда не согласовали OID для него и не использовали его.

Обычные типы подписей запрещены для файлов SU3; используйте варианты ph (prehash).

### Шаблоны рукопожатия

Новый максимальный размер Destination будет составлять 2599 (3468 в base 64).

Обновите другие документы, которые содержат рекомендации по размерам Destination, включая:

- SAMv3
- Bittorrent
- Руководство для разработчиков
- Именование / адресная книга / jump-серверы
- Другая документация

## Overhead Analysis

### KDF рукопожатия Noise

Увеличение размера (байты):

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Скорость:

Скорости согласно данным [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Предварительные результаты тестирования в Java:

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Размер:

Типичные размеры ключей, подписей, RIdent, Dest или увеличения размеров (Ed25519 включён для справки) при условии использования типа шифрования X25519 для RI. Добавленный размер для Router Info, LeaseSet, датаграмм с возможностью ответа и каждого из двух streaming пакетов (SYN и SYN ACK). Текущие Destinations и Leasesets содержат повторяющееся заполнение и сжимаются при передаче. Новые типы не содержат заполнения и не будут сжиматься, что приведёт к значительно большему увеличению размера при передаче. См. раздел проектирования выше.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Скорость:

Скорости согласно данным [Cloudflare](https://blog.cloudflare.com/pq-2024/):

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Предварительные результаты тестирования в Java:

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

Категории безопасности NIST обобщены в [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) слайд 10. Предварительные критерии: Наша минимальная категория безопасности NIST должна быть 2 для гибридных протоколов и 3 для протоколов только PQ.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Все это гибридные протоколы. Вероятно, следует отдавать предпочтение MLKEM768; MLKEM512 недостаточно безопасен.

Категории безопасности NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Данное предложение определяет как гибридные, так и только PQ типы подписей. Гибридный MLDSA44 предпочтительнее только PQ MLDSA65. Размеры ключей и подписей для MLDSA65 и MLDSA87, вероятно, слишком велики для нас, по крайней мере на первом этапе.

Категории безопасности NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf):

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Хотя мы определим и реализуем 3 типа криптографии и 9 типов подписей, мы планируем измерять производительность в процессе разработки и дополнительно анализировать влияние увеличенных размеров структур. Мы также продолжим исследования и мониторинг разработок в других проектах и протоколах.

После года или более разработки мы попытаемся определиться с предпочтительным типом или значением по умолчанию для каждого случая использования. Выбор потребует компромиссов между пропускной способностью, процессором и оценочным уровнем безопасности. Не все типы могут быть подходящими или разрешенными для всех случаев использования.

Предварительные предпочтения следующие, могут изменяться:

Шифрование: MLKEM768_X25519

Подписи: MLDSA44_EdDSA_SHA512_Ed25519

Предварительные ограничения следующие, могут быть изменены:

Шифрование: MLKEM1024_X25519 не разрешено для SSU2

Подписи: MLDSA87 и гибридный вариант вероятно слишком большие; MLDSA65 и гибридный вариант могут быть слишком большими

## Implementation Notes

### Library Support

Библиотеки Bouncycastle, BoringSSL и WolfSSL теперь поддерживают MLKEM и MLDSA. Поддержка OpenSSL будет в их релизе 3.5 от 8 апреля 2025 года [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Библиотека Noise от southernstorm.com, адаптированная для Java I2P, содержала предварительную поддержку гибридных handshake, но мы удалили её как неиспользуемую; нам придётся добавить её обратно и обновить в соответствии с [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Мы будем использовать "hedged" или рандомизированный вариант подписи, а не "детерминистический" вариант, как определено в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) раздел 3.4. Это гарантирует, что каждая подпись будет отличаться, даже при подписании одних и тех же данных, и обеспечивает дополнительную защиту от атак по побочным каналам. Хотя [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) указывает, что "hedged" вариант является по умолчанию, это может быть так или не так в различных библиотеках. Разработчики должны убедиться, что для подписи используется "hedged" вариант.

Мы используем обычный процесс подписи (называемый Pure ML-DSA Signature Generation), который кодирует сообщение внутренне как 0x00 || len(ctx) || ctx || message, где ctx - это некоторое необязательное значение размером 0x00..0xFF. Мы не используем никакой необязательный контекст. len(ctx) == 0. Этот процесс определен в [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Алгоритм 2 шаг 10 и Алгоритм 3 шаг 5. Обратите внимание, что некоторые опубликованные тестовые векторы могут требовать установки режима, в котором сообщение не кодируется.

### Reliability

Увеличение размера приведет к значительно большей фрагментации туннелей для хранения NetDB, handshake-сообщений потокового протокола и других сообщений. Проверьте изменения производительности и надежности.

### Structure Sizes

Найдите и проверьте любой код, который ограничивает размер в байтах router infos и leasesets.

### NetDB

Проверить и возможно сократить максимальное количество LS/RI, хранящихся в RAM или на диске, чтобы ограничить рост объема хранилища. Увеличить минимальные требования к пропускной способности для floodfill-узлов?

### Ratchet

#### Определённые операции ML-KEM

Автоматическая классификация/обнаружение нескольких протоколов в одних и тех же туннелях должна быть возможна на основе проверки длины сообщения 1 (New Session Message). Используя MLKEM512_X25519 в качестве примера, длина сообщения 1 на 816 байт больше, чем у текущего ratchet протокола, а минимальный размер сообщения 1 (только с включенной полезной нагрузкой DateTime) составляет 919 байт. Большинство размеров сообщения 1 с текущим ratchet имеют полезную нагрузку менее 816 байт, поэтому их можно классифицировать как не-гибридный ratchet. Большие сообщения, вероятно, являются POST-запросами, которые встречаются редко.

Поэтому рекомендуемая стратегия заключается в следующем:

- Если сообщение 1 меньше 919 байт, это текущий ratchet протокол.
- Если сообщение 1 больше или равно 919 байт, это вероятно MLKEM512_X25519.
  Сначала попробуйте MLKEM512_X25519, и если это не сработает, попробуйте текущий ratchet протокол.

Это должно позволить нам эффективно поддерживать стандартный ratchet и гибридный ratchet на одном и том же destination, точно так же, как мы ранее поддерживали ElGamal и ratchet на одном и том же destination. Поэтому мы можем перейти на гибридный протокол MLKEM гораздо быстрее, чем если бы мы не могли поддерживать двойные протоколы для одного и того же destination, поскольку мы можем добавить поддержку MLKEM к существующим destination.

Требуемые поддерживаемые комбинации:

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Следующие комбинации могут быть сложными и НЕ обязательны к поддержке, но могут поддерживаться в зависимости от реализации:

- Более одного MLKEM
- ElG + один или более MLKEM
- X25519 + один или более MLKEM
- ElG + X25519 + один или более MLKEM

Мы не можем пытаться поддерживать несколько алгоритмов MLKEM (например, MLKEM512_X25519 и MLKEM_768_X25519) на одном и том же получателе. Выберите только один; однако это зависит от того, выберем ли мы предпочтительный вариант MLKEM, чтобы HTTP-клиентские туннели могли его использовать. Зависит от реализации.

Мы МОЖЕМ попытаться поддерживать три алгоритма (например, X25519, MLKEM512_X25519 и MLKEM769_X25519) на одном и том же назначении. Классификация и стратегия повторных попыток могут быть слишком сложными. Конфигурация и пользовательский интерфейс конфигурации могут быть слишком сложными. Зависит от реализации.

Мы, вероятно, НЕ будем пытаться поддерживать алгоритмы ElGamal и hybrid на одном destination. ElGamal устарел, а ElGamal + hybrid только (без X25519) не имеет особого смысла. Кроме того, New Session Messages для ElGamal и Hybrid являются большими, поэтому стратегии классификации часто должны были бы пытаться выполнить оба расшифрования, что было бы неэффективно. Зависит от реализации.

Клиенты могут использовать одни и те же или разные статические ключи X25519 для протоколов X25519 и гибридного на одних и тех же tunnel'ах, в зависимости от реализации.

#### Alice KDF для сообщения 1

Спецификация ECIES позволяет включать Garlic Messages в полезную нагрузку New Session Message, что обеспечивает доставку начального streaming пакета без дополнительных обращений (0-RTT), обычно HTTP GET, вместе с leaseset клиента. Однако полезная нагрузка New Session Message не обладает прямой секретностью. Поскольку данное предложение делает акцент на улучшенной прямой секретности для ratchet, реализации могут или должны отложить включение streaming полезной нагрузки, или полного streaming сообщения, до первого Existing Session Message. Это происходит за счет потери доставки 0-RTT. Стратегии также могут зависеть от типа трафика или типа туннеля, или от GET против POST, например. Зависит от реализации.

#### Bob KDF для сообщения 1

MLKEM, MLDSA или оба на одном destination, существенно увеличат размер New Session Message, как описано выше. Это может значительно снизить надежность доставки New Session Message через туннели, где они должны быть фрагментированы на множественные tunnel message размером 1024 байта. Успех доставки пропорционален экспоненциальному количеству фрагментов. Реализации могут использовать различные стратегии для ограничения размера сообщения за счет 0-RTT доставки. Зависит от реализации.

### Ratchet

Мы можем установить старший бит эфемерного ключа (key[31] & 0x80) в запросе сессии, чтобы указать, что это гибридное соединение. Это позволит нам запускать как стандартный NTCP, так и гибридный NTCP на одном порту. Будет поддерживаться только один гибридный вариант, который будет объявлен в адресе роутера. Например, v=2,3 или v=2,4 или v=2,5.

Если мы этого не сделаем, нам понадобится другой транспортный адрес/порт и новое имя протокола, например "NTCP1PQ1".

Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указываться в адресах router'ов.

TODO

### SSU2

ВОЗМОЖНО потребуется другой транспортный адрес/порт, но надеюсь, что нет, у нас есть заголовок с флагами для сообщения 1. Мы могли бы внутренне использовать поле версии и использовать 3 для MLKEM512 и 4 для MLKEM768. Возможно, просто v=2,3,4 в адресе будет достаточно. Но нам нужны идентификаторы для обоих новых алгоритмов: 3a, 3b?

Проверить и убедиться, что SSU2 может обрабатывать RI, фрагментированный на несколько пакетов (6-8?). i2pd в настоящее время поддерживает максимум только 2 фрагмента?

Примечание: Коды типов предназначены только для внутреннего использования. Router'ы останутся типа 4, а поддержка будет указана в адресах router'ов.

ЗАДАЧИ

## Router Compatibility

### Transport Names

Вероятно, нам не потребуются новые имена транспортов, если мы сможем запускать как стандартный, так и гибридный режимы на одном и том же порту с флагами версий.

Если нам потребуются новые имена транспортов, они будут:

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Обратите внимание, что SSU2 не может поддерживать MLKEM1024, он слишком большой.

### Router Enc. Types

У нас есть несколько альтернатив для рассмотрения:

#### Bob KDF для сообщения 2

Не рекомендуется. Используйте только новые транспорты, перечисленные выше, которые соответствуют типу router. Старые router не могут подключаться, создавать tunnel через них или отправлять netDb сообщения. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию. Может продлить развертывание на год или более по сравнению с альтернативами ниже.

#### Alice KDF для сообщения 2

Рекомендуется. Поскольку PQ не влияет на статический ключ X25519 или протоколы N handshake, мы могли бы оставить router'ы как тип 4 и просто анонсировать новые транспорты. Более старые router'ы всё ещё смогли бы подключаться, строить туннели через них или отправлять сообщения netDb.

#### KDF для сообщения 3 (только XK)

Роутеры типа 4 могли бы анонсировать как NTCP2, так и NTCP2PQ* адреса. Они могли бы использовать один и тот же статический ключ и другие параметры, или нет. Вероятно, для них потребуются разные порты; было бы очень сложно поддерживать как NTCP2, так и NTCP2PQ* протоколы на одном и том же порту, поскольку отсутствует заголовок или фреймирование, которые позволили бы Бобу классифицировать и обрамить входящее сообщение Session Request.

Отдельные порты и адреса будут сложными для Java, но простыми для i2pd.

#### KDF для split()

Маршрутизаторы типа 4 могли бы анонсировать как SSU2, так и SSU2PQ* адреса. С добавленными флагами заголовка, Боб мог бы определить тип входящего транспорта в первом сообщении. Поэтому мы могли бы поддерживать как SSU2, так и SSUPQ* на одном и том же порту.

Они могут быть опубликованы как отдельные адреса (как это делал i2pd в предыдущих переходах) или в том же адресе с параметром, указывающим поддержку PQ (как это делал Java i2p в предыдущих переходах).

Если в том же адресе или на том же порту в разных адресах, они будут использовать один и тот же статический ключ и другие параметры. Если в разных адресах с разными портами, они могут использовать один и тот же статический ключ и другие параметры, а могут и не использовать.

Отдельные порты и адреса будут сложными для Java, но простыми для i2pd.

#### Recommendations

TODO

### NTCP2

#### Идентификаторы Noise

Старые router'ы проверяют RI и поэтому не могут подключаться, строить туннели через них или отправлять netDb сообщения. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию. Будут те же проблемы, что и при развертывании enc. type 5/6/7; может продлить развертывание на год или более по сравнению с альтернативой развертывания type 4 enc. type, перечисленной выше.

Альтернативы отсутствуют.

### LS Enc. Types

#### 1b) Новый формат сессии (с привязкой)

Они могут присутствовать в LS со старыми ключами типа 4 X25519. Старые router'ы будут игнорировать неизвестные ключи.

Destinations могут поддерживать несколько типов ключей, но только путем пробных расшифровок сообщения 1 с каждым ключом. Накладные расходы могут быть снижены за счет ведения счетчиков успешных расшифровок для каждого ключа и первоочередного использования наиболее часто используемого ключа. Java I2P использует эту стратегию для ElGamal+X25519 на одном destination.

### Dest. Sig. Types

#### 1g) Формат ответа New Session Reply

Router'ы проверяют подписи leaseSet и поэтому не могут подключаться или получать leaseSet для назначений типа 12-17. Потребуется несколько циклов релизов для отладки и обеспечения поддержки перед включением по умолчанию.

Альтернативы отсутствуют.

## Спецификация

Наиболее ценными данными является сквозной трафик, зашифрованный с помощью ratchet. Для внешнего наблюдателя между переходами tunnel'а это дополнительно зашифровано дважды — шифрованием tunnel'а и шифрованием транспорта. Для внешнего наблюдателя между OBEP и IBGW это дополнительно зашифровано только один раз — шифрованием транспорта. Для участника OBEP или IBGW единственным шифрованием является ratchet. Однако, поскольку tunnel'ы являются однонаправленными, для перехвата обоих сообщений в ratchet handshake потребуются сговорившиеся роuters, если только tunnel'ы не были построены с OBEP и IBGW на одном router'е.

Наиболее беспокоящая модель угроз PQ в настоящее время - это сохранение трафика сегодня для расшифровки через много-много лет (прямая секретность). Гибридный подход защитил бы от этого.

Модель угроз PQ по взлому ключей аутентификации в разумный период времени (скажем, несколько месяцев) с последующим выдачей себя за другого при аутентификации или расшифровкой почти в реальном времени находится гораздо дальше? И именно тогда мы захотим мигрировать на статические ключи PQC.

Итак, самая ранняя модель угрозы PQ — это OBEP/IBGW, сохраняющие трафик для последующей расшифровки. Мы должны сначала реализовать гибридный ratchet.

Ratchet имеет наивысший приоритет. Транспорты идут следующими. Подписи имеют наименьший приоритет.

Внедрение подписей также будет отложено на год или более по сравнению с внедрением шифрования, поскольку обратная совместимость невозможна. Кроме того, принятие MLDSA в индустрии будет стандартизировано CA/Browser Forum и центрами сертификации. ЦС сначала нужна поддержка аппаратных модулей безопасности (HSM), которая в настоящее время недоступна [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Мы ожидаем, что CA/Browser Forum будет определять решения по конкретному выбору параметров, включая поддержку или требование композитных подписей [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Если мы не сможем поддерживать как старые, так и новые протоколы ratchet в одних и тех же туннелях, миграция будет намного сложнее.

Мы должны иметь возможность просто попробовать один-за-другим, как мы делали с X25519, что должно быть доказано.

## Issues

- Выбор Noise Hash - остаться с SHA256 или обновиться?
  SHA256 должен быть надёжным ещё 20-30 лет, не подвержен угрозе PQ,
  См. [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) и [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Если SHA256 будет взломан, у нас будут более серьёзные проблемы (netdb).
- NTCP2 отдельный порт, отдельный адрес router
- SSU2 relay / peer test
- SSU2 поле версии
- SSU2 версия адреса router
