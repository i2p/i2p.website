---
title: "Vypršení platnosti zaváděče"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Uzavřeno"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Přehled

Tento návrh se týká zlepšení úspěšnosti zavádění. Viz
[TRAC-TICKET]_.

## Motivace

Zaváděče vyprší po určité době, ale tato informace není zveřejněna v
[RouterInfo]_. Směrovače nyní musí používat heuristiku k odhadnutí, kdy
zaváděč už není platný.

## Návrh

V SSU [RouterAddress]_ obsahující zaváděče může vydavatel volitelně
zahrnout časy vypršení platnosti pro každý zaváděč.

## Specifikace

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: Číslo zaváděče (0-2)

  nnnnnnnnnn :: Čas v sekundách (ne ms) od počátku epochy.
{% endhighlight %}

Poznámky
`````
* Každé vypršení musí být větší než datum zveřejnění [RouterInfo]_,
  a menší než 6 hodin po datu zveřejnění RouterInfo.

* Směrovače a zaváděče by se měly snažit udržet zaváděč platný
  až do vypršení, avšak není možné toto zaručit.

* Směrovače by neměly používat zveřejněný zaváděč po jeho vypršení.

* Platnosti zaváděčů jsou v mapování [RouterAddress]_.
  Nejsou to (aktuálně nepoužívaná) 8-bajtová pole vypršení v [RouterAddress]_.

Příklad: ``iexp0=1486309470``

## Migrace

Žádné problémy. Implementace je volitelná.
Zpětná kompatibilita je zajištěna, protože starší směrovače budou neznámé parametry ignorovat.

## Odkazy

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
