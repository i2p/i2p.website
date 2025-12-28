---
title: "Trackers UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Fermé"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
toc: true
---

## Statut

Approuvé lors de la révision du 24-06-2025. La spécification se trouve à [spécification UDP](/docs/specs/udp-bittorrent-announces/). Implémenté dans zzzot 0.20.0-beta2. Implémenté dans i2psnark à partir de l'API 0.9.67. Consultez la documentation des autres implémentations pour connaître leur statut.

## Aperçu

Cette proposition concerne l'implémentation des trackers UDP dans I2P.

### Change History

Une proposition préliminaire pour les trackers UDP dans I2P a été publiée sur notre [page de spécification bittorrent](/docs/applications/bittorrent/) en mai 2014 ; celle-ci précédait notre processus de proposition formel, et elle n'a jamais été implémentée. Cette proposition a été créée au début de 2022 et simplifie la version de 2014.

Comme cette proposition repose sur des datagrammes auxquels on peut répondre, elle a été mise en suspens une fois que nous avons commencé à travailler sur la [proposition Datagram2](/proposals/163-datagram2/) au début de 2023. Cette proposition a été approuvée en avril 2025.

La version 2023 de cette proposition spécifiait deux modes, "compatibilité" et "rapide". Une analyse plus approfondie a révélé que le mode rapide serait peu sûr, et serait également inefficace pour les clients avec un grand nombre de torrents. De plus, BiglyBT a indiqué une préférence pour le mode compatibilité. Ce mode sera plus facile à implémenter pour tout tracker ou client prenant en charge le standard [BEP 15](http://www.bittorrent.org/beps/bep_0015.html).

Bien que le mode de compatibilité soit plus complexe à implémenter from-scratch côté client, nous avons du code préliminaire pour cela commencé en 2023.

Par conséquent, la version actuelle ici est davantage simplifiée pour supprimer le mode rapide et retirer le terme « compatibilité ». La version actuelle passe au nouveau format Datagram2 et ajoute des références au protocole d'extension d'annonce UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

De plus, un champ de durée de vie d'ID de connexion est ajouté à la réponse de connexion, pour étendre les gains d'efficacité de ce protocole.

## Motivation

Alors que la base d'utilisateurs en général et le nombre d'utilisateurs bittorrent en particulier continuent de croître, nous devons rendre les trackers et les annonces plus efficaces afin que les trackers ne soient pas submergés.

Bittorrent a proposé les trackers UDP dans le BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) en 2008, et la grande majorité des trackers sur le clearnet sont maintenant exclusivement UDP.

Il est difficile de calculer les économies de bande passante des datagrammes par rapport au protocole de streaming. Une requête avec réponse possible fait à peu près la même taille qu'un SYN de streaming, mais la charge utile est environ 500 octets plus petite car le GET HTTP a une énorme chaîne de paramètres d'URL de 600 octets. La réponse brute est beaucoup plus petite qu'un SYN ACK de streaming, fournissant une réduction significative pour le trafic sortant d'un tracker.

De plus, il devrait y avoir des réductions de mémoire spécifiques à l'implémentation, car les datagrammes nécessitent beaucoup moins d'état en mémoire qu'une connexion en streaming.

Le chiffrement et les signatures post-quantiques tels qu'envisagés dans [/proposals/169-pq-crypto/](/proposals/169-pq-crypto/) augmenteront considérablement la surcharge des structures chiffrées et signées, y compris les destinations, leasesets, streaming SYN et SYN ACK. Il est important de minimiser cette surcharge dans la mesure du possible avant que la cryptographie PQ soit adoptée dans I2P.

## Motivation

