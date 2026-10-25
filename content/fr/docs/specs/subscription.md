---
title: "Commandes de flux d'abonnement du carnet d'adresses"
description: "Spécification pour étendre le flux d'abonnement d'adresses avec des commandes permettant aux serveurs de noms de diffuser les mises à jour d'entrées provenant des détenteurs de noms d'hôte."
slug: "subscription"
aliases:
  - "/fr/docs/specs/subscription-spec"
  - "/fr/docs/specs/subscription-spec/"
category: "Formats"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Aperçu

Cette spécification étend le flux d'abonnement aux adresses avec des commandes, pour permettre aux serveurs de noms de diffuser les mises à jour d'entrées des détenteurs de noms d'hôte. Implémentée dans la version 0.9.26, initialement proposée dans la proposition 112.

## Motivation

Auparavant, les serveurs d'abonnement hosts.txt envoyaient simplement des données au format hosts.txt, qui est le suivant :

```
example.i2p=b64destination
```
Il y a plusieurs problèmes avec ceci :

- Les détenteurs de noms d'hôte ne peuvent pas mettre à jour la Destination associée à leurs noms d'hôte (par exemple pour mettre à niveau la clé de signature vers un type plus robuste).
- Les détenteurs de noms d'hôte ne peuvent pas abandonner leurs noms d'hôte arbitrairement ; ils doivent transmettre directement les clés privées de la Destination correspondante au nouveau détenteur.
- Il n'existe aucun moyen d'authentifier qu'un sous-domaine est contrôlé par le nom d'hôte de base correspondant ; ceci n'est actuellement appliqué individuellement que par certains serveurs de noms.

## Conception

Cette spécification ajoute un certain nombre de lignes de commande au format hosts.txt. Avec ces commandes, les serveurs de noms peuvent étendre leurs services pour fournir un certain nombre de fonctionnalités supplémentaires. Les clients qui implémentent cette spécification pourront écouter ces fonctionnalités via le processus d'abonnement habituel.

Toutes les lignes de commande doivent être signées par la Destination correspondante. Ceci garantit que les modifications ne sont effectuées qu'à la demande du détenteur du nom d'hôte.

## Implications de sécurité

Cette spécification n'affecte pas l'anonymat.

Il y a une augmentation du risque associé à la perte de contrôle d'une clé de Destination, car quelqu'un qui l'obtient peut utiliser ces commandes pour apporter des modifications à tous les noms d'hôte associés. Mais ce n'est pas plus problématique que le statu quo actuel, où quelqu'un qui obtient une Destination peut usurper l'identité d'un nom d'hôte et (partiellement) prendre le contrôle de son trafic. Le risque accru est également compensé en donnant aux détenteurs de noms d'hôte la capacité de changer la Destination associée à un nom d'hôte, dans le cas où ils pensent que la Destination a été compromise ; ceci est impossible avec le système actuel.

## Spécification

### Nouveaux types de ligne

Il y a deux nouveaux types de lignes :

1. Commandes d'ajout et de modification :

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Commandes de suppression :

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Commande

Un flux n'est pas nécessairement dans l'ordre ou complet. Par exemple, une commande de modification peut être sur une ligne avant une commande d'ajout, ou sans commande d'ajout.

Les clés peuvent être dans n'importe quel ordre. Les clés dupliquées ne sont pas autorisées. Toutes les clés et valeurs sont sensibles à la casse.

### Clés communes

Requis dans toutes les commandes :

**sig** : Signature B64, utilisant la clé de signature de la destination

Références à un second nom d'hôte et/ou destination :

**oldname** : Un second nom d'hôte (nouveau ou modifié)

**olddest** : Une seconde destination b64 (nouvelle ou modifiée)

**oldsig** : Une seconde signature b64, utilisant la clé de signature d'olddest

Autres clés communes :

**action** : Une commande

**name** : Le nom d'hôte, présent uniquement s'il n'est pas précédé par `example.i2p=b64dest`

**dest** : La destination b64, présente uniquement si elle n'est pas précédée de `example.i2p=b64dest`

**date** : En secondes depuis l'époque

**expires** : En secondes depuis l'époque

### Commandes

Toutes les commandes sauf la commande "Add" doivent contenir une paire clé/valeur `action=command`.

Pour la compatibilité avec les anciens clients, la plupart des commandes sont précédées par `example.i2p=b64dest`, comme indiqué ci-dessous. Pour les modifications, il s'agit toujours des nouvelles valeurs. Toutes les anciennes valeurs sont incluses dans la section clé/valeur.

Les clés listées sont obligatoires. Toutes les commandes peuvent contenir des éléments clé/valeur supplémentaires non définis ici.

#### Ajouter un nom d'hôte

**Précédé par example.i2p=b64dest** : OUI, ceci est le nouveau nom d'hôte et destination.

**action** : NON inclus, c'est implicite.

**sig** : signature

Exemple :

```
example.i2p=b64dest#!sig=b64sig
```
#### Changer le nom d'hôte

**Précédé par example.i2p=b64dest** : OUI, c'est le nouveau nom d'hôte et l'ancienne destination.

