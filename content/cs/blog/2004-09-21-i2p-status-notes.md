---
title: "Poznámky ke stavu I2P k 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Týdenní aktualizace stavu I2P zaměřená na pokrok ve vývoji, vylepšení TCP transportu a novou funkci userhosts.txt"
categories: ["status"]
---

Ahoj všichni, stručná aktualizace tento týden

## Rejstřík

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Stav vývoje

Síť byla v uplynulém týdnu poměrně stabilní, takže jsem se mohl soustředit na vydání 0.4.1 - přepracování TCP transportu a přidání podpory pro detekci IP adres a odstranění toho starého "target changed identities". To by také mělo odstranit potřebu záznamů dyndns.

Nebude to ideální 0-klikové nastavení pro uživatele za NATy nebo firewally - stále budou muset nastavit přesměrování portů, aby mohli přijímat příchozí TCP připojení. Mělo by to však být méně náchylné k chybám. Dělám maximum pro zachování zpětné kompatibility, ale v tomto ohledu nic neslibuji. Další novinky, až to bude připravené.

## 2) Nový userhosts.txt vs. hosts.txt

V příštím vydání budeme mít často požadovanou podporu pro dvojici souborů hosts.txt - jeden, který je při aktualizacích přepisován (nebo z `http://dev.i2p.net/i2p/hosts.txt`) a druhý, který si uživatel může spravovat lokálně. V příštím vydání (nebo v CVS HEAD) můžete upravovat soubor "userhosts.txt", který se kontroluje před hosts.txt kvůli jakýmkoli záznamům - prosíme, provádějte své lokální změny tam, protože proces aktualizace přepíše hosts.txt (ale ne userhosts.txt).

## 3) ???

Jak už bylo řečeno, tento týden jen stručné poznámky. Má někdo ještě něco, co chce zmínit? Zaskočte na schůzku za pár minut.

=jr
