---
title: "Protocoles de Cryptographie Post-Quantique"
number: "169"
author: "zzz, orignal, drzed, eyedeekay"
created: "2025-01-21"
lastupdated: "2025-06-12"
status: "Ouvert"
thread: "http://zzz.i2p/topics/3294"
target: "0.9.80"
toc: true
---

## Aperçu

Bien que la recherche et la compétition pour une cryptographie post-quantique (PQ) appropriée se soient poursuivies pendant une décennie, les choix ne sont devenus clairs que récemment.

Nous avons commencé à examiner les implications de la cryptographie PQ en 2022 [zzz.i2p](http://zzz.i2p/topics/3294).

Les normes TLS ont ajouté le support du chiffrement hybride au cours des deux dernières années et il est maintenant utilisé pour une portion significative du trafic chiffré sur internet grâce au support dans Chrome et Firefox [Cloudflare](https://blog.cloudflare.com/pq-2024/).

Le NIST a récemment finalisé et publié les algorithmes recommandés pour la cryptographie post-quantique [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards). Plusieurs bibliothèques de cryptographie courantes prennent désormais en charge les standards NIST ou publieront leur support dans un avenir proche.

Les deux [Cloudflare](https://blog.cloudflare.com/pq-2024/) et [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) recommandent que la migration commence immédiatement. Voir également la FAQ PQ 2022 de la NSA [NSA](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF). I2P devrait être un leader en sécurité et en cryptographie. Il est temps maintenant d'implémenter les algorithmes recommandés. En utilisant notre système flexible de types cryptographiques et de types de signature, nous ajouterons des types pour la cryptographie hybride, et pour les signatures PQ et hybrides.

## Objectifs

- Sélectionner des algorithmes résistants aux PQ
- Ajouter des algorithmes PQ uniquement et hybrides aux protocoles I2P lorsque approprié
- Définir plusieurs variantes
- Sélectionner les meilleures variantes après implémentation, tests, analyse et recherche
- Ajouter le support de manière incrémentale et avec rétrocompatibilité

## Objectifs exclus

- Ne pas modifier les protocoles de chiffrement unidirectionnel (Noise N)
- Ne pas abandonner SHA256, non menacé à court terme par PQ
- Ne pas sélectionner les variantes préférées finales pour le moment

## Modèle de menaces

- Routeurs au OBEP ou IBGW, possiblement en collusion,
  stockant les messages garlic pour déchiffrement ultérieur (confidentialité persistante)
- Observateurs réseau
  stockant les messages de transport pour déchiffrement ultérieur (confidentialité persistante)
- Participants réseau forgeant des signatures pour RI, LS, streaming, datagrammes,
  ou autres structures

## Protocoles affectés

Nous modifierons les protocoles suivants, approximativement dans l'ordre de développement. Le déploiement global se déroulera probablement de fin 2025 à mi-2027. Voir la section Priorités et déploiement ci-dessous pour plus de détails.

| Protocol / Feature | Status |
|--------------------|--------|
| Hybrid MLKEM Ratchet and LS | Approved 2026-06; beta target 2025-08; release target 2025-11 |
| Hybrid MLKEM NTCP2 | Some details to be finalized |
| Hybrid MLKEM SSU2 | Some details to be finalized |
| MLDSA SigTypes 12-14 | Proposal is stable but may not be finalized until 2026 |
| MLDSA Dests | Tested on live net, requires net upgrade for floodfill support |
| Hybrid SigTypes 15-17 | Preliminary |
| Hybrid Dests | |
## Conception

Nous prendrons en charge les standards NIST FIPS 203 et 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) qui sont basés sur, mais NON compatibles avec, CRYSTALS-Kyber et CRYSTALS-Dilithium (versions 3.1, 3, et antérieures).

### Key Exchange

Nous prendrons en charge l'échange de clés hybride dans les protocoles suivants :

| Proto   | Noise Type | Support PQ only? | Support Hybrid? |
|---------|------------|------------------|-----------------|
| NTCP2   | XK         | no               | yes             |
| SSU2    | XK         | no               | yes             |
| Ratchet | IK         | no               | yes             |
| TBM     | N          | no               | no              |
| NetDB   | N          | no               | no              |
PQ KEM fournit uniquement des clés éphémères, et ne prend pas en charge directement les échanges de clés statiques tels que Noise XK et IK.

Noise N n'utilise pas d'échange de clés bidirectionnel et n'est donc pas adapté au chiffrement hybride.

Nous ne prendrons donc en charge que le chiffrement hybride, pour NTCP2, SSU2, et Ratchet. Nous définirons les trois variantes ML-KEM comme dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), pour un total de 3 nouveaux types de chiffrement. Les types hybrides ne seront définis qu'en combinaison avec X25519.

Les nouveaux types de chiffrement sont :

| Type | Code |
|------|------|
| MLKEM512_X25519 | 5 |
| MLKEM768_X25519 | 6 |
| MLKEM1024_X25519 | 7 |
La surcharge sera substantielle. Les tailles typiques des messages 1 et 2 (pour XK et IK) sont actuellement d'environ 100 octets (avant toute charge utile supplémentaire). Cela augmentera de 8x à 15x selon l'algorithme.

### Signatures

Nous prendrons en charge les signatures PQ et hybrides dans les structures suivantes :

| Type | Support PQ only? | Support Hybrid? |
|------|------------------|-----------------|
| RouterInfo | yes | yes |
| LeaseSet | yes | yes |
| Streaming SYN/SYNACK/Close | yes | yes |
| Repliable Datagrams | yes | yes |
| Datagram2 (prop. 163) | yes | yes |
| I2CP create session msg | yes | yes |
| SU3 files | yes | yes |
| X.509 certificates | yes | yes |
| Java keystores | yes | yes |
Nous prendrons donc en charge les signatures PQ uniquement et hybrides. Nous définirons les trois variantes ML-DSA comme dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf), trois variantes hybrides avec Ed25519, et trois variantes PQ uniquement avec prehash pour les fichiers SU3 seulement, soit 9 nouveaux types de signature au total. Les types hybrides ne seront définis qu'en combinaison avec Ed25519. Nous utiliserons le ML-DSA standard, PAS les variantes pre-hash (HashML-DSA), sauf pour les fichiers SU3.

Nous utiliserons la variante de signature "hedged" ou randomisée, et non la variante "déterministe", telle que définie dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) section 3.4. Cela garantit que chaque signature est différente, même lorsqu'elle porte sur les mêmes données, et fournit une protection supplémentaire contre les attaques par canaux auxiliaires. Consultez la section des notes d'implémentation ci-dessous pour des détails supplémentaires sur les choix d'algorithme, notamment l'encodage et le contexte.

