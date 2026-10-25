---
title: "Старая реализация tunnel"
description: "Историческая документация оригинальной реализации tunnel в I2P до версии 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/ru/docs/historical/tunnel-alt"
  - "/ru/docs/historical/tunnel-alt/"
  - "/ru/tunnel"
  - "/ru/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Примечание: Устарело - НЕ используется! Заменено в версии 0.6.1.10 - см. [текущую реализацию](/docs/specs/tunnel-implementation) для актуальной спецификации.**

## 1) Обзор tunnel {#tunnel.overview}

В I2P сообщения передаются в одном направлении через виртуальный tunnel из узлов, используя любые доступные средства для передачи сообщения к следующему переходу. Сообщения поступают в шлюз tunnel'а, упаковываются для маршрута и перенаправляются к следующему переходу в tunnel'е, который обрабатывает и проверяет валидность сообщения и отправляет его к следующему переходу, и так далее, пока оно не достигнет конечной точки tunnel'а. Эта конечная точка принимает сообщения, упакованные шлюзом, и перенаправляет их согласно инструкциям - либо к другому router'у, либо к другому tunnel'у на другом router'е, либо локально.

Все tunnel работают одинаково, но могут быть разделены на две различные группы - входящие tunnel и исходящие tunnel. Входящие tunnel имеют недоверенный шлюз, который передает сообщения вниз к создателю tunnel, который служит конечной точкой tunnel. Для исходящих tunnel создатель tunnel служит шлюзом, передавая сообщения к удаленной конечной точке.

Создатель tunnel точно выбирает, какие узлы будут участвовать в tunnel, и предоставляет каждому необходимые данные конфигурации. Они могут варьироваться по длине от 0 переходов (где шлюз является также конечной точкой) до 7 переходов (где есть 6 узлов после шлюза и перед конечной точкой). Цель состоит в том, чтобы затруднить как участникам, так и третьим сторонам определение длины tunnel, или даже сговорившимся участникам определить, являются ли они частью одного и того же tunnel вообще (за исключением ситуации, когда сговорившиеся узлы находятся рядом друг с другом в tunnel). Поврежденные сообщения также отбрасываются как можно быстрее, снижая нагрузку на сеть.

Помимо длины, для каждого tunnel доступны дополнительные настраиваемые параметры, такие как ограничение размера или частоты доставляемых сообщений, способ использования дополнения (padding), продолжительность работы tunnel, следует ли внедрять ложные сообщения (chaff messages), использовать ли фрагментацию и какие стратегии группировки (batching) следует применять, если таковые имеются.

На практике используется серия пулов туннелей для различных целей - каждый локальный клиентский пункт назначения имеет свой собственный набор входящих туннелей и исходящих туннелей, настроенных в соответствии с его потребностями в анонимности и производительности. Кроме того, сам router поддерживает серию пулов для участия в сетевой базе данных и для управления самими туннелями.

I2P является сетью с коммутацией пакетов по своей природе, даже с учетом этих tunnel, что позволяет использовать преимущества нескольких параллельно работающих tunnel, повышая устойчивость и балансируя нагрузку. За пределами основного слоя I2P доступна опциональная библиотека потокового вещания end-to-end для клиентских приложений, обеспечивающая TCP-подобную работу, включая переупорядочивание сообщений, повторную передачу, управление перегрузкой и т.д.

## 2) Работа tunnel {#tunnel.operation}

Работа tunnel включает четыре различных процесса, выполняемых различными узлами в tunnel. Во-первых, tunnel gateway накапливает несколько tunnel сообщений и предварительно обрабатывает их во что-то для доставки через tunnel. Затем этот gateway шифрует предварительно обработанные данные и пересылает их на первый переход. Этот узел и последующие участники tunnel снимают слой шифрования, проверяя целостность сообщения, затем пересылают его следующему узлу. В конечном итоге сообщение приходит в конечную точку, где сообщения, объединенные gateway, снова разделяются и пересылаются по запросу.

Tunnel ID — это 4-байтовые числа, используемые на каждом узле - участники знают, какой tunnel ID слушать для сообщений и какой tunnel ID следует использовать для пересылки на следующий узел. Сами tunnel существуют недолго (в настоящее время 10 минут), но в зависимости от назначения tunnel, и хотя последующие tunnel могут быть построены с использованием той же последовательности узлов, tunnel ID каждого узла будет изменяться.

