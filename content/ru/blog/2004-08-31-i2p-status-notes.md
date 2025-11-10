---
title: "Заметки о статусе I2P за 2004-08-31"
date: 2004-08-31
author: "jr"
description: "Еженедельный отчёт о состоянии I2P, охватывающий ухудшение производительности сети, планирование релиза 0.3.5, потребности в документации и прогресс Stasher DHT (распределённая хеш-таблица)"
categories: ["status"]
---

Ну что, мальчики и девочки, снова вторник!

## Содержание:

1. 0.3.4.3
2. 0.3.5 and 0.4
3. docs
4. stasher update
5. ???

## 1) 0.3.4.3

Ну, как вы все заметили, хотя число пользователей в сети оставалось довольно стабильным, производительность за последние несколько дней существенно ухудшилась. Причиной стал ряд ошибок в механизмах выбора пиров и в коде доставки сообщений, которые проявились, когда на прошлой неделе была небольшая DoS-атака. В результате tunnels у всех стабильно отказывали, что породило эффект снежного кома. Так что нет, дело не только в вас — сеть была ужасной и для всех остальных ;)

Но хорошая новость в том, что мы довольно быстро исправили проблемы, и они уже в CVS с прошлой недели, но сеть всё ещё будет работать плохо для пользователей до выхода следующего релиза. В связи с этим...

## 2) 0.3.5 и 0.4

Хотя следующий релиз включит все вкусности, которые мы запланировали для релиза 0.4 (новый установщик, новый стандарт веб-интерфейса, новый интерфейс i2ptunnel, системный трей и служба Windows, улучшения многопоточности, исправления ошибок и т. д.), показательно то, как прошлый релиз со временем ухудшался. Я хочу, чтобы мы двигались с этими релизами более неспешно, давая им время более полно развернуться и чтобы проявились шероховатости. Хотя симулятор может изучать основы, у него нет способа смоделировать естественные сетевые проблемы, которые мы видим в живой сети (по крайней мере, пока).

В связи с этим следующий релиз будет 0.3.5 — надеюсь, последний релиз ветки 0.3.*, но, возможно, и нет, если возникнут другие проблемы. Оглядываясь на то, как сеть работала, когда я был вне сети в июне, ситуация начала ухудшаться примерно через две недели. Поэтому, по моему мнению, стоит повременить с повышением версии до 0.4, пока мы не сможем поддерживать высокий уровень надежности как минимум в течение двух недель. Разумеется, это не означает, что мы не будем вести работу в это время.

В любом случае, как упоминалось на прошлой неделе, hypercubus упорно трудится над новой системой установки, справляясь с тем, что я всё время что-то меняю и требую поддержки экзотических систем. Думаю, в ближайшие несколько дней мы доведём всё до ума и выпустим релиз 0.3.5.

## 3) документация

Одна из важных вещей, которую нам нужно сделать в течение этого двухнедельного "окна тестирования" перед 0.4, — это задокументировать всё как можно полнее. Меня интересует, чего, по вашему мнению, не хватает нашей документации - какие у вас есть вопросы, на которые нам нужно ответить? Хотя мне бы хотелось сказать: "ok, теперь идите и напишите эти документы", я реалист, поэтому прошу лишь указать, какие темы эти документы должны освещать.

Например, один из документов, над которыми я сейчас работаю, — это пересмотренная версия модели угроз, которую я бы теперь описал как серию сценариев использования, объясняющих, как I2P может удовлетворять потребности разных пользователей, включая функциональность, злоумышленников, которых опасается этот пользователь, и то, как он защищается.

Если вы считаете, что для ответа на ваш вопрос не нужен полноценный документ, просто сформулируйте его как вопрос, и мы сможем добавить его в раздел часто задаваемых вопросов (FAQ).

## 4) обновление stasher

Aum заглянул в канал сегодня пораньше с обновлением (пока я засыпал его вопросами):

```
<aum> quick stasher update, with apologies for tomorrow's meeting:
<aum> infinite-level splitfiles working, have successfully
      inserted and retrieved large files
<jrandom> w00t
<aum> splitfile fragmentation/reassembly transparently occuring
      within stasher
<aum> freenet interface working
<jrandom> wow
<jrandom> so FUQID/FIW works?
<aum> use of fcp splitfile commands in freenet clients strictly
      forbidden (at this stage)
<aum> most clients such as fuqid/fiw should allow setting
      extremely large splitfile sizes, which should prevent them
      trying to talk splitfiles
<aum> if not, then i can dummy up something
<jrandom> r0x0r aum, that kicks ass!
<aum> hooks are in for detailed freenet key support
<jrandom> detailed freenet key support?
<aum> yes, specific chk@, ssk@, ksk@
<jrandom> ok great, so they're all verified @ each node, etc?
<aum> no - only verifiable by the requestor
<aum> my thinking is, given KSK@fred = 'mary',
<aum> to store as SHA1(SHA1("KSK@fred")) = E(mary), where key
      for E is SHA1("KSK@fred")
<aum> ie, crypto key is SHA1(uri), and kademlia key is
      SHA1(SHA1(uri))
<jrandom> hm
<aum> so a possessor of the URI can decyrpt, but owner of a
      datastore cannot decrypt (and therefore has plausible
      deniability)
<jrandom> well, ksks are inherently insecure, so thats no big
      loss, but what about ssk?
<deer> <detonate> those keys aren't very large
<aum> SSK as for freenet
<jrandom> so the SSKs are verified at each node?
<aum> except i'm looking to use same encryption over the top
<aum> not feasible to verify SSK at the target node
<jrandom> why not?  freenet does
<aum> well maybe it is feasible,
<aum> i guess i shouldn't be so lazy
<aum> i was trying to keep the kademlia and freenet layers
      separate
<jrandom> heh, you're not being lazy, there's a truckload of
      work here, and you're doing a great job
<aum> verifying on target node will cause some pathological
      couplings between the two layers, and force deviation
      from pure kademlia
<jrandom> i dont think its possible to do SSKs or CHKs
      securely without having the node validate the key
      properties
<aum> not correct
<aum> fred asks mary, 'gimme SSK@madonna'
<aum> mary sends back what she thinks is 'SSK@madonna'
<aum> fred tests it, barfs, then goes on to ask the next node
<aum> anyway, i MUST go - but am open to continuing discussion
      over email, or tomorrow
<aum> bbl guys
<jrandom> mallory floods the net with 'SSK@madonna' ==
      'sexDrugsRockNRoll'
<jrandom> l8r aum
```
Итак, как видите, прогресса очень много. Даже если ключи проверяются выше уровня DHT (распределённой хеш-таблицы), это чертовски круто (имхо). Вперёд, aum!

## 5) ???

Окей, это всё, что я хотел сказать (что хорошо, потому что встреча начинается через пару минут)... заскакивайте и говорите, что хотите!

=jr
