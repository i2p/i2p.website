---
title: "Posuňte své I2P dovednosti na vyšší úroveň díky šifrovaným LeaseSets"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "Říká se, že I2P klade důraz na skryté služby; zkoumáme jednu interpretaci toho"
categories: ["general"]
API_Translate: pravda
---

## Posuňte své dovednosti v I2P na vyšší úroveň pomocí šifrovaných LeaseSets

V minulosti se říkalo, že I2P klade důraz na podporu skrytých služeb, což je v mnoha ohledech pravda. Co to však znamená pro uživatele, vývojáře a správce skrytých služeb, není vždy stejné. Šifrované LeaseSets a jejich případy použití poskytují jedinečný, praktický vhled do toho, jak I2P činí skryté služby všestrannějšími, snáze spravovatelnými a jak I2P rozšiřuje koncept skrytých služeb, aby poskytovalo bezpečnostní výhody pro potenciálně zajímavé případy použití.

## Co je to LeaseSet?

Když vytvoříte skrytou službu, zveřejníte v I2P NetDB něco, čemu se říká "LeaseSet". "LeaseSet" je, v nejjednodušších slovech, to, co ostatní uživatelé I2P potřebují k tomu, aby zjistili "kde" se vaše skrytá služba v síti I2P nachází. Obsahuje "Leases", které identifikují tunnels, jež lze použít k dosažení vaší skryté služby, a veřejný klíč vaší destinace, který budou klienti používat k šifrování zpráv. Tento typ skryté služby je dostupný komukoli, kdo má adresu, což je zatím pravděpodobně nejběžnější scénář použití.

Někdy však nemusíte chtít, aby byly vaše skryté služby přístupné komukoli. Někteří lidé používají skryté služby jako způsob přístupu k SSH serveru na domácím PC nebo k propojení IoT zařízení do sítě. V takových případech není nutné, a může být dokonce kontraproduktivní, aby byla vaše skrytá služba přístupná každému v síti I2P. Právě zde přicházejí ke slovu "Encrypted LeaseSets".

## Šifrované LeaseSets: VELMI skryté služby

Šifrované LeaseSets jsou LeaseSets, které jsou publikovány do NetDB v šifrované podobě, kde žádné Leases ani veřejné klíče nejsou viditelné, pokud klient nemá klíče potřebné k dešifrování v něm obsaženého LeaseSet. Pouze klienti, s nimiž sdílíte klíče(For PSK Encrypted LeaseSets), nebo kteří sdílejí své klíče s vámi(For DH Encrypted LeaseSets), budou moci vidět destinaci a nikdo jiný.

I2P podporuje několik strategií pro šifrované LeaseSets. Při rozhodování, kterou použít, je důležité porozumět klíčovým charakteristikám každé strategie. Pokud šifrovaný LeaseSet používá strategii "Pre-Shared Key(PSK; předem sdílený klíč)", pak server vygeneruje klíč (nebo klíče), který provozovatel serveru následně sdílí s každým klientem. Samozřejmě, tato výměna musí proběhnout out-of-band (mimo hlavní kanál), například přes IRC. Tato verze šifrovaných LeaseSets je tak trochu jako přihlášení k Wi-Fi pomocí hesla. Jenže to, kam se přihlašujete, je skrytá služba.

Pokud Encrypted LeaseSet používá "Diffie-Hellman(DH) strategii, pak se klíče generují na straně klienta. Když se Diffie-Hellman klient připojí k destinaci s Encrypted LeaseSet, musí nejprve sdílet své klíče s provozovatelem serveru. Provozovatel serveru pak rozhodne, zda klienta DH autorizuje. Tato verze Encrypted LeaseSets je tak trochu jako SSH se souborem `authorized_keys`. Až na to, že to, kam se přihlašujete, je skrytá služba.

Šifrováním svého LeaseSetu nejen znemožníte neoprávněným uživatelům připojit se k vaší destination (cílovému identifikátoru v I2P), ale také znemožníte neoprávněným návštěvníkům vůbec zjistit skutečnou destination I2P Hidden Service (skryté služby v I2P). Někteří čtenáři už pravděpodobně zvažovali konkrétní případ použití pro svůj vlastní Šifrovaný LeaseSet.

