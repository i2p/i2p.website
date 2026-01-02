---
title: "Support de Floodfill pour les Types de Signature Expérimentaux"
number: "136"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2279"
toc: true
---

## Vue d'ensemble

Pour les types de signature dans la plage expérimentale (65280-65534),
les floodfills devraient accepter les stockages netdb sans vérifier la signature.

Cela prendra en charge le test de nouveaux types de signature.


## Motivation

La proposition GOST 134 a révélé deux problèmes avec la plage de types de signature expérimentale précédemment inutilisée.

Premièrement, puisque les types de signature dans la plage expérimentale ne peuvent pas être réservés, ils peuvent être utilisés pour
plusieurs types de signature à la fois.

Deuxièmement, à moins qu'une information de routeur ou un ensemble de location avec un type de signature expérimental puisse être stocké à un floodfill,
le nouveau type de signature est difficile à tester complètement ou à utiliser sur une base d'essai.


## Conception

Les floodfills devraient accepter, et propager, les stockages LS avec des types de signature dans la plage expérimentale,
sans vérifier la signature. Le support pour les stockages RI est à définir, et peut avoir plus d'implications sécuritaires.


## Spécification


Pour les types de signature dans la plage expérimentale, un floodfill devrait accepter et propager les stockages netdb
sans vérifier la signature.

Pour empêcher l'usurpation de routeurs et de destinations non expérimentaux, un floodfill
ne devrait jamais accepter un stockage d'un type de signature expérimental ayant une collision de hachage
avec une entrée netdb existante d'un type de signature différent.
Cela empêche de détourner une entrée netdb précédente.

En outre, un floodfill devrait écraser une entrée netdb expérimentale
avec un stockage d'un type de signature non expérimental ayant une collision de hachage,
pour empêcher le détournement d'une hachage précédemment absent.

Les floodfills devraient supposer que la longueur de la clé publique de signature est de 128, ou la dériver de
la longueur du certificat de clé, si plus longue. Certaines implémentations peuvent
ne pas supporter les longueurs plus longues à moins que le type de signature ne soit réservé de manière informelle.


## Migration

Une fois cette fonctionnalité prise en charge, dans une version de routeur connue,
les entrées netdb de types de signature expérimentaux peuvent être stockées dans les floodfills de cette version ou plus.

Si certaines implémentations de routeurs ne prennent pas en charge cette fonctionnalité, le stockage netdb
échouera, mais c'est comme c'est actuellement.


## Problèmes

Il peut y avoir des implications sécuritaires supplémentaires, à rechercher (voir proposition 137)

Certaines implémentations peuvent ne pas supporter des longueurs de clé supérieures à 128,
comme décrit ci-dessus. De plus, il peut être nécessaire d'appliquer un maximum de 128
(en d'autres termes, il n'y a pas de données de clé excédentaires dans le certificat de clé),
pour réduire la capacité des attaquants à générer des collisions de hachage.

Des problèmes similaires devront être abordés avec des types de chiffrement non nuls,
ce qui n'a pas encore été proposé formellement.


## Notes

Les stockages NetDB de types de signature inconnus qui ne sont pas dans la plage expérimentale continueront
d'être rejetés par les floodfills, car la signature ne peut être vérifiée.


