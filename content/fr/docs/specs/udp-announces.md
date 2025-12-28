---
title: "Annonces BitTorrent via UDP"
description: "Spécification du protocole pour les annonces du tracker BitTorrent basées sur UDP dans I2P"
slug: "udp-announces"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

Cette spécification documente le protocole des annonces BitTorrent en UDP dans I2P. Pour la spécification générale de BitTorrent dans I2P, voir la [documentation BitTorrent sur I2P](/docs/applications/bittorrent/). Pour le contexte et des informations supplémentaires sur le développement de cette spécification, voir la [Proposition 160](/proposals/160-udp-trackers/).

Ce protocole a été formellement approuvé le 24 juin 2025 et implémenté dans la version 2.10.0 d'I2P (API 0.9.67), publiée le 8 septembre 2025. La prise en charge des trackers UDP est actuellement opérationnelle sur le réseau I2P, avec plusieurs trackers en production et une prise en charge complète du client i2psnark.

## Conception

Cette spécification utilise repliable datagram2, repliable datagram3 et des raw datagrams (datagrammes bruts), tels que définis dans la [Spécification des datagrammes I2P](/docs/api/datagrams/). Datagram2 et Datagram3 sont des variantes de repliable datagrams (datagrammes permettant la réponse), définies dans la [Proposition 163](/proposals/163-datagram2/). Datagram2 ajoute une résistance au rejeu et la prise en charge des signatures hors ligne. Datagram3 est plus petit que l’ancien format de datagramme, mais sans authentification.

### BEP 15

Pour référence, le flux de messages défini dans [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) est le suivant :

```
Client                        Tracker
  Connect Req. ------------->
    <-------------- Connect Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
  Announce Req. ------------->
    <-------------- Announce Resp.
```
La phase de connexion est requise pour empêcher l’usurpation d’adresse IP. Le tracker renvoie un identifiant de connexion que le client utilise dans les annonces suivantes. Cet identifiant de connexion expire par défaut au bout d’une minute côté client, et au bout de deux minutes côté tracker.

I2P utilise le même flux de messages que BEP 15 (proposition d’amélioration BitTorrent 15), afin de faciliter l’adoption dans des bases de code de clients existantes prenant en charge l’UDP, par souci d’efficacité, et pour des raisons de sécurité exposées ci-dessous:

```
Client                        Tracker
  Connect Req. ------------->       (Repliable Datagram2)
    <-------------- Connect Resp.   (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
  Announce Req. ------------->      (Repliable Datagram3)
    <-------------- Announce Resp.  (Raw)
           ...
```
Cela peut offrir une économie de bande passante importante par rapport aux annonces en streaming (TCP). Bien que le Datagram2 (datagramme 2) ait à peu près la même taille qu’un SYN en streaming, la réponse brute est bien plus petite que le SYN ACK en streaming. Les requêtes ultérieures utilisent Datagram3 (datagramme 3), et les réponses ultérieures sont brutes.

Les requêtes d’annonce sont des Datagram3 afin que le tracker (serveur de suivi) n’ait pas à maintenir une grande table de correspondance d’ID de connexion vers la destination ou le hachage d’annonce. À la place, le tracker peut générer des ID de connexion cryptographiquement à partir du hachage de l’expéditeur, de l’horodatage actuel (basé sur un certain intervalle) et d’une valeur secrète. Lorsqu’une requête d’annonce est reçue, le tracker valide l’ID de connexion, puis utilise le hachage d’expéditeur Datagram3 comme cible d’envoi.

### Durée de vie de la connexion

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) spécifie que l’ID de connexion expire au bout d’une minute côté client, et au bout de deux minutes côté tracker. Ce n’est pas configurable. Cela limite les gains d’efficacité potentiels, à moins que les clients ne regroupent les announces (requêtes d’annonce au tracker) pour les effectuer toutes dans une fenêtre d’une minute. i2psnark ne regroupe actuellement pas les announces ; il les échelonne afin d’éviter des pics de trafic. Il est rapporté que des utilisateurs avancés exécutent des milliers de torrents simultanément, et regrouper autant d’announces dans une minute n’est pas réaliste.

Ici, nous proposons d’étendre la réponse de connexion afin d’ajouter un champ facultatif de durée de vie de la connexion. Par défaut, si ce champ est absent, la durée de vie est d’une minute. Sinon, la durée spécifiée en secondes doit être utilisée par le client, et le tracker maintiendra l’ID de connexion pendant une minute supplémentaire.

### Compatibilité avec le BEP 15

Cette conception préserve autant que possible la compatibilité avec [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) afin de limiter les modifications requises dans les clients et les trackers (serveurs de suivi) existants.

