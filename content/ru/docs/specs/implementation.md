---
title: "Руководство по работе с tunnel"
description: "Унифицированная спецификация для построения, шифрования и передачи трафика с использованием I2P tunnels."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Область действия:** Это руководство объединяет реализацию tunnel, формат сообщений и обе спецификации создания tunnel (ECIES и устаревший ElGamal). Существующие глубокие ссылки продолжают работать через приведённые выше псевдонимы.

## Модель Tunnel {#tunnel-model}

I2P пересылает полезные данные через *однонаправленные tunnels*: упорядоченные наборы router, которые передают трафик в одном направлении. Полный обмен данными между двумя конечными точками требует четырёх tunnels (два исходящих, два входящих).

Начните с раздела [Обзор Tunnel](/docs/overview/tunnel-routing/) по терминологии, затем используйте это руководство для подробностей работы.

### Жизненный цикл сообщения {#message-lifecycle}

1. tunnel **шлюз** группирует одно или несколько сообщений I2NP, фрагментирует их и записывает инструкции доставки.
2. Шлюз инкапсулирует полезную нагрузку в фиксированное по размеру (1024&nbsp;B) сообщение tunnel, добавляя заполнение при необходимости.
3. Каждый **участник** проверяет предыдущий хоп, применяет свой слой шифрования и пересылает `{nextTunnelId, nextIV, encryptedPayload}` следующему хопу.
4. tunnel **конечная точка** удаляет последний слой, обрабатывает инструкции доставки, заново собирает фрагменты и передаёт восстановленные сообщения I2NP.

Обнаружение дубликатов использует затухающий фильтр Блума, в котором ключом служит XOR от IV (вектор инициализации) и первого блока шифротекста, чтобы предотвратить атаки с маркировкой, основанные на подмене IV.

### Роли вкратце {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Процесс шифрования {#encryption-workflow}

- **Входящие tunnels:** шлюз один раз шифрует своим ключом уровня; последующие участники продолжают шифровать, пока создатель не расшифрует конечную полезную нагрузку.
- **Исходящие tunnels:** шлюз предварительно применяет обратное преобразование шифрования для каждого перехода, так что каждый участник шифрует. Когда конечная точка шифрует, исходный открытый текст шлюза восстанавливается.

Оба направления пересылают `{tunnelId, IV, encryptedPayload}` на следующий хоп.

---

## Формат сообщения tunnel {#tunnel-message-format}

Шлюзы tunnel разбивают сообщения I2NP на оболочки фиксированного размера, чтобы скрыть длину полезной нагрузки и упростить обработку на каждом хопе.

### Зашифрованная структура {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – 32-битный идентификатор следующего узла (ненулевой, обновляется при каждом цикле построения).
- **IV** – 16-байтный AES IV, выбирается для каждого сообщения.
- **Encrypted payload** – 1008 байт шифротекста AES-256-CBC.

Общий размер: 1028 байт.

### Расшифрованная структура {#decrypted-layout}

После снятия промежуточным узлом своего слоя шифрования:

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Контрольная сумма** проверяет целостность расшифрованного блока.
- **Дополнение (padding)** — случайные ненулевые байты, оканчивающиеся нулевым байтом.
- **Инструкции доставки** сообщают конечной точке, как обрабатывать каждый фрагмент (доставить локально, переслать в другой tunnel и т. п.).
- **Фрагменты** содержат исходные сообщения I2NP; конечная точка собирает их, прежде чем передать на вышележащие уровни.

### Этапы обработки {#processing-steps}

1. Шлюзы фрагментируют и ставят в очередь сообщения I2NP, ненадолго удерживая частичные фрагменты для последующей сборки.
2. Шлюз шифрует полезную нагрузку соответствующими ключами уровня и устанавливает tunnel ID и IV (вектор инициализации).
3. Каждый участник шифрует IV (AES-256/ECB), затем полезную нагрузку (AES-256/CBC), после чего повторно шифрует IV и пересылает сообщение.
4. Конечная точка расшифровывает в обратном порядке, проверяет контрольную сумму, обрабатывает инструкции доставки и собирает фрагменты.

---

## Создание tunnel (ECIES-X25519) {#tunnel-creation-ecies}

Современные routers создают tunnels с ключами ECIES-X25519, что уменьшает размер сообщений построения и обеспечивает прямую секретность.

