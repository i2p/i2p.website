---
title: "Vérification de l'identifiant du réseau de transport"
number: "147"
author: "zzz"
created: "2019-02-28"
lastupdated: "2019-08-13"
status: "Fermé"
thread: "http://zzz.i2p/topics/2687"
target: "0.9.42"
implementedin: "0.9.42"
toc: true
---

## Vue d'ensemble

NTCP2 (proposition 111) n'élimine pas les connexions provenant de différents identifiants de réseau lors de la phase de demande de session.
La connexion doit actuellement être rejetée lors de la phase de confirmation de session, lorsque Bob vérifie le RI d'Alice.

De manière similaire, SSU n'élimine pas les connexions provenant de différents identifiants de réseau lors de la phase de demande de session.
La connexion doit actuellement être rejetée après la phase de confirmation de session, lorsque Bob vérifie le RI d'Alice.

Cette proposition modifie la phase de demande de session des deux transports pour inclure l'identifiant de réseau, d'une manière compatible avec les versions antérieures.


## Motivation

Les connexions provenant du mauvais réseau doivent être rejetées, et le pair doit être mis sur liste noire, dès que possible.


## Objectifs

- Empêcher la contamination croisée des réseaux de test et des réseaux forkés

- Ajouter l'identifiant de réseau à la poignée de main NTCP2 et SSU

- Pour NTCP2,
  le récepteur (connexion entrante) devrait pouvoir identifier que l'identifiant de réseau est différent,
  afin de pouvoir mettre sur liste noire l'IP du pair.

- Pour SSU,
  le récepteur (connexion entrante) ne peut pas mettre sur liste noire à la phase de demande de session, car
  l'IP entrante pourrait être usurpée. Il est suffisant de changer la cryptographie de la poignée de main.

- Empêcher le réensemencement depuis le mauvais réseau

- Doit être compatible avec les versions antérieures


## Non-objectifs

- NTCP 1 n'est plus utilisé, donc il ne sera pas modifié.


## Conception

Pour NTCP2,
faire un XOR avec une valeur ferait simplement échouer le chiffrement, et le
récepteur n'aurait pas suffisamment d'informations pour mettre sur liste noire l'origine,
donc cette approche n'est pas préférée.

Pour SSU,
nous effectuerons un XOR avec l'identifiant de réseau quelque part dans la demande de session.
Puisque cela doit être compatible avec les versions antérieures, nous effectuerons un XOR avec (id - 2)
afin que ce soit une opération sans effet pour la valeur actuelle de l'identifiant de réseau de 2.


## Spécification

### Documentation

Ajouter la spécification suivante pour les valeurs valides d'identifiant de réseau :


| Utilisation | Numéro NetID |
|-------|--------------|
| Réservé | 0 |
| Réservé | 1 |
| Réseau actuel (par défaut) | 2 |
| Réseaux futurs réservés | 3 - 15 |
| Forks et réseaux de test | 16 - 254 |
| Réservé | 255 |


La configuration Java I2P pour changer la valeur par défaut est "router.networkID=nnn".
Documenter ceci de manière plus approfondie et encourager les forks et les réseaux de test à ajouter ce paramètre à leur configuration.
Encourager d'autres implémentations à appliquer et documenter cette option.


### NTCP2

Utiliser le premier octet réservé des options (octet 0) dans le message de demande de session pour contenir l'identifiant de réseau, actuellement 2.
Il contient l'identifiant de réseau.
Si non nul, le récepteur doit le vérifier par rapport à l'octet le moins significatif de l'identifiant de réseau local.
S'ils ne correspondent pas, le récepteur doit immédiatement se déconnecter et mettre sur liste noire l'IP de l'origine.


### SSU

Pour SSU, ajoutez un XOR de ((netid - 2) << 8) dans le calcul HMAC-MD5.

Existante :

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion), macKey)

  '+' signifie append et '^' signifie exclusive-or.
  payloadLength est un entier non signé de 2 octets
  protocolVersion est un octet 0x00
```

Nouvelle :

```text
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)

  '+' signifie append, '^' signifie exclusive-or, '<<' signifie décalage à gauche.
  payloadLength est un entier non signé sur deux octets, big endian
  protocolVersion est deux octets 0x0000, big endian
  netid est un entier non signé sur deux octets, big endian, les valeurs légales sont 2-254
```


### Réensemencement

Ajouter un paramètre ?netid=nnn lors de la récupération du fichier su3 de réensemencement.
Mettre à jour le logiciel de réensemencement pour vérifier l'identifiant de réseau. S'il est présent et différent de "2",
la récupération doit être rejetée avec un code d'erreur, peut-être 403.
Ajouter une option de configuration au logiciel de réensemencement pour qu'un identifiant de réseau alternatif puisse être configuré
pour des réseaux de test ou forkés.


## Notes

Nous ne pouvons pas forcer les réseaux de test et les forks à changer l'identifiant de réseau.
Le mieux que nous puissions faire est de la documentation et de la communication.
Si nous découvrons une contamination croisée avec d'autres réseaux, nous devrions tenter de
contacter les développeurs ou opérateurs pour expliquer l'importance de changer l'identifiant de réseau.


## Problèmes


## Migration

Ceci est compatible avec les versions antérieures pour la valeur actuelle de l'identifiant de réseau de 2.
Si des personnes exécutent des réseaux (de test ou autres) avec une valeur d'identifiant de réseau différente,
ce changement est incompatible avec les versions antérieures.
Cependant, nous ne sommes pas conscients de personnes faisant ceci.
Si c'est uniquement un réseau de test, cela n'est pas un problème, il suffit de mettre à jour tous les routeurs en une fois.
