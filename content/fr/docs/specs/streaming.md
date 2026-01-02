---
title: "Protocole de streaming"
description: "Transport fiable, de type TCP, utilisé par la plupart des applications I2P"
slug: "streaming"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Aperçu

La bibliothèque de streaming d'I2P fournit une transmission de données fiable, ordonnée et authentifiée au-dessus de la couche de messages non fiable d'I2P — analogue à TCP sur IP. Elle est utilisée par la quasi-totalité des applications I2P interactives, telles que la navigation web, l’IRC, le courrier électronique et le partage de fichiers.

Il assure une transmission fiable, le contrôle de la congestion, la retransmission et le contrôle de flux à travers les tunnels anonymes à haute latence d’I2P. Chaque flux est entièrement chiffré de bout en bout entre les destinations.

---

## Principes fondamentaux de conception

La bibliothèque de streaming implémente une **procédure d’établissement de connexion en une seule phase**, où les indicateurs SYN, ACK et FIN peuvent transporter une charge utile de données dans le même message. Cela minimise les allers-retours dans des environnements à forte latence — une petite transaction HTTP peut s’achever en un seul aller-retour.

Le contrôle de congestion et la retransmission sont inspirés de TCP mais adaptés à l’environnement d’I2P. Les tailles de fenêtre sont basées sur les messages, et non sur les octets, et sont optimisées pour la latence et la surcharge du tunnel. Le protocole prend en charge le démarrage lent, l’évitement de congestion et une temporisation exponentielle, à l’instar de l’algorithme AIMD de TCP.

---

## Architecture

La bibliothèque de streaming fonctionne entre les applications et l’interface I2CP.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Layer</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Responsibility</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Application</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard I2PSocket and I2PServerSocket usage</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection setup, sequencing, retransmission, and flow control</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel creation, routing, and message handling</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2NP / Router Layer</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport through tunnels</td>
    </tr>
  </tbody>
</table>
La plupart des utilisateurs y accèdent via I2PSocketManager, I2PTunnel ou SAMv3. La bibliothèque prend en charge, de manière transparente, la gestion des destinations, l'utilisation des tunnel (chemins de communication I2P) et les retransmissions.

---

## Format du paquet

```
+-----------------------------------------------+
| Send Stream ID (4B) | Receive Stream ID (4B) |
+-----------------------------------------------+
| Sequence Number (4B) | Ack Through (4B)      |
+-----------------------------------------------+
| NACK Count (1B) | optional NACK list (4B each)
+-----------------------------------------------+
| Flags (1B) | Option Size (1B) | Options ...   |
+-----------------------------------------------+
| Payload ...                                  |
```
### Détails de l’en-tête

- **Identifiants de flux**: valeurs sur 32 bits identifiant de manière unique le flux local et le flux distant.
- **Numéro de séquence**: commence à 0 pour SYN, s'incrémente à chaque message.
- **Accusés de réception jusqu’à**: accuse réception de tous les messages jusqu'à N, à l'exception de ceux présents dans la liste NACK (accusé de réception négatif).
- **Drapeaux**: masque de bits contrôlant l'état et le comportement.
- **Options**: liste de longueur variable pour le RTT, le MTU et la négociation de protocole.

### Drapeaux de clé

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Flag</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SYN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection initiation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Acknowledge received packets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FIN</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Graceful close</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RST</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reset connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Sender’s destination included</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SIGNATURE_INCLUDED</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Message signed by sender</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECHO / ECHO_REPLY</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong keepalive</td>
    </tr>
  </tbody>
</table>
---

## Contrôle de flux et fiabilité

Le streaming utilise un **fenêtrage basé sur les messages**, contrairement à l'approche de TCP basée sur les octets. Le nombre de paquets non acquittés autorisés en transit est égal à la taille de fenêtre actuelle (par défaut 128).

### Mécanismes

- **Contrôle de congestion:** démarrage lent et évitement basé sur AIMD (augmentation additive/diminution multiplicative).  
- **Choke/Unchoke:** signalisation de contrôle de flux basée sur l'occupation du tampon.  
- **Retransmission:** calcul du RTO basé sur la RFC 6298 avec temporisation exponentielle.  
- **Filtrage des doublons:** garantit la fiabilité en présence de messages potentiellement réordonnés.

