---
title: "Transport SSU (Déprécié)"
description: "Transport UDP d'origine utilisé avant SSU2"
slug: "ssu"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
type: docs
reviewStatus: "needs-review"
---

> **Obsolète :** SSU (Secure Semi-Reliable UDP) a été remplacé par [SSU2](/docs/specs/ssu2/). Java I2P a retiré SSU dans la version 2.4.0 (API 0.9.61) et i2pd l'a retiré dans la version 2.44.0 (API 0.9.56). Ce document est conservé uniquement à des fins de référence historique.

## Points forts

- Transport UDP fournissant une livraison point à point chiffrée et authentifiée des messages I2NP.
- S’appuyait sur un échange Diffie–Hellman de 2048 bits (même nombre premier qu’ElGamal).
- Chaque datagramme transportait un HMAC‑MD5 de 16 octets (variante tronquée non standard) + un IV de 16 octets, suivi d’une charge utile chiffrée en AES‑256‑CBC.
- La prévention des attaques par rejeu et l’état de session étaient suivis à l’intérieur de la charge utile chiffrée.

## En-tête de message

```
[16-byte MAC][16-byte IV][encrypted payload]
```
Calcul de MAC utilisé : `HMAC-MD5(ciphertext || IV || (len ^ version ^ ((netid-2)<<8)))` avec une clé MAC de 32 octets. La longueur de la charge utile (payload), un entier 16 bits big-endian, était ajoutée dans le calcul du MAC. La version du protocole avait pour valeur par défaut `0` ; netId avait pour valeur par défaut `2` (réseau principal).

## Clés de session et de MAC

Dérivé du secret partagé DH:

1. Convertissez la valeur partagée en un tableau d’octets big-endian (préfixez par `0x00` si le bit de poids fort est à 1).
2. Clé de session : les 32 premiers octets (complétez avec des zéros si plus court).
3. Clé MAC : octets 33–64 ; si insuffisant, utilisez à défaut le hachage SHA-256 de la valeur partagée.

## Statut

Les routers n'annoncent plus d'adresses SSU. Les clients devraient migrer vers les transports SSU2 ou NTCP2. Des implémentations historiques peuvent être trouvées dans des versions plus anciennes :

- Sources Java antérieures à la 2.4.0 sous `router/transport/udp`
- Sources i2pd antérieures à la 2.44.0

Pour le comportement actuel du transport UDP, voir la [spécification SSU2](/docs/specs/ssu2/) (version 2 de SSU).
