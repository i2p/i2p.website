---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, orignal"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Remarque

Déploiement réseau et tests en cours. Sujet à des révisions mineures. Voir [SPEC](/docs/specs/ecies/) pour la spécification officielle.

Les fonctionnalités suivantes ne sont pas implémentées à partir de la version 0.9.46 :

- Blocs MessageNumbers, Options et Termination
- Réponses de couche protocole
- Clé statique zéro
- Multidiffusion

## Aperçu

Il s'agit d'une proposition pour le premier nouveau type de chiffrement de bout en bout depuis le début d'I2P, pour remplacer ElGamal/AES+SessionTags [Elg-AES](/docs/legacy/elgamal-aes/).

Il s'appuie sur les travaux antérieurs suivants :

- Spécification des structures communes [Common Structures](/docs/specs/common-structures/)
- Spécification [I2NP](/docs/specs/i2np/) incluant LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/legacy/elgamal-aes/)
- [http://zzz.i2p/topics/1768](http://zzz.i2p/topics/1768) aperçu de la nouvelle cryptographie asymétrique
- Aperçu cryptographique de bas niveau [CRYPTO-ELG](/docs/specs/cryptography/)
- ECIES [http://zzz.i2p/topics/2418](http://zzz.i2p/topics/2418)
- [NTCP2](/docs/specs/ntcp2/) [Proposition 111](/proposals/111-ntcp-2/)
- 123 Nouvelles entrées netDB
- 142 Nouveau modèle cryptographique
- Protocole [Noise](https://noiseprotocol.org/noise.html)
- Algorithme double ratchet [Signal](https://signal.org/docs/)

L'objectif est de prendre en charge le nouveau chiffrement pour la communication de bout en bout, de destination à destination.

La conception utilisera une négociation Noise et une phase de données incorporant le double ratchet de Signal.

Toutes les références à Signal and Noise dans cette proposition sont uniquement à titre d'information générale. La connaissance des protocoles Signal and Noise n'est pas requise pour comprendre ou implémenter cette proposition.

### Current ElGamal Uses

En guise de récapitulatif, les clés publiques ElGamal de 256 octets peuvent être trouvées dans les structures de données suivantes. Consultez la spécification des structures communes.

- Dans une Router Identity
  Il s'agit de la clé de chiffrement du routeur.

- Dans une Destination
  La clé publique de la destination était utilisée pour l'ancien chiffrement i2cp-to-i2cp
  qui a été désactivé dans la version 0.6, elle n'est actuellement pas utilisée sauf pour
  l'IV pour le chiffrement LeaseSet, qui est déprécié.
  La clé publique dans le LeaseSet est utilisée à la place.

- Dans un LeaseSet
  Il s'agit de la clé de chiffrement de la destination.

- Dans un LS2
  C'est la clé de chiffrement de la destination.

### EncTypes in Key Certs

Pour rappel, nous avons ajouté la prise en charge des types de chiffrement lorsque nous avons ajouté la prise en charge des types de signature. Le champ type de chiffrement est toujours zéro, à la fois dans les Destinations et les RouterIdentities. S'il faut jamais changer cela reste à déterminer. Consultez la spécification des structures communes [Common Structures](/docs/specs/common-structures/).

### Utilisations actuelles d'ElGamal

Pour rappel, nous utilisons ElGamal pour :

1) Messages de construction de tunnel (la clé est dans RouterIdentity)    Le remplacement n'est pas couvert dans cette proposition.    Voir la proposition 152 [Proposition 152](/proposals/152-ecies-tunnels).

2) Chiffrement router-à-router du netdb et autres messages I2NP (La clé est dans RouterIdentity)    Dépend de cette proposition.    Nécessite une proposition pour 1) également, ou placer la clé dans les options RI.

3) Client End-to-end ElGamal+AES/SessionTag (la clé est dans le LeaseSet, la clé de Destination n'est pas utilisée)    Le remplacement EST couvert dans cette proposition.

4) DH éphémère pour NTCP1 et SSU    Le remplacement n'est pas couvert dans cette proposition.    Voir la proposition 111 pour NTCP2.    Aucune proposition actuelle pour SSU2.

### EncTypes dans les Key Certs

- Rétrocompatible
- Nécessite et s'appuie sur LS2 (proposition 123)
- Exploite la nouvelle cryptographie ou les primitives ajoutées pour NTCP2 (proposition 111)
- Aucune nouvelle cryptographie ou primitive requise pour le support
- Maintenir le découplage de la cryptographie et de la signature ; supporter toutes les versions actuelles et futures
- Activer la nouvelle cryptographie pour les destinations
- Activer la nouvelle cryptographie pour les routeurs, mais uniquement pour les messages garlic - la construction de tunnels ferait l'objet d'une proposition séparée
- Ne rien casser qui repose sur les hachages de destination binaires de 32 octets, par ex. bittorrent
- Maintenir la livraison de messages 0-RTT en utilisant DH éphémère-statique
- Ne pas exiger la mise en mémoire tampon / file d'attente des messages à cette couche de protocole ; continuer à supporter la livraison illimitée de messages dans les deux directions sans attendre de réponse
- Mise à niveau vers DH éphémère-éphémère après 1 RTT
- Maintenir la gestion des messages hors séquence
- Maintenir la sécurité 256-bit
- Ajouter le secret de transmission (forward secrecy)
- Ajouter l'authentification (AEAD)
- Beaucoup plus efficace en CPU qu'ElGamal
- Ne pas dépendre de Java jbigi pour rendre DH efficace
- Minimiser les opérations DH
- Beaucoup plus efficace en bande passante qu'ElGamal (bloc ElGamal de 514 octets)
- Supporter la nouvelle et l'ancienne cryptographie sur le même tunnel si désiré
- Le destinataire est capable de distinguer efficacement la nouvelle de l'ancienne cryptographie arrivant par le même tunnel
- Les autres ne peuvent pas distinguer la nouvelle de l'ancienne ou future cryptographie
- Éliminer la classification de longueur de session nouvelle vs. existante (supporter le padding)
- Aucun nouveau message I2NP requis
- Remplacer la somme de contrôle SHA-256 dans la charge utile AES par AEAD
- Supporter la liaison des sessions de transmission et de réception pour que les accusés de réception puissent se faire dans le protocole, plutôt qu'uniquement hors bande. Cela permettra aussi aux réponses d'avoir le secret de transmission immédiatement.
- Activer le chiffrement de bout en bout de certains messages (stockages RouterInfo) que nous ne chiffrons actuellement pas en raison de la surcharge CPU.
- Ne pas changer le message I2NP Garlic Message ou le format des instructions de livraison Garlic Message.
- Éliminer les champs inutilisés ou redondants dans les formats Garlic Clove Set et Clove.

Éliminer plusieurs problèmes avec les balises de session, notamment :

- Impossibilité d'utiliser AES jusqu'à la première réponse
- Manque de fiabilité et blocages si la livraison de tags est présumée
- Inefficacité de la bande passante, particulièrement lors de la première livraison
- Énorme inefficacité d'espace pour stocker les tags
- Énorme surcharge de bande passante pour livrer les tags
- Très complexe, difficile à implémenter
- Difficile à ajuster pour divers cas d'usage
  (streaming vs. datagrammes, serveur vs. client, bande passante élevée vs. faible)
- Vulnérabilités d'épuisement de mémoire dues à la livraison de tags

### Utilisations de la Cryptographie Asymétrique

- Changements du format LS2 (la proposition 123 est terminée)
- Nouvel algorithme de rotation DHT ou génération aléatoire partagée
- Nouveau chiffrement pour la construction de tunnels.
  Voir la proposition 152 [Proposition 152](/proposals/152-ecies-tunnels).
- Nouveau chiffrement pour le chiffrement de couche tunnel.
  Voir la proposition 153 [Proposition 153](/proposals/153-chacha20-layer-encryption).
- Méthodes de chiffrement, transmission et réception des messages I2NP DLM / DSM / DSRM.
  Aucun changement.
- Aucune communication LS1-vers-LS2 ou ElGamal/AES-vers-cette-proposition n'est prise en charge.
  Cette proposition est un protocole bidirectionnel.
  Les destinations peuvent gérer la rétrocompatibilité en publiant deux leasesets
  utilisant les mêmes tunnels, ou en mettant les deux types de chiffrement dans le LS2.
- Changements du modèle de menace
- Les détails d'implémentation ne sont pas discutés ici et sont laissés à chaque projet.
- (Optimiste) Ajouter des extensions ou des hooks pour prendre en charge le multicast

### Objectifs

ElGamal/AES+SessionTag a été notre seul protocole de bout en bout pendant environ 15 ans, essentiellement sans modifications du protocole. Il existe maintenant des primitives cryptographiques qui sont plus rapides. Nous devons renforcer la sécurité du protocole. Nous avons également développé des stratégies heuristiques et des solutions de contournement pour minimiser la surcharge mémoire et bande passante du protocole, mais ces stratégies sont fragiles, difficiles à ajuster, et rendent le protocole encore plus susceptible de se briser, provoquant la chute de la session.

Pendant à peu près la même période, la spécification ElGamal/AES+SessionTag et la documentation associée ont décrit à quel point il est coûteux en bande passante de livrer les session tags, et ont proposé de remplacer la livraison de session tag par un "PRNG synchronisé". Un PRNG synchronisé génère de manière déterministe les mêmes tags aux deux extrémités, dérivés d'une graine commune. Un PRNG synchronisé peut également être appelé un "ratchet". Cette proposition spécifie (enfin) ce mécanisme de ratchet, et élimine la livraison de tags.

En utilisant un ratchet (un PRNG synchronisé) pour générer les session tags, nous éliminons la surcharge liée à l'envoi des session tags dans le message New Session et les messages suivants lorsque nécessaire. Pour un ensemble typique de 32 tags, cela représente 1 Ko. Cela élimine également le stockage des session tags côté expéditeur, réduisant ainsi les exigences de stockage de moitié.

Un handshake bidirectionnel complet, similaire au pattern Noise IK, est nécessaire pour éviter les attaques de type Key Compromise Impersonation (KCI). Voir le tableau "Payload Security Properties" de Noise dans [NOISE](https://noiseprotocol.org/noise.html). Pour plus d'informations sur KCI, voir l'article https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf

### Non-objectifs / Hors du périmètre

Le modèle de menace est quelque peu différent de celui pour NTCP2 (proposition 111). Les nœuds MitM sont l'OBEP et l'IBGW et sont supposés avoir une vue complète du netDb global actuel ou historique, en collaborant avec les floodfills.

L'objectif est d'empêcher ces attaques MitM de classifier le trafic comme des messages de Session Nouvelle et Existante, ou comme nouveau crypto vs. ancien crypto.

## Detailed Proposal

Cette proposition définit un nouveau protocole de bout en bout pour remplacer ElGamal/AES+SessionTags. La conception utilisera un handshake Noise et une phase de données incorporant le double ratchet de Signal.

### Justification

Il y a cinq parties du protocole à reconcevoir :

- 1) Les formats de conteneur de session nouveaux et existants
  sont remplacés par de nouveaux formats.
- 2) ElGamal (clés publiques de 256 octets, clés privées de 128 octets) est remplacé
  par ECIES-X25519 (clés publiques et privées de 32 octets)
- 3) AES est remplacé par
  AEAD_ChaCha20_Poly1305 (abrégé en ChaChaPoly ci-dessous)
- 4) Les SessionTags seront remplacés par des ratchets,
  qui sont essentiellement un PRNG cryptographique et synchronisé.
- 5) La charge utile AES, telle que définie dans la spécification ElGamal/AES+SessionTags,
  est remplacée par un format de bloc similaire à celui de NTCP2.

Chacune des cinq modifications a sa propre section ci-dessous.

### Modèle de menace

Les implémentations existantes de router I2P nécessiteront des implémentations pour les primitives cryptographiques standards suivantes, qui ne sont pas requises pour les protocoles I2P actuels :

