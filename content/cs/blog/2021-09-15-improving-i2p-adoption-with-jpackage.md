---
title: "Zlepšení adopce a onboardingu (uvedení nových uživatelů) I2P pomocí Jpackage a I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Univerzální a nově se objevující způsoby instalace a integrace I2P do vaší aplikace"
categories: ["general"]
API_Translate: pravda
---

Po většinu své existence bylo I2P aplikací, která běží s pomocí virtuálního stroje Java již nainstalovaného na dané platformě. To byl vždy obvyklý způsob distribuce aplikací v Javě, ale pro mnoho lidí to vede ke komplikovanému instalačnímu postupu. Aby to bylo ještě složitější, "správná odpověď" na to, jak učinit instalaci I2P na jakékoli platformě snadnou, nemusí být stejná jako na jiné platformě. Například na operačních systémech založených na Debianu a Ubuntu je instalace I2P pomocí standardních nástrojů poměrně jednoduchá, protože u našeho balíčku můžeme požadované komponenty Javy jednoduše uvést jako "Required", avšak ve Windows nebo na OSX neexistuje žádný takový systém, který by nám umožnil zajistit, že je nainstalována kompatibilní Java.

Zřejmým řešením by bylo spravovat instalaci Javy sami, ale to bývalo samo o sobě problémem, mimo rámec I2P. Avšak v nedávných verzích Javy se objevila nová sada možností, která má potenciál tento problém vyřešit pro mnoho Java aplikací. Tento zajímavý nástroj se nazývá **"Jpackage."**

## I2P-Zero a instalace I2P bez závislostí

Prvním velmi úspěšným pokusem o vytvoření balíčku I2P bez závislostí byl I2P-Zero, který byl vytvořen projektem Monero původně pro použití s kryptoměnou Monero. Tento projekt nás velmi nadchl díky svému úspěchu: podařilo se mu vytvořit univerzální I2P router, který lze snadno přibalit k aplikaci I2P. Zejména na Redditu mnoho lidí upřednostňuje jednoduché nastavení I2P-Zero router.

To nám skutečně potvrdilo, že s moderními nástroji Javy je možné vytvořit snadno instalovatelný balíček I2P bez závislostí, ale případ použití I2P-Zero byl trochu jiný než náš. Nejlépe se hodí pro vestavěné aplikace, které potřebují I2P router, který mohou snadno ovládat pomocí jeho praktického řídicího portu na portu "8051". Naším dalším krokem by bylo přizpůsobit tuto technologii obecně použitelné aplikaci I2P.

## Změny zabezpečení aplikací v OSX ovlivňují instalační program I2P IzPack

Problém se stal naléhavějším v novějších verzích Mac OSX, kde již není jednoduché použít instalační program "Classic", který je dodáván ve formátu .jar. Důvodem je, že aplikace není "Notarized" autoritami společnosti Apple a je považována za bezpečnostní riziko. **Nicméně**, Jpackage může vytvořit soubor .dmg, který lze autoritami společnosti Apple notarizovat, což náš problém pohodlně řeší.

Nový I2P .dmg instalátor, vytvořený Zlatinbem, usnadňuje instalaci I2P na OSX více než kdy dříve: už nevyžaduje, aby si uživatelé sami instalovali Javu, a využívá standardní instalační nástroje OSX předepsaným způsobem. Nový .dmg instalátor činí nastavení I2P na Mac OSX jednodušším než kdy dříve.

Stáhnout [dmg](https://geti2p.net/en/download/mac)

## I2P budoucnosti se snadno instaluje

Jedna z věcí, kterou od uživatelů slýchám nejčastěji, je, že pokud chce I2P dosáhnout širšího přijetí, musí být pro lidi snadné na používání. Mnozí z nich chtějí uživatelskou zkušenost "jako Tor Browser", řečeno slovy mnoha dobře známých uživatelů Redditu. Instalace by neměla vyžadovat komplikované a k chybám náchylné kroky "post-installation". Mnoho nových uživatelů není připraveno vypořádat se s konfigurací svého prohlížeče důkladně a úplně. Abychom tento problém vyřešili, vytvořili jsme I2P Profile Bundle, který nakonfiguroval Firefox tak, aby pro I2P automaticky "prostě fungoval". V průběhu vývoje přibyly bezpečnostní funkce a zlepšila se integrace se samotným I2P. V nejnovější verzi **také** obsahuje kompletní I2P Router využívající Jpackage. I2P Firefox Profile je nyní plnohodnotná distribuce I2P pro Windows, přičemž jedinou zbývající závislostí je samotný Firefox. To by mělo poskytnout bezprecedentní míru pohodlí pro uživatele I2P ve Windows.

Stáhněte si [instalátor](https://geti2p.net/en/download#windows)
