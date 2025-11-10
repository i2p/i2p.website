---
title: "Recherche de Service"
number: "122"
author: "zzz"
created: "2016-01-13"
lastupdated: "2016-01-13"
status: "Rejeté"
thread: "http://zzz.i2p/topics/2048"
supercedes: "102"
supercededby: "123"
---

## Vue d'ensemble

Voici la proposition complète, extravagante, tout-compris pour le netDB. Également connu sous le nom d'anycast. Ce serait le 4ème sous-type LS2 proposé.

## Motivation

Disons que vous vouliez annoncer votre destination en tant que proxy sortant, ou un nœud GNS, ou une passerelle Tor, ou un DHT Bittorrent ou imule ou i2phex ou un bootstrap Seedless, etc. Vous pourriez stocker cette information dans le netDB au lieu d'utiliser une couche de démarrage ou d'information séparée.

Il n'y a personne en charge, donc contrairement au multihébergement massif, vous ne pouvez pas avoir une liste signée et autoritaire. Vous publieriez donc simplement votre enregistrement sur un floodfill. Le floodfill agrégerait ces informations et les enverrait en réponse aux requêtes.

## Exemple

Disons que votre service était "GNS". Vous enverriez un stockage de base de données au floodfill :

- Hachage de "GNS"
- destination
- horodatage de publication
- expiration (0 pour la révocation)
- port
- signature

Lorsque quelqu'un effectue une recherche, il obtiendrait une liste de ces enregistrements :

- Hachage de "GNS"
- Hachage du floodfill
- Horodatage
- nombre d'enregistrements
- Liste d'enregistrements
- signature du floodfill

Les expirations seraient relativement longues, au moins des heures.

## Implications de sécurité

L'inconvénient est que cela pourrait se transformer en DHT Bittorrent ou pire. À tout le moins, les floodfills devraient sévèrement limiter le débit et la capacité des stockages et requêtes. Nous pourrions mettre sur liste blanche des noms de service approuvés pour des limites plus élevées. Nous pourrions également interdire complètement les services non approuvés.

Bien sûr, même le netDB actuel est sujet à abus. Vous pouvez stocker des données arbitraires dans le netDB, tant qu'elles ressemblent à un RI ou LS et que la signature est correcte. Mais cela rendrait la tâche beaucoup plus facile.
