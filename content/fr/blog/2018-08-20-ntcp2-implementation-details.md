---
title: "Détails de l'implémentation de NTCP2"
date: 2018-08-20
author: "villain"
description: "Détails d'implémentation et spécifications techniques du nouveau protocole de transport d'I2P"
categories: ["development"]
---

Les protocoles de transport d’I2P ont été initialement développés il y a environ 15 ans. À l’époque, l’objectif principal était de cacher les données transférées, pas de dissimuler le fait même d’utiliser le protocole. Personne ne pensait sérieusement à se protéger contre la DPI (inspection approfondie des paquets) et la censure des protocoles. Les temps changent, et bien que les protocoles de transport d’origine fournissent toujours une sécurité robuste, une demande s’est fait sentir pour un nouveau protocole de transport. NTCP2 est conçu pour résister aux menaces de censure actuelles. Principalement, l’analyse par DPI de la longueur des paquets. De plus, le nouveau protocole utilise les avancées cryptographiques les plus récentes. NTCP2 est basé sur le [Noise Protocol Framework](https://noiseprotocol.org/noise.html), avec SHA256 comme fonction de hachage et x25519 comme courbe elliptique pour l’échange de clés Diffie-Hellman (DH).

La spécification complète du protocole NTCP2 peut être [consultée ici](/docs/specs/ntcp2/).

## Nouvelle cryptographie

NTCP2 nécessite l’ajout des algorithmes cryptographiques suivants à une implémentation I2P :

- x25519
- HMAC-SHA256
- Chacha20
- Poly1305
- AEAD
- SipHash

Par rapport à notre protocole d'origine, NTCP, NTCP2 utilise x25519 au lieu d'ElGamal pour la fonction DH, AEAD/Chaha20/Poly1305 au lieu d'AES-256-CBC/Adler32, et utilise SipHash pour ofusquer la longueur du paquet. La fonction de dérivation de clés utilisée dans NTCP2 est plus complexe, utilisant désormais de nombreux appels HMAC-SHA256.

*i2pd (C++) note d’implémentation : Tous les algorithmes mentionnés ci‑dessus, à l’exception de SipHash, sont implémentés dans OpenSSL 1.1.0. SipHash sera ajouté dans la prochaine version 1.1.1 d’OpenSSL. Pour assurer la compatibilité avec OpenSSL 1.0.2, utilisé dans la plupart des systèmes actuels, le développeur principal d’i2pd, [Jeff Becker](https://github.com/majestrate), a fourni des implémentations autonomes des algorithmes cryptographiques manquants.*

## Modifications de RouterInfo

NTCP2 requiert une troisième clé (x25519) en plus des deux existantes (les clés de chiffrement et de signature). On l’appelle une clé statique et elle doit être ajoutée à chacune des adresses RouterInfo sous forme de paramètre "s". Elle est requise tant pour l’initiateur NTCP2 (Alice) que pour le répondant (Bob). Si plus d’une adresse prend en charge NTCP2, par exemple IPv4 et IPv6, "s" doit être identique pour toutes. L’adresse d’Alice peut n’avoir que le paramètre "s" sans "host" ni "port" définis. Un paramètre "v" est également requis, actuellement toujours défini à "2".

Une adresse NTCP2 peut être déclarée comme une adresse NTCP2 distincte ou comme une adresse NTCP de style ancien avec des paramètres supplémentaires, auquel cas elle acceptera à la fois des connexions NTCP et NTCP2. L’implémentation Java d’I2P utilise la seconde approche, i2pd (implémentation C++) utilise la première.

Si un nœud accepte des connexions NTCP2, il doit publier son RouterInfo avec le paramètre "i", qui est utilisé comme vecteur d'initialisation (IV) de la clé publique lorsque ce nœud établit de nouvelles connexions.

## Établir une connexion

Pour établir une connexion, les deux parties doivent générer des paires de clés x25519 éphémères. À partir de ces clés et de clés "statiques", elles dérivent un ensemble de clés pour le transfert de données. Les deux parties doivent vérifier que l’autre côté possède effectivement une clé privée pour cette clé statique, et que cette clé statique est la même que dans RouterInfo.

Trois messages sont envoyés pour établir une connexion :

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
Une clé partagée x25519, appelée « input key material » (matériel de clé d’entrée), est calculée pour chaque message, après quoi la clé de chiffrement du message est générée à l’aide d’une fonction MixKey. Une valeur ck (chaining key, clé de chaînage) est conservée pendant que les messages sont échangés. Cette valeur est utilisée comme entrée finale lors de la génération des clés pour le transfert de données.

La fonction MixKey ressemble à ceci dans l’implémentation C++ d’I2P :

```cpp
void NTCP2Establisher::MixKey (const uint8_t * inputKeyMaterial, uint8_t * derived)
{
    // temp_key = HMAC-SHA256(ck, input_key_material)
    uint8_t tempKey[32]; unsigned int len;
    HMAC(EVP_sha256(), m_CK, 32, inputKeyMaterial, 32, tempKey, &len);
    // ck = HMAC-SHA256(temp_key, byte(0x01))
    static uint8_t one[1] =  { 1 };
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_CK, &len);
    // derived = HMAC-SHA256(temp_key, ck || byte(0x02))
    m_CK[32] = 2;
    HMAC(EVP_sha256(), tempKey, 32, m_CK, 33, derived, &len);
}
```
Le message **SessionRequest** est composé d’une clé publique x25519 d’Alice (32 octets), d’un bloc de données chiffré avec AEAD/Chacha20/Poly1305 (16 octets), d’un hachage (16 octets) et de quelques données aléatoires à la fin (padding, remplissage). La longueur du padding est définie dans le bloc de données chiffré. Le bloc chiffré contient également la longueur de la seconde partie du message **SessionConfirmed**. Ce bloc de données est chiffré et signé avec une clé dérivée de la clé éphémère d’Alice et de la clé statique de Bob. La valeur initiale de ck pour la fonction MixKey est définie sur SHA256 (Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256).

Étant donné que 32 octets de clé publique x25519 peuvent être détectés par l’inspection approfondie des paquets (DPI), ils sont chiffrés avec l’algorithme AES-256-CBC en utilisant le hachage de l’adresse de Bob comme clé et le paramètre "i" de RouterInfo comme vecteur d’initialisation (IV).

Le message **SessionCreated** a la même structure que **SessionRequest**, sauf que la clé est calculée à partir des clés éphémères des deux parties. L’IV (vecteur d’initialisation) généré après le chiffrement/déchiffrement de la clé publique du message **SessionRequest** est utilisé comme IV pour le chiffrement/déchiffrement de la clé publique éphémère.

Le message **SessionConfirmed** comporte 2 parties : la clé publique statique et le RouterInfo d'Alice. La différence par rapport aux messages précédents est que la clé publique éphémère est chiffrée avec AEAD/Chaha20/Poly1305 en utilisant la même clé que pour **SessionCreated**. Cela a pour effet d'augmenter la première partie du message de 32 à 48 octets. La seconde partie est également chiffrée avec AEAD/Chaha20/Poly1305, mais en utilisant une nouvelle clé, calculée à partir de la clé éphémère de Bob et de la clé statique d'Alice. La partie RouterInfo peut également être complétée par un bourrage de données aléatoires, mais ce n'est pas nécessaire, puisque RouterInfo a généralement une longueur variable.

## Génération des clés de transfert de données

Si toutes les vérifications de hachage et de clé ont réussi, une valeur ck commune doit être présente après la dernière opération MixKey des deux côtés. Cette valeur est utilisée pour générer deux ensembles de clés <k, sipk, sipiv> pour chaque côté d'une connexion. "k" est une clé AEAD/Chaha20/Poly1305, "sipk" est une clé SipHash, "sipiv" est une valeur initiale pour l'IV SipHash (vecteur d'initialisation), qui est modifiée après chaque utilisation.

Le code utilisé pour générer des clés ressemble à ceci dans l’implémentation C++ d’I2P :

```cpp
void NTCP2Session::KeyDerivationFunctionDataPhase ()
{
    uint8_t tempKey[32]; unsigned int len;
    // temp_key = HMAC-SHA256(ck, zerolen)
    HMAC(EVP_sha256(), m_Establisher->GetCK (), 32, nullptr, 0, tempKey, &len);
    static uint8_t one[1] =  { 1 };
    // k_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Kab, &len);
    m_Kab[32] = 2;
    // k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Kab, 33, m_Kba, &len);
    static uint8_t ask[4] = { 'a', 's', 'k', 1 }, master[32];
    // ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, ask, 4, master, &len);
    uint8_t h[39];
    memcpy (h, m_Establisher->GetH (), 32);
    memcpy (h + 32, "siphash", 7);
    // temp_key = HMAC-SHA256(ask_master, h || "siphash")
    HMAC(EVP_sha256(), master, 32, h, 39, tempKey, &len);
    // sip_master = HMAC-SHA256(temp_key, byte(0x01))
    HMAC(EVP_sha256(), tempKey, 32, one, 1, master, &len);
    // temp_key = HMAC-SHA256(sip_master, zerolen)
    HMAC(EVP_sha256(), master, 32, nullptr, 0, tempKey, &len);
   // sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
    HMAC(EVP_sha256(), tempKey, 32, one, 1, m_Sipkeysab, &len);
    m_Sipkeysab[32] = 2;
     // sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02))
    HMAC(EVP_sha256(), tempKey, 32, m_Sipkeysab, 33, m_Sipkeysba, &len);
}
```
*i2pd (C++) note d’implémentation : Les 16 premiers octets du tableau "sipkeys" constituent une clé SipHash, les 8 derniers octets sont l’IV. SipHash nécessite deux clés de 8 octets, mais i2pd les traite comme une seule clé de 16 octets.*

## Transfert de données

Les données sont transférées sous forme de trames, chaque trame comporte 3 parties :

- 2 bytes of frame length obfuscated with SipHash
- data encrypted with Chacha20
- 16 bytes of Poly1305 hash value

La longueur maximale des données transférées dans une trame est de 65 519 octets.

La longueur du message est masquée en appliquant la fonction XOR avec les deux premiers octets de l’IV (vecteur d’initialisation) SipHash actuel.

La partie de données chiffrées contient des blocs de données. Chaque bloc est précédé d’un en-tête de 3 octets, qui définit le type et la longueur du bloc. En général, des blocs de type I2NP sont transmis ; il s’agit de messages I2NP dont l’en-tête est modifié. Une trame NTCP2 peut transférer plusieurs blocs I2NP.

L’autre type important de bloc de données est un bloc de données aléatoire. Il est recommandé d’ajouter un bloc de données aléatoire à chaque trame NTCP2. Un seul bloc de données aléatoire peut être ajouté et il doit être le dernier bloc.

Voici d'autres blocs de données utilisés dans l'implémentation NTCP2 actuelle :

- **RouterInfo** — usually contains Bob's RouterInfo after the connection has been established, but it can also contain RouterInfo of a random node for the purpose of speeding up floodfills (there is a flags field for that case).
- **Termination** — is used when a host explicitly terminates a connection and specifies a reason for that.
- **DateTime** — a current time in seconds.

## Résumé


Le nouveau protocole de transport I2P NTCP2 offre une résistance efficace à la censure par inspection approfondie des paquets (DPI). Il en résulte une réduction de la charge du processeur grâce à une cryptographie moderne plus rapide. Cela rend plus probable l’exécution d’I2P sur des appareils d’entrée de gamme, comme les smartphones et les routeurs domestiques. Les deux principales implémentations d’I2P prennent entièrement en charge NTCP2 et rendent NTCP2 disponible à partir des versions 0.9.36 (Java) et 2.20 (i2pd, C++).
