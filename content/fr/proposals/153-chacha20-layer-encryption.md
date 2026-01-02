---
title: "Chiffrement de Couche de Tunnel ChaCha"
number: "153"
author: "chisana"
created: "2019-08-04"
lastupdated: "2019-08-05"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2753"
toc: true
---

## Vue d'ensemble

Cette proposition s'appuie sur et nécessite les modifications de la proposition 152 : Tunnels ECIES.

Seuls les tunnels construits à travers des sauts supportant le format BuildRequestRecord pour les tunnels ECIES-X25519 peuvent implémenter cette spécification.

Cette spécification nécessite le format Tunnel Build Options pour indiquer le type de chiffrement de couche de tunnel et transmettre les clés AEAD de couche.

### Objectifs

Les objectifs de cette proposition sont :

- Remplacer AES256/ECB+CBC par ChaCha20 pour l'IV du tunnel établi et le chiffrement de couche
- Utiliser ChaCha20-Poly1305 pour la protection AEAD inter-saut
- Être indétectable à partir du chiffrement de couche de tunnel existant par des participants non-tunnel
- Ne pas modifier la longueur globale du message de tunnel

### Traitement des Messages de Tunnel Établis

Cette section décrit les modifications concernant :

- Prétraitement + chiffrement des passerelles sortantes et entrantes
- Chiffrement et post-traitement des participants
- Chiffrement et post-traitement des points de terminaison sortants et entrants

Pour un aperçu du traitement actuel des messages de tunnel, voir la spécification [Tunnel Implementation](/docs/specs/implementation/).

Seules les modifications pour les routeurs supportant le chiffrement de couche ChaCha20 sont discutées.

Aucune modification n'est envisagée pour les tunnels mixtes avec chiffrement de couche AES, jusqu'à ce qu'un protocole sûr puisse être conçu pour convertir un IV AES 128 bits en nonce ChaCha20 64 bits. Les filtres de Bloom garantissent l'unicité pour l'ensemble de l'IV, mais la première moitié des IV uniques pourrait être identique.

Cela signifie que le chiffrement de la couche doit être uniforme pour tous les sauts dans le tunnel et établi à l'aide des options de construction de tunnel pendant le processus de création de tunnel.

Toutes les passerelles et les participants de tunnel devront maintenir un filtre de Bloom pour valider les deux nonces indépendants.

Le ``nonceKey`` mentionné tout au long de cette proposition remplace le ``IVKey`` utilisé dans le chiffrement de couche AES. Il est généré en utilisant le même KDF de la proposition 152.

### Chiffrement AEAD des Messages de Saut à Saut

Une clé ``AEADKey`` unique supplémentaire devra être générée pour chaque paire de sauts consécutifs. Cette clé sera utilisée par les sauts consécutifs pour chiffrer et déchiffrer les messages de tunnel internes chiffrés ChaCha20.

Les messages de tunnel devront réduire la longueur du cadre chiffré interne de 16 octets pour accueillir le MAC Poly1305.

AEAD ne peut pas être utilisé directement sur les messages, car le déchiffrement itératif est nécessaire par les tunnels sortants. Le déchiffrement itératif ne peut être réalisé, dans son utilisation actuelle, qu'en utilisant ChaCha20 sans AEAD.

```text
+----+----+----+----+----+----+----+----+
  |    ID de Tunnel    |   tunnelNonce     |
  +----+----+----+----+----+----+----+----+
  | suite de tunnelNonce |    obfsNonce      |
  +----+----+----+----+----+----+----+----+
  | suite d'obfsNonce  |                   |
  +----+----+----+----+                   +
  |                                       |
  +           Données Chiffrées           +
  ~                                       ~
  |                                       |
  +                   +----+----+----+----+
  |                   |    MAC Poly1305    |
  +----+----+----+----+                   +  
  |                                       |
  +                   +----+----+----+----+
  |                   |
  +----+----+----+----+

  ID de Tunnel :: `TunnelId`
         4 octets
         l'ID du prochain saut

  tunnelNonce ::
         8 octets
         le nonce de couche du tunnel

  obfsNonce ::
         8 octets
         le nonce de chiffrement de couche du tunnel

  Données Chiffrées ::
         992 octets
         le message chiffré du tunnel

  MAC Poly1305 ::
         16 octets

  taille totale : 1028 Octets
```

Les sauts internes (avec des sauts précédents et suivants) auront deux ``AEADKeys``, un pour déchiffrer la couche AEAD du saut précédent, et chiffrer la couche AEAD vers le saut suivant.

Tous les participants au saut interne auront ainsi 64 octets supplémentaires de matériel de clé inclus dans leurs BuildRequestRecords.

