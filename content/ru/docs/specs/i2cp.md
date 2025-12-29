---
title: "Клиентский протокол I2P (I2CP)"
description: "Как приложения согласовывают сессии, tunnels и LeaseSets с I2P router."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

I2CP — это низкоуровневый протокол управления между I2P router и любым клиентским процессом. Он определяет строгое разделение ответственности:

- **Router**: Управляет маршрутизацией, криптографией, жизненными циклами tunnel и операциями сетевой базы данных
- **Клиент**: Выбирает параметры анонимности, настраивает tunnels и отправляет/получает сообщения

Весь обмен данными осуществляется через один TCP-сокет (опционально — в TLS-обёртке), что обеспечивает асинхронную, полнодуплексную работу.

**Версия протокола**: I2CP использует байт версии протокола `0x2A` (42 в десятичной системе), отправляемый во время первоначального установления соединения. Этот байт версии оставался неизменным с момента создания протокола.

**Текущее состояние**: Эта спецификация актуальна для router версии 0.9.67 (версия API 0.9.67), выпущенной в сентябре 2025 года.

## Контекст реализации

### Реализация на Java

Референсная реализация находится в Java I2P: - Клиентский SDK: `i2p.jar` пакет - Реализация router: `router.jar` пакет - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Когда клиент и router выполняются в одной виртуальной машине Java (JVM), сообщения I2CP передаются как объекты Java без сериализации. Внешние клиенты используют сериализованный протокол поверх TCP.

### Реализация на C++

i2pd (C++ I2P router) также реализует I2CP как внешний интерфейс для клиентских подключений.

### Клиенты не на Java

Не существует **известных реализаций не на Java** полной клиентской библиотеки I2CP. Приложения не на Java должны вместо этого использовать более высокоуровневые протоколы:

- **SAM (Simple Anonymous Messaging — простой анонимный обмен сообщениями) v3**: Интерфейс на основе сокетов с библиотеками на нескольких языках программирования
- **BOB (Basic Open Bridge — базовый открытый мост)**: Более простая альтернатива SAM

Эти протоколы более высокого уровня скрывают сложность I2CP внутри себя и также предоставляют потоковую библиотеку (для TCP-подобных соединений) и библиотеку дейтаграмм (для UDP-подобных соединений).

## Установление соединения

### 1. TCP-соединение

Подключитесь к порту I2CP router:
- По умолчанию: `127.0.0.1:7654`
- Настраивается в настройках router
- Необязательная TLS-обёртка (настоятельно рекомендуется для удалённых подключений)

### 2. Рукопожатие протокола

**Шаг 1**: Отправьте байт версии протокола `0x2A`

**Шаг 2**: Синхронизация часов

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
router возвращает свою текущую метку времени и строку версии API I2CP (начиная с 0.8.7).

**Шаг 3**: Аутентификация (если включена)

Начиная с 0.9.11, аутентификация может быть включена в GetDateMessage в виде Mapping (структуры ключ-значение), который содержит: - `i2cp.username` - `i2cp.password`

Начиная с 0.9.16, если включена аутентификация, она **должна** быть завершена через GetDateMessage до отправки любых других сообщений.

**Шаг 4**: Создание сеанса

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Шаг 5**: Сигнал готовности Tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
Это сообщение сигнализирует о том, что входящие tunnels построены. router НЕ отправит его, пока не будут существовать как минимум один входящий И один исходящий tunnel.

**Шаг 6**: Публикация LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
На этом этапе сеанс полностью готов к отправке и получению сообщений.

## Шаблоны потоков сообщений

### Исходящее сообщение (клиент отправляет удалённому назначению)

**При i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**С i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Входящее сообщение (Router доставляет клиенту)

