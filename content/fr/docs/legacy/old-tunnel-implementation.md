---
title: "Ancienne implémentation de tunnel"
description: "Documentation historique de l'implémentation originale des tunnels d'I2P avant la version 0.6.1.10"
slug: "old-tunnel-implementation"
aliases:
  - "/fr/docs/historical/tunnel-alt"
  - "/fr/docs/historical/tunnel-alt/"
  - "/fr/tunnel"
  - "/fr/tunnel/"
lastUpdated: "2016-11"
accurateFor: "historical"
---

**Note : Obsolète - NON utilisé ! Remplacé dans la version 0.6.1.10 - voir [l'implémentation actuelle](/docs/specs/tunnel-implementation) pour la spécification active.**

## 1) Aperçu des tunnels {#tunnel.overview}

Dans I2P, les messages sont transmis dans une direction à travers un tunnel virtuel de pairs, en utilisant tous les moyens disponibles pour transmettre le message au saut suivant. Les messages arrivent à la passerelle du tunnel, sont regroupés pour le chemin, et sont transmis au saut suivant dans le tunnel, qui traite et vérifie la validité du message et l'envoie au saut suivant, et ainsi de suite, jusqu'à ce qu'il atteigne le point de terminaison du tunnel. Ce point de terminaison prend les messages regroupés par la passerelle et les transmet selon les instructions - soit vers un autre router, vers un autre tunnel sur un autre router, ou localement.

Tous les tunnels fonctionnent de la même manière, mais peuvent être segmentés en deux groupes différents - les tunnels entrants et les tunnels sortants. Les tunnels entrants ont une passerelle non fiable qui transmet les messages vers le créateur du tunnel, qui sert de point de terminaison du tunnel. Pour les tunnels sortants, le créateur du tunnel sert de passerelle, transmettant les messages vers le point de terminaison distant.

Le créateur du tunnel sélectionne exactement quels pairs participeront au tunnel, et fournit à chacun les données de configuration nécessaires. Ils peuvent varier en longueur de 0 saut (où la passerelle est aussi le point de terminaison) à 7 sauts (où il y a 6 pairs après la passerelle et avant le point de terminaison). L'intention est de rendre difficile pour les participants ou les tiers de déterminer la longueur d'un tunnel, ou même pour des participants en collusion de déterminer s'ils font partie du même tunnel (sauf dans la situation où des pairs en collusion sont adjacents dans le tunnel). Les messages qui ont été corrompus sont également abandonnés dès que possible, réduisant la charge réseau.

Au-delà de leur longueur, il existe des paramètres configurables supplémentaires pour chaque tunnel qui peuvent être utilisés, tels qu'une limitation de la taille ou de la fréquence des messages délivrés, comment le remplissage doit être utilisé, combien de temps un tunnel doit rester en fonctionnement, s'il faut injecter des messages de brouillage, s'il faut utiliser la fragmentation, et quelles stratégies de traitement par lots, le cas échéant, doivent être employées.

En pratique, une série de groupes de tunnels sont utilisés à des fins différentes - chaque destination client locale a son propre ensemble de tunnels entrants et sortants, configurés pour répondre à ses besoins d'anonymat et de performance. De plus, le router lui-même maintient une série de groupes pour participer à la base de données réseau et pour gérer les tunnels eux-mêmes.

I2P est un réseau intrinsèquement à commutation de paquets, même avec ces tunnels, ce qui lui permet de tirer parti de plusieurs tunnels fonctionnant en parallèle, augmentant la résilience et équilibrant la charge. En dehors de la couche I2P centrale, il existe une bibliothèque de streaming de bout en bout optionnelle disponible pour les applications clientes, exposant un fonctionnement similaire à TCP, incluant la réorganisation des messages, la retransmission, le contrôle de congestion, etc.

## 2) Fonctionnement des tunnels {#tunnel.operation}

Le fonctionnement des tunnels comprend quatre processus distincts, pris en charge par différents pairs dans le tunnel. Premièrement, le gateway du tunnel accumule un certain nombre de messages de tunnel et les prétraite en quelque chose destiné à la livraison par tunnel. Ensuite, ce gateway chiffre ces données prétraitées, puis les transmet au premier saut. Ce pair, ainsi que les participants suivants du tunnel, retirent une couche du chiffrement, vérifient l'intégrité du message, puis le transmettent au pair suivant. Finalement, le message arrive au point de terminaison où les messages regroupés par le gateway sont à nouveau séparés et transmis comme demandé.

Les ID de tunnel sont des nombres de 4 octets utilisés à chaque saut - les participants savent quel ID de tunnel écouter pour les messages et quel ID de tunnel ils doivent utiliser pour les transmettre au saut suivant. Les tunnels eux-mêmes ont une durée de vie courte (10 minutes actuellement), mais selon l'objectif du tunnel, et bien que des tunnels ultérieurs puissent être construits en utilisant la même séquence de pairs, l'ID de tunnel de chaque saut changera.

### 2.1) Prétraitement des messages {#tunnel.preprocessing}

Lorsque la passerelle veut livrer des données à travers le tunnel, elle rassemble d'abord zéro ou plusieurs messages I2NP (pas plus de 32 Ko au total), sélectionne la quantité de remplissage qui sera utilisée, et décide comment chaque message I2NP doit être traité par le point de terminaison du tunnel, encodant ces données dans la charge utile brute du tunnel :

- Entier non signé de 2 octets spécifiant le nombre d'octets de remplissage
- ce nombre d'octets aléatoires
- une série de zéro ou plusieurs paires { instructions, message }

Les instructions sont encodées comme suit :

- Valeur de 1 octet :
  ```
  bits 0-1: type de livraison
            (0x0 = LOCAL, 0x01 = TUNNEL, 0x02 = ROUTER)
     bit 2: délai inclus ?  (1 = vrai, 0 = faux)
     bit 3: fragmenté ?  (1 = vrai, 0 = faux)
     bit 4: options étendues ?  (1 = vrai, 0 = faux)
  bits 5-7: réservé
  ```
- si le type de livraison était TUNNEL, un ID de tunnel de 4 octets
- si le type de livraison était TUNNEL ou ROUTER, un hash de router de 32 octets
- si le drapeau délai inclus est vrai, une valeur de 1 octet :
  ```
     bit 0: type (0 = strict, 1 = aléatoire)
  bits 1-7: exposant de délai (2^valeur minutes)
  ```
- si le drapeau fragmenté est vrai, un ID de message de 4 octets, et une valeur de 1 octet :
  ```
  bits 0-6: numéro de fragment
     bit 7: est-ce le dernier ?  (1 = vrai, 0 = faux)
  ```
- si le drapeau options étendues est vrai :
  ```
  = une taille d'option de 1 octet (en octets)
  = ce nombre d'octets
  ```
- Taille de 2 octets du message I2NP

Le message I2NP est encodé dans sa forme standard, et la charge utile prétraitée doit être complétée pour atteindre un multiple de 16 octets.

### 2.2) Traitement de la passerelle {#tunnel.gateway}

Après le préprocessing des messages en une charge utile rembourrée, la passerelle chiffre la charge utile avec les huit clés, construisant un bloc de somme de contrôle afin que chaque pair puisse vérifier l'intégrité de la charge utile à tout moment, ainsi qu'un bloc de vérification de bout en bout pour que le point de terminaison du tunnel vérifie l'intégrité du bloc de somme de contrôle. Les détails spécifiques suivent.

Le chiffrement utilisé est tel que le déchiffrement nécessite simplement de parcourir les données avec AES en mode CBC, de calculer le SHA256 d'une portion fixe spécifique du message (octets 16 à $size-144), et de rechercher les 16 premiers octets de ce hash dans le bloc de somme de contrôle. Il y a un nombre fixe de sauts défini (8 pairs) afin que nous puissions vérifier le message sans révéler la position dans le tunnel ni faire "rétrécir" continuellement le message au fur et à mesure que les couches sont supprimées. Pour les tunnels de moins de 8 sauts, le créateur du tunnel prendra la place des sauts excédentaires, déchiffrant avec ses clés (pour les tunnels sortants, ceci est fait au début, et pour les tunnels entrants, à la fin).

La partie difficile dans le chiffrement consiste à construire ce bloc de somme de contrôle intriqué, ce qui nécessite essentiellement de déterminer à quoi ressemblera le hachage de la charge utile à chaque étape, d'ordonner aléatoirement ces hachages, puis de construire une matrice de ce à quoi ressemblera chacun de ces hachages ordonnés aléatoirement à chaque étape. La passerelle elle-même doit prétendre qu'elle est l'un des pairs dans le bloc de somme de contrôle afin que le premier saut ne puisse pas détecter que le saut précédent était la passerelle. Pour visualiser cela un peu :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Peer</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Key</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Dir</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">IV</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">Payload</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[0]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[1]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[2]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[3]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[4]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[5]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[6]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">eH[7]</th>
      <th style="border:1px solid var(--color-border); padding:0.4rem; text-align:left; background:var(--color-bg-secondary);">V</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer0</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[0]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[0])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[0]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer1</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[1]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[1])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[1]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer2</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[2]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[2])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[2]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer3</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[3]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[3])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[3]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer4</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[4]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[4])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[4]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer5</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[5]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[5])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[5]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer6</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">recv</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[6]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[6])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[6]</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">peer7</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">K[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">send</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">IV[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">P[7]</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">H(P[7])</td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.4rem;">V[7]</td>
    </tr>
  </tbody>
