---
title: "Commandes de Flux d'Abonnement à un Carnet d'Adresses"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Closed"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Remarque
Déploiement du réseau terminé.
Voir [SPEC](/docs/specs/subscription/) pour la spécification officielle.


## Vue d'ensemble

Cette proposition concerne l'extension du flux d'abonnement à l'adresse avec des commandes, pour permettre aux serveurs de noms de diffuser des mises à jour d'entrées des détenteurs de noms d'hôte.
Implémenté dans la version 0.9.26.


## Motivation

Actuellement, les serveurs d'abonnement hosts.txt envoient simplement des données au format hosts.txt, qui est le suivant :

    example.i2p=b64destination

Il y a plusieurs problèmes avec cela :

- Les détenteurs de noms d'hôte ne peuvent pas mettre à jour la Destination associée à leurs noms d'hôte
  (pour par exemple mettre à niveau la clé de signature vers un type plus fort).
- Les détenteurs de noms d'hôte ne peuvent pas céder arbitrairement leurs noms d'hôte ; ils doivent donner directement les clés privées de Destination au nouveau détenteur.
- Il n'y a aucun moyen d'authentifier qu'un sous-domaine est contrôlé par le
  nom d'hôte de base correspondant ; cela est actuellement appliqué individuellement par
  certains serveurs de noms.


## Conception

Cette proposition ajoute un certain nombre de lignes de commande au format hosts.txt. Avec ces commandes, les serveurs de noms peuvent étendre leurs services pour fournir un certain nombre de fonctionnalités supplémentaires. Les clients qui implémentent cette proposition pourront écouter ces fonctionnalités via le processus d'abonnement régulier.

Toutes les lignes de commande doivent être signées par la Destination correspondante. Cela garantit que les modifications sont effectuées uniquement à la demande du détenteur du nom d'hôte.


## Implications en matière de sécurité

Cette proposition n'a pas d'implications sur l'anonymat.

Il y a une augmentation du risque associé à la perte de contrôle d'une clé de Destination, car quelqu'un qui l'obtient peut utiliser ces commandes pour apporter des modifications à tous les noms d'hôte associés. Mais cela n'est pas plus problématique que la situation actuelle, où quelqu'un qui obtient une Destination peut usurper un nom d'hôte et
(présentement) s'emparer de son trafic. Le risque accru est également équilibré par
le fait de donner aux détenteurs de noms d'hôte la possibilité de changer la Destination associée à un nom d'hôte, dans le cas où ils pensent que la Destination a été compromise;
ce qui est impossible avec le système actuel.


## Spécification

### Nouveaux types de lignes

Cette proposition ajoute deux nouveaux types de lignes :

1. Commandes d'ajout et de modification :

     example.i2p=b64destination#!key1=val1#key2=val2 ...

2. Commandes de suppression :

     #!key1=val1#key2=val2 ...

#### Ordre
Un flux n'est pas nécessairement ordonné ou complet. Par exemple, une commande de modification
peut être sur une ligne avant une commande d'ajout, ou sans commande d'ajout.

Les clés peuvent être dans n'importe quel ordre. Les doubles clés ne sont pas autorisées. Toutes les clés et valeurs sont sensibles à la casse.


### Clés communes

Requises dans toutes les commandes :

sig
  Signature B64, utilisant la clé de signature de la destination

Références à un deuxième nom d'hôte et/ou destination :

oldname
  Un deuxième nom d'hôte (nouveau ou modifié)
olddest
  Une deuxième destination b64 (nouvelle ou modifiée)
oldsig
  Une deuxième signature b64, utilisant la clé de signature de nolddest

Autres clés communes :

action
  Une commande
name
  Le nom d'hôte, présent uniquement s'il n'est pas précédé par example.i2p=b64dest
dest
  La destination b64, présente uniquement s'il n'est pas précédé par example.i2p=b64dest
date
  En secondes depuis l'époque Unix
expires
  En secondes depuis l'époque Unix


### Commandes

Toutes les commandes sauf la commande "Add" doivent contenir une clé/valeur "action=command".

Pour la compatibilité avec les anciens clients, la plupart des commandes sont précédées de example.i2p=b64dest,
comme noté ci-dessous. Pour les modifications, ce sont toujours les nouvelles valeurs. Toutes les anciennes valeurs
sont incluses dans la section clé/valeur.

Les clés listées sont obligatoires. Toutes les commandes peuvent contenir des éléments supplémentaires de clé/valeur non définis ici.

#### Ajouter un nom d'hôte
Précédée par example.i2p=b64dest
  OUI, ceci est le nouveau nom d'hôte et la nouvelle destination.
action
  NON incluse, elle est implicite.
sig
  signature

Exemple :

  example.i2p=b64dest#!sig=b64sig

#### Modifier le nom d'hôte
Précédée par example.i2p=b64dest
  OUI, ceci est le nouveau nom d'hôte et l'ancienne destination.
action
  changename
oldname
  l'ancien nom d'hôte, à remplacer
sig
  signature

