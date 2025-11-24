```markdown
---
title: "Trackers UDP"
number: "160"
author: "zzz"
created: "2022-01-03"
lastupdated: "2025-06-25"
status: "Fermé"
thread: "http://zzz.i2p/topics/1634"
target: "0.9.67"
---

## Statut

Approuvé lors de la revue du 2025-06-24.
La spécification est disponible à [UDP specification](/en/docs/spec/udp-bittorrent-announces/).
Implémenté dans zzzot 0.20.0-beta2.
Implémenté dans i2psnark à partir de l'API 0.9.67.
Vérifiez la documentation d'autres implémentations pour connaître le statut.


## Aperçu

Cette proposition concerne l'implémentation des trackers UDP dans I2P.


### Historique des changements

Une proposition préliminaire pour les trackers UDP dans I2P a été publiée sur notre page de spécification bittorrent [/en/docs/applications/bittorrent/](/en/docs/applications/bittorrent/)
en mai 2014 ; cela a précédé notre processus formel de proposition, et elle n'a jamais été implémentée.
Cette proposition a été créée début 2022 et simplifie la version de 2014.

Comme cette proposition repose sur des datagrammes réplicitables, elle a été mise en attente une fois que nous
avons commencé à travailler sur la proposition Datagram2 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/) début 2023.
Cette proposition a été approuvée en avril 2025.

La version 2023 de cette proposition spécifiait deux modes, "compatibilité" et "rapide".
Une analyse plus approfondie a révélé que le mode rapide serait peu sûr et également
inefficace pour les clients avec un grand nombre de torrents.
De plus, BiglyBT a indiqué une préférence pour le mode compatibilité.
Ce mode sera plus facile à implémenter pour tout tracker ou client supportant
[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) standard.

Bien que le mode compatibilité soit plus complexe à implémenter de zéro côté client,
nous avons un code préliminaire pour cela commencé en 2023.

Par conséquent, la version actuelle ici est encore simplifiée pour supprimer le mode rapide,
et supprimer le terme "compatibilité". La version actuelle passe au
nouveau format Datagram2, et ajoute des références au protocole d'extension d'annonce UDP [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).

De plus, un champ de durée de vie de l'identifiant de connexion est ajouté à la réponse de connexion,
pour augmenter les gains d'efficacité de ce protocole.


## Motivation

Alors que la base d'utilisateurs en général et le nombre d'utilisateurs bittorrent en particulier continuent de croître,
nous devons rendre les trackers et les annonces plus efficaces afin que les trackers ne soient pas submergés.

Bittorrent a proposé des trackers UDP dans BEP 15 [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) en 2008, et la grande majorité
des trackers sur clearnet sont maintenant exclusivement UDP.

Il est difficile de calculer les économies de bande passante des datagrammes par rapport au protocole de streaming.
Une demande réplicable est d'environ la même taille qu'un streaming SYN, mais la charge utile
est environ 500 octets plus petite car le GET HTTP a une longue chaîne de paramètres URL de 600 octets.
La réponse brute est beaucoup plus petite qu'un ACK SYN en streaming, offrant une réduction significative
pour le trafic sortant d'un tracker.

De plus, il devrait y avoir des réductions de mémoire spécifiques à l'implémentation,
car les datagrammes nécessitent beaucoup moins d'état en mémoire qu'une connexion en streaming.

Le chiffrement et les signatures post-quantum tels qu'envisagés dans [/en/proposals/169-pq-crypto/](/en/proposals/169-pq-crypto/) augmenteront considérablement
le surcoût des structures chiffrées et signées, y compris les destinations, les leasesets, les SYN et SYN ACK en streaming. Il est important de minimiser ce
surcoût autant que possible avant que la crypto PQ ne soit adoptée dans I2P.


## Conception

Cette proposition utilise des datagrammes réplicables datagram2, datagram3 réplicables et des datagrammes bruts,
comme défini dans [/en/docs/spec/datagrams/](/en/docs/spec/datagrams/).
Datagram2 et Datagram3 sont de nouvelles variantes de datagrammes réplicables,
définis dans la Proposition 163 [/en/proposals/163-datagram2/](/en/proposals/163-datagram2/).
Datagram2 ajoute une résistance à la relecture et un support de signature hors ligne.
Datagram3 est plus petit que l'ancien format de datagrammes, mais sans authentification.


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

La phase de connexion est requise pour empêcher le spoofing d'adresses IP.
Le tracker renvoie un identifiant de connexion que le client utilise dans les annonces suivantes.
Cet identifiant de connexion expire par défaut en une minute chez le client, et en deux minutes chez le tracker.

I2P utilisera le même flux de messages que BEP 15,
pour facilité d'adoption dans les bases de code client existantes compatibles UDP :
pour l'efficacité, et pour des raisons de sécurité discutées ci-dessous :

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

Cela offre potentiellement de grandes économies de bande passante par rapport aux
annonces en streaming (TCP).
Alors que le Datagram2 est à peu près de la même taille qu'un SYN en streaming,
la réponse brute est beaucoup plus petite que le SYN ACK en streaming.
Les demandes suivantes utilisent Datagram3, et les réponses suivantes sont brutes.

Les demandes d'annonce sont des Datagram3 afin que le tracker n'ait pas besoin
de maintenir une grande table de correspondance des identifiants de connexion à l'adresse de destination ou au hachage de l'annonce.
Au lieu de cela, le tracker peut générer des identifiants de connexion de manière cryptographique
à partir du hachage de l'expéditeur, du timestamp actuel (basé sur un certain intervalle),
et d'une valeur secrète.
Lorsqu'une demande d'annonce est reçue, le tracker valide l'identifiant de connexion,
puis utilise le hachage de l'expéditeur Datagram3 comme cible d'envoi.


### Support Tracker/Client

Pour une application intégrée (routeur et client dans un seul processus, par exemple i2psnark, et le plugin Java ZzzOT),
ou pour une application basée sur I2CP (par exemple BiglyBT),
il devrait être simple de mettre en œuvre et de router séparément le trafic de streaming et de datagrammes.
ZzzOT et i2psnark devraient être le premier tracker et client à implémenter cette proposition.

Les trackers et clients non intégrés sont discutés ci-dessous.


Trackers
````````

Il existe quatre implémentations de trackers I2P connues :

- zzzot, un plugin routeur Java intégré, fonctionnant sur opentracker.dg2.i2p et plusieurs autres
- tracker2.postman.i2p, fonctionnant vraisemblablement derrière un tunnel routeur et HTTP Server Java
- L'ancien C opentracker, porté par zzz, avec le support UDP commenté
- Le nouveau C opentracker, porté par r4sas, fonctionnant sur opentracker.r4sas.i2p et potentiellement d'autres,
  fonctionnant vraisemblablement derrière un routeur i2pd et un tunnel HTTP Server

Pour une application de tracker externe qui utilise actuellement un tunnel serveur HTTP pour recevoir
les demandes d'annonce, l'implémentation pourrait être assez difficile.
Un tunnel spécialisé pourrait être développé pour transformer les datagrammes en requêtes/réponses HTTP locales.
Ou bien, un tunnel spécialisé gérant à la fois les requêtes HTTP et les datagrammes pourrait être conçu
pour rediriger les datagrammes vers le processus externe.
Ces décisions de conception dépendront fortement des implémentations spécifiques du routeur et du tracker,
et sont hors du cadre de cette proposition.


Clients
```````
Les clients torrent externes basés sur SAM tels que qbittorrent et d'autres clients basés sur libtorrent
nécessiteraient SAM v3.3 [/en/docs/api/samv3/](/en/docs/api/samv3/) qui n'est pas pris en charge par i2pd.
Cela est également requis pour le support DHT, et est assez complexe pour qu'aucun client torrent
basé sur SAM connu ne l'ait implémenté.
Aucune implémentation basée sur SAM de cette proposition n'est attendue prochainement.


