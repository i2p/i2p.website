---
title: "ECIES-X25519-AEAD-Ratchet"
number: "144"
author: "zzz, chisana, original"
created: "2018-11-22"
lastupdated: "2025-03-05"
status: "Closed"
thread: "http://zzz.i2p/topics/2639"
target: "0.9.46"
implementedin: "0.9.46"
---

## Note
Déploiement et test sur le réseau en cours.
Sujet à des révisions mineures.
Voir [SPEC](/en/docs/spec/ecies/) pour la spécification officielle.

Les fonctionnalités suivantes ne sont pas implémentées à partir de 0.9.46 :

- Blocs MessageNumbers, Options et Termination
- Réponses au niveau du protocole
- Clé statique nulle
- Diffusion


## Aperçu

Il s'agit d'une proposition pour le premier nouveau type de cryptage de bout en bout
depuis le début de I2P, pour remplacer ElGamal/AES+SessionTags [Elg-AES](/en/docs/spec/elgamal-aes/).

Elle s'appuie sur des travaux précédents comme suit :

- Spécification des structures communes [Common](/en/docs/spec/common-structures/)
- Spécification [I2NP](/en/docs/spec/i2np/), y compris LS2
- ElGamal/AES+Session Tags [Elg-AES](/en/docs/spec/elgamal-aes/)
- Aperçu de la nouvelle crypto asymétrique http://zzz.i2p/topics/1768
- Aperçu de la crypto de bas niveau [CRYPTO-ELG](/en/docs/how/cryptography/)
- ECIES http://zzz.i2p/topics/2418
- [NTCP2](/en/docs/transport/ntcp2/) [Prop111](/en/proposals/111-ntcp2/)
- 123 Nouvelles entrées netDB
- 142 Nouveau modèle de cryptographie
- Protocole [Noise](https://noiseprotocol.org/noise.html)
- Algorithme à double cliquet [Signal](https://signal.org/docs/specifications/doubleratchet/)

L'objectif est de prendre en charge un nouveau cryptage pour la communication de bout en bout,
destination-à-destination.

La conception utilisera une phase de poignée de main et de données Noise incorporant le double cliquet Signal.

Toutes les références à Signal et Noise dans cette proposition sont uniquement à titre d'information.
Aucune connaissance des protocoles Signal et Noise n'est requise pour comprendre
ou mettre en œuvre cette proposition.


### Utilisations actuelles de ElGamal

Pour révision,
des clés publiques ElGamal de 256 octets peuvent être trouvées dans les structures de données suivantes.
Référez-vous à la spécification des structures communes.

- Dans une identité de routeur
  Il s'agit de la clé de cryptage du routeur.

- Dans une destination
  La clé publique de la destination était utilisée pour l'ancien cryptage i2cp-à-i2cp
  qui a été désactivé dans la version 0.6, elle est actuellement inutilisée sauf pour
  l'IV pour le cryptage LeaseSet, qui est déprécié.
  La clé publique du LeaseSet est utilisée à la place.

- Dans un LeaseSet
  Il s'agit de la clé de cryptage de la destination.

- Dans un LS2
  Il s'agit de la clé de cryptage de la destination.



### EncTypes dans les certificats de clé

Pour révision,
nous avons ajouté la prise en charge des types de cryptage lorsque nous avons ajouté la prise en charge des types de signature.
Le champ de type de cryptage est toujours à zéro, à la fois dans Destinations et RouterIdentities.
La décision de changer cela est TBD.
Référez-vous à la spécification des structures communes [Common](/en/docs/spec/common-structures/).




### Utilisations de la cryptographie asymétrique

Pour révision, nous utilisons ElGamal pour :

1) Messages de construction de tunnel (la clé est dans RouterIdentity)
   Le remplacement n'est pas couvert dans cette proposition.
   Voir la proposition 152 [Prop152](/en/proposals/152-ecies-tunnels/).

2) Cryptage routeur-à-routeur des messages netdb et autres messages I2NP (la clé est dans RouterIdentity)
   Dépend de cette proposition.
   Nécessite également une proposition pour 1), ou mettre la clé dans les options RI.

3) Cryptage ElGamal+AES/SessionTag de bout en bout client (la clé est dans LeaseSet, la clé de Destination est inutilisée)
   Le remplacement EST couvert dans cette proposition.

4) DH éphémère pour NTCP1 et SSU
   Le remplacement n'est pas couvert dans cette proposition.
   Voir la proposition 111 pour NTCP2.
   Aucune proposition actuelle pour SSU2.


### Objectifs

- Compatible en arrière
- Nécessite et se base sur LS2 (proposition 123)
- Exploite la nouvelle cryptographie ou les primitives ajoutées pour NTCP2 (proposition 111)
- Aucune nouvelle cryptographie ou primitives requises pour la prise en charge
- Maintient le découplage du cryptage et de la signature ; prend en charge toutes les versions actuelles et futures
- Permettre une nouvelle crypto pour les destinations
- Permettre une nouvelle crypto pour les routeurs, mais uniquement pour les messages garlic - la construction de tunnels serait
  une proposition séparée
- Ne pas casser quoi que ce soit qui repose sur des hachages de destination binaires de 32 octets, par exemple bittorrent
- Maintient la livraison de messages 0-RTT en utilisant DH éphémère-statique
- Ne pas nécessiter de mise en mémoire tampon / de mise en file d'attente des messages à ce niveau de protocole ;
  continue à prendre en charge la livraison illimitée de messages dans les deux directions sans attendre de réponse
- Mettre à niveau vers DH éphémère-éphémère après 1 RTT
- Maintenir le traitement des messages hors ordre
- Maintenir la sécurité de 256 bits
- Ajouter le secret de transmission
- Ajouter l'authentification (AEAD)
- Bien plus efficace en termes de CPU que ElGamal
- Ne pas dépendre de jbigi Java pour rendre DH efficace
- Minimiser les opérations DH
- Bien plus efficace en termes de bande passante que ElGamal (bloc ElGamal de 514 octets)
- Prendre en charge les cryptos nouveaux et anciens sur le même tunnel si nécessaire
- Le destinataire est capable de distinguer efficacement les nouveaux et anciens cryptos arrivant
  sur le même tunnel
- Les autres ne peuvent pas distinguer les cryptos nouveaux des anciens ou futurs
- Éliminer la classification de longueur de session nouvelle vs existante (prise en charge du remplissage)
- Aucun nouveau message I2NP requis
- Remplacer la somme de contrôle SHA-256 dans la charge utile AES par AEAD
- Prendre en charge la liaison des sessions d'émission et de réception afin que
  les accusés réception puissent avoir lieu dans le cadre du protocole, plutôt qu'exclusivement en dehors de la bande.
  Cela permettra également aux réponses d'avoir un secret de transmission immédiat.
- Permettre le cryptage de bout en bout de certains messages (magasins RouterInfo)
  que nous ne faisons pas actuellement en raison de la surcharge CPU.