Cette proposition utilise repliable datagram2, repliable datagram3, et raw datagrams, comme définis dans [/docs/api/datagrams/](/docs/api/datagrams/). Datagram2 et Datagram3 sont de nouvelles variantes de repliable datagrams, définies dans la Proposition 163 [/proposals/163-datagram2/](/proposals/163-datagram2/). Datagram2 ajoute une résistance contre la rejouabilité et le support de signature hors ligne. Datagram3 est plus petit que l'ancien format de datagram, mais sans authentification.

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
La phase de connexion est requise pour empêcher l'usurpation d'adresse IP. Le tracker retourne un ID de connexion que le client utilise dans les annonces subséquentes. Cet ID de connexion expire par défaut en une minute côté client, et en deux minutes côté tracker.

I2P utilisera le même flux de messages que BEP 15, pour faciliter l'adoption dans les bases de code client compatibles UDP existantes : pour l'efficacité, et pour les raisons de sécurité discutées ci-dessous :

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
Cela offre potentiellement des économies importantes de bande passante par rapport aux annonces en streaming (TCP). Bien que le Datagram2 soit de taille similaire à un SYN en streaming, la réponse brute est beaucoup plus petite qu'un SYN ACK en streaming. Les requêtes suivantes utilisent Datagram3, et les réponses suivantes sont brutes.

Les requêtes d'annonce sont des Datagram3 afin que le tracker n'ait pas besoin de maintenir une grande table de correspondance des ID de connexion vers la destination d'annonce ou le hachage. À la place, le tracker peut générer les ID de connexion de manière cryptographique à partir du hachage de l'expéditeur, de l'horodatage actuel (basé sur un certain intervalle), et d'une valeur secrète. Lorsqu'une requête d'annonce est reçue, le tracker valide l'ID de connexion, puis utilise le hachage de l'expéditeur Datagram3 comme cible d'envoi.

### Historique des modifications

Pour une application intégrée (router et client dans un seul processus, par exemple i2psnark, et le plugin Java ZzzOT), ou pour une application basée sur I2CP (par exemple BiglyBT), il devrait être simple d'implémenter et de router séparément le trafic streaming et datagram. ZzzOT et i2psnark devraient être les premiers tracker et client à implémenter cette proposition.

Les trackers et clients non intégrés sont abordés ci-dessous.

#### Trackers

Il existe quatre implémentations connues de tracker I2P :

- zzzot, un plugin router Java intégré, fonctionnant sur opentracker.dg2.i2p et plusieurs autres
- tracker2.postman.i2p, fonctionnant vraisemblablement derrière un router Java et un tunnel HTTP Server
- L'ancien opentracker C, porté par zzz, avec le support UDP commenté
- Le nouveau opentracker C, porté par r4sas, fonctionnant sur opentracker.r4sas.i2p et possiblement d'autres,
  fonctionnant vraisemblablement derrière un router i2pd et un tunnel HTTP Server

Pour une application tracker externe qui utilise actuellement un tunnel serveur HTTP pour recevoir les demandes d'annonce, l'implémentation pourrait être assez difficile. Un tunnel spécialisé pourrait être développé pour traduire les datagrammes en requêtes/réponses HTTP locales. Ou bien, un tunnel spécialisé qui gère à la fois les requêtes HTTP et les datagrammes pourrait être conçu pour transférer les datagrammes vers le processus externe. Ces décisions de conception dépendront fortement des implémentations spécifiques du router et du tracker, et sortent du cadre de cette proposition.

#### Clients

Les clients torrent externes basés sur SAM tels que qbittorrent et autres clients basés sur libtorrent nécessiteraient [SAM v3.3](/docs/api/samv3/) qui n'est pas pris en charge par i2pd. Ceci est également requis pour le support DHT, et est suffisamment complexe qu'aucun client torrent SAM connu ne l'a implémenté. Aucune implémentation basée sur SAM de cette proposition n'est attendue prochainement.