- ECIES (mais il s'agit essentiellement de X25519)
- Elligator2

Les implémentations de routeur I2P existantes qui n'ont pas encore implémenté [NTCP2](/docs/specs/ntcp2/) ([Proposition 111](/proposals/111-ntcp-2/)) nécessiteront également des implémentations pour :

- Génération de clés X25519 et DH
- AEAD_ChaCha20_Poly1305 (abrégé en ChaChaPoly ci-dessous)
- HKDF

### Crypto Type

Le type de chiffrement (utilisé dans le LS2) est 4. Ceci indique une clé publique X25519 de 32 octets en little-endian, et le protocole de bout en bout spécifié ici.

Le type de crypto 0 est ElGamal. Les types de crypto 1-3 sont réservés pour ECIES-ECDH-AES-SessionTag, voir la proposition 145 [Proposal 145](/proposals/145-ecies).

### Résumé de la conception cryptographique

Cette proposition fournit les exigences basées sur le Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11). Noise a des propriétés similaires au protocole Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), qui est la base du protocole [SSU](/docs/legacy/ssu/). Dans la terminologie Noise, Alice est l'initiateur, et Bob est le répondeur.

Cette proposition est basée sur le protocole Noise Noise_IK_25519_ChaChaPoly_SHA256. (L'identifiant réel pour la fonction de dérivation de clé initiale est "Noise_IKelg2_25519_ChaChaPoly_SHA256" pour indiquer les extensions I2P - voir la section KDF 1 ci-dessous) Ce protocole Noise utilise les primitives suivantes :

- Interactive Handshake Pattern: IK
  Alice transmet immédiatement sa clé statique à Bob (I)
  Alice connaît déjà la clé statique de Bob (K)

- One-Way Handshake Pattern: N
  Alice ne transmet pas sa clé statique à Bob (N)

- Fonction DH : X25519
  X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Fonction de chiffrement : ChaChaPoly
  AEAD_CHACHA20_POLY1305 tel que spécifié dans la [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8.
  Nonce de 12 octets, avec les 4 premiers octets définis à zéro.
  Identique à celui de [NTCP2](/docs/specs/ntcp2/).

- Hash Function: SHA256
  Hash standard de 32 octets, déjà utilisé de manière extensive dans I2P.

### Nouvelles primitives cryptographiques pour I2P

Cette proposition définit les améliorations suivantes à Noise_IK_25519_ChaChaPoly_SHA256. Celles-ci suivent généralement les directives de la section 13 de [NOISE](https://noiseprotocol.org/noise.html).

1) Les clés éphémères en clair sont encodées avec [Elligator2](https://elligator.cr.yp.to/).

2) La réponse est préfixée avec une balise en texte clair.

3) Le format de charge utile est défini pour les messages 1, 2, et la phase de données. Bien sûr, ceci n'est pas défini dans Noise.

Tous les messages incluent un en-tête de message Garlic [I2NP](/docs/specs/i2np/). La phase de données utilise un chiffrement similaire à, mais non compatible avec, la phase de données Noise.

### Type de cryptographie

Les handshakes utilisent les modèles de handshake [Noise](https://noiseprotocol.org/noise.html).

La correspondance de lettres suivante est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message

Les sessions One-time et Unbound sont similaires au pattern Noise N.

```

<- s
  ...
  e es p ->

```
Les sessions liées sont similaires au modèle Noise IK.

```

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->

```
### Framework de Protocole Noise

Le protocole ElGamal/AES+SessionTag actuel est unidirectionnel. À cette couche, le destinataire ne sait pas d'où provient un message. Les sessions sortantes et entrantes ne sont pas associées. Les accusés de réception sont hors-bande en utilisant un DeliveryStatusMessage (encapsulé dans un GarlicMessage) dans le clove.

Il y a une inefficacité substantielle dans un protocole unidirectionnel. Toute réponse doit également utiliser un message coûteux 'New Session'. Cela provoque une utilisation plus élevée de la bande passante, du CPU et de la mémoire.

Il existe également des faiblesses de sécurité dans un protocole unidirectionnel. Toutes les sessions sont basées sur DH éphémère-statique. Sans chemin de retour, il n'y a aucun moyen pour Bob de « faire progresser » sa clé statique vers une clé éphémère. Sans savoir d'où provient un message, il n'y a aucun moyen d'utiliser la clé éphémère reçue pour les messages sortants, donc la réponse initiale utilise également DH éphémère-statique.

Pour cette proposition, nous définissons deux mécanismes pour créer un protocole bidirectionnel - le "pairing" et le "binding". Ces mécanismes offrent une efficacité et une sécurité accrues.

### Ajouts au Framework

Comme avec ElGamal/AES+SessionTags, toutes les sessions entrantes et sortantes doivent être dans un contexte donné, soit le contexte du router soit le contexte d'une destination locale particulière. Dans Java I2P, ce contexte est appelé le Session Key Manager.

Les sessions ne doivent pas être partagées entre les contextes, car cela permettrait une corrélation entre les diverses destinations locales, ou entre une destination locale et un router.

Lorsqu'une destination donnée prend en charge à la fois ElGamal/AES+SessionTags et cette proposition, les deux types de sessions peuvent partager un contexte. Voir la section 1c) ci-dessous.

### Motifs de Handshake

Lorsqu'une session sortante est créée chez l'initiateur (Alice), une nouvelle session entrante est créée et associée à la session sortante, sauf si aucune réponse n'est attendue (par exemple, les datagrammes bruts).

Une nouvelle session entrante est toujours associée à une nouvelle session sortante, sauf si aucune réponse n'est demandée (par exemple, les datagrammes bruts).

Si une réponse est demandée et liée à une destination ou un router distant, cette nouvelle session sortante est liée à cette destination ou ce router, et remplace toute session sortante précédente vers cette destination ou ce router.

L'appariement des sessions entrantes et sortantes fournit un protocole bidirectionnel avec la capacité de faire évoluer les clés DH.

### Sessions

Il n'y a qu'une seule session sortante vers une destination ou un router donné. Il peut y avoir plusieurs sessions entrantes actuelles depuis une destination ou un router donné. Généralement, lorsqu'une nouvelle session entrante est créée et que du trafic est reçu sur cette session (ce qui sert d'ACK), toutes les autres seront marquées pour expirer relativement rapidement, en une minute environ. La valeur des messages précédents envoyés (PN) est vérifiée, et s'il n'y a pas de messages non reçus (dans la taille de fenêtre) dans la session entrante précédente, la session précédente peut être supprimée immédiatement.

Lorsqu'une session sortante est créée chez l'expéditeur (Alice), elle est liée à la Destination distante (Bob), et toute session entrante appariée sera également liée à la Destination distante. Au fur et à mesure que les sessions progressent, elles continuent d'être liées à la Destination distante.

Lorsqu'une session entrante est créée chez le destinataire (Bob), elle peut être liée à la Destination distante (Alice), selon le choix d'Alice. Si Alice inclut des informations de liaison (sa clé statique) dans le message New Session, la session sera liée à cette destination, et une session sortante sera créée et liée à la même Destination. Au fur et à mesure que les sessions évoluent, elles continuent d'être liées à la Destination distante.

### Contexte de Session

Pour le cas courant de streaming, nous nous attendons à ce qu'Alice et Bob utilisent le protocole comme suit :

- Alice apparie sa nouvelle session sortante à une nouvelle session entrante, toutes deux liées à la destination distante (Bob).
- Alice inclut les informations de liaison et la signature, ainsi qu'une demande de réponse, dans le
  message New Session envoyé à Bob.
- Bob apparie sa nouvelle session entrante à une nouvelle session sortante, toutes deux liées à la destination distante (Alice).
- Bob envoie une réponse (ack) à Alice dans la session appariée, avec un ratchet vers une nouvelle clé DH.
- Alice effectue un ratchet vers une nouvelle session sortante avec la nouvelle clé de Bob, appariée à la session entrante existante.

En liant une session entrante à une Destination distante, et en associant la session entrante à une session sortante liée à la même Destination, nous obtenons deux avantages majeurs :

1) La réponse initiale de Bob à Alice utilise un DH éphémère-éphémère

2) Après qu'Alice reçoit la réponse de Bob et effectue le ratcheting, tous les messages suivants d'Alice vers Bob utilisent DH éphémère-éphémère.

### Appairage des sessions entrantes et sortantes

Dans ElGamal/AES+SessionTags, lorsqu'un LeaseSet est regroupé comme un garlic clove, ou que des tags sont livrés, le router émetteur demande un ACK. Il s'agit d'un garlic clove séparé contenant un Message DeliveryStatus. Pour une sécurité supplémentaire, le Message DeliveryStatus est encapsulé dans un Message Garlic. Ce mécanisme est hors-bande du point de vue du protocole.

Dans le nouveau protocole, puisque les sessions entrantes et sortantes sont appariées, nous pouvons avoir des ACK dans la bande. Aucun clove séparé n'est requis.

Un ACK explicite est simplement un message de Session Existante sans bloc I2NP. Cependant, dans la plupart des cas, un ACK explicite peut être évité, car il y a du trafic en sens inverse. Il peut être souhaitable pour les implémentations d'attendre un court laps de temps (peut-être une centaine de ms) avant d'envoyer un ACK explicite, pour donner au streaming ou à la couche application le temps de répondre.

Les implémentations devront également différer l'envoi de tout ACK jusqu'à ce que le bloc I2NP soit traité, car le message Garlic peut contenir un message Database Store avec un lease set. Un lease set récent sera nécessaire pour router l'ACK, et la destination distante (contenue dans le lease set) sera nécessaire pour vérifier la clé statique de liaison.

### Sessions de liaison et destinations

Les sessions sortantes doivent toujours expirer avant les sessions entrantes. Une fois qu'une session sortante expire et qu'une nouvelle est créée, une nouvelle session entrante appariée sera également créée. S'il y avait une ancienne session entrante, elle sera autorisée à expirer.

### Avantages de la liaison et de l'appairage

À déterminer

### ACKs de message

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés.

ZEROLEN

    zero-length byte array

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).
    || below means append.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

MixHash(d)

    SHA-256 hash function that takes a previous hash h and new data d,
    and produces an output of length 32 bytes.
    || below means append.

    Use SHA-256 as follows::

        MixHash(d) := h = SHA-256(h || d)

STREAM

    The ChaCha20/Poly1305 AEAD as specified in [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Encrypts plaintext using the cipher key k, and nonce n which MUST be unique for
        the key k.
        Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16 bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, n, ciphertext, ad)
        Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional.
        Returns the plaintext.

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()
        Generates a new private key that maps to a public key suitable for Elligator2 encoding.
        Note that half of the randomly-generated private keys will not be suitable and must be discarded.

    ENCODE_ELG2(pubkey)
        Returns the Elligator2-encoded public key corresponding to the given public key (inverse mapping).
        Encoded keys are little endian.
        Encoded key must be 256 bits indistinguishable from random data.
        See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)
        Returns the public key corresponding to the given Elligator2-encoded public key.
        See Elligator2 section below for specification.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.

MixKey(d)

    Use HKDF() with a previous chainKey and new data d, and
    sets the new chainKey and k.
    As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]


### Délais d'expiration de session

### Multidiffusion

Le message Garlic tel que spécifié dans [I2NP](/docs/specs/i2np/) est le suivant. Comme un objectif de conception est que les sauts intermédiaires ne puissent pas distinguer la nouvelle cryptographie de l'ancienne, ce format ne peut pas changer, même si le champ de longueur est redondant. Le format est montré avec l'en-tête complet de 16 octets, bien que l'en-tête réel puisse être dans un format différent, selon le transport utilisé.

Lorsqu'elles sont déchiffrées, les données contiennent une série de Garlic Cloves et des données supplémentaires, également connues sous le nom de Clove Set.

Voir [I2NP](/docs/specs/i2np/) pour les détails et une spécification complète.

```

+----+----+----+----+----+----+----+----+
  |type|      msg_id       |  expiration
  +----+----+----+----+----+----+----+----+
                           |  size   |chks|
  +----+----+----+----+----+----+----+----+
  |      length       |                   |
  +----+----+----+----+                   +
  |          encrypted data               |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```
### Définitions

Le format de message actuel, utilisé depuis plus de 15 ans, est ElGamal/AES+SessionTags. Dans ElGamal/AES+SessionTags, il y a deux formats de message :

1) Nouvelle session : - bloc ElGamal de 514 octets - bloc AES (128 octets minimum, multiple de 16)

2) Session existante : - Session Tag de 32 octets - Bloc AES (128 octets minimum, multiple de 16)

Le padding minimum à 128 est tel qu'implémenté dans Java I2P mais n'est pas appliqué à la réception.

Ces messages sont encapsulés dans un message I2NP garlic, qui contient un champ de longueur, donc la longueur est connue.

Notez qu'aucun padding n'est défini pour une longueur non-mod-16, donc la New Session est toujours (mod 16 == 2), et une Existing Session est toujours (mod 16 == 0). Nous devons corriger cela.

