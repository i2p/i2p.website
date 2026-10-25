---
title: "Nommage et Carnet d'Adresses"
description: "Comment I2P associe les noms d'hôtes lisibles par l'homme aux destinations"
slug: "naming"
aliases:
  - "/fr/docs/specs/naming"
  - "/fr/docs/specs/naming/"
  - "/fr/docs/naming"
  - "/fr/docs/naming/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Aperçu

I2P est livré avec une bibliothèque de nommage générique et une implémentation de base conçue pour fonctionner à partir d'un mappage local de noms vers destinations, ainsi qu'une application complémentaire appelée le [carnet d'adresses](#address-book). I2P prend également en charge les [noms d'hôtes Base32](#base32-names) similaires aux adresses .onion de Tor.

Le carnet d'adresses est un système de nommage sécurisé, distribué et lisible par l'homme, basé sur un réseau de confiance, qui ne sacrifie que l'exigence d'unicité globale de tous les noms lisibles par l'homme en imposant uniquement une unicité locale. Bien que tous les messages dans I2P soient adressés cryptographiquement par leur destination, différentes personnes peuvent avoir des entrées de carnet d'adresses locales pour "Alice" qui font référence à différentes destinations. Les gens peuvent toujours découvrir de nouveaux noms en important les carnets d'adresses publiés de pairs spécifiés dans leur réseau de confiance, en ajoutant les entrées fournies par un tiers, ou (si certaines personnes organisent une série de carnets d'adresses publiés utilisant un système d'enregistrement premier arrivé, premier servi) les gens peuvent choisir de traiter ces carnets d'adresses comme des serveurs de noms, émulant le DNS traditionnel.

NOTE : Pour comprendre les raisons derrière le système de nommage I2P, les arguments courants contre celui-ci et les alternatives possibles, consultez la page [discussion sur le nommage](/docs/legacy/naming/).

---

## Composants du Système de Nommage

Il n'y a pas d'autorité de nommage centralisée dans I2P. Tous les noms d'hôtes sont locaux.

Le système de nommage est assez simple et la plupart de celui-ci est implémenté dans des applications externes au router, mais fournies avec la distribution I2P. Les composants sont :

1. Le [service de nommage](#naming-services) local qui effectue des recherches et gère également les [noms d'hôte Base32](#base32-names).
2. Le [proxy HTTP](#http-proxy) qui demande au router d'effectuer des recherches et dirige l'utilisateur vers des services de saut distants pour l'aider en cas d'échec de recherche.
3. Les [formulaires d'ajout d'hôte](#host-add-services) HTTP qui permettent aux utilisateurs d'ajouter des hôtes à leur fichier hosts.txt local.
4. Les [services de saut](#jump-services) HTTP qui fournissent leurs propres recherches et redirections.
5. L'application [carnet d'adresses](#address-book) qui fusionne les listes d'hôtes externes, récupérées via HTTP, avec la liste locale.
6. L'application [SusiDNS](#susidns) qui est une interface web simple pour la configuration du carnet d'adresses et la visualisation des listes d'hôtes locales.

---

## Services de nommage

Toutes les destinations dans I2P sont des clés de 516 octets (ou plus). (Pour être plus précis, il s'agit d'une clé publique de 256 octets plus une clé de signature de 128 octets plus un certificat de 3 octets ou plus, ce qui en représentation Base64 fait 516 octets ou plus. Les [Certificats](/docs/legacy/naming/#certificates) non nuls sont maintenant utilisés pour l'indication du type de signature. Par conséquent, les certificats dans les destinations générées récemment font plus de 3 octets.

Si une application (i2ptunnel ou le proxy HTTP) souhaite accéder à une destination par nom, le router effectue une recherche locale très simple pour résoudre ce nom.

### Service de nommage Hosts.txt

Le service de nommage hosts.txt effectue une recherche linéaire simple dans les fichiers texte. Ce service de nommage était celui par défaut jusqu'à la version 0.8.8 où il a été remplacé par le service de nommage Blockfile. Le format hosts.txt était devenu trop lent après que le fichier ait grandi pour contenir des milliers d'entrées.

Il effectue une recherche linéaire dans trois fichiers locaux, dans l'ordre, pour rechercher les noms d'hôte et les convertir en une clé de destination de 516 octets. Chaque fichier est dans un [format de fichier de configuration](/docs/specs/configuration/) simple, avec hostname=base64, un par ligne. Les fichiers sont :

1. privatehosts.txt
2. userhosts.txt
3. hosts.txt

### Service de nommage Blockfile

Le service de noms Blockfile stocke plusieurs "carnets d'adresses" dans un seul fichier de base de données nommé hostsdb.blockfile. Ce service de noms est celui par défaut depuis la version 0.8.8.

Un blockfile est simplement un stockage sur disque de plusieurs cartes triées (paires clé-valeur), implémenté sous forme de skiplists. Le format blockfile est spécifié sur la [page Blockfile](/docs/specs/blockfile/). Il fournit une recherche rapide de Destination dans un format compact. Bien que la surcharge du blockfile soit importante, les destinations sont stockées en binaire plutôt qu'en Base 64 comme dans le format hosts.txt. De plus, le blockfile offre la capacité de stockage de métadonnées arbitraires (telles que la date d'ajout, la source et les commentaires) pour chaque entrée afin d'implémenter des fonctionnalités avancées de carnet d'adresses. L'exigence de stockage du blockfile représente une augmentation modeste par rapport au format hosts.txt, et le blockfile fournit une réduction d'environ 10x des temps de recherche.

Lors de la création, le service de nommage importe les entrées des trois fichiers utilisés par le service de nommage hosts.txt. Le fichier bloc imite l'implémentation précédente en maintenant trois cartes qui sont recherchées dans l'ordre, nommées privatehosts.txt, userhosts.txt et hosts.txt. Il maintient également une carte de recherche inversée pour implémenter des recherches inversées rapides.

### Autres Services de Nommage

La recherche n'est pas sensible à la casse. La première correspondance est utilisée, et les conflits ne sont pas détectés. Il n'y a pas d'application des règles de nommage dans les recherches. Les recherches sont mises en cache pendant quelques minutes. La résolution Base 32 est [décrite ci-dessous](#base32-names). Pour une description complète de l'API du Service de Nommage, voir la [Javadoc du Service de Nommage](http://idk.i2p/javadoc-i2p/net/i2p/client/naming/package-summary.html). Cette API a été considérablement étendue dans la version 0.8.7 pour fournir des ajouts et suppressions, le stockage de propriétés arbitraires avec le nom d'hôte, et d'autres fonctionnalités.

### Services de nommage alternatifs et expérimentaux

Le service de nommage est spécifié avec la propriété de configuration `i2p.naming.impl=class`. D'autres implémentations sont possibles. Par exemple, il existe une fonctionnalité expérimentale pour les recherches en temps réel (à la manière du DNS) sur le réseau au sein du router. Pour plus d'informations, voir les [alternatives sur la page de discussion](/docs/legacy/naming/#alternatives).

Le proxy HTTP effectue une recherche via le router pour tous les noms d'hôte se terminant par '.i2p'. Sinon, il transmet la requête à un outproxy HTTP configuré. Ainsi, en pratique, tous les noms d'hôte HTTP (I2P Site) doivent se terminer par le pseudo-domaine de premier niveau '.i2p'.

Si le router ne parvient pas à résoudre le nom d'hôte, le proxy HTTP renvoie une page d'erreur à l'utilisateur avec des liens vers plusieurs services de "saut". Voir ci-dessous pour les détails.

---

## Domaine .i2p.alt

Nous avons précédemment [demandé à réserver le TLD .i2p](https://datatracker.ietf.org/doc/draft-grothoff-iesg-special-use-p2p-names/) en suivant les procédures spécifiées dans la [RFC 6761](https://www.rfc-editor.org/rfc/rfc6761.html). Cependant, cette demande et toutes les autres ont été rejetées, et la RFC 6761 a été déclarée comme une "erreur".

Après de nombreuses années de travail par l'équipe GNUnet et d'autres, le domaine .alt a été réservé comme TLD à usage spécial dans la [RFC 9476](https://www.rfc-editor.org/rfc/rfc9476.html) à la fin de 2023. Bien qu'il n'y ait pas de registraires officiels sanctionnés par l'IANA, nous avons enregistré le domaine .i2p.alt auprès du registraire non officiel principal [GANA](https://gana.gnunet.org/dot-alt/dot_alt.html). Cela n'empêche pas d'autres personnes d'utiliser le domaine, mais cela devrait aider à le décourager.

Un avantage du domaine .alt est que, en théorie, les résolveurs DNS ne transmettront pas les requêtes .alt une fois qu'ils seront mis à jour pour se conformer à la RFC 9476, ce qui empêchera les fuites DNS. Pour assurer la compatibilité avec les noms d'hôte .i2p.alt, les logiciels et services I2P devraient être mis à jour pour gérer ces noms d'hôte en supprimant le TLD .alt. Ces mises à jour sont prévues pour la première moitié de 2024.

À l'heure actuelle, il n'y a pas de plans pour faire de .i2p.alt la forme préférée pour l'affichage et l'échange des noms d'hôtes I2P. C'est un sujet qui nécessite des recherches et discussions supplémentaires.

---

## Carnet d'adresses

### Abonnements entrants et fusion

L'application de carnet d'adresses récupère périodiquement les fichiers hosts.txt d'autres utilisateurs et les fusionne avec le fichier hosts.txt local, après plusieurs vérifications. Les conflits de nommage sont résolus selon le principe du premier arrivé, premier servi.

S'abonner au fichier hosts.txt d'un autre utilisateur implique de lui accorder une certaine confiance. Vous ne voulez pas qu'il « détourne » un nouveau site, par exemple, en saisissant rapidement sa propre clé pour un nouveau site avant de vous transmettre la nouvelle entrée hôte/clé.

Pour cette raison, le seul abonnement configuré par défaut est `http://i2p-projekt.i2p/hosts.txt (http://udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p/hosts.txt)`, qui contient une copie du fichier hosts.txt inclus dans la version I2P. Les utilisateurs doivent configurer des abonnements supplémentaires dans leur application de carnet d'adresses local (via subscriptions.txt ou [SusiDNS](#susidns)).

Quelques autres liens d'abonnement au carnet d'adresses public :

- http://i2host.i2p/cgi-bin/i2hostetag
- http://stats.i2p/cgi-bin/newhosts.txt

Les opérateurs de ces services peuvent avoir différentes politiques pour lister les hôtes. La présence sur cette liste n'implique pas une approbation.

### Règles de nommage

Bien qu'il n'y ait espérons-le aucune limitation technique au sein d'I2P concernant les noms d'hôte, le carnet d'adresses applique plusieurs restrictions sur les noms d'hôte importés depuis les abonnements. Il fait cela pour une cohérence typographique de base et la compatibilité avec les navigateurs, ainsi que pour la sécurité. Les règles sont essentiellement les mêmes que celles de la RFC2396 Section 3.2.2. Tout nom d'hôte violant ces règles pourrait ne pas être propagé vers d'autres routers.

Règles de nommage :

- Les noms sont convertis en minuscules lors de l'importation.
- Les noms sont vérifiés pour éviter les conflits avec les noms existants dans userhosts.txt et hosts.txt (mais pas privatehosts.txt) après conversion en minuscules.
- Doivent contenir uniquement [a-z] [0-9] '.' et '-' après conversion en minuscules.
- Ne doivent pas commencer par '.' ou '-'.
- Doivent se terminer par '.i2p'.
- 67 caractères maximum, incluant le '.i2p'.
- Ne doivent pas contenir '..'.
- Ne doivent pas contenir '.-' ou '-.' (depuis la version 0.6.1.33).
- Ne doivent pas contenir '--' sauf dans 'xn--' pour IDN.
- Les noms d'hôtes Base32 (*.b32.i2p) sont réservés pour l'utilisation base 32 et ne sont donc pas autorisés à l'importation.
- Certains noms d'hôtes réservés pour l'usage du projet ne sont pas autorisés (proxy.i2p, router.i2p, console.i2p, mail.i2p, *.proxy.i2p, *.router.i2p, *.console.i2p, *.mail.i2p, et autres)
- Les noms d'hôtes commençant par 'www.' sont découragés et sont rejetés par certains services d'enregistrement. Certaines implémentations d'addressbook suppriment automatiquement les préfixes 'www.' des recherches. Ainsi, enregistrer 'www.example.i2p' est inutile, et enregistrer une destination différente pour 'www.example.i2p' et 'example.i2p' rendra 'www.example.i2p' inaccessible pour certains utilisateurs.
- Les clés sont vérifiées pour la validité base64.
- Les clés sont vérifiées pour éviter les conflits avec les clés existantes dans hosts.txt (mais pas privatehosts.txt).
- Longueur minimale de clé : 516 octets.
- Longueur maximale de clé : 616 octets (pour tenir compte des certificats jusqu'à 100 octets).

Tout nom reçu via abonnement qui réussit toutes les vérifications est ajouté via le service de nommage local.

Notez que les symboles '.' dans un nom d'hôte n'ont aucune signification et ne dénotent aucune hiérarchie réelle de nommage ou de confiance. Si le nom 'host.i2p' existe déjà, rien n'empêche quiconque d'ajouter un nom 'a.host.i2p' à son hosts.txt, et ce nom peut être importé par le carnet d'adresses d'autres utilisateurs. Les méthodes pour refuser les sous-domaines aux non-'propriétaires' de domaine (certificats ?), ainsi que la désirabilité et la faisabilité de ces méthodes, sont des sujets de discussion future.

Les noms de domaine internationalisés (IDN) fonctionnent également dans i2p (en utilisant la forme punycode 'xn--'). Pour voir les noms de domaine IDN .i2p affichés correctement dans la barre d'adresse de Firefox, ajoutez 'network.IDN.whitelist.i2p (boolean) = true' dans about:config.

Comme l'application carnet d'adresses n'utilise pas du tout privatehosts.txt, en pratique ce fichier est le seul endroit où il est approprié de placer des alias privés ou des "noms familiers" pour des sites déjà présents dans hosts.txt.

### Format avancé de flux d'abonnement

À partir de la version 0.9.26, les sites d'abonnement et les clients peuvent prendre en charge un protocole avancé de flux hosts.txt qui inclut des métadonnées y compris des signatures. Ce format est rétrocompatible avec le format standard hosts.txt hostname=base64destination. Consultez [la spécification](/docs/specs/subscription/) pour plus de détails.

### Abonnements sortants

Address Book publiera le fichier hosts.txt fusionné vers un emplacement (traditionnellement hosts.txt dans le répertoire racine du site I2P local) pour être accessible par d'autres utilisateurs pour leurs abonnements. Cette étape est optionnelle et est désactivée par défaut.

### Problèmes d'hébergement et de transport HTTP

L'application carnet d'adresses, avec eepget, sauvegarde les informations Etag et/ou Last-Modified retournées par le serveur web de l'abonnement. Ceci réduit considérablement la bande passante requise, car le serveur web retournera un '304 Not Modified' lors de la prochaine récupération si rien n'a changé.

Cependant, l'intégralité du fichier hosts.txt est téléchargée s'il a été modifié. Voir ci-dessous pour une discussion sur ce problème.

Les hôtes servant un fichier hosts.txt statique ou une application CGI équivalente sont fortement encouragés à fournir un en-tête Content-Length, ainsi qu'un en-tête Etag ou Last-Modified. Assurez-vous également que le serveur renvoie un '304 Not Modified' le cas échéant. Cela réduira considérablement la bande passante réseau et diminuera les risques de corruption.

---

## Services d'ajout d'hôtes

Un service d'ajout d'hôte est une application CGI simple qui prend un nom d'hôte et une clé Base64 comme paramètres et les ajoute à son fichier hosts.txt local. Si d'autres routers s'abonnent à ce fichier hosts.txt, le nouveau nom d'hôte/clé sera propagé à travers le réseau.

Il est recommandé que les services d'ajout d'hôtes imposent, au minimum, les restrictions imposées par l'application de carnet d'adresses listée ci-dessus. Les services d'ajout d'hôtes peuvent imposer des restrictions supplémentaires sur les noms d'hôtes et les clés, par exemple :

- Une limite sur le nombre de 'sous-domaines'.
- Autorisation pour les 'sous-domaines' par diverses méthodes.
- Hashcash ou certificats signés.
- Révision éditoriale des noms d'hôtes et/ou du contenu.
- Catégorisation des hôtes par contenu.
- Réservation ou rejet de certains noms d'hôtes.
- Restrictions sur le nombre de noms enregistrés dans une période donnée.
- Délais entre l'enregistrement et la publication.
- Exigence que l'hôte soit actif pour vérification.
- Expiration et/ou révocation.
- Rejet d'usurpation IDN.

---

## Services de redirection

Un service de saut est une application CGI simple qui prend un nom d'hôte comme paramètre et retourne une redirection 301 vers l'URL appropriée avec une chaîne `?i2paddresshelper=key` ajoutée. Le proxy HTTP interprétera la chaîne ajoutée et utilisera cette clé comme destination réelle. De plus, le proxy mettra cette clé en cache de sorte que l'assistant d'adresse ne soit pas nécessaire jusqu'au redémarrage.

Notez que, comme pour les abonnements, l'utilisation d'un service de saut implique un certain niveau de confiance, car un service de saut pourrait malicieusement rediriger un utilisateur vers une destination incorrecte.

Pour fournir le meilleur service, un service de saut devrait s'abonner à plusieurs fournisseurs de hosts.txt afin que sa liste d'hôtes locale soit à jour.

---

## SusiDNS

SusiDNS est simplement une interface web frontale pour configurer les abonnements aux carnets d'adresses et accéder aux quatre fichiers de carnet d'adresses. Tout le véritable travail est effectué par l'application 'address book'.

Actuellement, il y a peu d'application des règles de nommage du carnet d'adresses dans SusiDNS, donc un utilisateur peut saisir localement des noms d'hôte qui seraient rejetés par les règles d'abonnement du carnet d'adresses.

---

## Noms Base32

I2P prend en charge les noms d'hôte Base32 similaires aux adresses .onion de Tor. Les adresses Base32 sont beaucoup plus courtes et plus faciles à gérer que les Destinations Base64 complètes de 516 caractères ou les addresshelpers. Exemple : `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`

Dans Tor, l'adresse fait 16 caractères (80 bits), soit la moitié du hachage SHA-1. I2P utilise 52 caractères (256 bits) pour représenter le hachage SHA-256 complet. La forme est {52 caractères}.b32.i2p. Tor a une [proposition](https://blog.torproject.org/blog/tor-weekly-news-%E2%80%94-december-4th-2013) pour convertir vers un format identique de {52 caractères}.onion pour leurs services cachés. Base32 est implémenté dans le service de noms, qui interroge le router via I2CP pour rechercher le leaseSet afin d'obtenir la Destination complète. Les recherches Base32 ne réussiront que lorsque la Destination est active et publie un leaseSet. Comme la résolution peut nécessiter une recherche dans la base de données réseau, elle peut prendre significativement plus de temps qu'une recherche dans le carnet d'adresses local.

Les adresses Base32 peuvent être utilisées dans la plupart des endroits où des noms d'hôtes ou des destinations complètes sont utilisés, cependant il existe quelques exceptions où elles peuvent échouer si le nom ne se résout pas immédiatement. I2PTunnel échouera, par exemple, si le nom ne se résout pas vers une destination.

---

## Noms Base32 Étendus

Les noms base 32 étendus ont été introduits dans la version 0.9.40 pour prendre en charge les leaseSet chiffrés. Les adresses pour les leaseSet chiffrés sont identifiées par 56 caractères encodés ou plus, sans inclure le ".b32.i2p" (35 octets décodés ou plus), comparé à 52 caractères (32 octets) pour les adresses base 32 traditionnelles. Voir les propositions 123 et 149 pour des informations supplémentaires.

Les adresses Base 32 standard ("b32") contiennent le hachage de la destination. Cela ne fonctionnera pas pour les ls2 chiffrés (proposition 123).

Vous ne pouvez pas utiliser une adresse base 32 traditionnelle pour un LS2 chiffré (proposition 123), car elle ne contient que le hash de la destination. Elle ne fournit pas la clé publique non-aveuglée. Les clients doivent connaître la clé publique de la destination, le type de sig, le type de sig aveuglée, et une clé secrète ou privée optionnelle pour récupérer et déchiffrer le leaseSet. Par conséquent, une adresse base 32 seule est insuffisante. Le client a besoin soit de la destination complète (qui contient la clé publique), soit de la clé publique seule. Si le client a la destination complète dans un carnet d'adresses, et que le carnet d'adresses prend en charge la recherche inversée par hash, alors la clé publique peut être récupérée.

Nous avons donc besoin d'un nouveau format qui place la clé publique au lieu du hash dans une adresse base32. Ce format doit également contenir le type de signature de la clé publique et le type de signature du schéma de masquage.

Cette section documente un nouveau format b32 pour ces adresses. Bien que nous ayons fait référence à ce nouveau format lors des discussions comme une adresse "b33", le nouveau format actuel conserve le suffixe habituel ".b32.i2p".

### Création et encodage

Construisez un nom d'hôte de {56+ caractères}.b32.i2p (35+ caractères en binaire) comme suit. D'abord, construisez les données binaires à encoder en base 32 :

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Post-traitement et somme de contrôle :

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Tous les bits inutilisés à la fin du b32 doivent être 0. Il n'y a pas de bits inutilisés pour une adresse standard de 56 caractères (35 octets).

### Décodage et Vérification

```
Strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes) :
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits de Clé Secrète et Privée

Les bits de clé secrète et privée sont utilisés pour indiquer aux clients, proxies, ou autres codes côté client que la clé secrète et/ou privée sera requise pour déchiffrer le leaseSet. Des implémentations particulières peuvent inviter l'utilisateur à fournir les données requises, ou rejeter les tentatives de connexion si les données requises sont manquantes.

### Notes

- Le XOR des 3 premiers octets avec le hachage fournit une capacité de checksum limitée, et garantit que tous les caractères base32 au début sont randomisés. Seules quelques combinaisons de flag et sigtype sont valides, donc toute faute de frappe est susceptible de créer une combinaison invalide et sera rejetée.
- Dans le cas habituel (sigtypes de 1 octet, pas de secret, pas d'authentification par client), le nom d'hôte sera {56 chars}.b32.i2p, décodant vers 35 octets, comme pour Tor.
- Le checksum 2 octets de Tor a un taux de faux négatifs de 1/64K. Avec 3 octets, moins quelques octets ignorés, le nôtre approche 1 sur un million, puisque la plupart des combinaisons flag/sigtype sont invalides.
- Adler-32 est un mauvais choix pour les petites entrées, et pour détecter de petits changements. Nous utilisons CRC-32 à la place. CRC-32 est rapide et largement disponible.
- Bien que cela sorte du cadre de cette spécification, les routers et/ou clients doivent se souvenir et mettre en cache (probablement de manière persistante) la correspondance de clé publique vers destination, et vice versa.
- Distinguer les anciennes des nouvelles variantes par la longueur. Les anciennes adresses b32 sont toujours {52 chars}.b32.i2p. Les nouvelles sont {56+ chars}.b32.i2p
- Le fil de discussion Tor [est ici](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)
- Ne vous attendez pas à ce que les sigtypes 2 octets arrivent jamais, nous n'en sommes qu'à 13. Pas besoin d'implémenter maintenant.
- Le nouveau format peut être utilisé dans les liens de redirection (et servi par les serveurs de redirection) si désiré, tout comme b32.
- Tout secret, clé privée, ou clé publique de plus de 32 octets dépasserait la longueur maximale d'étiquette DNS de 63 caractères. Les navigateurs ne s'en soucient probablement pas.
- Aucun problème de rétrocompatibilité. Les adresses b32 plus longues échoueront à être converties en hachages 32 octets dans les anciens logiciels.
