---
title: "SOCKS-прокси"
description: "Безопасное использование SOCKS-туннеля I2P (обновлено для версии 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Внимание:** SOCKS-туннель передает данные приложений без их санитарной обработки. Многие протоколы раскрывают IP-адреса, имена хостов или другие идентификаторы. Используйте SOCKS только с программным обеспечением, которое вы проверили на предмет анонимности.

---

## 1. Обзор

I2P предоставляет поддержку прокси **SOCKS 4, 4a и 5** для исходящих соединений через **I2PTunnel клиент**. Это позволяет стандартным приложениям обращаться к I2P-адресатам, но **не может получить доступ к clearnet** (обычному интернету). **SOCKS outproxy отсутствует**, и весь трафик остается внутри сети I2P.

### Краткое описание реализации

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Поддерживаемые типы адресов:** - доменные имена `.i2p` (записи адресной книги) - Base32 хеши (`.b32.i2p`) - Base64 и обычная сеть не поддерживаются

---

## 2. Риски безопасности и ограничения

### Утечка на уровне приложения

SOCKS работает ниже прикладного уровня и не может очищать протоколы. Многие клиенты (например, браузеры, IRC, электронная почта) включают метаданные, которые раскрывают ваш IP-адрес, имя хоста или сведения о системе.

Распространённые утечки включают: - IP-адреса в заголовках почты или CTCP-ответах IRC   - Настоящие имена/имена пользователей в данных протокола   - Строки user-agent с отпечатками ОС   - Внешние DNS-запросы   - WebRTC и телеметрия браузера

**I2P не может предотвратить эти утечки** — они происходят выше уровня tunnel. Используйте SOCKS только для **проверенных клиентов**, разработанных с учетом анонимности.

### Общая идентичность туннеля

Если несколько приложений используют один SOCKS tunnel, они разделяют одну и ту же идентичность I2P destination. Это позволяет проводить корреляцию или снятие цифровых отпечатков между различными сервисами.

**Меры противодействия:** Используйте **неразделяемые tunnel** для каждого приложения и включите **постоянные ключи**, чтобы поддерживать согласованные криптографические идентификаторы при перезапусках.

### Режим UDP заглушен

Поддержка UDP в SOCKS5 не реализована. Протокол объявляет о возможности UDP, но вызовы игнорируются. Используйте клиенты только с TCP.

### Отсутствие Outproxy по дизайну

В отличие от Tor, I2P **не** предоставляет SOCKS-based прокси для выхода в clearnet (обычный интернет). Попытки подключиться к внешним IP-адресам завершатся неудачей или раскроют вашу личность. Если требуется выход в обычный интернет, используйте HTTP или HTTPS прокси.

---

## 3. Исторический контекст

Разработчики давно не рекомендуют использовать SOCKS для анонимного использования. Из внутренних обсуждений разработчиков и встреч 2004 года [Meeting 81](/ru/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) и [Meeting 82](/ru/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> "Пересылка произвольного трафика небезопасна, и нам как разработчикам программного обеспечения для анонимности следует в первую очередь заботиться о безопасности наших конечных пользователей."

Поддержка SOCKS была включена для совместимости, но не рекомендуется для производственных сред. Практически каждое интернет-приложение пропускает конфиденциальные метаданные, непригодные для анонимной маршрутизации.

---

## 4. Конфигурация

### Java I2P

1. Откройте [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Создайте новый клиентский tunnel типа **"SOCKS 4/4a/5"**  
3. Настройте параметры:  
   - Локальный порт (любой доступный)  
   - Shared client: *отключите* для отдельной идентичности каждого приложения  
   - Persistent key: *включите* для уменьшения корреляции ключей  
4. Запустите tunnel

### i2pd

i2pd включает поддержку SOCKS5, включенную по умолчанию на `127.0.0.1:4447`. Конфигурация в `i2pd.conf` в разделе `[SOCKSProxy]` позволяет настроить порт, хост и параметры tunnel.

---

## 5. График разработки

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
Сам модуль SOCKS не получал значительных обновлений протокола с 2013 года, но окружающий стек туннелей получил улучшения производительности и криптографии.

---

## 6. Рекомендуемые альтернативы

Для любого **производственного**, **публичного** или **критически важного для безопасности** приложения используйте один из официальных I2P API вместо SOCKS:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Эти API обеспечивают надлежащую изоляцию точек назначения, управление криптографическими идентификаторами и повышенную производительность маршрутизации.

---

## 7. OnionCat / GarliCat

OnionCat поддерживает I2P через режим GarliCat (диапазон IPv6 `fd60:db4d:ddb5::/48`). До сих пор функционирует, но с ограниченной разработкой с 2019 года.

**Ограничения использования:** - Требует ручной настройки `.oc.b32.i2p` в SusiDNS   - Необходимо статическое назначение IPv6   - Официально не поддерживается проектом I2P

Рекомендуется только для продвинутых настроек VPN поверх I2P.

---

## 8. Лучшие практики

Если необходимо использовать SOCKS: 1. Создавайте отдельные туннели для каждого приложения. 2. Отключайте режим общего клиента. 3. Включайте постоянные ключи. 4. Принудительно используйте разрешение DNS через SOCKS5. 5. Проверяйте поведение протокола на предмет утечек. 6. Избегайте соединений с обычной сетью. 7. Отслеживайте сетевой трафик на предмет утечек.

---

## 9. Техническое резюме

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Заключение

SOCKS-прокси в I2P обеспечивает базовую совместимость с существующими TCP-приложениями, но **не предназначен для обеспечения строгих гарантий анонимности**. Его следует использовать только в контролируемых, проверенных тестовых средах.

> Для серьезных развертываний переходите на **SAM v3** или **Streaming API**. Эти API изолируют идентификаторы приложений, используют современную криптографию и получают постоянную поддержку разработки.

---

### Дополнительные ресурсы

- [Официальная документация SOCKS](/docs/api/socks/)  
- [Спецификация SAM v3](/docs/api/samv3/)  
- [Документация библиотеки Streaming](/docs/specs/streaming/)  
- [Справочник I2PTunnel](/docs/specs/implementation/)  
- [Документация для разработчиков I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Форум сообщества](https://i2pforum.net)
