---
title: "Type de signature GOST"
number: "134"
author: "original"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2239"
---

## Aperçu

La signature par courbe elliptique GOST R 34.10 est utilisée par les fonctionnaires et les entreprises en Russie. La prise en charge de celle-ci pourrait simplifier l'intégration des applications existantes (généralement basées sur CryptoPro). La fonction de hachage est GOST R 34.11 de 32 ou 64 octets. Fonctionne essentiellement de la même manière que l’EcDSA, la taille de la signature et de la clé publique est de 64 ou 128 octets.

## Motivation

La cryptographie par courbe elliptique n'a jamais été totalement fiable et produit beaucoup de spéculations sur de possibles portes dérobées. Par conséquent, il n'y a pas de type de signature ultime en qui tout le monde a confiance. Ajouter un type de signature supplémentaire donnera aux gens plus de choix concernant ce en quoi ils ont plus confiance.

## Conception

GOST R 34.10 utilise une courbe elliptique standard avec ses propres ensembles de paramètres. Les mathématiques des groupes existants peuvent être réutilisées. Cependant, la signature et la vérification sont différentes et doivent être mises en œuvre. Voir RFC : https://www.rfc-editor.org/rfc/rfc7091.txt GOST R 34.10 est censé fonctionner de concert avec le hachage GOST R 34.11. Nous utiliserons GOST R 34.10-2012 (alias steebog) soit 256 ou 512 bits. Voir RFC : https://tools.ietf.org/html/rfc6986

GOST R 34.10 ne spécifie pas de paramètres, cependant, il existe certains bons ensembles de paramètres utilisés par tout le monde. GOST R 34.10-2012 avec des clés publiques de 64 octets hérite des ensembles de paramètres de CryptoPro de GOST R 34.10-2001. Voir RFC : https://tools.ietf.org/html/rfc4357

Cependant, des ensembles de paramètres plus récents pour des clés de 128 octets sont créés par un comité technique spécial tc26 (tc26.ru). Voir RFC : https://www.rfc-editor.org/rfc/rfc7836.txt

L'implémentation basée sur Openssl dans i2pd montre qu'elle est plus rapide que P256 et plus lente que 25519.

## Spécification

Seuls GOST R 34.10-2012 et GOST R 34.11-2012 sont pris en charge. Deux nouveaux types de signature : 9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A correspond à un type de clé publique et de signature de 64 octets, une taille de hachage de 32 octets et un ensemble de paramètres CryptoProA (alias CryptoProXchA) 10 - GOSTR3410_GOSTR3411_512_TC26_A correspond à un type de clé publique et de signature de 128 octets, une taille de hachage de 64 octets et un ensemble de paramètres A de TC26.

## Migration

Ces types de signatures sont censés être utilisés uniquement en tant que type de signature optionnel. Aucune migration n'est requise. i2pd le prend déjà en charge.
