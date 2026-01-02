---
title: "Потоковый протокол"
description: "TCP-подобный транспорт, используемый большинством I2P-приложений"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

**I2P Streaming Library** обеспечивает надежную, упорядоченную и аутентифицированную передачу данных поверх слоя сообщений I2P, аналогично **TCP поверх IP**. Она располагается над [протоколом I2CP](/docs/specs/i2cp/) и используется практически всеми интерактивными приложениями I2P, включая HTTP-прокси, IRC, BitTorrent и электронную почту.

### Основные характеристики

- Однофазная установка соединения с использованием флагов **SYN**, **ACK** и **FIN**, которые могут объединяться с полезной нагрузкой для уменьшения количества циклов обмена данными.
- **Управление перегрузкой со скользящим окном** с медленным стартом и предотвращением перегрузки, настроенными для высоколатентной среды I2P.
- Сжатие пакетов (по умолчанию сегменты размером 4 КБ в сжатом виде), балансирующее стоимость повторной передачи и задержку фрагментации.
- Полностью **аутентифицированный, зашифрованный** и **надежный** канал между I2P-назначениями.

Эта конструкция позволяет небольшим HTTP-запросам и ответам завершаться за один цикл обмена данными. SYN-пакет может нести полезную нагрузку запроса, в то время как SYN/ACK/FIN ответчика может содержать полное тело ответа.

---

## Основы API

Java streaming API соответствует стандартному программированию сокетов в Java:

```java
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(host, port, options);
I2PSocket socket       = mgr.connect(destination);
I2PServerSocket server = mgr.getServerSocket();
```
- `I2PSocketManagerFactory` согласовывает или повторно использует сессию router через I2CP.
- Если ключ не предоставлен, новый destination создаётся автоматически.
- Разработчики могут передавать параметры I2CP (например, длину tunnel, типы шифрования или настройки соединения) через карту `options`.
- `I2PSocket` и `I2PServerSocket` повторяют стандартные интерфейсы Java `Socket`, что делает миграцию простой.

Полные Javadocs доступны из консоли I2P router или [здесь](/docs/specs/streaming/).

---

## Конфигурация и настройка

Вы можете передать свойства конфигурации при создании менеджера сокетов через:

```java
I2PSocketManagerFactory.createManager(host, port, properties);
```
### Ключевые опции

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum send window (bytes)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128 KB</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Timeout before connection close</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.enforceProtocol</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enforce protocol ID (prevents confusion)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">true</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.congestionAlgorithm</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion control method</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default (AIMD TCP-like)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.streaming.disableRejectLogging</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Disable logging rejected packets</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">false</td>
    </tr>
  </tbody>
</table>
### Поведение в зависимости от рабочей нагрузки

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Workload</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Settings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>HTTP-like</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default parameters are ideal.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Bulk Transfer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Increase window size to 256 KB or 512 KB; lengthen timeouts.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Real-time Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length to 1-2 hops; adjust RTO downwards.</td>
    </tr>
  </tbody>
</table>
Новые функции, начиная с версии 0.9.4, включают подавление журнала отклонений, поддержку списков DSA (0.9.21) и обязательное соблюдение протокола (0.9.36). Роутеры начиная с версии 2.10.0 включают постквантовое гибридное шифрование (ML-KEM + X25519) на транспортном уровне.

---

## Детали протокола

Каждый поток идентифицируется по **Stream ID**. Пакеты несут управляющие флаги, аналогичные TCP: `SYNCHRONIZE`, `ACK`, `FIN` и `RESET`. Пакеты могут одновременно содержать как данные, так и управляющие флаги, что повышает эффективность для кратковременных соединений.

### Жизненный цикл соединения

1. **SYN отправлен** — инициатор включает необязательные данные.  
2. **SYN/ACK ответ** — отвечающая сторона включает необязательные данные.  
3. **ACK финализация** — устанавливает надёжность и состояние сессии.  
4. **FIN/RESET** — используется для упорядоченного закрытия или внезапного завершения.

