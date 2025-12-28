---
title: "Protocole Datagram2"
number: "163"
author: "zzz, orignal, drzed, eyedeekay"
created: "2023-01-24"
lastupdated: "2025-04-16"
status: "Fermé"
thread: "http://zzz.i2p/topics/3540"
target: "0.9.66"
toc: true
---

## Statut

Approuvé lors de la révision du 2025-04-15.
Changements incorporés dans les spécifications.
Implémenté dans Java I2P à partir de l'API 0.9.66.
Vérifiez la documentation de l'implémentation pour le statut.


## Vue d'ensemble

Extrait de [Prop123](/proposals/123-new-netdb-entries/) en tant que proposition distincte.

Les signatures hors ligne ne peuvent pas être vérifiées dans le traitement des datagrammes réadmettables.
Nécessite un indicateur pour indiquer une signature hors ligne mais il n'y a pas de place pour mettre un indicateur.

Nécessitera un tout nouveau numéro et format de protocole I2CP,
à ajouter à la spécification [DATAGRAMS](/docs/api/datagrams/).
Appelons-le "Datagram2".


## Objectifs

- Ajouter la prise en charge des signatures hors ligne
- Ajouter une résistance au replay
- Ajouter une saveur sans signatures
- Ajouter des champs de drapeaux et d'options pour l'extensibilité


## Non-objectifs

Soutien complet du protocole de bout en bout pour le contrôle de congestion, etc.
Cela serait construit au-dessus de, ou une alternative à, Datagram2, qui est un protocole de bas niveau.
Il n'aurait pas de sens de concevoir un protocole de haute performance uniquement sur
Datagram2, en raison du champ de provenance et du surcoût de signature.
Tout tel protocole devrait effectuer un handshake initial avec Datagram2 puis
passer à des datagrammes RAW.


## Motivation

Restant du travail sur LS2 autrement complété en 2019.

La première application à utiliser Datagram2 devrait être
les annonces UDP de bittorrent, telles qu'implémentées dans i2psnark et zzzot,
voir [Prop160](/proposals/160-udp-trackers/).


## Spécification des datagrammes réadmettables

À titre de référence,
ce qui suit est un examen de la spécification des datagrammes réadmettables,
copié de [Datagrams](/docs/api/datagrams/).
Le numéro de protocole I2CP standard pour les datagrammes réadmettables est PROTO_DATAGRAM (17).

```text
+----+----+----+----+----+----+----+----+
  | from                                  |
  +                                       +
  |                                       |
  ~                                       ~
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  |                                       |
  +----+----+----+----+----+----+----+----+
  | signature                             |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  | payload...
  +----+----+----+----//


  from :: un `Destination`
          longueur : 387+ octets
          L'initiateur et le signataire du datagramme

  signature :: une `Signature`
               Le type de signature doit correspondre au type de clé publique de signature de $from
               longueur : 40+ octets, comme impliqué par le type de Signature.
               Pour le type de clé DSA_SHA1 par défaut :
                  La `Signature` DSA du hachage SHA-256 de la charge utile.
               Pour d'autres types de clés :
                  La `Signature` de la charge utile.
               La signature peut être vérifiée par la clé publique de signature de $from

  payload ::  Les données
              Longueur : de 0 à environ 31,5 Ko (voir notes)

  Longueur totale : Longueur de la charge utile + 423+
```


## Conception

- Définir un nouveau protocole 19 - Datagramme réadmettable avec options.
- Définir un nouveau protocole 20 - Datagramme réadmettable sans signature.
- Ajouter un champ de drapeaux pour les signatures hors ligne et les extensions futures
- Déplacer la signature après la charge utile pour un traitement plus facile
- Nouvelle spécification de signature différente des datagrammes réadmettables ou streaming, pour que
  la vérification de la signature échoue si interprétée comme datagramme réadmettable ou streaming.
  Cela est accompli en déplaçant la signature après la charge utile,
  et en incluant le hachage de destination dans la fonction de signature.