**При i2cp.fastReceive=true** (по умолчанию начиная с версии 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**При i2cp.fastReceive=false** (УСТАРЕЛО):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Современные клиенты всегда должны использовать режим быстрого приёма.

## Общие структуры данных

### Заголовок сообщения I2CP

Все сообщения I2CP используют этот общий заголовок:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Длина тела**: 4-байтовое целое число, длина только тела сообщения (без заголовка)
- **Тип**: 1-байтовое целое число, идентификатор типа сообщения
- **Тело сообщения**: 0+ байт, формат зависит от типа сообщения

**Ограничение размера сообщения**: Примерно 64 КБ максимум.

### Идентификатор сессии

Двухбайтовое целое число, уникально идентифицирующее сеанс на router.

**Специальное значение**: `0xFFFF` означает «нет сессии» (используется для разрешения имени хоста без установленной сессии).

### Идентификатор сообщения

4-байтовое целое число, генерируемое router для однозначной идентификации сообщения в рамках сеанса.

**Важно**: идентификаторы сообщений **не** являются глобально уникальными, они уникальны только в пределах сеанса. Они также отличаются от nonce (одноразового числа), генерируемого клиентом.

### Формат полезной нагрузки

Полезные данные сообщений сжимаются gzip с использованием стандартного 10-байтового заголовка gzip: - Начинается с: `0x1F 0x8B 0x08` (RFC 1952) - Начиная с 0.7.1: неиспользуемые части заголовка gzip содержат информацию о протоколе, from-port (порт-источник) и to-port (порт-назначение) - Это позволяет использовать потоковую передачу и дейтаграммы на одном и том же назначении

**Управление сжатием**: Установите `i2cp.gzip=false`, чтобы отключить сжатие (устанавливает уровень сжатия gzip в 0). Заголовок gzip по-прежнему включается, но накладные расходы на сжатие минимальны.

### Структура SessionConfig

Определяет конфигурацию для клиентского сеанса:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Критические требования**: 1. **Отображение должно быть отсортировано по ключу** для проверки подписи 2. **Дата создания** должна быть в пределах ±30 секунд от текущего времени router 3. **Подпись** создаётся с помощью SigningPrivateKey объекта Destination (адрес назначения в I2P)

**Офлайн-подписи** (по состоянию на 0.9.38):

При использовании офлайн-подписания Mapping (отображение ключ‑значение) должно содержать: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

Затем подпись генерируется временным закрытым ключом подписи (SigningPrivateKey).

## Параметры конфигурации ядра

### Конфигурация Tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Примечания**: - Значения параметра `quantity` > 6 требуют узлов, работающих на версии 0.9.0+, и существенно увеличивают потребление ресурсов - Установите `backupQuantity` в значение 1-2 для сервисов с высокой доступностью - Zero-hop tunnels (туннели без промежуточных узлов) жертвуют анонимностью ради снижения задержки, но полезны для тестирования

### Обработка сообщений

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Надёжность сообщений**: - `None`: Нет подтверждений от router (значение по умолчанию стриминговой библиотеки начиная с 0.8.1) - `BestEffort`: Router отправляет уведомления о принятии + об успехе/сбое - `Guaranteed`: Не реализовано (в настоящее время ведёт себя как BestEffort)

**Переопределение на уровне сообщения** (начиная с 0.9.14): - В сессии с `messageReliability=none`, установка ненулевого nonce (одноразовое число) запрашивает уведомление о доставке для этого конкретного сообщения - Установка nonce=0 в сессии `BestEffort` отключает уведомления для этого сообщения

### Конфигурация LeaseSet

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Устаревшие теги сеанса ElGamal/AES

Эти параметры применимы только к устаревшему шифрованию Эль-Гамаля:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Примечание**: Клиенты ECIES-X25519 используют другой механизм ратчета и игнорируют эти параметры.

## Типы шифрования

I2CP поддерживает несколько схем сквозного шифрования с помощью параметра `i2cp.leaseSetEncType`. Можно указать несколько типов (через запятую), чтобы обеспечить совместимость как с современными пирами, так и с пирами старых версий.

### Поддерживаемые типы шифрования

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Рекомендуемая конфигурация**:

```
i2cp.leaseSetEncType=4,0
```
Здесь используется X25519 (предпочтительно) с резервным переходом на ElGamal для совместимости.

### Подробности о типах шифрования

**Тип 0 - ElGamal/AES+SessionTags (одноразовые теги сессии)**: - 2048-битные открытые ключи ElGamal (256 байт) - симметричное шифрование AES-256 - 32-байтные session tags передаются партиями - высокие накладные расходы по CPU, полосе пропускания и памяти - постепенно выводится из эксплуатации по всей сети

**Тип 4 - ECIES-X25519-AEAD-Ratchet**: - Обмен ключами X25519 (ключи по 32 байта) - ChaCha20/Poly1305 AEAD - Двойной ратчет в стиле Signal - 8-байтовые теги сеанса (по сравнению с 32 байтами у ElGamal) - Теги генерируются с помощью синхронизированного PRNG (генератора псевдослучайных чисел; не отправляются заранее) - ~92% сокращение накладных расходов по сравнению с ElGamal - Стандарт для современного I2P (это используется большинством routers)

**Типы 5-6 - постквантовый гибрид**: - Комбинирует X25519 с ML-KEM (NIST FIPS 203) - Обеспечивает устойчивость к квантовым атакам - ML-KEM-768 — для баланса безопасности/производительности - ML-KEM-1024 — для максимальной безопасности - Увеличенный размер сообщений из-за постквантового ключевого материала - Поддержка в сети всё ещё внедряется

### Стратегия миграции

Сеть I2P активно мигрирует с ElGamal (тип 0) на X25519 (тип 4): - NTCP → NTCP2 (завершено) - SSU → SSU2 (завершено) - ElGamal tunnels → X25519 tunnels (завершено) - сквозное шифрование ElGamal → ECIES-X25519 (в основном завершено)

## LeaseSet2 (новый формат LeaseSet в I2P) и расширенные возможности

### Параметры LeaseSet2 (начиная с 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Ослеплённые адреса

Начиная с версии 0.9.39, назначения могут использовать адреса "blinded" (b33 format) (адреса с ослеплением — скрывают исходный публичный ключ), которые периодически меняются: - Требуется `i2cp.leaseSetSecret` для защиты паролем - Необязательная аутентификация для каждого клиента - Подробности см. в предложениях 123 и 149

### Сервисные записи (начиная с 0.9.66)

LeaseSet2 поддерживает параметры сервисной записи (предложение 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Формат следует стилю записей DNS SRV, но адаптирован для I2P.

## Несколько сеансов (начиная с 0.9.21)

Одно подключение по I2CP может поддерживать несколько сеансов:

**Основная сессия**: Первая сессия, созданная для соединения **Подсессии**: Дополнительные сессии, разделяющие пул tunnel основной сессии

### Характеристики подсессии

1. **Общие Tunnels**: Используют те же пулы входящих/исходящих tunnel, что и у основного
2. **Общие ключи шифрования**: Должны использовать идентичные ключи шифрования LeaseSet
3. **Разные ключи подписи**: Должны использовать различные ключи подписи Destination (адрес назначения)
4. **Нет гарантии анонимности**: Явно связаны с основным сеансом (тот же router, те же tunnels)

### Сценарий использования подсессии

Включить связь с назначениями, использующими разные типы подписи: - Основной: подпись EdDSA (современная) - Subsession (подсессия): подпись DSA (обратная совместимость)

### Жизненный цикл подсессии

**Создание**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Уничтожение**: - Уничтожение подсессии: Оставляет основную сессию нетронутой - Уничтожение основной сессии: Уничтожает все подсессии и закрывает соединение - DisconnectMessage (сообщение отключения): Уничтожает все сессии

### Обработка идентификатора сеанса

Большинство сообщений I2CP содержат поле идентификатора сеанса (Session ID). Исключения: - DestLookup / DestReply (устарели, используйте HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (ответ не зависит от сеанса)

**Важно**: Клиентам не следует иметь несколько одновременно незавершённых сообщений CreateSession, поскольку ответы нельзя однозначно сопоставить с запросами.

## Каталог сообщений

### Сводка типов сообщений

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Условные обозначения**: C = Клиент, R = Router

### Ключевые сведения о сообщении

#### CreateSessionMessage (Тип 1)

**Назначение**: Инициировать новый сеанс I2CP

**Содержимое**: структура SessionConfig (конфигурация сеанса)

**Ответ**: SessionStatusMessage (status=Created или Invalid)

**Требования**: - Время в SessionConfig должно находиться в пределах ±30 секунд от времени на router (маршрутизаторе) - Отображение должно быть отсортировано по ключу для проверки подписи - У Destination (адрес назначения) не должно уже быть активного сеанса

#### RequestVariableLeaseSetMessage (Тип 37)

**Назначение**: Router запрашивает авторизацию клиента для входящих tunnels

**Содержимое**: - ID сессии - Количество Lease (элемент LeaseSet) - Массив структур Lease (каждая со своим временем истечения)

**Ответ**: CreateLeaseSet2Message

**Значение**: Это сигнал о том, что сеанс работоспособен. router отправляет это только после: 1. Построен хотя бы один входящий tunnel 2. Построен хотя бы один исходящий tunnel

**Рекомендация по тайм-ауту**: Клиентам следует закрыть сеанс, если это сообщение не получено в течение 5 минут и более с момента создания сеанса.

#### CreateLeaseSet2Message (Тип 41)

**Назначение**: Клиент публикует LeaseSet в сетевую базу данных

**Содержимое**: - ID сессии - байт типа LeaseSet (1, 3, 5 или 7) - LeaseSet или LeaseSet2 или EncryptedLeaseSet или MetaLeaseSet - Количество закрытых ключей - Список закрытых ключей (по одному на каждый публичный ключ в LeaseSet, в том же порядке)

**Закрытые ключи**: Необходимы для расшифровки входящих garlic messages (механизм I2P объединения нескольких сообщений для повышения анонимности). Формат:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Примечание**: Заменяет устаревший CreateLeaseSetMessage (тип 4), который не поддерживает: - Варианты LeaseSet2 - Шифрование, не основанное на ElGamal - Несколько типов шифрования - Зашифрованные LeaseSets - Офлайн-ключи подписи

#### SendMessageExpiresMessage (Тип 36)

**Назначение**: Отправить сообщение на адрес назначения с указанием срока действия и расширенными параметрами

**Содержимое**: - ID сеанса - Адрес назначения - Полезная нагрузка (gzipped) - Нонс (4 байта) - Флаги (2 байта) - см. ниже - Дата истечения срока (6 байт, усечено с 8 байт)

**Поле флагов** (2 байта, порядок битов 15...0):

**Биты 15–11**: не используются, должны быть 0

**Биты 10-9**: Переопределение надёжности сообщения (не используется, вместо этого используйте nonce (одноразовое число))

**Бит 8**: Не вкладывать LeaseSet - 0: Router может вкладывать LeaseSet в garlic (многокомпонентное зашифрованное сообщение I2P) - 1: Не вкладывать LeaseSet

**Биты 7-4**: Низкий порог тегов (только для ElGamal, игнорируется для ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Биты 3-0**: Метки для отправки при необходимости (только ElGamal, игнорируется для ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (сообщение о статусе) (тип 22)

**Назначение**: Уведомить клиента о статусе доставки сообщения

**Содержимое**: - Идентификатор сеанса - Идентификатор сообщения (генерируется router) - Код статуса (1 байт) - Размер (4 байта, имеет значение только при status=0) - Nonce (одноразовое число; 4 байта, совпадает с nonce клиента из SendMessage)

**Коды состояния** (исходящие сообщения):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Коды успеха**: 1, 2, 4, 6 **Коды ошибок**: все остальные

**Код состояния 0** (УСТАРЕВШЕ): Сообщение доступно (входящее, быстрый приём отключён)

#### HostLookupMessage (Тип 38)

**Назначение**: Поиск адреса назначения по имени хоста или хешу (заменяет DestLookup)

**Содержимое**: - ID сессии (или 0xFFFF при отсутствии сессии) - ID запроса (4 байта) - Тайм-аут в миллисекундах (4 байта, минимально рекомендуемое значение: 10000) - Тип запроса (1 байт) - Ключ поиска (Hash (хэш), строка hostname, или Destination (идентификатор назначения в I2P))

**Типы запросов**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Типы 2-4 возвращают параметры LeaseSet (предложение 167), если доступны.

**Ответ**: HostReplyMessage (сообщение ответа хоста)

#### HostReplyMessage (тип 39)

**Назначение**: Ответ на HostLookupMessage (запрос на разрешение имени хоста)

**Содержимое**: - Идентификатор сессии - Идентификатор запроса - Код результата (1 байт) - Назначение (присутствует при успехе, иногда — при некоторых конкретных ошибках) - Сопоставление (только для типов поиска 2-4, может быть пустым)

**Коды результатов**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (сообщение с информацией об ослеплении) (Тип 42)

**Назначение**: Сообщает router о требованиях к аутентификации для blinded destination (ослеплённый Destination) (начиная с 0.9.43)

**Содержимое**: - ID сеанса - Флаги (1 байт) - Тип конечной точки (1 байт): 0=хеш, 1=имя хоста, 2=назначение, 3=SigType+Key - Тип слепой подписи (2 байта) - Срок действия (4 байта, в секундах от эпохи Unix) - Данные конечной точки (зависят от типа) - Закрытый ключ (32 байта, только если установлен бит 0 флага) - Пароль для поиска (String, только если установлен бит 4 флага)

**Флаги** (порядок битов 76543210):

- **Бит 0**: 0=для всех, 1=для каждого клиента
- **Биты 3-1**: Схема аутентификации (если бит 0=1): 000=DH (Диффи-Хеллман), 001=PSK (предварительно разделённый ключ)
- **Бит 4**: 1=требуется секрет
- **Биты 7-5**: Не используется, установить в 0

**Нет ответа**: Router обрабатывает молча

**Сценарий использования**: Перед отправкой на ослеплённое назначение (адрес b33) клиент должен либо: 1. выполнить поиск b33 через HostLookup, ИЛИ 2. отправить сообщение BlindingInfo

Если Destination (идентификатор назначения в I2P) требует аутентификации, BlindingInfo (информация для ослепления Destination) является обязательным.

#### ReconfigureSessionMessage (Тип 2)

**Назначение**: Обновить конфигурацию сеанса после создания

**Содержимое**: - ID сессии - SessionConfig (нужны только изменённые параметры)

**Ответ**: SessionStatusMessage (status=Updated or Invalid)

**Примечания**: - Router объединяет новую конфигурацию с существующей конфигурацией - Параметры Tunnel (`inbound.*`, `outbound.*`) всегда применяются - Некоторые параметры могут быть неизменяемыми после создания сеанса - Дата должна находиться в пределах ±30 секунд от времени Router - Отображение должно быть отсортировано по ключу

#### DestroySessionMessage (Тип 3)

**Назначение**: Завершить сеанс

**Содержимое**: Идентификатор сеанса

**Ожидаемый ответ**: SessionStatusMessage (status=Destroyed)

**Фактическое поведение** (Java I2P до версии 0.9.66 включительно): - Router никогда не отправляет SessionStatus(Destroyed) - Если сеансов не осталось: Отправляет DisconnectMessage - Если остаются subsessions (подсеансы): Нет ответа

**Важно**: Поведение Java I2P отличается от спецификации. Реализациям следует проявлять осторожность при удалении отдельных подсессий.

#### DisconnectMessage (тип 30)

**Назначение**: Уведомить о скором завершении соединения

**Содержимое**: Строка причины

**Effect**: Все сеансы этого соединения уничтожаются, сокет закрывается

**Реализация**: Преимущественно router → клиент в Java I2P

## История версий протокола

### Определение версии

Информация о версии протокола I2CP обменивается в сообщениях Get/SetDate (начиная с 0.8.7). Для старых router информация о версии недоступна.

**Строка версии**: Указывает версию API "core", не обязательно версию router.

### Хронология функций

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Соображения безопасности

### Аутентификация

**По умолчанию**: Аутентификация не требуется **Необязательно**: Аутентификация по имени пользователя/паролю (начиная с 0.9.11) **Обязательно**: При включении аутентификация должна завершиться до других сообщений (начиная с 0.9.16)

**Удалённые подключения**: Всегда используйте TLS (`i2cp.SSL=true`), чтобы защитить учётные данные и закрытые ключи.

### Смещение часов

Значение SessionConfig Date должно находиться в пределах ±30 секунд от времени router, иначе сеанс будет отклонён. Для синхронизации используйте Get/SetDate.

### Обращение с закрытым ключом

CreateLeaseSet2Message содержит закрытые ключи для расшифровки входящих сообщений. Эти ключи должны: - Передаваться безопасно (TLS для удалённых подключений) - Храниться в защищённом виде у router - Заменяться при компрометации

### Истечение срока действия сообщения

Всегда используйте SendMessageExpires (а не SendMessage), чтобы указать явный срок истечения. Это позволяет:
- предотвращать бесконечное зависание сообщений в очереди
- снижать потребление ресурсов
- повышать надёжность

### Управление тегами сеанса

**ElGamal** (устаревший): - Теги должны передаваться пакетами - Потеря тегов приводит к ошибкам расшифрования - Высокие накладные расходы по памяти

**ECIES-X25519** (текущий): - Теги генерируются синхронизированным ГПСЧ - Предварительная передача не требуется - Устойчив к потере сообщений - Существенно меньшие накладные расходы

## Лучшие практики

### Для разработчиков клиентских приложений

1. **Используйте режим быстрого приёма**: Всегда устанавливайте `i2cp.fastReceive=true` (или оставьте значение по умолчанию)

2. **Предпочитайте ECIES-X25519**: Настройте `i2cp.leaseSetEncType=4,0` для лучшей производительности при сохранении совместимости

3. **Задайте явное время истечения**: Используйте SendMessageExpires, а не SendMessage

4. **Осторожно обращайтесь с подсессиями**: Имейте в виду, что подсессии не обеспечивают анонимности между адресами назначения

5. **Тайм-аут при создании сеанса**: Уничтожить сеанс, если RequestVariableLeaseSet не получен в течение 5 минут

6. **Сортировка сопоставлений конфигурации**: Всегда сортируйте ключи сопоставлений перед подписанием SessionConfig

7. **Используйте подходящее количество Tunnel**: Не устанавливайте `quantity` > 6, если это не требуется

8. **Рассмотрите SAM/BOB для приложений не на Java**: Реализуйте SAM вместо прямого использования I2CP

### Для разработчиков Router

1. **Проверка дат**: Соблюдать окно ±30 секунд для дат в SessionConfig

2. **Ограничить размер сообщений**: Обеспечить соблюдение максимального размера сообщения ~64 КБ

3. **Поддержка нескольких сессий**: Реализовать поддержку подсессий в соответствии со спецификацией 0.9.21

4. **Отправьте RequestVariableLeaseSet незамедлительно**: только после того, как будут созданы и входящие, и исходящие tunnels

5. **Обрабатывать устаревшие сообщения**: Принимать, но не рекомендовать ReceiveMessageBegin/End

6. **Поддержка ECIES-X25519 (ECIES на основе X25519)**: Отдавайте приоритет шифрованию типа 4 в новых развертываниях

## Отладка и устранение неполадок

### Распространённые проблемы

**Сессия отклонена (недействительна)**: - Проверьте расхождение часов (должно быть в пределах ±30 секунд) - Проверьте, что отображение отсортировано по ключу - Убедитесь, что адрес назначения ещё не используется

**Нет RequestVariableLeaseSet**: - Router может создавать tunnels (подождите до 5 минут) - Проверьте наличие проблем с сетевым подключением - Убедитесь в достаточном количестве соединений с пирами

**Сбои доставки сообщений**: - Проверьте коды MessageStatus, чтобы определить конкретную причину сбоя - Проверьте, что удалённый LeaseSet опубликован и актуален - Убедитесь, что используются совместимые типы шифрования

**Проблемы с подсессией**: - Убедитесь, что основная сессия создана первой - Подтвердите, что используются те же ключи шифрования - Проверьте, что ключи подписи различаются

### Диагностические сообщения

**GetBandwidthLimits**: Запросить лимиты пропускной способности router **HostLookup**: Проверить разрешение имени и доступность LeaseSet **MessageStatus**: Отслеживать сквозную доставку сообщений

## Связанные спецификации

- **Общие структуры**: /docs/specs/common-structures/
- **I2NP (сетевой протокол)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Создание tunnel'ов**: /docs/specs/implementation/
- **Библиотека потоков**: /docs/specs/streaming/
- **Библиотека дейтаграмм**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Упомянутые предложения

- [Предложение 123](/proposals/123-new-netdb-entries/): Зашифрованные LeaseSets и аутентификация
- [Предложение 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Предложение 149](/proposals/149-b32-encrypted-ls2/): Формат ослепленного адреса (b33)
- [Предложение 152](/proposals/152-ecies-tunnels/): Создание tunnel на основе X25519
- [Предложение 154](/proposals/154-ecies-lookups/): Запросы к базе данных из ECIES Destinations (адреса назначения)
- [Предложение 156](/proposals/156-ecies-routers/): Миграция router на ECIES-X25519
- [Предложение 161](/ru/proposals/161-ri-dest-padding/): Сжатие заполнения Destination
- [Предложение 167](/proposals/167-service-records/): Сервисные записи LeaseSet
- [Предложение 169](/proposals/169-pq-crypto/): Гибридная постквантовая криптография (ML-KEM)

## Справочник по Javadoc

- [Пакет I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [Клиентское API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Сводка устареваний

### Устаревшие сообщения (не использовать)

- **CreateLeaseSetMessage** (тип 4): Используйте CreateLeaseSet2Message
- **RequestLeaseSetMessage** (тип 21): Используйте RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (тип 6): Используйте режим быстрого приёма
- **ReceiveMessageEndMessage** (тип 7): Используйте режим быстрого приёма
- **DestLookupMessage** (тип 34): Используйте HostLookupMessage
- **DestReplyMessage** (тип 35): Используйте HostReplyMessage
- **ReportAbuseMessage** (тип 29): Никогда не реализовано

### Устаревшие параметры

- Шифрование Эль-Гамаля (тип 0): перейти на ECIES-X25519 (тип 4)
- Подписи DSA: перейти на EdDSA или ECDSA
- `i2cp.fastReceive=false`: Всегда использовать режим быстрого приёма
