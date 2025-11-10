---
title: "Bitcoin Core ajoute la prise en charge d'I2P !"
date: 2021-09-18
author: "idk"
description: "Un nouveau cas d'utilisation et un signe d'adoption croissante"
categories: ["general"]
API_Translate: vrai
---

Un événement préparé depuis des mois, Bitcoin Core a ajouté la prise en charge officielle d’I2P ! Les nœuds Bitcoin sur I2P peuvent interagir pleinement avec le reste des nœuds Bitcoin, grâce à des nœuds qui opèrent à la fois sur I2P et sur le clearnet, ce qui en fait des acteurs de premier plan du réseau Bitcoin. Il est enthousiasmant de voir de grandes communautés comme Bitcoin prendre conscience des avantages qu’I2P peut leur apporter, en offrant confidentialité et accessibilité aux personnes du monde entier.

## Comment cela fonctionne

La prise en charge d'I2P est automatique, via l'API SAM. C'est également une excellente nouvelle, car cela met en lumière certains des domaines dans lesquels I2P excelle tout particulièrement, comme permettre aux développeurs d'applications de créer des connexions I2P par programmation et de manière pratique. Les utilisateurs de Bitcoin via I2P peuvent utiliser I2P sans configuration manuelle en activant l'API SAM et en exécutant Bitcoin avec I2P activé.

## Configuration de votre router I2P

Pour configurer un I2P Router afin de fournir une connectivité anonyme à bitcoin, il est nécessaire d’activer la SAM API. Dans Java I2P, allez sur http://127.0.0.1:7657/configclients et démarrez la SAM Application Bridge avec le bouton "Start". Vous pouvez également activer la SAM Application Bridge par défaut en cochant la case "Run at Startup" puis en cliquant sur "Save Client Configuration".

Sur i2pd, l'API SAM est normalement activée par défaut, mais si ce n'est pas le cas, vous devriez configurer :

```
sam.enabled=true
```
dans votre fichier i2pd.conf.

## Configuration de votre nœud Bitcoin pour l’anonymat et la connectivité

Lancer Bitcoin lui-même en mode anonyme nécessite encore de modifier certains fichiers de configuration dans le répertoire de données de Bitcoin, à savoir %APPDATA%\Bitcoin sous Windows, ~/.bitcoin sous Linux, et ~/Library/Application Support/Bitcoin/ sous Mac OSX. Il faut également disposer d’au moins la version 22.0.0 afin que la prise en charge d’I2P soit disponible.

Après avoir suivi ces instructions, vous devriez disposer d’un nœud Bitcoin privé qui utilise I2P pour les connexions I2P, et Tor pour les connexions .onion et clearnet, afin que toutes vos connexions soient anonymes. Pour plus de commodité, les utilisateurs de Windows devraient ouvrir leur dossier de données Bitcoin en ouvrant le menu Démarrer et en recherchant "Run." Dans la boîte de dialogue Run, tapez "%APPDATA%\Bitcoin" et appuyez sur Entrée.

Dans ce répertoire, créez un fichier nommé "i2p.conf." Sous Windows, assurez-vous d’ajouter des guillemets autour du nom du fichier au moment de l’enregistrer, afin d’empêcher Windows d’ajouter une extension de fichier par défaut. Le fichier doit contenir les options de configuration Bitcoin liées à I2P suivantes :

```
i2psam=127.0.0.1:7656
i2pacceptincoming=true
onlynet=i2p
```
Ensuite, vous devriez créer un autre fichier appelé "tor.conf." Le fichier devrait contenir les options de configuration suivantes liées à Tor :

```
proxy=127.0.0.1:9050
onion=127.0.0.1:9050
onlynet=tor
```
Enfin, vous devrez "inclure" ces options de configuration dans votre fichier de configuration Bitcoin, appelé "bitcoin.conf" dans le répertoire de données. Ajoutez ces deux lignes à votre fichier bitcoin.conf :

```
includeconf=i2p.conf
includeconf=tor.conf
```
Maintenant, votre nœud Bitcoin est configuré pour n'utiliser que des connexions anonymes. Pour activer des connexions directes avec des nœuds distants, supprimez les lignes commençant par:

```
onlynet=
```
Vous pouvez le faire si vous n'avez pas besoin que votre nœud Bitcoin soit anonyme, et cela aide les utilisateurs anonymes à se connecter au reste du réseau Bitcoin.
