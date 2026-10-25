---
title: "Обзор I2CP"
description: "Обзор протокола клиентов I2P (I2CP) — управление сессиями, параметры, формат полезной нагрузки и мультиплексирование."
slug: "i2cp-overview"
aliases:
  - "/ru/docs/protocol/i2cp"
  - "/ru/docs/protocol/i2cp/"
category: "Протоколы"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Обзор

Протокол клиент-серверного взаимодействия I2P (I2CP) обеспечивает чёткое разделение ответственности между маршрутизатором и любым клиентом, желающим взаимодействовать через сеть. Он позволяет осуществлять безопасную и асинхронную передачу сообщений посредством отправки и получения сообщений через один TCP-сокет. С помощью I2CP клиентское приложение сообщает маршрутизатору, кто оно («назначение»), какие компромиссы между анонимностью, надёжностью и задержкой следует применить, а также куда направлять сообщения. В свою очередь, маршрутизатор использует I2CP, чтобы уведомить клиент о прибытии сообщений и запросить разрешение на использование некоторых туннелей.

Сам протокол реализован на Java для предоставления клиентского SDK. Этот SDK представлен в пакете i2p.jar, который реализует клиентскую часть I2CP. Клиентам никогда не нужно обращаться к пакету router.jar, в котором содержится сам маршрутизатор и сторонняя часть I2CP. Клиент на другом языке, кроме Java, также должен реализовать [библиотеку потоковой передачи](/docs/api/streaming/) для соединений по типу TCP.

Приложения могут использовать базовый I2CP вместе с библиотеками [потоковой передачи](/docs/api/streaming/) и [датаграмм](/docs/specs/datagrams/), применяя протокол [Простого Анонимного Обмена Сообщениями (SAM)](/docs/api/samv3/), который не требует от клиентов работы с криптографией. Кроме того, клиенты могут получать доступ к сети через один из нескольких прокси-протоколов — HTTP, CONNECT и SOCKS 4/4a/5. Альтернативно, клиенты на Java могут обращаться к этим библиотекам через ministreaming.jar и streaming.jar. Таким образом, существует несколько вариантов для приложений как на Java, так и на других языках.

