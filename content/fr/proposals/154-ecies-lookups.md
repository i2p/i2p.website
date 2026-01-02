---
title: "Recherches de base de données à partir de destinations ECIES"
number: "154"
author: "zzz"
created: "2020-03-23"
lastupdated: "2021-01-08"
status: "Closed"
thread: "http://zzz.i2p/topics/2856"
target: "0.9.46"
implementedin: "0.9.46"
toc: true
---

## Note
ECIES vers ElG est implémenté dans la version 0.9.46 et la phase de proposition est close.
Voir [I2NP](/docs/specs/i2np/) pour la spécification officielle.
Cette proposition peut encore être référencée pour des informations de contexte.
ECIES vers ECIES avec des clés incluses est implémenté à partir de la version 0.9.48.
La section ECIES-vers-ECIES (clés dérivées) peut être rouverte ou intégrée
dans une future proposition.

## Aperçu

### Définitions

- AEAD : ChaCha20/Poly1305
- DLM : Message de recherche de base de données I2NP
- DSM : Message de stockage de base de données I2NP
- DSRM : Réponse de recherche de base de données I2NP
- ECIES : ECIES-X25519-AEAD-Ratchet (proposition 144)
- ElG : ElGamal
- ENCRYPT(k, n, payload, ad) : Tel que défini dans [ECIES](/docs/specs/ecies/)
- LS : Leaseset
- lookup : DLM I2NP
- reply : DSM ou DSRM I2NP

### Résumé

Lors de l'envoi d'un DLM pour un LS à un floodfill, le DLM spécifie généralement
que la réponse soit étiquetée, chiffrée par AES, et envoyée à travers un tunnel vers la destination.
Le support des réponses chiffrées par AES a été ajouté dans la version 0.9.7.

Les réponses chiffrées par AES ont été spécifiées dans la version 0.9.7 pour minimiser la grande surcharge crypto
d'ElG, et parce qu'elles réutilisent la fonction tags/AES dans ElGamal/AES+SessionTags.
Cependant, les réponses AES peuvent être falsifiées à l'IBEP puisqu'il n'y a pas d'authentification,
et les réponses ne sont pas secrètes en avant.

Avec les destinations [ECIES](/docs/specs/ecies/), l'objectif de la proposition 144 est que
les destinations ne supportent plus les étiquettes de 32 octets et le décryptage AES.
Les détails n'ont pas été intentionnellement inclus dans cette proposition.

Cette proposition documente une nouvelle option dans le DLM pour demander des réponses chiffrées par ECIES.

### Objectifs

- Nouveaux drapeaux pour le DLM lorsqu'une réponse chiffrée est demandée à travers un tunnel vers une destination ECIES
- Pour la réponse, ajouter la confidentialité persistante et l'authentification de l'expéditeur résistante à
  l'usurpation d'identité en cas de compromission de la clé du demandeur (destination).
- Maintenir l'anonymat du demandeur
- Minimiser la surcharge crypto

### Non-Objectifs

- Aucun changement des propriétés de chiffrement ou de sécurité de la recherche (DLM).
  La recherche a une confidentialité persistante seulement pour la compromission de la clé du demandeur.
  Le chiffrement est fait avec la clé statique du floodfill.
- Aucun problème de confidentialité persistante ou d'authentification de l'expéditeur résistant à
  l'usurpation d'identité en cas de compromission de la clé du répondeur (floodfill).
  Le floodfill est une base de données publique et répondra aux recherches
  de n'importe qui.
- Ne pas concevoir de routeurs ECIES dans cette proposition.
  Où va la clé publique X25519 d'un routeur reste à déterminer.

## Alternatives

En l'absence d'une manière définie de chiffrer les réponses vers les destinations ECIES, il y a plusieurs alternatives :

1) Ne pas demander de réponses chiffrées. Les réponses seront non chiffrées.
Java I2P utilise actuellement cette approche.

