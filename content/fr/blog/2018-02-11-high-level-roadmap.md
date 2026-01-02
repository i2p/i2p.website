---
title: "Feuille de route de haut niveau pour 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 sera l’année de nouveaux protocoles, de nouvelles collaborations et d’une focalisation plus précise."
categories: ["roadmap"]
---

Parmi les nombreux sujets que nous avons abordés à 34C3 figurait la question de savoir sur quoi nous devrions nous concentrer pour l’année à venir. Plus précisément, nous voulions une feuille de route claire, distinguant ce que nous voulons absolument réaliser de ce qu’il serait très appréciable d’avoir, et qui permette d’aider à intégrer les nouveaux arrivants dans l’une ou l’autre catégorie. Voici ce que nous avons convenu :

## Priorité : Nouvelle crypto(graphie !)

De nombreuses primitives et protocoles actuels conservent encore leurs conceptions d’origine datant d’environ 2005 et doivent être améliorés. Nous avons, depuis plusieurs années, un certain nombre de propositions ouvertes présentant des idées, mais les progrès ont été lents. Nous sommes tous tombés d’accord pour en faire notre priorité absolue pour 2018. Les composants fondamentaux sont :

- New transport protocols (to replace NTCP and SSU). See Prop111.
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See Prop123.
- Upgraded end-to-end protocol (replacing ElGamal).

Le travail sur cette priorité se répartit en plusieurs domaines :

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Nous ne pouvons pas déployer de nouvelles spécifications de protocole sur l’ensemble du réseau sans avoir travaillé sur tous ces aspects.

## Souhaitable: Réutilisation du code

L’un des avantages à entreprendre le travail ci-dessus dès maintenant, c’est que, au cours des dernières années, des efforts indépendants ont visé à créer des protocoles simples et des cadres de protocoles qui atteignent bon nombre des objectifs que nous poursuivons pour nos propres protocoles, et qui ont gagné en adoption auprès de la communauté au sens large. En tirant parti de ces travaux, nous bénéficions d’un effet "multiplicateur":

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Mes propositions, en particulier, s'appuieront sur le [Noise Protocol Framework](https://noiseprotocol.org/), et sur le [format de paquets SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). J'ai des collaborations prévues avec plusieurs personnes en dehors d'I2P pour celles-ci !

## Priorité : collaboration sur le Clearnet

À ce sujet, nous suscitons progressivement de l’intérêt depuis environ six mois. Lors de PETS2017, 34C3 et RWC2018, j’ai eu de très bonnes discussions sur les moyens d’améliorer la collaboration avec la communauté au sens large. C’est vraiment important pour que nous puissions recueillir autant de relectures que possible sur les nouveaux protocoles. Le principal obstacle que j’ai constaté est que la majorité de la collaboration autour du développement d’I2P se déroule actuellement au sein d’I2P lui-même, ce qui accroît de manière significative l’effort nécessaire pour contribuer.

Les deux priorités dans ce domaine sont :

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Autres objectifs classés comme souhaitables:

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Je m’attends à ce que les collaborations avec des personnes en dehors d’I2P se fassent entièrement sur GitHub, afin de minimiser les frictions.

## Priorité : Préparation aux versions à longue durée de vie

I2P est désormais dans Debian Sid (leur dépôt instable), qui se stabilisera d'ici environ un an et demi, et a également été intégré au dépôt Ubuntu en vue de son inclusion dans la prochaine version LTS en avril. Nous allons commencer à avoir des versions d'I2P qui resteront en circulation pendant des années, et nous devons nous assurer que nous pouvons gérer leur présence sur le réseau.

L’objectif principal ici est de déployer autant de nouveaux protocoles que possible au cours de l’année à venir, afin de coïncider avec la prochaine version stable de Debian. Pour ceux qui nécessitent des déploiements pluriannuels, nous devrions intégrer les modifications de compatibilité ascendante le plus tôt possible.

## Priorité : conversion des applications actuelles en plugins

Le modèle Debian encourage l’utilisation de paquets distincts pour des composants distincts. Nous avons convenu que dissocier les applications Java actuellement regroupées du router Java principal serait bénéfique pour plusieurs raisons:

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Combiné aux priorités précédentes, cela oriente davantage le projet I2P principal dans la direction de, par exemple, le noyau Linux. Nous consacrerons davantage de temps au réseau lui-même, en laissant les développeurs tiers se concentrer sur des applications qui utilisent le réseau (ce qui est nettement plus facile à faire après notre travail de ces dernières années sur les API et les bibliothèques).

## Souhaitable: Améliorations de l'application

Il y a un certain nombre d’améliorations au niveau applicatif sur lesquelles nous souhaitons travailler, mais nous n’avons actuellement pas le temps de développement pour le faire, compte tenu de nos autres priorités. C’est un domaine dans lequel nous serions ravis de voir de nouveaux contributeurs ! Une fois le découplage ci-dessus terminé, il sera nettement plus facile pour quelqu’un de travailler sur une application spécifique indépendamment du router Java principal.

L’une des applications pour lesquelles nous aimerions recevoir de l’aide est I2P Android. Nous la maintiendrons à jour avec les versions du cœur d’I2P et corrigerons les bogues autant que possible, mais il reste beaucoup à faire pour améliorer le code sous-jacent ainsi que la facilité d’utilisation.

## Priorité : stabilisation de Susimail et d'I2P-Bote

Cela dit, nous voulons travailler spécifiquement sur des correctifs pour Susimail et I2P-Bote à court terme (dont certaines ont été intégrées dans la 0.9.33). Elles ont bénéficié de moins de travail ces dernières années que d’autres applications I2P, et nous voulons donc consacrer du temps à remettre leurs bases de code à niveau et à les rendre plus faciles d’accès pour que de nouveaux contributeurs puissent s’y plonger !

## Souhaitable : triage des tickets

Nous avons un important arriéré de tickets dans un certain nombre de sous-systèmes et d'applications I2P. Dans le cadre de l'effort de stabilisation mentionné ci-dessus, nous aimerions faire le ménage dans certains de nos problèmes de longue date. Plus important encore, nous voulons nous assurer que nos tickets sont correctement organisés, afin que les nouveaux contributeurs puissent trouver de bons tickets sur lesquels travailler.

## Priorité : Support utilisateur

Un aspect de ce qui précède sur lequel nous allons nous concentrer est de rester en contact avec les utilisateurs qui prennent le temps de signaler des problèmes. Merci ! Plus nous parvenons à raccourcir la boucle de rétroaction, plus nous pouvons résoudre rapidement les problèmes auxquels sont confrontés les nouveaux utilisateurs, et plus il est probable qu’ils continuent à participer à la communauté.

## Nous serions ravis de votre aide !

Tout cela semble très ambitieux, et ça l’est ! Mais beaucoup des éléments ci-dessus se recoupent et, avec une planification soigneuse, nous pouvons les entamer sérieusement.

Si vous souhaitez contribuer à l’un des objectifs ci‑dessus, venez discuter avec nous ! Vous pouvez nous trouver sur OFTC et Freenode (#i2p-dev), ainsi que sur Twitter (@GetI2P).