</table>
Dans ce qui précède, P[7] est identique aux données originales transmises à travers le tunnel (les messages prétraités), et V[7] correspond aux 16 premiers octets du SHA256 de eH[0-7] tel qu'observé sur le pair7 après déchiffrement. Pour les cellules de la matrice situées "plus haut" que le hachage, leur valeur est dérivée en chiffrant la cellule située en dessous avec la clé du pair situé en dessous, en utilisant la fin de la colonne à sa gauche comme IV. Pour les cellules de la matrice situées "plus bas" que le hachage, elles sont égales à la cellule située au-dessus, déchiffrée par la clé du pair actuel, en utilisant la fin du bloc chiffré précédent sur cette ligne.

Avec cette matrice randomisée de blocs de somme de contrôle, chaque pair sera capable de trouver le hash de la charge utile, ou s'il n'y est pas, de savoir que le message est corrompu. L'entrelacement en utilisant le mode CBC augmente la difficulté de marquage des blocs de somme de contrôle eux-mêmes, mais il reste possible que ce marquage passe brièvement inaperçu si les colonnes après les données marquées ont déjà été utilisées pour vérifier la charge utile chez un pair. Dans tous les cas, le point de terminaison du tunnel (pair 7) sait avec certitude si l'un des blocs de somme de contrôle a été marqué, car cela corromprait le bloc de vérification (V[7]).

