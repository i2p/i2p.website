---
title: "Stavové poznámky I2P k 2004-11-23"
date: 2004-11-23
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující obnovu sítě, pokrok v testování streamovací knihovny, plány nadcházejícího vydání 0.4.2 a vylepšení adresáře"
categories: ["status"]
---

Ahoj všichni, je čas na aktualizaci stavu

## Rejstřík:

1. Net status
2. Streaming lib
3. 0.4.2
4. Addressbook.py 0.3.1
5. ???

## 1) Stav sítě

Po minulém týdnu s 2-3denním obdobím, kdy byl provoz dost zahlcený, se síť vrátila zpět do normálu (pravděpodobně proto, že jsme přestali provádět zátěžové testy bittorrent portu ;). Od té doby je síť poměrně spolehlivá - opravdu máme pár routers, které jsou v provozu už 30-40+ dní, ale IRC připojení stále mají své občasné problémy. Na druhou stranu...

## 2) Streamovací knihovna

Za poslední zhruba týden jsme prováděli mnohem více testování v reálném provozu streamovací knihovny v síti a vypadá to docela dobře. Duck s ní nastavil tunnel, který mohli lidé použít k přístupu na jeho IRC server, a během několika dní jsem měl jen dvě zbytečná odpojení (což nám pomohlo dohledat některé chyby). Také jsme měli instanci i2ptunnel směřující na squid outproxy (výstupní proxy), kterou lidé zkoušeli, a propustnost, latence i spolehlivost jsou ve srovnání se starou knihovnou, kterou jsme provozovali paralelně, výrazně lepší.

Celkově vzato se streamovací knihovna zdá být v dostatečně dobré kondici na první vydání. Ještě zbývá několik věcí, které nejsou dokončené, ale je to výrazné zlepšení oproti staré knihovně, a musíme vám přece nechat důvod k pozdější aktualizaci, že? ;)

Vlastně, jen abych vás trochu poškádlil (nebo možná inspiroval k vymyšlení nějakých řešení), hlavní věci, které vidím na obzoru pro streaming lib (streamovací knihovna), jsou: - nějaké algoritmy pro sdílení informací o zahlcení a RTT napříč toky (pro target destination? pro source destination? pro všechny lokální destinations?) - další optimalizace pro interaktivní toky (většina pozornosti v současné implementaci je věnována hromadným tokům) - výraznější využití funkcí nové streaming lib v I2PTunnel, což sníží režii na jeden tunnel. - omezování šířky pásma na úrovni klienta (v jednom nebo obou směrech na jednom toku, případně sdílené mezi více toky). Toto by samozřejmě bylo nad rámec celkového omezování šířky pásma routeru. - různé ovládací prvky pro destinations (adresy Destination v I2P), aby mohly omezovat, kolik toků přijmou nebo vytvoří (máme nějaký základní kód, ale z větší části je vypnutý) - seznamy řízení přístupu (povolující toky pouze do/z některých jiných známých destinations) - webové ovládání a monitorování stavu různých toků, stejně jako možnost je explicitně uzavírat nebo omezovat

Určitě vás napadne i pár dalších věcí, ale tohle je jen stručný seznam věcí, které bych rád viděl ve streaming lib (streamingové knihovně), kvůli nimž však nebudu zdržovat vydání 0.4.2. Pokud má někdo o některou z nich zájem, prosím, dejte mi vědět!

## 3) 0.4.2

Takže, pokud je streamingová knihovna v dobrém stavu, kdy to vydáme? Aktuální plán je vydat to do konce týdne, možná dokonce už zítra. Ještě je tu pár dalších věcí, které chci nejdřív dát do pořádku, a samozřejmě je potřeba je otestovat, bla bla bla.

Velkou změnou ve vydání 0.4.2 bude samozřejmě nová streamingová knihovna. Z pohledu API je totožná se starou knihovnou - I2PTunnel a datové proudy SAM ji automaticky používají, ale z pohledu paketů *není* zpětně kompatibilní. To nás staví před zajímavé dilema - v rámci I2P není nic, co by nás nutilo udělat z 0.4.2 povinnou aktualizaci, nicméně lidé, kteří neaktualizují, nebudou moci používat I2PTunnel - žádné eepsites(I2P Sites), žádné IRC, žádný outproxy (výstupní proxy), žádný e‑mail. Nechci odradit naše dlouholeté uživatele tím, že je donutíme aktualizovat, ale také je nechci odradit tím, že se všechno užitečné rozbije ;)

Jsem otevřený argumentům pro obě možnosti – bylo by docela snadné změnit jediný řádek kódu, aby verze 0.4.2 nekomunikovala se staršími verzemi, nebo to prostě můžeme nechat být a lidé budou aktualizovat, až půjdou na web nebo na fórum nadávat, že je všechno rozbité. Co si o tom myslíte?

## 4) AddressBook.py 0.3.1

Ragnarok vydal novou opravnou verzi pro svou aplikaci adresáře kontaktů - viz `http://ragnarok.i2p/` pro více informací (nebo nám snad může poskytnout aktualizaci na schůzce?)

## 5) ???

Vím, že se toho děje mnohem víc – s portací BitTorrentu, susimailem, novou hostingovou službou od slackera a dalšími věcmi. Má někdo ještě něco, co by chtěl zmínit? Pokud ano, stavte se na schůzku za ~30 min na #i2p na obvyklých IRC serverech!

=jr