**action** : changename

**oldname** : l'ancien nom d'hôte, à remplacer

**sig** : signature

Exemple :

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Changer la destination

**Précédé par example.i2p=b64dest** : OUI, c'est l'ancien nom d'hôte et la nouvelle destination.

**action** : changedest

**olddest** : l'ancienne dest, à remplacer

**oldsig** : signature utilisant olddest

**sig** : signature

Exemple :

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Ajouter un Alias de Nom d'Hôte

**Précédé de example.i2p=b64dest** : OUI, c'est le nouveau nom d'hôte (alias) et l'ancienne destination.

**action** : addname

**oldname** : l'ancien nom d'hôte

**sig** : signature

Exemple :

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Ajouter un Alias de Destination

(Utilisé pour la mise à niveau cryptographique)

**Précédé par example.i2p=b64dest** : OUI, c'est l'ancien nom d'hôte et la nouvelle destination (alternative).

**action** : adddest

**olddest** : l'ancienne dest

**oldsig** : signature utilisant olddest

**sig** : signature utilisant dest

Exemple :

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Ajouter un sous-domaine

**Précédé par subdomain.example.i2p=b64dest** : OUI, il s'agit du nouveau nom de sous-domaine d'hôte et de la destination.

**action** : addsubdomain

**oldname** : le nom d'hôte de niveau supérieur (exemple.i2p)

**olddest** : la destination de niveau supérieur (par exemple.i2p)

**oldsig** : signature utilisant olddest

**sig** : signature utilisant dest

Exemple :

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Mettre à jour les métadonnées

**Précédé par example.i2p=b64dest** : OUI, c'est l'ancien nom d'hôte et destination.

**action** : update

**sig** : signature

(ajouter toutes les clés mises à jour ici)

Exemple :

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Supprimer le nom d'hôte

**Précédé par example.i2p=b64dest** : NON, ceux-ci sont spécifiés dans les options

**action** : remove

**name** : le nom d'hôte

**dest** : la destination

**sig** : signature

Exemple :

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Supprimer tout avec cette destination

**Précédé par example.i2p=b64dest** : NON, ceux-ci sont spécifiés dans les options

**action** : removeall

**name** : l'ancien nom d'hôte, consultatif seulement

**dest** : l'ancienne dest, toutes celles avec cette dest sont supprimées

**sig** : signature

Exemple :

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Signatures

Toutes les commandes doivent contenir une paire clé/valeur de signature `sig=b64signature` où la signature concerne les autres données, en utilisant la clé de signature de destination.

Pour les commandes incluant une ancienne et une nouvelle destination, il doit également y avoir un `oldsig=b64signature`, et soit oldname, olddest, ou les deux.

Dans une commande Add ou Change, la clé publique pour la vérification se trouve dans la Destination à ajouter ou à modifier.

Dans certaines commandes d'ajout ou de modification, il peut y avoir une destination supplémentaire référencée, par exemple lors de l'ajout d'un alias, ou lors du changement d'une destination ou d'un nom d'hôte. Dans ce cas, il doit y avoir une seconde signature incluse et les deux doivent être vérifiées. La seconde signature est la signature "interne" et est signée et vérifiée en premier (en excluant la signature "externe"). Le client doit prendre toute action supplémentaire nécessaire pour vérifier et accepter les modifications.

oldsig est toujours la signature "interne". Signer et vérifier sans les clés 'oldsig' ou 'sig' présentes. sig est toujours la signature "externe". Signer et vérifier avec la clé 'oldsig' présente mais pas la clé 'sig'.

#### Entrée pour les signatures

Pour générer un flux d'octets afin de créer ou vérifier la signature, sérialisez comme suit :

- Supprimer la clé "sig"
- Si la vérification se fait avec oldsig, supprimer également la clé "oldsig"
- Pour les commandes Add ou Change uniquement, afficher `example.i2p=b64dest`
- S'il reste des clés, afficher `#!`
- Trier les options par clé UTF-8, échouer s'il y a des clés dupliquées
- Pour chaque paire clé/valeur, afficher `key=value`, suivi de (si ce n'est pas la dernière paire clé/valeur) un `#`

Notes :

- Ne pas produire de nouvelle ligne
- L'encodage de sortie est UTF-8
- Tout encodage de destination et de signature est en Base 64 utilisant l'alphabet I2P
- Les clés et valeurs sont sensibles à la casse
- Les noms d'hôtes doivent être en minuscules

## Compatibilité

Toutes les nouvelles lignes du format hosts.txt sont implémentées en utilisant des caractères de commentaire en début de ligne, de sorte que toutes les anciennes versions d'I2P interpréteront les nouvelles commandes comme des commentaires.

Lorsque les routeurs I2P se mettent à jour vers la nouvelle spécification, ils ne réinterprèteront pas les anciens commentaires, mais commenceront à écouter les nouvelles commandes lors des récupérations ultérieures de leurs flux d'abonnement. Il est donc important que les serveurs de noms persistent les entrées de commande d'une manière ou d'une autre, ou activent le support etag afin que les routeurs puissent récupérer toutes les commandes passées.
