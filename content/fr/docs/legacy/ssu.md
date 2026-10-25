---
title: "SSU (UDP Semi-fiable Sécurisé)"
description: "Spécification du protocole de transport UDP original (obsolète, remplacé par SSU2)"
slug: "ssu"
aliases:
  - "/fr/docs/transport/ssu"
  - "/fr/docs/transport/ssu/"
  - "/fr/docs/transports/ssu"
  - "/fr/docs/transports/ssu/"
  - "/fr/docs/specs/ssu-spec"
  - "/fr/docs/specs/ssu-spec/"
  - "/fr/udp_spec"
  - "/fr/udp_spec/"
category: "Transports"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Aperçu

OBSOLÈTE - SSU a été remplacé par SSU2. Le support SSU a été supprimé d'i2pd dans la version 2.44.0 (API 0.9.56) en novembre 2022. Le support SSU a été supprimé de Java I2P dans la version 2.4.0 (API 0.9.61) en décembre 2023.

Voir la [présentation SSU](/docs/transport/ssu/) pour plus d'informations.

## Échange de clés DH {#dh}

L'échange initial de clés DH 2048 bits est décrit sur la [page des clés SSU](/docs/transport/ssu/#keys). Cet échange utilise le même nombre premier partagé que celui utilisé pour le [chiffrement ElGamal](/docs/specs/cryptography/#elgamal) d'I2P.

## En-tête de Message {#header}

Tous les datagrammes UDP commencent par un MAC (Message Authentication Code) de 16 octets et un IV (Initialization Vector) de 16 octets suivis d'une charge utile de taille variable chiffrée avec la clé appropriée. Le MAC utilisé est HMAC-MD5, tronqué à 16 octets, tandis que la clé est une clé AES256 complète de 32 octets. La construction spécifique du MAC correspond aux 16 premiers octets de :

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
où '+' signifie concaténer et '^' signifie ou-exclusif.

L'IV est généré de manière aléatoire pour chaque paquet. Le encryptedPayload est la version chiffrée du message commençant par l'octet de drapeau (chiffrer-puis-MAC). Le payloadLength utilisé dans le MAC est un entier non signé de 2 octets, gros-boutiste. Notez que protocolVersion est 0, donc l'ou-exclusif est une non-opération. Le macKey est soit la clé d'introduction ou est construit à partir de la clé DH échangée (voir les détails ci-dessous), comme spécifié pour chaque message ci-dessous.

**AVERTISSEMENT** - le HMAC-MD5-128 utilisé ici n'est pas standard, voir [détails HMAC](/docs/specs/cryptography/#udp) pour plus d'informations.

Le payload lui-même (c'est-à-dire, le message commençant par l'octet de flag) est chiffré AES256/CBC avec l'IV et la sessionKey, avec la prévention de rejeu traitée dans son corps, expliquée ci-dessous.

Le protocolVersion est un entier non signé de 2 octets, big endian, et est actuellement défini à 0. Les pairs utilisant une version de protocole différente ne pourront pas communiquer avec ce pair, bien que les versions antérieures n'utilisant pas ce drapeau le puissent.

Le OU exclusif de ((netid - 2) << 8) est utilisé pour identifier rapidement les connexions inter-réseaux. Le netid est un entier non signé de 2 octets, big endian, et est actuellement défini à 2. Depuis la version 0.9.42. Voir la proposition 147 pour plus d'informations. Comme l'ID réseau actuel est 2, ceci est une opération nulle pour le réseau actuel et est rétrocompatible. Toute connexion provenant de réseaux de test devrait avoir un ID différent et échouera à la vérification HMAC.

### Spécification HMAC