### Durée de vie de la connexion

[BEP 15](http://www.bittorrent.org/beps/bep_0015.html) spécifie que l'identifiant de connexion expire en une minute chez le client, et en deux minutes chez le tracker.
Ce n'est pas configurable.
Cela limite les gains potentiels d'efficacité, sauf si
les clients regroupent les annonces pour les faire toutes dans une fenêtre d'une minute.
i2psnark ne regroupe actuellement pas les annonces ; il les échelonne, pour éviter les pics de trafic.
Des utilisateurs intensifs seraient signalés pour exécuter des milliers de torrents à la fois,
et il n'est pas réaliste de regrouper autant d'annonces en une minute.

Ici, nous proposons d'étendre la réponse de connexion pour ajouter un champ optionnel de durée de vie de l'identifiant de connexion.
Le défaut, s'il n'est pas présent, est d'une minute. Sinon, la durée de vie spécifiée
en secondes, sera utilisée par le client, et le tracker maintiendra l'identifiant
pour une minute de plus.


### Compatibilité avec BEP 15

Cette conception maintient autant que possible la compatibilité avec [BEP 15](http://www.bittorrent.org/beps/bep_0015.html)
pour limiter les changements requis dans les clients et trackers existants.

Le seul changement requis est le format des informations de pair dans la réponse d'annonce.
L'ajout du champ de durée de vie dans la réponse de connexion n'est pas requis
mais est fortement recommandé pour l'efficacité, comme expliqué ci-dessus.



### Analyse de sécurité

Un objectif important d'un protocole d'annonce UDP est de prévenir le spoofing d'adresses.
Le client doit exister réellement et regrouper un vrai leaseset.
Il doit avoir des tunnels entrants pour recevoir la réponse de connexion.
Ces tunnels pourraient être zéro-hop et construire instantanément, mais cela exposerait le créateur.
Ce protocole accomplit cet objectif.



### Problèmes

- Cette proposition ne prend pas en charge les destinations aveuglées,
  mais peut être étendue pour le faire. Voir ci-dessous.




## Spécification

### Protocoles et Ports

Repliable Datagram2 utilise le protocole I2CP 19 ;
repliable Datagram3 utilise le protocole I2CP 20 ;
les datagrammes bruts utilisent le protocole I2CP 18.
Les demandes peuvent être Datagram2 ou Datagram3. Les réponses sont toujours brutes.
Le format de datagramme répliquable plus ancien ("Datagram1") utilisant le protocole I2CP 17
ne doit PAS être utilisé pour les demandes ou les réponses ; ceux-ci doivent être rejetés s'ils sont reçus
sur les ports de demande/réponse. Notez que le protocole Datagram1 17
est toujours utilisé pour le protocole DHT.

Les demandes utilisent le "to port" I2CP de l'URL de l'annonce ; voir ci-dessous.
Le "from port" de la demande est choisi par le client, mais doit être non nul,
et un port différent de ceux utilisés par DHT, de sorte que les réponses
puissent être facilement classifiées.
Les trackers doivent rejeter les demandes reçues sur le mauvais port.

Les réponses utilisent le "to port" I2CP de la demande.
Le "from port" de la demande est le "to port" de la demande.


### URL de l'annonce

Le format de l'URL de l'annonce n'est pas spécifié dans [BEP 15](http://www.bittorrent.org/beps/bep_0015.html),
mais comme sur clearnet, les URL d'annonce UDP sont de la forme "udp://host:port/path".
Le chemin est ignoré et peut être vide, mais est généralement "/announce" sur clearnet.
La partie :port devrait toujours être présente, cependant,
si la partie ":port" est omise, utilisez un port I2CP par défaut de 6969,
car c'est le port commun sur clearnet.
Il peut également y avoir des paramètres cgi &a=b&c=d ajoutés,
ceux-ci peuvent être traités et fournis dans la demande d'annonce, voir [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).
S'il n'y a pas de paramètres ou de chemin, le / final peut également être omis,
comme cela est impliqué dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html).


### Formats de Datagramme

Toutes les valeurs sont envoyées en ordre d'octets réseau (big endian).
Ne vous attendez pas à ce que les paquets aient exactement une certaine taille.
Les extensions futures pourraient augmenter la taille des paquets.



Demande de connexion
`````````````````````

Client au tracker.
16 octets. Doit être un Datagram2 répliquable. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Pas de changements.


```
Offset  Taille          Nom              Valeur
  0       Entier 64 bits  protocol_id     0x41727101980 // constante magique
  8       Entier 32 bits  action          0 // connecter
  12      Entier 32 bits  transaction_id
```



Réponse de connexion
````````````````````

Tracker au client.
16 ou 18 octets. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepté comme indiqué ci-dessous.


```
Offset  Taille          Nom              Valeur
  0       Entier 32 bits  action          0 // connecter
  4       Entier 32 bits  transaction_id
  8       Entier 64 bits  connection_id
  16      Entier 16 bits  lifetime        optionnel  // Changement de BEP 15
```

La réponse DOIT être envoyée au "to port" I2CP qui a été reçu comme le "from port" de la demande.

Le champ duration est optionnel et indique la durée de vie client de connection_id en secondes.
La valeur par défaut est 60, et le minimum si spécifié est 60.
Le maximum est 65535 ou environ 18 heures.
Le tracker doit maintenir connection_id pendant 60 secondes de plus que la durée de vie client.



Demande d'annonce
``````````````````

Client au tracker.
98 octets minimum. Doit être un Datagram3 répliquable. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepté comme indiqué ci-dessous.

Connection_id est tel que reçu dans la réponse de connexion.



```
Offset  Taille          Nom              Valeur
  0       Entier 64 bits  connection_id
  8       Entier 32 bits  action          1     // annoncer
  12      Entier 32 bits  transaction_id
  16      Chaîne de 20 octets  info_hash
  36      Chaîne de 20 octets  peer_id
  56      Entier 64 bits  téléchargé
  64      Entier 64 bits  restant
  72      Entier 64 bits  téléchargé
  80      Entier 32 bits  événement          0     // 0: aucun ; 1: terminé ; 2: commencé ; 3: arrêté
  84      Entier 32 bits  Adresse IP      0     // défaut
  88      Entier 32 bits  clé
  92      Entier 32 bits  num_want        -1    // défaut
  96      Entier 16 bits  port
  98      varie           options     optionnel  // Tel que spécifié dans BEP 41
```

Changements par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) :

- clé est ignorée
- port est probablement ignoré
- La section options, si présente, est telle que définie dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html)

La réponse DOIT être envoyée au "to port" I2CP qui a été reçu comme le "from port" de la demande.
Ne pas utiliser le port de la demande d'annonce.



Réponse d'annonce
`````````````````

Tracker au client.
20 octets minimum. Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) excepté comme indiqué ci-dessous.



