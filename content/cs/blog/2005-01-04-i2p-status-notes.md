---
title: "Poznámky ke stavu I2P k 2005-01-04"
date: 2005-01-04
author: "jr"
description: "První týdenní poznámky o stavu v roce 2005, pokrývající růst sítě na 160 routers, funkce verze 0.4.2.6 a vývoj verze 0.5"
categories: ["status"]
---

Ahoj všichni, je čas na naše první týdenní shrnutí stavu v roce 2005

* Index

1) Stav sítě 2) 0.4.2.6 3) 0.5 4) jabber @ chat.i2p 5) ???

* 1) Net status

Za poslední týden se na síti děly docela zajímavé věci – na Silvestra se na populárním webu objevily komentáře o i2p-bt a zaznamenali jsme menší příliv nových uživatelů. V tuto chvíli je v síti mezi 120-150 routerů, i když před pár dny to vyletělo až na 160. Síť to však ustála; peery s vysokou kapacitou převzaly přebytečné zatížení bez většího narušení ostatních peerů. Někteří uživatelé bez omezení šířky pásma na opravdu rychlých linkách hlásí propustnost 2-300KBps, zatímco ti s menší kapacitou dosahují obvyklých nízkých 1-5KBps.

Myslím, že si pamatuji Connellyho poznámku, že během několika dnů po Novém roce viděl více než 300 různých routerů, takže docházelo k výrazné fluktuaci. Na druhou stranu nyní máme stabilně 120–150 uživatelů online, na rozdíl od dřívějších 80–90, což je rozumný nárůst. Stále však *nechceme*, aby to zatím příliš rostlo, protože jsou známy implementační problémy, které je ještě potřeba vyřešit. Konkrétně do vydání verze 0.6 [1] budeme chtít zůstat pod 200–300 peerů (uzlů), aby počet vláken zůstal na rozumné úrovni. Nicméně pokud by někdo chtěl pomoci s implementací UDP transportu, můžeme toho dosáhnout mnohem rychleji.

Za poslední týden jsem sledoval statistiky, které zveřejňují trackery i2p-bt, a byly přeneseny gigabajty velkých souborů; některé zprávy uvádějí 80–120KBps. IRC mělo od chvíle, kdy byly na tom webu zveřejněny ty komentáře, více výpadků než obvykle, ale stále jde o rozestupy v řádu hodin mezi jednotlivými odpojeními. (podle toho, co mohu usuzovat, router, na kterém běží irc.duck.i2p, pracuje poměrně blízko svému limitu šířky pásma, což by to vysvětlovalo)

[1] http://www.i2p.net/roadmap#0.6

* 2) 0.4.2.6

Od vydání 0.4.2.5 bylo do CVS přidáno několik oprav a nových funkcí, které budeme chtít brzy nasadit, včetně oprav zvyšujících spolehlivost streamingové knihovny, zvýšené odolnosti vůči změně IP adresy a začlenění implementace knihy adres od ragnaroka.

Pokud jste o addressbooku (adresáři) neslyšeli nebo jste jej nepoužívali, stručně řečeno bude automaticky aktualizovat váš soubor hosts.txt pravidelným stahováním a slučováním změn z některých anonymně hostovaných umístění (výchozí jsou http://dev.i2p/i2p/hosts.txt a http://duck.i2p/hosts.txt). Nebudete muset měnit žádné soubory, sahat na žádnou konfiguraci ani spouštět žádné další aplikace - bude nasazen uvnitř I2P routeru jako standardní soubor .war.

Samozřejmě, pokud se *opravdu* chcete pustit do addressbooku (adresář adres v I2P) pořádně, jste více než vítáni - viz Ragnarokův web [2] pro podrobnosti. Lidé, kteří už mají addressbook nasazený ve svém routeru, budou muset během upgradu na verzi 0.4.2.6 udělat pár drobných kroků navíc, ale bude fungovat se všemi vašimi starými konfiguračními nastaveními.

[2] http://ragnarok.i2p/

* 3) 0.5

Čísla, čísla, čísla! No, jak už jsem říkal dřív, verze 0.5 přepracuje způsob, jak funguje směrování tunnelů, a v tomto směru se dělá pokrok. Posledních pár dní implementuji nový kód šifrování (a jednotkové testy) a jakmile budou fungovat, zveřejním dokument popisující mé aktuální úvahy o tom, jak, co a proč bude nové směrování tunnelů fungovat. Šifrování do toho zavádím už teď, ne až později, aby si lidé mohli konkrétně posoudit, co to znamená, a zároveň odhalit problematické oblasti a navrhnout zlepšení. Doufám, že do konce týdne bude kód fungovat, takže možná o víkendu přibudou další dokumenty. Ale nic neslibuji.

* 4) jabber @ chat.i2p

jdot spustil nový jabber server a zdá se, že funguje docela dobře jak pro konverzace jeden na jednoho, tak pro skupinový chat. podívejte se na informace na fóru [3]. diskusní kanál vývojářů I2P bude nadále irc #i2p, ale je vždy fajn mít alternativy.

[3] http://forum.i2p.net/viewtopic.php?t=229

* 5) ???

OK, to je asi všechno, co mám momentálně zmínit - jsem si ale jistý, že se děje spousta dalších věcí, které budou chtít ostatní zmínit, takže se stavte na schůzce za 15 minut @ obvyklém místě [4] a dejte nám vědět, co je nového!

=jr