- Remplissage interne : 0x36...
- Remplissage externe : 0x5C...
- Clé : 32 octets
- Fonction de hachage : MD5, 16 octets
- Taille de bloc : 64 octets
- Taille MAC : 16 octets
- Exemples d'implémentations C :
  - hmac.h dans [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp dans [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Exemple d'implémentation Java :
  - I2PHMac.java dans [I2P](https://github.com/i2p/i2p.i2p)

### Détails de la clé de session

La clé de session de 32 octets est créée comme suit :

1. Prendre la clé DH échangée, représentée comme un tableau d'octets
   BigInteger de longueur minimale positive (complément à deux big-endian)
2. Si le bit le plus significatif est 1 (c'est-à-dire array[0] & 0x80 != 0),
   ajouter un octet 0x00 au début, comme dans la représentation
   BigInteger.toByteArray() de Java
3. Si le tableau d'octets fait 32 octets ou plus, utiliser les
   32 premiers octets (les plus significatifs)
4. Si le tableau d'octets fait moins de 32 octets, ajouter des octets 0x00
   à la fin pour étendre à 32 octets. *Très improbable - Voir note ci-dessous.*

### Détails de la clé MAC

La clé MAC de 32 octets est créée comme suit :

1. Prenez le tableau de bytes de la clé DH échangée, précédé d'un byte 0x00 si
   nécessaire, de l'étape 2 dans les Détails de la Clé de Session ci-dessus.
2. Si ce tableau de bytes est supérieur ou égal à 64 bytes, la clé MAC
   est constituée des bytes 33-64 de ce tableau de bytes.
3. Si ce tableau de bytes est inférieur à 64 bytes, la clé MAC est le Hash SHA-256
   de ce tableau de bytes. *À partir de la version 0.9.8. Voir la note ci-dessous.*

#### Note importante

Le code antérieur à la version 0.9.8 était défaillant et ne gérait pas correctement les tableaux d'octets de clés DH entre 32 et 63 octets (étapes 3 et 4 ci-dessus) et la connexion échouait. Comme ces cas n'ont jamais fonctionné, ils ont été redéfinis comme décrit ci-dessus pour la version 0.9.8, et le cas 0-32 octets a également été redéfini. Étant donné que la clé DH échangée nominale fait 256 octets, les chances que la représentation minimale soit inférieure à 64 octets sont extrêmement faibles.

### Format d'en-tête

Dans la charge utile chiffrée AES, il y a une structure commune minimale aux différents messages - un drapeau d'un octet et un horodatage d'envoi de quatre octets (secondes depuis l'époque Unix).

Le format d'en-tête est :

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
L'octet de drapeau contient les champs de bits suivants :

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Sans rekeying et options étendues, la taille de l'en-tête est de 37 octets.

### Renouvellement des clés {#rekey}

Si le flag de renouvellement de clé est défini, 64 octets de matériel de clé suivent l'horodatage.

Lors du renouvellement des clés, les 32 premiers octets du matériel de chiffrement sont alimentés dans un SHA256 pour produire la nouvelle clé MAC, et les 32 octets suivants sont alimentés dans un SHA256 pour produire la nouvelle clé de session, bien que les clés ne soient pas utilisées immédiatement. L'autre côté devrait également répondre avec le flag de renouvellement des clés activé et ce même matériel de chiffrement. Une fois que les deux côtés ont envoyé et reçu ces valeurs, les nouvelles clés devraient être utilisées et les clés précédentes supprimées. Il peut être utile de conserver brièvement les anciennes clés, pour gérer la perte et le réordonnancement des paquets.

NOTE : La regénération des clés n'est actuellement pas implémentée.

### Options étendues {#extend}

Si le flag d'options étendues est défini, une valeur de taille d'option d'un octet est ajoutée, suivie de ce nombre d'octets d'options étendues. Les options étendues ont toujours fait partie de la spécification, mais n'ont pas été implémentées jusqu'à la version 0.9.24. Lorsqu'elles sont présentes, le format d'option est spécifique au type de message. Voir la documentation des messages ci-dessous pour savoir si des options étendues sont attendues pour le message donné, et le format spécifié. Bien que les routeurs Java aient toujours reconnu le flag et la longueur des options, d'autres implémentations ne l'ont pas fait. Par conséquent, n'envoyez pas d'options étendues aux routeurs antérieurs à la version 0.9.24.

## Bourrage

Tous les messages contiennent 0 ou plusieurs octets de remplissage. Chaque message doit être complété pour respecter une limite de 16 octets, comme requis par la [couche de chiffrement AES256](/docs/specs/cryptography/#AES).

Jusqu'à la version 0.9.7, les messages n'étaient rembourrés que jusqu'à la prochaine limite de 16 octets, et les messages dont la taille n'était pas un multiple de 16 octets pouvaient potentiellement être invalides.

À partir de la version 0.9.7, les messages peuvent être complétés à n'importe quelle longueur tant que la MTU actuelle est respectée. Tous les octets de bourrage supplémentaires de 1 à 15 au-delà du dernier bloc de 16 octets ne peuvent pas être chiffrés ou déchiffrés et seront ignorés. Cependant, la longueur complète et tout le bourrage sont inclus dans le calcul du MAC.

À partir de la version 0.9.8, les messages transmis ne sont pas nécessairement un multiple de 16 octets. Le message SessionConfirmed est une exception, voir ci-dessous.

## Clés

Les signatures dans les messages SessionCreated et SessionConfirmed sont générées en utilisant la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) de la [RouterIdentity](/docs/specs/common-structures/#routeridentity) qui est distribuée hors-bande en publiant dans la base de données réseau, et la [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) associée.

Jusqu'à la version 0.9.15, l'algorithme de signature était toujours DSA, avec une signature de 40 octets.

Depuis la version 0.9.16, l'algorithme de signature peut être spécifié par un [KeyCertificate](/docs/specs/common-structures/#key-certificates) dans la [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Bob.

Les clés d'introduction et les clés de session font toutes deux 32 octets, et sont définies par la spécification des structures communes [SessionKey](/docs/specs/common-structures/#sessionkey). La clé utilisée pour le MAC et le chiffrement est spécifiée pour chaque message ci-dessous.

Les clés d'introduction sont livrées via un canal externe (la base de données réseau), où elles ont traditionnellement été identiques au Hash du router jusqu'à la version 0.9.47, mais peuvent être aléatoires à partir de la version 0.9.48.

## Notes

### IPv6

La spécification du protocole autorise à la fois les adresses IPv4 de 4 octets et les adresses IPv6 de 16 octets. SSU-over-IPv6 est pris en charge depuis la version 0.9.8. Consultez la documentation des messages individuels ci-dessous pour les détails sur la prise en charge d'IPv6.

### Horodatage {#time}

Bien que la plupart d'I2P utilise des horodatages [Date](/docs/specs/common-structures/#date) de 8 octets avec une résolution en millisecondes, SSU utilise des horodatages d'entiers non signés de 4 octets avec une résolution d'une seconde. Comme ces valeurs sont non signées, elles ne se réinitialiseront pas avant février 2106.

## Messages

Il y a 10 messages (types de charge utile) définis :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (type 0) {#sessionrequest}

Ceci est le premier message envoyé pour établir une session.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Format de message :

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 304 (IPv4) ou 320 (IPv6) octets (avant le bourrage non-mod-16)

#### Options étendues

Note : Implémenté dans la version 0.9.24.

- Longueur minimale : 3 (octet de longueur d'option + 2 octets)
- Longueur d'option : 2 minimum
- 2 octets de drapeaux :

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Notes

- Les adresses IPv4 et IPv6 sont prises en charge.
- Les données non interprétées pourraient éventuellement être utilisées à l'avenir pour des défis.

### SessionCreated (type 1) {#sessioncreated}

Ceci est la réponse à une [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Format du message :

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 368 octets (IPv4 ou IPv6) (avant le remplissage non-mod-16)

#### Notes

- Les adresses IPv4 et IPv6 sont prises en charge.
- Si l'étiquette de relais est non nulle, Bob propose d'agir comme introducteur pour
  Alice. Alice peut ensuite publier l'adresse de Bob et l'étiquette de relais dans la
  base de données réseau.
- Pour la signature, Bob doit utiliser son port externe, car c'est ce qu'Alice utilisera
  pour vérifier. Si le NAT/pare-feu de Bob a mappé son port interne vers un
  port externe différent, et que Bob n'en a pas conscience, la vérification par Alice
  échouera.
- Voir la section [Clés](#keys) ci-dessus pour les détails sur les signatures. Alice a déjà
  la clé publique de signature de Bob, provenant de la base de données réseau.
- Jusqu'à la version 0.9.15, la signature était toujours une signature DSA de 40 octets et
  le padding était toujours de 8 octets. À partir de la version 0.9.16, le type et la
  longueur de signature sont implicites selon le type de la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) dans la
  [RouterIdentity](/docs/specs/common-structures/#routeridentity) de Bob. Le padding est nécessaire pour un multiple de 16 octets.
- C'est le seul message qui utilise la clé d'introduction de l'expéditeur. Tous les autres utilisent la
  clé d'introduction du destinataire ou la clé de session établie.
- L'horodatage de signature semble inutilisé ou non vérifié dans l'implémentation
  actuelle.
- Les données non interprétées pourraient éventuellement être utilisées à l'avenir pour des défis.
- Options étendues dans l'en-tête : Non attendues, non définies.

### SessionConfirmed (type 2) {#sessionconfirmed}

Il s'agit de la réponse à un message [SessionCreated](#sessioncreated) et de la dernière étape pour établir une session. Plusieurs messages SessionConfirmed peuvent être nécessaires si l'identité du routeur doit être fragmentée.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 à F-2** (seulement si F > 1 ; actuellement inutilisé, voir les notes ci-dessous) :

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (dernier ou seul fragment) :**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 512 octets (avec signature Ed25519) ou 480 octets (avec signature DSA-SHA1) (avant le remplissage non-mod-16)

#### Notes

- Dans l'implémentation actuelle, la taille maximale de fragment est de 512 octets. Cela
  devrait être étendu pour que les signatures plus longues fonctionnent sans fragmentation.
  L'implémentation actuelle ne traite pas correctement les signatures réparties sur
  deux fragments.
- La [RouterIdentity](/docs/specs/common-structures/#routeridentity) typique fait 387 octets, donc aucune fragmentation n'est jamais
  nécessaire. Si une nouvelle cryptographie étend la taille de la RouterIdentity, le
  schéma de fragmentation doit être testé attentivement.
- Il n'y a aucun mécanisme pour demander ou livrer à nouveau les fragments manquants.
- Le champ total de fragments F doit être défini de manière identique dans tous les fragments.
- Voir la section [Keys](#keys) ci-dessus pour les détails sur les signatures DSA.
- L'horodatage de signature semble être inutilisé ou non vérifié dans l'implémentation
  actuelle.
- Puisque la signature est à la fin, le remplissage dans le dernier ou unique paquet
  doit compléter le paquet total à un multiple de 16 octets, sinon la signature ne
  sera pas déchiffrée correctement. Ceci est différent de tous les autres types de
  messages, où le remplissage est à la fin.
- Jusqu'à la version 0.9.15, la signature était toujours une signature DSA de 40 octets. À
  partir de la version 0.9.16, le type et la longueur de signature sont implicites par le type de
  la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) dans la [RouterIdentity](/docs/specs/common-structures/#routeridentity) d'Alice. Le remplissage est selon
  les besoins à un multiple de 16 octets.
- Options étendues dans l'en-tête : Non attendues, non définies.

### SessionDestroyed (type 8) {#sessiondestroyed}

Le message SessionDestroyed a été implémenté (réception uniquement) dans la version 0.8.1, et est envoyé depuis la version 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Ce message ne contient aucune donnée. Taille typique incluant l'en-tête, dans l'implémentation actuelle : 48 octets (avant le remplissage non-mod-16)

#### Notes

- Les messages de destruction reçus avec la clé d'introduction de l'expéditeur ou du destinataire seront ignorés.
- Options étendues dans l'en-tête : Non attendues, non définies.

### RelayRequest (type 3) {#relayrequest}

Ceci est le premier message envoyé d'Alice à Bob pour demander une présentation à Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Format de message :

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 96 octets (IP d'Alice non incluse) ou 112 octets (IP d'Alice de 4 octets incluse) (avant le remplissage non-mod-16)

#### Notes

- L'adresse IP n'est incluse que si elle est différente de l'adresse source et du port du paquet.
- Ce message peut être envoyé via IPv4 ou IPv6.
  Si le message est en IPv6 pour une introduction IPv4,
  ou (à partir de la version 0.9.50) en IPv4 pour une introduction IPv6,
  Alice doit inclure son adresse et son port d'introduction.
  Ceci est pris en charge à partir de la version 0.9.50.
- Si Alice inclut son adresse/port, Bob peut effectuer une validation supplémentaire
  avant de continuer.
  - Avant la version 0.9.24, Java I2P rejetait toute adresse ou port qui était
    différent de la connexion.
- Le défi n'est pas implémenté, la taille du défi est toujours zéro
- Le relais pour IPv6 est pris en charge à partir de la version 0.9.50.
- Avant la version 0.9.12, la clé d'introduction de Bob était toujours utilisée. À partir de la version
  0.9.12, la clé de session est utilisée s'il existe une session établie entre
  Alice et Bob. En pratique, il doit y avoir une session établie, car Alice
  n'obtiendra le nonce (tag d'introduction) qu'à partir du message de création de session,
  et Bob marquera le tag d'introduction comme invalide une fois la session détruite.
- Options étendues dans l'en-tête : Non attendues, non définies.

### RelayResponse (type 4) {#relayresponse}

Ceci est la réponse à une [RelayRequest](#relayrequest) et est envoyée de Bob vers Alice.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Format du message :

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 64 (Alice IPv4) ou 80 (Alice IPv6) octets (avant le remplissage non-mod-16)

#### Notes

- Ce message peut être envoyé via IPv4 ou IPv6.
- L'adresse IP/port d'Alice sont l'IP/port apparent que Bob a reçu dans la
  RelayRequest (pas nécessairement l'IP qu'Alice a inclus dans la RelayRequest),
  et peuvent être IPv4 ou IPv6. Alice ignore actuellement ces informations à la réception.
- L'adresse IP de Charlie peut être IPv4, ou, depuis la version 0.9.50, IPv6,
  car c'est l'adresse vers laquelle Alice va
  envoyer la SessionRequest après le Hole Punch.
- Le relayage pour IPv6 est pris en charge depuis la version 0.9.50.
- Avant la version 0.9.12, la clé d'intro d'Alice était toujours utilisée. Depuis la version
  0.9.12, la clé de session est utilisée s'il y a une session établie entre
  Alice et Bob.
- Options étendues dans l'en-tête : Non attendues, non définies.

### RelayIntro (type 5) {#relayintro}

Ceci est la présentation pour Alice, qui est envoyée de Bob à Charlie.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Format du message :

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 48 octets (avant le remplissage non-mod-16)

#### Notes

- Pour IPv4, l'adresse IP d'Alice fait toujours 4 octets, car Alice essaie de se connecter à Charlie via IPv4.
  Depuis la version 0.9.50, IPv6 est pris en charge, et l'adresse IP d'Alice peut faire 16 octets.
- Pour IPv4, ce message doit être envoyé via une connexion IPv4 établie,
  car c'est la seule façon pour Bob de connaître l'adresse IPv4 de Charlie à retourner à Alice dans la RelayResponse.
  Depuis la version 0.9.50, IPv6 est pris en charge, et ce message peut être envoyé via une connexion IPv6 établie.
- Depuis la version 0.9.50, toute adresse SSU publiée avec des introducers doit contenir "4" ou "6" dans l'option "caps".
- Challenge n'est pas implémenté, la taille du challenge est toujours zéro
- Options étendues dans l'en-tête : Non attendues, indéfinies.

### Données (type 6) {#data}

Ce message est utilisé pour le transport de données et l'accusé de réception.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Données :** 1 octet de flags (voir ci-dessous) ; si des ACK explicites sont inclus : 1 octet indiquant le nombre d'ACK, suivi de ce nombre de MessageIds de 4 octets étant entièrement accusés de réception ; si des champs de bits ACK sont inclus : 1 octet indiquant le nombre de champs de bits ACK, suivi de ce nombre de MessageIds de 4 octets + 1 ou plusieurs octets de champ de bits ACK (voir notes) ; Si des données étendues sont incluses : 1 octet de taille de données, suivi de ce nombre d'octets de données étendues (actuellement non interprétées) ; 1 octet indiquant le nombre de fragments (peut être zéro) ; Si non nul, ce nombre de fragments de message.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Chaque fragment contient : - messageId de 4 octets - informations de fragment de 3 octets :   - bits 23-17 : n° de fragment 0 - 127   - bit 16 : isLast (1 = vrai)   - bits 15-14 : inutilisés, définis à 0 pour compatibilité avec les utilisations futures   - bits 13-0 : taille de fragment 0 - 16383 - ce nombre d'octets de données de fragment

Format du message :

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Notes sur les champs de bits ACK

Le bitfield utilise les 7 bits de poids faible de chaque octet, le bit de poids fort spécifiant si un octet de bitfield supplémentaire suit (1 = vrai, 0 = l'octet de bitfield actuel est le dernier). Cette séquence de tableaux de 7 bits représente si un fragment a été reçu - si un bit est à 1, le fragment a été reçu. Pour clarifier, en supposant que les fragments 0, 2, 5 et 9 ont été reçus, les octets du bitfield seraient les suivants :

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Notes

- L'implémentation actuelle ajoute un nombre limité d'accusés de réception dupliqués pour les messages précédemment acquittés, si l'espace est disponible.
- Si le nombre de fragments est zéro, il s'agit d'un message d'acquittement uniquement ou de maintien de connexion.
- La fonctionnalité ECN n'est pas implémentée, et le bit n'est jamais défini.
- Dans l'implémentation actuelle, le bit de demande de réponse est défini lorsque le nombre de fragments est supérieur à zéro, et n'est pas défini lorsqu'il n'y a pas de fragments.
- Les données étendues ne sont pas implémentées et jamais présentes.
- La réception de fragments multiples est prise en charge dans toutes les versions. La transmission de fragments multiples est implémentée dans la version 0.9.16.
- Selon l'implémentation actuelle, le maximum de fragments est de 64 (numéro de fragment maximum = 63).
- Selon l'implémentation actuelle, la taille maximale de fragment est bien sûr inférieure au MTU.
- Veillez à ne pas dépasser le MTU maximum même s'il y a un grand nombre d'ACK à envoyer.
- Le protocole permet des fragments de longueur zéro mais il n'y a aucune raison de les envoyer.
- Dans SSU, les données utilisent un court en-tête I2NP de 5 octets suivi de la charge utile du message I2NP au lieu de l'en-tête I2NP standard de 16 octets. L'en-tête I2NP court ne consiste qu'en le type I2NP d'un octet et l'expiration de 4 octets en secondes. L'ID du message I2NP est utilisé comme ID de message pour le fragment. La taille I2NP est assemblée à partir des tailles de fragments. La somme de contrôle I2NP n'est pas requise car l'intégrité du message UDP est assurée par le déchiffrement.
- Les ID de messages ne sont pas des numéros de séquence et ne sont pas consécutifs. SSU ne garantit pas la livraison dans l'ordre. Bien que nous utilisions l'ID du message I2NP comme ID de message SSU, du point de vue du protocole SSU, ce sont des nombres aléatoires. En fait, puisque le routeur utilise un seul filtre de Bloom pour tous les pairs, l'ID de message doit être un nombre véritablement aléatoire.
- Parce qu'il n'y a pas de numéros de séquence, il n'y a aucun moyen d'être sûr qu'un ACK a été reçu. L'implémentation actuelle envoie régulièrement une grande quantité d'ACK dupliqués. Les ACK dupliqués ne doivent pas être considérés comme une indication de congestion.
- Notes sur le champ de bits ACK : Le récepteur d'un paquet de données ne sait pas combien de fragments sont dans le message à moins d'avoir reçu le dernier fragment. Par conséquent, le nombre d'octets de champ de bits envoyés en réponse peut être inférieur ou supérieur au nombre de fragments divisé par 7. Par exemple, si le fragment le plus élevé que le récepteur a vu est le numéro 4, un seul octet doit être envoyé, même s'il peut y avoir 13 fragments au total. Jusqu'à 10 octets (c'est-à-dire (64 / 7) + 1) peuvent être inclus pour chaque ID de message acquitté.
- Options étendues dans l'en-tête : Non attendues, non définies.

### PeerTest (type 7) {#peertest}

Voir [Test de pairs SSU](/docs/transport/ssu/#peerTesting) pour plus de détails. Note : le test de pairs IPv6 est pris en charge depuis la version 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Clé cryptographique utilisée (listée par ordre d'occurrence) : 1. Lorsque envoyé d'Alice à Bob : sessionKey Alice/Bob 2. Lorsque envoyé de Bob à Charlie : sessionKey Bob/Charlie 3. Lorsque envoyé de Charlie à Bob : sessionKey Bob/Charlie 4. Lorsque envoyé de Bob à Alice : sessionKey Alice/Bob (ou pour Bob antérieur à 0.9.52, introKey d'Alice) 5. Lorsque envoyé de Charlie à Alice : introKey d'Alice, tel que reçu dans le message PeerTest de Bob 6. Lorsque envoyé d'Alice à Charlie : introKey de Charlie, tel que reçu dans le message PeerTest de Charlie

Clé MAC utilisée (listée par ordre d'occurrence) : 1. Lors de l'envoi d'Alice vers Bob : Clé MAC Alice/Bob 2. Lors de l'envoi de Bob vers Charlie : Clé MAC Bob/Charlie 3. Lors de l'envoi de Charlie vers Bob : Clé MAC Bob/Charlie 4. Lors de l'envoi de Bob vers Alice : introKey d'Alice, telle que reçue dans le message PeerTest d'Alice 5. Lors de l'envoi de Charlie vers Alice : introKey d'Alice, telle que reçue dans le message PeerTest de Bob 6. Lors de l'envoi d'Alice vers Charlie : introKey de Charlie, telle que reçue dans le message PeerTest de Charlie

Format de message :

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Taille typique incluant l'en-tête, dans l'implémentation actuelle : 80 octets (avant le remplissage non-mod-16)

#### Notes

- Lorsqu'envoyé par Alice, la taille de l'adresse IP est 0, l'adresse IP n'est pas présente, et le port
  est 0, car Bob et Charlie n'utilisent pas les données ; le but est de déterminer
  la véritable adresse IP/port d'Alice et de l'informer ; Bob et Charlie ne se soucient pas de ce
  qu'Alice pense être son adresse.
- Lorsqu'envoyé par Bob ou Charlie, l'IP et le port sont présents, et l'adresse IP fait
  4 ou 16 octets. Les tests IPv6 sont pris en charge depuis la version 0.9.27.
- Lorsqu'envoyé par Charlie à Alice, l'IP et le port sont comme suit :
  Première fois (message 5) : IP et port demandés par Alice tels que reçus dans le message 2.
  Seconde fois (message 7) : IP et port réels d'Alice depuis lesquels le message 6 a été reçu.
- Notes IPv6 : Jusqu'à la version 0.9.26, seuls les tests d'adresses IPv4 sont pris en charge. Par conséquent, toute
  communication Alice-Bob et Alice-Charlie doit se faire via IPv4. La communication Bob-Charlie,
  cependant, peut se faire via IPv4 ou IPv6. L'adresse d'Alice, lorsque
  spécifiée dans le message PeerTest, doit faire 4 octets.
  Depuis la version 0.9.27, les tests d'adresses IPv6 sont pris en charge,
  et la communication Alice-Bob et Alice-Charlie peut se faire via IPv6,
  si Bob et Charlie indiquent leur support avec une capacité 'B' dans leur adresse IPv6 publiée.
  Voir la Proposition 126 pour les détails.
- Alice envoie la requête à Bob en utilisant une session existante sur le transport (IPv4 ou IPv6) qu'elle souhaite tester.
  Lorsque Bob reçoit une requête d'Alice via IPv4, Bob doit sélectionner un Charlie qui annonce une adresse IPv4.
  Lorsque Bob reçoit une requête d'Alice via IPv6, Bob doit sélectionner un Charlie qui annonce une adresse IPv6.
  La communication réelle Bob-Charlie peut se faire via IPv4 ou IPv6 (c'est-à-dire, indépendamment du type d'adresse d'Alice).
- Un pair doit maintenir une table des états de test actifs (nonces). À la réception d'un
  message PeerTest, rechercher le nonce dans la table. S'il est trouvé, c'est un
  test existant et vous connaissez votre rôle (Alice, Bob, ou Charlie). Sinon, si
  l'IP n'est pas présente et le port est 0, c'est un nouveau test et vous êtes Bob.
  Sinon, c'est un nouveau test et vous êtes Charlie.
- Depuis la version 0.9.15, Alice doit avoir une session établie avec Bob et utiliser
  la clé de session.
- Avant la version API 0.9.52, dans certaines implémentations, Bob répondait à Alice en utilisant
  la clé d'introduction d'Alice plutôt que la clé de session Alice/Bob, même si
  Alice et Bob ont une session établie (depuis 0.9.15).
  Depuis la version API 0.9.52, Bob utilisera correctement la clé de session dans toutes
  les implémentations, et Alice devrait rejeter un message reçu de Bob
  avec la clé d'introduction d'Alice si Bob est en version API 0.9.52 ou supérieure.
- Options étendues dans l'en-tête : Non attendues, indéfinies.

### HolePunch {#holepunch}

Un HolePunch est simplement un paquet UDP sans données. Il n'est ni authentifié ni chiffré. Il ne contient pas d'en-tête SSU, donc il n'a pas de numéro de type de message. Il est envoyé de Charlie à Alice dans le cadre de la séquence d'Introduction.

## Échantillons de datagrammes {#sampledatagrams}

### Message de données minimal

- pas de fragments, pas d'ACK, pas de NACK, etc
- Taille : 39 octets

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Message de données minimal avec charge utile

- Taille : 46+fragmentSize octets

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Références

- [Chiffrement AES](/docs/specs/cryptography/#AES)
- [Spécification des structures communes](/docs/specs/common-structures/)
- [Date](/docs/specs/common-structures/#date)
- [Chiffrement ElGamal](/docs/specs/cryptography/#elgamal)
- [Détails HMAC](/docs/specs/cryptography/#udp)
- [Source I2P](https://github.com/i2p/i2p.i2p)
- [Source i2pd](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Aperçu SSU](/docs/transport/ssu/)
- [Clés SSU](/docs/transport/ssu/#keys)
- [Test de pairs SSU](/docs/transport/ssu/#peerTesting)
