---
title: "Extension rapide (BEP 6) : Fast autorisé avec identité de pair basée sur le hachage de la destination"
number: "172"
author: "dr|z3d"
created: "2026-08-10"
lastupdated: "2026-08-10"
status: "Brouillon"
toc: true
---

## Aperçu

Le BEP 6 (extension Fast) regroupe cinq fonctionnalités : **Have All / Have None**, **Reject Requests**, **Suggestions** et **Allowed Fast**. Le protocole réseau — bit de négociation, identifiants de message et sémantique de choke — est indépendant du transport et fonctionne tel quel sur le streaming I2P. La seule partie du BEP 6 qui ne peut pas être directement transposée à I2P est la **génération de l'ensemble Allowed Fast**, car elle est définie en fonction de l'adresse IPv4 du pair. Les pairs I2P n'ont pas d'adresses IP ; ils sont identifiés par des hachages de destination de 32 octets.

Cette proposition standardise la génération d'un ensemble « Allowed Fast » natif I2P, de sorte que tous les clients torrent I2P génèrent des ensembles allowed fast *identiques* pour un même pair et un même torrent, rendant cette fonctionnalité utile (et vérifiable) à travers différentes implémentations.

## Motivation

Les nouveaux pairs ont besoin des premiers morceaux avant que le système « donne pour donne » du BitTorrent ne puisse s'accélérer. Sur I2P, cette accélération est plus lente que sur le réseau clair : la configuration de la connexion et la livraison des morceaux traversent plusieurs sauts par des tunnels à forte latence, ce qui allonge la fenêtre entre la connexion et le premier déblocage réciproque. Allowed Fast attaque directement cette fenêtre — un pair en démarrage se voit autoriser un petit nombre de morceaux même lorsqu'il est bloqué, reçoit immédiatement des données, et peut commencer à échanger plus tôt.

Le BEP 6 de référence calcule l'ensemble rapide autorisé à partir de l'adresse IPv4 du pair afin de garantir que l'*expéditeur* puisse sélectionner des morceaux uniques pour le *destinataire* (un utilisateur disposant de plusieurs adresses IP ne peut pas récolter de nombreux ensembles). Sur I2P, le hachage de destination du pair remplit le même rôle de liaison et est accessible aux deux extrémités de chaque connexion, ce qui rend l'ensemble déterministe et *vérifiable localement* — une caractéristique que le schéma basé sur l'IP ne peut pas offrir.

## Modifications apportées à la BEP 6

La négociation de l'extension Fast et les quatre types de messages sont adoptés sans changement :

- Négociation : troisième bit le moins significatif du dernier octet réservé, `reserved[7] |= 0x04`, des deux côtés  
- Have All `<len=0x0001><op=0x0E>`, Have None `<len=0x0001><op=0x0F>`  
- Suggest Piece `<len=0x0005><op=0x0D><index>`  
- Reject Request `<len=0x000D><op=0x10><index><begin><length>`  
- Allowed Fast `<len=0x0005><op=0x11><index>`  
- Chaque requête entraîne exactement une réponse (pièce ou rejet) ; le blocage (choke) n'entraîne plus implicitement le rejet des requêtes en attente

La seule différence réside dans la génération de l'ensemble Allowed Fast, où les octets de l'adresse IP sont remplacés par les octets du hachage de destination du pair.

### Dérivation : hacher les octets au lieu de l'IP masquée

Référence BEP 6, étape (1) :

```
x = 0xFFFFFF00 & ip
```
Cela prend trois octets de l'adresse IPv4 du pair et **met le 4e octet à zéro**. Il s'agit d'une heuristique de sous-réseau : les utilisateurs qui peuvent obtenir plusieurs adresses IP sur le même /24 ne devraient pas obtenir plusieurs ensembles rapides autorisés.

Notre version d'I2P remplace cela par les quatre premiers octets du hachage de destination de 32 octets du pair :

```
x = first 4 bytes of peer destination hash
```
La distinction par rapport à l'implémentation de référence :

« Ce sont les 3 octets de l'IP suivis par un zéro. Vous êtes les 4 octets du hachage. C'est différent de BEP 6 parce qu'il n'y a pas d'IP et on ne met pas à zéro le 4e octet. »

Les deux extrémités d'une connexion I2P connaissent déjà le hachage de destination du pair (il s'agit de l'adresse à laquelle la connexion a été établie), ce qui ne nécessite aucun échange supplémentaire, aucune découverte NAT, ni détection d'IP externe — aucun de ces mécanismes n'existant sur I2P.

### Algorithme de génération rapide autorisé

Soit `hash` le hachage de destination de 32 octets du pair destinataire, `infohash` le hachage d'information du torrent de 20 octets, `sz` le nombre de morceaux dans le torrent, `k` le nombre final de morceaux dans l'ensemble autorisé rapide (10, comme dans BEP 6), et `a` l'ensemble de sortie :

