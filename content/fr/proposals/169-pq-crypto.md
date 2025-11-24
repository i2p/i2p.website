---
title: "Protocoles de cryptographie post-quantique"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Ouvert"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
---

## Aperçu

Bien que la recherche et la compétition pour une cryptographie post-quantique (PQ) appropriée se poursuivent depuis une décennie, les choix ne sont devenus clairs que récemment.

Nous avons commencé à examiner les implications de la cryptographie PQ en 2022 [FORUM](http://zzz.i2p/topics/3294).

Les standards TLS ont ajouté un support de chiffrement hybride ces deux dernières années et sont désormais utilisés pour une part importante du trafic crypté sur Internet grâce au support dans Chrome et Firefox [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/).

NIST a récemment finalisé et publié les algorithmes recommandés pour la cryptographie post-quantique [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Plusieurs bibliothèques de cryptographie courantes supportent maintenant les standards NIST ou vont bientôt publier un support.

Tant [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) que [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recommandent que la migration commence immédiatement. Voir aussi la FAQ 2022 de la NSA sur la PQ [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P devrait être un leader en matière de sécurité et de cryptographie. Il est temps de mettre en œuvre les algorithmes recommandés. En utilisant notre système flexible de type de crypto et de type de signature, nous ajouterons des types pour la crypto hybride, et pour les signatures PQ et hybrides.


## Objectifs

- Sélectionner des algorithmes résistants à la PQ
- Ajouter des algorithmes uniquement PQ et hybrides aux protocoles I2P où cela est approprié
- Définir plusieurs variantes
- Sélectionner les meilleures variantes après implémentation, test, analyse et recherche
- Ajouter un support de manière progressive et avec compatibilité descendante


## Non-objectifs

- Ne pas modifier les protocoles de chiffrement à sens unique (Noise N)
- Ne pas s'éloigner de SHA256, pas menacé à court terme par PQ
- Ne pas sélectionner les variantes finales préférées pour le moment


## Modèle de menace

- Routeurs à l'OBEP ou l'IBGW, pouvant collaborer, stockant des messages d'ail pour un déchiffrement ultérieur (secret de transmission)
- Observateurs du réseau stockant les messages de transport pour un déchiffrement ultérieur (secret de transmission)
- Participants au réseau falsifiant des signatures pour RI, LS, streaming, datagrammes, ou autres structures


## Protocoles affectés

Nous allons modifier les protocoles suivants, plus ou moins dans l'ordre de développement. Le déploiement global s'étendra probablement de fin 2025 à mi-2027. Voir la section Priorités et déploiement ci-dessous pour plus de détails.


| Protocole / Fonctionnalité | Statut |
| -------------------------- | ------ |
| Hybride MLKEM Ratchet et LS | Approu |
| Hybride MLKEM NTCP2 | Quelqu |
| Hybride MLKEM SSU2 | Quelqu |
| MLDSA SigTypes 12-14 | Propos |
| MLDSA Dests | Testé |
| Hybrid SigTypes 15-17 | Prélim |
| Hybrid Dests |  |




## Conception

Nous prendrons en charge les standards NIST FIPS 203 et 204 [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
qui sont basés sur, mais NE sont PAS compatibles avec,
CRYSTALS-Kyber et CRYSTALS-Dilithium (versions 3.1, 3 et plus anciennes).



### Échange de clés

Nous prendrons en charge l'échange de clés hybride dans les protocoles suivants :

| Proto | Noise Type | Supporte uniquem | t PQ?  Supporte |
| ----- | ---------- | ---------------- | --------------- |
| NTCP2 | XK | non | oui |
| SSU2 | XK | non | oui |
| Ratchet | IK | non | oui |
| TBM | N | non | non |
| NetDB | N | non | non |


PQ KEM fournit uniquement des clés éphémères et ne supporte pas directement
les échanges de clés statiques tels que Noise XK et IK.

Noise N n'utilise pas un échange de clés bidirectionnel et il n'est donc pas adapté
au chiffrement hybride.

Nous ne supporterons donc que le chiffrement hybride, pour NTCP2, SSU2 et Ratchet.
Nous définirons les trois variantes ML-KEM comme dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf),
pour un total de 3 nouveaux types de chiffrement.
Les types hybrides ne seront définis qu'en combinaison avec X25519.

Les nouveaux types de chiffrement sont :

| Type | Code |
| ---- | ---- |
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |


La surcharge sera substantielle. Les tailles typiques des messages 1 et 2 (pour XK et IK)
sont actuellement d'environ 100 octets (avant toute charge utile supplémentaire).
Cela augmentera de 8x à 15x selon l'algorithme.


### Signatures

Nous prendrons en charge les signatures PQ et hybrides dans les structures suivantes :

| Type | Supporte uniquem | t PQ?  Supporte |
| ---- | ---------------- | --------------- |
| RouterInfo | oui | oui |
| LeaseSet | oui | oui |
| Streaming SYN/SYNACK/Close | oui | oui |
| Repliable Datagrams | oui | oui |
| Datagram2 (prop. 163) | oui | oui |
| I2CP create session msg | oui | oui |
| SU3 files | oui | oui |
| X.509 certificates | oui | oui |
| Java keystores | oui | oui |



Nous prendrons donc en charge à la fois les signatures uniquement PQ et hybrides.
Nous définirons les trois variantes ML-DSA comme dans [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf),
trois variantes hybrides avec Ed25519,
et trois variantes uniquement PQ avec pré-hachage pour les fichiers SU3 uniquement,
pour un total de 9 nouveaux types de signatures.
Les types hybrides ne seront définis qu'en combinaison avec Ed25519.
Nous utiliserons la ML-DSA standard, PAS les variantes de pré-hachage (HashML-DSA),
à l'exception des fichiers SU3.

Nous utiliserons la variante de signature "hedged" ou aléatoire,
pas la variante "déterministe", telle que définie dans [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) section 3.4.
Cela garantit que chaque signature est différente, même lorsqu'elle est appliquée aux mêmes données,
et procure une protection supplémentaire contre les attaques par canaux auxiliaires.
Voir la section des notes d'implémentation ci-dessous pour des détails supplémentaires
sur les choix d'algorithmes, y compris le codage et le contexte.


Les nouveaux types de signature sont :

| Type | Code |
| ---- | ---- |
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |


Les certificats X.509 et autres codages DER utiliseront les
structures composites et OIDs définis dans [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).

La surcharge sera substantielle. Les tailles typiques des destinations Ed25519 et des identités de routeur
sont de 391 octets.
Celles-ci augmenteront de 3.5x à 6.8x selon l'algorithme.
Les signatures Ed25519 mesurent 64 octets.
Celles-ci augmenteront de 38x à 76x selon l'algorithme.
Les RouterInfo signés typiques, les LeaseSet, les datagrammes répliables et les messages de streaming signés sont d'environ 1Ko.
Ceux-ci augmenteront de 3x à 8x selon l'algorithme.

Étant donné que les nouveaux types de destination et d'identité de routeur ne contiendront pas de remplissage,
ils ne seront pas compressibles. Les tailles des destinations et des identités de routeurs
qui sont compressées en transit augmenteront de 12x à 38x selon l'algorithme.



### Combinaisons légales

Pour les destinations, les nouveaux types de signature sont pris en charge avec tous les types de chiffrement
dans le leaseset. Définir le type de chiffrement dans le certificat de clé sur NONE (255).

Pour les identités de routeurs, le type de chiffrement ElGamal est obsolète.
Les nouveaux types de signature sont pris en charge uniquement avec le chiffrement X25519 (type 4).
Les nouveaux types de chiffrement seront indiqués dans les adresses de routeur.
Le type de chiffrement dans le certificat de clé continuera d'être de type 4.



### Nouveautés de la crypto requises

- ML-KEM (anciennement CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anciennement CRYSTALS-Dilithium) [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anciennement Keccak-256) [FIPS202]_ Utilisé uniquement pour SHAKE128
- SHA3-256 (anciennement Keccak-512) [FIPS202]_
- SHAKE128 et SHAKE256 (extensions XOF de SHA3-128 et SHA3-256) [FIPS202]_

Les vecteurs de test pour SHA3-256, SHAKE128 et SHAKE256 sont disponibles sur [NIST-VECTORS]_.

Notez que la bibliothèque Java bouncycastle supporte tout ce qui précède.
Le support des bibliothèques C++ est dans OpenSSL 3.5 [OPENSSL]_.


### Alternatives

Nous ne prendrons pas en charge [FIPS205]_ (Sphincs+), c'est beaucoup plus lent et volumineux que ML-DSA.
Nous ne prendrons pas en charge le futur FIPS206 (Falcon), il n'est pas encore standardisé.
Nous ne prendrons pas en charge NTRU ou d'autres candidats PQ qui n'ont pas été standardisés par le NIST.


Rosenpass
``````````

Il y a quelques recherches [PQ-WIREGUARD]_ sur l'adaptation de Wireguard (IK)
pour une crypto pure PQ, mais il y a plusieurs questions ouvertes dans ce document.
Plus tard, cette approche a été implémentée sous le nom de Rosenpass [Rosenpass]_ [Rosenpass-Whitepaper]_
pour le Wireguard PQ.

Rosenpass utilise une poignée de main semblable à Noise KK avec des clés statiques Classic McEliece 460896 préséchées
(500 KB chacune) et des clés éphémères Kyber-512 (essentiellement MLKEM-512).
Comme les textes chiffrés Classic McEliece ne mesurent que 188 octets, et que les clés publiques et les textes chiffrés Kyber-512 sont raisonnables, chaque message de poignée de main tient dans un MTU UDP standard.
La clé partagée en sortie (osk) de la poignée de main PQ KK est utilisée comme clé préséchée en entrée (psk)
pour la poignée de main IK standard de Wireguard.
Il y a donc deux poignées de main complètes au total, une pure PQ et une pure X25519.

Nous ne pouvons pas faire tout cela pour remplacer nos poignées de main XK et IK parce que :

- Nous ne pouvons pas faire KK, Bob n'a pas la clé statique d'Alice
- Les clés statiques de 500KB sont beaucoup trop grandes
- Nous ne voulons pas d'un aller-retour supplémentaire

Il y a beaucoup d'informations intéressantes dans le livre blanc,
et nous les examinerons pour des idées et de l'inspiration. À faire.



## Spécification

### Structures communes

Mettre à jour les sections et tableaux dans le document sur les structures communes [COMMON](https://geti2p.net/spec/common-structures) comme suit :


PublicKey
````````````````

Les nouveaux types de clé publique sont :

| Type | Longueur clé publ | que De | is |
| ---- | ----------------- | ------ | --- |
| MLKEM512_X25519 | 32 | 0.9.xx | Voir |
| MLKEM768_X25519 | 32 | 0.9.xx | Voir |
| MLKEM1024_X25519 | 32 | 0.9.xx | Voir |
| MLKEM512 | 800 | 0.9.xx | Voir |
| MLKEM768 | 1184 | 0.9.xx | Voir |
| MLKEM1024 | 1568 | 0.9.xx | Voir |
| MLKEM512_CT | 768 | 0.9.xx | Voir |
| MLKEM768_CT | 1088 | 0.9.xx | Voir |
| MLKEM1024_CT | 1568 | 0.9.xx | Voir |
| NONE | 0 | 0.9.xx | Voir |


Les clés publiques hybrides sont la clé X25519.
Les clés publiques KEM sont la clé PQ éphémère envoyée de Alice à Bob.
Le codage et l'ordre des octets sont définis dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Les clés MLKEM*_CT ne sont pas vraiment des clés publiques, elles sont le "texte chiffré" envoyé de Bob à Alice dans la poignée de main Noise.
Elles sont listées ici pour compléter l'information.



PrivateKey
````````````````

Les nouveaux types de clé privée sont :

| Type | Longueur clé privé | Depui | Usa |
| ---- | ------------------ | ----- | --- |
| MLKEM512_X25519 | 32 | 0.9.xx | Voir |
| MLKEM768_X25519 | 32 | 0.9.xx | Voir |
| MLKEM1024_X25519 | 32 | 0.9.xx | Voir |
| MLKEM512 | 1632 | 0.9.xx | Voir |
| MLKEM768 | 2400 | 0.9.xx | Voir |
| MLKEM1024 | 3168 | 0.9.xx | Voir |


Les clés privées hybrides sont les clés X25519.
Les clés privées KEM sont uniquement pour Alice.
Le codage KEM et l'ordre des octets sont définis dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).




SigningPublicKey
````````````````

Les nouveaux types de clé publique de signature sont :

| Type | Longueur (octe | )  Dep | s   U |
| ---- | -------------- | ------ | ----- |
| MLDSA44 | 1312 | 0.9.xx | Voir |
| MLDSA65 | 1952 | 0.9.xx | Voir |
| MLDSA87 | 2592 | 0.9.xx | Voir |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Voir |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Voir |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Voir |
| MLDSA44ph | 1344 | 0.9.xx | Seule |
| MLDSA65ph | 1984 | 0.9.xx | Seule |
| MLDSA87ph | 2624 | 0.9.xx | Seule |


Les clés publiques de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Le codage et l'ordre des octets sont définis dans [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).


SigningPrivateKey
`````````````````

Les nouveaux types de clé privée de signature sont :

| Type | Longueur (octe | )  Dep | s   U |
| ---- | -------------- | ------ | ----- |
| MLDSA44 | 2560 | 0.9.xx | Voir |
| MLDSA65 | 4032 | 0.9.xx | Voir |
| MLDSA87 | 4896 | 0.9.xx | Voir |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Voir |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Voir |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Voir |
| MLDSA44ph | 2592 | 0.9.xx | Seule |
| MLDSA65ph | 4064 | 0.9.xx | Seule |
| MLDSA87ph | 4928 | 0.9.xx | Seule |


Les clés privées de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Le codage et l'ordre des octets sont définis dans [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).


Signature
``````````

Les nouveaux types de signature sont :

| Type | Longueur (octe | )  Dep | s   U |
| ---- | -------------- | ------ | ----- |
| MLDSA44 | 2420 | 0.9.xx | Voir |
| MLDSA65 | 3309 | 0.9.xx | Voir |
| MLDSA87 | 4627 | 0.9.xx | Voir |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Voir |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Voir |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Voir |
| MLDSA44ph | 2484 | 0.9.xx | Seule |
| MLDSA65ph | 3373 | 0.9.xx | Seule |
| MLDSA87ph | 4691 | 0.9.xx | Seule |


Les signatures hybrides sont la signature Ed25519 suivie de la signature PQ, comme dans [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ounsworth-pq-composite-sigs/).
Les signatures hybrides sont vérifiées en vérifiant les deux signatures et échouant
si l'une des deux échoue.
Le codage et l'ordre des octets sont définis dans [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).



Certificats de clé
``````````````````

Les nouveaux types de clé publique de signature sont :

| Type | Code de typ | Longueur totale de l | clé pu | ique |
| ---- | ----------- | -------------------- | ------ | ---- |
| MLDSA44 | 12 | 1312 | 0.9.xx | Voir |
| MLDSA65 | 13 | 1952 | 0.9.xx | Voir |
| MLDSA87 | 14 | 2592 | 0.9.xx | Voir |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Voir |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Voir |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Voir |
| MLDSA44ph | 18 | n/a | 0.9.xx | Seule |
| MLDSA65ph | 19 | n/a | 0.9.xx | Seule |
| MLDSA87ph | 20 | n/a | 0.9.xx | Seule |




Les nouveaux types de clé publique Crypto sont :

| Type | Code de typ | Longueur totale de l | clé p | lique |
| ---- | ----------- | -------------------- | ----- | ----- |
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Voir |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Voir |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Voir |
| NONE | 255 | 0 | 0.9.xx | Voir |



Les types de clé hybrides ne sont JAMAIS inclus dans les certificats de clé ; seulement dans les leasesets.

Pour les destinations avec des types de signature Hybride ou PQ,
utiliser NONE (type 255) pour le type de chiffrement,
mais il n'y a pas de clé de crypto, et la
entière section de 384 octets est pour la clé de signature.


Tailles de destination
``````````````````````

Voici les longueurs pour les nouveaux types de destination.
Le type enc pour tous est NONE (type 255) et la longueur de la clé de chiffrement est considérée comme 0.
La section entière de 384 octets est utilisée pour la première partie de la clé publique de signature.
NOTE : Cela est différent de la spécification pour les types de signature ECDSA_SHA512_P521
et RSA, où nous avons maintenu la clé ElGamal de 256 octets dans la destination même si elle était inutilisée.

Pas de remplissage.
La longueur totale est de 7 + longueur totale de la clé.
La longueur du certificat de clé est de 4 + longueur excédentaire de la clé.

Exemple de flux d'octets de destination de 1319 octets pour MLDSA44 :

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]



| Type | Code de typ | Longueur totale de l | clé pu | ique | incip |
| ---- | ----------- | -------------------- | ------ | ---- | ----- |
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |




Tailles de RouterIdent
``````````````````````

Voici les longueurs pour les nouveaux types de destination.
Le type enc pour tous est X25519 (type 4).
La section entière de 352 octets après la clé publique X28819 est utilisée pour la première partie de la clé publique de signature.
Pas de remplissage.
La longueur totale est de 39 + longueur totale de la clé.
La longueur du certificat de clé est de 4 + longueur excédentaire de la clé.

Exemple de flux d'octets d'identité de routeur de 1351 octets pour MLDSA44 :

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]



| Type | Code de typ | Longueur totale de l | clé pu | ique | incip |
| ---- | ----------- | -------------------- | ------ | ---- | ----- |
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |




### Modèles de poignée de main

Les poignées de main utilisent les modèles de poignée de main [Noise].

La correspondance des lettres suivante est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message
- e1 = clé éphémère PQ à usage unique, envoyée d'Alice à Bob
- ekem1 = le texte chiffré KEM, envoyé de Bob à Alice

Les modifications suivantes à XK et IK pour le secret de transmission hybride (hfs) sont
comme spécifié dans [Noise-Hybrid]_ section 5 :

```dataspec

XK :                       XKhfs :
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK :                       IKhfs :
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 et ekem1 sont chiffrés. Voir les définitions de modèle ci-dessous.
  NOTE : e1 et ekem1 ont des tailles différentes (contrairement à X25519)

```

Le modèle e1 est défini comme suit, tel que spécifié dans [Noise-Hybrid]_ section 4 :

```dataspec

Pour Alice :
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  Pour Bob :

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)


```


Le modèle ekem1 est défini comme suit, tel que spécifié dans [Noise-Hybrid]_ section 4 :

```dataspec

Pour Bob :

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  Pour Alice :

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)


```




### KDF de poignée de main Noise

Problèmes
``````

- Devons-nous changer la fonction de hachage de la poignée de main ? Voir [Choosing-Hash]_.
  SHA256 n'est pas vulnérable à la PQ, mais si nous voulons mettre à jour
  notre fonction de hachage, c'est maintenant, pendant que nous changeons d'autres choses.
  La proposition IETF SSH actuelle [SSH-HYBRID]_ est d'utiliser MLKEM768
  avec SHA256, et MLKEM1024 avec SHA384. Cette proposition inclut
  une discussion sur les considérations de sécurité.
- Devrions-nous cesser d'envoyer des données de cliquet 0-RTT (autres que la LS) ?
- Devons-nous passer le cliquet d'IK à XK si nous n'envoyons pas de données 0-RTT ?


Aperçu
````````

Cette section s'applique aux protocoles IK et XK.

La poignée de main hybride est définie dans [Noise-Hybrid]_.
Le premier message, d'Alice à Bob, contient e1, la clé d'encapsulation, avant la charge utile du message.
Cela est traité comme une clé statique supplémentaire; appeler EncryptAndHash() dessus (en tant qu'Alice)
ou DecryptAndHash() (en tant que Bob).
Puis traiter la charge utile du message comme d'habitude.

Le second message, de Bob à Alice, contient ekem1, le texte chiffré, avant la charge utile du message.
Cela est traité comme une clé statique supplémentaire; appeler EncryptAndHash() dessus (en tant que Bob)
ou DecryptAndHash() (en tant qu'Alice).
Ensuite, calculer la kem_shared_key et appeler MixKey(kem_shared_key).
Puis traiter la charge utile du message comme d'habitude.


Opérations ML-KEM définies
`````````````````````````

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés
tels que définis dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()
    Alice crée les clés d'encapsulation et de décapsulation
    La clé d'encapsulation est envoyée dans le message 1.
    Les tailles encap_key et decap_key varient en fonction de la variante ML-KEM.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)
    Bob calcule le texte chiffré et la clé partagée,
    en utilisant le texte chiffré reçu dans le message 1.
    Le texte chiffré est envoyé dans le message 2.
    La taille du texte chiffré varie en fonction de la variante ML-KEM.
    La kem_shared_key a toujours 32 octets.

kem_shared_key = DECAPS(ciphertext, decap_key)
    Alice calcule la clé partagée,
    en utilisant le texte chiffré reçu dans le message 2.
    La kem_shared_key a toujours 32 octets.

Notez que les encap_key et ciphertext sont chiffrés à l'intérieur des blocs ChaCha/Poly
dans les messages 1 et 2 de la poignée de main Noise.
Ils seront déchiffrés dans le cadre du processus de poignée de main.

La kem_shared_key est mélangée dans la clé de chaînage avec MixHash().
Voir ci-dessous pour les détails.


KDF pour le Message 1 d'Alice
```````````````````````````

Pour XK : Après le modèle de message 'es' et avant la charge utile, ajouter :

OU

Pour IK : Après le modèle de message 'es' et avant le modèle de message 's', ajouter :

```text
Ceci est le modèle de message "e1" :
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  Fin du modèle de message "e1".

  NOTE: Pour la section suivante (charge utile pour XK ou clé statique pour IK),
  les keydata et chain key restent les mêmes,
  et n maintenant égale 1 (au lieu de 0 pour non-hybride).

```


KDF pour le Message 1 de Bob
```````````````````````````

Pour XK : Après le modèle de message 'es' et avant la charge utile, ajouter :

OU

Pour IK : Après le modèle de message 'es' et avant le modèle de message 's', ajouter :

```text
Ceci est le modèle de message "e1" :

  // DecryptAndHash(encap_key_section)
  // paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  Fin du modèle de message "e1".

  NOTE: Pour la section suivante (charge utile pour XK ou clé statique pour IK),
  les keydata et chain key restent les mêmes,
  et n maintenant égale 1 (au lieu de 0 pour non-hybride).

```


KDF pour le Message 2 de Bob
```````````````````````````

Pour XK : Après le modèle de message 'ee' et avant la charge utile, ajouter :

OU

Pour IK : Après le modèle de message 'ee' et avant le modèle de message 'se', ajouter :

```text
Ceci est le modèle de message "ekem1" :

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Fin du modèle de message "ekem1".

```


KDF pour le Message 2 d'Alice
```````````````````````````

Après le modèle de message 'ee' (et avant le modèle de message 'ss' pour IK), ajouter :

```text
Ceci est le modèle de message "ekem1" :

  // DecryptAndHash(kem_ciphertext_section)
  // paramètres AEAD
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  Fin du modèle de message "ekem1".

```


KDF pour le message 3 (XK uniquement)
```````````````````````````
inchangé


KDF pour split()
```````````````
inchangé



### Ratchet

Mettre à jour la spécification ECIES-Ratchet [ECIES](https://geti2p.net/spec/ecies) comme suit :


Identifiants Noise
`````````````````

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"



1b) Nouveau format de session (avec liaison)
`````````````````````````````````````

Changements : Le ratchet actuel contenait la clé statique dans la première section ChaCha,
et la charge utile dans la deuxième section.
Avec ML-KEM, il y a maintenant trois sections.
La première section contient la clé publique PQ chiffrée.
La deuxième section contient la clé statique.
La troisième section contient la charge utile.


Format chiffré :

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Nouvelle clé publique éphémère de session  |
  +             32 octets                  +
  |     Codé avec Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Clé d'encapsulation ML-KEM            +
  |       Données chiffrées avec ChaCha20         |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +    (MAC) pour la section encap_key        +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           Clé statique X25519           +
  |       Données chiffrées avec ChaCha20         |
  +             32 octets                  +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +    (MAC) pour la section Clé statique       +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Section de charge utile            +
  |       Données chiffrées avec ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +         (MAC) pour la section de charge utile     +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+


```

Format déchiffré :

```dataspec
Partie 1 de la charge utile :

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       encap_key ML-KEM                +
  |                                       |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Partie 2 de la charge utile :

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Clé statique X25519               +
  |                                       |
  +      (32 octets)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Partie 3 de la charge utile :

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Section de charge utile            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tailles :

| Type | Code de t | e  X | n  Msg 1 | n  Msg 1 Enc | n  Msg 1 Dec | n  Longueu | de clé |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ------ |
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |


Notez que la charge utile doit contenir un bloc DateTime, donc la taille minimale de la charge utile est 7.
Les tailles minimales des messages 1 peuvent être calculées en conséquence.



1g) Nouveau format de réponse de session
````````````````````````````

Changements : Le ratchet actuel a une charge utile vide pour la première section ChaCha,
et la charge utile dans la deuxième section.
Avec ML-KEM, il y a maintenant trois sections.
La première section contient le texte chiffré PQ.
La deuxième section a une charge utile vide.
La troisième section contient la charge utile.


Format chiffré :

```dataspec
+----+----+----+----+----+----+----+----+
  |       Étiquette de session   8 octets           |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Clé publique éphémère           +
  |                                       |
  +            32 octets                   +
  |     Codé avec Elligator2           |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  | ChaCha20 texte chiffré de ML-KEM  |
  +      (voir tableau ci-dessous pour la longueur)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +  (MAC) pour la section de texte chiffré         +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +  (MAC) pour la section de clé (pas de données)      +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Section de charge utile            +
  |       Données chiffrées avec ChaCha20         |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Code d'authentification de message Poly1305 |
  +         (MAC) pour la section de charge utile     +
  |             16 octets                  |
  +----+----+----+----+----+----+----+----+


```

Format déchiffré :

```dataspec
Partie 1 de la charge utile :


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Texte chiffré ML-KEM               +
  |                                       |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Partie 2 de la charge utile :

  vide

  Partie 3 de la charge utile :

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Section de charge utile            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tailles :

| Type | Code de t | e  Y | n  Msg 2 | n  Msg 2 Enc | n  Msg 2 Dec | n  Longueu | CT PQ |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |


Notez que tant bien que mal, le message 2 aura normalement une charge utile non nulle,
la spécification du cliquet [ECIES](https://geti2p.net/spec/ecies) ne l'exige pas, donc la taille minimale de la charge utile est 0.
Les tailles minimales des messages 2 peuvent être calculées en conséquence.



### NTCP2

Mettre à jour la spécification NTCP2 [NTCP2](https://geti2p.net/spec/ntcp2) comme suit :


Identifiants Noise
`````````````````

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


1) Demande de session
````````````````````

Changements : NTCP2 actuel ne contient que les options dans la section ChaCha.
Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.


Contenu brut :

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfusqué avec RH_B           +
  |       X chiffré avec AES-CBC-256         |
  +             (32 octets)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Trame ChaChaPoly (MLKEM)            |
  +      (voir tableau ci-dessous pour la longueur)     +
  |   k défini dans KDF pour le message 1      |
  +   n = 0                               +
  |   voir KDF pour les données associées         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Trame ChaChaPoly (options)          |
  +         32 octets                      +
  |   k défini dans KDF pour le message 1      |
  +   n = 0                               +
  |   voir KDF pour les données associées         |
  +----+----+----+----+----+----+----+----+
  |     rembourrage authentifié non chiffré         |
  ~         (optionnel)            ~
  |     longueur définie dans le bloc options   |
  +----+----+----+----+----+----+----+----+

  Identique à avant sauf ajout d'une deuxième trame ChaChaPoly


```

Données non chiffrées (tag d'authentification Poly1305 non affiché) :

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Clé d'encapsulation ML-KEM            |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 octets)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     rembourrage authentifié non chiffré         |
  +         (optionnel)            +
  |     longueur définie dans le bloc options   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+



```

Tailles :

| Type | Code de t | e  X | n  Msg 1 | n  Msg 1 Enc | n  Msg 1 Dec | n  Longueu | de clé |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ------ |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |


Note : Les codes de type sont uniquement pour un usage interne. Les routeurs resteront de type 4,
et le support sera indiqué dans les adresses de routeur.


2) SessionCreated
``````````````````