2) Ajouter un support pour les étiquettes de 32 octets et les réponses chiffrées par AES pour les destinations uniquement ECIES,
et demander des réponses chiffrées par AES comme d'habitude. i2pd utilise actuellement cette approche.

3) Demander des réponses chiffrées par AES comme d'habitude, mais les router à travers des tunnels exploratoires vers le routeur.
Java I2P utilise actuellement cette approche dans certains cas.

4) Pour les destinations duales ElG et ECIES,
demander des réponses chiffrées par AES comme d'habitude. Java I2P utilise actuellement cette approche.
i2pd n'a pas encore implémenté de destinations crypto-duales.

## Conception

- Un nouveau format DLM ajoutera un bit au champ drapeaux pour spécifier des réponses chiffrées par ECIES.
  Les réponses chiffrées par ECIES utiliseront le format de message [ECIES](/docs/specs/ecies/) Session existante,
  avec une étiquette préfixée et une charge utile et un MAC ChaCha/Poly.

- Définir deux variantes. Une pour les routeurs ElG, où une opération DH n'est pas possible,
  et une pour les futurs routeurs ECIES, où une opération DH est possible et peut fournir
  une sécurité supplémentaire. À étudier davantage.

DH n'est pas possible pour les réponses des routeurs ElG car ils ne publient pas
une clé publique X25519.

## Spécification

Dans la spécification DLM (DatabaseLookup) [I2NP](/docs/specs/i2np/), apporter les modifications suivantes.

Ajouter le bit de drapeau 4 "ECIESFlag" pour les nouvelles options de chiffrement.

```text
flags ::
       bit 4: ECIESFlag
               avant la version 0.9.46 ignoré
               depuis la version 0.9.46 :
               0  => envoyer une réponse non chiffrée ou ElGamal
               1  => envoyer une réponse chiffrée par ChaCha/Poly en utilisant la clé incluse
                     (si l'étiquette est incluse dépend du bit 1)
```

Le bit de drapeau 4 est utilisé en combinaison avec le bit 1 pour déterminer le mode de chiffrement de la réponse.
Le bit de drapeau 4 ne doit être défini que lors de l'envoi à des routeurs avec la version 0.9.46 ou supérieure.

Dans le tableau ci-dessous,
"DH n/a" signifie que la réponse n'est pas chiffrée.
"DH non" signifie que les clés de réponse sont incluses dans la requête.
"DH oui" signifie que les clés de réponse sont dérivées de l'opération DH.

| Flag bits 4,1 | De Dest | Vers Routeur | Réponse | DH? | notes |
|---------------|---------|--------------|---------|-----|-------|
| 0 0            | Any     | Any          | no enc  | n/a | courant |
| 0 1            | ElG     | ElG          | AES     | non | courant |
| 0 1            | ECIES   | ElG          | AES     | non | solution de contournement i2pd |
| 1 0            | ECIES   | ElG          | AEAD    | non | cette proposition |
| 1 0            | ECIES   | ECIES        | AEAD    | non | 0.9.49 |
| 1 1            | ECIES   | ECIES        | AEAD    | oui | futur |

### ElG à ElG

La destination E한G envoie une recherche à un routeur ElG.

Modifications mineures dans la spécification pour vérifier le nouveau bit 4.
Aucun changement dans le format binaire existant.

Génération de clés de demandeur (clarification) :

```text
reply_key :: CSRNG(32) 32 octets de données aléatoires
  reply_tags :: Chacun est CSRNG(32) 32 octets de données aléatoires
```

Format du message (ajouter une vérification pour ECIESFlag) :

