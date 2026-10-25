---
title: "I2PTunnel"
description: "Outil pour interfacer avec et fournir des services sur I2P"
slug: "i2ptunnel"
aliases:
  - "/fr/i2ptunnel"
  - "/fr/i2ptunnel/"
  - "/fr/i2ptunnel_migration"
  - "/fr/i2ptunnel_migration/"
  - "/fr/i2ptunnel_services"
  - "/fr/i2ptunnel_services/"
lastUpdated: "2023-10"
accurateFor: "0.9.59"
---

## Aperçu {#overview}

I2PTunnel est un outil permettant d'interfacer avec et de fournir des services sur I2P. La destination d'un I2PTunnel peut être définie en utilisant un [hostname](/docs/overview/naming), [Base32](/docs/overview/naming#base32), ou une clé de destination complète de 516 octets. Un I2PTunnel établi sera disponible sur votre machine cliente en tant que localhost:port. Si vous souhaitez fournir un service sur le réseau I2P, vous créez simplement un I2PTunnel vers l'adresse_ip:port appropriée. Une clé de destination correspondante de 516 octets sera générée pour le service et celui-ci deviendra disponible dans tout I2P. Une interface web pour la gestion d'I2PTunnel est disponible sur [localhost:7657/i2ptunnel/](http://localhost:7657/i2ptunnel/).

## Services par défaut {#default-services}

### Tunnels serveur {#default-server-tunnels}

- **I2P Webserver** - Un tunnel pointé vers un serveur web Jetty fonctionnant
  sur [localhost:7658](http://localhost:7658) pour un hébergement pratique et rapide sur I2P.
  Le répertoire racine des documents est :
  - **Unix** - `$HOME/.i2p/eepsite/docroot`
  - **Windows** - `%LOCALAPPDATA%\I2P\I2P Site\docroot`, qui se développe en : `C:\Users\**nom_utilisateur**\AppData\Local\I2P\I2P Site\docroot`

### Tunnels Client {#default-client-tunnels}

- **I2P HTTP Proxy** - *localhost:4444* - Un proxy HTTP utilisé pour naviguer sur I2P et internet normal de manière anonyme via I2P. La navigation sur internet via I2P utilise un proxy aléatoire spécifié par l'option "Outproxies:".
- **Irc2P** - *localhost:6668* - Un tunnel IRC vers le réseau IRC anonyme par défaut, Irc2P.
- **gitssh.idk.i2p** - *localhost:7670* - Accès SSH au dépôt Git du projet
- **smtp.postman.i2p** - *localhost:7659* - Un service SMTP fourni par postman à hq.postman.i2p
- **pop3.postman.i2p** - *localhost:7660* - Le service POP associé de postman à hq.postman.i2p

## Configuration {#configuration}

[Configuration d'I2PTunnel](/docs/specs/configuration)

## Modes Client {#client-modes}

### Standard {#client-modes-standard}

Ouvre un port TCP local qui se connecte à un service (comme HTTP, FTP ou SMTP) sur une destination à l'intérieur d'I2P. Le tunnel est dirigé vers un hôte aléatoire de la liste de destinations séparées par des virgules (", ").

### HTTP {#client-mode-http}

Un tunnel client HTTP. Le tunnel se connecte à la destination spécifiée par l'URL dans une requête HTTP. Prend en charge le proxy vers internet si un outproxy est fourni. Supprime les en-têtes suivants des connexions HTTP :

- **Accept\*:** (n'incluant pas "Accept" et "Accept-Encoding") car ils varient grandement entre les navigateurs et peuvent être utilisés comme identifiant.
- **Referer:**
- **Via:**
- **From:**

Le proxy client HTTP fournit plusieurs services pour protéger l'utilisateur et offrir une meilleure expérience utilisateur.

**Traitement des en-têtes de requête :** - Suppression des en-têtes problématiques pour la confidentialité - Routage vers un outproxy local ou distant - Sélection, mise en cache et suivi de la disponibilité des outproxy - Recherches de nom d'hôte vers destination - Remplacement de l'en-tête Host par b32 - Ajout d'en-tête pour indiquer la prise en charge de la décompression transparente - Forcer connection: close - Prise en charge de proxy conforme RFC - Traitement et suppression conformes RFC des en-têtes hop-by-hop - Authentification optionnelle par digest et nom d'utilisateur/mot de passe de base - Authentification optionnelle d'outproxy par digest et nom d'utilisateur/mot de passe de base - Mise en mémoire tampon de tous les en-têtes avant transmission pour l'efficacité - Liens de serveur de saut - Traitement des réponses de saut et formulaires (assistant d'adresse) - Traitement b32 aveugle et formulaires d'identifiants - Prend en charge les requêtes HTTP et HTTPS (CONNECT) standard

**Traitement des en-têtes de réponse :** - Vérifier s'il faut décompresser la réponse - Forcer connection: close - Traitement et suppression des en-têtes hop-by-hop conformes à la RFC - Mise en mémoire tampon de tous les en-têtes avant transmission pour l'efficacité

**Réponses d'erreur HTTP :** - Pour de nombreuses erreurs courantes et moins courantes, afin que l'utilisateur sache ce qui s'est passé - Plus de 20 pages d'erreur uniques traduites, stylisées et formatées pour diverses erreurs - Serveur web interne pour servir les formulaires, CSS, images et erreurs

#### Compression Transparente des Réponses {#transparent-response-compression}

La compression de réponse i2ptunnel est demandée avec l'en-tête HTTP :

- **X-Accept-Encoding:** x-i2p-gzip;q=1.0, identity;q=0.5, deflate;q=0, gzip;q=0, *;q=0

Le côté serveur supprime cet en-tête hop-by-hop avant d'envoyer la requête au serveur web. L'en-tête élaboré avec toutes les valeurs q n'est pas nécessaire ; les serveurs doivent simplement rechercher "x-i2p-gzip" n'importe où dans l'en-tête.

Le côté serveur détermine s'il faut compresser la réponse en se basant sur les en-têtes reçus du serveur web, incluant Content-Type, Content-Length et Content-Encoding, pour évaluer si la réponse est compressible et si cela justifie le CPU supplémentaire requis. Si le côté serveur compresse la réponse, il ajoute l'en-tête HTTP suivant :

- **Content-Encoding:** x-i2p-gzip

Si cet en-tête est présent dans la réponse, le proxy client HTTP le décompresse de manière transparente. Le côté client supprime cet en-tête et décompresse avec gunzip avant d'envoyer la réponse au navigateur. Notez que nous avons toujours la compression gzip sous-jacente au niveau de la couche I2CP, qui reste efficace si la réponse n'est pas compressée au niveau de la couche HTTP.

Cette conception et l'implémentation actuelle violent la RFC 2616 de plusieurs manières :

- X-Accept-Encoding n'est pas un en-tête standard
- Ne décompresse/compresse pas par saut ; il transmet la compression de bout en bout
- Transmet l'en-tête Transfer-Encoding de bout en bout
- Utilise Content-Encoding, et non Transfer-Encoding, pour spécifier l'encodage par saut
- Interdit la compression gzip x-i2p lorsque Content-Encoding est défini (mais nous ne voulons probablement pas le faire de toute façon)
- Le côté serveur compresse en gzip la segmentation envoyée par le serveur, plutôt que de faire décompression-gzip-recompression et décompression-gunzip-recompression
- Le contenu compressé en gzip n'est pas segmenté par la suite. RFC 2616 exige que tout Transfer-Encoding autre que "identity" soit segmenté.
- Parce qu'il n'y a pas de segmentation à l'extérieur (après) le gzip, il est plus difficile de trouver la fin des données, rendant toute implémentation de keepalive plus difficile.
- RFC 2616 dit que Content-Length ne doit pas être envoyé si Transfer-Encoding est présent, mais nous le faisons. La spécification dit d'ignorer Content-Length si Transfer-Encoding est présent, ce que font les navigateurs, donc cela fonctionne pour nous.

Les modifications pour implémenter une compression saut-par-saut conforme aux standards de manière rétro-compatible constituent un sujet d'étude supplémentaire. Tout changement au processus dechunk-gzip-rechunk nécessiterait un nouveau type d'encodage, peut-être x-i2p-gzchunked. Ceci serait identique à Transfer-Encoding: gzip, mais devrait être signalé différemment pour des raisons de compatibilité. Tout changement nécessiterait une proposition formelle.

#### Compression transparente des requêtes {#transparent-request-compression}

Non pris en charge, bien que POST en bénéficierait. Notez que nous avons toujours la compression gzip sous-jacente au niveau de la couche I2CP.

#### Persistance {#persistence}

Les proxies client et serveur ne prennent actuellement pas en charge les sockets HTTP persistants RFC 2616 sur aucun des trois sauts (socket navigateur, socket I2P, socket serveur). Les en-têtes Connection: close sont injectés à chaque saut. Des modifications pour implémenter la persistance sont à l'étude. Ces modifications devraient être conformes aux standards et rétrocompatibles, et ne nécessiteraient pas de proposition formelle.

#### Pipelining {#pipelining}

Les proxies client et serveur ne supportent pas actuellement le pipelining HTTP RFC 2616 et il n'y a pas de plans pour le faire. Les navigateurs modernes ne supportent pas le pipelining à travers les proxies car la plupart des proxies ne peuvent pas l'implémenter correctement.

#### Compatibilité {#compatibility}

Les implémentations de proxy doivent fonctionner correctement avec d'autres implémentations de l'autre côté. Les proxies clients devraient fonctionner sans proxy serveur compatible HTTP (c'est-à-dire un tunnel standard) du côté serveur. Toutes les implémentations ne prennent pas en charge x-i2p-gzip.

#### Agent Utilisateur {#user-agent}

Selon que le tunnel utilise un outproxy ou non, il ajoutera le User-Agent suivant :

- *Outproxy :* **User-Agent :** Utilise l'agent utilisateur d'une version récente de Firefox sur Windows
- *Utilisation I2P interne :* **User-Agent :** MYOB/6.66 (AN/ON)

### Client IRC {#client-mode-irc}

Crée une connexion vers un serveur IRC aléatoire spécifié par la liste de destinations séparées par des virgules (", "). Seul un sous-ensemble de commandes IRC autorisées est permis en raison de préoccupations liées à l'anonymat.

La liste d'autorisation suivante concerne les commandes entrantes du serveur IRC vers le client IRC.

**Liste d'autorisation :** - AUTHENTICATE - CAP - ERROR - H - JOIN - KICK - MODE - NICK - PART - PING - PROTOCTL - QUIT - TOPIC - WALLOPS

Il existe également une liste d'autorisation pour les commandes sortantes du client IRC vers le serveur IRC. Elle est assez volumineuse en raison du nombre de commandes administratives IRC. Voir le code source IRCFilter.java pour plus de détails.

Le filtre sortant modifie également les commandes suivantes pour supprimer les informations d'identification : - NOTICE - PART - PING - PRIVMSG - QUIT - USER

### SOCKS 4/4a/5 {#client-mode-socks}

Permet d'utiliser le router I2P comme un proxy SOCKS.

### SOCKS IRC {#client-mode-socks-irc}

Permet d'utiliser le router I2P comme proxy SOCKS avec la liste blanche de commandes spécifiée par le mode client [IRC](#client-mode-irc).

### CONNECT {#client-mode-connect}

Crée un tunnel HTTP et utilise la méthode de requête HTTP "CONNECT" pour construire un tunnel TCP qui est généralement utilisé pour SSL et HTTPS.

### Streamr {#client-mode-streamr}

Crée un serveur UDP attaché à un tunnel I2PTunnel client Streamr. Le tunnel client streamr s'abonnera à un tunnel serveur streamr.

![Diagramme Streamr](/images/I2PTunnel-streamr.png)

## Modes Serveur {#server-modes}

### Standard {#server-mode-standard}

Crée une destination vers une ip:port locale avec un port TCP ouvert.

### HTTP {#server-mode-http}

Crée une destination vers un serveur HTTP local ip:port. Prend en charge gzip pour les requêtes avec Accept-encoding: x-i2p-gzip, répond avec Content-encoding: x-i2p-gzip dans une telle requête.

Le proxy de serveur HTTP fournit un certain nombre de services pour faciliter l'hébergement d'un site web et le rendre plus sécurisé, et pour offrir une meilleure expérience utilisateur côté client.

**Traitement des en-têtes de requête :** - Validation des en-têtes - Protection contre l'usurpation d'en-têtes - Vérifications de la taille des en-têtes - Rejet optionnel des inproxy et user-agent - Ajout d'en-têtes X-I2P pour que le serveur web sache d'où provient la requête - Remplacement de l'en-tête Host pour faciliter les vhosts du serveur web - Forcer connection: close - Traitement et suppression des en-têtes hop-by-hop conformes à la RFC - Mise en mémoire tampon de tous les en-têtes avant transmission pour l'efficacité

**Protection DDoS :** - Limitation du débit POST - Protection contre les timeouts et slowloris - Une limitation supplémentaire se produit dans le streaming pour tous les types de tunnel

**Traitement des en-têtes de réponse :** - Suppression de certains en-têtes problématiques pour la confidentialité - Vérification du type MIME et autres en-têtes pour déterminer s'il faut compresser la réponse - Forcer connection: close - Traitement et suppression conformes RFC des en-têtes hop-by-hop - Mise en mémoire tampon de tous les en-têtes avant transmission pour l'efficacité

**Réponses d'erreur HTTP :** - Pour de nombreuses erreurs courantes et moins courantes ainsi que pour la limitation de débit, afin que l'utilisateur côté client sache ce qui s'est passé

**Compression transparente des réponses :** - Le serveur web et/ou la couche I2CP peuvent compresser, mais le serveur web ne le fait souvent pas, et il est plus efficace de compresser à un niveau élevé, même si I2CP compresse également. Le proxy serveur HTTP fonctionne en coopération avec le proxy côté client pour compresser les réponses de manière transparente.

### HTTP Bidirectionnel {#server-mode-http-bidir}

*Déprécié*

Fonctionne à la fois comme un serveur HTTP I2PTunnel et un client HTTP I2PTunnel sans capacités de proxy sortant. Un exemple d'application serait une application web qui effectue des requêtes de type client, ou le test en boucle locale d'un site I2P comme outil de diagnostic.

### Serveur IRC {#server-mode-irc}

Crée une destination qui filtre la séquence d'enregistrement d'un client et transmet la clé de destination du client comme nom d'hôte au serveur IRC.

### Streamr {#server-mode-streamr}

Un client UDP qui se connecte à un serveur multimédia est créé. Le client UDP est couplé avec un serveur Streamr I2PTunnel.
