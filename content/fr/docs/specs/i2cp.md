---
title: "Protocole client I2P (I2CP)"
description: "Comment les applications négocient des sessions, des tunnels et des LeaseSets avec le router I2P."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Vue d'ensemble

I2CP est le protocole de contrôle de bas niveau entre un router I2P et tout processus client. Il définit une séparation stricte des responsabilités :

- **Router**: Gère le routage, la cryptographie, les cycles de vie des tunnels et les opérations de la base de données du réseau
- **Client**: Sélectionne les propriétés d'anonymat, configure des tunnels et envoie/reçoit des messages

Toutes les communications transitent par une seule socket TCP (éventuellement encapsulée dans TLS), ce qui permet des opérations asynchrones en duplex intégral.

**Version du protocole**: I2CP utilise un octet de version de protocole `0x2A` (42 décimal) envoyé lors de l'établissement initial de la connexion. Cet octet de version est resté stable depuis la création du protocole.

**Statut actuel**: Cette spécification est valable pour la version 0.9.67 du router (version d'API 0.9.67), publiée en 2025-09.

## Contexte d'implémentation

### Implémentation Java

L’implémentation de référence est en Java I2P: - SDK client: `i2p.jar` package - Implémentation du Router: `router.jar` package - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Lorsque le client et le router s’exécutent dans la même JVM, les messages I2CP sont transmis sous forme d’objets Java sans sérialisation. Les clients externes utilisent le protocole sérialisé via TCP.

### Implémentation C++

i2pd (le router I2P en C++) implémente également I2CP en externe pour les connexions client.

### Clients non-Java

Il n'existe **aucune implémentation non-Java connue** d'une bibliothèque cliente I2CP complète. Les applications non-Java devraient plutôt utiliser des protocoles de plus haut niveau :

- **SAM (Simple Anonymous Messaging) v3**: Interface basée sur des sockets avec des bibliothèques disponibles dans plusieurs langages
- **BOB (Basic Open Bridge)**: Alternative plus simple à SAM

Ces protocoles de niveau supérieur gèrent en interne la complexité d'I2CP et fournissent également la bibliothèque de streaming (pour des connexions de type TCP) et la bibliothèque de datagrammes (pour des connexions de type UDP).

## Établissement de la connexion

### 1. Connexion TCP

Connectez-vous au port I2CP du router : - Par défaut : `127.0.0.1:7654` - Configurable via les paramètres du router - Enveloppe TLS optionnelle (fortement recommandée pour les connexions à distance)

### 2. Négociation du protocole

**Étape 1**: Envoyez l'octet de version du protocole `0x2A`

**Étape 2**: Synchronisation de l'horloge

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
Le router renvoie son horodatage actuel et la chaîne de version de l’API I2CP (depuis la version 0.8.7).

**Étape 3**: Authentification (si activée)

À partir de la version 0.9.11, l’authentification peut être incluse dans GetDateMessage via un Mapping contenant: - `i2cp.username` - `i2cp.password`

À partir de la version 0.9.16, lorsque l’authentification est activée, elle **doit** être effectuée via GetDateMessage avant l’envoi de tout autre message.

**Étape 4**: Création de la session

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Étape 5**: Signal de disponibilité du Tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
Ce message indique que des tunnels entrants ont été établis. Le router n’enverra PAS ce message tant qu’au moins un tunnel entrant ET un tunnel sortant n’existent pas.

**Étape 6**: Publication du LeaseSet

```
Client → Router: CreateLeaseSet2Message
```
À ce stade, la session est entièrement opérationnelle pour l’envoi et la réception de messages.

## Modèles de flux de messages

### Message sortante (Le client envoie vers une destination distante)

**Avec i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Avec i2cp.messageReliability=BestEffort**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Message entrant (le Router le remet au client)

**Avec i2cp.fastReceive=true** (valeur par défaut depuis la version 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Avec i2cp.fastReceive=false** (DÉPRÉCIÉ):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Les clients modernes devraient toujours utiliser le mode de réception rapide.

## Structures de données courantes

### En-tête de message I2CP

Tous les messages I2CP utilisent cet en-tête commun:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Longueur du corps** : entier sur 4 octets, longueur du corps du message uniquement (exclut l'en-tête)
- **Type** : entier sur 1 octet, identifiant du type de message
- **Corps du message** : 0+ octets, le format varie selon le type de message

**Taille maximale du message**: Environ 64 Ko maximum.

### ID de session

Entier sur 2 octets identifiant de manière unique une session sur un router.

**Valeur spéciale** : `0xFFFF` indique "aucune session" (utilisée pour les résolutions de noms d’hôte sans session établie).

### ID du message

Entier sur 4 octets généré par le router pour identifier de manière unique un message au sein d'une session.

**Important** : Les IDs de message ne sont **pas** uniques globalement, uniquement au sein d'une session. Ils sont également distincts du nonce (nombre utilisé une seule fois) généré par le client.

### Format de la charge utile

Les charges utiles des messages sont compressées avec gzip avec un en-tête gzip standard de 10 octets : - Commence par : `0x1F 0x8B 0x08` (RFC 1952) - Depuis 0.7.1 : Les parties inutilisées de l'en-tête gzip contiennent des informations de protocole, from-port et to-port - Cela permet le streaming et les datagrammes sur la même destination

**Contrôle de la compression** : Définissez `i2cp.gzip=false` pour désactiver la compression (définit l'effort de gzip à 0). L'en-tête gzip est toujours inclus, mais avec un surcoût de compression minimal.

### Structure de SessionConfig

Définit la configuration pour une session client :

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Exigences critiques**: 1. **Le mappage doit être trié par clé** pour la validation de la signature 2. **Date de création** doit se situer dans un intervalle de ±30 secondes par rapport à l'heure actuelle du router 3. **Signature** est créée par la SigningPrivateKey (clé privée de signature) de la Destination

**Signatures hors ligne** (à partir de la 0.9.38):

Si vous utilisez la signature hors ligne, le mappage doit contenir : - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

La Signature est ensuite générée par la SigningPrivateKey (clé privée de signature) éphémère.

## Options de configuration du cœur

### Configuration du tunnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Remarques**: - Des valeurs de `quantity` > 6 nécessitent des pairs exécutant la version 0.9.0 ou supérieure et augmentent considérablement l'utilisation des ressources - Réglez `backupQuantity` sur 1-2 pour des services à haute disponibilité - Les tunnels à zéro saut sacrifient l'anonymat au profit de la latence, mais sont utiles pour les tests

### Gestion des messages

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Fiabilité des messages**: - `None`: Aucun accusé de réception du router (paramètre par défaut de la bibliothèque de streaming depuis la version 0.8.1) - `BestEffort`: Le router envoie l’acceptation + des notifications de réussite/échec - `Guaranteed`: Non implémenté (se comporte actuellement comme BestEffort)

**Dérogation par message** (depuis la version 0.9.14): - Dans une session avec `messageReliability=none`, définir un nonce non nul (nombre à usage unique) demande une notification de livraison pour ce message spécifique - Définir nonce=0 dans une session `BestEffort` désactive les notifications pour ce message

### Configuration du LeaseSet (annonce de service I2P)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Anciennes étiquettes de session ElGamal/AES

Ces options ne concernent que l'ancien chiffrement ElGamal:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Remarque**: Les clients ECIES-X25519 utilisent un mécanisme de ratchet (mécanisme à cliquet) différent et ignorent ces options.

## Types de chiffrement

I2CP prend en charge plusieurs schémas de chiffrement de bout en bout via l’option `i2cp.leaseSetEncType`. Plusieurs types peuvent être spécifiés (séparés par des virgules) afin de prendre en charge à la fois les pairs modernes et anciens.

### Types de chiffrement pris en charge

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Configuration recommandée**:

```
i2cp.leaseSetEncType=4,0
```
Cela fournit X25519 (préféré) avec une solution de repli ElGamal pour la compatibilité.

### Détails du type de chiffrement

**Type 0 - ElGamal/AES+SessionTags (schéma ElGamal/AES avec étiquettes de session)**: - clés publiques ElGamal 2048 bits (256 octets) - chiffrement symétrique AES-256 - étiquettes de session de 32 octets envoyées par lots - surcharge élevée en CPU, bande passante et mémoire - en cours de retrait progressif à l’échelle du réseau

**Type 4 - ECIES-X25519-AEAD-Ratchet**: - Échange de clés X25519 (clés de 32 octets) - ChaCha20/Poly1305 AEAD - Double ratchet de style Signal (algorithme à double cliquet) - Étiquettes de session de 8 octets (contre 32 octets pour ElGamal) - Étiquettes générées via un PRNG synchronisé (non envoyées à l'avance) - Réduction de ~92 % du surcoût par rapport à ElGamal - Standard pour l'I2P moderne (la plupart des routers l'utilisent)

**Types 5-6 - Hybride post-quantique**: - Combine X25519 avec ML-KEM (NIST FIPS 203) - Fournit une sécurité résistante aux attaques quantiques - ML-KEM-768 pour un équilibre sécurité/performances - ML-KEM-1024 pour une sécurité maximale - Tailles de messages plus grandes en raison du PQ key material (matériel de clé post-quantique) - La prise en charge réseau est encore en cours de déploiement

### Stratégie de migration

Le réseau I2P migre activement d'ElGamal (type 0) vers X25519 (type 4): - NTCP → NTCP2 (terminé) - SSU → SSU2 (terminé) - ElGamal tunnels → X25519 tunnels (terminé) - ElGamal de bout en bout → ECIES-X25519 (majoritairement terminé)

## LeaseSet2 et fonctionnalités avancées

### Options de LeaseSet2 (depuis la version 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Adresses aveuglées

À partir de la 0.9.39, les destinations peuvent utiliser des adresses "blinded" (masquées) (format b33) qui changent périodiquement: - Nécessite `i2cp.leaseSetSecret` pour la protection par mot de passe - Authentification optionnelle par client - Voir les propositions 123 et 149 pour plus de détails

### Enregistrements de service (depuis 0.9.66)

LeaseSet2 prend en charge des options pour les enregistrements de service (proposition 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Le format suit le style des enregistrements SRV DNS, mais il est adapté à I2P.

## Sessions multiples (depuis 0.9.21)

Une seule connexion I2CP peut maintenir plusieurs sessions :

**Session principale**: La première session créée sur une connexion **Sous-sessions**: Sessions supplémentaires partageant le pool de tunnel de la session principale

### Caractéristiques des sous-sessions

1. **Tunnels partagés**: Utiliser les mêmes pools de tunnel entrants/sortants que la session principale
2. **Clés de chiffrement partagées**: Doit utiliser des clés de chiffrement LeaseSet identiques
3. **Clés de signature différentes**: Doit utiliser des clés de signature de Destination distinctes
4. **Aucune garantie d’anonymat**: Clairement lié à la session principale (même router, mêmes tunnels)

### Cas d'utilisation d'une sous-session

Activer la communication avec des destinations utilisant différents types de signature : - Principale : signature EdDSA (moderne) - Sous-session : signature DSA (compatibilité héritée)

### Cycle de vie d’une sous-session

**Création**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Destruction**: - Détruire une sous-session : laisse la session principale intacte - Détruire la session principale : détruit toutes les sous-sessions et ferme la connexion - DisconnectMessage (message de déconnexion) : détruit toutes les sessions

### Gestion de l'ID de session

La plupart des messages I2CP contiennent un champ d'ID de session. Exceptions: - DestLookup / DestReply (dépréciés, utilisez HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (réponse non spécifique à la session)

**Important** : Les clients ne doivent pas avoir plusieurs messages CreateSession en attente simultanément, car les réponses ne peuvent pas être corrélées sans ambiguïté aux requêtes.

## Catalogue de messages

### Résumé des types de messages

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Légende**: C = Client, R = Router

### Détails du message clé

#### CreateSessionMessage (Type 1)

**Objectif**: Initier une nouvelle session I2CP

**Contenu**: structure SessionConfig

**Réponse**: SessionStatusMessage (status=Created ou Invalid)

**Exigences**: - La date dans SessionConfig doit être dans une fenêtre de ±30 secondes par rapport à l’horloge du router - Le mapping doit être trié par clé pour la validation de la signature - Destination ne doit pas déjà avoir une session active

#### RequestVariableLeaseSetMessage (Type 37)

**Objectif**: Le Router demande l'autorisation du client pour les tunnels entrants

**Contenu**: - ID de session - Nombre de leases (jetons de routage temporaires) - Tableau de structures Lease (chacune avec sa propre expiration)

**Réponse**: CreateLeaseSet2Message

**Importance**: C’est le signal indiquant que la session est opérationnelle. Le router l’envoie uniquement après: 1. Au moins un tunnel entrant est établi 2. Au moins un tunnel sortant est établi

**Recommandation de délai d’expiration**: Les clients doivent détruire la session si ce message n’est pas reçu dans un délai de 5 minutes ou plus après la création de la session.

#### CreateLeaseSet2Message (Type 41)

**Objectif**: Le client publie le LeaseSet dans la base de données du réseau

**Contenu**: - ID de session - Octet de type LeaseSet (1, 3, 5 ou 7) - LeaseSet ou LeaseSet2 ou EncryptedLeaseSet ou MetaLeaseSet - Nombre de clés privées - Liste des clés privées (une par clé publique dans le LeaseSet, même ordre)

**Clés privées**: Nécessaires pour déchiffrer les garlic messages entrants (messages « garlic » d’I2P). Format:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Remarque**: Remplace le CreateLeaseSetMessage obsolète (type 4), qui ne prend pas en charge :
- Variantes de LeaseSet2
- Chiffrement non-ElGamal
- Plusieurs types de chiffrement
- LeaseSets chiffrés
- Clés de signature hors ligne

#### SendMessageExpiresMessage (Type 36)

**Objectif**: Envoyer un message vers une destination avec expiration et options avancées

**Contenu**: - ID de session - Destination - Charge utile (compressée en gzip) - Nonce (4 octets) - Indicateurs (2 octets) - voir ci-dessous - Date d'expiration (6 octets, tronquée depuis 8)

**Champ des drapeaux** (2 octets, ordre des bits 15...0) :

**Bits 15-11**: Non utilisés, doivent être à 0

**Bits 10-9**: Forçage de la fiabilité des messages (inutilisé ; utiliser plutôt un nonce, valeur unique à usage unique)

**Bit 8**: Ne pas inclure le LeaseSet - 0: Le Router peut inclure le LeaseSet dans un message garlic (mécanisme d'agrégation de messages d'I2P) - 1: Ne pas inclure le LeaseSet

**Bits 7-4**: Seuil bas de tags (ElGamal uniquement, ignoré pour ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bits 3-0**: Étiquettes à envoyer si nécessaire (ElGamal uniquement, ignorées pour ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Type 22)

**Objectif**: Notifier le client du statut de livraison du message

**Contenu**: - ID de session - ID de message (généré par le router) - Code d'état (1 octet) - Taille (4 octets, pertinent uniquement si status=0) - Nonce (valeur unique utilisée une seule fois) (4 octets, correspond au nonce de SendMessage du client)

**Codes d'état** (Messages sortants):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Codes de réussite**: 1, 2, 4, 6 **Codes d'échec**: Tous les autres

**Code d’état 0** (OBSOLÈTE): Message disponible (entrant, réception rapide désactivée)

#### HostLookupMessage (Type 38)

**Objectif**: Rechercher la destination par nom d'hôte ou par hachage (remplace DestLookup)

**Contenu**: - ID de session (ou 0xFFFF s'il n'y a pas de session) - ID de requête (4 octets) - Délai d'attente en millisecondes (4 octets, minimum recommandé: 10000) - Type de requête (1 octet) - Clé de recherche (hachage, chaîne de nom d'hôte, ou Destination)

**Types de requêtes**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Les types 2 à 4 renvoient les options de LeaseSet (proposition 167) si elles sont disponibles.

**Réponse**: HostReplyMessage

#### HostReplyMessage (message de réponse d’hôte) (Type 39)

**Objectif**: Réponse à HostLookupMessage (message de résolution de nom d’hôte)

**Contenu**: - ID de session - ID de requête - Code de résultat (1 octet) - Destination (présente en cas de réussite, parfois en cas d'échecs spécifiques) - Mappage (uniquement pour les types de recherche 2-4, peut être vide)

**Codes de résultat**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (Type 42)

**Objectif**: Informer le router des exigences d’authentification concernant les destinations aveuglées (depuis la version 0.9.43)

**Contenu**: - ID de session - Indicateurs (1 octet) - Type de point de terminaison (1 octet): 0=Hash, 1=nom d'hôte, 2=Destination, 3=SigType+Key - Type de signature aveuglée (2 octets) - Expiration (4 octets, secondes depuis l'époque Unix) - Données du point de terminaison (varient selon le type) - Clé privée (32 octets, uniquement si le bit d'indicateur 0 est activé) - Mot de passe de recherche (Chaîne, uniquement si le bit d'indicateur 4 est activé)

**Indicateurs** (ordre des bits 76543210):

- **Bit 0**: 0=tout le monde, 1=par client
- **Bits 3-1**: Schéma d'authentification (si le bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=secret requis
- **Bits 7-5**: Non utilisés, fixés à 0

**Aucune réponse**: Le Router traite silencieusement

**Cas d'utilisation** : Avant d'envoyer vers une blinded destination (b33 address, destination aveuglée), le client doit soit : 1. Rechercher l'adresse b33 via HostLookup (recherche d'hôte), OU 2. Envoyer un BlindingInfo message (message d'information d'aveuglement)

Si la destination nécessite une authentification, BlindingInfo (informations d'aveuglement) est obligatoire.

#### ReconfigureSessionMessage (Type 2)

**Objectif**: Mettre à jour la configuration de la session après la création

**Contenu**: - Session ID - SessionConfig (seules les options modifiées sont nécessaires)

**Réponse**: SessionStatusMessage (status=Updated ou Invalid)

**Remarques**: - Router fusionne la nouvelle configuration avec la configuration existante - Les options de tunnel (`inbound.*`, `outbound.*`) sont toujours appliquées - Certaines options peuvent être immuables après la création de la session - La date doit être à ±30 secondes de l'heure du router - Le mappage doit être trié par clé

#### DestroySessionMessage (message de destruction de session) (Type 3)

**Objectif**: Terminer une session

**Contenu**: ID de session

**Réponse attendue**: SessionStatusMessage (status=Destroyed)

**Comportement actuel** (Java I2P jusqu'à la 0.9.66): - Router n'envoie jamais SessionStatus(Destroyed) - S'il ne reste aucune session : envoie DisconnectMessage - S'il reste des sous-sessions : aucune réponse

**Important**: Le comportement de Java I2P s'écarte de la spécification. Les implémentations devraient faire preuve de prudence lors de la destruction de sous-sessions individuelles.

#### DisconnectMessage (message de déconnexion) (Type 30)

**Objectif**: Indiquer que la connexion est sur le point d'être fermée

**Contenu**: Motif (chaîne de caractères)

**Effet**: Toutes les sessions de la connexion sont détruites, le socket se ferme

**Implémentation**: Principalement router → client dans Java I2P

## Historique des versions du protocole

### Détection de version

La version du protocole I2CP est échangée dans les messages Get/SetDate (depuis la 0.8.7). Pour les routers plus anciens, les informations de version ne sont pas disponibles.

**Chaîne de version**: Indique la version de l'API "core", pas nécessairement la version du router.

### Chronologie des fonctionnalités

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Considérations de sécurité

### Authentification

**Par défaut**: Aucune authentification requise **Facultatif**: Authentification par nom d'utilisateur/mot de passe (depuis 0.9.11) **Obligatoire**: Lorsque cette option est activée, l'authentification doit se terminer avant les autres messages (depuis 0.9.16)

**Connexions distantes** : Utilisez toujours TLS (`i2cp.SSL=true`) pour protéger les identifiants et les clés privées.

### Décalage de l'horloge

SessionConfig Date doit être à ±30 secondes de l’heure du router, sinon la session sera rejetée. Utilisez Get/SetDate pour synchroniser.

### Gestion des clés privées

CreateLeaseSet2Message (message CreateLeaseSet2, type de message I2P) contient des clés privées pour déchiffrer les messages entrants. Ces clés doivent être : - Transmises de manière sécurisée (TLS pour les connexions distantes) - Stockées de manière sécurisée par le router - Renouvelées en cas de compromission

### Expiration des messages

Utilisez toujours SendMessageExpires (et non SendMessage) pour définir une expiration explicite. Ceci : - Empêche que les messages restent en file d’attente indéfiniment - Réduit la consommation de ressources - Améliore la fiabilité

### Gestion des tags de session

**ElGamal** (déprécié): - Les tags doivent être transmis par lots - La perte de tags entraîne des échecs de déchiffrement - Surcoût mémoire élevé

**ECIES-X25519** (actuel): - Étiquettes générées via un PRNG synchronisé - Aucune transmission préalable nécessaire - Résistant à la perte de messages - Surcharge nettement plus faible

## Bonnes pratiques

### Pour les développeurs de clients

1. **Utilisez le mode de réception rapide**: Définissez toujours `i2cp.fastReceive=true` (ou laissez la valeur par défaut)

2. **Privilégiez ECIES-X25519**: Configurez `i2cp.leaseSetEncType=4,0` pour des performances optimales tout en préservant la compatibilité

3. **Définissez une expiration explicite**: Utilisez SendMessageExpires, pas SendMessage

4. **Manipulez les sous-sessions avec précaution**: Sachez que les sous-sessions n'offrent aucun anonymat entre destinations

5. **Expiration de la création de session**: Détruire la session si RequestVariableLeaseSet n'est pas reçu dans les 5 minutes

6. **Trier les mappages de configuration**: Toujours trier les clés de mappage avant de signer SessionConfig

7. **Utilisez des nombres de tunnel appropriés**: Ne définissez pas `quantity` à plus de 6 sauf si nécessaire

8. **Envisagez SAM/BOB pour les langages non Java**: Implémentez SAM plutôt qu’I2CP directement

### Pour les développeurs du Router

1. **Valider les dates** : Appliquer une tolérance de ±30 secondes sur les dates de SessionConfig

2. **Limiter la taille des messages**: Imposer une taille de message maximale de ~64 KB

3. **Prise en charge de plusieurs sessions** : Implémenter la prise en charge des sous-sessions conformément à la spécification 0.9.21

4. **Envoyez RequestVariableLeaseSet (requête de leaseSet variable) rapidement**: Uniquement une fois que les tunnels entrants et sortants sont établis

5. **Gérer les messages obsolètes**: Accepter mais déconseiller ReceiveMessageBegin/End

6. **Prendre en charge ECIES-X25519 (implémentation ECIES utilisant X25519)**: Privilégier le chiffrement de type 4 pour les nouveaux déploiements

## Débogage et dépannage

### Problèmes courants

**Session rejetée (invalide)**: - Vérifiez le décalage d'horloge (doit être dans une marge de ±30 secondes) - Vérifiez que Mapping est trié par clé - Assurez-vous que Destination n'est pas déjà utilisée

**Aucun RequestVariableLeaseSet**: - Router est peut-être en train de construire des tunnels (attendez jusqu'à 5 minutes) - Vérifiez s'il y a des problèmes de connectivité réseau - Vérifiez qu'il y a suffisamment de connexions aux pairs

**Échecs d'acheminement des messages**: - Vérifiez les codes MessageStatus pour identifier la cause précise de l'échec - Vérifiez que le LeaseSet distant est publié et à jour - Assurez-vous que les types de chiffrement sont compatibles

**Problèmes de Subsession (sous-session)**: - Vérifier que la session principale a été créée en premier - Confirmer les mêmes clés de chiffrement - Vérifier des clés de signature distinctes

### Messages de diagnostic

**GetBandwidthLimits**: Interroger les limites de bande passante du router **HostLookup**: Tester la résolution de noms et la disponibilité du LeaseSet **MessageStatus**: Suivre l'acheminement des messages de bout en bout

## Spécifications connexes

- **Structures communes**: /docs/specs/common-structures/
- **I2NP (protocole réseau)**: /docs/specs/i2np/
- **ECIES-X25519 (schéma ECIES avec X25519)**: /docs/specs/ecies/
- **Création de tunnel**: /docs/specs/implementation/
- **Bibliothèque de streaming**: /docs/specs/streaming/
- **Bibliothèque de datagrammes**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Propositions référencées

- [Proposition 123](/proposals/123-new-netdb-entries/): LeaseSets chiffrés et authentification
- [Proposition 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet (mécanisme de ratchet cryptographique combinant ECIES et X25519 avec AEAD)
- [Proposition 149](/proposals/149-b32-encrypted-ls2/): Format d’adresse aveuglé (b33)
- [Proposition 152](/proposals/152-ecies-tunnels/): Création de tunnel X25519
- [Proposition 154](/proposals/154-ecies-lookups/): Recherches dans la base de données à partir de destinations ECIES
- [Proposition 156](/proposals/156-ecies-routers/): Migration des routers vers ECIES-X25519
- [Proposition 161](/fr/proposals/161-ri-dest-padding/): Compression du bourrage de destination
- [Proposition 167](/proposals/167-service-records/): Enregistrements de service du LeaseSet
- [Proposition 169](/proposals/169-pq-crypto/): Cryptographie hybride post-quantique (ML-KEM)

## Référence des Javadocs

- [Package I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [API client](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Résumé des dépréciations

### Messages dépréciés (à ne pas utiliser)

- **CreateLeaseSetMessage** (type 4): Utilisez CreateLeaseSet2Message
- **RequestLeaseSetMessage** (type 21): Utilisez RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (type 6): Utilisez le mode de réception rapide
- **ReceiveMessageEndMessage** (type 7): Utilisez le mode de réception rapide
- **DestLookupMessage** (type 34): Utilisez HostLookupMessage
- **DestReplyMessage** (type 35): Utilisez HostReplyMessage
- **ReportAbuseMessage** (type 29): Jamais implémenté

### Options dépréciées

- Chiffrement ElGamal (type 0) : migrer vers ECIES-X25519 (type 4)
- Signatures DSA : migrer vers EdDSA ou ECDSA
- `i2cp.fastReceive=false` : toujours utiliser le mode de réception rapide
