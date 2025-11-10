---
title: "Stavové poznámky I2P k 2004-07-20"
date: 2004-07-20
author: "jr"
description: "Týdenní aktualizace stavu zahrnující vydání 0.3.2.3, změny kapacity, aktualizace webových stránek a bezpečnostní hlediska"
categories: ["status"]
---

**1) 0.3.2.3, 0.3.3, and the roadmap**

Po vydání 0.3.2.3 minulý týden jste odvedli skvělou práci s aktualizací – teď máme jen dva opozdilce (jeden na 0.3.2.2 a druhý až na 0.3.1.4 :). Během posledních několika dní byla síť spolehlivější než obvykle – lidé zůstávají na irc.duck.i2p celé hodiny, daří se stahovat větší soubory z eepsites(I2P Sites) a obecná dosažitelnost eepsite(I2P Site) je docela dobrá. Protože to jde dobře a chci vás udržet ve střehu, rozhodl jsem se změnit pár základních konceptů a během jednoho či dvou dnů je nasadíme ve vydání 0.3.3.

Protože se několik lidí vyjádřilo k našemu harmonogramu a zajímalo je, zda stihneme termíny, které jsme zveřejnili, rozhodl jsem se, že bych měl asi aktualizovat web, aby odrážel roadmapu, kterou mám ve svém palmpilotu, takže jsem to udělal [1]. Termíny se posunuly a některé body se přesunuly, ale plán je stále stejný jako ten, o kterém jsme diskutovali minulý měsíc [2].

Verze 0.4 splní čtyři zmíněná kritéria vydání (funkční, bezpečná, anonymní a škálovatelná), i když před verzí 0.4.2 se bude moci zapojit jen málo lidí za NATy a firewally, a před verzí 0.4.3 bude existovat praktický horní limit velikosti sítě kvůli režii spojené s udržováním velkého počtu TCP spojení k dalším routerům.

[1] http://www.i2p.net/redesign/roadmap [2] http://dev.i2p.net/pipermail/i2p/2004-June/000286.html

**2) s/reliability/capacity/g**

Během posledního týdne nebo tak nějak mě lidé na #i2p občas slyšeli, jak se rozčiluji nad tím, že naše hodnocení spolehlivosti je naprosto arbitrární (a nad problémy, které to v posledních několika vydáních způsobilo). Takže jsme se konceptu spolehlivosti úplně zbavili a nahradili ho měřením kapacity - "kolik pro nás může peer udělat?" To mělo vedlejší dopady napříč kódem pro výběr peerů (protějšků v síti) a profilování peerů (a pochopitelně také na router console), ale jinak se toho moc nezměnilo.

Více informací o této změně najdete na revidované stránce výběru peerů [3] a až vyjde verze 0.3.3, vy všichni budete moci vidět dopad na vlastní oči (posledních pár dní jsem si s tím hrál, dolaďoval některá nastavení apod.).

[3] http://www.i2p.net/redesign/how_peerselection

**3) aktualizace webu**

Za poslední týden jsme udělali velký pokrok v redesignu webu [4] - zjednodušujeme navigaci, čistíme některé klíčové stránky, importujeme starý obsah a píšeme několik nových příspěvků [5]. Jsme téměř připraveni nasadit web do ostrého provozu, ale pořád ještě zbývá udělat pár věcí.

Dnes dříve duck prošel web a sestavil seznam stránek, které nám chybí, a po dnešních odpoledních aktualizacích tu zbývá několik nevyřešených problémů, u nichž doufám, že je buď zvládneme vyřešit, nebo se najdou dobrovolníci, kteří se do nich pustí:

* **documentation**: hmm, do we need any content for this? or can we have it just sit as a header with no page behind it?
* **development**: I think this is in the same boat as "documentation" above
* **news**: perhaps we can remove the 'announcements' page and put that content here? or should we do as above and let news be a simple heading, with an announcements page below?
* **i2ptunnel_services, i2ptunnel_tuning, i2ptunnel_lan**: We need someone to rewrite the 'how to set up an eepsite(I2P Site)' page, as well as include answers to the two most frequently asked I2PTunnel questions (how to access it through a LAN and how to configure its tunnels - answers being: -e "listen_on 0.0.0.0" and -e 'clientoptions tunnels.numInbound=1 tunnels.depthInbound=1', respectively) Perhaps we can come up with some more comprehensive user level I2PTunnel documentation?
* **jvm**: er, I'm not sure about this page - is it 'how to tweak the JVM for optimal performance'? do we *know*?
* **config_tweaks**: other config parameters for the router (bandwidth limiting, etc). could someone go through the router.config and take a stab at what everything means? if anyone has any questions, please let me know.
* **more meeting logs**: mihi posted up an archive of some logs, perhaps a volunteer can sift through those and post them up?
* perhaps we can update the meetings.html to be date based and include a link to that week's status update along with any release announcements preceding it?

Kromě toho si myslím, že web je už poměrně blízko tomu, aby byl připraven k nasazení do ostrého provozu. Má někdo v tomto ohledu nějaké návrhy nebo obavy?

[4] http://www.i2p.net/redesign/ [5] http://dev.i2p.net/pipermail/i2pwww/2004-July/thread.html

**4) útoky a obrana**

Connelly přichází s několika novými přístupy, jak se pokusit najít slabiny v zabezpečení a anonymitě sítě, a při tom narazil na způsoby, jak můžeme věci zlepšit. Ačkoli některé aspekty jím popsaných technik se s I2P úplně nekryjí, možná vy ostatní uvidíte, jak je rozvinout tak, aby šly použít k dalším útokům na síť? No tak, zkuste to :)

**5) ???**

To je asi všechno, na co si před dnešní schůzkou vzpomenu – neváhejte zmínit cokoli dalšího, co mi uniklo. Každopádně, sejdeme se za pár minut na #i2p.

=jr
