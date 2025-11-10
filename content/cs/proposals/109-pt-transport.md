---
title: "PT Transport"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/1551"
---

## Přehled

Tento návrh je určen pro vytvoření I2P transportu, který se připojuje k dalším routerům
prostřednictvím připojitelných přenosů.


## Motivace

Připojitelné přenosy (PTs) byly vyvinuty projektem Tor jako způsob, jak modulárně přidávat
obfuskační přenosy k Tor bridge.

I2P již má modulární transportní systém, který snižuje bariéru k přidání alternativních přenosů. Přidání podpory pro PTs by poskytlo I2P snadný způsob, jak experimentovat s alternativními protokoly a připravit se na odolnost vůči blokování.


## Návrh

Existuje několik potenciálních vrstev implementace:

1. Obecný PT, který implementuje SOCKS a ExtORPort a konfiguruje a rozděluje
   procesy vstupu a výstupu a registruje se s komunikačním systémem. Tato vrstva nic neví
   o NTCP a může, ale nemusí používat NTCP. Dobré pro testování.

2. Buduje na 1), obecný NTCP PT, který staví na kódu NTCP a směruje
   NTCP do 1).

3. Buduje na 2), konkrétní NTCP-xxxx PT nakonfigurovaný pro spuštění daného externího vstupního
   a výstupního procesu.
