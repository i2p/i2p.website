---
title: "Větší I2NP Zprávy"
number: "103"
author: "zzz"
created: "2009-04-05"
lastupdated: "2009-05-27"
status: "Neaktivní"
thread: "http://zzz.i2p/topics/258"
---

## Přehled

Tento návrh se týká zvýšení limitu velikosti I2NP zpráv.


## Motivace

Použití 12KB datagramů v iMule odhalilo mnoho problémů. Skutečný limit je dnes
spíše kolem 10KB.


## Návrh

Je potřeba udělat:

- Zvýšit limit NTCP - není tak snadné?

- Více úprav množství značek relací. Může to poškodit maximální velikost okna? Existují statistiky pro náhled? Udělat číslo proměnlivé na základě toho, kolik si myslíme, že potřebují? Mohou žádat o více? žádat o množství?

- Prozkoumat zvýšení maximální velikosti SSU (zvýšením MTU?)

- Hodně testování

- Nakonec zkontrolovat vylepšení fragmentátoru? - Nejprve je třeba provést porovnávací testování!