```
Offset  Taille          Nom              Valeur
  0          Entier 32 bits  action          1 // annoncer
  4          Entier 32 bits  transaction_id
  8          Entier 32 bits  intervalle
  12         Entier 32 bits  leecheurs
  16         Entier 32 bits  seeders
  20  32 * n Chaîne de hachage de 32 octets hachages binaires     // Changement de BEP 15
  ...                                           // Changement de BEP 15
```

Changements par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) :

- Au lieu des adresses IP de 6 octets + port pour IPv4 ou de 18 octets pour IPv6 + port, nous retournons
  un multiple de réponses "compactes" de 32 octets avec les hachages binaires SHA-256 des pairs.
  Comme avec les réponses compactes TCP, nous n'incluons pas de port.

La réponse DOIT être envoyée au "to port" I2CP qui a été reçu comme le "from port" de la demande.
Ne pas utiliser le port de la demande d'annonce.

Les datagrammes I2P ont une taille maximale très grande d'environ 64 Ko ;
toutefois, pour une livraison fiable, les datagrammes de plus de 4 Ko devraient être évités.
Pour l'efficacité de la bande passante, les trackers devraient probablement limiter le nombre maximum de pairs
à environ 50, ce qui correspond à environ un paquet de 1600 octets avant les frais généraux
à différents niveaux, et devrait se situer dans une limite de charge utile de message de tunnel à deux après fragmentation.

