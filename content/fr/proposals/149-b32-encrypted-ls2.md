---
title: "B32 pour LS2 Cryptée"
number: "149"
author: "zzz"
created: "2019-03-13"
lastupdated: "2020-08-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2682"
target: "0.9.40"
implementedin: "0.9.40"
---

## Remarque
Déploiement et test réseau en cours.
Sujet à de légères révisions.
Voir [SPEC](/docs/specs/b32-for-encrypted-leasesets/) pour la spécification officielle.


## Aperçu

Les adresses Standard Base 32 ("b32") contiennent le hash de la destination.
Cela ne fonctionne pas pour ls2 chiffrées (proposition 123).

Vous ne pouvez pas utiliser une adresse base 32 traditionnelle pour une LS2 chiffrée (proposition 123),
car elle contient uniquement le hash de la destination. Elle ne fournit pas la clé publique non masquée.
Les clients doivent connaître la clé publique de la destination, le type de signature,
le type de signature masqué, et une clé secrète ou privée optionnelle
pour récupérer et déchiffrer le leaseset.
Ainsi, une adresse base 32 seule est insuffisante.
Le client a besoin soit de la destination complète (qui contient la clé publique),
soit de la clé publique seule.
Si le client dispose de la destination complète dans un carnet d'adresses, et que le carnet d'adresses
supporte la recherche inversée par hash, alors la clé publique peut être récupérée.

Nous avons donc besoin d'un nouveau format qui place la clé publique au lieu du hash dans
une adresse base32. Ce format doit également contenir le type de signature de la
clé publique, et le type de signature du schéma de masquage.

Cette proposition documente un nouveau format b32 pour ces adresses.
Bien que nous ayons fait référence à ce nouveau format lors des discussions
comme une adresse "b33", le nouveau format conserve le suffixe habituel ".b32.i2p".

## Objectifs

- Inclure les types de signature non masqués et masqués pour supporter les futurs schémas de masquage
- Supporter les clés publiques de plus de 32 octets
- Assurer que les caractères b32 soient tous ou majoritairement aléatoires, particulièrement au début
  (ne pas vouloir que toutes les adresses commencent par les mêmes caractères)
- Analysable
- Indiquer qu'un secret de masquage et/ou une clé par client est requis
- Ajouter une somme de contrôle pour détecter les fautes de frappe
- Minimiser la longueur, maintenir la longueur des labels DNS inférieure à 63 caractères pour un usage normal
- Continuer à utiliser la base 32 pour l'insensibilité à la casse
- Conserver le suffixe habituel ".b32.i2p".

## Objectifs Non Visés

- Ne pas supporter les liens "privés" qui incluent un secret de masquage et/ou une clé par client ;
  cela serait non sécurisé.


## Conception

- Le nouveau format contiendra la clé publique non masquée, le type de signature non masqué,
  et le type de signature masqué.
- Contient éventuellement un secret et/ou une clé privée, pour les liens privés uniquement
- Utiliser le suffixe existant ".b32.i2p", mais avec une plus grande longueur.
- Ajouter une somme de contrôle.
- Les adresses pour les leasesets cryptés sont identifiées par 56 caractères ou plus encodés
  (35 octets ou plus décodés), par rapport à 52 caractères (32 octets) pour les adresses base 32 traditionnelles.


## Spécification

### Création et encodage

Construire un nom d'hôte de {56+ chars}.b32.i2p (35+ chars en binaire) comme suit :

```text
drapeau (1 octet)
    bit 0 : 0 pour les types de signature sur un octet, 1 pour les types de signature sur deux octets
    bit 1 : 0 pour aucun secret, 1 si un secret est requis
    bit 2 : 0 pour aucune authentification par client,
           1 si une clé privée client est requise
    bits 7-3 : Non utilisés, réglés sur 0

  type de signature clé publique (1 ou 2 octets comme indiqué dans les drapeaux)
    Si 1 octet, le byte supérieur est supposé zéro

  type de signature clé masquée (1 ou 2 octets comme indiqué dans les drapeaux)
    Si 1 octet, le byte supérieur est supposé zéro

  clé publique
    Nombre d'octets comme impliqué par le type de signature

```