Exemple :

  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig

#### Modifier la destination
Précédée par example.i2p=b64dest
  OUI, ceci est l'ancien nom d'hôte et la nouvelle destination.
action
  changedest
olddest
  l'ancienne destination, à remplacer
oldsig
  signature utilisant olddest
sig
  signature

Exemple :

  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig

#### Ajouter un alias de nom d'hôte
Précédée par example.i2p=b64dest
  OUI, ceci est le nouveau (alias) nom d'hôte et l'ancienne destination.
action
  addname
oldname
  l'ancien nom d'hôte
sig
  signature

Exemple :

  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig

#### Ajouter un alias de destination
(Utilisé pour la mise à niveau cryptographique)

Précédée par example.i2p=b64dest
  OUI, ceci est l'ancien nom d'hôte et la nouvelle destination (alternative).
action
  adddest
olddest
  l'ancienne destination
oldsig
  signature utilisant olddest
sig
  signature utilisant dest

Exemple :

  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig

#### Ajouter un sous-domaine
Précédée par subdomain.example.i2p=b64dest
  OUI, ceci est le nouveau nom de sous-domaine d'hôte et la nouvelle destination.
action
  addsubdomain
oldname
  le nom d'hôte de niveau supérieur (example.i2p)
olddest
  la destination de niveau supérieur (pour example.i2p)
oldsig
  signature utilisant olddest
sig
  signature utilisant dest

Exemple :

  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig

#### Mettre à jour les métadonnées
Précédée par example.i2p=b64dest
  OUI, ceci est l'ancien nom et la destination d'hôte.
action
  update
sig
  signature

(ajouter ici toutes les clés mises à jour)

Exemple :

  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig

#### Supprimer le nom d'hôte
Précédée par example.i2p=b64dest
  NON, ceux-ci sont spécifiés dans les options
action
  remove
name
  le nom d'hôte
dest
  la destination
sig
  signature

Exemple :

  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig

#### Supprimer tout avec cette destination
Précédée par example.i2p=b64dest
  NON, ceux-ci sont spécifiés dans les options
action
  removeall
name
  l'ancien nom d'hôte, à titre consultatif uniquement
dest
  l'ancienne destination, tout avec cette destination est supprimé
sig
  signature

Exemple :

  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig


### Signatures

Toutes les commandes doivent contenir une clé/valeur de signature "sig=b64signature" où la signature pour les autres données, en utilisant la clé de signature de destination.

Pour les commandes incluant une ancienne et une nouvelle destination, il doit également y avoir un
oldsig=b64signature, et soit oldname, olddest, ou les deux.

Dans une commande d'ajout ou de modification, la clé publique pour vérification se trouve dans la
Destination à ajouter ou à modifier.

Dans certaines commandes d'ajout ou de modification, il peut y avoir une destination supplémentaire référencée, par exemple lors de l'ajout d'un alias, ou lors de la modification d'une destination ou d'un nom d'hôte. Dans ce cas, il doit y avoir une deuxième signature incluse et les deux doivent être
vérifiées. La deuxième signature est la signature "interne" et est signée et vérifiée en premier (en excluant la signature "externe"). Le client doit prendre toutes les mesures supplémentaires nécessaires pour vérifier et accepter les modifications.

oldsig est toujours la signature "interne". Signer et vérifier sans les clés 'oldsig' ou
'sig' présentes. sig est toujours la signature "externe". Signer et vérifier avec la
clé 'oldsig' présente mais pas la clé 'sig'.

#### Entrée pour les signatures
Pour générer un flux d'octets pour créer ou vérifier la signature, sérialiser comme suit :

- Retirer la clé "sig"
- Si la vérification avec oldsig, retirer également la clé "oldsig"
- Pour les commandes d'ajout ou de modification uniquement,
  output example.i2p=b64dest
- Si des clés restent, output "#!"
- Trier les options par clé UTF-8, échouer en cas de clés dupliquées
- Pour chaque clé/valeur, output clé=valeur, suivi (si ce n'est pas la dernière clé/valeur)
  d'un '#'

Notes

- Ne pas output une nouvelle ligne
- L'encodage de sortie est UTF-8
- Tout encodage de destination et de signature est en Base 64 utilisant l'alphabet I2P
- Les clés et les valeurs sont sensibles à la casse
- Les noms d'hôte doivent être en minuscules


## Compatibilité

Toutes les nouvelles lignes dans le format hosts.txt sont implémentées en utilisant des caractères de commentaire en tête, de sorte que toutes les anciennes versions I2P interpréteront les nouvelles commandes comme des commentaires.

Lorsque les routeurs I2P se mettront à jour selon la nouvelle spécification, ils ne réinterpréteront pas
les anciens commentaires, mais commenceront à écouter les nouvelles commandes dans les récupérations ultérieures de
leurs flux d'abonnement. Il est donc important que les serveurs de noms conservent
les entrées de commande d'une certaine manière, ou activent le support etag pour que les routeurs puissent
récupérer toutes les commandes passées.