- **Сообщение построения:** одно сообщение I2NP `TunnelBuild` (или `VariableTunnelBuild`) переносит 1–8 зашифрованных записей построения, по одной на каждый hop (переход).
- **Ключи слоя:** создатель выводит для каждого хопа ключи слоя, IV и ключи ответа с помощью HKDF, используя статический X25519-идентификатор хопа и свой эфемерный ключ.
- **Обработка:** каждый хоп расшифровывает свою запись, проверяет флаги запроса, записывает блок ответа (успех или подробный код ошибки), повторно шифрует оставшиеся записи и пересылает сообщение дальше.
- **Ответы:** создатель получает ответное сообщение, упакованное с garlic encryption. Записи, помеченные как неуспешные, содержат код уровня серьёзности, чтобы router мог профилировать пира.
- **Совместимость:** routers всё ещё могут принимать устаревшие построения ElGamal для обратной совместимости, но новые tunnels по умолчанию используют ECIES.

> За константами для каждого поля и примечаниями по выведению ключей см. историю предложений ECIES (схема интегрированного шифрования на эллиптических кривых) и исходный код router; это руководство описывает последовательность работы.

---

## Устаревшее создание Tunnel (ElGamal-2048) {#tunnel-creation-elgamal}

Первоначальный формат построения tunnel использовал открытые ключи ElGamal. Современные routers сохраняют ограниченную поддержку для обратной совместимости.

> **Статус:** Устарело. Оставлено здесь для исторической справки и для тех, кто поддерживает инструменты, совместимые с устаревшими версиями.

- **Неинтерактивное телескопирование:** одно сообщение построения проходит по всему маршруту. Каждый хоп расшифровывает свою 528-байтовую запись, обновляет сообщение и пересылает его дальше.
- **Переменная длина:** Variable Tunnel Build Message (VTBM; переменное сообщение построения tunnel) допускало 1–8 записей. Более раннее фиксированное сообщение всегда содержало восемь записей, чтобы скрыть длину tunnel.
- **Структура записи запроса:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Флаги:** бит 7 обозначает входной шлюз (IBGW); бит 6 помечает исходящую конечную точку (OBEP). Они взаимно исключают друг друга.
- **Шифрование:** каждая запись зашифрована с помощью ElGamal-2048 с использованием открытого ключа хопа. Многослойное симметричное шифрование AES-256-CBC обеспечивает, что только целевой хоп может прочитать свою запись.
- **Ключевые факты:** идентификаторы tunnel — это ненулевые 32-битные значения; создатели могут вставлять фиктивные записи, чтобы скрыть фактическую длину tunnel; надежность зависит от повторных попыток при неудачных построениях.

---

## Пулы Tunnel и жизненный цикл {#tunnel-pools}

Routers поддерживают независимые входящие и исходящие tunnel-пулы для исследовательского трафика и для каждой сессии I2CP.

- **Выбор пиров:** исследовательские tunnels выбираются из бакета пиров “активные, без сбоев” для повышения разнообразия; клиентские tunnels предпочитают быстрых пиров с высокой пропускной способностью.
- **Детерминированная упорядоченность:** пиры сортируются по расстоянию XOR между `SHA256(peerHash || poolKey)` и случайным ключом пула. Ключ сменяется при перезапуске, обеспечивая стабильность в рамках одного запуска и затрудняя атаки предшественника между запусками.
- **Жизненный цикл:** routers отслеживают исторические времена построения для каждого кортежа `{mode, direction, length, variance}`. По мере приближения срока истечения tunnels замены запускаются заранее; router увеличивает число параллельных сборок при сбоях, ограничивая максимальное количество незавершённых попыток.
- **Параметры конфигурации:** число активных/резервных tunnels, длина хопа и вариация, разрешение zero-hop (0 хопов), а также лимиты скорости построения — всё настраивается для каждого пула.

---

## Перегрузка и надёжность {#congestion}

Хотя tunnels напоминают цепочки, routers рассматривают их как очереди сообщений. Взвешенное случайное раннее отбрасывание (Weighted Random Early Discard, WRED) используется, чтобы поддерживать задержку в заданных пределах:

- Вероятность отбрасывания растёт по мере приближения загрузки к настроенным пределам.
- Участники используют фрагменты фиксированного размера; шлюзы/конечные точки отбрасывают на основании суммарного размера фрагментов, отдавая приоритет отбрасыванию крупных полезных нагрузок.
- Исходящие конечные точки отбрасывают раньше других ролей, чтобы минимизировать напрасные затраты сетевых ресурсов.

Гарантированная доставка оставлена более высоким уровням, таким как [Streaming library (библиотека потоковой передачи данных)](/docs/specs/streaming/). Приложения, которым требуется надежность, должны самостоятельно обрабатывать повторную передачу и подтверждения.

---

## Дополнительные материалы {#further-reading}

- [Однонаправленные Tunnels (исторические)](/docs/legacy/unidirectional-tunnels/)
- [Выбор пиров](/docs/overview/tunnel-routing#peer-selection/)
- [Обзор Tunnel](/docs/overview/tunnel-routing/)
- [Старая реализация Tunnel](/docs/legacy/old-implementation/)