Le Point d'Entrée Sortant et la Passerelle Entrante ne nécessiteront que 32 octets supplémentaires de données clé, puisqu'ils ne chiffrent pas la couche tunnel lors du transfert de messages entre eux.

La Passerelle Sortante génère sa clé ``outAEAD``, qui est identique à la clé ``inAEAD`` du premier saut sortant.

Le Point d'Entrée Entrant génère sa clé ``inAEAD``, qui est identique à la clé ``outAEAD`` du dernier saut entrant.

Les sauts internes recevront et utiliseront une ``inAEADKey`` pour déchiffrer les messages entrants et une ``outAEADKey`` pour chiffrer les messages sortants, respectivement.

À titre d'exemple, dans un tunnel avec sauts internes OBGW, A, B, OBEP :

- La clé ``inAEADKey`` de A est identique à la clé ``outAEADKey`` de OBGW
- La clé ``inAEADKey`` de B est identique à la clé ``outAEADKey`` de A
- La clé ``outAEADKey`` de B est identique à la clé ``inAEADKey`` de OBEP

Les clés sont uniques aux paires de sauts, donc la clé ``inAEADKey`` de OBEP sera différente de la clé ``inAEADKey`` de A, la clé ``outAEADKey`` de A sera différente de la clé ``outAEADKey`` de B, etc.

### Traitement des Messages de Créateur de Tunnel et de Passerelle

Les passerelles fragmenteront et regrouperont les messages de la même manière, en réservant de l'espace après le cadre d'instructions-fragment pour le MAC Poly1305.

Les messages I2NP internes contenant des cadres AEAD (y compris le MAC) peuvent être répartis sur plusieurs fragments, mais tout fragment perdu entraînera un échec du déchiffrement AEAD (échec de la vérification MAC) au point d'extrémité.

### Prétraitement & Chiffrement de Passerelle

Lorsque les tunnels supportent le chiffrement de couche ChaCha20, les passerelles généreront deux nonces 64 bits par ensemble de messages.

Tunnels entrants :

- Chiffrer l'IV et le(s) message(s) de tunnel en utilisant ChaCha20
- Utiliser un ``tunnelNonce`` et ``obfsNonce`` de 8 octets compte tenu de la durée de vie des tunnels
- Utiliser un ``obfsNonce`` de 8 octets pour le chiffrement de ``tunnelNonce``
- Détruire le tunnel avant 2^(64 - 1) - 1 ensembles de messages : 2^63 - 1 = 9,223,372,036,854,775,807

  - Limite de nonce en place pour éviter la collision des nonces 64 bits
  - Limite de nonce presque impossible à atteindre, compte tenu que cela représenterait ~15,372,286,728,091,294 msgs/seconde pour des tunnels de 10 minutes

- Ajuster le filtre de Bloom en fonction d'un nombre raisonnable d'éléments attendus (128 msgs/sec, 1024 msgs/sec ? À déterminer)

La passerelle entrante (IBGW) du tunnel, traite les messages reçus d'un point de terminaison sortant (OBEP) d'un autre tunnel.

À ce stade, la couche extérieure du message est chiffrée à l'aide d'un chiffrement de transport point à point. Les en-têtes de message I2NP sont visibles, au niveau de la couche tunnel, par OBEP et IBGW. Les messages I2NP internes sont enveloppés dans des gousses Garlic, chiffrés en utilisant un chiffrement de session de bout en bout.

L'IBGW prétraite les messages dans les messages de tunnel formatés de manière appropriée, et chiffre comme suit :

```text

// L'IBGW génère des nonces aléatoires, assurant aucune collision dans son filtre de Bloom pour chaque nonce
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)
  // L'IBGW "chiffre" chaque message de tunnel prétraité avec son tunnelNonce et sa layerKey en utilisant ChaCha20
  encMsg = ChaCha20(msg = tunnel msg, nonce = tunnelNonce, key = layerKey)

  // Chacre20-Poly1305 chiffre chaque cadre de données chiffrées du message avec le tunnelNonce et outAEADKey
  (encMsg, MAC) = ChanCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)
```

Le format du message de tunnel changera légèrement, utilisant deux nonces de 8 octets au lieu d'un IV de 16 octets. Le ``obfsNonce`` utilisé pour chiffrer le nonce est ajouté au ``tunnelNonce`` de 8 octets et est chiffré par chaque saut en utilisant le ``tunnelNonce`` chiffré et le ``nonceKey`` du saut.

Après que l'ensemble de messages a été préalablement déchiffré pour chaque saut, la passerelle sortante chiffre à nouveau la partie du message de tunnel en utilisant ChaCha20-Poly1305 AEAD en utilisant le ``tunnelNonce`` et sa ``outAEADKey``.

