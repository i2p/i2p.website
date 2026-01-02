---
title: "Installer I2P sur macOS (La méthode longue)"
description: "Guide étape par étape pour installer manuellement I2P et ses dépendances sur macOS"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Ce dont vous aurez besoin

- Un Mac fonctionnant sous macOS 10.14 (Mojave) ou version ultérieure
- Accès administrateur pour installer des applications
- Environ 15 à 20 minutes
- Connexion Internet pour télécharger les installateurs

## Vue d'ensemble

Ce processus d'installation comporte quatre étapes principales :

1. **Installer Java** - Téléchargez et installez Oracle Java Runtime Environment
2. **Installer I2P** - Téléchargez et exécutez le programme d'installation I2P
3. **Configurer l'application I2P** - Configurez le lanceur et ajoutez-le à votre dock
4. **Configurer la bande passante I2P** - Lancez l'assistant de configuration pour optimiser votre connexion

## Première partie : Installer Java

I2P nécessite Java pour fonctionner. Si vous avez déjà Java 8 ou une version ultérieure installée, vous pouvez [passer directement à la deuxième partie](#part-two-download-and-install-i2p).

### Step 1: Download Java

Visitez la [page de téléchargement Oracle Java](https://www.oracle.com/java/technologies/downloads/) et téléchargez l'installateur macOS pour Java 8 ou version ultérieure.

![Télécharger Oracle Java pour macOS](/images/guides/macos-install/0-jre.png)

### Step 2: Run the Installer

Localisez le fichier `.dmg` téléchargé dans votre dossier Téléchargements et double-cliquez pour l'ouvrir.

![Ouvrir l'installateur Java](/images/guides/macos-install/1-jre.png)

### Step 3: Allow Installation

macOS peut afficher une invite de sécurité car l'installateur provient d'un développeur identifié. Cliquez sur **Ouvrir** pour continuer.

![Autoriser l'installateur à continuer](/images/guides/macos-install/2-jre.png)

### Étape 1 : Télécharger Java

Cliquez sur **Install** pour commencer le processus d'installation de Java.

![Commencer l'installation de Java](/images/guides/macos-install/3-jre.png)

### Étape 2 : Exécuter l'installateur

L'installateur copiera les fichiers et configurera Java sur votre système. Cela prend généralement 1 à 2 minutes.

![Attendez que le programme d'installation se termine](/images/guides/macos-install/4-jre.png)

### Étape 3 : Autoriser l'installation

Lorsque vous voyez le message de réussite, Java est installé ! Cliquez sur **Fermer** pour terminer.

![Installation de Java terminée](/images/guides/macos-install/5-jre.png)

## Part Two: Download and Install I2P

Maintenant que Java est installé, vous pouvez installer le routeur I2P.

### Étape 4 : Installer Java

Visitez la [page Téléchargements](/downloads/) et téléchargez l'installateur **I2P pour Unix/Linux/BSD/Solaris** (le fichier `.jar`).

![Télécharger l'installateur I2P](/images/guides/macos-install/0-i2p.png)

### Étape 5 : Attendre l'installation

Double-cliquez sur le fichier `i2pinstall_X.X.X.jar` téléchargé. Le programme d'installation se lancera et vous demandera de sélectionner votre langue préférée.

![Sélectionnez votre langue](/images/guides/macos-install/1-i2p.png)

### Étape 6 : Installation terminée

Lisez le message de bienvenue et cliquez sur **Suivant** pour continuer.

![Introduction de l'installateur](/images/guides/macos-install/2-i2p.png)

### Step 4: Important Notice

L'installateur affichera un avis important concernant les mises à jour. Les mises à jour I2P sont **signées et vérifiées de bout en bout**, même si cet installateur lui-même n'est pas signé. Cliquez sur **Suivant**.

![Avis important concernant les mises à jour](/images/guides/macos-install/3-i2p.png)

### Étape 1 : Télécharger I2P

Lisez le contrat de licence I2P (licence de type BSD). Cliquez sur **Suivant** pour accepter.

![Accord de licence](/images/guides/macos-install/4-i2p.png)

### Étape 2 : Exécuter l'Installateur

Choisissez l'emplacement d'installation d'I2P. L'emplacement par défaut (`/Applications/i2p`) est recommandé. Cliquez sur **Suivant**.

![Sélectionner le répertoire d'installation](/images/guides/macos-install/5-i2p.png)

### Étape 3 : Écran de bienvenue

Laissez tous les composants sélectionnés pour une installation complète. Cliquez sur **Suivant**.

![Sélectionner les composants à installer](/images/guides/macos-install/6-i2p.png)

### Étape 4 : Avis Important

Vérifiez vos choix et cliquez sur **Suivant** pour commencer l'installation d'I2P.

![Démarrer l'installation](/images/guides/macos-install/7-i2p.png)

### Étape 5 : Accord de licence

L'installateur copiera les fichiers I2P sur votre système. Cela prend environ 1 à 2 minutes.

![Installation en cours](/images/guides/macos-install/8-i2p.png)

### Étape 6 : Sélectionner le répertoire d'installation

L'installateur crée des scripts de lancement pour démarrer I2P.

![Génération des scripts de lancement](/images/guides/macos-install/9-i2p.png)

### Étape 7 : Sélectionner les composants

L'installateur propose de créer des raccourcis sur le bureau et des entrées de menu. Effectuez vos sélections et cliquez sur **Suivant**.

![Créer des raccourcis](/images/guides/macos-install/10-i2p.png)

### Étape 8 : Démarrer l'installation

Succès ! I2P est maintenant installé. Cliquez sur **Terminé** pour finaliser.

![Installation terminée](/images/guides/macos-install/11-i2p.png)

## Part Three: Configure I2P App

Maintenant, facilitons le lancement d'I2P en l'ajoutant à votre dossier Applications et au Dock.

### Étape 9 : Installation des fichiers

Ouvrez le Finder et naviguez vers votre dossier **Applications**.

![Ouvrir le dossier Applications](/images/guides/macos-install/0-conf.png)

### Étape 10 : Générer les scripts de lancement

Recherchez le dossier **I2P** ou l'application **Start I2P Router** dans `/Applications/i2p/`.

![Trouver le lanceur I2P](/images/guides/macos-install/1-conf.png)

### Étape 11 : Raccourcis d'installation

Faites glisser l'application **Start I2P Router** vers votre Dock pour un accès facile. Vous pouvez également créer un alias sur votre bureau.

![Ajouter I2P à votre Dock](/images/guides/macos-install/2-conf.png)

**Astuce** : Faites un clic droit sur l'icône I2P dans le Dock et sélectionnez **Options → Garder dans le Dock** pour la rendre permanente.

## Part Four: Configure I2P Bandwidth

Lorsque vous lancez I2P pour la première fois, vous passerez par un assistant de configuration pour paramétrer vos réglages de bande passante. Cela permet d'optimiser les performances d'I2P pour votre connexion.

### Étape 12 : Installation terminée

Cliquez sur l'icône I2P dans votre Dock (ou double-cliquez sur le lanceur). Votre navigateur web par défaut s'ouvrira sur la Console du Routeur I2P.

![Écran d'accueil de la console du routeur I2P](/images/guides/macos-install/0-wiz.png)

### Step 2: Welcome Wizard

L'assistant de configuration vous accueillera. Cliquez sur **Next** pour commencer à configurer I2P.

![Introduction de l'assistant de configuration](/images/guides/macos-install/1-wiz.png)

### Étape 1 : Ouvrir le dossier Applications

Sélectionnez votre **langue d'interface** préférée et choisissez entre le thème **clair** ou **sombre**. Cliquez sur **Suivant**.

![Sélectionner la langue et le thème](/images/guides/macos-install/2-wiz.png)

### Étape 2 : Trouver le lanceur I2P

L'assistant expliquera le test de bande passante. Ce test se connecte au service **M-Lab** pour mesurer votre vitesse internet. Cliquez sur **Suivant** pour continuer.

![Explication du test de bande passante](/images/guides/macos-install/3-wiz.png)

### Étape 3 : Ajouter au Dock

Cliquez sur **Run Test** pour mesurer vos vitesses de téléchargement ascendant et descendant. Le test dure environ 30 à 60 secondes.

![Exécution du test de bande passante](/images/guides/macos-install/4-wiz.png)

### Step 6: Test Results

Examinez vos résultats de test. I2P recommandera des paramètres de bande passante en fonction de la vitesse de votre connexion.

![Résultats du test de bande passante](/images/guides/macos-install/5-wiz.png)

### Étape 1 : Lancer I2P

Choisissez la quantité de bande passante que vous souhaitez partager avec le réseau I2P :

- **Automatique** (Recommandé) : I2P gère la bande passante en fonction de votre utilisation
- **Limitée** : Définir des limites spécifiques de téléversement/téléchargement
- **Illimitée** : Partager autant que possible (pour les connexions rapides)

Cliquez sur **Suivant** pour enregistrer vos paramètres.

![Configurer le partage de bande passante](/images/guides/macos-install/6-wiz.png)

### Étape 2 : Assistant de bienvenue

Votre routeur I2P est maintenant configuré et en fonctionnement ! La console du routeur affichera l'état de votre connexion et vous permettra de naviguer sur les sites I2P.

## Getting Started with I2P

Maintenant que I2P est installé et configuré, vous pouvez :

1. **Parcourir les sites I2P** : Visitez la [page d'accueil I2P](http://127.0.0.1:7657/home) pour voir les liens vers les services I2P populaires
2. **Configurer votre navigateur** : Créez un [profil de navigateur](/docs/guides/browser-config) pour accéder aux sites `.i2p`
3. **Explorer les services** : Découvrez le courrier électronique I2P, les forums, le partage de fichiers et bien plus encore
4. **Surveiller votre router** : La [console](http://127.0.0.1:7657/console) affiche l'état de votre réseau et les statistiques

### Étape 3 : Langue et Thème

- **Console du routeur** : [http://127.0.0.1:7657/](http://127.0.0.1:7657/)
- **Configuration** : [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)
- **Carnet d'adresses** : [http://127.0.0.1:7657/susidns/addressbook](http://127.0.0.1:7657/susidns/addressbook)
- **Paramètres de bande passante** : [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config)

## Re-running the Setup Wizard

Si vous souhaitez modifier vos paramètres de bande passante ou reconfigurer I2P ultérieurement, vous pouvez relancer l'assistant de bienvenue depuis la Console du routeur :

1. Allez sur [l'assistant de configuration I2P](http://127.0.0.1:7657/welcome)
2. Suivez à nouveau les étapes de l'assistant

## Troubleshooting

### Étape 4 : Informations sur le test de bande passante

- **Vérifier Java** : Assurez-vous que Java est installé en exécutant `java -version` dans le Terminal
- **Vérifier les permissions** : Assurez-vous que le dossier I2P dispose des permissions correctes
- **Vérifier les logs** : Consultez `~/.i2p/wrapper.log` pour les messages d'erreur

### Étape 5 : Exécuter le test de bande passante

- Assurez-vous qu'I2P est en cours d'exécution (vérifiez la Console du Router)
- Configurez les paramètres proxy de votre navigateur pour utiliser le proxy HTTP `127.0.0.1:4444`
- Patientez 5 à 10 minutes après le démarrage pour qu'I2P s'intègre au réseau

### Étape 6 : Résultats des tests

- Exécutez à nouveau le test de bande passante et ajustez vos paramètres
- Assurez-vous de partager de la bande passante avec le réseau
- Vérifiez l'état de votre connexion dans la Console du Router

## Partie Deux : Télécharger et Installer I2P

Pour supprimer I2P de votre Mac :

1. Quittez le routeur I2P s'il est en cours d'exécution
2. Supprimez le dossier `/Applications/i2p`
3. Supprimez le dossier `~/.i2p` (votre configuration et vos données I2P)
4. Retirez l'icône I2P de votre Dock

## Next Steps

- **Rejoignez la communauté** : Visitez [i2pforum.net](http://i2pforum.net) ou consultez I2P sur Reddit
- **En savoir plus** : Lisez la [documentation I2P](/en/docs) pour comprendre le fonctionnement du réseau
- **Participez** : Envisagez de [contribuer au développement d'I2P](/en/get-involved) ou d'héberger de l'infrastructure

Félicitations ! Vous faites maintenant partie du réseau I2P. Bienvenue sur l'internet invisible !

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.
