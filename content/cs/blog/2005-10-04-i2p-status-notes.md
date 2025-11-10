---
title: "Stavové poznámky I2P ze dne 2005-10-04"
date: 2005-10-04
author: "jr"
description: "Týdenní aktualizace pokrývající úspěch vydání 0.6.1.1 s 3-400 uzly, úsilí o sladění forků i2phex a pokrok v automatizaci Syndie s pet names (přezdívkami) a scheduled pulls (naplánovanými stahováními)"
categories: ["status"]
---

Ahoj všichni, je čas na naše týdenní statusové poznámky (sem vložte jásot)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

Jak bylo oznámeno na obvyklých místech, 0.6.1.1 vyšlo před pár dny a zatím jsou ohlasy pozitivní. Síť se rozrostla na stabilních 3-400 známých peerů a výkon byl poměrně dobrý, i když využití CPU trochu vzrostlo. To je pravděpodobně způsobeno dlouhodobou chybou, která nesprávně umožňuje přijímat neplatné IP adresy, což následně způsobuje vyšší než nutnou churn (fluktuaci uzlů). V CVS sestaveních od 0.6.1.1 byly opravy tohoto i dalších problémů, takže pravděpodobně budeme mít 0.6.1.2 později tento týden.

* 2) i2phex

Zatímco si někteří mohli všimnout diskuse na různých fórech ohledně i2phexu a legionova forku, proběhla další komunikace mezi mnou a legionem a pracujeme na opětovném sloučení obou. Více informací k tomu, jakmile budou k dispozici.

Kromě toho redzara intenzivně pracuje na sloučení i2phex s aktuálním vydáním phexu a striker přišel s dalšími vylepšeními, takže se brzy chystají některé vzrušující novinky.

* 3) syndie

Ragnarok posledních pár dní pilně pracoval na syndie, na integraci databáze pet name (osobních názvů) syndie s databází routeru, stejně jako na automatizaci syndikace pomocí plánovaných stažení z vybraných vzdálených archivů. Část týkající se automatizace je hotová a přestože zbývá ještě nějaká práce na uživatelském rozhraní, je v docela dobrém stavu!

* 4) ???

V poslední době se toho taky děje hodně, včetně práce na nových úvodních technických dokumentech, migrace IRC a přepracování webu. Pokud má někdo něco, co by chtěl probrat, zastavte se na schůzku za pár minut a ozvěte se!

=jr