### 2.1) Предварительная обработка сообщений {#tunnel.preprocessing}

Когда шлюз хочет доставить данные через туннель, он сначала собирает ноль или более I2NP сообщений (не более 32КБ), выбирает объем заполнения, который будет использован, и решает, как каждое I2NP сообщение должно обрабатываться конечной точкой туннеля, кодируя эти данные в необработанную полезную нагрузку туннеля:

- 2-байтовое беззнаковое целое число, указывающее количество байтов заполнения
- соответствующее количество случайных байтов
- серия из нуля или более пар { инструкции, сообщение }

Инструкции кодируются следующим образом:

- 1 байт значения:
  ```
  биты 0-1: тип доставки
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     бит 2: включена задержка?  (1 = да, 0 = нет)
     бит 3: фрагментирован?  (1 = да, 0 = нет)
     бит 4: расширенные опции?  (1 = да, 0 = нет)
  биты 5-7: зарезервированы
  ```
- если тип доставки был TUNNEL, 4 байта ID туннеля
- если тип доставки был TUNNEL или ROUTER, 32 байта хэша router'а
- если флаг включения задержки равен true, 1 байт значения:
  ```
     бит 0: тип (0 = строгий, 1 = случайный)
  биты 1-7: экспонента задержки (2^значение минут)
  ```
- если флаг фрагментации равен true, 4 байта ID сообщения и 1 байт значения:
  ```
  биты 0-6: номер фрагмента
     бит 7: последний?  (1 = да, 0 = нет)
  ```
- если флаг расширенных опций равен true:
  ```
  = 1 байт размера опции (в байтах)
  = столько байт
  ```
- 2 байта размера I2NP сообщения

Сообщение I2NP кодируется в стандартной форме, и предобработанная полезная нагрузка должна быть дополнена до кратного 16 байтам размера.

### 2.2) Обработка шлюза {#tunnel.gateway}

После предварительной обработки сообщений в дополненную полезную нагрузку, шлюз шифрует полезную нагрузку восемью ключами, создавая блок контрольной суммы, чтобы каждый узел мог проверить целостность полезной нагрузки в любое время, а также блок сквозной проверки для конечной точки tunnel, чтобы проверить целостность блока контрольной суммы. Конкретные детали приведены ниже.

Используемое шифрование таково, что расшифровка требует лишь прогона данных через AES в режиме CBC, вычисления SHA256 определённой фиксированной части сообщения (байты с 16 по $size-144) и поиска первых 16 байт этого хеша в блоке контрольной суммы. Определено фиксированное количество переходов (8 узлов), чтобы мы могли проверить сообщение, не раскрывая позицию в tunnel и не позволяя сообщению постоянно "сжиматься" по мере снятия слоёв. Для tunnel короче 8 переходов создатель tunnel займёт место избыточных переходов, расшифровывая своими ключами (для исходящих tunnel это делается в начале, а для входящих tunnel — в конце).

Сложная часть в шифровании заключается в построении этого связанного блока контрольных сумм, что требует по сути выяснения того, как будет выглядеть хеш полезной нагрузки на каждом шаге, случайного упорядочивания этих хешей, а затем построения матрицы того, как будет выглядеть каждый из этих случайно упорядоченных хешей на каждом шаге. Сам gateway должен притворяться одним из узлов внутри блока контрольных сумм, чтобы первый hop не мог определить, что предыдущим hop был gateway. Для наглядности:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
В приведенном выше примере P[7] является теми же исходными данными, которые передаются через tunnel (предварительно обработанные сообщения), а V[7] — это первые 16 байт SHA256 от eH[0-7], как видно на peer7 после расшифровки. Для ячеек в матрице "выше" хеша их значение получается путем шифрования ячейки под ней ключом узла под ней, используя конец столбца слева от неё в качестве IV. Для ячеек в матрице "ниже" хеша они равны ячейке над ними, расшифрованной ключом текущего узла, используя конец предыдущего зашифрованного блока в этой строке.