Шифрование с конца в конец на стороне клиента (шифрование данных через соединение I2CP) было отключено в релизе I2P 0.6, при этом осталось шифрование с конца в конец по схеме ElGamal/AES, реализованное в маршрутизаторе. Единственная криптография, которую клиентским библиотекам всё ещё необходимо реализовывать — это подпись по алгоритму DSA с открытым/закрытым ключом для [LeaseSets](/docs/specs/i2cp/#msg_CreateLeaseSet) и [Session Configurations](/docs/specs/i2cp/#struct_SessionConfig), а также управление этими ключами.

В стандартной установке I2P порт 7654 используется внешними Java-клиентами для связи с локальным маршрутизатором через I2CP. По умолчанию маршрутизатор привязывается к адресу 127.0.0.1. Чтобы привязаться к 0.0.0.0, установите расширенный параметр конфигурации маршрутизатора `i2cp.tcp.bindAllInterfaces=true` и перезапустите его. Клиенты, работающие в той же JVM, что и маршрутизатор, передают сообщения напрямую через внутренний интерфейс JVM.

Некоторые реализации маршрутизатора и клиента также могут поддерживать внешние подключения по SSL, как настроено параметром `i2cp.SSL=true`. Хотя SSL не является значением по умолчанию, его настоятельно рекомендуется использовать для любого трафика, который может быть доступен в открытом Интернете. Учётные данные авторизации (имя пользователя и пароль, если таковые имеются), [Закрытый ключ](/docs/specs/common-structures/#type_PrivateKey) и [Закрытый ключ для подписи](/docs/specs/common-structures/#type_SigningPrivateKey) для [Назначения](/docs/specs/common-structures/#struct_Destination) передаются открыто, если SSL не включён. Некоторые реализации маршрутизатора и клиента также могут поддерживать внешние подключения через доменные сокеты.

## Спецификация протокола I2CP

Полная спецификация протокола доступна на [странице спецификации I2CP](/docs/specs/i2cp/).

## Инициализация I2CP {#initialization}

Когда клиент подключается к маршрутизатору, он сначала отправляет один байт версии протокола (0x2A). Затем он отправляет [Сообщение GetDate](/docs/specs/i2cp/#msg_GetDate) и ожидает ответа [Сообщения SetDate](/docs/specs/i2cp/#msg_SetDate). Далее клиент отправляет [Сообщение CreateSession](/docs/specs/i2cp/#msg_CreateSession), содержащее конфигурацию сессии. После этого он ожидает получения от маршрутизатора [Сообщения RequestLeaseSet](/docs/specs/i2cp/#msg_RequestLeaseSet), которое указывает на то, что входящие туннели построены, и отвечает сообщением CreateLeaseSetMessage, содержащим подписанный LeaseSet. Теперь клиент может инициировать соединения или принимать подключения от других I2P-адресов.

## Параметры I2CP {#options}

### Опции на стороне роутера

Следующие параметры традиционно передаются маршрутизатору через [SessionConfig](/docs/specs/i2cp/#struct_SessionConfig), содержащийся в сообщении [CreateSession Message](/docs/specs/i2cp/#msg_CreateSession) или в сообщении [ReconfigureSession Message](/docs/specs/i2cp/#msg_ReconfigureSession).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Router-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">clientMessageTimeout</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8*1000 - 120*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">60*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The timeout (ms) for all sent messages. Unused. See the protocol specification for per-message settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.lowTagThreshold</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum number of ElGamal/AES Session Tags before we send more. Recommended: approximately tagsToSend * 2/3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.inboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset size. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.outboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to the far-end in the options block. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.tagsToSend</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of ElGamal/AES Session Tags to send at a time. For clients with relatively low bandwidth per-client-pair (IRC, some UDP apps), this may be set lower.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">explicitPeers</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">null</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Comma-separated list of Base 64 Hashes of peers to build tunnels through; for debugging only</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.dontPublishLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Should generally be set to true for clients and false for servers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4,0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineExpiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The expiration of the offline signature, 4 bytes, seconds since the epoch. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineSignature</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the offline signature. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A base 64 X25519 private key for the router to use to decrypt the encrypted LS2 locally, only if per-client authentication is enabled. Optionally preceded by the key type and ':'. Only "ECIES_X25519:" is supported, which is the default. See proposal 123. Do not confuse with i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetTransientPublicKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">[type:]b64 The base 64 of the transient private key, prefixed by an optional sig type number or name, default DSA_SHA1. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; the streaming lib default is None as of 0.8.1, the client side default is None as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.password</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">For authorization, if required by the router. If the client is running in the same JVM as a router, this option is not required. Warning - username and password are sent in the clear to the router, unless using SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.username</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If incoming zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If outgoing zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels in. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels out. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally used in routerconsole, which will use the first few characters of the Base64 hash of the destination by default.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally ignored unless inbound.nickname is unset.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.priority</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority adjustment for outbound messages. Higher is higher priority.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels in. Limit was increased from 6 to 16 in release 0.9; however, numbers higher than 6 are incompatible with older releases.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">Used for consistent peer ordering across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "inbound." are stored in the "unknown options" properties of the inbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "outbound." are stored in the "unknown options" properties of the outbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">shouldBundleReplyInfo</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Set to false to disable ever bundling a reply LeaseSet. For clients that do not publish their LeaseSet, this option must be true for any reply to be possible. "true" is also recommended for multihomed servers with long connection times.

Setting to "false" may save significant outbound bandwidth, especially if the client is configured with a large number of inbound tunnels (Leases). If replies are still required, this may shift the bandwidth burden to the far-end client and the floodfill. There are several cases where "false" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a "server", all connections are inbound so the connecting far-end destination obviously has the leaseset already. Connections are either short, or it is acceptable for latency on a long-lived connection to temporarily increase while the other end re-fetches the LeaseSet after expiration. HTTP servers may fit these requirements.</td>
</tr>
</table>
Примечание: высокие значения количества, длины или дисперсии могут вызвать серьёзные проблемы с производительностью или надёжностью.

Примечание: Начиная с версии 0.7.7, имена и значения параметров должны использовать кодировку UTF-8. Это в первую очередь полезно для псевдонимов. В более ранних версиях параметры с многобайтовыми символами повреждались. Поскольку параметры кодируются в [Mapping](/docs/specs/common-structures/#type_Mapping), длина имён и значений параметров ограничена максимум 255 байтами (не символами).

### Опции на стороне клиента

Следующие параметры интерпретируются на стороне клиента и будут обработаны, если переданы в I2PSession через вызов I2PClient.createSession(). Библиотека потоковой передачи также должна передавать эти параметры через I2CP. Другие реализации могут иметь другие значения по умолчанию.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Client-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1800000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 30 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Close I2P session when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.encryptLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypt the lease</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.gzip</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip outbound data</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetBlindedType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See prop. 123</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The sig type of the blinded key for encrypted LS2. Default depends on the destination sig type. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.dh.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64pubkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the public key to use for DH per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.psk.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64privkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the private key to use for PSK per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">For encrypted leasesets. Base 64 SessionKey (44 characters)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOption.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">srvKey=srvValue</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A service record to be placed in the LeaseSet2 options. Example: "_smtp._tcp=1 86400 0 0 25 ...b32.i2p". nnn starts with 0. See proposal 167.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private keys for encryption. Optionally preceded by the encryption type name or number and ':'. For LS1, only one key is supported, and only "0:" or "ELGAMAL_2048:" is supported, which is the default. As of 0.9.39, for LS2, multiple keys may be comma-separated, and each key must be a different encryption type. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts. See proposals 123, 144, and 145. See also i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSigningPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private key for signatures. Optionally preceded by the key type and ':'. DSA_SHA1 is the default. Key type must match the signature type in the destination. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; None is the default as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 20 minutes, minimum 5 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reduce tunnel quantity when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel quantity when reduced (applies to both inbound and outbound)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.SSL</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Connect to the router using SSL. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.host</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">127.0.0.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router hostname. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.port</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7654</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router I2CP port. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
</table>
Примечание: Все аргументы, включая числа, являются строками. Значения true/false — строки без учёта регистра. Любое значение, отличное от "true" (без учёта регистра), интерпретируется как false. Названия всех параметров чувствительны к регистру.

## Формат данных полезной нагрузки I2CP и мультиплексирование {#format}

Сообщения с сквозным шифрованием, обрабатываемые I2CP (то есть данные, отправленные клиентом в [SendMessageMessage](/docs/specs/i2cp/#msg_SendMessage) и полученные клиентом в [MessagePayloadMessage](/docs/specs/i2cp/#msg_MessagePayload)), сжимаются с использованием стандартного 10-байтового заголовка gzip, начинающегося с 0x1F 0x8B 0x08, как указано в [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). Начиная с версии 0.7.1, I2P использует игнорируемые части заголовка gzip для включения информации о протоколе, порте отправителя и порте получателя, что обеспечивает поддержку потоковой передачи и датаграмм на одном и том же адресате, а также надёжную работу запросов/ответов с использованием датаграмм при наличии нескольких каналов.

Функцию gzip нельзя полностью отключить, однако установка параметра `i2cp.gzip=false` приводит к тому, что уровень сжатия gzip устанавливается в 0, что может немного сэкономить процессорное время. Реализации могут выбирать различные уровни сжатия gzip для каждого сокета или сообщения в зависимости от оценки степени сжимаемости содержимого. Из-за сжимаемости дополнительных данных назначения, реализованной в API 0.9.57 (предложение 161), рекомендуется использовать сжатие для SYN-пакетов потоковой передачи в обоих направлениях, а также для ответных датаграмм, даже если полезная нагрузка не поддаётся сжатию. Реализациям может быть полезно написать упрощённую функцию gzip/gunzip для уровня сжатия 0, что обеспечит значительный выигрыш в эффективности по сравнению с использованием полноценной библиотеки gzip в данном случае.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Content</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip header 0x1F 0x8B 0x08</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip flags</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4-5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Source port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6-7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Destination port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip xflags (set to 2 to be indistinguishable from the Java implementation)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip OS)</td>
</tr>
</table>
Примечание: номера протоколов I2P 224–254 зарезервированы для экспериментальных протоколов. Номер протокола I2P 255 зарезервирован для будущего расширения.

Целостность данных проверяется с помощью стандартной CRC-32 gzip, как указано в [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt).

## Важные различия от стандартного IP {#ip-differences}

Порты I2CP предназначены для сокетов и датаграмм I2P. Они не связаны с вашими локальными сокетами или портами. Поскольку I2P не поддерживал порты и номера протоколов до выпуска 0.7.1, порты и номера протоколов в нём несколько отличаются от стандартных IP-решений, во имя обратной совместимости:

- Порт 0 является допустимым и имеет особое значение.
- Порты 1–1023 не являются специальными или привилегированными.
- Серверы по умолчанию прослушивают порт 0, что означает «все порты».
- Клиенты по умолчанию отправляют данные на порт 0, что означает «любой порт».
- Клиенты по умолчанию отправляют данные с порта 0, что означает «неуказанный».
- На серверах может быть сервис, прослушивающий порт 0, и другие сервисы, прослушивающие более высокие порты. В таком случае сервис на порту 0 будет использоваться по умолчанию и к нему будет установлено соединение, если входящий порт сокета или датаграммы не соответствует другому сервису.
- На большинстве I2P-адресов работает только одна служба, поэтому вы можете использовать значения по умолчанию и игнорировать настройку портов I2CP.
- Протокол 0 является допустимым и означает «любой протокол». Однако это не рекомендуется и, вероятно, работать не будет. Для потоковой передачи необходимо, чтобы номер протокола был установлен в 6.
- Потоковые сокеты отслеживаются по внутреннему идентификатору соединения. Следовательно, нет необходимости в уникальности 5-кортежа dest:port:dest:port:protocol. Например, может существовать несколько сокетов с одинаковыми портами между двумя адресами. Клиентам не нужно выбирать «свободный порт» для исходящего соединения.

## Будущая работа {#future}

- Текущий механизм авторизации можно изменить для использования хешированных паролей.
- Закрытый ключ подписи включается в сообщение Create Lease Set, хотя это не требуется. Отзыв не реализован. Следует заменить его случайными данными или удалить.
- Некоторые улучшения могут использовать сообщения, ранее определённые, но не реализованные.
