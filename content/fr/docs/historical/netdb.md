---
title: "Discussion sur la base de données réseau"
description: "Notes historiques sur floodfill, les expérimentations Kademlia, et l'optimisation future pour la netDb"
slug: "netdb"
aliases:
  - "/fr/docs/legacy/netdb"
  - "/fr/docs/legacy/netdb/"
  - "/fr/netdb_discussion"
  - "/fr/netdb_discussion/"
lastUpdated: "2008-03"
accurateFor: "0.7"
---

NOTE : Ce qui suit est une discussion sur l'historique de l'implémentation de netDb et n'est pas une information actuelle. Voir [la page principale de netDb](/docs/overview/network-database) pour la documentation actuelle.

## Historique {#status}

Le netDb est distribué avec une technique simple appelée "floodfill". Il y a longtemps, le netDb utilisait aussi le DHT Kademlia comme algorithme de secours. Cependant, cela ne fonctionnait pas bien dans notre application, et cela a été complètement désactivé dans la version 0.6.1.20.

*(Adapté d'un message de jrandom dans l'ancien Syndie, 26 nov. 2005)*

Le floodfill netDb n'est en réalité qu'une mesure simple et peut-être temporaire, utilisant l'algorithme le plus simple possible - envoyer les données à un pair dans le floodfill netDb, attendre 10 secondes, choisir un pair aléatoire dans le netDb et lui demander l'entrée à envoyer, en vérifiant sa bonne insertion / distribution. Si le pair de vérification ne répond pas, ou s'il n'a pas l'entrée, l'expéditeur répète le processus. Quand le pair dans le floodfill netDb reçoit un stockage netDb d'un pair qui n'est pas dans le floodfill netDb, il l'envoie à tous les pairs dans le floodfill netDb.

À un moment donné, la fonctionnalité de recherche/stockage Kademlia était encore en place. Les pairs considéraient les pairs floodfill comme étant toujours « plus proches » de chaque clé que tout pair ne participant pas au netDb. Nous nous rabattions sur le netDb Kademlia si les pairs floodfill échouaient pour une raison ou une autre. Cependant, Kademlia a ensuite été complètement désactivé (voir ci-dessous).

Plus récemment, Kademlia a été partiellement réintroduit fin 2009, comme moyen de limiter la taille de la netDb que chaque router floodfill doit stocker.

### L'Introduction de l'Algorithme Floodfill

Floodfill a été introduit dans la version 0.6.0.4, en gardant Kademlia comme algorithme de sauvegarde.