- Ne pas changer le Message Garlic I2NP
  ou le format des instructions de livraison du Message Garlic.
- Éliminer les champs inutilisés ou redondants dans le Garlic Clove Set et les formats de Clove.

Éliminer plusieurs problèmes avec les étiquettes de session, y compris :

- Incapacité à utiliser AES jusqu'à la première réponse
- Fiabilité et arrêts si la livraison de l'étiquette est supposée
- Inefficace en termes de bande passante, surtout lors de la première livraison
- Énorme inefficacité en termes d'espace pour stocker les étiquettes
- Énorme surcharge de bande passante pour livrer les étiquettes
- Très complexe, difficile à mettre en œuvre
- Difficile à ajuster pour divers cas d'utilisation
  (streaming vs datagrammes, serveur vs client, bande passante élevée vs basse)
- Vulnérabilités d'épuisement de la mémoire dues à la livraison de l'étiquette


### Non-Objectifs / Hors du champ d'application

- Modifications du format LS2 (la proposition 123 est terminée)
- Nouvel algorithme de rotation DHT ou génération aléatoire partagée
- Nouveau cryptage pour la construction de tunnels.
  Voir la proposition 152 [Prop152](/en/proposals/152-ecies-tunnels/).
- Nouveau cryptage pour le cryptage de la couche de tunnel.
  Voir la proposition 153 [Prop153](/en/proposals/153-ecies-garlic/).
- Méthodes de cryptage, transmission et réception de messages I2NP DLM / DSM / DSRM.
  Pas de changement.
- Aucune communication LS1-à-LS2 ou ElGamal/AES-à-cette proposition n'est prise en charge.
  Cette proposition est un protocole bidirectionnel.
  Les destinations peuvent gérer la rétrocompatibilité en publiant deux ensembles de droits
  en utilisant les mêmes tunnels, ou mettre les deux types de cryptage dans le LS2.
- Changements de modèle de menace
- Les détails d'implémentation ne sont pas discutés ici et sont laissés à chaque projet.
- (Optimiste) Ajoutez des extensions ou des crochets pour prendre en charge la diffusion


### Justification

ElGamal/AES+SessionTag a été notre seul protocole de bout en bout pendant environ 15 ans,
essentiellement sans modifications du protocole.
Il existe maintenant des primitives cryptographiques qui sont plus rapides.
Nous devons améliorer la sécurité du protocole.
Nous avons également développé des stratégies heuristiques et des solutions de contournement pour minimiser la
consommation de mémoire et de bande passante du protocole, mais ces stratégies
sont fragiles, difficiles à ajuster et rendent le protocole encore plus sujet à
des interruptions, entraînant la chute de la session.

Pendant à peu près la même période, la spécification ElGamal/AES+SessionTag et la documentation connexe ont décrit à quel
point il est coûteux en bande passante de livrer des balises de session,
et ont proposé de remplacer la livraison des balises de session par un "PRNG synchronisé".
Un PRNG synchronisé génère de manière déterministe les mêmes balises aux deux extrémités,
dérivées d'une graine commune.
Un PRNG synchronisé peut également être qualifié de "cliquet".
Cette proposition (enfin) spécifie ce mécanisme de cliquet et élimine la livraison de balises.

En utilisant un cliquet (un PRNG synchronisé) pour générer les
balises de session, nous éliminons la surcharge d'envoi des balises de session
dans le message de nouvelle session et les messages suivants si nécessaire.
Pour un ensemble de balises typique de 32 balises, c'est 1 Ko.
Cela élimine également le stockage des balises de session sur le site émetteur,
réduisant ainsi de moitié les besoins en stockage.

Une poignée de main bidirectionnelle complète, similaire au modèle Noise IK, est nécessaire pour éviter les attaques d'usurpation de compromission de clé (KCI).
Voir le tableau des propriétés de sécurité de la charge utile Noise dans [NOISE](https://noiseprotocol.org/noise.html).
Pour plus d'informations sur le KCI, voir le document https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf


### Modèle de menace

Le modèle de menace est quelque peu différent de celui de NTCP2 (proposition 111).
Les nœuds MitM sont l'OBEP et l'IBGW et on suppose qu'ils ont une vision complète du
netDB mondial actuel ou historique, en collusion avec des floodfills.

L'objectif est d'empêcher ces MitM de classifier le trafic comme
nouveaux et existants messages de session, ou comme nouveau crypto contre ancien crypto.


## Proposition détaillée

Cette proposition définit un nouveau protocole de bout en bout pour remplacer ElGamal/AES+SessionTags.
La conception utilisera une phase de poignée de main et de données Noise incorporant le double cliquet Signal.


### Résumé de la conception cryptographique

Il y a cinq parties du protocole à redessiner :


- 1) Les nouveaux formats de conteneur de session et de session existante
  sont remplacés par de nouveaux formats.
- 2) ElGamal (clés publiques de 256 octets, clés privées de 128 octets) est remplacé
  par ECIES-X25519 (clés publiques et privées de 32 octets)
- 3) AES est remplacé par
  AEAD_ChaCha20_Poly1305 (abrégé en ChaChaPoly ci-dessous)
- 4) Les SessionTags seront remplacés par des cliquets,
  qui est essentiellement un PRNG synchronisé cryptographique.
- 5) La charge utile AES, telle que définie dans la spécification ElGamal/AES+SessionTags,
  est remplacée par un format de bloc similaire à celui de NTCP2.

Chacun des cinq changements a sa propre section ci-dessous.


### Nouvelles primitives cryptographiques pour I2P

Les implémentations actuelles du routeur I2P nécessiteront des implémentations pour
les primitives cryptographiques standard suivantes,
qui ne sont pas requises pour les protocoles I2P actuels :

