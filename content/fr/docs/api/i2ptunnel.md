---
title: "I2PTunnel"
description: "Outil pour interagir avec I2P et fournir des services sur le réseau"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

I2PTunnel est un composant central d'I2P permettant d'interagir avec le réseau I2P et d'y fournir des services. Il permet aux applications basées sur TCP et au streaming multimédia de fonctionner de manière anonyme grâce à l'abstraction des tunnels. La destination d'un tunnel peut être définie par un [nom d'hôte](/docs/overview/naming), un [Base32](/docs/overview/naming#base32), ou une clé de destination complète.

Chaque tunnel établi écoute localement (par exemple, `localhost:port`) et se connecte en interne aux destinations I2P. Pour héberger un service, créez un tunnel pointant vers l'IP et le port souhaités. Une clé de destination I2P correspondante est générée, permettant au service de devenir accessible globalement au sein du réseau I2P. L'interface web I2PTunnel est disponible à l'adresse [I2P Router Tunnel Manager](http://localhost:7657/i2ptunnel/).

---

## Services par défaut

### Tunnel serveur

- **I2P Webserver** – Un tunnel vers un serveur web Jetty sur [localhost:7658](http://localhost:7658) pour héberger facilement sur I2P.  
  - **Unix:** `$HOME/.i2p/eepsite/docroot`  
  - **Windows:** `%LOCALAPPDATA%\I2P\I2P Site\docroot` → `C:\Users\<username>\AppData\Local\I2P\I2P Site\docroot`

### Tunnels clients

- **I2P HTTP Proxy** – `localhost:4444` – Utilisé pour naviguer sur I2P et Internet via des outproxies.  
- **I2P HTTPS Proxy** – `localhost:4445` – Variante sécurisée du proxy HTTP.  
- **Irc2P** – `localhost:6668` – Tunnel par défaut vers le réseau IRC anonyme.  
- **Git SSH (gitssh.idk.i2p)** – `localhost:7670` – Tunnel client pour l'accès SSH aux dépôts.  
- **Postman SMTP** – `localhost:7659` – Tunnel client pour le courrier sortant.  
- **Postman POP3** – `localhost:7660` – Tunnel client pour le courrier entrant.

> Note : Seul le serveur web I2P est un **tunnel serveur** par défaut ; tous les autres sont des tunnels clients se connectant à des services I2P externes.

---

## Configuration

La spécification de configuration I2PTunnel est documentée sur [/spec/configuration](/docs/specs/configuration/).

---

## Modes Client

### Standard

Ouvre un port TCP local qui se connecte à un service sur une destination I2P. Prend en charge plusieurs entrées de destination séparées par des virgules pour la redondance.

### HTTP

Un tunnel proxy pour les requêtes HTTP/HTTPS. Prend en charge les proxies sortants locaux et distants, le filtrage d'en-têtes, la mise en cache, l'authentification et la compression transparente.

**Protections de la vie privée :**   - Supprime les en-têtes : `Accept-*`, `Referer`, `Via`, `From`   - Remplace les en-têtes d'hôte par des destinations Base32   - Applique la suppression hop-by-hop conforme à la RFC   - Ajoute la prise en charge de la décompression transparente   - Fournit des pages d'erreur internes et des réponses localisées

**Comportement de compression :**   - Les requêtes peuvent utiliser l'en-tête personnalisé `X-Accept-Encoding: x-i2p-gzip`   - Les réponses avec `Content-Encoding: x-i2p-gzip` sont décompressées de manière transparente   - La compression est évaluée selon le type MIME et la longueur de la réponse pour plus d'efficacité

**Persistance (nouveauté depuis la version 2.5.0) :**   HTTP Keepalive et les connexions persistantes sont désormais pris en charge pour les services hébergés sur I2P via le Hidden Services Manager. Cela réduit la latence et la surcharge de connexion, mais n'active pas encore les sockets persistants entièrement conformes à la RFC 2616 sur tous les sauts.

**Pipelining :**   Reste non pris en charge et inutile ; les navigateurs modernes l'ont abandonné.

**Comportement du User-Agent :**   - **Outproxy :** Utilise un User-Agent Firefox ESR actuel.   - **Interne :** `MYOB/6.66 (AN/ON)` pour cohérence de l'anonymat.

### Client IRC

Se connecte aux serveurs IRC basés sur I2P. Autorise un sous-ensemble sécurisé de commandes tout en filtrant les identifiants pour protéger la vie privée.

### SOCKS 4/4a/5

Fournit la capacité de proxy SOCKS pour les connexions TCP. UDP reste non implémenté dans Java I2P (uniquement dans i2pd).

### CONNECT

Implémente la tunnelisation HTTP `CONNECT` pour les connexions SSL/TLS.

### Streamr

Active la diffusion en continu de style UDP via une encapsulation basée sur TCP. Prend en charge la diffusion multimédia lorsqu'il est associé à un tunnel serveur Streamr correspondant.

![Diagramme I2PTunnel Streamr](/images/I2PTunnel-streamr.png)

---

## Modes du serveur

### Serveur Standard

Crée une destination TCP mappée vers une IP:port locale.

### Serveur HTTP

Crée une destination qui s'interface avec un serveur web local. Prend en charge la compression (`x-i2p-gzip`), la suppression des en-têtes et les protections DDoS. Bénéficie désormais de la **prise en charge des connexions persistantes** (v2.5.0+) et de **l'optimisation du pool de threads** (v2.7.0–2.9.0).

### HTTP Bidirectionnel

**Obsolète** – Toujours fonctionnel mais déconseillé. Agit à la fois comme serveur et client HTTP sans outproxying. Principalement utilisé pour les tests de diagnostic en boucle locale.

### Serveur IRC

Crée une destination filtrée pour les services IRC, en transmettant les clés de destination du client comme noms d'hôte.

### Serveur Streamr

Se couple avec un tunnel client Streamr pour gérer les flux de données de type UDP sur I2P.

---

## Nouvelles fonctionnalités (2.4.0–2.10.0)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Summary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Keepalive/Persistent Connections</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP tunnels now support persistent sockets for I2P-hosted services, improving performance.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Thread Pooling Optimization</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0-2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduced CPU overhead and latency by improving thread management.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-Quantum Encryption (ML-KEM)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Optional hybrid X25519+ML-KEM encryption to resist future quantum attacks.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>NetDB Segmentation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Isolates I2PTunnel contexts for improved security and privacy.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Removal / SSU2 Adoption</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.4.0-2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Upgraded transport layer; transparent to users.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor Blocking</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Prevents inefficient and unstable I2P-over-Tor routing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Browser Proxy (Proposal 166)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced identity-aware proxy mode; details pending confirmation.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 Requirement (upcoming)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.11.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Future release will require Java 17+.</td>
    </tr>
  </tbody>
</table>
---

## Fonctionnalités de sécurité

- **Suppression d'en-têtes** pour l'anonymat (Accept, Referer, From, Via)
- **Randomisation du User-Agent** selon l'in/outproxy
- **Limitation du taux de POST** et **protection Slowloris**
- **Limitation des connexions** dans les sous-systèmes de streaming
- **Gestion de la congestion réseau** au niveau de la couche tunnel
- **Isolation du NetDB** empêchant les fuites inter-applications

---

## Détails techniques

- Taille par défaut de la clé de destination : 516 octets (peut être dépassée pour les certificats LS2 étendus)
- Adresses Base32 : `{52–56+ chars}.b32.i2p`
- Les tunnels serveur restent compatibles avec Java I2P et i2pd
- Fonctionnalité dépréciée : `httpbidirserver` uniquement ; aucune suppression depuis 0.9.59
- Ports par défaut et racines de documents vérifiés corrects pour toutes les plateformes

---

## Résumé

I2PTunnel reste la colonne vertébrale de l'intégration des applications avec I2P. Entre les versions 0.9.59 et 2.10.0, il a bénéficié de la prise en charge des connexions persistantes, du chiffrement post-quantique et d'améliorations majeures du threading. La plupart des configurations restent compatibles, mais les développeurs doivent vérifier leurs paramètres pour garantir la conformité avec les valeurs par défaut modernes de transport et de sécurité.
