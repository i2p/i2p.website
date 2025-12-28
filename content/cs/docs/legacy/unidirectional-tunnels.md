---
title: "Jednosměrné tunnels"
description: "Historické shrnutí architektury jednosměrného tunnelu v I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Historická poznámka:** Tato stránka pro referenci uchovává starší diskusi „Unidirectional Tunnels“. Pro aktuální chování nahlédněte do aktivní [dokumentace implementace tunnel](/docs/specs/implementation/).

## Přehled

I2P vytváří **jednosměrné tunnels**: jeden tunnel přenáší odchozí provoz a samostatný tunnel přenáší příchozí odpovědi. Tato struktura sahá až k nejranějším návrhům sítě a nadále představuje klíčový odlišující prvek oproti systémům s obousměrnými okruhy, jako je Tor. Pro terminologii a podrobnosti o implementaci viz [přehled tunnel](/docs/overview/tunnel-routing/) a [specifikace tunnel](/docs/specs/implementation/).

## Kontrola

- Jednosměrné tunnels udržují provoz požadavků a odpovědí odděleně, takže jakákoli jednotlivá skupina spolupracujících peers (účastníků sítě) pozoruje jen polovinu cesty tam a zpět.
- Časovací útoky musejí protnout dva pooly tunnelů (odchozí a příchozí) namísto analýzy jediného okruhu, což zvyšuje náročnost korelace.
- Nezávislé příchozí a odchozí pooly umožňují routers ladit latenci, kapacitu a chování při selháních pro každý směr.
- Mezi nevýhody patří vyšší složitost správy peers a potřeba udržovat více sad tunnelů pro spolehlivé poskytování služby.

## Anonymita

Článek Hermanna a Grothoffa, [*I2P je pomalé… a co s tím dělat*](http://grothoff.org/christian/i2p.pdf), analyzuje útoky předchůdce proti jednosměrným tunnels a naznačuje, že odhodlaní protivníci mohou postupem času potvrdit dlouhodobě aktivní uzly. Zpětná vazba komunity upozorňuje, že studie se opírá o specifické předpoklady týkající se trpělivosti protivníka a jeho právních pravomocí a neporovnává tento přístup s časovacími útoky, které dopadají na obousměrné návrhy. Pokračující výzkum a praktické zkušenosti nadále posilují jednosměrné tunnels jako záměrnou volbu pro anonymitu, nikoli jako opomenutí.
