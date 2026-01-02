---
title: "Datagrammes"
description: "Formats de messages authentifiés, avec réponse et bruts au-dessus d'I2CP"
slug: "datagrams"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Aperçu

Les datagrammes fournissent une communication orientée message au-dessus d'[I2CP](/docs/specs/i2cp/) et en parallèle de la bibliothèque de streaming. Ils permettent des paquets **avec réponse possible**, **authentifiés** ou **bruts** sans nécessiter de flux orientés connexion. Les routeurs encapsulent les datagrammes dans des messages I2NP et des messages tunnel, que le trafic soit transporté par NTCP2 ou SSU2.

La motivation principale est de permettre aux applications (comme les trackers, les résolveurs DNS ou les jeux) d'envoyer des paquets autonomes qui identifient leur expéditeur.

> **Nouveau en 2025 :** Le projet I2P a approuvé **Datagram2 (protocole 19)** et **Datagram3 (protocole 20)**, ajoutant une protection contre la rejouabilité et une messagerie répondable à faible surcharge pour la première fois en une décennie.

---

## 1. Constantes de protocole

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed (repliable) datagram – “Datagram1”</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM_RAW</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsigned (raw) datagram – no sender info</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Signed + replay-protected datagram</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>PROTO_DATAGRAM3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable (no signature, hash only)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">API 0.9.66 (2025)</td>
    </tr>
  </tbody>
</table>
Les protocoles 19 et 20 ont été formalisés dans la **Proposition 163 (avril 2025)**. Ils coexistent avec Datagram1 / RAW pour assurer la rétrocompatibilité.

---

## 2. Types de datagrammes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Repliable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Authenticated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Replay Protection</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Min Overhead</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Raw</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal size; spoofable.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 427</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Full Destination + signature.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 457</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replay prevention + offline signatures; PQ-ready.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Datagram3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">≈ 34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender hash only; low overhead.</td>
    </tr>
  </tbody>
</table>
### Modèles de conception typiques

- **Requête → Réponse :** Envoyez un Datagram2 signé (requête + nonce), recevez une réponse brute ou Datagram3 (écho nonce).  
- **Haute fréquence/faible surcharge :** Préférez Datagram3 ou RAW.  
- **Messages de contrôle authentifiés :** Datagram2.  
- **Compatibilité héritée :** Datagram1 toujours entièrement pris en charge.

---

## 3. Détails de Datagram2 et Datagram3 (2025)

### Datagram2 (Protocole 19)

Remplacement amélioré de Datagram1. Fonctionnalités : - **Prévention de la rejouabilité :** jeton anti-rejouabilité de 4 octets. - **Support de signature hors ligne :** permet l'utilisation par des Destinations signées hors ligne. - **Couverture de signature étendue :** inclut le hachage de destination, les drapeaux, les options, le bloc de signature hors ligne, la charge utile. - **Prêt pour le post-quantique :** compatible avec les futurs hybrides ML-KEM. - **Surcharge :** ≈ 457 octets (clés X25519).

### Datagram3 (Protocole 20)

Comble le fossé entre les types bruts et signés. Fonctionnalités : - **Peut être répondu sans signature :** contient le hash 32 octets de l'expéditeur + drapeaux 2 octets. - **Surcharge minime :** ≈ 34 octets. - **Aucune défense contre la rejouabilité** — l'application doit l'implémenter.

Les deux protocoles sont des fonctionnalités de l'API 0.9.66 et implémentés dans le routeur Java depuis la version 2.9.0 ; aucune implémentation i2pd ou Go pour l'instant (octobre 2025).

---

## 4. Limites de taille et de fragmentation

- **Taille du message tunnel :** 1 028 octets (4 o ID Tunnel + 16 o IV + 1 008 o charge utile).  
- **Fragment initial :** 956 o (livraison TUNNEL typique).  
- **Fragment suivant :** 996 o.  
- **Fragments max :** 63–64.  
- **Limite pratique :** ≈ 62 708 o (~61 Ko).  
- **Limite recommandée :** ≤ 10 Ko pour une livraison fiable (les pertes augmentent de manière exponentielle au-delà).

**Résumé de la surcharge :** - Datagram1 ≈ 427 o (minimum).   - Datagram2 ≈ 457 o.   - Datagram3 ≈ 34 o.   - Couches supplémentaires (en-tête I2CP gzip, I2NP, Garlic, Tunnel) : + ~5,5 Ko dans le pire cas.

---

## 5. Intégration I2CP / I2NP

Chemin du message : 1. L'application crée un datagramme (via l'API I2P ou SAM). 2. I2CP l'enveloppe avec un en-tête gzip (`0x1F 0x8B 0x08`, RFC 1952) et une somme de contrôle CRC-32. 3. Les numéros de protocole + port sont stockés dans les champs d'en-tête gzip. 4. Le router encapsule comme message I2NP → clove Garlic → fragments de tunnel de 1 KB. 5. Les fragments traversent le tunnel sortant → réseau → tunnel entrant. 6. Le datagramme réassemblé est livré au gestionnaire d'application en fonction du numéro de protocole.

