---
title: "Spécification de création de tunnel (ECIES-X25519)"
description: "Chiffrement des messages de construction de tunnel utilisant les primitives cryptographiques ECIES-X25519 pour la confidentialité persistante."
slug: "tunnel-creation-ecies"
aliases:
  - "/fr/docs/specs/tunnel-creation-ecies-spec"
  - "/fr/docs/specs/tunnel-creation-ecies-spec/"
category: "Protocoles"
lastUpdated: "2025-06"
accurateFor: "0.9.66"
---

## Aperçu

Ce document spécifie le chiffrement des messages Tunnel Build utilisant les primitives cryptographiques introduites par [ECIES-X25519](/docs/specs/ecies/). Il fait partie de la proposition globale [Prop156](/proposals/156/) pour convertir les routers d'ElGamal vers les clés ECIES-X25519.

Deux versions sont spécifiées. La première utilise les messages de construction existants et la taille d'enregistrement de construction actuelle, pour la compatibilité avec les routeurs ElGamal. Cette spécification a été implémentée à partir de la version 0.9.48 et est maintenant dépréciée. La seconde utilise deux nouveaux messages de construction et une taille d'enregistrement de construction plus petite, et ne peut être utilisée qu'avec les routeurs ECIES. Cette spécification est implémentée à partir de la version 0.9.51.

Dans le but de faire la transition du réseau d'ElGamal + AES256 vers ECIES + ChaCha20, les tunnels avec des routers ElGamal et ECIES mixtes sont nécessaires. Les spécifications pour gérer les sauts de tunnel mixtes sont fournies. Aucun changement ne sera apporté au format, au traitement ou au chiffrement des sauts ElGamal. Ce format maintient la même taille pour les enregistrements de construction de tunnel, comme requis pour la compatibilité.

Les créateurs de tunnel ElGamal génèreront des paires de clés X25519 éphémères par saut, et suivront cette spécification pour créer des tunnels contenant des sauts ECIES.

Ce document spécifie la construction de tunnels ECIES-X25519. Pour un aperçu de tous les changements requis pour les routeurs ECIES, voir la proposition 156 [Prop156](/proposals/156/). Pour plus d'informations sur le développement de la spécification des enregistrements longs, voir la proposition 152 [Prop152](/proposals/152/). Pour plus d'informations sur le développement de la spécification des enregistrements courts, voir la proposition 157 [Prop157](/proposals/157/).

### Primitives cryptographiques

Les primitives requises pour implémenter cette spécification sont :

