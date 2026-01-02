---
title: "Jak dobrovolně pomoci s bootstrapem (počáteční inicializací) I2P-Bote"
date: 2019-05-20
author: "idk"
description: "Pomozte s inicializací I2P-Bote!"
categories: ["development"]
---

Snadný způsob, jak lidem pomoci posílat si navzájem soukromé zprávy, je provozovat uzel I2P-Bote, který mohou noví uživatelé Bote použít k inicializaci svých vlastních uzlů I2P-Bote. Bohužel až dosud byl proces nastavení počátečního uzlu I2P-Bote mnohem méně srozumitelný, než by měl být. Ve skutečnosti je to velmi jednoduché!

**Co je I2P-bote?**

I2P-bote je systém soukromého zasílání zpráv postavený na i2p, který má dodatečné funkce, jež ještě více ztěžují odhalení informací o přenášených zprávách. Díky tomu jej lze použít k bezpečnému přenosu soukromých zpráv i při vysoké latenci a bez spoléhání na centralizovaný přeposílací uzel pro odesílání zpráv, když je odesílatel offline. To je v kontrastu s téměř všemi ostatními populárními systémy soukromého zasílání zpráv, které buď vyžadují, aby byly obě strany online, nebo se spoléhají na částečně důvěryhodnou službu, jež přenáší zprávy jménem odesílatelů, kteří se odpojili.

nebo, zjednodušeně řečeno: Používá se podobně jako e‑mail, ale netrpí žádnými nedostatky e‑mailu v oblasti soukromí.

**Krok 1: Nainstalujte I2P-Bote**

I2P-Bote je zásuvný modul i2p a jeho instalace je velmi snadná. Původní pokyny jsou k dispozici na [bote eepSite, bote.i2p](http://bote.i2p/install/), ale pokud si je chcete přečíst na clearnetu (běžném internetu), tyto pokyny jsou zde se svolením bote.i2p:

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Krok dva: Získejte base64 adresu svého uzlu I2P-Bote**

Tady se člověk může zaseknout, ale nebojte se. I když je trochu obtížné najít k tomu pokyny, ve skutečnosti je to snadné a máte k dispozici několik nástrojů a možností v závislosti na vaší situaci. Pro ty, kdo chtějí jako dobrovolníci pomáhat provozovat bootstrap uzly, je nejlepší způsob vyčíst potřebné informace ze souboru se soukromým klíčem, který používá bote tunnel.

**Kde jsou klíče?**

I2P-Bote ukládá své klíče destinace do textového souboru, který je v Debianu umístěn v `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. Na systémech mimo Debian, kde je i2p nainstalováno uživatelem, bude klíč v `$HOME/.i2p/i2pbote/local_dest.key`, a ve Windows bude soubor v `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Metoda A: Převeďte klíč v prostém textu na destinaci v base64**

Aby bylo možné převést klíč v prostém textu na destination (cílový identifikátor v I2P) v base64, je třeba vzít klíč a oddělit z něj pouze část destination. Aby bylo možné toto provést správně, je třeba provést následující kroky:

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Existuje řada aplikací a skriptů, které tyto kroky provedou za vás. Zde je několik z nich, ale tento výčet zdaleka není úplný:

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Tyto možnosti jsou také k dispozici v řadě knihoven pro vývoj aplikací pro I2P.

**Zkratka:**


Protože local destination (cílová identita) vašeho uzlu I2P-Bote je DSA destination, je rychlejší jednoduše zkrátit soubor local_dest.key na prvních 516 bajtů. Abyste to provedli snadno, spusťte tento příkaz při běhu I2P-Bote s I2P na Debianu:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Nebo pokud je I2P nainstalované pod vaším uživatelským účtem:

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Metoda B: Proveďte vyhledání**

Pokud se vám to zdá jako příliš práce, můžete zjistit destinaci ve formátu base64 svého připojení Bote tak, že vyhledáte jeho adresu base32 pomocí libovolného z dostupných způsobů pro vyhledávání adres base32. Adresa base32 vašeho uzlu Bote je k dispozici na stránce "Connection" v rámci pluginu Bote na [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Krok tři: Kontaktujte nás!**

**Aktualizujte soubor built-in-peers.txt přidáním svého nového uzlu**

Nyní, když máte správnou destinaci pro svůj uzel I2P-Bote, posledním krokem je přidat se do výchozího seznamu peerů pro [I2P-Bote zde](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) zde. Můžete to udělat tak, že vytvoříte fork repozitáře, přidáte se do seznamu se svým jménem zakomentovaným a svou 516znakovou destinací hned pod ním, takto:

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
a odesláním pull requestu. To je všechno, takže pomozte udržet i2p živé, decentralizované a spolehlivé.
