---
title: "Zrychlení vaší sítě I2P"
date: 2019-07-27
author: "mhatta"
description: "Zrychlení vaší sítě I2P"
categories: ["tutorial"]
---

*Tento příspěvek byl přímo převzat a upraven z materiálu původně vytvořeného pro mhattaův* [blog na Medium](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Zásluhy za původní příspěvek patří jemu. Byl aktualizován na některých místech, kde* *odkazuje na staré verze I2P jako na aktuální, a prošel drobnými* *úpravami. -idk*

Hned po spuštění se I2P často jeví jako trochu pomalé. Je to pravda a všichni víme proč: ze své podstaty [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) (technika směrování používaná v I2P pro soukromí) přidává režii k běžnému používání internetu, abyste měli soukromí, což však znamená, že u mnoha nebo dokonce většiny služeb I2P budou vaše data muset ve výchozím nastavení projít dvanácti skoky.

![Analýza nástrojů pro anonymitu na internetu](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Kromě toho, na rozdíl od Toru, byl I2P primárně navržen jako uzavřená síť. K [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) nebo dalším zdrojům uvnitř I2P lze snadno přistupovat, ale k webům na [clearnetu](https://en.wikipedia.org/wiki/Clearnet_(networking)) by se přes I2P přistupovat nemělo. Existuje několik I2P "outproxies" (výstupní proxy) podobných výstupním uzlům sítě [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)) pro přístup na clearnet, ale většina z nich je velmi pomalá, protože cesta na clearnet je fakticky *další* skok v rámci spojení, které už samo o sobě má 6 skoků dovnitř a šest skoků ven.

Ještě před několika verzemi byl tento problém mnohem obtížnější řešit, protože mnoho uživatelů I2P routeru mělo potíže s konfigurací nastavení šířky pásma u svých routerů. Pokud si každý, kdo může, najde čas a správně upraví nastavení šířky pásma, zlepší tím nejen vaše připojení, ale i síť I2P jako celek.

## Úprava limitů šířky pásma

Protože I2P je síť peer-to-peer, musíte sdílet část své šířky pásma s ostatními uzly. Množství si můžete zvolit v "I2P Bandwidth Configuration" (tlačítko "Configure Bandwidth" v sekci "Applications and Configuration" v I2P Router Console, nebo http://localhost:7657/config).

![Konfigurace šířky pásma I2P](https://geti2p.net/images/blog/bandwidthmenu.png)

Pokud vidíte limit sdílené šířky pásma 48 KBps, který je velmi nízký, pak jste možná nezměnili výchozí nastavení sdílené šířky pásma. Jak poznamenal původní autor materiálu, ze kterého byl tento blogový příspěvek adaptován, I2P má výchozí limit sdílené šířky pásma, který je velmi nízký, dokud si jej uživatel neupraví, aby se předešlo problémům s uživatelovým připojením.

Nicméně, protože mnoho uživatelů nemusí přesně vědět, která nastavení šířky pásma upravit, [vydání I2P 0.9.38](https://geti2p.net/en/download) představilo Průvodce novou instalací. Obsahuje Test šířky pásma, který (díky [NDT](https://www.measurementlab.net/tests/ndt/) od M‑Lab) automaticky zjistí a tomu přizpůsobí nastavení šířky pásma I2P.

Pokud chcete znovu spustit průvodce, například po změně svého poskytovatele internetových služeb nebo proto, že jste nainstalovali I2P před verzí 0.9.38, můžete jej znovu spustit prostřednictvím odkazu 'Setup' na stránce 'Help & FAQ', anebo se k průvodci jednoduše dostat přímo na adrese http://localhost:7657/welcome

![Najdete „Setup“?](https://geti2p.net/images/blog/sidemenu.png)

Používání Průvodce je jednoduché, stačí stále klikat na "Další". Někdy jsou vybrané měřicí servery M-Labu nedostupné a test selže. V takovém případě klikněte na "Předchozí" (nepoužívejte ve svém webovém prohlížeči tlačítko "Zpět"), poté to zkuste znovu.

![Výsledky testu šířky pásma](https://geti2p.net/images/blog/bwresults.png)

## Nepřetržitý provoz I2P

I po upravení šířky pásma může být vaše připojení stále pomalé. Jak jsem zmínil, I2P je P2P síť. Chvíli trvá, než je váš I2P router objeven ostatními uzly a začleněn do sítě I2P. Pokud váš router neběží dostatečně dlouho, aby se dobře integroval, nebo jej příliš často ukončujete nekorektně, zůstane síť poměrně pomalá. Naopak čím déle necháte svůj I2P router běžet nepřetržitě, tím rychlejší a stabilnější bude vaše připojení a tím více vašeho podílu šířky pásma bude v síti využito.

Nicméně mnoho lidí nemusí být schopno udržet svůj I2P router v provozu. V takovém případě můžete stále spustit I2P router na vzdáleném serveru, například na VPS, a poté použít SSH přesměrování portů.
