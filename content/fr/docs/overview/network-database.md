---
title: "La base de données réseau"
description: "Comprendre la base de données réseau distribuée d'I2P (netDb) - une DHT spécialisée pour les informations de contact des routeurs et la recherche de destinations"
slug: "network-database"
aliases:
  - "/fr/how_networkdatabase"
  - "/fr/how_networkdatabase/"
lastUpdated: "2025-03"
accurateFor: "0.9.65"
---

## Aperçu

La netDb d'I2P est une base de données distribuée spécialisée, contenant seulement deux types de données - les informations de contact des routeurs (**RouterInfos**) et les informations de contact des destinations (**LeaseSets**). Chaque élément de données est signé par la partie appropriée et vérifié par quiconque l'utilise ou le stocke. De plus, les données contiennent des informations de vivacité, permettant d'abandonner les entrées non pertinentes, aux nouvelles entrées de remplacer les anciennes, et offrant une protection contre certaines classes d'attaques.

La netDb est distribuée avec une technique simple appelée "floodfill", où un sous-ensemble de tous les routers, appelés "floodfill routers", maintient la base de données distribuée.

---

## RouterInfo

Lorsqu'un router I2P veut contacter un autre router, il doit connaître certaines données clés - toutes regroupées et signées par le router dans une structure appelée "RouterInfo", qui est distribuée avec le SHA256 de l'identité du router comme clé. La structure elle-même contient :

- L'identité du router (une clé de chiffrement, une clé de signature, et un certificat)
- Les adresses de contact auxquelles il peut être joint
- Quand ceci a été publié
- Un ensemble d'options texte arbitraires
- La signature de ce qui précède, générée par la clé de signature de l'identité

### Options attendues

Les options de texte suivantes, bien que non strictement requises, sont censées être présentes :

