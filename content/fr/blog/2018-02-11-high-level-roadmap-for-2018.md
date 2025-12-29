---
title: "Feuille de route de haut niveau pour 2018"
date: 2018-02-11
slug: "high-level-roadmap-for-2018"
author: "str4d"
description: "2018 sera l'année de nouveaux protocoles, de nouvelles collaborations et d'une orientation plus précise"
categories: ["roadmap"]
---

L’une des nombreuses choses que nous avons abordées au 34C3 était de déterminer sur quoi nous devrions nous concentrer pour l’année à venir. Nous voulions notamment une feuille de route qui clarifie ce que nous voulons absolument réaliser, par opposition à ce qu’il serait vraiment appréciable d’avoir, et qui nous permette d’aider à intégrer les nouveaux venus dans l’une ou l’autre catégorie. Voici ce que nous avons élaboré :

## Priorité : Nouvelle crypto(graphie !)

De nombreux primitifs et protocoles actuels conservent encore leur conception d’origine datant d’environ 2005 et nécessitent des améliorations. Nous avons depuis plusieurs années un certain nombre de propositions ouvertes présentant des idées, mais les progrès concrets ont été lents. Nous sommes tous convenus que cela doit être notre priorité absolue pour 2018. Les composants essentiels sont :

- New transport protocols (to replace NTCP and SSU). See [Prop111](https://geti2p.net/spec/proposals/111).
- New onion-encryption protocol for building and using tunnels.
- New NetDB datatypes to enable enhanced Destinations. See [Prop123](https://geti2p.net/spec/proposals/123).
- Upgraded end-to-end protocol (replacing ElGamal).

Le travail sur cette priorité se répartit en plusieurs domaines :

- Writing proposals.
- Writing working implementations of them that we can test.
- Reviewing proposals.

Nous ne pouvons pas déployer de nouvelles spécifications de protocole sur l’ensemble du réseau sans un travail sur tous ces domaines.

## Souhaitable : réutilisation du code

L’un des avantages de démarrer le travail ci-dessus dès maintenant, c’est que, ces dernières années, des efforts indépendants ont été menés pour créer des protocoles simples et des cadres de protocoles qui atteignent bon nombre des objectifs que nous avons pour nos propres protocoles, et ont gagné du terrain au sein de la communauté plus large. En tirant parti de ce travail, nous obtenons un effet « multiplicateur » :

- We benefit from protocol designs, security proofs, and code written by others, reducing the amount of work we need to do for the same level of feature-completeness and security assurances.

- Work we do can be leveraged by other communities, increasing their interest in collaborating with us, and thinking about I2P as a whole.

Mes propositions, en particulier, s’appuieront sur le [Noise Protocol Framework](https://noiseprotocol.org/), ainsi que sur le [format de paquet SPHINX](https://katzenpost.mixnetworks.org/docs/specs/sphinx.html). J’ai déjà des collaborations prévues avec plusieurs personnes en dehors d’I2P pour celles-ci !

## Priorité : collaboration sur le Clearnet

À ce sujet, nous avons progressivement suscité de l'intérêt au cours des six derniers mois environ. À l'occasion de PETS2017, 34C3 et RWC2018, j'ai eu de très bonnes discussions sur les moyens d'améliorer la collaboration avec la communauté au sens large. C'est vraiment important afin de garantir que nous puissions obtenir autant de revues que possible des nouveaux protocoles. Le principal obstacle que j'ai constaté est que la majeure partie de la collaboration au développement d'I2P se déroule actuellement au sein d'I2P elle-même, ce qui augmente considérablement l'effort nécessaire pour contribuer.

Les deux priorités dans ce domaine sont :

- Set up a project-run development forum that is accessible both inside and outside I2P.

- Set up mailing lists for review and discussion of proposals (possibly connected to the above forum).

Autres objectifs classés comme souhaitables :

- Set up a usable git-to-mtn pathway, to enable us to effectively solicit clearnet contributions on GitHub while keeping the canonical dev environment on Monotone.

- Write a "position paper" that accurately explains I2P to academic audiences, and puts it in context with existing literature.

Je m’attends à ce que les collaborations avec des personnes en dehors d’I2P se fassent entièrement sur GitHub, afin de réduire au minimum les frictions.

## Priorité : Préparation en vue de versions à longue durée de vie

I2P est désormais dans Debian Sid (leur dépôt instable), qui se stabilisera d’ici environ un an et demi, et a également été intégré au dépôt Ubuntu en vue de son inclusion dans la prochaine version LTS en avril. Nous allons commencer à avoir des versions d’I2P qui resteront en circulation pendant des années, et nous devons nous assurer que nous pouvons gérer leur présence sur le réseau.

L’objectif principal ici est de déployer, au cours de l’année à venir, autant de nouveaux protocoles qu’il nous sera raisonnablement possible, afin d’être à temps pour la prochaine version stable de Debian. Pour ceux qui nécessitent des déploiements pluriannuels, nous devrions intégrer les changements de compatibilité avec les versions futures le plus tôt possible.

## Priorité : conversion des applications actuelles en plugins

Le modèle Debian encourage l’utilisation de paquets distincts pour chaque composant. Nous avons convenu que le découplage des applications Java actuellement fournies avec le router Java principal serait bénéfique pour plusieurs raisons :

- It codifies the boundary between the applications and the router.

- It should make it easier to get these apps running with non-Java routers.

- It would enable third parties to create "I2P bundles" containing just the applications they want.

Combiné aux priorités précédentes, cela oriente le projet I2P principal davantage dans la direction, par exemple, du noyau Linux. Nous consacrerons plus de temps au réseau lui-même, en laissant aux développeurs tiers le soin de se concentrer sur les applications qui utilisent le réseau (ce qui est nettement plus facile à faire après notre travail de ces dernières années sur les API et les bibliothèques).

## Souhaitable : améliorations de l'application

Nous avons toute une série d’améliorations au niveau applicatif sur lesquelles nous souhaitons travailler, mais nous n’avons actuellement pas le temps de développement nécessaire pour le faire, étant donné nos autres priorités. C’est un domaine où nous aimerions beaucoup voir de nouveaux contributeurs ! Une fois le découplage ci-dessus terminé, il sera nettement plus facile pour quelqu’un de travailler sur une application spécifique indépendamment du router Java principal.

L’une des applications pour lesquelles nous aimerions recevoir de l’aide est I2P Android. Nous la maintiendrons à jour au rythme des versions principales d’I2P, et nous corrigerons les bogues autant que possible, mais il reste beaucoup à faire pour améliorer à la fois le code sous-jacent et l’ergonomie.

## Priorité : stabilisation de Susimail et d'I2P-Bote

Cela dit, nous souhaitons effectivement travailler spécifiquement sur des correctifs pour Susimail et I2P-Bote à court terme (dont certains ont été intégrés dans la version 0.9.33). Elles ont reçu moins d’attention ces dernières années que d’autres applications I2P, et nous voulons donc consacrer du temps à remettre leurs bases de code à niveau et à les rendre plus faciles à prendre en main pour les nouveaux contributeurs !

## Souhaitable : Tri des tickets

Nous avons un important arriéré de tickets dans un certain nombre de sous-systèmes et d'applications I2P. Dans le cadre de l'effort de stabilisation mentionné ci-dessus, nous aimerions faire le ménage dans certains de nos problèmes de longue date. Plus important encore, nous voulons nous assurer que nos tickets sont correctement organisés, afin que les nouveaux contributeurs puissent trouver de bons tickets sur lesquels travailler.

## Priorité : Assistance utilisateur

Un des aspects mentionnés ci-dessus sur lequel nous allons nous concentrer est de rester en contact avec les utilisateurs qui prennent le temps de signaler des problèmes. Merci ! Plus nous pourrons raccourcir la boucle de retour d’information, plus vite nous pourrons résoudre les problèmes auxquels les nouveaux utilisateurs sont confrontés, et plus il est probable qu’ils continueront à participer à la communauté.

## Nous serions ravis de votre aide !

Tout cela paraît très ambitieux, et ça l’est ! Mais nombre des éléments ci‑dessus se recoupent et, avec une planification soignée, nous pouvons les entamer sérieusement.

Si vous souhaitez contribuer à l’un des objectifs ci-dessus, venez discuter avec nous ! Vous pouvez nous trouver sur OFTC et Freenode (#i2p-dev), ainsi que sur Twitter (@GetI2P).