## Použití šifrovaných LeaseSets pro bezpečný přístup ke konzoli routeru

Obecně platí, že čím podrobnější informace má služba k dispozici o vašem zařízení, tím nebezpečnější je vystavit takovou službu Internetu nebo dokonce síti skrytých služeb, jako je I2P. Pokud chcete takovou službu zpřístupnit, musíte ji chránit například heslem, nebo v případě I2P může být mnohem důkladnější a bezpečnější možností šifrovaný LeaseSet.

**Než budete pokračovat, přečtěte si, prosím, a pochopte, že pokud provedete následující postup bez Encrypted LeaseSet, zmaříte zabezpečení svého I2P routeru. Nekonfigurujte přístup ke konzoli svého routeru přes I2P bez Encrypted LeaseSet. Dále nesdílejte PSK svého Encrypted LeaseSet s žádnými zařízeními, která nemáte pod kontrolou.**

Mezi služby, které je užitečné sdílet přes I2P, ovšem POUZE se šifrovaným LeaseSetem, patří i samotná konzole I2P routeru. Zpřístupnění konzole I2P routeru z jednoho počítače do I2P pomocí šifrovaného LeaseSetu umožní jinému počítači s prohlížečem spravovat vzdálenou instanci I2P. Považuji to za užitečné pro vzdálené monitorování mých běžných služeb I2P. Lze to rovněž použít k monitorování serveru, který se používá k dlouhodobému seedování torrentu, jako způsob přístupu k I2PSnark.

I když jejich vysvětlení může chvíli trvat, nastavení Encrypted LeaseSet je jednoduché nakonfigurovat prostřednictvím Hidden Services Manager UI (uživatelské rozhraní správce skrytých služeb).

## Na "Serveru"

Začněte otevřením Správce skrytých služeb na adrese http://127.0.0.1:7657/i2ptunnelmgr a přejděte na konec oddílu s názvem "I2P Hidden Services." Vytvořte novou skrytou službu s hostitelem "127.0.0.1" a portem "7657", s těmito "Tunnel Cryptography Options", a skrytou službu uložte.

Poté vyberte svůj nový tunnel na hlavní stránce Správce skrytých služeb. Možnosti kryptografie tunnelu by nyní měly zahrnovat váš první Pre-Shared Key (předem sdílený klíč). Zkopírujte si jej pro další krok spolu se šifrovanou adresou Base32 vašeho tunnelu.

## Na straně „klienta“

Teď přepněte na počítač klienta, který se připojí ke skryté službě, a navštivte stránku Konfigurace klíčenky na adrese http://127.0.0.1:7657/configkeyring, abyste přidali dříve získané klíče. Začněte vložením Base32 ze serveru do pole označeného: "Plná destinace, název, Base32 nebo hash." Dále vložte předem sdílený klíč ze serveru do pole "Šifrovací klíč". Klikněte na Uložit a můžete bezpečně navštívit skrytou službu; použije se šifrovaný LeaseSet (záznam dostupnosti v I2P).

## Nyní jste připraveni vzdáleně spravovat I2P

Jak je vidět, I2P nabízí správcům skrytých služeb jedinečné možnosti, které jim umožňují odkudkoli na světě bezpečně spravovat jejich I2P připojení. Další Encrypted LeaseSets, které ze stejného důvodu uchovávám na tomtéž zařízení, směřují na SSH server, instanci Portaineru, kterou používám ke správě svých kontejnerů služeb, a na moji osobní instanci NextCloudu. S I2P je opravdu soukromé, vždy dostupné vlastní hostování dosažitelným cílem; ve skutečnosti si myslím, že je to jedna z věcí, k nimž jsme díky Encrypted LeaseSets jedinečně předurčeni. Díky nim by se I2P mohlo stát klíčem k zabezpečení samohostované automatizace domácnosti, nebo se jednoduše stát páteří nového, soukromějšího peer-to-peer webu.
