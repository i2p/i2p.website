---
title: "Commandes du flux d'abonnement aux adresses"
description: "Extension des flux d’abonnement d’adresses, permettant aux titulaires de noms d’hôte de mettre à jour et de gérer leurs entrées"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Aperçu

Cette spécification étend le flux d’abonnement aux adresses avec des commandes, permettant aux serveurs de noms de diffuser des mises à jour des entrées provenant des détenteurs de noms d’hôte. Proposée à l’origine dans [Proposal 112](/proposals/112-addressbook-subscription-feed-commands/) (septembre 2014), implémentée dans la version 0.9.26 (juin 2016) et déployée à l’échelle du réseau avec le statut CLOSED.

Le système est resté stable et inchangé depuis sa mise en œuvre initiale, continuant à fonctionner à l’identique dans I2P 2.10.0 (Router API 0.9.65, septembre 2025).

## Motivation

Auparavant, les serveurs d’abonnement hosts.txt envoyaient des données uniquement dans un format hosts.txt simple :

```
example.i2p=b64destination
```
Ce format de base a créé plusieurs problèmes :

- Les détenteurs de noms d’hôte ne peuvent pas mettre à jour la Destination (identifiant public I2P) associée à leurs noms d’hôte (par exemple, pour mettre à niveau la clé de signature vers un type cryptographique plus robuste).
- Les détenteurs de noms d’hôte ne peuvent pas céder leurs noms d’hôte arbitrairement. Ils doivent remettre directement au nouveau titulaire les clés privées de la Destination correspondante.
- Il n’existe aucun moyen d’authentifier qu’un sous-domaine est contrôlé par le nom d’hôte de base correspondant. Cela n’est actuellement appliqué qu’individuellement par certains serveurs de noms.

## Conception

Cette spécification ajoute des directives au format hosts.txt. Grâce à ces directives, les serveurs de noms peuvent étendre leurs services afin de fournir des fonctionnalités supplémentaires. Les clients qui implémentent cette spécification peuvent recevoir ces fonctionnalités via le processus d’abonnement habituel.

Toutes les lignes de commande doivent être signées par la Destination correspondante. Cela garantit que les modifications ne sont effectuées qu’à la demande du titulaire du nom d’hôte.

## Implications en matière de sécurité

Cette spécification n'affecte pas l'anonymat.

On observe une augmentation du risque lié à la perte de contrôle d’une Destination key (clé associée à une Destination I2P), car toute personne qui l’obtient peut utiliser ces commandes pour apporter des modifications à tous les noms d’hôte associés. Cependant, ce n’est pas plus problématique que le statu quo, où quelqu’un qui obtient une Destination (identifiant I2P) peut usurper un nom d’hôte et prendre (partiellement) le contrôle de son trafic. Ce risque accru est compensé par la possibilité donnée aux détenteurs de noms d’hôte de modifier la Destination associée à un nom d’hôte s’ils estiment que la Destination a été compromise. Cela est impossible avec le système actuel.

## Spécification

### Nouveaux types de ligne

Il existe deux nouveaux types de lignes :

1. **Commandes Add et Change:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Supprimer les commandes:**

```
#!key1=val1#key2=val2...
```
#### Ordonnancement

Un flux n'est pas nécessairement dans l'ordre ni complet. Par exemple, une commande change peut apparaître sur une ligne avant une commande add, ou sans commande add.

Les clés peuvent être dans n'importe quel ordre. Les clés en double ne sont pas autorisées. Toutes les clés et les valeurs sont sensibles à la casse.

### Clés communes

**Requis dans toutes les commandes :**

**sig** : signature Base64, utilisant la clé de signature de la destination

**Références à un second nom d'hôte et/ou une destination:**

**oldname** : Un deuxième nom d’hôte (nouveau ou modifié)

**olddest** : Une deuxième destination Base64 (nouvelle ou modifiée)

**oldsig** : Une deuxième signature Base64, utilisant la clé de signature provenant de olddest

**Autres clés courantes :**

**action** : Une commande

**name** : Le nom d'hôte, présent uniquement s'il n'est pas précédé de `example.i2p=b64dest`

**dest** : La destination Base64, uniquement présente si elle n'est pas précédée de `example.i2p=b64dest`

**date** : En secondes depuis l'époque Unix

**expires** : En secondes depuis l'époque Unix

### Commandes

Toutes les commandes, à l’exception de la commande "Add", doivent contenir une paire clé/valeur `action=command`.

Pour assurer la compatibilité avec des clients plus anciens, la plupart des commandes sont précédées de `example.i2p=b64dest`, comme indiqué ci-dessous. En cas de modification, les valeurs indiquées sont toujours les nouvelles. Les anciennes valeurs sont incluses dans la section clé/valeur.