Comme dans le BEP 15, il n'y a pas de nombre inclus indiquant le nombre d'adresses de pairs
(IP/port pour BEP 15, hachages ici) à suivre.
Bien qu'il ne soit pas envisagé dans BEP 15, un marqueur de fin de pairs
de zéros complets pourrait être défini pour indiquer que l'information sur les pairs est complète
et que des données d'extension suivent.

Pour que l'extension soit possible à l'avenir, les clients devraient ignorer
un hachage de 32 octets avec tous les zéros, et toute donnée qui suit.
Les trackers devraient rejeter les annonces provenant d'un hachage entièrement en zéros,
bien que ce hachage soit déjà banni par les routeurs Java.


Scrape
``````

La demande/réponse de scrape de [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) n'est pas requise par cette proposition,
mais peut être implémentée si désiré, aucun changement requis.
Le client doit acquérir un identifiant de connexion en premier.
La demande de scrape est toujours un Datagram3 répliquable.
La réponse de scrape est toujours brute.



Réponse d'erreur
````````````````

Tracker au client.
8 octets minimum (si le message est vide).
Doit être brut. Identique à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html). Pas de changements.

```

Offset  Taille          Nom              Valeur
  0       Entier 32 bits  action          3 // erreur
  4       Entier 32 bits  transaction_id
  8       chaîne          message

```



