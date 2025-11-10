---
title: "Version 1.9.0 du pack d'installation facile pour Windows"
date: 2022-08-28
author: "idk"
description: "Windows Easy-Install Bundle 1.9.0 - Améliorations majeures de stabilité/compatibilité"
categories: ["release"]
API_Translate: vrai
---

## Cette mise à jour inclut le nouveau router 1.9.0 et des améliorations majeures du confort d'utilisation pour les utilisateurs du bundle.

Cette version inclut le nouveau router I2P 1.9.0 et est basée sur Java 18.02.1.

Les anciens scripts batch ont été abandonnés au profit d’une solution plus flexible et plus stable, intégrée directement à jpackage. Cela devrait corriger tous les bogues liés à la résolution des chemins et à la mise entre guillemets des chemins qui étaient présents dans les scripts batch. Après la mise à jour, les scripts batch peuvent être supprimés en toute sécurité. Ils seront supprimés par le programme d’installation lors de la prochaine mise à jour.

Un sous-projet dédié à la gestion des outils de navigation a été lancé : i2p.plugins.firefox, qui offre de vastes capacités pour configurer automatiquement et de manière stable les navigateurs I2P sur de nombreuses plateformes. Celui-ci a été utilisé pour remplacer les scripts batch, mais sert également d'outil de gestion multiplateforme pour l'I2P Browser. Les contributions sont les bienvenues ici : http://git.idk.i2p/idk/i2p.plugins.firefox dans le dépôt source.

Cette version améliore la compatibilité avec les routers I2P s’exécutant en externe, comme ceux fournis par le programme d’installation IzPack et par des implémentations de router tierces telles que i2pd. En améliorant la découverte des routers externes, elle requiert moins de ressources système, améliore le temps de démarrage et empêche que des conflits de ressources ne se produisent.

Par ailleurs, le profil a été mis à jour vers la dernière version du profil Arkenfox. I2P en navigation privée et NoScript ont tous deux été mis à jour. Le profil a été restructuré afin de pouvoir évaluer différentes configurations selon différents modèles de menace.
