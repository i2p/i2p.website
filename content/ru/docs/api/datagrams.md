---
title: "Датаграммы"
description: "Аутентифицированный, с возможностью ответа и сырой форматы сообщений поверх I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Обзор

Датаграммы обеспечивают ориентированную на сообщения коммуникацию поверх [I2CP](/docs/specs/i2cp/) и параллельно с библиотекой потоковой передачи данных. Они позволяют отправлять **пакеты с возможностью ответа**, **аутентифицированные** или **сырые** пакеты без необходимости использования потоков с установлением соединения. Роутеры инкапсулируют датаграммы в I2NP-сообщения и tunnel-сообщения, независимо от того, используется ли для передачи трафика NTCP2 или SSU2.

Основная мотивация заключается в том, чтобы позволить приложениям (таким как трекеры, DNS-резолверы или игры) отправлять самодостаточные пакеты, которые идентифицируют своего отправителя.

> **Новое в 2025 году:** Проект I2P утвердил **Datagram2 (протокол 19)** и **Datagram3 (протокол 20)**, добавив защиту от повторов и обмен сообщениями с ответами и низкими накладными расходами впервые за десятилетие.

---

## 1. Константы протокола

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Протоколы 19 и 20 были формализованы в **Предложении 163 (апрель 2025 года)**. Они сосуществуют с Datagram1 / RAW для обратной совместимости.

---

## 2. Типы датаграмм

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Типовые шаблоны проектирования

- **Запрос → Ответ:** Отправить подписанный Datagram2 (запрос + nonce), получить raw или Datagram3 ответ (echo nonce).  
- **Высокая частота/низкие накладные расходы:** Предпочтительно использовать Datagram3 или RAW.  
- **Аутентифицированные управляющие сообщения:** Datagram2.  
- **Совместимость с устаревшими версиями:** Datagram1 по-прежнему полностью поддерживается.

---

## 3. Детали Datagram2 и Datagram3 (2025)

### Datagram2 (Протокол 19)

Улучшенная замена Datagram1. Возможности: - **Защита от повторов:** 4-байтовый токен защиты от повторного воспроизведения. - **Поддержка оффлайн-подписей:** позволяет использовать Destinations с оффлайн-подписью. - **Расширенное покрытие подписью:** включает хеш destination, флаги, опции, блок оффлайн-подписи, полезную нагрузку. - **Готовность к постквантовой эре:** совместимость с будущими гибридами ML-KEM. - **Накладные расходы:** ≈ 457 байт (ключи X25519).

### Datagram3 (Протокол 20)

Связывает необработанные и подписанные типы. Особенности: - **Возможность ответа без подписи:** содержит 32-байтовый хэш отправителя + 2-байтовые флаги. - **Минимальные накладные расходы:** ≈ 34 байта. - **Без защиты от повторов** — должно быть реализовано приложением.

Оба протокола являются функциями API 0.9.66 и реализованы в Java router начиная с Release 2.9.0; реализаций для i2pd или Go пока нет (октябрь 2025).

---

## 4. Ограничения по размеру и фрагментации

- **Размер сообщения tunnel:** 1 028 байт (4 Б Tunnel ID + 16 Б IV + 1 008 Б полезная нагрузка).  
- **Начальный фрагмент:** 956 Б (типичная доставка TUNNEL).  
- **Последующий фрагмент:** 996 Б.  
- **Максимум фрагментов:** 63–64.  
- **Практический лимит:** ≈ 62 708 Б (~61 КБ).  
- **Рекомендуемый лимит:** ≤ 10 КБ для надёжной доставки (потери увеличиваются экспоненциально выше этого значения).

**Сводка по накладным расходам:** - Datagram1 ≈ 427 Б (минимум).   - Datagram2 ≈ 457 Б.   - Datagram3 ≈ 34 Б.   - Дополнительные уровни (заголовок I2CP gzip, I2NP, Garlic, Tunnel): + ~5,5 КБ в худшем случае.

---

## 5. Интеграция I2CP / I2NP