- ECIES (mais c'est essentiellement X25519)
- Elligator2

Les implémentations actuelles du routeur I2P qui n'ont pas encore implémenté [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/))
nécessiteront également des implémentations pour :

- X25519 génération de clés et DH
- AEAD_ChaCha20_Poly1305 (abrégé en ChaChaPoly ci-dessous)
- HKDF


### Type de Crypto

Le type de crypto (utilisé dans le LS2) est 4.
Cela indique une clé publique X25519 de 32 octets en little-endian,
et le protocole de bout en bout spécifié ici.

Le type de crypto 0 est ElGamal.
Les types de crypto 1 à 3 sont réservés pour ECIES-ECDH-AES-SessionTag, voir la proposition 145 [Prop145](/en/proposals/145-ecies/).


### Cadre du protocole Noise

Cette proposition fournit les exigences basées sur le cadre du protocole Noise
[NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11).
Noise a des propriétés similaires au protocole Station-To-Station
[STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), qui est la base du protocole [SSU](/en/docs/transport/ssu/). En termes de Noise, Alice
est l'initiateur, et Bob est le répondeur.

Cette proposition est basée sur le protocole Noise Noise_IK_25519_ChaChaPoly_SHA256.
(L'identifiant réel pour la fonction de dérivation initiale des clés
est "Noise_IKelg2_25519_ChaChaPoly_SHA256"
pour indiquer les extensions de I2P - voir la section KDF 1 ci-dessous)
Ce protocole Noise utilise les primitives suivantes :

- Motif de poignée de main interactif : IK
  Alice transmet immédiatement sa clé statique à Bob (I)
  Alice connaît déjà la clé statique de Bob (K)

- Motif de poignée de main unilatéral : N
  Alice ne transmet pas sa clé statique à Bob (N)

- Fonction DH : X25519
  X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Fonction de chiffrement : ChaChaPoly
  AEAD_CHACHA20_POLY1305 tel que spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8.
  Nonce de 12 octets, avec les 4 premiers octets définis à zéro.
  Identique à celui de [NTCP2](/en/docs/transport/ntcp2/).

- Fonction de hachage : SHA256
  Hachage standard de 32 octets, déjà utilisé extensivement dans I2P.


Ajouts au cadre
``````````````````````````

Cette proposition définit les améliorations suivantes à
Noise_IK_25519_ChaChaPoly_SHA256. Ces améliorations suivent généralement les directives dans
[NOISE](https://noiseprotocol.org/noise.html) section 13.

1) Les clés éphémères en clair sont encodées avec [Elligator2](https://elligator.org/).

2) La réponse est préfixée avec une balise en clair.

3) Le format de la charge utile est défini pour les messages 1, 2 et la phase de données.
   Bien sûr, cela n'est pas défini dans Noise.

Tous les messages incluent un en-tête de message Garlic [I2NP](/en/docs/spec/i2np/).
La phase de données utilise un cryptage similaire, mais non compatible avec, la phase de données Noise.


### Motifs de poignée de main

Les poignées de main utilisent des motifs de poignée de main [Noise](https://noiseprotocol.org/noise.html).

La correspondance des lettres suivante est utilisée :

- e = clé éphémère unique
- s = clé statique
- p = charge utile du message

Les sessions uniques et non liées sont similaires au motif Noise N.

```dataspec

<- s
  ...
  e es p ->


```

Les sessions liées sont similaires au motif Noise IK.

```dataspec

<- s
  ...
  e es s ss p ->
  <- tag e ee se
  <- p
  p ->


```


### Sessions

Le protocole ElGamal/AES+SessionTag actuel est unidirectionnel.
À ce niveau, le récepteur ne sait pas d'où vient un message.
Les sessions sortantes et entrantes ne sont pas associées.
Les accusés de réception sont hors-bande à l'aide d'un DeliveryStatusMessage
(encapsulé dans un GarlicMessage) dans le clove.

Il y a une inefficacité substantielle dans un protocole unidirectionnel.
Toute réponse doit également utiliser un message coûteux de 'nouvelle session'.
Cela entraîne une consommation plus élevée de bande passante, de CPU et de mémoire.

Il y a également des faiblesses de sécurité dans un protocole unidirectionnel.
Toutes les sessions sont basées sur DH éphémère-statique.
Sans chemin de retour, il n'y a aucun moyen pour Bob de "cliqueter" sa clé statique
pour une clé éphémère.
Sans savoir d'où vient un message, il n'y a aucun moyen d'utiliser
la clé éphémère reçue pour les messages sortants,
donc la réponse initiale utilise également DH éphémère-statique.

Pour cette proposition, nous définissons deux mécanismes pour créer un protocole bidirectionnel -
"jumelage" et "liaison".
Ces mécanismes fournissent une efficacité et une sécurité accrues.


Contexte de session
`````````````````````

Comme pour ElGamal/AES+SessionTags, toutes les sessions entrantes et sortantes
doivent être dans un contexte donné, soit le contexte du routeur,
soit le contexte pour une destination locale particulière.
Dans Java I2P, ce contexte est appelé le gestionnaire de clés de session.

Les sessions ne doivent pas être partagées entre les contextes, car cela permettrait
de corréler les différentes destinations locales,
ou entre une destination locale et un routeur.

Lorsqu'une destination donnée prend en charge à la fois ElGamal/AES+SessionTags
et cette proposition, les deux types de sessions peuvent partager un contexte.
Voir section 1c) ci-dessous.



Appariement des sessions entrantes et sortantes
```````````````````````````````````````

Lorsqu'une session sortante est créée à l'initiatrice (Alice),
une nouvelle session entrante est créée et associée à la session sortante,
à moins qu'aucune réponse ne soit attendue (par exemple, datagrammes bruts).

Une nouvelle session entrante est toujours associée à une nouvelle session sortante,
à moins qu'aucune réponse ne soit demandée (par exemple, datagrammes bruts).

Si une réponse est demandée et liée à une destination ou un routeur distant,
cette nouvelle session sortante est liée à cette destination ou ce routeur,
et remplace toute session sortante précédente vers cette destination ou ce routeur.

L'appariement des sessions entrantes et sortantes fournit un protocole bidirectionnel
avec la capacité de cliqueter les clés DH.



Liaison des sessions et destinations
`````````````````````````````````````

Il n'y a qu'une seule session sortante vers une destination ou un routeur donné.
Il peut y avoir plusieurs sessions entrantes actuelles d'une destination ou d'un routeur donné.
Généralement, lorsqu'une nouvelle session entrante est créée et que le trafic est reçu
sur cette session (qui sert de ACK), tous les autres seront marqués
pour expirer relativement vite, en une minute ou moins.
La valeur des messages envoyés précédemment (PN) est vérifiée, et s'il n'y a pas de
messages non reçus (dans la taille de la fenêtre) dans la session entrante précédente,
la session précédente peut être supprimée immédiatement.


Lorsqu'une session sortante est créée à l'initiatrice (Alice),
elle est liée à la destination distante (Bob),
et toute session entrante appariée sera également liée à la destination distante.
À mesure que les sessions cliquettent, elles restent liées à la destination distante.

Lorsqu'une session entrante est créée chez le récepteur (Bob),
elle peut être liée à la destination distante (Alice), à la discrétion d'Alice.
Si Alice inclut des informations de liaison (sa clé statique) dans le message de nouvelle session,
la session sera liée à cette destination,
et une session sortante sera créée et liée à la même destination.
À mesure que les sessions cliquettent, elles restent liées à la destination distante.


Avantages de la liaison et de l'appariement
`````````````````````````````````````````

Pour le cas commun, de streaming, nous nous attendons à ce qu'Alice et Bob utilisent le protocole comme suit :

- Alice apparait sa nouvelle session sortante à une nouvelle session entrante, toutes deux liées à la destination distante (Bob).
- Alice inclut les informations de liaison et la signature, et une demande de réponse, dans le
  message de nouvelle session envoyé à Bob.
- Bob apparait sa nouvelle session entrante à une nouvelle session sortante, toutes deux liées à la destination distante (Alice).
- Bob envoie une réponse (ack) à Alice dans la session appariée, avec un cliquet vers une nouvelle clé DH.
- Alice fait un cliquet vers une nouvelle session sortante avec la nouvelle clé de Bob, appariée à la session entrante existante.

En liant une session entrante à une destination distante et en apparant la session entrante
à une session sortante liée à la même destination, nous obtenons deux avantages majeurs :

1) La réponse initiale de Bob à Alice utilise DH éphémère-éphémère