С этой рандомизированной матрицей блоков контрольной суммы каждый peer сможет найти хэш полезной нагрузки или, если его там нет, узнать, что сообщение повреждено. Переплетение с использованием режима CBC увеличивает сложность пометки самих блоков контрольной суммы, но всё ещё возможно, что такая пометка может остаться ненадолго незамеченной, если столбцы после помеченных данных уже использовались для проверки полезной нагрузки на peer. В любом случае, конечная точка tunnel (peer 7) точно знает, были ли помечены какие-либо блоки контрольной суммы, поскольку это повредило бы блок верификации (V[7]).

IV[0] является случайным 16-байтовым значением, а IV[i] — это первые 16 байт H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Мы не используем один и тот же IV вдоль пути, поскольку это позволило бы тривиальное сговор, и мы используем хеш расшифрованного значения для распространения IV, чтобы затруднить утечку ключей. IV_WHITENER — это фиксированное 16-байтовое значение.

Когда шлюз хочет отправить сообщение, он экспортирует нужную строку для узла, который является первым переходом (обычно строка peer1.recv) и полностью передает её.

### 2.3) Обработка участника {#tunnel.participant}

Когда участник tunnel получает сообщение, он расшифровывает слой своим ключом tunnel, используя AES256 в режиме CBC с первыми 16 байтами в качестве IV. Затем он вычисляет хеш того, что видит как полезную нагрузку (байты с 16 по $size-144) и ищет первые 16 байт этого хеша в расшифрованном блоке контрольной суммы. Если совпадение не найдено, сообщение отбрасывается. В противном случае IV обновляется путем его расшифровки, выполнения операции XOR этого значения с IV_WHITENER и замены его первыми 16 байтами его хеша. Полученное сообщение затем пересылается следующему узлу для обработки.

Для предотвращения атак повторного воспроизведения на уровне tunnel, каждый участник отслеживает полученные IV в течение времени жизни tunnel, отклоняя дубликаты. Требуемое использование памяти должно быть незначительным, поскольку каждый tunnel имеет очень короткое время жизни (на данный момент 10 минут). Постоянная скорость 100 КБ/с через tunnel с полными 32 КБ сообщениями даст 1875 сообщений, требуя менее 30 КБ памяти. Шлюзы и конечные точки обрабатывают повторное воспроизведение, отслеживая идентификаторы сообщений и время истечения I2NP сообщений, содержащихся в tunnel.

### 2.4) Обработка конечной точки {#tunnel.endpoint}

Когда сообщение достигает конечной точки tunnel, она расшифровывает и проверяет его как обычный участник. Если блок контрольной суммы имеет допустимое совпадение, конечная точка затем вычисляет хеш самого блока контрольной суммы (как он выглядит после расшифровки) и сравнивает его с расшифрованным хешем проверки (последние 16 байт). Если этот хеш проверки не совпадает, конечная точка отмечает попытку маркировки одним из участников tunnel и, возможно, отбрасывает сообщение.

На этом этапе конечная точка туннеля получает предварительно обработанные данные, отправленные шлюзом, которые она затем может разобрать на включенные I2NP сообщения и переадресовать их согласно инструкциям доставки.

### 2.5) Заполнение {#tunnel.padding}

Возможны несколько стратегий заполнения tunnel, каждая со своими достоинствами:

- Без заполнения
- Заполнение до случайного размера
- Заполнение до фиксированного размера
- Заполнение до ближайшего КБ
- Заполнение до ближайшего экспоненциального размера (2^n байт)

*Какой использовать? отсутствие заполнения наиболее эффективно, случайное заполнение — это то, что у нас есть сейчас, фиксированный размер будет либо крайней тратой ресурсов, либо заставит нас реализовать фрагментацию. Заполнение до ближайшего экспоненциального размера (как в Freenet) выглядит многообещающе. Возможно, нам следует собрать статистику по сети о том, какого размера сообщения передаются, а затем посмотреть, какие затраты и преимущества возникнут от различных стратегий?*

### 2.6) Фрагментация туннелей {#tunnel.fragmentation}

