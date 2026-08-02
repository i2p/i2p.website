---
title: "SAMv3"
description: "Протокол простого анонимного обмена сообщениями для приложений I2P, не использующих Java"
slug: "samv3"
aliases:
  - "/docs/api/samv3"
  - "/docs/api/samv3/"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

SAM — это простой клиентский протокол для взаимодействия с I2P. SAM рекомендуется использовать в качестве протокола для приложений, не написанных на Java, чтобы подключаться к сети I2P, и поддерживается несколькими реализациями роутеров. Приложениям на Java следует использовать API потоковой передачи или I2CP напрямую.

Версия SAM 3 была представлена в релизе I2P 0.7.3 (май 2009 года) и является стабильным и поддерживаемым интерфейсом. Версия 3.1 также стабильна и поддерживает опцию типа подписи, что настоятельно рекомендуется. Более поздние версии 3.x поддерживают расширенные функции. Обратите внимание, что i2pd в настоящее время не поддерживает большинство функций версий 3.2 и 3.3.

Альтернативы: [SOCKS](/docs/api/socks), [Streaming](/docs/api/streaming), [I2CP](/docs/protocol/i2cp), [BOB (устаревший)](/docs/api/bob). Устаревшие версии: [SAM V1](/docs/api/sam), [SAM V2](/docs/api/samv2).

## Известные библиотеки SAM

Предупреждение: некоторые из них могут быть устаревшими или неподдерживаемыми. Никакие из них не тестируются, не проверяются и не поддерживаются проектом I2P, если ниже не указано иное. Проведите собственное исследование.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">STREAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DGRAM</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">RAW</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Site</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2psam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++, C wrapper</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2psam">github.com/i2p/i2psam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">gosam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/goSam">github.com/eyedeekay/goSam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/sam3">github.com/eyedeekay/sam3</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">onramp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/onramp">github.com/eyedeekay/onramp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">txi2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/str4d/txi2p">github.com/str4d/txi2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.socket</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/majestrate/i2p.socket">github.com/majestrate/i2p.socket</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/l-n-s/i2plib">github.com/l-n-s/i2plib</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib-fork</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://codeberg.org/weko/i2plib-fork">codeberg.org/weko/i2plib-fork</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/i2p-rs">github.com/i2p/i2p-rs</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">libsam3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/i2p/libsam3">github.com/i2p/libsam3</a><br>(Maintained by the I2P project)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/villain/mooni2p">notabug.org/villain/mooni2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">haskell-network-anonymous-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/solatis/haskell-network-anonymous-i2p">github.com/solatis/haskell-network-anonymous-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-sam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Typescript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/diva-exchange/i2p-sam">github.com/diva-exchange/i2p-sam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Javascript</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/redhog/node-i2p">github.com/redhog/node-i2p</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Jsam</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/eyedeekay/Jsam">github.com/eyedeekay/Jsam</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/MohA39/I2PSharp">github.com/MohA39/I2PSharp</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2pdotnet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">.Net</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">unk</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/SamuelFisher/i2pdotnet">github.com/SamuelFisher/i2pdotnet</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">i2p.rb</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ruby</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/dryruby/i2p.rb">github.com/dryruby/i2p.rb</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">solitude</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">WIP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/syvita/solitude">github.com/syvita/solitude</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Samty</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://notabug.org/acetone/samty">notabug.org/acetone/samty</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">bitcoin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">no</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><a href="https://github.com/bitcoin/bitcoin/blob/master/src/i2p.cpp">source (not a library, but good reference code)</a></td>
    </tr>
  </tbody>
</table>
## Быстрый старт

Для реализации базового приложения с использованием только TCP и архитектуры «равный к равному» клиент должен поддерживать следующие команды:

- `HELLO VERSION MIN=3.1 MAX=3.1` - Требуется для всех остальных команд
- `DEST GENERATE SIGNATURE_TYPE=7` - Для генерации нашего приватного ключа и дестинации
- `NAMING LOOKUP NAME=...` - Для преобразования .i2p адресов в дестинации
- `SESSION CREATE STYLE=STREAM ID=... DESTINATION=... i2cp.leaseSetEncType=6,4` - Требуется для команд STREAM CONNECT и STREAM ACCEPT
- `STREAM CONNECT ID=... DESTINATION=...` - Для исходящих соединений
- `STREAM ACCEPT ID=...` - Для приёма входящих соединений

## Общие рекомендации для разработчиков

### Дизайн приложения

Сессии SAM (или, внутри I2P, пулы туннелей или наборы туннелей) предназначены для длительного использования. Большинству приложений понадобится только одна сессия, создаваемая при запуске и закрываемая при выходе. I2P отличается от Tor, где цепи могут быстро создаваться и отбрасываться. Тщательно продумайте и проконсультируйтесь с разработчиками I2P, прежде чем проектировать своё приложение с использованием более одной-двух одновременных сессий или с быстрым созданием и удалением сессий. Большинству моделей угроз не требуется уникальная сессия для каждого соединения.

Кроме того, пожалуйста, убедитесь, что настройки вашего приложения (и инструкции для пользователей по настройке роутера, или настройки по умолчанию, если вы распространяете роутер совместно с приложением) обеспечивают вклад пользователей в сеть больших ресурсов, чем они потребляют. I2P — это одноранговая сеть, и сеть не сможет существовать, если популярное приложение будет вызывать постоянную перегрузку сети.

### Совместимость и тестирование

Реализации маршрутизаторов Java I2P и i2pd являются независимыми и имеют незначительные различия в поведении, поддержке функций и настройках по умолчанию. Пожалуйста, тестируйте ваше приложение с последней версией обоих маршрутизаторов.

i2pd SAM включён по умолчанию; SAM в Java I2P — нет. Предоставьте пользователям инструкции по включению SAM в Java I2P (через /configclients в консоли роутера) и/или выведите понятное сообщение об ошибке при неудачном первом подключении, например: «убедитесь, что I2P запущен и интерфейс SAM включён».

Маршрутизаторы Java I2P и i2pd используют разные значения количества туннелей по умолчанию. В Java значение по умолчанию — 2, а в i2pd — 5. Для большинства случаев с низким или средним уровнем пропускной способности и небольшим или средним количеством соединений достаточно 2 или 3 туннелей. Укажите требуемое количество туннелей в сообщении SESSION CREATE, чтобы обеспечить согласованную производительность с маршрутизаторами Java I2P и i2pd. См. ниже.

Более подробные рекомендации для разработчиков по обеспечению того, чтобы ваше приложение использовало только необходимые ему ресурсы, см. в [нашем руководстве по встраиванию I2P в ваше приложение](/docs/applications/embedding).

### Типы подписи и шифрования

I2P поддерживает несколько типов подписей и шифрования. Для обратной совместимости SAM по умолчанию использует старые и неэффективные типы, поэтому все клиенты должны указывать более новые типы.

Тип подписи указывается в командах DEST GENERATE и SESSION CREATE (для временных ключей). Все клиенты должны устанавливать `SIGNATURE_TYPE=7` (Ed25519).

Тип шифрования указывается в команде SESSION CREATE. Допускается использование нескольких типов шифрования. Клиентам следует установить либо `i2cp.leaseSetEncType=4` (только для ECIES-X25519), либо `i2cp.leaseSetEncType=6,4` (для MLKEM-768 и ECIES-X25519, для маршрутизаторов, поддерживающих API 0.9.67 или выше)

## Изменения в версии 3

### Изменения в версии 3.0

Версия 3.0 была представлена в релизе I2P 0.7.3. SAM v2 предоставил возможность управлять несколькими сокетами на одном и том же I2P-адресате *параллельно*, то есть клиенту не нужно было ждать успешной отправки данных через один сокет перед отправкой данных через другой. Однако все данные проходили через один и тот же сокет «клиент–SAM», что было довольно сложно для управления со стороны клиента.

SAM v3 управляет сокетами иным способом: каждый *I2P-сокет* соответствует уникальному клиентскому сокету SAM, что значительно упрощает обработку. Это похоже на [BOB](/docs/api/bob).

SAM v3 также предоставляет UDP-порт для отправки датаграмм через I2P и может пересылать входящие I2P-датаграммы на сервер датаграмм клиента.

### Изменения в версии 3.1

Версия 3.1 была представлена в релизе Java I2P 0.9.14 (июль 2014 г.). SAM 3.1 рекомендуется в качестве минимальной реализации SAM, поскольку она поддерживает более надёжные типы подписей по сравнению с SAM 3.0. i2pd также поддерживает большинство функций версии 3.1.

- DEST GENERATE и SESSION CREATE теперь поддерживают параметр SIGNATURE_TYPE.
- Параметры MIN и MAX в HELLO VERSION теперь являются необязательными.
- Параметры MIN и MAX в HELLO VERSION теперь поддерживают однозначные версии, такие как "3".
- RAW SEND теперь поддерживается на мостовом сокете.

