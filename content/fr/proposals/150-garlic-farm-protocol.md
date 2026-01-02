---
title: "Protocole de la ferme à l'ail"
number: "150"
author: "zzz"
created: "2019-05-02"
lastupdated: "2019-05-20"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2234"
toc: true
---

## Vue d'ensemble

Ceci est la spécification pour le protocole de la ferme à l'ail,
basé sur JRaft, son code "exts" pour l'implémentation sur TCP,
et son application exemple "dmprinter" [JRAFT](https://github.com/datatechnology/jraft).
JRaft est une implémentation du protocole Raft [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf).

Nous n'avons pas été en mesure de trouver une implémentation avec un protocole documenté.
Cependant, l'implémentation JRaft est suffisamment simple pour que nous puissions
inspecter le code et puis documenter son protocole.
Cette proposition est le résultat de cet effort.

Cela servira de backend pour la coordination des routeurs publiant
des entrées dans un Meta LeaseSet. Voir la proposition 123.


## Objectifs

- Taille réduite du code
- Basé sur une implémentation existante
- Pas d'objets Java sérialisés ni de fonctionnalités ou d'encodages spécifiques à Java
- Tout amorçage est hors-scope. Au moins un autre serveur est supposé
  être codé en dur, ou configuré hors bande de ce protocole.
- Support des cas d'utilisation hors bande et dans I2P.


## Conception

Le protocole Raft n'est pas un protocole concret ; il définit seulement une machine à états.
Par conséquent, nous documentons le protocole concret de JRaft et basons notre protocole dessus.
Il n'y a pas de changements au protocole JRaft autre que l'ajout d'une
authentification par poignée de main.

Raft élit un Leader dont le travail est de publier un journal.
Le journal contient des données de configuration Raft et les données d'application.
Les données d'application contiennent le statut de chaque routeur du serveur et la destination
pour le cluster Meta LS2.
Les serveurs utilisent un algorithme commun pour déterminer l'éditeur et le contenu
du Meta LS2.
L'éditeur du Meta LS2 n'est PAS nécessairement le Leader Raft.


## Spécification

Le protocole filaire utilise des sockets SSL ou des sockets I2P non SSL.
Les sockets I2P sont proxifiés via le proxy HTTP.
Il n'y a pas de support pour les sockets non-SSL en clair.

### Poignée de main et authentification

Non défini par JRaft.

Objectifs :

- Méthode d'authentification par utilisateur/mot de passe
- Identifiant de version
- Identifiant de cluster
- Extensible
- Facilité de proxy lorsqu'il est utilisé pour les sockets I2P
- Ne pas exposer inutilement le serveur en tant que serveur de la ferme à l'ail
- Protocole simple pour éviter la nécessité d'une implémentation complète de serveur web
- Compatible avec les standards courants, pour que les implémentations puissent utiliser
  des bibliothèques standard si désiré

Nous utiliserons une poignée de main similaire à websocket [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
et une authentification HTTP Digest [RFC-2617](https://tools.ietf.org/html/rfc2617).
L'authentification de base RFC 2617 n'est PAS supportée.
Quand on passe par le proxy HTTP, communiquer avec
le proxy comme spécifié dans [RFC-2616](https://tools.ietf.org/html/rfc2616).

#### Identifiants

Que les noms d'utilisateur et les mots de passe soient par cluster, ou
par serveur, dépend de l'implémentation.


#### Requête HTTP 1

L'initiateur enverra ce qui suit.

Toutes les lignes se terminent par CRLF comme requis par HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Hôte : (ip):(port)
  Cache-Control: no-cache
  Connexion: close
  (tous les autres en-têtes ignorés)
  (ligne vide)

  CLUSTER est le nom du cluster (par défaut "farm")
  VERSION est la version de la ferme à l'ail (actuellement "1")
```


#### Réponse HTTP 1

Si le chemin n'est pas correct, le destinataire enverra une réponse standard "HTTP/1.1 404 Not Found",
comme dans [RFC-2616](https://tools.ietf.org/html/rfc2616).

Si le chemin est correct, le destinataire enverra une réponse standard "HTTP/1.1 401 Unauthorized",
incluant l'en-tête d'authentification HTTP digest WWW-Authenticate,
comme dans [RFC-2617](https://tools.ietf.org/html/rfc2617).

Les deux parties fermeront alors le socket.


#### Requête HTTP 2

L'initiateur enverra ce qui suit,
comme dans [RFC-2617](https://tools.ietf.org/html/rfc2617) et [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Toutes les lignes se terminent par CRLF comme requis par HTTP.

```text
GET /GarlicFarm/CLUSTER/VERSION/websocket HTTP/1.1
  Hôte : (ip):(port)
  Cache-Control: no-cache
  Connexion: keep-alive, Upgrade
  Upgrade: websocket
  (en-têtes Sec-Websocket-* si proxifié)
  Authorization: (en-tête d'autorisation HTTP digest comme dans RFC 2617)
  (tous les autres en-têtes ignorés)
  (ligne vide)

  CLUSTER est le nom du cluster (par défaut "farm")
  VERSION est la version de la ferme à l'ail (actuellement "1")
```


#### Réponse HTTP 2

Si l'authentification n'est pas correcte, le destinataire enverra une autre réponse standard "HTTP/1.1 401 Unauthorized",
comme dans [RFC-2617](https://tools.ietf.org/html/rfc2617).

Si l'authentification est correcte, le destinataire enverra la réponse suivante,
comme dans [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket).

Toutes les lignes se terminent par CRLF comme requis par HTTP.

```text
HTTP/1.1 101 Switching Protocols
  Connexion: Upgrade
  Upgrade: websocket
  (en-têtes Sec-Websocket-*)
  (tous les autres en-têtes ignorés)
  (ligne vide)
```

Après réception, le socket reste ouvert.
Le protocole Raft tel que défini ci-dessous commence, sur le même socket.


#### Mise en cache

Les identifiants doivent être mis en cache pendant au moins une heure, pour que
les connexions ultérieures puissent passer directement à
"Requête HTTP 2" ci-dessus.


### Types de messages

Il existe deux types de messages, les requêtes et les réponses.
Les requêtes peuvent contenir des entrées de journal, et sont de taille variable ;
les réponses ne contiennent pas d'entrées de journal, et sont de taille fixe.

Les types de messages 1-4 sont les messages RPC standards définis par Raft.
Ceci est le protocole Raft de base.

Les types de messages 5-15 sont les messages RPC étendus définis par
JRaft, pour prendre en charge les clients, les modifications dynamiques du serveur et
la synchronisation efficace des journaux.

Les types de messages 16-17 sont les messages RPC de compactage de journal définis
dans la section 7 de Raft.


| Message | Numéro | Envoyé par | Envoyé à | Remarques |
| :--- | :--- | :--- | :--- | :--- |
| RequestVoteRequest | 1 | Candidat | Suiveur | RPC standard Raft; ne doit pas contenir d'entrées de journal |
| RequestVoteResponse | 2 | Suiveur | Candidat | RPC standard Raft |
| AppendEntriesRequest | 3 | Leader | Suiveur | RPC standard Raft |
| AppendEntriesResponse | 4 | Suiveur | Leader / Client | RPC standard Raft |
| ClientRequest | 5 | Client | Leader / Suiveur | La réponse est AppendEntriesResponse; doit contenir uniquement des entrées de journal d'application |
| AddServerRequest | 6 | Client | Leader | Doit contenir une seule entrée de journal ClusterServer uniquement |
| AddServerResponse | 7 | Leader | Client | Le leader enverra également une demande JoinClusterRequest |
| RemoveServerRequest | 8 | Suiveur | Leader | Doit contenir une seule entrée de journal ClusterServer uniquement |
| RemoveServerResponse | 9 | Leader | Suiveur | |
| SyncLogRequest | 10 | Leader | Suiveur | Doit contenir une seule entrée de journal LogPack uniquement |
| SyncLogResponse | 11 | Suiveur | Leader | |
| JoinClusterRequest | 12 | Leader | Nouveau Serveur | Invitation à rejoindre; doit contenir une seule entrée de journal de configuration uniquement |
| JoinClusterResponse | 13 | Nouveau Serveur | Leader | |
| LeaveClusterRequest | 14 | Leader | Suiveur | Commande de quitter |
| LeaveClusterResponse | 15 | Suiveur | Leader | |
| InstallSnapshotRequest | 16 | Leader | Suiveur | Section 7 de Raft; doit contenir une seule entrée de journal SnapshotSyncRequest uniquement |
| InstallSnapshotResponse | 17 | Suiveur | Leader | Section 7 de Raft |


### Établissement

Après la poignée de main HTTP, la séquence d'établissement est la suivante :

```text
Nouveau Serveur Alice              Suiveur Aléatoire Bob

  ClientRequest   ------->
          <---------   AppendEntriesResponse

  Si Bob dit qu'il est le leader, continuez comme ci-dessous.
  Sinon, Alice doit se déconnecter de Bob et se connecter au leader.


  Nouveau Serveur Alice              Leader Charlie

  ClientRequest   ------->
          <---------   AppendEntriesResponse
  AddServerRequest   ------->
          <---------   AddServerResponse
          <---------   JoinClusterRequest
  JoinClusterResponse  ------->
          <---------   SyncLogRequest
                       OU InstallSnapshotRequest
  SyncLogResponse  ------->
  OU InstallSnapshotResponse
```

Séquence de déconnexion :

```text
Suiveur Alice              Leader Charlie

  RemoveServerRequest   ------->
          <---------   RemoveServerResponse
          <---------   LeaveClusterRequest
  LeaveClusterResponse  ------->
```

Séquence d'élection :

```text
Candidat Alice               Suiveur Bob

  RequestVoteRequest   ------->
          <---------   RequestVoteResponse

  si Alice remporte l'élection :

  Leader Alice                Suiveur Bob

  AppendEntriesRequest   ------->
  (coup de cœur)
          <---------   AppendEntriesResponse
```


### Définitions

- Source : Identifie l'origine du message
- Destination : Identifie le destinataire du message
- Termes : Voir Raft. Initialisé à 0, augmente de façon monotone
- Indexes : Voir Raft. Initialisé à 0, augmente de façon monotone


### Requêtes

Les requêtes contiennent un en-tête et zéro ou plusieurs entrées de journal.
Les requêtes contiennent un en-tête de taille fixe et des entrées de journal optionnelles de taille variable.


#### En-tête de requête

L'en-tête de requête fait 45 octets, comme suit.
Toutes les valeurs sont en big-endian non signé.

```dataspec
Type de message :      1 octet
  Source :           ID, entier 4 octets
  Destination :      ID, entier 4 octets
  Terme :            Terme actuel (voir notes), entier 8 octets
  Dernier Terme de Journal :   entier 8 octets
  Dernier Index de Journal :   entier 8 octets
  Index de Validation :   entier 8 octets
  Taille des entrées de journal :  Taille totale en octets, entier 4 octets
  Entrées de journal :       voir ci-dessous, longueur totale comme spécifié
```


#### Remarques

Dans le RequestVoteRequest, le terme est le terme du candidat.
Sinon, c'est le terme actuel du leader.

Dans le AppendEntriesRequest, lorsque la taille des entrées de journal est zéro,
ce message est un message de maintien (keepalive).


#### Entrées de journal

Le journal contient zéro ou plusieurs entrées de journal.
Chaque entrée de journal est comme suit.
Toutes les valeurs sont en big-endian non signé.

```dataspec
Terme :           entier 8 octets
  Type de valeur :   1 octet
  Taille de l'entrée :  En octets, entier 4 octets
  Entrée :          longueur comme spécifié
```


#### Contenu du journal

Toutes les valeurs sont en big-endian non signé.

| Type de valeur du journal | Numéro |
| :--- | :--- |
| Application | 1 |
| Configuration | 2 |
| ClusterServer | 3 |
| LogPack | 4 |
| SnapshotSyncRequest | 5 |


#### Application

Les contenus d'application sont encodés en UTF-8 [JSON](https://www.json.org/).
Voir la section Couche d'application ci-dessous.


#### Configuration

Ceci est utilisé pour que le leader série un nouvelle configuration de cluster et réplique aux pairs.
Cela contient zéro ou plusieurs configurations de ClusterServer.

```dataspec
Index du Journal :  entier 8 octets
  Dernier Index du Journal :  entier 8 octets
  Données de Clusterserver pour chaque serveur :
    ID :                entier 4 octets
    Taille des données de point de terminaison : En octets, entier 4 octets
    Données de point de terminaison :     chaîne ASCII sous la forme "tcp://localhost:9001", longueur comme spécifié
```


#### ClusterServer

Les informations de configuration pour un serveur dans un cluster.
Ceci est inclus uniquement dans un message AddServerRequest ou RemoveServerRequest.

Lorsqu'il est utilisé dans un message AddServerRequest :

```dataspec
ID :                entier 4 octets
  Taille des données de point de terminaison : En octets, entier 4 octets
  Données de point de terminaison :     chaîne ASCII sous la forme "tcp://localhost:9001", longueur comme spécifié
```


Lorsqu'il est utilisé dans un message RemoveServerRequest :

```dataspec
ID :                entier 4 octets
```


#### LogPack

Cela est inclus uniquement dans un message SyncLogRequest.

Ce qui suit est comprimé en gzip avant la transmission :

```dataspec
Taille des données d'index : En octets, entier 4 octets
  Taille des données de journal :   En octets, entier 4 octets
  Données d'index :     8 octets pour chaque index, longueur comme spécifié
  Données de journal :       longueur comme spécifié
```


#### SnapshotSyncRequest

Cela est inclus uniquement dans un message InstallSnapshotRequest.

```dataspec
Dernier Index de Journal :  entier 8 octets
  Dernier Terme de Journal :   entier 8 octets
  Taille des données de configuration : En octets, entier 4 octets
  Données de configuration :     longueur comme spécifié
  Décalage :          Le décalage des données dans la base de données, en octets, entier 8 octets
  Taille des données :        En octets, entier 4 octets
  Données :            longueur comme spécifié
  Est Fait :         1 si terminé, 0 sinon (1 octet)
```


### Réponses

Toutes les réponses font 26 octets, comme suit.
Toutes les valeurs sont en big-endian non signé.

```dataspec
Type de message :   1 octet
  Source :         ID, entier 4 octets
  Destination :    Habituellement l'ID de destination réel (voir remarques), entier 4 octets
  Terme :           Terme actuel, entier 8 octets
  Index suivant :     Initialisé à l'index du dernier journal du leader + 1, entier 8 octets
  Est Accepté :    1 si accepté, 0 si non accepté (voir remarques), 1 octet
```


#### Remarques

L'ID de destination est habituellement l'ID de destination réel pour ce message.
Cependant, pour AppendEntriesResponse, AddServerResponse, et RemoveServerResponse,
c'est l'ID du leader actuel.

Dans le RequestVoteResponse, Est Accepté est 1 pour un vote pour le candidat (demandeur),
et 0 pour aucun vote.


## Couche d'application

Chaque serveur publie périodiquement des données d'application dans le journal lors d'une ClientRequest.
Les données d'application contiennent le statut de chaque routeur du serveur et la destination
pour le cluster Meta LS2.
Les serveurs utilisent un algorithme commun pour déterminer l'éditeur et le contenu
du Meta LS2.
Le serveur avec le "meilleur" état récent dans le journal est l'éditeur du Meta LS2.
L'éditeur du Meta LS2 n'est PAS nécessairement le Leader Raft.


### Contenu des données d'application

Les contenus d'application sont encodés en UTF-8 [JSON](https://www.json.org/),
pour la simplicité et l'extensibilité.
La spécification complète est à déterminer (TBD).
L'objectif est de fournir suffisamment de données pour écrire un algorithme déterminant quel est le "meilleur"
routeur pour publier le Meta LS2, et pour que l'éditeur ait suffisamment d'informations
pour pondérer les destinations dans le Meta LS2.
Les données contiendront à la fois les statistiques de routeur et de destination.

Les données peuvent optionnellement contenir des données de télédétection sur la santé des
autres serveurs, et la capacité à récupérer le Meta LS.
Ces données ne seraient pas supportées dans la première version.

Les données peuvent optionnellement contenir des informations de configuration publiées
par un client administrateur.
Ces données ne seraient pas supportées dans la première version.

Si "name: value" est listé, cela spécifie la clé et la valeur dans la carte JSON.
Sinon, la spécification est à déterminer.


Données de cluster (niveau supérieur) :

- cluster: Nom du cluster
- date: Date de ces données (long, ms depuis l'époque)
- id: ID Raft (entier)

Données de configuration (config) :

- Tout paramètre de configuration

Statut de publication MetaLS (meta) :

- destination: la destination Meta LS2, base64
- lastPublishedLS: si présent, encodage base64 du dernier Meta LS publié
- lastPublishedTime: en ms, ou 0 si jamais
- publishConfig: Statut de configuration de publication éteint/allumé/auto
- publishing: Statut de publication Meta LS2 boolean vrai/faux

Données de routeur (router) :

- lastPublishedRI: si présent, encodage base64 des dernières informations de routeur publiées
- uptime: Temps de fonctionnement en ms
- Retard de travail
- Tunnels exploratoires
- Tunnels participants
- Bande passante configurée
- Bande passante actuelle

Destinations (destinations) :
Liste

Données de destination :

- destination: la destination, base64
- uptime: Temps de fonctionnement en ms
- Tunnels configurés
- Tunnels actuels
- Bande passante configurée
- Bande passante actuelle
- Connexions configurées
- Connexions actuelles
- Données de liste noire

Données de télédétection à distance de routeur :

- Dernière version RI vue
- Temps de récupération LS
- Données de test de connexion
- Données de profil des closest floodfills
  pour les périodes hier, aujourd'hui, et demain

Données de télédétection à distance de destination :

- Dernière version LS vue
- Temps de récupération LS
- Données de test de connexion
- Données de profil des closest floodfills
  pour les périodes hier, aujourd'hui, et demain

Données de télédétection Meta LS :

- Dernière version vue
- Temps de récupération
- Données de profil des closest floodfills
  pour les périodes hier, aujourd'hui, et demain


## Interface d'administration

TBD, peut-être une proposition séparée.
Non requis pour la première version.

Exigences d'une interface d'administration :

- Support pour plusieurs destinations maîtres, c'est-à-dire plusieurs clusters (fermes) virtuels
- Fournir une vue globale de l'état partagé du cluster - toutes les statistiques publiées par les membres, qui est le leader actuel, etc.
- Capacité à forcer la suppression d'un participant ou d'un leader du cluster
- Capacité à forcer la publication de metaLS (si le nœud actuel est l'éditeur)
- Capacité à exclure des hachages de metaLS (si le nœud actuel est l'éditeur)
- Fonctionnalité d'import/export de configuration pour les déploiements en masse


## Interface des routeurs

TBD, peut-être une proposition séparée.
i2pcontrol n'est pas requis pour la première version et les changements détaillés seront inclus dans une proposition séparée.

Exigences pour Garlic Farm à API de routeur (en-JVM java ou i2pcontrol)

- Obtenez le statut de routeur local ()
- Obtenez le hachage de feuille local (Hash masterHash)
- Obtenez le statut de feuille local (Hash leaf)
- Obtenez le statut mesuré à distance (Hash masterOrLeaf) // probablement pas dans le MVP
- Publier la metaLS (Hash masterHash, List<MetaLease> contents) // ou MetaLeaseSet signé? Qui signe ?
- Arrêter la publication de la metaLS (Hash masterHash)
- authentification TBD?


## Justification

Atomix est trop volumineux et ne permettra pas de personnalisation pour que nous puissions acheminer
le protocole sur I2P. De plus, son format filaire n'est pas documenté et
dépend de la sérialisation en Java.


## Remarques


## Problèmes

- Il n'y a pas de moyen pour un client de découvrir et de se connecter à un leader inconnu.
  Ce serait un changement mineur pour un Suiveur d'envoyer la configuration comme une entrée de journal dans la réponse AppendEntriesResponse.


## Migration

Aucun problème de compatibilité rétroactive.


## Références

* [JRAFT](https://github.com/datatechnology/jraft)
* [JSON](https://json.org/)
* [RAFT](https://ramcloud.stanford.edu/wiki/download/attachments/11370504/raft.pdf)
* [RFC-2616](https://tools.ietf.org/html/rfc2616)
* [RFC-2617](https://tools.ietf.org/html/rfc2617)
* [WEBSOCKET](https://en.wikipedia.org/wiki/WebSocket)
