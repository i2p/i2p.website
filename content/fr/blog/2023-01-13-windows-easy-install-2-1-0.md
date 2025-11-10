---
title: "Version 2.1.0 de Windows Easy-Install"
date: 2023-01-13
author: "idk"
description: "Windows Easy-Install Bundle 2.1.0 publié afin d’améliorer la stabilité et les performances"
categories: ["release"]
API_Translate: vrai
---

## Détails de la mise à jour

Le bundle Easy-Install I2P pour Windows version 2.1.0 a été publié. Comme d'habitude, cette version inclut une version mise à jour de l'I2P Router. Cette version d'I2P fournit des stratégies améliorées pour gérer la congestion du réseau. Celles-ci devraient améliorer les performances, la connectivité et garantir la bonne santé à long terme du réseau I2P.

Cette version propose principalement des améliorations internes au lanceur du profil de navigateur. La compatibilité avec le Tor Browser Bundle a été améliorée en permettant la configuration de TBB via des variables d’environnement. Le profil Firefox a été mis à jour, et les versions de base des extensions ont été mises à jour. Des améliorations ont été apportées à l’ensemble de la base de code et au processus de déploiement.

Malheureusement, cette version est toujours un programme d'installation .exe non signé. Veuillez vérifier la somme de contrôle du programme d'installation avant de l'utiliser. Les mises à jour, en revanche, sont signées avec mes clés de signature I2P et sont donc sûres.

Cette version a été compilée avec OpenJDK 19. Elle utilise i2p.plugins.firefox en version 1.0.7 comme bibliothèque pour lancer le navigateur. Elle utilise i2p.i2p en version 2.1.0 en tant qu’I2P router, et pour fournir des applications. Comme toujours, il est recommandé de mettre à jour vers la dernière version de l’I2P router dès que possible.
