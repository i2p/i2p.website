---
title: "Spécification I2NP"
description: "Formats de messages, priorités et structures communes du protocole réseau I2P (I2NP) pour la communication entre routeurs."
slug: "i2np"
aliases:
  - "/fr/spec/i2np"
  - "/fr/spec/i2np/"
category: "Protocoles"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Aperçu

Le protocole réseau I2P (I2NP) est la couche située au-dessus des protocoles de transport I2P. C'est un protocole de router à router. Il est utilisé pour les recherches et réponses dans la base de données réseau, pour créer des tunnels, et pour les messages de données chiffrés du router et du client. Les messages I2NP peuvent être envoyés point-à-point vers un autre router, ou envoyés de manière anonyme à travers des tunnels vers ce router.

## Versions du protocole {#versions}

Tous les routeurs doivent publier leur version du protocole I2NP dans le champ "router.version" des propriétés RouterInfo. Ce champ de version correspond à la version de l'API, indiquant le niveau de prise en charge des diverses fonctionnalités du protocole I2NP, et ne correspond pas nécessairement à la version réelle du routeur.

Si les routers alternatifs (non-Java) souhaitent publier des informations de version sur l'implémentation réelle du router, ils doivent le faire dans une autre propriété. Les versions autres que celles listées ci-dessous sont autorisées. Le support sera déterminé par une comparaison numérique ; par exemple, 0.9.13 implique le support des fonctionnalités 0.9.12. Notez que la propriété "coreVersion" n'est plus publiée dans les informations du router, et n'a jamais été utilisée pour déterminer la version du protocole I2NP.

Un résumé de base des versions du protocole I2NP est le suivant. Pour plus de détails, voir ci-dessous.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Notez qu'il existe également des fonctionnalités et des problèmes de compatibilité liés au transport ; consultez la documentation des transports NTCP et SSU pour plus de détails.

## Structures communes {#structures}

Les structures suivantes sont des éléments de plusieurs messages I2NP. Ce ne sont pas des messages complets.

### En-tête de message I2NP {#struct-I2NPMessageHeader}

#### Description

En-tête commun à tous les messages I2NP, qui contient des informations importantes comme une somme de contrôle, une date d'expiration, etc.

#### Sommaire

Il existe trois formats distincts utilisés, selon le contexte ; un format standard et deux formats courts.

Le format standard de 16 octets contient 1 octet [Integer](/docs/specs/common-structures/#integer) spécifiant le type de ce message, suivi d'un [Integer](/docs/specs/common-structures/#integer) de 4 octets spécifiant l'identifiant du message. Après cela, il y a une [Date](/docs/specs/common-structures/#date) d'expiration, suivie d'un [Integer](/docs/specs/common-structures/#integer) de 2 octets spécifiant la longueur de la charge utile du message, suivi d'un [Hash](/docs/specs/common-structures/#hash), qui est tronqué au premier octet. Après cela suivent les données réelles du message.

Les formats courts utilisent une expiration de 4 octets en secondes au lieu d'une expiration de 8 octets en millisecondes. Les formats courts ne contiennent pas de somme de contrôle ou de taille, celles-ci sont fournies par les encapsulations, selon le contexte.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Notes

- Lorsqu'il est transmis via [SSU](/docs/transports/ssu/), l'en-tête standard de 16 octets n'est pas utilisé. Seuls un type de 1 octet et une expiration de 4 octets en secondes sont inclus. L'identifiant de message et la taille sont incorporés dans le format de paquet de données SSU. La somme de contrôle n'est pas requise car les erreurs sont détectées lors du déchiffrement.

- Lors de la transmission via [NTCP2](/docs/specs/ntcp2/) ou [SSU2](/docs/specs/ssu2/), l'en-tête standard de 16 octets n'est pas utilisé. Seuls un type d'1 octet, un identifiant de message de 4 octets, et une expiration de 4 octets en secondes sont inclus. La taille est incorporée dans les formats de paquet de données NTCP2 et SSU2. La somme de contrôle n'est pas requise car les erreurs sont détectées lors du déchiffrement.

- L'en-tête standard est également requis pour les messages I2NP contenus dans d'autres messages et structures (Data, TunnelData, TunnelGateway, et GarlicClove). Depuis la version 0.8.12, pour réduire la surcharge, la vérification de la somme de contrôle est désactivée à certains endroits dans la pile de protocole. Cependant, pour la compatibilité avec les versions plus anciennes, la génération de la somme de contrôle est toujours requise. C'est un sujet de recherche future que de déterminer les points dans la pile de protocole où la version du router distant est connue et où la génération de la somme de contrôle peut être désactivée.

- L'expiration courte n'est pas signée et bouclera le 7 février 2106. À partir de cette date, un décalage devra être ajouté pour obtenir l'heure correcte.

- Les implémentations peuvent rejeter les messages avec des expirations trop lointaines dans le futur. L'expiration maximale recommandée est de 60s dans le futur.

### BuildRequestRecord {#struct-BuildRequestRecord}

OBSOLÈTE, utilisé uniquement dans le réseau actuel lorsqu'un tunnel contient un router ElGamal. Voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Description

Un enregistrement dans un ensemble de plusieurs enregistrements pour demander la création d'un saut dans le tunnel. Pour plus de détails, voir la [vue d'ensemble des tunnels](/docs/specs/tunnel-implementation/) et la [spécification de création de tunnel ElGamal](/docs/specs/tunnel-creation/).