### Изменения в версии 3.2

Версия 3.2 была представлена в Java I2P версии 0.9.24 (январь 2016). Обратите внимание, что i2pd в настоящее время не поддерживает большинство функций версии 3.2.

#### Поддержка портов и протоколов I2CP

- Параметры СОЗДАНИЯ СЕССИИ FROM_PORT и TO_PORT
- Параметр СЕССИИ СОЗДАНИЯ STYLE=RAW с опцией PROTOCOL
- Параметры ПОДКЛЮЧЕНИЯ ПОТОКА, ОТПРАВКИ ДЕЙТАГРАММЫ и ОТПРАВКИ RAW с опциями FROM_PORT и TO_PORT
- Параметр ОТПРАВКИ RAW с опцией PROTOCOL
- СОБЫТИЕ ПОЛУЧЕНИЯ ДЕЙТАГРАММЫ, ПОЛУЧЕНИЕ RAW, а также пересылаемые или полученные потоки и отвечаемые дейтаграммы включают FROM_PORT и TO_PORT
- Опция RAW-сессии HEADER=true приведёт к тому, что пересылаемые RAW-дейтаграммы будут начинаться со строки вида PROTOCOL=nnn FROM_PORT=nnnn TO_PORT=nnnn
- Первая строка дейтаграмм, отправляемых через порт 7655, теперь может начинаться с любой версии 3.x
- Первая строка дейтаграмм, отправляемых через порт 7655, может содержать любые из параметров FROM_PORT, TO_PORT, PROTOCOL
- СОБЫТИЕ ПОЛУЧЕНИЯ RAW включает PROTOCOL=nnn

#### SSL и аутентификация

