---
title: "Introduction à I2P"
description: "Une introduction moins technique au réseau anonyme I2P"
slug: "intro"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---

## Qu'est-ce qu'I2P ?

Le Invisible Internet Project (I2P) est une couche réseau anonyme qui permet une communication pair-à-pair résistante à la censure. Les connexions anonymes sont obtenues en chiffrant le trafic de l'utilisateur et en l'acheminant à travers un réseau distribué géré par des volontaires du monde entier.

## Fonctionnalités principales

### Anonymity

I2P cache à la fois l'expéditeur et le destinataire des messages. Contrairement aux connexions internet traditionnelles où votre adresse IP est visible par les sites web et les services, I2P utilise plusieurs couches de chiffrement et de routage pour préserver la confidentialité de votre identité.

### Decentralization

Il n'existe aucune autorité centrale dans I2P. Le réseau est maintenu par des bénévoles qui donnent de la bande passante et des ressources informatiques. Cela le rend résistant à la censure et aux points de défaillance uniques.

### Anonymat

Tout le trafic au sein d'I2P est chiffré de bout en bout. Les messages sont chiffrés plusieurs fois lorsqu'ils traversent le réseau, de manière similaire au fonctionnement de Tor mais avec des différences importantes dans l'implémentation.

## How It Works

### Décentralisation

I2P utilise des « tunnels » pour acheminer le trafic. Lorsque vous envoyez ou recevez des données :

1. Votre routeur crée un tunnel sortant (pour l'envoi)
2. Votre routeur crée un tunnel entrant (pour la réception)
3. Les messages sont chiffrés et envoyés à travers plusieurs routeurs
4. Chaque routeur ne connaît que le saut précédent et le suivant, pas le chemin complet

### Chiffrement de bout en bout

I2P améliore le routage en oignon traditionnel avec le « garlic routing » :

- Plusieurs messages peuvent être regroupés ensemble (comme des gousses dans une tête d'ail)
- Cela offre de meilleures performances et un anonymat supplémentaire
- Rend l'analyse de trafic plus difficile

### Network Database

I2P maintient une base de données réseau distribuée contenant :

- Informations du routeur
- Adresses de destination (similaires aux sites web .i2p)
- Données de routage chiffrées

## Common Use Cases

### Tunnels

Hébergez ou visitez des sites web se terminant par `.i2p` - ceux-ci ne sont accessibles que depuis le réseau I2P et offrent de solides garanties d'anonymat tant pour les hébergeurs que pour les visiteurs.

### Routage en Ail

Partagez des fichiers de manière anonyme en utilisant BitTorrent sur I2P. De nombreuses applications de torrent intègrent nativement le support I2P.

### Base de données réseau

Envoyez et recevez des courriels anonymes en utilisant I2P-Bote ou d'autres applications de messagerie conçues pour I2P.

### Messaging

Utilisez IRC, la messagerie instantanée ou d'autres outils de communication de manière privée sur le réseau I2P.

## Getting Started

Prêt à essayer I2P ? Consultez notre [page de téléchargements](/downloads) pour installer I2P sur votre système.

Pour plus de détails techniques, consultez l'[Introduction technique](/docs/overview/tech-intro) ou explorez la [documentation](/docs) complète.

## Comment ça fonctionne

- [Introduction technique](/docs/overview/tech-intro) - Concepts techniques approfondis
- [Modèle de menace](/docs/overview/threat-model) - Comprendre le modèle de sécurité d'I2P
- [Comparaison avec Tor](/docs/overview/comparison) - En quoi I2P diffère de Tor
- [Cryptographie](/docs/specs/cryptography) - Détails sur les algorithmes cryptographiques d'I2P
