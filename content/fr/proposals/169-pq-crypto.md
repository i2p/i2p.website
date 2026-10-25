---
title: "Protocoles de Cryptographie Post-Quantique"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2026-10-24"
status: "Ouvrir"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

### Statut

| Protocole / Fonctionnalité | Statut |
|--------------------|--------|
| Ratchet | Complet dans Java I2P et i2pd |
| NTCP2 | Bêta T1 2026 |
| SSU2 | Implémentation bientôt commencée, Bêta T2-T3 2026 |
| MLDSA SigTypes | Priorité faible, probablement 2027+ |
## Aperçu

Bien que la recherche et la compétition pour une cryptographie post-quantique (PQ) appropriée se poursuivent depuis une décennie, les choix ne sont devenus clairs que récemment.

Nous avons commencé à examiner les implications de la cryptographie PQ en 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Les standards TLS ont ajouté le support du chiffrement hybride au cours des deux dernières années et il est maintenant utilisé pour une portion significative du trafic chiffré sur internet grâce au support dans Chrome et Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

Le NIST a récemment finalisé et publié les algorithmes recommandés pour la cryptographie post-quantique [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Plusieurs bibliothèques cryptographiques courantes prennent désormais en charge les standards NIST ou publieront leur support dans un avenir proche.

[Cloudflare](https://blog.cloudflare.com/pq-2024/) et [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recommandent tous deux que la migration commence immédiatement. Voir également la FAQ PQ 2022 de la [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P devrait être un leader en sécurité et cryptographie. Il est temps maintenant d'implémenter les algorithmes recommandés. En utilisant notre système flexible de types cryptographiques et de types de signature, nous ajouterons des types pour la cryptographie hybride, et pour les signatures PQ et hybrides.

## Objectifs

- Sélectionner des algorithmes résistants PQ
- Ajouter des algorithmes PQ uniquement et hybrides aux protocoles I2P selon les besoins
- Définir plusieurs variantes
- Sélectionner les meilleures variantes après implémentation, tests, analyse et recherche
- Ajouter le support de manière incrémentale et avec rétrocompatibilité

## Non-objectifs

- Ne pas modifier les protocoles de chiffrement unidirectionnel (Noise N)
- Ne pas abandonner SHA256, pas menacé à court terme par PQ
- Ne pas sélectionner les variantes préférées finales à ce stade

## Modèle de menace

- Routers au OBEP ou IBGW, possiblement en collusion,
  stockant les messages garlic pour un déchiffrement ultérieur (forward secrecy)
- Observateurs réseau
  stockant les messages de transport pour un déchiffrement ultérieur (forward secrecy)
- Participants réseau falsifiant les signatures pour RI, LS, streaming, datagrams,
  ou autres structures

## Protocoles affectés

Nous modifierons les protocoles suivants, approximativement dans l'ordre de développement. Le déploiement global aura probablement lieu de fin 2025 à mi-2027. Consultez la section Priorités et déploiement ci-dessous pour plus de détails.

| Protocole / Fonctionnalité | Statut |
|--------------------|--------|
| Hybrid MLKEM Ratchet et LS | Approuvé 2025-06 ; bêta 2025-08 ; version finale 2025-11 |
| Hybrid MLKEM NTCP2 | Testé sur le réseau réel, Approuvé 2026-02 ; objectif bêta 2026-05 ; objectif version finale 2026-08 |
| Hybrid MLKEM SSU2 | Approuvé 2026-02 ; objectif bêta 2026-08 ; objectif version finale 2026-11 |
| MLDSA SigTypes 12-14 | La proposition est stable mais pourrait ne pas être finalisée avant 2027 |
| MLDSA Dests | Testé sur le réseau réel, nécessite une mise à niveau du réseau pour le support floodfill |
| Hybrid SigTypes 15-17 | Préliminaire |
| Hybrid Dests | |
## Conception

Nous prendrons en charge les standards NIST FIPS 203 et 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) qui sont basés sur, mais PAS compatibles avec, CRYSTALS-Kyber et CRYSTALS-Dilithium (versions 3.1, 3, et antérieures).

### Échange de clés

Nous prendrons en charge l'échange de clés hybride dans les protocoles suivants :

| Proto   | Type Noise | Support PQ uniquement ? | Support hybride ? |
|---------|------------|-------------------------|-------------------|
| NTCP2   | XK         | non                     | oui               |
| SSU2    | XK         | non                     | oui               |
| Ratchet | IK         | non                     | oui               |
| TBM     | N          | non                     | non               |
| NetDB   | N          | non                     | non               |
PQ KEM fournit uniquement des clés éphémères et ne prend pas directement en charge les échanges de clés statiques tels que Noise XK et IK.

Noise N n'utilise pas d'échange de clés bidirectionnel et n'est donc pas adapté au chiffrement hybride.

Nous ne prendrons donc en charge que le chiffrement hybride, pour NTCP2, SSU2 et Ratchet. Nous définirons les trois variantes ML-KEM comme dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), pour un total de 3 nouveaux types de chiffrement. Les types hybrides ne seront définis qu'en combinaison avec X25519.

Les nouveaux types de chiffrement sont :

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
La surcharge sera substantielle. Les tailles typiques des messages 1 et 2 (pour XK et IK) sont actuellement d'environ 100 octets (avant toute charge utile supplémentaire). Cela augmentera de 8x à 15x selon l'algorithme.

### Signatures

Nous prendrons en charge les signatures PQ et hybrides dans les structures suivantes :

Nous prendrons donc en charge les signatures PQ uniquement et hybrides. Nous définirons les trois variantes ML-DSA comme dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), trois variantes hybrides avec Ed25519, et trois variantes PQ uniquement avec pré-hachage pour les fichiers SU3 seulement, soit 9 nouveaux types de signature au total. Les types hybrides ne seront définis qu'en combinaison avec Ed25519. Nous utiliserons le ML-DSA standard, PAS les variantes de pré-hachage (HashML-DSA), sauf pour les fichiers SU3.