### Connection Lifetime

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) spécifie que l'ID de connexion expire en une minute côté client, et en deux minutes côté tracker. Ce n'est pas configurable. Cela limite les gains d'efficacité potentiels, sauf si les clients groupaient les annonces pour toutes les effectuer dans une fenêtre d'une minute. i2psnark ne groupe actuellement pas les annonces ; il les étale pour éviter les pics de trafic. Il est rapporté que les utilisateurs expérimentés font tourner des milliers de torrents simultanément, et concentrer autant d'annonces en une minute n'est pas réaliste.

Ici, nous proposons d'étendre la réponse de connexion pour ajouter un champ optionnel de durée de vie de connexion. La valeur par défaut, si elle n'est pas présente, est d'une minute. Sinon, la durée de vie spécifiée en secondes sera utilisée par le client, et le tracker maintiendra l'ID de connexion pendant une minute supplémentaire.

### Compatibility with BEP 15

Cette conception maintient la compatibilité avec [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) autant que possible pour limiter les modifications requises dans les clients et trackers existants.

Le seul changement requis est le format des informations de peer dans la réponse d'annonce. L'ajout du champ lifetime dans la réponse de connexion n'est pas obligatoire mais est fortement recommandé pour l'efficacité, comme expliqué ci-dessus.

### BEP 15

Un objectif important d'un protocole d'annonce UDP est d'empêcher l'usurpation d'adresse. Le client doit réellement exister et regrouper un vrai leaseset. Il doit avoir des tunnels entrants pour recevoir la réponse de connexion. Ces tunnels pourraient être à zéro saut et construits instantanément, mais cela exposerait le créateur. Ce protocole atteint cet objectif.

### Support Tracker/Client

- Cette proposition ne prend pas en charge les destinations masquées,
  mais peut être étendue pour le faire. Voir ci-dessous.

## Conception

### Protocols and Ports

Repliable Datagram2 utilise le protocole I2CP 19 ; repliable Datagram3 utilise le protocole I2CP 20 ; les datagrammes bruts utilisent le protocole I2CP 18. Les requêtes peuvent être Datagram2 ou Datagram3. Les réponses sont toujours brutes. L'ancien format de datagramme repliable ("Datagram1") utilisant le protocole I2CP 17 ne DOIT PAS être utilisé pour les requêtes ou les réponses ; ceux-ci doivent être abandonnés s'ils sont reçus sur les ports de requête/réponse. Notez que le protocole Datagram1 17 est toujours utilisé pour le protocole DHT.

Les requêtes utilisent le "to port" I2CP de l'URL d'annonce ; voir ci-dessous. Le "from port" de la requête est choisi par le client, mais doit être non nul, et un port différent de ceux utilisés par DHT, afin que les réponses puissent être facilement classifiées. Les trackers doivent rejeter les requêtes reçues sur le mauvais port.

Les réponses utilisent le "to port" I2CP de la requête. Le "from port" de la requête est le "to port" de la requête.

### Announce URL