2) Après qu'Alice ait reçu la réponse de Bob et cliquetté, tous les messages suivants d'Alice à Bob
utilisent DH éphémère-éphémère.


Acks de message
```````````````

Dans ElGamal/AES+SessionTags, lorsque un LeaseSet est intégré en tant que clove d'ail,
ou que des balises sont livrées, le routeur expéditeur demande un ACK.
Il s'agit d'un clove d'ail séparé contenant un message DeliveryStatus.
Pour des raisons de sécurité supplémentaires, le message DeliveryStatus est enveloppé dans un Garlic Message.
Ce mécanisme est hors-bande du point de vue du protocole.

Dans le nouveau protocole, comme les sessions entrantes et sortantes sont appariées,
nous pouvons avoir des ACK en bande. Aucun clove séparé n'est nécessaire.

Un ACK explicite est simplement un message de session existante sans bloc I2NP.
Cependant, dans la plupart des cas, un ACK explicite peut être évité, car il y a du trafic en sens inverse.
Il peut être souhaitable pour les implémentations d'attendre un court instant (peut-être une centaine de ms)
avant d'envoyer un ACK explicite, pour donner le temps à la couche de streaming ou d'application de répondre.

Les implémentations devront également différer tout envoi d'ACK jusqu'à
ce que le bloc I2NP soit traité, car le Garlic Message peut contenir un Database Store Message
avec un lease set. Un lease set récent sera nécessaire pour acheminer l'ACK,
et la destination distante (contenue dans le lease set) sera nécessaire pour
vérifier la clé statique de liaison.


Timeouts de session
````````````````````

Les sessions sortantes doivent toujours expirer avant les sessions entrantes.
Une fois qu'une session sortante expire et qu'une nouvelle est créée, une nouvelle session entrante appariée
sera également créée. S'il y avait une ancienne session entrante,
elle sera autorisée à expirer.


### Diffusion

TBD


### Définitions
Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés.

ZEROLEN
    tableau de bytes de longueur zéro

CSRNG(n)
    sortie de n bytes par un générateur de nombre aléatoire cryptographiquement sécurisé.

H(p, d)
    fonction de hachage SHA-256 prenant une chaîne de personnalisation p et des données d, et
    produisant une sortie de longueur 32 bytes.
    Tel que défini dans [NOISE](https://noiseprotocol.org/noise.html).
    || ci-dessous signifie ajouter.

    Utiliser SHA-256 comme suit ::

        H(p, d) := SHA-256(p || d)

MixHash(d)
    fonction de hachage SHA-256 prenant un hachage précédent h et de nouvelles données d,
    et produisant une sortie de longueur 32 bytes.
    || ci-dessous signifie ajouter.

    Utiliser SHA-256 comme suit ::

        MixHash(d) := h = SHA-256(h || d)

STREAM
    Le ChaCha20/Poly1305 AEAD tel que spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539).
    S_KEY_LEN = 32 et S_IV_LEN = 12.

    ENCRYPT(k, n, plaintext, ad)
        Crypte plaintext en utilisant la clé de chiffre k, et le nonce n qui DOIT être unique pour
        la clé k.
        Les données associées ad sont facultatives.
        Retourne un ciphertext de la taille du plaintext + 16 bytes pour le HMAC.

        Tout le ciphertext doit être indiscernable du hasard si la clé est secrète.

    DECRYPT(k, n, ciphertext, ad)
        Décrypte ciphertext en utilisant la clé de chiffre k, et nonce n.
        Les données associées ad sont facultatives.
        Retourne le plaintext.

DH
    Le système de consensus public X25519. Clés privées de 32 bytes, clés publiques de 32
    bytes, produit des sorties de 32 bytes. Il a les fonctions suivantes :

    GENERATE_PRIVATE()
        Génère une nouvelle clé privée.

    DERIVE_PUBLIC(privkey)
        Retourne la clé publique correspondante à la clé privée donnée.

    GENERATE_PRIVATE_ELG2()
        Génère une nouvelle clé privée qui se transforme en une clé publique adaptée à un encodage Elligator2.
        Notez que la moitié des clés privées générées aléatoirement ne conviendront pas et doivent être rejetées.

    ENCODE_ELG2(pubkey)
        Retourne la clé publique encodée en Elligator2 correspondant à la clé publique donnée (mapping inverse).
        Les clés encodées sont en little endian.
        La clé encodée doit être de 256 bits indiscernables des données aléatoires.
        Voir la section Elligator2 ci-dessous pour la spécification.

    DECODE_ELG2(pubkey)
        Retourne la clé publique correspondant à la clé publique encodée en Elligator2 donnée.
        Voir la section Elligator2 ci-dessous pour la spécification.

    DH(privkey, pubkey)
        Génère un secret partagé à partir des clés privées et publiques données.

HKDF(salt, ikm, info, n)
    Une fonction cryptographique de dérivation des clés qui prend en entrée du matériau de clé ikm (qui
    doit avoir une bonne entropie mais n'est pas tenue d'être une chaîne aléatoire uniforme), un sel
    de longueur 32 bytes, et une valeur 'info' spécifique au contexte, et produit une sortie
    de n bytes adaptée à l'utilisation comme matériau de clé.

    Utiliser HKDF tel que spécifié dans [RFC-5869](https://tools.ietf.org/html/rfc5869), en utilisant la fonction de hachage HMAC SHA-256
    tel que spécifié dans [RFC-2104](https://tools.ietf.org/html/rfc2104). Cela signifie que SALT_LEN est de 32 bytes max.

MixKey(d)
    Utiliser HKDF() avec un chainKey précédent et de nouvelles données d, et
    définir le nouveau chainKey et k.
    Tel que défini dans [NOISE](https://noiseprotocol.org/noise.html).

    Utiliser HKDF comme suit ::

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]



### 1) Format des messages


Revue du format actuel des messages
````````````````````````````````````

Le message Garlic tel que spécifié dans [I2NP](/en/docs/spec/i2np/) est le suivant.
Comme l'objectif de conception est que les sauts intermédiaires ne peuvent pas distinguer le nouveau du ancien cryptage,
ce format ne peut pas changer, même si le champ de longueur est redondant.
Le format est affiché avec l'en-tête complet de 16 bytes, bien que le
l'en-tête réel puisse être dans un format différent, selon le transport utilisé.

Lorsque les données sont décryptées, elles contiennent une série de gousses d'ail et des
données supplémentaires, également connues sous le nom de Clove Set.

Voir [I2NP](/en/docs/spec/i2np/) pour les détails et une spécification complète.


```dataspec

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


