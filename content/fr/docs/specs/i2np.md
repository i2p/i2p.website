---
title: "Protocole réseau d'I2P (I2NP)"
description: "Formats de messages de router à router, priorités et limites de taille au sein d’I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Vue d'ensemble

Le protocole réseau I2P (I2NP) définit comment les routers échangent des messages, sélectionnent les transports et mélangent le trafic tout en préservant l’anonymat. Il fonctionne entre **I2CP** (API client) et les protocoles de transport (**NTCP2** et **SSU2**).

I2NP est la couche au-dessus des protocoles de transport I2P. C'est un protocole de type router-to-router utilisé pour: - Recherches et réponses dans la base de données du réseau - Création de tunnels - Messages de données chiffrés du router et du client

Les messages I2NP peuvent être envoyés point à point à un autre router, ou envoyés anonymement via des tunnels vers ce router.

Les Routers placent en file d’attente les tâches sortantes à l’aide de priorités locales. Les numéros de priorité plus élevés sont traités en premier. Toute priorité supérieure à la priorité standard des données de tunnel (400) est considérée comme urgente.

### Transports actuels

I2P utilise désormais **NTCP2** (TCP) et **SSU2** (UDP) à la fois pour IPv4 et IPv6. Les deux transports emploient: - **X25519** échange de clés (cadre de protocole Noise) - **ChaCha20/Poly1305** chiffrement authentifié (AEAD) - **SHA-256** hachage

**Transports hérités supprimés:** - NTCP (TCP d'origine) a été supprimé du router Java dans la version 0.9.50 (mai 2021) - SSU v1 (UDP d'origine) a été supprimé du router Java dans la version 2.4.0 (décembre 2023) - SSU v1 a été supprimé d'i2pd dans la version 2.44.0 (novembre 2022)

À partir de 2025, le réseau a entièrement basculé vers des transports basés sur Noise (cadre de protocoles cryptographiques), sans aucune prise en charge des transports hérités.

---

## Système de numérotation des versions

**IMPORTANT:** I2P utilise un double système de versionnage qui doit être clairement compris :

### Versions de publication (visibles par l’utilisateur)

Voici les versions que les utilisateurs voient et téléchargent : - 0.9.50 (mai 2021) - Dernière version 0.9.x - **1.5.0** (août 2021) - Première version 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (de 2021 à 2022) - **2.0.0** (novembre 2022) - Première version 2.x - 2.1.0 à 2.9.0 (de 2023 à 2025) - **2.10.0** (8 septembre 2025) - Version actuelle

### Versions d’API (compatibilité du protocole)

Ce sont les numéros de version internes publiés dans le champ "router.version" des propriétés RouterInfo : - 0.9.50 (mai 2021) - **0.9.51** (août 2021) - Version d'API pour la version 1.5.0 - 0.9.52 à 0.9.66 (se poursuivant dans les versions 2.x) - **0.9.67** (septembre 2025) - Version d'API pour la version 2.10.0

**Point clé :** Il n'y a eu AUCUNE version numérotée de 0.9.51 à 0.9.67. Ces numéros existent uniquement en tant qu'identifiants de version d'API. I2P est passé de la version 0.9.50 directement à la version 1.5.0.

### Table de correspondance des versions

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**À venir :** La version 2.11.0 (prévue pour décembre 2025) nécessitera Java 17+ et activera par défaut la cryptographie post-quantique.

---

## Versions du protocole

Tous les routers doivent publier leur version du protocole I2NP dans le champ "router.version" des propriétés RouterInfo (métadonnées d’un router I2P). Ce champ de version correspond à la version de l'API, indiquant le niveau de prise en charge de diverses fonctionnalités du protocole I2NP, et n’est pas nécessairement la version réelle du router.

Si des routers alternatifs (non-Java) souhaitent publier des informations de version concernant l’implémentation du router proprement dite, ils doivent le faire dans une autre propriété. Des versions autres que celles indiquées ci-dessous sont autorisées. La prise en charge sera déterminée par une comparaison numérique ; par exemple, 0.9.13 implique la prise en charge des fonctionnalités de 0.9.12.

**Remarque :** La propriété "coreVersion" n'est plus publiée dans les informations du router et n'a jamais été utilisée pour déterminer la version du protocole I2NP.

### Résumé des fonctionnalités par version de l’API

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Remarque :** Il existe également des fonctionnalités liées au transport et des problèmes de compatibilité. Voir la documentation des transports NTCP2 et SSU2 pour plus de détails.

---

## En-tête du message

I2NP utilise une structure d’en-tête logique de 16 octets, tandis que les transports modernes (NTCP2 et SSU2) utilisent un en-tête raccourci de 9 octets, omettant les champs de taille et de somme de contrôle redondants. Les champs restent conceptuellement identiques.

### Comparaison des formats d'en-tête

**Format standard (16 octets):**

Utilisé dans le transport NTCP hérité et lorsque des messages I2NP sont encapsulés dans d'autres messages (TunnelData, TunnelGateway, GarlicClove).

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Format court pour SSU (Obsolète, 5 octets):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Format court pour NTCP2, SSU2 et ECIES-Ratchet Garlic Cloves (éléments « clove » d’un message garlic dans ECIES-Ratchet) (9 octets):**

Utilisé dans les transports modernes et dans les garlic messages (messages groupés spécifiques à I2P) chiffrés avec ECIES.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Détails des champs d'en-tête

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Notes de mise en œuvre

- Lorsqu’il est transmis via SSU (obsolète), seuls le type et l’expiration sur 4 octets étaient inclus
- Lorsqu’il est transmis via NTCP2 ou SSU2, le format court de 9 octets est utilisé
- L’en-tête standard de 16 octets est requis pour les messages I2NP contenus dans d’autres messages (Data, TunnelData, TunnelGateway, GarlicClove)
- Depuis la version 0.8.12, la vérification de la somme de contrôle est désactivée à certains endroits de la pile de protocoles pour des raisons d’efficacité, mais la génération de la somme de contrôle reste requise pour la compatibilité
- L’expiration courte est non signée et reviendra à zéro le 7 février 2106. Après cette date, un décalage doit être ajouté pour obtenir l’heure correcte
- Pour la compatibilité avec les anciennes versions, générez toujours des sommes de contrôle même si elles peuvent ne pas être vérifiées

---

## Contraintes de taille

Les messages Tunnel fragmentent les charges utiles I2NP en morceaux de taille fixe:
- **Premier fragment:** environ 956 octets
- **Fragments suivants:** environ 996 octets chacun
- **Nombre maximal de fragments:** 64 (numérotés 0-63)
- **Charge utile maximale:** environ 61 200 octets (61,2 KB)

**Calcul:** 956 + (63 × 996) = maximum théorique de 63,704 octets, avec une limite pratique d'environ 61,200 octets en raison de l'overhead (surcharge).

### Contexte historique