```text
reply_key ::
       32 octet `SessionKey` big-endian
       inclus uniquement si encryptionFlag == 1 ET ECIESFlag == 0, uniquement à partir de la version 0.9.7

  tags ::
       1 octet `Integer`
       plage de valeur valide : 1-32 (typiquement 1)
       le nombre d'étiquettes de réponse qui suivent
       inclus uniquement si encryptionFlag == 1 ET ECIESFlag == 0, uniquement à partir de la version 0.9.7

  reply_tags ::
       une ou plusieurs `SessionTag` de 32 octets (typiquement une)
       inclus uniquement si encryptionFlag == 1 ET ECIESFlag == 0, uniquement à partir de la version 0.9.7
```

### ECIES à ElG

La destination ECIES envoie une recherche à un routeur ElG.
Pris en charge depuis la version 0.9.46.

Les champs reply_key et reply_tags sont redéfinis pour une réponse chiffrée par ECIES.

Génération de clés de demandeur :

```text
reply_key :: CSRNG(32) 32 octets de données aléatoires
  reply_tags :: Chacun est CSRNG(8) 8 octets de données aléatoires
```

Format du message :
Redéfinir les champs reply_key et reply_tags comme suit :

```text
reply_key ::
       32 octet ECIES `SessionKey` big-endian
       inclus uniquement si encryptionFlag == 0 ET ECIESFlag == 1, uniquement à partir de la version 0.9.46

  tags ::
       1 octet `Integer`
       valeur requise : 1
       le nombre d'étiquettes de réponse qui suivent
       inclus uniquement si encryptionFlag == 0 ET ECIESFlag == 1, uniquement à partir de la version 0.9.46

  reply_tags ::
       une `SessionTag` ECIES de 8 octets
       inclus uniquement si encryptionFlag == 0 ET ECIESFlag == 1, uniquement à partir de la version 0.9.46
```

La réponse est un message de Session existante ECIES, tel que défini dans [ECIES](/docs/specs/ecies/).

```text
tag :: une reply_tag de 8 octets

  k :: une clé de session de 32 octets
     La clé de réponse.

  n :: 0

  ad :: Le reply_tag de 8 octets

  payload :: Données en clair, le DSM ou DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### ECIES à ECIES (0.9.49)

Destinations ou routeurs ECIES envoient une recherche à un routeur ECIES, avec des clés de réponse intégrées.
Pris en charge depuis la version 0.9.49.

Les routeurs ECIES ont été introduits dans la version 0.9.48, voir [Prop156](/proposals/156-ecies-routers/).
À partir de la version 0.9.49, les destinations et routeurs ECIES peuvent utiliser le même format que dans
la section "ECIES à ElG" ci-dessus, avec des clés de réponse incluses dans la requête.
La recherche utilisera le format "one time" dans [ECIES](/docs/specs/ecies/)
car le demandeur est anonyme.

Pour une nouvelle méthode avec des clés dérivées, voir la section suivante.

### ECIES à ECIES (futur)

Destinations ou routeurs ECIES envoient une recherche à un routeur ECIES, et les clés de réponse sont dérivées du DH.
Non entièrement défini ou pris en charge, l'implémentation est à déterminer.

La recherche utilisera le format "one time" dans [ECIES](/docs/specs/ecies/)
car le demandeur est anonyme.

Redéfinir le champ reply_key comme suit. Il n'y a pas d'étiquettes associées.
Les étiquettes seront générées dans le KDF ci-dessous.

Cette section est incomplète et nécessite une étude plus approfondie.

```text
reply_key ::
       32 octet X25519 `PublicKey` éphémère du demandeur, little-endian
       inclus uniquement si encryptionFlag == 1 ET ECIESFlag == 1, uniquement à partir de la version 0.9.TBD
