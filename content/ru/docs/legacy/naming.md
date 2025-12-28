---
title: "Обсуждение именования"
description: "Историческая дискуссия о модели именования I2P и о том, почему были отвергнуты глобальные DNS‑подобные схемы"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Контекст:** На этой странице собраны затяжные дискуссии из раннего этапа проектирования I2P. Она объясняет, почему проект отдавал предпочтение локально доверенным адресным книгам, а не DNS-подобному разрешению имён или реестрам, основанным на решении большинством. Актуальные рекомендации по использованию см. в [документации по именованию](/docs/overview/naming/).

## Отклонённые альтернативы

Цели безопасности I2P исключают привычные схемы именования:

- **Разрешение в стиле DNS.** Любой резолвер на пути разрешения может подделать или цензурировать ответы. Даже с DNSSEC скомпрометированные регистраторы или центры сертификации остаются единой точкой отказа. В I2P destinations (адреса назначения) *являются* открытыми ключами—перехват запроса на разрешение полностью компрометирует идентичность.
- **Именование на основе голосования.** Противник может создавать неограниченное число идентичностей (атака Сивиллы) и “выигрывать” голоса за популярные имена. Меры на основе доказательства работы повышают стоимость атаки, но вносят серьёзные накладные расходы на координацию.

Вместо этого в I2P система именования сознательно располагается над транспортным уровнем. Встроенная библиотека именования предоставляет интерфейс поставщика услуг, чтобы альтернативные схемы могли сосуществовать — пользователи сами решают, каким адресным книгам или jump services (службам перехода) они доверяют.

## Локальные и глобальные имена (jrandom, 2005)

- Имена в I2P являются **локально уникальными, но человекочитаемыми**. Ваш `boss.i2p` может не совпадать с `boss.i2p` другого человека, и это сделано намеренно.
- Если злоумышленник обманом заставит вас изменить Destination (назначение), стоящее за именем, он фактически захватит сервис. Отказ от глобальной уникальности предотвращает такой класс атак.
- Относитесь к именам как к закладкам или никам в мессенджерах — вы сами выбираете, каким Destination доверять, подписываясь на конкретные адресные книги или добавляя ключи вручную.

## Распространённые возражения и ответы (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Обсуждение идей повышения эффективности

- Предоставлять инкрементальные обновления (только назначения, добавленные после последнего получения).
- Предлагать дополнительные фиды (`recenthosts.cgi`) наряду с полными файлами hosts.
- Рассмотреть инструменты с поддержкой скриптов (например, `i2host.i2p`) для объединения фидов или фильтрации по уровням доверия.

## Основные выводы

- Безопасность важнее глобального консенсуса: локально сопровождаемые адресные книги минимизируют риск подмены.
- Несколько подходов к именованию могут сосуществовать через API именования—пользователи сами решают, чему доверять.
- Полностью децентрализованная глобальная система именования все еще остается открытой исследовательской задачей; компромиссы между безопасностью, удобством запоминания для человека и глобальной уникальностью по-прежнему отражают [треугольник Зуко](https://zooko.com/distnames.html).

## Ссылки

- [Документация по именованию](/docs/overview/naming/)
- [Зуко: «Имена: децентрализованные, безопасные, понятные человеку: выберите любые два»](https://zooko.com/distnames.html)
- Пример инкрементальной ленты: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
