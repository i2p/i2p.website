---
title: "RedDSA-BLAKE2b-Ed25519"
number: "148"
author: "zzz"
created: "2019-03-12"
lastupdated: "2019-04-11"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2689"
---

## Aperçu

Cette proposition ajoute un nouveau type de signature utilisant BLAKE2b-512 avec des chaînes de personnalisation et des sels, pour remplacer SHA-512. Cela éliminera trois types d'attaques possibles.

## Motivation

Lors des discussions et de la conception de NTCP2 (proposition 111) et LS2 (proposition 123), nous avons brièvement considéré diverses attaques possibles et comment les prévenir. Trois de ces attaques sont les attaques d'extension de longueur, les attaques cross-protocole, et l'identification des messages dupliqués.

Pour NTCP2 et LS2, nous avons décidé que ces attaques n'étaient pas directement pertinentes pour les propositions en cours, et toute solution était en conflit avec l'objectif de minimiser les nouvelles primitives. De plus, nous avons déterminé que la vitesse des fonctions de hachage dans ces protocoles n'était pas un facteur important dans nos décisions. Par conséquent, nous avons principalement renvoyé la solution à une proposition distincte. Bien que nous ayons ajouté certaines fonctionnalités de personnalisation à la spécification LS2, nous n'avons pas exigé de nouvelles fonctions de hachage.

De nombreux projets, tels que ZCash [ZCASH]_, utilisent des fonctions de hachage et des algorithmes de signature basés sur des algorithmes plus récents qui ne sont pas vulnérables aux attaques suivantes.

### Attaques d'extension de longueur

SHA-256 et SHA-512 sont vulnérables aux attaques d'extension de longueur (LEA) [LEA]_. C'est le cas lorsque des données réelles sont signées, et non le hachage des données. Dans la plupart des protocoles I2P (streaming, datagrammes, netdb, et autres), les données réelles sont signées. Une exception est les fichiers SU3, où le hachage est signé. L'autre exception est les datagrammes signés pour DSA (type de signature 0) uniquement, où le hachage est signé. Pour les autres types de signature de datagramme signés, les données sont signées.

### Attaques cross-protocole