Les clés répertoriées sont obligatoires. Toutes les commandes peuvent contenir des paires clé-valeur supplémentaires non définies ici.

#### Ajouter un nom d'hôte

**Précédé par example.i2p=b64dest** : OUI, il s’agit du nouveau nom d’hôte et de la destination.

**action** : NON incluse, c'est implicite.

**sig** : signature

Exemple :

```
example.i2p=b64dest#!sig=b64sig
```
#### Modifier le nom d'hôte

**Précédé par example.i2p=b64dest** : OUI, c'est le nouveau nom d'hôte et l'ancienne destination.

**action** : changename

**oldname** : l'ancien nom d'hôte, à remplacer

**sig** : signature

Exemple:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Changer de destination

**Précédé de example.i2p=b64dest** : OUI, c’est l’ancien nom d’hôte et la nouvelle destination.

**action** : changedest

**olddest** : l'ancienne destination, à remplacer

**oldsig** : signature utilisant olddest

**sig** : signature

Exemple :

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Ajouter un alias de nom d’hôte

**Précédé de example.i2p=b64dest** : OUI, il s'agit du nouveau nom d'hôte (alias) et de l'ancienne destination.

**action** : addname

**oldname** : l'ancien nom d'hôte

**sig** : signature

Exemple :

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Ajouter un alias de destination

(Utilisé pour la mise à niveau cryptographique)

**Précédé par example.i2p=b64dest** : OUI, il s’agit de l’ancien nom d’hôte et de la nouvelle destination (alternative).

**action** : adddest

**olddest** : l'ancienne destination

**oldsig** : signature utilisant olddest

**sig** : signature utilisant dest

Exemple:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Ajouter un sous-domaine

**Précédé par subdomain.example.i2p=b64dest** : OUI, c'est le nouveau nom de sous-domaine et la destination.

**action** : addsubdomain

**oldname** : le nom d'hôte de niveau supérieur (example.i2p)

**olddest** : la destination de niveau supérieur (par exemple example.i2p)

**oldsig** : signature utilisant olddest

**sig** : signature utilisant dest

Exemple :

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Mettre à jour les métadonnées

**Précédé par example.i2p=b64dest** : OUI, il s'agit de l'ancien nom d'hôte et de la destination.

**action** : mise à jour

**sig** : signature

(ajoutez ici toutes les clés mises à jour)

Exemple:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Supprimer le nom d'hôte

**Précédé par example.i2p=b64dest** : NON, ceux-ci sont spécifiés dans les options

**action** : supprimer

**name** : le nom d'hôte

**dest** : la destination

**sig** : signature

Exemple:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Supprimer tout ayant cette destination

**Précédé par example.i2p=b64dest** : NON, cela est spécifié dans les options

**action** : removeall

**dest** : la destination

**sig** : signature

Exemple:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Signatures

Toutes les commandes doivent être signées par la Destination correspondante. Les commandes avec deux destinations peuvent nécessiter deux signatures.

`oldsig` est toujours la signature "interne". Signez et vérifiez sans que les clés `oldsig` ou `sig` soient présentes. `sig` est toujours la signature "externe". Signez et vérifiez avec la clé `oldsig` présente mais pas la clé `sig`.

#### Entrée pour les signatures

Pour générer un flux d'octets afin de créer ou de vérifier la signature, sérialisez comme suit :

1. Supprimez la clé `sig`
2. Si vous vérifiez avec `oldsig`, supprimez également la clé `oldsig`
3. Pour les commandes Add ou Change uniquement, émettez `example.i2p=b64dest`
4. S'il reste des clés, émettez `#!`
5. Triez les options par clé UTF-8, échouez en cas de clés en double
6. Pour chaque paire clé/valeur, émettez `key=value`, suivi (s'il ne s'agit pas de la dernière paire clé/valeur) d'un `#`

**Remarques**

- Ne pas produire de saut de ligne
- L'encodage de sortie est UTF-8
- Tout encodage de destination et de signature est en Base 64 utilisant l'alphabet I2P
- Les clés et les valeurs sont sensibles à la casse
- Les noms d'hôte doivent être en minuscules

#### Types de signature actuels

À partir de I2P 2.10.0, les types de signature suivants sont pris en charge pour les destinations :

- **EdDSA_SHA512_Ed25519** (Type 7): Le plus courant pour les destinations depuis la 0.9.15. Utilise une clé publique de 32 octets et une signature de 64 octets. C’est le type de signature recommandé pour les nouvelles destinations.
- **RedDSA_SHA512_Ed25519** (Type 13): Disponible uniquement pour les destinations et les leaseSets chiffrés (depuis la 0.9.39).
- Types hérités (DSA_SHA1, variantes ECDSA): Toujours pris en charge mais dépréciés pour les nouvelles identités de router depuis la 0.9.58.

