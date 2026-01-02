---
title: "Nouveau Modèle de Proposition de Chiffrement"
number: "142"
author: "zzz"
created: "2018-01-11"
lastupdated: "2018-01-20"
status: "Meta"
thread: "http://zzz.i2p/topics/2499"
toc: true
---

## Vue d'ensemble

Ce document décrit des questions importantes à considérer lors de la proposition
d'un remplacement ou d'un ajout à notre chiffrement asymétrique ElGamal.

Ceci est un document informatif.


## Motivation

ElGamal est ancien et lent, et il existe de meilleures alternatives.
Cependant, plusieurs problèmes doivent être résolus avant que nous puissions ajouter ou remplacer par un nouvel algorithme.
Ce document met en évidence ces problèmes non résolus.


## Recherche de Fond

Toute personne proposant une nouvelle cryptographie doit d'abord être familière avec les documents suivants :

- [Proposition 111 NTCP2](/fr/proposals/111-ntcp-2/)
- [Proposition 123 LS2](/fr/proposals/123-new-netdb-entries/)
- [Proposition 136 types de signature expérimentale](/fr/proposals/136-experimental-sigtypes/)
- [Proposition 137 types de signature optionnelle](/fr/proposals/137-optional-sigtypes/)
- Fils de discussion ici pour chacune des propositions ci-dessus, liés à l'intérieur
- [priorités des propositions 2018](http://zzz.i2p/topics/2494)
- [proposition ECIES](http://zzz.i2p/topics/2418)
- [aperçu de la nouvelle cryptographie asymétrique](http://zzz.i2p/topics/1768)
- [Vue d'ensemble de la cryptographie bas niveau](/fr/docs/specs/common-structures/)


## Utilisations de la Cryptographie Asymétrique

En révision, nous utilisons ElGamal pour :

1) Messages de Construction de Tunnel (la clé est dans RouterIdentity)

2) Chiffrement routeur-à-routeur des netdb et autres messages I2NP (la clé est dans RouterIdentity)

3) Fin-à-fin client ElGamal+AES/SessionTag (la clé est dans LeaseSet, la clé Destination n'est pas utilisée)

4) Ephemeral DH pour NTCP et SSU


## Conception

Toute proposition visant à remplacer ElGamal par autre chose doit fournir les détails suivants.


## Spécification

Toute proposition de nouvelle cryptographie asymétrique doit spécifier complètement les éléments suivants.


### 1. Général

Répondez aux questions suivantes dans votre proposition. Notez qu'il pourrait être nécessaire que cela soit une proposition distincte des détails dans la section 2) ci-dessous, car cela pourrait entrer en conflit avec les propositions existantes 111, 123, 136, 137, ou autres.

- Pour lesquels des cas ci-dessus 1-4 proposez-vous d'utiliser la nouvelle cryptographie ?
- Si pour 1) ou 2) (routeur), où va la clé publique, dans le RouterIdentity ou dans les propriétés de RouterInfo ? Avez-vous l'intention d'utiliser le type de cryptographie dans le certificat de clé ? Spécifiez complètement. Justifiez votre décision dans tous les cas.
- Si pour 3) (client), avez-vous l'intention de stocker la clé publique dans la destination et d'utiliser le type de cryptographie dans le certificat de clé (comme dans la proposition ECIES), ou de la stocker dans LS2 (comme dans la proposition 123), ou autre chose ? Spécifiez complètement, et justifiez votre décision.
- Pour toutes les utilisations, comment le support sera-t-il annoncé ? Si pour 3), cela va-t-il dans le LS2, ou ailleurs ? Si pour 1) et 2), est-ce similaire aux propositions 136 et/ou 137 ? Spécifiez complètement, et justifiez vos décisions. Il faudra probablement une proposition séparée pour cela.
- Spécifiez complètement comment et pourquoi cela est rétrocompatible, et spécifiez un plan de migration complet.
- Quelles propositions non mises en œuvre sont des prérequis pour votre proposition ?


### 2. Type de cryptographie spécifique

Répondez aux questions suivantes dans votre proposition :

- Informations générales sur la cryptographie, courbes/paramètres spécifiques, justifiez complètement votre choix. Fournissez des liens vers les spécifications et autres informations.
- Résultats des tests de vitesse par rapport à ElG et autres alternatives si applicable. Incluez le chiffrement, le déchiffrement, et la génération de clé.
- Disponibilité de la bibliothèque en C++ et Java (OpenJDK, BouncyCastle, et tierces parties)
  Pour les parties tierces ou non-Java, fournissez des liens et licences
- Numéro(s) de type de cryptographie proposé(s) (gamme expérimentale ou non)


## Notes


