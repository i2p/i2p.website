---
title: "Низкоуровневая криптография"
description: "Сводка симметричных, асимметричных и примитивов электронной подписи, используемых в I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

> **Статус:** Эта страница сводит воедино материалы из устаревшей "Low-level Cryptography Specification" (спецификация криптографии низкого уровня). Современные релизы I2P (2.10.0, октябрь 2025) завершили миграцию на новые криптографические примитивы. Для деталей реализации используйте специализированные спецификации, такие как [ECIES](/docs/specs/ecies/), [Encrypted LeaseSets](/docs/specs/encryptedleaseset/), [NTCP2](/docs/specs/ntcp2/), [Red25519](/docs/specs/red25519-signature-scheme/), [SSU2](/docs/specs/ssu2/) и [Tunnel Creation (ECIES)](/docs/specs/implementation/).

## Снимок эволюции

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Асимметричное шифрование

### X25519 (алгоритм обмена ключами на эллиптических кривых)

- Используется для NTCP2, ECIES-X25519-AEAD-Ratchet (схема шифрования/обмена ключами на основе X25519 с AEAD и ратчетом), SSU2 и создания tunnel на основе X25519.  
- Обеспечивает компактные ключи, операции с постоянным временем выполнения и прямую секретность через фреймворк протокола Noise.  
- Обеспечивает 128-битную криптостойкость с 32-байтовыми ключами и эффективный обмен ключами.

### Эль-Гамаль (устаревший)

- Сохранено для обратной совместимости со старыми routers.  
- Работает на 2048‑битном простом числе группы Oakley 14 (RFC 3526) с генератором 2.  
- Шифрует сеансовые ключи AES и векторы инициализации (IVs) в 514‑байтовые шифротексты.  
- Не обеспечивает аутентифицированного шифрования и прямой секретности; все современные конечные точки перешли на ECIES.

## Симметричное шифрование

### ChaCha20/Poly1305 (алгоритм аутентифицированного шифрования AEAD)

- Примитив аутентифицированного шифрования по умолчанию для NTCP2, SSU2 и ECIES.  
- Обеспечивает защиту AEAD и высокую производительность без аппаратной поддержки AES.  
- Реализован согласно RFC 7539 (256‑битный ключ, 96‑битный nonce (одноразовое число), 128‑битный тег).

### AES‑256/CBC (устаревший)

- По‑прежнему используется для шифрования на уровне tunnel, где его структура блочного шифра хорошо вписывается в многослойную модель шифрования I2P.  
- Использует дополнение PKCS#5 и преобразования IV на каждом переходе.  
- Запланирован к долгосрочному пересмотру, но остаётся криптографически стойким.

## Подписи

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Хэш и деривация ключей

- **SHA‑256:** Используется для ключей DHT (распределённой хеш‑таблицы), HKDF и устаревших подписей.  
- **SHA‑512:** Используется в EdDSA/RedDSA и при выводе ключей HKDF в Noise.  
- **HKDF‑SHA256:** Используется для вывода сеансовых ключей в ECIES, NTCP2 и SSU2.  
- Ежедневно ротируемые производные SHA‑256 защищают места хранения RouterInfo и LeaseSet в netDb.

## Сводка по транспортному уровню

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Оба транспорта обеспечивают прямую секретность и защиту от повторов на канальном уровне, используя шаблон рукопожатия Noise_XK.

## Шифрование уровня tunnel

- По‑прежнему используется AES‑256/CBC для многослойного шифрования на каждом переходе.  
- Шлюзы исходящего туннеля выполняют итеративную расшифровку AES; каждый переход повторно шифрует, используя свой ключ слоя и ключ IV (инициализационный вектор).  
- Шифрование с двойным IV снижает риск корреляционных и подтверждающих атак.  
- Переход на AEAD (аутентифицированное шифрование с дополнительными данными) изучается, но в настоящее время не планируется.

## Постквантовая криптография

- I2P 2.10.0 представляет **экспериментальное гибридное постквантовое шифрование**.  
- Включается вручную через менеджер скрытых сервисов для тестирования.  
- Комбинирует X25519 с квантово‑устойчивым KEM (механизм инкапсуляции ключа) (гибридный режим).  
- Не включено по умолчанию; предназначено для исследований и оценки производительности.

## Фреймворк расширяемости

- Идентификаторы типов шифрования и подписи обеспечивают параллельную поддержку нескольких криптографических примитивов.  
- Текущие соответствия включают:  
  - **Типы шифрования:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Типы подписей:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Этот механизм позволяет выполнять будущие обновления, включая пост‑квантовые схемы, без разделения сети.

## Композиция криптографических примитивов

- **Транспортный уровень:** X25519 + ChaCha20/Poly1305 (фреймворк Noise).  
- **Уровень tunnel:** многослойное шифрование AES‑256/CBC для анонимности.  
- **Сквозной:** ECIES‑X25519‑AEAD‑Ratchet для конфиденциальности и прямой секретности (forward secrecy).  
- **Уровень базы данных:** подписи EdDSA/RedDSA для аутентичности.

Эти уровни в совокупности обеспечивают защиту в глубину: даже если один из уровней скомпрометирован, остальные сохраняют конфиденциальность и несвязываемость.

## Сводка

Криптографический стек I2P 2.10.0 сосредоточен на:

- **Curve25519 (X25519)** для обмена ключами  
- **ChaCha20/Poly1305** для симметричного шифрования  
- **EdDSA / RedDSA** для подписей  
- **SHA‑256 / SHA‑512** для хеширования и деривации ключей  
- **Экспериментальные постквантовые гибридные режимы** для обеспечения совместимости в будущем

Устаревшие ElGamal, AES‑CBC и DSA сохраняются для обратной совместимости, но больше не используются в активных транспортах или путях шифрования.