Post-traitement et somme de contrôle :

```text
Construire les données binaires comme ci-dessus.
  Traiter la somme de contrôle comme little-endian.
  Calculer la somme de contrôle = CRC-32(données[3:fin])
  données[0] ^= (octet) somme de contrôle
  données[1] ^= (octet) (somme de contrôle >> 8)
  données[2] ^= (octet) (somme de contrôle >> 16)

  nom d'hôte = Base32.encode(données) || ".b32.i2p"
```

Tous les bits non utilisés à la fin du b32 doivent être 0.
Il n’y a pas de bits inutilisés pour une adresse standard de 56 caractères (35 octets).


### Décodage et Vérification

```text
enlever le ".b32.i2p" du nom d'hôte
  données = Base32.decode(nom d'hôte)
  Calculer la somme de contrôle = CRC-32(données[3:fin])
  Traiter la somme de contrôle comme little-endian.
  drapeaux = données[0] ^ (octet) somme de contrôle
  si types de signature sur 1 octet :
    type sig clé publique = données[1] ^ (octet) (somme de contrôle >> 8)
    type sig masquée = données[2] ^ (octet) (somme de contrôle >> 16)
  sinon (types de signature sur 2 octets) :
    type sig clé publique = données[1] ^ ((octet) (somme de contrôle >> 8)) || données[2] ^ ((octet) (somme de contrôle >> 16))
    type sig masquée = données[3] || données[4]
  analyser le reste basé sur les drapeaux pour obtenir la clé publique
```


### Secret et Bits de Clé Privée

Les bits de secret et de clé privée sont utilisés pour indiquer aux clients, proxys ou autres
code côté client que le secret et/ou la clé privée sera nécessaire pour décrypter le
leaseset. Les implémentations particulières peuvent inviter l'utilisateur à fournir les
données requises, ou rejeter les tentatives de connexion si les données requises manquent.


## Justification

- XORer les 3 premiers octets avec le hash fournit une capacité limitée de somme de contrôle,
  et s'assure que tous les caractères base32 au début sont aléatoires.
  Seules quelques combinaisons de drapeaux et de type sig sont valides, donc toute faute de frappe est susceptible de créer une combinaison invalide et sera rejetée.
- Dans le cas habituel (types sig sur 1 octet, pas de secret, pas d'authentification par client),
  le nom d'hôte sera {56 caractères}.b32.i2p, décodant à 35 octets, comme Tor.
- La somme de contrôle sur 2 octets de Tor a un taux de false négatif de 1/64K. Avec 3 octets, moins quelques octets ignorés,
  la nôtre approche de 1 sur un million, car la plupart des combinaisons drapeaux/type sig sont invalides.
- Adler-32 est un mauvais choix pour les petites entrées, et pour détecter les petits changements .
  Utiliser CRC-32 à la place. CRC-32 est rapide et largement disponible.

## Mise en cache

Bien qu'en dehors du champ de cette proposition, les routeurs et/ou les clients doivent se souvenir et mettre en cache
(probablement de manière persistante) la correspondance de la clé publique à la destination, et vice versa.



## Remarques

- Distinguer les anciennes des nouvelles saveurs par la longueur. Les anciennes adresses b32 sont toujours {52 caractères}.b32.i2p. Les nouvelles sont {56+ caractères}.b32.i2p
- Discussion sur Tor : https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html
- Ne vous attendez pas à ce que des types de signature sur 2 octets arrivent un jour, nous n'en sommes qu'à 13. Pas besoin d’implémenter maintenant.
- Le nouveau format peut être utilisé dans les liens de saut (et servi par des serveurs de saut) si désiré, tout comme b32.


## Problèmes

- Tout secret, clé privée ou clé publique de plus de 32 octets dépasserait
  la longueur maximale du label DNS de 63 caractères. Les navigateurs ne s'en soucient probablement pas.


## Migration

Aucun problème de compatibilité ascendante. Les adresses b32 plus longues échoueront à être converties
en haches de 32 octets dans les anciens logiciels.
