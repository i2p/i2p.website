---
title: "I2P není ovlivněno zranitelností log4j"
date: 2021-12-11
author: "idk, zzz"
description: "I2P nepoužívá log4j, a proto se ho CVE-2021-44228 netýká"
categories: ["security"]
---

I2P není ovlivněno zranitelností log4j 0-Day, která byla zveřejněna včera, CVE-2021-44228. I2P nepoužívá log4j pro logování, nicméně jsme také museli prověřit naše závislosti z hlediska použití log4j, zejména jetty. Tato prověrka neodhalila žádné zranitelnosti.

Bylo také důležité zkontrolovat všechny naše zásuvné moduly. Zásuvné moduly mohou obsahovat vlastní systémy logování, včetně log4j. Zjistili jsme, že většina zásuvných modulů log4j také nepoužívá, a ty, které ano, nepoužívaly zranitelnou verzi log4j.

Nenašli jsme žádnou zranitelnou závislost, zásuvný modul ani aplikaci.

Dodáváme soubor log4j.properties společně s jetty pro pluginy, které zavádějí log4j. Tento soubor má účinek pouze na pluginy, které interně používají logování log4j. Zapracovali jsme doporučené zmírnění rizika (mitigation) do souboru log4j.properties. Pluginy, které povolují log4j, poběží s vypnutou zranitelnou funkcí. Protože nikde nenacházíme žádné použití log4j 2.x, nemáme v tuto chvíli v plánu vydat nouzové vydání.
