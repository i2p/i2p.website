---
title: "Proces návrhov I2P"
number: "001"
author: "str4d"
created: "2016-04-10"
lastupdated: "2017-04-07"
status: "Meta"
thread: "http://zzz.i2p/topics/1980"
---

## Přehled

Tento dokument popisuje, jak změnit specifikace I2P, jak fungují návrhy I2P a vztah mezi návrhy I2P a specifikacemi.

Tento dokument je přizpůsoben z procesu návrhů Tor a velká část níže uvedeného obsahu byla původně napsána Nickem Mathewsonem.

Jedná se o informační dokument.

## Motivace

Dříve byl náš proces pro aktualizaci specifikací I2P poměrně neformální: vytvořili jsme návrh na vývojovém fóru a diskutovali o změnách, poté jsme dosáhli konsensu a opravili specifikaci návrhem změn (ne nutně v tomto pořadí) a nakonec jsme implementovali změny.

To mělo několik problémů.

Za prvé, i při své nejefektivnější podobě byl starý proces často mimo synchronizaci se specifikací. Nejhorší případy byly ty, kdy byla implementace odložena: specifikace a kód mohly zůstat mimo synchronizaci po několik verzí.

Za druhé, bylo obtížné se zapojit do diskuze, protože nebylo vždy jasné, které části diskusního vlákna byly součástí návrhu nebo které změny ve specifikaci byly implementovány. Vývojová fóra jsou také přístupná pouze uvnitř I2P, což znamená, že návrhy mohl vidět jen ten, kdo používá I2P.

Za třetí, bylo velmi snadné na některé návrhy zapomenout, protože by se zaryly několik stránek zpět v seznamu vláken fóra.

## Jak nyní změnit specifikace

Nejprve někdo napíše dokument návrhu. Ten by měl podrobně popsat změnu, která by měla být provedena, a poskytnout nějaké představy o tom, jak ji implementovat. Když je návrh dostatečně promyšlen, stává se návrhem.

Stejně jako RFC každý návrh dostane číslo. Na rozdíl od RFC se návrhy mohou v průběhu času měnit a zachovat si stejné číslo, dokud nejsou konečně přijaty nebo odmítnuty. Historie pro každý návrh bude uložena v repozitáři webové stránky I2P.

Jakmile je návrh v repozitáři, měli bychom o něm diskutovat v odpovídajícím vlákně a zlepšovat ho, dokud nedosáhneme konsensu, že je to dobrý nápad a že je dostatečně podrobný k implementaci. Když se tak stane, implementujeme návrh a začleníme jej do specifikací. Tím zůstávají specifikace kanonickou dokumentací pro protokol I2P: žádný návrh nikdy není kanonickou dokumentací pro implementovanou funkci.

(Tento proces je docela podobný procesu vylepšení Pythonu, s hlavní výjimkou, že návrhy I2P jsou po implementaci znovu integrovány do specifikací, zatímco PEPy *se stávají* novou specifikací.)

### Malé změny

Stále je v pořádku provádět malé změny přímo ve specifikaci, pokud může být kód napsán více méně okamžitě, nebo kosmetické změny, pokud není nutná žádná změna kódu. Tento dokument odráží aktuální *záměr* vývojářů, nikoli trvalý slib, že tento proces bude vždy používán v budoucnu: vyhrazujeme si právo dostat se skutečně nadšení a rozběhnout se, a něco implementovat při nočním maratonu napájeném kofeinem nebo M&M.

## Jak se přidávají nové návrhy

Chcete-li podat návrh, zveřejněte ho na vývojovém fóru nebo zadejte lístek s přiloženým návrhem.

Jakmile je nápad navržen, existuje správně formátovaný (viz níže) návrh a existuje hrubý konsenzus aktivní vývojové komunity, že tento nápad stojí za zvážení, návrhoví editoři oficiálně přidají návrh.

Aktuálními návrhovými editory jsou zzz a str4d.

## Co by mělo být v návrhu

Každý návrh by měl mít záhlaví obsahující tyto pole:

```
:author:
:created:
:thread:
:lastupdated:
:status:
```

- Pole `author` by mělo obsahovat jména autorů tohoto návrhu.
- Pole `thread` by mělo být odkazem na vlákno vývojového fóra, kde byl tento návrh původně zveřejněn, nebo na nové vlákno vytvořené pro diskuzi o tomto návrhu.
- Pole `lastupdated` by mělo být zpočátku stejné jako pole `created` a mělo by být aktualizováno, kdykoli se návrh změní.

Tato pole by měla být nastavena, když je to nezbytné:

```
:supercedes:
:supercededby:
:editor:
```

- Pole `supercedes` je čárkou oddělený seznam všech návrhů, které tento návrh nahrazuje. Tyto návrhy by měly být odmítnuty a měly by mít pole `supercededby` nastaveno na číslo tohoto návrhu.
- Pole `editor` by mělo být nastaveno, pokud se v tomto návrhu provedou podstatné změny, které podstatně nemění jeho obsah. Pokud se obsah podstatně mění, buď by měl být přidán další `author`, nebo by měl být vytvořen nový návrh nahrazující tento.

Tato pole jsou volitelná, ale doporučená:

```
:target:
:implementedin:
```