L'IV[0] est une valeur aléatoire de 16 octets, et IV[i] correspond aux 16 premiers octets de H(D(IV[i-1], K[i-1]) xor IV_WHITENER). Nous n'utilisons pas le même IV le long du chemin, car cela permettrait une collusion triviale, et nous utilisons le hash de la valeur déchiffrée pour propager l'IV afin d'entraver la fuite de clés. IV_WHITENER est une valeur fixe de 16 octets.

Lorsque la passerelle veut envoyer le message, elle exporte la bonne ligne pour le pair qui est le premier saut (généralement la ligne peer1.recv) et la transmet entièrement.

### 2.3) Traitement des participants {#tunnel.participant}

Lorsqu'un participant dans un tunnel reçoit un message, il déchiffre une couche avec sa clé de tunnel en utilisant AES256 en mode CBC avec les 16 premiers octets comme IV. Il calcule ensuite le hachage de ce qu'il voit comme charge utile (octets 16 à $size-144) et recherche ces 16 premiers octets de ce hachage dans le bloc de somme de contrôle déchiffré. Si aucune correspondance n'est trouvée, le message est rejeté. Sinon, l'IV est mis à jour en le déchiffrant, en effectuant un XOR de cette valeur avec l'IV_WHITENER, et en le remplaçant par les 16 premiers octets de son hachage. Le message résultant est ensuite transmis au pair suivant pour traitement.

