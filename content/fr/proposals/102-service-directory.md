---
title: "Répertoire de Services"
number: "102"
author: "zzz"
created: "2009-01-01"
lastupdated: "2009-01-06"
status: "Rejeté"
thread: "http://zzz.i2p/topics/180"
supercededby: "122"
---

## Vue d'ensemble

Cette proposition concerne un protocole que les applications pourraient utiliser pour enregistrer et rechercher des services dans un répertoire.

## Motivation

La manière la plus simple de prendre en charge onioncat est avec un répertoire de services.

Ceci est similaire à une proposition que Sponge avait faite il y a quelque temps sur IRC. Je ne pense pas qu'il l'ait rédigée, mais son idée était de l'inclure dans le netDb. Je ne suis pas en faveur de cela, mais la discussion sur la meilleure méthode d'accès au répertoire (recherches dans le netDb, DNS-over-i2p, HTTP, hosts.txt, etc.) je la laisserai pour un autre jour.

Je pourrais probablement bricoler ça assez rapidement en utilisant HTTP et la collection de scripts perl que j'utilise pour le formulaire d'ajout de clé.

## Spécification

Voici comment une application interfacerait avec le répertoire :

REGISTRER
  - DestKey
  - Liste de paires Protocole/Service :

    - Protocole (optionnel, par défaut : HTTP)
    - Service (optionnel, par défaut : site web)
    - ID (optionnel, par défaut : aucun)

  - Nom d'hôte (optionnel)
  - Expiration (par défaut : 1 jour ? 0 pour supprimer)
  - Sig (utilisant la clé privée pour dest)

  Renvoie : succès ou échec

  Mises à jour autorisées

RECHERCHE
  - Hash ou clé (optionnel). UN de :

    - Hash partiel de 80 bits
    - Hash complet de 256 bits
    - Clé de destination complète

  - Pair protocole/service (optionnel)

  Renvoie : succès, échec, ou (pour 80 bits) collision.
  Si succès, renvoie le descripteur signé ci-dessus.