Revue du format des données cryptées
````````````````````````````````````

Le format de message actuel, utilisé pendant plus de 15 ans,
est ElGamal/AES+SessionTags.
Dans ElGamal/AES+SessionTags, il y a deux formats de message :

1) Nouvelle session :
- Bloc ElGamal de 514 octets
- Bloc AES (128 octets minimum, multiple de 16)

2) Session existante :
- Balise de session de 32 octets
- Bloc AES (128 octets minimum, multiple de 16)

Le remplissage minimum à 128 est tel qu'implémenté dans Java I2P mais n'est pas appliqué lors de la réception.

Ces messages sont encapsulés dans un message garlic I2NP, qui contient
un champ de longueur, donc la longueur est connue.

Notez qu'il n'y a pas de remplissage défini à une longueur non mod-16,
donc la nouvelle session est toujours (mod 16 == 2),
et une session existante est toujours (mod 16 == 0).
Nous devons corriger cela.

Le récepteur tente d'abord de rechercher les 32 premiers octets comme balise de session.
Si trouvé, il décrypte le bloc AES.
Sinon trouvé, et les données font au moins (514+16) octets de long, il tente de déchiffrer le bloc ElGamal,
et s'il réussit, décrypte le bloc AES.


Nouvelles balises de session et comparaison avec Signal
`````````````````````````````````````````````````````

Dans le Signal Double Ratchet, l'en-tête contient :

- DH : Clé de cliquet actuelle
- PN : Longueur du message de chaîne précédent
- N : Numéro de message

Les "chaînes d'envoi" de Signal sont approximativement équivalentes à nos ensembles d'étiquettes.
En utilisant une balise de session, nous pouvons éliminer la plupart de cela.

Dans New Session, nous mettons uniquement la clé publique dans l'en-tête non crypté.

Dans Existing Session, nous utilisons une balise de session pour l'en-tête.
La balise de session est associée à la clé de cliquet actuelle,
et le numéro de message.

Dans les deux nouvelles et Existing Session, PN et N sont dans le corps crypté.

Dans Signal, les choses cliquetent constamment. Une nouvelle clé publique DH oblige le
récepteur à cliqueter et envoyer une nouvelle clé publique en retour, ce qui sert également
d'ack pour la clé publique reçue.
Cela représenterait bien trop d'opérations DH pour nous.
Donc nous séparons l'ack de la clé reçue et la transmission d'une nouvelle clé publique.
Tout message utilisant une balise de session générée à partir de la nouvelle clé publique DH constitue un ACK.
Nous ne transmettons une nouvelle clé publique que lorsque nous souhaitons réinitialiser la clé.

Le nombre maximum de messages avant que DH ne doit cliqueter est de 65535.

Lors de la livraison d'une clé de session, nous dérivons l'"Ensemble de balises" à partir de celle-ci,
plutôt que de devoir également livrer des balises de session.
Un Ensemble de balises peut contenir jusqu'à 65536 balises.
Cependant, les récepteurs doivent mettre en œuvre une stratégie de "regard vers l'avenir", plutôt
que de générer toutes les balises possibles en même temps.
Ne générez au maximum N balises au-delà de la dernière bonne balise reçue.
N pourrait être au maximum 128, mais 32 ou même moins pourrait être un meilleur choix.


### 1a) Format de nouvelle session

Nouvelle clé publique éphémère de session (32 octets)
Données cryptées et MAC (octets restants)

Le message de nouvelle session peut ou non contenir la clé publique statique de l'expéditeur.
Si elle est incluse, la session inversée est liée à cette clé.
La clé statique devrait être incluse si des réponses sont attendues,
c'est-à-dire pour le streaming et les datagrammes pouvant répondre.
Elle ne devrait pas être incluse pour les datagrammes bruts.

Le message de nouvelle session est similaire au modèle unidirectionnel de Noise [NOISE](https://noiseprotocol.org/noise.html)
"N" (si la clé statique n'est pas envoyée),
ou le modèle bidirectionnel "IK" (si la clé statique est envoyée).



### 1b) Format de nouvelle session (avec liaison)

La longueur est de 96 + longueur de la charge utile.
Format crypté :

```dataspec

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


Nouvelle clé éphémère de session
```````````````````````````

La clé éphémère est de 32 octets, encodée avec Elligator2.
Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec
chaque message, y compris les retransmissions.

Clé statique
````````````

Lors du décryptage, la clé statique X25519 d'Alice, 32 octets.


Charge utile
```````

La longueur cryptée est le reste des données.
La longueur décryptée est 16 de moins que la longueur cryptée.
La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove.
Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.



### 1c) Format de nouvelle session (sans liaison)

Si aucune réponse n'est requise, aucune clé statique n'est envoyée.


La longueur est de 96 + longueur de la charge utile.
Format crypté :

```dataspec

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

Nouvelle clé éphémère de session
`````````````````````````````````

La clé éphémère d'Alice.
La clé éphémère est de 32 octets, encodée avec Elligator2, little endian.
Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec
chaque message, y compris les retransmissions.


Section des drapeaux Données décryptées
````````````````````````````````````````

La section des drapeaux ne contient rien.
Elle est toujours de 32 octets, car elle doit être de la même longueur
que la clé statique pour les messages de nouvelle session avec liaison.
Bob détermine si c'est une clé statique ou une section de drapeaux
en testant si les 32 octets sont tous des zéros.

TODO des drapeaux nécessaires ici ?

Charge utile
```````

La longueur cryptée est le reste des données.
La longueur décryptée est 16 de moins que la longueur cryptée.
La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove.
Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.



### 1d) Format à usage unique (pas de liaison ni de session)

Si un seul message est censé être envoyé,
aucune configuration de session ou clé statique n'est requise.


La longueur est de 96 + longueur de la charge utile.
Format crypté :

```dataspec

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


Nouvelle clé éphémère d'une seule fois
````````````````````````````````````````

La clé unique est de 32 octets, encodée avec Elligator2, little endian.
Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec
chaque message, y compris les retransmissions.


Section des drapeaux Données décryptées
``````````````````````````````````````````

La section des drapeaux ne contient rien.
Elle est toujours de 32 octets, car elle doit être de la même longueur
que la clé statique pour les messages de nouvelle session avec liaison.
Bob détermine si c'est une clé statique ou une section de drapeaux
en testant si les 32 octets sont tous des zéros.

TO DO des drapeaux nécessaires ici ?

```dataspec

+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                                       |
  +             All zeros                 +
  |              32 bytes                 |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  zeros:: Tous les zéros, 32 octets.


```


