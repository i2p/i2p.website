---
title: "v3dgsend"
description: "Utilitaire CLI pour envoyer des datagrammes I2P via SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Statut : Ceci est une référence concise pour l'utilitaire `v3dgsend`. Il complète la documentation de l'[API Datagram](/docs/api/datagrams/) et de [SAM v3](/docs/api/samv3/).

## Aperçu

`v3dgsend` est un utilitaire en ligne de commande pour envoyer des datagrammes I2P via l'interface SAMv3. Il est utile pour tester la livraison de datagrammes, prototyper des services et vérifier le comportement de bout en bout sans avoir à écrire un client complet.

Utilisations typiques :

- Test de fumée de l'accessibilité des datagrammes vers une Destination
- Validation de la configuration du pare-feu et du carnet d'adresses
- Expérimentation avec des datagrammes bruts vs. signés (auxquels on peut répondre)

## Utilisation

L'invocation de base varie selon la plateforme et l'empaquetage. Les options courantes incluent :

- Destination : Destination en base64 ou nom `.i2p`
- Protocol : raw (PROTOCOL 18) ou signed (PROTOCOL 17)
- Payload : chaîne inline ou fichier en entrée

Consultez l'empaquetage de votre distribution ou la sortie de `--help` pour les options exactes.

## Voir aussi

- [API Datagram](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Bibliothèque Streaming](/docs/api/streaming/) (alternative aux datagrammes)