Valeurs de configuration typiques :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxWindowSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Max unacknowledged messages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>maxMessageSize</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1730</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Maximum payload bytes per message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>initialRTO</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial retransmission timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>inactivityTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">90000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Idle connection timeout</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connectTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">300000 ms</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Connection establishment timeout</td>
    </tr>
  </tbody>
</table>
---

## Établissement de la connexion

1. **Initiateur** envoie un SYN (facultativement avec charge utile et FROM_INCLUDED).  
2. **Répondeur** répond avec SYN+ACK (peut inclure une charge utile).  
3. **Initiateur** envoie l’ACK final confirmant l’établissement.

Les charges utiles initiales facultatives permettent la transmission de données avant l'achèvement complet du handshake (phase de négociation initiale).

---

## Détails de l'implémentation

### Retransmission et délai d'expiration

L'algorithme de retransmission suit la **RFC 6298**.   - **RTO initiale:** 9s   - **RTO min:** 100ms   - **RTO max:** 45s   - **Alpha:** 0.125   - **Beta:** 0.25

### Partage du bloc de contrôle

Les connexions récentes avec le même pair réutilisent les données de RTT (temps aller-retour) et de fenêtre pour une montée en régime plus rapide, évitant la latence de “démarrage à froid”. Les blocs de contrôle expirent après plusieurs minutes.

### MTU et fragmentation

- MTU par défaut : **1730 octets** (suffit pour deux messages I2NP).  
- Destinations ECIES (schéma de chiffrement intégré aux courbes elliptiques) : **1812 octets** (surcharge réduite).  
- MTU minimale prise en charge : 512 octets.

La taille de la charge utile exclut l’en-tête de streaming minimal de 22 octets.

---

## Historique des versions

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol numbers defined in I2CP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Variable-length signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ed25519 signature support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ping/Pong payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">FROM_INCLUDED not required in RESET</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.36</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Protocol enforcement enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">OFFLINE_SIGNATURE support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bob’s hash added to NACK field in SYN</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-Quantum hybrid encryption (experimental)</td>
    </tr>
  </tbody>
</table>
---

## Utilisation au niveau applicatif

### Exemple Java

```java
Properties props = new Properties();
props.setProperty("i2p.streaming.maxWindowSize", "512");
I2PSocketManager mgr = I2PSocketManagerFactory.createManager(props);

I2PSocket socket = mgr.connect(destination);
InputStream in = socket.getInputStream();
OutputStream out = socket.getOutputStream();
```
### Prise en charge de SAMv3 et i2pd

- **SAMv3**: Fournit les modes STREAM et DATAGRAM pour les clients non-Java.  
- **i2pd**: Expose des paramètres de streaming identiques via des options du fichier de configuration (p. ex. `i2p.streaming.maxWindowSize`, `profile`, etc)

---

## Choisir entre streaming et datagrammes

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Use Case</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP, IRC, Email</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Requires reliability</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Repliable Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Single request/response</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Telemetry, Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Raw Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Best-effort acceptable</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P2P DHT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">High connection churn</td>
    </tr>
  </tbody>
</table>
---

## Sécurité et avenir post-quantique

Les sessions de streaming sont chiffrées de bout en bout au niveau de la couche I2CP. Le chiffrement hybride post-quantique (ML-KEM + X25519) est pris en charge à titre expérimental dans la version 2.10.0, mais il est désactivé par défaut.

---

## Références

- [Aperçu de l’API de Streaming](/docs/specs/streaming/)  
- [Spécification du protocole Streaming](/docs/specs/streaming/)  
- [Spécification I2CP](/docs/specs/i2cp/)  
- [Proposition 144 : Calculs de MTU pour le Streaming](/proposals/144-ecies-x25519-aead-ratchet/)  
- [Notes de version d’I2P 2.10.0](/fr/blog/2025/09/08/i2p-2.10.0-release/)