**Intégrité :** CRC-32 (depuis I2CP) + signature cryptographique optionnelle (Datagram1/2). Il n'y a pas de champ de somme de contrôle séparé dans le datagramme lui-même.

---

## 6. Interfaces de programmation

### API Java

Le package `net.i2p.client.datagram` comprend : - `I2PDatagramMaker` – construit des datagrammes signés.   - `I2PDatagramDissector` – vérifie et extrait les informations de l'expéditeur.   - `I2PInvalidDatagramException` – levée en cas d'échec de vérification.

`I2PSessionMuxedImpl` (`net.i2p.client.impl.I2PSessionMuxedImpl`) gère le multiplexage de protocole et de port pour les applications partageant une Destination.

**Accès Javadoc :** - [idk.i2p Javadoc](http://idk.i2p/javadoc-i2p/) (réseau I2P uniquement) - [Miroir Javadoc](https://eyedeekay.github.io/javadoc-i2p/) (miroir clearnet) - [Javadocs officiels](http://docs.i2p-projekt.de/javadoc/) (documentation officielle)

### Support SAMv3

- SAM 3.2 (2016) : ajout des paramètres PORT et PROTOCOL.  
- SAM 3.3 (2016) : introduction du modèle PRIMARY/subsession ; permet les flux + datagrammes sur une seule Destination.  
- Support des styles de session Datagram2 / 3 ajouté à la spécification 2025 (implémentation en attente).  
- Spécification officielle : [Spécification SAM v3](/docs/api/samv3/)

### Modules i2ptunnel

- **udpTunnel:** Base entièrement fonctionnelle pour les applications I2P UDP (`net.i2p.i2ptunnel.udpTunnel`).  
- **streamr:** Opérationnel pour le streaming A/V (`net.i2p.i2ptunnel.streamr`).  
- **SOCKS UDP:** **Non fonctionnel** depuis la version 2.10.0 (stub UDP uniquement).

> Pour l'UDP à usage général, utilisez l'API Datagram ou udpTunnel directement — ne vous fiez pas au SOCKS UDP.

---

## 7. Écosystème et support linguistique (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Library / Package</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">SAM Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Java</td><td style="border:1px solid var(--color-border); padding:0.5rem;">core API (net.i2p.client.datagram)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">✓ full support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C++</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2pd / libsam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2 partial</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Limited</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Go</td><td style="border:1px solid var(--color-border); padding:0.5rem;">go-i2p / sam3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.1–3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Python</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2plib, i2p.socket, txi2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rust</td><td style="border:1px solid var(--color-border); padding:0.5rem;">i2p-rs, i2p_client</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">C#</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2PSharp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">JS/TS</td><td style="border:1px solid var(--color-border); padding:0.5rem;">node-i2p, i2p-sam</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Haskell</td><td style="border:1px solid var(--color-border); padding:0.5rem;">network-anonymous-i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lua</td><td style="border:1px solid var(--color-border); padding:0.5rem;">mooni2p</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3.2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td></tr>
  </tbody>
</table>
Java I2P est le seul routeur prenant en charge les subsessions SAM 3.3 complètes et l'API Datagram2 à l'heure actuelle.

---

## 8. Exemple d'utilisation – Tracker UDP (I2PSnark 2.10.0)

Première application concrète de Datagram2/3 :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Datagram Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Announce Request</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Repliable but low-overhead update</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Response</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Raw Datagram</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal payload return</td></tr>
  </tbody>
</table>
Le modèle démontre l'utilisation mixte de datagrammes authentifiés et légers pour équilibrer sécurité et performance.

---

## 9. Sécurité et bonnes pratiques

- Utilisez Datagram2 pour tout échange authentifié ou lorsque les attaques par rejeu sont importantes.
- Préférez Datagram3 pour des réponses rapides reproductibles avec une confiance modérée.
- Utilisez RAW pour les diffusions publiques ou les données anonymes.
- Maintenez les charges utiles ≤ 10 Ko pour une livraison fiable.
- Sachez que SOCKS UDP reste non fonctionnel.
- Vérifiez toujours le CRC gzip et les signatures numériques à la réception.

---

## 10. Spécification technique

Cette section couvre les formats de datagrammes de bas niveau, l'encapsulation et les détails du protocole.

### 10.1 Identification du protocole

Les formats de datagramme **ne partagent pas** d'en-tête commun. Les routeurs ne peuvent pas déduire le type uniquement à partir des octets de la charge utile.

Lors du mélange de plusieurs types de datagrammes—ou lors de la combinaison de datagrammes avec du streaming—définissez explicitement : - Le **numéro de protocole** (via I2CP ou SAM) - Éventuellement le **numéro de port**, si votre application multiplexe des services

Laisser le protocole non défini (`0` ou `PROTO_ANY`) est déconseillé et peut entraîner des erreurs de routage ou de livraison.

### 10.2 Datagrammes bruts

Les datagrammes non répondables ne contiennent aucune donnée d'expéditeur ou d'authentification. Ce sont des charges utiles opaques, gérées en dehors de l'API de datagrammes de niveau supérieur mais prises en charge via SAM et I2PTunnel.

**Protocole :** `18` (`PROTO_DATAGRAM_RAW`)

**Format :**

```
+----+----+----+----+----//
|     payload...
+----+----+----+----+----//
```
La longueur de la charge utile est contrainte par les limites du transport (≈32 Ko max pratique, souvent beaucoup moins).

### 10.3 Datagram1 (Datagrammes avec réponse)

Intègre la **Destination** de l'expéditeur et une **Signature** pour l'authentification et l'adressage de réponse.

**Protocole :** `17` (`PROTO_DATAGRAM`)

**Surcharge :** ≥427 octets **Charge utile :** jusqu'à ~31,5 Ko (limité par le transport)

**Format :**

```
+----+----+----+----+----+----+----+----+
|               from                    |
+                                       +
|                                       |
~             Destination bytes         ~
|                                       |
+----+----+----+----+----+----+----+----+
|             signature                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     payload...
+----+----+----+----//
```
- `from` : une Destination (387+ octets)
- `signature` : une Signature correspondant au type de clé
  - Pour DSA_SHA1 : Signature du hash SHA-256 de la charge utile
  - Pour les autres types de clés : Signature directement sur la charge utile

**Notes :** - Les signatures pour les types non-DSA ont été normalisées dans I2P 0.9.14. - Les signatures hors ligne LS2 (Proposition 123) ne sont actuellement pas prises en charge dans Datagram1.

### 10.4 Format Datagram2

Un datagramme réponse amélioré qui ajoute une **résistance aux rejeux** tel que défini dans la [Proposition 163](/proposals/163-datagram2/).

**Protocole:** `19` (`PROTO_DATAGRAM2`)

La mise en œuvre est en cours. Les applications doivent inclure des vérifications de nonce ou d'horodatage pour la redondance.

### 10.5 Format Datagram3

Fournit des datagrammes **pouvant recevoir une réponse mais non authentifiés**. S'appuie sur l'authentification de session maintenue par le router plutôt que sur une destination et une signature intégrées.

**Protocole :** `20` (`PROTO_DATAGRAM3`) **Statut :** En développement depuis 0.9.66

Utile lorsque : - Les destinations sont volumineuses (par exemple, clés post-quantiques) - L'authentification se produit à une autre couche - L'efficacité de la bande passante est critique

### 10.6 Intégrité des données

L'intégrité du datagramme est protégée par la **somme de contrôle gzip CRC-32** dans la couche I2CP. Aucun champ de somme de contrôle explicite n'existe dans le format de charge utile du datagramme lui-même.

### 10.7 Encapsulation des paquets

Chaque datagramme est encapsulé comme un seul message I2NP ou comme un clove individuel dans un **Garlic Message**. Les couches I2CP, I2NP et tunnel gèrent la longueur et le cadrage — il n'y a pas de délimiteur interne ou de champ de longueur dans le protocole de datagramme.

### 10.8 Considérations post-quantiques (PQ)

Si la **Proposition 169** (signatures ML-DSA) est mise en œuvre, les tailles de signature et de destination augmenteront considérablement — passant de ~455 octets à **≥3739 octets**. Ce changement augmentera substantiellement la surcharge des datagrammes et réduira la capacité de charge utile effective.

**Datagram3**, qui repose sur l'authentification au niveau de la session (et non sur des signatures intégrées), deviendra probablement la conception privilégiée dans les environnements I2P post-quantiques.

---

## 11. Références

- [Proposition 163 – Datagram2 et Datagram3](/proposals/163-datagram2/)
- [Proposition 160 – Intégration de Tracker UDP](/proposals/160-udp-trackers/)
- [Proposition 144 – Calculs MTU en Streaming](/proposals/144-ecies-x25519-aead-ratchet/)
- [Proposition 169 – Signatures Post-Quantiques](/proposals/169-pq-crypto/)
- [Spécification I2CP](/docs/specs/i2cp/)
- [Spécification I2NP](/docs/specs/i2np/)
- [Spécification des Messages Tunnel](/docs/specs/implementation/)
- [Spécification SAM v3](/docs/api/samv3/)
- [Documentation i2ptunnel](/docs/api/i2ptunnel/)

## 12. Points saillants du journal des modifications (2019 – 2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Year</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2019</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram API stabilization</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2021</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Protocol port handling reworked</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2022</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.0.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 adoption completed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.6.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy transport removal simplified UDP code</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.9.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Datagram2/3 support added (Java API)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">2025</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2.10.0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP Tracker implementation released</td></tr>
  </tbody>
</table>
---

## 13. Résumé

Le sous-système datagram prend désormais en charge quatre variantes de protocole offrant un spectre allant de la transmission entièrement authentifiée à la transmission brute légère. Les développeurs devraient migrer vers **Datagram2** pour les cas d'usage sensibles en matière de sécurité et **Datagram3** pour un trafic efficient avec possibilité de réponse. Tous les anciens types restent compatibles pour garantir l'interopérabilité à long terme.