Для различных схем дополнения и перемешивания может быть полезно с точки зрения анонимности фрагментировать одно I2NP сообщение на несколько частей, каждая из которых доставляется отдельно через разные tunnel сообщения. Конечная точка может поддерживать или не поддерживать такую фрагментацию (отбрасывая или сохраняя фрагменты по мере необходимости), и обработка фрагментации не будет реализована немедленно.

### 2.7) Альтернативы {#tunnel.alternatives}

#### 2.7.1) Не использовать блок контрольной суммы {#tunnel.nochecksum}

Одной из альтернатив описанному выше процессу является полное удаление блока контрольной суммы и замена хэша верификации простым хэшем полезной нагрузки. Это упростило бы обработку на шлюзе tunnel и сэкономило бы 144 байта пропускной способности на каждом переходе. С другой стороны, злоумышленники внутри tunnel могли бы тривиально изменить размер сообщения до такого, который легко отслеживается сговорившимися внешними наблюдателями в дополнение к последующим участникам tunnel. Повреждение также привело бы к потере всей пропускной способности, необходимой для передачи сообщения. Без проверки на каждом переходе также стало бы возможным потреблять избыточные сетевые ресурсы путем построения чрезвычайно длинных tunnel или создания циклов в tunnel.

#### 2.7.2) Настройка обработки tunnel в процессе {#tunnel.reroute}

Хотя простого алгоритма маршрутизации tunnel должно быть достаточно для большинства случаев, существует три альтернативы, которые можно рассмотрить:

- Задержать сообщение внутри tunnel на произвольном hop либо на указанное время, либо на случайный период. Это можно достичь, заменив хеш в блоке контрольной суммы на, например, первые 8 байт хеша, за которыми следуют инструкции задержки. Альтернативно, инструкции могли бы сказать участнику фактически интерпретировать исходную полезную нагрузку как есть и либо отбросить сообщение, либо продолжить пересылать его по пути (где оно было бы интерпретировано конечной точкой как chaff сообщение). Последняя часть этого потребовала бы от шлюза корректировки алгоритма шифрования для создания открытой полезной нагрузки на другом hop, но это не должно вызвать больших трудностей.

- Разрешить router'ам, участвующим в tunnel, перемешивать сообщение перед его пересылкой - перенаправляя его через один из собственных исходящих tunnel'ей этого узла с инструкциями для доставки к следующему узлу. Это может использоваться либо контролируемым образом (с инструкциями по маршруту, такими как задержки, упомянутые выше), либо вероятностно.

- Реализовать код для создателя tunnel, позволяющий переопределить "следующий переход" узла в tunnel, обеспечивая дальнейшее динамическое перенаправление.

#### 2.7.3) Использование двунаправленных tunnel {#tunnel.bidirectional}

Текущая стратегия использования двух отдельных tunnel для входящей и исходящей связи не является единственной доступной техникой, и она имеет последствия для анонимности. С положительной стороны, использование отдельных tunnel уменьшает объем трафика, подверженного анализу участниками tunnel - например, узлы в исходящем tunnel от веб-браузера видели бы только трафик HTTP GET, в то время как узлы во входящем tunnel видели бы полезную нагрузку, доставляемую по tunnel. При двунаправленных tunnel все участники имели бы доступ к информации о том, что, например, 1КБ было отправлено в одном направлении, а затем 100КБ в другом. С отрицательной стороны, использование однонаправленных tunnel означает, что есть два набора узлов, которые нужно профилировать и учитывать, и необходимо принимать дополнительные меры для решения проблемы увеличенной скорости атак предшественников. Процесс объединения в пулы и построения tunnel, описанный ниже, должен минимизировать беспокойства об атаке предшественников, хотя при желании не составило бы большого труда построить как входящие, так и исходящие tunnel вдоль одних и тех же узлов.

#### 2.7.4) Использовать меньший размер блока {#tunnel.smallerhashes}

В данный момент наше использование AES ограничивает размер блока до 16 байт, что в свою очередь определяет минимальный размер для каждого столбца блока контрольной суммы. Если бы использовался другой алгоритм с меньшим размером блока, или который иным образом позволял бы безопасно создавать блок контрольной суммы с меньшими частями хеша, это могло бы стоить изучения. 16 байт, используемых сейчас на каждом узле, должно быть более чем достаточно.

