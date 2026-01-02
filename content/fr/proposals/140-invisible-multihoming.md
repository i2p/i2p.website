---
title: "Multihébergement invisible"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Ouvrir"
thread: "http://zzz.i2p/topics/2335"
toc: true
---

## Aperçu

Cette proposition décrit la conception d'un protocole permettant à un client I2P, un service ou un processus d'équilibrage externe de gérer de manière transparente plusieurs routers hébergeant une seule [Destination](http://localhost:63465/docs/specs/common-structures/#destination).

La proposition ne spécifie actuellement pas d'implémentation concrète. Elle pourrait être implémentée comme une extension d'[I2CP](/docs/specs/i2cp/), ou comme un nouveau protocole.

## Motivation

Le multihoming consiste à utiliser plusieurs routeurs pour héberger la même Destination. La méthode actuelle pour faire du multihoming avec I2P est d'exécuter la même Destination sur chaque routeur de manière indépendante ; le routeur utilisé par les clients à un moment donné est le dernier à publier un LeaseSet.

C'est un hack et cela ne fonctionnera probablement pas pour de gros sites web à grande échelle. Supposons que nous ayons 100 routeurs multihoming avec chacun 16 tunnels. Cela fait 1600 publications de LeaseSet toutes les 10 minutes, soit presque 3 par seconde. Les floodfills seraient submergés et les limitations se déclencheraient. Et c'est avant même de mentionner le trafic de recherche.

La Proposition 123 résout ce problème avec un méta-LeaseSet, qui liste les 100 hashs de LeaseSet réels. Une recherche devient un processus en deux étapes : d'abord chercher le méta-LeaseSet, puis l'un des LeaseSets nommés. C'est une bonne solution au problème de trafic de recherche, mais en soi cela crée une fuite de confidentialité significative : Il est possible de déterminer quels routeurs multihébergés sont en ligne en surveillant le méta-LeaseSet publié, car chaque LeaseSet réel correspond à un seul routeur.

Nous avons besoin d'un moyen pour qu'un client ou service I2P puisse répartir une seule Destination sur plusieurs routers, d'une manière qui soit indiscernable de l'utilisation d'un seul router (du point de vue du leaseSet lui-même).

## Conception

### Definitions

    User
        The person or organisation wanting to multihome their Destination(s). A
        single Destination is considered here without loss of generality (WLOG).

    Client
        The application or service running behind the Destination. It may be a
        client-side, server-side, or peer-to-peer application; we refer to it as
        a client in the sense that it connects to the I2P routers.

        The client consists of three parts, which may all be in the same process
        or may be split across processes or machines (in a multi-client setup):

        Balancer
            The part of the client that manages peer selection and tunnel
            building. There is a single balancer at any one time, and it
            communicates with all I2P routers. There may be failover balancers.

        Frontend
            The part of the client that can be operated in parallel. Each
            frontend communicates with a single I2P router.

        Backend
            The part of the client that is shared between all frontends. It has
            no direct communication with any I2P router.

    Router
        An I2P router run by the user that sits at the boundary between the I2P
        network and the user's network (akin to an edge device in corporate
        networks). It builds tunnels under the command of a balancer, and routes
        packets for a client or frontend.

### High-level overview

Imaginez la configuration souhaitée suivante :

- Une application cliente avec une seule Destination.
- Quatre routers, chacun gérant trois tunnels entrants.
- Les douze tunnels doivent être publiés dans un seul leaseSet.

