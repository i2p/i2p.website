---
title: "Hébergement Multiple Invisible"
number: "140"
author: "str4d"
created: "2017-05-22"
lastupdated: "2017-07-04"
status: "Open"
thread: "http://zzz.i2p/topics/2335"
---

## Vue d'ensemble

Cette proposition présente un design pour un protocole permettant à un client I2P, un service ou un processus de répartition externe de gérer plusieurs routeurs hébergeant de manière transparente une seule [Destination](http://localhost:63465/en/docs/specs/common-structures/#destination).

La proposition ne spécifie actuellement pas une implémentation concrète. Elle pourrait être implémentée comme une extension de [I2CP](/en/docs/specs/i2cp/) ou comme un nouveau protocole.

## Motivation

L'hébergement multiple consiste à utiliser plusieurs routeurs pour héberger la même destination. La manière actuelle de procéder avec I2P est de faire fonctionner la même destination sur chaque routeur de manière indépendante ; le routeur utilisé par les clients à un moment donné est le dernier à publier un [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset).

C'est un hack et cela ne fonctionne probablement pas pour des sites web de grande taille. Disons que nous avions 100 routeurs d'hébergement multiple chacun avec 16 tunnels. Cela ferait 1600 publications de LeaseSet toutes les 10 minutes, soit presque 3 par seconde. Les floodfills seraient submergés et des limitations interviendraient. Et cela avant même de mentionner le trafic de recherche.

[Proposal 123](/en/proposals/123-new-netdb-entries/) résout ce problème avec un meta-LeaseSet, qui liste les 100 vrais hachages de LeaseSet. Une recherche devient un processus en deux étapes : d'abord rechercher le meta-LeaseSet, puis l'un des LeaseSet nommés. C'est une bonne solution au problème du trafic de recherche, mais à elle seule elle crée une fuite de confidentialité importante : il est possible de déterminer quels routeurs d'hébergement multiple sont en ligne en surveillant le meta-LeaseSet publié, car chaque vrai LeaseSet correspond à un seul routeur.

Nous avons besoin d'un moyen pour qu'un client ou service I2P puisse répartir une seule destination sur plusieurs routeurs, de manière indiscernable de l'utilisation d'un seul routeur (du point de vue du LeaseSet lui-même).

## Design

### Définitions

    Utilisateur
        La personne ou l'organisation souhaitant héberger en multiple leur(s) destination(s). 
        Une seule destination est considérée ici sans perte de généralité (WLOG).

    Client
        L'application ou le service fonctionnant derrière la destination. 
        Il peut s'agir d'une application côté client, côté serveur, ou peer-to-peer ; 
        nous le désignons comme un client dans le sens où il se connecte aux routeurs I2P.

        Le client se compose de trois parties, qui peuvent toutes être dans le même processus 
        ou peuvent être réparties entre différents processus ou machines (dans une configuration multi-client):

        Répartiteur
            La partie du client qui gère la sélection des pairs et la construction des tunnels. 
            Il y a un seul répartiteur à tout moment, et il communique avec tous les routeurs I2P. 
            Il peut y avoir des répartiteurs de secours.

        Frontend
            La partie du client qui peut être opérée en parallèle. 
            Chaque frontend communique avec un seul routeur I2P.

        Backend
            La partie du client qui est partagée entre tous les frontends. 
            Elle n'a pas de communication directe avec un routeur I2P.

    Routeur
        Un routeur I2P exploité par l'utilisateur qui se situe à la frontière entre le réseau 
        I2P et le réseau de l'utilisateur (semblable à un dispositif périphérique dans un réseau d'entreprise). 
        Il construit des tunnels sous la commande d'un répartiteur, et route les paquets pour un client ou frontend.

### Vue d'ensemble de haut niveau

Imaginez la configuration souhaitée suivante :

- Une application client avec une destination.
- Quatre routeurs, chacun gérant trois tunnels entrants.
- Tous les douze tunnels devraient être publiés dans un seul LeaseSet.

Single-client

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

Multi-client

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

### Processus général client
- Charger ou générer une destination.

- Ouvrir une session avec chaque routeur, liée à la destination.

- Périodiquement (toutes les dix minutes environ, mais plus ou moins en fonction 
de la survie des tunnels) :

  - Obtenir le niveau rapide de chaque routeur.

  - Utiliser le sur-ensemble de pairs pour construire des tunnels vers/à partir de chaque routeur.

    - Par défaut, les tunnels vers/à partir d'un routeur particulier utiliseront des pairs 
      du niveau rapide de ce routeur, mais cela n'est pas imposé par le protocole.

  - Collecter l'ensemble des tunnels entrants actifs de tous les routeurs actifs 
    et créer un LeaseSet.

  - Publier le LeaseSet par l'intermédiaire d'un ou plusieurs des routeurs.

### Différences avec I2CP
Pour créer et gérer cette configuration, le client a besoin des nouvelles fonctionnalités suivantes 
au-delà de ce qui est actuellement fourni par [I2CP](/en/docs/specs/i2cp/) :

- Dire à un routeur de construire des tunnels, sans créer de LeaseSet pour eux.
- Obtenir une liste des tunnels actuels dans le pool entrant.

De plus, les fonctionnalités suivantes permettraient une flexibilité significative dans la manière 
dont le client gère ses tunnels :

- Obtenir le contenu du niveau rapide d'un routeur.
- Dire à un routeur de construire un tunnel entrant ou sortant en utilisant une liste donnée de pairs.

### Plan du protocole