*(Adapté des publications de jrandom dans l'ancien Syndie, 26 nov. 2005)*

Comme je l'ai souvent dit, je ne suis pas particulièrement attaché à une technologie spécifique - ce qui compte pour moi, c'est ce qui donnera des résultats. Bien que j'aie travaillé sur diverses idées de netDb au cours des dernières années, les problèmes auxquels nous avons été confrontés ces dernières semaines ont fait ressortir certains d'entre eux. Sur le réseau en direct, avec le facteur de redondance netDb réglé sur 4 peers (ce qui signifie que nous continuons à envoyer une entrée à de nouveaux peers jusqu'à ce que 4 d'entre eux confirment qu'ils l'ont reçue) et le timeout par peer réglé à 4 fois le temps de réponse moyen de ce peer, nous obtenons **encore** une moyenne de 40-60 peers contactés avant que 4 accusent réception du stockage. Cela signifie envoyer 36-56 fois plus de messages que ce qui devrait sortir, chacun utilisant des tunnels et traversant donc 2-4 liens. Qui plus est, cette valeur est fortement biaisée, car le nombre moyen de peers contactés lors d'un stockage 'échoué' (c'est-à-dire que moins de 4 personnes ont accusé réception du message après 60 secondes d'envoi de messages) était dans la fourchette de 130-160 peers.

C'est de la folie, surtout pour un réseau qui ne compte peut-être que 250 pairs.

La réponse la plus simple serait de dire "eh bien, évidemment jrandom, c'est cassé. répare-le", mais cela ne va pas vraiment au cœur du problème. En accord avec un autre effort en cours, il est probable que nous ayons un nombre substantiel de problèmes réseau dus à des routes restreintes - des pairs qui ne peuvent pas communiquer avec certains autres pairs, souvent à cause de problèmes de NAT ou de pare-feu. Si, disons, les K pairs les plus proches d'une entrée netDb particulière sont derrière une 'route restreinte' de sorte que le message de stockage netDb puisse les atteindre mais que le message de recherche netDb d'un autre pair ne le puisse pas, cette entrée serait essentiellement inaccessible. En suivant ces pistes un peu plus loin et en prenant en considération le fait que certaines routes restreintes seront créées avec une intention hostile, il est clair que nous allons devoir examiner de plus près une solution netDb à long terme.

Il existe quelques alternatives, mais deux méritent d'être mentionnées en particulier. La première consiste simplement à exécuter la netDb comme une DHT Kademlia en utilisant un sous-ensemble du réseau complet, où tous ces pairs sont accessibles de l'extérieur. Les pairs qui ne participent pas à la netDb interrogent toujours ces pairs mais ils ne reçoivent pas de messages netDb store ou lookup non sollicités. La participation à la netDb serait à la fois auto-sélective et éliminatoire par l'utilisateur - les routers choisiraient de publier ou non un indicateur dans leur routerInfo indiquant s'ils souhaitent participer, tandis que chaque router choisit quels pairs il veut traiter comme faisant partie de la netDb (les pairs qui publient cet indicateur mais ne fournissent jamais de données utiles seraient ignorés, les éliminant essentiellement de la netDb).

Une autre alternative est un retour aux sources, revenant à la mentalité DTSTTCPW (Do The Simplest Thing That Could Possibly Work - Faire la Chose la Plus Simple Qui Pourrait Possiblement Fonctionner) - un floodfill netDb, mais comme l'alternative ci-dessus, utilisant seulement un sous-ensemble du réseau complet. Quand un utilisateur veut publier une entrée dans le floodfill netDb, il l'envoie simplement à l'un des routeurs participants, attend un ACK, puis 30 secondes plus tard, interroge un autre participant aléatoire dans le floodfill netDb pour vérifier qu'elle a été correctement distribuée. Si c'est le cas, parfait, et si ce n'est pas le cas, il suffit de répéter le processus. Quand un router floodfill reçoit un netDb store, il ACK immédiatement et met en file d'attente le netDb store vers tous ses pairs netDb connus. Quand un router floodfill reçoit un netDb lookup, s'il a les données, il répond avec celles-ci, mais s'il ne les a pas, il répond avec les hachages de, disons, 20 autres pairs dans le floodfill netDb.

En l'examinant du point de vue de l'économie de réseau, la netDb floodfill est assez similaire à la netDb de diffusion originale, sauf que le coût de publication d'une entrée est supporté principalement par les pairs dans la netDb, plutôt que par l'éditeur. En développant cela un peu plus et en traitant la netDb comme une boîte noire, nous pouvons voir que la bande passante totale requise par la netDb est :

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
où :

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
En insérant quelques valeurs :

```
recvKBps = 1000 * (5 + 1) * (1 + 0.05) * (1 + 0.2) * 2KB / 10m
         = 25.2KBps
```
Cela, à son tour, évolue de manière linéaire avec N (avec 100 000 pairs, la netDb doit être capable de gérer des messages de stockage netDb totalisant 2,5 Mo/s, ou, avec 300 pairs, 7,6 Ko/s).

Bien que la netDb floodfill ferait en sorte que chaque participant netDb ne reçoive directement qu'une petite fraction des stockages netDb générés par les clients, ils recevraient tous toutes les entrées à terme, donc tous leurs liens devraient être capables de gérer la totalité des recvKBps. En retour, ils devront tous envoyer `(recvKBps/sizeof(netDb)) * (sizeof(netDb)-1)` pour maintenir les autres pairs synchronisés.

Un floodfill netDb ne nécessiterait ni routage de tunnel pour le fonctionnement du netDb ni aucune sélection spéciale quant aux entrées auxquelles il peut répondre de manière « sûre », car l'hypothèse de base est qu'ils stockent tous tout. Oh, et en ce qui concerne l'utilisation disque requise par le netDb, elle reste assez négligeable pour toute machine moderne, nécessitant environ 11 Mo pour chaque 1000 pairs `(N * (L + 1) * S)`.

Le netDb Kademlia réduirait ces chiffres, les ramenant idéalement à K sur M fois leur valeur, avec K = le facteur de redondance et M étant le nombre de routeurs dans le netDb (par exemple 5/100, donnant un recvKBps de 126KBps et 536MB à 100 000 routeurs). L'inconvénient du netDb Kademlia est cependant la complexité accrue d'un fonctionnement sûr dans un environnement hostile.

Ce à quoi je pense maintenant, c'est d'implémenter et de déployer simplement un floodfill netDb dans notre réseau existant en production, permettant aux pairs qui veulent l'utiliser de sélectionner d'autres pairs qui sont marqués comme membres et de les interroger au lieu d'interroger les pairs netDb Kademlia traditionnels. Les exigences en bande passante et en espace disque à ce stade sont suffisamment triviales (7,6 KBps et 3 MB d'espace disque) et cela supprimera entièrement le netDb du plan de débogage - les problèmes qui restent à résoudre seront causés par quelque chose qui n'est pas lié au netDb.