Les nouveaux types de signature sont :

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
Les certificats X.509 et autres encodages DER utiliseront les structures composites et OID définis dans [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

La surcharge sera substantielle. Les tailles typiques de destination Ed25519 et d'identité de router sont de 391 octets. Celles-ci augmenteront de 3,5x à 6,8x selon l'algorithme. Les signatures Ed25519 font 64 octets. Celles-ci augmenteront de 38x à 76x selon l'algorithme. Les RouterInfo signés typiques, leaseSet, datagrammes avec réponse, et messages de streaming signés font environ 1KB. Ceux-ci augmenteront de 3x à 8x selon l'algorithme.

Comme les nouveaux types d'identités de destination et de router ne contiendront pas de remplissage, ils ne seront pas compressibles. Les tailles des destinations et des identités de router qui sont compressées en gzip durant le transit augmenteront de 12x à 38x selon l'algorithme.

### Legal Combinations

Pour les Destinations, les nouveaux types de signature sont pris en charge avec tous les types de chiffrement dans le leaseSet. Définissez le type de chiffrement dans le certificat de clé sur NONE (255).

Pour les RouterIdentities, le type de chiffrement ElGamal est obsolète. Les nouveaux types de signature sont pris en charge uniquement avec le chiffrement X25519 (type 4). Les nouveaux types de chiffrement seront indiqués dans les RouterAddresses. Le type de chiffrement dans le certificat de clé continuera d'être de type 4.

### New Crypto Required

- ML-KEM (anciennement CRYSTALS-Kyber) [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- ML-DSA (anciennement CRYSTALS-Dilithium) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
- SHA3-128 (anciennement Keccak-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Utilisé uniquement pour SHAKE128
- SHA3-256 (anciennement Keccak-512) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 et SHAKE256 (extensions XOF de SHA3-128 et SHA3-256) [FIPS 202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Les vecteurs de test pour SHA3-256, SHAKE128 et SHAKE256 sont disponibles à l'adresse [NIST](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Notez que la bibliothèque Java bouncycastle prend en charge tout ce qui précède. La prise en charge par la bibliothèque C++ se trouve dans OpenSSL 3.5 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Alternatives

Nous ne prendrons pas en charge [FIPS 205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf) (Sphincs+), c'est beaucoup beaucoup plus lent et plus volumineux que ML-DSA. Nous ne prendrons pas en charge le prochain FIPS206 (Falcon), il n'est pas encore standardisé. Nous ne prendrons pas en charge NTRU ou d'autres candidats PQ qui n'ont pas été standardisés par le NIST.

### Rosenpass

Il existe des recherches [paper](https://eprint.iacr.org/2020/379.pdf) sur l'adaptation de Wireguard (IK) pour la cryptographie PQ pure, mais plusieurs questions restent ouvertes dans ce document. Par la suite, cette approche a été implémentée sous le nom de Rosenpass [Rosenpass](https://rosenpass.eu/) [whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf) pour Wireguard PQ.

Rosenpass utilise une négociation similaire à Noise KK avec des clés statiques Classic McEliece 460896 prépartagées (500 Ko chacune) et des clés éphémères Kyber-512 (essentiellement MLKEM-512). Comme les textes chiffrés Classic McEliece ne font que 188 octets, et que les clés publiques et textes chiffrés Kyber-512 sont de taille raisonnable, les deux messages de négociation tiennent dans un MTU UDP standard. La clé partagée de sortie (osk) de la négociation PQ KK est utilisée comme clé prépartagée d'entrée (psk) pour la négociation Wireguard IK standard. Il y a donc deux négociations complètes au total, une purement PQ et une purement X25519.

Nous ne pouvons faire aucune de ces choses pour remplacer nos handshakes XK et IK car :

- Nous ne pouvons pas faire KK, Bob n'a pas la clé statique d'Alice
- Les clés statiques de 500KB sont beaucoup trop volumineuses
- Nous ne voulons pas d'aller-retour supplémentaire

Il y a beaucoup de bonnes informations dans le livre blanc, et nous l'examinerons pour des idées et de l'inspiration. TODO.

## Specification

### Échange de clés

Mettez à jour les sections et tableaux dans le document des structures communes [/docs/specs/common-structures/](/docs/specs/common-structures/) comme suit :

### Signatures

Les nouveaux types de clés publiques sont :

| Type | Public Key Length | Since | Usage |
|------|-------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 800 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 1184 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM512_CT | 768 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768_CT | 1088 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024_CT | 1568 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| NONE | 0 | 0.9.xx | See proposal 169, for destinations with PQ sig types only, not for RIs or Leasesets |
Les clés publiques hybrides sont la clé X25519. Les clés publiques KEM sont la clé PQ éphémère envoyée d'Alice à Bob. L'encodage et l'ordre des octets sont définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

Les clés MLKEM*_CT ne sont pas vraiment des clés publiques, elles sont le "texte chiffré" envoyé de Bob à Alice lors de la négociation Noise. Elles sont listées ici par souci d'exhaustivité.

### Combinaisons légales

Les nouveaux types de Private Key sont :

| Type | Private Key Length | Since | Usage |
|------|---------------------|-------|-------|
| MLKEM512_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM512 | 1632 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM768 | 2400 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
| MLKEM1024 | 3168 | 0.9.xx | See proposal 169, for handshakes only, not for Leasesets, RIs or Destinations |
Les clés privées hybrides sont les clés X25519. Les clés privées KEM sont uniquement pour Alice. L'encodage KEM et l'ordre des octets sont définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

### Nouvelle cryptographie requise

Les nouveaux types de clés publiques de signature sont :

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 1344 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA65ph | 1984 | 0.9.xx | Only for SU3 files, not for netdb structures |
| MLDSA87ph | 2624 | 0.9.xx | Only for SU3 files, not for netdb structures |
Les clés publiques de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Alternatives

Les nouveaux types de Signing Private Key sont :

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2560 | 0.9.xx | See proposal 169 |
| MLDSA65 | 4032 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4896 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 4064 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4928 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2592 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 4064 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4928 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Les clés privées de signature hybrides sont la clé Ed25519 suivie de la clé PQ, comme dans [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Rosenpass

Les nouveaux types de Signature sont :

| Type | Length (bytes) | Since | Usage |
|------|----------------|-------|-------|
| MLDSA44 | 2420 | 0.9.xx | See proposal 169 |
| MLDSA65 | 3309 | 0.9.xx | See proposal 169 |
| MLDSA87 | 4627 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 2484 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 3373 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 4691 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 2484 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA65ph | 3373 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
| MLDSA87ph | 4691 | 0.9.xx | Only for SU3 files, not for netdb structures. See proposal 169 |
Les signatures hybrides sont la signature Ed25519 suivie de la signature PQ, comme dans [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/). Les signatures hybrides sont vérifiées en vérifiant les deux signatures, et échouent si l'une d'entre elles échoue. L'encodage et l'ordre des octets sont définis dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf).

### Key Certificates

Les nouveaux types de clés publiques de signature sont :

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLDSA44 | 12 | 1312 | 0.9.xx | See proposal 169 |
| MLDSA65 | 13 | 1952 | 0.9.xx | See proposal 169 |
| MLDSA87 | 14 | 2592 | 0.9.xx | See proposal 169 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 0.9.xx | See proposal 169 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 0.9.xx | See proposal 169 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 0.9.xx | See proposal 169 |
| MLDSA44ph | 18 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA65ph | 19 | n/a | 0.9.xx | Only for SU3 files |
| MLDSA87ph | 20 | n/a | 0.9.xx | Only for SU3 files |
Les nouveaux types de clés publiques cryptographiques sont :

| Type | Type Code | Total Public Key Length | Since | Usage |
|------|-----------|-------------------------|-------|-------|
| MLKEM512_X25519 | 5 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM768_X25519 | 6 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| MLKEM1024_X25519 | 7 | 32 | 0.9.xx | See proposal 169, for Leasesets only, not for RIs or Destinations |
| NONE | 255 | 0 | 0.9.xx | See proposal 169 |
Les types de clés hybrides ne sont JAMAIS inclus dans les certificats de clé ; seulement dans les leaseSets.

Pour les destinations avec des types de signature Hybrid ou PQ, utilisez NONE (type 255) pour le type de chiffrement, mais il n'y a pas de clé crypto, et toute la section principale de 384 octets est pour la clé de signature.

### Structures Communes

Voici les longueurs pour les nouveaux types de Destination. Le type de chiffrement pour tous est NONE (type 255) et la longueur de clé de chiffrement est traitée comme 0. La section entière de 384 octets est utilisée pour la première partie de la clé publique de signature. NOTE : Ceci est différent de la spécification pour les types de signature ECDSA_SHA512_P521 et RSA, où nous avons maintenu la clé ElGamal de 256 octets dans la destination même si elle n'était pas utilisée.

Pas de remplissage. La longueur totale est de 7 + longueur totale de la clé. La longueur du certificat de clé est de 4 + longueur de clé excédentaire.

Exemple de flux d'octets de destination de 1319 octets pour MLDSA44 :

skey[0:383] 5 (932 >> 8) (932 & 0xff) 00 12 00 255 skey[384:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total Dest Length |
|------|-----------|-------------------------|------|--------|-------------------|
| MLDSA44 | 12 | 1312 | 384 | 928 | 1319 |
| MLDSA65 | 13 | 1952 | 384 | 1568 | 1959 |
| MLDSA87 | 14 | 2592 | 384 | 2208 | 2599 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 384 | 960 | 1351 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 384 | 1600 | 1991 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 384 | 2240 | 2631 |
### PublicKey

Voici les longueurs pour les nouveaux types de Destination. Le type Enc pour tous est X25519 (type 4). Toute la section de 352 octets après la clé publique X25519 est utilisée pour la première partie de la clé publique de signature. Pas de rembourrage. La longueur totale est 39 + longueur totale de la clé. La longueur du certificat de clé est 4 + longueur de clé excédentaire.

Exemple de flux d'octets d'identité de routeur de 1351 octets pour MLDSA44 :

enckey[0:31] skey[0:351] 5 (960 >> 8) (960 & 0xff) 00 12 00 4 skey[352:1311]

| Type | Type Code | Total Public Key Length | Main | Excess | Total RouterIdent Length |
|------|-----------|-------------------------|------|--------|--------------------------|
| MLDSA44 | 12 | 1312 | 352 | 960 | 1351 |
| MLDSA65 | 13 | 1952 | 352 | 1600 | 1991 |
| MLDSA87 | 14 | 2592 | 352 | 2240 | 2631 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 15 | 1344 | 352 | 992 | 1383 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 16 | 1984 | 352 | 1632 | 2023 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 17 | 2624 | 352 | 2272 | 2663 |
### CléPrivée

Les handshakes utilisent les motifs de handshake [Noise Protocol](https://noiseprotocol.org/noise.html).

La correspondance de lettres suivante est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message
- e1 = clé PQ éphémère à usage unique, envoyée d'Alice à Bob
- ekem1 = le texte chiffré KEM, envoyé de Bob à Alice

Les modifications suivantes à XK et IK pour la confidentialité parfaite hybride (hfs) sont spécifiées dans [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 5 :

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
Le motif e1 est défini comme suit, tel que spécifié dans [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4 :

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
Le motif ekem1 est défini comme suit, tel que spécifié dans [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4 :

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
### SigningPublicKey

#### Issues

- Devrions-nous changer la fonction de hachage du handshake ? Voir [comparison](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3).
  SHA256 n'est pas vulnérable à PQ, mais si nous voulons mettre à niveau
  notre fonction de hachage, c'est le moment, pendant que nous changeons d'autres choses.
  La proposition SSH IETF actuelle [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/) est d'utiliser MLKEM768
  avec SHA256, et MLKEM1024 avec SHA384. Cette proposition inclut
  une discussion des considérations de sécurité.
- Devrions-nous arrêter d'envoyer des données ratchet 0-RTT (autres que le LS) ?
- Devrions-nous basculer le ratchet de IK vers XK si nous n'envoyons pas de données 0-RTT ?

#### Overview

Cette section s'applique aux protocoles IK et XK.

La poignée de main hybride est définie dans [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Le premier message, d'Alice vers Bob, contient e1, la clé d'encapsulation, avant la charge utile du message. Ceci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant qu'Alice) ou DecryptAndHash() (en tant que Bob). Ensuite, traitez la charge utile du message comme d'habitude.

Le deuxième message, de Bob à Alice, contient ekem1, le texte chiffré, avant la charge utile du message. Celui-ci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant que Bob) ou DecryptAndHash() (en tant qu'Alice). Ensuite, calculez le kem_shared_key et appelez MixKey(kem_shared_key). Puis traitez la charge utile du message comme d'habitude.

#### Defined ML-KEM Operations

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés comme défini dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Notez que l'encap_key et le ciphertext sont tous deux chiffrés à l'intérieur des blocs ChaCha/Poly dans les messages 1 et 2 de la négociation Noise. Ils seront déchiffrés dans le cadre du processus de négociation.

La kem_shared_key est mélangée dans la clé de chaînage avec MixHash(). Voir ci-dessous pour les détails.

#### Alice KDF for Message 1

Pour XK : Après le motif de message 'es' et avant la charge utile, ajouter :

OU

Pour IK : Après le motif de message 'es' et avant le motif de message 's', ajouter :

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
#### Bob KDF for Message 1

Pour XK : Après le modèle de message 'es' et avant la charge utile, ajouter :

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
#### Bob KDF for Message 2

Pour XK : Après le motif de message 'ee' et avant la charge utile, ajouter :

OU

Pour IK : Après le pattern de message 'ee' et avant le pattern de message 'se', ajouter :

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
```
#### Alice KDF for Message 2

Après le modèle de message 'ee' (et avant le modèle de message 'ss' pour IK), ajouter :

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
```
#### KDF for Message 3 (XK only)

inchangé

#### KDF for split()

inchangé

### SigningPrivateKey

Mettre à jour la spécification ECIES-Ratchet [/docs/specs/ecies/](/docs/specs/ecies/) comme suit :

#### Noise identifiers

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1b) New session format (with binding)

Changements : Le ratchet actuel contenait la clé statique dans la première section ChaCha, et la charge utile dans la seconde section. Avec ML-KEM, il y a maintenant trois sections. La première section contient la clé publique PQ chiffrée. La deuxième section contient la clé statique. La troisième section contient la charge utile.

Format chiffré :

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

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 96+pl | 64+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 912+pl | 880+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1296+pl | 1360+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1680+pl | 1648+pl | 1568+pl | 1568 | pl |
Notez que la charge utile doit contenir un bloc DateTime, donc la taille minimale de la charge utile est de 7. Les tailles minimales du message 1 peuvent être calculées en conséquence.

#### 1g) New Session Reply format

Changements : Le ratchet actuel a une charge utile vide pour la première section ChaCha, et la charge utile dans la seconde section. Avec ML-KEM, il y a maintenant trois sections. La première section contient le texte chiffré PQ crypté. La seconde section a une charge utile vide. La troisième section contient la charge utile.

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 72+pl | 32+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 856+pl | 816+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1176+pl | 1136+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | 32 | 1656+pl | 1616+pl | 1568+pl | 1568 | pl |
Notez que bien que le message 2 ait normalement une charge utile non nulle, la spécification ratchet [/docs/specs/ecies/](/docs/specs/ecies/) ne l'exige pas, donc la taille minimale de charge utile est de 0. Les tailles minimales du message 2 peuvent être calculées en conséquence.

### Signature

Mettez à jour la spécification NTCP2 [/docs/specs/ntcp2/](/docs/specs/ntcp2/) comme suit :

#### Noise identifiers

- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfsaesobfse+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### 1) SessionRequest

Changements : Le NTCP2 actuel ne contient que les options dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Contenu brut :

```
+----+----+----+----+----+----+----+----+
  |                                       |
  +        obfuscated with RH_B           +
  |       AES-CBC-256 encrypted X         |
  +             (32 bytes)                +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (MLKEM)            |
  +      (see table below for length)     +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  ~   n = 0                               ~
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaChaPoly frame (options)          |
  +         32 bytes                      +
  |   k defined in KDF for message 1      |
  +   n = 0                               +
  |   see KDF for associated data         |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  ~         padding (optional)            ~
  |     length defined in options block   |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Données non chiffrées (tag d'authentification Poly1305 non affiché) :

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
Tailles :

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | opt len |
|------|-----------|-------|-----------|---------------|---------------|------------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 880+pad | 848 | 816 | 800 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1264+pad | 1232 | 1200 | 1184 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1648+pad | 1616 | 1584 | 1568 | 16 |
Note : Les codes de type sont destinés à un usage interne uniquement. Les routers resteront de type 4, et la prise en charge sera indiquée dans les adresses de router.

#### 2) SessionCreated

Changements : Le NTCP2 actuel contient uniquement les options de la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Contenu brut :

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
  |   ChaChaPoly frame (MLKEM)            |
  +   Encrypted and authenticated data    +
  -      (see table below for length)     -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaChaPoly frame (options)          |
  +   Encrypted and authenticated data    +
  -           32 bytes                    -
  +   k defined in KDF for message 2      +
  |   n = 0; see KDF for associated data  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     unencrypted authenticated         |
  +         padding (optional)            +
  |     length defined in options block   |
  ~               .   .   .               ~
  |                                       |
  +----+----+----+----+----+----+----+----+

  Same as before except add a second ChaChaPoly frame
```
Données non chiffrées (tag d'authentification Poly1305 non affiché) :

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | opt len |
|------|-----------|-------|-----------|---------------|---------------|-----------|---------|
| X25519 | 4 | 32 | 64+pad | 32 | 16 | -- | 16 |
| MLKEM512_X25519 | 5 | 32 | 848+pad | 816 | 784 | 768 | 16 |
| MLKEM768_X25519 | 6 | 32 | 1136+pad | 1104 | 1104 | 1088 | 16 |
| MLKEM1024_X25519 | 7 | 32 | 1616+pad | 1584 | 1584 | 1568 | 16 |
Remarque : Les codes de type sont destinés à un usage interne uniquement. Les routers resteront de type 4, et le support sera indiqué dans les adresses de router.

#### 3) SessionConfirmed

Inchangé

#### Key Derivation Function (KDF) (for data phase)

Inchangé

### Certificats de Clé

Mettre à jour la spécification SSU2 [/docs/specs/ssu2/](/docs/specs/ssu2/) comme suit :

#### Noise identifiers

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Long Header

L'en-tête long fait 32 octets. Il est utilisé avant qu'une session ne soit créée, pour Token Request, SessionRequest, SessionCreated, et Retry. Il est également utilisé pour les messages Peer Test et Hole Punch hors session.

TODO : Nous pourrions utiliser en interne le champ version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768. Ne faisons-nous cela que pour les types 0 et 1 ou pour les 6 types ?

Avant le chiffrement d'en-tête :

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

  ver :: The protocol version, equal to 2
         TODO We could internally use the version field and use 3 for MLKEM512 and 4 for MLKEM768.

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### Short Header

inchangé

#### SessionRequest (Type 0)

Changements : Le SSU2 actuel ne contient que les données de bloc dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Contenu brut :

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
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Données non chiffrées (tag d'authentification Poly1305 non affiché) :

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
Tailles, sans inclure la surcharge IP :

| Type | Type Code | X len | Msg 1 len | Msg 1 Enc len | Msg 1 Dec len | PQ key len | pl len |
|------|-----------|-------|-----------|---------------|---------------|------------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Note : Les codes de type sont uniquement à usage interne. Les routers resteront de type 4, et la prise en charge sera indiquée dans les adresses de router.

MTU minimum pour MLKEM768_X25519 : Environ 1316 pour IPv4 et 1336 pour IPv6.

#### SessionCreated (Type 1)

Modifications : Le SSU2 actuel ne contient que les données de bloc dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Contenu brut :

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
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  n = 0; see KDF for associated data   |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Données non chiffrées (tag d'authentification Poly1305 non affiché) :

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

| Type | Type Code | Y len | Msg 2 len | Msg 2 Enc len | Msg 2 Dec len | PQ CT len | pl len |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1118+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | too big | | | | |
Note : Les codes de type sont uniquement à usage interne. Les routers resteront de type 4, et le support sera indiqué dans les adresses de router.

MTU minimum pour MLKEM768_X25519 : Environ 1316 pour IPv4 et 1336 pour IPv6.

#### SessionConfirmed (Type 2)

inchangé

#### KDF for data phase

inchangé

#### Problèmes

Les blocs Relay, les blocs Peer Test, et les messages Peer Test contiennent tous des signatures. Malheureusement, les signatures PQ sont plus volumineuses que le MTU. Il n'existe actuellement aucun mécanisme pour fragmenter les blocs Relay ou Peer Test ou les messages sur plusieurs paquets UDP. Le protocole doit être étendu pour supporter la fragmentation. Cela sera fait dans une proposition séparée à déterminer. Jusqu'à ce que cela soit terminé, Relay et Peer Test ne seront pas supportés.

#### Aperçu

Nous pourrions utiliser en interne le champ de version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768.

Pour les messages 1 et 2, MLKEM768 augmenterait la taille des paquets au-delà du MTU minimum de 1280. Probablement qu'on ne le prendrait simplement pas en charge pour cette connexion si le MTU était trop bas.

Pour les messages 1 et 2, MLKEM1024 augmenterait la taille des paquets au-delà du MTU maximum de 1500. Cela nécessiterait de fragmenter les messages 1 et 2, et ce serait une grosse complication. Probablement qu'on ne le fera pas.

Relay et Test de Pair : Voir ci-dessus

### Tailles des destinations

TODO : Existe-t-il un moyen plus efficace de définir la signature/vérification pour éviter de copier la signature ?

### Tailles des RouterIdent

À FAIRE

[IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) section 8.1 interdit HashML-DSA dans les certificats X.509 et n'assigne pas d'OID pour HashML-DSA, en raison de complexités d'implémentation et de sécurité réduite.

Pour les signatures PQ uniquement des fichiers SU3, utilisez les OID définis dans [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/) des variantes sans pré-hachage pour les certificats. Nous ne définissons pas de signatures hybrides des fichiers SU3, car nous pourrions avoir à hacher les fichiers deux fois (bien que HashML-DSA et X2559 utilisent la même fonction de hachage SHA512). De plus, concaténer deux clés et signatures dans un certificat X.509 serait complètement non-standard.

Notez que nous interdisons la signature Ed25519 des fichiers SU3, et bien que nous ayons défini la signature Ed25519ph, nous ne nous sommes jamais mis d'accord sur un OID pour celle-ci, ni ne l'avons utilisée.

Les types de signature normaux sont interdits pour les fichiers SU3 ; utilisez les variantes ph (prehash).

### Modèles de négociation

La nouvelle taille maximale de Destination sera de 2599 (3468 en base 64).

Mettre à jour les autres documents qui donnent des conseils sur les tailles de Destination, notamment :

- SAMv3
- Bittorrent
- Directives pour les développeurs
- Nommage / carnet d'adresses / serveurs de saut
- Autres documents

## Overhead Analysis

### KDF de négociation Noise

Augmentation de taille (octets) :

| Type | Pubkey (Msg 1) | Cipertext (Msg 2) |
|------|----------------|-------------------|
| MLKEM512_X25519 | +816 | +784 |
| MLKEM768_X25519 | +1200 | +1104 |
| MLKEM1024_X25519 | +1584 | +1584 |
Vitesse :

Vitesses telles que rapportées par [Cloudflare](https://blog.cloudflare.com/pq-2024/) :

| Type | Relative speed |
|------|----------------|
| X25519 DH/keygen | baseline |
| MLKEM512 | 2.25x faster |
| MLKEM768 | 1.5x faster |
| MLKEM1024 | 1x (same) |
| XK | 4x DH (keygen + 3 DH) |
| MLKEM512_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower |
| MLKEM768_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower |
| MLKEM1024_X25519 | 4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower |
Résultats de tests préliminaires en Java :

| Type | Relative DH/encaps | DH/decaps | keygen |
|------|-------------------|-----------|--------|
| X25519 | baseline | baseline | baseline |
| MLKEM512 | 29x faster | 22x faster | 17x faster |
| MLKEM768 | 17x faster | 14x faster | 9x faster |
| MLKEM1024 | 12x faster | 10x faster | 6x faster |
### Signatures

Taille :

Tailles typiques des clés, signatures, RIdent, Dest ou augmentations de taille (Ed25519 inclus pour référence) en supposant un type de chiffrement X25519 pour les RI. Taille ajoutée pour un Router Info, LeaseSet, datagrammes répondables, et chacun des deux paquets de streaming (SYN et SYN ACK) listés. Les Destinations et Leasesets actuels contiennent un remplissage répété et sont compressibles en transit. Les nouveaux types ne contiennent pas de remplissage et ne seront pas compressibles, résultant en une augmentation de taille beaucoup plus importante en transit. Voir la section conception ci-dessus.

| Type | Pubkey | Sig | Key+Sig | RIdent | Dest | RInfo | LS/Streaming/Datagram (each msg) |
|------|--------|-----|---------|--------|------|-------|----------------------------------|
| EdDSA_SHA512_Ed25519 | 32 | 64 | 96 | 391 | 391 | baseline | baseline |
| MLDSA44 | 1312 | 2420 | 3732 | 1351 | 1319 | +3316 | +3284 |
| MLDSA65 | 1952 | 3309 | 5261 | 1991 | 1959 | +5668 | +5636 |
| MLDSA87 | 2592 | 4627 | 7219 | 2631 | 2599 | +7072 | +7040 |
| MLDSA44_EdDSA_SHA512_Ed25519 | 1344 | 2484 | 3828 | 1383 | 1351 | +3412 | +3380 |
| MLDSA65_EdDSA_SHA512_Ed25519 | 1984 | 3373 | 5357 | 2023 | 1991 | +5668 | +5636 |
| MLDSA87_EdDSA_SHA512_Ed25519 | 2624 | 4691 | 7315 | 2663 | 2631 | +7488 | +7456 |
Vitesse :

Vitesses telles que rapportées par [Cloudflare](https://blog.cloudflare.com/pq-2024/) :

| Type | Relative speed sign | verify |
|------|---------------------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline |
| MLDSA44 | 5x slower | 2x faster |
| MLDSA65 | ??? | ??? |
| MLDSA87 | ??? | ??? |
Résultats de tests préliminaires en Java :

| Type | Relative speed sign | verify | keygen |
|------|---------------------|--------|--------|
| EdDSA_SHA512_Ed25519 | baseline | baseline | baseline |
| MLDSA44 | 4.6x slower | 1.7x faster | 2.6x faster |
| MLDSA65 | 8.1x slower | same | 1.5x faster |
| MLDSA87 | 11.1x slower | 1.5x slower | same |
## Security Analysis

Les catégories de sécurité NIST sont résumées dans [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) diapositive 10. Critères préliminaires : Notre catégorie de sécurité NIST minimale devrait être 2 pour les protocoles hybrides et 3 pour PQ uniquement.

| Category | As Secure As |
|----------|--------------|
| 1 | AES128 |
| 2 | SHA256 |
| 3 | AES192 |
| 4 | SHA384 |
| 5 | AES256 |
### Handshakes

Ce sont tous des protocoles hybrides. Il faut probablement privilégier MLKEM768 ; MLKEM512 n'est pas suffisamment sécurisé.

Catégories de sécurité NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) :

| Algorithm | Security Category |
|-----------|-------------------|
| MLKEM512 | 1 |
| MLKEM768 | 3 |
| MLKEM1024 | 5 |
### Signatures

Cette proposition définit à la fois les types de signature hybrides et PQ uniquement. MLDSA44 hybride est préférable à MLDSA65 PQ uniquement. Les tailles de clés et de signatures pour MLDSA65 et MLDSA87 sont probablement trop importantes pour nous, du moins au début.

Catégories de sécurité NIST [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) :

| Algorithm | Security Category |
|-----------|-------------------|
| MLDSA44 | 2 |
| MLKEM67 | 3 |
| MLKEM87 | 5 |
## Type Preferences

Bien que nous définirons et implémenterons 3 types de chiffrement et 9 types de signature, nous prévoyons de mesurer les performances pendant le développement, et d'analyser davantage les effets de l'augmentation de la taille des structures. Nous continuerons également à rechercher et surveiller les développements dans d'autres projets et protocoles.

Après un an ou plus de développement, nous tenterons de nous fixer sur un type préféré ou par défaut pour chaque cas d'usage. La sélection nécessitera de faire des compromis entre bande passante, CPU et niveau de sécurité estimé. Tous les types peuvent ne pas être adaptés ou autorisés pour tous les cas d'usage.

Les préférences préliminaires sont les suivantes, sous réserve de modifications :

Chiffrement : MLKEM768_X25519

Signatures : MLDSA44_EdDSA_SHA512_Ed25519

Les restrictions préliminaires sont les suivantes, sous réserve de modifications :

Chiffrement : MLKEM1024_X25519 non autorisé pour SSU2

Signatures : MLDSA87 et la variante hybride probablement trop volumineux ; MLDSA65 et la variante hybride peuvent être trop volumineux

## Implementation Notes

### Library Support

Les bibliothèques Bouncycastle, BoringSSL et WolfSSL prennent désormais en charge MLKEM et MLDSA. Le support OpenSSL sera disponible dans leur version 3.5 le 8 avril 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

La bibliothèque Noise de southernstorm.com adaptée par Java I2P contenait un support préliminaire pour les handshakes hybrides, mais nous l'avons supprimé car inutilisé ; nous devrons le rajouter et le mettre à jour pour correspondre à [Noise HFS spec](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Signing Variants

Nous utiliserons la variante de signature "hedged" ou randomisée, et non la variante "déterministe", telle que définie dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) section 3.4. Ceci garantit que chaque signature est différente, même pour les mêmes données, et fournit une protection supplémentaire contre les attaques par canaux auxiliaires. Bien que [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) spécifie que la variante "hedged" est celle par défaut, cela peut ou ne peut pas être vrai dans diverses bibliothèques. Les implémenteurs doivent s'assurer que la variante "hedged" est utilisée pour la signature.

Nous utilisons le processus de signature normal (appelé Pure ML-DSA Signature Generation) qui encode le message en interne sous la forme 0x00 || len(ctx) || ctx || message, où ctx est une valeur optionnelle de taille 0x00..0xFF. Nous n'utilisons aucun contexte optionnel. len(ctx) == 0. Ce processus est défini dans [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) Algorithme 2 étape 10 et Algorithme 3 étape 5. Notez que certains vecteurs de test publiés peuvent nécessiter la définition d'un mode où le message n'est pas encodé.

### Reliability

L'augmentation de la taille entraînera beaucoup plus de fragmentation de tunnel pour les stockages NetDB, les établissements de connexion streaming, et autres messages. Vérifiez les changements de performance et de fiabilité.

### Structure Sizes

Trouvez et vérifiez tout code qui limite la taille en octets des informations de router et des leaseSets.

### NetDB

Examiner et possiblement réduire le maximum de LS/RI stockés en RAM ou sur disque, pour limiter l'augmentation du stockage. Augmenter les exigences minimales de bande passante pour les floodfills ?

### Ratchet

#### Opérations ML-KEM Définies

La classification/détection automatique de multiples protocoles sur les mêmes tunnels devrait être possible basée sur une vérification de la longueur du message 1 (New Session Message). En utilisant MLKEM512_X25519 comme exemple, la longueur du message 1 est de 816 octets plus grande que le protocole ratchet actuel, et la taille minimale du message 1 (avec seulement une charge utile DateTime incluse) est de 919 octets. La plupart des tailles de message 1 avec le ratchet actuel ont une charge utile de moins de 816 octets, donc elles peuvent être classifiées comme ratchet non-hybride. Les gros messages sont probablement des POSTs qui sont rares.

Donc la stratégie recommandée est :

- Si le message 1 fait moins de 919 octets, c'est le protocole ratchet actuel.
- Si le message 1 fait 919 octets ou plus, c'est probablement MLKEM512_X25519.
  Essayez d'abord MLKEM512_X25519, et si cela échoue, essayez le protocole ratchet actuel.

Cela devrait nous permettre de prendre en charge efficacement le ratchet standard et le ratchet hybride sur la même destination, tout comme nous avons précédemment pris en charge ElGamal et ratchet sur la même destination. Par conséquent, nous pouvons migrer vers le protocole hybride MLKEM beaucoup plus rapidement que si nous ne pouvions pas prendre en charge les protocoles duaux pour la même destination, car nous pouvons ajouter la prise en charge MLKEM aux destinations existantes.

Les combinaisons prises en charge requises sont :

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Les combinaisons suivantes peuvent être complexes, et ne sont PAS requises d'être supportées, mais peuvent l'être, selon l'implémentation :

- Plus d'un MLKEM
- ElG + un ou plusieurs MLKEM
- X25519 + un ou plusieurs MLKEM
- ElG + X25519 + un ou plusieurs MLKEM

Nous ne pouvons pas tenter de prendre en charge plusieurs algorithmes MLKEM (par exemple, MLKEM512_X25519 et MLKEM_768_X25519) sur la même destination. Choisissez-en un seul ; cependant, cela dépend de notre sélection d'une variante MLKEM préférée, afin que les tunnels clients HTTP puissent en utiliser une. Dépendant de l'implémentation.

Nous POUVONS tenter de prendre en charge trois algorithmes (par exemple X25519, MLKEM512_X25519, et MLKEM769_X25519) sur la même destination. La classification et la stratégie de nouvelle tentative peuvent être trop complexes. La configuration et l'interface utilisateur de configuration peuvent être trop complexes. Dépendant de l'implémentation.

Nous ne tenterons probablement PAS de prendre en charge les algorithmes ElGamal et hybrides sur la même destination. ElGamal est obsolète, et ElGamal + hybride uniquement (sans X25519) n'a pas beaucoup de sens. De plus, les messages de nouvelle session ElGamal et hybrides sont tous deux volumineux, donc les stratégies de classification devraient souvent essayer les deux déchiffrements, ce qui serait inefficace. Dépendant de l'implémentation.

Les clients peuvent utiliser les mêmes clés statiques X25519 ou des clés différentes pour les protocoles X25519 et hybride sur les mêmes tunnels, selon l'implémentation.

#### Alice KDF pour le Message 1

La spécification ECIES permet les Garlic Messages dans la charge utile du New Session Message, ce qui permet la livraison 0-RTT du paquet de streaming initial, généralement un HTTP GET, avec le leaseset du client. Cependant, la charge utile du New Session Message n'a pas de confidentialité persistante. Comme cette proposition met l'accent sur la confidentialité persistante améliorée pour le ratchet, les implémentations peuvent ou devraient reporter l'inclusion de la charge utile de streaming, ou du message de streaming complet, jusqu'au premier Existing Session Message. Ceci se ferait au détriment de la livraison 0-RTT. Les stratégies peuvent également dépendre du type de trafic ou du type de tunnel, ou de GET vs. POST, par exemple. Dépendant de l'implémentation.

#### Bob KDF pour le Message 1

MLKEM, MLDSA, ou les deux sur la même destination, augmenteront considérablement la taille du Message de Nouvelle Session, comme décrit ci-dessus. Cela peut diminuer significativement la fiabilité de la livraison des Messages de Nouvelle Session à travers les tunnels, où ils doivent être fragmentés en plusieurs messages de tunnel de 1024 octets. Le succès de la livraison est proportionnel au nombre exponentiel de fragments. Les implémentations peuvent utiliser diverses stratégies pour limiter la taille du message, au détriment de la livraison 0-RTT. Dépendant de l'implémentation.

### Ratchet

Nous pouvons définir le MSB de la clé éphémère (key[31] & 0x80) dans la requête de session pour indiquer qu'il s'agit d'une connexion hybride. Cela nous permettrait d'exécuter à la fois NTCP standard et NTCP hybride sur le même port. Seule une variante hybride serait prise en charge, et annoncée dans l'adresse du router. Par exemple, v=2,3 ou v=2,4 ou v=2,5.

Si nous ne faisons pas cela, nous avons besoin d'une adresse/port de transport différent, et un nouveau nom de protocole tel que "NTCP1PQ1".

Note : Les codes de type sont uniquement à usage interne. Les routers resteront de type 4, et le support sera indiqué dans les adresses des routers.

TODO

### SSU2

PEUT nécessiter une adresse/port de transport différent, mais espérons que non, nous avons un en-tête avec des flags pour le message 1. Nous pourrions utiliser en interne le champ version et utiliser 3 pour MLKEM512 et 4 pour MLKEM768. Peut-être que simplement v=2,3,4 dans l'adresse serait suffisant. Mais nous avons besoin d'identifiants pour les deux nouveaux algorithmes : 3a, 3b ?

Vérifiez et confirmez que SSU2 peut gérer le RI fragmenté sur plusieurs paquets (6-8 ?). i2pd ne supporte actuellement que 2 fragments maximum ?

Note : Les codes de type sont uniquement à usage interne. Les routers resteront de type 4, et le support sera indiqué dans les adresses de router.

À FAIRE

## Router Compatibility

### Transport Names

Nous n'aurons probablement pas besoin de nouveaux noms de transport, si nous pouvons exécuter à la fois la version standard et hybride sur le même port, avec des indicateurs de version.

Si nous avons besoin de nouveaux noms de transport, ils seraient :

| Transport | Type |
|-----------|------|
| NTCP2PQ1 | MLKEM512_X25519 |
| NTCP2PQ2 | MLKEM768_X25519 |
| NTCP2PQ3 | MLKEM1024_X25519 |
| SSU2PQ1 | MLKEM512_X25519 |
| SSU2PQ2 | MLKEM768_X25519 |
Notez que SSU2 ne peut pas prendre en charge MLKEM1024, il est trop volumineux.

### Router Enc. Types

Nous avons plusieurs alternatives à considérer :

#### Bob KDF pour le Message 2

Non recommandé. Utilisez uniquement les nouveaux transports listés ci-dessus qui correspondent au type de router. Les anciens routers ne peuvent pas se connecter, construire des tunnels à travers, ou envoyer des messages netDb vers. Il faudrait plusieurs cycles de version pour déboguer et assurer le support avant d'activer par défaut. Pourrait prolonger le déploiement d'un an ou plus par rapport aux alternatives ci-dessous.

#### Alice KDF pour Message 2

Recommandé. Comme PQ n'affecte pas la clé statique X25519 ou les protocoles de handshake N, nous pourrions laisser les routers en type 4, et simplement annoncer de nouveaux transports. Les routers plus anciens pourraient encore se connecter, construire des tunnels à travers, ou envoyer des messages netDb vers.

#### KDF pour le Message 3 (XK uniquement)

Les routeurs de type 4 pourraient annoncer à la fois des adresses NTCP2 et NTCP2PQ*. Celles-ci pourraient utiliser la même clé statique et d'autres paramètres, ou non. Elles devront probablement être sur des ports différents ; il serait très difficile de supporter à la fois les protocoles NTCP2 et NTCP2PQ* sur le même port, car il n'y a pas d'en-tête ou de tramage qui permettrait à Bob de classifier et de tramer le message Session Request entrant.

Des ports et adresses séparés seront difficiles pour Java mais simples pour i2pd.

#### KDF pour split()

Les routers de type 4 pourraient annoncer à la fois des adresses SSU2 et SSU2PQ*. Avec des drapeaux d'en-tête ajoutés, Bob pourrait identifier le type de transport entrant dans le premier message. Par conséquent, nous pourrions prendre en charge à la fois SSU2 et SSUPQ* sur le même port.

Celles-ci pourraient être publiées sous des adresses séparées (comme i2pd l'a fait lors de transitions précédentes) ou dans la même adresse avec un paramètre indiquant le support PQ (comme Java i2p l'a fait lors de transitions précédentes).

Si dans la même adresse, ou sur le même port dans des adresses différentes, ceux-ci utiliseraient la même clé statique et les autres paramètres. Si dans des adresses différentes avec des ports différents, ceux-ci pourraient utiliser la même clé statique et les autres paramètres, ou pas.

Des ports et adresses séparés seront difficiles pour Java mais simples pour i2pd.

#### Recommendations

À FAIRE

### NTCP2

#### Identificateurs Noise

Les routers plus anciens vérifient les RI et ne peuvent donc pas se connecter, construire des tunnels à travers, ou envoyer des messages netdb à. Il faudrait plusieurs cycles de versions pour déboguer et assurer le support avant d'activer par défaut. Ce seraient les mêmes problèmes que le déploiement du type de chiffrement 5/6/7 ; pourrait prolonger le déploiement d'un an ou plus par rapport à l'alternative de déploiement du type de chiffrement type 4 listée ci-dessus.

Aucune alternative.

### LS Enc. Types

#### 1b) Nouveau format de session (avec liaison)

Ces clés peuvent être présentes dans le LS avec des clés X25519 de type 4 plus anciennes. Les routeurs plus anciens ignoreront les clés inconnues.

Les destinations peuvent prendre en charge plusieurs types de clés, mais seulement en effectuant des déchiffrements d'essai du message 1 avec chaque clé. La surcharge peut être atténuée en maintenant des compteurs de déchiffrements réussis pour chaque clé, et en essayant d'abord la clé la plus utilisée. Java I2P utilise cette stratégie pour ElGamal+X25519 sur la même destination.

### Dest. Sig. Types

#### 1g) Format de réponse de nouvelle session

Les routeurs vérifient les signatures des leaseSets et ne peuvent donc pas se connecter ou recevoir des leaseSets pour les destinations de type 12-17. Il faudrait plusieurs cycles de version pour déboguer et garantir la prise en charge avant d'activer par défaut.

Aucune alternative.

## Spécification

Les données les plus précieuses sont le trafic de bout en bout, chiffré avec ratchet. En tant qu'observateur externe entre les sauts de tunnel, cela est chiffré deux fois de plus, avec le chiffrement de tunnel et le chiffrement de transport. En tant qu'observateur externe entre OBEP et IBGW, cela n'est chiffré qu'une fois de plus, avec le chiffrement de transport. En tant que participant OBEP ou IBGW, ratchet est le seul chiffrement. Cependant, comme les tunnels sont unidirectionnels, capturer les deux messages dans la négociation ratchet nécessiterait des routeurs complices, à moins que les tunnels ne soient construits avec l'OBEP et l'IBGW sur le même routeur.

Le modèle de menace PQ le plus préoccupant actuellement est le stockage du trafic aujourd'hui, pour un déchiffrement dans de très nombreuses années (confidentialité persistante). Une approche hybride protégerait contre cela.

Le modèle de menace PQ de compromission des clés d'authentification dans un délai raisonnable (disons quelques mois) puis d'usurpation de l'authentification ou de déchiffrement en quasi-temps réel, est beaucoup plus éloigné ? Et c'est à ce moment-là que nous voudrions migrer vers des clés statiques PQC.

Donc, le modèle de menace PQ le plus précoce est le stockage de trafic par OBEP/IBGW pour un déchiffrement ultérieur. Nous devrions implémenter le ratchet hybride en premier.

Ratchet est la priorité la plus élevée. Les transports sont les suivants. Les signatures sont la priorité la plus faible.

Le déploiement des signatures sera également reporté d'un an ou plus par rapport au déploiement du chiffrement, car aucune rétrocompatibilité n'est possible. De plus, l'adoption de MLDSA dans l'industrie sera standardisée par le CA/Browser Forum et les Autorités de Certification. Les CA ont d'abord besoin du support des modules de sécurité matériels (HSM), qui n'est actuellement pas disponible [CA/Browser Forum](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/). Nous nous attendons à ce que le CA/Browser Forum guide les décisions sur les choix de paramètres spécifiques, y compris s'il faut supporter ou exiger les signatures composites [IETF draft](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/).

| Milestone | Target |
|-----------|--------|
| Ratchet beta | Late 2025 |
| Select best enc type | Early 2026 |
| NTCP2 beta | Early 2026 |
| SSU2 beta | Mid 2026 |
| Ratchet production | Mid 2026 |
| Ratchet default | Late 2026 |
| Signature beta | Late 2026 |
| NTCP2 production | Late 2026 |
| SSU2 production | Early 2027 |
| Select best sig type | Early 2027 |
| NTCP2 default | Early 2027 |
| SSU2 default | Mid 2027 |
| Signature production | Mid 2027 |
## Migration

Si nous ne pouvons pas prendre en charge à la fois les anciens et nouveaux protocoles ratchet sur les mêmes tunnels, la migration sera beaucoup plus difficile.

Nous devrions pouvoir simplement essayer l'un puis l'autre, comme nous l'avons fait avec X25519, pour être prouvé.

## Issues

- Sélection du hash Noise - rester avec SHA256 ou faire une mise à niveau ?
  SHA256 devrait être valable encore 20-30 ans, pas menacé par PQ,
  Voir [NIST presentation](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf) et [NIST presentation](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf).
  Si SHA256 est cassé, nous avons de pires problèmes (netdb).
- NTCP2 port séparé, adresse router séparée
- SSU2 relay / test de pair
- SSU2 champ de version
- SSU2 version d'adresse router