Pour les BuildRequestRecords ECIES-X25519, voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Sommaire (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) pour recevoir les messages, suivi du [Hash](/docs/specs/common-structures/#hash) de notre [RouterIdentity](/docs/specs/common-structures/#routeridentity). Après cela suivent le [TunnelId](/docs/specs/common-structures/#tunnelid) et le [Hash](/docs/specs/common-structures/#hash) de la [RouterIdentity](/docs/specs/common-structures/#routeridentity) du router suivant.

Chiffré avec ElGamal et AES :

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
Chiffré ElGamal :

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Texte en clair :

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Notes

- Dans l'enregistrement chiffré de 512 octets, les données ElGamal contiennent les octets 1-256 et 258-513 du bloc chiffré ElGamal de 514 octets [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Les deux octets de remplissage du bloc (les octets zéro aux emplacements 0 et 257) sont supprimés.

- Voir la [spécification de création de tunnel](/docs/specs/tunnel-creation/) pour les détails sur le contenu des champs.

### BuildResponseRecord {#struct-BuildResponseRecord}

OBSOLÈTE, utilisé uniquement dans le réseau actuel lorsqu'un tunnel contient un router ElGamal. Voir [Création de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Description

Un enregistrement dans un ensemble de plusieurs enregistrements avec des réponses à une demande de construction. Pour plus de détails, voir l'[aperçu des tunnels](/docs/specs/tunnel-implementation/) et la [spécification de création de tunnel ElGamal](/docs/specs/tunnel-creation/).

Pour les BuildResponseRecords ECIES-X25519, voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

#### Sommaire (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Notes

- Le champ de données aléatoires pourrait, à l'avenir, être utilisé pour renvoyer des informations de congestion ou de connectivité des pairs au demandeur.

- Voir la [spécification de création de tunnel](/docs/specs/tunnel-creation/) pour plus de détails sur le champ de réponse.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Pour les routeurs ECIES-X25519 uniquement, à partir de la version API 0.9.51. 218 octets lorsque chiffré. Voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Pour les routers ECIES-X25519 uniquement, à partir de la version API 0.9.51. 218 octets lorsque chiffré. Voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Avertissement : Ceci est le format utilisé pour les segments de garlic encryption dans les messages garlic encryption chiffrés avec ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Le format pour les messages garlic encryption et segments garlic encryption ECIES-AEAD-X25519-Ratchet est significativement différent ; voir [ECIES](/docs/specs/ecies/) pour la spécification.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Notes

- Les cloves ne sont jamais fragmentés. Lorsqu'ils sont utilisés dans un Garlic Clove, le premier bit de l'octet de flag des Instructions de Livraison spécifie le chiffrement. Si ce bit est 0, le clove n'est pas chiffré. Si c'est 1, le clove est chiffré, et une Clé de Session de 32 octets suit immédiatement l'octet de flag. Le chiffrement de clove n'est pas entièrement implémenté.

- Voir aussi la [spécification du routage en ail](/docs/overview/garlic-routing/).

- La longueur maximale est une fonction de la longueur totale de tous les cloves et de la longueur maximale du GarlicMessage.

- À l'avenir, le certificat pourrait éventuellement être utilisé pour un HashCash afin de "payer" pour le routage.

- Le message peut être n'importe quel message I2NP (y compris un GarlicMessage, bien que cela ne soit pas utilisé en pratique). Les messages utilisés en pratique sont DataMessage, DeliveryStatusMessage, et DatabaseStoreMessage.

- L'ID Clove est généralement défini sur un nombre aléatoire lors de la transmission et est vérifié pour les doublons lors de la réception (même espace d'ID de message que les ID de Message de niveau supérieur)

