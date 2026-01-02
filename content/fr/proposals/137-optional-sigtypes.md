---
title: "Support Floodfill pour Types de Signature Optionnels"
number: "137"
author: "zzz"
created: "2017-03-31"
lastupdated: "2017-11-12"
status: "Open"
thread: "http://zzz.i2p/topics/2280"
toc: true
---

## Vue d'ensemble

Ajouter un moyen pour que les floodfills annoncent un support pour des types de signature optionnels. Cela offrira une manière de prendre en charge de nouveaux types de signature à long terme, même si toutes les implémentations ne les prennent pas en charge.

## Motivation

La proposition GOST 134 a révélé plusieurs problèmes avec la gamme de types de signature expérimentale précédemment inutilisée.

Premièrement, puisque les types de signature dans la gamme expérimentale ne peuvent pas être réservés, ils peuvent être utilisés pour plusieurs types de signature à la fois.

Deuxièmement, à moins qu'un router info ou un lease set avec un type de signature expérimental puisse être stocké dans un floodfill, le nouveau type de signature est difficile à tester complètement ou à utiliser à titre d'essai.

Troisièmement, si la proposition 136 est mise en œuvre, ce n'est pas sécurisé, car n'importe qui peut écraser une entrée.

Quatrièmement, mettre en œuvre un nouveau type de signature peut représenter un effort de développement conséquent. Il peut être difficile de convaincre les développeurs de toutes les implémentations de routeurs d'ajouter la prise en charge d'un nouveau type de signature à temps pour une sortie particulière. Le temps et les motivations des développeurs peuvent varier.

Cinquièmement, si GOST utilise un type de signature dans la gamme standard, il n'y a toujours aucun moyen de savoir si un floodfill particulier prend en charge GOST.

## Conception

Tous les floodfills doivent prendre en charge les types de signature DSA (0), ECDSA (1-3) et EdDSA (7).

Pour tout autre type de signature dans la gamme standard (non expérimentale), un floodfill peut annoncer la prise en charge dans ses propriétés router info.

## Spécification


Un routeur qui prend en charge un type de signature optionnel doit ajouter la propriété "sigTypes" à ses informations publiées de routeur, avec des numéros de type de signature séparés par des virgules. Les types de signature seront dans un ordre numérique trié. Les types de signature obligatoires (0-4,7) ne doivent pas être inclus.

Par exemple: sigTypes=9,10

Les routeurs qui prennent en charge les types de signature optionnels doivent uniquement stocker, rechercher ou propager à des floodfills qui annoncent la prise en charge de ce type de signature.

## Migration

Non applicable. Seuls les routeurs qui prennent en charge un type de signature optionnel doivent implémenter.

## Problèmes

S'il n'y a pas beaucoup de floodfills prenant en charge le type de signature, ils peuvent être difficiles à trouver.

Il peut ne pas être nécessaire d'exiger ECDSA 384 et 521 (types de signature 2 et 3) pour tous les floodfills. Ces types ne sont pas largement utilisés.

Des problèmes similaires devront être abordés avec des types de cryptage non nuls, qui n'ont pas encore été formellement proposés.

## Remarques

Les NetDB stockant des types de signature inconnus qui ne sont pas dans la gamme expérimentale continueront d'être rejetés par les floodfills, car la signature ne peut pas être vérifiée.


