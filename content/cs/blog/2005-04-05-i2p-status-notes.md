---
title: "Poznámky ke stavu I2P ke dni 2005-04-05"
date: 2005-04-05
author: "jr"
description: "Týdenní aktualizace o problémech vydání 0.5.0.5, výzkumu bayesovského profilování peerů (uzlů) a pokroku aplikace Q"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

* Index

1) 0.5.0.5 2) Bayesovské profilování peerů 3) Q 4) ???

* 1) 0.5.0.5

Minulý týden vydaná verze 0.5.0.5 měla své plusy i mínusy - zásadní změna, která řeší některé útoky v netDb, se zdá fungovat podle očekávání, ale odhalila několik dlouho přehlížených chyb v provozu netDb. To způsobilo značné problémy se spolehlivostí, zejména pro eepsites(I2P Sites). Chyby však byly identifikovány a opraveny v CVS a tyto opravy spolu s několika dalšími budou během příštího dne uvolněny jako verze 0.5.0.6.

* 2) Bayesian peer profiling

bla v poslední době provádí výzkum zaměřený na zlepšení našeho profilování peerů využitím jednoduchého bayesovského filtrování z nasbíraných statistik [1]. Vypadá to docela slibně, i když si nejsem jistý, v jaké fázi to v tuto chvíli je - možná bychom mohli během schůzky od bla získat aktualizaci?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

U aplikace Q od auma dochází k velkému pokroku, a to jak v oblasti základní funkčnosti, tak i díky práci několika lidí na různých xmlrpc frontendech. Proslýchá se, že bychom už tento víkend mohli vidět další sestavení Q s celou řadou novinek popsaných na http://aum.i2p/q/

* 4) ???

Ok, jo, velmi stručné poznámky ke stavu, protože jsem si *zase* popletl časová pásma (vlastně jsem si popletl i dny, ještě před pár hodinami jsem si myslel, že je pondělí). Každopádně se děje spousta věcí, které výše nejsou zmíněné, tak se stavte na schůzce a podívejte se, co je nového!

=jr
