---
title: "Použití git bundle k získání zdrojového kódu I2P"
date: 2020-03-18
author: "idk"
description: "Stáhněte si zdrojový kód I2P přes BitTorrent"
categories: ["development"]
---

Klonování velkých softwarových repozitářů přes I2P může být obtížné a používání Gitu to může někdy ještě ztížit. Naštěstí to může Git někdy i usnadnit. Git má příkaz `git bundle`, který lze použít k převodu repozitáře Git na soubor; z umístění na vašem místním disku pak z něj může Git klonovat, načítat nebo importovat. Spojením této možnosti se stahováním přes BitTorrent můžeme vyřešit zbývající problémy s `git clone`.

## Než začnete

Pokud máte v úmyslu vytvořit git bundle, **musíte** již mít úplnou kopii repozitáře **git**, nikoli repozitáře mtn. Můžete jej získat z githubu nebo z git.idk.i2p, ale mělký klon (klon provedený s --depth=1) *nebude fungovat*. Selže tiše, vytvoří něco, co vypadá jako bundle, ale když se jej pokusíte klonovat, selže. Pokud pouze získáváte předem vytvořený git bundle, pak se na vás tato část nevztahuje.

## Stažení zdrojových kódů I2P přes BitTorrent

Někdo vám bude muset poskytnout soubor .torrent nebo magnet odkaz odpovídající existujícímu `git bundle` (balíček), který pro vás již byl vytvořen. Jakmile budete mít bundle z BitTorrentu, budete muset použít git k vytvoření pracovního repozitáře z něj.

## Použití `git clone`

Klonování z git bundle je snadné, stačí:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
If you get the following error, try using git init and git fetch manually instead:

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Použití `git init` a `git fetch`

Nejprve vytvořte adresář i2p.i2p, který převedete na repozitář Git:

```
mkdir i2p.i2p && cd i2p.i2p
```
Dále inicializujte prázdný repozitář Git, do kterého budete načítat změny:

```
git init
```
Nakonec načtěte repozitář z balíčku:

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Nahraďte vzdálený repozitář bundle vzdáleným repozitářem upstream.

Nyní, když máte balíček, můžete držet krok se změnami tak, že nastavíte vzdálený repozitář na upstream (původní) zdroj repozitáře:

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Vytvoření balíčku

Nejprve postupujte podle průvodce Git pro uživatele, dokud nebudete mít klon repozitáře i2p.i2p úspěšně rozšířený pomocí `--unshallow`. Pokud už klon máte, ujistěte se, že před vytvořením torrentového balíčku spustíte `git fetch --unshallow`.

Jakmile to budete mít, jednoduše spusťte odpovídající cíl Antu:

```
ant bundle
```
a zkopírujte výsledný balíček do vašeho adresáře pro stahování I2PSnarku. Například:

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
Za minutu nebo dvě I2PSnark torrent zaregistruje. Klikněte na tlačítko "Start" a zahajte seedování torrentu.
