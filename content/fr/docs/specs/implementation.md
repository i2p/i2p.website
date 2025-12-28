---
title: "Guide d’exploitation des tunnels"
description: "Spécification unifiée pour la construction, le chiffrement et le transport du trafic avec des tunnels I2P."
slug: "implementation"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

> **Portée:** Ce guide regroupe l’implémentation du tunnel, le format des messages, ainsi que les deux spécifications de création de tunnel (ECIES et ElGamal ancien). Les liens profonds existants continuent de fonctionner via les alias ci-dessus.

## Modèle de Tunnel {#tunnel-model}

I2P achemine les charges utiles via *tunnels unidirectionnels*: des ensembles ordonnés de routers qui transportent le trafic dans une seule direction. Un aller-retour complet entre deux destinations nécessite quatre tunnels (deux sortants, deux entrants).

Commencez par le [Tunnel Overview](/docs/overview/tunnel-routing/) pour la terminologie, puis utilisez ce guide pour les détails opérationnels.

### Cycle de vie des messages {#message-lifecycle}

1. La **passerelle** du tunnel regroupe un ou plusieurs messages I2NP, les fragmente et écrit les instructions de livraison.
2. La **passerelle** encapsule la charge utile dans un message de tunnel de taille fixe (1024&nbsp;B), en ajoutant du bourrage si nécessaire.
3. Chaque **participant** vérifie le saut précédent, applique sa couche de chiffrement et transmet `{nextTunnelId, nextIV, encryptedPayload}` au saut suivant.
4. Le **point de terminaison** du tunnel retire la couche finale, lit et applique les instructions de livraison, réassemble les fragments et achemine les messages I2NP reconstruits.

La détection des doublons utilise un filtre de Bloom à vieillissement, dont la clé est dérivée de l’XOR du vecteur d’initialisation (IV) et du premier bloc chiffré, afin d’empêcher les attaques par marquage basées sur des échanges d’IV.