### Instructions de livraison de gousse Garlic {#struct-GarlicCloveDeliveryInstructions}

Il s'agit du format utilisé pour les clous garlic chiffrés à la fois avec ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) et avec ECIES-AEAD-X25519-Ratchet [ECIES](/docs/specs/ecies/).

Cette spécification concerne uniquement les Instructions de Livraison à l'intérieur des Garlic Cloves. Notez que les "Instructions de Livraison" sont également utilisées à l'intérieur des Messages de Tunnel, où le format est significativement différent. Consultez la [documentation des Messages de Tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) pour plus de détails. N'utilisez PAS la spécification suivante pour les Instructions de Livraison des Messages de Tunnel !

La clé de session et le délai ne sont pas utilisés et jamais présents, donc les trois longueurs possibles sont 1 (LOCAL), 33 (ROUTER et DESTINATION), et 37 (TUNNEL) octets.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Messages

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Description

Un stockage de base de données non sollicité, ou la réponse à un message [DatabaseLookup](#msg-DatabaseLookup) réussi

#### Sommaire

Un LeaseSet, LeaseSet2, MetaLeaseSet ou EncryptedLeaseset non compressé, ou un RouterInfo compressé

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Notes

- Pour des raisons de sécurité, les champs de réponse sont ignorés si le message est reçu via un tunnel.

- La clé est le hash "réel" du RouterIdentity ou de la Destination, PAS la clé de routage.

- Les types 3, 5, et 7 sont disponibles depuis la version 0.9.38. Voir la proposition 123 pour plus d'informations. Ces types ne doivent être envoyés qu'aux routers avec la version 0.9.38 ou supérieure.

- Comme optimisation pour réduire les connexions, si le type est un LeaseSet, que le jeton de réponse est inclus, que l'ID du tunnel de réponse est non nul, et que la paire passerelle de réponse/ID de tunnel est trouvée dans le LeaseSet comme un bail, le destinataire peut rediriger la réponse vers tout autre bail dans le LeaseSet.

- Pour masquer l'OS du router et l'implémentation, faire correspondre l'implémentation du router Java de gzip en définissant le temps de modification à 0 et l'octet OS à 0xFF, et définir XFL à 0x02 (compression maximale, algorithme le plus lent). Voir RFC 1952. Les 10 premiers octets des informations de router compressées seront (hex) : 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Description

Une demande de recherche d'un élément dans la base de données réseau. La réponse est soit un [DatabaseStore](#msg-DatabaseStore) soit un [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Sommaire

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Chiffrement des réponses

NOTE : Les routers ElGamal sont dépréciés depuis l'API 0.9.58. Comme la version minimale recommandée de floodfill à interroger est maintenant 0.9.58, les implémentations n'ont plus besoin d'implémenter le chiffrement pour les routers floodfill ElGamal. Les destinations ElGamal sont toujours supportées.

Le bit de flag 4 est utilisé en combinaison avec le bit 1 pour déterminer le mode de chiffrement de réponse. Le bit de flag 4 ne doit être défini que lors de l'envoi vers des routers avec la version 0.9.46 ou supérieure. Voir les propositions 154 et 156 pour plus de détails.

Dans le tableau ci-dessous, "DH n/a" signifie que la réponse n'est pas chiffrée. "DH no" signifie que les clés de réponse sont incluses dans la requête. "DH yes" signifie que les clés de réponse sont dérivées de l'opération DH.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Aucun chiffrement

reply_key, tags, et reply_tags ne sont pas présents.

#### ElG vers ElG

Pris en charge à partir de la version 0.9.7. Obsolète à partir de la version 0.9.58. La destination ElG envoie une recherche à un router ElG.

Génération de clé du demandeur :

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Format du message :

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES vers ElG

Pris en charge depuis la version 0.9.46. Déprécié depuis la version 0.9.58. Une destination ECIES envoie une requête à un router ElG. Les champs reply_key et reply_tags sont redéfinis pour une réponse chiffrée ECIES.

Génération de clé du demandeur :

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Format de message : Redéfinir les champs reply_key et reply_tags comme suit :

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
La réponse est un message ECIES Existing Session, tel que défini dans [ECIES](/docs/specs/ecies/).

#### Format de réponse

Il s'agit du message de session existant, identique à celui dans [ECIES](/docs/specs/ecies/), copié ci-dessous pour référence.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Paramètres AEAD :

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES vers ECIES (0.9.49)

Une destination ECIES ou un router envoie une requête de recherche à un router ECIES. Pris en charge depuis la version 0.9.49.

Les routers ECIES ont été introduits dans la version 0.9.48, voir [Proposition 156](/proposals/156/). Les destinations et routers ECIES peuvent utiliser le même format que dans la section "ECIES vers ElG" ci-dessus, avec les clés de réponse incluses dans la requête. Le chiffrement des messages de recherche est spécifié dans [ECIES-ROUTERS](/docs/specs/ecies-routers/). Le demandeur est anonyme.

#### ECIES vers ECIES (futur)

Cette option n'est pas encore entièrement définie. Voir [Proposition 156](/proposals/156/).

#### Notes

- Avant la version 0.9.16, la clé peut être pour un RouterInfo ou un LeaseSet, car ils sont dans le même espace de clés, et il n'y avait pas d'indicateur pour demander seulement un type particulier de données.

- Flag de chiffrement, clé de réponse, et tags de réponse depuis la version 0.9.7.

- Les réponses chiffrées ne sont utiles que lorsque la réponse transite par un tunnel.

- Le nombre d'étiquettes incluses pourrait être supérieur à un si des stratégies alternatives de recherche DHT (par exemple, les recherches récursives) sont implémentées.

- Les clés de recherche et les clés d'exclusion sont les hachages "réels", PAS les clés de routage.

- Les types 3, 5 et 7 peuvent être retournés à partir de la version 0.9.38. Voir la proposition 123 pour plus d'informations.

- Notes sur la recherche exploratoire : Une recherche exploratoire est définie pour retourner une liste de hachages non-floodfill proches de la clé. Cependant, voir les notes importantes pour DatabaseSearchReply concernant les variantes d'implémentation. De plus, cette spécification n'a jamais clairement indiqué si le récepteur devrait rechercher la clé de recherche pour un RI et retourner un DatabaseStore au lieu d'un DSRM s'il est présent. Java effectue la recherche ; i2pd ne le fait pas. Par conséquent, il n'est pas recommandé d'utiliser une recherche exploratoire pour des hachages précédemment reçus.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Description

La réponse à un message [DatabaseLookup](#msg-DatabaseLookup) échoué

#### Sommaire

Une liste de hachages de router les plus proches de la clé demandée

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Notes

- Le hash 'from' n'est pas authentifié et ne peut pas être considéré comme fiable.

- Les hachages de pairs renvoyés ne sont pas nécessairement plus proches de la clé que le router interrogé. Pour les réponses aux recherches régulières, cela facilite la découverte de nouveaux floodfills et la recherche "à rebours" (plus éloignée de la clé) pour la robustesse.

- La clé pour une recherche d'exploration est généralement générée de manière aléatoire. Par conséquent, les peer_hashes non-floodfill de la réponse peuvent être sélectionnés en utilisant un algorithme optimisé, tel que fournir des pairs qui sont proches de la clé mais pas nécessairement les plus proches dans l'ensemble de la base de données réseau locale, pour éviter un tri ou une recherche inefficace de toute la base de données locale. D'autres stratégies telles que la mise en cache peuvent également être appropriées. Ceci dépend de l'implémentation.

- Nombre typique de hashes retournés : 3

- Nombre maximum recommandé de hachages à retourner : 16

- La clé de recherche, les hachages des pairs et le hachage source sont des hachages "réels", PAS des clés de routage.

### DeliveryStatus {#msg-DeliveryStatus}

#### Description

Un simple accusé de réception de message. Généralement créé par l'expéditeur du message, et encapsulé dans un Garlic Message avec le message lui-même, pour être retourné par la destination.

Ce message est également utilisé pour le test des tunnels, où l'initiateur l'envoie à travers un tunnel sortant, vers un tunnel entrant, puis de retour à lui-même. Dans ce cas également, il est généralement encapsulé dans du garlic encryption. Le test des tunnels est requis à partir de la version 0.9.68 de l'API (2026-02), car les routeurs sont autorisés à abandonner les tunnels participants n'ayant reçu aucun trafic après les deux premières minutes.

#### Sommaire

L'ID du message livré, ainsi que l'heure de création ou d'arrivée.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Notes

- Il semble que l'horodatage soit toujours défini par le créateur à l'heure actuelle. Cependant, il y a plusieurs utilisations de ceci dans le code, et d'autres pourraient être ajoutées à l'avenir.

- Ce message est également utilisé comme confirmation d'établissement de session dans SSU [SSU-ED](/docs/transports/ssu/#establishDirect). Dans ce cas, l'ID du message est défini sur un nombre aléatoire, et le "temps d'arrivée" est défini sur l'ID réseau actuel, qui est 2 (c'est-à-dire 0x0000000000000002).

### Garlic {#msg-Garlic}

Avertissement : Ceci est le format utilisé pour les messages épelés chiffrés avec ElGamal [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Le format pour les messages épelés utilisant ECIES-AEAD-X25519-Ratchet ainsi que pour les clous d'ail est sensiblement différent ; voir [ECIES](/docs/specs/ecies/) pour la spécification.

#### Description

Utilisé pour encapsuler plusieurs messages I2NP chiffrés

#### Sommaire

Une fois déchiffré, une série de [Garlic Cloves](#struct-GarlicClove) et des données supplémentaires, également appelée un ensemble de Clove (Clove Set).

Chiffré :

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Données déchiffrées, également appelées ensemble Clove (Clove Set) :

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Notes

- Lorsque non chiffrées, les données contiennent un ou plusieurs [Garlic Cloves](#struct-GarlicClove).

- Le bloc chiffré AES est complété à un minimum de 128 octets ; avec le Session Tag de 32 octets, la taille minimale du message chiffré est de 160 octets ; avec les 4 octets de longueur, la taille minimale du Garlic Message est de 164 octets.

- La longueur maximale réelle est inférieure à 64 Ko ; voir [I2NP](/docs/protocol/i2np/).

- Voir aussi la [spécification ElGamal/AES](/docs/specs/elgamal-aes/).

- Voir également la [spécification du routage garlic](/docs/overview/garlic-routing/).

- La taille minimum de 128 octets du bloc chiffré AES n'est actuellement pas configurable, cependant la taille minimum d'un DataMessage dans un GarlicClove dans un GarlicMessage, avec les en-têtes, est de toute façon de 128 octets. Une option configurable pour augmenter la taille minimum pourrait être ajoutée dans le futur.

- L'ID du message est généralement défini sur un nombre aléatoire lors de la transmission et semble être ignoré lors de la réception.

- À l'avenir, le certificat pourrait éventuellement être utilisé pour un HashCash afin de « payer » pour le routage.

### TunnelData {#msg-TunnelData}

#### Description

Un message envoyé depuis la passerelle ou un participant d'un tunnel vers le participant suivant ou le point de terminaison. Les données ont une longueur fixe et contiennent des messages I2NP fragmentés, regroupés, complétés et chiffrés.

#### Sommaire

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Remarques

- L'ID de message I2NP pour ce message est défini à un nouveau nombre aléatoire à chaque saut.

- Voir également la [Spécification des Messages de Tunnel](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Description

Encapsule un autre message I2NP à envoyer dans un tunnel à la passerelle entrante du tunnel.

#### Sommaire

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notes

- La charge utile est un message I2NP avec un en-tête standard de 16 octets.

### Données {#msg-Data}

#### Description

Utilisé par les messages Garlic et les gousses Garlic pour encapsuler des données arbitraires.

#### Sommaire

Un entier de longueur, suivi de données opaques.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notes

- Ce message ne contient aucune information de routage et ne sera jamais envoyé "non encapsulé". Il n'est utilisé que dans les messages `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

OBSOLÈTE, utiliser [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Notes

- À partir de la version 0.9.48, peut également contenir des BuildRequestRecords ECIES-X25519, voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- Voir aussi la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

- L'ID de message I2NP pour ce message doit être défini selon la spécification de création de tunnel.

- Bien que ce message soit rarement vu dans le réseau actuel, ayant été remplacé par le message `VariableTunnelBuild`, il peut encore être utilisé pour de très longs tunnels, et n'a pas été déprécié. Les routeurs doivent l'implémenter.

### TunnelBuildReply {#msg-TunnelBuildReply}

OBSOLÈTE, utiliser [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Notes

- À partir de la version 0.9.48, peut également contenir des BuildResponseRecords ECIES-X25519, voir [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Voir également la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

- L'ID du message I2NP pour ce message doit être défini selon la spécification de création de tunnel.

- Bien que ce message soit rarement vu dans le réseau actuel, ayant été remplacé par le message `VariableTunnelBuildReply`, il peut encore être utilisé pour des tunnels très longs, et n'a pas été déprécié. Les routers doivent l'implémenter.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Notes

- À partir de la version 0.9.48, peut également contenir des BuildRequestRecords ECIES-X25519, voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- Ce message a été introduit dans la version 0.7.12 du router, et ne peut pas être envoyé aux participants de tunnel antérieurs à cette version.

- Voir aussi la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

- L'ID de message I2NP pour ce message doit être défini selon la spécification de création de tunnel.

- Le nombre typique d'enregistrements dans le réseau actuel est de 4, pour une taille totale de 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Notes

- À partir de la version 0.9.48, peut également contenir des BuildResponseRecords ECIES-X25519, voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- Ce message a été introduit dans la version 0.7.12 du router, et peut ne pas être envoyé aux participants de tunnel antérieurs à cette version.

- Voir aussi la [spécification de création de tunnel](/docs/specs/tunnel-creation/).

- L'ID de message I2NP pour ce message doit être défini selon la spécification de création de tunnel.

- Le nombre typique d'enregistrements dans le réseau actuel est de 4, pour une taille totale de 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Description

À partir de la version d'API 0.9.51, uniquement pour les routeurs ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Notes

- À partir de la version 0.9.51. Voir [Création de tunnel ECIES](/docs/specs/tunnel-creation-ecies/).

- Ce message a été introduit dans la version 0.9.51 du router, et ne peut pas être envoyé aux participants de tunnel antérieurs à cette version.

- Le nombre typique d'enregistrements dans le réseau actuel est de 4, pour une taille totale de 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Description

Envoyé depuis le point de terminaison sortant d'un nouveau tunnel vers l'initiateur. À partir de la version 0.9.51 de l'API, uniquement pour les routeurs ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Notes

- Depuis la version 0.9.51. Voir [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Le nombre typique d'enregistrements dans le réseau actuel est de 4, pour une taille totale de 873.

## Références

- **[CRYPTO-ELG]** [Cryptographie - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Structures Communes - Date](/docs/specs/common-structures/#date)
- **[ECIES]** [Spécification ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Spécification des Routeurs ECIES](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Routage Garlic](/docs/overview/garlic-routing/)
- **[Hash]** [Structures Communes - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [Protocole I2NP](/docs/protocol/i2np/)
- **[Integer]** [Structures Communes - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Spécification NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Proposition 156](/proposals/156/)
- **[Prop157]** [Proposition 157](/proposals/157/)
- **[RouterIdentity]** [Structures Communes - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [Transport SSU](/docs/transports/ssu/)
- **[SSU-ED]** [Transport SSU - Establish Direct](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Spécification SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Instructions de Livraison des Messages Tunnel](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Spécification de Création de Tunnel](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Création de Tunnel ECIES](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Implémentation des Tunnels](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Spécification des Messages Tunnel](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Structures Communes - TunnelId](/docs/specs/common-structures/#tunnelid)
