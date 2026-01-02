---
title: "Clients I2P alternatifs"
description: "Implémentations client I2P maintenues par la communauté (mises à jour pour 2025)"
slug: "alternative-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

L'implémentation principale du client I2P utilise **Java**. Si vous ne pouvez pas ou préférez ne pas utiliser Java sur un système particulier, il existe des implémentations alternatives du client I2P développées et maintenues par des membres de la communauté. Ces programmes fournissent les mêmes fonctionnalités de base en utilisant différents langages de programmation ou approches.

---

## Tableau de comparaison

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Client</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Language</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Maturity</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Actively Maintained</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Suitable For</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes (official)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">General users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard full router; includes console, plugins, and tools</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>i2pd</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">C++</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-resource systems, servers</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lightweight, fully compatible with Java I2P, includes web console</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Go-I2P</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Go</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚙️ In development</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Developers, testing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Early-stage Go implementation; not yet production ready</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P+</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable (fork)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Advanced users</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enhanced Java I2P fork with UI and performance improvements</td>
    </tr>
  </tbody>
</table>
---

## i2pd (C++)

**Site web :** [https://i2pd.website](https://i2pd.website)

**Description :** i2pd (le *I2P Daemon*) est un client I2P complet implémenté en C++. Il est stable pour une utilisation en production depuis de nombreuses années (depuis environ 2016) et est activement maintenu par la communauté. i2pd implémente entièrement les protocoles réseau et les API I2P, le rendant totalement compatible avec le réseau I2P Java. Ce router C++ est souvent utilisé comme alternative légère sur les systèmes où l'environnement d'exécution Java n'est pas disponible ou souhaité. i2pd inclut une console web intégrée pour la configuration et la surveillance. Il est multiplateforme et disponible dans de nombreux formats de paquets — il existe même une version Android d'i2pd (par exemple, via F-Droid).

---

## Go-I2P (Go)

**Dépôt :** [https://github.com/go-i2p/go-i2p](https://github.com/go-i2p/go-i2p)

**Description :** Go-I2P est un client I2P écrit dans le langage de programmation Go. Il s'agit d'une implémentation indépendante du router I2P, visant à tirer parti de l'efficacité et de la portabilité de Go. Le projet est en développement actif, mais il est encore à un stade précoce et n'est pas encore complet en termes de fonctionnalités. En 2025, Go-I2P est considéré comme expérimental — il fait l'objet d'un travail actif par les développeurs de la communauté, mais il n'est pas recommandé pour une utilisation en production tant qu'il n'aura pas davantage mûri. L'objectif de Go-I2P est de fournir un router I2P moderne et léger avec une compatibilité totale avec le réseau I2P une fois le développement terminé.

---

## I2P+ (fork Java)

**Site web :** [https://i2pplus.github.io](https://i2pplus.github.io)

**Description :** I2P+ est un fork maintenu par la communauté du client Java I2P standard. Il ne s'agit pas d'une réimplémentation dans un nouveau langage, mais plutôt d'une version améliorée du router Java avec des fonctionnalités et optimisations supplémentaires. I2P+ se concentre sur l'amélioration de l'expérience utilisateur et de meilleures performances tout en restant totalement compatible avec le réseau I2P officiel. Il introduit une interface de console web rafraîchie, des options de configuration plus conviviales et diverses optimisations (par exemple, performances torrent améliorées et meilleure gestion des pairs réseau, en particulier pour les routers derrière des pare-feu). I2P+ nécessite un environnement Java tout comme le logiciel I2P officiel, ce n'est donc pas une solution pour les environnements non-Java. Cependant, pour les utilisateurs qui disposent de Java et souhaitent une version alternative avec des capacités supplémentaires, I2P+ offre une option intéressante. Ce fork est maintenu à jour avec les versions I2P en amont (sa numérotation de version ajoutant un « + ») et peut être obtenu depuis le site web du projet.
