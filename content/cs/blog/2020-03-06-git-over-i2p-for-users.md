---
title: "Git přes I2P pro uživatele"
date: 2020-03-06
author: "idk"
description: "Git přes I2P"
categories: ["development"]
---

Návod k nastavení přístupu ke gitu přes I2P Tunnel. Tento tunnel bude sloužit jako váš přístupový bod k jediné službě gitu v I2P. Je to součást celkového úsilí o přechod I2P z monotone na Git.

## Než cokoli jiného: Mějte jasno v tom, jaké možnosti služba nabízí veřejnosti

V závislosti na tom, jak je služba Git nakonfigurována, může, ale nemusí nabízet všechny služby na stejné adrese. V případě git.idk.i2p existuje veřejná HTTP adresa URL a SSH adresa URL pro nastavení vašeho SSH klienta pro Git. Obojí lze použít k odesílání (push) i stahování (pull), ale doporučuje se SSH.

## Nejprve: Vytvořte si účet na službě Git

Chcete-li vytvořit své repozitáře na vzdálené službě git, zaregistrujte si u této služby uživatelský účet. Samozřejmě je také možné vytvářet repozitáře lokálně a odeslat je (push) na vzdálenou službu git, ale většina bude vyžadovat účet a také vytvoření prostoru pro repozitář na serveru.

## Za druhé: Vytvořte projekt pro testování

Abyste se ujistili, že proces nastavení funguje, je užitečné vytvořit si pro testování repozitář přímo ze serveru. Přejděte k repozitáři i2p-hackers/i2p.i2p a vytvořte si z něj na svém účtu fork.

## Třetí: Nastavte svůj klientský tunnel pro Git

Abyste měli přístup pro čtení i zápis k serveru, budete muset nastavit tunnel pro svého SSH klienta. Pokud vám stačí klonování přes HTTP/S jen pro čtení, můžete toto celé přeskočit a jednoduše použít proměnnou prostředí `http_proxy` k tomu, abyste nakonfigurovali git tak, aby používal předem nakonfigurovaný I2P HTTP Proxy. Například:

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Pro přístup přes SSH spusťte "New Tunnel Wizard" z http://127.0.0.1:7657/i2ptunnelmgr a nastavte klientský tunnel směřující na SSH adresu služby Git v base32.

## Za čtvrté: Zkuste klonování

Nyní máte svůj tunnel nastavený, můžete se pokusit o klonování přes SSH:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Můžete narazit na chybu, kdy vzdálená strana neočekávaně ukončí spojení. Bohužel git stále nepodporuje klonování s možností navázání. Do té doby existuje několik poměrně snadných způsobů, jak to řešit. První a nejjednodušší je zkusit vytvořit mělký klon:

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Jakmile provedete mělký klon, můžete zbytek dostáhnout s možností pokračování po přerušení tak, že přejdete do adresáře repozitáře a spustíte:

```
git fetch --unshallow
```
V tuto chvíli ještě nemáte všechny své větve. Můžete je získat spuštěním:

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Doporučený pracovní postup pro vývojáře

Správa verzí funguje nejlépe, když ji používáte správně! Důrazně doporučujeme pracovní postup fork-first (nejprve fork), feature-branch (větev pro funkci):

1. **Never make changes to the Master Branch**. Use the master branch to periodically obtain updates to the official source code. All changes should be made in feature branches.

2. Set up a second remote in your local repository using the upstream source code:

```
git remote add upstream git@127.0.0.1:i2p-hackers/i2p.i2p
```
3. Pull in any upstream changes on your current master:

```
git pull upstream master
```
4. Before making any changes to the source code, check out a new feature branch to develop on:

```
git checkout -b feature-branch-name
```
5. When you're done with your changes, commit them and push them to your branch:

```
git commit -am "I added an awesome feature!"
git push origin feature-branch-name
```
6. Submit a merge request. When the merge request is approved, check out the master locally and pull in the changes:

```
git checkout master
git pull upstream master
```