- AES-256-CBC comme dans [Cryptography](/docs/specs/cryptography/)
- Fonctions STREAM ChaCha20 : ENCRYPT(k, iv, plaintext) et DECRYPT(k, iv, ciphertext) - comme dans [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) et [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Fonctions STREAM ChaCha20/Poly1305 : ENCRYPT(k, n, plaintext, ad) et DECRYPT(k, n, ciphertext, ad) - comme dans [NTCP2](/docs/specs/ntcp2/), [ECIES-X25519](/docs/specs/ecies/), et [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Fonctions X25519 DH - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

Autres fonctions Noise définies ailleurs :

- MixHash(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

## Conception

### Framework du Protocole Noise

Cette spécification fournit les exigences basées sur le Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11). Dans la terminologie Noise, Alice est l'initiateur, et Bob est le répondeur.

Il est basé sur le protocole Noise Noise_N_25519_ChaChaPoly_SHA256. Ce protocole Noise utilise les primitives suivantes :

- Modèle de poignée de main unidirectionnelle : N - Alice ne transmet pas sa clé statique à Bob (N)
- Fonction DH : X25519 - X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748)
- Fonction de chiffrement : ChaChaPoly - AEAD_CHACHA20_POLY1305 comme spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8. Nonce de 12 octets, avec les 4 premiers octets définis à zéro. Identique à celui dans [NTCP2](/docs/specs/ntcp2/)
- Fonction de hachage : SHA256 - Hachage standard de 32 octets, déjà largement utilisé dans I2P

### Modèles de négociation

Les handshakes utilisent les modèles de handshake [Noise](https://noiseprotocol.org/noise.html).

Le mappage de lettres suivant est utilisé :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message

La demande de construction est identique au modèle Noise N. Ceci est également identique au premier message (Session Request) dans le modèle XK utilisé dans [NTCP2](/docs/specs/ntcp2/).

```
<- s
  ...
  e es p ->
```
### Chiffrement des requêtes

Les enregistrements de demande de construction sont créés par le créateur de tunnel et chiffrés de manière asymétrique pour le saut individuel. Ce chiffrement asymétrique des enregistrements de demande est actuellement ElGamal tel que défini dans [Cryptographie](/docs/specs/cryptography/) et contient une somme de contrôle SHA-256. Cette conception n'offre pas de confidentialité persistante.

La conception ECIES utilise le modèle Noise unidirectionnel "N" avec ECIES-X25519 éphémère-statique DH, avec un HKDF, et ChaCha20/Poly1305 AEAD pour la confidentialité persistante, l'intégrité et l'authentification. Alice est le demandeur de construction de tunnel. Chaque saut dans le tunnel est un Bob.

### Chiffrement des réponses

Les enregistrements de réponse de construction sont créés par le créateur des hops et chiffrés symétriquement vers le créateur. Ce chiffrement symétrique des enregistrements de réponse ElGamal utilise AES avec une somme de contrôle SHA-256 ajoutée au début. Cette conception n'offre pas de confidentialité persistante.

Les réponses ECIES utilisent ChaCha20/Poly1305 AEAD pour l'intégrité et l'authentification.

## Spécification des enregistrements longs

NOTE : Obsolète, déprécié. Utiliser le format Short Record spécifié ci-dessous.

### Enregistrements de demande de construction

Les BuildRequestRecords chiffrés font 528 octets pour ElGamal et ECIES, pour des raisons de compatibilité.

#### Enregistrement de Requête Non Chiffré

Ceci est la spécification du tunnel BuildRequestRecord pour les routers ECIES-X25519. Résumé des modifications :

- Supprimer le hachage de router inutilisé de 32 octets
- Changer le temps de requête d'heures en minutes
- Ajouter un champ d'expiration pour un temps de tunnel variable futur
- Ajouter plus d'espace pour les drapeaux
- Ajouter un mapping pour des options de construction supplémentaires
- La clé de réponse AES-256 et l'IV ne sont pas utilisés pour l'enregistrement de réponse propre au saut
- L'enregistrement non chiffré est plus long car il y a moins de surcharge de chiffrement

L'enregistrement de requête ne contient aucune clé de réponse ChaCha. Ces clés sont dérivées d'une KDF. Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non chiffrée : 464 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40-71</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel layer key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">72-103</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 tunnel IV key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">104-135</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">136-151</td><td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 reply IV</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">152</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">153-155</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">156-159</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">160-163</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">164-167</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">168-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-463</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding</td></tr>
</tbody>
</table>
Le champ flags est le même que celui défini dans [Tunnel-Creation](/docs/specs/tunnel-creation/) et contient ce qui suit :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Le bit 7 indique que le saut sera une passerelle d'entrée (IBGW). Le bit 6 indique que le saut sera un point de sortie (OBEP). Si aucun des deux bits n'est défini, le saut sera un participant intermédiaire. Les deux ne peuvent pas être définis en même temps.

L'expiration de la requête est destinée à une durée de tunnel variable future. Pour l'instant, la seule valeur prise en charge est 600 (10 minutes).

Les options de construction de tunnel sont une structure Mapping telle que définie dans [Common](/docs/specs/common-structures/). Les seules options actuellement définies concernent les paramètres de bande passante, à partir de l'API 0.9.65, voir ci-dessous pour les détails. Si la structure Mapping est vide, cela représente deux octets 0x00 0x00. La taille maximale du Mapping (y compris le champ de longueur) est de 296 octets, et la valeur maximale du champ de longueur du Mapping est de 294.

#### Enregistrement de Requête Chiffré

Tous les champs sont en big-endian sauf la clé publique éphémère qui est en little-endian.

Taille chiffrée : 528 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Construire les enregistrements de réponse

Les BuildReplyRecords chiffrés font 528 octets pour ElGamal et ECIES, par souci de compatibilité.

#### Enregistrement de Réponse Non Chiffré

Ceci est la spécification du BuildReplyRecord de tunnel pour les routeurs ECIES-X25519. Résumé des modifications :

- Ajouter un mappage pour les options de réponse de construction
- L'enregistrement non chiffré est plus long car il y a moins de surcharge de chiffrement

Les réponses ECIES sont chiffrées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non chiffrée : 512 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-510</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Les options de réponse de construction de tunnel sont une structure Mapping telle que définie dans [Common](/docs/specs/common-structures/). Les seules options actuellement définies concernent les paramètres de bande passante, depuis l'API 0.9.65, voir ci-dessous pour plus de détails. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (y compris le champ de longueur) est de 511 octets, et la valeur maximale du champ de longueur du Mapping est de 509.

L'octet de réponse est l'une des valeurs suivantes telles que définies dans [Tunnel-Creation](/docs/specs/tunnel-creation/) pour éviter l'empreinte digitale :

- 0x00 (accepter)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Enregistrement de Réponse Chiffré

Taille chiffrée : 528 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-511</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted BuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">512-527</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
Après la transition complète vers les enregistrements ECIES, les règles de padding par plages sont les mêmes que pour les enregistrements de requête.

### Chiffrement symétrique des enregistrements

Les tunnels mixtes sont autorisés et nécessaires pour la transition d'ElGamal vers ECIES. Pendant la période de transition, un nombre croissant de routeurs seront dotés de clés ECIES.

Le préprocessing de cryptographie symétrique s'exécutera de la même manière :

- "encryption" :
  - chiffrement exécuté en mode déchiffrement
  - enregistrements de requête déchiffrés de manière préventive lors du prétraitement (masquant les enregistrements de requête chiffrés)
- "decryption" :
  - chiffrement exécuté en mode chiffrement
  - enregistrements de requête chiffrés (révélant le prochain enregistrement de requête en texte clair) par les sauts participants
- ChaCha20 n'a pas de "modes", il est donc simplement exécuté trois fois :
  - une fois lors du prétraitement
  - une fois par le saut
  - une fois lors du traitement final de la réponse

Lorsque des tunnels mixtes sont utilisés, les créateurs de tunnels devront baser le chiffrement symétrique de BuildRequestRecord sur le type de chiffrement du saut actuel et du saut précédent.

Chaque hop utilisera son propre type de chiffrement pour chiffrer les BuildReplyRecords, et les autres enregistrements dans le VariableTunnelBuildMessage (VTBM).

Sur le chemin de retour, le point de terminaison (expéditeur) devra annuler le [Multiple-Encryption](https://en.wikipedia.org/wiki/Multiple_encryption), en utilisant la clé de réponse de chaque saut.

À titre d'exemple explicatif, examinons un tunnel sortant avec ECIES entouré par ElGamal :

- Expéditeur (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tous les BuildRequestRecords sont dans leur état chiffré (en utilisant ElGamal ou ECIES).

Le chiffrement AES256/CBC, lorsqu'il est utilisé, est encore utilisé pour chaque enregistrement, sans chaînage entre plusieurs enregistrements.

De même, ChaCha20 sera utilisé pour chiffrer chaque enregistrement, et non en streaming sur l'ensemble du VTBM.

Les enregistrements de requête sont prétraités par l'Expéditeur (OBGW) :

- L'enregistrement de H3 est "chiffré" en utilisant :
  - La clé de réponse de H2 (ChaCha20)
  - La clé de réponse de H1 (AES256/CBC)
- L'enregistrement de H2 est "chiffré" en utilisant :
  - La clé de réponse de H1 (AES256/CBC)
- L'enregistrement de H1 sort sans chiffrement symétrique

Seul H2 vérifie le flag de chiffrement de réponse, et voit qu'il est suivi par AES256/CBC.

Après avoir été traités par chaque saut, les enregistrements sont dans un état "déchiffré" :

- L'enregistrement de H3 est "déchiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
- L'enregistrement de H2 est "déchiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
  - La clé de réponse de H2 (ChaCha20-Poly1305)
- L'enregistrement de H1 est "déchiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
  - La clé de réponse de H2 (ChaCha20)
  - La clé de réponse de H1 (AES256/CBC)

Le créateur du tunnel, également appelé Inbound Endpoint (IBEP), post-traite la réponse :

- L'enregistrement de H3 est "chiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
- L'enregistrement de H2 est "chiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
  - La clé de réponse de H2 (ChaCha20-Poly1305)
- L'enregistrement de H1 est "chiffré" en utilisant :
  - La clé de réponse de H3 (AES256/CBC)
  - La clé de réponse de H2 (ChaCha20)
  - La clé de réponse de H1 (AES256/CBC)

### Clés d'enregistrement de requête

Ces clés sont explicitement incluses dans les ElGamal BuildRequestRecords. Pour les ECIES BuildRequestRecords, les clés de tunnel et les clés de réponse AES sont incluses, mais les clés de réponse ChaCha sont dérivées de l'échange DH. Voir [Prop156](/proposals/156/) pour les détails des clés ECIES statiques du routeur.

Ci-dessous figure une description de la façon de dériver les clés précédemment transmises dans les enregistrements de requête.

#### KDF pour ck et h initiaux

Il s'agit du [NOISE](https://noiseprotocol.org/noise.html) standard pour le motif "N" avec un nom de protocole standard.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
(31 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
// Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
h = protocol_name || 0

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by all routers.
```
#### KDF pour l'enregistrement de requête

Les créateurs de tunnel ElGamal génèrent une paire de clés X25519 éphémère pour chaque saut ECIES dans le tunnel, et utilisent le schéma ci-dessus pour chiffrer leur BuildRequestRecord. Les créateurs de tunnel ElGamal utiliseront le schéma antérieur à cette spécification pour chiffrer vers les sauts ElGamal.

Les créateurs de tunnel ECIES devront chiffrer vers la clé publique de chaque hop ElGamal en utilisant le schéma défini dans [Tunnel-Creation](/docs/specs/tunnel-creation/). Les créateurs de tunnel ECIES utiliseront le schéma ci-dessus pour chiffrer vers les hops ECIES.

Cela signifie que les sauts de tunnel ne verront que les enregistrements chiffrés de leur même type de chiffrement.

Pour les créateurs de tunnels ElGamal et ECIES, ils généreront des paires de clés X25519 éphémères uniques par saut pour chiffrer vers les sauts ECIES.

**IMPORTANT** : Les clés éphémères doivent être uniques par hop ECIES et par enregistrement de construction. L'échec à utiliser des clés uniques ouvre un vecteur d'attaque permettant aux hops complices de confirmer qu'ils sont dans le même tunnel.

```
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
hesk = GENERATE_PRIVATE()
hepk = DERIVE_PUBLIC(hesk)

// MixHash(hepk)
// || below means append
h = SHA256(h || hepk);

// up until here, can all be precalculated by each router
// for all incoming build requests

// Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
sesk = GENERATE_PRIVATE()
sepk = DERIVE_PUBLIC(sesk)

// MixHash(sepk)
h = SHA256(h || sepk);

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
// Sender performs an X25519 DH with Hop's static public key.
// Each Hop, finds the record w/ their truncated identity hash,
// and extracts the Sender's ephemeral key preceding the encrypted record.
sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
// Save for Reply Record KDF
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
plaintext = 464 byte build request record
ad = h
ciphertext = ENCRYPT(k, n, plaintext, ad)

End of "es" message pattern.

// MixHash(ciphertext)
// Save for Reply Record KDF
h = SHA256(h || ciphertext)
```
`replyKey`, `layerKey` et `layerIV` doivent toujours être inclus dans les enregistrements ElGamal, et peuvent être générés aléatoirement.

### Chiffrement des enregistrements de réponse

L'enregistrement de réponse est chiffré avec ChaCha20/Poly1305.

```
// AEAD parameters
k = chainkey from build request
n = 0
plaintext = 512 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
## Spécification d'Enregistrement Court

Cette spécification utilise deux nouveaux messages I2NP de construction de tunnel, Short Tunnel Build Message (type 25) et Outbound Tunnel Build Reply Message (type 26).

Le créateur du tunnel et tous les relais dans le tunnel créé doivent supporter ECIES-X25519, et au moins la version 0.9.51. Les relais dans le tunnel de réponse (pour une construction sortante) ou le tunnel sortant (pour une construction entrante) n'ont aucune exigence.

Les enregistrements de demande et de réponse chiffrés feront 218 octets, comparé à 528 octets pour tous les autres messages de construction.

Les enregistrements de requête en texte clair feront 154 octets, comparés à 222 octets pour les enregistrements ElGamal, et 464 octets pour les enregistrements ECIES tels que définis ci-dessus.

Les enregistrements de réponse en texte clair feront 202 octets, comparés à 496 octets pour les enregistrements ElGamal, et 512 octets pour les enregistrements ECIES tels que définis ci-dessus.

Le chiffrement de la réponse sera ChaCha20/Poly1305 pour l'enregistrement propre au saut, et ChaCha20 (PAS ChaCha20/Poly1305) pour les autres enregistrements dans le message de construction.

Les enregistrements de requête seront rendus plus petits en utilisant HKDF pour créer les clés de couche et de réponse, de sorte qu'elles ne soient pas explicitement incluses dans la requête.

### Flux des Messages

```
STBM: Short tunnel build message (type 25)
OTBRM: Outbound tunnel build reply message (type 26)

Outbound Build A-B-C
Reply through existing inbound D-E-F


                New Tunnel
         STBM      STBM      STBM
Creator ------> A ------> B ------> C ---\
                                   OBEP   \
                                          | Garlic wrapped (optional)
                                          | OTBRM
                                          | (TUNNEL delivery)
                                          | from OBEP to
                                          | creator
              Existing Tunnel             /
Creator <-------F---------E-------- D <--/
                                   IBGW



Inbound Build D-E-F
Sent through existing outbound A-B-C


              Existing Tunnel
Creator ------> A ------> B ------> C ---\
                                  OBEP    \
                                          | Garlic wrapped (optional)
                                          | STBM
                                          | (ROUTER delivery)
                                          | from creator
                New Tunnel                | to IBGW
          STBM      STBM      STBM        /
Creator <------ F <------ E <------ D <--/
                                   IBGW
```
#### Notes

L'encapsulation garlic des messages les cache de l'OBEP (pour une construction entrante) ou de l'IBGW (pour une construction sortante). Ceci est recommandé mais pas obligatoire. Si l'OBEP et l'IBGW sont le même router, ce n'est pas nécessaire.

### Enregistrements de Demande de Construction Courts

Les BuildRequestRecords chiffrés courts font 218 octets.

#### Enregistrement de Requête Courte Non Chiffré

Résumé des changements par rapport aux enregistrements longs :

- Changer la longueur non chiffrée de 464 à 154 octets
- Changer la longueur chiffrée de 528 à 218 octets
- Supprimer les clés de couche et de réponse ainsi que les IV, ils seront générés à partir d'une KDF

L'enregistrement de requête ne contient aucune clé de réponse ChaCha. Ces clés sont dérivées d'une KDF. Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non chiffrée : 154 octets.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-3</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel ID to receive messages as, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">4-7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next tunnel ID, nonzero</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">8-39</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next router identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">40</td><td style="border:1px solid var(--color-border); padding:0.6rem;">flags</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">41-42</td><td style="border:1px solid var(--color-border); padding:0.6rem;">more flags, unused, set to 0 for compatibility</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">43</td><td style="border:1px solid var(--color-border); padding:0.6rem;">layer encryption type</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">44-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request time (in minutes since the epoch, rounded down)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-51</td><td style="border:1px solid var(--color-border); padding:0.6rem;">request expiration (in seconds since creation)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">52-55</td><td style="border:1px solid var(--color-border); padding:0.6rem;">next message ID</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">56-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">tunnel build options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by flags or options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-153</td><td style="border:1px solid var(--color-border); padding:0.6rem;">random padding (see below)</td></tr>
</tbody>
</table>
Le champ flags est le même que celui défini dans [Tunnel-Creation](/docs/specs/tunnel-creation/) et contient les éléments suivants :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bit</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;" colspan="2"><em>Bit order: 76543210 (bit 7 is MSB)</em></td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">7</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages from anyone</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">6</td><td style="border:1px solid var(--color-border); padding:0.6rem;">if set, allow messages to anyone, and send the reply to the specified next hop in a Tunnel Build Reply Message</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">5-0</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Undefined, must set to 0 for compatibility with future options</td></tr>
</tbody>
</table>
Le bit 7 indique que le saut sera une passerelle d'entrée (IBGW). Le bit 6 indique que le saut sera un point de sortie (OBEP). Si aucun des deux bits n'est défini, le saut sera un participant intermédiaire. Les deux ne peuvent pas être définis en même temps.

Type de chiffrement de couche : 0 pour AES (comme dans les tunnels actuels) ; 1 pour futur (ChaCha?)

L'expiration de la requête est destinée à une durée de tunnel variable future. Pour l'instant, la seule valeur prise en charge est 600 (10 minutes).

La clé publique éphémère du créateur est une clé ECIES, big-endian. Elle est utilisée pour la KDF pour la couche IBGW et les clés et IV de réponse. Ceci n'est inclus que dans l'enregistrement en texte clair dans un message Inbound Tunnel Build. C'est requis car il n'y a pas de DH à cette couche pour l'enregistrement de construction.

Les options de construction de tunnel sont une structure Mapping telle que définie dans [Common](/docs/specs/common-structures/). Les seules options actuellement définies concernent les paramètres de bande passante, à partir de l'API 0.9.65, voir ci-dessous pour les détails. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (y compris le champ de longueur) est de 98 octets, et la valeur maximale du champ de longueur du Mapping est de 96.

#### Enregistrement de Requête Courte Chiffré

Tous les champs sont en big-endian sauf pour la clé publique éphémère qui est en little-endian.

Taille chiffrée : 218 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-15</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Hop's truncated identity hash</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">16-47</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Sender's ephemeral X25519 public key</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">48-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildRequestRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### Enregistrements de Réponse de Construction Courte

Les BuildReplyRecords chiffrés courts font 218 octets.

#### Enregistrement de Réponse Courte Non Chiffré

Résumé des modifications des enregistrements longs :

- Changer la longueur non chiffrée de 512 à 202 octets
- Changer la longueur chiffrée de 528 à 218 octets

Les réponses ECIES sont chiffrées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non chiffrée : 202 octets.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel Build Reply Options (Mapping)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-x</td><td style="border:1px solid var(--color-border); padding:0.6rem;">other data as implied by options</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">x-200</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Random padding (see below)</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Reply byte</td></tr>
</tbody>
</table>
Les options de réponse de construction de tunnel constituent une structure Mapping telle que définie dans [Common](/docs/specs/common-structures/). Les seules options actuellement définies concernent les paramètres de bande passante, depuis l'API 0.9.65, voir ci-dessous pour plus de détails. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (y compris le champ de longueur) est de 201 octets, et la valeur maximale du champ de longueur du Mapping est de 199.

L'octet de réponse est l'une des valeurs suivantes telles que définies dans [Tunnel-Creation](/docs/specs/tunnel-creation/) pour éviter l'empreinte digitale :

- 0x00 (accepter)
- 30 (TUNNEL_REJECT_BANDWIDTH)

Une valeur de réponse supplémentaire pourra être définie à l'avenir pour représenter le rejet d'options non prises en charge.

#### Enregistrement de Réponse Courte Chiffré

Taille chiffrée : 218 octets

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
<thead>
<tr>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Bytes</th>
<th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
</tr>
</thead>
<tbody>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">0-201</td><td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20 encrypted ShortBuildReplyRecord</td></tr>
<tr><td style="border:1px solid var(--color-border); padding:0.6rem;">202-217</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Poly1305 MAC</td></tr>
</tbody>
</table>
### KDF

Nous utilisons la clé de chaînage (ck) de l'état Noise après le chiffrement/déchiffrement de l'enregistrement de construction de tunnel pour dériver les clés suivantes : clé de réponse, clé de couche AES, clé IV AES et clé/tag de réponse garlic encryption pour l'OBEP.

Clés de réponse : Notez que la KDF est légèrement différente pour les sauts OBEP et non-OBEP. Contrairement aux enregistrements longs, nous ne pouvons pas utiliser la partie gauche de ck pour la clé de réponse, car ce n'est pas le dernier et elle sera utilisée plus tard. La clé de réponse est utilisée pour chiffrer la réponse de cet enregistrement en utilisant AEAD/ChaCha20/Poly1305 et ChaCha20 pour répondre aux autres enregistrements. Les deux utilisent la même clé. Le nonce est la position de l'enregistrement dans le message en commençant par 0. Voir ci-dessous pour les détails.

```
keydata = HKDF(ck, ZEROLEN, "SMTunnelReplyKey", 64)
replyKey = keydata[32:63]
ck = keydata[0:31]

AES Layer key:
keydata = HKDF(ck, ZEROLEN, "SMTunnelLayerKey", 64)
layerKey = keydata[32:63]

IV key for non-OBEP record:
ivKey = keydata[0:31]
because it's last

IV key for OBEP record:
ck = keydata[0:31]
keydata = HKDF(ck, ZEROLEN, "TunnelLayerIVKey", 64)
ivKey = keydata[32:63]
ck = keydata[0:31]

OBEP garlic reply key/tag:
keydata = HKDF(ck, ZEROLEN, "RGarlicKeyAndTag", 64)
garlicReplyKey = keydata[32:63]
garlicReplyTag = keydata[0:7]
```
Note : Le KDF pour la clé IV à l'OBEP est différent de celui pour les autres sauts, même si la réponse n'est pas chiffrée avec garlic encryption.

#### Chiffrement des enregistrements

L'enregistrement de réponse propre au saut est chiffré avec ChaCha20/Poly1305. C'est identique à la spécification d'enregistrement long ci-dessus, SAUF que 'n' est le numéro d'enregistrement 0-7, au lieu d'être toujours 0. Voir [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// AEAD parameters
k = replyKey from KDF above
n = record number 0-7
plaintext = 202 byte build reply record
ad = h from build request

ciphertext = ENCRYPT(k, n, plaintext, ad)
```
Les autres enregistrements sont chiffrés de manière itérative et symétrique à chaque saut avec ChaCha20 (PAS ChaCha20/Poly1305). Ceci diffère de la spécification d'enregistrement long ci-dessus, qui utilise AES et n'utilise pas le numéro d'enregistrement.

Le numéro d'enregistrement est placé dans l'IV à l'octet 4, car ChaCha20 utilise un IV de 12 octets avec un nonce little-endian aux octets 4-11. Voir [RFC-7539](https://tools.ietf.org/html/rfc7539).

```
// Parameters
k = replyKey from KDF above
n = record number 0-7
iv = 12 bytes, all zeros except iv[4] = n
plaintext = 218 byte encrypted record

ciphertext = ENCRYPT(k, iv, plaintext)
```
#### Garlic Encryption

L'encapsulation garlic des messages les cache de l'OBEP (pour une construction entrante) ou de l'IBGW (pour une construction sortante). Ceci est recommandé mais pas obligatoire. Si l'OBEP et l'IBGW sont le même router, ce n'est pas nécessaire.

La garlic encryption d'un message entrant Short Tunnel Build Message, par le créateur, chiffré vers l'ECIES IBGW, utilise le chiffrement Noise 'N', tel que défini dans [ECIES-ROUTERS](/docs/specs/ecies-routers/).

Le garlic encryption d'un message Outbound Tunnel Build Reply, par l'OBEP, chiffré pour le créateur, utilise des messages de session existante avec la clé de réponse garlic de 32 octets et l'étiquette de réponse garlic de 8 octets du KDF ci-dessus. Le format est tel que spécifié pour les réponses aux Database Lookups dans [I2NP](/docs/specs/i2np/), [ECIES-ROUTERS](/docs/specs/ecies-routers/), et [ECIES-X25519](/docs/specs/ecies/).

#### Chiffrement par couches

Cette spécification inclut un champ de type de chiffrement de couche dans l'enregistrement de demande de construction. Le seul chiffrement de couche actuellement pris en charge est le type 0, qui est AES. Ceci est inchangé par rapport aux spécifications précédentes, sauf que la clé de couche et la clé IV sont dérivées du KDF ci-dessus plutôt que d'être incluses dans l'enregistrement de demande de construction.

L'ajout de nouveaux types de chiffrement de couche, par exemple ChaCha20, est un sujet de recherche supplémentaire et ne fait pas actuellement partie de cette spécification.

## Notes d'implémentation

- Les anciens routers ne vérifient pas le type de chiffrement du saut et enverront des enregistrements chiffrés ElGamal. Certains routers récents contiennent des bogues et enverront divers types d'enregistrements mal formés. Les implémenteurs devraient détecter et rejeter ces enregistrements avant l'opération DH si possible, pour réduire l'utilisation du CPU.

### Enregistrements de construction

L'ordre des enregistrements de construction doit être randomisé, afin que les relais intermédiaires ne connaissent pas leur position dans le tunnel.

Le nombre minimum recommandé d'enregistrements de construction est de 4. S'il y a plus d'enregistrements de construction que de sauts, des enregistrements "factices" doivent être ajoutés, contenant des données aléatoires ou spécifiques à l'implémentation. Pour les constructions de tunnel entrant, il doit toujours y avoir un enregistrement "factice" pour le router d'origine, avec le préfixe de hash de 16 octets correct et une vraie clé éphémère X25519, sinon le saut le plus proche saura que le saut suivant est l'initiateur.

Le reste de l'enregistrement "factice" peut être des données aléatoires, ou peut être chiffré dans n'importe quel format pour que l'initiateur s'envoie des données à lui-même concernant la construction, peut-être pour réduire les exigences de stockage pour les constructions en attente.

Les initiateurs de tunnels entrants doivent utiliser une méthode pour valider que leur enregistrement "factice" n'a pas été modifié par le saut précédent, car cela peut également être utilisé pour la désanonymisation. L'initiateur peut stocker et vérifier une somme de contrôle de l'enregistrement, ou inclure la somme de contrôle dans l'enregistrement, ou utiliser une fonction de chiffrement/déchiffrement AEAD, selon l'implémentation. Si le préfixe de hachage de 16 octets ou d'autres contenus de l'enregistrement de construction ont été modifiés, le router doit rejeter le tunnel.

Les faux enregistrements pour les tunnels sortants, et les faux enregistrements supplémentaires pour les tunnels entrants, n'ont pas ces exigences et peuvent être des données complètement aléatoires, car ils ne seront jamais visibles à aucun saut. Il peut néanmoins être souhaitable pour l'initiateur de valider qu'ils n'ont pas été modifiés.

## Paramètres de bande passante des tunnels

### Aperçu

Alors que nous avons amélioré les performances du réseau au cours des dernières années avec de nouveaux protocoles, types de chiffrement et améliorations du contrôle de congestion, des applications plus rapides comme la diffusion vidéo en continu deviennent possibles. Ces applications nécessitent une bande passante élevée à chaque saut dans leurs tunnels clients.

Cependant, les routers participants n'ont aucune information sur la quantité de bande passante qu'un tunnel utilisera lorsqu'ils reçoivent un message de construction de tunnel. Ils ne peuvent qu'accepter ou rejeter un tunnel en se basant sur la bande passante totale actuellement utilisée par tous les tunnels participants et la limite de bande passante totale pour les tunnels participants.

Les routers qui font les demandes n'ont également aucune information sur la quantité de bande passante disponible à chaque saut.

De plus, les routers n'ont actuellement aucun moyen de limiter le trafic entrant sur un tunnel. Cela serait très utile en cas de surcharge ou d'attaque DDoS sur un service.

Les paramètres de bande passante tunnel dans les messages de demande et de réponse de construction de tunnel ajoutent la prise en charge de ces fonctionnalités. Voir [Prop168](/proposals/168/) pour plus de contexte. Ces paramètres sont définis depuis l'API 0.9.65, mais la prise en charge peut varier selon l'implémentation. Ils sont pris en charge pour les enregistrements de construction ECIES longs et courts.

### Options de Requête de Construction

Les trois options suivantes peuvent être définies dans le champ de mappage des options de construction de tunnel de l'enregistrement : Un router demandeur peut inclure n'importe laquelle, toutes, ou aucune.

- m := bande passante minimale requise pour ce tunnel (KBps entier positif sous forme de chaîne)
- r := bande passante demandée pour ce tunnel (KBps entier positif sous forme de chaîne)
- l := bande passante limite pour ce tunnel ; envoyé uniquement à IBGW (KBps entier positif sous forme de chaîne)

Contrainte : m <= r <= l

Le router participant devrait rejeter le tunnel si "m" est spécifié et qu'il ne peut pas fournir au moins cette quantité de bande passante.

Les options de requête sont envoyées à chaque participant dans l'enregistrement de requête de construction chiffrée correspondant, et ne sont pas visibles aux autres participants.

### Option de Construction de Réponse

L'option suivante peut être définie dans le champ de mappage des options de réponse de construction de tunnel de l'enregistrement, lorsque la réponse est ACCEPTED :

- b := bande passante disponible pour ce tunnel (entier positif en KBps sous forme de chaîne)

Contrainte : b >= m

Le router participant devrait inclure ceci si "m" ou "r" a été spécifié dans la requête de construction. La valeur devrait être au moins celle de la valeur "m" si spécifiée, mais peut être inférieure ou supérieure à la valeur "r" si spécifiée.

Le router participant devrait tenter de réserver et fournir au moins cette quantité de bande passante pour le tunnel, cependant ceci n'est pas garanti. Les routers ne peuvent pas prédire les conditions 10 minutes dans le futur, et le trafic de participation est de priorité inférieure au trafic et aux tunnels propres du router.

Les routers peuvent également sur-allouer la bande passante disponible si nécessaire, et ceci est probablement souhaitable, car d'autres sauts dans le tunnel pourraient le rejeter.

Pour ces raisons, la réponse du router participant doit être traitée comme un engagement de meilleur effort, mais pas comme une garantie.

Les options de réponse sont envoyées au router demandeur dans l'enregistrement de réponse de construction chiffrée correspondant, et ne sont pas visibles aux autres participants.

### Notes d'implémentation

Les paramètres de bande passante sont tels qu'observés au niveau des routers participants dans la couche tunnel, c'est-à-dire le nombre de messages tunnel de taille fixe de 1 Ko par seconde. Les frais généraux de transport (NTCP2 ou SSU2) ne sont pas inclus.

Cette bande passante peut être bien supérieure ou inférieure à la bande passante observée au niveau du client. Les messages de tunnel contiennent une surcharge substantielle, incluant la surcharge des couches supérieures comme le ratchet et le streaming. Les petits messages intermittents tels que les accusés de réception de streaming seront étendus à 1 Ko chacun. Cependant, la compression gzip au niveau de la couche I2CP peut réduire substantiellement la bande passante.

L'implémentation la plus simple au niveau du router demandeur consiste à utiliser les bandes passantes moyenne, minimale et/ou maximale des tunnels actuels dans le pool pour calculer les valeurs à inclure dans la requête. Des algorithmes plus complexes sont possibles et relèvent du choix de l'implémenteur.

Il n'existe actuellement aucune option I2CP ou SAM définie permettant au client d'indiquer au router la bande passante requise, et aucune nouvelle option n'est proposée ici. Des options pourront être définies ultérieurement si nécessaire.

Les implémentations peuvent utiliser la bande passante disponible ou toute autre donnée, algorithme, politique locale ou configuration locale pour calculer la valeur de bande passante retournée dans la réponse de construction.

## Références

- [Structures communes](/docs/specs/common-structures/)
- [Cryptographie](/docs/specs/cryptography/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ECIES-X25519](/docs/specs/ecies/)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)
- [I2NP](/docs/specs/i2np/)
- [Chiffrement multiple](https://en.wikipedia.org/wiki/Multiple_encryption)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop119](/proposals/119/)
- [Prop143](/proposals/143/)
- [Prop152](/proposals/152/)
- [Prop153](/proposals/153/)
- [Prop156](/proposals/156/)
- [Prop157](/proposals/157/)
- [Prop168](/proposals/168/)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [Création de tunnel](/docs/specs/tunnel-creation/)