Les anciens transports avaient des limites de taille de trame plus strictes: - NTCP: trames de 16 Ko - SSU: trames d’environ 32 Ko

NTCP2 prend en charge des trames d’environ 65 Ko, mais la limite de fragmentation du tunnel s’applique toujours.

### Considérations relatives aux données applicatives

Les Garlic messages (messages composites d'I2P) peuvent regrouper des LeaseSets, des Session Tags (étiquettes de session), ou des variantes LeaseSet2 chiffrées, réduisant l'espace disponible pour les données de charge utile.

**Recommandation:** Les datagrammes devraient rester ≤ 10 KB pour assurer une livraison fiable. Les messages s'approchant de la limite de 61 KB peuvent subir : - Latence accrue due au réassemblage après fragmentation - Probabilité plus élevée d'échec de livraison - Plus grande exposition à l'analyse du trafic

### Détails techniques de la fragmentation

Chaque message de tunnel fait exactement 1 024 octets (1 Ko) et contient : - ID de tunnel de 4 octets - vecteur d'initialisation de 16 octets (IV) - 1 004 octets de données chiffrées

Au sein des données chiffrées, les messages tunnel transportent des messages I2NP fragmentés avec des en-têtes de fragment indiquant: - Numéro de fragment (0-63) - S'il s'agit du premier fragment ou d'un fragment suivant - ID de message global pour le réassemblage

Le premier fragment inclut l’en-tête complet de message I2NP (16 octets), laissant environ 956 octets pour la charge utile. Les fragments suivants n’incluent pas l’en-tête du message, ce qui permet environ 996 octets de charge utile par fragment.

---

## Types de messages courants

Les routers utilisent le type de message et la priorité pour ordonnancer les tâches sortantes. Les valeurs de priorité les plus élevées sont traitées en premier. Les valeurs ci-dessous correspondent aux valeurs par défaut actuelles de Java I2P (version de l'API 0.9.67).

**Remarque:** Les priorités dépendent de l’implémentation. Pour connaître les valeurs de priorité de référence, consultez la documentation de la classe `OutNetMessage` dans le code source Java d’I2P.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Types de messages réservés :** - Type 0 : Réservé - Types 4-9 : Réservés pour un usage futur - Types 12-17 : Réservés pour un usage futur - Types 224-254 : Réservés pour des messages expérimentaux - Type 255 : Réservé pour de futures extensions

### Notes sur les types de messages

- Les messages du plan de contrôle (DatabaseLookup, TunnelBuild, etc.) empruntent généralement des **tunnels exploratoires**, et non des tunnels clients, ce qui permet une priorisation indépendante
- Les valeurs de priorité sont approximatives et peuvent varier selon l'implémentation
- TunnelBuild (21) et TunnelBuildReply (22) sont dépréciés mais toujours implémentés pour la compatibilité avec les tunnels très longs (>8 sauts)
- La priorité standard des données de tunnel est de 400; tout ce qui est au-dessus est traité comme urgent
- La longueur typique des tunnels dans le réseau actuel est de 3-4 sauts, donc la plupart des constructions de tunnel utilisent ShortTunnelBuild (enregistrements de 218 octets) ou VariableTunnelBuild (enregistrements de 528 octets)

---

## Chiffrement et encapsulation des messages

Les routers encapsulent fréquemment des messages I2NP avant la transmission, créant plusieurs couches de chiffrement. Un message DeliveryStatus peut être : 1. enveloppé dans un GarlicMessage (chiffré) 2. à l’intérieur d’un DataMessage 3. au sein d’un TunnelData message (à nouveau chiffré)

Chaque saut ne déchiffre que sa couche ; la destination finale révèle la charge utile la plus interne.

### Algorithmes de chiffrement

**Hérité (en cours de retrait progressif):** - ElGamal/AES + SessionTags (étiquettes de session) - ElGamal-2048 pour le chiffrement asymétrique - AES-256 pour le chiffrement symétrique - session tags de 32 octets

**Actuel (Standard depuis l'API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD avec confidentialité persistante à cliquet - Noise Protocol Framework (Noise_IK_25519_ChaChaPoly_SHA256 pour les destinations) - Étiquettes de session de 8 octets (réduites de 32 octets) - Algorithme Signal Double Ratchet pour la confidentialité persistante (forward secrecy) - Introduit dans la version d'API 0.9.46 (2020) - Obligatoire pour tous les routers à partir de la version d'API 0.9.58 (2023)

**À venir (Bêta à partir de la version 2.10.0):** - Cryptographie hybride post-quantique utilisant MLKEM (ML-KEM-768) combinée avec X25519 - Cliquet hybride combinant des mécanismes d’accord de clé classiques et post-quantiques - Rétrocompatible avec ECIES-X25519 - Deviendra la valeur par défaut dans la version 2.11.0 (décembre 2025)

### Mise en obsolescence du Router ElGamal

**CRITIQUE:** Les routers ElGamal ont été dépréciés à partir de la version d’API 0.9.58 (version 2.2.0, mars 2023). Étant donné que la version floodfill minimale recommandée pour les requêtes est désormais 0.9.58, les implémentations n’ont pas besoin d’implémenter le chiffrement pour les routers floodfill ElGamal.

**Cependant :** Les destinations ElGamal sont toujours prises en charge pour la rétrocompatibilité. Les clients utilisant le chiffrement ElGamal peuvent toujours communiquer via des routers ECIES.

### Détails sur ECIES-X25519-AEAD-Ratchet (mécanisme de cliquet cryptographique basé sur ECIES-X25519 avec AEAD)

C'est le crypto type 4 (type de chiffrement 4) dans la spécification de cryptographie d'I2P. Il fournit:

**Caractéristiques clés :** - Confidentialité persistante grâce au ratcheting (mécanisme à cliquet cryptographique; nouvelles clés pour chaque message) - Réduction du stockage des étiquettes de session (8 octets contre 32 octets) - Plusieurs types de session (nouvelle session, session existante, session à usage unique) - Basé sur le protocole Noise Noise_IK_25519_ChaChaPoly_SHA256 - Intégré à l’algorithme Double Ratchet de Signal

**Primitives cryptographiques:** - X25519 pour l'accord de clé Diffie-Hellman - ChaCha20 pour le chiffrement en flux - Poly1305 pour l'authentification des messages (AEAD, chiffrement authentifié avec données associées) - SHA-256 pour le hachage - HKDF pour la dérivation de clés

**Gestion des sessions:** - Nouvelle session: Connexion initiale utilisant une clé de destination statique - Session existante: Messages ultérieurs utilisant des session tags (étiquettes de session) - Session à usage unique: Sessions à message unique pour une surcharge réduite

Voir [Spécification ECIES](/docs/specs/ecies/) et [Proposition 144](/proposals/144-ecies-x25519-aead-ratchet/) pour des détails techniques complets.

---

## Structures communes

Les structures suivantes sont des éléments de plusieurs messages I2NP. Ce ne sont pas des messages complets.

### BuildRequestRecord (enregistrement de requête de construction) (ElGamal)

**DÉPRÉCIÉ.** Uniquement utilisé dans le réseau actuel lorsqu'un tunnel contient un router ElGamal. Voir [ECIES Tunnel Creation](/docs/specs/implementation/) pour le format moderne.

**Objectif:** Un enregistrement dans un ensemble de plusieurs enregistrements pour demander la création d'un saut dans le tunnel.

**Format:**

Chiffré avec ElGamal et AES (528 octets au total):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
Structure chiffrée par ElGamal (528 octets):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Structure en clair (222 octets avant chiffrement) :

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Notes :** - Le chiffrement ElGamal-2048 produit un bloc de 514 octets, mais les deux octets de bourrage (aux positions 0 et 257) sont supprimés, pour un total de 512 octets - Voir [Spécification de création de Tunnel](/docs/specs/implementation/) pour les détails des champs - Code source : `net.i2p.data.i2np.BuildRequestRecord` - Constante : `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 Long)

Pour les routers ECIES-X25519, introduits dans la version de l’API 0.9.48. Utilise 528 octets pour la rétrocompatibilité avec des tunnels mixtes.

**Format :**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Taille totale :** 528 octets (identique à ElGamal pour des raisons de compatibilité)

Voir [Création de Tunnel ECIES](/docs/specs/implementation/) pour la structure des données en clair et les détails du chiffrement.

### BuildRequestRecord (ECIES-X25519 version courte)

Uniquement pour les routers ECIES-X25519, à partir de la version de l'API 0.9.51 (version 1.5.0). Il s’agit du format standard actuel.

**Format:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Taille totale:** 218 octets (réduction de 59 % par rapport à 528 octets)

**Différence clé :** Les enregistrements courts dérivent TOUTES les clés via HKDF (fonction de dérivation de clés) plutôt que de les inclure explicitement dans l'enregistrement. Cela inclut : - Clés de couche (pour le chiffrement du tunnel) - Clés IV (vecteur d'initialisation) (pour le chiffrement du tunnel) - Clés de réponse (pour build reply [réponse de construction]) - IV de réponse (pour build reply)

Toutes les clés sont dérivées à l'aide du mécanisme HKDF du protocole Noise, à partir du secret partagé issu de l'échange de clés X25519.

**Avantages:** - 4 enregistrements courts tiennent dans un seul message de tunnel (873 octets) - 3 messages de construction de tunnel au lieu de messages séparés pour chaque enregistrement - Bande passante et latence réduites - Mêmes propriétés de sécurité que le format long

Voir [Proposition 157](/proposals/157-new-tbm/) pour la justification et [Création de tunnel ECIES](/docs/specs/implementation/) pour la spécification complète.

**Code source :** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Constante : `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (enregistrement de réponse de construction) (ElGamal)

**OBSOLÈTE.** Uniquement utilisé lorsque le tunnel contient un router ElGamal.

**Objectif :** Un enregistrement au sein d’un ensemble de plusieurs enregistrements contenant des réponses à une requête de construction.

**Format :**

Chiffré (528 octets, même taille que BuildRequestRecord) :

```
bytes 0-527 :: AES-encrypted record
```
Structure non chiffrée:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Codes de réponse :** - `0` - Accepté - `30` - Rejeté (bande passante dépassée)

Voir [Spécification de création de tunnel](/docs/specs/implementation/) pour plus de détails sur le champ de réponse.

### BuildResponseRecord (ECIES-X25519)

Pour les routers ECIES-X25519, version de l’API 0.9.48+. Même taille que la requête correspondante (528 pour le format long, 218 pour le format court).

**Format:**

Format long (528 octets):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Format court (218 octets):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Structure du texte en clair (les deux formats):**

Contient une structure Mapping (format clé-valeur d'I2P) avec: - Code d'état de réponse (obligatoire) - Paramètre de bande passante disponible ("b") (facultatif, ajouté dans l'API 0.9.65) - Autres paramètres optionnels pour de futures extensions

**Codes d'état de réponse:** - `0` - Succès - `30` - Rejet : bande passante dépassée

Voir [Création de tunnel ECIES](/docs/specs/implementation/) pour la spécification complète.

### GarlicClove (ElGamal/AES) (élément de base d’un message garlic d’I2P)

**AVERTISSEMENT :** Ceci est le format utilisé pour les garlic cloves (gousses de message) à l’intérieur des garlic messages chiffrés avec ElGamal. Le format des garlic messages et des garlic cloves ECIES-AEAD-X25519-Ratchet est sensiblement différent. Voir [Spécification ECIES](/docs/specs/ecies/) pour le format moderne.

**Déprécié pour les routers (API 0.9.58+), toujours pris en charge pour les destinations.**

**Format :**

Non chiffré:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Remarques:** - Les clove (sous-messages) ne sont jamais fragmentés - Lorsque le premier bit de l'octet de drapeau des Delivery Instructions vaut 0, le clove n'est pas chiffré - Lorsque le premier bit vaut 1, le clove est chiffré (fonctionnalité non implémentée) - La longueur maximale est fonction de la somme des longueurs des clove et de la longueur maximale de GarlicMessage - Le certificat pourrait éventuellement être utilisé avec HashCash pour "payer" l'acheminement (possibilité future) - Messages utilisés en pratique : DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage peut contenir un GarlicMessage (garlic imbriqué), mais cela n'est pas utilisé en pratique

Voir [Garlic Routing](/docs/overview/garlic-routing/) (technique de routage d'I2P où plusieurs messages sont regroupés) pour un aperçu conceptuel.

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

Pour les routers et les destinations ECIES-X25519, version de l'API 0.9.46+. C'est le format standard actuel.

**DIFFÉRENCE FONDAMENTALE:** ECIES garlic utilise une structure complètement différente, basée sur des blocs du protocole Noise plutôt que sur des structures de clove (sous-message d’un message garlic) explicites.

**Format :**

Les messages garlic (agrégation de messages spécifique à I2P) ECIES contiennent une série de blocs :

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Types de blocs:** - `0` - Garlic Clove Block (bloc « Garlic Clove »; contient un message I2NP) - `1` - Bloc DateTime (horodatage) - `2` - Bloc d’options (options d’acheminement) - `3` - Bloc de bourrage - `254` - Bloc de terminaison (non implémenté)

**Bloc Garlic Clove (gousse d'ail) (type 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Principales différences par rapport au format ElGamal :** - Utilise une expiration sur 4 octets (secondes depuis l'époque Unix) au lieu d'une Date sur 8 octets - Aucun champ de certificat - Encapsulé dans une structure de blocs avec type et longueur - Message entier chiffré avec ChaCha20/Poly1305 AEAD - Gestion de session via ratcheting (mécanisme à cliquet)

Voir [Spécification ECIES](/docs/specs/ecies/) pour des détails complets sur le Noise Protocol Framework (cadre de protocoles Noise) et les structures de blocs.

### Instructions d’acheminement de Garlic Clove (élément « clove » d’un message garlic dans I2P)

Ce format est utilisé à la fois pour les gousses « garlic » (terme I2P) ElGamal et ECIES. Il spécifie comment acheminer le message inclus.

**AVERTISSEMENT CRITIQUE:** Cette spécification concerne UNIQUEMENT les Delivery Instructions ("instructions de livraison") à l'intérieur des Garlic Cloves (gousses d'ail). "Delivery Instructions" sont également utilisées à l'intérieur des Tunnel Messages, où le format est sensiblement différent. Voir la [Tunnel Message Specification](/docs/specs/implementation/) pour les instructions de livraison liées aux tunnels. NE PAS confondre ces deux formats.

**Format :**

La clé de session et le délai ne sont pas utilisés et ne sont jamais présents, donc les trois longueurs possibles sont :
- 1 octet (LOCAL)
- 33 octets (ROUTER et DESTINATION)
- 37 octets (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Longueurs typiques:** - acheminement LOCAL: 1 octet (drapeau uniquement) - acheminement ROUTER / DESTINATION: 33 octets (drapeau + hachage) - acheminement TUNNEL: 37 octets (drapeau + hachage + ID de tunnel)

**Descriptions des types de livraison:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Notes d'implémentation:** - Le chiffrement par clé de session n'est pas implémenté et le bit de drapeau est toujours à 0 - Le délai n'est pas entièrement implémenté et le bit de drapeau est toujours à 0 - Pour l'acheminement TUNNEL, le hachage identifie le router passerelle et l'ID de tunnel spécifie quel tunnel entrant - Pour l'acheminement DESTINATION, le hachage est le SHA-256 de la clé publique de la destination - Pour l'acheminement ROUTER, le hachage est le SHA-256 de l'identité du router

---

## Messages I2NP

Spécifications complètes pour tous les types de messages I2NP.

### Résumé des types de messages

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Réservé:** - Type 0: Réservé - Types 4-9: Réservés pour une utilisation future - Types 12-17: Réservés pour une utilisation future - Types 224-254: Réservés pour des messages expérimentaux - Type 255: Réservé pour de futures extensions

---

### DatabaseStore (Type 1)

**Objectif :** Un enregistrement non sollicité dans la base de données, ou la réponse à un message DatabaseLookup (recherche dans la base de données) réussi.

**Contenu :** Un LeaseSet non compressé, un LeaseSet2, un MetaLeaseSet ou un EncryptedLeaseSet, ou un RouterInfo compressé.

**Format avec jeton de réponse:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Format avec le jeton de réponse == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**Notes :** - Pour des raisons de sécurité, les champs de réponse sont ignorés si le message est reçu via un tunnel - La clé est le hachage « réel » de la RouterIdentity ou de la Destination, ET NON la clé de routage - Les types 3, 5 et 7 (variantes de LeaseSet2) ont été ajoutés dans la version 0.9.38 (API 0.9.38). Voir [Proposition 123](/proposals/123-new-netdb-entries/) pour plus de détails - Ces types ne doivent être envoyés qu’aux routers dont la version d’API est 0.9.38 ou supérieure - À titre d’optimisation pour réduire les connexions, si le type est un LeaseSet, que le jeton de réponse est inclus, que l’ID de tunnel de réponse est non nul, et que la paire passerelle de réponse/tunnelID se trouve dans le LeaseSet en tant que lease, le destinataire peut réacheminer la réponse vers n’importe quel autre lease dans le LeaseSet - **Format gzip de RouterInfo :** Pour masquer l’OS et l’implémentation du router, imiter l’implémentation du router Java en définissant la date de modification à 0 et l’octet OS à 0xFF, et régler XFL à 0x02 (compression maximale, algorithme le plus lent) conformément à la RFC 1952. 10 premiers octets : `1F 8B 08 00 00 00 00 00 02 FF`

**Code source:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (pour la structure RouterInfo) - `net.i2p.data.LeaseSet` (pour la structure LeaseSet)

---

### DatabaseLookup (Type 2) (requête de recherche dans la base de données)

**Objectif:** Une requête visant à rechercher un élément dans la base de données réseau. La réponse est soit un DatabaseStore, soit un DatabaseSearchReply.

**Format :**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Modes de chiffrement des réponses :**

**REMARQUE:** Les routers ElGamal sont dépréciés depuis l'API 0.9.58. Étant donné que la version minimale recommandée de floodfill à interroger est désormais 0.9.58, les implémentations n'ont pas à implémenter le chiffrement pour les routers floodfill ElGamal. Les destinations ElGamal sont toujours prises en charge.

Le bit d’indicateur 4 (ECIESFlag) est utilisé en combinaison avec le bit 1 (encryptionFlag) pour déterminer le mode de chiffrement de la réponse :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Aucun chiffrement (indicateurs 0,0):**

reply_key, tags et reply_tags ne sont pas présents.

**ElG vers ElG (indicateurs 0,1) - OBSOLÈTE:**

Pris en charge à partir de 0.9.7, déprécié à partir de 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES vers ElG (indicateurs 1,0) - OBSOLÈTE:**

Pris en charge depuis la 0.9.46, déprécié depuis la 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
La réponse est un message ECIES Existing Session (session existante) tel que défini dans la [Spécification ECIES](/docs/specs/ecies/) :

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES (schéma de chiffrement intégré à courbe elliptique) vers ECIES (drapeaux 1,0) - NORME ACTUELLE:**

Une destination ECIES ou un router envoie une requête de recherche à un router ECIES. Pris en charge à partir de la version 0.9.49.

Même format que "ECIES to ElG" ci-dessus. Le chiffrement du message de recherche est spécifié dans [ECIES Routers](/docs/specs/ecies/#routers). Le demandeur est anonyme.

**ECIES vers ECIES avec DH (indicateurs 1,1) - FUTUR:**

Pas encore entièrement défini. Voir [la Proposition 156](/proposals/156-ecies-routers/).

**Notes :** - Avant la 0.9.16, la clé pouvait correspondre à un RouterInfo (descriptif de routeur) ou à un LeaseSet (ensemble de baux) (même espace de clés, aucun indicateur pour les distinguer) - Les réponses chiffrées ne sont utiles que lorsque la réponse passe par un tunnel - Le nombre d’étiquettes (tags) incluses peut être supérieur à un si des stratégies alternatives de recherche DHT sont mises en œuvre - La clé de recherche et les clés d’exclusion sont les hachages « réels », PAS des clés de routage - Les types 3, 5 et 7 (variantes de LeaseSet2) peuvent être retournés depuis la 0.9.38. Voir [Proposition 123](/proposals/123-new-netdb-entries/) - **Notes sur les recherches exploratoires :** Une recherche exploratoire est définie comme renvoyant une liste de hachages non-floodfill proches de la clé. Cependant, les implémentations varient : Java recherche bien la clé de recherche pour un RI (RouterInfo) et renvoie un DatabaseStore (enregistrement de base de données) s’il est présent ; i2pd ne le fait pas. Par conséquent, il n’est pas recommandé d’utiliser une recherche exploratoire pour des hachages déjà reçus

**Code source:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Chiffrement: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Type 3)

**Objectif :** La réponse à un message DatabaseLookup (recherche dans la base de données) ayant échoué.

**Contenu:** Une liste de hachages de router les plus proches de la clé demandée.

**Format:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Remarques:** - Le hachage 'from' n'est pas authentifié et ne peut pas être considéré comme digne de confiance - Les hachages des pairs renvoyés ne sont pas nécessairement plus proches de la clé que le router interrogé. Pour les réponses aux recherches normales, cela facilite la découverte de nouveaux floodfills et la recherche "à rebours" (plus éloignée de la clé) afin d'améliorer la robustesse - Pour les recherches d'exploration, la clé est généralement générée aléatoirement. Les peer_hashes non-floodfill de la réponse peuvent être sélectionnés à l'aide d'un algorithme optimisé (par ex., des pairs proches mais pas nécessairement les plus proches) afin d'éviter un tri inefficace de toute la base de données locale. Des stratégies de mise en cache peuvent également être utilisées. Cela dépend de l'implémentation - **Nombre typique de hachages renvoyés:** 3 - **Nombre maximal recommandé de hachages à renvoyer:** 16 - La clé de recherche, les hachages des pairs et le hachage 'from' sont de "vrais" hachages, PAS des clés de routage - Si num vaut 0, cela indique qu'aucun pair plus proche n'a été trouvé (impasse)

**Code source :** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (statut de livraison) (Type 10)

**Objectif:** Un simple accusé de réception de message. Généralement créé par l’émetteur du message et encapsulé dans un Garlic Message (message de type « Garlic » dans I2P) avec le message lui-même, pour être renvoyé par la destination.

**Contenu :** L'identifiant du message livré ainsi que l'heure de création ou d'arrivée.

**Format :**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Remarques :** - L'horodatage est toujours défini par le créateur sur l'heure actuelle. Cependant, cela est utilisé à plusieurs endroits dans le code, et d'autres usages pourraient être ajoutés à l'avenir - Ce message est également utilisé comme confirmation d'établissement de session dans SSU. Dans ce cas, l'ID de message est défini sur un nombre aléatoire, et le "arrival time" (heure d'arrivée) est défini sur l'ID global du réseau actuel, qui vaut 2 (c.-à-d. `0x0000000000000002`) - DeliveryStatus est généralement encapsulé dans un GarlicMessage et envoyé via un tunnel afin de fournir un accusé de réception sans révéler l'expéditeur - Utilisé pour les tests de tunnel afin de mesurer la latence et la fiabilité

**Code source :** - `net.i2p.data.i2np.DeliveryStatusMessage` - Utilisé dans : `net.i2p.router.tunnel.InboundEndpointProcessor` pour les tests de tunnel

---

### GarlicMessage (Type 11)

**AVERTISSEMENT :** Il s'agit du format utilisé pour les messages garlic chiffrés avec ElGamal. Le format des messages garlic ECIES-AEAD-X25519-Ratchet (mécanisme à cliquet cryptographique) est sensiblement différent. Voir la [Spécification ECIES](/docs/specs/ecies/) pour le format moderne.

**Objectif:** Utilisé pour encapsuler plusieurs messages I2NP chiffrés.

**Contenu:** Une fois déchiffré, une série de Garlic Cloves (éléments unitaires d’un message garlic encryption) et des données supplémentaires, également appelée Clove Set (ensemble de Garlic Cloves).

**Format chiffré:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Données déchiffrées (Clove Set, ensemble de gousses):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
**Notes:** - Lorsque non chiffrées, les données contiennent une ou plusieurs Garlic Cloves (segments « garlic ») - Le bloc chiffré AES est rembourré jusqu’à un minimum de 128 octets ; avec la Session Tag de 32 octets (étiquette de session), la taille minimale du message chiffré est de 160 octets ; avec le champ de longueur de 4 octets, la taille minimale du Garlic Message (message « garlic ») est de 164 octets - La longueur maximale réelle est inférieure à 64 Ko (limite pratique d’environ 61,2 Ko pour les messages de tunnel) - Voir [ElGamal/AES Specification](/docs/legacy/elgamal-aes/) pour les détails du chiffrement - Voir [Garlic Routing](/docs/overview/garlic-routing/) pour une vue d’ensemble conceptuelle - La taille minimale de 128 octets du bloc chifré AES n’est pas configurable pour le moment - L’ID de message est généralement défini à un nombre aléatoire à l’émission et semble être ignoré à la réception - Le certificat pourrait éventuellement être utilisé avec HashCash pour « payer » le routage (possibilité future) - **Structure de chiffrement ElGamal :** session tag de 32 octets + clé de session chiffrée ElGamal + charge utile chiffrée AES

**Pour le format ECIES-X25519-AEAD-Ratchet (standard actuel pour les routers):**

Voir [Spécification ECIES](/docs/specs/ecies/) et [Proposition 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Code source:** - `net.i2p.data.i2np.GarlicMessage` - Chiffrement: `net.i2p.crypto.elgamal.ElGamalAESEngine` (déprécié) - Chiffrement moderne: `net.i2p.crypto.ECIES` packages

---

### TunnelData (type 18)

**Objectif:** Un message envoyé depuis la passerelle d’un tunnel ou d’un participant vers le participant suivant ou le point de terminaison. Les données sont de longueur fixe et contiennent des messages I2NP qui sont fragmentés, regroupés par lots, complétés par remplissage et chiffrés.

**Format :**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Structure de la charge utile (1024 octets) :**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Remarques :** - L'ID du message I2NP pour TunnelData est défini sur un nouveau nombre aléatoire à chaque saut - Le format des messages de tunnel (dans les données chiffrées) est spécifié dans [Spécification des messages de tunnel](/docs/specs/implementation/) - Chaque saut déchiffre une couche à l'aide d'AES-256 en mode CBC - L'IV (vecteur d'initialisation) est mis à jour à chaque saut en utilisant les données déchiffrées - La taille totale est exactement de 1,028 octets (4 tunnelId + 1024 data) - C'est l'unité fondamentale du trafic de tunnel - Les messages TunnelData transportent des messages I2NP fragmentés (GarlicMessage, DatabaseStore, etc.)

**Code source:** - `net.i2p.data.i2np.TunnelDataMessage` - Constante: `TunnelDataMessage.DATA_LENGTH = 1024` - Traitement: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (passerelle de tunnel) (Type 19)

**Objectif:** Encapsule un autre message I2NP destiné à être envoyé dans un tunnel, à la passerelle d'entrée du tunnel.

**Format:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Remarques:** - La charge utile est un message I2NP avec un en-tête standard de 16 octets - Utilisé pour injecter des messages dans des tunnels depuis le router local - La passerelle fragmente le message inclus si nécessaire - Après fragmentation, les fragments sont encapsulés dans des messages TunnelData (messages de données de tunnel) - TunnelGateway (type de message « passerelle de tunnel ») n'est jamais envoyé sur le réseau; c'est un type de message interne utilisé avant le traitement du tunnel

**Code source:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Traitement: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (message de données) (Type 20)

**Objectif :** Utilisé par les Garlic Messages (messages Garlic, mécanisme d’agrégation de messages dans I2P) et les Garlic Cloves (sous-messages contenus dans un Garlic Message) pour encapsuler des données arbitraires (généralement des données applicatives chiffrées de bout en bout).

**Format :**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Remarques:** - Ce message ne contient aucune information de routage et ne sera jamais envoyé "non encapsulé" - Uniquement utilisé à l'intérieur de Garlic messages (format de message spécifique à I2P) - Contient généralement des données d'application chiffrées de bout en bout (HTTP, IRC, email, etc.) - Les données sont généralement une charge utile chiffrée ElGamal/AES ou ECIES - La taille maximale pratique est d'environ 61,2 Ko en raison des limites de fragmentation des messages de tunnel

**Code source:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Type 21)

**OBSOLÈTE.** Utilisez VariableTunnelBuild (type 23) ou ShortTunnelBuild (type 25).

**Objectif:** Requête de construction de tunnel de longueur fixe pour 8 sauts.

**Format :**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Notes :** - Depuis la version 0.9.48, peut contenir des BuildRequestRecords ECIES-X25519 (enregistrements de requête de construction). Voir [Création de tunnel ECIES](/docs/specs/implementation/) - Voir [Spécification de création de tunnel](/docs/specs/implementation/) pour plus de détails - L'ID de message I2NP pour ce message doit être défini conformément à la spécification de création de tunnel - Bien que rarement observé sur le réseau actuel (remplacé par VariableTunnelBuild (construction de tunnel variable)), il peut encore être utilisé pour des tunnels très longs et n'a pas été officiellement déprécié - Routers doivent toujours l'implémenter pour des raisons de compatibilité - Le format fixe à 8 enregistrements est peu flexible et gaspille de la bande passante pour les tunnels plus courts

**Code source :** - `net.i2p.data.i2np.TunnelBuildMessage` - Constante : `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (réponse de construction de tunnel) (Type 22)

**DÉPRÉCIÉ.** Utilisez VariableTunnelBuildReply (type 24) ou OutboundTunnelBuildReply (type 26).

**Objectif :** Réponse de construction de tunnel de longueur fixe pour 8 sauts.

**Format :**

Même format que TunnelBuildMessage, avec BuildResponseRecords au lieu de BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Remarques :** - À partir de la version 0.9.48, peut contenir ECIES-X25519 BuildResponseRecords. Voir [Création de tunnel ECIES](/docs/specs/implementation/) - Voir [Spécification de création de tunnel](/docs/specs/implementation/) pour plus de détails - L'ID de message I2NP pour ce message doit être défini conformément à la spécification de création de tunnel - Bien que rarement observé dans le réseau actuel (remplacé par VariableTunnelBuildReply), il peut encore être utilisé pour des tunnels très longs et n'a pas été formellement déprécié - Les Routers doivent encore l'implémenter pour des raisons de compatibilité

**Code source:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Type 23)

**Objectif:** Construction de tunnel à longueur variable de 1 à 8 sauts. Prend en charge les routers ElGamal et ECIES-X25519.

**Format :**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Notes :** - À partir de la 0.9.48, peut contenir des BuildRequestRecords ECIES-X25519 (enregistrements de demande de construction). Voir [Création de Tunnel ECIES](/docs/specs/implementation/) - Introduit dans la version 0.7.12 (2009) du router - Ne doit pas être envoyé aux participants du tunnel antérieurs à la version 0.7.12 - Voir [Spécification de création de tunnel](/docs/specs/implementation/) pour plus de détails - L'ID de message I2NP doit être défini conformément à la spécification de création de tunnel - **Nombre typique d'enregistrements :** 4 (pour un tunnel à 4 sauts) - **Taille totale typique :** 1 + (4 × 528) = 2 113 octets - Ceci est le message standard de construction de tunnel pour les routers ElGamal - Les routers ECIES utilisent généralement ShortTunnelBuild (construction de tunnel courte, type 25) à la place

**Code source:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Type 24)

**Objectif :** Réponse de construction de tunnel de longueur variable pour 1 à 8 sauts. Prend en charge à la fois les routers ElGamal et ECIES-X25519.

**Format:**

Même format que VariableTunnelBuildMessage, avec BuildResponseRecords au lieu de BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Remarques :** - À partir de la 0.9.48, peut contenir des ECIES-X25519 BuildResponseRecords. Voir [Création de tunnel ECIES](/docs/specs/implementation/) - Introduit dans la version 0.7.12 du router (2009) - Ne doit pas être envoyé aux participants du tunnel exécutant une version antérieure à 0.7.12 - Voir [Spécification de création de tunnel](/docs/specs/implementation/) pour plus de détails - L’ID de message I2NP doit être défini conformément à la spécification de création de tunnel - **Nombre typique d’enregistrements :** 4 - **Taille totale typique :** 2 113 octets

**Code source :** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Type 25)

**Objectif :** Messages courts de construction de tunnel pour les routers ECIES-X25519 uniquement. Introduit dans la version d'API 0.9.51 (version 1.5.0, août 2021). C'est le standard actuel pour les constructions de tunnel ECIES.

**Format :**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Remarques :** - Introduit dans la version 0.9.51 du router (version 1.5.0, août 2021) - Ne peut pas être envoyé aux participants du tunnel utilisant une version d’API antérieure à 0.9.51 - Voir [Création de tunnel ECIES](/docs/specs/implementation/) pour la spécification complète - Voir [Proposition 157](/proposals/157-new-tbm/) pour la justification - **Nombre typique d’enregistrements :** 4 - **Taille totale typique :** 1 + (4 × 218) = 873 octets - **Économie de bande passante :** 59 % plus petit que VariableTunnelBuild (873 contre 2,113 octets) - **Gain de performance :** 4 enregistrements courts tiennent dans un seul message de tunnel ; VariableTunnelBuild nécessite 3 messages de tunnel - Il s’agit désormais du format standard de construction de tunnel pour les tunnels ECIES-X25519 purs - Les enregistrements dérivent les clés via HKDF (fonction de dérivation de clés HMAC) au lieu de les inclure explicitement

**Code source :** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Constante : `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (réponse de construction de tunnel sortant) (Type 26)

**But:** Envoyé depuis l'extrémité sortante d'un nouveau tunnel vers l'initiateur. Pour les routers ECIES-X25519 uniquement. Introduit dans la version 0.9.51 de l'API (version 1.5.0, août 2021).

**Format :**

Même format que ShortTunnelBuildMessage, avec ShortBuildResponseRecords au lieu de ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Remarques :** - Introduit dans la version 0.9.51 du router (version 1.5.0, août 2021) - Voir [Création de tunnel ECIES](/docs/specs/implementation/) pour la spécification complète - **Nombre typique d’enregistrements :** 4 - **Taille totale typique :** 873 octets - Cette réponse est envoyée depuis le point d’extrémité sortant (OBEP) vers le créateur du tunnel via le tunnel sortant nouvellement créé - Fournit la confirmation que tous les sauts ont accepté la création du tunnel

**Code source:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Références

### Spécifications officielles

- **[Spécification I2NP](/docs/specs/i2np/)** - Spécification complète du format des messages I2NP
- **[Structures communes](/docs/specs/common-structures/)** - Types de données et structures utilisés dans tout I2P
- **[Création de tunnel](/docs/specs/implementation/)** - Création de tunnel ElGamal (obsolète)
- **[Création de tunnel ECIES](/docs/specs/implementation/)** - Création de tunnel ECIES-X25519 (actuelle)
- **[Message de tunnel](/docs/specs/implementation/)** - Format des messages de tunnel et instructions d'acheminement
- **[Spécification NTCP2](/docs/specs/ntcp2/)** - Protocole de transport TCP
- **[Spécification SSU2](/docs/specs/ssu2/)** - Protocole de transport UDP
- **[Spécification ECIES](/docs/specs/ecies/)** - Chiffrement ECIES-X25519-AEAD-Ratchet
- **[Spécification de cryptographie](/docs/specs/cryptography/)** - Primitives cryptographiques de bas niveau
- **[Spécification I2CP](/docs/specs/i2cp/)** - Spécification du protocole client
- **[Spécification des datagrammes](/docs/api/datagrams/)** - Formats Datagram2 et Datagram3

### Propositions

- **[Proposal 123](/proposals/123-new-netdb-entries/)** - Nouvelles entrées netDB (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)** - Chiffrement ECIES-X25519-AEAD-Ratchet (mécanisme à cliquet AEAD avec X25519)
- **[Proposal 154](/proposals/154-ecies-lookups/)** - Recherche chiffrée dans la base de données
- **[Proposal 156](/proposals/156-ecies-routers/)** - routers ECIES
- **[Proposal 157](/proposals/157-new-tbm/)** - Messages de construction de tunnel plus petits (format court)
- **[Proposal 159](/proposals/159-ssu2/)** - Transport SSU2
- **[Proposal 161](/fr/proposals/161-ri-dest-padding/)** - Bourrage compressible
- **[Proposal 163](/proposals/163-datagram2/)** - Datagram2 et Datagram3
- **[Proposal 167](/proposals/167-service-records/)** - Paramètres d'enregistrement de service LeaseSet
- **[Proposal 168](/proposals/168-tunnel-bandwidth/)** - Paramètres de bande passante de construction de tunnel
- **[Proposal 169](/proposals/169-pq-crypto/)** - Cryptographie hybride post-quantique

### Documentation

- **[Garlic Routing](/docs/overview/garlic-routing/)** (routage Garlic) - Regroupement de messages en couches
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Schéma de chiffrement déprécié
- **[Implémentation du tunnel](/docs/specs/implementation/)** - Fragmentation et traitement
- **[Base de données réseau](/docs/specs/common-structures/)** - Table de hachage distribuée
- **[Transport NTCP2](/docs/specs/ntcp2/)** - Spécification du transport TCP
- **[Transport SSU2](/docs/specs/ssu2/)** - Spécification du transport UDP
- **[Introduction technique](/docs/overview/tech-intro/)** - Aperçu de l’architecture I2P

### Code source

- **[Dépôt Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Implémentation Java officielle
- **[Miroir GitHub](https://github.com/i2p/i2p.i2p)** - Miroir GitHub de Java I2P
- **[Dépôt i2pd](https://github.com/PurpleI2P/i2pd)** - Implémentation C++

### Emplacements clés du code source

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - Implémentations des messages I2NP - `core/java/src/net/i2p/crypto/` - Implémentations cryptographiques - `router/java/src/net/i2p/router/tunnel/` - Traitement du tunnel - `router/java/src/net/i2p/router/transport/` - Implémentations du transport

**Constantes et valeurs:** - `I2NPMessage.MAX_SIZE = 65536` - Taille maximale d’un message I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - Taille standard de l’en-tête - `TunnelDataMessage.DATA_LENGTH = 1024` - Charge utile du message de tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Enregistrement de construction long - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Enregistrement de construction court - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Nombre maximal d’enregistrements par construction

---

## Annexe A : Statistiques du réseau et état actuel

### Composition du réseau (en octobre 2025)

- **Nombre total de routers:** Environ 60 000-70 000 (variable)
- **Routers floodfill:** Environ 500-700 actifs
- **Types de chiffrement:**
  - ECIES-X25519: >95 % des routers
  - ElGamal: <5 % des routers (déprécié, usage hérité uniquement)
- **Adoption des transports:**
  - SSU2: >60 % comme transport principal
  - NTCP2: ~40 % comme transport principal
  - Transports hérités (SSU1, NTCP): 0 % (supprimés)
- **Types de signature:**
  - EdDSA (Ed25519): Très grande majorité
  - ECDSA: Faible pourcentage
  - RSA: Interdit (supprimé)

### Exigences minimales du router

- **Version de l'API:** 0.9.16+ (pour la compatibilité EdDSA avec le réseau)
- **Minimum recommandé:** API 0.9.51+ (constructions de tunnels courts ECIES)
- **Minimum actuel pour les floodfills:** API 0.9.58+ (dépréciation du router ElGamal)
- **Exigence à venir:** Java 17+ (à partir de la version 2.11.0, décembre 2025)

### Exigences de bande passante

- **Minimum :** 128 KBytes/sec (drapeau N ou supérieur) pour le floodfill
- **Recommandé :** 256 KBytes/sec (drapeau O) ou supérieur
- **Exigences pour le floodfill :**
  - Bande passante minimale de 128 KB/sec
  - Temps de fonctionnement stable (>95% recommandé)
  - Faible latence (<500ms vers les pairs)
  - Réussir les tests d’intégrité (temps de file d’attente, retard des tâches)

### Statistiques des tunnels

- **Longueur typique du tunnel :** 3-4 sauts
- **Longueur maximale du tunnel :** 8 sauts (théorique, rarement utilisée)
- **Durée de vie typique du tunnel :** 10 minutes
- **Taux de réussite de construction de tunnel :** >85% pour des routers bien connectés
- **Format des messages de construction de tunnel :**
  - routers ECIES (schéma de chiffrement intégré à courbe elliptique) : ShortTunnelBuild (enregistrements de 218 octets)
  - Tunnels mixtes : VariableTunnelBuild (enregistrements de 528 octets)

### Métriques de performance

- **Temps de construction du tunnel:** 1-3 secondes (typique)
- **Latence de bout en bout:** 0,5-2 secondes (typique, 6-8 sauts au total)
- **Débit:** Limité par la bande passante du tunnel (typiquement 10-50 KB/sec par tunnel)
- **Taille maximale du datagramme:** 10 KB recommandé (61,2 KB maximum théorique)

---

## Annexe B : Fonctionnalités dépréciées et supprimées

### Entièrement supprimé (n'est plus pris en charge)

- **Transport NTCP** - Supprimé dans la version 0.9.50 (mai 2021)
- **Transport SSU v1** - Supprimé de Java I2P dans la version 2.4.0 (décembre 2023)
- **Transport SSU v1** - Supprimé d'i2pd dans la version 2.44.0 (novembre 2022)
- **Types de signature RSA** - Interdits depuis l'API 0.9.28

### Déprécié (pris en charge mais déconseillé)

- **ElGamal routers** - Dépréciés depuis l’API 0.9.58 (mars 2023)
  - Les destinations ElGamal sont toujours prises en charge pour la rétrocompatibilité
  - Les nouveaux routers doivent utiliser ECIES-X25519 exclusivement
- **TunnelBuild (type 21)** - Déprécié au profit de VariableTunnelBuild et ShortTunnelBuild
  - Toujours implémenté pour des tunnels très longs (>8 sauts)
- **TunnelBuildReply (type 22)** - Déprécié au profit de VariableTunnelBuildReply et OutboundTunnelBuildReply
- **Chiffrement ElGamal/AES** - Déprécié au profit d’ECIES-X25519-AEAD-Ratchet
  - Toujours utilisé pour les anciennes destinations
- **BuildRequestRecords ECIES longs (528 octets)** - Dépréciés au profit du format court (218 octets)
  - Toujours utilisés pour des tunnels mixtes avec des sauts ElGamal

### Calendrier de prise en charge des anciennes versions

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Annexe C : Développements futurs

### Cryptographie post-quantique

**Statut :** Bêta à partir de la version 2.10.0 (septembre 2025), deviendra l’option par défaut avec la version 2.11.0 (décembre 2025)

**Implémentation:** - Approche hybride combinant X25519 classique et MLKEM post-quantique (ML-KEM-768) - Rétrocompatible avec l'infrastructure ECIES-X25519 existante - Utilise Signal Double Ratchet (mécanisme à double cliquet de Signal) avec du matériel de clés classique et PQ - Voir [Proposition 169](/proposals/169-pq-crypto/) pour plus de détails

**Plan de migration:** 1. Version 2.10.0 (septembre 2025): Disponible en tant qu’option bêta 2. Version 2.11.0 (décembre 2025): Activé par défaut 3. Versions futures: À terme, obligatoire

### Fonctionnalités prévues

- **Améliorations IPv6** - Meilleure prise en charge d'IPv6 et des mécanismes de transition
- **Régulation de débit par tunnel** - Contrôle fin de la bande passante par tunnel
- **Métriques améliorées** - Meilleure surveillance des performances et des capacités de diagnostic
- **Optimisations des protocoles** - Surcharge réduite et efficacité accrue
- **Sélection floodfill améliorée** - Meilleure distribution de la base de données réseau

### Domaines de recherche

- **Optimisation de la longueur des tunnels** - Longueur de tunnels dynamique basée sur le modèle de menace
- **Bourrage avancé** - Améliorations de la résistance à l'analyse de trafic
- **Nouveaux schémas de chiffrement** - Préparation face aux menaces de l'informatique quantique
- **Contrôle de congestion** - Meilleure gestion de la charge réseau
- **Prise en charge mobile** - Optimisations pour les appareils et réseaux mobiles

---

## Annexe D : Directives de mise en œuvre

### Pour les nouvelles implémentations

**Exigences minimales:** 1. Prendre en charge les fonctionnalités de la version 0.9.51+ de l’API 2. Implémenter le chiffrement ECIES-X25519-AEAD-Ratchet 3. Prendre en charge les transports NTCP2 et SSU2 4. Implémenter les messages ShortTunnelBuild (enregistrements de 218 octets) 5. Prendre en charge les variantes LeaseSet2 (types 3, 5, 7) 6. Utiliser des signatures EdDSA (Ed25519)

**Recommandé:** 1. Prendre en charge la cryptographie hybride post-quantique (à partir de la version 2.11.0) 2. Implémenter des paramètres de bande passante par tunnel 3. Prendre en charge les formats Datagram2 et Datagram3 4. Implémenter les options d’enregistrement de service dans les LeaseSets 5. Suivre les spécifications officielles à /docs/specs/

**Non requis:** 1. Prise en charge du router ElGamal (dépréciée) 2. Prise en charge des transports hérités (SSU1, NTCP) 3. BuildRequestRecords ECIES longs (528 octets pour des tunnels ECIES purs) 4. messages TunnelBuild/TunnelBuildReply (utiliser les variantes Variable ou Short)

### Tests et validation

**Conformité au protocole:** 1. Tester l'interopérabilité avec le router I2P officiel en Java 2. Tester l'interopérabilité avec le router i2pd en C++ 3. Valider les formats de message selon les spécifications 4. Tester les cycles d'établissement/démontage de tunnel 5. Vérifier le chiffrement/déchiffrement avec des vecteurs de test

**Tests de performance:** 1. Mesurer les taux de réussite de la construction des tunnels (devraient être > 85 %) 2. Tester avec différentes longueurs de tunnels (2-8 sauts) 3. Valider la fragmentation et le réassemblage 4. Tester sous charge (tunnels multiples simultanés) 5. Mesurer la latence de bout en bout

**Tests de sécurité:** 1. Vérifier l'implémentation du chiffrement (utiliser des vecteurs de test) 2. Tester la prévention des attaques par rejeu 3. Valider la gestion de l'expiration des messages 4. Tester la robustesse face aux messages malformés 5. Vérifier la génération correcte de nombres aléatoires

### Écueils courants d’implémentation

1. **Formats d'instructions de livraison déroutants** - Garlic clove (élément « gousse » du schéma garlic) vs tunnel message (message de tunnel)
2. **Dérivation de clés incorrecte** - Utilisation de HKDF pour short build records (format court des enregistrements de construction de tunnel)
3. **Gestion de l'ID de message** - Non défini correctement pour les constructions de tunnel
4. **Problèmes de fragmentation** - Non-respect de la limite pratique de 61,2 Ko
5. **Erreurs d'ordre des octets** - Java utilise le big-endian pour tous les entiers
6. **Gestion de l'expiration** - Le format court déborde le 7 février 2106
7. **Génération de somme de contrôle** - Toujours requise même si elle n'est pas vérifiée