Comment les pairs seraient-ils choisis pour publier ce drapeau indiquant qu'ils font partie du netDb floodfill ? Au début, cela pourrait être fait manuellement comme une option de configuration avancée (ignorée si le router n'est pas capable de vérifier sa capacité d'accès externe). Si trop de pairs définissent ce drapeau, comment les participants du netDb choisissent-ils lesquels éjecter ? Encore une fois, au début cela pourrait être fait manuellement comme une option de configuration avancée (après avoir supprimé les pairs qui sont injoignables). Comment évitons-nous le partitionnement du netDb ? En faisant en sorte que les routers vérifient que le netDb effectue le flood fill correctement en interrogeant K pairs netDb aléatoires. Comment les routers ne participant pas au netDb découvrent-ils de nouveaux routers par lesquels faire transiter leurs tunnel ? Cela pourrait peut-être être fait en envoyant une requête netDb particulière de sorte que le router netDb répondrait non pas avec des pairs dans le netDb, mais avec des pairs aléatoires en dehors du netDb.

La netDb d'I2P est très différente des DHT traditionnelles supportant une charge - elle ne contient que les métadonnées du réseau, pas de charge utile réelle, c'est pourquoi même une netDb utilisant un algorithme floodfill sera capable de supporter une quantité arbitraire de données I2P Site/IRC/bt/mail/syndie/etc. Nous pouvons même faire quelques optimisations à mesure qu'I2P grandit pour distribuer cette charge un peu plus (peut-être en passant des filtres de Bloom entre les participants de la netDb pour voir ce qu'ils ont besoin de partager), mais il semble que nous puissions nous en sortir avec une solution beaucoup plus simple pour l'instant.

