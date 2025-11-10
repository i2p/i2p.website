---
title: "Routes Restreintes"
number: "100"
author: "zzz"
created: "2008-09-14"
lastupdated: "2008-10-13"
status: "Reserve"
thread: "http://zzz.i2p/topics/114"
---

## Introduction


## Réflexions

- Ajouter un nouveau transport "IND" (indirect) qui publie un hash leaseSet dans la 
  structure RouterAddress : "IND : [key=aababababababababb]". Ce transport propose 
  la plus basse priorité lorsque le routeur cible le publie. Pour envoyer à un pair via 
  ce transport, récupérer le leaseset d'un pair ff comme d'habitude, et l'envoyer 
  directement au lease.

- Un pair annonçant IND doit construire et maintenir un ensemble de tunnels vers un 
  autre pair. Ce ne sont pas des tunnels exploratoires ni des tunnels clients, mais un 
  deuxième ensemble de tunnels routeurs.

  - 1-hop est-il suffisant ?
  - Comment sélectionner les pairs pour ces tunnels ?
  - Ils doivent être "non restreints" mais comment le savoir ? Cartographie de la 
    connectivité ? La théorie des graphes, les algorithmes, les structures de données 
    peuvent aider ici. Besoin de lire à ce sujet. Voir tunnels TODO.

- Si vous avez des tunnels IND alors votre transport IND doit proposer (priorité basse) 
  d'envoyer des messages via ces tunnels.

- Comment décider d'activer la construction de tunnels indirects

- Comment implémenter et tester sans se faire remarquer