Pour prévenir les attaques par rejeu au niveau du tunnel, chaque participant garde une trace des IV reçus pendant la durée de vie du tunnel, en rejetant les doublons. L'utilisation mémoire requise devrait être mineure, car chaque tunnel n'a qu'une durée de vie très courte (10m actuellement). Un débit constant de 100KBps à travers un tunnel avec des messages complets de 32KB donnerait 1875 messages, nécessitant moins de 30KB de mémoire. Les passerelles et points de terminaison gèrent le rejeu en suivant les ID de message et les expirations sur les messages I2NP contenus dans le tunnel.

### 2.4) Traitement des points d'extrémité {#tunnel.endpoint}

Lorsqu'un message atteint l'extrémité du tunnel, celle-ci le déchiffre et le vérifie comme un participant normal. Si le bloc de somme de contrôle a une correspondance valide, l'extrémité calcule alors le hachage du bloc de somme de contrôle lui-même (tel qu'il apparaît après déchiffrement) et le compare au hachage de vérification déchiffré (les 16 derniers octets). Si ce hachage de vérification ne correspond pas, l'extrémité prend note de la tentative de marquage par l'un des participants du tunnel et peut éventuellement rejeter le message.

À ce stade, le point de terminaison du tunnel possède les données prétraitées envoyées par la passerelle, qu'il peut ensuite analyser pour extraire les messages I2NP inclus et les transmettre comme demandé dans leurs instructions de livraison.

### 2.5) Remplissage {#tunnel.padding}

Plusieurs stratégies de remplissage de tunnel sont possibles, chacune ayant ses propres avantages :

- Aucun padding
- Padding à une taille aléatoire
- Padding à une taille fixe
- Padding au KB le plus proche
- Padding à la taille exponentielle la plus proche (2^n octets)

*Lequel utiliser ? aucun padding est le plus efficace, le padding aléatoire est ce que nous avons actuellement, une taille fixe serait soit un gaspillage extrême soit nous forcerait à implémenter la fragmentation. Le padding à la taille exponentielle la plus proche (comme Freenet) semble prometteur. Peut-être devrions-nous rassembler quelques statistiques sur le réseau concernant la taille des messages, puis voir quels coûts et bénéfices découleraient des différentes stratégies ?*

### 2.6) Fragmentation de tunnel {#tunnel.fragmentation}

Pour divers schémas de remplissage et de mélange, il peut être utile d'un point de vue anonymat de fragmenter un seul message I2NP en plusieurs parties, chacune étant livrée séparément via différents messages de tunnel. Le point de terminaison peut ou non prendre en charge cette fragmentation (supprimant ou conservant les fragments selon les besoins), et la gestion de la fragmentation ne sera pas implémentée immédiatement.

### 2.7) Alternatives {#tunnel.alternatives}

#### 2.7.1) Ne pas utiliser un bloc de somme de contrôle {#tunnel.nochecksum}

Une alternative au processus ci-dessus consiste à supprimer complètement le bloc de somme de contrôle et à remplacer le hash de vérification par un hash simple de la charge utile. Cela simplifierait le traitement au niveau de la passerelle tunnel et économiserait 144 octets de bande passante à chaque saut. D'autre part, les attaquants à l'intérieur du tunnel pourraient facilement ajuster la taille du message à une taille facilement traçable par des observateurs externes complices en plus des participants tunnel ultérieurs. La corruption entraînerait également le gaspillage de toute la bande passante nécessaire pour transmettre le message. Sans la validation par saut, il serait également possible de consommer des ressources réseau excessives en construisant des tunnels extrêmement longs, ou en créant des boucles dans le tunnel.

#### 2.7.2) Ajuster le traitement de tunnel en cours de route {#tunnel.reroute}

Bien que l'algorithme de routage de tunnel simple devrait être suffisant pour la plupart des cas, il existe trois alternatives qui peuvent être explorées :

