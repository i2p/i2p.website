---
title: "Заметки о статусе I2P за 2005-03-08"
date: 2005-03-08
author: "jr"
description: "Еженедельные заметки о ходе разработки I2P, посвященные улучшениям релиза 0.5.0.2, акценту на надежности сети и обновлениям почтовых и BitTorrent‑сервисов"
categories: ["status"]
---

Всем привет, пора еженедельного обновления

* Index

1) 0.5.0.2 2) mail.i2p updates 3) i2p-bt updates 4) ???

* 1) 0.5.0.2

На днях мы выпустили релиз 0.5.0.2, и значительная часть сети уже обновилась (ура!). Поступают сообщения, что самые серьёзные проблемы 0.5.0.1 были устранены, и в целом всё, похоже, работает нормально. Всё ещё есть некоторые проблемы с надёжностью, хотя streaming lib (библиотека потоковой передачи данных) с этим справляется (IRC-подключения, длящиеся 12-24+ часов, похоже, стали нормой). Я пытаюсь разобраться с некоторыми из оставшихся проблем, но было бы очень-очень хорошо, если бы все обновились как можно скорее.

As things stand for moving forward, reliability is king.  Only after an overwhelming majority of messages that should succeed do succeed will there be work on improving throughput.  Beyond the batching tunnel preprocessor, another dimension we may want to explore is feeding more latency data into the profiles.  We currently only use test and tunnel management messages to determine each peer's "speed" ranking, but we should probably snag any measurable RTTs for other actions, such as netDb and even end to end client messages.  On the other hand, we'll have to weight them accordingly, since for an end to end message, we cannot separate the four portions of the measurable RTT (our outbound, their inbound, their outbound, our inbound).  Perhaps we can do some garlic trickery to bundle a message targetting one of our inbound tunnels along side some outbound messages, cutting the other side's tunnels out of the measurement loop.

* 2) mail.i2p updates

Ок, я не знаю, какие обновления postman для нас припас, но во время встречи будет обновление. Смотрите логи, чтобы узнать!

* 3) i2p-bt update

Я не знаю, какие новости у duck & gang для нас, но до меня доходили разговоры о прогрессе на канале. Может, удастся выудить из него какие‑нибудь новости.

* 4) ???

Много всего происходит, но если есть что-то конкретное, что вы хотите поднять и обсудить, загляните на встречу через несколько минут. И да, просто напоминание: если вы ещё не обновились, пожалуйста, сделайте это как можно скорее (обновление до смешного простое — скачайте файл, нажмите кнопку).

=jr