La seule modification requise concerne le format des informations sur les pairs dans la réponse d’annonce. L’ajout du champ de durée de vie dans la réponse de connexion n’est pas obligatoire, mais il est fortement recommandé pour des raisons d’efficacité, comme expliqué ci-dessus.

### Analyse de sécurité

Un objectif important d’un protocole d’annonce UDP est d’empêcher l’usurpation d’adresse. Le client doit réellement exister et inclure un véritable leaseSet. Il doit disposer de tunnels entrants pour recevoir la Connect Response (réponse de connexion). Ces tunnels pourraient être zero-hop (sans relais) et être construits instantanément, mais cela exposerait le créateur. Ce protocole atteint cet objectif.

### Problèmes

Ce protocole ne prend pas en charge les blinded destinations (destinations aveuglées), mais pourrait être étendu pour les prendre en charge. Voir ci-dessous.

## Spécification

### Protocoles et ports

Datagram2 repliable (permettant une réponse) utilise le protocole I2CP 19; Datagram3 repliable utilise le protocole I2CP 20; les datagrammes bruts utilisent le protocole I2CP 18. Les requêtes peuvent être en Datagram2 ou Datagram3. Les réponses sont toujours brutes. L'ancien format de datagramme repliable ("Datagram1") utilisant le protocole I2CP 17 ne doit PAS être utilisé pour les requêtes ou les réponses; ceux-ci doivent être rejetés s'ils sont reçus sur les ports de requête/réponse. Notez que le protocole Datagram1 17 est toujours utilisé pour le protocole DHT.

Les requêtes utilisent le "port de destination" I2CP indiqué dans l’URL d’annonce ; voir ci-dessous. Le "port source" de la requête est choisi par le client, mais devrait être non nul et différent des ports utilisés par la DHT, afin que les réponses puissent être facilement classées. Les trackers devraient rejeter les requêtes reçues sur le mauvais port.

Les réponses utilisent le "to port" I2CP de la requête (port de destination). Le "from port" de la réponse (port source) est le "to port" de la requête.

### URL d'annonce

Le format de l’URL d’annonce n’est pas spécifié dans [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), mais, comme sur le clearnet (Internet public), les URL d’annonce UDP sont de la forme "udp://host:port/path". Le chemin est ignoré et peut être vide, mais il est généralement "/announce" sur le clearnet. La partie :port devrait toujours être présente ; toutefois, si la partie ":port" est omise, utilisez un port I2CP par défaut de 6969, car c’est le port usuel sur le clearnet. Il peut aussi y avoir des paramètres CGI &a=b&c=d ajoutés ; ceux-ci peuvent être traités et fournis dans la requête d’annonce, voir [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). S’il n’y a ni paramètres ni chemin, le '/' final peut aussi être omis, comme l’implique [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Formats de datagrammes

Toutes les valeurs sont envoyées en ordre d’octets réseau (big endian, octet de poids fort en premier). Ne vous attendez pas à ce que les paquets aient exactement une taille donnée. De futures extensions pourraient augmenter la taille des paquets.

#### Demande de connexion

Client vers le tracker. 16 octets. Doit être un Datagram2 repliable (permettant la réponse). Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Aucun changement.

```
Offset  Size            Name            Value
0       64-bit integer  protocol_id     0x41727101980 // magic constant
8       32-bit integer  action          0 // connect
12      32-bit integer  transaction_id
```
#### Réponse de connexion

Du tracker vers le client. 16 ou 18 octets. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf comme indiqué ci-dessous.

```
Offset  Size            Name            Value
0       32-bit integer  action          0 // connect
4       32-bit integer  transaction_id
8       64-bit integer  connection_id
16      16-bit integer  lifetime        optional  // Change from BEP 15
```
La réponse DOIT être envoyée vers le "to port" I2CP reçu en tant que "from port" dans la requête.

Le champ lifetime est facultatif et indique, en secondes, la durée de vie du client associée au connection_id. La valeur par défaut est 60, et la valeur minimale, si elle est spécifiée, est 60. La valeur maximale est 65535, soit environ 18 heures. Le tracker (serveur de suivi) devrait conserver le connection_id pendant 60 secondes de plus que la durée de vie du client.

#### Requête d’annonce

Client vers le tracker. 98 octets minimum. Doit être un Datagram3 (datagramme v3) pouvant recevoir une réponse. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf mention contraire ci-dessous.

Le connection_id est tel que reçu dans la réponse de connexion.

```
Offset  Size            Name            Value
0       64-bit integer  connection_id
8       32-bit integer  action          1     // announce
12      32-bit integer  transaction_id
16      20-byte string  info_hash
36      20-byte string  peer_id
56      64-bit integer  downloaded
64      64-bit integer  left
72      64-bit integer  uploaded
80      32-bit integer  event           0     // 0: none; 1: completed; 2: started; 3: stopped
84      32-bit integer  IP address      0     // default, unused in I2P
88      32-bit integer  key
92      32-bit integer  num_want        -1    // default
96      16-bit integer  port                  // must be same as I2CP from port
98      varies          options     optional  // As specified in BEP 41
```
Modifications par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html):