### Rôles en un coup d’œil {#roles}

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Role</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Pre-processing</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Crypto Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Post-processing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound gateway (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively <em>decrypt</em> using every hop’s keys (so downstream peers encrypt)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to first hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Participant</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt IV and payload with hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outbound endpoint</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt once more to reveal plaintext payload</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deliver to target tunnel/destination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound gateway</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fragment, batch, pad</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Encrypt with local keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Forward to next hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Inbound endpoint (creator)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Iteratively decrypt using stored hop keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reassemble and deliver locally</td>
    </tr>
  </tbody>
</table>
### Processus de chiffrement {#encryption-workflow}

- **Tunnels entrants:** la passerelle chiffre une fois avec sa clé de couche ; les participants en aval continuent à chiffrer jusqu’à ce que le créateur déchiffre la charge utile finale.
- **Tunnels sortants:** la passerelle préapplique l’inverse du chiffrement de chaque saut afin que chaque participant chiffre. Lorsque l’extrémité chiffre, le texte en clair d’origine de la passerelle est révélé.

Les deux directions acheminent `{tunnelId, IV, encryptedPayload}` vers le prochain saut.

---

## Format du message tunnel {#tunnel-message-format}

Les passerelles de tunnel fragmentent les messages I2NP en enveloppes de taille fixe afin de masquer la longueur de la charge utile et de simplifier le traitement à chaque saut.

### Structure chiffrée {#encrypted-layout}

```
+----------------+----------------+-------------------+
| Tunnel ID (4B) | IV (16B)       | Encrypted payload |
+----------------+----------------+-------------------+
```
- **Tunnel ID** – identifiant sur 32 bits pour le prochain saut (non nul, renouvelé à chaque cycle de construction).
- **IV** – IV AES de 16 octets choisi pour chaque message.
- **Charge utile chiffrée** – 1008 octets de texte chiffré AES-256-CBC.

Taille totale : 1028 octets.

### Structure déchiffrée {#decrypted-layout}

Après qu'un relais a retiré sa couche de chiffrement :

```
[Checksum (4B)][Padding ... 0x00 terminator]
[Delivery Instructions 1][I2NP fragment 1]
[Delivery Instructions 2][I2NP fragment 2]
...
```
- **Somme de contrôle** vérifie l’intégrité du bloc déchiffré.
- **Bourrage** consiste en des octets aléatoires non nuls, terminés par un octet nul.
- **Instructions de livraison** indiquent au point de terminaison comment traiter chaque fragment (livrer localement, transférer vers un autre tunnel, etc.).
- **Fragments** transport les messages I2NP sous-jacents; le point de terminaison les réassemble avant de les transmettre aux couches supérieures.

### Étapes de traitement {#processing-steps}

1. Les passerelles fragmentent et mettent en file d'attente les messages I2NP, en conservant brièvement les fragments partiels pour leur réassemblage.
2. La passerelle chiffre la charge utile avec les clés de couche appropriées et inscrit l'ID du tunnel ainsi que le vecteur d'initialisation (IV).
3. Chaque participant chiffre l'IV (AES-256/ECB) puis la charge utile (AES-256/CBC), avant de rechiffrer l'IV et de transmettre le message.
4. Le point de terminaison déchiffre dans l'ordre inverse, vérifie la somme de contrôle, traite les instructions de remise et réassemble les fragments.

---

## Création de tunnel (ECIES-X25519) {#tunnel-creation-ecies}

Les routers modernes construisent des tunnels avec des clés ECIES-X25519, réduisant la taille des messages de construction et permettant la confidentialité persistante.

- **Message de construction :** un seul message I2NP `TunnelBuild` (ou `VariableTunnelBuild`) transporte 1 à 8 enregistrements de construction chiffrés, un par saut.
- **Clés de couche :** les créateurs dérivent, pour chaque saut, les clés de couche, d’IV et de réponse via HKDF (fonction de dérivation de clé basée sur HMAC) en utilisant l’identité X25519 statique du saut et la clé éphémère du créateur.
- **Traitement :** chaque saut déchiffre son enregistrement, valide les indicateurs de requête, écrit le bloc de réponse (succès ou code d’échec détaillé), rechiffre les enregistrements restants et transmet le message.
- **Réponses :** le créateur reçoit un message de réponse encapsulé via garlic encryption. Les enregistrements marqués comme ayant échoué incluent un code de gravité afin que le router puisse profiler le pair.
- **Compatibilité :** les routers peuvent encore accepter des constructions ElGamal héritées pour la rétrocompatibilité, mais les nouveaux tunnels utilisent ECIES par défaut.

> Pour les constantes champ par champ et les notes sur la dérivation de clés, voir l'historique de la proposition ECIES et le code source du router ; ce guide couvre le déroulement opérationnel.

---

## Création de tunnel héritée (ElGamal-2048) {#tunnel-creation-elgamal}

Le format de construction de tunnel d’origine utilisait des clés publiques ElGamal. Les routers modernes conservent une prise en charge limitée pour la rétrocompatibilité.

> **Statut :** Obsolète. Conservé ici à titre de référence historique et pour toute personne assurant la maintenance d’outils compatibles avec les systèmes hérités.

- **Non-interactive telescoping (télescopage non interactif):** un seul message de construction parcourt l’intégralité du chemin. Chaque saut déchiffre son enregistrement de 528 octets, met à jour le message et le relaie.
- **Longueur variable:** le Variable Tunnel Build Message (VTBM) autorisait 1–8 enregistrements. Le message fixe antérieur contenait toujours huit enregistrements pour masquer la longueur du tunnel.
- **Structure de l’enregistrement de requête:**

```
Bytes 0–3    : Tunnel ID (receiving ID)
Bytes 4–35   : Current hop router hash
Bytes 36–39  : Next tunnel ID
Bytes 40–71  : Next hop router hash
Bytes 72–103 : AES-256 layer key
Bytes 104–135: AES-256 IV key
Bytes 136–167: AES-256 reply key
Bytes 168–183: AES-256 reply IV
Byte 184     : Flags (bit7=IBGW, bit6=OBEP)
Bytes 185–188: Request time (hours since epoch)
Bytes 189–192: Next message ID
Bytes 193–221: Padding
```
- **Drapeaux:** le bit 7 indique une passerelle entrante (IBGW); le bit 6 marque une extrémité sortante (OBEP). Ils sont mutuellement exclusifs.
- **Chiffrement:** chaque enregistrement est chiffré en ElGamal-2048 avec la clé publique du saut. Une superposition symétrique AES-256-CBC garantit que seul le saut visé peut lire son enregistrement.
- **Points clés:** les ID de tunnel sont des valeurs 32 bits non nulles; les créateurs peuvent insérer des enregistrements factices pour masquer la longueur réelle du tunnel; la fiabilité dépend du réessai des constructions échouées.

---

## Pools de tunnels et cycle de vie {#tunnel-pools}

Les routers maintiennent des pools de tunnels entrants et sortants indépendants pour le trafic exploratoire et pour chaque session I2CP.

- **Sélection des pairs :** les tunnels exploratoires puisent dans le groupe de pairs “actifs, non défaillants” afin de favoriser la diversité ; les tunnels clients privilégient des pairs rapides et à haute capacité.
- **Ordonnancement déterministe :** les pairs sont triés selon la distance XOR entre `SHA256(peerHash || poolKey)` et la clé aléatoire du pool (groupe de tunnels). La clé est renouvelée au redémarrage, apportant de la stabilité au sein d’une exécution tout en contrariant les attaques du prédécesseur d’une exécution à l’autre.
- **Cycle de vie :** les routers suivent les temps de construction historiques par tuple {mode, direction, longueur, variance}. À l’approche de l’expiration des tunnels, les remplacements commencent tôt ; le router augmente les constructions parallèles en cas d’échecs tout en plafonnant les tentatives en cours.
- **Paramètres de configuration :** nombres de tunnels actifs/de secours, longueur de saut et variance, autorisations zero-hop (0 saut) et limites de cadence de construction sont tous réglables pour chaque pool.

---

## Congestion et fiabilité {#congestion}

Bien que les tunnels ressemblent à des circuits, les routers les traitent comme des files d'attente de messages. L'élimination aléatoire anticipée pondérée (WRED) est utilisée pour maintenir la latence limitée:

- La probabilité de rejet augmente à mesure que l’utilisation se rapproche des limites configurées.
- Les participants considèrent des fragments de taille fixe ; les passerelles/points d’extrémité rejettent en fonction de la taille combinée des fragments, en pénalisant en priorité les charges utiles volumineuses.
- Les points d’extrémité sortants rejettent avant les autres rôles afin de gaspiller le moins possible de ressources réseau.

La remise garantie est laissée aux couches supérieures telles que la [bibliothèque de streaming](/docs/specs/streaming/). Les applications qui exigent de la fiabilité doivent prendre en charge elles-mêmes la retransmission et les accusés de réception.

---

## Pour aller plus loin {#further-reading}

- [Tunnels unidirectionnels (historique)](/docs/legacy/unidirectional-tunnels/)
- [Sélection des pairs](/docs/overview/tunnel-routing#peer-selection/)
- [Aperçu des Tunnels](/docs/overview/tunnel-routing/)
- [Ancienne implémentation des Tunnels](/docs/legacy/old-implementation/)