Changements : NTCP2 actuel ne contient que les options dans la section ChaCha.
Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.


Contenu brut :

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfusqué avec RH_B           +
  |       Y chiffré avec AES-CBC-256         |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Trame ChaChaPoly (MLKEM)            |
  +   Données chiffrées et authentifiées | 
  -      (voir tableau ci-dessous pour la longueur)     -
  +   k défini dans KDF pour le message 2      +
  |   n = 0; voir KDF pour les données associées  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Trame ChaChaPoly (options)          |
  +   Données chiffrées et authentifiées      +
  -           32 octets                    -
  +   k défini dans KDF pour le message 2      +
  |   n = 0; voir KDF pour les données associées  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     rembourrage authentifié non chiffré         |
  +         (optionnel)            +
  |     longueur définie dans le bloc options   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Identique à avant sauf ajout d'une deuxième trame ChaChaPoly

```

Données non chiffrées (tag d'authentification Poly1305 non affiché) :

```dataspec
+----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Texte chiffré ML-KEM           |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 octets)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     rembourrage authentifié non chiffré         |
  +         (optionnel)            +
  |     longueur définie dans le bloc options   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

```

Tailles :

| Type | Code de t | e  Y | n  Msg 2 | n  Msg 2 Enc | n  Msg 2 Dec | n  Longueu | CT PQ |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |


Note : Les codes de type sont uniquement pour un usage interne. Les routeurs resteront de type 4,
et le support sera indiqué dans les adresses de routeur.



3) SessionConfirmed
```````````````````

