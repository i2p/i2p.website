---
title: "Intégrer I2P dans votre application"
description: "Guide pratique mis à jour pour intégrer un routeur I2P à votre application de manière responsable"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Intégrer I2P dans votre application est un moyen puissant d'embarquer les utilisateurs — mais seulement si le router est configuré de manière responsable.

## 1. Coordonner avec les équipes de routeurs

- Contactez les mainteneurs de **Java I2P** et **i2pd** avant de les intégrer. Ils peuvent examiner vos paramètres par défaut et signaler les problèmes de compatibilité.
- Choisissez l'implémentation du router qui correspond à votre pile technologique :
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Autres langages** → intégrez un router et connectez-le en utilisant [SAM v3](/docs/api/samv3/) ou [I2CP](/docs/specs/i2cp/)
- Vérifiez les conditions de redistribution pour les binaires du router et les dépendances (environnement d'exécution Java, ICU, etc.).

## 2. Valeurs par défaut de configuration recommandées

Visez à "contribuer plus que vous ne consommez." Les paramètres par défaut modernes privilégient la santé et la stabilité du réseau.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Les tunnels participants restent essentiels

Ne désactivez **pas** les tunnels de participation.

1. Les routeurs qui ne relaient pas de trafic ont eux-mêmes de moins bonnes performances.
2. Le réseau dépend du partage volontaire de capacité.
3. Le trafic de couverture (trafic relayé) améliore l'anonymat.

**Minimums officiels :** - Bande passante partagée : ≥ 12 Ko/s   - Activation automatique floodfill : ≥ 128 Ko/s   - Recommandé : 2 tunnels entrants / 2 tunnels sortants (par défaut Java I2P)

## 3. Persistance et Reseeding

Les répertoires d'état persistants (`netDb/`, profils, certificats) doivent être préservés entre les exécutions.

Sans persistance, vos utilisateurs déclencheront des réamorçages (reseeds) à chaque démarrage, ce qui dégradera les performances et augmentera la charge sur les serveurs de réamorçage.

Si la persistance est impossible (par exemple, conteneurs ou installations éphémères) :

1. Intégrer **1 000 à 2 000 router infos** dans le programme d'installation.  
2. Exploiter un ou plusieurs serveurs de reseed personnalisés pour décharger les serveurs publics.

Variables de configuration : - Répertoire de base : `i2p.dir.base` - Répertoire de configuration : `i2p.dir.config` - Inclut `certificates/` pour le reseeding.

## 4. Sécurité et exposition

- Gardez la console du routeur (`127.0.0.1:7657`) en local uniquement.  
- Utilisez HTTPS si vous exposez l'interface utilisateur en externe.  
- Désactivez SAM/I2CP externe sauf si nécessaire.  
- Vérifiez les plugins inclus—distribuez uniquement ce que votre application prend en charge.  
- Incluez toujours une authentification pour l'accès distant à la console.

**Fonctionnalités de sécurité introduites depuis la version 2.5.0 :** - Isolation du netDb entre les applications (2.4.0+)   - Atténuation des attaques DoS et listes de blocage Tor (2.5.1)   - Résistance au sondage NTCP2 (2.9.0)   - Améliorations de la sélection des routeurs floodfill (2.6.0+)

## 5. APIs prises en charge (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Toute la documentation officielle se trouve sous `/docs/api/` — l'ancien chemin `/spec/samv3/` n'existe **pas**.

## 6. Réseau et Ports

Ports par défaut typiques : - 4444 – Proxy HTTP   - 4445 – Proxy HTTPS   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Console du routeur   - 7658 – Site I2P local   - 6668 – Proxy IRC   - 9000–31000 – Port routeur aléatoire (UDP/TCP entrant)

Les routeurs sélectionnent un port entrant aléatoire lors de la première exécution. Le transfert de port améliore les performances, mais UPnP peut gérer cela automatiquement.

## 7. Changements récents (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Expérience utilisateur et tests

- Communiquer ce que fait I2P et pourquoi la bande passante est partagée.
- Fournir des diagnostics du router (bande passante, tunnels, statut de reseed).
- Tester les bundles sur Windows, macOS et Linux (RAM faible incluse).
- Vérifier l'interopérabilité avec les pairs **Java I2P** et **i2pd**.
- Tester la récupération après des coupures réseau et des sorties non gracieuses.

## 9. Ressources de la Communauté

- Forum : [i2pforum.net](https://i2pforum.net) ou `http://i2pforum.i2p` à l'intérieur d'I2P.  
- Code : [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (réseau Irc2P) : `#i2p-dev`, `#i2pd`.  
  - `#i2papps` non vérifié ; pourrait ne pas exister.  
  - Précisez quel réseau (Irc2P vs ilita.i2p) héberge votre canal.

Intégrer de manière responsable signifie trouver un équilibre entre l'expérience utilisateur, les performances et la contribution au réseau. Utilisez ces valeurs par défaut, restez synchronisé avec les mainteneurs du router, et testez sous charge réelle avant la publication.
