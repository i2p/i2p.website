---
title: "Recherche Académique"
description: "Informations et directives pour la recherche académique sur le réseau I2P"
layout: "research"
aliases:
  - /en/research
  - /en/research/index
  - /en/research/questions
---

<div id="intro"></div>

## Recherche Académique I2P

Il existe une grande communauté de recherche qui examine un large éventail d'aspects de l'anonymat. Pour que les réseaux d'anonymat continuent à s'améliorer, nous estimons qu'il est essentiel de comprendre les problèmes rencontrés. La recherche sur le réseau I2P en est encore à ses débuts, la majeure partie des travaux de recherche jusqu'à présent étant concentrée sur d'autres réseaux d'anonymat. Cela représente une opportunité unique pour des contributions de recherche originales.

<div id="notes"></div>

## Notes aux Chercheurs

### Priorités de la Recherche Défensive

Nous accueillons favorablement la recherche qui nous aide à renforcer le réseau et à améliorer sa sécurité. Les tests qui renforcent l'infrastructure I2P sont encouragés et appréciés.

### Directives de Communication de la Recherche

Nous encourageons vivement les chercheurs à communiquer leurs idées de recherche dès le début avec l'équipe de développement. Cela aide à :

- Éviter un éventuel chevauchement avec des projets existants
- Minimiser le potentiel de nuire au réseau
- Coordonner les efforts de test et de collecte de données
- Veiller à ce que la recherche soit alignée sur les objectifs du réseau

<div id="ethics"></div>

## Éthique de la Recherche & Directives de Test

### Principes Généraux

Lors de la conduite de recherches sur I2P, veuillez prendre en considération les éléments suivants :

1. **Évaluer les bénéfices de la recherche par rapport aux risques** - Considérez si les bénéfices potentiels de votre recherche l'emportent sur les risques pour le réseau ou ses utilisateurs
2. **Privilégier le réseau de test par rapport au réseau en direct** - Utilisez autant que possible la configuration du réseau de test de I2P
3. **Collecter le minimum de données nécessaire** - Ne collectez que le minimum de données nécessaire pour votre recherche
4. **Veiller à ce que les données publiées respectent la vie privée des utilisateurs** - Toute donnée publiée doit être anonymisée et respecter la vie privée des utilisateurs

### Méthodes de Test du Réseau

Pour les chercheurs qui ont besoin de tester sur I2P :

- **Utilisez la configuration du réseau de test** - I2P peut être configuré pour fonctionner sur un réseau de test isolé
- **Utilisez le mode MultiRouter** - Exécutez plusieurs instances de routeur sur une seule machine pour les tests
- **Configurez la famille de routeurs** - Rendez vos routeurs de recherche identifiables en les configurant comme une famille de routeurs

### Pratiques Recommandées

- **Contactez l'équipe I2P avant les tests sur le réseau en direct** - Contactez-nous à research@i2p.net avant de réaliser des tests sur le réseau en direct
- **Utilisez la configuration de la famille de routeurs** - Cela rend vos routeurs de recherche transparents pour le réseau
- **Prévenez une éventuelle interférence sur le réseau** - Concevez vos tests pour minimiser tout impact négatif sur les utilisateurs réguliers

<div id="questions"></div>

## Questions de Recherche Ouvertes

La communauté I2P a identifié plusieurs domaines où la recherche serait particulièrement précieuse :

### Base de Données du Réseau

**Floodfills :**
- Existe-t-il d'autres moyens de réduire les attaques par force brute sur le réseau via un contrôle significatif du floodfill ?
- Existe-t-il un moyen de détecter, de signaler et de potentiellement retirer les 'mauvais floodfills' sans réellement avoir besoin de se fier à une forme d'autorité centrale ?

### Transports

- Comment les stratégies de retransmission de paquets et les délais d'attente peuvent-ils être améliorés ?
- Existe-t-il un moyen pour I2P d'obfusquer les paquets et de réduire plus efficacement l'analyse du trafic ?

### Tunnels et Destinations

**Sélection des Pairs :**
- Existe-t-il un moyen pour que I2P puisse effectuer la sélection des pairs de manière plus efficace ou sécurisée ?
- L'utilisation de geoip pour prioriser les pairs voisins aurait-elle un impact négatif sur l'anonymat ?

**Tunnels Unidirectionnels :**
- Quels sont les avantages des tunnels unidirectionnels par rapport aux tunnels bidirectionnels ?
- Quels sont les compromis entre les tunnels unidirectionnels et bidirectionnels ?

**Multihoming :**
- Quelle est l'efficacité du multihoming en matière d'équilibrage de charge ?
- Quelle est son évolutivité ?
- Que se passe-t-il lorsque plus de routeurs hébergent la même Destination ?
- Quels sont les compromis en termes d'anonymat ?

### Routage des Messages

- Dans quelle mesure l'efficacité des attaques par synchronisation est-elle réduite par la fragmentation et le mélange des messages ?
- Quelles stratégies de mélange pourraient bénéficier à I2P ?
- Comment des techniques à haute latence peuvent-elles être efficacement employées au sein ou à côté de notre réseau à faible latence ?

### Anonymat

- Dans quelle mesure l'empreinte numérique du navigateur affecte-t-elle l'anonymat des utilisateurs I2P ?
- Le développement d'un ensemble logiciel pour navigateur bénéficierait-il aux utilisateurs moyens ?

### Relatif au Réseau

- Quel est l'impact global sur le réseau créé par les 'utilisateurs gourmands' ?
- Des étapes supplémentaires pour encourager la participation en bande passante seraient-elles précieuses ?

<div id="contact"></div>

## Contact

Pour les demandes de recherche, opportunités de collaboration ou pour discuter de vos plans de recherche, veuillez nous contacter à :

**Email :** research@i2p.net

Nous nous réjouissons de travailler avec la communauté de recherche pour améliorer le réseau I2P !