Inchangé


Fonction de dérivation de clé (KDF) (pour la phase de données)
`````````````````````````````````````

Inchangé




### SSU2

Mettre à jour la spécification SSU2 [SSU2](https://geti2p.net/spec/ssu2) comme suit :


Identifiants Noise
`````````````````

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"


En-tête long
`````````````
L'en-tête long est de 32 octets. Il est utilisé avant qu'une session ne soit créée, pour la demande de jeton, la SessionRequest, la SessionCreated, et la tentative.
Il est également utilisé pour les messages de test et de perçage hors session.

TODO : Nous pourrions utiliser en interne le champ de version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768.
Doit-on le faire uniquement pour les types 0 et 1 ou pour tous les 6 types ?


Avant le chiffrement de l'en-tête :

```dataspec

+----+----+----+----+----+----+----+----+
  |      ID de connexion de destination        |
  +----+----+----+----+----+----+----+----+
  |   Numéro de paquet   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de connexion source           |
  +----+----+----+----+----+----+----+----+
  |                 Jeton                 |
  +----+----+----+----+----+----+----+----+

  ID de connexion de destination :: Entier de 8 octets, non signé, gros-boutiste

  Numéro de paquet :: Entier de 4 octets, non signé, gros-boutiste

  type :: Type de message = 0, 1, 7, 9, 10, ou 11

  ver :: Version du protocole, égale à 2
         TODO Nous pourrions utiliser en interne le champ de version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768.

  id :: 1 octet, l'ID du réseau (actuellement 2, sauf pour les réseaux de test)

  flag :: 1 octet, inutilisé, fixé à 0 pour une compatibilité future

  ID de connexion source :: Entier de 8 octets, non signé, gros-boutiste

  Jeton :: Entier de 8 octets, non signé, gros-boutiste

