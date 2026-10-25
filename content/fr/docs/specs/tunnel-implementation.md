---
title: "Implémentation des tunnels"
description: "Spécification du fonctionnement des tunnels I2P, de leur construction et du traitement des messages"
slug: "tunnel-implementation"
aliases:
  - "/fr/docs/specs/implementation"
  - "/fr/docs/specs/implementation/"
lastUpdated: "2019-07"
accurateFor: "0.9.41"
---

Cette page documente l'implémentation actuelle des tunnels.

## Aperçu des tunnels {#tunnel.overview}

Dans I2P, les messages sont transmis dans une direction à travers un tunnel virtuel de pairs, en utilisant tous les moyens disponibles pour transmettre le message au saut suivant. Les messages arrivent à la *passerelle* du tunnel, sont regroupés et/ou fragmentés en messages de tunnel de taille fixe, puis transmis au saut suivant dans le tunnel, qui traite et vérifie la validité du message et l'envoie au saut suivant, et ainsi de suite, jusqu'à ce qu'il atteigne le point de terminaison du tunnel. Ce *point de terminaison* prend les messages regroupés par la passerelle et les transmet selon les instructions - soit vers un autre router, vers un autre tunnel sur un autre router, ou localement.

Les tunnels fonctionnent tous de la même manière, mais peuvent être segmentés en deux groupes différents - les tunnels entrants et les tunnels sortants. Les tunnels entrants ont une passerelle non fiable qui transmet les messages vers le créateur du tunnel, qui sert de point de terminaison du tunnel. Pour les tunnels sortants, le créateur du tunnel sert de passerelle, transmettant les messages vers le point de terminaison distant.

Le créateur du tunnel sélectionne exactement quels pairs participeront au tunnel, et fournit à chacun les données de configuration nécessaires. Ils peuvent avoir n'importe quel nombre de sauts. L'intention est de rendre difficile pour les participants ou les tiers de déterminer la longueur d'un tunnel, ou même pour les participants qui collaborent de déterminer s'ils font partie du même tunnel (excepté dans la situation où des pairs qui collaborent sont adjacents dans le tunnel).

En pratique, une série de pools de tunnels sont utilisés à des fins différentes - chaque destination de client local a son propre ensemble de tunnels entrants et sortants, configurés pour répondre à ses besoins d'anonymat et de performance. De plus, le router lui-même maintient une série de pools pour participer à la base de données réseau et pour gérer les tunnels eux-mêmes.

I2P est un réseau intrinsèquement à commutation de paquets, même avec ces tunnels, lui permettant de tirer parti de plusieurs tunnels fonctionnant en parallèle, augmentant la résilience et équilibrant la charge. En dehors de la couche I2P principale, il existe une bibliothèque de streaming de bout en bout optionnelle disponible pour les applications clientes, exposant un fonctionnement similaire à TCP, incluant la réorganisation des messages, la retransmission, le contrôle de congestion, etc.