```
x = hash[0:4]  ++  infohash        (1)
while |a| < k:
    x = SHA1(x)                    (2)
    for i in [0:5] and |a| < k:    (3)
        y = x[i*4 : i*4+4]         (4)
        index = y % sz             (5)
        if index not in a:         (6)
            add index to a         (7)
```
Notes :

- 4 octets du hachage de destination remplacent les 3 octets IP masqués. Les quatre octets transportent de l'entropie de hachage ; aucun n'est mis à zéro.
- Comme dans BEP 6, la chaîne SHA1 produit une longue séquence pseudo-aléatoire, divisée en indices de morceaux ; `k = 10` correspond à la valeur par défaut de référence.
- Le message Allowed Fast est indicatif : le destinataire NE DOIT PAS l'interpréter comme signifiant que l'expéditeur possède le morceau — seulement que l'expéditeur fournira ce morceau même s'il est étouffé.

## Avantages

| Domaine             | Avantage                                                                                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latence au démarrage | Les nouveaux pairs téléchargent les premiers morceaux même lorsqu'ils sont étouffés, réduisant ainsi la phase initiale d'échange progressif, plus lente via les tunnels I2P multi-sauts                                                                 |
| Déterminisme         | L'ensemble est une fonction pure du hachage de destination + infohash, donc toute implémentation calcule le même ensemble — contrairement au BEP 6 basé sur IP, où la vision que l'expéditeur a de l'IP du destinataire peut différer (NAT) |
| Vérifiabilité        | Le pair récepteur connaît son propre hachage de destination et peut recalculer localement et valider l'ensemble, détectant ainsi les expéditeurs malhonnêtes                                                               |
| Pas de mécanisme IP  | Pas de traversée NAT, pas de découverte d'IP externe, ni d'heuristiques de sous-réseau — tout cela étant impossible ou dénué de sens sur I2P                                                                             |
| Lien d'identité      | Un seul ensemble rapide autorisé par destination. Un utilisateur possédant plusieurs destinations obtient un ensemble par destination — conservant ainsi la même propriété anti-triche que fournissait le masque IP sur le clairnet                                        |
| Confidentialité      | Aucune adresse IP n'est jamais transmise ni implicite dans le calcul                                                                                                                               |
| Bande passante       | « Avoir Tout » / « Avoir Rien » remplace le bitfield complet pour les gros torrents ; « Rejeter » supprime les demandes redondantes                                                                                       |
## Considérations relatives à la mise en œuvre

- **Identité du pair** : le hachage de destination du pair est obtenu à partir de la connexion de flux (la destination de la session), et correspond à la même valeur utilisée par les deux extrémités. Pour les connexions sortantes, utilisez la destination à laquelle vous vous êtes connecté ; pour les connexions entrantes, utilisez la destination d’où provient la connexion.
- **Négociation** : envoyez `reserved[7] |= 0x04` dans l’échange initial (handshake) ; n’envoyez des messages Fast Extension que si le handshake du pair a également activé ce bit ; si un pair envoie des messages Fast Extension sans négociation préalable, fermez la connexion.
- **Have All / Have None** : envoyez exactement un seul message parmi bitfield / Have All / Have None immédiatement après le handshake. Utilisez Have All pour les seeders, Have None jusqu’à obtention du premier morceau.
- **Côté émetteur Allowed Fast** : annoncez uniquement les morceaux que vous possédez réellement ; le destinataire peut les demander même s’il est étouffé (choked). Limitez l'ensemble *servi* (par exemple, rejetez les demandes allowed-fast provenant d’un pair qui détient déjà plus de `k` morceaux, conformément aux recommandations de la BEP 6).
- **Côté récepteur Allowed Fast** : stockez l’ensemble reçu ; autorisez les demandes de ces morceaux même en état d’étouffement (choked) ; éventuellement, vérifiez cet ensemble en le recalculant à partir de votre propre hachage de destination et de l’infohash, et ignorez les morceaux absents de l’ensemble recalculé.
- **Reject** : chaque demande doit recevoir exactement une réponse ; en cas d’étouffement (choke), rejetez toutes les demandes qui ne font pas partie de l’ensemble allowed fast, au lieu de simplement ignorer silencieusement le pair.
- **Taille de l’ensemble** : utilisez `k = 10` pour assurer la compatibilité ; les pairs peuvent choisir une valeur inférieure sous charge, mais les deux extrémités ne doivent annoncer que ce qu’elles sont effectivement prêtes à fournir.
- **Limite des morceaux** : `index = y % sz` doit utiliser le nombre total de morceaux du torrent `sz` ; ignorez les indices ≥ sz (mesure défensive), car une chaîne de hachage n’est pas limitée par plage de morceaux.
- **Compatibilité ascendante** : les clients qui ne négocient pas le bit fast n’auront tout simplement jamais connaissance de ces messages ; aucune autre modification du protocole n’est nécessaire.

## Implémentations de référence

L'algorithme est petit et autonome — une dizaine de lignes dans n'importe quel langage. Les trois exemples ci-dessous calculent le même ensemble pour des entrées identiques (`hash[0:4] ++ infohash`, chaîne SHA1, `y % sz`, avec `k = 10` comme limite).

### Java