### Фрагментация и переупорядочивание

Поскольку I2P tunnel вносят задержки и изменяют порядок сообщений, библиотека буферизует пакеты из неизвестных или рано прибывших потоков. Буферизованные сообщения хранятся до завершения синхронизации, обеспечивая полную доставку в правильном порядке.

### Применение протокола

Опция `i2p.streaming.enforceProtocol=true` (по умолчанию с версии 0.9.36) гарантирует, что соединения используют правильный номер протокола I2CP, предотвращая конфликты между несколькими подсистемами, использующими одно назначение.

---

## Совместимость и Лучшие Практики

Протокол потоковой передачи сосуществует с **Datagram API**, предоставляя разработчикам выбор между транспортом с установлением соединения и без установления соединения.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reliable, ordered data (HTTP, IRC, FTP)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connectionless or lossy data (DNS, telemetry)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
    </tr>
  </tbody>
</table>
### Общие клиенты

Приложения могут повторно использовать существующие туннели, работая как **общие клиенты** (shared clients), что позволяет нескольким сервисам использовать один и тот же destination. Хотя это снижает накладные расходы, это увеличивает риск корреляции между сервисами — используйте с осторожностью.

### Управление перегрузкой

- Потоковый уровень постоянно адаптируется к задержкам и пропускной способности сети с помощью обратной связи на основе RTT.
- Приложения работают лучше всего, когда роутеры являются активными участниками (включены туннели для участия в сети).
- Механизмы контроля перегрузки, подобные TCP, предотвращают перегрузку медленных узлов и помогают балансировать использование пропускной способности между туннелями.

### Соображения по задержкам

Поскольку I2P добавляет несколько сотен миллисекунд базовой задержки, приложения должны минимизировать количество обменов данными. По возможности объединяйте данные с установкой соединения (например, HTTP-запросы в SYN). Избегайте архитектур, основанных на многочисленных последовательных обменах небольшими порциями данных.

---

## Тестирование и совместимость

- Всегда тестируйте совместимость с **Java I2P** и **i2pd**.  
- Несмотря на стандартизацию протокола, могут существовать незначительные различия в реализации.  
- Корректно обрабатывайте устаревшие router'ы — многие узлы по-прежнему используют версии до 2.0.  
- Отслеживайте статистику соединений с помощью `I2PSocket.getOptions()` и `getSession()` для получения метрик RTT и повторных передач.

Производительность сильно зависит от конфигурации tunnel:   - **Короткие tunnel (1–2 hop)** → меньшая задержка, сниженная анонимность.   - **Длинные tunnel (3+ hop)** → более высокая анонимность, увеличенное RTT.

---

## Ключевые улучшения (2.0.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent ACK Bundling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optimized round-trip reduction for HTTP workloads.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Adaptive Window Scaling</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved large file transfer stability.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling and Socket Reuse</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced per-connection overhead.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Protocol Enforcement Default</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures correct stream usage.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hybrid ML-KEM Ratchet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adds post-quantum hybrid encryption layer.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd Streaming API Compatibility Fixes</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full parity with Java I2P library behavior.</td>
    </tr>
  </tbody>
</table>
---

## Краткое описание

**I2P Streaming Library** — это основа всех надёжных коммуникаций в I2P. Она обеспечивает упорядоченную, аутентифицированную и зашифрованную доставку сообщений и предоставляет практически готовую замену TCP в анонимных средах.

Для достижения оптимальной производительности: - Минимизируйте количество циклов обмена данными с помощью объединения SYN+полезной нагрузки.   - Настройте параметры окна и тайм-аута для вашей рабочей нагрузки.   - Отдавайте предпочтение более коротким tunnel для приложений, чувствительных к задержкам.   - Используйте дизайн, учитывающий перегрузки, чтобы избежать перегрузки узлов.