## 3) Построение tunnel {#tunnel.building}

При построении tunnel создатель должен отправить запрос с необходимыми конфигурационными данными каждому из узлов, а затем ждать, пока потенциальный участник ответит, что он либо согласен, либо не согласен. Эти сообщения запроса tunnel и их ответы упакованы с помощью garlic encryption, чтобы только router, знающий ключ, мог их расшифровать, и путь, пройденный в обоих направлениях, также маршрутизируется через tunnel. При создании tunnel важно учитывать три аспекта: какие узлы используются (и где), как отправляются запросы (и получаются ответы), и как они поддерживаются.

### 3.1) Выбор узлов {#tunnel.peerselection}

Помимо двух типов tunnel'ов - входящих и исходящих - существует два стиля выбора узлов, используемых для разных tunnel'ов - исследовательский и клиентский. Исследовательские tunnel'ы используются как для обслуживания сетевой базы данных, так и для обслуживания tunnel'ов, в то время как клиентские tunnel'ы используются для сквозных клиентских сообщений.

#### 3.1.1) Выбор участника разведывательного tunnel {#tunnel.selection.exploratory}

Исследовательские tunnel строятся из случайной выборки узлов из подмножества сети. Конкретное подмножество зависит от локального router и от того, какие потребности в маршрутизации tunnel у него есть. В общем случае исследовательские tunnel строятся из случайно выбранных узлов, которые находятся в категории профиля "не падающие, но активные". Вторичная цель tunnel, помимо простой маршрутизации tunnel, заключается в поиске недогруженных узлов с высокой пропускной способностью, чтобы их можно было использовать в клиентских tunnel.

#### 3.1.2) Выбор узлов для клиентского tunnel {#tunnel.selection.client}

Клиентские tunnel строятся с более строгим набором требований - локальный router выберет узлы из своей категории профилей "быстрые и высокопроизводительные", чтобы производительность и надежность соответствовали потребностям клиентского приложения. Однако существует несколько важных деталей помимо этого базового выбора, которых следует придерживаться в зависимости от потребностей клиента в анонимности.

Для некоторых клиентов, которые беспокоятся о том, что противники могут осуществить атаку предшественника, выбор tunnel может поддерживать выбранные узлы в строгом порядке - если A, B и C находятся в tunnel, переход после A всегда ведет к B, а переход после B всегда ведет к C. Менее строгое упорядочивание также возможно, гарантируя, что хотя переход после A может вести к B, B никогда не может находиться перед A. Другие параметры конфигурации включают возможность фиксации только входящих tunnel-шлюзов и исходящих tunnel-конечных точек, или их ротации с частотой MTBF.

### 3.2) Доставка запроса {#tunnel.request}

Как упоминалось выше, когда создатель туннеля знает, какие узлы должны войти в туннель и в каком порядке, создатель формирует серию сообщений запроса туннеля, каждое из которых содержит необходимую информацию для этого узла. Например, участвующие туннели получают 4-байтовый tunnel ID, на котором они должны принимать сообщения, 4-байтовый tunnel ID, на котором они должны отправлять сообщения, 32-байтовый хеш идентичности следующего узла и 32-байтовый ключ слоя, используемый для удаления слоя из туннеля. Разумеется, конечные точки исходящих туннелей не получают никакой информации о "следующем узле" или "следующем tunnel ID". Однако шлюзы входящих туннелей получают 8 ключей слоя в том порядке, в котором они должны быть зашифрованы (как описано выше). Для обеспечения возможности ответов запрос содержит случайный session tag и случайный session key, с помощью которых узел может использовать garlic encryption для своего решения, а также туннель, в который следует отправить этот garlic. В дополнение к вышеуказанной информации могут включаться различные специфичные для клиента параметры, такие как какие ограничения пропускной способности применить к туннелю, какие стратегии заполнения или пакетирования использовать и т.д.

После создания всех сообщений запроса они упаковываются с помощью garlic encryption для целевого router'а и отправляются через исследовательский tunnel. По получении узел определяет, может ли он или будет ли участвовать, создает ответное сообщение и как упаковывает его с помощью garlic encryption, так и направляет через tunnel с использованием предоставленной информации. По получении ответа создателем tunnel'я, tunnel считается действительным на данном участке (если принят). Как только все узлы дали согласие, tunnel становится активным.

