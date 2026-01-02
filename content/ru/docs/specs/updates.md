---
title: "Спецификация обновления программного обеспечения"
description: "Безопасный механизм подписанных обновлений и структура канала обновлений для I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Обзор

Routers автоматически проверяют наличие обновлений, опрашивая подписанную ленту новостей, распространяемую через сеть I2P. Когда анонсируется более новая версия, router загружает криптографически подписанный архив обновления (`.su3`) и подготавливает его к установке.   Эта система обеспечивает **аутентифицированное, защищённое от подмены** и **многоканальное** распространение официальных релизов.

Начиная с I2P 2.10.0, система обновлений использует:
- подписи **RSA-4096 / SHA-512**
- **формат контейнера SU3** (вместо устаревших SUD/SU2)
- **Избыточные зеркала:** HTTP в сети I2P, HTTPS в клирнете и BitTorrent

---

## 1. Лента новостей

Routers опрашивают подписанную ленту Atom каждые несколько часов, чтобы обнаруживать новые версии и уведомления о безопасности.   Лента подписывается и распространяется в виде файла `.su3`, который может включать:

- `<i2p:version>` — номер новой версии  
- `<i2p:minVersion>` — минимально поддерживаемая версия router  
- `<i2p:minJavaVersion>` — требуемая минимальная среда выполнения Java  
- `<i2p:update>` — перечисляет несколько зеркал загрузки (I2P, HTTPS, торрент)  
- `<i2p:revocations>` — данные об отзыве сертификатов  
- `<i2p:blocklist>` — блок-листы на уровне сети для скомпрометированных пиров

### Распространение ленты

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers предпочитают I2P‑фид, но при необходимости могут переключиться на clearnet (открытый интернет) или торрент-распространение.

---

## 2. Форматы файлов

### SU3 (Текущий стандарт)

Начиная с версии 0.9.9, SU3 заменил устаревшие форматы SUD и SU2.   Каждый файл содержит заголовок, полезную нагрузку и завершающую подпись.

**Структура заголовка** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Шаги проверки подписи** 1. Разберите заголовок и определите алгоритм подписи.   2. Проверьте хэш и подпись, используя сохранённый сертификат подписанта.   3. Убедитесь, что сертификат подписанта не отозван.   4. Сравните встроенную строку версии с метаданными полезной нагрузки.

Routers поставляются с сертификатами доверенных подписантов (в настоящее время — **zzz** и **str4d**) и отклоняют любые неподписанные или отозванные источники.

### SU2 (устарело)

- Использовалось расширение `.su2` для JAR-файлов, сжатых с помощью Pack200.  
- Удалено после того, как в Java 14 Pack200 был объявлен устаревшим (JEP 367).  
- Отключено в I2P 0.9.48+; теперь полностью заменено ZIP-сжатием.

### SUD (устаревшее)

- Ранний формат ZIP с подписью DSA-SHA1 (до 0.9.9).  
- Нет идентификатора подписанта или заголовка, ограниченная защита целостности.  
- Заменён из-за слабой криптографии и отсутствия принудительного контроля версий.

---

## 3. Рабочий процесс обновления

### 3.1 Проверка заголовка

Routers получают только **SU3 header** (заголовок SU3) для проверки строки версии перед загрузкой полных файлов.   Это позволяет избежать напрасной траты пропускной способности на устаревшие зеркала или версии.

### 3.2 Полная загрузка

После проверки заголовка, router загружает полный файл `.su3` с: - Внутрисетевые зеркала eepsite (предпочтительно)   - HTTPS зеркала clearnet (обычный интернет) (резервный вариант)   - BitTorrent (необязательное распространение при участии пиров)

Для загрузок используются стандартные HTTP‑клиенты I2PTunnel с повторными попытками, обработкой таймаутов и переключением на зеркала.

### 3.3 Проверка подписи

Каждый загруженный файл проходит: - **Проверка подписи:** верификация RSA-4096/SHA512   - **Сопоставление версий:** проверка соответствия версий заголовка и полезной нагрузки   - **Предотвращение понижения версии:** гарантирует, что обновление новее установленной версии

Некорректные или несовпадающие файлы немедленно отбрасываются.

### 3.4 Подготовка к установке

После проверки: 1. Извлеките содержимое ZIP во временный каталог   2. Удалите файлы, перечисленные в `deletelist.txt`   3. Замените нативные библиотеки, если включён `lib/jbigi.jar`   4. Скопируйте сертификаты подписанта в `~/.i2p/certificates/`   5. Переместите обновление в `i2pupdate.zip` для применения при следующем перезапуске

Обновление устанавливается автоматически при следующем запуске или при ручном запуске «Install update now».

---

## 4. Управление файлами

### deletelist.txt

Текстовый список устаревших файлов, которые нужно удалить перед распаковкой нового содержимого.

**Правила:** - Один путь на строку (только относительные пути) - Строки, начинающиеся с `#`, игнорируются - `..` и абсолютные пути отклоняются

### Нативные библиотеки

Чтобы избежать использования устаревших или несовместимых нативных бинарных файлов: - Если `lib/jbigi.jar` существует, старые файлы `.so` или `.dll` удаляются   - Обеспечивается повторное извлечение библиотек, зависящих от платформы

---

## 5. Управление сертификатами

Routers могут получать **новые сертификаты подписанта** посредством обновлений или аннулирований в ленте новостей.

- Новые файлы `.crt` копируются в каталог сертификатов.  
- Отозванные сертификаты удаляются перед последующими проверками.  
- Поддерживает ротацию ключей без необходимости ручного вмешательства пользователя.

Все обновления подписываются в автономном режиме с использованием **air-gapped signing systems** (систем подписания, изолированных от сети).   Закрытые ключи никогда не хранятся на серверах сборки.

---

## 6. Рекомендации для разработчиков

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
В будущих релизах будут изучаться вопросы интеграции постквантовых подписей (см. Proposal 169) и реализации воспроизводимых сборок.

---

## 7. Обзор безопасности

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Версионирование

- Router: **2.10.0 (API 0.9.67)**  
- Семантическое версионирование с `Major.Minor.Patch`.  
- Принудительное соблюдение минимальной версии предотвращает небезопасные обновления.  
- Поддерживаемые версии Java: **Java 8–17**. В будущих версиях 2.11.0+ потребуется Java 17+.

---
