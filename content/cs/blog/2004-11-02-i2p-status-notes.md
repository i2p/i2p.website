---
title: "Stavové poznámky I2P ze dne 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující stav sítě, optimalizace paměti v jádru, bezpečnostní opravy směrování tunnelů, pokrok knihovny pro streamování a novinky v poště/BitTorrentu"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

## Rejstřík:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) Stav sítě

Víceméně jako dřív - stálý počet peerů, eepsites(I2P Sites) poměrně dobře dosažitelné a IRC funguje celé hodiny v kuse. Na dosažitelnost různých eepsites(I2P Sites) se můžete podívat na několika různých stránkách: - `http://gott.i2p/sites.html` - `http://www.baffled.i2p/links.html` - `http://thetower.i2p/pings.txt`

## 2) Aktualizace jádra

Ti, kdo se zdržují na kanálu (nebo čtou logy CVS), už viděli, že se děje spousta věcí, i když od posledního vydání uplynula už nějaká doba. Úplný seznam změn od vydání 0.4.1.3 najdete online, ale jsou tu dvě zásadní změny, jedna dobrá a jedna špatná:

Dobrá zpráva je, že jsme dramaticky snížili zátěž paměti způsobenou všemožným šíleným vytvářením dočasných objektů. Už mě definitivně přestalo bavit dívat se, jak GC (garbage collector) šílí při ladění nové streamingové knihovny, takže po pár dnech profilování, úprav a ladění se nám podařilo ty nejošklivější části vyčistit.

Ta horší je oprava chyby v tom, jak jsou zpracovávány některé zprávy směrované přes tunnel – v některých situacích byla zpráva odeslána přímo na cílový router místo toho, aby byla před doručením směrována přes tunnel, což mohl zneužít protivník, který umí trochu programovat. Nyní v případě pochybností správně směrujeme přes tunnel.

To může znít dobře, ale ta 'špatná' část je, že to znamená určité zvýšení latence kvůli dalším hopům, ačkoli jsou to hopy, které se stejně musely použít.

V jádru zároveň probíhá další ladění, takže zatím nevyšlo žádné oficiální vydání - CVS HEAD je 0.4.1.3-8. V příštích několika dnech pravděpodobně vydáme verzi 0.4.1.4, jen abychom všechny ty věci dořešili. Samozřejmě nebude obsahovat novou streaming lib (streamovací knihovnu).

## 3) Streamovací knihovna

Co se týče streamovací knihovny, došlo zde k velkému pokroku a srovnání staré a nové knihovny vedle sebe vypadá dobře. Stále je ale co dělat a, jak jsem uvedl minule, nebudeme to pouštět ven narychlo. To však znamená, že se roadmapa zpozdila, pravděpodobně o 2–3 týdny. Více podrobností, jakmile budou k dispozici.

## 4) pokrok mail.i2p

Spousta novinek tento týden - fungující inproxy i outproxy! Viz www.postman.i2p pro více informací.

## 5) Průběh BT

V poslední době byla zvýšená aktivita kolem portování BitTorrent klienta a aktualizace některých nastavení trackeru. Možná během setkání získáme od zúčastněných nějaké aktuality.

## 6) ???

To je ode mě všechno. Omlouvám se za zpoždění, úplně jsem zapomněl na tu celou věc s letním časem. Každopádně, uvidíme se za chvilku.

=jr