- Pole `target` by mělo popisovat, ve které verzi je plánováno, že bude návrh implementován (pokud je Otevřený nebo Přijatý).
- Pole `implementedin` by mělo popisovat, ve které verzi byl návrh implementován (pokud je Dokončený nebo Uzavřený).

Tělo návrhu by mělo začínat sekcí Přehled, která vysvětluje, o čem návrh je, co dělá a v jakém je stavu.

Po Přehledu se návrh stává více volnou formou. V závislosti na jeho délce a složitosti může návrh rozdělit na sekce podle potřeby, nebo sledovat krátký diskurzivní formát. Každý návrh by měl obsahovat alespoň následující informace před jeho přijetím, ačkoli informace nemusí být v sekcích s těmito jmény.

**Motivace**
: Jaký problém se návrh snaží vyřešit? Proč na tomto problému záleží? Pokud je možné několik přístupů, proč zvolit tento?

**Návrh**
: Vysoká úroveň toho, co jsou nové nebo upravené funkce, jak nové nebo upravené funkce fungují, jak vzájemně interagují a jak interagují se zbytkem I2P. To je hlavní část návrhu. Některé návrhy začnou pouze s Motivací a Návrhem a čekají na specifikaci, dokud se Návrh nejeví přibližně správně.

**Bezpečnostní důsledky**
: Jaké účinky mohou navrhované změny mít na anonymitu, jak dobře jsou tyto účinky pochopeny atd.

**Specifikace**
: Podrobný popis toho, co je potřeba přidat do specifikací I2P, aby bylo možné návrh implementovat. To by mělo být přibližně stejně podrobné jako specifikace, které nakonec obsahují: mělo by být možné pro nezávislé programátory napsat vzájemně kompatibilní implementace návrhu na základě jeho specifikací.

**Kompatibilita**
: Budou verze I2P, které budou následovat návrh, kompatibilní s verzemi, které nebudou? Pokud ano, jak bude dosaženo kompatibility? Obecně se snažíme, aby nedocházelo ke ztrátě kompatibility, pokud je to možné; od března 2008 jsme neprovedli žádnou změnu typu "flag day" a nechceme dělat další.

**Implementace**
: Pokud bude návrh obtížné implementovat v současné architektuře I2P, dokument může obsahovat nějakou diskuzi o tom, jak to udělat, aby fungoval. Skutečné opravy by měly být na veřejných větvích monotone nebo nahrány do Trac.

**Poznámky k výkonu a škálovatelnosti**
: Pokud bude mít funkce vliv na výkon (v RAM, CPU, šířce pásma) nebo škálovatelnost, měla by být provedena nějaká analýza toho, jak významný bude tento vliv, abychom se vyhnuli opravdu drahým regresím výkonu a abychom neztráceli čas na nevýznamné zisky.

**Reference**
: Pokud návrh odkazuje na externí dokumenty, měly by být uvedeny.

## Stav návrhu

**Otevřený**
: Návrh je v diskuzi.

**Přijatý**
: Návrh je kompletní a máme v úmyslu ho implementovat. Po tomto bodě by se měly vyhnout podstatným změnám návrhu a měly by být vnímány jako známka selhání procesu někde.

**Dokončený**
: Návrh byl přijat a implementován. Po tomto bodě by se návrh neměl měnit.

**Uzavřený**
: Návrh byl přijat, implementován a sloučen do hlavních specifikačních dokumentů. Návrh by se neměl měnit po tomto bodě.

**Odmítnutý**
: Nechystáme se implementovat funkci, jak je popsáno zde, i když můžeme udělat nějakou jinou verzi. Podrobnosti viz komentáře v dokumentu. Návrh by neměl být změněn po tomto bodě; chcete-li vznést jinou verzi myšlenky, napište nový návrh.

**Návrh**
: Toto ještě není kompletní návrh; existují zjevné chybějící části. Prosím, nepřidávejte žádné nové návrhy s tímto stavem; dejte je místo toho do podadresáře "nápady".

**Potřebuje-revizi**
: Myšlenka pro návrh je dobrá, ale návrh, jak stojí, má vážné problémy, které brání jeho přijetí. Podrobnosti viz komentáře v dokumentu.

**Mrtvý**
: Návrh nebyl po dlouhou dobu dotčen, a nevypadá to, že by ho někdo brzy dokončil. Může se stát znovu "Otevřeným", pokud získá nového prosazovatele.

**Potřebuje-výzkum**
: Před tím, než bude jasné, zda je návrh dobrým nápadem, je třeba vyřešit výzkumné problémy.

**Meta**
: Toto není návrh, ale dokument o návrzích.

**Rezervovat**
: Tento návrh není něco, co bychom v současné době plánovali realizovat, ale mohli bychom ho chtít vzkřísit někdy, pokud se rozhodneme udělat něco podobného tomu, co navrhuje.

**Informační**
: Tento návrh je posledním slovem v tom, co dělá. Nezmění se na specifikaci, pokud ho někdo nezkopíruje a nevloží do nové specifikace pro nový subsystém.

Editoři udržují správný stav návrhů na základě hrubého konsensu a vlastního uvážení.

## Číslování návrhů

Čísla 000-099 jsou vyhrazena pro speciální a meta-návrhy. 100 a více se používá pro skutečné návrhy. Čísla nejsou recyklována.

## Reference

- [Proces návrhov Tor](https://gitweb.torproject.org/torspec.git/tree/proposals/001-process.txt)
