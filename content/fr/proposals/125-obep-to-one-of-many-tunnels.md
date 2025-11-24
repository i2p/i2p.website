---
title: "Livraison OBEP vers 1-sur-N ou N-sur-N Tunnels"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Open"
thread: "http://zzz.i2p/topics/2099"
---

## Vue d'ensemble

Cette proposition couvre deux améliorations pour améliorer les performances du réseau :

- Déléguer la sélection IBGW à l'OBEP en lui fournissant une liste
  d'alternatives au lieu d'une seule option.

- Activer le routage multicast de paquets à l'OBEP.


## Motivation

Dans le cas de connexion directe, l'idée est de réduire la congestion de la connexion, en
donnant à l'OBEP la flexibilité dans la façon dont il se connecte aux IBGWs. La capacité de spécifier
plusieurs tunnels nous permet également de mettre en œuvre le multicast à l'OBEP (en
livrant le message à tous les tunnels spécifiés).

Une alternative à la partie délégation de cette proposition serait de passer par
un hash [LeaseSet](http://localhost:63465/en/docs/specs/common-structures/#leaseset), semblable à la capacité existante de spécifier un hash cible
[RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification). Cela aboutirait à un message plus petit et potentiellement un
nouveau LeaseSet. Cependant :

1. Cela obligerait l'OBEP à effectuer une recherche

2. Le LeaseSet peut ne pas être publié à un floodfill, donc la recherche échouerait.

3. Le LeaseSet peut être chiffré, donc l'OBEP ne pourrait pas obtenir les leases.

4. Spécifier un LeaseSet révèle à l'OBEP la [Destination](/en/docs/specs/common-structures/#destination) du message,
   qu'ils pourraient autrement seulement découvrir en scrutant tous les LeaseSets dans le
   réseau et en cherchant une correspondance de Lease.


## Conception

L'initiateur (OBGW) placerait certains (tous?) des [Leases](http://localhost:63465/en/docs/specs/common-structures/#lease) cibles dans
les instructions de livraison [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) au lieu d'en choisir un seul.

L'OBEP sélectionnerait l'un de ceux-là pour livrer. L'OBEP sélectionnerait, si
disponible, un à auquel il est déjà connecté, ou qu'il connaît déjà. Cela
rendrait le chemin OBEP-IBGW plus rapide et plus fiable, et réduirait les connexions
réseau globales.

Nous avons un type de livraison inutilisé (0x03) et deux bits restants (0 et 1) dans
les indicateurs pour [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions), que nous pouvons exploiter pour mettre en œuvre ces
fonctionnalités.


## Implications de sécurité

Cette proposition ne change pas la quantité d'informations divulguées sur la
destination cible de l'OBGW ou leur vision du NetDB :

- Un adversaire qui contrôle l'OBEP et scrute les LeaseSets du NetDB peut déjà
  déterminer si un message est envoyé à une Destination particulière, en
  recherchant la paire [TunnelId](http://localhost:63465/en/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/en/docs/specs/common-structures/#common-structure-specification). Au pire, la présence de
  multiples Leases dans le TMDI pourrait accélérer la recherche d'une
  correspondance dans la base de données de l'adversaire.

- Un adversaire qui exploite une Destination malveillante peut déjà obtenir
  des informations sur la vision du NetDB d'une victime se connectant, en
  publiant des LeaseSets contenant différents tunnels entrants vers différents floodfills,
  et en observant par quels tunnels l'OBGW se connecte. De leur point de vue,
  la sélection du tunnel par l'OBEP est fonctionnellement identique à la sélection
  faite par l'OBGW.

Le drapeau multicast divulgue le fait que l'OBGW envoie en multicast aux OBEPs.
Cela crée un compromis entre performance et confidentialité qui doit être
considéré lors de l'implémentation de protocoles de haut niveau. Étant un drapeau
optionnel, les utilisateurs peuvent prendre la décision appropriée pour leur
application. Il peut être bénéfique que cela soit le comportement par défaut
pour les applications compatibles, cependant, étant donné qu'une utilisation
généralisée par une variété d'applications réduirait la fuite d'informations
concernant l'application particulière d'où provient un message.


## Spécification

Les instructions de livraison du premier fragment [TUNNEL-DELIVERY](/en/docs/specs/i2np/#tunnel-message-delivery-instructions) seraient
modifiées comme suit :

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Message  
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|cnt | (o)
+----+----+----+----+----+----+----+----+
 Tunnel ID N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         To Hash N (optional)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | Tunnel ID N+1 (o) |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         To Hash N+1 (optional)        |
+                                       +
|                                       |
+                                  +----+
|                                  | sz
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bits 6-5: type de livraison
                 0x03 = TUNNELS
       bit 0: multicast? Si 0, livrer à l'un des tunnels
                         Si 1, livrer à tous les tunnels
                         Mettre à 0 pour la compatibilité avec les futurs usages si
                         le type de livraison n'est pas TUNNELS

Count ::
       1 byte
       Optionnel, présent si le type de livraison est TUNNELS
       2-255 - Nombre de paires id/hash à suivre

Tunnel ID :: `TunnelId`
To Hash ::
       36 bytes chacun
       Optionnel, présent si le type de livraison est TUNNELS
       paires id/hash

Longueur totale : La longueur typique est :
       75 bytes pour une livraison TUNNELS à compte 2 (message de tunnel non fragmenté);
       79 bytes pour une livraison TUNNELS à compte 2 (premier fragment)

Le reste des instructions de livraison reste inchangé
```


## Compatibilité

Les seuls pairs qui ont besoin de comprendre la nouvelle spécification sont les OBGWs
et les OBEPs. Nous pouvons donc rendre ce changement compatible avec le réseau
existant en rendant son utilisation conditionnelle à la version cible I2P [VERSIONS](/en/docs/specs/i2np/#protocol-versions) :

* Les OBGWs doivent sélectionner des OBEPs compatibles lors de la construction
  de tunnels sortants, en se basant sur la version I2P annoncée dans leur [RouterInfo](http://localhost:63465/en/docs/specs/common-structures/#routerinfo).

* Les pairs qui annoncent la version cible doivent supporter l'analyse des
  nouveaux drapeaux, et ne doivent pas rejeter les instructions comme invalides.