- la clé est ignorée
- l'adresse IP n'est pas utilisée
- le port est probablement ignoré, mais doit être identique au port source I2CP
- la section des options, si présente, est telle que définie dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La réponse DOIT être envoyée au "to port" I2CP qui a été reçu en tant que "from port" de la requête. N'utilisez pas le port de la requête d'annonce.

#### Réponse d'annonce

Du tracker au client. 20 octets minimum. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf comme indiqué ci-dessous.

```
Offset  Size            Name            Value
0           32-bit integer  action          1 // announce
4           32-bit integer  transaction_id
8           32-bit integer  interval
12          32-bit integer  leechers
16          32-bit integer  seeders
20   32 * n 32-byte hash    binary hashes     // Change from BEP 15
...                                           // Change from BEP 15
```
Modifications par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) :

- Au lieu d’un IPv4+port de 6 octets ou d’un IPv6+port de 18 octets, nous renvoyons une séquence de "réponses compactes" de 32 octets contenant les hachages binaires SHA-256 des pairs. Comme pour les réponses compactes TCP, nous n’incluons pas de port.

La réponse DOIT être envoyée au "to port" I2CP qui a été reçu comme "from port" de la requête. N'utilisez pas le port de la requête d'annonce.

Les datagrammes I2P ont une taille maximale très élevée, d’environ 64 Ko ; toutefois, pour un acheminement fiable, il convient d’éviter les datagrammes de plus de 4 Ko. Pour optimiser l’utilisation de la bande passante, les trackers devraient probablement limiter le nombre maximal de pairs à environ 50, ce qui correspond à un paquet d’environ 1 600 octets avant la surcharge introduite par les différentes couches, et devrait rester dans la limite de charge utile équivalente à deux messages tunnel après fragmentation.

Comme dans le BEP 15, aucun décompte du nombre d’adresses de pairs (IP/port pour le BEP 15, des hachages ici) à venir n’est inclus. Bien que non prévu par le BEP 15, on pourrait définir un marqueur de fin de liste de pairs tout à zéro pour indiquer que les informations sur les pairs sont complètes et que des données d’extension suivent.

Afin de permettre cette extension à l'avenir, les clients devraient ignorer un hachage de 32 octets composé uniquement de zéros, ainsi que toutes les données qui suivent. Les trackers devraient rejeter les requêtes d'annonce utilisant un hachage tout en zéros, bien que ce hachage soit déjà banni par les Java routers.

#### Extraction de données (scrape)

La requête/réponse scrape (interrogation du tracker) de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) n’est pas requise par cette spécification, mais peut être mise en œuvre si souhaité, sans nécessiter de modifications. Le client doit d’abord obtenir un identifiant de connexion. La requête scrape est toujours un Datagram3 repliable (auquel on peut répondre). La réponse scrape est toujours raw (brut).

#### Réponse d'erreur

Du tracker au client. 8 octets minimum (si le message est vide). Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Aucun changement.

```
Offset  Size            Name            Value
0       32-bit integer  action          3 // error
4       32-bit integer  transaction_id
8       string          message
```
## Extensions

Les bits d’extension ou un champ de version ne sont pas inclus. Les clients et les trackers ne devraient pas supposer que les paquets ont une taille déterminée. Ainsi, des champs supplémentaires peuvent être ajoutés sans compromettre la compatibilité. Le format d’extensions défini dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) est recommandé si nécessaire.

La réponse de connexion est modifiée pour ajouter une durée de vie optionnelle pour l’identifiant de connexion.