| Type | Support PQ seulement ? | Support Hybride ? |
|------|------------------------|-------------------|
| RouterInfo | oui | oui |
| LeaseSet | oui | oui |
| Streaming SYN/SYNACK/Close | oui | oui |
| Repliable Datagrams | oui | oui |
| Datagram2 (prop. 163) | oui | oui |
| I2CP create session msg | oui | oui |
| SU3 files | oui | oui |
| X.509 certificates | oui | oui |
| Java keystores | oui | oui |
Nous utiliserons la variante de signature "hedged" ou randomisée, et non la variante "déterministe", telle que définie dans la section 3.4 de [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Cela garantit que chaque signature est différente, même sur les mêmes données, et fournit une protection supplémentaire contre les attaques par canaux auxiliaires. Voir la section des notes d'implémentation ci-dessous pour des détails supplémentaires sur les choix d'algorithmes, y compris l'encodage et le contexte.

Les nouveaux types de signature sont :

Les certificats X.509 et autres encodages DER utiliseront les structures composites et OID définis dans le [projet IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Type | Code |
|------|------|
| MLDSA44 | 12 |
| MLDSA65 | 13 |
| MLDSA87 | 14 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 |
| MLDSA44ph | 18 |
| MLDSA65ph | 19 |
| MLDSA87ph | 20 |
La surcharge sera substantielle. Les tailles typiques des destinations Ed25519 et des identités de router sont de 391 octets. Celles-ci augmenteront de 3,5x à 6,8x selon l'algorithme. Les signatures Ed25519 font 64 octets. Celles-ci augmenteront de 38x à 76x selon l'algorithme. Les RouterInfo signés typiques, leaseSet, datagrammes avec réponse possible, et messages de streaming signés font environ 1KB. Ceux-ci augmenteront de 3x à 8x selon l'algorithme.

Comme les nouveaux types d'identité de destination et de router ne contiendront pas de remplissage, ils ne seront pas compressibles. Les tailles des destinations et des identités de router qui sont compressées en gzip pendant le transit augmenteront de 12x à 38x selon l'algorithme.

Pour les Destinations, les nouveaux types de signature sont pris en charge avec tous les types de chiffrement dans le leaseSet. Définissez le type de chiffrement dans le certificat de clé sur NONE (255).

### Combinaisons légales

Pour les RouterIdentities, le type de chiffrement ElGamal est déprécié. Les nouveaux types de signature ne sont pris en charge qu'avec le chiffrement X25519 (type 4). Les nouveaux types de chiffrement seront indiqués dans les RouterAddresses. Le type de chiffrement dans le certificat de clé continuera d'être le type 4.

Les vecteurs de test pour SHA3-256, SHAKE128 et SHAKE256 sont disponibles sur [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

### Nouvelle cryptographie requise

- ML-KEM (anciennement CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anciennement CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anciennement Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Utilisé uniquement pour SHAKE128
- SHA3-256 (anciennement Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 et SHAKE256 (extensions XOF pour SHA3-128 et SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Notez que la bibliothèque Java bouncycastle prend en charge tout ce qui précède. La prise en charge de la bibliothèque C++ est dans OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

Nous ne prendrons pas en charge [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), il est beaucoup plus lent et volumineux que ML-DSA. Nous ne prendrons pas en charge le prochain FIPS206 (Falcon), il n'est pas encore standardisé. Nous ne prendrons pas en charge NTRU ou d'autres candidats PQ qui n'ont pas été standardisés par le NIST.

### Alternatives

Il existe des recherches [paper](https://eprint.iacr.org/2020/379.pdf) sur l'adaptation de Wireguard (IK) pour la cryptographie PQ pure, mais il y a plusieurs questions ouvertes dans cet article. Plus tard, cette approche a été implémentée sous le nom de Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) pour PQ Wireguard.

### Rosenpass

Rosenpass utilise un handshake similaire à Noise KK avec des clés statiques Classic McEliece 460896 pré-partagées (500 Ko chacune) et des clés éphémères Kyber-512 (essentiellement MLKEM-512). Comme les textes chiffrés Classic McEliece ne font que 188 octets, et que les clés publiques et textes chiffrés Kyber-512 ont une taille raisonnable, les deux messages de handshake tiennent dans un MTU UDP standard. La clé partagée de sortie (osk) du handshake PQ KK est utilisée comme clé pré-partagée d'entrée (psk) pour le handshake Wireguard IK standard. Il y a donc deux handshakes complets au total, un purement PQ et un purement X25519.

Nous ne pouvons faire aucune de ces choses pour remplacer nos handshakes XK et IK car :

Il y a beaucoup de bonnes informations dans le livre blanc, et nous l'examinerons pour des idées et de l'inspiration. TODO.

- Nous ne pouvons pas faire KK, Bob n'a pas la clé statique d'Alice
- Les clés statiques de 500KB sont bien trop importantes
- Nous ne voulons pas d'un aller-retour supplémentaire

Mettez à jour les sections et tableaux dans le document des structures communes [/docs/specs/common-structures/](/docs/specs/common-structures/) comme suit :

## Spécification

### Structures communes

Les nouveaux types de clés publiques sont :

#### Problèmes

Les clés publiques hybrides sont la clé X25519. Les clés publiques KEM sont la clé PQ éphémère envoyée d'Alice à Bob. L'encodage et l'ordre des octets sont définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Type | Longueur de Clé Publique | Depuis | Usage |
|------|--------------------------|--------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | Voir proposition 169, pour leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Voir proposition 169, pour leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Voir proposition 169, pour leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM512 | 800 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| MLKEM768 | 1184 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| MLKEM1024 | 1568 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| MLKEM512_CT | 768 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | Voir proposition 169, pour handshakes uniquement, pas pour leasesets, RI ou Destinations |
| NONE | 0 | 0.9.xx | Voir proposition 169, pour destinations avec types de signature PQ uniquement, pas pour RI ou leasesets |
Les clés MLKEM*_CT ne sont pas vraiment des clés publiques, elles sont le "texte chiffré" envoyé de Bob à Alice dans la négociation Noise. Elles sont listées ici par souci d'exhaustivité.

Les nouveaux types de clés privées sont :

#### PrivateKey

Les clés privées hybrides sont les clés X25519. Les clés privées KEM sont uniquement pour Alice. L'encodage KEM et l'ordre des octets sont définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

| Type | Longueur de clé privée | Depuis | Utilisation |
|------|------------------------|--------|-------------|
| MLKEM512_X25519 | 32 | 0.9.xx | Voir proposition 169, pour les leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | Voir proposition 169, pour les leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | Voir proposition 169, pour les leasesets uniquement, pas pour les RI ou Destinations |
| MLKEM512 | 1632 | 0.9.xx | Voir proposition 169, pour les négociations uniquement, pas pour les leasesets, RI ou Destinations |
| MLKEM768 | 2400 | 0.9.xx | Voir proposition 169, pour les négociations uniquement, pas pour les leasesets, RI ou Destinations |
| MLKEM1024 | 3168 | 0.9.xx | Voir proposition 169, pour les négociations uniquement, pas pour les leasesets, RI ou Destinations |
Les nouveaux types de clés publiques de signature sont :

#### SigningPublicKey

Les clés publiques de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans le [brouillon IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Type | Longueur (octets) | Depuis | Utilisation |
|------|-------------------|--------|-------------|
| MLDSA44 | 1312 | 0.9.xx | Voir proposition 169 |
| MLDSA65 | 1952 | 0.9.xx | Voir proposition 169 |
| MLDSA87 | 2592 | 0.9.xx | Voir proposition 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | Voir proposition 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | Voir proposition 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | Voir proposition 169 |
| MLDSA44ph | 1344 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb |
| MLDSA65ph | 1984 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb |
| MLDSA87ph | 2624 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb |
Les nouveaux types de clés privées de signature sont :

#### SigningPrivateKey

Les clés privées de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans le [brouillon IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Type | Longueur (octets) | Depuis | Usage |
|------|-------------------|--------|-------|
| MLDSA44 | 2560 | 0.9.xx | Voir proposition 169 |
| MLDSA65 | 4032 | 0.9.xx | Voir proposition 169 |
| MLDSA87 | 4896 | 0.9.xx | Voir proposition 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | Voir proposition 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | Voir proposition 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | Voir proposition 169 |
| MLDSA44ph | 2592 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
| MLDSA65ph | 4064 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
| MLDSA87ph | 4928 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
Les nouveaux types de signature sont :

Les signatures hybrides sont la signature Ed25519 suivie de la signature PQ, comme dans le [projet IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Les signatures hybrides sont vérifiées en vérifiant les deux signatures, et échouent si l'une d'entre elles échoue. L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

#### Signature

Les nouveaux types de clés publiques de signature sont :

| Type | Longueur (octets) | Depuis | Usage |
|------|-------------------|--------|-------|
| MLDSA44 | 2420 | 0.9.xx | Voir proposition 169 |
| MLDSA65 | 3309 | 0.9.xx | Voir proposition 169 |
| MLDSA87 | 4627 | 0.9.xx | Voir proposition 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | Voir proposition 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | Voir proposition 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | Voir proposition 169 |
| MLDSA44ph | 2484 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
| MLDSA65ph | 3373 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
| MLDSA87ph | 4691 | 0.9.xx | Uniquement pour les fichiers SU3, pas pour les structures netDb. Voir proposition 169 |
Les nouveaux types de clés publiques cryptographiques sont :

#### Certificats de clés

Les clés publiques de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans le [brouillon IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

| Type | Code de Type | Longueur Totale de la Clé Publique | Depuis | Utilisation |
|------|--------------|-------------------------------------|--------|-------------|
| MLDSA44 | 12 | 1312 | 0.9.xx | Voir proposition 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | Voir proposition 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | Voir proposition 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | Voir proposition 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | Voir proposition 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | Voir proposition 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Uniquement pour les fichiers SU3 |
| MLDSA65ph | 19 | n/a | 0.9.xx | Uniquement pour les fichiers SU3 |
| MLDSA87ph | 20 | n/a | 0.9.xx | Uniquement pour les fichiers SU3 |
Pour les destinations avec des types de signature Hybrid ou PQ, utilisez NONE (type 255) pour le type de chiffrement, mais il n'y a pas de clé cryptographique, et toute la section principale de 384 octets est destinée à la clé de signature.

| Type | Code de Type | Longueur Totale de Clé Publique | Depuis | Utilisation |
|------|--------------|----------------------------------|--------|-------------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | Voir proposition 169, pour les leaseSets uniquement, pas pour les RI ou Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | Voir proposition 169, pour les leaseSets uniquement, pas pour les RI ou Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | Voir proposition 169, pour les leaseSets uniquement, pas pour les RI ou Destinations |
| NONE | 255 | 0 | 0.9.xx | Voir proposition 169 |
Les types de clés hybrides ne sont JAMAIS inclus dans les certificats de clé ; seulement dans les leaseSets.

Aucun remplissage. La longueur totale est de 7 + longueur totale de la clé. La longueur du certificat de clé est de 4 + longueur de clé excédentaire.

#### Tailles de destination

Voici les longueurs pour les nouveaux types de Destination. Le type de chiffrement pour tous est NONE (type 255) et la longueur de la clé de chiffrement est traitée comme 0. Toute la section de 384 octets est utilisée pour la première partie de la clé publique de signature. NOTE : Ceci est différent de la spécification pour les types de signature ECDSA_SHA512_P521 et RSA, où nous avons maintenu la clé ElGamal de 256 octets dans la destination même si elle n'était pas utilisée.

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

Exemple de flux d'octets de destination de 1319 octets pour MLDSA44 :

Exemple de flux d'octets d'identité de router de 1351 octets pour MLDSA44 :

| Type | Code Type | Longueur Totale de Clé Publique | Principal | Excès | Longueur Totale Dest |
|------|-----------|--------------------------------|-----------|-------|---------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
#### Tailles des RouterIdent

Voici les longueurs pour les nouveaux types de Destination. Le type de chiffrement pour tous est X25519 (type 4). La section entière de 352 octets après la clé publique X25519 est utilisée pour la première partie de la clé publique de signature. Pas de remplissage. La longueur totale est 39 + longueur totale de la clé. La longueur du certificat de clé est 4 + longueur excédentaire de la clé.

Les handshakes utilisent les modèles de handshake du [Noise Protocol](https://noiseprotocol.org/noise.html).

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Code de Type | Longueur Totale de Clé Publique | Principal | Excès | Longueur Totale de RouterIdent |
|------|--------------|----------------------------------|-----------|-------|--------------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### PublicKey

Les modifications suivantes à XK et IK pour le secret de transmission hybride (hfs) sont spécifiées dans la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 5 :

Le motif e1 est défini comme suit, tel que spécifié dans la section 4 de la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

#### KDF pour split()

```

  M = message
  Prefix = "CompositeAlgorithmSignatures2025" (32 bytes, not null terminated)
  Label = (30 bytes, not null terminated), one of:
          "COMPSIG-MLDSA44-Ed25519-SHA512"
          "COMPSIG-MLDSA65-Ed25519-SHA512"
          "COMPSIG-MLDSA87-Ed25519-SHA512"  // not in [COMPOSITE-SIGS]
  ctx = "" (0 bytes)
  len(ctx) = 0  (1 byte)
  PH(M) = SHA512(M) (64 bytes)


  Compute a hash of the message prepended as follows:

  M' = Prefix || Label || len(ctx) || ctx || PH( M )

  M' length is 127 bytes.

  Sign the prehashed message M':

  signature = MLDSA_SIGN(M') || Ed25519_SIGN(M')

```
#### Identificateurs Noise

Le motif ekem1 est défini comme suit, tel que spécifié dans la section 4 de la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

```

  M' = as above

  signature = MLDSA_VERIFY(M') && Ed25519_VERIFY(M')


```
#### 1b) Nouveau format de session (avec liaison)

Cette section s'applique aux protocoles IK et XK.

### Modèles de négociation

Le handshake hybride est défini dans la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Le premier message, d'Alice vers Bob, contient e1, la clé d'encapsulation, avant la charge utile du message. Celle-ci est traitée comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant qu'Alice) ou DecryptAndHash() (en tant que Bob). Ensuite, traitez la charge utile du message comme d'habitude.

Le mappage de lettres suivant est utilisé :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message
- e1 = clé PQ éphémère à usage unique, envoyée d'Alice à Bob
- ekem1 = le texte chiffré KEM, envoyé de Bob à Alice

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés tels que définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  IK:                       IKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, s, ss, p       -> e, es, e1, s, ss, p
  <- tag, e, ee, se, p     <- tag, e, ee, ekem1, se, p
  <- p                     <- p
  p ->                     p ->

  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
(encap_key, decap_key) = PQ_KEYGEN()

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
(ciphertext, kem_shared_key) = ENCAPS(encap_key)

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF de handshake Noise

#### 1b) Nouveau format de session (avec liaison)

- Devrions-nous changer la fonction de hachage de handshake ? Voir [comparaison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 n'est pas vulnérable à PQ, mais si nous voulons mettre à niveau
  notre fonction de hachage, c'est le moment, pendant que nous changeons d'autres choses.
  La proposition SSH IETF actuelle [brouillon IETF](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) est d'utiliser MLKEM768
  avec SHA256, et MLKEM1024 avec SHA384. Cette proposition inclut
  une discussion des considérations de sécurité.
- Devrions-nous arrêter d'envoyer des données ratchet 0-RTT (autres que le leaseSet) ?
- Devrions-nous passer le ratchet d'IK à XK si nous n'envoyons pas de données 0-RTT ?

#### Aperçu

kem_shared_key = DECAPS(ciphertext, decap_key)

Notez que la encap_key et le ciphertext sont tous deux chiffrés à l'intérieur des blocs ChaCha/Poly dans les messages 1 et 2 de la négociation Noise. Ils seront déchiffrés dans le cadre du processus de négociation.

Le second message, de Bob à Alice, contient ekem1, le texte chiffré, avant la charge utile du message. Ceci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant que Bob) ou DecryptAndHash() (en tant qu'Alice). Ensuite, calculez la kem_shared_key et appelez MixKey(kem_shared_key). Puis traitez la charge utile du message comme d'habitude.

#### Opérations ML-KEM définies

Pour XK : Après le motif de message 'es' et avant la charge utile, ajouter :

OU

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

Pour IK : Après le motif de message 'es' et avant le motif de message 's', ajouter :

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

Pour XK : Après le modèle de message 'es' et avant la charge utile, ajouter :

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

OU

La kem_shared_key est mélangée dans la clé de chaînage avec MixHash(). Voir ci-dessous pour les détails.

#### KDF d'Alice pour le Message 1

Pour XK : Après le motif de message 'ee' et avant la charge utile, ajouter :

OU

Pour IK : Après le motif de message 'ee' et avant le motif de message 'se', ajouter :

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob pour le Message 1

Pour XK : Après le motif de message 'ee' et avant la charge utile, ajouter :

OU

Pour IK : Après le motif de message 'es' et avant le motif de message 's', ajouter :

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob pour le Message 2

Mettre à jour la spécification ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) comme suit :

OU

Format chiffré :

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### Alice KDF pour le Message 2

Après le motif de message 'ee' (et avant le motif de message 'ss' pour IK), ajouter :

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
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

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF pour le Message 3 (XK uniquement)

inchangé

#### Identifiants Noise

inchangé

### Ratchet

Modifications : Le ratchet actuel a une charge utile vide pour la première section ChaCha, et la charge utile dans la deuxième section. Avec ML-KEM, il y a maintenant trois sections. La première section contient le texte chiffré PQ chiffré. La deuxième section a une charge utile vide. La troisième section contient la charge utile.

#### En-tête Long

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### En-tête Court

Changements : Le ratchet actuel contenait la clé statique dans la première section ChaCha, et la charge utile dans la seconde section. Avec ML-KEM, il y a maintenant trois sections. La première section contient la clé publique PQ chiffrée. La deuxième section contient la clé statique. La troisième section contient la charge utile.

Format déchiffré :

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
  +           ML-KEM encap_key            +
  |       ChaCha20 encrypted data         |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +    (MAC) for encap_key Section        +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +           X25519 Static Key           +
  |       ChaCha20 encrypted data         |
  +             32 bytes                  +
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
```
Format décrypté :

```
Payload Part 1:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM encap_key                +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X25519 Static Key               +
  |                                       |
  +      (32 bytes)                       +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tailles :

| Type | Code Type | Long X | Long Msg 1 | Long Msg 1 Chif | Long Msg 1 Déchif | Long clé PQ | Long pl |
|------|-----------|--------|------------|------------------|-------------------|-------------|---------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Notez que la charge utile doit contenir un bloc DateTime, donc la taille minimale de la charge utile est de 7. Les tailles minimales du message 1 peuvent être calculées en conséquence.

#### 1g) Format de réponse pour nouvelle session

Modifications : Le NTCP2 actuel ne contient que les options de la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Format chiffré :

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
  |                                       |
  +                                       +
  | ChaCha20 encrypted ML-KEM ciphertext  |
  +      (see table below for length)     +
  ~                                       ~
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for ciphertext Section         +
  |             16 bytes                  |
  +----+----+----+----+----+----+----+----+
  |  Poly1305 Message Authentication Code |
  +  (MAC) for key Section (no data)      +
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
```
Format décrypté :

```
Payload Part 1:


  +----+----+----+----+----+----+----+----+
  |                                       |
  +       ML-KEM ciphertext               +
  |                                       |
  +      (see table below for length)     +
  |                                       |
  ~                                       ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Payload Part 2:

  empty

  Payload Part 3:

  +----+----+----+----+----+----+----+----+
  |                                       |
  +            Payload Section            +
  |                                       |
  ~                                       ~
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tailles :

| Type | Code Type | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Notez que bien que le message 2 ait normalement une charge utile non nulle, la spécification ratchet [/docs/specs/ecies/](/docs/specs/ecies/) ne l'exige pas, donc la taille minimale de la charge utile est 0. Les tailles minimales du message 2 peuvent être calculées en conséquence.

### NTCP2

Mettre à jour la spécification NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) comme suit :

#### Identifiants Noise

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Contenu brut :

Afin que NTCP2 PQ et non-PQ puissent être pris en charge sur la même adresse et le même port de router, nous utilisons le bit le plus significatif de la valeur X (clé publique éphémère X25519) pour marquer qu'il s'agit d'une connexion PQ. Ce bit est toujours désactivé pour les connexions non-PQ.

Note : le champ version dans le bloc d'options du message 1 doit être défini sur 2, même pour les connexions PQ.

Pour Bob, après la dé-obfuscation AES de X, tester X[31] & 0x80. Si le bit est défini, l'effacer avec X[31] &= 0x7f, et déchiffrer via Noise comme une connexion PQ. Si le bit n'est pas défini, déchiffrer via Noise comme une connexion non-PQ comme d'habitude.

Pour PQ NTCP2 annoncé sur une adresse et un port de router différents, cela n'est pas requis.

Pour des informations supplémentaires, voir la section Adresses publiées ci-dessous.

Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |        MS bit set to 1 and then       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly encrypted data (MLKEM)   |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~                                       ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 1                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses du routeur.

Tailles :

| Type | Code Type | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

#### 2) SessionCreated

Contenu brut :

Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted Y         |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (options)   |
  +         16 bytes                      +
  +   k defined in KDF for message 2      +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as current specification except add a second ChaChaPoly frame
```
Tailles :

```
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |               options                 |
  +              (16 bytes)               +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+
```
Tailles :

| Type | Code de type | Longueur Y | Longueur Msg 2 | Longueur Msg 2 enc | Longueur Msg 2 déc | Longueur PQ CT | Longueur opt |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1168+pad | 1136 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

#### 3) SessionConfirmed

Inchangé

#### Fonction de dérivation de clé (KDF) (pour la phase de données)

Inchangé

#### Adresses Publiées

Dans tous les cas, utilisez le nom de transport NTCP2 comme d'habitude.

Utiliser la même adresse/port que pour une connexion non-PQ et non-firewalled. Une seule variante PQ est prise en charge. Dans l'adresse du router, publier v=2 (comme d'habitude) et le nouveau paramètre pq=[3|4|5] pour indiquer MLKEM 512/768/1024. Alice positionne le MSB de la clé éphémère (key[31] & 0x80) dans la requête de session pour indiquer qu'il s'agit d'une connexion hybride. Voir ci-dessus. Les routers plus anciens ignoreront le paramètre pq et se connecteront en non-PQ comme d'habitude.

Adresses derrière pare-feu (aucune IP publiée) : Dans l'adresse du router, publier v=2 (comme d'habitude). Il n'est pas nécessaire de publier un paramètre pq.

Alice peut se connecter à un Bob PQ en utilisant la variante PQ que Bob publie, que Alice annonce ou non le support pq dans ses informations de router, ou qu'elle annonce la même variante.

Dans la spécification actuelle, les messages 1 et 2 sont définis comme ayant une quantité "raisonnable" de remplissage, avec une plage de 0-31 octets recommandée, et aucun maximum spécifié.

#### Padding Maximum

Jusqu'à l'API 0.9.68 (version 2.11.0), Java I2P implémentait un maximum de 256 octets de remplissage pour les connexions non-PQ, cependant cela n'était pas documenté auparavant. À partir de l'API 0.9.69 (version 2.12.0), Java I2P implémente le même remplissage maximum pour les connexions non-PQ que pour MLKEM-512. Voir le tableau ci-dessous.

Utiliser la taille de message définie comme rembourrage maximum, c'est-à-dire que le rembourrage maximum doublera la taille du message pour les connexions PQ, comme suit :

Utiliser la taille de message définie comme padding maximal, c'est-à-dire que le padding maximal doublera la taille du message pour les connexions PQ, comme suit :

| Remplissage Max du Message | non-PQ (jusqu'à 0.9.68) | non-PQ (à partir de 0.9.69) | MLKEM-512 | MLKEM-768 | MLKEM-1024 |
|---------------------|----------------------|-----------------------|-----------|-----------|------------|
| Session Request  |   256   |   880   |    880   |     1264   |    1648  |
| Session Created  |   256   |   848   |    848   |     1136   |    1616  |
### SSU2

Notez que MLKEM-1024 n'est PAS pris en charge pour SSU2, car les clés sont trop volumineuses pour tenir dans un datagramme standard de 1500 octets.

#### Identifiants Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

L'en-tête long fait 32 octets. Il est utilisé avant qu'une session soit créée, pour Token Request, SessionRequest, SessionCreated, et Retry. Il est également utilisé pour les messages Peer Test et Hole Punch hors session.

#### Confidentialité persistante

Dans les messages suivants, définissez le champ ver (version) dans l'en-tête long à 3 ou 4, pour indiquer MLKEM-512 ou MLKEM-768.

Dans les messages suivants, définissez le champ ver (version) dans l'en-tête long à 2, comme d'habitude, même si MLKEM-512 ou MLKEM-768 est pris en charge. Les implémentations peuvent également définir la valeur à 3 ou 4, si l'autre extrémité le prend en charge, mais cela n'est pas nécessaire. Les implémentations devraient accepter toute valeur de 2 à 4.

- (0) Demande de session
- (1) Session créée
- (9) Nouvelle tentative
- (10) Demande de jeton
- (11) Perforation de trou

Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

- (7) Test de pair (messages hors session 5-7)

Tailles, sans inclure la surcharge IP :

- Demande de relais
- Réponse de relais
- Introduction de relais
- Test de pair

Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

inchangé

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Taille de Nouvelle Session

inchangé

#### SessionRequest (Type 0)

Modification du KDF pour la protection contre l'usurpation : Pour répondre aux problèmes soulevés dans la Proposition 165 [Prop165]_, mais avec une solution différente, nous modifions le KDF pour la Session Request. Ceci concerne uniquement les sessions PQ. Le KDF pour les sessions non-PQ reste inchangé.

Contenu brut :

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
MTU minimum pour MLKEM768_X25519 : Environ 1316 pour IPv4 et 1336 pour IPv6.

| Type | Code Type | Longueur X | Longueur Msg 1 | Longueur Msg 1 Chiffré | Longueur Msg 1 Déchiffré | Longueur clé PQ | Longueur pl |
|------|-----------|------------|---------------|------------------------|--------------------------|----------------|-------------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/d | trop gros | | | | |
Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

Modifications : Le SSU2 actuel ne contient que les données de bloc dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

#### SessionCreated (Type 1)

Contenu brut :

Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (MLKEM)     |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 encrypted data (payload)   |
  ~  length varies                        ~
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Tailles :

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tailles, sans inclure la surcharge IP :

| Type | Code de type | Long. Y | Long. Msg 2 | Long. Msg 2 Enc | Long. Msg 2 Dec | Long. PQ CT | Long. pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | trop grand | | | | |
Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

Modifications : Le SSU2 actuel ne contient que les données de bloc dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Signatures PQ : Les blocs Relay, les blocs Peer Test et les messages Peer Test contiennent tous des signatures. Malheureusement, les signatures PQ sont plus grandes que le MTU. Il n'existe actuellement aucun mécanisme pour fragmenter les blocs Relay ou Peer Test ou les messages sur plusieurs paquets UDP. Le protocole doit être étendu pour supporter la fragmentation. Cela sera fait dans une proposition séparée à déterminer. Jusqu'à ce que cela soit terminé, Relay et Peer Test ne seront pas supportés.

#### SessionConfirmed (Type 2)

inchangé

#### KDF pour la phase de données

inchangé

#### Relais et Test de Pairs

Les blocs suivants contiennent des champs de version. Ils resteront en version 2 (pour la compatibilité avec un Bob non-PQ), et ne passeront pas à la version 3/4 pour PQ.

- SAMv3
- Bittorrent
- Directives pour développeurs
- Nommage / carnet d'adresses / serveurs de redirection
- Autres documents

Dans tous les cas, utilisez le nom de transport SSU2 comme d'habitude. MLKEM-1024 n'est pas pris en charge.

#### Adresses Publiées

Utilisez la même adresse/port que pour non-PQ, non-firewalled. Une ou les deux variantes PQ sont prises en charge. Dans l'adresse du router, publiez v=2 (comme d'habitude) et le nouveau paramètre pq=[3|4|3,4] pour indiquer MLKEM 512/768/les deux. Les anciens routers ignoreront le paramètre pq et se connecteront en non-pq comme d'habitude.

Faites attention à ne pas dépasser la MTU avec MLKEM768. La MTU minimale pour SSU2 est de 1280, qui correspond à la taille du message 1 sans padding. N'incluez pas de padding dans le message 1 si la MTU d'Alice ou Bob est de 1280.

Adresses derrière pare-feu (aucune IP publiée) : Dans l'adresse du router, publier v=2 (comme d'habitude). Le paramètre pq DOIT être publié dans les adresses derrière pare-feu, pour supporter le relais.

Alice peut se connecter à un Bob PQ en utilisant la variante PQ que Bob publie, qu'Alice annonce ou non le support pq dans ses informations de router, ou qu'elle annonce la même variante.

Dans la spécification actuelle, les messages 1 et 2 sont définis comme ayant une quantité "raisonnable" de remplissage, avec une plage de 0-31 octets recommandée, et aucun maximum spécifié.

#### MTU

Nous pourrions utiliser en interne le champ version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768.

### Streaming

Pour les messages 1 et 2, MLKEM768 augmenterait la taille des paquets au-delà du MTU minimum de 1280. On ne le supporterait probablement tout simplement pas pour cette connexion si le MTU était trop faible.

### Fichiers SU3

Pour les messages 1 et 2, MLKEM1024 augmenterait la taille des paquets au-delà du MTU maximum de 1500. Cela nécessiterait de fragmenter les messages 1 et 2, et ce serait une complication majeure. Probablement que nous ne le ferons pas.

Relais et test de pair : Voir ci-dessus

TODO : Y a-t-il un moyen plus efficace de définir la signature/vérification pour éviter de copier la signature ?

À FAIRE

La section 8.1 du [projet IETF](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) interdit l'utilisation de HashML-DSA dans les certificats X.509 et n'attribue pas d'OID pour HashML-DSA, en raison de complexités d'implémentation et de sécurité réduite.

### Autres spécifications

La nouvelle taille maximale de Destination sera de 2599 (3468 en base 64).

Notez que nous interdisons la signature Ed25519 des fichiers SU3, et bien que nous ayons défini la signature Ed25519ph, nous ne nous sommes jamais mis d'accord sur un OID pour celle-ci, ni ne l'avons utilisée.

- Si le message 1 fait moins de 919 octets, c'est le protocole ratchet actuel.
- Si le message 1 fait 919 octets ou plus, c'est probablement MLKEM512_X25519.
  Essayez d'abord MLKEM512_X25519, et si cela échoue, essayez le protocole ratchet actuel.

## Analyse des frais généraux

### Échange de clés

Les types de signature normaux ne sont pas autorisés pour les fichiers SU3 ; utilisez les variantes ph (prehash).

| Type | Pubkey (Msg 1) | Texte chiffré (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
La nouvelle taille maximale de Destination sera de 2599 (3468 en base 64).

Mettre à jour les autres documents qui donnent des conseils sur les tailles de Destination, notamment :

| Type | Vitesse relative |
|------|------------------|
| X25519 DH/keygen | référence |
| MLKEM512 | 2,25x plus rapide |
| MLKEM768 | 1,5x plus rapide |
| MLKEM1024 | 1x (identique) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4,9x DH = 22% plus lent |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5,3x DH = 32% plus lent |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% plus lent |
Augmentation de taille (octets) :

| Type | DH/encaps relatif | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | référence | référence | référence |
| MLKEM512 | 29x plus rapide | 22x plus rapide | 17x plus rapide |
| MLKEM768 | 17x plus rapide | 14x plus rapide | 9x plus rapide |
| MLKEM1024 | 12x plus rapide | 10x plus rapide | 6x plus rapide |
### Signatures

#### Tailles

Vitesses rapportées par [Cloudflare](https://blog.cloudflare.com/pq-2024/) :

| Type | Clé publique | Sig | Clé+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (chaque msg) |
|------|--------------|-----|---------|--------|------|-------|-------------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
#### Vitesses

Mettre à jour les autres documents qui donnent des conseils sur les tailles de Destination, notamment :

| Type | Signe de vitesse relative | vérification |
|------|---------------------------|--------------|
| EdDSA_SHA512_Ed25519 | référence | référence |
| MLDSA44 | 5x plus lent | 2x plus rapide |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Augmentation de taille (octets) :

| Type | Signe de vitesse relative | vérify | keygen |
|------|---------------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | référence | référence | référence |
| MLDSA44 | 4.6x plus lent | 1.7x plus rapide | 2.6x plus rapide |
| MLDSA65 | 8.1x plus lent | identique | 1.5x plus rapide |
| MLDSA87 | 11.1x plus lent | 1.5x plus lent | identique |
## Analyse de Sécurité

Tailles typiques des clés, signatures, RIdent, Dest ou augmentations de taille (Ed25519 inclus pour référence) en supposant un type de chiffrement X25519 pour les RI. Taille ajoutée pour une Router Info, LeaseSet, datagrammes avec réponse, et chacun des deux paquets de streaming (SYN et SYN ACK) listés. Les Destinations et Leasesets actuels contiennent un remplissage répété et sont compressibles en transit. Les nouveaux types ne contiennent pas de remplissage et ne seront pas compressibles, résultant en une augmentation de taille beaucoup plus importante en transit. Voir la section conception ci-dessus.

| Catégorie | Aussi Sécurisé Que |
|----------|---------------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Poignées de main

Vitesses rapportées par [Cloudflare](https://blog.cloudflare.com/pq-2024/) :

Résultats de tests préliminaires en Java :

| Algorithme | Catégorie de sécurité |
|------------|----------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Les catégories de sécurité NIST sont résumées dans la [présentation NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) diapositive 10. Critères préliminaires : Notre catégorie de sécurité NIST minimale devrait être 2 pour les protocoles hybrides et 3 pour PQ uniquement.

Ce sont tous des protocoles hybrides. Les implémentations devraient privilégier MLKEM768 ; MLKEM512 n'est pas suffisamment sécurisé.

| Algorithme | Catégorie de sécurité |
|------------|----------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Préférences de type

Catégories de sécurité NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) :

Cette proposition définit à la fois des types de signature hybrides et uniquement PQ. MLDSA44 hybride est préférable à MLDSA65 uniquement PQ. Les tailles des clés et signatures pour MLDSA65 et MLDSA87 sont probablement trop importantes pour nous, du moins au début.

Catégories de sécurité NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) :

Bien que nous définirons et implémenterons 3 types de cryptographie et 9 types de signatures, nous prévoyons de mesurer les performances pendant le développement et d'analyser davantage les effets de l'augmentation de la taille des structures. Nous continuerons également à rechercher et surveiller les développements dans d'autres projets et protocoles.

Après une année ou plus de développement, nous tenterons de nous fixer sur un type préféré ou par défaut pour chaque cas d'usage. La sélection nécessitera de faire des compromis entre la bande passante, le CPU et le niveau de sécurité estimé. Tous les types peuvent ne pas être appropriés ou autorisés pour tous les cas d'usage.

Les préférences préliminaires sont les suivantes, sous réserve de modifications :

Chiffrement : MLKEM768_X25519

## Notes d'implémentation

### Support de bibliothèque

Signatures : MLDSA44_EdDSA_SHA512_Ed25519

Les restrictions préliminaires sont les suivantes, sous réserve de modification :

### Variantes de signature

Chiffrement : MLKEM1024_X25519 non autorisé pour SSU2

Signatures : MLDSA87 et la variante hybride probablement trop volumineuses ; MLDSA65 et la variante hybride peuvent être trop volumineuses

### Fiabilité

Les bibliothèques Bouncycastle, BoringSSL et WolfSSL prennent désormais en charge MLKEM et MLDSA. La prise en charge d'OpenSSL sera disponible dans leur version 3.5 le 8 avril 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tailles des structures

La bibliothèque Noise de southernstorm.com adaptée par Java I2P contenait un support préliminaire pour les négociations hybrides, mais nous l'avons supprimé car il n'était pas utilisé ; nous devrons le rajouter et le mettre à jour pour correspondre à la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### NetDB

Nous utiliserons la variante de signature "hedged" ou randomisée, et non la variante "déterministe", telle que définie dans la section 3.4 de [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf). Cela garantit que chaque signature est différente, même sur les mêmes données, et offre une protection supplémentaire contre les attaques par canaux auxiliaires. Bien que [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) spécifie que la variante "hedged" est celle par défaut, cela peut ou non être vrai dans diverses bibliothèques. Les implémenteurs doivent s'assurer que la variante "hedged" est utilisée pour la signature.

### Ratchet

#### Problèmes

Nous utilisons le processus de signature normal (appelé Pure ML-DSA Signature Generation) qui encode le message en interne comme 0x00 || len(ctx) || ctx || message, où ctx est une valeur optionnelle de taille 0x00..0xFF. Nous n'utilisons aucun contexte optionnel. len(ctx) == 0. Ce processus est défini dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithme 2 étape 10 et Algorithme 3 étape 5. Notez que certains vecteurs de test publiés peuvent nécessiter la définition d'un mode où le message n'est pas encodé.

L'augmentation de la taille entraînera beaucoup plus de fragmentation de tunnel pour les stockages NetDB, les poignées de main de streaming et autres messages. Vérifiez les changements de performance et de fiabilité.

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Trouvez et vérifiez tout code qui limite la taille en octets des informations de routeur et des leaseSets.

Examiner et possiblement réduire le maximum de LS/RI stockés en RAM ou sur disque, pour limiter l'augmentation du stockage. Augmenter les exigences minimales de bande passante pour les floodfills ?

- Plus d'un MLKEM
- ElG + un ou plusieurs MLKEM
- X25519 + un ou plusieurs MLKEM
- ElG + X25519 + un ou plusieurs MLKEM

La classification/détection automatique de multiples protocoles sur les mêmes tunnels devrait être possible en se basant sur une vérification de la longueur du message 1 (New Session Message). En utilisant MLKEM512_X25519 comme exemple, la longueur du message 1 est de 816 octets plus grande que le protocole ratchet actuel, et la taille minimale du message 1 (avec seulement une charge utile DateTime incluse) est de 919 octets. La plupart des tailles de message 1 avec le ratchet actuel ont une charge utile de moins de 816 octets, elles peuvent donc être classifiées comme ratchet non-hybride. Les messages volumineux sont probablement des POST qui sont rares.

- Sélection de Hash Noise - conserver SHA256 ou mettre à niveau ?
  SHA256 devrait être bon pour encore 20-30 ans, pas menacé par PQ,
  Voir [présentation NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) et [présentation NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Si SHA256 est cassé, nous avons des problèmes plus graves (netdb).
- NTCP2 port séparé, adresse router séparée
- SSU2 relay / test de pair
- Champ de version SSU2
- Version d'adresse router SSU2

Ainsi, la stratégie recommandée est :

Cela devrait nous permettre de prendre en charge efficacement le ratchet standard et le ratchet hybride sur la même destination, tout comme nous avons précédemment pris en charge ElGamal et ratchet sur la même destination. Par conséquent, nous pouvons migrer vers le protocole hybride MLKEM beaucoup plus rapidement que si nous ne pouvions pas prendre en charge les protocoles duaux pour la même destination, car nous pouvons ajouter la prise en charge MLKEM aux destinations existantes.

Les combinaisons prises en charge requises sont :

Les combinaisons suivantes peuvent être complexes, et ne sont PAS obligatoires d'être supportées, mais peuvent l'être, selon l'implémentation :

#### Tunnels partagés

Nous ne pourrions pas tenter de supporter plusieurs algorithmes MLKEM (par exemple, MLKEM512_X25519 et MLKEM_768_X25519) sur la même destination. Choisissez-en un seul ; cependant, cela dépend de notre sélection d'une variante MLKEM préférée, pour que les tunnels clients HTTP puissent en utiliser une. Dépendant de l'implémentation.

#### Taille de la nouvelle session

Nous POUVONS tenter de prendre en charge trois algorithmes (par exemple X25519, MLKEM512_X25519, et MLKEM769_X25519) sur la même destination. La classification et la stratégie de nouvelle tentative peuvent être trop complexes. La configuration et l'interface utilisateur de configuration peuvent être trop complexes. Dépendant de l'implémentation.

### NTCP2

Nous ne tenterons probablement PAS de prendre en charge les algorithmes ElGamal et hybrides sur la même destination. ElGamal est obsolète, et ElGamal + hybride uniquement (pas de X25519) n'a pas beaucoup de sens. De plus, les messages de nouvelle session ElGamal et hybrides sont tous deux volumineux, donc les stratégies de classification devraient souvent essayer les deux déchiffrements, ce qui serait inefficace. Dépendant de l'implémentation.

#### Obfuscation

Les clients peuvent utiliser les mêmes clés statiques X25519 ou des clés différentes pour les protocoles X25519 et hybride sur les mêmes tunnels, selon l'implémentation.

La spécification ECIES permet les Garlic Messages dans la charge utile du New Session Message, ce qui permet la livraison 0-RTT du paquet de streaming initial, généralement un HTTP GET, avec le leaseSet du client. Cependant, la charge utile du New Session Message ne dispose pas de confidentialité persistante. Comme cette proposition met l'accent sur une confidentialité persistante renforcée pour le ratchet, les implémentations peuvent ou devraient reporter l'inclusion de la charge utile de streaming, ou du message de streaming complet, jusqu'au premier Existing Session Message. Ceci serait au détriment de la livraison 0-RTT. Les stratégies peuvent également dépendre du type de trafic ou du type de tunnel, ou de GET vs. POST, par exemple. Dépendant de l'implémentation.

MLKEM, MLDSA, ou les deux sur la même destination, augmenteront considérablement la taille du Message de Nouvelle Session, comme décrit ci-dessus. Cela peut réduire significativement la fiabilité de la livraison des Messages de Nouvelle Session à travers les tunnels, où ils doivent être fragmentés en plusieurs messages de tunnel de 1024 octets. Le succès de livraison est proportionnel au nombre exponentiel de fragments. Les implémentations peuvent utiliser diverses stratégies pour limiter la taille du message, au détriment de la livraison 0-RTT. Dépendant de l'implémentation.

Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

### SSU2

Nous définissons le MSB de la clé éphémère (key[31] & 0x80) dans la demande de session pour indiquer qu'il s'agit d'une connexion hybride. Cela nous permet d'exécuter à la fois NTCP standard et NTCP hybride sur le même port. Une seule variante hybride serait prise en charge et annoncée dans l'adresse du router. Par exemple, v=2,3 ou v=2,4 ou v=2,5.

En tant que Bob, testez si (X[31] & 0x80) != 0 après dé-obfuscation. Si c'est le cas, c'est une connexion PQ.

Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses de routeur.

## Compatibilité des routeurs

### Noms de Transport

La version minimale du router requise pour NTCP2-PQ est à déterminer.

### Types de chiffrement du router

Nous utilisons le champ version dans l'en-tête long et le définissons à 3 pour MLKEM512 et 4 pour MLKEM768. v=2,3,4 dans l'adresse serait suffisant.

#### Obfuscation

Vérifier que SSU2 peut gérer les RI signés MLDSA fragmentés sur plusieurs paquets (6-8 ?).

#### Routeurs de type 5/6/7

Note : Les codes de type sont uniquement à usage interne. Les routeurs resteront de type 4, et le support sera indiqué dans les adresses de routeur.

#### Routers de type 4

Dans tous les cas, utilisez les noms de transport NTCP2 et SSU2 comme d'habitude.

### Types de signatures de router

#### Recommandations

Nous avons plusieurs alternatives à considérer :

Non recommandé. Utilisez uniquement les nouveaux transports listés ci-dessus qui correspondent au type de router. Les anciens routers ne peuvent pas se connecter, construire des tunnels à travers, ou envoyer des messages netDb vers ceux-ci. Il faudrait plusieurs cycles de version pour déboguer et assurer le support avant d'activer par défaut. Pourrait prolonger le déploiement d'un an ou plus par rapport aux alternatives ci-dessous.

### Types de chiffrement LS

#### Routers de Type 12-17

Recommandé. Comme PQ n'affecte pas la clé statique X25519 ou les protocoles de handshake N, nous pourrions laisser les routers comme type 4, et simplement annoncer de nouveaux transports. Les anciens routers pourraient toujours se connecter, construire des tunnels à travers, ou envoyer des messages netDb vers.

MLKEM-768 est recommandé pour Ratchet, NTCP2, et SSU2, comme le meilleur équilibre entre sécurité et longueur de clé.

### Types de Sig. Dest.

#### Clés LS de type 5-7

Les routers plus anciens vérifient les RI et ne peuvent donc pas se connecter, construire des tunnels ou envoyer des messages netDb. Cela prendrait plusieurs cycles de version pour déboguer et assurer la compatibilité avant d'activer par défaut. Ce seraient les mêmes problèmes que le déploiement des types de chiffrement 5/6/7 ; cela pourrait prolonger le déploiement d'un an ou plus par rapport à l'alternative de déploiement du type de chiffrement 4 listée ci-dessus.

Non recommandé. Utilisez uniquement les nouveaux transports listés ci-dessus qui correspondent au type de router. Les anciens routers ne peuvent pas se connecter, construire des tunnels à travers, ou envoyer des messages netDb vers ceux-ci. Il faudrait plusieurs cycles de version pour déboguer et assurer le support avant d'activer par défaut. Pourrait prolonger le déploiement d'un an ou plus par rapport aux alternatives ci-dessous.

## Priorités et déploiement

Aucune alternative.

Les destinations peuvent prendre en charge plusieurs types de clés, mais seulement en effectuant des déchiffrements d'essai du message 1 avec chaque clé. La surcharge peut être atténuée en maintenant des compteurs de déchiffrements réussis pour chaque clé, et en essayant d'abord la clé la plus utilisée. Java I2P utilise cette stratégie pour ElGamal+X25519 sur la même destination.

Les routers vérifient les signatures de leaseSet et ne peuvent donc pas se connecter ou recevoir des leaseSets pour les destinations de type 12-17. Il faudrait plusieurs cycles de publication pour déboguer et assurer la prise en charge avant l'activation par défaut.

Aucune alternative.

Les données les plus précieuses sont le trafic de bout en bout, chiffré avec ratchet. En tant qu'observateur externe entre les sauts de tunnel, cela est chiffré deux fois de plus, avec le chiffrement de tunnel et le chiffrement de transport. En tant qu'observateur externe entre OBEP et IBGW, cela n'est chiffré qu'une fois de plus, avec le chiffrement de transport. En tant que participant OBEP ou IBGW, ratchet est le seul chiffrement. Cependant, comme les tunnels sont unidirectionnels, capturer les deux messages dans l'échange ratchet nécessiterait des routers complices, à moins que les tunnels ne soient construits avec l'OBEP et l'IBGW sur le même router.

Le modèle de menace PQ consistant à casser les clés d'authentification dans un délai raisonnable (disons quelques mois) puis à usurper l'authentification ou à déchiffrer en temps quasi-réel, est beaucoup plus lointain ? Et c'est alors que nous voudrions migrer vers des clés statiques PQC.

Les travaux sur la prise en charge des signatures MLDSA dans I2P sont en suspens jusqu'à la fin 2027 ou 2028, en attendant que les organismes de standardisation choisissent des algorithmes, éventuellement réduisent la taille des clés et/ou des signatures, et favorisent l'adoption par l'industrie. Voir [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/), [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/), et [PLANTS](https://datatracker.ietf.org/wg/plants/about/). Par ailleurs, l'adoption de MLDSA par l'industrie sera standardisée par l'IETF, le CA/Browser Forum et les autorités de certification. Les AC ont besoin d'abord d'un support par les modules matériels de sécurité (HSM), qui n'est pas disponible actuellement [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Nous nous attendons à ce que l'IETF et le CA/Browser Forum pilotent les décisions concernant les choix spécifiques de paramètres, notamment sur la prise en charge ou l'obligation de signatures composites [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Étape | Cible |
|-------|-------|
| Ratchet beta | Fin 2025 |
| Sélection du meilleur type de chiffrement | Début 2026 |
| NTCP2 beta | Début 2026 |
| SSU2 beta | Milieu 2026 |
| Ratchet production | Milieu 2026 |
| Ratchet par défaut | Fin 2026 |
| Signature beta | Fin 2026 |
| NTCP2 production | Fin 2026 |
| SSU2 production | Début 2027 |
| Sélection du meilleur type de signature | Début 2027 |
| NTCP2 par défaut | Début 2027 |
| SSU2 par défaut | Milieu 2027 |
| Signature production | Milieu 2027 |
## Migration

Ratchet est la priorité la plus élevée. Les transports sont suivants. Les signatures ont la priorité la plus basse.

Le déploiement des signatures sera également reporté d'un an ou plus par rapport au déploiement du chiffrement, car aucune rétrocompatibilité n'est possible. De plus, l'adoption de MLDSA dans l'industrie sera standardisée par le CA/Browser Forum et les Autorités de Certification. Les AC ont d'abord besoin du support des modules de sécurité matériel (HSM), qui n'est actuellement pas disponible [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Nous nous attendons à ce que le CA/Browser Forum conduise les décisions sur les choix de paramètres spécifiques, y compris s'il faut supporter ou exiger les signatures composites [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

## Problèmes

Le SHA256 devrait rester sûr pendant encore 20 à 30 ans et n'est pas menacé par l'informatique quantique. Voir la [présentation du NIST](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) et la [présentation du NCCOE](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf). Si le SHA256 venait à être cassé, nous aurions des problèmes bien plus graves (notamment au niveau du netDb).

## Références

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