Le format de l'URL d'annonce n'est pas spécifié dans [BEP 15](http://www.bittorrent.org/beps/bep_0015.html), mais comme sur le clearnet, les URL d'annonce UDP sont de la forme "udp://host:port/path". Le chemin est ignoré et peut être vide, mais est typiquement "/announce" sur le clearnet. La partie :port devrait toujours être présente, cependant, si la partie ":port" est omise, utilisez un port I2CP par défaut de 6969, car c'est le port commun sur le clearnet. Il peut également y avoir des paramètres cgi &a=b&c=d ajoutés, ceux-ci peuvent être traités et fournis dans la requête d'annonce, voir [BEP 41](http://www.bittorrent.org/beps/bep_0041.html). S'il n'y a pas de paramètres ou de chemin, le / final peut aussi être omis, comme sous-entendu dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

### Durée de Vie des Connexions

Toutes les valeurs sont envoyées dans l'ordre des octets réseau (big endian). Ne vous attendez pas à ce que les paquets aient exactement une taille donnée. Les extensions futures pourraient augmenter la taille des paquets.

#### Connect Request

Client vers tracker. 16 octets. Doit être un Datagram2 avec réponse possible. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Aucun changement.

```
Offset  Size            Name            Value
  0       64-bit integer  protocol_id     0x41727101980 // magic constant
  8       32-bit integer  action          0 // connect
  12      32-bit integer  transaction_id
```
#### Connect Response

Tracker vers client. 16 ou 18 octets. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf indication contraire ci-dessous.

```
Offset  Size            Name            Value
  0       32-bit integer  action          0 // connect
  4       32-bit integer  transaction_id
  8       64-bit integer  connection_id
  16      16-bit integer  lifetime        optional  // Change from BEP 15
```
La réponse DOIT être envoyée au « to port » I2CP qui a été reçu comme « from port » de la requête.

Le champ lifetime est optionnel et indique la durée de vie du connection_id client en secondes. La valeur par défaut est 60, et le minimum s'il est spécifié est 60. Le maximum est 65535 ou environ 18 heures. Le tracker devrait maintenir le connection_id pendant 60 secondes de plus que la durée de vie du client.

#### Announce Request

Client vers tracker. 98 octets minimum. Doit être un Datagram3 avec réponse possible. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf mention contraire ci-dessous.

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
  84      32-bit integer  IP address      0     // default
  88      32-bit integer  key
  92      32-bit integer  num_want        -1    // default
  96      16-bit integer  port
  98      varies          options     optional  // As specified in BEP 41
```
Changements par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) :

- key est ignoré
- port est probablement ignoré
- La section options, si présente, est définie comme dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La réponse DOIT être envoyée au "port de destination" I2CP qui a été reçu comme "port d'origine" de la requête. N'utilisez pas le port de la requête d'annonce.

#### Announce Response

Tracker vers client. 20 octets minimum. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sauf indication contraire ci-dessous.

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
Changements par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) :

- Au lieu de 6 octets IPv4+port ou 18 octets IPv6+port, nous retournons
  un multiple de « réponses compactes » de 32 octets avec les hachages binaires SHA-256 des pairs.
  Comme avec les réponses compactes TCP, nous n'incluons pas de port.

La réponse DOIT être envoyée au "port de destination" I2CP qui a été reçu comme "port source" de la demande. N'utilisez pas le port de la requête d'annonce.

Les datagrammes I2P ont une taille maximale très importante d'environ 64 Ko ; cependant, pour une livraison fiable, les datagrammes de plus de 4 Ko doivent être évités. Pour l'efficacité de la bande passante, les trackers devraient probablement limiter le nombre maximum de pairs à environ 50, ce qui correspond à un paquet d'environ 1600 octets avant les frais généraux des diverses couches, et devrait rester dans la limite de charge utile de deux messages tunnel après fragmentation.

Comme dans BEP 15, il n'y a pas de compteur inclus du nombre d'adresses de pairs (IP/port pour BEP 15, hashes ici) à suivre. Bien que cela ne soit pas envisagé dans BEP 15, un marqueur de fin de pairs composé uniquement de zéros pourrait être défini pour indiquer que les informations de pair sont complètes et que des données d'extension suivent.

Afin que l'extension soit possible à l'avenir, les clients doivent ignorer un hash de 32 octets composé uniquement de zéros, ainsi que toutes les données qui suivent. Les trackers doivent rejeter les annonces provenant d'un hash composé uniquement de zéros, bien que ce hash soit déjà banni par les routeurs Java.

#### Scrape

La demande/réponse scrape de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) n'est pas requise par cette proposition, mais peut être implémentée si souhaité, aucun changement requis. Le client doit d'abord acquérir un ID de connexion. La demande scrape est toujours un Datagram3 répondable. La réponse scrape est toujours brute.

#### Trackers

Tracker vers client. 8 octets minimum (si le message est vide). Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Aucun changement.

```
Offset  Size            Name            Value
  0       32-bit integer  action          3 // error
  4       32-bit integer  transaction_id
  8       string          message
```
## Extensions

Les bits d'extension ou un champ de version ne sont pas inclus. Les clients et trackers ne doivent pas présumer que les paquets font une certaine taille. De cette façon, des champs supplémentaires peuvent être ajoutés sans casser la compatibilité. Le format d'extensions défini dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) est recommandé si nécessaire.

La réponse de connexion est modifiée pour ajouter une durée de vie optionnelle de l'ID de connexion.

Si le support des destinations aveugles est requis, nous pouvons soit ajouter l'adresse aveugle de 35 octets à la fin de la requête d'annonce, soit demander des hachages aveugles dans les réponses, en utilisant le format [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (paramètres à déterminer). L'ensemble des adresses de pairs aveugles de 35 octets pourrait être ajouté à la fin de la réponse d'annonce, après un hachage de 32 octets composé uniquement de zéros.

## Implementation guidelines

Voir la section conception ci-dessus pour une discussion des défis pour les clients et trackers non intégrés, non-I2CP.

### Compatibilité avec BEP 15

Pour un nom d'hôte de tracker donné, un client devrait privilégier les URL UDP plutôt que HTTP, et ne devrait pas annoncer aux deux.

Les clients avec un support BEP 15 existant ne devraient nécessiter que de petites modifications.

Si un client prend en charge DHT ou d'autres protocoles de datagrammes, il devrait probablement sélectionner un port différent comme "port source" de la requête afin que les réponses reviennent sur ce port et ne soient pas mélangées avec les messages DHT. Le client ne reçoit que des datagrammes bruts comme réponses. Les trackers n'enverront jamais un datagram2 avec possibilité de réponse au client.

Les clients avec une liste par défaut d'opentrackers devraient mettre à jour la liste pour ajouter des URLs UDP après que les opentrackers connus soient reconnus comme supportant UDP.

Les clients peuvent ou non implémenter la retransmission des requêtes. Les retransmissions, si elles sont implémentées, devraient utiliser un délai d'attente initial d'au moins 15 secondes, et doubler le délai d'attente pour chaque retransmission (backoff exponentiel).

Les clients doivent reculer après avoir reçu une réponse d'erreur.

### Analyse de sécurité

Les trackers avec un support BEP 15 existant ne devraient nécessiter que de petites modifications. Cette proposition diffère de la proposition de 2014, en ce que le tracker doit supporter la réception de repliable datagram2 et datagram3 sur le même port.

Pour minimiser les exigences en ressources du tracker, ce protocole est conçu pour éliminer toute exigence que le tracker stocke les mappages des hachages clients vers les ID de connexion pour validation ultérieure. Ceci est possible car le paquet de requête d'annonce est un paquet Datagram3 auquel on peut répondre, il contient donc le hachage de l'expéditeur.

Une implémentation recommandée est :

- Définir l'époque actuelle comme le temps actuel avec une résolution de la durée de vie de la connexion,
  ``epoch = now / lifetime``.
- Définir une fonction de hachage cryptographique ``H(secret, clienthash, epoch)`` qui génère
  une sortie de 8 octets.
- Générer la constante aléatoire secrète utilisée pour toutes les connexions.
- Pour les réponses de connexion, générer ``connection_id = H(secret,  clienthash, epoch)``
- Pour les requêtes d'annonce, valider l'ID de connexion reçu dans l'époque actuelle en vérifiant
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``

## Migration

Les clients existants ne prennent pas en charge les URL d'annonce UDP et les ignorent.

Les trackers existants ne prennent pas en charge la réception de datagrammes répondables ou bruts, ils seront abandonnés.

Cette proposition est complètement optionnelle. Ni les clients ni les trackers ne sont tenus de l'implémenter à quelque moment que ce soit.

## Rollout

Les premières implémentations sont attendues dans ZzzOT et i2psnark. Elles seront utilisées pour tester et vérifier cette proposition.

D'autres implémentations suivront selon les besoins après que les tests et la vérification soient terminés.
