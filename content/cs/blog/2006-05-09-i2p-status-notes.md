---
title: "Poznámky ke stavu I2P k 2006-05-09"
date: 2006-05-09
author: "jr"
description: "Vydání 0.6.1.18 s vylepšeními stability sítě, novým vývojovým serverem 'baz' a problémy s kompatibilitou GCJ ve Windows"
categories: ["status"]
---

Ahoj všichni, úterý je tu zase

* Index

1) Stav sítě a 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Po dalším týdnu testování a ladění jsme dnes odpoledne vydali novou verzi, která by nás měla dostat do stabilnějšího prostředí, na jehož základě budeme moci provádět další vylepšení. Nejspíš neuvidíme větší efekt, dokud nebude široce nasazena, takže si možná budeme muset pár dní počkat, jak se to vyvine, ale měření budou samozřejmě pokračovat.

Jedním aspektem nejnovějších sestavení a vydání, na který zzz nedávno upozornil, bylo, že zvýšení počtu záložních tunnels může nyní mít výrazný dopad, pokud se provede současně se snížením počtu paralelních tunnels. Nové leases (časově omezené záznamy pro příjem na cílovém routeru) nevytváříme, dokud nemáme dostatečný počet živých tunnels, takže záložní tunnels lze rychle nasadit v případě selhání live tunnel, což snižuje četnost, s jakou je klient bez aktivního lease. Je to však jen drobná úprava symptomu a nejnovější vydání by mělo pomoci řešit kořenovou příčinu.

* 2) baz

"baz", nový stroj, který daroval bar, konečně dorazil, notebook s amd64 turion (s winxp na bootovacím disku a s několika dalšími OS připravenými na externích discích). Posledních pár dní na něm také pracuji a snažím se na něm otestovat několik nápadů na nasazení. Na jeden problém ale narážím: zprovoznit gcj na Windows. Přesněji řečeno, gcj s moderním gnu/classpath. Podle toho, co se říká, je to ale dost negativní – dá se sestavit buď nativně v mingw, nebo křížově z Linuxu, ale má problémy, například dochází k segfaultu pokaždé, když výjimka překročí hranici dll. Takže například pokud java.io.File (umístěná v libgcj.dll) vyvolá výjimku a ta je zachycena něčím v net.i2p.* (umístěném v libi2p.dll nebo i2p.exe), *puf*, je po aplikaci.

Jo, nevypadá to zrovna dobře. Lidi kolem gcj by byli velmi rádi, kdyby se někdo přidal a pomohl s vývojem pro win32, ale životaschopná podpora zřejmě není na spadnutí. Takže to vypadá, že budeme muset dál používat Sun JVM na Windows, zatímco na *nix budeme podporovat gcj/kaffe/sun/ibm/atd. Myslím, že to ale není zas tak špatné, protože právě uživatelé *nix mají problémy s balením a distribucí JVM.

* 3) ???

Ok, už mám zpoždění na schůzku, takže bych to měl rychle uzavřít a přepnout se do okna irc, předpokládám... uvidíme se za chvilku ;)

=jr
