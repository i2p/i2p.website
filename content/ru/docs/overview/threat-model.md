---
title: "Модель угроз I2P"
description: "Каталог атак, учтенных в дизайне I2P, и существующие меры защиты"
slug: "threat-model"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## 1. Что означает "Анонимный"

I2P обеспечивает *практическую анонимность* — не невидимость. Анонимность определяется как сложность для противника получить информацию, которую вы хотите сохранить в тайне: кто вы, где вы находитесь или с кем вы общаетесь. Абсолютная анонимость невозможна; вместо этого I2P стремится к **достаточной анонимности** в условиях глобальных пассивных и активных противников.

Ваша анонимность зависит от того, как вы настроите I2P, как выберете узлы и подписки, и какие приложения вы откроете для доступа.

---

## 2. Эволюция криптографии и транспорта (2003 → 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Era</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Algorithms</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.3 – 0.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal + AES-256 + DSA-SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy stack (2003–2015)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Replaced DSA</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36 (2018)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NTCP2</strong> introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise <em>XK_25519_ChaChaPoly_SHA256</em></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.56 (2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU2</strong> enabled by default</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0 (2023)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Sub-DB isolation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents router↔client linkage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.8.0+ (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing / observability reductions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DoS hardening</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0 (2025)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid ML-KEM support (optional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
    </tr>
  </tbody>
</table>
**Текущий криптографический набор (Noise XK):** - **X25519** для обмена ключами   - **ChaCha20/Poly1305 AEAD** для шифрования   - **Ed25519 (EdDSA-SHA512)** для подписей   - **SHA-256** для хеширования и HKDF   - Опциональные **ML-KEM гибриды** для постквантового тестирования

Все использования ElGamal и AES-CBC упразднены. Транспорт полностью основан на NTCP2 (TCP) и SSU2 (UDP); оба поддерживают IPv4/IPv6, прямую секретность (forward secrecy) и обфускацию для противодействия DPI.

---

## 3. Краткий обзор сетевой архитектуры

- **Mixnet со свободной маршрутизацией:** Отправители и получатели самостоятельно определяют свои tunnel.  
- **Отсутствие центрального органа:** Маршрутизация и именование децентрализованы; каждый router поддерживает локальное доверие.  
- **Однонаправленные tunnel:** Входящие и исходящие разделены (время жизни 10 минут).  
- **Exploratory tunnel:** По умолчанию 2 hop; клиентские tunnel — 2–3 hop.  
- **Floodfill router:** ~1 700 из ~55 000 узлов (~6 %) поддерживают распределённую NetDB.  
- **Ротация NetDB:** Пространство ключей обновляется ежедневно в полночь UTC.  
- **Изоляция под-БД:** Начиная с версии 2.4.0, каждый клиент и router используют отдельные базы данных для предотвращения связывания.

---

