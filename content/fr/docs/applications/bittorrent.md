---
title: "Bittorrent sur I2P"
description: "Spécifications de protocole pour les clients et trackers BitTorrent sur I2P"
slug: "bittorrent"
lastUpdated: "2026-08"
accurateFor: "0.9.70"
---

Il existe plusieurs clients BitTorrent et trackers sur I2P. Comme l'adressage I2P utilise une Destination au lieu d'une IP et d'un port, des modifications mineures sont nécessaires pour que les logiciels de tracker et de client fonctionnent sur I2P. Ces modifications sont spécifiées ci-dessous. Notez bien les directives pour la compatibilité avec les anciens clients et trackers I2P.

Cette page spécifie les détails de protocole communs à tous les clients et trackers. Des clients et trackers spécifiques peuvent implémenter d'autres fonctionnalités ou protocoles uniques.

Nous encourageons les portages supplémentaires de logiciels clients et trackers vers I2P.

---

## Guide général pour les développeurs

La plupart des clients bittorrent non-Java se connecteront à I2P via [SAMv3](/docs/api/samv3/). Les sessions SAM (ou à l'intérieur d'I2P, les pools de tunnel ou ensembles de tunnels) sont conçues pour être durables. La plupart des clients bittorrent n'auront besoin que d'une seule session, créée au démarrage et fermée à la sortie. I2P est différent de Tor, où les circuits peuvent être créés et supprimés rapidement. Réfléchissez bien et consultez les développeurs I2P avant de concevoir votre application pour utiliser plus d'une ou deux sessions simultanées, ou pour les créer et les supprimer rapidement. Les clients bittorrent ne doivent pas créer une session unique pour chaque connexion. Concevez votre client pour utiliser la même session pour les annonces et les connexions client.

De plus, veuillez vous assurer que les paramètres de votre client (et les conseils aux utilisateurs concernant les paramètres du router, ou les paramètres par défaut du router si vous incluez un router) permettront à vos utilisateurs de contribuer plus de ressources au réseau qu'ils n'en consomment. I2P est un réseau pair-à-pair, et le réseau ne peut survivre si une application populaire pousse le réseau vers une congestion permanente.

Ne fournissez pas de support pour bittorrent via un outproxy I2P vers le clearnet car il sera probablement bloqué. Consultez les opérateurs d'outproxy pour obtenir des conseils.

Les implémentations router Java I2P et i2pd sont indépendantes et présentent des différences mineures de comportement, de support des fonctionnalités et de paramètres par défaut. Veuillez tester votre application avec la dernière version des deux routers.

SAM d'i2pd est activé par défaut ; SAM de Java I2P ne l'est pas. Fournissez des instructions à vos utilisateurs sur comment activer SAM dans Java I2P (via /configclients dans la console du router), et/ou fournissez un bon message d'erreur à l'utilisateur si la connexion initiale échoue, par exemple "assurez-vous qu'I2P fonctionne et que l'interface SAM est activée".

Les routeurs Java I2P et i2pd ont des valeurs par défaut différentes pour les quantités de tunnels. La valeur par défaut de Java est 2 et celle d'i2pd est 5. Pour la plupart des utilisations avec une bande passante faible à moyenne et un nombre de connexions faible à moyen, 3 est suffisant. Veuillez spécifier la quantité de tunnels dans le message SESSION CREATE pour obtenir des performances cohérentes avec les routeurs Java I2P et i2pd.

I2P prend en charge plusieurs types de signature et de chiffrement. Pour des raisons de compatibilité, I2P utilise par défaut des types anciens et inefficaces, donc tous les clients devraient spécifier des types plus récents.

Si vous utilisez SAM, le type de signature est spécifié dans les commandes DEST GENERATE et SESSION CREATE (pour les sessions transitoires). Tous les clients doivent définir SIGNATURE_TYPE=7 (Ed25519).

Le type de chiffrement est spécifié dans la commande SAM SESSION CREATE ou dans les options i2cp. Plusieurs types de chiffrement sont autorisés. Certains trackers supportent ECIES-X25519, certains supportent ElGamal, et certains supportent les deux. Les clients devraient définir i2cp.leaseSetEncType=4,0 (pour ECIES-X25519 et ElGamal) afin de pouvoir se connecter aux deux.

La prise en charge de DHT nécessite SAMv3.3 PRIMARY et SUBSESSIONS pour TCP et UDP sur la même session. Cela nécessitera un effort de développement substantiel côté client, à moins que le client ne soit écrit en Java. i2pd ne prend actuellement pas en charge SAMv3.3. libtorrent ne prend actuellement pas en charge SAMv3.3.