Un fait mérite d'être approfondi - tous les leaseSets n'ont pas besoin d'être publiés dans la netDb ! En fait, la plupart n'en ont pas besoin - seulement ceux des destinations qui recevront des messages non sollicités (c'est-à-dire les serveurs). C'est parce que les messages garlic encryption envoyés d'une destination à une autre incluent déjà le leaseSet de l'expéditeur, de sorte que tout envoi/réception ultérieur entre ces deux destinations (dans une courte période de temps) fonctionne sans aucune activité de la netDb.

Donc, en revenant à ces équations, nous pouvons changer L de 5 à quelque chose comme 0,1 (en supposant que seulement 1 destination sur 50 est un serveur). Les équations précédentes ont également fait abstraction de la charge réseau nécessaire pour répondre aux requêtes des clients, mais bien que celle-ci soit très variable (selon l'activité des utilisateurs), il est également très probable qu'elle soit assez insignifiante comparée à la fréquence de publication.

Quoi qu'il en soit, toujours pas de magie, mais une belle réduction de près d'1/5ème de la bande passante/espace disque requis (peut-être plus tard, selon que la distribution des routerInfo se fasse directement dans le cadre de l'établissement de pairs ou seulement à travers le netDb).

### La désactivation de l'algorithme Kademlia

Kademlia a été complètement désactivé dans la version 0.6.1.20.

*(Adapté d'une conversation IRC avec jrandom 11/07)*

Kademlia nécessite un niveau minimum de service que la configuration de base ne pouvait pas offrir (bande passante, processeur), même après l'ajout de niveaux (Kademlia pur est absurde sur ce point). Kademlia ne fonctionnerait tout simplement pas. C'était une belle idée, mais pas pour un environnement hostile et fluide.

### Statut actuel

Le netDb joue un rôle très spécifique dans le réseau I2P, et les algorithmes ont été ajustés selon nos besoins. Cela signifie également qu'il n'a pas été optimisé pour répondre aux besoins auxquels nous n'avons pas encore été confrontés. I2P est actuellement assez petit (quelques centaines de routers). Il y a eu des calculs montrant que 3 à 5 routers floodfill devraient pouvoir gérer 10 000 nœuds dans le réseau. L'implémentation du netDb répond plus qu'adéquatement à nos besoins actuels, mais il y aura probablement d'autres ajustements et corrections de bogues à mesure que le réseau grandit.

### Mise à jour des calculs 03-2008

Nombres actuels :

```
recvKBps = N * (L + 1) * (1 + F) * (1 + R) * S / T
```
où :

```
N = number of routers in the entire network
L = average number of client destinations on each router
    (+1 for the routerInfo)
F = tunnel failure percentage
R = tunnel rebuild period, as a fraction of the tunnel lifetime
S = average netDb entry size
T = tunnel lifetime
```
Changements dans les hypothèses :

- L est maintenant d'environ 0,5, comparé à 0,1 ci-dessus, en raison de la popularité d'i2psnark
  et d'autres applications.
- F est d'environ 0,33, mais les bogues dans les tests de tunnel sont corrigés dans 0.6.1.33, donc cela va s'améliorer considérablement.
- Puisque netDb contient environ 2/3 de routerInfos de 5K et 1/3 de leaseSets de 2K, S = 4K.
  La taille des RouterInfo diminue dans 0.6.1.32 et 0.6.1.33 car nous supprimons les statistiques inutiles.
- R = période de construction de tunnel : 0,2 était très faible - c'était peut-être 0,7 -
  mais les améliorations de l'algorithme de construction dans 0.6.1.32 devraient le ramener à environ 0,2
  au fur et à mesure que le réseau se met à niveau. Disons 0,5 maintenant avec la moitié du réseau à .30 ou antérieur.

```
recvKBps = 700 * (0.5 + 1) * (1 + 0.33) * (1 + 0.5) * 4KB / 10m
         ~= 28KBps
```
Ceci ne concerne que les magasins - qu'en est-il des requêtes ?

### Le retour de l'algorithme Kademlia ?

*(Adapté de la réunion I2P du 2 janvier 2007)*

La netDb Kademlia ne fonctionnait tout simplement pas correctement. Est-elle morte pour toujours ou va-t-elle revenir ? Si elle revient, les pairs dans la netDb Kademlia seraient un sous-ensemble très limité des routeurs du réseau (essentiellement un nombre élargi de pairs floodfill, si/quand les pairs floodfill ne peuvent pas gérer la charge). Mais tant que les pairs floodfill peuvent gérer la charge (et que d'autres pairs qui le peuvent ne peuvent pas être ajoutés), c'est inutile.

### L'avenir des Floodfill

*(Adapté d'une conversation IRC avec jrandom 11/07)*

Voici une proposition : La classe de capacité O est automatiquement floodfill. Hmm. À moins d'être sûrs, nous pourrions finir avec une façon élégante de faire du DDoS sur tous les routeurs de classe O. C'est tout à fait le cas : nous voulons nous assurer que le nombre de floodfill soit aussi petit que possible tout en fournissant une accessibilité suffisante. Si/quand les requêtes netDb échouent, alors nous devons augmenter le nombre de pairs floodfill, mais pour le moment, je ne suis pas au courant d'un problème de récupération netDb. Il y a 33 pairs de classe "O" selon mes données. 33, c'est /beaucoup/ pour faire du floodfill.

Donc floodfill fonctionne mieux quand le nombre de pairs dans ce pool est fermement limité ? Et la taille du pool floodfill ne devrait pas beaucoup grandir, même si le réseau lui-même grandirait graduellement ? 3-5 pairs floodfill peuvent gérer 10K routers si je me souviens bien (j'ai posté plein de chiffres là-dessus expliquant les détails dans l'ancien syndie). Ça semble être une exigence difficile à remplir avec une participation automatique, surtout si les nœuds qui participent ne peuvent pas faire confiance aux données des autres. par ex. "voyons si je suis parmi le top 5", et ne peuvent faire confiance qu'aux données les concernant (par ex. "Je suis définitivement classe O, et je transfère 150 KB/s, et je suis en ligne depuis 123 jours"). Et le top 5 est hostile aussi. En gros, c'est la même chose que les serveurs d'annuaire tor - choisis par des personnes de confiance (aka les devs). Ouais, en ce moment ça pourrait être exploité par la participation automatique, mais ce serait trivial à détecter et traiter. Il semble qu'au final, nous pourrions avoir besoin de quelque chose de plus utile que Kademlia, et n'avoir que des pairs raisonnablement capables rejoindre ce schéma. La classe N et au-dessus devrait être une quantité assez importante pour supprimer le risque qu'un adversaire cause un déni de service, j'espère. Mais ça devrait être différent de floodfill alors, dans le sens où ça ne causerait pas un trafic énorme. Grande quantité ? Pour un netDb basé sur DHT ? Pas nécessairement basé sur DHT.

### Liste TODO Floodfill {#todo}

NOTE : Les informations suivantes ne sont pas à jour. Consultez [la page principale netDb](/docs/overview/network-database) pour le statut actuel et une liste des travaux futurs.

Le réseau n'avait plus qu'un seul floodfill pendant quelques heures le 13 mars 2008 (environ 18h00 - 20h00 UTC), et cela a causé beaucoup de problèmes.

Deux modifications implémentées dans la version 0.6.1.33 devraient réduire les perturbations causées par la suppression ou le renouvellement des pairs floodfill :

1. Randomiser les pairs floodfill utilisés pour la recherche à chaque fois.
   Cela vous permettra de contourner ceux qui échouent au final.
   Cette modification corrige également un bug vicieux qui rendait parfois fou le code de recherche ff.
2. Privilégier les pairs floodfill qui sont actifs.
   Le code évite maintenant les pairs qui sont sur liste noire, défaillants, ou dont on n'a pas eu de nouvelles depuis
   une demi-heure, si possible.

Un avantage est un premier contact plus rapide vers un site I2P (c'est-à-dire quand vous devez d'abord récupérer le leaseset). Le délai d'expiration de recherche est de 10s, donc si vous ne commencez pas par interroger un pair qui est hors service, vous pouvez économiser 10s.

Il *pourrait* y avoir des implications d'anonymat dans ces changements. Par exemple, dans le code de **stockage** floodfill, il y a des commentaires indiquant que les pairs shitlistés ne sont pas évités, car un pair pourrait être "pourri" et ensuite voir ce qui se passe. Les recherches sont beaucoup moins vulnérables que les stockages - elles sont beaucoup moins fréquentes et révèlent moins d'informations. Alors peut-être qu'on ne pense pas avoir besoin de s'en inquiéter ? Mais si on veut ajuster les changements, il serait facile d'envoyer vers un pair listé comme "hors ligne" ou shitlisté de toute façon, juste ne pas le compter dans les 2 auxquels on envoie (puisqu'on ne s'attend pas vraiment à une réponse).

Il y a plusieurs endroits où un pair floodfill est sélectionné - cette correction ne concerne qu'un seul cas - celui où un pair régulier effectue des recherches [2 à la fois]. Autres endroits où une meilleure sélection floodfill devrait être implémentée :

1. À qui un pair régulier stocke [1 à la fois]
   (aléatoire - besoin d'ajouter une qualification, car les délais d'attente sont longs)
2. À qui un pair régulier effectue des recherches pour vérifier un stockage [1 à la fois]
   (aléatoire - besoin d'ajouter une qualification, car les délais d'attente sont longs)
3. À qui un pair floodfill envoie en réponse à une recherche échouée (3 les plus proches de la recherche)
4. À qui un pair floodfill diffuse (tous les autres pairs floodfill)
5. La liste des pairs floodfill envoyée dans le "chuchotement" NTCP toutes les 6 heures
   (bien que cela ne soit peut-être plus nécessaire grâce à d'autres améliorations floodfill)

Beaucoup plus pourrait et devrait être fait :

- Utiliser les statistiques "dbHistory" pour mieux évaluer l'intégration d'un pair floodfill
- Utiliser les statistiques "dbHistory" pour réagir immédiatement aux pairs floodfill qui ne répondent pas
- Être plus intelligent sur les nouvelles tentatives - les nouvelles tentatives sont gérées par une couche supérieure, pas dans
  FloodOnlySearchJob, donc elle fait un autre tri aléatoire et essaie à nouveau,
  plutôt que d'ignorer délibérément les pairs ff que nous venons d'essayer.
- Améliorer davantage les statistiques d'intégration
- Utiliser réellement les statistiques d'intégration plutôt que juste l'indication floodfill dans netDb
- Utiliser aussi les statistiques de latence ?
- Plus d'amélioration sur la reconnaissance des pairs floodfill défaillants

Récemment terminé :

- [Dans la version 0.6.3]
  Implémenter l'adhésion automatique
  au floodfill pour un certain pourcentage de pairs de classe O, basé sur l'analyse du réseau.
- [Dans la version 0.6.3]
  Continuer à réduire la taille des entrées netDb pour réduire le trafic floodfill -
  nous sommes maintenant au nombre minimum de statistiques requises pour surveiller le réseau.
- [Dans la version 0.6.3]
  Liste manuelle des pairs floodfill à exclure
  ([listes de blocage](/docs/overview/threat-model#blocklist) par identité de router)
- [Dans la version 0.6.3]
  Meilleure sélection des pairs floodfill pour le stockage :
  Éviter les pairs dont la netDb est ancienne, ou qui ont un stockage récemment échoué,
  ou qui sont mis sur liste noire de façon permanente.
- [Dans la version 0.6.4]
  Préférer les pairs floodfill déjà connectés pour le stockage des RouterInfo, pour
  réduire le nombre de connexions directes aux pairs floodfill.
- [Dans la version 0.6.5]
  Les pairs qui ne sont plus floodfill envoient leur routerInfo en réponse
  à une requête, afin que le router qui fait la requête sache qu'il
  n'est plus floodfill.
- [Dans la version 0.6.5]
  Ajustement supplémentaire des exigences pour devenir automatiquement floodfill
- [Dans la version 0.6.5]
  Corriger le profilage du temps de réponse en préparation pour favoriser les floodfills rapides
- [Dans la version 0.6.5]
  Améliorer la mise sur liste de blocage
- [Dans la version 0.7]
  Corriger l'exploration netDb
- [Dans la version 0.7]
  Activer la mise sur liste de blocage par défaut, bloquer les fauteurs de troubles connus
- [Plusieurs améliorations dans les versions récentes, un effort continu]
  Réduire les demandes de ressources sur les routers haute bande passante et floodfill

C'est une longue liste mais il faudra autant de travail pour avoir un réseau qui résiste aux attaques DOS provenant de nombreux pairs qui activent et désactivent l'option floodfill. Ou qui prétendent être un routeur floodfill. Rien de tout cela n'était un problème quand nous n'avions que deux routeurs ff, et qu'ils étaient tous les deux en ligne 24h/24 et 7j/7. Encore une fois, l'absence de jrandom nous a montré des endroits qui nécessitent des améliorations.

Pour aider dans cet effort, des données de profil supplémentaires pour les pairs floodfill sont maintenant (depuis la version 0.6.1.33) affichées sur la page "Profiles" dans la console du router. Nous utiliserons ces données pour analyser quelles informations sont appropriées pour évaluer les pairs floodfill.

Le réseau est actuellement assez résilient, cependant nous continuerons d'améliorer nos algorithmes pour mesurer et réagir aux performances et à la fiabilité des pairs floodfill. Bien que nous ne soyons pas, pour le moment, entièrement protégés contre les menaces potentielles de floodfills malveillants ou d'un DDOS de floodfill, la majeure partie de l'infrastructure est en place, et nous sommes bien positionnés pour réagir rapidement si le besoin s'en faisait sentir.
