---
title: "Notes d'état I2P du 2004-08-10"
date: 2004-08-10
author: "jr"
description: "Mise à jour hebdomadaire de l'état d'I2P portant sur les performances de la version 0.3.4.1, l'équilibrage de charge des outproxy (proxy de sortie vers l'Internet clair) et des mises à jour de la documentation"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

## Index :

1. 0.3.4.1 status
2. Updated docs
3. 0.4 progress
4. ???

## 1) 0.3.4.1 statut

Eh bien, nous avons publié la version 0.3.4.1 l’autre jour, et elle fonctionne plutôt bien. Les connexions sur IRC tiennent régulièrement plusieurs heures, et les débits de transfert sont également assez bons (l’autre jour, j’ai atteint 25KBps depuis un eepsite(site I2P) en utilisant 3 flux parallèles).

Une fonctionnalité vraiment sympa ajoutée dans la version 0.3.4.1 (que j’ai oublié de mentionner dans l’annonce de version) a été le correctif de mule permettant à l’eepproxy d’effectuer un « round-robin » (répartition circulaire) des requêtes non-I2P via une série d’outproxies (proxies de sortie). La valeur par défaut reste simplement d’utiliser l’outproxy squid.i2p, mais si vous allez dans votre router.config et modifiez la ligne clientApp pour qu’elle contienne :

```
-e 'httpclient 4444 squid.i2p,www1.squid.i2p'
```
il acheminera aléatoirement chaque requête HTTP via l’un des deux proxies de sortie répertoriés (squid.i2p et www1.squid.i2p). Avec ça, si quelques personnes de plus font tourner des proxies de sortie, vous ne serez pas aussi dépendants de squid.i2p. Bien sûr, vous avez tous entendu mes préoccupations concernant les proxies de sortie, mais disposer de cette possibilité donne aux gens plus d’options.

Nous avons constaté une certaine instabilité ces dernières heures, mais avec l'aide de duck et cervantes, j'ai identifié deux bogues coriaces et je teste des correctifs en ce moment. Les correctifs sont conséquents, donc je prévois de publier une 0.3.4.2 d'ici un jour ou deux, après avoir vérifié les résultats.

## 2) Documentation mise à jour

Nous avons un peu relâché nos efforts pour tenir la documentation du site à jour et, même s’il reste encore quelques grosses lacunes (p. ex. la documentation de netDb et d’i2ptunnel), nous en avons récemment mis quelques-unes à jour (les comparaisons de réseaux et la FAQ). À l’approche des versions 0.4 et 1.0, j’aimerais que des personnes parcourent le site et identifient ce qui peut être amélioré.

À noter en particulier, un Hall of Fame mis à jour - nous l’avons enfin synchronisé pour refléter les généreux dons que vous toutes et tous avez effectués (merci !) À l’avenir, nous utiliserons ces ressources pour rémunérer les développeurs et autres contributeurs, ainsi que pour couvrir les coûts engagés (p. ex. fournisseurs d’hébergement, etc.).

## 3) Avancement de la 0.4

En relisant les notes de la semaine dernière, il nous reste encore quelques points pour la 0.4, mais les simulations se sont plutôt bien déroulées et la majorité des problèmes liés à Kaffe ont été identifiés. Ce qui serait très utile, toutefois, ce serait que vous mettiez à l’épreuve différents aspects du router ou des applications clientes et que vous signaliez tous les bogues que vous rencontrez.

## 4) ???

C’est tout ce que j’ai à aborder pour le moment — j’apprécie le temps que vous prenez tous pour nous aider à avancer, et je pense que nous faisons de grands progrès. Bien sûr, si quelqu’un a autre chose dont il veut parler, passez à la réunion sur #i2p à… euh… maintenant :)

=jr
