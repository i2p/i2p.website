---
title: "Git via I2P pour les utilisateurs"
date: 2020-03-06
author: "idk"
description: "Git via I2P"
categories: ["development"]
---

Tutoriel pour configurer l’accès à git via un I2P Tunnel. Ce tunnel servira de point d’accès à un service git unique sur I2P. Il fait partie de l’effort global visant à faire passer I2P de monotone à Git.

## Avant tout : sachez quelles fonctionnalités le service propose au public

Selon la façon dont le service git est configuré, il peut proposer ou non tous les services sur la même adresse. Dans le cas de git.idk.i2p, il existe une URL HTTP publique et une URL SSH à configurer pour votre client Git en SSH. Les deux peuvent être utilisés pour pousser ou tirer, mais SSH est recommandé.

## D'abord: Créez un compte sur un service Git

Pour créer vos dépôts sur un service Git distant, inscrivez-vous pour obtenir un compte utilisateur sur ce service. Bien sûr, il est également possible de créer des dépôts en local et de les pousser vers un service Git distant, mais la plupart exigeront un compte et que vous créiez le dépôt sur le serveur.

## Deuxièmement : Créez un projet pour effectuer des tests

Pour s’assurer que le processus de configuration fonctionne, il est utile de créer un dépôt de test à partir du serveur. Accédez au dépôt i2p-hackers/i2p.i2p et créez un fork sur votre compte.

## Troisièmement : configurez votre tunnel client git

Pour disposer d’un accès en lecture-écriture à un serveur, vous devrez configurer un tunnel pour votre client SSH. Si vous n’avez besoin que du clonage HTTP/S en lecture seule, vous pouvez alors ignorer tout cela et simplement utiliser la variable d’environnement http_proxy pour configurer git afin d’utiliser le proxy HTTP I2P préconfiguré. Par exemple :

```
http_proxy=http://localhost:4444 git clone --depth=1 http://git.idk.i2p/youruser/i2p.i2p
git fetch --unshallow
```
Pour l'accès SSH, lancez le "New Tunnel Wizard" depuis http://127.0.0.1:7657/i2ptunnelmgr et configurez un tunnel client pointant vers l'adresse base32 SSH du service Git.

## Quatrième : tentez un clonage

Maintenant que votre tunnel est configuré, vous pouvez tenter un clonage via SSH :

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone git@127.0.0.1:youruser/i2p.i2p
```
Il est possible que vous obteniez une erreur indiquant que l’extrémité distante a fermé la connexion de façon inattendue. Malheureusement, Git ne prend toujours pas en charge la reprise d’un clonage interrompu. En attendant, il existe deux façons assez simples de gérer cela. La première, et la plus simple, consiste à essayer de cloner avec une profondeur limitée :

```
GIT_SSH_COMMAND="ssh -p 7670" \
    git clone --depth 1 git@127.0.0.1:youruser/i2p.i2p
```
Une fois que vous avez effectué un clonage superficiel, vous pouvez récupérer le reste avec reprise possible en vous plaçant dans le répertoire du dépôt et en exécutant :

```
git fetch --unshallow
```
À ce stade, vous n’avez pas encore toutes vos branches. Vous pouvez les obtenir en exécutant :

```
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
## Flux de travail proposé pour les développeurs

Le contrôle de version donne les meilleurs résultats si vous l’utilisez correctement ! Nous recommandons vivement un flux de travail fork-first (fork d’abord) et feature-branch (branche de fonctionnalité) :

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