---
title: "Poznámky ke stavu I2P k 2006-01-24"
date: 2006-01-24
author: "jr"
description: "Aktualizace stavu sítě, nový proces budování tunnel pro 0.6.2 a vylepšení spolehlivosti"
categories: ["status"]
---

Ahoj všichni, úterý se pořád vrací...

* Index

1) Stav sítě 2) Nový proces sestavení 3) ???

* 1) Net status

Uplynulý týden nepřinesl v síti mnoho změn, většina uživatelů (77 %) má nainstalované nejnovější vydání. Přesto jsou na obzoru některé zásadní změny související s novým procesem budování tunnelů a tyto změny způsobí určité komplikace těm, kdo pomáhají testovat nevydaná sestavení. Celkově však by ti, kdo používají vydané verze, měli i nadále mít poměrně spolehlivou úroveň služeb.

* 2) New build process

V rámci přepracování tunnel pro 0.6.2 měníme postup používaný uvnitř router tak, aby se lépe přizpůsoboval měnícím se podmínkám a čistěji zvládal zátěž. Jde o předstupeň integrace nových strategií výběru peer (protějšků) a nové kryptografie pro vytváření tunnel a je plně zpětně kompatibilní. Současně však při této příležitosti odstraňujeme některé zvláštnosti v procesu vytváření tunnel a přestože některé z nich pomáhaly zamaskovat určité problémy se spolehlivostí, mohly vést k méně než optimálnímu kompromisu mezi anonymitou a spolehlivostí. Konkrétně se při katastrofálních selháních používaly záložní 1 hop tunnels – nový postup naproti tomu upřednostní nedostupnost před použitím záložních tunnels, což znamená, že lidé uvidí více problémů se spolehlivostí. Alespoň budou viditelné, dokud nebude odstraněn zdroj problému se spolehlivostí u tunnel.

Každopádně, v tuto chvíli proces sestavení nezajišťuje přijatelnou spolehlivost, ale jakmile tomu tak bude, uvolníme to pro všechny v rámci vydání.

* 3) ???

Vím, že pár dalších lidí pracuje na různých souvisejících aktivitách, ale nechám na nich, aby nám novinky sdělili, až to uznají za vhodné. Každopádně, uvidíme se na schůzce za pár minut!

=jr
