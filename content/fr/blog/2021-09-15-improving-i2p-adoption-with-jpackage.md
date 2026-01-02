---
title: "Améliorer l’adoption d’I2P et l’intégration des nouveaux utilisateurs avec Jpackage et I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Des méthodes polyvalentes et émergentes pour installer et intégrer I2P dans votre application"
categories: ["general"]
API_Translate: vrai
---

Pendant la majeure partie de son existence, I2P a été une application qui s'exécute grâce à une machine virtuelle Java déjà installée sur la plateforme. Cela a toujours été la manière normale de distribuer des applications Java, mais cela entraîne une procédure d'installation compliquée pour de nombreuses personnes. Pour compliquer encore les choses, la "bonne solution" pour rendre l'installation d'I2P simple sur une plateforme donnée n'est pas forcément la même que sur une autre plateforme. Par exemple, I2P est assez simple à installer avec les outils standard sur les systèmes d'exploitation basés sur Debian et Ubuntu, parce que nous pouvons simplement indiquer les composants Java nécessaires comme "Required" par notre paquet, cependant sous Windows ou OSX, il n'existe pas de tel système nous permettant de nous assurer qu'une version compatible de Java est installée.

La solution évidente serait de gérer nous-mêmes l’installation de Java, mais cela était en soi un problème, en dehors du cadre d’I2P. Cependant, dans les versions récentes de Java, un nouvel ensemble d’options est apparu, susceptible de résoudre ce problème pour de nombreux logiciels Java. Cet outil prometteur s’appelle **"Jpackage."**

## I2P-Zero et installation d'I2P sans dépendances

La première initiative très réussie visant à créer un paquet I2P sans dépendances a été I2P-Zero, créé par le projet Monero à l’origine pour être utilisé avec la cryptomonnaie Monero. Ce projet nous a beaucoup enthousiasmés en raison de son succès à créer un router I2P à usage général qui pouvait être facilement packagé avec une application I2P. En particulier sur Reddit, de nombreuses personnes expriment leur préférence pour la simplicité de la configuration d’un router I2P-Zero.

Cela nous a vraiment prouvé qu’il était possible, avec des outils Java modernes, de proposer un paquet I2P sans dépendances et facile à installer, mais le cas d’utilisation d’I2P-Zero était un peu différent du nôtre. Il convient surtout aux applications embarquées qui ont besoin d’un I2P router qu’elles peuvent contrôler facilement via son port de contrôle pratique, sur le port "8051". Notre prochaine étape serait d’adapter la technologie à l’Application I2P généraliste.

## Les modifications de sécurité des applications sous OSX affectent le I2P IzPack Installer

Le problème est devenu plus pressant dans les versions récentes de Mac OSX, où il n’est plus simple d’utiliser l’installateur "Classic" qui est fourni au format .jar. Cela s’explique par le fait que l’application n’est pas "notarisée" par les autorités d’Apple et qu’elle est considérée comme un risque pour la sécurité. **Cependant**, Jpackage peut produire un fichier .dmg, qui peut être notarisé par les autorités d’Apple, ce qui résout commodément notre problème.

Le nouveau programme d’installation I2P au format .dmg, créé par Zlatinb, rend l’installation d’I2P sur OSX plus facile que jamais, n’oblige plus les utilisateurs à installer eux-mêmes Java et utilise les outils d’installation standard d’OSX comme prévu. Le nouveau programme d’installation .dmg rend la mise en place d’I2P sur Mac OSX plus simple que jamais.

Téléchargez le [dmg](https://geti2p.net/en/download/mac)

## L'I2P du futur est facile à installer

Une des choses que j'entends le plus souvent de la part des utilisateurs, c'est que si I2P veut être adopté, il doit être facile à utiliser pour tout le monde. Beaucoup souhaitent une expérience utilisateur "type Tor Browser", pour citer ou paraphraser de nombreux habitués de Reddit. L'installation ne devrait pas nécessiter des étapes de "post-installation" compliquées et sujettes aux erreurs. Beaucoup de nouveaux utilisateurs ne sont pas prêts à gérer la configuration de leur navigateur de manière approfondie et complète. Pour répondre à ce problème, nous avons créé l'I2P Profile Bundle qui configure Firefox afin qu'il "fonctionne tout simplement" avec I2P. Au fil de son développement, il s'est enrichi de fonctionnalités de sécurité et d'une meilleure intégration avec I2P lui-même. Dans sa dernière version, il intègre **également** un I2P Router complet, propulsé par Jpackage. L'I2P Firefox Profile est désormais une distribution I2P à part entière pour Windows, la seule dépendance restante étant Firefox lui-même. Cela devrait offrir un niveau de commodité sans précédent pour les utilisateurs d'I2P sous Windows.

Téléchargez l’[installateur](https://geti2p.net/en/download#windows)