- Retarder un message dans un tunnel à un saut arbitraire pendant soit une durée spécifiée soit une période aléatoire. Ceci pourrait être accompli en remplaçant le hash dans le bloc de somme de contrôle par par exemple les 8 premiers octets du hash, suivis de quelques instructions de délai. Alternativement, les instructions pourraient dire au participant d'interpréter réellement la charge utile brute telle qu'elle est, et soit rejeter le message soit continuer à le transmettre le long du chemin (où il serait interprété par le point de terminaison comme un message de bourrage). La dernière partie de ceci nécessiterait que la passerelle ajuste son algorithme de chiffrement pour produire la charge utile en clair sur un saut différent, mais cela ne devrait pas poser beaucoup de difficultés.

- Permettre aux routers participant à un tunnel de remixer le message avant de le transmettre - en le faisant rebondir à travers l'un des tunnels sortants de ce pair, avec des instructions pour la livraison au prochain saut. Ceci pourrait être utilisé soit de manière contrôlée (avec des instructions en route comme les délais ci-dessus) soit de manière probabiliste.

- Implémenter le code pour que le créateur de tunnel puisse redéfinir le "saut suivant" d'un pair dans le tunnel, permettant une redirection dynamique supplémentaire.

#### 2.7.3) Utiliser des tunnels bidirectionnels {#tunnel.bidirectional}

La stratégie actuelle d'utilisation de deux tunnels séparés pour les communications entrantes et sortantes n'est pas la seule technique disponible, et elle a des implications en matière d'anonymat. Du côté positif, en utilisant des tunnels séparés, cela réduit les données de trafic exposées à l'analyse aux participants d'un tunnel - par exemple, les pairs dans un tunnel sortant depuis un navigateur web ne verraient que le trafic d'une requête HTTP GET, tandis que les pairs dans un tunnel entrant verraient la charge utile livrée le long du tunnel. Avec des tunnels bidirectionnels, tous les participants auraient accès au fait que par exemple 1 Ko a été envoyé dans une direction, puis 100 Ko dans l'autre. Du côté négatif, utiliser des tunnels unidirectionnels signifie qu'il y a deux ensembles de pairs qui doivent être profilés et pris en compte, et des précautions supplémentaires doivent être prises pour traiter la vitesse accrue des attaques de prédécesseur. Le processus de regroupement et de construction de tunnels décrit ci-dessous devrait minimiser les inquiétudes concernant l'attaque de prédécesseur, bien que si cela était souhaité, il ne serait pas très difficile de construire à la fois les tunnels entrants et sortants le long des mêmes pairs.

#### 2.7.4) Utiliser une taille de bloc plus petite {#tunnel.smallerhashes}

À l'heure actuelle, notre utilisation d'AES limite notre taille de bloc à 16 octets, ce qui fournit à son tour la taille minimale pour chacune des colonnes de bloc de somme de contrôle. Si un autre algorithme était utilisé avec une taille de bloc plus petite, ou pouvait permettre autrement la construction sécurisée du bloc de somme de contrôle avec des portions plus petites du hachage, cela pourrait valoir la peine d'être exploré. Les 16 octets utilisés maintenant à chaque saut devraient être largement suffisants.

## 3) Construction de tunnel {#tunnel.building}

Lors de la construction d'un tunnel, le créateur doit envoyer une requête avec les données de configuration nécessaires à chacun des relais, puis attendre que le participant potentiel réponde en indiquant qu'il accepte ou refuse. Ces messages de requête de tunnel et leurs réponses sont encapsulés par garlic encryption de sorte que seul le router qui connaît la clé peut les déchiffrer, et le chemin emprunté dans les deux directions est également routé par tunnel. Il y a trois dimensions importantes à garder à l'esprit lors de la production des tunnels : quels pairs sont utilisés (et où), comment les requêtes sont envoyées (et les réponses reçues), et comment ils sont maintenus.

### 3.1) Sélection des pairs {#tunnel.peerselection}

Au-delà des deux types de tunnels - entrants et sortants - il existe deux styles de sélection de pairs utilisés pour différents tunnels - exploratoire et client. Les tunnels exploratoires sont utilisés à la fois pour la maintenance de la base de données réseau et la maintenance des tunnels, tandis que les tunnels clients sont utilisés pour les messages clients de bout en bout.