### 3.3) Объединение в пулы {#tunnel.pooling}

Для обеспечения эффективной работы router поддерживает серию пулов tunnel, каждый из которых управляет группой tunnel, используемых для конкретной цели с собственной конфигурацией. Когда tunnel необходим для этой цели, router случайным образом выбирает один из соответствующего пула. В общем, существует два исследовательских пула tunnel - один входящий и один исходящий - каждый использует настройки исследования по умолчанию router'а. Кроме того, есть пара пулов для каждого локального назначения - один входящий и один исходящий tunnel. Эти пулы используют конфигурацию, указанную при подключении локального назначения к router'у, или настройки router'а по умолчанию, если не указано иное.

Каждый пул имеет в своей конфигурации несколько ключевых настроек, определяющих сколько tunnel поддерживать активными, сколько резервных tunnel содержать на случай отказа, как часто тестировать tunnel, какой длины должны быть tunnel, следует ли рандомизировать эти длины, как часто строить заменяющие tunnel, а также любые другие настройки, разрешенные при конфигурировании отдельных tunnel.

### 3.4) Альтернативы {#tunnel.building.alternatives}

#### 3.4.1) Телескопическое построение {#tunnel.building.telescoping}

Один вопрос, который может возникнуть относительно использования исследовательских tunnel для отправки и получения сообщений создания tunnel, заключается в том, как это влияет на уязвимость tunnel к атакам предшественников. Хотя конечные точки и gateway этих tunnel будут случайно распределены по сети (возможно, даже включая создателя tunnel в этот набор), другой альтернативой является использование самих путей tunnel для передачи запроса и ответа, как это делается в [TOR](https://www.torproject.org/). Это, однако, может привести к утечкам во время создания tunnel, позволяя узлам обнаружить, сколько хопов находится дальше в tunnel, отслеживая время или количество пакетов при построении tunnel. Можно использовать методы для минимизации этой проблемы, такие как использование каждого из хопов в качестве конечных точек (согласно [2.7.2](#tunnel.reroute)) для случайного количества сообщений перед продолжением построения следующего хопа.

#### 3.4.2) Неисследовательские tunnel для управления {#tunnel.building.nonexploratory}

Вторая альтернатива процесса построения туннелей заключается в том, чтобы предоставить router дополнительный набор неисследовательских входящих и исходящих пулов, используя их для запроса и ответа туннеля. Предполагая, что router имеет хорошо интегрированное представление о сети, это не должно быть необходимо, но если router был каким-то образом разделен, использование неисследовательских пулов для управления туннелями уменьшило бы утечку информации о том, какие узлы находятся в разделе router'а.

## 4) Ограничение пропускной способности tunnel {#tunnel.throttling}

Несмотря на то, что tunnel в I2P напоминают сеть с коммутацией каналов, все в I2P строго основано на сообщениях - tunnel являются лишь учетными приемами для организации доставки сообщений. Не делается никаких предположений относительно надежности или порядка сообщений, и повторные передачи остаются на усмотрение более высоких уровней (например, клиентской библиотеки потокового вещания I2P). Это позволяет I2P использовать методы регулирования пропускной способности, доступные как в сетях с коммутацией пакетов, так и с коммутацией каналов. Например, каждый router может отслеживать скользящее среднее объема данных, используемых каждым tunnel, объединять это со всеми средними значениями других tunnel, в которых участвует router, и на основе своей пропускной способности и загрузки принимать или отклонять дополнительные запросы на участие в tunnel. С другой стороны, каждый router может просто отбрасывать сообщения, превышающие его возможности, используя исследования, применяемые в обычном Интернете.

## 5) Смешивание/пакетирование {#tunnel.mixing}

Какие стратегии следует использовать на шлюзе и на каждом hop для задержки, переупорядочивания, перемаршрутизации или дополнения сообщений? В какой степени это должно делаться автоматически, сколько должно настраиваться как параметр для каждого tunnel или каждого hop, и как создатель tunnel (и, в свою очередь, пользователь) должен контролировать эту операцию? Все это остается неизвестным и будет проработано для будущего релиза.