## 4. Категории атак и текущие средства защиты

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current Status (2025)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Primary Defenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Brute Force / Cryptanalysis</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Impractical with modern primitives (X25519, ChaCha20).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Strong crypto, key rotation, Noise handshakes.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Timing Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Still unsolved for low-latency systems.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Unidirectional tunnels, 1024&nbsp;B cells, profile recalc (45&nbsp;s). Research continues for non-trivial delays (3.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Intersection Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inherent weakness of low latency mixnets.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel rotation (10&nbsp;min), leaseset expirations, multihoming.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Predecessor Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Partially mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tiered peer selection, strict XOR ordering, variable length tunnels.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Sybil Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No comprehensive defense.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IP /16 limits, profiling, diversity rules; HashCash infra exists but not required.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Floodfill / NetDB Attacks</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved but still a concern.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">One /16 per lookup, limit 500 active, daily rotation, randomized verification delay, Sub-DB isolation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS / Flooding</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Frequent (esp. 2023 incidents).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Congestion-aware routing (2.4+), aggressive leaseset removal (2.8+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Traffic ID / Fingerprinting</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Greatly reduced.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise obfuscation, random padding, no plaintext headers.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Censorship / Partitioning</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Possible with state-level blocking.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden mode, IPv6, multiple reseeds, mirrors.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Development / Supply Chain</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Mitigated.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Open source, signed SU3 releases (RSA-4096), multi-signer trust model.</td>
    </tr>
  </tbody>
</table>
---

## 5. Современная сетевая база данных (NetDB)

**Основные факты (всё ещё актуальны):** - Модифицированная Kademlia DHT хранит RouterInfo и LeaseSets.   - Хеширование ключей SHA-256; параллельные запросы к 2 ближайшим floodfills с таймаутом 10 с.   - Время жизни LeaseSet ≈ 10 мин (LeaseSet2) или 18 ч (MetaLeaseSet).

**Новые типы (начиная с версии 0.9.38):** - **LeaseSet2 (тип 3)** – несколько типов шифрования, с временными метками.   - **EncryptedLeaseSet2 (тип 5)** – скрытый destination для приватных сервисов (аутентификация DH или PSK).   - **MetaLeaseSet (тип 7)** – мультихоминг и расширенные сроки действия.

**Крупное обновление безопасности – изоляция Sub-DB (2.4.0):** - Предотвращает связывание router↔client.   - Каждый client и router используют отдельные сегменты netDb.   - Проверено и прошло аудит (2.5.0).

---

## 6. Скрытый режим и ограниченные маршруты

- **Hidden Mode:** Реализован (автоматически активируется в странах со строгими ограничениями согласно индексу Freedom House).  
    Роутеры не публикуют RouterInfo и не маршрутизируют трафик.  
- **Restricted Routes:** Частично реализовано (базовые tunnel только через доверенные узлы).  
    Комплексная маршрутизация через доверенные узлы запланирована (3.0+).

Компромисс: Лучшая конфиденциальность ↔ уменьшенный вклад в пропускную способность сети.

---

## 7. DoS и Floodfill атаки

**Исторический контекст:** Исследование UCSB 2013 года показало возможность атак Eclipse и захвата Floodfill.   **Современные меры защиты включают:** - Ежедневная ротация keyspace.   - Ограничение Floodfill ≈ 500, один на /16.   - Рандомизированные задержки проверки хранилища.   - Предпочтение более новым роутерам (2.6.0).   - Исправление автоматической регистрации (2.9.0).   - Маршрутизация с учётом перегрузки и throttling lease (2.4.0+).

Атаки на floodfill остаются теоретически возможными, но практически более сложными.

---

## 8. Анализ трафика и цензура

Трафик I2P сложно идентифицировать: нет фиксированного порта, нет handshake в открытом виде и используется случайное заполнение. Пакеты NTCP2 и SSU2 имитируют распространённые протоколы и применяют обфускацию заголовков ChaCha20. Стратегии заполнения базовые (случайные размеры), фиктивный трафик не реализован (ресурсозатратно). Подключения с выходных узлов Tor блокируются начиная с версии 2.6.0 (для защиты ресурсов).

---

## 9. Постоянные ограничения (признанные)

- Корреляция по времени для низколатентных приложений остается фундаментальным риском.
- Атаки пересечения все еще эффективны против известных публичных узлов назначения.
- Атаки Сивиллы не имеют полной защиты (HashCash не применяется принудительно).
- Трафик с постоянной скоростью и нетривиальные задержки остаются нереализованными (запланировано в 3.0).

Прозрачность в отношении этих ограничений является намеренной — она предотвращает переоценку пользователями уровня анонимности.

---

## 10. Сетевая статистика (2025)

- ~55 000 активных роутеров по всему миру (↑ с 7 000 в 2013)  
- ~1 700 floodfill роутеров (~6 %)  
- 95 % участвуют в маршрутизации туннелей по умолчанию  
- Уровни пропускной способности: K (<12 КБ/с) → X (>2 МБ/с)  
- Минимальная скорость для floodfill: 128 КБ/с  
- Консоль роутера требует Java 8+, планируется Java 17+ в следующем цикле

---

## 11. Разработка и центральные ресурсы

- Официальный сайт: [geti2p.net](/)
- Документация: [Documentation](/docs/)  
- Репозиторий Debian: <https://deb.i2pgit.org> (заменил deb.i2p2.de в октябре 2023)  
- Исходный код: <https://i2pgit.org/I2P_Developers/i2p.i2p> (Gitea) + зеркало на GitHub  
- Все релизы подписаны в контейнерах SU3 (RSA-4096, ключи zzz/str4d)  
- Активных списков рассылки нет; сообщество на <https://i2pforum.net> и IRC2P.  
- Цикл обновлений: стабильные релизы каждые 6–8 недель.

---

## 12. Обзор улучшений безопасности с версии 0.8.x

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Effect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed SHA1/DSA weakness</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2018</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2019</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">LeaseSet2 / EncryptedLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden services privacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Noise-based UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2023</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sub-DB Isolation + Congestion-Aware Routing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stopped NetDB linkage / improved resilience</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Floodfill selection improvements</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced long-term node influence</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Observability reductions + PQ hybrid crypto</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Harder timing analysis / future-proofing</td>
    </tr>
  </tbody>
</table>
---

## 13. Известные нерешенные вопросы или запланированная работа

- Комплексная маршрутизация через ограниченные маршруты (доверенные узлы) → запланировано в 3.0.  
- Нетривиальные задержки/пакетирование для защиты от анализа времени → запланировано в 3.0.  
- Расширенное дополнение (padding) и фиктивный трафик → не реализовано.  
- Проверка идентификации через HashCash → инфраструктура существует, но неактивна.  
- Замена DHT на R5N → только предложение.

---

## 14. Ключевые ссылки

- *Practical Attacks Against the I2P Network* (Egger et al., RAID 2013)  
- *Privacy Implications of Performance-Based Peer Selection* (Herrmann & Grothoff, PETS 2011)  
- *Resilience of the Invisible Internet Project* (Muntaka et al., Wiley 2025)  
- [Официальная документация I2P](/docs/)

---

## 15. Заключение

Базовая модель анонимности I2P существует уже два десятилетия: жертвовать глобальной уникальностью ради локального доверия и безопасности. От ElGamal к X25519, от NTCP к NTCP2 и от ручных reseed к изоляции Sub-DB, проект эволюционировал, сохраняя при этом свою философию эшелонированной защиты и прозрачности.

Многие атаки остаются теоретически возможными против любой низколатентной mixnet, но непрерывное укрепление I2P делает их всё более непрактичными. Сеть больше, быстрее и безопаснее, чем когда-либо, — но по-прежнему честно признаёт свои ограничения.