Le récepteur tente d'abord de rechercher les 32 premiers octets en tant que Session Tag. S'il la trouve, il décrypte le bloc AES. Si elle n'est pas trouvée, et que les données font au moins (514+16) de long, il tente de décrypter le bloc ElGamal, et en cas de succès, décrypte le bloc AES.

### 1) Format de message

Dans Signal Double Ratchet, l'en-tête contient :

- DH: Clé publique ratchet actuelle
- PN: Longueur du message de la chaîne précédente
- N: Numéro de message

Les "chaînes d'envoi" de Signal sont à peu près équivalentes à nos ensembles de balises. En utilisant une balise de session, nous pouvons éliminer la plupart de cela.

Dans New Session, nous mettons seulement la clé publique dans l'en-tête non chiffré.

Dans une Session Existante, nous utilisons un tag de session pour l'en-tête. Le tag de session est associé à la clé publique ratchet actuelle et au numéro de message.

Dans les sessions nouvelles et existantes, PN et N sont dans le corps chiffré.

Dans Signal, les choses sont constamment en rotation (ratcheting). Une nouvelle clé publique DH exige que le récepteur effectue une rotation et renvoie une nouvelle clé publique, ce qui sert également d'accusé de réception pour la clé publique reçue. Cela représenterait beaucoup trop d'opérations DH pour nous. Nous séparons donc l'accusé de réception de la clé reçue et la transmission d'une nouvelle clé publique. Tout message utilisant une balise de session générée à partir de la nouvelle clé publique DH constitue un ACK. Nous ne transmettons une nouvelle clé publique que lorsque nous souhaitons effectuer un renouvellement de clé.

Le nombre maximum de messages avant que le DH doive effectuer une rotation est de 65535.

Lors de la livraison d'une clé de session, nous dérivons le "Tag Set" à partir de celle-ci, plutôt que d'avoir à livrer également les session tags. Un Tag Set peut contenir jusqu'à 65536 tags. Cependant, les récepteurs doivent implémenter une stratégie de "look-ahead", plutôt que de générer tous les tags possibles en une seule fois. Ne générer au maximum que N tags au-delà du dernier bon tag reçu. N pourrait être au maximum 128, mais 32 ou même moins peut être un meilleur choix.

### Revue du format de message actuel

Nouvelle session Clé publique à usage unique (32 octets) Données chiffrées et MAC (octets restants)

Le message New Session peut contenir ou non la clé publique statique de l'expéditeur. Si elle est incluse, la session inverse est liée à cette clé. La clé statique devrait être incluse si des réponses sont attendues, c'est-à-dire pour le streaming et les datagrammes auxquels on peut répondre. Elle ne devrait pas être incluse pour les datagrammes bruts.

Le message New Session est similaire au pattern Noise [NOISE](https://noiseprotocol.org/noise.html) unidirectionnel "N" (si la clé statique n'est pas envoyée), ou au pattern bidirectionnel "IK" (si la clé statique est envoyée).

### Examen du format de données chiffrées

La longueur est de 96 + longueur de la charge utile. Format chiffré :

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +         Static Key                    +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for Static Key Section       +
  |             16 bytes                  |
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
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Static Key encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Nouvelles étiquettes de session et comparaison avec Signal

La clé éphémère fait 32 octets, encodée avec Elligator2. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec chaque message, y compris les retransmissions.

### 1a) Nouveau format de session

Quand déchiffrée, la clé statique X25519 d'Alice, 32 octets.

### 1b) Nouveau format de session (avec liaison)

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### Nouvelle Clé Éphémère de Session

Si aucune réponse n'est requise, aucune clé statique n'est envoyée.

La longueur est de 96 + longueur du payload. Format chiffré :

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   New Session Ephemeral Public Key    |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
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
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Clé Statique

Clé éphémère d'Alice. La clé éphémère fait 32 octets, encodée avec Elligator2, little endian. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec chaque message, y compris les retransmissions.

### Charge utile

La section Flags ne contient rien. Elle fait toujours 32 octets, car elle doit avoir la même longueur que la clé statique pour les messages New Session avec liaison. Bob détermine s'il s'agit d'une clé statique ou d'une section flags en testant si les 32 octets sont tous des zéros.

TODO des flags nécessaires ici ?

### 1c) Nouveau format de session (sans liaison)

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. Le payload doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section payload ci-dessous pour le format et les exigences supplémentaires.

### Clé Éphémère de Nouvelle Session

Si un seul message doit être envoyé, aucune configuration de session ou clé statique n'est requise.

La longueur est de 96 + longueur de la charge utile. Format chiffré :

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       Ephemeral Public Key            |
  +             32 bytes                  +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Flags Section               +
  |       ChaCha20 encrypted data         |
  +            32 bytes                   +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +         (MAC) for above section       +
  |             16 bytes                  |
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
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  Flags Section encrypted data :: 32 bytes

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Section Flags Données déchiffrées

La clé à usage unique fait 32 octets, encodée avec Elligator2, little endian. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée pour chaque message, y compris les retransmissions.

### Charge utile

La section Flags ne contient rien. Elle fait toujours 32 octets, car elle doit avoir la même longueur que la clé statique pour les messages New Session avec liaison. Bob détermine s'il s'agit d'une clé statique ou d'une section flags en testant si les 32 octets sont tous des zéros.

TODO des drapeaux nécessaires ici ?

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: All zeros, 32 bytes.

```
### 1d) Format ponctuel (sans liaison ni session)

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### Nouvelle Clé de Session à Usage Unique

### Section Flags Données déchiffrées

Il s'agit du [NOISE](https://noiseprotocol.org/noise.html) standard pour IK avec un nom de protocole modifié. Notez que nous utilisons le même initialisateur pour le motif IK (sessions liées) et pour le motif N (sessions non liées).

Le nom du protocole est modifié pour deux raisons. Premièrement, pour indiquer que les clés éphémères sont encodées avec Elligator2, et deuxièmement, pour indiquer que MixHash() est appelé avant le second message pour mélanger la valeur du tag.

```

This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  h = SHA256(protocol_name);

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by Alice for all outgoing connections

```
### Charge utile

```

This is the "e" message pattern:

  // Bob's X25519 static keys
  // bpk is published in leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Bob static public key
  // MixHash(bpk)
  // || below means append
  h = SHA256(h || bpk);

  // up until here, can all be precalculated by Bob for all incoming connections

  // Alice's X25519 ephemeral keys
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Alice ephemeral public key
  // MixHash(aepk)
  // || below means append
  h = SHA256(h || aepk);

  // h is used as the associated data for the AEAD in the New Session Message
  // Retain the Hash h for the New Session Reply KDF
  // eapk is sent in cleartext in the
  // beginning of the New Session message
  elg2_aepk = ENCODE_ELG2(aepk)
  // As decoded by Bob
  aepk = DECODE_ELG2(elg2_aepk)

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, flags/static key section, ad)

  End of "es" message pattern.

  This is the "s" message pattern:

  // MixHash(ciphertext)
  // Save for Payload section KDF
  h = SHA256(h || ciphertext)

  // Alice's X25519 static keys
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  End of "s" message pattern.


```
### 1f) KDF pour le message de nouvelle session

```

This is the "ss" message pattern:

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from Static Key Section
  Set sharedSecret = X25519 DH result
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)

  End of "ss" message pattern.

  // MixHash(ciphertext)
  // Save for New Session Reply KDF
  h = SHA256(h || ciphertext)

```
### KDF pour la ChainKey initiale

Notez que ceci est un motif Noise "N", mais nous utilisons le même initialiseur "IK" que pour les sessions liées.

Les messages New Session ne peuvent pas être identifiés comme contenant ou non la clé statique d'Alice jusqu'à ce que la clé statique soit déchiffrée et inspectée pour déterminer si elle contient uniquement des zéros. Par conséquent, le récepteur doit utiliser la machine d'état "IK" pour tous les messages New Session. Si la clé statique ne contient que des zéros, le motif de message "ss" doit être ignoré.

```

chainKey = from Flags/Static key section
  k = from Flags/Static key section
  n = 1
  ad = h from Flags/Static key section
  ciphertext = ENCRYPT(k, n, payload, ad)

```
### KDF pour le Contenu Chiffré de la Section Flags/Static Key

Une ou plusieurs réponses New Session Reply peuvent être envoyées en réponse à un seul message New Session. Chaque réponse est préfixée par une balise, qui est générée à partir d'un TagSet pour la session.

La New Session Reply est en deux parties. La première partie est l'achèvement du handshake Noise IK avec un tag préfixé. La longueur de la première partie est de 56 octets. La seconde partie est la charge utile de la phase de données. La longueur de la seconde partie est de 16 + longueur de la charge utile.

La longueur totale est de 72 + longueur de la charge utile. Format chiffré :

```

