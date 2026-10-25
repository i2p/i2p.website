---
title: "Протокол клиента I2P (I2CP)"
description: "Как приложения согласовывают сессии, tunnel и leaseSet с I2P router."
slug: "i2cp"
aliases:
  - "/ru/docs/api/i2cp"
  - "/ru/docs/api/i2cp/"
  - "/ru/docs/specs/i2cp-spec"
  - "/ru/docs/specs/i2cp-spec/"
  - "/ru/i2cp_spec"
  - "/ru/i2cp_spec/"
category: "Протоколы"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Обзор

Это спецификация протокола управления I2P (I2CP) — низкоуровневого интерфейса между клиентами и router. Java-клиенты будут использовать клиентский API I2CP, который реализует этот протокол.

Не существует известных реализаций клиентской библиотеки I2CP на языках, отличных от Java. Кроме того, приложениям, ориентированным на сокеты (потоковым), потребуется реализация протокола потоковой передачи, но библиотек для этого на других языках также не существует. Поэтому клиентам на языках, отличных от Java, следует вместо этого использовать протокол более высокого уровня SAM [SAMv3](/docs/api/samv3/), для которого существуют библиотеки на нескольких языках.

Это низкоуровневый протокол, поддерживаемый как внутренне, так и внешне Java I2P router. Протокол сериализуется только в том случае, если клиент и router не находятся в одной JVM; в противном случае Java-объекты I2CP сообщений передаются через внутренний интерфейс JVM. I2CP также поддерживается внешне C++ router i2pd.

Более подробная информация находится на странице обзора I2CP [I2CP](/docs/specs/i2cp/).

## Сессии

