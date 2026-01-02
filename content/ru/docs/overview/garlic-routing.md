---
title: "Garlic Routing"
description: "Понимание терминологии garlic routing, архитектуры и современной реализации в I2P"
slug: "garlic-routing"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

---

## 1. Обзор

**Garlic routing** (маршрутизация «чеснок») остается одним из ключевых нововведений I2P, объединяя многоуровневое шифрование, группировку сообщений и однонаправленные туннели. Хотя концептуально схож с **onion routing** (луковичной маршрутизацией), он расширяет модель, объединяя несколько зашифрованных сообщений («зубчики») в один конверт («головку чеснока»), что повышает эффективность и анонимность.

Термин *garlic routing* был введён [Майклом Дж. Фридманом](https://www.cs.princeton.edu/~mfreed/) в [магистерской диссертации Роджера Динглдайна о Free Haven](https://www.freehaven.net/papers.html) (июнь 2000, §8.1.1). Разработчики I2P приняли этот термин в начале 2000-х годов, чтобы отразить улучшения в группировке сообщений и однонаправленную модель передачи данных, отличающую его от дизайна Tor с коммутацией каналов.

> **Резюме:** Garlic routing = многослойное шифрование + объединение сообщений + анонимная доставка через однонаправленные туннели.

---

## 2. Терминология "Garlic"

Исторически термин *garlic* использовался в трёх различных контекстах в рамках I2P:

1. **Многослойное шифрование** – защита на уровне туннелей в стиле луковичной маршрутизации  
2. **Объединение нескольких сообщений** – несколько "cloves" внутри "garlic message"  
3. **Сквозное шифрование** – ранее *ElGamal/AES+SessionTags*, теперь *ECIES‑X25519‑AEAD‑Ratchet*

Хотя архитектура остается неизменной, схема шифрования была полностью модернизирована.

---

## 3. Многослойное шифрование

Garlic routing разделяет свой основополагающий принцип с onion routing: каждый router расшифровывает только один слой шифрования, узнавая только следующий переход, но не весь путь целиком.

Однако I2P реализует **однонаправленные туннели**, а не двунаправленные цепи:

- **Outbound tunnel**: отправляет сообщения от создателя  
- **Inbound tunnel**: доставляет сообщения обратно к создателю

Полный цикл обмена данными (Алиса ↔ Боб) использует четыре tunnel: исходящий tunnel Алисы → входящий tunnel Боба, затем исходящий tunnel Боба → входящий tunnel Алисы. Такая архитектура **вдвое снижает возможность корреляции данных** по сравнению с двунаправленными каналами.

Для получения информации о деталях реализации туннелей см. [Спецификацию туннелей](/docs/specs/implementation) и спецификацию [Создание туннелей (ECIES)](/docs/specs/implementation).

---

## 4. Объединение нескольких сообщений («дольки»)

Оригинальная концепция garlic routing Фридмана предполагала объединение нескольких зашифрованных «луковиц» внутри одного сообщения. I2P реализует это как **cloves** (зубчики) внутри **garlic message** (чесночного сообщения) — каждый clove имеет свои собственные зашифрованные инструкции доставки и цель (router, destination или tunnel).

Garlic bundling позволяет I2P:

- Объединять подтверждения и метаданные с сообщениями данных
- Снижать наблюдаемые шаблоны трафика
- Поддерживать сложные структуры сообщений без дополнительных соединений

![Garlic Message Cloves](/images/garliccloves.png)   *Рисунок 1: Garlic Message, содержащее несколько cloves, каждый со своими инструкциями доставки.*

Типичные зубчики включают:

1. **Delivery Status Message** — подтверждения успешной или неуспешной доставки.  
   Они заворачиваются в отдельный слой garlic для сохранения конфиденциальности.
2. **Database Store Message** — автоматически включаемые LeaseSet'ы, чтобы узлы могли ответить без повторного запроса к netDb.

Гвоздики объединяются в пучки, когда:

- Необходимо опубликовать новый LeaseSet  
- Доставлены новые теги сессии  
- В последнее время не происходило объединение (~1 минута по умолчанию)

Garlic-сообщения обеспечивают эффективную сквозную доставку нескольких зашифрованных компонентов в одном пакете.

---

## 5. Эволюция шифрования

### 5.1 Historical Context

Ранняя документация (≤ v0.9.12) описывала шифрование *ElGamal/AES+SessionTags*:   - **ElGamal 2048‑бит** для упаковки AES ключей сеанса   - **AES‑256/CBC** для шифрования полезной нагрузки   - 32‑байтовые теги сеанса, используемые один раз на сообщение

Эта криптосистема **устарела**.

### 5.2 ECIES‑X25519‑AEAD‑Ratchet (Current Standard)

В период с 2019 по 2023 год I2P полностью перешёл на ECIES‑X25519‑AEAD‑Ratchet. Современный стек стандартизирует следующие компоненты:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ECIES Primitive or Concept</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport Layer (NTCP2, SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise_NX → X25519, ChaCha20/Poly1305, BLAKE2s</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2NP Delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES‑X25519‑AEAD (ChaCha20/Poly1305)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Session Management</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ratchet with rekey records, per-clove key material</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline Authentication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA (Ed25519) with LeaseSet2/MetaLeaseSet chains</td>
    </tr>
  </tbody>
</table>
Преимущества перехода на ECIES:

- **Прямая секретность** за счёт ключей с посменной ротацией для каждого сообщения  
- **Уменьшенный размер полезной нагрузки** по сравнению с ElGamal  
- **Устойчивость** к достижениям криптоанализа  
- **Совместимость** с будущими постквантовыми гибридами (см. Proposal 169)

Дополнительные подробности: см. [спецификацию ECIES](/docs/specs/ecies) и [спецификацию EncryptedLeaseSet](/docs/specs/encryptedleaseset).

---

## 6. LeaseSets and Garlic Bundling

Garlic-конверты часто включают LeaseSets для публикации или обновления доступности назначения.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Capabilities</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Distribution Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet (legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single encryption/signature pair</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Accepted for backward compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple crypto suites, offline signing keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for modern routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EncryptedLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Access-controlled, destination hidden from floodfill</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires shared decryption key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MetaLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Aggregates multiple destinations or multi-homed services</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Extends LeaseSet2 fields recursively</td>
    </tr>
  </tbody>
</table>
Все LeaseSets распространяются через *floodfill DHT* (распределённую хеш-таблицу), поддерживаемую специализированными роутерами. Публикации проверяются, снабжаются временными метками и ограничиваются по частоте для снижения корреляции метаданных.

См. [документацию Network Database](/docs/specs/common-structures) для подробностей.

---

## 7. Modern “Garlic” Applications within I2P

Garlic encryption и объединение сообщений используются во всём стеке протоколов I2P:

1. **Создание и использование туннелей** — послойное шифрование на каждом hop  
2. **Сквозная доставка сообщений** — связанные garlic-сообщения с клонированным подтверждением и LeaseSet cloves  
3. **Публикация в Network Database** — LeaseSets, упакованные в garlic-конверты для обеспечения приватности  
4. **Транспорты SSU2 и NTCP2** — нижележащее шифрование с использованием фреймворка Noise и примитивов X25519/ChaCha20

Garlic routing — это одновременно и *метод многослойного шифрования*, и *модель сетевого обмена сообщениями*.

---

## 6. LeaseSets и Garlic Bundling

Центр документации I2P [доступен здесь](/docs/) и постоянно обновляется. Актуальные спецификации включают:

- [Спецификация ECIES](/docs/specs/ecies) — ECIES‑X25519‑AEAD‑Ratchet
- [Создание туннелей (ECIES)](/docs/specs/implementation) — современный протокол построения туннелей
- [Спецификация I2NP](/docs/specs/i2np) — форматы сообщений I2NP
- [Спецификация SSU2](/docs/specs/ssu2) — транспорт SSU2 UDP
- [Общие структуры](/docs/specs/common-structures) — поведение netDb и floodfill

Академическая валидация: Hoang et al. (IMC 2018, USENIX FOCI 2019) и Muntaka et al. (2025) подтверждают архитектурную стабильность и операционную устойчивость дизайна I2P.

---

## 7. Современные "Garlic" приложения в I2P

Текущие предложения:

- **Предложение 169:** Гибридная постквантовая криптография (ML-KEM 512/768/1024 + X25519)  
- **Предложение 168:** Оптимизация пропускной способности транспорта  
- **Обновления датаграмм и потоковой передачи:** Улучшенное управление перегрузкой

Будущие адаптации могут включать дополнительные стратегии задержки сообщений или избыточность нескольких туннелей на уровне garlic-сообщений, основываясь на неиспользуемых опциях доставки, изначально описанных Фридманом.

---

## 8. Текущая документация и справочные материалы

- Freedman, M. J. & Dingledine, R. (2000). *Free Haven Master's Thesis,* § 8.1.1. [Free Haven Papers](https://www.freehaven.net/papers.html)  
- [Onion Router Publications](https://www.onion-router.net/Publications.html)  
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)  
- [Tor Project](https://www.torproject.org/)  
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)  
- Goldschlag, D. M., Reed, M. G., Syverson, P. F. (1996). *Hiding Routing Information.* NRL Publication.

---
