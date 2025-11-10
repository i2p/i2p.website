---
title: "Easy-Install pour Windows 2.3.0 publié"
date: 2023-07-10
author: "idk"
description: "Easy-Install pour Windows 2.3.0 publié"
categories: ["release"]
API_Translate: vrai
---

L’I2P Easy-Install bundle pour Windows version 2.3.0 est désormais disponible. Comme d’habitude, cette version inclut un router I2P mis à jour. Cela s’étend aux problèmes de sécurité qui affectent les personnes hébergeant des services sur le réseau.

Il s’agira de la dernière version du bundle Easy-Install à être incompatible avec l’I2P Desktop GUI. Il a été mis à jour pour inclure de nouvelles versions de toutes les extensions Web incluses. Un bogue de longue date dans I2P in Private Browsing, qui le rendait incompatible avec les thèmes personnalisés, a été corrigé. Il est toujours recommandé aux utilisateurs de ne *pas* installer de thèmes personnalisés. Les onglets Snark ne sont pas automatiquement épinglés en haut de l’ordre des onglets dans Firefox. À l’exception de l’utilisation de cookieStores (conteneurs de cookies) alternatifs, les onglets Snark se comportent désormais comme des onglets de navigateur normaux.

**Malheureusement, cette version est toujours un programme d'installation `.exe` non signé.** Veuillez vérifier la somme de contrôle du programme d'installation avant de l'utiliser. **Les mises à jour, en revanche** sont signées avec mes clés de signature I2P et sont donc sûres.

Cette version a été compilée avec OpenJDK 20. Elle utilise i2p.plugins.firefox version 1.1.0 comme bibliothèque pour lancer le navigateur. Elle utilise i2p.i2p version 2.3.0 en tant qu'I2P router, et pour fournir des applications. Comme toujours, il est recommandé de mettre à jour vers la dernière version de l'I2P router dès que cela vous est possible.

- [Easy-Install Bundle Source](http://git.idk.i2p/i2p-hackers/i2p.firefox/-/tree/i2p-firefox-2.3.0)
- [Router Source](http://git.idk.i2p/i2p-hackers/i2p.i2p/-/tree/i2p-2.3.0)
- [Profile Manager Source](http://git.idk.i2p/i2p-hackers/i2p.plugins.firefox/-/tree/1.1.0)
