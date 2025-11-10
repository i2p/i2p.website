---
title: "Stavové poznámky I2P k 22. 3. 2005"
date: 2005-03-22
author: "jr"
description: "Týdenní poznámky ke stavu vývoje I2P zahrnující vydání 0.5.0.3, implementaci dávkování zpráv pro tunnel a nástroje pro automatické aktualizace"
categories: ["status"]
---

Ahoj všichni, krátká aktualizace stavu

* Index

1) 0.5.0.3 2) seskupování do dávek 3) aktualizace 4) ???

* 0.5.0.3

Nové vydání je venku a většina z vás aktualizovala poměrně rychle – díky! Došlo k opravám chyb v různých oblastech, ale nic revolučního – největší změnou bylo odpojení uživatelů verzí 0.5 a 0.5.0.1 od sítě. Od té doby sleduji chování sítě, probírám se tím, co se děje, a i když došlo k určitému zlepšení, pořád je ještě pár věcí, které je potřeba dořešit.

Během příštího dne nebo dvou vyjde nové vydání s opravou chyby, na kterou zatím nikdo nenarazil, ale která rozbíjí nový kód pro dávkové zpracování. K dispozici budou také některé nástroje pro automatizaci procesu aktualizace podle preferencí uživatele, spolu s dalšími drobnostmi.

* batching

Jak jsem zmínil na svém blogu, je prostor pro dramatické snížení šířky pásma a počtu zpráv vyžadovaných v síti pomocí velmi jednoduchého dávkování tunnel messages – místo abychom každou I2NP message, bez ohledu na velikost, vkládali do samostatného tunnel message, můžeme s krátkým zpožděním sloučit až 15 nebo i více do jediného tunnel message. Největší přínosy to přinese u služeb, které používají malé zprávy (například IRC), zatímco velké přenosy souborů to příliš neovlivní. Kód pro dávkování byl implementován a otestován, ale bohužel je na produkční síti chyba, která by způsobila ztrátu všech I2NP message kromě té první uvnitř jednoho tunnel message. Proto vydáme přechodné vydání s touto opravou a přibližně o týden později na něj naváže vydání s dávkováním.

* updating

V tomto průběžném vydání budeme dodávat část často diskutovaného kódu 'autoupdate'. Máme nástroje pro pravidelnou kontrolu autentických oznámení o aktualizacích, stažení aktualizace buď anonymně, nebo ne, a následně její instalaci, nebo pouze zobrazení oznámení na router console, že je připravena a čeká na instalaci. Samotná aktualizace nyní použije smegheadův nový formát podepsané aktualizace, což je v podstatě aktualizace plus DSA podpis. Klíče použité k ověření tohoto podpisu budou součástí I2P a budou i konfigurovatelné na router console.

Výchozí chování bude spočívat v tom, že se budou v pravidelných intervalech pouze kontrolovat oznámení o aktualizacích, ale nebude se podle nich jednat - na konzoli routeru se jen zobrazí funkce „Aktualizovat nyní“ na jedno kliknutí. Existuje spousta dalších scénářů pro různé potřeby uživatelů, ale doufejme, že všechny budou zohledněny prostřednictvím nové konfigurační stránky.

* ???

I'm feeling a bit under the weather, so the above doesn't really go into all the detail about whats up.  Swing on by the meeting and fill in the gaps :)

Mimochodem, během příštího dne nebo dvou také zveřejním nový PGP klíč pro sebe (protože tomuto brzy vyprší platnost...), takže to sledujte.

=jr