Charge utile
```````

La longueur cryptée est le reste des données.
La longueur décryptée est 16 de moins que la longueur cryptée.
La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove.
Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.



### 1f) KDFs pour le Message de Nouvelle Session

KDF pour la Chaîne de clés Initiale
``````````````````````````````````

C'est du [NOISE](https://noiseprotocol.org/noise.html) standard pour IK avec un nom de protocole modifié.
Notez que nous utilisons le même initialiseur pour le modèle IK (sessions liées)
et pour le modèle N (sessions non liées).

Le nom du protocole est modifié pour deux raisons.
Premièrement, pour indiquer que les clés éphémères sont encodées avec Elligator2,
et deuxièmement, pour indiquer que MixHash() est appelé avant le deuxième message
pour mélanger la valeur de la balise.

```text

C'est le modèle de message "e" :

  // Définir protocol_name.
  Définir protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
   (40 bytes, US-ASCII encodé, sans terminaison NULL).

  // Définir Hash h = 32 bytes
  h = SHA256(protocol_name);

  Définir ck = chaîne d'appariement de 32 bytes. Copier les données h dans ck.
  Définir chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // jusqu'ici, tout peut être pré-calculé par Alice pour toutes les connexions sortantes


```


KDF pour le Contenu Crypté de la Section des Drapeaux / Clé Statique
````````````````````````````````````````````````````````````````````

```text

C'est le modèle de message "e" :

  // Clés statiques X25519 de Bob
  // bpk est publié dans leaseset
  bsk = GENERATE_PRIVATE()
  bpk = DERIVE_PUBLIC(bsk)

  // Clé publique statique de Bob
  // MixHash(bpk)
  // || ci-dessous signifie ajouter
  h = SHA256(h || bpk);

  // jusqu'ici, tout peut être pré-calculé par Bob pour toutes les connexions entrantes

  // Clés éphémères X25519 d'Alice
  aesk = GENERATE_PRIVATE_ELG2()
  aepk = DERIVE_PUBLIC(aesk)

  // Clé publique éphémère d'Alice
  // MixHash(aepk)
  // || ci-dessous signifie ajouter
  h = SHA256(h || aepk);

  // h est utilisé comme les données associées pour l'AEAD dans le message de nouvelle session
  // Retenir le Hash h pour le KDF de Nouvelle Session Réponse
  // eapk est envoyé en clair dans le
  // début du message de Nouvelle Session
  elg2_aepk = ENCODE_ELG2(aepk)
  // Tel que décodé par Bob
  aepk = DECODE_ELG2(elg2_aepk)

  Fin du modèle de message "e".

  C'est le modèle de message "es" :

  // Noise es
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Paramètres ChaChaPoly pour crypter/déchiffrer
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, section des drapeaux/clé statique, ad)

  Fin du modèle de message "es".

  C'est le modèle de message "s" :

  // MixHash(ciphertext)
  // Enregistrer pour KDF de Section de Charge utile
  h = SHA256(h || ciphertext)

  // Clés statiques X25519 d'Alice
  ask = GENERATE_PRIVATE()
  apk = DERIVE_PUBLIC(ask)

  Fin du modèle de message "s".



```



KDF pour la Section de Charge utile (avec clé statique d'Alice)
````````````````````````````````````````````````````````````````````

```text

C'est le modèle de message "ss" :

  // Noise ss
  sharedSecret = DH(ask, bpk) = DH(bsk, apk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Paramètres ChaChaPoly pour crypter/déchiffrer
  // chainKey de Section de Clé Statique
  Set sharedSecret = X25519 résultat DH
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, charge utile, ad)

  Fin du modèle de message "ss".

  // MixHash(ciphertext)
  // Enregistrer pour Nouvelle Session Réponse KDF
  h = SHA256(h || ciphertext)


```


KDF pour la Section de Charge utile (sans clé statique d'Alice)
``````````````````````````````````````````````````````````````````

Notez que ceci est un modèle "N" de Noise, mais nous utilisons le même initialiseur "IK"
que pour les sessions liées.

Les messages de Nouvelle Session ne peuvent pas être identifiés comme contenant la clé statique d'Alice ou non
jusqu'à ce que la clé statique soit décryptée et inspectée pour déterminer si elle contient tous des zéros.
Par conséquent, le récepteur doit utiliser la machine d'état "IK" pour tous
les messages de Nouvelle Session.
Si la clé statique est tous des zéros, le modèle de message "ss" doit être ignoré.



```text

chainKey = de Flags/Static key section
  k = de Flags/Static key section
  n = 1
  ad = h de Flags/Static key section
  ciphertext = ENCRYPT(k, n, charge utile, ad)


```



### 1g) Format de Réponse de Nouvelle Session

Une ou plusieurs Réponses de Nouvelle Session peuvent être envoyées en réponse à un seul message de Nouvelle Session.
Chaque réponse est préfixée par une balise, qui est générée à partir d'un TagSet pour la session.

La Réponse de Nouvelle Session est en deux parties.
La première partie est l'achèvement de la poignée de main Noise IK avec une balise préfixée.
La longueur de la première partie est de 56 octets.
La deuxième partie est la charge utile de la phase de données.
La longueur de la deuxième partie est de 16 + longueur de la charge utile.

La longueur totale est de 72 + longueur de la charge utile.
Format crypté :

```dataspec

+----+----+----+----+----+----+----+----+
  |       Balise de Session   8 bytes     |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Clé Publique Éphémère          +
  |                                       |
  +            32 bytes                   +
  |     Encoded with Elligator2           +
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
         Note: Le texte brut ChaCha20 est vide (ZEROLEN)

  Payload Section encrypted data :: remaining data minus 16 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```

Balise de session
`````````````````
La balise est générée dans le KDF des balises de session, comme initialisé
dans le DH Initialization KDF ci-dessous.
Cela corrèle la réponse à la session.
La clé de session du DH initiiateur n'est pas utilisée.

Clé Éphémère de Réponse de Nouvelle Session
````````````````````````````````````````````

La clé éphémère de Bob.
La clé éphémère est de 32 octets, encodée avec Elligator2, little endian.
Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec
chaque message, y compris les retransmissions.


Charge utile
```````
La longueur cryptée est le reste des données.
La longueur décryptée est 16 de moins que la longueur cryptée.
La charge utile contiendra généralement un ou plusieurs blocs Garlic Clove.
Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.


KDF pour l'Ensemble de Balises de Réponse
```````````````````````````````````````````

Une ou plusieurs balises sont créées à partir de l'Ensemble de Balises, qui est initialisé en utilisant
le KDF ci-dessous, en utilisant la clé de chaîne du message de Nouvelle Session.

```text

// Générer l'Ensemble de Balises
  tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
  tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)


```


KDF pour le Contenu Crypté de la Section Clé de Réponse
````````````````````````````````````````````````````````````