- Ajouter la prévention du replay pour les datagrammes, comme cela a été fait dans [Prop164](/proposals/164-streaming/) pour le streaming.
- Ajouter une section pour les options arbitraires
- Réutiliser le format de signature hors ligne de [Common](/docs/specs/common-structures/) et [Streaming](/docs/specs/streaming/).
- La section de signature hors ligne doit être avant les sections
  de charge utile et de signature de longueur variable, car elle spécifie la longueur
  de la signature.


## Spécification

### Protocole

Le nouveau numéro de protocole I2CP pour Datagram2 est 19.
Ajoutez-le en tant que PROTO_DATAGRAM2 à [I2CP](/docs/specs/i2cp/).

Le nouveau numéro de protocole I2CP pour Datagram3 est 20.
Ajoutez-le en tant que PROTO_DATAGRAM2 à [I2CP](/docs/specs/i2cp/).


### Format Datagram2

Ajoutez Datagram2 à [DATAGRAMS](/docs/api/datagrams/) comme suit :

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            from                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~     offline_signature (optional)      ~
  ~   expires, sigtype, pubkey, offsig    ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            signature                  ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  from :: un `Destination`
          longueur : 387+ octets
          L'initiateur et (sauf signature hors ligne) signataire du datagramme

  flags :: (2 octets)
           Ordre des bits : 15 14 ... 3 2 1 0
           Bits 3-0 : Version : 0x02 (0 0 1 0)
           Bit 4 : Si 0, pas d'options; si 1, mappage des options inclus
           Bit 5 : Si 0, pas de sig. hors ligne; si 1, signé hors ligne
           Bits 15-6 : inutilisés, réglés à 0 pour compatibilité avec des usages futurs

  options :: (2+ octets si présent)
           Si le drapeau indique que des options sont présentes, un `Mapping`
           contenant des options de texte arbitraires

  offline_signature ::
               Si le drapeau indique des clés hors ligne, la section de signature hors ligne,
               comme spécifié dans la spécification des structures communes,
               avec les 4 champs suivants. Longueur : varie selon les types de sig en ligne et hors ligne, typiquement 102 octets pour Ed25519
               Cette section peut, et devrait, être générée hors ligne.

    expires :: Horodatage d'expiration
               (4 octets, big endian, secondes depuis l'époque, se réinitialise en 2106)

    sigtype :: Type de sig. transitoire (2 octets, big endian)

    pubkey :: Clé publique de signature transitoire (longueur selon le type de sig),
              typiquement 32 octets pour le type de sig Ed25519.

    offsig :: une `Signature`
              Signature du timestamp d'expiration, du type de sig transitoire,
              et clé publique, par la clé publique de destination,
              longueur : 40+ octets, comme impliqué par le type de Signature, typiquement
              64 octets pour le type de sig Ed25519.

  payload ::  Les données
              Longueur : de 0 à environ 61 Ko (voir notes)

  signature :: une `Signature`
               Le type de signature doit correspondre au type de clé publique de signature de $from
               (si pas de signature hors ligne) ou le type de sig transitoire
               (si signé hors ligne)
               longueur : 40+ octets, comme impliqué par le type de Signature, typiquement
               64 octets pour le type de sig Ed25519.
               La `Signature` de la charge utile et d'autres champs comme spécifié ci-dessous.
               La signature est vérifiée par la clé publique de signature de $from
               (si pas de signature hors ligne) ou la clé publique transitoire
               (si signé hors ligne)

```

Longueur totale : minimum 433 + longueur de charge utile;
longueur typique pour les expéditeurs X25519 et sans signatures hors ligne :
457 + longueur de charge utile.
Notez que le message sera généralement compressé avec gzip à la couche I2CP,
ce qui entraînera des économies significatives si la destination from est compressible.

Note : Le format de signature hors ligne est le même que dans la spécification des structures communes [Common](/docs/specs/common-structures/) et [Streaming](/docs/specs/streaming/).

### Signatures

La signature couvre les champs suivants.

- Préambule : Le hachage de 32 octets de la destination cible (non inclus dans le datagramme)
- flags
- options (si présentes)
- offline_signature (si présente)
- payload

Dans le datagramme réadmettable, pour le type de clé DSA_SHA1, la signature portait sur le
hachage SHA-256 de la charge utile, pas sur la charge utile elle-même; ici, la signature couvre
toujours les champs ci-dessus (PAS le hachage), quel que soit le type de clé.


### Vérification de ToHash

Les récepteurs doivent vérifier la signature (en utilisant leur hachage de destination)
et rejeter le datagramme en cas d'échec, pour la prévention du replay.


### Format Datagram3

Ajoutez Datagram3 à [DATAGRAMS](/docs/api/datagrams/) comme suit :

```text
+----+----+----+----+----+----+----+----+
  |                                       |
  ~            fromhash                   ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  flags  |     options (optional)      |
  +----+----+                             +
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  ~            payload                    ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  fromhash :: un `Hash`
              longueur : 32 octets
              L'initiateur du datagramme

  flags :: (2 octets)
           Ordre des bits : 15 14 ... 3 2 1 0
           Bits 3-0 : Version : 0x03 (0 0 1 1)
           Bit 4 : Si 0, pas d'options; si 1, mappage des options inclus
           Bits 15-5 : inutilisés, réglés à 0 pour compatibilité avec des usages futurs

  options :: (2+ octets si présent)
           Si le drapeau indique que des options sont présentes, un `Mapping`
           contenant des options de texte arbitraires

  payload ::  Les données
              Longueur : de 0 à environ 61 Ko (voir notes)

```

Longueur totale : minimum 34 + longueur de charge utile.


### SAM

Ajoutez STYLE=DATAGRAM2 et STYLE=DATAGRAM3 à la spécification SAMv3.
Mettez à jour les informations sur les signatures hors ligne.


### Surcoût

Cette conception ajoute 2 octets de surcoût aux datagrammes réadmettables pour les drapeaux.
Cela est acceptable.


## Analyse de sécurité

Inclure le hachage cible dans la signature devrait être efficace pour prévenir les attaques de replay.

Le format Datagram3 n'a pas de signatures, donc l'expéditeur ne peut pas être vérifié,
et les attaques de replay sont possibles. Toute validation requise doit être effectuée au niveau de l'application,
ou par le routeur au niveau de la gestion des clés.


## Notes

- La longueur pratique est limitée par les couches inférieures de protocoles - la spécification des
  messages de tunnel [TUNMSG](/docs/specs/tunnel-message/#notes) limite les messages à environ 61,2 Ko et les transports
  [TRANSPORT](/docs/transport/) limitent actuellement les messages à environ 64 Ko, donc la longueur des données ici
  est limitée à environ 61 Ko.
- Voir les notes importantes sur la fiabilité des grands datagrammes [API](/docs/api/datagrams/). Pour
  de meilleurs résultats, limitez la charge utile à environ 10 Ko ou moins.


## Compatibilité

Aucune. Les applications doivent être réécrites pour acheminer les messages I2CP Datagram2
basés sur le protocole et/ou le port.
Les messages Datagram2 qui sont mal acheminés et interprétés comme
des messages de datagrammes réadmettables ou streaming échoueront basés sur la signature, le format, ou les deux.


## Migration

Chaque application UDP doit détecter séparément la prise en charge et migrer.
L'application UDP la plus en vue est bittorrent.

### Bittorrent

Bittorrent DHT : Probablement besoin d'un drapeau d'extension,
par exemple i2p_dg2, coordonner avec BiglyBT

Annonces UDP pour Bittorrent [Prop160](/proposals/160-udp-trackers/): Conception dès le début.
Coordonner avec BiglyBT, i2psnark, zzzot

### Autres

Bote : Peu probable qu'il migre, pas activement maintenu

Streamr : Personne ne l'utilise, aucune migration prévue

Applications SAM UDP : Aucune connue


## Références

* [API](/docs/api/datagrams/)
* [BT-SPEC](/docs/applications/bittorrent/)
* [Common](/docs/specs/common-structures/)
* [DATAGRAMS](/docs/api/datagrams/)
* [I2CP](/docs/specs/i2cp/)
* [Prop123](/proposals/123-new-netdb-entries/)
* [Prop160](/proposals/160-udp-trackers/)
* [Prop164](/proposals/164-streaming/)
* [Streaming](/docs/specs/streaming/)
* [TRANSPORT](/docs/transport/)
* [TUNMSG](/docs/specs/tunnel-message/#notes)
