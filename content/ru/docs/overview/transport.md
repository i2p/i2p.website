---
title: "Транспортный уровень"
description: "Понимание транспортного уровня I2P - методы связи «точка-точка» между routers, включая NTCP2 и SSU2"
slug: "transport"
lastUpdated: "2025-03"
accurateFor: "2.10.0"
---

---

## 1. Обзор

**Транспорт** в I2P — это способ прямой связи между routers по схеме точка‑к‑точке. Эти механизмы обеспечивают конфиденциальность и целостность, одновременно выполняя проверку аутентификации router.

Каждый транспорт работает на основе моделей соединений с поддержкой аутентификации, управления потоком, подтверждений и повторной передачи.

---

## 2. Текущие транспорты

В настоящее время I2P поддерживает два основных транспортных протокола:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport with modern encryption (as of 0.9.36)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Secure Semireliable UDP with modern encryption (as of 0.9.56)</td>
    </tr>
  </tbody>
</table>
### 2.1 Устаревшие транспортные протоколы (не рекомендуется к использованию)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by NTCP2; removed in 0.9.62</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced by SSU2; removed in 0.9.62</td>
    </tr>
  </tbody>
</table>
---

## 3. Транспортные службы

Транспортная подсистема предоставляет следующие службы:

### 3.1 Доставка сообщений

- Надёжная доставка сообщений [I2NP](/docs/specs/i2np/) (транспортные протоколы обрабатывают исключительно обмен сообщениями I2NP)
- Доставка в порядке отправки **НЕ гарантируется** в общем случае
- Очередь сообщений на основе приоритетов

### 3.2 Управление соединениями

- Установление и завершение соединений
- Управление лимитами соединений с принудительным соблюдением пороговых значений
- Отслеживание состояния по каждому пиру
- Автоматическое и ручное применение черного списка пиров

### 3.3 Конфигурация сети

- Несколько адресов router для каждого транспорта (поддержка IPv4 и IPv6 начиная с v0.9.8)
- Открытие портов брандмауэра через UPnP
- Поддержка обхода NAT/брандмауэра
- Определение локального IP-адреса несколькими методами

### 3.4 Безопасность

- Шифрование для обменов точка-точка
- Проверка IP-адреса по локальным правилам
- Определение консенсуса времени (резерв через NTP)

### 3.5 Управление пропускной способностью

- Ограничения пропускной способности для входящего и исходящего трафика
- Выбор оптимального транспорта для исходящих сообщений

---

## 4. Транспортные адреса

Подсистема ведёт список точек контакта router:

- Тип транспорта (NTCP2, SSU2)
- IP-адрес
- Номер порта
- Необязательные параметры

Возможны несколько адресов для каждого транспорта.

### 4.1 Распространённые конфигурации адресов

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Configuration</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Hidden</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers with no published addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Firewalled</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers publishing SSU2 addresses with "introducer" peer lists for NAT traversal</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Unrestricted</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Routers advertising both NTCP2 and SSU2 addresses on IPv4 and/or IPv6</td>
    </tr>
  </tbody>
</table>
---

## 5. Выбор транспорта

Система выбирает транспорты для [сообщений I2NP](/docs/specs/i2np/) независимо от протоколов верхнего уровня. Выбор осуществляется с помощью **системы торгов**, в которой каждый транспорт подает ставки, и побеждает ставка с наименьшим значением.

### 5.1 Факторы определения ставки

- Настройки предпочтений транспорта
- Существующие соединения с пирами
- Текущее и пороговое количество соединений
- История недавних попыток соединения
- Ограничения на размер сообщений
- Транспортные возможности RouterInfo (информация о router) пира
- Прямота соединения (прямое или через introducer (узел-посредник в SSU))
- Объявленные пиром предпочтения транспорта

Обычно два router одновременно поддерживают соединения по одному транспорту, хотя возможны одновременные соединения по нескольким транспортам.

---

## 6. NTCP2

**NTCP2** (New Transport Protocol 2) — современный транспорт на базе TCP для I2P, представленный в версии 0.9.36.

### 6.1 Ключевые возможности

- Основано на **Noise Protocol Framework** (паттерн Noise_XK)
- Использует **X25519** для обмена ключами
- Использует **ChaCha20/Poly1305** для аутентифицированного шифрования
- Использует **BLAKE2s** для хеширования
- Обфускация протокола для противодействия DPI (глубокая инспекция пакетов)
- Необязательное заполнение для устойчивости к анализу трафика