Tunnels sortants :

- Déchiffrer de manière itérative les messages de tunnel
- Chiffrer ChaCha20-Poly1305 de manière préemptive les cadres chiffrés de message de tunnel
- Utiliser les mêmes règles pour les nonces de couche que pour les tunnels entrants
- Générer des nonces aléatoires une fois par ensemble de messages de tunnel expédiés

```text


// Pour chaque ensemble de messages, générer des nonces uniques et aléatoires
  tunnelNonce = Random(len = 64-bits)
  obfsNonce = Random(len = 64-bits)

  // Pour chaque saut, décrypter ChaCha20 le tunnelNonce précédent avec le key IV du saut actuel
  tunnelNonce = ChaCha20(msg = prev. tunnelNonce, nonce = obfsNonce, key = hop's nonceKey)

  // Pour chaque saut, décrypter ChaCha20 le message de tunnel avec le tunnelNonce actuel et layerKey du saut
  decMsg = ChaCha20(msg = tunnel msg(s), nonce = tunnelNonce, key = hop's layerKey)

  // Pour chaque saut, décrypter ChaCha20 le obfsNonce avec le tunnelNonce chiffré actuel et nonceKey du saut
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = hop's nonceKey)

  // Après le traitement des sauts, chiffrer ChaCha20-Poly1305 chaque cadre de données "déchiffrées" des messages de tunnel avec le premier tunnelNonce chiffré des sauts et inAEADKey du saut
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = decMsg, nonce = first hop's encrypted tunnelNonce, key = first hop's inAEADKey / GW outAEADKey)
```

### Traitement des Participants

Les participants suivront les messages reçus de la même manière, utilisant des filtres de Bloom décroissants.

Les nonces de tunnel devront être chiffrés une fois par saut, pour éviter les attaques de confirmation par des sauts collusifs non-consecutifs.

Les sauts chiffreront le nonce reçu pour éviter les attaques de confirmation entre des sauts précédents et ultérieurs, c'est-à-dire, les sauts collusifs et non-consecutifs étant capables de dire qu'ils appartiennent au même tunnel.

Pour valider les ``tunnelNonce`` et ``obfsNonce`` reçus, les participants vérifient chaque nonce individuellement contre leur filtre de Bloom pour éviter les doublons.

Après validation, le participant :

- Déchiffre ChaCha20-Poly1305 chaque cadre chiffré AEAD des messages de tunnel avec le ``tunnelNonce`` reçu et sa ``inAEADKey``
- Chiffre ChaCha20 le ``tunnelNonce`` avec le ``nonceKey`` reçu et le ``obfsNonce``
- Chiffre ChaCha20 chaque cadre de données chiffré du message de tunnel avec le ``tunnelNonce`` chiffré et sa ``layerKey``
- Chiffre ChaCha20-Poly1305 chaque cadre de données chiffré de message de tunnel avec le ``tunnelNonce`` chiffré et sa ``outAEADKey`` 
- Chiffre ChaCha20 le ``obfsNonce`` avec son ``nonceKey`` et le ``tunnelNonce`` chiffré
- Envoie le tuple {``nextTunnelId``, chiffré (``tunnelNonce`` || ``obfsNonce``), texte chiffré AEAD || MAC} au saut suivant.

```text

// Pour vérification, les sauts de tunnel devraient vérifier le filtre de Bloom pour l'unicité de chaque nonce reçu
  // Après vérification, défaire le(s) cadre(s) AEAD en déchiffrant ChaCha20-Poly1305 chaque cadre chiffré des messages de tunnel
  // avec le tunnelNonce reçu et inAEADKey 
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg = encMsg reçu \|\| MAC, nonce = tunnelNonce reçu, key = inAEADKey)

  // Chiffre ChaCha20 le tunnelNonce avec le obfsNonce reçu et nonceKey du saut
  tunnelNonce = ChaCha20(msg = tunnelNonce reçu, nonce = obfsNonce reçu, key = nonceKey)

  // Chiffre ChaCha20 chaque cadre de données chiffré du message de tunnel avec le tunnelNonce chiffré et layerKey du saut
  encMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)

  // Pour la protection AEAD, chiffre également ChaCha20-Poly1305 chaque cadre de données chiffré
  // avec le tunnelNonce chiffré et outAEADKey du saut
  (encMsg, MAC) = ChaCha20-Poly1305-Encrypt(msg = encMsg, nonce = tunnelNonce, key = outAEADKey)

  // Chiffre ChaCha20 le obfsNonce reçu avec le tunnelNonce chiffré et nonceKey du saut
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
```

### Traitement du Point de Terminaison Entrant

Pour les tunnels ChaCha20, le schéma suivant sera utilisé pour déchiffrer chaque message de tunnel :

