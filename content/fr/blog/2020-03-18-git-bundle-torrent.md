---
title: "Utiliser un bundle Git pour récupérer le code source d'I2P"
date: 2020-03-18
author: "idk"
description: "Téléchargez le code source d’I2P via BitTorrent"
categories: ["development"]
---

Cloner de grands dépôts logiciels via I2P peut être difficile, et l'utilisation de git peut parfois compliquer encore les choses. Heureusement, git peut aussi parfois les simplifier. Git possède une commande `git bundle` qui peut être utilisée pour transformer un dépôt git en un fichier à partir duquel git peut ensuite cloner, fetch ou importer depuis un emplacement sur votre disque local. En combinant cette capacité avec des téléchargements BitTorrent, nous pouvons résoudre nos problèmes restants avec `git clone`.

## Avant de commencer


Si vous avez l'intention de générer un bundle git, vous **devez** déjà disposer d'une copie complète du dépôt **git**, et non du dépôt mtn. Vous pouvez l'obtenir depuis github ou depuis git.idk.i2p, mais un clone superficiel (un clone effectué avec --depth=1) *ne fonctionnera pas*. Il échouera silencieusement, en créant quelque chose qui ressemble à un bundle, mais lorsque vous tenterez de le cloner, la tentative de clonage échouera. Si vous ne faites que récupérer un bundle git pré-généré, alors cette section ne s'applique pas à vous.

## Récupération du code source d'I2P via BitTorrent

Quelqu’un devra vous fournir un fichier torrent ou un lien magnet correspondant à un `git bundle` existant qu’une personne a déjà généré pour vous. Une fois que vous avez un bundle provenant de BitTorrent, vous devrez utiliser git pour créer à partir de celui-ci un dépôt opérationnel.

## Utilisation de `git clone`

Cloner à partir d'un bundle Git est facile, il suffit de:

```
git clone $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
Si vous obtenez l’erreur suivante, essayez plutôt d’exécuter git init et git fetch manuellement :

```
fatal: multiple updates for ref 'refs/remotes/origin/master' not allowed
```
## Utilisation de `git init` et `git fetch`

Tout d'abord, créez un répertoire i2p.i2p pour en faire un dépôt Git :

```
mkdir i2p.i2p && cd i2p.i2p
```
Ensuite, initialisez un dépôt git vide pour y récupérer les modifications:

```
git init
```
Enfin, récupérez le dépôt à partir du bundle :

```
git fetch $HOME/.i2p/i2psnark/i2p.i2p.bundle
```
## Remplacez le dépôt distant bundle par le dépôt distant upstream

Maintenant que vous avez un bundle, vous pouvez suivre les modifications en configurant le dépôt distant pour pointer vers le dépôt amont :

```
git remote set-url origin git@127.0.0.1:i2p-hackers/i2p.i2p
```
## Génération d’un bundle

Pour commencer, suivez le guide Git pour les utilisateurs jusqu’à obtenir un clone `--unshallow`é avec succès du dépôt i2p.i2p. Si vous avez déjà un clone, assurez-vous d’exécuter `git fetch --unshallow` avant de générer un bundle torrent.

Une fois que c'est fait, exécutez simplement la cible Ant correspondante:

```
ant bundle
```
et copiez le bundle (archive) obtenu dans votre répertoire de téléchargements d'I2PSnark. Par exemple :

```
cp i2p.i2p.bundle* $HOME/.i2p/i2psnark/
```
Dans une minute ou deux, I2PSnark détectera le torrent. Cliquez sur le bouton "Start" pour commencer à mettre le torrent en partage.
