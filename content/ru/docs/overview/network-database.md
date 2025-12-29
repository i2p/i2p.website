---
title: "Сетевая база данных (netDb)"
description: "Понимание распределённой сетевой базы данных I2P (netDb) - специализированной DHT для контактной информации о router и поиска назначений"
slug: "network-database"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Обзор

**netDb** — специализированная распределённая база данных, содержащая всего два типа данных: - **RouterInfos** – контактная информация router - **LeaseSets** – контактная информация назначения

Все данные криптографически подписаны и могут быть проверены. Каждая запись содержит информацию о liveness (о «живости»/доступности), позволяющую отбрасывать устаревшие записи и заменять неактуальные, что обеспечивает защиту от некоторых классов атак.

Распределение использует механизм **floodfill**, при котором подмножество routers поддерживает распределённую базу данных.

---

## 2. Информация о router

Когда routers нужно связаться с другими routers, они обмениваются пакетами **RouterInfo**, содержащими:

- **Идентичность router** – ключ шифрования, ключ подписи, сертификат
- **Контактные адреса** – как связаться с router
- **Метка времени публикации** – когда эта информация была опубликована
- **Произвольные текстовые опции** – флаги возможностей и настройки
- **Криптографическая подпись** – подтверждает подлинность

### 2.1 Флаги возможностей

Routers сообщают о своих возможностях с помощью буквенных кодов в своих RouterInfo:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>f</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill participation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>R</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>U</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unreachable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>D</strong>, <strong>E</strong>, <strong>G</strong>, <strong>H</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Various capability indicators</td>
    </tr>
  </tbody>
