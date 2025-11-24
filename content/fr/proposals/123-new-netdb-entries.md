```markdown
---
title: "Nouvelles entrées netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Open"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Statut

Des parties de cette proposition sont complètes et implémentées dans les versions 0.9.38 et 0.9.39.
Les Structures Communes, I2CP, I2NP et autres spécifications
sont maintenant mises à jour pour refléter les changements qui sont actuellement supportés.

Les parties complétées sont toujours sujettes à des révisions mineures.
D'autres parties de cette proposition sont toujours en développement
et peuvent être soumises à des révisions substantielles.

La Recherche de Service (types 9 et 11) est à faible priorité et
non programmée, et pourrait être séparée dans une proposition distincte.


## Aperçu

Ceci est une mise à jour et une agrégation des 4 propositions suivantes :

- 110 LS2
- 120 Meta LS2 pour un multi-domiciliation massive
- 121 LS2 chiffré
- 122 Recherche de service non authentifiée (anycasting)

Ces propositions sont principalement indépendantes, mais pour la cohérence, nous définissons et utilisons un
format commun pour plusieurs d'entre elles.

Les propositions suivantes sont quelque peu liées :

- 140 Multi-domiciliation invisible (incompatible avec cette proposition)
- 142 Nouveau modèle Crypto (pour la nouvelle crypto symétrique)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 pour LS2 chiffré
- 150 Protocole Garlic Farm
- 151 ECDSA Blinding


## Proposition

Cette proposition définit 5 nouveaux types d'entrée de base de données et le processus de
stockage et de récupération à partir de la base de données du réseau,
ainsi que la méthode pour les signer et vérifier ces signatures.

### Objectifs

- Compatible avec les versions antérieures
- LS2 utilisable avec l'ancienne méthode de multi-domiciliation
- Aucune nouvelle crypto ou primitives requises pour le support
- Maintenir le découplage de la crypto et de la signature; supporte toutes les versions actuelles et futures
- Autoriser des clés de signature hors-ligne optionnelles
- Réduire la précision des horodatages pour réduire l'empreinte
- Activer la nouvelle crypto pour les destinations
- Activer le multi-domiciliation massive
- Corriger plusieurs problèmes avec les LS chiffrés existants
- Blindage optionnel pour réduire la visibilité par les inondations
- LS chiffré supporte à la fois une clé unique et plusieurs clés révocables
- Recherche de service pour faciliter les recherches de proxys de sortie, bootstrap DHT applicatif,
  et autres usages
- Ne rien casser qui repose sur des hachages de destination binaire de 32 octets, par ex. bittorrent
- Ajouter de la flexibilité aux sets de location via des propriétés, comme nous en avons dans routerinfos.
- Mettre l'horodatage publié et l'expiration variable dans l'entête, de sorte à ce que cela fonctionne même
  si le contenu est chiffré (ne pas dériver l'horodatage du premier lease)
- Tous les nouveaux types vivent dans le même espace DHT et les mêmes emplacements que les sets de location existants,
  de sorte que les utilisateurs puissent migrer de l'ancien LS à LS2,
  ou changer entre LS2, Meta, et Encrypté,
  sans changer la Destination ou le hachage.
- Une Destination existante peut être convertie pour utiliser des clés hors-ligne,
  ou revenir à des clés en ligne, sans changer la Destination ou le hachage.


### Non-objectifs / Hors périmètre

- Nouveau algorithme de rotation DHT ou génération aléatoire partagée
- Le type de chiffrement spécifique et le schéma de chiffrement de bout en bout
  utilisant ce nouveau type serait dans une proposition séparée.
  Aucune nouvelle crypto n'est spécifiée ou discutée ici.
- Nouveau chiffrement pour les RIs ou la construction de tunnel.
  Cela serait dans une proposition séparée.
- Méthodes de chiffrement, transmission, et réception des messages I2NP DLM / DSM / DSRM.
  Pas de changement.
- Comment générer et supporter Meta, y compris la communication inter-routeurs backend, la gestion, le basculement et la coordination.
  Le support peut être ajouté à I2CP ou i2pcontrol ou un nouveau protocole.
  Cela peut ou ne peut pas être standardisé.
- Comment implémenter et gérer des tunnels avec une expiration plus longue, ou annuler les tunnels existants.
  C'est extrêmement difficile, et sans lui, vous ne pouvez pas avoir un arrêt en douceur raisonnable.
- Changements au modèle de menace
- Format de stockage hors-ligne, ou méthodes pour stocker/récupérer/partager les données.
- Les détails de l'implémentation ne sont pas discutés ici et sont laissés à chaque projet.



### Justification

LS2 ajoute des champs pour changer le type de chiffrement et pour des changements de protocole futurs.

LS2 chiffré corrige plusieurs problèmes de sécurité avec le LS chiffré existant en
utilisant le chiffrement asymétrique de l'ensemble des leases.

Meta LS2 offre une solution flexible, efficace, efficace, et à grande échelle de multi-domiciliation.

Service Record et Service List fournissent des services anycast tels que la recherche de nom
et le bootstrap de DHT.


### Types de données NetDB

Les numéros de type sont utilisés dans les messages de Lookup/Store de la base de données I2NP.

La colonne de bout en bout fait référence à si oui ou non les requêtes/réponses sont envoyées à une Destination dans un message Garlic.


Types existants :

            Données NetDB           Type Lookup   Type Store 
any                                       0           any     
LS                                        1            1      
RI                                        2            0      
exploratory                               3           DSRM    

Nouveaux types :

            Données NetDB           Type Lookup   Type Store   Entête LS2 Std.?   Envoyé de bout en bout ?
LS2                                       1            3             yes                 yes
LS2 chiffré                               1            5             no                  no
Meta LS2                                  1            7             yes                 no
Service Record                           n/a           9             yes                 no
Service List                              4           11             no                  no



Notes
`````
- Les types de Lookup sont actuellement les bits 3-2 dans le message de Database Lookup.
  Tout type additionnel nécessiterait l'utilisation du bit 4.

- Tous les types de store sont impairs puisque les bits supérieurs dans le champ de type de message de Database Store
  sont ignorés par les anciens routeurs.
  Nous préférerions que l'analyse échoue en tant que LS plutôt qu'en tant que RI compressé.

- Le type doit-il être explicite ou implicite ou ni l'un ni l'autre dans les données couvertes par la signature ?



### Processus de Lookup/Store

Les types 3, 5, et 7 peuvent être retournés en réponse à un Lookup de leaseset standard (type 1).
Le type 9 n'est jamais retourné en réponse à un Lookup.
Le type 11 est retourné en réponse à un nouveau type de Lookup de service (type 11).

Seul le type 3 peut être envoyé dans un message Garlic client-à-client.



### Format

Les types 3, 7, et 9 ont tous un format commun :

  Entête LS2 Standard
  - tel que défini ci-dessous

  Partie spécifique au Type
  - tel que défini ci-dessous dans chaque partie

  Signature LS2 Standard :
  - Longueur telle qu'impliquée par le type de sig de la clé de signature

Le type 5 (Encrypté) ne commence pas avec une Destination et a un
format différent. Voir ci-dessous.

Le type 11 (Service List) est une agrégation de plusieurs Service Records et a un
format différent. Voir ci-dessous.


### Considérations sur la confidentialité/sécurité

TBD



## Entête LS2 Standard