- **caps** (Indicateurs de capacités - utilisés pour indiquer la participation floodfill, la bande passante approximative et l'accessibilité perçue)
  - **D**: Congestion moyenne (depuis la version 0.9.58)
  - **E**: Congestion élevée (depuis la version 0.9.58)
  - **f**: Floodfill
  - **G**: Rejette tous les tunnels (depuis la version 0.9.58)
  - **H**: Caché
  - **K**: Moins de 12 KBps de bande passante partagée
  - **L**: 12 - 48 KBps de bande passante partagée (par défaut)
  - **M**: 48 - 64 KBps de bande passante partagée
  - **N**: 64 - 128 KBps de bande passante partagée
  - **O**: 128 - 256 KBps de bande passante partagée
  - **P**: 256 - 2000 KBps de bande passante partagée (depuis la version 0.9.20, voir note ci-dessous)
  - **R**: Accessible
  - **U**: Inaccessible
  - **X**: Plus de 2000 KBps de bande passante partagée (depuis la version 0.9.20, voir note ci-dessous)

"Bande passante partagée" == (pourcentage de partage %) * min(bande passante entrante, bande passante sortante)

Pour la compatibilité avec les routers plus anciens, un router peut publier plusieurs lettres de bande passante, par exemple "PO".

Note : la limite entre les classes de bande passante P et X peut être soit 2000 soit 2048 KBps, au choix de l'implémenteur.

- **netId** = 2 (Compatibilité réseau de base - Un router refusera de communiquer avec un pair ayant un netId différent)
- **router.version** (Utilisé pour déterminer la compatibilité avec les nouvelles fonctionnalités et messages)

Notes sur les capacités R/U : Un router devrait généralement publier la capacité R ou U, sauf si l'état de joignabilité est actuellement inconnu. R signifie que le router est directement joignable (aucun introducers requis, pas de pare-feu) sur au moins une adresse de transport. U signifie que le router n'est PAS directement joignable sur AUCUNE adresse de transport.

Options dépréciées : - ~~coreVersion~~ (Jamais utilisé, supprimé dans la version 0.9.24) - ~~stat_uptime~~ = 90m (Inutilisé depuis la version 0.7.9, supprimé dans la version 0.9.24)

Ces valeurs sont utilisées par d'autres routers pour des décisions de base. Devons-nous nous connecter à ce router ? Devons-nous tenter de router un tunnel à travers ce router ? Le flag de capacité de bande passante, en particulier, est utilisé uniquement pour déterminer si le router atteint un seuil minimum pour router des tunnels. Au-dessus du seuil minimum, la bande passante annoncée n'est ni utilisée ni fiable nulle part dans le router, sauf pour l'affichage dans l'interface utilisateur et pour le débogage et l'analyse réseau.

Numéros NetID valides :

| Utilisation | Numéro NetID |
|-------------|--------------|
| Réservé | 0 |
| Réservé | 1 |
| Réseau Actuel (par défaut) | 2 |
| Réseaux Futurs Réservés | 3 - 15 |
| Forks et Réseaux de Test | 16 - 254 |
| Réservé | 255 |
### Options supplémentaires

Les options de texte supplémentaires incluent un petit nombre de statistiques sur la santé du router, qui sont agrégées par des sites tels que [stats.i2p](http://stats.i2p/) pour l'analyse des performances réseau et le débogage. Ces statistiques ont été choisies pour fournir des données cruciales aux développeurs, telles que les taux de succès de construction de tunnel, tout en équilibrant le besoin de ces données avec les effets secondaires qui pourraient résulter de la révélation de ces données. Les statistiques actuelles se limitent à :

- Taux de succès, de rejet et de timeout de construction de tunnel exploratoire
- Nombre moyen sur 1 heure de tunnels participants

Ces éléments sont optionnels, mais s'ils sont inclus, ils aident à l'analyse des performances à l'échelle du réseau. Depuis l'API 0.9.58, ces statistiques sont simplifiées et standardisées, comme suit :

- Les clés d'option sont stat_(nomstat).(périodestat)
- Les valeurs d'option sont séparées par ';'
- Les statistiques pour les compteurs d'événements ou les pourcentages normalisés utilisent la 4ème valeur ; les trois premières valeurs ne sont pas utilisées mais doivent être présentes
- Les statistiques pour les valeurs moyennes utilisent la 1ère valeur, et aucun séparateur ';' n'est requis
- Pour une pondération égale de tous les routers dans l'analyse des statistiques, et pour un anonymat supplémentaire, les routers ne devraient inclure ces statistiques qu'après un temps de fonctionnement d'une heure ou plus, et seulement une fois toutes les 16 fois que le RI est publié.

Exemple :

```
stat_tunnel.buildExploratoryExpire.60m = 0;0;0;53.14
stat_tunnel.buildExploratoryReject.60m = 0;0;0;15.51
stat_tunnel.buildExploratorySuccess.60m = 0;0;0;31.35
stat_tunnel.participatingTunnels.60m = 289.20
```
Les routeurs floodfill peuvent publier des données supplémentaires sur le nombre d'entrées dans leur base de données réseau. Ces données sont optionnelles, mais si elles sont incluses, elles aident à l'analyse des performances à l'échelle du réseau.

Les deux options suivantes doivent être incluses par les routeurs floodfill dans chaque RI publié :

- **netdb.knownLeaseSets**
- **netdb.knownRouters**

Exemple :

```
netdb.knownLeaseSets = 158
netdb.knownRouters = 11374
```
Les données publiées peuvent être consultées dans l'interface utilisateur du router, mais ne sont pas utilisées ou considérées comme fiables par aucun autre router.

### Options de famille

À partir de la version 0.9.24, les routers peuvent déclarer qu'ils font partie d'une "famille", exploitée par la même entité. Plusieurs routers de la même famille ne seront pas utilisés dans un seul tunnel.

Les options de famille sont :

- **family** (Le nom de famille)
- **family.key** Le code de type de signature de la [Clé Publique de Signature](/docs/specs/common-structures/#type_SigningPublicKey) de la famille (en chiffres ASCII) concaténé avec ':' concaténé avec la Clé Publique de Signature en base 64
- **family.sig** La signature de ((nom de famille en UTF-8) concaténé avec (hash de router de 32 octets)) en base 64

### Expiration des RouterInfo

Les RouterInfos n'ont pas de temps d'expiration défini. Chaque router est libre de maintenir sa propre politique locale pour équilibrer la fréquence des recherches de RouterInfo avec l'utilisation de la mémoire ou du disque. Dans l'implémentation actuelle, il existe les politiques générales suivantes :

- Il n'y a pas d'expiration pendant la première heure de fonctionnement, car les données stockées de manière persistante peuvent être anciennes.
- Il n'y a pas d'expiration s'il y a 25 RouterInfos ou moins.
- À mesure que le nombre de RouterInfos locaux augmente, le délai d'expiration diminue, dans une tentative de maintenir un nombre raisonnable de RouterInfos. Le délai d'expiration avec moins de 120 routeurs est de 72 heures, tandis que le délai d'expiration avec 300 routeurs est d'environ 30 heures.
- Les RouterInfos contenant des introducteurs [SSU](/docs/legacy/ssu/) expirent en environ une heure, car la liste des introducteurs expire dans ce délai.
- Les floodfills utilisent un délai d'expiration court (1 heure) pour tous les RouterInfos locaux, car les RouterInfos valides leur seront fréquemment republiés.

### Stockage persistant des RouterInfo

Les RouterInfos sont périodiquement écrites sur le disque afin qu'elles soient disponibles après un redémarrage.

Il peut être souhaitable de stocker de manière persistante les Meta LeaseSets avec de longues expirations. Ceci dépend de l'implémentation.

### Voir Aussi

- [Spécification RouterInfo](/docs/specs/common-structures/#struct_RouterInfo)
- [Javadoc RouterInfo](http://idk.i2p/javadoc-i2p/net/i2p/data/router/RouterInfo.html)

---

## LeaseSet

Le deuxième type de données distribué dans le netDb est un "leaseSet" - documentant un groupe de **points d'entrée de tunnel (leases)** pour une destination client particulière. Chacun de ces leases spécifie les informations suivantes :

- Le router de passerelle du tunnel (en spécifiant son identité)
- L'ID du tunnel sur ce router pour envoyer les messages (un nombre de 4 octets)
- Quand ce tunnel expirera.

Le leaseSet lui-même est stocké dans la netDb sous la clé dérivée du SHA256 de la destination. Une exception existe pour les Encrypted LeaseSets (LS2), à partir de la version 0.9.38. Le SHA256 de l'octet de type (3) suivi de la clé publique aveuglée est utilisé pour la clé DHT, puis fait l'objet d'une rotation comme d'habitude. Voir la section Métrique de proximité Kademlia ci-dessous.

En plus de ces baux, le LeaseSet inclut :

- La destination elle-même (une clé de chiffrement, une clé de signature et un certificat)
- Clé publique de chiffrement supplémentaire : utilisée pour le chiffrement de bout en bout des messages garlic
- Clé publique de signature supplémentaire : prévue pour la révocation du leaseSet, mais actuellement inutilisée.
- Signature de toutes les données du leaseSet, pour s'assurer que la destination a publié le leaseSet.

- [Spécification Lease](/docs/specs/common-structures/#struct_Lease)
- [Spécification LeaseSet](/docs/specs/common-structures/#struct_LeaseSet)
- [Javadoc Lease](http://idk.i2p/javadoc-i2p/net/i2p/data/Lease.html)
- [Javadoc LeaseSet](http://idk.i2p/javadoc-i2p/net/i2p/data/LeaseSet.html)

À partir de la version 0.9.38, trois nouveaux types de LeaseSets sont définis ; LeaseSet2, MetaLeaseSet, et EncryptedLeaseSet. Voir ci-dessous.

### LeaseSets non publiés

Un leaseSet pour une destination utilisée uniquement pour les connexions sortantes est *non publié*. Il n'est jamais envoyé pour publication vers un router floodfill. Les tunnels "Client", tels que ceux pour la navigation web et les clients IRC, sont non publiés. Les serveurs pourront toujours renvoyer des messages vers ces destinations non publiées, grâce aux [messages de stockage I2NP](#leaseset-storage-to-peers).

### LeaseSets révoqués

Un LeaseSet peut être *révoqué* en publiant un nouveau LeaseSet avec zéro lease. Les révocations doivent être signées par la clé de signature additionnelle dans le LeaseSet. Les révocations ne sont pas entièrement implémentées, et il n'est pas certain qu'elles aient une utilité pratique. C'est la seule utilisation prévue pour cette clé de signature, elle n'est donc actuellement pas utilisée.

### LeaseSet2 (LS2)

À partir de la version 0.9.38, les floodfills prennent en charge une nouvelle structure LeaseSet2. Cette structure est très similaire à l'ancienne structure LeaseSet et remplit le même objectif. La nouvelle structure offre la flexibilité nécessaire pour prendre en charge de nouveaux types de chiffrement, plusieurs types de chiffrement, des options, des clés de signature hors ligne et d'autres fonctionnalités. Voir la proposition 123 pour plus de détails.

### Meta LeaseSet (LS2)

Depuis la version 0.9.38, les floodfills prennent en charge une nouvelle structure Meta LeaseSet. Cette structure fournit une structure arborescente dans la DHT, pour référencer d'autres LeaseSets. En utilisant les Meta LeaseSets, un site peut implémenter de grands services multi-hébergés, où plusieurs Destinations différentes sont utilisées pour fournir un service commun. Les entrées dans un Meta LeaseSet sont des Destinations ou d'autres Meta LeaseSets, et peuvent avoir de longues expirations, jusqu'à 18,2 heures. En utilisant cette fonctionnalité, il devrait être possible d'exécuter des centaines ou des milliers de Destinations hébergeant un service commun. Voir la proposition 123 pour plus de détails.

### LeaseSets chiffrés (LS1)

Cette section décrit l'ancienne méthode non sécurisée de chiffrement des LeaseSets utilisant une clé symétrique fixe. Voir ci-dessous pour la version LS2 des LeaseSets chiffrés.

Dans un LeaseSet *chiffré*, tous les Leases sont chiffrés avec une clé séparée. Les leases ne peuvent être décodés, et donc la destination ne peut être contactée, que par ceux qui possèdent la clé. Il n'y a aucun indicateur ou autre indication directe que le LeaseSet est chiffré. Les LeaseSets chiffrés ne sont pas largement utilisés, et c'est un sujet de travail futur de rechercher si l'interface utilisateur et l'implémentation des LeaseSets chiffrés pourraient être améliorées.

### LeaseSets chiffrés (LS2)

À partir de la version 0.9.38, les floodfills prennent en charge une nouvelle structure EncryptedLeaseSet. La Destination est masquée, et seule une clé publique aveuglée et une date d'expiration sont visibles pour le floodfill. Seuls ceux qui possèdent la Destination complète peuvent déchiffrer la structure. La structure est stockée à un emplacement DHT basé sur le hachage de la clé publique aveuglée, et non sur le hachage de la Destination. Voir la proposition 123 pour plus de détails.

### Expiration des LeaseSet

Pour les LeaseSets classiques, l'expiration correspond à l'heure d'expiration la plus tardive de ses leases. Pour les nouvelles structures de données LeaseSet2, l'expiration est spécifiée dans l'en-tête. Pour LeaseSet2, l'expiration devrait correspondre à l'expiration la plus tardive de ses leases. Pour EncryptedLeaseSet et MetaLeaseSet, l'expiration peut varier, et une expiration maximale peut être appliquée, ceci reste à déterminer.

### Stockage Persistant des LeaseSet

Aucun stockage persistant des données de leaseSet n'est requis, car elles expirent si rapidement. Cependant, le stockage persistant des données d'EncryptedLeaseSet et de MetaLeaseSet avec de longues expirations peut être recommandé.

### Sélection de Clé de Chiffrement (LS2)

LeaseSet2 peut contenir plusieurs clés de chiffrement. Les clés sont classées par ordre de préférence du serveur, la plus préférée en premier. Le comportement client par défaut est de sélectionner la première clé avec un type de chiffrement pris en charge. Les clients peuvent utiliser d'autres algorithmes de sélection basés sur la prise en charge du chiffrement, les performances relatives et d'autres facteurs.

---

## Amorçage

La netDb est décentralisée, cependant vous avez besoin d'au moins une référence à un pair pour que le processus d'intégration vous connecte. Ceci est accompli en "resemant" votre router avec le RouterInfo d'un pair actif - spécifiquement, en récupérant leur fichier `routerInfo-$hash.dat` et en le stockant dans votre répertoire `netDb/`. N'importe qui peut vous fournir ces fichiers - vous pouvez même les fournir à d'autres en exposant votre propre répertoire netDb. Pour simplifier le processus, des volontaires publient leurs répertoires netDb (ou un sous-ensemble) sur le réseau ordinaire (non-i2p), et les URLs de ces répertoires sont codées en dur dans I2P. Quand le router démarre pour la première fois, il récupère automatiquement depuis l'une de ces URLs, sélectionnée au hasard.

---

## Floodfill

La floodfill netDb est un mécanisme de stockage distribué simple. L'algorithme de stockage est simple : envoyer les données au pair le plus proche qui s'est annoncé comme un floodfill router. Lorsque le pair dans la floodfill netDb reçoit un stockage netDb d'un pair qui n'est pas dans la floodfill netDb, il l'envoie à un sous-ensemble des pairs de la floodfill netDb. Les pairs sélectionnés sont ceux les plus proches (selon la [métrique XOR](#kademlia-closeness-metric)) d'une clé spécifique.

Déterminer qui fait partie du netDb floodfill est trivial - cela est exposé dans le routerInfo publié de chaque router en tant que capacité.

Les floodfills n'ont pas d'autorité centrale et ne forment pas de "consensus" - ils implémentent seulement une superposition DHT simple.

### Participation volontaire au router floodfill

Contrairement à Tor, où les serveurs d'annuaire sont codés en dur et de confiance, et exploités par des entités connues, les membres de l'ensemble de pairs floodfill d'I2P n'ont pas besoin d'être de confiance et changent au fil du temps.

Pour augmenter la fiabilité de la netDb et minimiser l'impact du trafic netDb sur un router, le floodfill n'est activé automatiquement que sur les routers configurés avec des limites de bande passante élevées. Les routers avec des limites de bande passante élevées (qui doivent être configurés manuellement, car la valeur par défaut est beaucoup plus faible) sont présumés être sur des connexions à faible latence et sont plus susceptibles d'être disponibles 24h/24 et 7j/7. La bande passante de partage minimale actuelle pour un router floodfill est de 128 Ko/sec.

De plus, un router doit réussir plusieurs tests supplémentaires de santé (temps de file d'attente des messages sortants, retard des tâches, etc.) avant que l'opération floodfill ne soit automatiquement activée.

Avec les règles actuelles pour l'adhésion automatique, environ 6% des routeurs du réseau sont des routeurs floodfill.

Alors que certains pairs sont configurés manuellement pour être floodfill, d'autres sont simplement des routers à haute bande passante qui se portent automatiquement volontaires lorsque le nombre de pairs floodfill tombe en dessous d'un seuil. Cela empêche tout dommage réseau à long terme causé par la perte de la plupart ou de tous les floodfills lors d'une attaque. À leur tour, ces pairs se désactiveront du mode floodfill lorsqu'il y aura trop de floodfills en service.

### Rôles des routeurs floodfill

Les seuls services d'un router floodfill qui s'ajoutent à ceux des routers non-floodfill sont l'acceptation des stockages netDb et la réponse aux requêtes netDb. Étant donné qu'ils disposent généralement d'une bande passante élevée, ils sont plus susceptibles de participer à un grand nombre de tunnels (c'est-à-dire servir de « relais » pour d'autres), mais cela n'est pas directement lié à leurs services de base de données distribuée.

---

## Métrique de proximité Kademlia

Le netDb utilise une métrique XOR simple de style Kademlia pour déterminer la proximité. Pour créer une clé Kademlia, le hachage SHA256 de la RouterIdentity ou Destination est calculé. Une exception concerne les Encrypted LeaseSets (LS2), depuis la version 0.9.38. Le SHA256 de l'octet de type (3) suivi de la clé publique aveuglée est utilisé pour la clé DHT, puis fait l'objet d'une rotation comme d'habitude.

Une modification de cet algorithme est effectuée pour augmenter les coûts des [attaques Sybil](#sybil-attack-partial-keyspace). Au lieu du hash SHA256 de la clé recherchée ou stockée, le hash SHA256 est calculé sur la clé de recherche binaire de 32 octets concaténée avec la date UTC représentée sous forme de chaîne ASCII de 8 octets yyyyMMdd, c'est-à-dire SHA256(key + yyyyMMdd). Ceci s'appelle la "clé de routage", et elle change chaque jour à minuit UTC. Seule la clé de recherche est modifiée de cette manière, pas les hashes des router floodfill. La transformation quotidienne de la DHT est parfois appelée "rotation d'espace de clés", bien qu'il ne s'agisse pas strictement d'une rotation.

Les clés de routage ne sont jamais envoyées sur le réseau dans aucun message I2NP, elles sont uniquement utilisées localement pour déterminer la distance.

---

## Segmentation de la base de données réseau - Sous-bases de données

Traditionnellement, les DHT de style Kademlia ne se préoccupent pas de préserver la non-associabilité des informations stockées sur un nœud particulier de la DHT. Par exemple, une information peut être stockée sur un nœud de la DHT, puis récupérée de ce nœud de manière inconditionnelle. Dans I2P et avec la netDb, ce n'est pas le cas, les informations stockées dans la DHT ne peuvent être partagées que dans certaines circonstances connues où il est "sûr" de le faire. Ceci permet d'éviter une classe d'attaques où un acteur malveillant peut essayer d'associer un tunnel client avec un router en envoyant un stockage vers un tunnel client, puis en le récupérant directement depuis l'« Hôte » suspecté du tunnel client.

### Structure de segmentation

Les routers I2P peuvent implémenter des défenses efficaces contre cette classe d'attaque à condition que quelques conditions soient remplies. Une implémentation de base de données réseau devrait être capable de suivre si une entrée de base de données a été reçue via un tunnel client ou directement. Si elle a été reçue via un tunnel client, alors elle devrait également suivre par quel tunnel client elle a été reçue, en utilisant la destination locale du client. Si l'entrée a été reçue via plusieurs tunnels clients, alors la netDb devrait suivre toutes les destinations où l'entrée a été observée. Elle devrait également suivre si une entrée a été reçue comme réponse à une recherche, ou comme un stockage.

Dans les implémentations Java et C++, ceci est réalisé en utilisant d'abord une seule netDb "Principale" pour les recherches directes et les opérations floodfill. Cette netDb principale existe dans le contexte du router. Ensuite, chaque client reçoit sa propre version de la netDb, qui est utilisée pour capturer les entrées de base de données envoyées aux tunnels client et répondre aux recherches envoyées via les tunnels client. Nous appelons ces "Bases de Données Réseau Client" ou "Sous-Bases de Données" et elles existent dans le contexte client. La netDb exploitée par le client existe uniquement pendant la durée de vie du client et contient seulement les entrées qui communiquent avec les tunnels du client. Cela rend impossible le chevauchement entre les entrées envoyées via les tunnels client et les entrées envoyées directement au router.

De plus, chaque netDb doit être capable de se souvenir si une entrée de base de données a été reçue parce qu'elle a été envoyée vers l'une de nos destinations, ou parce qu'elle a été demandée par nous dans le cadre d'une recherche. Si une entrée de base de données a été reçue comme un stockage, c'est-à-dire qu'un autre router nous l'a envoyée, alors un netDb devrait répondre aux demandes pour cette entrée quand un autre router recherche la clé. Cependant, si elle a été reçue comme réponse à une requête, alors le netDb ne devrait répondre à une requête pour cette entrée que si l'entrée avait déjà été stockée vers la même destination. Un client ne devrait jamais répondre aux requêtes avec une entrée du netDb principal, seulement avec sa propre base de données réseau client.

Ces stratégies doivent être adoptées et utilisées de manière combinée pour que les deux soient appliquées. En combinaison, elles "segmentent" la netDb et la sécurisent contre les attaques.

---

## Mécanismes de Stockage, Vérification et Recherche

### Stockage des RouterInfo vers les pairs

Les [I2NP](/docs/specs/i2np/) DatabaseStoreMessages contenant le RouterInfo local sont échangés avec les pairs dans le cadre de l'initialisation d'une connexion de transport [NTCP](/docs/specs/ntcp2/) ou [SSU](/docs/specs/ssu2/).

### Stockage des LeaseSet vers les pairs

Les [I2NP](/docs/specs/i2np/) DatabaseStoreMessages contenant le leaseSet local sont périodiquement échangés avec les pairs en les regroupant dans un message garlic avec le trafic normal de la destination associée. Cela permet d'envoyer une réponse initiale, et des réponses ultérieures, vers un lease approprié, sans nécessiter de recherches de leaseSet, ou exiger que les destinations communicantes aient publié des leaseSets.

### Sélection des Floodfill

Le DatabaseStoreMessage doit être envoyé au floodfill qui est le plus proche de la clé de routage actuelle pour le RouterInfo ou LeaseSet en cours de stockage. Actuellement, le floodfill le plus proche est trouvé par une recherche dans la base de données locale. Même si ce floodfill n'est pas réellement le plus proche, il le fera "remonter" plus près en l'envoyant à plusieurs autres floodfills. Cela fournit un haut degré de tolérance aux pannes.

Dans le Kademlia traditionnel, un pair effectuerait une recherche "find-closest" avant d'insérer un élément dans la DHT vers la cible la plus proche. Comme l'opération de vérification aura tendance à découvrir des floodfills plus proches s'ils sont présents, un router améliorera rapidement sa connaissance du "voisinage" DHT pour les RouterInfo et LeaseSets qu'il publie régulièrement. Bien qu'I2NP ne définisse pas de message "find-closest", si cela devient nécessaire, un router peut simplement effectuer une recherche itérative pour une clé avec le bit le moins significatif inversé (c'est-à-dire key ^ 0x01) jusqu'à ce qu'aucun pair plus proche ne soit reçu dans les DatabaseSearchReplyMessages. Cela garantit que le vrai pair le plus proche sera trouvé même si un pair plus distant avait l'élément netdb.

### Stockage des RouterInfo vers les Floodfills

Un router publie son propre RouterInfo en se connectant directement à un router floodfill et en lui envoyant un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage avec un Reply Token non nul. Le message n'est pas chiffré de bout en bout par garlic encryption, car il s'agit d'une connexion directe, donc il n'y a pas de routers intermédiaires (et aucun besoin de cacher ces données de toute façon). Le router floodfill répond avec un [I2NP](/docs/specs/i2np/) DeliveryStatusMessage, avec l'ID du message défini à la valeur du Reply Token.

Dans certaines circonstances, un router peut également envoyer le RouterInfo DatabaseStoreMessage via un tunnel exploratoire ; par exemple, en raison de limites de connexion, d'incompatibilité de connexion, ou d'un désir de cacher l'IP réelle au floodfill. Le floodfill peut ne pas accepter un tel stockage en cas de surcharge ou selon d'autres critères ; la question de savoir s'il faut déclarer explicitement illégal le stockage non-direct d'un RouterInfo est un sujet d'étude future.

### Stockage des leaseSet vers les floodfills

Le stockage des leaseSets est beaucoup plus sensible que celui des RouterInfos, car un router doit veiller à ce que le leaseSet ne puisse pas être associé au router.

Un router publie un LeaseSet local en envoyant un DatabaseStoreMessage [I2NP](/docs/specs/i2np/) avec un Reply Token non nul via un tunnel client sortant pour cette Destination. Le message est chiffré de bout en bout avec garlic encryption en utilisant le Session Key Manager de la Destination, afin de masquer le message au point de sortie du tunnel. Le router floodfill répond avec un DeliveryStatusMessage [I2NP](/docs/specs/i2np/), avec le Message ID défini sur la valeur du Reply Token. Ce message est renvoyé vers l'un des tunnels entrants du client.

### Flooding

Comme tout router, un floodfill utilise divers critères pour valider le leaseSet ou RouterInfo avant de le stocker localement. Ces critères peuvent être adaptatifs et dépendants des conditions actuelles, notamment la charge actuelle, la taille de la netDb, et d'autres facteurs. Toute validation doit être effectuée avant la diffusion.

Après qu'un router floodfill reçoit un DatabaseStoreMessage contenant un RouterInfo ou LeaseSet valide qui est plus récent que celui précédemment stocké dans sa NetDb locale, il le "flood". Pour flooder une entrée NetDb, il recherche plusieurs (actuellement 3) routers floodfill les plus proches de la clé de routage de l'entrée NetDb. (La clé de routage est le hash SHA256 de la RouterIdentity ou Destination avec la date (aaaammjj) ajoutée.) En floodant vers ceux les plus proches de la clé, et non les plus proches de lui-même, le floodfill s'assure que le stockage arrive au bon endroit, même si le router de stockage n'avait pas une bonne connaissance du "voisinage" DHT pour la clé de routage.

Le floodfill se connecte alors directement à chacun de ces pairs et lui envoie un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage avec un Reply Token à zéro. Le message n'est pas chiffré garlic de bout en bout, car il s'agit d'une connexion directe, donc il n'y a pas de routers intermédiaires (et aucun besoin de cacher ces données de toute façon). Les autres routers ne répondent pas et ne re-diffusent pas, car le Reply Token est à zéro.

Les floodfills ne doivent pas inonder via les tunnels ; le DatabaseStoreMessage doit être envoyé via une connexion directe.

Les floodfills ne doivent jamais diffuser un leaseSet expiré ou un RouterInfo publié il y a plus d'une heure.

### Recherche de RouterInfo et LeaseSet

Le [I2NP](/docs/specs/i2np/) DatabaseLookupMessage est utilisé pour demander une entrée netDb à un router floodfill. Les recherches sont envoyées par l'un des tunnels exploratoires sortants du router. Les réponses sont spécifiées pour revenir via l'un des tunnels exploratoires entrants du router.

Les recherches sont généralement envoyées en parallèle aux deux routeurs floodfill "fiables" (dont la connexion ne échoue pas) les plus proches de la clé demandée.

Si la clé est trouvée localement par le router floodfill, il répond avec un [I2NP](/docs/specs/i2np/) DatabaseStoreMessage. Si la clé n'est pas trouvée localement par le router floodfill, il répond avec un [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage contenant une liste d'autres routers floodfill proches de la clé.

Les recherches de leaseSet sont chiffrées par garlic encryption de bout en bout depuis la version 0.9.5. Les recherches de RouterInfo ne sont pas chiffrées et sont donc vulnérables à l'espionnage par le point de terminaison sortant (OBEP) du tunnel client. Ceci est dû au coût du chiffrement ElGamal. Le chiffrement des recherches de RouterInfo pourrait être activé dans une future version.

À partir de la version 0.9.7, les réponses à une recherche de leaseSet (un DatabaseStoreMessage ou un DatabaseSearchReplyMessage) seront chiffrées en incluant la clé de session et le tag dans la recherche. Cela masque la réponse de la passerelle d'entrée (IBGW) du tunnel de réponse. Les réponses aux recherches de RouterInfo seront chiffrées si nous activons le chiffrement de recherche.

(Référence : [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sections 2.2-2.3 pour les termes ci-dessous en italique)

En raison de la taille relativement petite du réseau et de la redondance de flooding, les recherches sont généralement en O(1) plutôt qu'en O(log n). Un router a de fortes chances de connaître un router floodfill suffisamment proche de la clé pour obtenir la réponse au premier essai. Dans les versions antérieures à 0.8.9, les routers utilisaient une redondance de recherche de deux (c'est-à-dire que deux recherches étaient effectuées en parallèle vers différents pairs), et ni le routage *récursif* ni *itératif* pour les recherches n'était implémenté. Les requêtes étaient envoyées via *plusieurs routes simultanément* pour *réduire le risque d'échec de la requête*.

À partir de la version 0.8.9, les *recherches itératives* sont implémentées sans redondance de recherche. Il s'agit d'une recherche plus efficace et fiable qui fonctionnera beaucoup mieux lorsque tous les pairs floodfill ne sont pas connus, et cela supprime une limitation sérieuse à la croissance du réseau. Au fur et à mesure que le réseau grandit et que chaque router ne connaît qu'un petit sous-ensemble des pairs floodfill, les recherches deviendront O(log n). Même si le pair ne retourne pas de références plus proches de la clé, la recherche continue avec le pair suivant le plus proche, pour une robustesse accrue et pour empêcher un floodfill malveillant de créer un trou noir dans une partie de l'espace de clés. Les recherches continuent jusqu'à ce qu'un délai d'expiration total de recherche soit atteint, ou que le nombre maximum de pairs soit interrogé.

Les *ID de nœud* sont *vérifiables* car nous utilisons le hash du router directement à la fois comme ID de nœud et comme clé Kademlia. Les réponses incorrectes qui ne sont pas plus proches de la clé de recherche sont généralement ignorées. Étant donné la taille actuelle du réseau, un router a une *connaissance détaillée du voisinage de l'espace d'ID de destination*.

### Vérification du stockage des RouterInfo

Remarque : La vérification RouterInfo est désactivée depuis la version 0.9.7.1 pour empêcher l'attaque décrite dans l'article [Practical Attacks Against the I2P Network](http://wwwcip.informatik.uni-erlangen.de/~spjsschl/i2p.pdf). Il n'est pas certain que la vérification puisse être reconçue pour être effectuée en toute sécurité.

Pour vérifier qu'un stockage a réussi, un router attend simplement environ 10 secondes, puis envoie une recherche à un autre floodfill router proche de la clé (mais pas celui auquel le stockage a été envoyé). Les recherches sont envoyées via l'un des tunnels exploratoires sortants du router. Les recherches sont chiffrées garlic de bout en bout pour empêcher l'espionnage par le point de terminaison sortant (OBEP).

### Vérification du stockage des leaseSet

Pour vérifier qu'un stockage a réussi, un router attend simplement environ 10 secondes, puis envoie une recherche à un autre router floodfill proche de la clé (mais pas celui auquel le stockage a été envoyé). Les recherches sont envoyées via l'un des tunnels clients sortants pour la destination du LeaseSet en cours de vérification. Pour empêcher l'espionnage par l'OBEP du tunnel sortant, les recherches sont chiffrées de bout en bout avec garlic encryption. Les réponses sont spécifiées pour revenir via l'un des tunnels entrants du client.

À partir de la version 0.9.7, les réponses pour les recherches de RouterInfo et de LeaseSet (un DatabaseStoreMessage ou un DatabaseSearchReplyMessage) seront chiffrées, afin de masquer la réponse à la passerelle entrante (IBGW) du tunnel de réponse.

### Exploration

*L'exploration* est une forme spéciale de recherche netdb, où un router tente d'apprendre l'existence de nouveaux routers. Il fait cela en envoyant à un router floodfill un Message DatabaseLookup [I2NP](/docs/specs/i2np/), cherchant une clé aléatoire. Comme cette recherche échouera, le floodfill répondrait normalement avec un DatabaseSearchReplyMessage [I2NP](/docs/specs/i2np/) contenant les hachages des routers floodfill proches de la clé. Cela ne serait pas utile, car le router demandeur connaît probablement déjà ces floodfills, et il serait impraticable d'ajouter tous les routers floodfill au champ "ne pas inclure" du Message DatabaseLookup. Pour une requête d'exploration, le router demandeur définit un indicateur spécial dans le Message DatabaseLookup. Le floodfill répondra alors uniquement avec des routers non-floodfill proches de la clé demandée.

### Notes sur les Réponses de Recherche

La réponse à une requête de recherche est soit un Database Store Message (en cas de succès) soit un Database Search Reply Message (en cas d'échec). Le DSRM contient un champ de hachage du router 'from' pour indiquer la source de la réponse ; le DSM n'en contient pas. Le champ 'from' du DSRM n'est pas authentifié et peut être falsifié ou invalide. Il n'y a pas d'autres balises de réponse. Par conséquent, lors de l'exécution de plusieurs requêtes en parallèle, il est difficile de surveiller les performances des différents floodfill routers.

---

## MultiHoming

Les destinations peuvent être hébergées simultanément sur plusieurs routeurs, en utilisant les mêmes clés privées et publiques (traditionnellement stockées dans les fichiers eepPriv.dat). Comme les deux instances publieront périodiquement leurs LeaseSets signés vers les pairs floodfill, le LeaseSet publié le plus récemment sera retourné à un pair demandant une recherche dans la base de données. Comme les LeaseSets ont une durée de vie de 10 minutes au maximum, si une instance particulière tombe en panne, la panne durera 10 minutes au maximum, et généralement beaucoup moins que cela. La fonction de multihébergement a été vérifiée et est utilisée par plusieurs services sur le réseau.

À partir de la version 0.9.38, les floodfills prennent en charge une nouvelle structure Meta LeaseSet. Cette structure fournit une structure arborescente dans la DHT, pour référencer d'autres LeaseSets. En utilisant les Meta LeaseSets, un site peut implémenter de grands services multihébergés, où plusieurs Destinations différentes sont utilisées pour fournir un service commun. Les entrées dans un Meta LeaseSet sont des Destinations ou d'autres Meta LeaseSets, et peuvent avoir de longues expirations, jusqu'à 18,2 heures. En utilisant cette fonctionnalité, il devrait être possible d'exécuter des centaines ou des milliers de Destinations hébergeant un service commun. Voir la proposition 123 pour plus de détails.

---

## Analyse des menaces

Également abordé sur [la page du modèle de menace](/docs/overview/threat-model/#floodfill).

Un utilisateur malveillant peut tenter de nuire au réseau en créant un ou plusieurs floodfill routers et en les configurant pour offrir des réponses erronées, lentes, ou aucune réponse. Certains scénarios sont discutés ci-dessous.

### Atténuation générale par la croissance

Il y a actuellement environ 1700 routeurs floodfill dans le réseau. La plupart des attaques suivantes deviendront plus difficiles, ou auront moins d'impact, à mesure que la taille du réseau et le nombre de routeurs floodfill augmenteront.

### Atténuation Générale par Redondance

Via flooding, toutes les entrées netdb sont stockées sur les 3 routeurs floodfill les plus proches de la clé.

### Contrefaçons

Toutes les entrées netDb sont signées par leurs créateurs, donc aucun router ne peut falsifier un RouterInfo ou un LeaseSet.

### Lent ou ne répond pas

Chaque router maintient un ensemble étendu de statistiques dans le [profil de pair](/docs/overview/peer-selection/) pour chaque router floodfill, couvrant diverses métriques de qualité pour ce pair. L'ensemble comprend :

- Temps de réponse moyen
- Pourcentage de requêtes ayant reçu les données demandées
- Pourcentage de stockages vérifiés avec succès
- Dernier stockage réussi
- Dernière recherche réussie
- Dernière réponse

Chaque fois qu'un router doit déterminer quel router floodfill est le plus proche d'une clé, il utilise ces métriques pour déterminer quels routers floodfill sont « bons ». Les méthodes et les seuils utilisés pour déterminer cette « qualité » sont relativement nouveaux et font l'objet d'analyses et d'améliorations supplémentaires. Bien qu'un router complètement non réactif soit rapidement identifié et évité, les routers qui ne sont malveillants que parfois peuvent être beaucoup plus difficiles à gérer.

### Attaque Sybil (Espace de clés complet)

Un attaquant peut monter une [attaque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) en créant un grand nombre de floodfill routers répartis dans tout l'espace de clés.

(Dans un exemple connexe, un chercheur a récemment créé un [grand nombre de relais Tor](http://blog.torproject.org/blog/june-2010-progress-report).) En cas de succès, cela pourrait constituer une attaque DOS efficace sur l'ensemble du réseau.

Si les floodfills ne se comportent pas suffisamment mal pour être marqués comme "mauvais" en utilisant les métriques de profil de pairs décrites ci-dessus, c'est un scénario difficile à gérer. La réponse de Tor peut être beaucoup plus agile dans le cas des relais, car les relais suspects peuvent être supprimés manuellement du consensus. Quelques réponses possibles pour le réseau I2P sont listées ci-dessous, cependant aucune d'entre elles n'est complètement satisfaisante :

- Compiler une liste des hash de router ou d'IP malveillants, et annoncer la liste par divers moyens (actualités de la console, site web, forum, etc.) ; les utilisateurs devraient télécharger manuellement la liste et l'ajouter à leur "liste noire" locale.
- Demander à tous les participants du réseau d'activer floodfill manuellement (combattre Sybil avec plus de Sybil)
- Publier une nouvelle version du logiciel qui inclut la liste "malveillante" codée en dur
- Publier une nouvelle version du logiciel qui améliore les métriques et seuils de profil des pairs, dans une tentative d'identifier automatiquement les pairs "malveillants".
- Ajouter un logiciel qui disqualifie les floodfills si trop d'entre eux se trouvent dans un même bloc IP
- Implémenter une liste noire automatique basée sur abonnement contrôlée par un individu ou groupe unique. Cela implémentrait essentiellement une partie du modèle de "consensus" de Tor. Malheureusement, cela donnerait aussi à un individu ou groupe unique le pouvoir de bloquer la participation de n'importe quel router ou IP particulier dans le réseau, ou même d'arrêter ou détruire complètement l'ensemble du réseau.

Cette attaque devient plus difficile à mesure que la taille du réseau augmente.

### Attaque Sybil (Espace de clés partiel)

Un attaquant peut mener une [attaque Sybil](https://www.freehaven.net/anonbib/cache/sybil.pdf) en créant un petit nombre (8-15) de routeurs floodfill regroupés étroitement dans l'espace de clés, et distribuer largement les RouterInfos de ces routeurs. Ensuite, toutes les recherches et stockages pour une clé dans cet espace de clés seraient dirigés vers l'un des routeurs de l'attaquant. Si elle réussit, cela pourrait constituer une attaque DOS efficace sur un site I2P particulier, par exemple.

Comme l'espace de clés est indexé par le hachage cryptographique (SHA256) de la clé, un attaquant doit utiliser une méthode de force brute pour générer de manière répétée des hachages de router jusqu'à ce qu'il en ait suffisamment qui soient suffisamment proches de la clé. La quantité de puissance de calcul requise pour cela, qui dépend de la taille du réseau, est inconnue.

Comme défense partielle contre cette attaque, l'algorithme utilisé pour déterminer la "proximité" Kademlia varie dans le temps. Plutôt que d'utiliser le Hash de la clé (c'est-à-dire H(k)) pour déterminer la proximité, nous utilisons le Hash de la clé ajoutée avec la chaîne de date actuelle, c'est-à-dire H(k + YYYYMMDD). Une fonction appelée "générateur de clé de routage" fait cela, qui transforme la clé originale en "clé de routage". En d'autres termes, l'ensemble de l'espace de clés netDb "tourne" chaque jour à minuit UTC. Toute attaque d'espace de clés partiel devrait être régénérée chaque jour, car après la rotation, les routeurs attaquants ne seraient plus proches de la clé cible, ni les uns des autres.

Cette attaque devient plus difficile à mesure que la taille du réseau augmente. Cependant, des recherches récentes démontrent que la rotation de l'espace de clés n'est pas particulièrement efficace. Un attaquant peut précalculer de nombreux hachages de router à l'avance, et seulement quelques routers suffisent pour "éclipser" une partie de l'espace de clés dans la demi-heure suivant la rotation.

Une conséquence de la rotation quotidienne de l'espace de clés est que la base de données réseau distribuée peut devenir peu fiable pendant quelques minutes après la rotation -- les recherches échoueront car le router "le plus proche" n'a pas encore reçu de stockage. L'étendue du problème et les méthodes d'atténuation (par exemple les "transferts" netDb à minuit) sont un sujet d'étude supplémentaire.

### Attaques de Bootstrap

Un attaquant pourrait tenter de démarrer de nouveaux routers dans un réseau isolé ou majoritairement contrôlé en prenant le contrôle d'un site web de reseed, ou en trompant les développeurs pour qu'ils ajoutent son site web de reseed à la liste codée en dur dans le router.

Plusieurs défenses sont possibles, et la plupart de celles-ci sont prévues :

- Interdire le repli de HTTPS vers HTTP pour le reseeding. Un attaquant MITM pourrait simplement bloquer HTTPS, puis répondre au HTTP.
- Intégrer les données de reseed dans l'installateur

Défenses qui sont implémentées :

- Modifier la tâche de reseed pour récupérer un sous-ensemble de RouterInfos depuis plusieurs sites de reseed plutôt que d'utiliser un seul site
- Créer un service de surveillance de reseed externe au réseau qui interroge périodiquement les sites web de reseed et vérifie que les données ne sont pas obsolètes ou incohérentes avec d'autres vues du réseau
- Depuis la version 0.9.14, les données de reseed sont regroupées dans un fichier zip signé et la signature est vérifiée lors du téléchargement. Voir [la spécification su3](/docs/specs/updates/#su3) pour plus de détails.

### Capture de Requêtes

Voir aussi [lookup](#routerinfo-and-leaseset-lookup) (Référence : [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Sections 2.2-2.3 pour les termes ci-dessous en italique)

Similaire à une attaque de bootstrap, un attaquant utilisant un router floodfill pourrait tenter de "diriger" les pairs vers un sous-ensemble de routers qu'il contrôle en retournant leurs références.

Ceci est peu susceptible de fonctionner via l'exploration, car l'exploration est une tâche de faible fréquence. Les routers acquièrent la majorité de leurs références de pairs par l'activité normale de construction de tunnels. Les résultats d'exploration sont généralement limités à quelques hachages de router, et chaque requête d'exploration est dirigée vers un router floodfill aléatoire.

À partir de la version 0.8.9, les *recherches itératives* sont implémentées. Pour les références de router floodfill retournées dans une réponse [I2NP](/docs/specs/i2np/) DatabaseSearchReplyMessage à une recherche, ces références sont suivies si elles sont plus proches (ou les plus proches suivantes) de la clé de recherche. Le router demandeur ne fait pas confiance au fait que les références sont plus proches de la clé (c'est-à-dire qu'elles sont *vérifiablement correctes*). La recherche ne s'arrête pas non plus quand aucune clé plus proche n'est trouvée, mais continue en interrogeant le nœud le plus proche suivant, jusqu'à ce que le délai d'expiration ou le nombre maximum de requêtes soit atteint. Ceci empêche un floodfill malveillant de créer un trou noir dans une partie de l'espace de clés. De plus, la rotation quotidienne de l'espace de clés oblige un attaquant à régénérer une information de router dans la région d'espace de clés désirée. Cette conception garantit que l'attaque de capture de requête décrite dans [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) est beaucoup plus difficile.

### Sélection de relais basée sur DHT

(Référence : [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) Section 3)

Cela n'a pas grand-chose à voir avec floodfill, mais consultez la [page de sélection des pairs](/docs/overview/peer-selection/) pour une discussion sur les vulnérabilités de la sélection des pairs pour les tunnels.

### Fuites d'informations

(Référence : [In Search of an Anonymous and Secure Lookup](https://www.freehaven.net/anonbib/cache/ccs10-lookup.pdf) Section 3)

Cet article traite des faiblesses dans les recherches DHT "Finger Table" utilisées par Torsk et NISAN. À première vue, celles-ci ne semblent pas s'appliquer à I2P. Premièrement, l'utilisation de DHT par Torsk et NISAN est significativement différente de celle d'I2P. Deuxièmement, les recherches de base de données réseau d'I2P ne sont que faiblement corrélées aux processus de [sélection des pairs](/docs/overview/peer-selection/) et de [construction de tunnels](/docs/overview/tunnel-routing/) ; seuls les pairs précédemment connus sont utilisés pour les tunnels. De plus, la sélection des pairs n'est liée à aucune notion de proximité de clé DHT.

Une partie de ceci pourrait en fait être plus intéressante lorsque le réseau I2P deviendra beaucoup plus important. À l'heure actuelle, chaque router connaît une grande proportion du réseau, donc rechercher une Router Info particulière dans la netDb n'indique pas fortement une intention future d'utiliser ce router dans un tunnel. Peut-être que lorsque le réseau sera 100 fois plus grand, la recherche pourra être plus corrélative. Bien sûr, un réseau plus grand rend une attaque Sybil d'autant plus difficile.

Cependant, la question générale des fuites d'informations DHT dans I2P nécessite des investigations plus poussées. Les routeurs floodfill sont en position d'observer les requêtes et de collecter des informations. Certainement, à un niveau de *f* = 0,2 (20% de nœuds malveillants, comme spécifié dans l'article) nous nous attendons à ce que de nombreuses menaces Sybil que nous décrivons ([ici](/docs/overview/threat-model/#sybil), [ici](#sybil-attack-full-keyspace) et [ici](#sybil-attack-partial-keyspace)) deviennent problématiques pour plusieurs raisons.

---

## Historique

[Déplacé vers la page de discussion netdb](/docs/legacy/netdb/).

---

## Travaux futurs

Chiffrement de bout en bout des requêtes et réponses netDb supplémentaires.

Meilleures méthodes pour suivre les réponses de recherche.