+----+----+----+----+----+----+----+----+
  |       Session Tag   8 bytes           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Ephemeral Public Key           +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for Key Section (no data)      +
  |             16 bytes                  |
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
  +         (MAC) for Payload Section     +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  Tag :: 8 bytes, cleartext

  Public Key :: 32 bytes, little endian, Elligator2, cleartext

  MAC :: Poly1305 message authentication code, 16 bytes
         Note: The ChaCha20 plaintext data is empty (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### KDF pour la Section Payload (avec la clé statique d'Alice)

Le tag est généré dans le Session Tags KDF, tel qu'initialisé dans le DH Initialization KDF ci-dessous. Ceci corrèle la réponse à la session. La Session Key du DH Initialization n'est pas utilisée.

### KDF pour la Section de Charge Utile (sans clé statique d'Alice)

Clé éphémère de Bob. La clé éphémère fait 32 octets, encodée avec Elligator2, little endian. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec chaque message, y compris les retransmissions.

### 1g) Format de réponse New Session

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### Balise de Session

Un ou plusieurs tags sont créés à partir du TagSet, qui est initialisé en utilisant le KDF ci-dessous, en utilisant la chainKey du message New Session.

```

// Generate tagset
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
### Réponse de Nouvelle Session Clé Éphémère

```

// Keys from the New Session message
  // Alice's X25519 keys
  // apk and aepk are sent in original New Session message
  // ask = Alice private static key
  // apk = Alice public static key
  // aesk = Alice ephemeral private key
  // aepk = Alice ephemeral public key
  // Bob's X25519 static keys
  // bsk = Bob private static key
  // bpk = Bob public static key

  // Generate the tag
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  This is the "e" message pattern:

  // Bob's X25519 ephemeral keys
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Bob's ephemeral public key
  // MixHash(bepk)
  // || below means append
  h = SHA256(h || bepk);

  // elg2_bepk is sent in cleartext in the
  // beginning of the New Session message
  elg2_bepk = ENCODE_ELG2(bepk)
  // As decoded by Bob
  bepk = DECODE_ELG2(elg2_bepk)

  End of "e" message pattern.

  This is the "ee" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  // chainKey from original New Session Payload Section
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  End of "ee" message pattern.

  This is the "se" message pattern:

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  End of "se" message pattern.

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey is used in the ratchet below.

```
### Charge utile

C'est comme le premier message de Session Existante, post-division, mais sans balise séparée. De plus, nous utilisons le hachage ci-dessus pour lier la charge utile au message NSR.

```

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // AEAD parameters for New Session Reply payload
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### KDF pour Reply TagSet

Plusieurs messages NSR peuvent être envoyés en réponse, chacun avec des clés éphémères uniques, selon la taille de la réponse.

Alice et Bob sont tenus d'utiliser de nouvelles clés éphémères pour chaque message NS et NSR.

Alice doit recevoir un des messages NSR de Bob avant d'envoyer des messages de Session Existante (ES), et Bob doit recevoir un message ES d'Alice avant d'envoyer des messages ES.

Les ``chainKey`` et ``k`` de la Section de Charge Utile NSR de Bob sont utilisés comme entrées pour les Ratchets DH ES initiaux (dans les deux directions, voir DH Ratchet KDF).

Bob ne doit conserver que les Sessions Existantes pour les messages ES reçus d'Alice. Toutes les autres sessions entrantes et sortantes créées (pour plusieurs NSR) doivent être détruites immédiatement après avoir reçu le premier message ES d'Alice pour une session donnée.

### KDF pour le contenu chiffré de la section clé de réponse

Tag de session (8 octets) Données chiffrées et MAC (voir section 3 ci-dessous)

### KDF pour le contenu chiffré de la section Payload

Chiffré :

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
### Notes

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. Voir la section payload ci-dessous pour le format et les exigences.

KDF

```
See AEAD section below.

  // AEAD parameters for Existing Session payload
  k = The 32-byte session key associated with this session tag
  n = The message number N in the current chain, as retrieved from the associated Session Tag.
  ad = The session tag, 8 bytes
  ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1h) Format de session existant

Format : Clés publiques et privées de 32 octets, little-endian.

Justification : Utilisé dans [NTCP2](/docs/specs/ntcp2/).

### Format

Dans les handshakes Noise standard, les messages de handshake initiaux dans chaque direction commencent par des clés éphémères qui sont transmises en texte clair. Comme les clés X25519 valides sont distinguables de l'aléatoire, un homme-du-milieu peut distinguer ces messages des messages de Session Existante qui commencent par des tags de session aléatoires. Dans [NTCP2](/docs/specs/ntcp2/) ([Proposition 111](/proposals/111-ntcp-2/)), nous avons utilisé une fonction XOR à faible surcharge utilisant la clé statique hors-bande pour obfusquer la clé. Cependant, le modèle de menace ici est différent ; nous ne voulons permettre à aucun MitM d'utiliser quelque moyen que ce soit pour confirmer la destination du trafic, ou pour distinguer les messages de handshake initiaux des messages de Session Existante.

Par conséquent, [Elligator2](https://elligator.cr.yp.to/) est utilisé pour transformer les clés éphémères dans les messages New Session et New Session Reply afin qu'elles soient indiscernables de chaînes aléatoires uniformes.

### Charge utile

Clés publiques et privées de 32 octets. Les clés encodées sont en little endian.

Comme défini dans [Elligator2](https://elligator.cr.yp.to/), les clés encodées sont indiscernables de 254 bits aléatoires. Nous avons besoin de 256 bits aléatoires (32 octets). Par conséquent, l'encodage et le décodage sont définis comme suit :

Encodage :

```

ENCODE_ELG2() Definition

  // Encode as defined in Elligator2 specification
  encodedKey = encode(pubkey)
  // OR in 2 random bits to MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)
```
Décodage :

```

DECODE_ELG2() Definition

  // Mask out 2 random bits from MSB
  encodedKey[31] &= 0x3f
  // Decode as defined in Elligator2 specification
  pubkey = decode(encodedKey)
```
### 2) ECIES-X25519

Requis pour empêcher l'OBEP et l'IBGW de classifier le trafic.

### 2a) Elligator2

Elligator2 double en moyenne le temps de génération de clés, car la moitié des clés privées résultent en clés publiques qui ne conviennent pas pour l'encodage avec Elligator2. De plus, le temps de génération de clés est non borné avec une distribution exponentielle, car le générateur doit continuer à réessayer jusqu'à ce qu'une paire de clés appropriée soit trouvée.

Cette surcharge peut être gérée en effectuant la génération de clés à l'avance, dans un thread séparé, pour maintenir un pool de clés appropriées.

Le générateur effectue la fonction ENCODE_ELG2() pour déterminer la pertinence. Par conséquent, le générateur devrait stocker le résultat d'ENCODE_ELG2() afin qu'il n'ait pas à être calculé à nouveau.

De plus, les clés inadéquates peuvent être ajoutées au pool de clés utilisées pour [NTCP2](/docs/specs/ntcp2/), où Elligator2 n'est pas utilisé. Les problèmes de sécurité liés à cette pratique restent à déterminer.

### Format

AEAD utilisant ChaCha20 et Poly1305, identique à celui de [NTCP2](/docs/specs/ntcp2/). Ceci correspond à [RFC-7539](https://tools.ietf.org/html/rfc7539), qui est également utilisé de manière similaire dans TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

### Justification

Entrées vers les fonctions de chiffrement/déchiffrement pour un bloc AEAD dans un message New Session :

```

k :: 32 byte cipher key
       See New Session and New Session Reply KDFs above.

  n :: Counter-based nonce, 12 bytes.
       n = 0

  ad :: Associated data, 32 bytes.
        The SHA256 hash of the preceding data, as output from mixHash()

  data :: Plaintext data, 0 or more bytes

```
### Notes

Entrées aux fonctions de chiffrement/déchiffrement pour un bloc AEAD dans un message de Session Existante :

```

k :: 32 byte session key
       As looked up from the accompanying session tag.

  n :: Counter-based nonce, 12 bytes.
       Starts at 0 and incremented for each message when transmitting.
       For the receiver, the value
       as looked up from the accompanying session tag.
       First four bytes are always zero.
       Last eight bytes are the message number (n), little-endian encoded.
       Maximum value is 65535.
       Session must be ratcheted when N reaches that value.
       Higher values must never be used.

  ad :: Associated data
        The session tag

  data :: Plaintext data, 0 or more bytes

```
### 3) AEAD (ChaChaPoly)

Sortie de la fonction de chiffrement, entrée de la fonction de déchiffrement :

```

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |       ChaCha20 encrypted data         |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +              (MAC)                    +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+

  encrypted data :: Same size as plaintext data, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes

```
### Entrées New Session et New Session Reply

- Étant donné que ChaCha20 est un chiffre de flux, les textes en clair n'ont pas besoin d'être complétés par du bourrage.
  Les octets de flux de clés supplémentaires sont supprimés.

- La clé pour le chiffrement (256 bits) est convenue au moyen du SHA256 KDF.
  Les détails du KDF pour chaque message se trouvent dans les sections séparées ci-dessous.

- Les trames ChaChaPoly ont une taille connue car elles sont encapsulées dans le message de données I2NP.

- Pour tous les messages,
  le remplissage est à l'intérieur de la
  trame de données authentifiées.

### Entrées de Session Existantes

Toutes les données reçues qui échouent à la vérification AEAD doivent être supprimées. Aucune réponse n'est retournée.

### Format Chiffré

Utilisé dans [NTCP2](/docs/specs/ntcp2/).

### Notes

Nous utilisons toujours les session tags, comme avant, mais nous utilisons des ratchets pour les générer. Les session tags avaient aussi une option de renouvellement de clé que nous n'avons jamais implémentée. Donc c'est comme un double ratchet mais nous n'avons jamais fait le second.

Ici nous définissons quelque chose de similaire au Double Ratchet de Signal. Les tags de session sont générés de manière déterministe et identique côté récepteur et côté expéditeur.

En utilisant un ratchet de clé/tag symétrique, nous éliminons l'utilisation de la mémoire pour stocker les session tags du côté de l'expéditeur. Nous éliminons également la consommation de bande passante liée à l'envoi d'ensembles de tags. L'utilisation côté récepteur reste importante, mais nous pouvons la réduire davantage car nous allons réduire le session tag de 32 octets à 8 octets.

Nous n'utilisons pas le chiffrement d'en-tête tel que spécifié (et optionnel) dans Signal, nous utilisons les balises de session à la place.

En utilisant un ratchet DH, nous obtenons la confidentialité persistante, qui n'a jamais été implémentée dans ElGamal/AES+SessionTags.

Note : La clé publique à usage unique New Session ne fait pas partie du ratchet, sa seule fonction est de chiffrer la clé ratchet DH initiale d'Alice.

### Gestion des erreurs AEAD

Le Double Ratchet gère les messages perdus ou arrivés dans le désordre en incluant une étiquette dans chaque en-tête de message. Le récepteur recherche l'index de l'étiquette, qui correspond au numéro de message N. Si le message contient un bloc Message Number avec une valeur PN, le destinataire peut supprimer toutes les étiquettes supérieures à cette valeur dans le jeu d'étiquettes précédent, tout en conservant les étiquettes ignorées du jeu d'étiquettes précédent au cas où les messages ignorés arriveraient plus tard.

### Justification

Nous définissons les structures de données et fonctions suivantes pour implémenter ces ratchets.

TAGSET_ENTRY

    A single entry in a TAGSET.

    INDEX
        An integer index, starting with 0

    SESSION_TAG
        An identifier to go out on the wire, 8 bytes

    SESSION_KEY
        A symmetric key, never goes on the wire, 32 bytes

TAGSET

    A collection of TAGSET_ENTRIES.

    CREATE(key, n)
        Generate a new TAGSET using initial cryptographic key material of 32 bytes.
        The associated session identifier is provided.
        The initial number of of tags to create is specified; this is generally 0 or 1
        for an outgoing session.
        LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)
        Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()
        Generate one more TAGSET_ENTRY, unless the maximum number SESSION_TAGS have
        already been generated.
        If LAST_INDEX is greater than or equal to 65535, return.
        ++ LAST_INDEX
        Create a new TAGSET_ENTRY with the LAST_INDEX value and the calculated SESSION_TAG.
        Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may
        be deferred and calculated in GET_SESSION_KEY().
        Calls EXPIRE()

    EXPIRE()
        Remove tags and keys that are too old, or if the TAGSET size exceeds some limit.

    RATCHET_TAG()
        Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()
        Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION
        The associated session.

    CREATION_TIME
        When the TAGSET was created.

    LAST_INDEX
        The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()
        Used for outgoing sessions only.
        EXTEND(1) is called if there are no remaining TAGSET_ENTRIES.
        If EXTEND(1) did nothing, the max of 65535 TAGSETS have been used,
        and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)
        Used for incoming sessions only.
        Returns the TAGSET_ENTRY containing the sessionTag.
        If found, the TAGSET_ENTRY is removed.
        If the SESSION_KEY calculation was deferred, it is calculated now.
        If there are few TAGSET_ENTRIES remaining, EXTEND(n) is called.


### 4) Ratchets

Ratchets mais pas aussi rapidement que Signal. Nous séparons l'accusé de réception de la clé reçue de la génération de la nouvelle clé. Dans un usage typique, Alice et Bob vont chacun effectuer un ratchet (deux fois) immédiatement dans une Nouvelle Session, mais n'effectueront plus de ratchet par la suite.

Notez qu'un ratchet est unidirectionnel et génère une chaîne de ratchet New Session tag / clé de message pour cette direction. Pour générer des clés dans les deux directions, vous devez effectuer le ratchet deux fois.

Vous effectuez un ratchet à chaque fois que vous générez et envoyez une nouvelle clé. Vous effectuez un ratchet à chaque fois que vous recevez une nouvelle clé.

Alice effectue un ratchet une fois lors de la création d'une session sortante non liée, elle ne crée pas de session entrante (non liée signifie non-répondable).

Bob effectue un ratchet une fois lors de la création d'une session entrante non liée, et ne crée pas de session sortante correspondante (non liée signifie non-répondable).

Alice continue d'envoyer des messages New Session (NS) à Bob jusqu'à recevoir un de ses messages New Session Reply (NSR). Elle utilise ensuite les résultats KDF de la Section Payload du NSR comme entrées pour les cliquets de session (voir DH Ratchet KDF), et commence à envoyer des messages Existing Session (ES).

Pour chaque message NS reçu, Bob crée une nouvelle session entrante, utilisant les résultats KDF de la section Payload de réponse comme entrées pour le nouveau DH Ratchet ES entrant et sortant.

Pour chaque réponse requise, Bob envoie à Alice un message NSR avec la réponse dans le payload. Il est obligatoire que Bob utilise de nouvelles clés éphémères pour chaque NSR.

Bob doit recevoir un message ES d'Alice sur l'une des sessions entrantes, avant de créer et d'envoyer des messages ES sur la session sortante correspondante.

Alice devrait utiliser un minuteur pour recevoir un message NSR de Bob. Si le minuteur expire, la session devrait être supprimée.

Pour éviter une attaque KCI et/ou d'épuisement des ressources, où un attaquant rejette les réponses NSR de Bob pour maintenir Alice en train d'envoyer des messages NS, Alice devrait éviter de démarrer de nouvelles sessions vers Bob après un certain nombre de tentatives dues à l'expiration du minuteur.

Alice et Bob effectuent chacun un ratchet DH pour chaque bloc NextKey reçu.

Alice et Bob génèrent chacun de nouveaux ratchets d'ensembles de tags et deux ratchets de clés symétriques après chaque ratchet DH. Pour chaque nouveau message ES dans une direction donnée, Alice et Bob font avancer les ratchets de tags de session et de clés symétriques.

La fréquence des ratchets DH après la négociation initiale dépend de l'implémentation. Bien que le protocole impose une limite de 65535 messages avant qu'un ratchet soit requis, un ratcheting plus fréquent (basé sur le nombre de messages, le temps écoulé, ou les deux) peut fournir une sécurité supplémentaire.

Après le KDF de poignée de main finale sur les sessions liées, Bob et Alice doivent exécuter la fonction Noise Split() sur le CipherState résultant pour créer des clés de chaîne symétriques et de tag indépendantes pour les sessions entrantes et sortantes.

#### KEY AND TAG SET IDS

Les numéros d'ID des clés et des ensembles de balises sont utilisés pour identifier les clés et les ensembles de balises. Les ID de clés sont utilisés dans les blocs NextKey pour identifier la clé envoyée ou utilisée. Les ID d'ensembles de balises sont utilisés (avec le numéro de message) dans les blocs ACK pour identifier le message acquitté. Les ID de clés et d'ensembles de balises s'appliquent aux ensembles de balises pour une seule direction. Les numéros d'ID des clés et des ensembles de balises doivent être séquentiels.

Dans les premiers ensembles de tags utilisés pour une session dans chaque direction, l'ID de l'ensemble de tags est 0. Aucun bloc NextKey n'a été envoyé, il n'y a donc pas d'ID de clé.

Pour commencer un ratchet DH, l'expéditeur transmet un nouveau bloc NextKey avec un ID de clé de 0. Le destinataire répond avec un nouveau bloc NextKey avec un ID de clé de 0. L'expéditeur commence alors à utiliser un nouveau jeu de tags avec un ID de jeu de tags de 1.

Les ensembles de tags suivants sont générés de manière similaire. Pour tous les ensembles de tags utilisés après les échanges NextKey, le numéro d'ensemble de tags est (1 + l'ID de clé d'Alice + l'ID de clé de Bob).

Les IDs des clés et des ensembles de tags commencent à 0 et s'incrémentent séquentiellement. L'ID maximum d'un ensemble de tags est 65535. L'ID maximum d'une clé est 32767. Lorsqu'un ensemble de tags est presque épuisé, l'expéditeur de l'ensemble de tags doit initier un échange NextKey. Lorsque l'ensemble de tags 65535 est presque épuisé, l'expéditeur de l'ensemble de tags doit initier une nouvelle session en envoyant un message New Session.

Avec une taille maximale de message en streaming de 1730, et en supposant aucune retransmission, le transfert de données théorique maximum utilisant un seul ensemble de tags est de 1730 * 65536 ~= 108 MB. Le maximum réel sera plus faible en raison des retransmissions.

Le transfert de données théorique maximum avec les 65536 ensembles de tags disponibles, avant que la session doive être supprimée et remplacée, est de 64K * 108 MB ~= 6,9 TB.

#### DH RATCHET MESSAGE FLOW

Le prochain échange de clés pour un ensemble de tags doit être initié par l'expéditeur de ces tags (le propriétaire de l'ensemble de tags sortants). Le récepteur (propriétaire de l'ensemble de tags entrants) répondra. Pour un trafic HTTP GET typique au niveau de la couche application, Bob enverra plus de messages et effectuera le ratchet en premier en initiant l'échange de clés ; le diagramme ci-dessous le montre. Quand Alice effectue le ratchet, la même chose se produit en sens inverse.

Le premier jeu de tags utilisé après la négociation NS/NSR est le jeu de tags 0. Lorsque le jeu de tags 0 est presque épuisé, de nouvelles clés doivent être échangées dans les deux directions pour créer le jeu de tags 1. Après cela, une nouvelle clé n'est envoyée que dans une seule direction.

Pour créer l'ensemble de balises 2, l'expéditeur de balises envoie une nouvelle clé et le destinataire de balises envoie l'ID de son ancienne clé en guise d'accusé de réception. Les deux parties effectuent un DH.

Pour créer le jeu de tags 3, l'expéditeur de tag envoie l'ID de son ancienne clé et demande une nouvelle clé au destinataire de tag. Les deux côtés effectuent un DH.

Les ensembles de balises suivants sont générés comme pour les ensembles de balises 2 et 3. Le numéro de l'ensemble de balises est (1 + ID de clé de l'expéditeur + ID de clé du destinataire).

```

Tag Sender                    Tag Receiver

                   ... use tag set #0 ...


  (Tagset #0 almost empty)
  (generate new key #0)

  Next Key, forward, request reverse, with key #0  -------->
  (repeat until next key received)

                              (generate new key #0, do DH, create IB Tagset #1)

          <-------------      Next Key, reverse, with key #0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #1)


                   ... use tag set #1 ...


  (Tagset #1 almost empty)
  (generate new key #1)

  Next Key, forward, with key #1        -------->
  (repeat until next key received)

                              (reuse key #0, do DH, create IB Tagset #2)

          <--------------     Next Key, reverse, id 0
                              (repeat until tag received on new tagset)

  (do DH, create OB Tagset #2)


                   ... use tag set #2 ...


  (Tagset #2 almost empty)
  (reuse key #1)

  Next Key, forward, request reverse, id 1  -------->
  (repeat until next key received)

                              (generate new key #1, do DH, create IB Tagset #3)

          <--------------     Next Key, reverse, with key #1

  (do DH, create OB Tagset #3)
  (reuse key #1, do DH, create IB Tagset #3)


                   ... use tag set #3 ...


       After tag set 3, repeat the above
       patterns as shown for tag sets 2 and 3.

       To create a new even-numbered tag set, the sender sends a new key
       to the receiver. The receiver sends his old key ID
       back as an acknowledgement.

       To create a new odd-numbered tag set, the sender sends a reverse request
       to the receiver. The receiver sends a new reverse key to the sender.

```
Après que le ratchet DH est terminé pour un tagset sortant, et qu'un nouveau tagset sortant est créé, il devrait être utilisé immédiatement, et l'ancien tagset sortant peut être supprimé.

Après que le ratchet DH est terminé pour un tagset entrant, et qu'un nouveau tagset entrant est créé, le récepteur devrait écouter les tags dans les deux tagsets, et supprimer l'ancien tagset après un court délai, environ 3 minutes.

Le résumé de la progression de l'ensemble de balises et de l'ID de clé est dans le tableau ci-dessous. * indique qu'une nouvelle clé est générée.

| New Tag Set ID | Sender key ID | Rcvr key ID |
|----------------|---------------|-------------|
| 0              | n/a           | n/a         |
| 1              | 0 *           | 0 *         |
| 2              | 1 *           | 0           |
| 3              | 1             | 1 *         |
| 4              | 2 *           | 1           |
| 5              | 2             | 2 *         |
| ...            | ...           | ...         |
| 65534          | 32767 *       | 32766       |
| 65535          | 32767         | 32767 *     |
Les numéros d'ID des ensembles de clés et d'étiquettes doivent être séquentiels.

#### DH INITIALIZATION KDF

Ceci est la définition de DH_INITIALIZE(rootKey, k) pour une seule direction. Elle crée un tagset, et une "clé racine suivante" à utiliser pour un ratchet DH ultérieur si nécessaire.

Nous utilisons l'initialisation DH à trois endroits. Premièrement, nous l'utilisons pour générer un ensemble de tags pour les New Session Replies. Deuxièmement, nous l'utilisons pour générer deux ensembles de tags, un pour chaque direction, destinés aux messages Existing Session. Enfin, nous l'utilisons après un DH Ratchet pour générer un nouvel ensemble de tags dans une seule direction pour des messages Existing Session supplémentaires.

```

Inputs:
  1) rootKey = chainKey from Payload Section
  2) k from the New Session KDF or split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Output 1: The next Root Key (KDF input for the next DH ratchet)
  nextRootKey = keydata[0:31]
  // Output 2: The chain key to initialize the new
  // session tag and symmetric key ratchets
  // for the tag set
  ck = keydata[32:63]

  // session tag and symmetric key chain keys
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

```
#### DH RATCHET KDF

Ceci est utilisé après l'échange de nouvelles clés DH dans les blocs NextKey, avant qu'un tagset soit épuisé.

```


// Tag sender generates new X25519 ephemeral keys
  // and sends rapk to tag receiver in a NextKey block
  rask = GENERATE_PRIVATE()
  rapk = DERIVE_PUBLIC(rask)
  
  // Tag receiver generates new X25519 ephemeral keys
  // and sends rbpk to Tag sender in a NextKey block
  rbsk = GENERATE_PRIVATE()
  rbpk = DERIVE_PUBLIC(rbsk)

  sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
  tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
  rootKey = nextRootKey // from previous tagset in this direction
  newTagSet = DH_INITIALIZE(rootKey, tagsetKey)

```
### Numéros de Message

Ratchets pour chaque message, comme dans Signal. Le ratchet de tag de session est synchronisé avec le ratchet de clé symétrique, mais le ratchet de clé du récepteur peut "prendre du retard" pour économiser la mémoire.

Le transmetteur effectue un ratchet une fois pour chaque message transmis. Aucune étiquette supplémentaire ne doit être stockée. Le transmetteur doit également maintenir un compteur pour 'N', le numéro de message du message dans la chaîne actuelle. La valeur 'N' est incluse dans le message envoyé. Voir la définition du bloc Message Number.

Le récepteur doit avancer le ratchet de la taille maximale de la fenêtre et stocker les tags dans un "tag set", qui est associé à la session. Une fois reçu, le tag stocké peut être supprimé, et s'il n'y a pas de tags non reçus précédents, la fenêtre peut être avancée. Le récepteur devrait conserver la valeur 'N' associée à chaque tag de session, et vérifier que le numéro dans le message envoyé correspond à cette valeur. Voir la définition du bloc Message Number.

#### KDF

Ceci est la définition de RATCHET_TAG().

```

Inputs:
  1) Session Tag Chain key sessTag_ck
     First time: output from DH ratchet
     Subsequent times: output from previous session tag ratchet

  Generated:
  2) input_key_material = SESSTAG_CONSTANT
     Must be unique for this tag set (generated from chain key),
     so that the sequence isn't predictable, since session tags
     go out on the wire in plaintext.

  Outputs:
  1) N (the current session tag number)
  2) the session tag (and symmetric key, probably)
  3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

  Initialization:
  keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
  // Output 1: Next chain key
  sessTag_chainKey = keydata[0:31]
  // Output 2: The constant
  SESSTAG_CONSTANT = keydata[32:63]

  // KDF_ST(ck, constant)
  keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_0 = keydata_0[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_0 = keydata_0[32:39]

  // repeat as necessary to get to tag_n
  keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
  // Output 1: Next chain key
  sessTag_chainKey_n = keydata_n[0:31]
  // Output 2: The session tag
  // or more if tag is longer than 8 bytes
  tag_n = keydata_n[32:39]

```
### Implémentation exemple

Ratchets pour chaque message, comme dans Signal. Chaque clé symétrique a un numéro de message et une étiquette de session associés. Le ratchet de clé de session est synchronisé avec le ratchet d'étiquette symétrique, mais le ratchet de clé du destinataire peut "prendre du retard" pour économiser la mémoire.

Les ratchets de transmission avancent d'un cran pour chaque message transmis. Aucune clé supplémentaire ne doit être stockée.

Lorsque le destinataire reçoit un session tag, s'il n'a pas déjà fait avancer le ratchet de clé symétrique jusqu'à la clé associée, il doit "rattraper" jusqu'à la clé associée. Le destinataire mettra probablement en cache les clés pour tous les tags précédents qui n'ont pas encore été reçus. Une fois reçue, la clé stockée peut être supprimée, et s'il n'y a pas de tags précédents non reçus, la fenêtre peut être avancée.

Pour l'efficacité, les cliquets des balises de session et des clés symétriques sont séparés afin que le cliquet des balises de session puisse avancer par rapport au cliquet des clés symétriques. Cela offre également une sécurité supplémentaire, puisque les balises de session circulent sur le réseau.

#### KDF

Ceci est la définition de RATCHET_KEY().

```

Inputs:
  1) Symmetric Key Chain key symmKey_ck
     First time: output from DH ratchet
     Subsequent times: output from previous symmetric key ratchet

  Generated:
  2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
     No need for uniqueness. Symmetric keys never go out on the wire.
     TODO: Set a constant anyway?

  Outputs:
  1) N (the current session key number)
  2) the session key
  3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

  // KDF_CK(ck, constant)
  SYMMKEY_CONSTANT = ZEROLEN
  // Output 1: Next chain key
  keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  symmKey_chainKey_0 = keydata_0[0:31]
  // Output 2: The symmetric key
  k_0 = keydata_0[32:63]

  // repeat as necessary to get to k[n]
  keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
  // Output 1: Next chain key
  symmKey_chainKey_n = keydata_n[0:31]
  // Output 2: The symmetric key
  k_n = keydata_n[32:63]


```
### 4a) Cliquet DH

Cela remplace le format de section AES défini dans la spécification ElGamal/AES+SessionTags.

Ceci utilise le même format de bloc que celui défini dans la spécification [NTCP2](/docs/specs/ntcp2/). Les types de blocs individuels sont définis différemment.

Il existe des préoccupations selon lesquelles encourager les implémenteurs à partager du code pourrait entraîner des problèmes d'analyse syntaxique. Les implémenteurs devraient soigneusement considérer les avantages et les risques du partage de code, et s'assurer que les règles d'ordonnancement et de blocs valides sont différentes pour les deux contextes.

### Payload Section Decrypted data

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. Tous les types de blocs sont pris en charge. Le contenu typique inclut les blocs suivants :

| Payload Block Type | Type Number | Block Length |
|--------------------|-------------|--------------|
| DateTime           | 0           | 7            |
| Termination (TBD)  | 4           | 9 typ.       |
| Options (TBD)      | 5           | 21+          |
| Message Number (TBD) | 6           | TBD          |
| Next Key           | 7           | 3 or 35      |
| ACK                | 8           | 4 typ.       |
| ACK Request        | 9           | 3            |
| Garlic Clove       | 11          | varies       |
| Padding            | 254         | varies       |
### Unencrypted data

Il y a zéro ou plusieurs blocs dans la trame chiffrée. Chaque bloc contient un identifiant d'un octet, une longueur de deux octets, et zéro ou plusieurs octets de données.

Pour l'extensibilité, les récepteurs DOIVENT ignorer les blocs avec des numéros de type inconnus, et les traiter comme du remplissage.

Les données chiffrées ont une taille maximale de 65535 octets, incluant un en-tête d'authentification de 16 octets, donc la taille maximale des données non chiffrées est de 65519 octets.

(Tag d'authentification Poly1305 non affiché) :

```

+----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |blk |  size   |       data             |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  ~               .   .   .               ~

  blk :: 1 byte
         0 datetime
         1-3 reserved
         4 termination
         5 options
         6 previous message number
         7 next session key
         8 ack
         9 ack request
         10 reserved
         11 Garlic Clove
         224-253 reserved for experimental features
         254 for padding
         255 reserved for future extension
  size :: 2 bytes, big endian, size of data to follow, 0 - 65516
  data :: the data

  Maximum ChaChaPoly frame is 65535 bytes.
  Poly1305 tag is 16 bytes
  Maximum total block size is 65519 bytes
  Maximum single block size is 65519 bytes
  Block type is 1 byte
  Block length is 2 bytes
  Maximum single block data size is 65516 bytes.

```
### Block Ordering Rules

Dans le message New Session, le bloc DateTime est requis et doit être le premier bloc.

Autres blocs autorisés :

- Garlic Clove (type 11)
- Options (type 5)
- Padding (type 254)

Dans le message New Session Reply, aucun bloc n'est requis.

Autres blocs autorisés :

- Garlic Clove (type 11)
- Options (type 5)
- Padding (type 254)

Aucun autre bloc n'est autorisé. Le padding, s'il est présent, doit être le dernier bloc.

Dans le message Existing Session, aucun bloc n'est requis, et l'ordre n'est pas spécifié, sauf pour les exigences suivantes :

La terminaison, si présente, doit être le dernier bloc excepté pour le remplissage. Le remplissage, s'il est présent, doit être le dernier bloc.

Il peut y avoir plusieurs blocs Garlic Clove dans une seule trame. Il peut y avoir jusqu'à deux blocs Next Key dans une seule trame. Plusieurs blocs Padding ne sont pas autorisés dans une seule trame. Les autres types de blocs n'auront probablement pas plusieurs blocs dans une seule trame, mais ce n'est pas interdit.

### DateTime

Une expiration. Aide à la prévention de réponse. Bob doit valider que le message est récent, en utilisant cet horodatage. Bob doit implémenter un filtre de Bloom ou un autre mécanisme pour prévenir les attaques par rejeu, si le temps est valide. Généralement inclus uniquement dans les messages New Session.

```

+----+----+----+----+----+----+----+
  | 0  |    4    |     timestamp     |
  +----+----+----+----+----+----+----+

  blk :: 0
  size :: 2 bytes, big endian, value = 4
  timestamp :: Unix timestamp, unsigned seconds.
               Wraps around in 2106

```
### 4b) Cliquet des étiquettes de session

Un seul Garlic Clove déchiffré tel que spécifié dans [I2NP](/docs/specs/i2np/), avec des modifications pour supprimer les champs inutilisés ou redondants. Attention : Ce format est significativement différent de celui pour ElGamal/AES. Chaque clove est un bloc de charge utile séparé. Les Garlic Cloves ne peuvent pas être fragmentés entre les blocs ou entre les trames ChaChaPoly.

```

+----+----+----+----+----+----+----+----+
  | 11 |  size   |                        |
  +----+----+----+                        +
  |      Delivery Instructions            |
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |type|  Message_ID       | Expiration   
  +----+----+----+----+----+----+----+----+
       |      I2NP Message body           |
  +----+                                  +
  ~                                       ~
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  size :: size of all data to follow

  Delivery Instructions :: As specified in
         the Garlic Clove section of [I2NP](/docs/specs/i2np/).
         Length varies but is typically 1, 33, or 37 bytes

  type :: I2NP message type

  Message_ID :: 4 byte `Integer` I2NP message ID

  Expiration :: 4 bytes, seconds since the epoch

```
Notes :

- Les implémenteurs doivent s'assurer que lors de la lecture d'un bloc,
  des données malformées ou malveillantes ne causeront pas de débordements
  de lecture dans le bloc suivant.

- Le format Clove Set spécifié dans [I2NP](/docs/specs/i2np/) n'est pas utilisé.
  Chaque clove est contenu dans son propre bloc.

- L'en-tête du message I2NP fait 9 octets, avec un format identique
  à celui utilisé dans [NTCP2](/docs/specs/ntcp2/).

- Le Certificate, Message ID et Expiration de la
  définition du Garlic Message dans [I2NP](/docs/specs/i2np/) ne sont pas inclus.

- Le Certificate, Clove ID, et Expiration de la
  définition Garlic Clove dans [I2NP](/docs/specs/i2np/) ne sont pas inclus.

Justification :

- Les certificats n'ont jamais été utilisés.
- L'ID de message séparé et les ID de clove séparés n'ont jamais été utilisés.
- Les expirations séparées n'ont jamais été utilisées.
- Les économies globales par rapport aux anciens formats Clove Set et Clove
  sont d'environ 35 octets pour 1 clove, 54 octets pour 2 cloves,
  et 73 octets pour 3 cloves.
- Le format de bloc est extensible et tout nouveau champ peut être ajouté
  comme nouveaux types de blocs.

### Termination

L'implémentation est optionnelle. Abandonne la session. Ceci doit être le dernier bloc non-padding dans la trame. Aucun message supplémentaire ne sera envoyé dans cette session.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de session existante.

```

+----+----+----+----+----+----+----+----+
  | 4  |  size   | rsn|     addl data     |
  +----+----+----+----+                   +
  ~               .   .   .               ~
  +----+----+----+----+----+----+----+----+

  blk :: 4
  size :: 2 bytes, big endian, value = 1 or more
  rsn :: reason, 1 byte:
         0: normal close or unspecified
         1: termination received
         others: optional, impementation-specific
  addl data :: optional, 0 or more bytes, for future expansion, debugging,
               or reason text.
               Format unspecified and may vary based on reason code.

```
### 4c) Symmetric Key Ratchet

NON IMPLÉMENTÉ, pour étude ultérieure. Passer les options mises à jour. Les options incluent divers paramètres pour la session. Voir la section Analyse de la longueur des tags de session ci-dessous pour plus d'informations.

Le bloc d'options peut avoir une longueur variable, car more_options peut être présent.

```

+----+----+----+----+----+----+----+----+
  | 5  |  size   |ver |flg |STL |STimeout |
  +----+----+----+----+----+----+----+----+
  |  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
  +----+----+----+----+----+----+----+----+
  |  tdmy   |  rdmy   |  tdelay |  rdelay |
  +----+----+----+----+----+----+----+----+
  |              more_options             |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 5
  size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
  ver :: Protocol version, must be 0
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility
  STL :: Session tag length (must be 8), other values unimplemented
  STimeout :: Session idle timeout (seconds), big endian
  SOTW :: Sender Outbound Tag Window, 2 bytes big endian
  RITW :: Receiver Inbound Tag Window 2 bytes big endian

  tmin, tmax, rmin, rmax :: requested padding limits
      tmin and rmin are for desired resistance to traffic analysis.
      tmax and rmax are for bandwidth limits.
      tmin and tmax are the transmit limits for the router sending this options block.
      rmin and rmax are the receive limits for the router sending this options block.
      Each is a 4.4 fixed-point float representing 0 to 15.9375
      (or think of it as an unsigned 8-bit integer divided by 16.0).
      This is the ratio of padding to data. Examples:
      Value of 0x00 means no padding
      Value of 0x01 means add 6 percent padding
      Value of 0x10 means add 100 percent padding
      Value of 0x80 means add 800 percent (8x) padding
      Alice and Bob will negotiate the minimum and maximum in each direction.
      These are guidelines, there is no enforcement.
      Sender should honor receiver's maximum.
      Sender may or may not honor receiver's minimum, within bandwidth constraints.

  tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
  rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
  tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
  rdelay: Requested intra-message delay, 2 bytes big endian, msec average

  more_options :: Format undefined, for future use

```
SOTW est la recommandation de l'expéditeur au destinataire pour la fenêtre de tag entrant du destinataire (l'anticipation maximale). RITW est la déclaration de l'expéditeur de la fenêtre de tag entrant (anticipation maximale) qu'il prévoit d'utiliser. Chaque côté définit ou ajuste ensuite l'anticipation basée sur un minimum ou maximum ou autre calcul.

Notes :

- Le support pour une longueur de balise de session non-par défaut ne devrait, espérons-le, jamais être requis.
- La fenêtre de balise est MAX_SKIP dans la documentation Signal.

Problèmes :

- La négociation des options est à définir.
- Les valeurs par défaut sont à définir.
- Les options de remplissage et de délai sont copiées depuis NTCP2,
  mais ces options n'ont pas été entièrement implémentées ou étudiées là-bas.

### Message Numbers

L'implémentation est optionnelle. La longueur (nombre de messages envoyés) dans le jeu de balises précédent (PN). Le récepteur peut immédiatement supprimer les balises supérieures à PN du jeu de balises précédent. Le récepteur peut faire expirer les balises inférieures ou égales à PN du jeu de balises précédent après un court délai (par exemple 2 minutes).

```

+----+----+----+----+----+
  | 6  |  size   |  PN    |
 +----+----+----+----+----+

  blk :: 6
  size :: 2
  PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.

```
Notes :

- Le PN maximum est 65535.
- Les définitions de PN sont égales à la définition Signal, moins une.
  C'est similaire à ce que fait Signal, mais dans Signal, PN et N sont dans l'en-tête.
  Ici, ils sont dans le corps du message chiffré.
- N'envoyez pas ce bloc dans le tag set 0, car il n'y avait pas de tag set précédent.

### 5) Charge utile

La prochaine clé de ratchet DH est dans la charge utile, et elle est optionnelle. Nous ne faisons pas de ratchet à chaque fois. (Ceci est différent de Signal, où elle est dans l'en-tête et envoyée à chaque fois)

Pour le premier ratchet, Key ID = 0.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de session existante.

```

+----+----+----+----+----+----+----+----+
  | 7  |  size   |flag|  key ID |         |
  +----+----+----+----+----+----+         +
  |                                       |
  +                                       +
  |     Next DH Ratchet Public Key        |
  +                                       +
  |                                       |
  +                             +----+----+
  |                             |
  +----+----+----+----+----+----+

  blk :: 7
  size :: 3 or 35
  flag :: 1 byte flags
          bit order: 76543210
          bit 0: 1 for key present, 0 for no key present
          bit 1: 1 for reverse key, 0 for forward key
          bit 2: 1 to request reverse key, 0 for no request
                 only set if bit 1 is 0
          bits 7-2: Unused, set to 0 for future compatibility
  key ID :: The key ID of this key. 2 bytes, big endian
            0 - 32767
  Public Key :: The next X25519 public key, 32 bytes, little endian
                Only if bit 0 is 1


```
Notes :

- Key ID est un compteur incrémentiel pour la clé locale utilisée pour cet ensemble de tags, commençant à 0.
- L'ID ne doit pas changer à moins que la clé ne change.
- Ce n'est peut-être pas strictement nécessaire, mais c'est utile pour le débogage.
  Signal n'utilise pas d'ID de clé.
- L'ID de clé maximum est 32767.
- Dans le cas rare où les ensembles de tags dans les deux directions font du ratcheting en
  même temps, une trame contiendra deux blocs Next Key, un pour
  la clé directe et un pour la clé inverse.
- Les numéros d'ID de clé et d'ensemble de tags doivent être séquentiels.
- Voir la section DH Ratchet ci-dessus pour les détails.

### Section Payload Données décryptées

Ceci n'est envoyé que si un bloc de demande d'ack a été reçu. Plusieurs acks peuvent être présents pour accuser réception de plusieurs messages.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de session existante.

```
+----+----+----+----+----+----+----+----+
  | 8  |  size   |tagsetid |   N     |    |
  +----+----+----+----+----+----+----+    +
  |             more acks                 |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 8
  size :: 4 * number of acks to follow, minimum 1 ack
  for each ack:
  tagsetid :: 2 bytes, big endian, from the message being acked
  N :: 2 bytes, big endian, from the message being acked


```
Notes :

- L'ID du jeu de balises et N identifient de manière unique le message accusé de réception.
- Dans les premiers jeux de balises utilisés pour une session dans chaque direction, l'ID du jeu de balises est 0.
- Aucun bloc NextKey n'a été envoyé, il n'y a donc pas d'ID de clé.
- Pour tous les jeux de balises utilisés après les échanges NextKey, le numéro du jeu de balises est (1 + ID de clé d'Alice + ID de clé de Bob).

### Données non chiffrées

Demander un accusé de réception dans la bande. Pour remplacer le message DeliveryStatus hors bande dans le Garlic Clove.

Si un accusé de réception explicite est demandé, l'ID du tagset actuel et le numéro de message (N) sont retournés dans un bloc d'accusé de réception.

Non autorisé dans NS ou NSR. Uniquement inclus dans les messages de session existante.

```

+----+----+----+----+
  |  9 |  size   |flg |
  +----+----+----+----+

  blk :: 9
  size :: 1
  flg :: 1 byte flags
         bits 7-0: Unused, set to 0 for future compatibility

```
### Règles d'ordonnancement des blocs

Tout le padding est à l'intérieur des trames AEAD. TODO Le padding à l'intérieur d'AEAD devrait approximativement adhérer aux paramètres négociés. TODO Alice a envoyé ses paramètres tx/rx min/max demandés dans le message NS. TODO Bob a envoyé ses paramètres tx/rx min/max demandés dans le message NSR. Des options mises à jour peuvent être envoyées pendant la phase de données. Voir les informations du bloc d'options ci-dessus.

S'il est présent, ce bloc doit être le dernier dans la trame.

```

+----+----+----+----+----+----+----+----+
  |254 |  size   |      padding           |
  +----+----+----+                        +
  |                                       |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  blk :: 254
  size :: 2 bytes, big endian, 0-65516
  padding :: zeros or random data

```
Notes :

- Le remplissage tout-zéro convient, car il sera chiffré.
- Les stratégies de remplissage sont à déterminer.
- Les trames de remplissage uniquement sont autorisées.
- Le remplissage par défaut est de 0-15 octets.
- Voir le bloc d'options pour la négociation des paramètres de remplissage
- Voir le bloc d'options pour les paramètres de remplissage min/max
- La réponse du router en cas de violation du remplissage négocié dépend de l'implémentation.

### DateTime

Les implémentations doivent ignorer les types de blocs inconnus pour la compatibilité ascendante.

### Gousse de Garlic

- La longueur de remplissage doit être décidée soit au cas par cas en fonction
  d'estimations de la distribution des longueurs, soit des délais aléatoires doivent être
  ajoutés. Ces contre-mesures doivent être incluses pour résister au DPI, car les tailles
  des messages révéleraient autrement que le trafic I2P est transporté par le protocole
  de transport. Le schéma de remplissage exact est un domaine de travail futur, l'Annexe A
  fournit plus d'informations sur le sujet.

## Typical Usage Patterns

### Terminaison

C'est le cas d'usage le plus typique, et la plupart des cas d'usage de streaming non-HTTP seront identiques à ce cas d'usage également. Un petit message initial est envoyé, une réponse suit, et des messages supplémentaires sont envoyés dans les deux directions.

Une requête HTTP GET tient généralement dans un seul message I2NP. Alice envoie une petite requête avec un seul nouveau message Session, regroupant un leaseset de réponse. Alice inclut un ratchet immédiat vers une nouvelle clé. Inclut une signature pour lier à la destination. Aucun accusé de réception demandé.

Bob effectue immédiatement la rotation des clés.

Alice effectue le ratchet immédiatement.

Continue avec ces sessions.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5

```
### Options

Alice a trois options :

1) Envoyer uniquement le premier message (taille de fenêtre = 1), comme dans HTTP GET. Non recommandé.

2) Envoyer jusqu'à la fenêtre de streaming, mais en utilisant la même clé publique en clair encodée Elligator2. Tous les messages contiennent la même clé publique suivante (ratchet). Ceci sera visible pour OBGW/IBEP car ils commencent tous avec le même texte en clair. Les choses se déroulent comme en 1). Non recommandé.

3) Implémentation recommandée.    Envoyer jusqu'à la fenêtre de streaming, mais en utilisant une clé publique en clair encodée Elligator2 différente (session) pour chacun.    Tous les messages contiennent la même clé publique suivante (ratchet).    Cela ne sera pas visible pour OBGW/IBEP car ils commencent tous avec un texte en clair différent.    Bob doit reconnaître qu'ils contiennent tous la même clé publique suivante,    et répondre à tous avec le même ratchet.    Alice utilise cette clé publique suivante et continue.

Flux de messages de l'Option 3 :

```

Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack

```
### Numéros de Message

Un seul message, avec une seule réponse attendue. Des messages ou réponses supplémentaires peuvent être envoyés.

Similaire à HTTP GET, mais avec des options plus petites pour la taille de fenêtre et la durée de vie des balises de session. Peut-être ne pas demander de ratchet.

```

Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message

```
### Prochaine clé publique DH Ratchet

Plusieurs messages anonymes, sans réponses attendues.

Dans ce scénario, Alice demande une session, mais sans liaison. Un nouveau message de session est envoyé. Aucun LS de réponse n'est groupé. Un DSM de réponse est groupé (c'est le seul cas d'usage qui nécessite des DSM groupés). Aucune clé suivante n'est incluse. Aucune réponse ou ratchet n'est demandé. Aucun ratchet n'est envoyé. Les options définissent la fenêtre des étiquettes de session à zéro.

```

Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->

```
### Accusé de réception

Un seul message anonyme, sans réponse attendue.

Un message unique est envoyé. Aucun LS de réponse ou DSM n'est inclus. Aucune clé suivante n'est incluse. Aucune réponse ou ratchet n'est demandé. Aucun ratchet n'est envoyé. Les options définissent la fenêtre des session tags à zéro.

```

Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message

```
### Demande d'acquittement

Les sessions de longue durée peuvent effectuer un ratchet, ou demander un ratchet, à tout moment, pour maintenir le secret de transmission parfaite à partir de ce moment-là. Les sessions doivent effectuer un ratchet lorsqu'elles approchent de la limite de messages envoyés par session (65535).

## Implementation Considerations

### Remplissage

Comme avec le protocole ElGamal/AES+SessionTag existant, les implémentations doivent limiter le stockage des balises de session et se protéger contre les attaques d'épuisement de mémoire.

Voici quelques stratégies recommandées :

- Limite stricte sur le nombre de session tags stockés
- Expiration agressive des sessions entrantes inactives en cas de pression mémoire
- Limite sur le nombre de sessions entrantes liées à une seule destination distante
- Réduction adaptative de la fenêtre de session tag et suppression des anciens tags inutilisés
  en cas de pression mémoire
- Refus d'effectuer le ratchet lorsque demandé, si sous pression mémoire

### Autres types de blocs

Paramètres recommandés et délais d'expiration :

- Taille du tagset NSR : 12 tsmin et tsmax
- Taille du tagset ES 0 : tsmin 24, tsmax 160
- Taille du tagset ES (1+) : 160 tsmin et tsmax
- Délai d'expiration du tagset NSR : 3 minutes pour le récepteur
- Délai d'expiration du tagset ES : 8 minutes pour l'expéditeur, 10 minutes pour le récepteur
- Supprimer le tagset ES précédent après : 3 minutes
- Anticipation du tagset pour le tag N : min(tsmax, tsmin + N/4)
- Élagage du tagset derrière le tag N : min(tsmax, tsmin + N/4) / 2
- Envoyer la prochaine clé au tag : TBD
- Envoyer la prochaine clé après la durée de vie du tagset : TBD
- Remplacer la session si NS reçu après : 3 minutes
- Décalage d'horloge maximum : -5 minutes à +2 minutes
- Durée du filtre de rejeu NS : 5 minutes
- Taille de remplissage : 0-15 octets (autres stratégies TBD)

### Travaux futurs

Voici les recommandations pour classifier les messages entrants.

### X25519 Only

Sur un tunnel utilisé uniquement avec ce protocole, effectuez l'identification comme cela se fait actuellement avec ElGamal/AES+SessionTags :

D'abord, traiter les données initiales comme un tag de session, et rechercher le tag de session. Si trouvé, déchiffrer en utilisant les données stockées associées à ce tag de session.

Si non trouvé, traiter les données initiales comme une clé publique DH et un nonce. Effectuer une opération DH et le KDF spécifié, puis tenter de déchiffrer les données restantes.

### HTTP GET

Sur un tunnel qui prend en charge à la fois ce protocole et ElGamal/AES+SessionTags, classifiez les messages entrants comme suit :

En raison d'un défaut dans la spécification ElGamal/AES+SessionTags, le bloc AES n'est pas complété à une longueur aléatoire non-mod-16. Par conséquent, la longueur des messages de Session Existante mod 16 est toujours 0, et la longueur des messages de Nouvelle Session mod 16 est toujours 2 (puisque le bloc ElGamal fait 514 octets de long).

Si la longueur mod 16 n'est pas 0 ou 2, traiter les données initiales comme un session tag, et rechercher le session tag. Si trouvé, déchiffrer en utilisant les données stockées associées à ce session tag.

Si non trouvé, et si la longueur mod 16 n'est pas 0 ou 2, traiter les données initiales comme une clé publique DH et un nonce. Effectuer une opération DH et la KDF spécifiée, et tenter de déchiffrer les données restantes. (basé sur le mélange de trafic relatif, et les coûts relatifs des opérations DH X25519 et ElGamal, cette étape peut être effectuée en dernier à la place)

Sinon, si la longueur modulo 16 est égale à 0, traiter les données initiales comme un tag de session ElGamal/AES, et rechercher le tag de session. Si trouvé, déchiffrer en utilisant les données stockées associées à ce tag de session.

Si non trouvé, et que les données font au moins 642 (514 + 128) octets de long, et que la longueur modulo 16 est 2, traiter les données initiales comme un bloc ElGamal. Tenter de déchiffrer les données restantes.

Notez que si la spécification ElGamal/AES+SessionTag est mise à jour pour permettre un padding non-mod-16, les choses devront être faites différemment.

### HTTP POST

Les implémentations initiales s'appuient sur le trafic bidirectionnel aux couches supérieures. C'est-à-dire que les implémentations supposent que le trafic dans la direction opposée sera bientôt transmis, ce qui forcera toute réponse requise au niveau de la couche ECIES.

Cependant, certains trafics peuvent être unidirectionnels ou de très faible bande passante, de sorte qu'il n'y a pas de trafic de couche supérieure pour générer une réponse en temps opportun.

La réception des messages NS et NSR nécessite une réponse ; la réception des blocs ACK Request et Next Key nécessite également une réponse.

Une implémentation sophistiquée peut démarrer un minuteur lorsqu'un de ces messages nécessitant une réponse est reçu, et générer une réponse "vide" (sans bloc Garlic Clove) au niveau de la couche ECIES si aucun trafic de retour n'est envoyé dans une courte période de temps (par exemple 1 seconde).

Il peut également être approprié d'utiliser un délai d'expiration encore plus court pour les réponses aux messages NS et NSR, afin de rediriger le trafic vers les messages ES plus efficaces dès que possible.

## Analysis

### Datagramme avec Réponse

La surcharge de message pour les deux premiers messages dans chaque direction est la suivante. Ceci suppose seulement un message dans chaque direction avant l'ACK, ou que tous les messages supplémentaires sont envoyés de manière spéculative comme des messages de Session Existante. S'il n'y a pas d'accusés de réception spéculatifs des balises de session livrées, la surcharge ou l'ancien protocole est beaucoup plus élevée.

Aucun padding n'est supposé pour l'analyse du nouveau protocole. Aucun leaseSet groupé n'est supposé.

### Datagrammes Bruts Multiples

Message de nouvelle session, identique dans chaque direction :

```

ElGamal block:
  514 bytes

  AES block:
  - 2 byte tag count
  - 1024 bytes of tags (32 typical)
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte clove cert, id, exp.
  - 15 byte msg cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  1143 total

  Total:
  1657 bytes
```
Messages de session existants, identiques dans chaque direction :

```

AES block:
  - 32 byte session tag
  - 2 byte tag count
  - 4 byte payload size
  - 32 byte hash of payload
  - 1 byte flags
  - 1 byte clove count
  - 33 byte Garlic deliv. inst.
  - 16 byte I2NP header
  - 15 byte msg cert, id, exp.
  - 15 byte clove cert, id, exp.
  - 0 byte padding assuming 1936 byte message
  151 total
```
```
Four message total (two each direction)
  3616 bytes overhead
```
### Datagramme Brut Simple

Message de Nouvelle Session Alice-vers-Bob :

```

- 32 byte ephemeral public key
  - 32 byte static public key
  - 16 byte Poly1305 MAC
  - 7 byte DateTime block
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  148 bytes overhead
```
Message de réponse de nouvelle session de Bob vers Alice :

```

- 8 byte session tag
  - 32 byte ephemeral public key
  - 16 byte Poly1305 MAC
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  117 bytes overhead
```
Messages de session existants, identiques dans chaque direction :

```

- 8 byte session tag
  - 3 byte Garlic block overhead
  - 9 byte I2NP header
  - 33 byte Garlic deliv. inst.
  - 16 byte Poly1305 MAC

  Total:
  69 bytes
```
### Sessions de Longue Durée

Quatre messages au total (deux dans chaque direction) :

```

372 bytes
  90% (approx. 10x) reduction compared to ElGamal/AES+SessionTags
```
Handshake uniquement :

```

ElGamal: 1657 + 1657 = 3314 bytes
  Ratchet: 148 _ 117 = 265 bytes
  92% (approx. 12x) reduction compared to ElGamal/AES+SessionTags
```
Total à long terme (sans tenir compte des négociations) :

```
ElGamal: 151 + 32 byte tag sent previously = 183 bytes
  Ratchet: 69 bytes
  64% (approx. 3x) reduction compared to ElGamal/AES+SessionTags
```
### CPU

TODO mettre à jour cette section une fois la proposition stabilisée.

Les opérations cryptographiques suivantes sont requises par chaque partie pour échanger les messages New Session et New Session Reply :

- HMAC-SHA256 : 3 par HKDF, total à déterminer
- ChaChaPoly : 2 chacun
- Génération de clé X25519 : 2 Alice, 1 Bob
- X25519 DH : 3 chacun
- Vérification de signature : 1 (Bob)

Alice calcule 5 ECDH par session liée (minimum), 2 pour chaque message NS vers Bob, et 3 pour chacun des messages NSR de Bob.

Bob calcule également 6 ECDHs par session liée, 3 pour chacun des messages NS d'Alice, et 3 pour chacun de ses messages NSR.

Les opérations cryptographiques suivantes sont requises par chaque partie pour chaque message de Session Existante :

- HKDF : 2
- ChaChaPoly : 1

### Défense

La longueur actuelle des session tags est de 32 octets. Nous n'avons pas encore trouvé de justification pour cette longueur, mais nous continuons à rechercher dans les archives. La proposition ci-dessus définit la nouvelle longueur des tags à 8 octets. L'analyse justifiant un tag de 8 octets est la suivante :

Le ratchet de session tag est supposé générer des tags aléatoires, distribués uniformément. Il n'y a aucune raison cryptographique pour une longueur particulière de session tag. Le ratchet de session tag est synchronisé avec, mais génère une sortie indépendante de, le ratchet de clé symétrique. Les sorties des deux ratchets peuvent avoir des longueurs différentes.

Par conséquent, la seule préoccupation est la collision de tags de session. Il est supposé que les implémentations ne tenteront pas de gérer les collisions en essayant de déchiffrer avec les deux sessions ; les implémentations associeront simplement le tag soit à la session précédente, soit à la nouvelle session, et tout message reçu avec ce tag sur l'autre session sera abandonné après l'échec du déchiffrement.

L'objectif est de sélectionner une longueur de balise de session suffisamment grande pour minimiser le risque de collisions, tout en étant suffisamment petite pour minimiser l'utilisation de la mémoire.

Ceci suppose que les implémentations limitent le stockage des étiquettes de session pour prévenir les attaques d'épuisement de mémoire. Cela réduira également considérablement les chances qu'un attaquant puisse créer des collisions. Voir la section Considérations d'implémentation ci-dessous.

Pour un cas le plus défavorable, supposons un serveur très occupé avec 64 nouvelles sessions entrantes par seconde. Supposons une durée de vie des session tags entrants de 15 minutes (comme actuellement, devrait probablement être réduite). Supposons une fenêtre de session tags entrants de 32. 64 * 15 * 60 * 32 = 1 843 200 tags Le maximum actuel de tags entrants dans Java I2P est de 750 000 et n'a jamais été atteint à notre connaissance.

Un objectif d'une collision de tag de session sur un million (1e-6) est probablement suffisant. La probabilité de perdre un message en cours de route en raison de la congestion est bien plus élevée que cela.

Réf : https://en.wikipedia.org/wiki/Birthday_paradox section Tableau de probabilités.

Avec des session tags de 32 octets (256 bits), l'espace des session tags est de 1,2e77. La probabilité d'une collision avec une probabilité de 1e-18 nécessite 4,8e29 entrées. La probabilité d'une collision avec une probabilité de 1e-6 nécessite 4,8e35 entrées. 1,8 million de tags de 32 octets chacun représente environ 59 MB au total.

Avec des session tags de 16 octets (128 bits), l'espace des session tags est de 3,4e38. La probabilité d'une collision avec une probabilité de 1e-18 nécessite 2,6e10 entrées. La probabilité d'une collision avec une probabilité de 1e-6 nécessite 2,6e16 entrées. 1,8 million de tags de 16 octets chacun représente environ 30 Mo au total.

Avec des session tags de 8 octets (64 bits), l'espace des session tags est de 1,8e19. La probabilité d'une collision avec une probabilité de 1e-18 nécessite 6,1 entrées. La probabilité d'une collision avec une probabilité de 1e-6 nécessite 6,1e6 (6 100 000) entrées. 1,8 million de tags de 8 octets chacun représente environ 15 Mo au total.

6,1 millions de tags actifs représentent plus de 3 fois notre estimation pessimiste de 1,8 million de tags. Donc la probabilité de collision serait inférieure à une sur un million. Nous concluons par conséquent que des session tags de 8 octets sont suffisants. Cela résulte en une réduction d'espace de stockage de 4x, en plus de la réduction de 2x parce que les tags de transmission ne sont pas stockés. Nous aurons donc une réduction de 8x de l'utilisation mémoire des session tags comparé à ElGamal/AES+SessionTags.

Pour maintenir la flexibilité au cas où ces hypothèses seraient erronées, nous inclurons un champ de longueur de session tag dans les options, afin que la longueur par défaut puisse être remplacée sur une base par session. Nous ne nous attendons pas à implémenter une négociation dynamique de longueur de tag à moins que ce ne soit absolument nécessaire.

Les implémentations devraient, au minimum, reconnaître les collisions de session tag, les gérer de manière élégante, et enregistrer ou compter le nombre de collisions. Bien qu'encore extrêmement improbables, elles seront beaucoup plus probables qu'elles ne l'étaient pour ElGamal/AES+SessionTags, et pourraient effectivement se produire.

### Paramètres

En utilisant deux fois plus de sessions par seconde (128) et deux fois plus de fenêtre de tag (64), nous avons 4 fois plus de tags (7,4 millions). Le maximum pour une chance de collision sur un million est de 6,1 millions de tags. Des tags de 12 octets (ou même 10 octets) ajouteraient une marge énorme.

Cependant, est-ce qu'une chance de collision d'un sur un million est un bon objectif ? Bien plus importante que la chance d'être abandonné en cours de route n'est pas très utile. La cible de faux positifs pour le DecayingBloomFilter de Java est d'environ 1 sur 10 000, mais même 1 sur 1000 n'est pas préoccupant. En réduisant la cible à 1 sur 10 000, il y a une marge suffisante avec des tags de 8 octets.

### Classification

L'expéditeur génère les balises et les clés à la volée, il n'y a donc pas de stockage. Cela réduit de moitié les exigences globales de stockage par rapport à ElGamal/AES. Les balises ECIES font 8 octets au lieu de 32 pour ElGamal/AES. Cela réduit les exigences globales de stockage d'un facteur de 4 supplémentaire. Les clés de session par balise ne sont pas stockées au niveau du récepteur sauf pour les "lacunes", qui sont minimales pour des taux de perte raisonnables.

La réduction de 33% du temps d'expiration des étiquettes crée une économie supplémentaire de 33%, en supposant des durées de session courtes.

Par conséquent, l'économie d'espace totale par rapport à ElGamal/AES est d'un facteur de 10,7, soit 92%.

## Related Changes

### X25519 uniquement

Recherches dans la base de données depuis les destinations ECIES : Voir la [Proposition 154](/proposals/154-ecies-lookups), désormais incorporée dans [I2NP](/docs/specs/i2np/) pour la version 0.9.46.

Cette proposition nécessite le support LS2 pour publier la clé publique X25519 avec le leaseSet. Aucune modification n'est requise pour les spécifications LS2 dans [I2NP](/docs/specs/i2np/). Tout le support a été conçu, spécifié et implémenté dans la [Proposition 123](/proposals/123-new-netdb-entries) implémentée dans la version 0.9.38.

### X25519 partagé avec ElGamal/AES+SessionTags

Aucune. Cette proposition nécessite la prise en charge de LS2, et qu'une propriété soit définie dans les options I2CP pour être activée. Aucune modification n'est requise pour les spécifications [I2CP](/docs/specs/i2cp/). Toute la prise en charge a été conçue, spécifiée et implémentée dans la [Proposition 123](/proposals/123-new-netdb-entries) implémentée dans la version 0.9.38.

L'option requise pour activer ECIES est une seule propriété I2CP pour I2CP, BOB, SAM, ou i2ptunnel.

Les valeurs typiques sont i2cp.leaseSetEncType=4 pour ECIES uniquement, ou i2cp.leaseSetEncType=4,0 pour les clés doubles ECIES et ElGamal.

### Réponses de la couche protocole

Cette section est copiée de la [Proposition 123](/proposals/123-new-netdb-entries).

Option dans le mapping SessionConfig :

```
  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  0: ElGamal
                                  1-3: See proposal 145
                                  4: This proposal.
```
### Create Leaseset2 Message

Cette proposition nécessite LS2 qui est pris en charge depuis la version 0.9.38. Aucune modification n'est requise pour les spécifications [I2CP](/docs/specs/i2cp/). Tout le support a été conçu, spécifié et implémenté dans la [Proposition 123](/proposals/123-new-netdb-entries) implémentée dans la version 0.9.38.

### Surcharge

Tout router prenant en charge LS2 avec des clés duales (0.9.38 ou supérieur) devrait prendre en charge la connexion aux destinations avec des clés duales.

Les destinations ECIES uniquement nécessiteront qu'une majorité des floodfills soient mis à jour vers la version 0.9.46 pour obtenir des réponses de recherche chiffrées. Voir [Proposition 154](/proposals/154-ecies-lookups).

Les destinations ECIES uniquement peuvent seulement se connecter avec d'autres destinations qui sont soit ECIES uniquement, soit à double clé.