### Single-client

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]-----
                 |-{ [Tunnel 3]===/               \
                 |                                 \
                 |-{ [Tunnel 4]===\                 \
  [Destination]  |-{ [Tunnel 5]====[Router 2]-----   \
    \            |-{ [Tunnel 6]===/               \   \
     [LeaseSet]--|                               [Client]
                 |-{ [Tunnel 7]===\               /   /
                 |-{ [Tunnel 8]====[Router 3]-----   /
                 |-{ [Tunnel 9]===/                 /
                 |                                 /
                 |-{ [Tunnel 10]==\               /
                 |-{ [Tunnel 11]===[Router 4]-----
                  -{ [Tunnel 12]==/
```
### Définitions

```
                -{ [Tunnel 1]===\
                 |-{ [Tunnel 2]====[Router 1]---------[Frontend 1]
                 |-{ [Tunnel 3]===/          \                    \
                 |                            \                    \
                 |-{ [Tunnel 4]===\            \                    \
  [Destination]  |-{ [Tunnel 5]====[Router 2]---\-----[Frontend 2]   \
    \            |-{ [Tunnel 6]===/          \   \                \   \
     [LeaseSet]--|                         [Balancer]            [Backend]
                 |-{ [Tunnel 7]===\          /   /                /   /
                 |-{ [Tunnel 8]====[Router 3]---/-----[Frontend 3]   /
                 |-{ [Tunnel 9]===/            /                    /
                 |                            /                    /
                 |-{ [Tunnel 10]==\          /                    /
                 |-{ [Tunnel 11]===[Router 4]---------[Frontend 4]
                  -{ [Tunnel 12]==/
```
### Aperçu de haut niveau

- Charger ou générer une Destination.

- Ouvrir une session avec chaque routeur, liée à la Destination.

- Périodiquement (environ toutes les dix minutes, mais plus ou moins selon la
  vivacité des tunnels) :

- Obtenir le niveau rapide de chaque router.

- Utiliser le sur-ensemble de pairs pour construire des tunnels vers/depuis chaque router.

    - By default, tunnels to/from a particular router will use peers from
      that router's fast tier, but this is not enforced by the protocol.

- Collecter l'ensemble des tunnels entrants actifs de tous les routeurs actifs, et créer un LeaseSet.

- Publier le LeaseSet à travers un ou plusieurs des routeurs.

### Client unique

Pour créer et gérer cette configuration, le client a besoin des fonctionnalités nouvelles suivantes au-delà de ce qui est actuellement fourni par [I2CP](/docs/specs/i2cp/) :

- Dire à un router de construire des tunnels, sans créer un LeaseSet pour eux.
- Obtenir une liste des tunnels actuels dans le pool entrant.

De plus, les fonctionnalités suivantes permettraient une flexibilité significative dans la façon dont le client gère ses tunnels :

- Obtenir le contenu du niveau rapide d'un router.
- Dire à un router de construire un tunnel entrant ou sortant en utilisant une liste donnée de
  pairs.

### Multi-client

```
         Client                           Router

                    --------------------->  Create Session
   Session Status  <---------------------
                    --------------------->  Get Fast Tier
        Peer List  <---------------------
                    --------------------->  Create Tunnel
    Tunnel Status  <---------------------
                    --------------------->  Get Tunnel Pool
      Tunnel List  <---------------------
                    --------------------->  Publish LeaseSet
                    --------------------->  Send Packet
      Send Status  <---------------------
  Packet Received  <---------------------
```
### Processus général du client

**Créer une Session** - Créer une session pour la Destination donnée.

**Statut de Session** - Confirmation que la session a été configurée, et le client peut maintenant commencer à construire des tunnels.

**Get Fast Tier** - Demander une liste des pairs que le router considère actuellement pour construire des tunnels.

**Liste des pairs** - Une liste des pairs connus du router.

**Créer un Tunnel** - Demander au router de construire un nouveau tunnel à travers les pairs spécifiés.

**Statut du Tunnel** - Le résultat d'une construction de tunnel particulière, une fois qu'il est disponible.

**Get Tunnel Pool** - Demander une liste des tunnels actuels dans le pool entrant ou sortant pour la Destination.

**Liste des Tunnels** - Une liste de tunnels pour le pool demandé.

**Publier LeaseSet** - Demande que le router publie le LeaseSet fourni à travers l'un des tunnels sortants pour la Destination. Aucun statut de réponse n'est nécessaire ; le router doit continuer à réessayer jusqu'à ce qu'il soit satisfait que le LeaseSet ait été publié.

**Send Packet** - Un paquet sortant du client. Spécifie optionnellement un tunnel sortant par lequel le paquet doit (devrait ?) être envoyé.

**Statut d'envoi** - Informe le client du succès ou de l'échec de l'envoi d'un paquet.

**Paquet Reçu** - Un paquet entrant pour le client. Spécifie optionnellement le tunnel entrant par lequel le paquet a été reçu(?)

## Security implications

Du point de vue des routers, cette conception est fonctionnellement équivalente au statu quo. Le router construit toujours tous les tunnels, maintient ses propres profils de pairs, et applique la séparation entre les opérations du router et du client. Dans la configuration par défaut, c'est complètement identique, car les tunnels pour ce router sont construits à partir de son propre niveau rapide.

Du point de vue de la netDB, un seul LeaseSet créé via ce protocole est identique au statu quo, car il exploite des fonctionnalités préexistantes. Cependant, pour des LeaseSets plus importants approchant 16 Leases, il peut être possible pour un observateur de déterminer que le LeaseSet est multihébergé :

- La taille maximale actuelle du niveau rapide est de 75 pairs. La passerelle d'entrée
  (IBGW, le nœud publié dans un Lease) est sélectionnée à partir d'une fraction du niveau
  (partitionnée aléatoirement par pool de tunnel par hash, pas par nombre) :

      1 hop
          The whole fast tier

      2 hops
          Half of the fast tier
          (the default until mid-2014)

      3+ hops
          A quarter of the fast tier
          (3 being the current default)

Cela signifie qu'en moyenne les IBGW proviendront d'un ensemble de 20 à 30 pairs.

- Dans une configuration single-homed, un leaseSet complet de 16 tunnels aurait 16 IBGWs sélectionnés aléatoirement parmi un ensemble de jusqu'à (disons) 20 pairs.

- Dans une configuration multihomée à 4 routeurs utilisant la configuration par défaut, un LeaseSet complet à 16 tunnels aurait 16 IBGWs sélectionnés aléatoirement parmi un ensemble d'au maximum 80 pairs, bien qu'il soit probable qu'il y ait une fraction de pairs communs entre les routeurs.

Ainsi, avec la configuration par défaut, il pourrait être possible par analyse statistique de déterminer qu'un LeaseSet est généré par ce protocole. Il pourrait également être possible de déterminer combien de routers il y a, bien que l'effet du renouvellement sur les niveaux rapides réduirait l'efficacité de cette analyse.

Comme le client a un contrôle total sur les pairs qu'il sélectionne, cette fuite d'informations pourrait être réduite ou éliminée en sélectionnant les IBGW à partir d'un ensemble réduit de pairs.

## Compatibility

Cette conception est entièrement rétrocompatible avec le réseau, car il n'y a aucun changement au format LeaseSet. Tous les routeurs devraient être conscients du nouveau protocole, mais cela ne pose pas de problème car ils seraient tous contrôlés par la même entité.

## Performance and scalability notes

La limite supérieure de 16 Leases par LeaseSet n'est pas modifiée par cette proposition. Pour les Destinations qui nécessitent plus de tunnels que cela, il existe deux modifications réseau possibles :

- Augmenter la limite supérieure de la taille des LeaseSets. Ce serait le plus simple à implémenter (bien que cela nécessiterait encore un support réseau généralisé avant de pouvoir être largement utilisé), mais pourrait entraîner des recherches plus lentes en raison de la taille plus importante des paquets. La taille maximale réalisable d'un LeaseSet est définie par le MTU des transports sous-jacents, et se situe donc autour de 16kB.

- Implémenter la Proposition 123 pour les LeaseSets à niveaux. En combinaison avec cette proposition,
  les Destinations pour les sous-LeaseSets pourraient être réparties sur plusieurs
  routers, agissant efficacement comme plusieurs adresses IP pour un service clearnet.

## Acknowledgements

Merci à psi pour la discussion qui a mené à cette proposition.
