---
title: "Limites de Congestion"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Ouvert"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Vue d'ensemble

Ajoutez des indicateurs de congestion au Router Info (RI) publié.




## Motivation

Les "caps" (capacités) de bande passante indiquent les limites de partage de bande passante et la connectivité mais pas l'état de congestion.
Un indicateur de congestion aidera les routeurs à éviter de tenter de construire via un routeur congestionné,
ce qui contribue à plus de congestion et réduit le succès de la construction de tunnels.



## Conception

Définir de nouvelles capacités pour indiquer divers niveaux de congestion ou de problèmes de capacité.
Ceux-ci seront dans les capacités RI de niveau supérieur, pas dans les capacités d'adresse.


### Définition de la Congestion

La congestion, en général, signifie que le pair est peu susceptible de
recevoir et accepter une demande de construction de tunnel.
La définition ou la classification des niveaux de congestion dépend de l'implémentation.

Les implémentations peuvent considérer un ou plusieurs des éléments suivants :

- Aux limites ou proches des limites de bande passante
- Aux limites ou proches des tunnels participants maximums
- Aux limites ou proches des connexions maximums sur un ou plusieurs transports
- Au-dessus du seuil pour la profondeur de la file d'attente, la latence ou l'utilisation du CPU ; débordement de file d'attente interne
- Capacités de base de la plateforme / système d'exploitation pour le CPU et la mémoire
- Congestion perçue du réseau
- État du réseau tel que pare-feu ou NAT symétrique ou caché ou avec proxy
- Configuré pour ne pas accepter les tunnels

L'état de congestion doit être basé sur une moyenne des conditions
sur plusieurs minutes, pas une mesure instantanée.



## Spécification

Mettre à jour [NETDB](/docs/how/network-database/) comme suit :


```text
D : Congestion moyenne, ou un routeur à faibles performances (par exemple Android, Raspberry Pi)
     Les autres routeurs devraient rétrograder ou limiter
     la capacité apparente de tunnel de ce routeur dans le profil.

  E : Forte congestion, ce routeur est près ou atteint une limite,
     et rejette ou abandonne la plupart des demandes de tunnel.
     Si ce RI a été publié dans les 15 dernières minutes, les autres routeurs
     devraient sévèrement rétrograder ou limiter la capacité de ce routeur.
     Si ce RI est plus ancien que 15 minutes, traiter comme 'D'.

  G : Ce routeur rejette temporairement ou définitivement tous les tunnels.
     Ne pas tenter de construire un tunnel via ce routeur,
     jusqu'à ce qu'un nouveau RI soit reçu sans le 'G'.
```

Pour la cohérence, les implémentations devraient ajouter tout cap de congestion
à la fin (après R ou U).



## Analyse de Sécurité

Toute information de pair publiée ne peut pas être digne de confiance.
Les caps, comme tout autre élément dans le Router Info, peuvent être usurpés.
Nous n'utilisons jamais rien dans le Router Info pour augmenter la capacité perçue d'un routeur.

Publier des indicateurs de congestion, en disant aux pairs d'éviter ce routeur, est intrinsèquement
beaucoup plus sûr que les indicateurs permissifs ou de capacité sollicitant plus de tunnels.

Les indicateurs actuels de capacité de bande passante (L-P, X) sont fiables uniquement pour éviter
les routeurs à très basse bande passante. Le cap "U" (inaccessible) a un effet similaire.

Tout indicateur de congestion publié devrait avoir le même effet que
le rejet ou l'abandon d'une demande de construction de tunnel, avec des propriétés de sécurité similaires.



## Remarques

Les pairs ne doivent pas éviter complètement les routeurs 'D', seulement les sous-évaluer.

Il faut prendre soin de ne pas éviter complètement les routeurs 'E',
pour que lorsque tout le réseau est en congestion et publie 'E',
les choses ne se cassent pas complètement.

Les routeurs peuvent utiliser différentes stratégies pour quels types de tunnels construire via les routeurs 'D' et 'E',
par exemple exploratoire vs. client, ou tunnels clients à haut vs. bas débit.

Les routeurs ne devraient probablement pas publier un cap de congestion au démarrage ou à l'arrêt par défaut,
même si leur état de réseau est inconnu, pour prévenir la détection de redémarrage par les pairs.




## Compatibilité

Aucun problème, toutes les implémentations ignorent les caps inconnus.


## Migration

Les implémentations peuvent ajouter un support à tout moment, sans coordination nécessaire.

Plan préliminaire :
Publier les caps dans 0.9.58 (avril 2023) ;
agir sur les caps publiés dans 0.9.59 (juillet 2023).



## Références

* [NETDB](/docs/how/network-database/)