Les données signées dans les protocoles I2P peuvent être vulnérables aux attaques cross-protocole (CPA) en raison d'un manque de séparation de domaine. Cela permet à un attaquant d'utiliser des données reçues dans un contexte (tel qu'un datagramme signé) et de les présenter comme des données signées valides dans un autre contexte (tel que le streaming ou la base de données réseau). Bien qu'il soit peu probable que les données signées d'un contexte soient analysées comme des données valides dans un autre contexte, il est difficile ou impossible d'analyser toutes les situations pour en être sûr. De plus, dans certains contextes, il peut être possible pour un attaquant d'inciter une victime à signer des données spécialement conçues qui pourraient être des données valides dans un autre contexte. Encore une fois, il est difficile ou impossible d'analyser toutes les situations pour en être sûr.

### Identification des messages dupliqués

Les protocoles I2P peuvent être vulnérables à l'identification des messages dupliqués (DMI). Cela peut permettre à un attaquant d'identifier que deux messages signés ont le même contenu, même si ces messages et leurs signatures sont chiffrés. Bien que cela soit peu probable en raison des méthodes de chiffrement utilisées dans I2P, il est difficile ou impossible d'analyser toutes les situations pour en être sûr. En utilisant une fonction de hachage qui fournit une méthode pour ajouter un sel aléatoire, toutes les signatures seront différentes même lorsqu'on signe les mêmes données. Bien que Red25519 tel que défini dans la proposition 123 ajoute un sel aléatoire à la fonction de hachage, cela ne résout pas le problème pour les ensembles de location non chiffrés.

### Vitesse

Bien que cela ne soit pas une motivation principale pour cette proposition, SHA-512 est relativement lent et des fonctions de hachage plus rapides sont disponibles.

## Objectifs

- Prévenir les attaques ci-dessus
- Minimiser l'utilisation de nouvelles primitives cryptographiques
- Utiliser des primitives cryptographiques éprouvées et standardisées
- Utiliser des courbes standard
- Utiliser des primitives plus rapides si disponibles

## Conception

Modifier le type de signature existant RedDSA_SHA512_Ed25519 pour utiliser BLAKE2b-512 au lieu de SHA-512. Ajouter des chaînes de personnalisation uniques pour chaque cas d'utilisation. Le nouveau type de signature peut être utilisé pour les ensembles de location aussi bien aveuglés que non aveuglés.

## Justification

- BLAKE2b n'est pas vulnérable à LEA [BLAKE2]_.
- BLAKE2b offre un moyen standard d'ajouter des chaînes de personnalisation pour la séparation des domaines.
- BLAKE2b offre un moyen standard d'ajouter un sel aléatoire pour prévenir DMI.
- BLAKE2b est plus rapide que SHA-256 et SHA-512 (et MD5) sur le matériel moderne, selon [BLAKE2]_.
- Ed25519 est toujours notre type de signature le plus rapide, beaucoup plus rapide qu'ECDSA, du moins en Java.
- Ed25519 [ED25519-REFS]_ nécessite une fonction de hachage cryptographique de 512 bits. Il ne spécifie pas SHA-512. BLAKE2b est tout aussi approprié pour la fonction de hachage.
- BLAKE2b est largement disponible dans les bibliothèques pour de nombreux langages de programmation, tels que Noise.

## Spécification

Utiliser BLAKE2b-512 non clé comme dans [BLAKE2]_ avec sel et personnalisation. Toutes les utilisations des signatures BLAKE2b utiliseront une chaîne de personnalisation de 16 caractères.

Lorsqu'il est utilisé dans la signature RedDSA_BLAKE2b_Ed25519, un sel aléatoire est autorisé, cependant il n'est pas nécessaire, car l'algorithme de signature ajoute 80 octets de données aléatoires (voir proposition 123). Si désiré, lors du hachage des données pour calculer r, définir un nouveau sel aléatoire BLAKE2b de 16 octets pour chaque signature. Lors du calcul de S, réinitialiser le sel à la valeur par défaut de tous les zéros.

Lorsqu'il est utilisé dans la vérification RedDSA_BLAKE2b_Ed25519, ne pas utiliser un sel aléatoire, utiliser la valeur par défaut de tous les zéros.

Les fonctionnalités de sel et de personnalisation ne sont pas spécifiées dans [RFC-7693]_; utiliser ces fonctionnalités telles que spécifiées dans [BLAKE2]_.

### Type de signature

Pour RedDSA_BLAKE2b_Ed25519, remplacer la fonction de hachage SHA-512 dans RedDSA_SHA512_Ed25519 (type de signature 11, tel que défini dans la proposition 123) par BLAKE2b-512. Aucun autre changement.

Nous n'avons pas besoin d'un remplacement pour EdDSA_SHA512_Ed25519ph (type de signature 8) pour les fichiers su3, car la version préhachée d'EdDSA n'est pas vulnérable à LEA. EdDSA_SHA512_Ed25519 (type de signature 7) n'est pas pris en charge pour les fichiers su3.

=======================  ===========  ======  =====
        Type             Code Type    Depuis  Usage
=======================  ===========  ======  =====
RedDSA_BLAKE2b_Ed25519       12        À déterminer    Pour les identités des routeurs, les destinations et les ensembles de location chiffrés uniquement; jamais utilisé pour les identités de routeur
=======================  ===========  ======  =====

### Longueurs des données de structure commune

Ce qui suit s'applique au nouveau type de signature.

==================================  =============
            Type de données            Longueur  
==================================  =============
Hachage                                64      
Clé privée                             32      
Clé publique                           32      
Signature                              64      
==================================  =============

### Personnalisations

Pour fournir une séparation de domaine pour les différentes utilisations des signatures, nous utiliserons la fonctionnalité de personnalisation de BLAKE2b.

Toutes les utilisations des signatures BLAKE2b utiliseront une chaîne de personnalisation de 16 caractères. Toute nouvelle utilisation doit être ajoutée au tableau ici, avec une personnalisation unique.

Les utilisations de la poignée de main NTCP 1 et SSU ci-dessous sont pour les données signées définies dans la poignée de main elle-même. Les RouterInfos signés dans les messages DatabaseStore utiliseront la personnalisation d'entrée NetDb, tout comme s'ils étaient stockés dans le NetDB.

==================================  ==========================
         Utilisation                 Personnalisation de 16 octets
==================================  ==========================
I2CP SessionConfig                  "I2CP_SessionConf"
Entrées NetDB (RI, LS, LS2)         "network_database"
Poignée de main NTCP 1              "NTCP_1_handshake"
Datagrammes signés                  "sign_datagramI2P"
Streaming                           "streaming_i2psig"
Poignée de main SSU                 "SSUHandshakeSign"
Fichiers SU3                        n/a, non pris en charge
Tests unitaires                     "test1234test5678"
==================================  ==========================

## Notes

## Problèmes

- Alternative 1 : Proposition 146 ; fournit une résistance LEA
- Alternative 2 : Ed25519ctx dans RFC 8032 ; fournit une résistance LEA et une personnalisation. Standardisé, mais quelqu'un l'utilise-t-il ? Voir [RFC-8032]_ et [ED25519CTX]_.
- Le hachage "clé" est-il utile pour nous ?

## Migration

La même chose qu'avec le déploiement pour les types de signature précédents.

Nous prévoyons de changer les nouveaux routeurs du type 7 au type 12 par défaut. Nous prévoyons de migrer éventuellement les routeurs existants du type 7 au type 12, en utilisant le processus de "reclé" utilisé après l'introduction du type 7. Nous prévoyons de changer les nouvelles destinations du type 7 au type 12 par défaut. Nous prévoyons de changer les nouvelles destinations chiffrées du type 11 au type 13 par défaut.

Nous prendrons en charge le masquage des types 7, 11 et 12 vers le type 12. Nous ne prendrons pas en charge le masquage du type 12 vers le type 11.

Les nouveaux routeurs pourraient commencer à utiliser le nouveau type de signature par défaut après quelques mois. Les nouvelles destinations pourraient commencer à utiliser le nouveau type de signature par défaut après environ un an.

Pour la version minimale du routeur 0.9.TBD, les routeurs doivent s'assurer :

- Ne pas stocker (ou diffuser) un RI ou LS avec le nouveau type de signature vers des routeurs de version inférieure à 0.9.TBD.
- Lors de la vérification d'un stockage netdb, ne pas récupérer un RI ou LS avec le nouveau type de signature à partir de routeurs de version inférieure à 0.9.TBD.
- Les routeurs avec un nouveau type de signature dans leur RI ne peuvent pas se connecter à des routeurs de version inférieure à 0.9.TBD, que ce soit avec NTCP, NTCP2 ou SSU.
- Les connexions de streaming et les datagrammes signés ne fonctionneront pas avec des routeurs de version inférieure à 0.9.TBD, mais il n'y a aucun moyen de le savoir, donc le nouveau type de signature ne devrait pas être utilisé par défaut pendant une certaine période de mois ou d'années après la version 0.9.TBD.

## Références

.. [BLAKE2]
   https://blake2.net/blake2.pdf

.. [ED25519CTX]
   https://moderncrypto.org/mail-archive/curves/2017/000925.html

.. [ED25519-REFS]
    "High-speed high-security signatures" par Daniel
    J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe, et
    Bo-Yin Yang. http://cr.yp.to/papers.html#ed25519

.. [EDDSA-FAULTS]
   https://news.ycombinator.com/item?id=15414760

.. [LEA]
   https://fr.wikipedia.org/wiki/Attaque_par_extension_de_longueur

.. [RFC-7693]
   https://tools.ietf.org/html/rfc7693

.. [RFC-8032]
   https://tools.ietf.org/html/rfc8032

.. [ZCASH]
   https://github.com/zcash/zips/tree/master/protocol/protocol.pdf