Путь сообщения: 1. Приложение создает датаграмму (через I2P API или SAM).   2. I2CP оборачивает её заголовком gzip (`0x1F 0x8B 0x08`, RFC 1952) и контрольной суммой CRC-32.   3. Номера протокола + порта сохраняются в полях заголовка gzip.   4. Router инкапсулирует как I2NP сообщение → Garlic clove → фрагменты tunnel по 1 КБ.   5. Фрагменты проходят через outbound → сеть → inbound tunnel.   6. Собранная датаграмма доставляется обработчику приложения на основе номера протокола.

**Целостность:** CRC-32 (из I2CP) + опциональная криптографическая подпись (Datagram1/2). Отдельного поля контрольной суммы внутри самой датаграммы нет.

---

## 6. Программные интерфейсы

### Java API

Пакет `net.i2p.client.datagram` включает: - `I2PDatagramMaker` – создаёт подписанные датаграммы.   - `I2PDatagramDissector` – проверяет и извлекает информацию об отправителе.   - `I2PInvalidDatagramException` – выбрасывается при сбое проверки.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) управляет мультиплексированием протоколов и портов для приложений, использующих общий Destination.

**Доступ к Javadoc:** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (только в сети I2P) - [Зеркало Javadoc](https://eyedeekay.github.io/javadoc-i2p/) (зеркало в clearnet) - [Официальная Javadoc](http://docs.i2p-projekt.de/javadoc/) (официальная документация)

### Поддержка SAM v3

- SAM 3.2 (2016): добавлены параметры PORT и PROTOCOL.  
- SAM 3.3 (2016): введена модель PRIMARY/subsession; позволяет использовать потоки + датаграммы на одном Destination.  
- Добавлена поддержка стилей сессий Datagram2 / 3 в спецификацию 2025 (реализация ожидается).  
- Официальная спецификация: [Спецификация SAM v3](/docs/api/samv3/)

### Модули i2ptunnel

- **udpTunnel:** Полностью функциональная основа для I2P UDP-приложений (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Работает для A/V потоковой передачи (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Не функционален** по состоянию на 2.10.0 (только заглушка UDP).

> Для UDP общего назначения используйте Datagram API или udpTunnel напрямую — не полагайтесь на SOCKS UDP.

---

## 7. Экосистема и поддержка языков (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
На данный момент Java I2P является единственным router, поддерживающим полные подсессии SAM 3.3 и API Datagram2.

---

## 8. Пример использования – UDP Tracker (I2PSnark 2.10.0)

Первое реальное применение Datagram2/3:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Паттерн демонстрирует комбинированное использование аутентифицированных и облегченных датаграмм для баланса между безопасностью и производительностью.

---

## 9. Безопасность и рекомендации

- Используйте Datagram2 для любого аутентифицированного обмена или когда важны атаки повторного воспроизведения.
- Предпочитайте Datagram3 для быстрых ответов с возможностью ответа при умеренном доверии.
- Используйте RAW для публичных широковещательных рассылок или анонимных данных.
- Держите полезную нагрузку ≤ 10 КБ для надежной доставки.
- Имейте в виду, что SOCKS UDP остается нерабочим.
- Всегда проверяйте CRC gzip и цифровые подписи при получении.

---

## 10. Техническая спецификация

Этот раздел описывает низкоуровневые форматы датаграмм, инкапсуляцию и детали протокола.

### 10.1 Идентификация протокола

Форматы датаграмм **не** имеют общего заголовка. Роутеры не могут определить тип только по байтам полезной нагрузки.

При смешивании нескольких типов датаграмм — или при комбинировании датаграмм с потоковой передачей — явно устанавливайте: - **Номер протокола** (через I2CP или SAM) - Опционально **номер порта**, если ваше приложение мультиплексирует сервисы

Оставлять протокол неустановленным (`0` или `PROTO_ANY`) не рекомендуется, так как это может привести к ошибкам маршрутизации или доставки.

### 10.2 Сырые датаграммы

Датаграммы без возможности ответа (non-repliable datagrams) не содержат данных отправителя или аутентификации. Это непрозрачные полезные нагрузки, обрабатываемые вне API датаграмм более высокого уровня, но поддерживаемые через SAM и I2PTunnel.

**Протокол:** `18` (`PROTO_DATAGRAM_RAW`)

**Формат:**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
Длина полезной нагрузки ограничена лимитами транспорта (≈32 КБ практический максимум, часто намного меньше).

### 10.3 Datagram1 (Датаграммы с возможностью ответа)

Встраивает **Destination** отправителя и **Signature** для аутентификации и адресации ответов.

**Протокол:** `17` (`PROTO_DATAGRAM`)

**Накладные расходы:** ≥427 байт **Полезная нагрузка:** до ~31,5 КБ (ограничено транспортом)

**Формат:**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from`: Destination (387+ байт)
- `signature`: Signature, соответствующая типу ключа
  - Для DSA_SHA1: Signature SHA-256 хеша полезной нагрузки
  - Для других типов ключей: Signature непосредственно полезной нагрузки

**Примечания:** - Подписи для типов, отличных от DSA, были стандартизированы в I2P 0.9.14. - Оффлайн-подписи LS2 (Предложение 123) в настоящее время не поддерживаются в Datagram1.

### 10.4 Формат Datagram2

Улучшенная датаграмма с возможностью ответа, которая добавляет **защиту от повторов** согласно определению в [Предложении 163](/proposals/163-datagram2/).

**Протокол:** `19` (`PROTO_DATAGRAM2`)

Реализация продолжается. Приложения должны включать проверки nonce или временных меток для избыточности.

### 10.5 Формат Datagram3

Обеспечивает **датаграммы с возможностью ответа, но без аутентификации**. Полагается на аутентификацию сессии, поддерживаемую роутером, а не на встроенный destination и подпись.

**Протокол:** `20` (`PROTO_DATAGRAM3`) **Статус:** В разработке с версии 0.9.66

Полезно в случаях: - Назначения имеют большой размер (например, постквантовые ключи) - Аутентификация происходит на другом уровне - Критична эффективность использования пропускной способности

### 10.6 Целостность данных

Целостность датаграммы защищена **контрольной суммой gzip CRC-32** на уровне I2CP. Явное поле контрольной суммы в самом формате полезной нагрузки датаграммы отсутствует.

### 10.7 Инкапсуляция пакетов

Каждая датаграмма инкапсулируется как одно I2NP-сообщение или как отдельный clove в **Garlic Message**. Уровни I2CP, I2NP и туннеля обрабатывают длину и фрейминг — во внутреннем протоколе датаграмм нет разделителей или полей длины.

### 10.8 Соображения о постквантовой (PQ) безопасности

Если будет реализовано **Предложение 169** (подписи ML-DSA), размеры подписей и destination (адресов назначения) резко возрастут — с ~455 байт до **≥3739 байт**. Это изменение существенно увеличит служебные данные дейтаграмм и уменьшит эффективную ёмкость полезной нагрузки.

**Datagram3**, который основан на аутентификации на уровне сессии (не встроенных подписях), вероятно, станет предпочтительным решением в постквантовых средах I2P.

---

## 11. Ссылки

- [Предложение 163 – Datagram2 и Datagram3](/proposals/163-datagram2/)
- [Предложение 160 – Интеграция UDP Tracker](/proposals/160-udp-trackers/)
- [Предложение 144 – Расчёты MTU для Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Предложение 169 – Постквантовые подписи](/proposals/169-pq-crypto/)
- [Спецификация I2CP](/docs/specs/i2cp/)
- [Спецификация I2NP](/docs/specs/i2np/)
- [Спецификация сообщений tunnel](/docs/specs/implementation/)
- [Спецификация SAM v3](/docs/api/samv3/)
- [Документация i2ptunnel](/docs/api/i2ptunnel/)

## 12. Основные изменения (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Резюме

Подсистема датаграмм теперь поддерживает четыре варианта протокола, предлагающих спектр от полностью аутентифицированной до облегченной сырой передачи. Разработчикам следует переходить на **Datagram2** для критичных к безопасности случаев использования и **Datagram3** для эффективного трафика с возможностью ответа. Все старые типы остаются совместимыми для обеспечения долгосрочной интероперабельности.