```text

// Clés de la message Nouvelle Session
  // Clés X25519 d'Alice
  // apk et aepk sont envoyés dans le message Nouvelle Session d'origine
  // ask = Clé privée statique d'Alice
  // apk = Clé publique statique d'Alice
  // aesk = Clé privée éphémère d'Alice
  // aepk = Clé publique éphémère d'Alice
  // Clés statiques X25519 de Bob
  // bsk = Clé privée statique de Bob
  // bpk = Clé publique statique de Bob

  // Générer la balise
  tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
  tag = tagsetEntry.SESSION_TAG

  // MixHash(tag)
  h = SHA256(h || tag)

  C'est le modelo de message "e" :

  // Clés éphémères X25519 de Bob
  besk = GENERATE_PRIVATE_ELG2()
  bepk = DERIVE_PUBLIC(besk)

  // Clé publique éphémère de Bob
  // MixHash(bepk)
  // || ci-dessous signifie ajouter
  h = SHA256(h || bepk);

  // elg2_bepk est envoyé en clair dans le
  // début du message Nouvelle Session
  elg2_bepk = ENCODE_ELG2(bepk)
  // Tel que décodé par Bob
  bepk = DECODE_ELG2(elg2_bepk)

  Fin du modèle de message "e".

  C'est le modèle de message "ee" :

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // Paramètres ChaChaPoly pour crypter/déchiffrer
  // chainKey du message de Section de Charge utile de la Nouvelle Session d'origine
  sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "", 32)
  chainKey = keydata[0:31]

  Fin du modèle de message "ee".

  C'est le modèle de message "se" :

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  sharedSecret = DH(ask, bepk) = DH(besk, apk)
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  chainKey = keydata[0:31]

  // Paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

  Fin du modèle de message "se".

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  chainKey est utilisé dans le cliquet ci-dessous.


```


KDF pour les Contenus Cryptés de la Section de Charge utile
````````````````````````````````````````````````````````````

C'est comme le premier message de session existante,
après division, mais sans balise séparée.
De plus, nous utilisons le hachage ci-dessus pour lier la
charge utile au message NSR.


```text

// split()
  keydata = HKDF(chainKey, ZEROLEN, "", 64)
  k_ab = keydata[0:31]
  k_ba = keydata[32:63]
  tagset_ab = DH_INITIALIZE(chainKey, k_ab)
  tagset_ba = DH_INITIALIZE(chainKey, k_ba)

  // Paramètres AEAD pour la charge utile de la Nouvelle Session Réponse
  k = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, charge utile, ad)

```


### Notes

Plusieurs messages NSR peuvent être envoyés en réponse, chacun avec des clés éphémères uniques, selon la taille de la réponse.

Alice et Bob sont tenus d'utiliser de nouvelles clés éphémères pour chaque message NS et NSR.

Alice doit recevoir un des messages NSR de Bob avant d'envoyer des messages de session existante (ES),
et Bob doit recevoir un message ES d'Alice avant d'envoyer des messages ES.

Les ``chainKey`` et ``k`` de la Section de Charge utile du NSR de Bob sont utilisés
comme entrées pour les cliquets DH initiaux ES (dans les deux directions, voir DH Ratchet KDF).

Bob doit seulement conserver les sessions existantes pour les messages ES reçus d'Alice.
Les autres sessions entrantes et sortantes créées (pour plusieurs NSR) doivent être
immédiatement détruites après avoir reçu le premier message ES d'Alice pour une session donnée.



### 1h) Format de session existante

Balise de session (8 octets)
Données cryptées et MAC (voir section 3 ci-dessous)


Format
``````
Crypté :

```dataspec

+----+----+----+----+----+----+----+----+
  |       Balise de Session               |
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


Charge utile
```````
La longueur cryptée est le reste des données.
La longueur décryptée est 16 de moins que la longueur cryptée.
Voir la section charge utile ci-dessous pour le format et les exigences.


KDF
```

```text

Voir la section AEAD ci-dessous.

  // Paramètres AEAD pour la charge utile de session existante
  k = La clé de session de 32 bytes associée à cette balise de session
  n = Le numéro de message N dans la chaîne actuelle, récupéré de la balise de session associée.
  ad = La balise de session, 8 bytes
  ciphertext = ENCRYPT(k, n, charge utile, ad)

```



### 2) ECIES-X25519


Format : clés publiques et privées de 32 octets, little-endian.

Justification : Utilisé dans [NTCP2](/en/docs/transport/ntcp2/).



### 2a) Elligator2

Dans les poignées de main Noise standard, les messages de poignée de main initiaux dans chaque direction commencent par
des clés éphémères qui sont transmises en clair.
Comme les clés X25519 valides sont distinguables au hasard, un homme du milieu pourrait distinguer
ces messages des messages de session existante qui commencent par des balises de session aléatoires.
Dans [NTCP2](/en/docs/transport/ntcp2/) ([Prop111](/en/proposals/111-ntcp2/)), nous avons utilisé une fonction XOR à faible surcharge utilisant la clé statique en dehors de bande pour obfusquer
la clé. Cependant, le modèle de menace est différent ici ; nous ne voulons permettre à aucun MitM
d'utiliser un quelconque moyen pour confirmer la destination du trafic, ou de distinguer
les messages de poignée de main initiaux des messages de session existante.

Par conséquent, [Elligator2](https://elligator.org/) est utilisé pour transformer les clés éphémères dans les messages Nouvelle Session et Réponse de Nouvelle Session
afin qu'elles soient indiscernables de chaînes aléatoires uniformes.



Format
``````

Clés publiques et privées de 32 octets.
Les clés encodées sont en little endian.

Tel que défini dans [Elligator2](https://elligator.org/), les clés encodées sont indiscernables de 254 bits aléatoires.
Nous avons besoin de 256 bits aléatoires (32 octets). Par conséquent, l'encodage et le décodage sont
définis comme suit :

Encodage :

```text

Définition ENCODE_ELG2()

  // Encodez comme défini dans la spécification Elligator2
  encodedKey = encode(pubkey)
  // OU en 2 bits aléatoires vers MSB
  randomByte = CSRNG(1)
  encodedKey[31] |= (randomByte & 0xc0)

```


Décodage :

```text

Définition DECODE_ELG2()

  // Masquez 2 bits aléatoires hors du MSB
  encodedKey[31] &= 0x3f
  // Décodez comme défini dans la spécification Elligator2
  pubkey = decode(encodedKey)

```




Justification
`````````````

Nécessaire pour empêcher l'OBEP et l'IBGW de classifier le trafic.