## Extensions

Les bits d'extension ou un champ de version ne sont pas inclus.
Les clients et les trackers ne doivent pas supposer que les paquets ont une certaine taille.
De cette façon, des champs supplémentaires peuvent être ajoutés sans casser la compatibilité.
Le format d'extensions défini dans [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) est recommandé si nécessaire.

La réponse de connexion est modifiée pour ajouter une durée de vie optionnelle pour l'identifiant de connexion.

Si le support des destinations aveuglées est requis, nous pouvons soit ajouter l'adresse aveuglée de 35 octets à la fin de la demande d'annonce,
soit demander des hachages aveuglés dans les réponses,
en utilisant le format [BEP 41](http://www.bittorrent.org/beps/bep_0041.html) (paramètres à déterminer).
L'ensemble des adresses 35 octets des pairs aveuglés pourrait être ajouté à la fin de la réponse d'annonce,
après un hachage de 32 octets tous à zéro.



## Lignes directrices d'implémentation

Voir la section conception ci-dessus pour une discussion des défis liés aux
trackers et clients non intégrés, non-I2CP.


### Clients

Pour un nom de tracker donné, un client devrait préférer les URLs UDP aux URLs HTTP,
et ne devrait pas annoncer aux deux.

Les clients avec un support existant de BEP 15 devraient nécessiter seulement de petites modifications.

Si un client supporte DHT ou d'autres protocoles de datagrammes, il devrait probablement
choisir un port différent comme le "from port" de la demande afin que les réponses
retournent vers ce port et ne soient pas confondues avec des messages DHT.
Le client ne reçoit que des datagrammes bruts comme réponses.
Les trackers n'enverront jamais un datagram2 répliquable au client.

Les clients avec une liste par défaut d'opentrackers devraient mettre à jour la liste pour
ajouter des URLs UDP après que les opentrackers connus soient connus pour supporter UDP.

Les clients peuvent ou non mettre en œuvre la retransmission de demandes.
Les retransmissions, si implémentées, devraient utiliser un délai initial d'au moins 15 secondes, et doubler le délai pour chaque retransmission
(retrait exponentiel).

Les clients doivent se retirer après avoir reçu une réponse d'erreur.


### Trackers

Les trackers avec un support existant de BEP 15 devraient nécessiter seulement de petites modifications.
Cette proposition diffère de la proposition de 2014, car le tracker
doit supporter la réception de datagrammes répliquables datagram2 et datagram3 sur le même port.

Pour minimiser les exigences en ressources du tracker,
ce protocole est conçu pour éliminer toute exigence que le tracker
stocke des mappages de hachages clients à des identifiants de connexion pour une validation ultérieure.
Ceci est possible car le paquet de demande d'annonce est un Datagram3
répliquable, donc il contient le hachage de l'expéditeur.

Une implémentation recommandée est :

- Définissez l'époque actuelle comme le temps actuel avec une résolution de la durée de vie de la connexion,
  ``epoch = now / lifetime``.
- Définissez une fonction de hachage cryptographique ``H(secret, clienthash, epoch)`` qui génère
  une sortie de 8 octets.
- Générez la constante aléatoire secrète utilisée pour toutes les connexions.
- Pour les réponses de connexion, générez ``connection_id = H(secret, clienthash, epoch)``
- Pour les demandes d'annonces, validez l'identifiant de connexion reçu dans l'époque actuelle en vérifiant
  ``connection_id == H(secret, clienthash, epoch) || connection_id == H(secret, clienthash, epoch - 1)``


## Migration

Les clients existants ne supportent pas les URLs d'annonce UDP et les ignorent.

Les trackers existants ne supportent pas la réception de datagrammes répliquables ou bruts, ils seront supprimés.

Cette proposition est complètement optionnelle. Ni les clients ni les trackers ne sont tenus de l'implémenter à tout moment.



## Déploiement

Les premières implémentations devraient être dans ZzzOT et i2psnark.
Elles seront utilisées pour tester et vérifier cette proposition.

D'autres implémentations suivront selon les besoins après que les tests et la vérification soient terminés.