Un aperçu de la terminologie des tunnels I2P se trouve [sur la page d'aperçu des tunnels](/docs/overview/tunnel-routing).

## Fonctionnement des tunnels (Traitement des messages) {#tunnel.operation}

### Aperçu

Après qu'un tunnel est construit, les [messages I2NP](/docs/specs/i2np) sont traités et transmis à travers celui-ci. Le fonctionnement du tunnel comprend quatre processus distincts, pris en charge par différents pairs dans le tunnel.

1. Tout d'abord, la passerelle de tunnel accumule un certain nombre
   de messages I2NP et les prétraite en messages de tunnel pour
   la livraison.
2. Ensuite, cette passerelle chiffre ces données prétraitées, puis
   les transmet au premier saut.
3. Ce pair, et les participants suivants du tunnel,
   déchiffrent une couche du chiffrement, vérifient qu'il ne s'agit pas
   d'un doublon, puis le transmettent au pair suivant.
4. Finalement, les messages de tunnel arrivent au point de terminaison où les messages I2NP
   originalement regroupés par la passerelle sont réassemblés et transmis comme
   demandé.

Les participants intermédiaires du tunnel ne savent pas s'ils se trouvent dans un tunnel entrant ou sortant ; ils "chiffrent" toujours pour le saut suivant. Par conséquent, nous tirons parti du chiffrement AES symétrique pour "déchiffrer" à la passerelle du tunnel sortant, de sorte que le texte en clair soit révélé au point de sortie du tunnel sortant.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Preprocessing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Postprocessing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Gateway (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively encrypt (using decryption operations)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound Endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Decrypt (using an encryption operation) to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Forward as instructed to Inbound Gateway or Router</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="4"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, Batch, and Pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound Endpoint (Creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt to reveal plaintext tunnel message</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble Fragments, Receive data</td>
    </tr>
  </tbody>
</table>
### Traitement de la passerelle {#tunnel.gateway}

#### Prétraitement des messages {#tunnel.preprocessing}

La fonction d'une passerelle de tunnel est de fragmenter et d'empaqueter les [messages I2NP](/docs/specs/i2np) dans des [messages de tunnel](/docs/specs/tunnel-message) de taille fixe et de chiffrer les messages de tunnel. Les messages de tunnel contiennent les éléments suivants :

- Un Tunnel ID de 4 octets
- Un IV (vecteur d'initialisation) de 16 octets
- Une somme de contrôle
- Du rembourrage, si nécessaire
- Une ou plusieurs paires { instruction de livraison, fragment de message I2NP }

Les identifiants de tunnel sont des nombres de 4 octets utilisés à chaque saut - les participants savent quel identifiant de tunnel écouter pour les messages et quel identifiant de tunnel ils doivent utiliser pour transférer au saut suivant, et chaque saut choisit l'identifiant de tunnel sur lequel il reçoit les messages. Les tunnels eux-mêmes ont une durée de vie courte (10 minutes). Même si des tunnels ultérieurs sont construits en utilisant la même séquence de pairs, l'identifiant de tunnel de chaque saut changera.

Pour empêcher les adversaires de marquer les messages le long du chemin en ajustant la taille des messages, tous les messages de tunnel ont une taille fixe de 1024 octets. Pour accommoder les messages I2NP plus volumineux ainsi que pour prendre en charge plus efficacement les plus petits, la passerelle divise les messages I2NP plus volumineux en fragments contenus dans chaque message de tunnel. Le point de terminaison tentera de reconstituer le message I2NP à partir des fragments pendant une courte période, mais les supprimera si nécessaire.

Les détails se trouvent dans la [spécification des messages de tunnel](/docs/specs/tunnel-message).

### Chiffrement de passerelle

Après le prétraitement des messages en une charge utile rembourrée, la passerelle construit une valeur IV aléatoire de 16 octets, la chiffre de manière itérative ainsi que le message tunnel selon les besoins, et transmet le tuple {tunnelID, IV, message tunnel chiffré} au saut suivant.

La façon dont le chiffrement au niveau de la passerelle est effectué dépend du fait que le tunnel soit entrant ou sortant. Pour les tunnels entrants, ils sélectionnent simplement un IV aléatoire, le post-traitent et le mettent à jour pour générer l'IV de la passerelle et utilisent cet IV avec leur propre clé de couche pour chiffrer les données prétraitées. Pour les tunnels sortants, ils doivent déchiffrer de manière itérative l'IV (non chiffré) et les données prétraitées avec l'IV et les clés de couche pour tous les sauts dans le tunnel. Le résultat du chiffrement du tunnel sortant est que lorsque chaque pair le chiffre, le point de terminaison récupérera les données prétraitées initiales.

### Traitement des participants {#tunnel.participant}

Lorsqu'un pair reçoit un message de tunnel, il vérifie que le message provient du même saut précédent qu'auparavant (initialisé lors du passage du premier message dans le tunnel). Si le pair précédent est un router différent, ou si le message a déjà été vu, le message est abandonné. Le participant chiffre ensuite l'IV reçu avec AES256/ECB en utilisant sa clé IV pour déterminer l'IV actuel, utilise cet IV avec la clé de couche du participant pour chiffrer les données, chiffre l'IV actuel avec AES256/ECB en utilisant à nouveau sa clé IV, puis transmet le tuple {nextTunnelId, nextIV, encryptedData} au saut suivant. Ce double chiffrement de l'IV (à la fois avant et après utilisation) aide à contrer une certaine classe d'attaques de confirmation.

La détection de messages dupliqués est gérée par un filtre de Bloom décroissant sur les IV des messages. Chaque router maintient un seul filtre de Bloom pour contenir le XOR de l'IV et du premier bloc du message reçu pour tous les tunnels auxquels il participe, modifié pour supprimer les entrées vues après 10-20 minutes (lorsque les tunnels auront expiré). La taille du filtre de Bloom et les paramètres utilisés sont suffisants pour plus que saturer la connexion réseau du router avec une chance négligeable de faux positif. La valeur unique alimentée dans le filtre de Bloom est le XOR de l'IV et du premier bloc afin d'empêcher les pairs collusoires non séquentiels dans le tunnel de marquer un message en le renvoyant avec l'IV et le premier bloc échangés.

### Traitement des points de terminaison {#tunnel.endpoint}

Après avoir reçu et validé un message de tunnel au dernier saut du tunnel, la façon dont le point de terminaison récupère les données encodées par la passerelle dépend de si le tunnel est un tunnel entrant ou sortant. Pour les tunnels sortants, le point de terminaison chiffre le message avec sa clé de couche comme tout autre participant, exposant les données prétraitées. Pour les tunnels entrants, le point de terminaison est aussi le créateur du tunnel donc il peut simplement déchiffrer de manière itérative l'IV et le message, en utilisant les clés de couche et d'IV de chaque étape dans l'ordre inverse.

À ce stade, le point de terminaison du tunnel dispose des données prétraitées envoyées par la passerelle, qu'il peut alors analyser pour extraire les messages I2NP inclus et les transmettre selon les instructions de livraison demandées.

## Construction de tunnel {#tunnel.building}

Lors de la construction d'un tunnel, le créateur doit envoyer une requête avec les données de configuration nécessaires à chacun des sauts et attendre que tous acceptent avant d'activer le tunnel. Les requêtes sont chiffrées de sorte que seuls les pairs qui ont besoin de connaître une information (comme la couche du tunnel ou la clé IV) disposent de ces données. De plus, seul le créateur du tunnel aura accès à la réponse du pair. Il y a trois dimensions importantes à garder à l'esprit lors de la production des tunnels : quels pairs sont utilisés (et où), comment les requêtes sont envoyées (et les réponses reçues), et comment ils sont maintenus.

### Sélection des pairs {#tunnel.peerselection}

Au-delà des deux types de tunnels - entrant et sortant - il existe deux styles de sélection de pairs utilisés pour différents tunnels - exploratoire et client. Les tunnels exploratoires sont utilisés à la fois pour la maintenance de la base de données réseau et la maintenance des tunnels, tandis que les tunnels clients sont utilisés pour les messages client de bout en bout.

#### Sélection des pairs de tunnel exploratoire {#tunnel.selection.exploratory}

Les tunnels exploratoires sont construits à partir d'une sélection aléatoire de pairs provenant d'un sous-ensemble du réseau. Ce sous-ensemble particulier varie selon le router local et ses besoins de routage de tunnel. En général, les tunnels exploratoires sont construits à partir de pairs sélectionnés aléatoirement qui se trouvent dans la catégorie de profil "non défaillant mais actif" du pair. L'objectif secondaire des tunnels, au-delà du simple routage de tunnel, est de trouver des pairs de haute capacité sous-utilisés afin qu'ils puissent être promus pour être utilisés dans les tunnels clients.

La sélection exploratoire de pairs est discutée plus en détail sur la [page Profilage et Sélection de Pairs](/docs/overview/peer-selection).

#### Sélection des pairs pour les tunnels client {#tunnel.selection.client}

Les tunnels clients sont construits avec un ensemble d'exigences plus strictes - le router local sélectionnera des pairs dans sa catégorie de profil "rapide et haute capacité" afin que les performances et la fiabilité répondent aux besoins de l'application cliente. Cependant, il existe plusieurs détails importants au-delà de cette sélection de base qui doivent être respectés, selon les besoins d'anonymat du client.

La sélection des pairs clients est discutée plus en détail sur la [page Profilage et Sélection des Pairs](/docs/overview/peer-selection).

#### Ordre des pairs dans les tunnels {#ordering}

Les pairs sont ordonnés dans les tunnels pour faire face à l'[attaque du prédécesseur](http://forensics.umass.edu/pubs/wright-tissec.pdf) ([mise à jour 2008](http://forensics.umass.edu/pubs/wright.tissec.2008.pdf)).

Pour contrecarrer l'attaque de prédécesseur, la sélection de tunnel maintient les pairs sélectionnés dans un ordre strict - si A, B et C sont dans un tunnel pour un pool de tunnels particulier, le saut après A est toujours B, et le saut après B est toujours C.

L'ordonnancement est implémenté en générant une clé aléatoire de 32 octets pour chaque pool de tunnel au démarrage. Les pairs ne devraient pas pouvoir deviner l'ordonnancement, sinon un attaquant pourrait créer deux hachages de router très éloignés pour maximiser les chances d'être aux deux extrémités d'un tunnel. Les pairs sont triés par distance XOR du hachage SHA256 de (le hachage du pair concaténé avec la clé aléatoire) depuis la clé aléatoire :

```
      p = peer hash
      k = random key
      d = XOR(H(p+k), k)
```
Comme chaque pool de tunnels utilise une clé aléatoire différente, l'ordre est cohérent au sein d'un seul pool mais pas entre différents pools. De nouvelles clés sont générées à chaque redémarrage du router.

### Livraison de requête {#tunnel.request}

Un tunnel multi-saut est construit en utilisant un seul message de construction qui est décrypté et transmis de manière répétée. Dans la terminologie de [Hashing it out in Public](http://www-users.cs.umn.edu/~hopper/hashing_it_out.pdf), il s'agit de construction de tunnel télescopique "non-interactive".

Cette méthode de préparation, de livraison et de réponse des demandes de tunnel est [conçue](/docs/specs/tunnel-creation) pour réduire le nombre de prédécesseurs exposés, diminuer le nombre de messages transmis, vérifier la connectivité appropriée, et éviter l'attaque de comptage de messages de la création traditionnelle de tunnel télescopique. (Cette méthode, qui envoie des messages pour étendre un tunnel à travers la partie déjà établie du tunnel, est appelée création de tunnel télescopique "interactive" dans le document "Hashing it out".)

Les détails des messages de demande et de réponse de tunnel, ainsi que leur chiffrement, [sont spécifiés ici](/docs/specs/tunnel-creation).

Les pairs peuvent rejeter les demandes de création de tunnel pour diverses raisons, bien que quatre rejets de sévérité croissante soient connus : rejet probabiliste (dû à l'approche de la capacité du router, ou en réponse à un flot de demandes), surcharge transitoire, surcharge de bande passante, et défaillance critique. Lorsqu'ils sont reçus, ces quatre types sont interprétés par le créateur de tunnel pour aider à ajuster leur profil du router en question.

Pour plus d'informations sur le profilage des pairs, consultez la [page Profilage et Sélection des Pairs](/docs/overview/peer-selection).

### Groupes de tunnels {#tunnel.pooling}

Pour permettre un fonctionnement efficace, le router maintient une série de pools de tunnels, chacun gérant un groupe de tunnels utilisés à des fins spécifiques avec leur propre configuration. Lorsqu'un tunnel est nécessaire pour cette fin, le router en sélectionne un au hasard dans le pool approprié. Globalement, il y a deux pools de tunnels exploratoires - un entrant et un sortant - chacun utilisant la configuration par défaut du router. De plus, il y a une paire de pools pour chaque destination locale - un pool de tunnels entrants et un pool de tunnels sortants. Ces pools utilisent la configuration spécifiée lorsque la destination locale se connecte au router via [I2CP](/docs/specs/i2cp), ou les paramètres par défaut du router si non spécifiés.

Chaque pool contient dans sa configuration quelques paramètres clés, définissant combien de tunnels maintenir actifs, combien de tunnels de sauvegarde conserver en cas de panne, quelle longueur les tunnels devraient avoir, si ces longueurs devraient être randomisées, ainsi que tous les autres paramètres autorisés lors de la configuration de tunnels individuels. Les options de configuration sont spécifiées sur la [page I2CP](/docs/specs/i2cp).

### Longueurs de tunnel et valeurs par défaut {#length}

[Sur la page de présentation des tunnels](/docs/overview/tunnel-routing#length).

### Stratégie et priorité de construction anticipée {#strategy}

La construction de tunnels est coûteuse, et les tunnels expirent à un moment fixe après leur construction. Cependant, quand un pool manque de tunnels, la Destination est essentiellement morte. De plus, le taux de succès de construction de tunnels peut varier considérablement selon les conditions du réseau local et global. Par conséquent, il est important de maintenir une stratégie de construction anticipatrice et adaptative pour s'assurer que de nouveaux tunnels sont construits avec succès avant d'en avoir besoin, sans construire un excès de tunnels, les construire trop tôt, ou consommer trop de CPU ou de bande passante en créant et envoyant les messages de construction chiffrés.

Pour chaque tuple {exploratoire/client, entrant/sortant, longueur, variance de longueur}, le router maintient des statistiques sur le temps nécessaire pour une construction de tunnel réussie. En utilisant ces statistiques, il calcule combien de temps avant l'expiration d'un tunnel il devrait commencer à tenter de construire un remplaçant. À l'approche du délai d'expiration sans remplacement réussi, il commence plusieurs tentatives de construction en parallèle, puis augmentera le nombre de tentatives parallèles si nécessaire.

Pour limiter la bande passante et l'utilisation du processeur, le router limite également le nombre maximum de tentatives de construction en cours sur tous les pools. Les constructions critiques (celles pour les tunnels exploratoires et pour les pools qui n'ont plus de tunnels) sont prioritaires.

## Limitation du débit des messages de tunnel {#tunnel.throttling}

Bien que les tunnels dans I2P ressemblent à un réseau à commutation de circuits, tout dans I2P est strictement basé sur les messages - les tunnels ne sont que des artifices comptables pour aider à organiser la livraison des messages. Aucune supposition n'est faite concernant la fiabilité ou l'ordonnancement des messages, et les retransmissions sont laissées aux niveaux supérieurs (par exemple la bibliothèque de streaming de la couche client d'I2P). Cela permet à I2P de tirer parti des techniques de limitation disponibles tant pour les réseaux à commutation de paquets que pour les réseaux à commutation de circuits. Par exemple, chaque router peut suivre la moyenne mobile de la quantité de données que chaque tunnel utilise, la combiner avec toutes les moyennes utilisées par les autres tunnels auxquels le router participe, et être capable d'accepter ou de rejeter des demandes de participation à des tunnels supplémentaires basées sur sa capacité et son utilisation. D'autre part, chaque router peut simplement abandonner les messages qui dépassent sa capacité, exploitant les recherches utilisées sur Internet normal.

Dans l'implémentation actuelle, les routers mettent en œuvre une stratégie de rejet précoce aléatoire pondéré (WRED). Pour tous les routers participants (participant interne, passerelle entrante et point de sortie sortant), le router commencera à abandonner de manière aléatoire une partie des messages lorsque les limites de bande passante sont approchées. À mesure que le trafic se rapproche ou dépasse les limites, davantage de messages sont abandonnés. Pour un participant interne, tous les messages sont fragmentés et complétés et ont donc la même taille. À la passerelle entrante et au point de sortie sortant, cependant, la décision d'abandon est prise sur le message complet (fusionné), et la taille du message est prise en compte. Les messages plus volumineux sont plus susceptibles d'être abandonnés. De plus, les messages sont plus susceptibles d'être abandonnés au point de sortie sortant qu'à la passerelle entrante, car ces messages ne sont pas aussi "avancés" dans leur parcours et donc le coût réseau de l'abandon de ces messages est plus faible.

## Travaux futurs {#future}

### Mélange/Regroupement {#tunnel.mixing}

Quelles stratégies pourraient être utilisées au niveau de la passerelle et à chaque hop pour retarder, réorganiser, rerouter ou ajouter du rembourrage aux messages ? Dans quelle mesure cela devrait-il être fait automatiquement, quelle part devrait être configurée comme paramètre par tunnel ou par hop, et comment le créateur du tunnel (et par extension, l'utilisateur) devrait-il contrôler cette opération ? Tout cela reste inconnu, à déterminer pour une version future lointaine.

### Remplissage

Les stratégies de remplissage peuvent être utilisées à différents niveaux, traitant l'exposition des informations de taille de message à différents adversaires. La taille fixe actuelle des messages de tunnel est de 1024 octets. Cependant, à l'intérieur de ceux-ci, les messages fragmentés eux-mêmes ne sont pas du tout remplis par le tunnel, bien que pour les messages de bout en bout, ils peuvent être remplis dans le cadre de l'encapsulation garlic.

### WRED

Les stratégies WRED ont un impact significatif sur les performances de bout en bout et la prévention de l'effondrement de la congestion réseau. La stratégie WRED actuelle devrait être soigneusement évaluée et améliorée.