### 6.2 Установление соединения

1. **Запрос сеанса** (Alice → Bob): Эфемерный ключ X25519 + зашифрованная полезная нагрузка
2. **Сеанс создан** (Bob → Alice): Эфемерный ключ + зашифрованное подтверждение
3. **Сеанс подтверждён** (Alice → Bob): Завершающее рукопожатие с RouterInfo (информация о Router)

Все последующие данные шифруются сеансовыми ключами, выведенными из рукопожатия.

Подробности см. в [спецификации NTCP2](/docs/specs/ntcp2/).

---

## 7. SSU2

**SSU2** (Secure Semireliable UDP 2 — защищённый полунадёжный UDP 2) — современный транспорт на основе UDP для I2P, представленный в версии 0.9.56.

### 7.1 Ключевые особенности

- Основан на **Noise Protocol Framework** (фреймворк протокола Noise; шаблон Noise_XK)
- Использует **X25519** для обмена ключами
- Использует **ChaCha20/Poly1305** для аутентифицированного шифрования
- Частично надёжная доставка с выборочными подтверждениями
- Обход NAT посредством hole punching (пробивание) и ретрансляции/введения
- Поддержка миграции соединения
- Обнаружение MTU на пути

### 7.2 Преимущества по сравнению с SSU (устаревшим)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU (Legacy)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">SSU2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 + ChaCha20/Poly1305</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Header encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partial</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (ChaCha20)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fixed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted, rotatable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NAT traversal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Basic introduction</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced hole punching + relay</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Obfuscation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Minimal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved (variable padding)</td>
    </tr>
  </tbody>
</table>
Подробности см. в [спецификации SSU2](/docs/specs/ssu2/).

---

## 8. Обход NAT

Оба транспорта поддерживают обход NAT, чтобы routers, находящиеся за межсетевым экраном, могли участвовать в сети.

### 8.1 Введение в SSU2

Когда router не может напрямую принимать входящие соединения:

1. router публикует адреса **introducer** (узел‑посредник для обхода NAT) в своем RouterInfo
2. Подключающийся пир отправляет запрос на представление в адрес introducer
3. Introducer пересылает информацию для соединения router за файрволом
4. Router за файрволом инициирует исходящее соединение (NAT-пробивка (hole punching))
5. Установлена прямая связь

### 8.2 NTCP2 и межсетевые экраны

NTCP2 требует доступности входящих соединений по TCP. Routers, находящиеся за NAT, могут:

- Использовать UPnP для автоматического открытия портов
- Вручную настроить проброс портов
- Полагаться на SSU2 для входящих соединений, а для исходящих использовать NTCP2

---

## 9. Обфускация протокола

Оба современных транспортных протокола включают возможности маскировки:

- **Случайное заполнение** в сообщениях рукопожатия
- **Зашифрованные заголовки**, не раскрывающие сигнатуры протокола
- **Сообщения переменной длины** для противодействия анализу трафика
- **Отсутствие фиксированных шаблонов** при установлении соединения

> **Примечание**: Обфускация на транспортном уровне дополняет, но не заменяет анонимность, обеспечиваемую архитектурой tunnel I2P.

---

## 10. Дальнейшее развитие

Планируемые исследования и улучшения включают:

- **Подключаемые транспорты** – совместимые с Tor плагины маскировки
- **Транспорт на основе QUIC** – исследование преимуществ протокола QUIC
- **Оптимизация лимита соединений** – исследование оптимальных лимитов соединений с пирами
- **Расширенные стратегии padding (добавочного трафика)** – улучшенная устойчивость к анализу трафика

---

## 11. Ссылки

- [Спецификация NTCP2](/docs/specs/ntcp2/) – TCP-транспорт на основе Noise
- [Спецификация SSU2](/docs/specs/ssu2/) – Безопасный полунадежный UDP 2
- [Спецификация I2NP](/docs/specs/i2np/) – Сообщения протокола I2NP
- [Общие структуры](/docs/specs/common-structures/) – RouterInfo и структуры адресов
- [Историческое обсуждение NTCP](/docs/ntcp/) – История разработки устаревшего транспорта
- [Устаревшая документация по SSU](/docs/legacy/ssu/) – Исходная спецификация SSU (устарело)