</table>
### 2.2 Классификации пропускной способности

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bandwidth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>K</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Under 12 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>L</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12–48 KBps (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>M</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48–64 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>N</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64–128 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>O</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128–256 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256–2000 KBps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>X</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Over 2000 KBps</td>
    </tr>
  </tbody>
</table>
### 2.3 Значения идентификатора сети

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Current Network (default)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for Future Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3–15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forks and Test Networks</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16–254</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved</td>
    </tr>
  </tbody>
</table>
### 2.4 Статистика RouterInfo

Routers публикуют необязательную статистику состояния для анализа сети: - Показатели успешности/отклонений/тайм-аутов при построении Exploratory tunnel - Среднее за 1 час число участвующих tunnel

Статистические данные соответствуют формату `stat_(statname).(statperiod)` со значениями, разделёнными точкой с запятой.

**Пример статистики:**

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Floodfill routers также могут публиковать: `netdb.knownLeaseSets` и `netdb.knownRouters`

### 2.5 Параметры семейства

Начиная с релиза 0.9.24, routers могут объявлять принадлежность к семье (один и тот же оператор):

- **family**: Имя семейства
- **family.key**: Код типа подписи, конкатенированный с открытым ключом подписи, закодированным в base64
- **family.sig**: Подпись имени семейства и 32-байтового хеша router

Несколько routers из одного семейства не будут использоваться в одном tunnel.

### 2.6 Истечение срока действия RouterInfo (информация о router)

- Нет истечения в первый час работы
- Нет истечения при 25 или меньше сохранённых RouterInfos (записей с информацией о маршрутизаторах)
- Срок истечения уменьшается по мере роста локального числа routers (72 часа при <120 routers; ~30 часов при 300 routers)
- SSU introducers (вводящие узлы) истекают примерно через ~1 час
- Floodfills используют истечение через 1 час для всех локальных RouterInfos

---

## 3. LeaseSet

**LeaseSets** описывают точки входа в tunnel для конкретных назначений, указывая:

- **Идентичность router шлюза Tunnel**
- **4-байтовый tunnel ID**
- **Время истечения срока действия Tunnel**

LeaseSets include: - **Destination (адрес назначения)** – ключ шифрования, ключ подписи, сертификат - **Дополнительный открытый ключ шифрования** – для сквозного garlic encryption - **Дополнительный открытый ключ подписи** – предназначен для отзыва (в настоящее время не используется) - **Криптографическая подпись**

### 3.1 Варианты LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unpublished</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Destinations used only for outgoing connections aren't published to floodfill routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Revoked</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Published with zero leases, signed by additional signing key (not fully implemented)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet2 (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, supports new encryption types, multiple encryption types, options, offline signing keys ([Proposal 123](/proposals/123-new-netdb-entries/))</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Meta LeaseSet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tree-like DHT structure for multihomed services, supporting hundreds/thousands of destinations with long expirations (up to 18.2 hours)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS1)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All leases encrypted with separate key; only those with the key can decode and contact the destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Encrypted LeaseSet (LS2)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">As of 0.9.38, destination hidden with only blinded public key and expiration visible to floodfill</td>
    </tr>
  </tbody>
</table>
### 3.2 Истечение срока действия LeaseSet

Обычные LeaseSets истекают в момент самого позднего истечения срока действия их lease (lease — запись о сроке действия для конкретного tunnel). Срок действия LeaseSet2 указан в заголовке. Срок действия EncryptedLeaseSet и MetaLeaseSet может различаться; может применяться принудительное ограничение максимального срока.

---

## 4. Инициализация

Децентрализованная netDb требует как минимум одной ссылки на узел для включения в сеть. **Reseeding** (начальная загрузка netDb) загружает файлы RouterInfo (`routerInfo-$hash.dat`) из каталогов netDb добровольцев. При первом запуске они автоматически загружаются с жестко заданных URL-адресов, выбираемых случайным образом.

---

## 5. Механизм Floodfill

Система floodfill netDb использует простую распределённую схему хранения: данные отправляются ближайшему узлу floodfill. Когда узлы, не являющиеся floodfill, отправляют данные на сохранение, узлы floodfill пересылают их подмножеству узлов floodfill, ближайших к заданному ключу.

Участие в Floodfill указывается как флаг возможности (`f`) в RouterInfo.

### 5.1 Требования к добровольному участию в Floodfill

В отличие от жестко заданных доверенных серверов каталогов Tor, множество floodfill в I2P **не является доверенным** и со временем меняется.

Floodfill автоматически включается только на routers с высокой пропускной способностью, соответствующих следующим требованиям: - Минимум 128 KBytes/sec общей пропускной способности (настраивается вручную) - Должны пройти дополнительные тесты работоспособности (время ожидания в очереди исходящих сообщений, задержка задач)

Текущее автоматическое включение приводит примерно к **6% доле узлов сети, участвующих в floodfill**.

Ручные floodfill существуют наряду с автоматическими добровольцами. Когда число floodfill падает ниже порога, routers с высокой пропускной способностью автоматически берут на себя роль floodfill. Когда число floodfill становится слишком большим, они снимают с себя роль floodfill.

### 5.2 Роли Floodfill

Помимо приёма записей в netDb и обработки запросов, floodfills выполняют стандартные функции router. Их более высокая пропускная способность обычно означает участие в большем числе tunnel, но это не связано напрямую со службами базы данных.

---

## 6. Метрика близости Kademlia

В netDb используется измерение расстояния на основе XOR, **в стиле Kademlia**. Хэш SHA256 от RouterIdentity или Destination формирует ключ Kademlia (за исключением LS2 зашифрованных LeaseSets, которые используют SHA256 от байта типа 3 вместе с ослеплённым открытым ключом).

### 6.1 Ротация пространства ключей

Чтобы увеличить затраты на Sybil-атаку, вместо использования `SHA256(key)` система использует:

```
SHA256(key + yyyyMMdd)
```
где дата — это 8-байтовая дата UTC в ASCII. Это создаёт **ключ маршрутизации**, который меняется ежедневно в полночь по UTC — что называется **ротацией пространства ключей**.

Ключи маршрутизации никогда не передаются в сообщениях I2NP; они используются только для локального определения расстояния.

---

## 7. Сегментация Network Database (сетевая база данных I2P)

Традиционные DHT Kademlia не обеспечивают unlinkability (несвязываемость) хранимых данных. I2P предотвращает атаки, связывающие клиентские tunnels с routers, реализуя **сегментацию**.

### 7.1 Стратегия сегментации

Routers отслеживают: - Пришли ли записи через клиентские tunnels или напрямую - Если через tunnel, то какой клиентский tunnel/destination (адрес назначения в I2P) - Отслеживаются множественные поступления через tunnels - Различаются ответы на операции хранения и на операции поиска

Обе реализации на Java и C++ используют: - **"Основная" netDb** для прямых запросов/операций floodfill в контексте router - **"Клиентские сетевые базы данных"** или **"Под-базы данных"** в клиентских контекстах, собирающие записи, отправляемые в клиентские tunnels

Клиентские netDb существуют только на время жизни клиента и содержат только записи клиентских tunnel. Записи из клиентских tunnel не могут пересекаться с прямыми поступлениями.

Каждый netDb отслеживает, поступили ли записи как store (в ответ на запросы поиска) или как ответы на поиск (отвечают только если ранее были сохранены для того же назначения). Клиенты никогда не отвечают на запросы записями из основного netDb, только записями из клиентского netDb.

Комбинированные стратегии **сегментируют** netDb против атак на установление соответствия между клиентом и router.

---

## 8. Хранение, проверка и поиск

### 8.1 Сохранение RouterInfo (информация о router) у пиров

I2NP `DatabaseStoreMessage`, содержащее локальный RouterInfo (информация о маршрутизаторе) для обмена во время инициализации транспортного соединения NTCP или SSU.

### 8.2 Хранение LeaseSet у пиров

I2NP `DatabaseStoreMessage`, содержащие локальный LeaseSet, периодически передаются через сообщения, зашифрованные с помощью garlic encryption, в составе трафика Destination (адрес назначения в I2P), что позволяет отвечать без запросов к LeaseSet.

### 8.3 Выбор Floodfill

`DatabaseStoreMessage` отправляет ближайшему к текущему ключу маршрутизации floodfill. Ближайший floodfill определяется посредством поиска по локальной базе данных. Даже если это фактически не самый близкий, flooding (широковещательная рассылка) распространяет его "ближе", отправляя нескольким floodfill.

Традиционная Kademlia использует поиск "find-closest" (поиск ближайших узлов) перед вставкой. Хотя в I2NP нет таких сообщений, routers могут выполнять итеративный поиск с инверсией младшего значащего бита (`key ^ 0x01`), чтобы обеспечить обнаружение действительно ближайшего узла.

### 8.4 Сохранение RouterInfo на floodfill-узлах

Routers публикуют RouterInfo (информация о router), напрямую подключаясь к floodfill и отправляя I2NP `DatabaseStoreMessage` с ненулевым Reply Token (токеном ответа). Сообщение не использует сквозное garlic encryption (прямое соединение, без посредников). Floodfill отвечает `DeliveryStatusMessage`, используя Reply Token в качестве ID сообщения.

Routers также могут отправлять RouterInfo через исследовательский tunnel (ограничения на соединения, несовместимость, сокрытие IP). Floodfills могут отклонять такие операции хранения при перегрузке.

### 8.5 Хранение LeaseSet в узлах Floodfill

Хранение LeaseSet более чувствительно, чем хранение RouterInfo. Routers должны предотвращать привязку LeaseSet к себе.

Routers публикуют LeaseSet, отправляя через исходящий клиентский tunnel `DatabaseStoreMessage` с ненулевым токеном ответа. Сообщение сквозным образом зашифровано с использованием garlic encryption и менеджера сеансовых ключей Destination (идентификатор назначения в I2P), что скрывает его от конечной точки исходящего tunnel. Floodfill отвечает `DeliveryStatusMessage`, который возвращается через входящий tunnel.

### 8.6 Процесс flooding (массовой рассылки)

Floodfills (специализированные узлы netdb) проверяют RouterInfo/LeaseSet перед локальным сохранением, используя адаптивные критерии, зависящие от нагрузки, размера netdb и других факторов.

После получения более новых корректных данных floodfills "flood" их, находя 3 ближайших floodfill routers к ключу маршрутизации. Прямые соединения отправляют I2NP `DatabaseStoreMessage` с нулевым Reply Token (токен ответа). Другие routers не отвечают и не выполняют повторный flood.

**Важные ограничения:** - Floodfills не должны рассылать через tunnels; только прямые соединения - Floodfills никогда не рассылают устаревший LeaseSet или RouterInfo, опубликованные более часа назад

### 8.7 Поиск RouterInfo и LeaseSet

I2NP `DatabaseLookupMessage` запрашивает записи netdb у floodfill routers. Запросы отправляются через исходящий исследовательский tunnel; в ответах указывается входящий исследовательский tunnel для возврата.

Запросы поиска обычно отправляются к двум "хорошим" floodfill routers, ближайшим к запрашиваемому ключу, параллельно.

- **Локальное совпадение**: получает ответ I2NP `DatabaseStoreMessage`
- **Нет локального совпадения**: получает I2NP `DatabaseSearchReplyMessage` со ссылками на другие floodfill router (узлы индексирования), близкие к ключу

Запросы LeaseSet используют сквозное garlic encryption (начиная с 0.9.5). Запросы RouterInfo (описание узла I2P) не шифруются из-за высокой вычислительной стоимости алгоритма Эль-Гамаля, что делает их уязвимыми для перехвата на выходной конечной точке.

Начиная с версии 0.9.7, ответы на запросы поиска включают сеансовый ключ и тег, скрывая ответы от входного шлюза.

### 8.8 Итеративные поиски

До 0.8.9: два параллельных избыточных поиска без рекурсивной или итеративной маршрутизации.

Начиная с 0.8.9: **Итеративные поиски** реализованы без избыточности — более эффективны, надёжны и лучше подходят для неполного знания о floodfill. По мере роста сетей и уменьшения числа floodfills, известных routers, сложность поисков приближается к O(log n).

Итеративные поиски продолжаются даже при отсутствии ссылок на более близких узлов, что предотвращает злонамеренный black-holing (скрытое «поглощение» запросов без ответов). Действуют текущие значения максимального числа запросов и тайм-аута.

### 8.9 Проверка

**Проверка RouterInfo (запись с данными узла I2P)**: Отключена начиная с версии 0.9.7.1, чтобы предотвратить атаки, описанные в статье "Practical Attacks Against the I2P Network".

**Проверка LeaseSet**: Routers ждут ~10 секунд, затем выполняют запрос к другому floodfill (специализированному узлу каталога) через исходящий клиентский tunnel. Сквозное garlic encryption (многосообщенческое шифрование в I2P) скрывает это от исходящей конечной точки. Ответы возвращаются через входящие tunnels.

Начиная с 0.9.7, ответы шифруются с применением сокрытия ключа/тега сеанса от входного шлюза.

### 8.10 Исследование

**Исследование** включает поиск в netdb по случайным ключам, чтобы обнаруживать новые router. Узлы floodfill отвечают сообщением `DatabaseSearchReplyMessage`, содержащим хэши router, не являющихся floodfill, близкие к запрошенному ключу. Исследовательские запросы устанавливают специальный флаг в `DatabaseLookupMessage`.

---

## 9. Мультихоминг

Назначения, использующие идентичные закрытые/открытые ключи (традиционный `eepPriv.dat`), могут одновременно размещаться на нескольких router. Каждый экземпляр периодически публикует подписанные LeaseSets; наиболее недавно опубликованный LeaseSet отдаётся запрашивающим при поиске. При максимальном времени жизни LeaseSet в 10 минут простои длятся не более ~10 минут.

Начиная с 0.9.38, **Meta LeaseSets** поддерживают крупные мультихоминговые сервисы, использующие отдельные Destinations (адреса назначения в I2P), предоставляющие общие сервисы. Записи Meta LeaseSet — это Destinations или другие Meta LeaseSets со сроком действия до 18,2 часа, что позволяет иметь сотни/тысячи Destinations, размещающих общие сервисы.

---

## 10. Анализ угроз

В настоящее время работают примерно 1700 floodfill routers (специализированных узлов для распространения netDb). Рост сети делает большинство атак более сложными или менее эффективными.

### 10.1 Общие меры по смягчению рисков

- **Рост**: Увеличение числа floodfills делает атаки сложнее или менее ощутимыми
- **Избыточность**: Все записи netdb хранятся на 3 floodfill routers, ближайших к ключу, посредством flooding (массовой рассылки)
- **Подписи**: Все записи подписаны создателем; их подделка невозможна

### 10.2 Медленные или не отвечающие routers

Routers ведут расширенную статистику профилей пиров для floodfills: - Среднее время отклика - Процент отвеченных запросов - Процент успешной проверки сохранения - Последнее успешное сохранение - Последний успешный поиск - Последний ответ

Routers используют эти метрики при оценке «качества» для выбора ближайшего floodfill. Полностью не отвечающие routers быстро выявляются и избегаются; частично вредоносные routers представляют более серьёзную сложность.

### 10.3 Атака Сивиллы (полное пространство ключей)

Злоумышленники могут создать многочисленные floodfill routers, распределённые по всему пространству ключей, в качестве эффективной DoS-атаки.

Если подозрительное поведение недостаточно серьёзно для присвоения статуса "bad", возможные меры включают: - Составление списков хэшей router и IP, публикуемых через новости консоли, веб‑сайт, форум - Включение floodfill по всей сети («бороться с Sybil ещё большим количеством Sybil») - Новые версии ПО с жёстко заданными списками "bad" - Улучшенные метрики профилей пиров и пороги для автоматической идентификации - Квалификация IP‑блоков, запрещающая несколько floodfill в одном IP‑блоке - Автоматический чёрный список по подписке (аналогичный консенсусу Tor)

Более крупные сети делают это сложнее.

### 10.4 Атака Сивиллы (частичное пространство ключей)

Злоумышленники могут создать 8–15 экземпляров floodfill router, тесно сгруппированных в пространстве ключей. Все операции поиска/сохранения для этого пространства ключей будут направляться к router, контролируемым злоумышленником, что позволяет проводить DoS-атаку на конкретные I2P-сайты.

Поскольку пространство ключей индексирует криптографические хэши SHA256, атакующим требуется перебор, чтобы создать routers, расположенные достаточно близко (в пространстве ключей).

**Защита**: Алгоритм близости Kademlia со временем варьируется с использованием `SHA256(key + YYYYMMDD)`, обновляясь ежедневно в полночь по UTC. Эта **ротация пространства ключей** вынуждает ежедневную регенерацию атаки.

> **Примечание**: Недавние исследования показывают, что ротация пространства ключей не особенно эффективна — атакующие могут заранее предвычислить хэши router, и им достаточно нескольких router, чтобы затмить части пространства ключей в течение получаса после ротации.

Последствие ежедневной ротации: распределённая netdb становится ненадёжной на несколько минут после ротации — запросы поиска завершаются неудачей до того, как новый ближайший router получит вставки (stores).

### 10.5 Атаки на инициализацию

Злоумышленники могут перехватить контроль над reseed websites (сайтами начальной загрузки сети) или обманом склонить разработчиков добавить в список враждебные reseed websites, из‑за чего новые router будут запускаться в изолированных или контролируемых большинством сетях.

**Реализованные меры защиты:** - Получение подмножеств RouterInfo (запись с информацией о маршрутизаторе) с нескольких reseed-сайтов (сайтов первичной загрузки узлов) вместо одного сайта - Внешний по отношению к сети мониторинг reseed с периодическим опросом сайтов - Начиная с 0.9.14, наборы данных reseed распространяются как подписанные zip-файлы с проверкой загруженной подписи (см. [спецификацию su3](/docs/specs/updates))

### 10.6 Перехват запросов

Floodfill routers могут «направлять» пиров к контролируемым атакующим routers через возвращаемые ссылки.

Маловероятно через exploration (процедуру исследования пиров) из-за низкой частоты; routers получают ссылки на пиров главным образом в ходе обычного построения tunnel'ов.

Начиная с 0.8.9 реализованы итеративные поиски. Ссылки floodfill из `DatabaseSearchReplyMessage` используются, если они ближе к ключу поиска. Запрашивающие routers не доверяют оценке близости ссылок. Поиски продолжаются, даже при отсутствии более близких ключей, до истечения тайм-аута/достижения максимального числа запросов, что предотвращает злонамеренное black-holing (направление запросов в «черную дыру»).

### 10.7 Утечки информации

Утечка информации в DHT (распределённая хеш-таблица) в I2P требует дальнейшего исследования. Floodfill routers наблюдают за запросами, собирая информацию. При доле вредоносных узлов в 20% ранее описанные атаки Sybil (атаки с множественными личностями) становятся проблематичными по нескольким причинам.

---

## 11. Дальнейшая работа

- Сквозное шифрование дополнительных запросов и ответов netDb
- Улучшенные методы отслеживания ответов на поисковые запросы
- Методы смягчения проблем надежности, связанных с ротацией пространства ключей

---

## 12. Ссылки

- [Спецификация общих структур](/docs/specs/common-structures/) – структуры RouterInfo и LeaseSet
- [Спецификация I2NP](/docs/specs/i2np/) – типы сообщений базы данных
- [Предложение 123: Новые записи netDb](/proposals/123-new-netdb-entries) – спецификация LeaseSet2
- [Историческое обсуждение netDb](/docs/netdb/) – история разработки и архивные обсуждения