Si la prise en charge des destinations aveuglées est requise, nous pouvons soit ajouter l’adresse aveuglée de 35 octets à la fin de la requête d’annonce, soit demander des hachages aveuglés dans les réponses, en utilisant le format [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (paramètres à définir). L’ensemble des adresses de pairs aveuglées de 35 octets pourrait être ajouté à la fin de la réponse d’annonce, après un hachage de 32 octets composé uniquement de zéros.

## Directives de mise en œuvre

Voir la section de conception ci-dessus pour une discussion des défis liés aux clients non intégrés, non I2CP, et aux trackers.

### Clients

Pour un nom d'hôte de tracker donné, un client devrait préférer les URL UDP aux URL HTTP, et ne devrait pas s'annoncer aux deux.

Les clients prenant déjà en charge BEP 15 ne devraient nécessiter que de légères modifications.

Si un client prend en charge la DHT ou d'autres protocoles de datagrammes, il devrait probablement choisir un port différent comme "from port" (port source) de la requête, afin que les réponses reviennent sur ce port et ne se confondent pas avec les messages DHT. Le client ne reçoit que des datagrammes bruts en réponse. Les trackers n'enverront jamais au client un datagram2 répliable.

Les clients disposant d’une liste par défaut d’opentrackers (trackers ouverts) devraient mettre cette liste à jour pour y ajouter des URL UDP après confirmation que les opentrackers connus prennent en charge UDP.

Les clients peuvent ou non implémenter la retransmission des requêtes. Les retransmissions, si elles sont mises en œuvre, devraient utiliser un délai d’expiration initial d’au moins 15 secondes et doubler ce délai à chaque retransmission (exponential backoff (attente exponentielle)).

Les clients doivent attendre avant de réessayer après avoir reçu une réponse d’erreur.

### Serveurs de suivi

Les trackers (serveurs de suivi BitTorrent) prenant déjà en charge BEP 15 ne devraient nécessiter que des modifications mineures. Cette spécification diffère de la proposition de 2014, en ce que le tracker doit prendre en charge la réception de datagram2 et datagram3 répliables sur le même port.

Pour minimiser les ressources nécessaires côté tracker, ce protocole est conçu pour supprimer toute nécessité pour le tracker de stocker des correspondances entre les hachages des clients et les identifiants de connexion en vue d’une validation ultérieure. Ceci est possible parce que le paquet de requête announce (requête d’annonce) est un paquet Datagram3 permettant la réponse, et il contient donc le hachage de l’expéditeur.

Une implémentation recommandée est :

- Définir l'époque actuelle comme le temps actuel avec une résolution égale à la durée de vie de la connexion, `epoch = now / lifetime`.
- Définir une fonction de hachage cryptographique `H(secret, clienthash, epoch)` qui génère une sortie de 8 octets.
- Générer le secret constant aléatoire utilisé pour toutes les connexions.
- Pour les réponses de connexion, générer `connection_id = H(secret, clienthash, epoch)`
- Pour les requêtes d'annonce, valider l'ID de connexion reçu pour l'époque actuelle en vérifiant `connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)`

## Statut du déploiement

Ce protocole a été approuvé le 24 juin 2025 et est entièrement opérationnel sur le réseau I2P depuis septembre 2025.

### Implémentations actuelles

**i2psnark**: La prise en charge complète des traqueurs UDP est intégrée à I2P version 2.10.0 (API 0.9.67), publiée le 8 septembre 2025. Toutes les installations d'I2P à partir de cette version incluent par défaut la prise en charge des traqueurs UDP.

**zzzot tracker**: À partir de la version 0.20.0-beta2, les annonces UDP sont prises en charge. En octobre 2025, les trackers de production suivants sont opérationnels: - opentracker.dg2.i2p - opentracker.simp.i2p - opentracker.skank.i2p

### Notes de compatibilité pour les clients

**Limitations de SAM v3.3**: Les clients BitTorrent externes utilisant SAM (Simple Anonymous Messaging, messagerie anonyme simple) nécessitent la prise en charge de SAM v3.3 pour Datagram2/3. Ceci est disponible dans Java I2P mais n'est pas actuellement pris en charge par i2pd (l'implémentation I2P en C++), ce qui peut limiter l'adoption dans les clients basés sur libtorrent comme qBittorrent.

**Clients I2CP**: Les clients utilisant I2CP directement (comme BiglyBT) peuvent implémenter la prise en charge du tracker UDP sans les limitations de SAM.

## Références

- **[BEP15]**: [Protocole du tracker UDP de BitTorrent](http://www.bittorrent.org/beps/bep_0015.html)
- **[BEP41]**: [Extensions du protocole du tracker UDP](http://www.bittorrent.org/beps/bep_0041.html)
- **[DATAGRAMS]**: [Spécification des datagrammes I2P](/docs/api/datagrams/)
- **[Prop160]**: [Proposition relative aux trackers UDP](/proposals/160-udp-trackers/)
- **[Prop163]**: [Proposition Datagram2](/proposals/163-datagram2/)
- **[SPEC]**: [BitTorrent sur I2P](/docs/applications/bittorrent/)
