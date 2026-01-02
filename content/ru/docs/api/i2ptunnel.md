---
title: "I2PTunnel"
description: "Инструмент для взаимодействия с I2P и предоставления сервисов в сети"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

I2PTunnel — это основной компонент I2P для взаимодействия с сетью I2P и предоставления сервисов в ней. Он позволяет приложениям на основе TCP и потоковой передачи медиа работать анонимно через абстракцию tunnel. Назначение tunnel может быть определено через [имя хоста](/docs/overview/naming), [Base32](/docs/overview/naming#base32) или полный ключ destination.

Каждый установленный tunnel прослушивает локально (например, `localhost:port`) и подключается внутренне к I2P-адресатам. Для размещения сервиса создайте tunnel, указывающий на нужный IP-адрес и порт. Генерируется соответствующий ключ I2P destination, позволяющий сервису стать глобально доступным в сети I2P. Веб-интерфейс I2PTunnel доступен по адресу [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Службы по умолчанию

### Серверный туннель

- **I2P Webserver** – Tunnel к веб-серверу Jetty на [localhost:7658](http://localhost:7658) для удобного хостинга в I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Клиентские туннели

- **I2P HTTP Proxy** – `localhost:4444` – Используется для просмотра I2P и Интернета через outproxy-серверы.  
- **I2P HTTPS Proxy** – `localhost:4445` – Защищённый вариант HTTP proxy.  
- **Irc2P** – `localhost:6668` – Tunnel по умолчанию для анонимной IRC-сети.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Клиентский tunnel для SSH-доступа к репозиториям.  
- **Postman SMTP** – `localhost:7659` – Клиентский tunnel для исходящей почты.  
- **Postman POP3** – `localhost:7660` – Клиентский tunnel для входящей почты.

> Примечание: Только веб-сервер I2P является **server tunnel** по умолчанию; все остальные являются клиентскими туннелями, подключающимися к внешним сервисам I2P.

---

## Конфигурация

Спецификация конфигурации I2PTunnel задокументирована на странице [/spec/configuration](/docs/specs/configuration/).

---

## Режимы клиента

### Стандартный

Открывает локальный TCP-порт, который подключается к службе на I2P destination. Поддерживает несколько записей destination, разделенных запятыми, для обеспечения избыточности.

### HTTP

Прокси-туннель для HTTP/HTTPS запросов. Поддерживает локальные и удаленные outproxy, удаление заголовков, кэширование, аутентификацию и прозрачное сжатие.

**Защита конфиденциальности:**   - Удаляет заголовки: `Accept-*`, `Referer`, `Via`, `From`   - Заменяет заголовки хоста на Base32 назначения   - Обеспечивает RFC-совместимое удаление hop-by-hop заголовков   - Добавляет поддержку прозрачной декомпрессии   - Предоставляет внутренние страницы ошибок и локализованные ответы

**Поведение сжатия:**   - Запросы могут использовать пользовательский заголовок `X-Accept-Encoding: x-i2p-gzip`   - Ответы с `Content-Encoding: x-i2p-gzip` автоматически распаковываются   - Сжатие оценивается по типу MIME и длине ответа для повышения эффективности

**Постоянные соединения (новое с версии 2.5.0):**   HTTP Keepalive и постоянные соединения теперь поддерживаются для сервисов, размещённых в I2P, через Hidden Services Manager. Это снижает задержки и накладные расходы на соединения, но пока не обеспечивает полную совместимость с RFC 2616 для постоянных сокетов на всех hop'ах (участках маршрута).

**Pipelining:**   Остается неподдерживаемым и ненужным; современные браузеры отказались от этой функции.

**Поведение User-Agent:**   - **Outproxy:** Использует актуальный User-Agent Firefox ESR.   - **Внутренний:** `MYOB/6.66 (AN/ON)` для согласованности анонимности.

### IRC-клиент

Подключается к IRC-серверам на базе I2P. Разрешает безопасное подмножество команд, фильтруя идентификаторы для обеспечения конфиденциальности.

### SOCKS 4/4a/5

Предоставляет возможность SOCKS-прокси для TCP-соединений. UDP остается нереализованным в Java I2P (только в i2pd).

### CONNECT

Реализует HTTP-туннелирование `CONNECT` для SSL/TLS-соединений.

### Streamr

Обеспечивает потоковую передачу в стиле UDP через инкапсуляцию на основе TCP. Поддерживает потоковую передачу медиа при работе с соответствующим серверным tunnel Streamr.

![Диаграмма I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Режимы сервера

### Стандартный сервер

Создает TCP-destination, сопоставленный с локальным IP:портом.

### HTTP-сервер

Создает destination, который взаимодействует с локальным веб-сервером. Поддерживает сжатие (`x-i2p-gzip`), удаление заголовков и защиту от DDoS-атак. Теперь включает **поддержку постоянных соединений** (v2.5.0+) и **оптимизацию пула потоков** (v2.7.0–2.9.0).

### HTTP двунаправленный

**Устарел** – Всё ещё функционален, но не рекомендуется к использованию. Работает одновременно как HTTP-сервер и клиент без outproxy. Используется в основном для диагностических тестов с петлёй обратной связи.

### IRC-сервер

Создает отфильтрованное назначение для IRC-сервисов, передавая ключи клиентских назначений в качестве имен хостов.

### Streamr Server

Сочетается с клиентским туннелем Streamr для обработки потоков данных в стиле UDP через I2P.

---

## Новые функции (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Функции безопасности

- **Удаление заголовков** для анонимности (Accept, Referer, From, Via)
- **Рандомизация User-Agent** в зависимости от in/outproxy
- **Ограничение частоты POST-запросов** и **защита от Slowloris**
- **Регулирование соединений** в подсистемах потоковой передачи
- **Обработка перегрузки сети** на уровне tunnel
- **Изоляция NetDB** для предотвращения утечек между приложениями

---

## Технические детали

- Размер ключа назначения по умолчанию: 516 байт (может быть больше для расширенных сертификатов LS2)  
- Base32 адреса: `{52–56+ символов}.b32.i2p`  
- Серверные туннели остаются совместимыми как с Java I2P, так и с i2pd  
- Устаревшая функция: только `httpbidirserver`; удалений с версии 0.9.59 не было  
- Проверены корректные порты по умолчанию и корневые директории документов для всех платформ

---

## Резюме

I2PTunnel остаётся основой интеграции приложений с I2P. Между версиями 0.9.59 и 2.10.0 он получил поддержку постоянных соединений, постквантовое шифрование и значительные улучшения многопоточности. Большинство конфигураций остаются совместимыми, но разработчикам следует проверить свои настройки для соответствия современным транспортным параметрам и настройкам безопасности по умолчанию.
