---
title: "I2P Jpackages se dočkaly první aktualizace"
date: 2021-11-02
author: "idk"
description: "Nové snáze instalovatelné balíčky dosahují nového milníku"
categories: ["general"]
API_Translate: pravda
---

Před pár měsíci jsme vydali nové balíčky, u nichž jsme doufali, že pomohou přivést do sítě I2P nové lidi tím, že více lidem usnadní instalaci a konfiguraci I2P. Z instalačního procesu jsme odstranili desítky kroků tím, že jsme přešli z externí JVM na Jpackage, vytvořili standardní balíčky pro cílové operační systémy a podepsali je způsobem, který operační systém rozpozná, aby byl uživatel v bezpečí. Od té doby jpackage router dosáhly nového milníku; brzy obdrží své první inkrementální aktualizace. Tyto aktualizace nahradí JDK 16 jpackage aktualizovaným JDK 17 jpackage a přinesou opravy několika drobných chyb, které jsme odhalili po vydání.

## Aktualizace společné pro Mac OS a Windows

Všechny jpackaged instalátory I2P obdrží následující aktualizace:

* Update the jpackaged I2P router to 1.5.1 which is built with JDK 17

Aktualizujte prosím co nejdříve.

## Aktualizace I2P Jpackage pro Windows

Balíčky pouze pro Windows obdrží následující aktualizace:

* Updates I2P in Private Browsing, NoScript browser extensions
* Begins to phase out HTTPS everywhere on new Firefox releases
* Updates launcher script to fix post NSIS launch issue on some architectures

Pro úplný seznam změn viz soubor changelog.txt v i2p.firefox

## Aktualizace Jpackage pro I2P na Mac OS

Pouze balíčky pro Mac OS obdrží následující aktualizace:

* No Mac-Specific changes. Mac OS is updated to build with JDK 17.

Pro souhrn vývoje viz záznamy commitů v i2p-jpackage-mac