Sans prise en charge DHT, vous pourriez souhaiter annoncer automatiquement à une liste configurable de trackers ouverts connus afin que les liens magnet fonctionnent. Consultez les utilisateurs I2P pour obtenir des informations sur les trackers ouverts actuellement en service et maintenez vos paramètres par défaut à jour. La prise en charge de l'extension i2p_pex aidera également à pallier l'absence de support DHT.

Pour plus de conseils aux développeurs sur la façon de s'assurer que votre application utilise uniquement les ressources dont elle a besoin, veuillez consulter la [spécification SAMv3](/docs/api/samv3/) et [notre guide pour intégrer I2P avec votre application](/docs/applications/embedding/). Contactez les développeurs I2P ou i2pd pour obtenir une assistance supplémentaire.

---

## Annonces

Les clients incluent généralement un faux paramètre port=6881 dans l'annonce, pour la compatibilité avec les trackers plus anciens. Les trackers peuvent ignorer le paramètre port et ne devraient pas l'exiger.

Le paramètre ip est le base 64 de la [Destination](/docs/specs/common-structures/#struct_Destination) du client, utilisant l'alphabet I2P Base 64 [A-Z][a-z][0-9]-~. Les [Destinations](/docs/specs/common-structures/#struct_Destination) font 387+ octets, donc le Base 64 fait 516+ octets. Les clients ajoutent généralement ".i2p" à la Destination Base 64 pour la compatibilité avec les anciens trackers. Les trackers ne devraient pas exiger un ".i2p" ajouté.

Les autres paramètres sont les mêmes que dans le bittorrent standard.

Les Destinations actuelles pour les clients font 387 octets ou plus (516 ou plus en encodage Base 64). Un maximum raisonnable à supposer, pour l'instant, est de 475 octets. Comme le tracker doit décoder le Base64 pour délivrer des réponses compactes (voir ci-dessous), le tracker devrait probablement décoder et rejeter le Base64 incorrect lors de l'annonce.

Le type de réponse par défaut est non-compact. Les clients peuvent demander une réponse compacte avec le paramètre compact=1. Un tracker peut, mais n'est pas obligé de, retourner une réponse compacte lorsqu'elle est demandée. Note : Tous les trackers populaires supportent maintenant les réponses compactes et au moins un exige compact=1 dans l'annonce. Tous les clients devraient demander et supporter les réponses compactes.

Les développeurs de nouveaux clients I2P sont fortement encouragés à implémenter les annonces via leur propre tunnel plutôt que par le proxy client HTTP sur le port 4444. Cette approche est à la fois plus efficace et permet l'application de l'authentification de destination par le tracker (voir ci-dessous).

La spécification pour les annonces UDP a été finalisée en juin 2025. La prise en charge dans divers clients I2P et trackers sera déployée plus tard en 2025. Voir ci-dessous pour des informations supplémentaires.

---

## Réponses de Tracker Non-Compactes

Note : Obsolète. Tous les trackers populaires prennent désormais en charge les réponses compactes et au moins un exige compact=1 dans l'annonce. Tous les clients devraient demander et prendre en charge les réponses compactes.

La réponse non-compacte est identique à celle du bittorrent standard, avec une "ip" I2P. Il s'agit d'une longue "chaîne DNS" encodée en base64, probablement avec un suffixe ".i2p".

Les trackers incluent généralement une clé de port factice, ou utilisent le port de l'annonce, pour la compatibilité avec les anciens clients. Les clients doivent ignorer le paramètre de port et ne devraient pas l'exiger.

La valeur de la clé ip est le base 64 de la [Destination](/docs/specs/common-structures/#struct_Destination) du client, comme décrit ci-dessus. Les trackers ajoutent généralement ".i2p" à la Destination Base 64 si elle n'était pas présente dans l'ip de l'annonce, pour la compatibilité avec les clients plus anciens. Les clients ne doivent pas exiger un ".i2p" ajouté dans les réponses.

Les autres clés et valeurs de réponse sont identiques à celles du bittorrent standard.

---

## Réponses de Tracker Compactes

Dans la réponse compacte, la valeur de la clé de dictionnaire "peers" est une chaîne d'octets unique, dont la longueur est un multiple de 32 octets. Cette chaîne contient les [hachages SHA-256 de 32 octets](/docs/specs/common-structures/#type_Hash) concaténés des [Destinations](/docs/specs/common-structures/#struct_Destination) binaires des pairs. Ce hachage doit être calculé par le tracker, sauf si l'application de destination (voir ci-dessous) est utilisée, auquel cas le hachage livré dans les en-têtes HTTP X-I2P-DestHash ou X-I2P-DestB32 peut être converti en binaire et stocké. La clé peers peut être absente, ou la valeur peers peut avoir une longueur nulle.

Bien que le support des réponses compactes soit optionnel pour les clients et les trackers, il est fortement recommandé car il réduit la taille nominale des réponses de plus de 90%.

---

## Application des Destinations

Certains clients BitTorrent I2P, mais pas tous, annoncent via leurs propres tunnels. Les trackers peuvent choisir de prévenir l'usurpation d'identité en l'exigeant, et en vérifiant la [Destination](/docs/specs/common-structures/#struct_Destination) du client en utilisant les en-têtes HTTP ajoutés par le tunnel I2PTunnel HTTP Server. Les en-têtes sont X-I2P-DestHash, X-I2P-DestB64, et X-I2P-DestB32, qui sont différents formats pour la même information. Ces en-têtes ne peuvent pas être usurpés par le client. Un tracker appliquant les destinations n'a pas du tout besoin d'exiger le paramètre d'annonce ip.

Comme plusieurs clients utilisent le proxy HTTP au lieu de leur propre tunnel pour les annonces, l'application de la destination empêchera l'utilisation par ces clients à moins ou jusqu'à ce que ces clients soient convertis pour annoncer via leur propre tunnel.

Malheureusement, à mesure que le réseau grandit, la quantité de malveillance augmentera également, nous nous attendons donc à ce que tous les trackers finissent par imposer des destinations. Les développeurs de trackers et de clients devraient s'y préparer.

---

## Annoncer les noms d'hôtes

Les noms d'hôtes des URL d'annonce dans les fichiers torrent suivent généralement les [standards de nommage I2P](/docs/overview/naming/). En plus des noms d'hôtes provenant des carnets d'adresses et des noms d'hôtes Base 32 ".b32.i2p", la Destination Base 64 complète (avec ou sans ".i2p" ajouté) devrait être prise en charge. Les trackers non-ouverts devraient reconnaître leur propre nom d'hôte dans n'importe lequel de ces formats.

Pour préserver l'anonymat, les clients devraient généralement ignorer les URL d'annonce non-I2P dans les fichiers torrent.

---

## Connexions client

Les connexions client-à-client utilisent le protocole standard sur TCP. Il n'y a pas de clients I2P connus qui prennent actuellement en charge la communication uTP.

I2P utilise des [Destinations](/docs/specs/common-structures/#struct_Destination) de 387+ octets pour les adresses, comme expliqué ci-dessus.

Si le client n'a que le hash de la destination (comme dans une réponse compacte ou PEX), il doit effectuer une recherche en l'encodant avec Base 32, en ajoutant ".b32.i2p", et en interrogeant le service de nommage, qui retournera la destination complète si elle est disponible.

Si le client possède la Destination complète d'un pair qu'il a reçue dans une réponse non-compacte, il devrait l'utiliser directement lors de la configuration de la connexion. Ne convertissez pas une Destination en hash Base 32 pour la recherche, c'est assez inefficace.

---

## Prévention Inter-Réseaux

Pour préserver l'anonymat, les clients bittorrent I2P ne prennent généralement pas en charge les annonces ou connexions de pairs non-I2P. Les proxies de sortie HTTP I2P bloquent souvent les annonces. Il n'existe aucun proxy de sortie SOCKS connu prenant en charge le trafic bittorrent.

Pour empêcher l'utilisation par des clients non-I2P via un proxy entrant HTTP, les trackers I2P bloquent souvent les accès ou annonces qui contiennent un en-tête HTTP X-Forwarded-For. Les trackers devraient rejeter les annonces de réseau standard avec des IP IPv4 ou IPv6, et ne pas les transmettre dans les réponses.

---

## PEX

I2P PEX est basé sur ut_pex. Comme il ne semble pas y avoir de spécification formelle d'ut_pex disponible, il peut être nécessaire d'examiner le code source de libtorrent pour obtenir de l'aide. C'est un message d'extension, identifié comme "i2p_pex" dans [la négociation d'extension](http://www.bittorrent.org/beps/bep_0010.html). Il contient un dictionnaire bencodé avec jusqu'à 3 clés, "added", "added.f", et "dropped". Les valeurs added et dropped sont chacune une chaîne d'octets unique, dont la longueur est un multiple de 32 octets. Ces chaînes d'octets sont les hachages SHA-256 concaténés des [Destinations](/docs/specs/common-structures/#struct_Destination) binaires des pairs. C'est le même format que la valeur du dictionnaire peers dans le format de réponse compacte i2p spécifié ci-dessus. La valeur added.f, si présente, est la même que dans ut_pex.

---

## DHT

Le support DHT est inclus dans le client i2psnark depuis la version 0.9.2. Les différences préliminaires par rapport à [BEP 5](http://www.bittorrent.org/beps/bep_0005.html) sont décrites ci-dessous et sont sujettes à changement. Contactez les développeurs I2P si vous souhaitez développer un client supportant DHT.

Contrairement au DHT standard, le DHT I2P n'utilise pas un bit dans la négociation des options, ou le message PORT. Il est annoncé avec un message d'extension, identifié comme "i2p_dht" dans [la négociation d'extension](http://www.bittorrent.org/beps/bep_0010.html). Il contient un dictionnaire bencodé avec deux clés, "port" et "rport", toutes deux des entiers.

Le port UDP (datagram) listé dans les informations de nœud compactes est utilisé pour recevoir des datagrammes auxquels on peut répondre (signés). Ceci est utilisé pour les requêtes, à l'exception des annonces. Nous appelons ceci le "port de requête". Il s'agit de la valeur "port" du message d'extension. Les requêtes utilisent le numéro de protocole [I2CP](/docs/specs/i2cp/) 17.

En plus de ce port UDP, nous utilisons un second port de datagramme égal au port de requête + 1. Celui-ci est utilisé pour recevoir des datagrammes non signés (bruts) pour les réponses, erreurs et annonces. Ce port offre une efficacité accrue car les réponses contiennent des jetons envoyés dans la requête, et n'ont pas besoin d'être signées. Nous appelons ceci le "port de réponse". Il s'agit de la valeur "rport" du message d'extension. Il doit être égal à 1 + le port de requête. Les réponses et annonces utilisent le protocole [I2CP](/docs/specs/i2cp/) numéro 18.

Les informations de pair compactes font 32 octets (hachage SHA256 de 32 octets) au lieu de 4 octets d'IP + 2 octets de port. Il n'y a pas de port de pair. Dans une réponse, la clé "values" est une liste de chaînes, chacune contenant une seule information de pair compacte.

L'information de nœud compacte fait 54 octets (20 octets d'ID de nœud + 32 octets de hachage SHA256 + 2 octets de port) au lieu de 20 octets d'ID de nœud + 4 octets d'IP + 2 octets de port. Dans une réponse, la clé "nodes" est une chaîne d'octets unique avec les informations de nœud compactes concaténées.

Exigence d'ID de nœud sécurisé : Pour rendre plus difficiles diverses attaques DHT, les 4 premiers octets de l'ID de nœud doivent correspondre aux 4 premiers octets du hash de destination, et les deux octets suivants de l'ID de nœud doivent correspondre aux deux octets suivants du hash de destination avec un OU exclusif avec le port.

Dans un fichier torrent, la clé "nodes" du dictionnaire torrent sans tracker est à déterminer. Elle pourrait être une liste de chaînes binaires de 32 octets (hachages SHA256) au lieu d'une liste de listes contenant une chaîne d'hôte et un entier de port. Alternatives : Une seule chaîne d'octets avec des hachages concaténés, ou une liste de chaînes seules.

---

## Trackers Datagram (UDP)

La spécification pour les annonces UDP dans I2P a été finalisée en juin 2025. Le support dans divers clients I2P et trackers sera déployé plus tard en 2025. Les différences par rapport à [BEP 15](http://www.bittorrent.org/beps/bep_0015.html) sont documentées dans [la spécification des annonces UDP](/docs/specs/udp-announces/). La spécification nécessite également le support des [nouveaux formats Datagram 2/3](/docs/specs/datagrams/).

---

## Informations supplémentaires

Une spécification préliminaire pour le calcul de l'ensemble rapide autorisé se trouve dans la [Proposition 172](/proposals/172-bep6-allowed-fast)

---

## Informations supplémentaires

- Les standards I2P bittorrent sont généralement discutés sur [zzz.i2p](http://zzz.i2p/).
- Un tableau des capacités actuelles des logiciels de tracker est [également disponible là-bas](http://zzz.i2p/files/trackers.html).
- La [FAQ I2P bittorrent](http://forum.i2p/viewtopic.php?t=2068)
- [Discussion sur DHT sur I2P](http://zzz.i2p/topics/812)
