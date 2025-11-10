---
title: "Примечания о состоянии I2P за 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Еженедельное обновление статуса, охватывающее релиз 0.3.2.3, изменения пропускной способности, обновления веб‑сайта и соображения безопасности"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, и дорожная карта**

После выпуска 0.3.2.3 на прошлой неделе вы все отлично справились с обновлением - сейчас у нас осталось всего двое отстающих (один на 0.3.2.2 и один вообще на 0.3.1.4 :). За последние несколько дней сеть была стабильнее обычного - люди остаются на irc.duck.i2p часами, крупные файлы успешно скачиваются с eepsites(сайты I2P), и общая доступность eepsite(сайт I2P) довольно хорошая. Раз всё идёт хорошо и чтобы не давать вам расслабиться, я решил изменить несколько базовых концепций, и мы развернём их в релизе 0.3.3 через день-другой.

Поскольку несколько человек прокомментировали наш график, задаваясь вопросом, уложимся ли мы в объявленные сроки, я решил, что, наверное, стоит обновить сайт, чтобы отразить дорожную карту, которая у меня в PalmPilot, и так и сделал [1]. Сроки сдвинулись, некоторые пункты были переставлены, но план остался тем же, что обсуждался в прошлом месяце [2].

Версия 0.4 будет соответствовать четырём упомянутым критериям релиза (функциональность, безопасность, анонимность и масштабируемость), однако до 0.4.2 немногие пользователи, находящиеся за NAT и межсетевыми экранами, смогут участвовать, а до 0.4.3 будет фактическое верхнее ограничение размера сети из‑за накладных расходов на поддержание большого числа TCP‑соединений с другими routers.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

За последнюю неделю или около того люди в #i2p иногда слышали, как я раздраженно говорю о том, что наши рейтинги надежности совершенно произвольны (и о том, сколько проблем это принесло в нескольких последних релизах). Поэтому мы полностью отказались от понятия надежности, заменив его показателем capacity (возможностей) — «сколько пользы пир может нам принести?». Это имело каскадные последствия по всему коду выбора пиров и профилирования пиров (и, разумеется, в консоли router), но помимо этого существенных изменений почти не было.

Более подробную информацию об этом изменении можно найти на обновлённой странице выбора пиров [3], а когда выйдет 0.3.3, все вы сможете воочию увидеть эффект (я последние несколько дней с этим экспериментировал, подправлял некоторые настройки и т. п.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) обновления веб-сайта**

За последнюю неделю мы значительно продвинулись в работе над редизайном сайта [4] - упростили навигацию, привели в порядок некоторые ключевые страницы, импортировали старый контент и подготовили несколько новых материалов [5]. Мы почти готовы вывести сайт в продакшен, но ещё осталось несколько вещей, которые нужно сделать.

Сегодня утром duck прошёлся по сайту и составил перечень недостающих страниц, а после дневных обновлений осталось несколько нерешённых вопросов, которые, надеюсь, мы сможем либо решить, либо найти добровольцев, которые возьмутся за них:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Кроме того, думаю, сайт уже почти готов к запуску в продакшен. Есть ли у кого‑нибудь предложения или замечания по этому поводу?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) атаки и методы защиты**

Коннелли придумал несколько новых подходов, чтобы попытаться найти слабые места в безопасности и анонимности сети, и при этом наткнулся на некоторые способы, как мы можем улучшить ситуацию. Хотя отдельные аспекты описанных им методик не слишком применимы к I2P, возможно, вы сможете увидеть, как их можно развить, чтобы продвинуть атаку на сеть ещё дальше? Ну же, попробуйте :)

**5) ???**

Пожалуй, это всё, что я могу вспомнить перед сегодняшней встречей - если я что-то упустил, пожалуйста, сообщите. В любом случае, увидимся в #i2p через несколько минут.

=jr
