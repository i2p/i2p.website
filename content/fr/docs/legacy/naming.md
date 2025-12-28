---
title: "Discussion sur le nommage"
description: "Débat historique sur le modèle de nommage d’I2P et les raisons pour lesquelles les schémas de type DNS global ont été rejetés"
slug: "naming"
layout: "single"
lastUpdated: "2025-02"
accurateFor: "historical"
reviewStatus: "needs-review"
---

> **Contexte:** Cette page archive des débats de longue haleine datant des débuts de la conception d'I2P. Elle explique pourquoi le projet a privilégié des carnets d'adresses locaux de confiance plutôt que des résolutions de type DNS ou des registres fondés sur un vote majoritaire. Pour des recommandations d'utilisation à jour, voir la [documentation sur le nommage](/docs/overview/naming/).

## Alternatives écartées

Les objectifs de sécurité d’I2P excluent les schémas de nommage familiers:

- **Résolution de type DNS.** N’importe quel résolveur sur la chaîne de résolution pourrait usurper ou censurer les réponses. Même avec DNSSEC, des bureaux d’enregistrement ou des autorités de certification compromis restent un point de défaillance unique. Dans I2P, les destinations *sont* des clés publiques — détourner une requête de résolution compromettrait entièrement une identité.
- **Nommage par vote.** Un adversaire peut créer un nombre illimité d’identités (une attaque Sybil) et « gagner » des votes pour des noms populaires. Les contre-mesures basées sur la preuve de travail augmentent le coût, mais introduisent une lourde surcharge de coordination.

Au lieu de cela, I2P maintient délibérément la résolution de noms au-dessus de la couche de transport. La bibliothèque de nommage incluse offre une interface de fournisseur de services afin que des mécanismes alternatifs puissent coexister—les utilisateurs décident à quels carnets d’adresses ou jump services (services de saut aidant à résoudre les adresses) ils font confiance.

## Noms locaux vs noms globaux (jrandom, 2005)

- Dans I2P, les noms sont **localement uniques mais lisibles par des humains**. Votre `boss.i2p` peut ne pas correspondre au `boss.i2p` de quelqu’un d’autre, et c’est voulu.
- Si un acteur malveillant vous amenait à modifier la destination (identifiant d’un service dans I2P) associée à un nom, il détournerait effectivement un service. Le fait de ne pas imposer l’unicité globale empêche cette catégorie d’attaque.
- Traitez les noms comme des signets ou des pseudos de messagerie instantanée — vous choisissez les destinations auxquelles faire confiance en vous abonnant à des carnets d’adresses spécifiques ou en ajoutant des clés manuellement.

## Objections courantes et réponses (zzz)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Concern</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Response</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Downloading hosts.txt is inefficient.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">At ~400&nbsp;KB for ~800 hosts the bandwidth impact is minor (~10&nbsp;B/s if refreshed twice daily). ETags already avoid unnecessary transfers. Alternate formats (for example <code>recenthosts.cgi</code>) can deliver only new entries.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“It won’t scale.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A hosts.txt entry is ~500&nbsp;bytes; storing thousands locally is practical. Real-time lookups would dramatically slow browsing.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Requires trust and manual setup.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">True—and intentional. Users must choose address book providers they trust. Trust is not binary; forcing configuration encourages users to think about it.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Why not just use DNS?”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DNS depends on short TTLs and can be hijacked mid-path. I2P destinations are immutable public keys, so DNS semantics map poorly.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Subscriptions rely on specific servers.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscriptions are decentralised—you can add multiple providers or run your own. Completely decentralised systems struggle with conflict resolution and hijacking.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>“Jump services and hosts.txt feel awkward.”</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">They are pragmatic trade-offs. Jump services provide just-in-time lookups; subscriptions keep a local cache for performance.</td>
    </tr>
  </tbody>
</table>
## Idées d’efficacité abordées

- Servir des mises à jour incrémentielles (uniquement les destinations ajoutées depuis la dernière récupération).
- Proposer des flux supplémentaires (`recenthosts.cgi`) en complément des fichiers hosts complets.
- Explorer des outils scriptables (par exemple, `i2host.i2p`) pour fusionner des flux ou filtrer par niveaux de confiance.

## Points clés

- La sécurité prime sur le consensus global : des carnets d'adresses gérés localement minimisent le risque d'usurpation.
- Plusieurs approches de nommage peuvent coexister via l'API de nommage—les utilisateurs décident à quoi faire confiance.
- Un nommage global entièrement décentralisé reste un problème de recherche ouvert ; les compromis entre la sécurité, la mémorisation humaine et l'unicité globale reflètent toujours le [triangle de Zooko](https://zooko.com/distnames.html).

## Références

- [Documentation sur la résolution de noms](/docs/overview/naming/)
- [“Noms : décentralisés, sécurisés, compréhensibles pour l’humain : choisissez-en deux” de Zooko](https://zooko.com/distnames.html)
- Exemple de flux incrémentiel: [stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
