---
title: "Pomozte svým přátelům připojit se k I2P sdílením Reseed Bundles"
date: 2020-06-07
author: "idk"
description: "Vytvářejte, vyměňujte a používejte balíčky pro reseed"
categories: ["reseed"]
---

Většina nových I2P routerů se do sítě připojuje prostřednictvím bootstrapu za pomoci reseed služby. Reseed služby jsou však centralizované a v porovnání se zbytkem sítě I2P, kde je kladen důraz na decentralizovaná a neblokovatelná spojení, je poměrně snadné je blokovat. Pokud nový I2P router není schopen provést bootstrap, může být možné použít existující I2P router k vygenerování funkčního "Reseed bundle" (balíček pro reseed) a provést bootstrap bez potřeby reseed služby.

Je možné, aby uživatel s funkčním připojením k I2P pomohl zablokovanému routeru připojit se k síti tím, že vygeneruje reseed file a předá jej přes tajný nebo neblokovaný kanál. Ve skutečnosti nebývá v mnoha situacích již připojený I2P router blokováním reseedu vůbec ovlivněn, takže **mít nablízku funkční I2P routery znamená, že stávající I2P routery mohou pomoci novým I2P routerům tím, že jim poskytnou skrytý způsob bootstrappingu (počátečního připojení)**.

## Generování balíčku Reseed

- To create a reseed bundle for others to use, go to the [Reseed configuration page](http://127.0.0.1:7657/configreseed). You will see a section that looks like this. Click the button indicated by the red circle to create a reseed zip.
- Now that you've clicked the button, a zip will be generated containing enough information to bootstrap a new I2P router. Download it and transfer it to the computer with the new, un-bootstrapped I2P router.

## Provedení Reseedu ze souboru

- Obtain an i2preseed.zip file from a friend with an I2P router that is already running, or from a trusted source somewhere on the internet, and visit the [Reseed Configuration page](http://127.0.0.1:7657/configreseed). Click the button that says "Select zip or su3 file" and navigate to that file.
- When you've selected your reseed file, click the "Reseed from File" button. You're done! Your router will now bootstrap using the zip file, and you will be ready to join the I2P network.