```

La réponse est un message de Session existante ECIES, tel que défini dans [ECIES](/docs/specs/ecies/).
Voir [ECIES](/docs/specs/ecies/) pour toutes les définitions.

```text
// Clés éphémères X25519 d'Alice
  // aesk = clé privée éphémère d'Alice
  aesk = GENERATE_PRIVATE()
  // aepk = clé publique éphémère d'Alice
  aepk = DERIVE_PUBLIC(aesk)
  // Clés statiques X25519 de Bob
  // bsk = clé statique privée de Bob
  bsk = GENERATE_PRIVATE()
  // bpk = clé statique publique de Bob
  // bpk fait partie de RouterIdentity, ou publié dans RouterInfo (à déterminer)
  bpk = DERIVE_PUBLIC(bsk)

  // (DH()
  //[chainKey, k] = MixKey(sharedSecret)
  // chainKey de ???
  sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)
  keydata = HKDF(chainKey, sharedSecret, "ECIES-DSM-Reply1", 32)
  chainKey = keydata[0:31]

  1) rootKey = chaîne de clé de la section Payload
  2) k de la nouvelle session KDF ou split()

  // KDF_RK(rk, dh_out)
  keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

  // Sortie 1: inutilisé
  unused = keydata[0:31]
  // Sortie 2: La chaîne de clé pour initialiser le nouveau
  // session tag et chaîne de clé symétrique
  // pour les transmissions d'Alice vers Bob
  ck = keydata[32:63]

  // chaîne de clés de session tag et de clés symétriques
  keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
  sessTag_ck = keydata[0:31]
  symmKey_ck = keydata[32:63]

  tag :: une étiquette de 8 octets générée à partir de RATCHET_TAG() dans [ECIES](/docs/specs/ecies/)

  k :: une clé de 32 octets générée à partir de RATCHET_KEY() dans [ECIES](/docs/specs/ecies/)

  n :: L'indice de l'étiquette. Typiquement 0.

  ad :: L'étiquette de 8 octets

  payload :: Données en clair, le DSM ou DSRM.

  ciphertext = ENCRYPT(k, n, payload, ad)
```

### Format de réponse

Ceci est le message de session existante,
comme dans [ECIES](/docs/specs/ecies/), copié ci-dessous pour référence.

```text
+----+----+----+----+----+----+----+----+
  |       Étiquette de session               |
  +----+----+----+----+----+----+----+----+
  |                                         |
  +           Section de charge             +
  |        Données chiffrées par ChaCha20   |
  ~                                         ~
  |                                         |
  +                                         +
  |                                         |
  +----+----+----+----+----+----+----+----+
  | Message d'authentification Poly1305    |
  +              (MAC)                      +
  |             16 octets                   |
  +----+----+----+----+----+----+----+----+

  Étiquette de session :: 8 octets, en clair

  Données chiffrées de la section de charge :: données restantes sauf 16 octets

  MAC :: code d'authentification par message Poly1305, 16 octets
```

## Justification

Les paramètres de chiffrement de réponse dans la recherche, introduits pour la première fois dans la version 0.9.7,
sont quelque peu une violation de la couche. C'est fait ainsi pour l'efficacité.
Mais aussi parce que la recherche est anonyme.

Nous pourrions rendre le format de recherche générique, comme avec un champ de type de chiffrement,
mais cela serait probablement plus problématique que bénéfique.

La proposition ci-dessus est la plus simple et minimise le changement du format de recherche.

## Notes

Les recherches et stockages dans la base de données vers les routeurs ElG doivent être chiffrés par ElGamal/AESSessionTag
comme d'habitude.

## Problèmes

Une analyse plus approfondie est nécessaire sur la sécurité des deux options de réponse ECIES.

## Migration

Aucun problème de compatibilité rétroactive. Les routeurs annonçant une version de routeur 0.9.46 ou plus dans leur RouterInfo
doivent supporter cette fonctionnalité.
Les routeurs ne doivent pas envoyer un DatabaseLookup avec les nouveaux drapeaux à des routeurs avec une version inférieure à 0.9.46.
Si un message de recherche de base de données avec le bit 4 défini et le bit 1 non défini est envoyé par erreur à un
routeur sans support, il ignorera probablement la clé et l'étiquette fournies et
enverra la réponse non chiffrée.
