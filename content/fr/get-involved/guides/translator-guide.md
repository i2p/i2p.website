---
title: "Guide de Traduction"
description: "Aidez à rendre I2P accessible aux utilisateurs du monde entier en traduisant la console du routeur et le site Web"
date: 2025-01-15
layout: "single"
type: "docs"
---

## Vue d'ensemble

Aidez à rendre I2P accessible aux utilisateurs du monde entier en traduisant la console du routeur I2P et le site Web dans votre langue. La traduction est un processus continu, et les contributions de toute taille sont précieuses.

## Plateforme de Traduction

Nous utilisons **Transifex** pour toutes les traductions I2P. C'est la méthode la plus simple et la plus recommandée pour les traducteurs novices comme expérimentés.

### Commencer avec Transifex

1. **Créez un compte** sur [Transifex](https://www.transifex.com/)
2. **Rejoignez le projet I2P** : [I2P sur Transifex](https://explore.transifex.com/otf/I2P/)
3. **Demandez à rejoindre** votre équipe de langue (ou demandez une nouvelle langue si elle n'est pas listée)
4. **Commencez à traduire** une fois approuvé

### Pourquoi Transifex?

- **Interface conviviale** - Aucune connaissance technique requise
- **Mémoire de traduction** - Suggestion de traductions basées sur les travaux précédents
- **Collaboration** - Travaillez avec d'autres traducteurs dans votre langue
- **Contrôle qualité** - Processus de révision garantissant l'exactitude
- **Mises à jour automatiques** - Les changements se synchronisent avec l'équipe de développement

## Que Traduire

### Console du Routeur (Priorité)

La console du routeur I2P est l'interface principale avec laquelle les utilisateurs interagissent lors de l'utilisation d'I2P. Sa traduction a l'impact le plus immédiat sur l'expérience utilisateur.

**Principaux domaines à traduire :**

- **Interface principale** - Navigation, menus, boutons, messages d'état
- **Pages de configuration** - Descriptions des réglages et options
- **Documentation d'aide** - Fichiers d'aide intégrés et info-bulles
- **Actualités et mises à jour** - Flux d'actualités initial affiché aux utilisateurs
- **Messages d'erreur** - Messages d'erreur et d'avertissement destinés aux utilisateurs
- **Configurations de proxy** - Pages de configuration HTTP, SOCKS et tunnels

Toutes les traductions de la console du routeur sont gérées via Transifex au format `.po` (gettext).

## Directives de Traduction

### Style et Ton

- **Clair et concis** - I2P traite des concepts techniques; gardez les traductions simples
- **Terminologie cohérente** - Utilisez les mêmes termes partout (vérifiez la mémoire de traduction)
- **Formel vs informel** - Suivez les conventions pour votre langue
- **Préserver le formatage** - Gardez intacts les espaces réservés comme `{0}`, `%s`, `<b>balises</b>`

### Considérations Techniques

- **Encodage** - Utilisez toujours l'encodage UTF-8
- **Espaces réservés** - Ne traduisez pas les espaces réservés de variables (`{0}`, `{1}`, `%s`, etc.)
- **HTML/Markdown** - Conservez les balises HTML et le formatage Markdown
- **Liens** - Conservez les URL inchangées à moins qu'il n'y ait une version localisée
- **Abréviations** - Déterminez si vous devez traduire ou conserver l'original (ex. : "KB/s", "HTTP")

### Tester Vos Traductions

Si vous avez accès à un routeur I2P :

1. Téléchargez les derniers fichiers de traduction de Transifex
2. Placez-les dans votre installation I2P
3. Redémarrez la console du routeur
4. Vérifiez les traductions dans leur contexte
5. Signalez tout problème ou amélioration nécessaire

## Obtenir de l'Aide

### Support Communautaire

- **Canal IRC** : `#i2p-dev` sur I2P IRC ou OFTC
- **Forum** : Forums de développement I2P
- **Commentaires Transifex** : Posez des questions directement sur les chaînes de traduction

### Questions Courantes

**Q : À quelle fréquence devrais-je traduire ?**
Traduisez à votre rythme. Même traduire quelques chaînes aide. Le projet est en cours.

**Q : Que faire si ma langue n'est pas listée ?**
Demandez une nouvelle langue sur Transifex. S'il y a de la demande, l'équipe l'ajoutera.

**Q : Puis-je traduire seul ou ai-je besoin d'une équipe ?**
Vous pouvez commencer seul. À mesure que d'autres traducteurs rejoignent votre langue, vous pouvez collaborer.

**Q : Comment savoir ce qu'il faut traduire ?**
Transifex affiche les pourcentages de complétion et met en évidence les chaînes non traduites.

**Q : Que faire si je ne suis pas d'accord avec une traduction existante ?**
Suggérez des améliorations dans Transifex. Les réviseurs évalueront les changements.

## Avancé : Traduction Manuelle (Optionnel)

Pour les traducteurs expérimentés qui souhaitent un accès direct aux fichiers sources :

### Exigences

- **Git** - Système de contrôle de version
- **POEdit** ou éditeur de texte - Pour éditer les fichiers `.po`
- **Connaissance de base de la ligne de commande**

### Processus

1. **Clonez le dépôt** :
   ```bash
   git clone https://i2pgit.org/i2p-hackers/i2p.i2p.git
   ```

2. **Trouvez les fichiers de traduction** :
   - Console du routeur : `apps/routerconsole/locale/`
   - Cherchez `messages_xx.po` (où `xx` est votre code langue)

3. **Éditez les traductions** :
   - Utilisez POEdit ou un éditeur de texte
   - Enregistrez avec l'encodage UTF-8

4. **Testez localement** (si vous avez installé I2P)

5. **Soumettez les changements** :
   - Créez une demande de fusion sur [I2P Git](https://i2pgit.org/)
   - Ou partagez votre fichier `.po` avec l'équipe de développement

**Note** : La plupart des traducteurs devraient utiliser Transifex. La traduction manuelle est réservée à ceux à l'aise avec Git et les flux de travail de développement.

## Merci

Chaque traduction aide à rendre I2P plus accessible aux utilisateurs du monde entier. Que vous traduisiez quelques chaînes ou des sections entières, votre contribution fait une réelle différence pour aider les gens à protéger leur vie privée en ligne.

**Prêt à commencer ?** [Rejoignez I2P sur Transifex →](https://explore.transifex.com/otf/I2P/)