#### 3.1.1) Sélection des pairs pour les tunnels exploratoires {#tunnel.selection.exploratory}

Les tunnels exploratoires sont construits à partir d'une sélection aléatoire de pairs issus d'un sous-ensemble du réseau. Ce sous-ensemble particulier varie selon le router local et ses besoins de routage de tunnels. En général, les tunnels exploratoires sont construits à partir de pairs sélectionnés aléatoirement qui se trouvent dans la catégorie de profil "non défaillant mais actif" du pair. L'objectif secondaire des tunnels, au-delà du simple routage de tunnels, est de trouver des pairs haute capacité sous-utilisés afin qu'ils puissent être promus pour une utilisation dans les tunnels clients.

#### 3.1.2) Sélection des pairs de tunnel client {#tunnel.selection.client}

Les tunnels clients sont construits avec un ensemble d'exigences plus strictes - le router local sélectionnera des pairs dans sa catégorie de profil "rapide et haute capacité" afin que les performances et la fiabilité répondent aux besoins de l'application cliente. Cependant, il y a plusieurs détails importants au-delà de cette sélection de base qui doivent être respectés, selon les besoins d'anonymat du client.

Pour certains clients qui s'inquiètent d'adversaires montant une attaque de prédécesseur, la sélection de tunnel peut maintenir les pairs sélectionnés dans un ordre strict - si A, B, et C sont dans un tunnel, le saut après A est toujours B, et le saut après B est toujours C. Un ordonnancement moins strict est également possible, assurant que bien que le saut après A puisse être B, B ne peut jamais être avant A. D'autres options de configuration incluent la capacité pour seulement les passerelles de tunnel entrant et les points de sortie de tunnel sortant d'être fixes, ou alternés selon un taux MTBF.

### 3.2) Livraison de requêtes {#tunnel.request}

Comme mentionné ci-dessus, une fois que le créateur du tunnel sait quels pairs doivent être inclus dans un tunnel et dans quel ordre, le créateur construit une série de messages de requête de tunnel, chacun contenant les informations nécessaires pour ce pair. Par exemple, les tunnels participants recevront l'ID de tunnel de 4 octets sur lequel ils doivent recevoir des messages, l'ID de tunnel de 4 octets sur lequel ils doivent envoyer les messages, le hash de 32 octets de l'identité du prochain saut, et la clé de couche de 32 octets utilisée pour supprimer une couche du tunnel. Bien entendu, les points de terminaison des tunnels sortants ne reçoivent aucune information de "prochain saut" ou "ID de tunnel suivant". Les passerelles des tunnels entrants reçoivent cependant les 8 clés de couche dans l'ordre où elles doivent être chiffrées (comme décrit ci-dessus). Pour permettre les réponses, la requête contient une étiquette de session aléatoire et une clé de session aléatoire avec laquelle le pair peut chiffrer avec garlic encryption sa décision, ainsi que le tunnel auquel ce garlic doit être envoyé. En plus des informations ci-dessus, diverses options spécifiques au client peuvent être incluses, telles que la limitation à placer sur le tunnel, les stratégies de remplissage ou de traitement par lots à utiliser, etc.

Après avoir construit tous les messages de requête, ils sont encapsulés par garlic encryption pour le router cible et envoyés via un tunnel exploratoire. À la réception, ce pair détermine s'il peut ou veut participer, créant un message de réponse et encapsulant la réponse par garlic encryption et routage tunnel avec les informations fournies. À la réception de la réponse chez le créateur du tunnel, le tunnel est considéré comme valide sur ce saut (si accepté). Une fois que tous les pairs ont accepté, le tunnel devient actif.

### 3.3) Mise en commun {#tunnel.pooling}

Pour permettre un fonctionnement efficace, le router maintient une série de pools de tunnels, chacun gérant un groupe de tunnels utilisés dans un but spécifique avec leur propre configuration. Lorsqu'un tunnel est nécessaire pour cet usage, le router en sélectionne un aléatoirement dans le pool approprié. Globalement, il existe deux pools de tunnels exploratoires - un entrant et un sortant - chacun utilisant les paramètres d'exploration par défaut du router. De plus, il y a une paire de pools pour chaque destination locale - un tunnel entrant et un tunnel sortant. Ces pools utilisent la configuration spécifiée lorsque la destination locale s'est connectée au router, ou les paramètres par défaut du router si aucune configuration n'est spécifiée.

