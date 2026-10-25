---
title: "Spécification de Création de Tunnel (ElGamal)"
description: "Spécification de construction de tunnel basée sur l'ancien ElGamal, remplacée par X25519"
slug: "elgamal-tunnel-creation"
aliases:
  - "/fr/tunnel-alt-creation"
  - "/fr/tunnel-alt-creation/"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Aperçu {#tunnelcreate-overview}

NOTE : OBSOLÈTE - Ceci est la spécification de construction de tunnel ElGamal. Voir la [spécification de construction de tunnel X25519](/docs/specs/tunnel-creation-ecies) pour la méthode actuelle.

Ce document spécifie les détails des messages de construction de tunnel chiffrés utilisés pour créer des tunnels en utilisant une méthode de "téléscopage non-interactif". Voir le document de construction de tunnel [TUNNEL-IMPL](/docs/specs/tunnel-implementation) pour un aperçu du processus, incluant les méthodes de sélection et d'ordonnancement des pairs.

La création de tunnel est accomplie par un seul message passé le long du chemin des pairs dans le tunnel, réécrit sur place, et transmis en retour au créateur du tunnel. Ce message de tunnel unique est composé d'un nombre variable d'enregistrements (jusqu'à 8) - un pour chaque pair potentiel dans le tunnel. Les enregistrements individuels sont chiffrés de manière asymétrique (ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal)) pour être lus uniquement par un pair spécifique le long du chemin, tandis qu'une couche supplémentaire de chiffrement symétrique (AES [CRYPTO-AES](/docs/specs/cryptography#AES)) est ajoutée à chaque saut afin d'exposer l'enregistrement chiffré asymétriquement seulement au moment approprié.

### Nombre d'enregistrements {#number}

Tous les enregistrements ne doivent pas nécessairement contenir des données valides. Le message de construction pour un tunnel à 3 sauts, par exemple, peut contenir plus d'enregistrements pour cacher la longueur réelle du tunnel aux participants. Il existe deux types de messages de construction. Le message Tunnel Build Message original ([TBM](/docs/specs/i2np#msg-tunnelbuild)) contient 8 enregistrements, ce qui est largement suffisant pour toute longueur de tunnel pratique. Le plus récent Variable Tunnel Build Message ([VTBM](/docs/specs/i2np#msg-variabletunnelbuild)) contient de 1 à 8 enregistrements. L'initiateur peut faire un compromis entre la taille du message et le niveau d'obscurcissement souhaité de la longueur du tunnel.

Dans le réseau actuel, la plupart des tunnels font 2 ou 3 sauts de long. L'implémentation actuelle utilise un VTBM à 5 enregistrements pour construire des tunnels de 4 sauts ou moins, et le TBM à 8 enregistrements pour les tunnels plus longs. Le VTBM à 5 enregistrements (qui, une fois fragmenté, tient dans trois messages de tunnel de 1KB) réduit le trafic réseau et augmente le taux de succès de construction, car les messages plus petits sont moins susceptibles d'être abandonnés.

Le message de réponse doit être du même type et de la même longueur que le message de construction.

### Spécification d'enregistrement de requête {#tunnelcreate-requestrecord}

Également spécifié dans la spécification I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

Texte en clair de l'enregistrement, visible uniquement au saut interrogé :

```
bytes     0-3: tunnel ID to receive messages as, nonzero
bytes    4-35: local router identity hash
bytes   36-39: next tunnel ID, nonzero
bytes   40-71: next router identity hash
bytes  72-103: AES-256 tunnel layer key
bytes 104-135: AES-256 tunnel IV key
bytes 136-167: AES-256 reply key
bytes 168-183: AES-256 reply IV
byte      184: flags
bytes 185-188: request time (in hours since the epoch, rounded down)
bytes 189-192: next message ID
bytes 193-221: uninterpreted / random padding
```
Les champs ID de tunnel suivant et hachage d'identité de routeur suivant sont utilisés pour spécifier le saut suivant dans le tunnel, bien que pour un point de terminaison de tunnel sortant, ils spécifient où le message de réponse de création de tunnel réécrit doit être envoyé. De plus, l'ID de message suivant spécifie l'ID de message que le message (ou la réponse) doit utiliser.

La clé de couche tunnel, la clé IV tunnel, la clé de réponse et l'IV de réponse sont chacune des valeurs aléatoires de 32 octets générées par le créateur, pour utilisation uniquement dans cet enregistrement de demande de construction.

Le champ flags contient les éléments suivants :

```
Bit order: 76543210 (bit 7 is MSB)
bit 7: if set, allow messages from anyone
bit 6: if set, allow messages to anyone, and send the reply to the
       specified next hop in a Tunnel Build Reply Message
bits 5-0: Undefined, must set to 0 for compatibility with future options
```
Le bit 7 indique que le saut sera une passerelle d'entrée (IBGW). Le bit 6 indique que le saut sera un point de sortie (OBEP). Si aucun des deux bits n'est défini, le saut sera un participant intermédiaire. Les deux ne peuvent pas être définis en même temps.

#### Création d'Enregistrement de Requête

Chaque saut reçoit un Tunnel ID aléatoire, non nul. Les Tunnel ID du saut actuel et du saut suivant sont renseignés. Chaque enregistrement reçoit une clé IV de tunnel aléatoire, un IV de réponse, une clé de couche et une clé de réponse.

#### Chiffrement des enregistrements de requête {#encryption}

Cet enregistrement en clair est chiffré ElGamal 2048 [CRYPTO-ELG](/docs/specs/cryptography#elgamal) avec la clé de chiffrement publique du saut et formaté en un enregistrement de 528 octets :

```
bytes   0-15: First 16 bytes of the SHA-256 of the current hop's router identity
bytes 16-527: ElGamal-2048 encrypted request record
```
Dans l'enregistrement chiffré de 512 octets, les données ElGamal contiennent les octets 1-256 et 258-513 du bloc chiffré ElGamal de 514 octets [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Les deux octets de remplissage du bloc (les octets zéro aux emplacements 0 et 257) sont supprimés.

Puisque le texte en clair utilise le champ complet, il n'y a pas besoin de remplissage supplémentaire au-delà de `SHA256(cleartext) + cleartext`.

Chaque enregistrement de 528 octets est ensuite chiffré de manière itérative (en utilisant le déchiffrement AES, avec la clé de réponse et l'IV de réponse pour chaque saut) de sorte que l'identité du router ne soit en clair que pour le saut en question.

### Traitement des sauts et chiffrement {#tunnelcreate-hopprocessing}

Lorsqu'un saut reçoit un TunnelBuildMessage, il parcourt les enregistrements qu'il contient pour en trouver un commençant par son propre hash d'identité (tronqué à 16 octets). Il déchiffre ensuite le bloc ElGamal de cet enregistrement et récupère le texte en clair protégé. À ce moment-là, il s'assure que la demande de tunnel n'est pas un doublon en alimentant la clé de réponse AES-256 dans un filtre de Bloom. Les doublons ou les demandes invalides sont supprimés. Les enregistrements qui ne sont pas horodatés avec l'heure actuelle, ou l'heure précédente si peu après le début de l'heure, doivent être supprimés. Par exemple, prenez l'heure dans l'horodatage, convertissez-la en temps complet, puis si elle a plus de 65 minutes de retard ou 5 minutes d'avance par rapport à l'heure actuelle, elle est invalide. Le filtre de Bloom doit avoir une durée d'au moins une heure (plus quelques minutes, pour tenir compte du décalage d'horloge), afin que les enregistrements dupliqués dans l'heure actuelle qui ne sont pas rejetés par la vérification de l'horodatage d'heure dans l'enregistrement, soient rejetés par le filtre.

Après avoir décidé s'ils acceptent ou non de participer au tunnel, ils remplacent l'enregistrement qui contenait la demande par un bloc de réponse chiffré. Tous les autres enregistrements sont chiffrés en AES-256 [CRYPTO-AES](/docs/specs/cryptography#AES) avec la clé de réponse et l'IV inclus. Chacun est chiffré séparément en AES/CBC avec la même clé de réponse et le même IV de réponse. Le mode CBC n'est pas continué (chaîné) entre les enregistrements.

Chaque saut ne connaît que sa propre réponse. S'il accepte, il maintiendra le tunnel jusqu'à expiration, même s'il ne sera pas utilisé, car il ne peut pas savoir si tous les autres sauts ont accepté.

#### Spécification de l'enregistrement de réponse {#tunnelcreate-replyrecord}

Après que le saut actuel lit son enregistrement, il le remplace par un enregistrement de réponse indiquant s'il accepte ou non de participer au tunnel, et s'il refuse, il classe sa raison de rejet. Il s'agit simplement d'une valeur de 1 octet, où 0x0 signifie qu'il accepte de participer au tunnel, et des valeurs plus élevées signifient des niveaux de rejet plus élevés.

Les codes de rejet suivants sont définis :

- TUNNEL_REJECT_PROBABALISTIC_REJECT = 10
- TUNNEL_REJECT_TRANSIENT_OVERLOAD = 20
- TUNNEL_REJECT_BANDWIDTH = 30
- TUNNEL_REJECT_CRIT = 50

Pour cacher d'autres causes, telles que l'arrêt du router, aux pairs, l'implémentation actuelle utilise TUNNEL_REJECT_BANDWIDTH pour presque tous les rejets.

La réponse est chiffrée avec la clé de session AES qui lui est transmise dans le bloc chiffré, complétée avec 495 octets de données aléatoires pour atteindre la taille complète de l'enregistrement. Le remplissage est placé avant l'octet de statut :

```
AES-256-CBC(SHA-256(padding+status) + padding + status, key, IV)

bytes   0-31 : SHA-256 of bytes 32-527
bytes 32-526 : Random padding
byte 527     : Reply value
```
Ceci est également décrit dans la spécification I2NP [BRR](/docs/specs/i2np#struct-buildrequestrecord).

### Préparation des messages de construction de tunnel {#tunnelcreate-requestpreparation}

Lors de la construction d'un nouveau Tunnel Build Message, tous les Build Request Records doivent d'abord être construits et chiffrés de manière asymétrique en utilisant ElGamal [CRYPTO-ELG](/docs/specs/cryptography#elgamal). Chaque enregistrement est ensuite déchiffré de manière préventive avec les clés de réponse et les IV des sauts précédents dans le chemin, en utilisant AES [CRYPTO-AES](/docs/specs/cryptography#AES). Ce déchiffrement doit être exécuté dans l'ordre inverse afin que les données chiffrées de manière asymétrique apparaissent en clair au bon saut après que leur prédécesseur les ait chiffrées.

Les enregistrements excédentaires non nécessaires pour les requêtes individuelles sont simplement remplis avec des données aléatoires par le créateur.

### Livraison des Messages de Construction de Tunnel {#tunnelcreate-requestdelivery}

Pour les tunnels sortants, la livraison se fait directement du créateur du tunnel vers le premier saut, en empaquetant le TunnelBuildMessage comme si le créateur était juste un autre saut dans le tunnel. Pour les tunnels entrants, la livraison se fait à travers un tunnel sortant existant. Le tunnel sortant provient généralement du même pool que le nouveau tunnel en cours de construction. Si aucun tunnel sortant n'est disponible dans ce pool, un tunnel exploratoire sortant est utilisé. Au démarrage, quand aucun tunnel exploratoire sortant n'existe encore, un faux tunnel sortant à 0 saut est utilisé.

### Gestion des points de terminaison des messages de construction de tunnel {#tunnelcreate-endpointhandling}

Pour la création d'un tunnel sortant, lorsque la requête atteint un point de terminaison sortant (tel que déterminé par le flag 'autoriser les messages à quiconque'), le saut est traité comme d'habitude, chiffrant une réponse à la place de l'enregistrement et chiffrant tous les autres enregistrements, mais puisqu'il n'y a pas de 'saut suivant' vers lequel transférer le TunnelBuildMessage, il place plutôt les enregistrements de réponse chiffrés dans un TunnelBuildReplyMessage ([TBRM](/docs/specs/i2np#msg-tunnelbuildreply)) ou VariableTunnelBuildReplyMessage ([VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply)) (le type de message et le nombre d'enregistrements doivent correspondre à ceux de la requête) et le livre au tunnel de réponse spécifié dans l'enregistrement de requête. Ce tunnel de réponse transfère le Tunnel Build Reply Message vers le créateur du tunnel, exactement comme pour tout autre message [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation). Le créateur du tunnel le traite ensuite, comme décrit ci-dessous.

Le tunnel de réponse a été sélectionné par le créateur comme suit : Généralement, il s'agit d'un tunnel entrant du même pool que le nouveau tunnel sortant en cours de construction. Si aucun tunnel entrant n'est disponible dans ce pool, un tunnel exploratoire entrant est utilisé. Au démarrage, lorsqu'aucun tunnel exploratoire entrant n'existe encore, un faux tunnel entrant à 0 saut est utilisé.

Pour la création d'un tunnel entrant, lorsque la requête atteint le point d'arrivée entrant (également connu sous le nom de créateur de tunnel), il n'est pas nécessaire de générer un message de réponse de construction de tunnel explicite, et le router traite chacune des réponses, comme ci-dessous.

### Traitement des messages de réponse de construction de tunnel {#tunnelcreate-replyprocessing}

Pour traiter les enregistrements de réponse, le créateur doit simplement déchiffrer AES chaque enregistrement individuellement, en utilisant la clé de réponse et l'IV de chaque saut dans le tunnel après le pair (dans l'ordre inverse). Ceci expose alors la réponse spécifiant s'ils acceptent de participer au tunnel ou pourquoi ils refusent. S'ils acceptent tous, le tunnel est considéré comme créé et peut être utilisé immédiatement, mais si quelqu'un refuse, le tunnel est abandonné.

Les accords et rejets sont notés dans le profil de chaque pair [PEER-SELECTION](/docs/overview/peer-selection), pour être utilisés dans les évaluations futures de la capacité de tunnel du pair.

## Historique et Notes {#tunnelcreate-notes}

Cette stratégie est née lors d'une discussion sur la liste de diffusion I2P entre Michael Rogers, Matthew Toseland (toad), et jrandom concernant l'attaque de prédécesseur. Voir [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html), [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html). Elle a été introduite dans la version 0.6.1.10 le 2006-02-16, qui était la dernière fois qu'un changement non rétrocompatible était effectué dans I2P.

Notes :

- Cette conception n'empêche pas deux pairs hostiles au sein d'un tunnel de
  marquer un ou plusieurs enregistrements de requête ou de réponse pour détecter qu'ils se trouvent dans
  le même tunnel, mais cela peut être détecté par le créateur du tunnel lors de
  la lecture de la réponse, provoquant le marquage du tunnel comme invalide.

- Cette conception n'inclut pas de preuve de travail sur la section chiffrée asymétriquement, bien que le hachage d'identité de 16 octets pourrait être réduit de moitié avec cette dernière partie remplacée par une fonction hashcash d'un coût allant jusqu'à 2^64.

- Cette conception seule n'empêche pas deux pairs hostiles au sein d'un tunnel d'utiliser les informations de synchronisation pour déterminer s'ils se trouvent dans le même tunnel. L'utilisation de la livraison groupée et synchronisée des requêtes pourrait aider (regrouper les requêtes et les envoyer à la minute (synchronisée ntp)). Cependant, cela permet aux pairs de « marquer » les requêtes en les retardant et en détectant le retard plus tard dans le tunnel, bien que peut-être abandonner les requêtes non livrées dans une petite fenêtre pourrait fonctionner (bien que cela nécessiterait un haut degré de synchronisation d'horloge). Alternativement, peut-être que les sauts individuels pourraient injecter un délai aléatoire avant de transmettre la requête ?

- Existe-t-il des méthodes non fatales pour étiqueter la requête ?

- L'horodatage avec une résolution d'une heure est utilisé pour la prévention des attaques par rejeu. Cette contrainte n'était pas appliquée avant la version 0.9.16.

## Travail futur {#future}

- Dans l'implémentation actuelle, l'initiateur laisse un enregistrement vide
  pour lui-même. Ainsi un message de n enregistrements ne peut construire qu'un tunnel de n-1 sauts.
  Cela semble nécessaire pour les tunnels entrants (où l'avant-dernier saut
  peut voir le préfixe de hachage pour le saut suivant), mais pas pour les tunnels sortants.
  Cela doit être étudié et vérifié. S'il est possible d'utiliser
  l'enregistrement restant sans compromettre l'anonymat, nous devrions le faire.

- Analyse approfondie des possibles attaques de marquage et de synchronisation décrites dans les notes ci-dessus.

- Utiliser uniquement VTBM ; ne pas sélectionner d'anciens pairs qui ne le prennent pas en charge.

- L'enregistrement de demande de construction ne spécifie pas de durée de vie ou d'expiration du tunnel ;
  chaque saut fait expirer le tunnel après 10 minutes, ce qui est une
  constante codée en dur à l'échelle du réseau. Nous pourrions utiliser un bit dans le champ de drapeaux et prendre 4 (ou 8)
  octets du remplissage pour spécifier une durée de vie ou une expiration. Le demandeur
  ne spécifierait cette option que si tous les participants la prenaient en charge.

## Références {#ref}

- [BRR](/docs/specs/i2np#struct-buildrequestrecord) - Build Request Record
- [CRYPTO-AES](/docs/specs/cryptography#AES) - AES Encryption
- [CRYPTO-ELG](/docs/specs/cryptography#elgamal) - ElGamal Encryption
- [HASHING-IT-OUT](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf) - Hashing It Out Paper
- [PEER-SELECTION](/docs/overview/peer-selection) - Peer Selection
- [PREDECESSOR](http://forensics.umass.edu/pubs/wright-tissec.pdf) - Predecessor Attack Paper
- [PREDECESSOR-2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf) - Predecessor Attack Paper (2008)
- [TBM](/docs/specs/i2np#msg-tunnelbuild) - Tunnel Build Message
- [TBRM](/docs/specs/i2np#msg-tunnelbuildreply) - Tunnel Build Reply Message
- [TUNBUILD-REASONING](http://zzz.i2p/archive/2005-10/msg00129.html) - Tunnel Build Reasoning
- [TUNBUILD-SUMMARY](http://zzz.i2p/archive/2005-10/msg00138.html) - Tunnel Build Summary
- [TUNNEL-IMPL](/docs/specs/tunnel-implementation) - Tunnel Implementation
- [TUNNEL-OP](/docs/specs/tunnel-implementation#tunnel.operation) - Tunnel Operation
- [VTBM](/docs/specs/i2np#msg-variabletunnelbuild) - Variable Tunnel Build Message
- [VTBRM](/docs/specs/i2np#msg-variabletunnelbuildreply) - Variable Tunnel Build Reply Message