```


En-tête court
`````````````
inchangé


SessionRequest (Type 0)
```````````````````````

Changements : SSU2 actuel contient uniquement les données de bloc dans la section ChaCha.
Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.


Contenu brut :

```dataspec
+----+----+----+----+----+----+----+----+
  |  Octets d'en-tête long 0-15, ChaCha20     |
  +  chiffré avec la clé d'intro de Bob         +
  |    Voir KDF de chiffrement de l'en-tête          |
  +----+----+----+----+----+----+----+----+
  |  Octets d'en-tête long 16-31, ChaCha20    |
  +  chiffré avec la clé d'intro de Bob n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, chiffré avec ChaCha20           +
  |       avec la clé d'intro de Bob n=0          |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Données chiffrées avec ChaCha20 (MLKEM)     |
  +          (longueur varie)              +
  |  k défini dans KDF pour la demande de session |
  +  n = 0                                +
  |  voir KDF pour les données associées        |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   Données chiffrées avec ChaCha20 (payload)   |
  +          (longueur varie)              +
  |  k défini dans KDF pour la demande de session |
  +  n = 0                                +
  |  voir KDF pour les données associées        |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC Poly1305 (16 octets)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Données non chiffrées (tag d'authentification Poly1305 non affiché) :

```dataspec
+----+----+----+----+----+----+----+----+
  |      ID de connexion de destination        |
  +----+----+----+----+----+----+----+----+
  |   Numéro de paquet   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de connexion source           |
  +----+----+----+----+----+----+----+----+
  |                 Jeton                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Clé d'encapsulation ML-KEM            |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Charge utile Noise (données de bloc)        |
  +          (longueur varie)              +
  |     voir ci-dessous pour les blocs autorisés      +
  +----+----+----+----+----+----+----+----+


```

Tailles, hors surcharge IP :

| Type | Code de t | e  X | n  Msg 1 | n  Msg 1 Enc | n  Msg 1 Dec | n  Longueu | de clé |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ------ |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | trop gran |  |  |  |  |


Note : Les codes de type sont uniquement pour un usage interne. Les routeurs resteront de type 4,
et le support sera indiqué dans les adresses de routeur.

MTU minimum pour MLKEM768_X25519 :
Environ 1316 pour IPv4 et 1336 pour IPv6.



SessionCreated (Type 1)
````````````````````````
Changements : SSU2 actuel contient uniquement les données de bloc dans la section ChaCha.
Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.


Contenu brut :

```dataspec
+----+----+----+----+----+----+----+----+
  |  Octets d'en-tête long 0-15, ChaCha20     |
  +  chiffré avec la clé d'intro de Bob et     +
  | clé dérivée, voir KDF de chiffrement de l'en-tête |
  +----+----+----+----+----+----+----+----+
  |  Octets d'en-tête long 16-31, ChaCha20    |
  +  chiffré avec la clé dérivée n=0       +
  |  Voir KDF de chiffrement de l'en-tête            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, chiffré avec ChaCha20           +
  |       avec la clé dérivée n=0            |
  +              (32 octets)               +
  |       Voir KDF de chiffrement de l'en-tête       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Données ChaCha20 (MLKEM)               |
  +   Données chiffrées et authentifiées    +
  |  la longueur varie                        |
  +  k défini dans KDF pour le Session Created +
  |  n = 0; voir KDF pour les données associées   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   Données ChaCha20 (payload)             |
  +   Données chiffrées et authentifiées    +
  |  la longueur varie                        |
  +  k défini dans KDF pour le Session Created +
  |  n = 0; voir KDF pour les données associées   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        MAC Poly1305 (16 octets)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```

Données non chiffrées (tag d'authentification Poly1305 non affiché) :

```dataspec
+----+----+----+----+----+----+----+----+
  |      ID de connexion de destination        |
  +----+----+----+----+----+----+----+----+
  |   Numéro de paquet   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        ID de connexion source           |
  +----+----+----+----+----+----+----+----+
  |                 Jeton                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 octets)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           Texte chiffré ML-KEM           |
  +      (voir tableau ci-dessous pour la longueur)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Chargement Noise (données de bloc)        |
  +          (longueur varie)              +
  |      voir ci-dessous pour les blocs autorisés     |
  +----+----+----+----+----+----+----+----+

```

Tailles, hors surcharge IP :

| Type | Code de t | e  Y | n  Msg 2 | n  Msg 2 Enc | n  Msg 2 Dec | n  Longueu | CT PQ |
| ---- | --------- | ---- | -------- | ------------ | ------------ | ---------- | ----- |
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| ML |  |  |  |  |  |  |  |
