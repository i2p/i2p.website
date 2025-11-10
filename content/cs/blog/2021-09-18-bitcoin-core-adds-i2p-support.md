---
title: "Bitcoin Core přidává podporu pro I2P!"
date: 2021-09-18
author: "idk"
description: "Nový případ použití a známka rostoucího přijetí"
categories: ["general"]
API_Translate: pravda
---

Událost, která se připravovala měsíce: Bitcoin Core přidal oficiální podporu pro I2P! Uzly Bitcoin-over-I2P mohou plně komunikovat se zbytkem uzlů Bitcoinu, a to s pomocí uzlů, které fungují jak v I2P, tak v clearnetu, čímž se z nich stávají plnohodnotní účastníci sítě Bitcoinu. Je vzrušující vidět, že si velké komunity jako Bitcoin všímají výhod, které jim I2P může přinést — I2P poskytuje soukromí a dosažitelnost lidem po celém světě.

## Jak to funguje

Podpora I2P je automatická, a to prostřednictvím SAM API. Je to také skvělá zpráva, protože to zdůrazňuje některé věci, ve kterých je I2P výjimečně dobré, například tím, že dává vývojářům aplikací možnost programově a pohodlně vytvářet I2P spojení. Uživatelé Bitcoin-over-I2P mohou používat I2P bez ruční konfigurace tak, že povolí SAM API a spustí Bitcoin s povoleným I2P.

## Konfigurace vašeho I2P Routeru

Aby bylo možné nastavit I2P Router pro poskytování anonymní konektivity k bitcoinu, je potřeba povolit SAM API. V Java I2P byste měli přejít na http://127.0.0.1:7657/configclients a spustit SAM Application Bridge tlačítkem "Start". Také můžete SAM Application Bridge povolit ve výchozím nastavení zaškrtnutím políčka "Run at Startup" a kliknutím na "Save Client Configuration."

V i2pd je SAM API obvykle povoleno ve výchozím nastavení, ale pokud není, měli byste nastavit:

```
sam.enabled=true
```
ve vašem souboru i2pd.conf.

## Konfigurace vašeho bitcoinového uzlu pro anonymitu a konektivitu

Aby bylo možné samotný Bitcoin spustit v anonymním režimu, je stále nutné upravit některé konfigurační soubory v datovém adresáři Bitcoinu, kterým je %APPDATA%\Bitcoin ve Windows, ~/.bitcoin v Linuxu a ~/Library/Application Support/Bitcoin/ v Mac OSX. Dále je vyžadována alespoň verze 22.0.0, aby byla k dispozici podpora I2P.

Po dodržení těchto pokynů budete mít soukromý bitcoinový uzel, který používá I2P pro připojení v rámci I2P a Tor pro připojení k .onion a clearnetu (veřejnému internetu), takže všechna vaše připojení budou anonymní. Pro pohodlí by uživatelé Windows měli otevřít svůj datový adresář Bitcoinu tak, že otevřou nabídku Start a vyhledají „Spustit“. Do okna Spustit napište "%APPDATA%\Bitcoin" a stiskněte Enter.

V daném adresáři vytvořte soubor s názvem "i2p.conf." Ve Windows byste se měli ujistit, že při ukládání uzavřete název souboru do uvozovek, abyste zabránili Windows v přidání výchozí přípony k souboru. Soubor by měl obsahovat následující konfigurační možnosti Bitcoinu související s I2P:

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Dále byste měli vytvořit další soubor s názvem "tor.conf." Soubor by měl obsahovat následující konfigurační volby související s Torem:

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Nakonec budete muset "zahrnout" tyto konfigurační volby do svého konfiguračního souboru Bitcoinu, který se v adresáři Data Directory nazývá "bitcoin.conf". Do souboru bitcoin.conf přidejte tyto dva řádky:

```
includeconf=i2p.conf
includeconf=tor.conf
```
Nyní je váš uzel Bitcoinu nakonfigurován tak, aby používal pouze anonymní připojení. Chcete-li povolit přímá připojení ke vzdáleným uzlům, odstraňte řádky začínající na:

```
onlynet=
```
Můžete to udělat, pokud nevyžadujete, aby byl váš bitcoinový uzel anonymní, a pomůže to anonymním uživatelům připojit se ke zbytku bitcoinové sítě.