```java
// I2P: peer.getPeerID().getDestHash() is the 32-byte destination hash.
// Big-endian word reads build each candidate piece index from the SHA1 chain.
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

public static Set<Integer> generateAllowedFastSet(byte[] destHash, byte[] infohash, int pieces) {
    Set<Integer> rv = new HashSet<>(10);
    if (destHash == null || infohash == null || pieces <= 0) {
        return rv;
    }
    byte[] x = new byte[24];
    System.arraycopy(destHash, 0, x, 0, 4);          // 4 hash bytes, no IP, no zeroed 4th byte
    System.arraycopy(infohash, 0, x, 4, Math.min(20, infohash.length));
    MessageDigest md = MessageDigest.getInstance("SHA-1");
    while (rv.size() < 10) {
        x = md.digest(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            long y = ((x[i * 4] & 0xFFL) << 24) | ((x[i * 4 + 1] & 0xFFL) << 16)
                   | ((x[i * 4 + 2] & 0xFFL) << 8) | (x[i * 4 + 3] & 0xFFL);
            rv.add((int) (y % pieces));
        }
    }
    return rv;
}
```
### C++

```cpp
// Peer identity input is the 32-byte destination hash available on the connection.
#include <cstdint>
#include <set>
#include <vector>

extern std::vector<uint8_t> sha1(const std::vector<uint8_t>& in); // e.g. OpenSSL SHA1()

std::set<int> generate_allowed_fast_set(const std::vector<uint8_t>& dest_hash,
                                        const std::vector<uint8_t>& infohash,
                                        int pieces) {
    std::set<int> rv;
    if (dest_hash.size() < 4 || infohash.size() < 20 || pieces <= 0) { return rv; }
    std::vector<uint8_t> x(dest_hash.begin(), dest_hash.begin() + 4); // 4 hash bytes,
                                                                      // no IP mask
    x.insert(x.end(), infohash.begin(), infohash.begin() + 20);
    while (rv.size() < 10) {
        x = sha1(x);
        for (int i = 0; i < 5 && rv.size() < 10; i++) {
            uint32_t y = (uint32_t(x[i * 4]) << 24) | (uint32_t(x[i * 4 + 1]) << 16) |
                         (uint32_t(x[i * 4 + 2]) << 8) | uint32_t(x[i * 4 + 3]);
            rv.insert(int(y % uint32_t(pieces)));
        }
    }
    return rv;
}
```
### Python

```python
import hashlib

def generate_allowed_fast_set(dest_hash: bytes, infohash: bytes, pieces: int) -> set:
    """4 bytes of the destination hash stand in for the masked IP; no byte is zeroed."""
    rv = set()
    if len(dest_hash) < 4 or len(infohash) < 20 or pieces <= 0:
        return rv
    x = dest_hash[:4] + infohash[:20]
    while len(rv) < 10:
        x = hashlib.sha1(x).digest()
        for i in range(5):
            if len(rv) >= 10:
                break
            y = int.from_bytes(x[i * 4 : i * 4 + 4], "big")
            rv.add(y % pieces)
    return rv
```
## Compatibilité

- **Compatible au niveau du protocole** : le bit de négociation et les formats de message sont strictement identiques en octets au BEP 6 du réseau clair ; seule l'entrée pour la génération du jeu diffère.
- **Non-interopérable entre réseaux** : un client I2P et un client du réseau clair ne peuvent de toute façon pas se connecter entre eux ; l'écart affecte uniquement les octets d'identité des pairs, jamais le format du protocole.
- **Au sein d'I2P** : tout client implémentant cette proposition calcule des ensembles rapides autorisés identiques et peut les servir et les vérifier indifféremment. Les clients qui ignorent Allowed Fast le considèrent simplement comme une recommandation sans effet et ne perdent que l'avantage au démarrage.

## Questions ouvertes

1. La taille de l'ensemble `k` doit-elle rester fixe à 10, ou s'adapter à la charge (par exemple, plus petite sous une forte charge de requêtes), comme le permet BEP 6 ?
2. Les destinataires doivent-ils vérifier que l'ensemble correspond au hachage de leur propre destination et rejeter les indices incohérents (protection contre des émetteurs bogués ou malveillants) ? Recommandé : oui.
3. Faut-il choisir le *préfixe* de 4 octets (octets 0-3) comme indiqué, ou bien les 4 derniers octets — n'importe quelle fenêtre fixe de 4 octets offre les mêmes propriétés ; le préfixe conserve l'ordre naturel des octets dans le code de référence (`hash[0:4]`).

## État de la technique

- Référence : [Extension rapide BEP 6](https://www.bittorrent.org/beps/bep_0006.html)
- Implémentation de référence dans I2PSnark : `PeerState.sendAllowedFast()` / `generateAllowedFastSet()` dans `apps/i2psnark/java/src/org/klomp/snark/PeerState.java` (@depuis 0.9.71+)
- Fonctionne conjointement avec la BEP 40 (priorité canonique des pairs) et la BEP 21 (partiels seeds), toutes deux prises en charge par I2PSnark
