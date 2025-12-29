---
title: "Протокол потоковой передачи"
description: "Надежный, похожий на TCP транспорт, используемый большинством приложений I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Обзор

I2P Streaming Library (библиотека потоковой передачи данных I2P) обеспечивает надёжную, упорядоченную и аутентифицированную доставку данных поверх ненадёжного уровня сообщений I2P — аналогично TCP поверх IP. Её используют почти все интерактивные приложения I2P, такие как просмотр веб‑страниц, IRC, электронная почта и обмен файлами.

Он обеспечивает надежную передачу данных, контроль перегрузок, ретрансляцию и управление потоком поверх анонимных tunnels I2P с высокой задержкой. Каждый поток полностью зашифрован от конца до конца между назначениями.

---

## Основные принципы проектирования

Стриминговая библиотека реализует **однофазную установку соединения**, при которой флаги SYN, ACK и FIN могут нести полезную нагрузку в том же сообщении. Это минимизирует число обменов туда‑обратно в средах с высокой задержкой — небольшая HTTP‑транзакция может завершиться за один обмен.

Контроль перегрузки и повторная передача смоделированы по образцу TCP, но адаптированы к среде I2P. Размеры окна основаны на сообщениях, а не на байтах, и подстроены под задержки и накладные расходы tunnel. Протокол поддерживает медленный старт, предотвращение перегрузок и экспоненциальное увеличение интервала ожидания, аналогичные алгоритму AIMD в TCP.

---

## Архитектура

Потоковая библиотека работает между приложениями и интерфейсом I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
Большинство пользователей получают доступ к нему через I2PSocketManager, I2PTunnel или SAMv3. Библиотека прозрачно обрабатывает управление destination (адресом назначения в I2P), работу с tunnel и повторные передачи.

---

## Формат пакета

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Сведения о заголовке

- **Идентификаторы потоков**: 32-битные значения, однозначно идентифицирующие локальные и удаленные потоки.
- **Порядковый номер**: начинается с 0 для SYN (сегмента инициации соединения), увеличивается на 1 для каждого сообщения.
- **Подтверждение до (Ack Through)**: подтверждает все сообщения до N, за исключением находящихся в списке NACK (отрицательных подтверждений).
- **Флаги**: битовая маска, управляющая состоянием и поведением.
- **Параметры**: список переменной длины для RTT (время туда-обратно), MTU (максимальная передаваемая единица) и согласования протокола.

### Ключевые флаги

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Управление потоком и надёжность

Streaming (библиотека потоковой передачи данных в I2P) использует **оконный механизм на основе сообщений**, в отличие от байтово-ориентированного подхода TCP. Количество неподтверждённых пакетов, разрешённых в полёте, равно текущему размеру окна (по умолчанию 128).

### Механизмы

- **Контроль перегрузки:** Медленный старт и предотвращение перегрузки на основе AIMD (аддитивное увеличение/мультипликативное уменьшение).  
- **Choke/Unchoke (блокировка/разблокировка передачи):** Сигнализация управления потоком на основе заполненности буфера.  
- **Повторная передача:** Расчет RTO (таймаута повторной передачи) согласно RFC 6298 с экспоненциальным увеличением интервала.  
- **Фильтрация дубликатов:** Обеспечивает надежность при возможном переупорядочивании сообщений.

Типичные значения конфигурации:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Установление соединения

1. **Инициатор** отправляет SYN (необязательно с полезной нагрузкой и FROM_INCLUDED).  
2. **Ответчик** отвечает SYN+ACK (может включать полезную нагрузку).  
3. **Инициатор** отправляет финальный ACK, подтверждающий установление соединения.

Необязательные начальные полезные нагрузки позволяют передавать данные до завершения полного рукопожатия.

---

## Подробности реализации

### Повторная передача и таймаут

Алгоритм повторной передачи соответствует **RFC 6298**.   - **Начальный RTO (тайм-аут повторной передачи):** 9 с   - **Минимальный RTO:** 100 мс   - **Максимальный RTO:** 45 с   - **Альфа:** 0.125   - **Бета:** 0.25

### Совместное использование блока управления

Недавние соединения с тем же пиром повторно используют прежние данные RTT (время кругового прохода) и окна для более быстрого разгона, избегая задержки “холодного старта”. Контрольные блоки истекают через несколько минут.

### MTU и фрагментация

- MTU по умолчанию: **1730 байт** (вмещает два сообщения I2NP).  
- ECIES destinations (тип назначения в I2P на основе ECIES): **1812 байт** (сниженные накладные расходы).  
- Минимально поддерживаемый MTU: 512 байт.

Размер полезной нагрузки не включает минимальный 22-байтовый заголовок Streaming (библиотека потоковой передачи I2P).

---

## История версий

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Использование на уровне приложений

### Пример на Java

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Поддержка SAMv3 и i2pd

- **SAMv3**: Предоставляет режимы STREAM и DATAGRAM для клиентов, не использующих Java.  
- **i2pd**: Предоставляет идентичные параметры потоковой передачи через опции файла конфигурации (например, `i2p.streaming.maxWindowSize`, `profile`, и т. д.).

---

## Выбор между потоковой передачей и дейтаграммами

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Безопасность и постквантовое будущее

Сеансы библиотеки Streaming защищены сквозным шифрованием на уровне I2CP. Постквантовое гибридное шифрование (ML-KEM + X25519) поддерживается экспериментально в версии 2.10.0, но по умолчанию отключено.

---

## Ссылки

- [Обзор Streaming API](/docs/specs/streaming/)  
- [Спецификация протокола Streaming (потоковый протокол)](/docs/specs/streaming/)  
- [Спецификация I2CP](/docs/specs/i2cp/)  
- [Предложение 144: расчёты MTU для Streaming](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Примечания к выпуску I2P 2.10.0](/ru/blog/2025/09/08/i2p-2.10.0-release/)
