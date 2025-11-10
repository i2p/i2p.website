---
title: "Tunnels bidirectionnels"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/2041"
---

## Aperçu

Cette proposition concerne la mise en œuvre de tunnels bidirectionnels dans I2P.


## Motivation

i2pd va introduire des tunnels bidirectionnels construits uniquement à travers d'autres routeurs i2pd pour le moment. Pour le réseau, ils apparaîtront comme des tunnels entrants et sortants réguliers.


## Conception

### Objectifs

1. Réduire l'utilisation du réseau et du processeur en diminuant le nombre de messages TunnelBuild
2. Être capable de savoir instantanément si un participant s'est retiré.
3. Profilage et statistiques plus précis
4. Utiliser d'autres darknets comme pairs intermédiaires


### Modifications du tunnel

TunnelBuild
```````````
Les tunnels sont construits de la même manière que les tunnels entrants. Aucun message de réponse n'est requis. Il y a un type spécial de participant appelé "entrée" marqué par un drapeau, servant à la fois d'IBGW et d'OBEP. Le message a le même format que VaribaleTunnelBuild mais le texte clair contient différents champs ::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Il contiendra également un champ mentionnant à quel darknet appartient le prochain pair et des informations supplémentaires si ce n'est pas I2P.

TunnelTermination
``````````````````
Si un pair veut se retirer, il crée des messages TunnelTermination qu'il chiffre avec la clé de couche et envoie dans la direction "in". Si un participant reçoit un tel message, il le chiffre avec sa clé de couche et l'envoie au pair suivant. Une fois qu'un message atteint le propriétaire du tunnel, il commence à déchiffrer pair par pair jusqu'à obtenir un message non chiffré. Il découvre quel pair s'est retiré et termine le tunnel.
