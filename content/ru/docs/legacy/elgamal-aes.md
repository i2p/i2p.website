---
title: "Шифрование ElGamal/AES + SessionTag (метка сессии)"
description: "Устаревшее сквозное шифрование, сочетающее ElGamal, AES, SHA-256 и одноразовые сеансовые теги"
slug: "elgamal-aes"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Статус:** В этом документе описан устаревший протокол шифрования ElGamal/AES+SessionTag. Он поддерживается только для обратной совместимости, поскольку современные версии I2P (2.10.0+) используют [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/). Протокол ElGamal признан устаревшим и сохраняется исключительно в исторических целях и для обеспечения совместимости.

## Обзор

ElGamal/AES+SessionTag обеспечивал первоначальный механизм сквозного шифрования в I2P для garlic messages (garlic-сообщений). Он объединял:

- **ElGamal (2048-битный)** — для обмена ключами
- **AES-256/CBC** — для шифрования полезной нагрузки
- **SHA-256** — для хеширования и генерации IV (инициализационный вектор)
- **Сеансовые теги (32 байта)** — для одноразовых идентификаторов сообщений

Протокол позволял routers и адресатам безопасно обмениваться данными без поддержания постоянных соединений. В каждой сессии выполнялся асимметричный обмен по алгоритму ElGamal для установления симметричного ключа AES, после чего передавались легковесные "помеченные" сообщения, ссылающиеся на эту сессию.

## Работа протокола

### Установление сеанса (новый сеанс)

Новый сеанс начался с сообщения, содержащего два раздела:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Section</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>ElGamal-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">222 bytes of plaintext encrypted using the recipient's ElGamal public key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Establishes the AES session key and IV seed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>AES-encrypted block</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (≥128 bytes typical)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload data, integrity hash, and session tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Carries the actual message and new tags</td>
    </tr>
  </tbody>
</table>
Открытый текст внутри блока ElGamal состоял из:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 key for the session</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Pre-IV</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Material for deriving the AES initialization vector (<code>IV = first 16 bytes of SHA-256(Pre-IV)</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">158 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Filler to reach required ElGamal plaintext length</td>
    </tr>
  </tbody>
</table>
### Сообщения для существующей сессии

После установления сеанса отправитель мог отправлять сообщения **existing-session** (для уже существующей сессии), используя кэшированные теги сеанса:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single-use identifier tied to the existing session key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-Encrypted Block</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted payload and metadata using the established AES key</td>
    </tr>
  </tbody>
</table>
Routers кэшировали полученные теги примерно **15 минут**, после чего срок действия неиспользованных тегов истекал. Каждый тег был действителен ровно для **одного сообщения**, чтобы предотвратить корреляционные атаки.

### Формат AES-зашифрованного блока

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tag Count</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Number (0–200) of new session tags included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Tags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 × N bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Newly generated single-use tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Size</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Length of the payload in bytes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SHA-256 digest of the payload</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Flag</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 byte</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0x00</code> normal, <code>0x01</code> = new session key follows (unused)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">New Session Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32 bytes (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replacement AES key (rarely used)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypted message data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable (16-byte aligned)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding to block boundary</td>
    </tr>
  </tbody>
</table>
Routers расшифровывают, используя сеансовый ключ и IV, полученные либо из Pre-IV (предварительный IV) для новых сеансов, либо из сеансового тега для существующих сеансов. После расшифрования они проверяют целостность, пересчитывая хэш SHA-256 от открытого текста полезной нагрузки.

## Управление тегами сеанса

- Теги — **односторонние**: теги для направления Алиса → Боб не могут быть повторно использованы для Боб → Алиса.
- Срок действия тегов истекает примерно через **15 минут**.
- Routers поддерживают по одному **менеджеру сеансовых ключей** для каждого назначения, чтобы отслеживать теги, ключи и время их истечения.
- Приложения могут управлять поведением тегов с помощью [параметров I2CP](/docs/specs/i2cp/):
  - **`i2cp.tagThreshold`** — минимальное количество кэшированных тегов до пополнения
  - **`i2cp.tagCount`** — число новых тегов на сообщение

Этот механизм минимизировал ресурсоёмные рукопожатия ElGamal, сохраняя при этом несвязываемость между сообщениями.

## Конфигурация и эффективность

Сеансовые теги были введены, чтобы повысить эффективность при работе поверх транспорта I2P с высокой задержкой и неупорядоченной доставкой. Типичная конфигурация передавала **40 тегов на сообщение**, добавляя около 1,2 КБ служебных данных. Приложения могли настраивать поведение доставки в зависимости от ожидаемого трафика:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Tags</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Short-lived requests (HTTP, datagrams)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0 – 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low overhead, may trigger ElGamal fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent streams or bulk transfer</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20 – 50</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Higher bandwidth use, avoids session re-establishment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Long-term services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">50+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensures steady tag supply despite loss or delay</td>
    </tr>
  </tbody>
</table>
Routers периодически удаляют просроченные теги и подчищают неиспользуемое состояние сеанса, чтобы снизить использование памяти и противодействовать атакам tag-flooding (наводнение метками).

## Ограничения

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Limitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Performance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">514-byte ElGamal block adds heavy overhead for new sessions; session tags consume 32 bytes each.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Security</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No forward secrecy – compromise of ElGamal private key exposes past sessions.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Integrity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-CBC requires manual hash verification; no AEAD.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Quantum Resistance</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Vulnerable to Shor's algorithm – will not survive quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Complexity</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires stateful tag management and careful timeout tuning.</td>
    </tr>
  </tbody>
</table>
Эти недостатки непосредственно подтолкнули к разработке протокола [ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/), который обеспечивает совершенную прямую секретность, аутентифицированное шифрование и эффективный обмен ключами.

## Статус устаревания и миграции

- **Введено:** Ранние релизы I2P (до 0.6)
- **Устарело:** С появлением ECIES-X25519 (0.9.46 → 0.9.48)
- **Удалено:** Больше не используется по умолчанию начиная с 2.4.0 (декабрь 2023 г.)
- **Поддерживается:** Только для обратной совместимости

Современные router и назначения теперь анонсируют **тип криптографии 4 (ECIES-X25519)** вместо **типа 0 (ElGamal/AES)**. Устаревший протокол по‑прежнему распознаётся для обеспечения совместимости с устаревшими пирами, но его не следует использовать для новых развёртываний.

## Исторический контекст

ElGamal/AES+SessionTag лежал в основе ранней криптографической архитектуры I2P. Его гибридная конструкция ввела такие новшества, как одноразовые session tags (метки сеанса) и однонаправленные сеансы, которые повлияли на последующие протоколы. Многие из этих идей эволюционировали в современные конструкции, такие как детерминированные ratchets (механизмы последовательного обновления ключей) и гибридные постквантовые обмены ключами.