Les types 3, 7, et 9 utilisent l'entête LS2 standard, spécifié ci-dessous :


### Format
::

  Entête LS2 Standard :
  - Type (1 octet)
    Pas réellement dans l'entête, mais partie des données couvertes par la signature.
    Pris du champ du message de Database Store.
  - Destination (387+ octets)
  - Horodatage publié (4 octets, big endian, secondes depuis l'époque, se réinitialise en 2106)
  - Expire (2 octets, big endian) (décalage de secondes par rapport à l'horodatage publié, maximum 18.2 heures)
  - Drapeaux (2 octets)
    Ordre des bits : 15 14 ... 3 2 1 0
    Bit 0 : Si 0, pas de clés hors-ligne ; si 1, clés hors-ligne
    Bit 1 : Si 0, un leaseset publié standard.
           Si 1, un leaseset non publié. Ne doit pas être inondé, publié, ou
           envoyé en réponse à une requête. Si ce leaseset expire, ne pas interroger le
           netdb pour un nouveau, à moins que le bit 2 ne soit défini.
    Bit 2 : Si 0, un leaseset publié standard.
           Si 1, ce leaseset non chiffré sera masqué et chiffré lorsqu'il sera publié.
           Si ce leaseset expire, interrogez l'emplacement masqué dans le netdb pour un nouveau.
           Si ce bit est défini sur 1, définissez également le bit 1 sur 1.
           À partir de la version 0.9.42.
    Bits 3-15 : définis sur 0 pour la compatibilité avec des utilisations futures
  - Si le drapeau indique des clés hors-ligne, la section de signature hors-ligne :
    Horodatage d'expiration (4 octets, big endian, secondes depuis l'époque, se réinitialise en 2106)
    Type sig transitoire (2 octets, big endian)
    Clé publique de signature transitoire (longueur telle qu'impliquée par le type de sig)
    Signature de l'horodatage d'expiration, type de sig transitoire, et clé publique,
    par la clé publique de destination,
    longueur telle qu'impliquée par le type de sig clé publique de destination.
    Cette section peut, et doit, être générée hors-ligne.


Justification
`````````````

- Non publié/publié : A utiliser lors de l'envoi d'une base de données de store bout-en-bout,
  le routeur émetteur peut souhaiter indiquer que ce leaseset ne doit pas être
  envoyé aux autres. Nous utilisons actuellement des heuristiques pour maintenir cet état.

- Publié : Remplace la logique complexe requise pour déterminer la 'version' du
  leaseset. Actuellement, la version est l'expiration du lease expirant en dernier,
  et un routeur de publication doit incrémenter cette expiration d'au moins 1ms lors
  de la publication d'un leaseset qui ne fait que supprimer un lease plus ancien.

- Expire : Permet une expiration d'une entrée netdb plus tôt que celle
  du leaseset expirant en dernier. Peut ne pas être utile pour LS2, où les leasesets
  sont censés rester avec une expiration maximale de 11 minutes, mais
  pour d'autres nouveaux types, cela est nécessaire (voir Meta LS et Service Record ci-dessous).

- Les clés hors-ligne sont optionnelles, pour réduire la complexité de l'implémentation initiale/requise.


### Problèmes

- Pourrait réduire encore plus la précision des horodatages (10 minutes?) mais il faudrait ajouter
  un numéro de version. Cela pourrait casser le multi-domiciliation, sauf si nous avons un chiffrement conservant l'ordre ?
  Probablement pas possible de se passer totalement d'horodatages.

- Alternative : horodatage sur 3 octets (époque / 10 minutes), numéro de version sur 1 octet, expiration sur 2 octets

- Le type est-il explicite ou implicite dans les données / signature ? Constantes de "domaine" pour signature ?


Notes
`````

- Les routeurs ne devraient pas publier un LS plus d'une fois par seconde.
  S'ils le font, ils doivent incrémenter artificiellement l'horodatage publié de 1
  par rapport au LS précédemment publié.

- Les implémentations de routeur peuvent mettre en cache les clés transitoires et la signature pour
  éviter la vérification à chaque fois. En particulier, les inondations, et les routeurs aux deux
  extrémités des connexions longue durée, pourraient en bénéficier.

- Les clés et signatures hors-ligne ne conviennent que pour les destinations longue durée,
  c'est-à-dire les serveurs, pas les clients.



## Nouveaux types d'entrées de base de données


### LeaseSet 2

Changements par rapport au LeaseSet existant :

- Ajouter un horodatage publié, un horodatage d'expiration, des drapeaux et des propriétés
- Ajouter un type de chiffrement
- Supprimer la clé de révocation

Lookup avec
    Drapeau LS standard (1)
Store avec
    Type LS2 standard (3)
Stockage à
    Hachage de la destination
    Ce hachage est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1
Expiration typique
    10 minutes, comme dans un LS régulier.
Publié par
    Destination

Format
``````
::

  Entête LS2 Standard tel que spécifié ci-dessus

  Partie Spécifique LS2 Standard
  - Propriétés (Mappage tel que spécifié dans les structures communes de spec, 2 octets zéro si aucune)
  - Nombre de sections de clés à suivre (1 octet, max TBD)
  - Sections de clés :
    - Type de chiffrement (2 octets, big endian)
    - Longueur de la clé de chiffrement (2 octets, big endian)
      Ceci est explicite, donc les floodfills peuvent analyser LS2 avec des types de chiffrement inconnus.
    - Clé de chiffrement (nombre d'octets spécifié)
  - Nombre de lease2 (1 octet)
  - Lease2 (40 octets chacun)
    Il s'agit de leases, mais avec une expiration de 4 octets au lieu de 8 octets,
    en secondes depuis l'époque (se réinitialise en 2106)

  Signature LS2 Standard :
  - Signature
    Si le drapeau indique des clés hors-ligne, cela est signé par la clé publique transitoire,
    sinon, par la clé publique de destination
    Longueur telle qu'impliquée par le type de sig de la clé de signature
    La signature concerne tout ce qui précède.




Justification
`````````````

- Propriétés : Expansion future et flexibilité.
  Placé en premier au cas où nécessaire pour l'analyse des données restantes.

- Plusieurs types de chiffrement/paires de clés publiques sont
  pour faciliter la transition vers de nouveaux types de chiffrement. L'autre moyen de le faire
  est de publier plusieurs leasesets, éventuellement en utilisant les mêmes tunnels,
  comme nous le faisons maintenant pour les destinations DSA et EdDSA.
  L'identification du type de chiffrement entrant sur un tunnel
  peut être effectuée avec le mécanisme existant du tag de session,
  et/ou un décryptage d'essai utilisant chaque clé. Les longueurs des messages entrants peuvent également fournir un indice.

Discussion
``````````

Cette proposition continue d'utiliser la clé publique dans le leaseset pour la
clé de chiffrement de bout en bout, et laisse le champ de clé publique dans le
certificat de clé de destination inutilisé, comme c'est le cas maintenant. Le type de chiffrement n'est pas spécifié
dans le certificat de clé de destination, il restera à 0.

Une alternative rejetée est de spécifier le type de chiffrement dans le certificat de clé de destination,
d'utiliser la clé publique dans la Destination, et de ne pas utiliser la clé publique
dans le leaseset. Nous n'avons pas l'intention de faire cela.

Avantages de LS2 :

- L'emplacement de la clé publique réelle ne change pas.
- Le type de chiffrement ou la clé publique peuvent changer sans changer la Destination.
- Supprime le champ de révocation inutilisé
- Compatibilité de base avec d'autres types d'entrée de base de données dans cette proposition
- Permet plusieurs types de chiffrement

Inconvénients de LS2 :

- L'emplacement de la clé publique et du type de chiffrement diffère de RouterInfo
- Maintient la clé publique inutilisée dans le leaseset
- Nécessite une implémentation à travers le réseau ; dans l'alternative, des
  types de chiffrement expérimentaux peuvent être utilisés, si autorisés par les floodfills
  (mais voir les propositions 136 et 137 concernant le support des types de signature expérimentaux).
  L'alternative pourrait être plus facile à implémenter et tester pour les types de chiffrement expérimentaux.


Problèmes de Nouveau Chiffrement
`````````````````````````````````
Une partie de cela est hors-sujet pour cette proposition,
mais on met les notes ici pour l'instant car nous n'avons pas encore
de proposition de chiffrement séparée.
Voir également les propositions ECIES 144 et 145.

- Le type de chiffrement représente la combinaison
  de courbe, longueur de clé, et schéma de bout en bout,
  y compris KDF et MAC, le cas échéant.

- Nous avons inclus un champ de longueur de clé, de sorte que le LS2
  soit analysable et vérifiable par le floodfill même pour les types de chiffrement inconnus.

- Le premier type de chiffrement à être proposé sera
  probablement ECIES/X25519. Comment il est utilisé de bout en bout
  (soit une version légèrement modifiée de ElGamal/AES+SessionTag
  soit quelque chose de complètement nouveau, par exemple ChaCha/Poly) sera spécifié
  dans un ou plusieurs propositions séparées.
  Voir également les propositions ECIES 144 et 145.


Notes
`````
- Expiration modifiée dans leases de 8 octets à 4 octets.

- Si nous implémentons un jour une révocation, nous pouvons le faire avec un champ d'expiration de zéro,
  ou zéro leases, ou les deux. Pas besoin d'une clé de révocation distincte.

- Les clés de chiffrement sont dans l'ordre de préférence du serveur, la plus préférée d'abord.
  Le comportement par défaut du client est de sélectionner la première clé avec
  un type de chiffrement supporté. Les clients peuvent utiliser d'autres algorithmes de sélection
  basés sur le support de chiffrement, la performance relative et d'autres facteurs.


### LS2 chiffré

Objectifs :

- Ajouter le blindage
- Permettre plusieurs types de signatures
- Ne pas nécessiter de nouvelles primitives crypto
- Chiffrer éventuellement pour chaque destinataire, révocable
- Supporter le chiffrement de LS2 Standard et Meta LS2 uniquement

LS2 chiffré n'est jamais envoyé dans un message garlic de bout en bout.
Utilisez le LS2 standard ci-dessus.


Changements par rapport au LeaseSet chiffré existant :

- Chiffrer l'ensemble pour la sécurité
- Chiffrer de façon sécurisée, pas avec AES seulement.
- Chiffrer pour chaque destinataire

Lookup avec
    Drapeau LS standard (1)
Store avec
    Type LS2 chiffré (5)
Stockage à
    Hachage du type sig masqué et clé publique masquée
    Type sig deux octets (big endian, par exemple 0x000b) || clé publique masquée
    Ce hachage est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1
Expiration typique
    10 minutes, comme dans un LS régulier, ou des heures, comme dans un meta LS.
Publié par
    Destination


Définitions
```````````
Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés
pour LS2 chiffré :

CSRNG(n)
    Sortie de n octets d'un générateur de nombres aléatoires cryptographiquement sûr.

    En plus de l'obligation pour CSRNG d'être cryptographiquement sûr (et donc
    adapté à la génération de matériel de clé), il DOIT être sûr
    pour qu'une sortie de n octets soit utilisée pour du matériel de clé lorsque les séquences d'octets immédiatement
    précédentes et suivantes sont exposées sur le réseau (par exemple dans un sel, ou padding chiffré). Les implémentations qui dépendent d'une source potentiellement peu fiable devraient hacher
    toute sortie qui doit être exposée sur le réseau [PRNG-REFS]_.

H(p, d)
    Fonction de hachage SHA-256 qui prend une chaîne de personnalisation p et des données d, et
    produit une sortie de longueur de 32 octets.

    Utiliser SHA-256 comme suit :

        H(p, d) := SHA-256(p || d)

STREAM
    Le chiffrement de flux ChaCha20 tel que spécifié dans [RFC-7539-S2.4]_, avec le compteur initial
    réglé à 1. S_KEY_LEN = 32 et S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Chiffre le texte en clair en utilisant la clé de chiffrement k, et le nonce iv qui DOIT être unique pour
        la clé k. Retourne un texte chiffré qui est de la même taille que le texte en clair.

        Le texte chiffré entier doit être indistinguable de l'aléatoire si la clé est secrète.

    DECRYPT(k, iv, ciphertext)
        Déchiffre le texte chiffré en utilisant la clé de chiffrement k, et le nonce iv. Retourne le texte en clair.


SIG
    Le schéma de signature RedDSA (correspondant au SigType 11) avec masquage de clé.
    Il a les fonctions suivantes :

    DERIVE_PUBLIC(privkey)
        Retourne la clé publique correspondant à la clé privée donnée.

    SIGN(privkey, m)
        Retourne une signature par la clé privée privkey sur le message donné m.

    VERIFY(pubkey, m, sig)
        Vérifie la signature sig par rapport à la clé publique pubkey et le message m. Retourne
        vrai si la signature est valide, faux sinon.

    Il doit également prendre en charge les opérations de masquage de clé suivantes :

    GENERATE_ALPHA(data, secret)
        Générer alpha pour ceux qui connaissent les données et un secret optionnel.
        Le résultat doit être distribué de manière identique aux clés privées.

    BLIND_PRIVKEY(privkey, alpha)
        Masque une clé privée, en utilisant un secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Masque une clé publique, en utilisant un secret alpha.
        Pour une paire de clés donnée (privkey, pubkey) la relation suivante est vérifiée :

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

DH
    Système d'accord de clé public X25519. Clés privées de 32 octets, clés publiques de 32
    octets, produit des sorties de 32 octets. Il a les fonctions
    suivantes :

    GENERATE_PRIVATE()
        Génère une nouvelle clé privée.

    DERIVE_PUBLIC(privkey)
        Retourne la clé publique correspondant à la clé privée donnée.

    DH(privkey, pubkey)
        Génère un secret partagé à partir des clés privée et publique données.

HKDF(salt, ikm, info, n)
    Une fonction de dérivation de clé cryptographique qui prend une clé d'entrée ikm (qui
    devrait avoir une bonne entropie mais n'est pas nécessairement une chaîne aléatoire uniforme), un sel
    de longueur de 32 octets, et une valeur contextuelle spécifique au contexte et produit une sortie
    de n octets adaptée à une utilisation en tant que matériel de clé.

    Utiliser HKDF comme spécifié dans [RFC-5869]_, utilisant la fonction de hachage HMAC SHA-256
    comme spécifié dans [RFC-2104]_. Cela signifie que SALT_LEN est de 32 octets max.


Format
``````
Le format LS2 chiffré consiste en trois couches imbriquées :

- Une couche extérieure contenant les informations en texte clair nécessaires au stockage et à la récupération.
- Une couche intermédiaire qui gère l'authentification du client.
- Une couche interne qui contient les données LS2 réelles.

Le format global ressemble à :

    Données de la couche 0 + Enc(données de la couche 1 + Enc(données de la couche 2)) + Signature

Notez que LS2 chiffré est masqué. La Destination n'est pas dans l'entête.
Le lieu de stockage DHT est SHA-256(type sig || clé publique masquée), et tourné quotidiennement.

N'utilise PAS l'entête LS2 standard spécifié ci-dessus.

#### Couche 0 (extérieure)
Type
    1 octet

    Pas réellement dans l'entête, mais partie des données couvertes par la signature.
    Pris du champ du message de Database Store.

Type de Sig Clé Publique Masquée
    2 octets, big endian
    Cela sera toujours le type 11, identifiant une clé masquée Red25519.

Clé Publique Masquée
    Longueur telle qu'impliquée par le type sig

Horodatage publié
    4 octets, big endian

    Secondes depuis l'époque, se réinitialise en 2106

Expire
    2 octets, big endian

    Décalage par rapport à l'horodatage publié en secondes, max 18,2 heures

Drapeaux
    2 octets

    Ordre des bits : 15 14 ... 3 2 1 0

    Bit 0 : Si 0, pas de clés hors-ligne ; si 1, clés hors-ligne

    Autres bits : fixés à 0 pour la compatibilité avec des utilisations futures

Données clés transitoires
    Présent si le drapeau indique des clés hors-ligne

    Horodatage d'expiration
        4 octets, big endian

        Secondes depuis l'époque, se réinitialise en 2106

    Type sig transitoire
        2 octets, big endian

    Clé publique de signature transitoire
        Longueur telle qu'impliquée par le type sig

    Signature
        Longueur telle qu'impliquée par le type sig clé publique masquée

        Sur l'horodatage d'expiration, le type sig transitoire et la clé publique.

        Vérifié avec la clé publique masquée.

longueurChiffrementExtérieur
    2 octets, big endian

chiffrementExtérieur
    longueurChiffrementExtérieur octets

    Données de la couche 1 chiffrées. Voir ci-dessous pour la dérivation de clé et les algorithmes de chiffrement.

Signature
    Longueur telle qu'impliquée par le type de sig de la clé de signature utilisée

    La signature couvre tout ce qui précède.

    Si le drapeau indique des clés hors-ligne, la signature est vérifiée avec la clé publique transitoire.
    Sinon, la signature est vérifiée avec la clé publique masquée.


#### Couche 1 (intermédiaire)
Drapeaux
    1 octet
    
    Ordre des bits : 76543210

    Bit 0 : 0 pour tout le monde, 1 pour par client, section d'authentification à suivre

    Bits 3-1 : Schéma d'authentification, seulement si le bit 0 est défini sur 1 pour par client, sinon 000
              000: Authentification client DH (ou pas d'authentification par client)
              001: Authentification client PSK

    Bits 7-4 : Non utilisé, défini sur 0 pour la compatibilité future

Données auth client DH
    Présent si le bit de drapeau 0 est défini sur 1 et les bits de drapeau 3-1 sont définis sur 000.

    cléPubliqueÉphémère
        32 octets

    clients
        2 octets, big endian

        Nombre d'entrées authClient à suivre, 40 octets chacune

    authClient
        Données d'autorisation pour un client unique.
        Voir ci-dessous l'algorithme d'autorisation par client.

        clientID_i
            8 octets

        clientCookie_i
            32 octets

Données auth client PSK
    Présent si le bit de drapeau 0 est défini sur 1 et les bits de drapeau 3-1 sont définis sur 001.

    authSalt
        32 octets

    clients
        2 octets, big endian

        Nombre d'entrées authClient à suivre, 40 octets chacune

    authClient
        Données d'autorisation pour un client unique.
        Voir ci-dessous l'algorithme d'autorisation par client.

        clientID_i
            8 octets

        clientCookie_i
            32 octets


chiffrementIntérieur
    Longueur implicite par longueurChiffrementExtérieur (les données restantes)

    Données de couche 2 chiffrées. Voir ci-dessous pour la dérivation de clé et les algorithmes de chiffrement.


#### Couche 2 (intérieure)
Type
    1 octet

    Soit 3 (LS2) ou 7 (Meta LS2)

Données
    Données LeaseSet2 pour le type donné.

    Inclut l'entête et la signature.


Dérivation de clé Masquage
`````````````````````````````

Nous utilisons le schéma suivant pour le masquage de clé,
basé sur Ed25519 et ZCash RedDSA [ZCASH]_.
Les signatures Re25519 sont sur la courbe Ed25519, utilisant SHA-512 pour le hachage.

Nous n'utilisons pas l'appendix A.2 de rend-spec-v3.txt de Tor [TOR-REND-SPEC-V3]_,
qui a des objectifs de conception similaires, car ses clés publiques masquées
peuvent ne pas être sur le sous-groupe d'ordre premier, avec des implications de sécurité inconnues.


#### Objectifs

- La clé publique de signature dans la destination non masquée doit être
  Ed25519 (type sig 7) ou Red25519 (type sig 11) ;
  aucun autre type de sig n'est supporté
- Si la clé publique de signature est hors-ligne, la clé publique de signature transitoire doit également être Ed25519
- Le masquage doit être computationnellement simple
- Utiliser les primitives cryptographiques existantes
- Les clés publiques masquées ne peuvent pas être démasquées
- Les clés publiques masquées doivent être sur la courbe Ed25519 et le sous-groupe d'ordre premier
- Doit connaître la clé publique de signature de la destination
  (la destination complète n'est pas requise) pour dériver la clé publique masquée
- Éventuellement prévoir un secret supplémentaire requis pour dériver la clé publique masquée


#### Sécurité

La sécurité d'un schéma de masquage nécessite que la
distribution d'alpha soit la même que les clés privées non masquées.
Cependant, lorsque nous masquons une clé privée Ed25519 (type sig 7)
en une clé privée Red25519 (type sig 11), la distribution est différente.
Pour répondre aux exigences de Zcash section 4.1.6.1 [ZCASH]_,
Red25519 (type sig 11) devrait être utilisé pour les clés non masquées également, de sorte que
"la combinaison d'une clé publique ré-randomisée et de signature(s)
sous cette clé ne révèle pas la clé à partir de laquelle elle a été ré-randomisée."
Nous autorisons le type 7 pour les destinations existantes, mais recommandons
type 11 pour les nouvelles destinations qui seront chiffrées.



#### Définitions

B
    Le point de base Ed25519 (générateur) 2^255 - 19 comme dans [ED25519-REFS]_

L
    L'ordre Ed25519 2^252 + 27742317777372353535851937790883648493
    comme dans [ED25519-REFS]_

DERIVE_PUBLIC(a)
    Convertir une clé privée en publique, comme dans Ed25519 (multiplier par G)

alpha
    Un nombre aléatoire de 32 octets connu de ceux qui connaissent la destination.

GENERATE_ALPHA(destination, date, secret)
    Générer alpha pour la date actuelle, pour ceux qui connaissent la destination et le secret.
    Le résultat doit être distribué de manière identique aux clés privées Ed25519.

a
    La clé privée de signature non masquée de 32 octets EdDSA ou RedDSA utilisée pour signer la destination

A
    La clé publique de signature non masquée de 32 octets EdDSA ou RedDSA dans la destination,
    = DERIVE_PUBLIC(a), comme dans Ed25519

a'
    La clé privée de signature EdDSA masquée de 32 octets utilisée pour signer le leaseset chiffré
    C'est une clé privée EdDSA valide.

A'
    La clé publique de signature EdDSA masquée de 32 octets dans la Destination,
    peut être générée avec DERIVE_PUBLIC(a'), ou à partir de A et alpha.
    C'est une clé publique EdDSA valide, sur la courbe et sur le sous-groupe d'ordre premier.

LEOS2IP(x)
    Renverser l'ordre des octets d'entrée en petit-boutisme

H*(x)
    32 octets = (LEOS2IP(SHA512(x))) mod B, même que dans Ed25519 hash-and-reduce


#### Calculs de Masquage

Un nouveau secret alpha et des clés masquées doivent être générés chaque jour (UTC).
Le secret alpha et les clés masquées sont calculés comme suit.

GENERATE_ALPHA(destination, date, secret), pour toutes les parties:

  ```text
// GENERATE_ALPHA(destination, date, secret)

  // le secret est optionnel, sinon de longueur zéro
  A = clé publique de signature de la destination
  stA = type de signature de A, 2 octets big endian (0x0007 ou 0x000b)
  stA' = type de signature de clé publique masquée A', 2 octets big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 octets ASCII YYYYMMDD de la date UTC actuelle
  secret = chaîne encodée en UTF-8 
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // traiter seed comme une valeur de 64 octets en petit-boutisme
  alpha = seed mod L
```

BLIND_PRIVKEY(), pour le propriétaire publiant le leaseset:

  ```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // Si pour une clé privée Ed25519 (type 7)
  seed = clé privée de signature de la destination
  a = moitié gauche de SHA512(seed) et pincé comme d'habitude pour Ed25519
  // sinon, pour une clé privée Red25519 (type 11)
  a = clé privée de signature de la destination
  // Addition en utilisant l'arithmétique scalaire
  clé privée de signature masquée = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  clé publique de signature masquée = A' = DERIVE_PUBLIC(a')
```

BLIND_PUBKEY(), pour les clients récupérant le leaseset:

  ```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = clé publique de signature de la destination
  // Addition en utilisant des éléments de groupe (points sur la courbe)
  clé publique masquée = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```

Les deux méthodes de calcul de A' donnent le même résultat, comme requis.



#### Signature

Le leaseset non masqué est signé par la clé privée de signature Ed25519 ou Red25519 non masquée
et vérifié avec la clé publique de signature Ed25519 ou Red25519 non masquée (types sig 7 ou 11) comme d'habitude.

Si la clé publique de signature est hors-ligne,
le leaseset non masqué est signé par la clé privée de signature transitoire Ed25519 ou Red25519 non masquée
et vérifié avec la clé publique de signature transitoire Ed25519 ou Red25519 non masquée (types sig 7 ou 11) comme d'habitude.
Voir ci-dessous pour des notes supplémentaires sur les clés hors-ligne pour les leasesetscryptés.

Pour la signature du leaseset chiffré, nous utilisons Red25519, basé sur RedDSA [ZCASH]_
pour signer et vérifier avec des clés masquées.
Les signatures Red25519 sont sur la courbe Ed25519, utilisant SHA-512 pour le hachage.

Red25519 est identique à Ed25519 sauf comme spécifié ci-dessous.


#### Calculs de Signature/Vérification

La partie extérieure du leaseset chiffré utilise les clés et signatures Red25519.

Red25519 est presque identique à Ed25519. Il y a deux différences :

Les clés privées Red25519 sont générées à partir de nombres aléatoires puis doivent être réduites mod L, où L est défini ci-dessus.
Les clés privées Ed25519 sont générées à partir de nombres aléatoires puis "pincées" en utilisant
le masquage de bit aux octets 0 et 31. Cela n'est pas fait pour Red25519.
Les fonctions GENERATE_ALPHA() et BLIND_PRIVKEY() définies ci-dessus génèrent des clés privées
Red25519 correctes en utilisant mod L.

Dans Red25519, le calcul de r pour la signature utilise des données aléatoires supplémentaires,
et utilise la valeur de clé publique plutôt que le hachage de la clé privée.
À cause des données aléatoires, chaque signature Red25519 est différente, même
lors de la signature des mêmes données avec la même clé.

Signature :

  ```text
T = 80 octets aléatoires
  r = H*(T || publickey || message)
  // le reste est le même que dans Ed25519
```

Vérification :

  ```text
// même que dans Ed25519
```



Chiffrement et traitement
``````````````````````````
#### Dérivation des souscrédits
Dans le cadre du processus de masquage, nous devons nous assurer qu'un LS2 chiffré ne peut pas être
déchiffré par quelqu'un qui ne connaît pas la clé publique de signature correspondante de Destination.
La destination complète n'est pas requise.
Pour y parvenir, nous dérivons une accréditation à partir de la clé publique de signature :

  ```text
A = clé publique de signature de la destination
  stA = type de signature de A, 2 octets big endian (0x0007 ou 0x000b)
  stA' = type de signature de A', 2 octets big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```

La chaîne de personnalisation garantit que l'accréditation ne se heurte pas à un hachage utilisé
comme clé de Lookup DHT, tel que le hachage simple de Destination.

Pour une clé masquée donnée, nous pouvons alors dériver une souscréditation :

  ```text
subcredential = H("subcredential", credential || blindedPublicKey)
```

La souscréditation est incluse dans les processus de dérivation de clé ci-dessous, ce qui lie ces
clés à la connaissance de la clé publique de signature de Destination.

#### Chiffrement de la couche 1
Tout d'abord, l'entrée au processus de dérivation de clé est préparée :

  ```text
outerInput = subcredential || publishedTimestamp
```

Ensuite, un sel aléatoire est généré :

  ```text
outerSalt = CSRNG(32)
```

Ensuite, la clé utilisée pour chiffrer la couche 1 est dérivée :

  ```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Enfin, le texte en clair de la couche 1 est chiffré et sérialisé :

  ```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```

#### Déchiffrement de la couche 1
Le sel est analysé à partir du texte chiffré de la couche 1 :

  ```text
outerSalt = outerCiphertext[0:31]
```

Ensuite, la clé utilisée pour chiffrer la couche 1 est dérivée :

  ```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```

Enfin, le texte chiffré de la couche 1 est déchiffré :

  ```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```

#### Chiffrement de la couche 2
Lorsque l'autorisation du client est activée, ``authCookie`` est calculé comme décrit ci-dessous.
Lorsque l'autorisation du client est désactivée, ``authCookie`` est le tableau d'octets de longueur nulle.

Le chiffrement se poursuit de manière similaire à la couche 1 :

  ```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```

#### Déchiffrement de la couche 2
Lorsque l'autorisation du client est activée, ``authCookie`` est calculé comme décrit ci-dessous.
Lorsque l'autorisation du client est désactivée, ``authCookie`` est le tableau d'octets de longueur nulle.

Le déchiffrement se poursuit de manière similaire à la couche 1 :

  ```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```


Autorisation par client
````````````````````````
Lorsque l'autorisation par client est activée pour une Destination, le serveur maintient une liste de
clients qu'ils autorisent à déchiffrer les données LS2 chiffrées. Les données stockées par client
dépend de la mécanique d'autorisation, et inclut une forme de matériel de clé que chaque
client génère et envoie au serveur via un mécanisme sécurisé hors-bande.

Il y a deux alternatives pour implémenter l'autorisation par client :

#### Authentification client DH
Chaque client génère une paire de clés DH ``[csk_i, cpk_i]`` et envoie la clé publique ``cpk_i``
au serveur.

Traitement côté serveur
^^^^^^^^^^^^^^^^^
Le serveur génère un nouveau ``authCookie`` et une paire de clés DH éphémère :

  ```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```

Ensuite, pour chaque client autorisé, le serveur chiffre ``authCookie`` vers sa clé publique :

  ```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Le serveur place chaque couple ``[clientID_i, clientCookie_i]`` dans la couche 1 de
LS2 chiffré, avec ``epk``.

Traitement côté client
^^^^^^^^^^^^^^^^^
Le client utilise sa clé privée pour dériver son identifiant client ``clientID_i`` attendu,
la clé de chiffrement ``clientKey_i``, et le IV de chiffrement ``clientIV_i`` :

  ```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Ensuite, le client recherche dans les données d'autorisation de couche 1 une entrée contenant
``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir
``authCookie`` :

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Authentification client par clé prépartagée
Chaque client génère une clé secrète de 32 octets ``psk_i`` et l'envoie au serveur.
Alternativement, le serveur peut générer la clé secrète et l'envoyer à un ou plusieurs clients.


Traitement côté serveur
^^^^^^^^^^^^^^^^^
Le serveur génère un nouveau ``authCookie`` et sel :

  ```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```

Ensuite, pour chaque client autorisé, le serveur chiffre ``authCookie`` à sa clé prépartagée :

  ```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```

Le serveur place chaque couple ``[clientID_i, clientCookie_i]`` dans la couche 1 de
LS2 chiffré, avec ``authSalt``.

Traitement côté client
^^^^^^^^^^^^^^^^^
Le client utilise sa clé prépartagée pour dériver son identifiant client ``clientID_i`` attendu,
la clé de chiffrement ``clientKey_i``, et le IV de chiffrement ``clientIV_i`` :

  ```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```

Ensuite, le client recherche dans les données d'autorisation de la couche 1 une entrée contenant
``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir
``authCookie`` :

  ```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```

#### Considérations de sécurité
Les deux mécanismes d'autorisation de client ci-dessus fournissent une confidentialité pour l'appartenance du client.
Une entité qui ne connaît que la Destination peut voir combien de clients sont abonnés à tout
moment, mais ne peut pas savoir quels clients sont ajoutés ou révoqués.

Les serveurs DOIVENT randomiser l'ordre des clients chaque fois qu'ils génèrent un LS2 chiffré, pour
empêcher les clients d'apprendre leur position dans la liste et d'inférer quand d'autres clients ont
été ajoutés ou révoqués.

Un serveur PEUT choisir de masquer le nombre de clients qui sont abonnés en insérant des
entrées aléatoires dans la liste des données d'autorisation.

Avantages de l'authentification client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- La sécurité du schéma ne dépend pas uniquement de l'échange hors-bande du matériel de clé client.
  La clé privée du client n'a jamais besoin de quitter leur appareil, et ainsi un
  adversaire qui parvient à intercepter l'échange hors-bande, mais ne peut pas briser l'algorithme DH,
  ne peut pas déchiffrer le LS2 chiffré, ou déterminer combien de temps le client reçoit
  l'accès.

Inconvénients de l'authentification client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Nécessite N + 1 opérations DH côté serveur pour N clients.
- Nécessite une opération DH côté client.
- Nécessite que le client génère la clé secrète.

Avantages de l'authentification client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Ne nécessite aucune opération DH.
- Permet au serveur de générer la clé secrète.
- Autorise le serveur à partager la même clé avec plusieurs clients, si souhaité.

Inconvénients de l'authentification client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- La sécurité du schéma dépend de manière cruciale de l'échange hors-bande du matériel de clé client.
  Un adversaire qui intercepte l'échange pour un client particulier peut
  déchiffrer tout LS2 chiffré ultérieur pour lequel ce client est autorisé, ainsi que déterminer
  quand l'accès du client est révoqué.


LS chiffré avec adresses Base 32
````````````````````````````````

Voir la proposition 149.

Vous ne pouvez pas utiliser un LS2 chiffré pour bittorrent, à cause des réponses d'annonce compactes qui sont de 32 octets.
Les 32 octets contiennent uniquement le hachage. Il n'y a pas de place pour une indication que le
leaseset est chiffré, ou les types de signature.



LS chiffré avec Clés Hors-ligne
```````````````````````````````
Pour les leasesets chiffrés avec des clés hors-ligne, les clés privées masquées doivent également être générées hors-ligne,
une pour chaque jour.

Comme le bloc de signature hors-ligne optionnel est dans la partie claire du leaseset chiffré,
quiconque récupère les inondations pourrait utiliser cela pour suivre le leaseset (mais ne peut pas le déchiffrer)
pendant plusieurs jours.
Pour éviter cela, le propriétaire des clés devrait générer de nouvelles clés transitoires
pour chaque jour également.
Les clés transitoires et masquées peuvent être générées à l'avance, et livrées au routeur
en un lot.

Il n'est pas défini dans cette proposition de format de fichier pour conditionner plusieurs clés transitoires et
masquées et les fournir au client ou au routeur.
Il n'y a pas d'amélioration du protocole I2CP définie dans cette proposition pour supporter
les leasesets chiffrés avec des clés hors-ligne.



Notes
`````

- Un service utilisant des leasesets chiffrés publierait la version chiffrée vers les
  floodfills. Cependant, pour plus d'efficacité, il enverrait des leasesets non chiffrés aux
  clients dans le message garlic enveloppé, une fois authentifié (via whitelist, par
  exemple).

- Les floodfills peuvent limiter la taille maximale à une valeur raisonnable pour prévenir les abus.

- Après le déchiffrement, plusieurs vérifications doivent être effectuées, y compris que
  l'horodatage et l'expiration internes correspondent à ceux au niveau supérieur.

- ChaCha20 a été sélectionné par rapport à AES. Bien que les vitesses soient similaires si le support matériel AES est
  disponible, ChaCha20 est 2.5-3x plus rapide lorsque
  le support matériel AES n'est pas disponible, comme sur les appareils ARM de bas de gamme.

- Nous ne nous soucions pas assez de la vitesse pour utiliser BLAKE2b avec clé. Il a une
  taille de sortie suffisamment grande pour accommoder les plus grandes n que nous pouvons nécessiter (ou nous pouvons l'appeler une fois par clé requise avec un argument de compteur). BLAKE2b est beaucoup plus rapide que SHA-256, et
  BLAKE2b avec clé réduirait le nombre total d'appels de fonction de hachage.
  Cependant, voir la proposition 148, où il est proposé que nous passions à BLAKE2b pour d'autres raisons.
  [UNSCIENTIFIC-KDF-SPEEDS]_


### Meta LS2

Ceci est utilisé pour remplacer le multi-domiciliation. Comme tout leaseset, cela est signé par le
créateur. Ceci est une liste authentifiée de hachages de destination.

Le Meta LS2 est le sommet de, et peut-être aussi les nœuds intermédiaires de,
une structure arborescente.
Il contient un certain nombre d'entrées, chacune pointant vers un LS, LS2, ou un autre Meta LS2
pour supporter un multi-domiciliation massif.
Un Meta LS2 peut contenir un mélange d'entrées LS, LS2, et Meta LS2.
Les feuilles de l'arbre sont toujours un LS ou LS2.
L'arborescence est un DAG ; les boucles sont interdites ; les clients effectuant des recherches doivent détecter et
refuser de suivre des boucles.

Un Meta LS2 peut avoir une expiration beaucoup plus longue qu'un LS standard ou LS2.
Le niveau supérieur peut avoir une expiration plusieurs heures après la date de publication.
Le temps d'expiration maximum sera imposé par les floodfills et les clients, et est TBD.

Le cas d'utilisation pour Meta LS2 est un multi-domiciliation massif, mais sans plus
de protection pour la corrélation de routeurs aux leasesets (au moment du redémarrage du routeur) que
n'est actuellement fourni avec LS ou LS2.
Ceci est égal au cas d'utilisation "facebook", qui probablement n'a pas besoin
de protection de corrélation. Ce cas d'utilisation a probablement besoin de clés hors-ligne,
qui sont fournies dans l'entête standard à chaque nœud de l'arborescence.

Le protocole back-end pour la coordination entre les routeurs de feuilles, les intermédiaires et les signataires principaux de Meta LS
n'est pas spécifié ici. Les exigences sont extrêmement simples - juste vérifier que le pair est actif,
et publier un nouveau LS toutes les quelques heures. La seule complexité est pour choisir de nouvelles
éditeurs pour les Meta LS du niveau supérieur ou intermédiaire en cas d'échec.

Les sets de locations "invisibles de multi-domiciliation" où les locations de plusieurs routeurs sont combinés, signés, et publiés
dans un seul set de locations est documentée dans la proposition 140, "multi-domiciliation invisible".
Cette proposition est intenable telle qu'écrite, car les connexions de streaming ne seraient pas
"permanentes" à un seul routeur, voir http://zzz.i2p/topics/2335 .

Le protocole back-end, et l'interaction avec les routeurs et les clients internes, serait
assez complexe pour la multi-domiciliation invisible.

Pour éviter de surcharger le floodfill pour le Meta LS de niveau supérieur, l'expiration doit
être au moins plusieurs heures. Les clients doivent mettre en cache le Meta LS de niveau supérieur, et persister
across restarts if unexpired.

We need to define some algorithm for clients to traverse the tree, including fallbacks,
so that the usage is dispersed. Some function of hash distance, cost, and randomness.
If a node has both LS or LS2 and Meta LS, we need to know when it's allowed
to use those leasesets, and when to keep traversing the tree.




Lookup avec
    Drapeau LS standard (1)
Store avec
    Type Meta LS2 (7)
Stockage à
    Hachage de la destination
    Ce hachage est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1
Expiration typique
    Heures. Max 18.2 heures (65535 secondes)
Publié par
    Destination "maître" ou coordinateur, ou coordinateurs intermédiaires

Format
``````
::

  Entête LS2 Standard tel que spécifié ci-dessus

  Partie Spécifique Meta LS2
  - Propriétés (Mappage tel que spécifié dans les structures communes de spec, 2 octets zéro si aucune)
  - Nombre d'entrées (1 octet) Maximum TBD
  - Entrées. Chaque entrée contient : (40 octets)
    - Hachage (32 octets)
    - Drapeaux (2 octets)
      TBD. Définir tous à zéro pour la compatibilité avec les usages futurs.
    - Type (1 octet) Le type de LS auquel il fait référence ;
      1 pour LS, 3 pour LS2, 5 pour chiffré, 7 pour meta, 0 pour inconnu.
    - Coût (priorité) (1 octet)
    - Expiration (4 octets) (4 octets, big endian, secondes depuis l'époque, se réinitialise en 2106)
  - Nombre de révocations (1 octet) Maximum TBD
  - Révocations : Chaque révocation contient : (32 octets)
    - Hachage (32 octets)

  Signature LS2 Standard :
  - Signature (40+ octets)
    La signature concerne tout ce qui précède.

Drapeaux et propriétés : pour usage futur


Notes
`````
- Un service distribué utilisant cela aurait un ou plusieurs "maîtres" avec la
  clé privée de la destination de service. Ils détermineraient (hors bande) la
  liste actuelle des destinations actives et publieraient le Meta LS2. Pour
  la redondance, plusieurs maîtres pourraient faire du multi-domiciliation (i.e. publier simultanément) le
  Meta LS2.

- Un service distribué pourrait commencer avec une destination unique ou utiliser l'ancienne méthode
  de multi-domiciliation, puis passer à un Meta LS2. Un Lookup de LS standard pourrait retourner
  un LS, LS2 ou Meta LS2.

- Lorsqu'un service utilise un Meta LS2, il n'a pas de tunnels (leases).


### Service Record

Il s'agit d'un enregistrement individuel indiquant qu'une destination participe à un
service. Il est envoyé de la part du participant au floodfill. Il n'est jamais envoyé
individuellement par un floodfill, mais uniquement dans le cadre d'une Service List. Le 
Service Record est également utilisé pour révoquer la participation à un service, en définissant 
l'expiration à zéro.

Ce n'est pas un LS2 mais il utilise le format standard d'entête et de signature LS2.

Lookup avec
    n/a, voir Service List
Store avec
    Type de Service Record (9)
Stockage à
    Hachage du nom de service
    Ce hachage est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1
Expiration typique
    Heures. Max 18.2 heures (65535 secondes)
Publié par
    Destination

Format
``````
::

  Entête LS2 Standard tel que spécifié ci-dessus

  Partie Spécifique Service Record
  - Port (2 octets, big endian) (0 si non spécifié)
  - Hachage du nom de service (32 octets)

  Signature LS2 Standard :
  - Signature (40+ octets)
    La signature concerne tout ce qui précède.


Notes
`````
- Si expire est à zéro, le floodfill devrait révoquer l'enregistrement et ne plus
  l'inclure dans la liste de service.

- Stockage : Le floodfill peut limiter strictement le stockage de ces enregistrements et
  limiter le nombre d'enregistrements stockés par hachage et leur expiration. Une whitelist
  de hachages peut également être utilisée.

- Tout autre type netdb au même hachage a la priorité, donc un enregistrement de service ne peut jamais
  écraser un LS/RI, mais un LS/RI écrasera tous les enregistrements de service à ce hachage.



### Service List

Cela n'est rien comme un LS2 et utilise un format différent.

La liste de service est créée et signée par le floodfill. Elle est non authentifiée
en ce sens que n'importe qui peut rejoindre un service en publiant un Service Record à un
floodfill.

Une Service List contient des Bons de service courts, pas des Service Records complets. Ceux-ci
contiennent des signatures mais seulement des hachages, pas des destinations complètes, donc ils ne peuvent pas être
vérifiés sans la destination complète.

La sécurité, si elle existe, et la désirabilité des listes de services sont TBD.
Les floodfills pourraient limiter la publication et les recherches à une whitelist de services,
mais cette whitelist peut varier en fonction de l'implémentation ou des préférences de l'opérateur.
Il peut ne pas être possible d'obtenir un consensus sur une liste blanche commune
across implementations.

If the service name is included in the service record above,
then floodfill operators may object; if only the hash is included,
there's no verification, and a service record could "get in" ahead of
any other netdb type and get stored in the floodfill.

Lookup avec
    Type de Lookup de Service List (11)
Store avec
    Type de Service List (11)
Stockage à
    Hachage du nom de service
    Ce hachage est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1
Expiration typique
    Heures, non spécifié dans la liste elle-même, jusqu'à la politique locale
Publié par
    Personne, jamais envoyé aux floodfills, jamais inondé.

Format
``````
N'utilise PAS l'entête LS2 standard spécifié ci-dessus.

::

  - Type (1 octet)
    Pas réellement dans l'entête, mais partie des données couvertes par la signature.
    Pris du champ du message de Database Store.
  - Hachage du nom de service (implicite, dans le message de Database Store)
  - Hachage du Créateur (floodfill) (32 octets)
  - Horodatage publié (8 octets, big endian)

  - Nombre de Short Service Records (1 octet)
  - Liste de Short Service Records :
    Chaque Short Service Record contient (90+ octets)
    - Dest hachage (32 octets)
    - Horodatage publié (8 octets, big endian)
    - Expires (4 octets, big endian) (décalage par rapport au publié en ms)
    - Drapeaux (2 octets)
    - Port (2 octets, big endian)
    - Longueur signature (2 octets, big endian)
    - Signature de dest (40+ octets)

  - Nombre de Revocation Records (1 octet)
  - Liste de Revocation Records :
    Chaque Revocation Record contient (86+ octets)
    - Dest hachage (32 octets)
    - Horodatage publié (8 octets, big endian)
    - Drapeaux (2 octets)
    - Port (2 octets, big endian)
    - Longueur signature (2 octets, big endian)
    - Signature de dest (40+ octets)

  - Signature de floodfill (40+ octets)
    La signature concerne tout ce qui précède.

Pour vérifier la signature de la Service List :

- préfixer le hachage du nom de service
- retirer le hachage du créateur
- Vérifiez la signature du contenu modifié

Pour vérifier la signature de chaque Short Service Record :

- Récupérer la destination
- Vérifiez la signature de (horodatage publié + expire + drapeaux + port + Hachage du
  nom de service)

Pour vérifier la signature de chaque Revocation Record :

- Récupérer la destination
- Vérifiez la signature de (horodatage publié + 4 octets à zéro + drapeaux + port + Hachage
  du nom de service)

Notes
`````
- Nous utilisons la longueur de la signature au lieu du type de sig pour que nous puissions supporter les types
  de signature inconnus.

- Il n'y a pas d'expiration d'une liste de services, les destinataires peuvent prendre leur propre
  décision basée sur la politique ou l'expiration des enregistrements individuels.

- Les listes de services ne sont pas inondées, seuls les Service Records individuels le sont. Chaque
  floodfill crée, signe et met en cache une liste de services. Le floodfill utilise sa
  propre politique pour le temps de cache et le nombre maximum de services et d'
  enregistrements de révocation.



## Modifications spécifiées des structures communes requises


### Certificats de clé

Hors-sujet pour cette proposition.
Ajoutez aux propositions ECIES 144 et 145.


### Nouvelles structures intermédiaires

Ajouter de nouvelles structures pour Lease2, MetaLease, LeaseSet2Header, et OfflineSignature.
Effectif à partir de la version 0.9.38.


### Nouveaux types NetDB

Ajouter des structures pour chaque nouveau type de leaseset, incorporé à partir de ce qui précède.
Pour LeaseSet2, EncryptedLeaseSet, et MetaLeaseSet,
effectif à partir de la version 0.9.38.
Pour Service Record et Service List,
préliminaire et non prévu.


### Nouveau type de signature

Ajouter RedDSA_SHA512_Ed25519 Type 11.
Clé publique est de 32 octets ; clé privée est de 32 octets ; hachage est de 64 octets ; signature est de 64 octets.



## Modifications du chiffrement requises

Hors-sujet pour cette proposition.
Voir les propositions 144 et 145.



## Modifications I2NP requises

Ajouter une note : LS2 ne peut être publié que sur des floodfills avec un minimum de version.


### Message de Lookup de base de données

Ajouter le type de recherche de liste de services.

Changements
```````
::

  Byte Flags : Champ de type de Lookup, actuellement bits 3-2, s'étend aux bits 4-2.
  Le type de Lookup 0x04 est défini comme le Lookup de la liste de services.

  Ajouter une note : Le Lookup de liste de service ne peut être envoyé qu'à des floodfills avec une version minimale.
  La version minimale est 0.9.38.


### Message de Store de base de données

Ajouter tous les nouveaux types de Store.

Changements
```````
::

  Byte Type : Champ de type, actuellement bit 0, s'étend aux bits 3-0.
  Le type 3 est défini comme un LS2 store.
  Le type 5 est défini comme un LS2 chiffré store.
  Le type 7 est défini comme un meta LS2 store.
  Le type 9 est défini comme un service record store.
  Le type 11 est défini comme un service list store.
  Les autres types ne sont pas définis et valides.

  Ajouter une note : Tous les nouveaux types ne peuvent être publiés que sur des floodfills avec une version minimale.
  La version minimale est 0.9.38.




## Modifications I2CP requises


### Options I2CP

Nouvelles options interprétées côté routeur, envoyées dans le Mappage de SessionConfig :

::

  i2cp.leaseSetType=nnn       Le type de leaseset à envoyer dans le Message Create Leaseset
                              La valeur est la même que le type de store netdb dans le tableau ci-dessus.
                              Interprétée côté client, mais aussi transmise au routeur dans le
                              SessionConfig, pour déclarer l'intention et vérifier le support.

  i2cp.leaseSetEncType=nnn[,nnn]  Les types de chiffrement à utiliser.
                                  Interprété côté client, mais aussi transmis au routeur dans
                                  le SessionConfig, pour déclarer l'intention et vérifier le support.
                                  Voir les propositions 144 et 145.

  i2cp.leaseSetOfflineExpiration=nnn  L'expiration de la signature hors-ligne, ASCII,
                                      secondes depuis l'époque.

  i2cp.leaseSetTransientPublicKey=[type:]b64  La base 64 de la clé privée transitoire,
                                              précédée d'un numéro de type sig optionnel
                                              ou nom, par défaut DSA_SHA1.
                                              Longueur telle qu'inférée du type sig

  i2cp.leaseSetOfflineSignature=b64   La base 64 de la signature hors-ligne.
                                      Longueur telle qu'inférée du type de sig clé publique de destination

  i2cp.leaseSetSecret=b64     La base 64 d'un secret utilisé pour masquer le
                              l'adresse du leaseset, par défaut ""

  i2cp.leaseSetAuthType=nnn   Le type d'authentification pour LS2 chiffré.
                              0 pour pas d'authentification par client (la valeur par défaut)
                              1 pour authentication par client DH
                              2 pour authentication par client PSK

  i2cp.leaseSetPrivKey=b64    Une clé privée en base 64 pour le routeur à utiliser pour
                              déchiffrer le LS2 chiffré,
                              seulement si l'authentification par client est activée


Nouvelles options interprétées côté client :

::

  i2cp.leaseSetType=nnn     Le type de leaseset à envoyer dans le Message Create Leaseset
                            La valeur est la même que le type de store netdb dans le tableau ci-dessus.
                            Interprétée côté client, mais aussi transmise par le routeur dans le
                            SessionConfig, pour déclarer