Протокол был разработан для обработки нескольких "сессий", каждая с 2-байтовым идентификатором сессии, через одно TCP-соединение, однако множественные сессии не были реализованы до версии 0.9.21. См. [раздел о мультисессиях ниже](#multisession). Не пытайтесь использовать множественные сессии на одном I2CP-соединении с router версии старше 0.9.21.

Также похоже, что есть некоторые возможности для одного клиента взаимодействовать с несколькими router через отдельные соединения. Это также не тестировалось и, вероятно, не является полезным.

Не существует способа поддерживать сессию после отключения или восстановить её на другом I2CP соединении. Когда сокет закрывается, сессия уничтожается.

## Примеры последовательностей сообщений

Примечание: Примеры ниже не показывают байт протокола (0x2a), который должен быть отправлен от клиента к router при первом подключении. Больше информации об инициализации соединения находится на странице обзора I2CP [I2CP](/docs/specs/i2cp/).

### Стандартная установка сессии

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Получить ограничения пропускной способности (простая сессия)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Поиск назначения (простая сессия)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Исходящее сообщение

Существующая сессия, с i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Существующая сессия, с i2cp.messageReliability=none и ненулевым nonce

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Существующая сессия с i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Входящее сообщение

Существующая сессия с i2cp.fastReceive=true (начиная с версии 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Существующая сессия, с i2cp.fastReceive=false (УСТАРЕЛО)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Заметки о многосессионности {#multisession}

Множественные сессии на одном I2CP соединении поддерживаются начиная с версии router 0.9.21. Первая созданная сессия является "основной сессией". Дополнительные сессии являются "подсессиями". Подсессии используются для поддержки нескольких назначений, разделяющих общий набор tunnel. Основное применение заключается в том, что основная сессия использует ключи подписи ECDSA, в то время как подсессия использует ключи подписи DSA для связи со старыми eepsite.

Подсессии используют те же пулы входящих и исходящих туннелей, что и основная сессия. Подсессии должны использовать те же ключи шифрования, что и основная сессия. Это относится как к ключам шифрования leaseSet, так и к (неиспользуемым) ключам шифрования Destination. Подсессии должны использовать разные ключи подписи в destination, поэтому хэш destination отличается от основной сессии. Поскольку подсессии используют те же ключи шифрования и туннели, что и основная сессия, всем очевидно, что Destination-ы работают на одном router-е, поэтому обычные гарантии анонимности против корреляции не применяются.

Подсессии создаются путем отправки сообщения CreateSession и получения ответного сообщения SessionStatus, как обычно. Подсессии должны создаваться после создания основной сессии. Ответ SessionStatus при успехе будет содержать уникальный Session ID, отличный от ID основной сессии. Хотя сообщения CreateSession должны обрабатываться по порядку, нет надежного способа сопоставить сообщение CreateSession с ответом, поэтому клиент не должен иметь несколько одновременно ожидающих ответа сообщений CreateSession. Параметры SessionConfig для подсессии могут не учитываться, если они отличаются от основной сессии. В частности, поскольку подсессии используют тот же tunnel pool, что и основная сессия, параметры tunnel могут игнорироваться.

Router отправит отдельные сообщения RequestVariableLeaseSet для каждого Destination клиенту, и клиент должен ответить сообщением CreateLeaseSet для каждого. Leases для двух Destination не обязательно будут идентичными, даже если они выбраны из одного и того же пула tunnel.

Подсессия может быть уничтожена с помощью сообщения DestroySession как обычно. Это не уничтожит основную сессию и не остановит I2CP соединение. Однако уничтожение основной сессии уничтожит все подсессии и остановит I2CP соединение. Сообщение Disconnect уничтожает все сессии.

Обратите внимание, что большинство, но не все сообщения I2CP содержат Session ID. Для тех, которые не содержат, клиентам может потребоваться дополнительная логика для правильной обработки ответов router. DestLookup и DestReply не содержат Session ID; используйте вместо них более новые HostLookup и HostReply. GetBandwidthLimts и BandwidthLimits не содержат session ID, однако ответ не является специфичным для сессии.

### Примечания к версии {#notes}

Начальный байт версии протокола (0x2a), отправляемый клиентом, не должен изменяться. До версии 0.8.7 информация о версии router не была доступна клиенту, что препятствовало работе новых клиентов со старыми router. Начиная с версии 0.8.7, строки версий протокола обеих сторон обмениваются в сообщениях Get/Set Date Messages. В дальнейшем клиенты могут использовать эту информацию для правильного взаимодействия со старыми router. Клиенты и router не должны отправлять сообщения, которые не поддерживаются другой стороной, поскольку они обычно разрывают сессию при получении неподдерживаемого сообщения.

Обмениваемая информация о версии представляет собой версию "основного" API или версию протокола I2CP, и не обязательно соответствует версии router'а.

Краткое описание версий протокола I2CP выглядит следующим образом. Подробности смотрите ниже.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Общие структуры {#structures}

### Заголовок сообщения I2CP {#struct-I2CPMessageHeader}

#### Описание

Общий заголовок для всех I2CP сообщений, содержащий длину сообщения и тип сообщения.

#### Содержание

1.  4-байтовое [Integer](/docs/specs/common-structures/#integer), указывающее длину
    тела сообщения
2.  1-байтовое [Integer](/docs/specs/common-structures/#integer), указывающее тип
    сообщения.
3.  Тело I2CP сообщения, 0 или более байт

#### Заметки

Фактический лимит длины сообщения составляет около 64 КБ.

### Идентификатор сообщения {#struct-MessageId}

#### Описание

Уникально идентифицирует сообщение, ожидающее на конкретном router в определенный момент времени. Это всегда генерируется router и НЕ является тем же самым nonce, который генерируется клиентом.

#### Содержание

1.  4 байта [Integer](/docs/specs/common-structures/#integer)

#### Заметки

ID сообщений уникальны только в рамках сессии; они не являются глобально уникальными.

### Полезная нагрузка {#struct-Payload}

#### Описание

Эта структура представляет содержимое сообщения, доставляемого от одного Destination к другому.

#### Содержание

1.  4-байтовая длина [Integer](/docs/specs/common-structures/#integer)
2.  Столько байт

#### Примечания

Полезная нагрузка представлена в формате gzip, как указано на странице обзора I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

Фактический лимит длины сообщения составляет около 64 КБ.

### Конфигурация сессии {#struct-SessionConfig}

#### Описание

Определяет параметры конфигурации для конкретной клиентской сессии.

#### Содержание

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) опций
3.  [Date](/docs/specs/common-structures/#date) создания
4.  [Signature](/docs/specs/common-structures/#signature) предыдущих 3 полей,
    подписанная [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Примечания

- Опции указаны на странице обзора I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- [Mapping](/docs/specs/common-structures/#mapping) должен быть отсортирован по ключу, чтобы
  подпись была правильно проверена в router.
- Дата создания должна находиться в пределах +/- 30 секунд от текущего времени
  при обработке router'ом, иначе конфигурация будет отклонена.

#### Автономные подписи

- Если [Destination](/docs/specs/common-structures/#destination) подписан в автономном режиме,
  [Mapping](/docs/specs/common-structures/#mapping) должен содержать три опции
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, и
  i2cp.leaseSetOfflineSignature. 
  [Signature](/docs/specs/common-structures/#signature) затем генерируется временным
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) и
  проверяется с помощью
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey), указанного в
  i2cp.leaseSetTransientPublicKey. См.
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) для подробностей.

### Идентификатор сессии {#struct-SessionId}

#### Описание

Уникально идентифицирует сессию на конкретном router в определённый момент времени.

#### Содержание

1.  2-байтовое [Целое число](/docs/specs/common-structures/#integer)

#### Примечания

Session ID 0xffff используется для обозначения "отсутствия сессии", например, для поиска имён хостов.

## Сообщения

См. также [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Типы сообщений {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Описание

Сообщить клиенту, какие ограничения пропускной способности установлены.

Отправляется от router к клиенту в ответ на [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Содержание

1.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит входящих соединений клиента
    (КБ/с)
2.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит исходящих соединений клиента
    (КБ/с)
3.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит входящих соединений router
    (КБ/с)
4.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит пиковых входящих соединений router
    (КБ/с)
5.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит исходящих соединений router
    (КБ/с)
6.  4 байта [Integer](/docs/specs/common-structures/#integer) Лимит пиковых исходящих соединений router
    (КБ/с)
7.  4 байта [Integer](/docs/specs/common-structures/#integer) Время пиковой нагрузки router
    (секунды)
8.  Девять 4-байтовых [Integer](/docs/specs/common-structures/#integer) (не определено)

#### Примечания

Ограничения клиента могут быть единственными установленными значениями и могут представлять фактические ограничения router, или процент от ограничений router, или быть специфичными для конкретного клиента, в зависимости от реализации. Все значения, помеченные как ограничения router, могут быть равны 0, в зависимости от реализации. По состоянию на релиз 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Описание

Уведомить router о том, что Destination является blinded, с дополнительным паролем для поиска и дополнительным приватным ключом для расшифровки. См. предложения 123 и 149 для подробностей.

Router должен знать, является ли место назначения скрытым. Если оно скрыто и использует секретную или индивидуальную аутентификацию клиента, ему также необходимо иметь эту информацию.

Host Lookup нового формата b32 адреса ("b33") сообщает router'у, что адрес является скрытым, но нет механизма для передачи секретного или приватного ключа router'у в сообщении Host Lookup. Хотя мы могли бы расширить сообщение Host Lookup для добавления этой информации, более чистым решением будет определить новое сообщение.

Это сообщение предоставляет программный способ для клиента сообщить router'у. В противном случае пользователю пришлось бы вручную настраивать каждый пункт назначения.

#### Использование

Прежде чем клиент отправит сообщение к blinded destination (скрытому назначению), он должен либо найти "b33" в сообщении Host Lookup, либо отправить сообщение Blinding Info. Если blinded destination требует секрет или аутентификацию для каждого клиента, клиент должен отправить сообщение Blinding Info.

Router не отправляет ответ на это сообщение. Отправляется от клиента к router.

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  1 байт [Integer](/docs/specs/common-structures/#integer) Флаги

> - Порядок битов: 76543210 > - Бит 0: 0 для всех, 1 для каждого клиента > - Биты 3-1: Схема аутентификации, если бит 0 установлен в 1 для >   каждого клиента, иначе 000 >   - 000: DH аутентификация клиента (или отсутствие аутентификации для каждого клиента) >   - 001: PSK аутентификация клиента > - Бит 4: 1 если требуется секрет, 0 если секрет не требуется > - Биты 7-5: Не используются, устанавливаются в 0 для совместимости с будущими версиями

3.  1 байт [Integer](/docs/specs/common-structures/#integer) Тип конечной точки

> - Тип 0 - это [Hash](/docs/specs/common-structures/#hash) > - Тип 1 - это имя хоста [String](/docs/specs/common-structures/#string) > - Тип 2 - это [Destination](/docs/specs/common-structures/#destination) > - Тип 3 - это Sig Type и >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 байта [Integer](/docs/specs/common-structures/#integer) Тип слепой подписи
5.  4 байта [Integer](/docs/specs/common-structures/#integer) Секунды истечения срока с
    начала эпохи
6.  Конечная точка: Данные как указано, одно из

> - Тип 0: 32-байтный [Hash](/docs/specs/common-structures/#hash) > > - Тип 1: имя хоста [String](/docs/specs/common-structures/#string) > > - Тип 2: бинарный [Destination](/docs/specs/common-structures/#destination) > >  > >  - Тип 3: 2-байтный [Integer](/docs/specs/common-structures/#integer) тип подписи, за которым следует > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (длина как >       подразумевается типом подписи)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Ключ расшифровки Присутствует
    только если бит флага 0 установлен в 1. 32-байтовый приватный ключ ECIES_X25519,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Пароль поиска Присутствует только если
    бит флага 4 установлен в 1.

#### Примечания

- По состоянию на релиз 0.9.43.
- Тип конечной точки Hash вероятно не полезен, если только router не может выполнить обратный поиск в адресной книге для получения Destination.
- Тип конечной точки hostname вероятно не полезен, если только router не может выполнить поиск в адресной книге для получения Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

УСТАРЕЛО. Не может использоваться для LeaseSet2, оффлайн ключей, типов шифрования отличных от ElGamal, множественных типов шифрования или зашифрованных LeaseSet. Используйте CreateLeaseSet2Message со всеми router версии 0.9.39 или выше.

#### Описание

Это сообщение отправляется в ответ на [RequestLeaseSetMessage](#RequestLeaseSetMessage) или [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) и содержит все структуры [Lease](/docs/specs/common-structures/#lease), которые должны быть опубликованы в базе данных сети I2NP.

Отправлено от клиента к router.

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) или 20
    игнорируемых байт
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Примечания

SigningPrivateKey соответствует [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) из LeaseSet, только если тип ключа подписи - DSA. Это предназначено для отзыва LeaseSet, который не реализован и вряд ли когда-либо будет реализован. Если тип ключа подписи не DSA, это поле содержит 20 байт случайных данных. Длина этого поля всегда составляет 20 байт, она никогда не равна длине приватного ключа подписи не-DSA типа.

PrivateKey соответствует [PublicKey](/docs/specs/common-structures/#publickey) из LeaseSet. PrivateKey необходим для расшифровки сообщений, маршрутизируемых через garlic encryption.

Отзыв не реализован. Подключение к нескольким router не реализовано ни в одной клиентской библиотеке.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Описание

Это сообщение отправляется в ответ на [RequestLeaseSetMessage](#RequestLeaseSetMessage) или [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) и содержит все структуры [Lease](/docs/specs/common-structures/#lease), которые должны быть опубликованы в I2NP Network Database.

Отправляется от клиента к router. Начиная с версии 0.9.39. Аутентификация по клиенту для EncryptedLeaseSet поддерживается с версии 0.9.41. MetaLeaseSet пока не поддерживается через I2CP. См. предложение 123 для получения дополнительной информации.

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  Один байт типа leaseSet, который следует далее.

> - Тип 1 это [LeaseSet](/docs/specs/common-structures/#leaseset) (устарел) > - Тип 3 это [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Тип 5 это [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Тип 7 это [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) или
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) или
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) или
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Однобайтовое число приватных ключей, которые следуют далее.
5.  Список [PrivateKey](/docs/specs/common-structures/#privatekey). По одному для каждого публичного
    ключа в lease set, в том же порядке. (Отсутствует для Meta LS2)

> - Тип шифрования (2 байта [Integer](/docs/specs/common-structures/#integer)) > - Длина ключа шифрования (2 байта [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) для шифрования (количество байт >   как указано)

#### Примечания

PrivateKeys соответствуют каждому [PublicKey](/docs/specs/common-structures/#publickey) из LeaseSet. PrivateKeys необходимы для расшифровки сообщений с garlic encryption.

См. предложение 123 для получения дополнительной информации о зашифрованных leaseSet.

Содержимое и формат для MetaLeaseSet являются предварительными и могут быть изменены. Протокол для администрирования нескольких router'ов не определен. Смотрите предложение 123 для получения дополнительной информации.

Приватный ключ подписи, ранее определенный для отзыва и неиспользуемый, отсутствует в LS2.

Предварительная версия с типом сообщения 40 была в 0.9.38, но формат был изменен. Тип 40 заброшен и не поддерживается. Тип 41 не действителен до версии 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Описание

Это сообщение отправляется клиентом для инициации сессии, где сессия определяется как подключение одного Destination к сети, через которое будут доставляться все сообщения для этого Destination и через которое этот Destination будет отправлять все сообщения любому другому Destination.

Отправляется от клиента к маршрутизатору. Маршрутизатор отвечает [SessionStatusMessage](#SessionStatusMessage).

#### Содержание

1.  [Конфигурация сессии](#struct-sessionconfig)

#### Примечания

- Это второе сообщение, отправленное клиентом. Ранее клиент
  отправил [GetDateMessage](#GetDateMessage) и получил
  ответ [SetDateMessage](#SetDateMessage).
- Если дата в конфигурации сессии слишком отличается (более чем на +/- 30
  секунд) от текущего времени router'а, сессия будет
  отклонена.
- Если на router'е уже существует сессия для этого Destination, сессия
  будет отклонена.
- [Mapping](/docs/specs/common-structures/#mapping) в конфигурации сессии должен быть
  отсортирован по ключу, чтобы подпись была корректно проверена в
  router'е.

### DestLookupMessage {#DestLookupMessage}

#### Описание

Отправляется от клиента к router'у. Router отвечает сообщением [DestReplyMessage](#DestReplyMessage).

#### Содержание

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Примечания

Начиная с версии 0.7.

Начиная с версии 0.8.3, поддерживаются множественные одновременные запросы, и запросы поддерживаются как в I2PSimpleSession, так и в стандартных сессиях.

[HostLookupMessage](#HostLookupMessage) является предпочтительным начиная с версии 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Описание

Отправляется от Router к Client в ответ на [DestLookupMessage](#DestLookupMessage).

#### Содержание

1.  [Destination](/docs/specs/common-structures/#destination) при успехе, или
    [Hash](/docs/specs/common-structures/#hash) при неудаче

#### Примечания

Начиная с версии 0.7.

Начиная с версии 0.8.3, запрошенный Hash возвращается при неудачном поиске, чтобы клиент мог иметь несколько активных запросов и сопоставлять ответы с запросами. Чтобы сопоставить ответ Destination с запросом, возьмите Hash от Destination. До версии 0.8.3 ответ был пустым при неудаче.

### DestroySessionMessage {#DestroySessionMessage}

#### Описание

Это сообщение отправляется от клиента для уничтожения сессии.

Отправляется от клиента к router. Router должен ответить сообщением [SessionStatusMessage](#SessionStatusMessage) (Destroyed). Однако см. важные примечания ниже.

#### Содержание

1.  [ID сессии](#struct-sessionid)

#### Заметки

На данном этапе router должен освободить все ресурсы, связанные с сессией.

В API 0.9.66 Java I2P router и клиентские библиотеки существенно отклоняются от данной спецификации. Router никогда не отправляет ответ SessionStatus(Destroyed). Если сессий не осталось, он отправляет [DisconnectMessage](#DisconnectMessage). Если остаются подсессии или основная сессия, он не отвечает.

Клиентская библиотека Java отвечает на сообщение SessionStatus уничтожением всех сессий и переподключением.

Уничтожение отдельных подсессий на соединении с несколькими сессиями может быть не полностью протестировано или не работать в различных реализациях router и клиентов. Будьте осторожны.

Реализации должны обрабатывать уничтожение основной сессии как уничтожение всех подсессий, но позволять уничтожение одной подсессии с сохранением соединения открытым, однако Java I2P сейчас этого не делает. Если поведение Java I2P изменится в последующих выпусках, это будет задокументировано здесь.

### DisconnectMessage {#DisconnectMessage}

#### Описание

Сообщить другой стороне о наличии проблем и том, что текущее соединение будет разорвано. Это завершает все сессии на данном соединении. Сокет будет закрыт в ближайшее время. Отправляется либо от router к клиенту, либо от клиента к router.

#### Содержание

1.  Причина [String](/docs/specs/common-structures/#string)

#### Примечания

Реализовано только в направлении от router к клиенту, по крайней мере в Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Описание

Запросить у router информацию о текущих ограничениях пропускной способности.

Отправляется от клиента к router. Router отвечает сообщением [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Содержание

*Нет*

#### Заметки

По состоянию на выпуск 0.7.2.

Начиная с версии 0.8.3, поддерживается как в I2PSimpleSession, так и в стандартных сессиях.

### GetDateMessage {#GetDateMessage}

#### Описание

Отправляется от клиента к router. Router отвечает сообщением [SetDateMessage](#SetDateMessage).

#### Содержание

1.  Версия I2CP API [String](/docs/specs/common-structures/#string)
2.  Аутентификация [Mapping](/docs/specs/common-structures/#mapping) (опционально, начиная с
    релиза 0.9.11)

#### Заметки

- Обычно это первое сообщение, отправляемое клиентом после отправки
  байта версии протокола.
- Строка версии включена начиная с релиза 0.8.7. Это полезно только
  если клиент и router не находятся в одной JVM. Если она отсутствует,
  клиент имеет версию 0.8.6 или более раннюю.
- Начиная с релиза 0.9.11, может быть включено
  [Mapping](/docs/specs/common-structures/#mapping) аутентификации с ключами
  i2cp.username и i2cp.password. Mapping не обязательно должно быть отсортировано,
  поскольку это сообщение не подписывается. До релиза 0.9.10 включительно
  аутентификация включалась в [Session Config](#struct-sessionconfig)
  Mapping, и аутентификация не применялась для
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) или
  [DestLookupMessage](#DestLookupMessage). Когда включена, аутентификация
  через [GetDateMessage](#GetDateMessage) требуется перед любыми другими
  сообщениями начиная с релиза 0.9.16. Это полезно только вне контекста router.
  Это несовместимое изменение, но затронет только сессии
  вне контекста router с аутентификацией, что должно быть редким случаем.

### HostLookupMessage {#HostLookupMessage}

#### Описание

Отправляется от клиента к router. Router отвечает сообщением [HostReplyMessage](#HostReplyMessage).

Это заменяет [DestLookupMessage](#DestLookupMessage) и добавляет ID запроса, таймаут и поддержку поиска по имени хоста. Поскольку это также поддерживает поиск по Hash, оно может использоваться для всех поисков, если router это поддерживает. Для поиска по имени хоста, router будет запрашивать naming service своего контекста. Это полезно только если клиент находится вне контекста router'а. Внутри контекста router'а клиент должен самостоятельно запрашивать naming service, что гораздо более эффективно.

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  4 байта [Integer](/docs/specs/common-structures/#integer) ID запроса
3.  4 байта [Integer](/docs/specs/common-structures/#integer) тайм-аут (мс)
4.  1 байт [Integer](/docs/specs/common-structures/#integer) тип запроса
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) или имя хоста
    [String](/docs/specs/common-structures/#string) или
    [Destination](/docs/specs/common-structures/#destination)

Типы запросов:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Типы 2-4 запрашивают, чтобы соответствие опций из LeaseSet было возвращено в сообщении HostReply. См. предложение 167.

#### Примечания

- Начиная с релиза 0.9.11. Используйте [DestLookupMessage](#DestLookupMessage) для
  старых router'ов.
- ID сессии и ID запроса будут возвращены в
  [HostReplyMessage](#HostReplyMessage). Используйте 0xFFFF для ID сессии,
  если сессии нет.
- Timeout полезен для Hash поиска. Рекомендуемый минимум 10,000 (10
  сек.). В будущем он также может быть полезен для поиска в удаленной службе имен. Значение может не учитываться для поиска локальных имен хостов,
  который должен быть быстрым.
- Поиск имени хоста в Base 32 поддерживается, но предпочтительно сначала
  преобразовать его в Hash.

### HostReplyMessage {#HostReplyMessage}

#### Описание

Отправляется от Router к Client в ответ на [HostLookupMessage](#HostLookupMessage).

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  4-байтовый [Integer](/docs/specs/common-structures/#integer) идентификатор запроса
3.  1-байтовый [Integer](/docs/specs/common-structures/#integer) код результата

> - 0: Успешно > - 1: Неудача > - 2: Требуется пароль для поиска (начиная с версии 0.9.43) > - 3: Требуется приватный ключ (начиная с версии 0.9.43) > - 4: Требуются пароль для поиска и приватный ключ (начиная с версии 0.9.43) > - 5: Ошибка расшифровки leaseSet (начиная с версии 0.9.43) > - 6: Ошибка поиска leaseSet (начиная с версии 0.9.66) > - 7: Неподдерживаемый тип поиска (начиная с версии 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), присутствует только если код результата равен нулю, за исключением того, что может также возвращаться для типов поиска 2-4. См. ниже.
5.  [Mapping](/docs/specs/common-structures/#mapping), присутствует только если код результата равен нулю, возвращается только для типов поиска 2-4. Начиная с версии 0.9.66. См. ниже.

#### Ответы для типов поиска 2-4

Предложение 167 определяет дополнительные типы поиска, которые возвращают все опции из leaseSet, если они присутствуют. Для типов поиска 2-4 router должен получить leaseSet, даже если ключ поиска находится в адресной книге.

В случае успеха, HostReply будет содержать опции Mapping из leaseset и включит их как элемент 5 после destination. Если в Mapping нет опций, или leaseset был версии 1, он всё равно будет включён как пустой Mapping (два байта: 0 0). Будут включены все опции из leaseset, а не только опции записей служб. Например, могут присутствовать опции для параметров, которые будут определены в будущем. Возвращаемый Mapping может быть отсортирован или нет, в зависимости от реализации.

При неудаче поиска leaseset ответ будет содержать новый код ошибки 6 (Неудача поиска leaseset) и не будет включать сопоставление. Когда возвращается код ошибки 6, поле Destination может присутствовать или отсутствовать. Оно будет присутствовать, если поиск имени хоста в адресной книге был успешным, или если предыдущий поиск был успешным и результат был кэширован, или если Destination присутствовал в сообщении поиска (тип поиска 4).

Если тип поиска не поддерживается, ответ будет содержать новый код ошибки 7 (тип поиска не поддерживается).

#### Примечания

- Начиная с релиза 0.9.11. См. заметки к [HostLookupMessage](#HostLookupMessage).
- ID сессии и ID запроса соответствуют тем, что указаны в [HostLookupMessage](#HostLookupMessage).
- Код результата: 0 для успеха, 1-255 для неудачи. 1 означает общую ошибку. Начиная с версии 0.9.43, были определены дополнительные коды ошибок 2-5 для поддержки расширенных ошибок при "b33" поиске. См. предложения 123 и 149 для дополнительной информации. Начиная с версии 0.9.66, были определены дополнительные коды ошибок 6-7 для поддержки расширенных ошибок при поиске типа 2-4. См. предложение 167 для дополнительной информации.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Описание

Доставить полезную нагрузку сообщения клиенту.

Отправляется от router к клиенту. Если i2cp.fastReceive=true, что не является значением по умолчанию, клиент отвечает [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  [ID сообщения](#struct-messageid)
3.  [Полезная нагрузка](#struct-payload)

#### Заметки

### MessageStatusMessage {#MessageStatusMessage}

#### Описание

Уведомить клиента о статусе доставки входящего или исходящего сообщения. Отправляется от Router к Client. Если это сообщение указывает, что входящее сообщение доступно, клиент отвечает [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Для исходящего сообщения это ответ на [SendMessageMessage](#SendMessageMessage) или [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid), сгенерированный router'ом
3.  1 байт [Integer](/docs/specs/common-structures/#integer) статус
4.  4 байта [Integer](/docs/specs/common-structures/#integer) размер
5.  4 байта [Integer](/docs/specs/common-structures/#integer) nonce, ранее сгенерированный
    клиентом

#### Примечания

До версии 0.9.4 известными значениями статуса являются: 0 для сообщения доступно, 1 для принято, 2 для успешной доставки best effort, 3 для неудачной доставки best effort, 4 для успешной гарантированной доставки, 5 для неудачной гарантированной доставки. Целое число size указывает размер доступного сообщения и актуально только для статуса = 0. Несмотря на то, что гарантированная доставка не реализована (единственным сервисом является best effort), текущая реализация router использует коды статуса гарантированной доставки, а не коды best effort.

Начиная с версии router 0.9.5, определены дополнительные коды состояния, однако они не обязательно реализованы. См. [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) для получения подробной информации. Для исходящих сообщений коды 1, 2, 4 и 6 указывают на успех; все остальные являются ошибками. Возвращаемые коды ошибок могут различаться и зависят от реализации.

Все коды состояния:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Когда status = 1 (принято), nonce соответствует nonce в [SendMessageMessage](#SendMessageMessage), и включенный Message ID будет использоваться для последующего уведомления об успехе или неудаче. В противном случае nonce может игнорироваться.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

УСТАРЕЛО. Не поддерживается i2pd.

#### Описание

Запросить у router доставку сообщения, о котором он был ранее уведомлен. Отправляется от клиента к router. Router отвечает сообщением [MessagePayloadMessage](#MessagePayloadMessage).

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  [ID сообщения](#struct-messageid)

#### Примечания

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) отправляется как ответ на [MessageStatusMessage](#MessageStatusMessage), сообщающее о том, что новое сообщение доступно для получения. Если идентификатор сообщения, указанный в [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage), недействителен или неверен, router может просто не ответить или отправить обратно [DisconnectMessage](#DisconnectMessage).

Это не используется в режиме "быстрого получения", который является настройкой по умолчанию начиная с версии 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

УСТАРЕЛО. Не поддерживается i2pd.

#### Описание

Сообщить router'у, что доставка сообщения была успешно завершена и что router может удалить сообщение.

Отправлено с клиента на router.

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  [ID сообщения](#struct-messageid)

#### Заметки

Сообщение [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) отправляется после того, как [MessagePayloadMessage](#MessagePayloadMessage) полностью доставляет полезную нагрузку сообщения.

Это не используется в режиме "быстрого приёма", который является режимом по умолчанию начиная с версии 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Описание

Отправляется от клиента к router для обновления конфигурации сессии. Router отвечает сообщением [SessionStatusMessage](#SessionStatusMessage).

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  [Конфигурация сессии](#struct-sessionconfig)

#### Примечания

- По состоянию на релиз 0.7.1.
- Если дата в Session Config слишком сильно отличается (более чем на +/- 30
  секунд) от текущего времени router'а, сессия будет
  отклонена.
- [Mapping](/docs/specs/common-structures/#mapping) в Session Config должен быть
  отсортирован по ключу, чтобы подпись была правильно валидирована в
  router'е.
- Некоторые параметры конфигурации могут быть установлены только в
  [CreateSessionMessage](#CreateSessionMessage), и изменения здесь не будут
  распознаны router'ом. Изменения параметров tunnel inbound.\*
  и outbound.\* всегда распознаются.
- В общем случае router должен объединить обновленную конфигурацию с
  текущей конфигурацией, поэтому обновленная конфигурация должна содержать только новые или
  измененные параметры. Однако из-за объединения параметры нельзя
  удалить таким образом; они должны быть явно установлены в желаемое
  значение по умолчанию.

### ReportAbuseMessage {#ReportAbuseMessage}

УСТАРЕЛО, НЕ ИСПОЛЬЗУЕТСЯ, НЕ ПОДДЕРЖИВАЕТСЯ

#### Описание

Сообщить другой стороне (клиенту или router), что она находится под атакой, возможно со ссылкой на конкретный MessageId. Если router находится под атакой, клиент может принять решение о миграции на другой router, а если клиент находится под атакой, router может перестроить свои маршруты или внести в черный список некоторых из узлов, которые отправляли ему сообщения с атакой.

Отправляется либо от router к клиенту, либо от клиента к router.

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  1 байт [Integer](/docs/specs/common-structures/#integer) степень нарушения (0 — минимальное нарушение, 255 — крайне серьёзное нарушение)
3.  Причина [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Примечания

Не используется. Не полностью реализовано. И router, и клиент могут генерировать [ReportAbuseMessage](#ReportAbuseMessage), но ни у одного из них нет обработчика для этого сообщения при получении.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

УСТАРЕЛО. Не поддерживается i2pd. Не отправляется Java I2P клиентам версии 0.9.7 или выше (2013-07). Используйте RequestVariableLeaseSetMessage.

#### Описание

Запрос клиенту на авторизацию включения определенного набора входящих tunnel. Отправляется с Router на клиента. Клиент отвечает сообщением [CreateLeaseSetMessage](#CreateLeaseSetMessage).

Первое из этих сообщений, отправленных в сессии, является сигналом клиенту о том, что tunnel построены и готовы к передаче трафика. Router не должен отправлять первое из этих сообщений до тех пор, пока не будут построены как минимум один входящий И один исходящий tunnel. Клиенты должны прервать сессию по таймауту и уничтожить её, если первое из этих сообщений не получено в течение некоторого времени (рекомендуется: 5 минут или более).

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  1 байт [Integer](/docs/specs/common-structures/#integer) количество tunnel'ов
3.  Столько же пар:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  Конец [Date](/docs/specs/common-structures/#date)

#### Примечания

Это запрашивает [LeaseSet](/docs/specs/common-structures/#leaseset) со всеми записями [Lease](/docs/specs/common-structures/#lease), для которых установлено одинаковое время истечения. Для клиентских версий 0.9.7 или выше используется [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage).

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Описание

Запрос на то, чтобы клиент авторизовал включение определенного набора входящих tunnel'ов.

Отправляется от router к клиенту. Клиент отвечает [CreateLeaseSetMessage](#CreateLeaseSetMessage) или [CreateLeaseSet2Message](#CreateLeaseSet2Message).

Первое из этих сообщений, отправляемых в сессии, является сигналом клиенту о том, что tunnel построены и готовы для трафика. Router не должен отправлять первое из этих сообщений до тех пор, пока не будет построен хотя бы один входящий И один исходящий tunnel. Клиенты должны завершать по таймауту и уничтожать сессию, если первое из этих сообщений не получено через некоторое время (рекомендуется: 5 минут или более).

#### Содержание

1.  [ID сессии](#struct-sessionid)
2.  1 байт [Integer](/docs/specs/common-structures/#integer) количество tunnel'ов
3.  Соответствующее количество записей [Lease](/docs/specs/common-structures/#lease)

#### Примечания

Это запрашивает [LeaseSet](/docs/specs/common-structures/#leaseset) с индивидуальным временем истечения для каждого [Lease](/docs/specs/common-structures/#lease).

Начиная с версии 0.9.7. Для клиентов более ранних версий используйте [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Описание

Так клиент отправляет сообщение (полезную нагрузку) в [Destination](/docs/specs/common-structures/#destination). Router будет использовать срок истечения по умолчанию.

Отправляется от клиента к router. Router отвечает [MessageStatusMessage](#MessageStatusMessage).

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4-байтовый [Integer](/docs/specs/common-structures/#integer) nonce

#### Заметки

Как только [SendMessageMessage](#SendMessageMessage) поступает полностью целым, router должен вернуть [MessageStatusMessage](#MessageStatusMessage), указывающее, что сообщение принято к доставке. Это сообщение будет содержать тот же nonce, который был отправлен здесь. Позже, основываясь на гарантиях доставки конфигурации сессии, router может дополнительно отправить обратно еще один [MessageStatusMessage](#MessageStatusMessage), обновляющий статус.

Начиная с версии 0.8.1, router не отправляет ни одно [MessageStatusMessage](#MessageStatusMessage), если i2cp.messageReliability=none.

До выпуска версии 0.9.4 значение nonce равное 0 не допускалось. Начиная с версии 0.9.4, значение nonce равное 0 разрешено и указывает router'у, что он не должен отправлять [MessageStatusMessage](#MessageStatusMessage), то есть это работает как если бы для данного сообщения было установлено i2cp.messageReliability=none.

До выпуска 0.9.14 сессия с i2cp.messageReliability=none не могла быть переопределена для отдельного сообщения. Начиная с выпуска 0.9.14, в сессии с i2cp.messageReliability=none клиент может запросить доставку [MessageStatusMessage](#MessageStatusMessage) с информацией об успехе или неудаче доставки, установив nonce в ненулевое значение. Router не отправит [MessageStatusMessage](#MessageStatusMessage) "принято", но позже отправит клиенту [MessageStatusMessage](#MessageStatusMessage) с тем же nonce и значением успеха или неудачи.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Описание

Отправляется от клиента к router. То же самое, что [SendMessageMessage](#SendMessageMessage), за исключением того, что включает время истечения и опции.

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4-байтовый [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 байта флагов (опции)
6.  [Date](/docs/specs/common-structures/#date) истечения срока, сокращенная с 8 байт до 6
    байт

#### Примечания

По состоянию на версию 0.7.1.

В режиме "best effort", как только SendMessageExpiresMessage поступает полностью неповрежденным, router должен вернуть MessageStatusMessage, указывающее, что сообщение было принято к доставке. Это сообщение будет содержать тот же nonce, который был отправлен здесь. Позже, основываясь на гарантиях доставки конфигурации сессии, router может дополнительно отправить обратно другое MessageStatusMessage с обновлением статуса.

Начиная с версии 0.8.1, router не отправляет сообщения Message Status Message, если i2cp.messageReliability=none.

До версии 0.9.4 значение nonce равное 0 не допускалось. Начиная с версии 0.9.4, значение nonce равное 0 разрешено и указывает router'у, что он не должен отправлять никаких Message Status Message, то есть это действует так, как если бы для данного сообщения было установлено i2cp.messageReliability=none.

До версии 0.9.14 сессия с i2cp.messageReliability=none не могла быть переопределена для отдельного сообщения. Начиная с версии 0.9.14, в сессии с i2cp.messageReliability=none клиент может запросить доставку Message Status Message с результатом успешной или неудачной доставки, установив nonce в ненулевое значение. Router не отправит "accepted" Message Status Message, но позже отправит клиенту Message Status Message с тем же nonce и значением успеха или неудачи.

#### Поле флагов

Начиная с релиза 0.8.4, верхние два байта поля Date переопределены для содержания флагов. Флаги должны по умолчанию иметь значение все нули для обратной совместимости. Date не будет затрагивать поле флагов до 10889 года. Флаги могут использоваться приложением для предоставления подсказок router'у о том, должен ли LeaseSet и/или ElGamal/AES Session Tags доставляться вместе с сообщением. Настройки значительно повлияют на количество протокольных накладных расходов и надежность доставки сообщений. Отдельные биты флагов определены следующим образом, начиная с релиза 0.9.2. Определения могут изменяться. Используйте класс SendMessageOptions для конструирования флагов.

Порядок битов: 15...0

Биты 15-11

:   Не используется, должно быть ноль

Биты 10-9

:   Переопределение надежности сообщений (не реализовано, будет удалено).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Бит 8

:   Если 1, не включать leaseSet в garlic с этим сообщением. Если

    0, the router may bundle a lease set at its discretion.

Биты 7-4

:   Нижний порог тегов. Если доступно меньше этого количества тегов,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Биты 3-0

:   Количество тегов для отправки при необходимости. Это рекомендательное значение и не

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Описание

Уведомить клиента о статусе его сессии.

Отправляется от router к клиенту в ответ на [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage) или [DestroySessionMessage](#DestroySessionMessage). Во всех случаях, включая ответ на [CreateSessionMessage](#CreateSessionMessage), router должен отвечать немедленно (не ждать построения tunnel).

#### Содержание

1.  [Session ID](#struct-sessionid)
2.  1 байт [Integer](/docs/specs/common-structures/#integer) статус

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Примечания

Значения статуса определены выше. Если статус Created, то Session ID является идентификатором, который будет использоваться для остальной части сессии.

### SetDateMessage {#SetDateMessage}

#### Описание

Текущие дата и время. Отправляется от Router к клиенту как часть начального рукопожатия. Начиная с релиза 0.9.20, также может отправляться в любое время после рукопожатия для уведомления клиента о сдвиге часов.

#### Содержание

1.  [Date](/docs/specs/common-structures/#date)
2.  Версия I2CP API [String](/docs/specs/common-structures/#string)

#### Заметки

Это обычно первое сообщение, отправляемое router'ом. Строка версии включается начиная с релиза 0.8.7. Это полезно только в том случае, если клиент и router не находятся в одной JVM. Если она отсутствует, то router имеет версию 0.8.6 или более раннюю.

Дополнительные сообщения SetDate не будут отправляться клиентам в той же JVM.

## Ссылки

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Обзор I2CP](/docs/specs/i2cp/)
- [Javadocs I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Javadocs MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