Remarque : Des options cryptographiques post-quantiques sont disponibles depuis I2P 2.10.0, mais ne sont pas encore les types de signature par défaut.

## Compatibilité

Toutes les nouvelles lignes au format hosts.txt sont implémentées à l’aide de caractères de commentaire en tête (`#!`), de sorte que toutes les anciennes versions d’I2P interpréteront les nouvelles commandes comme des commentaires et les ignoreront proprement.

Lorsque les routers I2P sont mis à jour vers la nouvelle spécification, ils ne réinterpréteront pas les anciens commentaires, mais commenceront à prendre en compte les nouvelles commandes lors des récupérations ultérieures de leurs flux d’abonnement. Il est donc important que les serveurs de noms assurent la persistance des entrées de commande, d’une manière ou d’une autre, ou activent la prise en charge d’ETag afin que les routers puissent récupérer toutes les commandes passées.

## État de l'implémentation

**Déploiement initial :** Version 0.9.26 (7 juin 2016)

**Statut actuel:** Stable et inchangé jusqu'à I2P 2.10.0 (Router API 0.9.65, septembre 2025)

**Statut de la proposition:** FERMÉE (déployée avec succès sur l'ensemble du réseau)

**Emplacement de l'implémentation:** `apps/addressbook/java/src/net/i2p/addressbook/` dans le router Java d'I2P

**Classes clés:** - `SubscriptionList.java`: Gère le traitement des abonnements - `Subscription.java`: Gère les flux d’abonnement individuels - `AddressBook.java`: Fonctionnalité de base du carnet d’adresses - `Daemon.java`: Service d’arrière-plan du carnet d’adresses

**URL d'abonnement par défaut :** `http://i2p-projekt.i2p/hosts.txt`

## Détails des transports

Les abonnements utilisent HTTP avec prise en charge des requêtes GET conditionnelles:

- **En-tête ETag:** Permet une détection efficace des modifications
- **En-tête Last-Modified:** Suit les dates de mise à jour des abonnements
- **304 Not Modified:** Les serveurs devraient renvoyer ce code lorsque le contenu n'a pas changé
- **Content-Length:** Fortement recommandé pour toutes les réponses

Le router I2P utilise le comportement standard d'un client HTTP avec une prise en charge appropriée de la mise en cache.

## Contexte de version

**Note sur le versionnage d'I2P :** À partir de la version 1.5.0 (août 2021), I2P est passé d'un schéma de versionnage 0.9.x à un versionnage sémantique (1.x, 2.x, etc.). Cependant, la version interne de l'API du Router continue d'utiliser une numérotation en 0.9.x pour assurer la rétrocompatibilité. En octobre 2025, la version actuelle est I2P 2.10.0 avec une version de l'API du Router 0.9.65.

Ce document de spécification a été rédigé à l’origine pour la version 0.9.49 (février 2021) et reste parfaitement exact pour la version actuelle 0.9.65 (I2P 2.10.0), car le système de flux d’abonnement n’a connu aucun changement depuis sa mise en œuvre initiale dans la version 0.9.26.

## Références

- [Proposition 112 (version originale)](/proposals/112-addressbook-subscription-feed-commands/)
- [Spécification officielle](/docs/specs/subscription/)
- [Documentation sur le nommage I2P](/docs/overview/naming/)
- [Spécification des structures communes](/docs/specs/common-structures/)
- [Dépôt du code source I2P](https://github.com/i2p/i2p.i2p)
- [Dépôt I2P sur Gitea](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Développements connexes

Bien que le système de flux d’abonnement lui-même n’ait pas changé, les développements connexes suivants dans l’infrastructure de nommage d’I2P peuvent vous intéresser :

- **Noms Base32 étendus** (0.9.40+) : Prise en charge des adresses base32 de 56 caractères et plus pour les leaseSets chiffrés. N'affecte pas le format du flux d'abonnement.
- **Enregistrement du TLD .i2p.alt** (RFC 9476, fin 2023) : Enregistrement officiel par la GANA de .i2p.alt en tant que TLD alternatif. De futures mises à jour du router pourraient supprimer le suffixe .alt, mais aucune modification des commandes d'abonnement n'est requise.
- **Cryptographie post-quantique** (2.10.0+) : Disponible mais non activée par défaut. Des évolutions futures sont envisagées pour les algorithmes de signature dans les flux d'abonnement.
