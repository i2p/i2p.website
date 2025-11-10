---
title: "Notes d'état I2P du 2004-08-03"
date: 2004-08-03
author: "jr"
description: "Mise à jour d'état hebdomadaire d'I2P couvrant les performances de la version 0.3.4, le développement d'une nouvelle console web et divers projets d'applications"
categories: ["status"]
---

Salut à tous, expédions cette mise à jour de statut.

## Index :

1. 0.3.4 status
2. On deck for 0.3.4.1
3. New web console / I2PTunnel controller
4. 0.4 stuff
5. Other development activities
6. ???

## 1) statut de 0.3.4

Avec la version 0.3.4 de la semaine dernière, le nouveau réseau fonctionne plutôt bien - les connexions irc durent plusieurs heures d'affilée et la récupération d'eepsite(Site I2P) semble assez fiable. Le débit reste généralement faible, bien qu’en légère amélioration (je voyais auparavant un débit constant de 4-5KBps, maintenant je vois régulièrement 5-8KBps). oOo a publié une paire de scripts résumant l’activité irc, y compris le temps aller-retour des messages et la durée de vie de la connexion (basés sur le bogobot de hypercubus, récemment intégré dans CVS)

## 2) Prévu pour 0.3.4.1

Comme tous ceux qui sont en 0.3.4 l'ont remarqué, j’ai été *cough* un peu verbeux dans ma journalisation, ce qui a été corrigé dans cvs. De plus, après avoir écrit quelques outils pour mettre la bibliothèque ministreaming sous pression, j’ai ajouté un 'choke' (mécanisme de limitation) afin qu’elle n’engloutisse pas des tonnes de mémoire (ce mécanisme bloquera lorsqu’on essaiera d’ajouter plus de 128KB de données dans le tampon d’un flux, de sorte qu’au moment d’envoyer un gros fichier, votre router n’ait pas tout ce fichier chargé en mémoire). Je pense que cela aidera avec les problèmes OutOfMemory que les gens ont constatés, mais je vais ajouter du code de surveillance / débogage supplémentaire pour le vérifier.

## 3) Nouvelle console web / contrôleur I2PTunnel

En plus des modifications ci‑dessus pour la 0.3.4.1, nous avons une première itération de la nouvelle console du router prête à être testée. Pour plusieurs raisons, nous n’allons pas l’inclure dans l’installation par défaut pour l’instant, il y aura donc des instructions pour la faire fonctionner lorsque la révision 0.3.4.1 sortira dans quelques jours. Comme vous l’avez vu, je suis vraiment mauvais en conception Web, et comme beaucoup d’entre vous l’ont dit, je devrais arrêter de bricoler la couche applicative et rendre le cœur et le router parfaitement stables et fiables. Donc, bien que la nouvelle console intègre une grande partie des fonctionnalités souhaitées (configurer le router entièrement via quelques pages Web simples, offrir un résumé rapide et lisible de l’état de santé du router, permettre de créer / modifier / arrêter / démarrer différentes instances I2PTunnel), j’ai vraiment besoin d’aide de la part de personnes compétentes sur le côté Web.

Les technologies utilisées dans la nouvelle console web sont des JSP et CSS standard, ainsi que de simples beans Java qui interrogent le router / I2PTunnels pour obtenir des données et traiter les requêtes. Elles sont toutes regroupées dans deux fichiers .war et déployées dans un serveur web Jetty intégré (qui doit être démarré via les lignes clientApp.* du router). Les JSP et beans de la console principale du router sont plutôt solides sur le plan technique, même si les nouveaux JSP et beans que j’ai créés pour gérer les instances I2PTunnel sont un peu bancals.

## 4) Éléments de la 0.4

Au-delà de la nouvelle interface web, la version 0.4 inclura le nouveau programme d'installation d'hypercubus que nous n'avons pas encore vraiment intégré. Nous devons également effectuer d'autres simulations à grande échelle (en particulier la gestion d'applications asymétriques comme IRC et outproxies (mandataires sortants)). En outre, il y a quelques mises à jour que je dois faire intégrer dans kaffe/classpath afin que nous puissions faire fonctionner la nouvelle infrastructure web sur des JVM open source. De plus, je dois préparer quelques autres documents (l'un sur le passage à l'échelle et un autre analysant la sécurité/l'anonymat dans quelques scénarios courants). Nous voulons également que toutes les améliorations que vous proposerez soient intégrées dans la nouvelle console web.

Ah, et corrigez tous les bogues que vous contribuez à trouver :)

## 5) Autres activités de développement

Bien qu'il y ait eu beaucoup de progrès réalisés sur le système I2P de base, ce n'est que la moitié de l'histoire - beaucoup d'entre vous font un excellent travail sur des applications et des bibliothèques pour rendre I2P utile. J'ai vu quelques questions dans le scrollback (historique de discussion) concernant qui travaille sur quoi, donc pour aider à diffuser ces informations, voici tout ce que je sais (si vous travaillez sur quelque chose qui n'est pas listé et que vous souhaitez le partager, si je me trompe, ou si vous voulez discuter de vos avancées, n'hésitez pas à vous manifester !)

### Active development:

- python SAM/I2P lib (devs: sunshine, aum)
- C SAM lib (devs: nightblade)
- python kademlia/I2P DHT (devs: aum)
- v2v - Voice over I2P (devs: aum)
- outproxy load balancing (devs: mule)

### Development I've heard about but don't know the status of:

- swarming file transfer / BT (devs: nickster)

### Paused development:

- Enclave DHT (devs: nightblade)
- perl SAM lib (devs: BrianR)
- I2PSnark / BT (devs: eco)
- i2pIM (devs: thecrypto)
- httptunnel (devs: mihi)
- MyI2P address book (devs: jrandom)
- MyI2P blogging (devs: jrandom)

## 6) ???

C’est tout ce qui me vient à l’esprit pour l’instant - passez à la réunion plus tard ce soir pour discuter de tout ça. Comme d’habitude, à 21 h GMT sur #i2p, sur les serveurs habituels.

=jr
