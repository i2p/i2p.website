---
title: "I2P Jpackages получили своё первое обновление"
date: 2021-11-02
author: "idk"
description: "Новые более простые в установке пакеты достигают новой вехи"
categories: ["general"]
---

Несколько месяцев назад мы выпустили новые пакеты, которые, как мы надеялись, помогут подключать новых пользователей к сети I2P, упростив установку и настройку I2P для большего числа людей. Мы убрали десятки шагов из процесса установки, перейдя с внешней JVM на Jpackage, подготовили стандартные пакеты для целевых операционных систем и подписали их таким образом, чтобы операционная система их распознавала, что повышает безопасность пользователя. С тех пор router, собранные с помощью jpackage, достигли нового рубежа: они вот-вот получат свои первые инкрементные обновления. Эти обновления заменят jpackage на базе JDK 16 обновлённым jpackage на базе JDK 17 и включат исправления некоторых небольших ошибок, которые мы обнаружили после релиза.

## Общие обновления для Mac OS и Windows

Все jpackaged (собранные с использованием jpackage) установщики I2P получают следующие обновления:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Пожалуйста, обновите как можно скорее.

## I2P Windows Jpackage Updates

Пакеты, предназначенные только для Windows, получают следующие обновления:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Полный список изменений см. в changelog.txt в i2p.firefox

## Обновления Jpackage для I2P на Mac OS

Пакеты, предназначенные только для Mac OS, получают следующие обновления:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Для сводки разработки см. коммиты в i2p-jpackage-mac
