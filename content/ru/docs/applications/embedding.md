---
title: "Встраивание I2P в ваше приложение"
description: "Обновленное практическое руководство по ответственной интеграции I2P router в ваше приложение"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Встраивание I2P в ваше приложение — мощный способ привлечь пользователей, но только если router настроен ответственно.

## 1. Координация с командами разработчиков роутеров

- Свяжитесь с разработчиками **Java I2P** и **i2pd** перед интеграцией. Они могут проверить ваши настройки по умолчанию и указать на проблемы совместимости.
- Выберите реализацию router, которая подходит для вашего стека:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Другие языки** → интегрируйте router и подключайтесь через [SAM v3](/docs/api/samv3/) или [I2CP](/docs/specs/i2cp/)
- Проверьте условия распространения для бинарных файлов router и зависимостей (среда выполнения Java, ICU и т.д.).

## 2. Рекомендуемые значения конфигурации по умолчанию

Стремитесь «вносить больше вклада, чем потреблять». Современные настройки по умолчанию приоритизируют здоровье и стабильность сети.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Участвующие туннели остаются важными

**Не** отключайте участие в туннелях.

1. Роутеры, которые не ретранслируют трафик, работают хуже сами.
2. Сеть зависит от добровольного предоставления пропускной способности.
3. Маскирующий трафик (ретранслируемый трафик) улучшает анонимность.

**Официальные минимумы:** - Общая пропускная способность: ≥ 12 КБ/с   - Автоматическое включение floodfill: ≥ 128 КБ/с   - Рекомендуется: 2 входящих / 2 исходящих tunnel (значение по умолчанию в Java I2P)

## 3. Постоянство и пересев (reseeding)

Директории постоянного состояния (`netDb/`, профили, сертификаты) должны сохраняться между запусками.

Без сохранения состояния ваши пользователи будут запускать reseed при каждом старте — что ухудшит производительность и увеличит нагрузку на reseed-серверы.

Если сохранение данных невозможно (например, контейнеры или временные установки):

1. Включите **1 000–2 000 router info** в установщик.  
2. Используйте один или несколько собственных reseed-серверов, чтобы снизить нагрузку на публичные.

Конфигурационные переменные: - Базовая директория: `i2p.dir.base` - Директория конфигурации: `i2p.dir.config` - Включает `certificates/` для reseed (повторного заполнения базы данных сети).

## 4. Безопасность и уязвимости

- Держите консоль router (`127.0.0.1:7657`) только для локального доступа.
- Используйте HTTPS при внешнем доступе к интерфейсу.
- Отключите внешние SAM/I2CP, если они не требуются.
- Проверьте включенные плагины — поставляйте только те, которые поддерживает ваше приложение.
- Всегда включайте аутентификацию для удаленного доступа к консоли.

**Функции безопасности, представленные начиная с версии 2.5.0:** - Изоляция NetDB между приложениями (2.4.0+)   - Защита от DoS-атак и блок-листы Tor (2.5.1)   - Устойчивость NTCP2 к зондированию (2.9.0)   - Улучшения в выборе floodfill-роутеров (2.6.0+)

## 5. Поддерживаемые API (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Вся официальная документация находится в `/docs/api/` — старый путь `/spec/samv3/` **не существует**.

## 6. Сеть и порты

Типичные порты по умолчанию: - 4444 – HTTP прокси   - 4445 – HTTPS прокси   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Консоль роутера   - 7658 – Локальный I2P сайт   - 6668 – IRC прокси   - 9000–31000 – Случайный порт роутера (UDP/TCP входящий)

Маршрутизаторы выбирают случайный входящий порт при первом запуске. Проброс портов улучшает производительность, но UPnP может обработать это автоматически.

## 7. Современные изменения (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Пользовательский опыт и тестирование

- Объяснить, что делает I2P и почему пропускная способность является общим ресурсом.
- Предоставить диагностику router (пропускная способность, tunnel, статус reseed).
- Протестировать сборки на Windows, macOS и Linux (включая системы с малым объемом RAM).
- Проверить совместимость с узлами **Java I2P** и **i2pd**.
- Протестировать восстановление после обрывов сети и некорректных завершений работы.

## 9. Ресурсы сообщества

- Форум: [i2pforum.net](https://i2pforum.net) или `http://i2pforum.i2p` внутри I2P.  
- Код: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (сеть Irc2P): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` не подтверждён; возможно, не существует.  
  - Уточните, какая сеть (Irc2P или ilita.i2p) размещает ваш канал.

Ответственное встраивание означает баланс между пользовательским опытом, производительностью и вкладом в сеть. Используйте эти настройки по умолчанию, поддерживайте синхронизацию с разработчиками router и тестируйте под реальной нагрузкой перед релизом.