```
         Client                           Router

                    --------------------->  Créer une session
   État de la session  <---------------------
                    --------------------->  Obtenir le niveau rapide
        Liste des pairs  <---------------------
                    --------------------->  Créer un tunnel
    État du tunnel  <---------------------
                    --------------------->  Obtenir le pool de tunnels
      Liste des tunnels  <---------------------
                    --------------------->  Publier le LeaseSet
                    --------------------->  Envoyer un paquet
      État de l'envoi  <---------------------
  Paquet reçu  <---------------------

### Messages
    Créer une session
        Créer une session pour la destination donnée.

    État de la session
        Confirmation que la session a été établie et que le client peut maintenant
        commencer à construire des tunnels.

    Obtenir le niveau rapide
        Demander une liste des pairs que le routeur envisagerait actuellement 
        de construire des tunnels à travers.

    Liste des pairs
        Une liste de pairs connus du routeur.

    Créer un tunnel
        Demander au routeur de construire un nouveau tunnel à travers les pairs spécifiés.

    État du tunnel
        Le résultat d'une construction de tunnel particulière, une fois qu'elle est disponible.

    Obtenir le pool de tunnels
        Demander une liste des tunnels actuels dans le pool entrant ou sortant
        pour la destination.

    Liste des tunnels
        Une liste de tunnels pour le pool demandé.

    Publier le LeaseSet
        Demander au routeur de publier le LeaseSet fourni par l'un des
        tunnels sortants pour la destination. Aucun état de réponse n'est nécessaire; 
        le routeur devrait continuer à réessayer jusqu'à ce qu'il soit satisfait que 
        le LeaseSet ait été publié.

    Envoyer un paquet
        Un paquet sortant du client. Spécifie éventuellement un tunnel sortant à travers lequel 
        le paquet doit (peut-être ?) être envoyé.

    État de l'envoi
        Informe le client du succès ou de l'échec de l'envoi d'un paquet.

    Paquet reçu
        Un paquet entrant pour le client. Spécifie éventuellement le tunnel entrant 
        à travers lequel le paquet a été reçu(?)

## Implications de sécurité

Du point de vue des routeurs, ce design est fonctionnellement équivalent au statut quo. Le routeur construit toujours tous les tunnels, maintient ses propres profils de pairs et applique la séparation entre les opérations du routeur et du client. Dans la configuration par défaut, il est complètement identique, car les tunnels pour ce routeur sont construits à partir de son propre niveau rapide.

Du point de vue du netDB, un seul LeaseSet créé via ce protocole est identique au statut quo, car il exploite des fonctionnalités préexistantes. Cependant, pour des LeaseSets plus grands approchant 16 Leases, il peut être possible pour un observateur de déterminer que le LeaseSet est hébergé multiple :

- La taille maximale actuelle du niveau rapide est de 75 pairs. La passerelle entrante (IBGW, le nœud publié dans un Lease) est sélectionnée dans une fraction du niveau (partitionnée aléatoirement par pool de tunnels, par hachage, pas par décompte) :

      1 hop
          L'ensemble du niveau rapide

      2 hops
          La moitié du niveau rapide
          (le défaut jusqu'à mi-2014)

      3+ hops
          Un quart du niveau rapide
          (3 étant actuellement la valeur par défaut)

  Cela signifie qu'en moyenne, les IBGWs proviendront d'un ensemble de 20 à 30 pairs.

- Dans une configuration à hébergement simple, un LeaseSet complet de 16 tunnels aurait 16 IBGWs
  sélectionnés aléatoirement dans un ensemble allant jusqu'à (disons) 20 pairs.

- Dans une configuration à 4 routeurs hébergée multiple utilisant la configuration par défaut, 
  un LeaseSet complet de 16 tunnels aurait 16 IBGWs sélectionnés aléatoirement dans un ensemble d'au
  plus 80 pairs, bien qu'il soit probable qu'il y ait une fraction de pairs communs entre les routeurs.

Ainsi, avec la configuration par défaut, il peut être possible, grâce à une analyse statistique, de déterminer qu'un LeaseSet est généré par ce protocole. Il pourrait également être possible de déterminer combien de routeurs il y a, bien que l'effet de la rotation sur les niveaux rapides réduirait l'efficacité de cette analyse.

Comme le client a un contrôle total sur les pairs qu'il sélectionne, cette fuite d'information pourrait être réduite ou éliminée en sélectionnant les IBGWs à partir d'un ensemble réduit de pairs.

## Compatibilité

Ce design est complètement compatible à rebours avec le réseau, car il n'y a aucun changement dans le format du [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset). Tous les routeurs devraient être conscients du nouveau protocole, mais ce n'est pas un problème car ils seraient tous contrôlés par la même entité.

## Notes de performance et de scalabilité

La limite supérieure de 16 [Lease](http://localhost:63465/en/docs/specs/common-structures/#lease) par LeaseSet n'est pas modifiée par cette proposition. Pour les destinations qui nécessitent plus de tunnels que cela, il y a deux modifications possibles du réseau :

- Augmenter la limite supérieure sur la taille des LeaseSets. Cela serait le plus simple à implémenter (bien que cela nécessiterait encore un support réseau répandu avant d'être largement utilisé), mais pourrait entraîner des recherches plus lentes en raison de la taille plus importante des paquets. La taille maximale réalisable d'un LeaseSet est définie par le MTU des transports sous-jacents, et est donc d'environ 16 kB.

- Mettre en œuvre [Proposal 123](/en/proposals/123-new-netdb-entries/) pour les LeaseSets hiérarchisés. En combinaison avec cette proposition, les destinations pour les sous-LeaseSets pourraient être réparties sur plusieurs routeurs, agissant effectivement comme plusieurs adresses IP pour un service en clair.

## Remerciements

Merci à psi pour la discussion qui a conduit à cette proposition.