Notes
`````

Elligator2 double le temps moyen de génération des clés, car la moitié des clés privées
entraînent des clés publiques inadaptées à l'encodage avec Elligator2.
De plus, le temps de génération des clés est illimité avec une distribution exponentielle,
car le générateur doit continuer à réessayer jusqu'à ce qu'une paire de clés adaptées soit trouvée.

Cette surcharge peut être gérée en générant des clés à l'avance,
dans un thread séparé, pour maintenir un pool de clés adaptées.

Le générateur effectue la fonction ENCODE_ELG2() pour déterminer l'adéquation.
Par conséquent, le générateur doit stocker le résultat de ENCODE_ELG2()
pour qu'il n'ait pas à être calculé à nouveau.

De plus, les clés inadaptées peuvent être ajoutées au pool de clés
utilisées pour [NTCP2](/en/docs/transport/ntcp2/), où Elligator2 n'est pas utilisé.
Les questions de sécurité associées sont TBD.




### 3) AEAD (ChaChaPoly)

AEAD utilisant ChaCha20 et Poly1305, identique à [NTCP2](/en/docs/transport/ntcp2/).
Cela correspond à [RFC-7539](https://tools.ietf.org/html/rfc7539), qui est également
utilisé de manière similaire dans TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).



Entrées Nouvelle Session et Réponse de Nouvelle Session
````````````````````````````````````````````````````````````````

Entrées aux fonctions de chiffrement/déchiffrement
pour un bloc AEAD dans un message de Nouvelle Session :

```dataspec

k :: clé de chiffrement de 32 bytes
       Voir les KDFs de Nouvelle Session et Réponse de Nouvelle Session ci-dessus.

  n :: nonce basé sur le compteur, 12 bytes.
       n = 0

  ad :: données associées, 32 bytes.
        Le hachage SHA256 des données précédentes, tel que produit par mixHash()

  data :: données en clair, 0 ou plus bytes


```


Entrées de Session Existante
``````````````````````````````

Entrées aux fonctions de chiffrement/déchiffrement
pour un bloc AEAD dans un message de Session Existante :

```dataspec

k :: clé de session de 32 bytes
       Tel que recherché à partir de la balise de session d'accompagnement.

  n :: nonce basé sur le compteur, 12 bytes.
       Commence à 0 et s'incrémente pour chaque message lors de la transmission.
       Pour le récepteur, la valeur
       telle que recherchée à partir de la balise de session d'accompagnement.
       Les quatre premiers bytes sont toujours zéro.
       Les huit derniers bytes sont le numéro de message (n), encodé en little-endian.
       La valeur maximale est 65535.
       La session doit être cliquetée lorsque N atteint cette valeur.
       Les valeurs plus élevées ne doivent jamais être utilisées.

  ad :: données associées
        La balise de session

  data :: données en clair, 0 ou plus bytes


```


Format Crypté
````````````````

Sortie de la fonction de chiffrement, entrée de la fonction de déchiffrement :

```dataspec

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

  encrypted data :: Taille identique aux données en clair, 0 - 65519 bytes

  MAC :: Poly1305 message authentication code, 16 bytes


```

Notes
`````
- Comme ChaCha20 est un chiffrement par flux, les textes en clair n'ont pas besoin d'être remplis.
  Les octets de flux de clés supplémentaires sont ignorés.

- La clé pour le chiffrement (256 bits) est convenue par le biais de la fonction de dérivation de clés SHA256.
  Les détails de la fonction de dérivation de clés pour chaque message sont dans des sections séparées ci-dessous.

- Les trames ChaChaPoly sont de taille connue car elles sont encapsulées dans le message de données I2NP.

- Pour tous les messages,
  le remplissage est à l'intérieur du
  cadre authentifié.


Gestion des erreurs AEAD
```````````````````````````

Toutes les données reçues qui échouent à la vérification AEAD doivent être ignorées.
Aucune réponse n'est renvoyée.


Justification
`````````````

Utilisé dans [NTCP2](/en/docs/transport/ntcp2/).



### 4) Cliquets

Nous utilisons toujours des balises de session, comme auparavant, mais nous utilisons des cliquets pour les générer.
Les balises de session avaient également une option de réinitialisation de la clé que nous n'avons jamais implémentée.
Donc c'est comme un double cliquet mais nous n'en avons jamais fait le second.

Ici nous définissons quelque chose de similaire au double cliquet de Signal.
Les balises de session sont générées de manière déterministe et identique des deux côtés
récepteur et émetteur.

En utilisant un cliquet symétrique clé/balise, nous éliminons l'utilisation de la mémoire pour stocker les balises de session côté émetteur.
Nous éliminons également la consommation de bande passante d'envoi des ensembles de balises.
L'utilisation côté récepteur est toujours significative, mais nous pouvons la réduire encore plus
car nous allons réduire la balise de session de 32 octets à 8 octets.

Nous n'utilisons pas le cryptage d'en-tête tel que spécifié (et facultatif) dans Signal,
nous utilisons plutôt des balises de session.

En utilisant un cliquet DH, nous atteignons le secret de transfert, qui n'a jamais été implémenté
dans ElGamal/AES+SessionTags.

Remarque : La clé publique unique de Nouvelle Session ne fait pas partie du cliquet, sa seule fonction
est de crypter la clé de cliquet DH initiale d'Alice.


Numéros de messages
```````````````````````

Le Double Ratchet gère les messages perdus ou hors d'ordre en incluant dans chaque en-tête de message
une balise. Le récepteur recherche l'indice de la balise, c'est le numéro de message N.
Si le message contient un bloc Numéro de Message avec une valeur PN,
le récepteur peut supprimer toutes les balises supérieures à cette valeur dans l'ensemble de balises précédent,
tout en conservant les balises sautées
de l'ensemble de balises précédent au cas où les messages sautés arriveraient plus tard.


Exemple d'implémentation
````````````````````````````

Nous définissons les structures de données et fonctions suivantes pour implémenter ces cliquets.

ENTRY_TAGSET
    Une seule entrée dans un TAGSET.

    INDEX
        Un index entier, commençant à 0

    SESSION_TAG
        Un identifiant pour aller sur le fil, 8 bytes

    SESSION_KEY
        Une clé symétrique, ne va jamais sur le fil, 32 bytes

TAGSET
    Un ensemble de ENTRY_TAGSET.

    CREATE(key, n)
        Génère un nouveau TAGSET en utilisant un matériau de clé cryptographique initial de 32 bytes.
        L'identifiant de session associé est fourni.
        Le nombre initial de balises à créer est spécifié ; c'est généralement 0 ou 1
        pour une session sortante.
        LAST_INDEX = -1
        EXTEND(n) est appelé.

    EXTEND(n)
        Génère n autres ENTRY_TAGSET en appelant EXTEND() n fois.

    EXTEND()
        Génère un autre ENTRY_TAGSET, à moins que le nombre maximum de SESSION_TAGS ait
        déjà été généré.
        Si LAST_INDEX est supérieur ou égal à 65535, retour.
        ++ LAST_INDEX
        Crée un nouveau ENTRY_TAGSET avec la valeur LAST_INDEX et le SESSION_TAG calculé.
        Appelle RATCHET_TAG() et (éventuellement) RATCHET_KEY().
        Pour les sessions entrantes, le calcul du SESSION_KEY peut
        être reporté et calculé dans GET_SESSION_KEY().
        Appelle EXPIRE()

    EXPIRE()