Chaque pool contient dans sa configuration quelques paramètres clés, définissant combien de tunnels maintenir actifs, combien de tunnels de sauvegarde conserver en cas de défaillance, à quelle fréquence tester les tunnels, quelle longueur les tunnels devraient avoir, si ces longueurs devraient être randomisées, à quelle fréquence les tunnels de remplacement devraient être construits, ainsi que tous les autres paramètres autorisés lors de la configuration de tunnels individuels.

### 3.4) Alternatives {#tunnel.building.alternatives}

#### 3.4.1) Construction télescopique {#tunnel.building.telescoping}

Une question qui peut se poser concernant l'utilisation des tunnels exploratoires pour envoyer et recevoir les messages de création de tunnel est de savoir comment cela affecte la vulnérabilité du tunnel aux attaques de prédécesseur. Bien que les points de terminaison et les passerelles de ces tunnels soient distribués de manière aléatoire à travers le réseau (incluant peut-être même le créateur du tunnel dans cet ensemble), une autre alternative consiste à utiliser les chemins de tunnel eux-mêmes pour transmettre la demande et la réponse, comme cela se fait dans [TOR](https://www.torproject.org/). Ceci, cependant, peut conduire à des fuites lors de la création du tunnel, permettant aux pairs de découvrir combien de sauts il y a plus tard dans le tunnel en surveillant le timing ou le nombre de paquets pendant la construction du tunnel. Des techniques pourraient être utilisées pour minimiser ce problème, comme utiliser chacun des sauts comme points de terminaison (selon [2.7.2](#tunnel.reroute)) pour un nombre aléatoire de messages avant de continuer à construire le saut suivant.

#### 3.4.2) Tunnels non exploratoires pour la gestion {#tunnel.building.nonexploratory}

Une seconde alternative au processus de construction de tunnel consiste à donner au router un ensemble supplémentaire de pools entrants et sortants non exploratoires, en les utilisant pour les requêtes et réponses de tunnel. En supposant que le router dispose d'une vue bien intégrée du réseau, cela ne devrait pas être nécessaire, mais si le router était partitionné d'une manière ou d'une autre, utiliser des pools non exploratoires pour la gestion des tunnels réduirait la fuite d'informations sur les pairs qui se trouvent dans la partition du router.

## 4) Limitation de débit des tunnels {#tunnel.throttling}

Même si les tunnels au sein d'I2P ressemblent à un réseau à commutation de circuits, tout dans I2P est strictement basé sur des messages - les tunnels ne sont que des astuces comptables pour aider à organiser la livraison des messages. Aucune hypothèse n'est faite concernant la fiabilité ou l'ordre des messages, et les retransmissions sont laissées aux niveaux supérieurs (par exemple, la bibliothèque de streaming de la couche client d'I2P). Cela permet à I2P de tirer parti des techniques de régulation disponibles pour les réseaux à commutation de paquets et à commutation de circuits. Par exemple, chaque router peut suivre la moyenne mobile de la quantité de données utilisée par chaque tunnel, la combiner avec toutes les moyennes utilisées par les autres tunnels auxquels le router participe, et être capable d'accepter ou de rejeter des demandes de participation à des tunnels supplémentaires en fonction de sa capacité et de son utilisation. D'autre part, chaque router peut simplement abandonner les messages qui dépassent sa capacité, exploitant les recherches utilisées sur l'Internet normal.

## 5) Mélange/regroupement {#tunnel.mixing}

Quelles stratégies devraient être utilisées au niveau de la passerelle et à chaque saut pour retarder, réordonner, rediriger ou compléter les messages ? Dans quelle mesure cela devrait-il être fait automatiquement, quelle part devrait être configurée comme paramètre par tunnel ou par saut, et comment le créateur du tunnel (et par extension, l'utilisateur) devrait-il contrôler cette opération ? Tout cela reste inconnu, à déterminer pour une version future.