- Valider les ``tunnelNonce`` et ``obfsNonce`` reçus indépendamment contre son filtre de Bloom
- Déchiffrer ChaCha20-Poly1305 le cadre de données chiffré en utilisant le ``tunnelNonce`` reçu et ``inAEADKey``
- Déchiffrer ChaCha20 le cadre de données chiffré en utilisant le ``tunnelNonce`` reçu et ``layerKey`` du saut
- Déchiffrer ChaCha20 le ``obfsNonce`` en utilisant le ``nonceKey`` du saut et le ``tunnelNonce`` reçu pour obtenir le ``obfsNonce`` précédent
- Déchiffrer ChaCha20 le ``tunnelNonce`` reçu en utilisant le ``nonceKey`` du saut et ``obfsNonce`` déchiffré pour obtenir le ``tunnelNonce`` précédent
- Déchiffrer ChaCha20 les données chiffrées en utilisant le ``tunnelNonce`` déchiffré et la ``layerKey`` du saut précédent
- Répéter les étapes pour déchiffrement des nonces et de la couche pour chaque saut dans le tunnel, jusqu'à l'IBGW
- La déchiffrement du cadre AEAD n'est nécessaire que lors du premier tour

```text

// Pour le premier tour, déchiffre ChaCha20-Poly1305 chaque cadre de données chiffré + MAC
  // en utilisant le tunnelNonce reçu et inAEADKey
  msg = encTunMsg \|\| MAC
  tunnelNonce = tunnelNonce reçu
  encTunMsg = ChaCha20-Poly1305-Decrypt(msg, nonce = tunnelNonce, key = inAEADKey)

  // Répéter pour chaque saut dans le tunnel jusqu'à l'IBGW
  // Pour chaque tour, déchiffre ChaCha20 chaque chiffrement de couche de chaque message de cadre de données chiffré
  // Remplacer le tunnelNonce reçu par le tunnelNonce déchiffré du tour précédent pour chaque saut
  decMsg = ChaCha20(msg = encTunMsg, nonce = tunnelNonce, key = layerKey)
  obfsNonce = ChaCha20(msg = obfsNonce, nonce = tunnelNonce, key = nonceKey)
  tunnelNonce = ChaCha20(msg = tunnelNonce, nonce = obfsNonce, key = nonceKey)
```

### Analyse de Sécurité pour le Chiffrement de Couche de Tunnel ChaCha20+ChaCha20-Poly1305

Passer d'AES256/ECB+AES256/CBC à ChaCha20+ChaCha20-Poly1305 présente plusieurs avantages et de nouvelles considérations de sécurité.

Les plus grandes considérations de sécurité à prendre en compte sont que les nonces ChaCha20 et ChaCha20-Poly1305 doivent être uniques par message, pendant la durée de vie de la clé utilisée.

Ne pas utiliser des nonces uniques avec la même clé sur des messages différents casse ChaCha20 et ChaCha20-Poly1305.

Utiliser un ``obfsNonce`` ajouté permet à l'IBEP de déchiffrer le ``tunnelNonce`` pour chaque chiffrement de couche de saut, récupérant le nonce précédent.

Le ``obfsNonce`` aux côtés du ``tunnelNonce`` ne révèle aucune nouvelle information aux sauts de tunnel, puisque le ``obfsNonce`` est chiffré en utilisant le ``tunnelNonce`` chiffré. Cela permet également à l'IBEP de récupérer le ``obfsNonce`` précédent d'une manière similaire à la récupération du ``tunnelNonce``.

Le plus grand avantage en matière de sécurité est qu'il n'y a pas d'attaques de confirmation ou d'oracle contre ChaCha20, et utiliser ChaCha20-Poly1305 entre les sauts ajoute une protection AEAD contre la manipulation de texte chiffré par des attaquants MITM hors bande.

Il existe des attaques d'oracle pratiques contre AES256/ECB + AES256/CBC, lorsque la clé est réutilisée (comme dans le chiffrement de couche de tunnel).

Les attaques d'oracle contre AES256/ECB ne fonctionneront pas, en raison du double chiffrement utilisé, et le chiffrement est effectué sur un seul bloc (l'IV de tunnel).

Les attaques d'oracle de padding contre AES256/CBC ne fonctionneront pas, car aucun padding n'est utilisé. Si la longueur du message de tunnel changeait jamais vers des longueurs non mod-16, AES256/CBC ne serait toujours pas vulnérable en raison du rejet des IV en doublon.

Les deux attaques sont également bloquées en interdisant les multiples appels d'oracle utilisant le même IV, les IV en doublon étant rejetés.

## Références

* [Tunnel-Implementation](/docs/specs/implementation/)