- USER/PASSWORD в параметрах HELLO для авторизации. См. [ниже](#authorization).
- Необязательная настройка авторизации с помощью команды AUTH. См. [ниже](#authorization-configuration-sam-32-or-higher-optional-feature).
- Необязательная поддержка SSL/TLS на управляющем сокете. См. [ниже](#ssl).
- Опция STREAM FORWARD SSL=true

#### Многопоточность

- Параллельные ожидаемые STREAM ACCEPT разрешены для одного и того же идентификатора сессии.

#### Разбор командной строки и поддержание соединения

- Необязательные команды QUIT, STOP и EXIT для закрытия сессии и сокета. См. [ниже](#quitstopexitinvisible-sam-32-or-higher-optional-features).
- Разбор команд должен корректно обрабатывать UTF-8.
- Разбор команд надёжно обрабатывает пробелы внутри кавычек.
- Обратный слеш '\\' может экранировать кавычки в командной строке.
- Рекомендуется, чтобы сервер приводил команды к верхнему регистру для удобства тестирования через telnet.
- Пустые значения опций, такие как PROTOCOL или PROTOCOL=, могут разрешаться — зависит от реализации.
- Поддержка PING/PONG для поддержания соединения. См. ниже.
- Серверы могут реализовывать тайм-ауты для команды HELLO или последующих команд — зависит от реализации.

### Изменения в версии 3.3

Версия 3.3 была представлена в релизе Java I2P 0.9.25 (март 2016). Обратите внимание, что i2pd в настоящее время не поддерживает большинство функций версии 3.3.

- Одна и та же сессия может одновременно использоваться для потоков, датаграмм и RAW. Входящие пакеты и потоки будут направляться на основе протокола I2P и порта назначения (to-port). См. [раздел PRIMARY ниже](#sam-primary-sessions-v33-and-higher).
- DATAGRAM SEND и RAW SEND теперь поддерживают опции SEND_TAGS, TAG_THRESHOLD, EXPIRES и SEND_LEASESET. См. [раздел отправки датаграмм ниже](#sending-repliable-or-raw-datagrams).

### Изменения 2025-04

Два предложения были одобрены и включены в спецификацию в апреле 2025 года. Изменения версии для обозначения поддержки нет. Некоторые реализации пока не поддерживают, а в других реализациях поддержка является предварительной.

- Поддержка датаграмм 2/3 (предложение 163). Указывается в SESSION CREATE и SESSION ADD (подсессиях). См. ниже.
- Получение параметров leaseset (предложение 167). Задаётся с помощью NAMING LOOKUP OPTIONS=true. См. ниже.

## Протокол версии 3

### Обзор спецификации Simple Anonymous Messaging (SAM) версии 3.3

Клиентское приложение взаимодействует с мостом SAM, который обрабатывает всю функциональность I2P (используя [библиотеку потоков](/docs/api/streaming) для виртуальных потоков или напрямую [I2CP](/docs/protocol/i2cp) для датаграмм).

По умолчанию, соединение между клиентом и мостом SAM не шифруется и не проходит аутентификацию. Мост SAM может поддерживать SSL/TLS-соединения; настройка и детали реализации находятся за рамками данного документа. Начиная с версии SAM 3.2, в начальном рукопожатии поддерживаются необязательные параметры аутентификации — имя пользователя и пароль, которые могут потребоваться мостом.

Связь через I2P может принимать несколько различных форм:

- [Виртуальные потоки](/docs/api/streaming)
- [Ответные и аутентифицированные датаграммы](/docs/specs/datagrams#repliable) (сообщения с полем FROM)
- [Анонимные датаграммы](/docs/specs/datagrams#raw) (сырые анонимные сообщения)
- [Datagram2](/docs/specs/datagrams#datagram2) (новый ответный и аутентифицированный формат)
- [Datagram3](/docs/specs/datagrams#datagram3) (новый ответный, но неаутентифицированный формат)

Связь в I2P поддерживается через сессии I2P, и каждая сессия I2P привязана к адресу (называемому назначением). Сессия I2P связана с одним из трёх вышеперечисленных типов и не может передавать данные другого типа, если не используются [основные сессии](#sam-primary-sessions-v33-and-higher).

### Кодирование и экранирование

Все эти сообщения SAM отправляются в одной строке и завершаются символом новой строки (\\n). До версии SAM 3.2 поддерживался только 7-битный ASCII. Начиная с SAM 3.2, кодировка должна быть UTF-8. Должны работать любые ключи или значения, закодированные в UTF-8.

Форматирование, показанное в данной спецификации ниже, предназначено исключительно для удобства чтения, и, хотя первые два слова в каждом сообщении должны оставаться в строго определённом порядке, порядок пар «ключ=значение» может меняться (например, "ONE TWO A=B C=D" и "ONE TWO C=D A=B" — оба варианта являются корректными). Кроме того, протокол чувствителен к регистру символов. В приведённых далее примерах сообщения, отправляемые клиентом мосту SAM, обозначаются стрелкой "->", а сообщения, отправляемые мостом SAM клиенту — стрелкой "<-".

Базовая команда или строка ответа имеет одну из следующих форм:

```
COMMAND SUBCOMMAND [key=value] [key=value] ...
COMMAND                                           # As of SAM 3.2
PING[ arbitrary text]                             # As of SAM 3.2
PONG[ arbitrary text]                             # As of SAM 3.2
```
КОМАНДА без ПОДКОМАНДЫ поддерживается только для некоторых новых команд в SAM 3.2.

Пары ключ=значение должны быть разделены одним пробелом. (Начиная с SAM 3.2, разрешены несколько пробелов) Значения должны быть заключены в двойные кавычки, если они содержат пробелы, например: key="long value text". (До SAM 3.2 это работало ненадёжно в некоторых реализациях)

До SAM 3.2 не было механизма экранирования. Начиная с SAM 3.2, двойные кавычки можно экранировать обратной косой чертой '\\' и саму обратную косую черту можно представить как две обратные косые черты '\\\\'.

### Пустые значения

Начиная с SAM 3.2, пустые значения параметров, такие как KEY, KEY= или KEY="", могут разрешаться — это зависит от реализации.

### Чувствительность к регистру

Протокол, как указано, чувствителен к регистру. Рекомендуется, но не обязательно, чтобы сервер преобразовывал команды в верхний регистр для удобства тестирования через telnet. Это позволит, например, использовать команду "hello version". Это зависит от реализации. Не следует преобразовывать ключи или значения в верхний регистр, так как это может повредить параметры [I2CP](/docs/protocol/i2cp).

### Согласование соединения SAM

Обмен сообщениями SAM невозможен до тех пор, пока клиент и мост не договорятся о версии протокола, что осуществляется путём отправки клиентом сообщения HELLO, а мостом — ответа HELLO REPLY:

```
->  HELLO VERSION
          [MIN=$min]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [MAX=$max]            # Optional as of SAM 3.1, required for 3.0 and earlier
          [USER="xxx"]          # As of SAM 3.2, required if authentication is enabled, see below
          [PASSWORD="yyy"]      # As of SAM 3.2, required if authentication is enabled, see below
```
и

```
<-  HELLO REPLY RESULT=OK VERSION=3.1
```
Начиная с версии 3.1 (I2P 0.9.14), параметры MIN и MAX являются необязательными. SAM всегда возвращает максимально возможную версию с учётом ограничений MIN и MAX или текущую версию сервера, если ограничения не заданы.

Если мост SAM не может найти подходящую версию, он отвечает:

```
<- HELLO REPLY RESULT=NOVERSION
```
Если возникла ошибка, например, неверный формат запроса, возвращается:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
#### SSL

Контрольный сокет сервера может при необходимости поддерживать SSL/TLS, в зависимости от настроек сервера и клиента. Реализации могут также поддерживать и другие транспортные уровни; это выходит за рамки определения протокола.

#### Авторизация

Для авторизации клиент добавляет параметры USER="xxx" PASSWORD="yyy" к параметрам HELLO. Двойные кавычки для пользователя и пароля рекомендуются, но не обязательны. Двойная кавычка внутри имени пользователя или пароля должна быть экранирована обратным слэшем. В случае ошибки сервер ответит сообщением I2P_ERROR. Рекомендуется включать SSL на всех SAM-серверах, где требуется авторизация.

#### Таймауты

Серверы могут реализовывать тайм-ауты для команды HELLO или последующих команд, в зависимости от реализации. Клиенты должны оперативно отправлять команду HELLO и следующую команду после подключения.

Если тайм-аут возник до получения HELLO, мост отвечает:

```
<- HELLO REPLY RESULT=I2P_ERROR MESSAGE="$message"
```
а затем отключается.

Если тайм-аут происходит после получения HELLO, но до следующей команды, мост отвечает:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
а затем отключается.

### Порты и протокол I2CP

Начиная с SAM 3.2, клиент SAM может указать порты и протокол I2CP, которые будут переданы через I2CP, а мост SAM передаст клиенту SAM полученную информацию о портах и протоколе I2CP.

Для FROM_PORT и TO_PORT допустимый диапазон — 0-65535, значение по умолчанию — 0.

Для ПРОТОКОЛА, который может быть указан только для RAW, допустимый диапазон — 0–255, значение по умолчанию — 18.

Для команд SESSION указанные порты и протокол являются значениями по умолчанию для этой сессии. Для отдельных потоков или датаграмм указанные порты и протокол переопределяют значения по умолчанию сессии. Для полученных потоков или датаграмм указанные порты и протокол соответствуют тем, которые были получены через [I2CP](/docs/protocol/i2cp).

#### Важные различия от стандартного IP

Порты I2CP предназначены для сокетов и датаграмм I2P. Они не связаны с вашими локальными сокетами, подключающимися к SAM.

- Порт 0 является допустимым и имеет особое значение.
- Порты 1–1023 не являются специальными или привилегированными.
- Серверы по умолчанию слушают порт 0, что означает «все порты».
- Клиенты по умолчанию отправляют данные на порт 0, что означает «любой порт».
- Клиенты по умолчанию отправляют данные с порта 0, что означает «неуказанный».
- На серверах может быть сервис, прослушивающий порт 0, и другие сервисы, прослушивающие более высокие порты. В таком случае сервис на порту 0 считается основным и будет использоваться, если входящий порт сокета или датаграммы не соответствует другому сервису.
- На большинстве I2P-адресов запущена только одна служба, поэтому вы можете использовать значения по умолчанию и игнорировать настройку портов I2CP.
- Для указания портов I2CP требуется SAM 3.2 или 3.3.
- Если вам не нужны порты I2CP, вам не нужен SAM 3.2 или 3.3; достаточно версии 3.1.
- Протокол 0 является допустимым и означает «любой протокол». Это не рекомендуется и, скорее всего, работать не будет.
- I2P-сокеты отслеживаются по внутреннему идентификатору соединения. Следовательно, нет необходимости в уникальности 5-кортежа dest:port:dest:port:protocol. Например, может существовать несколько сокетов с одинаковыми портами между двумя адресами. Клиентам не нужно выбирать «свободный порт» для исходящего соединения.

Если вы разрабатываете приложение SAM 3.3 с несколькими подсессиями, тщательно продумайте, как эффективно использовать порты и протоколы. Дополнительную информацию см. в спецификации [I2CP](/docs/protocol/i2cp).

### Сессии SAM

Сеанс SAM создается, когда клиент открывает сокет к мосту SAM, выполняет рукопожатие и отправляет сообщение SESSION CREATE, а сеанс завершается при отключении сокета.

Каждый зарегистрированный адрес I2P однозначно связан с идентификатором сессии (или псевдонимом). Идентификаторы сессий, включая идентификаторы подсессий для ОСНОВНЫХ сессий, должны быть глобально уникальными на сервере SAM. Во избежание возможных конфликтов идентификаторов с другими клиентами, рекомендуется, чтобы клиент генерировал идентификаторы случайным образом.

Каждая сессия уникально связана с:

- сокет, через который клиент создаёт сессию
- его ID (или никнейм)

#### Запрос на создание сессии

Сообщение создания сеанса может использовать только одну из этих форм (сообщения, полученные в других формах, отвечаются сообщением об ошибке):

```
->  SESSION CREATE
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, for DESTINATION=TRANSIENT only, default DSA_SHA1
          [PORT=$port]                         # Required for DATAGRAM* RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [HEADER={true,false}]                # SAM 3.2 or higher only, for STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
DESTINATION указывает, какой адрес следует использовать для отправки и получения сообщений/потоков. Значение $privkey представляет собой строку в кодировке base64, полученную путём конкатенации [Destination](/docs/specs/common-structures#type_Destination), за которым следует [Private Key](/docs/specs/common-structures#type_PrivateKey), затем [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), и, опционально, [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), который занимает 663 или более байт в бинарном виде и 884 или более байт в кодировке base64, в зависимости от типа подписи. Бинарный формат описан в разделе Private Key File. Дополнительные сведения о [Private Key](/docs/specs/common-structures#type_PrivateKey) см. в разделе ниже «Генерация ключей адреса».

Если закрытый ключ подписи состоит из одних нулей, следует раздел [Офлайн-подписи](/docs/specs/common-structures#struct_OfflineSignature). Офлайн-подписи поддерживаются только для STREAM и RAW сессий. Офлайн-подписи нельзя создавать с параметром DESTINATION=TRANSIENT. Формат раздела офлайн-подписи следующий:

1. Отметка времени истечения (4 байта, big endian, секунды с эпохи, переполнение в 2106 году)
2. Тип подписи временного публичного ключа (2 байта, big endian)
3. Временный публичный ключ подписи (длина определяется типом временной подписи)
4. Подпись вышеуказанных трех полей оффлайн-ключом (длина определяется типом подписи назначения)
5. Временный приватный ключ подписи (д游戏副本 определяется типом временной подписи)

Если назначение указано как TRANSIENT, мост SAM создает новое назначение. Начиная с версии 3.1 (I2P 0.9.14), если назначение является TRANSIENT, поддерживается необязательный параметр SIGNATURE_TYPE. Значение SIGNATURE_TYPE может быть любым именем (например, ECDSA_SHA256_P256, без учета регистра) или числом (например, 1), поддерживаемым [Key Certificates](/docs/specs/common-structures#type_Certificate). По умолчанию используется DSA_SHA1, что НЕ является желаемым вариантом. Для большинства приложений, пожалуйста, укажите SIGNATURE_TYPE=7.

$nickname выбирается клиентом. Пробелы не допускаются.

Дополнительные параметры, если они не интерпретируются SAM-мостом (например, outbound.length=0), передаются в конфигурацию сеанса I2P.

Маршрутизаторы Java I2P и i2pd используют разные значения количества туннелей по умолчанию. В Java значение по умолчанию — 2, а в i2pd — 5. Для большинства случаев с низким или средним уровнем пропускной способности и небольшим или средним количеством соединений достаточно 2 или 3 туннелей. Укажите количество туннелей в сообщении SESSION CREATE, чтобы обеспечить согласованную производительность с маршрутизаторами Java I2P и i2pd, используя параметры, например: inbound.quantity=3 outbound.quantity=3. Эти и другие параметры [задокументированы в приведённых ниже ссылках](#tunnel-i2cp-and-streaming-options).

Сам SAM-мост уже должен быть настроен на взаимодействие с определённым роутером через I2P (хотя при необходимости может существовать способ задать параметры вручную, например i2cp.tcp.host=localhost и i2cp.tcp.port=7654).

#### Ответ на создание сессии

После получения сообщения о создании сеанса, мост SAM ответит сообщением о состоянии сеанса, следующего вида:

Если создание прошло успешно:

```
<-  SESSION STATUS RESULT=OK DESTINATION=$privkey
```
$privkey — это base64-кодированная конкатенация [Destination](/docs/specs/common-structures#type_Destination), за которой следует [Private Key](/docs/specs/common-structures#type_PrivateKey), затем [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) и, опционально, [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature). В бинарном виде это 663 или более байт, а в base64 — 884 или более байт, в зависимости от типа подписи. Бинарный формат описан в Private Key File.

Если в SESSION CREATE содержался закрытый ключ подписи, состоящий из одних нулей, и раздел [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature), ответ SESSION STATUS будет включать те же данные в том же формате. Подробности см. в разделе SESSION CREATE выше.

Если ник уже связан с сессией:

```
<-  SESSION STATUS RESULT=DUPLICATED_ID
```
Если адрес уже используется:

```
<-  SESSION STATUS RESULT=DUPLICATED_DEST
```
Если адрес назначения не является действительным закрытым ключом адреса:

```
<-  SESSION STATUS RESULT=INVALID_KEY
```
Если произошла другая ошибка:

```
<-  SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
Если состояние не является удовлетворительным, поле MESSAGE должно содержать информацию, понятную человеку, с объяснением, почему сеанс не может быть создан.

Обратите внимание, что маршрутизатор строит туннели до отправки ответа SESSION STATUS. Это может занять несколько секунд, а при запуске маршрутизатора или сильной сетевой перегрузке — минуту или более. Если построение туннелей не удалось, маршрутизатор не отправит сообщение об ошибке в течение нескольких минут. Не устанавливайте короткий таймаут ожидания ответа. Не покидайте сессию во время построения туннелей и не пытайтесь перезапустить её заново.

Сессии SAM существуют и завершаются вместе с сокетом, с которым они связаны. Когда сокет закрывается, сессия завершается, и все соединения, использующие эту сессию, также прекращаются одновременно. И наоборот, когда сессия завершается по любой причине, мост SAM закрывает сокет.

### Виртуальные потоки SAM

Виртуальные потоки гарантированно отправляются надежно и в правильном порядке, с уведомлением об успехе или неудаче сразу же, как только такая информация становится доступна.

Потоки представляют собой двунаправленные коммуникационные сокеты между двумя адресами I2P, но их открытие должно быть инициировано одной из сторон. Далее команды CONNECT используются клиентом SAM для отправки такого запроса. Команды FORWARD / ACCEPT используются клиентом SAM, когда он хочет ожидать запросы от других адресов I2P.

### Виртуальные потоки SAM: CONNECT

Клиент запрашивает подключение следующим образом:

- открытие нового сокета через мост SAM
- передача того же приветственного handshake-сообщения, что и выше
- отправка команды STREAM CONNECT

#### Запрос подключения

```
-> STREAM CONNECT
         ID=$nickname
         DESTINATION=$destination
         [SILENT={true,false}]                # default false
         [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
         [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
```
Это устанавливает новое виртуальное соединение от локальной сессии с идентификатором $nickname к указанному пику.

Цель — $destination, представляющая собой base64-кодировку [Destination](/docs/specs/common-structures#type_Destination), которая состоит из 516 или более символов base64 (387 или более байт в бинарном виде), в зависимости от типа подписи.

**ПРИМЕЧАНИЕ:** Начиная примерно с 2014 года (SAM v3.1), Java I2P также поддерживает доменные имена и b32-адреса для параметра $destination, однако ранее это не было задокументировано. Начиная с версии 0.9.48, Java I2P официально поддерживает доменные имена и b32-адреса. Маршрутизатор i2pd поддерживает доменные имена и b32-адреса начиная с версии 2.38.0 (0.9.50). В обоих маршрутизаторах поддержка «b32» включает расширенные «b33»-адреса для скрытых назначений.

#### Ответ на подключение

Если передано SILENT=true, мост SAM не будет отправлять никаких других сообщений через сокет. Если подключение не удастся, сокет будет закрыт. Если подключение успешно, все остальные данные, передаваемые через текущий сокет, будут пересылаться туда и обратно от подключенного I2P-пира-получателя.

Если SILENT=false, что является значением по умолчанию, SAM-мост отправляет последнее сообщение своему клиенту перед пересылкой или завершением работы сокета:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Значение RESULT может быть одним из следующих:

```
OK
CANT_REACH_PEER
I2P_ERROR
INVALID_KEY
INVALID_ID
TIMEOUT
```
Если РЕЗУЛЬТАТ равен OK, все остальные данные, передаваемые через текущий сокет, пересылаются в подключённый пир I2P и обратно. Если подключение было невозможно (таймаут и т.д.), РЕЗУЛЬТАТ будет содержать соответствующее значение ошибки (с необязательным понятным человеку СООБЩЕНИЕМ), и мост SAM закрывает сокет.

Внутренний таймаут подключения потока маршрутизатора составляет примерно одну минуту и зависит от реализации. Не устанавливайте более короткий таймаут ожидания ответа.

### Виртуальные потоки SAM: ПРИНЯТЬ

Клиент ожидает входящий запрос соединения путем:

- открытие нового сокета через мост SAM
- передача того же приветственного сообщения HELLO, что и выше
- отправка команды STREAM ACCEPT

#### Принять запрос

```
-> STREAM ACCEPT
         ID=$nickname
         [SILENT={true,false}]                # default false
```
Это заставляет сеанс ${nickname} ожидать одного входящего запроса на подключение из сети I2P. ACCEPT не разрешён, пока в сеансе активен FORWARD.

Начиная с SAM 3.2, разрешено несколько одновременных ожидающих STREAM ACCEPT для одного и того же идентификатора сессии (даже с одним и тем же портом). До версии 3.2 одновременные запросы завершались ошибкой ALREADY_ACCEPTING. Примечание: Java I2P также поддерживает одновременные ACCEPT в SAM 3.1, начиная с версии 0.9.24 (2016-01). i2pd также поддерживает одновременные ACCEPT в SAM 3.1, начиная с версии 2.50.0 (2023-12).

#### Принять ответ

Если передано SILENT=true, мост SAM не будет отправлять никаких других сообщений через сокет. Если accept завершится неудачно, сокет будет закрыт. Если accept выполнен успешно, все остальные данные, проходящие через текущий сокет, будут пересылаться в подключенный I2P-пир и от него. Для надёжности и получения адреса для входящих соединений рекомендуется использовать SILENT=false.

Если SILENT=false, что является значением по умолчанию, мост SAM отвечает:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Значение RESULT может быть одним из следующих:

```
OK
I2P_ERROR
INVALID_ID
```
Если результат не является OK, сокет немедленно закрывается мостом SAM. Если результат OK, мост SAM начинает ожидание входящего запроса соединения от другого узла I2P. Когда запрос поступает, мост SAM принимает его и:

Если передано SILENT=true, мост SAM не будет отправлять никаких других сообщений через клиентский сокет. Все остальные данные, передаваемые через текущий сокет, пересылаются от и к подключенному I2P-партнёру назначения.

Если передано значение SILENT=false, которое является значением по умолчанию, мост SAM отправляет клиенту ASCII-строку, содержащую публичный ключ назначения (base64) запрашивающего узла, а также дополнительную информацию, только для SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
После этой строки, завершённой '\\n', все остальные данные, передаваемые через текущий сокет, пересылаются от и к подключенному I2P-партнёру, пока один из партнёров не закроет сокет.

#### Ошибки после OK

В редких случаях мост SAM может столкнуться с ошибкой после отправки RESULT=OK, но до поступления соединения и отправки клиенту строки $destination. Эти ошибки могут включать завершение работы маршрутизатора, перезагрузку маршрутизатора и закрытие сессии. В таких случаях, когда SILENT=false, мост SAM может (но не обязан — зависит от реализации) отправить строку:

```
<-  STREAM STATUS
         RESULT=I2P_ERROR
         [MESSAGE=...]
```
перед немедленным закрытием сокета. Эта строка, конечно, не может быть декодирована как валидный Base 64 адрес.

### Виртуальные потоки SAM: FORWARD

Клиент может использовать обычный сокет-сервер и ожидать запросы подключений из I2P. Для этого клиент должен:

- открыть новый сокет с мостом SAM
- передать тот же HELLO-рукопожатие, что указано выше
- отправить команду пересылки

#### Запрос пересылки

```
-> STREAM FORWARD
         ID=$nickname
         PORT=$port
         [HOST=$host]
         [SILENT={true,false}]                # default false
         [SSL={true,false}]                   # SAM 3.2 or higher only, default false
```
Это позволяет сеансу ${nickname} ожидать входящие запросы на подключение из сети I2P. Действие FORWARD не разрешено, пока в сеансе имеется ожидающий запрос ACCEPT.

#### Прямой ответ

SILENT по умолчанию имеет значение false. Независимо от того, установлено ли значение SILENT в true или false, мост SAM всегда отвечает сообщением STREAM STATUS. Обратите внимание, что это отличается от поведения STREAM ACCEPT и STREAM CONNECT при SILENT=true. Сообщение STREAM STATUS выглядит следующим образом:

```
<-  STREAM STATUS
         RESULT=$result
         [MESSAGE=...]
```
Значение RESULT может быть одним из следующих:

```
OK
I2P_ERROR
INVALID_ID
```
$host — это имя хоста или IP-адрес сервера сокета, на который SAM будет перенаправлять запросы на подключение. Если не указано, SAM использует IP-адрес сокета, отправившего команду перенаправления.

$port — это номер порта сервера сокетов, на который SAM будет перенаправлять запросы подключения. Указание порта обязательно.

Когда запрос на подключение поступает из I2P, мост SAM устанавливает сокет-соединение с $host:$port. Если соединение принимается менее чем за 3 секунды, SAM принимает соединение из I2P, после чего:

Если передано SILENT=true, все данные, проходящие через полученный текущий сокет, пересылаются от и к подключенному I2P-партнеру назначения.

Если передано значение SILENT=false, которое является значением по умолчанию, мост SAM отправляет по полученному сокету ASCII-строку, содержащую публичный ключ базы64 запрашивающего пира, а также дополнительную информацию, относящуюся только к SAM 3.2:

```
$destination
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
```
После этой строки, завершаемой '\\n', все остальные данные, передаваемые через сокет, пересылаются в подключенный пир I2P и обратно, пока одна из сторон не закроет сокет.

Начиная с SAM 3.2, если указано SSL=true, пересылающий сокет работает через SSL/TLS.

Маршрутизатор I2P прекратит прослушивание входящих запросов на подключение, как только сокет "forwarding" будет закрыт.

### SAM Datagrams

SAMv3 предоставляет механизмы для отправки и получения датаграмм через локальные датаграммные сокеты. Некоторые реализации SAMv3 также поддерживают устаревший способ v1/v2 отправки/приема датаграмм через сокет моста SAM. Оба способа документированы ниже.

I2P поддерживает четыре типа датаграмм:

- Датаграммы с возможностью ответа и аутентификацией имеют префикс с адресом отправителя и содержат подпись отправителя, чтобы получатель мог проверить, что адрес отправителя не подделан, и мог ответить на датаграмму. Новый формат Datagram2 также поддерживает ответ и аутентификацию.
- Новый формат Datagram3 поддерживает ответ, но не аутентифицирует отправителя. Информация об отправителе не проверяется.
- Сырые датаграммы не содержат адреса отправителя и подписи.

Порты I2CP по умолчанию определены как для repliable, так и для raw datagram. Порт I2CP может быть изменён для raw datagram.

Распространённой практикой проектирования протоколов является отправка ответных датаграмм на серверы с включением идентификатора, а сервер отвечает «голой» датаграммой, содержащей этот идентификатор, чтобы ответ можно было сопоставить с запросом. Такой подход исключает значительные накладные расходы, связанные с использованием ответных датаграмм в ответах. Все выборы протоколов и портов I2CP зависят от конкретного приложения, и разработчики должны учитывать эти аспекты.

См. также важные примечания о MTU датаграммы в разделе ниже.

#### Отправка реплицируемых или необработанных датаграмм

Хотя в I2P изначально не содержится адрес ОТПРАВИТЕЛЯ (FROM), для удобства использования предусмотрен дополнительный уровень в виде отвечаемых датаграмм — неупорядоченных и ненадёжных сообщений объёмом до 31744 байт, включающих адрес отправителя (с оставлением до 1 КБ для заголовков). Этот адрес отправителя аутентифицируется внутри SAM (с использованием ключа подписи получателя для проверки источника) и включает защиту от повторного воспроизведения (replay prevention).

Минимальный размер составляет 1. Для наилучшей надежности доставки рекомендуемый максимальный размер составляет приблизительно 11 КБ. Надежность обратно пропорциональна размеру сообщения, возможно, даже экспоненциально.

После установления сеанса SAM с параметром STYLE=DATAGRAM или STYLE=RAW клиент может отправлять ответные или сырые датаграммы через UDP-порт SAM (по умолчанию 7655).

Первая строка датаграммы, отправленной через этот порт, должна иметь следующий формат. Это всё одна строка (с разделителями-пробелами), показанная в нескольких строках для ясности:

```
3.0                                  # As of SAM 3.2, any "3.x" is allowed. Prior to that, "3.0" is required.
$nickname
$destination
[FROM_PORT=nnn]                      # SAM 3.2 or higher only, default from session options
[TO_PORT=nnn]                        # SAM 3.2 or higher only, default from session options
[PROTOCOL=nnn]                       # SAM 3.2 or higher only, only for RAW sessions, default from session options
[SEND_TAGS=nnn]                      # SAM 3.3 or higher only, number of session tags to send
                                     # Overrides crypto.tagsToSend I2CP session option
                                     # Default is router-dependent (40 for Java router)
[TAG_THRESHOLD=nnn]                  # SAM 3.3 or higher only, low session tag threshold
                                     # Overrides crypto.lowTagThreshold I2CP session option
                                     # Default is router-dependent (30 for Java router)
[EXPIRES=nnn]                        # SAM 3.3 or higher only, expiration from now in seconds
                                     # Overrides clientMessageTimeout I2CP session option (which is in ms)
                                     # Default is router-dependent (60 for Java router)
[SEND_LEASESET={true,false}]         # SAM 3.3 or higher only, whether to send our leaseset
                                     # Overrides shouldBundleReplyInfo I2CP session option
                                     # Default is true
\n
```
- 3.0 — это версия SAM. Начиная с SAM 3.2, разрешена любая версия 3.x.
- $nickname — идентификатор сессии DATAGRAM, который будет использоваться
- Пункт назначения — это $destination, представляющий собой base64-кодировку [Destination](/docs/specs/common-structures#type_Destination), которая состоит из 516 или более символов в формате base64 (387 или более байт в двоичном виде), в зависимости от типа подписи. **ПРИМЕЧАНИЕ:** С примерно 2014 года (SAM v3.1) Java I2P также поддерживает доменные имена и b32-адреса для параметра $destination, однако ранее эта возможность не была задокументирована. Начиная с выпуска 0.9.48, доменные имена и b32-адреса официально поддерживаются Java I2P. В настоящее время маршрутизатор i2pd не поддерживает доменные имена и b32-адреса; поддержка может быть добавлена в будущих версиях.
- Все опции являются настройками, применяемыми к каждому дейтаграммному сообщению, и переопределяют значения по умолчанию, указанные в команде SESSION CREATE.
- Опции версии 3.3 SEND_TAGS, TAG_THRESHOLD, EXPIRES и SEND_LEASESET будут переданы в [I2CP](/docs/protocol/i2cp), если они поддерживаются. Подробности см. в [спецификации I2CP](/docs/protocol/i2cp#msg_SendMessageExpire). Поддержка этих опций со стороны сервера SAM является необязательной; сервер проигнорирует их, если они не поддерживаются.
- данная строка завершается символом '\\n'.

Первая строка будет отброшена SAM до отправки оставшихся данных сообщения указанному получателю.

Для альтернативного метода отправки ответных и необработанных датаграмм см. [DATAGRAM SEND и RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### SAM Repliable Datagrams: Получение датаграммы

Полученные датаграммы записываются SAM в сокет, из которого была открыта сессия датаграммы, если в команде SESSION CREATE не указан порт пересылки. Это совместимый со способ v1/v2 способ получения датаграмм.

Когда приходит датаграмма, мост передает её клиенту через сообщение:

```
<-  DATAGRAM RECEIVED
           DESTINATION=$destination           # See notes below for Datagram3 format
           SIZE=$numBytes
           FROM_PORT=nnn                      # SAM 3.2 or higher only
           TO_PORT=nnn                        # SAM 3.2 or higher only
           \n
       [$numBytes of data]
```
Источник — это $destination, который представляет собой base64-кодировку [Destination](/docs/specs/common-structures#type_Destination), состоящую из 516 или более символов base64 (387 или более байт в двоичном виде), в зависимости от типа подписи.

Мост SAM никогда не передает клиенту заголовки аутентификации или другие поля, а лишь данные, предоставленные отправителем. Это продолжается до тех пор, пока сеанс не будет закрыт (клиентом путем разрыва соединения).

#### Пересылка необработанных или поддающихся повторной передаче датаграмм

При создании сеанса датаграммы клиент может попросить SAM пересылать входящие сообщения на указанный ip:порт. Для этого он отправляет команду CREATE с параметрами PORT и HOST:

```
-> SESSION CREATE
          STYLE={DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See below for DATAGRAM2/3
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          PORT=$port
          [HOST=$host]
          [FROM_PORT=nnn]                      # SAM 3.2 or higher only, default 0
          [TO_PORT=nnn]                        # SAM 3.2 or higher only, default 0
          [PROTOCOL=nnn]                       # SAM 3.2 or higher only, for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP options
```
$privkey — это base64-кодированная конкатенация [Destination](/docs/specs/common-structures#type_Destination), за которой следует [Private Key](/docs/specs/common-structures#type_PrivateKey), затем [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey) и, опционально, [Offline Signature](/docs/specs/common-structures#struct_OfflineSignature). В итоге получается строка длиной 884 или более символов в кодировке base64 (663 или более байт в бинарном виде), в зависимости от типа подписи. Бинарный формат описан в разделе Private Key File.

Офлайн-подписи поддерживаются для датаграмм RAW, DATAGRAM2 и DATAGRAM3, но не для DATAGRAM. Подробности см. в разделе СОЗДАНИЕ СЕССИИ выше и в разделе DATAGRAM2/3 ниже.

$host — это имя хоста или IP-адрес сервера датаграмм, на который SAM будет пересылать датаграммы. Если не указано, SAM использует IP-адрес сокета, отправившего команду пересылки.

$port — это номер порта датаграммного сервера, на который SAM будет пересылать датаграммы. Если $port не задан, датаграммы НЕ будут пересылаться, они будут приниматься на управляющем сокете способом, совместимым с v1/v2.

Дополнительные опции передаются в конфигурацию сеанса I2P, если они не интерпретируются SAM-мостом (например, outbound.length=0). Эти опции [задокументированы ниже](#tunnel-i2cp-and-streaming-options).

Пересылаемые датаграммы с ответом всегда имеют префикс в виде base64-адресата, за исключением Datagram3, см. ниже. Когда приходит датаграмма с ответом, мост отправляет на указанный хост:порт UDP-пакет, содержащий следующие данные:

```
$destination                       # See notes below for Datagram3 format
FROM_PORT=nnn                      # SAM 3.2 or higher only
TO_PORT=nnn                        # SAM 3.2 or higher only
\n
$datagram_payload
```
Пересылаемые необработанные датаграммы передаются «как есть» на указанный хост:порт без префикса. Пакет UDP содержит следующие данные:

```
$datagram_payload
```
Начиная с SAM 3.2, когда в команде SESSION CREATE указан параметр HEADER=true, в начало пересылаемого необработанного датаграммы будет добавлена строка заголовка следующего вида:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
$destination — это base64-представление [Destination](/docs/specs/common-structures#type_Destination), состоящее из 516 или более символов base64 (387 или более байт в бинарном виде), в зависимости от типа подписи.

#### SAM Анонимные (сырые) датаграммы

SAM позволяет клиентам максимально эффективно использовать пропускную способность I2P, отправляя и получая анонимные датаграммы, при этом аутентификация и информация для ответа остаются на усмотрение самого клиента. Эти датаграммы являются ненадёжными и неупорядоченными, и могут иметь размер до 32768 байт.

Минимальный размер — 1. Для максимальной надежности доставки рекомендуемый максимальный размер составляет примерно 11 КБ.

После установки сеанса SAM с параметром STYLE=RAW клиент может отправлять анонимные датаграммы через мост SAM точно таким же образом, как и [отправка отвечаемых датаграмм](#sending-repliable-or-raw-datagrams).

Оба способа получения датаграмм также доступны для анонимных датаграмм.

Полученные датаграммы записываются SAM в сокет, из которого была открыта сессия датаграммы, если в команде SESSION CREATE не указан порт пересылки. Это совместимый со способ v1/v2 способ получения датаграмм.

```
<- RAW RECEIVED
          SIZE=$numBytes
          FROM_PORT=nnn                      # SAM 3.2 or higher only
          TO_PORT=nnn                        # SAM 3.2 or higher only
          PROTOCOL=nnn                       # SAM 3.2 or higher only
          \n
      [$numBytes of data]
```
Когда анонимные датаграммы должны быть пересланы на определенный хост:порт, мост отправляет на указанный хост:порт сообщение, содержащее следующие данные:

```
$datagram_payload
```
Начиная с SAM 3.2, когда в команде SESSION CREATE указан параметр HEADER=true, в начало пересылаемого необработанного датаграммы будет добавлена строка заголовка следующего вида:

```
FROM_PORT=nnn
TO_PORT=nnn
PROTOCOL=nnn
\n
$datagram_payload
```
Для альтернативного метода отправки анонимных датаграмм см. [RAW SEND](#datagram-send-raw-send-v1v2-compatible-datagram-handling).

#### Дейтаграмма 2/3

Datagram 2/3 — это новые форматы, определённые в начале 2025 года. На данный момент известных реализаций не существует. Проверьте документацию реализации для получения актуального статуса. Смотрите [спецификацию](/docs/specs/datagrams) для дополнительной информации.

В настоящее время нет планов по увеличению версии SAM для указания поддержки Datagram 2/3. Это может быть проблематично, поскольку реализации могут хотеть поддерживать Datagram 2/3, но не поддерживать функции SAM v3.3. Любое изменение версии остаётся неопределённым (TBD).

Datagram2 и Datagram3 поддерживают ответы. Только Datagram2 является аутентифицированным.

Datagram2 идентичен repliable datagrams с точки зрения SAM. Оба являются аутентифицированными. Отличаются только формат I2CP и подпись, но это не видно клиентам SAM. Datagram2 также поддерживает офлайн-подписи, поэтому может использоваться офлайн-подписанными адресатами.

Предназначение Datagram2 — заменить Repliable-датаграммы для новых приложений, которым не требуется обратная совместимость. Datagram2 обеспечивает защиту от повторного воспроизведения, которой нет у Repliable-датаграмм. Если требуется обратная совместимость, приложение может поддерживать как Datagram2, так и Repliable, используя одну и ту же сессию с PRIMARY-сессиями SAM 3.3.

Datagram3 поддерживает ответ, но не аутентифицирован. Поле 'from' в формате I2CP — это хэш, а не назначение. $destination, отправляемый сервером SAM клиенту, будет 44-символьным base64 хэшем. Чтобы преобразовать его в полный адрес для ответа, декодируйте из base64 в 32-байтный двоичный формат, затем закодируйте в base32 в строку из 52 символов и добавьте ".b32.i2p" для NAMING LOOKUP. Как обычно, клиентам следует вести собственный кэш, чтобы избежать повторных запросов NAMING LOOKUP.

Разработчики приложений должны проявлять особую осторожность и учитывать последствия для безопасности неподтверждённых датаграмм.

#### Соображения по MTU датаграммы V3

Дейтаграммы I2P могут быть больше типичного интернет-MTU в 1500 байт. Локально отправляемые дейтаграммы и пересылаемые дейтаграммы с ответом, начинающиеся с 516-байтного и более base64-представления адресата, вероятно, превысят этот MTU. Однако, MTU для localhost в системах Linux обычно намного больше, например, 65536. Значение MTU для localhost зависит от операционной системы. Дейтаграммы I2P никогда не будут превышать размера в 65536 байт. Размер дейтаграммы зависит от протокола приложения.

Если SAM-клиент находится локально по отношению к SAM-серверу и система поддерживает больший MTU, то датаграммы не будут фрагментироваться локально. Однако, если SAM-клиент является удалённым, датаграммы IPv4 будут фрагментированы, а датаграммы IPv6 завершатся ошибкой (IPv6 не поддерживает фрагментацию UDP).

Разработчики клиентских библиотек и приложений должны быть осведомлены об этих проблемах и документировать рекомендации по предотвращению фрагментации и потери пакетов, особенно при удалённых подключениях клиента и сервера SAM.

#### ОТПРАВКА ДАТАГРАММ, СЫРАЯ ОТПРАВКА (обработка датаграмм, совместимая с V1/V2)

В SAM V3 предпочтительный способ отправки датаграмм — через датаграммный сокет на порту 7655, как описано выше. Однако датаграммы с поддержкой ответа можно отправлять напрямую через сокет моста SAM с использованием команды DATAGRAM SEND, как описано в [SAM V1](/docs/api/sam) и [SAM V2](/docs/api/samv2).

Начиная с версии 0.9.14 (версия 3.1), анонимные датаграммы можно отправлять напрямую через сокет моста SAM с помощью команды RAW SEND, как описано в [SAM V1](/docs/api/sam) и [SAM V2](/docs/api/samv2).

Начиная с версии 0.9.24 (версия 3.2), команды DATAGRAM SEND и RAW SEND могут включать параметры FROM_PORT=nnnn и/или TO_PORT=nnnn для переопределения портов по умолчанию. Начиная с версии 0.9.24 (версия 3.2), команда RAW SEND может включать параметр PROTOCOL=nnn для переопределения протокола по умолчанию.

Эти команды *не* поддерживают параметр ID. Дейтаграммы отправляются в сессию типа DATAGRAM или RAW, которая была создана последней, в зависимости от ситуации. Поддержка параметра ID может быть добавлена в одной из будущих версий.

Форматы DATAGRAM2 и DATAGRAM3 *не* поддерживаются совместимым образом с V1/V2.

### Основные сессии SAM (V3.3 и выше)

*Версия 3.3 была представлена в релизе I2P 0.9.25.*

*В более ранней версии данной спецификации PRIMARY-сессии назывались MASTER-сессиями. В `i2pd` и `I2P+` они по-прежнему известны исключительно как MASTER-сессии.*

SAM v3.3 добавляет поддержку запуска потоковой передачи, датаграмм и необработанных подсессий в одной основной сессии, а также возможность запуска нескольких подсессий одного типа. Весь трафик подсессий использует одно и то же назначение или набор туннелей. Маршрутизация трафика в I2P основывается на параметрах порта и протокола подсессий.

Чтобы создать мультиплексированные подсессии, вы должны создать основную сессию, а затем добавить подсессии к основной сессии. Каждая подсессия должна иметь уникальный идентификатор и уникальный протокол и порт прослушивания. Подсессии также могут быть удалены из основной сессии.

С основной сессией и комбинацией подсессий клиент SAM может поддерживать несколько приложений или одно сложное приложение, использующее различные протоколы, на одном наборе туннелей. Например, клиент BitTorrent может настроить потоковую подсессию для одноранговых соединений, а также подсессии datagram и raw для взаимодействия через DHT.

#### Создание ОСНОВНОЙ сессии

```
->  SESSION CREATE
          STYLE=PRIMARY                        # prior to 0.9.47, use STYLE=MASTER
          ID=$nickname
          DESTINATION={$privkey,TRANSIENT}
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Мост SAM ответит об успехе или неудаче, как указано в [ответе на стандартное создание сессии](#session-creation-response).

Не устанавливайте параметры PORT, HOST, FROM_PORT, TO_PORT, PROTOCOL, LISTEN_PORT, LISTEN_PROTOCOL или HEADER для основной сессии. Вы не можете отправлять данные через основной идентификатор сессии или через управляющий сокет. Все команды, такие как STREAM CONNECT, DATAGRAM SEND и т.д., должны использовать идентификатор подсессии на отдельном сокете.

Основная сессия подключается к маршрутизатору и создает туннели. Когда мост SAM отвечает, туннели уже построены, и сессия готова к добавлению подсессий. Все параметры [I2CP](/docs/protocol/i2cp), касающиеся параметров туннелей, такие как длина, количество и псевдоним, должны быть указаны при создании основной сессии (SESSION CREATE).

Все служебные команды поддерживаются в основной сессии.

Когда основная сессия закрывается, все подсессии также закрываются.

ПРИМЕЧАНИЕ: До выпуска 0.9.47 используйте STYLE=MASTER. Начиная с выпуска 0.9.47 поддерживается STYLE=PRIMARY. Для обратной совместимости MASTER по-прежнему поддерживается.

#### Создание подсессии

Используя тот же сокет управления, на котором была создана ОСНОВНАЯ сессия:

```
->  SESSION ADD
          STYLE={STREAM,DATAGRAM,RAW,DATAGRAM2,DATAGRAM3}   # See above for DATAGRAM2/3
          ID=$nickname                         # must be unique
          [PORT=$port]                         # Required for DATAGRAM* and RAW, invalid for STREAM
          [HOST=$host]                         # Optional for DATAGRAM* and RAW, invalid for STREAM
          [FROM_PORT=nnn]                      # For outbound traffic, default 0
          [TO_PORT=nnn]                        # For outbound traffic, default 0
          [PROTOCOL=nnn]                       # For outbound traffic for STYLE=RAW only, default 18.
                                               # 6, 17, 19, 20 not allowed.
          [LISTEN_PORT=nnn]                    # For inbound traffic, default is the FROM_PORT value.
                                               # For STYLE=STREAM, only the FROM_PORT value or 0 is allowed.
          [LISTEN_PROTOCOL=nnn]                # For inbound traffic for STYLE=RAW only.
                                               # Default is the PROTOCOL value; 6 (streaming) is disallowed
          [HEADER={true,false}]                # For STYLE=RAW only, default false
          [sam.udp.host=hostname]              # Datagram bind host, Java I2P only, DATAGRAM*/RAW only, default 127.0.0.1
          [sam.udp.port=nnn]                   # Datagram bind port, Java I2P only, DATAGRAM*/RAW only, default 7655
          [option=value]*                      # I2CP and streaming options
```
Мост SAM ответит об успехе или неудаче, как указано в [ответе на стандартное создание сеанса](#session-creation-response). Поскольку туннели уже были построены при первичном создании сеанса, мост SAM должен ответить немедленно.

Не устанавливайте опцию DESTINATION при SESSION ADD. Подсессия будет использовать назначение, указанное в основной сессии. Все подсессии должны быть добавлены через управляющий сокет, то есть через то же соединение, на котором была создана основная сессия.

Несколько подсессий должны иметь достаточно уникальные параметры, чтобы входящие данные можно было правильно маршрутизировать. В частности, несколько сессий одного стиля должны иметь разные параметры LISTEN_PORT (и/или LISTEN_PROTOCOL, только для RAW). Попытка добавить сессию с портом и протоколом прослушивания, которые дублируют существующую подсессию, приведёт к ошибке.

LISTEN_PORT — это локальный порт I2P, т.е. порт получения (TO) для входящих данных. Если LISTEN_PORT не указан, будет использовано значение FROM_PORT. Если не указаны ни LISTEN_PORT, ни FROM_PORT, маршрутизация входящих данных будет основываться исключительно на параметрах STYLE и PROTOCOL. Для LISTEN_PORT и LISTEN_PROTOCOL значение 0 означает «любое», то есть подстановочный знак (wildcard). Если и LISTEN_PORT, и LISTEN_PROTOCOL равны 0, этот подсеанс будет использоваться по умолчанию для входящего трафика, который не может быть направлен в другой подсеанс. Входящий потоковый трафик (протокол 6) никогда не будет направляться в RAW-подсеанс, даже если его LISTEN_PROTOCOL равен 0. RAW-подсеанс не может устанавливать LISTEN_PROTOCOL равным 6. Если нет подсеанса по умолчанию или подходящего подсеанса, соответствующего протоколу и порту входящего трафика, такие данные будут отброшены.

Используйте идентификатор подсессии, а не основной идентификатор сессии, для отправки и получения данных. Все команды, такие как STREAM CONNECT, DATAGRAM SEND и т.д., должны использовать идентификатор подсессии.

Все служебные команды поддерживаются в основной сессии или подсессии. Отправка/прием датаграмм v1/v2 и в режиме raw не поддерживается в основной сессии или на подсессиях.

#### Остановка подсессии

Используя тот же сокет управления, на котором была создана ОСНОВНАЯ сессия:

```
->  SESSION REMOVE
          ID=$nickname
```
Это удаляет подсессию из основной сессии. Не устанавливайте никакие другие параметры при SESSION REMOVE. Подсессии должны удаляться через управляющий сокет, то есть по тому же соединению, на котором была создана основная сессия. После удаления подсессия закрывается и не может использоваться для передачи или получения данных.

Мост SAM ответит об успехе или неудаче, как указано в [ответе на стандартное создание сессии](#session-creation-response).

### Команды утилиты SAM

Некоторые служебные команды требуют существующей сессии, а некоторые — нет. Смотрите подробности ниже.

#### Поиск имени хоста

Следующее сообщение может быть использовано клиентом для запроса моста SAM на разрешение имени:

```
NAMING LOOKUP
       NAME=$name
       [OPTIONS=true]     # Default false, as of router API 0.9.66
```
на который отвечает

```
NAMING REPLY
       RESULT=$result
       NAME=$name
       [VALUE=$destination]
       [MESSAGE="$message"]
       [OPTION:optionkey="$optionvalue"]   # As of router API 0.9.66
```
Значение RESULT может быть одним из следующих:

```
OK
INVALID_KEY
KEY_NOT_FOUND
```
Если NAME=ME, то ответ будет содержать адрес, используемый текущей сессией (полезно, если вы используете TRANSIENT). Если $result не равен OK, то MESSAGE может содержать описательное сообщение, например «bad format» и т.д. INVALID_KEY означает, что что-то не так с $name в запросе, возможно, недопустимые символы.

$destination — это base64-представление [Destination](/docs/specs/common-structures#type_Destination), состоящее из 516 или более символов base64 (387 или более байт в бинарном виде), в зависимости от типа подписи.

NAMING LOOKUP не требует, чтобы сначала была создана сессия. Однако в некоторых реализациях поиск по адресу .b32.i2p, который не закэширован и требует сетевого запроса, может завершиться неудачей из-за отсутствия доступных клиентских туннелей для выполнения поиска.

#### Параметры поиска имени

NAMING LOOKUP расширен, начиная с API маршрутизатора 0.9.66, для поддержки поиска служб. Поддержка может отличаться в зависимости от реализации. Дополнительную информацию см. в предложении 167.

NAMING LOOKUP NAME=example.i2p OPTIONS=true запрашивает отображение параметров в ответе. NAME может быть полным base64-адресом, когда OPTIONS=true.

Если поиск адреса прошёл успешно и в leaseset были указаны параметры, то в ответе после адреса будут следовать один или несколько параметров в формате OPTION:key=value. Каждый параметр будет иметь отдельный префикс OPTION:. Будут включены все параметры из leaseset, а не только параметры служебных записей. Например, могут присутствовать параметры для определений, введённых в будущем. Пример:

NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Ключи, содержащие '=', а также ключи или значения, содержащие символ новой строки, считаются недопустимыми, и соответствующая пара ключ-значение будет удалена из ответа. Если в leaseset не найдено ни одной опции, или если версия leaseset — 1, то в ответе не будет указано ни одной опции. Если в запросе было указано OPTIONS=true, и leaseset не найден, будет возвращено новое значение результата LEASESET_NOT_FOUND.

#### Генерация ключа назначения

Открытый и закрытый ключи в формате base64 могут быть сгенерированы с помощью следующего сообщения:

```
->  DEST GENERATE
          [SIGNATURE_TYPE=value]               # SAM 3.1 or higher only, default DSA_SHA1
```
на который отвечает

```
DEST REPLY
     PUB=$destination
     PRIV=$privkey
```
Начиная с версии 3.1 (I2P 0.9.14), поддерживается необязательный параметр SIGNATURE_TYPE. Значение SIGNATURE_TYPE может быть любым именем (например, ECDSA_SHA256_P256, без учёта регистра) или числом (например, 1), которое поддерживается [сертификатами ключей](/docs/specs/common-structures#type_Certificate). По умолчанию используется DSA_SHA1, что, скорее всего, не подходит. Для большинства приложений укажите SIGNATURE_TYPE=7.

$destination — это base64-представление [Destination](/docs/specs/common-structures#type_Destination), состоящее из 516 или более символов base64 (387 или более байт в бинарном виде), в зависимости от типа подписи.

$privkey — это base64-кодировка конкатенации [Destination](/docs/specs/common-structures#type_Destination), за которым следует [Private Key](/docs/specs/common-structures#type_PrivateKey), а затем [Signing Private Key](/docs/specs/common-structures#type_SigningPrivateKey), что составляет 884 или более символа в формате base64 (663 или более байт в бинарном виде), в зависимости от типа подписи. Бинарный формат описан в разделе Private Key File.

Примечания о 256-байтовом двоичном [приватном ключе](/docs/specs/common-structures#type_PrivateKey): это поле не используется с версии 0.6 (2005). Реализации SAM могут отправлять в этом поле случайные данные или строку из нулей; не стоит беспокоиться о появлении последовательности AAAA в base64. Большинство приложений просто сохраняют строку в формате base64 и возвращают её «как есть» в команде SESSION CREATE, либо декодируют в двоичный формат для хранения, а затем снова кодируют при отправке SESSION CREATE. Приложения же могут декодировать base64, распарсить двоичные данные согласно спецификации PrivateKeyFile, удалить 256-байтовую часть приватного ключа и заменить её 256 байтами случайных данных или нулей при повторном кодировании для SESSION CREATE. При этом ВСЕ остальные поля в спецификации PrivateKeyFile должны быть сохранены. Такой подход позволит сэкономить 256 байт на файловой системе, однако для большинства приложений это, вероятно, не стоит затраченных усилий. Дополнительную информацию и контекст см. в предложении 161.

DEST GENERATE не требует предварительного создания сессии.

DEST GENERATE нельзя использовать для создания назначения с автономными подписями.

#### PING/PONG (SAM 3.2 или выше)

Либо клиент, либо сервер могут отправить:

```
PING[ arbitrary text]
```
на порту управления с ответом:

```
PONG[ arbitrary text from the ping]
```
используется для поддержания активности сокета управления. Любая из сторон может закрыть сеанс и сокет, если в разумные сроки не будет получено ответа, в зависимости от реализации.

Если при ожидании PONG от клиента происходит тайм-аут, мост может отправить:

```
<- SESSION STATUS RESULT=I2P_ERROR MESSAGE="$message"
```
а затем отключитесь.

Если при ожидании PONG от моста происходит тайм-аут, клиент может просто отключиться.

PING/PONG не требуют предварительного создания сессии.

#### QUIT/STOP/EXIT (SAM 3.2 или выше, необязательные функции)

Команды QUIT, STOP и EXIT закроют сеанс и сокет. Реализация является необязательной и предназначена для удобства тестирования через telnet. Наличие или отсутствие ответа перед закрытием сокета (например, сообщения SESSION STATUS) зависит от реализации и выходит за рамки данного спецификации.

QUIT/STOP/EXIT не требуют предварительного создания сессии.

#### СПРАВКА (необязательная функция)

Серверы могут реализовывать команду HELP. Реализация является необязательной и предназначена для упрощения тестирования через telnet. Формат вывода и определение конца вывода зависят от реализации и находятся за рамками настоящей спецификации.

HELP не требует, чтобы сначала была создана сессия.

#### Конфигурация авторизации (SAM 3.2 или выше, необязательная функция)

Конфигурация авторизации с использованием команды AUTH. Сервер SAM может реализовывать эти команды для обеспечения постоянного хранения учётных данных. Настройка аутентификации, не связанная с этими командами, зависит от реализации и выходит за рамки данного спецификации.

- AUTH ENABLE включает авторизацию для последующих соединений
- AUTH DISABLE отключает авторизацию для последующих соединений
- AUTH ADD USER="foo" PASSWORD="bar" добавляет пользователя и пароль
- AUTH REMOVE USER="foo" удаляет этого пользователя

Использование двойных кавычек для имени пользователя и пароля рекомендуется, но не обязательно. Двойные кавычки внутри имени пользователя или пароля должны быть экранированы обратной косой чертой. В случае ошибки сервер ответит сообщением I2P_ERROR и текстом.

AUTH не требует, чтобы сначала была создана сессия.

### Значения RESULT

Это значения, которые могут передаваться в поле RESULT, вместе с их значением:

```
OK              Operation completed successfully
CANT_REACH_PEER The peer exists, but cannot be reached
DUPLICATED_DEST The specified Destination is already in use
I2P_ERROR       A generic I2P error (e.g. I2CP disconnection, etc.)
INVALID_KEY     The specified key is not valid (bad format, etc.)
KEY_NOT_FOUND   The naming system can't resolve the given name
PEER_NOT_FOUND  The peer cannot be found on the network
TIMEOUT         Timeout while waiting for an event (e.g. peer answer)
LEASESET_NOT_FOUND  See Name Lookup Options above. As of router API 0.9.66.
```
Разные реализации могут по-разному возвращать RESULT в различных сценариях.

Большинство ответов с результатом, отличным от OK, также будут содержать сообщение (MESSAGE) с дополнительной информацией. Сообщение, как правило, будет полезно при отладке проблем. Однако строки MESSAGE зависят от реализации, могут быть переведены сервером SAM на текущую локаль или не переведены, могут содержать внутреннюю информацию, специфичную для реализации (например, исключения), и могут быть изменены без предупреждения. Хотя клиенты SAM могут по своему усмотрению отображать строки MESSAGE пользователям, они не должны принимать программные решения на основе этих строк, так как это сделает работу приложения уязвимой.

### Параметры туннеля, I2CP и потоковой передачи

Эти параметры могут передаваться в виде пар имя=значение в строке SAM SESSION CREATE.

Все сеансы могут включать [опции I2CP, такие как длина и количество туннелей](/docs/protocol/i2cp#options). Сеансы STREAM могут включать [опции библиотеки потоковой передачи](/docs/api/streaming#options).

См. указанные ссылки для имён параметров и значений по умолчанию. Указанная документация относится к реализации маршрутизатора на Java. Значения по умолчанию могут быть изменены. Имена параметров и значений чувствительны к регистру. Другие реализации маршрутизаторов могут не поддерживать все параметры и могут иметь различные значения по умолчанию; подробности см. в документации маршрутизатора.

### Примечания по Base64

Для кодирования Base 64 необходимо использовать алфавит Base 64 по стандарту I2P: "A–Z, a–z, 0–9, –, ~".

### Настройка SAM по умолчанию

Порт SAM по умолчанию — 7656. SAM по умолчанию отключён в Java I2P-роутере; его необходимо запустить вручную или настроить автозапуск на странице настройки клиентов в консоли роутера либо в файле clients.config. Порт UDP для SAM по умолчанию — 7655, прослушивается на 127.0.0.1. Эти параметры можно изменить в Java-роутере, добавив аргументы sam.udp.port=nnnnn и/или sam.udp.host=w.x.y.z при запуске или в строке SESSION.

Конфигурация в других маршрутизаторах зависит от реализации. См. [руководство по настройке i2pd здесь](https://i2pd.readthedocs.io/en/latest/user-guide/configuration/).
