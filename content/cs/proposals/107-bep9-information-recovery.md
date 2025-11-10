---
title: "BEP9 Obnova Informací"
number: "107"
author: "sponge"
created: "2011-02-23"
lastupdated: "2011-02-23"
status: "Mrtvý"
thread: "http://zzz.i2p/topics/860"
---

## Přehled

Tento návrh je o přidání plné obnovy informací do implementace BEP9 v I2P.


## Motivace

BEP9 neposílá celý torrent soubor, čímž ztrácí několik důležitých položek ve slovníku a mění celkový SHA1 torrent souboru. To je špatné pro odkazy na tok Torrent, a to proto, že se ztrácí důležité informace. Seznamy trackerů, komentáře a jakékoli dodatečné údaje jsou pryč. Je důležité mít způsob, jak tyto informace obnovit, a je potřeba přidat k torrent souboru co nejméně. Také to nesmí být kruhově závislé. Obnova informací by neměla žádným způsobem ovlivňovat současné klienty. Torrenty, které nemají tracker (URL trackeru je doslova 'trackerless'), neobsahují dodatečné pole, protože jsou specifické pro použití maggot protokolu pro objevování a stahování, což nevede ke ztrátě informací.


## Řešení

Vše, co je třeba udělat, je zkomprimovat informace, které by se ztratily, a uložit je do info slovníku.


### Implementace
1. Vygenerujte normální info slovník.
2. Vygenerujte hlavní slovník a vynechejte položku info.
3. Zakódujte a zkomprimujte hlavní slovník pomocí gzip.
4. Přidejte zkomprimovaný hlavní slovník do info slovníku.
5. Přidejte info do hlavního slovníku.
6. Zapište torrent soubor.

### Obnova
1. Rozbalte obnovovací pole v info slovníku.
2. Dekódujte obnovovací pole.
3. Přidejte info do obnoveného slovníku.
4. Pro klienty, kteří jsou si vědomi maggot, můžete nyní ověřit, že SHA1 je správný.
5. Zapište obnovený torrent soubor.


## Diskuze

Použitím výše načrtnuté metody je velikost nárůstu torrentu velmi malá,
typicky 200 až 500 bajtů. Robert bude dodávat s novým vytvořením položky info
ve slovníku, a nebude možné ji vypnout. Zde je struktura:

```
hlavní slovník {
    Řetězce trackeru, komentáře, atd...
    info : {
        gzipovaný hlavní bencodeovaný slovník bez slovníku info a všech ostatních
        obvyklých informací
    }
}
```
